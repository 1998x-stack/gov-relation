#!/usr/bin/env python3
"""元宝区领导班子工作关系网络 — 辽宁省丹东市元宝区"""

import sqlite3
from datetime import datetime

SLUG = "元宝区"
TODAY = datetime.now().strftime("%Y-%m-%d")
DB_PATH = "data/tmp/liaoning_元宝区/元宝区_network.db"
GEXF_PATH = "data/tmp/liaoning_元宝区/元宝区_network.gexf"

# ═══════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════

persons = [
    # id, name, gender, ethnicity, birth, birthplace, education,
    #    party_join, work_start, current_post, current_org, source
    [1, "赵洪绪", "男", "汉族", "", "", "",
     "", "", "区委书记", "中共元宝区委",
     "https://www.yuanbao.gov.cn (元宝区政府网站 2026-07-07 防汛报道)"],
    [2, "夏昌海", "男", "汉族", "", "", "",
     "", "", "区委副书记、区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn (元宝区政府网站 2026-01-15/07-14/07-08 多篇报道)"],
    [3, "高琨", "男", "", "", "", "",
     "", "", "区人大常委会主任", "元宝区人大常委会",
     "https://www.yuanbao.gov.cn 2026-06-25 全区警示教育会报道"],
    [4, "张瑞杰", "男", "", "", "", "",
     "", "", "区政协主席", "元宝区政协",
     "https://www.yuanbao.gov.cn 2026-06-25 全区警示教育会报道"],
    [5, "王丽", "女", "", "", "", "",
     "", "", "区政府副区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn 2025-10-29 区政府常务会议报道"],
    [6, "马晓冬", "男", "", "", "", "",
     "", "", "区政府副区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn 2025-10-29 区政府常务会议报道"],
    [7, "王宪滨", "男", "", "", "", "",
     "", "", "区政府副区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn 2025-10-29/2026-07-07 区政府会议报道"],
    [8, "孟庆舜", "男", "", "", "", "",
     "", "", "区政府副区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn 2025-10-29 区政府常务会议报道"],
    [9, "王慧", "男", "", "", "", "",
     "", "", "区委常委、政法委书记", "中共元宝区委政法委",
     "https://www.yuanbao.gov.cn 2026-01-12 夏昌海走访慰问公安报道"],
    [10, "徐振利", "男", "", "", "", "",
     "", "", "区政府副区长（公安分局局长）", "丹东市公安局元宝分局",
     "https://www.yuanbao.gov.cn 2026-01-12 夏昌海走访慰问公安报道"],
    [11, "吕文明", "男", "", "", "", "",
     "", "", "区委常委", "中共元宝区委",
     "https://www.yuanbao.gov.cn 2025-10-29 重阳慰问报道"],
    [12, "蒋露", "女", "", "", "", "",
     "", "", "区政府副区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn 元政发〔2026〕2号 2026-04 任职通知"],
    [13, "王丹扬", "男", "", "", "", "",
     "", "", "原副区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn 元政发〔2026〕4号 2026-07-21 免职通知"],
    [14, "辛德成", "男", "", "", "", "",
     "", "", "原副区长", "元宝区人民政府",
     "https://www.yuanbao.gov.cn 元政发〔2026〕6号 2026-07-22 免职通知"],
]

organizations = [
    # id, name, type, level, parent, location
    [1, "中共元宝区委", "党委", "市辖区", "中共丹东市委", "辽宁省丹东市元宝区"],
    [2, "元宝区人民政府", "政府", "市辖区", "丹东市人民政府", "辽宁省丹东市元宝区"],
    [3, "元宝区人大常委会", "人大", "市辖区", "丹东市人大常委会", "辽宁省丹东市元宝区"],
    [4, "元宝区政协", "政协", "市辖区", "政协丹东市委员会", "辽宁省丹东市元宝区"],
    [5, "中共元宝区委政法委", "党委", "市辖区", "中共元宝区委", "辽宁省丹东市元宝区"],
    [6, "丹东市公安局元宝分局", "政府", "市辖区", "丹东市公安局", "辽宁省丹东市元宝区"],
]

positions = [
    # person_id, org_id, title, start_date, end_date, rank, note
    [1, 1, "区委书记", "", "", "正处级", "2026年7月仍在任"],
    [2, 2, "区委副书记、区长", "", "", "正处级", "2026年7月仍在任"],
    [3, 3, "区人大常委会主任", "", "", "正处级", "2026年6月仍在任"],
    [4, 4, "区政协主席", "", "", "正处级", "2026年6月仍在任"],
    [5, 2, "副区长", "", "", "副处级", "2025年10月仍在任"],
    [6, 2, "副区长", "", "", "副处级", "2025年10月仍在任"],
    [7, 2, "副区长", "", "", "副处级", "2026年7月仍在任"],
    [8, 2, "副区长", "", "", "副处级", "2025年10月仍在任"],
    [9, 5, "区委常委、政法委书记", "", "", "副处级", "2026年1月仍在任"],
    [10, 6, "副区长兼公安分局局长", "", "", "副处级", "2026年1月仍在任"],
    [11, 1, "区委常委", "", "", "副处级", "2025年10月仍在任"],
    [12, 2, "副区长", "", "", "副处级", "2026年4月任职"],
    [13, 2, "副区长", "", "", "副处级", "2026年7月免职"],
    [14, 2, "副区长", "", "", "副处级", "2026年7月免职"],
]

relationships = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    [1, 2, "搭档", "区委书记与区长党政搭档", "元宝区委/区政府", "2025-2026"],
    [2, 5, "上下级", "区长与副区长", "元宝区人民政府", "2025-2026"],
    [2, 6, "上下级", "区长与副区长", "元宝区人民政府", "2025-2026"],
    [2, 7, "上下级", "区长与副区长", "元宝区人民政府", "2025-2026"],
    [2, 8, "上下级", "区长与副区长", "元宝区人民政府", "2025-2026"],
    [2, 12, "上下级", "区长与新任副区长", "元宝区人民政府", "2026-"],
]


# ═══════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
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
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 元宝区人民政府网站 (yuanbao.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p[i] if i < len(p) else "" for i in range(len(cols_p))]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o[i] if i < len(o) else "" for i in range(len(cols_o))]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos[i] if i < len(pos) else "" for i in range(len(cols_pos))]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r[i] if i < len(r) else "" for i in range(len(cols_r))]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "区委书记" in post:
            return ("255,50,50", 20.0)
        elif "区长" in post and "副" not in post:
            return ("50,100,255", 20.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "政协主席" in post:
            return ("255,240,200", 15.0)
        elif "副区长" in post or "原副区长" in post or "原" in post:
            return ("100,100,255", 12.0)
        elif "政法委" in post:
            return ("255,165,0", 12.0)
        elif "公安" in post:
            return ("100,100,100", 12.0)
        elif "常委" in post:
            return ("150,50,50", 12.0)
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
        c, sz = person_color(p[9])  # current_post
        lines.append(f'      <node id="p{p[0]}" label="{esc(p[1])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p[9])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p[10])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p[4])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p[11])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o[2])
        lines.append(f'      <node id="o{o[0]}" label="{esc(o[1])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[5])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r[2])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r[4])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r[5])}"/>')
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
