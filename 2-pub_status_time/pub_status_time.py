import pandas as pd

INPUT_CLEAN = 'arxiv_clean.csv'
INPUT_RAW = 'pub_status_raw.csv'
OUTPUT= 'pub_status_final.csv'

df = pd.read_csv(INPUT_CLEAN, dtype={'arxiv_id': str})
df = df[df['pub_month'] >= '2023-01'].copy()
df['doi'] = df['doi'].fillna('').astype(str).str.strip()
pairs = df[df['doi'] != ''][['arxiv_id', 'doi']].copy()
pairs['doi'] = pairs['doi'].str.lower().str.split()
pairs = pairs.explode('doi').drop_duplicates()
pairs = pairs[~pairs['doi'].str.contains(',')]

raw = pd.read_csv(INPUT_RAW, sep='|', dtype=str)
raw['found'] = raw['found'].astype(int)
raw['published'] = raw['published'].astype(int)

m = pairs.merge(raw, on='doi', how='left')
m['found'] = m['found'].fillna(0).astype(int)
m['published'] = m['published'].fillna(0).astype(int)
m['pub_date_hit'] = m['pub_date'].where(m['published'] == 1)

agg = m.groupby('arxiv_id').agg(
    found=('found', 'max'),
    published=('published', 'max'),
    pub_date=('pub_date_hit', 'min'),
    venue=('venue', 'first'),
).reset_index()

full = df[['arxiv_id']].drop_duplicates().merge(agg, on='arxiv_id', how='left')
full['found'] = full['found'].fillna(0).astype(int)
full['published'] = full['published'].fillna(0).astype(int)

full['published_censored'] = 0
mask = (full['published'] == 1) & (full['pub_date'].notna()) & (full['pub_date'] <= '2024-06-30')
full.loc[mask, 'published_censored'] = 1

full.to_csv(OUTPUT, index=False)
