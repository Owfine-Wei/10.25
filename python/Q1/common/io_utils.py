"""配置与路径；所有路径以项目根目录为基准。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q1_DIR = ROOT / "python/Q1"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
