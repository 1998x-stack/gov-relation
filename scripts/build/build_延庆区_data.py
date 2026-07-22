#!/usr/bin/env python3
"""
北京市延庆区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yanqing District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjyq.gov.cn (official leadership pages)
- Baidu Baike, government appointment notices, media reports
- As of: July 2026

Current leadership (as of 2026-07):
  区委书记: 于波 (since 2022-07)
  区委副书记、区长: 叶大华 (since 2022-07)
  区委副书记: 刘瑞成
  区委常委、常务副区长: 丁章春
  区委常委、组织部部长: 管小丽 (female)
  区委常委、宣传部部长: 马红寰
  区委常委、纪委书记/监委主任: 杨新光
  区委常委、副区长: 苏礼华
  区委常委、统战部部长: 索轶军
  区委常委、政法委书记: 刘学龙
  副区长: 任江浩, 卫洪英 (female), 张佰军, 彭海宇
  区人大常委会主任: 吕桂富
  区政协主席: 张远

Predecessors:
  前任区委书记: 穆鹏 (2018 ~ 2022-07)
  前任区长: 于波 (2019-01 ~ 2022-07, 升任区委书记)

Relationships:
- 于波曾任延庆区长(2019-2022)→升任区委书记(2022)
- 叶大华曾任延庆区委副书记→升任区长(2022)
- 穆鹏→于波：区委书记前后任交接(2022)
- 于波→叶大华：区长前后任交接(2022)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "延庆区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "延庆区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子（现任） ──
    ("yq_yu_bo", "于波", "男", "汉族", "1969年10月", "北京延庆",
     "中央党校研究生/工学学士", "中共党员", "1992年7月",
     "区委书记", "中共北京市延庆区委员会",
     "bjyq.gov.cn;baidu.baike;media"),

    ("yq_ye_dahua", "叶大华", "男", "汉族", "1971年12月", "待查",
     "大学/管理学学士", "中共党员", "1994年7月",
     "区委副书记、区长", "北京市延庆区人民政府",
     "bjyq.gov.cn;baidu.baike;media"),

    ("yq_liu_ruicheng", "刘瑞成", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、党校校长", "中共北京市延庆区委员会",
     "bjyq.gov.cn;media"),

    ("yq_ding_zhangchun", "丁章春", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "北京市延庆区人民政府",
     "bjyq.gov.cn;media"),

    ("yq_guan_xiaoli", "管小丽", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市延庆区委组织部",
     "bjyq.gov.cn;media"),

    ("yq_ma_honghuan", "马红寰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市延庆区委宣传部",
     "bjyq.gov.cn;media"),

    ("yq_yang_xinguang", "杨新光", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共北京市延庆区纪律检查委员会",
     "bjyq.gov.cn;media"),

    ("yq_su_lihua", "苏礼华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长", "北京市延庆区人民政府",
     "bjyq.gov.cn;media"),

    ("yq_suo_yijun", "索轶军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共北京市延庆区委统战部",
     "bjyq.gov.cn;media"),

    ("yq_liu_xuelong", "刘学龙", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共北京市延庆区委政法委员会",
     "bjyq.gov.cn;media"),

    # ── 副区长（非常委身份） ──
    ("yq_ren_jianghao", "任江浩", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市延庆区人民政府",
     "bjyq.gov.cn;media"),

    ("yq_wei_hongying", "卫洪英", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市延庆区人民政府",
     "bjyq.gov.cn;media"),

    ("yq_zhang_baijun", "张佰军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市延庆区人民政府",
     "bjyq.gov.cn;media"),

    ("yq_peng_haiyu", "彭海宇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市延庆区人民政府",
     "bjyq.gov.cn;media"),

    # ── 人大、政协主要领导 ──
    ("yq_lv_guifu", "吕桂富", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "北京市延庆区人民代表大会常务委员会",
     "bjyq.gov.cn;media"),

    ("yq_zhang_yuan", "张远", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议北京市延庆区委员会",
     "bjyq.gov.cn;media"),

    # ── 前任领导 ──
    ("yq_mu_peng", "穆鹏", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原区委书记(已离任)", "中共北京市延庆区委员会(原)",
     "baidu.baike;media"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("org_yq_qw", "中共北京市延庆区委员会", "党委", "正厅级", "北京市委", "北京市延庆区"),
    ("org_yq_zf", "北京市延庆区人民政府", "政府", "正厅级", "北京市政府", "北京市延庆区"),
    ("org_yq_jw", "中共北京市延庆区纪律检查委员会", "党委", "副厅级", "北京市纪委监委", "北京市延庆区"),
    ("org_yq_zzb", "中共北京市延庆区委组织部", "党委", "正处级", "延庆区委", "北京市延庆区"),
    ("org_yq_xcb", "中共北京市延庆区委宣传部", "党委", "正处级", "延庆区委", "北京市延庆区"),
    ("org_yq_tyb", "中共北京市延庆区委统战部", "党委", "正处级", "延庆区委", "北京市延庆区"),
    ("org_yq_zfw", "中共北京市延庆区委政法委员会", "党委", "正处级", "延庆区委", "北京市延庆区"),
    ("org_yq_rd", "北京市延庆区人民代表大会常务委员会", "人大", "正厅级", "北京市人大", "北京市延庆区"),
    ("org_yq_zx", "中国人民政治协商会议北京市延庆区委员会", "政协", "正厅级", "北京市政协", "北京市延庆区"),
    ("org_yq_yqy", "中关村科技园区延庆园", "开发区", "正处级", "延庆区政府", "北京市延庆区"),
]

POSITIONS = [
    # ── 区委班子（现任） ──
    ("yq_yu_bo", "org_yq_qw", "区委书记", "2022-07", "present", "正厅级", "接替穆鹏"),
    ("yq_ye_dahua", "org_yq_zf", "区长", "2022-07", "present", "正厅级", "由代区长转正"),
    ("yq_ye_dahua", "org_yq_qw", "区委副书记", "2022-03", "present", "正厅级", ""),
    ("yq_liu_ruicheng", "org_yq_qw", "区委副书记", "待查", "present", "副厅级", "兼任区委党校校长"),
    ("yq_ding_zhangchun", "org_yq_zf", "常务副区长", "待查", "present", "副厅级", "区委常委"),
    ("yq_guan_xiaoli", "org_yq_zzb", "组织部部长", "待查", "present", "正处级", "区委常委"),
    ("yq_ma_honghuan", "org_yq_xcb", "宣传部部长", "待查", "present", "正处级", "区委常委"),
    ("yq_yang_xinguang", "org_yq_jw", "纪委书记、监委主任", "待查", "present", "副厅级", "区委常委"),
    ("yq_su_lihua", "org_yq_zf", "副区长", "待查", "present", "副厅级", "区委常委"),
    ("yq_suo_yijun", "org_yq_tyb", "统战部部长", "待查", "present", "正处级", "区委常委"),
    ("yq_liu_xuelong", "org_yq_zfw", "政法委书记", "待查", "present", "正处级", "区委常委"),
    ("yq_ren_jianghao", "org_yq_zf", "副区长", "待查", "present", "副厅级", ""),
    ("yq_wei_hongying", "org_yq_zf", "副区长", "待查", "present", "副厅级", ""),
    ("yq_zhang_baijun", "org_yq_zf", "副区长", "待查", "present", "副厅级", ""),
    ("yq_peng_haiyu", "org_yq_zf", "副区长", "待查", "present", "副厅级", ""),
    ("yq_lv_guifu", "org_yq_rd", "区人大常委会主任", "待查", "present", "正厅级", ""),
    ("yq_zhang_yuan", "org_yq_zx", "区政协主席", "待查", "present", "正厅级", ""),

    # ── 前任领导 ──
    ("yq_mu_peng", "org_yq_qw", "区委书记", "2018", "2022-07", "正厅级", "接替待查"),
    ("yq_yu_bo", "org_yq_zf", "区长", "2019-01", "2022-07", "正厅级", "由代区长转正；升任区委书记"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period, confidence)

    # 前后任关系
    ("yq_mu_peng", "yq_yu_bo", "predecessor_successor",
     "穆鹏2022年7月不再担任区委书记，于波接任",
     "中共北京市延庆区委员会", "2022-07", "confirmed"),

    ("yq_yu_bo", "yq_ye_dahua", "predecessor_successor",
     "于波2022年7月升任区委书记，叶大华接任区长",
     "北京市延庆区人民政府", "2022-07", "confirmed"),

    # 现任班子内部的上下级/共事关系
    ("yq_yu_bo", "yq_ye_dahua", "superior_subordinate",
     "于波任区委书记，叶大华任区委副书记、区长",
     "中共北京市延庆区委员会", "2022-07~present", "confirmed"),

    ("yq_yu_bo", "yq_liu_ruicheng", "superior_subordinate",
     "于波任区委书记，刘瑞成任区委副书记",
     "中共北京市延庆区委员会", "待查~present", "confirmed"),

    ("yq_ye_dahua", "yq_liu_ruicheng", "overlap",
     "叶大华任区委副书记、区长，刘瑞成任区委副书记",
     "中共北京市延庆区委员会", "待查~present", "confirmed"),

    ("yq_yu_bo", "yq_ding_zhangchun", "superior_subordinate",
     "于波任区委书记，丁章春任常务副区长",
     "中共北京市延庆区委员会", "待查~present", "confirmed"),

    ("yq_yu_bo", "yq_yang_xinguang", "superior_subordinate",
     "于波任区委书记，杨新光任区纪委书记",
     "中共北京市延庆区委员会", "待查~present", "confirmed"),

    ("yq_ye_dahua", "yq_su_lihua", "superior_subordinate",
     "叶大华任区长，苏礼华任副区长",
     "北京市延庆区人民政府", "待查~present", "confirmed"),

    # 于波"区长→书记"晋升路径
    ("yq_yu_bo", "yq_mu_peng", "superior_subordinate",
     "于波任区长期间，穆鹏任区委书记",
     "中共北京市延庆区委员会/延庆区人民政府", "2019-01~2022-07", "confirmed"),

    # 共事关系（同一班子成员）
    ("yq_ding_zhangchun", "yq_su_lihua", "overlap",
     "丁章春任常务副区长，苏礼华任副区长，同为区政府班子成员",
     "北京市延庆区人民政府", "待查~present", "plausible"),

    ("yq_guan_xiaoli", "yq_ma_honghuan", "overlap",
     "管小丽任组织部部长，马红寰任宣传部部长，同为区委常委",
     "中共北京市延庆区委员会", "待查~present", "confirmed"),

    ("yq_yang_xinguang", "yq_liu_xuelong", "overlap",
     "杨新光任区纪委书记，刘学龙任政法委书记，同为区委常委",
     "中共北京市延庆区委员会", "待查~present", "confirmed"),

    ("yq_suo_yijun", "yq_liu_xuelong", "overlap",
     "索轶军任统战部部长，刘学龙任政法委书记，同为区委常委",
     "中共北京市延庆区委员会", "待查~present", "plausible"),
]


# ════════════════════════════════════════════
# BUILD SQLite DATABASE
# ════════════════════════════════════════════

def build_database():
    """Create and populate the SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
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
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    c.executemany(
        "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        PERSONS
    )
    c.executemany(
        "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
        ORGANIZATIONS
    )
    c.executemany(
        "INSERT INTO positions(person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
        POSITIONS
    )
    c.executemany(
        "INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?,?,?,?,?,?,?)",
        RELATIONSHIPS
    )

    conn.commit()
    conn.close()
    print(f"  Database created: {DB_PATH}")

# ════════════════════════════════════════════
# BUILD GEXF GRAPH
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id):
    """Return 'r,g,b' color string for a person node based on role."""
    role_map = {
        "yq_yu_bo":       "255,50,50",    # party secretary - red
        "yq_ye_dahua":    "50,100,255",   # mayor - blue
        "yq_mu_peng":     "255,50,50",    # former secretary - red
        "yq_yang_xinguang": "255,165,0",  # discipline inspection - orange
    }
    return role_map.get(person_id, "100,100,100")

def is_top_leader(person_id):
    return person_id in ("yq_yu_bo", "yq_ye_dahua", "yq_mu_peng")

def org_color(org_type):
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
    }
    return color_map.get(org_type, "200,200,200")

def build_gexf():
    """Generate GEXF XML using string formatting (not ElementTree) to avoid namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>北京市延庆区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('      <attribute id="4" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    # Person nodes
    for p in PERSONS:
        pid, name, gender, eth, birth, bp, edu, party, ws, post, org, src = p
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        label_display = f"{name}\\n{post}"
        lines.append(f'      <node id="{pid}" label="{esc(label_display)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(name)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="4" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(name)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    # Person→Organization (worked_at) edges
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person (relationship) edges
    for rel in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period, confidence = rel
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(confidence)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF graph created: {GEXF_PATH}")

# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

def main():
    print("Building 延庆区 leadership network data...")
    build_database()
    build_gexf()
    print("Done.")

if __name__ == "__main__":
    main()
