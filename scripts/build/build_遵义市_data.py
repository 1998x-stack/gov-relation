#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 遵义市 leadership network (地级市).

Targets: 市委书记 (李睿) & 市长 (宋旭升)
Data as of: 2026-08-05
Sources:
- 中国经济网 district.ce.cn 地方党政领导人物库 (贵州各地市州书记市长名单, 2026-07-20)
- 中国经济网《宋旭升当选遵义市市长》(2026-04-28)
- 中国经济网《贵州省委常委李睿任省纪委书记、省监委代理主任》(2026-07-14)
- 遵义市人民政府门户 www.zunyi.gov.cn — 机关简介·市政府领导 (2026-08)
- 遵义新闻网 / 遵义日报 (遵义要闻 2026-07/08)
"""

import os
import sqlite3
from datetime import datetime

# Staging directory
TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(TMP_DIR, "..", "..", "..")
DB_PATH = os.path.join(TMP_DIR, "遵义市_network.db")
GEXF_PATH = os.path.join(TMP_DIR, "遵义市_network.gexf")
PERSONS_DIR = os.path.join(TMP_DIR, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────

persons = [
    # === Current Top Leaders ===
    {
        "id": 1, "name": "李睿", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年10月", "birthplace": "山西汾阳", "education": "长安大学，在职研究生，工学博士",
        "party_join": "1987年6月", "work_start": "1991年7月",
        "current_post": "遵义市委书记（贵州省委常委、省纪委书记、省监委代理主任兼）",
        "current_org": "中共遵义市委员会",
        "source": "http://district.ce.cn/newarea/sddy/202607/t20260714_3085708.shtml",
    },
    {
        "id": 2, "name": "宋旭升", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年10月", "birthplace": "山东泰安", "education": "清华大学，研究生学历，管理学硕士",
        "party_join": "1996年7月", "work_start": "2002年8月",
        "current_post": "遵义市委副书记、市人民政府市长、市政府党组书记",
        "current_org": "遵义市人民政府",
        "source": "http://district.ce.cn/newarea/sddy/202604/t20260428_2935692.shtml",
    },
    # === Other leadership team members ===
    {
        "id": 3, "name": "梁铮", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市委副书记", "current_org": "中共遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260731_90680254.html",
    },
    {
        "id": 4, "name": "何薇", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人大常委会主任", "current_org": "遵义市人大常委会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260731_90280254.html",
    },
    {
        "id": 5, "name": "汪海波", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市政协主席", "current_org": "政协遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260731_90280254.html",
    },
    {
        "id": 6, "name": "郭晓武", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市委常委、遵义军分区政委", "current_org": "中共遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260731_90280254.html",
    },
    {
        "id": 7, "name": "许文辉", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市委常委、市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 8, "name": "李明", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 9, "name": "程涛", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 10, "name": "骆亚", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 11, "name": "冉拥军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 12, "name": "陈致豫", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 13, "name": "冉崇庆", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 14, "name": "王埝", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府副市长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 15, "name": "宋祖禹", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市人民政府秘书长", "current_org": "遵义市人民政府",
        "source": "https://www.zunyi.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/",
    },
    {
        "id": 21, "name": "魏树旺（前任遵义市委书记）", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年12月", "birthplace": "河北清苑", "education": "北京师范大学哲学系",
        "party_join": "", "work_start": "",
        "current_post": "（前任遵义市委书记）",
        "current_org": "中共遵义市委员会",
        "source": "媒体：政事儿/贵州日报（2022-06-02 另有任用）",
    },
    # === Additional 市领导 (参会, 职务待确认) ===
    {
        "id": 16, "name": "邓航", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市领导", "current_org": "中共遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260729_90671084.html",
    },
    {
        "id": 17, "name": "徐永琳", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市领导", "current_org": "中共遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260729_90671084.html",
    },
    {
        "id": 18, "name": "缪凡", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市领导", "current_org": "中共遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202608/t20260803_90686389.html",
    },
    {
        "id": 19, "name": "王继松", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市领导", "current_org": "中共遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260729_90671084.html",
    },
    {
        "id": 20, "name": "吴起", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义市领导", "current_org": "中共遵义市委员会",
        "source": "https://www.zunyi.gov.cn/xwdt/zyyw/202607/t20260729_90671084.html",
    },
]

organizations = [
    {"id": 1, "name": "中共遵义市委员会", "type": "党委",
     "level": "地级市", "parent": "中共贵州省委员会", "location": "贵州省遵义市"},
    {"id": 2, "name": "遵义市人民政府", "type": "政府",
     "level": "地级市", "parent": "贵州省人民政府", "location": "贵州省遵义市"},
    {"id": 3, "name": "遵义市人大常委会", "type": "人大",
     "level": "地级市", "parent": "贵州省人大常委会", "location": "贵州省遵义市"},
    {"id": 4, "name": "政协遵义市委员会", "type": "政协",
     "level": "地级市", "parent": "政协贵州省委员会", "location": "贵州省遵义市"},
    {"id": 5, "name": "中共贵州省委员会", "type": "党委",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 6, "name": "贵州省人民政府", "type": "政府",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 7, "name": "贵州省纪委监委", "type": "党委",
     "level": "省级", "parent": "中共贵州省委员会", "location": "贵州省贵阳市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "遵义市委书记", "start": "2022", "end": "present", "rank": "副省级（省委常委高配）", "note": "2022年任贵州省委常委、遵义市委书记"},
    {"person_id": 1, "org_id": 5, "title": "贵州省委常委", "start": "2022", "end": "present", "rank": "副省级", "note": "2022年任省委常委"},
    {"person_id": 1, "org_id": 7, "title": "贵州省纪委书记、省监委代理主任", "start": "2026-07", "end": "present", "rank": "副省级", "note": "2026-07-13/14任"},
    {"person_id": 2, "org_id": 2, "title": "遵义市人民政府市长", "start": "2026-04", "end": "present", "rank": "正厅级", "note": "2026-04-28遵义市六届人大七次会议选举"},
    {"person_id": 2, "org_id": 2, "title": "遵义市人民政府党组书记", "start": "", "end": "present", "rank": "正厅级", "note": "市政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "遵义市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "遵义市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "遵义市人大常委会主任", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "遵义市政协主席", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "遵义市委常委、军分区政委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "遵义市人民政府副市长（市委常委）", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "遵义市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "遵义市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "遵义市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "遵义市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "遵义市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "遵义市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "遵义市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "遵义市人民政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "遵义市领导", "start": "", "end": "present", "rank": "", "note": "参加市政府党组会/集中整治会等"},
    {"person_id": 17, "org_id": 1, "title": "遵义市领导", "start": "", "end": "present", "rank": "", "note": "参加市集中整治小组会议"},
    {"person_id": 18, "org_id": 1, "title": "遵义市领导", "start": "", "end": "present", "rank": "", "note": "参加市住建领域集中整治专题会议"},
    {"person_id": 19, "org_id": 1, "title": "遵义市领导", "start": "", "end": "present", "rank": "", "note": "参加市集中整治小组会议"},
    {"person_id": 20, "org_id": 1, "title": "遵义市领导", "start": "", "end": "present", "rank": "", "note": "参加市集中整治小组会议"},
    {"person_id": 21, "org_id": 1, "title": "遵义市委书记（前任）", "start": "unknown", "end": "2022-06-02", "rank": "正厅级", "note": "2022-06-02由李睿接任；离任时另有任用"},
]

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政一把手搭档",
        "context": "李睿为遵义市委书记，宋旭升为遵义市委副书记、市长、市政府党组书记，两人为党政一把手搭档关系",
        "overlap_org": "中共遵义市委员会 / 遵义市人民政府",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "上下级",
        "context": "李睿任遵义市委书记，梁铮为遵义市委副书记，上下级共事关系",
        "overlap_org": "中共遵义市委员会",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "共事",
        "context": "宋旭升（市长）与梁铮（市委副书记）同为市委委员，共同出席半年经济工作会等",
        "overlap_org": "中共遵义市委员会",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "共事",
        "context": "宋旭升与何薇（市人大主任）、汪海波（市政协主席）等市四套班子共同出席半年经济工作会等",
        "overlap_org": "遵义市四套班子",
        "overlap_period": "2026",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "共事",
        "context": "宋旭升与市政协主席汪海波共同出席市领导走访慰问、半年经济工作会",
        "overlap_org": "遵义市四套班子",
        "overlap_period": "2026",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "领导下属",
        "context": "宋旭升市长与副市长/常委许文辉在市政府工作中为领导下属关系",
        "overlap_org": "遵义市人民政府",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 21,
        "type": "前任后任",
        "context": "2022-06-02李睿接替魏树旺任遵义市委书记，魏树旺另有任用调离",
        "overlap_org": "中共遵义市委员会",
        "overlap_period": "2022-06",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "领导下属",
        "context": "宋旭升市长与副市长骆亚共同出席市住建及集中整治会议",
        "overlap_org": "遵义市人民政府",
        "overlap_period": "2026-08",
        "strength": "strong",
        "confidence": "confirmed",
    },
]

# ═══════════════════════════════════════════════════════
#  Build SQLite DB
# ═══════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    strength TEXT, confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

cur.executemany(
    "INSERT OR REPLACE INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)",
    persons,
)
cur.executemany(
    "INSERT OR REPLACE INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)",
    organizations,
)
cur.executemany(
    "INSERT INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)",
    positions,
)
cur.executemany(
    "INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period,:strength,:confidence)",
    relationships,
)

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
ps = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc = cur.fetchone()[0]
conn.close()

print(f"Database: {DB_PATH}")
print(f"  Persons: {pc}, Organizations: {oc}, Positions: {ps}, Relationships: {rc}")

# ═══════════════════════════════════════════════════════
#  Build GEXF Graph
# ═══════════════════════════════════════════════════════


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    title = p.get("current_post", "")
    if "市委书记" in title:
        return "255,50,50"
    if "市长" in title and "副" not in title:
        return "50,100,255"
    if "纪委" in title:
        return "255,165,0"
    if "人大" in title:
        return "200,255,255"
    if "政协" in title:
        return "255,240,200"
    if "副市长" in title or "秘书长" in title:
        return "100,100,255"
    return "100,100,100"


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


def is_top_leader(p):
    title = p.get("current_post", "")
    return "市委书记" in title or ("市长" in title and "副" not in title)


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append("    <creator>Gov Relation Research Agent</creator>")
lines.append(f"    <description>遵义市领导班子关系网络 — 数据截至 {datetime.now().strftime('%Y-%m-%d')}</description>")
lines.append("  </meta>")
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="education" type="string"/>')
lines.append("    </attributes>")

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="confidence" type="string"/>')
lines.append("    </attributes>")

# Nodes
lines.append("    <nodes>")
for p in persons:
    pid = p["id"]
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p.get("education",""))}"/>')
    lines.append("        </attvalues>")
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append("      </node>")

for o in organizations:
    oid = o["id"]
    c = org_color(o)
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
    lines.append("        </attvalues>")
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append("      </node>")

lines.append("    </nodes>")

# Edges
lines.append("    <edges>")
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
    lines.append('          <attvalue for="2" value="confirmed"/>')
    lines.append("        </attvalues>")
    lines.append("      </edge>")

for r in relationships:
    eid += 1
    w = "2.0" if r.get("strength") == "strong" else "1.0"
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type",""))}" weight="{w}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence",""))}"/>')
    lines.append("        </attvalues>")
    lines.append("      </edge>")

lines.append("    </edges>")
lines.append("  </graph>")
lines.append("</gexf>")

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"GEXF: {GEXF_PATH}")
print(f"  Total edges: {eid}")

print("\nDone.")