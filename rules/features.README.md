# rules/features.tsv — provenance

Built by `rules/build_features.py` from `chat-imports/phoible_inventories_starter.csv` (PHOIBLE
half, `source = phoible:<InventoryID>`) plus hand rows added in Task 1b (`source = hand:...`).
Rebuild the PHOIBLE half with:

    uv run python rules/build_features.py chat-imports/phoible_inventories_starter.csv rules/features.tsv

Re-sort a table that already contains hand rows (no re-import):

    uv run python rules/build_features.py --sort-only rules/features.tsv rules/features.tsv

Columns: `segment  class  source` + the 38 PHOIBLE features in PHOIBLE order. `class` is `C`
for `SegmentClass=consonant`, `V` for `vowel`. Rows are sorted by (`class`, segment code
points) so rebuilds are byte-identical. The build is test-covered by
`tests/test_features_phoible.py`, including a byte-stability check.

## Input facts (asserted by the script — it fails if the CSV changes)

- 153 data rows, 91 distinct `Phoneme` spellings, 4 inventories: Belgian Dutch 2169, Cairene
  Arabic 231, Georgian 2183, Southern Welsh 2406.
- No identically-spelled phoneme has different feature vectors across inventories.

## Normalization map (plan I-34, spec §12.F)

The dental `◌̪` (U+032A) and retracted `◌̠` (U+0320) combining marks are stripped so the table
uses the digests' spellings. Exactly 15 spellings change:

    d̠ʒ→dʒ  d̪→d  d̪ˤ→dˤ  l̪→l  n̪→n  s̪→s  s̪ˤ→sˤ  t̪→t  t̪ˤ→tˤ  z̪→z  z̪ˤ→zˤ
    t̠ʃ→tʃ  t̠ʃʼ→tʃʼ  t̪ʰ→tʰ  t̪ʼ→tʼ

Strings are NFC-normalized first (I-1); no spelling in the CSV changes under NFC.

## Collisions (7) and the discarded vectors

Where the stripped spelling already existed as a PHOIBLE spelling, the row that was already
canonical is kept and the dental row is discarded. Every discarded vector differs from the kept
one only in `distributed` (dental `+` vs alveolar `-`).

| canonical | kept row (inventory) | discarded PHOIBLE row (inventory) | difference | discarded vector (38 PHOIBLE features, in header order) |
|---|---|---|---|---|
| `d` | `d` (Dutch, 2169) | `d̪` (Egyptian Arabic (Cairene), 231) | `distributed` +→- | `0 - - - - + - - - - - - - - - 0 0 + + + - - 0 0 0 0 0 - - + - - - - - - - -` |
| `l` | `l` (Dutch, 2169) | `l̪` (Egyptian Arabic (Cairene), 231) | `distributed` +→- | `0 - - - - + + + 0 + - - - + - 0 0 + + + - - 0 0 0 0 0 - - + - - - - - - - -` |
| `n` | `n` (Dutch, 2169) | `n̪` (Egyptian Arabic (Cairene), 231) | `distributed` +→- | `0 - - - - + + - 0 - - - + - - 0 0 + + + - - 0 0 0 0 0 - - + - - - - - - - -` |
| `s` | `s` (Dutch, 2169) | `s̪` (Egyptian Arabic (Cairene), 231) | `distributed` +→- | `0 - - - - + - + + - - - - - - 0 0 + + + + - 0 0 0 0 0 - - - - - - - - - - -` |
| `t` | `t` (Dutch, 2169) | `t̪` (Egyptian Arabic (Cairene), 231) | `distributed` +→- | `0 - - - - + - - - - - - - - - 0 0 + + + - - 0 0 0 0 0 - - - - - - - - - - -` |
| `z` | `z` (Dutch, 2169) | `z̪` (Egyptian Arabic (Cairene), 231) | `distributed` +→- | `0 - - - - + - + + - - - - - - 0 0 + + + + - 0 0 0 0 0 - - + - - - - - - - -` |
| `tʰ` | `tʰ` (Welsh (Southern), 2406) | `t̪ʰ` (Georgian, 2183) | `distributed` +→- | `0 - - - - + - - - - - - - - - 0 0 + + + - - 0 0 0 0 0 - - - - + - - - - - -` |

## Contour values

PHOIBLE writes some features as onset/offglide pairs (`-,+`). After the diphthongs are dropped
the only remaining ones are `retractedTongueRoot = -,+` on the four Cairene pharyngealized
consonants `dˤ sˤ tˤ zˤ`. The script resolves these to `+`: the whole segment is
pharyngealized, and it is the sole feature separating `sˤ` from `s` (`-` would make the
two rows identical). Any other contour value aborts the build. *(Not anticipated by the plan's
Task 1a "verified facts"; flagged in the Task 1a report.)*

## Dropped rows (plan I-2, I-35)

The 11 PHOIBLE diphthong rows are not imported; diphthongs are two segments grouped into one
nucleus by each rule file's `[syllable] nuclei` line:

    ai au ɔi əi əu ɛu ɪu ʊi œy ɔu ɛi

## Row count

91 spellings − 15 renamed with 7 collisions = 84 segments − 11 diphthongs = **73 PHOIBLE rows**
(54 consonants, 19 vowels).
