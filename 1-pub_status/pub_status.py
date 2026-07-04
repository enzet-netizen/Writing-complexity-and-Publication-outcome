import pandas as pd, requests, time, os

INPUT   = 'arxiv_clean.csv'
CACHE   = 'pub_status_raw.csv'
OUTPUT  = 'pub_status.csv'
API_KEY = ''   

df = pd.read_csv(INPUT, dtype={'arxiv_id': str})
df = df[df['pub_month'] >= '2023-01'].copy()

df['doi'] = df['doi'].fillna('').astype(str).str.strip()
pairs = df[df['doi'] != ''][['arxiv_id', 'doi']].copy()
pairs['doi'] = pairs['doi'].str.lower().str.split()
pairs = pairs.explode('doi').drop_duplicates()
pairs = pairs[~pairs['doi'].str.contains(',')] 

done = set()
if os.path.exists(CACHE):
    done = set(pd.read_csv(CACHE, sep='|', dtype=str)['doi'])
todo_dois = [x for x in pairs['doi'].unique() if x not in done]

if not os.path.exists(CACHE):
    with open(CACHE, 'w') as f:
        f.write('doi|found|published|pub_date|venue\n')

url = 'https://api.openalex.org/works'
BATCH = 50

for i in range(0, len(todo_dois), BATCH):
    bdoi = todo_dois[i:i+BATCH]
    params = {'filter': 'doi:' + '|'.join(bdoi), 'per-page': 100, 'api_key': API_KEY}

    results = []
    for attempt in range(3):
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 429:
                time.sleep(10)
                continue
            results = r.json().get('results', [])
            break
        except Exception as e:
            print('retry:', e)
            time.sleep(5)

    found_map = {}
    for w in results:
        wdoi = (w.get('doi') or '').lower().replace('https://doi.org/', '')
        found_map[wdoi] = w

    lines = []
    for d1 in bdoi:
        w = found_map.get(d1)
        if w is None:
            lines.append(f'{d1}|0|0||\n')
            continue
        published, venue = 0, ''
        locs = [w.get('primary_location')] + (w.get('locations') or [])
        for loc in locs:
            if not loc:
                continue
            src = loc.get('source') or {}
            if src.get('type') in ('journal', 'conference'):
                published = 1
                venue = (src.get('display_name') or '').replace('|', ' ')
                break
        lines.append(f"{d1}|1|{published}|{w.get('publication_date') or ''}|{venue}\n")

    with open(CACHE, 'a') as f:
        f.writelines(lines)
    if (i // BATCH) % 20 == 0:
        print(i + len(bdoi), '/', len(todo_dois))
    time.sleep(0.12)

raw = pd.read_csv(CACHE, sep='|', dtype=str)
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
