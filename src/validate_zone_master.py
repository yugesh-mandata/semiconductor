"""Independently verify ZONE_MASTER.xlsx against the KML and CAMPUS_MASTER.md.

Reads the KML with regexes and the xlsx as raw XML (no openpyxl), so it shares no parsing code with
build_zone_master.py. Compares the untouched sheets against the committed workbook (git HEAD).
"""
import datetime as dt
import io
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from shapely.geometry import Polygon

ROOT = Path(__file__).resolve().parent.parent
XLSX_REL = "layouts/master_layout/ZONE_MASTER.xlsx"
CAMPUS_MD = ROOT / "layouts/CAMPUS_MASTER.md"

# Per-zone values stored in each placemark's <description>.
DESCRIPTION_FIELDS = [
    "record_id", "zone_code", "production_unit_name", "production_unit_code", "production_unit_type",
    "zone_type", "zone_type_confidence", "primary_product_association", "product_association_confidence",
    "effective_from", "effective_to", "pit_available_from", "pit_available_to", "imagery_acquired_date",
]
# Client code list (layouts/client/DEV_..._20261021.xlsx, INFORMATION sheet), plus NULL.
ENUMS = {
    "zone_type": {"OP", "EX", "CD", "MX"},  # MX pending confirmation
    "production_unit_type": {"FRONT_END_FAB", "PACKAGING_TEST", "MIXED", "UNKNOWN", "NULL"},
    "primary_product_association": {"HBM", "DRAM", "NAND", "LOGIC", "MIXED", "UNKNOWN", "NULL"},
    "zone_type_confidence": {"HIGH", "MEDIUM", "LOW", "NULL"},
    "product_association_confidence": {"HIGHLY_ASSOC", "ASSOC", "UNCERTAIN", "NULL"},
}
# Combined product values such as DRAM_NAND_LOGIC are allowed for now instead of MIXED (pending client decision).
PRODUCT_PARTS = {"HBM", "DRAM", "NAND", "LOGIC"}
UNIT_COLS = ("production_unit_name", "production_unit_code", "production_unit_type", "primary_product_association")
DATE_COLS = ("effective_from", "effective_to", "pit_available_from", "pit_available_to", "imagery_acquired_date")
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
errors = []


def err(msg):
    errors.append(msg)


def col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_sheets(data):
    """Return {sheet name: (dimension ref, [rows as lists of str])} from raw xlsx bytes."""
    z = zipfile.ZipFile(io.BytesIO(data))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(M + "si"):
            shared.append("".join(t.text or "" for t in si.iter(M + "t")))
    out = {}
    for s in wb.find(M + "sheets"):
        target = rels[s.get(R + "id")].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        root = ET.fromstring(z.read(target))
        dim = root.find(M + "dimension")
        rows = []
        for row in root.find(M + "sheetData").findall(M + "row"):
            vals = {}
            for c in row.findall(M + "c"):
                v, inline = c.find(M + "v"), c.find(M + "is")
                if v is not None:
                    vals[col_index(c.get("r"))] = shared[int(v.text)] if c.get("t") == "s" else v.text
                elif inline is not None:
                    vals[col_index(c.get("r"))] = "".join(t.text or "" for t in inline.iter(M + "t"))
            rows.append([vals.get(i, "") for i in range(max(vals) + 1)] if vals else [])
        out[s.get("name")] = (dim.get("ref") if dim is not None else None, rows)
    return out


# ---- KML, parsed from raw text (folders, placemarks, balloon text of each zone's own style, coordinates)
kml_path = Path(sys.argv[1])
raw = kml_path.read_text(encoding="utf-8")
if "<description>" in raw or "$[description]" in raw:
    err("KML still has <description> elements or $[description] balloon text")
balloon = {}
for m in re.finditer(r'<gx:CascadingStyle kml:id="([^"]+)">(.*?)</gx:CascadingStyle>', raw, re.S):
    t = re.search(r"<BalloonStyle>\s*<text><!\[CDATA\[(.*?)\]\]></text>", m.group(2), re.S)
    balloon[m.group(1)] = t.group(1) if t else ""
stylemap = {
    m.group(1): dict(re.findall(r"<key>(\w+)</key>\s*<styleUrl>#([^<]+)</styleUrl>", m.group(2)))
    for m in re.finditer(r'<StyleMap id="([^"]+)">(.*?)</StyleMap>', raw, re.S)
}
kml, style_users = [], {}
for fm in re.finditer(r"<Folder[^>]*>.*?<name>([^<]+)</name>(.*?)</Folder>", raw, re.S):
    for pm in re.finditer(r"<Placemark[^>]*>(.*?)</Placemark>", fm.group(2), re.S):
        body = pm.group(1)
        name = re.search(r"<name>(.*?)</name>", body).group(1)
        sid = re.search(r"<styleUrl>#(.*?)</styleUrl>", body).group(1)
        style_users.setdefault(sid, []).append(name)
        pair = stylemap.get(sid, {"normal": sid, "highlight": sid})
        attrs = dict(re.findall(r"<h1>([a-z_]+): ([^<]*?)</h1>", balloon.get(pair["normal"], "")))
        if list(attrs) != DESCRIPTION_FIELDS:
            err(f"{name}: Description fields {list(attrs)} != {DESCRIPTION_FIELDS}")
        if balloon.get(pair["highlight"]) != balloon.get(pair["normal"]):
            err(f"{name}: highlight style's Description differs from the normal one")
        kml.append(dict(
            folder=fm.group(1),
            name=name,
            attrs=attrs,
            polygon=" ".join(re.search(r"<coordinates>(.*?)</coordinates>", body, re.S).group(1).split()),
        ))
for sid, names in style_users.items():
    if len(names) > 1:
        err(f"zones {names} share style {sid}; editing one in Google Earth would change all of them")
if len(kml) != raw.count("<Placemark"):
    err(f"parsed {len(kml)} placemarks inside folders, KML has {raw.count('<Placemark')}")

# ---- Campus master
campus = {}
for ln in CAMPUS_MD.read_text(encoding="utf-8").splitlines():
    if re.match(r"\| (SK|SAMSUNG)", ln):
        company, isin, name, code, address = [c.strip() for c in ln.strip().strip("|").split("|")]
        campus[code] = dict(company_name_en=company, security_code=isin, campus_name=name, campus_address=address)


def poly(raw_coords):
    return Polygon([tuple(float(v) for v in tok.split(",")[:2]) for tok in raw_coords.split()])


# ---- Workbook (new) and committed workbook (for untouched sheets)
new = read_sheets((ROOT / XLSX_REL).read_bytes())
old = read_sheets(subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{XLSX_REL}"], capture_output=True, check=True).stdout)

if list(new) != list(old):
    err(f"sheet list changed: {list(old)} -> {list(new)}")
for name in old:
    if name not in ("ZONE_MASTER", "ZONE_LINEAGE_MASTER") and old[name][1] != new.get(name, (None, None))[1]:
        err(f"sheet {name} values changed but should be untouched")

dim, zm = new["ZONE_MASTER"]
header, data = zm[0], [r for r in zm[1:] if r]
if "check_status(TEMP)" in header:
    err("check_status(TEMP) column still present")
if len(zm) - 1 != len(data):
    err(f"ZONE_MASTER has {len(zm) - 1 - len(data)} empty rows after the header")
if dim != f"A1:U{len(data) + 1}":
    err(f"ZONE_MASTER dimension {dim} != A1:U{len(data) + 1}")
rows = [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in data]

# ---- Row-by-row checks
mx_skipped = len(rows) == len(kml) - sum(1 for k in kml if k["attrs"].get("zone_type") == "MX")
expected = [k for k in kml if not (mx_skipped and k["attrs"].get("zone_type") == "MX")]
if len(rows) != len(expected):
    err(f"row count {len(rows)} != KML zones {len(expected)}")

report, created, pu_names = [], set(), {}
for i, (k, r) in enumerate(zip(expected, rows), start=2):
    code = k["name"]
    issues = []
    parts = code.split("_")
    cc, zt = "_".join(parts[:2]), parts[2]
    for f in DESCRIPTION_FIELDS:
        if r[f] != k["attrs"].get(f):
            issues.append(f"{f} {r[f]!r} != KML {k['attrs'].get(f)!r}")
    if r["zone_code"] != code:
        issues.append(f"zone_code {r['zone_code']!r} (KML order)")
    if r["zone_type"] != zt:
        issues.append(f"zone_type {r['zone_type']!r} != code part {zt!r}")
    if r["campus_code"] != cc or cc != k["folder"]:
        issues.append(f"campus_code {r['campus_code']!r} / folder {k['folder']!r}")
    for col in ("company_name_en", "security_code", "campus_name", "campus_address"):
        if r[col] != campus[cc][col]:
            issues.append(f"{col} {r[col]!r} != CAMPUS_MASTER {campus[cc][col]!r}")
    if r["polygon"] != k["polygon"]:
        issues.append("polygon text differs from KML")
    for col in DATE_COLS:
        if r[col] != "NULL" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[col]):
            issues.append(f"{col} {r[col]!r} is not YYYY-MM-DD or NULL")
    if (r["pit_available_from"], r["pit_available_to"]) != (r["effective_from"], r["effective_to"]):
        issues.append("pit_available_from/to not equal to effective_from/to (backfill)")
    if not re.fullmatch(rf"{cc}_\d{{3}}", r["record_id"]):
        issues.append(f"record_id {r['record_id']!r}")
    created.add(r["record_created_at"])
    for col, allowed in ENUMS.items():
        parts = r[col].split("_")
        combined = col == "primary_product_association" and len(parts) > 1 and set(parts) <= PRODUCT_PARTS
        if r[col] not in allowed and not combined:
            issues.append(f"{col} {r[col]!r} not in code list")
    if r["imagery_acquired_date"] != "NULL" and r["imagery_acquired_date"] > r["record_created_at"][:10]:
        issues.append("imagery_acquired_date after record_created_at")
    if zt == "OP":
        if not re.fullmatch(rf"{cc}_PU_\d{{3}}", r["production_unit_code"]):
            issues.append(f"production_unit_code {r['production_unit_code']!r}")
        if r["production_unit_name"] != "NULL":
            pu_names.setdefault((cc, r["production_unit_name"]), set()).add(r["production_unit_code"])
    elif zt != "MX" and any(r[c] != "NULL" for c in UNIT_COLS):  # MX zones may carry unit/product values
        issues.append(f"{zt} zone must have NULL unit/product fields")
    report.append((r["record_id"], code, r["production_unit_name"], r["production_unit_code"], "PASS" if not issues else "FAIL"))
    errors.extend(f"row {i} {code}: {s}" for s in issues)

if len({r["record_id"] for r in rows}) != len(rows):
    err("record_id is not unique")
if len(created) != 1:
    err(f"record_created_at differs across rows: {sorted(created)}")
for key, codes in pu_names.items():
    if len(codes) != 1:
        err(f"production unit {key} has several codes {sorted(codes)}")
named = {c for cs in pu_names.values() for c in cs}
unnamed = [r["production_unit_code"] for r in rows if r["zone_type"] == "OP" and r["production_unit_name"] == "NULL"]
if len(unnamed) != len(set(unnamed)) or set(unnamed) & named:
    err("an unnamed OP zone shares a production_unit_code")

# ---- Lineage
_, lm = new["ZONE_LINEAGE_MASTER"]
lh = lm[0]
lineage = [dict(zip(lh, r)) for r in lm[1:] if r]
by_record = {r["record_id"]: r for r in rows}
for l in lineage:
    p, c = by_record.get(l["parent_record_id"]), by_record.get(l["child_record_id"])
    tag = f"lineage {l['lineage_id']}"
    if not p or not c:
        err(f"{tag}: unknown record_id")
        continue
    nxt = (dt.date.fromisoformat(p["effective_to"]) + dt.timedelta(days=1)).isoformat() if p["effective_to"] != "NULL" else None
    if p["zone_type"] != "EX":
        err(f"{tag}: parent {p['zone_code']} is not EX")
    if l["relationship_type"] != "TRANSFORM" or not poly(p["polygon"]).equals(poly(c["polygon"])):
        err(f"{tag}: expected TRANSFORM with identical polygons")
    if not (nxt == l["effective_at"] == c["effective_from"] == l["pit_available_from"]) or l["pit_available_to"] != "NULL":
        err(f"{tag}: dates parent_to+1={nxt} effective_at={l['effective_at']} child_from={c['effective_from']}")
    if not re.fullmatch(rf"LIN_{p['campus_code'].split('_')[1]}_\d{{3}}", l["lineage_id"]):
        err(f"{tag}: lineage_id format")
if len({l["lineage_id"] for l in lineage}) != len(lineage):
    err("lineage_id is not unique")
# Every EX that ends with an identical successor starting the next day must be linked.
linked = {(l["parent_record_id"], l["child_record_id"]) for l in lineage}
for p in rows:
    if p["zone_type"] != "EX" or p["effective_to"] == "NULL":
        continue
    nxt = (dt.date.fromisoformat(p["effective_to"]) + dt.timedelta(days=1)).isoformat()
    for c in rows:
        if c is not p and c["campus_code"] == p["campus_code"] and c["effective_from"] == nxt \
                and poly(p["polygon"]).equals(poly(c["polygon"])) and (p["record_id"], c["record_id"]) not in linked:
            err(f"missing lineage {p['zone_code']} -> {c['zone_code']}")

# ---- Report
size = (ROOT / XLSX_REL).stat().st_size
if size > 100_000:
    err(f"file size {size} bytes > 100 KB")
print(f"{'record_id':<13}{'zone_code':<16}{'unit':<10}{'unit_code':<16}result")
for row in report:
    print(f"{row[0]:<13}{row[1]:<16}{row[2]:<10}{row[3]:<16}{row[4]}")
print(f"\nzones: {len(rows)}   lineage rows: {len(lineage)}   size: {size:,} bytes")
if errors:
    print(f"\nFAILED with {len(errors)} error(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nALL CHECKS PASSED")
