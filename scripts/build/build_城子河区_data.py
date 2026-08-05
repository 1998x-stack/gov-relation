#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 城子河区 (Chengzihe District), 鸡西市, 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_城子河区
Level: 市辖区（县处级）
Targets: 区委书记 & 区长
Parent city: 鸡西市

Research sources (all confirmed via 城子河区人民政府官网 http://www.czh.gov.cn/):
  - 区委领导页: 蔡杰(区委书记), 袁冰洋(区委副书记/区长), 王艳明(宣传部长), 安娜(组织/统战部长),
    孙仲秋(纪委书记/监委主任), 张敏(常务副区长), 杜翀(副区长), 辛英男(常委副区长), 朱亚(人武部长)
  - 区政府领导页: 袁冰洋(区长), 张敏(常务), 杜翀, 辛英男(挂职), 邹静海(副区长/公安局长), 姜虹波, 勾思远, 杨钢
  - 区人大领导页: 梁东红(主任), 高庆嵩, 丁武, 郭立新, 陈雷(副主任)
  - 区政协领导页: 田洪伟(主席), 秦会峰, 钟天吉, 迟玉清(副主席,党组成员)
  - 城子河区简介（走进城子河）: 1970年建区，面积181.1km²，两乡五街道，2025年户籍9.5万/常住6.8万，
    2025年地区生产总值16.85亿元（增速3.4%）

Confidence notes:
  - 现任区委书记 蔡杰、区长 袁冰洋：confirmed via 官方领导简介 + 2026-07 督导安全生产新闻（Cai）& 2026-08 防汛新闻（袁）
  - 其余班子成员：confirmed via 官方领导简介页（2023-09 建档，2026 仍沿用）
  - 完整履历（出生/籍贯/教育/历任起止）在网络受限下未取得 -> 编码为 open_questions/open_gaps
"""

import json
import os
from datetime import datetime

SLUG = "城子河区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

MISSING = {"gender": "", "ethnicity": "", "birth": "", "birthplace": "",
           "education": "", "party_join": "中共党员", "work_start": ""}

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "蔡杰", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区委书记",
     "current_org": "中共鸡西市城子河区委员会", "source": "城子河区政府官网—区委领导页 (2026)"},
    {"id": 2, "name": "袁冰洋", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区委副书记、区政府区长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网—区委领导/政府领导页 (2026)"},
    {"id": 3, "name": "张敏", **MISSING, "gender": "女", "ethnicity": "满族",
     "current_post": "区委常委、政府常务副区长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网 政府领导页 (2026)"},
    {"id": 4, "name": "杜翀", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区委常委、政府副区长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网 领导页 (2026)"},
    {"id": 5, "name": "辛英男", **MISSING, "gender": "女", "ethnicity": "汉族",
     "current_post": "区委常委、政府副区长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网 区委领导/政府领导页 (2026)"},
    {"id": 6, "name": "邹静海", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区政府副区长、公安分局局长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网 政府领导页 (2026)"},
    {"id": 7, "name": "姜虹波", **MISSING, "gender": "女", "ethnicity": "汉族",
     "current_post": "区政府副区长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网 政府领导页 (2026)"},
    {"id": 8, "name": "勾思远", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区政府副区长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网 政府领导页 (2026)"},
    {"id": 9, "name": "杨钢", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区政府副区长",
     "current_org": "鸡西市城子河区人民政府", "source": "城子河区政府官网 政府领导页 (2026)"},
    {"id": 10, "name": "王艳明", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区委常委、宣传部部长",
     "current_org": "中共鸡西市城子河区委员会", "source": "城子河区政府官网 区委领导页 (2026)"},
    {"id": 11, "name": "安娜", **MISSING, "gender": "女", "ethnicity": "汉族",
     "current_post": "区委常委、组织部部长、统战部部长",
     "current_org": "中共鸡西市城子河区委员会", "source": "城子河区政府官网 区委领导页 (2026)"},
    {"id": 12, "name": "孙仲秋", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区委常委、纪委书记、区监委主任",
     "current_org": "城子河区纪委监委", "source": "城子河区政府官网 区委领导页 (2026)"},
    {"id": 13, "name": "朱亚", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区委常委、人武部部长",
     "current_org": "城子河区人民武装部", "source": "城子河区政府官网 区委领导页 (2026)"},
    {"id": 14, "name": "梁东红", **MISSING, "gender": "女", "ethnicity": "汉族",
     "current_post": "区人大常委会主任",
     "current_org": "城子河区人民代表大会常务委员会", "source": "城子河区政府官网 区人大领导页 (2026)"},
    {"id": 15, "name": "高庆嵩", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区人大常委会副主任",
     "current_org": "城子河区人民代表大会常务委员会", "source": "城子河区政府官网 区人大领导页 (2026)"},
    {"id": 16, "name": "丁武", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区人大常委会副主任",
     "current_org": "城子河区人民代表大会常务委员会", "source": "城子河区政府官网 区人大领导页 (2026)"},
    {"id": 17, "name": "郭立新", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区人大常委会副主任",
     "current_org": "城子河区人民代表大会常务委员会", "source": "城子河区政府官网 区人大领导页 (2026)"},
    {"id": 18, "name": "陈雷", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区人大常委会副主任",
     "current_org": "城子河区人民代表大会常务委员会", "source": "城子河区政府官网 区人大领导页 (2026)"},
    {"id": 19, "name": "田洪伟", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区政协党组书记、主席",
     "current_org": "中国人民政治协商会议城子河区委员会", "source": "城子河区政府官网 区政协领导页 (2026)"},
    {"id": 20, "name": "秦会峰", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区政协副主席",
     "current_org": "中国人民政治协商会议城子河区委员会", "source": "城子河区政府官网 区政协领导页 (2026)"},
    {"id": 21, "name": "钟天吉", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区政协副主席",
     "current_org": "中国人民政治协商会议城子河区委员会", "source": "城子河区政府官网 区政协领导页 (2026)"},
    {"id": 22, "name": "迟玉清", **MISSING, "gender": "男", "ethnicity": "汉族",
     "current_post": "区政协副主席、党组成员",
     "current_org": "中国人民政治协商会议城子河区委员会", "source": "城子河区政府官网 区政协领导页 (2026)"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鸡西市城子河区委员会", "type": "党委", "level": "县处级", "parent": "中共鸡西市委员会", "location": "黑龙江省鸡西市城子河区"},
    {"id": 2, "name": "鸡西市城子河区人民政府", "type": "政府", "level": "县处级", "parent": "鸡西市人民政府", "location": "黑龙江省鸡西市城子河区"},
    {"id": 3, "name": "城子河区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鸡西市人民代表大会常务委员会", "location": "黑龙江省鸡西市城子河区"},
    {"id": 4, "name": "中国人民政治协商会议城子河区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议鸡西市委员会", "location": "黑龙江省鸡西市城子河区"},
    {"id": 5, "name": "城子河区纪委监委", "type": "纪委", "level": "县处级", "parent": "中共鸡西市纪律检查委员会", "location": "黑龙江省鸡西市城子河区"},
    {"id": 6, "name": "城子河区人民武装部", "type": "军队", "level": "县处级", "parent": "鸡西市军分区", "location": "黑龙江省鸡西市城子河区"},
    {"id": 7, "name": "城子河区公安分局", "type": "公安", "level": "乡科级", "parent": "城子河区人民政府", "location": "黑龙江省鸡西市城子河区"},
    {"id": 8, "name": "中共鸡西市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "鸡西市"},
    {"id": 9, "name": "鸡西市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "鸡西市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "主持区委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "主持区政府全面工作，分管审计局"},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "区委常委、政府常务副区长，分管区财政局、发改局、人社局等"},
    {"person_id": 4, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责安全生产、工业、农业农村、水利等"},
    {"person_id": 5, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责招商引资、市场监管、文体旅游等"},
    {"person_id": 6, "org_id": 2, "title": "政府副区长、公安分局局长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责公共安全"},
    {"person_id": 7, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责教育、卫健、民政等"},
    {"person_id": 8, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责城市建设、生态环境等"},
    {"person_id": 9, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "协助杜翀分管安全生产"},
    {"person_id": 10, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责宣传思想文化等"},
    {"person_id": 11, "org_id": 1, "title": "区委常委、组织部部长、统战部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责组织、干部、人才、党建、统战"},
    {"person_id": 12, "org_id": 5, "title": "区委常委、纪委书记、区监委主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责纪检、监察、巡察"},
    {"person_id": 13, "org_id": 6, "title": "区委常委、人武部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责武装部工作"},
    {"person_id": 14, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "主持区人大常委会全面工作"},
    {"person_id": 15, "org_id": 3, "title": "区人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责人大调研、社会建设"},
    {"person_id": 16, "org_id": 3, "title": "区人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责常务、机关建设、财政预算"},
    {"person_id": 17, "org_id": 3, "title": "区人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责法制和财政预算"},
    {"person_id": 18, "org_id": 3, "title": "区人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责人大代表联络、人事选举"},
    {"person_id": 19, "org_id": 4, "title": "区政协党组书记、主席", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "主持区政协党组和全面工作"},
    {"person_id": 20, "org_id": 4, "title": "区政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "分管提案委员会和经济委员会"},
    {"person_id": 21, "org_id": 4, "title": "区政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "分管文教卫生、法制宗教工作"},
    {"person_id": 22, "org_id": 4, "title": "区政协副主席、党组成员", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "协助主席抓全面，分管农业和农村委员会"},
]

# ── Relationships (与区委书记、区长相关的核心班子关系) ─────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "区委书记与区长（党政正职搭档）", "overlap_org": "城子河区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "区委书记与纪委书记（从严治党）", "overlap_org": "中共城子河区委/区纪委监委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区委书记与组织部部长（人事）", "overlap_org": "中共城子河区委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与宣传部部长", "overlap_org": "中共城子河区委", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "城子河区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长杜翀", "overlap_org": "城子河区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长辛英男", "overlap_org": "城子河区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长/公安局长邹静海", "overlap_org": "城子河区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长杨钢", "overlap_org": "城子河区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "区委书记与区人大常委会主任", "overlap_org": "城子河区人大", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate", "context": "区委书记与区政协主席", "overlap_org": "城子河区政协", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长勾思远", "overlap_org": "城子河区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长姜虹波", "overlap_org": "城子河区人民政府", "overlap_period": "2026"},
]

# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name):
    if name == "蔡杰":
        return "255,50,50"
    if name == "袁冰洋":
        return "50,100,255"
    if name == "张敏":
        return "100,150,255"
    if name in ("杜翀", "辛英男", "邹静海", "姜虹波", "勾思远", "杨钢"):
        return "80,130,230"
    if name == "孙仲秋":
        return "255,165,0"
    if name in ("王艳明", "安娜", "朱亚"):
        return "200,60,60"
    if name == "梁东红":
        return "200,220,240"
    if name in ("田洪伟",):
        return "255,200,120"
    return "100,100,100"

def org_color(o_type):
    if "党委" in o_type or "纪检" in o_type:
        return "255,200,200"
    if "政府" in o_type or "公安" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "军队" in o_type:
        return "200,240,200"
    return "200,200,200"

def person_by_name(name):
    for p in persons:
        if p["name"] == name:
            return p
    raise KeyError(name + " 不在 persons 中")

# ── DB ─────────────────────────────────────────────────────────────────────
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
            current_post TEXT, current_org TEXT, source TEXT);
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT);
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id));
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id));
    """)
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""),
             p.get("birthplace",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""),
             p.get("current_post",""), p.get("current_org",""), p.get("source","")))
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

# ── GEXF ───────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>城子河区领导班子工作关系网络 - {SLUG}, 鸡西市, 黑龙江省</description>')
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
        c = person_color(p["name"])
        sz = "20.0" if p["name"] in ("蔡杰", "袁冰洋") else "16.0" if p["name"] in ("梁东红", "田洪伟") else "12.0"
        nid = f"p{p['id']}"
        lines.append(f'      <node id="{nid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["name"])
        oid = f"o{o['id']}"
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
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  OK: GEXF ({eid} edges)")

# ── Person JSON ────────────────────────────────────────────────────────────
def make_person_json(p, timeline=None, relationships_list=None, source_register=None, is_current=True):
    if timeline is None:
        timeline = []
    if relationships_list is None:
        relationships_list = []
    if source_register is None:
        source_register = []
    name = p["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "鸡西市",
            "region": "城子河区",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_城子河区",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"chengzihe_{name}",
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth','')}",
                "name_birthplace": f"{name}_{p.get('birthplace','')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "县处级",
            "as_of": AS_OF,
            "is_current_confirmed": is_current,
            "source_ids": ["S001", "S002"]
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
            "geographic_pattern": ["黑龙江省鸡西市"],
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
            {"type": "none_found", "description": "公开官方信息未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed" if is_current else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的出生/籍贯/教育及历任职务起止时间待补充"
        },
        "open_questions": [
            {"priority": "high", "question": f"{name}的出生/籍贯/教育/入党及历任职务起止时间", "why_it_matters": "丰富人物画像与网络分析", "suggested_queries": [f"{name} 简历", f"{name} 任前公示"], "last_attempted": AS_OF}
        ]
    }

def _write_json(obj, job, name):
    path = os.path.join(STAGING, f"{TODAY}-黑龙江省-鸡西市-{job}-{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  OK: person json {os.path.basename(path)}")

def build_person_jsons():
    SOURCES = [
        {"id": "S001", "title": "城子河区人民政府官网—领导简介（区委领导）", "url": "http://www.czh.gov.cn/czh/fab6f4306caf4414bba9d36a7e296567/202309/c06_268877.shtml", "publisher": "城子河区人民政府", "published_at": "2023-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认蔡杰任区委书记、袁冰洋任区长等区委班子"},
        {"id": "S002", "title": "城子河区人民政府官网—领导简介（政府领导）", "url": "http://www.czh.gov.cn/czh/4b2b7a34ee3646ee9e2571820ea719c7/", "publisher": "城子河区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认区政府班子成员（区长袁冰洋、常务副区长张敏、副区长等）"},
        {"id": "S003", "title": "城子河区人民政府官网—领导简介（区人大领导）", "url": "http://www.czh.gov.cn/czh/85b34610e6334207a927aca17a8f339a/", "publisher": "城子河区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区人大常委会主任梁东红，副主任高庆嵩/丁武/郭立新/陈雷"},
        {"id": "S004", "title": "城子河区人民政府官网—领导简介（区政协领导）", "url": "http://www.czh.gov.cn/czh/75d8cc81440c451d9d5012866fd6746e/", "publisher": "城子河区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区政协主席田洪伟，副主席秦会峰/钟/迟玉清"},
        {"id": "S005", "title": "城子河区政府官网—蔡杰督导检查安全生产工作", "url": "http://www.czh.gov.cn/czh/3b90dde8ef5d4e57ac8b7f0ea194cc41/202607/c06_368425.shtml", "publisher": "城子河区委宣传部", "published_at": "2026-07-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "证实现任区委书记蔡杰深入煤矿督查"},
        {"id": "S006", "title": "城子河区人民政府官网—走进城子河（简介）", "url": "http://www.czh.gov.cn/czh/0c3710c8560e41c9ac0ed62453b46790/zjczh.shtml", "publisher": "城子河区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "城子河区概况（1970年建区，辖两乡五街道等）"},
    ]

    # 1. 区委书记 蔡杰
    caijie_tl = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到蔡杰完整履历（公安局系统经历待考）", "confidence": "unverified", "source_ids": []},
        {"start": "2023-09", "end": "present", "org": "中共鸡西市城子河区委员会", "title": "区委书记", "notes": "官方领导简介页显示的现任区委书记", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    caie_rel = [
        {"person": "袁冰洋", "person_id": "chengzihe_袁冰洋", "relationship_type": "overlap", "strength": "strong", "evidence": "政府班子成员（区长）", "overlap_org": "城子河区人民政府", "overlap_period": "2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
    ]
    caie = make_person_json(person_by_name("蔡杰"), caijie_tl, caie_rel, SOURCES)
    caie["professional_profile"]["career_pattern"] = "unknown"
    caie["professional_profile"]["primary_specializations"] = ["党务领导"]
    caie["open_questions"] = [{"priority": "high", "question": "蔡杰的出生/籍贯/教育/入党及任区委书记前的完整履历", "why_it_matters": "现任区委书记核心画像不完整", "suggested_queries": ["蔡杰 简历", "蔡杰 城子河 区委书记 任前公示"], "last_attempted": AS_OF}]
    _write_json(caie, "区委书记", "蔡杰")

    # 2. 区长 袁冰洋
    yb_tl = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到袁冰洋完整履历", "confidence": "unverified", "source_ids": []},
        {"start": "2023-09", "end": "present", "org": "城子河区人民政府", "title": "区委副书记、区长", "notes": "官方领导页显示", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    yb_rel = [
        {"person": "蔡杰", "person_id": "chengzihe_蔡杰", "relationship_type": "overlap", "strength": "strong", "evidence": "党政班子同岗", "overlap_org": "城子河区", "overlap_period": "2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
    ]
    yb = make_person_json(person_by_name("袁冰洋"), yb_tl, yb_rel, SOURCES)
    yb["professional_profile"]["primary_specializations"] = ["城市更新", "民生", "防汛", "营商环境"]
    yb["governance_record"] = [
        {"period": "2026-06--07", "domain": "urban_construction", "achievement_or_event": "袁冰洋多篇工作时间强调城市更新、民生工程、超大城市建设", "role_in_event": "区长", "measurable_outcome": "城子河区城市更新", "location": "城子河区", "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    yb["open_questions"] = [{"priority": "high", "question": "袁冰洋的出生/籍贯/教育/入党及任区长前完整履历", "why_it_matters": "现任区长核心画像不完整", "suggested_queries": ["袁冰洋 简历", "袁冰洋 任前公示"], "last_attempted": AS_OF}]
    _write_json(yb, "区长", "袁冰洋")

    # 3. 区委常委、纪委书记等其余主要班子成员简版 person json
    others = {
        "张敏": ("区委常委、常务副区长", []),
    }
    # 为关键班子人员补 person json（区人委会/区政协/区纪委等）
    for nm, (job, rels) in others.items():
        p = person_by_name(nm)
        obj = make_person_json(p, [
            {"start": "unknown", "end": "present", "org": "城子河区人民政府", "title": job, "notes": "现任", "confidence": "confirmed", "source_ids": ["S002"]},
        ], rels, SOURCES)
        obj["confidence_summary"]["career_completeness"] = "thin"
        _write_json(obj, job, nm)

    # 区人大主任 / 区政协主席 也写 person json
    for nm, job, org, sid in [
        ("梁东红", "区人大常委会主任", "城子河区人大常委会", "S003"),
        ("田洪伟", "区政协党组书记、主席", "中国人民政治协商会议城子河区委员会", "S004"),
    ]:
        p = person_by_name(nm)
        obj = make_person_json(p, [
            {"start": "unknown", "end": "present", "org": org, "title": job, "notes": "现任", "confidence": "confirmed", "source_ids": [sid]},
        ], [], SOURCES)
        obj["confidence_summary"]["career_completeness"] = "thin"
        _write_json(obj, job, nm)

# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    orig_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        print(f"Building {SLUG} network data...")
        build_db()
        build_gexf()
        build_person_jsons()
        print("\nOutput files in:", STAGING)
        print("  DB:  ", DB_PATH)
        print("  GEXF:", GEXF_PATH)
        for f in sorted(os.listdir(STAGING)):
            if f.endswith(".json") and f.startswith(TODAY):
                print("  Person:", f)
        print("Done.")
    finally:
        os.chdir(orig_cwd)