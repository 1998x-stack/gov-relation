# Audit: data/graph/*.gexf — Structural Integrity, Naming & DB-Pairing Review

**Audit date:** read-only run against /Users/x/Desktop/gov-relation — nothing modified.
**Scope:** all 2284 `{name}_network.gexf` files in `data/graph/`, cross-checked with `data/database/`, `data/provinces/`, `data/tmp/`, `scripts/build/`, `data/root/`.
**Method:** Python 3 stdlib only (`xml.etree.ElementTree`, `os`, `re`, `json`).

---

## 1. Sampled file inspection (14 files, mixed regions/naming)

Two distinct generator lineages are present.

### Lineage A — canonical `GEXFBuilder` (gov_relation/gexf.py, GEXF 1.3)
Sample: `玉田县_network.gexf`, `丰润区_network.gexf`, `baoding_network.gexf`, `cangzhou_network.gexf`, `chengde_network.gexf`.

- root: `<gexf xmlns="http://www.gexf.net/1.3" xmlns:viz="http://www.gexf.net/1.3/viz" xmlns:xsi=".." version="1.3">`
- `<graph mode="static" defaultedgetype="directed">`
- **Node attrs (10):** `type, current_post, current_org, gender, ethnicity, birth, source, org_type, level, location`
- **Edge attrs (4):** `type, context, overlap_org, overlap_period`
- `viz:size`, `viz:shape`, `viz:color` present on nodes; numeric node ids; occasional `<meta><title>…</title></meta>`.

### Lineage B — newer hand-built variants (xmlns **without** `www.`, GEXF 1.0)
Sample: `aksai_network.gexf`, `changzhou_network.gexf`, `anyi_network.gexf`, `donghu_network.gexf`, `张掖市_network.gexf`.

- root: `<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.0">`
- `<graph mode="static" defaultedgetype="undirected">` (some files `directed`)
- **Rich `<meta>` block:** `<meta lastmodifieddate="2026-07-22"><creator>Claude Code Research Agent</creator><description>…</description></meta>`
- **no common node-attr schema** — highly variable; string-prefixed ids (`p1`, `org2`); `viz:size`/`viz:color`, often no `viz:shape`.

**meta block presence:** 2235 of 2254 parse-clean files carry `<meta>` (99.2%).

---

## 2. Structural consistency — variants & counts

**Not consistent: there is no single shared template.**

| Lineage | xmlns | version | defaultedgetype | Node-attr schema | files (share of parseable) |
|---|---|---|---|---|---|
| A (canonical) | http://www.gexf.net/1.3 | 1.3 | directed | fixed 10-attr | 1269 (56.3%) |
| B (legacy) | http://gexf.net/1.3 | 1.0 | undirected | highly variable | ~985 (43.7%) |

- **154 distinct node-attribute schemas** and **159 distinct full variant combinations** across the 2254 clean files.
- Dominant single schema = Lineage A 10-attr (**56.3%**); the remainder is a long tail of ~150 schemas.
- Edge-attr variants: `(type,context,overlap_org,overlap_period)` = 1457; `(type,context)` = 226; `(type,start,end,context)` = 99; `(type,context,confidence)` = 58; `(Type,Context,Period)` = 56; `(type,context,period)` = 51; more.
- **Same semantic, different field name across files:** `type` vs `Type` vs `Node Type` vs `Kind` vs `Category` vs `entity_type`; `current_post` vs `role` vs `Current Post` vs `job_title`; `current_org` vs `org` vs `organization`; show inconsistent capitalization and snake_case/TitleCase.

### Attribute-name variants (person/org encoding)
- `type` = `person` / `organization` (canonical)
- `type` = `person` / `org` / `organization` (legacy)
- `entity_type`, `Node Type`, `Kind`, `Category`, `role_or_type` — same person/org split under different keys.

---

## 3. Malformed / truncated files

**30 of 2284 GEXF files fail basic `xml.etree.ElementTree` parsing.**


| Failure mode | count |
|---|---|
| mismatched tag | 20 |
| not well-formed (invalid token) | 8 |
| unbound prefix | 2 |

**Full broken-file list (30)** — `data/graph/` prefix:

`honggutan_network.gexf`, `qingyunpu_network.gexf`, `shangrao_network.gexf`,
`三元区_network.gexf`, `仓山区_network.gexf`, `会昌县_network.gexf`, `合川区_network.gexf`, `吴川市_network.gexf`,
`坡头区_network.gexf`, `城厢区_network.gexf`, `将乐县_network.gexf`, `尼木县_network.gexf`, `岷县_network.gexf`,
`廉江市_network.gexf`, `新罗区_network.gexf`, `昌都市_network.gexf`, `望奎县_network.gexf`,
`武义县_network.gexf`, `泉州市_network.gexf`, `涵江区_network.gexf`, `石狮市_network.gexf`,
`秀屿区_network.gexf`, `索县_network.gexf`, `覃塘区_network.gexf`, `通州区_network.gexf`,
`遂溪县_network.gexf`, `长乐区_network.gexf`, `雷州市_network.gexf`, `马尾区_network.gexf`, `麻章区_network.gexf`

Of these 30, only **2** have a matching DB: `昌都市` (in `data/provinces/xizang/database/`) and `望奎县` (in `data/tmp/heilongjiang_望奎县/`). The other 28 are orphaned/broken.

---

## 4. Naming cross-check vs `scripts/build/`

- `scripts/build/` holds **2280 `.py`** files.
- **2226 / 2284 GEXF (≈97%)** have an exact-name builder `build_<name>_data.py` (e.g. `玉田县_network.gexf` ⇄ `build_玉田县_data.py`). Newer builders set `GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"` so the literal filename is not always in the script text.
- **58 GEXF have NO exact-name builder** — these are city/county aggregates served by **shared/batch scripts** (`build_hebei_all_data.py`, `build_henan_province_data.py`, `build_guangdong_province_data.py`, `build_guangxi_province_data.py`, `build_fuzhou_*`, `build_ganzhou_remaining_data.py`, …) or province-wide networks whose output name uses a variable slug.
- Residually **17 files** are not referenced by any `scripts/build/*.py` at all: `hebei_province_network.gexf`, `hukou_network.gexf`, `langfang_network.gexf`, `nanxiong_network.gexf`, `pengze_network.gexf`, `qinhuangdao_network.gexf`, `tangshan_network.gexf`, `zhangjiakou_network.gexf`, `井陉矿区_network.gexf`, `任城区_network.gexf`, `壤塘县_network.gexf`, `微山县_network.gexf`, `正定县_network.gexf`, `略阳县_network.gexf`, `行唐县_network.gexf`, `裕华区_network.gexf`, `贡山独龙族怒族自治县_network.gexf`.

**Conclusion:** filenames ⇄ scripts are NOT 1:1. The ASCII city/county family is many-to-one via batch generators; the Chinese-slug regional family is one-script-per-file.

---

## 5. DB pairing status (whole-repo search for `<slug>_network.db`)

- **692 / 2284 GEXF (30.3%)** have ≥1 matching `_network.db` in the repo.
- **1592 / 2284 GEXF (69.7%)** have **no** `_network.db` anywhere.
- Distinct `_network.db` basenames in repo: **725** (756 total `.db` files, incl. non-`network` test dbs).

Where DBs actually live (occurrence count across the matched graphs):

| DB location | # occurrences | notes |
|---|---|---|
| `data/tmp/**/` (staging) | 652 | not promoted, by far the largest pool |
| `scripts/build/` | 50 | build-side artifacts |
| `data/provinces/*/database/` | 9 | per-province canonical nests |
| `scripts/data/database/` | 9 | legacy nest (e.g. `naidong_network.db`) |
| `data/database/` (intended canonical) | **1** | only `zigong_network.db`; `test_region` has no gexf |
| `data/root` | 2 | `宾阳县`, `隆安县` are here; gaps already into tmp |

**Key gap:** the intended canonical `data/database/` holds only 2 DBs. ~652 staging DBs sit in `data/tmp/` with GEXF only; ~70% of GEXF graphs have no DB at all.

---

## 6. Top-3 standardization fixes (recommendations)

1. **Standardize the GEXF template and validate on write.** Keep only the canonical `GEXFBuilder` output (GEXF 1.3, `xmlns http://www.gexf.net/1.3`, static/directed, fixed 10-node/4-edge attributes). Add a parser regression test over all `data/graph/*.gexf` asserting the fixed node/edge attribute titles + xmlns + version, and rebuild the 30 broken files against it.
2. **Normalize the node-type discriminator.** Pick one attr name (`type`) and one enum (`person` / `organization`); translate legacy `kind`/`entity_type`/`Node Type`/`Category` independently of case/schema. This unblocks every downstream graph consumer.
3. **Reconcile the DB registry.** Promote + co-locate `data/tmp/*.db` (652 present) into `data/database/`, relink each `<name>_graph.gexf` to its canonical DB, and add an inventory assertion (`scripts/inventory.py`) that every GEXF either has a canonical DB or an explicit acknowledged standalone status. Also rebuild 28 orphan broken graphs.

---

## Appendix
- Canonical generator: `gov_relation/gexf.py` (`GEXFBuilder`, version 1.3).
- Runner: `gov_relation/runner.py` — `run_build()`.
- Skill: `.agents/skills/china-gov-network/SKILL.md`.
