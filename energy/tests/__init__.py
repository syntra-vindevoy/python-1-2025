import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent

# `energy` package + the top-level `database` package both need to be importable.
for path in (_PROJECT_ROOT / "src", _PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
