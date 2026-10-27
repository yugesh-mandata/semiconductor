# Semiconductor Zone Layouts — Knowledge Base

> Last updated: 2026-10-27 · Maintainer: Mandata

## 1. Purpose

This folder holds Mandata's geographic zone layouts for Korean semiconductor campuses (SK hynix and Samsung). Each layout splits a campus into zones (operating fabs, packaging/test plants, expansion sites, campus divisions) with a boundary polygon. The zones are used to link activity data to individual fabs.

---

## 2. Folder map

| Path | What it contains | Source |
| --- | --- | --- |
| `ZONE_LAYOUTS.md` | This knowledge base | Written by hand |
| `CAMPUS_MASTER.md` | Company, ISIN, campus name and address per `campus_code` | Written by hand, with sources |
| `master_layout/ZONE_BOUNDARY_MASTER.kml` | **Source of truth.** 53 zones: polygons, plus every per-zone value in each zone's Description (§6) | Google Earth export, edited in Google Earth |
| `master_layout/ZONE_MASTER.xlsx` | Master zone table: `ZONE_MASTER` (53 rows), `ZONE_LINEAGE_MASTER` (7 rows), `ZONE_OWNER_CARD_MASTER` (12 rows) and `ZONE_OWNER_FT_MASTER` (53 rows) are built from the KML. `ZONE_BOUNDARY_MASTER` and `FT_LIST_ZONE` are older sheets (§8) | `src/build_zone_master.py` |
| `master_layout/ZONE_BOUNDARY_MASTER.zip` | The KML as a zipped PolygonZ shapefile (`zone_code`, `eff_from`, `eff_to`) | `src/kml_to_shp.py` |
| `client/` | Client data-layout workbooks (`DEV_…_INFORMATION_<date>.xlsx`). The latest defines the target `FT_LIST_ZONE` layout and code lists | Client |
| `owner/` | Empty | — |

---

## 3. Layout inventory

### `master_layout`

**Campuses and zone counts by `zone_type`** (CD = campus-division rows, which carry `zone_type` `NULL`)

| `campus_code` | `campus_name` | OP | EX | OAE | CD | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `SKH_ICH` | ICHEON | 6 | 1 | 0 | 1 | 8 |
| `SKH_CJJ` | CHEONGJU | 4 | 3 | 0 | 5 | 12 |
| `SKH_YIN` | YONGIN | 0 | 1 | 0 | 1 | 2 |
| `SSE_GHG` | GIHEUNG | 3 | 0 | 0 | 1 | 4 |
| `SSE_HWA` | HWASEONG | 6 | 1 | 0 | 1 | 8 |
| `SSE_PTK` | PYEONGTAEK | 4 | 6 | 1 | 2 | 13 |
| `SSE_ONY` | ONYANG | 4 | 1 | 0 | 1 | 6 |
| **Total** | | **27** | **13** | **1** | **12** | **53** |

The KML also has an empty `SSE_CAN` (Cheonan) folder.

**Value distribution (OP zones)**

- `production_unit_type`: `FRONT_END_FAB` 19 · `PACKAGING_TEST` 8
- `primary_product_association`: `DRAM` 8 · `LOGIC` 5 · `UNKNOWN` 5 · `NAND` 3 · `HBM` 2 · `DRAM_NAND_LOGIC` 2 · `DRAM_NAND` 1 · `LOGIC_DRAM_NAND` 1
- `SSE_PTK_OAE_01` (Pyeongtaek P4) carries product `MIXED` and no unit values.

**Other columns:** `zone_type_confidence` is `HIGH` 29 · `MEDIUM` 1 · `NULL` 23. `product_association_confidence` is `HIGHLY_ASSOC` 23 · `NULL` 30.

**Known data issues:** see §8.

---

## 4. Schema

Each sheet maps to a database table. The target layout is the client's `FT_LIST_ZONE` sheet (`client/DEV_…_20261021.xlsx`), and allowed values come from its INFORMATION code list.

| Sheet | Database table |
| --- | --- |
| `ZONE_MASTER` | `FT_LIST_ZONE` |
| `ZONE_LINEAGE_MASTER` | `FT_ZONE_LINEAGE` |

### `ZONE_MASTER`

Key: (`record_id`, `pit_available_from`). `record_id` alone is **not** unique (see §5). Columns are listed in sheet order. Missing values are the text `NULL`.

| # | Column | Type | Definition | Example |
| --- | --- | --- | --- | --- |
| 1 | `record_id` | VARCHAR(40) | Identifier for a zone. Format `<campus_code>_<NNN>`. Stays the same across corrections and schema changes; a new one is issued only on a split or transform, and never reused | `SKH_ICH_001` |
| 2 | `zone_code` | VARCHAR(24) | Mandata-assigned business identifier for the geographic analysis zone. Format `<campus_code>_<zone_type>_<NN>` | `SKH_ICH_OP_01` |
| 3 | `company_name_en` | VARCHAR(40) | Disclosed listed-company name in English (from `CAMPUS_MASTER.md`) | `SK HYNIX INC` |
| 4 | `security_code` | VARCHAR(12) | ISIN identifying the listed company (from `CAMPUS_MASTER.md`) | `KR7000660001` |
| 5 | `campus_name` | VARCHAR(24) | Name of the semiconductor campus by location (from `CAMPUS_MASTER.md`) | `ICHEON` |
| 6 | `campus_code` | VARCHAR(16) | Mandata-assigned identifier for the campus. Format `<company prefix>_<campus>` (`SKH` = SK hynix, `SSE` = Samsung) | `SKH_ICH` |
| 7 | `campus_address` | VARCHAR(80) | Physical address of the semiconductor campus (from `CAMPUS_MASTER.md`) | `2091, Gyeongchung-daero, Bubal-eup, Icheon-si, Gyeonggi-do (17336)` |
| 8 | `production_unit_name` | VARCHAR(40) | Display name of the production unit. OP only; `NULL` for EX, OAE and CD zones, and for OP zones whose unit isn't known yet | `M10` |
| 9 | `production_unit_code` | VARCHAR(24) | Mandata-assigned identifier for the production unit. Format `<campus_code>_PU_<NNN>`. OP only; assigned once, never reused. Zones of the same named unit share one code (e.g. Giheung S1 spans `SSE_GHG_OP_02` and `OP_03`) | `SKH_ICH_PU_001` |
| 10 | `production_unit_type` | VARCHAR(16) | Classification of the production unit. OP only. Values: `FRONT_END_FAB`, `PACKAGING_TEST`, `MIXED`, `UNKNOWN` | `FRONT_END_FAB` |
| 11 | `zone_type` | VARCHAR(8) | High-level zone classification, equal to the third part of `zone_code`: `OP` = Operation, `EX` = Expansion, `OAE` = Operation expansion. Campus-division rows keep `CD` in the code (`SKH_ICH_CD_01`) but carry `NULL` here, because a campus division is a level, not a zone type. Others (`OTH`) is calculated as CD − OP − EX − OAE and never stored | `OP` |
| 12 | `zone_type_confidence` | VARCHAR(8) | Confidence of the zone-type classification. Values: `HIGH`, `MEDIUM`, `LOW` | `HIGH` |
| 13 | `primary_product_association` | VARCHAR(16) | Primary product family associated with the zone; association does not represent direct production measurement. OP and OAE only (EX and CD `NULL` for now). Values: `HBM`, `DRAM`, `NAND`, `LOGIC`, `MIXED`, `UNKNOWN`, or for now `_`-joined combinations such as `DRAM_NAND_LOGIC` instead of `MIXED` (see §8) | `DRAM` |
| 14 | `product_association_confidence` | VARCHAR(16) | Confidence of the product association. Values: `HIGHLY_ASSOC`, `ASSOC`, `UNCERTAIN` | `NULL` |
| 15 | `effective_from` | DATE | Date from which this zone definition is valid in the real world | `2020-01-01` |
| 16 | `effective_to` | DATE | Last date this zone definition is valid. `NULL` while currently valid | `NULL` |
| 17 | `pit_available_from` | DATE | Date from which this specific record version became available to clients. For backfilled history (rows covering the period before the first client release), set equal to `effective_from` | `2020-01-01` |
| 18 | `pit_available_to` | DATE | Date until which this specific record version was available to clients. `NULL` for the currently available version. For backfilled history (rows covering the period before the first client release), set equal to `effective_to` | `NULL` |
| 19 | `imagery_acquired_date` | DATE | Date the satellite image used to draw this zone's boundary was taken | `2020-03-08` |
| 20 | `record_created_at` | DATETIME (UTC) | Date and time this record version was created. Set by the build; never edited | `2026-10-22 02:42` |
| 21 | `polygon` | TEXT | Zone boundary as raw KML coordinates (see §6). Longest value in data: 1,544 characters | `127.4797427,37.2514443,0 127.4797427,37.2500277,0 …` |

**Naming convention:** `_date` = DATE, `_at` = timestamp. The `…_from` / `…_to` pairs are DATEs.

**Why two separate date columns:** `imagery_acquired_date` describes the *evidence* (what the satellite saw, and when). `record_created_at` describes *our process* (when we wrote the row). They are often months apart, and clients need the imagery date to judge how fresh a boundary is.

### `ZONE_OWNER_CARD_MASTER`

Campus-division zones only: one row per current campus division in `ZONE_MASTER` (`CD` as the third part of `zone_code`, and `pit_available_to = NULL`), in `ZONE_MASTER` order. No database table yet.

| # | Column | Type | Description | Example |
| --- | --- | --- | --- | --- |
| 1 | `zone_code` | VARCHAR(24) | `zone_code` from `ZONE_MASTER` | `SKH_ICH_CD_01` |
| 2 | `polygon` | TEXT | `polygon` from `ZONE_MASTER` (raw KML coordinates) | `127.47929,37.25468,0 …` |

### `ZONE_OWNER_FT_MASTER`

The zone list for the foot-traffic data owner (KT): every zone in `ZONE_MASTER`, campus divisions and ended zones included, one row per `record_id` (its version with the latest `pit_available_from`), in `ZONE_MASTER` order. The effective dates say which period to extract for each zone. No database table yet.

| # | Column | Type | Description | Example |
| --- | --- | --- | --- | --- |
| 1 | `zone_code` | VARCHAR(24) | `zone_code` from `ZONE_MASTER` | `SKH_ICH_EX_01` |
| 2 | `effective_from` | DATE | `effective_from` from `ZONE_MASTER` | `2020-01-01` |
| 3 | `effective_to` | DATE | `effective_to` from `ZONE_MASTER`; `NULL` while the zone is valid | `2021-06-30` |
| 4 | `polygon` | TEXT | `polygon` from `ZONE_MASTER` (raw KML coordinates) | `127.4797427,37.2514443,0 …` |

### `ZONE_LINEAGE_MASTER`

Records how zones evolve, so users can trace an expansion zone into the operating zones it became, and an operating zone through its operation-expansion (OAE) works. Built from the KML (§6). Key: `lineage_id`.

| # | Column | Type | Definition | Example |
| --- | --- | --- | --- | --- |
| 1 | `lineage_id` | VARCHAR(40) | Unique identifier for a lineage record. Format `LIN_<campus>_<NNN>` | `LIN_ICH_001` |
| 2 | `parent_record_id` | VARCHAR(40) | `record_id` of the zone that existed before the transition: EX, OP or OAE | `SKH_ICH_007` |
| 3 | `child_record_id` | VARCHAR(40) | `record_id` of the zone created by the transition | `SKH_ICH_005` |
| 4 | `relationship_type` | VARCHAR(16) | `TRANSFORM` = one zone replaces the parent with an unchanged polygon (EX → OP, EX → OAE, OP → OAE, OAE → OP). `SPLIT` = several zones replace an EX zone, inside its polygon | `TRANSFORM` |
| 5 | `effective_at` | DATE | Date the transition took effect: the child's `effective_from`; the parent's `effective_to` is the day before | `2021-07-01` |
| 6 | `pit_available_from` | DATE | Date from which this lineage record became available to clients. Backfill: `effective_at` | `2021-07-01` |
| 7 | `pit_available_to` | DATE | Date until which this lineage record version was available to clients. `NULL` while current | `NULL` |

---

## 5. How to track changes

Two time axes are tracked separately:

- **Real world:** `effective_from` / `effective_to`. When the zone exists on the ground.
- **Client availability (point-in-time):** `pit_available_from` / `pit_available_to`. When a version of the record was published to clients.

**Which rule applies**

| Change | `record_id` | Lineage row? | Case |
| --- | --- | --- | --- |
| Expansion completed (split or transform) | **New** | Yes | 1 |
| OAE works start (OP → OAE) or end (OAE → OP), or an EX starts operating while construction continues in the same building (EX → OAE) | **New** | Yes (`TRANSFORM`) | 1 |
| Value correction, column definition change, column added | **Same** | No | 2 |

### Date columns at a glance

| Column | Answers | Set by |
| --- | --- | --- |
| `imagery_acquired_date` | What did we see, and when? | Satellite image metadata |
| `effective_from` / `effective_to` | When is the zone real on the ground? | Analyst |
| `record_created_at` | When did we write this row? | Build, automatically |
| `pit_available_from` / `pit_available_to` | When could clients see this row? | Publishing process |

**Rules**

- `imagery_acquired_date` ≤ `record_created_at`: you can't trace an image you don't have yet.
- `record_created_at` ≤ `pit_available_from`: you can't publish before creating. **Exception:** backfilled history (before the first client release) uses `pit_available_from` = `effective_from` and `pit_available_to` = `effective_to` (client spec; see §8, issues 2–3).
- `imagery_acquired_date` is **not** `effective_from`. The image is evidence that the zone existed on that day; the zone may have been valid much earlier.
- Both `imagery_acquired_date` and `record_created_at` are set **per row version**.

### Case 1: When an expansion is completed

1. Set `effective_to` on the expansion zone.
2. Add the zones that become operational, each with a new `record_id` and an `effective_from` on the day after.
3. The build adds the lineage rows (§6).

**Example** (illustrative, after the first client release; these zones don't exist in the data)

| record_id | zone_code | production_unit_code | zone_type | effective_from | effective_to | pit_available_from | pit_available_to |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKH_ICH_901` | `SKH_ICH_EX_09` | `NULL` | `EX` | 2026-01-01 | 2027-06-30 | 2026-01-05 | `NULL` |
| `SKH_ICH_902` | `SKH_ICH_OP_09` | `SKH_ICH_PU_901` | `OP` | 2027-07-01 | `NULL` | 2027-07-05 | `NULL` |
| `SKH_ICH_903` | `SKH_ICH_OP_10` | `SKH_ICH_PU_902` | `OP` | 2027-07-01 | `NULL` | 2027-07-05 | `NULL` |

Lineage: `SKH_ICH_901` → `SKH_ICH_902` and `SKH_ICH_901` → `SKH_ICH_903`, both `SPLIT`, `effective_at` 2027-07-01. The expansion zone stops being valid on 2027-06-30 but stays available to clients (`pit_available_to` = `NULL`), because the record itself wasn't wrong.

### Case 2: When a record is changed (correction, column definition change, column addition)

`record_id` stays the same, and no lineage row is added.

1. Set `pit_available_to` on the current row.
2. Add a new row with the same `record_id`, a new `pit_available_from`, a new `record_created_at`, and a null `pit_available_to`. Update `imagery_acquired_date` only if newer imagery was used.

---

## 6. Building `ZONE_MASTER` from the KML

The KML is the source of truth. Edit zones in Google Earth, export the KML into `master_layout/`, then rebuild. Any edits made directly in the workbook are overwritten by the next build.

### KML requirements

- One folder per campus, named with the campus code (`SKH_ICH`). Every placemark sits directly inside a folder.
- Placemark name = `zone_code`. One outer ring per placemark, with no holes.
- Each zone's **Description** (Google Earth edit panel, `<>` HTML view) holds these 14 lines, in this order, following the §4 rules:
  ```html
  <!DOCTYPE html>
  <html>
    <h1>record_id: SKH_ICH_001</h1>
    <h1>zone_code: SKH_ICH_OP_01</h1>
    <h1>production_unit_name: M10</h1>
    <h1>production_unit_code: SKH_ICH_PU_001</h1>
    <h1>production_unit_type: FRONT_END_FAB</h1>
    <h1>zone_type: OP</h1>
    <h1>zone_type_confidence: HIGH</h1>
    <h1>primary_product_association: DRAM</h1>
    <h1>product_association_confidence: NULL</h1>
    <h1>effective_from: 2020-01-01</h1>
    <h1>effective_to: NULL</h1>
    <h1>pit_available_from: 2020-01-01</h1>
    <h1>pit_available_to: NULL</h1>
    <h1>imagery_acquired_date: 2020-03-08</h1>
  </html>
  ```
- Google Earth stores the Description as the balloon text (`<BalloonStyle><text>`) of the zone's style, not as a `<description>` element. **Every zone needs its own style.** If two zones share one, editing one zone's Description changes both, and the build stops.

### Mapping

| `ZONE_MASTER` column | Source |
| --- | --- |
| The 14 Description fields | Copied as written |
| `company_name_en`, `security_code`, `campus_name`, `campus_address` | `CAMPUS_MASTER.md`, joined on `campus_code` |
| `campus_code` | First two parts of `zone_code`; must equal the KML folder name |
| `record_created_at` | Build time, UTC |
| `polygon` | `<coordinates>` text with whitespace collapsed: `lon,lat,0` points (longitude first) separated by single spaces, closed ring |

**Lineage:** the build derives `ZONE_LINEAGE_MASTER`. An EX zone gets a `TRANSFORM` row when a zone in the same campus with an **identical** polygon starts the day after its `effective_to`, or `SPLIT` rows when several zones inside its polygon start that day. If an EX zone ends with no successor, the build prints a warning.

### How to rebuild

Run from the repo root, with `ZONE_MASTER.xlsx` closed in Excel.

```
git pull --no-rebase origin main
.venv/bin/pip install -r requirements.txt     # first time only
.venv/bin/python src/build_zone_master.py layouts/master_layout/ZONE_BOUNDARY_MASTER.kml
.venv/bin/python src/kml_to_shp.py layouts/master_layout/ZONE_BOUNDARY_MASTER.kml
.venv/bin/python src/validate_shp.py layouts/master_layout/ZONE_BOUNDARY_MASTER.kml
```

- **What the build does:** it replaces `ZONE_MASTER`, `ZONE_LINEAGE_MASTER`, `ZONE_OWNER_CARD_MASTER` and `ZONE_OWNER_FT_MASTER` and leaves the other sheets alone. It then runs `src/validate_zone_master.py`, which re-reads the KML and the workbook without sharing any code with the build.
- **Before committing:** both validators must print `ALL CHECKS PASSED`, and you should read the build's `WARNING` lines.

**Initial population (2026-10-22):** the 14 Description fields were generated once and written into the KML.
- `record_id` and `production_unit_code` were numbered per campus in KML order.
- OP unit and product values came from a draft GeoJSON (old zone codes), but only where the draft zone with the same code still had the same boundary (IoU ≥ 0.8). Where the code had been reassigned to another building, they were set to `NULL`.
- `zone_type_confidence` came from the draft's `location_confidence`.

---

## 7. Loading into AWS RDS MySQL

Use MySQL 8.0 or 8.4. Version 5.7 ignores SRIDs in calculations and is past end of life.

**Table**

```sql
CREATE TABLE ft_list_zone (
  record_id             VARCHAR(40) NOT NULL,
  zone_code             VARCHAR(24) NOT NULL,
  -- ... columns 3–18 as in §4 ...
  imagery_acquired_date DATE        NULL,
  record_created_at     DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- store UTC
  polygon               POLYGON     NOT NULL SRID 4326,
  CHECK (imagery_acquired_date IS NULL OR imagery_acquired_date <= DATE(record_created_at)),
  CHECK (pit_available_from >= DATE(record_created_at)),
  PRIMARY KEY (record_id, pit_available_from),
  SPATIAL INDEX idx_zone_polygon (polygon)
);
```

- **`SRID 4326`** means longitude/latitude on WGS84, the same system the KML uses. `NOT NULL` and `SRID` are both required for the spatial index to be built and used.
- **`record_id` is not `AUTO_INCREMENT`.** It is assigned by Mandata and repeats across versions (§5).
- **Backfilled rows fail the second `CHECK`** (`pit_available_from` = `effective_from` is before `record_created_at`). See §8, issue 3.

**Convert the polygon before inserting.** The sheet stores raw KML text, but MySQL needs WKT: drop the altitude, separate longitude and latitude with a space, and separate points with commas.

```python
def kml_to_wkt(raw: str) -> str:
    pts = (p.split(",")[:2] for p in raw.split())
    return "POLYGON((" + ", ".join(f"{lon} {lat}" for lon, lat in pts) + "))"
```

**Insert and read with explicit axis order.** For SRID 4326, MySQL assumes latitude comes first, but our data is longitude-first:

```sql
INSERT INTO ft_list_zone (record_id, zone_code, pit_available_from, polygon)
VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326, 'axis-order=long-lat'));

SELECT zone_code, ST_AsText(polygon, 'axis-order=long-lat') FROM ft_list_zone;
```

If you leave out `axis-order=long-lat`, the insert fails, because longitude 127 is read as a latitude (out of range).

**NULLs:** the sheet stores missing values as the text `NULL`. Convert them to real NULLs, for example with `NULLIF(@col, 'NULL')` in `LOAD DATA`, or in the loader code.

**Useful queries**

```sql
-- zone containing a point
SELECT zone_code FROM ft_list_zone
WHERE ST_Contains(polygon, ST_GeomFromText('POINT(127.486 37.2507)', 4326, 'axis-order=long-lat'));

-- area in m²
SELECT zone_code, ST_Area(polygon) AS area_m2 FROM ft_list_zone;

-- shape check after loading (MySQL doesn't validate shapes on insert)
SELECT zone_code FROM ft_list_zone WHERE NOT ST_IsValid(polygon);
```

---

## 8. Open issues

| # | Issue | Location | Owner |
| --- | --- | --- | --- |
| 2 | Backfill sets `pit_available_to` = `effective_to`, but `effective_to` is the zone's last valid day and the backtest rule excludes it (`as-of < pit_available_to`). A backfilled zone is therefore hidden on its last valid day. `effective_to` + 1 day would close the gap | 7 ended EX zones | TBD |
| 3 | Backfill sets `pit_available_from` = `effective_from`, which breaks `record_created_at ≤ pit_available_from` and the MySQL `CHECK` (§7) | All rows | TBD |
| 4 | `primary_product_association` uses combined values (`DRAM_NAND`, `DRAM_NAND_LOGIC`, `LOGIC_DRAM_NAND`) that aren't in the client code list, which has only `MIXED`. Kept as written for now; `src/validate_zone_master.py` accepts `_`-joined combinations of `HBM`/`DRAM`/`NAND`/`LOGIC` | `SSE_PTK` OP zones | TBD |
| 5 | `zone_type_confidence` is `NULL` for 23 zones, and `product_association_confidence` for 30 | `ZONE_MASTER` | TBD |
| 6 | Sheets `ZONE_BOUNDARY_MASTER` and `FT_LIST_ZONE` still hold the old 34 zones; the build doesn't touch them | `ZONE_MASTER.xlsx` | TBD |
| 7 | `SKH_CJJ_EX_02` and `SSE_PTK_EX_04` ended in 2026; if that's after the first client release, they aren't backfill and should follow the normal publishing rules | `ZONE_MASTER` | TBD |
| 8 | `owner/` folder is empty; its purpose is undocumented | `layouts/` | TBD |

**Resolved (2026-10-27)**

- **Issue 1 (`zone_type` `MX`):** `SSE_PTK_MX_01` (Pyeongtaek P4) is now OAE, `SSE_PTK_OAE_01`: it started operating on 2026-07-01 while construction continues in the same building. Its unit fields are `NULL`, its product `HBM_DRAM_NAND` became `MIXED`, and `MX_HANDLING` was removed from the build. `record_id` `SSE_PTK_005` is unchanged (a correction), and the lineage row from `SSE_PTK_EX_04` is now EX → OAE.

**Resolved (2026-10-22, with the 53-zone KML)**

- **Old issues 1, 4 (duplicate `SKH_ICH_OP_01`, `RD` zone type):** gone. The KML was renumbered, and `RD` no longer occurs.
- **Old issues 2, 8 (inconsistent unit codes such as `SKH_ICH_PCK`, `SKH_YIN_EX`):** replaced by the client format `<campus_code>_PU_<NNN>`.
- **Old issue 3 (`sk_hynix…` file name):** the KML is now `ZONE_BOUNDARY_MASTER.kml`.
- **Old issues 5, 6, 7 (spec vs data format, empty columns, unused Location confidence):**
  - `record_id`, company, campus and date columns are filled in the spec format.
  - Location confidence became `zone_type_confidence` where the zone was unchanged.
- **Backfill rule for `pit_available_to`:** set equal to `effective_to`, now also in the client spec.
- **`check_status(TEMP)` test column:** removed from `ZONE_MASTER`. It ran to row 1,048,576, and the file shrank from 5.6 MB to 26 KB.
- **Earlier:** date columns `record_created_at` and `imagery_acquired_date` added (2026-10-12). `record_id` identifies a zone, not one version of it (2026-10-12).

---

## 9. Changelog

| Date | Change |
| --- | --- |
| 2026-10-27 | `ZONE_OWNER_FT_MASTER` is now built from `ZONE_MASTER`: all 53 zones with `zone_code`, `effective_from`, `effective_to` and `polygon`, replacing the old 34-zone list. Build and validator updated; added to §2, §4, §6, §8 |
| 2026-10-27 | Campus-division rows: `zone_type` `CD` → `NULL` (12 rows); the code keeps `CD`, and the build and validator now find campus divisions by `zone_code`. `SSE_PTK_MX_01` → `SSE_PTK_OAE_01` (P4; open issue 1 resolved); `TRANSFORM` now also allows EX → OAE. Sheets renamed: `ZONE_SAMSUNG_CARD_MASTER` → `ZONE_OWNER_CARD_MASTER`, `ZONE_OWNER_MASTER` → `ZONE_OWNER_FT_MASTER`. Updated §2–§6, §8 |
| 2026-10-26 | Lineage: `TRANSFORM` now also links OP → OAE and OAE → OP (unchanged polygon); `SPLIT` stays EX-only. Updated §4 (`zone_type`, lineage columns) and the §5 rule table; build and validator updated, validator accepts `zone_type` `OAE` |
| 2026-10-22 | Added the built sheet `ZONE_SAMSUNG_CARD_MASTER` (`zone_code`, `polygon`, same names as `ZONE_MASTER`) for the 12 current CD zones; build and validator updated |
| 2026-10-22 | Rebuilt for the 53-zone KML: the KML is now the source of truth, with per-zone values in each zone's Google Earth Description (§6). Updated folder map, inventory, schema (sheet column order, PU code format, client code lists, backfill rule for `pit_available_from/to`), lineage (`TRANSFORM` / `SPLIT`), open issues. Merged the separate build guide into §6 |
| 2026-10-12 | Resolved open issue #10 (date columns applied to `ZONE_MASTER`: `record_created_at`, `imagery_acquired_date`); discarded #11 (multiple images / `imagery_source_id`) |
| 2026-10-12 | Added `record_created_at` (replaces `recorded_at`) and `imagery_acquired_date` to `ZONE_MASTER`; added "Date columns at a glance" with date rules; updated Case 2, MySQL DDL and open issues #10–11 |
| 2026-10-12 | Initial version: folder map, `master_layout` inventory, schema for `ZONE_MASTER` / `ZONE_LINEAGE_MASTER`, change-tracking cases, ingestion rules, RDS MySQL loading guide, open issues |
