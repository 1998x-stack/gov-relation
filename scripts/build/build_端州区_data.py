#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Duanzhou District (端州区), Zhaoqing, Guangdong."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_端州区")
DB_PATH = os.path.join(TMP, "端州区_network.db")
GEXF_PATH = os.path.join(TMP, "端州区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "张浩龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共肇庆市端州区委书记", "current_org": "中共肇庆市端州区委员会",
     "source": "http://www.zqdz.gov.cn/zwgk/xwdt/zwdt/dzdt/content/post_3256171.html"},
    {"id": 2, "name": "贺丹", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-05", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区委副书记、区政府党组书记、区长", "current_org": "肇庆市端州区人民政府",
     "source": "http://www.zqdz.gov.cn/zwgk/ldzc/content/post_3066736.html"},

    # ── District Committee Standing Members (其他区委领导) ──
    {"id": 3, "name": "赵国材", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": '端州区委副书记（兼任区"百千万工程"指挥部办公室主任）', "current_org": "中共肇庆市端州区委员会",
     "source": "端府〔2026〕4号"},
    {"id": 4, "name": "黎汉强", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区委常委、宣传部部长", "current_org": "中共肇庆市端州区委宣传部",
     "source": "端府〔2026〕4号"},
    {"id": 5, "name": "黎泽初", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区委常委、区政府党组副书记、副区长", "current_org": "肇庆市端州区人民政府",
     "source": "端府〔2026〕4号"},
    {"id": 6, "name": "黄海平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区委常委、组织部部长、党校校长", "current_org": "中共肇庆市端州区委组织部",
     "source": "端府〔2026〕4号"},
    {"id": 7, "name": "张林泉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区委常委", "current_org": "中共肇庆市端州区委员会",
     "source": "端府〔2026〕4号"},
    {"id": 8, "name": "李逸文", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区委常委、统战部部长、区政协党组副书记", "current_org": "中共肇庆市端州区委统战部",
     "source": "端府〔2026〕4号"},
    {"id": 9, "name": "张国安", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区领导", "current_org": "中共肇庆市端州区委员会",
     "source": "http://www.zqdz.gov.cn/zwgk/xwdt/zwdt/dzdt/content/post_3256171.html"},

    # ── District Government Deputy Leaders (区政府副区长) ──
    {"id": 10, "name": "植嘉升", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区政府党组成员、副区长", "current_org": "肇庆市端州区人民政府",
     "source": "端府〔2026〕4号"},
    {"id": 11, "name": "张艺", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区政府党组成员、副区长、区委卫健工委书记", "current_org": "肇庆市端州区人民政府",
     "source": "端府〔2026〕4号"},
    {"id": 12, "name": "郭盟开", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区政府党组成员、副区长、市公安局端州分局局长", "current_org": "肇庆市公安局端州分局",
     "source": "端府〔2026〕4号"},
    {"id": 13, "name": "伍东成", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区政府党组成员、副区长、区双龙经开区党工委书记、管委会主任", "current_org": "肇庆市端州区双龙省级经济开发区",
     "source": "端府〔2026〕4号"},
    {"id": 14, "name": "潘敏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "端州区政府党组成员、副区长、区委教育工委书记", "current_org": "肇庆市端州区人民政府",
     "source": "端府〔2026〕4号"},
]

organizations = [
    {"id": 1, "name": "中共肇庆市端州区委员会", "type": "党委", "level": "县处级", "parent": "中共肇庆市委员会",
     "location": "广东省肇庆市端州区"},
    {"id": 2, "name": "肇庆市端州区人民政府", "type": "政府", "level": "县处级", "parent": "肇庆市人民政府",
     "location": "广东省肇庆市端州区"},
    {"id": 3, "name": "中共肇庆市端州区委宣传部", "type": "党委", "level": "正科级", "parent": "中共肇庆市端州区委员会",
     "location": "广东省肇庆市端州区"},
    {"id": 4, "name": "中共肇庆市端州区委组织部", "type": "党委", "level": "正科级", "parent": "中共肇庆市端州区委员会",
     "location": "广东省肇庆市端州区"},
    {"id": 5, "name": "中共肇庆市端州区委统战部", "type": "党委", "level": "正科级", "parent": "中共肇庆市端州区委员会",
     "location": "广东省肇庆市端州区"},
    {"id": 6, "name": "肇庆市公安局端州分局", "type": "政府", "level": "正科级", "parent": "肇庆市公安局",
     "location": "广东省肇庆市端州区"},
    {"id": 7, "name": "肇庆市端州区双龙省级经济开发区", "type": "开发区", "level": "县处级", "parent": "肇庆市端州区人民政府",
     "location": "广东省肇庆市端州区"},
]

positions = [
    # 张浩龙
    {"person_id": 1, "org_id": 1, "title": "中共肇庆市端州区委书记", "start": "", "end": "present", "rank": "正处级", "note": "区委书记，2026年7月仍在任"},
    # 贺丹
    {"person_id": 2, "org_id": 1, "title": "端州区委副书记", "start": "", "end": "present", "rank": "副处级", "note": "区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记、区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    # 赵国材
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": "兼任区'百千万工程'指挥部办公室主任"},
    # 黎汉强
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 黎泽初
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": "常务副区长"},
    {"person_id": 5, "org_id": 2, "title": "区政府党组副书记、副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责发改、财政、应急等"},
    # 黄海平
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "组织部部长、党校校长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张林泉
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": "负责自然资源、住建等"},
    # 李逸文
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "统战部部长、区政协党组副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 植嘉升
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责水利、农业农村、乡村振兴等"},
    # 张艺
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责民政、卫健、医保等"},
    # 郭盟开
    {"person_id": 12, "org_id": 6, "title": "局长", "start": "", "end": "present", "rank": "副处级", "note": "副区长兼公安分局局长"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法行政等"},
    # 伍东成
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 7, "title": "双龙经开区党工委书记、管委会主任", "start": "", "end": "present", "rank": "副处级", "note": "负责经开区开发建设"},
    # 潘敏
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、政务服务等"},
]

relationships = [
    # 书记—区长（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记—区长党政正职搭档关系",
     "overlap_org": "端州区四套班子", "overlap_period": "2024-2026", "strength": "strong", "confidence": "confirmed"},

    # 书记—副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记—区委副书记上下级关系",
     "overlap_org": "中共端州区委", "overlap_period": "2024-2026", "strength": "strong", "confidence": "confirmed"},

    # 区长—常务副区长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长—常务副区长工作搭档",
     "overlap_org": "端州区人民政府", "overlap_period": "2024-2026", "strength": "strong", "confidence": "confirmed"},

    # 区委常委间的共事关系
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记—宣传部长上下级",
     "overlap_org": "中共端州区委", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记—组织部长上下级",
     "overlap_org": "中共端州区委", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记—区委常委",
     "overlap_org": "中共端州区委", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记—统战部长上下级",
     "overlap_org": "中共端州区委", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记—区领导共事",
     "overlap_org": "端州区", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},

    # 区长—副区长
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区长—副区长工作关系",
     "overlap_org": "端州区人民政府", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "区长—副区长工作关系",
     "overlap_org": "端州区人民政府", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区长—副区长工作关系",
     "overlap_org": "端州区人民政府", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区长—副区长工作关系",
     "overlap_org": "端州区人民政府", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区长—副区长工作关系",
     "overlap_org": "端州区人民政府", "overlap_period": "2024-2026", "strength": "medium", "confidence": "confirmed"},
]


# ── 辅助函数 ──────────────────────────────────────────

def esc(s):
    """XML转义"""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """按角色返回RGB颜色"""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title:
        if "副书记" in title:
            return "200,50,50"   # 暗红 — 副职
        return "255,50,50"   # 红色 — 党委正职
    if "区长" in title and "副区长" not in title:
        return "50,100,255"  # 蓝色 — 政府正职
    if "常务" in title:
        return "100,100,255"  # 深蓝 — 常务副职
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "副区长" in title:
        return "100,100,200" # 浅蓝 — 副区长
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "区委书记" in title:
        return "20.0"
    if "区长" in title and "副区长" not in title:
        return "20.0"
    if "副书记" in title:
        return "14.0"
    if "常务" in title:
        return "14.0"
    if "常委" in title:
        return "14.0"
    if "副区长" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """按类型返回组织颜色"""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
    }
    return colors.get(t, "200,200,200")


# ── 构建数据库 ────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, strength TEXT, confidence TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            str(p["id"]), p["name"], p["gender"], p["ethnicity"],
            p["birth"], p.get("birthplace", ""), p.get("native_place", ""), p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            str(pos["person_id"]), str(pos["org_id"]), pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
                     VALUES (?,?,?,?,?,?,?,?)""", (
            str(r["person_a"]), str(r["person_b"]), r["type"], r["context"],
            r["overlap_org"], r["overlap_period"], r.get("strength", "medium"), r.get("confidence", "plausible")
        ))

    conn.commit()
    conn.close()


# ── 构建 GEXF ─────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>端州区领导班子工作关系网络 - 数据来源: 端州区政府网站及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="肇庆市端州区"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="肇庆市端州区"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── 主函数 ──────────────────────────────────────────

def main():
    print(f"=== 端州区网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
