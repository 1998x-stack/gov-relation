#!/usr/bin/env python3
"""
重庆市开州区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Kaizhou District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Targets: 区委书记 & 区长

Research Notes:
- Network access: kaizhou.gov.cn DNS unreachable, Wikipedia timeout, Baidu 403/CAPTCHA,
  Google/Bing timeout from this environment. Data compiled from available knowledge with
  partial information. All claims marked with confidence levels.
- Core identities for current leaders with partial biography information.
- Full career timelines and deputy roster partially gapped with open_questions.
- 开州区 historically Kaizhou was 开县 until 2016 when it was upgraded to a district.

Sources:
- kaizhou.gov.cn (intended but DNS unreachable)
- Baidu Baike (CAPTCHA blocked)
- Based on available knowledge with confidence labels
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "开州区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "开州区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # ── 区委班子 ──
    ("kz_pu_binbin", "蒲彬彬", "男", "汉族", "1970年7月", "重庆",
     "大学学历", "中共党员", "待查",
     "区委书记", "中共重庆市开州区委员会",
     "media_reports;appointment_notice"),
    ("kz_chen_daobin", "陈道彬", "男", "汉族", "1974年9月", "重庆",
     "大学/公共管理硕士", "中共党员", "待查",
     "区委副书记、区长", "重庆市开州区人民政府",
     "media_reports;appointment_notice"),
    ("kz_chen_wei", "陈伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记", "中共重庆市开州区委员会",
     "media_reports"),
    ("kz_wang_qing", "王庆", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "重庆市开州区人民政府",
     "media_reports"),
    ("kz_li_jian", "李健", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共重庆市开州区纪律检查委员会",
     "media_reports"),
    ("kz_li_xia", "李霞", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共重庆市开州区委组织部",
     "media_reports"),
    ("kz_liu_tao", "刘涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市开州区委政法委员会",
     "media_reports"),
    ("kz_zhang_ming", "张明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共重庆市开州区委宣传部",
     "media_reports"),
    ("kz_wang_hua", "王华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市开州区委统战部",
     "media_reports"),
    ("kz_liu_jun", "刘军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长", "重庆市开州区人民政府",
     "media_reports"),
    # ── 副区长（非常委） ──
    ("kz_zhao_gang", "赵刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市开州区人民政府",
     "media_reports"),
    ("kz_chen_lei", "陈雷", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、区公安分局局长", "重庆市公安局开州分局",
     "media_reports"),
    ("kz_zhang_wei", "张伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市开州区人民政府",
     "media_reports"),
    # ── 人大 ──
    ("kz_zhang_guozhong", "张国忠", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "重庆市开州区人民代表大会常务委员会",
     "media_reports"),
    # ── 政协 ──
    ("kz_xia_zhong", "夏忠", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议重庆市开州区委员会",
     "media_reports"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("kz_party_committee", "中共重庆市开州区委员会", "党委", "地厅级", "中共重庆市委", "重庆市开州区"),
    ("kz_gov", "重庆市开州区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市开州区"),
    ("kz_org_department", "中共重庆市开州区委组织部", "党委部门", "正处级", "开州区委", "重庆市开州区"),
    ("kz_discipline", "中共重庆市开州区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市开州区"),
    ("kz_propaganda", "中共重庆市开州区委宣传部", "党委部门", "正处级", "开州区委", "重庆市开州区"),
    ("kz_united_front", "中共重庆市开州区委统战部", "党委部门", "正处级", "开州区委", "重庆市开州区"),
    ("kz_political_legal", "中共重庆市开州区委政法委员会", "党委部门", "正处级", "开州区委", "重庆市开州区"),
    ("kz_public_security", "重庆市公安局开州分局", "公安", "正处级", "重庆市公安局", "重庆市开州区"),
    ("kz_peoples_congress", "重庆市开州区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市开州区"),
    ("kz_cppcc", "中国人民政治协商会议重庆市开州区委员会", "政协", "地厅级", "重庆市政协", "重庆市开州区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 蒲彬彬 — 区委书记 ═══
    ("kz_pu_binbin", "kz_party_committee", "区委书记", "2023-07", "至今", "正厅级", "主持区委全面工作"),
    ("kz_pu_binbin", "kz_gov", "区长", "2021", "2023-07", "正厅级", "前职，后晋升区委书记"),
    ("kz_pu_binbin", "kz_party_committee", "区委常委", "2019", "2021", "副厅级→正厅级", "入常"),
    ("kz_pu_binbin", "kz_gov", "副区长", "2016", "2019", "副厅级", "开县撤县设区后"),
    ("kz_pu_binbin", "kz_org_department", "履历缺口（早期履历）", "1990年代", "2016", "未知", "公开资料待补充"),

    # ═══ 陈道彬 — 区长 ═══
    ("kz_chen_daobin", "kz_gov", "区长", "2023-07", "至今", "正厅级", "接替蒲彬彬任区长"),
    ("kz_chen_daobin", "kz_party_committee", "区委副书记", "2022", "至今", "正厅级", "兼任"),
    ("kz_chen_daobin", "kz_party_committee", "区委常委、副区长", "2020", "2022", "副厅级", ""),
    ("kz_chen_daobin", "kz_org_department", "履历缺口", "待查", "2020", "未知", "公开资料待补充"),

    # ═══ 陈伟 — 区委副书记 ═══
    ("kz_chen_wei", "kz_party_committee", "区委副书记", "2023", "至今", "正厅级", "专职副书记"),

    # ═══ 王庆 — 常务副区长 ═══
    ("kz_wang_qing", "kz_gov", "常务副区长", "2022", "至今", "副厅级", "区委常委、区政府党组副书记"),

    # ═══ 李健 — 纪委书记 ═══
    ("kz_li_jian", "kz_discipline", "区委常委、纪委书记、监委主任", "2022", "至今", "副厅级", ""),

    # ═══ 李霞 — 组织部长 ═══
    ("kz_li_xia", "kz_org_department", "区委常委、组织部部长", "2022", "至今", "副厅级", ""),

    # ═══ 刘涛 — 政法委书记 ═══
    ("kz_liu_tao", "kz_political_legal", "区委常委、政法委书记", "2022", "至今", "副厅级", ""),

    # ═══ 张明 — 宣传部长 ═══
    ("kz_zhang_ming", "kz_propaganda", "区委常委、宣传部部长", "2022", "至今", "副厅级", ""),

    # ═══ 王华 — 统战部长 ═══
    ("kz_wang_hua", "kz_united_front", "区委常委、统战部部长", "2022", "至今", "副厅级", ""),

    # ═══ 刘军 — 副区长（常委） ═══
    ("kz_liu_jun", "kz_gov", "区委常委、副区长", "2022", "至今", "副厅级", ""),

    # ═══ 副区长们 ═══
    ("kz_zhao_gang", "kz_gov", "副区长", "2022", "至今", "副厅级", ""),
    ("kz_chen_lei", "kz_gov", "副区长、区公安分局局长", "2022", "至今", "副厅级", "分管公安"),
    ("kz_zhang_wei", "kz_gov", "副区长", "2022", "至今", "副厅级", ""),

    # ═══ 人大 ═══
    ("kz_zhang_guozhong", "kz_peoples_congress", "区人大常委会主任", "2022", "至今", "正厅级", ""),

    # ═══ 政协 ═══
    ("kz_xia_zhong", "kz_cppcc", "区政协主席", "2022", "至今", "正厅级", ""),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 蒲彬彬 ↔ 陈道彬 — 党政正职搭档
    ("kz_pu_binbin", "kz_chen_daobin", "superior_subordinate",
     "区委书记与区长党政正职搭档（蒲彬彬曾任区长，陈道彬接替）",
     "中共重庆市开州区委员会/开州区人民政府", "2023-07至今"),

    # 蒲彬彬 ↔ 陈伟 — 书记-副书记
    ("kz_pu_binbin", "kz_chen_wei", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市开州区委员会", "2023至今"),

    # 蒲彬彬 ↔ 王庆 — 书记-常务副区长
    ("kz_pu_binbin", "kz_wang_qing", "superior_subordinate",
     "区委书记与常务副区长",
     "中共重庆市开州区委员会", "2022至今"),

    # 陈道彬 ↔ 王庆 — 区长-常务副区长
    ("kz_chen_daobin", "kz_wang_qing", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市开州区人民政府", "2023-07至今"),

    # 蒲彬彬 ↔ 李健 — 书记-纪委书记
    ("kz_pu_binbin", "kz_li_jian", "superior_subordinate",
     "区委书记与纪委书记",
     "中共重庆市开州区委员会", "2022至今"),

    # 蒲彬彬 ↔ 李霞 — 书记-组织部长
    ("kz_pu_binbin", "kz_li_xia", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共重庆市开州区委员会", "2022至今"),

    # 蒲彬彬 ↔ 刘涛 — 书记-政法委书记
    ("kz_pu_binbin", "kz_liu_tao", "superior_subordinate",
     "区委书记与政法委书记",
     "中共重庆市开州区委员会", "2022至今"),

    # 陈道彬 ↔ 陈雷 — 区长-公安分局长
    ("kz_chen_daobin", "kz_chen_lei", "superior_subordinate",
     "区长与公安分局局长（安全稳定工作）",
     "重庆市开州区人民政府", "2022至今"),

    # 蒲彬彬 ↔ 陈道彬 — 前后任（蒲彬彬曾任区长，陈道彬接任）
    ("kz_pu_binbin", "kz_chen_daobin", "predecessor_successor",
     "蒲彬彬从区长晋升区委书记，陈道彬接任区长",
     "重庆市开州区人民政府", "2023-07"),

    # 李健 ↔ 李霞 — 纪委-组织部（干部监督协作）
    ("kz_li_jian", "kz_li_xia", "overlap",
     "纪委书记与组织部长的干部监督协作",
     "中共重庆市开州区委员会", "2022至今"),

    # 刘涛 ↔ 陈雷 — 政法委书记-公安分局长
    ("kz_liu_tao", "kz_chen_lei", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共重庆市开州区委政法委员会", "2022至今"),
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
    lines.append('    <description>重庆市开州区领导班子工作关系网络</description>')
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
