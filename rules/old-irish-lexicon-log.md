# Old Irish lexicon — harvest log

Companion to `rules/old-irish-lexicon.tsv`. Built 2026-08-27 for strand 5
(`docs/specs/2026-08-27-old-irish-design.md` §3). Harvested by six parallel sourcing agents
(names, common nouns, adjectives/numerals/prefixes, wider given names, formation elements +
paradigm words, gap-fill) plus a digest-sourced batch taken directly from
`sources/irish/digest.md` §10.5–§10.6.

## Counts

| | rows |
|---|---|
| `attested` | 270 |
| `none` (loan / post-Old-Irish coinage) | 29 |
| **total rows in the file** | **299** |
| unresolved (harvested, no row written) | 49 |

Of the 270 attested rows, 163 carry an attested genitive and
107 have `oi_gen` blank. A blank genitive is always explained in `note` — either
"genitive unattested in sources consulted", or because the row is an adjective, numeral,
prefix or indeclinable, for which a genitive singular is not the relevant form.

Stem-class distribution: `o` 92, `(blank)` 91, `irregular` 37, `ā` 30, `n` 16, `i` 16, `u` 13, `dental` 4.

Gender distribution: `m` 114, `(blank)` 96, `f` 63, `n` 26.

## Sources used (citations per source)

| source | citations |
|---|---|
| en.wiktionary.org (Old Irish entries + Irish etymology sections) | 311 |
| sources/irish/digest.md §10.5–§10.6 | 28 |
| en.wikipedia.org (name / dynasty / mythology articles) | 23 |
| strachan1909-oldirish-paradigms (via the digest) | 3 |

Every row carries at least one citation; 27 rows carry two. No paywalled or login-gated
source was used; eDIL was not scraped. `digest §10.n` citations are the local digest, which
in turn cites `strachan1909-oldirish-paradigms` and `wiki-old-irish*` — they are the only
citations in the file that a web re-check cannot follow.

## Test-word coverage

The 144 test-word rows in `sources/irish/test-words.tsv` reduce to 138 distinct orthography
keys. Against the lexicon:

- **74 match a lexicon row directly.**
- **52 are mutated, inflected or phrasal surface forms** whose citation form is in the
  lexicon (see the mapping below). These are *not* given rows of their own: per spec §2 the
  lookup stage matches the row's citation form, and the Irish pre-pass has already applied the
  mutation/inflection on the modern side. **This is a lookup-stage requirement, not a lexicon
  gap** — the lookup must key on the citation form, never on the mutated surface string.
- **12 have no lexicon coverage** (listed in "unresolved" below, or missing a compound element).

### Mutated / inflected / phrasal keys and their citation forms

| test-word key | citation form used |
|---|---|
| `Ard-Easpag` | `ard + easpag` |
| `Fíor-Dhia` | `fíor- + dia` |
| `Lasairchos` | `lasair + cos` |
| `Ní Bhriain` | `Brian` |
| `a Sheáin` | `Seán` |
| `a bpeann` | `peann` |
| `an bhean` | `bean` |
| `an tsaoil` | `saol` |
| `an tsneachta` | `sneachta` |
| `an tsúil` | `súil` |
| `an-chiúin` | `ciúin` |
| `an-mhaith` | `maith` |
| `bhean` | `bean` |
| `bhfreagra` | `freagra` |
| `bhlas` | `blas` |
| `bhán` | `bán` |
| `bpeann` | `peann` |
| `caisleáin` | `caisleán` |
| `cheann` | `ceann` |
| `chrom` | `crom` |
| `cois` | `cos` |
| `deich bpeann` | `peann` |
| `dhearg` | `dearg` |
| `dhorn` | `dorn` |
| `dhroim` | `droim` |
| `droch-dhuine` | `droch- + duine` |
| `dteach` | `teach` |
| `fhreagra` | `freagra` |
| `fíoruisce` | `fíor- + uisce` |
| `garmhac` | `gar- + mac` |
| `gceann` | `ceann` |
| `ghlúin` | `glúin` |
| `héan` | `éan` |
| `lagphortach` | `lag- + portach` |
| `leabhair` | `leabhar` |
| `mbean` | `bean` |
| `mbláth` | `bláth` |
| `mháthair` | `máthair` |
| `mhór` | `mór` |
| `mo pheann` | `peann` |
| `n-éan` | `éan` |
| `na bpeann` | `peann` |
| `na héisc` | `iasc` |
| `ndroim` | `droim` |
| `ngasúr` | `gasúr` |
| `ngeata` | `geata` |
| `nglúin` | `glúin` |
| `pheann` | `peann` |
| `shnámh` | `snámh` |
| `shúil` | `súil` |
| `t-éan` | `éan` |
| `theach` | `teach` |

### Test-word keys with no coverage

- `Eoghan` — no base mapping / not in lexicon
- `Gráinne` — no base mapping / not in lexicon
- `Matánach` — matán + -ach (element(s) missing: matán, -ach)
- `Oisín` — no base mapping / not in lexicon
- `Tadhg` — no base mapping / not in lexicon
- `carrbhealach` — carr + bealach (element(s) missing: bealach)
- `dualgas` — no base mapping / not in lexicon
- `sméara` — sméar (element(s) missing: sméar)
- `splanc` — no base mapping / not in lexicon
- `stríoc` — no base mapping / not in lexicon
- `Órla` — no base mapping / not in lexicon
- `Úna` — no base mapping / not in lexicon

## Unresolved

Harvested but deliberately left OUT of the lexicon: no attested Old Irish form could be found
and loan/coinage status could not be established either, so writing a row would have meant
inventing a form. These fall through to the retro-filter and come out flagged `RETRO`.

| headword | why |
|---|---|
| `Eoghan` | Wiktionary explicitly labels the attested ancestor as "Middle Irish Eógan" (not Old Irish); no dedicated Old Irish lemma/declension page found for Eógan/Eogan on Wiktionary; no Wikipedia article confirms an Old Irish period form with citation |
| `Órla` | No Old Irish or Middle Irish section exists on Wiktionary for Órfhlaith (only Modern Irish); Wikipedia's Orla (name) article only says "Irish Órfhlaith" without specifying period or citing a primary source |
| `Tadhg` | Wiktionary explicitly labels the attested ancestor "Tadg" as Middle Irish, not Old Irish; no evidence of genuine Old Irish attestation, nor proof of loan/coinage status |
| `Gráinne` | Wiktionary only offers a speculative link ("possibly a derivative of Old Irish grán") for the common noun root, not an attested Old Irish form of the name itself |
| `Oisín` | Wiktionary labels "oisín" as Middle Irish/Irish only with no Old Irish section; no Old Irish attestation confirmed despite association with early Fenian Cycle material |
| `Úna` | Wiktionary only says "possibly from uan ('lamb')" with no Old Irish label or citation; no proof of attestation or of loan/coinage status |
| `Ardghal` | No Wiktionary entry exists for Ardghal/Ardgal/Artgal; Wikipedia biographical stubs (e.g. Ardgal mac Conaill, d.520) use the spelling but predate the conventional Old Irish period (c.600-900) and do not discuss it linguistically |
| `dualgas` | Wiktionary's Irish entry gives only Middle Irish forms (dúalgas/dúalcus/dúalus) from Middle Irish dúal "native, hereditary"; the dúal page has only a Middle Irish section with no etymology given at all — neither an attested OI ancestor nor a confirmed loan origin could be established from Wiktionary/Wikipedia |
| `splanc` | en.wiktionary.org/wiki/splanc has no Etymology section at all (only Alternative forms, Noun, Verb, Pronunciation, References); no OI/MI ancestor or loan source stated anywhere on the page or findable via WebSearch limited to wiktionary/wikipedia |
| `stríoc` | en.wiktionary.org/wiki/stríoc likewise has no Etymology section; no ancestor form or loan source given |
| `sméar` | Irish entry's etymology reads "From Middle Irish smér, from Proto-Celtic *smiyoros" — establishes the word is inherited, not borrowed, but skips stating any Old Irish form; no dedicated Old Irish Wiktionary page for smér exists; reporting an OI form would require inventing one |
| `gearr` | inherited from Proto-Celtic via Middle Irish, so an Old Irish ancestor existed, but no source consulted shows the Old Irish form — not a loan, so cannot be a `none` row |
| `garbh` | inherited from Proto-Celtic via Middle Irish, so an Old Irish ancestor existed, but no source consulted shows the Old Irish form — not a loan, so cannot be a `none` row |
| `Lorcán` | etymology only traces to epithet "Lorc" (Wiktionary), no attested Old Irish form of "Lorcán" itself found |
| `Éanna` | Wikipedia (Enda of Aran) gives "Éanna, Éinne or Endeus" as name variants but none explicitly labeled Old Irish; no Wiktionary entry |
| `Laoise` | no Etymology section found; only Wiktionary entry found is unrelated (genitive singular of place name Laois) |
| `Méabh` | Wiktionary gives only "from Middle Irish Medb"; Medb's own Wiktionary entry is also labeled Middle Irish, not Old Irish |
| `Naoise` | no Etymology section found on Wiktionary; Wikipedia (Deirdre) mentions Naoise but gives no Old Irish spelling |
| `Bláthnaid` | Wikipedia (Bláthnat) exists but does not label the form as Old Irish (calls it "early Irish literature") |
| `Damhnait` | no Wiktionary or Wikipedia page found under this or attempted Old Irish spellings (Damnat, Damhnait_of_Tydavnet, etc.) |
| `Macha` | no Old Irish section on Wiktionary; Wikipedia goddess page fetch failed (404) and was not otherwise confirmed |
| `Ríona` | no Wiktionary or Wikipedia page found |
| `Sláine` | Wikipedia page exists ("Sláine... is an Irish given name") but gives no Old Irish ancestor form |
| `Áine` | Wiktionary only says name is "a derivative of Old Irish án" (an adjective, not itself an attested OI proper name); Wikipedia mentions meaning but no attested OI form of the name Áine |
| `Barra` | no Irish-language Etymology section found on Wiktionary; not checked on Wikipedia within budget |
| `Brígh` | no Wiktionary page found (404); not checked further within budget |
| `Cairbre` | Wikipedia is a disambiguation page listing "Cairpre, Coirpre" as variants with no Old Irish label or discussion |
| `Comhghall` | no Wiktionary entry; Wikipedia (Comgall) does not give an Old Irish spelling in the article body (only via interlanguage link to modern Irish Wikipedia) |
| `Criomhthann` | Wikipedia (Crimthann) gives "Crimthann, Cremthann" without an explicit "Old Irish" label |
| `Cúán` | no Wiktionary or Wikipedia page found/checked successfully within budget |
| `Dallán` | no Wiktionary page (404); Wikipedia page for Dallán Forgaill not found under attempted title |
| `Dubhghall` | Wiktionary etymology gives only a surface compound analysis (dubh + gall), no attested Old Irish ancestor form |
| `Eoghanán` | no Wiktionary page found (404); not checked on Wikipedia within budget |
| `Fachtna` | Wiktionary etymology section is incomplete; no Old Irish form given, only speculative Latin derivation |
| `Fionntan` | Wikipedia (Fintan mac Bóchra) gives only "modern spelling: Fionntán" without an Old Irish label |
| `Garbhán` | no Wiktionary page found (404); not checked on Wikipedia within budget |
| `Iarlaith` | no Wiktionary page found (404); Wikipedia page for Jarlath of Tuam not found under attempted title |
| `Maolmhuire` | Wikipedia (Máel Muire) discusses the name but does not explicitly label "Máel Muire" as Old Irish (could be Middle Irish); no Wiktionary entry |
| `Ronán` | Wikipedia (Rónán mac Colmáin) uses only modern orthography, no Old Irish spelling given |
| `Séadna` | no Wiktionary page found; Wikipedia lookup under a plausible OI form (Sétna) resolved to an unrelated page (Sétanta/Cú Chulainn) |
| `Suibhne` | Wikipedia (Buile Shuibhne, Suibne mac Colmáin) discusses the name but does not give an explicit Old Irish label; text described as "Early Modern Irish" |
| `Ultán` | Wikipedia gives "Ultan (Irish: Ultán)" — labeled only "Irish", not "Old Irish" |
| `bealach` | Wiktionary derives it from Middle Irish belach only; no Old Irish entry exists. Inherited, not a documented loan, so it cannot be a `none` row |
| `matán` | Wiktionary Irish entry has no etymology section at all; neither an Old Irish ancestor nor loan status could be established |
| `gealach` | Wiktionary cites only an UNATTESTED Middle Irish *gelach; no attested Old Irish ancestor and no loan etymology |
| `uisce beatha` | two-word phrase; only the first element (uisce) has an attested Old Irish form, so the phrase cannot be keyed as one lexicon row — use the element rows uisce and beatha instead |
| `gruaig` | Wiktionary cites only an UNATTESTED Middle Irish *gruac; no attested Old Irish ancestor and no loan etymology |
| `gaiscíoch` | traced only to Middle Irish; no Old Irish form and no loan etymology found |
| `saoi` | Wiktionary gives only Middle Irish sui; no Old Irish section on any candidate page |

The dominant pattern here is **Middle Irish attestation without an Old Irish one**. Wiktionary
is explicit and consistent about this: *Eoghan* ← Middle Irish *Eógan*, *Tadhg* ← Middle Irish
*Tadg*, *Méabh* ← Middle Irish *Medb*, *bealach* ← Middle Irish *belach*, *saoi* ← Middle Irish
*suí*. These are not loans, so they cannot be `none` rows under spec §3 rule (2), and the Old
Irish form is not shown, so they cannot be `attested` rows either. If the strand later wants
them, the two honest routes are (a) an eDIL pass, or (b) an explicit policy decision to admit
Middle Irish forms as fallback ancestors with a distinct status value — a spec change, not a
harvest fix.

A second, smaller group is **inherited-from-Proto-Celtic with the Old Irish stage skipped**
(*gearr* < *gerr* < PC \*gerros; *garbh* < *garb* < PC \*garwos; *sméar* < *smér* <
PC \*smiyoros). An Old Irish ancestor certainly existed; no source consulted prints it.

## Sample verification

35 rows (5-seeded random sample, ~12% of the file) were re-checked against their cited pages by
an independent agent: **26 OK, 4 MINOR, 1 FAIL, 4 SKIP** (SKIP = `digest §10.n` citations, which
are local and not web-checkable). All five defects were corrected in the file:

| row | defect | correction |
|---|---|---|
| `buí` | the cited modern-Irish page has no Old Irish section | source repointed to the Old Irish entry `buide` |
| `nead` | genitive given as *neit* | corrected to *nit* per the cited page |
| `Maol Muire` | `gender = m` | the cited page calls *Máel Muire* unisex → gender blanked |
| `dán` | note claimed *dána* as an alternative genitive | it is an alternative nominative plural |
| `dubh` | note glossed the noun *dub* as "fault/blemish" | the page glosses it "ink, pigment, gall" |

Extrapolated, ~1 row in 30 has a wrong secondary field and ~1 in 35 has a wrong source pointer.
Spec §7 asks for a ≥30-row cross-family verification before the file is admitted; this pass
satisfies that bar, but a second pass over the ~107 rows with no genitive would be worth doing
before the inflection tests lean on them.

## Systematic findings

These are the harvest's payload for the retro-filter (`old-irish.rules [substitute]`, spec §4).
All counts are over the 270 attested rows in this file.

### 1. Modern ⟨ao⟩ corresponds to Old Irish ⟨óe/oí⟩ far more often than to ⟨áe/aí⟩ — decision O1 points the wrong way

Spec §8 decision O1 makes **⟨áe⟩ the default** for modern ⟨ao⟩ with ⟨óe⟩ as the
lexicon-attested alternative. The harvested pairs do not support that default. Of the 20 attested
pairs whose modern form contains ⟨ao⟩:

- **⟨óe/oí⟩ — 8:** *aon ~ óen*, *Aonghus ~ Oíngus*, *Caoimhe ~ cóem*, *caol ~ coíl*,
  *naoi ~ noí*, *naomh ~ noíb*, *taoiseach ~ toísech*, *Laoghaire ~ Lóegaire*.
- **⟨áe/aí⟩ — 10:** *Aodhán ~ Aédán*, *Aoibheann ~ Aíbinn*, *Aoife ~ Aífe*,
  *Faolán ~ Fáelán*, *laoch ~ láech*, *Éadaoin ~ Étaín*, *Maol ~ máel* and its three
  compounds *Maol Coluim ~ Máel Coluim*, *Maol Muire ~ Máel Muire*,
  *Maol Seachlainn ~ Máel Sechnaill*.
- **neither — 2:** *caora ~ cauru*, *saol ~ saegul*.

⟨áe/aí⟩ leads 10–8 on raw count, but four of those ten are the single *Máel* element repeated
across its compounds; counting *Máel* once, the two reversals are at parity — ⟨óe/oí⟩ wins the
high-frequency short words (*aon, naoi, naomh, caol*) and ⟨áe/aí⟩ wins the
*Máel-/láech/Fáelán/Aoife* group.
**Neither is a safe blanket default.** The concrete recommendation is a two-way split rather than
one default plus lexicon exceptions: **⟨ao⟩ before a slender consonant (modern ⟨aoi⟩) → ⟨aí/óe⟩,
⟨ao⟩ before a broad consonant → ⟨áe⟩ in the *Máel/láech* shape and ⟨óe⟩ elsewhere.** Whichever way
the decision goes, 20 lexicon pairs now exist to test it against, so the filter-regression test in
spec §7 will measure the choice directly rather than leaving it to taste.

### 2. Modern ⟨ea io ui ai⟩ around a single vowel are quality digraphs, not vowels — the largest single reversal class

50 attested pairs — the biggest correspondence in the harvest — show the modern spelling adding a
glide letter that Old Irish did not write, because Old Irish marked consonant quality by the
*following* vowel only (digest §10.2.5), while modern Irish brackets the vowel on both sides
(*caol le caol*):

*fear ~ fer* · *bean ~ ben* · *ceann ~ cenn* · *dearg ~ derg* · *geal ~ gel* · *beag ~ bec* ·
*deas ~ dess* · *nead ~ net* · *neamh ~ nem* · *fearg ~ ferg* · *easpag ~ epscop* ·
*leabhar ~ lebor* · *leanbh ~ lenab* · *freagra ~ frecrae* · *airgead ~ argat* ·
*Fionn ~ Finn* · *Giolla ~ gilla* · *inion ~ ingen* · *iolar ~ irar* · *muileann ~ muilenn* ·
*Muireann ~ Muirenn* · *Ceallach ~ Cellach* · *croiceann ~ croiccenn* · *Fearghal ~ Fergal* …

The reversal rule is therefore **delete the glide letter, keep the quality**: modern ⟨ea⟩ → OI
⟨e⟩, ⟨io⟩ → ⟨i⟩, ⟨ai⟩/⟨oi⟩ before a slender consonant → the bare vowel. This is purely
orthographic and needs the `@orth` atom of spec §4 — the *sound* is unchanged across the two
stages, so no sound-driven rule can see it. It is also the class most likely to dominate the
filter-regression match rate, simply by count.

### 3. Old Irish writes geminates that modern Irish has simplified — and modern lenition digraphs correspond to *nothing* in the Old Irish spelling

Two reversals that must run in opposite directions on the same word:

- **Geminates (47 attested pairs).** Old Irish ⟨cc nn ll rr mm tt⟩ where modern Irish has a
  single letter or a different digraph: *mac ~ macc* · *cnoc ~ cnocc* · *ainm ~ ainmm* ·
  *droim ~ druimm* · *bacach ~ baccach* · *cill ~ cell* · *bainne ~ bannae* ·
  *Fionnbharr ~ Findbarr* · *Neasa ~ Nessa*. Note the geminate is often *restored* going
  backwards (mac → macc), so this is a rule the retro-filter must add material for, not strip.
- **Lenition digraphs (~100 attested pairs: bh 16, dh 11, gh 8, mh 14, ch 29, th 22).** Modern
  ⟨bh dh gh mh⟩ correspond to Old Irish **plain, unmarked** ⟨b d g m⟩ — *dubh ~ dub*,
  *adharc ~ adarc*, *Lughaidh ~ Lugaid*, *lámh ~ lám*, *Domhnall ~ Domnall*, *sluagh ~ slóg*,
  *claíomh ~ claideb* — while modern ⟨ch th⟩ correspond to Old Irish ⟨ch th⟩ *unchanged*
  (*cloch ~ cloch*, *bláth ~ bláth*, *cath ~ cath*, *athair ~ athair*). **⟨ph⟩ and ⟨sh⟩ do not
  occur at all in the 270 attested modern keys** — those two branches of the §4 substitute rule
  have no lexicon pair to instantiate them and will stay `%design`, untested, unless a word with
  a lenited *p* or *s* in its citation form is added deliberately.

### 4. Smaller but clean correspondences

- **Modern ⟨ua ia⟩ ↔ Old Irish ⟨úa ía⟩ with the length mark on the *first* element** (33 pairs):
  *tuath ~ túath* · *sliabh ~ slíab* · *iasc ~ íasc* · *grian ~ grían* · *Niall ~ Níall* ·
  *cluas ~ clúas* · *uasal ~ úasal* · *Ciarán ~ Cíarán*. The reversal is mechanical: add the
  acute to the first vowel of the diphthong. Two exceptions worth noting, both where modern ⟨ua⟩
  comes from an Old Irish long monophthong rather than a diphthong: *sluagh ~ slóg*,
  *fuar ~ úar* (and *Nuala ~ Finnguala*, which is a clipping, not a sound change).
- **Word-final unstressed vowels survive**, contra the usual "Old Irish had more endings"
  intuition: *cara ~ carae*, *sneachta ~ snechtae*, *freagra ~ frecrae*, *croí ~ cride*,
  *céile ~ céile*, *duine ~ duine*, *uisce ~ uisce*. The io-stem/iā-stem classes are the ones
  that keep a final vowel in both stages; the retro-filter should *not* strip modern final ⟨-a
  -e⟩, it should respell them (⟨-a⟩ → ⟨-ae⟩ is the commonest single reversal here).
- **The ⟨-án⟩ diminutive is invariant** across the whole harvest: *Ciarán ~ Cíarán*,
  *Colmán ~ Colmán*, *Faolán ~ Fáelán*, *Odhrán ~ Odrán*, *bradán ~ bratán*, *arán ~ arán*,
  *Rónán ~ Rónán*. No reversal rule needed.
- **The r-stem kinship set is spelling-invariant**: *athair ~ athair*, *bráthair ~ bráthair*,
  *máthair ~ máthair* (Wiktionary also gives *máthir*). These are the best "does the filter leave
  well enough alone" regression cases in the file.

### 5. Stem-class mapping decisions taken during the harvest (affects `[inflect]`)

The spec's `stem` vocabulary has seven values but Old Irish grammars distinguish more classes, so
the harvest applied a fixed mapping, recorded in every affected row's `note`:

| real Old Irish class | `stem` value | why |
|---|---|---|
| o-stem, io-stem | `o` | same endings modulo the glide |
| ā-stem, iā-stem, ī-stem | `ā` | ditto |
| i-stem, u-stem, n-stem, dental stem | as named | direct |
| **velar (guttural) stem, r-stem, s-stem, indeclinable** | `irregular` | no spec slot; true class in `note` |

`irregular` is therefore **37 rows covering four genuinely different paradigms** — it is a
placeholder, not a class. `[inflect]` cannot inflect an `irregular` row from the column alone; it
must read the `note`, or the spec must grow the vocabulary. The affected paradigm words are the
ones the inflection tests want most: *teach ~ tech* (s-stem), *athair* (r-stem),
*rí ~ ríg* (velar), *sliabh ~ slíab* (s-stem), *Lughaidh ~ Luigdech* (velar),
*Eochaidh ~ Echach* (velar). **This is the one finding that needs a decision before milestone 4.**

### 6. Where sources disagreed

Kept the better-attested form, recorded the alternative in `note`, per spec §3 rule (4):

- *ball* gen. **baill** (Wiktionary declension table), not *boill* as the digest's §10.5 table
  prints it.
- *scél* gen. **scéuil**, not *scéil* (digest §10.5 gives both).
- *cnáim* is **masculine** on Wiktionary; the digest's §10.5 table lists it under the feminine
  i-stems.
- *Eochu* is spelled **Echu** as the Wiktionary lemma; *Eochu/Eochaid/Eocho* are cross-referenced
  alternatives. The digest uses *Eochu*.
- *gilla* is labelled **Middle Irish** by Wiktionary even though it is the first element of Old
  Irish *Gilla Pátraic*; the row is kept `attested` on the Wikipedia citation that shows the Old
  Irish compound, with the conflict recorded.
- *madra*: the modern entry's etymology names Old Irish *madrad, matrad*, but the dedicated
  *madrad* entry is categorised Middle Irish. Kept on the etymology citation, conflict recorded.
- *mór*: nominative *mór*, alternative *már*.
- *Fergal* is grammatically masculine but declines as a feminine ā-stem (the *-gal* compound
  ending): row is `stem = ā`, `gender = m`.
- *Lothland* (~ *Lochlann*) is attested only as the **place name** "Scandinavia"; the modern
  given name is a secondary reuse. Flagged in the row's note — worth a decision on whether that
  counts as an ancestor.

### 7. A note on `none` rows

29 rows are `none`. They split into two kinds, and the distinction matters for the `RETRO:loan`
flag (spec §8 decision O4):

- **True post-Old-Irish loans (12):** *Seán*, *Siobhán*, *Séamus*, *Brian* (Old Breton *Brient*),
  *tobac*, *téarma*, *seirbhís*, *geata*, *bád*, *speal*, *cnaipe*, *Cairmilíteach*.
- **Irish-internal formations later than Old Irish (17):** *Ciara*, *Saoirse* (20th c.),
  *Gaelach*, *naofa*, *leisciúil*, *ardnósach*, *drochbhéasach*, *cailín*, *portach*, *bádóir*,
  *gasúr*, *spraoi*, *breá*, *cliste*, *cróga*, *dílis*, *an-*.

The second group is not a *loan* in any sense — flagging them `RETRO:loan` would be misleading in
the trace. If the flag vocabulary can afford it, `RETRO:late` for the second group would say what
actually happened. Note also that several `attested` rows are Latin loans that Old Irish had
*already* taken (*peann ~ penn*, *leabhar ~ lebor*, *caisleán ~ caisel*, *easpag ~ epscop*,
*saol ~ saegul*, *cill ~ cell*, *ór ~ ór*) — these are correctly `attested`, and they are the
reason the loan test has to be "is it in Old Irish?", not "is it ultimately foreign?".
