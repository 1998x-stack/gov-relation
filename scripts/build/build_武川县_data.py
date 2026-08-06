#!/usr/bin/env python3
"""Build 武川县 leadership network SQLite database and GEXF graph.

武川县, 呼和浩特市, 内蒙古自治区
Research date: 2026-08-06

Current leadership (confirmed via wuchuan.gov.cn 领导之窗 / 第十六次党代会公报):
  - 县委书记: 宝力高 (蒙古族; 2026-07-29 当选第十六届县委书记; 兼任县人武部党委第一书记)
  - 县委副书记、县长: 金少琳 (男，汉族，1981年5月生，研究生，中共党员)
  - 县委副书记: 王瑶 (女，蒙古族)
  - 县纪委书记、监委主任: 陈攀攀 (女，蒙古族)
  - 人大常委会主任: 智建刚
  - 政协主席: 杨永刚

Sources:
  - S001: 十六届县委一次全会公报 http://www.wuchuan.gov.cn/dtzx/zwyw/202607/t20260730_2024595.html
  - S002: 金少琳 政府领导之窗简历 http://www.wuchuan.gov.cn/zwgk/ldzc/zf/202505/t20250528_1895048.html
  - S003: 宝力高一拄 2026-08-06 http://www.wuchuan.gov.cn/dtzx/zwyw/202608/t20260806_2026606.html
  - S004: 县政府常务会议 2026-08-06 http://www.wuchuan.gov.cn/dtzx/zwyw/202608/t20260806_2026603.html
  - S005: 人大常委会议 2026-08-06 http://www.wuchuan.gov.cn/dtzx/zwyw/202608/t20260806_2026608.html
  - S006: 党代会开幕 2026-07-27 http://www.wuchuan.gov.cn/dtzx/zwyw/202607/t20260727_2023838.html
  - S007: 人武部任命 2026-07-10 http://www.wuchuan.gov.cn/dtzx/zwyw/202607/t20260710_2020118.html
  - S008: 县委常委会（2026-06-17 县委书记哈达主持）http://www.wuchuan.gov.cn/dtzx/zwyw/202606/t20260617_2014498.html

Usage: python3 build_武川县_data.py
"""

import sqlite3
import os

# ── Paths ────────────────────────────────────────────────────────────
SLUG = "武川县"
# Resolve repo root: this file is at data/tmp/<task_id>/build_...
# Repo root is 3 directories up from the script when in staging,
# or 2 directories up when in scripts/build/
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
    # 县委班子
    (1, "宝力高", "", "蒙古族", "", "", "", "", "", "县委书记、县人武部党委第一书记", "中国共产党武川县委员会", "S001/S003"),
    (2, "金少琳", "男", "汉族", "1981年5月", "", "研究生", "中共党员", "", "县委副书记、县人民政府党组书记、县长", "武川县人民政府", "S002"),
    (3, "王瑶", "女", "蒙古族", "", "", "", "", "", "县委副书记", "中国共产党武川县委员会", "S001"),
    (4, "李敏", "女", "", "", "", "", "", "", "县委常委", "中国共产党武川县委员会", "S001"),
    (5, "王登龙", "男", "", "", "", "", "", "", "县委常委", "中国共产党武川县委员会", "S001"),
    (6, "赵伟", "男", "", "", "", "", "", "", "县委常委", "中国共产党武川县委员会", "S001"),
    (7, "崔振华", "男", "", "", "", "", "", "", "县委常委", "中国共产党武川县委员会", "S001"),
    (8, "陈攀攀", "女", "蒙古族", "", "", "", "", "", "县委常委、县纪委书记、监委主任", "中国共产党武川县委员会", "S001"),
    (9, "张杰", "男", "", "", "", "", "", "", "县委常委", "中国共产党武川县委员会", "S001"),
    (10, "白志轩", "男", "蒙古族", "", "", "", "", "", "县委常委", "中国共产党武川县委员会", "S001"),
    (11, "李艳雷", "男", "", "", "", "", "", "", "县委常委", "中国共产党武川县委员会", "S001"),
    (12, "兰雪刚", "男", "", "", "", "", "", "", "纪委副书记、监委副主任", "武川县纪委", "S001"),
    (13, "乌恩齐", "男", "蒙古族", "", "", "", "", "", "纪委副书记、监委副主任", "武川县纪委", "S001"),
    (14, "智建刚", "男", "", "", "", "", "", "", "县人大常委会党组书记、主任", "武川县人大常委会", "S005"),
    (15, "杨永刚", "男", "", "", "", "", "", "", "县政协党组书记、主席", "武川县政协", "S001/八一"),
    (16, "邢志恒", "男", "", "", "", "", "", "", "县人大常委会副主任", "武川县人大常委会", "S005"),
    (17, "李慧", "女", "", "", "", "", "", "", "县人大常委会副主任", "武川县人大常委会", "S005"),
    (18, "杜晓宏", "男", "", "", "", "", "", "", "县人大常委会副主任", "武川县人大常委会", "S005"),
    (19, "魏福龙", "男", "", "", "", "", "", "", "县人大常委会副主任", "武川县人大常委会", "S005"),
    (20, "哈达", "男", "蒙古族", "", "", "", "", "", "前任县委书记（~2025初-2026-06）", "中国共产党武川县委员会", "S008"),
    (21, "杨星晟", "男", "", "", "", "", "", "", "更早的原县委书记（~2025初）", "中国共产党武川县委员会", "S008"),
(22, "云海", "", "", "", "", "", "", "", "更早的原县委书记（~2021-06前）", "中国共产党武川县委员会", "S009"),
    (23, "荀皓", "男", "蒙古族", "1988年4月", "", "", "", "", "县政府党组成员、副县长", "武川县人民政府", "S010"),
    (24, "温林凡", "男", "", "", "", "", "", "", "副县长、县公安局局长", "武川县人民政府", "S010"),
    (25, "王登龙", "男", "", "", "", "", "", "", "县委常委、常务副县长", "武川县人民政府", "S010"),
    (26, "屈雪峰", "男", "", "", "", "", "", "", "县委常委、副县长（挂职）", "武川县人民政府", "S010"),
    (27, "魏会东", "男", "", "", "", "", "", "", "县委常委、副县长", "武川县人民政府", "S010"),
    (28, "云晓敏", "女", "蒙古族", "", "", "", "", "", "副县长", "武川县人民政府", "S010"),
    (29, "齐璞", "男", "", "", "", "", "", "", "副县长", "武川县人民政府", "S010"),
    (30, "白宇", "男", "", "", "", "", "", "", "副县长", "武川县人民政府", "S010"),
]


# ── Organizations ────────────────────────────────────────────────────
organizations = [
    (1, "中国共产党武川县委员会", "党委", "县处级", "中国共产党呼和浩特市委员会", "呼和浩特市武川县"),
    (2, "武川县人民政府", "政府", "县处级", "呼和浩特市人民政府", "呼和浩特市武川县"),
    (3, "武川县人民代表大会常务委员会", "人大", "县处级", "呼和浩特市人大常委会", "呼和浩特市武川县"),
    (4, "中国人民政治协商会议武川县委员会", "政协", "县处级", "呼和浩特市政协", "呼和浩特市武川县"),
    (5, "中共武川县纪律检查委员会", "党委", "县处级", "中共呼和浩特市纪委", "呼和浩特市武川县"),
    (6, "武川县人民武装部", "党委", "县处级", "呼和浩特警备区", "呼和浩特市武川县"),
]

# ── Positions ────────────────────────────────────────────────────────
# (person_id, org_id, title, start, end, rank, note)
positions = [
    (1, 1, "县委书记", "2026-07", "present", "正处级", "兼任县人武部党委第一书记"),
    (1, 6, "县人武部党委第一书记", "2026-07-09", "present", "正处级", ""),
    (2, 2, "县委副书记、县长", "2025-05", "present", "正处级", "2026-05-27 十六届县人大五次会议正式当选县长"),
    (2, 1, "县委副书记", "2025-05", "present", "正处级", "兼任"),
    (3, 1, "县委副书记", "2026-07", "present", "副处级", ""),
    (4, 1, "县委常委", "2026-07", "present", "副处级", ""),
    (5, 1, "县委常委", "2026-07", "present", "副处级", ""),
    (6, 1, "县委常委", "2026-07", "present", "副处级", ""),
    (7, 1, "县委常委", "2026-07", "present", "副处级", ""),
    (8, 1, "县委常委", "2026-07", "present", "副处级", "纪委书记"),
    (8, 5, "县纪委书记、监委主任", "2026-07", "present", "副处级", ""),
    (9, 1, "县委常委", "2026-07", "present", "副处级", ""),
    (10, 1, "县委常委", "2026-07", "present", "副处级", ""),
    (11, 1, "县委常委", "2026-07", "present", "副处级", ""),
    (12, 5, "纪委副书记、监委副主任", "2026-07", "present", "副处级", ""),
    (13, 5, "纪委副书记、监委副主任", "2026-07", "present", "副处级", ""),
    (14, 3, "县人大常委会主任", "", "present", "正处级", ""),
    (16, 3, "县人大常委会副主任", "", "present", "副处级", ""),
    (17, 3, "县人大常委会副主任", "", "present", "副处级", ""),
    (18, 3, "县人大常委会副主任", "", "present", "副处级", ""),
    (19, 3, "县人大常委会副主任", "", "present", "副处级", ""),
    (15, 4, "县政协主席", "", "present", "正处级", ""),
    (20, 1, "县委书记", "2025", "2026-06", "正处级", "前任县委书记（哈达）"),
    (21, 1, "县委书记", "", "2025", "正处级", "更早的原县委书记（杨星晟，后任呼和浩特市人大副主任）"),
    (22, 1, "县委书记", "", "2021-06", "正处级", "更早的原县委书记（云海）"),
    (23, 2, "县政府党组成员、副县长", "", "present", "副处级", "蒙古族，分管工业经济、民政、生态环保、招商引资等"),
    (24, 2, "副县长、县公安局局长", "", "present", "副处级", ""),
    (25, 2, "县委常委、常务副县长", "", "present", "副处级", ""),
    (25, 1, "县委常委", "", "present", "副处级", "兼任常务副县长"),
    (26, 2, "县委常委、副县长（挂职）", "", "present", "副处级", ""),
    (27, 2, "县委常委、副县长", "", "present", "副处级", ""),
    (28, 2, "副县长", "", "present", "副处级", ""),
    (29, 2, "副县长", "", "present", "副处级", ""),
    (30, 2, "副县长", "", "present", "副处级", ""),
]

# ── Relationships ────────────────────────────────────────────────────
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    # 党政一把手
    (1, 2, "overlap", "县委书记—县长 党政一把手搭档", "武川县四套班子", "2026-07至今"),
    # 县委班子内部
    (1, 3, "superior_subordinate", "书记—副书记 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 8, "superior_subordinate", "书记—纪委书记 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 4, "superior_subordinate", "书记—常委 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 5, "superior_subordinate", "书记—常委 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 6, "superior_subordinate", "书记—常委 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 7, "superior_subordinate", "书记—常委 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 9, "superior_subordinate", "书记—常委 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 10, "superior_subordinate", "书记—常委 上下级", "中共武川县委员会", "2026-07至今"),
    (1, 11, "superior_subordinate", "书记—常委 上下级", "中共武川县委员会", "2026-07至今"),
    (2, 3, "superior_subordinate", "县长—副书记 平级协岗", "中共武川县委员会", "2026-07至今"),
    # 纪委班子
    (8, 12, "superior_subordinate", "纪委书记—纪委副书记 上下级", "武川县纪委", "2026-07至今"),
    (8, 13, "superior_subordinate", "纪委书记—纪委副书记 上下级", "武川县纪委", "2026-07至今"),
    # 四套班子领导
    (1, 14, "overlap", "县委—人大 领导关系", "武川县四班子", "present"),
    (1, 15, "overlap", "县委—政协 领导关系", "武川县四套班子", "present"),
    (2, 14, "overlap", "政府—人大 领导关系", "武川县四套班子", "present"),
    (2, 15, "overlap", "政府—政协 领导关系", "武川县四套班子", "present"),
    (14, 16, "superior_subordinate", "人大主任—人大副主任 上下级", "武川县人大常委会", "present"),
    (14, 17, "superior_subordinate", "人大主任—人大副主任 上下级", "武川县人大常委会", "present"),
    (14, 18, "superior_subordinate", "人大主任—人大副主任 上下级", "武川县人大常委会", "present"),
    (14, 19, "superior_subordinate", "人大主任—人大副主任 上下级", "武川县人大常委会", "present"),
    # 前任交接链条
    (1, 20, "predecessor_successor", "宝力高接任哈达为县委书记", "中共武川县委员会", "2026-07"),
    (20, 21, "predecessor_successor", "哈达接任杨星晟为县委书记", "中共武川县委员会", "2025"),
    (21, 22, "predecessor_successor", "杨星晟接任云海为县委书记", "中共武川县委员会", "2021"),
    # 县政府班子（县长—副县长）
    (2, 23, "superior_subordinate", "县长—副县长 上下级（荀皓）", "武川县人民政府", "present"),
    (2, 24, "superior_subordinate", "县长—副县长/公安局长 上下级（温林凡）", "武川县人民政府", "present"),
    (2, 25, "superior_subordinate", "县长—常务副县长 上下级（王登龙）", "武川县人民政府", "present"),
    (2, 26, "superior_subordinate", "县长—挂职副县长 上下级（屈雪峰）", "武川县人民政府", "present"),
    (2, 27, "superior_subordinate", "县长—副县长 上下级（魏会东）", "武川县人民政府", "present"),
    (2, 28, "superior_subordinate", "县长—副县长 上下级（云晓敏）", "武川县人民政府", "present"),
    (2, 29, "superior_subordinate", "县长—副县长 上下级（齐璞）", "武川县人民政府", "present"),
    (2, 30, "superior_subordinate", "县长—副县长 上下级（白宇）", "武川县人民政府", "present"),
]


# ── Helpers ───────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


_ORG_COLORS = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
               "政协": "255,240,200", "开发区": "200,255,200", "事业单位": "220,220,220",
               "default": "200,200,200"}


def person_color(post):
    """Person node color by current title."""
    if ("纪委" in post):
        return "255,165,0"           # 纪委书记/纪委 - orange
    if ("书记" in post and "副" not in post):
        return "200,30,30"          # 县委书记 - red
    if ("县长" in post and "副" not in post):
        return "30,100,200"          # 县长 - blue
    if "人大" in post or "政协" in post:
        return "60,180,60"           # 人大/政协 - green
    if "副" in post or "副书记" in post:
        return "100,150,220"         # 副职/副书记 - light blue
    return "180,180,180"


def person_size(post):
    """Top leaders bigger in the graph."""
    if ("书记" in post and "副" not in post and "纪委" not in post) or ("县长" in post and "副" not in post):
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
    lines.append(f'    <description>{SLUG} 领导班子关系网络图（呼和浩特市武川县）</description>')
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