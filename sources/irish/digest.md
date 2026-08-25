# Source digest: Irish (Gaeilge), Connacht reference — **donor/source language**

This directory is the **source side** of the project. Irish supplies the words; the four target
languages supply all rules. The template (`../DIGEST-TEMPLATE.md`) is written for a target
language, so three sections are re-pointed for the donor role, and one is added:

| Template section | Donor-role reading used here |
|---|---|
| §2 Syllable structure and phonotactics | **What Irish words bring to a target**: the syllable shapes, the initial and final cluster inventory, and the epenthesis Irish itself applies before the word ever reaches a target |
| §3 Repair strategies | **What alternations the source side produces**: lenition and eclipsis as phoneme→phoneme tables, plus the genitive/vocative changes that appear in names and epithets |
| §5 Romanization | Reading Irish orthography (how to hand-transcribe an input name), and what the donor spelling offers the per-target romanizers |
| §8 Irish-specific mismatch notes | **An explicit catalogue of the Irish segments and structures that will need a decision in every target** — the item list the four target digests must each answer |
| §10 (new) | **Old Irish**, for strand 5 |

Citation rule as in the brief: `[key p.N]` / `[wiki-x §Section]` on every factual claim;
`(unattested)` on anything supplied from general knowledge; `CONFLICT:` where sources disagree.

---

## 0. Variety and scope

**Reference variety: Connacht (Connemara / Cois Fharraige / Erris), with the Wikipedia
"standard-ish" IPA scheme.** This matches the user's own hand transcriptions — *Ciara*
/ˈkɪə.ɾˠə/, *Matánach* /ˈmˠat̪ˠɑːnˠəx/, *Lasairchos* /ˈl̪ˠɑsˠəɾʲxosˠ/ — which show initial stress
(not Munster), a two-way rhotic /ɾˠ ɾʲ/, dental /t̪ˠ/, and velarized /l̪ˠ/.

The transcription system used throughout is the Wikipedia scheme, which is itself based on Ní
Chasaide's IPA-Handbook description [wiki-help-ipa-irish §Comparison of transcription schemes].
That page also gives a conversion table between this scheme and Quiggin (1906, Glenties),
Breatnach (1947, Ring), Ó Sé (2000, Dingle), Mhac an Fhailigh (1968, Erris), Ó Siadhail (1988,
Cois Fharraige) and *Foclóir Póca* (Lárchanúint) — use it when reading any of those
[wiki-help-ipa-irish §Comparison of transcription schemes].

Where the dialects differ in a way that matters for the tool, this digest flags it as
**[M]** Munster, **[U]** Ulster, **[C]** Connacht.

Source-base caveats:
- The **cluster inventory** (§2) traces entirely to Ní Chiosáin 1999, which is paywalled and not
  held; Wikipedia and the three Commons cluster charts are our only route to it
  [wiki-irish-phonology §Word-initial consonant clusters].
- **Ní Chasaide's** description is **Ulster (Gaoth Dobhair, Donegal)** [nichasaide1999 p.111];
  where it conflicts with the Connacht picture, Connacht wins for this project.
- **Ní Chiosáin et al. 2018** and the two Bennett-group papers are **Connemara** — i.e. exactly
  our reference dialect — and are the articulatory evidence base for §8.1.
- **Quiggin 1906** is Ulster (Glenties) in a pre-IPA notation; used here only for the two facts
  nothing else open supplies (voiceless sonorants, fortis/lenis length).

**PHOIBLE:** `../../chat-imports/phoible_inventories_starter.csv` **has no Irish row** — it
contains only the four target inventories. There is therefore nothing to reconcile; §1 below is
the inventory, assembled from Wikipedia + Ní Chasaide, and it is what the tool should use as
the donor inventory.

---

## 1. Inventory

### 1.1 Consonants — the full broad/slender pair list

"Almost all consonants (except /h/) come in pairs, a 'broad' and a 'slender' pronunciation."
Broad = velarized (◌ˠ) or plain velar (/k ɡ/); slender = palatalized (◌ʲ)
[wiki-irish-phonology §Consonants].

| | Labial | Coronal | Dorsal | Glottal |
|---|---|---|---|---|
| **Stop, voiceless** | pˠ / pʲ | t̪ˠ / tʲ | k / c | — |
| **Stop, voiced** | bˠ / bʲ | d̪ˠ / dʲ | ɡ / ɟ | — |
| **Continuant, voiceless** | fˠ / fʲ | sˠ / ʃ | x / ç | **h** |
| **Continuant, voiced** | **w** / vʲ | l̪ˠ / lʲ | ɣ / j | — |
| **Nasal** | mˠ / mʲ | n̪ˠ / nʲ | ŋ / ɲ | — |
| **Tap** | — | ɾˠ / ɾʲ | — | — |

[wiki-irish-phonology §Consonants]

The 31-segment list, spelled out, is the donor's phoneme set:

    pˠ pʲ  bˠ bʲ  t̪ˠ tʲ  d̪ˠ dʲ  k c  ɡ ɟ
    fˠ fʲ  sˠ ʃ   x ç   h
    w vʲ   ɣ j
    mˠ mʲ  n̪ˠ nʲ  ŋ ɲ
    l̪ˠ lʲ  ɾˠ ɾʲ

Asymmetries the tool must know about:

- **/h/ has no broad/slender partner** — the single unpaired consonant
  [wiki-irish-phonology §Consonants]. It can be elided intervocalically: *athair* → /aːɾʲ/
  [wiki-help-ipa-irish note 4].
- **The broad partner of /vʲ/ is /w/, not /vˠ/.** /w/ (spelled ⟨bh, mh, v⟩) has allophones
  [w] and [vˠ]. **[M]** generally only [vˠ]; **[U]** generally only [w]; **[C]** [w]
  word-initially before a vowel (*bhfuil* [wɪlʲ]), [vˠ] elsewhere (*naomh* [n̪ˠiːvˠ], *fómhar*
  [ˈfˠuːvˠəɾˠ]) [wiki-irish-phonology §Allophones]. **This matters:** a Connacht input name
  will show [w] initially and [vˠ] medially/finally for the same phoneme.
- **The tap has only coronal members** /ɾˠ ɾʲ/; there is no labial or dorsal tap
  [wiki-irish-phonology §Consonants]. Broad /ɾˠ/ is a tap; slender /ɾʲ/'s primary allophone is
  **[ɹ̝ʲ]**, a palatalized postalveolar *fricative* (Ó Sé 2000)
  [wiki-irish-phonology §Allophones] — worth knowing when picking a target substitute.
- **/j/** has three allophones: [j] prevocalically except before /iː/ and syllable-finally
  (*dheas* [jasˠ], *beidh* [bʲɛj]); **[ʝ]** (voiced palatal fricative) preconsonantally
  (*ghrian* [ʝɾʲiən̪ˠ]); [j˔] before /iː/ [wiki-irish-phonology §Allophones]. **[M]**
  word-final /j/ is fortified to [ɟ], merging with /ɟ/ [wiki-help-ipa-irish note 2].
- **/x ç/ vs /h/ alternate** in many varieties. As the lenition product of /tʲ/ and /ʃ/, /h/ is
  replaced by [ç] before back vowels (*sheoil* /çoːlʲ/, *thabharfainn* /ˈçuːɾˠhən̠ʲ/).
  **[M]** /ç/ → [h] after a vowel (*fiche* [ˈfʲɪhə]). **[U]** (Tory Island) /x/ can become [h]
  (*cha* [ha]) or delete finally / before /t̪ˠ/ (*seacht* [ʃat̪ˠ])
  [wiki-irish-phonology §Allophones].
- **Coronal place:** broad stops and approximants are **dental** [t̪ˠ d̪ˠ n̪ˠ l̪ˠ]; the rest of
  the coronals are alveolar; slender /ʃ/ is postalveolar. /tʲ dʲ/ may be alveolo-palatal
  affricates [tɕ dʑ] (Tourmakeady, Erris, Teelin) [wiki-irish-phonology §Allophones].
- **/c ɟ ɲ/** may be true palatals or palatovelars [k̟ ɡ˖ ŋ˖] (Ó Sé 2000)
  [wiki-irish-phonology §Allophones].
- **Aspiration:** voiceless stops are aspirated word-initially and **unaspirated after /sˠ ʃ/**
  (*scanradh* [sˠkauɾˠə]); voiced stops are incompletely voiced but never aspirated
  [wiki-irish-phonology §Allophones]. **[U]** Ní Chasaide reports the voiceless series is also
  **preaspirated**, "fairly widely… especially in non-intervocalic contexts"
  [nichasaide1999 p.113].
- **Not in the inventory:** the article nowhere flags /pˠ pʲ/ as marginal, and does not list
  /z ʒ/ at all [wiki-irish-phonology §Consonants]. Loan letters do add them at the margin: ⟨z⟩
  → /zˠ/ (*zú* /zˠuː/), ⟨j⟩ → [dʒ] "a non-native phoneme", substituted by /ʃ/ in integrated
  loans (*Seapáin* /ˈʃapˠaːnʲ/) [wiki-irish-orthography §Letters and letter names,
  §Grapheme to phoneme correspondence]. **For this project these should not appear in input
  names** — treat /z ʒ dʒ/ as out of the donor inventory.

**Fortis/lenis sonorants — a four-way L and N system in the transcription scheme, but not in
any one modern dialect.** Wikipedia's IPA key lists **four laterals** /l̪ˠ lˠ l̠ʲ lʲ/ and
**four nasals** /n̪ˠ nˠ n̠ʲ nʲ/ [wiki-help-ipa-irish §Consonants]. But: "Few, if any, modern
dialects of Irish distinguish all four types of L sound. Most dialects have merged /l̪ˠ/ and
/lˠ/ as [l̪ˠ], and some have also merged /l̠ʲ/ and /lʲ/ as [lʲ]" — same for the nasals; and
"in parts of Munster, /n̠ʲ/ has merged with /ɲ/ in non-initial position"
[wiki-help-ipa-irish notes 5, 6]. The **four historical rhotics have merged to /ɾˠ ɾʲ/ in all
dialects** [wiki-irish-phonology §Fortis and lenis sonorants].
**[U]** Ní Chasaide reports Gaoth Dobhair reduced from four to a robust **three-way** lateral
contrast, and for nasals the palatalized alveolar tends to merge with /ɲ/ [nichasaide1999 p.113].
**Practical consequence for input:** hand transcriptions will use the **two-way** system
/l̪ˠ lʲ n̪ˠ nʲ/, matching *Lasairchos* /ˈl̪ˠɑsˠəɾʲxosˠ/. The tool should accept /lˠ l̠ʲ nˠ n̠ʲ/
as input aliases folding onto /l̪ˠ lʲ n̪ˠ nʲ/ (unattested — a tooling convenience, not a claim
about Irish).

### 1.2 Vowels

"Connacht and Munster at least agree in having the monophthongs /iː/, /ɪ/, /uː/, /ʊ/, /eː/,
/ɛ/, /oː/, /ɔ/, /aː/, /a/, and schwa (/ə/), which is found only in unstressed syllables; and
the diphthongs /əi/, /əu/, /iə/, and /uə/." "The vowels of Ulster Irish are more divergent and
are not discussed in this article." [wiki-irish-phonology §Vowels]

| | front | central | back |
|---|---|---|---|
| **long** | iː eː | aː | uː oː |
| **short** | ɪ ɛ | a | ʊ ɔ |
| **reduced** | | ə (unstressed only) | |
| **diphthongs** | iə uə əi əu | | |

- All four diphthongs have **falling sonority**; more precisely [iə̯ uə̯ əi̯ əu̯]
  [wiki-help-ipa-irish note 9].
- **[U]** /əi əu/ can be compressed to /eː oː/ [wiki-help-ipa-irish note 10].
- **/ə/ occurs only in unstressed syllables** [wiki-irish-phonology §Vowels] — so an Irish word
  never brings a stressed schwa to a target.
- Vowel **quality is heavily conditioned by flanking consonant quality**: e.g. /iː/ is front
  [iː] between two slender consonants, retracted [i̠ː] slender–broad, centralized [ïː] between
  two broad; /uː/ mirrors this; and schwa itself is [ɪ] next to a palatal, [ə] next to broad
  consonants, [ʊ̽] when the preceding syllable has /uː ʊ/
  [wiki-irish-phonology §Vowel backness]. **This is the single fact that makes the
  broad/slender decision in §8.1 partly recoverable from the vowels alone.**
- **[M] vs [C] on the open vowels:** in Munster /aː/ and /a/ have roughly the same
  front↔back range; in Connacht the allophones of short /a/ sit consistently further front
  than those of /aː/, and in Connemara /a/ is lengthened so that **only quality** separates
  /a/ from /aː/ [wiki-irish-phonology §Vowel backness].
- **Glide transitions.** Broad consonants take a velar offglide [ɰ] before front vowels
  (*naoi* [n̪ˠɰiː]), labialized to [w] after labials (*buí* [bˠwiː]); slender consonants take
  a palatal offglide [j] before back vowels (*tiubh* [tʲjuː]). In the other direction there is
  an onglide: [ə̯] before a broad consonant after a front vowel (*díol* [dʲiːə̯l̪ˠ]), [i̯]
  before a slender consonant after a back vowel (*áit* [aːi̯tʲ], *dúinn* [d̪ˠuːi̯n̠ʲ])
  [wiki-irish-phonology §On- and offglides]. **These glides are the natural raw material for a
  target that wants to render Cʲ as Cj / Ci — they are already phonetically present.**
- **Nasalized vowels** exist for some (usually older) speakers, from historical lenited /m/;
  "the contrast is not robust in any dialect"
  [wiki-irish-phonology §Nasalized vowels]. **Ignore for the tool.**

---

## 2. What Irish words bring to a target

This section is the donor's export list: the shapes, the clusters, and the internal epenthesis
that will already have applied before the target's rules see the word.

### 2.1 Syllable shapes

Irish onsets run C, CC and CCC; the codas run up to CC with a well-defined epenthesis escape
(§2.4). Worked shapes from attested transcriptions:

| Shape | Example |
|---|---|
| V | *ádh* /aː/ 'luck' [wiki-irish-orthography §Grapheme to phoneme correspondence] |
| CV | *bí*, *rí* /ɾˠiː/ 'king' [wiki-irish-orthography] |
| CVC | *mac* /mˠak/ 'son'; *bog* /bˠɔɡ/ 'soft' [wiki-irish-orthography] |
| CCV | *breá* /bʲɾʲaː/ 'fine'; *dlí* /dʲlʲiː/ 'law' [wiki-irish-phonology §Word-initial consonant clusters] |
| CCVC | *scéal* /ʃceːl̪ˠ/ 'story'; *bleán* /bʲlʲaːnˠ/ 'milking' [wiki-irish-phonology §Word-initial consonant clusters] |
| CCCV | *spraoi* /sˠpˠɾˠiː/ 'fun' [wiki-irish-phonology §Word-initial consonant clusters] |
| CCCVC | *splanc* /sˠpˠl̪ˠaŋk/ 'flash'; *stríoc* /ʃtʲɾʲiːk/ 'streak' [wiki-irish-phonology §Word-initial consonant clusters] |
| CVCC | *ceart* /caɾˠt̪ˠ/ 'right'; *beirt* /bʲɛɾˠtʲ/ 'two people' [wiki-irish-orthography; wiki-irish-phonology §Post-vocalic consonant clusters and epenthesis] |
| CVːCC | *ard* /aːɾˠd̪ˠ/ 'high'; *bord* /bˠoːɾˠd̪ˠ/ 'table' [wiki-irish-orthography] |
| CCVCC | *scuab* /sˠkuəbˠ/ 'broom'; *post* /pˠɔsˠt̪ˠ/ 'post' [wiki-irish-orthography] |
| CCCVCC | *splanc* /sˠpˠl̪ˠaŋk/ [wiki-irish-phonology §Word-initial consonant clusters] |

So the **maximal shape a donor word can present is roughly CCCVːCC** (unattested as an explicit
statement; assembled from the attested examples above — no source in this directory states an
Irish maximal syllable template as a formula).

Name-sized words are typically **one or two syllables with a heavy first syllable**, or two-to-
three syllables with the stress initial: *Seán* /ʃaːnˠ/ (CVːC), *Siobhán* /ˈʃʊwaːnˠ/
(CV.CVːC), *cailín* /ˈkalʲiːnʲ/ (CV.CVːC), *Diarmaid* /dʲiərmədʲ/ (CVː(diph)C.CVC)
[wiki-irish-orthography §Grapheme to phoneme correspondence]. Adjectival epithets in **-ach**
add a final /əx/ syllable: *taoiseach* /ˈt̪ˠiːʃəx/, *Gaelach* /ˈɡeːlˠəx/, *bacach* 'lame'
[wiki-irish-orthography; wiki-irish-phonology §Munster].

### 2.2 Word-initial clusters — the export inventory

**General rule:** "Irish words can begin with clusters of two or three consonants. In general,
all the consonants in a cluster agree in their quality, i.e. either all are broad or all are
slender." [wiki-irish-phonology §Word-initial consonant clusters]

**Two-consonant onsets, non-mutation environments.** Obstruent + liquid/nasal (but **labial
obstruents may not be followed by a nasal**), plus /sˠ ʃ/ + voiceless stop
[wiki-irish-phonology §Word-initial consonant clusters, from Ní Chiosáin 1999]. The Commons
grid states it as three products [wiki-clusterchart-nonmut]:

    C1 ∈ {pˠ bˠ fˠ d̪ˠ} / {pʲ bʲ fʲ dʲ}   +   C2 ∈ {l̪ˠ ɾˠ} / {lʲ ɾʲ}
    C1 ∈ {t̪ˠ k ɡ}      / {tʲ c ɟ}        +   C2 ∈ {l̪ˠ ɾˠ n̪ˠ} / {lʲ ɾʲ nʲ}
    C1 ∈ {sˠ}          / {ʃ}             +   C2 ∈ {pˠ t̪ˠ k mˠ l̪ˠ ɾˠ n̪ˠ} / {pʲ tʲ c mʲ lʲ ɾʲ nʲ}
    plus the single irregular cluster  mˠ + n̪ˠ

Attested examples: *bleán* /bʲlʲaːnˠ/, *breá* /bʲɾʲaː/, *cnaipe* /ˈkn̪ˠapʲə/ 'button',
*dlí* /dʲlʲiː/, *gnáth* /ɡn̪ˠaː/ 'usual', *pleidhce* /ˈpʲlʲəicə/, *slios* /ʃlʲɪsˠ/,
*sneachta* /ˈʃnʲaxt̪ˠə/ 'snow', *tlúth* /t̪ˠl̪ˠuː/ 'poker', *tnúth* /t̪ˠn̪ˠuː/,
*sparán* /ˈsˠpˠaɾˠaːn̪ˠ/, *scéal* /ʃceːl̪ˠ/, *mná* /mˠn̪ˠaː/ 'women'
[wiki-irish-phonology §Word-initial consonant clusters].

**Three-consonant onsets:** "/sˠ/ or /ʃ/ plus a voiceless stop plus a liquid."
*scliúchas* /ˈʃclʲuːxəsˠ/, *scread* /ʃcɾʲad̪ˠ/, *splanc* /sˠpˠl̪ˠaŋk/, *spraoi* /sˠpˠɾˠiː/,
*stríoc* /ʃtʲɾʲiːk/ [wiki-irish-phonology §Word-initial consonant clusters].

**The quality-agreement exception:** "broad /sˠ/ is found before slender labials (and for some
speakers in Connemara and Dingle before /c/ as well)": *sméara* /sˠmʲeːɾˠə/ 'berries',
*speal* /sˠpʲal/ 'scythe', *spleách* /sˠpʲlʲaːx/, *spreag* /sˠpʲɾʲaɡ/, and
*scéal* /sˠceːl̪ˠ/ ~ /ʃceːl̪ˠ/ [wiki-irish-phonology §Word-initial consonant clusters]. The
Commons grid marks exactly those cells [wiki-clusterchart-nonmut]. **So a donor word can
present a quality-mismatched onset /sˠpʲ/, /sˠmʲ/, /sˠc/ — a target that maps broad→X and
slender→Y will get a mixed cluster here.**

**[C]/[U] The /Cn/ → /Cɾ/ rule.** "In Donegal, Mayo, and Connemara dialects (but not usually on
the Aran Islands), the coronal nasals /nˠ, nʲ/ can follow only /sˠ, ʃ/ respectively in a
word-initial cluster. After other consonants, they are replaced by /ɾˠ, ɾʲ/":
*cnoc* /kɾˠʊk/ 'hill', *mná* /mˠɾˠaː/, *gnaoi* /ɡɾˠiː/, *tnúth* /t̪ˠɾˠuː/
[wiki-irish-phonology §Word-initial consonant clusters, from Ó Siadhail 1989].
**Because Connacht is our reference dialect, /kn ɡn tn mn/ mostly do NOT reach the targets —
they arrive as /kɾˠ ɡɾˠ t̪ˠɾˠ mˠɾˠ/.** This deletes one whole row from the target digests'
"Irish initial clusters the target bans" list. It is worth carrying both variants in the test
set (see `test-words.tsv`, *cnoc*).

**Mutation-environment onsets — the much larger set.** Because Irish mutates word-initially,
an inflected name or epithet can begin with clusters that are impossible in the citation form
[wiki-irish-phonology §Word-initial consonant clusters; wiki-clusterchart-mut2]:

*Lenition environment*

    {fˠ, w} / {fʲ, vʲ}   +   {l̪ˠ ɾˠ} / {lʲ ɾʲ}
    {h, x, ɣ} / {h, ç, j} +  {l̪ˠ ɾˠ n̪ˠ} / {lʲ ɾʲ nʲ}
    w + n̪ˠ

*Eclipsis environment*

    {bˠ mˠ w n̪ˠ} / {bʲ mʲ vʲ nʲ}  +  {l̪ˠ ɾˠ} / {lʲ ɾʲ}
    {d̪ˠ ɡ ŋ}   / {dʲ ɟ ɲ}         +  {l̪ˠ ɾˠ n̪ˠ} / {lʲ ɾʲ nʲ}

Attested: *bhlas* /wl̪ˠasˠ/, *bhris* /vʲɾʲɪʃ/, *chleacht* /çlʲaxt̪ˠ/, *chrom* /xɾˠɔmˠ/,
*ghreamaigh* /ˈjɾʲamˠə/, *ghníomhaigh* /ˈjnʲiːwə/, *shleamhnaigh* /hlʲəun̪ˠə/,
*shnámh* /hn̪ˠaːw/, *shroich* /hɾˠɪç/, *mbláth* /mˠl̪ˠaː/, *mbliana* /ˈmʲlʲiən̪ˠə/,
*ndlúth* /n̪ˠl̪ˠuː/, *ndroichead* /ˈn̪ˠɾˠɔhəd̪ˠ/, *ngléasfá* /ˈɲlʲeːsˠaː/,
*ngníomhófá* /ˈɲnʲiːwoːhaː/ [wiki-irish-phonology §Word-initial consonant clusters].

**These are the hard cases for every target**: /wl̪ˠ/, /ɣɾˠ/, /çl/, /xɾˠ/, /jn/, /hl/, /hn/,
/hɾ/, /ŋl/, /ɲn/ — onsets built on segments (/w ɣ ç x j h ŋ ɲ/) that most targets lack outright.
Whether the generator ever emits them is a **design decision, not a phonological fact**: if
epithets are generated in citation form only, the mutation onsets never arise; if the generator
produces *a Sheáin*, *na hÉireann*, *i gCiarraí* etc., they do. See §9.

### 2.3 Coda and medial clusters

Wikipedia gives no exhaustive final-cluster list [wiki-irish-phonology — not covered], but
**Green does**, and it is short and closed:

> "Syllable codas may consist of a single consonant, or of a cluster of nasal plus homorganic
> voiceless stop, or liquid plus obstruent (provided the obstruent is a voiceless stop or
> d(ʲ)), or sibilant plus voiceless stop, plus /xt/." [green1997 p.55]

Tabulated [green1997 p.56], in Green's notation (′ = slender):

    liquid + stop   rp r′p′  rt rt′  rk r′k′  rd rd′
                    lp l′p′  lt l′t′  lk l′k′  ld l′d′
    nasal + homorganic voiceless stop   mp m′p′  nt n′t′  ŋk ŋ′k′
    liquid + nasal  rn rn′
    sibilant + stop sp s′p′  st s′t′  sk s′k′
    /xt/            xt xt′

"Other underlying clusters are broken up by epenthesis" [green1997 p.55] — i.e. §2.4 is the
complement of this list, and **the two together fully determine which codas a donor word can
export.** Compare the attested codas in the harvest: /ɾˠt̪ˠ/ *ceart*, /ɾˠd̪ˠ/ *ard*,
/ɾˠn̪ˠ/ *dorn*, /ŋk/ *splanc*, /sˠt̪ˠ/ *post*, /ʃtʲ/ *ceist*, /xt̪ˠ/ *éisteacht* — all in
Green's list.

Other statements:

- **Post-vocalic clusters usually agree in quality**, with one exception: "broad /ɾˠ/, not
  slender /ɾʲ/, appears before the slender coronals /tʲ, dʲ, ʃ, nʲ, lʲ/" (Ó Sé 2000):
  *beirt* /bʲɛɾˠtʲ/, *ceird* /ceːɾˠdʲ/, *doirse* /ˈd̪ˠoːɾˠʃə/, *doirnín* /d̪ˠuːɾˠˈnʲiːnʲ/,
  *comhairle* /ˈkuːɾˠlʲə/ [wiki-irish-phonology §Post-vocalic consonant clusters and
  epenthesis]. **Second quality-mismatch case the targets will see.**
  (Note /ɾˠʃ/ and /ɾˠlʲ/ are not in Green's coda list — they are heterosyllabic there.)
- **Medial two-consonant clusters syllabify heterosyllabically (V.C₁C₂V)** *except* where the
  sonority rise from C₁ to C₂ is steep (stop+liquid, s+liquid), in which case C₁ is
  ambisyllabic: *achrann* [ˈaxrən] 'entanglement' (split) vs. *lasrach* [ˈlaʃrəx] 'flames',
  *ocras* [ˈokərəs] 'hunger' (C₁ ambisyllabic) [green1997 pp.144–146].
- **A single intervocalic consonant after a short stressed vowel is ambisyllabic**
  [green1997 pp.137–138]; not after an unstressed or a long vowel.
- **Irish has no gemination.** "Irish coda consonants are nonmoraic; ambisyllabic consonants
  are not phonetically lengthened — Irish has no gemination" [green1997 p.136]. So a target
  with contrastive gemination (Arabic) receives no geminates from the donor and must decide
  whether to create any. The orthographic ⟨ll nn rr⟩ are **not** geminates: they are the
  historical fortis sonorants, and in modern Irish they surface as vowel lengthening on the
  preceding vowel (§4.2).
- **Hiatus: not covered** by any source here as a phonotactic statement.

Green's own **onset**-cluster table [green1997 pp.55–56] largely matches §2.2 but adds the
lenition-only and nasalization-only series (/vl vr xn ɣn ŋl/ etc.) and notes one explicit
exclusion: **/ʃɾʲ/ is disallowed in Modern Irish** (historical /ʃRʲ/ → /sˠɾˠ/)
[green1997 p.56]. Green also states a **prosodic licensing** restriction that bears directly
on the export list: in Connacht/Ulster, only stop+liquid and s+liquid are licensed as onsets
**syllable-internally**; noncoronal-fricative+liquid and obstruent+nasal are permitted
**word-initially but not word-internally** (they split, hence *achrann*). **[M]** In Munster
no cluster at all is licensed at a plain syllable edge and only stop+liquid at a foot edge —
everything else epenthesizes [green1997 pp.144–149].

### 2.4 Irish's own epenthesis — applied before the target ever sees the word

This is the most consequential §2 fact for the tool, because it means Irish **does not export**
most of its sonorant+labial/dorsal codas: it has already broken them with a schwa.

**Rule** [wiki-irish-phonology §Post-vocalic consonant clusters and epenthesis, from Ní Chiosáin
1999]:

    ∅ → ə / {ɾˠ ɾʲ l̪ˠ lʲ n̪ˠ nʲ} _ C[labial or dorsal, except the voiceless stops pˠ pʲ k c]

The Commons grid states it as [wiki-clusterchart-epenthesis]:

    {l̪ˠ ɾˠ} / {lʲ ɾʲ}  +  {bˠ ɡ fˠ w mˠ} / {bʲ ɟ fʲ vʲ mʲ}
    {n̪ˠ}   / {nʲ}      +  {bˠ fˠ w mˠ}   / {bʲ fʲ vʲ mʲ}

Attested outputs: *borb* /ˈbˠɔɾˠəbˠ/, *gorm* /ˈɡɔɾˠəmˠ/ 'blue', *dearmad* /ˈdʲaɾˠəmˠəd̪ˠ/,
*dearfa* /ˈdʲaɾˠəfˠə/, *seirbhís* /ˈʃɛɾʲəvʲiːʃ/, *fearg* /ˈfʲaɾˠəɡ/ 'anger',
*dorcha* /ˈd̪ˠɔɾˠəxə/ 'dark', *dalba* /ˈd̪ˠal̪ˠəbˠə/, *colm* /ˈkɔl̪ˠəmˠ/ 'dove',
*soilbhir* /ˈsˠɪlʲəvʲəɾʲ/, *gealbhan* /ˈɟal̪ˠəwən̪ˠ/ 'sparrow', *binb* /ˈbʲɪnʲəbʲ/,
*Banbha* /ˈbˠan̪ˠəwə/, *ainm* /ˈanʲəmʲ/ 'name', *meanma* /ˈmʲan̪ˠəmˠə/,
*ainmhí* /ˈanʲəvʲiː/ [wiki-irish-phonology §Post-vocalic consonant clusters and epenthesis].

**Blocking conditions:**
1. **No epenthesis if the preceding vowel is long or a diphthong**: *fáirbre* /ˈfˠaːɾʲbʲɾʲə/,
   *téarma* /ˈtʲeːɾˠmˠə/, *léargas* /ˈlʲeːɾˠɡəsˠ/, *dualgas* /ˈd̪ˠuəl̪ˠɡəsˠ/
   [wiki-irish-phonology §Post-vocalic consonant clusters and epenthesis].
2. **No epenthesis in words of ≥3 syllables**: *firmimint* /ˈfʲɪɾʲmʲəmʲənʲtʲ/,
   *smiolgadán* /ˈsˠmʲɔl̪ˠɡəd̪ˠaːn̪ˠ/, *caisearbhán* /ˈkaʃəɾˠwaːn̪ˠ/,
   *Cairmilíteach* /ˈkaɾʲmʲəlʲiːtʲəx/ [ibid.].
3. **[wiki-irish-orthography adds] No epenthesis across a morpheme boundary** — after prefixes
   and inside compounds: *garmhac* /ˈɡaɾˠwak/ 'grandson' (gar- + mac), *an-chiúin* /ˈan̪ˠçuːnʲ/,
   *carrbhealach* /ˈkaːɾˠvʲalˠəx/ [wiki-irish-orthography §Epenthesis]. **This directly affects
   compound epithets** of the *Lasairchos* type — a compound boundary suppresses the schwa.

**Green states the same rule more generally**, in sonority terms, and adds a fourth blocker:

> an epenthetic /ə/ breaks up **falling-sonority** clusters (C₁ more sonorant than C₂) where C₂
> is neither a voiceless stop nor **homorganic with C₁** [green1997 p.152]

with examples /sʲalv/ → [ʃaləv] 'possession', /gorm/ → [gorəm] 'blue', /dʲarg/ → [dʲarəg] 'red'
[green1997 p.152]. His blocking conditions:
1. **long vowel or diphthong before the cluster** — *téarma* not *téarəma*, *dualgas* not
   *dualəgas* [green1997 p.152];
2. **homorganic C₁C₂** — *gaimbín* [gamʲbʲiːnʲ] not *gamʲəbʲiːnʲ; *teanga* [tʲaŋgə] not
   *tʲaŋəgə [green1997 p.154]. **This is the source of Wikipedia's "⟨ng⟩ is the main
   exception"** and it is a cleaner statement of it: /mˠbˠ mʲbʲ ŋɡ ɲɟ/ never epenthesize.
3. **C₂ is a voiceless stop** — *cearc* [kʲark] 'hen', not *kʲarək [green1997 p.153];
4. **≥3-syllable words — but only in Connacht.** "No epenthesis in Connemara (*barbarach*
   [barbərəx]), but Déise (Munster) and Tory (Ulster) *do* have it (*barabarach*
   [barəbərəxt])" [green1997 pp.152–153].

**CONFLICT resolved by Green.** The two Wikipedia articles state the rule with different
conditions:
- [wiki-irish-phonology §Post-vocalic consonant clusters and epenthesis] gives long
  vowel/diphthong and ≥3 syllables as the blockers, and says nothing about morpheme boundaries.
- [wiki-irish-orthography §Epenthesis] gives long vowel/diphthong and morpheme boundary, and no
  syllable-count condition; this section carries a Wikipedia "does not cite any sources" banner.
Green supplies both plus homorganicity, and shows the **syllable-count blocker is
dialect-specific — it holds in Connacht, which is our reference dialect** [green1997 pp.152–153].
So for the tool: apply all four blockers (long vowel/diphthong, homorganic, voiceless stop C₂,
≥3 syllables) plus the morpheme boundary, and note that a Munster or Ulster reading would drop
the syllable-count one.

**[M]** Munster epenthesizes *more* in two further ways: (a) across morpheme boundaries, when
⟨l n r⟩ **follow** ⟨b bh ch g mh⟩ (after any vowel) or ⟨th⟩ (after short vowels), and when ⟨n⟩
follows ⟨c g m r⟩ [wiki-irish-orthography §Epenthesis]; (b) into **rising**-sonority clusters
that are not prosodically licensed at their level — *eagla* → [agələ] 'fear', *ocras* →
[okərəs] 'hunger', *aigne* → [agʲənʲə] 'mind' [green1997 p.149]. **A Munster reading therefore
delivers noticeably more syllables to the target than a Connacht one.**

Quiggin describes the same phenomenon for Ulster 1906 as "svarabhakti", inserted into l+b, l+g,
l+m, l+bh, r+g, r+m etc. and explicitly **not** into l+p (*alp* stays /alp/), which matches the
voiceless-stop exclusion [quiggin1906 §111, §138ff].

**The epenthetic schwa is a near-neutralization.** McCullough measures epenthetic schwa as
~10 ms shorter than underlying schwa (0.059 s vs 0.069 s, p<0.029), but with **no significant
difference in formant frequencies** (F1 ≈ 550/535 Hz, F2 ≈ 1680/1729 Hz) — quality is
neutralized, duration is not [irish-schwa-kwpl §5.1–5.2]. A sonority-based prediction that
epenthetic vowels in closer-sonority sequences would be longer was **not confirmed**
[irish-schwa-kwpl §5.3]. No confirmed dialect difference: the single Connemara speaker was a
statistical outlier, which the paper attributes to a methodological artifact (one reading
rather than two) rather than to dialect [irish-schwa-kwpl §5, §5.1].
**For the tool this is a non-issue at input** — both come out as /ə/ in the IPA string — but see
§9.6 on whether the tool should be told which is which. The paper's **15 near-minimal pairs**
(underlying vs. epenthetic schwa: *anam*/*ainm*, *talamh*/*sealbh*, *cothrom*/*gorm*,
*léirigh*/*dearg*, *gaineamh*/*banbh*, …) [irish-schwa-kwpl p.5] are a ready-made discriminating
sub-suite and several are in `test-words.tsv`.

---

## 3. What alternations the source side produces

Irish inflects names and epithets by changing the **initial** consonant (mutation) and by
changing the **final** consonant's quality or adding an ending (genitive/vocative). The tool
needs these because an epithet is a grammatical construction, not a bare stem.

### 3.1 Lenition (séimhiú) as a phoneme→phoneme table

[wiki-irish-mutations §Summary table]

| Radical (broad) | → | Radical (slender) | → | Spelling |
|---|---|---|---|---|
| pˠ | fˠ | pʲ | fʲ | p → ph |
| bˠ | **w** | bʲ | vʲ | b → bh |
| mˠ | **w** | mʲ | vʲ | m → mh |
| fˠ | **∅** | fʲ | **∅** | f → fh (silent) |
| t̪ˠ | **h** | tʲ | **h** | t → th |
| d̪ˠ | **ɣ** | dʲ | **j** | d → dh |
| sˠ | **h** | ʃ | **h** | s → sh |
| k | **x** | c | **ç** | c → ch |
| ɡ | **ɣ** | ɟ | **j** | g → gh |
| l̪ˠ | lˠ | l̠ʲ | lʲ | l (unwritten; fortis→lenis) |
| n̪ˠ | nˠ | n̠ʲ | nʲ | n (unwritten; fortis→lenis) |

- **Vowels and /ɾ/ do not lenite**; ⟨r⟩ has no entry in the table
  [wiki-irish-mutations §Summary table].
- The l/n rows are the fortis→lenis alternation, footnoted "Not all dialects contrast lenited
  ⟨l⟩ and ⟨n⟩ from their unlenited forms" [wiki-irish-mutations §Summary table]. **For a
  two-way-L/N Connacht transcription these two rows are null.**
- **The four lenition outputs that are the real problem for targets: /w/, /ɣ/, /h/, /x ç j/.**
  All four are §8 items.
- After the definite article, lenition of ⟨s⟩ is **replaced by t-prefixation**: *an tsolais*
  /ə(n̪ˠ) ˈt̪ˠɔlˠəʃ/, *an tSín* /ə(nʲ) tʲiːnʲ/
  [wiki-irish-orthography §Grapheme to phoneme correspondence;
  wiki-irish-mutations §Environments of lenition].
- **[C]/[U]** in the /Cn/→/Cɾ/ dialects, lenited /sˠn̪ˠ ʃnʲ/ → /hn̪ˠ hnʲ/ as expected, but after
  the article they become /t̪ˠɾˠ tʲɾʲ/: *sneachta* /ʃnʲaxt̪ˠə/ → *shneachta* /hnʲaxt̪ˠə/ →
  *an tsneachta* /ə tʲɾʲaxt̪ˠə/ [wiki-irish-phonology §Word-initial consonant clusters].

**CONFLICT:** [wiki-irish-mutations §Summary table] gives the lenition of ⟨bh mh⟩ as **/w/**
(broad) with no dialect split, and of ⟨dh gh⟩ as **/ɣ/** with no split. But
[wiki-irish-phonology §Allophones] states that broad /w/ is realized only as **[vˠ]** in
Munster, only as **[w]** in Ulster, and as **[w]** initially / **[vˠ]** elsewhere in Connacht.
Take the phonology article's dialect statement as the finer-grained one; the mutations table is
phonemic.

### 3.2 Eclipsis (urú) as a phoneme→phoneme table

[wiki-irish-mutations §Summary table]

| Radical (broad) | → | Radical (slender) | → | Spelling |
|---|---|---|---|---|
| pˠ | bˠ | pʲ | bʲ | p → bp |
| t̪ˠ | d̪ˠ | tʲ | dʲ | t → dt |
| k | ɡ | c | ɟ | c → gc |
| bˠ | mˠ | bʲ | mʲ | b → mb |
| d̪ˠ | n̪ˠ | dʲ | n̠ʲ | d → nd |
| ɡ | **ŋ** | ɟ | **ɲ** | g → ng |
| fˠ | **w** | fʲ | vʲ | f → bhf |
| (vowel) | n̪ˠV | (vowel) | n̠ʲV | V → n-V |

/s l m n r h/ have no eclipsis entry [wiki-irish-mutations §Summary table].

Attested: *gcáis* /ɡaːʃ/, *gceist* /ɟɛʃtʲ/, *mbéal* /mʲeːlˠ/, *ndorn* /n̪ˠoːɾˠn̪ˠ/,
*ngasúr* /ˈŋasˠuːɾˠ/, *ngeata* /ˈɲat̪ˠə/, *bhfíon* /vʲiːnˠ/, *bhfuinneog* /ˈwɪn̠ʲoːɡ/,
*bpoll* /bˠoːl̪ˠ/, *bpríosún* /ˈbʲɾʲiːsˠuːnˠ/, *dtír* /dʲiːɾʲ/, *dtaisce* /ˈd̪ˠaʃcə/
[wiki-irish-orthography §Grapheme to phoneme correspondence].

**The eclipsis outputs that matter for targets: word-initial /ŋ/ and /ɲ/** (both §8 items), and
initial /n̪ˠ/ before a vowel.

### 3.3 The other initial changes

[wiki-irish-mutations §Changes to vowel-initial words]

| Change | Environment | Output |
|---|---|---|
| **t-prothesis** | masc. sg. nom. vowel-initial noun after the article | /t̪ˠV/ (broad), /tʲV/ (slender): *an t-uisce*, *t-éan* /tʲeːnˠ/ |
| **h-prothesis** | after a proclitic that ends in a vowel and causes neither lenition nor eclipsis | /hV/: *a haois* 'her age', *go hÉirinn*, *le hAntaine*, *na hoíche*, *na héin*, *go hálainn* |
| **n-prothesis** | eclipsis of a vowel-initial word | /n̪ˠV/ or /n̠ʲV/: *a n-aois* 'their age' |

Minimal triple: *a aois* 'his age' (no change) / *a haois* 'her age' / *a n-aois* 'their age'
[wiki-irish-mutations §Changes to vowel-initial words].

### 3.4 Triggers that matter for names and epithets

[wiki-irish-mutations §Environments of lenition, §Environments of eclipsis;
wiki-irish-declension §Articles; wiki-irish-name §Ó and Mac surnames]

**Lenition:**
- Vocative particle **a**: *a Bhríd*, *a Sheáin*, *a chairde* — attested *a Sheáin* [ə çaːnʲ]
  [wiki-irish-phonology §Vowel backness].
- Article *an* + **feminine** noun, nom. sg. (*an bhean*); article *an* + **masculine** noun,
  **gen.** sg. (*an fhir*). Blocked when a coronal follows *an* (*an deoch*, *an tí*), where
  ⟨s⟩ instead goes to ⟨ts⟩.
- Possessives *mo*, *do*, *a* 'his'.
- Attributive **adjective after a feminine singular noun**, after a plural noun ending in a
  slender consonant, and after a masculine singular noun in the genitive.
- **Preposed adjectives / prefixes in compounds**: *sean-*, *droch-*, *dea-*, *nua-*,
  *tréan-*, *fíor-*, *ard-*, *óg-* → *seanbhean*, *drochdhuine*, *ardbhrú*, *ógfhear*.
- The **second element of some compounds**: *ainmfhocal*, *dúghorm*, *státfhiach*.
- Surname particles **Ní, Nic, Uí, Mhic, Bean Uí, Bean Mhic** lenite the following name —
  *except* Nic/Mhic before ⟨c⟩ or ⟨g⟩ [wiki-irish-name §Ó and Mac surnames].
- Numerals *aon, an chéad, dhá, beirt, trí, ceithre, cúig, sé* + singular noun.

**Eclipsis:**
- Plural possessives *ár, bhur, a* 'their'.
- Preposition *i* 'in': *i dteach*.
- **Genitive plural after the article** *na*: *na n-asal*, *na bhfocal*.
- Numerals *seacht, ocht, naoi, deich* + singular noun.

**Name-particle system** [wiki-irish-name §Ó and Mac surnames]:

| Base | Man | Wife | Daughter | Mutation on following name |
|---|---|---|---|---|
| Ó 'descendant' | Ó / gen.-voc. Uí | (Bean) Uí | Ní | Uí, Ní lenite; Ó + vowel takes **h-** (*Ó hUiginn*) |
| Mac 'son' | Mac / Mhic | (Bean) Mhic | Nic | lenite, except Nic/Mhic before ⟨c g⟩ |
| Mag (before vowel or silent ⟨fh⟩+vowel) | Mag / Mhig | (Bean) Mhig | Nig | as Mac |
| de (Norman) | de | — | — | none stated |

**[U]** In Ulster a married woman commonly just uses *Ní* or *Nic*
[wiki-irish-name §Ó and Mac surnames].

### 3.5 Genitive and vocative — the endings a name actually takes

[wiki-irish-declension §Declension, §Vocative]

| Decl. | Gen. sg. formation | Example |
|---|---|---|
| 1 (masc.) | final broad consonant → **slender** | *bád* → *báid*; *fear* → *fir*; *mac* → *mic* /mˠak/ → /mʲɪc/; *marcach* → *marcaigh* (/x/ → /j/, spelled -(a)igh) |
| 2 (mostly fem.) | slenderize + **-e** | *bróg* → *bróige*; *deoir* → *deoire*; *girseach* → *girsí* (/x/ → /iː/, spelled -(a)í) |
| 3 | broaden + **-a** | *bádóir* → *bádóra*; *rás* → *rása*; *canúint* → *canúna*; *bagairt* → *bagartha* |
| 4 | **no change** (stems in a vowel or -ín) | *balla*, *cailín* unchanged |
| 5 (mostly fem.) | **add a broad consonant** | *pearsa* → *pearsan*; *cathair* → *cathrach*; or broaden the final consonant: *athair* → *athar*, *máthair* → *máthar* |

**Vocative:** always preceded by particle *a*, which lenites (and is silent before a vowel).
"The first declension is the only declension in which the vocative is distinct from the
nominative" — masculine 1st-declension vocative sg. takes the **slenderized (genitive) stem**:
*mac* → *a mhic*, *Seán* → *a Sheáin* /ə çaːnʲ/
[wiki-irish-declension §Vocative; wiki-irish-phonology §Vowel backness].

**The two phonological effects that matter to a target:**
1. **Slenderization** — the final consonant flips quality: /mˠak/ → /mʲɪc/ changes *both* the
   final consonant's quality *and* the vowel (§1.2). A target that neutralizes the broad/slender
   contrast (§8.1) will **lose the genitive/vocative distinction entirely** unless the vowel
   change carries it.
2. **Lenition of the initial** — /ʃaːnˠ/ → /çaːnʲ/. A target lacking /ç/ (§8) must decide what
   the vocative of a name even sounds like.

### 3.6 Adjective agreement, and compounding for epithets

[wiki-irish-declension §Adjectives]

- Predicate adjectives **do not inflect**; attributive adjectives **follow the noun** and
  inflect for gender/case/number in four classes mirroring noun declensions 1–4.
  1st-decl. adj. *bocht*: masc. gen. *bhoicht* (slenderized), fem. nom. *bhocht* (lenited),
  fem. gen. *boichte* (slender + -e). 3rd-decl. (-úil) fem. gen. *misniúla* (broad + -a).
  4th-decl. *crua* does not inflect but does lenite.
- Nominative plural adjective lenites **only if the noun ends in a slender consonant**:
  *cait bhacacha* vs. *táilliúirí bacacha*.
- **Compounding:** the sources here state compound-lenition for **prefix/preposed-adjective +
  noun** (*seanbhean*, *drochdhuine*, *ardbhrú*, *fíorchneas*) and for the second element of
  some fixed compounds (*ainmfhocal*, *dúghorm*) [wiki-irish-mutations §After preposed
  adjectives, §After most prefixes, §The second part of a compound]. A vowel-initial second
  element is unchanged: *seanathair* [wiki-irish-mutations §Changes to vowel-initial words].
  **Noun + noun compounding (the *Lasairchos* = lasair 'flame' + cos 'foot' type) is not
  covered by any source in this directory** — no rule is given for whether the second noun
  lenites. The user's own transcription /ˈl̪ˠɑsˠəɾʲxosˠ/ shows *cos* /kosˠ/ appearing as
  /xosˠ/, i.e. **lenited**, and stress on the first element only. That is consistent with the
  prefix pattern; treat it as the working rule (unattested for noun+noun specifically).
- **Epithet slots** [wiki-irish-name §Epithets]: *Mór* 'big' and *Óg* 'young' (and *Beag*)
  sit **between** given name and surname — *Seán Óg Ó Súilleabháin*. Colour epithets follow the
  name: *Pádraig Rua* 'red-haired Patrick', *Máire Bhán* 'fair-haired Mary' (note *Bhán*
  lenited after a feminine name; *Rua* unlenited after a masculine one).
- **Traditional Gaeltacht patronymic chain**: given name + father's name (gen.) + grandfather's
  name (gen.), both lenited: *Seán Phóil Shéamuis* [wiki-irish-name §Traditional Gaeltacht names].

---

## 4. Stress and length

### 4.1 Stress

- **[C] and [U] — initial stress.** "Outside of Munster this is usually the first syllable of
  the word": *d'imigh* /ˈdʲɪmʲiː/, *easonóir* /ˈasˠən̪ˠoːɾʲ/
  [wiki-irish-phonology §Stress, from de Búrca 1958]. Ní Chasaide, for Ulster: "Primary lexical
  stress is located on the first syllable of most words" [nichasaide1999 p.115].
  **This matches the user's transcriptions** — /ˈkɪə.ɾˠə/, /ˈmˠat̪ˠɑːnˠəx/, /ˈl̪ˠɑsˠəɾʲxosˠ/ —
  and is the default the tool should assume.
  Exceptions: "certain words, especially adverbs and loanwords, have stress on a noninitial
  syllable": *amháin* /əˈwaːnʲ/, *tobac* /təˈbak/ [wiki-irish-phonology §Stress].
- **[M] — weight-attracted stress.** "Stress is attracted to a long vowel or diphthong in the
  second or third syllable of a word": *cailín* /kaˈlʲiːnʲ/, *achainí* /axəˈnʲiː/ (Ó Sé 2000).
  Green's fuller statement: **stress σ2 if heavy; else the leftmost heavy syllable within a
  three-syllable window; else σ1** [green1997 p.123] — *cearchán* [kərˈkaːn], *bóthar*
  [ˈboːhər], *údarás* [ˈuːdəraːs], *asal* [ˈasəl]; and in 4–5-syllable words only σ1–σ3 count,
  so *pataileachán* keeps initial stress [green1997 p.125]. Kukhto gives the same rule as
  "σ2 if heavy, else σ3 if heavy and σ2 light, else σ1" [kukhto2019 p.1565].
  Additionally stress is attracted to **/a/ in the second syllable when followed by /x/**,
  provided the first (and third) syllables have short vowels: *bacach* /bˠəˈkax/ 'lame',
  *slisneacha* /ʃlʲəˈʃnʲaxə/; but if the first or third syllable has a long vowel or diphthong,
  stress goes there and the /a/ before /x/ reduces to /ə/: *éisteacht* /ˈeːʃtʲəxt̪ˠ/,
  *moltachán* /ˌmˠɔl̪ˠhəˈxaːn̪ˠ/ (Ó Cuív 1944) [wiki-irish-phonology §Munster].
  **This is exactly the *-ach* epithet class** (*Matánach*), so the Munster/non-Munster choice
  visibly changes the shape of every *-ach* epithet: **[C]** /ˈmˠat̪ˠɑːnˠəx/ vs. a Munster
  reading that would place the accent on the long ⟨á⟩.
  Green sharpens the *-ach* fact: adjectival **-ach** attracts stress when all other syllables
  are light (*beannacht* [bʲəˈnaxt], *bacacha* [bəˈkaxə]) but not when unfooted (*fásach*
  [ˈfaːsəx]); the **nominalizing -acht** '-ness' **never** attracts it, giving the near-minimal
  pair *aiteach* [əˈtʲax] 'strange' vs. *aitheacht* [ˈatʲəxt] 'strangeness'
  [green-munster pp.4–5].
  **CONFLICT on why.** Green posits *both* an underlying schwa in σ1 *and* special prosodic
  prominence for /ax/ in σ2 [green1997; green-munster]. Kukhto argues the /ax/-prominence
  mechanism is unnecessary and that the underlying-schwa account alone suffices, citing
  *macalla* [maˈkalə] 'echo', which resists reduction without containing /ax/
  [kukhto2019 pp.1566–1568]. **Empirically both predict the same surface stress for *-ach*
  epithets**, so the tool need not choose; the conflict is about mechanism.
  **CONFLICT on the three-syllable window.** Green's Munster rule depends on it, but Green's
  own earlier paper reports Gussmann (1995) finding 4th-syllable stress, "thereby disproving
  the hypothesis of the three-syllable 'stress window'" [green-munster p.3], and Rowicka's
  independent account also predicts non-window patterns [rowicka pp.7–8]. The three sources
  disagree three ways on the stress of *imigéiniúla* 'distant (pl.)': penultimate
  (Gussmann, Rowicka [rowicka pp.7–8]) vs. antepenultimate (Green, citing Ó Sé p.c., who calls
  Gussmann's citation unreliable [green1997 p.125 fn.18]). Rowicka further disputes the
  framing that initial stress is the Munster default at all, arguing primary stress is
  "preferably non-initial" [rowicka p.6]. **Only relevant if the user ever switches the
  reference dialect to Munster.**
- **Compound stress — four patterns** [wiki-irish-phonology §Compound words, from Ó Liatháin et
  al. 1998]:
  1. Most compounds: primary on first member, secondary on second —
     *lagphortach* /ˈl̪ˠaɡˌfˠɔɾˠt̪ˠəx/.
  2. *do-, so-, in-*: secondary on the prefix, **primary on the following element** —
     *dothuigthe* /ˌdˠoˈhɪkʲə/.
  3. *an-* (intensive), *bith-* 'perpetual', *colg-, comh-, dian-, glan-, gnáth-, lán-,
     príomh-*: **two primaries** — *an-mhaith* /ˈanˈwa/.
  4. *ard-, dearg-, droch-, fíor-, iar-, ró-, síor-*: mixed — *Fíor-Dhia* /ˈfʲiːɾˠˈjiːə/ vs.
     *fíoruisce* /ˈfʲiːɾˠˌɪʃcə/; *droch-dhuine* /ˈd̪ˠɾˠɔxˈɣinʲə/ vs.
     *drochbhéasach* /ˈd̪ˠɾˠɔxˌvʲeːsəx/; *Ard-Easpag* /ˈaːɾˠd̪ˠˈæsˠpˠəɡ/ vs.
     *ardnósach* /ˈaːɾˠd̪ˠˌn̪ˠõːsəx/.
  **Compound epithets are pattern 1 by default: `ˈσ … ˌσ`.**
- **Secondary stress** is "usually found only in compounds" [wiki-help-ipa-irish §Suprasegmentals].

### 4.2 Length

- **Vowel length is phonemic** — the five long/short pairs of §1.2. Length is written with the
  *síneadh fada* ⟨á é í ó ú⟩ and by vowel digraphs [wiki-irish-orthography §Vowels].
- **Only long vowels and diphthongs are heavy; coda consonants do not contribute weight.**
  "Only syllables containing a long vowel or a diphthong count as heavy. Consonants in the coda
  do not contribute to syllable weight" [rowicka p.2]; "recall that CVC syllables are light"
  [green1997 p.121], and Modern Irish differs from **Old Irish** here, where CVC *was* heavy —
  the evidence being the absence of compensatory lengthening in forms like *fúl*, *brígh*
  [green1997 pp.72–73]. **This is a real Old-Irish/Modern-Irish difference that §10 has to
  carry.**
- **Unstressed long vowels behave differently by dialect** [green1997 pp.76, 94]:
  **[U]** Ulster (and Scottish Gaelic) categorically **shortens** unstressed long vowels —
  *cailín* [ˈkalʲinʲ] < [ˈkalʲiːnʲ], *galún* [ˈgalun] 'gallon'. **[M]** Munster instead
  **shifts stress onto** the heavy syllable rather than shortening it. **[C]** Connacht does
  neither and tolerates the mismatch — so a Connacht donor word **keeps its unstressed long
  vowels**, which is what the user's *Matánach* /ˈmˠat̪ˠɑːnˠəx/ shows. Ulster also has an
  irregular, lexically variable *trochaic shortening* of a stressed heavy initial syllable
  before an unstressed light one, but only 6 of 52 eligible LASID forms show it
  [green1997 p.77].
- **Lengthening/diphthongization before "fortis" sonorants** — the reflexes of Old Irish fortis
  sonorants in syllable-final position lengthen or diphthongize the preceding vowel
  [wiki-irish-phonology §Lengthening before fortis sonorants]:
  - **[U] (Donegal/Mayo):** only before ⟨rd rl rn⟩, before ⟨rr⟩ (unless a vowel follows), and in
    a few words before final ⟨ll⟩: *barr* /bˠaːɾˠ/, *ard* /aːɾˠd̪ˠ/, *orlach* /ˈoːɾˠl̪ˠax/,
    *tuirne* /ˈt̪uːɾˠn̠ʲə/, *thall* /haːl̪ˠ/.
  - **[C] (Connemara, Aran) and [M]:** additionally before ⟨nn⟩ (unless a vowel follows) and
    before word-final ⟨m ng⟩: *poll* → /pˠəul̪ˠ/; *greim* → /ɟɾʲiːmʲ/ in Connemara/Aran vs.
    /ɟɾʲəimʲ/ in Munster.
  - Generally no lengthening when the sonorant is followed by a vowel, producing alternations:
    Dingle *ceann* /cəun̪ˠ/ ~ gen. *cinn* /ciːnʲ/ ~ pl. *ceanna* /ˈcan̪ˠə/.
  **Consequence for the tool:** *ceann* 'head' is /caːn̪ˠ/ in the standard-ish transcription
  [wiki-irish-orthography], /can̪ˠ/ elsewhere [wiki-irish-phonology §Sandhi], /cəun̪ˠ/ in
  Dingle. The donor's vowel length is therefore **partly a dialect choice, not a fixed fact**,
  in exactly the ⟨ll nn rr rd rl rn m ng⟩ environments. Fix the dialect once and stay there.
- **Devoicing:** "Where a voiced obstruent or /w/ comes into contact with /h/, the /h/ is
  absorbed into the other sound, which then becomes voiceless (in the case of /w/, devoicing is
  to /fˠ/)": *scuab* /sˠkuəbˠ/ → *scuabfaidh* /ˈsˠkuəpˠəɟ/, *scuabtha* /ˈsˠkuəpˠə/
  [wiki-irish-phonology §Devoicing, from Breatnach 1947]. Mostly a verb-morphology fact; it
  reaches names only through verbal adjectives used as epithets.

---

## 5. Reading Irish orthography (input side), and what it offers the output side

The tool's inputs are **hand-transcribed IPA**, so orthography matters here only for (a)
checking a hand transcription, and (b) the fact that the *targets'* romanizations are being
designed to sit beside Irish-looking names.

### 5.1 The quality rule

"**caol le caol agus leathan le leathan**" ('slender with slender and broad with broad'): "the
vowels on either side of any consonant (or consonant cluster) must be both slender (⟨e, é, i,
í⟩) or both broad (⟨a, á, o, ó, u, ú⟩), to unambiguously determine if the consonant(s) are
broad or slender. An apparent exception is ⟨ae⟩, which is followed by a broad consonant despite
the ⟨e⟩." [wiki-irish-orthography §Vowels]

So in Irish spelling, **⟨e i⟩ flanking a consonant letter = slender; ⟨a o u⟩ = broad**, and many
written vowel letters are purely diacritic — they mark the consonant, not a vowel sound. This is
why *Siobhán* is /ˈʃʊwaːnˠ/ (the ⟨io⟩ writes /ʊ/ after a slender /ʃ/) and *Seán* is /ʃaːnˠ/
(the ⟨e⟩ writes nothing but the slenderness of ⟨s⟩)
[wiki-irish-orthography §Grapheme to phoneme correspondence].

### 5.2 Alphabet and loan letters

The traditional alphabet is 18 letters ⟨a b c d e f g h i l m n o p r s t u⟩; ⟨j k q v w x y z⟩
"are used in scientific terminology and modern loanwords". ⟨v⟩ occurs in a few mainly
onomatopoeic native words (*vácarnach* 'to quack', *vrác* 'caw') and colloquialisms.
⟨h⟩, when not a lenition mark or a prothesis, occurs word-initially in loanwords (*hata* 'hat').
⟨k⟩ is replaced by ⟨c⟩ in integrated loans (*karate* → *cearáité*). ⟨j⟩ represents [dʒ], "a
non-native phoneme", and is substituted by /ʃ/ in integrated loans (*Seapáin* /ˈʃapˠaːnʲ/)
[wiki-irish-orthography §Letters and letter names].

**Implication for the output romanizations:** an Irish-flavoured romanization should avoid
⟨j k q v w x y z⟩ if it is meant to look Gaelic; conversely, a target romanization that *uses*
them (Georgian's strand-4 names *Xelxyx*, *Th'tysh* do) will read as visibly non-Irish, which is
the point for strand 4 [see `../../notes/project-goals.md`].

### 5.3 Mutation and eclipsis spellings

Lenition is written by adding ⟨h⟩: ⟨bh ch dh fh gh mh ph sh th⟩ (in Gaelic type, a dot ⟨ċ⟩)
[wiki-irish-orthography §Alphabet]. Eclipsis is written by **prefixing** the new sound and
keeping the old letter: ⟨mb ɡc nd bhf ng bp dt⟩ and ⟨n-⟩ before a vowel
[wiki-irish-mutations §Summary table]. So an eclipsed word's spelling still shows its radical —
useful if the generator ever needs to recover a stem from spelling.

### 5.4 The síneadh fada, and the epenthetic vowel

⟨á é í ó ú⟩ mark **long** vowels; accented letters sort as variants of the unaccented letter
[wiki-irish-orthography §Letters and letter names]. The **epenthetic /ə/ of §2.4 is unwritten**
[wiki-irish-orthography §Epenthesis] — so *gorm* has two syllables in speech and one vowel
letter in spelling. A hand transcription must supply it; a romanizer that wants to look Irish
may want to omit it.

---

## 6. Morphology usable for epithets

Ten productive patterns, source-side, that the generator can build an epithet from.

| # | Form | Function | Attachment | Example |
|---|---|---|---|---|
| 1 | **-ach / -each** (adj., /əx/) | 'characterized by', ethnonym/adjective from noun | to a noun stem | *Gaelach* /ˈɡeːlˠəx/ 'Gaelic'; *bacach* 'lame'; *Matánach* 'burly'; *Cairmilíteach* /ˈkaɾʲmʲəlʲiːtʲəx/ [wiki-irish-orthography; wiki-irish-phonology §Munster] |
| 2 | **-án** (n., /aːn̪ˠ/) | noun/diminutive-augmentative | to a noun/adj. stem | *sparán* /ˈsˠpˠaɾˠaːn̪ˠ/, *moltachán* /ˌmˠɔl̪ˠhəˈxaːn̪ˠ/, *cromóg*-type formations [wiki-irish-phonology §Munster] |
| 3 | **-ín** (n., /iːnʲ/) | **diminutive** | any noun; the word becomes 4th declension (indeclinable) | *cailín* /ˈkalʲiːnʲ/ 'girl'; *toitín* /ˈt̪ˠɛtʲiːnʲ/; *dreoilín* /ˈdʲɾʲoːlʲiːnʲ/ 'wren' [wiki-irish-orthography; wiki-irish-declension §Declension] |
| 4 | **-óir / -eoir** (n.) | **agent noun** | to a verb/noun stem; 3rd declension (gen. -óra) | *bádóir* /ˈbˠaːd̪ˠoːɾʲ/ 'boatman' [wiki-irish-orthography; wiki-irish-declension] |
| 5 | **-úil** (adj., /uːlʲ/) | 'like, -ly' | to a noun; 3rd-decl. adj. (fem. gen. -úla) | *cosúil* /ˈkɔsˠuːlʲ/ 'like'; *leisciúil* /ˈl̠ʲɛʃcuːlʲ/ 'lazy'; *ríúil* /ˈɾˠiːuːlʲ/ 'kingly' [wiki-irish-orthography; wiki-irish-declension §Adjectives] |
| 6 | **Attributive adjective after the noun**, agreeing | the basic epithet | lenites after fem. sg., after a slender-final plural, and after masc. sg. genitive | *Máire Bhán*, *Pádraig Rua* [wiki-irish-name §Epithets; wiki-irish-declension §Adjectives] |
| 7 | **Preposed adjective / intensifying prefix + lenition** | compound epithet | *sean-, droch-, dea-, nua-, tréan-, fíor-, ard-, óg-, an-, ró-, príomh-* | *seanbhean*, *drochdhuine*, *ardbhrú*, *ógfhear*, *an-mhaith* /ˈanˈwa/ [wiki-irish-mutations §After preposed adjectives, §After most prefixes] |
| 8 | **Noun + noun compound**, second element lenited | *Lasairchos* type | see §3.6 — attested for prefixes, extrapolated for N+N | *Lasairchos* /ˈl̪ˠɑsˠəɾʲxosˠ/ 'flame-foot' (user's transcription) |
| 9 | **Genitive of a following noun** (*X na Y*, *X + gen.*) | 'X of the Y' | article *na* + gen.; gen. pl. eclipses | *na hoíche* 'of the night'; *na bhfocal* [wiki-irish-mutations §Changes to vowel-initial words, §Environments of eclipsis] |
| 10 | **Ó / Mac / Ní / Nic / Uí / Mhic + genitive name** | patronymic | see §3.4 table | *Ó Súilleabháin*, *Ní Bhriain*, *Mac Giolla Phádraig*, *Ó Maoil Eoin* [wiki-irish-name §Ó and Mac surnames] |

Plus the two **positional** epithets: *Óg / Mór / Beag* between given name and surname
(*Seán Óg Ó Súilleabháin*), and the traditional patronymic chain *Seán Phóil Shéamuis*
[wiki-irish-name §Epithets, §Traditional Gaeltacht names].

**eDIL** (`https://dil.ie/`) is the place to look up any specific epithet element; there is no
bulk download or public API, so query it per word at generation time [bib.md §edil].

---

## 7. Test words

See **`test-words.tsv`** in this directory (not `attested.tsv` — this is the source side, so the
file is the tool's **input** test set rather than a record of adaptations).

Columns: `orthography, ipa, dialect, gloss, category, features, note`.
`features` is a semicolon list of the §8 mismatch cases the word exercises, so the harness can
select a subset ("all the words with `slender_coronal`") when testing one target's rules.

**Count and provenance: 102 rows** — 29 `name`, 20 `epithet`, 53 `descriptor`.
- **79 rows carry IPA copied verbatim from a held source**, overwhelmingly
  `wiki-irish-orthography §Grapheme to phoneme correspondence` and
  `wiki-irish-phonology §Word-initial consonant clusters` / `§Post-vocalic consonant clusters
  and epenthesis` / `§Compound words`, which between them supply ~550 word+IPA pairs. The
  `note` column names the section for every row.
- **20 rows are marked `(constructed)`** in the note column: personal names for which no held
  source gives IPA. Each was assembled from attested pieces and the note names the attested
  model (e.g. *Sorcha* /ˈsˠɔɾˠəxə/ from attested *dorcha* /ˈd̪ˠɔɾˠəxə/; *Saoirse* /ˈsˠiːɾˠʃə/
  from attested *doirse* /ˈd̪ˠoːɾˠʃə/), following the caol-le-caol rule of §5.1. **These are
  the least trustworthy rows and should be the first replaced if the user hand-transcribes
  them.**
- **3 rows are the user's own transcriptions** (*Ciara*, *Matánach*, *Lasairchos*), noted as such.

**`dialect` column values:** `std` = the Wikipedia pan-dialectal scheme (§0), `C` Connacht,
`M` Munster, `U` Ulster.

**`features` vocabulary** — semicolon-separated, keyed to §8:

| Prefix | Tags |
|---|---|
| `bs:` broad/slender contrast at a place | `bs:labial`, `bs:coronal`, `bs:dorsal` |
| `seg:` a §8.2 segment the word contains | `seg:x`, `seg:ç`, `seg:ɣ`, `seg:j`, `seg:h`, `seg:w`, `seg:vʲ`, `seg:ŋ`, `seg:ɲ`, `seg:c-ɟ`, `seg:ɾˠ`, `seg:ɾʲ`, `seg:l̪ˠ`, `seg:lʲ`, `seg:n̪ˠ`, `seg:nʲ`, `seg:ʃ`, `seg:t̪ˠ` |
| `len:`/`dip:` §8.3 | `len:V` (contains a long vowel), `dip:iə`, `dip:uə`, `dip:əi`, `dip:əu` |
| `syl:` §2/§8.4 | `syl:onsetCC`, `syl:onsetCCC`, `syl:sC`, `syl:codaCC`, `syl:qualmismatch`, `syl:CnCr` |
| `eps:` §2.4 | `eps:epenthetic` (contains an epenthetic schwa), `eps:blocked` (an epenthesis environment where a blocker applies) |
| `mut:` §3.1–3.3 | `mut:lenition`, `mut:eclipsis`, `mut:hproth`, `mut:tproth` |
| `mor:` §3.5/§6 | `mor:genitive`, `mor:vocative`, `mor:compound`, `mor:patronymic`, `mor:suffix-ach`, `mor:suffix-ín`, `mor:suffix-úil`, `mor:suffix-óir` |
| `str:` §4.1 | `str:initial`, `str:munster`, `str:compound` |

So a harness can select "every word exercising /ɣ/" as `grep 'seg:ɣ'`, or "every word whose
output tests the epenthesis blockers" as `grep 'eps:blocked'`.

**Deliberate minimal pairs in the set**, for testing that a target's rules preserve a
distinction Irish makes:
- *mac* /mˠak/ ~ *mic* /mʲɪc/ — genitive by slenderization of both consonants.
- *caisleán* /ˈkaʃl̠ʲaːnˠ/ ~ *caisleáin* /ˈkaʃl̠ʲaːnʲ/ — genitive differing **only** in the
  final consonant's quality. **A target that neutralizes quality loses this pair entirely.**
- *Seán* /ʃaːnˠ/ ~ *a Sheáin* [ə çaːnʲ] — vocative = lenition + slenderization at once.
- *mór* /mˠoːɾˠ/ ~ *mhór* /woːɾˠ/ — radical vs. lenited.
- *cnoc* /kɾˠʊk/ ~ *cnaipe* /ˈkn̪ˠapʲə/ — the Cn→Cɾ dialect split.
- *speal* /sˠpʲal/, *sméara* /sˠmʲeːɾˠə/ (onset) and *beirt* /bʲɛɾˠtʲ/ (coda) — the
  quality-mismatch cases.
- *ainm* /ˈanʲəmʲ/ and *dearg* /ˈdʲaɾˠəɡ/ — epenthetic schwa; their near-minimal partners
  *anam*, *léirigh* carry an underlying schwa [irish-schwa-kwpl p.5].

**Bias to be aware of:** the attested IPA is heavily weighted toward *common nouns and
adjectives*, because those are what the Wikipedia articles use as illustrations.
`wiki-irish-name` contains large tables of Irish personal names but **gives no pronunciations
at all** [wiki-irish-name §Examples of first names and surnames] — hence the 20 constructed
rows, which are almost all given names. eDIL has no bulk download or API [bib.md §edil], so
there was no way to close this gap automatically.

## 8. Catalogue: the Irish segments and structures every target must decide about

This is the checklist each of the four target digests has to answer. Each item states what the
donor actually presents, how often, and what the options are. **Nothing here is decided.**

### 8.1 The broad/slender contrast — the decision that dominates all others

**What the donor presents:** a near-complete doubling of the consonant inventory, ~15 pairs
(§1.1), present in **every** Irish word, and carrying grammatical information (§3.5).

**What it actually is, articulatorily** (Connemara ultrasound, i.e. our reference dialect):
palatalization = active tongue-body **raising + fronting**, an [j]/[i]-like gesture;
velarization = tongue-body **backing**. Both also involve an independent tongue-**root**
component (~30% of the variance), so this is not purely a backness contrast
[nichiosain2018 p.31].

Place-by-place robustness — **this is the evidence for a place-sensitive adaptation rule**:
- **Labials:** robust, large tongue-body excursions for both palatalized and velarized —
  contradicting the traditional claim that slender labials are barely palatalized. But labials
  are the **most variable** place, since there is no lingual primary constriction to anchor to
  [nichiosain2018 pp.5–7, p.32].
- **Coronals: the weakest contrast.** For /sˠ/ vs /ʃ/ the backness difference is near-absent;
  /t̪ˠ/ vs /tʲ/ is better separated mainly because /tʲ/ is strongly fronted. Irish compensates
  with **secondary acoustic cues**: /tʲ ʃ/ have louder, longer, higher-CoG frication and are
  frequently affricated [nichiosain2018 p.31]. **This means the coronal broad/slender contrast
  is partly a sibilant-quality contrast** — /sˠ/ vs /ʃ/ — which most targets can carry directly
  as /s/ vs /ʃ/.
- **Dorsals:** height difference minimal (both closures are high) but **backness difference
  large**; velarized /x/ is markedly further back and lower than /k/, "possibly indicating
  uvular realization" — i.e. **velarization may be uvularization** [nichiosain2018 p.31].
  **This is the single most useful finding for the Arabic strand**, where broad → emphatic /
  uvular is on the table.

**Position:** the contrast is **weaker in codas**, significantly so for **labials and dorsals**
but *not* for coronals; coda ranking of stability is Coronal > Labial > Dorsal
[bennett-syllpos §7.1]. No position fully neutralizes it. Cause: general coda gestural
reduction plus stronger coarticulation of velarized consonants with the preceding vowel
[bennett-syllpos §7.1]. **So "neutralize quality in codas" is a defensible target-side rule with
Irish-internal support — but it should apply to labials and dorsals, not coronals.**

**Unit segment or C+glide?** The timing paper does not answer this in those terms, but its data
bear on it: in onsets the secondary gesture **lags** the primary one and peaks at release; in
codas the two gestures align independently to different landmarks by place (coda /Pʲ/ to the VC
transition, coda /Tʲ/ to C release) [bennett-timing §3.2, §9]. That is more consistent with a
**two-gesture, sequenced** coordination than a synchronous single segment — though the authors
themselves treat the secondary articulation as a property of one consonant "at least
phonologically" [bennett-timing p.38]. **Report this as an inference, not their claim.**
The **on/off-glides of §1.2 are already there phonetically** ([ɰ], [w], [j], [ə̯], [i̯]), so
"Cʲ → Cj" and "Cˠ → Cw/Cɰ" are not inventions — they externalize something audible.

**Options (undecided):**
1. **Depalatalize/deveralize** — collapse to a plain series. Cheapest; destroys the
   genitive/vocative contrast of §3.5 and makes many names homophonous.
2. **Cʲ → Cj, Cˠ → C** (or Cˠ → Cw) — export the secondary articulation as a segment.
3. **Colour the adjacent vowel** — let /Cʲ V/ surface as /C i̯V/ or a fronted vowel, /Cˠ V/ as a
   backed vowel. Has the most Irish-internal support (§1.2 vowel allophony).
4. **Map onto a marked target series** — Arabic emphatics for broad (with the uvular finding
   above as support), a palatalized series where a target has one.
5. **Place-sensitive hybrid** — carry the contrast on coronals (as /s/ vs /ʃ/, /t/ vs /tʃ/),
   drop it on labials and dorsals, drop it in codas. The articulatory evidence supports exactly
   this split.

### 8.2 The segment-by-segment list

Each target digest must give a row for each. "Frequency" is impressionistic from the ~550
attested transcriptions harvested here (unattested as a count).

| Irish segment | Source | Frequency in names | Notes for the target decision |
|---|---|---|---|
| **/x/** | radical ⟨ch⟩; lenition of /k/; the *-ach* suffix | **very high** — every *-ach* epithet ends /əx/ | *Matánach* /…nˠəx/, *taoiseach* /ˈt̪ˠiːʃəx/, *Gaelach*, *Lasairchos* /…xosˠ/. **[U]** can be [h] or delete finally [wiki-irish-phonology §Allophones]. Georgian has /x/; Welsh has /χ/; Arabic has /x/; Dutch has /x/ — this one is mostly free. |
| **/ç/** | lenition of /c/; /h/ before back vowels | moderate | *cheist* /çɛʃtʲ/, *deich* /dʲɛç/, *oíche* /ˈiːçə/, *a Sheáin* [ə çaːnʲ]. Dutch and German have it; Welsh, Arabic, Georgian do not. |
| **/ɣ/** | lenition/eclipsis of ⟨d g⟩ | moderate, and **word-initial** in mutated forms | *dhorn* /ɣoːɾˠn̪ˠ/, *ghasúr* /ˈɣasˠuːɾˠ/, *droch-dhuine* /…ˈɣinʲə/. **No home in Welsh or Arabic**; the project note suggests /ʁ/ [project-goals]. Georgian **has** /ɣ/. Dutch has /ɣ/ (or /ɦ/ in the north). |
| **/j/** | lenition of ⟨d g⟩ slender; ⟨gh dh⟩ | moderate, word-initial in mutated forms | *dhearg* /ˈjaɾˠəɡ/, *gheata* /ˈjat̪ˠə/, *Fíor-Dhia* /…ˈjiːə/. Allophone [ʝ] preconsonantally. **[M]** final /j/ → [ɟ]. |
| **/h/** | ⟨h⟩; lenition of /t̪ˠ tʲ sˠ ʃ/; h-prothesis | **high** — every lenited t/s | *hata*, *thall* /haːl̪ˠ/, *athair* /ˈahəɾʲ/, *na héisc*. Can be **elided intervocalically** [wiki-help-ipa-irish note 4]. Every target has /h/ except Georgian (which has /h/) and Dutch (/ɦ/) — mostly free; French-type targets would be the problem. |
| **/w/** | lenition of /bˠ mˠ/; eclipsis of /fˠ/; ⟨bh mh⟩ medially | **high** | *bhain* /wanʲ/, *mhór* /woːɾˠ/, *ábhar* /ˈaːwəɾˠ/, *leanbh* /ˈl̠ʲanˠəw/, *Siobhán* /ˈʃʊwaːnˠ/. **[C]:** [w] initially, **[vˠ]** elsewhere — so the same phoneme presents two very different targets depending on position. Arabic has /w/; Georgian has /v/ not /w/. |
| **/vʲ/** | lenition of /bʲ mʲ/; ⟨bh mh⟩ slender | high | *bhéal* /vʲeːlˠ/, *nimh* /n̠ʲɪvʲ/, *seirbhís* /ˈʃɛɾʲəvʲiːʃ/, *veidhlín* /ˈvʲəilʲiːnʲ/. Georgian lacks /f/ but has /v/; Arabic **lacks /v/** (→/f/ per project-goals). |
| **/fˠ fʲ/** | radical ⟨f⟩; lenition of /pˠ pʲ/ | moderate | *fós*, *fíon*, *pholl* /fˠoːl̪ˠ/. **Georgian lacks /f/** [project-goals] — a required decision there. |
| **/pˠ pʲ/** | ⟨p⟩ | **low in native vocabulary** — the article does not flag it as marginal, but ⟨p⟩ is mostly in loans and in eclipsed/lenited forms | *poll*, *príosún*, *pic*. Not a problem for any target. |
| **/ŋ/, /ɲ/** | eclipsis of /ɡ/, /ɟ/; ⟨ng⟩ | moderate, and crucially **word-initial** after eclipsis | *ngasúr* /ˈŋasˠuːɾˠ/, *ngeata* /ˈɲat̪ˠə/, *long* /l̪ˠuːŋɡ/, *rinc* /ɾˠɪɲc/, *cuing* /kɪɲɟ/. **Word-initial /ŋ ɲ/ is banned in most targets.** Only arises if the generator emits eclipsed forms (§9). |
| **/ɾˠ/ vs /ɾʲ/** | everywhere | **very high** | Both are taps in the transcription, but /ɾʲ/'s primary allophone is a palatalized postalveolar **fricative [ɹ̝ʲ]** [wiki-irish-phonology §Allophones]. A target with a single /r/ or /ɾ/ must choose whether the slender member becomes /rʲ/, /rj/, /ʒ/-ish, or merges. Note Irish has **no trill** in the modern dialects — the four historical rhotics merged to two taps [wiki-irish-phonology §Fortis and lenis sonorants]. Also note the **/ɾˠ before slender coronals** exception of §2.3, which delivers quality-mismatched /ɾˠtʲ/, /ɾˠdʲ/, /ɾˠʃ/, /ɾˠnʲ/, /ɾˠlʲ/. |
| **/l̪ˠ lʲ n̪ˠ nʲ/** (the four laterals/nasals) | everywhere | **very high** | Present in every transcription. Broad /l̪ˠ n̪ˠ/ are **dental**; slender /lʲ nʲ/ alveolar/alveolo-palatal [wiki-irish-phonology §Allophones]. The four-way fortis/lenis system of the IPA key (/l̪ˠ lˠ l̠ʲ lʲ/, /n̪ˠ nˠ n̠ʲ nʲ/) is not distinguished by any modern dialect [wiki-help-ipa-irish notes 5, 6] — so treat input as two-way per §1.1. A target must decide: dental vs. alveolar (usually free), and slender /lʲ nʲ/ vs /lj nj/ vs /ʎ ɲ/. |
| **Voiceless sonorants** | — | **not a phoneme; a phonetic effect** | Two sources describe them. Quiggin documents voiceless L, l, L′, l′, N, n, N′, r, r′ "with strongly breathed off-glide", arising from historical sonorant + *th*/*f(h)* clusters, mainly in the future tense [quiggin1906 §213, §220, §227, §232, §242, §248, §259, §264, §279, §288]. Ní Chasaide reports nasals and liquids are **devoiced before and after voiceless plosives**, and that prepausal /l n/ devoice [nichasaide1999 p.113]. Neither is a contrastive segment. **The project-goals note "Irish lenition outputs [v w j h] and voiceless sonorants" is only half right**: [v w j h] are phonemic lenition outputs; the voiceless sonorants are allophonic and mostly verbal-morphological. **Recommendation: do not put voiceless sonorants in the input inventory.** |
| **/sˠ/ vs /ʃ/** | everywhere | very high | The one broad/slender pair most targets can carry losslessly (§8.1). |
| **/t̪ˠ d̪ˠ/ dental** | everywhere | very high | Note the PHOIBLE convention warning that applies to the Arabic row: UPSID dental diacritics there mark plain coronals, not true dentals [project-goals]. Irish's **are** true dentals [wiki-irish-phonology §Allophones]. |
| **/c ɟ/** | slender ⟨c g⟩ | high | *ceist* /cɛʃtʲ/, *geata* /ˈɟat̪ˠə/, *scéal* /ʃceːl̪ˠ/. May be palatovelar [k̟ ɡ˖]. Few targets have palatal stops; the natural repairs are /kj ɡj/, /tʃ dʒ/, or plain /k ɡ/. |

### 8.3 Vowel length and the diphthongs

- **Five long/short pairs** /iː ɪ, eː ɛ, aː a, oː ɔ, uː ʊ/, with the long/short members
  **qualitatively distinct as well as durationally** [wiki-irish-phonology §Vowels;
  nichasaide1999 p.114]. A target without phonemic length must decide between mapping length to
  quality (the pairs already differ in quality, so this is nearly free), dropping it, or
  reinterpreting it as stress.
- **Four diphthongs /iə uə əi əu/**, all **falling** [wiki-help-ipa-irish note 9].
  - /iə/ and /uə/ are **centering** — the natural repairs are a long monophthong (/iː uː/),
    a two-syllable /i.a u.a/, or a glide-initial /ja wa/. Note *Ciara* /ˈkɪə.ɾˠə/ shows the
    user syllabifying /ɪə/ as a **single nucleus** in a two-syllable word.
  - /əi/ and /əu/ are **wide** and pattern like English /aɪ aʊ/; **[U]** compresses them to
    /eː oː/ [wiki-help-ipa-irish note 10], which is itself a ready-made repair.
  - /iə/ appears after a broad consonant essentially only in word-initial broad /ɾˠ/
    [wiki-irish-phonology §Vowel backness] — so /ɾˠiə/ is the marked case (*riamh*).
- **Schwa never occurs stressed** [wiki-irish-phonology §Vowels], and much of the schwa in a
  donor word is **epenthetic** (§2.4) rather than lexical. A target could legitimately delete
  epenthetic schwa and rebuild its own — this is worth flagging as an option, since it changes
  the syllable count of every *gorm*-type word.

### 8.4 Initial clusters the targets will have to handle

From §2.2, the clusters that actually arrive, grouped by the §3-style repair each target will
have to assign. **The list is smaller than the project-goals note assumes**, because of the
Connacht /Cn/→/Cɾ/ rule (§2.2).

| Group | Clusters | Notes |
|---|---|---|
| **obstruent + liquid** | /pˠl̪ˠ pʲlʲ bˠl̪ˠ bʲlʲ fˠl̪ˠ fʲlʲ d̪ˠl̪ˠ dʲlʲ t̪ˠl̪ˠ tʲlʲ kl̪ˠ clʲ ɡl̪ˠ ɟlʲ/ and the /ɾ/ series /pˠɾˠ … ɟɾʲ/ | The commonest type; most targets allow at least some |
| **obstruent + nasal** | /t̪ˠn̪ˠ tʲnʲ kn̪ˠ cnʲ ɡn̪ˠ ɟnʲ/ + irregular /mˠn̪ˠ/ | **[C] these mostly do not arrive** — they surface as /t̪ˠɾˠ kɾˠ ɡɾˠ mˠɾˠ/ [wiki-irish-phonology §Word-initial consonant clusters] |
| **/s/ + stop** | /sˠpˠ sˠt̪ˠ sˠk/, /ʃpʲ ʃtʲ ʃc/ | The classic sC problem for Arabic (which epenthesizes) |
| **/s/ + sonorant** | /sˠmˠ sˠl̪ˠ sˠɾˠ sˠn̪ˠ/, /ʃmʲ ʃlʲ ʃɾʲ ʃnʲ/ | |
| **/s/ + stop + liquid (CCC)** | /sˠpˠl̪ˠ sˠpˠɾˠ ʃclʲ ʃcɾʲ ʃtʲɾʲ/ | Three-consonant; the hardest for Arabic and Georgian-with-repair |
| **quality-mismatched** | /sˠpʲ sˠmʲ sˠc/ and /sˠpʲlʲ sˠpʲɾʲ/ | §2.2 exception — a target with a broad→X / slender→Y rule gets a mixed output here |
| **mutation-only** | /wl̪ˠ vʲɾʲ çlʲ xɾˠ jɾʲ jnʲ hlʲ hn̪ˠ hɾˠ mˠl̪ˠ mʲlʲ mʲɾʲ n̪ˠl̪ˠ n̪ˠɾˠ nʲɾʲ ɲlʲ ɲɾʲ ɲnʲ/ | Only if the generator emits mutated forms — see §9 |

### 8.5 Mutation and case on the source side

The mutation and genitive/vocative machinery is fully specified in §3. What each target digest
needs to say is only: **does the target's loan phonology have anything to say about
alternating stems?** No source in this directory addresses that (it is a target-side question).
What the Irish side guarantees:
- The **same name can present up to four different initial consonants** (radical, lenited,
  eclipsed, t-/h-prefixed): *Seán* /ʃ/ ~ *a Sheáin* /ç/ ~ (after some particles) etc.
- The **same name can present two different final consonant qualities** (nom. vs. gen./voc.).
- A target that neutralizes quality (§8.1) **collapses the second of these entirely**.

---

## 9. Open questions

1. **Does the generator emit mutated forms at all?** This is the biggest fork. If epithets are
   generated only in citation form, then /w ɣ ç j h ŋ ɲ/ appear only where they are radical, and
   the whole "mutation-only onset" row of §8.4 disappears. If the generator produces
   vocatives (*a Sheáin*), genitive chains (*Seán Phóil Shéamuis*) or article phrases
   (*na hÉireann*), then every target needs a rule for word-initial /ç x ɣ j h w ŋ ɲ/ and for
   the mutation cluster set. **Not a linguistic question — a design decision, and it changes
   the size of every target's rule file.**
2. **Which dialect fixes the vowel length?** The ⟨ll nn rr rd rl rn m ng⟩ lengthening (§4.2)
   differs between Ulster, Connacht and Munster, so *ceann* is /caːn̪ˠ/, /can̪ˠ/ or /cəun̪ˠ/
   depending. The user's transcriptions look Connacht/standard; but *Ciara* /ˈkɪə.ɾˠə/ has a
   diphthong where the ⟨ia⟩ spelling and *ciall* /ciəl̪ˠ/ would predict /iə/ after a **slender**
   /c/, not /kɪə/ after a broad /k/ — **worth asking the user whether /ˈkɪə.ɾˠə/ is deliberate**
   (the expected Connacht form would be /ˈciəɾˠə/).
3. **Noun+noun compound lenition** (§3.6) is unattested in this source set; the *Lasairchos*
   transcription implies it applies. Confirm before generating compound epithets in bulk.
4. **The epenthesis rule's blocking conditions conflict between the two Wikipedia articles**
   (§2.4). The ≥3-syllable condition is only in the phonology article; the morpheme-boundary
   condition is only in the (uncited) orthography article. Ní Chiosáin 1999, the underlying
   source, is not held.
5. **No exhaustive licit-final-cluster list exists in the open literature we hold** (§2.3). The
   attested coda set had to be assembled by inspection.
6. **Whether the epenthetic schwa should survive adaptation.** It is not lexical, it is
   durationally distinct from underlying schwa [irish-schwa-kwpl], and a target with its own
   epenthesis would arguably re-derive it. Currently the tool would receive it as a plain /ə/
   in the input string with no marking. **A `features` tag on the input, or a separate
   underlying-form column, would let the tool choose.**
7. **The four-way L/N system.** No modern dialect has it, but the Wikipedia IPA key uses it, so
   third-party transcriptions of Irish names may contain /lˠ l̠ʲ nˠ n̠ʲ/. Decide whether the
   tool normalizes these on input.
8. **Strand 5 has no derivation path from Modern Irish to Old Irish** (§10.7). `bib.md`
   promised one from `wiki-oi-phonhistory`; that article covers Proto-Celtic → Old Irish only.
   The recommendation in §10.7 is to look each name up in eDIL and inflect it with §10.5 rather
   than derive it — **but that makes strand 5 a lookup task, not a rule task, and changes its
   cost profile relative to the other four.** Worth confirming with the user before building it.
9. **Does strand 5 use the Old Irish neuter and dual?** Old Irish has three genders and three
   numbers; Modern Irish has two and two [wiki-oi-grammar §Nouns; wiki-irish-declension §lead].
   Whether strand-5 names carry neuter/dual forms is a setting decision, not a linguistic one.
10. **Does strand 5 use the third mutation?** Old Irish aspiration/gemination (§10.4) has no
    Modern Irish counterpart as a system, and it is triggered by the **genitive singular of all
    feminines** and the **vocative and accusative plural** — very common name environments. It
    was also barely written [wiki-oi-grammar §Aspiration and gemination], so including it is
    audible but nearly invisible in the romanization.

---

## 10. Old Irish (strand 5)

*(Added for this digest; not in `../DIGEST-TEMPLATE.md`.)*

Old Irish = c. 600–900. Strand 5 takes Old Irish forms of the same names with **no foreign
filter**, so what this section has to supply is: the inventory, enough orthography→sound to
pronounce a written form, the stress rule, and enough noun/adjective/compound morphology to
**inflect** a name rather than guess at it.

### 10.1 Inventory

**The system is a four-way split of each inherited consonant**, from crossing two independent
binary features: **fortis vs. lenis** (= unlenited vs. lenited) and **broad (velarized) vs.
slender (palatalized)** [wiki-old-irish §Consonants]. "Both the palatalised ('slender') and
lenited variants of consonants were phonemicised, **multiplying the consonant inventory by
four**" [wiki-oi-phonhistory §Summary of changes]. For obstruents the fortis/lenis dimension is
**stop vs. fricative**; for *l n r m* it is **tense/long vs. lax/short**
[wiki-old-irish §Consonants].

| | Labial | Dental | Alveolar | Velar | Glottal |
|---|---|---|---|---|---|
| Nasal | m / mʲ | N n / Nʲ nʲ | | ŋ / ŋʲ | |
| Plosive | p b / pʲ bʲ | t d / tʲ dʲ | | k ɡ / kʲ ɡʲ | |
| Fricative | f v / fʲ vʲ | θ ð / θʲ ðʲ | s / sʲ | x ɣ / xʲ ɣʲ | h / hʲ |
| Nasalized fric. | ṽ / ṽʲ | | | | |
| Rhotic | | R r / Rʲ rʲ | | | |
| Lateral | | L l / Lʲ lʲ | | | |

[wiki-old-irish §Consonants] — **≈46 consonant phonemes** on this count. The pairing statement:
"/f v θ ð x ɣ h ṽ n l r/ are the broad **lenis** equivalents of broad **fortis**
/p b t d k ɡ s m N L R/; likewise for the slender equivalents" [wiki-old-irish §Consonants].

Uncertain values [wiki-old-irish §Consonants]:
- /sʲ/ "may have been pronounced [ɕ] or [ʃ], as in Modern Irish."
- /hʲ/ "may have been the same sound as /h/ or /xʲ/."
- "The precise articulation of the fortis sonorants /N Nʲ L Lʲ R Rʲ/ is unknown, but they were
  probably longer, tenser and generally more strongly articulated… /Nʲ/ and /Lʲ/ may have been
  [ɲ] and [ʎ]. The difference between /R(ʲ)/ and /r(ʲ)/ may have been that the former were
  trills while the latter were flaps."
- **/p pʲ/ is marginal**: "relatively rare in Old Irish, being a recent import from other
  languages such as Latin"; and "most /f fʲ/ sounds actually derive historically from /w/."

**Fortis/lenis minimal pairs** [wiki-old-irish §The consonants l, n, r]:
*corr* /koR/ 'crane' vs. *cor* /kor/ 'putting'; *coll* /koL/ 'hazel' vs. *col* /kol/ 'sin';
*sonn* /soN/ 'stake' vs. *son* /son/ 'sound'; **/iNʲɡʲən/ 'nail, claw' vs. /inʲɣʲən/
'daughter'** — both written *ingen*.

**Vowels** [wiki-old-irish §Vowels]. Short: /i e a o u/ + a marginal /æ ~ œ/ (from u-infection
of stressed /a/ before a palatalized consonant — the source of the wild spelling variation in
*tulach ~ telaig ~ taulich ~ tailaig* 'hill', and rampant in names in the prefix *air-*).
Long: /iː eː aː oː uː/. Pokorny's list: "5 short vowels *a e i o u*, 5 long *á é í ó ú*, and
**8 diphthongs: *aí (áe), oí (óe), uí, áu, éu (éo), íu, ía, úa***" [pokorny1914 p.6 §4].

Two important early/late splits:
- **Two é's.** /e₁ː/ (< PC \*ē, or Latin ē) vs. /e₂ː/ (from compensatory lengthening), both
  written ⟨é⟩ but distinct. In later Old Irish **/e₁ː/ becomes ⟨ía⟩** (⟨é⟩ before a palatal
  consonant) while **/e₂ː/ stays ⟨é⟩**; /e₂ː/ undergoes u-affection to ⟨éu/íu⟩, /e₁ː/ does not
  [wiki-old-irish §Vowels]. "Perhaps /e₁ː/ was [eː] while /e₂ː/ was [ɛː]."
- **Two ó's** (possibly), from former diphthongs \*eu \*au \*ou vs. from compensatory
  lengthening; "in later Old Irish both sounds appear usually as **⟨úa⟩**, sometimes ⟨ó⟩"
  [wiki-old-irish §Vowels]. Early /ai/ and /oi/ merged in later Old Irish, but scribes kept
  writing both ⟨aí⟩ and ⟨oí⟩.

**Unstressed vowels** [wiki-old-irish §Vowels]:
- **Word-finally, all ten short-vowel × quality combinations occur**: *marba* /ˈmarva/,
  *léicea* /ˈLʲeːɡʲa/, *marbae* /ˈmarve/, *léice* /ˈLʲeːɡʲe/, *marbai* /ˈmarvi/,
  *léici* /ˈlʲeːɡʲi/, *súlo* /ˈsuːlo/, *doirseo* /ˈdoRʲsʲo/, *marbu* /ˈmarvu/,
  *léiciu* /ˈLʲeːɡʲu/.
- **Non-finally, only two phonemes: /ə/** (written ⟨a ai e i⟩ by surrounding consonant quality)
  **and /u/** (written ⟨u o⟩; occurs after a broad labial — *lebor* /ˈLʲevur/ 'book',
  *domun* /ˈdoṽun/ 'world' — or where the following syllable had PC \*ū).
- "**All unstressed long vowels that have not been thrown out by syncope have been shortened**"
  [pokorny1914 p.20 §56], though length is analogically restored in compounds (*ír-bág*).

**CONFLICT — two-way vs. three-way quality.** `wiki-old-irish` and `wiki-oi-phonhistory` use a
**two-way** broad/slender contrast. Pokorny uses **three**: "Every consonant may be pronounced
in three different ways. It may possess a **palatal (i) quality**, a **broad or neutral (a)
quality**, or a **rounded (o and u) quality**… A palatal consonant is followed by *e* or *i*, a
broad consonant by *a*, and a rounded one by *o* or *u*" [pokorny1914 pp.13–14 §35]. UT Austin
names three labels (palatal / velar / neutral) but they resolve to the two-way system
[utaustin-l1 §1.1]. **The three-way system is what generates the ⟨-iu -eo -eu -au⟩ glide
spellings**; the two-way account handles the same data as "u-infection". **For generating name
spellings, Pokorny's three-way system is the directly implementable one.**

### 10.2 Orthography → sound

Eighteen letters *a b c d e f g h i l m n o p r s t u*, plus *á é í ó ú*, the lenition superdots
*ḟ ṡ*, and the eclipsis superdots *ṁ ṅ* [wiki-old-irish §Orthography]. Standing caveat: "the
orthography of Old Irish is not fixed… Individual manuscripts may vary greatly"
[wiki-old-irish §Orthography].

**Master table** [wiki-old-irish §Orthography]:

| Letter | Initial | Initial eclipsed | Initial lenited | Non-initial single | Geminate |
|---|---|---|---|---|---|
| b | /b/ | ⟨mb⟩ /m/ | /v/ | /v/ | ⟨bb⟩ /b/ |
| c | /k/ | /ɡ/ | ⟨ch⟩ /x/ | /k/, **/ɡ/** | ⟨cc⟩ /k/ |
| d | /d/ | ⟨nd⟩ /N/ | /ð/ | /ð/ | — |
| f | /f/ | /v/ | ⟨ḟ, fh⟩ **∅** | /f/ | — |
| g | /ɡ/ | ⟨ng⟩ /ŋ/ | /ɣ/ | /ɣ/ | — |
| l | /L/ | — | /l/ | /l/ | ⟨ll⟩ /L/ |
| m | /m/ | — | /ṽ/ | /ṽ/ | ⟨mm⟩ /m/ |
| n | /N/ | — | /n/ | /n/ | ⟨nn⟩ /N/ |
| p | /p/ | /b/ | ⟨ph⟩ /f/ | /p/, **/b/** | ⟨pp⟩ /p/ |
| r | /R/ | — | /r/ | /r/ | ⟨rr⟩ /R/ |
| s | /s/ | — | ⟨ṡ, sh⟩ /h/ | /s/ | — |
| s₂ (< \*sw, \*sɸ) | /s/ | — | ⟨f, ph⟩ /f/ | — | — |
| t | /t/ | /d/ | ⟨th⟩ /θ/ | /t/, **/d/** | ⟨tt⟩ /t/ |

*r l n s* are **not subject to eclipsis** [wiki-old-irish §Orthography]. s₂ is a handful of
words: *sïur* ~ *fïur* 'sister', *sesser* ~ *mórfesser*, *do·seinn* ~ *do·sephainn*
[wiki-old-irish §Orthography note 1].

**Six conventions that between them let you read a written name:**

1. **Lenition is mostly not written.** "Lenition was **not indicated in the spelling except in
   the case of initial voiceless stops**, written *ph th ch* when lenited. In later Old Irish,
   initial *f s* come to be written *ḟ ṡ*" [wiki-oi-grammar §Lenition]. Pokorny identically:
   "Only in the case of c, p, t is aspiration regularly expressed in writing… **b, d, g, m, l,
   n, r may represent the aspirated or the unaspirated sounds**" [pokorny1914 p.7 §8].
   **There is no ⟨bh dh gh mh⟩ in Old Irish** — that is a later development
   [utaustin-l1 §1.1; wiki-irish-orthography §Diacritics], and it is the single biggest visual
   difference between an Old Irish and a Modern Irish name.
2. **⟨c t p⟩ are voiced /ɡ d b/ non-initially unless doubled.** *macc* /mak/ 'son' vs.
   *bec/becc* /bʲeɡ/ 'small'; *bratt* /brat/ 'mantle' vs. *brot/brott* /brod/ 'goad'
   [wiki-old-irish §Stops following vowels]. The reason is script poverty: ⟨b d g⟩ were needed
   for the **fricatives** /v ð ɣ/ [utaustin-l1 §1.1]. So: **⟨b d g⟩ non-initially = /v ð ɣ/**
   (*dub* /duv/, *mod* /moð/, *mug* /muɣ/, *claideb* /klaðʲəv/), and ⟨ch ph th⟩ = /x f θ/
   (*ech* /ex/, *oíph* /oif/, *áth* /aːθ/).
3. **Double letters mean fortis.** ⟨ll nn rr mm⟩ = /L N R m/, single = /l n r ṽ/. "Doubly
   written consonants of this sort **do not occur in positions where tense sonorants developed
   from non-geminated Proto-Celtic sonorants** (such as word-initially or before a consonant)"
   [wiki-old-irish §The consonants l, n, r]. More generally, "**geminating a consonant ensures
   its unmutated sound**" [wiki-old-irish §Orthography]. And Pokorny's warning: "double
   consonants are often written **only in order to show that the respective consonant was not
   aspirated**" [pokorny1914 p.5].
4. **Stops after ⟨l n r m⟩ are genuinely ambiguous** [wiki-old-irish §Stops following other
   consonants]: *derc* is both /dʲerk/ 'hole' and /dʲerɡ/ 'red'; *daltae* /daLte/ 'fosterling'
   vs. *celtae* /kʲeLde/. Rules of thumb: after *m*, ⟨b⟩ = /b/ (*imb* /imʲbʲ/); after *d l r*,
   ⟨b⟩ = /v/ (*delb* /dʲelv/, *marb* /marv/); after *n r*, ⟨d⟩ = /d/ (*bind*, *cerd*); after
   *n l r*, ⟨g⟩ is usually /ɡ/ (*long* /Loŋɡ/, *delg* /dʲelɡ/) but /ɣ/ in a few words
   (*ingen* /inʲɣʲən/ 'daughter', *bairgen* /barʲɣʲən/ 'loaf').
5. **Glide vowels mark consonant quality — this is the core name-spelling machinery.** Slender
   consonants occur "(i) before a written *e é i í*; (ii) **after a written *i*, when not
   followed by a vowel letter** (but not after the diphthongs *aí oí uí*)"
   [wiki-old-irish §Orthography]. Pokorny's rules [pokorny1914 p.14 §§36–41]:
   - **§36 i-glide:** "Before a palatal consonant at the end of a word or of a syllable
     (**except after í, é, and the diphthongs áe/aí, óe/oí, uí**) a glide-vowel *i* is regularly
     inserted": *muir* 'sea' < \*mori, *toimtiu* 'opinion'.
   - **§37:** before an intervocalic palatal consonant an *i* glide is often inserted, "**though
     not regularly**": *flathi* ~ *flaithi*.
   - **§38 u-glide:** "Before an *u*-coloured consonant at the end of a word or of a syllable
     **after short a, e, i**, an *u* glide is regularly inserted": *fiuss* 'knowledge',
     *firu* 'men (acc. pl.)'.
   - **§39:** "**No glide-vowel is inserted before (originally) a- or o-coloured consonants**":
     *fer* 'man' < \*viros.
   - **§40:** final *a o u* after palatal consonants are written **-ea -eo -iu**.
   - **§41:** final *e i* after non-palatal consonants are written **-ae -ai** from the 9th c.:
     *nuie → nuae → nua*; *lobre → lobrae → lobra* 'weakness'.
   The i-glide was probably real: "*duine* /dunʲe/ was realised as [dui̯nʲe]"
   [wiki-old-irish §Vowels].
   The post-stress /ə/ spelling grid [wiki-old-irish §Vowels] — **the vowel letter has no
   relation to the etymological vowel**:

   | preceding C | following C | spelling | example |
   |---|---|---|---|
   | broad | broad | ⟨a⟩ | *dígal* /ˈdʲiːɣəl/ |
   | broad | slender (closed syll.) | ⟨ai⟩ | *dígail* /ˈdʲiːɣəlʲ/ |
   | slender | broad | ⟨e⟩ | *dliged* /ˈdʲlʲiɣʲəð/ |
   | slender | slender | ⟨i⟩ | *dligid* /ˈdʲlʲiɣʲəðʲ/ |

6. **⟨h⟩ is not a reliable sound.** "Although Old Irish has both a sound /h/ and a letter *h*,
   **there is no consistent relationship between the two**. Vowel-initial words are sometimes
   written with an unpronounced *h*… **the name of Ireland, *Ériu*, was sometimes written
   *Hériu***. On the other hand, words that begin with the sound /h/ are usually written without
   it: *a ór* /a hoːr/ 'her gold'" [wiki-old-irish §Orthography].

### 10.3 Stress

"**Stress is generally on the first syllable of a word.** However, in verbs it occurs on the
second syllable when the first syllable is a clitic (*as·beir* /asˈberʲ/ 'he says'). In such
cases, **the unstressed prefix is indicated with a following centre dot ⟨·⟩**"
[wiki-old-irish §Stress].

Pokorny states which words are never stressed: "**The article, pronouns, and prepositions before
their relation, infixed personal pronouns and the copula as well as emphasising pronouns,
affixed demonstrative pronouns, and some conjunctions, never bear any stress**… **All other
words with the exception of the verbs are stressed on the first syllable.** Note — In compounds,
as *ro-mór* 'very great', *com-lán* 'complete', the stem syllable may bear a secondary stress.
This is of course a late development" [pokorny1914 p.17 §§51–52].

**For names this is simple: initial stress, including in nominal compounds** — "the first
syllable in uncompounded words susceptible of full stress **as well as in nominal compounds**"
[utaustin-l1 §1.2]. The deuterotonic/prototonic verb machinery (*do·beir* vs. *ní·tabair*)
[utaustin-l1 §1.2; wiki-oi-phonhistory §Allomorphy] does not touch nouns and can be ignored for
strand 5 unless verbal epithets are wanted.

**What initial stress did to everything else** — the three changes that give Old Irish its
shape, and which a generator has to reproduce:
1. **Apocope.** "In words of more than one syllable **all final vowels and diphthongs have been
   dropped**, except when preceded by *i*" (*túath* < \*teutā); final *d t k n m s* and
   s-clusters dropped (*rí* < \*rēgs); in polysyllables a short vowel goes with them
   (*traig* 'foot' < \*traghets) [pokorny1914 p.15 §§42–45].
2. **Syncope.** "In words of more than two (and four) syllables… the vowel of the second (and
   fourth) syllable is thrown out" — *toimtiu* < \*to-mentiu, *apstal* < Lat. *apostolus*
   [pokorny1914 pp.18–19 §55]. **And syncope transphonologises quality across the resulting
   cluster:** *dorus* /ˈdorus/ 'door' → gen. *doirseo* /ˈdorʲsʲo/
   [wiki-oi-grammar §Syncope]. Pokorny's rule: "**When consonants of different quality come
   together by syncope, the quality of the first consonant prevails. But when consonants of *u*
   and *i* quality come together, the whole group becomes palatal**" — *rígnai* dat. of
   *rígain* 'queen'; **Lugaid → gen. Luigdech** (Ogam *Lugudeccas*) [pokorny1914 p.19 §55.II].
3. **Secondary (epenthetic) vowels.** "If after the loss of final syllables a final consonant
   group ended in *l r n m*, preceded by a different consonant, **a secondary vowel is developed
   between them**": *arathar* 'plough' < \*aratrom, *immon* 'hymn' < Lat. *hymnus*,
   *domun* 'world' < \*domn. Not when the preceding consonant was lost (*úar* 'cold'), nor when
   *m n* follow postvocalic *r l* or lenited *d* (*salm* 'psalm') [pokorny1914 pp.16–17 §50].
   **This is the Old Irish ancestor of the modern epenthesis of §2.4, and it applies in a
   different, wider set of environments.**

### 10.4 Initial mutations

Three, not two [wiki-oi-grammar §Initial mutations]. The contrast set:

| No change | Lenition (ᴸ) | Nasalization (ᴺ) | Aspiration/gemination (ᴴ) |
|---|---|---|---|
| *ech* /ex/ 'horse' | *a ech* /a ex/ 'his horse' | *a n-ech* /a nex/ 'their horse' | *a ech* /a hex/ 'her horse' |
| *bo* /bo/ 'cow' | *a bo* /a vo/ | *a m-bo* /a mbo/ | *a bo* /a bbo/ |
| *tech* /tʲex/ 'house' | *a thech* /a θʲex/ | *a tech* /a dʲex/ | *a tech* /a ttʲex/ |

**Lenition** [wiki-old-irish §Orthography; pokorny1914 p.7 §7]:
/p/→/f/ ⟨ph⟩ · /t/→/θ/ ⟨th⟩ · /k/→/x/ ⟨ch⟩ · /b/→/v/ · /d/→/ð/ · /ɡ/→/ɣ/ · /m/→/ṽ/ ·
/s/→/h/ ⟨ṡ sh⟩ · s₂→/f/ ⟨f ph⟩ · /f/→∅ ⟨ḟ fh⟩ · **/L N R/→/l n r/** (never written).
Word-initial sonorants are fortis by default and lenite to lenis: *rún* /Rˠuːnˠ/ vs.
*a rún* /a rˠuːnˠ/; *lón* /Lˠoːnˠ/ vs. *a lón* /a lˠoːnˠ/
[wiki-irish-phonology §Fortis and lenis sonorants].

**Nasalization (→ modern eclipsis)** [pokorny1914 p.10 §21]: /p t k/ → /b d ɡ/ (unwritten);
/b/ → /m/ ⟨mb⟩; /d/ → /N/ ⟨nd⟩; /ɡ/ → /ŋ/ ⟨ng⟩; /f/ → /v/ (written ⟨b⟩); vowel → /n/+V ⟨n-⟩;
*s r l n m* unchanged. "It is only in the case of b, d, g and of initial vowels that eclipsis is
regularly expressed in writing." "This mutation gave rise to the eclipsis mutation in modern
Irish" [wiki-oi-phonhistory §Nasalization].

**Aspiration/gemination** — the mutation Modern Irish has lost as a system. "**Aspiration
involved prepending an additional /h/ to a vowel-initial word**… **In gemination, an initial
consonant was geminated** by a preceding word originally ending in /k/, /s/ or /t/ after a
vowel… **Gemination was only occasionally indicated**… **Aspiration was not indicated at all**"
[wiki-oi-grammar §Aspiration and gemination]. UT Austin's worked example: preposition *la*ᴴ +
*Ultu* → ***hUltu*** [utaustin-l1 §1.1]. It is the modern *na hÉireann* h-prothesis, but with a
much wider distribution — notably **the genitive singular of all feminines** and **the vocative
and accusative plural of all genders** [wiki-oi-grammar §Aspiration and gemination].

**Environments, by case** [wiki-oi-grammar §Lenition, §Nasalisation, §Aspiration and gemination]:

| Mutation | Triggering case-forms |
|---|---|
| ᴸ lenition | nom./voc. sg. of **all feminines**; **dat. sg. of all genders**; nom./voc./acc./gen. **dual** of masc. and fem.; nom./voc./acc. **plural of all neuters** |
| ᴺ nasalization | nom./voc./acc. sg. and dual **of all neuters**; **acc. sg. of all masc. and fem.**; **gen. pl. of all genders** |
| ᴴ aspiration/gemination | **gen. sg. of all feminines**; **voc. and acc. pl. of all genders** — i.e. the vowel-final forms that trigger neither of the other two |

Pokorny's operational trigger list for lenition is the fuller one and the one to implement
[pokorny1914 pp.7–9 §§9–18]; the name-relevant entries:
- **the vocative particle *a*** lenites [pokorny1914 p.8 §12];
- an **adjective or dependent genitive** closely following is lenited after a dat. sg., after a
  **nom. sg. f. or voc. sg. of any gender**, after a gen. sg. of a masc./neut. o- or io-stem,
  after a nom. pl. masc. o-/io-stem, and after nom./voc. pl. neut. [pokorny1914 p.8 §10];
- possessives *m(o), do, t', a* (m./n.) lenite — *a chenél* 'his tribe' [pokorny1914 p.8 §11];
- **inside nominal compounds**, after nouns, adjectives and numerals, and after the prefixes
  *so-/su-, do-/du-, mí-, neb-/neph-* — *dag-theist* 'a good testimony', *mí-thoimtiu* 'a false
  opinion' [pokorny1914 p.8 §16].
- **Blocked**: before *d t* when the preceding word ends in *l n s* (*cen tossach*); and when
  the preceding word ends in a **homorganic** consonant (*cach cloine*) [pokorny1914 p.9 §19].

Nasalization triggers, name-relevant: **after the gen. pl. and acc. sg. of all genders and the
nom./acc. sg. neuter** (*nert n-irisse* 'strength of faith', *co cenn m-bliadnae*); after the
possessives *ar, far, a* 'their'; after *secht ocht noí deich* [pokorny1914 pp.10–11 §§22–23].
"**Unstressed words or syllables cannot be eclipsed as a rule**" [pokorny1914 p.11 §22].

**Possessive paradigm** [wiki-oi-grammar §Possessive pronouns], directly usable:
1sg *mo*ᴸ / *m'* · 2sg *do*ᴸ / *t' th'* · 3sg m *a*ᴸ · 3sg f *a*ᴴ · 3sg n *a*ᴸ · 1pl *ar*ᴺ ·
2pl *for/far/bar*ᴺ · 3pl *a*ᴺ. So *a thech* 'his house' / *a tech* [a tʲex] 'her house' /
*a tech* [a dʲex] 'their house'; *a ainm* /a hanʲmʲ/ 'her name'; *ar n-anmann* 'our names'.

**The article** [wiki-oi-grammar §Declension of the definite article, §Morphophonology]:
sg. m. nom. *in(t)*, f. nom. *in(d)*ᴸ / *int*ᴸ, n. nom. *a*ᴺ; gen. m./n. *in(d)*ᴸ / *int*ᴸ,
f. gen. *(in)na*ᴴ; dat. *-(si)n(d)*ᴸ; pl. m. nom. *in(d)*ᴸ, f. *(in)na*ᴴ, gen. *(in)na*ᴺ,
dat. *-(s)naib*. Sandhi: the forms "end in an extra ***d*** when the next word begins in a
vowel, a liquid, *n*, or *f*" (*ind nime*, *ind fir*, *dind ríg*), and "**in an extra *t***
when the next word begins in *s*" (*int sléibe*, *int súil*).
**CONFLICT:** Pokorny restricts this — "The final *-d* of the article remains only **before
vowels or aspirated *f, l, n, r***" [pokorny1914 p.59 §132], i.e. the following *f l n r* must
be lenited; the Wikipedia statement is unqualified.

### 10.5 Name morphology

Three genders (m/f/**n**), three numbers (sg/**dual**/pl), five cases (nom/voc/acc/gen/dat)
[wiki-oi-grammar §Nouns]. **The neuter is gone from Modern Irish** [wiki-irish-declension §lead]
— one of the most visible Old-vs-Modern differences.

Standing syncretisms [wiki-oi-grammar §Nouns]: nom.=voc.=acc. in all neuters, all numbers;
nom.=voc.=acc. dual everywhere; **voc.=acc. plural everywhere**; dat. dual = dat. plural.

**Nominative / genitive / vocative singular, by stem class.** Superscripts = the mutation the
form causes on a following word.

| Class | Nom. sg. | **Gen. sg.** | **Voc. sg.** | Example |
|---|---|---|---|---|
| **o-stem masc.** | *fer* | ***fir***ᴸ (palatalize final C) | ***a fir***ᴸ (= gen.) | *fer / fir / a fir* 'man'; *claideb / claidib*; *ball / boill* |
| **o-stem neut.** | *scél*ᴺ | *scéil, scéuil*ᴸ | = nom. | *scél* 'story'; *cenél / ceníuil* 'kindred' |
| **io-stem masc.** | *céile*ᴴ | *céili*ᴸ | ***a chéili***ᴸ | *céile* 'companion'; *daltae / daltai* 'fosterling' |
| **io-stem neut.** | *cride*ᴺ | *cridi*ᴸ | = nom. | *cride* 'heart' |
| **ā-stem fem.** | *túath*ᴸ | ***túaithe***ᴴ | = nom. | *túath* 'tribe'; *cíall / céille* 'sense' |
| **iā-stem fem.** | *guide*ᴸ | *guide*ᴴ | = nom. | *guide* 'prayer'; *ungae* 'ounce' |
| **ī-stem fem.** | *rígain*ᴸ | *rígnae*ᴴ | = nom. | *rígain* 'queen'; ***Brigit / Brigte*** |
| **i-stem** | *cnáim* (f. *súil*ᴸ) | *cnámo/-a*ᴴ (depalatalize) | = nom., leniting | *cnáim* 'bone'; *súil* 'eye'; *muir* n. 'sea' |
| **u-stem** | *guth* | *gotho/-a*ᴴ | = nom. | *guth* 'voice'; *dorus / doirseo* 'doorway' |
| **velar stem** | *rí*ᴴ | ***ríg*** | = nom. | *rí / ríg* 'king'; **Lugaid / Luigdech**; **Eochu / Echach** |
| **dental stem** | *carae*ᴴ | ***carat*** | = nom. | *carae / carat* 'friend'; *fili / filed* 'poet'; **Núadu / Núadat** |
| **n-stem** | *brithem* | ***brithemon*** | = nom. | *brithem* 'judge'; *ainm / anmae* n. 'name'; **Ériu / Érenn** |
| **r-stem** | *athair* | ***athar*** | = nom. | *athair, máthair, bráthair, siur / sethar* |
| **s-stem neut.** | *nem*ᴺ | ***nime***ᴴ | = nom. | *nem* 'heaven'; *tech / tige* 'house'; *slíab / sléibe* 'mountain' |

[wiki-oi-grammar §§o-/io-/ā-/iā-/ī-/i-/u-/Velar/Dental/n-/r-/s-stems; strachan1909 pp.2–16;
pokorny1914 pp.59–70 §§133–148]

**The vocative rule, stated:** "**The vocative has in the singular the same form as the
nominative, in the plural the same form as the accusative**" — for all consonant stems
[pokorny1914 p.65 §142; strachan1909 p.9 fn.]. **The masculine o-stem and io-stem are the
exceptions**, taking the genitive/palatalized form (< PIE \*-e), which is exactly the modern
*a Sheáin* pattern (§3.5). The particle is **a** (Strachan writes *á*), and it lenites
[pokorny1914 p.8 §12]: *á fir*, *á chéiliu*, *á daltai*, *á chathir*, *á chathracha*.
**Vocative plural = accusative plural** and takes ᴴ: *a firu*, *a chéiliu*, *a chathracha*.

**Indeclinable names** [wiki-oi-grammar §Indeclinable nouns]: "Many names of Biblical figures
(including *Ísu* 'Jesus', *Iohain* 'John', *Duaid* 'David'), ***Patraic* 'Patrick'**, and
several mythical names beginning with the element *da*, such as ***Da Derga***."

**Adjectives.** "**In the positive degree, adjectives agree with nouns in case, gender, and
number.** The other three degrees do not inflect" [wiki-oi-grammar §Adjectives]. Four classes:
o-ā (*bec* 'small': m. gen. *bic*ᴸ, f. nom. *bec*ᴸ, f. gen. *bice*ᴴ, m. voc. *bic*ᴸ),
io-iā (*nue* 'new'), i (*maith* 'good'), u (*follus* 'clear')
[wiki-oi-grammar §Adjective inflection classes; strachan1909 pp.17–19].
**Word order is head-first** — "**the determinans follows the determinatum**… nominal
modifiers such as genitives, descriptive adjectives and relative constructions **follow** the
noun they modify" [utaustin-l1 §2.1]; the adjective's initial is mutated by the noun's
underlying case-ending: *fer becc* (nom.) vs. *fer m-becc* (acc.)
[wiki-oi-grammar §Initial mutations, §Nouns].
**Vocative phrases:** "**When the N. Sg. of a noun is used for V., a qualifying adjective is
also N. Sg.: *a rí már*, 'O great king'**" [strachan1909 p.17 note 2].
**Comparison** is predicative only: equative *-ithir/-idir* (*áthithir*), comparative *-(i)u*
(*sen → siniu*, *ard → ardu*, *brónach → brónchu*, *cumachtach → cumachtchu*), superlative
*-em/-am* (***caín → caínem* 'fairest'**, ***álaind → áildem* 'most beautiful'**)
[wiki-oi-grammar §Degrees of comparison; strachan1909 p.20; pokorny1914 p.72 §154].
Irregulars: *maith : ferr : dech*; *olc : messa : messam*; *már/mór : mó : maam*;
*bec : lugu : luigem*; *trén : tressa : tressam*.

**Compounding — the *Lasairchos* machinery.** Two rules, both stated:
1. **Order is reversed relative to phrasal syntax: modifier first.** "In nominal compounds, such
   as ***énlorg* 'flight of the birds'** and ***énamar* 'singing of the birds'**, the
   VSO-specific syntactical order of modifier and modified element appears **reversed**. Here we
   find **determinans-determinatum**… The explanation is that compounds preserve archaic
   patterns and Irish, like all other ancient Indo-European languages, originally belonged to
   the SOV type" [utaustin-l1 §2.2]. **So Old Irish compounds an epithet the same way Modern
   Irish does — flame+foot, not foot-of-flame — and this is the one place Old Irish word order
   agrees with the modern compound.**
2. **The second element is lenited.** "In the interior of nominal compounds aspiration takes
   place: (a) after nouns, adjectives, and numerals — ***dag-theist* 'a good testimony'**;
   (b) after the prefixes *so-/su-, do-/du-, mí-, neb-/neph-*; (c) after prepositions ending
   originally in a vowel" [pokorny1914 p.8 §16]. Live example: ***énḟlaith*** 'flock of birds'
   = *én* + **lenited** *flaith* [utaustin-l1 glossary].
   **This is exactly the rule §3.6 could not attest for Modern Irish** — so *Lasairchos*'s
   lenited /xosˠ/ has an Old Irish precedent even though the modern sources are silent.
No **composition vowel** is stated as such, but: a prefix's final vowel is dropped before a
vowel (*síar* < *so-íar*, *tadall* < \*to-ad-elnom) [pokorny1914 p.56 §126.4]; the first
element may have a distinct compositional stem (*gu-* for *gáu* in *gú-brithemnacht*)
[pokorny1914 p.43 §111]; syncope operates across the whole compound (*ern-bás* 'death by the
sword' < *íarn* + *bás*) [pokorny1914 p.19 §55 note a]; and quality assimilation is irregular
inside compounds — "**In compound words the assimilation of different-coloured consonants does
not always take place**" (*dagtheist* for expected \*dagthaist) [pokorny1914 p.19 §55.II].
Stress stays initial on the whole compound, with a **late** optional secondary stress on the
second member [pokorny1914 p.17 §52 note; utaustin-l1 §1.2].

**Patronymics.** No source in this directory states the formula as a rule; all of them show it
by example, and the case of the second element is **always the genitive** (consistent with
"nominal modifiers… follow the noun they modify" [utaustin-l1 §2.1]).
- ***mac(c)* 'son' + genitive**: *macc* /mak/, gen. *maicc* (< Ogam *maqqi*)
  [wiki-old-irish §Stops following vowels; wiki-oi-phonhistory §Examples of changes]. Attested:
  **Conchobar mac Nessa**, **Lug mac Ethnenn**, **Sualtaim mac Roich** [utaustin-l1 preamble];
  *Aislinge **Meic Con Glinne*** — showing the genitive of *mac* itself, and *Con* as gen. of
  *cú* [utaustin-intro].
- ***ingen* 'daughter'** /inʲɣʲən/ < Ogam *inigena* [wiki-oi-phonhistory §Examples of changes] —
  attested as a word, **not attested in these sources as a naming formula**.
- ***aue / ua* 'grandson, descendant'**, masc. io-stem: "N. Sg. *aue*, G. *aui*, D. *auu*"
  [strachan1909 p.5 note 1]; "*aue* 'descendant', later *á(u)e*, *ú(a)e*"
  [pokorny1914 p.43 §111]. **No Old Irish *aue*+genitive naming formula is stated** — the
  modern *Ó/Ua* rule [wiki-irish-name §Ó and Mac surnames] is Modern Irish and would have to be
  projected backwards. ***maccu / moccu*: not covered by any source here.**

**Derivational suffixes usable for epithets** [strachan1909 pp.3–4, 12, 16, 20;
pokorny1914 pp.43, 67, 72; wiki-oi-grammar §n-stems]:

| Suffix | Function | Example |
|---|---|---|
| **-ach / -ech** | adjective and noun forming | *brónach* 'sad' (comp. *brónchu*), *cumachtach* 'mighty', *toísech* 'chief, first', *tossach* 'beginning'. Resists u-infection: "adjectives in *-ach* have always *-ach*" [strachan1909 p.3] |
| **-acht** | abstract (ā-stem) | *doínacht* 'manhood', *bendacht* 'blessing', *maldacht* 'curse', *gú-brithemnacht* 'false judgment' |
| **-tu / gen. -tad** | abstract (dental stem) | *bethu* 'life' / *bethad*; *foirbthetu* 'perfection' / *foirbthetad* |
| **-e / -ae** | abstract from adjective (iā-stem) | *lobor* 'weak' → *lobre, lobrae, lobra* 'weakness' |
| **-am / -em** | **agentive** (n-stem) | *brithem* 'judge' / gen. *brithemon*. ⚠️ Homographic with the **superlative** *-em/-am* |
| **-de / -the** | adjective-forming, incl. participles | *colnide* 'carnal', *filetae* 'poetical' |
| **so-/su-, do-/du-, mí-, neb-/neph-** | prefixes: good / bad / mis- / un- — **all leniting** | *mí-thoimtiu* 'a false opinion' |
| **ro-, ru-, der-, ér-, rug-** | intensifiers — all leniting; *ro-* also 'excessively' | *ro-mór* 'very great' |
| **com-** | equative prefix | *commór* 'equally big'; seen in the personal names Gaulish *Comaros*, Old Breton *Commor* [utaustin-intro] |

***-án*, *-ín* and diminutives generally: not covered** by any source in this directory.
"Every adjective may become an adverb by putting the article before the dat. sg. n.":
*in maith* 'well', *a biucc* 'little'; later with *co*: *commaith* [pokorny1914 p.72 §155].

### 10.6 Attested Old Irish personal names

The set actually present in these sources, with genitives where the paradigms give them. This
doubles as a shape template for coining new ones.

**With genitive** [strachan1909 pp.7, 9–15; pokorny1914 p.19; wiki-oi-phonhistory §Examples]:
*Lugaid / **Luigdech*** (velar; Ogam *Lugudeccas*) · *Findubair* f. / *Findubrech* ·
*Ainmire / Ainmirech* · *Cúanu / Cúanach* · *Eochu / Echach* · *Núadu / Núadat* (dental) ·
*Miliucc / Milcon* (n-stem) · *Bricriu / Bricrenn* · *Derdriu* f. / *Derdrenn* ·
*Brigit / Brigte* (ī-stem) · *Anu / Anann* · *Cúalu / Cúalann* · *Tailltiu* f. / *Taillten* ·
*Anblamath / Anfolmithe* (< Primitive Irish *Anavlamattias*) · gen. *Coílbad*
(< *Coillabotas*).

**Territory names, declined identically** [strachan1909 p.15]:
***Ériu* f. 'Ireland' / gen. *Érenn* / dat. *Érinn*** · *Mumu* f. 'Munster' / *Mumen, Muman* ·
*Albu* f. 'Britain, Scotland' / *Alban*. Also *Emain* (*Emain Macha*), *Brega*,
*Slíab Fúait* 'Wooden Hill', *Bruig na Bóinne* [utaustin-l1].

**Without genitive** [utaustin-l1; utaustin-intro; wiki-oi-grammar]:
*Conchobar / Conchubur* · ***Cú Chulainn*, gen. *Con Culainn*** · *Sétanta* ·
*Deichtire / Deichtine* · *Conall* · *Lóegaire* · *Nes(s)a* · *Ulaid* / gen. pl. *Ulad* ·
*Morann / Morainn* · *Bran / Brain* · ***Rónán / Rónáin*** · *Líadain / Líadaine* ·
*Cuirithir* · *Óengus* · *Aldfrith* · *Patraic* (indeclinable) · *Da Derga* (indeclinable).
The language's own name: ***Goídelc*** [ˈɡoːi̯ðʲelɡ] [wiki-old-irish §infobox].

### 10.7 Old Irish → Modern Irish: the correspondence set does not exist in these sources

**This is the largest gap in the whole digest, and it is directly load-bearing for strand 5.**
`bib.md` describes `wiki-oi-phonhistory` as covering "the systematic correspondences between Old
Irish and Modern Irish forms… That correspondence set is what lets strand 5 be generated from
the same Irish lexicon as the other four." **That description is wrong.** The article
"Phonological history of Old Irish" is entirely about **Proto-Celtic / Primitive Irish → Old
Irish**: "Old Irish was affected by a series of phonological changes that radically altered its
appearance **compared with Proto-Celtic**… between 350 and 550 CE" [wiki-oi-phonhistory §lead].
Its sections are Summary of changes, Syncope in detail, Changes to PC stressed short vowels,
PC long vowels and diphthongs, Changes to PC consonants, Initial clusters, Intervocalic
clusters, Examples of changes, Allomorphy. **There is no Old→Modern section.** The single
forward-looking sentence in the file is "This mutation gave rise to the eclipsis mutation in
modern Irish" [wiki-oi-phonhistory §Nasalization].

**Not covered anywhere in this directory:** the fate of Old Irish /θ ð ɣ ṽ/ into Modern Irish;
loss and reduction of unstressed/final syllables between the two stages; final-consonant
treatment; OI *-ach* → Modern *-ach* as a stated correspondence; modern long vowels from
compensatory lengthening outside the fortis-sonorant environment; diphthong development;
mutation-system changes. **OI ~ Modern word pairs are essentially absent** — the only ones on
disk are *bec/becc* ~ *beag*, and the remark that "only ***bráthair* 'brother'** survived into
Modern Irish with its r-stem declension intact" [wiki-oi-grammar §r-stems].

**What IS available to bridge the two stages:**
- **The fortis-sonorant correspondence.** "In the modern language, **the four rhotics have been
  reduced to two in all dialects**"; and "**where reflexes of the Old Irish fortis sonorants
  appear in syllable-final position, they trigger a lengthening or diphthongization of the
  preceding vowel in most dialects**" [wiki-irish-phonology §Fortis and lenis sonorants,
  §Lengthening before fortis sonorants]. This is §4.2 of this digest read backwards: Modern
  *barr* /bˠaːɾˠ/, *ard* /aːɾˠd̪ˠ/, *thall* /haːl̪ˠ/, *ceann* /cəun̪ˠ/ point back to Old Irish
  /R L N/ with a **short** vowel. **The Old Irish minimal pairs are directly usable in both
  directions**: *coll* /koL/ ~ *col* /kol/, *sonn* /soN/ ~ *son* /son/, *rún* ~ *a rún*.
- **The orthographic correspondence.** Modern ⟨bh dh gh mh⟩ ↔ Old Irish **unmarked** ⟨b d g m⟩
  in lenited position; modern ⟨ch ph th sh fh⟩ ↔ Old Irish ⟨ch ph th ṡ ḟ⟩
  [wiki-irish-orthography §Diacritics; utaustin-l1 §1.1]. **This alone converts most of a name's
  spelling between the two stages**, in the direction the generator needs.
- **caol le caol** (§5.1) is the modern regularization of the Old Irish glide-vowel system of
  §10.2.5 — which was **not yet regular**: Pokorny §37 says the intervocalic i-glide is inserted
  "though not regularly" [pokorny1914 p.14 §37].
- **The stress rule is continuous** — initial in both stages outside Munster
  [wiki-old-irish §Stress; wiki-irish-phonology §Stress].

**Recommendation for strand 5:** do not try to derive Old Irish forms from Modern Irish ones
phonologically — the correspondence set to do it is not in this source set, and reconstructing
it from Pokorny's Proto-Celtic→Old-Irish chapter would be running the sound changes backwards,
which is not well-posed. **Instead look each name up in eDIL** (`https://dil.ie/`, free, no bulk
download or API [bib.md §edil]), take the Old Irish headword and its stem class, and inflect it
with §10.5. The 40-odd attested names of §10.6 already cover a usable starting lexicon.

### 10.8 Old Irish CONFLICT summary

1. **Two-way vs. three-way consonant quality** — §10.1 above. Pokorny's three-way system is the
   implementable one for spelling.
2. **Fortis/lenis sonorants** are phonemic in `wiki-old-irish` and `pokorny1914` (§7) but
   **absent from `utaustin-l1`'s chart** [utaustin-l1 §1.1].
3. **Value of lenited *b* and *m***: /v/ and /ṽ/ [wiki-old-irish] vs. /β/ and /β̃/
   [wiki-oi-phonhistory §Table of basic consonant outcomes] vs. lenis *m* = a nasalized
   semivowel [w̃] [wiki-irish-phonology §Fortis and lenis sonorants]. Notational variants of one
   bilabial nasalized continuant.
4. **Broad-consonant notation**: unmarked [wiki-old-irish] vs. ◌ˠ [wiki-irish-phonology]; fortis
   written L N R, or ʟ ɴ ʀ, or (Stifter 2006) Latin *l n r m* fortis vs. Greek *λ ν ρ μ* lenis
   [wiki-irish-phonology §Fortis and lenis sonorants].
5. **⟨aí⟩ vs. ⟨ái⟩.** Pokorny writes ***aí (áe)*** and says so explicitly, "in order to
   distinguish these diphthongs from long *á, ó, ú*, followed by a palatal glide"
   [pokorny1914 p.6 §4]; `wiki-old-irish` agrees. **`utaustin-l1` writes *ái (áe)***
   [utaustin-l1 §1.1] — which on Pokorny's convention means something else. **This matters for
   spelling names.**
6. **The article's final *-d*** — §10.4 above.
7. **`bib.md` mis-describes `wiki-oi-phonhistory`** as covering Old→Modern correspondences —
   §10.7 above.
