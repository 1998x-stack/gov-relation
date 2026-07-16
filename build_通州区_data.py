#!/usr/bin/env python3
"""
北京市通州区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Tongzhou District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjtzh.gov.cn/bjtz/zwgk/qwld/index.shtml (official leadership pages, accessed 2026-07-16)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "通州区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "通州区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子（11人） ──
    ("tz_lijunjie", "李俊杰", "男", "汉族", "1978年8月", "待查",
     "研究生，经济学博士", "中共党员", "待查",
     "区委书记", "中共北京市通州区委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/mjw/index.shtml"),

    ("tz_zheng_hao", "郑皓", "女", "朝鲜族", "1977年2月", "待查",
     "在职研究生，文学博士", "中共党员", "待查",
     "区委副书记、区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/zh/index.shtml"),

    ("tz_lijinke", "李金克", "男", "汉族", "1972年4月", "待查",
     "大学，经济学硕士", "中共党员", "待查",
     "区委副书记", "中共北京市通州区委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/cxs/index.shtml"),

    ("tz_hou_jianmei", "侯健美", "女", "汉族", "1978年12月", "待查",
     "研究生，哲学硕士、工商管理硕士", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市通州区委宣传部",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/wyj/index.shtml"),

    ("tz_li_xianxia", "李先侠", "男", "汉族", "1979年5月", "待查",
     "研究生，管理学硕士", "中共党员", "待查",
     "区委常委、常务副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/wb/index.shtml"),

    ("tz_wu_kongan", "吴孔安", "男", "汉族", "1976年8月", "待查",
     "中央党校研究生，管理学学士", "中共党员", "待查",
     "区委常委、副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/wka/index.shtml"),

    ("tz_wang_xiangyu", "王翔宇", "男", "汉族", "1980年1月", "待查",
     "研究生，工学硕士", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市通州区委组织部",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/hjm/index.shtml"),

    ("tz_qin_tao", "秦涛", "男", "汉族", "1972年2月", "待查",
     "在职研究生，管理学硕士", "中共党员", "待查",
     "区委常委、政法委书记", "中共北京市通州区委政法委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/wym/index.shtml"),

    ("tz_lai_yibin", "赖毅斌", "男", "汉族", "1979年3月", "待查",
     "研究生，法学硕士", "中共党员", "待查",
     "区委常委、纪委书记、区监察委员会主任", "中共北京市通州区纪律检查委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/hxj/index.shtml"),

    ("tz_dong_lixian", "董丽献", "男", "汉族", "1976年6月", "待查",
     "中央党校大学", "中共党员", "待查",
     "区委常委、武装部政委", "北京市通州区人民武装部",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/yl/index.shtml"),

    ("tz_lu_qinglei", "卢庆雷", "男", "汉族", "1976年4月", "待查",
     "在职研究生，工商管理硕士", "中共党员", "待查",
     "区委常委、统战部部长", "中共北京市通州区委统战部",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qwldr/wxy/index.shtml"),

    # ── 区政府副区长（非常委） ──
    ("tz_dong_minghui", "董明慧", "女", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/dmh/index.shtml"),

    ("tz_gao_fei", "高飞", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/ndc/index.shtml"),

    ("tz_han_song", "韩松", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/gf/index.shtml"),

    ("tz_lin_zhenghang", "林正航", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/qt/index.shtml"),

    ("tz_yao_weilong", "姚伟龙", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/ywl/index.shtml"),

    ("tz_zou_haitao", "邹海涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/zht/index.shtml"),

    ("tz_zheng_yi", "郑毅", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/tq/index.shtml"),

    ("tz_he_ming", "何明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市通州区人民政府",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/qzzc/qlz/index.shtml"),

    # ── 区人大主要领导 ──
    ("tz_zhao_yuying", "赵玉影", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "北京市通州区人民代表大会常务委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/rdld/zyy/index.shtml"),

    ("tz_cheng_weimin", "程卫民", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市通州区人民代表大会常务委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/rdld/cwm/index.shtml"),

    ("tz_lu_xinhong", "鲁新红", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任", "北京市通州区人民代表大会常务委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/rdld/lxh/index.shtml"),

    ("tz_fang_yajun", "房亚军", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任", "北京市通州区人民代表大会常务委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/rdld/fyj/index.shtml"),

    ("tz_liu_xiujie", "刘秀杰", "女", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任", "北京市通州区人民代表大会常务委员会",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/rdld/lxj/index.shtml"),

    # ── 区政协主要领导 ──
    ("tz_hu_xuefeng", "胡雪峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "北京市通州区政协",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/zxld/zdq/index.shtml"),

    ("tz_ni_decai", "倪德才", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "北京市通州区政协",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/zxld/fly/index.shtml"),

    ("tz_zhen_yu", "甄宇", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "北京市通州区政协",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/zxld/zy/index.shtml"),

    ("tz_jin_wenling", "金文岭", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "北京市通州区政协",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/zxld/jwl/index.shtml"),

    ("tz_pei_zhigang", "裴志刚", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "北京市通州区政协",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/zxld/wt/index.shtml"),

    ("tz_xu_xiaoyun", "徐晓云", "女", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "北京市通州区政协",
     "bjtzh.gov.cn/bjtz/zwgk/qwld/zxld/tch/index.shtml"),
]

# id → name lookup
PID_NAME = {p[0]: p[1] for p in PERSONS}

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("org_qw", "中共北京市通州区委员会", "党委", "正厅级", "中共北京市委", "北京市通州区"),
    ("org_qw_xcb", "中共北京市通州区委宣传部", "党委", "正处级", "中共北京市通州区委员会", "北京市通州区"),
    ("org_qw_zzb", "中共北京市通州区委组织部", "党委", "正处级", "中共北京市通州区委员会", "北京市通州区"),
    ("org_qw_zfw", "中共北京市通州区委政法委员会", "党委", "正处级", "中共北京市通州区委员会", "北京市通州区"),
    ("org_qw_tyzxb", "中共北京市通州区委统战部", "党委", "正处级", "中共北京市通州区委员会", "北京市通州区"),
    ("org_qw_jw", "中共北京市通州区纪律检查委员会", "党委", "正处级", "中共北京市通州区委员会", "北京市通州区"),
    ("org_zf", "北京市通州区人民政府", "政府", "正厅级", "北京市人民政府", "北京市通州区"),
    ("org_rd", "北京市通州区人民代表大会常务委员会", "人大", "正厅级", "北京市人民代表大会常务委员会", "北京市通州区"),
    ("org_zx", "北京市通州区政协", "政协", "正厅级", "北京市政协", "北京市通州区"),
    ("org_wzb", "北京市通州区人民武装部", "政府", "正师级", "北京卫戍区", "北京市通州区"),
]

POSITIONS = []
pid = 1
for p in PERSONS:
    pid_key = p[0]
    org_key = None
    title = p[9]
    if "区委" in title or "书记" == p[9] or "副书记" == p[9]:
        org_key = "org_qw"
    elif "宣传部" in title:
        org_key = "org_qw_xcb"
    elif "组织部" in title:
        org_key = "org_qw_zzb"
    elif "政法委" in title:
        org_key = "org_qw_zfw"
    elif "统战部" in title:
        org_key = "org_qw_tyzxb"
    elif "纪委" in title or "监察" in title:
        org_key = "org_qw_jw"
    elif "武装部" in title:
        org_key = "org_wzb"
    elif "政府" in title or "区长" == p[9] or "副区长" in title:
        org_key = "org_zf"
    elif "人大" in p[9]:
        org_key = "org_rd"
    elif "政协" in p[9]:
        org_key = "org_zx"

    rank = "正厅级" if "书记" == p[9] or "区长" == p[9] else \
           "正厅级" if "人大" in p[8] and "主任" in p[9] else \
           "正厅级" if "政协" in p[8] and "主席" in p[9] else \
           "副厅级" if "常委" in p[8] or "副主任" in p[9] or "副主席" in p[9] else \
           "副厅级"

    POSITIONS.append((pid, pid_key, org_key, title, rank, "", ""))
    pid += 1


RELATIONSHIPS = []

# 书记-区长：党政搭档
RELATIONSHIPS.append((1, "tz_lijunjie", "tz_zheng_hao", "党政搭档", "中共北京市通州区委/区政府", "2025-", "strong"))

# 书记-副书记（专职）
RELATIONSHIPS.append((2, "tz_lijunjie", "tz_lijinke", "上下级", "中共北京市通州区委", "2025-", "strong"))

# 区长-常务副区长
RELATIONSHIPS.append((3, "tz_zheng_hao", "tz_li_xianxia", "上下级", "北京市通州区人民政府", "2025-", "strong"))

# 区长-副区长吴孔安
RELATIONSHIPS.append((4, "tz_zheng_hao", "tz_wu_kongan", "上下级", "北京市通州区人民政府", "2025-", "strong"))

# 区委常委班子所有成员 → 书记
for rel_id, pid_key in [(5, "tz_hou_jianmei"), (6, "tz_li_xianxia"), (7, "tz_wu_kongan"),
                         (8, "tz_wang_xiangyu"), (9, "tz_qin_tao"), (10, "tz_lai_yibin"),
                         (11, "tz_dong_lixian"), (12, "tz_lu_qinglei")]:
    RELATIONSHIPS.append((rel_id, "tz_lijunjie", pid_key, "区委常委班子", "中共北京市通州区委", "2025-", "strong"))

# 副书记-常委（李金克）
for rel_id, pid_key in [(13, "tz_hou_jianmei"), (14, "tz_li_xianxia"), (15, "tz_wu_kongan"),
                         (16, "tz_wang_xiangyu"), (17, "tz_qin_tao"), (18, "tz_lai_yibin"),
                         (19, "tz_dong_lixian"), (20, "tz_lu_qinglei")]:
    RELATIONSHIPS.append((rel_id, "tz_lijinke", pid_key, "专职副书记与常委", "中共北京市通州区委", "2025-", "medium"))


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
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
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT,
            title TEXT,
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
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  p)

    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], ""))

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r[1], r[2], r[3], r[4], r[5], r[6]))

    conn.commit()
    conn.close()
    print(f"✅ Database: {DB_PATH}")


def build_gexf():
    now = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>北京市通州区领导班子工作关系网络 - Party Secretary, District Mayor and Leadership Team</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="education" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[9]
        birth = p[4] if p[4] != "待查" else ""
        edu = p[6] if p[6] != "待查" else ""

        # Determine color by role
        if "书记" == role:
            color = "255,50,50"
            role_type = "party_secretary"
            sz = "20.0"
        elif "区长" in role:
            color = "50,100,255"
            role_type = "district_mayor"
            sz = "20.0"
        elif "副区长" in role:
            color = "50,100,255"
            role_type = "deputy_mayor"
            sz = "12.0"
        elif "纪委书记" in role or "监委" in role:
            color = "255,165,0"
            role_type = "discipline"
            sz = "12.0"
        elif "副书记" in role:
            color = "255,50,50"
            role_type = "deputy_secretary"
            sz = "15.0"
        elif "常委" in role:
            color = "100,100,100"
            role_type = "standing_committee"
            sz = "12.0"
        elif "人大会" in role:
            color = "100,100,100"
            role_type = "npc"
            sz = "10.0"
        elif "政协" in role:
            color = "100,100,100"
            role_type = "cppcc"
            sz = "10.0"
        else:
            color = "100,100,100"
            role_type = "other"
            sz = "12.0"

        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role_type)}"/>')
        if birth:
            lines.append(f'          <attvalue for="2" value="{esc(birth)}"/>')
        if edu:
            lines.append(f'          <attvalue for="3" value="{esc(edu)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]

        # Color by org type
        if "党委" == otype:
            orgc = "255,200,200"
        elif "政府" == otype:
            orgc = "200,200,255"
        elif "人大" == otype:
            orgc = "200,255,255"
        elif "政协" == otype:
            orgc = "255,240,200"
        else:
            orgc = "200,200,200"

        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{orgc.split(",")[0]}" g="{orgc.split(",")[1]}" b="{orgc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    eid = 0
    lines.append('    <edges>')

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        person_id = pos[1]
        org_id = pos[2]
        if org_id is None:
            continue
        title = pos[3] if pos[3] else "任职"
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        eid += 1
        pa = r[1]
        pb = r[2]
        rtype = r[3]
        ctx = r[4]
        org = r[5] if r[5] else ""
        period = r[6] if r[6] else ""
        w = "2.0" if r[6] == "strong" else "1.5"

        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        if org:
            lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        if period:
            lines.append(f'          <attvalue for="3" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF: {GEXF_PATH}")


def main():
    build_db()
    build_gexf()

    # Print summary
    print(f"\n📊  Summary:")
    print(f"   Persons: {len(PERSONS)}")
    print(f"   Organizations: {len(ORGANIZATIONS)}")
    print(f"   Positions: {len(POSITIONS)}")
    print(f"   Relationships: {len(RELATIONSHIPS)}")


if __name__ == "__main__":
    main()
