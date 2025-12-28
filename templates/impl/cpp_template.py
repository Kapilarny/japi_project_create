# from itemplate import ITemplate, TemplateFile, resource_path
import os

from templates.itemplate import ITemplate, TemplateFile, resource_path, reformat_string

class CppTemplate(ITemplate):
    def render_template_files(self, ctx: dict) -> list[TemplateFile]:
        base = resource_path("resources/cpp")

        result = []

        for root, _, files in os.walk(base):
            for file in files:
                rel = os.path.relpath(os.path.join(root, file), base)
                print(rel)

                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    tf = TemplateFile(filename=file, path=os.path.dirname(rel))
                    tf.content = reformat_string(content, ctx)
                    result.append(tf)
                    
        return result
    
    def get_template_name(self) -> str:
        return "cpp"
