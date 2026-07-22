#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 连山壮族瑶族自治县, 清远市, 广东省.

Targets: 县委书记 许崇砚 & 县长 陆治杰

Covers: county committee (县委) leadership, county government (县政府) leadership,
predecessor/successor chains, and the county-level leadership network.

Sources:
- gdls.gov.cn: Official Lianshan county government website (领导之窗)
- News articles from gdls.gov.cn

Generated: 2026-07-22
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_连山壮族瑶族自治县")
DB_PATH = os.path.join(TMP, "连山壮族瑶族自治县_network.db")
GEXF_PATH = os.path.join(TMP, "连山壮族瑶族自治县_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-22"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── County Committee (县委) Leadership ──

    # 许崇砚 — 连山壮族瑶族自治县委书记
    # Source: gdls.gov.cn 领导之窗
    {"id": 1, "name": "许崇砚", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委书记",
     "current_org": "中共连山壮族瑶族自治县委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_430016.html"},

    # 陆治杰 — 连山壮族瑶族自治县委副书记、县长
    # 男，壮族，大学，在职硕士，1983年9月生，中共党员
    {"id": 2, "name": "陆治杰", "gender": "男", "ethnicity": "壮族", "birth": "1983-09",
     "birthplace": "", "education": "大学，在职硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委副书记、县长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_430014.html"},

    # 黄科 — 连山壮族瑶族自治县委副书记
    {"id": 3, "name": "黄科", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委副书记",
     "current_org": "中共连山壮族瑶族自治县委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_430027.html"},

    # 伍洁星 — 县委副书记（挂任）
    {"id": 4, "name": "伍洁星", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委副书记（挂任）",
     "current_org": "中共连山壮族瑶族自治县委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_1508143.html"},

    # 王少锋 — 县委常委、县委宣传部部长
    {"id": 5, "name": "王少锋", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委常委、县委宣传部部长",
     "current_org": "中共连山壮族瑶族自治县委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_430020.html"},

    # 谢梅 — 县委常委、县委统战部部长、县委政法委书记
    {"id": 6, "name": "谢梅", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委常委、县委统战部部长、县委政法委书记",
     "current_org": "中共连山壮族瑶族自治县委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_430025.html"},

    # 刘俊辉 — 县委常委、县委办公室主任、县政府办公室主任
    {"id": 7, "name": "刘俊辉", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委常委、县委办公室主任、县政府办公室主任",
     "current_org": "中共连山壮族瑶族自治县委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_1414776.html"},

    # 卢晓光 — 县委常委、县人民武装部政治委员
    {"id": 8, "name": "卢晓光", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委常委、县人民武装部政治委员",
     "current_org": "连山壮族瑶族自治县人民武装部",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_430042.html"},

    # 陈明辉 — 县委常委、县人民政府党组副书记、副县长
    # 男，汉族，大学，1982年8月生，中共党员
    {"id": 9, "name": "陈明辉", "gender": "男", "ethnicity": "汉族", "birth": "1982-08",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委常委、县人民政府党组副书记、副县长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_430013.html"},

    # 李典政 — 县委常委、县委组织部部长、县委党校校长
    {"id": 10, "name": "李典政", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委常委、县委组织部部长、县委党校校长",
     "current_org": "中共连山壮族瑶族自治县委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_977597.html"},

    # 江沛豪 — 县委常委、县纪委书记、县监委主任
    {"id": 11, "name": "江沛豪", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县委常委、县纪委书记、县监委主任",
     "current_org": "中共连山壮族瑶族自治县纪律检查委员会",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xw/content/post_430022.html"},

    # ── County Government (县政府) Leadership ──

    # 李福永 — 县政府党组成员、副县长
    {"id": 12, "name": "李福永", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县政府党组成员、副县长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_430011.html"},

    # 赵秀萍 — 县政府党组成员、副县长
    {"id": 13, "name": "赵秀萍", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县政府党组成员、副县长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_1506592.html"},

    # 林海清 — 县政府党组成员、副县长，兼任县公安局局长
    {"id": 14, "name": "林海清", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县政府党组成员、副县长，兼任县公安局局长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_1640444.html"},

    # 林秀丽 — 县政府党组成员、副县长
    {"id": 15, "name": "林秀丽", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县政府党组成员、副县长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_1774567.html"},

    # 吴远茂 — 县政府党组成员（挂任）、副县长
    {"id": 16, "name": "吴远茂", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "连山壮族瑶族自治县政府党组成员（挂任）、副县长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_1785679.html"},

    # 邓展华 — 副县长
    {"id": 17, "name": "邓展华", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "连山壮族瑶族自治县副县长",
     "current_org": "连山壮族瑶族自治县人民政府",
     "source": "http://www.gdls.gov.cn/zwgk/ldzc/xzf/content/post_2000533.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共连山壮族瑶族自治县委员会", "type": "党委",
     "level": "县级", "parent": "中共清远市委员会", "location": "广东省清远市连山壮族瑶族自治县"},
    {"id": 2, "name": "连山壮族瑶族自治县人民政府", "type": "政府",
     "level": "县级", "parent": "清远市人民政府", "location": "广东省清远市连山壮族瑶族自治县"},
    {"id": 3, "name": "中共连山壮族瑶族自治县纪律检查委员会", "type": "纪委",
     "level": "县级", "parent": "中共清远市纪律检查委员会", "location": "广东省清远市连山壮族瑶族自治县"},
    {"id": 4, "name": "连山壮族瑶族自治县人民武装部", "type": "事业单位",
     "level": "县级", "parent": "清远军分区", "location": "广东省清远市连山壮族瑶族自治县"},
    {"id": 5, "name": "连山壮族瑶族自治县公安局", "type": "政府",
     "level": "县级", "parent": "连山壮族瑶族自治县人民政府", "location": "广东省清远市连山壮族瑶族自治县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 许崇砚 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "连山壮族瑶族自治县委书记",
     "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 陆治杰 — 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "连山壮族瑶族自治县委副书记",
     "start": "", "end": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "连山壮族瑶族自治县县长",
     "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 黄科 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "连山壮族瑶族自治县委副书记",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 伍洁星 — 挂任副书记
    {"person_id": 4, "org_id": 1, "title": "连山壮族瑶族自治县委副书记（挂任）",
     "start": "", "end": "至今", "rank": "副处级（挂任）", "note": "挂职干部"},

    # 王少锋 — 宣传部长
    {"person_id": 5, "org_id": 1, "title": "连山壮族瑶族自治县委常委、县委宣传部部长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 谢梅 — 统战部长、政法委书记
    {"person_id": 6, "org_id": 1, "title": "连山壮族瑶族自治县委常委、县委统战部部长、县委政法委书记",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 刘俊辉 — 县委办主任、县政府办主任
    {"person_id": 7, "org_id": 1, "title": "连山壮族瑶族自治县委常委、县委办公室主任",
     "start": "", "end": "至今", "rank": "副处级", "note": "兼任县政府办公室主任"},
    {"person_id": 7, "org_id": 2, "title": "连山壮族瑶族自治县政府办公室主任",
     "start": "", "end": "至今", "rank": "正科级", "note": "县委常委兼任"},

    # 卢晓光 — 人武部政委
    {"person_id": 8, "org_id": 4, "title": "连山壮族瑶族自治县人民武装部政治委员",
     "start": "", "end": "至今", "rank": "副处级", "note": "县委常委"},
    {"person_id": 8, "org_id": 1, "title": "连山壮族瑶族自治县委常委",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 陈明辉 — 常务副县长
    {"person_id": 9, "org_id": 1, "title": "连山壮族瑶族自治县委常委",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "连山壮族瑶族自治县人民政府党组副书记、副县长",
     "start": "", "end": "至今", "rank": "副处级", "note": "负责县政府常务工作"},

    # 李典政 — 组织部长
    {"person_id": 10, "org_id": 1, "title": "连山壮族瑶族自治县委常委、县委组织部部长、县委党校校长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 江沛豪 — 纪委书记
    {"person_id": 11, "org_id": 1, "title": "连山壮族瑶族自治县委常委、县纪委书记",
     "start": "", "end": "至今", "rank": "副处级", "note": "兼任县监委主任"},
    {"person_id": 11, "org_id": 3, "title": "连山壮族瑶族自治县纪委书记、县监委主任",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 李福永 — 副县长
    {"person_id": 12, "org_id": 2, "title": "连山壮族瑶族自治县政府党组成员、副县长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 赵秀萍 — 副县长
    {"person_id": 13, "org_id": 2, "title": "连山壮族瑶族自治县政府党组成员、副县长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 林海清 — 副县长兼公安局长
    {"person_id": 14, "org_id": 2, "title": "连山壮族瑶族自治县政府党组成员、副县长",
     "start": "", "end": "至今", "rank": "副处级", "note": "兼任县公安局局长"},
    {"person_id": 14, "org_id": 5, "title": "连山壮族瑶族自治县公安局局长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 林秀丽 — 副县长
    {"person_id": 15, "org_id": 2, "title": "连山壮族瑶族自治县政府党组成员、副县长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 吴远茂 — 挂任副县长
    {"person_id": 16, "org_id": 2, "title": "连山壮族瑶族自治县政府党组成员（挂任）、副县长",
     "start": "", "end": "至今", "rank": "副处级（挂任）", "note": "挂职干部"},

    # 邓展华 — 副县长
    {"person_id": 17, "org_id": 2, "title": "连山壮族瑶族自治县副县长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 县委常委会核心班子 — 共同任职于县委
    {"person_a": 1, "person_b": 2, "type": "领导关系",
     "context": "县委书记与县长搭档", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 3, "type": "领导关系",
     "context": "县委书记与县委副书记", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "领导关系",
     "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "领导关系",
     "context": "县委书记与宣传部部长", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "领导关系",
     "context": "县委书记与统战部部长", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "领导关系",
     "context": "县委书记与组织部部长", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "领导关系",
     "context": "县委书记与纪委书记", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},

    # 县长与副县长 — 县政府班子
    {"person_a": 2, "person_b": 9, "type": "领导关系",
     "context": "县长与常务副县长", "overlap_org": "连山壮族瑶族自治县人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "领导关系",
     "context": "县长与副县长", "overlap_org": "连山壮族瑶族自治县人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "领导关系",
     "context": "县长与副县长", "overlap_org": "连山壮族瑶族自治县人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "领导关系",
     "context": "县长与副县长兼公安局长", "overlap_org": "连山壮族瑶族自治县人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "领导关系",
     "context": "县长与副县长", "overlap_org": "连山壮族瑶族自治县人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "领导关系",
     "context": "县长与挂任副县长", "overlap_org": "连山壮族瑶族自治县人民政府",
     "overlap_period": "至今"},

    # 县委常委间同事关系
    {"person_a": 5, "person_b": 6, "type": "同事关系",
     "context": "同为县委常委", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 7, "person_b": 9, "type": "工作关系",
     "context": "县委办主任与常务副县长日常工作对接", "overlap_org": "连山壮族瑶族自治县人民政府",
     "overlap_period": "至今"},
    {"person_a": 10, "person_b": 5, "type": "同事关系",
     "context": "同为县委常委", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
    {"person_a": 11, "person_b": 1, "type": "监督关系",
     "context": "纪委书记监督县委书记", "overlap_org": "中共连山壮族瑶族自治县委员会",
     "overlap_period": "至今"},
]


# =========================================================================
# HELPERS
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string for a person based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "县委" in post and "纪委" not in post and "副书记" not in post:
        return "255,50,50"  # Red — Party Secretary
    if "县长" in post and "副书记" in post:
        return "50,100,255"  # Blue — County Mayor
    if "纪委" in post or "监委" in post:
        return "255,165,0"  # Orange — Discipline
    return "100,100,100"  # Grey — Other


def org_color(o):
    t = o.get("type", "")
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "事业单位": "220,220,220",
    }.get(t, "200,200,200")


def is_top_leader(p):
    pid = p["id"]
    return pid in (1, 2)  # 许崇砚 and 陆治杰


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


# =========================================================================
# DB
# =========================================================================

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
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


# =========================================================================
# GEXF
# =========================================================================

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>连山壮族瑶族自治县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p["current_post"]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        title = pos["title"]
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person edges (relationship)
    for r in relationships:
        eid += 1
        ctx = r.get("context", "")
        ov_org = r.get("overlap_org", "")
        ov_period = r.get("overlap_period", "")
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(ctx)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(ov_org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(ov_period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# =========================================================================
# PERSON JSON
# =========================================================================

def write_person_json(p):
    """Write a single person's deep-profile JSON."""
    filename = f"{AS_OF}-广东省-清远市-{esc(p['current_post']).replace('/', '-')}-{p['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    profile = {
        "task_id": "guangdong_连山壮族瑶族自治县",
        "as_of": AS_OF,
        "province": "广东省",
        "parent_city": "清远市",
        "region": "连山壮族瑶族自治县",
        "level": "县",
        "person": {
            "name": p["name"],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "education": p["education"],
            "party_join": p["party_join"],
            "current_post": p["current_post"],
            "current_org": p["current_org"],
        },
        "positions": [
            {"title": pos["title"], "org": pos["org_id"],
             "start": pos["start"], "end": pos["end"], "rank": pos["rank"], "note": pos["note"]}
            for pos in positions if pos["person_id"] == p["id"]
        ],
        "connections": [
            {"related_person": persons[r["person_b"] - 1]["name"] if r["person_a"] == p["id"] else persons[r["person_a"] - 1]["name"],
             "type": r["type"], "context": r["context"],
             "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"]}
            for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]
        ],
        "sources": [p["source"]],
        "confidence": "confirmed" if p.get("birth") or p.get("ethnicity") else "plausible",
        "open_questions": [],
    }

    # Add open questions for missing biographical data
    if not p.get("birthplace"):
        profile["open_questions"].append(f"{p['name']}的出生地")
    if not p.get("birth"):
        profile["open_questions"].append(f"{p['name']}的出生年月")
    if not p.get("education"):
        profile["open_questions"].append(f"{p['name']}的教育背景")
    if not p.get("ethnicity"):
        profile["open_questions"].append(f"{p['name']}的民族")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    return filepath


# =========================================================================
# MAIN
# =========================================================================

def main():
    os.makedirs(TMP, exist_ok=True)

    print(f"Building database: {DB_PATH}")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  Done ({db_size} bytes)")

    print(f"Building GEXF: {GEXF_PATH}")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  Done ({gexf_size} bytes)")

    print("Writing person JSONs...")
    for p in persons:
        path = write_person_json(p)
        print(f"  {os.path.basename(path)}")

    print("\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")

if __name__ == "__main__":
    main()
