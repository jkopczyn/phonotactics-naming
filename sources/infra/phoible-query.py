#!/usr/bin/env python3
"""Query PHOIBLE 2.0 from the CLDF release — plain csv, no pycldf needed.

The repo already has a starter extract at
    ../../chat-imports/phoible_inventories_starter.csv
(long format: one row per segment per inventory, 38 PHOIBLE features).
This script is the recipe for regenerating or extending it.

Get the data (StructureDataset; ~10 MB):
    for f in values inventories languages parameters; do
      curl -LO https://raw.githubusercontent.com/cldf-datasets/phoible/v2.0.1/cldf/$f.csv
    done
CLDF tables (v2.0.1):
    languages.csv    ID = Glottocode, Name, ISO639P3code
    inventories.csv  ID (= PHOIBLE InventoryID), Name, Contribution_ID, Source
    parameters.csv   ID, Name = the segment (IPA), plus the 37 feature columns
    values.csv       one row per segment-in-inventory:
                     ID, Language_ID (glottocode), Parameter_ID, Value (the
                     segment), Contribution_ID (= InventoryID), Marginal,
                     Allophones, Source

The inventories pinned for this project (see notes/project-goals.md):
    231  Egyptian Arabic (UPSID)   2406 Southern Welsh (Llanwrtyd)
    2169 Dutch (Belgian Standard)  2183 Georgian (Standard/literary)

Usage:  python3 phoible-query.py <dir-with-phoible-cldf-csvs> 231 2406 2169 2183
Writes phoible-selected.csv (segment + all features, long format) to cwd.
"""
import csv, os, sys

d = sys.argv[1]
want = set(sys.argv[2:]) or {'231', '2406', '2169', '2183'}
rd = lambda n: list(csv.DictReader(open(os.path.join(d, n), encoding='utf-8')))

params = {p['ID']: p for p in rd('parameters.csv')}
invs = {i['ID']: i for i in rd('inventories.csv')}
langs = {l['ID']: l for l in rd('languages.csv')}

feat_cols = [c for c in next(iter(params.values())) if c not in ('ID', 'Name', 'Description')]
out = []
for v in rd('values.csv'):
    if v['Contribution_ID'] not in want:
        continue
    p = params.get(v['Parameter_ID'], {})
    row = {
        'InventoryID': v['Contribution_ID'],
        'InventoryName': invs.get(v['Contribution_ID'], {}).get('Name', ''),
        'Glottocode': v['Language_ID'],
        'LanguageName': langs.get(v['Language_ID'], {}).get('Name', ''),
        'Segment': v['Value'],
        'Marginal': v['Marginal'],
        'Allophones': v['Allophones'],
    }
    row.update({c: p.get(c, '') for c in feat_cols})
    out.append(row)

with open('phoible-selected.csv', 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)
print('%d segment rows for inventories %s' % (len(out), sorted(want)))
