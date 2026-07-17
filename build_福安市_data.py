#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 福安市 (Fu'an City, Ningde, Fujian).

Task: fujian_福安市 — 市委书记 & 市长
Province: 福建省
City: 宁德市
Region: 福安市
Level: 县级市
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17):
- 市委书记: 黄其山 (born 1971.10, male, Han, Fujian Ningde, university + management bachelor)
- 市长: 许春林 (前周宁县领导, 2025.12.31任代市长, 2026.01.02当选)
- 市人大常委会主任: 詹廷平
- 市政协主席: 林志生

市委常委会 confirmed members (from fjfa.gov.cn official articles):
黄其山(书记), 许春林(副书记/市长), 缪碧华(常委/副市长),
连俊成(常委), 钟乐光(常委), 李章通(常委), 连坚(常委), 张为明(常委)

市政府领导班子 (partial):
许春林(市长), 缪碧华(常务副市长), 李章通(副市长), 连坚(副市长), 张为明(副市长)

Sources:
- zh.wikipedia.org 福安市、福安历任行政长官列表
- baidu.com 搜索结果 (黄其山简历、福安市政府领导)
- fjfa.gov.cn 福安市人民政府官方网站 (2026年领导活动新闻)
- news.qq.com 新闻报道
- 163.com 网易新闻

Confidence: Current leadership confirmed from Wikipedia and Baidu search results.
Career details partial — full career histories are not fully available.
Marked gaps explicitly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOV_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "data" else SCRIPT_DIR
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "fujian_福安市")
DB_PATH = os.path.join(STAGING, "福安市_network.db")
GEXF_PATH = os.path.join(STAGING, "福安市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 市委书记 — 黄其山
    {
        "id": "fuan_huang_qishan",
        "name": "黄其山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "福建宁德",
        "native_place": "福建宁德",
        "education": "大学学历、管理学学士（省委党校大学学历）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委书记",
        "current_org": "中共福安市委员会",
        "source": "zh.wikipedia.org, baidu.com (黄其山简历), news.qq.com",
        "notes": "2025年12月由市长升任市委书记。2026年2月兼任市人武部党委第一书记。"
             "曾任古田县委副书记、县长，宁德市委宣传部副部长、市委网信办主任，"
             "蕉城区飞鸾镇镇长、洪口乡党委书记、霍童镇党委书记等职。"
             "福建省第十四届人大代表。",
        "confidence": "confirmed",
    },

    # 市长 — 许春林
    {
        "id": "fuan_xu_chunlin",
        "name": "许春林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "福建周宁",
        "native_place": "福建周宁",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委副书记、市长",
        "current_org": "福安市人民政府",
        "source": "zh.wikipedia.org (福安历任行政长官列表), news.qq.com, fjfa.gov.cn",
        "notes": "2025年12月31日任福安市副市长、代市长，2026年1月2日当选市长。"
             "此前曾任周宁县领导职务。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 市人大常委会主任 — 詹廷平
    {
        "id": "fuan_zhan_tingping",
        "name": "詹廷平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市人大常委会主任",
        "current_org": "福安市人大常委会",
        "source": "fjfa.gov.cn (市委2026年工作会议 2026-03-01)",
        "notes": "2026年2月25日市委工作会议列名市人大常委会主任。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 市政协主席 — 林志生
    {
        "id": "fuan_lin_zhisheng",
        "name": "林志生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市政协主席",
        "current_org": "福安市政协",
        "source": "fjfa.gov.cn (市委2026年工作会议 2026-03-01)",
        "notes": "2026年2月25日市委工作会议列名市政协主席。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 市委常委、副市长 — 缪碧华
    {
        "id": "fuan_miao_bihua",
        "name": "缪碧华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委常委、副市长",
        "current_org": "福安市人民政府",
        "source": "fjfa.gov.cn (许春林检查台风防范 2026-07-10)",
        "notes": "2026年7月10日陪同市长许春林检查台风防范工作。具体分管领域待确认。",
        "confidence": "confirmed",
    },

    # 市委常委 — 连俊成
    {
        "id": "fuan_lian_juncheng",
        "name": "连俊成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委常委",
        "current_org": "中共福安市委员会",
        "source": "fjfa.gov.cn (许春林检查台风防范 2026-07-10)",
        "notes": "2026年7月10日陪同市长许春林检查台风防范工作。具体职务分工待确认。",
        "confidence": "confirmed",
    },

    # 市委常委 — 钟乐光
    {
        "id": "fuan_zhong_leguang",
        "name": "钟乐光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委常委",
        "current_org": "中共福安市委员会",
        "source": "fjfa.gov.cn (许春林检查台风防范 2026-07-10)",
        "notes": "2026年7月10日陪同市长许春林检查台风防范工作。具体职务分工待确认。",
        "confidence": "confirmed",
    },

    # 市委常委 — 李章通
    {
        "id": "fuan_li_zhangtong",
        "name": "李章通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委常委",
        "current_org": "中共福安市委员会",
        "source": "fjfa.gov.cn (国资国企工作会议 2026-05-22)",
        "notes": "完整履历及具体分工待补充。",
        "confidence": "confirmed",
    },

    # 市委常委、副市长 — 连坚
    {
        "id": "fuan_lian_jian",
        "name": "连坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委常委、副市长",
        "current_org": "福安市人民政府",
        "source": "fjfa.gov.cn (国资国企工作会议 2026-05-22)",
        "notes": "2026年5月22日国资国企工作会议列名市委常委。具体分管领域待确认。",
        "confidence": "confirmed",
    },

    # 市委常委 — 张为明
    {
        "id": "fuan_zhang_weiming",
        "name": "张为明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福安市委常委",
        "current_org": "中共福安市委员会",
        "source": "fjfa.gov.cn (黄其山检查台风防范 2026-07-11)",
        "notes": "2026年7月11日陪同市委书记黄其山检查台风防范工作。具体职务分工待确认。",
        "confidence": "confirmed",
    },

    # ══════════════ 前任领导 ══════════════

    # 周祥祺 — 前任市委书记 (2021-2025)
    {
        "id": "fuan_zhou_xiangqi",
        "name": "周祥祺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任福安市委书记",
        "current_org": "",
        "source": "zh.wikipedia.org, 福州新闻网 (2021年5月15日)",
        "notes": "2021年5月任福安市委书记至2025年12月。此前曾任宁德市委组织部副部长、市人社局局长等职。"
             "2025年12月卸任后新职待确认。",
        "confidence": "confirmed",
    },

    # 叶其发 — 前前任市委书记
    {
        "id": "fuan_ye_qifa",
        "name": "叶其发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年4月",
        "birthplace": "福建寿宁",
        "native_place": "福建寿宁",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任福安市委书记",
        "current_org": "",
        "source": "人民网, zh.wikipedia.org",
        "notes": "2018年9月至2021年1月任福安市委书记。此前曾任福安市长、周宁县长、屏南县委副书记/政法委书记。"
             "后任宁德市副市长、宁德市委常委/宣传部部长。",
        "confidence": "confirmed",
    },

    # 钟宜国 — 前任市长
    {
        "id": "fuan_zhong_yiguo",
        "name": "钟宜国",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "",
        "birthplace": "福建宁德",
        "native_place": "福建宁德",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任福安市长",
        "current_org": "",
        "source": "zh.wikipedia.org",
        "notes": "2018年9月至2021年6月任福安代市长/市长。畲族。后去向待确认。",
        "confidence": "confirmed",
    },
]


organizations = [
    {"id": "cpc_fuan",       "name": "中共福安市委员会", "type": "党委", "level": "县级市", "parent": "中共宁德市委员会", "location": "福建省宁德市福安市"},
    {"id": "gov_fuan",       "name": "福安市人民政府", "type": "政府", "level": "县级市", "parent": "宁德市人民政府", "location": "福建省宁德市福安市"},
    {"id": "npc_fuan",       "name": "福安市人大常委会", "type": "人大", "level": "县级市", "parent": "", "location": "福建省宁德市福安市"},
    {"id": "cppcc_fuan",     "name": "福安市政协", "type": "政协", "level": "县级市", "parent": "", "location": "福建省宁德市福安市"},
    {"id": "polit_fuan",     "name": "中共福安市委政法委员会", "type": "党委", "level": "县级市", "parent": "中共福安市委员会", "location": "福建省宁德市福安市"},
    {"id": "psb_fuan",       "name": "福安市公安局", "type": "政府", "level": "县级市", "parent": "福安市人民政府", "location": "福建省宁德市福安市"},
    {"id": "cpc_ningde",     "name": "中共宁德市委员会", "type": "党委", "level": "地级市", "parent": "中共福建省委员会", "location": "福建省宁德市"},
    {"id": "gov_ningde",     "name": "宁德市人民政府", "type": "政府", "level": "地级市", "parent": "福建省人民政府", "location": "福建省宁德市"},
]


positions = [
    # 黄其山 — 现任市委书记
    {"person_id": "fuan_huang_qishan", "org_id": "cpc_fuan", "title": "福安市委书记", "start": "2025-12", "end": "present", "rank": "正处级", "note": "市人武部党委第一书记"},
    {"person_id": "fuan_huang_qishan", "org_id": "gov_fuan", "title": "福安市市长（前任）", "start": "2021-06", "end": "2025-12", "rank": "正处级", "note": "2021年6月任代市长，2021年12月转正"},
    # 许春林 — 现任市长
    {"person_id": "fuan_xu_chunlin", "org_id": "cpc_fuan", "title": "福安市委副书记", "start": "2025-12", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "fuan_xu_chunlin", "org_id": "gov_fuan", "title": "福安市市长", "start": "2025-12", "end": "present", "rank": "正处级", "note": "2025.12.31任代市长，2026.01.02当选市长"},
    # 詹廷平 — 人大主任
    {"person_id": "fuan_zhan_tingping", "org_id": "npc_fuan", "title": "福安市人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 林志生 — 政协主席
    {"person_id": "fuan_lin_zhisheng", "org_id": "cppcc_fuan", "title": "福安市政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 缪碧华 — 市委常委、副市长
    {"person_id": "fuan_miao_bihua", "org_id": "cpc_fuan", "title": "福安市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "fuan_miao_bihua", "org_id": "gov_fuan", "title": "福安市副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 连俊成 — 市委常委
    {"person_id": "fuan_lian_juncheng", "org_id": "cpc_fuan", "title": "福安市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务分工待确认"},
    # 钟乐光 — 市委常委
    {"person_id": "fuan_zhong_leguang", "org_id": "cpc_fuan", "title": "福安市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务分工待确认"},
    # 李章通 — 市委常委
    {"person_id": "fuan_li_zhangtong", "org_id": "cpc_fuan", "title": "福安市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务分工待确认"},
    # 连坚 — 市委常委、副市长
    {"person_id": "fuan_lian_jian", "org_id": "cpc_fuan", "title": "福安市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "fuan_lian_jian", "org_id": "gov_fuan", "title": "福安市副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张为明 — 市委常委
    {"person_id": "fuan_zhang_weiming", "org_id": "cpc_fuan", "title": "福安市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务分工待确认"},
    # 周祥祺 — 前任市委书记
    {"person_id": "fuan_zhou_xiangqi", "org_id": "cpc_fuan", "title": "福安市委书记（前任）", "start": "2021-05", "end": "2025-12", "rank": "正处级", "note": ""},
    # 叶其发 — 前前任市委书记
    {"person_id": "fuan_ye_qifa", "org_id": "cpc_fuan", "title": "福安市委书记（前前任）", "start": "2018-09", "end": "2021-01", "rank": "正处级", "note": ""},
    {"person_id": "fuan_ye_qifa", "org_id": "gov_fuan", "title": "福安市市长（前任）", "start": "2016-06", "end": "2018-09", "rank": "正处级", "note": "2016年任代市长，后转正"},
    # 钟宜国 — 前任市长
    {"person_id": "fuan_zhong_yiguo", "org_id": "gov_fuan", "title": "福安市市长（前任）", "start": "2018-09", "end": "2021-06", "rank": "正处级", "note": "畲族"},
]


# ── Relationship edges ──────────────────────────────────────────────────

relationships = [
    # 黄其山 ↔ 许春林 (书记↔市长，党政一把手搭档)
    {"person_a": "fuan_huang_qishan", "person_b": "fuan_xu_chunlin",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，黄其山主持市委全面工作，许春林主持市政府全面工作",
     "overlap_org": "中共福安市委员会/福安市人民政府",
     "overlap_period": "2025年12月起", "confidence": "confirmed"},

    # 黄其山 ↔ 缪碧华 (书记↔常委副市长)
    {"person_a": "fuan_huang_qishan", "person_b": "fuan_miao_bihua",
     "type": "superior_subordinate", "strength": "strong",
     "context": "缪碧华在市委常委会内受书记领导",
     "overlap_org": "中共福安市委员会/福安市人民政府",
     "overlap_period": "", "confidence": "confirmed"},

    # 许春林 ↔ 缪碧华 (市长↔副市长)
    {"person_a": "fuan_xu_chunlin", "person_b": "fuan_miao_bihua",
     "type": "superior_subordinate", "strength": "strong",
     "context": "缪碧华陪同许春林检查台风防范工作",
     "overlap_org": "福安市人民政府",
     "overlap_period": "2025年12月起", "confidence": "confirmed"},

    # 黄其山 ↔ 周祥祺 (现任书记↔前任书记，predecessor_successor)
    {"person_a": "fuan_zhou_xiangqi", "person_b": "fuan_huang_qishan",
     "type": "predecessor_successor", "strength": "strong",
     "context": "周祥祺2021-2025任市委书记，黄其山2025年12月接任",
     "overlap_org": "中共福安市委员会",
     "overlap_period": "2025（交接）", "confidence": "confirmed"},

    # 周祥祺 ↔ 叶其发 (前任书记↔前前任书记)
    {"person_a": "fuan_ye_qifa", "person_b": "fuan_zhou_xiangqi",
     "type": "predecessor_successor", "strength": "strong",
     "context": "叶其发2018-2021任市委书记，周祥祺2021年5月接任",
     "overlap_org": "中共福安市委员会",
     "overlap_period": "2021（交接）", "confidence": "confirmed"},

    # 黄其山 ↔ 钟宜国 (前市长→市长→书记的承接)
    {"person_a": "fuan_zhong_yiguo", "person_b": "fuan_huang_qishan",
     "type": "predecessor_successor", "strength": "strong",
     "context": "钟宜国2018-2021任市长，黄其山2021年6月接任市长",
     "overlap_org": "福安市人民政府",
     "overlap_period": "2021（交接）", "confidence": "confirmed"},

    # 许春林 ↔ 黄其山 (市长↔前市长)
    {"person_a": "fuan_huang_qishan", "person_b": "fuan_xu_chunlin",
     "type": "predecessor_successor", "strength": "strong",
     "context": "黄其山此前任市长，许春林2025年12月接任市长",
     "overlap_org": "福安市人民政府",
     "overlap_period": "2025（交接）", "confidence": "confirmed"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p.get("birthplace", ""), p.get("native_place", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    current = p.get("current_post", "")
    if "市委书记" in current:
        return "255,50,50"
    if "市长" in current or "副市长" in current or "常委" in current:
        return "50,100,255"
    if "人大" in current:
        return "200,255,255"
    if "政协" in current:
        return "255,240,200"
    return "100,100,100"


def is_top_leader(p):
    current = p.get("current_post", "")
    return "市委书记" in current or "市长" in current


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
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>福安市领导班子工作关系网络 — 中共福安市委员会、福安市人民政府</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        is_pred = p["id"] in ("fuan_zhou_xiangqi", "fuan_ye_qifa", "fuan_zhong_yiguo")
        is_org_leader = p["id"] in ("fuan_zhan_tingping", "fuan_lin_zhisheng")
        if is_pred:
            sz = "8.0"
        elif is_org_leader:
            sz = "12.0"
        else:
            sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        co = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{co.split(",")[0]}" g="{co.split(",")[1]}" b="{co.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for rel in relationships:
        w = "2.0" if rel.get("strength") == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(rel["person_a"])}" target="{esc(rel["person_b"])}" label="{esc(rel["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("strength",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
