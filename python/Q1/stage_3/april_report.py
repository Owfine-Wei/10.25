"""把价格反应诊断转成一张图与可直接阅读的解释。"""
import matplotlib.pyplot as plt
import numpy as np

from stage_3.plots import finish, setup_style
from stage_3.report import markdown_table


def focused_rows(table, config):
    policy = config["april_2025"]
    return table.loc[table.regime.eq(policy["reference_regime"]) & table.scenario.eq(policy["focus_stage"])]


def plot_diagnostics(main, config, style, output):
    setup_style(style)
    focused = focused_rows(main, config)
    profiles = config["april_2025"]["profiles"]
    x = np.arange(len(profiles))
    fig, axes = plt.subplots(1, 2, figsize=style["figure_size"])
    for i, country in enumerate(config["countries"]):
        rows = focused.loc[focused.country.eq(country)].set_index("profile").loc[[p["id"] for p in profiles]]
        for ax, field in zip(axes, ["april_quantity_change_pct", "april_price_change_pct"]):
            ax.bar(x + (i - 1) * 0.25, rows[field], width=0.24,
                   color=style["country_colors"][country], label=config["country_names"][country])
    for ax in axes:
        ax.set_xticks(x, [p["label"] for p in profiles])
        ax.set_ylabel("相对无4月加税情景的变化（%）")
        ax.axhline(0, color="#777777", linewidth=0.8)
    axes[0].set_title("4月12日税率情景：对华出口量")
    axes[1].set_title("同一政策情景：FOB价格反应")
    axes[0].legend(loc="lower left")
    finish(fig, axes, output / "fig04_april_diagnostics.png", style)


def result_section(main, config):
    focused = focused_rows(main, config)
    rows = [[r.profile_label, config["country_names"][r.country],
             "{:+.2f}%".format(r.april_quantity_change_pct), "{:+.2f}%".format(r.april_price_change_pct),
             "{:+.2f}%".format(r.april_value_change_pct)] for r in focused.itertuples()]
    reference = focused.loc[focused.profile.eq(config["april_2025"]["reference_profile"])]
    binding = [config["country_names"][c] for c in reference.loc[reference.capacity_binding, "country"]]
    distribution = [[config["country_names"][r.country], "{:.3f}".format(r.quantity_tonnes / 1e6),
                     "{:.3f}".format(r.value_usd / 1e9), "{:.2f}%".format(r.quantity_share * 100),
                     "{:.2f}%".format(r.value_share * 100)] for r in reference.itertuples()]
    return "\n\n".join([
        "## 2. 第4步：价格反应是否合理——已完成的对照实验",
        "![同一4月政策冲击下的参数诊断](fig04_april_diagnostics.png)",
        markdown_table(["参数组", "国家", "数量变化", "FOB价格变化", "FOB金额变化"], rows),
        "这里都与同组参数下的‘保留3月10个百分点、没有4月新增关税’比较，未把3月影响算成4月影响。",
        "原组与‘仅换供给弹性’组只有供给弹性不同，因此两者差异可以用于定位供给假设的作用。文献参考组还改变了需求与替代弹性，只能作为综合参数比较。",
        "小供给弹性意味着数量稍有收缩就需要很大降价。中国市场单独闭合时，模型可能让美国通过过度降价消化冲击；提高对华供给弹性后，更多调整表现为减少销售数量。",
        "不能只因某组结果更符合直觉，就认定其参数是真实值。本实验验证的是模型机制与参数敏感性，不是2025年外样本预测精度。",
        "### 文献参考组的条件性分布",
        markdown_table(["国家", "年度基期尺度数量（百万吨）", "FOB金额（十亿美元）", "数量份额", "金额份额"], distribution),
        "本组达到假设供给上限的国家：{}。这些国家的数量受人为容量约束影响，不能当作独立估计出的真实出口能力；其价格上涨也可能被偏紧的上限放大。".format("、".join(binding) or "无"),
        "以上绝对量采用2024年年度基期尺度，表示高税率持续、模型调整后的条件性均衡；不是2025年4月当月出口量，也不是2025全年预测。份额只在三国合计内部计算。"])


def robustness_section(sensitivity, config, checks):
    elastic = sensitivity.loc[sensitivity.test.eq("elasticity")]
    rows = []
    for country in config["countries"]:
        subset = elastic.loc[elastic.country.eq(country)]
        rows.append([config["country_names"][country],
                     "{:+.2f}% 至 {:+.2f}%".format(subset.april_quantity_change_pct.min(), subset.april_quantity_change_pct.max()),
                     "{:+.2f}% 至 {:+.2f}%".format(subset.april_price_change_pct.min(), subset.april_price_change_pct.max())])
    cap = sensitivity.loc[sensitivity.test.eq("capacity") & sensitivity.country.eq("USA")]
    caps = [[r.capacity_multiplier_test, "{:+.2f}%".format(r.april_quantity_change_pct),
             "{:+.2f}%".format(r.april_price_change_pct)] for r in cap.itertuples()]
    return "\n\n".join([
        "## 3. 稳健性与校验",
        "27组弹性组合只改变σ、η和供给弹性倍数，其他假设不变：",
        markdown_table(["国家", "4月数量效应范围", "4月FOB价格效应范围"], rows),
        "另将三国容量上限统一设为基期的1.1、1.2、1.5倍，仅为边界实验：",
        markdown_table(["容量倍数", "美国数量变化", "美国价格变化"], caps),
        "区间不是置信区间；容量实验不是农业产能估计，亦未涵盖运输、非关税措施与季节性。",
        "程序检查：{}项全部通过；主情景和敏感性求解都逐次检查供需残差。".format(len(checks)),
        "已完成数值一致性与参数稳健性检查。尚未完成历史事件外样本检验，不能声称预测已验证。",
        "## 4. 第5步：论文组织与后续验证",
        "可以直接使用本目录的《第一问建模与验证写作稿.md》组织方法章节；政策来源见《2025年4月政策与参数依据.md》。",
        "要验证4月实际到港量，需要月度分来源净重、金额、在途合同和季节性信息；全年数据不能除以12替代。",
        "建议用2017年校准、2018年事件作方向性外部检查，同时控制同期需求和收成。不能把两年全部变化当作关税效应，也不能用2024校准结果倒推2018作为验证。",
        "2025年后续观察可用于事后检验，但不能作为4月决策时已知参数。当前结果最好写为政策比较静态分析。"])


def write_april_report(main, sensitivity, config, checks, output):
    sections = ["# 2025年4月关税影响：结果解释补充",
                "**用途：针对4月政策核实与模型合理性诊断。原《解释结果文档.md》为通用假设演示，本补充用于4月研究。**",
                "## 1. 本次分析口径",
                config["april_2025"]["scope"],
                "政策输入、文献参数及其可迁移性见[政策与参数依据](2025年4月政策与参数依据.md)。主展示条件是旧附加税获批排除、且不享受本轮在途例外的主要非种用黄大豆货物。",
                "34%仅为公告方案比较，不能解释为实际生效的一段关税水平。84%与125%分别是后续替换税率，不相加。",
                result_section(main, config), robustness_section(sensitivity, config, checks),
                "## 5. 复现与结果字段",
                "入口为 `python/Q1/run_april.py`；参数全部在 `config.json` 的 `april_2025` 字段。",
                "`april_scenario_results.csv` 包含两种旧税排除条件、三组参数与四个政策情景；`april_robustness.csv` 包含弹性与容量检查。",
                "`april_*_change_pct` 是相对无4月加税对照的效应；原 `*_change_pct` 字段仍是相对2024校准点，二者不得混用。",
                "该程序不覆盖原演示输出；参数快照与检查保存在 `april_diagnostics.json`。"]
    (output / "2025年4月结果解释补充.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
