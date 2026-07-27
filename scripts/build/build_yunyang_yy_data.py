#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 郧阳区 (Yunyang District), 十堰市, 湖北省."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yunyang_yy_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yunyang_yy_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ── Current District Committee Secretary (Party) ──
    {"id": 1, "name": "梅华", "gender": "男", "ethnicity": "土家族",
     "birth": "1975-04", "birthplace": "湖北省恩施州建始县", "education": "硕士研究生",
     "party_join": "1997-04", "work_start": "1998-07",
     "current_post": "十堰市郧阳区委书记、一级调研员", "current_org": "中共十堰市郧阳区委员会",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502378.shtml"},

    # ── Current District Mayor ──
    {"id": 2, "name": "刘伟华", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-03", "birthplace": "山东省潍坊市", "education": "研究生/工学博士",
     "party_join": "2003-12", "work_start": "2004-07",
     "current_post": "十堰市郧阳区委副书记、区长", "current_org": "十堰市郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202505/t20250508_4736615.shtml"},

    # ── Deputy Party Secretary ──
    {"id": 3, "name": "董会祥", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "十堰市郧阳区", "education": "党校大学",
     "party_join": "1998-04", "work_start": "1994-09",
     "current_post": "十堰市郧阳区委副书记、区委政法委书记、三级调研员", "current_org": "中共十堰市郧阳区委员会",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654540.shtml"},

    # ── Executive Deputy Mayor ──
    {"id": 4, "name": "刘群", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-03", "birthplace": "湖北省竹溪县", "education": "省委党校研究生",
     "party_join": "2000-05", "work_start": "1995-11",
     "current_post": "十堰市郧阳区委常委、常务副区长", "current_org": "十堰市郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502470.shtml"},

    # ── United Front Work Director ──
    {"id": 5, "name": "雷涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-05", "birthplace": "十堰市郧阳区", "education": "党校研究生",
     "party_join": "2001-05", "work_start": "1999-10",
     "current_post": "十堰市郧阳区委常委、统战部部长、总工会主席", "current_org": "中共十堰市郧阳区委员会",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654545.shtml"},

    # ── Party Committee Office Director ──
    {"id": 6, "name": "柯相国", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "十堰市郧阳区", "education": "农业推广硕士",
     "party_join": "1998-03", "work_start": "1995-09",
     "current_post": "十堰市郧阳区委常委、区委办公室主任", "current_org": "中共十堰市郧阳区委员会",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654548.shtml"},

    # ── Discipline Inspection Secretary ──
    {"id": 7, "name": "王凡", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-04", "birthplace": "湖北省郧西县", "education": "省委党校研究生",
     "party_join": "2005-01", "work_start": "2005-07",
     "current_post": "十堰市郧阳区委常委、纪委书记、监委主任", "current_org": "中共十堰市郧阳区纪律检查委员会",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502477.shtml"},

    # ── Propaganda Department Director ──
    {"id": 8, "name": "卢金华", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-12", "birthplace": "河南省开封市", "education": "法学硕士",
     "party_join": "2006-05", "work_start": "2011-09",
     "current_post": "十堰市郧阳区委常委、宣传部部长", "current_org": "中共十堰市郧阳区委员会",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502460.shtml"},

    # ── Vice District Mayor (Standing Committee) ──
    {"id": 9, "name": "王俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-01", "birthplace": "十堰市郧阳区", "education": "大学",
     "party_join": "2001-10", "work_start": "1996-12",
     "current_post": "十堰市郧阳区委常委、副区长", "current_org": "十堰市郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220516_3503477.shtml"},

    # ── Organization Department Director ──
    {"id": 10, "name": "王一鸣", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-02", "birthplace": "湖北省郧西县", "education": "省委党校研究生",
     "party_join": "2010-12", "work_start": "2008-07",
     "current_post": "十堰市郧阳区委常委、组织部部长", "current_org": "中共十堰市郧阳区委员会",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502440.shtml"},

    # ── Vice District Mayor (Ethnic) ──
    {"id": 11, "name": "韦燕珍", "gender": "男", "ethnicity": "壮族",
     "birth": "1979-11", "birthplace": "广西崇左市", "education": "大学",
     "party_join": "2001-04", "work_start": "2002-07",
     "current_post": "十堰市郧阳区委常委、副区长", "current_org": "十堰市郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654543.shtml"},

    # ── Vice District Mayor (Beijing origin) ──
    {"id": 12, "name": "王铭", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-09", "birthplace": "北京市东城区", "education": "党校研究生",
     "party_join": "2005-01", "work_start": "2002-07",
     "current_post": "十堰市郧阳区委常委、副区长", "current_org": "十堰市郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241209_4655599.shtml"},

    # ── Former Party Secretaries ──
    {"id": 13, "name": "胡先平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "去向待查", "current_org": "",
     "source": "https://search.cctv.com/search.php?qtext=胡先平+郧阳+区委书记"},

    {"id": 14, "name": "孙道军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "1996",  # 1996年大学毕业
     "current_post": "去向待查", "current_org": "",
     "source": "https://search.cctv.com/search.php?qtext=孙道军+十堰"},
]

organizations = [
    {"id": 1, "name": "中共十堰市郧阳区委员会", "type": "党委", "level": "县级行政区",
     "parent": "中共十堰市委", "location": "湖北省十堰市郧阳区"},
    {"id": 2, "name": "十堰市郧阳区人民政府", "type": "政府", "level": "县级行政区",
     "parent": "十堰市人民政府", "location": "湖北省十堰市郧阳区"},
    {"id": 3, "name": "中共十堰市郧阳区纪律检查委员会", "type": "纪委", "level": "县级行政区",
     "parent": "中共十堰市纪委", "location": "湖北省十堰市郧阳区"},
]

positions = [
    # Current leaders at 区委
    {"person_id": 1, "org_id": 1, "title": "区委书记、一级调研员", "start": "", "end": "", "rank": "正县级", "note": "在任"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start": "2024", "end": "", "rank": "正县级", "note": "在任"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记、区委政法委书记", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、统战部部长", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 6, "org_id": 1, "title": "区委常委、区委办公室主任", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 7, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 8, "org_id": 1, "title": "区委常委、宣传部部长", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 9, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 10, "org_id": 1, "title": "区委常委、组织部部长", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 11, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "", "rank": "副县级", "note": "在任"},
    {"person_id": 12, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "", "rank": "副县级", "note": "在任"},

    # Former leaders
    {"person_id": 13, "org_id": 1, "title": "区委书记", "start": "2021", "end": "~2023/2024", "rank": "正县级", "note": "前任"},
    {"person_id": 13, "org_id": 2, "title": "区长", "start": "~2017", "end": "2021", "rank": "正县级", "note": "以前任区长身份升书记"},
    {"person_id": 14, "org_id": 1, "title": "区委书记", "start": "~2014", "end": "~2021", "rank": "正县级", "note": "前任的书记"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记+区长（当前郧阳区党政一把手）",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记+区委副书记",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长+常务副区长（政府运行线）",
     "overlap_org": "十堰市郧阳区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记+区委办主任（办公厅行政线）",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "书记+组织部长（干部管理线）",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "书记+纪委书记（监督线）",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "工作协同", "context": "政法委书记+纪委书记（政法+纪检协同）",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 13, "person_b": 14, "type": "前后任", "context": "胡先平接替孙道军任郧阳区委书记",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": "~2021"},
    {"person_a": 13, "person_b": 1, "type": "前后任", "context": "梅华接替胡先平任郧阳区委书记",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": "~2023-2024"},
    {"person_a": 2, "person_b": 8, "type": "跨省同僚", "context": "刘伟华（山东潍坊人）与卢金华（河南开封人），均非湖北籍",
     "overlap_org": "十堰市郧阳区人民政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 7, "type": "同乡", "context": "王一鸣（郧西人）与王凡（郧西人），同乡关系",
     "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
]

# ── BUILD DATABASE ─────────────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT,
        source TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✓ Database built: {DB_PATH}")
    print(f"  - {len(persons)} persons")
    print(f"  - {len(organizations)} organizations")
    print(f"  - {len(positions)} positions")
    print(f"  - {len(relationships)} relationships")

# ── BUILD GEXF ─────────────────────────────────────────────────────────────

def build_gexf():
    ns = 'xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz"'

    # Node colors by role
    def node_color(person_id):
        # red=party secretary, blue=government, orange=discipline, grey=other
        colors = {
            1:  "r=\"220\" g=\"40\" b=\"40\"",     # 梅华 - red (party secretary)
            2:  "r=\"40\" g=\"100\" b=\"200\"",    # 刘伟华 - blue (government)
            3:  "r=\"100\" g=\"100\" b=\"100\"",   # 董会祥 - grey (deputy)
            4:  "r=\"40\" g=\"100\" b=\"200\"",    # 刘群 - blue (gov)
            5:  "r=\"100\" g=\"100\" b=\"100\"",   # 雷涛 - grey
            6:  "r=\"100\" g=\"100\" b=\"100\"",   # 柯相国 - grey
            7:  "r=\"240\" g=\"140\" b=\"30\"",    # 王凡 - orange (discipline)
            8:  "r=\"100\" g=\"100\" b=\"100\"",   # 卢金华 - grey
            9:  "r=\"100\" g=\"100\" b=\"100\"",   # 王俊 - grey
            10: "r=\"100\" g=\"100\" b=\"100\"",   # 王一鸣 - grey
            11: "r=\"100\" g=\"100\" b=\"100\"",   # 韦燕珍 - grey
            12: "r=\"100\" g=\"100\" b=\"100\"",   # 王铭 - grey
            13: "r=\"160\" g=\"160\" b=\"160\"",   # 胡先平 - light grey (former)
            14: "r=\"160\" g=\"160\" b=\"160\"",   # 孙道军 - light grey (former)
        }
        return colors.get(person_id, "r=\"180\" g=\"180\" b=\"180\"")

    def node_size(person_id):
        return "20.0" if person_id <= 2 else "12.0"

    nodes_xml = ""
    for p in persons:
        color = node_color(p["id"])
        size = node_size(p["id"])
        label = f"{p['name']}\n{p['current_post']}"
        nodes_xml += f'''      <node id="{p['id']}" label="{label}">
        <viz:color {color}/>
        <viz:size value="{size}"/>
        <attvalues>
          <attvalue for="birthplace" value="{p['birthplace']}"/>
          <attvalue for="ethnicity" value="{p['ethnicity']}"/>
          <attvalue for="education" value="{p['education']}"/>
        </attvalues>
      </node>\n'''

    # Organization nodes
    org_colors = {
        1: "r=\"200\" g=\"50\" b=\"50\"",     # committee - red
        2: "r=\"50\" g=\"100\" b=\"200\"",    # gov - blue
        3: "r=\"200\" g=\"120\" b=\"20\"",    # discipline - orange
    }
    org_xml = ""
    for o in organizations:
        oc = org_colors.get(o["id"], "r=\"150\" g=\"150\" b=\"150\"")
        org_xml += f'''      <node id="org_{o['id']}" label="{o['name']}">
        <viz:color {oc}/>
        <viz:size value="8.0"/>
        <viz:shape value="square"/>
      </node>\n'''

    # Person-Org edges (worked_at)
    pos_edges = ""
    for pos in positions:
        pid = pos["person_id"]
        oid = f"org_{pos['org_id']}"
        label = pos["title"]
        pos_edges += f'''      <edge source="{pid}" target="{oid}" label="{label}" type="directed">
        <attvalues>
          <attvalue for="type" value="worked_at"/>
          <attvalue for="title" value="{label}"/>
        </attvalues>
      </edge>\n'''

    # Person-Person edges (relationship)
    rel_edges = ""
    for r in relationships:
        label = f"{r['type']}: {r['context'][:40]}"
        rel_edges += f'''      <edge source="{r['person_a']}" target="{r['person_b']}" label="{label}" type="undirected">
        <attvalues>
          <attvalue for="type" value="relationship"/>
          <attvalue for="context" value="{r['context']}"/>
        </attvalues>
      </edge>\n'''

    gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf {ns}>
  <meta>
    <creator>gov-relation research</creator>
    <description>郧阳区领导班子工作关系网络 - {datetime.now().strftime('%Y-%m-%d')}</description>
  </meta>
  <graph mode="static" defaultedgetype="directed">
    <attributes class="node">
      <attribute id="birthplace" title="籍贯" type="string"/>
      <attribute id="ethnicity" title="民族" type="string"/>
      <attribute id="education" title="学历" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="关系类型" type="string"/>
      <attribute id="title" title="职务/关系说明" type="string"/>
      <attribute id="context" title="详细描述" type="string"/>
    </attributes>
    <nodes>
{nodes_xml}{org_xml}    </nodes>
    <edges>
{pos_edges}{rel_edges}    </edges>
  </graph>
</gexf>"""

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf)
    print(f"✓ GEXF graph built: {GEXF_PATH}")

# ── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("\nDone. Summary:")
    print(f"  Database: {DB_PATH}")
    print(f"  Graph:    {GEXF_PATH}")
