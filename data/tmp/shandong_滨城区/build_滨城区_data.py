#!/usr/bin/env python3
"""
滨城区 (Bincheng District, Binzhou City, Shandong Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-25
信息来源:
  - 滨城区人民政府网站 (bincheng.gov.cn)
  - 百度百科
  - 新闻报道
"""

import sqlite3
import os
from datetime import datetime

TODAY = "2026-07-25"
SLUG = "滨城区"
PROVINCE = "山东省"
PARENT_CITY = "滨州市"

# Paths relative to staging dir
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "滨城区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "滨城区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 区委书记 ──
    {
        "id": 1,
        "name": "单纪亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年6月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1998年7月",
        "current_post": "区委书记",
        "current_org": "中共滨城区委员会",
        "source": "https://baike.baidu.com/item/%E5%8D%95%E7%BA%AA%E4%BA%AE",
    },
    # ── 2. 区长 ──
    {
        "id": 2,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "滨城区人民政府",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 3. 区委副书记 ──
    {
        "id": 3,
        "name": "张洪柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区人大常委会主任",
        "current_org": "中共滨城区委员会/滨城区人大常委会",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 4. 区政协主席 (原区委副书记、曾任区委常委) ──
    {
        "id": 4,
        "name": "边洪芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "滨城区政协",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 5. 区委常委、副区长 (常务) ──
    {
        "id": 5,
        "name": "李一鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "中共滨城区委员会/滨城区人民政府",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 6. 区委常委 ──
    {
        "id": 6,
        "name": "刘晓兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共滨城区委员会",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 7. 区委常委、宣传部部长、统战部部长 ──
    {
        "id": 7,
        "name": "袁俊英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、统战部部长",
        "current_org": "中共滨城区委员会",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 8. 区委常委、纪委书记 ──
    {
        "id": 8,
        "name": "刘一兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记",
        "current_org": "中共滨城区纪律检查委员会",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 9. 区人大常委会副主任 ──
    {
        "id": 9,
        "name": "薛爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "滨城区人大常委会",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 10. 区人大常委会副主任 ──
    {
        "id": 10,
        "name": "张红辛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "滨城区人大常委会",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 11. 区人大常委会副主任 ──
    {
        "id": 11,
        "name": "丁云霄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "滨城区人大常委会",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 12. 副区长 ──
    {
        "id": 12,
        "name": "张旋",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "滨城区人民政府",
        "source": "https://www.bincheng.gov.cn/",
    },
    # ── 13. 前任区委书记 (单纪亮的前任) ──
    {
        "id": 13,
        "name": "白平和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共滨城区委员会",
        "source": "新闻报道",
    },
    # ── 14. 刘祖庆 ──
    {
        "id": 14,
        "name": "刘祖庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "滨城区人大常委会",
        "source": "https://www.bincheng.gov.cn/",
    },
]

organizations = [
    {"id": 1, "name": "中共滨城区委员会", "type": "党委", "level": "县级", "parent": "中共滨州市委员会", "location": "滨城区"},
    {"id": 2, "name": "滨城区人民政府", "type": "政府", "level": "县级", "parent": "滨州市人民政府", "location": "滨城区"},
    {"id": 3, "name": "滨城区人大常委会", "type": "人大", "level": "县级", "parent": "滨州市人大常委会", "location": "滨城区"},
    {"id": 4, "name": "滨城区政协", "type": "政协", "level": "县级", "parent": "政协滨州市委员会", "location": "滨城区"},
    {"id": 5, "name": "中共滨城区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共滨州市纪律检查委员会", "location": "滨城区"},
    {"id": 6, "name": "滨城区委宣传部", "type": "党委", "level": "县级", "parent": "中共滨城区委员会", "location": "滨城区"},
    {"id": 7, "name": "滨城区委统战部", "type": "党委", "level": "县级", "parent": "中共滨城区委员会", "location": "滨城区"},
]

positions = [
    # 单纪亮
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2021-12", "end_date": "present", "rank": "正县级", "note": "十届滨城区委书记"},
    # 李刚
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "区委副书记、区长"},
    # 张洪柱
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "区关工委主任"},
    # 边洪芳
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 李一鸣
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "常务副区长"},
    # 刘晓兵
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 袁俊英
    {"person_id": 7, "org_id": 6, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "区委常委、宣传部部长、统战部部长"},
    {"person_id": 7, "org_id": 7, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘一兵
    {"person_id": 8, "org_id": 5, "title": "区纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "区委常委、纪委书记"},
    # 薛爱民
    {"person_id": 9, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张红辛
    {"person_id": 10, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 丁云霄
    {"person_id": 11, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张旋
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 白平和 - 前任区委书记
    {"person_id": 13, "org_id": 1, "title": "前任区委书记", "start_date": "", "end_date": "2021-12", "rank": "正县级", "note": "滨城区前任区委书记"},
    # 刘祖庆
    {"person_id": 14, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
]

relationships = [
    # 单纪亮 — 李刚 (党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长搭班子", "overlap_org": "中共滨城区委员会/滨城区人民政府", "overlap_period": "2021-至今"},
    # 单纪亮 — 张洪柱 (书记与副书记)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委副书记搭班子", "overlap_org": "中共滨城区委员会", "overlap_period": "至今"},
    # 单纪亮 — 白平和 (前后任)
    {"person_a": 1, "person_b": 13, "type": "前后任", "context": "单纪亮接替白平和任区委书记", "overlap_org": "中共滨城区委员会", "overlap_period": "2021-12交接"},
    # 李刚 — 张洪柱 (区长与副书记)
    {"person_a": 2, "person_b": 3, "type": "党政副职", "context": "区长与区委副书记在区委常委会共事", "overlap_org": "中共滨城区委员会", "overlap_period": "至今"},
    # 张洪柱 — 边洪芳 (副书记与政协主席)
    {"person_a": 3, "person_b": 4, "type": "同级", "context": "同为区级领导", "overlap_org": "滨城区", "overlap_period": "至今"},
    # 李一鸣 — 袁俊英 (常委同僚)
    {"person_a": 5, "person_b": 7, "type": "常委同僚", "context": "同届区委常委", "overlap_org": "中共滨城区委员会", "overlap_period": "至今"},
    # 刘一兵 — 单纪亮 (纪委与书记)
    {"person_a": 8, "person_b": 1, "type": "上下级", "context": "纪委书记受区委书记领导", "overlap_org": "中共滨城区委员会", "overlap_period": "至今"},
    # 张旋 — 李刚 (副区长与区长)
    {"person_a": 12, "person_b": 2, "type": "上下级", "context": "副区长协助区长工作", "overlap_org": "滨城区人民政府", "overlap_period": "至今"},
    # 张旋 — 袁俊英 (宣传相关工作)
    {"person_a": 12, "person_b": 7, "type": "工作协作", "context": "参与黄河大集等宣传活动", "overlap_org": "滨城区", "overlap_period": "至今"},
]


# ═══════════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 滨城区人民政府网站 (bincheng.gov.cn) 及新闻报道")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        if "区委书记" in post and "前任" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "区长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "区委副书记" in post:
            return ("150,50,50", 15.0)
        elif "区政协主席" in post:
            return ("255,240,200", 15.0)
        elif "区人大常委会主任" in post and "副" not in post:
            return ("200,255,255", 15.0)
        elif "人大常委会" in post:
            return ("200,255,255", 12.0)
        elif "纪委书记" in post:
            return ("255,165,0", 12.0)  # Orange
        elif "区委常委" in post:
            return ("100,150,255", 12.0)
        elif "副区长" in post:
            return ("100,100,255", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)  # Grey, past
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
            f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
            f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()
