数据整体可分为三组，服务于“关税—贸易—宏观经济”分析。

### 1. 关税数据（2015—2025）

每个年份文件基本是美国 HTS 关税税则数据库，`.xlsx` 与 `.txt` 多为同一数据的不同格式。

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\Tariff Data\tariff_data_2025\tariff_database_2025.xlsx" artifact_kind="workbook" purpose="source"}

主要字段含义：

- `hts8`：美国 8 位税则号，用于识别具体商品。
- `brief_description`：商品简要描述。
- `quantity_1_code`、`quantity_2_code`：计量单位，如千克、件、数量等。
- `mfn_text_rate`：最惠国税率的文字表示。
- `mfn_ad_val_rate`：从价税率，例如 `0.25` 表示 25%。
- `mfn_specific_rate`：从量税率，例如每千克征收多少美元。
- `mfn_other_rate`：其他形式的税率或附加税。
- `mfn_rate_type_code`：税率类型代码，用于区分从价税、从量税等。
- `wto_binding_code`：WTO 约束税率相关标识。
- `col1_special_text`：特殊贸易待遇或特殊税率说明。
- `gsp_indicator`：普惠制待遇标识。
- `nafta_canada_ind`、`nafta_mexico_ind`：加拿大、墨西哥相关优惠待遇标识。
- `mexico_ad_val_rate`、`mexico_specific_rate`：对墨西哥适用的税率。
- 各类 `*_indicator`：表示某项贸易协定、优惠政策或特殊待遇是否适用。
- 日期字段：表示税率或特殊措施的生效、失效时间。

这些数据适合用于比较不同年份的税率变化、分析某类商品的关税水平，以及识别特定国家的优惠税率。

### 2. 美国贸易数据

#### 大豆出口数据

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\Trade Data\Soybean_Competition_Exports_to_China_2015_2024.csv" artifact_kind="workbook" purpose="source"}

该文件记录阿根廷、巴西等大豆出口国向中国及全球的出口情况。

- `reporterISO`：报告国，例如 `ARG`、`BRA`。
- `partnerISO`：贸易伙伴，例如 `CHN` 表示中国，`W00` 表示全球。
- `flowDesc`：贸易流向，本文件主要是出口。
- `refYear`、`period`：年份或统计期。
- `cmdCode`、`cmdDesc`：商品编码和商品名称，这里主要是大豆。
- `qty`、`qtyUnitAbbr`：出口数量及单位。
- `netWgt`：净重量。
- `fobvalue`：离岸价出口金额。
- `primaryValue`：主要贸易价值指标。
- `isQtyEstimated`、`isNetWgtEstimated`：数量或重量是否为估算值。

它可以用来比较不同国家对中国的大豆出口规模和竞争关系。

#### 美国从日本、墨西哥进口汽车

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\Trade Data\US_Auto_Imports_JP_2015_2024.xlsx" artifact_kind="workbook" purpose="source"}

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\Trade Data\US_Auto_Imports_MX_2015_2024.xlsx" artifact_kind="workbook" purpose="source"}

两个文件结构相同，记录美国从日本和墨西哥进口汽车的年度海关价值：

- `Data Type`：指标类型，这里是 `General Customs Value`。
- `TOTAL`：2015—2024 年累计进口金额。
- `2015`—`2024`：各年度进口金额。
- 金额单位通常为美元。

可以用来分析美国汽车进口来源变化，并比较日本与墨西哥在美国汽车市场中的份额。

#### 美国进口汽车和芯片数据

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\Trade Data\US_Import_Cars_Chips_2015_2024.csv" artifact_kind="workbook" purpose="source"}

该文件是更细的贸易明细数据，包含美国从中国、日本、墨西哥等国家进口汽车和半导体产品。

- `partnerISO`：进口来源国。
- `flowDesc`：进口。
- `cmdCode`、`cmdDesc`：HS 商品编码及商品描述。
- 汽车相关商品主要是 `8703` 类。
- 芯片相关商品主要包括 `8541`、`8542` 等类别。
- `primaryValue`、`cifvalue`：进口贸易金额。
- `qty`、`netWgt`：数量和重量。
- `isAggregate`、`isLeaf`：是否为汇总项目或最底层商品项目。

该文件适合研究汽车、芯片进口规模及其来源国变化。

### 3. 美国宏观经济数据

这些文件大多是月度或季度时间序列，覆盖约 2015—2025 年。

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\US_Macroeconomic\US_CPI_2015_2025.csv" artifact_kind="workbook" purpose="source"}

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\US_Macroeconomic\US_GDP_2015_2025.csv" artifact_kind="workbook" purpose="source"}

:codex-file-citation{path="C:\Users\lenovo\Desktop\题目\10.25\data\US_Macroeconomic\Chip_Production.csv" artifact_kind="workbook" purpose="source"}

| 文件                              | 数据含义                                     | 频率 |
| --------------------------------- | -------------------------------------------- | ---- |
| `Chip_High_IC.csv`                | 高端集成电路生产者价格指数，`WPU1176`        | 月度 |
| `Chip_Low_Discrete.csv`           | 低端/分立半导体生产者价格指数，`WPU1178`     | 月度 |
| `Chip_Production.csv`             | 半导体及相关电子元件工业生产指数，`IPG3344S` | 月度 |
| `US_CPI_2015_2025.csv`            | 美国消费者价格指数，衡量整体消费品价格水平   | 月度 |
| `US_CUSR0000SETA01_2015_2025.csv` | 美国服装类消费者价格指数                     | 月度 |
| `US_DEXCHUS_2015_2025.csv`        | 美元兑人民币汇率，`DEXCHUS`                  | 日度 |
| `US_DEXJPUS_2015_2025.csv`        | 日元兑美元相关汇率，`DEXJPUS`                | 日度 |
| `US_GDP_2015_2025.csv`            | 美国国内生产总值，单位通常为十亿美元         | 季度 |
| `US_PCU33443344_2015_2025.csv`    | 半导体及相关设备生产者价格指数               | 月度 |
| `US_PCU336336_2015_2025.csv`      | 汽车及零部件制造业生产者价格指数             | 月度 |
| `US_PPIACO_2015_2025.csv`         | 美国全部商品生产者价格指数                   | 月度 |

其中：

- `observation_date`：观测日期。
- 第二列代码，如 `GDP`、`CPIAUCSL`：具体经济指标值。
- CPI、PPI 和行业价格指数反映价格变化。
- GDP 反映宏观经济总量。
- 汇率数据可用于解释进口成本、贸易价格和竞争力变化。
- 芯片生产指数和芯片价格指数可用于分析半导体产业供给与价格变化。

### 总体关系

这些数据可以组合成如下分析逻辑：

关税税率变化  
→ 影响进口成本和商品价格  
→ 影响汽车、芯片、大豆等贸易流量  
→ 进一步与 GDP、CPI、汇率、产业生产指数联系起来。

需要注意的是，关税数据库中的税率是“法定或适用税率”，贸易数据中的金额是实际贸易结果，两者不能直接认为存在一一对应关系，还需要按照商品编码、国家和年份进行匹配。