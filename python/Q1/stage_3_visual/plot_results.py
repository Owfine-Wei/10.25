"""阶段3：结果可视化（论文级风格，参考 modelviz-skill 模板美学）。

风格约定（来自模板库）：Times New Roman / 衬线字体、dpi=300、
去顶/右边框、浅色虚线网格、统一底部图例、数值标注。
"""
from __future__ import annotations

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from io_utils import get_project_root, load_config, load_soybean_rows
from data_prep import build_import_frame

# ---- 全局论文风样式 ----
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
mpl.rcParams["mathtext.fontset"] = "stix"
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["axes.unicode_minus"] = False

COUNTRIES = ["USA", "BRA", "ARG"]
CNAME = {"USA": "United States", "BRA": "Brazil", "ARG": "Argentina"}
COLOR = {"USA": "#377eb8", "BRA": "#4daf4a", "ARG": "#ff7f0e"}


def _style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25, ls="--")
    ax.set_axisbelow(True)


def plot_historical(frame, out):
    df = frame.copy()
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=300)
    for c in COUNTRIES:
        sub = df[df.country == c].sort_values("year")
        ax.plot(sub.year, sub.share * 100, marker="o", ms=6, lw=2,
                color=COLOR[c], label=CNAME[c])
        for _, r in sub.iterrows():
            ax.annotate(f"{r.share*100:.0f}", (r.year, r.share * 100),
                        textcoords="offset points", xytext=(0, 7),
                        ha="center", fontsize=8, color=COLOR[c])
    ax.axvline(2018, color="#999999", ls=":", lw=1.2)
    ax.annotate("2018 US-China\ntrade war", (2018, 70), textcoords="offset points",
                xytext=(6, 0), fontsize=9, color="#666666", va="center")
    ax.axvspan(2017.5, 2018.5, color="#f0f0f0", zorder=0)
    _style(ax)
    ax.set_xticks(sorted(df["year"].unique().tolist()))
    ax.set_xlabel("Year")
    ax.set_ylabel("Import share (%)")
    ax.set_title("China's Soybean Import Share by Origin, 2015–2024", fontsize=13)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    ax.set_ylim(0, 80)
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _baseline(base_params):
    bp = base_params
    tot = bp["total_demand_ton"]
    base = {}
    for c in COUNTRIES:
        q_ton = bp["base_share"][c] * tot
        base[c] = {"share": bp["base_share"][c] * 100,
                   "qty_Mt": q_ton / 1e6,
                   "value_bil": q_ton * bp["base_price"][c] / 1e9}
    return base


def plot_scenario_bar(res, base, label_map, out, kind="share"):
    col, ylab, title = {
        "share": ("share", "Import share (%)", "Post-Tariff Import Share by Scenario"),
        "qty": ("qty_Mt", "Export volume (Mt)", "Post-Tariff Export Volume by Scenario"),
        "value": ("value_bil", "Export value (B USD)", "Post-Tariff Export Value by Scenario"),
    }[kind]
    rows = [{"label": "Baseline\n(0%)", **{f"{col}_{c}": base[c][col] for c in COUNTRIES}}]
    for _, r in res.iterrows():
        rows.append({"label": label_map[r["scenario"]],
                     **{f"{col}_{c}": r[f"{col}_{c}"] * (100 if kind == "share" else 1)
                        for c in COUNTRIES}})
    d = pd.DataFrame(rows)
    scen = d["label"].tolist()
    x = np.arange(len(scen))
    w = 0.25
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=300)
    for i, c in enumerate(COUNTRIES):
        vals = d[f"{col}_{c}"].tolist()
        bars = ax.bar(x + (i - 1) * w, vals, w, label=CNAME[c], color=COLOR[c],
                      edgecolor="white", linewidth=0.6)
        for b, v in zip(bars, vals):
            ax.annotate(f"{v:.1f}", (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
    _style(ax)
    ax.set_xticks(x)
    ax.set_xticklabels(scen)
    ax.set_ylabel(ylab)
    ax.set_title(title, fontsize=13)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_sensitivity(sens, out):
    sens = sens[sens["scenario"].astype(str).str.startswith("S2_mid")].copy()
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=300)
    for c in COUNTRIES:
        ax.plot(sens.sigma, sens[f"share_{c}"] * 100, marker="o", ms=5, lw=2,
                color=COLOR[c], label=CNAME[c])
    for sx in (4.0, 4.9):
        ax.axvline(sx, color="#999999", ls="--", lw=1)
    ax.annotate("main σ=4.0", (4.0, 78), fontsize=8, color="#666666", ha="center")
    ax.annotate("GTAP σ=4.9", (4.9, 70), fontsize=8, color="#666666", ha="center")
    ax.axvspan(2.0, 4.9, color="#f5f5f5", zorder=0)
    _style(ax)
    ax.set_xlabel("Substitution elasticity σ")
    ax.set_ylabel("Import share (%)")
    ax.set_title("Sensitivity of Import Share to σ (mid scenario, +20%)", fontsize=13)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    ax.set_ylim(0, 85)
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_donut(res, base, label_map, out):
    groups = [("Baseline (0%)", {c: base[c]["share"] / 100 for c in COUNTRIES})]
    for _, r in res.iterrows():
        groups.append((label_map[r["scenario"]], {c: r[f"share_{c}"] for c in COUNTRIES}))
    labels = [CNAME[c] for c in COUNTRIES]
    colors = [COLOR[c] for c in COUNTRIES]
    n = len(groups)
    ncols = 2
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(9, 4.5 * nrows), dpi=300)
    axes = axes.flatten()
    for i, (title, sh) in enumerate(groups):
        ax = axes[i]
        sizes = [sh[c] * 100 for c in COUNTRIES]
        wedges, _, autotexts = ax.pie(
            sizes, colors=colors, startangle=90, autopct="%1.1f%%",
            pctdistance=0.74, wedgeprops={"edgecolor": "white", "linewidth": 1.2})
        ax.add_artist(plt.Circle((0, 0), 0.5, fc="white"))
        for at in autotexts:
            at.set_color("black"); at.set_fontsize(9); at.set_fontweight("bold")
        ax.text(0, 0, title, ha="center", va="center", fontsize=11, fontweight="bold")
    for j in range(n, len(axes)):
        axes[j].axis("off")
    fig.legend(wedges, labels, loc="lower center", bbox_to_anchor=(0.5, 0.0),
               ncol=3, frameon=False, fontsize=11)
    fig.suptitle("Composition Shift Under US Tariff Scenarios", fontsize=14, y=0.96)
    fig.tight_layout(rect=[0, 0.06, 1, 0.95])
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    root = get_project_root()
    cfg = load_config(root / "python" / "Q1" / "config.json")
    rdir = root / cfg["paths"]["result_dir"]

    with open(rdir / "base_params.json", encoding="utf-8") as f:
        base_params = json.load(f)
    base = _baseline(base_params)

    label_map = {name: f"+{int(round(v['USA'] * 100))}%"
                 for name, v in cfg["scenarios"].items()}

    rows = load_soybean_rows(root / cfg["paths"]["data_csv"])
    frame = build_import_frame(rows, cfg.get("exclude_years", []))
    plot_historical(frame, rdir / "fig_historical_shares.png")

    res = pd.read_csv(rdir / "ces_scenario_results.csv")
    plot_scenario_bar(res, base, label_map, rdir / "fig_scenario_shares.png", "share")
    plot_scenario_bar(res, base, label_map, rdir / "fig_scenario_qty.png", "qty")
    plot_scenario_bar(res, base, label_map, rdir / "fig_scenario_value.png", "value")
    plot_donut(res, base, label_map, rdir / "fig_scenario_donut.png")

    sens = pd.read_csv(rdir / "ces_sensitivity.csv")
    plot_sensitivity(sens, rdir / "fig_sensitivity_sigma.png")

    print("[阶段3] 论文级图表已保存到", rdir)


if __name__ == "__main__":
    main()
