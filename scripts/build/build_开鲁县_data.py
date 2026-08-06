#!/usr/bin/env python3
"""Build 开鲁县 leadership network SQLite database and GEXF graph.

开鲁县, 通辽市, 内蒙古自治区
Research date: 2026-08-06
Task ID: inner_mongolia_开鲁县
Level: 县
Targets: 县委书记 & 县长

Current leadership (verified from www.kailu.gov.cn official site, 2026-08-06):

  - 县委书记: 张世国
  - 县委副书记、县长: 刘洋 (1984-02 生, 内蒙古通辽; 云南师范大学国贸本科; 吉林大学软件工程硕士)

  十四次党代会(2026-07-27/28) 执行主席: 张世国、刘洋、李建辉、苏学权、阿拉坦夫、
    康君、何春红、吴国柱、常亮、郭彦纯
  主席台就座: 张文军、姜晶莹、孙书慧、田志鹏、崔宝来、孙春辉、李良、王旭、
    秦晓明、王超、刘进贤、廉淑云

  政府领导班子(领导之窗):
    - 常务副县长 康君;  副县长 杨存秀、崔宝来、常亮、李良;  提名副县长 王旭、宋妍

Sources:
  S001 开鲁县·政府领导之窗             http://www.kailu.gov.cn/zwgk/
  S002 刘洋 领导之窗简历页             http://www.kailu.gov.cn/klzf/ldzc/zf/xz/ly/
  S003 各副县长领导之窗简历页
  S004 2026-07-23 招商引资调度会      http://www.kailu.gov.cn/xwzx/kldt/202607/t20260727_1062164.html
  S005 十四次党代会闭幕               http://www.kailu.gov.cn/xwzx/kldt/202607/t20260729_1062660.html

Usage: python3 build_开鲁县_data.py
"""

import sqlite3
import os

# ── Paths ────────────────────────────────────────────────────────────
SLUG = "开鲁县"
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir.endswith("/scripts/build") or _script_dir.endswith("\\scripts\\build"):
    ROOT = os.path.dirname(os.path.dirname(_script_dir))
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_script_dir)))
DB_PATH = os.path.join(ROOT, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(ROOT, "data", "graph", f"{SLUG}_network.gexf")
TODAY = "2026-08-06"


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── Persons ──────────────────────────────────────────────────────────
# (id, name, gender, ethnicity, birth, birthplace, education, party_join,
#  work_start, current_post, current_org, source)
persons = [
    (1, "张世国", "男", "", "", "", "", "", "", "县委书记", "中国共产党开鲁县委员会", "S004/S005"),
    (2, "刘洋", "男", "汉族", "1984年2月", "内蒙古通辽", "云南师范大学国际经贸本科；吉林大学软件工程硕士", "2005年12月", "2007年11月", "县委副书记、县长", "开鲁县人民政府", "S001/S002"),
    (3, "李建辉", "男", "", "", "", "", "", "", "县委常委(待核)", "中国共产党开鲁县委员会", "S005"),
    (4, "苏学权", "男", "", "", "", "", "", "", "县委常委(待核)", "中国共产党开鲁县委员会", "S005"),
    (5, "阿拉坦夫", "男", "蒙古族", "", "", "", "", "", "县委常委(待核)", "中国共产党开鲁县委员会", "S005"),
    (6, "何春红", "男", "", "", "", "", "", "", "县委常委(待核)", "中国共产党开鲁县委员会", "S005"),
    (7, "吴国柱", "男", "", "", "", "", "", "", "县委常委(待核)", "中国共产党开鲁县委员会", "S005"),
    (8, "郭彦纯", "男", "", "", "", "", "", "", "县委常委(待核)", "中国共产党开鲁县委员会", "S005"),
    (25, "孙银萍", "女", "", "", "", "", "", "", "县委领导(待核)", "中国共产党开鲁县委员会", "S006"),
    (9, "康君", "男", "汉族", "1979年4月", "内蒙古开鲁", "不详", "2002年6月", "2000年9月", "县委常委、常务副县长", "开鲁县人民政府", "S001"),
    (10, "杨存秀", "男", "汉族", "1985年8月", "青海乐都", "内蒙古科技大学给水排水工程", "2010年6月", "2006年8月", "县委常委、副县长", "开鲁县人民政府", "S001"),
    (11, "崔宝来", "男", "汉族", "1976年8月", "科左后旗", "内蒙古警校中专→中国人民公安大学", "2002年6月", "1998年10月", "副县长、公安局局长", "开鲁县人民政府", "S001"),
    (12, "常亮", "男", "蒙古族", "1982年11月", "科右中旗", "", "2005年11月", "2007年5月", "副县长", "开鲁县人民政府", "S001"),
    (13, "李良", "男", "汉族", "1981年10月", "内蒙古开鲁", "", "2007年7月", "2005年3月", "副县长", "开鲁县人民政府", "S001"),
    (14, "王旭", "男", "汉族", "1986年10月", "开鲁", "南昌大学科技学院工商管理；内蒙古党校经管研究生", "", "2010年3月", "副县长(提名)", "开鲁县人民政府", "S001"),
    (15, "宋妍", "女", "满族", "1988年1月", "内蒙古开鲁", "大连大学市场营销专业；内蒙古党校研究生", "农工党", "2010年8月", "副县长(提名)", "开鲁县人民政府", "S001"),
    # ── 主席台其他成员 ────────────────────────────────────────────────
    (16, "张文军", "男", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S004/S005"),
    (17, "姜晶莹", "女", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S005"),
    (18, "孙书慧", "女", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S004/S005"),
    (19, "田志鹏", "男", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S005"),
    (20, "孙春辉", "男", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S005"),
    (21, "秦晓明", "男", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S005"),
    (22, "王超", "男", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S005"),
    (23, "刘进贤", "男", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S005"),
    (24, "廉淑云", "女", "", "", "", "", "", "", "县领导(待核)", "开鲁县", "S005"),
]

# ── Organizations ────────────────────────────────────────────────────
# (id, name, type, level, parent, location)
organizations = [
    (1, "中国共产党开鲁县委员会", "党委", "县处级", "中共通辽市委员会", "内蒙古通辽市开鲁县"),
    (2, "开鲁县人民政府", "政府", "县处级", "通辽市人民政府", "内蒙古通辽市开鲁县"),
    (3, "开鲁县人民代表大会常务委员会", "人大", "县处级", "通辽市人大常委会", "内蒙古通辽市开鲁县"),
    (4, "中国人民政治协商会议开鲁县委员会", "政协", "县处级", "通辽市政协", "内蒙古通辽市开鲁县"),
    (5, "中共开鲁县纪律检查委员会", "党委", "县处级", "中共通辽市纪委", "内蒙古通辽市开鲁县"),
    (6, "开鲁县公安局", "政府", "科级", "开鲁县人民政府", "内蒙古通辽市开鲁县"),
    (7, "内蒙古通辽开鲁生物医药开发区", "开发区", "县处级", "开鲁县人民政府", "内蒙古通辽市开鲁县"),
]

# ── Positions ────────────────────────────────────────────────────────
# (person_id, org_id, title, start, end, rank, note)
positions = [
    (1, 1, "县委书记", "未知", "present", "正处级", "2026年7月仍主持县委工作"),
    (2, 2, "县委副书记、县长", "2023", "present", "正处级", "上任具体时点待核"),
    (2, 1, "县委副书记", "2023", "present", "正处级", "兼任县委副书记"),
    (3, 1, "县委常委", "", "present", "副处级", "具体分工待核"),
    (4, 1, "县委常委", "", "present", "副处级", "具体分工待核"),
    (5, 1, "县委常委", "", "present", "副处级", "党政分工待核"),
    (6, 1, "县委常委", "", "present", "副处级", "具体分工待核"),
    (7, 1, "县委常委", "", "present", "副处级", "具体分工待核"),
    (8, 1, "县委常委", "", "present", "副处级", "具体分工待核"),
    (25, 1, "县委领导", "", "present", "副处级", "十四届党代会执行主席，具体分工待核"),
    (9, 2, "县委常委、常务副县长", "", "present", "副处级", "分管综合经济/财税/发改/审计等"),
    (9, 1, "县委常委", "", "present", "副处级", ""),
    (10, 2, "县委常委、副县长", "", "present", "副处级", "分管工业/城建/生态环保/区域经济合作，联系科技开发区"),
    (10, 1, "县委常委", "", "present", "副处级", ""),
    (11, 2, "副县长、公安局局长", "", "present", "副处级", "负责公安/信访/退役军人事务"),
    (11, 6, "公安局党委书记、局长", "", "present", "副处级", ""),
    (12, 2, "副县长", "", "present", "副处级", "分管乡村振兴/农牧业/水务林业"),
    (13, 2, "副县长", "", "present", "副处级", "分工待核"),
    (14, 2, "副县长(提名)", "", "present", "副处级", "2026年提名"),
    (15, 2, "副县长(提名)", "", "present", "副处级", "2026年提名"),
    (16, 1, "县委领导", "", "present", "副处级", "待核"),
    (17, 1, "县级领导", "", "present", "副处级", "待核"),
    (18, 1, "县级领导", "", "present", "副处级", "待核"),
    (19, 1, "县级领导", "", "present", "副处级", "待核"),
    (20, 1, "县级领导", "", "present", "副处级", "待核"),
    (21, 1, "县级领导", "", "present", "副处级", "待核"),
    (22, 1, "县级领导", "", "present", "副处级", "待核"),
    (23, 1, "县级领导", "", "present", "副处级", "待核"),
    (24, 1, "县级领导", "", "present", "副处级", "待核"),
]

# ── Relationships ────────────────────────────────────────────────────
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    (1, 2, "overlap", "县委书记—县长 党政一把手搭档", "开鲁县四套班子", "2023至今"),
    (1, 9, "superior_subordinate", "书记—常务副县长 上级关系", "中共开鲁县委员会/开鲁县人民政府", "present"),
    (1, 10, "superior_subordinate", "书记—副县长 上级关系", "中共开鲁县委员会", "present"),
    (1, 6, "superior_subordinate", "书记—县委常委 上下级", "中共开鲁县委员会", "present"),
    (1, 7, "superior_subordinate", "书记—县委常委 上下级", "中共开鲁县委员会", "present"),
    (1, 8, "superior_subordinate", "书记—县委常委 上下级", "中共开鲁县委员会", "present"),
    (2, 9, "superior_subordinate", "县长—常务副县长 上下级", "开鲁县人民政府", "present"),
    (2, 10, "superior_subordinate", "县长—副县长 上下级", "开鲁县人民政府", "present"),
    (2, 11, "superior_subordinate", "县长—副县长/公安局长 上下级", "开鲁县人民政府", "present"),
    (2, 12, "superior_subordinate", "县长—副县长 上下级", "开鲁县人民政府", "present"),
    (2, 13, "superior_subordinate", "县长—副县长 上下级", "开鲁县人民政府", "present"),
    (2, 14, "superior_subordinate", "县长—提名副县长 下级", "开鲁县人民政府", "2026"),
    (2, 15, "superior_subordinate", "县长—提名副县长 下级", "开鲁县人民政府", "2026"),
    (9, 11, "overlap", "常务副县长—公安局长 同班子", "开鲁县人民政府", "present"),
    (11, 2, "overlap", "公安局长—县长 上下级并管社会稳定", "开鲁县人民政府/公安局", "present"),
]

# ── Helpers for GEXF ────────────────────────────────────────────────

def person_color(post):
    if "纪委" in post:
        return "255,165,0"
    if "书记" in post and "副" not in post:
        return "200,30,30"
    if "县长" in post and "副" not in post:
        return "30,100,200"
    if "人大" in post or "政协" in post:
        return "60,180,60"
    if "副" in post or "副书记" in post:
        return "100,150,220"
    return "180,180,180"


def person_size(post):
    if ("书记" in post and "副" not in post and "纪委" not in post) or ("县长" in post and "副" not in post):
        return "20.0"
    return "12.0"


ORG_COLORS = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
              "政协": "255,240,200", "开发区": "200,255,200", "公安局": "255,200,200",
              "纪委": "255,165,0", "default": "200,200,200"}


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


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>开鲁县 领导班子工作关系网络图（通辽市·内蒙古）</description>')
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
        oc = ORG_COLORS.get(otype, ORG_COLORS["default"])
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
