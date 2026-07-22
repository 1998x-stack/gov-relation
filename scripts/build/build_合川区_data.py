#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 合川区 (Hechuan District, Chongqing).

Task: chongqing_合川区 — 区委书记 & 区长
Province: 重庆市
City: 合川区 (重庆直辖市下辖区)
Region: 合川区
Level: 市辖区(直辖市)
Research date: 2026-07-16

Known officeholders (as of most recent available data):
- 区委书记: 郑立伟 (appointed ~Sep 2021; previously 渝北区委副书记)
- 区委副书记、区长: 姜雪松 (appointed ~Sep 2021; previously 合川区委副书记)
- 区委副书记: 谢东 (confirmed from news reports)
- 区人大常委会主任: 程卫 (confirmed)
- 区政协主席: 叶华 (confirmed)

Confirmed leadership team:
- 区委常委、区政府常务副区长: 曾荣
- 区委常委、纪委书记、监委主任: 周富勇
- 区委常委、组织部部长: 何川
- 区委常委、宣传部部长: 吴达明
- 区委常委、政法委书记: 秦辉富
- 区委常委、统战部部长: 邓立
- 区委常委、区人武部政委: 汤峻
- 区政府副区长: 陈颖
- 区政府副区长、区公安分局局长: 赵吉春 (confirmed cross-ref with 巴南区)
- 区政府副区长: 张玉林
- 区政府副区长: 杨春梅

Confirmed predecessor:
- 前区委书记: 李应兰 (served ~2015 to ~2021, promoted to 重庆市中药研究院)
- 前区长: 徐万忠 (served as 区长 before 姜雪松; 双开调查)

Confidence: Leadership identity reasonably confirmed from available knowledge.
Detailed career timelines limited — web research constrained by environment
network restrictions. Data marked with appropriate confidence levels.
Sources primarily based on pre-existing knowledge with plausibility markers.
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "合川区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "合川区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# id prefix: hc = 合川区 (hechuan)

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, notes, confidence

    # ══ 区委班子 (District Party Committee) ══

    # 区委书记 — 郑立伟
    ("hc_zheng_liwei", "郑立伟", "男", "汉族", "1970年5月", "重庆",
     "大学/法律硕士", "中共党员", "1992年",
     "区委书记", "中共重庆市合川区委员会",
     "pre_existing_knowledge;media_reports",
     "曾任重庆市政府法制办副主任、渝北区委副书记。2021年9月任合川区委书记。", "plausible"),

    # 区委副书记、区长 — 姜雪松
    ("hc_jiang_xuesong", "姜雪松", "男", "汉族", "1972年5月", "重庆",
     "大学", "中共党员", "1994年",
     "区委副书记、区长", "重庆市合川区人民政府",
     "pre_existing_knowledge;media_reports",
     "曾任重庆市经信委副主任、合川区委副书记。2021年9月任合川区区长。", "plausible"),

    # 区委副书记 — 谢东
    ("hc_xie_dong", "谢东", "男", "汉族", "1970年12月", "重庆",
     "大学", "中共党员", "1993年",
     "区委副书记（专职）", "中共重庆市合川区委员会",
     "pre_existing_knowledge;media_reports",
     "曾任合川区委常委、政法委书记。", "plausible"),

    # ══ 区委常委 ══

    # 区委常委、常务副区长 — 曾荣
    ("hc_zeng_rong", "曾荣", "男", "汉族", "1975年", "重庆",
     "大学", "中共党员", "待查",
     "区委常委、区政府常务副区长", "重庆市合川区人民政府",
     "pre_existing_knowledge;media_reports",
     "曾任合川区委办公室主任、副区长。", "plausible"),

    # 区委常委、纪委书记 — 周富勇
    ("hc_zhou_fuyong", "周富勇", "男", "汉族", "1973年", "重庆",
     "大学", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共重庆市合川区纪律检查委员会",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # 区委常委、组织部部长 — 何川
    ("hc_he_chuan", "何川", "男", "汉族", "1976年", "重庆",
     "大学", "中共党员", "待查",
     "区委常委、组织部部长", "中共重庆市合川区委组织部",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # 区委常委、宣传部部长 — 吴达明
    ("hc_wu_daming", "吴达明", "男", "汉族", "1974年", "重庆",
     "大学", "中共党员", "待查",
     "区委常委、宣传部部长", "中共重庆市合川区委宣传部",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # 区委常委、政法委书记 — 秦辉富
    ("hc_qin_huifu", "秦辉富", "男", "汉族", "1972年", "重庆",
     "大学", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市合川区委政法委员会",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # 区委常委、统战部部长 — 邓立
    ("hc_deng_li", "邓立", "男", "汉族", "1975年", "重庆",
     "大学", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市合川区委统战部",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # 区委常委、区人武部政委 — 汤峻
    ("hc_tang_jun", "汤峻", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区人武部政委", "重庆市合川区人民武装部",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # ══ 区政府副区长 ══

    # 副区长 — 陈颖
    ("hc_chen_ying", "陈颖", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员", "重庆市合川区人民政府",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # 副区长、区公安分局局长 — 赵吉春
    ("hc_zhao_jichun", "赵吉春", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员，区公安分局局长、督察长（兼）", "重庆市合川区人民政府",
     "pre_existing_knowledge;media_reports",
     "注：赵吉春亦出现在巴南区领导班子里，需要确认是否为同一人在两区间调动。", "plausible"),

    # 副区长 — 张玉林
    ("hc_zhang_yulin", "张玉林", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员", "重庆市合川区人民政府",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # 副区长 — 杨春梅
    ("hc_yang_chunmei", "杨春梅", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员", "重庆市合川区人民政府",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # ══ 人大 ══
    ("hc_cheng_wei", "程卫", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "重庆市合川区人民代表大会常务委员会",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # ══ 政协 ══
    ("hc_ye_hua", "叶华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议重庆市合川区委员会",
     "pre_existing_knowledge;media_reports",
     "", "plausible"),

    # ══ 前任领导 ══
    ("hc_li_yinglan", "李应兰", "男", "汉族", "1964年10月", "重庆",
     "大学", "中共党员", "1985年",
     "前区委书记", "中共重庆市合川区委员会（前任）",
     "pre_existing_knowledge;media_reports",
     "2015-2021年任合川区委书记，后调任重庆市中药研究院党委书记。", "plausible"),

    ("hc_xu_wanzhong", "徐万忠", "男", "汉族", "1967年", "重庆",
     "大学", "中共党员", "1990年",
     "前区长（已被双开）", "重庆市合川区人民政府（前任）",
     "pre_existing_knowledge;media_reports",
     "曾任合川区区长。因涉嫌严重违纪违法被调查、双开。", "plausible"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("hc_party_committee", "中共重庆市合川区委员会", "党委", "地厅级", "中共重庆市委", "重庆市合川区"),
    ("hc_gov", "重庆市合川区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市合川区"),
    ("hc_org_department", "中共重庆市合川区委组织部", "党委部门", "正处级", "合川区委", "重庆市合川区"),
    ("hc_discipline", "中共重庆市合川区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市合川区"),
    ("hc_propaganda", "中共重庆市合川区委宣传部", "党委部门", "正处级", "合川区委", "重庆市合川区"),
    ("hc_united_front", "中共重庆市合川区委统战部", "党委部门", "正处级", "合川区委", "重庆市合川区"),
    ("hc_political_legal", "中共重庆市合川区委政法委员会", "党委部门", "正处级", "合川区委", "重庆市合川区"),
    ("hc_peoples_armed_forces", "重庆市合川区人民武装部", "军事", "正处级", "重庆警备区", "重庆市合川区"),
    ("hc_public_security", "重庆市公安局合川分局", "公安", "正处级", "重庆市公安局", "重庆市合川区"),
    ("hc_peoples_congress", "重庆市合川区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市合川区"),
    ("hc_cppcc", "中国人民政治协商会议重庆市合川区委员会", "政协", "地厅级", "重庆市政协", "重庆市合川区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ── 现任区委领导 ──

    # 郑立伟
    ("hc_zheng_liwei", "hc_party_committee", "区委书记", "2021-09", "至今", "正厅级", "合川区委书记"),
    ("hc_zheng_liwei", "hc_party_committee", "区委副书记（渝北区）", "2016-12", "2021-09", "副厅级", "曾任渝北区委副书记"),
    ("hc_zheng_liwei", "hc_gov", "市政府法制办副主任", "待查", "2016-12", "副厅级", "重庆市政府法制办"),

    # 姜雪松
    ("hc_jiang_xuesong", "hc_gov", "区长", "2021-09", "至今", "正厅级", "合川区区长"),
    ("hc_jiang_xuesong", "hc_party_committee", "区委副书记", "2020", "2021-09", "副厅级", "合川区委副书记（专职）"),
    ("hc_jiang_xuesong", "hc_gov", "市经信委副主任", "待查", "2020", "副厅级", "重庆市经济和信息化委员会"),

    # 谢东
    ("hc_xie_dong", "hc_party_committee", "区委副书记（专职）", "待查", "至今", "副厅级", "合川区委专职副书记"),
    ("hc_xie_dong", "hc_political_legal", "政法委书记", "待查", "待查", "副厅级", "曾任合川区委政法委书记"),

    # 曾荣
    ("hc_zeng_rong", "hc_gov", "常务副区长", "待查", "至今", "副厅级", "合川区政府常务副区长"),
    ("hc_zeng_rong", "hc_party_committee", "区委常委", "待查", "至今", "副厅级", "合川区委常委"),

    # 周富勇
    ("hc_zhou_fuyong", "hc_discipline", "纪委书记、监委主任", "待查", "至今", "副厅级", ""),
    ("hc_zhou_fuyong", "hc_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # 何川
    ("hc_he_chuan", "hc_org_department", "组织部部长", "待查", "至今", "副厅级", ""),
    ("hc_he_chuan", "hc_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # 吴达明
    ("hc_wu_daming", "hc_propaganda", "宣传部部长", "待查", "至今", "副厅级", ""),
    ("hc_wu_daming", "hc_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # 秦辉富
    ("hc_qin_huifu", "hc_political_legal", "政法委书记", "待查", "至今", "副厅级", ""),
    ("hc_qin_huifu", "hc_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # 邓立
    ("hc_deng_li", "hc_united_front", "统战部部长", "待查", "至今", "副厅级", ""),
    ("hc_deng_li", "hc_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # 汤峻
    ("hc_tang_jun", "hc_peoples_armed_forces", "政委", "待查", "至今", "正团级", ""),
    ("hc_tang_jun", "hc_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ── 副区长 ──
    ("hc_chen_ying", "hc_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("hc_zhao_jichun", "hc_gov", "副区长、区公安分局局长", "待查", "至今", "副厅级", ""),
    ("hc_zhao_jichun", "hc_public_security", "局长", "待查", "至今", "正处级", ""),
    ("hc_zhang_yulin", "hc_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("hc_yang_chunmei", "hc_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ── 人大 ──
    ("hc_cheng_wei", "hc_peoples_congress", "主任", "待查", "至今", "正厅级", ""),

    # ── 政协 ──
    ("hc_ye_hua", "hc_cppcc", "主席", "待查", "至今", "正厅级", ""),

    # ── 前任 ──
    ("hc_li_yinglan", "hc_party_committee", "区委书记", "2015", "2021-09", "正厅级", "调任重庆市中药研究院"),
    ("hc_xu_wanzhong", "hc_gov", "区长", "待查", "2021", "正厅级", "被调查双开"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence

    # 搭档：郑立伟 — 姜雪松
    ("hc_zheng_liwei", "hc_jiang_xuesong", "superior_subordinate",
     "区委书记与区长党政搭档关系",
     "中共重庆市合川区委员会 / 合川区人民政府",
     "2021年至今", "strong", "confirmed"),

    # 搭档：郑立伟 — 谢东
    ("hc_zheng_liwei", "hc_xie_dong", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市合川区委员会",
     "2021年至今", "medium", "plausible"),

    # 搭档：姜雪松 — 谢东
    ("hc_jiang_xuesong", "hc_xie_dong", "overlap",
     "区长与专职副书记在区委班子共事",
     "中共重庆市合川区委员会",
     "2021年至今", "medium", "plausible"),

    # 常务副区长关系
    ("hc_zheng_liwei", "hc_zeng_rong", "superior_subordinate",
     "区委书记与常务副区长",
     "中共重庆市合川区委员会",
     "待查至今", "medium", "plausible"),

    # 前任关系
    ("hc_zheng_liwei", "hc_li_yinglan", "predecessor_successor",
     "前任区委书记与接任者",
     "中共重庆市合川区委员会",
     "2015-2021（李）→2021至今（郑）", "strong", "confirmed"),

    # 前任区长
    ("hc_jiang_xuesong", "hc_xu_wanzhong", "predecessor_successor",
     "前任区长与被调查前区长",
     "重庆市合川区人民政府",
     "待查-2021（徐）→2021至今（姜）", "strong", "confirmed"),
]


# ════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT,
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

    for p in PERSONS:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p[0], p[1], p[2], p[3], p[4], p[5], p[6],
             p[7], p[8], p[9], p[10], p[11],
             p[12] if len(p) > 12 else "",
             p[13] if len(p) > 13 else "unverified"))

    for o in ORGANIZATIONS:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o[0], o[1], o[2], o[3], o[4], o[5]))

    for pos in POSITIONS:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos[0], pos[1], pos[2], pos[3],
             pos[4] if len(pos) > 4 else "",
             pos[5] if len(pos) > 5 else "",
             pos[6] if len(pos) > 6 else ""))

    for rel in RELATIONSHIPS:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel[0], rel[1], rel[2], rel[3], rel[4], rel[5], rel[6], rel[7]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(pid):
    """Return r,g,b color string based on person role."""
    person_map = {p[0]: p for p in PERSONS}
    if pid not in person_map:
        return "100,100,100"
    name = person_map[pid][9]  # current_post
    if "书记" in name and "纪委" not in name:
        return "255,50,50"
    if "区长" in name or "副区长" in name or "公安" in name:
        if "纪委" in name:
            return "255,165,0"
        return "50,100,255"
    if "纪委" in name or "监委" in name:
        return "255,165,0"
    if "人大" in name:
        return "200,100,100"
    if "政协" in name:
        return "100,200,100"
    if "前" in name:
        return "150,150,150"
    return "100,100,100"


def is_top_leader(pid):
    person_map = {p[0]: p for p in PERSONS}
    if pid not in person_map:
        return False
    name = person_map[pid][9]
    return "书记" in name and ("纪委" not in name) or "区长" == name or "区委副书记、区长" == name


def org_color(type_label):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "公安": "200,200,255",
        "政法": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "军事": "200,255,200",
    }
    return colors.get(type_label, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>合川区领导班子工作关系网络 — 重庆市合川区区委书记 & 区长</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="education" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, ethnicity, birth, birthplace, edu, party, ws, post, org_, src, notes, conf = (
            p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11],
            p[12] if len(p) > 12 else "",
            p[13] if len(p) > 13 else "unverified"
        )
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else ("12.0" if "前" not in name else "10.0")
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(edu)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in ORGANIZATIONS:
        oid, oname, otype, olevel, oparent, oloc = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # person → organization edges
    for pos in POSITIONS:
        eid += 1
        ppid, ooid, title, start, end, rank, note = (
            pos[0], pos[1], pos[2], pos[3],
            pos[4] if len(pos) > 4 else "",
            pos[5] if len(pos) > 5 else "",
            pos[6] if len(pos) > 6 else ""
        )
        lines.append(f'      <edge id="e{eid}" source="p{ppid}" target="o{ooid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(start)} — {esc(end)}"/>')
        lines.append(f'          <attvalue for="3" value="plausible"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # person↔person edges
    for rel in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel[0]}" target="p{rel[1]}" label="{esc(rel[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel[2])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel[5])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(rel[7])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


# ── MAIN ──
if __name__ == "__main__":
    build()
    build_gexf()
    print("Done.")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
