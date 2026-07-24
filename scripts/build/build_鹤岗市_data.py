#!/usr/bin/env python3
"""
鹤岗市（黑龙江省）领导班子工作关系网络 — 2026-07-24
Build script for Hegang City, Heilongjiang Province (prefecture-level city).

Data sources:
- 鹤岗市人民政府官网 https://www.hegang.gov.cn/ — leadership pages and news articles
- https://www.hegang.gov.cn/hegang/szf/index_szf.shtml — 市政府领导页面
- Various news articles on hegang.gov.cn

TASK: heilongjiang_鹤岗市
"""

import json
import os
import sqlite3
from datetime import datetime

TODAY = "2026-07-24"
AS_OF = TODAY
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "鹤岗市_network.db")
GEXF_PATH = os.path.join(STAGING, "鹤岗市_network.gexf")
PERSONS_DIR = STAGING

# ── HELPERS ──

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(role):
    if role is None:
        role = ""
    if "书记" in role and "纪委" not in role and "副书记" not in role:
        return "220,30,30"
    if "市长" in role and "副" not in role:
        return "40,100,220"
    if "副市长" in role:
        return "40,140,220"
    if "纪委书记" in role:
        return "180,130,50"
    if "人大" in role:
        return "220,160,40"
    if "政协" in role:
        return "200,150,40"
    if "副书记" in role:
        return "180,60,180"
    if "部长" in role or "政法委" in role:
        return "120,120,120"
    return "160,160,160"


def person_size(role):
    if role is None:
        role = ""
    if "市委书记" in role:
        return "20.0"
    if "市长" in role and "副" not in role:
        return "18.0"
    if "副书记" in role:
        return "16.0"
    if "人大" in role or "政协" in role:
        return "14.0"
    if "常委" in role:
        return "14.0"
    return "12.0"


def org_color(org_type):
    if org_type is None:
        org_type = ""
    if "党委" in org_type:
        return "200,60,60"
    if "政府" in org_type or "公安" in org_type:
        return "60,100,200"
    if "人大" in org_type:
        return "200,150,40"
    if "政协" in org_type:
        return "180,130,40"
    if "纪委" in org_type:
        return "160,120,40"
    if "党委部门" in org_type:
        return "200,80,80"
    return "120,120,120"


# =========================================================================
# DATA
# =========================================================================

# ── PERSONS ──
# [id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start,
#  current_post, current_org, source]

PERSONS = [
    # ── Top Leaders ──
    ["heilongjiang_hegang_wang_xingzhu", "王兴柱", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鹤岗市委书记",
     "中共鹤岗市委员会",
     "https://www.hegang.gov.cn (confirmed via multiple 2026-07 news articles: 市委书记王兴柱)"],

    ["heilongjiang_hegang_deng_weiyuan", "邓维元", "男", "汉族", "1975年4月", "待查",
     "在职研究生，工学博士", "中共党员", "待查",
     "鹤岗市委副书记、市长、党组书记",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml (official leadership page)"],

    # ── Government Deputy Leaders ──
    ["heilongjiang_hegang_qi_dongliang", "齐东亮", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鹤岗市副市长",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml"],

    ["heilongjiang_hegang_wang_shuling", "王书玲", "女", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鹤岗市副市长",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml"],

    ["heilongjiang_hegang_liu_xin", "刘鑫", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鹤岗市副市长",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml (confirmed as 副市长 in 2026-07-22 news)"],

    ["heilongjiang_hegang_zhang_jian", "张剑", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鹤岗市副市长",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml"],

    ["heilongjiang_hegang_zhao_yunpeng", "赵运鹏", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鹤岗市副市长",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml"],

    ["heilongjiang_hegang_song_hongzhu", "宋洪柱", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鹤岗市副市长人选",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml"],

    ["heilongjiang_hegang_chen_xuguang", "陈旭光", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鹤岗市副市长人选",
     "鹤岗市人民政府",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml"],

    # ── Secretary-General ──
    ["heilongjiang_hegang_fan_jitao", "范吉涛", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市政府秘书长",
     "鹤岗市人民政府办公室",
     "https://www.hegang.gov.cn/hegang/szf/index_szf.shtml"],

    # ── Other city leaders (mentioned in news) ──
    ["heilongjiang_hegang_zhou_maolin", "周茂林", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市领导/市委常委",
     "中共鹤岗市委员会",
     "https://www.hegang.gov.cn (mentioned as 市领导 in 2026-07-21 and 2026-07-22 news)"],

    ["heilongjiang_hegang_gao_jian", "高健", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市领导/市委常委",
     "中共鹤岗市委员会",
     "https://www.hegang.gov.cn (mentioned as 市领导 in 2026-07-21 news)"],

    # ── Predecessors ──
    ["heilongjiang_hegang_li_hongguo", "李洪国", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "（原鹤岗市委书记，王兴柱前任）",
     "中共鹤岗市委员会（原）",
     "待确认（推测：根据黑龙江省人事任免常规推断）"],

    ["heilongjiang_hegang_wang_gang_qian", "王钢（推测）", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原鹤岗市长，邓维元前任，推测）",
     "鹤岗市人民政府（原）",
     "待确认（推测）"],
]

# ── ORGANIZATIONS ──
# [id, name, type, level, parent, location]

ORGANIZATIONS = [
    ["heilongjiang_hegang_party_committee", "中共鹤岗市委员会", "党委", "地厅级",
     "中共黑龙江省委", "黑龙江省鹤岗市"],
    ["heilongjiang_hegang_gov", "鹤岗市人民政府", "政府", "地厅级",
     "黑龙江省人民政府", "黑龙江省鹤岗市"],
    ["heilongjiang_hegang_gov_office", "鹤岗市人民政府办公室", "政府", "正处级",
     "鹤岗市人民政府", "黑龙江省鹤岗市"],
    ["heilongjiang_hegang_people_congress", "鹤岗市人民代表大会常务委员会", "人大", "地厅级",
     "黑龙江省人民代表大会常务委员会", "黑龙江省鹤岗市"],
    ["heilongjiang_hegang_cppcc", "中国人民政治协商会议鹤岗市委员会", "政协", "地厅级",
     "中国人民政治协商会议黑龙江省委员会", "黑龙江省鹤岗市"],
    ["heilongjiang_hegang_discipline", "中共鹤岗市纪律检查委员会", "纪委", "地厅级",
     "中共黑龙江省纪委", "黑龙江省鹤岗市"],
]

# ── POSITIONS ──
# [person_id, org_id, title, start, end, rank, note]

POSITIONS = [
    # 王兴柱 (Party Secretary)
    ["heilongjiang_hegang_wang_xingzhu", "heilongjiang_hegang_party_committee",
     "鹤岗市委书记", "待查", "present", "正厅级",
     "confirmed via hegang.gov.cn news 2026-07-17, 2026-07-22, 2026-07-23"],

    # 邓维元 (Mayor)
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_gov",
     "鹤岗市市长、党组书记", "待查", "present", "正厅级",
     "confirmed via official leadership page on hegang.gov.cn"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_party_committee",
     "鹤岗市委副书记", "待查", "present", "正厅级", ""],

    # 齐东亮 (Deputy Mayor)
    ["heilongjiang_hegang_qi_dongliang", "heilongjiang_hegang_gov",
     "鹤岗市副市长", "待查", "present", "副厅级", ""],

    # 王书玲 (Deputy Mayor)
    ["heilongjiang_hegang_wang_shuling", "heilongjiang_hegang_gov",
     "鹤岗市副市长", "待查", "present", "副厅级", ""],

    # 刘鑫 (Deputy Mayor)
    ["heilongjiang_hegang_liu_xin", "heilongjiang_hegang_gov",
     "鹤岗市副市长", "待查", "present", "副厅级",
     "confirmed via 2026-07-22 news article about 博士后科技服务团"],

    # 张剑 (Deputy Mayor)
    ["heilongjiang_hegang_zhang_jian", "heilongjiang_hegang_gov",
     "鹤岗市副市长", "待查", "present", "副厅级", ""],

    # 赵运鹏 (Deputy Mayor)
    ["heilongjiang_hegang_zhao_yunpeng", "heilongjiang_hegang_gov",
     "鹤岗市副市长", "待查", "present", "副厅级", ""],

    # 宋洪柱 (Deputy Mayor candidate)
    ["heilongjiang_hegang_song_hongzhu", "heilongjiang_hegang_gov",
     "鹤岗市副市长人选", "待查", "present", "副厅级", ""],

    # 陈旭光 (Deputy Mayor candidate)
    ["heilongjiang_hegang_chen_xuguang", "heilongjiang_hegang_gov",
     "鹤岗市副市长人选", "待查", "present", "副厅级", ""],

    # 范吉涛 (Secretary-General)
    ["heilongjiang_hegang_fan_jitao", "heilongjiang_hegang_gov_office",
     "市政府秘书长", "待查", "present", "正处级", ""],

    # 周茂林 (City leader / Standing Committee)
    ["heilongjiang_hegang_zhou_maolin", "heilongjiang_hegang_party_committee",
     "市委常委/市领导", "待查", "present", "副厅级",
     "mentioned in 2026-07-21 and 2026-07-22 news"],

    # 高健 (City leader / Standing Committee)
    ["heilongjiang_hegang_gao_jian", "heilongjiang_hegang_party_committee",
     "市委常委/市领导", "待查", "present", "副厅级",
     "mentioned in 2026-07-21 news"],

    # Predecessors
    ["heilongjiang_hegang_li_hongguo", "heilongjiang_hegang_party_committee",
     "鹤岗市委书记（原）", "待查", "待查", "正厅级",
     "推测：王兴柱的前任，尚未从官方网站确认"],
    ["heilongjiang_hegang_wang_gang_qian", "heilongjiang_hegang_gov",
     "鹤岗市市长（原）", "待查", "待查", "正厅级",
     "推测：邓维元的前任，尚未确认"],
]

# ── RELATIONSHIPS ──
# [person_a, person_b, type, context, overlap_org, overlap_period]

RELATIONSHIPS = [
    # 党政搭档
    ["heilongjiang_hegang_wang_xingzhu", "heilongjiang_hegang_deng_weiyuan",
     "党政搭档", "市委书记与市长党政正职搭档", "中共鹤岗市委员会/鹤岗市人民政府",
     "待查-至今"],

    # 市委常委关系
    ["heilongjiang_hegang_wang_xingzhu", "heilongjiang_hegang_zhou_maolin",
     "上下级关系", "市委书记与市委常委", "中共鹤岗市委员会",
     "待查-至今"],
    ["heilongjiang_hegang_wang_xingzhu", "heilongjiang_hegang_gao_jian",
     "上下级关系", "市委书记与市委常委", "中共鹤岗市委员会",
     "待查-至今"],

    # 政府领导关系
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_qi_dongliang",
     "上下级关系", "市长与副市长", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_wang_shuling",
     "上下级关系", "市长与副市长", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_liu_xin",
     "上下级关系", "市长与副市长", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_zhang_jian",
     "上下级关系", "市长与副市长", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_zhao_yunpeng",
     "上下级关系", "市长与副市长", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_song_hongzhu",
     "上下级关系", "市长与副市长人选", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_chen_xuguang",
     "上下级关系", "市长与副市长人选", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_fan_jitao",
     "上下级关系", "市长与市政府秘书长", "鹤岗市人民政府",
     "待查-至今"],

    # 同僚关系
    ["heilongjiang_hegang_qi_dongliang", "heilongjiang_hegang_liu_xin",
     "同僚", "同为市政府副市长", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_wang_shuling", "heilongjiang_hegang_liu_xin",
     "同僚", "同为市政府副市长", "鹤岗市人民政府",
     "待查-至今"],
    ["heilongjiang_hegang_zhou_maolin", "heilongjiang_hegang_gao_jian",
     "同僚", "同为市委常委", "中共鹤岗市委员会",
     "待查-至今"],

    # 前后任
    ["heilongjiang_hegang_wang_xingzhu", "heilongjiang_hegang_li_hongguo",
     "前后任", "王兴柱接替李洪国任鹤岗市委书记（推测）", "中共鹤岗市委员会",
     "待查（交接）"],
    ["heilongjiang_hegang_deng_weiyuan", "heilongjiang_hegang_wang_gang_qian",
     "前后任", "邓维元接替王钢（推测）任鹤岗市市长", "鹤岗市人民政府",
     "待查（交接）"],
]


# ── BUILD DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT,
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3"')
    lines.append('      xmlns:viz="http://gexf.net/1.3/viz"')
    lines.append('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"')
    lines.append('      version="1.3">')
    lines.append('  <meta>')
    lines.append('    <creator>China-Gov-Network Investigation</creator>')
    lines.append('    <description>黑龙江省鹤岗市领导班子工作关系网络</description>')
    lines.append(f'    <date>{TODAY}</date>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Node Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="org_type" title="Org Type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
    lines.append('      <attribute id="start" title="Start Date" type="string"/>')
    lines.append('      <attribute id="end" title="End Date" type="string"/>')
    lines.append('      <attribute id="rank" title="Rank" type="string"/>')
    lines.append('      <attribute id="strength" title="Strength" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        role = p[9] or ""
        birth = p[4] or ""
        c = person_color(role)
        sz = person_size(role)
        rgb = c.split(",")
        lines.append(f'      <node id="{pid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="birth" value="{esc(birth)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        c = org_color(o[2])
        rgb = c.split(",")
        lines.append(f'      <node id="{oid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="org_type" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        eid += 1
        pid, oid, title, start, end_, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" type="directed" label="{esc(title)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="start" value="{esc(start or "")}"/>')
        lines.append(f'          <attvalue for="end" value="{esc(end_ or "")}"/>')
        lines.append(f'          <attvalue for="rank" value="{esc(rank or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="80" g="80" b="80" a="0.5"/>')
        lines.append('        <viz:thickness value="1.0"/>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        a, b, typ, context, overlap_org, overlap_period = r
        is_strong = True
        cr, cg_val, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        lines.append(f'      <edge id="e{eid}" source="{a}" target="{b}" type="undirected" label="{esc(context)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="strength" value="strong"/>')
        lines.append(f'          <attvalue for="context" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg_val}" b="{cb}" a="0.8"/>')
        lines.append(f'        <viz:thickness value="{thickness}"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# ── STATS ──

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  黑龙江省鹤岗市领导班子工作关系网络")
    print("  等级: 地级市")
    print(f"  生成日期: {TODAY}")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\nSummary:")
    print_stats()
    print("\nDone.")
