"""Archive .pine files under indicators/ older than a given number of days.

Behavior:
- Default threshold: 30 days (files last modified before now - 30 days are archived).
- For each file matched:
  - create a backup copy at the original path with suffix `.archive.bak` (preserve metadata)
  - move the original file to `indicators/archive/<relative path>` (creating directories as needed)
  - if target exists, append a numeric suffix to avoid overwrite
- Print a report and exit with non-zero code on fatal errors.

Usage:
  python scripts/archive_old_pine.py --days 30
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
IND = ROOT / 'indicators'
ARCH = IND / 'archive'

p = argparse.ArgumentParser()
p.add_argument('--days', type=int, default=30, help='Archive files older than this many days')
args = p.parse_args()

if not IND.exists():
    print('indicators/ not found at', IND)
    raise SystemExit(1)

threshold = datetime.now().timestamp() - args.days * 24 * 3600

to_archive = []
for pth in IND.rglob('*.pine'):
    try:
        mtime = pth.stat().st_mtime
    except Exception as e:
        print('ERR stat', pth, e)
        continue
    # skip files already inside indicators/archive
    if 'indicators' + os.sep + 'archive' in str(pth).replace('/', os.sep):
        continue
    if mtime < threshold:
        to_archive.append(pth)

print(f'Found {len(to_archive)} .pine files older than {args.days} days')

moved = []
errors = []
for old in to_archive:
    rel = old.relative_to(IND)
    target = ARCH / rel
    target_parent = target.parent
    try:
        target_parent.mkdir(parents=True, exist_ok=True)
        # create backup at original location
        bak = old.with_suffix(old.suffix + '.archive.bak')
        if not bak.exists():
            shutil.copy2(old, bak)
            print('Backed up', old, '->', bak)
        else:
            print('Backup exists', bak)
        # avoid overwrite at target
        base_target = target
        i = 1
        while target.exists():
            target = base_target.with_name(base_target.stem + f'-{i}' + base_target.suffix)
            i += 1
        shutil.move(str(old), str(target))
        moved.append((old, target))
        print('Moved', old, '->', target)
    except Exception as e:
        print('ERROR archiving', old, e)
        errors.append((old,e))

print('\nSummary:')
print('Archived:', len(moved))
if moved:
    for o,t in moved:
        print(' -', o, '->', t)
if errors:
    print('\nErrors:')
    for o,e in errors:
        print(' -', o, e)

print('\nDone')
