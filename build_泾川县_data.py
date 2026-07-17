#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 泾川县 (Jingchuan County, Pingliang City, Gansu Province) leadership network.

Covers: Party Secretary (县委书记), County Mayor (县长), their predecessors/successors,
key deputy leaders, and cross-county exchange patterns.
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_泾川县")
DB_PATH = os.path.join(STAGING, "泾川县_network.db")
GEXF_PATH = os.path.join(STAGING, "泾川县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 刘懿平 — 泾川县委书记 (as of 2024.12)
    {"id":1,"name":"刘懿平","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"甘肃灵台","education":"省委党校研究生、农业推广硕士","party_join":"中共党员","work_start":"1995-07","current_post":"泾川县委书记","current_org":"中共泾川县委员会","source":"https://baike.baidu.com/item/%E5%88%98%E6%87%BF%E5%B9%B3/3553790"},
    # 郭凯 — 泾川县县长 (as of 2026)
    {"id":2,"name":"郭凯","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委副书记、县长","current_org":"泾川县人民政府","source":"https://www.jingchuan.gov.cn/"},

    # ── Predecessors — 县委书记 ──
    # 于宏勤 — 原泾川县委书记, 现任平凉市人大常委会副主任
    {"id":3,"name":"于宏勤","gender":"男","ethnicity":"汉族","birth":"1971-03","birthplace":"甘肃灵台","education":"中央党校函授经济管理专业、大学学历","party_join":"1997-05","work_start":"","current_post":"平凉市人大常委会党组成员、副主任（原泾川县委书记）","current_org":"平凉市人大常委会","source":"https://baike.baidu.com/item/%E4%BA%8E%E5%AE%8F%E5%8B%A4"},

    # ── Predecessors — 县长 (王德全 is the predecessor of 郭凯)
    {"id":4,"name":"王德全","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原泾川县长","current_org":"","source":"https://www.jingchuan.gov.cn/"},

    # ── 县委领导班子成员 ──
    {"id":5,"name":"李中尧","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委副书记","current_org":"中共泾川县委员会","source":"https://www.jingchuan.gov.cn/"},
    {"id":6,"name":"田庆银","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委常委、县政府常务副县长","current_org":"泾川县人民政府","source":"https://www.jingchuan.gov.cn/"},
    {"id":7,"name":"李永红","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委常委、县纪委书记、县监委主任","current_org":"中共泾川县纪律检查委员会","source":"https://www.jingchuan.gov.cn/"},
    {"id":8,"name":"徐爱平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委常委、组织部部长","current_org":"中共泾川县委组织部","source":"https://www.jingchuan.gov.cn/"},
    {"id":9,"name":"白亚军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委常委、宣传部部长","current_org":"中共泾川县委宣传部","source":"https://www.jingchuan.gov.cn/"},
    {"id":10,"name":"石佩奇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委常委、统战部部长","current_org":"中共泾川县委统战部","source":"https://www.jingchuan.gov.cn/"},
    {"id":11,"name":"靳姚平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委常委、政法委书记","current_org":"中共泾川县委政法委","source":"https://www.jingchuan.gov.cn/"},
    {"id":12,"name":"张伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县委常委、副县长","current_org":"泾川县人民政府","source":"https://www.jingchuan.gov.cn/"},

    # ── 县政府副县长 ──
    {"id":13,"name":"杨波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县副县长","current_org":"泾川县人民政府","source":"https://www.jingchuan.gov.cn/"},
    {"id":14,"name":"徐辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县副县长","current_org":"泾川县人民政府","source":"https://www.jingchuan.gov.cn/"},
    {"id":15,"name":"李杰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县副县长、县公安局局长","current_org":"泾川县人民政府","source":"https://www.jingchuan.gov.cn/"},
    {"id":16,"name":"张航","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县副县长","current_org":"泾川县人民政府","source":"https://www.jingchuan.gov.cn/"},

    # ── 人大、政协 ──
    {"id":17,"name":"朱卫华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"泾川县政协主席","current_org":"政协泾川县委员会","source":"https://www.jingchuan.gov.cn/"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共泾川县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市泾川县"},
    {"id":2,"name":"泾川县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市泾川县"},
    {"id":3,"name":"泾川县人大常委会","type":"人大","level":"县级","parent":"平凉市人大常委会","location":"甘肃省平凉市泾川县"},
    {"id":4,"name":"政协泾川县委员会","type":"政协","level":"县级","parent":"政协平凉市委员会","location":"甘肃省平凉市泾川县"},
    {"id":5,"name":"中共泾川县纪律检查委员会","type":"党委","level":"县级","parent":"中共泾川县委员会","location":"甘肃省平凉市泾川县"},
    {"id":6,"name":"中共泾川县委组织部","type":"党委","level":"县级","parent":"中共泾川县委员会","location":"甘肃省平凉市泾川县"},
    {"id":7,"name":"中共泾川县委宣传部","type":"党委","level":"县级","parent":"中共泾川县委员会","location":"甘肃省平凉市泾川县"},
    {"id":8,"name":"中共泾川县委统战部","type":"党委","level":"县级","parent":"中共泾川县委员会","location":"甘肃省平凉市泾川县"},
    {"id":9,"name":"中共泾川县委政法委","type":"党委","level":"县级","parent":"中共泾川县委员会","location":"甘肃省平凉市泾川县"},
    {"id":10,"name":"泾川县公安局","type":"政府","level":"县级","parent":"泾川县人民政府","location":"甘肃省平凉市泾川县"},

    # 刘懿平前工作相关机构
    {"id":11,"name":"中共灵台县新集乡委员会","type":"党委","level":"乡镇","parent":"中共灵台县委员会","location":"甘肃省平凉市灵台县"},
    {"id":12,"name":"灵台县人民政府办公室","type":"政府","level":"县级","parent":"灵台县人民政府","location":"甘肃省平凉市灵台县"},
    {"id":13,"name":"中共平凉市委办公室","type":"党委","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":14,"name":"共青团平凉市委员会","type":"群团","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":15,"name":"中共庄浪县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市庄浪县"},
    {"id":16,"name":"平凉市能源局","type":"政府","level":"地级","parent":"平凉市人民政府","location":"甘肃省平凉市"},
    {"id":17,"name":"中共平凉市崆峒区委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市崆峒区"},
    {"id":18,"name":"平凉市崆峒区人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市崆峒区"},

    # 于宏勤前工作相关机构（前任县委书记）
    {"id":19,"name":"平凉市疾病预防控制中心","type":"事业单位","level":"地级","parent":"平凉市卫生健康委员会","location":"甘肃省平凉市"},
    {"id":20,"name":"平凉市科学技术局","type":"政府","level":"地级","parent":"平凉市人民政府","location":"甘肃省平凉市"},
    {"id":21,"name":"平凉市市场监督管理局","type":"政府","level":"地级","parent":"平凉市人民政府","location":"甘肃省平凉市"},
    {"id":22,"name":"平凉市人大常委会","type":"人大","level":"地级","parent":"甘肃省人大常委会","location":"甘肃省平凉市"},

    # 王德全前工作相关
    {"id":23,"name":"平凉市文化广电和旅游局","type":"政府","level":"地级","parent":"平凉市人民政府","location":"甘肃省平凉市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 刘懿平 (id=1) ──
    {"pid":1,"org":1,"title":"泾川县委书记","start":"2024-12","end":"至今","rank":"正处级（二级巡视员）","note":"2024年12月2日泾川县领导干部大会宣布省委、市委决定"},
    {"pid":1,"org":17,"title":"崆峒区委副书记、区长、二级巡视员","start":"2019-01","end":"2024-12","rank":"正处级","note":"兼任崆峒区委副书记"},
    {"pid":1,"org":16,"title":"平凉市能源局局长","start":"2017-02","end":"2019-01","rank":"正处级","note":""},
    {"pid":1,"org":15,"title":"庄浪县委副书记（正县级）","start":"2012-08","end":"2017-02","rank":"正处级","note":""},
    {"pid":1,"org":14,"title":"共青团平凉市委书记","start":"2010-12","end":"2012-08","rank":"正处级","note":"2012.02-2012.05挂职福州市马尾区区长助理"},
    {"pid":1,"org":13,"title":"平凉市委副秘书长","start":"2010-04","end":"2010-12","rank":"副处级","note":""},
    {"pid":1,"org":13,"title":"平凉市委办公室副主任","start":"2007-07","end":"2010-04","rank":"副处级","note":""},
    {"pid":1,"org":13,"title":"平凉市委办公室干部（历任副科级秘书、秘书科科长）","start":"1997-11","end":"2007-07","rank":"正科级","note":"1999.11任副科级秘书；2002.12任秘书科科长"},
    {"pid":1,"org":12,"title":"灵台县政府办公室干部","start":"1996-07","end":"1997-11","rank":"","note":""},
    {"pid":1,"org":11,"title":"灵台县新集乡党委干部","start":"1995-07","end":"1996-07","rank":"","note":""},

    # ── 郭凯 (id=2) ──
    {"pid":2,"org":2,"title":"泾川县委副书记、县长","start":"","end":"至今","rank":"正处级","note":"现任泾川县县长"},
    {"pid":2,"org":2,"title":"泾川县委副书记、代县长","start":"","end":"","rank":"正处级","note":""},

    # ── 于宏勤 (id=3) ──
    {"pid":3,"org":22,"title":"平凉市人大常委会党组成员、副主任","start":"2025-02","end":"至今","rank":"副厅级","note":""},
    {"pid":3,"org":1,"title":"泾川县委书记","start":"2021-08","end":"2024-12","rank":"正处级","note":"晋升二级巡视员"},
    {"pid":3,"org":21,"title":"平凉市市场监督管理局局长","start":"2019-01","end":"2021-08","rank":"正处级","note":""},
    {"pid":3,"org":20,"title":"平凉市科学技术局局长","start":"2018-06","end":"2019-01","rank":"正处级","note":""},
    {"pid":3,"org":19,"title":"平凉市疾病预防控制中心主任","start":"2017-04","end":"2018-06","rank":"正处级","note":""},

    # ── 王德全 (id=4) ── 前任县长
    {"pid":4,"org":2,"title":"泾川县委副书记、县长","start":"","end":"","rank":"正处级","note":"前任泾川县长"},
    {"pid":4,"org":23,"title":"平凉市文化广电和旅游局局长","start":"","end":"","rank":"正处级","note":"此前任职"},
    {"pid":4,"org":15,"title":"庄浪县委副书记","start":"","end":"","rank":"副处级","note":""},

    # ── 李中尧 (id=5) ──
    {"pid":5,"org":1,"title":"泾川县委副书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 田庆银 (id=6) ──
    {"pid":6,"org":2,"title":"泾川县委常委、常务副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李永红 (id=7) ──
    {"pid":7,"org":5,"title":"泾川县委常委、纪委书记、监委主任","start":"","end":"至今","rank":"副处级","note":""},

    # ── 徐爱平 (id=8) ──
    {"pid":8,"org":6,"title":"泾川县委常委、组织部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 白亚军 (id=9) ──
    {"pid":9,"org":7,"title":"泾川县委常委、宣传部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 石佩奇 (id=10) ──
    {"pid":10,"org":8,"title":"泾川县委常委、统战部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 靳姚平 (id=11) ──
    {"pid":11,"org":9,"title":"泾川县委常委、政法委书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张伟 (id=12) ──
    {"pid":12,"org":2,"title":"泾川县委常委、副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 杨波 (id=13) ──
    {"pid":13,"org":2,"title":"泾川县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 徐辉 (id=14) ──
    {"pid":14,"org":2,"title":"泾川县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李杰 (id=15) ──
    {"pid":15,"org":10,"title":"泾川县副县长、县公安局局长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张航 (id=16) ──
    {"pid":16,"org":2,"title":"泾川县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 朱卫华 (id=17) ──
    {"pid":17,"org":4,"title":"泾川县政协主席","start":"","end":"至今","rank":"正处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 刘懿平 ↔ 于宏勤 (predecessor-successor, 县委书记)
    {"a":1,"b":3,"type":"predecessor_successor","context":"刘懿平于2024年12月接替于宏勤担任泾川县委书记","overlap_org":"中共泾川县委员会","overlap_period":"2024-12","strength":"strong","confidence":"confirmed"},

    # 刘懿平 ↔ 郭凯 (current party secretary - county mayor, 党政搭档)
    {"a":1,"b":2,"type":"overlap","context":"刘懿平任县委书记，郭凯任县长，党政搭档","overlap_org":"中共泾川县委员会、泾川县人民政府","overlap_period":"至今","strength":"strong","confidence":"confirmed"},

    # 于宏勤 ↔ 王德全 (前县委书记与前县长搭档)
    {"a":3,"b":4,"type":"overlap","context":"于宏勤任县委书记期间，王德全任县长，党政搭档","overlap_org":"中共泾川县委员会、泾川县人民政府","overlap_period":"2021-2024","strength":"strong","confidence":"confirmed"},

    # 刘懿平 ↔ 李中尧 (县委书记 - 副书记)
    {"a":1,"b":5,"type":"superior_subordinate","context":"刘懿平任县委书记，李中尧任县委副书记","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 田庆银 (县委书记 - 常务副县长)
    {"a":1,"b":6,"type":"superior_subordinate","context":"刘懿平任县委书记，田庆银任县委常委、常务副县长","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 李永红
    {"a":1,"b":7,"type":"superior_subordinate","context":"刘懿平任县委书记，李永红任县纪委书记","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 徐爱平
    {"a":1,"b":8,"type":"superior_subordinate","context":"刘懿平任县委书记，徐爱平任县委组织部部长","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 白亚军
    {"a":1,"b":9,"type":"superior_subordinate","context":"刘懿平任县委书记，白亚军任县委宣传部部长","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 石佩奇
    {"a":1,"b":10,"type":"superior_subordinate","context":"刘懿平任县委书记，石佩奇任县委统战部部长","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 靳姚平
    {"a":1,"b":11,"type":"superior_subordinate","context":"刘懿平任县委书记，靳姚平任县委政法委书记","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 张伟
    {"a":1,"b":12,"type":"superior_subordinate","context":"刘懿平任县委书记，张伟任县委常委、副县长","overlap_org":"中共泾川县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 郭凯 ↔ 田庆银 (县长 - 常务副县长)
    {"a":2,"b":6,"type":"superior_subordinate","context":"郭凯任县长，田庆银任常务副县长","overlap_org":"泾川县人民政府","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 郭凯 ↔ 王德全 (predecessor-successor, 县长)
    {"a":2,"b":4,"type":"predecessor_successor","context":"郭凯接替王德全担任泾川县长","overlap_org":"泾川县人民政府","overlap_period":"","strength":"strong","confidence":"confirmed"},

    # 于宏勤 ↔ 郭凯 (前县委书记与现任县长)
    {"a":3,"b":2,"type":"overlap","context":"于宏勤任县委书记期间与郭凯曾同为县领导","overlap_org":"中共泾川县委员会","overlap_period":"","strength":"medium","confidence":"plausible"},

    # 刘懿平与于宏勤同籍贯（均为灵台人）
    {"a":1,"b":3,"type":"same_native","context":"刘懿平与于宏勤均为甘肃灵台人，系同籍贯","overlap_org":"","overlap_period":"","strength":"weak","confidence":"confirmed"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["pid"], str(pos["org"]), pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["a"], r["b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")

    # Stats
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    print(f"  Persons: {conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        current = p.get("current_post", "")
        if "书记" in current and "纪委" not in current and "人大" not in current and "政协" not in current:
            return "255,50,50"  # Red — party secretary
        if "县长" in current or "区长" in current or "副市长" in current or "人大" in current:
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "政协" in current:
            return "255,240,200"  # Cream - CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        if name in ("刘懿平", "郭凯", "于宏勤"):
            return "20.0"
        if name in ("王德全",):
            return "15.0"
        return "12.0"

    def org_color(o):
        t = o.get("type", "")
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        if "群团" in t:
            return "255,220,255"
        if "事业" in t:
            return "220,220,220"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>泾川县领导班子工作关系网络 — 中共泾川县委、泾川县人民政府及跨县人事交流</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "未知")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        c = org_color(o)
        oid = str(o["id"]) if isinstance(o["id"], int) else o["id"]
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Position edges: person -> organization
    for pos in positions:
        eid += 1
        oid = str(pos["org"]) if isinstance(pos["org"], int) else pos["org"]
        period = f"{pos['start']} - {pos['end']}" if pos['start'] else ""
        lines.append(f'      <edge id="e{eid}" source="p{pos["pid"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges: person <-> person
    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["a"]}" target="p{r["b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}")
    print(f"  Edges: {eid}")


if __name__ == "__main__":
    build_database()
    build_gexf()
    print("\nDone. Generated artifacts:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
