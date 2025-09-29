"""Generate a complete catalog and grouping of all .pine files.

Outputs:
 - docs/pine_catalog.csv : row per file with metadata
 - docs/pine_groups.md : proposed grouping and rationale

Algorithm:
 - Read every .pine file (no omitted lines). Extract:
   * declared name: indicator(...)/study(...)/@description/first comment
   * full header comments (first 50 lines) for human-readable description
   * line counts, token counts
   * keyword presence (heuristic list)
   * normalized token shingles (k=5)
 - Compute pairwise Jaccard similarity on shingles and form groups using threshold 0.45 (tunable)
 - For each group choose a representative and list common keywords and files

This is a read-only analysis (it won't modify files) and writes reports only.
"""

import os
import re
import csv
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]
IND = ROOT / 'indicators'
OUT_CSV = ROOT / 'docs' / 'pine_catalog.csv'
OUT_MD = ROOT / 'docs' / 'pine_groups.md'

if not IND.exists():
    print('indicators/ directory not found:', IND)
    raise SystemExit(1)

# regex
indicator_re = re.compile(r"indicator\s*\(\s*['\"](.*?)['\"]", re.IGNORECASE)
study_re = re.compile(r"study\s*\(\s*['\"](.*?)['\"]", re.IGNORECASE)
desc_re = re.compile(r"@description\s*[:=]?\s*(.*)", re.IGNORECASE)
comment_re = re.compile(r"^\s*//\s*(.*)")
string_re = re.compile(r'(".*?(?<!\\)"|\'.*?(?<!\\)\')', re.DOTALL)
nonword_re = re.compile(r"[^0-9A-Za-z_]+")
block_comment_re = re.compile(r"/\*.*?\*/", re.DOTALL)

KEYWORDS = [
    'volume','cumulative','cvd','cv','vwap','value-area','valuearea','value area','vpp','vpp_v4','profile','volume_profile',
    'vsa','vyas','wyckoff','smc','hybrid','scalp','scalping','trend','ema','sma','rma','ma','signal','orderflow','order_flow',
    'confluence','fvg','imbalance','delta','buy','sell','vpo','vpoc','poc','va','vwap','range','session','liquidity',
    'supply','demand','gap','wick','wicked','wick area'
]

K_SHINGLE = 5
MIN_TOKENS = 20
SIM_THRESHOLD = 0.45  # lower to catch family-level similarity

# helper

def normalize_code(text):
    t = block_comment_re.sub(' ', text)
    t = string_re.sub(' ', t)
    # remove single-line comments but keep them in header extraction separately
    t = re.sub(r"//.*?$", ' ', t, flags=re.MULTILINE)
    t = nonword_re.sub(' ', t).lower()
    t = ' '.join(t.split())
    return t


def tokens(text):
    if not text:
        return []
    return text.split()


def shingles_from_tokens(toks, k=K_SHINGLE):
    if len(toks) < k:
        return set()
    return set(' '.join(toks[i:i+k]) for i in range(len(toks)-k+1))


def jaccard(a,b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    uni = len(a | b)
    return inter/uni if uni else 0.0

# collect files
pine_files = [p for p in IND.rglob('*.pine')]
print(f'Found {len(pine_files)} .pine files')

rows = []
shingles_map = {}
keywords_map = {}
header_map = {}

for p in sorted(pine_files):
    try:
        text = p.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print('ERROR reading', p, e)
        continue
    lines = text.splitlines()
    total_lines = len(lines)
    nonempty = sum(1 for L in lines if L.strip())
    # extract declared name
    declared = None
    m = indicator_re.search(text)
    if not m:
        m = study_re.search(text)
    if m:
        declared = m.group(1).strip()
    else:
        m = desc_re.search(text)
        if m:
            declared = m.group(1).strip()
    # header comments (first 40 lines)
    header_lines = []
    for L in lines[:60]:
        cm = comment_re.match(L)
        if cm:
            header_lines.append(cm.group(1).strip())
        elif L.strip()=='' and header_lines:
            break
    header_map[str(p)] = '\n'.join(header_lines)

    norm = normalize_code(text)
    toks = tokens(norm)
    sh = shingles_from_tokens(toks)
    shingles_map[str(p)] = sh

    # keywords
    present = [kw for kw in KEYWORDS if kw in norm]
    keywords_map[str(p)] = present

    rows.append({
        'path': str(p),
        'filename': p.name,
        'declared_name': declared or '',
        'header_sample': header_map[str(p)],
        'total_lines': total_lines,
        'nonempty_lines': nonempty,
        'token_count': len(toks),
        'unique_tokens': len(set(toks)),
        'keywords': '|'.join(present),
        'shingle_count': len(sh)
    })

# pairwise similarity
files = list(shingles_map.keys())
N = len(files)
pairs = []
for i in range(N):
    for j in range(i+1, N):
        a = files[i]
        b = files[j]
        sim = jaccard(shingles_map[a], shingles_map[b])
        if sim >= SIM_THRESHOLD:
            pairs.append((a,b,sim))

print(f'Found {len(pairs)} similar pairs with threshold {SIM_THRESHOLD}')

# group connected components
parent = {}

def find(x):
    parent.setdefault(x,x)
    if parent[x]!=x:
        parent[x] = find(parent[x])
    return parent[x]

def union(a,b):
    ra = find(a); rb = find(b)
    if ra!=rb:
        parent[rb]=ra

for a,b,_ in pairs:
    union(a,b)

groups = defaultdict(list)
for a,b,_ in pairs:
    root = find(a)
    groups[root].append(a); groups[root].append(b)

final_groups = []
for root,members in groups.items():
    uniq = sorted(set(members))
    if len(uniq)>1:
        final_groups.append(uniq)

# write CSV
os.makedirs(OUT_CSV.parent, exist_ok=True)
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as cf:
    w = csv.writer(cf)
    w.writerow(['path','filename','declared_name','total_lines','nonempty_lines','token_count','unique_tokens','shingle_count','keywords','header_sample'])
    for r in rows:
        w.writerow([r['path'],r['filename'],r['declared_name'],r['total_lines'],r['nonempty_lines'],r['token_count'],r['unique_tokens'],r['shingle_count'],r['keywords'], r['header_sample']])

# write markdown groups
with open(OUT_MD, 'w', encoding='utf-8') as md:
    md.write('# Pine files grouping proposal\n\n')
    md.write(f'Analyzed {len(rows)} files. Similarity threshold={SIM_THRESHOLD} (shingle k={K_SHINGLE})\n\n')
    md.write('## Groups (connected by similarity)\n\n')
    gid = 0
    for grp in sorted(final_groups, key=lambda g: (-len(g), g)):
        gid += 1
        md.write(f'### Group {gid} (size={len(grp)})\n\n')
        # common keywords
        kwc = Counter()
        for f in grp:
            kwc.update(keywords_map.get(f, []))
        md.write('Common keywords: ' + ', '.join([f'{k}({v})' for k,v in kwc.most_common()]) + '\n\n')
        # write files with declared names
        for f in grp:
            dn = next((r['declared_name'] for r in rows if r['path']==f), '')
            header_sample = header_map.get(f, '')[:200].replace('\n', ' ')
            md.write(f'- {f}\n')
            md.write(f'  - declared: {dn}\n')
            md.write('  - header: ' + header_sample + '\n')
        md.write('\n')

    md.write('## Unclustered files (no similar neighbors above threshold)\n\n')
    clustered = set(x for g in final_groups for x in g)
    for r in rows:
        if r['path'] not in clustered:
            md.write(f'- {r["path"]} - declared: {r["declared_name"]} - keywords: {r["keywords"]}\n')

print('Wrote catalog and groups:')
print(' -', OUT_CSV)
print(' -', OUT_MD)
print('Done')
