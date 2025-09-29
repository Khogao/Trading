"""Regroup pine indicators by core logic: VSA, VP, PA, Composite, Other.

Reads docs/pine_catalog.csv and assigns each file to one of the groups based on keywords and header/declaration.
Writes docs/pine_groups_by_corelogic.md
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / 'docs' / 'pine_catalog.csv'
OUT = ROOT / 'docs' / 'pine_groups_by_corelogic.md'

if not CAT.exists():
    print('Catalog not found:', CAT)
    raise SystemExit(1)

# heuristics
vp_terms = ['vpp','vp','value-area','valuearea','value area','volume_profile','volume profile','volume_profile','vpp_v4','vpp_v4_2','vpp_v4_0','valuearea','vpp4','vpp42','vpp5','vpp-']
vsa_terms = ['vsa','vsa-','vsa_','vsa ']  # simple
pa_terms = ['wyckoff','pa','price action','price-action','priceaction','price','supply','demand','liquidity','structure','orderflow','order_flow']

groups = {'VSA':[], 'VP':[], 'PA':[], 'COMPOSITE':[], 'OTHER':[]}

with CAT.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        path = row['path']
        declared = (row.get('declared_name') or '').lower()
        keywords = (row.get('keywords') or '').lower()
        header = (row.get('header_sample') or '').lower()
        text = ' '.join([declared, keywords, header])
        is_vp = any(t in text for t in vp_terms)
        is_vsa = any(t in text for t in vsa_terms)
        is_pa = any(t in text for t in pa_terms)
        flags = [is_vp, is_vsa, is_pa]
        n = sum(1 for v in flags if v)
        if n >= 2:
            groups['COMPOSITE'].append((path, declared, keywords))
        elif is_vp:
            groups['VP'].append((path, declared, keywords))
        elif is_vsa:
            groups['VSA'].append((path, declared, keywords))
        elif is_pa:
            groups['PA'].append((path, declared, keywords))
        else:
            groups['OTHER'].append((path, declared, keywords))

# write markdown
with OUT.open('w', encoding='utf-8') as md:
    md.write('# Pine grouping by core logic\n\n')
    md.write('Rules: assign to VSA if indicators contain VSA-related keywords; VP for volume-profile/value-area related; PA for price-action/Wyckoff/structure; COMPOSITE if multiple categories match; OTHER otherwise.\n\n')
    for g in ['VSA','VP','PA','COMPOSITE','OTHER']:
        md.write(f'## {g} ({len(groups[g])} files)\n\n')
        for p,decl,kw in groups[g]:
            md.write(f'- {p}\n')
            if decl or kw:
                md.write(f'  - declared: {decl}\n')
                md.write(f'  - keywords: {kw}\n')
        md.write('\n')

print('Wrote', OUT)
