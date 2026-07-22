#!/usr/bin/env python3
"""
Build 定南县 (Dingnan County) government personnel network database and GEXF graph.

定南县 is a county under 赣州市, 江西省.
Current leadership as of 2026-07-15:
- 龙小东: 定南县委书记 (Party Secretary)
- 陈钰滢: 定南县委副书记、县长 (County Mayor)
- 邝冬明: 县委常委、常务副县长 (Executive Deputy County Mayor)

Predecessor chain: 赖正文 → 龙小东 → 陈钰滢 (transition)

Sources:
- Official government site www.dingnan.gov.cn leadership pages (fetched 2026-07-15)
- 定南县 homepage news articles (June-July 2026)

This script generates:
- data/database/定南县_network.db (SQLite database)
- data/graph/定南县_network.gexf (GEXF graph for Gephi)
"""
import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = BASE

today = datetime.now().strftime("%Y-%m-%d")

DB_REL = "定南县_network.db"
GEXF_REL = "定南县_network.gexf"

DB_PATH = os.path.join(STAGING_DIR, DB_REL)
GEXF_PATH = os.path.join(STAGING_DIR, GEXF_REL)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ---- Core Leaders ----
    {
        "id": 1,
        "name": "龙小东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "江西赣州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委书记",
        "current_org": "中共定南县委员会",
        "source": "http://www.dingnan.gov.cn/ homepage news articles (June 2026); 旧数据库记录/公开报道",
    },
    {
        "id": 2,
        "name": "陈钰滢",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-02",
        "birthplace": "江西赣州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1996-11",
        "current_post": "定南县委副书记、县长",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202212/fe1938fc525449308633cff4b50be070.shtml",
    },
    {
        "id": 3,
        "name": "邝冬明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "江西赣州",
        "education": "研究生学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委常委、常务副县长",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124986/202212/6dbdb1e1aa3f4d9e843dfba5cbcff87f.shtml",
    },
    # ---- Standing Committee Members (县委领导) ----
    {
        "id": 4,
        "name": "刘金阁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委副书记、副县长（挂职）",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202409/b7650dd55e794f2f8e6ca9a73e58b1d2.shtml",
    },
    {
        "id": 5,
        "name": "刘鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-07",
        "birthplace": "江西瑞金",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2003-07",
        "current_post": "定南县委常委、宣传部部长",
        "current_org": "中共定南县委宣传部",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202212/9ef16eb89f40421c8e77415794f5881a.shtml",
    },
    {
        "id": 6,
        "name": "杨鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-12",
        "birthplace": "河北晋州",
        "education": "大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "2008-01",
        "current_post": "定南县委常委、政法委书记",
        "current_org": "中共定南县委政法委员会",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202212/6c0e179240c74a4aa61a9d33a23b7017.shtml",
    },
    {
        "id": 7,
        "name": "刘成成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-06",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委常委、组织部部长",
        "current_org": "中共定南县委组织部",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202212/ed1943eda1f4495e9ebb471cbef45402.shtml",
    },
    {
        "id": 8,
        "name": "黄海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委常委、统战部部长",
        "current_org": "中共定南县委统战部",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202403/ea35363c702d47e6972e039afe0adcf9.shtml",
    },
    {
        "id": 9,
        "name": "郭玉峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委常委、纪委书记、监委主任",
        "current_org": "中共定南县纪律检查委员会",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202212/9729d219c845495ebdaa63c76d3809cc.shtml",
    },
    {
        "id": 10,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委常委（挂职）",
        "current_org": "中共定南县委员会",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202409/6357026b2e304011aadff2f2e86e0a42.shtml",
    },
    {
        "id": 11,
        "name": "张俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-02",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县委常委、县人武部上校部长",
        "current_org": "定南县人武部",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124984/202212/b3e6da86a04a49bfa5fc6b1c08a3288b.shtml",
    },
    # ---- County Government Leaders (县政府领导) ----
    {
        "id": 12,
        "name": "廖为星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县政府副县长",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124986/202212/a3dc42126e2d4d619d5e92450895791c.shtml",
    },
    {
        "id": 13,
        "name": "蓝启玉",
        "gender": "女",
        "ethnicity": "畲族",
        "birth": "1985-09",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "定南县政府副县长",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124986/202212/fc9563e50cc246a8bf457916ab125855.shtml",
    },
    {
        "id": 14,
        "name": "温春荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-01",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县政府副县长",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124986/202303/3ed4959057b849608b4ccc62e6fabacc.shtml",
    },
    {
        "id": 15,
        "name": "龙林峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-01",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县政府副县长",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124986/202509/656b2c0954824066be2beb89464dbac9.shtml",
    },
    {
        "id": 16,
        "name": "孙鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县政府副县长、公安局局长",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124986/202212/c6b5d5eca4574f389116095d37a446bc.shtml",
    },
    {
        "id": 17,
        "name": "黄日强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定南县政府副县长、党组成员",
        "current_org": "定南县人民政府",
        "source": "http://www.dingnan.gov.cn/dnxxxgk/c124986/202603/d3ed08562f2341309f0e7467f34443d6.shtml",
    },
    # ---- Predecessors ----
    {
        "id": 18,
        "name": "赖正文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原定南县委书记）",
        "current_org": "",
        "source": "定南县2021年8月党政主要领导职务调整公告；赖正文~2021年卸任定南县委书记，龙小东接任",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共定南县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共赣州市委员会",
        "location": "江西赣州定南",
    },
    {
        "id": 2,
        "name": "定南县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "赣州市人民政府",
        "location": "江西赣州定南",
    },
    {
        "id": 3,
        "name": "中共定南县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定南县委员会",
        "location": "江西赣州定南",
    },
    {
        "id": 4,
        "name": "中共定南县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定南县委员会",
        "location": "江西赣州定南",
    },
    {
        "id": 5,
        "name": "中共定南县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定南县委员会",
        "location": "江西赣州定南",
    },
    {
        "id": 6,
        "name": "中共定南县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定南县委员会",
        "location": "江西赣州定南",
    },
    {
        "id": 7,
        "name": "中共定南县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定南县委员会",
        "location": "江西赣州定南",
    },
    {
        "id": 8,
        "name": "定南县人武部",
        "type": "政府",
        "level": "县处级",
        "parent": "赣州军分区",
        "location": "江西赣州定南",
    },
]

positions = [
    # 龙小东 — 县委书记
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "定南县委书记",
        "start": "2021",
        "end": "",
        "rank": "县处级正职",
        "note": "现任。2021年接替赖正文任定南县委书记。省委党校研究生，1971年11月生。",
    },
    # 陈钰滢 — 县委副书记
    {
        "id": 2,
        "person_id": 2,
        "org_id": 1,
        "title": "定南县委副书记",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。同时兼任县长。",
    },
    # 陈钰滢 — 县长
    {
        "id": 3,
        "person_id": 2,
        "org_id": 2,
        "title": "定南县长",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "现任。2026年政府工作报告以县长身份签名。2026年7月14日以县委副书记、县长身份主持县委常委会（扩大）会议。",
    },
    # 邝冬明
    {
        "id": 4,
        "person_id": 3,
        "org_id": 2,
        "title": "定南县委常委、常务副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。负责县政府常务工作。1984年10月生，研究生学历，工程硕士。",
    },
    # 刘金阁（挂职）
    {
        "id": 5,
        "person_id": 4,
        "org_id": 2,
        "title": "定南县委副书记、副县长（挂职）",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "挂职。来自中国进出口银行。",
    },
    # 刘鹏
    {
        "id": 6,
        "person_id": 5,
        "org_id": 3,
        "title": "定南县委常委、宣传部部长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。江西瑞金人，1981年7月生，2003年7月参加工作。",
    },
    # 杨鹏飞
    {
        "id": 7,
        "person_id": 6,
        "org_id": 4,
        "title": "定南县委常委、政法委书记",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。河北晋州人，1983年12月生，2008年1月参加工作。",
    },
    # 刘成成
    {
        "id": 8,
        "person_id": 7,
        "org_id": 5,
        "title": "定南县委常委、组织部部长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。1978年6月生。",
    },
    # 黄海
    {
        "id": 9,
        "person_id": 8,
        "org_id": 6,
        "title": "定南县委常委、统战部部长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。",
    },
    # 郭玉峰
    {
        "id": 10,
        "person_id": 9,
        "org_id": 7,
        "title": "定南县委常委、纪委书记、监委主任",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。",
    },
    # 张斌（挂职）
    {
        "id": 11,
        "person_id": 10,
        "org_id": 1,
        "title": "定南县委常委（挂职）",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "挂职。负责普惠金融方面工作。",
    },
    # 张俊
    {
        "id": 12,
        "person_id": 11,
        "org_id": 8,
        "title": "定南县委常委、县人武部上校部长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。1977年2月生。",
    },
    # 廖为星
    {
        "id": 13,
        "person_id": 12,
        "org_id": 2,
        "title": "定南县政府副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。负责工业、商务等。1984年10月生。",
    },
    # 蓝启玉
    {
        "id": 14,
        "person_id": 13,
        "org_id": 2,
        "title": "定南县政府副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。无党派。1985年9月生，畲族。",
    },
    # 温春荣
    {
        "id": 15,
        "person_id": 14,
        "org_id": 2,
        "title": "定南县政府副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。负责农业农村、水利等。1982年1月生。",
    },
    # 龙林峰
    {
        "id": 16,
        "person_id": 15,
        "org_id": 2,
        "title": "定南县政府副县长",
        "start": "2025",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。1987年1月生。2025年任副县长。",
    },
    # 孙鹏
    {
        "id": 17,
        "person_id": 16,
        "org_id": 2,
        "title": "定南县政府副县长、公安局局长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。1979年5月生。兼公安局党委书记、局长。",
    },
    # 黄日强
    {
        "id": 18,
        "person_id": 17,
        "org_id": 2,
        "title": "定南县政府副县长",
        "start": "2026",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年任副县长，负责住建、自然资源等。",
    },
    # 赖正文（前任县委书记）
    {
        "id": 19,
        "person_id": 18,
        "org_id": 1,
        "title": "定南县委书记（前任）",
        "start": "",
        "end": "2021-08",
        "rank": "县处级正职",
        "note": "前任县委书记。~2021年8月卸任，由龙小东接替。出生年月、籍贯、完整履历待查。去向待查。",
    },
]

relationships = [
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政搭档",
        "context": "龙小东（县委书记）与陈钰滢（县委副书记、县长）为定南县党政正职搭档关系",
        "overlap_org": "定南县",
        "overlap_period": "现任",
    },
    {
        "id": 2,
        "person_a_id": 2,
        "person_b_id": 3,
        "type": "党政搭档",
        "context": "陈钰滢（县长）与邝冬明（常务副县长）为定南县党政正副职搭档关系",
        "overlap_org": "定南县人民政府",
        "overlap_period": "现任",
    },
    {
        "id": 3,
        "person_a_id": 1,
        "person_b_id": 18,
        "type": "前任接任",
        "context": "赖正文为前任定南县委书记（~2021年8月卸任），龙小东接任",
        "overlap_org": "中共定南县委员会",
        "overlap_period": "2021",
    },
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    post = post or ""
    if "书记" in post and ("县委" in post or "党委" in post):
        return "230,50,50"
    if "县长" in post or "区长" in post:
        if "副" not in post:
            return "50,100,230"
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    return "120,120,120"


def ocolor_viz(otype):
    return {"党委": "255,200,200", "政府": "200,200,255"}.get(otype, "200,200,200")


def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    return counts


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus-junior</creator>')
    lines.append(f'    <description>定南县领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c_val = pcolor_viz(p.get("current_post", ""))
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")), ("2", p.get("birthplace", "")),
                      ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c_val = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""), ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start", "")), ("2", pos.get("end", "")),
                      ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("定南县 Government Personnel Network Builder")
    print(f"Date: {today}")
    print("=" * 60)

    print(f"\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    print(f"\n▶ Building GEXF graph...")
    tn, te = build_gexf()
    print(f"  ✓ {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    import sys
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"DB file not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF file not created: {GEXF_PATH}")

    if errors:
        print(f"\n✗ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\n✓ BUILD COMPLETE - All artifacts created successfully")
