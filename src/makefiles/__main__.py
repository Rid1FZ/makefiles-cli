"""
Entry point for running the package as a script via `python3 -m makefiles`.
"""

import sys

from makefiles.mkfile import main

if __name__ == "__main__":
    sys.exit(main())
