# attested.csv format

Comma-separated (RFC 4180), UTF-8, one attested adaptation per line, header row:

    source_lang,source_form,source_ipa,target_form,target_ipa,process,provenance,note

An optional ninth column `layer` (`historical` | `modern` | `translit`; welsh only so far) tags
the period of the evidence; readers ignore columns they do not know.

- `source_lang` — ISO 639-3 of the donor (eng, fra, rus, gle, …).
- `source_form` — donor orthography as given in the source document.
- `source_ipa` — donor pronunciation in IPA if the source gives it; else leave blank (do not
  invent).
- `target_form` — adapted form in the target's own orthography/transliteration as given.
- `target_ipa` — adapted form in IPA if the source gives it; else blank.
- `process` — semicolon-separated tags from: `epenthesis`, `deletion`, `substitution`,
  `devoicing`, `gemination`, `glide`, `metathesis`, `length`, `stress`, `vowel`, `none`.
- `provenance` — bib.md key + page, e.g. `ema1958 p.4`, `wold`, `wiki-cy §Loanwords`,
  `ga-wiki-transliteration`.
- `note` — free text, short.

Minimum 30 rows per target language; more is better. Prefer rows where the source document
states the pronunciation of both sides. Rows from transliteration practice (Wikipedia
renderings of foreign names) are acceptable but must be tagged as such in `provenance`, since
they reflect an English-mediated pronunciation and editorial convention rather than speech.
