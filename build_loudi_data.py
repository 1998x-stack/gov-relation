#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 娄底市 (Loudi City, Hunan) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/loudi_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/loudi_network.gexf")

# ═══════════════════════════════════════════════════════════════
# DATA — ALL PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ── A. City-level leadership ──
    {"id": 1, "name": "曾超群", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-09", "birthplace": "湖南省邵东市", "education": "北京大学经济学院国际经济专业/管理学博士",
     "party_join": "1998-12", "work_start": "1997-09",
     "current_post": "娄底市委书记（2025.04-）", "current_org": "中共娄底市委",
     "source": "https://zh.wikipedia.org/wiki/曾超群_(1975年)"},
    {"id": 2, "name": "何朝晖", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-04", "birthplace": "湖南省攸县", "education": "在职研究生/管理学博士",
     "party_join": "", "work_start": "",
     "current_post": "娄底市长（2025.11-）", "current_org": "娄底市人民政府",
     "source": "https://zh.wikipedia.org/wiki/娄底市"},
    {"id": 3, "name": "邹文辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-02", "birthplace": "湖南省常宁市", "education": "",
     "party_join": "1986", "work_start": "",
     "current_post": "湖南省人大常委会委员/环资委主任委员（2025.01-）", "current_org": "湖南省人大常委会",
     "source": "https://zh.wikipedia.org/wiki/邹文辉"},
    {"id": 4, "name": "李定桥", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-09", "birthplace": "湖南省安仁县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "娄底市人大常委会主任（2026.01-）", "current_org": "娄底市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/娄底市"},
    {"id": 5, "name": "梁立坚", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "湖南省涟源市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "娄底市政协主席（2022.01-）", "current_org": "娄底市政协",
     "source": "https://zh.wikipedia.org/wiki/娄底市"},

    # ── B. 娄星区 ──
    {"id": 10, "name": "李彦文", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-03", "birthplace": "湖南省涟源市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "娄星区委书记（2018.10-）", "current_org": "中共娄星区委",
     "source": "https://zh.wikipedia.org/wiki/娄星区"},
    {"id": 11, "name": "刘志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "湖南省新化县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "娄星区长（2021.10-）", "current_org": "娄星区人民政府",
     "source": "https://zh.wikipedia.org/wiki/娄星区"},
    {"id": 12, "name": "陈晓林", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-02", "birthplace": "湖南省新化县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "娄星区人大常委会主任（2021.10-）", "current_org": "娄星区人大常委会",
     "source": "https://zh.wikipedia.org/wiki/娄星区"},
    {"id": 13, "name": "邓伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-04", "birthplace": "湖南省宁乡市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "娄星区政协主席（2021.10-）", "current_org": "娄星区政协",
     "source": "https://zh.wikipedia.org/wiki/娄星区"},

    # ── C. 双峰县 ──
    {"id": 20, "name": "彭石清", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-07", "birthplace": "湖南省娄底市娄星区", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "双峰县委书记（2021.07-）", "current_org": "中共双峰县委",
     "source": "https://zh.wikipedia.org/wiki/双峰县"},
    {"id": 21, "name": "李基联", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-07", "birthplace": "湖南省溆浦县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "双峰县长（2021.10-）", "current_org": "双峰县人民政府",
     "source": "https://zh.wikipedia.org/wiki/双峰县"},
    {"id": 22, "name": "段平屏", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-10", "birthplace": "湖南省冷水江市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "双峰县人大常委会主任（2021.10-）", "current_org": "双峰县人大常委会",
     "source": "https://zh.wikipedia.org/wiki/双峰县"},
    {"id": 23, "name": "王德文", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-07", "birthplace": "（待查）", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "双峰县政协主席（2021.10-）", "current_org": "双峰县政协",
     "source": "https://zh.wikipedia.org/wiki/双峰县"},

    # ── D. 新化县 ──
    {"id": 30, "name": "彭韬", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-01", "birthplace": "湖南省新化县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新化县委书记（2025.06-）", "current_org": "中共新化县委",
     "source": "https://zh.wikipedia.org/wiki/新化县"},
    {"id": 31, "name": "邹剑锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-09", "birthplace": "湖南省长沙县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新化县长（2025.12-）", "current_org": "新化县人民政府",
     "source": "https://zh.wikipedia.org/wiki/新化县"},
    {"id": 32, "name": "杨韶红", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-11", "birthplace": "湖南省新化县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新化县人大常委会主任（2021.10-）", "current_org": "新化县人大常委会",
     "source": "https://zh.wikipedia.org/wiki/新化县"},
    {"id": 33, "name": "李笃成", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-04", "birthplace": "（待查）", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新化县政协主席（2021.10-）", "current_org": "新化县政协",
     "source": "https://zh.wikipedia.org/wiki/新化县"},

    # ── E. 冷水江市 ──
    {"id": 40, "name": "曾伯怡", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-10", "birthplace": "湖南省双峰县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "冷水江市委书记（2021.07-）", "current_org": "中共冷水江市委",
     "source": "https://zh.wikipedia.org/wiki/冷水江市"},
    {"id": 41, "name": "陈创业", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-06", "birthplace": "湖南省新化县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "冷水江市长（2021.09-）", "current_org": "冷水江市人民政府",
     "source": "https://zh.wikipedia.org/wiki/冷水江市"},
    {"id": 42, "name": "孙纬辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "湖南省新化县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "冷水江市人大常委会主任（2021.11-）", "current_org": "冷水江市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/冷水江市"},
    {"id": 43, "name": "罗中秋", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-09", "birthplace": "湖南省邵东市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "冷水江市政协主席（2018-）", "current_org": "冷水江市政协",
     "source": "https://zh.wikipedia.org/wiki/冷水江市"},

    # ── F. 涟源市 ──
    {"id": 50, "name": "段晓赛", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "湖南省耒阳市", "education": "",
     "party_join": "", "work_start": "1998-08",
     "current_post": "涟源市委书记（2025.03-）", "current_org": "中共涟源市委",
     "source": "https://zh.wikipedia.org/wiki/段晓赛"},
    {"id": 51, "name": "邓伟谋", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "湖南省双峰县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "涟源市长（2021.07-）", "current_org": "涟源市人民政府",
     "source": "https://zh.wikipedia.org/wiki/涟源市"},
    {"id": 52, "name": "梁育清", "gender": "女", "ethnicity": "汉族",
     "birth": "1967-11", "birthplace": "湖南省涟源市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "涟源市人大常委会主任（2021-）", "current_org": "涟源市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/涟源市"},
    {"id": 53, "name": "周惠军", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-03", "birthplace": "湖南省娄底市娄星区", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "涟源市政协主席（2021.10-）", "current_org": "涟源市政协",
     "source": "https://zh.wikipedia.org/wiki/涟源市"},

    # ── G. 知名前任领导人 ──
    {"id": 60, "name": "林武", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-02", "birthplace": "福建省闽侯县", "education": "江西冶金学院",
     "party_join": "1987-01", "work_start": "1982-08",
     "current_post": "山东省委书记（2023-）", "current_org": "中共山东省委",
     "source": "https://zh.wikipedia.org/wiki/林武_(1962年)"},
    {"id": 61, "name": "李荐国", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-03", "birthplace": "湖南省衡东县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（已落马，判刑13年）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/李荐国"},
    {"id": 62, "name": "杨懿文", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-07", "birthplace": "湖南省汨罗市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（已落马，判刑16年6个月）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/杨懿文"},
]

# ── Organizations ──
organizations = [
    # City-level
    {"id": 1, "name": "中共娄底市委", "type": "党委", "level": "地级", "parent": "中共湖南省委", "location": "娄底市"},
    {"id": 2, "name": "娄底市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "娄底市"},
    {"id": 3, "name": "娄底市人大常委会", "type": "人大", "level": "地级", "parent": "", "location": "娄底市"},
    {"id": 4, "name": "娄底市政协", "type": "政协", "level": "地级", "parent": "", "location": "娄底市"},
    # Louxing District
    {"id": 10, "name": "中共娄星区委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "娄星区"},
    {"id": 11, "name": "娄星区人民政府", "type": "政府", "level": "县级", "parent": "", "location": "娄星区"},
    {"id": 12, "name": "娄星区人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "娄星区"},
    {"id": 13, "name": "娄星区政协", "type": "政协", "level": "县级", "parent": "", "location": "娄星区"},
    # Shuangfeng County
    {"id": 20, "name": "中共双峰县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "双峰县"},
    {"id": 21, "name": "双峰县人民政府", "type": "政府", "level": "县级", "parent": "", "location": "双峰县"},
    {"id": 22, "name": "双峰县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "双峰县"},
    {"id": 23, "name": "双峰县政协", "type": "政协", "level": "县级", "parent": "", "location": "双峰县"},
    # Xinhua County
    {"id": 30, "name": "中共新化县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "新化县"},
    {"id": 31, "name": "新化县人民政府", "type": "政府", "level": "县级", "parent": "", "location": "新化县"},
    {"id": 32, "name": "新化县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "新化县"},
    {"id": 33, "name": "新化县政协", "type": "政协", "level": "县级", "parent": "", "location": "新化县"},
    # Lengshuijiang
    {"id": 40, "name": "中共冷水江市委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "冷水江市"},
    {"id": 41, "name": "冷水江市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "冷水江市"},
    {"id": 42, "name": "冷水江市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "冷水江市"},
    {"id": 43, "name": "冷水江市政协", "type": "政协", "level": "县级", "parent": "", "location": "冷水江市"},
    # Lianyuan
    {"id": 50, "name": "中共涟源市委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "涟源市"},
    {"id": 51, "name": "涟源市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "涟源市"},
    {"id": 52, "name": "涟源市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "涟源市"},
    {"id": 53, "name": "涟源市政协", "type": "政协", "level": "县级", "parent": "", "location": "涟源市"},
    # Higher-level
    {"id": 100, "name": "中共湖南省委", "type": "党委", "level": "省级", "parent": "中共中央", "location": "长沙市"},
    {"id": 101, "name": "湖南省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "长沙市"},
]

# ── Positions (person_id, org_id, title, start, end, rank) ──
positions = [
    # City-level
    (1, 1, "中共娄底市委书记", "2025-04", "", "正厅级"),
    (1, 2, "娄底市人民政府市长", "2021-04", "2025-11", "正厅级"),
    (2, 2, "娄底市人民政府市长", "2025-11", "", "正厅级"),
    (3, 1, "中共娄底市委书记", "2021-10", "2025-04", "正厅级"),
    (3, 101, "湖南省人大常委会环资委主任委员", "2025-01", "", "正厅级"),
    (4, 3, "娄底市人大常委会主任", "2026-01", "", "正厅级"),
    (5, 4, "娄底市政协主席", "2022-01", "", "正厅级"),
    # Louxing
    (10, 10, "娄星区委书记", "2018-10", "", "副厅级"),
    (11, 11, "娄星区长", "2021-10", "", "正处级"),
    (12, 12, "娄星区人大常委会主任", "2021-10", "", "正处级"),
    (13, 13, "娄星区政协主席", "2021-10", "", "正处级"),
    # Shuangfeng
    (20, 20, "双峰县委书记", "2021-07", "", "副厅级"),
    (21, 21, "双峰县长", "2021-10", "", "正处级"),
    (22, 22, "双峰县人大常委会主任", "2021-10", "", "正处级"),
    (23, 23, "双峰县政协主席", "2021-10", "", "正处级"),
    # Xinhua
    (30, 30, "新化县委书记", "2025-06", "", "副厅级"),
    (30, 31, "新化县人民政府县长", "2021", "2025-06", "正处级"),
    (31, 31, "新化县长", "2025-12", "", "正处级"),
    (32, 32, "新化县人大常委会主任", "2021-10", "", "正处级"),
    (33, 33, "新化县政协主席", "2021-10", "", "正处级"),
    # Lengshuijiang
    (40, 40, "冷水江市委书记", "2021-07", "", "副厅级"),
    (41, 41, "冷水江市长", "2021-09", "", "正处级"),
    (42, 42, "冷水江市人大常委会主任", "2021-11", "", "正处级"),
    (43, 43, "冷水江市政协主席", "2018", "", "正处级"),
    # Lianyuan
    (50, 50, "涟源市委书记", "2025-03", "", "副厅级"),
    (51, 51, "涟源市长", "2021-07", "", "正处级"),
    (52, 52, "涟源市人大常委会主任", "2021", "", "正处级"),
    (53, 53, "涟源市政协主席", "2021-10", "", "正处级"),
    # Former leaders
    (60, 1, "中共娄底市委书记", "2008-03", "2012-12", "正厅级"),
    (61, 1, "中共娄底市委书记", "2016-03", "2019-12", "正厅级"),
    (62, 2, "娄底市人民政府市长", "2016-03", "2021-04", "正厅级"),
]

# ── Relationships (person_a, person_b, type, context, overlap_org, overlap_period) ──
relationships = [
    # Succession
    (1, 3, "succession", "曾超群接替邹文辉任娄底市委书记", "中共娄底市委", "2025"),
    (1, 62, "succession", "曾超群接替杨懿文任娄底市长", "娄底市人民政府", "2021"),
    # Same-org overlaps
    (1, 3, "colleague", "曾超群任市长期间与邹文辉（书记）共事", "中共娄底市委/娄底市人民政府", "2021-2025"),
    (1, 4, "colleague", "曾超群与李定桥在娄底市共事", "娄底市", "2026"),
    (1, 5, "colleague", "曾超群与梁立坚在娄底市共事", "娄底市", "2022-"),
    (2, 4, "colleague", "何朝晖与李定桥在娄底市共事", "娄底市", "2026"),
    (2, 5, "colleague", "何朝晖与梁立坚在娄底市共事", "娄底市", "2025-"),
    # Cross-county linkages (same hometown origin)
    (10, 5, "hometown", "李彦文（涟源人）与梁立坚（涟源人）同乡", "涟源市", ""),
    (11, 41, "hometown", "刘志刚（新化人）与陈创业（新化人）同乡", "新化县", ""),
    (11, 40, "hometown", "刘志刚（新化人）与曾伯怡（双峰人，曾在双峰）", "", ""),
    (20, 51, "hometown", "彭石清（娄星区人）与周惠军（娄星区人）同乡", "娄星区", ""),
    (21, 40, "hometown", "李基联（溆浦人）- 曾伯怡非同一家乡", "", ""),
    (40, 51, "hometown", "曾伯怡（双峰人）与邓伟谋（双峰人）同乡", "双峰县", ""),
    (40, 20, "hometown", "曾伯怡（双峰人）与彭石清（娄星区人）同乡跨县", "", ""),
    (30, 32, "colleague", "彭韬与杨韶红在新化县委共事", "中共新化县委", "2025-"),
    (30, 11, "hometown", "彭韬（新化人）与刘志刚（新化人）同乡", "新化县", ""),
    (30, 41, "hometown", "彭韬（新化人）与陈创业（新化人）同乡", "新化县", ""),
    (30, 42, "hometown", "彭韬（新化人）与孙纬辉（新化人）同乡", "新化县", ""),
    (31, 30, "subordinate", "邹剑锋任县长、彭韬任书记，党政搭档", "新化县", "2025-"),
    (50, 51, "colleague", "段晓赛与邓伟谋党政搭档", "涟源市", "2025-"),
    (10, 51, "hometown", "李彦文（涟源人）与邓伟谋（双峰人）毗邻", "", ""),
    (3, 7, "colleague", "邹文辉与段晓赛无直接交集（段2025年调任）", "", ""),
    # Corruption connections
    (61, 62, "corruption", "李荐国与杨懿文均涉及娄底腐败案", "娄底市", "2015-2021"),
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def role_category(p):
    """Return role category for coloring."""
    post = p.get("current_post", "")
    if "书记" in post and "市委" in post:
        return "party_secretary"
    elif "书记" in post:
        return "party_secretary"
    elif "市长" in post or "区长" in post or "县长" in post:
        return "mayor"
    elif "主任" in post:
        return "npc"
    elif "主席" in post:
        return "cppcc"
    return "other"


def person_color(p):
    cat = role_category(p)
    if cat == "party_secretary":
        return "255,50,50"       # Red
    elif cat == "mayor":
        return "50,100,255"      # Blue
    elif cat == "npc":
        return "255,165,0"       # Orange
    elif cat == "cppcc":
        return "100,180,100"     # Green
    elif p["name"] in ("李荐国", "杨懿文"):
        return "150,0,0"         # Dark red for fallen
    else:
        return "100,100,100"     # Grey


def is_top_leader(p):
    return any(kw in p["current_post"] for kw in ["书记", "市长", "区长", "县长"])


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


# ═══════════════════════════════════════════════════════════════
# SQLITE DATABASE
# ═══════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"],
         p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions (person_id,org_id,title,start,end,rank)
        VALUES (?,?,?,?,?,?)""",
        (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]))

for r in relationships:
    cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (r[0], r[1], r[2], r[3], r[4], r[5]))

conn.commit()

stats_p = cur.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
stats_o = cur.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
stats_pos = cur.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
stats_r = cur.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
conn.close()

print(f"SQLite: {DB_PATH}")
print(f"  Persons: {stats_p}, Organizations: {stats_o}, Positions: {stats_pos}, Relationships: {stats_r}")


# ═══════════════════════════════════════════════════════════════
# GEXF GRAPH
# ═══════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>娄底市（Loudi City, Hunan）领导班子工作关系网络 — 含市级及5区县主要领导</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="birth" type="string"/>')
lines.append('      <attribute id="3" title="birthplace" type="string"/>')
lines.append('      <attribute id="4" title="source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="start" type="string"/>')
lines.append('      <attribute id="3" title="end" type="string"/>')
lines.append('    </attributes>')

# NODES
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    role = role_category(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# EDGES
lines.append('    <edges>')
eid = 0

# Person → Organization (worked_at)
for pos in positions:
    pid, oid, title = pos[0], pos[1], pos[2]
    start = pos[3]
    end = pos[4]
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(start)}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(end)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person ↔ Person (relationships)
for r in relationships:
    pa, pb, rtype, ctx = r[0], r[1], r[2], r[3]
    period = r[5] if len(r) > 5 else ""
    eid += 1
    weight = "2.0" if rtype in ("colleague", "subordinate") else "1.5"
    lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(ctx)}" weight="{weight}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"GEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons) + len(organizations)}, Edges: {eid}")
print("Done.")
