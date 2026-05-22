"""CLI principale per il confronto tra agenti AI."""

import sys
import typer
from rich import print as rprint
from rich.console import Console
from typing import Optional


from src.agents.compare import compare_agents
from src.agents.smol_wrapper import SmolAgentWrapper
from src.agents.tiny_wrapper import TinyAgentWrapper

# Crea l'app Typer con metadati
app = typer.Typer(
    name="agent-cli",
    help="CLI demo: Typer + confronto agenti AI",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()


@app.command()
def run_smol(
    prompt: str = typer.Argument(..., help="Il prompt da processare"),
    steps: int = typer.Option(3, "--steps", "-s", min=1, max=10, help="Numero di passi dell'agente"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mostra output dettagliato"),
):
    """
    Esegui uno workflow semplice con SmolAgents.
    
    Esempio: python -m src.cli run-smol "Riassumi questo testo" --steps 5
    """
    try:
        rprint("[bold cyan]Inizializzazione SmolAgents...[/bold cyan]")
        agent = SmolAgentWrapper(max_steps=steps)
        
        with console.status("[bold green]Elaborazione in corso...[/bold green]"):
            result = agent.run(prompt)
        
        rprint("\n[bold green]✅ SmolAgents result:[/bold green]")
        
        if verbose:
            rprint(f"[dim]Prompt originale:[/dim] {result['state']['prompt'][:100]}...")
            rprint(f"\n[dim]Trace dettagliato:[/dim]")
            for i, step in enumerate(result['state']['trace'], 1):
                rprint(f"  Step {i}: {step}")
            rprint(f"\n[dim]Risultato finale:[/dim] {result['state']['final'][:200]}...")
        else:
            rprint(f"[green]{result['state']['final'][:200]}...[/green]")
        
        rprint(f"\n[bold yellow]Tempo di esecuzione:[/bold yellow] {result['time_s']:.4f}s")
        
    except Exception as e:
        rprint(f"[bold red]❌ Errore durante l'esecuzione:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def run_tiny(
    prompt: str = typer.Argument(..., help="Il prompt da processare"),
    steps: int = typer.Option(3, "--steps", "-s", min=1, max=10, help="Numero di passi dell'agente"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mostra output dettagliato"),
):
    """
    Esegui uno workflow semplice con TinyAgent (libreria alternativa).
    
    Esempio: python -m src.cli run-tiny "Riassumi questo testo" --steps 4
    """
    try:
        rprint("[bold cyan]Inizializzazione TinyAgent...[/bold cyan]")
        agent = TinyAgentWrapper(max_steps=steps)
        
        with console.status("[bold blue]Elaborazione in corso...[/bold blue]"):
            result = agent.run(prompt)
        
        rprint("\n[bold blue]✅ TinyAgent result:[/bold blue]")
        
        if verbose:
            rprint(f"[dim]Prompt originale:[/dim] {result['state']['prompt'][:100]}...")
            rprint(f"\n[dim]Trace dettagliato:[/dim]")
            for i, step in enumerate(result['state']['trace'], 1):
                rprint(f"  Step {i}: {step}")
            rprint(f"\n[dim]Risultato finale:[/dim] {result['state']['final'][:200]}...")
        else:
            rprint(f"[blue]{result['state']['final'][:200]}...[/blue]")
        
        rprint(f"\n[bold yellow]Tempo di esecuzione:[/bold yellow] {result['time_s']:.4f}s")
        
    except Exception as e:
        rprint(f"[bold red]❌ Errore durante l'esecuzione:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def compare(
    prompt: str = typer.Argument(..., help="Il prompt da processare"),
    steps: int = typer.Option(3, "--steps", "-s", min=1, max=10, help="Numero di passi dell'agente"),
    repeat: int = typer.Option(1, "--repeat", "-r", min=1, max=10, help="Numero di ripetizioni per statistica"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Esporta risultati in file JSON"),
):
    """
    Confronta i due agent su uno stesso prompt, mostrando output e tempi.
    
    Esempio: python -m src.cli compare "Riassumi questo testo" --steps 5 --repeat 3
    """
    try:
        with console.status("[bold yellow]Confronto in corso...[/bold yellow]"):
            results = compare_agents(prompt, steps=steps, repeat=repeat, export_path=export)
        
        rprint("\n[bold green]✅ Confronto completato![/bold green]")
        
        if export:
            rprint(f"[dim]Risultati esportati in:[/dim] [yellow]{export}[/yellow]")
            
    except Exception as e:
        rprint(f"[bold red]❌ Errore durante il confronto:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-V", help="Mostra la versione"),
):
    """Callback principale per opzioni globali."""
    if version:
        rprint(f"[bold]typer-smol-agents-demo[/bold] v{__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()