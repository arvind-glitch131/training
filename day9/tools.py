import os
from langchain_core.tools import tool

@tool
def file_writer(content: str, filename: str) -> str:
    """
    Writes the research summary to a physical file on the disk.
    Args:
        content: The text summary to save.
        filename: The name of the file (e.g., 'quantum_report.txt').
    """
    directory = "research_output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return f"Successfully saved to {file_path}"