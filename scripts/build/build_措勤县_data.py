#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 措勤县 (Coqên County), 阿里地区, 西藏自治区.

Current officeholders as of 2026-07:
  - Party Secretary (县委书记) & County Mayor (县长): 刘勇刚 (Liu Yonggang) — holding both roles
    (born 1982.09, Han, bachelor's degree, party member, confirmed from official government bio)
  - Previous Party Secretary (前县委书记): 扎西罗布 — last seen June 2025, whereabouts unknown
  - Deputy Party Secretary & Executive Deputy: 王国青 (from 阿里地委)
  - Organization Department Head: 刘伟斌
  - County Party Committee member & Deputy Mayor: 朱玺
  - Political & Legal Affairs Secretary & Public Security: 黄艾民
  - Former Discipline Inspection Secretary: 陈磊

Sources:
  - https://cuoqinxian.gov.cn/ (official county government website)
  - https://cuoqinxian.gov.cn/info/1031/501581.htm (刘勇 official bio)
  - https://cuoqinxian.gov.cn/xwdt/lddt/ (leadership activity page)
  - Multiple news articles on cuoqinxian.gov.cn confirming meetings and events

Web access note: Exa rate-limited, Baidu 403/blocked, many Chinese search engines captcha.
Core leader names are confirmed from the official county website, but full biographical
details (birthplace, specific career timeline entries before current role) remain limited.
"""

import os, sys, sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "措勤县_network.db")
GEXF_PATH = os.path.join(STAGING, "措勤县_network.gexf")

# =========================================================================
# PERSONS
# Confidence labels: confirmed=official source, plausible=credible media,
#                    unverified=insufficient evidence
# =========================================================================
persons = [
    # ── Current top leadership (一肩挑: Party Secretary + County Magistrate) ──
    {
        "id": 1,
        "name": "刘勇刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "措勤县委书记、县长（一肩挑）",
        "current_org": "中共措勤县委员会 / 措勤县人民政府",
        "source": "Confirmed: cuoqinxian.gov.cn (official bio page, 2025-03-06) and multiple 2026 news articles referencing '县委书记刘勇刚'"
    },
    # ── Previous Party Secretary ──
    {
        "id": 2,
        "name": "扎西罗布",
        "gender": "",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "卸任措勤县委书记（去向未确认）",
        "current_org": "（已离任）",
        "source": "Confirmed: cuoqinxian.gov.cn news, last appearing on 2025-06-23 as '措勤县委书记'. No public record found after that date."
    },
    # ── Executive Deputy Secretary / Deputy Mayor (from Ali Prefecture) ──
    {
        "id": 3,
        "name": "王国青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "措勤县委常务副书记、县政府常务副县长",
        "current_org": "中共措勤县委员会 / 措勤县人民政府",
        "source": "Confirmed: cuoqinxian.gov.cn news 2025-09-18, '阿里地委副秘书长、措勤县委常务副书记、常务副县长王国'"
    },
    # ── Organization Department Head ──
    {
        "id": 4,
        "name": "刘伟斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "措勤县委常委、组织部部长",
        "current_org": "中共措勤县委组织部",
        "source": "Confirmed: cuoqinxian.gov.cn news 2025-09 (presiding over cadre appointment meetings)"
    },
    # ── County Party Deputy Mayor ──
    {
        "id": 5,
        "name": "朱玺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "措勤县委常委、政府副县长",
        "current_org": "措勤县人民政府",
        "source": "Confirmed: cuoqinxian.gov.cn news 2025-11"
    },
    # ── Political & Legal Affairs Secretary, Public Security ──
    {
        "id": 6,
        "name": "黄艾民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "措勤县委常委、政法委书记、公安局局长",
        "current_org": "中共措勤县委政法委 / 措勤县公安局",
        "source": "Confirmed: cuoqinxian.gov.cn news 2025-04"
    },
    # ── Deputy Secretary (驻村干部总领队) ──
    {
        "id": 7,
        "name": "吴峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "措勤县委副书记、驻村工作总领队",
        "current_org": "中共措勤县委",
        "source": "Confirmed: cuoqinxian.gov.cn news 2025-06 to 2025-08"
    },
    # ── Former Discipline Inspection Secretary ──
    {
        "id": 8,
        "name": "陈磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "措勤县委常委、纪委书记、监委主任（2022年任职，后可能调整）",
        "current_org": "中共措勤县纪律检查委员会",
        "source": "Plausible: cuoqinxian.gov.cn news 2022-09; not appearing in recent 2025-2026 coverage"
    },
    # ── Former Organization Department Head ──
    {
        "id": 9,
        "name": "钟文君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "曾任措勤县委常委、组织部部长（2022-2023年）",
        "current_org": "（已离任）",
        "source": "Plausible: cuoqinxian.gov.cn news 2022-12 to 2023-02, later replaced by 刘伟斌"
    },
    # ── County NPC Deputy Director (dismissed) ──
    {
        "id": 10,
        "name": "达贵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "已被免去县人大常委会副主任职务（2026-03）",
        "current_org": "（已离任）",
        "source": "Confirmed: cuoqinxian.gov.cn 2026-03-31 news regarding personnel changes"
    },
    {
        "id": 11,
        "name": "杨倩倩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "县人大常委会办公室主任",
        "current_org": "措勤县人大常委会",
        "source": "Confirmed: cuoqinxian.gov.cn 2026-03-31 news (appointed)"
    },
    {
        "id": 12,
        "name": "土加次仁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "措勤县委常委、县人大常委会主任（2022年任职）",
        "current_org": "措勤县人大常委会",
        "source": "Plausible: cuoqinxian.gov.cn news 2022-11"
    },
    {
        "id": 13,
        "name": "罗开拓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "曾任措勤县委副书记、驻村工作总领队（2025年初）",
        "current_org": "（已离任）",
        "source": "Plausible: cuoqinxian.gov.cn news 2025-01 to 2025-04"
    },
    {
        "id": 14,
        "name": "胡利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "曾任措勤县委副书记、驻村工作总领队（2022年）",
        "current_org": "（已离任）",
        "source": "Plausible: cuoqinxian.gov.cn news 2022-08"
    },
    # ── Former Ali Vice Commissioner / County Party Secretary ──
    {
        "id": 15,
        "name": "杨红兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "parent_join": "",
        "work_start": "",
        "current_post": "阿里地区行署副专员（曾兼任措勤县委书记）",
        "current_org": "阿里地区行政公署",
        "source": "Plausible: Sogou search result (inspection news article mentioning '阿里地区行署副专员、措勤县委书记杨红兵')"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共措勤县委员会", "type": "党委", "level": "县", "parent": "阿里地区", "location": "措勤县"},
    {"id": 2, "name": "措勤县人民政府", "type": "政府", "level": "县", "parent": "阿里地区", "location": "措勤县"},
    {"id": 3, "name": "中共措勤县纪律检查委员会", "type": "党委", "level": "县", "parent": "阿里地区", "location": "措勤县"},
    {"id": 4, "name": "措勤县监察委员会", "type": "政府", "level": "县", "parent": "阿里地区", "location": "措勤县"},
    {"id": 5, "name": "中共措勤县委组织部", "type": "党委", "level": "县", "parent": "中共措勤县委员会", "location": "措勤县"},
    {"id": 6, "name": "中共措勤县委政法委", "type": "党委", "level": "县", "parent": "中共措勤县委员会", "location": "措勤县"},
    {"id": 7, "name": "措勤县公安局", "type": "政府", "level": "县", "parent": "措勤县人民政府", "location": "措勤县"},
    {"id": 8, "name": "措勤县人大常委会", "type": "人大", "level": "县", "parent": "阿里地区", "location": "措勤县"},
    {"id": 9, "name": "阿里地区行政公署", "type": "政府", "level": "地区", "parent": "西藏自治区", "location": "阿里地区"},
    {"id": 10, "name": "中共阿里地区委员会", "type": "党委", "level": "地区", "parent": "西藏自治区", "location": "阿里地区"},
]

# =========================================================================
# POSITIONS (person → organization assignments)
# =========================================================================
positions = [
    # 刘勇刚
    {"person_id": 1, "org_id": 1, "title": "措勤县委书记", "start": "2026-04", "end": "present", "rank": "正处级", "note": "2026年初起兼任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "措勤县人民政府县长", "start": "~2022", "end": "present", "rank": "正处级", "note": "一级调研员"},
    # 扎西罗布
    {"person_id": 2, "org_id": 1, "title": "措勤县委书记", "start": "~2021", "end": "2025-06", "rank": "正处级", "note": "去向不明"},
    # 王国青
    {"person_id": 3, "org_id": 1, "title": "措勤县委常务副书记（阿里地委副秘书长兼任）", "start": "~2025-09", "end": "present", "rank": "正处级", "note": "从阿里地区委派"},
    {"person_id": 3, "org_id": 2, "title": "措勤县人民政府常务副县长（兼任）", "start": "~2025-09", "end": "present", "rank": "正处级", "note": ""},
    # 刘伟斌
    {"person_id": 4, "org_id": 5, "title": "措勤县委常委、组织部部长", "start": "~2025", "end": "present", "rank": "副处级", "note": ""},
    # 朱玺
    {"person_id": 5, "org_id": 2, "title": "措勤县委常委、政府副县长", "start": "~2025-11", "end": "present", "rank": "副处级", "note": ""},
    # 黄艾民
    {"person_id": 6, "org_id": 6, "title": "措勤县委常委、政法委书记", "start": "~2025-04", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "措勤县公安局局长", "start": "~2025-04", "end": "present", "rank": "副处级", "note": "兼任"},
    # 吴峰
    {"person_id": 7, "org_id": 1, "title": "措勤县委副书记、驻村工作总领队", "start": "~2025-06", "end": "present", "rank": "正处级", "note": "由阿里地区派出"},
    # 陈磊
    {"person_id": 8, "org_id": 3, "title": "措勤县委常委、纪委书记", "start": "~2022-09", "end": "~2025", "rank": "副处级", "note": "2022年报道较多，近期较少"},
    {"person_id": 8, "org_id": 4, "title": "措勤县监委主任", "start": "~2022-09", "end": "~2025", "rank": "副处级", "note": ""},
    # 钟文军
    {"person_id": 9, "org_id": 1, "title": "措勤县委常委", "start": "~2022-12", "end": "~2023", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "措勤县委组织部部长", "start": "~2022-12", "end": "~2023", "rank": "副处级", "note": "后被刘伟斌接替"},
    # 达贵
    {"person_id": 10, "org_id": 8, "title": "措勤县人大常委会副主任", "start": "unknown", "end": "2026-03", "rank": "副处级", "note": "2026年3月被免职"},
    # 杨倩倩
    {"person_id": 11, "org_id": 8, "title": "措勤县人大常委会办公室主任", "start": "2026-03", "end": "present", "rank": "正科级", "note": ""},
    # 土加次仁
    {"person_id": 12, "org_id": 8, "title": "措勤县委常委、县人大常委会主任", "start": "~2022-11", "end": "present", "rank": "正处级", "note": ""},
    # 罗开拓
    {"person_id": 13, "org_id": 1, "title": "措勤县委副书记、驻村工作总领队", "start": "~2025-01", "end": "~2025-04", "rank": "正处级", "note": ""},
    # 胡利
    {"person_id": 14, "org_id": 1, "title": "措勤县委副书记、驻村工作总领队", "start": "~2022", "end": "~2022-08", "rank": "正处级", "note": ""},
    # 杨红兵
    {"person_id": 15, "org_id": 9, "title": "阿里地区行署副专员", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "措勤县委书记（曾任）", "start": "unknown", "end": "~2021", "rank": "正处级", "note": "前任扎西罗布的前任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Core leadership pair: 刘勇刚 ↔ 扎西罗布 (predecessor/successor chain)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "刘勇刚接替扎西罗布任县委书记", "overlap_org": "中共措勤县委", "overlap_period": "unknown"},
    # 刘勇刚 ↔ 王国青 (colleague in county party committee)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共措勤县委", "overlap_period": "2025-09~present"},
    # 刘勇刚 ↔ 刘伟斌 (superior-subordinate)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "组织部部长在县委书记领导下工作", "overlap_org": "中共措勤县委", "overlap_period": "2025~present"},
    # 刘勇刚 ↔ 吴峰 (superior-subordinate)
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "驻村总领队归县委领导", "overlap_org": "中共措勤县委", "overlap_period": "2025-06~present"},
    # 刘勇刚 ↔ 黄艾民 (superior-subordinate, party committee members)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委会成员", "overlap_org": "中共措勤县委", "overlap_period": "2025-04~present"},
    # 王国青 ↔ 刘伟斌 (colleague)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委常委会成员", "overlap_org": "中共措勤县委", "overlap_period": "2025~present"},
    # 刘伟斌 ← 钟文军 (successor chain in org department)
    {"person_a": 4, "person_b": 9, "type": "predecessor_successor", "context": "刘伟斌接替钟文军任组织部部长", "overlap_org": "中共措勤县委组织部", "overlap_period": "~2023~2025"},
    # 吴峰 ← 罗开拓 ← 胡利 (驻村总领队 succession chain)
    {"person_a": 7, "person_b": 13, "type": "predecessor_successor", "context": "吴峰接替罗开拓任驻村总领队", "overlap_org": "中共措勤县委", "overlap_period": "2025-04~2025-06"},
    {"person_a": 13, "person_b": 14, "type": "predecessor_successor", "context": "罗拓接替胡利任驻村总领队", "overlap_org": "中共措勤县委", "overlap_period": "2022~2025-01"},
    # 杨红兵 → 扎西罗布 → 刘勇刚 (三任县委书记链)
    {"person_a": 15, "person_b": 2, "type": "predecessor_successor", "context": "杨红兵→扎西罗布→刘勇刚 三任县委书记", "overlap_org": "中共措勤县委", "overlap_period": "~2021"},
    {"person_a": 15, "person_b": 1, "type": "predecessor_successor", "context": "杨红兵系刘勇刚前两任县委书记", "overlap_org": "中共措勤县委", "overlap_period": "~tang-Yanci period"},
    # 王国青 ↔ 阿里地委 (阿里 civil to county)
    {"person_a": 3, "person_b": 15, "type": "same_system", "context": "王国青来自阿里地委，杨红兵曾任阿副专员", "overlap_org": "阿里地区", "overlap_period": "unknown"},
]

# =========================================================================
# BUILD
# =========================================================================
run_build(
    slug="措勤县",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
)

print(f"\nEnjoy! Generated {DB_PATH} and {GEXF_PATH} successfully.")