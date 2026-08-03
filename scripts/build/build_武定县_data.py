#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Wuding County leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
TODAY = "2026-08-03"
SLUG = "武定县"

# Staging paths
STAGING_DIR = os.path.join(BASE, "tmp", f"yunnan_{SLUG}")
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current County Party Secretary ──
    {"id": 1, "name": "代淳志", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共武定县委书记", "current_org": "中共武定县委员会",
     "source": "https://www.ynwd.gov.cn/info/1040/346301.htm"},

    # ── Current County Mayor ──
    {"id": 2, "name": "沈海燕", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-07", "birthplace": "", "education": "",
     "party_join": "2002-06", "work_start": "2003-12",
     "current_post": "武定县委副书记、县人民政府县长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41761.htm"},

    # ── Deputy Party Secretary ──
    {"id": 3, "name": "潘德志", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "武定县委副书记", "current_org": "中共武定县委员会",
     "source": "https://www.ynwd.gov.cn/info/1040/346041.htm"},

    # ── Standing Committee / Government Leaders ──
    {"id": 4, "name": "刘海东", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-06", "birthplace": "", "education": "",
     "party_join": "1999-12", "work_start": "2002-12",
     "current_post": "武定县委常委、县人民政府常务副县长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41766.htm"},

    {"id": 5, "name": "孙道坤", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-09", "birthplace": "", "education": "",
     "party_join": "2004-09", "work_start": "2002-12",
     "current_post": "武定县委常委、县人民政府副县长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41764.htm"},

    {"id": 6, "name": "徐建荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-08", "birthplace": "", "education": "",
     "party_join": "2012-07", "work_start": "2004-07",
     "current_post": "武定县委常委、县人民政府副县长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41765.htm"},

    {"id": 7, "name": "宋春宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-01", "birthplace": "", "education": "",
     "party_join": "2008-08", "work_start": "2006-08",
     "current_post": "武定县委常委、县人民政府副县长、武定产业园区管委会副主任", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/45913.htm"},

    # ── Deputy County Mayors ──
    {"id": 8, "name": "杨艳", "gender": "女", "ethnicity": "彝族",
     "birth": "1980-09", "birthplace": "", "education": "",
     "party_join": "2006-12", "work_start": "2004-12",
     "current_post": "武定县人民政府副县长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41769.htm"},

    {"id": 9, "name": "周学强", "gender": "男", "ethnicity": "彝族",
     "birth": "1979-12", "birthplace": "", "education": "",
     "party_join": "2002-04", "work_start": "2003-12",
     "current_post": "武定县人民政府副县长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41762.htm"},

    {"id": 10, "name": "夏文贵", "gender": "男", "ethnicity": "彝族",
     "birth": "1979-08", "birthplace": "", "education": "",
     "party_join": "2001-12", "work_start": "2000-08",
     "current_post": "武定县人民政府副县长、县公安局局长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41763.htm"},

    {"id": 11, "name": "刘彬杉", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-03", "birthplace": "", "education": "",
     "party_join": "", "work_start": "2000-08",
     "current_post": "武定县人民政府副县长", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41767.htm"},

    {"id": 12, "name": "孟国栋", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-06", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "武定县人民政府副县长（挂职）", "current_org": "武定县人民政府",
     "source": "https://www.ynwd.gov.cn/info/2501/41771.htm"},

    # ── Government Office ──
    {"id": 13, "name": "祖正文", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-04", "birthplace": "", "education": "",
     "party_join": "2006-03", "work_start": "2003-12",
     "current_post": "武定县人民政府党组成员、办公室主任", "current_org": "武定县人民政府办公室",
     "source": "https://www.ynwd.gov.cn/info/2501/41770.htm"},

    # ── 四套班子 Leaders ──
    {"id": 14, "name": "普正祥", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "武定县人大常委会主任", "current_org": "武定县人大常委会",
     "source": "https://www.ynwd.gov.cn/info/1040/346041.htm"},

    {"id": 15, "name": "周廷质", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "武定县政协主席", "current_org": "武定县政协",
     "source": "https://www.ynwd.gov.cn/info/1040/346041.htm"},
]

organizations = [
    {"id": 1, "name": "中共武定县委员会", "type": "党委", "level": "县级",
     "parent": "中共楚雄彝族自治州委员会", "location": "云南省楚雄州武定县"},
    {"id": 2, "name": "武定县人民政府", "type": "政府", "level": "县级",
     "parent": "楚雄彝族自治州人民政府", "location": "云南省楚雄州武定县"},
    {"id": 3, "name": "武定县人大常委会", "type": "人大", "level": "县级",
     "parent": "", "location": "云南省楚雄州武定县"},
    {"id": 4, "name": "武定县政协", "type": "政协", "level": "县级",
     "parent": "", "location": "云南省楚雄州武定县"},
    {"id": 5, "name": "武定县人民政府办公室", "type": "政府", "level": "县级",
     "parent": "武定县人民政府", "location": "云南省楚雄州武定县"},
    {"id": 6, "name": "武定产业园区管委会", "type": "开发区", "level": "县级",
     "parent": "武定县人民政府", "location": "云南省楚雄州武定县"},
    {"id": 7, "name": "武定县公安局", "type": "政法机关", "level": "县级",
     "parent": "武定县人民政府", "location": "云南省楚雄州武定县"},
]

positions = [
    # 代淳志
    {"person_id": 1, "org_id": 1, "title": "中共武定县委书记",
     "start_date": "2026", "end_date": "present", "rank": "正处级",
     "note": "十六届武定县委书记，2026年就任"},

    # 沈海燕
    {"person_id": 2, "org_id": 2, "title": "武定县人民政府县长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "县委副书记、县长、党组书记"},
    {"person_id": 2, "org_id": 1, "title": "武定县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "县委副书记"},

    # 潘德志
    {"person_id": 3, "org_id": 1, "title": "武定县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年7月在职"},

    # 刘海东
    {"person_id": 4, "org_id": 2, "title": "武定县委常委、常务副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "党组副书记、县行政学校校长"},
    {"person_id": 4, "org_id": 1, "title": "武定县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "十六届县委常委"},

    # 孙道坤
    {"person_id": 5, "org_id": 2, "title": "武定县委常委、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 5, "org_id": 1, "title": "武定县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "十六届县委常委"},

    # 徐建荣
    {"person_id": 6, "org_id": 2, "title": "武定县委常委、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 6, "org_id": 1, "title": "武定县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "十六届县委常委"},

    # 宋春宇
    {"person_id": 7, "org_id": 2, "title": "武定县委常委、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "武定产业园区管委会分管日常工作的副主任"},
    {"person_id": 7, "org_id": 1, "title": "武定县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "十六届县委常委"},
    {"person_id": 7, "org_id": 6, "title": "武定产业园区管委会副主任",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "分管日常工作的副主任"},

    # 杨艳
    {"person_id": 8, "org_id": 2, "title": "武定县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 周学强
    {"person_id": 9, "org_id": 2, "title": "武定县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 夏文贵
    {"person_id": 10, "org_id": 2, "title": "武定县人民政府副县长、县公安局局长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 10, "org_id": 7, "title": "武定县公安局局长",
     "start_date": "", "end_date": "present", "rank": "",
     "note": ""},

    # 刘彬杉
    {"person_id": 11, "org_id": 2, "title": "武定县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 孟国栋（挂职）
    {"person_id": 12, "org_id": 2, "title": "武定县人民政府副县长（挂职）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "招商银行挂职干部"},

    # 祖正文
    {"person_id": 13, "org_id": 5, "title": "武定县人民政府办公室主任",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "县政府党组成员"},

    # 普正祥
    {"person_id": 14, "org_id": 3, "title": "武定县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": ""},

    # 周廷质
    {"person_id": 15, "org_id": 4, "title": "武定县政协主席",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "县委书记与县长搭档", "overlap_org": "武定县四班子",
     "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "colleague",
     "context": "县委书记与副书记搭档", "overlap_org": "中共武定县委员会",
     "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "县长与副书记在县委常委会共事", "overlap_org": "中共武定县委常委会",
     "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长", "overlap_org": "武定县人民政府",
     "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "colleague",
     "context": "同为县委常委、县政府领导", "overlap_org": "武定县委常委班子、武定县人民政府",
     "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "colleague",
     "context": "同为县委常委、县政府领导", "overlap_org": "武定县委常委班子、武定县人民政府",
     "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "colleague",
     "context": "同为县委常委、县政府领导", "overlap_org": "武定县委常委班子、武定县人民政府",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "colleague",
     "context": "县委与县人大领导", "overlap_org": "武定县四班子",
     "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 15, "type": "colleague",
     "context": "县委与县政协领导", "overlap_org": "武定县四班子",
     "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "colleague",
     "context": "县政府与县人大领导", "overlap_org": "武定县四班子",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "colleague",
     "context": "县政府与县政协领导", "overlap_org": "武定县四班子",
     "overlap_period": ""},
]


# ── BUILD ────────────────────────────────────────────────────────────

def main():
    import os
    os.makedirs(STAGING_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

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

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- 构建 GEXF 图文件 ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post and "副书记" not in post:
            return ("255,50,50", 20.0)   # Red
        elif "县长" in post and "副" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "副书记" in post:
            return ("100,100,255", 15.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post:
            return ("100,100,255", 15.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "政协主席" in post:
            return ("255,240,200", 15.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
            "开发区": ("200,255,200"),
            "政法机关": ("200,200,200"),
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
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        c_vals = c.split(",")
        lines.append(f'        <viz:color r="{c_vals[0]}" g="{c_vals[1]}" b="{c_vals[2]}"/>')
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
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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
    main()