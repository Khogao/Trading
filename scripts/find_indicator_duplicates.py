"""Find and remove exact duplicate .pine files under indicators/

Rules:
- Exact duplicate = identical file bytes (SHA256 hash).
- Keep one canonical file per group. Selection priority:
  1) Prefer paths that do NOT contain '/archive/' or '/z_archive/'.
  2) Prefer files under 'production' or 'volume_profile'.
  3) Otherwise pick the file with shortest path length.
- For each duplicate file to be removed: create a .bak copy next to it, then delete the original.

Usage:
  python scripts/find_indicator_duplicates.py

This script prints a report of duplicates and actions taken.
"""

import os
import hashlib
import shutil
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IND = os.path.join(ROOT, 'indicators')

if not os.path.isdir(IND):
    print('indicators/ directory not found at', IND)
    raise SystemExit(1)

# collect .pine files
pine_files = []
for dirpath, dirnames, filenames in os.walk(IND):
    for fn in filenames:
        if fn.lower().endswith('.pine'):
            pine_files.append(os.path.join(dirpath, fn))

print(f'Found {len(pine_files)} .pine files under indicators/')

# compute hashes
hash_map = defaultdict(list)
for p in pine_files:
    try:
        with open(p, 'rb') as f:
            data = f.read()
    except Exception as e:
        print('ERROR reading', p, e)
        continue
    h = hashlib.sha256(data).hexdigest()
    hash_map[h].append(p)

# find duplicate groups
dup_groups = [v for v in hash_map.values() if len(v) > 1]
print(f'Found {len(dup_groups)} groups of exact duplicates')

removed = []
backed = []

def is_archive(path):
    low = path.replace('\\','/').lower()
    return '/archive/' in low or '/z_archive/' in low

for group in dup_groups:
    # pick keeper
    non_archive = [p for p in group if not is_archive(p)]
    candidates = non_archive if non_archive else group
    # prefer production or volume_profile
    preferred = [p for p in candidates if '/production/' in p.replace('\\','/').lower() or '/volume_profile/' in p.replace('\\','/').lower()]
    if preferred:
        keeper = sorted(preferred, key=lambda x: len(x))[0]
    else:
        keeper = sorted(candidates, key=lambda x: len(x))[0]

    to_remove = [p for p in group if p != keeper]

    print('\nDuplicate group:')
    for p in group:
        mark = '(KEEP)' if p == keeper else ''
        print('  ', p, mark)

    # backup & remove duplicates
    for p in to_remove:
        bak = p + '.bak'
        try:
            if not os.path.exists(bak):
                shutil.copy2(p, bak)
                backed.append(bak)
                print('   Backed up ->', bak)
            else:
                print('   Backup already exists ->', bak)
            os.remove(p)
            removed.append(p)
            print('   Removed ->', p)
        except Exception as e:
            print('   ERROR handling', p, e)

# final report
print('\nSummary:')
print('Backed up', len(backed), 'files')
print('Removed', len(removed), 'duplicate files')

if removed:
    print('\nRemoved files:')
    for r in removed:
        print('  ', r)

if backed:
    print('\nBackup files:')
    for b in backed:
        print('  ', b)

print('\nDone.')
