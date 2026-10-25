"""2025年4月专用比较与验证；保留通用演示代码和结果。"""
import logging
import subprocess
import sys

sys.dont_write_bytecode = True

from common.io_utils import ROOT, Q1_DIR, read_json, write_json
from stage_2.april_analysis import main_comparison, robustness, check_april
from stage_3.april_report import plot_diagnostics, write_april_report

CONFIG_PATH = Q1_DIR / "config.json"


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = read_json(CONFIG_PATH)
    style = read_json(Q1_DIR / "config_pic.json")
    output = ROOT / config["output_dir"]
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "script/prepare_q1.py")], check=True)
    logging.info("计算4月政策配对反事实：两种旧税条件，三组参数，四种政策状态")
    results = main_comparison(ROOT, config)
    sensitive = robustness(ROOT, config)
    checks = check_april(results, sensitive, config)
    results.to_csv(output / "april_scenario_results.csv", index=False, encoding="utf-8-sig")
    sensitive.to_csv(output / "april_robustness.csv", index=False, encoding="utf-8-sig")
    write_json(output / "april_diagnostics.json", {"checks": checks, "config": config,
               "figure_config": style, "main_max_residual": float(results.max_relative_residual.max()),
               "robustness_max_residual": float(sensitive.max_relative_residual.max())})
    plot_diagnostics(results, config, style, output)
    write_april_report(results, sensitive, config, checks, output)
    logging.info("完成，%s项检查通过；写入2个CSV、1个JSON、1张图及1份结果补充", len(checks))
    focus = results.loc[results.regime.eq("legacy_excluded") & results.scenario.eq("april12_125")]
    print(focus[["profile", "country", "april_quantity_change_pct", "april_price_change_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
