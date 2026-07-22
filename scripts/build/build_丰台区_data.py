#!/usr/bin/env python3
"""
北京市丰台区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Fengtai District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjft.gov.cn (official government site)
- Publicly available appointment notices and media reports
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "丰台区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "丰台区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子 ──
    ("ft_wang_shaofeng", "王少峰", "男", "汉族", "1965年4月", "山东日照",
     "北京大学法学博士", "1987年12月", "1990年7月",
     "区委书记", "中共北京市丰台区委员会",
     "bjft.gov.cn;media:people.cn"),

    ("ft_chu_junwei", "初军威", "男", "汉族", "1971年12月", "山东莱阳",
     "北京理工大学工学博士", "1995年6月", "1995年7月",
     "区委副书记、区长", "北京市丰台区人民政府",
     "bjft.gov.cn;media:people.cn"),

    ("ft_tian_tao", "田涛", "男", "汉族", "1972年8月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区委副书记", "中共北京市丰台区委员会",
     "bjft.gov.cn/official"),

    ("ft_lian_yuhui", "廉钰辉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区纪委书记、区监委主任", "中共北京市丰台区纪律检查委员会",
     "bjft.gov.cn/official"),

    ("ft_tian_yandong", "田艳东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "北京市丰台区人民政府",
     "bjft.gov.cn/official"),

    ("ft_gui_yu", "桂昱", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市丰台区委宣传部",
     "bjft.gov.cn/official"),

    ("ft_liu_yonghong", "刘永洪", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市丰台区委组织部",
     "bjft.gov.cn/official"),

    ("ft_liu_yongjie", "刘永杰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共北京市丰台区委政法委员会",
     "bjft.gov.cn/official"),

    ("ft_zhao_xiuping", "赵秀萍", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共北京市丰台区委统战部",
     "bjft.gov.cn/official"),

    ("ft_gao_feng", "高峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长", "北京市丰台区人民政府",
     "bjft.gov.cn/official"),

    # ── 副区长（除常委外） ──
    ("ft_chen_li", "陈丽", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市丰台区人民政府",
     "bjft.gov.cn/official"),

    ("ft_gao_rongjun", "高荣军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、区公安分局局长", "北京市公安局丰台分局",
     "bjft.gov.cn/official"),

    ("ft_li_zongrong", "李宗荣", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市丰台区人民政府",
     "bjft.gov.cn/official"),

    ("ft_dai_wei", "戴伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市丰台区人民政府",
     "bjft.gov.cn/official"),

    ("ft_wu_kun", "吴坤", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市丰台区人民政府",
     "bjft.gov.cn/official"),

    # ── 人大 ──
    ("ft_feng_yuanxiang", "冯源祥", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "北京市丰台区人民代表大会常务委员会",
     "bjft.gov.cn/official"),

    # ── 政协 ──
    ("ft_li_jiacheng", "李嘉诚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议北京市丰台区委员会",
     "bjft.gov.cn/official"),

    # ── 前主要领导 ──
    ("ft_xu_guangbin", "徐光彬", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前区委书记", "已离任",
     "media:thepaper.cn;baike.baidu.com"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("ft_party_committee", "中共北京市丰台区委员会", "党委", "地厅级", "中共北京市委", "北京市丰台区"),
    ("ft_gov", "北京市丰台区人民政府", "政府", "地厅级", "北京市人民政府", "北京市丰台区"),
    ("ft_org_department", "中共北京市丰台区委组织部", "党委部门", "正处级", "丰台区委", "北京市丰台区"),
    ("ft_discipline", "中共北京市丰台区纪律检查委员会", "纪委", "地厅级", "北京市纪委监委", "北京市丰台区"),
    ("ft_propaganda", "中共北京市丰台区委宣传部", "党委部门", "正处级", "丰台区委", "北京市丰台区"),
    ("ft_united_front", "中共北京市丰台区委统战部", "党委部门", "正处级", "丰台区委", "北京市丰台区"),
    ("ft_political_legal", "中共北京市丰台区委政法委员会", "党委部门", "正处级", "丰台区委", "北京市丰台区"),
    ("ft_party_school", "中共北京市丰台区委党校", "党委部门", "正处级", "丰台区委", "北京市丰台区"),
    ("ft_public_security", "北京市公安局丰台分局", "公安", "正处级", "北京市公安局", "北京市丰台区"),
    ("ft_peoples_congress", "北京市丰台区人民代表大会常务委员会", "人大", "地厅级", "北京市人大常委会", "北京市丰台区"),
    ("ft_cppcc", "中国人民政治协商会议北京市丰台区委员会", "政协", "地厅级", "北京市政协", "北京市丰台区"),
    ("ft_development_zone", "中关村科技园区丰台园管委会", "开发区", "正处级", "北京市丰台区人民政府", "北京市丰台区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 王少峰 — 区委书记 ═══
    ("ft_wang_shaofeng", "ft_party_committee", "区委书记", "2023-03", "至今", "正厅级", "主持区委全面工作。前任为北京经济技术开发区工委书记"),
    # 履历缺口（早年的详细履历）
    ("ft_wang_shaofeng", "ft_org_department", "履历缺口（签字前约33年职业生涯）", "1990", "2023-03", "未知", "公开资料记载其历任共青团北京市委、北京市委组织部副部长等职，具体时间线待完善"),

    # ═══ 初军威 — 区长 ═══
    ("ft_chu_junwei", "ft_gov", "区长", "2022-01", "至今", "正厅级", "区政府党组书记。2021年12月任代区长，2022年1月正式当选"),
    ("ft_chu_junwei", "ft_party_committee", "区委副书记", "2021-12", "至今", "正厅级", "兼任"),
    # 履历缺口
    ("ft_chu_junwei", "ft_org_department", "履历缺口（部分早期职业生涯）", "1995", "2021-12", "未知", "公开资料记载其曾任北京理工大学、中关村科技园区等职，具体时间线需补充"),

    # ═══ 田涛 — 区委副书记 ═══
    ("ft_tian_tao", "ft_party_committee", "区委副书记", "待查", "至今", "副厅级", "协助区委书记处理区委日常事务"),
    ("ft_tian_tao", "ft_party_school", "区委党校校长（兼）", "待查", "至今", "副厅级", "兼任"),

    # ═══ 廉钰辉 — 纪委书记 ═══
    ("ft_lian_yuhui", "ft_discipline", "区委常委、纪委书记、监委主任", "待查", "至今", "副厅级", "纪检监察系统"),
    ("ft_lian_yuhui", "ft_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 田艳东 — 常务副区长 ═══
    ("ft_tian_yandong", "ft_gov", "常务副区长", "待查", "至今", "副厅级", "区政府党组副书记"),
    ("ft_tian_yandong", "ft_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 桂昱 — 宣传部长 ═══
    ("ft_gui_yu", "ft_propaganda", "区委常委、宣传部部长", "待查", "至今", "副厅级", ""),
    ("ft_gui_yu", "ft_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 刘永洪 — 组织部长 ═══
    ("ft_liu_yonghong", "ft_org_department", "区委常委、组织部部长", "待查", "至今", "副厅级", ""),
    ("ft_liu_yonghong", "ft_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 刘永杰 — 政法委书记 ═══
    ("ft_liu_yongjie", "ft_political_legal", "区委常委、政法委书记", "待查", "至今", "副厅级", ""),
    ("ft_liu_yongjie", "ft_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 赵秀萍 — 统战部长 ═══
    ("ft_zhao_xiuping", "ft_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级", ""),
    ("ft_zhao_xiuping", "ft_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 高峰 — 副区长（常委） ═══
    ("ft_gao_feng", "ft_gov", "区委常委、副区长", "待查", "至今", "副厅级", "区政府党组成员"),
    ("ft_gao_feng", "ft_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 副区长们 ═══
    ("ft_chen_li", "ft_gov", "副区长", "待查", "至今", "副厅级", "区政府党组成员"),
    ("ft_gao_rongjun", "ft_gov", "副区长、区公安分局局长", "待查", "至今", "副厅级", ""),
    ("ft_gao_rongjun", "ft_public_security", "公安分局党委书记、局长", "待查", "至今", "正处级", ""),
    ("ft_li_zongrong", "ft_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("ft_dai_wei", "ft_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("ft_wu_kun", "ft_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 人大 ═══
    ("ft_feng_yuanxiang", "ft_peoples_congress", "区人大常委会党组书记、主任", "待查", "至今", "正厅级", ""),

    # ═══ 政协 ═══
    ("ft_li_jiacheng", "ft_cppcc", "区政协党组书记、主席", "待查", "至今", "正厅级", ""),

    # ═══ 前区委书记 ═══
    ("ft_xu_guangbin", "ft_party_committee", "区委书记（前任）", "待查", "2023-03", "正厅级", "王少峰的前任"),
]

# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 王少峰 ↔ 初军威 — 党政正职搭档
    ("ft_wang_shaofeng", "ft_chu_junwei", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共北京市丰台区委员会/丰台区人民政府", "2023-03至今"),

    # 王少峰 ↔ 田涛 — 书记-副书记
    ("ft_wang_shaofeng", "ft_tian_tao", "superior_subordinate",
     "区委书记与区委副书记（日常事务协助）",
     "中共北京市丰台区委员会", "待查至今"),

    # 王少峰 ↔ 廉钰辉 — 书记-纪委书记
    ("ft_wang_shaofeng", "ft_lian_yuhui", "superior_subordinate",
     "区委书记与纪委书记（从严治党主体责任）",
     "中共北京市丰台区委员会", "待查至今"),

    # 王少峰 ↔ 田艳东 — 书记-常务副区长
    ("ft_wang_shaofeng", "ft_tian_yandong", "superior_subordinate",
     "区委书记与常务副区长",
     "中共北京市丰台区委员会", "待查至今"),

    # 初军威 ↔ 田艳东 — 区长-常务副区长
    ("ft_chu_junwei", "ft_tian_yandong", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "北京市丰台区人民政府", "待查至今"),

    # 王少峰 ↔ 刘永洪 — 书记-组织部长
    ("ft_wang_shaofeng", "ft_liu_yonghong", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共北京市丰台区委员会", "待查至今"),

    # 王少峰 ↔ 刘永杰 — 书记-政法委书记
    ("ft_wang_shaofeng", "ft_liu_yongjie", "superior_subordinate",
     "区委书记与政法委书记",
     "中共北京市丰台区委员会", "待查至今"),

    # 王少峰 ↔ 桂昱 — 书记-宣传部长
    ("ft_wang_shaofeng", "ft_gui_yu", "superior_subordinate",
     "区委书记与宣传部部长",
     "中共北京市丰台区委员会", "待查至今"),

    # 王少峰 ↔ 赵秀萍 — 书记-统战部长
    ("ft_wang_shaofeng", "ft_zhao_xiuping", "superior_subordinate",
     "区委书记与统战部部长",
     "中共北京市丰台区委员会", "待查至今"),

    # 王少峰 ↔ 高峰 — 书记-常委副区长
    ("ft_wang_shaofeng", "ft_gao_feng", "superior_subordinate",
     "区委书记与常委副区长",
     "中共北京市丰台区委员会", "待查至今"),

    # 初军威 ↔ 高峰 — 区长-副区长
    ("ft_chu_junwei", "ft_gao_feng", "superior_subordinate",
     "区长与副区长",
     "北京市丰台区人民政府", "待查至今"),

    # 初军威 ↔ 高荣军 — 区长-公安分局长
    ("ft_chu_junwei", "ft_gao_rongjun", "superior_subordinate",
     "区长与公安分局局长（安全稳定）",
     "北京市丰台区人民政府", "待查至今"),

    # 刘永杰 ↔ 高荣军 — 政法委书记-公安分局长
    ("ft_liu_yongjie", "ft_gao_rongjun", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共北京市丰台区委政法委员会", "待查至今"),

    # 廉钰辉 ↔ 刘永洪 — 纪委书记-组织部长
    ("ft_lian_yuhui", "ft_liu_yonghong", "overlap",
     "纪委与组织部在干部监督方面的协作",
     "中共北京市丰台区委员会", "待查至今"),

    # 王少峰 ↔ 徐光彬 — 前后任区委书记
    ("ft_wang_shaofeng", "ft_xu_guangbin", "predecessor_successor",
     "王少峰接替徐光彬任丰台区委书记",
     "中共北京市丰台区委员会", "2023-03"),
]


# ════════════════════════════════════════════
# DATABASE BUILDER
# ════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons(
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
    )""")

    c.execute("""CREATE TABLE organizations(
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    )""")

    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF BUILDER
# ════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "副" not in post and "副书记" not in post:
        return "255,50,50"
    if "区长" in post and "副" not in post:
        return "50,100,255"
    if "副书记" in post:
        return "255,100,100"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "常务副" in post:
        return "50,130,255"
    if "副区长" in post:
        return "100,130,255"
    if "部长" in post or "统战" in post or "组织" in post:
        return "180,100,200"
    if "政法委" in post:
        return "200,150,50"
    if "主任" in post or "人大" in post:
        return "200,255,255"
    if "政协" in post or "主席" in post:
        return "255,240,200"
    if "前" in post:
        return "150,150,150"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "公安": "200,200,255",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    post_clean = post.strip()
    if post_clean == "区委书记":
        return True
    if "区长" in post_clean and "副" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>北京市丰台区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role_or_type" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="edge_type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, eth, birth, bp, edu, party, work, post, org, src = p
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        if "副书记" in post and "区委副书记" in post:
            sz = "15.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(parent)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period = r
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF created: {GEXF_PATH}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    create_gexf()
    print("[DONE] Build complete.")
