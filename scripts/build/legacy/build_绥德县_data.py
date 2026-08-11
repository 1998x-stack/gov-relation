#!/usr/bin/env python3
"""
绥德县领导班子工作关系网络数据生成脚本

数据来源：绥德县人民政府官方网站 (www.sxsd.gov.cn)、绥德融媒新闻报道
生成日期：2026-07-25

当前领导班子（截至2026年7月）：
- 县委书记：陈斌（2026年6月13日任命）
- 县委副书记、县长：常彦林
- 县人大常委会主任：孙虎生
- 县政协主席：黑兆龙
- 县委常委、常务副县长：苗立群
- 县委常委、组织部部长：李亚明
- 县委常委、纪委书记、监委主任：李泓江
- 夏卫峰、魏锦斌、许文元、慕探建、高胜利、李永刚、朱国锋、邓乐、李锦鹏

前任县委书记：杨文慧（至2026年6月，现任榆林市人大常委会副主任）

使用说明：
  python3 build_绥德县_data.py
"""

import sqlite3
from datetime import datetime

# ──────────────────────────────────────────────
# 人员数据 (id = 0..N 整数；slug 用于 GEXF 节点)
# ──────────────────────────────────────────────
PERSON_SLUG = {
    0: "suide_chen_bin",
    1: "suide_chang_yanlin",
    2: "suide_sun_husheng",
    3: "suide_hei_zhaolong",
    4: "suide_miao_liqun",
    5: "suide_li_yaming",
    6: "suide_li_hongjiang",
    7: "suide_xia_weifeng",
    8: "suide_wei_jinbin",
    9: "suide_xu_wenyuan",
    10: "suide_mu_tanjian",
    11: "suide_gao_shengli",
    12: "suide_li_yonggang",
    13: "suide_zhu_guofeng",
    14: "suide_deng_le",
    15: "suide_li_jinpeng",
    16: "suide_yang_wenhui",
}
SLUG_PERSON = {v: k for k, v in PERSON_SLUG.items()}

persons = [
    {"id": 0, "name": "陈斌", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委书记", "current_org": "中共绥德县委员会", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260615_2107578.html"},
    {"id": 1, "name": "常彦林", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记、县长", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115538.html"},
    {"id": 2, "name": "孙虎生", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县人大常委会主任", "current_org": "绥德县人大常委会", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260623_2109183.html"},
    {"id": 3, "name": "黑兆龙", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县政协主席", "current_org": "政协绥德县委员会", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260623_2109183.html"},
    {"id": 4, "name": "苗立群", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、常务副县长", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115538.html"},
    {"id": 5, "name": "李亚明", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、组织部部长", "current_org": "中共绥德县委组织部", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260624_2109497.html"},
    {"id": 6, "name": "李泓江", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共绥德县纪律检查委员会", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260624_2109497.html"},
    {"id": 7, "name": "夏卫峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115537.html"},
    {"id": 8, "name": "魏锦斌", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115538.html"},
    {"id": 9, "name": "许文元", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115538.html"},
    {"id": 10, "name": "慕探建", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115538.html"},
    {"id": 11, "name": "高胜利", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115538.html"},
    {"id": 12, "name": "李永刚", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202607/t20260717_2115537.html"},
    {"id": 13, "name": "朱国锋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260612_2107271.html"},
    {"id": 14, "name": "邓乐", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260612_2107271.html"},
    {"id": 15, "name": "李锦鹏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县级领导", "current_org": "绥德县人民政府", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260612_2107271.html"},
    {"id": 16, "name": "杨文慧", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "榆林市人大常委会副主任（前任县委书记）", "current_org": "榆林市人大常委会", "source": "http://www.sxsd.gov.cn/xwzx/zwyw/202606/t20260615_2107578.html"},
]

# ──────────────────────────────────────────────
# 组织数据
# ──────────────────────────────────────────────
organizations = [
    {"id": 0, "name": "中共绥德县委员会", "type": "党委", "level": "县级", "parent": "", "location": "陕西省榆林市绥德县"},
    {"id": 1, "name": "绥德县人民政府", "type": "政府", "level": "县级", "parent": "", "location": "陕西省榆林市绥德县"},
    {"id": 2, "name": "绥德县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "陕西省榆林市绥德县"},
    {"id": 3, "name": "政协绥德县委员会", "type": "政协", "level": "县级", "parent": "", "location": "陕西省榆林市绥德县"},
    {"id": 4, "name": "中共绥德县纪律检查委员会", "type": "党委", "level": "县级", "parent": "", "location": "陕西省榆林市绥德县"},
    {"id": 5, "name": "中共绥德县委组织部", "type": "党委", "level": "县级", "parent": "", "location": "陕西省榆林市绥德县"},
    {"id": 6, "name": "榆林市人大常委会", "type": "人大", "level": "地市级", "parent": "", "location": "陕西省榆林市"},
]

# ──────────────────────────────────────────────
# 任职数据 (person_id 和 org_id 引用整数 id)
# ──────────────────────────────────────────────
positions = [
    {"person_id": 0, "org_id": 0, "title": "县委书记", "start_date": "2026-06-13", "end_date": "present", "rank": "正县级", "note": "2026年6月13日省委、市委宣布任命"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 6, "title": "榆林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "同时曾任绥德县委书记至2026年6月"},
    {"person_id": 16, "org_id": 0, "title": "县委书记（前任）", "start_date": "2021", "end_date": "2026-06-13", "rank": "正县级", "note": "2021年至少已在任；2026年6月13日免职"},
]

# ──────────────────────────────────────────────
# 关系数据 (person_a/person_b 引用整数 id)
# ──────────────────────────────────────────────
relationships = [
    {"person_a": 0, "person_b": 1, "type": "superior_subordinate", "context": "县委书记与县长搭档关系", "overlap_org": "中共绥德县委员会/绥德县人民政府", "overlap_period": "2026-06-13至今"},
    {"person_a": 0, "person_b": 16, "type": "predecessor_successor", "context": "陈斌接替杨文慧担任县委书记", "overlap_org": "中共绥德县委员会", "overlap_period": "2026-06-13"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县长与常务副县长工作关系", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共绥德县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共绥德县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共绥德县委员会", "overlap_period": ""},
    {"person_a": 16, "person_b": 1, "type": "superior_subordinate", "context": "前任县委书记与县长搭档关系", "overlap_org": "中共绥德县委员会/绥德县人民政府", "overlap_period": "至2026-06-13"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县人大与县政协主要领导", "overlap_org": "绥德县", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate", "context": "县政府班子成员", "overlap_org": "绥德县人民政府", "overlap_period": ""},
]

# ══════════════════════════════════════════════
# DB / GEXF 辅助函数
# ══════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p["current_post"]
    if "书记" in post and "纪委" not in post:
        return "255,50,50"
    if "县长" in post or "副县长" in post:
        return "50,100,255"
    if "纪委" in post or "监委" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"
    if "政协" in post:
        return "255,240,200"
    return "100,100,100"

def person_size(p):
    if p["id"] in (0, 1, 16):  # 书记、县长、前书记
        return "20.0"
    return "12.0"

def org_color(o):
    type_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_map.get(o["type"], "200,200,200")

# ══════════════════════════════════════════════
# 构建 SQLite 数据库
# ══════════════════════════════════════════════

def build_db(db_path):
    conn = sqlite3.connect(str(db_path))
    
    # 删除旧表
    for tbl in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {tbl}")
    
    # 建表
    conn.execute("CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)")
    conn.execute("CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT)")
    conn.execute("CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER, title TEXT, start_date TEXT, end_date TEXT, rank TEXT, note TEXT, FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id))")
    conn.execute("CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT, FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id))")
    
    # 插入数据
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                      p["education"], p["party_join"], p["work_start"], p["current_post"],
                      p["current_org"], p["source"]))
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
                     (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                     (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    
    conn.commit()
    conn.close()
    
    n_p = len(persons)
    n_o = len(organizations)
    n_pos = len(positions)
    n_r = len(relationships)
    print(f"  Persons: {n_p}, Orgs: {n_o}, Positions: {n_pos}, Relationships: {n_r}")

# ══════════════════════════════════════════════
# 构建 GEXF 图文件
# ══════════════════════════════════════════════

def build_gexf(gexf_path):
    lines = []
    today = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>绥德县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('      <attribute id="4" title="role" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = PERSON_SLUG[p["id"]]
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "")
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    # Organization nodes
    for o in organizations:
        c = org_color(o)
        oid = o["id"] + 100000
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["location"])}"/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    # person -> organization edges
    for pos in positions:
        pid = PERSON_SLUG[pos["person_id"]]
        oid = pos["org_id"] + 100000
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    
    # person <-> person edges
    for r in relationships:
        pid_a = PERSON_SLUG[r["person_a"]]
        pid_b = PERSON_SLUG[r["person_b"]]
        lines.append(f'      <edge id="{eid}" source="p{pid_a}" target="p{pid_b}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(str(gexf_path), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Edges: {eid}")

# ══════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════

import sys
import os

if __name__ == "__main__":
    # 默认在当前目录输出；可通过命令行参数指定输出目录
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    db_path = os.path.join(out_dir, "绥德县_network.db")
    gexf_path = os.path.join(out_dir, "绥德县_network.gexf")
    
    print(f"Building database: {db_path}")
    build_db(db_path)
    
    print(f"Building GEXF: {gexf_path}")
    build_gexf(gexf_path)
    
    print("Done!")
