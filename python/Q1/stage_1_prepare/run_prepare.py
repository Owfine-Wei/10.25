"""阶段1：数据预处理与现状分析，输出基准表。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))

from io_utils import (get_project_root, load_config, load_soybean_rows,
                      save_dataframe, save_json)
from data_prep import build_import_frame, get_base_params


def main():
    root = get_project_root()
    cfg = load_config(root / "python" / "Q1" / "config.json")
    rows = load_soybean_rows(root / cfg["paths"]["data_csv"])
    frame = build_import_frame(rows, cfg.get("exclude_years", []))

    save_dataframe(frame, root / cfg["paths"]["result_dir"] / "historical_shares.csv")

    base = get_base_params(frame, cfg["base_year"])
    base["base_year"] = cfg["base_year"]
    save_json(base, root / cfg["paths"]["result_dir"] / "base_params.json")

    print("[阶段1] 历史份额已保存。基准年 %d：" % cfg["base_year"])
    print("  基准价格(USD/t):", {k: round(v, 1) for k, v in base["base_price"].items()})
    print("  基准份额:", {k: round(v, 3) for k, v in base["base_share"].items()})
    print("  中国总进口需求(百万吨):", round(base["total_demand_ton"] / 1e6, 2))


if __name__ == "__main__":
    main()
