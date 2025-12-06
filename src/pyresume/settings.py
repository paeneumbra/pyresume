from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Directories
OUTPUT_DIR = PROJECT_ROOT / "output"
ASSETS_DIR = Path(__file__).resolve().parent / "assets"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
