import subprocess
import requests
import re
import ast
import json
import sys
import glob

PIP_SEARCH = re.compile(r"\<div\sclass\=\"[^\"]*\"\>pypi\.org\s[^\s]*\sproject\s[^\s]*\s([^\<]*)\<\/div\>")

def have_dependency(dependency: str) -> bool:
    try:
        exec(f"import {dependency}")

    except ImportError:
        return False

    return True

def install_dependency(dependency: str) -> None:
    url = f"https://www.google.com/search?q={dependency}+pypi"
    try:
        cmd = PIP_SEARCH.findall(requests.get(url).content.decode(errors="ignore"))[0]
    
    except IndexError:
        print(f"failed to install dependency: {dependency}")
        return

    pip_command = subprocess.Popen(["pip3", "install", cmd], stdout=subprocess.PIPE)
    pip_command.wait()
    print(f"Successfully installed dependency {dependency}")

def install_dependencies_from_files(files: list[str]):
    dependencies = []
    for file in files:
        with open(file, "r") as fh:
            code = fh.read()

        ast_representation = ast.parse(code)
        for block in ast_representation.body:
            if isinstance(block, ast.Import):
                for import_ in block.names:
                    dependencies.append(import_.name)
            
            if isinstance(block, ast.ImportFrom):
                dependencies.append(block.module)
        
    dependencies = list(set(dependencies))
    for dependency in dependencies:
        if not have_dependency(dependency):
            install_dependency(dependency)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("PLEASE SPECIFY THE CONFIG FILE: python3 auto_pip_install.py {CONFIG JSON FILE}")
        exit(1)

    with open(sys.argv[1], "r") as fh:
        data = json.load(fh)

    files = []
    for file in data: files += glob.glob(file)

    install_dependencies_from_files(files)