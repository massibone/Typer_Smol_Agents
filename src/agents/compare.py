"""Funzioni per confrontare i diversi agenti."""

import json
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from src.agents.smol_wrapper import SmolAgentWrapper
from src.agents.tiny_wrapper import TinyAgentWrapper

console = Console()


class ComparisonError(Exception):
    """Errore durante il confronto degli agenti."""
    pass


def _format_time(seconds: float) -> str:
    """Formatta il tempo in modo leggibile."""
    if seconds < 0.001:
        return f"{seconds * 1000000:.0f}μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.4f}s"


def _run_single_comparison(
    agent_cls: type,
    prompt: str,
    steps: int,
    repeats: int,
) -> Dict[str, Any]:
    """
    Esegue una serie di ripetizioni per un singolo agente.
    
    Returns:
        Dict con statistiche e ultimo risultato
    """
    times = []
    last_result = None
    
    for _ in range(repeats):
        agent = agent_cls(max_steps=steps)
        result = agent.run(prompt)
        times.append(result["time_s"])
        last_result = result
    
    # Calcola statistiche
    avg_time = statistics.mean(times)
    std_time = statistics.stdev(times) if len(times) > 1 else 0.0
    min_time = min(times)
    max_time = max(times)
    
    return {
        "agent_name": last_result["agent"],
        "times": times,
        "statistics": {
            "mean": avg_time,
            "std": std_time,
            "min": min_time,
            "max": max_time,
            "total": sum(times),
        },
        "last_result": last_result,
    }


def compare_agents(
    prompt: str,
    steps: int = 3,
    repeat: int = 1,
    export_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Confronta SmolAgents e TinyAgent sullo stesso prompt.
    
    Args:
        prompt: Prompt da processare
        steps: Numero di passi per agente
        repeat: Numero di ripetizioni per statistica
        export_path: Path opzionale per esportare risultati in JSON
        
    Returns:
        Dict con tutti i risultati del confronto
    """
    if not prompt or not prompt.strip():
        raise ComparisonError("Il prompt non può essere vuoto")
    
    if repeat < 1:
        raise ComparisonError("repeat deve essere >= 1")
    
    # Crea tabella risultati
    results_table = Table(
        title=f"🤖 Confronto Agenti\n[dim]Prompt: '{prompt[:50]}...' | Passi: {steps} | Ripetizioni: {repeat}[/dim]",
        title_justify="center",
        padding=(0, 2),
    )
    
    results_table.add_column("Agente", style="cyan", no_wrap=True)
    results_table.add_column("Media (s)", justify="right", style="green")
    results_table.add_column("Dev. Std", justify="right", style="yellow")
    results_table.add_column("Min (s)", justify="right")
    results_table.add_column("Max (s)", justify="right")
    results_table.add_column("Primo Trace", overflow="fold")
    
    # Esegui confronto
    all_results = {}
    
    for agent_cls, emoji in [
        (SmolAgentWrapper, "🧠"),
        (TinyAgentWrapper, "⚡"),
    ]:
        try:
            agent_result = _run_single_comparison(
                agent_cls, prompt, steps, repeat
            )
            
            stats = agent_result["statistics"]
            first_trace = (
                agent_result["last_result"]["state"]["trace"][0]
                if agent_result["last_result"]["state"]["trace"]
                else "N/A"
            )
            
            results_table.add_row(
                f"{emoji} {agent_result['agent_name']}",
                f"{stats['mean']:.4f}",
                f"{stats['std']:.4f}",
                f"{stats['min']:.4f}",
                f"{stats['max']:.4f}",
                first_trace[:50] + "...",
            )
            
            all_results[agent_result['agent_name']] = agent_result
            
        except Exception as e:
            console.print(f"[bold red]Errore con {agent_cls.__name__}:[/bold red] {str(e)}")
            results_table.add_row(
                f"❌ {agent_cls.__name__}",
                "ERRORE",
                "-",
                "-",
                "-",
                str(e)[:50],
            )
    
    # Stampa tabella
    console.print("\n")
    console.print(results_table)
    console.print("\n")
    
    # Mostra dettagli se repeat > 1
    if repeat > 1:
        for agent_name, agent_data in all_results.items():
            times_str = ", ".join([_format_time(t) for t in agent_data["times"]])
            stats = agent_data["statistics"]
            
            info_panel = Panel(
                f"[bold]{agent_name}[/bold]\n"
                f"Tempi: [yellow]{times_str}[/yellow]\n"
                f"Media: [green]{_format_time(stats['mean'])}[/green] ± "
                f"[yellow]{_format_time(stats['std'])}[/yellow]\n"
                f"Range: [{_format_time(stats['min'])} - {_format_time(stats['max'])}]",
                title=f"Dettaglio {agent_name}",
                border_style="blue",
            )
            console.print(info_panel)
    
    # Determina vincitore se possibile
    if len(all_results) == 2:
        smol_stats = all_results["SmolAgents"]["statistics"]
        tiny_stats = all_results["TinyAgent"]["statistics"]
        
        if smol_stats["mean"] < tiny_stats["mean"]:
            diff = tiny_stats["mean"] - smol_stats["mean"]
            winner = "SmolAgents"
            speedup = (tiny_stats["mean"] / smol_stats["mean"]) if smol_stats["mean"] > 0 else float('inf')
        else:
            diff = smol_stats["mean"] - tiny_stats["mean"]
            winner = "TinyAgent"
            speedup = (smol_stats["mean"] / tiny_stats["mean"]) if tiny_stats["mean"] > 0 else float('inf')
        
        console.print(
            f"\n[bold cyan]🏆 Vincitore velocità: {winner}[/bold cyan] "
            f"([green]{_format_time(diff)}[/green] più veloce, "
            f"x{speedup:.2f} speedup)"
        )
    
    # Prepara risultati per export
    export_data = {
        "metadata": {
            "prompt": prompt,
            "steps": steps,
            "repeats": repeat,
            "timestamp": __import__('datetime').datetime.now().isoformat(),
        },
        "results": {}
    }
    
    for agent_name, agent_data in all_results.items():
        export_data["results"][agent_name] = {
            "statistics": agent_data["statistics"],
            "last_result": agent_data["last_result"],
        }
    
    # Esporta se richiesto
    if export_path:
        export_file = Path(export_path)
        export_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepara dati JSON (rimuovi datetime non serializzabile)
        export_json = json.dumps(export_data, indent=2, default=str)
        
        export_file.write_text(export_json, encoding="utf-8")
        console.print(f"\n[green]✅ Risultati esportati in:[/green] {export_file.absolute()}")
        
        # Mostra anteprima
        preview = export_json[:500]
        console.print(Panel(
            Syntax(preview, "json", theme="monokai", line_numbers=False),
            title="Anteprima export JSON",
            border_style="green",
        ))
    
    return export_data