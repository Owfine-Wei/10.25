# 2025 Asia and Pacific Mathematical Contest in Modeling — Problem C

# 2025 亚太地区数学建模竞赛 — C 题

## Impact of U.S. Tariff Policies on Global Trade and Regional Economies

## 美国关税政策对全球贸易与区域经济的影响

---

### Background | 背景

**EN:** On April 2, 2025, the Trump administration introduced the so-called "Reciprocal Tariffs" policy, establishing a 10% "minimum baseline tariff" on all trading partners and imposing additional higher tariffs on approximately 60 countries and regions with which the U.S. ran trade deficits, including China. The U.S. claimed that varying tariff rates and non-tariff barriers among trading partners made it harder for American manufacturers to sell products abroad, leading to persistent U.S. trade deficits and manufacturing decline. Thus, it imposed "reciprocal tariffs" on all countries to reduce its trade deficit and promote manufacturing reshoring[1]. However, this policy is inconsistent with the fundamental principle of "Most-Favored-Nation (MFN) Treatment" of the World Trade Organization (WTO) and also challenges the WTO's tariff preference principle for developing countries. Under WTO rules, members must apply uniform tariffs to all partners, but the Trump administration exercised unilateral pressure and bilateral negotiations to implement widely varying tariff standards across economies, with agreed rates far exceeding previous levels. According to a tariff tracking tool jointly developed by the WTO and International Monetary Fund (IMF), the U.S. trade-weighted average tariff rate on all products rose sharply from 2.44% at the start of 2025 to 20.11% by August 2025[2]. A Yale Budget Lab report noted that this tariff increase pushed the U.S. overall average effective tariff rate to its highest level since 1933[3].

**中：** 2025 年 4 月 2 日，特朗普政府推出了所谓的"对等关税"政策，对所有贸易伙伴设立 10% 的"最低基准关税"，并对包括中国在内的、与美国存在贸易逆差的约 60 个国家和地区加征更高的关税。美国声称，贸易伙伴之间差异化的关税税率和非关税壁垒，使美国制造商更难在海外销售产品，导致美国持续出现贸易逆差并造成制造业衰退。因此，美国对各国加征"对等关税"，以减少贸易逆差、推动制造业回流[1]。然而，该政策违背了世界贸易组织（WTO）"最惠国待遇"的基本原则，也挑战了 WTO 对发展中国家的关税优惠原则。根据 WTO 规则，成员须对所有伙伴适用统一关税，但特朗普政府通过单边施压和双边谈判，在不同经济体间实施差异巨大的关税标准，且协定税率远高于以往水平。根据 WTO 与国际货币基金组织（IMF）联合开发的关税追踪工具，美国对所有产品的贸易加权平均关税税率从 2025 年初的 2.44% 急剧上升至 2025 年 8 月的 20.11%[2]。耶鲁预算实验室（Yale Budget Lab）的一份报告指出，此次关税上调使美国整体平均有效关税税率达到 1933 年以来的最高水平[3]。

**EN:** Beyond serving as a source of fiscal revenue, tariffs are an important tool of national trade policy. Appropriate tariffs can protect domestic industries from global economic monopoly and coercive practices, and are therefore permitted by the WTO.

**中：** 关税除了作为财政收入来源外，还是国家贸易政策的重要工具。适当的关税能够保护国内产业免受全球经济垄断和强制性行为的侵害，因此为 WTO 所允许。

**EN:** However, the impact of tariffs is multifaceted. Excessively high tariffs hinder the development of global trade and are detrimental to long-term world economic growth. In the short term, high U.S. tariffs may bring benefits such as increased tariff revenue and a reduced trade deficit, but they also lead to declining exports and higher domestic consumer prices. For example, according to statistics from General Administration of Customs of the People's Republic of China (GACC) [4], in the month the "reciprocal tariffs" took effect, U.S. imports from China fell 20% year-on-year, while U.S. exports to China dropped 13% due to Chinese countermeasures. By May 2025, imports from China had fallen 35% compared with May 2024, and exports to China declined 18%. In absolute terms, the U.S. trade deficit with China narrowed from $30.8 billion in May 2024 to $18.0 billion in May 2025, but U.S. exports to China also fell from $13.2 billion to $10.4 billion, negatively impacting related U.S. industries. Overall, the adverse effects of high tariffs on U.S. trade and the economy cannot be overlooked.

**中：** 然而，关税的影响是多方面的。过高的关税阻碍全球贸易的发展，不利于世界经济的长期增长。短期内，美国的高关税可能带来关税收入增加、贸易逆差缩小等好处，但也会导致出口下降和国内消费者价格上涨。例如，根据中华人民共和国海关总署（GACC）[4] 的统计数据，在"对等关税"生效当月，美国从中国进口同比下降 20%，而受中国反制措施影响，美国对华出口下降 13%。到 2025 年 5 月，自华进口较 2024 年 5 月下降 35%，对华出口下降 18%。从绝对值看，美国对华贸易逆差从 2024 年 5 月的 308 亿美元收窄至 2025 年 5 月的 180 亿美元，但美国对华出口也从 132 亿美元降至 104 亿美元，对美国相关产业造成负面影响。总体而言，高关税对美国贸易和经济的负面影响不容忽视。

---

### Task | 任务

**EN:** Your team is tasked with analyzing the impact of U.S. tariff policy adjustments on international trade and regional economies, based on U.S. tariff and global trade data. Address the following questions:

**中：** 你们团队的任务是基于美国关税及全球贸易数据，分析美国关税政策调整对国际贸易和区域经济的影响。请回答以下问题：

---

### Question 1 | 问题一

**EN:** The United States, Brazil, and Argentina are the world's largest soybean producers and exporters, while China is the largest soybean importer. Analyze the current state of soybean trade between China and these countries. Develop a model to assess the impact of U.S. tariff adjustments on the soybean industries of the U.S., Brazil, and Argentina. Estimate the post-adjustment distribution of soybean export volumes and values for these three countries.

**中：** 美国、巴西和阿根廷是世界上最大的大豆生产国和出口国，而中国是最大的大豆进口国。分析中国与这些国家之间大豆贸易的现状。建立模型评估美国关税调整对美、巴、阿三国大豆产业的影响。估算调整后这三国大豆出口量与出口额的分布情况。

---

### Question 2 | 问题二

**EN:** The United States is the world's second-largest automobile market and the largest automobile importer. In 2024, 46% of cars sold in the U.S. were imported [5], with Japan as a major source. Besides direct exports from Japan, Japanese automakers also invest in U.S. production or manufacture in countries like Mexico for export to the U.S. Analyze the current position of Japanese automobiles in the U.S. market. Develop a model that incorporates Japan's non-tariff response strategies and economic transmission effects to examine the impact of U.S. tariff adjustments on U.S.-Japan automobile trade, the structure of U.S. auto imports, and the U.S. automobile industry.

**中：** 美国是全球第二大汽车市场，也是最大的汽车进口国。2024 年，美国市场销售的汽车中有 46% 为进口[5]，其中日本是主要来源国。除直接从日本出口外，日本汽车制造商还在美国投资设厂，或在墨西哥等国生产后出口至美国。分析日本汽车在美国市场的现状。建立模型，纳入日本的非关税应对策略与经济传导效应，考察美国关税调整对美日汽车贸易、美国汽车进口结构及美国汽车产业的影响。

---

### Question 3 | 问题三

**EN:** The United States dominates the global semiconductor (chip) industry but lacks strong manufacturing capacity. The Biden administration passed the CHIPS and Science Act in August 2022, using subsidies to boost advanced semiconductor manufacturing. However, the Trump administration in 2025 argued that tariffs are more effective than subsidies. Concurrently, the U.S. imposed export controls on high-end chips to China, citing national security and technological leadership concerns. Develop a model analyzing the effects of U.S. tariff policies on domestic semiconductor manufacturing and trade in high-, mid-, and low-end chips, considering both economic efficiency and national security.

**中：** 美国主导着全球半导体（芯片）产业，但缺乏强大的制造能力。拜登政府于 2022 年 8 月通过《芯片与科学法案》，以补贴推动先进半导体制造。然而，2025 年的特朗普政府认为关税比补贴更有效。与此同时，美国以国家安全和技术领先为由，对高端芯片对华实施出口管制。建立模型，在分析经济效率与国家安全双重因素的基础上，考察美国关税政策对国内半导体制造以及高、中、低端芯片贸易的影响。

---

### Question 4 | 问题四

**EN:** Raising tariff rates may increase government tariff revenue in the short term but reduce trade volumes, potentially lowering revenue over time. Develop a model to analyze the short- and medium-term impact of U.S. tariff adjustments on U.S. tariff revenue. Predict the net change resulting from these adjustments in U.S. tariff revenue during the second term of the Trump administration.

**中：** 提高关税税率可能在短期内增加政府关税收入，但会减少贸易量，从而可能随着时间的推移降低收入。建立模型分析美国关税调整对美国关税收入的短中期影响。预测上述调整在特朗普政府第二任期内给美国关税收入带来的净变化。

---

### Question 5 | 问题五

**EN:** U.S. tariff hikes may trigger countermeasures from trading partners. For instance, China imposed reciprocal tariff countermeasures and implemented targeted export controls on rare earths, lithium batteries, etc. [9]. These countermeasures will undoubtedly bring complex impacts on U.S. foreign trade, thereby exerting comprehensive and profound effects on agriculture, industry, and other sectors within the United States, and may also affect financial markets such as the U.S. dollar, U.S. Treasury bonds, and virtual currencies. Select or construct economic indicators to model the short- and medium-term impact of U.S. tariff adjustments on the U.S. economy. Use the model to evaluate whether the "reciprocal tariffs" policy can genuinely drive manufacturing reshoring.

**中：** 美国提高关税可能引发贸易伙伴的反制措施。例如，中国实施了对等关税反制，并对稀土、锂电池等实施了针对性出口管制[9]。这些反制措施无疑将给美国外贸带来复杂影响，进而对美国国内的农业、工业等领域产生全面而深远的影响，并可能波及美元、美国国债、虚拟货币等金融市场。选取或构建经济指标，建立模型分析美国关税调整对美国经济的短中期影响。利用该模型评估"对等关税"政策是否真正能够推动制造业回流。

---

### Glossary | 术语表

**EN:** Reciprocal Tariffs: Originally refers to a system where two or more countries mutually reduce or eliminate import tariffs through bilateral or multilateral negotiations. Here, it specifically denotes the tariff policy announced by the Trump administration on April 2, 2025. While nominally implying equal tariff rates between the U.S. and its partners, the U.S. imposed a 10% "minimum baseline tariff" on all partners and additional tariffs ranging from 11% to 50% on approximately 60 trading partners.

**中：** 对等关税（Reciprocal Tariffs）：原指两个或多个国家通过双边或多边谈判相互降低或取消进口关税的体系。此处特指向特朗普政府于 2025 年 4 月 2 日宣布的关税政策。虽然名义上意味着美国与其伙伴之间实行同等关税税率，但美国对所有伙伴加征 10% 的"最低基准关税"，并对约 60 个贸易伙伴加征 11% 至 50% 不等的额外关税。

**EN:** Most-Favored-Nation (MFN) Treatment: Refers to the tariff and non-tariff preferential treatments mutually granted by WTO members that are no less favorable than those granted to any third country. According to Article I of the General Agreement on Tariffs and Trade (GATT 1994), any preference granted by a member to another member must be immediately and unconditionally extended to all other members.

**中：** 最惠国待遇（Most-Favored-Nation, MFN）：指 WTO 成员相互给予的、不低于其给予任何第三国的关税与非关税优惠待遇。根据《1994 年关税与贸易总协定》（GATT 1994）第一条，一成员给予另一成员的任何优惠，必须立即、无条件地扩及所有其他成员。

---

### Data Notes | 数据说明

**EN:** The attached data provides U.S. foreign trade data from 2020 onward, sourced from U.S. Trade & Tariff Data [6]. Teams are not limited to this data and may obtain additional trade data from official sources such as [4] or non-tariff policy information from sources like [9]. Reasonable simulated data is also permitted.

**中：** 附件数据提供了 2020 年以来的美国对外贸易数据，来源于美国贸易与关税数据[6]。参赛队伍不限于使用该数据，也可从 [4] 等官方来源获取额外贸易数据，或从 [9] 等来源获取非关税政策信息。合理的模拟数据同样允许使用。

---

### References | 参考文献

**[1] EN:** The White House, *Regulating Imports with a Reciprocal Tariff to Rectify Trade Practices that Contribute to Large and Persistent Annual United States Goods Trade Deficits.*
https://www.whitehouse.gov/presidential-actions/2025/04/regulating-imports-with-a-reciprocal-tariff-to-rectify-trade-practices-that-contribute-to-large-and-persistent-annual-united-states-goods-trade-deficits/

**[1] 中：** 美国白宫，《以对等关税监管进口，纠正导致美国年度货物贸易持续巨额逆差的贸易行为》。

**[2] EN:** China Financial Information Network, [Global Finance] U.S. Average Tariff Rate Surges Significantly.
https://www.cnfin.com/hg-lb/detail/20250809/4283370_1.html

**[2] 中：** 中国金融信息网，《[环球金融] 美国平均关税税率大幅飙升》。

**[3] EN:** Yale Budget Lab, *State of U.S. Tariffs: August 7, 2025.*
https://budgetlab.yale.edu/research/state-us-tariffs-august-7-2025

**[3] 中：** 耶鲁预算实验室，《美国关税现状：2025 年 8 月 7 日》。

**[4] EN:** General Administration of Customs of the People's Republic of China, Customs Statistics.
http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/index.html

**[4] 中：** 中华人民共和国海关总署，《海关统计》。

**[5] EN:** China Automotive News, *U.S. Establishes New Tariff Barriers: Impact on Imported Cars?*
http://www.cnautonews.com/yaowen/2025/02/28/detail_20250228372164.html

**[5] 中：** 中国汽车报，《美国设立新关税壁垒：对进口车影响几何？》

**[6] EN:** DataWeb: U.S. Trade & Tariff Data.
https://dataweb.usitc.gov/

**[6] 中：** DataWeb：美国贸易与关税数据。

**[7] EN:** Stephen Miran. *A User's Guide to Restructuring the Global Trading System.* Hudson Bay Capital.
https://www.hudsonbaycapital.com/documents/FG/hudsonbay/research/638199_A_Users_Guide_to_Restructuring_the_Global_Trading_System.pdf

**[7] 中：** Stephen Miran，《重构全球贸易体系使用者指南》。Hudson Bay Capital。

**[8] EN:** Digital Economy Laboratory, University of International Business and Economics, *Monthly Monitoring Report on China-U.S. Goods Trade (Jan-Aug 2025).*
https://delab.uibe.edu.cn/kydt/cgzs/2025n/2025n8yjcbg/d9650830544c49e2812662f722b08325.htm

**[8] 中：** 对外经济贸易大学数字经济实验室，《中美货物贸易月度监测报告（2025 年 1—8 月）》。

**[9] EN:** Ministry of Commerce of the People's Republic of China, Announcements & Orders.
https://www.mofcom.gov.cn/zcfb/blgg/index.html

**[9] 中：** 中华人民共和国商务部，《公告与决定》。
