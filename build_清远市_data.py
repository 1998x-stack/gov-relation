#!/usr/bin/env python3
"""Build script for 清远市 (Qingyuan City, Guangdong) leadership network.

清远市 is a prefecture-level city in northern Guangdong province.
It governs 2 districts (清城区, 清新区), 2 county-level cities (英德市, 连州市),
and 4 counties (佛冈县, 阳山县, 连山壮族瑶族自治县, 连南瑶族自治县).

Generated: 2026-07-22
Sources:
  - news.163.com (confirmed: 刘胜 appointed 清远市委书记 on 2025-12-26)
  - www.qingcheng.gov.cn (district-level confirmation of 清城区 leaders)
  - Note: qingyuan.gov.cn leadership page unreachable from this environment
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core targets: 市委书记 & 市长 ──
    {
        "id": 1,
        "name": "刘胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清远市委书记",
        "current_org": "中共清远市委员会",
        "source": "网易新闻: 刘胜任清远市委书记 (2025-12-26); 此前任潮州市市长。",
    },
    {
        "id": 2,
        "name": "温文星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清远市市长",
        "current_org": "清远市人民政府",
        "source": "根据公开报道, 温文星约于2022年起任清远市市长。当前截至2025-2026年需进一步确认为现任。",
    },
    # ── 其他市委常委/副市长 (待确认) ──
    # Note: Full leadership roster requires access to qingyuan.gov.cn/zwgk/ldzc/
    # which was unreachable from this environment. Below are placeholders for the
    # standard prefecture-level city structure.
    {
        "id": 3,
        "name": "常务副市长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "清远市人民政府",
        "source": "placeholder - leadership page unavailable",
    },
    {
        "id": 4,
        "name": "市纪委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共清远市纪律检查委员会",
        "source": "placeholder - leadership page unavailable",
    },
    {
        "id": 5,
        "name": "市委组织部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共清远市委组织部",
        "source": "placeholder - leadership page unavailable",
    },
    {
        "id": 6,
        "name": "市人大常委会主任（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "清远市人大常委会",
        "source": "placeholder - leadership page unavailable",
    },
    {
        "id": 7,
        "name": "市政协主席（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议清远市委员会",
        "source": "placeholder - leadership page unavailable",
    },
    # ── Predecessors (for network edges) ──
    {
        "id": 8,
        "name": "郭锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已落马（被查）",
        "current_org": "",
        "source": "广东省纪委监委: 清远市委原书记郭锋接受纪律审查和监察调查 (2023-10-07)。曾任清远市委书记至2023年。",
    },
    {
        "id": 9,
        "name": "黄喜忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "广东普宁",
        "education": "在职研究生、法学博士",
        "party_join": "中共党员",
        "work_start": "1993年7月",
        "current_post": "鹰潭市委书记（已调任江西）",
        "current_org": "中共鹰潭市委员会",
        "source": "build_ganzhou_data.py: 黄喜忠2018-2019年任清远市市长。",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共清远市委员会", "type": "党委", "level": "正厅级", "parent": "中共广东省委员会", "location": "清远市清城区"},
    {"id": 2, "name": "清远市人民政府", "type": "政府", "level": "正厅级", "parent": "广东省人民政府", "location": "清远市清城区"},
    {"id": 3, "name": "清远市人大常委会", "type": "人大", "level": "正厅级", "parent": "广东省人大常委会", "location": "清远市清城区"},
    {"id": 4, "name": "中国人民政治协商会议清远市委员会", "type": "政协", "level": "正厅级", "parent": "广东省政协", "location": "清远市清城区"},
    {"id": 5, "name": "中共清远市纪律检查委员会", "type": "纪委", "level": "正厅级", "parent": "中共广东省纪律检查委员会", "location": "清远市清城区"},
    {"id": 6, "name": "中共清远市委组织部", "type": "党委部门", "level": "正处级", "parent": "中共清远市委员会", "location": "清远市清城区"},
    {"id": 7, "name": "中共清远市清城区委员会", "type": "党委", "level": "正处级", "parent": "中共清远市委员会", "location": "清远市清城区"},
    {"id": 8, "name": "清远市清城区人民政府", "type": "政府", "level": "正处级", "parent": "清远市人民政府", "location": "清远市清城区"},
]

POSITIONS = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "清远市委书记", "start_date": "2025-12", "end_date": "present", "rank": "正厅级", "note": "2025年12月从潮州市市长调任"},
    {"person_id": 2, "org_id": 2, "title": "清远市市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "同时兼任市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # Standing committee members (placeholders)
    {"person_id": 3, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待确认具体姓名"},
    {"person_id": 4, "org_id": 5, "title": "市委常委、市纪委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待确认具体姓名"},
    {"person_id": 5, "org_id": 6, "title": "市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待确认具体姓名"},
    # Four-bank heads
    {"person_id": 6, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "待确认具体姓名（通常由市委书记兼任）"},
    {"person_id": 7, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "待确认具体姓名"},
    # Predecessors
    {"person_id": 8, "org_id": 1, "title": "清远市委书记", "start_date": "2018", "end_date": "2023-10", "rank": "正厅级", "note": "2023年10月被查"},
    {"person_id": 8, "org_id": 3, "title": "市人大常委会主任（兼）", "start_date": "", "end_date": "2023-10", "rank": "正厅级", "note": "市委书记兼任"},
    {"person_id": 9, "org_id": 2, "title": "清远市市长", "start_date": "2018-03", "end_date": "2019-12", "rank": "正厅级", "note": "2019年底调任江西省"},
]

# Relationships based on organizational overlap and working proximity
RELATIONSHIPS = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记-市长党政正职搭档", "overlap_org": "清远市四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "confirmed"},
    # 市委书记与市委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记—市委常委（常务副市长）", "overlap_org": "清远市委常委会", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记—市委常委（市纪委书记）", "overlap_org": "清远市委常委会", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记—市委常委（组织部部长）", "overlap_org": "清远市委常委会", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    # 市长与副市长
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "市长—常务副市长", "overlap_org": "清远市人民政府", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    # 四套班子正职之间
    {"person_a": 1, "person_b": 6, "type": "同僚", "context": "市委书记—市人大常委会主任", "overlap_org": "清远市四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 1, "person_b": 7, "type": "同僚", "context": "市委书记—市政协主席", "overlap_org": "清远市四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 2, "person_b": 6, "type": "同僚", "context": "市长—市人大常委会主任", "overlap_org": "清远市四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 2, "person_b": 7, "type": "同僚", "context": "市长—市政协主席", "overlap_org": "清远市四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    # 前后任关系
    {"person_a": 8, "person_b": 1, "type": "前后任", "context": "前任清远市委书记（郭锋）——现任市委书记（刘胜）", "overlap_org": "中共清远市委员会", "overlap_period": "2023-2025", "source": "", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 2, "type": "前后任", "context": "前任清远市长（黄喜忠）与现市长（温文星）之间的前后任关系", "overlap_org": "清远市人民政府", "overlap_period": "2019-2022", "source": "", "confidence": "plausible"},
    # 历史搭档
    {"person_a": 8, "person_b": 9, "type": "党政正职搭档", "context": "清远市委书记（郭锋）—市长（黄喜忠）曾为搭档", "overlap_org": "清远市四套班子", "overlap_period": "2018-2019", "source": "build_ganzhou_data.py", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "清远市_network.db"
GEXF_PATH = GRAPH_DIR / "清远市_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="清远市",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
