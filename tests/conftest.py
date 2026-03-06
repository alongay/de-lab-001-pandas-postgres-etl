from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root (/app) is on sys.path when pytest runs from /app/tests
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
