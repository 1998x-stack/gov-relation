#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 巴青县 (Baqing County) leadership network.

巴青县, 那曲市, 西藏自治区
Investigation: 县委书记 & 县长
"""

import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
STAGING = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(STAGING, "巴青县_network.db")
GEXF_PATH = os.path.join(STAGING, "巴青县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    {"id": 1, "name": "孟令合", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-09", "birthplace": "待查", "education": "西藏大学政史系",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县委书记", "current_org": "中共巴青县委员会",
     "source": "http://www.nqbqx.gov.cn/nqbqx/shuji/202303/3792ec9fc23f4d5f973f722b0f5529d9.shtml"},
    {"id": 2, "name": "平措顿珠", "gender": "男", "ethnicity": "藏族",
     "birth": "1983-09", "birthplace": "待查", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县委副书记、县长", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/xzqz/202207/c5c1f9fdc6e44e3699ae58513be1f625.shtml"},
    {"id": 3, "name": "童阿木", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-07", "birthplace": "待查", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县委常务副书记、常务副县长（援藏）", "current_org": "中共巴青县委员会",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/xxgk_zfld.shtml"},
    {"id": 4, "name": "谢松", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-11", "birthplace": "待查", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县委常委、常务副县长", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 5, "name": "黄磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-04", "birthplace": "待查", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县政府党组成员、副县长", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 6, "name": "王剑", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-08", "birthplace": "待查", "education": "中央党校大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县人民政府党组成员、副县长", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 7, "name": "格桑", "gender": "男", "ethnicity": "藏族",
     "birth": "1982-03", "birthplace": "待查", "education": "浙江公安高等专科学校刑侦",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县副县长、公安局局长", "current_org": "巴青县公安局",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 8, "name": "扎西", "gender": "女", "ethnicity": "藏族",
     "birth": "1981-06", "birthplace": "待查", "education": "西藏民族学院档案管理",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县政府党组成员、副县长", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 9, "name": "军民", "gender": "男", "ethnicity": "藏族",
     "birth": "1976-07", "birthplace": "待查", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县人民政府党组成员、副县长", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 10, "name": "迟拉", "gender": "男", "ethnicity": "藏族",
     "birth": "1985-09", "birthplace": "待查", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县政府党组成员、副县长、雅安镇党委书记", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 11, "name": "格桑伦珠", "gender": "男", "ethnicity": "藏族",
     "birth": "1979-09", "birthplace": "待查", "education": "在职大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县政府党组成员、副县长", "current_org": "巴青县人民政府",
     "source": "http://www.nqbqx.gov.cn/nqbqx/ldxx/ldgk_zfld.shtml"},
    {"id": 12, "name": "张军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "待查", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "那曲市政协主席", "current_org": "那曲市政协",
     "source": "http://www.nqbqx.gov.cn/nqbqx/xqyw/202207/59ab0e7037c14101bd36dacc548ff80f.shtml"},
    {"id": 13, "name": "苍阳才让", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "待查", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（前任巴青县县长）", "current_org": "",
     "source": "http://www.nqbqx.gov.cn/nqbqx/xwqw/202309/79904d3018ab4bdbbddb91c21b422a02.shtml"},
    {"id": 14, "name": "才仁郎公", "gender": "男", "ethnicity": "藏族",
     "birth": "1965", "birthplace": "西藏巴青", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "那曲市人大常委会主任", "current_org": "那曲市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E6%89%8D%E4%BB%81%E9%83%8E%E5%85%AC"},
    {"id": 15, "name": "徐恩发", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "待查", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县人大常委会副主任", "current_org": "巴青县人大常委会",
     "source": "http://www.nqbqx.gov.cn/"},
    {"id": 16, "name": "李勇", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "待查", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县人大常委会副主任", "current_org": "巴青县人大常委会",
     "source": "http://www.nqbqx.gov.cn/"},
    {"id": 17, "name": "次仁平措", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "待查", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴青县政协三级调研员", "current_org": "巴青县政协",
     "source": "http://www.nqbqx.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共巴青县委员会", "type": "党委", "level": "县处级", "parent": "中共那曲市委员会", "location": "西藏自治区那曲市巴青县"},
    {"id": 2, "name": "巴青县人民政府", "type": "政府", "level": "县处级", "parent": "那曲市人民政府", "location": "西藏自治区那曲市巴青县"},
    {"id": 3, "name": "巴青县公安局", "type": "政府", "level": "乡科级", "parent": "巴青县人民政府", "location": "西藏自治区那曲市巴青县"},
    {"id": 4, "name": "巴青县雅安镇", "type": "乡镇/街道", "level": "乡科级", "parent": "巴青县人民政府", "location": "西藏自治区那曲市巴青县"},
    {"id": 5, "name": "那曲市政协", "type": "政协", "level": "地厅级", "parent": "那曲市", "location": "西藏自治区那曲市"},
    {"id": 6, "name": "那曲市人大常委会", "type": "人大", "level": "地厅级", "parent": "那曲市", "location": "西藏自治区那曲市"},
    {"id": 7, "name": "巴青县人大常委会", "type": "人大", "level": "县处级", "parent": "巴青县", "location": "西藏自治区那曲市巴青县"},
    {"id": 8, "name": "巴青县政协", "type": "政协", "level": "县处级", "parent": "巴青县", "location": "西藏自治区那曲市巴青县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "巴青县委书记", "start_date": "2022-12", "end_date": "至今", "rank": "正县级", "note": "接替张军"},
    {"person_id": 2, "org_id": 2, "title": "巴青县委副书记、县长", "start_date": "2023末", "end_date": "至今", "rank": "正县级", "note": "接替苍阳才让"},
    {"person_id": 3, "org_id": 1, "title": "巴青县委常务副书记", "start_date": "", "end_date": "至今", "rank": "正县级", "note": "第十批援藏干部"},
    {"person_id": 3, "org_id": 2, "title": "巴青县常务副县长（援藏）", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "巴青县委常委", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "三级调研员"},
    {"person_id": 4, "org_id": 2, "title": "巴青县常务副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "巴青县副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "巴青县副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "巴青县副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "三级高级警长"},
    {"person_id": 7, "org_id": 3, "title": "巴青县公安局长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "巴青县副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "巴青县副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "巴青县副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "雅安镇党委书记", "start_date": "", "end_date": "至今", "rank": "正科级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "巴青县副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "巴青县委书记", "start_date": "", "end_date": "2022-10", "rank": "正县级", "note": "同时担任那曲市政协主席"},
    {"person_id": 12, "org_id": 5, "title": "那曲市政协主席", "start_date": "2022前", "end_date": "至今", "rank": "地厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "巴青县县长", "start_date": "", "end_date": "2023末", "rank": "正县级", "note": "一级调研员"},
    {"person_id": 14, "org_id": 6, "title": "那曲市人大常委会主任", "start_date": "2022", "end_date": "至今", "rank": "地厅级", "note": "巴青县人"},
    {"person_id": 15, "org_id": 7, "title": "巴青县人大常委会副主任", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "巴青县人大常委会副主任", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 8, "title": "巴青县政协三级调研员", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政正职搭档", "overlap_org": "巴青县委/县政府", "overlap_period": "2023末至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副书记（援藏干部）", "overlap_org": "中共巴青县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与常委、常务副县长", "overlap_org": "中共巴青县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴青县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴青县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长、公安局长", "overlap_org": "巴青县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴青县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴青县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴青县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴青县人民政府", "overlap_period": "至今"},
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "前任→现任县委书记", "overlap_org": "中共巴青县委员会", "overlap_period": "2022交接"},
    {"person_a": 12, "person_b": 14, "type": "work_relationship", "context": "市政协主席与市人大常委会主任", "overlap_org": "那曲市", "overlap_period": "2022至今"},
    {"person_a": 13, "person_b": 2, "type": "predecessor_successor", "context": "前任→现任县长", "overlap_org": "巴青县人民政府", "overlap_period": "2023交接"},
    {"person_a": 14, "person_b": 1, "type": "regional_link", "context": "巴青籍那曲市领导与现任县委书记", "overlap_org": "那曲市", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate", "context": "县委书记与人大副主任", "overlap_org": "巴青县", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 16, "type": "superior_subordinate", "context": "县委书记与人大副主任", "overlap_org": "巴青县", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate", "context": "县委书记与政协干部", "overlap_org": "巴青县", "overlap_period": "至今"},
]


def esc(s):
    if s is None: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "")
    if "县委书记" in post: return "255,50,50"
    if "县长" in post: return "50,100,255"
    if "常务副书记" in post: return "255,165,0"
    return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    if "乡镇" in t: return "255,255,200"
    return "200,200,200"


def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)


def build_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    for t in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.execute("CREATE TABLE persons (id INTEGER PRIMARY KEY,name TEXT NOT NULL,gender TEXT DEFAULT '',ethnicity TEXT DEFAULT '',birth TEXT DEFAULT '',birthplace TEXT DEFAULT '',education TEXT DEFAULT '',party_join TEXT DEFAULT '',work_start TEXT DEFAULT '',current_post TEXT DEFAULT '',current_org TEXT DEFAULT '',source TEXT DEFAULT '')")
    conn.execute("CREATE TABLE organizations (id INTEGER PRIMARY KEY,name TEXT NOT NULL,type TEXT DEFAULT '',level TEXT DEFAULT '',parent TEXT DEFAULT '',location TEXT DEFAULT '')")
    conn.execute("CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT,person_id INTEGER NOT NULL,org_id INTEGER NOT NULL,title TEXT DEFAULT '',start_date TEXT DEFAULT '',end_date TEXT DEFAULT '',rank TEXT DEFAULT '',note TEXT DEFAULT '',FOREIGN KEY (person_id) REFERENCES persons(id),FOREIGN KEY (org_id) REFERENCES organizations(id))")
    conn.execute("CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT,person_a INTEGER NOT NULL,person_b INTEGER NOT NULL,type TEXT DEFAULT '',context TEXT DEFAULT '',overlap_org TEXT DEFAULT '',overlap_period TEXT DEFAULT '',FOREIGN KEY (person_a) REFERENCES persons(id),FOREIGN KEY (person_b) REFERENCES persons(id))")
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (p["id"],p["name"],p.get("gender",""),p.get("ethnicity",""),p.get("birth",""),p.get("birthplace",""),p.get("education",""),p.get("party_join",""),p.get("work_start",""),p.get("current_post",""),p.get("current_org",""),p.get("source","")))
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", (o["id"],o["name"],o.get("type",""),o.get("level",""),o.get("parent",""),o.get("location","")))
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)", (pos["person_id"],pos["org_id"],pos.get("title",""),pos.get("start_date",""),pos.get("end_date",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)", (r["person_a"],r["person_b"],r.get("type",""),r.get("context",""),r.get("overlap_org",""),r.get("overlap_period","")))
    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")


def build_gexf():
    lines = []
    today = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>巴青县（西藏那曲市）领导干部工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("ethnicity",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        sz = "8.0"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title",""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date",""))} - {esc(pos.get("end_date",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type",""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print(f"Done. {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships.")