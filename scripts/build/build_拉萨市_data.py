#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 拉萨市 (Lhasa City) leadership network.

Current as of: 2026-08-03
Data sources:
  - https://www.lasa.gov.cn/lasa/ldxx/ldzc.shtml (government leadership listing)
  - https://www.lasa.gov.cn/lasa/shiz/202212/... (mayor Wang Qiang resume)
  - https://www.lasa.gov.cn/lasa/fsz/ (deputy mayor bios)
"""

import sqlite3
import os
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "拉萨市_network.db")
GEXF_PATH = os.path.join(STAGING, "拉萨市_network.gexf")

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "拉萨市"
TODAY = "2026-08-03"

# ── Persons (from official lasa.gov.cn leadership page) ─────────────
persons = [
    {"id": 1, "name": "达娃次仁", "gender": "男", "ethnicity": "藏族",
     "birth": "1972-00", "birthplace": "西藏自治区萨嘎县",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西藏自治区党委常委、拉萨市委书记", "current_org": "中共拉萨市委员会",
     "source": "https://www.lasa.gov.cn/lasa/ldhd/"},
    {"id": 2, "name": "王强", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-10", "birthplace": "江西省瑞昌市",
     "education": "中央党校博士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市委副书记、市政府党组书记、市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/shiz/202212/d07fbbbca9424a91aa14e74a71948715.shtml"},
    {"id": 3, "name": "李江新", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "",
     "education": "南京大学法学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市委副书记、常务副市长（援藏）", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202402/c81eeacb470c4845b32c0ea14f8473c7.shtml"},
    {"id": 4, "name": "张明智", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-04", "birthplace": "",
     "education": "中国农业大学农业推广硕士、中央党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市委副书记、常务副市长（援藏）", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202508/b8dc4bafe28843a1b656fe05181525fd.shtml"},
    {"id": 5, "name": "扎西白珍", "gender": "女", "ethnicity": "藏族",
     "birth": "1969-08", "birthplace": "",
     "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202111/dfa6316930ac42ce9ebba9010d46df29.shtml"},
    {"id": 6, "name": "陆从福", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "",
     "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202111/ba0497fe76db48aea557bda595df2fc3.shtml"},
    {"id": 7, "name": "洛色", "gender": "男", "ethnicity": "藏族",
     "birth": "1979-09", "birthplace": "",
     "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202111/78f7e25083a14caeb990f206174f712a.shtml"},
    {"id": 8, "name": "赵世东", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "",
     "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202111/61907adc72974507bdf759f272bfd161.shtml"},
    {"id": 9, "name": "巴桑多吉", "gender": "男", "ethnicity": "藏族",
     "birth": "1978-02", "birthplace": "",
     "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长、市公安局局长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202304/814fd8b880b44cd0bde5016f6c9ea120.shtml"},
    {"id": 10, "name": "罗丹", "gender": "男", "ethnicity": "藏族",
     "birth": "1975-10", "birthplace": "",
     "education": "中国政法大学法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202402/915b793eb0e24aa9b9e30f8954f6bb22.shtml"},
    {"id": 11, "name": "高军", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "",
     "education": "四川省工商管理学院研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202405/f4c09f7eda7d4ec58bd07f3b1c2ac5e8.shtml"},
    {"id": 12, "name": "白玛玉珍", "gender": "女", "ethnicity": "藏族",
     "birth": "1971-06", "birthplace": "",
     "education": "中央民族学院藏语言文学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市副市长", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202405/cb97f80273074373b14346947729873c.shtml"},
    {"id": 13, "name": "陆文忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-10", "birthplace": "",
     "education": "江苏省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市政府党组成员（援藏）", "current_org": "拉萨市人民政府",
     "source": "https://www.lasa.gov.cn/lasa/fsz/202411/a89c080813224e1b9e0223e1b3d76fcb.shtml"},
    {"id": 14, "name": "史文颖", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-07", "birthplace": "",
     "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拉萨市政府党组成员、秘书长", "current_org": "拉萨市人民政府办公室",
     "source": "https://www.lasa.gov.cn/lasa/msz/202506/3a86d3bee204423485f59661cc57a803.shtml"},
    {"id": 15, "name": "肖友才", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E8%8B%8F%E7%A4%BA%E5%8F%8B%E6%89%8D"},
    {"id": 16, "name": "果果", "gender": "男", "ethnicity": "藏族",
     "birth": "1967", "birthplace": "西藏自治区墨竹工卡县",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共拉萨市委员会", "type": "党委", "level": "地级市", "parent": "中共西藏自治区委员会", "location": "西藏自治区拉萨市"},
    {"id": 2, "name": "拉萨市人民政府", "type": "政府", "level": "地级市", "parent": "西藏自治区人民政府", "location": "西藏自治区拉萨市"},
    {"id": 3, "name": "拉萨市人民政府办公室", "type": "政府", "level": "正处级", "parent": "拉萨市人民政府", "location": "西藏自治区拉萨市"},
    {"id": 4, "name": "拉萨市公安局", "type": "政府", "level": "正处级", "parent": "拉萨市人民政府", "location": "西藏自治区拉萨市"},
]

# ── Positions ──────────────────────────────────────────────────────
positions = [
    # Current positions
    {"person_id": 1, "org_id": 1, "title": "西藏自治区党委常委", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "拉萨市委书记", "start_date": "2026-03", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "拉萨市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "拉萨市市长", "start_date": "2022-12", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "拉萨市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "援藏（江苏南京）"},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "援藏（江苏南京）"},
    {"person_id": 4, "org_id": 1, "title": "拉萨市委副书记", "start_date": "2025-08", "end_date": "present", "rank": "正厅级", "note": "援藏（北京）"},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "2025-08", "end_date": "present", "rank": "正厅级", "note": "援藏（北京）"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "援藏（江苏）"},
    {"person_id": 14, "org_id": 2, "title": "市政府党组成员、秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "办公室主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────
relationships = [
    # Top leadership pair
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长，党政主要领导工作搭档", "overlap_org": "中共拉萨市委员会", "overlap_period": "2026-03至今"},
    # Party Standing Committee overlaps
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "市委副书记协助市委书记工作", "overlap_org": "中共拉萨市委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "市委副书记协助市委书记工作", "overlap_org": "中共拉萨市委员会", "overlap_period": "2025-08至今"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "2025-08至今"},
    # Deputy mayors with mayor
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    # Predecessor relationships
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor", "context": "达娃次仁接替肖友才任拉萨市委书记", "overlap_org": "中共拉萨市委员会", "overlap_period": "2026-03"},
    {"person_a": 2, "person_b": 16, "type": "predecessor_successor", "context": "王强接替果果任拉萨市市长", "overlap_org": "拉萨市人民政府", "overlap_period": "2022-12"},
    # Deputy mayor group overlaps
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    # Aid cadre connections
    {"person_a": 3, "person_b": 13, "type": "overlap", "context": "同为江苏援藏干部", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "王强早期为北京援藏干部，李江新为江苏援藏干部", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "王强早期为北京援藏干部，张明智为北京援藏干部", "overlap_org": "拉萨市人民政府", "overlap_period": "current"},
]

# ── SQLite ─────────────────────────────────────────────────────────
def create_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '')""")


def insert_data(conn):
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     [p.get(k, "") for k in ["id","name","gender","ethnicity","birth","birthplace",
                                             "education","party_join","work_start","current_post",
                                             "current_org","source"]])
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     [o.get(k, "") for k in ["id","name","type","level","parent","location"]])
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                     [pos.get(k, "") for k in ["person_id","org_id","title","start_date","end_date","rank","note"]])
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                     [r.get(k, "") for k in ["person_a","person_b","type","context","overlap_org","overlap_period"]])
    conn.commit()


# ── GEXF ───────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    if p["id"] == 1:
        return "255,50,50"   # Party secretary - red
    elif p["id"] == 2:
        return "50,100,255"  # Mayor - blue
    elif p["id"] in (3, 4):
        return "255,165,0"   # Executive deputy mayors - orange
    else:
        return "100,100,100"  # Others - grey

def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 2)

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Government Personnel Network Investigator</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        if p["id"] > 14 and not p["name"]:
            continue  # skip unnamed predecessors
        sz = "20.0" if is_top_leader(p) else ("15.0" if p["id"] in (3, 4) else "12.0")
        c = person_color(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        insert_data(conn)
    finally:
        conn.close()
    build_gexf()
    print(f"Done. DB: {DB_PATH}")
    print(f"Done. GEXF: {GEXF_PATH}")
    print(f"Summary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")