#!/usr/bin/env python3
"""Extract the WOLD Dutch loanword subset as source-form -> adapted-form pairs.

Usage:
    python3 wold-dutch-extract.py <dir-with-wold-cldf-csvs> [language_id]

Expects lexibank/wold CLDF tables (v4.2) in <dir>:
    forms.csv  borrowings.csv  languages.csv  parameters.csv
Get them with e.g.
    for f in forms borrowings languages parameters; do
      curl -LO https://raw.githubusercontent.com/lexibank/wold/v4.2/cldf/$f.csv
    done

Writes two files to the cwd:
    wold-<lang>-forms.csv       every form for that recipient language
    wold-<lang>-loanpairs.csv   one row per (target form, donor etymon) link

Key facts about the shape of the data (checked 2026-08-24 against v4.2):
  * forms.csv    Language_ID selects the recipient language ('Dutch').
                 Form = orthography, Segments = space-separated IPA
                 (the whole database is segmented, so the ADAPTED side is
                 already in IPA).
                 Loan = 'true'/'false'; Borrowed = the 5-point WOLD scale.
  * borrowings.csv links Target_Form_ID (a forms.csv ID) to the donor etymon.
                 Source_Form_ID is EMPTY throughout the database, so the donor
                 side is only ever the *orthographic* string in Source_word
                 plus Source_languoid — there is NO IPA for the source form.
                 Source_relation is 'immediate' or 'earlier'.
"""
import csv, os, sys

d = sys.argv[1] if len(sys.argv) > 1 else '.'
lang = sys.argv[2] if len(sys.argv) > 2 else 'Dutch'
rd = lambda n: list(csv.DictReader(open(os.path.join(d, n), encoding='utf-8')))

forms = rd('forms.csv')
params = {p['ID']: p for p in rd('parameters.csv')}
mine = [f for f in forms if f['Language_ID'] == lang]
byid = {f['ID']: f for f in mine}

with open('wold-%s-forms.csv' % lang.lower(), 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(forms[0].keys()))
    w.writeheader()
    w.writerows(mine)

rows = []
for b in rd('borrowings.csv'):
    t = byid.get(b['Target_Form_ID'])
    if not t:
        continue
    rows.append(dict(
        target_form=t['Form'],
        target_ipa=t['Segments'],
        source_word=b['Source_word'],
        source_languoid=b['Source_languoid'],
        source_meaning=b['Source_meaning'],
        source_relation=b['Source_relation'],
        source_certain=b['Source_certain'],
        concept=params.get(t['Parameter_ID'], {}).get('Name', ''),
        age=t['Age'],
        borrowed=t['Borrowed'],
        form_id=t['ID'],
    ))
rows.sort(key=lambda r: (r['source_languoid'], r['target_form']))
with open('wold-%s-loanpairs.csv' % lang.lower(), 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter='\t')
    w.writeheader()
    w.writerows(rows)
print('%s: %d forms (%d flagged Loan=true), %d loan-pair rows'
      % (lang, len(mine), sum(1 for f in mine if f['Loan'] == 'true'), len(rows)))
