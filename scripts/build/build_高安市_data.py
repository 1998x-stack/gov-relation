#!/usr/bin/env python3
"""
高安市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Gao'an City leadership.

Research as of 2026-07-15:
- 市委书记: 罗功成 (since early July 2026, previously 樟树市长)
- 市长提名人选: 陈志军 (appointed early July 2026)
- 前任市委书记: 郑绍 (2021.08-2026.07, 任宜春市委常委)
- 前任市委书记: 袁和庚 (2016.07-2021.08, 2022年被查)
- 前任市长: 周万辉 (2022.09-2026.07, 去向待查)

Note: Full standing committee roster unavailable from open web. Core positions
are documented from Baidu Baike, appointment notices, and media reports.
"""

import sqlite3
import os
import json
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "高安市_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "高安市_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""

# ── DATA ──
# Person ID convention: gaoan_{surname_givenname}

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Current Leaders ═══

    # 市委书记 — 罗功成 (newly appointed July 2026)
    # Source: Baidu Baike 罗功成; 高品高安 news (2026-07-05)
    ("gaoan_luo_gongcheng", "罗功成", "男", "汉族", "1980-01", "江西宜丰", "中央党校大学",
     "中共党员", "1997-08",
     "市委书记", "中共高安市委员会",
     "Baidu Baike https://baike.baidu.com/item/%E7%BD%97%E5%8A%9F%E6%88%90 — 罗功成履历; 高品高安 2026-07-05 — 罗功成任高安市委书记"),

    # 市长提名人选 — 陈志军 (newly appointed July 2026)
    # Source: 高品高安 news (2026-07-05) — 市委副书记、市长提名人选
    # Note: Full biography pending — only appointment notice available
    ("gaoan_chen_zhijun", "陈志军", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委副书记、市长提名人选", "高安市人民政府",
     "高品高安 2026-07-05 — 陈志军同志任高安市委副书记、市长提名人选"),

    # ═══ Predecessors ═══

    # 前任市委书记 — 郑绍 (2021.08-2026.07, now 宜春市委常委 only)
    # Source: Baidu Baike 郑绍
    ("gaoan_zheng_shao", "郑绍", "男", "汉族", "1980-10", "江西濂溪区", "江西省委党校研究生/工商管理硕士",
     "中共党员", "1997（推算）",
     "宜春市委常委（原高安市委书记）", "中共宜春市委",
     "Baidu Baike https://baike.baidu.com/item/%E9%83%91%E7%BB%8D/577437 — 郑绍履历"),

    # 前任市长 — 周万辉 (2022.09-2026.07)
    # Source: Baidu Baike 周万辉
    ("gaoan_zhou_wanhui", "周万辉", "男", "汉族", "1978-11", "江西万载", "大学/法学学士",
     "2002-12", "2004-07",
     "原高安市委副书记、市长（去向待查）", "高安市人民政府",
     "Baidu Baike https://baike.baidu.com/item/%E5%91%A8%E4%B8%87%E8%BE%89/55694918 — 周万辉履历"),

    # 前前任市委书记 — 袁和庚 (2016.07-2021.08, 2022年被查)
    # Source: Baidu Baike 袁和庚
    ("gaoan_yuan_hegeng", "袁和庚", "男", "汉族", "1965-03", "江西袁州", "大学",
     "1986-06", "1984-08",
     "原宜春市政府党组成员、二级巡视员（被查）", "宜春市人民政府",
     "Baidu Baike https://baike.baidu.com/item/%E8%A2%81%E5%92%8C%E5%BA%9A — 袁和庚履历; 江西省纪委监委通报 2022-05"),

    # ═══ Other Known Leadership Figures (partial, from news reports) ═══

    ("gaoan_tao_yu", "陶宇", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_yan_weihua", "晏卫华", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_chen_wu", "陈武", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_gu_hongling", "古红玲", "女", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_xi_jiebin", "习杰斌", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_xiong_huihua", "熊慧华", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_jiang_lei", "江雷", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_lai_xiongwei", "赖雄伟", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),

    ("gaoan_xu_jialong", "许家龙", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "市委常委（职务待确认）", "中共高安市委员会",
     "高品高安 2026-07 — 领导名单"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)

    ("org_gaoan_cpc", "中共高安市委员会", "党委", "县级市", "中共宜春市委", "高安市"),
    ("org_gaoan_gov", "高安市人民政府", "政府", "县级市", "宜春市人民政府", "高安市"),
    ("org_gaoan_discipline", "中共高安市纪律检查委员会", "纪律检查", "县级市", "中共宜春市纪委", "高安市"),
    ("org_gaoan_org_dept", "中共高安市委组织部", "党委部门", "县级市", "中共高安市委员会", "高安市"),
    ("org_gaoan_propaganda", "中共高安市委宣传部", "党委部门", "县级市", "中共高安市委员会", "高安市"),
    ("org_gaoan_united_front", "中共高安市委统战部", "党委部门", "县级市", "中共高安市委员会", "高安市"),
    ("org_gaoan_legal_affairs", "中共高安市委政法委员会", "党委部门", "县级市", "中共高安市委员会", "高安市"),
    ("org_yichun_cpc", "中共宜春市委", "党委", "地级市", "中共江西省委", "宜春市"),
    ("org_yichun_gov", "宜春市人民政府", "政府", "地级市", "江西省人民政府", "宜春市"),
    ("org_zhangshu_gov", "樟树市人民政府", "政府", "县级市", "宜春市人民政府", "樟树市"),
    ("org_zhangshu_cpc", "中共樟树市委员会", "党委", "县级市", "中共宜春市委", "樟树市"),
    ("org_jingan_cpc", "中共靖安县委员会", "党委", "县", "中共宜春市委", "靖安县"),
    ("org_yongxiu_cpc", "中共永修县委员会", "党委", "县", "中共九江市委", "永修县"),
    ("org_yongxiu_gov", "永修县人民政府", "政府", "县", "九江市人民政府", "永修县"),
    ("org_jiujiang_tuanwei", "共青团九江市委", "群团", "地级市", "共青团江西省委", "九江市"),
    ("org_gaoan_npc", "高安市人大常委会", "人大", "县级市", "宜春市人大常委会", "高安市"),
    ("org_gaoan_ppcc", "高安市政协", "政协", "县级市", "宜春市政协", "高安市"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # 罗功成 — 现任市委书记
    ("gaoan_luo_gongcheng", "org_gaoan_cpc", "市委书记", "2026-07", "present", "正处级",
     "2026年7月从樟树市长调任高安市委书记"),

    # 罗功成 — 过往履历
    ("gaoan_luo_gongcheng", "org_zhangshu_gov", "樟树市委副书记、市长", "2023-08", "2026-07", "正处级",
     "2023年8月任代市长，2023年9月任市长"),
    ("gaoan_luo_gongcheng", "org_yichun_gov", "宜春市人民政府副秘书长、办公室主任", "2021-09", "2023-08", "正处级",
     "2021.09-2023.12 宜春市人民政府办公室主任"),
    ("gaoan_luo_gongcheng", "org_gaoan_cpc", "高安市委常委、常务副市长", "2019-01", "2021-09", "副处级",
     "2019.01起任高安市委常委、常务副市长"),
    ("gaoan_luo_gongcheng", "org_gaoan_cpc", "高安市政府副市长、党组成员", "2015-12", "2018-01", "副处级",
     "初至高安任职"),
    ("gaoan_luo_gongcheng", "org_gaoan_gov", "高安市政府副市长", "2015-12", "2018-01", "副处级",
     ""),

    # 陈志军 — 市长提名人选
    ("gaoan_chen_zhijun", "org_gaoan_cpc", "市委副书记", "2026-07", "present", "正处级",
     "2026年7月任"),
    ("gaoan_chen_zhijun", "org_gaoan_gov", "市长提名人选", "2026-07", "present", "正处级",
     "2026年7月提名高安市市长候选人"),

    # 郑绍 — 前任市委书记
    ("gaoan_zheng_shao", "org_yichun_cpc", "宜春市委常委", "2023-12", "present", "副厅级",
     "2023年12月任宜春市委常委，仍兼任高安市委书记至2026年7月"),
    ("gaoan_zheng_shao", "org_gaoan_cpc", "市委书记", "2021-08", "2026-07", "正处级",
     "2021年8月从靖安县委书记调任高安市委书记"),
    ("gaoan_zheng_shao", "org_yichun_gov", "宜春市政府副市长、党组成员", "2021-10", "2023-12", "副厅级",
     "兼任高安市委书记"),
    ("gaoan_zheng_shao", "org_jingan_cpc", "靖安县委书记", "2019-08", "2021-08", "正处级",
     ""),
    ("gaoan_zheng_shao", "org_yongxiu_cpc", "永修县委副书记", "2014-09", "2016-07", "正处级",
     "正县级"),
    ("gaoan_zheng_shao", "org_yongxiu_gov", "永修县委副书记、代县长/县长", "2016-07", "2019-08", "正处级",
     "2016.07代县长，2016.09县长"),
    ("gaoan_zheng_shao", "org_jiujiang_tuanwei", "共青团九江市委副书记/书记", "2007（估）", "2014-09", "正处级",
     "从团市委副书记升至书记"),

    # 周万辉 — 前任市长
    ("gaoan_zhou_wanhui", "org_gaoan_cpc", "高安市委副书记", "2022-05", "2026-07", "正处级",
     ""),
    ("gaoan_zhou_wanhui", "org_gaoan_gov", "高安市代市长/市长", "2022-06", "2026-07", "正处级",
     "2022.06代市长，2022.09正式当选市长"),
    ("gaoan_zhou_wanhui", "org_gaoan_cpc", "市长提名人选", "2022-05", "2022-06", "正处级",
     ""),
    ("gaoan_zhou_wanhui", "org_gaoan_cpc", "上高县委副书记、县长", "2021-08", "2022-05", "正处级",
     "调任高安前的职位"),
    ("gaoan_zhou_wanhui", "org_gaoan_cpc", "宜丰县委常委、常务副县长", "2020-12", "2021-08", "副处级",
     ""),
    ("gaoan_zhou_wanhui", "org_gaoan_cpc", "宜丰县委常委、组织部部长", "2018-01", "2020-11", "副处级",
     ""),
    ("gaoan_zhou_wanhui", "org_gaoan_cpc", "宜丰县政府副县长", "2016-10", "2018-01", "副处级",
     ""),
    ("gaoan_zhou_wanhui", "org_gaoan_cpc", "宜春市委统战部副调研员/科长", "2013-08", "2016-07", "副处级",
     "统战部系统任职，从秘书科科长到副调研员"),

    # 袁和庚 — 前前任书记
    ("gaoan_yuan_hegeng", "org_yichun_gov", "宜春市政府党组成员、二级巡视员", "2021-09", "2022-05", "副厅级",
     "2022年5月被免职，接受审查调查"),
    ("gaoan_yuan_hegeng", "org_gaoan_cpc", "市委书记", "2016-07", "2021-08", "正处级",
     "2020.04起一级调研员，2020.04起二级巡视员"),
    ("gaoan_yuan_hegeng", "org_gaoan_gov", "高安市委副书记、市长", "2012-10", "2016-07", "正处级",
     ""),
    ("gaoan_yuan_hegeng", "org_gaoan_cpc", "宜春市经济开发区管委会主任", "2010-04", "2012-10", "正处级",
     ""),
    ("gaoan_yuan_hegeng", "org_gaoan_cpc", "万载县委常委、副县长", "2004-12", "2010-04", "副处级",
     ""),
    ("gaoan_yuan_hegeng", "org_gaoan_cpc", "袁州区委常委、宣传部长", "2002-11", "2004-12", "副处级",
     ""),
]

# Confirmed relationships between people
RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)

    # 郑绍 — 罗功成: 前后任关系 (高安市委书记)
    ("gaoan_zheng_shao", "gaoan_luo_gongcheng", "predecessor_successor",
     "郑绍2021.08-2026.07任高安市委书记，2026年7月罗功成接任",
     "org_gaoan_cpc", "2019-01至2021-09（罗功成任高安市委常委期间与郑绍共事）",
     "strong", "confirmed"),

    # 罗功成 — 郑绍: 工作交集（罗在郑书记时期任高安常务副市长）
    ("gaoan_luo_gongcheng", "gaoan_zheng_shao", "overlap",
     "罗功成2019-2021年任高安市委常委、常务副市长，与郑绍在同一班子共事约2年",
     "org_gaoan_cpc", "2021-08至2021-09",
     "strong", "confirmed"),

    # 郑绍 — 袁和庚: 前后任关系 (高安市委书记)
    ("gaoan_zheng_shao", "gaoan_yuan_hegeng", "predecessor_successor",
     "袁和庚2016.07-2021.08任高安市委书记，郑绍2021年8月接任",
     "org_gaoan_cpc", "2021-08",
     "strong", "confirmed"),

    # 周万辉 — 郑绍: 搭班关系 (高安市长和书记)
    ("gaoan_zhou_wanhui", "gaoan_zheng_shao", "overlap",
     "周万辉2022年任高安市长，郑绍为市委书记，搭班约4年",
     "org_gaoan_cpc", "2022-09至2026-07",
     "strong", "confirmed"),

    # 罗功成 — 周万辉: 前任关系（罗是周在高安常务副市长任期的前任）
    ("gaoan_luo_gongcheng", "gaoan_zhou_wanhui", "overlap",
     "罗功成2019-2021年任高安常务副市长，此前周万辉在宜丰县委任职，交集待确认",
     "", "",
     "medium", "unverified"),

    # 罗功成 — 袁和庚: 工作交集
    ("gaoan_luo_gongcheng", "gaoan_yuan_hegeng", "overlap",
     "罗功成2015-2018年任高安副市长，袁和庚为市委书记",
     "org_gaoan_cpc", "2015-12至2018-01",
     "strong", "confirmed"),

    # 袁和庚 — 周万辉: 无直接交集
    ("gaoan_yuan_hegeng", "gaoan_zhou_wanhui", "overlap",
     "袁和庚2021年8月离任时，周万辉2022年才到高安，无直接交集",
     "", "",
     "weak", "unverified"),
]


# ── Build Functions ──

def build_db():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    )''')

    c.execute('''CREATE TABLE organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )''')

    c.execute('''CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )''')

    c.execute('''CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        strength TEXT, confidence TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )''')

    for p in PERSONS:
        c.execute('INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', p)

    for o in ORGANIZATIONS:
        c.execute('INSERT INTO organizations VALUES (?,?,?,?,?,?)', o)

    for pos in POSITIONS:
        c.execute('INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)', pos)

    for r in RELATIONSHIPS:
        c.execute('INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?,?,?,?,?,?,?,?)', r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def person_color(name):
    """Assign color based on role."""
    role_colors = [
        ("罗功成", "255,50,50"),      # Party Secretary - Red
        ("陈志军", "50,100,255"),     # Government leader - Blue
        ("郑绍", "255,50,50"),        # Former Party Secretary - Red
        ("周万辉", "50,100,255"),     # Former Government leader - Blue
        ("袁和庚", "255,165,0"),      # Discipline/Controversial - Orange
    ]
    for key, color in role_colors:
        if key in name:
            return color
    return "100,100,100"  # Grey for others


def is_top_leader(name):
    """Identify top leaders for node sizing."""
    top = ["罗功成", "陈志军", "郑绍", "周万辉", "袁和庚"]
    return any(t in name for t in top)


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪律检查": "255,165,0",
        "党委部门": "255,220,255",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf():
    """Create GEXF 1.3 graph file with viz namespace."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>高安市领导班子工作关系网络 - 罗功成/陈志军 period 2026.07</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="organization" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[9]
        org_name = p[10]
        c = person_color(name)
        sz = "20.0" if is_top_leader(name) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org_name)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        c = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{esc(oname)}">')
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

    # Person -> Organization (worked_at)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        period = f"{pos[3]}-{pos[4]}"
        weight = "2.0" if is_top_leader(next((p[1] for p in PERSONS if p[0] == pid), "")) else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(title)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationship)
    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        period = r[5]
        weight = "2.0" if r[6] == "strong" else ("1.0" if r[6] == "medium" else "0.5")
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    """Print summary statistics."""
    print(f"\n📊 高安市网络数据统计:")
    print(f"   人员: {len(PERSONS)}")
    print(f"   机构: {len(ORGANIZATIONS)}")
    print(f"   任职记录: {len(POSITIONS)}")
    print(f"   关系: {len(RELATIONSHIPS)}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    tables = ["persons", "organizations", "positions", "relationships"]
    for t in tables:
        count = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"   DB {t}: {count}")
    conn.close()


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_stats()
    print("\n✅ 高安市数据构建完成")
