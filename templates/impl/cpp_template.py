# from itemplate import ITemplate, TemplateFile, resource_path
import os

from templates.build import *
from templates.itemplate import ITemplate, TemplateFile, resource_path, reformat_string

class CppTemplate(ITemplate):
    def get_build_steps(self, ctx: dict[str, str]) -> list[BuildStep]:
        result = []

        # Download, extract includes.zip, and then delete the zip file
        result.append(DownloadFileStep(
            url="https://github.com/Kapilarny/JAPI/releases/latest/download/includes.zip",
            destination=os.path.join(ctx["guid"], "includes.zip")
        ))

        result.append(ExtractZipStep(
            zip_path=os.path.join(ctx["guid"], "includes.zip"),
            extract_to=os.path.join(ctx["guid"], "includes")
        ))

        result.append(DeleteFileStep(
            file_path=os.path.join(ctx["guid"], "includes.zip")
        ))

        # Download JAPI.dll
        result.append(DownloadFileStep(
            url="https://github.com/Kapilarny/JAPI/releases/latest/download/JAPI.dll",
            destination=os.path.join(ctx["guid"], "bins", "JAPI.dll")
        ))

        # Write template files
        result.append(WriteTemplateFilesStep(
            template_files=self.render_template_files(ctx),
            project_dir=ctx["guid"]
        ))    

        return result
    
    def get_template_name(self) -> str:
        return "cpp"
