"""一键运行 Q1 三阶段（顺序执行）。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STAGES = [
    "stage_1_prepare/run_prepare.py",
    "stage_2_model/run_ces.py",
    "stage_3_visual/plot_results.py",
]

for stage in STAGES:
    print(">>> 运行", stage)
    subprocess.run([sys.executable, str(ROOT / stage)], check=True)
