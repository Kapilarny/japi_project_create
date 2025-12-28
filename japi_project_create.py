import argparse
import os
import sys
import requests
import zipfile

from templates.impl.cpp_template import CppTemplate

templates = [
    CppTemplate(),
]

parser = argparse.ArgumentParser(description="Create a new JAPI project.")
parser.add_argument("guid", type=str, help="Name of the JAPI plugin to create.")
parser.add_argument("author", type=str, help="Author(s) of the project.")
parser.add_argument("--description", type=str, default="A JAPI plugin.", help="Description of the project.")
parser.add_argument("--language", type=str, choices=[templ.get_template_name() for templ in templates], default=templates[0].get_template_name(), help="Programming language to use.")

parser.exit_on_error = True

args = parser.parse_args()

# Find the selected template
selected_template = None
for templ in templates:
    if templ.get_template_name() == args.language:
        selected_template = templ
        break

if selected_template is None:
    print(f"Template '{args.language}' not found.")
    sys.exit(1)

print(f"Creating JAPI project: {args.guid} (Language: {args.language})")

# Create project directory
project_dir = args.guid
os.makedirs(project_dir, exist_ok=True)
print(f"Project directory '{project_dir}' created.")

# Render template files
ctx = {
    "guid": args.guid,
    "author": args.author,
    "description": args.description,
}

template_files = selected_template.render_template_files(ctx)
for tf in template_files:
    file_path = os.path.join(project_dir, tf.full_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(tf.content)
    print(f"Created file: {tf.full_path}")

# Download includes.zip and extract it
includes_url = "https://github.com/Kapilarny/JAPI/releases/latest/download/includes.zip"
includes_zip_path = os.path.join(project_dir, "includes.zip")

response = requests.get(includes_url)
if response.status_code != 200:
    print(f"Failed to download includes.zip: {response.status_code}")
    exit(1)

with open(includes_zip_path, "wb") as f:
    f.write(response.content)
    print("Downloaded includes.zip")

# Extract includes.zip
with zipfile.ZipFile(includes_zip_path, 'r') as zip_ref:
    zip_ref.extractall(os.path.join(project_dir, "includes"))
    print("Extracted includes.zip")

os.remove(includes_zip_path)
print("Removed includes.zip")

# Download JAPI.dll
japi_dll_url = "https://github.com/Kapilarny/JAPI/releases/latest/download/JAPI.dll"
japi_dll_path = os.path.join(project_dir, "bins", "JAPI.dll")
os.makedirs(os.path.dirname(japi_dll_path), exist_ok=True)

response = requests.get(japi_dll_url)
if response.status_code != 200:
    print(f"Failed to download JAPI.dll: {response.status_code}")
    exit(1)

with open(japi_dll_path, "wb") as f:
    f.write(response.content)
    print("Downloaded JAPI.dll")