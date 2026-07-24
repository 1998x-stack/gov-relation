#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 桦川县 (Huachuan County) leadership network.

Investigation date: 2026-07-24
Task ID: heilongjiang_桦川县
"""

import sqlite3
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

# ══════════════════════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════════════════════

SLUG = "桦川县"
AS_OF = "2026-07-24"
TASK_ID = "heilongjiang_桦川县"

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ══════════════════════════════════════════════════════════════════════════════
# Data - Persons
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Party Secretary (县委书记) ──
    {
        "id": 1,
        "name": "范继涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "",
        "education": "省委党校班经济管理专业研究生",
        "party_join": "中共党员",
        "work_start": "1995-08",
        "current_post": "桦川县委书记",
        "current_org": "中共桦川县委员会",
        "source": "https://www.huachuan.gov.cn/hcx/c100013/202502/c04_228672.shtml",
    },
    # ── County Mayor (县长) ──
    {
        "id": 2,
        "name": "李水泉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-03",
        "birthplace": "",
        "education": "佳木斯大学思想政治教育专业硕士研究生",
        "party_join": "中共党员",
        "work_start": "2002-10",
        "current_post": "桦川县委副书记、政府县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100013/202201/c04_228649.shtml",
    },
    # ── Standing Committee Members ──
    {
        "id": 3,
        "name": "张淑芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桦川县委常委、纪委书记、监委主任",
        "current_org": "中共桦川县纪律检查委员会",
        "source": "https://www.huachuan.gov.cn/hcx/c100013/202306/c04_228661.shtml",
    },
    {
        "id": 4,
        "name": "韩天甲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-03",
        "birthplace": "",
        "education": "澳大利亚新英格兰大学计算机科学专业 研究生工学硕士",
        "party_join": "中共党员",
        "work_start": "2010-09",
        "current_post": "桦川县委常委、政府副县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100013/202411/c04_228668.shtml",
    },
    {
        "id": 5,
        "name": "王跃金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1996-11",
        "current_post": "桦川县委常委、政法委书记",
        "current_org": "中共桦川县委员会政法委员会",
        "source": "https://www.huachuan.gov.cn/hcx/c100013/202201/c04_228652.shtml",
    },
    {
        "id": 6,
        "name": "周建伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县委常委",
        "current_org": "中共桦川县委员会",
        "source": "https://www.huachuan.gov.cn/hcx/c100012/ldzc.shtml",
    },
    {
        "id": 7,
        "name": "边晓飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1993-12",
        "current_post": "桦川县委常委、人民武装部政委",
        "current_org": "桦川县人民武装部",
        "source": "https://www.huachuan.gov.cn/hcx/c100013/202306/c04_228660.shtml",
    },
    {
        "id": 8,
        "name": "曹哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-04",
        "birthplace": "",
        "education": "大学，农业推广硕士",
        "party_join": "中共党员",
        "work_start": "1998-09",
        "current_post": "桦川县委常委、组织部部长",
        "current_org": "中共桦川县委员会组织部",
        "source": "https://www.huachuan.gov.cn/hcx/c100013/202406/c04_228666.shtml",
    },
    {
        "id": 9,
        "name": "朱虹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县委常委、政府副县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100012/ldzc.shtml",
    },
    {
        "id": 10,
        "name": "冯宇墨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县委常委（挂职）",
        "current_org": "中共桦川县委员会",
        "source": "https://www.huachuan.gov.cn/hcx/c100012/ldzc.shtml",
    },
    {
        "id": 11,
        "name": "周淼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县委常委、宣传部部长",
        "current_org": "中共桦川县委员会宣传部",
        "source": "https://www.huachuan.gov.cn/hcx/c100012/ldzc.shtml",
    },
    # ── Deputy County Mayors ──
    {
        "id": 12,
        "name": "原传栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县人民政府副县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100015/202308/c04_228746.shtml",
    },
    {
        "id": 13,
        "name": "孔祥林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县人民政府副县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100015/202312/c04_228789.shtml",
    },
    {
        "id": 14,
        "name": "梅雪松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县人民政府副县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100015/202412/c04_228962.shtml",
    },
    {
        "id": 15,
        "name": "赵光辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县人民政府副县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100015/202503/c04_229003.shtml",
    },
    {
        "id": 16,
        "name": "贺立峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县人民政府副县长",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100015/202505/c04_229064.shtml",
    },
    {
        "id": 17,
        "name": "何飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县人民政府副县长（挂职）",
        "current_org": "桦川县人民政府",
        "source": "https://www.huachuan.gov.cn/hcx/c100015/202411/c04_228921.shtml",
    },
    # ──人大领导──
    {
        "id": 18,
        "name": "孙国炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县人大常委会主任",
        "current_org": "桦川县人民代表大会常务委员会",
        "source": "https://www.huachuan.gov.cn/hcx/c100014/202201/c04_228678.shtml",
    },
    # ──政协领导──
    {
        "id": 19,
        "name": "胡婧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桦川县政协主席",
        "current_org": "中国人民政治协商会议桦川县委员会",
        "source": "https://www.huachuan.gov.cn/hcx/c100016/202201/c04_229078.shtml",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# Data - Organizations
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共桦川县委员会", "type": "党委", "level": "县处级", "parent": "中共佳木斯市委员会", "location": "桦川县"},
    {"id": 2, "name": "桦川县人民政府", "type": "政府", "level": "县处级", "parent": "佳木斯市人民政府", "location": "桦川县"},
    {"id": 3, "name": "中共桦川县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共桦川县委员会", "location": "桦川县"},
    {"id": 4, "name": "中共桦川县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共桦川县委员会", "location": "桦川县"},
    {"id": 5, "name": "桦川县人民武装部", "type": "政府", "level": "县处级", "parent": "", "location": "桦川县"},
    {"id": 6, "name": "中共桦川县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共桦川县委员会", "location": "桦川县"},
    {"id": 7, "name": "中共桦川县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共桦川县委员会", "location": "桦川县"},
    {"id": 8, "name": "桦川县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "桦川县"},
    {"id": 9, "name": "中国人民政治协商会议桦川县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "桦川县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# Data - Positions
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "桦川县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "主持县委全面工作"},
    # County Mayor
    {"person_id": 2, "org_id": 1, "title": "桦川县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "桦川县人民政府县长", "start": "", "end": "present", "rank": "县处级正职", "note": "主持县政府全面工作；黑龙江省第十四届人大代表"},
    # Standing Committee
    {"person_id": 3, "org_id": 3, "title": "桦川县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": "四级高级监察官"},
    {"person_id": 4, "org_id": 2, "title": "桦川县委常委、政府副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责县政府常务工作"},
    {"person_id": 5, "org_id": 4, "title": "桦川县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "桦川县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "桦川县委常委、人民武装部政委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "桦川县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "桦川县委常委、政府副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "桦川县委常委（挂职）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 11, "org_id": 7, "title": "桦川县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # Deputy County Mayors
    {"person_id": 12, "org_id": 2, "title": "桦川县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "桦川县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "桦川县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "桦川县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "桦川县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "桦川县人民政府副县长（挂职）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    # 人大
    {"person_id": 18, "org_id": 8, "title": "桦川县人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 政协
    {"person_id": 19, "org_id": 9, "title": "桦川县政协主席", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# Data - Relationships
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 书记-县长 工作搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政正职搭档", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    # 书记-常委 班子成员
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委班子", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委班子", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委班子", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委班子", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委班子", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委班子", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委班子", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    # 县长-副县长 政府班子
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县政府班子，韩天甲协助县长分管审计局", "overlap_org": "桦川县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县政府班子", "overlap_org": "桦川县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县政府班子", "overlap_org": "桦川县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县政府班子", "overlap_org": "桦川县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县政府班子", "overlap_org": "桦川县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县政府班子", "overlap_org": "桦川县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县政府班子", "overlap_org": "桦川县人民政府", "overlap_period": "至今"},
    # 纪委-县委 监督关系
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate", "context": "纪委书记在县委领导下工作", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
    # 组织部长-书记 干部管理
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate", "context": "组织部在县委领导下负责干部工作", "overlap_org": "中共桦川县委员会", "overlap_period": "至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else ""

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")
    
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    
    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return ("255,50,50", 20.0)
    elif "县长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    elif "副" in post and ("县长" in post or "书记" in post) and "常委" in post:
        return ("100,150,255", 15.0)
    elif "副" in post and ("县长" in post or "书记" in post):
        return ("100,150,255", 12.0)
    elif "常委" in post:
        return ("100,150,255", 12.0)
    elif "人大" in post:
        return ("200,255,255", 12.0)
    elif "政协" in post:
        return ("255,240,200", 12.0)
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>桦川县领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"桦川县人民政府—领导之窗（县委领导）","url":"https://www.huachuan.gov.cn/hcx/c100012/ldzc.shtml","publisher":"桦川县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县委、人大、政府、政协领导名单"},
        {"id":"S002","title":"范继涛—桦川县委书记简历","url":"https://www.huachuan.gov.cn/hcx/c100013/202502/c04_228672.shtml","publisher":"桦川县人民政府","published_at":"2025-02-28","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1972年7月生，1995年8月参加工作，省委党校研究生"},
        {"id":"S003","title":"李水泉—桦川县委副书记、县长简历","url":"https://www.huachuan.gov.cn/hcx/c100013/202201/c04_228649.shtml","publisher":"桦川县人民政府","published_at":"2022-01-21","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1980年3月生，2002年10月参加工作，佳木斯大学硕士"},
        {"id":"S004","title":"李水泉—桦川县政府县长简历","url":"https://www.huachuan.gov.cn/hcx/c100015/202201/c04_228716.shtml","publisher":"桦川县人民政府","published_at":"2022-01-21","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1980年3月生，法学硕士"},
        {"id":"S005","title":"张淑芬—桦川县委常委、纪委书记简历","url":"https://www.huachuan.gov.cn/hcx/c100013/202306/c04_228661.shtml","publisher":"桦川县人民政府","published_at":"2023-06-30","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1973年6月生，大学学历"},
        {"id":"S006","title":"韩天甲—桦川县委常委、政府副县长简历","url":"https://www.huachuan.gov.cn/hcx/c100013/202411/c04_228668.shtml","publisher":"桦川县人民政府","published_at":"2024-11-30","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1985年3月生，澳大利亚新英格兰大学计算机科学硕士"},
        {"id":"S007","title":"王跃金—桦川县委常委、政法委书记简历","url":"https://www.huachuan.gov.cn/hcx/c100013/202201/c04_228652.shtml","publisher":"桦川县人民政府","published_at":"2022-01-21","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1975年2月生，1996年11月参加工作"},
        {"id":"S008","title":"边晓飞—桦川县委常委、人武部政委简历","url":"https://www.huachuan.gov.cn/hcx/c100013/202306/c04_228660.shtml","publisher":"桦川县人民政府","published_at":"2023-06-30","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1975年9月生，1993年12月参加工作"},
        {"id":"S009","title":"曹哲—桦川县委常委、组织部部长简历","url":"https://www.huachuan.gov.cn/hcx/c100013/202406/c04_228666.shtml","publisher":"桦川县人民政府","published_at":"2024-06-30","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"1979年4月生，1998年9月参加工作，农业推广硕士"},
        {"id":"S010","title":"范继涛调研全县稻米产业发展情况","url":"https://www.huachuan.gov.cn/hcx/c100001/202607/c04_306515.shtml","publisher":"桦川县人民政府","published_at":"2026-07-23","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县委书记范继涛调研活动报道"},
        {"id":"S011","title":"李水泉深入督导检查防汛备汛","url":"https://www.huachuan.gov.cn/hcx/c100001/202607/c04_305714.shtml","publisher":"桦川县人民政府","published_at":"2026-07-13","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县长李水泉防汛检查，韩天甲参加"},
    ]


def make_person_json(p, timeline, relationships_list, src_reg):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "桦川县",
            "job": p["current_post"],
            "task_id": TASK_ID,
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"huachuan_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if ("县委书记" in p["current_post"] or ("县长" in p["current_post"] and "副" not in p["current_post"])) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": []
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
        "risk_and_integrity_signals": [{"type":"none_found","description":"No negative media or disciplinary signals found in official records as of investigation date.","date":"","confidence":"unverified","source_ids":[]}],
        "source_register": src_reg,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "详细履历缺失——缺乏上任时间和此前任职信息"
        },
        "open_questions": [
            {"priority":"high","question":"范继涛担任桦川县委书记的具体上任时间？此前的任职经历？","why_it_matters":"建立完整履历时间线","suggested_queries":["范继涛 简历","范继涛 任职 桦川"],"last_attempted":AS_OF},
            {"priority":"high","question":"李水泉担任桦川县长的具体上任时间？此前的任职经历？","why_it_matters":"建立完整履历时间线","suggested_queries":["李水泉 简历","李水泉 桦川"],"last_attempted":AS_OF},
            {"priority":"medium","question":"桦川县的前任县委书记是谁？调往何处？","why_it_matters":"建立前后任关系","suggested_queries":["桦川县委 前任书记","桦川县委书记 任职"],"last_attempted":AS_OF},
            {"priority":"medium","question":"桦川县的前任县长是谁？调往何处？","why_it_matters":"建立前后任关系","suggested_queries":["桦川县长 前任","桦川县人民政府 县长 任免"],"last_attempted":AS_OF},
        ]
    }
    return result


def write_person_json(p, timeline, relationships_list, src_reg):
    import json
    data = make_person_json(p, timeline, relationships_list, src_reg)
    fname = f"{AS_OF}-黑龙江省-佳木斯市-{p['current_post'].replace('桦川','')}-{p['name']}.json"
    fpath = os.path.join(STAGING_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  JSON: {fpath}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} leadership network...")
    
    build_db()
    build_gexf()
    
    src_reg = make_source_register()
    
    # Person JSONs for core figures
    # 范继涛 - 县委书记
    fan_timeline = [
        {"start":"unknown","end":"2025","org":"未知","title":"此前任职","level":"","location":"","system":"other","rank":"","is_key_promotion":False,"notes":"公开资料未找到范继涛任桦川县委书记前的完整履历","confidence":"unverified","source_ids":["S002"]},
        {"start":"2025","end":"present","org":"中共桦川县委员会","title":"桦川县委书记","level":"县处级正职","location":"桦川县","system":"party","rank":"正处级","is_key_promotion":True,"notes":"主持县委全面工作","confidence":"confirmed","source_ids":["S002","S010"]},
    ]
    fan_relationships = [
        {"person":"李水泉","person_id":"huachuan_李水泉","relationship_type":"superior_subordinate","strength":"strong","evidence":"县委书记与县长党政正职搭档","overlap_org":"中共桦川县委员会","overlap_period":"至今","direction":"person_to_other","confidence":"confirmed","source_ids":["S001"]},
        {"person":"张淑芬","person_id":"huachuan_张淑芬","relationship_type":"superior_subordinate","strength":"strong","evidence":"县委班子共同工作","overlap_org":"中共桦川县委员会","overlap_period":"至今","direction":"person_to_other","confidence":"confirmed","source_ids":["S001"]},
        {"person":"韩天甲","person_id":"huachuan_韩天甲","relationship_type":"superior_subordinate","strength":"strong","evidence":"县委班子共同工作","overlap_org":"中共桦川县委员会","overlap_period":"至今","direction":"person_to_other","confidence":"confirmed","source_ids":["S001"]},
    ]
    write_person_json(persons[0], fan_timeline, fan_relationships, src_reg)
    
    # 李水泉 - 县长
    li_timeline = [
        {"start":"unknown","end":"2022","org":"未知","title":"此前任职","level":"","location":"","system":"other","rank":"","is_key_promotion":False,"notes":"公开资料未找到李水泉任桦川县长前的完整履历","confidence":"unverified","source_ids":["S003","S004"]},
        {"start":"2022","end":"present","org":"桦川县人民政府","title":"桦川县委副书记、政府县长","level":"县处级正职","location":"桦川县","system":"government","rank":"正处级","is_key_promotion":True,"notes":"主持县政府全面工作。黑龙江省第十四届人大代表。","confidence":"confirmed","source_ids":["S003","S004","S011"]},
    ]
    li_relationships = [
        {"person":"范继涛","person_id":"huachuan_范继涛","relationship_type":"superior_subordinate","strength":"strong","evidence":"县委书记与县长党政正职搭档","overlap_org":"中共桦川县委员会","overlap_period":"至今","direction":"other_to_person","confidence":"confirmed","source_ids":["S001"]},
        {"person":"韩天甲","person_id":"huachuan_韩天甲","relationship_type":"superior_subordinate","strength":"strong","evidence":"韩天甲协助县长分管审计局","overlap_org":"桦川县人民政府","overlap_period":"至今","direction":"person_to_other","confidence":"confirmed","source_ids":["S006","S011"]},
    ]
    write_person_json(persons[1], li_timeline, li_relationships, src_reg)
    
    print(f"\n{SLUG} build complete!")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  JSONs: {STAGING_DIR}/")

if __name__ == "__main__":
    main()
