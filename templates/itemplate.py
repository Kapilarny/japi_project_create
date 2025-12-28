from abc import ABC, abstractmethod
import sys
import os
import re

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path) # type: ignore[attr-defined]
    return os.path.join(os.path.abspath("."), relative_path)

def reformat_string(s: str, values: dict[str, str]) -> str:
    pattern = re.compile(r"%%\{([^}]+)\}%%")
    
    def replacer(match):
        key = match.group(1)
        return str(values.get(key, match.group(0)))
    
    return pattern.sub(replacer, s)

class TemplateFile:
    def __init__(self, filename: str, path: str = ""):
        self.filename = filename
        self.content = ""
        self.path = path
        self.full_path = f"{path}/{filename}" if path else filename

class ITemplate(ABC):
    @abstractmethod
    def render_template_files(self, ctx: dict) -> list[TemplateFile]:
        """Render the template files with the given context."""
        pass

    @abstractmethod
    def get_template_name(self) -> str:
        """Return the name of the template."""
        pass