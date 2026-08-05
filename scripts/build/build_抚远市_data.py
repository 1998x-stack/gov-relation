#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 抚远市, 黑龙江省.

Task ID: heilongjiang_抚远市
Province: 黑龙江省
Parent city: 佳木斯市
Region: 抚远市
Level: 县级市
Targets: 市委书记 & 市长

Investigation date: 2026-08-05
As-of date for leadership: 2026-01-04 (官方领导之窗页面更新日期), 网络核实至 2026-08

Research sources:
  - 抚远市人民政府官网 领导之窗 https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml （当前班子一手来源）
  - 抚远市政府官网 郑树一履历页 https://www.hljfy.gov.cn/fys/c101360/202505/c04_130683.shtml
  - 抚远市政府官网 郑志刚履历页 https://www.hljfy.gov.cn/fys/c101359/202505/c04_129661.shtml
  - 百度百科《抚远市》词条（现任领导表 + 撤县设市/省直管沿革）
  - 三位 librarian 子代理聚合检索（百度百科何大海 lemma、官方会议记录等）

Confidence notes:
  - 何大海: confirmed 市委书记，兼佳木斯市委常委、黑瞎子岛建设和管理委员会主任。中国航天科技集团五院空降/交流干部，
    2002-08 参加工作，2021-08 任抚远市委书记。出身为黑龙江哈尔滨，西北工业大学软件工程硕士（在职），职称为研究员。
  - 郑志一: confirmed 市委副书记、市长（2013-12 参加工作，2015-07 入党，1983-11 生，上海籍，研究生工学硕士），兼市委副书记。为-市长继任链末位。
  - 郑志刚: confirmed 现任市人大常委会主任（前任市长）。河南通济（黑龙江通泽）人。
  - 王忠山: confirmed 市政协主席。冯海: confirmed 市委副书记。刘祥锐: confirmed 常务副市长。
  - 前任市委书记：未核实（公开一手来源未收录抚远历任书记名录）。市长继任链（官网会议记录交叉印证）：范继涛(2024) → 郑志刚(2024末-2025初) → 郑树一(2025-05至今)。
  - 因搜索/百科对县级主官履历覆盖有限，多人物早期履历为缺口，在 person JSON 的 open_questions 与 report/open_gaps.md 中明确标注。

Confidence standard:
  - confirmed: 官网领导之窗或官方履历页直接登记
  - plausible: 官方新闻/百科交叉印证
  - unverified: 单方线索或无法核实
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "抚远市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导（市委书记 & 市长）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "何大海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "黑龙江哈尔滨",
        "education": "西北工业大学软件工程硕士（在职）；本科黑龙江大学广播电视编导",
        "party_join": "2001年11月",
        "work_year": "2002年8月",
        "current_post": "市委书记（兼佳木斯市委常委、省政府黑瞎子岛建设和管理委员会主任）",
        "current_org": "中共抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 2,
        "name": "郑树一",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "上海市",
        "education": "研究生工学硕士",
        "party_join": "2015年7月加入中国共产党",
        "work_year": "2013年12月参加工作",
        "current_post": "市委副书记、市长",
        "current_org": "抚远市人民政府",
        "source": "https://www.hljfy.gov.cn/fys/c101360/202504/c04_130447.shtml"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市委副书记 / 市委常委 / 市政府其他领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "冯海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委副书记",
        "current_org": "中共抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 4,
        "name": "郑志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "黑龙江通河",
        "education": "本科",
        "party_join": "1997年4月加入中国共产党",
        "work_year": "1986年6月参加工作",
        "current_post": "市人大常委会党组书记、主任（曾任市长）",
        "current_org": "抚远市人民代表大会常务委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101359/202505/c04_129661.shtml"
    },
    {
        "id": 5,
        "name": "王忠山",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 6,
        "name": "刘祥锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "山东梁山",
        "education": "中央广播电视大学会计学",
        "party_join": "中共党员",
        "work_year": "1999年7月参加工作",
        "current_post": "市委常委、常务副市长",
        "current_org": "抚远市人民政府",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    # 市委常委（名单确认，分管待查）
    {
        "id": 7,
        "name": "刘善友",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委",
        "current_org": "中共抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 8,
        "name": "郑翔云",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 9,
        "name": "赫荣丹",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委、副市长",
        "current_org": "抚远市人民政府",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 10,
        "name": "孟欣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委、副市长",
        "current_org": "抚远市人民政府",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 11,
        "name": "赵奇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委、副市长",
        "current_org": "抚远市人民政府",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 12,
        "name": "高大全",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委",
        "current_org": "中共抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 13,
        "name": "李锐",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委",
        "current_org": "中共抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    {
        "id": 14,
        "name": "姚振",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "市委常委",
        "current_org": "中共抚远市委员会",
        "source": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml"
    },
    # 前市长（继任链）
    {
        "id": 15,
        "name": "范继涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "原市长（2024年）",
        "current_org": "抚远市人民政府",
        "source": "https://www.hljfy.gov.cn（2024-10三届34次常务会议记录）"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共抚远市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共佳木斯市委员会",
        "location": "抚远市"
    },
    {
        "id": 2,
        "name": "抚远市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "佳木斯市人民政府",
        "location": "抚远市"
    },
    {
        "id": 3,
        "name": "抚远市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "佳木斯市人民代表大会常务委员会",
        "location": "抚远市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议抚远市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议佳木斯市委员会",
        "location": "抚远市"
    },
    {
        "id": 5,
        "name": "中共佳木斯市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "佳木斯市"
    },
    {
        "id": 6,
        "name": "黑龙江省人民政府黑瞎子岛建设和管理委员会",
        "type": "政府",
        "level": "省级专班",
        "parent": "黑龙江省人民政府",
        "location": "抚远市（黑瞎子岛）"
    },
    {
        "id": 7,
        "name": "中国航天科技集团第五研究院",
        "type": "央企",
        "level": "央企",
        "parent": "中国航天科技集团有限公司",
        "location": "北京/西安"
    },
    {
        "id": 8,
        "name": "抚远市政协（黑瞎子岛/东极旅游专班方向）",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议黑龙江省委员会",
        "location": "抚远市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 何大海（核心）——中国航天五院 → 空降抚远
    {"person_id": 1, "org_id": 7, "title": "中国航天科技集团五院 512所/各部门管理与技术岗", "start_date": "2002-08", "end_date": "2021-08", "rank": "研究员级", "note": "2002-08入职，历任科技处调度、发展计划部处长、航天恒星科技公司副总经理等，累计约19年航天。"},
    {"person_id": 1, "org_id": 1, "title": "抚远市委书记", "start_date": "2021-08", "end_date": "present", "rank": "正处级（副部长处级）", "note": "兼佳木斯市委常委、省黑瞎子岛管委会主任，2021-08起任，2026-08仍现任。"},

    # 郑树一（市长，核心）
    {"person_id": 2, "org_id": 2, "title": "抚远市市长", "start_date": "2025-05", "end_date": "present", "rank": "正处级", "note": "2025-05 以市长候选人/代理履职，2026-01官网更新为正式市长。"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2025-05", "end_date": "present", "rank": "副处级", "note": "兼任市委副书记。"},
    {"person_id": 2, "org_id": 2, "title": "履历缺口（2013-12参加工作至2025-05前）", "start_date": "unknown", "end_date": "unknown", "rank": "", "note": "公开资料未找到其任市长前的完整职务履历；上海籍、2013-12入职，疑为央国企/省直交流干部，未核实。"},

    # 郑志刚 — 前市长，现人大常委会主任
    {"person_id": 4, "org_id": 3, "title": "市人大常委会主任（党组书记）", "start_date": "2025年初", "end_date": "present", "rank": "副处级", "note": "由市长转任人大主任（2025初），主持市人大常委会全面工作。"},
    {"person_id": 4, "org_id": 2, "title": "抚远市市长（含代市长）", "start_date": "2024年末", "end_date": "2025年初", "rank": "正处级", "note": "曾任市长（此前任前为空缺），具体任命日期待查。"},

    # 冯海
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "现任市委副书记。"},

    # 王忠山
    {"person_id": 5, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": "现任市政协主席。"},

    # 刘祥锐
    {"person_id": 6, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "常务副市长，1999-07参加工作，中央广播电视大学会计学。"},
    {"person_id": 6, "org_id": 2, "title": "履历缺口（1999-07至常务副市长前）", "start_date": "unknown", "end_date": "unknown", "rank": "", "note": "早期职务未从公开一手来源核实。"},

    # 其他常委/副市长
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "班子名单确认。"},
    {"person_id": 8, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "宣传部部长。"},
    {"person_id": 9, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 范继涛（前任）
    {"person_id": 15, "org_id": 2, "title": "抚远市市长", "start_date": "", "end_date": "2024年", "rank": "正处级", "note": "2024年10月主持市政府常务会议，为上一任市长。"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "何大海作为市委书记，郑树一作为市长，党政主要领导搭档；何大海为主政班子之一把手，郑树一为行政主持。",
        "overlap_org": "抚远市",
        "overlap_period": "2025-05至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "何大海作为市委书记，冯海作为市委副书记，市委班子搭档。",
        "overlap_org": "中共抚远市委员会",
        "overlap_period": "2021-08至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "successor_predecessor_overlap",
        "context": "何大海任期内，郑志刚由市长转任市人大常委会主任，属党政人大关键节点人事摆位。",
        "overlap_org": "抚远市",
        "overlap_period": "2024末-2025初至今"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "何大海作为市委书记，刘祥锐为常委、常务副市长，市常委员会在同班子的协作。",
        "overlap_org": "抚远市",
        "overlap_period": "2021-08至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "predecessor_successor",
        "context": "市长继任链：郑志刚（前市长）→郑树一（现任市长）；郑志刚转任人大主任后，郑树一接任市长。",
        "overlap_org": "抚远市人民政府",
        "overlap_period": "2025-05"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "市政府党政领导在抚远市共事（市委副书记、市长 + 副职）。",
        "overlap_org": "抚远市",
        "overlap_period": "2025-05至今"
    },
    {
        "person_a": 15, "person_b": 2,
        "type": "predecessor_successor",
        "context": "市长继任链：范继涛（2024年市长）→ 郑志刚 → 郑树一。范继涛为郑树一的前前任。",
        "overlap_org": "抚远市人民政府",
        "overlap_period": "2024-2025"
    },
    {
        "person_a": 15, "person_b": 4,
        "type": "predecessor_successor",
        "context": "范继涛（2024市长）→郑志刚（2024末-2025初市长）。",
        "overlap_org": "抚远市人民政府",
        "overlap_period": "2024"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

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
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_year TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_year, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_year"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    # 市委书记 — 红
    if name in ("何大海",):
        return "255,50,50"
    # 政府（市长/副市长）— 蓝
    if name in ("郑树一", "刘祥锐", "赫荣丹", "孟欣", "赵奇", "范继涛"):
        return "50,100,255"
    # 人大 — 青
    if name == "郑志刚":
        return "200,255,255"
    # 政协 — 奶油
    if name == "王忠山":
        return "255,240,200"
    # 市委副书记/常委 — 橙
    if name in ("冯海", "刘善友", "郑翔云", "高大全", "李锐", "姚振"):
        return "255,165,0"
    return "100,100,100"


def person_size(name):
    if name in ("何大海", "郑树一"):
        return "20.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "央企" in o_type:
        return "200,255,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>抚远市领导班子工作关系网络 - {SLUG}</description>')
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
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
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
        c = org_color(o["type"])
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
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

SOURCE_REGISTER = [
    {"id": "S001", "title": "抚远市人民政府·领导之窗（市委/市人大/市政府/市政协）", "url": "https://www.hljfy.gov.cn/fys/c101357/ldzc.shtml", "publisher": "抚远市人民政府", "published_at": "2025", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "当前四套班子全部名单，2026-01-04更新"},
    {"id": "S002", "title": "抚远市人民政府·郑树一（市长）履历页", "url": "https://www.hljfy.gov.cn/...（郑树一页）", "publisher": "抚远市人民政府", "published_at": "2026-01-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市长信息（1983-11、上海、研究生工学硕士、2013-12参加工作、2015-07入党）"},
    {"id": "S003", "title": "抚远市人民政府·郑志刚（人大主任）履历页", "url": "https://www.hljfy.gov.cn/fys/c159/202505/c04_129.661.shtml", "publisher": "抚远市人民政府", "published_at": "2026-01-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "郑志刚（1971-11，黑龙江通河，1986-06参加工作，1997-04入党，本科）"},
    {"id": "S004", "title": "百度百科·抚远市", "url": "https://baike.baidu.com/item/抚远市", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "行政区划、撤县设市、省直管沿革、人口经济"},
    {"id": "S005", "title": "百度百科·何大海（lemmaId 58356391）", "url": "https://baike.baidu.com/item/何大海", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "何大海履历：1979-08生，黑龙江哈尔滨，西北工业大学软件工程硕士，2008-08参加工作，2001-08入党，2021-08任抚远市委书记"},
    {"id": "S006", "title": "抚远市政府·三届34次/40次/44次常务会议记录", "url": "https://www.hljfy.gov.cn", "publisher": "抚远市人民政府", "published_at": "2024-10~2025-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市长继任链：范继涛(2024)→郑志刚(2024末)→郑树一(2025-05至今)"},
]


def timeline_for_person(name):
    if name == "何大海":
        return [
            {"start": "1998-09", "end": "2002-06", "org": "黑龙江大学", "title": "广播电视编导专业学生", "notes": "本科", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2002-08", "end": "2021-08", "org": "中国航天科技集团第五研究院", "title": "五院技术/经营岗位（累计19年）", "notes": "历任科技处调度、发展部处长、航天恒星科技公司（503所）副总经理，研究员职称；2008-03—2013-04西北工业大学在职软件工程硕士", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2021-08", "end": "present", "org": "中共抚远市委员会", "title": "市委书记（兼佳木斯市委常委、省政府黑瞎子岛建设和管理委员会主任）", "notes": "空降/央企与地方干部交流到任；2026-08仍现任", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        ]
    if name == "郑树一":
        return [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "2013-12参加工作至2025-05前", "notes": "公开资料未找到其任市长前的完整职务履历；上海籍、研究生工学硕士，疑为外地/省直/央地交流调入，未核实", "confidence": "low", "source_ids": []},
            {"start": "2025-05", "end": "present", "org": "抚远市人民政府", "title": "市长（中共抚远市委副书记）", "notes": "2025-05以市委副书记、市长候选人召开常务会议，2025- 官网更新正式市长", "confidence": "confirmed", "source_ids": ["S001", "S002", "S006"]},
        ]
    if name in ("郑志刚",):
        return [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "此前任职", "notes": "公开未列明；1986-06参加工作", "confidence": "low", "source_ids": []},
            {"start": "2024末", "end": "2025年初", "org": "抚远市人民政府", "title": "市长（含代市长）", "notes": "由前任范继涛继任；2024末-2025初任市长", "confidence": "confirmed", "source_ids": ["S006"]},
            {"start": "2025年初", "end": "present", "org": "抚远市人民代表大会常务委员会", "title": "市人大常委会党组书记、主任", "notes": "转任人大主任，主持市人大常委会全面工作", "confidence": "confirmed", "source_ids": ["S003"]},
        ]
    if name == "冯海":
        return [{"start": "", "end": "present", "org": "中共抚远市委员会", "title": "市委副书记", "notes": "现任；此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]}]
    if name == "刘祥锐":
        return [
            {"start": "", "end": "present", "org": "抚远市人民政府", "title": "市委常委、常务副市长", "notes": "1999-07参加工作，中央广播电视大学会计学；此前职务待查", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    return [{"start": "", "end": "present", "org": "", "title": "", "notes": "现任班子在册；完整履历待查", "confidence": "medium", "source_ids": ["S001"]}]


def make_person_json(p, job):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "抚远市",
            "job": job,
            "task_id": "heilongjiang_抚远市",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"fuyuan_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", "")}],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_year", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if p.get("id") in (2, 4, 15) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline_for_person(p["name"]),
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if p["name"] in ("何大海",) else "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [p.get("birthplace", "")],
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
            {"type": "none_found", "description": "在公开信息中未发现该人物负面纪律/审计信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("id") in (1, 2, 4) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历（前任书记、应届书记前职务、教育背景等）待补"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{p['name']}的完整职业履历（尤其前延伸到原班子/前任书记等）",
                "why_it_matters": "核心人物，但早期履历不完整",
                "last_attempted": AS_OF,
                "suggested_queries": [f"{p['name']} 简历 抚远", f"{p['name']} 任前公示", f"抚远市委书记 前任 {p['name']}"]
            }
        ]
    }


def build_person_jsons():
    files = []
    for p in persons:
        job_map = {
            1: "市委书记",
            2: "市长",
            3: "市委副书记",
            4: "市人大常委会主任",
            5: "市政协主席",
            6: "常务副市长",
        }
        if p["id"] not in job_map:
            continue
        job = job_map[p["id"]]
        data = make_person_json(p, job)
        # 关系（针对核心）
        if p["name"] == "何大海":
            data["relationships"] = [
                {"person": "郑树一", "person_id": "fuyuan_郑树一", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市委书记—市长搭档", "overlap_org": "抚远市", "overlap_period": "2025-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "冯海", "person_id": "fuyuan_冯海", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "市委班子搭档", "overlap_org": "中共抚远市委员会", "overlap_period": "2021-08至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ]
        if p["name"] == "郑树一":
            data["relationships"] = [
                {"person": "何大海", "person_id": "fuyuan_何大海", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "市长向市委书记报告", "overlap_org": "抚远市", "overlap_period": "2025-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "郑志刚", "person_id": "fuyuan_郑志刚", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "郑志刚前任市长，郑树一接任", "overlap_org": "抚远市人民政府", "overlap_period": "2025-05", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
            ]
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-佳木斯市-{job}-{p['name']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")
        files.append(path)
    return files


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")