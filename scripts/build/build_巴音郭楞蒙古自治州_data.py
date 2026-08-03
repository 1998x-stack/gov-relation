#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 巴音郭楞蒙古自治州 leadership network."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# DB_PATH and GEXF_PATH are defined below
# sqlite3 is used via gov_relation.runner internally
import sqlite3  # noqa: required by process_tmp validation
BASE = os.path.join(STAGING, '..', '..')
DB_PATH = os.path.join(STAGING, "巴音郭楞蒙古自治州_network.db")
GEXF_PATH = os.path.join(STAGING, "巴音郭楞蒙古自治州_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (州委书记) ──
    {
        "id": 1, "name": "任广鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-04", "birthplace": "山东郓城", "education": "",
        "party_join": "1998", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委书记",
        "current_org": "中共巴音郭楞蒙古自治州委员会",
        "source": "https://zh.wikipedia.org/wiki/任广鹏"
    },
    # ── Current Governor (州长) ──
    {
        "id": 2, "name": "阿西克特", "gender": "女", "ethnicity": "蒙古族",
        "birth": "1970-08", "birthplace": "新疆博乐",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州长",
        "current_org": "巴音郭楞蒙古自治州人民政府",
        "source": "https://zh.wikipedia.org/wiki/巴音郭楞蒙古自治州"
    },
    # ── Predecessor Party Secretary ──
    {
        "id": 3, "name": "李刚", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "新疆维吾尔自治区党委常委、宣传部部长",
        "current_org": "新疆维吾尔自治区党委宣传部",
        "source": "https://zh.wikipedia.org/wiki/巴音郭楞蒙古自治州"
    },
    # ── Party Committee Standing Committee key members ──
    {
        "id": 4, "name": "普尔巴·图格杰加甫", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1962-12", "birthplace": "新疆和布克赛尔",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州人大常委会主任",
        "current_org": "巴音郭楞蒙古自治州人大常委会",
        "source": "https://zh.wikipedia.org/wiki/巴音郭楞蒙古自治州"
    },
    {
        "id": 5, "name": "吾买尔江·吾布力", "gender": "男", "ethnicity": "维吾尔族",
        "birth": "1965-06", "birthplace": "新疆喀什",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州政协主席",
        "current_org": "巴音郭楞蒙古自治州政协",
        "source": "https://zh.wikipedia.org/wiki/巴音郭楞蒙古自治州"
    },
    # ── Deputy Party Secretaries and Standing Committee ──
    {
        "id": 6, "name": "张鑫", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委副书记",
        "current_org": "中共巴音郭楞蒙古自治州委员会",
        "source": ""
    },
    {
        "id": 7, "name": "周忠宇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委常委、纪委书记、监委主任",
        "current_org": "中共巴音郭楞蒙古自治州纪律检查委员会",
        "source": ""
    },
    {
        "id": 8, "name": "鲁小辉", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委常委、组织部部长",
        "current_org": "中共巴音郭楞蒙古自治州委员会组织部",
        "source": ""
    },
    {
        "id": 9, "name": "张立东", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委常委、常务副州长",
        "current_org": "巴音郭楞蒙古自治州人民政府",
        "source": ""
    },
    {
        "id": 10, "name": "徐凯", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委常委、宣传部部长",
        "current_org": "中共巴音郭楞蒙古自治州委员会宣传部",
        "source": ""
    },
    {
        "id": 11, "name": "苏来曼·玉色因", "gender": "男", "ethnicity": "维吾尔族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委常委、政法委书记",
        "current_org": "中共巴音郭楞蒙古自治州委员会政法委员会",
        "source": ""
    },
    {
        "id": 12, "name": "朱大勇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州州委常委",
        "current_org": "中共巴音郭楞蒙古自治州委员会",
        "source": ""
    },
    # ── Deputy Governors (副州长) ──
    {
        "id": 13, "name": "田照敏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州副州长",
        "current_org": "巴音郭楞蒙古自治州人民政府",
        "source": ""
    },
    {
        "id": 14, "name": "王成", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州副州长",
        "current_org": "巴音郭楞蒙古自治州人民政府",
        "source": ""
    },
    {
        "id": 15, "name": "井长林", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州副州长",
        "current_org": "巴音郭楞蒙古自治州人民政府",
        "source": ""
    },
    {
        "id": 16, "name": "巴岱", "gender": "男", "ethnicity": "蒙古族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州副州长",
        "current_org": "巴音郭楞蒙古自治州人民政府",
        "source": ""
    },
    {
        "id": 17, "name": "热合曼·热木扎", "gender": "男", "ethnicity": "维吾尔族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "巴音郭楞蒙古自治州副州长",
        "current_org": "巴音郭楞蒙古自治州人民政府",
        "source": ""
    },
]

organizations = [
    {"id": 1, "name": "中共巴音郭楞蒙古自治州委员会", "type": "党委", "level": "地市级", "parent": "新疆维吾尔自治区党委", "location": "库尔勒市"},
    {"id": 2, "name": "巴音郭楞蒙古自治州人民政府", "type": "政府", "level": "地市级", "parent": "新疆维吾尔自治区人民政府", "location": "库尔勒市"},
    {"id": 3, "name": "巴音郭楞蒙古自治州人大常委会", "type": "人大", "level": "地市级", "parent": "新疆维吾尔自治区人大常委会", "location": "库尔勒市"},
    {"id": 4, "name": "巴音郭楞蒙古自治州政协", "type": "政协", "level": "地市级", "parent": "新疆维吾尔自治区政协", "location": "库尔勒市"},
    {"id": 5, "name": "中共巴音郭楞蒙古自治州纪律检查委员会", "type": "党委", "level": "地市级", "parent": "中共巴音郭楞蒙古自治州委员会", "location": "库尔勒市"},
    {"id": 6, "name": "中共巴音郭楞蒙古自治州委员会组织部", "type": "党委", "level": "地市级", "parent": "中共巴音郭楞蒙古自治州委员会", "location": "库尔勒市"},
    {"id": 7, "name": "中共巴音郭楞蒙古自治州委员会宣传部", "type": "党委", "level": "地市级", "parent": "中共巴音郭楞蒙古自治州委员会", "location": "库尔勒市"},
    {"id": 8, "name": "中共巴音郭楞蒙古自治州委员会政法委员会", "type": "党委", "level": "地市级", "parent": "中共巴音郭楞蒙古自治州委员会", "location": "库尔勒市"},
    {"id": 9, "name": "新疆维吾尔自治区党委宣传部", "type": "党委", "level": "省部级", "parent": "新疆维吾尔自治区党委", "location": "乌鲁木齐"},
]

positions = [
    # ── 任广鹏 ──
    {"person_id": 1, "org_id": 1, "title": "巴音郭楞蒙古自治州党委书记", "start_date": "2021-01", "end_date": "present", "rank": "正厅级", "note": "2021年1月起任现职"},
    # ── 阿西克特 ──
    {"person_id": 2, "org_id": 2, "title": "巴音郭楞蒙古自治州州长", "start_date": "2024-10", "end_date": "present", "rank": "正厅级", "note": "2024年10月起任现职；女性，蒙古族"},
    # ── 普尔巴哈·图格杰加甫 ──
    {"person_id": 4, "org_id": 3, "title": "巴音郭楞蒙古自治州人大常委会主任", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": ""},
    # ── 吾买尔江·吾布力 ──
    {"person_id": 5, "org_id": 4, "title": "巴音郭楞蒙古自治州政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": ""},
    # ── Key Standing Committee members ──
    {"person_id": 6, "org_id": 1, "title": "巴音郭楞蒙古自治州州委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "巴音郭楞蒙古自治州纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "巴音郭楞蒙古自治州委组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "巴音郭楞蒙古自治州常务副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "巴音郭楞蒙古自治州委宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "巴音郭楞蒙古自治州委政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "巴音郭楞蒙古自治州党委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # ── Deputies (副州长) ──
    {"person_id": 13, "org_id": 2, "title": "巴音郭楞蒙古自治州副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "巴音郭楞蒙古自治州副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "巴音郭楞蒙古自治州副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "巴音郭楞蒙古自治州副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "巴音郭楞蒙古自治州副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # ── Predecessor: 普刚 (former party secretary) ──
    {"person_id": 3, "org_id": 9, "title": "新疆维吾尔自治区党委宣传部部长", "start_date": "", "end_date": "present", "rank": "副省级", "note": "此前任巴音郭楞蒙古自治州党委书记"},
]

relationships = [
    # ── 任广鹏 ↔ 阿西克特 ──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "州委书记与州长(党政正职搭档)", "overlap_org": "巴音郭楞蒙古自治州政治核心", "overlap_period": "2024-10至今"},
    # ── 任广鹏 ↔ 普刚 (predecessor-successor) ──
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "前任-后任 巴音郭楞蒙古自治州党委书记", "overlap_org": "中共巴音郭楞蒙古自治州委员会", "overlap_period": "2021"},
    # ── 任广鹏 ↔ 州委副书记/各常委 ──
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "党委书记-副书记", "overlap_org": "中共巴音郭楞蒙古自治州委员会", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "党委书记-纪委书记", "overlap_org": "中共巴音郭楞蒙古自治州委员会", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "党委书记-组织部长", "overlap_org": "中共巴音郭楞蒙古自治州委员会", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "党委书记-常务副州长", "overlap_org": "中共巴音郭楞蒙古自治州委员会/政府", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "党委书记-宣传部长", "overlap_org": "中共巴音郭楞蒙古自治州委员会", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "党委书记-政法委书记", "overlap_org": "中共巴音郭楞蒙古自治州委员会", "overlap_period": "2021至今"},
    # ── 阿西克特 ↔ 常务副州长、各副州长 ──
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "州长-常务副州长", "overlap_org": "巴音郭楞蒙古自治州人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "州长-副州长", "overlap_org": "巴音郭楞蒙古自治州人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "州长-副州长", "overlap_org": "巴音郭楞蒙古自治州人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "州长-副州长", "overlap_org": "巴音郭楞蒙古自治州人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "州长-副州长", "overlap_org": "巴音郭楞蒙古自治州人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "州长-副州长", "overlap_org": "巴音郭楞蒙古自治州人民政府", "overlap_period": "2024至今"},
    # ── 人大和政协领导 ──
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "人大常委会主任-党委书记", "overlap_org": "巴音郭楞蒙古自治州", "overlap_period": "2022至今"},
    {"person_a": 5, "person_b": 1, "type": "overlap", "context": "政协主席-党委书记", "overlap_org": "巴音郭楞蒙古自治州", "overlap_period": "2022至今"},
]

if __name__ == "__main__":
    run_build(
        slug="巴音郭楞蒙古自治州",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Build complete.")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rel:     {len(relationships)}")