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
发表率由0.298变为0，207

