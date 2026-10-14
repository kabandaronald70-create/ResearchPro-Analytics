"""
Pytest configuration for ResearchPro Analytics tests.

Adds the project's src/ directory to sys.path so tests can
import modules directly without installing the package.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
