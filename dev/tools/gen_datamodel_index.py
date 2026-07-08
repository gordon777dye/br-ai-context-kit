#!/usr/bin/env python3
"""Generate data-model-index.json from an app's data-model.md.

Sister of gen_topics.py: the same anchor->line-range sharding, applied to the
app data model instead of statement-semantics.md.

  * reads the <a id="..."></a> anchors and ## headings that extract-schema.js
    emits (one per data file), derives each file's 1-based inclusive line range,
    and pulls recl / field-count / key-count from the section body.
  * emits data-model-index.json beside the .md so a tool or model can load just
    one file's slice ([lines]) instead of the whole (large) document.

Regenerate whenever data-model.md is (re)generated or hand-edited.

  Usage: python tools/gen_datamodel_index.py [data-model.md]
         (defaults to ../../app/data-model.md relative to this tool)
  --verify : don't write; check data-model-index.json is in sync with data-model.md
             (source hash, range validity, and a full regenerate-and-compare). Exit 1 on drift.
"""
import io, os, re, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONTEXT = os.path.dirname(os.path.dirname(HERE))          # context/
default_md = os.path.join(CONTEXT, "app", "data-model.md")
positional = [a for a in sys.argv[1:] if not a.startswith("-")]
verify_mode = "--verify" in sys.argv
md_path = os.path.abspath(positional[0]) if positional else default_md
out_path = os.path.join(os.path.dirname(md_path), "data-model-index.json")

with io.open(md_path, "r", encoding="utf-8", newline="") as f:
    raw = f.read()
lines = raw.split("\n")
src_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

anchor_re = re.compile(r'^<a id="([^"]+)"></a>\s*$')
recl_re   = re.compile(r'\*\*recl\*\*\s*(\d+)')
keybul_re = re.compile(r'^  - `')          # a "  - `idx` = ..." key bullet
fieldrow_re = re.compile(r'^\| `')         # a "| `FIELD$` | ..." table row

found = []
for i, ln in enumerate(lines):
    m = anchor_re.match(ln)
    if m:
        found.append((m.group(1), i + 1))   # (name, anchor line, 1-based)

total = len(lines)
entries = []
for k, (name, aline) in enumerate(found):
    heading_line = aline + 1
    end_line = (found[k + 1][1] - 1) if k + 1 < len(found) else total
    body = lines[heading_line:end_line]
    reclM = next((recl_re.search(b) for b in body if recl_re.search(b)), None)
    entries.append({
        "name": name,
        "anchor": name,
        "lines": [heading_line, end_line],
        "recl": int(reclM.group(1)) if reclM else None,
        "fields": sum(1 for b in body if fieldrow_re.match(b)),
        "keys": sum(1 for b in body if keybul_re.match(b)),
    })

rel_md = os.path.relpath(md_path, os.path.dirname(out_path)).replace("\\", "/")
doc = {
    "$comment": "Per-file section index over data-model.md. 'lines' are 1-based inclusive "
                "ranges for cheap per-file loading; regenerate with tools/gen_datamodel_index.py.",
    "generated": datetime.date.today().isoformat(),
    "source": rel_md,
    "source_sha256": src_hash,
    "count": len(entries),
    "files": entries,
}


def _drop_generated(d):
    return {k: v for k, v in d.items() if k != "generated"}

if verify_mode:
    name = os.path.basename(out_path)
    if not os.path.exists(out_path):
        print("VERIFY FAIL: %s missing — run tools/gen_datamodel_index.py" % name); sys.exit(1)
    with io.open(out_path, "r", encoding="utf-8") as f:
        existing = json.load(f)
    problems = []
    if existing.get("source_sha256") != src_hash:
        problems.append("source_sha256 mismatch: data-model.md changed since last generate")
    prev_end = 0
    for e in existing.get("files", []):
        rng = e.get("lines")
        nm = e.get("name")
        if not (isinstance(rng, list) and len(rng) == 2 and all(isinstance(n, int) for n in rng)):
            problems.append("file %s: malformed line range %r" % (nm, rng)); continue
        lo, hi = rng
        if lo < 1 or hi < lo:
            problems.append("file %s: invalid range [%d,%d]" % (nm, lo, hi))
        if hi > total:
            problems.append("file %s: range [%d,%d] exceeds file length %d" % (nm, lo, hi, total))
        if lo <= prev_end:
            problems.append("file %s: range starts at %d, overlaps previous file (ended %d)" % (nm, lo, prev_end))
        prev_end = hi
    if _drop_generated(existing) != _drop_generated(doc):
        problems.append("content drift: regenerated index differs from on-disk "
                        "(line ranges / recl / field or key counts) - run tools/gen_datamodel_index.py")
    if problems:
        print("VERIFY FAIL (%d issue%s):" % (len(problems), "" if len(problems) == 1 else "s"))
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("VERIFY OK: %s in sync - %d files, source hash %s..."
          % (name, len(entries), src_hash[:12]))
    sys.exit(0)

with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
    f.write("\n")

no_recl = [e["name"] for e in entries if e["recl"] is None]
print("files: %d | fields %d | keys %d | no-recl: %s"
      % (len(entries), sum(e["fields"] for e in entries),
         sum(e["keys"] for e in entries), no_recl or "none"))
