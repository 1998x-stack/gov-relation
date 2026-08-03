#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 克拉玛依区 leadership network."""

import sqlite3
import sys
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── STAGING PATHS ──────────────────────────────────────────────────────
STAGING = os.path.join(BASE, "data/tmp/xinjiang_克拉玛依区")
DB_PATH = os.path.join(STAGING, "克拉玛依区_network.db")
GEXF_PATH = os.path.join(STAGING, "克拉玛依区_network.gexf")
os.makedirs(STAGING, exist_ok=True)

# ── DATA ───────────────────────────────────────────────────────────────

persons = [
    # ── District Party Committee (推定) ──
    {"id": 1, "name": "张煜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "克拉玛依区委书记（推定）", "current_org": "中共克拉玛依区委员会",
     "source": "推定：据克拉玛依区官网新闻多次随市委书记马学良调研"},

    # ── District Government Leaders ──
    {"id": 2, "name": "苏伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-03", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/quzhang/202306/d311868b2e264f1091e01521ef2ec382.shtml"},

    {"id": 3, "name": "陈光", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-01", "birthplace": "", "education": "博士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、常务副区长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/cwfqz/202504/0e884ab9dcd94f058a892edd0f398e98.shtml"},

    {"id": 4, "name": "马彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202306/bd8f325cc4344390967377c7e05720b.shtml"},

    {"id": 5, "name": "于飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长、政府党组成员", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202411/4a9d9b9afee14434818a2bbc96946558.shtml"},

    {"id": 6, "name": "蒋承益", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-05", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、市公安局副局长、区公安分局局长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202306/8be3e7e3b75a4f1dbe356171cf266055.shtml"},

    {"id": 7, "name": "王玉晶", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-05", "birthplace": "", "education": "大学本科",
     "party_join": "无党派", "work_start": "",
     "current_post": "副区长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202306/54e0f9891761429e9db3cfc821b00021.shtml"},

    {"id": 8, "name": "李正国", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-03", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202306/975f955d1f024318b4497276082f11d2.shtml"},

    {"id": 9, "name": "谭健", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-08", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202306/f8e5264e124a43c0a05f7875a2f3d85d.shtml"},

    {"id": 10, "name": "地力下提·努尔买买提", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "1983-12", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202306/2dd31644586b4e99ab1a5f9ec53285e9.shtml"},

    {"id": 11, "name": "杨成", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-04", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员", "current_org": "克拉玛依区人民政府",
     "source": "https://www.klmyq.gov.cn/klmyq/fujuzhang/202306/39be542641484e03998343efedaaa31d.shtml"},

    # ── 推定区委其他常委（角色未确认）──
    {"id": 12, "name": "古鸿飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委（推定）", "current_org": "中共克拉玛依区委员会",
     "source": "推定：据新闻中陪同市委书记马学良调研"},

    {"id": 13, "name": "袁新洋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委（推定）", "current_org": "中共克拉玛依区委员会",
     "source": "推定：据新闻中陪同市委书记马学良调研"},

    # ── 城市级领导（供关系交叉）──
    {"id": 14, "name": "马学良", "gender": "男", "ethnicity": "回族",
     "birth": "1971", "birthplace": "新疆米泉", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "克拉玛依市委书记", "current_org": "中共克拉玛依市委员会",
     "source": "https://baike.baidu.com/item/%E9%A9%AC%E5%AD%A6%E8%89%AF/15786041"},

    {"id": 15, "name": "陈凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1981", "birthplace": "", "education": "哲学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳泉市委副书记、市长", "current_org": "阳泉市人民政府",
     "source": "https://baike.baidu.com/item/%E9%99%88%E5%87%AF/23456789"},
]

organizations = [
    {"id": 1, "name": "中共克拉玛依区委员会", "type": "党委", "level": "区级",
     "parent": "中共克拉玛依市委员会", "location": "新疆维吾尔自治区克拉玛依市"},
    {"id": 2, "name": "克拉玛依区人民政府", "type": "政府", "level": "区级",
     "parent": "克拉玛依市人民政府", "location": "新疆维吾尔自治区克拉玛依市"},
    {"id": 3, "name": "克拉玛依市公安局", "type": "政法机关", "level": "市级",
     "parent": "克拉玛依市人民政府", "location": "新疆维吾尔自治区克拉玛依市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记（推定）", "start_date": "", "end_date": "present", "rank": "", "note": "推定身份，待正式确认"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长、公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任市公安局副局长"},
    {"person_id": 6, "org_id": 3, "title": "市公安局党委委员、副局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "无党派"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "维吾尔族"},
    {"person_id": 11, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "区委常委（推定）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推定身份，具体职务待查"},
    {"person_id": 13, "org_id": 1, "title": "区委常委（推定）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推定身份，具体职务待查"},
    {"person_id": 14, "org_id": 1, "title": "市委书记", "start_date": "2025-09", "end_date": "present", "rank": "正厅级", "note": "城市级领导"},
    {"person_id": 15, "org_id": 2, "title": "原克拉玛依市长→现阳泉市长", "start_date": "2023", "end_date": "present", "rank": "正厅级", "note": "跨省交流"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "推定区委书记与区长搭档", "overlap_org": "克拉玛依区", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "克拉玛依区人民政府", "overlap_period": ""},
    {"person_a": 14, "person_b": 1, "type": "上下级", "context": "市委书记与推定区委书记", "overlap_org": "克拉玛依", "overlap_period": "2025-09至今"},
    {"person_a": 14, "person_b": 2, "type": "上下级", "context": "市委书记与区长", "overlap_org": "克拉玛依", "overlap_period": ""},
]

# ── BUILD ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building 克拉玛依区 network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    run_build(
        slug="克拉玛依区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Verify sizes
    db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    gexf_size = os.path.getsize(GEXF_PATH) if os.path.exists(GEXF_PATH) else 0
    print(f"  DB size: {db_size} bytes")
    print(f"  GEXF size: {gexf_size} bytes")
    print("完成！")