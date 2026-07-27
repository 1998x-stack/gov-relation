#!/usr/bin/env python3
"""Build 赛罕区 leadership network database and GEXF graph.

Data sourced from the official 赛罕区人民政府 website (www.saihan.gov.cn)
领导之窗 page as of 2026-07-25.

Sources:
  - S001: http://www.saihan.gov.cn/zwgk_new/ldzc/
  - S002: http://www.saihan.gov.cn/zwgk_new/ldzc/zf/202508/t20250829_1926810.html

Usage: python3 scripts/build/build_赛罕区_data.py
"""

import sqlite3
import os

# ── Paths ────────────────────────────────────────────────────────────
SLUG = "赛罕区"
# Resolve repo root: this file is at data/tmp/<task_id>/build_...
# The repo root is 3 directories up from the script when in staging,
# or 2 directories up when in scripts/build/
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir.endswith("/scripts/build") or _script_dir.endswith("\\scripts\\build"):
    ROOT = os.path.dirname(os.path.dirname(_script_dir))
else:
    # In staging: data/tmp/<task_id>/ -> go up 3 levels
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_script_dir)))
DB_PATH = os.path.join(ROOT, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(ROOT, "data", "graph", f"{SLUG}_network.gexf")
TODAY = "2026-07-25"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    (1, "殷树刚", "男", "汉族", "", "", "", "", "", "赛罕区委书记", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (2, "杨朋飞", "男", "汉族", "1985年7月", "", "研究生，农学硕士", "中共党员", "", "赛罕区委副书记、政府党组书记、区长，航天经济开发区党工委书记", "赛罕区人民政府", "赛罕区人民政府官网 政府领导"),
    (3, "刘涛", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (4, "孙继斌", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (5, "杨聪林", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (6, "刘卿", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (7, "李赞峰", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (8, "王文涛", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (9, "郭文英", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (10, "高敏捷", "", "", "", "", "", "", "", "区委领导", "中共呼和浩特市赛罕区委员会", "赛罕区人民政府官网 领导之窗"),
    (11, "赵胜利", "", "", "", "", "", "", "", "政府副区长", "赛罕区人民政府", "赛罕区人民政府官网 领导之窗"),
    (12, "张乙宁", "", "", "", "", "", "", "", "政府副区长", "赛罕区人民政府", "赛罕区人民政府官网 领导之窗"),
    (13, "石颜博", "", "", "", "", "", "", "", "政府副区长", "赛罕区人民政府", "赛罕区人民政府官网 领导之窗"),
    (14, "马斌", "", "", "", "", "", "", "", "政府副区长", "赛罕区人民政府", "赛罕区人民政府官网 领导之窗"),
    (15, "刘天梅", "", "", "", "", "", "", "", "政府领导", "赛罕区人民政府", "赛罕区人民政府官网 领导之窗"),
    (16, "张俊耀", "", "", "", "", "", "", "", "区人大常委会党组书记、主任", "赛罕区人大常委会", "赛罕区人民政府官网 领导之窗"),
    (17, "徐玲玲", "", "", "", "", "", "", "", "区人大常委会副主任", "赛罕区人大常委会", "赛罕区人民政府官网 领导之窗"),
    (18, "刘踔斌", "", "", "", "", "", "", "", "区人大常委会副主任", "赛罕区人大常委会", "赛罕区人民政府官网 领导之窗"),
    (19, "刘亚林", "", "", "", "", "", "", "", "区人大常委会副主任", "赛罕区人大常委会", "赛罕区人民政府官网 领导之窗"),
    (20, "贾晋峰", "", "", "", "", "", "", "", "区政协党组书记、主席", "赛罕区政协", "赛罕区人民政府官网 领导之窗"),
    (21, "郑华", "", "", "", "", "", "", "", "区政协副主席", "赛罕区政协", "赛罕区人民政府官网 领导之窗"),
    (22, "刘鹏", "", "", "", "", "", "", "", "区政协副主席", "赛罕区政协", "赛罕区人民政府官网 领导之窗"),
    (23, "王俊伟", "", "", "", "", "", "", "", "区政协副主席", "赛罕区政协", "赛罕区人民政府官网 领导之窗"),
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    (1, "中共呼和浩特市赛罕区委员会", "党委", "县处级", "中共呼和浩特市委员会", "呼和浩特市赛罕区"),
    (2, "赛罕区人民政府", "政府", "县处级", "呼和浩特市人民政府", "呼和浩特市赛罕区"),
    (3, "赛罕区人大常委会", "人大", "县处级", "呼和浩特市人大常委会", "呼和浩特市赛罕区"),
    (4, "赛罕区政协", "政协", "县处级", "呼和浩特市政协", "呼和浩特市赛罕区"),
    (5, "呼和浩特航天经济开发区", "开发区", "县处级", "呼和浩特市人民政府", "呼和浩特市"),
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    (1, 1, "赛罕区委书记", "", "present", "正处级", ""),
    (2, 2, "赛罕区委副书记、区长", "", "present", "正处级", ""),
    (2, 5, "航天经济开发区党工委书记", "", "present", "", "兼任"),
    (3, 1, "区委领导", "", "present", "副处级", ""),
    (4, 1, "区委领导", "", "present", "副处级", ""),
    (5, 1, "区委领导", "", "present", "副处级", ""),
    (6, 1, "区委领导", "", "present", "副处级", ""),
    (7, 1, "区委领导", "", "present", "副处级", ""),
    (8, 1, "区委领导", "", "present", "副处级", ""),
    (9, 1, "区委领导", "", "present", "副处级", ""),
    (10, 1, "区委领导", "", "present", "副处级", ""),
    (5, 2, "政府副区长", "", "present", "副处级", "杨聪林兼任"),
    (7, 2, "政府副区长", "", "present", "副处级", "李赞峰兼任"),
    (11, 2, "政府副区长", "", "present", "副处级", ""),
    (12, 2, "政府副区长", "", "present", "副处级", ""),
    (13, 2, "政府副区长", "", "present", "副处级", ""),
    (14, 2, "政府副区长", "", "present", "副处级", ""),
    (15, 2, "政府领导", "", "present", "副处级", ""),
    (16, 3, "区人大常委会党组书记、主任", "", "present", "正处级", ""),
    (17, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (18, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (19, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (20, 4, "区政协党组书记、主席", "", "present", "正处级", ""),
    (21, 4, "区政协副主席", "", "present", "副处级", ""),
    (22, 4, "区政协副主席", "", "present", "副处级", ""),
    (23, 4, "区政协副主席", "", "present", "副处级", ""),
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    (1, 2, "overlap", "赛罕区党政一把手", "中共呼和浩特市赛罕区委员会 / 赛罕区人民政府", "present"),
    (1, 16, "overlap", "区委—人大 领导关系", "赛罕区四套班子", "present"),
    (2, 16, "overlap", "政府—人大 领导关系", "赛罕区四套班子", "present"),
    (1, 20, "overlap", "区委—政协 领导关系", "赛罕区四套班子", "present"),
    (2, 20, "overlap", "政府—政协 领导关系", "赛罕区四套班子", "present"),
    (5, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (5, 2, "superior_subordinate", "副区长—区长 上下级关系", "赛罕区人民政府", "present"),
    (7, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (7, 2, "superior_subordinate", "副区长—区长 上下级关系", "赛罕区人民政府", "present"),
    (3, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (4, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (6, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (8, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (9, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (10, 1, "superior_subordinate", "区委领导—区委书记 上下级关系", "中共呼和浩特市赛罕区委员会", "present"),
    (11, 2, "superior_subordinate", "副区长—区长 上下级关系", "赛罕区人民政府", "present"),
    (12, 2, "superior_subordinate", "副区长—区长 上下级关系", "赛罕区人民政府", "present"),
    (13, 2, "superior_subordinate", "副区长—区长 上下级关系", "赛罕区人民政府", "present"),
    (14, 2, "superior_subordinate", "副区长—区长 上下级关系", "赛罕区人民政府", "present"),
    (15, 2, "superior_subordinate", "政府领导—区长 上下级关系", "赛罕区人民政府", "present"),
]


# ── Helpers ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


_ORG_COLORS = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
               "政协": "255,240,200", "开发区": "200,255,200", "default": "200,200,200"}


def person_color(post):
    if "书记" in post and "副" not in post:
        return "200,30,30"
    if ("区长" in post and "副" not in post) or ("县长" in post and "副" not in post):
        return "30,100,200"
    if "人大" in post or "政协" in post:
        return "60,180,60"
    if "副" in post:
        return "100,150,220"
    return "180,180,180"


def person_size(post):
    if ("书记" in post and "副" not in post) or ("区长" in post and "副" not in post):
        return "20.0"
    return "12.0"


# ── SQLite ────────────────────────────────────────────────────────────

def build_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for t in ("relationships", "positions", "organizations", "persons"):
        c.execute(f"DROP TABLE IF EXISTS {t}")
    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")
    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)
    conn.commit()
    conn.close()
    print(f"DB ready: {DB_PATH}")
    print(f"  persons={len(persons)}, orgs={len(organizations)}, pos={len(positions)}, rel={len(relationships)}")


# ── GEXF ──────────────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子关系网络图</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid, name = p[0], p[1]
        post, org, source = p[9], p[10], p[11]
        c = person_color(post)
        sz = person_size(post)
        r, g, b = c.split(",")
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(source)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid, oname, otype = o[0], o[1], o[2]
        oc = _ORG_COLORS.get(otype, _ORG_COLORS["default"])
        r, g, b = oc.split(",")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── edges ──
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid, oid, title = pos[0], pos[1], pos[2]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        pa, pb, rtype, ctx, oo, op = r
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oo)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(op)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF ready: {GEXF_PATH}")


def main():
    build_database()
    build_gexf()


if __name__ == "__main__":
    main()
