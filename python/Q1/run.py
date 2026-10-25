"""一键执行：预处理 -> 校准 -> 均衡 -> 检查 -> 图表与报告。"""
import json
import logging
import subprocess
import sys

sys.dont_write_bytecode = True

from common.io_utils import Q1_DIR, ROOT, read_json, write_json
from common.validation import verify
from stage_1.calibration import calibrate
from stage_2.scenarios import run_scenarios, run_sensitivity, run_tariff_curve
from stage_3.plots import make_plots
from stage_3.report import write_report

CONFIG_PATH = Q1_DIR / "config.json"
STYLE_PATH = Q1_DIR / "config_pic.json"


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config, style = read_json(CONFIG_PATH), read_json(STYLE_PATH)
    output = ROOT / config["output_dir"]
    output.mkdir(parents=True, exist_ok=True)
    logging.info("阶段 0：清洗中国市场数据")
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "script/prepare_q1.py")], check=True)
    logging.info("阶段 1：校准 %s 年基准", config["base_year"])
    history, base = calibrate(ROOT / config["clean_csv"], config)
    logging.info("阶段 2：主情景、27 组弹性组合和税率曲线")
    results, diagnostics = run_scenarios(base, config)
    sensitivity = run_sensitivity(base, config)
    curve = run_tariff_curve(base, config)
    checks = verify(base, config, results, curve)
    logging.info("%s 项验证全部通过", len(checks))
    base.reset_index().to_csv(output / "baseline.csv", index=False, encoding="utf-8-sig")
    for name, table in [("scenario_results", results), ("sensitivity_results", sensitivity), ("tariff_curve", curve)]:
        table.to_csv(output / (name + ".csv"), index=False, encoding="utf-8-sig")
    write_json(output / "diagnostics.json", {"scenarios": diagnostics, "checks": checks,
                                             "sensitivity_max_residual": float(sensitivity.max_relative_residual.max()),
                                             "curve_max_residual": float(curve.max_relative_residual.max())})
    write_json(output / "config_used.json", {"model_config": config, "figure_config": style})
    logging.info("阶段 3：生成三张组合图和中文结果文档")
    make_plots(history, results, curve, sensitivity, config, style, output)
    write_report(base, results, diagnostics, sensitivity, json.dumps(checks, indent=2), config, output)
    logging.info("完成，结果目录：%s", output)
    print(results[["scenario", "country", "quantity_change_pct", "value_change_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
