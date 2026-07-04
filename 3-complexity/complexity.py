import pandas as pd, textstat

INPUT_CLEAN = 'arxiv_clean.csv'
INPUT_ALPHA = 'alpha_scores.csv'
INPUT_PUB = 'pub_status_final.csv'
OUTPUT      = 'fig3_data.csv'

df    = pd.read_csv(INPUT_CLEAN, dtype={'arxiv_id': str})
alpha = pd.read_csv(INPUT_ALPHA, dtype={'id': str})
pub   = pd.read_csv(INPUT_PUB, dtype={'arxiv_id': str})

df = df[df['pub_month'] >= '2023-01'].copy()

df = df.merge(alpha[['id', 'alpha', 'is_llm']], left_on='arxiv_id', right_on='id', how='inner')

df = df.merge(pub[['arxiv_id', 'published_censored']], on='arxiv_id', how='left')
df['published'] = df['published_censored'].fillna(0).astype(int)


wc_list = []
n = 0
for ab in df['abstract']:
    ab = str(ab)
    if len(ab.split()) < 100:
        wc_list.append(None)
    else:
        wc_list.append(-textstat.flesch_reading_ease(ab)) 
    n += 1
    if n % 20000 == 0:
        print(n, '/', len(df))

df['writing_complexity'] = wc_list
df = df.dropna(subset=['writing_complexity'])
df[['arxiv_id', 'pub_month', 'writing_complexity', 'is_llm', 'published', 'alpha']].to_csv(OUTPUT, index=False)
