from langchain.tools.base import tool

@tool
def calculator(expression: str) -> str:
    """Perform mathematical calculations based on the given expression."""
    try:
        # Evaluate the expression safely
        return str(eval(expression))
    except:
        return "Invaid Expression"
    
@tool
def word_counter(text: str) -> str:
    """Count the number of words in the given text."""
    return f"Total number of words: {len(text.split())}"