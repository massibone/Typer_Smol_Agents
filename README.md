# Typer_Smol_Agents

Esempio didattico che mostra come:
- Usare **Typer** per trasformare funzioni Python in una CLI pulita
- Integrare e confrontare due semplici "agent workflows" usando wrapper
- Creare un'interfaccia comune per confrontare diverse implementazioni

## Struttura del Repository
typer_smol_agents/
├── src/
│   ├── cli.py             # CLI principale con Typer
│   ├── agents/
│   │   ├── smol_wrapper.py # Wrapper per SmolAgents
│   │   ├── tiny_wrapper.py # Wrapper per TinyAgent
│   │   └── compare.py      # Logica di confronto statistico
│   └── examples/
│       └── simple_task.py
├── pyproject.toml
├── requirements.txt
└── README.md
Installazione
Installazione standard
Bash
pip install -e .
Installazione con dipendenze opzionali
Bash
# Con SmolAgents
pip install -e ".[smolagents]"

# Con TinyAgent
pip install -e ".[tinyagent]"

# Tutte le dipendenze
pip install -e ".[smolagents,tinyagent,test]"
Utilizzo
Eseguire gli Agenti
Bash
# SmolAgents
python -m src.cli run-smol "Riassumi questo testo" --steps 4

# TinyAgent
python -m src.cli run-tiny "Riassumi questo testo" --steps 4 --verbose
Confrontare i due agenti
Bash
python -m src.cli compare "Riassumi questo testo" --steps 4 --repeat 3

# Esportare i risultati in JSON
python -m src.cli compare "Testo lungo..." --repeat 5 --export results.json
Supporto File (Roadmap)
È previsto a breve l'aggiornamento per il caricamento di file di testo:

Bash
python -m src.cli run-smol --file documento.txt --steps 4
Come estendere con API Reali
Ogni wrapper deve implementare un'interfaccia comune che restituisca il dizionario: {"agent": str, "time_s": float, "state": dict}.

Esempio per SmolAgents:

Python
class SmolAgentWrapper:
    def run(self, prompt):
        start = time.perf_counter()
        response = self._agent.generate(prompt)
        execution_time = time.perf_counter() - start
        return {
            "agent": "SmolAgents",
            "time_s": execution_time,
            "state": {"prompt": prompt, "final": response["text"]}
        }
Test
Bash
pip install -e ".[test]"
pytest
Licenza
MIT

Come inizializzare subito il progetto
Bash
# Clona o crea la cartella
mkdir typer-smol-agents
cd typer-smol-agents

# Crea la struttura
mkdir -p src/agents src/examples tests

# Installa in modalità sviluppo
pip install -e .

# Verifica il funzionamento
python -m src.cli --help
