# Source digest: Dutch (Belgian Standard Dutch)

## 0. Variety and scope

**Variety: Belgian Standard Dutch** (Flanders), the variety described by Verhoeven (2005). This is
the variety behind **PHOIBLE InvID 2169**: the inventory row and its primary description are the
*same document*, so inventory and prose cannot disagree with each other
[verhoeven2005 p.243; bib.md "Belgian vs. Netherlandic"]. Verhoeven describes it as one of the two
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
Netherlandic sources write A-class vowels without length marks (`/i y u e ø o a/`), write the labial
approximant `/ʋ/`, and write the rhotic `/r/`. This digest keeps each source's symbols when quoting
its examples, but the Belgian phonemic targets are: `/i y u eː øː oː aː/`, `/w/` (or `/ʋ/`, see
CONFLICT in §1), `/r/` = alveolar **or** uvular trill.

**Licensing.** Taalportaal is free to read but **not openly licensed** (INT terms: non-commercial /
private use only). Citing and quoting is fine; shipping derived cluster tables in a public repo is
not clearly covered. Every Taalportaal-only fact below is marked `[taalportaal-*]` so it can be
re-sourced from `booij1978`/`booij1999`/`wiki-nl-phonology` if that becomes necessary
[bib.md `taalportaal` entry].

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
  /xɛil/, *geil* /ɣɛil/ [p.244]. Wikipedia agrees: in the south the /x/–/ɣ/ distinction "is
  generally preserved as velar [x, ɣ] or post-palatal [x̟, ɣ˖]", the *zachte g*
  [wiki-nl-phonology §Consonants/Dorsal]. **This is the single most important Belgian property for
  Irish input** (§8).
- **The fricative voicing contrast /f v/, /s z/, /x ɣ/ is phonologically stable in Belgian** but
  phonetically eroding: 70% of word-initial and 56% of intervocalic fricatives are realised with no
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
Belgian [eː øː oː] are **always monophthongs**; Netherlandic diphthongises them [p.245–246].

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
`(C)(C)(C) V (V) (C)(C)(C)(C)` — max three onset consonants, and if there are three the first must
be /s/ [taalportaal-onset-clusters-3c §quickinfo (Booij 1995:26)]. LAPSyD gives the same canon and
a syllabic index of 8 (onset 3 / nucleus 2 / coda 3) [lapsyd-dutch-nld]. Wikipedia states
(C)(C)(C)V(C)(C)(C)(C) and cites *straat* /straːt/, *herfst* /ɦɛrfst/, *ergst* /ɛrxst/
[wiki-nl-language §Phonology].
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
cluster [ibid.].
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
  member) [ibid. §Obstruent + sonorant sequences].
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
*enorm* [(ʔ)eˈnɔrm] [ibid. §3 (Gussenhoven 1992:45)]. Verhoeven independently reports the glottal
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
- **Sonorant + sonorant** (liquid before nasal only): `-lm` zalm, `-rm` arm, `-rn` karn.
  Banned: `*-ln` (German *Köln* → Dutch *Keulen*), `*-lŋ`, `*-rŋ`, `*-rl` (German *Karl* → Dutch
  *Karel*) [taalportaal-codas Table 1].
- **Liquid + obstruent**: `-lf` elf, `-lv` elf 'eleven', `-ls` als, `-lz` hals, `-lx` mulch,
  `-lɣ` balg, `-lp` hulp, `-lt` asfalt, `-ld` held, `-lk` elk, `-rf` smurf, `-rv` korf, `-rs` mars,
  `-rz` vers, `-rx` monarch, `-rɣ` erg, `-rp` harp, `-rt` art, `-rd` hard, `-rk` ark.
  Banned: `*-lb`, `*-rb` — these occur **only in loans** (*stilb, sorb, blurb*)
  [taalportaal-codas Table 2].
- **Nasal + obstruent**: only nasal + **homorganic stop**. `-mp` ramp, `-nt` munt, `-nd` mond,
  `-ŋk` koninklijk; `-md` hemd, vreemd is non-homorganic and infrequent. Banned: `*-mb`
  (only loan *aplomb* [aˈplɔm]), `*-ŋg`. **Nasals cannot combine with fricatives in the same coda**
  (cf. heterosyllabic *kamfer* /kɑm.fər/) [taalportaal-codas Table 3].
- **Obstruent + obstruent**: at least one member is coronal, normally the second (except /sC/):
  `-pt` intercept, `-ps` rups, `-ts` muts, `-tʃ` kitsch, `-kt` pact, `-ks` heks, `-ft` kaft,
  `-sp` wesp, `-st` beest, `-sk` kiosk, `-xt` macht. Gaps: `-fs`, `-xs`
  [taalportaal-codas Table 4].
- The /sp sk st/ codas violate sonority sequencing and are treated as the same /s/-appendix
  exception as in onsets [taalportaal-codas §Exceptional bisegmental coda clusters (Booij 1995:41)].
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
4. Diphthongs are partly exempt: all three may precede /s/ (*krijs, kruis, kous*) and /œy/ may
   precede /x/ (*gejuich*), evidenced by the *-te* past-tense suffix they select.
[all: taalportaal-coda-cooccurrence-restrictions §same]
**Irish /ɑː/ + /x/ (as in *Matánach*) is precisely the banned A-class + voiceless-fricative shape.
§3 gives the repair options.**

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
- Diphthong + consonant: freely before non-coronals and coronals alike (*eik, duim, faun, pijp,
  kuip, mijt, spruit, hout, slijk, buik, pauk*); voiced-obstruent codas surface devoiced (*tijd*
  [tɛit], *goud* [xɑut]) [ibid. Tables 2–3].
- Voiced obstruents never surface in a coda at all — see final devoicing, §3.

### Medial clusters, gemination, hiatus
- Word-medial clusters are licensed as (licit coda) + (licit onset); the Maximal Onset Principle
  assigns as much as possible to the onset [taalportaal-codas §quickinfo;
  booij1978-fonotactische § (*malkon* vs \**malrkon*)]. Word-medial coda ≤ 2 is the hard limit.
- **Gemination: none.** Identical adjacent consonants degeminate — obligatorily within the prosodic
  word across a morpheme boundary, optionally across word/compound boundaries: *eet* /et+t/ → [et],
  *grootte* [ˈɣrotə], *onmiddellijk* → [ɔˈmɪdələk]; compare optional *handdoek* [ˈhɑnduk] vs.
  *berggeit* [ˈbɛrxːɛit], and the pair *verassen* [vɛrɑsə(n)] / *verrassen* [vɛrːɑsə(n)]
  [taalportaal-degemination §quickinfo (Booij 1995:68–69)]. Double consonant *letters* in spelling
  mark a preceding short vowel and are not long consonants (§5).
- **Hiatus** is resolved by inserting a **homorganic glide**: after a front vowel [j], after a back
  vowel [w] — this is why Taalportaal writes *patio* [ˈpa.tsi.jo], *video* [ˈvi.de.jo], *acacia*
  [a.ˈka.si.ja], *ravioli* [ra.vi.'jo.li] [taalportaal-hiatus-resolution;
  taalportaal-stress-default-penultimate ex.4, 7, 8]. Vowel sequences do otherwise occur across
  syllable boundaries: *hiaat* [hi.ˈat], *chaos* [ˈxa.ɔs], *aorta* [a.ˈɔr.ta]
  [taalportaal-onsetless-syllables §5].

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
date of borrowing, and route of borrowing [ibid. p.33–34].
**Belgian bias (well attested and consequential):** Flemish speakers **nativize non-French loans
more, but French loans less**, than Netherlandic speakers [loan-kleinbreukink1999-culinair p.276];
and where they do nativize, they prefer **spelling-pronunciation** over the phonetically-nearest
repair — the [k] repair for foreign /g/ is a Netherlandic option that Flemish speakers essentially
do not use (*baguette*: Flanders [baɣɛt] 63–88%, [bakɛt] 0%) [ibid.]. Gerritsen & van Bezooijen
suggest Flemish speakers would rather use the fully foreign pronunciation than a "botched"
nativization [loan-gerritsen1995-engels p.17].

### 3.1 Illicit onset cluster
- Dutch onsets are permissive (three consonants, /s/+stop+liquid), so most donor onsets are simply
  licit. There is **no attested loanword epenthesis into an onset cluster** in these sources —
  "not covered".
- Where a cluster is illicit, the attested Dutch-internal preference is **deletion of one member**,
  and the acquisition data give the preference ranking; use only as a tiebreaker, since this is
  child Dutch, not adult loan adaptation [twpl-clusterreduction; flagged in bib.md].
- Loans *may simply keep* an illicit onset and be marked foreign (*pneumatisch* /pn-/,
  *psalm* /ps-/, *Pjotr* /pj-/) [booij2011-msc p.2052, p.2056].
- Attested change to an onset: `/ɡr/ → /xr/` in *grotte* → *grot* [xrɔt]; `/ɡ/ → /ɣ/` in *cigarette*
  → *sigaret* [siːɣaːrɛt] [wold, van der Sijs transcription — Netherlandic; Belgian keeps /ɣ/].

### 3.2 Illicit coda cluster
- **Schwa epenthesis** is the attested Dutch repair, and it is a live phonological rule, not a
  historical residue:
  `∅ → ə / [+liquid] __ C[-coronal]` within a complex coda.
  *melk* [mɛl(ə)k], *kalm* [kɑl(ə)m], *arm* [ɑr(ə)m], *help* [hɛl(ə)p], *harp* [hɑr(ə)p],
  *herfst* [hɛr(ə)fst], *elf* [ɛl(ə)f], *erg* [ɛr(ə)x], *hoorn* [hor(ə)n], *urn* [ʏr(ə)n]
  [taalportaal-schwa-epenthesis-deletion §quickinfo ex.1; devoic-warner2001-epenthetic-schwa p.388].
  It applies after **both /l/ and /r/**, though it is empirically commoner after /l/
  [devoic-warner2001-epenthetic-schwa p.397].
  **Blocked when the two consonants are homorganic**: *hals* [hɑls] never \*[hɑləs]; *damp* [dɑmp]
  never \*[dɑməp] [devoic-schwa-mpi §Introduction].
  **Blocked before the coronal appendix /s t/**: *hart* [hɑrt] never \*[hɑrət]; likewise *hars,
  halt, band, bank*; and no schwa inside an appendix: *kaft* [kɑft] \*[kɑfət], *paard* [paːrt]
  \*[paːrət], *herfst* [hɛr(ə)fst] but \*[hɛrfəst]
  [taalportaal-schwa-epenthesis-deletion ex.2 (Booij 1995:127f.); taalportaal-codas §figure 3].
  **Belgian note:** schwa epenthesis is reported as *more* prominent in Flanders than in the western
  Netherlands [devoic-jansen2021-schwa p.7, citing Sebregts 2014, Kloots et al. 2009].
- **Schwa epenthesis is also attested resolving foreign final clusters in borrowing**: French
  *ministre* → *minister* [miːnɪstər]; Latin *templum* → *tempel* [tɛmpəl]; Latin *fenestra* →
  *venster* [vɛnstər] [wold, van der Sijs].
- **English syllabic sonorants become /ə/+C**: *single* /ˈsɪŋɡl/ → [sɪŋɡəl]
  [loan-vandijk-toename p.26].

### 3.3 Three-consonant sequences
Word-finally, three and more consonants are licit if the extra ones are coronal obstruents
(appendix): *herfst*, *promptst* [taalportaal-codas §quickinfo]. Where they are not, the language's
own reduction is **t-deletion**: obligatory before diminutive *-je* after an obstruent
(*klachtje* [klɑxjə], *marktje* [mɑrkjə], *kastje* [kɑʃjə]) and before *-s/-st* (*echtst* [ɛxst],
*lichts* [lɪxs]); **blocked after a sonorant** (*tandje* [tɑntjə], never \*[tɑnjə])
[taalportaal-casual-speech §Consonant deletion ex.9]. Optional in compounds and phrases, graded by
the following segment (plosive > nasal > liquid/glide > pause) [ibid. ex.10–11]. Also /xts/ → /xs/
[codaclusters-nl-af].

### 3.4 Absent segment → substitute

| Source segment | Belgian Dutch substitute | Attested example | Citation |
|---|---|---|---|
| /g/ | **/ɣ/** (etymological/spelling route) or kept as loan [g]; **[k] is a Netherlandic-only repair** | *garage, garderobe, yoga* fully nativized to /ɣ/; *baguette* Flanders [baɣɛt] 63–88%, [bakɛt] **0%**; *spaghetti* Flanders young 100% native /ɣ/; *drugs* Flanders 14/15 spelling-/ɣ/ | [loan-posthumus1988-uitspraak §a; loan-kleinbreukink1999-culinair p.276; loan-gerritsen1995-engels p.16] |
| /θ/ | /t/ | *thinner* → *tinner* | [loan-posthumus1988-uitspraak §repertoire] |
| /ð/ | /d/ | *the* → *de* | [ibid.] |
| /dʒ/ | /ʃ/ ("sj"), or /j/ in established words, or /ts/ finally | *jam* → *sjem*; *joker, jumbo, jumper* with /j/; *bridge* → *brits* | [ibid. §c–d] |
| /tʃ/ | /ʃ/ carefully, /s/ casually (final) | *match* → *mets*, *kitsch* → *kiets*; *lunch* → [lʏnʃ] | [ibid. §c; wold] |
| /ʃ/ | kept (loan phoneme) or → /s/ finally in casual style | *douche* → *does*, *finish* → *fienis* | [ibid. §b] |
| /ʒ/ | kept (loan phoneme); prescriptively → /ɣ/ | *gendarme, horloge* keep [ʒ]; *garage, bagage, intrige* with the g of *gaan* | [vandersijs1996 p.57; loan-mars1994-vreemde p.141 — prescriptive, not a measured rule] |
| /æ/ | **/ɛ/** (merging with the vowel of *zet*) | *match* = *set*; *jackpot* → [dʒɛkpɔt]; *slash* → [slɛʃ]; *happy* → [hɛpi] | [loan-posthumus1988-uitspraak §repertoire; loan-vandijk-toename pp.26,33] |
| /ʌ/ | /ɑ/ or /ʏ/ (both attested, no rule) | *fuck* → [fɑk]; *bubble* → [bʏblɪŋ]; *lunch* → [lʏnʃ]; *bus* → [bʏs] | [loan-vandijk-toename pp.25,27; wold] |
| /eɪ/ | **/eː/** (Belgian monophthong) | *tape* → [tep], *fake* → [fekə], *race* → [res] | [loan-vandijk-toename pp.24,32] |
| /oʊ/ | **/oː/** | *show* → [ʃo], *download* → [lodə] | [loan-vandijk-toename pp.24,25] |
| /iː uː/ | shortened to /i u/ | *groupies* → [ɡrupiz], *issue* → [ɪʃu] | [loan-vandijk-toename pp.26,31] |
| French /y/ | kept /y(ː)/ in learned loans; older loans → /œy/ | *communie* [kɔ.ˈmy.ni]; *juste* → *juist* [jœyst], *flûte* → *fluit* [flœyt] | [taalportaal-stress-loanwords; wold; nagy2008-frans §3.1.1] |
| French nasal vowels | **Belgian keeps them** (integration); Netherlandic denasalizes to [ɑn ɔn ɛn ʏm] | *parfum* B [pɑrfˈœ̃] 95% vs N [pɑrfˈʏm] 87%; *entrecôte, entree, ensemble, élan* B nasal / N denasal; both denasalize *plafond, campagne, restaurant* | [nagy2008-frans §3.2.1; loan-theissen2006-nasalen §1–3] |
| unstressed English /ə/ | restored to a full vowel from spelling | *tattoo* [tə'tu:] → [tɑtu:]; *community* [kə'mju:nəti] → [kɔmjunɪti] | [loan-vandijk-toename pp.24,27] |
| English post-vocalic /r/ | restored from spelling (Dutch is rhotic) | *porno* ['pɔ:noʊ] → ['pɔrno]; *to trigger* → [ɣətrɪɣərd] | [loan-vandijk-toename pp.24,29] |

### 3.5 Word-edge processes
- **Final devoicing** — an *active rule*, applied to loans without exception:
  `/b d v z ɣ/ → [p t f s x] / __ ]σ` (**syllable**-final, not merely word-final)
  [taalportaal-final-devoicing §quickinfo]. Evidence: *hand* [hɑnt] vs *handen* [hɑndən]; *huis*
  [hœys] vs *huizen* [hœyzən]; complex codas *krabt* [krɑpt], *broeds* [bruts] [ibid. ex.1–2].
  Suffix behaviour: vowel-initial suffixes and past *-de* are cohering and do **not** trigger it
  (*miljard* [mɪljɑrt] → *miljardair* [mɪljɑrdɛːr]); consonant-initial suffixes plus *-aardig*,
  *-achtig* do (*hond* [hɔnt] → *hondje* [hɔntjə]) [ibid. §Morphological aspects].
  In loans: *headset* → [hɛːtsɛt]; *rose* → *roos* [roːs]; and **English final voiced obstruents are
  devoiced with the vowel held long**: *cruise* → [kruːs], contrasting native *kroes*
  [loan-vandijk-toename p.27; wold; loan-posthumus1988-uitspraak §repertoire].
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
    → [ˈɑzbɛst] [ibid. ex.3]. Also tautosyllabic stop+fricative goes the other way: *goeds* → [ɣuts]
    [booij1979-syllabe p.548–549].
- **Nasal place assimilation:** `[+nas] → [α place] / __ [α place, −son]`, obligatory
  morpheme-internally; across boundaries **only /n/ assimilates**, never /m/ or /ŋ/.
  *baanbrekend* [bambrekənt], *bruinkool* [brœyŋkol], *bronwater* [brɔɱʋatər]; but *boomstam*,
  *hangmat* unchanged [taalportaal-nasal-assimilation §quickinfo, ex.7–9].
- **/n/-deletion:** `n → ∅ / ə __ ]σ` — obligatory in the western Netherlands, variable elsewhere:
  *regen* [ˈreɣə(n)], *molen* [ˈmolə(n)] [taalportaal-n-deletion §quickinfo]. Treat as optional for
  Belgian ("not covered" for Flanders specifically).
- **Initial glottal stop** before a vowel-initial stressed syllable (§2, and Verhoeven for Belgian).
- **No final-vowel addition, no prothesis** is reported anywhere in these sources.

### 3.6 Vowel adaptation
- Length is **not** carried over as length: it is reinterpreted as the **tense/lax (A/B class)**
  distinction, and the choice is then forced by the coda (§2 restrictions (a) and (b)). Attested:
  French /a/ in *calme, palme* → Dutch **lax** /ɑ/ before the non-coronal cluster (*kalm* [kɑlm],
  *palm* [pɑlm]) — exactly what `*[Vː]CC[-cor]` predicts [wold].
- English long vowels shorten (*groupies* [ɡrupiz], *issue* [ɪʃu]); English diphthongs /eɪ oʊ/
  monophthongize to /eː oː/ [loan-vandijk-toename pp.24–32].
- Loan-vowel length is itself a choice point: *team, pool, keeper, corner, partner* have competing
  long-loan-vowel and short-native-vowel pronunciations [loan-posthumus1988-uitspraak §e–f].
- Unstressed reduced vowels in the donor are typically **restored from spelling**, not kept as schwa
  (§3.4).
- French final /e/ can be reinterpreted as the diphthong /ɛi/: *vallée* → *vallei* [vɑlɛi] [wold].
- Hiatus in the donor gets a glide: *maíz* → *maïs* [mɑjs] [wold].

### 3.7 Anything else
- **Gemination: never** (§2, degemination).
- **Metathesis: not covered.**
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

### The practical rule (ordered; apply to a novel word)
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
penultimate stress (*academie* [ɑ.ka.ˈde.mi], *tragedie* [tra.ˈɣe.di]) [ibid. Tables 1–3].
Impressionistic ongoing shifts, mostly **towards the penult**: *democratie* → [de.mo.ˈkra.si],
*parfum* [pɑr.ˈfʏm] → [ˈpɑr.fʏm], *catalogus* → [ka.ta.ˈlo.ɣʏs], *pagina* → [pa.ˈɣi.na]
[ibid. Tables 4–5]. **Belgian**: van der Sijs notes Southern Dutch **retracts** stress in French
words where Northern Dutch does not (*pyjama*, *torpedo*), and that a word may be an English loan
with initial stress in the North and a French loan with final stress in the South (*detective*,
*recital*) [vandersijs1996-leenwoordenboek p.60]. Older Latin loans show retraction to the first
syllable (*bekken*); younger French loans keep final/penultimate stress (*bassin*)
[vandersijs1996-leenwoordenboek, "De uitspraak van leenwoorden"].

## 5. Romanization

Dutch orthography is a good vehicle for invented names because it is shallow *given* the
open/closed-syllable convention — but that convention is the thing an English reader will get wrong.

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
   *dag-arbeider*, not \**daggarbeider* [ibid.].

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
| 3 | **-pje** | same | after /m/ preceded by an A-class vowel, diphthong or schwa (the stop is homorganic with the nasal) | *boom* → *boompje* [ˈbompjə], *Mokum* → *Mokumpje*, *riem* → *riempje* | yes [ibid.; booij2011-msc p.2056] |
| 4 | **-etje** (i.e. -ətjə, with the stem consonant doubled) | same | after a sonorant preceded by a **B-class (lax) vowel** | *ram* → *rammetje*, *man* → *mannetje*, *bal* → *balletje*, *kar* → *karretje*, *rang* → *rangetje* | yes [taalportaal-coda-cooccurrence-restrictions Table 6] |
| 5 | **-kje** | same | after /ŋ/ preceded by unstressed /ɪ/ (competes with *-etje*) | *koning* → *koningkje* [ˈkonɪŋkjə]; *wandeling* → *wandelingetje* | yes; "selection also depends on the stress pattern, and there is dialectal variation" [taalportaal-nasal-assimilation §same] |
| — | note | | a stem-final /t d/ + *-je* surfaces with a **palatal stop**: *bootje* [boːcə], *paardje* [paːʀcə]; a stem-final /n/ + *-tje* gives [ɲc]: *landje* [lɔɲcə] | | [verhoeven2005 p.244] |
| 6 | attributive **-e** [ə] on adjectives | agreement | on any attributive adjective **except** before an indefinite singular **neuter** noun; never in the predicate | *de mooi-e fiets*, *het mooi-e huis*, *koud-e soep* — but *een mooi huis*, *koud water*, *De soep is koud* | fully productive [wiki-nl-language §Grammar] |
| 7 | genitive **-s / -'s / -'** | possessive, on **proper names** (nouns and adjectives are otherwise uninflected for case) | proper names | *Jans*, *Anna's* | productive [wiki-nl-language §Grammar] |
| 8 | **-ig**, **-lijk**, **-achtig** | adjective from noun/adjective ('-y, -like, -ish') | N→A, A→A; *-achtig* is one of only two consonant-initial suffixes that trigger final devoicing | *blauw* → *blauwig* 'bluish', *meester* → *meesterlijk* 'masterly', *superman* → *supermanachtig* | productive [booij2014-word-formation p.13; loan-vandijk-toename p.24] |
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
  stress-marked orthographic form only [taalportaal-stress-loanwords]. These are the stress rows.
- **20 rows from WOLD** (van der Sijs's Dutch vocabulary) — donor orthography + Dutch IPA. NB
  **bib.md and the task brief describe WOLD as orthography-only; the extracted
  `infra/wold-dutch-loanpairs.tsv` in fact carries a segmented Dutch IPA column**, so these rows
  have `target_ipa` filled. The transcription is **Netherlandic** (`ʋ`, `ɛi ɑu`, positional `ɣ/x`),
  which is flagged in each note. Donor side has no IPA anywhere in WOLD, so `source_ipa` is blank.
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
   Options, undecided: (a) collapse both series; (b) Cʲ → Cj in onsets only, collapse in codas;
   (c) Cʲ colours the following vowel (front it: /a/ → /ɛ/, /o/ → /ø/) — Dutch has the front rounded
   vowels /y ø/ to do this with, but no source attests such a repair.

### 8.2 Irish segments vs Belgian Dutch

| Irish | Belgian status | Note |
|---|---|---|
| /ɣ/ | **native phoneme** | Confirmed: Belgian has voiced velar /ɣ/, absent in the Netherlands [verhoeven2005 p.244]. Maps to itself. **This is why Belgian was chosen.** |
| /x/ | **native phoneme** | Also velar, contrasting with /ɣ/ [ibid.]. Maps to itself. Watch the §2(a) restriction: /x/ needs a **lax** vowel before it. |
| /h/ | native /ɦ/ | Belgian has /ɦ/; **barred from codas** [taalportaal-codas]. Irish /h/ in a coda must be deleted or moved. |
| voiceless sonorants (Irish lenition outputs) | **absent, no precedent** | Nothing in these sources. Nearest facts: Belgian /r/ *is* devoiced word-finally and before voiceless stops [verhoeven2005 p.245] — a hook for /r̥/ only. Options: map to the voiced sonorant; map to /h/+sonorant; delete. Undecided. |
| /ɾˠ/ vs trill | **fine either way** | Belgian /r/ is an alveolar trill in free variation with a uvular trill; the alveolar is the default. Irish /ɾˠ/ and /rˠ/ both land on /r/ [verhoeven2005 p.245]. Belgian is a much better match here than Netherlandic. |
| /l̪ˠ lʲ n̪ˠ nʲ/ | one /l/, one /n/ | See 8.1. /l/ has velarized and palatalized allophones in Belgian; /n/ has [ɲ] before palatals. |
| /w/ (lenited b/m) | native /w/ (labial approximant) | CONFLICT on its exact realization, §1. Never word-final [wiki-nl-orthography]. |
| /v/, /f/ | native | Both phonemes; but expect voiceless phonetics for /v/ (70% of initial fricatives) and obligatory devoicing word-finally [verhoeven2005 p.244]. |
| /p/ | native | No issue. |
| /ŋ/ | native but **coda-only, only after a lax vowel** | Never in an onset; never after a tense vowel or diphthong [taalportaal-codas; taalportaal-onsets-simple]. Irish /ŋ/ after a long vowel needs the vowel laxed. |

### 8.3 Vowel length and the Irish diphthongs
Irish phonemic length maps onto the Dutch **A/B class** system, not onto a length feature, and the
class is then constrained by the coda (§2 (a) and (b)). Concretely:
- Irish long vowel + single consonant → A-class + C. Fine.
- Irish long vowel + cluster ending in a **non-coronal** → **banned** (`*[Vː]CC[-cor]`). Repair: lax
  the vowel (French *calme* → *kalm* [kɑlm] is the attested precedent), or let the final consonant
  begin a new syllable, or (if the second C is coronal) leave it — *taart* [taːrt] is licit
  [kager-pater2012 p.6; wold].
- Irish long vowel + voiceless fricative (e.g. **/ɑː/ + /x/ in *Matánach* /ˈmˠat̪ˠɑːnˠəx/**) →
  **banned** by §2(a). Three repairs, all with some support, none attested for this exact case:
  (i) **lax the vowel**: /ɑːx/ → /ɑx/ — matches the *lachen* /lɑxə(n)/ pattern and the *calme* →
  *kalm* precedent; (ii) **voice the fricative**: /ɑːx/ → /aːɣ/ — legal, since Belgian *has* /ɣ/ and
  A-class + /ɣ/ is the *vogel* /voɣəl/ pattern; (iii) accept it as one of the small genuine
  exception class (*goochem, tafel*). (i) and (ii) both produce Dutch-legal output;
  **which one is a decision for the tool's author.**
- Irish short vowel is already B-class and must be closed — no repair needed.
- **Irish /iə uə/**: no Dutch equivalent; Dutch resolves vowel sequences with a homorganic glide
  ([j] after front, [w] after back) [taalportaal-hiatus-resolution], so /iə/ → [i.jə] and /uə/ →
  [u.wə] is the target-internal route; alternatively they map to the tense monophthongs /i u/.
- **Irish /əi/ and /əu/** map directly onto Dutch /ɛi/ and /ɔu/ (Verhoeven's *lei* [lɛj], *lauw*
  [lɔu]) [verhoeven2005 p.245] — the closest fit in the whole inventory. Dutch has no /ai/ or /oi/
  except as loan diphthongs licensed by *hoi, ai* [vandersijs1996 p.57–58].

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
- Any Irish **sonorant + obstruent** onset — categorically banned [ibid.].
Note also the **Consonant Cluster Condition**: at most one non-coronal articulator per cluster. Irish
/kn̪ˠ/ is fine (/k/ dorsal, /n/ coronal); a hypothetical /pk-/ or /kp-/ is not.

### 8.5 Initial mutations and genitives
Nothing in these sources speaks to how Dutch treats donor-internal consonant alternations; loans are
borrowed in one fixed shape. **Leave for the Irish digest.** One relevant fact: Dutch morphology is
happy to bolt native affixes onto a foreign stem without altering it (*superman* → *supermanachtig*,
*to trigger* → *getriggerd*, *to download* → *down te loaden*)
[loan-vandijk-toename pp.24, 29], so an epithet formed from an Irish stem plus a Dutch suffix (§6) is
a well-attested shape.

## 9. Open questions

1. **The /ɑː/+/x/ repair for *Matánach*** — lax the vowel, voice the fricative, or accept the
   violation (§8.3). All three are Dutch-legal; the sources do not choose.
2. **Broad/slender** — no attested precedent exists (§8.1). The three options have different
   phonotactic costs, and the coda case is genuinely blocked for the Cj route.
3. **Which adaptation register** the strand uses — etymological / vernederlandst / spelling-
   pronunciation (§3.0). Belgian usage is measurably split by donor: it nativizes non-French loans
   more but French loans less, and prefers spelling-pronunciation to phonetic repair.
4. **/g/**: whether the strand's inventory admits it. Belgian survey data say the [k] repair is
   essentially absent in Flanders; the real Flemish choice is /ɣ/ (spelling route) vs keeping [g].
5. **Whether to model the Belgian fricative-devoicing phonetics** (70% of initial /v z ɣ/ voiceless)
   in the romanization, or only in the IPA, or not at all.
6. **/n/-deletion after schwa** — obligatory in the western Netherlands, "variable elsewhere"; no
   source states the Flemish rate. Affects every *-en* ending the tool generates.
7. **Cluster-reduction preference (which member gets deleted)** is documented only from child
   language acquisition [twpl-clusterreduction], never from adult loan adaptation.
8. **Secondary stress** was not extracted in detail; Taalportaal has eight sub-pages on it if the
   generator needs multi-word epithets to sound right.
