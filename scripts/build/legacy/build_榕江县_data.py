#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
榕江县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Region: 榕江县
Task: guizhou_榕江县
Targets: 县委书记 & 县长

当前在任 (as of 2026-08-05, 依据 rongjiang.gov.cn 官方网站确认):
- 县委书记: 徐勃 (confirmed; 主持村超推动, 2026年7-8月县委常委会主持)
- 县委副书记、县长: 王飞 (confirmed; 县政府全面工作, 分管财政/审计/粮食/人事)
- 县委副书记、县委政法委书记、贵州榕江经济开发区党工委书记: 黄博
- 县委副书记: 杨保军
- 县人大常委会主任: 龙见强
- 县政协主席: 潘建波
- 县政府常务副县长: 张平
- 县政府副县长: 银政、彭晖、吴永红、康其军、黄国锋、付文娟、吴超
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "guizhou_榕江县"
SLUG = "榕江县"
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

# =========================================================================
# 1. SOURCE REGISTER
# =========================================================================
source_register = [
    {"id": "S001", "title": "榕江县人民政府门户网站 —— 政务公开/领导之窗（县政府领导分工）",
     "url": "https://www.rongjiang.gov.cn/zwgk_5903530/",
     "publisher": "榕江县人民政府", "published_at": "2026-08", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认县长王飞（分管财政/审计/粮食/人事）、常务副县长张平、副县长银政/彭晖/吴永红/严其军/何耀/黄国锋/付文璆/吴超等"},
    {"id": "S002", "title": "榕江县人民政府门户网站 —— 县委常委会召开会议 徐勃主持并讲话（2026-07-31）",
     "url": "https://www.rongjiang.gov.cn/xwzx_5903512/rjyw_5903513/202607/t20260731_90682143.html",
     "publisher": "榕江县人民政府", "published_at": "2026-07-31", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "十三届县委常委会第237次会议：县委书记徐勃主持；县委副书记、县长王飞；县政协主席潘建波；县委副书记、县委政法委书记、贵州榕江经济开发区党工委书记黄博；县委副书记杨保军",
     },
    {"id": "S003", "title": "榕江县人民政府门户网站 —— 走访慰问寄深情 四大班子主要领导（2026-08-03）",
     "url": "https://www.rongjiang.gov.cn/xwzx_5902/rjyw_5903513/202608/t20260803_90688713.html",
     "publisher": "榕江县人民政府", "published_at": "2026-08-03", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "县委书记徐勃、县委副书记/县长王飞、县人大常委会主任龙见强、县政协主席潘建波开展八一建军节走访慰问"},
    {"id": "S004", "title": "榕江县人民政府门户网站 —— 杨光杰到榕江县调研（2026-08-04）",
     "url": "https://www.rongjiang.gov.cn/xwzx_5902/rjyw_5903513/202608/t20260804_90691853.html",
     "publisher": "黔东南州/榕江县", "published_at": "2026-08-04", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "黔东南州委副书记、州长杨光杰赴榕江市调研村超与项目建设；州政府秘书长舒健陪同"},
    {"id": "S005", "title": "榕江县人民政府门户网站 —— 王飞到乡镇调研（2026-07-29）",
     "url": "https://www.rongjiang.gov.cn/xwzx_5902/rjyw_5903513/202607/t20260729_90670483.html",
     "publisher": "榕江县人民政府", "published_at": "2026-07-28", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "县委副书记、县长王飞调研防溺水、特色产业等"},
    {"id": "S006", "title": "榕江县人民政府门户网站 —— 贵州纺织集团赴榕江县调研（2026-07-27）",
     "url": "https://www.rongjiang.gov.cn/xwzx_5902/rjyw_5903513/202607/t20260727_90661758.html",
     "publisher": "榕江县人民政府", "published_at": "2026-07-27", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "县委书记徐勃主持；县政协主席潘建波、县委副书记/政法委书记/经开区党工委书记黄博参加"},
    {"id": "S007", "title": "榕江县人民政府门户网站 —— 县情简介/走进榕江",
     "url": "https://www.rongjiang.gov.cn/zjrj_5903491/",
     "publisher": "榕江县人民政府", "published_at": "2026", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "榕江旧称古州，位于湘黔桂三省结合部；2020年底整县脱贫摘帽，现为国家乡村振兴重点帮扶县"},
    {"id": "S008", "title": "榕江县人民政府门户网站 —— 政府领导之窗（县政府领导任职分工/个人简历）",
     "url": "https://www.rongjiang.gov.cn/zwgk_5903530/ldzc_5903531/",
     "publisher": "榕江县人民政府", "published_at": "2026", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "县政府领导任期简历：王飞（1987-04，汉族，大学）；张平（1984-10，苗族，大学）；银政（1977-02，水族，大学）；彭晖（1976-11，汉族，研究生，挂职）；吴永红（1973-01，汉族，研究生，挂职）；康其军（1979-10，苗族，大学）；黄国锋（1978-11，侗族）；付文娟（1987-05，土族，本科）；吴超（1989-02，苗族，本科，公安局长）"},
]

# =========================================================================
# 2. PERSONS
# =========================================================================
persons = [
    # ── 核心领导：县委书记 ──
    {"id": 1, "name": "徐勃", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共榕江县委书记", "current_org": "中共榕江县委员会",
     "source": "S002"},

    # ── 核心领导：县长 ──
    {"id": 2, "name": "王飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-04", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县委副书记、县长", "current_org": "榕江县人民政府",
     "source": "S001"},

    # ── 县委班子 ──
    {"id": 3, "name": "黄博", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县委副书记、县委政法委书记、贵州榕江经济开发区党工委书记", "current_org": "中共榕江县委员会",
     "source": "S002"},
    {"id": 4, "name": "杨保军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县委副书记", "current_org": "中共榕江县委员会",
     "source": "S002"},

    # ── 县人大 / 县政协 ──
    {"id": 5, "name": "龙见强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人大常委会主任", "current_org": "榕江县人民代表大会常务委员会",
     "source": "S003"},
    {"id": 6, "name": "潘建波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县政协主席", "current_org": "中国人民政治协商会议榕江县委员会",
     "source": "S003"},

    # ── 县政府班子 ──
    {"id": 7, "name": "张平", "gender": "男", "ethnicity": "苗族",
     "birth": "1984-10", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人民政府常务副县长（县委常委）", "current_org": "榕江县人民政府",
     "source": "S001"},
    {"id": 8, "name": "银政", "gender": "男", "ethnicity": "水族",
     "birth": "1977-02", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人民政府副县长（县委常委）", "current_org": "榕江县人民政府",
     "source": "S001"},
    {"id": 9, "name": "彭晖", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人民政府副县长（县委常委、挂职）", "current_org": "榕江县人民政府",
     "source": "S001"},
    {"id": 10, "name": "吴永红", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人民政府副县长（县委常委、挂职）", "current_org": "榕江县人民政府",
     "source": "S001"},
    {"id": 11, "name": "康其军", "gender": "男", "ethnicity": "苗族",
     "birth": "1979-10", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人民政府副县长", "current_org": "榕江县人民政府",
     "source": "S001"},
    {"id": 12, "name": "黄国锋", "gender": "男", "ethnicity": "侗族",
     "birth": "1978-11", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "榕江县人民政府副县长", "current_org": "榕江县人民政府",
     "source": "S001"},
    {"id": 13, "name": "付文娟", "gender": "女", "ethnicity": "土族",
     "birth": "1987-05", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人民政府副县长", "current_org": "榕江县人民政府",
     "source": "S001"},
    {"id": 14, "name": "吴超", "gender": "男", "ethnicity": "苗族",
     "birth": "1989-02", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榕江县人民政府副县长、县公安局局长", "current_org": "榕江县人民政府",
     "source": "S001"},
]

# =========================================================================
# 3. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共榕江县委员会", "type": "党委", "level": "县处级",
     "parent": "中共黔东南苗族侗族自治州委员会", "location": "贵州省黔东南州榕江县"},
    {"id": 2, "name": "榕江县人民政府", "type": "政府", "level": "县处级",
     "parent": "黔东南苗族侗族自治州人民政府", "location": "贵州省黔东南州榕江县"},
    {"id": 3, "name": "榕江县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "黔东南苗族侗族自治州人民代表大会常务委员会", "location": "贵州省黔东南州榕江县"},
    {"id": 4, "name": "中国人民政治协商会议榕江县委员会", "type": "政协", "level": "县处级",
     "parent": "", "location": "贵州省黔东南州榕江县"},
    {"id": 5, "name": "中共榕江县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共黔东南苗族侗族自治州纪律检查委员会", "location": "贵州省黔东南州榕江县"},
    {"id": 6, "name": "中共榕江县委员会政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共黔东南苗族侗族自治州委员会政法委员会", "location": "贵州省黔东南州榕江县"},
    {"id": 7, "name": "贵州榕江经济开发区管理委员会", "type": "开发区", "level": "县处级",
     "parent": "榕江县人民政府", "location": "贵州省黔东南州榕江县"},
]

# =========================================================================
# 4. POSITIONS
# =========================================================================
positions = [
    # ── 徐勃 ──
    {"person_id": 1, "org_id": 1, "title": "中共榕江县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任，2026年确认；主持县委常委会，推动村超"}, 
    # ── 王飞 ──
    {"person_id": 2, "org_id": 1, "title": "榕江县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "榕江县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任，领导县政府全面工作，分管财政/审计/粮食/人事"},
    # ── 黄博 ──
    {"person_id": 3, "org_id": 1, "title": "榕江县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 3, "org_id": 6, "title": "榕江县委政法委书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 3, "org_id": 7, "title": "贵州榕江经济开发区党工委书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── 杨保军 ──
    {"person_id": 4, "org_id": 1, "title": "榕江县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── 龙见强 ──
    {"person_id": 5, "org_id": 3, "title": "榕江县人大常委会主任",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # ── 潘建波 ──
    {"person_id": 6, "org_id": 4, "title": "榕江县政协主席",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # ── 张平 ──
    {"person_id": 7, "org_id": 2, "title": "榕江县人民政府常务副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── 县政府副县长 ──
    {"person_id": 8, "org_id": 2, "title": "榕江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 2, "title": "榕江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 10, "org_id": 2, "title": "榕江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 11, "org_id": 2, "title": "榕江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 12, "org_id": 2, "title": "榕江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 13, "org_id": 2, "title": "榕江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 14, "org_id": 2, "title": "榕江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
]

# =========================================================================
# 5. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政主要领导 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "徐勃（县委书记）与王飞（县委副书记、县长）构成书记-县长搭档",
     "overlap_org": "中共榕江县委员会 / 榕江县人民政府", "overlap_period": ""},

    # ── 县委书记与县委副书记 ──
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "徐勃与县委副书记、政法委书记、经开区党工委书记黄博在县委班子共事",
     "overlap_org": "中共榕江县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "徐勃与县委副书记杨保军在县委班子共事",
     "overlap_org": "中共榕江县委员会", "overlap_period": ""},

    # ── 县长与政府班子 ──
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "王飞（县长）与常务副县长张平在县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "王飞（县长）与副县长银政局县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "王飞（县长）与副县长彭晖在县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "王飞（县长）与副县长吴永红在县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "王飞（县长）与副县长康其军在县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "王飞（县长）与副县长黄国锋在县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "王飞（县长）与副县长付文娟在县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "王飞（县长）与副县长吴超在县政府班子共事",
     "overlap_org": "榕江县人民政府", "overlap_period": ""},

    # ── 县委副书记 / 人大 / 政协 交叉 ──
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "黄博（县委副书记）与张平（常务副县长）在县领导层面共事",
     "overlap_org": "榕江县", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "王飞（县长）与龙见强（人大常委会主任）同属县级领导层，八一慰问同台",
     "overlap_org": "榕江县", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "王飞（县长）与潘建波（政协主席）同属县级领导层，八一慰问同台",
     "overlap_org": "榕江县", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "徐勃（县委书记）与龙见强（人大常委会主任）同属县级领导层，八一慰问同台",
     "overlap_org": "榕江县", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "徐勃（县委书记）与潘建波（政协主席）同属县级领导层，八一慰问同台",
     "overlap_org": "榕江县", "overlap_period": ""},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"rongjiang_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>榕江县领导班子关系网络（基于榕江县人民政府门户网站）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "贵州省",
                "city": "黔东南苗族侗族自治州",
                "region": "榕江县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年8月"
            },
            "identity": {
                "person_id": f"rongjiang_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "人大" not in p.get("current_post", "") and "政协" not in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": (["S002", "S003"] if p["id"] == 1
                               else (["S001"] if p["id"] == 2
                                     else (["S008"] if p["id"] >= 7 else ["S002"])))
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": ""
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历（出生、籍贯、教育背景、任职路径）",
                 "why_it_matters": "无法追溯其任职路径和系统经历，影响对晋升与关系网络的分析",
                 "suggested_queries": [f"{p['name']} 简历 榕江"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 徐勃 Person JSON ──
    xb_timeline = [
        {"start": "", "end": "present", "org": "中共榕江县委员会", "title": "中共榕江县委书记",
         "notes": "现任，2026年主持县委常委会、推动贵州村超；作为县委书记围绕'村超'品牌及乡村振兴开展工作",
         "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "徐勃任榕江县委书记之前的详细履历未在本次调查中找到（出生年月、籍贯、教育背景、早期任职等信息缺失；其为'村超'主要推手的公开形象已知，但任职路径待查）",
         "confidence": "unverified", "source_ids": []},
    ]
    xb_relationships = [
        {"person": "王飞", "person_id": "rongjiang_王飞", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "徐勃（县委书记）与王飞（县委副书记、县长）构成书记-县长搭档",
         "overlap_org": "中共榕江县委员会 / 榕江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "黄博", "person_id": "rongjiang_黄博", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "徐勃与县委副书记、政法委书记、经开区党工委书记黄博在县委班子共事",
         "overlap_org": "中共榕江县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]

    xb_json = make_person_json(persons[0], xb_timeline, xb_relationships)
    xb_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔东南苗族侗族自治州-县委书记-徐勃.json")
    with open(xb_path, "w", encoding="utf-8") as f:
        json.dump(xb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {xb_path}")

    # ── 王飞 Person JSON ──
    wf_timeline = [
        {"start": "", "end": "present", "org": "榕江县人民政府", "title": "榕江县委副书记、县长",
         "notes": "现任；领导县政府全面工作，负责财政、审计、粮食、人事方面工作；分管县财政局、县审计局；联系县监察委",
         "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "王飞任榕江县长前完整履历未找到（出生年月、籍贯、毕业院校、早期任职经历等信息缺失）",
         "confidence": "unverified", "source_ids": []},
    ]
    wf_relationships = [
        {"person": "徐勃", "person_id": "rongjiang_徐勃", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王飞（县长）与徐勃（县委书记）构成书记-县长搭档",
         "overlap_org": "中共榕江县委员会 / 榕江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "张平", "person_id": "rongjiang_张平", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王飞（县长）与常务副县长张平在县政府班子共事",
         "overlap_org": "榕江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "银政", "person_id": "rongjiang_银政", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王飞（县长）与副县长银政在县政府班子共事",
         "overlap_org": "榕江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "彭晖", "person_id": "rongjiang_彭晖", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王飞（县长）与副县长彭晖在县政府班子共事",
         "overlap_org": "榕江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "黄博", "person_id": "rongjiang_黄博", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王飞与县委副书记黄博在县领导层面共事",
         "overlap_org": "榕江县", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]

    wf_json = make_person_json(persons[1], wf_timeline, wf_relationships)
    wf_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔东南苗族侗族自治州-县长-王飞.json")
    with open(wf_path, "w", encoding="utf-8") as f:
        json.dump(wf_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wf_path}")

    print("\nDone. All artifacts generated in staging directory.")


if __name__ == "__main__":
    build()