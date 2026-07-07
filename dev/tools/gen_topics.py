#!/usr/bin/env python3
"""Generate topics.json from statement-semantics.md + tools/lexicon.json.

Router / lexical index for the interpret + code task bundles (see ../APP-DEV-GUIDE.md).

  * topic index: reads the <a id="..."></a> anchors and ## headings in
    statement-semantics.md, derives each topic's 1-based inclusive line range and first
    br_tree cross-reference, and joins the curated routing-keyword sets.
  * lexicon: loads the frozen, hand-owned classified inventory in tools/lexicon.json
    (counts recomputed here). The one hard fact for lexical analysis: only system
    functions (table6k u table7k) are reserved against variable names;
    statement/clause/command keywords are positional.

Fully self-contained within context/dev/ — no ../lsp/ dependency.
Run from anywhere:  python tools/gen_topics.py
"""
import io, os, re, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.dirname(HERE)                      # context/dev
sem_path = os.path.join(DEV, "statement-semantics.md")
out_path = os.path.join(DEV, "topics.json")
lex_path = os.path.join(HERE, "lexicon.json")

# Curated: id -> routing keywords. Absent id => kind "reference".
META = {
    "open-file": ["OPEN"], "read": ["READ"],
    "reread": ["REREAD"], "write": ["WRITE"],
    "rewrite": ["REWRITE"], "delete": ["DELETE"],
    "restore": ["RESTORE"], "close": ["CLOSE"],
    "form": ["FORM"], "sort": ["SORT"],
    "index": ["INDEX"],
    "database": ["OPEN SQL", "CONFIG DATABASE", "DATABASE"],
    "print": ["PRINT"], "input": ["INPUT", "LINPUT"],
    "open-serial": ["OPEN", "BAUD"],
    "display-menu": ["DISPLAY MENU", "INPUT MENU"],
    "open-window": ["OPEN"], "print-fields": ["PRINT FIELDS"],
    "input-fields": ["INPUT FIELDS"],
    "rinput-fields": ["RINPUT FIELDS", "RINPUT"],
    "input-select": ["INPUT SELECT", "RINPUT SELECT"],
    "grid-list-text": ["GRID", "LIST", "TEXT"],
    "screen-controls": ["COMBO", "RADIO", "CHECK"],
    "option": ["OPTION"], "dim": ["DIM"],
    "let": ["LET"], "forced-assignment": [":="],
    "mat": ["MAT"], "substring-assignment": [],
    "data-read-restore": ["DATA", "READ", "RESTORE"],
    "if-then-else": ["IF", "THEN", "ELSE", "END IF"],
    "goto": ["GOTO"], "on-goto-gosub": ["ON GOTO", "ON GOSUB"],
    "randomize": ["RANDOMIZE"],
    "stop-end-pause-chain": ["STOP", "END", "PAUSE", "CHAIN"],
    "for-next": ["FOR", "NEXT"], "do-loop": ["DO", "LOOP", "EXIT DO"],
    "gosub-return": ["GOSUB", "RETURN"], "exit": ["EXIT"],
    "execute": ["EXECUTE"], "on-condition": ["ON"],
    "on-error": ["ON ERROR"], "retry-continue": ["RETRY", "CONTINUE"],
    "def-fn": ["DEF", "FNEND"],
    "library-functions": ["LIBRARY", "DEF LIBRARY"],
}

# ---- topic index ---------------------------------------------------------
with io.open(sem_path, "r", encoding="utf-8", newline="") as f:
    lines = f.read().split("\n")

anchor_re = re.compile(r'^<a id="([^"]+)"></a>\s*$')
brtree_re = re.compile(r'\.\./br_tree/[^\s\)]+?spec\.md(?:#[\w-]+)?')

found = []
for i, ln in enumerate(lines):
    m = anchor_re.match(ln)
    if m:
        title = lines[i + 1][3:].strip() if i + 1 < len(lines) else ""
        found.append((m.group(1), i + 1, title))

total = len(lines)
topics = []
for k, (aid, aline, title) in enumerate(found):
    heading_line = aline + 1
    end_line = (found[k + 1][1] - 1) if k + 1 < len(found) else total
    body = "\n".join(lines[heading_line:end_line])
    bt = brtree_re.search(body)
    br_tree = bt.group(0) if bt else None
    if aid in META:
        topics.append({
            "id": aid, "kind": "statement", "title": title, "keywords": META[aid],
            "semantics": {"file": "statement-semantics.md", "anchor": aid,
                          "lines": [heading_line, end_line]},
            "br_tree": br_tree})
    else:
        topics.append({
            "id": aid, "kind": "reference", "title": title, "keywords": [],
            "semantics": {"file": "statement-semantics.md", "anchor": aid,
                          "lines": [heading_line, end_line]},
            "br_tree": br_tree})

kw_index = {}
for t in topics:
    for kw in t["keywords"]:
        kw_index.setdefault(kw, []).append(t["id"])

# ---- lexicon (frozen, hand-owned source: tools/lexicon.json) -------------
# Edit lexicon.json to change the classified keyword inventory; counts are recomputed
# and the lists re-sorted here so hand-edits stay normalized.
with io.open(lex_path, "r", encoding="utf-8", newline="") as f:
    lex = json.load(f)

reserved = sorted(set(lex["reserved_against_variables"]["names"]))
statement_kw = sorted(set(lex["positional"]["statement"]))
clause_kw = sorted(set(lex["positional"]["clause"]))
command_kw = sorted(set(lex["positional"]["command"]))

lexicon = {
    "note": lex["note"],
    "reserved_against_variables": {
        "note": lex["reserved_against_variables"]["note"],
        "count": len(reserved),
        "names": reserved,
        "intrinsics_outside_tables": lex["reserved_against_variables"]["intrinsics_outside_tables"],
    },
    "positional": {
        "note": lex["positional"]["note"],
        "statement": statement_kw,
        "clause": clause_kw,
        "command": command_kw,
    },
}

doc = {
    "$comment": "Topic index + lexicon over statement-semantics.md and tools/lexicon.json. "
                "Router for the interpret/code bundles (see APP-DEV-GUIDE.md). 'lines' are 1-based "
                "inclusive ranges for cheap section loading; regenerate with tools/gen_topics.py.",
    "generated": datetime.date.today().isoformat(),
    "source": "statement-semantics.md",
    "count": len(topics),
    "lexicon": lexicon,
    "keyword_index": dict(sorted(kw_index.items())),
    "topics": topics,
}

with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
    f.write("\n")

missing_bt = [t["id"] for t in topics if t["kind"] == "statement" and not t["br_tree"]]
print("topics: %d (stmt %d, ref %d) | routing-keywords %d | br_tree %d | missing: %s"
      % (len(topics), sum(1 for t in topics if t["kind"] == "statement"),
         sum(1 for t in topics if t["kind"] == "reference"), len(kw_index),
         sum(1 for t in topics if t["br_tree"]), missing_bt or "none"))
print("lexicon: reserved(fn) %d | statement %d | clause %d | command %d"
      % (len(reserved), len(statement_kw), len(clause_kw), len(command_kw)))
