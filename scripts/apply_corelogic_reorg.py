"""Apply core-logic reorganization: move and rename .pine files according to core logic grouping and declared description.

Rules:
- Read docs/pine_catalog.csv to determine grouping (VSA/VP/PA/COMPOSITE/OTHER) using the same heuristics as regroup_by_corelogic.py.
- Destination folders (use existing tree where possible):
  * VSA -> indicators/vsa
  * VP  -> indicators/vp
  * PA  -> indicators/wyckoff
  * COMPOSITE -> indicators/composite
  * OTHER -> leave in place
- For files moved: rename to sanitized declared name (from indicator/study/@description or header comment); if no declared name, keep original filename.
- Skip renaming/moving for explicit exceptions: Pi 34, VPP5, SMPA ORG (case-insensitive basenames).
- For safety: create a backup copy at original location with suffix `.apply.bak` before any move.
- Avoid overwriting by appending numeric suffix when target exists.
- Operate on working tree (no git ops inside script).

Usage:
  python scripts/apply_corelogic_reorg.py --dry-run   # show actions
  python scripts/apply_corelogic_reorg.py            # perform changes
"""

import csv
import re
import shutil
import argparse
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / 'docs' / 'pine_catalog.csv'
IND = ROOT / 'indicators'

EXCEPTIONS = {'pi 34.pine', 'vpp5.pine', 'smpa org.pine'}

# destination mapping
DEST = {
    'VSA': IND / 'vsa',
    'VP': IND / 'vp',
    'PA': IND / 'wyckoff',
    'COMPOSITE': IND / 'composite'
}

# heuristics (same as regroup_by_corelogic)
vp_terms = ['vpp','vp','value-area','valuearea','value area','volume_profile','volume profile','vpp_v4','vpp_v4_2','vpp_v4_0','vpp4','vpp42','vpp5','vpp-']
vsa_terms = ['vsa','vsa-','vsa_','vsa ']
pa_terms = ['wyckoff','pa','price action','price-action','priceaction','price','supply','demand','liquidity','structure','orderflow','order_flow']

indicator_re = re.compile(r"indicator\s*\(\s*['\"](.*?)['\"]", re.IGNORECASE)
study_re = re.compile(r"study\s*\(\s*['\"](.*?)['\"]", re.IGNORECASE)
desc_re = re.compile(r"@description\s*[:=]?\s*(.*)", re.IGNORECASE)
comment_re = re.compile(r"^\s*//\s*(.*)")


def sanitize(name: str) -> str:
    s = name.strip()
    s = re.sub(r"[\s/\\]+", '-', s)
    s = re.sub(r"[^0-9A-Za-z\-_.()]+", '', s)
    s = re.sub(r"-+", '-', s)
    if not s:
        s = 'unnamed'
    return s


def extract_declared(p: Path) -> str | None:
    try:
        txt = p.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None
    m = indicator_re.search(txt) or study_re.search(txt)
    if m:
        return m.group(1).strip()
    m = desc_re.search(txt)
    if m:
        return m.group(1).strip()
    # first comment line
    for L in txt.splitlines()[:40]:
        cm = comment_re.match(L)
        if cm:
            c = cm.group(1).strip()
            if c:
                return c
    return None


def decide_group(row):
    declared = (row.get('declared_name') or '').lower()
    keywords = (row.get('keywords') or '').lower()
    header = (row.get('header_sample') or '').lower()
    text = ' '.join([declared, keywords, header])
    is_vp = any(t in text for t in vp_terms)
    is_vsa = any(t in text for t in vsa_terms)
    is_pa = any(t in text for t in pa_terms)
    n = sum([is_vp, is_vsa, is_pa])
    if n >= 2:
        return 'COMPOSITE'
    if is_vp:
        return 'VP'
    if is_vsa:
        return 'VSA'
    if is_pa:
        return 'PA'
    return 'OTHER'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    if not CAT.exists():
        print('Catalog missing:', CAT)
        return 1

    rows = []
    with CAT.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    actions = []
    planned_targets = set()
    for r in rows:
        path = Path(r['path'])
        if not path.exists():
            continue
        basename = path.name.lower()
        if basename in EXCEPTIONS:
            # preserve exact file per user request
            print('Skip exception:', path)
            continue
        grp = decide_group(r)
        if grp == 'OTHER':
            # leave in place
            continue
        dest_dir = DEST.get(grp)
        if not dest_dir:
            continue
        # determine declared name
        declared = r.get('declared_name') or ''
        if not declared:
            declared = extract_declared(path) or ''
        if declared:
            newbase = sanitize(declared) + '.pine'
        else:
            newbase = path.name
        # prepare target
        target = dest_dir / newbase
        # ensure dest_dir exists
        base_target = target
        suffix = 1
        # avoid overwrite by adding suffix; check both filesystem and planned targets
        while target.exists() or str(target).lower() in planned_targets:
            target = base_target.with_name(f"{base_target.stem}-{suffix}{base_target.suffix}")
            suffix += 1
        planned_targets.add(str(target).lower())
        actions.append((path, target))

    if not actions:
        print('No actions to perform')
        return 0

    print(f'Planned {len(actions)} moves:')
    for a,b in actions:
        print(' -', a, '->', b)

    if args.dry_run:
        return 0

    # perform actions with backups
    for old, new in actions:
        try:
            new.parent.mkdir(parents=True, exist_ok=True)
            bak = old.with_suffix(old.suffix + '.apply.bak')
            if not bak.exists():
                shutil.copy2(old, bak)
            shutil.move(str(old), str(new))
            print('Moved', old, '->', new)
        except Exception as e:
            print('ERROR', old, e)

    print('Done')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
