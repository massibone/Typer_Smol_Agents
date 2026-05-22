"""
Modulo agents: wrapper e funzioni di confronto per agenti AI.
"""

from src.agents.smol_wrapper import SmolAgentWrapper
from src.agents.tiny_wrapper import TinyAgentWrapper
from src.agents.compare import compare_agents

__all__ = [
    "SmolAgentWrapper",
    "TinyAgentWrapper",
    "compare_agents",
]