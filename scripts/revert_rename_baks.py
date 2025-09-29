"""Revert renames made by rename_by_description.py by restoring all *.rename.bak files to their original filenames.

This will:
- For each file matching '**/*.rename.bak', compute original_path = bak_path with '.rename.bak' removed.
- If original_path exists (it may be the incorrectly renamed file), remove it, then move bak -> original_path.
- Print summary.

Use with caution: this undoes the earlier renames performed by the script.
"""

import sys
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
count = 0
restored = []
errors = []
for bak in ROOT.rglob('*.rename.bak'):
    orig = Path(str(bak)[:-len('.rename.bak')])
    try:
        # remove existing orig if present
        if orig.exists():
            # ensure it's not the same file
            try:
                orig.unlink()
            except Exception as e:
                errors.append((bak, orig, str(e)))
                continue
        bak.rename(orig)
        restored.append((bak, orig))
        count += 1
    except Exception as e:
        errors.append((bak, orig, str(e)))

print(f'Restored {count} files from .rename.bak')
if errors:
    print('Errors:')
    for b,o,e in errors:
        print(b, '->', o, 'ERROR', e)
else:
    print('No errors')

if __name__ == '__main__':
    sys.exit(0)
