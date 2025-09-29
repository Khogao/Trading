"""Find near-duplicate .pine files under indicators/

Approach:
- Normalize Pine code: remove block comments (/* */), remove single-line comments (//), remove string literals,
  collapse non-alphanumeric to spaces and tokenize.
- Build k-token shingles (default k=5) per file and compute Jaccard similarity between shingle sets.
- Report pairs/groups with similarity >= threshold (default 0.80).
- Save a human-readable markdown report `docs/near_duplicates_report.md` and a CSV `docs/near_duplicates.csv`.

Usage:
  python scripts/find_near_duplicates.py --threshold 0.8 --shingle 5

This is an offline, deterministic, no-external-deps script intended for manual review guidance.
"""

import os
import re
import argparse
import csv
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IND = os.path.join(ROOT, 'indicators')
OUT_MD = os.path.join(ROOT, 'docs', 'near_duplicates_report.md')
OUT_CSV = os.path.join(ROOT, 'docs', 'near_duplicates.csv')

if not os.path.isdir(IND):
    print('indicators/ directory not found at', IND)
    raise SystemExit(1)

# normalization helpers
_block_comment_re = re.compile(r"/\*.*?\*/", re.DOTALL)
_line_comment_re = re.compile(r"//.*?$", re.MULTILINE)
_string_re = re.compile(r'(""".*?"""|".*?(?<!\\)"|\'.*?(?<!\\)\')', re.DOTALL)
_nonword_re = re.compile(r"[^0-9A-Za-z_]+")


def normalize_code(text):
    # remove block comments
    t = _block_comment_re.sub(' ', text)
    # remove single-line comments
    t = _line_comment_re.sub(' ', t)
    # remove string literals
    t = _string_re.sub(' ', t)
    # collapse non-word to space, lowercase
    t = _nonword_re.sub(' ', t).lower()
    # collapse whitespace
    t = ' '.join(t.split())
    return t


def tokens_from_text(text):
    if not text:
        return []
    return text.split()


def shingles_from_tokens(tokens, k):
    if len(tokens) < k:
        return set()
    shingles = set()
    for i in range(len(tokens) - k + 1):
        shingles.add(' '.join(tokens[i:i+k]))
    return shingles


def jaccard(a, b):
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    uni = len(a | b)
    return inter / uni if uni else 0.0


def is_archive(path):
    low = path.replace('\\','/').lower()
    return '/archive/' in low or '/z_archive/' in low


def choose_keeper(group):
    # selection heuristics similar to exact dedupe script
    non_archive = [p for p in group if not is_archive(p)]
    candidates = non_archive if non_archive else group
    preferred = [p for p in candidates if '/production/' in p.replace('\\','/').lower() or '/volume_profile/' in p.replace('\\','/').lower()]
    if preferred:
        keeper = sorted(preferred, key=lambda x: len(x))[0]
    else:
        keeper = sorted(candidates, key=lambda x: len(x))[0]
    return keeper


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--threshold', type=float, default=0.8, help='Jaccard similarity threshold (0..1)')
    p.add_argument('--shingle', type=int, default=5, help='Tokens per shingle')
    p.add_argument('--min-tokens', type=int, default=30, help='Skip files with fewer tokens than this')
    p.add_argument('--max-pairs', type=int, default=10000, help='Max pair comparisons to evaluate (safety)')
    args = p.parse_args()

    pine_files = []
    for dirpath, dirnames, filenames in os.walk(IND):
        for fn in filenames:
            if fn.lower().endswith('.pine'):
                pine_files.append(os.path.join(dirpath, fn))
    print(f'Found {len(pine_files)} .pine files under indicators/')

    data = {}
    tokens_map = {}
    shingles_map = {}

    for pth in pine_files:
        try:
            with open(pth, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
        except Exception as e:
            print('ERROR reading', pth, e)
            continue
        norm = normalize_code(txt)
        toks = tokens_from_text(norm)
        tokens_map[pth] = toks
        if len(toks) < args.min_tokens:
            shingles_map[pth] = set()
        else:
            shingles_map[pth] = shingles_from_tokens(toks, args.shingle)

    # pairwise compare
    files = list(shingles_map.keys())
    n = len(files)
    pairs = []
    checked = 0
    for i in range(n):
        for j in range(i+1, n):
            checked += 1
            if checked > args.max_pairs:
                print('Reached max pairs limit, stopping comparisons')
                break
            a = files[i]
            b = files[j]
            sa = shingles_map[a]
            sb = shingles_map[b]
            if not sa or not sb:
                continue
            sim = jaccard(sa, sb)
            if sim >= args.threshold:
                pairs.append((a, b, sim))
        if checked > args.max_pairs:
            break

    print(f'Found {len(pairs)} pairs with similarity >= {args.threshold}')

    # group pairs into connected components
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a,b):
        ra = find(a)
        rb = find(b)
        if ra != rb:
            parent[rb] = ra

    for a,b,_ in pairs:
        union(a,b)

    groups = defaultdict(list)
    for a,b,_ in pairs:
        root = find(a)
        groups[root].append(a)
        groups[root].append(b)

    # deduplicate entries per group
    final_groups = []
    for root, members in groups.items():
        uniq = sorted(set(members))
        if len(uniq) > 1:
            final_groups.append(uniq)

    print(f'Connected groups found: {len(final_groups)}')

    # write reports
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, 'w', encoding='utf-8') as md, open(OUT_CSV, 'w', newline='', encoding='utf-8') as csvf:
        md.write('# Near-duplicate report\n\n')
        md.write(f'Threshold: {args.threshold}, shingle: {args.shingle}, min_tokens: {args.min_tokens}\n\n')
        w = csv.writer(csvf)
        w.writerow(['group_id','file','keeper','notes'])
        gid = 0
        for grp in sorted(final_groups, key=lambda g: (len(g), g), reverse=True):
            gid += 1
            md.write(f'## Group {gid} (size={len(grp)})\n\n')
            keeper = choose_keeper(grp)
            for fpath in grp:
                note = 'KEEP' if fpath == keeper else ''
                md.write(f'- {fpath} {note}\n')
                w.writerow([gid, fpath, 'YES' if fpath==keeper else 'NO', note])
            md.write('\n')

        # also write pair-level CSV for review
        w.writerow([])
        w.writerow(['file_a','file_b','similarity'])
        for a,b,sim in sorted(pairs, key=lambda x: -x[2]):
            w.writerow([a,b,f'{sim:.4f}'])

    print('\nWrote report:', OUT_MD)
    print('Wrote CSV:', OUT_CSV)
    print('\nDone.')


if __name__ == '__main__':
    main()
