# Source digest: Georgian (Standard / literary, Kartluri base)

Strand 4 target — the "harsh/alien" strand. Sources: `bib.md` in this directory.
Citation keys below are bib.md keys; `p.N` is the printed page of the source unless noted.
`(unattested)` marks anything supplied from general knowledge. `CONFLICT:` marks source
disagreement left unresolved.

---

## 0. Variety and scope

Standard (literary) Georgian, whose base is the Kartluri dialect of Kartli, the eastern province
containing Tbilisi [shosted2006 p.255]. This matches the PHOIBLE row exactly (InvID 2183,
"Standard (or literary) georgian (Kartluri dialect)").

The digest rests on:
- **§2 phonotactics** — `butskhrikidze2002` (Leiden PhD, *The Consonant Phonotactics of Georgian*),
  above all its **Appendix 2** (stem-initial sequences, pp. 197–205) and **Appendix 3** (stem-final
  sequences, pp. 207–209); cross-checked against `wiki-ka §Phonotactics`, `mccoy1999`,
  `crouch2022-diss`, `crouch2023-intrusive-vocoids`.
- **§1 inventory** — `shosted2006` (the JIPA Illustration), `begus2021`, `wiki-ka §Phonology`.
- **§3/§7 loanword repair** — `gabunia2021` (MA thesis on anglicism pronunciation, the only
  source here with IPA on both sides), plus the `ka-wiki-title` transliteration harvest.
- **§4 stress** — `borise2023` vs `jun2007`.
- **§5 romanization** — `ungegn-georgian` (the national 2002 system, authoritative),
  `wiki-ka-romanization`, `wiki-help-ipa-ka`, `peacecorps`.
- **§6 morphology** — `wiki-ka-grammar`, `wiki-ka-name`, `self-syncope`.

**Two scope warnings for anyone re-reading the sources.**

1. `butskhrikidze2002.txt` (the pdftotext extraction) is **badly corrupted for every non-ASCII
   glyph** — the PDF embeds a phonetic font that pdftotext decodes against the wrong mapping, and
   the mapping is *not* stable from run to run of text (`X` is `χ` in one line and `u` in the
   next). Every cluster list in §2 below was re-read from rendered PDF pages, not from the .txt.
   PDF page = thesis page + 14.
2. Butskhrikidze's own transcription is **not IPA**: plain `p t k c č` are the voiceless
   *aspirated* series (aspiration is not written), `'` marks ejectives, `x` is her velar
   fricative and `χ'` her uvular ejective [butskhrikidze2002 p.76–77, p.85]. Lists below are
   given in her notation with an IPA gloss where it matters.

**Nothing in the sources contradicts the PHOIBLE row's segment list.** The disagreements are all
about *transcription* of the back fricatives (§1.2) and about /v/'s status (§1.6).

---

## 1. Inventory deltas

28 consonants + 5 vowels, and Georgian orthography is one letter per phoneme
[shosted2006 p.255]. The PHOIBLE row's 33 segments are exactly this set.

### 1.1 The consonant chart [shosted2006 p.255]

| | Bilabial | Labiodental | Dental | Alveolar | Post-alv. | Velar | Uvular | Glottal |
|---|---|---|---|---|---|---|---|---|
| Plosive | pʰ pʼ b | | tʰ tʼ d | | | kʰ kʼ ɡ | qʼ | |
| Affricate | | | | ts tsʼ dz | tʃ tʃʼ dʒ | | | |
| Nasal | m | | | n | | | | |
| Tap/trill | | | | ɾ ~ r | | | | |
| Fricative | | v | | s z | ʃ ʒ | x ɣ | | h |
| Lateral | | | | l | | | | |

Three-way laryngeal series throughout the stops and affricates: voiced / voiceless aspirated /
ejective [shosted2006 p.255; butskhrikidze2002 p.85]. Aerodynamically the ejectives show a small
symmetrical oral-flow spike with flow returning to 0 ml/s (glottal closure through release), the
aspirates ~900 ml/s, the voiced ~375 ml/s [shosted2006 p.259–260]. Žgent'i (1956) found foreign
listeners mis-hear Georgian voiced stops as voiceless or glottalized because of their low degree
of voicing; Shosted & Chikovani conclude **aspiration, not voicing, is the primary perceptual cue**
[shosted2006 p.260].

PHOIBLE's dental diacritics (`t̪ʰ t̪ʼ d̪`) and its `t̠ʃ`/`d̠ʒ` retraction marks are notational; the
sources write plain `tʰ tʼ d tʃ dʒ`.

### 1.2 The back fricatives — velar or uvular?

`CONFLICT:` PHOIBLE 2183 gives **/x ɣ/ (velar)**. `wiki-ka-romanization`'s table gives
ხ = **/χ/** and ღ = **/ʁ/ (uvular)**. `shosted2006` reports the debate directly: velar per Vogt
(1971) and Shanidze (1973); uvular per Žgent'i (1956), Fähnrich (1987), Aronson (1997), Hewitt
(2005); and Butskhrikidze herself uses uvular `[χ]` on p.77 and velar `[x]` on p.87 for the same
sound [shosted2006 p.258]. Shosted & Chikovani ran a jitter test on `/ikʰi/` vs `/ixi/` nonsense
syllables (N=100) and found no significant difference in creak on flanking vowels, concluding
**"/x/ is likely velar for the present speaker"**, and use `[x]` in their chart [shosted2006
p.259]. They note there is **no phonemic velar/uvular fricative contrast in Georgian at all**, so
the question is phonetic, not phonological [shosted2006 p.258].

*Practical consequence for the tool: none phonologically — pick one symbol and keep it. Recommend
/x ɣ/ with PHOIBLE and shosted2006, and let the romanization write it `x` (§5), which reads
uvular-ish to an English eye anyway.*

### 1.3 /qʼ/ — the only uvular

Georgian has exactly one uvular phoneme, so ejectivity cannot be contrastive there
[shosted2006 p.257]. Its realizations **[qʼ], [qʼχ], [χʼ], [ʔ]** occur in apparent free variation —
the same speaker produced /qʼɔpʼɑ/ 'being' as [qʼχ] on one recording and [ʔ] on another
[shosted2006 p.256–258]. Aerodynamically it is neither a clean stop (no oral-flow peak) nor a
clean fricative (low flow); the unifying cue is **laryngealization of the neighbouring vowels**
[shosted2006 p.257–258]. PHOIBLE's allophone list `[qʼ χʼ qʼχ ʔ]` is exactly this and is correct.

There is **no plain /q/ or /qʰ/** in modern Standard Georgian: Proto-Kartvelian *q merged with the
velar fricative, giving homonyms like [xɛrxi] 'skill' and 'saw' < *qerxi, *xerxi; the *q/*x
opposition survives only in mountain dialects such as Khevsuruli [shosted2006 p.256].

*This matters for strand 4: the /qʼ/ ↔ [ʔ] alternation is documented, native, and is precisely the
"apostrophe = ejective **or** glottal break" behaviour the existing names show.*

### 1.4 /f/ — absent

Not in the chart [shosted2006 p.255]. **[f] and [ɸ] are allophones of /v/ before voiceless
consonants**, e.g. /vtʃʼɑm/ → [ftʃʼɑm] 'I eat', /vprtskʰvni/ → [ɸprtskʰvni] 'I peel'; labiodental
vs bilabial realization is unpredictable, and /v/ is sometimes simply deleted there
[shosted2006 p.261; wiki-help-ipa-ka n.7]. The letter ჶ *fi* exists but is outside the modern
33-letter alphabet, a loan letter [wiki-ka-scripts; gabunia2021 — see §3].

### 1.5 /h/ — a full phoneme, but not stem-final

In the chart as a glottal fricative [shosted2006 p.255], with the minimal-set item /hɑvɑ/
'climate'. Butskhrikidze restricts it distributionally: **a Georgian stem may end in any of the 27
consonants "except /h/"** [butskhrikidze2002 p.98].

### 1.6 /v/

Canonically a **voiced labiodental fricative** [vɑrdi] 'rose', [hɑvɑ] 'climate' [shosted2006
p.261]. Devoices to [f]~[ɸ] before voiceless consonants (§1.4), optionally drops word-initially
before /u/: /vutsʼɛr/ → [utsʼɛr] 'I write for someone' [shosted2006 p.261].

`CONFLICT:` Butskhrikidze analyses post-obstruent /v/ as **secondary rounding on the preceding
obstruent**, /qʼvɑvili/ → [qʼʷɑvili] 'flower' [butskhrikidze2002 p.88, p.93]. Shosted & Chikovani
accept this after *voiceless* obstruents (where the off-glide devoices and the two analyses are
acoustically indistinguishable) but reject it after voiced stops: /ɡvɛrdi/ 'side' keeps voicing,
labiodental contact and audible frication, and their Georgian-speaking co-author "strongly
disapproves" of *[ɡʷɛrdi] [shosted2006 p.261]. Wikipedia's IPA key states flatly "/v/ is realized
as [ʷ] after a consonant" [wiki-help-ipa-ka n.2].

*Practical: treat /v/ as a consonant that fills the C2/C3 sonorant slot of clusters (Appendix 2
and 3 are full of `-v` finals: `tkv`, `cxv`, `gv-`, `-šv`). Do not model the rounding allophone.*

### 1.7 Rhotic, lateral, sonorants

The sonorants are **/l r n m v/** [shosted2006 p.261]. The rhotic is a **tap**, not a trill, for
the Tbilisi speaker: mean intervocalic closure ~20 ms, no sustained trilling; occasional two-strike
trills appear intervocalically in free variation [shosted2006 p.261]. /l/ has velarized [ɫ] before
back vowels /ɑ ɔ u/ and plain [l] before /i ɛ/ [wiki-help-ipa-ka n.4] — *not* corroborated in
shosted2006 (not covered there).

There is a regular **/l/ ~ /r/ dissimilation** in the nominalizing suffix: `-uri` normally, but
`-uli` when the base contains a rhotic — /tʰbilisuri/ 'of Tbilisi' vs /kʰɑrtʰuli/ 'of Georgia'
[shosted2006 p.261, citing Hewitt 2005:282]. See §6.

**Syllabic sonorants are real**: in a language permitting clusters this long, sonorants are often
syllabic [butskhrikidze2002 p.88, endorsed by shosted2006 p.261]. PHOIBLE's `[l̩ m̩ n̩ ɾ̩ r̩ v̩]`
allophones are these.

### 1.8 Vowels

Five: /i ɛ ɑ ɔ u/ [shosted2006 p.261–262]. Transcription varies by author — Canepari
[i e̞ ä o̞ u], Aronson [i̞ e̞ ä o̞ u̞], Shosted [i ɛ ɑ ɔ u] [wiki-ka §Vowels]. PHOIBLE follows
Shosted. Shosted & Chikovani's auditory impression is that /i u/ are tense and only /ɛ ɔ/ lax
[shosted2006 p.262].

- **Length and nasalization are not features of the Georgian vowel system** [shosted2006 p.262].
- **Adjacent vowels are disallowed in monomorphemic words, ruling out diphthongs**; where two
  vowels do meet, as in [ɡirɑɔ] 'mortgage', they are **heterosyllabic** [shosted2006 p.262, citing
  butskhrikidze2002 p.83].
- Across a morpheme or word boundary, /aa ii ee oo uu/ may surface as a single long vowel:
  /kʼibɛɛbi/ → [ˈkʼibɛːbi] 'stairs' [wiki-ka §Vowels]. This is the only long vowel Georgian has.
- **[ə] may be inserted to break up consonant clusters**: /dɡɑs/ → [dəɡäs] [wiki-ka §Vowels].
  See §2.9 (intrusive vocoids) — this is allophonic, not repair.
- In casual speech /i/ next to a vowel → [i̯]~[j]; /u o/ before a vowel → [w] [wiki-ka §Vowels].

### 1.9 Net delta from the PHOIBLE row

None in segment membership. Adjustments only:
- /x ɣ/ may be uvular [χ ʁ] — see §1.2 CONFLICT.
- /ɾ/ is the right symbol (tap), and PHOIBLE's `[ɾ r]` free variation is correct [shosted2006 p.261].
- /h/ should be flagged **not stem-final** [butskhrikidze2002 p.98]; PHOIBLE has no such field.
- No segment is loan-only; the only loan segment is **[f]**, which never becomes phonemic in the
  nativized layer (§3).

---
## 2. Syllable structure and phonotactics

**Transcription warning for this whole section.** All cluster lists are given in
Butskhrikidze's notation (see §0): plain `p t k c č` = aspirated /pʰ tʰ kʰ tsʰ tʃʰ/; `'` = ejective;
`c` = /ts/, `č` = /tʃ/, `ʒ` = /dz/, `ǰ` = /dʒ/, `x` = /x/, `γ` = /ɣ/, `χ'` = /qʼ/ (her symbol for
the uvular ejective, elsewhere written `q'`), `š ž` = /ʃ ʒ/. **The `.txt` extraction of the thesis
mangles all of these**; the lists below were re-read from rendered PDF pages.

### 2.1 There is no syllable template — the domain is the STEM

Butskhrikidze's central claim is that the syllable is *not* the domain of Georgian phonotactic
generalizations: "the syllable does not comply with [the domain requirement] and consequently
cannot serve as the domain of phonotactic generalisations" [butskhrikidze2002 p.41]. What she
gives instead is a **word template — the minimal word is disyllabic, C1V1C2V2**
[butskhrikidze2002 p.100, p.120] — and stem-edge inventories (§2.4, §2.5).

Crouch works with syllables and gives a size bound rather than a template: "The minimal Georgian
syllable is a single V, such as either of the syllables in /i.a/ 'violet', but onsets can contain
up to seven consonants, as in /ɡvptsxvnis/ 'they (sg) peeled us'"; "Virtually any sequence of
consonants is permitted in the onset"; complex codas "are almost universally the result of
morphological affixation … word-medial consonant sequences are syllabified as a simplex coda
followed by a complex onset, so there are no word-medial complex codas at all"
[crouch2022-diss §1.3.1 p.13, p.76].

Attested shapes (assembled from examples; no source presents this as a template):

| Shape | Example | Source |
|---|---|---|
| V | /i.a/ 'violet' | [crouch2022-diss p.13] |
| CV | *xe* 'tree', *da* 'sister', *bu* 'owl' | [butskhrikidze2002 p.96, p.82] |
| CCV | *rk'o* 'acorn', *mze* 'sun' | [butskhrikidze2002 p.96, p.76] |
| CCCV | *brge* 'tall' | [butskhrikidze2002 p.96] |
| CCCCCCV | *brdγvna* 'to fight', *prckvna* 'to peel' | [butskhrikidze2002 p.108] |
| **CVC** | **does not exist as a lexical word** | [butskhrikidze2002 p.96] |

`CONFLICT: maximum onset length.` Butskhrikidze: **six** word-initially (*brdγvna*, *prckvna*)
[butskhrikidze2002 p.106–108]; Self follows her, "from two to six" [self-syncope p.2]; Crouch:
**seven**, /ɡvptsxvnis/ [crouch2022-diss p.13, p.39; crouch2023-intrusive-vocoids p.2000].
Partly reconcilable — Butskhrikidze excludes the verbal prefixes /ɡv-/ and /m-/ from her count as
morphological [butskhrikidze2002 p.105–106], and `gv-` in *gvptsxvnis* is exactly such a prefix.
`wiki-ka §Phonotactics` goes further still, listing seven-consonant *gvts'vrtni* 'you train us' and
**eight**-consonant *gvprtskvni* 'you peel us', *gvbrdghvni* 'you tear us'
[wiki-ka §Phonotactics].

`CONFLICT: are there restrictions at all?` Crouch: "there are minimal restrictions on the
combinations", the only one she names being a ban on three adjacent sonorants
[crouch2022-diss §1.3.1, p.76]. Butskhrikidze documents dozens (§2.6). Partly a difference of
counting: Crouch counts multimorphemic onsets that Butskhrikidze excludes by design.

### 2.2 Harmonic clusters — the inventory

A **harmonic cluster** is a two-consonant sequence meeting two criteria simultaneously
[butskhrikidze2002 p.102–103; butskhrikidze-vanheuven-avt18 p.27; mccoy1999 p.448]:
1. **Regressive** — anterior then posterior: `[−dorsal][+dorsal]`, i.e. a labial or coronal
   followed by a dorsal.
2. **Homogeneous** — both members share a laryngeal setting: both voiced, both aspirated, or both
   ejective.

The full inventory, table (53) [butskhrikidze2002 p.103], repeated identically at p.133 and in
[butskhrikidze-vanheuven-avt18 p.27]. **32 clusters**, in her notation:

| C1 | Type A: + velar **stop** /ɡ kʰ kʼ/ | | | Type B: + dorsal **fricative** /ɣ x qʼ/ | | |
|---|---|---|---|---|---|---|
| | voiced | aspirated | ejective | voiced | aspirated | ejective |
| labial | **bg** | **pk** | **p'k'** | **bγ** | **px** | **p'χ'** |
| dental | **dg** | **tk** | **t'k'** | **dγ** | **tx** | **t'χ'** |
| alv. affricate | **ʒg** | **ck** | **c'k'** | **ʒγ** | **cx** | **c'χ'** |
| p-alv. affricate | **ǰg** | **čk** | **č'k'** | **ǰγ** | **čx** | **č'χ'** |
| alv. fricative | *zg* | **sk** | — | **zγ** | **sx** | — |
| p-alv. fricative | *žg* | **šk** | — | **žγ** | **šx** | — |

In IPA the 24 non-fricative-initial ones are: bɡ dɡ dzɡ dʒɡ / pʰkʰ tʰkʰ tsʰkʰ tʃʰkʰ /
pʼkʼ tʼkʼ tsʼkʼ tʃʼkʼ / bɣ dɣ dzɣ dʒɣ / pʰx tʰx tsʰx tʃʰx / pʼqʼ tʼqʼ tsʼqʼ tʃʼqʼ.

`wiki-ka §Harmonic clusters` gives the same set minus the fricative-initial rows (**12 clusters**),
attributing it to Chitoran 1998, with examples: /bɡeɾa/ ბგერა 'sound', /pʰkʰʷili/ ფქვილი,
/pʼkʼuɾeba/ პკურება, /dɡoma/ დგომა, /tʰkʰeʃi/ თქეში, /tʼkʼbili/ ტკბილი, /dzɡide/ ძგიდე,
/tsʰkʰeɾa/ ცქერა, /tsʼkʼmutʼuni/ წკმუტუნი, /dʒɡupʰi/ ჯგუფი, /tʃʰkʰaɾa/ ჩქარა,
/tʃʼkʼʷiani/ ჭკვიანი, /bɣudʒa/ ბღუჯა, /pʰxizeli/ ფხიზელი, /pʼχʼrobi/ პყრობი, /dɣʷena/ დღვენა,
/tʰxili/ თხილი, /tʼχʼuili/ ტყუილი.

`CONFLICT: how many harmonic clusters?` McCoy lists **24** — the 12 stop-final + 12
fricative-final, all with stop/affricate C1 [mccoy1999 p.448]. This is not a real disagreement:
she excludes fricative-initial ones **by design** ("Although fricatives form harmonic clusters as
well as the stop series, their lack of total closure makes them even less likely candidates for
'zero release'; they will not be considered here" [mccoy1999 p.447]).

`CONFLICT: zg and žg.` Butskhrikidze lists them in (53) and in the AVT paper, but footnotes
"I. Melikishvili has pointed out to me that harmonic clusters such as **zg** and **žg** are almost
unattested. They were probably included in the set in order to maintain the symmetry with the Type
B set" [butskhrikidze2002 p.103 n.20] — and her own co-occurrence table marks `zg` **impossible**
[butskhrikidze2002 p.110]. *Treat `zg`/`žg` as gaps.*

`CONFLICT: single release.` The traditional grammars claim harmonic clusters have a single
release. McCoy's acoustic study (6 speakers, Tbilisi, 29 words × 3) finds "**all tokens** of
harmonic consonant clusters showed a release after each element in the cluster. There were no
cases of a single release" [mccoy1999 p.448], and Chitoran 1998 found bursts realised in >90% of
cases regardless of cluster type [butskhrikidze-vanheuven-avt18 p.29]. Butskhrikidze's weaker
version: C1 bursts "were always present but had shorter durations and/or weaker intensities"
[butskhrikidze-vanheuven-avt18 p.29]. Their perception experiment (24 native listeners, 192
non-words) found harmonic clusters behave like single consonants in hit rate (80% vs 78% for a
single C, 86% for an unrelated CC) but like a two-consonant sequence in detection time
(892 ms vs 844 / 894 ms) — "they have separate, **intermediate**, status"
[butskhrikidze-vanheuven-avt18 p.32–35]. `wiki-ka §Harmonic clusters` states the opposite of the
tradition: "Harmonic clusters are pronounced with individual releases of each segment".

*Practical: transcribe them as two segments. The interest of harmonic clusters for this project is
distributional, not phonetic — see §2.5 (they are the **only** obstruent sequence allowed
stem-finally).*

### 2.3 Stem-initial consonant sequences — the attested list

From **Appendix 2** [butskhrikidze2002 pp.197–205], compiled from Žgent'i (1956) with some
examples changed and some very common sequences added. **The list is explicitly "not exhaustive"**,
**excludes /m/+C sequences entirely**, and includes only two /v/+C cases
[butskhrikidze2002 p.197]. No totals are given.

**Two-member (CC), by manner class:**

- **stop+stop** — bg *bgera* 'sound'; dg *dguši* 'sucker'; gd *gdeba* 'lie about'; k'b *k'bili*
  'tooth'; p'k' *p'k'ureba* 'spray'; tb *tbili* 'warm'; tk *tkeši* 'downpour'; t'k' *t'k'acani* 'crack'
- **stop+affricate** — brǰ *brǰeni* 'rest'; bč' *bč'oba* 'discussion'; brj *brjaneba* 'order';
  kc *kceva* 'behaviour'; t'χ' *t'χ'avi* 'skin'
- **stop+fricative** — bz *bza* 'box-tree'; bž *bžit'i* 'duckling'; bγ *bγavili* 'bleating';
  dγ *dγe* 'day'; gz *gza* 'road'; ks *kseli* 'cob-web'; kš *kšena* 'to puff'; pš *pšat'i* (plant);
  px *pxa* 'skill'; tx *txa* 'goat'
- **stop+sonorant** — bl bm bn br; dv dm dn dr; gv gl gm gn gr; kv kl km kn kr; k'v k'l k'm k'n k'r;
  pl pr; p'l p'r; tv tl tm tr; t'v t'l t'r
  (*blu* 'tongue-tied', *bma*, *bneva*, *brazi*, *dvire*, *dmanisi*, *dnoba*, *dro* 'time',
  *gvalva*, *glova*, *gmiri* 'hero', *gnomi*, *gradusi*, *kva* 'stone', *kliavi* 'plum', *kmediti*,
  *knari* 'lyre', *kris*, *k'veba*, *k'lanč'i*, *k'maχ'opili*, *k'nut'i* 'kitten', *k'reba*,
  *ploba*, *prinveli* 'bird', *p'lombi*, *p'riali*, *tvali* 'eye', *tla*, *tma* 'hair', *treva*,
  *t'vini* 'brain', *t'lanki*, *t'rabaxi*)
- **affricate+stop** — cd ck čk c'k' č'd ǰd ǰg
- **affricate+fricative** — cx čx c'χ' č'χ' jγ ǰγ
- **affricate+sonorant** — cv cm cn cr; čv čl čr; c'v c'l c'm c'n c'r; č'v č'l č'm č'r;
  jv jl jm jn jr; ǰv ǰm
- **fricative+stop** — sk *skesi*; sk' *sk'a* 'hive'; st' *st'umari* 'guest'; šp *špoti*;
  št *štantkma*; št' *št'o* 'branch'; xd *xdoma*; χ'b *χ'ba* 'jaw'; χ'd *χ'da*
- **fricative+affricate** — sc' *sc'avla* 'study'; xc *xceneba*
- **fricative+fricative** — sx *sxivi* 'beam'; šx *šxap'una*; zγ *zγap'ari* 'tale'; žγ *žγera*;
  xš *xširi* 'frequent'
- **fricative+sonorant** — sv sl sm sr; šv šl šm šn šr; zv zl zm zn zr; žr žl; γv γl γm γr;
  xv xl xm xn xr; χ'v χ'l χ'm χ'n χ'r
  (*svavi*, *slok'ini*, *smena*, *srola*, *švili* 'child', *šlami*, *šmori*, *šno*, *šriali*,
  *zvavi*, *zlazvna*, *zmuili*, *zne*, *zrunva*, *žriamuli*, *žlet'a*, *γvino* 'wine', *γlet'a*,
  *γmeč'a*, *γreoba*, *xvadi*, *xleba*, *xma* 'voice', *xnieri*, *xrinc'i*, *χ'vavili* 'flower',
  *χ'lort'i*, *χ'muili*, *χ'nosva*, *χ'ra*)
- **sonorant+stop** — lb lt'; nd; rb rg rk rk' rt'
- **sonorant+affricate** — rc' rj rǰ
- **sonorant+fricative** — vs *vseba* 'to fill'; lx *lxena*; rχ' *rχ'eva*
- **sonorant+sonorant** — lm *lmobieri* 'soft-hearted'

**Three-member (CCC)** — 26 manner-classes, examples:
t'k'b *t'k'bili* 'sweet'; tkv *tkveni* 'your'; tkr; p'c'k'; psk' *psk'eri* 'bottom'; bγv; txl; txr;
t'χ'v; t'χ'l; brb *brbo* 'crowd'; brg; brk; grd *grdemli* 'anvil'; krt; k'vd; k'ld *k'lde* 'rock';
k'rt; prt *prta* 'wing'; trt; zrd *zrda* 'growth'; grj; k'rj; brm *brma* 'blind'; gvr; k'vn; k'vr;
tvl; ckv; c'k'l; c'k'm; c'k'r; č'k'n; cxv *cxviri* 'nose'; cxr *cxra* 'nine'; čxr; c'χ'v; c'χ'l;
c'χ'r; c'χ'n; č'χ'l; jγv; c'rt; c'rp; jrc'; črd *črdili* 'shade'; c'vr; č'vr; jvr; st'v *st'vena*
'whistle'; sc'r; sxv *sxva* 'other'; zγv *zγva* 'sea'; xsn *xsnari* 'solution'; xrt'; χ'rd; γrj;
žrž; švr; zmn *zmna* 'verb'; γrm *γrma* 'deep'; xvr; rgv; rtv; nǰr; rcx; rc'χ'; rγv; vrc

**Four-member (CCCC)**:
tkvl *tkvlepa*; txzv *txzva* 'compose'; pxvn *pxvnili* 'powder'; pšvn; brt'χ' *brt'χ'eli* 'flat';
prtx *prtxili* 'careful'; grgv *grgvinva* 'thunder'; prkv; brc'χ'; brč'χ' *brč'χ'ali* 'claw';
prčx *prčxili* 'nail'; grǰn *grǰnoba* 'feeling'; c'χ'vd; čxvl; c'rtv; sxvl *sxvla*; xrc'n *xrc'na*
'decay'; γrγn *γrγna*; rt'χ'm *rt'χ'ma* 'to hit'; nǰγr *nǰγreva* 'to shake'; rcxv *rcxvena* 'shame';
rχ'vn *rχ'vna* 'corrupt'

**Five-member (CCCCC)**: c'vrtn *c'vrtna* 'training'
**Six-member (CCCCCC)**: prckvn *prckvn(a)* 'to peel'; brdγvn *brdγvna* 'to fight'

### 2.4 Gvinadze's six-slot template — the compact statement of what may combine

The single most implementable generalization in the thesis [butskhrikidze2002 p.108]:

```
I    /b p p' m/
II   /r/
III  /d t t' ʒ c c' ǰ č č' z s ž š/
IV   /g k k' γ x χ'/
V    /v/
VI   /r l m n/
```

> "One consonant from each set can combine **in the strict order given** and form maximally a
> six-member cluster, e.g. /brdγvna/ 'to fight', /prckvna/ 'to peel'. **Any set can be skipped,
> but the order between the sets should be respected.** Consonants in the sequence must have the
> same laryngeal specification and must be regressive." [butskhrikidze2002 p.108]

Slot III+IV together "usually form harmonic clusters"; slot V /v/ is secondary articulation on the
preceding (usually dorsal) consonant; slot II /r/ is optional when flanked by consonants of
identical laryngeal specification and obligatory (and syllabic) when they differ
[butskhrikidze2002 p.108–109].

*This template plus the laryngeal-agreement requirement is the whole cluster grammar in four
lines. Recommend implementing exactly this as the licitness test, with Appendix 2/3 as the
attested-forms whitelist.*

### 2.5 Stem-final consonant sequences

From **Appendix 3** [butskhrikidze2002 pp.207–209], the two-member data from Uturgaidze (1976);
also explicitly "not exhaustive". Crucially:

> "the stem can end in any of the 27 consonants (i.e. except /h/) and maximally form a five-member
> sequence" [butskhrikidze2002 p.99]

and

> "**Harmonic clusters are the only obstruent sequence permitted stem-finally**"
> [butskhrikidze2002 p.104] — *ortkl-i* 'steam', *marc'χ'v-i* 'strawberry', *čončx-i* 'skeleton',
> *otx-i* 'four', *vepxv-i* 'tiger'.

**Two-member, stem-final:**
- harmonic: bγ dγ zγ žγ px sx šx c'χ' č'χ'
- obstruent+sonorant: zv zr zl pr tr sl šl žr šn zn xl xr γl γr
- **sonorant+obstruent — very common, but "most of them are loan words"**
  [butskhrikidze2002 p.207]: nd *gund-i* 'choir' (Pers.); nǰ *brinǰ-i* 'rice' (Pers.);
  ng *niangi* 'crocodile'; nk' *mank'-i* 'defect'; nč *kanč-i* (Turk.); rg *barg-i* 'luggage';
  rd *vard-i* 'rose'; rǰ *xarǰ-i* 'expense' (Arab.); rč *čarč-i* (Turk.); rk' *xark'-i* 'tribute';
  rp' *k'erp'-i* 'idol'; rj *k'erj-i*; rp *šarp-i* 'scarf' (Fr.); rb *xarb-i* 'greedy';
  lk *olk-i* 'district' (Turk.); lx **xalx-i* 'people'* (Arab.); vz *k'ovz-i* 'spoon';
  vt *navt-i* 'kerosene'
- obstruent sequences **found only in loans**: st' št' zd xt' šk' xš γd
- attested stem-**initially but not** stem-finally: t'b k'b xb tb gd xd gǰ ("non-deccessive
  clusters … found only in a few words … most of these clusters are secondary")
- attested in **neither** position: zb xp χ'p' žb rp rž lž lš lǰ

**Three-member, stem-final** — three types: (i) harmonic+sonorant (pxv *vepxv-i* 'tiger';
cxl *cecxl-i* 'fire'; cxv *ricxv-i* 'number'; t'χ'l *mat'χ'l-i* 'wool'; sxl *sisxl-i* 'blood');
(ii) sonorant+harmonic (nčx *čončx-i*; rcx *marcx-i*; rt'χ' *bart'χ'-i*; všv *bavšv-i* 'child');
(iii) sonorant+obstruent+sonorant (rpl, rp'l, rbl *zγurbl-i* 'threshold', rxv, rγv, rcv, rt'l,
rǰl, lkv, nc'l).

**Four-member**: rtkl *ortkl-i* 'steam'; rcxl *vercxl-i* 'silver'; rcxv *morcxv-i* 'shy';
rc'χ'v *marc'χ'v-i* 'strawberry'; nčxl *ančxl-i* 'irritable' — pattern: /r/ + harmonic cluster + /v/
[butskhrikidze2002 p.209].
**Five-member**: nǰgvl *banǰgvl-i* 'shaggy' — the only one given.

### 2.6 Co-occurrence restrictions

**Place-class OCP** [butskhrikidze2002 p.101–102]. Four classes; **no member of a class combines
with another member of the same class** (obstruents only — obstruent+sonorant of the same place is
fine: *dn*, *dr*, *t'l*):
- C1 labials /b p p' m v/ — *\*mb \*bp \*pv…*
- C2 coronals /d t t' ʒ c c' z s ǰ č č' ž š/
- C3 sonorants /r l n/
- C4 dorsals+laryngeal /g k k' γ x χ' h/

> "**Obstruents with identical place of articulation never combine**" [butskhrikidze2002 p.102]

**Coronal ordering** [butskhrikidze2002 p.102]:
> "A posterior coronal may precede an anterior coronal, but never follow it."
`št`, `ǰd`, `cd` attested; `*tš`, `*dǰ`, `*dc` never.

**Affricates** [butskhrikidze2002 p.86]: coronal stop + affricate barred (`*dc`, `*dǰ`), affricate
+ coronal stop fine (`cd`, `ǰd`); **affricates may be preceded by fricatives but never followed by
them** (`sc'`, `šǰ` yes; `*c's`, `*ǰš` no).

**Attested initial CC grid**, table (62) [butskhrikidze2002 p.110] — all 27 consonants except /h/,
excluding /m/+C and /v/+C:

| C1 | attested C2 |
|---|---|
| b | g ǰ č' z ž γ l r n |
| p | t k č s š x l r n |
| p' | k' χ' l r n |
| d | g γ v l r m n |
| t | b k x v l r m |
| t' | b k' χ' v l r |
| g | d z v l r m n |
| k | c s š v l r m n |
| k' | b v l r m n |
| ʒ | g γ v l r m n |
| c | b d t k x v r m n |
| c' | b t k' χ' v l r m n |
| ǰ | d g γ v l m |
| č | k x v l r m |
| č' | d k' χ' v l r m n |
| z | γ v r m n |
| s | p p' t' k k' c' x v l r m |
| ž | γ v l r |
| š | p p' t t' x v l r m n |
| γ | d ʒ ǰ v l r m n |
| x | d s š v l r m n |
| χ' | b d v l r m n |
| l | b p' t' x χ' v m |
| r | b t t' g k k' ʒ c c' ǰ č γ x χ' v |
| n | d t g ǰ |

Her reading [butskhrikidze2002 p.110–112]: the last five columns (`v l r m n`) hold most of the
attested cells — **initial clusters prefer rising sonority**; the `s` and `r` rows are the falling
ones, with /s/+C treated as a complex segment (partly loan-driven: *spero* 'sphere', *sp'ort'i*
'sport') and initial /r/ syllabic and historically derived; the rest are the harmonic clusters.
Summary (66) [butskhrikidze2002 p.112]: the four preferred biconsonantal types are
**(a) obstruent+sonorant, (b) harmonic clusters, (c) /s/+obstruent, (d) /r/+obstruent**.

**Restrictions across a vowel** (CVC stems, Kobalava 1967) [butskhrikidze2002 p.113–115]: of 729
possible C…C combinations only **457 are attested (63%)**. Same-place classes don't co-occur across
a vowel either; affricates and fricatives don't combine; if C1 is a glottalised stop/affricate a
following **voiced** C2 must be further front (so `t'b`, `c'b`, `k'b` occur, `*t'p'`, `*c'g` don't);
no two /r/s or two /v/s within a CVC stem.

### 2.7 Sonority

**All three profiles are attested word-initially** [crouch2022-diss §1.3.1 p.13]:
- **rises**: br *brelo*, bn *bneli* 'darkness', gl *glexi* 'peasant', gr, tm, dm
- **plateaus**: bg *bgera*, mn *mnaxe*, šx *šxama* 'poison', xš, gd, tb, t'χ', pt, k'b *k'bili* 'tooth'
- **falls / reversals**: rb *rbena* 'running', lb, lm, lp', mt *mtaze*, md *mdinare* 'river',
  rg, sp', rč *rčeva* 'advice'

> "the SSP is not relevant for syllabification in Georgian" [crouch2022-diss §1.3.1 p.13]

`wiki-ka §Phonotactics` agrees: Georgian clusters are notable because "many of which fail to
conform to the sonority sequencing principle."

Two sonority-linked regularities that *are* implementable:
- **Fricative + stop sequences are always separated by /r/**, which is then syllabic:
  *zrda* 'to grow', *xrt'ili* 'gristle'; whereas **stop + fricative is never separated by a
  sonorant** (`*brz`, `*pls`, `*glz` unattested) [butskhrikidze2002 p.92; self-syncope p.2].
- Crouch's only named restriction: **no three adjacent sonorants** — *mts'rali* → *mts'rlis* but
  *mtvrali* → *mtvralis*, not `*mtvrlis` [crouch2022-diss p.76, from Chitoran 1999].

### 2.8 Word-edge restrictions

**Word-final** [butskhrikidze2002 p.98, p.105]:
- **No consonant may end a well-formed minimal word; there are no word-final consonant sequences
  at all.** Consonant-final stems obligatorily take the nominative -i.
- Exceptions are adverbs and derived forms: sonorant-final *c'in* 'in front', *xval* 'tomorrow',
  *gušin* 'yesterday'; voiceless-obstruent-final *zevit* 'up', *k'argad* → [k'argat] 'well'.
- **Word-final devoicing** applies where a consonant does end a word (only in grammatical
  affixes): /v-a-k'et-eb/ → [vak'etep] 'I do'; /k'ac-ad/ → [k'ac-at]. Blocked when a further
  suffix follows [butskhrikidze2002 p.85].

**Word-initial** [butskhrikidze2002 p.99]:
- "**All 33 phonemes of Georgian can appear in word-initial position**". Native Georgian words are
  almost always consonant-initial; vowel-initial words are mostly Persian/Latin loans.
- **/h/ is barred everywhere except word-initially, and even there is receding**: OG *hazri* >
  *azri* 'mind', *hambavi* > *ambavi* 'story'. Most surviving h-initial words are Greek loans.
  "**This sound never occurs in consonant sequences**" [butskhrikidze2002 p.87].
- **/v/ may not be the first member of a monomorphemic cluster** — initial *v-* in clusters is the
  1SG prefix; only two lexical exceptions, *vseba* 'to fill', *vrceli* 'wide'
  [butskhrikidze2002 p.105].
- /r/ is the most dispreferred stem-initial sonorant and the most preferred stem-finally; /m/ the
  reverse [butskhrikidze2002 p.116].

### 2.9 Hiatus and glides

- **VV is barred within a monomorphemic word**: "two adjacent vowels are disallowed"
  [butskhrikidze2002 p.83]; hence **no diphthongs** [shosted2006 p.262]. Where two vowels do meet
  they are **heterosyllabic**, [ɡirɑɔ] 'mortgage' [shosted2006 p.262].
- Exceptions are loans and compounds: *musaipi* 'talk' (Arabic), *paipuri* 'porcelain' (Greek),
  *p'aik'i* 'pawn' (Persian), *daira* 'tambourine', *maudi* 'cloth'; *č'aobi* < *č'a-obi* 'swamp'
  [butskhrikidze2002 p.83 n.8]. **This matters: loanwords are exactly where Georgian tolerates
  VV** — and the transliteration harvest (§7) is full of it (*uaildi*, *jeimz*, *brius*).
- Across morpheme boundaries VV is tolerated at prefix#stem but not at stem#suffix
  [butskhrikidze2002 p.83].
- **Repair 1, /v/-epenthesis**: *rʒe* 'milk' → *me-rʒe-v-e* 'milkman'; *t'q'e* 'forest' →
  *me-t'q'e-v-e* 'forester'; *uto* 'iron' → *a-uto-v-eb-s* [butskhrikidze2002 p.83, p.95].
  **Blocked before /o/ or /u/**: *šina* → *sa-šina-o* 'domestic', not `*sa-šina-v-o`.
- **Repair 2, /b/-epenthesis** (rare): *ezo* 'yard' → *m-ezo-b-el-i* 'neighbour'.
- **Repair 3, vowel deletion**: *ʒma* 'brother' → *ʒm-is*; *xe* 'tree' → *x-is*
  [butskhrikidze2002 p.84].
- **Rounded-vowel sequences dissimilate**: *indo-uri* > *indauri* 'turkey'; *sa-uto-o* > *sautao*.
- Identical vowels across a boundary may coalesce to a long vowel: /kʼibɛɛbi/ → [ˈkʼibɛːbi]
  'stairs' [wiki-ka §Vowels].

### 2.10 Gemination — none

> "Geminates are disallowed in monomorphemic contexts… There are no geminates in Georgian."
> [butskhrikidze2002 p.101 n.18]

Identical consonants occur only across morpheme boundaries (/xaz-ze/ 'on the line', /mat-tan/
'with them'); where gemination would arise one consonant deletes (/t'ani-samosi/, not
`*/t'anis-samosi/`). **Loanwords degeminate on entry**: /alegoria/ 'allegory', /k'lasi/ 'class'
[butskhrikidze2002 p.101 n.18]. Corroborated in the harvest: Rotterdam → *rot'erdami*,
Cardiff → *k'ardipi*.

### 2.11 Syllabic sonorants

`CONFLICT:` **Butskhrikidze: yes.** "Georgian sonorants are phonetically syllabic in consonant
sequences… This especially concerns the most sonorous consonant /r/" [butskhrikidze2002 p.88].
Conditioning: **a sonorant is syllabic when flanked by less sonorous consonants**. Evidence:
derived final clusters *naγm-s* [naγm̩s], *saxl-s* [saxl̩s], *tetr-s* [tetr̩s]
[butskhrikidze2002 p.88]; dialect forms that insert *i* exactly there — *rgoli* : Khevsuruli
*girgoli* 'ring'; *γrma* : *γirma* 'deep'; *k'lde* : *k'ilde* 'rock' [butskhrikidze2002 p.89];
Kartvelian cognates PK *trt* : Geo. *trt-ol-a* : Megr. *tirt-ol-i* [butskhrikidze2002 p.89]. She
hedges that this "has to be substantiated by phonetic studies" [butskhrikidze2002 p.93].
**Crouch: flatly no** — "Georgian also does not permit consonants to serve as syllable nuclei"
[crouch2022-diss §1.3.1 p.13]. Self: yes, in passing [self-syncope p.2]. `shosted2006` sides with
Butskhrikidze [shosted2006 p.261], as does the PHOIBLE allophone list.

Sonorant ordering inside long clusters [butskhrikidze2002 p.91]: in `C S1 S2`, **S1 is always /v/**
and S2 ∈ {n, l, r} (*k'vnesa*, *gvrit'i*, *c'vrili*); in `C1 S1 C2 S2`, **/r/ takes S1 and /v/ can
only be S2** (*drt'vinva*, *grgvinva*, *brč'χ'viali*).

/r/ is "fleeting" — **optional** between laryngeally-identical consonants (*prta* ~ *pta* 'wing',
*grdemli* ~ *gdemli* 'anvil', *brʒeni* ~ *bʒeni* 'wise') and **obligatory** when the flanking
consonants differ laryngeally (*brč'χ'ali* 'claw', *k'rʒalva*) [butskhrikidze2002 p.92].

### 2.12 Intrusive vocoids — phonetic, do not write them

Schwa-like elements appear between the consonants of a complex onset "where no phonemic vowel is
present and **are not the result of a phonological process**" [crouch2022-diss p.56]. Distribution
by sonority shape: **rises 56%, plateaus 25%, falls 9%** [crouch2022-diss p.56]. Mean duration
**36.6 ms** vs 118.3 ms for lexical vowels; quality schwa-like (F1≈500, F2≈1500 Hz), significantly
distinct from /a/ and /e/, and **unaffected by the quality of the following vowel**
[crouch2023-intrusive-vocoids p.2002–2003]. Verdict: "intrusive vocoids in Georgian are
**articulatory artifacts** that emerge due to the long lag between consonant constrictions"
[crouch2023-intrusive-vocoids p.2003]. There is **no phonemic schwa in Georgian**
[crouch2022-diss §1.3 p.39].

Corroborated: McCoy found "clearly a schwa" between /d/ and /g/ in /dɡas/ → [dəɡas] in all six
speakers, all 18 tokens [mccoy1999 p.448]; `wiki-ka §Vowels` records the same as an allophonic
rule. Note also that the inter-consonantal lag averages ~100 ms, "nearly equivalent to the
duration of a full vowel" [crouch2023-intrusive-vocoids p.2002].

*Practical: do not romanize them, and do not use them as an epenthesis rule. But they are the
reason Georgian output does not sound as impossible as it looks on paper.*

### 2.13 Syncope — the cluster factory

Georgian's giant clusters are **derived**, not underlying: "(77) All consonant sequences (maximally
biconsonantal) are derived, i.e. the result of vowel deletion" [butskhrikidze2002 p.120]. The rule,
from `self-syncope` (OT machinery discarded per project rules; only the generalization and data
taken):

> **V[−high] → ∅ / [sonorant] _ ]stem + -V(C)**

Preconditions, all four required [self-syncope p.5]:
1. the final vowel of the root is **not [+high]** (i.e. /a e o/ delete; **/i u/ never do**);
2. the suffix is **not the nominative -i**;
3. the root **ends in a sonorant**;
4. the suffix has the shape **-V(C)**, not -CV.

Examples [self-syncope p.3–4; butskhrikidze2002 p.90]:
- *mercxal-i* 'swallow' → GEN *mercxl-is*, INST *mercxl-it*, ABL *mercxl-ad*; but ERG
  *mercxal-ma*, DAT *mercxal-s*, NOM *mercxal-i* — **no syncope** (suffix not -V(C))
- *xar* 'gnaw' → *xr-av-s* / *xvr-a*; *k'al* 'kill' → *k'l-av-s* / *k'vl-a*; *xan* 'plough' →
  *xn-av-s* / *xvn-a* — syncope plus **/v/-metathesis**
- **blocked by [+high]**: *mamul-i* → *mamul-is*, *γimil-i* → *γimil-is*, *nadim-i* → *nadim-is*
- **blocked by obstruent-final root**: *k'amat-i* → *k'amat-is*; *xed* → *xedv-a*, not `*xvd-a`
- **blocked by resulting two adjacent labials**: *ber* → *berv-a*, not `*bvr-a*`
- **blocked by homophony**: *kar-i* 'wind' GEN stays *kar-is*, because *kris* already means 'blows'
- Butskhrikidze adds: syncope also applies before the plural **-eb** (*bal-i* 'cherry' ~
  *bl-eb-i* 'cherries') [butskhrikidze2002 p.90 n.12], and requires the word to be **at least
  disyllabic** [butskhrikidze2002 p.90].
- Historically: *tbili* 'warm' < *gan-t'ep-it*; *cda* 'to try' < *e-cad-e* [self-syncope p.3].

**This is the rule to mimic if strand-4 output should *gain* clusters rather than merely keep the
Irish ones.** An adapted Irish stem ending in a sonorant, plus any -V(C) suffix from §6, produces
a new cluster for free.

---

## 3. Repair strategies (loanword adaptation)

### 3.0 The headline: Georgian barely repairs anything

**Of the four target languages this is the one that will leave Irish input almost untouched.**
Across all four loanword sources, **no instance of cluster repair is reported and none appears in
the data**: no epenthesis into a cluster, no deletion of a cluster member, no prothesis. Clusters
of up to four medial consonants are imported intact — English *record-breaker* → რეკორდსმენი
*rekordsmeni*, keeping `rdsm` [rayfield2023 p.22]. `gabunia2021` never uses the words *cluster*,
*epenthesis* or *syllable* except in the stress passage; the absence is total.

The repairs Georgian **does** perform are:
1. a **morphological** word-edge process — the obligatory nominative **-i** (§3.5);
2. **segment substitution** for the six English consonants Georgian lacks (§3.2);
3. **laryngeal re-assignment** of /p t k/ (§3.1);
4. **degemination** (§3.6);
5. **loss of vowel length** and resolution of diphthongs (§3.4).

### 3.1 The two layers, and the /p t k/ decision

`gabunia2021` is a sociolinguistic study, so every item has a Georgian-like and an English-like
variant. Her own definitions [gabunia2021 p.19]:

> "voiceless plosives are replaced by voiceless ejectives (Shukia Apridonidze introduced this
> approach, and the State Language Department follows it). Fricative /f/ is replaced by voiceless
> aspirated /pʰ/… semivowel /w/ … pronounced with labio-dental voiced fricative /v/. The latter
> was labelled as Geo-like."

Her label set is exactly four: `Geo-like`, `Eng-like`, `Mixed`, `Very Eng-like`. **"Eng-like" is
not English** — she calls it "in fact an **in-between** variant" [gabunia2021 p.19], because every
item still takes the Georgian -i. `Mixed` = /f/ kept but the plosive ejective, which she notes
"can also be argued to be affected by Russian, as Russian … has both fricative /f/ and more
ejective-like /p/, /t/, /k/" [gabunia2021 p.19].

**Take the Geo-like column as the grammar** (the project brief's instruction, and it is also the
State Language Department's official transphonemization norm). Two caveats the digest must record:

- **It is a prescriptive minority in her data**: 59.6% Eng-like vs 36.9% Geo-like across 1320
  tokens of 24 recent loans [gabunia2021 pp.24–25]. She explicitly excludes older,
  Russian-mediated loans as "fully adapted" [gabunia2021 p.26], so the ejective norm may well be
  the majority in the established lexicon and a minority only in the newest borrowings.
- **The choice is positionally conditioned.** Geo-like (ejective) rate by context
  [gabunia2021 p.25, Table 3.2]: word-initial `#CV` 43.7%; medial `CCV` **84.1%**; medial `VCV`
  26.5%; medial `VCC` 43.4%. Her interpretation: "only in Inlaut, if preceded by a consonant
  sound, aspiration is presumably less noticeable" [gabunia2021 p.25]. **After a consonant,
  ejective; between vowels, aspirate.**

> **Rule (nativized): /p t k/ → /pʼ tʼ kʼ/.**
> *snack* → /snɛkʼi/ · *speaker* → /spʼikʼɛri/ · *Twitter* → /tʼvitʼɛri/ · *Instagram* →
> /instʼagrami/ [gabunia2021 pp.50–51]
> **Prestige variant: /p t k/ → /pʰ tʰ kʰ/** — "acoustically, voiceless aspirated sounds
> /pʰ, tʰ, kʰ/ are closer to English /p, t, k/ than voiceless ejectives" [gabunia2021 p.16].

Three refinements:
- **Within-word agreement.** "if an item consisted of two plosives, the participants would always
  use either English-like or Georgian-like plosives in both cases (casting, Twitter, speaker)"
  [gabunia2021 p.26]. Rayfield sees the same in writing: *paste* → და/ჩა-**ფ**ეის**თ**ება ~
  და/ჩა-**პ**ეის**ტ**ება — aspirate-aspirate or ejective-ejective, never mixed
  [rayfield2023 p.22]. **Implement as a word-level harmony, not a per-segment rule.**
- **Plosive + labial blocks the ejective.** In *Queen* "none of the participants used ejective";
  "most other loanwords with the combination of plosive + labial sound … are rendered as Georgian
  voiceless aspirated plosives (quiz, cooler, Queens)" [gabunia2021 p.26]. Both *Queen* variants
  have /kʰ/.
- **Contrast preservation.** Apridonidze's rationale: in *theater* /θ/ → /tʰ/ and /t/ → /tʼ/; in
  *Philips*, /f/ → /pʰ/ and /p/ → /pʼ/ [gabunia2021 p.16]. The ejective assignment partly exists
  to keep two English segments distinct. Rayfield reports the same mechanism lexically: ლაი**ქ**ი
  for 'like' is stable with the aspirate "since the form with an ejective კ, ლაიკი, is reserved
  for the breed of dog" [rayfield2023 pp.20–21].

`CONFLICT: which series is "nativized"?` `gabunia2021`'s Geo-like = ejective, by prescriptive
fiat, but her own measured majority is aspirate outside the post-consonantal context
[gabunia2021 pp.19, 24–25]. Rayfield, describing written usage two years later, finds ejective the
default for *t* and for *k/c* — "in the case of t the ejective is normal (თ being more often used
for th) … otherwise any initial t- becomes ტ-"; "the aspirated plosive is less common than ejective
when transcribing k/c" — but reports ფ (aspirate p) frequently substituted for პ in
ფუბლიქი, ფლაგინი, ფოსტი, ფართი, ფლეი(ბოი), while **not** in პლეერი, and concedes that for კ/ქ he
"has not been able to identify any consistent decisive factor" [rayfield2023 pp.18, 25]. Two of
Gabunia's own Appendix-B rows are internally broken: *Chat* has **two rows both labelled
Geo-like**, and *Like* has the labels **swapped** relative to every other row (the ejective is
tagged Eng-like) [gabunia2021 pp.50–51].
*Recommendation for the tool: use ejective as the default for Irish /p t k/ — it is the norm, it
is 84.1% in post-consonantal position (which is where Irish clusters put most stops), and it is
what makes strand 4 sound like strand 4. Record that the aspirate is equally attestable.*

### 3.2 Absent segment → substitute

Only six English consonants are declared absent from Georgian by `gabunia2021`: **/f/ /θ/ /ð/ /ŋ/
/j/ /w/** [gabunia2021 p.14]. Everything else in the English inventory has a Georgian home.

| Source segment | Nativized | Prestige / variant | Evidence |
|---|---|---|---|
| **/f/** | **/pʰ/** (ფ) | **[f]** retained | "Nowadays, borrowings with /f/ is graphemically realised by ფ - /pʰ/" [gabunia2021 p.15]. *Facebook* → /pʰɛisbukʼi/, *iPhone* → /aipʰɔni/, *duty free* → /dutʼi pʰri/, *fake news* → /pʰɛikʼniusi/ [gabunia2021 pp.50–51]; *certificate* → სერთიფიკატი [gabunia2021 p.12]. Independently: Kirvalidze transcribes the ფ of loans as **[p]** — *forvardi* [pɔrvardɪ], *flirti* [plɪrtɪ], *fantastiuri* [pantastiurɪ] [kirvalidze2017 pp.291–292]. The prestige [f] is available because [f]~[ɸ] is already a positional allophone of /v/ (§1.4) and because of Russian [gabunia2021 pp.15, 36]. **Items with /f/ show more variation than any other segment** [gabunia2021 pp.24–25]. |
| | | | **Exception:** /f/ → **/v/** before a voiced stop: *half-back* → ჰა**ვ**ბეკი [rayfield2023 pp.23–24] (probably via Russian хавбек). |
| **/w/** | **/v/** medially; **/u/** word-initially | /u…/ everywhere | See §3.3 — this is a `CONFLICT:`. |
| **/ŋ/** | **/nɡ/** | — | `CONFLICT:` Gabunia's *prose* says /ŋ/ "does not show variation … and is substituted by /n/" [gabunia2021 p.14], but **her own data give [nɡ]**: *casting* → /kʼastinɡi/, *shopping* → /ʃɔpʼinɡi/ [gabunia2021 pp.50–51]. Rayfield is uniform: ფიშინგი, დრიბლინგი, ბულინგი, ფიტინგი [rayfield2023 pp.21, 23, 24]; the Wikipedia harvest agrees (*inglisi*, *springstʼini*, *vashingtʼoni*, *volpʰgang*). **Take the data: /ŋ/ → /nɡ/.** |
| **/j/** | **/i/** | ჲ (revived) | "graphemically substituted by /i/ - yoghurt – iogurti (იოგურტი)"; "even though it is not graphically present in Georgian, ჲ (or /j/) still exists as an allophone" [gabunia2021 p.14]. `CONFLICT:` Rayfield, two years later: "One positive result … is the revival of a lost letter, ჲ replacing initial y in **ჲოგურტი**, ჲახტა, ჲუნორი" [rayfield2023 p.25] — the *same word*, spelled two ways in the two sources. |
| **/θ/** | /tʰ/, /t/ or /s/ | — | [gabunia2021 p.14]. Apridonidze's *theater* has /θ/ → /tʰ/ [gabunia2021 p.16]. Loan datum: *thriller* → **თ**რილერი, aspirate, via Russian триллер [asaturova-garibashvili p.354]. `CONFLICT:` in the *L2* direction (Georgians speaking English), /θ/ → **/s/** and /ð/ → **/z/** is by far the most-reported error, 91 judge mentions [georgian-accented-speech p.36]. **The two routes differ: direct perception gives /s z/; loanword adaptation, being orthography- and Russian-mediated, gives /tʰ d/.** Do not merge them. |
| **/ð/** | /t/, /d/ or /z/ | — | [gabunia2021 p.14] |
| **/h/** | **/h/** — retained | — | Not discussed by `gabunia2021`, but corroboration is unanimous: *hobi* < hobby, *horori* < horror [asaturova-garibashvili p.353]; *seqondhendi* [kirvalidze2017 p.293]; ჰედლაინი, ჰავბეკი, ჰუქერი, ჰეითერები [rayfield2023 pp.18, 21, 23, 24]. See §8.2 for the positional restriction. |
| /v z s r l dʒ ʒ/ | unchanged | — | All present in the Georgian inventory; `gabunia2021` lists them as non-problems [gabunia2021 p.14]. |

Crucially, "the variation occurs **during adaptation**. The pronunciation of the adapted words …
are more or less stable" [gabunia2021 p.14] — i.e. once a loan is fixed, it stops alternating.

### 3.3 CONFLICT: /w/ — a positional rule miscoded as a prestige rule

`gabunia2021` frames /w/ → /v/ as **nativized** and /w/ → a vowel sequence [ui uɔ uɛ ua] as
**prestige** [gabunia2021 pp.14–15, 19]: *Winston* → /vinstoni/ ~ /uinstoni/, *Windows* →
/vindɔusi/ ~ /uindɔusi/, *Queen* → /kʰvini/ ~ /kʰuini/.

But three things cut across that:
- **Her own *weekend* has /u/ in BOTH variants**: /uikʼɛndi/ ~ /uikʰɛndi/ [gabunia2021 p.51].
- **Her own *forward* → ფორ*უ*არდი** *poruardi* [gabunia2021 pp.7–8].
- **Rayfield states the split positionally**: initial /w/ → **უ** *u* (*უორკშოპები* workshops),
  medial /w/ → **ვ** *v* (*ნეთვორქი* network, *ფორვარდი* forward) [rayfield2023 pp.23, 24].
- Kirvalidze's canonical example of adaptation is *uikendi* < weekend, with **[u]**, and no [v]
  variant is offered [kirvalidze2017 p.291]; `asaturova-garibashvili` list *uikendi* / *uik-endi*
  [asaturova-garibashvili pp.353–354].

The `ka-wiki-title` harvest lines up with the positional reading almost perfectly: **initial /w/ →
u** in *uelsi* (Wales), *uiliam* (William), *uinstʼon* (Winston), *uaildi* (Wilde), *uiliam*
(W. B. Yeats); **but /w/ → v** in *vashingtʼoni* (Washington), *varshava* (Warsaw), *volpʰgang*
(Wolfgang) — the three v-initial ones being exactly the Russian-mediated Germanic/Slavic names,
where the donor spelling is already ⟨W⟩ = /v/.

> **Proposed rule (this digest's reading, not stated by any single source):**
> `/w/ → /u/ / # _` · `/w/ → /v/ / V _ V` and after a consonant.

`georgian-accented-speech` corroborates the /v/ side in the L2 direction: *Hawaii* → /ˈhɑːvaɪɪ/,
*woman* → /ˈvʊmən/, *what* → /vɒt/, with hypercorrection *very* → /ˈwɛrɪ/
[georgian-accented-speech pp.36–37].

*For Irish, /w/ arises from lenited b/m and is usually word-initial after mutation — which the
positional rule sends to /u/, giving a hiatus vowel rather than a consonant. Flag as a decision.*

### 3.4 Vowel adaptation

- **Length is discarded.** "all Georgian vowels are short, therefore vowel length is not
  significant"; "English long and tense vowels are substituted by more-or-less corresponding short
  vowels" [gabunia2021 p.13]. Corroborated: "in Georgian language the length of the vowels are
  approximately the same, and consequently, the vowel length does not have distinctive character"
  [georgian-accented-speech p.40].
- **Vowels are otherwise faithful**: "The use of vowels in borrowed Anglicisms is rather
  **systematic**. Usually, vowels take on a form that is phonologically close to the source sound"
  [gabunia2021 p.13].
- **Diphthongs — two strategies, both attested** [gabunia2021 p.13]:
  1. **monophthongization**: *goal* [ɡəʊl] → *goli* [ɡɔli]; *bacon* [ˈbeɪkən] → *bekoni* [bɛkɔni]
  2. **two separate vowels (hiatus)**: *biker* [ˈbaɪkər] → *baikeri* [baikeri]
  **Strategy 2 dominates in Appendix B**: *lockdown* /lɔkʼdauni/, *like* /laikʼi/, *background*
  /bɛkʼɡraundi/, *Facebook* /pʰɛisbukʼi/, *Windows* /vindɔusi/ [gabunia2021 pp.50–51].
  Strategy 1 dominates in the L2 direction [georgian-accented-speech p.42].
- **/eɪ/ is the one vowel with a Geo/Eng split** — *mail* → /maili/ (Geo-like) vs /mɛili/
  (Eng-like): "some speakers pronounce the words based on the **orthography of the English etymon**,
  while others pronounce acoustically closer sounds" [gabunia2021 p.13]. **The spelling-based
  variant is the one labelled nativized** — a striking and usable fact: Georgian nativization can
  be orthographic rather than acoustic. Corroborated as a general Georgian habit: "Since in
  Georgian, speakers pronounce words as they are written, Georgian English speakers tend to repeat
  the same in the other languages" — *jail* → /dʒaɪl/, *son* → /son/, *club* → /klub/
  [georgian-accented-speech pp.42–43]. Only 4 of 55 participants chose it, though
  [gabunia2021 p.26].
- **/æ/ → /ɛ/** (*snack* /snɛkʼi/, *background* /bɛkʼɡraundi/, *kangaroo* → კენგურუ) or **/ɑ/**
  (*chat* /tʃatʼi/); **/ʌ/ → /ɑ/** (*puzzle* /pʼazli/, *plugin* → ფლაგინი) — (inferred from the
  data; `gabunia2021` does not state these). **/ə/, /ɜː/, /ɪ/: not covered.**

### 3.5 Word-edge: the nominative -i

> "Georgian words always end on vowels. If that is not the case, words (loanwords) **usually take
> suffix -i [i], which is the marker of the nominative case**: Certificate – სერთიფიკატი"
> [gabunia2021 p.12]

Note the framing: it is **morphological, not phonotactic** — a case suffix, not epenthesis. Every
source frames it that way; Kirvalidze calls it "**levelling transmorphemization**, i.e. when most
imported anglicisms take the Georgian suffixal inflexion of the nominative case –i [I], which is
considered to be a universal morphological marker of their adaptation": *blefi* < bluff, *testi* <
test, *starti* < start [kirvalidze2017 p.291].

It is **exceptionless in all 24 experimental items, in every variant including the Very-English-like
ones** — which is why "Eng-like" had to be defined as merely in-between: "there was practically
**no** English-like pronunciation due to the fact that **all** loanwords take Georgian suffix -i"
[gabunia2021 p.19].

Three scope conditions, all from the data (inferred where marked):
- **Vowel-final loans take nothing.** *duty free* → /dutʼi pʰri/, not */pʰrii/
  [gabunia2021 p.51]; *kangaroo* → კენგურუ [rayfield2023 p.25] (inferred — no source states it,
  but see §6.1, where the same rule is stated for native nouns).
- **Only the right edge of the whole item takes it.** *check in* → /tʃɛkʼini/, *weekend* →
  /uikʼɛndi/, *fake news* → /pʰɛikʼniusi/ [gabunia2021 p.51]; *talk show* → **თოქ შოუ**, where
  *talk* ends in a bare consonant and *show* is vowel-final, so **no -i appears at all**
  [rayfield2023 p.25]. Confirmed at scale in the Wikipedia harvest: *jorj vashingtʼoni*,
  *uiliam sheksp'iri*, *maikʼl kʼolinzi* (§7).
- **"Consonant sounds in Auslaut position are very rare in Georgian"** — Gabunia's own reason for
  only distinguishing Anlaut and Inlaut in her coding [gabunia2021 p.22].

**A consequence worth noting: the -i bleeds final devoicing.** `georgian-accented-speech` reports
final devoicing as the most intelligibility-damaging Georgian error in English (*food* → /fuːt/,
*boys* → /bɔɪs/) [georgian-accented-speech pp.38–39, 44] — but in loanwords the -i means no
consonant is ever word-final, so the devoicing rule of §2.8 never gets a chance to apply
(inferred).

### 3.6 Gemination — degemination is exceptionless

No source states a rule, but the data are unanimous [gabunia2021 pp.50–51; rayfield2023 pp.21–24;
kirvalidze2017 p.291]: *Twitter* → /tʼvitʼɛri/, *shopping* → /ʃɔpʼinɡi/, *puzzle* → /pʼazli/,
*bullying* → ბულინგი, *dribbling* → დრიბლინგი, *fitting* → ფიტინგი, *killer* → ქილერი,
*bluff* → ბლეფი, *troll* → ტროლი. This matches the native rule: "**Loanwords degeminate on
entry**: /aleɡoria/ 'allegory', /kʼlasi/ 'class'" [butskhrikidze2002 p.101 n.18].

One live generalization on top of it: **English orthographic doubling biases the plosive toward
the ejective.** *Twitter* and *shopping* favoured the Geo-like variant, and "the possible
explanation … might be the fact that in both of these items the linguistic variables in question
(/p/ and /t/) are **reduplicated**" [gabunia2021 p.26].

### 3.7 Consonant clusters — no repair, and this is the point

**Not covered by any loanword source** — `gabunia2021` never discusses cluster repair. But the
absence is itself the finding, because the data would show it if it happened:

*Instagram* /instʼaɡrami/ (nst, ɡr) · *Beatles* /bitʼlzi/ (tlz) · *chips* /tʃipʼsi/ ·
*background* /bɛkʼɡraundi/ (kɡr, nd) · *puzzle* /pʼazli/ · *speaker* /spʼikʼɛri/ ·
*snack* /snɛkʼi/ [gabunia2021 pp.50–51] · *sport* → სპორტი, *flirt* → ფლირტი
[gabunia2021 pp.7–8] · *headline* → ჰედლაინი (dl, no epenthesis) [rayfield2023 p.18] ·
*exports* → ექსპორტი, *infrastructure* → ინფრასტრუქტურა [asaturova-garibashvili pp.352–354] ·
**record-breaker → რეკორდსმენი, retaining a four-consonant medial `rdsm`** [rayfield2023 p.22].

The one contrary datum is L2 production, not loan adaptation: Georgians speaking English insert a
vowel inside *months* /mʌnθ/ → /mʌnθes/ ~ /mʌnses/ [georgian-accented-speech p.36] — and it
involves /θ/, so it should not be used as evidence that Georgian repairs clusters.

**The only cluster effect Rayfield reports is on lexical survival, not on form**: *retreat* →
რითრითი and *googles* → დაიგუგლება "have a choice and distribution of consonants and vowels which
integrate easily with Georgian", whereas "the alien-sounding აბეკაპებს ('backs up'), with its
**unGeorgian syllabic structure**, still has to compete with the periphrastic … სარეზერვოდ
ადუბლირებს" [rayfield2023 p.17]. Georgian does not fix an awkward loan; it declines to adopt it.

### 3.8 Russian mediation — tag it, do not model it

"numerous Anglicisms entered Georgian vocabulary through the mediatory language (Russian) and was
mainly based on **written** sources… a fair number of Anglicisms in Georgian are more
'**mediatory-language-like**', rather than source-like: **television – televisia; revolution –
revolutsia; jury – jiuri; Budget – biujeti; Partner – partniori**" — words in which "the 'English
markers' … are completely lost" [gabunia2021 p.11, citing Lomidze 2008]. Kirvalidze gives the same
three examples independently [kirvalidze2017 p.291]; `asaturova-garibashvili` supply 39
Georgian–Russian–English triples, of which the diagnostically Russian ones include *prodiuseri*
← продюсер, *pleieri* ← плейер, *distributori* ← дистрибьютор, *transaqcia* / *privatizacia* ←
-ация [asaturova-garibashvili pp.351–354].

**One datum here is worth more than the rest of the section for §8.1.** Gabunia excluded *costume*
from the study because "English [ˈkɒs.tjuːm] is either rendered as Georgian /kɔstʼumi/ or partially
Russian-like version **/kɔsʲtʲˈʉmi/**" [gabunia2021 p.18]. That parenthetical is the **only
palatalized Georgian form anywhere in this source set** — and it is reported as an
identifiably-foreign, Russian-flavoured pronunciation of a specific lexical item, not as a
productive adaptation strategy. It confirms that a palatalized realization is *sayable*, and that
Georgian speakers hear it as marked and Russian. It does not tell us what a Georgian grammar does
with foreign /Cʲ/ generally.

---

## 4. Stress and length

### 4.1 The rule to implement

**Primary stress on the first syllable of the word. No secondary stress. No weight sensitivity.**

This is `borise2023`'s conclusion: "initial syllables in Georgian words are marked by greater
duration than all subsequent syllables, regardless of syllable count and phrasal context"
[borise2023 p.1], and after excluding domain-initial strengthening as an alternative, "this effect
is best phonologically interpreted as cuing stress, fixed on the initial syllable" [borise2023
p.32]. The correlate is **duration**, not F0; intensity peaks initially too but declines gradually
across the whole word, which she says "questions the link between intensity and stress"
[borise2023 p.32].

Butskhrikidze independently states the accent is **fixed-initial and stem-bound** — *déda* 'mother'
→ *déd-eb-i* 'mothers', accent never moving onto an affix [butskhrikidze2002 p.48], and
"Modern Georgian has fixed accent, which falls on the first syllable of a word"
[butskhrikidze2002 p.152]. Clusters do not perturb it; historically the *reverse* is proposed
(fixed initial accent caused the vowel deletions that created the clusters), which she flags as
speculative and out of scope [butskhrikidze2002 p.152].

### 4.2 CONFLICT

`CONFLICT:` Sources disagree on whether Georgian has word-level stress at all and where it falls.
**Robins & Waterson (1952)**, reported second-hand, propose a length-conditioned alternating
pattern (disyllables initial; trisyllables 1st or 2nd; tetrasyllables 2nd, or 1st+3rd;
pentasyllables 1st+3rd or 2nd+4th; 6+ syllables 1st + antepenult), adding that "stress is weak in
Georgian and is realized through high pitch" [jun2007 p.41]. **Aronson (1990:18)**, also
second-hand, proposes 1st-or-antepenult for words ≤4 syllables and 1st+antepenult for longer words
[jun2007 p.41; borise2023 p.4]. A large introspective literature (Tschenkeli 1958, Tevdoradze
1978, Akhvlediani 1949, Vogt 1971, Hewitt 1995, Skopeteas & Féry 2016 …) variously puts stress on
the initial, antepenult, or penult by syllable count, and a further camp (Gorgadze 1912, Marr
1925, Zhghenti 1953/1963) denies lexical stress exists at all [borise2023 p.3–4]. Against these,
**Jun, Vicenik & Lofstedt (2007)** find durational/amplitude prominence only on the
word/AP-initial syllable and reanalyse the apparent antepenultimate stress as an **Accentual-Phrase
phrase accent (H+L)** that tracks the *phrase's* antepenult and can cross word boundaries, not the
word's [jun2007 p.42–43]. **Borise (2023)** resolves it in favour of fixed initial stress cued by
duration, with all F0 phenomena — including a **low phrase accent (L) on the penult** in
yes/no-questions, wh-questions and narrow focus — reserved for phrasal prosody [borise2023 p.1,
p.32]. Wikipedia records the residual disagreement: "there is disagreement as to whether Georgian
has lexical stress" [wiki-ka §Prosody].

*Reason for choosing Borise's rule:* the only two studies that measured anything (jun2007,
borise2023) both find the word-initial syllable is the only one with a duration/amplitude
correlate; every rival locus turns out phrasal or is inconsistent across authors. A deterministic
tool should take the newest, best-evidenced, simplest rule.

### 4.3 Stress is weak — consider not marking it at all

Every source that comments calls Georgian stress faint:
- "stress is weak in Georgian" [jun2007 p.41, reporting Robins & Waterson]; "not as prominent as
  stress in English" [jun2007 p.42].
- "Native speakers of Georgian have no consistent intuitions about stress placement, other than
  that stress never targets the ultima. There are no minimal pairs based on stress"
  [borise2023 p.3].
- "word stress in contemporary Georgian is considerably weaker than phrasal prosodic targets"
  [borise2023 p.4, reporting Chikobava 1942, Tschenkeli 1958].
- "The Georgian stress is so faintly distinguished that one has to really search for it"
  (Chikobava 2008:98, quoted at [gabunia2021 p.19]).
- "The stress (very light) is always on the first syllable" [peacecorps p.3].
- "there are no pairs of words in Georgian that contrast in meaning due to stress placement"
  [wiki-ka §Prosody].

*For output romanization this means: do not write an accent mark. Initial stress is the default an
English reader will apply anyway.*

### 4.4 Length

**No contrastive vowel length; no nasalization** [shosted2006 p.262]. Toft (1999) as reported:
"There are no long vowels or diphthongs in Georgian" [butskhrikidze2002 p.178]. The one long vowel
is the non-contrastive coalescence of identical vowels across a morpheme boundary,
/kʼibɛɛbi/ → [ˈkʼibɛːbi] 'stairs' [wiki-ka §Vowels].

**Consequence for Irish input: all Irish vowel length is discarded.** /ɑː iː uː oː eː/ → /ɑ i u ɔ ɛ/.
Corroborated on the loan side: "English long vowels are shortened" in Georgian anglicisms
(see §3).

### 4.5 Stress in loans

`gabunia2021` gives the only statement: Georgian's weak initial stress and the obligatory -i
suffix together reshape loan pronunciation, i.e. **stress is re-assigned to Georgian's own initial
position rather than retained from the donor** [gabunia2021 p.19]. No source studies loan stress
systematically. Not covered elsewhere.

---

## 5. Romanization

### 5.1 The two attestable conventions, and why the apostrophe flipped

The **national system (2002)**, adopted by the State Department of Geodesy and Cartography and the
Institute of Linguistics of the Georgian Academy of Sciences, in use on driving licences since
1998, approved by presidential decree 24 Feb 2011, and **adopted by BGN/PCGN in 2009**
[ungegn-georgian p.1]:

| ა a | ბ b | გ g | დ d | ე e | ვ v | ზ z | თ t | ი i | კ k' | ლ l |
|---|---|---|---|---|---|---|---|---|---|---|
| მ m | ნ n | ო o | პ p' | ჟ zh | რ r | ს s | ტ t' | უ u | ფ p | ქ k |
| ღ gh | ყ q' | შ sh | ჩ ch | ც ts | ძ dz | წ ts' | ჭ ch' | ხ kh | ჯ j | ჰ h |

The **retired BGN/PCGN 1981 system** was "almost identical … but differed radically in the use of
the apostrophe. While in the national system the apostrophe signifies an abruptive sound in
contrast to the respective aspirated sound, in the BGN/PCGN system the apostrophe marked the
aspirated sound vs. the unmarked abruptive sound" [ungegn-georgian p.1]. Under BGN 1981:
თ t' / ტ t; კ k / ქ k'; პ p / ფ p'; ყ q; ჩ ch'; ც ts'; წ ts; ჭ ch.

**Assessment against the strand-4 names.** The project brief states the signature as "apostrophe =
ejective/glottal break". That is the **national 2002** meaning, not the 1981 one. Under BGN 1981,
`Th'tysh` and `Kas'queil` would be reading as *aspirated*, which is the opposite of harsh — and it
would make the plain letters the ejectives, so `Xelxyx` and `Ysclyth`, which have no apostrophe at
all, would come out as strings of ejectives, which is not what they look like. **Take the national
2002 convention: apostrophe = ejective.** `peacecorps` independently reaches the same convention
ad hoc for learners (`p'`, `t'`, `k'`, `t's`, `t'ch`, `gh`, `kh`, `zh`, `dz`) [peacecorps p.2–3],
which is evidence that apostrophe-for-ejective is what an English reader will guess.

### 5.2 Fit of the five existing names, segment by segment

| Name | Reading under national 2002 | Verdict |
|---|---|---|
| **Xelxyx** | needs `x` = ხ /x/, and a `y` vowel | Phonologically perfect apart from `y`: /xɛlxix/; the medial cluster `lx` is directly attested (Appendix 3, *xalx-i* 'people'); /x/ is a licit stem-final. Only the spelling `x` (national writes `kh`) and the vowel `y` deviate. |
| **Ysclyth** | `y`, `sc` = /sk/, `th` = /tʰ/ | /isklitʰ/. Word-initial /i/ fine; `sk` is attested initially (*skesi* 'gender'); stem-final /tʰ/ fine. Respell `sc`→`sk`; `th`→`t` under national. |
| **Kas'queil** | `k` /kʰ/, `s`, `'`, `q`, `ue`, `i`, `l` | The apostrophe sits *after* `s`, which cannot be ejective. Only coherent reading: the apostrophe belongs to the **following** ყ, i.e. Kas-q'ueil /kʰɑsqʼvɛil/ or /kʰɑsqʼuɛil/. |
| **Th'tysh** | `th'` + `tysh` | Does not parse. `th` is not a Georgian digraph in any system, and there is no consonant after the apostrophe for it to ejectivize. Regularizable as **T'tysh** /tʼtʰiʃ/ (ejective + aspirate, a *non*-harmonic tt cluster) or **Tht'ysh** /tʰtʼiʃ/. |
| **Tchaeul** | `tch` for an affricate; `aeu`; `-l` | `tch` matches `peacecorps`'s `t'ch` for ჭ /tʃʼ/. The vowel run `aeu` is the one hard violation: Georgian bans adjacent vowels within a morpheme [shosted2006 p.262]. |

### 5.3 Proposed convention set

**Base: the national 2002 system, apostrophe = ejective, with four documented deviations.**

| # | Deviation | Georgian letter | National | Use instead | Why |
|---|---|---|---|---|---|
| D1 | back fricative | ხ /x/ | `kh` | **`x`** | Required by *Xelxyx*. `x` is the ISO 9984 value and the common "unofficial"/keyboard value [wiki-ka-romanization], so it is attestable, not invented. It also pulls the strand away from Welsh, which spells /x/ `ch` — an explicit project goal. Keep ღ /ɣ/ as `gh`. |
| D2 | ejective palato-alveolar affricate | ჭ /tʃʼ/ | `ch'` | **`tch`** | Required by *Tchaeul*. `peacecorps` writes `t'ch`. Leaves ჩ /tʃʰ/ = `ch`, and frees the apostrophe for stops. |
| D3 | the y-vowel | — | — | **`y` = an orthographic variant of `i`** | Georgian has no /ɨ/ or /y/, and no source supports adding one. Writing /i/ as `y` in closed and non-initial syllables costs *nothing phonologically* and gives an English reader the lax [ɪ] the strand wants. *Th'tysh* = /tʰtʼiʃ/, *Xelxyx* = /xɛlxix/, *Ysclyth* = /isklitʰ/. |
| D4 | word-final | — | nom. `-i` | **output the bare stem** | Decisive; see §6.1 and §8.6. All five existing names are consonant-final; every Georgian *word* is vowel-final. Georgian **stems** may end in any of the 27 consonants except /h/, in sequences up to five members [butskhrikidze2002 p.98]. Romanizing the stem is the principled way to get consonant-final names that are still Georgian. |

**Kept from the national system, with the reader-traps flagged:**

- **`q'` = ყ /qʼ/**, the uvular ejective. Trap: English readers see `qu` and say /kw/. In
  *Kas'queil* the `u` is really /v/ or a hiatus vowel. **Recommend never writing `qu`** — write
  `q'v` or `q'u` explicitly. (BGN 1981 and ISO 9984 both write bare `q`, so `q` without apostrophe
  is also attestable if the apostrophe count gets too high.)
- **`ts` `dz` `ch` `zh` `sh` `gh`** digraphs. Trap: `ts` is ambiguous between /tsʰ/ (ც) and a
  /tʰ+s/ sequence, and `ch` between /tʃʰ/ (ჩ) and /tʰ+ʃ/. These sequences do occur. Rule: never
  emit a bare `t`+`s` or `t`+`sh` boundary — insert a separator or re-order.
- **Apostrophe placement: *after* the consonant it ejectivizes** (`k'`, `t'`, `p'`, `q'`, `ts'`).
  This reproduces *Th'tysh*'s shape (consonant + apostrophe) and forces *Kas'queil* to be re-spelled
  **Kasq'ueil**. This is the one place where following the standard changes an existing name.
  → **decision for the tool's author.**
- **Vowels `a e i o u`** = /ɑ ɛ i ɔ u/. No accents, no length marks (§4.4).
- **No stress mark** (§4.3).

**Worked example of the whole scheme** — the Irish name *Lasairchos* 'Flamefoot' /ˈl̪ˠɑsˠəɾʲxosˠ/,
run through §3 and §8, would surface as a stem like `lasartchos-` → romanized **Lasartchos**;
under D3, **Lasartchos** ~ *Lasartchys*. (unattested — this is an illustration of the conventions,
not a source claim.)

---

## 6. Morphology usable for epithets

### 6.1 The nominative -i — the single most visible Georgian fact

Declension depends on whether the noun **root** ends in a consonant or a vowel
[wiki-ka-grammar §Declension]:

| Case | C-final root (*k'ats-* 'man') | V-final truncating (*mama-* 'father') | V-final non-truncating (*Sakartvelo-*) |
|---|---|---|---|
| Nominative | **-i** k'ats-**i** | -∅ mama | -∅ Sakartvelo |
| Ergative | -ma k'ats-ma | -m mama-m | -m Sakartvelo-m |
| Dative | -s k'ats-s | -s mama-s | -s Sakartvelo-s |
| Genitive | -is k'ats-is | -is* mam-is | -s Sakartvelo-s |
| Instrumental | -it k'ats-it | -it* mam-it | -ti Sakartvelo-ti |
| Adverbial | -ad k'ats-ad | -d mama-d | -d Sakartvelo-d |
| Vocative | -o k'ats-o! | -∅ mama! | -∅ Sakartvelo! |

`*` = the root's final vowel truncates (roots in *-e* and *-a* truncate; roots in *-o* and *-u* do
not) [wiki-ka-grammar §Declension].

So: **-i is a nominative case suffix on consonant-final roots, not part of the stem**, and it
disappears in every other case. This is exactly why §5's D4 (output the stem) is legitimate rather
than a cheat — *k'ats-* is as much a Georgian word-form as *k'atsi* is; it is what you see in the
ergative, genitive and vocative.

It is obligatory on foreign consonant-final nouns and names: every consonant-final item in the
`ka-wiki-title` harvest takes it (Amsterdam → *amst'erdam-i*, Berlin → *berlin-i*, Cork →
*k'ork'-i*), and vowel-final ones take nothing (Ankara → *ank'ara*, Chicago → *chik'ago*,
Glasgow → *glazgo*) — see §7.

**Important detail from the harvest:** in a multi-word foreign name, **only the last word takes
-i**: *jorj vashingt'oni* (George Washington), *uiliam sheksp'iri* (William Shakespeare),
*sherlok' holmzi* (Sherlock Holmes), *elvis p'resli* (Elvis Presley). And a non-final element may
therefore end in a full consonant cluster: Michael → *maik'l* (no -i), *bat'ler* (Butler).

Georgian has **no articles** and **no grammatical gender** [wiki-ka §Grammar summary].

### 6.2 Syncope with the plural -eb-

`X → ∅ / _ C(C) + eb`, where X ∈ {a, e} in the last syllable of the stem:

> "When a suffix (especially the plural suffix -eb-) is attached to a word that has either of the
> vowels *a* or *e* in the last syllable, this vowel is, in most words, lost. For example,
> *megobari* means 'friend'; *megobrebi* (megob∅rebi) means 'friends'" [wiki-ka §Morphophonology].

The plural sits between root and case suffix: *k'ats + eb + i* 'men' (nom.), *k'ats + eb + ma*
(erg.); truncating *xe* 'tree' → *xe + eb + i*; non-truncating *gogo* 'girl' → *gogo + eb + i*
[wiki-ka-grammar §Pluralisation]. The plural is **not** used after a numeral: *xuti k'atsi*
'five men', not *xuti k'atsebi* [wiki-ka-grammar §Pluralisation].

**This is the cluster-manufacturing rule.** *megobari* → *megobrebi* creates the `br` cluster out
of nothing. For the generator it means a Georgian-flavoured plural or derived form of an Irish stem
should *gain* clusters, not lose them. See §8.7 and §2.10.

### 6.3 Surname and origin suffixes [wiki-ka-name §Surnames]

Georgian surnames derive from patronymics or, less often, toponyms, and the suffix varies by
region:

| Suffix | Meaning / origin | Region | Examples |
|---|---|---|---|
| **-shvili** (-შვილი) | 'child' | west + east Georgia; also common among Georgian Jews | Baratashvili, Andronikashvili, Guramishvili |
| **-dze** (-ძე) | 'son' | west + east Georgia | Abashidze, Arveladze, Kaladze |
| **-eli** (-ელი) | 'from (place)' | east + west | Jaqeli, Tsereteli, Amashukeli |
| **-uri / -uli** (-ური/-ული) | relational, 'of' | mountainous east Georgia | Donauri, Burduli |
| **-ani** (-ანი) | Svan | mountainous west | Dadeshkeliani, Dadiani, Kipiani |
| **-ia, -ua, -va, -ri** | Mingrelian | west | Abakelia, Chichua, Gvazava, Mujiri |
| **-shi** (-ში) | Laz | west | Tugushi, Khalvashi, Jashi |
| **-khi** (-ხი) | — | south | Meskhi, Lashkhi |
| **-oni** (-ონი) | — | Tao-Klarjeti | Bagrationi |
| **-ti** (-ტი) | — | west | Glonti, Jgenti |

Ethnonym patronymics are a productive live pattern: *Kartvelishvili* 'child of a Georgian',
*Berdzenishvili* 'child of a Greek', *Prangishvili* 'child of a Frank/Western European'
[wiki-ka-name §Surnames]. **This is the readiest epithet machinery in the language**: attach
-shvili / -dze to any adapted Irish stem and you get a plausible Georgian surname.

Most common real surnames, for calibration: Beridze, Kapanadze, Gelashvili, Maisuradze, Giorgadze,
Lomidze, Tsiklauri, Bolkvadze, Kvaratskhelia, Nozadze [wiki-ka-name §Surnames].

### 6.4 -uri vs -uli — an /l/~/r/ dissimilation

The nominalizing/relational suffix is **-uri** normally but **-uli when the base contains a
rhotic**: /tʰbilisuri/ 'of Tbilisi (non-person)' vs /kʰɑrtʰuli/ 'of Georgia (non-person)'
[shosted2006 p.261, citing Hewitt 2005:282]. `wiki-ka-name` lists both as surname suffixes without
stating the conditioning [wiki-ka-name §Surnames]. Directly usable and cheap to implement:
`-uri → -uli / [stem containing r] _`.

### 6.5 Given-name shape, for calibration

Most common male given names: Giorgi, Davit, Zurab, Levan, Aleksandre, Irakli, Mikheil, Tamaz,
Nikoloz, Avtandil. Female: Nino, Tamar, Mariam, Maia, Nana, Ketevan, Natela, Manana, Natia, Eka,
Ana [wiki-ka-name §Given names]. Note that several male names are **consonant-final in citation
form** (Davit, Zurab, Levan, Tamaz, Nikoloz, Avtandil, Tamar) — i.e. Georgian personal names
already appear without the nominative -i, which supports §5's D4.

---
## 7. Attested adaptations

`attested.tsv` in this directory — **143 rows**, per `../ATTESTED-FORMAT.md`.

**Provenance mix:**

| Provenance | Rows | What it is | Both sides in IPA? |
|---|---|---|---|
| `gabunia2021` | 34 | The Appendix-B experimental table (24 items, Geo-like column, English-like recorded in `note`) plus transphonemization examples from the body | Georgian side only; the thesis gives **no English IPA column** |
| `rayfield2023` | 15 | Anglicisms in Georgian written form | **No** — Georgian orthography only, no IPA anywhere in the article |
| `kirvalidze2017`, `asaturova-garibashvili` | 6 | Loan lists; Kirvalidze gives a few bracketed transcriptions | Partly |
| `ka-wiki-title` | 88 | The Wikipedia-title transliteration harvest | Georgian orthography; **IPA derived, see below** |

**Biases, all of which matter:**

1. **The donor is English throughout.** There is no Russian→Georgian, no Persian→Georgian, no
   Arabic→Georgian adaptation data here — which is why §8.1 has no palatalization precedent. The
   older and larger contact layers are invisible.
2. **`gabunia2021`'s 24 items were chosen for sociolinguistic salience, not phonological
   coverage** [bib.md]. There is no /θ/ item, no /ð/ item, and nothing testing cluster repair.
3. **The `ka-wiki-title` rows are editorial practice, not speech** — Wikipedia article titles,
   frequently Russian-mediated, reflecting a written convention. Every such row carries the tag.
   Translation rows were discarded (see `digest-log.md`).
4. **`target_ipa` on the `ka-wiki-title` rows is derived, not quoted.** The source gives Mkhedruli
   only; the IPA was produced by mechanical letter-by-letter transliteration, which is defensible
   because Georgian orthography is one-to-one with the phoneme inventory [shosted2006 p.255] — but
   it is a derivation and the provenance field says so on every row. Those strings will not show
   intrusive vocoids (§2.12), running-speech cluster reduction [shosted2006 p.262], or the
   /qʼ/ → [ʔ] variation (§1.3).
5. **`source_ipa` is blank on every row** — none of the sources gives the donor pronunciation in
   IPA. Per `ATTESTED-FORMAT.md`, it was left blank rather than invented.

**What the harvest is actually good for**, beyond bulk: it is the only large sample showing
(a) the **-i on the last word only** of a multi-word name, with bare consonant-final and even
cluster-final non-final elements (*jorj*, *maikʼl*, *batʼler*, *sanktʼ-*); (b) /f/ → /pʰ/ six
times over; (c) the English /s/+stop → Georgian /s/+**ejective** repair (§8.4), which no prose
source states but which appears in seven independent rows.

---

## 8. Irish-specific mismatch notes

### 8.1 Broad (velarized) vs slender (palatalized) — NO TARGET-INTERNAL PRECEDENT

**There is no Russian→Georgian loanword-adaptation source in this bibliography, and none was
found** [bib.md §"Could not find or verify": "No source found on Russian→Georgian adaptation
specifically, which is a pity: Russian is the older and larger contact layer and would give
vowel-reduction and palatalization data that the English material does not"]. Russian is the only
large donor with a systematic palatalization contrast, so **Georgian's treatment of foreign
palatalized consonants is undocumented in everything we hold.** This is the single biggest gap.

What the sources *do* give, that bears on it:

1. **Georgian has a productive secondary-articulation slot, but it is labial, not palatal.**
   Butskhrikidze's slot V is /v/, analysed as **labialization on the preceding consonant**:
   /qʼvɑvili/ → [qʼʷɑvili] 'flower', /kʰvɑ/ → [kʰʷɑ] 'stone' [butskhrikidze2002 p.87–88, p.96].
   Historical /u/ > /v/ confirms it is a live process: OG *sik'udili* > *sik'vdili* [sikʼʷdili]
   'death', *ekusi* > *ekvsi* [ɛkʰʷsi] 'six', *varsk'ulavi* > *varsk'vlavi* 'star'
   [butskhrikidze2002 p.95]. Shosted & Chikovani accept the analysis after voiceless obstruents
   but reject it after voiced stops (§1.6).
2. **No palatal series and no /j/ phoneme.** /i/ adjacent to a vowel is realized [i̯]~[j] in casual
   speech; /u o/ before a vowel as [w] [wiki-ka §Vowels]. So a written `Ci` is the closest thing
   Georgian has to `Cj`.
3. **Editorial practice does render foreign palatalization as `Ci`** — but only as
   Russian-mediated spelling, not as speech: Bruce → *brius*, München → *miunkheni*, New York →
   *niu-iork'i*, Reykjavík → *reik'iavik'i*, Enya → *enia* [ka-wiki-title, see §7]. **Tag this
   provenance every time it is used** — it is editorial convention, mostly via Russian ю/я/ü, not
   evidence about Georgian speech.

**The options, for the tool's author to choose between (not decided here):**

| Option | Rule | Cost / evidence |
|---|---|---|
| **A. Collapse** | Cʲ → C, Cˠ → C | Zero risk, zero Irish flavour. Every Irish minimal pair merges. |
| **B. Slender → `Ci`** | Cʲ → C + /i/ before a non-front vowel; Cʲ → C before /i ɛ/ | The only option with *any* attestation (point 3), though the attestation is orthographic and Russian-mediated. Inflates syllable count. |
| **C. Symmetric secondary articulation** | Cʲ → C+/i/, **Cˠ → C+/v/ (= Cʷ)** | Uses Georgian's own slot V (point 1) for the broad series. Fully systematic; makes both Irish series visible; produces exactly the kind of `Cv-` onsets Georgian is full of (*kva*, *gvalva*, *tvali*, *cvari*, *švili*, *γvino*, *xvadi*, *χ'vavili*). **No attestation for the palatal half.** Doubles cluster length, which Georgian tolerates better than any of the other three targets. |
| **D. Broad → dorsal co-articulation** | Cˠ → C + harmonic-cluster back element (e.g. /tˠ/ → /tʰx/) | (unattested) — pure overlay. Maximally "harsh"/on-brand for strand 4; the output would be indistinguishable from native Georgian harmonic clusters, which is either the point or the problem. |

*Note that under Option C the /v/ from broad consonants and the /v/ from Irish lenited b/m (§8.5)
would merge, and that Georgian's own slot-V /v/ is normally at most one per cluster
[butskhrikidze2002 p.108].*

### 8.2 Irish segments and their Georgian home

| Irish | Georgian | Basis |
|---|---|---|
| /ɣ/ | **/ɣ/** — native (ღ) | [shosted2006 p.255]. No repair. Unlike Welsh and Arabic, Georgian has this segment outright. |
| /x/ | **/x/** — native (ხ) | [shosted2006 p.255]. No repair. (Velar vs uvular: §1.2.) |
| /h/ | **/h/** — native but heavily restricted | Native (ჰ) [shosted2006 p.255], but "**never occurs in consonant sequences**" and is barred except word-initially [butskhrikidze2002 p.87]; **stems cannot end in /h/** [butskhrikidze2002 p.98]. Loans do keep it intervocalically: *k'op'enhageni*, *bethoveni*, *st'ok'holmi*; and Tehran → *teirani* shows outright **deletion** [ka-wiki-title]. Rule: keep /h/ word-initially and intervocalically; **delete elsewhere**. |
| /f/ | **/pʰ/** | See §3. Attested six ways in the harvest (Belfast → *belpasti*, Cardiff → *k'ardipi*, Oxford → *okspordi*, Philadelphia → *piladelpia*, San Francisco → *san-pransisk'o*, Wolfgang → *volpgang*) and in `gabunia2021`. Georgian has no /f/ (§1.4); [f] exists only as an allophone of /v/ before voiceless consonants, which is **not** available in the positions Irish /f/ occupies. |
| /v/ | **/v/** — native | [shosted2006 p.261]. No repair. |
| /w/ (< lenited b, m) | **/u/ word-initially, /v/ elsewhere** | See §3.3, which is a `CONFLICT:`. `gabunia2021` frames /w/ → /v/ as nativized and /u/ as prestige [gabunia2021 pp.14–15], but her own *weekend* has /u/ in both variants and her own *forward* → *poruardi*; Rayfield states the split **positionally** — initial /w/ → უ *u* (*u’ork’shopebi*), medial /w/ → ვ *v* (*netvorki*, *porvardi*) [rayfield2023 pp.23, 24]. The harvest matches: *uelsi*, *uiliam*, *uaildi*, *uinst'on* vs *vashingt'oni*, *varshava*, *volpgang* (the v-forms are the Russian-mediated ones, where the donor ⟨W⟩ already reads /v/). **Irish /w/ is usually word-initial after lenition, so the positional rule sends it to /u/ — a hiatus vowel, not a consonant. → decision.** |
| /p/ (rare in native Irish) | **/pʼ/** (nativized) or /pʰ/ (prestige) | `gabunia2021`'s /p t k/ → ejective rule (§3). |
| /ŋ/ | **/nɡ/** | Harvest: England → *inglisi*, Springsteen → *springst'ini*, Washington → *vashingt'oni*, Wolfgang → *volpgang* (word-final -ng kept). Georgian has no /ŋ/. `gabunia2021` gives /ŋ/ → /n/ or /nɡ/. |
| voiceless sonorants | **plain sonorant** (unattested) | No Georgian precedent in any source. Georgian has one /l/, one /n/, one /m/, one rhotic. Options: (i) collapse to the voiced sonorant; (ii) sonorant + /h/ — ruled out, /h/ cannot occur in a cluster [butskhrikidze2002 p.87]. **(i) is effectively forced.** |
| /ɾ/ vs /r/ | **one rhotic /ɾ~r/** | Georgian's rhotic is a single phoneme, tap-dominant (mean intervocalic closure ~20 ms, trilling rare) [shosted2006 p.261]. Both Irish rhotics collapse. |
| /l̪ˠ lʲ n̪ˠ nʲ/ | **/l/ /n/** (+ whatever §8.1 decides) | Georgian has one /l/ and one /n/. /l/ has an allophonic velarized [ɫ] before back vowels [wiki-help-ipa-ka n.4], which coincidentally covers broad /l̪ˠ/ for free before /ɑ ɔ u/ — but it is allophonic, not contrastive, so it cannot carry the Irish contrast. |
| /tʲ dʲ/ (affricated in some dialects) | /tʰ tʼ d/ or /tʃʰ tʃʼ dʒ/ | Georgian has a full affricate series to receive them if §8.1 opts for a palatalization-to-affrication treatment. (unattested for Georgian.) |
| /ə/ (schwa) | **/ɑ/ or /ɛ/** | **Georgian has no schwa**: "there is no phonemic schwa in Georgian, nor are there any phonological processes that would reduce underlying phonemic vowels to schwa" [crouch2022-diss §1.3 p.39]. The intrusive vocoid (§2.12) is schwa-*like* but sub-phonemic and must not be used as a target. Harvest practice follows donor spelling. **Decision needed.** |

### 8.3 Vowel length and diphthongs

**Length: discarded.** Georgian has no contrastive vowel length [shosted2006 p.262] (§4.4), and
English long vowels shorten in Georgian anglicisms (§3). /ɑː iː uː oː eː/ → /ɑ i u ɔ ɛ/.

**Diphthongs /iə uə əi əu/:** Georgian has no diphthongs and bars VV within a monomorphemic word
[butskhrikidze2002 p.83; shosted2006 p.262]. But **loanwords are precisely where Georgian tolerates
VV** — the exceptions Butskhrikidze lists are all loans (*musaipi*, *paipuri*, *p'aik'i*, *daira*,
*maudi*) [butskhrikidze2002 p.83 n.8], and the transliteration harvest is full of it
(*uaildi*, *jeimz*, *joisi*, *shineid*, *sheimas*, *reik'iavik'i*, *sidnei*, *kairo*). Where two
vowels do meet they are **heterosyllabic** [shosted2006 p.262].

Recommended mapping (extrapolated from the loan pattern, not stated by any source):
`/iə/ → /iɑ/` · `/uə/ → /uɑ/` · `/əi/ → /ɛi/` · `/əu/ → /ɔu/`, each as two syllables.
The alternative — monophthongize to the first element — is simpler and equally defensible; the
loan evidence favours keeping both vowels.

### 8.4 Which Irish onset clusters does Georgian ban?

Checked against Appendix 2 [butskhrikidze2002 pp.197–205] and the initial-CC grid, table (62)
[butskhrikidze2002 p.110]. **The answer is: almost none.** Georgian is the one target of the four
that will not repair Irish clusters.

| Irish onset | Georgian status | Rule (§3) |
|---|---|---|
| /sp/ | **licit** — grid row `s` includes `p` and `p'` | none |
| /st/ | **ILLICIT as /stʰ/** — grid row `s` has `t'` but not `t`; Appendix 2 lists `st'` only | **substitution: /stʰ/ → /stʼ/**. Directly attested in loans: Istanbul → *st'amboli*, Stockholm → *st'ok'holmi*, Bristol → *brist'oli*, Amsterdam → *amst'erdami*, Manchester → *manchest'eri* [ka-wiki-title]. This is the single most reliable repair Georgian applies to English input. |
| /sk/ | **licit** — `sk` and `sk'` both attested (*skesi* 'gender', *sk'a* 'hive'); `sk` is also a harmonic cluster | none |
| /sm/ | **licit** — *smena* 'hearing' | none |
| /sn/ | **not attested** — absent from Appendix 2 and from grid row `s`, although `zn`, `šn`, `xn` all are | Appendix 2 is explicitly "not exhaustive", so this may be a gap rather than a ban. Options: leave as /sn/; or → /zn/ (attested, *zne* 'character'). **Decision needed, low stakes.** |
| /sl/, /sr/ | **licit** — *slok'ini*, *srola* | none |
| /ʃp ʃtʰ ʃtʼ ʃx ʃv ʃl ʃr ʃm ʃn/ (slender s + C) | **licit** — grid row `š` = p p' t t' x v l r m n | none. Note `šk` appears in the harmonic-cluster table but *not* in grid row `š` — an internal inconsistency in the thesis. |
| /kn/, /gn/ | **licit** — *knari* 'lyre', *k'nut'i* 'kitten', *gnomi* | none |
| /mn/ | **licit** — Appendix 2 excludes /m/+C by design [butskhrikidze2002 p.197], but `wiki-ka §Phonotactics` gives *mnaxe*, and *mtsvane* 'green', *mta* 'mountain', *mk'vleli* 'murderer' show m+C is fully productive | none |
| /bl br gl gr dr tr kr kl/ | **all licit** — grid rows b, g, d, t, k all admit l and r | none |
| /fl fr/ | **licit after /f/ → /pʰ/** — *ploba*, *prinveli* 'bird' | substitution only |
| /pl pr tl tv dv gv kv/ | **licit** | none |

**Coda side.** Irish word-final clusters have no direct Georgian analogue because **Georgian has no
word-final consonant sequences at all** [butskhrikidze2002 p.98, p.105] — but **stem**-final
sequences of up to five members are fine (§2.5), and stem-final is where our output lives (§8.6).
The stem-final restriction that bites is: **harmonic clusters are the only obstruent sequence
permitted stem-finally** [butskhrikidze2002 p.104]; everything else must be
obstruent+sonorant, sonorant+obstruent (mostly loans), or contain a sonorant. Irish final /xt/
(as in *-acht*) is a fricative+stop obstruent sequence that is **not** harmonic (x is dorsal, t is
coronal — the wrong order) → needs repair. Note the harvest's own answer for exactly this word:
**Connacht → კონაქტი *k'onakt'i*** — /xt/ → /kʰtʼ/, i.e. the fricative hardens to a stop and the
stop ejectivizes [ka-wiki-title]. That is a directly usable precedent for the Irish *-acht* suffix.

### 8.5 Irish initial mutations and genitives

The sources say nothing about how Georgian treats donor-side alternations; loans arrive as fixed
citation forms. **Not covered — leave for the Irish digest.** The one relevant target-side fact:
Georgian's own morphology is purely suffixal for nouns, so a mutated Irish initial will simply be
adapted as whatever segment it surfaces as (lenited /b/ → [v] → Georgian /v/; lenited /m/ → [w] →
/v/; lenited /k/ → [x] → /x/, all of which land on native Georgian segments — see §8.2).

### 8.6 The word-final problem — the decision that shapes everything

**This is the largest single conflict between Georgian's grammar and the strand's brief.**

- The strand-4 signature (per `project-goals.md`) is "every word consonant-final", and all five
  existing names — *Tchaeul, Th'tysh, Kas'queil, Xelxyx, Ysclyth* — are consonant-final.
- Georgian says the opposite: "a well-formed minimal word in Georgian must be vowel-final. The
  occurrence of a single consonant or a consonant sequence is disallowed in word-final position"
  [butskhrikidze2002 p.98]; there are **no word-final consonant sequences** at all
  [butskhrikidze2002 p.105]; consonant-final stems obligatorily take the nominative -i (§6.1);
  and every consonant-final foreign name in the harvest takes it (§7).

**Recommended resolution: output the STEM, not the nominative singular.** This is not a fudge:

1. Georgian **stems** may end in **any of the 27 consonants except /h/**, in sequences of up to
   five members [butskhrikidze2002 p.98–99].
2. The nominative -i is a **case suffix, not part of the stem** — it is absent in the ergative,
   genitive, instrumental, adverbial and vocative (§6.1).
3. Multi-word foreign names in Georgian editorial practice already show bare consonant-final and
   even cluster-final words: *jorj* (George), *maik'l* (Michael), *bat'ler* (Butler), *sankt'-*
   (Sankt), *elvis*, *sherlok'*, *uinst'on* [ka-wiki-title].
4. Several of the most common Georgian **given names are consonant-final in citation form**:
   Davit, Zurab, Levan, Tamaz, Nikoloz, Avtandil, Tamar [wiki-ka-name §Given names].

The residual exceptions Butskhrikidze allows for word-final consonants are sonorant-final adverbs
(*c'in*, *xval*, *gušin*) and voiceless-obstruent-final ones (*zevit*, [k'argat])
[butskhrikidze2002 p.98] — which happens to be exactly the *Xelxyx* / *Ysclyth* / *Tchaeul* shape.

**If instead the -i is kept**, every name becomes vowel-final and the strand loses its most visible
signature; the five existing names would have to be re-read as *Tchaeuli, Th'tyshi, Kas'queili,
Xelxyxi, Ysclythi*. → **decision for the tool's author.**

### 8.7 Where Georgian *adds* clusters

Unlike the other three targets, Georgian's characteristic process is cluster **creation**, not
repair. Two mechanisms are available and both are documented:

1. **Syncope** (§2.13): a stem ending in a sonorant loses its last /a e o/ before any -V(C) suffix.
   Apply a §6 suffix and the Irish stem gains a cluster for free. *megobari* → *megobrebi* is the
   model.
2. **The plural -eb-** (§6.2), which triggers the same syncope.

If the aim is output that looks maximally Georgian rather than merely Georgian-compatible, this is
the lever — and it is a *grammar* lever, not an overlay.

---

## 9. Open questions

1. **Palatalization has no precedent.** §8.1. No Russian→Georgian source exists in the open
   literature we could find; the `ka-wiki-title` `Ci` spellings are editorial and Russian-mediated.
   Four options laid out; none decided.
2. **Which laryngeal series receives Irish /p t k/** (§3.1). `gabunia2021`'s nativized layer
   says ejectives — but that is the State Language Department's *prescriptive* norm, and her own
   measured majority is the aspirate (59.6% Eng-like vs 36.9% Geo-like across 1320 tokens),
   except in post-consonantal medial position where the ejective wins 84.1%. Rayfield, describing
   written usage, finds the ejective the default for *t* and *k/c* but admits that for კ/ქ he
   "has not been able to identify any consistent decisive factor". Irish /p t k/ are themselves
   aspirated, so phonetic similarity argues for the aspirate. → decision. (This digest recommends
   the ejective, since it is the norm, it dominates exactly where Irish clusters put stops, and it
   is what makes strand 4 sound like strand 4.)
2b. **/w/ → /u/ or /v/** (§3.3). The digest proposes a positional rule that no single source
   states, assembled from four that each state half of it. Irish /w/ is mostly word-initial after
   lenition, so the choice changes almost every lenited-b/m name. → decision.
2c. **Within-word laryngeal harmony** (§3.1): Gabunia and Rayfield both report that a word takes
   *either* all-ejective or all-aspirate plosives, never a mix. Worth implementing, but it means
   the /p t k/ rule is word-level, not segment-level.
3. **Stem vs nominative output** (§8.6) — the single most consequential formatting decision.
4. **Apostrophe placement** in the romanization (§5.3): following the national standard forces
   *Kas'queil* → *Kasq'ueil*.
5. **/ə/ has no Georgian target** (§8.2). The intrusive vocoid is not usable as one.
6. **/sn/**: gap or ban? (§8.4)
7. **Velar vs uvular back fricatives** (§1.2) — cosmetic, but the IPA output has to pick.
8. **Whether to use syncope actively** (§8.7) to manufacture clusters, or only to preserve the
   Irish ones.
9. **`gabunia2021`'s data set is 24 English items chosen for sociolinguistic salience, not
   phonological coverage** [bib.md]. There is no peer-reviewed Georgian loanword-phonology paper
   with a full substitution table; several candidates exist but are login-walled.
10. **Six vs seven vs eight maximum onset consonants** (§2.1) — irrelevant in practice, since no
    Irish input approaches the limit.
