import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

if __package__ in (None, "") and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from shiftlens.cli import run_toy_state_shift_demo


if __name__ == "__main__":
    run_toy_state_shift_demo(Path("reports/demo"), seed=7, window=12, min_support_ratio=0.15)
