from abc import ABC, abstractmethod
import sys
import os
import re

from templates.build import BuildStep

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
    def get_build_steps(self, ctx: dict) -> list[BuildStep]:
        """Return the list of build steps for this template."""
        pass

    def render_template_files(self, ctx: dict) -> list[TemplateFile]:
        base = resource_path(f"resources/{self.get_template_name()}")

        result = []

        for root, _, files in os.walk(base):
            for file in files:
                rel = os.path.relpath(os.path.join(root, file), base)

                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    tf = TemplateFile(filename=file, path=os.path.dirname(rel))
                    tf.content = reformat_string(content, ctx)
                    result.append(tf)
                    
        return result

    @abstractmethod
    def get_template_name(self) -> str:
        """Return the name of the template."""
        pass