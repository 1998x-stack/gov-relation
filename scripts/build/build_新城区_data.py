#!/usr/bin/env python3
"""Build 呼和浩特市新城区 leadership network database and GEXF graph.

Data sourced from the official 呼和浩特市新城区人民政府 website
(www.xinchengqu.gov.cn) 领导之窗 pages, the 呼和浩特市委组织部 任前公示
(huhhot.gov.cn), and cross-region cadre movement reporting.

Core leaders (as of research date 2026-08):
  - 区委书记: 栗耀庭 (2026-07 到任; 前：呼和浩特市住建局党组书记、局长)
  - 区长:   金磊 (2026-01-30 当选; 前：市委宣传部副部长、市文旅广电局局长)

Sources:
  - S001: xinchengqu.gov.cn 区委领导之窗 http://www.xinchengqu.gov.cn/slbzd/zwdt_64218/ldzc_64223/xcqqw/
  - S002: xinchengqu.gov.cn 政府领导之窗 http://www.xinchengqu.gov.cn/slbzd/zwdt_64218/ldzc_64223/xcqzf/
  - S003: 栗耀庭个人简历页 (202607) http://www.xinchengqu.gov.cn/slbzd/zwdt_64218/ldzc_64223/xcqqw/202607/t20260703_2018295.html
  - S004: 金磊个人简历页 (202509) http://www.xinchengqu.gov.cn/slbzd/zwdt_64218/ldzc_64223/xcqqw/202509/t20250903_1928240.html
  - S005: 呼和浩特市委组织部公示 2025-08-21 http://www.huhhot.gov.cn/2022_zwdt/2022_tzgg/202508/t20250821_1923952.html
  - S006: 新城区十八届人大五次会议闭幕 (金磊当选区长) 2026-02-02 http://www.xinchengqu.gov.cn/zwdt/xczx/202602/t20260202_1973799.html
  - S007: 栗耀庭任呼和浩特市新城区委书记 (百家号) 2026-07-03 https://baijiahao.baidu.com/s?id=1869688005883702022
  - S008: 内蒙古建院原书记范志忠落马 (百家号) 2026-01-10 https://baijiahao.baidu.com/s?id=1853897682088623374
  - S009: 呼和浩特市对3名拟任干部公示 (含赵永刚) 2022-02-25 http://k.sina.com.cn/article_2810373291_a782e4ab02002ah3e.html

Usage: python3 scripts/build/build_新城区_data.py
"""

import sqlite3
import os

# ── Paths ────────────────────────────────────────────────────────────
SLUG = "新城区"
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
TODAY = "2026-08-06"

# ── Persons ──────────────────────────────────────────────────────────
# (id, name, gender, ethnicity, birth, birthplace, education, party_join,
#  work_start, current_post, current_org, source)
persons = [
    # 区委 (party committee)
    (1, "栗耀庭", "男", "汉族", "1971年10月", "内蒙古呼和浩特市武川县", "大学", "1996年7月", "1992年9月", "新城区委书记", "中共呼和浩特市新城区委员会", "新城区区委领导之窗 S001"),
    (2, "金磊", "男", "蒙古族", "1985年9月", "", "研究生，旅游管理硕士", "中共党员", "", "新城区委副书记、政府党组书记、区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    (3, "孙羽", "男", "汉族", "1982年7月", "", "大学", "中共党员", "", "新城区委副书记、政法委书记，区委教育工作委员会书记", "中共呼和浩特市新城区委员会", "新城区区委领导之窗 S001"),
    (4, "燕宪武", "男", "汉族", "1979年07月", "", "硕士研究生", "中共党员", "", "新城区委常委、纪委书记、监委主任", "中共呼和浩特市新城区委员会", "新城区区委领导之窗 S001"),
    (5, "云晓敏", "女", "蒙古族", "1980年4月", "", "研究生学历", "中共党员", "", "新城区委常委、统战部部长，政协党组副书记", "中共呼和浩特市新城区委员会", "新城区区委领导之窗 S001"),
    (6, "司瑞斌", "男", "汉族", "1979年5月", "", "大学", "中共党员", "", "新城区委常委、区政府党组成员、副区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    (7, "张飞", "男", "汉族", "1986年9月", "", "研究生", "中共党员", "", "新城区委常委、区政府党组成员、副区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    (8, "宋晓光", "男", "汉族", "1980年1月", "", "本科学历", "中共党员", "", "新城区委常委、武装部上校政治委员", "中共呼和浩特市新城区委员会", "新城区区委领导之窗 S001"),
    (9, "尹睿", "男", "汉族", "1982年4月", "", "硕士学历", "中共党员", "", "新城区委常委、宣传部部长", "中共呼和浩特市新城区委员会", "新城区区委领导之窗 S001"),
    (10, "赵晔青", "男", "汉族", "1985年7月", "", "研究生", "中共党员", "", "主持区委组织部全面工作（组织部长）", "中共呼和浩特市新城区委员会", "新城区区委领导之窗 S001"),
    # 政府 (government)
    (11, "王小平", "男", "汉族", "1973年12月", "", "大学", "中共党员", "", "政府党组成员、副区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    (12, "方达", "男", "蒙古族", "1976年3月", "", "大学", "中共党员", "", "政府党组成员、副区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    (13, "赵焱", "女", "汉族", "1984年11月", "", "大学本科", "中共党员", "", "政府党组成员、副区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    (14, "刘斐", "男", "汉族", "1983年7月", "", "大学", "民建会员", "", "政府副区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    (15, "白京东", "男", "汉族", "1993年4月", "", "大学", "无党派人士", "", "区政府挂职副区长", "新城区人民政府", "新城区区政府领导之窗 S002"),
    # 人大 (people's congress)
    (16, "刘冬生", "男", "汉族", "1970年12月", "", "大学", "中共党员", "", "新城区人大常委会党组书记、主任", "新城区人大常委会", "新城区人大领导之窗 S001"),
    (17, "张博文", "男", "汉族", "1975年3月", "", "", "中共党员", "", "新城区人大常委会党组成员、副主任", "新城区人大常委会", "新城区人大领导之窗 S001"),
    (18, "吴红莲", "女", "汉族", "1971年12月", "", "内蒙古党校研究生", "中共党员", "", "新城区人大常委会党组成员、副主任", "新城区人大常委会", "新城区人大领导之窗 S001"),
    (19, "唐亮", "男", "汉族", "1978年7月", "", "大学本科", "中共党员", "", "新城区人大常委会党组成员、副主任", "新城区人大常委会", "新城区人大领导之窗 S001"),
    # 政协 (CPPCC)
    (20, "朱艳梅", "女", "汉族", "1972年11月", "", "大学", "中共党员", "", "新城区政协党组书记、主席提名人选", "新城区政协", "新城区政协领导之窗 S001"),
    (21, "吴青", "女", "汉族", "1975年7月16日", "", "硕士研究生", "中共党员", "", "新城区政协党组成员、副主席提名人选", "新城区政协", "新城区政协领导之窗 S001"),
    (22, "王召祥", "男", "汉族", "1970年01月", "", "大学", "", "", "新城区政协副主席", "新城区政协", "新城区政协领导之窗 S001"),
    (23, "季利民", "男", "汉族", "1976年8月", "", "大学", "中共党员", "", "新城区政协党组成员、副主席", "新城区政协", "新城区政协领导之窗 S001"),
    # 前任/关联人物 (predecessors & cross-region)
    (24, "赵永刚", "男", "汉族", "1973年4月", "呼和浩特市土默特左旗", "内蒙古党校研究生", "中共党员", "1991年9月", "前期为新城区委书记（2022-2026）", "中共呼和浩特市新城区委员会", "百度百科 S_SINA / 新浪公示 S009"),
    (25, "范志忠", "男", "汉族", "1968年7月", "呼和浩特市武川县", "研究生", "1991年1月", "1991年8月", "前任新城区委书记（2021-2022，已落马）", "内蒙古建筑职业技术学院", "百家号 S008"),
    (26, "杨朋飞", "男", "汉族", "1985年7月", "", "研究生，农学硕士", "中共党员", "", "前期新城区委副书记、政法委书记；现任赛罕区委副书记、区长", "呼和浩特市赛罕区人民政府", "呼和浩特市委组织部公示 S005"),
    (27, "刘照江", "男", "", "1975年8月", "山东日照", "", "", "", "前任新城区政府区长（~2021-2024）", "新城区人民政府", "网易 旗县区名单"),
    (28, "白静", "女", "蒙古族", "1983年6月", "", "研究生，法学硕士", "中共党员", "", "前期新城区人民检察院检察长（2025年8月拟任市直部门正职）", "新城区人民检察院", "呼和浩特市委组织部公示 S005"),
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    (1, "中共呼和浩特市新城区委员会", "党委", "县处级", "中共呼和浩特市委员会", "呼和浩特市新城区"),
    (2, "新城区人民政府", "政府", "县处级", "呼和浩特市人民政府", "呼和浩特市新城区"),
    (3, "新城区人大常委会", "人大", "县处级", "呼和浩特市人大常委会", "呼和浩特市新城区"),
    (4, "新城区政协", "政协", "县处级", "呼和浩特市政协", "呼和浩特市新城区"),
    (5, "新城区人民检察院", "党委", "县处级", "呼和浩特市人民检察院", "呼和浩特市新城区"),
    (6, "呼和浩特市住房和城乡建设局", "政府", "县处级", "呼和浩特市人民政府", "呼和浩特市"),
    (7, "呼和浩特市文化旅游广电局", "政府", "县处级", "呼和浩特市人民政府", "呼和浩特市"),
    (8, "内蒙古建筑职业技术学院", "事业单位", "县处级", "内蒙古自治区教育厅", "呼和浩特市"),
    (9, "呼和浩特市赛罕区人民政府", "政府", "县处级", "呼和浩特市人民政府", "呼和浩特市赛罕区"),
]

# ── Positions ─────────────────────────────────────────────────────────
# (person_id, org_id, title, start, end, rank, note)
positions = [
    # 现任区委班子
    (1, 1, "新城区委书记", "2026-07", "present", "正处级", "2026-07 上任; 前任赵永刚"),
    (2, 1, "新城区委副书记", "2025-09", "present", "正处级", "兼任"),
    (2, 2, "新城区委副书记、区长", "2026-01", "present", "正处级", "2026-01-30 人大会当选"),
    (3, 1, "新城区委副书记、政法委书记", "", "present", "副处级", "兼区委教育工作委员会书记"),
    (4, 1, "新城区委常委、纪委书记、监委主任", "", "present", "副处级", ""),
    (5, 1, "新城区委常委、统战部部长、政协党组副书记", "", "present", "副处级", ""),
    (6, 1, "新城区委常委、副区长", "", "present", "副处级", ""),
    (6, 2, "区政府党组成员、副区长", "", "present", "副处级", "兼任"),
    (7, 1, "新城区委常委、副区长", "", "present", "副处级", ""),
    (7, 2, "区政府党组成员、副区长", "", "present", "副处级", "兼任"),
    (8, 1, "新城区委常委、武装部上校政治委员", "", "present", "副处级", ""),
    (9, 1, "新城区委常委、宣传部部长", "", "present", "副处级", ""),
    (10, 1, "主持区委组织部全面工作（组织部长）", "", "present", "副处级", ""),
    # 区政府
    (11, 2, "政府党组成员、副区长", "", "present", "副处级", ""),
    (12, 2, "政府党组成员、副区长", "", "present", "副处级", ""),
    (13, 2, "政府党组成员、副区长", "", "present", "副处级", ""),
    (14, 2, "政府副区长", "", "present", "副处级", "民建会员"),
    (15, 2, "区政府挂职副区长", "", "present", "副处级", ""),
    # 人大
    (16, 3, "区人大常委会党组书记、主任", "", "present", "正处级", ""),
    (17, 3, "区人大常委会党组成员、副主任", "", "present", "副处级", ""),
    (18, 3, "区人大常委会党组成员、副主任", "", "present", "副处级", ""),
    (19, 3, "区人大常委会党组成员、副主任", "", "present", "副处级", "2026-01 补选"),
    # 政协
    (20, 4, "区政协党组书记、主席提名人选", "", "present", "正处级", ""),
    (21, 4, "区政协党组成员、副主席提名人选", "", "present", "副处级", ""),
    (22, 4, "区政协副主席", "", "present", "副处级", ""),
    (23, 4, "区政协党组成员、副主席", "", "present", "副处级", ""),
    # 前任
    (24, 1, "新城区委书记", "2022-03", "2026-02", "正处级", "前任区委书记"),
    (25, 1, "新城区委书记", "2021-06", "2022-10", "正处级", "前任区委书记，后任内蒙古建院书记"),
    (25, 8, "内蒙古建筑职业技术学院党委书记", "2022-10", "2025-12", "正处级", "2025-12-17 落马被查"),
    (26, 9, "呼和浩特市赛罕区区委副书记、区长", "", "present", "正处级", "赛罕区领导班子（曾在民政区领导之窗）"),
    (27, 2, "新城区人民政府区长（代理）", "2021-07", "2022", "正处级", "前任区长"),
    (28, 5, "新城区人民检察院检察长", "", "2025", "副处级", "四级高级检察官"),
]

# ── Relationships ─────────────────────────────────────────────────────
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    # 党政一把手
    (1, 2, "overlap", "新城区党政一把手搭档", "中共呼和浩特市新城区委员会 / 新城区人民政府", "2026-07至今"),
    # 历任区委书记交接
    (1, 24, "predecessor_successor", "栗耀庭接任赵永刚为新城区委书记", "中共呼和浩特市新城区委员会", "2026-07"),
    (24, 25, "predecessor_successor", "赵永刚接替范志忠任新城区委书记", "中共呼和浩特市新城区委员会", "2022-2026"),
    (25, 27, "predecessor_successor", "范志忠曾任新城区区长，刘照江接任（代任）", "新城区人民政府", "2021"),
    (2, 27, "predecessor_successor", "金磊接任刘照江为新城区区长", "新城区人民政府", "2026"),
    # 区委班子上下级关系
    (3, 1, "superior_subordinate", "区委副书记—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    (4, 1, "superior_subordinate", "纪委常委—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    (5, 1, "superior_subordinate", "统战部长—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    (6, 1, "superior_subordinate", "副区长—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    (7, 1, "superior_subordinate", "副区长—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    (8, 1, "superior_subordinate", "武装部政委—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    (9, 1, "superior_subordinate", "宣传部长—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    (10, 1, "superior_subordinate", "组织部长—区委书记 上下级", "中共呼和浩特市新城区委员会", "present"),
    # 区政府班子下下级（与区长）
    (6, 2, "superior_subordinate", "副区长—区长 上下级", "新城区人民政府", "present"),
    (7, 2, "superior_subordinate", "副区长—区长 上下级", "新城区人民政府", "present"),
    (11, 2, "superior_subordinate", "副区长—区长 上下级", "新城区人民政府", "present"),
    (12, 2, "superior_subordinate", "副区长—区长 上下级", "新城区人民政府", "present"),
    (13, 2, "superior_subordinate", "副区长—区长 上下级", "新城区人民政府", "present"),
    (14, 2, "superior_subordinate", "副区长—区长 上下级", "新城区人民政府", "present"),
    (15, 2, "superior_subordinate", "挂职副区长—区长 上下级", "新城区人民政府", "present"),
    # 四套班子
    (1, 16, "overlap", "区委—人大 领导关系", "新城区四套班子", "present"),
    (1, 20, "overlap", "区委—政协 领导关系", "新城区四套班子", "present"),
    (2, 16, "overlap", "政府—人大 领导关系", "新城区四套班子", "present"),
    (2, 20, "overlap", "政府—政协 领导关系", "新城区四套班子", "present"),
    # 跨区/网络关系
    (26, 1, "overlap", "杨朋飞系新城区前任副书记、政法委书记，现任赛罕区区长，与区委书记在跨区交流网络中共事", "呼和浩特市辖区级领导班子", "2021-2025"),
    (25, 28, "overlap", "范志忠任新城区委书记期间，白静任新城区检察院检察长", "新城区四套班子", "2021-2022"),
    (24, 2, "overlap", "赵永刚任新城区委书记期间，金磊任新城区区长（搭档关系）", "新城区四套班子", "2025-2026"),
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
    if "书记" in post and "副" not in post:
        return "200,30,30"          # 区委书记 - red
    if ("区长" in post and "副" not in post) or ("县长" in post and "副" not in post):
        return "30,100,200"         # 区长 - blue
    if "人大" in post or "政协" in post:
        return "60,180,60"          # 人大/政协 - green
    if "副" in post:
        return "100,150,220"        # 副职 - light blue
    return "180,180,180"


def person_size(post):
    """Top leaders bigger in the graph."""
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
    lines.append(f'    <description>{SLUG} 领导班子关系网络图（呼和浩特市新城区）</description>')
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