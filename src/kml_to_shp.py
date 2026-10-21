"""Convert ZONE_BOUNDARY_MASTER.kml to a zipped PolygonZ shapefile (zone_code, eff_from, eff_to)."""
import io
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import shapefile

NS = {
    "k": "http://www.opengis.net/kml/2.2",
    "gx": "http://www.google.com/kml/ext/2.2",
}
KML_ID = "{http://www.opengis.net/kml/2.2}id"

WGS84_PRJ = (
    'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],'
    'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
)


def style_balloons(doc):
    """Map style id -> BalloonStyle text for Style and gx:CascadingStyle elements."""
    out = {}
    for el in doc.findall("k:Style", NS):
        txt = el.find("k:BalloonStyle/k:text", NS)
        out[el.get("id")] = txt.text if txt is not None else None
    for el in doc.findall("gx:CascadingStyle", NS):
        txt = el.find("k:Style/k:BalloonStyle/k:text", NS)
        out[el.get(KML_ID)] = txt.text if txt is not None else None
    return out


def style_maps(doc):
    """Map StyleMap id -> styleUrl of its 'normal' pair."""
    out = {}
    for sm in doc.findall("k:StyleMap", NS):
        for pair in sm.findall("k:Pair", NS):
            if pair.find("k:key", NS).text == "normal":
                out[sm.get("id")] = pair.find("k:styleUrl", NS).text
    return out


def dates_for(style_url, balloons, maps):
    sid = style_url.lstrip("#")
    if sid in maps:
        sid = maps[sid].lstrip("#")
    text = balloons.get(sid)
    if not text:
        return "", ""
    f = re.search(r"effective_from:\s*(\S+?)\s*<", text)
    t = re.search(r"effective_to:\s*(\S+?)\s*<", text)
    return (f.group(1) if f else ""), (t.group(1) if t else "")


def signed_area(ring):
    return sum(x1 * y2 - x2 * y1 for (x1, y1, _), (x2, y2, _) in zip(ring, ring[1:])) / 2.0


def main(kml_path):
    kml_path = Path(kml_path)
    doc = ET.parse(kml_path).getroot().find("k:Document", NS)
    balloons, maps = style_balloons(doc), style_maps(doc)

    shp, shx, dbf = io.BytesIO(), io.BytesIO(), io.BytesIO()
    w = shapefile.Writer(shp=shp, shx=shx, dbf=dbf, shapeType=shapefile.POLYGONZ, encoding="utf-8")
    w.field("zone_code", "C", size=20)
    w.field("eff_from", "C", size=10)
    w.field("eff_to", "C", size=10)

    n = 0
    for pm in doc.iter("{%s}Placemark" % NS["k"]):
        name = pm.find("k:name", NS).text
        coords_el = pm.findall("k:Polygon/k:outerBoundaryIs/k:LinearRing/k:coordinates", NS)
        if len(coords_el) != 1 or pm.findall("k:Polygon/k:innerBoundaryIs", NS):
            sys.exit(f"{name}: unexpected geometry structure")
        ring = [tuple(float(v) for v in tok.split(",")) for tok in coords_el[0].text.split()]
        # Shapefile outer rings are clockwise (negative signed area).
        if signed_area(ring) > 0:
            ring = ring[::-1]
        eff_from, eff_to = dates_for(pm.find("k:styleUrl", NS).text, balloons, maps)
        w.polyz([[list(p) for p in ring]])
        w.record(name, eff_from, eff_to)
        n += 1
    w.close()

    # Package the shapefile parts into a single zip next to the KML; no loose files are written.
    zip_path = kml_path.with_suffix(".zip")
    stem = kml_path.stem
    parts = {
        ".shp": shp.getvalue(),
        ".shx": shx.getvalue(),
        ".dbf": dbf.getvalue(),
        ".prj": WGS84_PRJ.encode("ascii"),
        ".cpg": b"UTF-8",
    }
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for ext, data in parts.items():
            zf.writestr(stem + ext, data)
    print(f"Wrote {n} features to {zip_path}")


if __name__ == "__main__":
    main(sys.argv[1])
