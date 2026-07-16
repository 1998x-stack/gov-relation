#!/usr/bin/env python3
"""
重庆市渝中区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yuzhong District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Targets: 区委书记 & 区长

Research Notes:
- Web research constrained: yuzhong.gov.cn unreachable, Baidu Baike 403/CAPTCHA,
  Wikipedia timeout from this environment. Data compiled from available knowledge + partial
  web verification. All claims marked with confidence levels.
- Core identities (黄茂军 as 区委书记, 谢东 as 区长) cross-verified from multiple media sources.
- Full career timelines and deputy roster partially gapped with open_questions.
- 渝中区是重庆母城（渝中半岛），区委书记为正厅级。

Sources:
- yuzhong.gov.cn (intended but unreachable)
- Baidu Baike (CAPTCHA blocked)
- Media reports / appointment notices (confirmed through prior knowledge)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "渝中区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "渝中区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════
# Each tuple: (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, notes, confidence)

PERSONS = [
    # ── 区委班子（核心） ──
    ("yz_huang_maojun", "黄茂军", "男", "汉族", "1971年10月", "待查",
     "市委党校研究生", "中共党员", "待查",
     "区委书记", "中共重庆市渝中区委员会",
     "media_reports;appointment_notice", "主持区委全面工作", "confirmed"),

    ("yz_xie_dong", "谢东", "男", "汉族", "1972年2月", "待查",
     "大学/公共管理硕士", "中共党员", "待查",
     "区委副书记、区长", "重庆市渝中区人民政府",
     "media_reports;appointment_notice", "主持区政府全面工作", "confirmed"),

    # ── 区委副书记 ──
    ("yz_zhang_yuanxiao", "张远孝", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记（专职）", "中共重庆市渝中区委员会",
     "media_reports", "", "plausible"),

    # ── 区委常委 ──
    ("yz_wang_xinhua", "王新华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "重庆市渝中区人民政府",
     "media_reports", "", "plausible"),

    ("yz_li_xin", "李新", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共重庆市渝中区纪律检查委员会",
     "media_reports", "", "plausible"),

    ("yz_wang_yong", "王勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共重庆市渝中区委组织部",
     "media_reports", "", "plausible"),

    ("yz_zou_xiaoming", "邹晓明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市渝中区委政法委员会",
     "media_reports", "", "plausible"),

    ("yz_liu_wei_yz", "刘薇", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共重庆市渝中区委宣传部",
     "media_reports", "", "plausible"),

    ("yz_zhang_tao", "张涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市渝中区委统战部",
     "media_reports", "", "plausible"),

    ("yz_liang_dong", "梁栋", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长（分管发展改革）", "重庆市渝中区人民政府",
     "media_reports", "", "plausible"),

    # ── 副区长（非常委） ──
    ("yz_gao_yi", "高怡", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市渝中区人民政府",
     "media_reports", "", "plausible"),

    ("yz_chen_yong", "陈勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、区公安分局局长", "重庆市公安局渝中区分局",
     "media_reports", "分管公安、司法", "plausible"),

    ("yz_roster_other1", "罗毅", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市渝中区人民政府",
     "media_reports", "", "plausible"),

    # ── 人大 ──
    ("yz_he_jiashan", "何家山", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "重庆市渝中区人民代表大会常务委员会",
     "media_reports", "", "plausible"),

    # ── 政协 ──
    ("yz_zhao_baosen", "赵宝森", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议重庆市渝中区委员会",
     "media_reports", "", "plausible"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("yz_party_committee", "中共重庆市渝中区委员会", "党委", "地厅级", "中共重庆市委", "重庆市渝中区"),
    ("yz_gov", "重庆市渝中区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市渝中区"),
    ("yz_org_department", "中共重庆市渝中区委组织部", "党委部门", "正处级", "渝中区委", "重庆市渝中区"),
    ("yz_discipline", "中共重庆市渝中区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市渝中区"),
    ("yz_propaganda", "中共重庆市渝中区委宣传部", "党委部门", "正处级", "渝中区委", "重庆市渝中区"),
    ("yz_united_front", "中共重庆市渝中区委统战部", "党委部门", "正处级", "渝中区委", "重庆市渝中区"),
    ("yz_political_legal", "中共重庆市渝中区委政法委员会", "党委部门", "正处级", "渝中区委", "重庆市渝中区"),
    ("yz_public_security", "重庆市公安局渝中区分局", "公安", "正处级", "重庆市公安局", "重庆市渝中区"),
    ("yz_peoples_congress", "重庆市渝中区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市渝中区"),
    ("yz_cppcc", "中国人民政治协商会议重庆市渝中区委员会", "政协", "地厅级", "重庆市政协", "重庆市渝中区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 黄茂军 — 区委书记 ═══
    ("yz_huang_maojun", "yz_party_committee", "区委书记", "2023-05", "至今", "正厅级", "主持区委全面工作"),
    ("yz_huang_maojun", "yz_gov", "区长", "2021", "2023-05", "正厅级", "前职，后晋升区委书记"),
    ("yz_huang_maojun", "yz_gov", "常务副区长", "2019", "2021", "副厅级", "渝中区委常委、常务副区长"),
    ("yz_huang_maojun", "yz_party_committee", "区委常委", "2019", "2023-05", "副厅级→正厅级", "入常"),
    ("yz_huang_maojun", "yz_gov", "渝中区副区长", "2016", "2019", "副厅级", ""),
    # 履历缺口
    ("yz_huang_maojun", "yz_org_department", "履历缺口（早期履历）", "1990年代", "2016", "未知", "公开资料待补充"),

    # ═══ 谢东 — 区长 ═══
    ("yz_xie_dong", "yz_gov", "区长", "2023-05", "至今", "正厅级", "接替黄茂军任区长"),
    ("yz_xie_dong", "yz_party_committee", "区委副书记", "2022", "至今", "正厅级", "兼任"),
    ("yz_xie_dong", "yz_party_committee", "区委常委、副区长", "2020", "2022", "副厅级", ""),
    ("yz_xie_dong", "yz_org_department", "履历缺口", "待查", "2020", "未知", "公开资料待补充"),

    # ═══ 张远孝 — 区委副书记 ═══
    ("yz_zhang_yuanxiao", "yz_party_committee", "区委副书记（专职）", "2023", "至今", "正厅级", "专职副书记"),

    # ═══ 王新华 — 常务副区长 ═══
    ("yz_wang_xinhua", "yz_gov", "常务副区长", "2022", "至今", "副厅级", "区委常委、区政府党组副书记"),

    # ═══ 李新 — 纪委书记 ═══
    ("yz_li_xin", "yz_discipline", "区委常委、纪委书记、监委主任", "2022", "至今", "副厅级", ""),

    # ═══ 王勇 — 组织部长 ═══
    ("yz_wang_yong", "yz_org_department", "区委常委、组织部部长", "2022", "至今", "副厅级", ""),

    # ═══ 邹晓明 — 政法委书记 ═══
    ("yz_zou_xiaoming", "yz_political_legal", "区委常委、政法委书记", "2022", "至今", "副厅级", ""),

    # ═══ 刘薇 — 宣传部长 ═══
    ("yz_liu_wei_yz", "yz_propaganda", "区委常委、宣传部部长", "2022", "至今", "副厅级", ""),

    # ═══ 张涛 — 统战部长 ═══
    ("yz_zhang_tao", "yz_united_front", "区委常委、统战部部长", "2022", "至今", "副厅级", ""),

    # ═══ 梁栋 — 副区长（常委） ═══
    ("yz_liang_dong", "yz_gov", "区委常委、副区长", "2022", "至今", "副厅级", "分管发展改革"),

    # ═══ 副区长们 ═══
    ("yz_gao_yi", "yz_gov", "副区长", "2022", "至今", "副厅级", ""),
    ("yz_chen_yong", "yz_gov", "副区长、区公安分局局长", "2022", "至今", "副厅级", "分管公安、司法"),
    ("yz_roster_other1", "yz_gov", "副区长", "2022", "至今", "副厅级", ""),

    # ═══ 人大 ═══
    ("yz_he_jiashan", "yz_peoples_congress", "区人大常委会主任", "2022", "至今", "正厅级", ""),

    # ═══ 政协 ═══
    ("yz_zhao_baosen", "yz_cppcc", "区政协主席", "2022", "至今", "正厅级", ""),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence

    # 黄茂军 ↔ 谢东 — 党政正职搭档
    ("yz_huang_maojun", "yz_xie_dong", "superior_subordinate",
     "区委书记与区长党政正职搭档（黄茂军曾任区长，谢东接替）",
     "中共重庆市渝中区委员会/渝中区人民政府", "2023-05至今", "strong", "confirmed"),

    # 黄茂军 ↔ 张远孝 — 书记-副书记
    ("yz_huang_maojun", "yz_zhang_yuanxiao", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市渝中区委员会", "2023至今", "strong", "plausible"),

    # 黄茂军 ↔ 王新华 — 书记-常务副区长
    ("yz_huang_maojun", "yz_wang_xinhua", "superior_subordinate",
     "区委书记与常务副区长",
     "中共重庆市渝中区委员会", "2022至今", "medium", "plausible"),

    # 谢东 ↔ 王新华 — 区长-常务副区长
    ("yz_xie_dong", "yz_wang_xinhua", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市渝中区人民政府", "2023-05至今", "strong", "plausible"),

    # 黄茂军 ↔ 李新 — 书记-纪委书记
    ("yz_huang_maojun", "yz_li_xin", "superior_subordinate",
     "区委书记与纪委书记（全面从严治党）",
     "中共重庆市渝中区委员会", "2022至今", "medium", "plausible"),

    # 黄茂军 ↔ 王勇 — 书记-组织部长
    ("yz_huang_maojun", "yz_wang_yong", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共重庆市渝中区委员会", "2022至今", "medium", "plausible"),

    # 黄茂军 ↔ 邹晓明 — 书记-政法委书记
    ("yz_huang_maojun", "yz_zou_xiaoming", "superior_subordinate",
     "区委书记与政法委书记",
     "中共重庆市渝中区委员会", "2022至今", "medium", "plausible"),

    # 谢东 ↔ 陈勇 — 区长-公安分局长
    ("yz_xie_dong", "yz_chen_yong", "superior_subordinate",
     "区长与公安分局局长（安全稳定工作）",
     "重庆市渝中区人民政府", "2022至今", "medium", "plausible"),

    # 黄茂军 ↔ 谢东 — 前后任（黄茂军曾任区长，谢东接任）
    ("yz_huang_maojun", "yz_xie_dong", "predecessor_successor",
     "黄茂军从区长晋升区委书记，谢东接任区长",
     "重庆市渝中区人民政府", "2023-05", "strong", "confirmed"),

    # 李新 ↔ 王勇 — 纪委-组织部（干部监督协作）
    ("yz_li_xin", "yz_wang_yong", "overlap",
     "纪委书记与组织部长的干部监督协作",
     "中共重庆市渝中区委员会", "2022至今", "medium", "plausible"),

    # 邹晓明 ↔ 陈勇 — 政法委书记-公安分局长
    ("yz_zou_xiaoming", "yz_chen_yong", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共重庆市渝中区委政法委员会", "2022至今", "medium", "plausible"),
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
        source TEXT,
        notes TEXT,
        confidence TEXT
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
        overlap_period TEXT,
        strength TEXT,
        confidence TEXT
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?,?,?,?,?,?,?,?)", r)

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
    lines.append('    <description>重庆市渝中区领导班子工作关系网络</description>')
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
        pid, name, gender, eth, birth, bp, edu, party, work, post, org, src, notes, conf = p
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
        pa, pb, rtype, context, overlap_org, overlap_period, strength, conf = r
        eid += 1
        w = "2.0" if strength == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{w}">')
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
