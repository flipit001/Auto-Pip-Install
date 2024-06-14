
# Auto-Pip-Install
Automatically install all needed dependencies from inputted python file(s).

# Install
```bash
> git clone git@github.com:flipit001/Auto-Pip-Install.git
> pip3 install -r requirements.txt
```
# Use
```bash
> python3 auto_pip_install.py {CONFIG JSON FILE}
```
## Example
```bash
> cat example.json
[
    "test.py",
    "test2.py",
    "test3.py",
    "tests/*.py"
]
> python3 auto_pip_install.py example.json
```
```json config file```: An array of strings to the path of files from which you want to install the needed dependencies.
