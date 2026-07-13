#!/usr/bin/env python3
"""Generate brtree-index.json from the br_tree/ spec frontmatter.

Third sibling of gen_topics.py / gen_datamodel_index.py: a concept -> spec router
over the whole language reference (all spec.md leaves), not just statements.

  * reads every br_tree/**/spec.md, parses its frontmatter (title, category,
    status, keywords, related) plus its <a id="..."> anchors and lead paragraph.
  * emits brtree-index.json: a per-spec record + an inverse keyword_index
    (BR keyword -> [spec paths]) so a lookup resolves "which spec covers X" in one read.

Self-contained: no PyYAML (frontmatter here is regular enough to parse directly).
Run from anywhere:  python tools/gen_brtree_index.py
  --verify : don't write; check brtree-index.json is in sync with br_tree/
             (source hash + regenerate-and-compare). Exit 1 on drift.
"""
import io, os, re, sys, glob, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.dirname(HERE)                       # context/dev
BRTREE = os.path.join(os.path.dirname(DEV), "br_tree")
out_path = os.path.join(DEV, "brtree-index.json")

fm_re     = re.compile(r"^---\n(.*?)\n---\n", re.S)
kv_re     = re.compile(r"^([A-Za-z][\w-]*):\s?(.*)$")
anchor_re = re.compile(r'<a id="([^"]+)"></a>')


def parse_list(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
    return []


def lead_paragraph(body):
    """First real paragraph after the H1, collapsed to one line.

    Kept whole: the summary is what a reader ranks specs on without opening them,
    so truncating it defeats the index.
    """
    lines = body.split("\n")
    # skip to after the first '# ' heading
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    para = []
    while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", ">", "|", "```", "<a")):
        para.append(lines[i].strip())
        i += 1
    text = " ".join(para)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # [label](url) -> label
    text = re.sub(r"[*`]", "", text)                        # drop **bold** / *em* / `code`
    return re.sub(r"\s+", " ", text).strip()


def build():
    specs, hash_material = [], []
    for path in sorted(glob.glob(os.path.join(BRTREE, "**", "spec.md"), recursive=True)):
        raw = io.open(path, "r", encoding="utf-8").read()
        m = fm_re.match(raw)
        if not m:
            continue
        fm, body = m.group(1), raw[m.end():]
        d = {}
        for line in fm.split("\n"):
            kv = kv_re.match(line)
            if kv:
                d[kv.group(1)] = kv.group(2)
        rel = os.path.relpath(path, BRTREE).replace("\\", "/")
        subpath = rel[:-len("/spec.md")]
        specs.append({
            "path": subpath,
            "name": subpath.rsplit("/", 1)[-1],
            "file": "br_tree/" + rel,
            "title": d.get("title", "").strip(),
            "category": d.get("category", "").strip(),
            "status": d.get("status", "").split("#")[0].strip(),
            "keywords": parse_list(d.get("keywords", "")),
            "related": parse_list(d.get("related", "")),
            "anchors": anchor_re.findall(body),
            "summary": lead_paragraph(body),
        })
        hash_material.append(rel + "\n" + fm)

    kw_index = {}
    for s in specs:
        for kw in s["keywords"]:
            kw_index.setdefault(kw, []).append(s["path"])
    src_hash = hashlib.sha256("\n".join(hash_material).encode("utf-8")).hexdigest()

    doc = {
        "$comment": "Concept -> spec router over br_tree/. keyword_index maps a BR keyword to the "
                    "spec path(s) that document it; each spec record carries title, status, anchors, "
                    "and lead summary. Regenerate with tools/gen_brtree_index.py.",
        "generated": datetime.date.today().isoformat(),
        "source": "br_tree/",
        "source_sha256": src_hash,
        "count": len(specs),
        "keyword_index": dict(sorted(kw_index.items())),
        "specs": specs,
    }
    return doc, src_hash


def _drop_generated(d):
    return {k: v for k, v in d.items() if k != "generated"}


doc, src_hash = build()

if "--verify" in sys.argv:
    name = os.path.basename(out_path)
    if not os.path.exists(out_path):
        print("VERIFY FAIL: %s missing - run tools/gen_brtree_index.py" % name); sys.exit(1)
    existing = json.load(io.open(out_path, "r", encoding="utf-8"))
    problems = []
    if existing.get("source_sha256") != src_hash:
        problems.append("source_sha256 mismatch: br_tree/ spec frontmatter changed since last generate")
    if _drop_generated(existing) != _drop_generated(doc):
        problems.append("content drift: regenerated index differs from on-disk "
                        "(keywords / related / anchors / titles) - run tools/gen_brtree_index.py")
    if problems:
        print("VERIFY FAIL (%d issue%s):" % (len(problems), "" if len(problems) == 1 else "s"))
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("VERIFY OK: %s in sync - %d specs, source hash %s..." % (name, len(doc["specs"]), src_hash[:12]))
    sys.exit(0)

with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
    f.write("\n")

multi = {k: v for k, v in doc["keyword_index"].items() if len(v) > 1}
print("specs: %d | keywords: %d (%d multi-spec) | source hash %s..."
      % (len(doc["specs"]), len(doc["keyword_index"]), len(multi), src_hash[:12]))
