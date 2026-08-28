#!/usr/bin/env python3
"""Extract Butskhrikidze's consonant-sequence lists from `sources/georgian/digest.md` (plan Task
23b, R29). The digest transcribes them as prose in HER notation (digest §2.0, table (1) p.77);
this script turns that prose back into IPA clusters so the `onsets` / `codas` whitelists of
`rules/georgian.rules` are reproducible and reviewable.

Sources read, by digest section (line ranges are located by heading, not hard-coded):

  onsets  §2.2  table (53) [butskhrikidze2002 p.103] — the bold harmonic clusters (30; the
                italic `zg` / `žg` are the S8 gaps and are skipped)
          §2.3  Appendix 2 [butskhrikidze2002 pp.197–205] — stem-initial CC (by manner class),
                CCC (table a–z), CCCC, CCCCC, CCCCCC
          §2.5  the "attested stem-initially but not stem-finally" set [p.207]
          §2.6  table (62) [butskhrikidze2002 p.110] — the attested initial CC grid
  codas   §2.5  Appendix 3 [butskhrikidze2002 pp.207–209] — stem-final CC (harmonic,
                obstruent+sonorant, sonorant+obstruent, loan-only obstruent), CCC, CCCC, CCCCC.
                The "attested in neither position" set is excluded.

Her notation -> this project's canonical IPA (digest §2.0; I-34): aspiration is unwritten
(`t p k c č` = /tʰ pʰ kʰ ts tʃʰ/ — `c` maps to the chart's `ts`, features.csv has no tsʰ row),
`j` = /dz/, `ǰ` = /dʒ/, `γ` = /ɣ/, `χ'` = /qʼ/, `x` = /x/, `g` = /ɡ/ (U+0261). Table (62)
writes /dz/ as `ʒ` (the Caucasianist convention; her `ž` /ʒ/ is separate).

Usage:
    extract_georgian_clusters.py sources/georgian/digest.md              # bare clusters
    extract_georgian_clusters.py sources/georgian/digest.md --sections   # "onset\\tCL" / "coda\\tCL"
Output order is deterministic (file order, first occurrence).
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

# Her symbols, longest first (digest §2.0 table (1)); `ʒ` is table (62)'s /dz/.
SYMBOLS: dict[str, str] = {
    "t'": "tʼ", "k'": "kʼ", "p'": "pʼ", "c'": "tsʼ", "č'": "tʃʼ", "χ'": "qʼ",
    "b": "b", "g": "ɡ", "d": "d", "v": "v", "z": "z", "t": "tʰ", "k": "kʰ", "l": "l",
    "m": "m", "n": "n", "p": "pʰ", "ž": "ʒ", "r": "r", "s": "s", "γ": "ɣ", "š": "ʃ",
    "c": "ts", "č": "tʃʰ", "j": "dz", "x": "x", "ǰ": "dʒ", "h": "h", "ʒ": "dz",
}
_ORDER = sorted(SYMBOLS, key=len, reverse=True)


def to_ipa(token: str) -> str | None:
    """Greedy longest-match over her symbol set; None when any character is foreign."""
    out: list[str] = []
    i = 0
    while i < len(token):
        for sym in _ORDER:
            if token.startswith(sym, i):
                out.append(SYMBOLS[sym])
                i += len(sym)
                break
        else:
            return None
    return "".join(out)


_ITALIC = re.compile(r"\*[^*\s][^*]*\*")          # *example*  (never `* (Fr.) ... *`)
_GLOSS = re.compile(r"(?<!\S)'[^']*'(?!\S)")       # 'gloss'  — not the ' of t'k'
_BRACKET = re.compile(r"\[[^\]]*\]")
_CODE = re.compile(r"`[^`]*`")


def clusters_in(text: str) -> list[str]:
    """Cluster tokens (>= 2 segments) left in a prose fragment once examples, glosses,
    citations, code spans and markup are removed. Parentheses become separators."""
    text = text.replace("**", " ")                 # bold first, or `**x**` reads as italic
    text = _ITALIC.sub(" ", text)
    text = _GLOSS.sub(" ", text)
    text = _BRACKET.sub(" ", text)
    text = _CODE.sub(" ", text)
    text = text.replace("†", " ")
    text = re.sub(r"[();:,—–]", " ", text)
    out: list[str] = []
    for tok in text.split():
        ipa = to_ipa(tok)
        if ipa is None or len(tok.replace("'", "")) < 2:
            continue
        if ipa not in out:
            out.append(ipa)
    return out


def section(lines: list[str], start: str, stop: str) -> list[str]:
    a = next(i for i, l in enumerate(lines) if l.startswith(start))
    b = next(i for i, l in enumerate(lines) if i > a and l.startswith(stop))
    return lines[a:b]


def harmonic(lines: list[str]) -> list[str]:
    """§2.2 table (53): bold cells only (italic zg/žg are the S8 gaps)."""
    out: list[str] = []
    for line in section(lines, "### 2.2", "### 2.3"):
        if not line.startswith("|"):
            continue
        for cell in re.findall(r"\*\*([^*]+)\*\*", line):
            ipa = to_ipa(cell.strip())
            if ipa and ipa not in out:
                out.append(ipa)
    return out


def appendix_2(lines: list[str]) -> list[str]:
    """§2.3: the bullets (CC), the a)–z) table (CCC), the CCCC paragraph, the five/six lines."""
    out: list[str] = []
    block = section(lines, "### 2.3", "### 2.4")
    text = "\n".join(block)
    # bullets: "- **class** — clusters ..." up to the next bullet / blank line
    for m in re.finditer(r"^- \*\*[^*]+\*\* — (.*?)(?=^\s*$|^- \*\*|\Z)", text, re.S | re.M):
        for c in clusters_in(m.group(1)):
            if c not in out:
                out.append(c)
    # table rows: "| a) label | seq *ex* 'gloss'; ... |"
    for line in block:
        if re.match(r"\| [a-z]\) ", line):
            cell = line.rstrip().rstrip("|").rsplit("|", 1)[1]
            for c in clusters_in(cell):
                if c not in out:
                    out.append(c)
    # four-member paragraph and the five/six-member lines
    m = re.search(r"\*\*Four-member \(CCCC\)\*\*(.*?)^\s*$", text, re.S | re.M)
    for c in clusters_in(m.group(1)):
        if c not in out:
            out.append(c)
    for m in re.finditer(r"^\*\*(?:Five|Six)-member \([C]+\)\*\*:(.*)$", text, re.M):
        for c in clusters_in(m.group(1)):
            if c not in out:
                out.append(c)
    return out


def appendix_3(lines: list[str]) -> tuple[list[str], list[str]]:
    """§2.5: (stem-final codas, the initial-only set). Bullets whose label says 'neither'
    are dropped; the 'stem-initially but not stem-finally' bullet goes to the onsets."""
    codas: list[str] = []
    initial_only: list[str] = []
    block = section(lines, "### 2.5", "### 2.6")
    text = "\n".join(block)
    bullets = re.findall(r"^- (.*?)(?=^- |^\s*$|\Z)", text, re.S | re.M)
    for b in bullets:
        head = b.split(":", 1)[0]
        if "neither" in head:
            continue
        body = b.split(":", 1)[1] if ":" in b else b
        if "stem-**initially" in head or "stem-initially" in head:
            initial_only.extend(c for c in clusters_in(body) if c not in initial_only)
            continue
        if "CONFLICT" in b:
            body = b.split("`CONFLICT:`", 1)[0].split(":", 1)[1]
        for c in clusters_in(body):
            if c not in codas:
                codas.append(c)
    for label in ("Three-member, stem-final", "Four-member", "Five-member"):
        m = re.search(r"\*\*" + re.escape(label) + r"\*\*(.*?)(?=^\*\*|^\s*$|^###)",
                      text, re.S | re.M)
        for c in clusters_in(m.group(1)):
            if c not in codas:
                codas.append(c)
    return codas, initial_only


def grid_62(lines: list[str]) -> list[str]:
    """§2.6 table (62): rows `| C1 | C2 C2 ... |`."""
    out: list[str] = []
    block = section(lines, "**Attested initial CC grid**", "Her reading")
    for line in block:
        m = re.match(r"^\| ([^|]+) \| ([^|]+) \|", line)
        if not m or m.group(1).strip() in ("C1", "---"):
            continue
        c1 = to_ipa(m.group(1).strip())
        if c1 is None:
            continue
        for c2 in m.group(2).split():
            ipa2 = to_ipa(c2)
            if ipa2 and c1 + ipa2 not in out:
                out.append(c1 + ipa2)
    return out


def extract(path: Path) -> tuple[list[str], list[str]]:
    lines = unicodedata.normalize("NFC", path.read_text(encoding="utf-8")).splitlines()
    onsets: list[str] = []
    codas, initial_only = appendix_3(lines)
    for src in (harmonic(lines), appendix_2(lines), initial_only, grid_62(lines)):
        for c in src:
            if c not in onsets:
                onsets.append(c)
    return onsets, codas


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    onsets, codas = extract(Path(argv[0]))
    if "--sections" in argv[1:]:
        for c in onsets:
            print(f"onset\t{c}")
        for c in codas:
            print(f"coda\t{c}")
    elif "--rules" in argv[1:]:
        print("onsets = " + " ".join(onsets))
        print("codas  = " + " ".join(codas))
    else:
        print(" ".join(onsets + [c for c in codas if c not in onsets]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
