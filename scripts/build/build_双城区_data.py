#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 双城区 (Shuangcheng District), 哈尔滨市, 黑龙江省.

Investigation date: 2026-07-29
Task ID: heilongjiang_双城区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources (primary, all official):
  - 双城区人民政府官网·领导信息  http://www.hrbsc.gov.cn/hebscq/c111355/ldxx.shtml  (刘启嘉)
  - 区长邹永强简历页  http://www.hrbsc.gov.cn/hebscq/c110671/ldxx.shtml
  - 徐鑫 简历页 http://www.hrbsc.gov.cn/hebscq/c111357/ldxx.shtml
  - 赵云鹏 简历页 http://www.hrbsc.gov.cn/hebscq/c111365/ldxx.shtml
  - 李艳秋（人大主任）http://www.hrbsc.gov.cn/hebscq/c111368/ldxx.shtml
  - 孙德新（政协主席）http://www.hrbsc.gov.cn/hebscq/sdx/ldxx.shtml
  - 区官网新闻（确认邹永强区长）http://www.hrbsc.gov.cn/hebscq/c110686/202602/c01_1137842.shtml

As-of: 2026-07

Confirmed:
  - 刘启嘉：区委书记（2023.06至今）— 纪检/外事系统出身
  - 邹永强：区委副书记、区长、经开区管委会主任（2026.01至今）— 阿城区系统出身（跨区轮岗）
  - 徐鑫（区委副书记）、李艳秋（区人大主任）、孙德新（区政协主席）、殷雷/赵云鹏（副区长）：confirmed via 官网简历

Gaps:
  - 前任区委书记（2023.06前）姓名/去向待查
  - 前任区长 赫彦明（官网旧稿列名，2026.01被邹永强接任）去向待核
  - 各核心人物出生/籍贯/学历字段未在官网简历公开
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "双城区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-29"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "刘启嘉", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "1993.12",
     "current_post": "区委书记", "current_org": "中共哈尔滨市双城区委员会",
     "source": "http://www.hrbsc.gov.cn/hebscq/c111355/ldxx.shtml"},
    {"id": 2, "name": "邹永强", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "1999.07",
     "current_post": "区委副书记、区长、经开区管委会主任", "current_org": "双城区人民政府",
     "source": "http://www.hrbsc.gov.cn/hebscq/c110671/ldxx.shtml"},
    {"id": 3, "name": "徐鑫", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "1995.07",
     "current_post": "区委副书记", "current_org": "中共哈尔滨市双城区委员会",
     "source": "http://www.hrbsc.gov.cn/hebscq/c111357/ldxx.shtml"},
    {"id": 4, "name": "李艳秋", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组书记、主任", "current_org": "双城区人民代表大会常务委员会",
     "source": "http://www.hrbsc.gov.cn/hebscq/c111368/ldxx.shtml"},
    {"id": 5, "name": "孙德新", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "1994.03",
     "current_post": "区政协党组书记、主席", "current_org": "中国人民政治协商会议哈尔滨市双城区委员会",
     "source": "http://www.hrbsc.gov.cn/hebscq/sdx/ldxx.shtml"},
    {"id": 6, "name": "殷雷", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "蚌埠坦克学院（指挥）、东北农业大学（在职硕士）", "party_join": "中共党员", "work_start": "1998.12",
     "current_post": "区委常委、区政府副区长", "current_org": "双城区人民政府",
     "source": "http://www.hrbsc.gov.cn/hebscq/c111362/ldxx.shtml"},
    {"id": 7, "name": "赵云鹏", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "1997.10",
     "current_post": "区委常委、区政府副区长", "current_org": "双城区人民政府",
     "source": "http://www.hrbsc.gov.cn/hebscq/c111365/ldxx.shtml"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共哈尔滨市双城区委员会", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委员会", "location": "双城区"},
    {"id": 2, "name": "双城区人民政府", "type": "政府", "level": "区级", "parent": "哈尔滨市人民政府", "location": "双城区"},
    {"id": 3, "name": "双城区人民代表大会常务委员会", "type": "人大", "level": "区级", "parent": "哈尔滨市人大常委会", "location": "双城区"},
    {"id": 4, "name": "中国人民政治协商会议哈尔滨市双城区委员会", "type": "政协", "level": "区级", "parent": "哈尔滨市政协", "location": "双城区"},
    {"id": 5, "name": "双城经济开发区管委会", "type": "开发区", "level": "区级", "parent": "双城区人民政府", "location": "双城区"},
    {"id": 6, "name": "哈尔滨市纪委市监委", "type": "纪委", "level": "市级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 7, "name": "哈尔滨市政府外事侨务办公室", "type": "政府", "level": "市级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市"},
    {"id": 8, "name": "道外区（区委）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 9, "name": "道里区（区委）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 10, "name": "阿城区（区委/区政府）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 11, "name": "延寿县（县委）", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 12, "name": "巴彦县（县委）", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 13, "name": "木兰县（县委）", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 14, "name": "呼兰区（区委）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市"},
    {"id": 15, "name": "哈尔滨市农业农村局", "type": "政府", "level": "市级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市"},
    {"id": 16, "name": "哈尔滨市城市管理局", "type": "政府", "level": "市级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市"},
]

# ── Positions (career timeline) ────────────────────────────────────────────
positions = [
    # 刘启嘉 — 纪检/外事系统
    {"person_id": 1, "org_id": 7, "title": "外事侨务办公室科员、副主任科员", "start_date": "1993.12", "end_date": "1996.10", "rank": "科员级", "note": "松花江地区"},
    {"person_id": 1, "org_id": 7, "title": "领事处副主任科员、主任科员、副处长", "start_date": "1996.10", "end_date": "2010.03", "rank": "副处", "note": "市政府外事侨务办"},
    {"person_id": 1, "org_id": 7, "title": "纪检组副组长、监察室主任", "start_date": "2010.03", "end_date": "2014.07", "rank": "正处", "note": "市政府外事侨务办"},
    {"person_id": 1, "org_id": 8, "title": "道外区委常委、纪委书记", "start_date": "2015.04", "end_date": "2016.11", "rank": "副区级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "道里区委常委、纪委书记、区监委主任", "start_date": "2016.11", "end_date": "2019.09", "rank": "副区级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "市纪委副书记、市监委副主任", "start_date": "2019.09", "end_date": "2023.06", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "双城区委书记", "start_date": "2023.06", "end_date": "present", "rank": "正处级", "note": "主持区委全面工作"},

    # 邹永强 — 阿城区→双城区
    {"person_id": 2, "org_id": 10, "title": "阿城第八中学教师", "start_date": "1999.07", "end_date": "2000.03", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "市政府办（信访办）科员", "start_date": "2000.03", "end_date": "2003.05", "rank": "科员", "note": "阿城"},
    {"person_id": 2, "org_id": 10, "title": "区政府办公室研究室主任", "start_date": "2003.05", "end_date": "2010.07", "rank": "正科", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区招商局副局长", "start_date": "2010.07", "end_date": "2012.02", "rank": "副科", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区委办公室副主任", "start_date": "2012.02", "end_date": "2017.11", "rank": "副处", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区委办公室副主任、区委保密委员会专职副主任", "start_date": "2017.11", "end_date": "2019.01", "rank": "副处", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区委办公室副主任、区委保密和机要局局长", "start_date": "2019.01", "end_date": "2020.06", "rank": "副处", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区政府党组成员、政府办公室主任", "start_date": "2020.06", "end_date": "2021.10", "rank": "正处", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区政府副区长", "start_date": "2021.10", "end_date": "2025.04", "rank": "副处", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区委常委、区政府副区长", "start_date": "2025.04", "end_date": "2025.07", "rank": "副处", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区委常委、区政府常务副区长", "start_date": "2025.07", "end_date": "2025.10", "rank": "副处", "note": "阿城区"},
    {"person_id": 2, "org_id": 10, "title": "区委常委、常务副区长、兼蜚克图街道党工委书记", "start_date": "2025.10", "end_date": "2026.01", "rank": "副处", "note": "阿城区"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区政府区长", "start_date": "2026.01", "end_date": "present", "rank": "正处级", "note": "兼经开区管委会主任"},

    # 徐鑫 — 延寿县→双城
    {"person_id": 3, "org_id": 11, "title": "延寿县六团镇财政所干部、团委书记、武装部长", "start_date": "1995.07", "end_date": "2011.09", "rank": "科员→正科", "note": "含乡镇多岗"},
    {"person_id": 3, "org_id": 2, "title": "双城区（市）人民政府副市长", "start_date": "2011.10", "end_date": "2015.04", "rank": "副县级", "note": "时为双城市"},
    {"person_id": 3, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "2015.04", "end_date": "2016.11", "rank": "副处", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "2016.11", "end_date": "2019.08", "rank": "副处", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "区委常委、区政府常务副区长", "start_date": "2019.08", "end_date": "2021.10", "rank": "副处", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "2021.10", "end_date": "present", "rank": "副区级", "note": ""},

    # 李艳秋 — 人大主任
    {"person_id": 4, "org_id": 13, "title": "木兰县委常委、宣传部部长", "start_date": "2006.11", "end_date": "2010.05", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 12, "title": "巴彦县委常委、组织部部长", "start_date": "2010.05", "end_date": "2011.09", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "2011.09", "end_date": "2016.11", "rank": "副区", "note": "双城区（市）"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、政府副区长", "start_date": "2016.11", "end_date": "2020.06", "rank": "副区", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "2020.06", "end_date": "2021.10", "rank": "副区级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "区人大常委会党组书记、主任", "start_date": "2021.10", "end_date": "present", "rank": "正处级", "note": ""},

    # 孙德新 — 政协主席
    {"person_id": 5, "org_id": 16, "title": "市城管局村镇环境监督指导处处长", "start_date": "2015.06", "end_date": "2019.04", "rank": "正处", "note": "哈尔滨市城管局"},
    {"person_id": 5, "org_id": 16, "title": "市城管局副局长、党组成员", "start_date": "2019.04", "end_date": "2025.12", "rank": "副局级", "note": "哈尔滨市城管局"},
    {"person_id": 5, "org_id": 4, "title": "区政协党组书记、主席", "start_date": "2025.12", "end_date": "present", "rank": "正处级", "note": ""},

    # 殷雷 — 军队转业 / 副区长
    {"person_id": 6, "org_id": 15, "title": "哈尔滨市农业农村局副局长、党组成员", "start_date": "2024.06", "end_date": "2025.04", "rank": "副局级", "note": "军队转业→市级农口"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、区政府副区长", "start_date": "2025.04", "end_date": "present", "rank": "副区级", "note": ""},

    # 赵云鹏 — 呼兰区→市信访局→双城
    {"person_id": 7, "org_id": 14, "title": "呼兰区孟家乡党委副书记、乡长/方台镇党委书记", "start_date": "2010.11", "end_date": "2014.04", "rank": "正科", "note": "呼兰区"},
    {"person_id": 7, "org_id": 6, "title": "哈尔滨市信访局驻京处→副局长", "start_date": "2014.04", "end_date": "2024.07", "rank": "副局级", "note": "哈尔滨市信访局"},
    {"person_id": 7, "org_id": 2, "title": "区委常委、区政府副区长", "start_date": "2024.07", "end_date": "present", "rank": "副区级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记刘启嘉与区长邹永强党政主要领导搭档", "overlap_org": "中共哈尔滨市双城区委员会", "overlap_period": "2026.01至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记徐鑫党委班子共事", "overlap_org": "中共哈尔滨市双城区委员会", "overlap_period": "2023.06至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与人大主任共事", "overlap_org": "双城区四套班子", "overlap_period": "2023.06至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与区委副书记徐鑫在区班子共事", "overlap_org": "双城区", "overlap_period": "2026.01至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长与政协主席孙德新共事", "overlap_org": "双城区", "overlap_period": "2026.01至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长领导副区长殷雷", "overlap_org": "双城区人民政府", "overlap_period": "2026.01至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长领导副区长赵云鹏", "overlap_org": "双城区人民政府", "overlap_period": "2026.01至今"},
    {"person_a": 4, "person_b": 7, "type": "cross_region_transfer", "context": "同为哈尔滨市域内区县际轮岗干部（巴彦/呼兰背景）", "overlap_org": "哈尔滨市干部交流网络", "overlap_period": ""},
]


# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    if name == "刘启嘉": return "255,50,50"
    if name == "邹永强": return "50,100,255"
    if name == "徐鑫": return "255,165,0"
    if name == "李艳秋": return "200,255,255"
    if name == "孙德新": return "255,240,200"
    if name in ("殷雷", "赵云鹏"): return "100,140,255"
    return "100,100,100"


def person_size(name):
    if name in ("刘启嘉", "邹永强"): return "20.0"
    if name in ("徐鑫", "李艳秋", "孙德新"): return "14.0"
    return "12.0"


def org_color(t):
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    if "纪委" in t: return "255,180,180"
    if "开发区" in t: return "200,255,200"
    return "200,200,200"


# ── Database ──────────────────────────────────────────────────────────────
def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p.get("gender"), p.get("ethnicity"), p.get("birth"), p.get("birthplace"),
                     p.get("education"), p.get("party_join"), p.get("work_start"), p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ── GEXF ──────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>哈尔滨市双城区领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"]); sz = person_size(p["name"]); pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"]); oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues><attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/></attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues><attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/></attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ── Person Graph JSON ─────────────────────────────────────────────────────
SOURCE_REGISTER = [
    {"id": "S001", "title": "双城区政府官网·区委书记 刘启嘉", "url": "http://www.hrbsc.gov.cn/hebscq/c511355/ldxx.shtml", "publisher": "双城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "完整简历"},
    {"id": "S002", "title": "双城区政府官网·区长 邹永强", "url": "http://www.hrbsc.gov.cn/hebscq/c110671/ldxx.shtml", "publisher": "双城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "完整简历"},
    {"id": "S003", "title": "双城区政府官网·区委副书记 徐鑫", "url": "http://www.hrbsc.gov.cn/hebscq/c111357/ldxx.shtml", "publisher": "双城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S004", "title": "双城区政府官网·区人大主任 李艳秋", "url": "http://www.hrbsc.gov.cn/hebscq/c111368/ldxx.shtml", "publisher": "双城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S005", "title": "双城区政府官网·区政协主席 孙德新", "url": "http://www.hrbsc.gov.cn/hebscq/sdx/ldxx.shtml", "publisher": "双城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S006", "title": "双城区政府官网·副区长 赵云鹏", "url": "http://www.hrbsc.gov.cn/hebscq/c111365/ldxx.shtml", "publisher": "双城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S007", "title": "双城区政府官网·副区长 殷雷", "url": "http://www.hrbsc.gov.cn/hebscq/c111362/ldxx.shtml", "publisher": "双城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S008", "title": "双城区政府官网新闻·区长邹永强走访一线", "url": "http://www.hrbsc.gov.cn/hebscq/c110686/202602/c01_1137842.shtml", "publisher": "双城区人民政府", "published_at": "2026-02-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认邹永强区长"},
]

_FULL_TIMELINES = {
    1: [
        {"start": "1993.12", "end": "1996.10", "org": "松花江地区外事侨务办公室", "title": "科员、副主任科员", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1996.10", "end": "2010.03", "org": "哈尔滨市政府外事侨务办公室", "title": "领事处副主任科员、主任科员、副处长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2010.03", "end": "2014.07", "org": "哈尔滨市政府外事侨务办纪检组", "title": "纪检组副组长、监察室主任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2015.04", "end": "2016.11", "org": "道外区", "title": "区委常委、纪委书记", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2016.11", "end": "2019.09", "org": "道里区", "title": "区委常委、纪委书记、区监委主任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2019.09", "end": "2023.06", "org": "哈尔滨市纪委市监委", "title": "市纪委副书记、市监委副主任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023.06", "end": "present", "org": "中共哈尔滨市双城区委员会", "title": "区委书记", "confidence": "confirmed", "source_ids": ["S001"]},
    ],
    2: [
        {"start": "1999.07", "end": "2000.03", "org": "阿城第八中学", "title": "教师", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2000.03", "end": "2003.05", "org": "阿城市政府办（信访办）", "title": "科员", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2003.05", "end": "2010.07", "org": "阿城区政府办公室", "title": "研究室主任", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2010.07", "end": "2012.02", "org": "阿城区招商局", "title": "副局长", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2012.02", "end": "2020.06", "org": "阿城区委办公室", "title": "副主任（含保密/机要局长）", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2020.06", "end": "2021.10", "org": "阿城区政府", "title": "党组成员、政府办公室主任", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2021.10", "end": "2025.04", "org": "阿城区政府", "title": "副区长", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2025.04", "end": "2026.01", "org": "阿城区委", "title": "区委常委、常务副区长", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2026.01", "end": "present", "org": "双城区人民政府", "title": "区长（区委副书记，兼经开区管委会主任）", "confidence": "confirmed", "source_ids": ["S002", "S008"]},
    ],
}

_DEPUTY_TIMELINES = {
    3: [
        {"start": "1995.07", "end": "2011.09", "org": "延寿县六团镇", "title": "财政所干部、团委书记、武装部长", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2011.10", "end": "2015.04", "org": "双城区（市）人民政府", "title": "副市长", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2015.04", "end": "2019.08", "org": "中共双城区委", "title": "区委常委、统战/政法委书记", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2019.08", "end": "2021.10", "org": "双城区人民政府", "title": "区委常委、常务副区长", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2021.10", "end": "present", "org": "中共双城区委", "title": "区委副书记", "confidence": "confirmed", "source_ids": ["S003"]},
    ],
    4: [
        {"start": "2011.09", "end": "2016.11", "org": "中共双城区委", "title": "区委常委、组织部部长", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2016.11", "end": "2020.06", "org": "双城区人民政府", "title": "区委常委、副区长", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2020.06", "end": "2021.10", "org": "中共双城区委", "title": "区委副书记", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2021.10", "end": "present", "org": "双城区人民代表大会常务委员会", "title": "党组书记、主任", "confidence": "confirmed", "source_ids": ["S004"]},
    ],
    5: [
        {"start": "2015.06", "end": "2019.04", "org": "哈尔滨市城管局", "title": "村镇环境监督指导处处长", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2019.04", "end": "2025.12", "org": "哈尔滨市城市管理局", "title": "副局长、党组成员", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2025.12", "end": "present", "org": "双城区政协", "title": "区政协党组书记、主席", "confidence": "confirmed", "source_ids": ["S005"]},
    ],
    6: [
        {"start": "2024.06", "end": "2025.04", "org": "哈尔滨市农业农村局", "title": "副局长、党组成员", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2025.04", "end": "present", "org": "双城区人民政府", "title": "区委常委、副区长", "confidence": "confirmed", "source_ids": ["S007"]},
    ],
    7: [
        {"start": "2014.04", "end": "2024.07", "org": "哈尔滨市信访局", "title": "驻京处长→副局长", "confidence": "confirmed", "source_ids": ["S006"]},
        {"start": "2024.07", "end": "present", "org": "双城区人民政府", "title": "区委常委、副区长", "confidence": "confirmed", "source_ids": ["S006"]},
    ],
}

_RELATIONSHIPS = {
    1: [
        {"person": "邹永强", "person_id": "shuangcheng_邹永强", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "区委书记—区长搭档", "overlap_org": "中共哈尔滨市双城区委员会", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
        {"person": "徐鑫", "person_id": "shuangcheng_徐鑫", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "书记—副书记在区委班子", "overlap_org": "中共哈尔滨市双城区委员会", "overlap_period": "2023.06至今", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "李艳秋", "person_id": "shuangcheng_李艳秋", "relationship_type": "overlap", "strength": "medium", "evidence": "四套班子共事", "overlap_org": "双城区", "overlap_period": "2023.06至今", "confidence": "confirmed", "source_ids": ["S001"]},
    ],
    2: [
        {"person": "刘启嘉", "person_id": "shuangcheng_刘启嘉", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "区长受区委书记领导", "overlap_org": "中共哈尔滨市双城区委员会", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S002", "S008"]},
        {"person": "赵云鹏", "person_id": "shuangcheng_赵云鹏", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区长—副区长", "overlap_org": "双城区人民政府", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "殷雷", "person_id": "shuangcheng_殷雷", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区长—副区长", "overlap_org": "双城区人民政府", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S002"]},
    ],
    3: [
        {"person": "刘启嘉", "person_id": "shuangcheng_刘启嘉", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区委书记—副书记", "overlap_org": "中共哈尔滨市双城区委员会", "overlap_period": "2023.06至今", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "邹永强", "person_id": "shuangcheng_邹永强", "relationship_type": "overlap", "strength": "medium", "evidence": "同届区委班子", "overlap_org": "双城区", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S003"]},
    ],
    4: [{"person": "刘启嘉", "person_id": "shuangcheng_刘启嘉", "relationship_type": "overlap", "strength": "medium", "evidence": "四套班子共事", "overlap_org": "双城区", "overlap_period": "2023.06至今", "confidence": "confirmed", "source_ids": ["S004"]}],
    5: [{"person": "邹永强", "person_id": "shuangcheng_邹永强", "relationship_type": "overlap", "strength": "medium", "evidence": "四套班子共事", "overlap_org": "双城区", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S005"]}],
    6: [{"person": "邹永强", "person_id": "shuangcheng_邹永强", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区长—副区长", "overlap_org": "双城区人民政府", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S007"]}],
    7: [{"person": "邹永强", "person_id": "shuangcheng_邹永强", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区长—副区长", "overlap_org": "双城区人民政府", "overlap_period": "2026.01至今", "confidence": "confirmed", "source_ids": ["S006"]}],
}


def build_person_jsons():
    job_map = {1: "区委书记", 2: "区长", 3: "区委副书记", 4: "区人大常委会主任",
               5: "区政协主席", 6: "区委常委_区政府副区长", 7: "区委常委_区政府副区长"}
    for p in persons:
        timeline = _FULL_TIMELINES.get(p["id"], _DEPUTY_TIMELINES.get(p["id"], []))
        rels = _RELATIONSHIPS.get(p["id"], [])
        data = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "黑龙江省", "city": "哈尔滨市", "region": "双城区",
                                    "job": p["current_post"], "task_id": "heilongjiang_双城区", "time_focus": "2026年7月"},
            "identity": {
                "person_id": f"shuangcheng_{p['name']}", "name": p["name"], "aliases": [],
                "gender": p.get("gender") or "", "ethnicity": p.get("ethnicity") or "",
                "birth": p.get("birth") or "", "birthplace": p.get("birthplace") or "", "native_place": "",
                "education": "", "party_join": p.get("party_join") or "", "work_start": p.get("work_start") or "",
                "dedupe_keys": {"name_birth": f"{p['name']}_", "name_birthplace": f"{p['name']}_", "official_profile_url": p.get("source", "")},
            },
            "current_status": {
                "current_post": p["current_post"], "current_org": p["current_org"],
                "administrative_rank": "", "as_of": AS_OF, "is_current_confirmed": True,
                "source_ids": list({e.get("source") for e in timeline if e.get("source")}),
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": rels,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [], "secondary_specializations": [],
                "career_pattern": "cross_county_rotation" if p["name"] in ("邹永强",) else "local_ladder",
                "systems_experience": [], "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [], "speech_themes": [], "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "公开官网简历未发现负面信号", "date": "", "confidence": "plausible", "source_ids": []},
            ],
            "source_register": SOURCE_REGISTER,
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed",
                "career_completeness": "partial", "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的出生/籍贯/学历信息未在官网简历公开或早期履历细化待补充",
            },
            "open_questions": [
                {"priority": "high", "question": f"{p['name']}的出生年份、籍贯、学历、入党时间", "why_it_matters": "官网简历未公开个人隐私字段", "suggested_queries": [f"{p['name']} 双城区 简历"], "last_attempted": AS_OF},
            ],
        }
        if p["id"] == 1:
            data["open_questions"].append(
                {"priority": "medium", "question": "刘启嘉任前（2023.06前）双城区委书记及去向", "why_it_matters": "区委一把手更替背景", "suggested_queries": ["双城区 前任 区委书记"], "last_attempted": AS_OF})
        if p["id"] == 2:
            data["open_questions"].append(
                {"priority": "medium", "question": "邹永强前任区长（赫彦明）任免/去向", "why_it_matters": "区长更替路径", "suggested_queries": ["双城区 前任 区长 赫彦明"], "last_attempted": AS_OF})
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-哈尔滨市-{job_map[p['id']]}-{p['name']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


if __name__ == "__main__":
    print(f"Building {SLUG} network data... (AS_OF={AS_OF})")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in sorted(PERSONS_DIR.glob(f"{TODAY}-黑龙江省-哈尔滨市-*.json")):
        print(f"  Person: {p.name}")
    print("Done.")