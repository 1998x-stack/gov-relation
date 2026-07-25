#!/usr/bin/env python3
"""Build 铁岭县 (Tieling County, Liaoning Province) personnel network database and graph."""

import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.abspath(os.path.join(BASE))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "铁岭县"
TASK_ID = "liaoning_铁岭县"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # === Core leaders (targets) ===
    {
        "id": 1,
        "name": "付尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党铁岭县委员会",
        "source": "https://www.tielingxian.gov.cn/tlx/xwzx/tlxxw/2026070708494779579/index.html",
    },
    {
        "id": 2,
        "name": "朱善植",
        "gender": "男",
        "ethnicity": "朝鲜族",
        "birth": "1985年8月",
        "birthplace": "",
        "education": "研究生学历，管理学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/xz/2022031922241534450/index.html",
    },
    # === 县委常委 ===
    {
        "id": 3,
        "name": "滕达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2025030708244779386/index.html",
    },
    {
        "id": 4,
        "name": "钟鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "education": "硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2025022411482388742/index.html",
    },
    # === 副县长（县政府领导班子） ===
    {
        "id": 5,
        "name": "李文涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁岭铁南经济开发区管委会主任",
        "current_org": "铁岭铁南经济开发区管委会",
        "source": "https://www.tielingxian.gov.cn/tlx/zwgk/zfwj/xzfbgswj/2026071313570170494/index.html",
    },
    {
        "id": 6,
        "name": "张宏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2026071314124848468/index.html",
    },
    {
        "id": 7,
        "name": "崔佳志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2023112810494963025/index.html",
    },
    {
        "id": 8,
        "name": "邓大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2024092609324396509/index.html",
    },
    {
        "id": 9,
        "name": "李文罡",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1975年6月",
        "birthplace": "",
        "education": "大学学历，法学学士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "铁岭县公安局",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2022031922241369056/index.html",
    },
    {
        "id": 10,
        "name": "刘军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2023042708425811118/index.html",
    },
    {
        "id": 11,
        "name": "龙朕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2022031922241382826/index.html",
    },
    {
        "id": 12,
        "name": "张睿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1995年11月",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2025030308424083354/index.html",
    },
    # === 其他重要人物 ===
    {
        "id": 13,
        "name": "银洪阁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "铁岭县人大常委会",
        "source": "https://www.tielingxian.gov.cn/tlx/xwzx/tlxxw/2026071309242227439/index.html",
    },
    # === 原任 ===
    {
        "id": 14,
        "name": "孙忠海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原副县长（已离任）",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/zwgk/zfwj/xzfbgswj/2026071313570170494/index.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党铁岭县委员会", "type": "党委", "level": "县", "parent": "中国共产党铁岭市委员会", "location": "辽宁省铁岭市铁岭县"},
    {"id": 2, "name": "铁岭县人民政府", "type": "政府", "level": "县", "parent": "铁岭市人民政府", "location": "辽宁省铁岭市铁岭县"},
    {"id": 3, "name": "铁岭县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "辽宁省铁岭市铁岭县"},
    {"id": 4, "name": "铁岭铁南经济开发区管委会", "type": "开发区", "level": "县", "parent": "铁岭县人民政府", "location": "辽宁省铁岭市铁岭县"},
    {"id": 5, "name": "铁岭县公安局", "type": "政府", "level": "县", "parent": "铁岭县人民政府", "location": "辽宁省铁岭市铁岭县"},
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    # 付尧
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 朱善植
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 滕达
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "县政府党组副书记"},
    # 钟鑫
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责国资改革、招商引资"},
    # 李文涛
    {"person_id": 5, "org_id": 4, "title": "管委会主任", "start": "", "end": "present", "rank": "副县级", "note": "负责工业、科技、民营经济"},
    # 张宏
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "2026-06", "end": "present", "rank": "副县级", "note": "接替孙忠海分工"},
    # 崔佳志
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责金融"},
    # 邓大伟
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责教育、自然资源、交通、文旅"},
    # 李文罡
    {"person_id": 9, "org_id": 5, "title": "县公安局局长", "start": "", "end": "present", "rank": "副县级", "note": "兼县公安局党委书记、督察长"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 刘军
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责生态环境、农业农村、水利"},
    # 龙朕
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责卫健、民政、退役军人、医保"},
    # 张睿
    {"person_id": 12, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "政府班子锻炼岗位"},
    # 银洪阁
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 孙忠海
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "2026-04", "rank": "副县级", "note": "已离任，张宏接替"},
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长", "overlap_org": "中国共产党铁岭县委员会", "overlap_period": "present"},
    # 书记-常委上下级
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—县委常委", "overlap_org": "中国共产党铁岭县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记—县委常委", "overlap_org": "中国共产党铁岭县委员会", "overlap_period": "present"},
    # 县长-副县长上下级
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—经开区主任", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长/公安局长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长—挂职副县长", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    # AB角互补关系
    {"person_a": 3, "person_b": 5, "type": "AB角互补", "context": "常务副县长与经开区主任互为AB角", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 6, "person_b": 11, "type": "AB角互补", "context": "张宏与龙朕互为AB角", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 4, "person_b": 12, "type": "AB角互补", "context": "钟鑫与张睿互为AB角", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 7, "person_b": 10, "type": "AB角互补", "context": "崔佳志与刘军互为AB角", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    {"person_a": 8, "person_b": 9, "type": "AB角互补", "context": "邓大伟与李文罡互为AB角", "overlap_org": "铁岭县人民政府", "overlap_period": "present"},
    # 前后任
    {"person_a": 6, "person_b": 14, "type": "前后任", "context": "张宏接替孙忠海副县长职位", "overlap_org": "铁岭县人民政府", "overlap_period": "2026"},
    # 人大常委会关系
    {"person_a": 13, "person_b": 1, "type": "党政搭档", "context": "人大常委会主任与县委书记", "overlap_org": "铁岭县", "overlap_period": "present"},
]

# ── Build ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    # Remove old db if exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    print(f"Building database: {DB_PATH}")
    print(f"Building GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Verify output
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # Check GEXF
    with open(GEXF_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  GEXF size: {len(content)} bytes")
    print(f"  GEXF has nodes: {'<nodes>' in content}")
    print(f"  GEXF has edges: {'<edges>' in content}")
    print("Build complete.")
