import os, sys
from pathlib import Path

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = Path(__file__).parent
    return os.path.join(base_path, relative_path)