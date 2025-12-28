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

ctx = {
    "guid": args.guid,
    "author": args.author,
    "description": args.description,
}

build_steps = selected_template.get_build_steps(ctx)
for step in build_steps:
    step.print_info()
    # print(f"Executing build step: {step.get_step_name()}")
    
    if not step.execute():
        print(f"Build step '{step.get_step_name()}' failed.")
        sys.exit(1)