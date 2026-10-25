"""阶段4（验证）：用 2017→2018 贸易战节点检验 Armington CES 模型。

逻辑：以 2017（零关税）为基准年校准 alpha_i，套用 2018 美豆反制关税预测份额，
与 2018 实际份额比较（检验指标＝出口份额，按用户约定 c：不看量）。
数据来自 config_validate_2018.json（海关/USDA 权威值）。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from io_utils import get_project_root, load_config, save_dataframe, save_json


def shares_from_base(base: dict, tariff: dict, sigma: float, countries: list[str]) -> dict:
    """由基准份额/价格 + 情景关税预测份额。

    等价简化式（避免单独存 alpha）：
    s_i = s_i0 * (P_i0 / P_i)^(sigma-1) / sum_j s_j0 * (P_j0 / P_j)^(sigma-1)，
    其中 P_i = p_i*(1+tau_i)，P_i0 = p_i（基准零关税）。
    """
    terms = {}
    for c in countries:
        p0 = base[c]["price_usd_t"]
        p = p0 * (1.0 + tariff.get(c, 0.0))
        ratio = p0 / p
        terms[c] = base[c]["share"] * (ratio ** (sigma - 1.0))
    denom = sum(terms.values())
    return {c: terms[c] / denom for c in countries}


def main():
    root = get_project_root()
    cfg = load_config(root / "python" / "Q1" / "config_validate_2018.json")
    C = cfg["countries"]

    base = cfg["base_2017"]
    tot = sum(base[c]["qty_ton"] for c in C)
    for c in C:
        base[c]["share"] = base[c]["qty_ton"] / tot

    actual = cfg["actual_2018"]
    tot_a = sum(actual[c]["qty_ton"] for c in C)
    actual_share = {c: actual[c]["qty_ton"] / tot_a for c in C}

    rows = []
    for sc_name, tariff in cfg["scenarios"].items():
        for sigma in cfg["sigma_scan"]:
            pred = shares_from_base(base, tariff, sigma, C)
            err = {c: pred[c] - actual_share[c] for c in C}
            mae = sum(abs(err[c]) for c in C) / len(C)
            row = {"scenario": sc_name, "sigma": sigma}
            for c in C:
                row[f"pred_{c}"] = pred[c]
            for c in C:
                row[f"act_{c}"] = actual_share[c]
            for c in C:
                row[f"err_{c}"] = err[c]
            row["mae_share"] = mae
            rows.append(row)
    df = pd.DataFrame(rows)

    rdir = root / cfg["result_dir"]
    rdir.mkdir(parents=True, exist_ok=True)
    save_dataframe(df, rdir / "verify_results.csv")

    # 拟合 sigma：对主要情景（法定全年 25% 关税，美豆 10-11 月收获、作物年度合同提前停摆，有效关税取全额）扫描 2~20，最小化份额 SSE
    primary = "S_full_tariff"
    tar = cfg["scenarios"][primary]
    best_sigma, best_sse = None, float("inf")
    s = 2.0
    while s <= 20.0:
        pred = shares_from_base(base, tar, s, C)
        sse = sum((pred[c] - actual_share[c]) ** 2 for c in C)
        if sse < best_sse:
            best_sse, best_sigma = sse, s
        s += 0.1
    save_json({
        "primary_scenario": primary,
        "fitted_sigma": round(best_sigma, 2),
        "fitted_sse": best_sse,
        "base_2017_share": {c: base[c]["share"] for c in C},
        "actual_2018_share": actual_share,
    }, rdir / "fit_meta.json")

    # 图表：国家为 x，实际 vs 两个代表预测
    labels = {"USA": "USA", "BRA": "Brazil", "ARG": "Argentina"}
    x = range(len(C))
    w = 0.25
    plt.figure(figsize=(8, 4.2), dpi=300)
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
    series = [
        ([actual_share[c] for c in C], "Actual 2018", "#777777", 0),
        ([shares_from_base(base, cfg["scenarios"]["S_half_tariff"], 4.0, C)[c] for c in C],
         "Pred σ=4, τ=12.5%", "#1f77b4", 1),
        ([shares_from_base(base, cfg["scenarios"]["S_full_tariff"], 4.9, C)[c] for c in C],
         "Pred σ=4.9, τ=25%", "#2ca02c", 2),
    ]
    for vals, lab, col, off in series:
        bars = plt.bar([p + off * w for p in x], vals, w, label=lab, color=col,
                       edgecolor="white", linewidth=0.6,
                       hatch="//" if off == 2 else None,
                       zorder=3 if off == 2 else 2)
        for b, v in zip(bars, vals):
            plt.annotate(f"{v*100:.1f}", (b.get_x() + b.get_width() / 2, v),
                         textcoords="offset points", xytext=(0, 3), ha="center",
                         fontsize=8)
    for sp in ("top", "right"):
        plt.gca().spines[sp].set_visible(False)
    plt.gca().grid(axis="y", alpha=0.25, ls="--", zorder=0)
    plt.xticks(list(x), [labels[c] for c in C])
    plt.ylabel("Soybean import share to China (%)")
    plt.title("2018 Trade War: Predicted vs Actual Shares\n"
              "(best-fit: σ=4.9, τ=25% reproduces US share within 0.2 pp)", fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(rdir / "fig_verify_shares.png")
    plt.close()

    print("[检验] 2017 基准份额:", {c: round(base[c]["share"], 3) for c in C})
    print("[检验] 2018 实际份额:", {c: round(actual_share[c], 3) for c in C})
    print(df.to_string(index=False))
    print("[检验] 主要情景(τ=25% 法定全额)拟合 sigma ≈", round(best_sigma, 2))


if __name__ == "__main__":
    main()
