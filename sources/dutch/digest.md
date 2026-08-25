# Source digest: Dutch (Belgian Standard Dutch)

## 0. Variety and scope

**Variety: Belgian Standard Dutch** (Flanders), the variety described by Verhoeven (2005). This is
the variety behind **PHOIBLE InvID 2169**: the inventory row and its primary description are the
*same document*, so inventory and prose cannot disagree with each other
[verhoeven2005 p.243; dutch/bib.md §"Belgian vs. Netherlandic"]. Verhoeven describes it as one of the two
institutionalised standard varieties, spoken by ~6 million people in the northern part of Belgium;
"the lexical and syntactic differences between the two language varieties are very small",
the differences being **phonetic** [verhoeven2005 p.243].

**Split-source warning — read this before using §2.** The inventory (§1) is Belgian
[verhoeven2005]. The **phonotactics (§2), the process rules (§3) and the stress system (§4) are
taken from Netherlandic-oriented sources** — Taalportaal (which restates Booij 1995 page by page),
Booij's own papers, Kager & Pater 2012, Wikipedia. This is defensible precisely because Verhoeven
locates the B/N difference in phonetics rather than phonotactics, but it is an assumption, not an
attested fact about Flanders, and every §2 rule should be read as "Netherlandic-sourced, assumed to
carry over".

**Transcription conventions differ between the two halves and must be normalised by the tool.**
This digest keeps each source's symbols inside quoted examples (so the citation can be checked), but
every rule is to be applied to the **Belgian target representation** below. Apply this mapping to any
Netherlandic-sourced list or example before encoding it.

**Normalization layer (Netherlandic source symbol → Belgian target symbol)**

| Source writes | Belgian target | Why |
|---|---|---|
| `a e o y ø` (A-class, no length mark) | `aː eː oː yː øː` | Belgian has these as long monophthongs, never diphthongised [verhoeven2005 p.245–246] |
| `i u` (A-class) | `i u` (unchanged) | phonetically short high tense vowels in both [verhoeven2005 p.245; kager-pater2012 p.7] |
| `ʋ` | `w` (a labial approximant, not English /w/, not /v/) | [verhoeven2005 p.245]; but see the CONFLICT in §1 |
| `r` | `r` = alveolar **or** uvular trill, in free variation | [verhoeven2005 p.245] |
| `h` (Taalportaal) / `ɦ` (Wikipedia, PHOIBLE) | `ɦ` | Verhoeven's chart has `ɦ` [verhoeven2005 p.243] |
| positional `x`/`ɣ` (van der Sijs's WOLD transcription) | keep the **lexical** value: Belgian contrasts `/x/` and `/ɣ/` | [verhoeven2005 p.244] |
| Netherlandic `χ` (uvular) | `x` | uvular `/χ/` "does not occur in Belgian Dutch" [verhoeven2005 p.244] |
| `ɛi œy ɑu` | `ɛi œy ɔu` | Verhoeven's chart and example words *lei, lui, lauw* [verhoeven2005 p.245] |

Normalized Belgian phoneme list to encode rules over:
consonants `/p b t d k f v s z x ɣ ɦ m n ŋ r l w j/` + loan `/ʃ ʒ g/`;
vowels `/i ɪ eː ɛ ɑ aː ɔ oː u ʏ yː øː ə/` + loan `/ɛː œː ɔː/`; diphthongs `/ɛi œy ɔu/`.

**Licensing.** Taalportaal is free to read but **not openly licensed** (INT terms: non-commercial /
private use only). Citing and quoting is fine; shipping derived cluster tables in a public repo is
not clearly covered. Every Taalportaal-only fact below is marked `[taalportaal-*]` so it can be
re-sourced from `booij1978`/`booij1999`/`wiki-nl-phonology` if that becomes necessary
[dutch/bib.md, `taalportaal` entry].

**Contradictions of the PHOIBLE row** are listed in §1: chiefly the missing `/ə/`.

## 1. Inventory deltas

### Consonants (Verhoeven's chart; parenthesised = "surface phenomena or marginal, loan words only")

| | Bilab | Labiodent | Alv | Postalv | Palatal | Velar | Uvular | Glottal |
|---|---|---|---|---|---|---|---|---|
| Plosive | p b | | t d | | (c) | k (g) | | (ʔ) |
| Nasal | m | (ɱ) | n | | (ɲ) | ŋ | | |
| Trill | | | (r) | | | | ʀ | |
| Fricative | | f v | s z | (ʃ) (ʒ) | | x ɣ | | ɦ |
| Approx | w | | | | j | | | |
| Lat. approx | | | l | | (ʎ) | | | |

[verhoeven2005 p.243, chart + p.244 word list]

- **/ɣ/ and /x/ are both phonemes in Belgian**: "Belgian Dutch has a voiced and voiceless velar
  fricative: these are absent in the Netherlands. The Netherlands has a voiceless uvular fricative
  which does not occur in Belgian Dutch" [verhoeven2005 p.244]. Minimal-ish pairs given: *chijl*
  /xɛil/, *geil* /ɣɛil/ [verhoeven2005 p.244]. Wikipedia agrees: in the south the /x/–/ɣ/ distinction "is
  generally preserved as velar [x, ɣ] or post-palatal [x̟, ɣ˖]", the *zachte g*
  [wiki-nl-phonology §Consonants/Dorsal]. **This is the single most important Belgian property for
  Irish input** (§8).
- **The fricative voicing contrast /f v/, /s z/, /x ɣ/.** Verhoeven's own wording is hedged: it
  "has been held traditionally" that the contrast "is still very stable in Belgian Dutch", and the
  same paragraph reports extensive phonetic devoicing — 70% of word-initial and 56% of intervocalic fricatives are realised with no
  vocal-fold vibration; **word-final fricatives are always voiceless** [verhoeven2005 p.244, citing
  Verhoeven & Hageman in press]. So: keep the contrast underlyingly, expect voiceless phonetics.
- **/r/**: free variation between an alveolar trill and a uvular trill; the alveolar is the most
  frequent and most widely distributed, the uvular is regionally concentrated (Ghent, Brussels,
  Limburg) and gaining. /r/ is **voiced in all positions except word-finally and before a voiceless
  stop**: [doːʀ̥] *door*, [vaːʀ̥t] *vaart* [verhoeven2005 p.245]. Verhoeven's own example words are
  transcribed with ʀ (*raad* [ʀaːt]).
- **Marginal / allophonic consonants and where they come from** [verhoeven2005 pp.244–245]:
  - [c] — diminutives of nouns in /t d/: *bootje* [boːcə], *paardje* [paːʀcə]
  - [ɲ] — foreign *lasagna* [lɑzɑɲa]; and /n/ + palatal stop in diminutives: *landje* [lɔɲcə]
  - [ɱ] — assimilation of /m/ before a labiodental fricative: *omvallen* [ɔɱvɑlə]
  - [g] — *zakdoek* [zɑgduk], *dekbed* [dɛgbɛt] (voicing assimilation), plus loans
  - [ʔ] — word-initial before a vowel, as a strong attack
  - [ʎ] — only from assimilation with a following /j/
  - a labiodental stop in *opvallen*, *opvoeren*
- **/w/**: "labial-velar articulation rather than labiodental in many accents of Netherlandic Dutch"
  [verhoeven2005 p.245]. **CONFLICT:** Wikipedia says southern-Netherlands/Belgian speakers use a
  **bilabial approximant [β̞]**, "like [w] but without velarisation"
  [wiki-nl-phonology §Sonorants]; Taalportaal writes the phoneme /ʋ/ throughout. Practically: it is
  a labial approximant, not English /w/ and not /v/.
- **/l/** is "often slightly velarized in postvocalic positions" [verhoeven2005 p.245]. Wikipedia
  makes this sharper for Belgium: dark /l/ is realised **velarised [lˠ]** (*schelp* [sxɛlˠp]) *or*
  **post-palatalised [lʲ̠]** (*schandaal* [sxaːnˈdaːlʲ̠]); some Standard Belgian speakers have clear
  /l/ everywhere; palatal [ʎ] appears before /j/ [wiki-nl-phonology §Sonorants]. Note for §8: those
  are exactly the two Irish /l̪ˠ/ ~ /lʲ/ colours, as sub-phonemic variants.

### Vowels

Verhoeven: **twelve monophthongs and three diphthongs** [verhoeven2005 p.245]:
/i ɪ eː ɛ ɑ aː ɔ oː u ʏ yː øː/ and /ɛi œy ɔu/ (his examples: *lei* [lɛj], *lui* [lœy], *lauw* [lɔu]).
Belgian [eː øː oː] are **always monophthongs**; Netherlandic diphthongises them [verhoeven2005 p.245–246].

**Delta 1 — /ə/ is missing from the PHOIBLE row and from Verhoeven's vowel chart, and must be
added.** Verhoeven's own broad-phonetic passage is full of it: *de noordenwind* [də noːʀdəwɪntˢ],
*warme* [wɑʀmə], *sterkste* [stɛʀkstə] [verhoeven2005 p.247]. It is the epenthetic vowel (*melk* →
[mɛlək], §3), the reduction vowel, and the vowel of most inflectional endings. Taalportaal treats it
as a nucleus with its own restrictions: schwa **can never bear stress**, lexical words must contain
at least one full vowel besides it, and schwa does not occur word-initially in polysyllabic lexical
words [taalportaal-nuclei §quickinfo; taalportaal-onsetless-syllables §2].

**Delta 2 — three loan vowels.** Taalportaal adds "three loan vowels /ɛː, œː, ɔː/ which occur in
loan words" [taalportaal-nuclei §quickinfo]. Van der Sijs's *leenfonemen* list is longer and
orthographic: long *è* (crème, malaise), long *o* (controle, zone, corner), long *eu*
(œuvre, girl, service), long *ie* (remise, team), long *oe* (rouge, cruise, pool), long *u*
(centrifuge), four nasal vowels (timbre, bon-ton, parfum, restaurant), the diphthongs [oi] and [ai]
(*boiler, boy, skyline* — licensed by the native interjections *hoi, ai*), and three loan consonants
[g], [ʃ], [ʒ] [vandersijs1996-leenwoordenboek p.57–58].
- **Nagy's adaptation-vs-integration distinction** is the right frame: *adaptation* replaces a
  foreign segment with a native one; *integration* admits the foreign segment or extends its
  distribution, and only integration changes the system [nagy2008-frans §3.1]. For Belgian, the
  **French nasal vowels are integrated** rather than adapted (see §3) [nagy2008-frans §3.2.1].
- /g/: not native, but its status is genuinely unsettled — see the /g/ row in §3.

### Notational quirks of the PHOIBLE row
- 37 segments; `ʃ ʒ ʔ` flagged Marginal (matching Verhoeven's parentheses), but `c g ɱ ɲ ʎ` (also
  parenthesised by Verhoeven) are simply absent, and so are `ə` and the loan vowels.
- The row writes the rhotic `r` and the labial approximant `w`; Verhoeven's example transcriptions
  use `ʀ`, and Netherlandic sources use `ʋ`.
- The row writes /i/ and /u/ without length but /aː eː oː yː øː/ with it. That matches Verhoeven's
  chart (high tense vowels are phonetically short) — it is **not** a claim that /i u/ are lax.
- CONFLICT (labels, not facts): **"A-class" and "B-class" mean opposite things in two of our
  sources.** Taalportaal: A-class = tense/long /i y u e ø o a/, B-class = lax/short /ɪ ʏ ɛ ɔ ɑ/
  [taalportaal-nuclei §A-class vowels, §B-class vowels]. Kager & Pater: Class A = the lax set,
  Class B = the tense set [kager-pater2012 p.5–6]. This digest uses **Taalportaal's** labels
  throughout (A = tense). Anyone reading the papers directly must re-check the polarity.

## 2. Syllable structure and phonotactics

### Maximal template
Onset: max three consonants, and if there are three the first must be /s/
[taalportaal-onset-clusters-3c §quickinfo (Booij 1995:26)].

**CONFLICT: the maximal coda.** Sources disagree on how many post-nuclear consonants to allow, and
the disagreement is about *analysis*, not data.
- `lapsyd-dutch-nld §Syllable structure` records `Coda=3` in its syllabic index but prints a
  canonical form with **four** coda slots, `(C)(C)(C)V(V)(C)(C)(C)(C)`.
- `wiki-nl-language §Phonology` gives `(C)(C)(C)V(C)(C)(C)(C)` and cites *herfst* /ɦɛrfst/, *ergst*
  /ɛrxst/.
- `taalportaal-codas §quickinfo` says word-final codas run "up to five consonants" (*herfst*,
  *promptst*) but word-medial codas max out at **two** (*werkloos* /ʋɛrk.los/).
- `taalportaal-nuclei §Rhyme structures, Table 2` says the rhyme itself allows **at most two** coda
  consonants, and only one after a tense vowel or diphthong.
**Resolution to encode** (Taalportaal's own reconciliation, after Booij 1995:41): a **rhyme coda of
at most two** consonants, plus **up to three appendix positions restricted to coronal obstruents**
at the word edge [taalportaal-codas §An alternative account of syllable structure and coda
clusters]. Everything above two is appendix, and each source's number falls out of this.
Worked shapes: *strak* /strɑk/ CCCVC, *scriptie* /skrɪp.si/, *herfst* /hɛrfst/ VCCCC, *hoorn* /horn/
[taalportaal-syllable-level §readmore].

### Onsets — singletons
Every consonant may be a syllable onset **except /ŋ/** [taalportaal-onsets-simple §quickinfo]. /ŋ/
is barred word-initially and morpheme-initially; word-medially it appears only intervocalically
after a B-class vowel and before schwa (*zwanger* /zʋɑŋər/, *engel* /ɛŋəl/), analysed as ambisyllabic
[taalportaal-onsets-simple §The velar nasal constraint (Booij 1995:36); booij1978-fonotactische §].
/g/ is an onset "only in loanwords" (*goal, regatta, slogan*) [taalportaal-onsets-simple Table 1].
/h/ never enters a cluster ("a branching onset may not dominate [+aspirated]")
[taalportaal-onset-clusters-2c §readmore (Booij 1995:36)]. /j/ is never the *first* member of a
cluster [taalportaal-onset-clusters-2c §readmore (Booij 1995:36)].
Onset–nucleus bans: */hə/; */ji/, */ʋy/, */ʋø/*
[taalportaal-onsets-simple §Co-occurrence restrictions].

### Onsets — CC (exhaustive; Netherlandic transcription as printed)
Native/frequent:
`pl` plug · `pr` prijs · `bl` bloem · `br` broek · `tʋ` twee · `tr` troep · `dʋ` dwars · `dr` droom ·
`kʋ` kwal · `kl` klok · `kr` krul · `kn` knie · `fl` fluit · `fr` framboos · `fn` fnuiken ·
`vl` vlag · `vr` vraag · `sl` sla · `sm` smaak · `sn` snaar · `sf` sfeer · `sx` schoen · `sp` spook ·
`st` stoel · `sk` ski · `zʋ` zwart · `xl` glas · `xr` groen · `xn` gnoe · `ʋr` wraak
Loanword-only / marginal:
`pj` piu · `pn` pneumonie · `pf` Pfeiffer · `ps` psalm · `pt` Ptolemeus · `pw` pointe · `ts` tsaar ·
`tʃ` chip · `tw` etui · `kj` barbecue · `ks` xylofoon · `gʋ` pinguin · `gl` neglige · `gr` grill ·
`fj` fjord · `vj` vieux · `vw` voile · `sʋ` suite · `sr` Sri Lanka · `ʃʋ` sjwa · `ʃl` schlemiel ·
`ʃm` schmink · `ʃn` schnabbel · `mw` moiré · `nw` nuit · `lj` milieu · `rw` bavarois
[taalportaal-onset-clusters-2c §Examples (Trommelen 1984:105);
taalportaal-fig-onset-cc-matrix.png; taalportaal-fig-onset-cc-matrix-native.png]

**Explicit exclusions** (the negative information, read off the matrices and the prose):
- **Sonorant + obstruent onsets are categorically banned** [taalportaal-onset-clusters-2c
  §Sonorant + obstruent sequences].
- Two-coronal: `*tl *dl *zl` (but /sl ʃl/ are fine — /s/ behaves as an appendix, not a true onset
  member) [taalportaal-onset-clusters-2c §Obstruent + sonorant sequences].
- Two-labial: `*pʋ *bʋ *fʋ *vʋ`.
- Sibilant + rhotic: `*zr *ʃr`; /sr/ only in very recent loans (*Sri Lanka*). Historical /t/-intrusion
  doublets: *remmen/stremmen*, *rekken/strekken*, *siroop/stroop* (Trommelen 1984:110–111).
- Velar fricative + glide: `*xj *ɣj *xʋ *ɣʋ`.
- Unattested sCC: `*sfl *sxl *skn` [taalportaal-onset-clusters-3c §readmore].
- **Consonant Cluster Condition** (Booij 1995:44, after Yip 1991): in a consonant cluster,
  consonants may have **at most one articulator feature other than coronal**. Every onset cluster
  obeys it except `/kʋ/` (*kwal*). /r/ counts as placeless and so combines with any place
  [taalportaal-consonant-cluster-condition §Onset consonant clusters;
  taalportaal-fig-onset-cc-coronal.png].
- Obstruent+obstruent onsets must agree in voicing; obstruent+/n l r/ clusters strongly prefer a
  voiceless obstruent [taalportaal-onset-clusters-2c §Obstruent + obstruent / + sonorant sequences].

### Onsets — CCC (complete)
Native: `spl` spleet, `spr` spreuk, `str` strop, `sxr` schrik.
Loanword-only: `skl` sclerose, `skr` screen, `skʋ` squash.
[taalportaal-onset-clusters-3c §readmore]

### Onsetless syllables
Always permitted, with any nucleus except schwa (schwa word-initially only in function words, e.g.
*een* [ən]) [taalportaal-onsetless-syllables §1–2]. **[ʔ] is inserted obligatorily before a
word-initial vowel in a stressed syllable, optionally when unstressed**: *opera* [ˈʔopəra],
*enorm* [(ʔ)eˈnɔrm] [taalportaal-onsetless-syllables §3 (Gussenhoven 1992:45)]. Verhoeven independently reports the glottal
stop "confined to word-initial position as a strong attack of vowels" for Belgian
[verhoeven2005 p.244].

### Rhymes: the nucleus/coda contract
- **A-class (tense) vowels and diphthongs** occur in open syllables and in closed syllables with
  **one** coda consonant; they cannot precede a branching coda.
- **B-class (lax) vowels cannot occur in open syllables**: minimally one coda consonant is
  obligatory, maximally two.
- Non-coronal coda clusters of more than two consonants are prohibited.
[taalportaal-nuclei §Rhyme structures, Table 2]

### Coda size
Word-**medially** codas max out at **two**: *werkloos* /ʋɛrk.los/. Word-**finally** they reach
**five**: *herfst* /hɛrfst/, *promptst* /prɔmptst/ [prɔmp(t)st] [taalportaal-codas §quickinfo]. The
extra positions are an **appendix restricted to coronal obstruents**, which is why word-final
coronals escape the rhyme limits [taalportaal-codas §An alternative account (Booij 1995:41)].
Four-consonant codas are limited to *-rnst*, *-rfst* (*ernst*, *herfst*)
[booij1978-fonotactische §].

### Coda clusters (with examples as printed)

**Read these lists as UNDERLYING (lexical) forms.** Taalportaal writes them phonemically, with the
voiced obstruent that resurfaces in the plural or past-tense form; **final devoicing (§3.5) means no
voiced obstruent ever surfaces in a coda.** Surface outputs are given in brackets where the source
gives them. A rule-writer must not license a voiced surface coda from this table.
- **Sonorant + sonorant** (liquid before nasal only): `-lm` zalm, `-rm` arm, `-rn` karn.
  Banned: `*-ln` (German *Köln* → Dutch *Keulen*), `*-lŋ`, `*-rŋ`, `*-rl` (German *Karl* → Dutch
  *Karel*) [taalportaal-codas Table 1].
- **Liquid + obstruent**: `-lf` elf, `-lv` elf 'eleven', `-ls` als, `-lz` hals, `-lx` mulch,
  `-lɣ` balg, `-lp` hulp, `-lt` asfalt, `-ld` held, `-lk` elk, `-rf` smurf, `-rv` korf, `-rs` mars,
  `-rz` vers, `-rx` monarch, `-rɣ` erg, `-rp` harp, `-rt` art, `-rd` hard, `-rk` ark.
  Banned: `*-lb`, `*-rb` — these occur **only in loans** (*stilb, sorb, blurb*)
  [taalportaal-codas Table 2].
  **Surface:** the voiced members neutralize — /-lv/ → [-lf] (*elf* 'eleven' = *elf* 'elf'),
  /-lz/ → [-ls] (*hals* [hɑls]), /-lɣ/ → [-lx] (*balg* [bɑl(ə)x]), /-ld/ → [-lt] (*held* [hɛlt]),
  /-rv/ → [-rf] (*korf* [kɔr(ə)f]), /-rz/ → [-rs] (*vers* [vɛrs]), /-rɣ/ → [-rx] (*erg* [ɛr(ə)x]),
  /-rd/ → [-rt] (*hard* [hɑrt]) [taalportaal-codas Table 2, bracketed forms].
- **Nasal + obstruent**: only nasal + **homorganic stop**. `-mp` ramp, `-nt` munt, `-nd` mond
  (surface [mɔnt]), `-ŋk` koninklijk; `-md` hemd (surface [hɛmt]), *vreemd* is non-homorganic and
  infrequent. Banned: `*-mb`
  (only loan *aplomb* [aˈplɔm]), `*-ŋg`. **Nasals cannot combine with fricatives in the same coda**
  (cf. heterosyllabic *kamfer* /kɑm.fər/) [taalportaal-codas Table 3].
- **Obstruent + obstruent**: at least one member is coronal, normally the second (except /sC/):
  `-pt` intercept, `-ps` rups, `-ts` muts, `-tʃ` kitsch, `-kt` pact, `-ks` heks, `-ft` kaft,
  `-sp` wesp, `-st` beest, `-sk` kiosk, `-xt` macht. Gaps: `-fs`, `-xs`
  [taalportaal-codas Table 4].
- The /sp sk st/ codas violate sonority sequencing and are treated as the same /s/-appendix
  exception as in onsets [taalportaal-codas §Exceptional bisegmental coda clusters (Booij 1995:41)].
- **True coda vs appendix.** In every cluster above, only the first two consonants occupy rhyme-coda
  positions; anything beyond them — and, on Van Oostendorp's account, the final coronal of *kaft*
  [kɑft], *paard* [paːrt], *herfst* [hɛr(ə)fst] — is appendix / extra-prosodic. The diagnostic the
  source gives is **schwa epenthesis: it can break a coda + extra-syllabic-consonant sequence
  ([hʏl(ə)p], [hɛr(ə)fst]) but never a consonant + appendix sequence (\*[kɑfət], \*[paːrət],
  \*[hɛrfəst])** [taalportaal-codas §An alternative account, figures 2–3]. That test is the practical
  way to decide which positions a generated form has.
- Coda clusters are broadly the **mirror image** of onset clusters, slightly larger: /-lm -rm -lt/
  exist though /ml- mr- tl-/ do not; conversely /bl- br-/ exist though /-lb -rb/ do not
  [taalportaal-codas §Bisegmental coda clusters (Booij 1981)].

### The two restrictions that bite hardest on Irish input

**(a) The tense-vowel / voiced-fricative pact.**
> A-class (tense) vowels and diphthongs are followed only by **voiced** fricatives /v z ɣ/;
> B-class (lax) vowels only by **voiceless** fricatives /f s x/.

Examples: *heuvel* /høvəl/, *vezel* /vezəl/, *vogel* /voɣəl/ vs. *knuffel* /knʏfəl/, *tussen*
/tʏsə(n)/, *lachen* /lɑxə(n)/ [taalportaal-coda-cooccurrence-restrictions §A-class vowel /
diphthong + /v, z, ɣ/ and B-class vowel + /f, s, x/].
Stated exceptions, all of them:
1. Loans *puzzel* /pʏzəl/, *mazzel* /mɑzəl/ (B-class + voiced) — and *puzzel* has a competing
   pronunciation [ˈpy.zəl] that repairs the violation by tensing the vowel.
2. The dialectal /x~ɣ/ merger makes *apparent* A-class + voiceless sequences; the merger is
   phonetic, since speakers still choose the past-tense suffix by the underlying voicing.
   (Belgian does **not** have this merger — §1.)
3. A small genuine set: *goochem* /xoxəm/, *sjofel* /ʃofəl/, *tafel* /tafəl/, *brasem* /brasəm/ —
   all morpheme-internal, all intervocalic.
4. **Schwa patterns with the lax vowels**, not with the tense ones: Table 1's /ə/ column has
   *gannef* (/f/), *hannes* (/s/), *jarig* (/x/), *hennep*, *lemmet*, *-(e)lijk*, but a dash for
   /v z ɣ/ [taalportaal-coda-cooccurrence-restrictions Table 1]. So **/əx/ is licit and /əɣ/ is
   not** — which matters directly for Irish unstressed *-ach* (see §8.3).
5. Diphthongs are partly exempt: all three may precede /s/ (*krijs, kruis, kous*) and /œy/ may
   precede /x/ (*gejuich*), evidenced by the *-te* past-tense suffix they select.
[all: taalportaal-coda-cooccurrence-restrictions §same]
**CORRECTION to bib.md.** bib.md's `taalportaal` entry says "Irish /ɑː/+/x/ (as in *Matánach*
/ˈmˠat̪ˠɑːnˠəx/) is exactly the banned A-class + voiceless fricative shape". **In that word it is
not**: the long /ɑː/ is followed by /nˠ/, and the /x/ is preceded by the *schwa* of unstressed
*-ach* — and schwa takes voiceless fricatives (exception class 4 above, *jarig* [jaːrəx]). So
*Matánach* passes this constraint unaltered. The constraint is real and does bite Irish input, but
only where a **long vowel directly precedes a voiceless fricative** — a stressed monosyllable like
*bách* /bˠɑːx/, or any /Vːx Vːf Vːs/ sequence. See the worked derivation in §8.6.

**(b) The Kager & Pater restriction: `*[Vː] C C[-coronal]`.**
> Dutch has very few sequences of a long/tense vowel followed by a consonant cluster whose **second
> member is non-coronal**.

Attested `VːC` and `VCC[-cor]`, banned `*VːCC[-cor]`:
*paal* [paːl] / *palm* [pɑlm] / \*[paːlm]; *stoom* / *stomp* / \*[stoːmp]; *haar* / *harp* /
\*[haːrp]; *meel* / *melk* / \*[meːlk] [kager-pater2012 p.6 ex.(2)].
Escape hatches: (i) a word-final **coronal** appendix is exempt — *taart* [taːrt] is fine;
(ii) the restriction is weakened when the final consonant begins a new syllable
[kager-pater2012 p.6, p.2]; (iii) lexical exceptions *twaalf* [tʋaːlf], *hielp*, *stierf*, *wierp*
[kager-pater2012 p.6–7]. Note this is the same generalization as "A-class vowels take at most one
coda consonant" stated from the other end.

### Other position restrictions
- **/h/ is barred from codas** entirely (it needs place from a following vowel)
  [taalportaal-codas §quickinfo (Booij 1995:40)].
- **/ŋ/ is coda-only, and only after a B-class vowel**: *ring* /rɪŋ/, *eng* /ɛŋ/, *tango* /tɑŋ.xo/.
  No A-class vowel or diphthong may be followed by /ŋ/, word-medially or word-finally
  [taalportaal-codas §quickinfo; taalportaal-coda-cooccurrence-restrictions §*A-class /
  diphthong + /ŋ/].
- **Glides in codas** only after A-class vowels, and /j/ only after back vowels (*roei* /ruj/,
  *ooi* /oj/, *aai* /aj/), /ʋ/ only after front vowels (*nieuw* /niʋ/, *uw* /yʋ/, *eeuw* /eʋ/);
  /ø/ never takes a glide. A glide may be followed only by a coronal (*ooit* /ojt/, *stoeis*
  /stujs/). Diphthongs cannot be followed by a glide at all. Loan exceptions with a B-class vowel +
  glide: *mais* /mɑjs/, *Thais*, *detail* /də.tɑj/, *boiler* /bɔj.lər/, and native *hoi* /hɔj/
  [taalportaal-coda-cooccurrence-restrictions §glides (Booij 1995:44)].
- **Diphthongs may not be followed tautosyllabically by /r/ or by either glide**: no /ɛir œyr ɑur/,
  no diphthong + /j ʋ/. Heterosyllabically /r/ is fine (*Caldeira* [ɛi.r], *Beira*)
  [taalportaal-coda-cooccurrence-restrictions §*Diphthong + /r, ʋ, j/ (Booij 1995:34)]. **Bites
  Irish directly** if /əi/ → /ɛi/ (8.3) and the next segment is /r/.
- Diphthong + consonant otherwise: freely before non-coronals and coronals alike (*eik, duim, faun, pijp,
  kuip, mijt, spruit, hout, slijk, buik, pauk*); voiced-obstruent codas surface devoiced (*tijd*
  [tɛit], *goud* [xɑut]) [taalportaal-coda-cooccurrence-restrictions Tables 2–3].
- Voiced obstruents never surface in a coda at all — see final devoicing, §3.

### Medial clusters, gemination, hiatus
- Word-medial clusters are licensed as (licit coda) + (licit onset); the Maximal Onset Principle
  assigns as much as possible to the onset [taalportaal-codas §quickinfo;
  booij1978-fonotactische § (*malkon* vs \**malrkon*)]. Word-medial coda ≤ 2 is the hard limit.
- **Gemination is domain-sensitive, not absent.** The rule as the source states it: "Dutch does not
  allow for geminate consonants **within prosodic words**"; degemination is **obligatory** there and
  **optional in larger domains**, "which means that geminates may occur in compounds or phonological
  phrases" [taalportaal-degemination §quickinfo (Booij 1995:68–69)].
  - Obligatory (within the prosodic word): *eet* /et+t/ → [et], *grootte* /ɣrot+tə/ → [ˈɣrotə],
    *zette* /zɛt+tə/ → [zɛtə], *gevoed* /ɣə+vud+d/ → [ɣəˈvut] (feeding final devoicing),
    *onmiddellijk* → [ɔˈmɪdələk] (feeding nasal assimilation)
    [taalportaal-degemination §readmore ex.1].
  - Optional (across a prosodic-word boundary): *handdoek* → [ˈhɑnduk], *tafellaken* →
    [ˈtafəlakə(n)], *plaaggeest* → [ˈplaxest]; in less frequent words the consonant is **not**
    degeminated but realized phonetically **long**: *berggeit* [ˈbɛrxːɛit]
    [taalportaal-degemination §readmore ex.2]. Minimal pair: *verassen* [vɛrɑsə(n)] vs *verrassen*
    [vɛrːɑsə(n)] [taalportaal-degemination §readmore ex.3].
  - Note also that **syllable-final devoicing does not apply** in those boundary cases: *handdoek*
    keeps [d] though *hand* alone is [hɑnt] [taalportaal-degemination §readmore].
  - Double consonant *letters* in spelling mark a preceding short vowel and are not long
    consonants (§5).
  **For a name generator:** within one generated prosodic word, never output a geminate; across a
  compound seam a geminate (or a phonetically long consonant) is legitimate.
- **Hiatus** (two adjacent heterosyllabic vowels) is licit but rare, and its first member is always
  an A-class vowel or a diphthong, since it stands in an open syllable: *chaos* /xa.ɔs/, *aorta*
  /a.ɔr.ta/, *Ephraim*, *farao* [taalportaal-hiatus-resolution §readmore ex.1]. It is resolved by a
  **transitional glide agreeing with the preceding vowel in backness and rounding** — four cases,
  not two:
  1. `∅ → [j] / V[+front, −round] __ V` — *hiaat* [hijat], *bioscoop* [bijɔskop], *creool* [krejol],
     *vijand* [vɛijɑnt].
  2. `∅ → [ʋ] / V[+back] __ V` — *Ruanda* [ruʋanda], *Boaz* [boʋɑs]. **Belgian target: [w]** (§0).
  3. `∅ → [ɥ] / V[+front, +round] __ V` — *uien* [œyɥən], *januari* [janyɥari] (Gussenhoven 1980;
     cf. Booij 1995:66).
  4. After **/a/ or schwa**, *no* transitional glide: a **glottal stop [ʔ]** is inserted instead if
     the second vowel begins the syllable carrying main stress (foot-initial); if it does not, the
     **hiatus is simply kept**.
  [all: taalportaal-hiatus-resolution §readmore ex.2–3]
  Case 1 is why Taalportaal writes *patio* [ˈpa.tsi.jo], *acacia* [a.ˈka.si.ja], *ravioli*
  [ra.vi.ˈjo.li] [taalportaal-stress-default-penultimate ex.4, 7, 8]; case 4 is why *chaos* stays
  [ˈxa.ɔs] [taalportaal-onsetless-syllables §5].

### Morpheme-structure constraints that loans may violate
Booij separates static shape-constraints (violable by loans) from active rules (not violable):
- `*[pn-` is a constraint on **native** morphemes only; *pneumatisch*, *pneumonie* keep the cluster
  and are thereby heard as foreign [booij2011-msc p.2052].
- No morpheme-internal voiced-obstruent clusters — violated by *labda* [lɑbda], *budget*; but final
  devoicing still applies without exception (*labda* never \*[lɑpta]) [booij2011-msc p.2052;
  booij1999-msc p.59].
- Word-initial `sk-` is loan-only (*scan, Skype*) [booij2011-msc p.2061–2062].
- No ambisyllabic /v z/ (the "VZ" generalization = restriction (a) above); loans *mazzel*, *puzzel*
  violate it [booij1999-msc p.57–58].
- Lexical morphemes never begin with a schwa syllable [booij1999-msc p.61].
- Lexical morphemes never begin with /pj- tj- kj-/, though the diminutive allomorphs *-pje -tje
  -kje* create them word-internally, and borrowed names *Pjotr, Tjeerd, Kjeld* have them
  word-initially [booij2011-msc p.2056]. **Relevant to §8.**

## 3. Repair strategies (loanword adaptation)

### 3.0 The three-way adaptation scale (choose one policy per strand)
Van der Sijs sets out the three pronunciations any Dutch loan may get [vandersijs1996-leenwoordenboek p.33]:
1. **Etymologische uitspraak** — approximate the source with the nearest Dutch phonemes (possibly a
   loan phoneme): *grill* [gril], *goal* [goːi̯].
2. **Vernederlandste uitspraak** — replace with ordinary native sounds, no attempt to approximate:
   *grill* [xril], *goal* [koːl], *cake* → *keek*, *coat* → *Koot*, *drugs* /g/ → [k] or [x].
3. **Spellinguitspraak** — read the spelling by Dutch letter-to-sound rules: *goal* [xoːl];
   *machine* with the final -e pronounced.
Conditioning factors named: region, education, register, analogy, word frequency, phonetic shape,
date of borrowing, and route of borrowing [vandersijs1996-leenwoordenboek p.33–34].
**Belgian bias (well attested and consequential):** Flemish speakers **nativize non-French loans
more, but French loans less**, than Netherlandic speakers [loan-kleinbreukink1999-culinair p.276];
and where they do nativize, they prefer **spelling-pronunciation** over the phonetically-nearest
repair — the [k] repair for foreign /g/ is a Netherlandic option that Flemish speakers essentially
do not use (*baguette*: Flanders [baɣɛt] 63–88%, [bakɛt] 0/96 observed)
[loan-kleinbreukink1999-culinair p.276]. Gerritsen & van Bezooijen
suggest Flemish speakers would rather use the fully foreign pronunciation than a "botched"
nativization [loan-gerritsen1995-engels p.17].

### 3.1 Illicit onset cluster
**No adult loan repair for an illicit initial cluster is attested in any source in this directory.**
That is a finding, not an omission — say so in the rule file rather than inventing one.
- Dutch onsets are permissive (three consonants, /s/+stop+liquid), so most donor onsets are simply
  licit and no repair is called for.
- **Attested option — keep it and be heard as foreign.** Loan onsets that violate a *native*
  morpheme-structure constraint survive intact: Taalportaal transcribes *pneumonie* /pnø.mo.ni/
  [pnømoˈni] and *psalm* /psɑlm/ in its CC-onset table [taalportaal-onset-clusters-2c §Examples],
  and Booij's point is that such words "betray their non-native origin", the constraint `*[pn-`
  characterizing the set of possible **native** morphemes only [booij2011-msc p.2052].
  (Booij's remark that speakers have no difficulty pronouncing *pneumatisk* is about **Norwegian**
  [booij2011-msc p.2062]; the earlier digest miscited it. Booij also notes that **English** repairs
  /pn-/ to /n/ — Dutch does not [booij2011-msc p.2052].)
- **(design fallback) — delete one member.** Not attested for adult loans. The only Dutch evidence
  for *which* member goes is child-language cluster reduction [twpl-clusterreduction §Introduction], which is
  acquisition data, not loan data. If the strand needs a deterministic repair, this is a policy
  choice to be made and labelled, not a rule this digest can supply.
- **(design fallback) — epenthesize into the onset.** No Dutch source here attests it at all.
- Attested change to an onset: `/ɡr/ → /xr/` in *grotte* → *grot* [xrɔt]; `/ɡ/ → /ɣ/` in *cigarette*
  → *sigaret* [siːɣaːrɛt] [wold-dutch, `infra/wold-dutch-loanpairs.tsv`; van der Sijs's
  Netherlandic transcription — Belgian keeps /ɣ/ in both].

### 3.2 Illicit coda cluster
- **Schwa epenthesis** is the attested Dutch repair, and it is a live phonological rule, not a
  historical residue. Stated as the source states it:

  > `∅ → ə / C1 __ C2` where C1 C2 form a **complex coda**, C1 is the sonorant **/l/ or /r/**, and
  > C1 and C2 are **non-homorganic** (do not share place of articulation).
  > [taalportaal-schwa-epenthesis-deletion §quickinfo, closing sentence]

  **It is optional**, and register-graded: the source calls it "a common phenomenon … especially in
  less-formal registers" and writes every example with the schwa in parentheses
  [taalportaal-schwa-epenthesis-deletion §quickinfo]. **Domain: within one coda** (tautosyllabic)
  [devoic-schwa-mpi §Introduction].
  Full example list as printed: *kalm* [kɑl(ə)m], *arm* [ɑr(ə)m], *help* [hɛl(ə)p], *harp*
  [hɑr(ə)p], *herfst* [hɛr(ə)fst], *elf* [ɛl(ə)f], *melk* [mɛl(ə)k], *werk* [ʋɛr(ə)k], *alg*
  [ɑl(ə)x], *erg* [ɛr(ə)x], ***urn* [ʏr(ə)n], *hoorn* [hor(ə)n]**
  [taalportaal-schwa-epenthesis-deletion §quickinfo ex.1]. Note the last two: C2 **is coronal**
  there, and the rule still applies, because /r/ and /n/ are not homorganic in the relevant sense —
  a `C[-coronal]` formulation would wrongly block them.
  It applies after **both /l/ and /r/**, though it is empirically commoner after /l/
  [devoic-warner2001-epenthetic-schwa p.397].
  **Two independent blocks:**
  1. **Homorganic C1 C2** — *hals* [hɑls] never \*[hɑləs]; *damp* [dɑmp] never \*[dɑməp]
     [taalportaal-schwa-epenthesis-deletion §General information; devoic-schwa-mpi §Introduction].
  2. **C2 is the coronal obstruent /s/ or /t/** — *hart* [hɑrt] \*[hɑrət], *hars* [hɑrs]
     \*[hɑrəs], *halt* [hɑlt] [taalportaal-schwa-epenthesis-deletion §General information ex.2
     (Booij 1995:127f.)]. This is the appendix effect of §2: no schwa inside a consonant + appendix
     sequence — *kaft* [kɑft] \*[kɑfət], *paard* [paːrt] \*[paːrət], and *herfst* is [hɛr(ə)fst]
     but never \*[hɛrfəst] [taalportaal-codas §An alternative account, figure 3].
  **Belgian note:** schwa epenthesis is reported as *more* prominent in Flanders than in the western
  Netherlands [devoic-jansen2021-schwa p.7, citing Sebregts 2014, Kloots et al. 2009].
- **Historical loans show a schwa in the corresponding position**: French *ministre* → *minister*
  [miːnɪstər]; Latin *templum* → *tempel* [tɛmpəl]; Latin *fenestra* → *venster* [vɛnstər]
  [wold-dutch, `infra/wold-dutch-loanpairs.tsv`, van der Sijs's Netherlandic transcription].
  **Caveat: WOLD supplies the orthographic donor form and the Dutch IPA only — no donor
  pronunciation.** That these pairs arose by *synchronic* schwa epenthesis rather than by centuries
  of independent development is an **inference**, and the `epenthesis` tag on those rows in
  `attested.tsv` is labelled accordingly.
- **English syllabic sonorants become /ə/+C**: *single* /ˈsɪŋɡl/ → [sɪŋɡəl]
  [loan-vandijk-toename p.26].

### 3.3 Three-consonant sequences
Word-finally, three and more consonants are licit if the extra ones are coronal obstruents
(appendix): *herfst*, *promptst* [taalportaal-codas §quickinfo]. So most long donor codas need no
repair at all, provided the surplus consonants are coronal obstruents.

**Dutch /t/-deletion exists but its attested scope is narrow, and it is a native morphological /
casual-speech process, not a loan repair.** As the source states it:
- **obligatory** in diminutives formed on an obstruent-final stem — *klachtje* /klɑxtjə/ [klɑxjə],
  *marktje* /mɑrktjə/ [mɑrkjə], *kastje* /kɑstjə/ [kɑʃjə] — and before the suffixes *-s* and *-st*
  when they form one prosodic word — *echtst* /ɛxtst/ [ɛxst], *lichts* /lɪxts/ [lɪxs]
  [taalportaal-casual-speech §Consonant deletion ex.9];
- **blocked after a sonorant** — *tandje* /tɑndjə/ [tɑntjə] \*[tɑnjə], *hemdje* [hɛmtjə] \*[hɛmjə]
  [taalportaal-casual-speech §Consonant deletion ex.9];
- **optional** in compounds (*herfstkleuren*, *zichtbaar*, *marktplein*, more often in frequent
  words) and across phrase boundaries, where the following segment grades it: a following plosive
  triggers it most, then nasal, then liquid/glide, least before a pause [taalportaal-casual-speech §Consonant deletion ex.10–11
  (Goeman 1999)].
Also /xts/ → /xs/ in coda simplification [codaclusters-nl-af §Dutch coda clusters].
**(design fallback)** Extending /t/-deletion — or any deletion — to an arbitrary illicit donor CCC
sequence is **not licensed by these sources**; the environments above are all morphological or
phrasal. If the strand needs it, mark it as a policy choice.

### 3.4 Absent segment → substitute

| Source segment | Belgian Dutch substitute | Attested example | Citation |
|---|---|---|---|
| /g/ | **/ɣ/** (etymological/spelling route) or kept as loan [g]; **[k] was not observed at all in these Belgian samples** | *garage, garderobe, yoga* fully nativized to /ɣ/; *baguette* Flanders [baɣɛt] 63–88%, [bakɛt] **0/96 observed**; *spaghetti* Flanders young speakers 100% native /ɣ/; *drugs* Flanders 14/15 spelling-/ɣ/, 1/15 [k] | [loan-posthumus1988-uitspraak §a; loan-kleinbreukink1999-culinair p.276; loan-gerritsen1995-engels p.16] |
| /θ/ | /t/ | *thinner* → *tinner* | [loan-posthumus1988-uitspraak §repertoire] |
| /ð/ | /d/ | *the* → *de* | [loan-posthumus1988-uitspraak §aanpassingsrepertoire] |
| /dʒ/ | /ʃ/ ("sj"), or /j/ in established words, or /ts/ finally | *jam* → *sjem*; *joker, jumbo, jumper* with /j/; *bridge* → *brits* | [loan-posthumus1988-uitspraak §c–d] |
| /tʃ/ | /ʃ/ carefully, /s/ casually (final) | *match* → *mets*, *kitsch* → *kiets*; *lunch* → [lʏnʃ] | [loan-posthumus1988-uitspraak §c; wold-dutch, `infra/wold-dutch-loanpairs.tsv`] |
| /ʃ/ | kept (loan phoneme) or → /s/ finally in casual style | *douche* → *does*, *finish* → *fienis* | [loan-posthumus1988-uitspraak §b] |
| /ʒ/ | kept (loan phoneme); prescriptively → /ɣ/ | *gendarme, horloge* keep [ʒ]; *garage, bagage, intrige* with the g of *gaan* | [vandersijs1996-leenwoordenboek p.57; loan-mars1994-vreemde p.141 — prescriptive, not a measured rule] |
| /æ/ | **/ɛ/** when the word is integrated; **retained [æ]** in unintegrated tokens — conditioned by integration score, not by phonology (see CONFLICT below) | integrated: *match* = *set*, *jackpot* → [dʒɛkpɔt], *slash* → [slɛʃ], *happy* → [hɛpi] (all score 3); retained: *jam* → [dʒæmə], *superman* → [ˈsuːpəmænɑχtɪɣ], *tax* → [sœykərtæks] | [loan-posthumus1988-uitspraak §aanpassingsrepertoire; loan-vandijk-toename pp.24–33] |
| /ʌ/ | /ɑ/ **or** /ʏ/ — both attested, no conditioning stated (see CONFLICT below) | *fuck* → [fɑk], *fucking* → [ˈfɑkɪŋ]; *bubble* → [bʏblɪŋ], *multinationals* → [mʏlti-], *lunch* → [lʏnʃ], *bus* → [bʏs] | [loan-vandijk-toename pp.25,27,29; wold-dutch, `infra/wold-dutch-loanpairs.tsv`] |
| /eɪ/ | **/eː/** (Belgian monophthong) | *tape* → [tep], *fake* → [fekə], *race* → [res] | [loan-vandijk-toename pp.24,32] |
| /oʊ/ | **/oː/** | *show* → [ʃo], *download* → [lodə] | [loan-vandijk-toename pp.24,25] |
| /iː uː/ | shortened to /i u/ | *groupies* → [ɡrupiz], *issue* → [ɪʃu] | [loan-vandijk-toename pp.26,31] |
| French /y/ | kept /y(ː)/ in learned loans; older loans → /œy/ | *communie* [kɔ.ˈmy.ni]; *juste* → *juist* [jœyst], *flûte* → *fluit* [flœyt] | [taalportaal-stress-loanwords; wold; nagy2008-frans §3.1.1] |
| French nasal vowels | **word-specific, not categorical.** Belgian speakers have a much larger nasal-preserving set than Netherlandic ones, but both denasalize a substantial set (to [ɑn ɔn ɛn ʏm]) | nasal preferred in the South, denasalized in the North: *parfum* B [pɑrfˈœ̃] 95% vs N [pɑrfˈʏm] 87%; *entrecôte, entree, ensemble, élan*. Nasal in **both**: *croissant*. Denasalized in **both**: *plafond, campagne, restaurant*. Counts: 5 words with a clear nasal preference in the North vs 39 in the South | [nagy2008-frans §3.2.1; loan-theissen2006-nasalen §1–3] |
| unstressed English /ə/ | restored to a full vowel from spelling **in the two tokens observed**; not established as a general rule | *tattoo* [tə'tu:] → [tɑtu:]; *community* [kə'mju:nəti] → [kɔmjunɪti] | [loan-vandijk-toename pp.24,27] |
| English post-vocalic /r/ | restored from spelling (Dutch is rhotic) | *porno* ['pɔ:noʊ] → ['pɔrno]; *to trigger* → [ɣətrɪɣərd] | [loan-vandijk-toename pp.24,29] |

**Making the variable rows executable.** Where the sources support conditioning, it is given; where
they do not, the decision is flagged rather than made.

- **Integration score is the one conditioning factor the data actually give.** Van Dijk scores every
  token 1–3 for degree of integration, and the substitutions cluster by score, not by segment: the
  score-3 tokens show /æ/→/ɛ/, /eɪ/→/eː/, /oʊ/→/oː/, length loss and Dutch verbal morphology, while
  the score-2 tokens are reproduced with English phonology intact (*core business*, *I owe you*,
  *charter schools*) [loan-vandijk-toename pp.24–33]. **Executable form: choose an integration level
  for the strand, then apply the whole substitution set or none of it** — do not mix.
- `CONFLICT: /æ/.` Integrated tokens give /ɛ/; unintegrated tokens keep [æ]; Dutch has no /æ/ in its
  native inventory. Posthumus states the merger as a rule ("*match* and *set* have the same vowel")
  [loan-posthumus1988-uitspraak §aanpassingsrepertoire], and van Dijk's corpus shows both outcomes
  [loan-vandijk-toename pp.24–33]. **Decision:** for a fully nativizing strand, /æ/ → /ɛ/. Not
  decided here.
- `CONFLICT: /ʌ/.` /ɑ/ (*fuck* → [fɑk]) and /ʏ/ (*bubble, lunch, bus*) are both attested and no
  source states a conditioning environment. Note only that the /ʏ/ cases are the older, fully
  established loans and the /ɑ/ cases are recent interjections. **Not decided here.**
- `CONFLICT: foreign /g/.` Belgian data give /ɣ/ (spelling route) and retained [g] as the live
  options and show [k] essentially unused in Flanders (0/96 for *baguette*, 1/15 for *drugs*)
  [loan-kleinbreukink1999-culinair p.276; loan-gerritsen1995-engels p.16]. Say "not observed in
  these Belgian samples" rather than banning [k]; the samples are small and word-specific.
- `CONFLICT: French nasal vowels.` Word-specific in both varieties (row above). An executable rule
  must be either lexical (a word list) or a blanket policy. **Not decided here.** For Irish input
  the question is moot — Irish has no nasal vowels — so this row matters only if the strand borrows
  French-shaped material.
- **Vowel length**: see §3.6, which is a proposed policy, not a sourced rule.

### 3.5 Word-edge processes
- **Final devoicing** — an *active rule* (as opposed to the violable morpheme-structure constraints
  of §2), and the sources show it applying to loans; note the source's own wording is the weaker
  "voiced obstruents are generally not found in syllable-final position", and the
  incomplete-neutralization literature reports small phonetic residues
  [taalportaal-final-devoicing §quickinfo, §Incomplete neutralization]:
  `/b d v z ɣ/ → [p t f s x] / __ ]σ` (**syllable**-final, not merely word-final)
  [taalportaal-final-devoicing §quickinfo]. Evidence: *hand* [hɑnt] vs *handen* [hɑndən]; *huis*
  [hœys] vs *huizen* [hœyzən]; complex codas *krabt* [krɑpt], *broeds* [bruts] [taalportaal-final-devoicing §Description ex.1–2].
  Suffix behaviour: vowel-initial suffixes and past *-de* are cohering and do **not** trigger it
  (*miljard* [mɪljɑrt] → *miljardair* [mɪljɑrdɛːr]); consonant-initial suffixes plus *-aardig*,
  *-achtig* do (*hond* [hɔnt] → *hondje* [hɔntjə]) [taalportaal-final-devoicing §The influence of suffixes, Tables 2–3].
  In loans: *headset* → [hɛːtsɛt] [loan-vandijk-toename p.27]; *rose* → *roos* [roːs]
  [wold-dutch, `infra/wold-dutch-loanpairs.tsv`]; and **English final voiced obstruents are devoiced
  with the vowel held long**: *cruise* → [kruːs], contrasting native *kroes*
  [loan-posthumus1988-uitspraak §aanpassingsrepertoire]. Counter-case to keep in view: *groupies* is
  transcribed [ɡrupiz] with a voiced final [loan-vandijk-toename p.26], so unassimilated (score-2/3)
  loans can escape the rule in running speech.
  Neutralization is phonetically incomplete (~3.5 ms of vowel duration)
  [taalportaal-final-devoicing §Incomplete neutralization].
- **Voice assimilation** — two rules, and the direction depends on the *manner* of the second
  obstruent [zonneveld1994-overzicht p.4–5]:
  - **Progressive (fricative devoicing):** if C2 is a **fricative**, the whole cluster is voiceless.
    *strafzaak* → [ˈstrɑfsak]; *huisvuil* /hœyz.vœyl/ → [ˈhœysfœyl].
  - **Regressive (RVA):** if C2 is a **plosive**, its [voice] value spreads leftward.
    *stropdas* → [ˈstrɔbdɑs]; *zesde*; *ijkpunt* [ˈɛikpʏnt] (voiceless C2, no voicing).
  - Ordering: final devoicing feeds progressive assimilation — *rondvaart* /rɔnd+vaːrt/ → [ˈrɔntfaːrt]
    [devoic-grijzenhout-roa303 pp.2–8].
  - **Sonorants and vowels never trigger RVA**: *zandloper* [ˈzɑntlopər] [taalportaal-voice-assimilation §RVA ex.4].
  - **RVA applies to loans and overrides source-language clusters**: *Lesbos* → [ˈlɛzbɔs], *asbest*
    → [ˈɑzbɛst] [taalportaal-voice-assimilation §RVA ex.3]. Also tautosyllabic stop+fricative goes the other way: *goeds* → [ɣuts]
    [booij1979-syllabe p.548–549].
- **Nasal place assimilation:** `[+nas] → [α place] / __ [α place, −son]`, obligatory
  morpheme-internally; across boundaries **only /n/ assimilates**, never /m/ or /ŋ/.
  *baanbrekend* [bambrekənt], *bruinkool* [brœyŋkol], *bronwater* [brɔɱʋatər]; but *boomstam*,
  *hangmat* unchanged [taalportaal-nasal-assimilation §quickinfo, ex.7–9].
- **/n/-deletion:** `n → ∅ / ə __ ]σ` — obligatory in the western Netherlands, variable elsewhere:
  *regen* [ˈreɣə(n)], *molen* [ˈmolə(n)] [taalportaal-n-deletion §quickinfo]. Treat as optional for
  Belgian ("not covered" for Flanders specifically).
- **Initial glottal stop** before a vowel-initial stressed syllable (§2, and Verhoeven for Belgian).
- **Final-vowel addition and prothesis: not covered.** Neither is described in any of the loanword
  sources read for this digest (`loan-posthumus1988-uitspraak`, `loan-theissen2006-nasalen`,
  `loan-gerritsen1995-*`, `loan-kleinbreukink1999-culinair`, `vandersijs1996-leenwoordenboek`
  ch. "De uitspraak van leenwoorden", `nagy2008-frans`, `loan-vandijk-toename`). Given Dutch's
  permissive onsets and codas neither would be expected, but that is reasoning, not a citation —
  treat as `(unattested)`.

### 3.6 Vowel adaptation
- `CONFLICT: what happens to donor vowel length.` **(proposed policy, not a sourced rule)** The
  digest's proposal is: donor length is reinterpreted as the **tense/lax (A/B class)** distinction,
  and where the two §2 restrictions apply, the coda decides the class. Evidence *for*: French /a/ in
  *calme, palme* surfaces as Dutch **lax** /ɑ/ before the non-coronal cluster — *kalm* [kɑlm],
  *palm* [pɑlm] — exactly what `*[Vː]CC[-cor]` predicts [wold-dutch,
  `infra/wold-dutch-loanpairs.tsv`; kager-pater2012 p.6]. Evidence *against* a categorical rule:
  these are medieval loans and WOLD gives no donor pronunciation, so the mechanism is inferred; and
  the modern data show competing outcomes for the *same* word class (*team, pool, keeper* have both
  long-loan-vowel and short-native-vowel pronunciations [loan-posthumus1988-uitspraak §e–f];
  *slow motion* monophthongizes its first /oʊ/ and keeps its second; *no way* keeps /eɪ/
  [loan-vandijk-toename pp.26,31]). **A strand policy must be chosen; this digest does not choose.**
- English long vowels shorten (*groupies* [ɡrupiz], *issue* [ɪʃu]); English diphthongs /eɪ oʊ/
  monophthongize to /eː oː/ [loan-vandijk-toename pp.24–32].
- Loan-vowel length is itself a choice point: *team, pool, keeper, corner, partner* have competing
  long-loan-vowel and short-native-vowel pronunciations [loan-posthumus1988-uitspraak §e–f].
- Unstressed reduced vowels in the donor are typically **restored from spelling**, not kept as schwa
  (§3.4).
- French final /e/ can be reinterpreted as the diphthong /ɛi/: *vallée* → *vallei* [vɑlɛi] [wold-dutch, `infra/wold-dutch-loanpairs.tsv`; process inferred].
- Hiatus in the donor gets a glide: *maíz* → *maïs* [mɑjs] [wold-dutch, `infra/wold-dutch-loanpairs.tsv`; process inferred —
  WOLD gives no Spanish pronunciation].

### 3.7 Anything else
- **Gemination: obligatorily degeminated within a prosodic word, optional across a
  compound/phrase boundary** (§2, degemination) [taalportaal-degemination §quickinfo].
- **Metathesis: not covered** by any source in this directory.
- Loans are permitted to keep foreign shapes and simply be heard as foreign; the MSCs in §2 are
  violable, active rules are not [booij2011-msc p.2052]. This is a **policy decision** for the tool:
  a "full nativization" mode applies every rule; a "Belgian-realistic" mode leaves French-shaped
  material (nasal vowels, /ʒ/) alone.

## 4. Stress and length

**Vowel-length contrast: present but reinterpretable.** Belgian has phonetically long /aː eː oː yː
øː/ vs short /ɑ ɛ ɔ ʏ ɪ/ and phonetically short high tense /i y u/ [verhoeven2005 p.245;
kager-pater2012 p.7]. Phonologically the productive contrast is **tense (A-class) vs lax
(B-class)**, and it is the A/B distinction — not duration — that drives the phonotactics in §2 and
the stress weight scale below.

**Generalizations** (Kager 1989's set as tabulated by Taalportaal; none exceptionless)
[taalportaal-stress-generalizations §Major/Minor generalizations]:
1. **Three-syllable window (strong):** primary stress falls within the last three syllables.
   *economie* [e.ko.no.ˈmi], *macaroni* [ma.ka.ˈro.ni], *magnolia* [max.ˈno.li.ja];
   \*[ˈta.rɑn.ty.la]. Exceptions: some toponyms and Latin grammatical terms — *Wageningen*
   [ˈʋa.ɣə.nɪŋ.ə(n)], *Scheveningen*, *infinitief* [ˈɪn.fi.ni.tif]
   [taalportaal-stress-three-syllable-window §General information].
2. **Schwa is never stressed**, and primary stress falls **immediately before** a schwa syllable:
   *palissade* [pa.li.ˈsa.də], *mirakel* [mi.ˈra.kəl].
3. **Closed penult restriction (strong):** primary stress cannot be on the antepenult if the penult
   is closed and contains a full vowel. *agenda* [a.ˈɣɛn.da], \*[ˈa.ɣɛn.da]; *rododendron*
   [ro.do.ˈdɛn.drɔn] [taalportaal-stress-closed-penult-restriction].
4. **A superheavy final syllable takes primary stress (strong):** *avontuur* [a.vɔn.ˈtyr],
   *serpentijn* [sɛr.pɛn.ˈtɛin], *document* [do.ky.ˈmɛnt].
5. **A final diphthong takes primary stress (strong):** *batterij* [bɑ.tə.ˈrɛi], *lakei* [la.ˈkɛi].
6. **A final closed B-class syllable → antepenultimate stress (weak):** *albatros* [ˈɑl.ba.trɔs],
   *carnaval* [ˈkɑr.na.vɑl].

**Superheavy** = rhyme containing at least (A-class vowel + C), (diphthong + C), or (B-class vowel +
CC); further consonants may follow but only coronal obstruents. Superheavy syllables occur only
word-finally and are strong stress attractors
[taalportaal-stress-superheavy-syllables §quickinfo].
**Weight scale** (light → heavy): schwa ≪ A-class/diphthong ≪ B-class+C ≪ B-class+CC ≪
A-class/diphthong+C — i.e. V ≪ VV ≪ VC ≪ VCC ≪ VVC. Note VV is *lighter* than VC in Dutch, which is
typologically odd and is why quantity-sensitivity is contested
[taalportaal-stress-quantity-sensitivity §readmore (Van der Hulst 1984)].
**Default:** penultimate, most clearly in disyllables of shape A-A (136/165 in CELEX)
[taalportaal-stress-default-penultimate §Disyllabic words]. In monomorphemic words it is
"usually the right-most stressable syllable that carries primary stress"
[taalportaal-stress-primary-simplex §quickinfo].

### The practical rule — **constructed by this digest from the tendencies above, not stated by any source**
Taalportaal grades its generalizations strong / solid / weak and warns that "none of these
generalizations are exceptionless" [taalportaal-stress-generalizations §quickinfo]; the ordering
below is the digest's reading of which tendency wins where the source's own tables conflict. Treat it
as a default that the user may override, not as an attested algorithm.
1. If any syllable contains schwa, it is unstressable; prefer the syllable immediately before it.
2. If the **final** syllable is superheavy (A-vowel/diphthong + C(+coronals), or B-vowel + CC) or
   ends in a diphthong → **stress the final syllable**.
3. Else if the **penult** is closed and has a full vowel → **stress the penult** (never skip it).
4. Else if the final syllable is a closed B-class syllable → **stress the antepenult** (weak
   tendency; a French-shaped word may instead take final stress).
5. Else → **stress the penult** (default).
6. Never stress outside the last three syllables.
Worked: *avontuur* [a.vɔn.ˈtyr] (rule 2) · *agenda* [a.ˈɣɛn.da] (rule 3) · *albatros*
[ˈɑl.ba.trɔs] (rule 4) · *arena* [a.ˈre.na], *avocado* [a.vo.ˈka.do] (rule 5) · *mirakel*
[mi.ˈra.kəl] (rule 1) [examples all from taalportaal-stress-*].
Secondary stress alternates from the primary outward (Alternating Stress Principle / Hammock
Principle) [taalportaal-word-stress §Secondary stress — headings only; detail not extracted].

### Loanword stress
"The large majority of loanwords follow the stress pattern of the source language"
[taalportaal-stress-loanwords §quickinfo]. Systematic exception: French words in *-ion* → Dutch
*-ie* take **penultimate** stress instead of final: *ad.mis.'sion* → *admissie* [ɑt.ˈmɪ.si];
*am.bi.'tion* → *ambitie* [ɑm.ˈbi.tsi]. But French *-ie* words keep final stress
(*anarchie* [ɑ.nɑr.ˈxi], *economie* [e.ko.no.ˈmi]), and Latin-derived *-ie* words keep Latin
penultimate stress (*academie* [ɑ.ka.ˈde.mi], *tragedie* [tra.ˈɣe.di]) [taalportaal-stress-loanwords Tables 1–3].
Impressionistic ongoing shifts, mostly **towards the penult**: *democratie* → [de.mo.ˈkra.si],
*parfum* [pɑr.ˈfʏm] → [ˈpɑr.fʏm], *catalogus* → [ka.ta.ˈlo.ɣʏs], *pagina* → [pa.ˈɣi.na]
[taalportaal-stress-loanwords Tables 4–5]. **Belgian**: van der Sijs notes Southern Dutch **retracts** stress in French
words where Northern Dutch does not (*pyjama*, *torpedo*), and that a word may be an English loan
with initial stress in the North and a French loan with final stress in the South (*detective*,
*recital*) [vandersijs1996-leenwoordenboek p.60].

### OPEN DECISION — precedence between Irish source stress and the Dutch procedure
Irish input arrives with stress already marked (*Ciara* /ˈkɪə.ɾˠə/, *Matánach* /ˈmˠat̪ˠɑːnˠəx/), and
Irish stress is initial. Dutch, applied to those forms, would often move it. This choice changes
every output, so it is left to the user. The evidence on each side:
- **Keep the Irish stress.** This is what Dutch actually does with most loans: "the large majority of
  loanwords follow the stress pattern of the source language"
  [taalportaal-stress-loanwords §quickinfo]. Van Oostendorp goes further and argues the
  three-syllable window itself is a *diachronic residue of loanword adaptation* rather than a live
  Dutch rule, precisely because donors (Latin, French, Italian) already obeyed it
  [taalportaal-stress-three-syllable-window §Debate (Van Oostendorp 2012)]. Initial stress is
  Dutch-legal in a great many native words. Cost: the strand will not *sound* rule-governed by
  Dutch, only filtered by it.
- **Re-stress by the Dutch procedure.** Attested for a systematic sub-case (French *-ion* → Dutch
  *-ie*, final → penultimate: *ad.mis.'sion* → *admissie* [ɑt.ˈmɪ.si]
  [taalportaal-stress-loanwords Table 1]) and for the impressionistic ongoing shifts toward the
  penult [taalportaal-stress-loanwords Tables 4–5]. Cost: it is precisely the part of the Dutch system the sources describe
  as tendencies with counterexamples.
- **Hybrid (the digest's suggestion, undecided):** keep Irish stress by default, but let the two
  *strong* Dutch generalizations override it — schwa can never be stressed, and a word-final
  superheavy syllable or final diphthong attracts stress. Under this, *Matánach* keeps initial
  stress; a coined form ending in a superheavy syllable would not. Older Latin loans show retraction to the first
syllable (*bekken*); younger French loans keep final/penultimate stress (*bassin*)
[vandersijs1996-leenwoordenboek, "De uitspraak van leenwoorden"].

## 5. Romanization

### OPEN DECISION — which output convention
The project brief asks for "a per-target romanization an English reader can pronounce approximately
right" [project-goals.md §What each per-language rule file needs]. Native Dutch orthography does
**not** meet that on its own: an English reader will misread ⟨g ch sch ij ei ui eu oe u w⟩ (list
below). Two workable conventions, both left to the user:
- **(a) Authentic Dutch spelling + a pronunciation key.** Maximum in-world plausibility; the names
  look Dutch and a Dutch reader pronounces them correctly. Requires shipping a short key, since an
  English reader gets ⟨Muijs⟩ badly wrong. The Dutch precedent for this is the whole
  `wiki-nl-orthography` system below.
- **(b) A separate English-reader respelling alongside the IPA.** Dutch itself does exactly this
  when it writes foreign sounds for its *own* readers — ⟨sj zj tsj⟩ for /ʃ ʒ tʃ/ in *Chroesjtsjov*,
  *Sjostakovitsj* — under the stated design goal that "the intuitive pronunciation of an arbitrary
  Dutch-speaking reader approximates the correct pronunciation as closely as possible"
  [names-wiki-translit §Uitgangspunten; vandersijs1999-transcriptie §Transcriptie]. The mirror-image
  convention for an English reader would be a genuine Dutch practice applied in the other direction.
Both need the same two tables. §5 supplies them; it does not choose.

### Phoneme → spelling (native/nativised vocabulary)
Consonants [wiki-nl-orthography §Sound to spelling correspondences]:
`p`→p · `b`→b (final ⟨b⟩ = [p]) · `t`→t · `d`→d (final ⟨d⟩ = [t]) · `k`→k · `ɣ`→g (final ⟨g⟩ = [x])
· `x`→ch · `f`→f · `v`→v (never final) · `s`→s · `z`→z (never final) · `ɦ`→h (never final) ·
`m`→m · `n`→n · `ŋ`→ng · `l`→l · `r`→r · `w`(/ʋ/)→w (never final) · `j`→j (never final) ·
`sx`→sch (word-finally ⟨sch⟩ = /s/) · `t`→th in loans.
Vowels — **checked (closed syllable) vs free (open syllable)**:

| Sound | Checked spelling | Free spelling | Example |
|---|---|---|---|
| /ɑ/ | a | — | *man* |
| /aː/ | aa | a | *maan* / *manen* |
| /ɛ/ | e | — | *bed* |
| /eː/ | ee | e | *leek* / *leken* |
| /ɪ/ | i | — | *lip* |
| /i/ | ie | ie | *dief* / *dieven* |
| /ɔ/ | o | — | *bon* |
| /oː/ | oo | o | *boon* / *bonen* |
| /ʏ/ | u | — | *mus* |
| /y/ | uu | u | *muur* / *muren* |
| /u/ | oe | oe | *boek* |
| /øː/ | eu | eu | *deur* |
| /ə/ | e (unstressed) | e | *de*, *-en* |
| /ɛi/ | ei, ij | | *lei*, *lijn* |
| /œy/ | ui | | *lui* |
| /ɔu/ | ou(w), au(w) | | *koud*, *lauw* |

[wiki-nl-orthography §Sound to spelling correspondences; §Morphological alternations]

### The doubling algorithm (state it exactly this way in the generator)
1. Syllabify. A vowel in an **open** syllable (no coda) is long/tense; in a **closed** syllable it is
   short/lax.
2. To write a **long** vowel in a closed syllable, **double the vowel letter** (*maan*, *boon*,
   *muur*); in an open syllable write it **single** (*ma-nen*, *bo-nen*, *mu-ren*).
3. To keep a **short** vowel before a single intervocalic consonant, **double the consonant letter**
   (*lat* → *lat-ten*, *bon* → *bon-nen*, *mus* → *mus-sen*).
4. "The simplest representation is always chosen: a double vowel is never written in an open
   syllable, and a double consonant is never written at the end of a word or next to another
   consonant" [wiki-nl-orthography §Exceptions].
5. Double consonant letters are **not** long consonants (§2: no gemination).
6. Compounds are spelled as if each member were written separately, which can look like a violation:
   *dag-arbeider*, not \**daggarbeider* [wiki-nl-orthography §Exceptions].

### Devoicing is not written
Final devoicing is never shown: *heb* [ɦɛp], *paard* [paːrt], *leg* [lɛx]
[wiki-nl-orthography §Final devoicing]. For invented names this is a **choice**: spell etymologically
(⟨-d⟩, read [t]) or phonetically (⟨-t⟩). Recommend phonetic spelling for names, since there is no
paradigm to recover the voiced form from.

### Where an English reader will go wrong
- ⟨g⟩ = /ɣ/ (Belgian *zachte g*), never English /dʒ/ or /g/; ⟨ch⟩ = /x/; ⟨sch⟩ = /sx/ initially but
  /s/ finally.
- ⟨ij⟩ and ⟨ei⟩ = /ɛi/, not /iː/ or /eɪ/.
- ⟨ui⟩ = /œy/ — no English equivalent at all.
- ⟨oe⟩ = /u/, ⟨u⟩ = /ʏ y/, ⟨eu⟩ = /øː/, ⟨ou/au⟩ = /ɔu/.
- ⟨w⟩ = a labial approximant, ⟨v⟩ = /v/, ⟨j⟩ = /j/.
- Single vs double vowel letters carry the whole length contrast (rule above).
- ⟨e⟩ in an unstressed syllable = schwa.
[wiki-nl-orthography §Sound to spelling correspondences]

### Spelling foreign sounds — the Dutch precedent
Loanwords usually keep their original spelling (*cadeau*); ⟨c, qu, x, y⟩ are *sometimes* adapted to
⟨k, kw, ks, i⟩ [wiki-nl-orthography §Loanwords]. For foreign *sounds*, Dutch transcription practice
writes them out with native digraphs — ⟨sj⟩ for /ʃ/, ⟨zj⟩ for /ʒ/, ⟨tsj⟩ for /tʃ/, ⟨dzj⟩ for /dʒ/,
⟨ch⟩ for /x/, ⟨j⟩ for /j/ — as in *Chroesjtsjov*, *Sjostakovitsj* [vandersijs1999-transcriptie;
names-wiki-translit — the nl.wikipedia Russian and Ukrainian tables give ж→zj, ш→sj, ч→tsj, е→je].
The nl.wikipedia guide's stated design goal is exactly ours: that "the intuitive pronunciation of an
arbitrary Dutch-speaking reader approximates the correct pronunciation as closely as possible"
[names-wiki-translit; as summarised in bib.md].
There is also a sanctioned **spelling-pronunciation** route for names: *cornedbeef* → *kornetbief*
[names-wiki-spellinguitspraak §Buitenlandse namen].

## 6. Morphology usable for epithets

| # | Form | Meaning | Attachment condition | Example | Productive? |
|---|---|---|---|---|---|
| 1 | **-je** (diminutive, default) | 'small, endearing'; output is always a **neuter** noun with plural *-s* | after most obstruents | *lief* → *liefje*, *dut* → *dutje*, *uit* → *uitje* | "very productive" [booij2014-word-formation p.14] |
| 2 | **-tje** | same | after a sonorant (/n l r/ or a glide) preceded by an A-class vowel, diphthong or schwa; also after vowels | *traan* → *traantje* [ˈtrantjə], *deken* → *dekentje*, *druppel* → *druppeltje*, *werker* → *werkertje*, *vrouw* → *vrouwtje* | yes [taalportaal-nasal-assimilation §Nasal assimilation and the diminutive morpheme (Trommelen 1984:8); taalportaal-coda-cooccurrence-restrictions Table 6] |
| 3 | **-pje** | same | after /m/ preceded by an A-class vowel, diphthong or schwa (the stop is homorganic with the nasal) | *boom* → *boompje* [ˈbompjə], *Mokum* → *Mokumpje*, *riem* → *riempje* | yes [taalportaal-nasal-assimilation §Nasal assimilation and the diminutive morpheme (Trommelen 1984:8); booij2011-msc p.2056] |
| 4 | **-etje** (i.e. -ətjə, with the stem consonant doubled) | same | after a sonorant preceded by a **B-class (lax) vowel** | *ram* → *rammetje*, *man* → *mannetje*, *bal* → *balletje*, *kar* → *karretje*, *rang* → *rangetje* | yes [taalportaal-coda-cooccurrence-restrictions Table 6] |
| 5 | **-kje** | same | after /ŋ/ preceded by unstressed /ɪ/ (competes with *-etje*) | *koning* → *koningkje* [ˈkonɪŋkjə]; *wandeling* → *wandelingetje* | yes; "selection also depends on the stress pattern, and there is dialectal variation" [taalportaal-nasal-assimilation §same] |
| — | note | | a stem-final /t d/ + *-je* surfaces with a **palatal stop**: *bootje* [boːcə], *paardje* [paːʀcə]; a stem-final /n/ + *-tje* gives [ɲc]: *landje* [lɔɲcə] | | [verhoeven2005 p.244] |
| 6 | attributive **-e** [ə] on adjectives | agreement | on any attributive adjective **except** before an indefinite singular **neuter** noun; never in the predicate | *de mooi-e fiets*, *het mooi-e huis*, *koud-e soep* — but *een mooi huis*, *koud water*, *De soep is koud* | fully productive [wiki-nl-language §Grammar] |
| 7 | genitive **-s / -'s / -'** | possessive, on **proper names** (nouns and adjectives are otherwise uninflected for case) | proper names | *Jans*, *Anna's* | productive [wiki-nl-language §Grammar] |
| 8 | **-ig**, **-lijk**, **-achtig** | adjective from noun/adjective ('-y, -like, -ish') | N→A, A→A. Note the phonology: *-ig* is a **cohering** vowel-initial suffix, so it syllabifies with the stem and final devoicing does **not** apply (*rood* [rot] → *rodig* [rodəɣ]); *-aardig* and *-achtig* are the **two vowel-initial exceptions**, non-cohering and therefore devoicing-triggering (*goed* [ɣut] → *goedaardig* [ɣutardəx]; *rood* → *roodachtig* [rotaxtəx]) | *blauw* → *blauwig* 'bluish', *meester* → *meesterlijk* 'masterly', *superman* → *supermanachtig* | productive [booij2014-word-formation p.13; taalportaal-final-devoicing §The influence of suffixes, Tables 2–3; loan-vandijk-toename p.24] |
| 9 | **-er** (allomorphs *-der*, *-aar*, *-enaar*) | agent / inhabitant | V→N mainly; *-enaar* on place names (*Utrecht* → *Utrechtenaar*) | *werk* → *werker*, *wandel* → *wandelaar*, *Langweer* → *Langweerder*, *stad* → *stedeling* | productive [booij2014-word-formation p.15–16] |
| 10 | linking **-s-** / **-en-** in compounds | none (junctural) | between compound members; not rule-predictable, but a coined compound tends to copy the linking element of an analogous one | *dorp-s-gek* 'village idiot', *scheid-s-rechter*, *lerar-en-kamer* | semi-productive [booij2014-word-formation p.11–12] |

**Not covered:** the family-name elements *-sen*, *van*, *de*, *van der*. No source in this directory
describes Dutch patronymic or surname formation; do not invent it from general knowledge.

## 7. Attested adaptations

See `attested.tsv` in this directory — **90 data rows** (plus header).

Provenance mix:
- **31 rows, English → Dutch, both sides in IPA**, transcribed off Dutch television
  [loan-vandijk-toename pp.24–33]. The best rows we have: they give the *actual realization*, not a
  dictionary norm, and carry the thesis's 1–3 integration score in the note.
- **15 rows, French/Latin → Dutch**, Dutch side in IPA with stress marked, donor side given as a
  **stress-marked orthographic form, not IPA** (`ad.mis.'sion`) [taalportaal-stress-loanwords
  Tables 1–3]. Per `ATTESTED-FORMAT.md`, `source_ipa` is therefore **blank** on these rows and the
  stress-marked form is carried in `note`. These are the stress rows.
- **20 rows from WOLD** (van der Sijs's Dutch vocabulary) — donor orthography + Dutch IPA. NB
  **bib.md and the task brief describe WOLD as orthography-only; the extracted
  `infra/wold-dutch-loanpairs.tsv` in fact carries a segmented Dutch IPA column**, so these rows
  have `target_ipa` filled. The transcription is **Netherlandic** (`ʋ`, `ɛi ɑu`, positional `ɣ/x`);
  apply the §0 normalization layer before using it. Donor side has **no IPA anywhere in WOLD**, so
  `source_ipa` is blank — and consequently **every `process` tag on a WOLD row is an inference from
  the orthographic pair, not an observation**; each such row's note now says
  `process tag inferred (WOLD gives no donor IPA)`. Most WOLD pairs are medieval French/Latin, so
  they document historical integration rather than modern loan repair
  [infra/bib.md `wold` §Caveat that matters for §7].
- **14 rows of measured survey data** (Belgian column where the study splits N/B)
  [loan-theissen2006-nasalen, loan-gerritsen1995-*, loan-kleinbreukink1999-culinair,
  nagy2008-frans]. These carry preference proportions in the note rather than a single output form.
- **9 rows from Posthumus** (+1 from names-wiki-spellinguitspraak), whose target forms are **Dutch respelling, not IPA** (*thinner* →
  *tinner*): `target_ipa` deliberately left blank and the respelling put in `target_form`
  [loan-posthumus1988-uitspraak].

**Bias to be aware of:** heavily English- and French-sourced; the English material is *recent*
borrowing, which van der Sijs says is adapted **least** [vandersijs2009-loanwords-dutch §Integration
of loanwords], so it under-represents the repairs we actually want to model. The thoroughly
nativized layer (Latin, medieval French) is what WOLD documents, but diachronically. No row in the
whole set comes from a language with a palatalization contrast.

## 8. Irish-specific mismatch notes

### 8.1 Broad (velarized) vs slender (palatalized)
Dutch has **no palatalization contrast**, and no source here documents Dutch borrowing from a
language that has one — the transliteration guides handle Russian by writing ⟨zj sj tsj je⟩ for the
*consonants* ж ш ч and the *vowel* onsets, and say nothing about ь or C ʲ
[names-wiki-translit; vandersijs1999-transcriptie]. **There is no attested precedent. State this as
a design decision, not a finding.** But there are three target-internal hooks, and they do not
point the same way:

1. **Cʲ → Cj has real support.** Dutch /Cj/ sequences surface as palatal(ized) segments across the
   board: /tj/ → [t͡ɕ] (or intervocalic [c], [ç]), /dj/ → [d͡ʑ] ([ɟ], [ʝ]), /kj/ → [c̠͡ç̠],
   /sj zj/ → [ɕ ʑ] or [ʃ ʒ], /nj/ → [ɲ], /lj/ → [ʎ]
   [wiki-nl-phonology §Consonants/Allophony]. Belgian confirms the outputs independently: [c] in
   *bootje*, [ɲ] in *landje*, [ʎ] only before /j/ [verhoeven2005 p.244–245]. And Dutch tolerates
   word-initial /pj tj kj/ in **borrowed names** specifically — *Pjotr, Tjeerd, Kjeld*
   [booij2011-msc p.2056]. So Cʲ → Cj is *pronounceable, spellable* (⟨tj sj nj lj⟩), and has name-
   shaped precedent.
   **But the phonotactics fight it:** /j/ is never the first member of an onset cluster, /Cj/ onsets
   are all marked loanword-only in the CC matrix (pj, kj, fj, vj, lj), /xj/ and /ɣj/ are outright
   banned, and **codas admit /j/ only after an A-class vowel and only before a coronal**
   [taalportaal-onset-clusters-2c; taalportaal-coda-cooccurrence-restrictions §glides]. A slender
   *coda* consonant therefore cannot become Cj at all without further repair.
2. **Broad → velarized has a Belgian phonetic hook for /l/ only.** Belgian /l/ is realized
   **velarised [lˠ]** or **post-palatalised [lʲ̠]** depending on context, and /l/ is "often slightly
   velarized postvocalically" [wiki-nl-phonology §Sonorants; verhoeven2005 p.245]. That is the Irish
   /l̪ˠ/ ~ /lʲ/ pair as allophones. It is sub-phonemic and confined to /l/; it will not generalise to
   a whole series.
3. **Depalatalize / collapse** costs nothing phonotactically and loses the contrast entirely.

**The three options, all `(design fallback)` — nothing here is attested for loan adaptation:**
| Option | Onset behaviour | **Coda behaviour (the part that is usually forgotten)** | Cost |
|---|---|---|---|
| (a) collapse | Cʲ, Cˠ → C | Cʲ, Cˠ → C | contrast wholly lost; output always Dutch-legal |
| (b) Cj in onsets, collapse in codas | Cʲ → Cj (spellable ⟨tj sj nj lj⟩; licit but loan-marked) | **must collapse**: /j/ is admitted in a coda only after an A-class vowel and only before a coronal [taalportaal-coda-cooccurrence-restrictions §glides], so a slender coda consonant cannot become Cj | asymmetric; a slender/broad pair neutralizes word-finally, which is where Irish names most often carry it |
| (c) vowel colouring | Cʲ fronts the following vowel (/ɑ/→/ɛ/, /aː/→/eː/, /oː/→/øː/, /u/→/y/); Cˠ backs it | same, on the preceding vowel | Dutch has /y yː øː/ to do it with, and it keeps the contrast audible without illegal clusters; **no source attests it**, and it will collide with the §2 vowel-class restrictions |
Note that Verhoeven's own [c ɲ ʎ] outputs and Booij's *Pjotr / Tjeerd / Kjeld* establish
**pronounceability and spellability** of option (b), not that Dutch maps a foreign palatalization
contrast onto it [verhoeven2005 p.244–245; booij2011-msc p.2056].

### 8.2 Irish segments vs Belgian Dutch

| Irish | Belgian status | Note |
|---|---|---|
| /ɣ/ | **native phoneme** | Confirmed: Belgian has voiced velar /ɣ/, absent in the Netherlands [verhoeven2005 p.244]. Maps to itself. **This is why Belgian was chosen.** |
| /x/ | **native phoneme** | Also velar, contrasting with /ɣ/ [verhoeven2005 p.244]. Maps to itself. Watch the §2(a) restriction: /x/ needs a **lax vowel or schwa** before it, never a tense vowel [taalportaal-coda-cooccurrence-restrictions Table 1]. |
| /h/ | native /ɦ/ in onsets | Belgian has /ɦ/ [verhoeven2005 p.243]. **Codas bar it absolutely**: "/h/ cannot occur in codas since it needs to receive its place specification from the following vowel" [taalportaal-codas §quickinfo (Booij 1995:40)]. What to do with an Irish coda /h/ is **`(design fallback)` and unresolved** — no Dutch source attests any repair. Options: **delete** it; **resyllabify** it as the onset of an added schwa syllable (Dutch-legal, but adds a syllable); **substitute** /x/ (Belgian has it, and it is a licit coda after a lax vowel, subject to §2(a)); or **substitute** /ɣ/ after a tense vowel. §3 supplies no attested deletion target and no movement rule, so this cannot be presented as sourced either way. |
| voiceless sonorants (Irish lenition outputs) | **absent; no precedent anywhere in this bibliography** | The only Dutch fact in the vicinity: Belgian /r/ **is** devoiced word-finally and before a voiceless stop — [doːʀ̥] *door*, [vaːʀ̥t] *vaart* [verhoeven2005 p.245]. That licenses [r̥] as a *positional allophone* in exactly those two environments, and nothing more. `(design fallback)`, unresolved: (i) map to the plain voiced sonorant (loses the contrast, always legal); (ii) map to /ɦ/ + sonorant in onsets (/ɦ/ never clusters in Dutch [taalportaal-onset-clusters-2c §readmore (Booij 1995:36)], so this produces an illegal onset — it would have to be a deliberate deviation); (iii) map to the voiced sonorant and let the *spelling* carry it (⟨hl hr hn⟩), leaving pronunciation Dutch. |
| /ɾˠ/ vs trill | **fine either way** | Belgian /r/ is an alveolar trill in free variation with a uvular trill; the alveolar is the default. Irish /ɾˠ/ and /rˠ/ both land on /r/ [verhoeven2005 p.245]. Belgian is a much better match here than Netherlandic. |
| /l̪ˠ lʲ n̪ˠ nʲ/ | one /l/, one /n/ | See 8.1. Belgian /l/ has **[lˠ] velarized and [lʲ̠] post-palatalized** realizations [wiki-nl-phonology §Sonorants], and /n/ has [ɲ] before palatals and in the diminutive [lɔɲcə] [verhoeven2005 p.244]. These are the closest thing to an Irish-style pair anywhere in the target — but they are **allophonic and phonetically conditioned**, so they support option (a)+phonetic-detail, not a contrast. |
| /w/ (lenited b/m) | native /w/ (labial approximant) | CONFLICT on its exact realization, §1. Never word-final [wiki-nl-orthography]. |
| /v/, /f/ | native | Both phonemes; but expect voiceless phonetics for /v/ (70% of initial fricatives) and obligatory devoicing word-finally [verhoeven2005 p.244]. |
| /p/ | native | No issue. |
| /ŋ/ | native but **coda-only, only after a lax vowel** | Never in an onset [taalportaal-onsets-simple §The velar nasal constraint (Booij 1995:36)]; never after a tense vowel or diphthong [taalportaal-coda-cooccurrence-restrictions §*A-class vowel / diphthong + /ŋ/]. Irish /ŋ/ after a long vowel forces a choice: lax the vowel (Dutch-legal, `(design fallback)` by analogy with *kalm*) or change the nasal. Irish word-initial /ŋ/ (from eclipsis) has **no** Dutch landing site at all. |

### 8.3 Irish vowels: length, quality, and the diphthongs

**The whole of this subsection is `(design fallback)`.** No source in this directory describes Dutch
adapting Irish, or any language with Irish's vowel system; the §3.6 CONFLICT applies here in full.
What *is* sourced is the set of Dutch-side constraints that any mapping must satisfy (§2), and those
do most of the work.

**Irish monophthong → Belgian Dutch `(design fallback)` mapping**, before the §2 constraints apply:

| Irish | nearest Belgian vowel | note |
|---|---|---|
| /iː/ | /i/ | Dutch /i/ is tense but phonetically short [kager-pater2012 p.7]; length is not contrastively available |
| /i/ | /ɪ/ | must be closed (B-class) [taalportaal-nuclei §B-class vowels] |
| /eː/ | /eː/ | direct |
| /e/ | /ɛ/ | must be closed |
| /aː/ | /aː/ | direct — but see the two §2 restrictions below |
| /a/ | /ɑ/ | must be closed |
| /oː/ | /oː/ | direct |
| /o/ | /ɔ/ | must be closed |
| /uː/ | /u/ | as /iː/ |
| /u/ | /ʏ/ **or** /ɔ/ | Dutch has no lax /u/; /ʏ/ is the attested landing site for English /ʌ ʊ/ (*bus* [bʏs], *push* → [puʃə]) [wold-dutch; loan-vandijk-toename p.27]. Unresolved |
| /ə/ | /ə/ | direct, and Dutch schwa is heavily restricted: never stressed, never word-initial in a polysyllabic lexical word, and every lexical word needs a full vowel besides it [taalportaal-nuclei §quickinfo] |

Then apply, in this order, the sourced Dutch constraints:
- **Lax vowels must be closed.** Any Irish short vowel in an open syllable must either gain a coda
  or be tensed [taalportaal-nuclei §B-class vowels].
- **`*[Vː]CC[-cor]`.** Irish long vowel + cluster whose second member is non-coronal is banned.
  Repairs: lax the vowel (French *calme* → *kalm* [kɑlm] is the historical analogue), let the last
  consonant begin the next syllable (the restriction is weakened there), or leave it if the second
  consonant is coronal — *taart* [taːrt] is licit [kager-pater2012 p.6].
- **Tense vowel + voiceless fricative is banned** (§2(a)); see the *Matánach* case below.
- **/ŋ/ only after a lax vowel**; **glides only after a tense vowel and only before a coronal**
  [taalportaal-coda-cooccurrence-restrictions].

Concretely:
- Irish long vowel + single consonant → A-class + C. Fine.
- Irish long vowel + cluster ending in a **non-coronal** → **banned** (`*[Vː]CC[-cor]`). Repair: lax
  the vowel (French *calme* → *kalm* [kɑlm] is the attested precedent), or let the final consonant
  begin a new syllable, or (if the second C is coronal) leave it — *taart* [taːrt] is licit
  [kager-pater2012 p.6; wold].
- Irish **long vowel directly followed by a voiceless fricative** (/Vːx/, /Vːf/, /Vːs/) → **banned**
  by §2(a). Three repairs, all with some support, none attested for this case:
  (i) **lax the vowel** — /ɑːx/ → /ɑx/, matching the native *lachen* /lɑxə(n)/ pattern and the
  *calme* → *kalm* historical analogue; (ii) **voice the fricative** — /ɑːx/ → /aːɣ/, legal because
  Belgian *has* /ɣ/ and tense + /ɣ/ is the *vogel* /voɣəl/ pattern; (iii) accept it as a member of
  the small genuine exception class (*goochem, sjofel, tafel, brasem*). All three are Dutch-legal.
  **`(design fallback)`; not decided here.**
  **Note (correcting bib.md): *Matánach* is not an instance of this.** Its /x/ follows the schwa of
  unstressed *-ach*, and schwa takes voiceless fricatives (§2, exception 4). Where it *does* bite is
  a stressed /Vːx/ syllable. Conversely, repair (ii) is **not available after schwa**: Table 1 gives
  no /əɣ/ [taalportaal-coda-cooccurrence-restrictions Table 1].
- **Irish /iə uə/** `(design fallback)`: Dutch has no such centring diphthongs. Two routes, neither
  attested for loans: (i) treat as **hiatus** and let Dutch's own rule insert the glide — /iə/ →
  [i.jə] (case 1 of the hiatus rule: [j] after an unrounded front vowel) and /uə/ → [u.wə] (case 2,
  which the source writes [ʋ] and which normalizes to Belgian **[w]** per §0); note this **adds a
  syllable** and the added schwa is then subject to the schwa restrictions above. (ii) Collapse to
  the tense monophthongs /i u/, losing the offglide. The hiatus rule itself is sourced
  [taalportaal-hiatus-resolution §readmore ex.2]; applying it to Irish input is not.
- **Irish /əi/ and /əu/** `(design fallback)`: Dutch /ɛi/ and /ɔu/ are the nearest segments in the
  whole inventory — Verhoeven's *lei* [lɛi], *lauw* [lɔu] [verhoeven2005 p.245] — and Dutch
  diphthongs are B-class + A-class sequences, i.e. schwa-ish first element
  [taalportaal-nuclei §Diphthongs], so the fit is close. But **the source says only that /ɛi œy ɔu/
  exist**; it says nothing about Irish or about adapting schwa-initial diphthongs. Treat the mapping
  as a well-motivated design decision, not an attested one. Dutch has no /ai/ or /oi/ except as loan
  diphthongs licensed by the native interjections *hoi, ai*
  [vandersijs1996-leenwoordenboek p.57–58].
- Note the free slot: Irish has no /œy/-like diphthong, so Dutch ⟨ui⟩ will simply go unused unless a
  vowel-colouring option (8.1c) is chosen, which would put it to work for slender-adjacent /u/.

### 8.4 Irish initial clusters against the Dutch onset inventory
Licit as-is (native Dutch clusters, §2): **/sp st sk sm sn sl/, /bl br gl gr dr tr kr kl fl fr/**
(with /g/ → /ɣ/ or kept as the loan phoneme: /ɣl ɣr/ = Dutch ⟨gl gr⟩ /xl xr/ in the Netherlandic
transcription), **/kn/** (native: *knie*), **/tʋ dʋ kʋ zʋ/** for /tw dw kw/.
**Not licit:**
- **/sr/** — sibilant + rhotic is historically filtered; attested only in the very recent loan
  *Sri Lanka* [taalportaal-onset-clusters-2c]. Falls under §3.1: keep as a marked loan onset, or use
  the attested Dutch historical repair of **/t/-intrusion** (*remmen/stremmen*, *siroop/stroop*) →
  /str/.
- **/gn/** — as an onset, Dutch has /xn/ (*gnoe*), so Irish /ɡn/ → /xn/ or /ɣn/ is available; but
  Irish /ŋ/-initial anything is impossible (/ŋ/ is coda-only).
- **/mn/** — sonorant + sonorant onsets are essentially banned; only /ʋr/ is native, the rest are
  marginal loans [taalportaal-onset-clusters-2c §Sonorant + sonorant]. /mn/ is not in the matrix at
  all → §3.1: delete a member (Dutch-internal preference: reduce to the more sonorous? not settled
  by these sources) or keep as marked-foreign, as with *pneumatisch*.
- Any Irish **sonorant + obstruent** onset — categorically banned
  [taalportaal-onset-clusters-2c §Sonorant + obstruent sequences].
Note also the **Consonant Cluster Condition**: at most one non-coronal articulator per cluster. Irish
/kn̪ˠ/ is fine (/k/ dorsal, /n/ coronal); a hypothetical /pk-/ or /kp-/ is not.

### 8.5 Initial mutations and genitives
Nothing in these sources speaks to how Dutch treats donor-internal consonant alternations; loans are
borrowed in one fixed shape. **Leave for the Irish digest.** One relevant fact: Dutch morphology is
happy to bolt native affixes onto a foreign stem without altering it (*superman* → *supermanachtig*,
*to trigger* → *getriggerd*, *to download* → *down te loaden*)
[loan-vandijk-toename pp.24, 29], so an epithet formed from an Irish stem plus a Dutch suffix (§6) is
a well-attested shape.

### 8.6 Rule order, and two worked derivations

The rules in §2–§4 feed each other, so the order matters. **This ordering is the digest's proposal**
— no source states a pipeline — but each *step* is sourced, and the two ordering facts that are
sourced are marked.

1. **Substitute segments** (§3.4) and resolve the broad/slender policy (§8.1).
2. **Map vowels** (§8.3) to a first-pass tense/lax class.
3. **Syllabify**, maximizing onsets [taalportaal-phonotactics-word-level §Maximal Onset Constraint];
   assign surplus word-final coronal obstruents to the appendix (§2).
4. **Enforce the rhyme constraints**, adjusting vowel class where needed: lax vowels must be closed;
   `*[Vː]CC[-cor]`; tense/voiced vs lax/voiceless fricative; /ŋ/ only after a lax vowel; glide and
   diphthong restrictions (§2).
5. **Repair remaining illicit clusters** (§3.1–§3.3) — and note that §3.1 has no attested repair, so
   this step is where the strand's policy shows.
6. **Degemination** within the prosodic word (§2).
7. **Voice assimilation**, then **final devoicing** — *sourced order*: final devoicing feeds
   progressive assimilation (*rondvaart* /rɔnd+vaːrt/ → [ˈrɔntfaːrt])
   [devoic-grijzenhout-roa303 pp.2–8].
8. **Schwa epenthesis** (§3.2) — optional, register-dependent; it applies to the *output* coda, so
   after 4–7.
9. **Nasal assimilation**; **hiatus resolution** (§2).
10. **Stress** (§4), subject to the open precedence decision.
11. **Romanize** (§5).

**Derivation A — *Matánach* 'Burly' /ˈmˠat̪ˠɑːnˠəx/** (policy: collapse broad/slender, 8.1a)
1. Collapse: /matɑːnəx/. All segments exist in Belgian (/m t n x/ native; /x/ is a Belgian phoneme).
2. Vowels: /a/ → /ɑ/ (lax), /ɑː/ → /aː/ (tense), /ə/ → /ə/.
3. Syllabify: /mɑ.taː.nəx/.
4. σ1 has a **lax vowel in an open syllable** — illegal [taalportaal-nuclei §B-class vowels]. Native
   Dutch fixes this by **ambisyllabicity**, exactly as in *katten* [ˈkɑtə(n)]
   [taalportaal-codas ex.2b]: /t/ is shared, giving [ˈmɑt.taː.nəx] at the syllable level and
   [ˈmɑtaːnəx] at the segmental level. (Alternative: tense σ1 to [maː-].) σ2 open + tense: legal.
   σ3 = schwa + /x/: legal (*jarig*).
5. No illicit clusters.  6. No geminates.  7. No voiced obstruents to devoice.
8. No liquid+C coda, so no schwa epenthesis.  9. Nothing to assimilate.
10. Stress: Irish initial stress is retained under the "keep source stress" or "hybrid" policy, and
    is Dutch-legal (no schwa is stressed; nothing final is superheavy) → [ˈmɑtaːnəx]. Under the
    "re-stress by Dutch" policy the closed-penult restriction does not apply (penult *taa* is open),
    schwa blocks final stress, and the default penult rule gives [mɑˈtaːnəx].
11. Romanize (§5): the tense /aː/ is in an open syllable, so it is written single; /x/ is ⟨ch⟩;
    schwa is ⟨e⟩ → **⟨Matanech⟩**, or with a doubled consonant to keep σ1 short, **⟨Mattanech⟩**.
    (⟨Matanach⟩ would be read with a tense /aː/ in the last syllable.)
**Result: *Matánach* survives Dutch almost intact.** That is the useful finding — the strand's Dutch
character will come from stress, romanization and the broad/slender decision, not from repair.

**Derivation B — *Lasairchos* 'Flamefoot' /ˈl̪ˠɑsˠəɾʲxosˠ/** (same policy)
1. Collapse: /lɑsəɾxos/ → /lɑsərxos/.
2. Vowels: /ɑ/ → /ɑ/, /ə/ → /ə/, /o/ → /ɔ/ (lax, since it is closed).
3. Syllabify with maximal onsets: /lɑ.sər.xɔs/ — /rx/ cannot be a Dutch **onset** (/xr/ is, /rx/ is
   not: sonorant+obstruent onsets are banned [taalportaal-onset-clusters-2c §Sonorant + obstruent]),
   so /r/ closes σ2 and /x/ opens σ3.
4. σ1 lax /ɑ/ open → ambisyllabic /s/ (as in *tussen* /tʏsə(n)/). σ2 = /sər/, a schwa syllable with a
   coda /r/: legal. σ3 = /xɔs/: lax vowel + /s/, which is the licit lax+voiceless-fricative pattern
   (§2(a)); *bos* [bɔs] is the source's own example.
5. `/-rx/` is a licit **coda** cluster (*monarch*, *erg*) but here /x/ is syllabified into the next
   onset, so nothing to repair.
6.–7. Nothing.
8. **Schwa epenthesis does not apply**: it needs a liquid+C *tautosyllabic* coda, and here /r/ and
   /x/ are in different syllables [taalportaal-schwa-epenthesis-deletion §quickinfo].
9. Nothing.  10. Initial stress retained → [ˈlɑsərxɔs].
11. Romanize: **⟨Lassercho(s)⟩** — ⟨ss⟩ keeps σ1 short, ⟨ch⟩ = /x/, ⟨e⟩ = schwa.
**Note the branch point:** if the strand takes broad/slender option (b), σ2's slender /ɾʲ/ is in a
**coda**, where /j/ is barred — so it must collapse anyway, and options (a) and (b) converge on this
word. Option (c) would front σ3's vowel: /xøːs/ → ⟨cheus⟩.

## 9. Open questions

Ordered by how much they change the output.

1. **Broad/slender** (§8.1) — no attested precedent. Three `(design fallback)` options with
   different coda behaviour; option (b) has to collapse in codas anyway, so (a) and (b) converge on
   many Irish words. **Nothing downstream can be finalised before this.**
2. **Stress precedence** (§4, OPEN DECISION) — keep the Irish source stress (which is what Dutch
   does with most loans, and what Van Oostendorp says the three-syllable window really reflects),
   re-stress by the Dutch tendencies, or take the hybrid. Changes every output.
3. **Romanization convention** (§5, OPEN DECISION) — authentic Dutch spelling plus a pronunciation
   key, or a separate English-reader respelling. Native Dutch spelling alone does not meet the
   project's "an English reader can pronounce it approximately right" requirement.
4. **Adaptation register** (§3.0) — etymological / vernederlandst / spelling-pronunciation, and at
   what integration level. Belgian usage is measurably split by donor: it nativizes non-French loans
   more but French loans less, and prefers spelling-pronunciation to phonetic repair.
5. **The /Vː/ + voiceless-fricative repair** (§8.3) — lax the vowel, voice the fricative, or accept
   the violation. All three are Dutch-legal. Note the correction: *Matánach* is **not** an instance
   (its /x/ follows schwa); the constraint bites stressed /Vːx Vːf Vːs/ syllables.
6. **Irish coda /h/** (§8.2) — delete, resyllabify, or substitute /x ɣ/. No Dutch source attests any
   repair; §3 supplies neither a deletion target nor a movement rule.
7. **Voiceless sonorants** (§8.2) — no precedent at all; the only Dutch fact nearby is positional
   [r̥] word-finally and before a voiceless stop. Three fallbacks listed, none sourced.
8. **Illicit onset clusters** (§3.1) — **there is no attested adult loan repair in this
   bibliography.** Keeping the cluster and sounding foreign *is* attested (*pneumonie*, *psalm*);
   deletion and epenthesis are policy choices. The only Dutch deletion-preference data is child
   language.
9. **Donor vowel length** (§3.6 CONFLICT) — the "reinterpret as tense/lax and let the coda decide"
   policy is the digest's proposal; the modern data show competing outcomes for the same word class.
10. **/ʌ/ → /ɑ/ or /ʏ/** (§3.4 CONFLICT) — both attested, no conditioning stated.
11. **/g/** (§3.4 CONFLICT) — /ɣ/ or retained [g]; [k] was **not observed** in the Belgian samples,
    which is not the same as banned.
12. **/n/-deletion after schwa** — obligatory in the western Netherlands, "variable elsewhere"; no
    source gives the Flemish rate. Affects every *-en* ending the tool generates.
13. **Whether to model the Belgian fricative-devoicing phonetics** (70% of initial /v z ɣ/ realized
    voiceless) in the output, or only in the phonemic representation.
14. **Rule order** (§8.6) — the pipeline given is the digest's proposal; only one ordering fact in
    it is sourced (final devoicing feeds progressive voice assimilation).
15. **Secondary stress** was not extracted in detail; Taalportaal has eight further sub-pages if
    multi-word epithets need it.
