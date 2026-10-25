"""阶段3：结果可视化（少量关键图，配色统一读 config_pic.json）。"""
from __future__ import annotations

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from io_utils import get_project_root, load_config, load_soybean_rows
from data_prep import build_import_frame


def _load_pic() -> dict:
    try:
        with open(get_project_root() / "python" / "Q1" / "config_pic.json",
                  encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def plot_historical(frame, pic, out):
    cmap = pic.get("palette", {})
    plt.figure(figsize=(7, 4), dpi=pic.get("figure_dpi", 150))
    for c in sorted(frame["country"].unique()):
        sub = frame[frame.country == c].sort_values("year")
        plt.plot(sub.year, sub.share, marker="o", label=c, color=cmap.get(c))
    plt.title("China Soybean Import Share by Origin (2015-2024)")
    plt.xlabel("Year")
    plt.ylabel("Import Share")
    plt.legend()
    plt.grid(alpha=pic.get("grid_alpha", 0.3))
    plt.tight_layout()
    plt.savefig(out)
    plt.close()


def plot_scenario(res, pic, out, countries):
    cmap = pic.get("palette", {})
    scen = res.scenario.tolist()
    x = range(len(scen))
    w = 0.25
    plt.figure(figsize=(8, 4), dpi=pic.get("figure_dpi", 150))
    for i, c in enumerate(countries):
        vals = res[f"share_{c}"].tolist()
        plt.bar([p + (i - 1) * w for p in x], vals, w, label=c, color=cmap.get(c))
    plt.xticks(list(x), scen)
    plt.ylabel("Import Share")
    plt.title("Post-Tariff Share by Scenario")
    plt.legend()
    plt.grid(alpha=pic.get("grid_alpha", 0.3))
    plt.tight_layout()
    plt.savefig(out)
    plt.close()


def plot_sensitivity(sens, pic, out, countries):
    cmap = pic.get("palette", {})
    sig = sens.sigma.tolist()
    plt.figure(figsize=(7, 4), dpi=pic.get("figure_dpi", 150))
    for c in countries:
        plt.plot(sig, sens[f"share_{c}"].tolist(), marker="o", label=c, color=cmap.get(c))
    plt.xlabel("Substitution Elasticity sigma")
    plt.ylabel("Import Share")
    plt.title("Sensitivity: Mid Scenario")
    plt.legend()
    plt.grid(alpha=pic.get("grid_alpha", 0.3))
    plt.tight_layout()
    plt.savefig(out)
    plt.close()


def plot_qty_value(res, pic, out, countries, kind="qty"):
    cmap = pic.get("palette", {})
    col = "qty_Mt" if kind == "qty" else "value_bil"
    ylab = "Export Volume (Mt)" if kind == "qty" else "Export Value (B USD)"
    title = ("Post-Tariff Export Volume by Scenario" if kind == "qty"
             else "Post-Tariff Export Value by Scenario")
    scen = res.scenario.tolist()
    x = range(len(scen))
    w = 0.25
    plt.figure(figsize=(8, 4), dpi=pic.get("figure_dpi", 150))
    for i, c in enumerate(countries):
        plt.bar([p + (i - 1) * w for p in x], res[f"{col}_{c}"].tolist(),
                w, label=c, color=cmap.get(c))
    plt.xticks(list(x), scen)
    plt.ylabel(ylab)
    plt.title(title)
    plt.legend()
    plt.grid(alpha=pic.get("grid_alpha", 0.3))
    plt.tight_layout()
    plt.savefig(out)
    plt.close()


def main():
    root = get_project_root()
    cfg = load_config(root / "python" / "Q1" / "config.json")
    pic = _load_pic()
    rdir = root / cfg["paths"]["result_dir"]

    rows = load_soybean_rows(root / cfg["paths"]["data_csv"])
    frame = build_import_frame(rows, cfg.get("exclude_years", []))
    plot_historical(frame, pic, rdir / "fig_historical_shares.png")

    res = pd.read_csv(rdir / "ces_scenario_results.csv")
    plot_scenario(res, pic, rdir / "fig_scenario_shares.png", cfg["countries"])
    plot_qty_value(res, pic, rdir / "fig_scenario_qty.png", cfg["countries"], "qty")
    plot_qty_value(res, pic, rdir / "fig_scenario_value.png", cfg["countries"], "value")

    sens = pd.read_csv(rdir / "ces_sensitivity.csv")
    plot_sensitivity(sens, pic, rdir / "fig_sensitivity_sigma.png", cfg["countries"])

    print("[阶段3] 图表已保存到", rdir)


if __name__ == "__main__":
    main()
