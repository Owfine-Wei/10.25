# 第一问文件结构与运行说明

## 2025年4月研究补充（2026-10-25）

研究4月政策请使用 `run_april.py`，原 `run.py` 保留为假设情景演示。

```powershell
& 'C:\Users\lenovo\.conda\envs\Lpytorch\python.exe' -B 'python\Q1\run_april.py'
```

新增参数全部集中于 `config.json` 的 `april_2025` 字段，图形仍共享 `config_pic.json`。

| 新增文件 | 作用 |
| --- | --- |
| python/Q1/run_april.py | 4月研究入口，保留原演示输出 |
| python/Q1/stage_2/april_analysis.py | 保留3月措施的配对反事实、两种旧税条件、弹性与容量实验 |
| python/Q1/stage_3/april_report.py | 参数诊断图与4月结果解释的自动生成 |
| result/Q1/april_scenario_results.csv | 2种旧税条件×3组参数×4种状态×3国，72行 |
| result/Q1/april_robustness.csv | 27组弹性和3组容量实验×3国，90行 |
| result/Q1/april_diagnostics.json | 本次配置、10项检查与求解残差 |
| result/Q1/fig04_april_diagnostics.png | 同一政策冲击下的数量、价格响应比较 |
| result/Q1/2025年4月结果解释补充.md | 自动生成的4月政策模拟与合理性诊断 |
| result/Q1/2025年4月政策与参数依据.md | 人工核实的政策、文献链接、参数依据及未决限制 |
| result/Q1/第一问建模与验证写作稿.md | 论文方法、验证和篇幅结构的写作稿 |

4月入口固定更新5个结果文件及2个预处理文件，另2份研究/写作说明不由程序覆盖。
`april_quantity_change_pct`、`april_price_change_pct`、`april_value_change_pct` 均相对“保留3月措施、无4月新增”的同参数反事实。
原 `quantity_change_pct` 等字段仍相对2024校准点。`counterfactual_*` 保存配对对照的水平值。
不将年度基期规模除以12来冒充4月到港量；34%仅是公告方案，旧税排除和在途例外是不同条件。

## 运行

在项目根目录的 PowerShell 中执行（已经用本机 Lpytorch 环境验证）：

```powershell
& 'C:\Users\lenovo\.conda\envs\Lpytorch\python.exe' -B 'python\Q1\run.py'
```

也可在已激活且满足 requirements.txt 的 Python 环境中执行 `python -B python/Q1/run.py`。
脚本以文件位置定位项目根目录，不依赖当前工作目录。依赖已存在，未安装或升级任何包。

代码遵循 `skill/代码书写.md` 的分阶段、配置集中、函数小于 100 行、统一配色等要求。
规范原先指定 `python/result/Qx`，本次用户明确要求 `result/Q1`，因此以本次要求为准。
每次运行固定生成 2 个预处理文件和 10 个结果文件，不逐次输出敏感性试验文件。
同名结果会更新；原始数据和已有 `analysis_q1.py` 不修改。

## 完整文件清单

以下路径均相对于项目根目录；仅列本问代码、依赖输入和输出。

```text
data/Trade Data/
└── Soybean_Competition_Exports_to_China_2015_2024.csv  # 原始年度贸易数据（不修改）
script/
└── prepare_q1.py                       # 清理尾部空列，提取对华记录，生成审计
outputs/Q1/
├── china_soybean_clean.csv             # 2015—2024年三国对华数量、FOB金额及单价
└── data_audit.json                     # 数据来源、修复行数、估算净重标识等审计
python/Q1/
├── run.py                             # 一键运行全部阶段，并输出日志
├── config.json                        # 年份、路径、税率情景、弹性、运费、容量、求解参数
├── config_pic.json                    # 全部图片的统一国家颜色、字体、尺寸、分辨率
├── requirements.txt                   # 本机验证通过的依赖库名称、版本及用途
├── common/
│   ├── __init__.py                     # 公共模块包标识
│   ├── io_utils.py                     # 项目路径、JSON读写
│   └── validation.py                   # 10项基期、会计、约束及边界检查
├── stage_1/
│   ├── __init__.py                     # 校准阶段包标识
│   └── calibration.py                  # 校准基期数量、价格、CES权重与供给上限
├── stage_2/
│   ├── __init__.py                     # 均衡阶段包标识
│   ├── equilibrium.py                  # CES需求、带上限的供给、非线性均衡求解
│   └── scenarios.py                    # 主情景、弹性敏感性和关税扫描
├── stage_3/
│   ├── __init__.py                     # 输出阶段包标识
│   ├── plots.py                        # 三张组合图的绘制
│   └── report.py                       # 用计算结果自动生成中文图文解释
└── docs/
    └── file_tree.md                    # 本文件：清单、运行、参数和字段说明
result/Q1/
├── .gitignore                         # 项目原有文件，未修改
├── baseline.csv                       # 2024年基期贸易和校准参数
├── scenario_results.csv               # 4个情景×3国：量、价、金额、份额、变化率
├── sensitivity_results.csv            # 27组弹性×3国：重点情景参数敏感性
├── tariff_curve.csv                   # 11个加税幅度×3国：税率响应曲线
├── diagnostics.json                   # 均衡残差、总量、价格指数、10项检查结果
├── config_used.json                   # 本次模型和图片配置快照
├── fig01_history.png                  # 历史数量与三国数量份额
├── fig02_scenarios.png                # 各关税情景的对华出口量与FOB出口额
├── fig03_response_sensitivity.png      # 税率响应与弹性敏感性区间
└── 解释结果文档.md                     # 模型、假设、图表解读、数值结果和局限
```

## 调参方法

所有模型参数在 `config.json`，所有图片样式在 `config_pic.json`。

| 配置项 | 含义与修改规则 |
| --- | --- |
| base_year | 基期，必须存在三国数据 |
| substitution_elasticity | 来源国替代弹性 σ，大于0，支持等于1的极限 |
| demand_elasticity | 综合需求价格弹性的绝对值 η，非负 |
| supply_elasticity | 各国面向中国的供给弹性 ε，必须为正 |
| base_tariff | 中国对各国大豆的基准适用税率，0.03表示3%，当前为假设 |
| freight_usd_per_tonne | 单位运费，美元/吨，当前零值为简化假设 |
| capacity_multiplier | 基期对华数量的可供给上限倍数，不能小于1 |
| scenarios[].tariff_addition | 相对基准税率新增值，0.25表示增加25个百分点 |
| focus_scenario | 用于报告重点分析与弹性敏感性的情景ID |
| sensitivity.supply_scale | 同时乘在三国供给弹性上的系数，不改变容量 |
| sensitivity.tariff_grid | 税率曲线中美国来源的新增税率列表 |
| solver | 求解容差、最大迭代评估数与允许相对残差 |

`baseline` 情景ID应保留且所有新增税率为零。默认国家顺序为 USA、BRA、ARG，模型和绘图面向这三个国家。
主情景中的基准税率、加税幅度与弹性不是由原始CSV估计或核验的事实。
当前三国对华子市场是一个简化封闭系统，供给曲线不单独模拟其他目的地或国内消费。

## 输出字段

| 字段 | 单位或定义 |
| --- | --- |
| quantity_tonnes | 对华出口量，吨 |
| value_usd | 对华FOB出口额，美元，等于FOB单价乘数量 |
| fob_usd_per_tonne | 离岸单位价值／模型均衡价格，美元/吨 |
| landed_usd_per_tonne | 含假设运费与中国关税的采购价格，美元/吨 |
| quantity_share / value_share | 三国合计内部份额，0—1，不是中国全部进口份额 |
| quantity_change_pct / price_change_pct / value_change_pct | 相对基期变化，单位为%，不是比率 |
| tariff | 中国最终适用税率，0.28表示28% |
| tariff_addition_pp | 新增关税百分点，25表示加25个百分点 |
| capacity_binding | 该国对华供给是否达到假设上限 |
| ces_weight | 基期含税采购支出份额，用于归一化CES价格指数 |
| price_index | CES价格指数相对基期之比，基期为1 |
| composite_demand_ratio | CES综合需求比率，不能当作实物总吨数比率 |
| max_relative_residual | 最大绝对供需相对误差 max(abs(D/S-1)) |

预处理审计中的 estimated_weight_rows 记录原始净重是否标记为估算。原始CSV的 World 记录全部排除。
原始 `qty` 不用于计算；CSV只修复多出的空字段，非空多余字段、重复国家年份、缺失或非正净重/FOB金额均报错。

## 检验的边界

默认运行包含基期复现、出口额会计恒等式、份额归一、正值、容量约束、美国税率响应单调性、容量绑定压力测试和σ=1极限检查。
每次均衡求解都会核查数值残差；任一失败则停止，不继续生成新报告。
这些检查证明程序和模型内部关系一致，不证明参数有实证依据，也不证明对2025年真实贸易预测准确。
