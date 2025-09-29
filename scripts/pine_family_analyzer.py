"""
Pine family analyzer
- Walks the Trading tree for .pine files
- For each file computes:
  - sha256 hash
  - token set and token counts
  - difflib ratio vs others
- Produces:
  - docs/pine_family_report.csv (per-file stats)
  - docs/pine_family_groups.json (clusters/groups with members and similarity)

Usage: python scripts/pine_family_analyzer.py --root "d:/Work/Coding/Trading"
"""
import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]+")


def sha256_of_text(t: str) -> str:
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def tokenize(text: str):
    # Remove comment-like lines that start with // or //-style or block comments; keep content but tokenize
    # For simplicity, strip strings in quotes to avoid huge tokens
    # We'll just extract identifier-like tokens
    tokens = TOKEN_RE.findall(text)
    tokens = [t.lower() for t in tokens]
    return tokens


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    uni = len(a | b)
    return inter / uni if uni else 0.0


def sequence_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def main(root):
    root = os.path.abspath(root)
    docs = os.path.join(root, 'docs')
    os.makedirs(docs, exist_ok=True)

    pine_files = []
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith('.pine'):
                pine_files.append(os.path.join(dirpath, fn))
    pine_files.sort()

    entries = []
    hashes = {}
    texts = {}
    token_sets = {}
    token_counts = {}

    for p in pine_files:
        try:
            with open(p, 'r', encoding='utf-8', errors='replace') as fh:
                text = fh.read()
        except Exception as e:
            print(f"Failed to read {p}: {e}")
            text = ''
        texts[p] = text
        h = sha256_of_text(text)
        hashes[p] = h
        tokens = tokenize(text)
        token_counts[p] = Counter(tokens)
        token_sets[p] = set(token_counts[p].keys())
        entries.append({
            'path': p,
            'sha256': h,
            'size_bytes': len(text.encode('utf-8')),
            'num_lines': text.count('\n') + 1 if text else 0,
            'token_count': sum(token_counts[p].values()),
            'unique_tokens': len(token_sets[p]),
            'top_tokens': ','.join([t for t, _ in token_counts[p].most_common(10)])
        })

    # Pairwise similarities
    n = len(pine_files)
    sims = []
    for i in range(n):
        p1 = pine_files[i]
        for j in range(i + 1, n):
            p2 = pine_files[j]
            # quick exact duplicate
            if hashes[p1] == hashes[p2]:
                sims.append((p1, p2, 1.0, 1.0))
                continue
            # compute jaccard on token sets
            jacc = jaccard(token_sets[p1], token_sets[p2])
            # compute sequence ratio on normalized text (strip whitespace)
            r = sequence_ratio(re.sub(r"\s+", " ", texts[p1]), re.sub(r"\s+", " ", texts[p2]))
            sims.append((p1, p2, jacc, r))

    # Build groups: exact duplicates grouped first, then near-duplicates by jaccard>0.85 or seq>0.9
    groups = []
    assigned = set()
    # exact duplicates
    hash_groups = defaultdict(list)
    for p, h in hashes.items():
        hash_groups[h].append(p)
    for h, members in hash_groups.items():
        if len(members) > 1:
            gid = f"dup-{h[:8]}"
            groups.append({'group_id': gid, 'type': 'exact_duplicates', 'members': members})
            assigned.update(members)

    # near duplicates
    NEAR_JACCARD = 0.80
    NEAR_SEQ = 0.88
    # cluster remaining by greedy approach
    remaining = [p for p in pine_files if p not in assigned]
    for p in remaining:
        if p in assigned:
            continue
        cluster = [p]
        assigned.add(p)
        for q in remaining:
            if q in assigned:
                continue
            # lookup sim
            # find tuple in sims (i<j)... faster to compute on the fly
            jacc = jaccard(token_sets[p], token_sets[q])
            seq = sequence_ratio(re.sub(r"\s+", " ", texts[p]), re.sub(r"\s+", " ", texts[q]))
            if jacc >= NEAR_JACCARD or seq >= NEAR_SEQ:
                cluster.append(q)
                assigned.add(q)
        if len(cluster) > 1:
            groups.append({'group_id': f"near-{hashlib.sha1(p.encode()).hexdigest()[:8]}", 'type': 'near_duplicates', 'members': cluster})

    # Output per-file CSV
    import csv
    csv_path = os.path.join(docs, 'pine_family_report.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=['path','sha256','size_bytes','num_lines','token_count','unique_tokens','top_tokens'])
        writer.writeheader()
        for e in entries:
            writer.writerow(e)

    json_path = os.path.join(docs, 'pine_family_groups.json')
    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump({'groups': groups, 'pairwise_count': len(sims)}, jf, indent=2)

    print(f"Wrote per-file report to {csv_path}")
    print(f"Wrote groups summary to {json_path}")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.path.join(os.path.dirname(__file__), '..'))
    args = ap.parse_args()
    main(args.root)
