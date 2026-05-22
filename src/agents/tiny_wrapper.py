"""Wrapper per TinyAgent (libreria alternativa fittizia) con interfaccia comune."""

import time
import random
import statistics
from typing import Any, Dict, List, Optional


class TinyAgentError(Exception):
    """Errore specifico per TinyAgent."""
    pass


class TinyAgentWrapper:
    """
    Wrapper per TinyAgent (libreria alternativa per confronto).
    
    Sostituire le simulazioni con chiamate reali all'API della libreria alternativa.
    Mantenere l'interfaccia comune per permettere il confronto.
    
    Args:
        max_steps: Numero massimo di passi di elaborazione
        model: Modello da utilizzare (se applicabile)
    """
    
    def __init__(self, max_steps: int = 3, model: str = "default"):
        """
        Inizializza il wrapper.
        
        Esempio di inizializzazione reale:
        ```python
        from tinyagent import Agent
        self._agent = Agent(model=model)
        ```
        """
        if max_steps < 1:
            raise TinyAgentError("max_steps deve essere >= 1")
        
        self.max_steps = max_steps
        self.model = model
        self._agent = None  # Sostituire con agente reale
        self._initialized = False
    
    def _initialize(self) -> None:
        """
        Inizializza l'agente reale.
        Da implementare quando si usa la libreria reale.
        """
        self._initialized = True
    
    def _simulate_step(self, step: int, prompt: str) -> str:
        """
        Simula un passo di elaborazione con comportamento diverso da SmolAgents.
        Sostituire con chiamata reale all'agente.
        """
        # Simula elaborazione diversa per mostrare variazione
        length_analysis = f"lunghezza={len(prompt)} caratteri"
        operations = [
            f"Tokenizzazione e preprocessing del prompt ({length_analysis})",
            f"Estrazione features: rilevati {random.randint(2, 8)} pattern",
            f"Applicazione trasformazione step {step}",
            f"Post-processing e normalizzazione output",
        ]
        
        operation = operations[(step - 1) % len(operations)]
        return f"TinyStep {step}: {operation}"
    
    def run(self, prompt: str) -> Dict[str, Any]:
        """
        Esegue l'agente sul prompt fornito.
        
        Args:
            prompt: Testo del prompt da processare
            
        Returns:
            Dict con chiavi: agent, time_s, state (prompt, trace, final)
            
        Raises:
            TinyAgentError: Se il prompt è vuoto o l'esecuzione fallisce
        """
        if not prompt or not prompt.strip():
            raise TinyAgentError("Il prompt non può essere vuoto")
        
        if not self._initialized:
            self._initialize()
        
        start_time = time.perf_counter()
        
        try:
            # Simulazione: sostituire con chiamata reale
            # Esempio reale: result = self._agent.process(prompt)
            
            # Simula tempo di elaborazione leggermente diverso
            processing_time = random.uniform(0.15, 0.35) * self.max_steps
            time.sleep(processing_time * 0.01)  # Scala per demo veloce
            
            trace = []
            for i in range(1, self.max_steps + 1):
                step_output = self._simulate_step(i, prompt)
                trace.append(step_output)
            
            # Genera risultato finale simulato (diverso da SmolAgents)
            final_output = (
                f"Output generato da TinyAgent (modello {self.model}):\n"
                f"Prompt: {prompt[:50]}...\n"
                f"Elaborazione completata in {self.max_steps} passi\n"
                f"Risultato: risposta alternativa per '{prompt[:30]}...'"
            )
            
            execution_time = time.perf_counter() - start_time
            
            return {
                "agent": "TinyAgent",
                "time_s": execution_time,
                "state": {
                    "prompt": prompt,
                    "trace": trace,
                    "final": final_output,
                },
                "metadata": {
                    "max_steps": self.max_steps,
                    "model": self.model,
                }
            }
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            raise TinyAgentError(
                f"Errore durante l'esecuzione (tempo: {execution_time:.4f}s): {str(e)}"
            )
    
    def __repr__(self) -> str:
        return f"TinyAgentWrapper(max_steps={self.max_steps}, model={self.model})"