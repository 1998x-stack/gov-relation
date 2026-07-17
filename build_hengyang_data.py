#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 衡阳市 (Hengyang City) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/hengyang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/hengyang_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════
    # A. CITY LEVEL (市级领导)
    # ═══════════════════════════════════════════════════════════════

    # ── 1. 市委书记 ──
    {"id": 1, "name": "朱健", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-07", "birthplace": "江苏江阴", "education": "上海交通大学动力机械工程系热能动力机械与装置专业工学学士(1997)/法学硕士(1998)/管理学博士(2001)",
     "party_join": "1994-08", "work_start": "1997",
     "current_post": "衡阳市委书记", "current_org": "中共衡阳市委",
     "source": "https://zh.wikipedia.org/wiki/%E6%9C%B1%E5%81%A5_(1975%E5%B9%B4)"},

    # ── 2. 市长 ──
    {"id": 2, "name": "刘中杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-09", "birthplace": "安徽无为", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "衡阳市市长", "current_org": "衡阳市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E9%98%B3%E5%B8%82"},

    # ── 3. 人大主任 ──
    {"id": 3, "name": "刘正兴", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-09", "birthplace": "湖南祁东", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "衡阳市人大常委会主任", "current_org": "衡阳市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E9%98%B3%E5%B8%82"},

    # ── 4. 政协主席 ──
    {"id": 4, "name": "吴曙光", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-02", "birthplace": "【待查】", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "衡阳市政协主席", "current_org": "衡阳市政协",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E9%98%B3%E5%B8%82"},

    # ── 5. 前任市委书记 (2023-2025) ──
    {"id": 5, "name": "刘越高", "gender": "男", "ethnicity": "汉族",
     "birth": "【待查】", "birthplace": "【待查】", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任衡阳市委书记（2023-2025）", "current_org": "中共衡阳市委（前任）",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E9%98%B3%E5%B8%82"},

    # ── 6. 前市长→书记→湖南省政协副主席 ──
    {"id": 6, "name": "邓群策", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-05", "birthplace": "湖南祁阳", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前衡阳市委书记/市长（2018-2023）", "current_org": "【待查】",
     "source": "https://zh.wikipedia.org/wiki/%E9%82%93%E7%BE%A4%E7%AD%96"},

    # ═══════════════════════════════════════════════════════════════
    # B. DISTRICT/COUNTY LEVEL — 12 regions, 24 positions
    # ═══════════════════════════════════════════════════════════════

    # ── 珠晖区 ──
    {"id": 10, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "珠晖区委书记", "current_org": "中共珠晖区委",
     "source": "https://zh.wikipedia.org/wiki/%E7%8F%A0%E6%99%96%E5%8C%BA"},
    {"id": 11, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "珠晖区区长", "current_org": "珠晖区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%8F%A0%E6%99%96%E5%8C%BA"},

    # ── 雁峰区 ──
    {"id": 12, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "雁峰区委书记", "current_org": "中共雁峰区委",
     "source": "https://zh.wikipedia.org/wiki/%E9%9B%81%E5%B3%B0%E5%8C%BA"},
    {"id": 13, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "雁峰区区长", "current_org": "雁峰区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E9%9B%81%E5%B3%B0%E5%8C%BA"},

    # ── 石鼓区 ──
    {"id": 14, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "石鼓区委书记", "current_org": "中共石鼓区委",
     "source": "https://zh.wikipedia.org/wiki/%E7%9F%B3%E9%BC%93%E5%8C%BA"},
    {"id": 15, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "石鼓区区长", "current_org": "石鼓区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%9F%B3%E9%BC%93%E5%8C%BA"},

    # ── 蒸湘区 ──
    {"id": 16, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蒸湘区委书记", "current_org": "中共蒸湘区委",
     "source": "https://zh.wikipedia.org/wiki/%E8%92%B8%E6%B9%98%E5%8C%BA"},
    {"id": 17, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蒸湘区区长", "current_org": "蒸湘区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%92%B8%E6%B9%98%E5%8C%BA"},

    # ── 南岳区 ──
    {"id": 18, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南岳区委书记", "current_org": "中共南岳区委",
     "source": "https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B2%B3%E5%8C%BA"},
    {"id": 19, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南岳区区长", "current_org": "南岳区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B2%B3%E5%8C%BA"},

    # ── 衡阳县 ──
    {"id": 20, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡阳县委书记", "current_org": "中共衡阳县委",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E9%98%B3%E5%8E%BF"},
    {"id": 21, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡阳县县长", "current_org": "衡阳县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E9%98%B3%E5%8E%BF"},

    # ── 衡南县 ──
    {"id": 22, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡南县委书记", "current_org": "中共衡南县委",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E5%8D%97%E5%8E%BF"},
    {"id": 23, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡南县县长", "current_org": "衡南县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E5%8D%97%E5%8E%BF"},

    # ── 衡山县 ──
    {"id": 24, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡山县委书记", "current_org": "中共衡山县委",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E5%B1%B1%E5%8E%BF"},
    {"id": 25, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡山县县长", "current_org": "衡山县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E5%B1%B1%E5%8E%BF"},

    # ── 衡东县 ──
    {"id": 26, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡东县委书记", "current_org": "中共衡东县委",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E4%B8%9C%E5%8E%BF"},
    {"id": 27, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "衡东县县长", "current_org": "衡东县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%A1%A1%E4%B8%9C%E5%8E%BF"},

    # ── 祁东县 ──
    {"id": 28, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "祁东县委书记", "current_org": "中共祁东县委",
     "source": "https://zh.wikipedia.org/wiki/%E7%A5%81%E4%B8%9C%E5%8E%BF"},
    {"id": 29, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "祁东县县长", "current_org": "祁东县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%A5%81%E4%B8%9C%E5%8E%BF"},

    # ── 耒阳市 ──
    {"id": 30, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "耒阳市委书记", "current_org": "中共耒阳市委",
     "source": "https://zh.wikipedia.org/wiki/%E8%80%92%E9%98%B3%E5%B8%82"},
    {"id": 31, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "耒阳市市长", "current_org": "耒阳市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%80%92%E9%98%B3%E5%B8%82"},

    # ── 常宁市 ──
    {"id": 32, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "常宁市委书记", "current_org": "中共常宁市委",
     "source": "https://zh.wikipedia.org/wiki/%E5%B8%B8%E5%AE%81%E5%B8%82"},
    {"id": 33, "name": "【待查】", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "常宁市市长", "current_org": "常宁市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%B8%B8%E5%AE%81%E5%B8%82"},

    # ═══════════════════════════════════════════════════════════════
    # Added key historical predecessors
    # ═══════════════════════════════════════════════════════════════
    {"id": 40, "name": "秦国文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前衡阳市委书记（2021-2022），现任湖南省副省长", "current_org": "湖南省人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%A7%A6%E5%9B%BD%E6%96%87"},
    {"id": 41, "name": "郑建新", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-12", "birthplace": "贵州贵阳", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前衡阳市委书记（2018-2020），前长沙市长（2021-2023，被查）", "current_org": "【被调查】",
     "source": "https://zh.wikipedia.org/wiki/%E9%83%91%E5%BB%BA%E6%96%B0"},
    {"id": 42, "name": "周农", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-08", "birthplace": "湖南益阳", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前衡阳市委书记（2016-2018），现任湖南省人大常委会副主任", "current_org": "湖南省人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E5%91%A8%E5%86%9C"},
    {"id": 43, "name": "李亿龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1958-10", "birthplace": "湖南长沙", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前衡阳市委书记（2014-2016，已被判刑）", "current_org": "【已被判刑】",
     "source": "https://zh.wikipedia.org/wiki/%E6%9D%8E%E4%BA%BF%E9%BE%99"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共衡阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "衡阳市蒸湘区"},
    {"id": 2, "name": "衡阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "衡阳市蒸湘区"},
    {"id": 3, "name": "衡阳市人大常委会", "type": "人大", "level": "地市级", "parent": "湖南省人大常委会", "location": "衡阳市"},
    {"id": 4, "name": "衡阳市政协", "type": "政协", "level": "地市级", "parent": "湖南省政协", "location": "衡阳市"},

    # Districts (市辖区)
    {"id": 10, "name": "中共珠晖区委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市珠晖区"},
    {"id": 11, "name": "珠晖区人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市珠晖区"},
    {"id": 12, "name": "中共雁峰区委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市雁峰区"},
    {"id": 13, "name": "雁峰区人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市雁峰区"},
    {"id": 14, "name": "中共石鼓区委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市石鼓区"},
    {"id": 15, "name": "石鼓区人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市石鼓区"},
    {"id": 16, "name": "中共蒸湘区委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市蒸湘区"},
    {"id": 17, "name": "蒸湘区人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市蒸湘区"},
    {"id": 18, "name": "中共南岳区委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市南岳区"},
    {"id": 19, "name": "南岳区人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市南岳区"},

    # Counties (县)
    {"id": 20, "name": "中共衡阳县委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市衡阳县"},
    {"id": 21, "name": "衡阳县人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市衡阳县"},
    {"id": 22, "name": "中共衡南县委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市衡南县"},
    {"id": 23, "name": "衡南县人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市衡南县"},
    {"id": 24, "name": "中共衡山县委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市衡山县"},
    {"id": 25, "name": "衡山县人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市衡山县"},
    {"id": 26, "name": "中共衡东县委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市衡东县"},
    {"id": 27, "name": "衡东县人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市衡东县"},
    {"id": 28, "name": "中共祁东县委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市祁东县"},
    {"id": 29, "name": "祁东县人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市祁东县"},

    # County-level cities (县级市)
    {"id": 30, "name": "中共耒阳市委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市耒阳市"},
    {"id": 31, "name": "耒阳市人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市耒阳市"},
    {"id": 32, "name": "中共常宁市委", "type": "党委", "level": "县处级", "parent": "中共衡阳市委", "location": "衡阳市常宁市"},
    {"id": 33, "name": "常宁市人民政府", "type": "政府", "level": "县处级", "parent": "衡阳市人民政府", "location": "衡阳市常宁市"},
]

# ── Positions (person → org relationships) ──
positions = [
    # City level
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2025-11", "end": "", "rank": "正厅级", "note": "此前为衡阳市市长(2020-2025)"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2025-12", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "2022-01", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "2024-12", "end": "", "rank": "正厅级", "note": ""},

    # Historical succession
    {"person_id": 5, "org_id": 1, "title": "市委书记", "start": "2023", "end": "2025-11", "rank": "正厅级", "note": "前任市委书记，去向待查"},
    {"person_id": 6, "org_id": 1, "title": "市委书记", "start": "2021", "end": "2023", "rank": "正厅级", "note": "前任市委书记，前市长"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start": "2020-02", "end": "2025-12", "rank": "正厅级", "note": "前任市长，后升书记"},
    {"person_id": 40, "org_id": 1, "title": "市委书记", "start": "2021", "end": "2022", "rank": "正厅级", "note": "前任市委书记，现任湖南省副省长"},
    {"person_id": 41, "org_id": 1, "title": "市委书记", "start": "2018", "end": "2020", "rank": "正厅级", "note": "前任市委书记，后任长沙市长"},
    {"person_id": 42, "org_id": 1, "title": "市委书记", "start": "2016", "end": "2018", "rank": "正厅级", "note": "前任市委书记，现任湖南省人大副主任"},
    {"person_id": 43, "org_id": 1, "title": "市委书记", "start": "2014", "end": "2016", "rank": "正厅级", "note": "已被判刑"},
]

# ── Person-to-Person Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "市委书记+市长搭档", "overlap_org": "衡阳市", "overlap_period": "2025-12至今"},
    {"person_a": 1, "person_b": 5, "type": "前后任", "context": "朱健接替刘越高任市委书记", "overlap_org": "中共衡阳市委", "overlap_period": "2025-11"},
    {"person_a": 1, "person_b": 6, "type": "前后任", "context": "朱健接替邓群策任市委书记", "overlap_org": "中共衡阳市委", "overlap_period": "2021-2025"},
    {"person_a": 5, "person_b": 40, "type": "前后任", "context": "刘越高接替秦国文任市委书记", "overlap_org": "中共衡阳市委", "overlap_period": "2022-2023"},
    {"person_a": 40, "person_b": 41, "type": "前后任", "context": "秦国文接替郑建新任市委书记", "overlap_org": "中共衡阳市委", "overlap_period": "2021"},
    {"person_a": 41, "person_b": 42, "type": "前后任", "context": "郑建新接替周农任市委书记", "overlap_org": "中共衡阳市委", "overlap_period": "2018"},
    {"person_a": 42, "person_b": 43, "type": "前后任", "context": "周农接替李亿龙任市委书记", "overlap_org": "中共衡阳市委", "overlap_period": "2016"},
]

# ── BUILD SQLITE ────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

# ── BUILD GEXF ─────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="organization" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="education" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        # Color by role
        color = "grey"
        post = p["current_post"]
        if "书记" in post and "副" not in post and "区委" not in post and "县委" not in post:
            color = "red"
        elif "市长" in post and "副" not in post and "市委" not in post:
            color = "blue"
        elif "人大" in post:
            color = "orange"
        elif "政协" in post:
            color = "orange"
        elif "区委书记" in post or "县委书记" in post:
            color = "#CC3333"
        elif "区长" in post or "县长" in post or "市长" in post:
            color = "#3366CC"
        elif "副" in post:
            color = "#CC9933"

        if color == "red":
            r, g, b = "200", "50", "50"
        elif color == "blue":
            r, g, b = "50", "100", "200"
        elif color == "orange":
            r, g, b = "200", "150", "50"
        elif color == "#CC3333":
            r, g, b = "204", "51", "51"
        elif color == "#3366CC":
            r, g, b = "51", "102", "204"
        elif color == "#CC9933":
            r, g, b = "204", "153", "51"
        else:
            r, g, b = "128", "128", "128"

        lines.append(f'      <node id="p{p["id"]}" label="{p["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{p["current_org"]}"/>')
        lines.append(f'          <attvalue for="2" value="{p["birth"]}"/>')
        lines.append(f'          <attvalue for="3" value="{p["birthplace"]}"/>')
        lines.append(f'          <attvalue for="4" value="{p["education"][:50] if p["education"] else ""}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="15.0"/>')
        lines.append(f'        <viz:position x="0" y="0" z="0"/>')
        lines.append(f'      </node>')

    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{o["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{o["type"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="100" g="100" b="100" a="1.0"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    edge_id = 0

    # Person → Organization (worked_at)
    for pos in positions:
        edge_id += 1
        lines.append(f'      <edge id="e{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="worked_at">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{pos["title"]}"/>')
        lines.append(f'          <attvalue for="2" value="{pos["start"]}"/>')
        lines.append(f'          <attvalue for="3" value="{pos["end"] if pos["end"] else "至今"}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="180" g="180" b="180" a="0.5"/>')
        lines.append(f'        <viz:thickness value="2.0"/>')
        lines.append(f'      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        edge_id += 1
        thickness = "3.0" if r["type"] in ("搭档",) else "1.5"
        if r["type"] == "搭档":
            cr, cg, cb = "200", "150", "50"
        elif r["type"] == "前后任":
            cr, cg, cb = "100", "150", "200"
        else:
            cr, cg, cb = "128", "128", "200"

        lines.append(f'      <edge id="e{edge_id}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{r["type"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{r["type"]}"/>')
        lines.append(f'          <attvalue for="2" value="{r["context"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append(f'        <viz:thickness value="{thickness}"/>')
        lines.append(f'      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"[GEXF] Created {GEXF_PATH}")

# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  衡阳市（Hengyang City）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
