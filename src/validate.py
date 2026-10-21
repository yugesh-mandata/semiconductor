"""Independently verify the zipped shapefile against the KML (raw-text KML parse + raw binary .shp/.shx checks)."""
import io
import re
import struct
import sys
import zipfile
from pathlib import Path

import shapefile

kml_path = Path(sys.argv[1])
zip_path = kml_path.with_suffix(".zip")
stem = kml_path.stem
raw = kml_path.read_text(encoding="utf-8")
errors = []

with zipfile.ZipFile(zip_path) as zf:
    if zf.testzip() is not None:
        sys.exit(f"{zip_path}: corrupt member {zf.testzip()}")
    members = {name: zf.read(name) for name in zf.namelist()}


def err(msg):
    errors.append(msg)


# ---- KML, parsed from raw text with regexes (independent of the converter's ElementTree path)
balloon = {}
for m in re.finditer(r'<(?:gx:CascadingStyle kml:id|Style id)="([^"]+)">(.*?)</(?:gx:CascadingStyle|Style)>', raw, re.S):
    t = re.search(r"<BalloonStyle>\s*<text><!\[CDATA\[(.*?)\]\]></text>", m.group(2), re.S)
    balloon[m.group(1)] = t.group(1) if t else None
stylemap = {
    m.group(1): re.search(r"<key>normal</key>\s*<styleUrl>#([^<]+)</styleUrl>", m.group(2)).group(1)
    for m in re.finditer(r'<StyleMap id="([^"]+)">(.*?)</StyleMap>', raw, re.S)
}

kml = []
for m in re.finditer(r"<Placemark[^>]*>(.*?)</Placemark>", raw, re.S):
    body = m.group(1)
    name = re.search(r"<name>(.*?)</name>", body).group(1)
    sid = re.search(r"<styleUrl>#(.*?)</styleUrl>", body).group(1)
    sid = stylemap.get(sid, sid)
    html = balloon.get(sid) or ""
    ef = re.search(r"effective_from: ([^<]*?)</h1>", html)
    et = re.search(r"effective_to: ([^<]*?)</h1>", html)
    rings = re.findall(r"<coordinates>(.*?)</coordinates>", body, re.S)
    if len(rings) != 1:
        err(f"{name}: expected 1 ring in KML, found {len(rings)}")
    tokens = [tuple(t.split(",")) for t in rings[0].split()]
    kml.append(dict(name=name, eff_from=ef.group(1) if ef else "", eff_to=et.group(1) if et else "", tokens=tokens))

# ---- Shapefile via pyshp
expected_members = {stem + ext for ext in (".shp", ".shx", ".dbf", ".prj", ".cpg")}
if set(members) != expected_members:
    err(f"zip members {sorted(members)} != {sorted(expected_members)}")
r = shapefile.Reader(
    shp=io.BytesIO(members[stem + ".shp"]),
    shx=io.BytesIO(members[stem + ".shx"]),
    dbf=io.BytesIO(members[stem + ".dbf"]),
    encoding="utf-8",
)
fields = [f.name for f in r.fields[1:]]
if fields != ["zone_code", "eff_from", "eff_to"]:
    err(f"unexpected fields {fields}")
if r.shapeType != shapefile.POLYGONZ:
    err(f"shapeType {r.shapeTypeName}, expected POLYGONZ")
if len(r) != len(kml):
    err(f"feature count {len(r)} != KML placemarks {len(kml)}")

rows = []
all_x, all_y, all_z = [], [], []
reversed_count = 0
for i, (k, sr) in enumerate(zip(kml, r.iterShapeRecords())):
    shp, rec = sr.shape, sr.record
    issues = []
    if rec["zone_code"] != k["name"]:
        issues.append(f"zone_code {rec['zone_code']!r} != {k['name']!r}")
    if rec["eff_from"] != k["eff_from"]:
        issues.append(f"eff_from {rec['eff_from']!r} != {k['eff_from']!r}")
    if rec["eff_to"] != k["eff_to"]:
        issues.append(f"eff_to {rec['eff_to']!r} != {k['eff_to']!r}")
    if shp.shapeType != shapefile.POLYGONZ or list(shp.parts) != [0]:
        issues.append(f"shape type/parts {shp.shapeType}/{list(shp.parts)}")

    exp = [(float(x), float(y), float(z)) for x, y, z in k["tokens"]]
    got = [(p[0], p[1], z) for p, z in zip(shp.points, shp.z)]
    if got == exp:
        order = "same"
    elif got == exp[::-1]:
        order = "reversed"
        reversed_count += 1
    else:
        order = "MISMATCH"
        issues.append("coordinates differ")
    # textual round-trip: shortest repr of each stored double must reproduce the KML text
    src_tokens = k["tokens"] if order != "reversed" else k["tokens"][::-1]
    for (x, y, z), (tx, ty, tz) in zip(got, src_tokens):
        if repr(x) != tx or repr(y) != ty or z != float(tz):
            issues.append(f"text round-trip {repr(x)},{repr(y)} vs {tx},{ty}")
            break
    all_x += [p[0] for p in exp]
    all_y += [p[1] for p in exp]
    all_z += [p[2] for p in exp]
    rows.append((k["name"], k["eff_from"] or "-", k["eff_to"] or "-", len(exp), order, "PASS" if not issues else "FAIL"))
    errors.extend(f"{k['name']}: {s}" for s in issues)

if len({k["name"] for k in kml}) != len(kml):
    err("duplicate zone_codes in KML")

# ---- Raw binary header checks (.shp / .shx)
hdr = members[stem + ".shp"][:100]
stype = struct.unpack("<i", hdr[32:36])[0]
xmin, ymin, xmax, ymax, zmin, zmax = struct.unpack("<6d", hdr[36:84])
if stype != 15:
    err(f".shp header shape type {stype} != 15 (PolygonZ)")
if (xmin, ymin, xmax, ymax) != (min(all_x), min(all_y), max(all_x), max(all_y)):
    err(f".shp bbox {(xmin, ymin, xmax, ymax)} != KML bbox")
if (zmin, zmax) != (min(all_z), max(all_z)):
    err(f".shp z-range {(zmin, zmax)} != KML z-range")
shx_len = struct.unpack(">i", members[stem + ".shx"][24:28])[0] * 2
if (shx_len - 100) // 8 != len(kml):
    err(f".shx record count {(shx_len - 100) // 8} != {len(kml)}")
if not members.get(stem + ".prj", b"").startswith(b'GEOGCS["GCS_WGS_1984"'):
    err(".prj is not WGS 84")
if members.get(stem + ".cpg") != b"UTF-8":
    err(".cpg is not UTF-8")

# ---- Report
print(f"{'zone_code':<16}{'eff_from':<12}{'eff_to':<12}{'verts':>6}  {'order':<9}result")
for row in rows:
    print(f"{row[0]:<16}{row[1]:<12}{row[2]:<12}{row[3]:>6}  {row[4]:<9}{row[5]}")
print()
print(f"KML placemarks: {len(kml)}   SHP features: {len(r)}   vertices: {len(all_x)}")
print(f"rings stored in reversed order (KML CCW -> SHP CW): {reversed_count}")
print(f"bbox: x[{xmin}, {xmax}] y[{ymin}, {ymax}] z[{zmin}, {zmax}]")
if errors:
    print(f"\nFAILED with {len(errors)} error(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nALL CHECKS PASSED - no information loss for zone_code, polygon, eff_from, eff_to")
