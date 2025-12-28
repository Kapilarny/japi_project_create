from abc import ABC, abstractmethod
import os

class BuildStep(ABC):
    @abstractmethod
    def execute(self) -> bool:
        """Execute the build step."""
        pass

    @abstractmethod
    def get_step_name(self) -> str:
        """Return the name of the build step."""
        pass

    @abstractmethod
    def print_info(self) -> None:
        """Print information about the build step."""
        pass

class WriteTemplateFilesStep(BuildStep):
    def __init__(self, template_files: list, project_dir: str):
        self.template_files = template_files
        self.project_dir = project_dir

    def execute(self) -> bool:
        for tf in self.template_files:
            file_path = os.path.join(self.project_dir, tf.full_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(tf.content)

        return True
    
    def print_info(self) -> None:
        for tf in self.template_files:
            print(f"Writing file: {os.path.join(self.project_dir, tf.full_path)}")

    def get_step_name(self) -> str:
        return "WriteTemplateFilesStep"

class WriteFileStep(BuildStep):
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content

    def execute(self) -> bool:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(self.content)

        return True
    
    def print_info(self) -> None:
        print(f"Writing file: {self.file_path}")

    def get_step_name(self) -> str:
        return "WriteFileStep"

class CreateDirectoryStep(BuildStep):
    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    def execute(self) -> bool:
        import os
        os.makedirs(self.directory_path, exist_ok=True)

        return True
    
    def print_info(self) -> None:
        print(f"Creating directory: {self.directory_path}")

    def get_step_name(self) -> str:
        return "CreateDirectoryStep"

class DownloadFileStep(BuildStep):
    def __init__(self, url: str, destination: str):
        self.url = url
        self.destination = destination

    def execute(self) -> bool:
        import requests
        response = requests.get(self.url)

        if response.status_code != 200:
            print(f"Failed to download file from {self.url}: {response.status_code}")
            return False

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.destination), exist_ok=True)

        with open(self.destination, "wb") as f:
            f.write(response.content)

        return True
    
    def print_info(self) -> None:
        print(f"Downloading file from {self.url} to {self.destination}")

    def get_step_name(self) -> str:
        return "DownloadFileStep"
    
class ExtractZipStep(BuildStep):
    def __init__(self, zip_path: str, extract_to: str):
        self.zip_path = zip_path
        self.extract_to = extract_to

    def execute(self) -> bool:
        import zipfile
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_to)

        return True

    def print_info(self) -> None:
        print(f"Extracting zip file {self.zip_path} to {self.extract_to}")

    def get_step_name(self) -> str:
        return "ExtractZipStep"
    
class DeleteFileStep(BuildStep):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def execute(self) -> bool:
        import os
        os.remove(self.file_path)

        return True

    def get_step_name(self) -> str:
        return "DeleteFileStep"
    
    def print_info(self) -> None:
        print(f"Deleting file: {self.file_path}")