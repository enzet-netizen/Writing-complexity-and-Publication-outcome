# Writing Complexity and Publication Outcomes

Replicator: Enzo Tang

Original paper: Kusumegi, K., de Vaan, M., Stuart, T., & Yin, Y. (2025).
Scientific production in the era of large language models.
*Science*, 390, 1240. https://doi.org/10.1126/science.adw3000

Last updated: July 2026

The fact that LLMs can almost effortlessly produce polished, professional text describing any scientific topic raises an important question: Does LLM use reveal or
conceal the quality of the underlying research?

<img width="775" height="89" alt="image" src="https://github.com/user-attachments/assets/8235d978-a881-4861-b051-3b9b84752ac8" />

---

## 1.发表结果追踪

#### input文件：arxiv_clean.csv
#### 运行文件：pub_status.py
#### 中间文件：pub_status_raw.csv
#### output文件：pub_status.csv

As a proxy for quality, we then created a binary outcome defined as publication in a peer-reviewed journal or conference by the end of our observation window (June 2024)
for all preprints since 2023.

We traced the publication outcomes of preprints from arXiv, bioRxiv, and SSRN using OpenAlex. For arXiv and bioRxiv papers, we linked them to their corresponding records in OpenAlex using their DOI.


给每篇 2023 年后的 preprint 打一个 0/1 标签，代表截至 2024 年 6 月它有没有通过同行评审发表。doi为空，就是没有发表，doi有值，去查openAlex，即发表成功。
元数据 doi 字段偶含多个 DOI,本复现将全部 DOI 逐一查询，任一命中期刊/会议即判定发表，发表日期取最早。

doi为空（144,717 篇，66.2%）,作者未回填任何期刊信息，直接判 published=0，不做查询
doi有值（73,915 篇，33.8%）,拿期刊 DOI 批量查询 OpenAlex，检查返回记录的locations中是否存在 journal, conference的来源,是则 published=1




## 2.时间筛选
#### input文件：arxiv_clean.csv, pub_status_raw.csv
#### 运行文件：pub_statis_time.py
#### output文件： pub_status_final.csv

by the end of our observation window (June 2024)

论文的发表结果只统计到 2024 年6月为止，需要进行截断。
把 publication_date > 2024-06-30 的论文重标为 0，得到与论文时间口径一致的最终因变量 published_censored

<img width="142" height="43" alt="image" src="https://github.com/user-attachments/assets/388fb3dc-66a8-4475-ad15-d17f45b4b58e" />。

probability：。

<img width="249" height="92" alt="image" src="https://github.com/user-attachments/assets/130d2653-c4e8-4cdb-845e-c2d56162846b" />。

count：

<img width="262" height="110" alt="image" src="https://github.com/user-attachments/assets/79a20188-9a42-4ec7-acae-25971e0862c8" />。

<img width="261" height="137" alt="image" src="https://github.com/user-attachments/assets/59708c6d-3be5-41ce-bd95-4c8688ee5887" />。








---


## 3.连接作者与性别分析结果
把性别结果贴回每个作者,通过左连接进行。性别没有判断出来的就写unknown.

#### input文件：authors_clean.csv，gender_cache.csv'
#### 运行文件：gender_match.py
#### output文件：authors_gender.csv

<img width="522" height="93" alt="image" src="https://github.com/user-attachments/assets/629887af-b49b-4210-ba72-5030bdc78305" />

接回性别表：
female     24272
male      114296，
无法查到性别的：4280，总计142848

---


## 4.构建panel

<img width="897" height="94" alt="image" src="https://github.com/user-attachments/assets/1feb3055-f50e-4e50-86bd-ea668797f892" />

<img width="568" height="88" alt="image" src="https://github.com/user-attachments/assets/7e0433ee-5462-49dd-8d16-bd27f5b67c21" />

#### input文件：panel.csv,authors_gender.csv
#### 运行文件：panel_gender.py
#### output文件：panel_gender.csv

<img width="446" height="33" alt="image" src="https://github.com/user-attachments/assets/4875878d-8a3a-4fae-ae9b-741076e4991c" />


<img width="229" height="61" alt="image" src="https://github.com/user-attachments/assets/46d74b9e-be8d-4acb-bd1e-de5c1da54cdf" />

<img width="161" height="38" alt="image" src="https://github.com/user-attachments/assets/7353a7db-cfef-47c5-b776-381de727a0f9" />


<img width="490" height="36" alt="image" src="https://github.com/user-attachments/assets/d33d44ca-f21d-4d3b-96c5-794db8472205" />








## 5.回归

#### input文件：panel_gender.csv
#### 运行文件：panel_gender.do
#### output文件：gender_coefficients.csv

<img width="309" height="17" alt="image" src="https://github.com/user-attachments/assets/b69a87b3-bfcd-42ff-9d0a-0610b5278b98" />.


<img width="314" height="177" alt="image" src="https://github.com/user-attachments/assets/1fba0d34-fa30-49b6-9134-af818058e16e" />.


<img width="190" height="20" alt="image" src="https://github.com/user-attachments/assets/b1e5564b-5123-4767-aa0c-8674429de2d7" />.


<img width="314" height="15" alt="image" src="https://github.com/user-attachments/assets/cb7c81d9-bd5a-4bdd-810e-5c436f0f8514" />.

<img width="225" height="74" alt="image" src="https://github.com/user-attachments/assets/b9fe7ea3-30b8-4461-8cfa-587644f70173" />

进回归的数据：male:78713, female:16843

用python进行回归




## 6.生图
#### input文件：gender_coefficients
#### 运行文件：gender_plot.py

<img width="1476" height="879" alt="image" src="https://github.com/user-attachments/assets/4180e258-cc33-496a-bef8-692c0f60337e" />

<img width="992" height="645" alt="image" src="https://github.com/user-attachments/assets/036b7eba-ac2b-4195-9c95-a1d88639494d" />

<img width="989" height="528" alt="image" src="https://github.com/user-attachments/assets/07dd7b13-9a1d-4433-9c62-0232845fc121" />

<img width="994" height="530" alt="image" src="https://github.com/user-attachments/assets/3f7a64a2-0cf3-4114-92bd-12f6a2de32a5" />








Overall 39.3%，Male 38.6%，置信区间36.3%-40.9%，Female 42.8%，置信区间37.7%-48%
<img width="495" height="501" alt="image" src="https://github.com/user-attachments/assets/b65cd48e-f231-4aba-8760-1a6111e05384" />


## Additional
用python进行代码实现

<img width="1474" height="874" alt="image" src="https://github.com/user-attachments/assets/cacc0b62-b2b7-449c-83e7-d898ca478f59" />

<img width="990" height="623" alt="image" src="https://github.com/user-attachments/assets/2da25fcd-0282-4ba1-bcde-fe89db745fad" />


<img width="1001" height="505" alt="image" src="https://github.com/user-attachments/assets/68f0ac27-6009-40c4-b494-6e792c8c5633" />

<img width="995" height="531" alt="image" src="https://github.com/user-attachments/assets/b3e8337d-b111-4e69-b036-56d8d1bc52e2" />


