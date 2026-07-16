#!/usr/bin/env python3
"""
重庆市涪陵区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Fuling District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Parent City: (直辖市辖区)
Targets: 区委书记 & 区长

Research Notes:
- All leadership data sourced from official fl.gov.cn government website (accessed 2026-07-16):
  - 区委领导: http://www.fl.gov.cn/zfxxgk_206/zfldxx/qw/
  - 区政府领导: http://www.fl.gov.cn/zfxxgk_206/zfldxx/qzf/
- Personal bios confirmed from individual leadership profile pages on fl.gov.cn
- Career timeline details for 黎勇 and 董奕锋 partially limited due to short official bios;
  prior roles inferred from media reports and appointment notices
- Predecessor info: 王志杰 was previous 区委书记 (2020-2024); 刘忠 was previous 区长 (until 2024)

Sources:
- http://www.fl.gov.cn — official government website (primary)
- Individual leadership profile pages on fl.gov.cn
- Baidu Baike (intended but blocked, fl.gov.cn used as primary)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "涪陵区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "涪陵区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 区委班子 (Party Committee) ══
    ("fl_li_yong", "黎勇", "男", "汉族", "1974年1月", "待查",
     "研究生/教育学博士", "中共党员", "待查",
     "区委书记", "中共重庆市涪陵区委员会",
     "fl.gov.cn_official_bio;fl.gov.cn_leader_page"),

    ("fl_dong_yifeng", "董奕锋", "男", "汉族", "1976年11月", "待查",
     "大学/公共管理硕士", "中共党员", "待查",
     "区委副书记、区长", "重庆市涪陵区人民政府",
     "fl.gov.cn_official_bio;fl.gov.cn_leader_page"),

    ("fl_zhou_jianchi", "周建池", "男", "汉族", "1975年9月", "待查",
     "研究生/公共管理硕士", "中共党员", "待查",
     "区委副书记", "中共重庆市涪陵区委员会",
     "fl.gov.cn_official_bio"),

    ("fl_yan_pei", "严培", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区人武部政委", "重庆市涪陵区人民武装部",
     "fl.gov.cn_leader_page"),

    ("fl_fang_guojun", "方国军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区纪委书记、区监委主任", "中共重庆市涪陵区纪律检查委员会",
     "fl.gov.cn_leader_page"),

    ("fl_deng_yuanfeng", "邓远峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委，涪陵高新区（涪陵综保区）党工委书记", "中共涪陵高新技术产业开发区工作委员会",
     "fl.gov.cn_leader_page"),

    ("fl_tuo_can", "庹灿", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区委统战部部长", "中共重庆市涪陵区委统战部",
     "fl.gov.cn_leader_page"),

    ("fl_xie_chenghong", "谢成洪", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区委政法委书记", "中共重庆市涪陵区委政法委员会",
     "fl.gov.cn_leader_page"),

    ("fl_feng_xinggui", "冯星贵", "男", "汉族", "1973年2月", "待查",
     "研究生/农学学士", "中共党员", "待查",
     "区委常委、区政府常务副区长", "重庆市涪陵区人民政府",
     "fl.gov.cn_official_bio"),

    ("fl_wu_hui", "吴辉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区委宣传部部长", "中共重庆市涪陵区委宣传部",
     "fl.gov.cn_leader_page"),

    ("fl_wu_hongkun", "吴洪坤", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区委组织部部长", "中共重庆市涪陵区委组织部",
     "fl.gov.cn_leader_page"),

    # ══ 区政府副区长 (Government Deputy Heads) ══
    ("fl_lu_zheng", "卢政", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、区公安局局长", "重庆市涪陵区公安局",
     "fl.gov.cn_leader_page"),

    ("fl_zheng_xiaoping", "郑小平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市涪陵区人民政府",
     "fl.gov.cn_leader_page"),

    ("fl_zhang_yu", "张宇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市涪陵区人民政府",
     "fl.gov.cn_leader_page"),

    ("fl_gao_fan", "高帆", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市涪陵区人民政府",
     "fl.gov.cn_leader_page"),

    ("fl_wang_yeping", "王业平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市涪陵区人民政府",
     "fl.gov.cn_leader_page"),

    ("fl_dai_weili", "代威力", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市涪陵区人民政府",
     "fl.gov.cn_leader_page"),

    # ══ 区政府党组成员 ══
    ("fl_yin_xing", "尹兴", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员", "重庆市涪陵区人民政府",
     "fl.gov.cn_leader_page"),

    # ══ 前任领导 ══
    ("fl_wang_zhijie", "王志杰", "男", "汉族", "1972年1月", "待查",
     "研究生/工学博士", "中共党员", "待查",
     "前任区委书记", "中共重庆市涪陵区委员会（原）",
     "media_reports"),

    ("fl_liu_zhong", "刘忠", "男", "汉族", "1968年6月", "待查",
     "大学", "中共党员", "待查",
     "前任区长", "重庆市涪陵区人民政府（原）",
     "media_reports"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("fl_party_committee", "中共重庆市涪陵区委员会", "党委", "地厅级", "中共重庆市委", "重庆市涪陵区"),
    ("fl_gov", "重庆市涪陵区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市涪陵区"),
    ("fl_discipline", "中共重庆市涪陵区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市涪陵区"),
    ("fl_organization", "中共重庆市涪陵区委组织部", "党委部门", "正处级", "涪陵区委", "重庆市涪陵区"),
    ("fl_propaganda", "中共重庆市涪陵区委宣传部", "党委部门", "正处级", "涪陵区委", "重庆市涪陵区"),
    ("fl_united_front", "中共重庆市涪陵区委统战部", "党委部门", "正处级", "涪陵区委", "重庆市涪陵区"),
    ("fl_political_legal", "中共重庆市涪陵区委政法委员会", "党委部门", "正处级", "涪陵区委", "重庆市涪陵区"),
    ("fl_military_department", "重庆市涪陵区人民武装部", "军事", "正师级", "重庆警备区", "重庆市涪陵区"),
    ("fl_high_tech_zone", "中共涪陵高新技术产业开发区工作委员会", "开发区", "正处级", "涪陵区委", "重庆市涪陵区"),
    ("fl_public_security", "重庆市涪陵区公安局", "公安", "正处级", "重庆市公安局", "重庆市涪陵区"),
    ("fl_peoples_congress", "重庆市涪陵区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市涪陵区"),
    ("fl_cppcc", "中国人民政治协商会议重庆市涪陵区委员会", "政协", "地厅级", "重庆市政协", "重庆市涪陵区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 黎勇 — 区委书记 ═══
    ("fl_li_yong", "fl_party_committee", "区委书记", "2024", "至今", "正厅级",
     "主持区委全面工作，联系区人大、区政协。十四届全国政协委员、六届市委委员"),
    # 黎勇 previous roles (known from media)
    ("fl_li_yong", "fl_party_committee", "履历缺口（媒体有限）", "待查", "2024", "未知",
     "曾任重庆市人社局局长等职，具体任职时间线待查"),

    # ═══ 董奕锋 — 区长 ═══
    ("fl_dong_yifeng", "fl_gov", "区长", "2024", "至今", "正厅级",
     "主持区政府全面工作；负责审计工作。主管区审计局。联系人大、政协、民主党派和工商联工作"),
    ("fl_dong_yifeng", "fl_party_committee", "区委副书记", "2024", "至今", "正厅级", "兼任"),
    ("fl_dong_yifeng", "fl_party_committee", "履历缺口", "待查", "2024", "未知",
     "曾任重庆市城口县委书记等职，具体任职时间线待查"),

    # ═══ 周建池 — 区委副书记 ═══
    ("fl_zhou_jianchi", "fl_party_committee", "区委副书记", "2026", "至今", "正厅级", "专职副书记"),

    # ═══ 严培 — 人武部政委 ═══
    ("fl_yan_pei", "fl_military_department", "区委常委、区人武部政委", "待查", "至今", "正师级", ""),

    # ═══ 方国军 — 纪委书记 ═══
    ("fl_fang_guojun", "fl_discipline", "区委常委、区纪委书记、区监委主任", "待查", "至今", "副厅级", ""),

    # ═══ 邓远峰 — 高新区书记 ═══
    ("fl_deng_yuanfeng", "fl_high_tech_zone", "区委常委、涪陵高新区（涪陵综保区）党工委书记", "待查", "至今", "副厅级", ""),

    # ═══ 庹灿 — 统战部长 ═══
    ("fl_tuo_can", "fl_united_front", "区委常委、统战部部长", "2022-01", "至今", "副厅级", ""),

    # ═══ 谢成洪 — 政法委书记 ═══
    ("fl_xie_chenghong", "fl_political_legal", "区委常委、政法委书记", "2022-01", "至今", "副厅级", ""),

    # ═══ 冯星贵 — 常务副区长 ═══
    ("fl_feng_xinggui", "fl_gov", "区委常委、常务副区长", "2024-11", "至今", "副厅级",
     "区政府党组副书记。负责区政府常务工作；分管发展改革、财税、金融等"),

    # ═══ 吴辉 — 宣传部长 ═══
    ("fl_wu_hui", "fl_propaganda", "区委常委、宣传部部长", "2024-03", "至今", "副厅级", ""),

    # ═══ 吴洪坤 — 组织部长 ═══
    ("fl_wu_hongkun", "fl_organization", "区委常委、组织部部长", "2026-03", "至今", "副厅级", ""),

    # ═══ 卢政 — 副区长/公安局长 ═══
    ("fl_lu_zheng", "fl_gov", "副区长", "待查", "至今", "副厅级", "兼任区公安局局长、督察长"),
    ("fl_lu_zheng", "fl_public_security", "区公安局局长", "待查", "至今", "副厅级", "区委政法委副书记(兼)"),

    # ═══ 郑小平 — 副区长 ═══
    ("fl_zheng_xiaoping", "fl_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 张宇 — 副区长 ═══
    ("fl_zhang_yu", "fl_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 高帆 — 副区长 ═══
    ("fl_gao_fan", "fl_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 王业平 — 副区长 ═══
    ("fl_wang_yeping", "fl_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 代威力 — 副区长 ═══
    ("fl_dai_weili", "fl_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 尹兴 — 区政府党组成员 ═══
    ("fl_yin_xing", "fl_gov", "区政府党组成员", "待查", "至今", "副厅级", ""),

    # ═══ 前任领导 ═══
    ("fl_wang_zhijie", "fl_party_committee", "前任区委书记", "2021", "2024", "正厅级", "调任他职"),
    ("fl_liu_zhong", "fl_gov", "前任区长", "2020", "2024", "正厅级", "调任他职"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 黎勇 ↔ 董奕锋 — 党政正职搭档
    ("fl_li_yong", "fl_dong_yifeng", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共重庆市涪陵区委员会", "2024至今"),

    # 黎勇 ↔ 周建池 — 书记-副书记
    ("fl_li_yong", "fl_zhou_jianchi", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市涪陵区委员会", "2026至今"),

    # 黎勇 ↔ 方国军 — 书记-纪委书记
    ("fl_li_yong", "fl_fang_guojun", "superior_subordinate",
     "区委书记与纪委书记（全面从严治党）",
     "中共重庆市涪陵区委员会", "待查至今"),

    # 黎勇 ↔ 冯星贵 — 书记-常务副区长
    ("fl_li_yong", "fl_feng_xinggui", "superior_subordinate",
     "区委书记与常务副区长",
     "中共重庆市涪陵区委员会", "2024至今"),

    # 黎勇 ↔ 吴洪坤 — 书记-组织部长
    ("fl_li_yong", "fl_wu_hongkun", "superior_subordinate",
     "区委书记与组织部部长（干部选拔任用）",
     "中共重庆市涪陵区委员会", "2026至今"),

    # 董奕锋 ↔ 冯星贵 — 区长-常务副区长
    ("fl_dong_yifeng", "fl_feng_xinggui", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市涪陵区人民政府", "2024至今"),

    # 董奕锋 ↔ 卢政 — 区长-公安局长
    ("fl_dong_yifeng", "fl_lu_zheng", "superior_subordinate",
     "区长与公安局局长（安全稳定工作）",
     "重庆市涪陵区人民政府", "待查至今"),

    # 黎勇 — 前任书记
    ("fl_li_yong", "fl_wang_zhijie", "predecessor_successor",
     "黎勇接替王志杰任涪陵区委书记",
     "中共重庆市涪陵区委员会", "2024"),

    # 董奕锋 — 前任区长
    ("fl_dong_yifeng", "fl_liu_zhong", "predecessor_successor",
     "董奕锋接替刘忠任涪陵区区长",
     "重庆市涪陵区人民政府", "2024"),

    # 方国军 ↔ 吴洪坤 — 纪委-组织部协作
    ("fl_fang_guojun", "fl_wu_hongkun", "overlap",
     "纪委书记与组织部长的干部监督协作",
     "中共重庆市涪陵区委员会", "待查至今"),

    # 谢成洪 ↔ 卢政 — 政法委-公安协作
    ("fl_xie_chenghong", "fl_lu_zheng", "overlap",
     "政法委书记与公安局局长的政法系统协作",
     "中共重庆市涪陵区委政法委员会", "待查至今"),

    # 邓远峰 ↔ 黎勇  — 高新区-区委
    ("fl_deng_yuanfeng", "fl_li_yong", "superior_subordinate",
     "高新区党工委书记与区委书记",
     "中共重庆市涪陵区委员会", "待查至今"),

    # 冯星贵 ↔ 郑小平 — 常务副区长-副区长
    ("fl_feng_xinggui", "fl_zheng_xiaoping", "overlap",
     "常务副区长与副区长（政府工作协作）",
     "重庆市涪陵区人民政府", "待查至今"),

    # 冯星贵 ↔ 张宇 — 常务副区长-副区长
    ("fl_feng_xinggui", "fl_zhang_yu", "overlap",
     "常务副区长与副区长（政府工作协作）",
     "重庆市涪陵区人民政府", "待查至今"),

    # 冯星贵 ↔ 高帆 — 常务副区长-副区长
    ("fl_feng_xinggui", "fl_gao_fan", "overlap",
     "常务副区长与副区长（政府工作协作）",
     "重庆市涪陵区人民政府", "待查至今"),

    # 冯星贵 ↔ 王业平 — 常务副区长-副区长
    ("fl_feng_xinggui", "fl_wang_yeping", "overlap",
     "常务副区长与副区长（政府工作协作）",
     "重庆市涪陵区人民政府", "待查至今"),

    # 冯星贵 ↔ 代威力 — 常务副区长-副区长
    ("fl_feng_xinggui", "fl_dai_weili", "overlap",
     "常务副区长与副区长（政府工作协作）",
     "重庆市涪陵区人民政府", "待查至今"),
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
    if "书记" in post and "副" not in post and "副书记" not in post and "书记" == post[-2:]:
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
    if "人武部" in post:
        return "150,200,100"
    if "高新区" in post:
        return "100,200,100"
    if "党组" in post:
        return "100,150,200"
    if "前任" in post or "原" in post:
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
        "军事": "200,255,200",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    if post == "区委书记":
        return True
    if "区长" in post and "副" not in post:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>重庆市涪陵区领导班子工作关系网络</description>')
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
        if "前任" in post or "原" in post:
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
