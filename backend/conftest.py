"""Pone `backend/` en sys.path para que los tests importen taxonomy/schemas/profile/agents."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
