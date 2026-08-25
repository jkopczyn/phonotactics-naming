# Claude.ai chat import: phonotactic name-adaptation tool

Source: https://claude.ai/share/094f80f3-0a99-495f-8d7f-57327b07a6a6
Imported 2026-08-24 by scraping the rendered share page. Tool-call details and attachments are collapsed on the share page and are not included.

---

## User

I'm revisiting the topic of a previous conversation; making a tool that can take names/words from one language and apply the phonological constraints and repair of another language to simulate names from a pidgin/creole/contact language between them. I don't know where to get appropriate sources for this. The target languages I know I want to use are Welsh and Arabic; I probably want to use Georgian and Dutch for the other two. Find sources I can use to write rule files for the target languages, which I can then start using to make the rule files and probably code. Freely available is best; purchasable in PDF is second-best. I'll be working with IPA or CLDF/CLTS, so romanization is only an issue if it gets in the way of converting to those formats.

---

## Claude

I'll dig into this. Before searching, one substantive flag on the framing, since it changes which sources are the right ones to hunt for.

What you've described operationally — take words from language X, apply the phonological constraints + repair of language Y — is loanword/adaptation phonology, not creolization. A real pidgin/creole doesn't apply one language's grammar wholesale to another's words; it grows an emergent, simplified phonology (cluster reduction, markedness reduction, regularization) that's typically simpler than either parent. Your description maps cleanly onto borrowing phonology, which is a much better-studied and more computationally tractable target. So the literature I should be finding you is (a) phoneme inventories, (b) phonotactics/syllable structure, and (c) loanword adaptation/repair for each language — with (c) being the part most people skip and the part that actually tells you what the repair does (epenthesis site and vowel quality, which cluster gets simplified, what an absent phoneme maps to). If you later want a creole-flavored result rather than a clean-borrowing result, you'd stack a reduction layer on top rather than relying on one language's repair alone. I'll note that but build the source list around loanword phonology.

Let me find the sources.

Searched the web

Searched the web

Infrastructure confirmed. Now the per-language sources, starting with Georgian (which has the most distinctive phonotactics of your four — those famous harmonic clusters).

Searched the web

Searched the web

Georgian is locked — Butskhrikidze's full dissertation is free. Now Arabic, where I need to flag a decision: "Arabic" isn't one phonotactic system. MSA, Egyptian, Gulf, Levantine, and Maghrebi differ sharply in exactly the things you're modeling — cluster tolerance, epenthesis site, and vowel quality in repair. Let me find the standard reference and the loanword literature.

Searched the web

Searched the web

Watson confirms the dialect split with a concrete example — Egyptian Arabic inserts a vowel between C2 and C3 in a three-consonant cluster, and dialects differ on exactly this. That's the kind of rule you'd encode, and it's why "Arabic" needs pinning down. Now the loanword/repair literature for Arabic.

Searched the web

Searched the web

Arabic literature is rich and confirms the dialect split is exactly where the action is — the classic Broselow finding is that Egyptian Arabic epenthesizes between C2–C3 while Iraqi does it between C1–C2, which is precisely the kind of directional repair rule you'd encode. Now Welsh.

Searched the web

Searched the web

Welsh is well-covered (Hannahs 2013 is the modern standard, same OUP series as Watson; plus a free Wood paper that explicitly treats loanword adaptation). Last language: Dutch.

Searched the web

Searched the web

Dutch is set — Booij (1995) is the standard reference, and there are free companion papers (Nagy on loanword integration, Kager on Dutch phonotactic restrictions). One last search for the general loanword-phonology backbone, since that's the literature that tells you how to model repair as a system rather than ad hoc rules.

Searched the web

Searched the web

I have what you need across all four languages plus the cross-linguistic infrastructure. Before the list, the organizing principle that should shape your rule files:

Three source types, and no single source gives you all three. A rule file needs (1) the inventory (segments + features), (2) the phonotactics (syllable template, licit onsets/codas, cluster co-occurrence), and (3) the repair (what happens to illicit input — epenthesis site and vowel quality, which cluster member deletes, what an absent phoneme maps to). PHOIBLE gives you (1) in exactly your target format and nothing else; LAPSyD gives you a coarse version of (2); the descriptive monographs give you fine-grained (2); and the loanword-adaptation literature is the only place (3) is documented empirically. Most people building something like this stall because they encode (1) and (2) from a grammar and then invent (3) — but repair is the part that's actually attested in the loanword studies, so that's where I've pointed you hardest.

Cross-linguistic infrastructure (use for inventories + a sanity check on syllable structure)

PHOIBLE 2.0 (phoible.org) is your inventory source and it's native to your workflow — it's distributed as a CLDF dataset on GitHub (cldf-datasets/phoible), with per-segment distinctive features and allophone data, and it's queryable via pycldf. Each row represents a single phoneme found in a particular inventory, referencing a language, an inventory, and a segment with features. 
GitHub
 All four of your languages have inventories (Arabic in several varieties). Pair it with CLTS (cldf-clts/clts), which is what lets you map any IPA string to a feature bundle — that's what you'll want for computing nearest-segment substitutions when a source phoneme is absent in the target. Note: PHOIBLE has no phonotactic or syllable-structure data, so it can't tell you what clusters are legal.

LAPSyD (lapsyd.huma-num.fr) fills part of that gap: it covers consonant/vowel inventories, syllable structure, and stress/tone summaries with bibliographic sources, 
Huma-num
 across ~700 languages. Treat it as a quick cross-language reference for maximal syllable shape, not as your detailed phonotactics — for that you need the per-language monographs.

Per-language sources

Georgian — easiest, because the definitive source is free. Butskhrikidze (2002), The Consonant Phonotactics of Georgian (Leiden diss., LOT series) is a full open-access PDF at lotpublications.nl/Documents/063_fulltext.pdf (mirror at pure.mpg.de). Its central finding matters directly for your repair model: Georgian's complex CCC sequences derive from CVCVCV structures via vowel reduction, and the underlying clusters are maximally biconsonantal. 
Academia.edu
 The practical upshot — Georgian tolerates enormous surface clusters, so as a "filter" language it barely repairs at all. That makes it your permissive extreme, a useful contrast against Arabic. For the inventory in prose form, the freely-available Self (n.d.) "OT Analysis of Vowel Syncope in Georgian" (diu.edu) summarizes it: 28 consonants, five vowels /i e a o u/, with a three-way voiced/voiceless/glottalized stop contrast across five places. 
Dallas International University

Welsh — the modern standard is Hannahs (2013), The Phonology of Welsh (OUP, "Phonology of the World's Languages" series). It's the reference for syllabification, phonotactics, the minimal word, and penultimate stress; purchasable, with a substantial Google Books preview — check library/institutional access. For free supplementary material: Wood (1986), "Vowel Quantity and Syllable Structure in Welsh" (swphonetics.com, open PDF) is useful precisely because it discusses how loanword syllable structure gets adapted, and the typological paper "Word-Initial Clusters in Welsh" (ResearchGate) covers cluster phonotactics and the syncope that creates them. Key phonotactic facts for your file: the syllable is broadly (C)(C)V(C), onsets allow obstruent+liquid (/pl pr bl br/) but ban obstruent+nasal (*/pn tn/), and the inventory includes /ɬ χ ð/, voiceless sonorants /m̥ n̥ ŋ̊ r̥/, and (Northern) /ɨ/. Welsh is a moderate-restriction filter, and your source phonemes from Arabic/Georgian will frequently lack a Welsh equivalent, so the substitution component will do a lot of work here. (There's a North/South split — Northern has /ɨ/ — that you may want as a parameter.)

Arabic — the standard reference is Watson (2002), The Phonology and Morphology of Arabic (OUP, same series), purchasable with a good Google Books preview. But Arabic forces a decision you should make explicitly, because the dialects differ in exactly what you're modeling. The classic, citeable contrast: Broselow's work shows Egyptian/Cairene Arabic repairs a three-consonant cluster by epenthesizing between C2 and C3, while Iraqi Arabic epenthesizes between C1 and C2 — and Watson confirms the well-known rule in Egyptian Arabic inserting a vowel between C2 and C3 in a three-consonant sequence. 
ResearchGate
 Same language family, opposite repair rule. For the repair layer there's a body of free/accessible loanword studies: an OT analysis of loanword adaptation in Cairene Arabic and "The Phonotactic Adaptation of English Loanwords in Arabic" (both on academia.edu/ResearchGate, free account), the latter documenting cluster simplification, syllabic-consonant conversion, gemination, and glide insertion in MSA borrowings. 
Academia.edu
 My recommendation, which you should overturn if you have a reason: default to Egyptian/Cairene — it's the best-documented for epenthesis, and the C2–C3 rule is clean to implement. Arabic is your restrictive, epenthesis-heavy extreme.

Dutch — the standard reference is Booij (1995), The Phonology of Dutch (OUP, same series), covering syllable structure, final devoicing, nasal assimilation, and loanword treatment; purchasable, older so often cheaper/more library-available, good Google Books preview. Two directly relevant free companion papers surface on academia.edu (free account): Nagy, "The phonological integration of loanwords in Dutch" (your repair source) and Kager, "Phonotactics as phonology: knowledge of a complex restriction in Dutch." Dutch has permissive clusters and a clean, implementable repair rule in final devoicing (which will affect any voiced-obstruent-final source word), so it sits with Georgian on the permissive side.

The backbone for modeling repair as a system

So your rule files aren't ad hoc, read one orientation piece on adaptation theory. Kang (2011), "Loanword Phonology" (Blackwell Companion to Phonology) is the standard overview and there's a free PDF on her site (yoonjungkang.com/uploads/1/1/6/2/11625099/tbc_100.kang.pdf); a current free alternative is J.L. Smith (2024), "Loanword Phonology" (users.castle.unc.edu/~jlsmith, open PDF). Two things from this literature will save you grief. First, there's a live debate over whether adaptation is driven by the borrower's phonological grammar vs. perception — for a rule-based generator the grammar model is the tractable one, but be aware that's a modeling choice. Second, when your phonotactics underdetermine the output (epenthesis vs. deletion vs. substitution, or which epenthetic vowel), that gap is exactly what the repair literature resolves: Uffmann (2006), for instance, uses a universal markedness hierarchy to predict epenthetic vowel quality. 
Yoonjungkang
 Most of these analyses are framed in OT (markedness + faithfulness constraints, repair = optimal candidate), which you can either implement directly or compile down to ordered rewrite rules.

Two flags worth your attention, treating your language picks as starting points rather than fixed: the Arabic variety decision above is load-bearing and worth settling before you write the Arabic file; and you'll want to decide the direction of adaptation — in a contact scenario between L1 and L2 you can run each language's words through the other's grammar, or designate one as the dominant filter, and that choice changes the output more than any single rule.

Want me to compile this into a markdown bibliography file with the access status and the distinctive-repair note for each, so you've got it alongside the rule files as you build? I can also pull the actual PHOIBLE inventory rows for the four languages into a starter table in your IPA/feature format if that'd be a useful first concrete step.

---

## User

Sure, write that down. If there's any variety of Arabic where there are more-freely-available resources that is more important than the particular variety. I suppose I prefer a MENA dialect to Polynesian but not strongly. In all cases it will be Irish Gaelic providing the vocabulary and the other language applying its rules.

I'll mostly be ignoring the theoretical arguments; I know from experience that linguistics is badly overtheorized, especially where any hints of Universal Grammar (a zombie of a theory, at this point long discredited but still holding on) get into it, as they do in the shorter of the two PDFs. If it's easier to implement a grammar-based tool, that's fine, and I can use it; it's certainly less accurate but I don't care.

---

## Claude

Irish as the source across the board sharpens things: the heavy lifting in every rule file will be the substitution component, because Irish carries a systematic broad/slender (velarized vs. palatalized) contrast on nearly every consonant that none of your four targets have — so each grammar has to decide what to do with slender consonants (depalatalize? render as Cⱼ?), and that decision will shape the output more than cluster repair will. Worth keeping front of mind as you build.

On the theory: agreed that it's separable from what you need, and grammar-based is the right call for a tractable tool. The practical move is to mine the loanword papers for their data tables — the attested source→target mappings — and ignore the OT tableaux and whatever framing sits on top. One small calibration, since you asked me not to just nod along: "long discredited" is stronger than I'd put it — strong nativist UG has genuinely lost ground over the last two decades, but it's contested rather than dead, and generative work still produces real results. None of which matters here, because attested adaptation data doesn't depend on the theory used to explain it.

Let me settle the Arabic variety on your free-resources criterion before writing the file.

Searched the web

Searched the web

Decision on Arabic: Egyptian (Cairene) Arabic. It wins on your stated criterion and your mild preference simultaneously — it's the most-studied Arabic dialect, and as a sedentary variety it has become the de facto standard in much of the Arabic-speaking world 
SciEdupress
 through Egyptian media dominance, so it's squarely MENA-mainstream. More importantly for you, it has the only genuinely open-access loanword-adaptation paper of the four languages — an Égypte/Monde arabe article with concrete attested substitution tables (e.g., /θ/ rendered as /s/ or /t/, as in thermos → /tormos/, and /ʒ/ replaced by /s/ under Coptic substrate influence). 
OpenEdition
 And it's one of Watson's two focus dialects, so the authoritative reference covers it. Cairene also has a couple of quirks that matter for Irish input: it has /g/ rather than /dʒ/, and foreign /q/ is either Egyptianized to /ʔ/ or approximated to /k/. 
Wikipedia

I've written the file with each source tagged by access tier, a phonotactics summary per language, and — since you confirmed Irish as the universal source — a short Irish→target mismatch note for each (the palatalization collapse plus the language-specific gaps). I also folded in a "building blocks → where to get each piece" table up top so it maps directly onto rule-file components.

Created a file, read a file

Created a file, read a file

Two things on the sources you'll hit fast, so they're not surprises: the OUP monographs (Hannahs, Watson, Booij) are the only paywalled pieces, and for those the free loanword papers plus PHOIBLE/LAPSyD will get you most of a working rule file — the monograph mainly sharpens the cluster constraints. And the ResearchGate/academia.edu items need a free account, so they're less frictionless than the OpenEdition and LOT PDFs, which are fully open.

Natural next step: pull the actual PHOIBLE inventories for the four languages into a starter table in your IPA+feature format. The one real decision there is which inventory per language — PHOIBLE has several per language (and several Arabic varieties), so I'd pick the source that best matches the monograph you'll use as the phonotactics backbone (e.g., the Cairene inventory for Egyptian, a Northern or Southern Welsh inventory depending on whether you want /ɨ/). Want me to do that, and if so, North or South for Welsh?

---

## User

Cairene's good, Southern Welsh seems good. Go ahead and pull the PHOIBLE inventories.
And I recognize universal grammar is still contested, but so are many matters of philosophy that were substantively resolved centuries ago. Statistical learning roundly defeated universal grammar both empirically and theoretically, more than twenty years ago, and Chomsky and others refused to listen to it, from some combination of ego and ignorance.

---

## Claude

Pulling the PHOIBLE inventories now — Cairene Arabic, Southern Welsh, Georgian, Dutch.

Ran 2 commands

Ran 2 commands

Good — now I can see the choices. Let me inspect the ambiguous cases (two Egyptian Arabic options, several Dutch standards) and confirm the Welsh vowel set before locking in.

Ran a command

Ran a command

All four are settled, and a couple of nice outcomes:

Welsh has only one PHOIBLE inventory (from Llanwrtyd, a southern-leaning locality), and it confirms its character: the vowels are /a ɑː ɛ eː ɔ oː ɪ iː ʊ uː ə/ + diphthongs with no central /ɨ/ — i.e. it's already Southern. Good.
Georgian has an entry explicitly tagged "Standard/literary Georgian" (28C/5V, the canonical count) — exact match for Butskhrikidze.
Egyptian Arabic has two: an spa one labeled "Egyptian Arabic" but with interdentals /θ ð/, non-marginal /q/, and /p v/ (an MSA-leaning superset), and the upsid one whose actual segments are the cleaner Cairene colloquial set — no interdentals, /q/ marginal, /g/ present, mid-long /eː oː/. The latter matches Watson's Cairene better, so I'm using it (the other is noted as an alternative).
Dutch: PHOIBLE's only "standard" entries are Belgian/Southern standard — worth flagging, since Booij's reference leans Netherlandic.

Let me build the filtered feature table.

Ran a command, read a file

Ran a command, read a file

The CSV is long-format: 153 segments across the four inventories, with all 38 PHOIBLE distinctive features plus the Marginal flag and Allophones, sorted by language and consonants-first. That's the feature matrix you'd compute substitution distances over when an Irish phoneme has no attested mapping in the target.

What's in each, and what it implies for Irish input:

Welsh (Southern), InvID 2406 — 29C/19V. Has /ɬ χ θ ð/, voiceless sonorants /m̥ n̥ ŋ̥ r̥/, the fortis/lenis pairs as /p pʰ, t tʰ, k kʰ/, and /v z d̠ʒ t̠ʃ/ (loan-ish). Notable gap: no /ɣ/ — so Irish broad ⟨dh/gh⟩ has no home and must be repaired (→ /g/, → /χ/, or deleted). Everything else Irish throws at it (/p f v x h/) lands cleanly.

Egyptian Arabic (Cairene), InvID 231 — 27C/8V. Two caveats to read it right: the dental diacritics (/t̪ d̪ s̪ z̪/) are just UPSID's notation for plain coronals — treat them as /t d s z/. And it lists both /ɡ/ and /d̠ʒ/ with /q/ marginal — consistent with Cairene if you take /ɡ/ as the native reflex of ⟨ج⟩ and /d̠ʒ/, /q/ as loan/MSA. It has the emphatics /d̪ˤ s̪ˤ t̪ˤ z̪ˤ/, so the "Irish broad consonant → Arabic emphatic" option I floated has concrete targets. No /p/ (Irish /p/ → /b/), no /v/ (→ /f/); /x ɣ/ → /χ ʁ/.

Georgian, InvID 2183 — 28C/5V. The canonical Standard set: three-way /b·pʰ·pʼ/ etc. across the stops/affricates, /x ɣ/ both present (Irish maps cleanly), no /f/ (Irish /f/ → /pʰ/, or import as loan /f/). Plain Irish voiceless stops naturally map to the aspirated series; the ejectives sit unused as outputs unless you want them.

Dutch (Belgian Standard), InvID 2169 — 22C/15V. The Belgian-standard provenance actually helps you here: it retains voiced /ɣ/ and the /v z/ series, so Irish broad /ɣ/ maps cleanly — the opposite of the Welsh situation. Final devoicing is your main repair. If you'd rather a Netherlandic-flavored inventory you'd be editing this by hand, since PHOIBLE doesn't carry one; and InvID 1050 is the alternative Belgian entry (adds marginal /ɲ ʎ/ and uvular /ʀ/).

If you want, the next concrete step is a draft Irish source inventory (the broad/slender pairs spelled out) plus a first-pass substitution matrix from Irish into each target — that's the piece that turns these tables into actual rule input.

On universal grammar — you asked me not to just nod, so: I think you're right about the direction and overstating the finish. Strong domain-specific UG has genuinely lost its dominance, and statistical/distributional learning is real and well-established — that's not in dispute. But "roundly defeated, empirically and theoretically, twenty years ago" describes a still-live debate as a settled rout. Saffran-style statistical learning (1996) decisively showed the mechanism exists and handles things like word segmentation; its scope — whether it accounts for hierarchical, structure-dependent syntax — is exactly what remains contested, with serious work on both sides (Perfors, Tenenbaum & Regier showed structure-dependence is learnable, but only given a structured hypothesis space, which concedes some prior bias). The honest middle most researchers occupy — domain-general learning over structured representations with some inductive biases — is neither pole, so "statistical learning won" flattens the interesting part.

Two smaller things. The timing is ironic: the strongest empirical pressure on nativism is recent (LLMs acquiring syntax from text alone — Piantadosi's 2023 paper makes that case sharply), not something closed circa 2000, and even that is contested on data-scale grounds. And I won't sign onto "ego and ignorance" — Minimalism's retreat to "Merge plus interface conditions" looks more like the program quietly conceding most of its earlier content than refusing to move, and people hold nativist views for substantive reasons (the logical problem of acquisition, specific island constraints) even where one thinks they're wrong. The philosophy analogy does some quiet work for you there: it treats an empirical question that's still generating new evidence as if it were conceptually settled and merely lingering. None of which touches the tool — the adaptation data stands regardless.

---

