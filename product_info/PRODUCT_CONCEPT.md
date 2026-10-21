<!-- Page 1 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

**MANDATA CORPORATION**

# Korea Semiconductor Fab Activity Data

**Product Concept and Data Development Framework**

August 2026

---

## 1. Product Scope — Relationship to Semiconductor KPIs

- Semiconductor investment KPIs fall into six groups: demand, inventory, price, shipments, revenue, and production.
- The core object of this product is observation of physical fab activity (the production side). The other KPIs serve mainly as targets, drivers, or validation inputs.
- Foot traffic (FT) measures the physical activity of people; it is not output itself.

| KPI | Relationship | Rationale and use |
|---|---|---|
| Production (utilization, ramp, capex) | ★ Target (the product itself) | What FT data proxies. No official production-volume data exists, so validation is indirect. |
| Price (spot) | Leading driver + validation | Price leads FT by roughly 10 months (counter-cyclical capex). Public data, so not a product to sell — used for interpretation and validation. |
| Shipments (export volume, kg) | Validation (primary validation target) | FT leads shipments by roughly 5 months, so realized shipments validate the signal ex post. |
| Revenue | Indirect validation | = shipments × price. Validates price and shipment volume rather than revenue itself. |
| Inventory | Supporting interpretation | Inferred indirectly from the production–shipment gap. Lower priority. |
| Demand | Out of scope | End-market demand has limited relevance to this product. |

<!-- Page 2 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

## 2. Core Categories and Approach

### 2.1 Production Cycles: Operations (OPS) and Expansion (EXP)

- **Fab Operating Cycle:** the degree to which existing capacity is actually being used, and how that changes over time — the repeating pattern in which equipment and labor utilization in production-capable areas rises, peaks, slows or declines, and recovers. Observed primarily in the Operations Zone (OP, formerly CPZ).
- **Capacity Expansion Cycle:** the linear lifecycle through which new fabs, lines, and production equipment move from planning to construction, installation, and qualification, and are converted into actual production capacity. Observed primarily in the Expansion Zone (EX, formerly CXZ).

#### 2.1.1 Operating Cycle (cyclical · 4 phases · 12 states)

- The 4 phases and 12 states are drawn so that the key investment questions group naturally around them.

| State | Description | Rate of change (Δ · ΔΔ · level) |
|---|---|---|
| **Phase 1 — Bottoming and Turnaround** | | |
| 1 Bottoming | Decline halts; activity settles into the trough range | Δ ≈ 0, low level |
| 2 Bottom Phase | Trough range sustained | Δ ≈ 0 sustained, low level |
| 3 Production Turnaround | Direction turns upward (trigger ending Phase 1) | Δ turns positive |
| **Phase 2 — Ramp-up** | | |
| 4 Ramp-up Acceleration | Increase accelerating | Δ +, ΔΔ + |
| 5 Ramp-up Continuation | Increase at a steady rate | Δ +, ΔΔ ≈ 0 |
| 6 Ramp-up Deceleration | Still increasing, but the increase is slowing | Δ + (clear), ΔΔ − |
| **Phase 3 — Peak** | | |
| 7 Peak Formation | Increase halts; activity settles into the peak range | Δ ≈ 0, high level |
| 8 Peak Phase | Peak range sustained | Δ ≈ 0 sustained, high level |
| 9 Production Downturn | Direction turns downward (trigger ending Phase 3) | Δ turns negative |
| **Phase 4 — Downturn** | | |
| 10 Downturn Acceleration | Decline accelerating | Δ −, ΔΔ − |
| 11 Downturn Continuation | Decline sustained | Δ −, ΔΔ ≈ 0 |
| 12 Downturn Deceleration | Still declining, but the decline is slowing (→ returns to state 1) | Δ − (clear), ΔΔ + |

<!-- Page 3 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

#### 2.1.2 Expansion Lifecycle (unidirectional · 3 stages)

- Expansion is not cyclical but a linear lifecycle running from groundbreaking to completion. Rather than fine-grained states, it is best divided into the three transition points that matter for investment: onset, persistence, and completion.

| Stage | Description | Nature of the signal |
|---|---|---|
| Build Onset | New on-site labor and outdoor activity above the historical baseline | Turning point (e.g. entry into counter-cyclical capex) |
| Build Persistence | Onset activity proves to be sustained and expanding rather than a one-off event | Intensity and duration |
| Build Completion Signal (completion or handover candidate) | Slowdown, withdrawal, or spatial relocation of construction labor suggesting completion or handover to the operations zone | Candidate turning point (e.g. leads an OPS ramp; handover candidate) |

- **Caveat:** a decline in FT activity alone cannot distinguish genuine completion from a construction halt, a delay, a temporary pause, or a transition into the equipment-installation stage. The third stage is therefore expressed not as "completion confirmed" but as a completion-or-handover candidate signal.

#### 2.1.3 Operations × Expansion Interaction — Overview

- The two cycles do not stand in a one-way leading relationship; they interact bidirectionally and phase-dependently.
- Their interaction is divided into six regimes, which form a core set of investment indicators (see 3.3, INT indicators).

| Operations (OPS) | Expansion (EXP) | Interaction regime (INT) |
|---|---|---|
| Rising | Build Onset · Persistence | Broad Expansion |
| Rising | Build Completion Signal | Handover Candidate (HOC) |
| Flat | Build Onset · Persistence | Capacity-Build Lead (CBL) |
| Flat | Build Completion Signal | Completion or Pause |
| Falling | Build Onset · Persistence | Strategic Divergence (SDV) |
| Falling | Build Completion Signal | Broad Contraction (BCT) |

### 2.2 Zones and Products

#### 2.2.1 Zone definitions

- The basic unit of observation is the fab, but within each fab activity is separated into zones.
- A separate code (`zone_type`) is used to avoid confusion with the investment-indicator groups (OPS / EXP / INT).

<!-- Page 4 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

| `zone_type` | Name | Definition | Implication |
|---|---|---|---|
| OP | Operations Zone | Existing production buildings; the core operating area for production | Coincident with current production and operating activity — the observation target for OPS indicators |
| EX | Expansion Zone | New fabs, expansions, cleanrooms, and equipment installation / commissioning areas | Future capacity build; may lead subsequent activity — the observation target for EXP indicators |
| RD | R&D / Office | Research, process-development, and office areas | Non-core operating activity that must be separated from core production areas |
| LG | Logistics / Gate | Access, logistics, and shift-boundary areas | Supporting diagnostic zone for confirming shift, contractor, installation, and logistics activity |
| CT | Control Zone | Comparison areas where fab activity does not directly occur | Control group used to net out common shocks and telecom-panel changes |

#### 2.2.2 Product exposure: how it is approached

- Global investors are not interested in "memory in general" but in specific products — above all in HBM (latest generation) production dynamics, and in whether the HBM capacity build sustains and extends through late 2026 and into early 2027.
- FT observes only aggregate population activity within fab boundaries, so HBM, DRAM, and NAND cannot be decomposed directly within a single fab.
- The alternative is spatial association rather than direct measurement: public information and geospatial information are used to tag whether a given fab or zone is associated with HBM, advanced packaging, and so on, and the physical activity of those areas is then reported.
- **Language principle:** terms implying direct measurement — "HBM output", "HBM utilization rate" — are not used. Activity is described in associational terms: "HBM-associated fab activity", "HBM-linked zone activity".

### 2.3 Core Approach: A Three-Layer Methodology

- The product is built on three layers: investment indicators → data metrics (for foot traffic, FT metrics) → data layout and columns.

| Layer | Definition | Composition |
|---|---|---|
| ① Investment Indicator | Independent, dataset-agnostic core investment questions (key use cases are defined separately) | OPS 12 + EXP 3 + INT 6 = 21 |
| ② FT Metric (for mobile population data) | Standardized data metrics that describe the investment indicators, neutral as between operations and expansion | 12 in MVP |
| ③ Data Layout and Columns | The actual data structures that make the FT metrics computable | 5 files (Presence · Flow · Dwell · Movement · Metrics) as the base |

<!-- Page 5 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

- The 5 company/fab comparison items (COM) and 4 product items (PRD) are not a separate methodological layer. They are classified as key use cases — questions answered by combining investment indicators.
- **Design principles for the data metrics:** representativeness, non-redundancy, mutual distinguishability, independent evidentiary value, and extensibility.
  - For FT, the characteristics the metrics measure are: level, direction, speed, persistence, volatility, and spatial diffusion. Period, population type, and time window are handled as columns, not as new metrics.
- **Direction:** a small set of standard FT metrics (12 in MVP) plus a wide range of observation conditions expressed through columns.

<!-- Page 6 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

## 3. Investment Indicators — 21 Core Indicators

| Analytical axis | Count | Ongoing investment importance | Importance in specific phases | Contribution to product differentiation |
|---|---|---|---|---|
| OPS — Operating cycle | 12 | Very high (base indicator set) | Very high | High |
| EXP — Expansion lifecycle | 3 | Supporting | Very high during expansion, new-fab, and HBM phases | High |
| INT — Operations × expansion interaction | 6 | High | Very high at inflection points and during strategic capex phases such as handover | Very high |

### 3.1 Operations (OPS) Indicators — 12

| Code | State | Investment indicator (i.e. the core investment question) |
|---|---|---|
| OPS01 | 1 Bottoming | Has the decline effectively stopped (rate of change near zero), with trough stabilization spreading across core zones and time windows? |
| OPS02 | 2 Bottom Phase | Is trough-level activity holding at a low level without declining further? |
| OPS03 | 3 Production Turnaround | Have multiple core metrics turned from declining or flat to rising? |
| OPS04 | 4 Ramp-up Acceleration | Since the upturn, has the rate of increase widened versus the prior period? |
| OPS05 | 5 Ramp-up Continuation | Is the strong rate of increase holding steady, neither accelerating nor decelerating? |
| OPS06 | 6 Ramp-up Deceleration | Is activity still increasing but with the rate of increase clearly slowing? |
| OPS07 | 7 Peak Formation | Has the increase effectively stopped, with entry into the peak range and exhaustion of upward momentum? |
| OPS08 | 8 Peak Phase | Is peak-range activity holding without rising or falling? |
| OPS09 | 9 Production Downturn | Has peak-range activity turned downward? |
| OPS10 | 10 Downturn Acceleration | Since the downturn, has the rate of decline widened versus the prior period? |
| OPS11 | 11 Downturn Continuation | Is the decline holding steady, neither accelerating nor decelerating? |
| OPS12 | 12 Downturn Deceleration | Is activity still declining but with the rate of decline beginning to slow? |

- The 12 states form a mutually exclusive state-classification system covering entry into, persistence within, and transition out of each of the 4 phases. Each state determination itself answers an investment question: which phase are we in now, and is the next transition imminent?

### 3.2 Expansion (EXP) Indicators — 3

<!-- Page 7 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

- Expansion carries lower general importance than operations, but during new-fab, HBM, and equipment-installation phases it has high standalone investment value. It is therefore retained as an independent indicator set rather than serving only as an input to the interaction indicators — but kept to a minimum of three.

| Code | Name | Investment indicator | Potential evidence (example FT metric combinations) |
|---|---|---|---|
| EXP01 | Build Onset | Has new expansion activity begun, above the historical baseline? | Rising presence level in the EX zone; momentum turning positive; rising acceleration and anomaly scores; diffusion across multiple cells (breadth) |
| EXP02 | Build Persistence | Is the initiated expansion activity sustaining and broadening rather than being a one-off event? | Persistence, breadth, volatility, night and weekend construction patterns, duration beyond a defined threshold |
| EXP03 | Build Completion Signal | Does the slowdown, withdrawal, or relocation of construction labor suggest completion or handover? | EX momentum turning negative + shift in population mix (falling contractor share) + subsequent response in the OP zone |

- **Naming:** the stages follow onset / persistence / completion, but the indicator names are "Build Persistence" (emphasizing durability and stability) and "Build Completion Signal" (making explicit that this is a candidate signal, not a confirmation).
- EXP03 does not assert "completion confirmed" but "completion or handover candidate". Distinguishing genuine completion from a halt, delay, or pause requires combination with the subsequent OP-zone response, gate and logistics activity, and public disclosures.

### 3.3 Operations × Expansion Interaction (INT) Indicators — 6

- INT creates no new source FT metrics. It interprets the combination of FT metrics observed in the OP zone and the EX zone.

| Code | Regime | OPS | EXP | Investment indicator | Interpretation points |
|---|---|---|---|---|---|
| INT01 | Broad Expansion | Rising | Onset · Persistence | Are fab activity and expansion broadening together, and is it sustaining? | – Entry into OPS03 alongside EXP is the strongest confirmation signal<br>– OPS04 and OPS05 confirm continuation |
| INT02 | Handover Candidate (HOC) | Rising | Completion Signal | Following the slowdown in expansion activity, is the transition into production actually appearing? (Is completed construction and equipment installation feeding through into an actual production ramp?) | – OPS03 + Completion Signal = a clean transition pattern<br>– OPS06 + Completion Signal may instead be an early warning of an approaching peak — the interpretation differs |
| INT03 | Capacity-Build Lead (CBL) | Flat | Onset · Persistence | Has the company begun preparing capacity expansion ahead of a recovery in production activity? And when does production respond? (After expansion rises, when and by how much does utilization respond?) | – Expansion initiated ahead of the cycle during a trough-stabilization window is a candidate leading signal for a turnaround<br>– Tracking the timing of the response is the crux |
| INT04 | Completion or Pause | Flat | Completion Signal | Is this completion, or delay and suspension? And does a production response follow? | – The hardest INT regime to resolve on FT alone<br>– A trough plateau (OPS01–02) and a peak plateau (OPS07–08) imply opposite readings<br>– At a trough: completion (+OPS01–02) is a catalyst for OPS03, while suspension prolongs the trough. At a peak: completion (OPS07–08) raises oversupply risk, while suspension points to an OPS09 downturn |
| INT05 | Strategic Divergence (SDV) | Falling | Onset · Persistence | Is strategic expansion continuing even through production cuts? (Is the company maintaining expansion investment aimed at future demand even in a cut phase?) | – Entry into OPS09 marks the first capture of a counter-cyclical signal<br>– Bullish (securing share ahead of the recovery) versus oversupply risk<br>– Track: (i) whether expansion persists, (ii) whether competitors do the same, (iii) whether expansion is confined to specific products or zones |
| INT06 | Broad Contraction (BCT) | Falling | Completion Signal | Are fab activity and expansion weakening together — a signal of medium-term capacity contraction? (Is current production weakness broadening from a temporary adjustment into a reduction in medium-term supply capability?) | – The most bearish regime<br>– OPS09 + Completion Signal: new supply may arrive before demand recovers — a near-term negative<br>– OPS10–11 + Completion Signal: the classic bearish confirmation window<br>– On transition to OPS12, whether expansion restarts determines whether the regime shifts to INT03 |

<!-- INT03–INT06 appear on Page 8 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

- The six regimes are the combinations of operating direction (rising / flat / falling) and expansion stage (in progress / completion signal). They are mutually exclusive and cover the full space. Note that "flat" reads in opposite directions depending on whether it sits at a trough or a peak, so the operating state (or the level position) must always be communicated alongside the regime.

<!-- Page 9 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

### 3.4 Key Use Cases — 9

- The nine items below are not investment indicators. They are the client-facing key use cases that can be answered by combining operations, expansion, and interaction results.

#### 3.4.1 Company and fab competitive comparison (COM) — 5

| Code | Key use case |
|---|---|
| COM1 | Samsung versus SK hynix: which company shows stronger fab operating activity and stronger expansion activity? |
| COM2 | Which company enters a Production Turnaround, or a Production Downturn, first? |
| COM3 | Which company shows a stronger and longer-lasting production ramp-up, and converts expansion activity into actual utilization gains more quickly? |
| COM4 | Are the two companies in different operating cycles, expansion cycles, or operations-expansion interaction regimes? |
| COM5 | Within each company, which fabs are leading? (Pyeongtaek · Hwaseong · Giheung / Icheon · Cheongju) |

#### 3.4.2 Product-associated activity analysis (PRD) — 4

| Code | Key use case |
|---|---|
| PRD1 | Among HBM, DRAM, NAND, and foundry, which product group is leading utilization, and which is leading expansion? |
| PRD2 | Among fabs and zones associated with HBM and advanced packaging, which show relatively stronger operating and expansion activity? |
| PRD3 | Is activity in HBM-associated expansion zones sustaining and extending? (Persistence, intensity, and spatial diffusion — the degree of spread to other zones or fabs.) |
| PRD4 | Between Samsung and SK hynix, which shows stronger HBM-associated operating and expansion signals, and which is faster in initiating expansion and converting it into production? |

<!-- Page 10 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

## 4. FT Metrics and Data Layout

### 4.1 FT Metrics — 12 in MVP

- **Core principle:** FT metrics are neutral as between operations and expansion.
  - An FT metric is in itself neither an operations metric nor an expansion metric. A rise in the night-activity ratio, for example, could be production staff on night shifts, construction crews working overnight, equipment commissioning, or R&D working late.
  - The operations-versus-expansion meaning is established by combining additional data: FT metric × zone type × population type × time window, and so on.
  - The same activity momentum metric applied to an OP zone is operating momentum; applied to an EX zone it is expansion momentum.
  - For that reason no separate lists of "operations FT metrics" and "expansion FT metrics" are maintained.

| No. | FT metric | Core concept | Example source columns |
|---|---|---|---|
| 1 | Presence Level | The absolute or normalized level of population activity present in a given period and space | Reference date, time window, grid cell code, de-facto population, floating population, working population, visiting population, resident population, domestic/foreign flag, population weight |
| 2 | Activity Momentum | The direction and strength of change in recent activity relative to a prior period | Presence Level columns + reference period, comparison period, daily/weekly/monthly aggregation flag, week-on-week, month-on-month, and year-on-year comparison values |
| 3 | Activity Acceleration | Whether the rate of change in activity is speeding up or slowing down | Reference date, continuous time-series values, short-horizon momentum, medium-horizon momentum, rate of change, prior-period rate of change |
| 4 | Activity Persistence | The degree to which an up or down direction is sustained continuously rather than being transitory | Reference date, time window, daily activity value, direction sign, length of consecutive up/down runs, lookback window, count of valid observation days |
| 5 | Activity Volatility | How stable or irregular the level or rate of change of activity is | Daily and hourly population counts, momentum time series, standard-deviation window, mean value, outlier-day flag, count of valid observations |
| 6 | Night Activity Ratio | The share of total activity occurring in a defined night-time window | Time code, reference date, hourly population counts, night-window flag, daily total population, population type (working, visiting, etc.) |
| 7 | Weekend Activity Ratio | The share of total activity occurring on weekends and public holidays | Reference date, day of week, weekday/weekend flag, public-holiday flag, daily population, weekend population, full-period population |
| 8 | Activity Breadth | Whether increases or decreases are confined to a few grid cells or are spreading across multiple zones and cells | Grid cell code, zone ID, fab ID, per-cell momentum, count of rising and falling cells, count of valid cells, per-cell population |
| 9 | Population Mix | The composition of activity by population type, sex, and age, and how that composition changes | Population type, sex, age band, domestic/foreign, resident/working/visiting flag, long- versus short-stay foreign nationals, population by type, total population |
| 10 | Calendar-Adjusted Activity Level | The activity level with calendar effects removed — day of week, public holidays, traditional holidays, and monthly seasonality | Reference date, day of week, public-holiday flag, traditional-holiday flag, month and week number, time window, actual population, same-weekday historical values, normal baseline value |
| 11 | Control-Adjusted Activity Change | Fab-specific activity change, distinguished from general local change around the fab | Target and control area codes, zone type, reference date, target-area population, control-area population, rates of change for both, distance and matching-type information |
| 12 | Activity Anomaly Score | Whether activity is statistically unusual relative to historical normal patterns | Reference date, time window, actual activity value, historical mean and median, standard deviation or quantiles, calendar-adjusted value, control-adjusted value, valid observation window |

<!-- Rows 9–12 appear on Page 11 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

### 4.2 Mapping FT Metrics to Investment Indicators

| Investment indicator | Principal FT metric combination | Applied zone |
|---|---|---|
| OPS01–03 (trough and turnaround) | Momentum (≈0 → +), Persistence, Breadth | OP |
| OPS04–06 (ramp-up) | Momentum +, Acceleration ±, rising night and weekend ratios | OP |
| OPS07–09 (peak and downturn) | Momentum ≈0 → −, Acceleration −, Anomaly | OP |
| OPS10–12 (downturn) | Momentum −, Acceleration ∓, Persistence | OP |
| EXP01 Build Onset | Presence Level ↑ + Momentum turning positive + Anomaly ↑ + Breadth diffusion | EX |
| EXP02 Build Persistence | Persistence + Breadth + Volatility + night and weekend construction patterns | EX |
| EXP03 Build Completion Signal | Momentum turning negative + Population Mix shift (contractor share ↓) + subsequent OP response | EX (+ OP confirmation) |
| INT01–06 | OP-zone metrics × EX-zone metrics — no separate source metrics | OP × EX |
| COM1–5 | Cross-company comparison, lead/lag in state entry, decomposition of fab-level contribution | Company and fab level |
| PRD1–4 | Level, momentum, breadth and related metrics for product-association-tagged zones | Product-associated zones |

### 4.3 Client Data File Structure

- Separated into point-in-time (snapshot) data and interval-based data.
  - In the client XLSX deliverable, each file below is implemented as a separate tab.

<!-- Page 12 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

| File | Measurement basis | Content | Release |
|---|---|---|---|
| `FT_PRESENCE_HOURLY` | Point in time: snapshot | Population present by fab / zone / cell, by hour | ✓ MVP |
| `FT_DWELL_DAILY` | Interval: dwell | Population by dwell-start time and dwell-duration band — used to separate construction from installation activity | Phase 1 or 2 |
| `FT_MOVEMENT_OD` | Interval: origin–destination | Inflow and outflow at the administrative-district level — commuting-catchment and labor-supply analysis | Phase 1 or 2 |
| `FT_METRICS_DAILY` | Metrics | Computed values for the 12 FT metrics — the core deliverable file | ✓ MVP |

- Phase 2 files are subject to source-data constraints and are scoped accordingly during development.
- A separate partner-side data layout is prepared, referencing the partner layout, to the extent needed for the client files above to be constructible.

### 4.4 Point-in-Time (PIT) Quality Control

| Column | Definition |
|---|---|
| `observation_date` | The date on which the activity actually occurred |
| `pit_as_of_date` | The first date (or the relevant snapshot date) on which a client or analyst could have known that value — updated daily by default |

- Issues under PIT management: lagged receipt of telecom data, retrospective correction at source, changes in estimation coefficients, changes in zone mapping, changes in the control set, backfills, and reprocessing of missing values.
- Backtests must use only the version that was available at the time, keyed on `pit_as_of_date`.

<!-- Page 13 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

## 5. Near-Fab Merchant (NFM) Data

### 5.1 Relationship Between NFM and FT Data

- FT data is primarily an activity signal for fab-related activity (people activity). NFM is an economic signal (economic activity): it confirms whether that activity showed up as actual consumption nearby, and decomposes who was active and the economic character of that activity.
- **Possible product mixes:**
  - **Core-Confirmation (Stage 1):** NFM data is demonstrated to be usable for re-validating investment-indicator determinations made from FT data ⇒ "FT-led Dual Signal".
  - **Core-Core (Stage 2):** once NFM is confirmed to explain the investment indicators satisfactorily on its own, both datasets serve as independent indicators validating the investment indicators and key use cases ⇒ "Dual Core".
  - **In either case:** (i) FT metrics and NFM metrics are built separately and need not map one-to-one; (ii) analysis against the investment indicators runs in three modes — FT only, NFM only, and FT + NFM (in the combined case: agreement, agreement with a lag, or disagreement).
  - **Note on the distinction:** an independent indicator has sufficient standalone grounds — and demonstrated performance — to determine all 21 investment indicators on its own (if NFM metrics alone can formally classify the cycle and states, NFM is an independent indicator). A confirmation indicator falls short of that but can independently re-confirm the signals produced by an independent indicator.
- **Process:** Stage 1 first, then Stage 2 — not straight to Stage 2.
  - Stage 1 NFM metrics: NFM Confirmation Metrics, developed to confirm, refute, or interpret the economic reality and diffusion of the semiconductor investment signals generated by FT metrics ⇒ a small core set of roughly 6–7 metrics.
  - For comparison, Stage 2 NFM metrics would exist in order to declare semiconductor investment signals on a standalone basis.
- **Validation structure under the Stage 1 strategy:**
  - FT ⇒ fab activity cycle signal
  - FT ⇒ NFM ⇒ economic confirmation
  - FT, NFM, and FT + NFM ⇒ compared against historical events in external semiconductor investment KPIs ⇒ validation of investment usefulness

### 5.2 Illustrative NFM Confirmation Metrics

- The metrics below, and the file structure in 5.3, are indicative and intended as a design guide.

| No. | NFM metric | Core concept |
|---|---|---|
| 1 | NFM Activity Level | The level of surrounding economic activity — transaction value, transaction count, customer count |
| 2 | NFM Activity Momentum | The direction of increase or decrease in economic activity |
| 3 | NFM Activity Acceleration | Whether the rate of increase or decrease is strengthening or slowing |
| 4 | NFM Activity Persistence | The persistence of the direction of change |
| 5 | Merchant Activity Breadth | The degree to which change is spreading across merchant categories, individual merchants, and distance bands |
| 6 | Merchant Category Mix | Shifts in the composition of spending — food and beverage, lodging, transport, personal services, and so on |
| 7 | Control-Adjusted NFM Change | Nets out a control catchment to remove local macro conditions, price effects, and general retail trends |

<!-- Rows 4–7 appear on Page 14 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

- Merchant types and transaction characteristics with high relevance to operations versus expansion respectively are handled at the layout level (for example, an expansion-proxy index).

### 5.3 NFM Data File Structure

- A layout built around merchant category (card-network merchant classification plus separate fab-relevant groupings), distance, and commercial catchment.
- As with the FT data layout, provision of an NFM confirmation-metrics file is planned.

| File | Content | Release |
|---|---|---|
| `NFM_TR_BASIC_DAILY` | Sales amount, transaction count, customer count for each campus and / or zones | ✓ MVP |
| `NFM_DEMOGRAPHIC_DAILY` | Breakdowns of `NFM_TR_BASIC_DAILY` data by Korean / Non-Korean, and by employes (Samsung Electronics, SK Hynix, each) / non-employes | ✓ MVP |
| `NFM_CONTROL_DAILY` | Non-8 campuses’ `NFM_TR_BASIC_DAILY` and `NFM_DEMOGRAPHIC_DAILY` | ✓ MVP |
| `NFM_AREA_MASTER` | Definitions of the observed catchment, distance bands, and control catchment for each fab | Phase 2 |
| `NFM_MERCHANT_GROUP_MAPPING` | Mapping from card-network merchant category codes to standard merchant groups: operations-related, expansion-related, and unrelated | Phase 2 |
| `NFM_METRICS_DAILY` | Computed values for the NFM confirmation metrics (approximately 7), with operations-relevance and expansion-relevance flags | Phase 2 |

- NFM file scope is subject to confirmation of the available granularity from the card-data source across days, catchments, and merchant categories.

<!-- Page 15 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->

## 6. Use Case: Event Study and Validation

### 6.1 Purpose and Principles

- External data is used first to fix the semiconductor cycle and its major inflection points since 2022 — building a ground truth from prices, inventories, shipment volumes, corporate disclosures, and earnings commentary. The FT metrics, the NFM metrics, and the FT + NFM combination (collectively, "the metrics") are then validated on directionality, inflection detection, and lead time.
- All analysis is performed on a point-in-time basis.

### 6.2 Historical Event Windows

| Period | Event |
|---|---|
| 2022 | Downturn Acceleration |
| 2022 | Production Response Lag |
| 2023 | Production Cut |
| 2023 | Supply Discipline |
| 2023 | Downturn Deceleration |
| 2023 | Bottoming / Bottom Phase |
| 2024 | Production Turnaround |
| 2024 | HBM Ramp-up |
| 2024 | Ramp-up Acceleration |
| 2025 | Ramp Sustainability |
| 2025 | Relative strength across companies and fabs |
| 2026 | Ramp continuation and deceleration |
| 2026 | Expansion persistence and possible Peak Formation |

### 6.3 Validation Items

- **Operations side:**
  - Comparison of the metrics against historical events
  - Differential response of the metrics across day, night, weekday, and weekend
  - Whether operating and expansion activity can be distinguished
  - Controls for control zones, traditional holidays, day of week, and seasonality
- **Operations–expansion interaction:**
  - Lead/lag from expansion onset to production ramp
  - Detection of the construction-to-production handover
  <!-- Page 16 · Mandata Corporation · Korea Semiconductor Fab Activity Data -->
  - Testing for false leads — expansion that does not feed through into higher utilization
- **Economic validation against shipments:**
  - Directionality and lead/lag between the metrics and DRAM and HBM shipment volumes
  - Timing of bottoming in the metrics versus bottoming in shipments; timing of ramp-up in the metrics versus recovery in shipments
  - Differences in lead time by fab, company, and product

### 6.4 Interpretation of Results and Limitations

- Validation results for each metric are classified as Validated, Directional, or Insufficient.
- The limitations of fab-to-export-item matching and the limited historical window are stated explicitly.
- Flow, dwell, and movement data, integration with electricity, gas, and water consumption, and linkage to external investment KPIs are set out as follow-on work.
