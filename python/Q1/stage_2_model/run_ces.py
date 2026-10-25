"""阶段2：Armington CES 情景模拟与敏感性分析。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))

import pandas as pd
from io_utils import (get_project_root, load_config, load_soybean_rows,
                      save_dataframe, save_json)
from data_prep import build_import_frame, get_base_params
from ces_core import calibrate_alpha, compute_qty_value, compute_shares


def run_scenario(cfg, base, name, tariff, sigma):
    """对单个情景+单个 sigma 计算三国份额、出口量、出口额。"""
    alpha = calibrate_alpha(base["base_share"], base["base_price"],
                            cfg["base_tariff"], sigma, base["countries"])
    shares = compute_shares(alpha, base["base_price"], tariff, sigma, base["countries"])
    growth = cfg["import_demand"].get("growth_factor", 1.0)
    demand = base["total_demand_ton"] * growth
    qty, value = compute_qty_value(shares, demand, base["base_price"], tariff, base["countries"])
    row = {"scenario": name, "sigma": sigma}
    for c in base["countries"]:
        row[f"share_{c}"] = shares[c]
        row[f"qty_Mt_{c}"] = qty[c] / 1e6
        row[f"value_bil_{c}"] = value[c] / 1e9
    return row


def main():
    root = get_project_root()
    cfg = load_config(root / "python" / "Q1" / "config.json")
    rows = load_soybean_rows(root / cfg["paths"]["data_csv"])
    frame = build_import_frame(rows, cfg.get("exclude_years", []))
    base = get_base_params(frame, cfg["base_year"])
    sigma = cfg["sigma"]

    results = []
    for name, tariff in cfg["scenarios"].items():
        results.append(run_scenario(cfg, base, name, tariff, sigma))
    df = pd.DataFrame(results)
    save_dataframe(df, root / cfg["paths"]["result_dir"] / "ces_scenario_results.csv")

    mid = (list(cfg["scenarios"].keys())[1]
           if len(cfg["scenarios"]) > 1 else list(cfg["scenarios"].keys())[0])
    sens = [run_scenario(cfg, base, f"{mid}|sigma={s}", cfg["scenarios"][mid], s)
            for s in cfg["sensitivity_sigma"]]
    sdf = pd.DataFrame(sens)
    save_dataframe(sdf, root / cfg["paths"]["result_dir"] / "ces_sensitivity.csv")
    save_json({"mid_scenario": mid},
              root / cfg["paths"]["result_dir"] / "sensitivity_meta.json")

    print("[阶段2] 情景结果：")
    print(df.to_string(index=False))
    cols = ["scenario", "sigma"] + [f"share_{c}" for c in base["countries"]]
    print("[阶段2] 敏感性(中间情景, 变动sigma)：")
    print(sdf[cols].to_string(index=False))


if __name__ == "__main__":
    main()
