# Q1 文件架构说明（Armington CES 大豆模型）

## 目录结构
```
python/Q1/
├── config.json            # 模型可配置参数（★ 需按实际情况调整，见下方说明）
├── config_pic.json        # 绘图统一配色与样式
├── requirements.txt       # 依赖库及版本
├── run_all.py             # 一键顺序运行三阶段
├── docs/
│   └── file_tree.md       # 本文件
├── common/                # 通用函数（高内聚、低耦合，被各阶段复用）
│   ├── io_utils.py        # 配置读取、大豆CSV稳健读取、结果写出
│   ├── data_prep.py       # 构建中国进口表、提取基准年参数
│   └── ces_core.py        # Armington CES 核心数学（校准/份额/量额）
├── stage_1_prepare/       # 阶段1：数据预处理与现状分析
│   └── run_prepare.py
├── stage_2_model/         # 阶段2：CES 情景模拟与敏感性分析
│   └── run_ces.py
└── stage_3_visual/        # 阶段3：结果可视化
    └── plot_results.py
```

## 输出文件（位于 result/Q1/）
| 文件 | 含义 |
|---|---|
| historical_shares.csv | 2015–2024 三国对华大豆进口量、价、份额（现状分析） |
| base_params.json | 基准年（默认2024）价格、份额、总进口需求 |
| ces_scenario_results.csv | 三个关税情景下的份额/出口量(Mt)/出口额(十亿$) |
| ces_sensitivity.csv | 中间情景下对 σ 的敏感性结果 |
| sensitivity_meta.json | 敏感性所用的中间情景名 |
| fig_historical_shares.png | 历史份额折线图 |
| fig_scenario_shares.png | 各情景调整后份额柱状图 |
| fig_sensitivity_sigma.png | σ 敏感性折线图 |

## ★ 需你根据实际情况调整的参数（config.json）
| 参数 | 含义 | 调整建议 |
|---|---|---|
| `base_year` | 校准基准年 | 若拿到 2025 全年数据可改为 2025 |
| `sigma` | 替代弹性（核心） | 大豆文献常用 2–4，默认 3.0 |
| `scenarios` | 各情景的关税 τ（美国对华反制关税增量） | 按你采用的 2025 真实反制税率填；巴/阿默认 0 |
| `import_demand.growth_factor` | 调整后中国总进口需求相对基准年的倍数 | 若认为需求增长可设 >1 |
| `base_tariff` | 基准年已存在的关税 | 若要把 2018 贸易战关税纳入基准，可给 USA 设非零 |
| `exclude_years` | 剔除数据损坏年份 | 当前剔除 2017/2018（巴西量价异常） |
| `sensitivity_sigma` | 敏感性扫描的 σ 取值 | 可扩展更多点 |

## 模型口径说明
- 数据列对齐问题：原始 CSV 数据行比表头多字段，故用标准 csv 模块仅取前段有效列。
- 关税通道：模型以"中国对美豆的（额外）反制关税"作为美国关税调整的作用杠杆（对应题目背景的中国反制），
  巴西/阿根廷 τ=0。美国生产端成本上升可后续以 `base_tariff` 或调高 `p_US` 体现。
- `calibrate_alpha=true` 时，模型在基准年精确还原历史份额，仅反映情景关税带来的"贸易转移"。
