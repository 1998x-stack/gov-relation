#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Hengzhou (横州市) leadership network.

横州市 is a county-level city under Nanning City, Guangxi Zhuang Autonomous Region.
Formerly Heng County (横县), upgraded to county-level city on 2021-02-03.
"""

import sys, os, sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from datetime import datetime

# Token markers for process_tmp.py validation
DB_PATH = "横州市_network.db"
GEXF_PATH = "横州市_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretaries (市委书记) ──
    {
        "id": 1,
        "name": "梁枫",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市委书记",
        "current_org": "中共横州市委员会",
        "source": "https://www.gxhx.gov.cn/yw/hzsyw/2026nhzsyw/t6685998.html",
    },
    {
        "id": 2,
        "name": "黄海韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任横州市委书记",
        "current_org": "中共横州市委员会（前任）",
        "source": "https://www.gxhx.gov.cn/",
    },

    # ── Current and Recent Mayors (市长) ──
    {
        "id": 3,
        "name": "廖知启",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市委副书记、市长",
        "current_org": "横州市人民政府",
        "source": "https://www.gxhx.gov.cn/xxgk/xxgkml/jcxxgk/ldzc/sz/",
    },

    # ── Deputy Mayors / Standing Committee Members ──
    {
        "id": 4,
        "name": "王治",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市领导",
        "current_org": "中共横州市委员会",
        "source": "https://www.gxhx.gov.cn/yw/ldhd/t6449315.html",
    },
    {
        "id": 5,
        "name": "农烈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市委常委、副市长",
        "current_org": "横州市人民政府",
        "source": "https://www.gxhx.gov.cn/xxgk/xxgkml/jcxxgk/ldzc/fsz/t5902236.html",
    },
    {
        "id": 6,
        "name": "肖彩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市委常委、统战部部长、副市长",
        "current_org": "中共横州市委员会",
        "source": "https://www.gxhx.gov.cn/xxgk/xxgkml/jcxxgk/ldzc/fsz/t6605848.html",
    },
    {
        "id": 7,
        "name": "姚剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市副市长、公安局局长",
        "current_org": "横州市人民政府",
        "source": "https://www.gxhx.gov.cn/xxgk/xxgkml/jcxxgk/ldzc/fsz/t4890748.html",
    },
    {
        "id": 8,
        "name": "蒙柯宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市副市长",
        "current_org": "横州市人民政府",
        "source": "https://www.gxhx.gov.cn/xxgk/xxgkml/jcxxgk/ldzc/fsz/t4890711.html",
    },
    {
        "id": 9,
        "name": "周念远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市副市长",
        "current_org": "横州市人民政府",
        "source": "https://www.gxhx.gov.cn/xxgk/xxgkml/jcxxgk/ldzc/fsz/t4890756.html",
    },
    {
        "id": 10,
        "name": "黄曦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市副市长",
        "current_org": "横州市人民政府",
        "source": "https://www.gxhx.gov.cn/xxgk/xxgkml/jcxxgk/ldzc/fsz/t4890740.html",
    },
    {
        "id": 11,
        "name": "宁华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "横州市领导",
        "current_org": "横州市人民政府",
        "source": "https://www.gxhx.gov.cn/yw/ldhd/t6449315.html",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共横州市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共南宁市委员会",
        "location": "广西南宁市横州市",
    },
    {
        "id": 2,
        "name": "横州市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "南宁市人民政府",
        "location": "广西南宁市横州市",
    },
    {
        "id": 3,
        "name": "横州市公安局",
        "type": "政府",
        "level": "科级",
        "parent": "横州市人民政府",
        "location": "广西南宁市横州市",
    },
    {
        "id": 4,
        "name": "横州市委统战部",
        "type": "党委",
        "level": "科级",
        "parent": "中共横州市委员会",
        "location": "广西南宁市横州市",
    },
    {
        "id": 5,
        "name": "横州市人大常委会",
        "type": "人大",
        "level": "县级市",
        "parent": "南宁市人大常委会",
        "location": "广西南宁市横州市",
    },
    {
        "id": 6,
        "name": "横州市政协",
        "type": "政协",
        "level": "县级市",
        "parent": "南宁市政协",
        "location": "广西南宁市横州市",
    },
    {
        "id": 7,
        "name": "南宁六景工业园区",
        "type": "开发区",
        "level": "省级开发区",
        "parent": "南宁市人民政府",
        "location": "广西南宁市横州市六景镇",
    },
    {
        "id": 8,
        "name": "横州市纪委监委",
        "type": "党委",
        "level": "县级市",
        "parent": "中共横州市委员会",
        "location": "广西南宁市横州市",
    },
]

positions = [
    # ── 梁枫 ──
    {"person_id": 1, "org_id": 1, "title": "横州市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任市委书记（截至2026年7月）"},
    # ── 黄海韬 (predecessor) ──
    {"person_id": 2, "org_id": 1, "title": "横州市委书记（原横县县委书记）", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任横州市委书记"},
    # ── 廖知启 ──
    {"person_id": 3, "org_id": 2, "title": "横州市人民政府市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "横州市委副书记、市长、南宁六景工业园区管委会主任"},
    {"person_id": 3, "org_id": 7, "title": "南宁六景工业园区管委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼任"},
    # ── 农烈 ──
    {"person_id": 5, "org_id": 2, "title": "横州市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "常务副市长"},
    # ── 肖彩 ──
    {"person_id": 6, "org_id": 4, "title": "横州市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼副市长、六景镇党委书记"},
    {"person_id": 6, "org_id": 2, "title": "横州市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任"},
    # ── 姚剑 ──
    {"person_id": 7, "org_id": 3, "title": "横州市公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼副市长"},
    {"person_id": 7, "org_id": 2, "title": "横州市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任"},
    # ── 蒙柯宇 ──
    {"person_id": 8, "org_id": 2, "title": "横州市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管农业农村、水利、文化等"},
    # ── 周念远 ──
    {"person_id": 9, "org_id": 2, "title": "横州市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # ── 黄曦 ──
    {"person_id": 10, "org_id": 2, "title": "横州市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

relationships = [
    # ── Core leader relationships ──
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "市委书记—市长搭档",
        "overlap_org": "中共横州市委员会/横州市人民政府",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "梁枫接替黄海韬任横州市委书记",
        "overlap_org": "中共横州市委员会",
        "overlap_period": "",
    },
    {
        "person_a": 5,
        "person_b": 3,
        "type": "overlap",
        "context": "副市长协助市长工作，常务副市长",
        "overlap_org": "横州市人民政府",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 5,
        "person_b": 1,
        "type": "overlap",
        "context": "市委常委—书记",
        "overlap_org": "中共横州市委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 6,
        "person_b": 1,
        "type": "overlap",
        "context": "市委常委—书记",
        "overlap_org": "中共横州市委员会",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 7,
        "person_b": 3,
        "type": "overlap",
        "context": "副市长（公安）—市长",
        "overlap_org": "横州市人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 8,
        "person_b": 3,
        "type": "overlap",
        "context": "副市长—市长",
        "overlap_org": "横州市人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 9,
        "person_b": 3,
        "type": "overlap",
        "context": "副市长—市长",
        "overlap_org": "横州市人民政府",
        "overlap_period": "",
    },
]

# ── BUILD ────────────────────────────────────────────────────────────

STAGING = os.path.join(os.path.dirname(__file__))

if __name__ == "__main__":
    run_build(
        slug="横州市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=os.path.join(STAGING, "横州市_network.db"),
        gexf_path=os.path.join(STAGING, "横州市_network.gexf"),
        overwrite=True,
    )
    print("Done.")
