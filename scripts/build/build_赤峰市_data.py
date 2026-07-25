#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 赤峰市 leadership network.

赤峰市, 内蒙古自治区 (地级市)
Research date: 2026-07-25
"""

import sqlite3  # noqa: F401  # required by process_tmp validation
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "赤峰市"
BASE = Path(__file__).resolve().parent
DB_PATH = BASE / f"{SLUG}_network.db"
GEXF_PATH = BASE / f"{SLUG}_network.gexf"

# ── PERSONS ──────────────────────────────────────────────────────────
# Confidence: confirmed = official source / appointment notice
#             plausible = credible media with partial corroboration
#             unverified = lead without enough evidence

persons = [
    # ════ Current Top Leaders (地厅级) ════
    {
        "id": 1,
        "name": "唐毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤峰市委书记",
        "current_org": "中国共产党赤峰市委员会",
        "source": "https://www.chifeng.gov.cn/ywdt/cfyw/202607/t20260723_2795708.html",
    },
    {
        "id": 2,
        "name": "栾天猛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤峰市委副书记、市长",
        "current_org": "赤峰市人民政府",
        "source": "https://www.chifeng.gov.cn/ywdt/cfyw/202607/t20260713_2791861.html",
    },
    # ════ 人大常委会主任 ════
    {
        "id": 3,
        "name": "睢利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤峰市人大常委会主任",
        "current_org": "赤峰市人民代表大会常务委员会",
        "source": "https://www.chifeng.gov.cn/ywdt/cfyw/202607/t20260723_2795708.html",
    },
    # ════ 政协主席 ════
    {
        "id": 4,
        "name": "苏雅勒其其格",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤峰市政协主席",
        "current_org": "中国人民政治协商会议赤峰市委员会",
        "source": "https://www.chifeng.gov.cn/ywdt/cfyw/202607/t20260723_2795708.html",
    },
    # ════ 市委常委 ════
    {
        "id": 5,
        "name": "王生才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤峰市委常委、统战部部长",
        "current_org": "中国共产党赤峰市委员会",
        "source": "https://www.chifeng.gov.cn/ywdt/cfyw/202607/t20260723_2795708.html",
    },
    # ════ 副市长/市领导 ════
    {
        "id": 6,
        "name": "王永军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤峰市副市长",
        "current_org": "赤峰市人民政府",
        "source": "https://www.chifeng.gov.cn/ywdt/cfyw/202607/t20260715_2793205.html",
    },
    {
        "id": 7,
        "name": "付守利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤峰市副市长",
        "current_org": "赤峰市人民政府",
        "source": "https://www.chifeng.gov.cn/ywdt/cfyw/202607/t20260708_2790877.html",
    },
    # ════ 前任市委书记 ════
    {
        "id": 8,
        "name": "万超岐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内蒙古自治区人大常委会代表工作委员会主任",
        "current_org": "内蒙古自治区人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E4%B8%87%E8%B6%85%E5%B2%90",
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党赤峰市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中国共产党内蒙古自治区委员会",
        "location": "内蒙古自治区赤峰市",
    },
    {
        "id": 2,
        "name": "赤峰市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "内蒙古自治区人民政府",
        "location": "内蒙古自治区赤峰市",
    },
    {
        "id": 3,
        "name": "赤峰市人民代表大会常务委员会",
        "type": "人大",
        "level": "地厅级",
        "parent": "",
        "location": "内蒙古自治区赤峰市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议赤峰市委员会",
        "type": "政协",
        "level": "地厅级",
        "parent": "",
        "location": "内蒙古自治区赤峰市",
    },
    {
        "id": 5,
        "name": "中国共产党赤峰市委员会统一战线工作部",
        "type": "党委",
        "level": "地厅级",
        "parent": "中国共产党赤峰市委员会",
        "location": "内蒙古自治区赤峰市",
    },
    {
        "id": 6,
        "name": "内蒙古自治区人民代表大会常务委员会",
        "type": "人大",
        "level": "省部级",
        "parent": "",
        "location": "内蒙古自治区呼和浩特市",
    },
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # 唐毅 - 赤峰市委书记 (current)
    {"id": 1, "person_id": 1, "org_id": 1, "title": "赤峰市委书记",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": "2026年7月以市委书记身份多次公开活动。此前曾任内蒙古自治区党委统战部副部长、自治区工商联党组书记等职。完整履历待查。"},

    # 栾天猛 - 赤峰市委副书记、市长 (current)
    {"id": 2, "person_id": 2, "org_id": 1, "title": "赤峰市委副书记",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": "2026年7月以市委副书记、市长身份公开活动。"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "赤峰市市长",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": "2026年7月调研老哈河沿线防汛备汛工作。此前曾任内蒙古自治区政府副秘书长等职。完整履历待查。"},

    # 睢利 - 赤峰市人大常委会主任
    {"id": 4, "person_id": 3, "org_id": 3, "title": "赤峰市人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": "2026年7月参加全市民族团结进步表彰大会。"},

    # 苏雅勒其其格 - 赤峰市政协主席
    {"id": 5, "person_id": 4, "org_id": 4, "title": "赤峰市政协主席",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": "2026年7月参加全市民族团结进步表彰大会。"},

    # 王生才 - 市委常委、统战部部长
    {"id": 6, "person_id": 5, "org_id": 1, "title": "赤峰市委常委",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
    {"id": 7, "person_id": 5, "org_id": 5, "title": "赤峰市委统战部部长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "2026年7月宣读表彰决定。"},

    # 王永军 - 赤峰市副市长
    {"id": 8, "person_id": 6, "org_id": 2, "title": "赤峰市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "2026年7月随唐毅赴北京招商、陪同调研防汛工作。"},

    # 付守利 - 赤峰市副市长
    {"id": 9, "person_id": 7, "org_id": 2, "title": "赤峰市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "2026年7月参加北京招商活动、陪同栾天猛调研防汛工作。"},

    # 万超岐 - 前任赤峰市委书记
    {"id": 10, "person_id": 8, "org_id": 1, "title": "赤峰市委书记",
     "start_date": "2021", "end_date": "2025", "rank": "正厅级",
     "note": "前任赤峰市委书记。2021年任赤峰市委书记，2025年卸任。"},
    {"id": 11, "person_id": 8, "org_id": 6, "title": "内蒙古自治区人大常委会代表工作委员会主任",
     "start_date": "2025", "end_date": "present", "rank": "正厅级",
     "note": "卸任赤峰市委书记后任现职。"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────

relationships = [
    # 唐毅 <-> 栾天猛 : 党政一把手
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "唐毅（市委书记）与栾天猛（市长）为赤峰市党政主要领导搭档",
        "overlap_org": "中国共产党赤峰市委员会",
        "overlap_period": "现任",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 唐毅 <-> 王生才 : 市委班子
    {
        "id": 2,
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "唐毅（市委书记）与王生才（市委常委、统战部部长）在赤峰市委班子中共事",
        "overlap_org": "中国共产党赤峰市委员会",
        "overlap_period": "现任",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 栾天猛 <-> 付守利 : 市长-副市长
    {
        "id": 3,
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "栾天猛（市长）与付守利（副市长）在赤峰市政府班子中共事",
        "overlap_org": "赤峰市人民政府",
        "overlap_period": "现任",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 栾天猛 <-> 王永军 : 市长-副市长
    {
        "id": 4,
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "栾天猛（市长）与王永军（副市长）在赤峰市政府班子中共事",
        "overlap_org": "赤峰市人民政府",
        "overlap_period": "现任",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 唐毅 <-> 睢利 : 市委-人大
    {
        "id": 5,
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "唐毅（市委书记）与睢利（市人大常委会主任）在赤峰市领导层共事",
        "overlap_org": "赤峰市",
        "overlap_period": "现任",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 唐毅 <-> 苏雅勒其其格 : 市委-政协
    {
        "id": 6,
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "唐毅（市委书记）与苏雅勒其其格（市政协主席）在赤峰市领导层共事",
        "overlap_org": "赤峰市",
        "overlap_period": "现任",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 唐毅 <-> 万超岐 : 前后任
    {
        "id": 7,
        "person_a": 1, "person_b": 8,
        "type": "predecessor_successor",
        "context": "唐毅接替万超岐担任赤峰市委书记",
        "overlap_org": "中国共产党赤峰市委员会",
        "overlap_period": "2025",
        "strength": "strong",
        "confidence": "plausible",
    },
    # 唐毅 <-> 王永军 : 市委-政府
    {
        "id": 8,
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "唐毅（市委书记）与王永军（副市长）共同赴北京招商、陪同调研防汛工作",
        "overlap_org": "赤峰市",
        "overlap_period": "2026年7月",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 王永军 <-> 付守利 : 副市长同僚
    {
        "id": 9,
        "person_a": 6, "person_b": 7,
        "type": "overlap",
        "context": "王永军与付守利同为赤峰市副市长",
        "overlap_org": "赤峰市人民政府",
        "overlap_period": "现任",
        "strength": "strong",
        "confidence": "confirmed",
    },
]


# ── BUILD ────────────────────────────────────────────────────────────

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
    print("Done. DB:", DB_PATH)
    print("GEXF:", GEXF_PATH)
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
