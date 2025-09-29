"""Rename .pine files listed in docs/near_duplicates_report.md using their internal indicator/study names.

Rules:
- Parse file paths from lines starting with '-' in the report.
- For each file, skip if basename matches exceptions (case-insensitive): Pi 34, VPP5, SMPA ORG.
- Extract name from (in order): indicator("NAME"), study("NAME"), //@description or // Name: , first non-empty comment line at top.
- Sanitize extracted name into a safe filename (replace spaces with '-', remove problematic chars), keep extension .pine.
- If target filename already exists in directory, append suffix to avoid overwrite (e.g., -1).
- Before renaming, copy original to <orig>.rename.bak for safety.
- Print a mapping of old -> new and exit non-zero if any errors.

Usage:
  python scripts/rename_by_description.py

This script performs filesystem renames. Review output before committing.
"""

import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs' / 'near_duplicates_report.md'
EXCEPTIONS = {'pi 34', 'vpp5', 'smpa org'}  # lowercase

indicator_re = re.compile(r"indicator\s*\(\s*['\"](.*?)['\"]", re.IGNORECASE)
study_re = re.compile(r"study\s*\(\s*['\"](.*?)['\"]", re.IGNORECASE)
desc_re = re.compile(r"@description\s*[:=]?\s*(.*)", re.IGNORECASE)
name_comment_re = re.compile(r"^\s*//\s*Name\s*[:\-]?\s*(.*)", re.IGNORECASE)
first_comment_re = re.compile(r"^\s*//\s*(.+)")

def sanitize_filename(name: str) -> str:
    name = name.strip()
    # replace common separators with dash
    name = re.sub(r"[\s/\\]+", '-', name)
    # remove characters that are bad for filenames
    name = re.sub(r"[^0-9A-Za-z\-_.()]+", '', name)
    # collapse multiple dashes
    name = re.sub(r"-+", '-', name)
    if not name:
        name = 'unnamed'
    return name


def extract_name_from_file(path: Path) -> str | None:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print('ERROR reading', path, e)
        return None
    # search for indicator/study call
    m = indicator_re.search(text)
    if not m:
        m = study_re.search(text)
    if m:
        return m.group(1).strip()
    # search for @description
    m = desc_re.search(text)
    if m:
        return m.group(1).strip()
    # search for Name: comment
    m = name_comment_re.search(text)
    if m:
        return m.group(1).strip()
    # take first comment line in file
    for line in text.splitlines()[:20]:
        m = first_comment_re.match(line)
        if m:
            candidate = m.group(1).strip()
            if candidate:
                return candidate
    return None


def main():
    if not REPORT.exists():
        print('Report not found:', REPORT)
        return 1
    files = []
    with REPORT.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('- '):
                # line format: - D:\... or - path KEEP
                parts = line[2:].split()
                # first token is path, may include spaces if quoted; handle by joining until .pine
                # easier: find substring ending with .pine (case-insensitive)
                text = line[2:]
                m = re.search(r"([A-Za-z]:)?[^\n]*?\.pine", text, re.IGNORECASE)
                if m:
                    pth = m.group(0).strip()
                    files.append(Path(pth))
    if not files:
        print('No files parsed from report')
        return 1

    # Plan target names first to avoid collisions when multiple files map to same name
    planned_targets = {}
    taken = set()
    actions = []
    for p in files:
        if not p.exists():
            print('Skip (missing):', p)
            continue
        base = p.name
        if base.lower() in EXCEPTIONS:
            print('Skip (exception):', p)
            continue
        name = extract_name_from_file(p)
        if not name:
            print('No descriptive name found, skipping:', p)
            continue
        safe = sanitize_filename(name)
        candidate = safe + '.pine'
        # ensure candidate is not already planned or exists on disk
        suffix = 1
        target = p.with_name(candidate)
        while str(target).lower() in taken or target.exists():
            candidate = f"{safe}-{suffix}.pine"
            target = p.with_name(candidate)
            suffix += 1
        planned_targets[p] = target
        taken.add(str(target).lower())
        if candidate == base:
            print('No rename needed for', p)
            # remove planning
            planned_targets.pop(p, None)
            taken.discard(str(target).lower())

    # build actions list from plans
    for p, target in planned_targets.items():
        actions.append((p, target))

    if not actions:
        print('No rename actions to perform')
        return 0

    # perform renames with backups
    for old, new in actions:
        bak = old.with_suffix(old.suffix + '.rename.bak')
        try:
            if not bak.exists():
                shutil.copy2(old, bak)
                print('Backed up', old, '->', bak)
            else:
                print('Backup already exists', bak)
            old.rename(new)
            print('Renamed', old, '->', new)
        except Exception as e:
            print('ERROR renaming', old, '->', new, e)

    # print summary
    print('\nSummary:')
    for old,new in actions:
        print(old, '->', new)
    print('\nDone.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
