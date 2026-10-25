"""IO 工具：配置读取、大豆数据加载、结果写出。"""
from __future__ import annotations

import csv
import json
from pathlib import Path


def get_project_root() -> Path:
    """返回工程根目录（python 的上两级：本文件位于 python/Q1/common）。"""
    return Path(__file__).resolve().parents[3]


def load_config(path) -> dict:
    """读取 JSON 配置。"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_soybean_rows(csv_path) -> list[dict]:
    """用 csv 模块稳健读取大豆贸易数据（尾部多余字段自动忽略）。

    说明：原始 CSV 数据行比表头多字段，pandas 易错位；
    用标准 csv.DictReader 仅映射表头命中的前段列，安全可用。
    """
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def save_dataframe(df, path) -> None:
    """写出 DataFrame 为 CSV（含 BOM 以便 Excel 中文）。"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def save_json(obj, path) -> None:
    """写出 JSON 结果。"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
