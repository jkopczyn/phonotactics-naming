# Source digest: Egyptian Arabic (Cairene)

## 0. Variety and scope

**Variety**: Cairene Colloquial Arabic (CCA / EA / `arz`), the prestige urban dialect of Cairo and
the lower Nile Delta. Chosen for the project because it has by far the most open-access loanword
and phonotactic material of the four targets, and because through the dominance of Egyptian
media it has "become the de facto standard variety **in certain segments of the Arabic speaking
population**" [alqarhi2019-arabic-phonology p.14].

**Explicitly out of scope** and to be kept out of the rules: rural/Delta and Ṣaʿīdi (Upper
Egyptian) features — /q/ or /g/~/dʒ/ reflexes of ǧīm, retention of *q, uvular rather than velar
dorsal fricatives, and the absence of the vowel-shortening rule [ema1952-woidich §Overview;
wiki-egy-phonology §Emphasis spreading; §Vowel shortening: "vowel shortening is not made by rural
speakers"].

**Sources this digest rests on.** §1 inventory: `wiki-egy-phonology` (which sources its chart to
Watson 2002), `wiki-help-ipa-egy`, `lapsyd arabic-egy-arz`, `hassig2011-cairene`, `abdelmassih-intro`.
§2 syllable/clusters: `ijllnet-cairene-english-syll` (Khalifa 2018), `broselow1976`,
`broselow-arabic-syll`, `hassig2011-cairene`, `ojml-cairene-syllable`, `lapsyd arabic-egy-arz`.
§3 repair: `ema1958` (Hafez 1996) and `kwpl-ot-cairene-loan` (Galal 2004) are the two dedicated
loanword sources; `broselow1976` and `broselow-position-quality` for epenthesis site and quality.
§4 stress: `watson2011-word-stress`, `mccarthy1979-stress-syll`, `broselow-stress-epenthesis`.
§5 romanization: `wiki-help-ipa-egy`, `wiki-romanization-arabic`, `wiki-egy-arabic`,
`abdelmassih-intro`. §6 morphology: `abdelmassih-v3`, `ema1958`, `wiki-egy-arabic`,
`wiki-sun-moon-letters`, `wiki-nisba`, `broselow1976` ch.2.

### What the sources say about the PHOIBLE row

The project's PHOIBLE row is InvID 231 (UPSID), consonants
`b d̠ʒ d̪ d̪ˤ f h j k l̪ m n̪ q(marginal) r s̪ s̪ˤ t̪ t̪ˤ w z̪ z̪ˤ ħ ɡ ʁ ʃ ʔ ʕ χ`, vowels
`a eː iː oː uː æː ɪ ʊ`. The identical inventory appears in LAPSyD, whose stated sources are Watson
2002 and **Thelwall & Sa'adeddin (1990), "Illustrations of the IPA: Egyptian Arabic", JIPA 20:
37–39** [lapsyd arabic-egy-arz]. Contradictions and quirks:

1. **The dental diacritics are notational.** `t̪ d̪ s̪ z̪ n̪ l̪` (and the emphatics `t̪ˤ d̪ˤ s̪ˤ z̪ˤ`)
   are UPSID's convention for plain coronals; every descriptive source writes them `t d s z n l`
   [wiki-egy-phonology §Consonants; hassig2011-cairene p.13]. Strip the diacritic.
2. **`/d̠ʒ/` should be removed.** Cairene has native **/g/** where other dialects have /dʒ/:
   ǧabal 'mountain' = [ˈɡæbæl] [wiki-egy-phonology §Consonants, citing Watson 2002 p.16];
   "Cairene Arabic transforms the Modern Standard Arabic phoneme /dʒ/ into /g/"
   [hassig2011-cairene p.16, pp.47–48]. /dʒ/ appears only as a rural or Ṣaʿīdi feature and, marginally,
   in unassimilated loans (where it more often deaffricates to /ʒ/, which then tends to merge with
   /ʃ/) [wiki-egy-phonology §Consonants note 2].
   `CONFLICT:` the PHOIBLE/LAPSyD row lists both /d̠ʒ/ and /ɡ/ [lapsyd arabic-egy-arz]; Hassig's own Figure 4
   also lists dʒ while his prose and his mapping table deny it [hassig2011-cairene p.13 vs p.15,47–48]
   — internal to that source, and best read as a chart-copying error.
3. **`/χ ʁ/` vs `/x ɣ/`.** The PHOIBLE/LAPSyD row and Hassig write the uvular pair; Wikipedia writes
   the velar pair and says explicitly that the uvular realization [χ ʁ] is the **Ṣaʿīdi** variant,
   and that prestige-Cairene /x ɣ/ are velar and (unlike uvulars) do **not** trigger emphasis
   spreading [wiki-egy-phonology §Emphasis spreading].
   `CONFLICT: wiki-egy-phonology §Emphasis spreading (Cairene /x ɣ/ velar, non-triggering) vs.
   lapsyd arabic-egy-arz / PHOIBLE row 231 (/χ ʁ/ uvular).` The segment exists either way; the consequential
   part is whether it triggers emphasis spread, and the Cairene-specific answer is **no**. Use
   /x ɣ/ for Cairene and treat /χ ʁ/ as a transcription variant.
4. **`/p v ʒ/` are missing from the row** but are real, if marginal, Cairene loan phonemes; see §1.
5. **`/q/` marginal** is right for Cairene [wiki-egy-phonology §Consonants note 5; lapsyd arabic-egy-arz:
   "only a few words retain /q/, including the name of the city, /el qaːˈhera/"].
   `CONFLICT:` Hassig treats /q/ as a fully regular CA phoneme with an unconditioned MSA→CA
   `q → q` mapping [hassig2011-cairene p.13, p.47]. Hassig's thesis derives Cairene *from MSA text*
   for a synthesizer, which biases it toward retaining MSA segments; prefer the marginal reading.
6. **The vowel row is defensible but is one of two competing analyses.** The row's 5 long / 3 short
   system (`iː uː eː oː æː` / `ɪ ʊ a`) matches LAPSyD's stated "consensus of 5 long and 3 short
   vowels ... (Tomiche 1964, Cowan 1970) ... with qualities as suggested by Thelwall & Sa'adeddin
   (1990)" [lapsyd arabic-egy-arz §Vowel notes] and Wikipedia's chart [wiki-egy-phonology §Vowels].
   `CONFLICT: hassig2011-cairene p.13 analyses Cairene as a 4-quality system /i u a ɑˤ/ ×
   short/long, with the back low vowel an allophone of /a/ produced by emphasis spread, and no
   /eː oː/ or /ɪ ʊ/ contrast` — a minority, MSA-derivational analysis. Use the PHOIBLE/Wikipedia
   system; it is what the loanword sources presuppose.
   Note also that the row's `a` should be understood as **/a/ with allophones [æ] (default) and
   [ɑ] (under emphasis, and lexically in European loans)**, and its `æː` correspondingly as
   /aː/ ~ [æː ɑː] [wiki-egy-phonology §Emphasis spreading].
7. Consonant length: "**All consonants can appear geminate**" [lapsyd arabic-egy-arz §Consonant notes]. The
   PHOIBLE row does not encode this; see §2.

---

## 1. Inventory deltas

### Consonants — the working inventory

Native, uncontested: **/b t d k g ʔ  f s z ʃ x ɣ ħ ʕ h  m n  r(~ɾ)  l  j w/**
plus the emphatic (pharyngealized) series **/tˤ dˤ sˤ zˤ/** [wiki-egy-phonology §Consonants,
citing Watson 2002 p.21; abdelmassih-intro; hassig2011-cairene p.13].

**Additions to the PHOIBLE row:**

| segment | status | evidence |
|---|---|---|
| /p/ | loan-only, marginal; substitutes to /b/ | "mostly found in names or loanwords from English, French and Persian, not Literary Arabic"; many Egyptians cannot pronounce it [wiki-egy-phonology §Consonants note 2, citing Watson 2002 p.22]. Hafez: "[p] is an allophone of /b/", e.g. [sapt] for /sabt/ 'Saturday' [ema1958 §13 n.1]; `p → b` word-initially, medially and finally [ema1958 §14]. Galal: "Arabic has no /p/, the available alternative is [b]", works "systematically for the loanwords" [kwpl-ot-cairene-loan p.5]. |
| /v/ | loan-only, marginal; substitutes to /f/ (also /b/, /w/) | [wiki-egy-phonology §Consonants note 2]; "[v] is an allophone of /f/", e.g. [ravd] for /rafd/ 'refusal', "mainly found in loanwords" [ema1958 §13 n.1, §15]. |
| /ʒ/ | loan-only, marginal; substitutes to /ʃ/ | "tends to merge with [ʃ]": garage is mostly [ɡɑˈɾɑːʃ] "even by educated speakers" [wiki-egy-phonology §Consonants note 2]. Hafez agrees, attributing the /ʃ/ outcome to a Coptic substrate: garaaǧ ~ garaaš [ema1958 §17]. |
| /rˤ/ | **underlying emphatic** for Broselow; "additional marginal consonant" for Watson | Broselow lists /tˤ dˤ sˤ zˤ **rˤ lˤ**/ as the underlyingly emphatic set [broselow1976 p.xiii]. Watson calls /ɾˤ bˤ mˤ lˤ/ "additional consonants ... with marginal status", with minimal pairs [ˈbɑʔɑɾi] 'my cows' vs [ˈbæʔæɾi] 'cow-like' [wiki-egy-phonology §Consonants note 4, citing Watson 2002 p.22]. `CONFLICT:` underlying (Broselow) vs. marginal (Watson) — but both have /rˤ/ and /lˤ/. **Abdel-Massih sides with Broselow**: "the emphatic counterparts of the PLAIN /t d s z l r/", six phonemic emphatics /tˤ dˤ sˤ zˤ lˤ rˤ/ [abdelmassih-intro p.6]. `CONFLICT` again with hassig2011-cairene p.13–14, which has four and analyses [lˤ rˤ] as allophones. Two of three sources give six. |
| /bˤ mˤ/ | marginal, chiefly in loans | minimal pair /bˤaːbˤa/ [ˈbɑːbɑ] 'patriarch' vs /baːba/ [ˈbæːbæ] 'Paopi' [wiki-egy-phonology §Consonants note 4]. Broselow reports only `mayya` /ˈmɑjjɑ/ 'water' as an /mˤ/ candidate, and notes transcribers disagree about it [broselow1976 p.57 n.8]. She does **not** report emphatic /b/ or /f/ as a class. |
| /q/ | marginal; learned/Literary vocabulary only | `CONFLICT` and detail in §0 above. In Broselow's terms /q/ is the one segment that is **always** emphatic: "All segments except /q/ occur both emphatic and non-emphatic" [broselow1976 p.32], and it triggers emphasis in its syllable [broselow1976 p.xiii]. Note Hafez treats /q/ as an available segment that loans can be *given*: `k → q / _ back V` (see §3) [ema1958 §19–20]. |
| /ŋ/ | not a phoneme; occurs as an allophone of /n m/ before a velar | /m/ → [ŋ] before a velar within the phonological word [hassig2011-cairene p.35, p.65 n.10]. Cairene also has /nb/ → [mb] (/zanb/ → [zæmb]) [wiki-egy-phonology §Assimilation]. Loan data shows source /ŋ/ simply **retained**: 'spring' → [ʔispiriŋ] [broselow-position-quality p.295]; Hafez's data has `weng` 'wing', `zegzaag`, `t(e)reng` with `ng` and no comment [ema1958 §32, §24]. |
| /tʃ/ | not native; → /ʃ/, though increasingly retained | šebs~šibs 'chips', wenš 'winch', marš 'march', konšertu 'concerto', šiili 'Chile' [ema1958 §17]; but hypercorrect /tšok/ 'shock' shows /tʃ/ being inserted where it does not belong [ema1958 §38], and Galal's data keeps it: `kalatʃ` 'clutch', `ʔisbiitʃ` 'speech' [kwpl-ot-cairene-loan p.2–3]. |
| /dʒ/ | not native; → /ʒ/ | "not very common in EA"; 'Jeep' /dʒiip/ → /ʒebb/ [ema1958 §17]. See §0 on the PHOIBLE row. |
| /θ ð ðˤ/ | absent | Inherited stratum → /t d dˤ/; learned stratum → /s z zˤ/ [wiki-egy-phonology §Consonants]. **For a non-Arabic donor the sibilant outcome is the stated one**: "Non-Egyptianized loanwords having interdental consonants (/θ/, /ð/) are approximated to the sibilants [s], [z]" [wiki-egy-phonology §Consonants note 5]. `CONFLICT:` Hafez says English loans give **/t/** — tormos 'thermos', termometr, termostaat (with /s/ only as a variant, sermostaat) and `talaata` 'three'; /s/ is the Classical/learned stratum, `saqaafa` [ema1958 §16]. |

**Loan-phoneme status is a social variable, not a phonological one.** Hafez is explicit: retention
of /p v ʒ tʃ/ and of initial clusters correlates with education, bilingualism and prestige, not
with phonological environment [ema1958 §15, §37–38, §57–60]. §60 states that frequency of use has
led to "the introduction into EA of such phonemes as /p/ and /v/ and of consonant clusters in
initial position" (brââvu 'bravo', trella 'trailer', kravat). Hypercorrection puts them in the
wrong places: /hapi persdej/ 'happy birthday', /prââvu/, /tšok/ 'shock', /kaveterja/ 'cafétéria'
[ema1958 §38]. The integration cline is stated for 'lamp': /lâmba/ (least integrated, "urban,
younger, better educated") > /lâmdâ/ > /lândâ/ (most integrated, "rural, older, less educated")
[ema1958 §58].
**Design consequence**: for a naming generator this is a register dial, not a rule. Pick one point
on the cline and hold it.

**Abdel-Massih's Table 1**, verified against the PDF, gives the same picture independently
[abdelmassih-intro p.2; abdelmassih-v3 pp.39–41]: `b t ṭ d ḍ k g q ʔ f s ṣ z ẓ š x ɣ ħ ʕ h m n
l ḷ r ṛ w y` plus starred `p* v* ž*` — "Occur in a few borrowed words, e.g. /pariis/ 'Paris',
/villa/ 'villa', /žakitta/ 'jacket'". /q/ has a full row but "occurs in borrowings from Modern
Literary Arabic" [abdelmassih-intro p.15]. There is **no /tʃ/** in his inventory: loans with a
donor affricate are written as a **t + š sequence** — `kutšeena` 'playing cards'
[abdelmassih-v4 p.314], `kawitš` 'tire' [abdelmassih-v4 p.147], `bilyatšu` 'clown'
[abdelmassih-v4 p.71]. **No /ŋ/** anywhere in his tables.

He also states a **final-devoicing allophone rule** no other source mentions: utterance-finally,
/r/ and /l/ devoice after a voiceless obstruent — `ʔatˤr̥` 'train', `ratˤl̥` 'pound', `ʔifl̥`
'a lock', `ʔasˤr̥` 'palace', `naʃr̥` 'publication' [abdelmassih-intro p.27; abdelmassih-v3 p.42].
*(Potentially useful: Irish voiceless sonorants have no other home — see §8.3.)*

### Vowels

Short **/i u a/** with allophones [ɪ~e], [ʊ~o], [æ]/[ɑ]; long **/iː uː eː oː aː/** with
[æː]/[ɑː] for /aː/ [wiki-egy-phonology §Vowels; lapsyd arabic-egy-arz]. Diphthongs /aj aw/ (also [ej ow])
exist as V+glide sequences and contrast with /eː oː/: /ʃajla/ [ˈʃæjlæ] 'carrying (f)' vs /ʃeːla/
[ˈʃeːlæ] 'burden' [wiki-egy-phonology §Vowels, citing Watson 2002 p.23].
- /eː oː/ derive historically from /aj aw/ and have **no short counterparts**: shortening turns
  them into [e o], which merge with shortened [iː uː] [wiki-egy-phonology §Vowel shortening].
  Broselow states this as a feature clause on the shortening rule: **mid vowels become high when
  shortened**, `eː → i`, `oː → u` [broselow1976 p.18–19].
- Long vowels are **always stressed** [wiki-egy-phonology §Vowels] (see §4).
- **[ɑ ɑː] in loans.** "the majority [of autonomous ɑ ɑː] are in words of non-Semitic origin —
  especially those derived from European languages — where [ɑ ɑː] echo the vowel quality of /a/
  in those languages" [wiki-egy-phonology §Emphasis spreading]. This is a directly usable rule:
  a donor back /a/ arrives as /ɑ/, phonemically or via a posited emphatic consonant.
- Hafez lists the loan-available vowel set as short /i e a â o u/ and long /ii ee aa ââ oo uu/
  [ema1958 §23], and claims /e/ and /i/ contrast (/kalbe bonni/ 'a brown dog' vs /kalbi bonni/
  'my dog is brown') [ema1958 §24].
  `CONFLICT: ema1958 §24 (/e/ and /i/ are separate phonemes) vs. wiki-egy-phonology §Vowel
  allophones (Watson 2002 p.22: short [e o] are not phonemes and "are not used by most speakers of
  Cairene") vs. Woidich 2006 p.7 (educated Cairenes distinguish them in careful slow speech only).`
  The [e]/[i] pair Hafez cites is in fact the well-known **epenthetic [e] vs. possessive [i]**
  contrast [wiki-egy-phonology §Epenthesis], which is a morphological, not a lexical, minimal pair.
  Recommendation: treat [e o] as allophones/epenthetic outputs, not phonemes.
  A **fourth** position: Abdel-Massih's Table 2 gives a symmetrical **ten**-vowel system
  /i u e o a iː uː eː oː aː/ with short /e o/ included, while conceding "the occurrence of short
  /e, o/ is not common in Egyptian Arabic" and offering only near-minimal pairs (`betna` 'our
  house' / `bitna` 'we spent the night'; `ʔotti` 'my room' / `ʔutti` 'my cat')
  [abdelmassih-intro p.21; abdelmassih-v3 p.316].

### Notational quirks of the PHOIBLE row

See §0. In short: strip the dental diacritics; delete /d̠ʒ/; read /χ ʁ/ as /x ɣ/; add /p v ʒ/
as marginal; read `a`/`æː` as /a/ ~ [æ ɑ] and /aː/ ~ [æː ɑː]; add "all consonants may geminate".

---

## 2. Syllable structure and phonotactics

### Maximal syllable template

**σ = C₁ V(ː) C₀₋₂**, i.e. exactly one onset consonant, obligatory; a short or long vowel; and
zero to two coda consonants, with two only word-finally
[ijllnet-cairene-english-syll p.95 (10); lapsyd arabic-egy-arz "Canonical Form (C)V(C)(C)";
broselow1976 p.34 (119); hassig2011-cairene p.31].

Six attested shapes, all sources agreeing on the set
[ijllnet-cairene-english-syll p.96 (11), citing Broselow 1988, Buell 1996, Mitchell 1960;
broselow1976 p.34; ojml-cairene-syllable p.260 (which lists five, omitting CVːCC); wiki-egy-phonology §Syllable structure]:

| shape | weight | example | gloss |
|---|---|---|---|
| CV | light | /la.ban/ | 'milk' |
| CVː | heavy | /saː.kin/ | 'inhabited (m.sg.)' |
| CVC | heavy (word-internally) | /mar.kaz/ | 'centre' |
| CVːC | superheavy | /mi.daːn/ | 'square' |
| CVCC | superheavy | /ka.tabt/ | 'I wrote' |
| CVːCC | extraheavy, rare, always a final geminate | /maːrr/ | 'passer-by' |

The last three (four) occur **word-finally only**
[ijllnet-cairene-english-syll p.98 — CVːCC is Khalifa's addition, from Mitchell 1960;
broselow-arabic-syll p.7 and hassig2011-cairene p.31 cover CVːC/CVCC only].
Watson tightens this: CVːC is licit word-finally anywhere in the utterance ([kitaːb kibiːr] 'a
big book'), but **CVCC is licit only utterance-finally** — non-utterance-finally it is broken by
epenthesis: /bint tˤawiːla/ → [binti tˤawiːla] 'a tall girl' [watson2011-word-stress p.2991].
Broselow says the same from the other direction: a word-final CC surfaces only in pause, since
epenthesis will otherwise supply a vowel after it [broselow1976 p.38].
Hassig adds that **CVː is banned word-finally** ("a result of a history in which long final vowels
were reduced to short final vowels") [hassig2011-cairene p.31, citing Watson 2002 p.56].

Explicitly impossible shapes [ijllnet-cairene-english-syll p.99]:
`*CCV *CCCV *CCVC *CVCCC *CCVː *CCVCC *CCVːCC *VC *VːC *VCC *VCCC`.

### Onsets

**Exactly one consonant, always.** No complex onsets and no onsetless syllables.
- "Every ECA syllable must begin with one and only one consonant" [broselow1976 p.48]; "#CC… is
  not a permissible sequence in ECA" [broselow1976 p.38]; "no ECA words begin with consonant
  clusters" [broselow1976 p.20].
- "Complex onsets are proscribed in ... dialects of Cairo and environs ... 'big' [is] disyllabic
  [ki.biir] in Cairene Arabic but ... monosyllabic [kbiir] in Syrian Arabic"
  [broselow-arabic-syll p.2].
- "CCA syllables must start with one and only one consonant"; template `O[C]`, hence `*O[V]`,
  `*O[CC]` [ijllnet-cairene-english-syll p.92–93].
- Maximal Onset Principle holds: "a single consonant followed by a vowel always shares [a]
  syllable with that vowel" [broselow1976 p.34; ijllnet-cairene-english-syll p.92].
- Hafez states the constraint as "no consonant clusters in syllable-initial position" and "no
  vowel in word/syllable-initial position" [ema1958 §11, §28–29].
- `CONFLICT:` **Abdel-Massih says word-initial CC is licit but very rare**: "The sequence C₁C₂
  initially is very rare; e.g. /kwayyis ~ kuwayyis/ 'good', /braavo/ 'bravo'"
  [abdelmassih-intro p.26 §8.1.1; verbatim abdelmassih-v3 p.42]. Both his examples are special —
  one alternates with a CVC form, the other is a European loan — and Hafez says prestige and
  hypercorrect speech now tolerate initial clusters (braavu, trella, kravat) [ema1958 §38, §60].
  Against this, Broselow: "no ECA words begin with consonant clusters" [broselow1976 p.20].
  This is a **register** question, not a description error. See §9.7.
- **Onset-cluster list: there is none.** For the integrated register the correct entry in a rule
  file is the empty set.

### Coda clusters

- **Word-medially: one consonant.** [ijllnet-cairene-english-syll p.94, citing Broselow 1992;
  ojml-cairene-syllable p.264; hassig2011-cairene p.31.]
  (Galal's rule (4c) reads "a maximum of two consonants may occur word medially"
  [kwpl-ot-cairene-loan p.4], which looks like a contradiction but is **not** one: he is counting
  a heterosyllabic C.C sequence straddling a syllable boundary, which everyone allows, while the
  others are counting the medial *coda*. Both amount to: medial coda = 1 C, medial cluster = 2 C,
  CCC banned. Recorded here because the surface wording invites a false conflict.)
- **Word-finally: two consonants.** [ijllnet-cairene-english-syll p.94; kwpl-ot-cairene-loan p.4
  rule (4b), with `faxr` 'pride', `ʔatl` 'killing'; broselow-arabic-syll p.2.]
- **CCC is banned everywhere**, including across a syllable or word boundary: "Sequences of three
  consonants are anathema in ECA" [broselow1976 p.1]; "the cluster CCC is not allowed in CA even
  if the cluster syllabifies into separate syllables" [kwpl-ot-cairene-loan p.7]; "Consonant
  clusters of more than two consonants are prohibited, not only tautosyllabically, but also over a
  syllable boundary" [ojml-cairene-syllable p.263]; "Three or more consonants are never allowed to
  appear together, including across a word boundary" [wiki-egy-phonology §Vowel insertion].
- **There is NO sonority restriction on the final CC.** This is the single most important
  phonotactic fact for Irish input, and Broselow states it as a typological oddity:
  > "Cairene Arabic is unusual among the world's languages in allowing **any combination of
  > word-final consonants regardless of sonority**, as for example in [ʔakl] 'food' with low
  > sonority [k] (a stop) followed by higher sonority [l] (a liquid)."
  > [broselow-arabic-syll p.3]

  Hassig reports the same as "no obedience to any sort of sonority hierarchy", with no positional
  pattern in the final CC [hassig2011-cairene p.31, there attributed to broselow1976 p.34 — note
  the word "sonority" does not itself occur in the dissertation, so this is Hassig's gloss].
  **No source gives an enumerated list of licit final CC**, because none is needed. Attested
  examples: `rd` (ward 'roses'), `mb` (kurumb 'cabbages'), `bt` (katabt 'I wrote'), `bn` (ʔibn
  'son'), `sm` (ʔism 'name') [ijllnet-cairene-english-syll p.94–95]; `lb` (kalb 'dog'), `nt`
  (bint 'girl'), `sˤrˤ` (masˤrˤ 'Egypt'), `kl` (ʔakl 'food') [broselow1976 p.34]; `xr` (faxr),
  `tl` (ʔatl) [kwpl-ot-cairene-loan p.4]; `ns` (gens 'jeans'), `lf` (balf 'valve'), `lt` (ʔasfalt),
  `lm` (felm 'film'), `nt` (tânt 'tante'), `tr` (letr 'litre'), `bl` (ʔestâbl 'stable'),
  `ks` (berifeks 'prix fixe') from loans — these are collected from across the article, not from
  one paragraph: only `letr` and `berifeks` are in [ema1958 §29]; the rest are scattered through
  §15–§55 (e.g. `balf` §15, `tânt` §20, `gens` §22, `felm` §46, `ʔasfalt` §55).

### Medial cluster limits

Two consonants maximum, heterosyllabic (C.C). A third triggers epenthesis (§3). The limit holds
**across word boundaries**, because Cairene syllabifies across words [broselow1976 p.1, p.35].

### Syllabification spans word boundaries

`katab # ilgawaab` → `[ka.ta.b# il.ga.waab]` 'he wrote the letter' [broselow-arabic-syll p.5];
`ilgumla gdiida` → `ilgumlag diida`; `bint kibiira` → `bintik biira`; `wi izzayyak inta` →
`wizzayya kinta` [broselow1976 p.35]. Broselow notes that failing to do this "results in a
judgment by a native speaker that one's pronunciation is 'non-Egyptian'" [broselow1976 p.36].
Wikipedia calls this **linking** and states its purpose as ensuring "that every syllable begins
with exactly one consonant" [wiki-egy-phonology §Vowel elision and linking].
*(For a name generator producing isolated words this matters mainly at the phrase level — e.g.
an epithet of two words. Word-internally it means the same one-onset rule applies throughout.)*

### Segment-position restrictions

- No consonant is barred from any syllable position: "no restrictions have been found"
  [hassig2011-cairene p.31, citing broselow1976 p.34].
- **/q/** occurs only in learned/Literary vocabulary [broselow1976 p.25; wiki-egy-phonology
  §Consonants note 5].
- **CVː is banned word-finally** [hassig2011-cairene p.31]; final long vowels historically
  shortened.
- **Unstressed word-initial CVː is not licit**: [ˈʃaːfit] 'she saw' vs [ʃaˈfitu] 'she saw him'
  — but /ʕalam-u/ 'his world' → [ʕaˈlamu], where the unstressed CVː reduces
  [watson2011-word-stress p.2991, p.3006].
- No syllabic consonants: `C nucleus allowed? No` [ijllnet-cairene-english-syll p.95].

### Vowel sequences / hiatus / glides

- **No two vowels in succession without an intervening consonant** [ema1958 §30];
  `VV nucleus allowed? No (but Vː allowed)` [ijllnet-cairene-english-syll p.95].
- Repairs: (a) **/ʔ/-insertion** to supply an onset (§3); (b) **/j/-insertion with compensatory
  lengthening** where the first vowel is /i/: `ia → iːja`, e.g. /masˤri/ + /a/ → [masˤriːja]
  'Egyptian (f.sg.)' [hassig2011-cairene p.34, p.65 n.9, citing Watson 2002 p.203];
  (c) **elision**, across word boundaries: when both vowels are the same, one elides; when final
  /i/ meets initial /a/, /i/ elides; when any vowel meets initial /i/, /i/ elides
  [wiki-egy-phonology §Vowel elision and linking].
- **/-a/ → /-it/ in the construct state** to keep two vowels apart: bâttârejjâ →
  bâttârejjet el-ʕârâbejjâ 'the car battery' [ema1958 §30]; mudarrisa → mudarrisit Fariid
  'Fariid's teacher' [broselow1976 p.62–63].
- Glides /j w/ are ordinary consonants and fill onset and coda slots.

### Gemination

- **"All consonants can appear geminate"** [lapsyd arabic-egy-arz §Consonant notes]. Abdel-Massih agrees
  and adds the position restriction: geminates occur **medially or finally, never initially**
  (`lissa` 'not yet', `bass` 'enough!'), and a geminate "has precisely twice the duration of a
  single consonant" — minimal pairs `sama` 'sky' / `samma` 'he named', `faani` 'mortal' /
  `fanni` 'technical', `hawa` 'air' / `hawwa` 'he fanned'
  [abdelmassih-intro pp.20, 24; abdelmassih-v3 p.257].
- A geminate closing a stressed penult is a productive target shape for loans: Hafez states the
  template **/CVCVCVCCV/** with examples kârâmellâ 'caramel', gârâfâttâ 'cravate', manafella
  'manivelle', and variants fanella 'flannel', bâttârejjâ 'battery', dântellâ 'dentelle',
  talleXrââf 'telegraph' [ema1958 §31]. Some geminates simply copy the donor spelling (villa >
  vella/fella), but not always: birra > /biira/, fattura > /fatuura/ [ema1958 §31 n.3].
- CVːCC (a final geminate after a long vowel) exists but is rare in Cairene:
  /maːrr/ 'passer-by', /haːmm/ 'important' [ijllnet-cairene-english-syll p.95].
- Cairene resists mora-sharing: rather than tolerate a word-internal long-segment sequence it
  **shortens** the long vowel (Closed Syllable Shortening, §3). Mora-sharing is permitted
  word-finally only [watson2007-syllabification p.350, p.354 (19d)].
- **No degemination rule is stated for Cairene** in any source consulted
  [hassig2011-cairene: `not covered`; watson2007-syllabification p.353 gives a degemination
  analysis but from **San'ani** data, not Cairene].

---

## 3. Repair strategies (loanword adaptation)

The two dedicated loanword sources are `ema1958` (Hafez 1996, ~40 pages of French/English/Italian/
Turkish loans in running text) and `kwpl-ot-cairene-loan` (Galal 2004, 20 English loans analysed
for epenthesis site and vowel quality). `broselow-position-quality` (2015) gives a third,
independent list. **They converge**, which is worth stating up front because it makes the
epenthesis rules unusually safe to implement.

### 3.1 Illicit onset cluster — the central rule, and it is SONORITY-CONDITIONED

Cairene has no complex onsets at all (§2), so every donor onset cluster must be repaired. Which
repair applies depends on the sonority profile of the cluster:

**(a) Rising sonority (obstruent + liquid/glide, and /s/ + liquid/glide) → ANAPTYXIS, vowel inserted
INSIDE the cluster, between C1 and C2. No glottal stop.**

`Ø → i / # C _ C V` where C1C2 rises in sonority

| donor | Cairene | source |
|---|---|---|
| freezer | firizar / firiizar | [kwpl-ot-cairene-loan p.2 (2a)]; [broselow-position-quality p.295 (2a)] |
| Bristol | biristul | [kwpl-ot-cairene-loan p.2 (2b)] |
| printer | birinter | [kwpl-ot-cairene-loan p.2 (2c)] |
| Crimplene | kirimbilin | [kwpl-ot-cairene-loan p.2 (2d)] |
| plastic | bilastik | [broselow-position-quality p.295 (2a)] |
| slide | silayd | [broselow-position-quality p.295 (2a)] |
| sweater | siwetar | [broselow-position-quality p.295 (2a)] |
| clutch | kalatʃ | [kwpl-ot-cairene-loan p.3 (3e)] |
| flash | filaʃ | [kwpl-ot-cairene-loan p.3 (3f)] |
| group | guruub | [kwpl-ot-cairene-loan p.3 (3d)] |
| crème | kereema | [ema1958 §29] |
| princess | berensiisa | [ema1958 §29] |
| platine | belatiin | [ema1958 §29] |
| protein | borotiin | [ema1958 §29] |
| classeur | kelaseer | [ema1958 §29] |
| balcon | balakoona | [ema1958 §29] |

Note **/sl/ and /sw/ pattern with the rising group** (silayd, siwetar), not with /s/+stop
[broselow-position-quality p.295 (2a)]. The split is /s/+**obstruent** vs everything else — but
Broselow hedges the sonorant side as "(and possibly some or all S-resonant clusters)", so /sm sn/
are **not** settled by this data. See §9.4.

**(b) /s/ + obstruent → PROTHESIS, vowel inserted BEFORE the cluster, plus an inserted
glottal stop to give the new syllable an onset.**

`Ø → ʔi / # _ s C[-son]`

(All attested cases are /s/-initial. Whether Irish slender /ʃ/ + obstruent behaves the same is
`(unattested)` — see §8.5.)

| donor | Cairene | source |
|---|---|---|
| ski | ʔiskii | [broselow-position-quality p.295 (2b)] |
| study | ʔistadi | [broselow-position-quality p.295 (2b)] |
| stereo | ʔistiryu | [kwpl-ot-cairene-loan p.2 (2e)] |
| speech | ʔisbiitʃ | [kwpl-ot-cairene-loan p.2 (2f)] |
| staff | ʔistaf | [kwpl-ot-cairene-loan p.3 (3h)] |
| stock | ʔistuk | [kwpl-ot-cairene-loan p.3 (3i)] |
| stop | ʔistub | [kwpl-ot-cairene-loan p.3 (3j)] |
| sport | ʔezbort | [ema1958 §29] |
| studio | ʔestodju | [ema1958 §29] |
| stable | ʔestâbl | [ema1958 §29] |

Broselow highlights that this is the *inefficient* option and that Cairene takes it anyway:
> "a particularly inefficient repair choice; because vowel-initial syllables are banned in
> Arabic, pre-cluster insertion necessitates an additional repair, the insertion of a glottal
> stop before the inserted vowel" — and `si.kii` "would constitute an entirely unobjectionable
> surface structure in this language (cf. [sikitt] 'I became quiet')", yet speakers do not use it.
> [broselow-position-quality pp.297–298]

Note the /s/ voices before a following voiced obstruent: sport → /ʔezbort/, Sprite →
/ʔezberâjt/, spray → /ʔezbereej/ [ema1958 §29] (source /p/ has become /b/, and /s/ agrees).

**(c) Three-consonant onset (sCC) → both repairs at once.**
English *street* → /ʔistiriit/ — prothesis + glottal stop, and anaptyxis in the remaining /tr/;
two vowels inserted [broselow-position-quality p.298 n.5]. Same shape in Hafez: *stretch* →
/ʔes-te-retš/ [ema1958 §29], and in the L2 data: *spring* → ʔisbiring, *spleen* → ʔisbileen
[ijllnet-cairene-english-syll p.108].

`CONFLICT (internal to Broselow, and it matters).` broselow1976 p.23 rule (80) states Word-Initial
Epenthesis as **unconditional prothesis** `Ø → i / # _ CC`, with no sonority condition and no
glottal stop: imperatives `iktib` 'write!', `iʃrab` 'drink!', `irmi` 'throw!', `imʃi` 'go!'; derived
verbs `itgamaʕ`, `igtamaʕ`, `istaʔbil`; the article /l/ → `il`. broselow-position-quality p.295
gives the sonority-conditioned mixed system above.
**These are not really in competition** — 1976 describes clusters derived by *native morphology*,
2015 describes *borrowing*. **For an Irish-input generator, implement the 2015 mixed pattern.**
Hafez independently confirms the mixed pattern for loans [ema1958 §29] and even records a doublet:
*classeur* → /ʔaklaseer/ (prothesis) ~ /kelaseer/ (anaptyxis).

### 3.2 Three-consonant sequences (CCC) — epenthesis after C2

This is the classic Cairene parameter, and every source agrees.

`Ø → i / C C _ C`  (applies word-internally and across word boundaries)

Broselow's formal rule [broselow1976 p.2 (5)]:
`Ø → [+syll, +hi, −bk, −long] / X [−syll]₂ [−seg]₀ __ [−syll] Y`

| input | output | gloss |
|---|---|---|
| /ma-katab-t-ʃ/ | makaˈtabtiʃ | 'I didn't write' |
| /katab-t # dars/ | kaˈtabti dars | 'I wrote a lesson' |
| /il-dars # sahl/ | idˈdarsi sahl | 'the lesson is easy' |
| /bint # kibiira/ | bin.tik.biː.ra | 'a big girl' |
| /katab + t + l + u/ | ka.tab.ti.lu | 'I wrote to him' |
| /ʔult + l + u/ | ʔul.ti.lu(h) | 'I said to him' [kiparsky-syll-moras §1] |
| /il/ + /bint/ + /di/ | el ˈbente ˈdi | 'this girl' [wiki-egy-phonology §Vowel insertion] |
| banknote | bankinut | [kwpl-ot-cairene-loan p.2 (2h)] |
| shark skin | ʃarkiskiin | [kwpl-ot-cairene-loan p.2 (2i)] |
| postman | bustiman | [kwpl-ot-cairene-loan p.2 (2j)] |

Cross-dialect minimal contrast, which is what fixes the parameter
[broselow-arabic-syll p.9 (8)]:
Cairene `ka.tab.ti.lu` (insert between **C2 and C3**) vs. Iraqi `ki.ta.bit.la` (between C1 and C2).
Kiparsky agrees and classes Cairene as a **CV-dialect**: "Medial -CCC- clusters are broken up as
-CiCC- in VC-dialects, and as -CCiC- in CV-dialects" [kiparsky-syll-moras §1].
In a **CCCC** sequence both dialects insert between C2 and C3: Cairene `ka.tab.til.ha`
[broselow-arabic-syll p.9 (7)].

`CONFLICT: ema1958 §29 does not describe C2–C3 epenthesis at all.` Hafez's loan data uses only
prothesis and C1–C2 anaptyxis, and she frames the goal as "to preserve the maximal syllabic length
CVCC". This is not a contradiction so much as a gap: her data are word-initial clusters, where
C2–C3 is not at issue; Broselow's and Galal's C2–C3 cases are word-internal. Implement both.

### 3.3 Epenthetic vowel quality

**Default: /i/, realized [e] (and strictly [e] word-finally).**
- Native rules insert an invariant `[+syll, +hi, −bk, −long]` = /i/, in both the medial and the
  word-initial rule; Broselow treats the identity of the vowel as evidence they are one process
  [broselow1976 p.2 (5), p.23 (80)]. No copy behaviour, no consonant conditioning.
- Wikipedia: "an epenthetic [e] is inserted between the second and third consonants ... analyzed
  as /i/"; word-finally the epenthetic vowel is strictly [e], contrasting with possessive [i]
  [wiki-egy-phonology §Vowel insertion, §Epenthesis].
- Hafez's prothetic vowel is /e/ in nearly all examples, /a/ in one (ʔaklaseer) [ema1958 §29].

**In loans, Cairene is a *default-vowel* language in BOTH positions** — this is Broselow's
typological finding and Cairene is the sole listed exemplar of the pattern:
> Cairene = `TiRA, iSTA`: /i/ inside obstruent–sonorant clusters **and** /i/ before /s/-stop
> clusters. Every other surveyed language with both positions uses a *copy* vowel in the
> anaptyctic position and a default only in the prothetic one.
> [broselow-position-quality p.309 table (21)]

**But there is a documented rounding/harmony exception in the ANAPTYCTIC position only:**
> "In both Cairene and Makkan Arabic, the high round vowel [u] may appear as the anaptyctic vowel
> when the next lexical vowel is round." [broselow-position-quality p.295 n.4]
> "…there is a tendency to insert a round vowel within obstruent–resonant clusters when the
> following vowel is round (Galal 2004; Ahyad 2013), suggesting that there may not, in fact, be
> clear cases of pure default systems." [broselow-position-quality p.309]

Galal is the cited data. His set [kwpl-ot-cairene-loan p.3 (3), p.13]:
- **[u]** when the following vowel is round: burujiktur 'projector', fulurusint 'fluorescent',
  furuut 'fruit', guruub 'group' — "the epenthetic [u] is a copy of the immediately following
  vowel", a **full** correspondence.
- **[a]** in the single case kalatʃ 'clutch' (following vowel /a/).
- **[i]** in filaʃ 'flash', kilaʃ 'clash', and in **all** the prothetic cases ʔistaf, ʔistuk,
  ʔistub — where "such correspondence is only partial".
Galal's own generalization is that the vowel harmonizes in **backness and roundness** (and in the
[u] cases, height) with the immediately following vowel, and that harmony is **blocked** in
(i) the s+obstruent prothetic site and (ii) compound-internal C2–C3 epenthesis (bankinut,
ʃarkiskiin, bustiman all take [i] regardless) [kwpl-ot-cairene-loan pp.13–17].

Hafez's data are consistent with harmony in the anaptyctic site — borotiin (o…o), berensiisa
(e…e), kereema (e…ee), balakoona (a…a), korwâsoon (ɑ…oo) — and she separately says vowels are
altered "to avoid variation and create harmony within a word … through duplication of the same
vowel in adjacent syllables" [ema1958 §25]. She does not connect the two statements; the
connection is an inference.

**A usable rule, in decreasing confidence:**
1. prothetic site (before /s/+obstruent): always **/i/**;
2. C2–C3 site: always **/i/**;
3. anaptyctic site (inside a rising-sonority onset): **/i/** by default; copy the following
   vowel's backness+roundness where that vowel is round or low — i.e. /u/ before a round vowel,
   optionally /a/ before /a/.

**One further conditioning, from the native morphology.** Abdel-Massih states the helping vowel
rule as `Ø → I / C C _ C` — "always added between the second and third consonants" — with the
vowel "a variant of /i/ which is usually **shorter and more lax** than the other variants",
written raised `ⁱ`, and deliberately contrasted with true /i/: `/dars + sahl/` → `dars ⁱ sahl`
'an easy lesson' vs `/darsi + sahl/` → `darsi sahl` 'my lesson is easy'
[abdelmassih-intro pp.24, 27–28; abdelmassih-v3 pp.37, 321–322]. Where the CCC arises from a
**pronominal suffix**, the quality is conditioned by the suffix: **/u/ before `-hum` and `-kum`,
/a/ before `-ha`, /i/ elsewhere** — `kalb` 'dog' → `kalbúhum` 'their dog', `kalbúkum`,
`kalbáha` 'her dog', `kalbína` 'our dog'; `gibt` → `gibtúhum`, `gibtáha`, `gibtílu`
[abdelmassih-v3 p.322]. **And that inserted vowel takes stress if the stress rule calls for it**
(see §4). One exception: a consonant-initial agreement suffix on a doubled stem inserts **/eː/**
instead — `sabb` 'he cursed' → `sabbeet` 'I cursed', `sabbeena` 'we cursed'.

**Nothing in any source conditions the epenthetic vowel on an adjacent consonant** — not on
emphasis, not on place. `not covered` [kwpl-ot-cairene-loan, ijllnet-cairene-english-syll,
ojml-cairene-syllable, broselow1976, broselow-position-quality: all silent].

### 3.4 Illicit coda cluster

Cairene accepts **any** final CC regardless of sonority (§2), so a two-member donor coda usually
needs no repair at all. Hafez's data confirms: /ʔestâbl/ 'stable', /termometr/ 'thermometer',
/letr/ 'litre', /balf/ 'valve', /ʔasfalt/ 'asphalt', /tajbest/ 'typist', /berifeks/ 'prix fixe',
/tânt/ 'tante', /bont/ 'point', /felm/ 'film', /marš/ 'march', /wenš/ 'winch', /šebs/ 'chips',
/gens/ 'jeans' — again gathered from across the article, not from a single paragraph;
see the citation note in §2.
A **three**-member donor coda falls under the CCC rule and is broken after C2 — attested only in
the L2 data: *strength* → strengith, *tempts* → tempits
[ijllnet-cairene-english-syll p.110, flagged there as L2 production, not lexicalized loans].
Hafez's one relevant lexical case is *half time* → /haftajem/ [ema1958 §29].

### 3.5 Deletion

**Cairene repairs by epenthesis, not deletion.** Galal is explicit:
> "CA seems to show a preference for epenthesis over deletion" … "The fact that CA opts for
> epenthesis rather than deletion as a strategy for adapting loanwords provides a piece of
> evidence to the cross-linguistically attested fact that epenthesis is a much more frequent
> repair strategy in loanwords than deletion." [kwpl-ot-cairene-loan p.4 and pp.17–18]

No consonant deletion appears anywhere in his English→Cairene data. (Aquil's deletion data
[ojml-cairene-syllable p.264–265] is native-Cairene phrasal high-vowel syncope, a different
process — see 3.7.)

The one deletion process Hafez reports is **syllabic omission**, and it is lexical/morphological,
not phonotactic [ema1958 §32]:
1. **Truncation toward a 3- or 4-consonant root**: training suit → /t(e)reng/, automatic →
   /tomatiiki/, automobile → /tombiil/ ~ /ʔotombiil/, accelerator → /ʔakserateer/, cinéma →
   /siinima/.
2. **Loss of a word-initial syllable homophonous with the definite article /el-/**: Italian
   *alfino* → /fiinu/ 'bread'; *élastique* → /ʔastek/.
3. **Multi-word expressions lose a word**: power steering → /bâwâr/, self adhesive → /self/,
   answering machine → /ʔânsâr/.

### 3.6 Absent segment → substitute

Attested mappings first; `(fallback)` marks a feature-nearest guess.

| donor segment | Cairene | evidence |
|---|---|---|
| /p/ | **b** | bântâloon 'pantalon', banduul 'pendule', boliis 'police', bâsboor 'passeport', debloom 'diplôme', bajeb 'pipe' [ema1958 §14]; ʔistub 'stop' [kwpl-ot-cairene-loan p.5]; bebsi 'Pepsi' [wiki-egy-arabic §Romanization]. Retained as [p] in prestige speech. |
| /v/ | **f**, also **b**, **w** | fella 'villa', fektorja 'Victoria', fêtees 'vitesse'; koberta 'couverture', wâbuur 'vapeur', bârândâ 'véranda'; balf 'valve', monâwrâ 'manoeuvre' [ema1958 §15]. Retained as [v] in prestige speech (viitu 'veto', viiza 'visa'). |
| /ʒ/ | **ʃ** | garaaš 'garage', debrejaaš 'débrayage', šaketta 'jaquette' (rural) [ema1958 §17]; [ɡɑˈɾɑːʃ] "even by educated speakers" [wiki-egy-phonology §Consonants note 2]. Retained as [ʒ] in prestige speech. |
| /dʒ/ | **ʒ** (thence often ʃ) | 'Jeep' → /ʒebb/ [ema1958 §17]. |
| /tʃ/ | **ʃ** | šebs 'chips', wenš 'winch', marš 'march', konšertu 'concerto', šiili 'Chile' [ema1958 §17]. Often retained: kalatʃ 'clutch', ʔisbiitʃ 'speech' [kwpl-ot-cairene-loan p.2–3]. |
| /θ/ | **t** (English loans) / **s** (Classical loans) | tormos 'thermos', termometr, termostaat ~ sermostaat, and `talaata` 'three'; the /s/ side is the Classical stratum, `saqaafa` ~ `saʔaafa` < *thaqaafah* [ema1958 §16]. `CONFLICT:` "Non-Egyptianized loanwords having interdental consonants (/θ/, /ð/) are approximated to the sibilants [s], [z]" [wiki-egy-phonology §Consonants note 5]. |
| /ð/ | **z** (learned) / **d** (inherited) | ʔizaːʕa < ʔiðaːʕa; deːl < *ðajl [wiki-egy-phonology §Consonants]. `not covered` by ema1958. |
| /q/ (donor) | **ʔ** or **k** | "Non-Egyptianized loanwords with /q/ may either be Egyptianized to [ʔ] or approximated to [k], with the front vowel /æ/ being backed to [ɑ] in a word having an open vowel in the latter case" [wiki-egy-phonology §Consonants note 5]. |
| /g/ (donor) | **g** normally, but **ʁ~ɣ** in a documented set | fonoXrââf 'phonograph', talleXrââf 'telegraph', mâXnâtiis 'magnet' — Hafez attributes this to Levantine jīm making ġayn the Arabic script's way of writing foreign /g/ [ema1958 §21, note 2]. A spelling-mediated, not a phonetic, repair. |
| /ŋ/ | **ŋ** (retained) or **ng** | 'spring' → ʔispiriŋ [broselow-position-quality p.295]; weng 'wing', zegzaag, t(e)reng [ema1958 §24, §32], with no comment from either author. |
| /x/, /ɣ/, /h/ | **x**, **ɣ**, **h** — native, no repair | [wiki-egy-phonology §Consonants]. Neither Hafez nor Galal has occasion to discuss them as inputs: `not covered` as a loan mapping, but the segments exist. |

**Idiosyncratic substitutions** Hafez reports with no stated conditioning [ema1958 §22]:
`z → s` (jeans > gens), `k → g` (cravate > gârâfâttâ), `m → n` (album > ʔalboon, diplôme >
dabloon), `n → m` (piston > bestem), `n → l` (journal > gornâân ~ gornââl,
"duplicating the same consonant for ease of pronunciation" — note the source **states** the
direction as `/n/ → /l/` while its example shows French /l/ surfacing as /n/; the statement and
the datum disagree, and the datum is the usable one). Two that *are* explicable, by voicing agreement within the cluster:
pizza → /betsa/ ~ /bedza/ "so that the two successive consonants are either both voiceless or both
voiced"; passeport → /bâzboor/, `s → z / _ b` agreeing with the /b/ that replaced source /p/.

### 3.7 Word-edge processes

- **Initial glottal-stop insertion, obligatory.** Cairene bans vowel-initial syllables, so any
  vowel-initial word acquires [ʔ]:
  `Ø → ʔ / # _ V` [broselow1976 p.25 (85) (optional, word-initial); p.49 (164) Late-ʔ-Insertion
  (obligatory, syllable-initial); hassig2011-cairene p.33; wiki-egy-phonology §Syllable structure].
  Loan evidence: accessoire → /ʔekseswââr/, autobus → /ʔotobiis/, hôtel → /ʔoteel/, élastique →
  /ʔastek/ [ema1958 §28]; [ʔotobiːs] [broselow-arabic-syll p.2]; America → [ʔamriːka]
  [ojml-cairene-syllable p.260].
  Broselow's ʔ-Insertion is ordered **before** the CCC rule, so an inserted [ʔ] can itself be the
  third consonant and trigger epenthesis: /ʃugl ʔibnak/ → ʃugli ʔibnak 'your son's work'
  [broselow1976 pp.25–26 (87): "an initial glottal stop is counted as a
  third consonant, triggering the application of I Ep"].
- **No final devoicing** is reported by any source. `not covered` — and given `gens`, `zegzaag`,
  `ʒebb`, `katsabb`, final voiced obstruents plainly survive [ema1958 §31, §22].
- **Final-vowel addition**: not a general rule, but see §3.9 — inanimate loans strongly prefer to
  end in feminine /-a/.

### 3.8 Vowel adaptation

**Donor vowel LENGTH is not inherited. Length is assigned by Cairene stress.** This is the single
most consequential statement in the loanword literature for an Irish-input generator, and Hafez
states it directly:
> "vowels are especially lengthened when they are in a stressed syllable, **stress following EA
> patterns rather than following the model pronunciation of the loanword in the SL**. Such
> lengthening is basic to stressed syllables in EA as it is a syllable-timed language while many
> of the SLs of loanwords are stress-timed ones, not linking length and stress."
> [ema1958 §26]

Examples: gaˈloon 'gallon', sâˈloon 'salon', ˈluuri 'lorry', kaˈtaawet 'cutout', maˈdaam 'madame',
seˈwiitâr 'sweater', dântˈeel 'dentelle', ʔetikˈeet 'étiquette', teliˈfoon 'telephone',
telefezˈjoon 'television' [ema1958 §26].

`CONFLICT (a gap, not a disagreement): bib.md describes broselow-stress-adaptation as covering
"what happens to source-language stress in loans". It contains no Arabic loanword data at all` —
its case studies are Spanish→Huave, English→Fijian, Spanish→K'ichee', Indonesian→Selayarese, and
Arabic appears only in one footnote about stress *perception* [broselow-stress-adaptation p.482].
So `ema1958 §26` is the **only** source we have for loan stress/length in Cairene.

**Donor short-vowel mappings actually stated** [ema1958 §23–24]:

| donor vowel | Cairene | examples |
|---|---|---|
| Fr. /ø œ/ (`eu`) | **eː** | kwafeer 'coiffeur', šofeer 'chauffeur' |
| Fr. /ø œ/ (`eu`) | **oː** | doktoor 'docteur', motoor ~ mâtoor 'moteur' |
| Fr. /y/ (`u`) | **uː** | banduul 'pendule' |
| Fr. /y/ (`u`) | **eː** | karikateer 'caricature', badikeer 'pédicure' |
| Fr. /y/ (`u`) | **iː** | manikiir 'manucure', ǧiiba 'jupe' |
| Eng./Fr. /ɪ i/ | **e** (a stated preference for /e/ over /i/) | vella 'villa', weng 'wing', sewetch 'switch', zegzaag 'zigzag', gens 'jeans', letr 'litre' |
| Eng./Fr. /i/ | **i** (exception) | dikoor 'décor' |
| unstressed /o/ | **a** | mâtoor 'moteur', dâktoor 'docteur' |
| unstressed /i/ | **a** | manafesto 'manifesto' |
| any **stressed** vowel | the corresponding **long** vowel | galoon, sâloon, luuri, madaam |

**Reduced vowels / /ə/**: `not covered` explicitly. The nearest statement is the general
preference for **/a/ in unstressed syllables** [ema1958 §24], plus vowel harmony, where an
unstressed vowel copies a neighbour: aluminium → /ʔalamonjom/ (Ca-Ca-CoC-CoC), chiffonier →
/šofoniira/ (Co-Co-CVVCV) [ema1958 §25].

**Diphthongs**: `not covered` as a rule. The data incidentally show donor diphthongs surfacing as
V+glide sequences: /ʔofsâjed/ 'offside', /ʔezberâjt/ 'Sprite', /kataawet/ 'cutout', /fawel/ 'foul'
[ema1958 §26, §29], and /silajd/ 'slide' [broselow-position-quality p.295].

**Cairene-internal length rules that will bite any long donor vowel** — these are native rules,
well attested, and they run after adaptation:
1. **Closed-syllable shortening**: `Vː → V / _ C C`. The rule is Broselow's (55)/(60)
   [broselow1976 pp.18–19]; her own examples are at rule 3 below. The stock illustrations come
   from the other two sources: /kitaab+na/ → `ki.tab.na` 'our book'
   [broselow-arabic-syll, ex. (6)]; /baːb+ha/ → `babha` 'her door' and /kaːtib+a/ → `katba`
   'writing (f.sg.)' [watson2007-syllabification p.340]. Watson's table marks Cairene "CSS: Yes" as against San'ani/
   Palestinian "No" — it is a Cairene-specific repair [watson2011-word-stress p.3013].
   Broselow 2018 adds that the result is **fully neutralized** with an underlying short vowel
   (durationally identical) [broselow-arabic-syll p.8].
2. **Unstressed long vowels shorten**: `Vː → V / [−stress]` — /joom/ 'day' → yuˈmeen 'two days';
   /habbeena/ 'we loved' → ma habbiˈnaaš; /ʕalam-u/ → [ʕaˈlamu]
   [broselow1976 p.19 (60); watson2011-word-stress p.3006, p.3013].
3. **Mid vowels raise on shortening**: `eː → i`, `oː → u`, because Cairene has no short mid
   vowels — /beet/ 'house' → bitha 'our house'; /yoom/ → yumkum
   [broselow1976 pp.18–19]. Wikipedia's version: shortened [iː uː] "collapse with [e o], which
   are, as well, the shortened form of [eː oː]", making /gibna/ 'cheese', /giːb+na/ 'we brought'
   and /geːb+na/ 'our pocket' all [ˈɡebnæ] [wiki-egy-phonology §Vowel shortening].
   `CONFLICT` in surface transcription only: Broselow writes the shortened output as high /i u/,
   Wikipedia as mid [e o]. Both describe the same neutralization; the difference is whether [e o]
   are written as allophones of /i u/. Adopt: shortened /eː oː/ merge with short /i u/, realized
   [e o].
4. **One long vowel per word.** Abdel-Massih makes this an explicit generalization: "EA does not
   permit more than one long vowel in a word; in the case of two long vowels (resulting from
   morphological suffixation), **the first is shortened and stress shifts to the second**" —
   `ʃaalu` 'they carried' + `-u` → `ʃaaluu` → `ʃaluu` 'they carried it'; `miil` → `mileen`
   'two miles'; `beet` → `biteen` 'two houses'; `magnuun` → `magnuniin` 'crazy (p)'
   [abdelmassih-intro p.24 §7.2(d), p.25 §7.5; abdelmassih-v3 pp.319, 325]. His compact rule is
   `Vː → V / _ {CC, C V́}` [abdelmassih-v3 p.318].
   **This is a strong constraint on Irish input**: an Irish word with two long vowels
   (Matánach /ˈmˠat̪ˠɑːnˠəx/ has one; many have two) can keep only one.
5. **Vowel lengthening**: final short vowels lengthen when stress moves onto them by suffixation:
   /katabu/ + /-ha/ → /kataˈbuːha/ [wiki-egy-phonology §Vowel lengthening].
6. **High-vowel deletion (syncope)**: `i, u → Ø / V C _ C V` when unstressed and short — fihim +
   -u → fihmu 'they understood'; kaatib + -a → katba; ṣaaḥib + -a → ṣaḥba
   [broselow1976 p.20 (63)]. Blocked where it would create CCC (fihim + -t → fihimt, not
   *fihmt) and blocked by stress (huwwa ʃírib, not *huwwa ʃrib) [broselow1976 p.4]. Only **high**
   vowels syncopate in Cairene [watson2011-word-stress p.3013]. Broselow notes Classical/MSA
   borrowings are lexically marked as exempt: taaliba 'student (f)', malika 'queen', Faatiha —
   against the native participle fatha 'opening (f)' [broselow1976 pp.6–7].

**Rule ordering.** Broselow gives the whole of ch.1 as an ordered list [broselow1976 pp.54–55]:
```
L-Assimilation → ʔ-Insertion → Word-Initial Epenthesis → V-Deletion Across Word Boundaries
→ I-Epenthesis → Stress Assignment → Stress Retraction → High Vowel Deletion → Vowel Shortening
→ Syllabication Rules I–IV → Emphasis Spread → Right Emphasis Spread → Left Emphasis Spread
→ Late ʔ-Insertion
```
Two orderings inside this are load-bearing and independently confirmed:
- **Epenthesis precedes syncope** — /bint/ + /kibiːra/ → epenthesis /bintikibiːra/ → syncope
  /bintikbiːra/ [hassig2011-cairene p.34; wiki-egy-phonology §Multiple processes;
  broselow-arabic-syll p.12].
- **Epenthesis precedes stress** — see §4.

### 3.9 Other reported processes

- **Gemination toward a target template.** Hafez states the productive loan shape as
  **/CVCVCVCCV/**: kârâmellâ 'caramel', gârâfâttâ 'cravate', manafella 'manivelle'; also fanella,
  bâttârejjâ, dântellâ, talleXrââf [ema1958 §31]. Other loan geminates: ǧebb 'jeep', katsabb
  'ketchup', sevenâbb 'seven up', došš 'douche', diss 'dish', trella 'trailer', fanne 'finished'.
- **Metathesis**, attributed to indirect transmission of the model [ema1958 §36]:
  pullover → /boloovâr/ ~ /boroovâr/ ~ /boroovâl/; litre → /letr/ ~ /retl/;
  flannel → /fanella/ ~ /falenna/; penalty → /benalti/ ~ /belenti/, with the plural /belentaat/
  built on the *transposed* stem. Socially marked: "a marker of little education and lower social
  class."
- **A feminine /-a/ on inanimate loans** — see §6.
- **Emphasis assigned to a loan consonant** — see §8, which is where the digest's Irish-relevant
  material on this lives.

---

## 4. Stress and length

### The rule

Watson and McCarthy give the **identical** algorithm; both trace it to Harrell 1957 and to
Langendoen's (1968) formulation of Mitchell's data
[watson2011-word-stress p.3003 (29), p.3004 (30); mccarthy1979-stress-syll p.446 (2), p.447 (5)].
**No CONFLICT between them.**

Weight, with the position-sensitivity that is the crux:
- **light** = CV, and **final CVC**.
- **heavy** = CVː, and **non-final CVC**.
- **superheavy** = CVCC, CVːC — word-final only.
> "a word-final CVC syllable fails to attract the stress: mʊˈdarris 'teacher', ˈʔabadan
> 'never'… In sum, there are two binary syllable weight distinctions, light versus heavy
> word-internally, and light and heavy versus superheavy word-finally."
> [mccarthy1979-stress-syll p.446]

Algorithm, quoted from Watson's (29) [watson2011-word-stress p.3003] and identical to
McCarthy's (2) [mccarthy1979-stress-syll p.446]:
1. **Stress a final CVː(C) or CVCC.** `kaˈtabt` 'I wrote', `ʔaˈbe(h)` 'his father',
   `sakaˈkiːn` 'knives', `tˤalaˈbaːt` 'demands'.
2. **Otherwise, stress the antepenult when the penult AND antepenult are light — unless the
   pre-antepenult is also light.** `ˈʔabadan` 'never', `muxˈtalifa` 'different (f.sg.)';
   cf. `kataˈbitu` 'she wrote it', which has a light pre-antepenult and so falls through.
3. **Otherwise, stress the penult.** `jikˈtibu` 'they write', `ʕaˈmalti` 'you (f.sg.) did',
   `marˈtaba` 'mattress', `ˈbeːtak` 'your (m.sg.) house'.

⚠ **Note carefully what step 2 does and does not say.** It fires only when the penult and the
antepenult are *both* light. **A heavy antepenult therefore REJECTS stress**, and it falls to the
light penult — this is the single most distinctive property of Cairene stress, and getting it
backwards will mis-stress a large share of generated names:
> "In words with a heavy antepenult, **Cairene stresses the light penult**, while most other
> dialects stress the antepenult: Cairene [madˈrasa] 'school' contrasts with Beirut/Damascene
> [ˈmadrase]." [watson2011-word-stress p.2991]

For runs of four or more light syllables, which step 2 cannot resolve, Watson and McCarthy both
give Langendoen's (1968) fuller rule: stress the penult or antepenult — whichever is separated by
an **even** number of syllables from the rightmost non-final heavy syllable, or, if there is
none, from the left word boundary [watson2011-word-stress p.3004 (30c);
mccarthy1979-stress-syll p.447 (5)]. Equivalently: group light syllables into left-headed pairs
from the left edge.

Cairene never retracts past the antepenult [mccarthy1979-stress-syll pp.459–460 — note the
passage makes this point about **Damascene**; the Cairene three-syllable window is implicit in
(29)/(2) rather than separately stated].

Wikipedia states the same rule as a right-to-left search, and it agrees
[wiki-egy-phonology §Stress]; so does LAPSyD's compact version from Mitchell 1962:
"stress falls on final long heavy syllable (CVVC, CVCC), otherwise penultimate syllable is
stressed, unless it and the preceding syllable are both CV, when the antepenultimate is stressed"
[lapsyd arabic-egy-arz §Stress]. Broselow's Conditions A/B/C are a fourth statement of it
[broselow1976 pp.7–8], and Abdel-Massih a fifth [abdelmassih-v3 p.254; abdelmassih-intro
pp.25–26]. His formulation is the mirror image of Watson's and is a useful sanity check on the
warning above: **"Primary stress is most frequently on the penult, e.g. yikˈtibu 'they write',
madˈrasa 'school'"**; the ultima is stressed if it has a long vowel or ends in two consonants
(`katabuu`, `katabt`); the antepenult is stressed "if the last three syllables have the structure
CVCVCV(C)" — `ˈʃabaka` 'a net', `ˈkatabit` 'she wrote', `inˈkasarit` 'it broke', `muxˈtalifa`
'different (f.sg.)'. He adds two sub-exceptions that go back to the penult: a CVCVCV(C) string
that is a feminine-singular perfect verb whose final V(C) is a pronoun suffix (`raˈmitu` 'she
threw it away'), and a broken plural with identical high vowels in the first two syllables
(`siˈbita` 'baskets', `nuˈmura` 'tigers'). He also notes that **long vowels are never unstressed**
[abdelmassih-intro p.25], and that shortening at a close word juncture does **not** move the
stress: `banaa` 'he built it' → `bana mbaariħ` [abdelmassih-v3 pp.254–255].

Worked examples. All are the sources' own, with the rule step that produces them
[watson2011-word-stress p.3003 (29); mccarthy1979-stress-syll p.446 (2); the four `wiki-` rows
from wiki-egy-phonology §Stress; `binˈtina` from watson2011-word-stress p.2992]:

| form | stress | gloss | step | source |
|---|---|---|---|---|
| ka.tabt | kaˈtabt | 'I wrote' | 1 (final CVCC) | watson2011 p.3003; mccarthy1979 p.446 |
| ʔa.be(h) | ʔaˈbe(h) | 'his father' | 1 | watson2011 p.3003 |
| sa.ka.kiːn | sakaˈkiːn | 'knives' | 1 (final CVːC) | watson2011 p.3003; mccarthy1979 p.446 |
| tˤa.la.baːt | tˤalaˈbaːt | 'demands' | 1 | watson2011 p.3003 |
| ʔa.ba.dan | ˈʔabadan | 'never' | 2 (penult+antepenult light, no pre-antepenult) | watson2011 p.3003 |
| mux.ta.li.fa | muxˈtalifa | 'different (f.sg.)' | 2 (pre-antepenult heavy) | watson2011 p.3003; mccarthy1979 p.446 |
| ka.ta.bi.tu | kataˈbitu | 'she wrote it' | 3 (pre-antepenult also light → step 2 blocked) | watson2011 p.3003; mccarthy1979 p.446 |
| jik.ti.bu | jikˈtibu | 'they write' | 3 (heavy antepenult rejects stress) | watson2011 p.3003 |
| ʕa.mal.ti | ʕaˈmalti | 'you (f.sg.) did' | 3 | watson2011 p.3003; mccarthy1979 p.446 |
| mar.ta.ba | marˈtaba | 'mattress' | 3 (heavy antepenult rejects stress) | watson2011 p.3003; mccarthy1979 p.446 |
| beː.tak | ˈbeːtak | 'your (m.sg.) house' | 3 | watson2011 p.3003; mccarthy1979 p.446 |
| mad.ra.sa | madˈrasa | 'school' | 3 — **the signature Cairene pattern**, vs Beirut/Damascene [ˈmadrase] | watson2011 p.2991 |
| bin.ti.na | binˈtina | 'our daughter' | 3 — with an **epenthetic** penult vowel | watson2011 p.2992 |
| ka.tab | ˈkatab | 'he wrote' | 3 (final CVC is light; only two syllables) | wiki-egy-phonology §Stress |
| ka.ta.bit | ˈkatabit | 'she wrote' | 2 | wiki-egy-phonology §Stress |
| kat.ba | ˈkatba | 'female writer' | 3 | wiki-egy-phonology §Stress |
| mak.ta.ba | mækˈtæbæ | 'library' | 3 (heavy antepenult rejects stress) | wiki-egy-phonology §Stress |

### Length

Contrastive: /i u a/ vs /iː uː aː/, plus /eː oː/ with no short counterparts. **Neutralized** in
three environments (all in §3.8): before CC, when unstressed, and (for /eː oː/) whenever
shortened, since the shortened output merges with /i u/. Long vowels are otherwise **always
stressed** [wiki-egy-phonology §Vowels]. Word-final CVː is banned [hassig2011-cairene p.31].

**Practical consequence for Irish input**: an Irish long vowel survives only if the Cairene stress
rule happens to put stress on that syllable and the syllable is not closed by two consonants.
Everywhere else it shortens — and /eː oː/ shorten all the way to [e o] ≈ /i u/.

### Stress vs. epenthesis ordering

**In Cairene, epenthetic vowels COUNT for stress.** Stress is computed after epenthesis.
> "In Cairene, a penultimate post-CVC syllable with an epenthetic vowel is stressed like any other
> penultimate post-CVC syllable: compare [binˈtina] 'our daughter' with [madˈrasa] 'school' and
> [fihˈmitu] 'she understood him'." [watson2011-word-stress p.2992]

Explicitly the opposite of Iraqi and Levantine, where epenthetic vowels are invisible to stress
[watson2011-word-stress p.2992; watson2007-syllabification p.340]. Kiparsky agrees:
Cairene /bint-na/ → binˈtiːna, stressed like makˈtaba [kiparsky-syll-moras §1]. Broselow's rule
order also has Word-Initial Epenthesis and I-Epenthesis before Stress Assignment, so the prothetic
vowel of an imperative can itself be stressed: ˈiktib 'write!' [broselow1976 p.23, pp.54–55].

`CONFLICT with bib.md, not between sources: bib.md describes broselow-stress-epenthesis as
covering "whether epenthetic vowels count for stress (Cairene among the cases)". It contains no
Cairene data` — its Arabic case study is **Iraqi** only. The Cairene answer above comes from
Watson.

### Source stress in loans

Ignored. Cairene stress is reassigned by the native rule, and the newly stressed vowel is then
lengthened [ema1958 §26, §33–35] — see §3.8. Hafez's own restatement of the rule for loans,
"whatever their SL" [ema1958 §34], is the same rule as above, with these worked cases:
dok-ˈtoor, bâs-ˈboor, ʔal-ˈboom, gor-ˈnâân, bân-tâ-ˈloon, te-li-ˈfoon, tal-leX-ˈrââf,
gen-tel-ˈmaan; kat-ˈsabb 'ketchup', ter-mo-ˈmetr, se-ven-ˈʔâbb 'Seven Up' (final CVCC);
ˈbaa-ku 'packet', ka-ˈtaa-wet 'cutout', bal-ˈloo-na 'balloon' (heavy penult);
ˈban-ju 'bagno', ka-ˈset 'cassette', ˈsam-bu 'shampoo', ˈwar-sa 'workshop', ko-ˈber-ta,
ga-ˈket-ta, bât-tâ-ˈrej-ja (penult).

---

## 5. Romanization

Two things are wanted here and they pull in opposite directions: a scholarly transcription that is
reversible, and a spelling an English reader will pronounce approximately right. For this project
the second is the deliverable, so the recommendation below is built on the convention Egyptians
themselves use for names — Wikipedia's Help:IPA/Egyptian Arabic gives it explicitly, saying "the
romanization of the examples is the commonly used form in Egypt" [wiki-help-ipa-egy].

### The reference table

| Cairene IPA | Arabic letter | Egyptian popular romanization | scholarly (Hinds/Badawi, Woidich) | Arabic chat ("Franco") |
|---|---|---|---|---|
| ʔ | ء أ إ آ ؤ ئ (and ق) | *unwritten* — Moamen مؤمن [ˈmoʔmen] | ʾ | 2 |
| b | ب | b — bawab [bæwˈwæːb] | b | b |
| t | ت | t — tout [tuːt] | t | t |
| tˤ | ط | **t** — Tarek [ˈtˤɑːɾeʔ] | ṭ | t |
| d | د | d — dakka [ˈdæʔʔæ] | d | d |
| dˤ | ض | **d** — damir [dˤɑˈmiːɾ] | ḍ | d |
| k | ك | k — kawarea [kæˈwæːɾeʕ] | k | k |
| g | ج | **g** — Gamal [ɡæˈmæːl] | g | g |
| q | ق | k — el Kahera [elqɑ(ː)ˈheɾɑ] | q | k |
| f | ف | f — foul [fuːl] | f | f |
| s | س ث | s — souk, Thamer | s | s |
| sˤ | ص | **s** — Sabah [sˤɑˈbɑːħ] | ṣ | s |
| z | ز ذ | z — zebala [zeˈbæːlæ] | z | z |
| zˤ | ظ | **z** — zabet [ˈzˤɑːbet] | ẓ | z |
| ʃ | ش | sh — shorba [ˈʃoɾbɑ] | š | sh / ch |
| x | خ | kh — kharif [xæˈɾiːf] | x (Woidich ḫ) | kh / 7' / 5 |
| ɣ | غ | gh — ghasil [ɣæˈsiːl] | ġ | gh / 3' |
| ħ | ح | **h** — hob [ħob] | ḥ | 7 |
| ʕ | ع | *unwritten*, or a/e — ein [ʕeːn] | ʿ | 3 |
| h | هـ | h — Hesham [heˈʃæːm] | h | h |
| m | م | m | m | m |
| n | ن | n | n | n |
| r ~ ɾ | ر | r — ragel [ˈɾɑːɡel] | r (Harrell ṛ for emphatic) | r |
| l | ل | l — lamba [ˈlɑmbɑ] | l | l |
| j | ي | y — yama | y | y / i |
| w | و | w — wesh | w | w / ou |
| p | پ (ب) | p — Peter [ˈpiːteɾ] | p | p |
| v | ڤ (ف) | v — Nevin [nɪˈviːn] | v | v |
| ʒ | چ (ج) | g/j — George [ʒoɾʒ] | ž | j |
| æ, ɑ | fatḥa / ا | a — Gamal, lamba | a (Spitta ɑ̈ / ɑ̊) | a |
| æː, ɑː | ا | a — Gamal, baba | ā | a |
| ɪ~e | kasra / ي | e — enti | i (Woidich e/i) | e / i |
| i, iː | ي | i — habibi | ī | i / ee |
| ʊ~o | ḍamma / و | o — ento | u (Woidich o/u) | o / ou |
| u, uː | و | ou — nounou, foul | ū | ou / oo / o |
| eː | ي | ei — leil [leːl] | ē | e / ei / ai |
| oː | و | o — roh [ɾoːħ] | ō | o |
| æj/ɑj | | ay — Ayman, mayya | ay | ay |
| æw/ɑw | | aw — dawla, dawra | aw | aw |
| ej | | ey — meyya | ey | ey |
[wiki-help-ipa-egy; wiki-egy-arabic §Romanization; wiki-romanization-arabic]

Abdel-Massih's own system, for decoding his books — **taken from the books themselves, not
from Wikipedia's comparison table, which describes it wrongly** (see digest-log.md correction 4):
emphatics with a **subscript dot** `ṭ ḍ ṣ ẓ ḷ ṛ`; `š ž` for /ʃ ʒ/; `x ɣ` for the dorsal
fricatives; `ħ ʕ` for the pharyngeals; **`ʔ` and `q` as two separate symbols** (a /ʔ/ deriving
from qāf is flagged in the lexicon with a parenthesised "(Q)", not with a distinct character);
`y` for /j/; **doubled vowels** `aa ii uu ee oo` for length; stress by acute accent
[abdelmassih-intro p.2, pp.4–6, p.29; abdelmassih-v3 pp.39–41, p.320 n.].

### Recommended output convention

Use the Egyptian popular column, with three deliberate departures where it under-differentiates in
a way that would make two generated names collide:

| Cairene phoneme | write | note |
|---|---|---|
| /b t d k g f s z m n l r h w/ | b t d k g f s z m n l r h w | as expected |
| /j/ | **y** | |
| /ʃ/ | **sh** | |
| /x/ | **kh** | English readers approximate this as /k/; acceptable |
| /ɣ/ | **gh** | |
| /ħ/ | **h** | merges with /h/ — **accept the merger**; the alternative (ḥ, 7) is unreadable |
| /ʕ/ | **a** initially/finally, **'** medially | e.g. /ʕeːn/ → *Ein*, /kæˈwæːɾeʕ/ → *Kawarea*. Wikipedia's convention leaves it unwritten; an apostrophe medially at least preserves the syllable count |
| /ʔ/ | **'** medially, unwritten initially | /ˈmoʔmen/ → *Mo'men* |
| /q/ | **q** | **departure** — the popular convention writes `k`, but /q/ vs /k/ is a real (if marginal) contrast and `q` is the English reader's expected spelling for an exotic back k |
| **emphatics /tˤ dˤ sˤ zˤ/** | **t d s z** | **accept the merger.** Every practical Egyptian convention writes them plain, and the emphasis is audible in the *vowel* colour, which the vowel spelling below carries |
| /p v ʒ/ | p v j | |
| /æ æː/ | **a** | |
| /ɑ ɑː/ | **a**, but see below | **departure** — where an emphatic-spread word would otherwise be spelled identically to its plain counterpart, write /ɑː/ as **aa** or **â**. This is the one place emphasis becomes visible in the romanization |
| /ɪ e/ | **e** | |
| /i iː/ | **i** | |
| /ʊ o/ | **o** | |
| /u uː/ | **ou** | *Foul, Nounou* — `ou` reads correctly to an English eye |
| /eː/ | **ei** | *Leil* |
| /oː/ | **o** | *Roh* |
| /aj aw ej/ | ay aw ey | |
| geminates | doubled letter | *Gaketta, Battareyya* |

**Ambiguities an English reader will hit** (accepted, listed so they are a decision and not an
accident): `h` = /h/ or /ħ/; `a` = /æ/ or /ɑ/, short or long; `o` = /ʊ/ or /oː/; `sh`, `kh`, `gh`
read as digraphs, not clusters; `'` = /ʔ/ or /ʕ/; the emphatic/plain contrast is invisible.
Length is largely unmarked, which is faithful to Egyptian practice but loses a real contrast — if
the generator ever produces a minimal pair, mark the long vowel by doubling.

---

## 6. Morphology usable for epithets

Ten productive patterns, in rough order of usefulness for a naming/epithet generator.

### 1. Definite article `il-` (with sun-letter assimilation)

Form **/il-/**, Cairene, *not* MSA `al-`. Underlyingly /ʔil-/, and the /ʔ/ "almost always elides"
[abdelmassih-intro p.29].

- **Obligatory assimilation** before /t tˤ d dˤ s sˤ z zˤ r rˤ n ʃ/ — Abdel-Massih's set is "a
  following dental consonant or a following /ʃ/", **which includes /ʃ/**:
  `ittaman` 'the price', `itˤtˤaalib` 'the student', `iddamm` 'the blood', `issamaka` 'the fish',
  `isˤsˤabuuna` 'the soap', `izzibiib` 'the raisins', `irraagil` 'the man', `innaas` 'the people',
  **`iʃʃams`** 'the sun' [abdelmassih-v3 pp.83–84].
- **Optional** assimilation before /k g/: `ilkalb ~ ikkalb` 'the dog', `ilgamal ~ iggamal`
  'the camel' [abdelmassih-v3 p.83].
- **After a vowel the article is `l-`**, and still assimilates: `itˤtˤaaliba lgidiida` 'the new
  student (f)', `itˤtˤaaliba nnabiiha` 'the intelligent student' [abdelmassih-v3 p.83, pp.42–43].
- Before a /ʔ/-initial stem: `il-`, e.g. `ilʔarnab` 'the rabbit'.
- A small class takes **`l- ~ lil-`** with the stem's /ʔ/ dropped — Form VIII verbal nouns,
  the `ʔaCCaC` colour adjectives, and `itneen` 'two': `ʔaħmarˤ` → `laħmarˤ ~ illaħmarˤ` 'the red'
  [abdelmassih-v3 p.84]. **This matters directly**: the elative/colour pattern in item 4 below
  is exactly this class.

`CONFLICT (which letters are sun letters):` [wiki-sun-moon-letters §Rule] gives the Classical set
ت ث د ذ ر ز س ش ص ض ط ظ ل ن = "the coronal consonants", explicitly **including ش /ʃ/** and
excluding ج. [abdelmassih-v3 pp.83–84] gives the Cairene set as dentals + /ʃ/, and adds
**optional** assimilation before /k g/, which the Classical statement does not have. The Cairene
list for a rule file: obligatory before /t tˤ d dˤ s sˤ z zˤ r rˤ n/ and /ʃ/ (Abdel-Massih's
enumerated set is exactly "t, ṭ, d, ḍ, s, ṣ, z, ẓ, r, ṛ, and n" plus /ʃ/ — **/l/ is not in it**,
since il- + l- gives a geminate anyway [abdelmassih-v3 p.83]); optional before /k g/;
none before /ʔ b f q x ɣ ħ ʕ h m w j/ (and the loan segments /p v ʒ/ are unclassified —
a design decision; /ʒ/ patterns with /ʃ/ phonetically and could reasonably assimilate).

### 2. Nisba (relative adjective) — the workhorse for place/origin epithets

**Form**: masculine **`-i`**, feminine **`-iyya`**, plural **`-iyyiin`**
[abdelmassih-v3 pp.142–143; broselow1976 p.114]. In names it is normally prefixed by the article
[wiki-nisba §Use in onomastics].

**Attachment rule, verbatim**: "The termination **-V or -(Vy)V is deleted before suffixing /-i/**"
[abdelmassih-v3 p.142]:

| base | nisba | gloss |
|---|---|---|
| `masˤrˤ` 'Egypt' | `ˈmasˤrˤi` | 'Egyptian' |
| `madrasa` 'school' | `madˈrasi` | 'scholastic' — final `-a` deleted |
| `balgiika` 'Belgium' | `balˈgiːki` | 'Belgian' — final `-a` deleted |
| `turkiyya` 'Turkey' | `ˈturki` | 'Turkish' — the whole `-iyya` deleted |
| `mawdˤiʕ` 'place' | `ˈmawdˤiʕi` | 'local' |
| `taˈriːx` 'history' | `taˈriːxi` | 'historical' [broselow1976 p.62] |
| `maˈħall` 'place' | `maˈħalli` | 'local' [broselow1976 p.62] |
| `ħarb` 'war' | `ˈħarbi` | 'military' [broselow1976 p.62] |
| `ziˈraːʕa` 'agriculture' | `ziˈraːʕi` | 'agricultural' [broselow1976 p.62] |
| `siˈjaːsa` 'politics' | `siˈjaːsi` | 'political' [broselow1976 p.62] |
| `ħuˈkuːma` 'government' | `ħuˈkuːmi` | 'governmental' [broselow1976 p.62] |

**A stem that always carries the article loses it under nisba-suffixation**: `ilyabaan` →
`yaˈbaːni` 'Japanese'; `ilʔurdun` → `ʔurˈduni` 'Jordanian' [abdelmassih-v3 p.142].

**Feminine/plural forms cause stem shortening.** `taˈriːx` → `taˈriːxi` → fem. `tariˈxijja`,
pl. `tarixijˈjiːn` — the stem's long /iː/ shortens because it loses stress (§3.8 rule 2)
[broselow1976 pp.114–115]. Broselow derives this from an underlying `-iːy` plus Y-Gemination, but
concludes the safe statement is straight allomorphy: **`-i` / `-iyya` / `-iyyiin`**
[broselow1976 p.115].

Some nisbas take **broken** plurals: `turki` → `atˤrˤaak`; `ingiliːzi` → `ingiliːz`
[abdelmassih-v3 p.142]. Attested Cairene denominal nisbas: `bunni` 'brown' (< bunn 'coffee
powder'), `rˤamaːdi` 'grey' (< rˤamaad 'ashes'), `banafsigi` 'purple', `burtuʔaani` 'orange',
`zibiibi` 'maroon' [wiki-egy-arabic §Color/defect nouns, citing Hinds & Badawi 1986 p.104].

**Syntax note worth having**: "In a sequence of adjectives, a nisba adjective must come first":
`karˤafatta ingiliːzi ħamrˤa` 'a red English tie'. A nisba may stand alone as a noun:
`ilmasˤri` 'the Egyptian (man)' [abdelmassih-v3 p.143].

Unpredictable stems exist and must be listed: `sana` 'year' → `sanawi`; `nabi` 'prophet' →
`nabawi`; `asya` 'Asia' → `asyawi` [abdelmassih-v3 p.142]. The `-awi` type is also the one
Wikipedia flags in names (Badawi) [wiki-nisba §Original use].

### 3. Feminine `-a`, and its construct form `-it` / `-t`

- Feminine singular nouns and adjectives end in **`-a`**: `tˤaalib`/`tˤaaliba` 'student',
  `nabiih`/`nabiiha` 'intelligent' [abdelmassih-v3 p.27].
- **Construct (annexed) form**: `-a` → **`-t`**, or **`-it`** where `-t` would create CCC
  [abdelmassih-v3 pp.255, 324]:
  `madiina` → `madiinit tˤantˤa` 'the city of Tanta'; `maktaba` → `maktabt iggamʕa` 'the
  university library' but `maktabit gamʕitna` 'our university library'; `saaʕa` → `saʕti`
  'my watch', `saʕitna` 'our watch', `saaʕit ʕali` "Ali's watch".
  `CONFLICT (the construct vowel):` Abdel-Massih's allomorph is **-it**; Hafez's, on loans, is
  consistently **-et** — `battˤaarˤejja` → `battˤaarˤejjet ilʕarˤabejja` 'the car battery';
  `fanella` → `fanellet innaadi`; `koberta` → `kobertet isseriːr`; `gaketta` → `gakettet
  ilbadla`; `warʃa` → `warʃet innaggaːrˤ` [ema1958 §30]. This is very likely the same morpheme
  written with different vowel symbols (Hafez's `e` vs Abdel-Massih's `i` for the same short
  high/mid vowel — see the /e/~/i/ CONFLICT in §1), not two allomorphs, but the digest does not
  assume that. Either spelling is defensible; pick one and be consistent.
- **Loans with inanimate referents strongly prefer to end in `-a`**: balakoona 'balcon',
  gaketta 'jacket', giːba 'jupe', ʃootˤa 'shot', battˤaarˤejja 'battery', bomba 'bomb', biira
  'beer', ʔesbetalja 'hospital', fatuurˤa 'fattura', baaSa 'pass', ʃofoniːra 'chiffonier',
  boola 'ball', lamba 'lamp' [ema1958 §44]. Hafez does not say the donor's gender is consulted;
  the generalization she states is simply the `-a` preference.
- Loans with **animate** referents take natural gender, with `-a` for the feminine:
  kowafeer/kowafeera, kaʃjeer/kaʃjeera, doktoor/doktoorˤa, sekerteer/sekerteera [ema1958 §43].

### 4. Elative / comparative — `ʔaCCaC`, and the colour-and-defect adjectives

**`ʔaCCaC` is invariable** as a comparative (no gender, no number) [abdelmassih-v3 pp.25–26]:

| pattern | condition | examples |
|---|---|---|
| **ʔaCCaC** | default | `kibiːr` 'big' → `ˈakbarˤ`; `gamiːl` 'pretty' → `ˈagmal`; `tˤawiːl` 'tall' → `ˈatˤwal` |
| **ʔaCCa** | base ends in `-i` or `-w` | `ʕaali` 'high' → `ˈaʕla`; `ħilw` 'sweet' → `ˈaħla` |
| **ʔaCaCC** | geminate root | `gidiːd` 'new' → `ˈagadd`; `muhimm` 'important' → `ˈahamm` |

'than' = **`min`**. There is **no separate superlative**: it is periphrastic on the same form —
`da atˤwal walad` 'this is the tallest boy', `huwwa min atˤwal ilʔawlaad` 'he is one of the
tallest boys' [abdelmassih-v3 p.26].

The same template also carries the **colour-and-defect** adjectives, which inflect
**ʔaCCaC (m) / CaCCa (f) / CuCC (pl)** [wiki-egy-arabic §Color/defect nouns]:
`ʔaxdˤarˤ / xadˤrˤa / xudˤr` 'green'; `ʔazraʔ / zarʔa / zurʔ` 'blue';
`ʔiswid / sooda / suud` 'black'; `ʔabjadˤ / beedˤa / biːdˤ` 'white'; `ʔaħmarˤ` 'red';
`ʔasˤfarˤ` 'yellow'; `ʔasmarˤ` 'brown-skinned'; `ʔaʃʔarˤ` 'blond';
`ʔatˤrˤaʃ / tˤarˤʃa / tˤurˤʃ` 'deaf'; `ʔaʕma / ʕamja / ʕumj` 'blind';
`ʔaʕwarˤ / ʕoorˤa / ʕuːrˤ` 'one-eyed'; `ʔasˤlaʕ` 'bald'; `ʔaxrˤas` 'mute'.
**For an epithet generator this is the single most productive slot** — it is exactly the "the
One-Eyed", "the Red", "the Swift" shape, and it takes the `l- ~ lil-` article variant (item 1).

### 5. Productive adjective measures

Three that Abdel-Massih names as taking the **sound** plural, i.e. transparently derived
[abdelmassih-v3 pp.28–29]:

| template | example | plural |
|---|---|---|
| **CuCayyaC** | `ʔusˤajjarˤ` 'short', `kuwajjis` 'good' | `-iin` |
| **CaCCaaC** | `nasˤsˤaab` 'a swindler' | `nasˤsˤabiin` (stem shortens) |
| **CaCCaan** | `kaslaan` 'lazy' | `kaslaniin` (stem shortens) |

Plus **CaCiiC**, the commonest simple adjective shape, though he does not name it as a measure:
`kibiːr` 'big', `gamiːl` 'pretty', `tˤawiːl` 'tall', `nabiːh` 'intelligent', `gidiːd` 'new',
`maskiːn` 'poor' [abdelmassih-v3 pp.25–29]; also `naʃiːtˤ` 'active', `nidˤiːf` 'clean',
`tixiːn` 'fat', `faʔiːr` 'poor', `xabiːr` 'expert' [wiki-egy-arabic §Plurals].
And the participles: **CaaCiC** active (`naajim` 'sleeping', `kaatib` 'writing/writer') and
**maCCuuC** passive (`maʕruuf` 'known', `maktuub` 'written') [abdelmassih-v3 p.28].

### 6. Sound plurals

- **`-iin`** masculine, on: (i) active/passive participles in their basic sense; (ii) **nisba
  adjectives** (→ `-iyyiin`); (iii) the CuCayyaC / CaCCaaC / CaCCaan measures
  [abdelmassih-v3 pp.28–29, p.211].
- **`-aat`** feminine; the stem-final `-a` is deleted first: `fallaaħa` → `fallaħaat`
  [abdelmassih-v3 p.317].
- Otherwise **broken**, and "unpredictable … must be learned for each noun separately"
  [abdelmassih-v3 pp.210–211]. Wikipedia gives a large table of patterns
  [wiki-egy-arabic §Plurals]; the epithet-relevant ones are CaCC/CiCC/CuCC → **ʔaCCaaC**
  (film/ʔaflaam, joom/ʔajjaam) and CaCiiC → **CuCaCa** (faʔiːr/fuʔarˤa) for adjectives.
- **Agreement**: human plurals take plural adjectives (`awlaad kubaarˤ`); **non-human** plurals
  take either a plural adjective or a **feminine singular** one
  (`kutub kubaarˤ` ~ `kutub kibiːra`) [abdelmassih-v3 p.211].

### 7. Loanwords get a full derivational paradigm — if a 3/4-consonant root can be abstracted

Hafez's procedure [ema1958 §40–41]: (i) abstract a 3- or 4-consonant root; (ii) run the ordinary
EA derivational patterns (perfective, imperfective, active/passive participle, verbal noun) on
the model of `katab, jekteb, kaateb, maktuub, ketaaba`.
- 'hydrogen' /hajedroʒiin/ → root **h-d-r-ʒ** → `hadraʒ` (perf.), `jehadraʒ` (imperf.),
  `hadraʒa` (verbal noun), `mehadraʒ` (pass. part.)
- 'nervous' → root **n-r-f-z** → transitive `narfez`, `jenarfez`, `menarfez`, `narfaza`;
  intransitive `ʔetnarfez`, `jetnarfez`, `metnarfez`
- ad-hoc denominals from brand names: `nebebsi` (< Pepsi), `barseli` / `tebarseli` (< Persil)
- **Limit**: more than four consonants and the root cannot be abstracted — `talleXraaf`
  'telegraph' yields the periphrasis `jebʕat talleXraaf` 'send a telegram', not *`jetalXraf`
  [ema1958 §41, §55].
Verbal-noun measures found: CVVC (v.n. CVVCa), CaCCaC (v.n. CaCCaCa), CaCCeC (v.n. CaCCaCa),
CaCCaC (v.n. taCCiiC) [ema1958 §39–40]; the tables themselves are images in the online text and
could not be read (see digest-log.md).

### 8. Diminutive — `not covered`

No source consulted gives a productive Cairene diminutive. Abdel-Massih's *Reference Grammar*
has no diminutive entry, his lexicon has no diminutive-marked entries, and the only trace is the
abbreviation `dim = diminutive` in the *Introduction*'s abbreviation list [abdelmassih-intro
p.329]. **`CuCayyaC` is formally the Arabic diminutive template**, and he gives `ʔusˤajjarˤ`
'short' and `kuwajjis` 'good' under it — but he presents it purely as an adjective measure and
never calls it a diminutive [abdelmassih-v3 pp.28–29]. Hafez likewise: `not covered`
[ema1958]. Do not treat CuCayyaC as a productive diminutive on these sources' authority; it is
available as an *adjective* template.

### 9. Gender assignment on loans

Animate: natural gender, feminine in `-a`. **Inanimate: default to feminine `-a`**
[ema1958 §43–44] — see item 3. Some loans take no feminine at all: `garˤsoon` 'garçon',
`tajbest` 'typist', `mekaniːki` 'mechanic' [ema1958 §43].

### 10. Vowel-final loans resist suffixation

Abdel-Massih's explicit note: vowel-final loans such as `kiːlu`, `radju`, `banju`, `antinna`
"seldom take pronominal suffixes"; possession is expressed periphrastically with **`bitaaʕ`**
instead [abdelmassih-v3 p.18]. Hafez reports the same avoidance for plurals of some loans:
`bankenoot` has no plural (`waraʔ bankenoot`), `kombjuutar` uses `ʔaghezet ilkombjuutar`
[ema1958 §52].
**Relevant because**: Irish names ending in a vowel (Ciara /ˈkɪəɾˠə/) will land in exactly this
class, and the safe treatment is to leave them uninflected and use `bitaaʕ` or a construct
phrase.

---

## 7. Attested adaptations

See **`attested.tsv`** in this directory (format: `../ATTESTED-FORMAT.md`).

**Count: 314 rows** (plus a header).

Provenance mix:
- **231 rows from `ema1958` (Hafez 1996)** — a loanword-integration article, whose examples are
  given in running text with the author's own transcription. This is the bulk of the file.
- **20 rows from `kwpl-ot-cairene-loan` (Galal 2004)** — his two numbered data sets, re-read
  from the PDF page images because the `.txt` extraction garbles several forms.
- **10 rows from `broselow-position-quality` (2015)**, +1 from `broselow-arabic-syll` — Broselow's Cairene English-loan list,
  which independently corroborates Galal's forms and adds the sonority split.
- **28 rows from the Abdel-Massih volumes** (14 from `-v4`, 10 from `-intro`, 4 from `-v3`) — established loans as they appear in a
  dictionary and a teaching grammar, every one confirmed against the PDF page images.
- **13 rows from Wikipedia** (`wiki-egy-phonology`, `wiki-egy-arabic`, `wiki-help-ipa-egy`),
  several of which Wikipedia itself sources to Hinds & Badawi 1986 or Watson 2002.
- **11 rows from `ijllnet-cairene-english-syll` (Khalifa 2018)**, which are **not observed data
  at all**: they come from a starred table headed "Error", introduced with "it is expected that
  the Cairene learners will … tend to…" — i.e. they are the author's *predictions* of L2 errors,
  not recorded productions and not lexicalized loans. They are kept because they are the only
  material bearing on cluster shapes the lexical corpus lacks (three-member codas, syllabic
  sonorants), but they carry the least evidential weight in the file and should be filtered out
  of any count. §3.4's three-member-coda evidence rests on them and is correspondingly weak.

**Biases to be aware of:**
1. **Donor mix is European.** 169 English, 98 French, 37 Italian, 5 Turkish, 3 Spanish, 1 Latin, 1 Japanese. There is no Celtic, no Germanic beyond English, and nothing with a palatalization
   contrast. §8's palatalization question therefore has no data behind it and cannot get any
   from this file.
2. **`source_ipa` is blank in EVERY row.** None of the sources states the donor pronunciation —
   not Hafez, Galal, Broselow, Abdel-Massih *or* Khalifa, all of whom give the donor word in
   ordinary orthography only. An earlier draft of this file carried IPA in the eleven Khalifa
   rows; those were supplied rather than read and have been removed.
3. **The `ema1958` rows do not show emphatics.** The OpenEdition online text has the emphatic
   diacritics stripped (the journal states this); every row from that source carries
   `emphatics unmarked in source` in the note column. **Absence of an emphatic in one of those
   rows is not evidence of a plain consonant.** The `target_ipa` in those rows is a mechanical
   conversion of Hafez's transcription and inherits the same gap. (Her `â` symbol is read as
   /ɑ/; that identification is an inference from its distribution, not something the readable
   text states.)
4. **Abdel-Massih's lexicon states no etymologies**, so every donor language in those 28 rows is
   this digest's inference and is marked as such in the note column.
5. **Register.** Hafez shows that the degree of integration is socially conditioned (§1), and her
   corpus deliberately includes both integrated and resistant forms. The file therefore contains
   doublets (`vella ~ fella`, `garaaǧ ~ garaaš`, `prââvu ~ berââvu`). Both members are real; a
   generator must pick a register.

---

## 8. Irish-specific mismatch notes

### 8.1 Broad (velarized) vs. slender (palatalized) — the big decision

**Is there any Cairene precedent for mapping a foreign palatalized or velarized consonant?**

**Palatalized: no. Flatly `not covered`.** Every source was checked
[ema1958, kwpl-ot-cairene-loan, ijllnet-cairene-english-syll, ojml-cairene-syllable, broselow1976,
broselow-position-quality, broselow-arabic-syll, hassig2011-cairene, wiki-egy-phonology]. None
discusses a donor palatalized consonant. Cairene has no Cʲ series and the loan corpora are from
English, French, Italian and Turkish, none of which supplies one. There is no target-internal
precedent to appeal to. Options, undecided:
1. **Depalatalize** — Cʲ → C. Costs the entire Irish contrast; every name loses half its identity.
2. **Cʲ → Cj** — insert /j/. Cairene /j/ is a full consonant, so this creates a CC cluster, which
   is illicit in the onset and would immediately be repaired by epenthesis (§3.1) — turning
   /kʲ/ into *kiy-* or *ki-*. This has the side effect of *lengthening* every word, which may
   read as excessive.
3. **Cʲ colours the following vowel** — e.g. Cʲa → Ce/Ci. This has no direct Cairene precedent
   either, **but it is the exact mirror image of a process Cairene really has**: emphasis colours
   /a/ to [ɑ] (§8.2). Using front-vowel colouring for slender and back-vowel colouring for broad
   makes the two Irish series map onto a single Cairene alternation the language already runs. Of
   the three this is the one with the most support by analogy, though the analogy is the digest
   author's, not a source's.

**Velarized: yes, and this is the digest's strongest finding for §8.**
There are **two** independent kinds of precedent.

**(a) Cairene productively ASSIGNS emphasis to loan consonants that were not emphatic in the
donor.** This is Hafez's "overdifferentiation":
> "the emphatic sounds /t d s z q ġ/, being unique to Arabic, are often produced in loanwords
> replacing other available sounds … when followed by a back vowel, alveolars are velarized and
> change to their emphatic counterparts."  [ema1958 §19–20]

Stated as a rule: `[alveolar] → [emphatic] / _ [back V]`, i.e.
`t → tˤ`, `d → dˤ`, `s → sˤ`, `z → zˤ`, and additionally `k → q`.
Attested [ema1958 §20, §5]:
- t → tˤ: tânt 'tante', bâttârejjâ 'battery', bont 'point', tâblejjâ 'table', etâljâ 'Italia',
  bântâloon 'pantalon', šuut 'shoot', qobtâân 'capitaine'
- d → dˤ: moodâ 'moda' — here stated as `d → dˤ / [back V] _`, i.e. *preceded* by a back vowel
- s → sˤ: sâloon 'salon', sââlâ 'salle'
- z → zˤ: vââzâ 'vase'
- k → q: qomisjoon 'commission', qobtâân 'capitaine', musiiqâ 'musica'
**Independently corroborated by Abdel-Massih's lexicon**, which prints established loans with
emphatics the donor did not have — `lukanḍa` /luˈkandˤa/ 'hotel' < Ital. *locanda*
[abdelmassih-v4 p.147]; `ṣaloon` /sˤaˈloːn/ < Fr. *salon* [abdelmassih-v4 p.150];
`tiṛamwaay` /tiˈrˤamwaːj/ < Eng. *tramway* [abdelmassih-v4 p.150]. In each the emphatic sits
next to a back vowel, exactly as Hafez's rule predicts. (An earlier draft listed `braavo` as a
fourth case; it is **not** one — Abdel-Massih prints it plain, with no emphatic
[abdelmassih-intro p.26].)

This is a genuine, documented, productive route by which a foreign word acquires the emphatic
series. **It is conditioned by an adjacent back vowel, not by anything in the donor consonant** —
which is the awkward part for an Irish mapping: Cairene assigns emphasis from the *vowel*, whereas
Irish supplies it from the *consonant*. Using it for Irish broad consonants means running the rule
backwards.

**(b) European loans are the documented home of the *marginal* emphatics.** Watson's evidence for
positing /rˤ bˤ mˤ/ at all is partly loanwords: [bɑɾɑˈʃot] 'parachute' for /rˤ/; /bˤaːbˤa/
[ˈbɑːbɑ] 'patriarch' vs /baːba/ [ˈbæːbæ] 'Paopi' for /bˤ/
[wiki-egy-phonology §Consonants note 4, citing Watson 2002 p.22]. And the whole class of
"autonomous [ɑ ɑː]" is said to be mostly "in words of non-Semitic origin — especially those
derived from European languages" [wiki-egy-phonology §Emphasis spreading].
One of the four analyses Wikipedia lists for those words is precisely **"created new emphatic
consonants (e.g. analyzing [ˈmɑjjɑ] as /mˤajja/, where underlying /mˤ/ surfaces as [m] but triggers
the back allophone [ɑ])"** — which is exactly the machinery an Irish-broad → Cairene-emphatic
mapping would need for labials and nasals, where no emphatic counterpart otherwise exists.

**What the mapping would look like, and where it breaks.**

| Irish broad C | Cairene emphatic available? | source |
|---|---|---|
| /t̪ˠ/ | **tˤ** yes | core emphatic [broselow1976 p.xiii] |
| /d̪ˠ/ | **dˤ** yes | core emphatic |
| /sˠ/ | **sˤ** yes | core emphatic |
| /l̪ˠ/ | **lˤ** yes | underlying emphatic for Broselow [broselow1976 p.xiii]; "marginal" for Watson [wiki-egy-phonology §Consonants note 4] |
| /ɾˠ/ (broad r) | **rˤ** yes | underlying for Broselow; marginal for Watson; attested in a European loan (parachute) |
| /mˠ/ | **mˤ** marginal only | mayya; transcribers disagree [broselow1976 p.57 n.8]; Watson posits it [wiki-egy-phonology note 4] |
| /bˠ/ | **bˤ** marginal only | bˤaːbˤa 'patriarch' [wiki-egy-phonology note 4] |
| /pˠ/ | — | /p/ is itself loan-only; no /pˤ/ |
| /fˠ/ | — | Broselow explicitly does **not** report emphatic /f/ as a class [broselow1976]. `not covered` |
| /kˠ/ /gˠ/ /ŋˠ/ /xˠ~x/ /ɣˠ~ɣ/ /w/ | — | velars/uvulars have no emphatic counterparts; and note /x ɣ/ do **not** even trigger emphasis spread in Cairene [wiki-egy-phonology §Emphasis spreading] |
| /nˠ/ | — | no /nˤ/ reported anywhere |

So roughly half the Irish broad series has an emphatic home (/t d s l r/, and marginally /m b/)
and half does not (/p f k g ŋ x ɣ w n/). **The decision the tool's author has to make is what to
do with the other half**, and the sources do not settle it. The two coherent positions are:
- **Segmental**: map broad → emphatic where an emphatic exists, and let the rest fall through to
  plain. Simple, but produces an inconsistent contrast.
- **Suprasegmental**: treat "broad" as a feature that colours the *syllable*, using Cairene's own
  emphasis-spread machinery (below) and the /mˤ/-style device of positing an emphatic consonant
  that surfaces plain but backs its vowels. This yields the contrast everywhere at the cost of one
  documented-but-marginal analytical move.

### 8.2 Emphasis spread — what a rule file needs

Broselow 1976 §1.8 is the only detailed statement available openly, and it is precise. Three
rules, in this order, after syllabification [broselow1976 pp.54–55]:

**Underlying emphatic set: /tˤ dˤ sˤ zˤ rˤ lˤ/**, plus /q/ which is *always* emphatic.
> "there is evidence that only the segments /tˤ, dˤ, sˤ, zˤ, rˤ, and lˤ/ are underlyingly
> emphatic" [broselow1976 p.xiii]; "All segments except /q/ occur both emphatic and non-emphatic"
> [broselow1976 p.32].
**Pharyngeals /ħ ʕ/ do NOT trigger spread** — they only slightly lower a following vowel; the rule
carries a `[−lo]` specification on the trigger to exclude them [broselow1976 p.41]. **Uvulars/
velars /x ɣ/ do not trigger it either** in prestige Cairene [wiki-egy-phonology §Emphasis
spreading].

1. **Emp-Sp (Emphasis Spreading) — domain: the SYLLABLE.**
   Within one syllable, everything adjacent to a `[+CP, −lo]` segment becomes emphatic. Since a
   Cairene syllable is at most CVːC, **the whole syllable goes emphatic**
   [broselow1976 p.41 (138)]. "The minimum domain of emphasis is the sequence CV"
   [broselow1976 p.32]. **Ignores word boundaries** — and since Cairene syllables span words,
   emphasis crosses words whenever a syllable does.
   The alternations that prove the syllable domain [broselow1976 p.34]:
   | form | syllabified | /l/ or /n/ or /f/ emphatic? |
   |---|---|---|
   | sˤaaliħ 'good (m)' | sˤaa/liħ | **no** — /l/ is in the second syllable |
   | sˤalˤħiin 'good (p)' | sˤal/ħiin | **yes** — /l/ now shares the syllable with /sˤ/ |
   | ħarraan 'hot (m)' | | **yes** — /n/ shares with /rˤ/ |
   | ħarraana 'hot (f)' | ħar/raa/na | **no** — /n/ resyllabified into its own syllable |
   | latˤiif 'pleasant (m)' | | **yes** |
   | latˤiifa 'pleasant (f)' | la/tˤii/fa | **no** |
   And across words: `ʔudit sitt` 'a woman's room' has an emphatic final /t/, but `ʔudit issitt`
   'the woman's room' does not, because /t/ has become the onset of the next syllable
   [broselow1976 p.35].

2. **RES (Right Emphasis Spread) — rightward, doubly conditioned** [broselow1976 p.45 (149)]:
   > If an emphatic syllable **ends in a consonant**, the **entire following syllable** becomes
   > emphatic **provided its vowel is LOW** (/a/ or /aː/).

   Both conditions bite. The vowel condition [broselow1976 pp.43–44]:
   | form | gloss | suffix emphatic? |
   |---|---|---|
   | sˤaħb-i | 'my friend' | no (/i/) |
   | sˤɑħb-ɑk | 'your (m) friend' | **yes** (/a/) |
   | sˤaħb-ik | 'your (f) friend' | no (/i/) |
   | sˤaħb-u | 'his friend' | no (/u/) |
   Also min ˈfɑdˤlɑk 'please (to m)' vs min fadˤlik 'please (to f)' [broselow1976 p.44].
   The closed-source-syllable condition is why ħarraana and latˤiifa do **not** have emphatic
   final syllables despite their low vowels: the preceding syllables `raa`, `tˤii` are open
   [broselow1976 p.45].

3. **LES (Left Emphasis Spread) — leftward to the WORD edge, unconditioned**
   [broselow1976 p.46 (152)]:
   > Everything from the left word boundary up to an emphatic syllable becomes emphatic — no
   > vowel-quality condition, no requirement that the target be closed. Unlike Emp-Sp and RES,
   > **LES is sensitive to the word boundary**.

   ʔudˤit 'room', ʕɑrˤɑbi 'Arabic', ʔistɑχrɑg 'he extracted' all go emphatic throughout
   [broselow1976 p.46]. Inflectional prefixes are variable: bɑʕrˤɑf 'I know', but `biti8raf`
   'you know' is "sometimes marked emphatic, sometimes not" [broselow1976 p.46].
   Broselow reports one counterexample where LES crosses a word boundary
   (*laylatan tˤayyiba* 'good night', Egyptian radio Arabic) and concludes "I suspect that the
   spread of emphasis by RES or LES across word boundaries is a function of the speed and
   formality of the utterance" [broselow1976 pp.46–47].

**Abdel-Massih states the syllable domain independently**, which matters because it is the one
part of Broselow's account that a second source confirms:
> "The occurrence of an emphatic consonant will cause a plain consonant in the same syllable
> (sometimes in the preceding and/or the following syllable) to become emphatic. The domain of
> the spread of emphasis is the syllable, which means that **a syllable has all or none of its
> sounds emphatic**. This also means that in Egyptian Arabic all of the consonants occur as both
> emphatic and plain." [abdelmassih-intro p.6]
with worked examples marked for syllable boundaries: /rˤabatˤu/ 'he tied him' → [rˤɑ.bˤɑ.tˤu];
/muħadˤrˤaːtˤ/ 'lectures' → [mu.ħɑdˤ.rˤɑːtˤ]; /tˤaab/ 'to ripen' → [tˤɑːbˤ], where the emphatic
/tˤ/ makes /b/ emphatic and backs the vowel [abdelmassih-intro p.14].
His "(sometimes in the preceding and/or the following syllable)" is Broselow's LES and RES in
compressed form.

**Phonetic effect on vowels**: /aː/ is [æ]~[ɛ] plain, [ɑ]~[ɔ] emphatic —
> "compare the pronunciation of *baat* 'he spent the night,' in which the vowel is approximately
> [ɛ] or [æ], with that of *baaṭ* 'armpit,' in which the vowel is closer to [a] or [ɔ]."
> [broselow1976 p.xiii]
Emphasis is audible on high vowels too (latˤiif has an emphatic [iiˤ]), but Broselow warns "it's
quite difficult to detect the presence of emphatic articulation in any vowel but /a/"
[broselow1976 pp.42, 44]. Wikipedia's centralization table gives the phonetic detail: near
emphatics iː→ɨː, uː→ʉː, eː→ɘː, oː→ɵː and the short counterparts
[wiki-egy-phonology §Vowels].

`CONFLICT: broselow1976 pp.41–46 (three rules: syllable domain, plus conditioned RES and
word-bounded LES) vs. wiki-egy-phonology §Emphasis spreading ("the back variants [ɑ ɑː] spread
both forward and backward throughout the phonological word … [with] some free variation", and no
blockers at all).` The Wikipedia section is tagged `{{Unreferenced}}` and is a coarser statement;
Broselow's conditions (especially "rightward only into a LOW vowel, and only out of a closed
syllable") are the implementable version and are backed by minimal pairs. Use Broselow; the
Wikipedia version is what you get if you drop the conditions.

**Warning, worth stating plainly:** Cairene emphasis spread is *aggressive*. LES takes it to the
left word edge unconditionally. So if the tool maps Irish broad consonants to emphatics, a single
broad consonant anywhere in a name will back the vowels of everything to its left, and often to
its right as well. On an Irish name with mixed broad and slender consonants — which is most of
them — the result will be a word that is emphatic almost throughout, and the broad/slender
contrast will be *lost again* to over-application. **Any implementation of the broad→emphatic idea
needs a deliberate decision about whether to also implement spread, and the honest answer may be
to implement Emp-Sp (syllable domain) and skip RES/LES.** That is a deviation from the real
grammar, and the digest flags it rather than deciding it.

### 8.3 Irish segments with no Cairene equivalent

| Irish | Cairene | verdict |
|---|---|---|
| /ɣ/ | **/ɣ/** exists | direct. (The project's own notes said /ɣ/ "has no home in Welsh or Arabic (→ /ʁ/)" — for Cairene that is **wrong**: /ɣ/ is a native phoneme [wiki-egy-phonology §Consonants], written غ. Whether it is realized velar [ɣ] or uvular [ʁ] is the Cairene/Ṣaʿīdi transcription question of §0, not a gap.) |
| /x/ | **/x/** exists | direct, written خ |
| /h/ | **/h/** exists | direct |
| voiceless sonorants (from lenition/devoicing) | no phonemes, but **one allophonic precedent** | `not covered` as a loan mapping. But Cairene does have voiceless [r̥ l̥]: utterance-finally, /r/ and /l/ devoice after a voiceless obstruent — `ʔatˤr̥` 'train', `ratˤl̥` 'pound', `ʔifl̥` 'a lock', `ʔasˤr̥` 'palace', `naʃr̥` 'publication' [abdelmassih-intro p.27; abdelmassih-v3 p.42]. That is the only target-internal precedent, and it is positionally restricted (final, after a voiceless obstruent) — it will not cover an Irish voiceless sonorant in onset position. Options: map to the voiced counterpart; map to C+/h/; use the allophone where the position happens to match. Undecided. |
| /ɾ/ vs /r/ | Cairene /r/ ~ [ɾ] is in **free variation** [wiki-help-ipa-egy note 2] | the contrast cannot be carried. **But /r/ vs /rˤ/ is a real Cairene contrast** ([ˈbɑʔɑɾi] vs [ˈbæʔæɾi]) and could carry the *broad/slender* r contrast instead |
| /l̪ˠ lʲ/ | /l/ and /lˤ/ | /lˤ/ is underlying for Broselow, marginal for Watson. This pair maps cleanly if broad→emphatic is adopted |
| /n̪ˠ nʲ/ | /n/ only | **no /nˤ/ in any source.** A real gap |
| /w/ (from lenited b/m) | /w/ exists | direct |
| /v/ | /v/ marginal, else /f/ or /b/ | [ema1958 §15] |
| /f/ | /f/ exists | direct |
| /p/ | /p/ marginal, else /b/ | [ema1958 §14; kwpl-ot-cairene-loan p.6–7] |
| /ŋ/ | not a phoneme; allophone of /n m/ before velars | but loan data simply **retains** it: ʔispiriŋ 'spring' [broselow-position-quality p.295], weng 'wing' [ema1958]. Recommend: retain, or write `ng` |
| /c ɟ/ (if the Irish transcription uses them for slender k/g) | /k g/ | plain, plus whatever slender treatment §8.1 settles on |

### 8.4 Irish vowel length and diphthongs

- **Length**: contrastive in Cairene, but see §4 — it survives only under stress and outside a
  closed-by-CC syllable. And **the donor's length is not what determines it**: Cairene assigns
  stress by its own rule and then lengthens the stressed vowel [ema1958 §26]. So an Irish long
  vowel in an unstressed position will shorten, and an Irish *short* vowel in the Cairene-stressed
  position may come out **long**. This is a large, systematic effect and is the loanword
  literature's clearest single statement.
- **Irish /iə uə/**: Cairene has no centring diphthongs. `not covered`. Nearest analogues are
  /eː oː/ (which are historically monophthongized /aj aw/) — mapping /iə/ → /eː/ and /uə/ → /oː/
  is unattested but phonetically defensible **(unattested)**. Alternatively /iːa/ → [iːja] by
  Cairene's own hiatus rule [hassig2011-cairene p.65 n.9], which would give *-iya-*.
- **Irish /əi əu/**: Cairene has /aj aw/ as V+glide sequences [wiki-help-ipa-egy §Diphthongs],
  and loan data shows donor diphthongs landing there: /ʔofsâjed/ 'offside', /ʔezberâjt/ 'Sprite',
  /silajd/ 'slide' [ema1958 §29; broselow-position-quality p.295]. Mapping /əi/ → /aj/ and /əu/ → /aw/ is the obvious move and is **(unattested)** for Irish
  specifically — the cited loan data only shows *donor* diphthongs landing on /aj aw/, and no
  source bears on Irish /əi əu/.
- **Irish /ə/** (unstressed): `not covered` explicitly. The two relevant Cairene statements are
  (a) a preference for **/a/** in unstressed syllables [ema1958 §24], and (b) vowel harmony,
  where an unstressed vowel copies a neighbour: aluminium → ʔalamonjom, chiffonier → šofoniira
  [ema1958 §25]. Either is defensible; harmony is more distinctive.

### 8.5 Irish initial clusters — which §3 rule each falls under

Every Irish initial cluster is illicit (Cairene onsets are strictly one consonant, §2). The split
is by sonority [broselow-position-quality p.295; kwpl-ot-cairene-loan p.2–3; ema1958 §29]:

| Irish onset cluster | rule | output shape |
|---|---|---|
| /sp st sk/ | **§3.1(b) prothesis** | ʔis-CC…  (e.g. /sk/ → ʔisk-) |
| /sl sr/ | **§3.1(a) anaptyxis** — /s/+liquid patterns with rising sonority (silayd, siwetar) | si-C… |
| /sm sn/ | **undecided** — Broselow's own hedge is "(and possibly some or all S-resonant clusters)" [broselow-position-quality p.295]; no source has an /sm/ or /sn/ example. See §9.4 | si-C… or ʔis-C… |
| /bl br gl gr dr tr kr kl fl fr pl pr/ | **§3.1(a) anaptyxis** | bi-l…, ki-r…, fi-l… |
| /kn gn mn/ | **§3.1(a) anaptyxis** presumably — but note these are *falling*-sonority in the stop+nasal cases, which is the profile that took prothesis for /s/+stop. `not covered`: no source has a stop+nasal onset. **Undecided.** |
| /ʃC/ (Irish slender s) | by analogy with /sC/ — `(unattested)` for Cairene, but Hafez's data has /ʃ/ behaving like /s/ before an obstruent (šebs, wenš are codas, not onsets) |
| three-member /spr str skr/ | **both repairs**: ʔis- + anaptyxis, as in *street* → ʔistiriit [broselow-position-quality p.298 n.5] | ʔis-Ci-C… |

**Irish final clusters** mostly need **no repair at all**: Cairene allows any final CC regardless
of sonority [broselow-arabic-syll p.2]. Only a three-member final cluster triggers the CCC rule
(§3.2), and only word-medially or non-utterance-finally does a final CVCC get broken at all
[watson2011-word-stress p.2991].

### 8.6 Initial mutations and genitives on the source side

`not covered` — no Cairene source says anything about how the target treats donor-internal
alternations. Leave for the Irish digest. One observation that may matter: Cairene **reanalyses a
loan-initial syllable that looks like the definite article and deletes it** — Italian *alfino* →
/fiinu/, French *élastique* → /ʔastek/ [ema1958 §32]. An Irish name beginning in *an-* or *il-*
would be exposed to the same reanalysis; whether the tool should imitate that is a design choice.

---

## 9. Open questions

1. **Palatalization has no Cairene precedent at all.** Nothing in nine sources addresses a donor
   palatalized consonant. The three options in §8.1 are the author's to choose between, and the
   digest deliberately does not choose.
2. **Emphasis spread will over-apply.** LES takes emphasis to the left word edge with no
   condition [broselow1976 p.46]. If broad → emphatic is adopted, the contrast will be flattened
   again by spread. Whether to implement spread at all, and if so which of the three rules, is
   undecided (§8.2).
3. **Half the Irish broad series has no emphatic counterpart** (/p f k g ŋ x ɣ w n/). The
   /mˤ/-style "surfaces plain, backs its vowels" device is attested but marginal and disputed
   [broselow1976 p.57 n.8; wiki-egy-phonology §Consonants note 4]. Whether to extend it is
   undecided.
4. **Where exactly the /s/+C prothesis boundary falls.** /sl sw/ take anaptyxis (silajd,
   siwetar) while /sk st sp/ take prothesis [broselow-position-quality p.295]. Where do /sm sn/
   fall? And stop+nasal onsets (/kn gn mn/, which Irish has) are **falling** sonority like
   /s/+stop but are not /s/-initial; no source has an example. `not covered`.
5. **/θ ð/ in a non-Arabic donor**: `t d` (Hafez, from English loans) or `s z` (Wikipedia's
   stated rule for non-Egyptianized loans)? Both are cited in §3.6. Irish has neither segment,
   so this may not matter.
6. **Are short /e o/ phonemes?** Four positions in the sources (§1). It matters only for whether
   the generator may output a short mid vowel that is not the shortening of /eː oː/.
7. **Word-initial CC: absolutely banned, or "very rare"?** Broselow says no ECA word begins with
   a cluster [broselow1976 p.20]; Abdel-Massih says initial CC is "very rare" and gives
   `kwajjis ~ kuwajjis` 'good' and `braavo` 'bravo' [abdelmassih-intro p.26; abdelmassih-v3
   p.42]; Hafez says prestige and hypercorrect speech now tolerate them (`braavu`, `trella`,
   `kravat`) [ema1958 §38, §60]. `CONFLICT`, and it is a live register question, not a
   description error. A generator aiming at a "prestige/educated" register could licence a
   small set of initial clusters; one aiming at the integrated register should not.
8. **Deletion is not a Cairene loan repair** [kwpl-ot-cairene-loan pp.17–18] — but the project's
   optional "creole-style reduction layer" would need one. Nothing in these sources supports it.
9. **The Hafez appendix and six data tables are images** and could not be read offline; the
   transcription key used for the 231 attested rows drawn from it is reconstructed from usage. See digest-log.md.
