from crewai.tools import BaseTool
import os
from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field

class FileWriterInput(BaseModel):
    """Input schema for file writing."""
    filename: str = Field(..., description="Filename (e.g., 'report.md')")
    content: str = Field(..., description="Content to write to the file")

class MCPFilesystemTool(BaseTool):
    name: str = "File Writer"
    description: str = "Write content to a markdown file in the reports directory. Useful for saving final reports."
    args_schema: Type[BaseModel] = FileWriterInput
    
    def _run(self, filename: str, content: str) -> str:
        """Write content to file."""
        try:
            reports_dir = os.getenv('REPORTS_DIR', './reports')
            
            # Create directory if it doesn't exist
            os.makedirs(reports_dir, exist_ok=True)
            
            # Add timestamp if it doesn't have one
            if not any(char.isdigit() for char in filename):
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
            
            filepath = os.path.join(reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"File saved successfully at: {filepath}"
            
        except Exception as e:
            return f"Error saving file: {str(e)}"