#!/usr/bin/env python3
"""
鸡西市（黑龙江省）领导班子工作关系网络 — 2026-07-24
Build script for Jixi City, Heilongjiang Province (prefecture-level city).

Data sources:
- 鸡西市人民政府官网 https://www.jixi.gov.cn/ — leadership pages and news
- Official leadership bio pages for each cadre member
- Various local news outlets

TASK: heilongjiang_鸡西市
"""

import json
import os
import sqlite3
from datetime import datetime

TODAY = "2026-07-24"
AS_OF = TODAY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", "..", ".."))
STAGING = BASE_DIR  # Same as data/tmp/heilongjiang_鸡西市
DB_PATH = os.path.join(STAGING, "鸡西市_network.db")
GEXF_PATH = os.path.join(STAGING, "鸡西市_network.gexf")
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

TODAY = "2026-07-24"

# ── PERSONS ──
# [id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start,
#  current_post, current_org, source]

PERSONS = [
    # ── Top Leaders ──
    ["heilongjiang_jixi_sun_chengkun", "孙成坤", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市委书记",
     "中共鸡西市委员会",
     "https://www.jixi.gov.cn (confirmed 市委书记 as of 2026-07-17 via news article)"],

    ["heilongjiang_jixi_xie_zhiqiang", "谢志强", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市委副书记、市长",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100011/202308/c06_144913.shtml"],

    # ── Government Deputy Leaders ──
    ["heilongjiang_jixi_gao_yunlu", "高运禄", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市委常委、常务副市长",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100012/202402/c06_288003.shtml"],

    ["heilongjiang_jixi_yu_jun", "于君", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市委常委、副市长，鸡冠区委书记",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100012/202603/c06_359134.shtml"],

    ["heilongjiang_jixi_guo_xianwen", "郭显文", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市政府副市长、党组成员（援藏）",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100012/202308/c06_144908.shtml"],

    ["heilongjiang_jixi_zhou_cheng", "周诚", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市政府副市长、党组成员",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100012/202308/c06_144906.shtml"],

    ["heilongjiang_jixi_xu_xiaoli", "徐晓利", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市政府副市长、市公安局党委书记、局长、督察长",
     "鸡西市人民政府/鸡西市公安局",
     "https://www.jixi.gov.cn/jixi/c100012/202308/c06_144905.shtml"],

    ["heilongjiang_jixi_li_chunyu", "李春宇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市政府副市长、党组成员",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100012/202401/c06_283551.shtml"],

    ["heilongjiang_jixi_qi_jianping", "齐剑萍", "女", "汉族", "待查", "待查",
     "待查", "待查",
     "待查",
     "鸡西市政府副市长",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100012/202507/c06_337501.shtml"],

    # ── Secretary-General ──
    ["heilongjiang_jixi_tang_lijun", "唐利军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "市政府党组成员、市政府秘书长",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn/jixi/c100020/202201/c06_15034.shtml"],

    # ── People's Congress & CPPCC ──
    ["heilongjiang_jixi_zhang_xingbin", "张行斌", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鸡西市人大常委会主任（推测）",
     "鸡西市人民代表大会常务委员会",
     "https://www.jixi.gov.cn (inferred from news: 市领导张行斌出席孙成坤专题党课)"],

    ["heilongjiang_jixi_zheng_yesheng", "郑野岩", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "鸡西市政协主席",
     "中国人民政治协商会议鸡西市委员会",
     "https://www.jixi.gov.cn (confirmed 市政协主席 主持市政协常委会)"],

    # ── Other Key Figures ──
    ["heilongjiang_jixi_li_yunzhi", "李云志", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市政协党组成员/有关领导",
     "中国人民政治协商会议鸡西市委员会",
     "https://www.jixi.gov.cn (mentioned in 市政协 news as 作调研报告)"],

    ["heilongjiang_jixi_wang_junbing", "王均兵", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市政协有关领导",
     "中国人民政治协商会议鸡西市委员会",
     "https://www.jixi.gov.cn (mentioned in 市政协会议)"],

    ["heilongjiang_jixi_tang_chunzheng", "唐春正", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市政协有关领导",
     "中国人民政治协商会议鸡西市委员会",
     "https://www.jixi.gov.cn (mentioned in 市政协会议)"],

    ["heilongjiang_jixi_wang_xiaofeng", "王晓锋", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市政协有关领导",
     "中国人民政治协商会议鸡西市委员会",
     "https://www.jixi.gov.cn (mentioned in 市政协会议)"],

    ["heilongjiang_jixi_liu_huizhi", "刘会芝", "女", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市政协有关领导/市政府有关领导",
     "鸡西市人民政府",
     "https://www.jixi.gov.cn (mentioned in both 市政协 and 市政府 meetings)"],

    ["heilongjiang_jixi_wang_xiaodong", "王晓东", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "市政协有关领导",
     "中国人民政治协商会议鸡西市委员会",
     "https://www.jixi.gov.cn (mentioned in 市政协会议)"],

    # ── Predecessors ──
    ["heilongjiang_jixi_lu_changyou", "鲁长友", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原鸡西市委书记，孙成坤前任）",
     "中共鸡西市委员会（原）",
     "https://www.jixi.gov.cn (predecessor; inferred from news timeline)"],

    ["heilongjiang_jixi_sun_chengkun_pre_mayor", "孙成坤（原市长）", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原鸡西市长，后升任市委书记）",
     "鸡西市人民政府（原）",
     "https://www.jixi.gov.cn (inferred: 孙成坤从市长升任市委书记)"],

    ["heilongjiang_jixi_ye_zhongsong_prev", "叶忠松（推测）", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原鸡西市长，谢志强前任，推测）",
     "鸡西市人民政府（原）",
     "待确认（推测）"],
]

# ── ORGANIZATIONS ──
# [id, name, type, level, parent, location]

ORGANIZATIONS = [
    ["heilongjiang_jixi_party_committee", "中共鸡西市委员会", "党委", "地厅级",
     "中共黑龙江省委", "黑龙江省鸡西市"],
    ["heilongjiang_jixi_gov", "鸡西市人民政府", "政府", "地厅级",
     "黑龙江省人民政府", "黑龙江省鸡西市"],
    ["heilongjiang_jixi_discipline", "中共鸡西市纪律检查委员会", "纪委", "地厅级",
     "中共黑龙江省纪委", "黑龙江省鸡西市"],
    ["heilongjiang_jixi_gov_office", "鸡西市人民政府办公室", "政府", "正处级",
     "鸡西市人民政府", "黑龙江省鸡西市"],
    ["heilongjiang_jixi_public_security", "鸡西市公安局", "政府", "正处级",
     "鸡西市人民政府", "黑龙江省鸡西市"],
    ["heilongjiang_jixi_people_congress", "鸡西市人民代表大会常务委员会", "人大", "地厅级",
     "黑龙江省人民代表大会常务委员会", "黑龙江省鸡西市"],
    ["heilongjiang_jixi_cppcc", "中国人民政治协商会议鸡西市委员会", "政协", "地厅级",
     "中国人民政治协商会议黑龙江省委员会", "黑龙江省鸡西市"],
    ["heilongjiang_jixi_jiguan_district", "鸡西市鸡冠区委员会/政府", "党委/政府", "县处级",
     "鸡西市", "黑龙江省鸡西市鸡冠区"],
]

# ── POSITIONS ──
# [person_id, org_id, title, start, end, rank, note]

POSITIONS = [
    # 孙成坤 (Party Secretary)
    ["heilongjiang_jixi_sun_chengkun", "heilongjiang_jixi_party_committee",
     "鸡西市委书记", "待查", "present", "正厅级",
     "confirmed via gov website news 2026-07-17"],

    # 谢志强 (Mayor)
    ["heilongjiang_jixi_xie_zhiqiang", "heilongjiang_jixi_gov",
     "鸡西市市长、党组书记", "待查", "present", "正厅级",
     "confirmed via official bio page"],
    ["heilongjiang_jixi_xie_zhiqiang", "heilongjiang_jixi_party_committee",
     "鸡西市委副书记", "待查", "present", "正厅级", ""],

    # 高运禄 (Executive Deputy Mayor)
    ["heilongjiang_jixi_gao_yunlu", "heilongjiang_jixi_gov",
     "鸡西市委常委、常务副市长", "待查", "present", "副厅级",
     "confirmed via official bio page"],
    ["heilongjiang_jixi_gao_yunlu", "heilongjiang_jixi_party_committee",
     "鸡西市委常委", "待查", "present", "副厅级", ""],

    # 于君 (Deputy Mayor & Jiguan District Secretary)
    ["heilongjiang_jixi_yu_jun", "heilongjiang_jixi_gov",
     "鸡西市委常委、副市长", "待查", "present", "副厅级",
     "confirmed via official bio page"],
    ["heilongjiang_jixi_yu_jun", "heilongjiang_jixi_party_committee",
     "鸡西市委常委", "待查", "present", "副厅级", ""],
    ["heilongjiang_jixi_yu_jun", "heilongjiang_jixi_jiguan_district",
     "鸡冠区委书记", "待查", "present", "县处级", ""],

    # 郭显文 (Deputy Mayor, Tibet mission)
    ["heilongjiang_jixi_guo_xianwen", "heilongjiang_jixi_gov",
     "鸡西市政府副市长、党组成员", "待查", "present", "副厅级",
     "援藏3年，目前在西藏日喀则"],

    # 周诚 (Deputy Mayor)
    ["heilongjiang_jixi_zhou_cheng", "heilongjiang_jixi_gov",
     "鸡西市政府副市长、党组成员", "待查", "present", "副厅级",
     "分管教育、民政、卫健等"],

    # 徐晓利 (Deputy Mayor & Public Security)
    ["heilongjiang_jixi_xu_xiaoli", "heilongjiang_jixi_gov",
     "鸡西市政府副市长", "待查", "present", "副厅级", ""],
    ["heilongjiang_jixi_xu_xiaoli", "heilongjiang_jixi_public_security",
     "市公安局党委书记、局长、督察长", "待查", "present", "正处级", ""],

    # 李春宇 (Deputy Mayor)
    ["heilongjiang_jixi_li_chunyu", "heilongjiang_jixi_gov",
     "鸡西市政府副市长、党组成员", "待查", "present", "副厅级",
     "分管工信、科技、农业农村、水利等"],

    # 齐剑萍 (Deputy Mayor)
    ["heilongjiang_jixi_qi_jianping", "heilongjiang_jixi_gov",
     "鸡西市政府副市长", "2025-07", "present", "副厅级",
     "分管市场监管、营商环境、商务、外事等"],

    # 唐利军 (Secretary-General)
    ["heilongjiang_jixi_tang_lijun", "heilongjiang_jixi_gov_office",
     "市政府党组成员、市政府秘书长", "待查", "present", "正处级",
     "confirmed via official bio page"],

    # 张行斌 (People's Congress)
    ["heilongjiang_jixi_zhang_xingbin", "heilongjiang_jixi_people_congress",
     "市人大常委会主任（推测）", "待查", "present", "正厅级",
     "inferred from news article"],

    # 郑野岩 (CPPCC)
    ["heilongjiang_jixi_zheng_yesheng", "heilongjiang_jixi_cppcc",
     "市政协主席", "待查", "present", "正厅级",
     "confirmed via news article 2026-07-20"],

    # Predecessors
    ["heilongjiang_jixi_lu_changyou", "heilongjiang_jixi_party_committee",
     "鸡西市委书记", "待查", "待查", "正厅级",
     "孙成坤的前任，推测鲁长友曾担任鸡西市委书记"],
    ["heilongjiang_jixi_sun_chengkun_pre_mayor", "heilongjiang_jixi_gov",
     "鸡西市市长", "待查", "待查", "正厅级",
     "孙成坤在升任市委书记前曾担任鸡西市市长"],
]

# ── RELATIONSHIPS ──
# [person_a, person_b, type, context, overlap_org, overlap_period]

RELATIONSHIPS = [
    # 党政搭档
    ["heilongjiang_jixi_sun_chengkun", "heilongjiang_jixi_xie_zhiqiang",
     "党政搭档", "市委书记与市长党政正职搭档", "中共鸡西市委员会/鸡西市人民政府",
     "待查-至今"],

    # 市委常委副职关系
    ["heilongjiang_jixi_sun_chengkun", "heilongjiang_jixi_gao_yunlu",
     "上下级关系", "市委书记与常务副市长", "中共鸡西市委员会",
     "待查-至今"],
    ["heilongjiang_jixi_xie_zhiqiang", "heilongjiang_jixi_gao_yunlu",
     "上下级关系", "市长与常务副市长", "鸡西市人民政府",
     "待查-至今"],
    ["heilongjiang_jixi_xie_zhiqiang", "heilongjiang_jixi_tang_lijun",
     "上下级关系", "市长与市政府秘书长", "鸡西市人民政府",
     "待查-至今"],

    # 同僚关系
    ["heilongjiang_jixi_gao_yunlu", "heilongjiang_jixi_yu_jun",
     "同僚", "同为市委常委、副市长", "中共鸡西市委员会",
     "待查-至今"],
    ["heilongjiang_jixi_gao_yunlu", "heilongjiang_jixi_zhou_cheng",
     "同僚", "同为市政府领导", "鸡西市人民政府",
     "待查-至今"],
    ["heilongjiang_jixi_gao_yunlu", "heilongjiang_jixi_xu_xiaoli",
     "同僚", "同为市政府领导", "鸡西市人民政府",
     "待查-至今"],
    ["heilongjiang_jixi_gao_yunlu", "heilongjiang_jixi_li_chunyu",
     "同僚", "同为市政府领导", "鸡西市人民政府",
     "待查-至今"],
    ["heilongjiang_jixi_gao_yunlu", "heilongjiang_jixi_qi_jianping",
     "同僚", "同为市政府领导", "鸡西市人民政府",
     "待查-至今"],
    ["heilongjiang_jixi_zhou_cheng", "heilongjiang_jixi_li_chunyu",
     "同僚", "同为市政府副市长", "鸡西市人民政府",
     "待查-至今"],

    # 前后任
    ["heilongjiang_jixi_sun_chengkun", "heilongjiang_jixi_lu_changyou",
     "前后任", "孙成坤接替鲁长友任鸡西市委书记（推测）", "中共鸡西市委员会",
     "待查（交接）"],
    ["heilongjiang_jixi_xie_zhiqiang", "heilongjiang_jixi_sun_chengkun_pre_mayor",
     "前后任", "谢志强接替孙成坤（原市长）任鸡西市市长", "鸡西市人民政府",
     "待查（交接）"],

    # 人大/政协
    ["heilongjiang_jixi_sun_chengkun", "heilongjiang_jixi_zhang_xingbin",
     "党政与人大", "市委书记与市人大常委会主任", "中共鸡西市委员会/鸡西市人大常委会",
     "待查-至今"],
    ["heilongjiang_jixi_sun_chengkun", "heilongjiang_jixi_zheng_yesheng",
     "党政与政协", "市委书记与市政协主席", "中共鸡西市委员会/鸡西市政协",
     "待查-至今"],
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
    lines.append('    <description>黑龙江省鸡西市领导班子工作关系网络</description>')
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
    print("  黑龙江省鸡西市领导班子工作关系网络")
    print("  等级: 地级市")
    print(f"  生成日期: {TODAY}")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\nSummary:")
    print_stats()
    print("\nDone.")
