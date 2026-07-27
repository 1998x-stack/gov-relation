#!/usr/bin/env python3
"""Build 昆都仑区 (包头市, 内蒙古自治区) leadership network database and GEXF graph.

Data sourced from official government website (kdl.gov.cn) and news articles.
Confidence levels: confirmed (gov source), plausible (media/baike), unverified.
"""

import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parent.parent.parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "昆都仑区"
TASK_ID = "inner_mongolia_昆都仑区"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════
    # 1. 区委书记 - Party Secretary
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "胡强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "昆都仑区委书记",
        "current_org": "中国共产党包头市昆都仑区委员会",
        "source": "kdl.gov.cn 官方新闻 (2024-2026)",
    },
    # ══════════════════════════════════════════════════════════════════
    # 2. 区长 - District Mayor
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "石丽娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "内蒙古包头",
        "education": "研究生学历",
        "party_join": "2002-05",
        "work_start": "1998-09",
        "current_post": "昆都仑区委副书记、区长",
        "current_org": "昆都仑区人民政府",
        "source": "kdl.gov.cn 领导信息页 (2026-06-02)",
    },
    # ══════════════════════════════════════════════════════════════════
    # 3. 常务副区长 - Executive Deputy Mayor
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "刘利文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（分管政府日常工作）",
        "current_org": "昆都仑区人民政府",
        "source": "kdl.gov.cn 领导信息页",
    },
    # ══════════════════════════════════════════════════════════════════
    # 4. 纪委书记 - Discipline Inspection Secretary
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "胡婷",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "昆都仑区纪委监委",
        "source": "kdl.gov.cn 新闻 (2026-07-20 全区警示教育会)",
    },
    # ══════════════════════════════════════════════════════════════════
    # 5. 副区长（公安分局局长） - Deputy Mayor, Public Security
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "贺欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "昆都仑区副区长、公安分局局长",
        "current_org": "昆都仑区人民政府 / 包头市公安局昆都仑区分局",
        "source": "kdl.gov.cn 领导信息页",
    },
    # ══════════════════════════════════════════════════════════════════
    # 6. 副区长 - Deputy Mayor
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "王秀娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "内蒙古乌兰察布",
        "education": "大学学历",
        "party_join": "2002-12",
        "work_start": "1995-10",
        "current_post": "昆都仑区副区长",
        "current_org": "昆都仑区人民政府",
        "source": "kdl.gov.cn 领导信息页",
    },
    # ══════════════════════════════════════════════════════════════════
    # 7. 副区长 - Deputy Mayor
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 7,
        "name": "李红宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "山西朔州（籍贯）/ 内蒙古包头（出生地）",
        "education": "大学学历",
        "party_join": "1996-11",
        "work_start": "",
        "current_post": "昆都仑区副区长",
        "current_org": "昆都仑区人民政府",
        "source": "kdl.gov.cn 领导信息页",
    },
    # ══════════════════════════════════════════════════════════════════
    # 8. 政府党组成员 / 经开区管委会副主任
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "周海飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "山西神池",
        "education": "研究生学历，工商管理硕士",
        "party_join": "1999-11",
        "work_start": "1995-09",
        "current_post": "区政府党组成员、包头昆都仑经济技术开发区党工委副书记兼管委会副主任",
        "current_org": "昆都仑区人民政府 / 包头昆都仑经济技术开发区",
        "source": "kdl.gov.cn 领导信息页",
    },
    # ══════════════════════════════════════════════════════════════════
    # 9. 政府办主任 - Government Office Director
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "李飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-01",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、机关党组书记、政府办主任",
        "current_org": "昆都仑区人民政府办公室",
        "source": "kdl.gov.cn 领导信息页",
    },
    # ══════════════════════════════════════════════════════════════════
    # 10. 人大常委会主任 - People's Congress Chair
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "周敏捷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "昆都仑区人大常委会主任",
        "current_org": "昆都仑区人大常委会",
        "source": "百度百科 / kdl.gov.cn 新闻报道",
    },
    # ══════════════════════════════════════════════════════════════════
    # 11. 政协主席 - CPPCC Chair
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "武文清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "昆都仑区政协主席",
        "current_org": "昆都仑区政协",
        "source": "百度百科 / kdl.gov.cn 新闻报道",
    },
    # ══════════════════════════════════════════════════════════════════
    # 12. 前任区长 - Former Mayor
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "于占江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "kdl.gov.cn 新闻: 2026年5月15日区政府常务会议",
    },
    # ══════════════════════════════════════════════════════════════════
    # 13. 前任区委书记 - Former Party Secretary
    # ══════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "金永丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "包头市人大常委会副主任",
        "current_org": "包头市人大常委会",
        "source": "kdl.gov.cn 新闻: 2024年11月",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {
        "id": 0,
        "name": "中国共产党包头市昆都仑区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共包头市委",
        "location": "包头市昆都仑区",
    },
    {
        "id": 1,
        "name": "昆都仑区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "包头市人民政府",
        "location": "包头市昆都仑区",
    },
    {
        "id": 2,
        "name": "昆都仑区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共包头市昆都仑区委员会",
        "location": "包头市昆都仑区",
    },
    {
        "id": 3,
        "name": "包头市公安局昆都仑区分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "昆都仑区人民政府",
        "location": "包头市昆都仑区",
    },
    {
        "id": 4,
        "name": "昆都仑区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "包头市人大常委会",
        "location": "包头市昆都仑区",
    },
    {
        "id": 5,
        "name": "昆都仑区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "包头市政协",
        "location": "包头市昆都仑区",
    },
    {
        "id": 6,
        "name": "包头昆都仑经济技术开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "昆都仑区人民政府",
        "location": "包头市昆都仑区",
    },
    {
        "id": 7,
        "name": "昆都仑区人民政府办公室",
        "type": "政府",
        "level": "乡科级",
        "parent": "昆都仑区人民政府",
        "location": "包头市昆都仑区",
    },
    {
        "id": 8,
        "name": "包头市人大常委会",
        "type": "人大",
        "level": "地厅级",
        "parent": "包头市",
        "location": "包头市",
    },
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 胡强 - Party Secretary
    {"person_id": 1, "org_id": 0, "title": "昆都仑区委书记", "start_date": "2024-12-28", "end_date": "present", "rank": "县处级正职", "note": "2024年12月28日任命"},
    # 石丽娜 - District Mayor
    {"person_id": 2, "org_id": 1, "title": "昆都仑区区长", "start_date": "2026-05-28", "end_date": "present", "rank": "县处级正职", "note": "2026年5月28日当选"},
    {"person_id": 2, "org_id": 0, "title": "昆都仑区委副书记", "start_date": "2026-05", "end_date": "present", "rank": "县处级副职", "note": "兼任"},
    # 刘利文 - Executive Deputy Mayor
    {"person_id": 3, "org_id": 1, "title": "副区长（分管政府日常工作）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "常务副区长"},
    {"person_id": 3, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 胡婷 - Discipline Inspection
    {"person_id": 4, "org_id": 2, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 贺欣 - Deputy Mayor / Public Security
    {"person_id": 5, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管公安、司法、信访"},
    {"person_id": 5, "org_id": 3, "title": "公安分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 王秀娟 - Deputy Mayor
    {"person_id": 6, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管城区办事处、民政、市场管理、人社等"},
    # 李红宇 - Deputy Mayor
    {"person_id": 7, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管教育、医保、卫健、退役军人事务"},
    # 周海飞 - Party Group / ETDZ
    {"person_id": 8, "org_id": 6, "title": "党工委副书记兼管委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管工业、信息化"},
    {"person_id": 8, "org_id": 1, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李飞 - Government Office Director
    {"person_id": 9, "org_id": 7, "title": "政府办公室主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区政府党组成员、机关党组书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 周敏捷 - People's Congress Chair
    {"person_id": 10, "org_id": 4, "title": "昆都仑区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 武文清 - CPPCC Chair
    {"person_id": 11, "org_id": 5, "title": "昆都仑区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 于占江 - Former Mayor
    {"person_id": 12, "org_id": 1, "title": "昆都仑区区长（前任）", "start_date": "", "end_date": "2026-05", "rank": "县处级正职", "note": "2026年5月离任"},
    {"person_id": 12, "org_id": 0, "title": "昆都仑区委副书记（前任）", "start_date": "", "end_date": "2026-05", "rank": "县处级副职", "note": ""},
    # 金永丽 - Former Party Secretary
    {"person_id": 13, "org_id": 0, "title": "昆都仑区委书记（前任）", "start_date": "", "end_date": "2024-12", "rank": "县处级正职", "note": "2024年12月离任"},
    {"person_id": 13, "org_id": 8, "title": "包头市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 胡强 ↔ 石丽娜: 书记-区长搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长搭档",
        "overlap_org": "昆都仑区党委/政府",
        "overlap_period": "2026-05至今",
    },
    # 胡强 ↔ 刘利文: 同区委班子
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "区委书记与区委常委、常务副区长",
        "overlap_org": "昆都仑区委",
        "overlap_period": "2024-12至今",
    },
    # 胡强 ↔ 胡婷: 同区委班子
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "区委书记与纪委书记",
        "overlap_org": "昆都仑区委",
        "overlap_period": "2024-12至今",
    },
    # 石丽娜 ↔ 刘利文: 政府班子同事
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "区长与常务副区长",
        "overlap_org": "昆都仑区人民政府",
        "overlap_period": "2026-05至今",
    },
    # 石丽娜 ↔ 贺欣: 政府班子同事
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "区长与副区长（公安）",
        "overlap_org": "昆都仑区人民政府",
        "overlap_period": "2026-05至今",
    },
    # 石丽娜 ↔ 王秀娟: 政府班子同事
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "区长与副区长",
        "overlap_org": "昆都仑区人民政府",
        "overlap_period": "2026-05至今",
    },
    # 石丽娜 ↔ 李红宇: 政府班子同事
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "区长与副区长",
        "overlap_org": "昆都仑区人民政府",
        "overlap_period": "2026-05至今",
    },
    # 胡强 ↔ 金永丽: 前任-继任
    {
        "person_a": 1, "person_b": 13,
        "type": "predecessor_successor",
        "context": "接任金永丽为昆都仑区委书记",
        "overlap_org": "昆都仑区委",
        "overlap_period": "2024-12（交接）",
    },
    # 石丽娜 ↔ 于占江: 前任-继任
    {
        "person_a": 2, "person_b": 12,
        "type": "predecessor_successor",
        "context": "接替于占江为昆都仑区长",
        "overlap_org": "昆都仑区人民政府",
        "overlap_period": "2026-05（交接）",
    },
    # 于占江 ↔ 刘利文: 政府班子前同事
    {
        "person_a": 12, "person_b": 3,
        "type": "overlap",
        "context": "前任区长与常务副区长",
        "overlap_org": "昆都仑区人民政府",
        "overlap_period": "~2025至2026-05",
    },
    # 金永丽 ↔ 周敏捷: 党委-人大
    {
        "person_a": 13, "person_b": 10,
        "type": "overlap",
        "context": "前任区委书记与人大常委会主任",
        "overlap_org": "昆都仑区",
        "overlap_period": "~2022至2024-12",
    },
    # 周海飞 ↔ 李飞: 政府党组同事
    {
        "person_a": 8, "person_b": 9,
        "type": "overlap",
        "context": "同为区政府党组成员",
        "overlap_org": "昆都仑区人民政府党组",
        "overlap_period": "",
    },
]

# ── Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "昆都仑区_network.db",
        gexf_path=GRAPH_DIR / "昆都仑区_network.gexf",
    )
