# Creating a harsh-sounding conlang from Irish Gaelic

Source: https://claude.ai/share/2f456675-b322-4a5e-a3f4-72545a7be87c  
Conversation dated 2026-06-01; imported 2026-08-24 from the share-snapshot JSON.

---

## User

If I want to make a naming language conlang, where I want it to take a source language (Irish Gaelic) and apply a foreign language's phonological constraints and repair strategies, and I'd like it to sound 'harsh' or 'evil' to a modern English-speaking ear (like Tolkien's Black Speech), what are the most appropriate real languages to use for the phonology?

---

## Claude

A few corrections to the framing first, because they change the answer.

"Evil-sounding" isn't a property a language has; it's the product of two things in an English listener's head: sounds English *lacks* (so they register as foreign and effortful — gutturals, ejectives, uvulars), and sounds tied to historical screen-villain cultures (German, Russian, Arabic — coding, not phonetics). Tolkien's Black Speech works largely by *contrast*: it's harsh because Quenya and Sindarin, sitting right next to it, are mellifluous (he built those on Finnish and Welsh). He engineered the harshness; he didn't lift it from one donor. So the question "which real language is the harsh one" has a slightly false bottom — the currency is *features*, and the effect depends on what you're contrasting against.

The more important correction is mechanical. Several languages with a "harsh" reputation have phonotactics that would *smooth Irish out*, not roughen it. Arabic is the clearest trap: it sounds guttural, but its syllable structure is fairly restrictive, so applying its constraints and repairs to Irish would tend to *epenthesize vowels into clusters* and break them up. You'd gain some uvular/pharyngeal color but lose the clotted-consonant quality that reads as harsh. So you should pick the donor by *which direction its repair strategies push* — toward clustering or away from it — not by its reputation.

The actual harshness levers, donor-independent:
- Back fricatives [x χ ʁ ɣ] and uvular stop/trill [q ʀ]
- Pharyngeals/emphatics [ħ ʕ] and ejectives/glottalization [pʼ tʼ kʼ qʼ]
- Lateral affricate/fricative [t͡ɬ ɬ]
- Heavy obstruent clusters, especially word-final, and lots of [z ʒ] (Tolkien leaned on z hard: *Nazgûl, Burzum, Lugbúrz*)
- Dark vowels (a o u), suppression of front/high vowels and light diphthongs
- Final-obstruent devoicing for a clipped, bitten-off feel; geminates; strong trilled r

Given that "push toward clustering + substitute in alien consonants" is the goal, the best donors are:

The **Northwest Caucasian** languages (Kabardian, Abkhaz, the extinct Ubykh) and **Georgian** (Kartvelian). These are the strongest fit, and not for their reputation — for their mechanics. Their phonotactics *permit and encourage* large consonant clusters, and their inventories let your repair rules *substitute* Irish plain stops with ejectives and back Irish articulations toward uvulars. The repairs roughen rather than smooth. They're also brutal to actually speak, but for a *naming* language that's irrelevant — you only need the output strings, never a conversation. This is the rare case where the hardest languages are the easiest to use.

**Pacific Northwest** languages (Tlingit, or Nuxalk if you want the famous vowelless words) are a strong alternative flavor: ejectives and uvulars again, plus the lateral affricate [t͡ɬ], which is maximally alien to English and not yet a fantasy cliché.

**Arabic/Hebrew** give you excellent gutturals and emphatics, but with the cluster-breaking caveat above, and with a real cultural-coding problem (below).

**Slavic** (Polish/Czech for clusters, Russian for the [x] and the Cold-War halo) and **German/Dutch** (the hard [x] of *loch*/*Gogh*, final devoicing) work, but here the harshness is substantially stereotype rather than phonetic strangeness, and the coding is heavy-handed.

Now the Irish-specific point, which I think is the most useful thing here. Irish is a good source partly because it already *contains* harsh material: broad (velarized) consonants, a real [x] (broad *ch*), [ɣ] (broad *dh/gh*), and a strong trilled r in several dialects. What makes Irish sound *soft* to English ears is the slender (palatalized) series, the lighter lenition outcomes ([v w j h]), and front vowels. So your filter's job is mostly subtractive: collapse the broad/slender contrast toward broad/velarized-uvular, route all lenition to the back fricatives instead of the soft ones, and back the vowels. De-palatalization is itself a harshening repair. *Niamh* /nʲiəv/ and *Aoife* /iːfʲə/ are soft precisely because they're slender and front; strip the palatalization, back the vowels, harden the final fricative, and you're well on your way without importing anything exotic. (Illustrative, not a rule: *Gráinne* → uvular onset, ejective, lost slender, hardened coda — something like *Qʼraːʁn*.)

This suggests a cleaner method than "adopt a donor wholesale": extract a *feature filter* (de-palatalize, uvularize, ejectivize plain stops, cluster-preserving repairs, dark vowels) rather than committing to one language's full grammar. It avoids the trap where the donor's own phonotactics fight your goal.

One real critique you asked for implicitly by invoking Tolkien: using a living, ethnically-identified language as your designated "evil" donor reproduces exactly the orientalist coding Tolkien gets criticized for (Haradrim, Easterlings). "Arabic = the evil tongue" lands very differently from "ejectives and uvulars = the evil tongue." Extracting abstract features, or leaning on a feature set rather than a flag, sidesteps that and is also better craft — it's less traceable and more distinctively yours.

If you tell me your actual phoneme inventory target and how aggressive you want the repairs, I can draft the substitution-and-repair ruleset and run a batch of Irish names through it.

---

## User

I'm ultimately going to make a tool for this - I'm using several other languages. The conceit is that there are five strands of a culture, which have split apart and drifted in different directions. To make them still feel related, they will all use Gaelic as a basis. To make them sound different, they will have four different target languages. (The fifth will use Old Gaelic rather than modern Gaelic.) Arabic and Welsh are the two already pinned down, a third I have some options I'm weighing, and the fourth has the constraint of an existing set of proper names that share few features other than looking and sounding foreign and evil (Tchaeul, Th'tysh, Kas'queil, Xelxyx, Ysclyth, etc.)  and being the most alien, violent, and sadistic of the five strands.
I don't care about the cultural associations; I don't think anyone but *maybe* my beta readers will even know which language I'm using. It just has to produce an appropriate reaction in the audience, while being something that can be written so an English-speaking audience can pronounce it approximately correctly. And for that I need a target language I can get phonological rules for, that matches the 'hostile and alien' first impression.

---

## Claude

Your premise that the five names "share few features" undersells them — they're more consistent than you think, and that's good news, because it means there's a coherent phonology to target rather than a grab-bag to rationalize. Reverse-engineering the set:

- Voiceless obstruents dominate completely. θ (th), ʃ (sh), tʃ (tch), k/c, s, q, x. There's not a single voiced stop or fricative across all five — no b, d, g, v, z — and no nasals at all (no m, n in the sample).
- Apostrophes break consonant sequences (Th'tysh, Kas'queil). To anyone who reads linguistic romanization, that's ejective marking; to a lay English reader, it's a glottal stop/pause. Both readings land as "harsh interruption."
- Back articulations: uvular q (queil), velar x. Articulated toward the back of the mouth, which is most of where the "guttural" impression comes from.
- Heavy clusters in both onset and coda: scl- (Ysclyth), the x-bracketing of Xelxyx, -lth, -sh codas.
- Y as a lax central/high vowel; otherwise short, non-bright vowels; every word ends on a consonant (clipped, no open syllables).

That signature — voiceless + ejective/glottal + uvular + cluster-tolerant — points squarely at one phonological family: the **Caucasian** languages, or secondarily the **Mayan** ones. Which to pick depends on which feature of your existing names you want to treat as load-bearing.

If the **clusters** are the priority (Xelxyx and Ysclyth are doing the heavy lifting), use **Georgian (Kartvelian)**. It's by far the best-documented language that tolerates the monstrous onset clusters you'd need, it has the uvular q, the voiceless affricates (your *tch*), ejectives (your apostrophes), and /x/ (your *x*). Phonotactics and rules are well published. The catch is that Georgian uses its own script, so transliteration conventions vary and you'll be designing the romanization yourself.

If the **apostrophe-ejectives** are the priority and you care about your third constraint — English-approximable spelling — use a **Mayan** language (K'iche' or Yucatec). This is the sleeper pick. Ejective-rich phonology, but with a *standard, ready-made apostrophe romanization* (K'iche', Tz'utujil, Xibalba), which matches your existing names' look exactly and is the closest thing to English-pronounceable in this space, because the apostrophe-as-pause is already an instinct English readers have from decades of fantasy names. It has x (= ʃ), tz, ch, and q built in. It clusters less aggressively than Georgian, so Ysclyth-density would be slightly off-signature, but everything else fits and the documentation is excellent. Bonus that's irrelevant to you but pleasing: Xibalba, the Maya underworld, literally means "place of fear."

If you just want it the **harshest possible** and don't mind sparse sourcing, **Northwest Caucasian** (Kabardian, or extinct Ubykh) is the extreme end — more consonants and bigger clusters than anything else on Earth — but rules are hard to find and the romanization is rough going.

The argument for any of these over, say, a Slavic option is contrast across your four targets. Arabic *smooths* clusters (its repairs epenthesize vowels to break them up), and Welsh is fairly euphonious despite its reputation. Neither does ejectives. So putting ejectives + maximal clustering on the fourth strand makes it phonologically the opposite of Arabic and clearly distinct from Welsh — the harshness is structural, not just a vibe, which is what you want for "most alien and violent."

One collision warning, and it's the real critique of the existing set: Xelxyx and Ysclyth read distinctly pseudo-Welsh (the y-vowel, the x, the scl cluster), and Welsh is your *other* pinned strand. If the fourth is supposed to be maximally distinct, I'd pull its romanization deliberately away from Welsh territory — lean on apostrophe-ejectives (C'), uvular q, and -kh/-x codas, and ration the y-vowel — so a reader doesn't subconsciously file it next to the Welsh strand. Your two most cluster-heavy names are the two most likely to muddy that line.

For the tool itself, the useful move is to extract that signature as an explicit feature filter (devoice everything, delete nasals or make them rare, route Irish lenition to back fricatives, ejectivize plain stops, uvularize velars before back vowels, preserve clusters rather than repairing them, force consonant-final words) rather than importing one donor's whole grammar — same logic as before, and it keeps the four filters cleanly separable in code.

If you want, tell me which of the three you're leaning toward and I'll draft the actual substitution-and-repair ruleset for the Gaelic→target filter and run your name set plus a batch of Irish names through it so you can see whether the output sits alongside Tchaeul and Xelxyx convincingly. I can also weigh in on the third strand — the main thing there is to make sure it occupies a different corner of feature-space than these three (e.g. nasal-heavy or vowel-harmony-driven rather than another obstruent-cluster language) so all four read as distinct.

---

