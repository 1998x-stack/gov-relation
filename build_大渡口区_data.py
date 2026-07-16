#!/usr/bin/env python3
"""
重庆市大渡口区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Dadukou District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Parent City: (直辖市辖区)
Targets: 区委书记 & 区长

Research Notes:
- Current 区委书记: 张果 (appointed ~Dec 2024, previously 永川区长/重庆市科技局局长)
- Current 区长: 张涛 (appointed April 2025 as 区委副书记、区政府党组书记, later 区长)
- All government deputy leader bios from official ddk.gov.cn leadership pages (2026-07-16)
- 张果's full bio not available on gov website (party secretary bio not published on gov site); 
  partial info from media reports
- Previous 区委书记 余长明 was investigated Sept 2024

Sources:
- https://www.ddk.gov.cn — official government website (primary)
- 张涛 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/zhangtao/
- 刘扬 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/liuyang/
- 夏小平 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/xiaxiaoping/
- 刘理国 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/liuliguo/
- 李佳敏 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/lijiamin/
- 伍平伟 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/wupingwei/
- 王希辉 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/wangxihui/
- 曹华 official bio: ddk.gov.cn/zwgk_271/zfxxgk/fdzdgknr/jgzn/fzrxx/caohua/
- Media reports: 网易, 澎湃新闻, 中国经济网 for appointment history
- Sogou search for 张果 background
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "大渡口区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "大渡口区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 区委班子 (Party Committee) ══
    ("ddk_zhang_guo", "张果", "男", "汉族", "1971年7月", "四川省万源市",
     "研究生/法学博士（西南大学）", "1993年11月", "1994年7月",
     "区委书记", "中共重庆市大渡口区委员会",
     "media_reports;sogou_search;163.com"),

    ("ddk_zhang_tao", "张涛", "男", "汉族", "1975年2月", "待查",
     "研究生/理学博士", "中共党员", "待查",
     "区委副书记、区长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    # ══ 区委常委/副区长 ══
    ("ddk_liu_yang", "刘扬", "男", "汉族", "1973年12月", "待查",
     "农业推广硕士", "中共党员", "待查",
     "区委常委、副区长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    # ══ 副区长 ══
    ("ddk_xia_xiaoping", "夏小平", "男", "汉族", "1971年1月", "待查",
     "研究生学历", "中共党员", "待查",
     "副区长、区公安分局局长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    ("ddk_liu_liguo", "刘理国", "男", "汉族", "1977年8月", "待查",
     "大学本科", "中共党员", "待查",
     "副区长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    ("ddk_wang_xihui", "王希辉", "男", "土家族", "1980年1月", "待查",
     "研究生/法学硕士/历史学博士/教授", "九三学社", "待查",
     "副区长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    ("ddk_li_jiamin", "李佳敏", "女", "汉族", "1984年4月", "待查",
     "理学硕士", "中共党员", "待查",
     "副区长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    ("ddk_wu_pingwei", "伍平伟", "男", "汉族", "1977年8月", "待查",
     "教育硕士", "中共党员", "待查",
     "副区长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    ("ddk_cao_hua", "曹华", "男", "汉族", "1981年5月", "待查",
     "经济学硕士", "中共党员", "待查",
     "副区长", "重庆市大渡口区人民政府",
     "ddk.gov.cn_official"),

    # ══ 前任领导 ══
    ("ddk_yu_changming", "余长明", "男", "汉族", "1965年3月", "四川峨眉山",
     "西南农业大学研究生/农学博士", "1985年4月", "1984年7月",
     "前任区委书记（被查）", "中共重庆市大渡口区委员会（原）",
     "baike_baidu;media_reports;163.com"),

    ("ddk_wang_jun", "王俊", "男", "汉族", "1966年9月", "重庆涪陵",
     "市委党校研究生", "1990年1月", "1985年10月",
     "前任区委书记（更早）", "中共重庆市大渡口区委员会（原）",
     "baike_baidu;media_reports;sogou_search"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("ddk_party_committee", "中共重庆市大渡口区委员会", "党委", "地厅级", "中共重庆市委", "重庆市大渡口区"),
    ("ddk_gov", "重庆市大渡口区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市大渡口区"),
    ("ddk_discipline", "中共重庆市大渡口区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市大渡口区"),
    ("ddk_organization", "中共重庆市大渡口区委组织部", "党委部门", "正处级", "大渡口区委", "重庆市大渡口区"),
    ("ddk_propaganda", "中共重庆市大渡口区委宣传部", "党委部门", "正处级", "大渡口区委", "重庆市大渡口区"),
    ("ddk_united_front", "中共重庆市大渡口区委统战部", "党委部门", "正处级", "大渡口区委", "重庆市大渡口区"),
    ("ddk_political_legal", "中共重庆市大渡口区委政法委员会", "党委部门", "正处级", "大渡口区委", "重庆市大渡口区"),
    ("ddk_military_department", "重庆市大渡口区人民武装部", "军事", "正师级", "重庆警备区", "重庆市大渡口区"),
    ("ddk_public_security", "重庆市公安局大渡口区分局", "公安", "正处级", "重庆市公安局", "重庆市大渡口区"),
    ("ddk_procuratorate", "重庆市大渡口区人民检察院", "检察院", "正处级", "重庆市检察院", "重庆市大渡口区"),
    ("ddk_court", "重庆市大渡口区人民法院", "法院", "正处级", "重庆市高院", "重庆市大渡口区"),
    ("ddk_peoples_congress", "重庆市大渡口区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市大渡口区"),
    ("ddk_cppcc", "中国人民政治协商会议重庆市大渡口区委员会", "政协", "地厅级", "重庆市政协", "重庆市大渡口区"),
    ("ddk_finance_bureau", "重庆市大渡口区财政局", "政府", "正处级", "大渡口区政府", "重庆市大渡口区"),
    ("ddk_audit_bureau", "重庆市大渡口区审计局", "政府", "正处级", "大渡口区政府", "重庆市大渡口区"),

    # External orgs for career timeline
    ("ddk_yongchuan_gov", "重庆市永川区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市永川区"),
    ("ddk_chongqing_science", "重庆市科学技术局", "政府", "地厅级", "重庆市人民政府", "重庆市"),
    ("ddk_chongqing_reform", "中共重庆市委全面深化改革委员会办公室", "党委部门", "地厅级", "中共重庆市委", "重庆市"),
    ("ddk_qianjiang_party", "中共重庆市黔江区委", "党委", "地厅级", "中共重庆市委", "重庆市黔江区"),
    ("ddk_nanan_party", "中共重庆市南岸区委", "党委", "地厅级", "中共重庆市委", "重庆市南岸区"),
    ("ddk_nanan_gov", "重庆市南岸区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市南岸区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 张果 — 区委书记 ═══
    ("ddk_zhang_guo", "ddk_party_committee", "区委书记", "2024-12", "至今", "正厅级",
     "主持区委全面工作。2024年12月任大渡口区委书记（接替被查的余长明）。"),
    ("ddk_zhang_guo", "ddk_yongchuan_gov", "永川区委副书记、区长", "2021", "2024-12", "正厅级",
     "永川区长，与永川区委书记张智奎搭档。"),
    ("ddk_zhang_guo", "ddk_chongqing_science", "重庆市科技局党组书记、局长", "2018", "2021", "正厅级",
     "2018年任市科技局局长。"),
    ("ddk_zhang_guo", "ddk_chongqing_reform", "重庆市委改革办副主任", "2017?", "2018", "副厅级",
     "市委改革办（法治办）副主任。"),
    ("ddk_zhang_guo", "ddk_chongqing_reform", "重庆市委改革办（法治办）处长", "2015?", "2017?", "正处级",
     "任市委改革办处长，时间待核实。"),
    ("ddk_zhang_guo", "ddk_nanan_party", "南岸区委常委、副区长", "2011?", "2015?", "副厅级",
     "南岸区任职经历，具体时间线待核实。"),
    ("ddk_zhang_guo", "ddk_nanan_gov", "南岸区副区长", "2009?", "2011?", "副厅级",
     "南岸区副区长。"),
    ("ddk_zhang_guo", "ddk_nanan_gov", "南岸区长助理", "2007?", "2009?", "正处级",
     "南岸区长助理。"),

    # ═══ 张涛 — 区长 ═══
    ("ddk_zhang_tao", "ddk_gov", "区长", "2025-04", "至今", "正厅级",
     "主持区政府全面工作；负责审计工作。主管区审计局。联系人大、政协、民主党派和工商联工作。"),
    ("ddk_zhang_tao", "ddk_party_committee", "区委副书记", "2025-04", "至今", "正厅级", "兼任区委副书记"),
    ("ddk_zhang_tao", "ddk_gov", "区政府党组书记", "2025-04", "至今", "正厅级",
     "2025年4月30日以大渡口区委副书记、区政府党组书记身份公开亮相"),

    # ═══ 刘扬 — 区委常委、副区长 ═══
    ("ddk_liu_yang", "ddk_gov", "区委常委、副区长", "待查", "至今", "副厅级",
     "负责科技、知识产权、工业和信息化、国有资产运营、高新区建桥园。分管区科技局、区经济信息委等。"),
    ("ddk_liu_yang", "ddk_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 夏小平 — 副区长、公安分局局长 ═══
    ("ddk_xia_xiaoping", "ddk_gov", "副区长", "待查", "至今", "副厅级",
     "负责公安、司法行政、信访、保密、退役军人事务工作。"),
    ("ddk_xia_xiaoping", "ddk_public_security", "区公安分局党委书记、局长、督察长", "待查", "至今", "正处级", "兼任"),

    # ═══ 刘理国 — 副区长 ═══
    ("ddk_liu_liguo", "ddk_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 王希辉 — 副区长 ═══
    ("ddk_wang_xihui", "ddk_gov", "副区长", "待查", "至今", "副厅级",
     "九三学社成员，教授职称。"),

    # ═══ 李佳敏 — 副区长 ═══
    ("ddk_li_jiamin", "ddk_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 伍平伟 — 副区长 ═══
    ("ddk_wu_pingwei", "ddk_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 曹华 — 副区长 ═══
    ("ddk_cao_hua", "ddk_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 余长明 — 前任区委书记 ═══
    ("ddk_yu_changming", "ddk_party_committee", "前任区委书记", "2021-08", "2024-09", "正厅级",
     "2021年8月-2024年9月任区委书记。2024年9月被查。"),
    ("ddk_yu_changming", "ddk_qianjiang_party", "黔江区委书记", "2015-07", "2021-08", "正厅级",
     "2015年7月—2021年8月任黔江区委书记。"),
    ("ddk_yu_changming", "ddk_chongqing_reform", "重庆市委副秘书长、办公厅主任", "2012-10", "2015-07", "正厅级",
     "明确为正厅局长级。兼任市委办公厅主任。"),
    ("ddk_yu_changming", "ddk_chongqing_reform", "重庆市委副秘书长、督查室主任", "2009-05", "2012-10", "正厅级",
     "明确为正厅局长级。"),
    ("ddk_yu_changming", "ddk_chongqing_reform", "重庆市委办公厅副主任", "2000s", "2009-05", "副厅级",
     "市委办公厅任职期间逐步晋升。"),

    # ═══ 王俊 — 更早前任区委书记 ═══
    ("ddk_wang_jun", "ddk_party_committee", "前任区委书记（更早）", "2018", "2021-08", "正厅级",
     "2018年-2021年8月任大渡口区委书记。"),
    ("ddk_wang_jun", "ddk_nanan_gov", "南岸区委副书记、区长", "2016", "2018", "正厅级",
     "南岸区长，后调任大渡口区委书记。"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 张果 ↔ 张涛 — 党政正职搭档 ═══
    ("ddk_zhang_guo", "ddk_zhang_tao", "superior_subordinate",
     "区委书记与区长党政正职搭档关系",
     "中共重庆市大渡口区委员会;重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张果 ↔ 刘扬 — 书记-区委常委 ═══
    ("ddk_zhang_guo", "ddk_liu_yang", "superior_subordinate",
     "区委书记与区委常委（副区长）",
     "中共重庆市大渡口区委员会", "2024-12至今"),

    # ═══ 张果 — 前任书记（余长明） ═══
    ("ddk_zhang_guo", "ddk_yu_changming", "predecessor_successor",
     "张果接替被查的余长明任大渡口区委书记",
     "中共重庆市大渡口区委员会", "2024-12"),

    # ═══ 余长明 — 前任书记（王俊） ═══
    ("ddk_yu_changming", "ddk_wang_jun", "predecessor_successor",
     "余长明接替王俊任大渡口区委书记",
     "中共重庆市大渡口区委员会", "2021-08"),

    # ═══ 张涛 ↔ 刘扬 — 区长-常委副区长 ═══
    ("ddk_zhang_tao", "ddk_liu_yang", "superior_subordinate",
     "区长与区委常委、副区长（区政府分管领导）",
     "重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张涛 ↔ 夏小平 — 区长-副区长 ═══
    ("ddk_zhang_tao", "ddk_xia_xiaoping", "superior_subordinate",
     "区长与副区长（公安分局局长）",
     "重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张涛 ↔ 刘理国 — 区长-副区长 ═══
    ("ddk_zhang_tao", "ddk_liu_liguo", "superior_subordinate",
     "区长与副区长",
     "重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张涛 ↔ 王希辉 — 区长-副区长 ═══
    ("ddk_zhang_tao", "ddk_wang_xihui", "superior_subordinate",
     "区长与副区长",
     "重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张涛 ↔ 李佳敏 — 区长-副区长 ═══
    ("ddk_zhang_tao", "ddk_li_jiamin", "superior_subordinate",
     "区长与副区长",
     "重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张涛 ↔ 伍平伟 — 区长-副区长 ═══
    ("ddk_zhang_tao", "ddk_wu_pingwei", "superior_subordinate",
     "区长与副区长",
     "重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张涛 ↔ 曹华 — 区长-副区长 ═══
    ("ddk_zhang_tao", "ddk_cao_hua", "superior_subordinate",
     "区长与副区长",
     "重庆市大渡口区人民政府", "2025-04至今"),

    # ═══ 张果 ↔ 余长明 — 相同机构不同时期 ═══
    ("ddk_zhang_guo", "ddk_yu_changming", "overlap",
     "先后任大渡口区委书记（张果接替被查的余长明）",
     "中共重庆市大渡口区委员会", "2021-2025"),
]

# ════════════════════════════════════════════
# SQLITE SETUP
# ════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
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
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT DEFAULT 'medium',
            confidence TEXT DEFAULT 'plausible',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?,?,?,?,?,?,'medium','plausible')", r)

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
        "政法": "200,200,255",
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
    lines.append('    <description>重庆市大渡口区领导班子工作关系网络</description>')
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
        pa, pb, rtype, context, overlap_org, overlap_period = r[:6]
        strength = r[6] if len(r) > 6 else "medium"
        w = "2.0" if strength == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
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
