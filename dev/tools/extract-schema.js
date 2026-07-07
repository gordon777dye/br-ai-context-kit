#!/usr/bin/env node
/* Parse a BR application's filelay/* data-dictionary into a structured schema catalog.
 * Generic: point it at any app's filelay directory.
 *   Usage: node extract-schema.js <filelayDir> [outDir]
 *   filelayDir defaults to $BR_FILELAY_DIR; outDir defaults to this tool's parent (context/dev).
 * Output: data-model.json (structured) + data-model.md (readable).
 * filelay format:
 *   <dir\datafile>,<PREFIX_>,<n>
 *   <dir\datafile.keyN>,<FIELD/FIELD/...>      (one per index)
 *   recl=<n>
 *   ==================
 *   NAME$, Description, FORM-spec, note, startpos - endpos
 */
const fs = require('fs');
const path = require('path');

const LAYDIR = process.argv[2] || process.env.BR_FILELAY_DIR;
const OUTDIR = process.argv[3] || path.resolve(__dirname, '..');
if (!LAYDIR) {
  console.error('Usage: node extract-schema.js <filelayDir> [outDir]   (or set $BR_FILELAY_DIR)');
  console.error('Generates a data model from a BR app\'s filelay/ directory. No default app is bundled.');
  process.exit(2);
}
const files = fs.readdirSync(LAYDIR).filter(n => fs.statSync(path.join(LAYDIR, n)).isFile());

const POSRE = /^\s*\d+\s*-\s*\d+\s*$/;

function parseLayout(name) {
  const raw = fs.readFileSync(path.join(LAYDIR, name), 'latin1').split(/\r?\n/);
  const rec = { name, dataFile: null, prefix: null, recl: null, keys: [], fields: [] };
  const TYPERE = /^[A-Za-z]{1,3}\s*[\d.]*$/;   // FORM type spec e.g. "C 8", "BH 2.2", "V 255"
  let inFields = false;
  for (const line of raw) {
    if (/^====+/.test(line)) { inFields = true; continue; }
    if (!inFields) {
      const reclM = line.match(/^recl\s*=\s*(\d+)/i);
      if (reclM) { rec.recl = Number(reclM[1]); continue; }
      const parts = line.split(',');
      if (parts.length < 1 || !parts[0].trim()) continue;
      const p0 = parts[0].trim();
      if (!rec.dataFile) {                       // first header line = data file
        rec.dataFile = p0;
        rec.prefix = (parts[1] || '').trim() || null;
      } else if (parts.length >= 2) {            // any later header line = a key index
        rec.keys.push({
          index: (p0.match(/\.([A-Za-z]+\d*)$/) || [, p0])[1].toLowerCase(),
          file: p0,
          fields: parts.slice(1).join(',').trim().split('/').map(s => s.trim()).filter(Boolean),
        });
      }
      continue;
    }
    // field line — tolerate 3/4/5 columns; parse from the right so commas in desc are safe
    const parts = line.split(',');
    if (parts.length < 3) continue;
    const fname = parts[0].trim();
    if (!fname) continue;
    const last = parts[parts.length - 1].trim();
    let pos, type, note, descEnd;
    if (POSRE.test(last)) {                       // has a position range
      pos = last.replace(/\s+/g, '');
      // type = rightmost middle column that looks like a FORM spec; note = anything after it
      let ti = -1;
      for (let k = parts.length - 2; k >= 1; k--) { if (TYPERE.test(parts[k].trim())) { ti = k; break; } }
      if (ti === -1) continue;
      type = parts[ti].trim();
      note = parts.slice(ti + 1, parts.length - 1).map(s => s.trim()).filter(Boolean).join(', ');
      descEnd = ti;
    } else if (TYPERE.test(last)) {               // no position (V-type config/log files)
      type = last; pos = undefined; note = '';
      descEnd = parts.length - 1;
    } else continue;
    const desc = parts.slice(1, descEnd).join(',').trim();
    const tM = type.match(/^([A-Za-z]+)\s*([\d.]+)?/);
    rec.fields.push({
      name: fname,
      desc,
      form: type.replace(/\s+/g, ' '),
      formCode: tM ? tM[1].toUpperCase() : type,
      size: tM && tM[2] ? tM[2] : undefined,
      note: note || undefined,
      pos,
      isString: fname.endsWith('$'),
    });
  }
  return rec;
}

const layouts = files.map(parseLayout).sort((a, b) => a.name.localeCompare(b.name));

fs.writeFileSync(path.join(OUTDIR, 'data-model.json'),
  JSON.stringify({ generated: new Date().toISOString().slice(0, 10), source: LAYDIR,
    fileCount: layouts.length, layouts }, null, 1));

// readable markdown
const L = [];
L.push('# BR application data model (file schemas)');
L.push('');
L.push(`Data dictionary for **${layouts.length}** BR data files, parsed from \`${LAYDIR}\`. Dual purpose:`);
L.push('an LLM uses this to know what files/fields exist and how they are keyed when writing BR');
L.push('code; an LSP uses field names + FORM types to validate/complete `OPEN`/`READ…USING` and');
L.push('to build correct key expressions. Machine-readable companion: `data-model.json`.');
L.push('');
L.push('Per file: the data path, record length, key indexes (with their composing fields — the');
L.push('order you concatenate values to build a `KEY=` lookup), and every field with its FORM type.');
L.push('');
L.push('| File | Recl | Fields | Keys |');
L.push('|---|---|---|---|');
for (const r of layouts) {
  L.push(`| [\`${r.name}\`](#${r.name}) | ${r.recl ?? '?'} | ${r.fields.length} | ${r.keys.length} |`);
}
L.push('');
for (const r of layouts) {
  L.push(`## ${r.name}`);
  L.push('');
  L.push(`- **Data file:** \`${r.dataFile || '?'}\`${r.prefix ? ` (field prefix \`${r.prefix}\`)` : ''} · **recl** ${r.recl ?? '?'}`);
  if (r.keys.length) {
    L.push('- **Keys:**');
    for (const k of r.keys) L.push(`  - \`${k.index}\` = ${k.fields.map(f => '`' + f + '`').join(' + ') || '(raw)'}`);
  }
  L.push('');
  L.push('| Field | Type | Pos | Description |');
  L.push('|---|---|---|---|');
  for (const f of r.fields) {
    const d = (f.desc || '').replace(/\|/g, '\\|');
    const note = f.note ? ` _(${f.note})_` : '';
    L.push(`| \`${f.name}\` | ${f.form} | ${f.pos || '—'} | ${d}${note} |`);
  }
  L.push('');
}
fs.writeFileSync(path.join(OUTDIR, 'data-model.md'), L.join('\n'));

const totalFields = layouts.reduce((s, r) => s + r.fields.length, 0);
console.log(`layouts: ${layouts.length}, total fields: ${totalFields}`);
console.log(`no-field-parse: ${layouts.filter(r => r.fields.length === 0).map(r => r.name).join(', ') || 'none'}`);
