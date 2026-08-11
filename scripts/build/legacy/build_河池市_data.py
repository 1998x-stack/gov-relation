#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 河池市 leadership network.

河池市（壮语 Hozciz Si）是广西壮族自治区下辖地级市，位于广西北部，云贵高原南麓，
市人民政府驻宜州区。下辖金城江、宜州2个市辖区，南丹、天峨、凤山、东兰4个县，
及罗城、环江、巴马、都安、大化5个自治县。是桂西北的重要中心城市。

本脚本聚焦河池市级党政领导（市委书记、市长）及其升迁网络。资料来源：维基百科
（河池市/朱会东/王军/秦春成）、中国经济网、河池市人民政府门户网站（http://www.hechi.gov.cn）、
中央纪委国家监委网站、人民网地方领导资料库等。置信度与缺口见 report 与 open_gaps.md。

Current (or recently current) city leadership as of 2026-07/08:
- 市委书记: 朱会东（2026-04 起，原贵港市委书记；前任秦春成 2021-2026-04）
- 市委副书记、市长: 汪东明（2026-02 起，代理后确认；8月仍主持市政府常务会与调研）
- 市人大常委会主任: 黄锦锋（2026-02 起）
- 市政协主席: 黎丽（2016-09 起）

重点风险信号：前任市委书记秦春成于 2026-06-05 因涉嫌严重违纪违法被广西壮族自治区
纪委监委纪律审查和监察调查（其被查前已任自治区政协港澳台侨和外事委员会分党组书记）。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]  # scripts/build -> repo root
# When run from staging (data/tmp/<task_id>/), parents[1] is not the repo root.
# Walk upward to locate the directory containing the gov_relation package.
for _parent in (Path(__file__).resolve().parents):
    if (_parent / "gov_relation" / "runner.py").exists():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "河池市"

# 构建入库（暂存）时通过 STAGING_DIR 覆盖；默认写入规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "河池市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "河池市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "河池市_network.db"
    GEXF_PATH = GRAPH_DIR / "河池市_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共河池市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区河池市宜州区"},
    {"id": 2, "name": "河池市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区河池市宜州区"},
    {"id": 3, "name": "河池市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "广西壮族自治区人大常委会", "location": "广西壮族自治区河池市宜州区"},
    {"id": 4, "name": "中国人民政治协商会议河池市委员会", "type": "政协", "level": "地厅级", "parent": "政协广西壮族自治区委员会", "location": "广西壮族自治区河池市宜州区"},
    {"id": 5, "name": "中共河池市纪律检查委员会/河池市监察委员会", "type": "纪委", "level": "地厅级", "parent": "中共广西壮族自治区纪委", "location": "广西壮族自治区河池市"},
    {"id": 6, "name": "中共贵港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区贵港市"},
    {"id": 7, "name": "贵港市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区贵港市"},
    {"id": 8, "name": "中共南宁市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区南宁市"},
    {"id": 9, "name": "南宁市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区南宁市"},
    {"id": 10, "name": "中共北海市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区北海市"},
    {"id": 11, "name": "中共贵港市委/贵港市人民政府", "type": "党委", "level": "地厅级", "parent": "", "location": "广西壮族自治区贵港市"},
    {"id": 12, "name": "桂林市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区桂林市"},
    {"id": 13, "name": "广西壮族自治区人民政府侨务办公室", "type": "政府", "level": "厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区南宁市"},
    {"id": 14, "name": "政协广西壮族自治区委员会", "type": "政协", "level": "省级", "parent": "", "location": "广西壮族自治区南宁市"},
    {"id": 15, "name": "中共百色市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区百色市"},
    {"id": 16, "name": "中共贺州市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区贺州市"},
    {"id": 17, "name": "中共河池市巴马瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委员会", "location": "广西壮族自治区河池市巴马县"},
    {"id": 18, "name": "清华大学", "type": "事业单位", "level": "", "parent": "教育部", "location": "北京市"},
    {"id": 19, "name": "中南财经大学", "type": "事业单位", "level": "", "parent": "", "location": "湖北省武汉市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # ═══ 党委正职 ═══
    # 1 — 朱会东 — 市委书记
    {"id": 1, "name": "朱会东", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年10月", "birthplace": "河南省西平县",
     "education": "中南财经大学经济学学士（商品检验与养护专业），经济师",
     "party_join": "1989年6月", "work_start": "1993年7月",
     "current_post": "中共河池市委书记", "current_org": "中共河池市委员会",
     "source": "https://zh.wikipedia.org/wiki/朱会东"},
    # ═══ 政府正职 ═══
    # 2 — 汪东明 — 市长
    {"id": 2, "name": "汪东明", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年5月", "birthplace": "浙江省杭州市",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "河池市委副书记、市政府市长", "current_org": "河池市人民政府",
     "source": "https://zh.wikipedia.org/wiki/河池市; http://www.hechi.gov.cn/"},
    # ═══ 市人大 ═══
    # 3 — 黄锦锋 — 市人大主任
    {"id": 3, "name": "黄锦锋", "gender": "男", "ethnicity": "壮族",
     "birth": "1972年9月", "birthplace": "广西壮族自治区来宾市武宣县",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "河池市人大常委会主任", "current_org": "河池市人民代表大会常务委员会",
     "source": "https://zh.wikipedia.org/wiki/河池市"},
    # ═══ 市政协 ═══
    # 4 — 黎丽 — 市政协主席
    {"id": 4, "name": "黎丽", "gender": "男", "ethnicity": "汉族",
     "birth": "1963年5月", "birthplace": "广西壮族自治区河池市宜州区",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政协河池市委员会主席", "current_org": "中国人民政治协商会议河池市委员会",
     "source": "https://zh.wikipedia.org/wiki/河池市"},
    # ═══ 前任 ═══
    # 5 — 秦春成 — 前任市委书记（落马）
    {"id": 5, "name": "秦春成", "gender": "男", "ethnicity": "汉族",
     "birth": "1966年5月", "birthplace": "广西壮族自治区贵港市",
     "education": "广西大学（校友/干部教育）",
     "party_join": "1987年", "work_start": "",
     "current_post": "（曾任中共河池市委书记 2021-2026.04；2026-06-05 被审查调查）", "current_org": "中共河池市委员会",
     "source": "https://www.ccdi.gov.cn/"},
    # 6 — 王军 — 前任市长
    {"id": 6, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年5月", "birthplace": "山东省淄博市",
     "education": "清华大学（硕士）",
     "party_join": "1996年6月", "work_start": "",
     "current_post": "（曾任河池市市长 2021.02-2026.01；卸任后去向待查）", "current_org": "河池市人民政府",
     "source": "https://zh.wikipedia.org/wiki/王军(1976年5月)"},
    # 7 — 何辛幸 — 前任市委书记（2015-2021，前前）
    {"id": 7, "name": "何辛幸", "gender": "男", "ethnicity": "汉族",
     "birth": "1963年11月", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任河池市委书记书记 2015.12-2021.06）", "current_org": "中共河池市委员会",
     "source": "https://zh.wikipedia.org/wiki/河池市"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 朱会东 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共河池市委书记", "start_date": "2026-04", "end_date": "present", "rank": "正厅级", "note": "接任秦春成"},
    {"person_id": 1, "org_id": 6, "title": "中共贵港市委书记", "start_date": "2023-05", "end_date": "2026-04", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "贵港市人民政府市长", "start_date": "2022-01", "end_date": "2023-05", "rank": "正厅级", "note": "前任蓝晓"},
    {"person_id": 1, "org_id": 8, "title": "中共南宁市委常委、常务副市长", "start_date": "2021-05", "end_date": "2022-01", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "南宁市人民政府副市长", "start_date": "2017-03", "end_date": "2021-05", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "北海市人民政府副市长/市委宣传部部长/工业园区管委会主任", "start_date": "2013-04", "end_date": "2017-03", "rank": "副厅级", "note": "北海发展改革系统出身；2016.09任副市长"},
    {"person_id": 1, "org_id": 19, "title": "中南财经大学（毕业生）", "start_date": "", "end_date": "1993", "rank": "", "note": "经济学学士"},
    # 汪东明 — 市长
    {"person_id": 2, "org_id": 2, "title": "河池市委副书记、市政府市长", "start_date": "2026-02", "end_date": "present", "rank": "正厅级", "note": "代理后市人大确认"},
    {"person_id": 2, "org_id": 1, "title": "中共河池市委副书记", "start_date": "2026-02", "end_date": "present", "rank": "副厅级", "note": ""},
    # 黄锦锋 — 市人大主任
    {"person_id": 3, "org_id": 3, "title": "河池市人大常委会主任", "start_date": "2026-02", "end_date": "present", "rank": "正厅级", "note": ""},
    # 黎丽 — 市政协主席
    {"person_id": 4, "org_id": 4, "title": "政协河池市委员会主席", "start_date": "2016-09", "end_date": "present", "rank": "正厅级", "note": "长期连任"},
    # 秦春成 — 前任市委书记（被查）
    {"person_id": 5, "org_id": 1, "title": "中共河池市委书记", "start_date": "2021-06", "end_date": "2026-04", "rank": "正厅级", "note": "2026-06-05 被广西纪委监委审查调查"},
    {"person_id": 5, "org_id": 12, "title": "桂林市人民政府市长", "start_date": "2017-11", "end_date": "2021-06", "rank": "正厅级", "note": "前任周家斌"},
    {"person_id": 5, "org_id": 13, "title": "广西壮族自治区人民政府侨务办公室主任", "start_date": "2015-12", "end_date": "2017-11", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 14, "title": "自治区政协港澳台侨和外事委员会分党组书记", "start_date": "2026-04", "end_date": "2026-06", "rank": "正厅级", "note": "被查前岗位"},
    # 王军 — 前任市长
    {"person_id": 6, "org_id": 2, "title": "河池市人民政府市长", "start_date": "2021-02", "end_date": "2026-01", "rank": "正厅级", "note": "接任唐云舒"},
    {"person_id": 6, "org_id": 1, "title": "中共河池市委副书记", "start_date": "2021-02", "end_date": "2026-01", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 17, "title": "中共河池市委常委、巴马瑶族自治县委书记", "start_date": "2016-06", "end_date": "2021-02", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 16, "title": "中共贺州市委常委、市政府党组副书记", "start_date": "2016-05", "end_date": "2016-06", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 18, "title": "清华大学助理研究员（挂职百色）", "start_date": "2006-07", "end_date": "2008", "rank": "", "note": "2006助研挂任百色市政府副秘书长"},
    {"person_id": 6, "org_id": 15, "title": "百色市（田东县）/百色市委", "start_date": "2007", "end_date": "2016-05", "rank": "副厅级", "note": "田东县委副书记/县长/书记"},
    # 何辛幸 — 前任市委书记
    {"person_id": 7, "org_id": 1, "title": "中共河池市委书记", "start_date": "2015-12", "end_date": "2021-06", "rank": "正厅级", "note": "接任后由秦春成继任"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "河池市党政正职搭档：市委书记朱会东与市长汪东明", "overlap_org": "中共河池市委/河池市人民政府", "overlap_period": "2026-至今"},
    # 前任/继任
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "朱会东接任秦春成任市委书记（何辛幸→秦春成→朱会东）", "overlap_org": "中共河池市委", "overlap_period": "2026-04"},
    {"person_a": 5, "person_b": 7, "type": "predecessor_successor", "context": "秦春成接任何辛幸任市委书记", "overlap_org": "中共河池市委", "overlap_period": "2021"},
    {"person_a": 2, "person_b": 6, "type": "predecessor_successor", "context": "汪东明接任王军任市长", "overlap_org": "河池市人民政府", "overlap_period": "2026-02"},
    # 前任书记与前任市长搭班子
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "秦春成任书记、王军任市长（2021-2025）党政共治", "overlap_org": "河池市", "overlap_period": "2021-2026"},
    # 现任班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记与市人大主任黄锦锋", "overlap_org": "河池市", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记与市政协主席黎丽", "overlap_org": "河池市", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "市长与市人大主任", "overlap_org": "河池市", "overlap_period": "2026-至今"},
    # 王军跨区域网络（百色→贺州→河池）
    {"person_a": 6, "person_b": 5, "type": "overlap", "context": "王军原系河池市长、秦春成任书记，同台搭班", "overlap_org": "河池市委市政府", "overlap_period": "2021-2025"},
    # 纪检风险信号（秦春成被查，连同县级前任金城江区主官）
    {"person_a": 5, "person_b": 3, "type": "overlap", "context": "前任书记被查与现任市人大主任同属市四套班子（监督信号）", "overlap_org": "河池市纪委监委", "overlap_period": "2026"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Build complete.")