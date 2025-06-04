# makefiles-cli - Command line interface for XDG_TEMPLATES_DIR

`makefiles-cli` is a simple commandline tool to create files and templates. It can create one or more empty files or any template defined in `XDG_TEMPLATES_DIR`. It also has support for [fzf](https://github.com/junegunn/fzf) to make it easier to find template.

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

Run `mkfile --help` for all the available options.

## Installation

_Requirements_:

- python3 (python3.10 or greater)
- pip

You can install `makefiles-cli` directly from **PyPI** using `pip`:

```bash
pip install makefiles-cli
```

Or if you love to stay on bleeding edge, install directly from github:

```bash
pip install git+https://github.com/Rid1FZ/makefiles-cli
```
