#!/usr/bin/env python3
"""
重庆市长寿区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Changshou District leadership.

Level: 市辖区(直辖市) — 地厅级
Province: 重庆市
Targets: 区委书记 & 区长

Research Notes:
- Current leaders confirmed from changshou.gov.cn official website (2026-06/07 articles)
- 江夏 as 区委书记 appointed Dec 2024, previously head of Chongqing Water Resources Bureau
- 李茂涛 as 区长 appointed Oct 2025, previously Yunyang County Mayor
- Full deputy roster from government leadership page (ldxx_3/)
- Party committee members (组织、宣传、统战、政法等) partially identified from news reports
- Web research constrained: Baidu Baike 403, some individual bio pages JS-rendered

Sources:
- cqcs.gov.cn official website (primary - confirmed)
- Media reports via news search
- Chongqing Municipal Organization Department appointment notices

Open Gaps:
- 江夏: full timeline pre-2010 (born 1970 北碚, teacher then DADukou district)
- 李茂涛: full education background (born 1978 四川射洪, 工学硕士)
- Most deputy birth years and full career histories
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "database", "长寿区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "data", "graph", "长寿区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # ── 区委班子 ──
    ("cs_jiang_xia", "江夏", "男", "汉族", "1970年9月", "重庆北碚",
     "市委党校研究生/高级管理人员工商管理硕士", "1996年12月", "1990年7月",
     "区委书记、长寿经开区党工委书记", "中共重庆市长寿区委员会",
     "cqcs.gov.cn;中国经济网"),
    ("cs_li_maotao", "李茂涛", "男", "汉族", "1978年3月", "四川射洪",
     "大学/工学硕士", "1999年4月", "2000年7月",
     "区委副书记、区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn;中国经济网;澎湃新闻"),
    ("cs_shi_mengming", "师明萌", "女", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议重庆市长寿区委员会",
     "cqcs.gov.cn"),
    ("cs_ran_hong", "冉洪", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "经开区党工委副书记、管委会主任", "重庆市长寿经济技术开发区",
     "cqcs.gov.cn"),

    # ── 政府领导班子(从官网确认) ──
    ("cs_jing_kaiyuan", "靖开媛", "女", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_shi_shaolin", "石少林", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_liu_chaoyu", "刘朝煜", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_jiang_famao", "江发茂", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_tu_qing", "涂庆", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_jiang_faping", "蒋发平", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_zou_xiangming", "邹翔名", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_li_jia", "李佳", "女", "汉", "待查", "待查",
     "待查", "非党", "待查",
     "副区长", "重庆市长寿区人民政府",
     "cqcs.gov.cn"),
    ("cs_deng_jun", "邓军", "男", "汉", "1977年8月", "待查",
     "研究生", "中共党员", "待查",
     "区政府党组成员、办公室主任", "重庆市长寿区人民政府办公室",
     "cqcs.gov.cn"),

    # ── 党口常委(部分确认) ──
    ("cs_li_yuanyuan", "李源源", "女", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共重庆市长寿区纪律检查委员会",
     "第三方媒体"),
    ("cs_hu_hongbing", "胡红兵", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市长寿区委统战部",
     "第三方媒体"),
    ("cs_zhang_mingwan", "张明万", "男", "汉", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市长寿区委政法委员会",
     "第三方媒体"),

    # ── 前任 ──
    ("cs_liu_xiaoqiang", "刘小强", "男", "汉族", "1971年5月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "前任区委书记(2021-2024)", "中共重庆市长寿区委员会(前)",
     "中国经济网"),
    ("cs_dai_ming", "戴明", "男", "汉族", "1969年10月", "待查",
     "待查", "中共党员", "待查",
     "前任区长(2020-2025)", "重庆市长寿区人民政府(前)",
     "中国经济网;搜狐新闻"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("cs_party_committee", "中共重庆市长寿区委员会", "党委", "地厅级", "中共重庆市委", "重庆市长寿区"),
    ("cs_gov", "重庆市长寿区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市长寿区"),
    ("cs_gov_office", "重庆市长寿区人民政府办公室", "政府", "正处级", "长寿区政府", "重庆市长寿区"),
    ("cs_etz", "重庆市长寿经济技术开发区", "开发区", "地厅级", "重庆市人民政府", "重庆市长寿区"),
    ("cs_discipline", "中共重庆市长寿区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市长寿区"),
    ("cs_united_front", "中共重庆市长寿区委统战部", "党委部门", "正处级", "长寿区委", "重庆市长寿区"),
    ("cs_political_legal", "中共重庆市长寿区委政法委员会", "党委部门", "正处级", "长寿区委", "重庆市长寿区"),
    ("cs_cppcc", "中国人民政治协商会议重庆市长寿区委员会", "政协", "地厅级", "重庆市政协", "重庆市长寿区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note
    # ═══ 江夏 — 区委书记 ═══
    ("cs_jiang_xia", "cs_party_committee", "区委书记、长寿经开区党工委书记", "2024-12", "至今", "正厅级", "主持区委全面工作，兼任经开区党工委书记"),
    ("cs_jiang_xia", "cs_etz", "长寿经开区党工委书记(兼)", "2024-12", "至今", "正厅级", ""),
    ("cs_jiang_xia", "cs_gov", "重庆市水利局党组书记、局长", "2023-03", "2024-12", "正厅级", "调任长寿前"),
    ("cs_jiang_xia", "cs_gov", "忠县县委书记", "2020", "2023-03", "正厅级", "主政一方"),
    ("cs_jiang_xia", "cs_gov", "忠县县委副书记、县长", "2016", "2020", "副厅级", ""),
    ("cs_jiang_xia", "cs_gov", "江津区委常委、双福新区党委书记", "~2013", "2016", "副厅级", "开发区分管"),
    ("cs_jiang_xia", "cs_gov", "大渡口区委组织部、区委办", "~2000s", "~2013", "正处级", "早期"),
    ("cs_jiang_xia", "cs_gov", "大渡口区团委副书记、书记", "~1990s", "~2000s", "处级", ""),
    ("cs_jiang_xia", "cs_gov", "重钢实验校、重钢子弟小学教师", "1990-07", "~1990s", "", "教职起步"),
    ("cs_jiang_xia", "cs_gov", "履历缺口(需补充)", "unknown", "unknown", "unknown", "1990s年代部分细节待核实"),

    # ═══ 李茂涛 — 区长 ═══
    ("cs_li_maotao", "cs_gov", "区长", "2025-10", "至今", "正厅级", "主持区政府全面工作"),
    ("cs_li_maotao", "cs_party_committee", "区委副书记", "2025-10", "至今", "正厅级", "兼任"),
    ("cs_li_maotao", "cs_gov", "云阳县委副书记、县长", "2021-09", "2025-10", "副厅级", "云阳县主政约4年"),
    ("cs_li_maotao", "cs_gov", "重庆市发改委党组成员、副主任", "2020-06", "2021-09", "副厅级", "兼市粮食局副局长"),
    ("cs_li_maotao", "cs_gov", "重庆市发改委固定资产投资处处长", "~约2018", "2020-06", "正处级", ""),
    ("cs_li_maotao", "cs_gov", "重庆市发改委固定资产投资处副处长", "~约2015", "~约2018", "副处级", ""),
    ("cs_li_maotao", "cs_gov", "重庆市发改委交通处副处长", "~2010", "~约2015", "副处级", "市发改委早期生涯"),
    ("cs_li_maotao", "cs_gov", "重庆市发改委工作", "2000-07", "~2010", "干部→副处", "教育背景不详"),

    # ═══ 靖开媛 — 常务副区长 ═══
    ("cs_jing_kaiyuan", "cs_gov", "区委常委、常务副区长", "待查", "至今", "副厅级", ""),
    ("cs_jing_kaiyuan", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", "公开资料待补充"),

    # ═══ 石少林 — 常委副区长 ═══
    ("cs_shi_shaolin", "cs_gov", "区委常委、副区长", "待查", "至今", "副厅级", ""),
    ("cs_shi_shaolin", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", "公开资料待补充"),

    # ═══ 刘朝煜 — 副区长 ═══
    ("cs_liu_chaoyu", "cs_gov", "副区长", "待查", "至今", "副厅级", "分管水利、城市管理"),
    ("cs_liu_chaoyu", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", "公开资料待补充"),

    # ═══ 江发茂 — 副区长 ═══
    ("cs_jiang_famao", "cs_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("cs_jiang_famao", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 涂庆 — 副区长 ═══
    ("cs_tu_qing", "cs_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("cs_tu_qing", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 蒋发平 — 副区长 ═══
    ("cs_jiang_faping", "cs_gov", "副区长", "待查", "至今", "副厅级", "经济/产业分管"),
    ("cs_jiang_faping", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 邹翔名 — 副区长 ═══
    ("cs_zou_xiangming", "cs_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("cs_zou_xiangming", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 李佳 — 副区长(非党) ═══
    ("cs_li_jia", "cs_gov", "副区长", "待查", "至今", "副厅级", "非中共党员"),
    ("cs_li_jia", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 邓军 — 办公室主任 ═══
    ("cs_deng_jun", "cs_gov_office", "区政府党组成员、办公室主任、外事办主任", "待查", "至今", "正处级", ""),
    ("cs_deng_jun", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 师明萌 — 政协主席 ═══
    ("cs_shi_mengming", "cs_cppcc", "区政协主席", "待查", "至今", "正厅级", ""),
    ("cs_shi_mengming", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 冉洪 — 经开区管委会主任 ═══
    ("cs_ran_hong", "cs_etz", "经开区党工委副书记、管委会主任", "待查", "至今", "正厅级", ""),
    ("cs_ran_hong", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 李源源 — 纪委书记 ═══
    ("cs_li_yuanyuan", "cs_discipline", "区委常委、纪委书记、监委主任", "待查", "至今", "副厅级", ""),
    ("cs_li_yuanyuan", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 胡红兵 — 统战部长 ═══
    ("cs_hu_hongbing", "cs_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级", ""),
    ("cs_hu_hongbing", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 张明万 — 政法委书记 ═══
    ("cs_zhang_mingwan", "cs_political_legal", "区委常委、政法委书记", "待查", "至今", "副厅级", ""),
    ("cs_zhang_mingwan", "cs_gov", "履历缺口", "unknown", "unknown", "unknown", ""),

    # ═══ 刘小强 — 前任书记 ═══
    ("cs_liu_xiaoqiang", "cs_party_committee", "区委书记(前)", "2021", "2024-12", "正厅级", "被江夏接替，去向待查"),
    ("cs_liu_xiaoqiang", "cs_gov", "重庆市九龙坡区委副书记、区长", "~2017", "2021", "正厅级", "调任长寿前"),

    # ═══ 戴明 — 前任区长 ═══
    ("cs_dai_ming", "cs_gov", "区长(前)", "2020", "2025-10", "正厅级", "被李茂涛接替"),
    ("cs_dai_ming", "cs_gov", "万盛经开区党工委书记", "2025-10", "至今", "正厅级", "去向"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 江夏 ↔ 李茂涛 — 党政正职搭档
    ("cs_jiang_xia", "cs_li_maotao", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共重庆市长寿区委员会/长寿区人民政府", "2025-10至今"),

    # 江夏 ↔ 靖开媛 — 书记-常务副区长
    ("cs_jiang_xia", "cs_jing_kaiyuan", "superior_subordinate",
     "区委书记与常务副区长",
     "中共重庆市长寿区委员会", "2024-12至今"),

    # 江夏 ↔ 石少林 — 书记-常委副区长
    ("cs_jiang_xia", "cs_shi_shaolin", "superior_subordinate",
     "区委书记与区委常委副区长",
     "中共重庆市长寿区委员会", "2024-12至今"),

    # 江夏 ↔ 蒋发平 — 书记-副区长
    ("cs_jiang_xia", "cs_jiang_faping", "superior_subordinate",
     "区委书记与分管经济的副区长",
     "重庆市长寿区人民政府", "2024-12至今"),

    # 江夏 ↔ 李源源 — 书记-纪委书记
    ("cs_jiang_xia", "cs_li_yuanyuan", "superior_subordinate",
     "区委书记与纪委书记",
     "中共重庆市长寿区委员会", "2024-12至今"),

    # 江夏 ↔ 冉洪 — 书记-经开区主任
    ("cs_jiang_xia", "cs_ran_hong", "superior_subordinate",
     "区委书记(兼经开区党工委书记)与经开区管委会主任",
     "长寿经济技术开发区", "2024-12至今"),

    # 李茂涛 ↔ 靖开媛 — 区长-常务副区长
    ("cs_li_maotao", "cs_jing_kaiyuan", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市长寿区人民政府", "2025-10至今"),

    # 李茂涛 ↔ 石少林 — 区长-常委副区长
    ("cs_li_maotao", "cs_shi_shaolin", "superior_subordinate",
     "区长与常委副区长",
     "重庆市长寿区人民政府", "2025-10至今"),

    # 李茂涛 ↔ 刘朝煜 — 区长-副区长
    ("cs_li_maotao", "cs_liu_chaoyu", "superior_subordinate",
     "区长与分管水利副区长",
     "重庆市长寿区人民政府", "2025-10至今"),

    # 李茂涛 ↔ 蒋发平 — 区长-副区长
    ("cs_li_maotao", "cs_jiang_faping", "superior_subordinate",
     "区长与分管产业副区长（经常同场调研）",
     "重庆市长寿区人民政府", "2025-10至今"),

    # 李茂涛 ↔ 邹翔名 — 区长-副区长
    ("cs_li_maotao", "cs_zou_xiangming", "superior_subordinate",
     "区长与副区长（2026-07-15同场调研政协提案）",
     "重庆市长寿区人民政府", "2025-10至今"),

    # 靖开媛 ↔ 蒋发平 — 常务副区长-副区长
    ("cs_jing_kaiyuan", "cs_jiang_faping", "overlap",
     "常务副区长与副区长的政府内部协作",
     "重庆市长寿区人民政府", "至今"),

    # 江夏 ↔ 刘小强 — 前后任书记
    ("cs_jiang_xia", "cs_liu_xiaoqiang", "predecessor_successor",
     "江夏2024年12月接替刘小强任长寿区委书记",
     "中共重庆市长寿区委员会", "2024-12"),

    # 李茂涛 ↔ 戴明 — 前后任区长
    ("cs_li_maotao", "cs_dai_ming", "predecessor_successor",
     "李茂涛2025年10月接替戴明任长寿区长",
     "重庆市长寿区人民政府", "2025-10"),

    # 江夏 ↔ 李茂涛 — 发改委系关联(间接)
    ("cs_li_maotao", "cs_dai_ming", "same_system",
     "李茂涛与戴明均出身重庆市发改委系统，可能互有交集",
     "重庆市发展和改革委员会", "~2010s"),
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
    if "书记" in post and "副" not in post and "副书记" not in post and "纪委书记" not in post:
        return "255,50,50"
    if "区长" in post and "副" not in post and "副书记" not in post:
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
    if "经开区" in post:
        return "200,255,200"
    if "前" in post:
        return "150,150,150"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    post_clean = post.strip()
    if post_clean == "区委书记":
        return True
    if "区长" in post_clean and "副" not in post_clean and "副书记" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>重庆市长寿区领导班子工作关系网络</description>')
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
        if "副书记" in post:
            sz = "15.0"
        if "前" in post:
            sz = "10.0"
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
