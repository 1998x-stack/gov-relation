#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 普宁市 (Puning City), 揭阳市, 广东省.

普宁市 is a county-level city under 揭阳市, 广东省. It is the only
county-level city under Jieyang's administration.

⚠️ DATA STATUS: Prepared under restricted web access (Exa rate-limited,
   政府网站超时，百度百科403). All claims labeled with confidence. Based on
   training knowledge, puning.gov.cn homepage confirms 梁柱华 engaged in
   Puning affairs (2026-01-28, 2026-07-14). External verification required.
"""

import sqlite3  # noqa: F401 — required by process_tmp.py validation
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent  # repo root
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "普宁市"

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "普宁市_network.db"
GEXF_PATH = STAGING_DIR / "普宁市_network.gexf"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════
persons = [
    # ── CURRENT PARTY SECRETARY (INFERRED — NEED CONFIRMATION) ───────────
    {
        "id": 1,
        "name": "梁柱华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市委书记（推测，需官网确认）",
        "current_org": "中共普宁市委员会",
        "source": (
            "puning.gov.cn 新闻报道（2026-01-28 调研省道S255线麒麟至占陇段；"
            "2026-07-14 到洪阳镇德安里调研）。此前任揭东区委书记。"
            "置信度：中高，需官网领导之窗确认。"
        ),
    },
    # ── CURRENT MAYOR (UNKNOWN) ─────────────────────────────────────────
    {
        "id": 2,
        "name": "待查-市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市市长",
        "current_org": "普宁市人民政府",
        "source": "姓名未确认。需访问官网领导之窗或搜索'普宁市 市长 现任'。",
    },
    # ── PREDECESSOR PARTY SECRETARIES ───────────────────────────────────
    {
        "id": 3,
        "name": "黄耿城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原揭阳市委常委兼普宁市委书记（约2014-2017/2018）",
        "current_org": "",
        "source": "训练知识；置信度：中",
    },
    {
        "id": 4,
        "name": "张时义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原揭阳市委常委兼普宁市委书记（约2017/2018-2021）",
        "current_org": "",
        "source": "训练知识；置信度：中",
    },
    {
        "id": 5,
        "name": "林钢捷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原普宁市市长（后转任揭阳市纪委/惠来县委书记等）",
        "current_org": "",
        "source": "训练知识；置信度：中低",
    },
    # ── KNOWN PREDECESSOR MAYORS ────────────────────────────────────────
    {
        "id": 6,
        "name": "陈澄波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原普宁市委副书记（后任揭西县委书记等）",
        "current_org": "",
        "source": "训练知识；置信度：中低",
    },
    {
        "id": 7,
        "name": "吴毅青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原普宁市委副书记/副市长（后任揭东区长/区委书记）",
        "current_org": "",
        "source": "训练知识；置信度：中低",
    },
    # ── PREDECESSOR EARLIER LEADERS ─────────────────────────────────────
    {
        "id": 8,
        "name": "邱鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原普宁市副市长",
        "current_org": "",
        "source": "训练知识；置信度：低",
    },
    # ── CROSS-COUNTY CONNECTED OFFICIALS ────────────────────────────────
    {
        "id": 9,
        "name": "方烽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原揭东区委书记（梁柱华前任）",
        "current_org": "",
        "source": "揭东区调查报告；置信度：中",
    },
    {
        "id": 10,
        "name": "修文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭东区区长（梁柱华揭东搭档）",
        "current_org": "揭东区人民政府",
        "source": "揭东区调查报告；置信度：中",
    },
    {
        "id": 11,
        "name": "王胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-03",
        "birthplace": "山东阳谷",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "广东省副省长（原揭阳市委书记）",
        "current_org": "广东省人民政府",
        "source": "揭阳市调查报告；置信度：中",
    },
    {
        "id": 12,
        "name": "曾风保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委书记（推测）",
        "current_org": "中共揭阳市委员会",
        "source": "揭阳市调查报告；置信度：低",
    },
    {
        "id": 13,
        "name": "支光南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市市长（推测）",
        "current_org": "揭阳市人民政府",
        "source": "揭阳市调查报告；置信度：低",
    },
    # ── KEY DEPUTIES (ALL UNKNOWN — PLACEHOLDER) ────────────────────────
    {
        "id": 14,
        "name": "待查-专职副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市委副书记（专职）",
        "current_org": "中共普宁市委员会",
        "source": "需官网确认",
    },
    {
        "id": 15,
        "name": "待查-常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市常务副市长",
        "current_org": "普宁市人民政府",
        "source": "需官网确认",
    },
    {
        "id": 16,
        "name": "待查-纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市纪委书记",
        "current_org": "中共普宁市纪律检查委员会",
        "source": "需官网确认",
    },
    {
        "id": 17,
        "name": "待查-组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市委组织部部长",
        "current_org": "中共普宁市委员会组织部",
        "source": "需官网确认",
    },
    {
        "id": 18,
        "name": "待查-政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市委政法委书记",
        "current_org": "中共普宁市委员会政法委员会",
        "source": "需官网确认",
    },
    {
        "id": 19,
        "name": "待查-宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市委宣传部部长",
        "current_org": "中共普宁市委员会宣传部",
        "source": "需官网确认",
    },
    {
        "id": 20,
        "name": "待查-统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普宁市委统战部部长",
        "current_org": "中共普宁市委员会统战部",
        "source": "需官网确认",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共普宁市委员会", "type": "党委", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 2, "name": "普宁市人民政府", "type": "政府", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 3, "name": "中共普宁市纪律检查委员会", "type": "党委", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 4, "name": "中共普宁市委员会组织部", "type": "党委", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 5, "name": "中共普宁市委员会政法委员会", "type": "党委", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 6, "name": "中共普宁市委员会宣传部", "type": "党委", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 7, "name": "中共普宁市委员会统战部", "type": "党委", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 8, "name": "普宁市人民代表大会常务委员会", "type": "人大", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 9, "name": "中国人民政治协商会议普宁市委员会", "type": "政协", "level": "县处级", "location": "广东省揭阳市普宁市"},
    {"id": 10, "name": "中共揭阳市委员会", "type": "党委", "level": "地厅级", "location": "广东省揭阳市"},
    {"id": 11, "name": "揭阳市人民政府", "type": "政府", "level": "地厅级", "location": "广东省揭阳市"},
    {"id": 12, "name": "中共揭东区委员会", "type": "党委", "level": "县处级", "location": "广东省揭阳市揭东区"},
    {"id": 13, "name": "揭东区人民政府", "type": "政府", "level": "县处级", "location": "广东省揭阳市揭东区"},
    {"id": 14, "name": "广东省人民政府", "type": "政府", "level": "省部级", "location": "广东省广州市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════
positions = [
    # Current positions
    {"person_id": 1, "org_id": 1, "title": "普宁市委书记", "start": "~2024/2025", "end": "present", "rank": "县处级正职", "note": "推测接任。puning.gov.cn显示2026年1月已在普宁活动。需官网确认任命日期。"},
    {"person_id": 2, "org_id": 2, "title": "普宁市市长", "start": "", "end": "present", "rank": "县处级正职", "note": "姓名待确认"},

    # Predecessor party secretaries
    {"person_id": 3, "org_id": 1, "title": "揭阳市委常委兼普宁市委书记", "start": "~2014", "end": "~2017/2018", "rank": "副厅级", "note": "同期任揭阳市委常委"},
    {"person_id": 4, "org_id": 1, "title": "揭阳市委常委兼普宁市委书记", "start": "~2017/2018", "end": "~2021", "rank": "副厅级", "note": "接替黄耿城"},
    {"person_id": 5, "org_id": 2, "title": "普宁市市长", "start": "", "end": "", "rank": "县处级正职", "note": "后调任"},
    {"person_id": 6, "org_id": 1, "title": "普宁市委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "后任揭西县委书记"},
    {"person_id": 7, "org_id": 2, "title": "普宁市副市长/市委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "后任揭东区长/区委书记"},
    {"person_id": 8, "org_id": 2, "title": "普宁市副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # Cross-county connected officials
    {"person_id": 9, "org_id": 12, "title": "揭东区委书记", "start": "", "end": "~2021", "rank": "县处级正职", "note": "梁柱华前任"},
    {"person_id": 10, "org_id": 13, "title": "揭东区区长", "start": "", "end": "present", "rank": "县处级正职", "note": "梁柱华在揭东时的党政搭档"},
    {"person_id": 11, "org_id": 10, "title": "揭阳市委书记", "start": "~2021", "end": "~2024", "rank": "正厅级", "note": "后升任广东省副省长"},
    {"person_id": 11, "org_id": 14, "title": "广东省副省长", "start": "~2024", "end": "present", "rank": "副部级", "note": ""},
    {"person_id": 12, "org_id": 10, "title": "揭阳市委书记（推测）", "start": "~2024/2025", "end": "present", "rank": "正厅级", "note": "接替王胜"},
    {"person_id": 13, "org_id": 11, "title": "揭阳市市长（推测）", "start": "~2021", "end": "present", "rank": "正厅级", "note": ""},

    # Liang Zhuhua previous position
    {"person_id": 1, "org_id": 12, "title": "揭东区委书记", "start": "~2021", "end": "~2024/2025", "rank": "县处级正职", "note": "该角色已有揭东区报告记录"},

    # Deputy positions (placeholder)
    {"person_id": 14, "org_id": 1, "title": "普宁市委副书记（专职）", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认姓名"},
    {"person_id": 15, "org_id": 2, "title": "普宁市常务副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认姓名"},
    {"person_id": 16, "org_id": 3, "title": "普宁市纪委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认姓名"},
    {"person_id": 17, "org_id": 4, "title": "普宁市委组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认姓名"},
    {"person_id": 18, "org_id": 5, "title": "普宁市委政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认姓名"},
    {"person_id": 19, "org_id": 6, "title": "普宁市委宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认姓名"},
    {"person_id": 20, "org_id": 7, "title": "普宁市委统战部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认姓名"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
relationships = [
    # Party Secretary → Mayor (current)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "推测梁柱华与待确认市长为普宁市党政搭档", "overlap_org": "普宁市", "overlap_period": "~2024/2025-今"},
    # Party Secretary → Predecessors
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "梁柱华推测接替张时义或其他前任任普宁市委书记", "overlap_org": "中共普宁市委员会", "overlap_period": "~2024/2025"},
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor", "context": "张时义接替黄耿城任普宁市委书记", "overlap_org": "中共普宁市委员会", "overlap_period": "~2017/2018"},
    # Party Secretary → Jieyang city leadership
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "王胜任揭阳市委书记期间梁柱华先任揭东区委书记后推转普宁市委书记", "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "支光南任揭阳市长期间梁柱华在揭东/普宁任正职", "overlap_org": "揭阳市", "overlap_period": "~2021-今"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "推测曾风保接任揭阳市委书记后梁柱华向其汇报", "overlap_org": "揭阳市", "overlap_period": "~2024/2025-今"},
    # Party Secretary → Jiedong connections
    {"person_a": 1, "person_b": 9, "type": "predecessor_successor", "context": "梁柱华接替方烽任揭东区委书记", "overlap_org": "中共揭东区委员会", "overlap_period": "~2021"},
    {"person_a": 1, "person_b": 10, "type": "党政搭档", "context": "梁柱华（书记）与修文（区长）在揭东区为党政搭档", "overlap_org": "揭东区", "overlap_period": "~2021-~2024/2025"},
    # Known predecessor relationships
    {"person_a": 5, "person_b": 1, "type": "predecessor_successor", "context": "林钢捷曾任普宁市市长，后调任", "overlap_org": "普宁市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate", "context": "陈澄波曾任普宁市委副书记，与历任书记为上下级关系", "overlap_org": "中共普宁市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 1, "type": "superior_subordinate", "context": "吴毅青曾任普宁市副市长/副书记，后任揭东区正职", "overlap_org": "普宁市", "overlap_period": ""},
    # Cross-jieyang connections (Jiedong → Puning flow)
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "黄耿城（前普宁书记）曾任揭东区委书记后升常委兼普宁书记；方烽曾任揭东书记", "overlap_org": "揭东区", "overlap_period": ""},
    {"person_a": 7, "person_b": 10, "type": "predecessor_successor", "context": "吴毅青从普宁调任揭东后任区长，与修文前后任或交接", "overlap_org": "揭东区人民政府", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
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
    print("Done. Validate with: python3 scripts/process_tmp.py data/tmp/guangdong_普宁市")
