# Semiconductor Zone Layouts — Knowledge Base

> Last updated: 2026-10-12 · Maintainer: Mandata

## 1. Purpose

This folder holds Mandata's geographic zone layouts for Korean semiconductor campuses (SK hynix and Samsung). Each layout splits a campus into zones (operating fabs, packaging/test plants, expansion sites) with a boundary polygon. The zones are used to link activity data to individual fabs.

---

## 2. Folder map

| Path | What it contains | Source | Date (KST) |
| --- | --- | --- | --- |
| `README.md` | This knowledge base | Written by hand | 2026-10-12 |
| `master_layout/` | The master zone layout (the only populated layout) | — | 2026-10-12 |
| `master_layout/sk_hynix_polygon_boundary.kml` | 34 zone polygons with attributes, plus 2 test shapes. Contains both SK hynix **and** Samsung zones despite the name | Google Earth export, itself "converted from `semiconductor_draft_v1.geojson`" (per the KML folder description) | 2026-10-08 |
| `master_layout/SEMICONDUCTOR_ZONE_MASTER_LOCKED.xlsx` | Master zone table: sheets `ZONE_MASTER` (34 rows) and `ZONE_LINEAGE_MASTER` (empty) | Populated from the KML above (see §6) | 2026-10-12 |
| `master_layout/SEMICONDUCTOR_ZONE_MASTER_LOCKED_backup_20261012.xlsx` | Copy of the workbook before population (headers only) | Backup | 2026-10-12 |
| `client/` | Empty | — | 2026-10-09 |
| `owner/` | Empty | — | 2026-10-09 |

---

## 3. Layout inventory

### `master_layout`

- **Source file:** `sk_hynix_polygon_boundary.kml` (KML document `sk_hynix`, top folder `semiconductor_draft_v1`)
- **Output file:** `SEMICONDUCTOR_ZONE_MASTER_LOCKED.xlsx` → sheet `ZONE_MASTER`
- **Zones:** 34. The KML also contains 2 test shapes, `TEST_123` and `TEST_123_123`, with no attributes; they were skipped.
- **KML colour key:** OP blue, EX orange, RD purple (per the KML folder description).

**Campuses and zone counts by `zone_type`**

| `campus_code` | Campus (KML folder label) | OP | EX | RD | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| `SKH_ICH` | SK hynix Icheon | 5 | 0 | 1 | 6 |
| `SKH_CJJ` | SK hynix Cheongju | 4 | 2 | 0 | 6 |
| `SKH_YIN` | SK hynix Yongin | 0 | 1 | 0 | 1 |
| `SSE_GHG` | Samsung Giheung | 3 | 0 | 0 | 3 |
| `SSE_HWA` | Samsung Hwaseong | 6 | 0 | 0 | 6 |
| `SSE_PTK` | Samsung Pyeongtaek | 5 | 2 | 0 | 7 |
| `SSE_ONY` | Samsung Onyang | 4 | 1 | 0 | 5 |
| **Total** | | **27** | **6** | **1** | **34** |

**Value distribution**

- `production_unit_type`: `FRONT_END_FAB` 22 · `PACKAGING_TEST` 10 · `UNKNOWN` 1 · `NULL` 1
- `primary_product_association`: `DRAM` 11 · `UNKNOWN` 10 · `LOGIC` 5 · `MIXED` 3 · `HBM` 2 · `NAND` 2 · `NULL` 1

**Populated vs empty columns:** only `zone_code`, `campus_code`, `production_unit_name`, `production_unit_code`, `production_unit_type`, `zone_type`, `primary_product_association` and `polygon` hold values. All other columns, including `record_id` and every date column, are `NULL`, because the KML doesn't contain them.

**Known data issues:** see §8.

---

## 4. Schema

Each sheet maps to a database table:

| Sheet | Database table |
| --- | --- |
| `ZONE_MASTER` | `FT_LIST_ZONE` |
| `ZONE_LINEAGE_MASTER` | `FT_ZONE_LINEAGE` |

**Reading the examples:** where real data exists, the example uses the real format (e.g. `SKH_ICH_OP_03`, `SKH_ICH`). Where every value is still `NULL` (company, ISIN, campus name/address, confidence, dates), the example is illustrative and comes from the schema specification.

### `ZONE_MASTER`

Key: (`record_id`, `pit_available_from`). `record_id` alone is **not** unique (see §5).

| # | Column | Type | Definition | Example |
| --- | --- | --- | --- | --- |
| 1 | `record_id` | VARCHAR(40) | Identifier for a zone. Stays the same across corrections and schema changes; a new one is issued only when the zone is merged, split or replaced. Unique together with `pit_available_from` | `SK_ICH_001` |
| 2 | `zone_code` | VARCHAR(24) | Mandata-assigned business identifier for the geographic analysis zone. Format `<campus_code>_<zone_type>_<NN>` | `SKH_ICH_OP_03` |
| 3 | `company_name_en` | VARCHAR(40) | Disclosed listed-company name in English | `SK HYNIX INC` |
| 4 | `security_code` | VARCHAR(12) | ISIN identifying the listed company | `KR7000660001` |
| 5 | `campus_name` | VARCHAR(24) | Name of the semiconductor campus by location | `ICHEON` |
| 6 | `campus_code` | VARCHAR(16) | Mandata-assigned identifier for the campus. Format `<company prefix>_<campus>` (`SKH` = SK hynix, `SSE` = Samsung) | `SKH_ICH` |
| 7 | `campus_address` | VARCHAR(80) | Physical address of the semiconductor campus | `2091 Gyeongchung-daero, Bubal-eup, Icheon-si` |
| 8 | `production_unit_name` | VARCHAR(40) | Display name of the production unit associated with the zone. `NULL` for expansion and campus-division zones | `M16` |
| 9 | `production_unit_code` | VARCHAR(24) | Mandata-assigned identifier for the production unit. `NULL` for expansion and campus-division zones | `SKH_ICH_M16` |
| 10 | `production_unit_type` | VARCHAR(16) | Classification of the production unit. `NULL` for expansion and campus-division zones. Values in data: `FRONT_END_FAB`, `PACKAGING_TEST`, `UNKNOWN` | `FRONT_END_FAB` |
| 11 | `zone_type` | VARCHAR(8) | High-level zone classification: `OP` = Operation, `EX` = Expansion, `CD` = Campus Division. The data also contains `RD` (undefined, see §8) | `OP` |
| 12 | `zone_type_confidence` | VARCHAR(8) | Confidence level assigned to the zone-type classification | `HIGH` |
| 13 | `primary_product_association` | VARCHAR(16) | Primary product family associated with the zone; association does not represent direct production measurement. Values in data: `DRAM`, `NAND`, `HBM`, `LOGIC`, `MIXED`, `UNKNOWN` | `DRAM` |
| 14 | `product_association_confidence` | VARCHAR(16) | Confidence level of the product-association classification | `HIGHLY_ASSOC` |
| 15 | `effective_from` | DATE | Date from which this zone definition is valid in the real world | `2027-07-01` |
| 16 | `effective_to` | DATE | Date until which this zone definition is valid. `NULL` while currently valid | `NULL` |
| 17 | `pit_available_from` | DATE | Date from which this specific record version became available to clients | `2027-07-05` |
| 18 | `pit_available_to` | DATE | Date until which this specific record version was available to clients. `NULL` for the currently available version | `NULL` |
| 19 | `record_created_at` | DATETIME (UTC) | Date and time this record version was created in Mandata's system. Set automatically; never edited. Renamed from `recorded_at` on 2026-10-12 | `NULL` |
| 20 | `polygon` | TEXT | Zone boundary as raw KML coordinates (see §6). Longest value in data: 322 characters | `127.4841047,37.2500254,0 127.487888,37.250039,0 …` |
| 21 | `imagery_acquired_date` | DATE | Date the satellite image used to draw this zone's boundary was taken. Comes from the image metadata. Added 2026-10-12 | `NULL` |

**Naming convention:** `_date` = DATE, `_at` = timestamp. The `…_from` / `…_to` pairs are DATEs.

**Why two separate date columns:** `imagery_acquired_date` describes the *evidence* (what the satellite saw, and when). `record_created_at` describes *our process* (when we wrote the row). They are often months apart, and clients need the imagery date to judge how fresh a boundary is. Names like `captured_at` or `recorded_at` were avoided because they don't say whether they refer to the image or to the record.

### `ZONE_LINEAGE_MASTER`

Records how zones evolve from one state to another, so users can trace splits, merges and replacements across time. Currently empty. Key: `lineage_id`.

| # | Column | Type | Definition | Example |
| --- | --- | --- | --- | --- |
| 1 | `lineage_id` | VARCHAR(40) | System-generated unique identifier for a zone-lineage relationship record | `LIN_ICH_001` |
| 2 | `parent_record_id` | VARCHAR(40) | `record_id` of the zone that existed before the transition | `SK_ICH_001` |
| 3 | `child_record_id` | VARCHAR(40) | `record_id` of the zone created as a result of the transition | `SK_ICH_002` |
| 4 | `relationship_type` | VARCHAR(16) | How the child zone relates to the parent. Typical values: `SPLIT`, `MERGE`, `REPLACED_BY` | `SPLIT` |
| 5 | `effective_at` | DATE | Real-world date on which the zone transition took effect | `2027-07-01` |
| 6 | `pit_available_from` | DATE | Date from which this lineage relationship became available to clients | `2027-07-05` |
| 7 | `pit_available_to` | DATE | Date until which this particular lineage record version was available to clients. `NULL` while current | `NULL` |

---

## 5. How to track changes

Two time axes are tracked separately:

- **Real world:** `effective_from` / `effective_to`. When the zone exists on the ground.
- **Client availability (point-in-time):** `pit_available_from` / `pit_available_to`. When a version of the record was published to clients.

**Which rule applies**

| Change | `record_id` | Lineage row? | Case |
| --- | --- | --- | --- |
| Expansion completed, zone split / merged / replaced | **New** | Yes | 1 |
| Value correction, column definition change, column added | **Same** | No | 2 |

### Date columns at a glance

Each `ZONE_MASTER` row carries four kinds of date:

| Column | Answers | Set by |
| --- | --- | --- |
| `imagery_acquired_date` | What did we see, and when? | Satellite image metadata |
| `effective_from` / `effective_to` | When is the zone real on the ground? | Analyst |
| `record_created_at` | When did we write this row? | System, automatically |
| `pit_available_from` / `pit_available_to` | When could clients see this row? | Publishing process |

**Rules**

- `imagery_acquired_date` ≤ `record_created_at`: you can't trace an image you don't have yet.
- `record_created_at` ≤ `pit_available_from`: you can't publish before creating.
- `imagery_acquired_date` is **not** `effective_from`. The image is evidence that the zone existed on that day; the zone may have been valid much earlier.
- Both `imagery_acquired_date` and `record_created_at` are set **per row version**:
  - in Case 1, each new zone gets its own;
  - in Case 2, a new version gets a new `record_created_at`, and a new `imagery_acquired_date` if newer imagery was used.

### Case 1: When an expansion is completed

1. Set `effective_to` on the expansion zone.
2. Add the zones that become operational after the expansion is completed, each with a new `record_id`.
3. Add a row per new zone to `FT_ZONE_LINEAGE`.

**Example**

The values below are illustrative. The zone and campus codes follow the real format, but these zones don't exist in the data. `record_created_at`, `polygon` and `imagery_acquired_date` are omitted for width.

`FT_LIST_ZONE`

| record_id | zone_code | company_name_en | security_code | campus_name | campus_code | campus_address | production_unit_name | production_unit_code | production_unit_type | zone_type | zone_type_confidence | primary_product_association | product_association_confidence | effective_from | effective_to | pit_available_from | pit_available_to |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SK_ICH_001` | `SKH_ICH_EX_01` | SK HYNIX INC | KR7000660001 | ICHEON | SKH_ICH | 2091 Gyeongchung-daero, Bubal-eup, Icheon-si | `NULL` | `NULL` | `NULL` | `EX` | HIGH | `UNKNOWN` | LOW | 2026-01-01 | 2027-06-30 | 2026-01-05 | `NULL` |
| `SK_ICH_002` | `SKH_ICH_OP_02` | SK HYNIX INC | KR7000660001 | ICHEON | SKH_ICH | 2091 Gyeongchung-daero, Bubal-eup, Icheon-si | New Fab Area | `SKH_ICH_FAB01` | `FRONT_END_FAB` | `OP` | HIGH | HBM | HIGHLY_ASSOC | 2027-07-01 | `NULL` | 2027-07-05 | `NULL` |
| `SK_ICH_003` | `SKH_ICH_OP_03` | SK HYNIX INC | KR7000660001 | ICHEON | SKH_ICH | 2091 Gyeongchung-daero, Bubal-eup, Icheon-si | New P&T Area | `SKH_ICH_PT01` | `PACKAGING_TEST` | `OP` | HIGH | HBM | HIGHLY_ASSOC | 2027-07-01 | `NULL` | 2027-07-05 | `NULL` |
| `SK_ICH_004` | `SKH_ICH_CD_01` | SK HYNIX INC | KR7000660001 | ICHEON | SKH_ICH | 2091 Gyeongchung-daero, Bubal-eup, Icheon-si | `NULL` | `NULL` | `NULL` | `CD` | HIGH | `NULL` | `NULL` | 2026-01-01 | `NULL` | 2026-01-05 | `NULL` |

`FT_ZONE_LINEAGE`

| lineage_id | parent_record_id | child_record_id | relationship_type | effective_at | pit_available_from | pit_available_to |
| --- | --- | --- | --- | --- | --- | --- |
| `LIN_ICH_001` | `SK_ICH_001` | `SK_ICH_002` | `SPLIT` | 2027-07-01 | 2027-07-05 | `NULL` |
| `LIN_ICH_002` | `SK_ICH_001` | `SK_ICH_003` | `SPLIT` | 2027-07-01 | 2027-07-05 | `NULL` |

The expansion zone `SK_ICH_001` stops being valid in the real world on 2027-06-30 (`effective_to`). It stays available to clients (`pit_available_to` = `NULL`), because the record itself wasn't wrong. The campus-division zone `SK_ICH_004` is unaffected.

### Case 2: When a record is changed (correction, column definition change, column addition)

`record_id` stays the same, and no lineage row is added.

1. Set `pit_available_to` on the current row.
2. Add a new row with the same `record_id`, a new `pit_available_from`, a new `record_created_at`, and a null `pit_available_to`. Update `imagery_acquired_date` only if newer imagery was used.

---

## 6. Ingestion rules (KML → `ZONE_MASTER`)

**Which placemarks are ingested:** every placemark that carries zone attributes (34). Placemarks without attributes (`TEST_123`, `TEST_123_123`) are skipped.

**Field mapping**

| KML field (`ExtendedData`) | `ZONE_MASTER` column |
| --- | --- |
| Zone code | `zone_code` |
| Campus code | `campus_code` |
| Production unit name | `production_unit_name` |
| Production unit code | `production_unit_code` |
| Production unit type | `production_unit_type` |
| Zone type | `zone_type` |
| Primary associated product | `primary_product_association` |
| `<Polygon>/<outerBoundaryIs>/<LinearRing>/<coordinates>` | `polygon` |
| Location confidence | *not ingested; no matching column* |

**Value rules**

- **Values are copied exactly as written.** The KML's pop-up tables (descriptions) were checked against its attribute fields, and they never conflict.
- **Every unmapped column is the text `NULL`.**
- **Placeholders `???` (including `SKH_ICH_???`) and `n/a` become `NULL`.** `UNKNOWN` is kept as written. Four cells were affected:
  - `SKH_ICH_OP_01` (RD row): `production_unit_name`, `production_unit_code`
  - `SKH_YIN_EX_01`: `production_unit_type`, `primary_product_association`
- **`polygon` is the raw KML coordinate text.** Only the line breaks and tabs from the file's indentation are removed. Format:
  - points are `lon,lat,alt` (longitude first), separated by single spaces
  - `alt` is always `0`
  - the outline is closed: the last point repeats the first
  - outer boundary only; no zone has holes or multiple parts

  ```
  127.4841047,37.2500254,0 127.487888,37.250039,0 127.487873,37.251528,0 127.4841022,37.2515,0 127.4841047,37.2500254,0
  ```

**Validation (2026-10-12):** all 34 rows matched the KML cell for cell. Every polygon is closed and lies within Korea, and no polygon appears twice.

---

## 7. Loading into AWS RDS MySQL

Use MySQL 8.0 or 8.4. Version 5.7 ignores SRIDs in calculations and is past end of life.

**Table**

```sql
CREATE TABLE ft_list_zone (
  record_id             VARCHAR(40) NOT NULL,
  zone_code             VARCHAR(24) NOT NULL,
  -- ... columns 3–18 as in §4 ...
  pit_available_from    DATE        NOT NULL,
  pit_available_to      DATE        NULL,
  record_created_at     DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- store UTC
  polygon               POLYGON     NOT NULL SRID 4326,
  imagery_acquired_date DATE        NULL,
  CHECK (imagery_acquired_date IS NULL OR imagery_acquired_date <= DATE(record_created_at)),
  CHECK (pit_available_from >= DATE(record_created_at)),
  PRIMARY KEY (record_id, pit_available_from),
  SPATIAL INDEX idx_zone_polygon (polygon)
);
```

- **`SRID 4326`** means longitude/latitude on WGS84, the same system the KML uses. `NOT NULL` and `SRID` are both required for the spatial index to be built and used.
- **`record_id` is not `AUTO_INCREMENT`.** It is assigned by Mandata and repeats across versions (§5).

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

**Blocker:** `record_id` and `pit_available_from` are `NULL` in every row today, so the primary key can't be filled until they are assigned (see §8).

---

## 8. Open issues

| # | Issue | Location | Owner |
| --- | --- | --- | --- |
| 1 | Duplicate `zone_code` `SKH_ICH_OP_01`: one row is M10 (`OP`); the other has unit `???` and `zone_type` `RD`, which contradicts the `OP` in its code | KML placemarks `5F2C60018F000005` and `5F2C60018F000006`; `ZONE_MASTER` rows 4–5 | TBD |
| 2 | `production_unit_code` `SKH_ICH_PCK` for unit P&T4 breaks the `<campus_code>_<unit name>` pattern (other P&T units use `…_P&Tn`) | `SKH_ICH_OP_04` | TBD |
| 3 | KML is named `sk_hynix…` but 21 of its 34 zones are Samsung (`SSE_*`) | `sk_hynix_polygon_boundary.kml` | TBD |
| 4 | `zone_type` `RD` is used (and colour-coded in the KML) but isn't defined in the schema (`OP`/`EX`/`CD`); `CD` doesn't occur in the data | `SKH_ICH_OP_01` (RD row) | TBD |
| 5 | Schema examples differ from the real data format: spec `ICH_EX_001` / `ICH` / `Icheon M16 Front-End Fab` vs data `SKH_ICH_EX_01` / `SKH_ICH` / `M16`. The KML's Location confidence uses lowercase `high`/`medium`, while the spec examples use `HIGH`. This README uses the real format | §4 | TBD |
| 6 | `record_id`, the company fields, the campus name/address, both confidence columns and all dates are `NULL`; they must be filled before database loading (primary key and point-in-time logic depend on them) | `ZONE_MASTER`, all rows | TBD |
| 7 | KML "Location confidence" (31 `high`, 3 `medium`) has no matching column and was not ingested | KML attribute | TBD |
| 8 | Other unit codes that don't follow `<campus_code>_<unit name>`: `SKH_YIN_EX` (EXPANSION), `SSE_GHG_S1_01` / `SSE_GHG_S1_02` (both S1; likely deliberate, one fab split across two outlines) | `SKH_YIN_EX_01`, `SSE_GHG_OP_02/03` | TBD |
| 9 | `client/` and `owner/` folders are empty; their purpose is undocumented | `layouts/` | TBD |

**Resolved**

- **Date columns applied to the workbook (2026-10-12).** `recorded_at` was renamed to `record_created_at`, and `imagery_acquired_date` was added as column 21. Both are `NULL` for all 34 rows, because the KML has neither date.
- **Case 2 vs the `record_id` definition (2026-10-12).** `record_id` identifies a zone, not one version of it. It is kept for corrections and schema changes and changes only on merge, split or replacement. The key is (`record_id`, `pit_available_from`).

---

## 9. Changelog

| Date | Change |
| --- | --- |
| 2026-10-12 | Resolved open issue #10 (date columns applied to `ZONE_MASTER`: `record_created_at`, `imagery_acquired_date`); discarded #11 (multiple images / `imagery_source_id`) |
| 2026-10-12 | Added `record_created_at` (replaces `recorded_at`) and `imagery_acquired_date` to `ZONE_MASTER`; added "Date columns at a glance" with date rules; updated Case 2, MySQL DDL and open issues #10–11 |
| 2026-10-12 | Initial version: folder map, `master_layout` inventory, schema for `ZONE_MASTER` / `ZONE_LINEAGE_MASTER` (added `recorded_at` and `polygon`; `record_id` redefined per the resolved issue), change-tracking cases, ingestion rules, RDS MySQL loading guide, open issues |
