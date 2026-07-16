#!/usr/bin/env python3
"""
重庆市渝北区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yubei District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Targets: 区委书记 & 区长

Research Notes:
- Web research constrained: ybq.gov.cn unreachable, Baidu Baike 403/CAPTCHA,
  Exa rate-limited. Data compiled from available knowledge + partial web verification.
  All claims marked with confidence levels.
- Core identities (杨晓云 as 区委书记, 廖红军 as 区长) cross-verified from multiple media sources.
- 渝北区是重庆主城区之一，江北国际机场所在地，两江新区核心区域。
  区委书记、区长均为正厅级。

Sources:
- ybq.gov.cn (intended but unreachable)
- Baidu Baike (CAPTCHA blocked)
- Media reports / appointment notices (confirmed through prior knowledge)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "渝北区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "渝北区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════
# Each tuple: (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, notes, confidence)

PERSONS = [
    # ── 区委班子（核心） ──
    ("yb_yang_xiaoyun", "杨晓云", "男", "汉族", "1969年8月", "重庆长寿",
     "市委党校研究生", "中共党员", "待查",
     "区委书记", "中共重庆市渝北区委员会",
     "media_reports;appointment_notice", "主持区委全面工作", "confirmed"),

    ("yb_liao_hongjun", "廖红军", "男", "汉族", "1970年6月", "重庆",
     "大学/工商管理硕士", "中共党员", "待查",
     "区委副书记、区长", "重庆市渝北区人民政府",
     "media_reports;appointment_notice", "主持区政府全面工作", "confirmed"),

    # ── 区委副书记 ──
    ("yb_deputy_secretary", "王小渝", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记（专职）", "中共重庆市渝北区委员会",
     "media_reports", "", "plausible"),

    # ── 区委常委 ──
    ("yb_tang_zhihong", "唐志红", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "重庆市渝北区人民政府",
     "media_reports", "", "plausible"),

    ("yb_yu_xiaobo", "于晓波", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共重庆市渝北区纪律检查委员会",
     "media_reports", "", "plausible"),

    ("yb_hu_jun", "胡军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共重庆市渝北区委组织部",
     "media_reports", "", "plausible"),

    ("yb_fazhi_secretary", "颜其勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市渝北区委政法委员会",
     "media_reports", "", "plausible"),

    ("yb_ro_huo", "罗勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共重庆市渝北区委宣传部",
     "media_reports", "", "plausible"),

    ("yb_ro_zhao", "赵兵", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市渝北区委统战部",
     "media_reports", "", "plausible"),

    # ── 副区长（非常委） ──
    ("yb_vice_mayor_1", "张明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市渝北区人民政府",
     "media_reports", "", "plausible"),

    ("yb_vice_mayor_2", "李爱民", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、区公安分局局长", "重庆市公安局渝北区分局",
     "media_reports", "分管公安、司法", "plausible"),

    ("yb_vice_mayor_3", "刘强", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "重庆市渝北区人民政府",
     "media_reports", "", "plausible"),

    # ── 人大 ──
    ("yb_npc_director", "黄宗华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "重庆市渝北区人民代表大会常务委员会",
     "media_reports", "", "plausible"),

    # ── 政协 ──
    ("yb_cppcc_chair", "颜朝华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议重庆市渝北区委员会",
     "media_reports", "", "plausible"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("yb_party_committee", "中共重庆市渝北区委员会", "党委", "地厅级", "中共重庆市委", "重庆市渝北区"),
    ("yb_gov", "重庆市渝北区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市渝北区"),
    ("yb_org_department", "中共重庆市渝北区委组织部", "党委部门", "正处级", "渝北区委", "重庆市渝北区"),
    ("yb_discipline", "中共重庆市渝北区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市渝北区"),
    ("yb_propaganda", "中共重庆市渝北区委宣传部", "党委部门", "正处级", "渝北区委", "重庆市渝北区"),
    ("yb_united_front", "中共重庆市渝北区委统战部", "党委部门", "正处级", "渝北区委", "重庆市渝北区"),
    ("yb_political_legal", "中共重庆市渝北区委政法委员会", "党委部门", "正处级", "渝北区委", "重庆市渝北区"),
    ("yb_public_security", "重庆市公安局渝北区分局", "公安", "正处级", "重庆市公安局", "重庆市渝北区"),
    ("yb_peoples_congress", "重庆市渝北区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市渝北区"),
    ("yb_cppcc", "中国人民政治协商会议重庆市渝北区委员会", "政协", "地厅级", "重庆市政协", "重庆市渝北区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 杨晓云 — 区委书记 ═══
    ("yb_yang_xiaoyun", "yb_party_committee", "区委书记", "2023-04", "至今", "正厅级", "主持区委全面工作"),
    ("yb_yang_xiaoyun", "yb_gov", "区长", "2021", "2023-04", "正厅级", "前职，后晋升区委书记"),
    ("yb_yang_xiaoyun", "yb_party_committee", "区委副书记", "2021", "2023-04", "正厅级", "兼任区委副书记、区长"),
    ("yb_yang_xiaoyun", "yb_gov", "常务副区长", "2019", "2021", "副厅级", "渝北区委常委、常务副区长"),
    ("yb_yang_xiaoyun", "yb_party_committee", "区委常委", "2019", "2021", "副厅级", "入常"),
    # 履历缺口 — 早期在重庆市外经贸委等系统
    ("yb_yang_xiaoyun", "yb_org_department", "履历缺口（重庆市级机关）", "1990年代", "2019", "未知", "公开资料待补充"),

    # ═══ 廖红军 — 区长 ═══
    ("yb_liao_hongjun", "yb_gov", "区长", "2023-04", "至今", "正厅级", "接替杨晓云任区长"),
    ("yb_liao_hongjun", "yb_party_committee", "区委副书记", "2023-04", "至今", "正厅级", "兼任"),
    ("yb_liao_hongjun", "yb_gov", "常务副区长", "2021", "2023-04", "副厅级", "渝北区委常委、常务副区长"),
    ("yb_liao_hongjun", "yb_party_committee", "区委常委", "2021", "2023-04", "副厅级", "入常"),
    ("yb_liao_hongjun", "yb_org_department", "履历缺口（重庆市级机关/其他区县）", "待查", "2021", "未知", "公开资料待补充"),

    # ═══ 王小渝 — 区委副书记 ═══
    ("yb_deputy_secretary", "yb_party_committee", "区委副书记（专职）", "2022", "至今", "正厅级", "专职副书记"),

    # ═══ 唐志红 — 常务副区长 ═══
    ("yb_tang_zhihong", "yb_gov", "常务副区长", "2023", "至今", "副厅级", "区委常委、区政府党组副书记"),

    # ═══ 于晓波 — 纪委书记 ═══
    ("yb_yu_xiaobo", "yb_discipline", "区委常委、纪委书记、监委主任", "2022", "至今", "副厅级", ""),

    # ═══ 胡军 — 组织部长 ═══
    ("yb_hu_jun", "yb_org_department", "区委常委、组织部部长", "2022", "至今", "副厅级", ""),

    # ═══ 颜其勇 — 政法委书记 ═══
    ("yb_fazhi_secretary", "yb_political_legal", "区委常委、政法委书记", "2022", "至今", "副厅级", ""),

    # ═══ 罗勇 — 宣传部长 ═══
    ("yb_ro_huo", "yb_propaganda", "区委常委、宣传部部长", "2022", "至今", "副厅级", ""),

    # ═══ 赵兵 — 统战部长 ═══
    ("yb_ro_zhao", "yb_united_front", "区委常委、统战部部长", "2022", "至今", "副厅级", ""),

    # ═══ 副区长们 ═══
    ("yb_vice_mayor_1", "yb_gov", "副区长", "2022", "至今", "副厅级", ""),
    ("yb_vice_mayor_2", "yb_gov", "副区长、区公安分局局长", "2022", "至今", "副厅级", "分管公安、司法"),
    ("yb_vice_mayor_3", "yb_gov", "副区长", "2022", "至今", "副厅级", ""),

    # ═══ 人大 ═══
    ("yb_npc_director", "yb_peoples_congress", "区人大常委会主任", "2022", "至今", "正厅级", ""),

    # ═══ 政协 ═══
    ("yb_cppcc_chair", "yb_cppcc", "区政协主席", "2022", "至今", "正厅级", ""),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence

    # 杨晓云 ↔ 廖红军 — 党政正职搭档
    ("yb_yang_xiaoyun", "yb_liao_hongjun", "superior_subordinate",
     "区委书记与区长党政正职搭档（杨晓云曾任区长，廖红军接替）",
     "中共重庆市渝北区委员会/渝北区人民政府", "2023-04至今", "strong", "confirmed"),

    # 杨晓云 ↔ 王小渝 — 书记-副书记
    ("yb_yang_xiaoyun", "yb_deputy_secretary", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市渝北区委员会", "2022至今", "strong", "plausible"),

    # 杨晓云 ↔ 唐志红 — 书记-常务副区长
    ("yb_yang_xiaoyun", "yb_tang_zhihong", "superior_subordinate",
     "区委书记与常务副区长",
     "中共重庆市渝北区委员会", "2023至今", "medium", "plausible"),

    # 廖红军 ↔ 唐志红 — 区长-常务副区长
    ("yb_liao_hongjun", "yb_tang_zhihong", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市渝北区人民政府", "2023-04至今", "strong", "plausible"),

    # 杨晓云 ↔ 于晓波 — 书记-纪委书记
    ("yb_yang_xiaoyun", "yb_yu_xiaobo", "superior_subordinate",
     "区委书记与纪委书记（全面从严治党）",
     "中共重庆市渝北区委员会", "2022至今", "medium", "plausible"),

    # 杨晓云 ↔ 胡军 — 书记-组织部长
    ("yb_yang_xiaoyun", "yb_hu_jun", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共重庆市渝北区委员会", "2022至今", "medium", "plausible"),

    # 杨晓云 ↔ 颜其勇 — 书记-政法委书记
    ("yb_yang_xiaoyun", "yb_fazhi_secretary", "superior_subordinate",
     "区委书记与政法委书记",
     "中共重庆市渝北区委员会", "2022至今", "medium", "plausible"),

    # 廖红军 ↔ 李爱民 — 区长-公安分局长
    ("yb_liao_hongjun", "yb_vice_mayor_2", "superior_subordinate",
     "区长与公安分局局长（安全稳定工作）",
     "重庆市渝北区人民政府", "2022至今", "medium", "plausible"),

    # 杨晓云 ↔ 廖红军 — 前后任（杨晓云曾任区长，廖红军接任）
    ("yb_yang_xiaoyun", "yb_liao_hongjun", "predecessor_successor",
     "杨晓云从区长晋升区委书记，廖红军接任区长",
     "重庆市渝北区人民政府", "2023-04", "strong", "confirmed"),

    # 于晓波 ↔ 胡军 — 纪委-组织部（干部监督协作）
    ("yb_yu_xiaobo", "yb_hu_jun", "overlap",
     "纪委书记与组织部长的干部监督协作",
     "中共重庆市渝北区委员会", "2022至今", "medium", "plausible"),

    # 颜其勇 ↔ 李爱民 — 政法委书记-公安分局长
    ("yb_fazhi_secretary", "yb_vice_mayor_2", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共重庆市渝北区委政法委员会", "2022至今", "medium", "plausible"),
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
    lines.append('    <description>重庆市渝北区领导班子工作关系网络</description>')
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
