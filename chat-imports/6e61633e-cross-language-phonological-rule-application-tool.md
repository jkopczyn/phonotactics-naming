# Cross-language phonological rule application tool

Source: https://claude.ai/share/6e61633e-c089-4422-a1c1-9683a0e26a99  
Conversation dated 2026-04-17; imported 2026-08-24 from the share-snapshot JSON.

---

## User

I want to create a tool for taking words from one language and apply the phonotactic and phonological rules of another language. Preferably generalizable to multiple target languages. What formats should I look to get for the source words and target-language rules? I assume IPA, but beyond that I don't know.

---

## Claude

IPA is the right starting answer but it's only the surface layer; you'll quickly find it underspecified for the kind of operations you want to do. Here's how the representation problem actually decomposes, with formats and tools that already exist for each layer.

**Source words.** Store canonical forms in Unicode IPA (phonemic, broad transcription — don't pull in fine phonetic detail you don't need). But for actually manipulating segments, you want featural decomposition: each segment becomes a vector over distinctive features like [±voice, ±continuant, ±coronal, ±high]. The library **PanPhon** does exactly this mapping (IPA → feature matrices) and is the de facto Python tool. If you want to accept orthographic input for many languages, **Epitran** handles grapheme-to-phoneme for ~100 languages into IPA. G2P is itself a substantial problem — don't underestimate it if your source is spelling rather than IPA. X-SAMPA is worth knowing as an ASCII-safe IPA encoding but you probably don't need it if you're comfortable with Unicode.

**Target-language rules.** Two traditions:

The classical format is **SPE-style rewrite rules**: `A → B / C _ D` (read: A becomes B between C and D), where A/B/C/D can be segments or feature bundles. This is what linguistics textbooks use and it's readable for humans authoring rule files. The computational implementation of choice is **finite-state transducers** — tools like **foma**, **HFST**, or **XFST** let you write rules in SPE-ish syntax and compile them into FSTs you can run on input strings. Rule ordering matters and FSTs handle it cleanly via composition. This is the most "solved" part of the stack.

The other tradition is **Optimality Theory** (ranked violable constraints), which is better suited to loanword adaptation in principle because nativization is fundamentally about repair of illegal structures. But OT is harder to implement and there isn't a standard off-the-shelf engine the way there is for SPE/FST. For a first version, go rule-based.

**Phonotactics is a separate layer** from segment rewriting, and this is where your framing slightly collapses two things. You actually need at least three components for believable nativization:

1. *Target inventory* — which phonemes exist at all. **PHOIBLE** has inventories for ~3000 languages in a standard format.
2. *Phonotactic constraints* — which sequences are legal. Often expressed as a syllable template (e.g., (C)(C)V(C)(C)) plus constraints on which segments can fill which slots, plus sonority sequencing. Can also be an FST that accepts the legal language.
3. *Repair strategies* — what to do when a source word violates (2). Epenthesis (insert vowel), deletion, substitution to nearest licit segment. This is language-specific and often the most interesting part: Japanese epenthesizes /u/ (or /o/ after coronals), Spanish prothesizes /e/ before /sC/, etc. You'll want to encode these as ordered preferences, and "nearest licit segment" is usually computed as feature-distance — which is why you wanted features in the first place.

**For cross-linguistic generalizability**, the ecosystem to know is **CLDF** (Cross-Linguistic Data Formats) and **CLTS** (Cross-Linguistic Transcription Systems), which standardize how phonological data gets shared. **Lexibank** is a large CLDF-formatted lexical dataset. If you build your tool to ingest CLDF/CLTS-compatible inputs, you get a lot of target languages essentially for free.

**One premise worth questioning.** You described the task as "apply the rules of the target language" to source words. Real loanword adaptation isn't quite that — it's driven by how the *borrower perceives* the source through their native phonology (perceptual assimilation), and the outcomes are often variable rather than deterministic. If you want faithful simulation rather than a stylized transformation, you'll need to think about whether your input is "the source word's phonemes" or "how a speaker of the target language would hear the source word," which are genuinely different. For a stylized/fun tool (English → pseudo-Japanese), deterministic rules are fine. For a linguistically serious tool, you probably want probabilistic output and a perception-side model.

Concrete suggestion for a minimum viable stack: Unicode IPA input → PanPhon features → foma/HFST for SPE-style target-language rules → a phonotactic FST + feature-distance repair for illegal sequences → IPA output. Author rules as text files per target language so adding a language is a data task, not a code task.

---

## User

I'm not looking for enormously serious, but I'd like it to be realistic. The case is for a conlang, a contact language between an underlying substrate (Irish Gaelic) and another language representing a divergent culture. (In fact, several languages, each for a different divergent culture.) I only intend to use this as a 'naming language' where I have minimal grammar; taking existing names (Ciara /ˈkɪə.ɾˠə/) , descriptions (Matánach 'Burly' /ˈmˠat̪ˠɑːnˠəx/), and possibly epithets (Lasairchos 'Flamefoot' /ˈl̪ˠɑsˠəɾʲxosˠ/) (where epithets may take a little grammar). Probabilistic output probably fails cost/benefit analysis but aspects of a perception-side model might be worthwhile.
Anything that I'd need to supply for that, that I won't find in Lexibank, PHOIBLE, or the suggested Python libraries?

---

## Claude

Short answer: the databases and libraries give you inventories and featural machinery; none of them give you the rules, which are the part that does the actual work. For a designed contact language you're inventing the rules anyway, so the missing-data problem and the worldbuilding problem are the same problem.

Per contact language, you'll need to author:

**Phonotactics.** PHOIBLE stops at segments. You need syllable templates, cluster restrictions, coda constraints, hiatus rules, any prohibited sequences. Usually fits on a page.

**Adaptation mappings.** Source → target substitutions where the source segment isn't in the target, or is legal-but-dispreferred. Feature-distance gives you a reasonable default ("nearest licit segment") but real nativizations have idiosyncratic quirks worth hand-authoring — French /y/ goes to English /ju/ rather than the featurally-closer /u/ or /i/, for instance. A handful of these per language (5–15) is what makes output feel language-specific rather than generic. This is also where a lightweight perception model lives: weight features manually per culture (a language with no voicing contrast weights [voice] near zero, collapsing /p b/ → /p/), and encode the asymmetric mappings explicitly.

**Repair strategies.** For each violation type: epenthesis, deletion, or substitution? With what vowel, in what position, under what conditions? Japanese inserts /u/ (or /o/ after coronals); Spanish prothesizes /e/ before /sC/; Irish has productive epenthesis between sonorants. Ordered preferences per language.

**Stress and prosody.** Not in any of the resources. Assignment rule (initial / penult / weight-sensitive) plus quantity handling if vowel length matters — it does in Irish.

**Sonority scale and syllabification.** Maximal Onset is standard but you implement it; sonority values are derivable from features but you should fix a scale up front.

**Orthography.** If outputs should be in a readable romanization rather than IPA, that's another mapping per target going the other direction. For a naming tool this is probably non-optional.

**Irish-specific things to budget for:**

The broad/slender distinction is the one that will bite you. Your examples mark it correctly with /ʲ/ and /ˠ/ diacritics, but PanPhon handles palatalization cleanly and velarization less so — you may need to extend the feature set or track secondary articulation as a parallel feature alongside the base segment. How each contact language treats the distinction (preserve? collapse? reinterpret as coloring of the adjacent vowel?) is one of the more interesting design decisions per culture and probably worth deciding deliberately rather than letting fall out of defaults.

For epithets: Irish genitive formation, adjective agreement, and initial mutations (lenition, eclipsis) aren't phonology proper, but mutations specifically *are* phonological and should live in the rule system. You can hardcode templates for the morphology itself rather than building an analyzer.

**One framing check.** "Contact language between Irish substrate and another language" is genuinely ambiguous. Reading A: the output sits in a contact language with Irish-shaped phonotactics partially overlaid by the superstrate's features, and you're running Irish-source names through that. Reading B: the output is in the superstrate language as spoken by Irish-substrate speakers, which would emphasize substrate interference rather than target-language nativization. The rule sets look pretty different. Different divergent cultures could plausibly sit at different points on that spectrum, so it's worth being explicit per language rather than picking one mode globally.

---

## User

I'm not looking for *original* rules, or complex modeling, I'm looking for the rules of the real languages I'm using. I don't expect to do much to change those rules for the conlang, though I might slightly modify the phonemic inventory if there's a very common source sound that's forbidden in the target.

For example, one of these will be between Gaelic and Arabic; I'd want to take Gaelic vocabulary and apply Arabic phonological constraints, phonemic inventory, and repair, and potentially rules about the endings needed for nouns/adjectives/etc. (I haven't picked which Arabic; I'm aware this will have a fairly significant effect.) Gaelic will be approximately the lexifier/superstrate providing the vocabulary, and Arabic (or another language) will be approximately the substrate, providing the phonological rules. I want to get appropriate rules without in-depth study of Arabic, since I'll be doing this three or more times.

---

## Claude

The frank answer is that there's no repository of formalized phonological rule sets for real languages. PHOIBLE gives inventories, WALS gives typological features, but neither gives you "here are Arabic's syllable templates and repair strategies in a format you can compile." That piece doesn't exist in machine-readable form for the languages you'd want. You'll read a grammar chapter or two and transcribe 20–50 rules into your rule file per language. For a naming tool that's a weekend per language, not more.

The closest thing to what you actually want is **WOLD** (World Loanword Database, wold.clld.org), which documents loanwords in ~40 recipient languages with source forms alongside adapted forms. Check which of your targets are covered — reading through the entries tells you more about how a language nativizes in practice than any theoretical description, because it shows you the mappings directly. Pair it with **Haspelmath & Tadmor's *Loanwords in the World's Languages*** (2009), the companion volume with per-language chapters on adaptation strategies.

For the phonology proper of each target, the efficient stack is:

- **Wikipedia's "[Language] phonology" page** for a first pass — for major languages these are well-sourced and give you inventory, syllable structure, and stress in twenty minutes.
- **One reference grammar** for the things Wikipedia is thin on (repair strategies, allomorphy, morphological templates). For MSA: Ryding's *Reference Grammar of Modern Standard Arabic*, or Watson's *The Phonology and Morphology of Arabic*. For dialects, the Routledge descriptive-grammar series.
- **WOLD data** as the ground-truth check.

For Arabic specifically, the variety question matters less than you might think for the phonotactic envelope: all varieties share CV / CVC / CVCC syllables, ban onset clusters, handle foreign clusters via /i/-epenthesis, and convert /p/→/b/ and /v/→/f/. What varies is a handful of segmental choices (/q/ vs /ʔ/ vs /g/, /dʒ/ vs /g/ vs /ʒ/, presence of interdentals) and some stress rules. Pick a variety, note the 5–10 segmental choices that matter, move on. The pharyngeals and emphatics — where Gaelic→Arabic will look most distinctive — are stable across varieties.

On morphology for your naming/epithet use case, Arabic has cheap wins. The **nisba** suffix /-iyy/ (m.) / /-iyya/ (f.) derives adjectives from nouns and is productive and recognizable — ideal for epithets. The **feminine ending** /-a(h)/ marks feminine nouns. The **definite article** /al-/ with sun-letter assimilation gives you another distinctive marker. You can get most of the "sounds Arabic" effect from those three alone, without touching case, broken plurals, or root-and-pattern derivation (which you can't cleanly apply to Gaelic roots anyway without inventing a root-extraction step, and that's a project).

One pragmatic accelerator: the grammar-chapter-to-rule-file step is exactly the kind of task an LLM is decent at — feed it the relevant sections of a reference grammar and ask for an SPE-formatted rule list, then verify against WOLD examples. It won't be perfect and you'll need to catch errors, but it's faster than doing it from scratch, and the verification step catches most hallucinations. This scales your "three or more times" concern from weeks to days.

---

## User

I suspected LLMs might be good at that. Would you suggest Claude Code, ordinary chat, or research mode? Or should I be doing something specific with the API?

---

## Claude

*[tool_use: view]*

*[tool_result: view]*

For your workflow, the two halves of the task map to different tools.

**Rule extraction from grammar chapters: ordinary chat, with Projects.** This is a document-transformation task. Upload PDFs of the relevant grammar chapters and work through them interactively — you'll want to iterate on the rule format, spot-check outputs against WOLD entries, and ask follow-ups when a rule is ambiguous in the source. None of that benefits from automation. Projects is genuinely useful here: put your rule-file schema, any example rule file from a previously-done language, a PHOIBLE inventory dump for the target, and the grammar PDFs in one Project. Each new language extraction then starts with all your conventions already loaded, which is most of what makes the output consistent across the three languages.

Skip research mode. It's built for open-ended web research across many sources; you have specific chapters from specific books, and breadth isn't the problem. It would probably pull in tangential web content and dilute the extraction.

**Building the tool itself: Claude Code.** Once you're writing the Python pipeline — PanPhon feature lookups, a rule interpreter or foma bindings, the syllabification and repair logic, test harnesses — Claude Code is meaningfully better than chat. It can run your rules against test words, see what breaks, and iterate without you copying code back and forth. The rule-interpreter-and-test-harness loop in particular is where it pays off: you supply "Ciara should come out as X in the Arabic-contact language," it runs the pipeline, adjusts, re-runs.

**API: probably not worth it** for a three-language project. The one case where it might earn its place is batch-verification — if you want to run every WOLD entry for your target language through your pipeline and diff against the attested adaptations, that's a few hundred calls and the API makes it clean. But you can also just do it in a script that calls Claude Code, or do smaller batches in chat.

One practical note regardless of interface: hallucination rate on linguistic detail drops sharply when you supply the actual source text rather than asking from memory. Upload the grammar chapter; don't ask "what are Levantine Arabic's syllable constraints" cold. The verification-against-WOLD step catches the rest.

---

