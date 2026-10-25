"""修复原始 CSV 的尾部空字段，提取三国对华 HS1201 年度数据。"""
import csv
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "python/Q1/config.json"


def read_raw(path):
    """只移除超出表头的空字段；非空多余字段和短行直接报错。"""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        header = next(reader)
        rows, repaired = [], 0
        for number, row in enumerate(reader, start=2):
            if not row:
                continue
            if len(row) > len(header) and all(not x.strip() for x in row[len(header):]):
                row = row[:len(header)]
                repaired += 1
            if len(row) != len(header):
                raise ValueError("CSV 第 {} 行列数异常".format(number))
            rows.append(row)
    return pd.DataFrame(rows, columns=header), repaired


def clean_china(raw, countries):
    """净重统一换算为吨；金额只用 FOB，拒绝静默填补缺失值。"""
    mask = ((raw.cmdCode == "1201") & (raw.partnerISO == "CHN")
            & (raw.flowCode == "X") & (raw.freqCode == "A")
            & raw.reporterISO.isin(countries))
    frame = raw.loc[mask].copy()
    frame["year"] = pd.to_numeric(frame.refYear, errors="raise").astype(int)
    frame["quantity_tonnes"] = pd.to_numeric(frame.netWgt, errors="raise") / 1000
    frame["value_usd"] = pd.to_numeric(frame.fobvalue, errors="raise")
    values = frame[["quantity_tonnes", "value_usd"]].to_numpy()
    if not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError("净重或 FOB 金额缺失、非有限或非正")
    if frame.duplicated(["year", "reporterISO"]).any():
        raise ValueError("国家—年份重复，须先核查统计口径，不能直接求和")
    frame["country"] = frame.reporterISO
    frame["fob_usd_per_tonne"] = frame.value_usd / frame.quantity_tonnes
    frame["quantity_share"] = frame.quantity_tonnes / frame.groupby("year").quantity_tonnes.transform("sum")
    frame["weight_estimated"] = frame.isNetWgtEstimated
    columns = ["year", "country", "quantity_tonnes", "value_usd",
               "fob_usd_per_tonne", "quantity_share", "weight_estimated"]
    return frame[columns].sort_values(["year", "country"])


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    raw, repaired = read_raw(ROOT / config["input_csv"])
    clean = clean_china(raw, config["countries"])
    output = ROOT / config["clean_csv"]
    output.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output, index=False, encoding="utf-8-sig")
    audit = {"source": config["input_csv"], "raw_rows": len(raw),
             "repaired_trailing_empty_rows": repaired, "china_rows": len(clean),
             "estimated_weight_rows": int(clean.weight_estimated.eq("true").sum()),
             "quantity_source": "netWgt / 1000 (tonnes)", "value_source": "fobvalue (USD)",
             "years": sorted(clean.year.unique().tolist()), "scope": "USA/BRA/ARG -> CHN only"}
    output.with_name("data_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    logging.info("修复 %s 行尾部空字段；保留 %s 条对华记录", repaired, len(clean))


if __name__ == "__main__":
    main()
