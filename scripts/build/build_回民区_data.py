#!/usr/bin/env python3
"""Build 回民区 (Hohhot 市辖区, Inner Mongolia) leadership network database and GEXF graph.

Data sourced from the official 回民区人民政府 website (www.huiminqu.gov.cn) 领导之窗
pages, cross-referenced with the 2026-08-06 呼和浩特市领导班子 report (for the current
区委书记 赵燕茹, who also holds 呼和浩特市委统战部部长).

Task: inner_mongolia_回民区
Investigation date: 2026-08-06

Confirmed as of 2026-08:
  区委书记: 赵燕茹 (呼和浩特市委常委、统战部部长、回民区委书记)
       — confirmed via 呼和浩特市 report 2026-08-06 + 呼和浩特 build script + 维基百科
  区长:     廖雁渝 (女, 汉族, 1982-10, 2006-04入党) — confirmed via 回民区官网 政府领导

Predecessors:
  区委书记: 乔文杰 (男, 回族, 1976-11; 2001-06入党; 时任回民区委书记, 官网区委领导页)
  区人大常委会主任候选人: 薄兆慧 (男, 汉, 1975-06, 2001-03参加工作, 2004-06入党)
  区政协主席: 高俊娟 (女, 汉, 1970-12, 河北石家庄, 大学, 2002-11入党)

Web access: 官网可访问; 百度/Exa 受限。个别字段 (出生地、学历) 用置信度标注/留空。

Usage: python3 scripts/build/build_回民区_data.py
"""

import sqlite3
import os

# ── Paths ────────────────────────────────────────────────────────────
SLUG = "回民区"
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir.endswith("/scripts/build") or _script_dir.endswith("\\scripts\\build"):
    ROOT = os.path.dirname(os.path.dirname(_script_dir))
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_script_dir)))
DB_PATH = os.path.join(ROOT, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(ROOT, "data", "graph", f"{SLUG}_network.gexf")
TODAY = "2026-08-06"

# ── Persons ──────────────────────────────────────────────────────────
# (id, name, gender, ethnicity, birth, birthplace, education, party_join,
#  work_start, current_post, current_org, source)
persons = [
    # 核心领导 区委书记 / 区长
    (1, "赵燕茹", "女", "汉族", "", "", "", "中共党员", "",
     "呼和浩特市委常委、统战部部长、回民区委书记", "中共呼和浩特市回民区委员会",
     "呼和浩特市领导班子报告 2026-08-06 / 维基百科·呼和浩特市"),
    (2, "廖燕渝", "女", "汉族", "1982年10月", "", "", "2006年4月", "",
     "回民区委副书记、政府党组书记、区长", "回民区人民政府",
     "回民区人民政府官网 政府领导"),
    # 区委领导 (官网区委领导页, 2022/2023——乔文杰时代, 部分职务已被赵燕茹时期取代)
    (3, "乔文杰", "男", "回族", "1976年11月", "", "", "2001年6月", "",
     "曾任回民区委书记", "中共呼和浩特市回民区委员会",
     "回民区人民政府官网 区委领导"),
    (4, "王晓鸣", "", "", "", "", "", "", "", "区委副书记、政法委书记",
     "中共呼和浩特市回民区委员会", "回民区人民政府官网 区委领导"),
    (5, "李海鹰", "", "", "", "", "", "", "", "区委常委、统战部部长",
     "中共呼和浩特市回民区委员会", "回民区人民政府官网 区委领导"),
    (6, "呼和", "", "", "", "", "", "", "", "区委常委、常务副区长",
     "回民区人民政府", "回民区人民政府官网 领导之窗"),
    (7, "李斌", "", "", "", "", "", "", "", "区委常委、宣传部部长",
     "中共呼和浩特市回民区委员会", "回民区人民政府官网 区委领导"),
    (8, "齐泽恩", "", "", "", "", "", "", "", "区委常委、办公室主任",
     "中共呼和浩特市回民区委员会", "回民区人民政府官网 区委领导"),
    (9, "陈景毅", "", "", "", "", "", "", "", "区委常委、组织部部长",
     "中共呼和浩特市回民区委员会", "回民区人民政府官网 区委领导"),
    (10, "黄喜杰", "", "", "", "", "", "", "", "区委常委、纪委书记、监委主任",
     "呼和浩特市回民区纪律检查委员会", "回民区人民政府官网 区委领导"),
    (11, "马欣纲", "", "", "", "", "", "", "", "区委常委、副区长",
     "回民区人民政府", "回民区人民政府官网 领导之窗"),
    (12, "吴新义", "", "", "", "", "", "", "", "区委常委、人民武装部部长",
     "回民区人民武装部", "回民区人民政府官网 区委领导"),
    # 区政府领导 (current 2025-07)
    (13, "刘建强", "", "", "", "", "", "", "", "政府党组成员、副区长",
     "回民区人民政府", "回民区人民政府官网 政府领导"),
    (14, "库晓星", "", "", "", "", "", "", "", "政府党组成员、副区长",
     "回民区人民政府", "回民区人民政府官网 政府领导"),
    (15, "张宏涛", "", "", "", "", "", "", "", "副区长",
     "回民区人民政府", "回民区人民政府官网 政府领导"),
    (16, "周云", "", "", "", "", "", "", "", "副区长",
     "回民区人民政府", "回民区人民政府官网 政府领导"),
    # 区人大常委会
    (17, "薄兆慧", "男", "汉族", "1975年6月", "", "", "2004年6月", "2001年3月",
     "回民区人大常委会党组书记、主任", "回民区人大常委会",
     "回民区人民政府官网 人大领导"),
    (18, "张海涛", "", "", "", "", "", "", "", "区人大常委会副主任",
     "回民区人大常委会", "回民区人民政府官网 人大领导"),
    (19, "杨卓新", "", "", "", "", "", "", "", "区人大常委会副主任",
     "回民区人大常委会", "回民区人民政府官网 人大领导"),
    (20, "白建华", "", "", "", "", "", "", "", "区人大常委会副主任",
     "回民区人大常委会", "回民区人民政府官网 人大领导"),
    (21, "韩忠", "", "", "", "", "", "", "", "区人大常委会副主任",
     "回民区人大常委会", "回民区人民政府官网 人大领导"),
    (22, "马海宏", "", "", "", "", "", "", "", "区人大常委会副主任",
     "回民区人大常委会", "回民区人民政府官网 人大领导"),
    # 区政协
    (23, "高俊娟", "女", "汉族", "1970年12月", "河北省石家庄市", "大学", "2002年11月", "",
     "回民区政协党组书记、主席", "回民区政协",
     "回民区人民政府官网 政协领导"),
    (24, "刘鲲", "", "", "", "", "", "", "", "区政协副主席、区总工会党组书记主席",
     "回民区政协", "回民区人民政府官网 政协领导"),
    (25, "付旭刚", "", "", "", "", "", "", "", "区政协副主席、工商联主席",
     "回民区政协", "回民区人民政府官网 政协领导"),
    (26, "张灵旺", "", "", "", "", "", "", "", "区政协副主席",
     "回民区政协", "回民区人民政府官网 政协领导"),
    (27, "韩旭东", "", "", "", "", "", "", "", "区政协副主席",
     "回民区政协", "回民区人民政府官网 政协领导"),
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    (1, "中共呼和浩特市回民区委员会", "党委", "县处级", "中共呼和浩特市委员会", "呼和浩特市回民区"),
    (2, "回民区人民政府", "政府", "县处级", "呼和浩特市人民政府", "呼和浩特市回民区"),
    (3, "回民区人大常委会", "人大", "县处级", "呼和浩特市人大常委会", "呼和浩特市回民区"),
    (4, "回民区政协", "政协", "县处级", "呼和浩特市政协", "呼和浩特市回民区"),
    (5, "呼和浩特市回民区纪律检查委员会", "纪委", "县处级", "中共呼和浩特市纪律检查委员会", "呼和浩特市回民区"),
    (6, "回民区人民武装部", "党委", "县处级", "呼和浩特警备区", "呼和浩特市回民区"),
]

# ── Positions ────────────────────────────────────────────────────────
# (person_id, org_id, title, start, end, rank, note)
positions = [
    (1, 1, "回民区委书记", "", "present", "正处级", "兼任呼和浩特市委常委、统战部部长"),
    (2, 1, "区委副书记、政府党组书记", "", "present", "正处级", ""),
    (2, 2, "区长", "", "present", "正处级", ""),
    (3, 1, "曾任回民区委书记", "2021", "2023", "正处级", "前任书记; 官网区委领导页该届领导"),
    (4, 1, "区委副书记、政法委书记", "", "present", "副处级", ""),
    (5, 1, "区委常委、统战部部长", "", "present", "副处级", ""),
    (6, 1, "区委常委", "", "present", "副处级", ""),
    (6, 2, "常务副区长", "", "present", "副处级", ""),
    (7, 1, "区委常委、宣传部部长", "", "present", "副处级", ""),
    (8, 1, "区委常委、办公室主任", "", "present", "副处级", ""),
    (9, 1, "区委常委、组织部部长", "", "present", "副处级", ""),
    (10, 1, "区委常委", "", "present", "副处级", ""),
    (10, 5, "区纪委书记、监委主任", "", "present", "副处级", ""),
    (11, 1, "区委常委", "", "present", "副处级", ""),
    (11, 2, "副区长", "", "present", "副处级", ""),
    (12, 1, "区委常委", "", "present", "副处级", ""),
    (12, 6, "人民武装部部长", "", "present", "", ""),
    (13, 2, "政府党组成员、副区长", "", "present", "副处级", ""),
    (14, 2, "政府党组成员、副区长", "", "present", "副处级", ""),
    (15, 2, "副区长", "", "present", "副处级", ""),
    (16, 2, "副区长", "", "present", "副处级", ""),
    (17, 3, "区人大常委会党组书记、主任", "", "present", "正处级", ""),
    (18, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (19, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (20, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (21, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (22, 3, "区人大常委会副主任", "", "present", "副处级", ""),
    (23, 4, "区政协党组书记、主席", "", "present", "正处级", ""),
    (24, 4, "区政协副主席", "", "present", "副处级", ""),
    (25, 4, "区政协副主席", "", "present", "副处级", ""),
    (26, 4, "区政协副主席", "", "present", "副处级", ""),
    (27, 4, "区政协副主席", "", "present", "副处级", ""),
]

# ── Relationships ────────────────────────────────────────────────────
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    (1, 2, "overlap", "回民区党政一把手搭档", "回民区领导班子", "present"),
    (1, 3, "predecessor_successor", "回民区委书记 前任继任关系", "中共呼和浩特市回民区委员会", "2021-2023→now"),
    (2, 6, "superior_subordinate", "区长—常务副区长 上下级关系", "回民区人民政府", "present"),
    (2, 11, "superior_subordinate", "区长—副区长 上下级关系", "回民区人民政府", "present"),
    (2, 13, "superior_subordinate", "区长—副区长 上下级关系", "回民区人民政府", "present"),
    (2, 14, "superior_subordinate", "区长—副区长 上下级关系", "回民区人民政府", "present"),
    (2, 15, "superior_subordinate", "区长—副区长 上下级关系", "回民区人民政府", "present"),
    (2, 16, "superior_subordinate", "区长—副区长 上下级关系", "回民区人民政府", "present"),
    (1, 17, "overlap", "区委—人大 领导关系", "回民区四套班子", "present"),
    (1, 23, "overlap", "区委—政协 领导关系", "回民区四套班子", "present"),
    (2, 17, "overlap", "政府—人大 领导关系", "回民区四套班子", "present"),
    (2, 23, "overlap", "政府—政协 领导关系", "回民区四套班子", "present"),
    (1, 4, "superior_subordinate", "区委书记—区委副书记 上下级关系", "中共呼和浩特市回民区委员会", "present"),
    (1, 5, "superior_subordinate", "区委书记—区委常委 上下级关系", "中共呼和浩特市回民区委员会", "present"),
    (1, 9, "superior_subordinate", "区委书记—组织部部长 上下级关系", "中共呼和浩特市回民区委员会", "present"),
    (1, 10, "superior_subordinate", "区委书记—纪委书记 上下级关系", "中共呼和浩特市回民区委员会", "present"),
    (1, 7, "superior_subordinate", "区委书记—宣传部长 上下级关系", "中共呼和浩特市回民区委员会", "present"),
]


# ── Helpers ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


_ORG_COLORS = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
               "政协": "255,240,200", "开发区": "200,255,200", "纪委": "255,210,160",
               "default": "200,200,200"}


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
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
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