"""只输出三张组合图；颜色、字体等统一读取 config_pic.json。"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def setup_style(style):
    plt.rcParams.update({"font.sans-serif": style["fonts"], "axes.unicode_minus": False,
                         "font.size": style["font_size"], "savefig.dpi": style["dpi"],
                         "axes.spines.top": False, "axes.spines.right": False})


def finish(fig, axes, path, style):
    for ax in axes:
        ax.grid(axis="y", alpha=style["grid_alpha"])
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_history(history, config, style, output):
    fig, axes = plt.subplots(1, 2, figsize=style["figure_size"])
    for country in config["countries"]:
        data = history.loc[history.country.eq(country)].sort_values("year")
        options = {"color": style["country_colors"][country],
                   "label": config["country_names"][country], "marker": "o", "markersize": 4}
        axes[0].plot(data.year, data.quantity_tonnes / 1e6, **options)
        axes[1].plot(data.year, data.quantity_share * 100, **options)
    axes[0].set(title="三国对华大豆出口量：历史数据", ylabel="百万吨", xlabel="年份")
    axes[1].set(title="三国合计内的数量份额", ylabel="%", xlabel="年份")
    axes[0].legend(loc="upper left")
    finish(fig, axes, output / "fig01_history.png", style)


def plot_scenarios(results, config, style, output):
    fig, axes = plt.subplots(1, 2, figsize=style["figure_size"])
    ids = [s["id"] for s in config["scenarios"]]
    labels = [s["label"].replace("美国", "美豆\n") for s in config["scenarios"]]
    x = np.arange(len(ids))
    for position, country in enumerate(config["countries"]):
        data = results.loc[results.country.eq(country)].set_index("scenario").loc[ids]
        options = {"width": 0.24, "color": style["country_colors"][country],
                   "label": config["country_names"][country]}
        axes[0].bar(x + (position - 1) * 0.25, data.quantity_tonnes / 1e6, **options)
        axes[1].bar(x + (position - 1) * 0.25, data.value_usd / 1e9, **options)
    axes[0].set(title="对华出口量：假设关税情景", ylabel="百万吨")
    axes[1].set(title="对华 FOB 出口额：假设关税情景", ylabel="十亿美元")
    for ax in axes:
        ax.set_xticks(x, labels)
    axes[0].legend(loc="upper left")
    finish(fig, axes, output / "fig02_scenarios.png", style)


def plot_response(curve, sensitivity, config, style, output):
    fig, axes = plt.subplots(1, 2, figsize=style["figure_size"])
    for position, country in enumerate(config["countries"]):
        options = {"color": style["country_colors"][country], "label": config["country_names"][country]}
        data = curve.loc[curve.country.eq(country)]
        axes[0].plot(data.tariff_addition_pp, data.quantity_change_pct, **options)
        values = sensitivity.loc[sensitivity.country.eq(country), "quantity_change_pct"]
        axes[1].plot([position, position], [values.min(), values.max()], linewidth=5, **options)
        axes[1].scatter([position, position], [values.min(), values.max()], color=options["color"], s=35)
    axes[0].set(title="加税幅度与对华出口量变化", xlabel="中国对美豆新增关税（百分点）", ylabel="相对基期变化（%）")
    axes[1].set(title="重点情景：27 组弹性组合的结果范围", ylabel="出口量相对基期变化（%）")
    axes[1].set_xticks(range(3), [config["country_names"][c] for c in config["countries"]])
    axes[0].legend()
    for ax in axes:
        ax.axhline(0, color="#777777", linewidth=0.8)
    finish(fig, axes, output / "fig03_response_sensitivity.png", style)


def make_plots(history, results, curve, sensitivity, config, style, output):
    setup_style(style)
    plot_history(history, config, style, output)
    plot_scenarios(results, config, style, output)
    plot_response(curve, sensitivity, config, style, output)
