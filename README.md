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
# output
 python -m src.cli --version
Usage: python -m src.cli [OPTIONS] COMMAND [ARGS]...
Try 'python -m src.cli --help' for help.
│ Missing command.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
PS C:\Users\D79197\OneDrive - Comune di FIRENZE\Documenti\PYTHON_PROJECT\broadcastSite\typer_smol_agents> python -m src.cli run-smol "Test veloce"
Inizializzazione SmolAgents...

✅ SmolAgents result:
Output generato da SmolAgents (modello simulato):
Prompt: Test veloce...
Elaborazione completata in 3 passi
Risultato: risposta simulata per 'Test veloce...'...

Tempo di esecuzione: 0.0049s
PS C:\Users\D79197\OneDrive - Comune di FIRENZE\Documenti\PYTHON_PROJECT\broadcastSite\typer_smol_agents> python -m src.cli compare "Riassumi questo testo" --steps 4 --repeat 3


                                      🤖 Confronto Agenti                                       
                 Prompt: 'Riassumi questo testo...' | Passi: 4 | Ripetizioni: 3                 
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Agente         ┃  Media (s)  ┃  Dev. Std  ┃  Min (s)  ┃  Max (s)  ┃  Primo Trace            ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  🧠 SmolAgents  │     0.0098  │    0.0019  │   0.0077  │   0.0116  │  Step 1: Analisi        │
│                 │             │            │           │           │  semantica del prompt   │
│                 │             │            │           │           │  (lunghezza=21...       │
│  ⚡ TinyAgent   │     0.0104  │    0.0017  │   0.0090  │   0.0123  │  TinyStep 1:            │
│                 │             │            │           │           │  Tokenizzazione e       │
│                 │             │            │           │           │  preprocessing del      │
│                 │             │            │           │           │  pro...                 │
└─────────────────┴─────────────┴────────────┴───────────┴───────────┴─────────────────────────┘


╭──────────────────────────────────── Dettaglio SmolAgents ────────────────────────────────────╮
│ SmolAgents                                                                                   │
│ Tempi: 11.55ms, 7.68ms, 10.03ms                                                              │
│ Media: 9.76ms ± 1.95ms                                                                       │
│ Range: [7.68ms - 11.55ms]                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────── Dettaglio TinyAgent ─────────────────────────────────────╮
│ TinyAgent                                                                                    │
│ Tempi: 9.82ms, 12.27ms, 9.03ms                                                               │
│ Media: 10.37ms ± 1.69ms                                                                      │
│ Range: [9.03ms - 12.27ms]                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯

🏆 Vincitore velocità: SmolAgents (618μs più veloce, x1.06 speedup)

✅ Confronto completato!
PS C:\Users\D79197\OneDrive - Comune di FIRENZE\Documenti\PYTHON_PROJECT\broadcastSite\typer_smol_agents> 
 *  History restored 

PS C:\Users\D79197\OneDrive - Comune di FIRENZE\Documenti\PYTHON_PROJECT\broadcastSite\typer_smol_agents> python -m src.cli compare "Riassumi questo testo" --steps 4 --repeat 3


                                🤖 Confronto Agenti                                 
           Prompt: 'Riassumi questo testo...' | Passi: 4 | Ripetizioni: 3           
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┓┃                 ┃             ┃            ┃           ┃           ┃  Primo      ┃┃  Agente         ┃  Media (s)  ┃  Dev. Std  ┃  Min (s)  ┃  Max (s)  ┃  Trace      ┃┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━┩│  🧠 SmolAgents  │     0.0081  │    0.0027  │   0.0050  │   0.0099  │  Step 1:    ││                 │             │            │           │           │  Analisi    ││                 │             │            │           │           │  semantica  ││                 │             │            │           │           │  del        ││                 │             │            │           │           │  prompt     ││                 │             │            │           │           │  (lunghezz  ││                 │             │            │           │           │  a=21...    ││  ⚡ TinyAgent   │     0.0110  │    0.0028  │   0.0078  │   0.0132  │  TinyStep   ││                 │             │            │           │           │  1:         ││                 │             │            │           │           │  Tokenizza  ││                 │             │            │           │           │  zione e    ││                 │             │            │           │           │  preproces  ││                 │             │            │           │           │  sing del   ││                 │             │            │           │           │  pro...     │└─────────────────┴─────────────┴────────────┴───────────┴───────────┴─────────────┘

╭────────────────────────────── Dettaglio SmolAgents ──────────────────────────────╮│ SmolAgents                                                                       ││ Tempi: 9.33ms, 5.01ms, 9.94ms                                                    ││ Media: 8.09ms ± 2.69ms                                                           ││ Range: [5.01ms - 9.94ms]                                                         │╰──────────────────────────────────────────────────────────────────────────────────╯╭────────────────────────────── Dettaglio TinyAgent ───────────────────────────────╮│ TinyAgent                                                                        ││ Tempi: 7.80ms, 11.98ms, 13.19ms                                                  ││ Media: 10.99ms ± 2.83ms                                                          ││ Range: [7.80ms - 13.19ms]                                                        │╰──────────────────────────────────────────────────────────────────────────────────╯
🏆 Vincitore velocità: SmolAgents (2.90ms più veloce, x1.36 speedup)

✅ Confronto completato!
