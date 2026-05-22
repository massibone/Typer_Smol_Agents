"""
Esempio di task che gli agenti dovrebbero svolgere.

Questo modulo fornisce funzioni di utilità per creare prompt di esempio
per testare gli agenti.
"""

from typing import List, Optional


def make_summary_prompt(text: str, max_words: Optional[int] = None) -> str:
    """
    Crea un prompt per riassumere un testo.
    
    Args:
        text: Testo da riassumere
        max_words: Numero massimo di parole per il riassunto
        
    Returns:
        Prompt formattato per il riassunto
    """
    limit = f" (massimo {max_words} parole)" if max_words else ""
    return f"Riassumi questo testo{limit}:\n\n{text}"


def make_qa_prompt(question: str, context: Optional[str] = None) -> str:
    """
    Crea un prompt per domanda-risposta.
    
    Args:
        question: Domanda da porre
        context: Contesto opzionale per la risposta
        
    Returns:
        Prompt formattato per Q&A
    """
    if context:
        return f"Contesto:\n{context}\n\nDomanda: {question}\n\nRisposta:"
    return f"Domanda: {question}\n\nRisposta:"


def make_translation_prompt(text: str, target_language: str = "italiano") -> str:
    """
    Crea un prompt per traduzione.
    
    Args:
        text: Testo da tradurre
        target_language: Lingua di destinazione
        
    Returns:
        Prompt formattato per traduzione
    """
    return f"Traduci il seguente testo in {target_language}:\n\n{text}"


def create_example_texts() -> List[str]:
    """
    Crea una lista di testi di esempio per test.
    
    Returns:
        Lista di testi di esempio
    """
    return [
        "L'intelligenza artificiale sta rivoluzionando il modo in cui interagiamo "
        "con la tecnologia. I modelli di linguaggio naturale sono in grado di "
        "comprendere e generare testo in modo sempre più sofisticato, aprendo "
        "nuove possibilità per l'automazione e l'assistenza.",
        
        "Il machine learning è un ramo dell'intelligenza artificiale che si "
        "concentra sullo sviluppo di algoritmi in grado di apprendere dai dati. "
        "Questi modelli migliorano le loro prestazioni nel tempo senza essere "
        "esplicitamente programmati per ogni compito specifico.",
        
        "La programmazione funzionale è un paradigma che tratta il calcolo come "
        "valutazione di funzioni matematiche. Evita stati mutabili e dati "
        "modificabili, rendendo il codice più prevedibile e più facile da testare.",
    ]


def main():
    """Esempio di utilizzo delle funzioni del modulo."""
    sample_text = (
        "Questo è un testo dimostrativo molto lungo che serve per testare "
        "le capacità di riassunto degli agenti. " * 5
    )
    
    print("=== Esempi di prompt ===")
    print("\n1. Prompt per riassunto:")
    print(make_summary_prompt(sample_text[:200], max_words=50))
    
    print("\n2. Prompt per domanda-risposta:")
    print(make_qa_prompt("Cosa è l'IA?", "L'intelligenza artificiale è..."))
    
    print("\n3. Prompt per traduzione:")
    print(make_translation_prompt("Hello, world!", "italiano"))
    
    print("\n4. Testi di esempio:")
    for i, text in enumerate(create_example_texts(), 1):
        print(f"\nTesto {i}: {text[:100]}...")


if __name__ == "__main__":
    main()