# makefiles-cli - Command line interface for XDG_TEMPLATES_DIR

makefiles-cli is a simple commandline tool to create files and templates. It can create one or more empty files or any template defined in `XDG_TEMPLATES_DIR`. It also has support for [fzf](https://github.com/junegunn/fzf) to make it easier to find template.

## Usage

Create empty files:

```bash
mkfile example1 example2
```

List all available templates:

```bash
mkfile --list
```

Create template from any template defined in `XDG_TEMPLATES_DIR`:

```bash
mkfile script.py --template="pyscript.py"
```

Create template using `fzf` as picker to pick template interactively:

```bash
mkfile script.py --template --picker="fzf"
```

## Installation

_Requirements_:

- python3 (python3.10 or greater)
- pip

You can install `makefiles-cli` directly from **PyPI** using `pip`:

```bash
pip install makefiles-cli
```
