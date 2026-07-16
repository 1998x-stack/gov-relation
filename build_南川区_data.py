#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Nanchuan District (南川区), Chongqing leadership network.

Generated: 2026-07-16
Task: chongqing_南川区
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/chongqing_南川区")
DB_PATH = os.path.join(STAGING, "南川区_network.db")
GEXF_PATH = os.path.join(STAGING, "南川区_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "马奇柯", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "重庆永川", "education": "研究生/法学博士",
     "party_join": "1993-07", "work_start": "1995-07",
     "current_post": "中共重庆市南川区委书记",
     "current_org": "中共重庆市南川区委员会",
     "source": "https://baike.baidu.com/item/%E9%A9%AC%E5%A5%87%E6%9F%AF/10437031"},
    {"id": 2, "name": "付嘉康", "gender": "男", "ethnicity": "满族",
     "birth": "1980-11", "birthplace": "黑龙江牡丹江", "education": "研究生/硕士",
     "party_join": "2003-10", "work_start": "2003-07",
     "current_post": "重庆市南川区人民政府区长",
     "current_org": "重庆市南川区人民政府",
     "source": "https://baike.baidu.com/item/%E4%BB%98%E5%98%89%E5%BA%B7"},
    {"id": 3, "name": "向业顺", "gender": "男", "ethnicity": "苗族",
     "birth": "1972-08", "birthplace": "重庆黔江", "education": "市委党校研究生/农业推广硕士",
     "party_join": "", "work_start": "1994-07",
     "current_post": "重庆市红十字会党组书记",
     "current_org": "重庆市红十字会",
     "source": "https://baike.baidu.com/item/%E5%90%91%E4%B8%9A%E9%A1%BA/4399863"},
    {"id": 4, "name": "丁中平", "gender": "女", "ethnicity": "汉族",
     "birth": "1965-04", "birthplace": "重庆垫江", "education": "市委党校研究生",
     "party_join": "", "work_start": "",
     "current_post": "被审查调查",
     "current_org": "",
     "source": "https://www.ccdi.gov.cn/"},
    {"id": 5, "name": "施崇刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "四川泸县", "education": "市委党校研究生",
     "party_join": "", "work_start": "",
     "current_post": "重庆市委统战部副部长、市工商联党组书记",
     "current_org": "重庆市委统战部",
     "source": ""},
    {"id": 6, "name": "张兴益", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-01", "birthplace": "重庆巫溪", "education": "中央党校大学",
     "party_join": "", "work_start": "",
     "current_post": "被审查调查",
     "current_org": "",
     "source": ""},
    {"id": 7, "name": "曹清尧", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-11", "birthplace": "湖南新化", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "被双开",
     "current_org": "",
     "source": ""},

    # ── Current Standing Committee ── (excluding top 2 already listed)
    {"id": 8, "name": "张立平", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共重庆市南川区委副书记",
     "current_org": "中共重庆市南川区委员会",
     "source": ""},
    {"id": 9, "name": "杨逃红", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-07", "birthplace": "", "education": "在职研究生/工学博士",
     "party_join": "", "work_start": "",
     "current_post": "中共重庆市南川区委常委、常务副区长",
     "current_org": "重庆市南川区人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%A8%E9%80%83%E7%BA%A2"},
    {"id": 10, "name": "陈松", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共重庆市南川区委常委、纪委书记、区监委主任",
     "current_org": "中共重庆市南川区纪律检查委员会",
     "source": ""},
    {"id": 11, "name": "冯雪勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-04", "birthplace": "", "education": "在职大学/农业推广硕士",
     "party_join": "", "work_start": "",
     "current_post": "中共重庆市南川区委常委、组织部部长",
     "current_org": "中共重庆市南川区委员会",
     "source": "https://baike.baidu.com/item/%E5%86%AF%E9%9B%AA%E5%8B%87"},
    {"id": 12, "name": "莫席成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共重庆市南川区委常委、政法委书记",
     "current_org": "中共重庆市南川区委员会",
     "source": ""},
    {"id": 13, "name": "陈光辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共重庆市南川区委常委、统战部部长",
     "current_org": "中共重庆市南川区委员会",
     "source": ""},
    {"id": 14, "name": "金强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "重庆市南川区人民政府副区长",
     "current_org": "重庆市南川区人民政府",
     "source": ""},
    {"id": 15, "name": "黄海帆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共重庆市南川区委常委、区人武部部长",
     "current_org": "重庆市南川区人民武装部",
     "source": ""},

    # ── Other Deputy Mayors ──
    {"id": 16, "name": "李恩华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "重庆市南川区人民政府副区长",
     "current_org": "重庆市南川区人民政府",
     "source": ""},
    {"id": 17, "name": "钟文华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "重庆市南川区人民政府副区长",
     "current_org": "重庆市南川区人民政府",
     "source": ""},
    {"id": 18, "name": "胡光模", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "重庆市南川区人民政府副区长",
     "current_org": "重庆市南川区人民政府",
     "source": ""},
    {"id": 19, "name": "李学民", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "重庆市南川区人民政府副区长",
     "current_org": "重庆市南川区人民政府",
     "source": ""},
    {"id": 20, "name": "李玉梅", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "重庆市南川区人民政府副区长",
     "current_org": "重庆市南川区人民政府",
     "source": ""},
    {"id": 21, "name": "李灿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "重庆市南川区人民政府副区长",
     "current_org": "重庆市南川区人民政府",
     "source": ""},
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共重庆市南川区委员会", "type": "党委", "level": "市辖区", "parent": "重庆市委", "location": "重庆市南川区"},
    {"id": 2, "name": "重庆市南川区人民政府", "type": "政府", "level": "市辖区", "parent": "重庆市人民政府", "location": "重庆市南川区"},
    {"id": 3, "name": "中共重庆市南川区纪律检查委员会", "type": "纪委", "level": "市辖区", "parent": "重庆市纪委监委", "location": "重庆市南川区"},
    {"id": 4, "name": "中共重庆市南川区委组织部", "type": "党委", "level": "市辖区", "parent": "中共重庆市南川区委员会", "location": "重庆市南川区"},
    {"id": 5, "name": "中共重庆市南川区委政法委员会", "type": "党委", "level": "市辖区", "parent": "中共重庆市南川区委员会", "location": "重庆市南川区"},
    {"id": 6, "name": "中共重庆市南川区委统一战线工作部", "type": "党委", "level": "市辖区", "parent": "中共重庆市南川区委员会", "location": "重庆市南川区"},
    {"id": 7, "name": "重庆市南川区人民武装部", "type": "军队", "level": "市辖区", "parent": "重庆警备区", "location": "重庆市南川区"},
    {"id": 8, "name": "重庆市红十字会", "type": "群团", "level": "省级", "parent": "重庆市政府", "location": "重庆市渝中区"},
    {"id": 9, "name": "重庆市委统战部", "type": "党委", "level": "省级", "parent": "重庆市委", "location": "重庆市渝中区"},
    {"id": 10, "name": "重庆市委政法委", "type": "党委", "level": "省级", "parent": "重庆市委", "location": "重庆市渝中区"},
    {"id": 11, "name": "重庆市委国安办", "type": "党委", "level": "省级", "parent": "重庆市委", "location": "重庆市"},
    {"id": 12, "name": "重庆红岩联线文化发展管理中心", "type": "事业单位", "level": "省级", "parent": "重庆市委宣传部", "location": "重庆市渝中区"},
    {"id": 13, "name": "重庆市武隆区委", "type": "党委", "level": "市辖区", "parent": "重庆市委", "location": "重庆市武隆区"},
    {"id": 14, "name": "重庆市武隆区人民政府", "type": "政府", "level": "市辖区", "parent": "重庆市人民政府", "location": "重庆市武隆区"},
    {"id": 15, "name": "重庆市合川区人民政府", "type": "政府", "level": "市辖区", "parent": "重庆市人民政府", "location": "重庆市合川区"},
    {"id": 16, "name": "中共秀山县委", "type": "党委", "level": "县级", "parent": "重庆市委", "location": "重庆市秀山县"},
    {"id": 17, "name": "秀山县人民政府", "type": "政府", "level": "县级", "parent": "重庆市人民政府", "location": "重庆市秀山县"},
    {"id": 18, "name": "重庆市巫山县人民政府", "type": "政府", "level": "县级", "parent": "重庆市人民政府", "location": "重庆市巫山县"},
    {"id": 19, "name": "重庆市商务委员会", "type": "政府", "level": "省级", "parent": "重庆市人民政府", "location": "重庆市"},
    {"id": 20, "name": "中国（重庆）自由贸易试验区", "type": "开发区", "level": "省级", "parent": "重庆市政府", "location": "重庆市"},
    {"id": 21, "name": "重庆市招商投资促进局", "type": "政府", "level": "省级", "parent": "重庆市人民政府", "location": "重庆市"},
    {"id": 22, "name": "重庆市民政局", "type": "政府", "level": "省级", "parent": "重庆市人民政府", "location": "重庆市"},
    {"id": 23, "name": "重庆市梁平区政府", "type": "政府", "level": "市辖区", "parent": "重庆市人民政府", "location": "重庆市梁平区"},
    {"id": 24, "name": "重庆市工商联", "type": "群团", "level": "省级", "parent": "重庆市委统战部", "location": "重庆市"},
    {"id": 25, "name": "中共重庆市南川区委宣传部", "type": "党委", "level": "市辖区", "parent": "中共重庆市南川区委员会", "location": "重庆市南川区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # 马奇柯 (id=1)
    {"person_id": 1, "org_id": 15, "title": "重庆市合川区人民政府区长助理（挂职）", "start": "2008-11", "end": "2010-05", "rank": "副处级", "note": "人大博士后挂职进入重庆政界"},
    {"person_id": 1, "org_id": 14, "title": "武隆县副县长→县委常委、宣传部长→政法委书记", "start": "2010-05", "end": "2016-11", "rank": "副厅级", "note": "县改区后延续"},
    {"person_id": 1, "org_id": 13, "title": "重庆市武隆区委常委、政法委书记", "start": "2016-12", "end": "2020-04", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "重庆红岩联线文化发展管理中心党委副书记、主任", "start": "2020-04", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "重庆市委政法委副书记", "start": "2021-07", "end": "2023", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "重庆市委国安办常务副主任", "start": "2023", "end": "2026-04", "rank": "正厅级", "note": "任南川区委书记前最后职务"},
    {"person_id": 1, "org_id": 1, "title": "中共重庆市南川区委书记", "start": "2026-04", "end": "present", "rank": "正厅级", "note": "2026年6月兼任区人武部党委第一书记"},

    # 付嘉康 (id=2)
    {"person_id": 2, "org_id": 19, "title": "重庆市外经贸委干部→市商务委/自贸区任职", "start": "2003-07", "end": "2018", "rank": "", "note": "早期职业生涯在外经贸/商务系统，含日本留学背景"},
    {"person_id": 2, "org_id": 21, "title": "重庆市招商投资促进局任职", "start": "2018", "end": "2020", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 18, "title": "巫山县人民政府县长", "start": "2020", "end": "2025-01", "rank": "正处级", "note": "平调南川区长"},
    {"person_id": 2, "org_id": 2, "title": "重庆市南川区人民政府区长", "start": "2025-01", "end": "present", "rank": "正厅级", "note": "2025年1月15日全票当选"},

    # 向业顺 (id=3)
    {"person_id": 3, "org_id": 17, "title": "秀山县委副书记、代县长→县长→县委书记", "start": "2015-09", "end": "2023-07", "rank": "正处→副厅", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "中共重庆市南川区委书记", "start": "2023-07", "end": "2026-04", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "重庆市红十字会党组书记", "start": "2026-04", "end": "present", "rank": "正厅级", "note": ""},

    # 丁中平 (id=4)
    {"person_id": 4, "org_id": 1, "title": "中共重庆市南川区委书记", "start": "2018-03", "end": "2023-03", "rank": "正厅级", "note": "2025年11月被查"},
    {"person_id": 4, "org_id": 22, "title": "重庆市民政局党委书记、局长", "start": "2023-03", "end": "2025-05", "rank": "正厅级", "note": ""},

    # 施崇刚 (id=5)
    {"person_id": 5, "org_id": 2, "title": "重庆市南川区人民政府区长", "start": "2021-09", "end": "2024-11", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 9, "title": "重庆市委统战部副部长、市工商联党组书记", "start": "2024-12", "end": "present", "rank": "正厅级", "note": ""},

    # 张兴益 (id=6)
    {"person_id": 6, "org_id": 2, "title": "重庆市南川区人民政府区长", "start": "2016-07", "end": "2021-09", "rank": "正厅级", "note": "2026年5月被查"},

    # 曹清尧 (id=7)
    {"person_id": 7, "org_id": 2, "title": "重庆市南川区人民政府区长", "start": "2012-02", "end": "2016-07", "rank": "正厅级", "note": "2025年8月被查，2026年5月双开"},

    # 张立平 (id=8)
    {"person_id": 8, "org_id": 1, "title": "中共重庆市南川区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "履历信息待查"},

    # 杨逃红 (id=9)
    {"person_id": 9, "org_id": 23, "title": "铜梁区委常委、副区长（兼高新区党工委书记）", "start": "", "end": "2025-04", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "南川区委常委、常务副区长", "start": "2025-05", "end": "present", "rank": "副厅级", "note": ""},

    # 冯雪勇 (id=11)
    {"person_id": 11, "org_id": 4, "title": "南川区委常委、组织部部长", "start": "2021-12", "end": "present", "rank": "副厅级", "note": "此前在黔江区工作，任区委办公室主任"},

    # Others with minimal info
    {"person_id": 10, "org_id": 3, "title": "南川区委常委、纪委书记、区监委主任", "start": "", "end": "present", "rank": "副厅级", "note": "履历信息待查"},
    {"person_id": 12, "org_id": 5, "title": "南川区委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": "履历信息待查"},
    {"person_id": 13, "org_id": 6, "title": "南川区委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": "履历信息待查"},
    {"person_id": 14, "org_id": 2, "title": "南川区人民政府副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 7, "title": "南川区委常委、区人武部部长", "start": "", "end": "present", "rank": "副师级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "南川区人民政府副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "南川区人民政府副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "南川区人民政府副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "南川区人民政府副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "南川区人民政府副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "南川区人民政府副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政正职搭档", "overlap_org": "南川区", "overlap_period": "2026-04至今"},

    # 前任→继任：区委书记链
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "向业顺→马奇柯：南川区委书记交接", "overlap_org": "中共重庆市南川区委员会", "overlap_period": "2026-04"},

    # 前任→继任：区长链
    {"person_a": 5, "person_b": 2, "type": "predecessor_successor", "context": "施崇刚→付嘉康：南川区长交接", "overlap_org": "南川区人民政府", "overlap_period": "2025-01"},

    # 前任党政搭档
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "向业顺任区委书记、施崇刚任区长时的党政搭档", "overlap_org": "南川区", "overlap_period": "2023-07至2024-11"},

    # 丁中平→向业顺 区委书记链
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor", "context": "丁中平→向业顺：南川区委书记交接", "overlap_org": "中共重庆市南川区委员会", "overlap_period": "2023-07"},

    # 丁中平+张兴益 党政搭档
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "丁中平任区委书记、张兴益任区长时的党政搭档", "overlap_org": "南川区", "overlap_period": "2018-03至2021-09"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "丁中平任区委书记、施崇刚任区长时的党政搭档", "overlap_org": "南川区", "overlap_period": "2021-09至2023-03"},

    # 曹清尧→张兴益 区长链
    {"person_a": 7, "person_b": 6, "type": "predecessor_successor", "context": "曹清尧→张兴益：南川区长交接", "overlap_org": "南川区人民政府", "overlap_period": "2016-07"},
]

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """GEXF color for person by role."""
    if "区委书记" in p["current_post"] and "副书记" not in p["current_post"]:
        return "255,50,50"   # Red - Party Secretary
    elif "区长" in p["current_post"] and "副区长" not in p["current_post"]:
        return "50,100,255"  # Blue - Government head
    elif "副区长" in p["current_post"] or "常务副区长" in p["current_post"]:
        return "100,150,255" # Light blue - deputy mayor
    elif "纪委书记" in p["current_post"] or "纪委" in p["current_post"]:
        return "255,165,0"   # Orange - Discipline
    elif "被查" in p["current_post"] or "双开" in p["current_post"]:
        return "128,128,128" # Grey - disgraced
    else:
        return "100,100,100" # Grey - other

def org_color(o):
    """GEXF color for organization."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "群团": "255,220,255",
        "事业单位": "220,220,220",
        "军队": "200,255,200",
        "开发区": "200,255,200",
    }
    return colors.get(o["type"], "200,200,200")

def is_top_leader(p):
    return p["id"] in [1, 2]  # 马奇柯 and 付嘉康

# ── BUILD SQLITE ───────────────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
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
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education,
         party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"],
         p["birth"], p["birthplace"], p["education"],
         p["party_join"], p["work_start"],
         p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions
        (person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?)""",
        (pos["person_id"], pos["org_id"], pos["title"],
         pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (r["person_a"], r["person_b"], r["type"],
         r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"✅ SQLite DB: {DB_PATH}")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")

# ── BUILD GEXF ─────────────────────────────────────────────────────────

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gov Relation Research Agent</creator>')
lines.append('    <description>南川区领导班子工作关系网络 - 重庆市 (含现任、前任及周边干部)</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org_type" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    role = p["current_post"]
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
    lines.append('          <attvalue for="2" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append('          <attvalue for="1" value=""/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
eid = 0

# Positions as person→organization edges
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Relationships as person↔person edges
for r in relationships:
    eid += 1
    w = "3.0" if r["type"] in ("predecessor_successor",) else "2.0"
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF Graph: {GEXF_PATH}")
print(f"   Person nodes: {len(persons)}")
print(f"   Organization nodes: {len(organizations)}")
print(f"   Position edges: {len(positions)}")
print(f"   Relationship edges: {len(relationships)}")
print(f"   Total edges: {eid}")
print("\nDone! DB and GEXF generated successfully.")
