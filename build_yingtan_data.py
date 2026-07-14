#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yingtan City (鹰潭市) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yingtan_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yingtan_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (市委书记) ──
    {"id": 1, "name": "王亚联", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-09", "birthplace": "江西九江", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市委书记", "current_org": "中共鹰潭市委员会",
     "source": "http://district.ce.cn/newarea/sddy/202601/t20260117_2709196.shtml"},

    # ── Mayor (市长) ──
    {"id": 2, "name": "王亚青", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-08", "birthplace": "安徽庐江", "education": "博士研究生（中科大）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市委副书记、市长", "current_org": "鹰潭市人民政府",
     "source": "http://district.ce.cn/newarea/sddy/202501/08/t20250108_39260015.shtml"},

    # ── NPC Standing Committee Director (市人大常委会主任) ──
    {"id": 3, "name": "黄金龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-03", "birthplace": "江西赣州赣县区", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市人大常委会主任", "current_org": "鹰潭市人大常委会",
     "source": "http://district.ce.cn/newarea/sddy/202501/08/t20250108_39260015.shtml"},

    # ── CPPCC Chairman (市政协主席) ──
    {"id": 4, "name": "黄云", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-11", "birthplace": "江西宁都", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市政协主席", "current_org": "政协鹰潭市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%B9%B0%E6%BD%AD%E5%B8%82"},

    # ── Executive Vice Mayor (常务副市长) ──
    {"id": 5, "name": "江训开", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-09", "birthplace": "江西都昌", "education": "省委党校研究生，农业推广硕士",
     "party_join": "1995-05", "work_start": "1996-08",
     "current_post": "鹰潭市委常委、常务副市长", "current_org": "鹰潭市人民政府",
     "source": "http://www.yingtan.gov.cn/art/2021/2/9/art_10130_21.html"},

    # ── Organization Department Head (组织部部长) ──
    {"id": 6, "name": "肖国军", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-12", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市委常委、组织部部长", "current_org": "中共鹰潭市委组织部",
     "source": "http://www.yingtan.gov.cn/art/2026/7/11/art_47_1602071.html"},

    # ── Discipline Inspection Secretary (市纪委书记) ──
    {"id": 7, "name": "毛晖圆", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-03", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市委常委、市纪委书记、市监委代主任", "current_org": "中共鹰潭市纪律检查委员会",
     "source": "http://www.yingtan.gov.cn/art/2026/7/11/art_47_1602069.html"},

    # ── Propaganda Department Head (宣传部部长) ──
    {"id": 8, "name": "黄忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-07", "birthplace": "江西新建", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "约1988年",
     "current_post": "鹰潭市委常委、宣传部部长", "current_org": "中共鹰潭市委宣传部",
     "source": "https://www.163.com/dy/article/ISJ2C3U90514A0A7.html"},

    # ── United Front Dept Head (统战部部长) ──
    {"id": 9, "name": "蔡江", "gender": "女", "ethnicity": "汉族",
     "birth": "1968-03", "birthplace": "江西贵溪", "education": "省委党校研究生",
     "party_join": "1994-07", "work_start": "1989-08",
     "current_post": "鹰潭市委常委、统战部部长", "current_org": "中共鹰潭市委统战部",
     "source": "https://www.163.com/dy/article/ISJ2C3U90514A0A7.html"},

    # ── Political & Legal Committee Secretary (政法委书记) ──
    {"id": 10, "name": "褚小涛", "gender": "男", "ethnicity": "汉族",
     "birth": "约1972", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市委常委、政法委书记", "current_org": "中共鹰潭市委政法委员会",
     "source": "https://www.yingtan.gov.cn/art/2026/6/18/art_47_1596959.html"},

    # ── Deputy Mayor (副市长) list ──
    {"id": 11, "name": "万玲", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "", "education": "大学，管理学硕士",
     "party_join": "民建会员", "work_start": "",
     "current_post": "鹰潭市副市长", "current_org": "鹰潭市人民政府",
     "source": "http://www.yingtan.gov.cn/art/2025/1/8/art_201_11.html"},

    {"id": 12, "name": "胡春平", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-09", "birthplace": "", "education": "博士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市副市长、党组成员", "current_org": "鹰潭市人民政府",
     "source": "http://www.yingtan.gov.cn"},

    {"id": 13, "name": "刘江", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-10", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市副市长、党组成员、市公安局局长", "current_org": "鹰潭市人民政府",
     "source": "http://www.yingtan.gov.cn"},

    {"id": 14, "name": "陈敏", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-08", "birthplace": "", "education": "在职研究生，经济学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市副市长、党组成员", "current_org": "鹰潭市人民政府",
     "source": "http://www.yingtan.gov.cn"},

    {"id": 15, "name": "王俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-09", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市政府秘书长、党组成员", "current_org": "鹰潭市人民政府",
     "source": "http://www.yingtan.gov.cn"},

    # ── Predecessor Mayors (前任市长) ──
    {"id": 16, "name": "张子建", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "江西贵溪", "education": "",
     "party_join": "中共党员", "work_start": "1994-08",
     "current_post": "楚雄州委书记（原鹰潭市长）", "current_org": "中共楚雄州委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%B9%B0%E6%BD%AD%E5%B8%82"},

    {"id": 17, "name": "陈敏(前任)", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "江西赣州", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江西省委常委、省委秘书长（原鹰潭市长）", "current_org": "中共江西省委",
     "source": "https://zh.wikipedia.org/wiki/%E9%99%88%E6%95%8F_(1972%E5%B9%B4)"},

    {"id": 18, "name": "于秀明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江西省政协副主席（原鹰潭市长）", "current_org": "江西省政协",
     "source": "https://zh.wikipedia.org/wiki/%E4%BA%8E%E7%A7%80%E6%98%8E"},

    {"id": 19, "name": "曹淑敏", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中央宣传部副部长、国家广电总局局长（原鹰潭市长/书记）", "current_org": "国家广播电视总局",
     "source": "https://zh.wikipedia.org/wiki/%E6%9B%B9%E6%B7%91%E6%95%8F"},

    {"id": 20, "name": "熊茂平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委副书记（原鹰潭市长）", "current_org": "中共辽宁省委",
     "source": "https://zh.wikipedia.org/wiki/%E7%86%8A%E8%8C%82%E5%B9%B3"},

    {"id": 21, "name": "钟志生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "已查（原鹰潭市长→景德镇书记→省人社厅长）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E9%92%9F%E5%BF%97%E7%94%9F"},

    {"id": 22, "name": "董仚生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "河北省委政法委原书记（原鹰潭市长→上饶书记）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E8%91%A3%E4%BB%9A%E7%94%9F"},

    # ── Other former party secretaries ──
    {"id": 23, "name": "许南吉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江西省财政厅厅长（原鹰潭市委书记）", "current_org": "江西省财政厅",
     "source": "https://zh.wikipedia.org/wiki/%E8%AE%B8%E5%8D%97%E5%90%89"},

    {"id": 24, "name": "黄喜忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-11", "birthplace": "广东揭阳", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赣州市委书记（原南昌市长→鹰潭书记）", "current_org": "中共赣州市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E5%96%9C%E5%BF%A0"},
]

# ── Organizations ──
orgs = [
    # Party
    {"id": 1, "name": "中共鹰潭市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "鹰潭市"},
    {"id": 2, "name": "中共鹰潭市委组织部", "type": "党委", "level": "地级市", "parent": "中共鹰潭市委员会", "location": "鹰潭市"},
    {"id": 3, "name": "中共鹰潭市委宣传部", "type": "党委", "level": "地级市", "parent": "中共鹰潭市委员会", "location": "鹰潭市"},
    {"id": 4, "name": "中共鹰潭市委统战部", "type": "党委", "level": "地级市", "parent": "中共鹰潭市委员会", "location": "鹰潭市"},
    {"id": 5, "name": "中共鹰潭市委政法委员会", "type": "党委", "level": "地级市", "parent": "中共鹰潭市委员会", "location": "鹰潭市"},
    {"id": 6, "name": "中共鹰潭市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共鹰潭市委员会", "location": "鹰潭市"},
    # Government
    {"id": 7, "name": "鹰潭市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "鹰潭市"},
    {"id": 8, "name": "鹰潭市公安局", "type": "政府", "level": "地级市", "parent": "鹰潭市人民政府", "location": "鹰潭市"},
    # People's Congress
    {"id": 9, "name": "鹰潭市人大常委会", "type": "人大", "level": "地级市", "parent": "", "location": "鹰潭市"},
    # CPPCC
    {"id": 10, "name": "政协鹰潭市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "鹰潭市"},
    # External orgs
    {"id": 11, "name": "中共江西省委组织部", "type": "党委", "level": "省级", "parent": "中共江西省委", "location": "南昌市"},
    {"id": 12, "name": "中共吉安市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "吉安市"},
    {"id": 13, "name": "吉安市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "吉安市"},
    {"id": 14, "name": "中共楚雄州委员会", "type": "党委", "level": "地级市（州）", "parent": "", "location": "云南省楚雄州"},
    {"id": 15, "name": "江西省财政厅", "type": "政府", "level": "省级", "parent": "江西省人民政府", "location": "南昌市"},
    {"id": 16, "name": "江西省政协", "type": "政协", "level": "省级", "parent": "", "location": "南昌市"},
    {"id": 17, "name": "中共赣州市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "赣州市"},
    {"id": 18, "name": "国家广播电视总局", "type": "政府", "level": "国家级", "parent": "", "location": "北京市"},
    {"id": 19, "name": "中共辽宁省委", "type": "党委", "level": "省级", "parent": "", "location": "沈阳市"},
    {"id": 20, "name": "中共江西省委", "type": "党委", "level": "省级", "parent": "", "location": "南昌市"},
    {"id": 21, "name": "中国电子科技集团（CETC）", "type": "事业单位", "level": "国家级", "parent": "", "location": "北京"},
]

# ── Positions (person_id, org_id, title, start, end, rank, note) ──
positions = [
    # 王亚联
    (1, 1, "鹰潭市委书记", "2026-01", "至今", "正厅级", ""),
    (1, 13, "吉安市委副书记、市长", "2021", "2026-01", "正厅级", "前任职务"),

    # 王亚青
    (2, 7, "鹰潭市委副书记、市长", "2025-01", "至今", "正厅级", "2024.12—2025.01代市长"),
    (2, 1, "鹰潭市委副书记", "2024-12", "至今", "副厅级", "兼任"),
    (2, 11, "江西省委组织部副部长", "2023-09", "2024-12", "副厅级", "空降前职务"),
    (2, 21, "中国电子科技集团（CETC）任职", "约2003", "2023", "", "曾长期任职CETC，具体职务待查"),

    # 黄金龙
    (3, 9, "鹰潭市人大常委会主任", "2025-01", "至今", "正厅级", "前专职副书记"),
    (3, 1, "鹰潭市委副书记（专职）", "2021-09", "2024-12", "副厅级", ""),

    # 黄云
    (4, 10, "鹰潭市政协主席", "2021-10", "至今", "正厅级", ""),

    # 江训开
    (5, 7, "鹰潭市委常委、常务副市长", "2024-04", "至今", "副厅级", "市政府党组副书记"),
    (5, 1, "鹰潭市委常委", "2024-04", "至今", "副厅级", ""),

    # 肖国军
    (6, 2, "鹰潭市委常委、组织部部长", "2021-09", "至今", "副厅级", ""),
    (6, 20, "江西省人社厅副厅长", "2020-01", "2021-09", "副厅级", ""),

    # 毛晖圆
    (7, 6, "鹰潭市委常委、市纪委书记、市监委代主任", "2026-05", "至今", "副厅级", "此前省纪委党风政风监督室主任"),

    # 黄忠
    (8, 3, "鹰潭市委常委、宣传部部长", "至今", "至今", "副厅级", ""),

    # 蔡江
    (9, 4, "鹰潭市委常委、统战部部长", "2021-09", "至今", "副厅级", "兼市政协党组副书记"),

    # 褚小涛
    (10, 5, "鹰潭市委常委、政法委书记", "约2021", "至今", "副厅级", ""),

    # 其他副市长
    (11, 7, "鹰潭市副市长", "至今", "至今", "副厅级", "民建"),
    (12, 7, "鹰潭市副市长、党组成员", "至今", "至今", "副厅级", ""),
    (13, 7, "鹰潭市副市长、党组成员、市公安局局长", "至今", "至今", "副厅级", ""),
    (13, 8, "鹰潭市公安局局长", "至今", "至今", "正处级", "兼"),
    (14, 7, "鹰潭市副市长、党组成员", "至今", "至今", "副厅级", ""),
    (15, 7, "鹰潭市政府秘书长、党组成员", "至今", "至今", "正处级", ""),

    # 张子建（前任市长）
    (16, 7, "鹰潭市人民政府市长", "2021-04", "2024-12", "正厅级", ""),
    (16, 14, "楚雄州委书记", "2024-10", "至今", "正厅级", "跨省调任"),

    # 陈敏（前任市长）
    (17, 7, "鹰潭市人民政府市长", "2020-06", "2021-03", "正厅级", ""),

    # 许南吉
    (23, 1, "鹰潭市委书记", "2021-12", "2025-09", "正厅级", ""),
    (23, 15, "江西省财政厅厅长", "2025-09", "至今", "正厅级", ""),
]

# ── Relationships (person_a, person_b, type, context, overlap_org, overlap_period) ──
relationships = [
    # Current leadership relationships
    (1, 2, "党政搭档", "市委书记与市长搭档", "中共鹰潭市委员会/鹰潭市人民政府", "2026-01—至今"),
    (2, 5, "上下级", "市长与常务副市长", "鹰潭市人民政府", "2024-04—至今"),
    (3, 2, "前任专职副书记→市长", "黄金龙原为专职副书记，后转人大主任", "中共鹰潭市委员会", "2021-09—2024-12"),
    (1, 23, "前后任", "王亚联接替许南吉为市委书记", "中共鹰潭市委员会", "2026年交接"),
    (2, 16, "前后任", "王亚青接替张子建为市长", "鹰潭市人民政府", "2024-12交接"),
    (16, 17, "前后任", "张子建接替陈敏为市长", "鹰潭市人民政府", "2021年交接"),

    # Exchange network
    (23, 15, "前后任（调度）", "许南吉调任省财政厅", "江西省", "2025-09"),
    (24, 1, "同系统交接", "黄喜忠曾任鹰潭书记后调赣州", "全省地市书记", "2021-2026"),
    (16, 14, "跨省调动", "张子建鹰潭→楚雄跨省", "跨省", "2024-10"),

    # 王亚青 career arc
    (2, 21, "央企转党政", "王亚青从中电科转入省委组织部", "央企→党政", "约2023"),
]

# ── Helpers ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_role_color(name, post):
    """Return R,G,B color string based on role."""
    post = post or ""
    if "书记" in post and "纪委" not in post and "政法" not in post:
        return "255,50,50" if "市委" in post or "县委" in post else "220,50,50"
    if "市长" in post or "区长" in post or "县长" in post or "副市长" in post or "副区长" in post:
        return "50,100,255"
    if "纪委" in post or "监委" in post:
        return "255,165,0"
    if "政协" in post:
        return "180,100,200"
    if "人大" in post:
        return "100,150,200"
    return "100,100,100"

def is_top_leader(post):
    post = post or ""
    return "市委书记" in post or "市长" in post and "副" not in post

def person_size(post):
    return 20.0 if is_top_leader(post) else 12.0

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

# ── BUILD DATABASE ──

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    );
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute("""
        INSERT OR REPLACE INTO persons
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"],
          p["birth"], p["birthplace"], p["education"],
          p["party_join"], p["work_start"],
          p["current_post"], p["current_org"], p["source"]))

for o in orgs:
    cur.execute("""
        INSERT OR REPLACE INTO organizations
        VALUES (?,?,?,?,?,?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?)
    """, pos)

for r in relationships:
    cur.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)
    """, r)

conn.commit()
conn.close()
print(f"✅ Database written: {DB_PATH}")

# ── BUILD GEXF ──

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>鹰潭市领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="birth" type="string"/>')
lines.append('      <attribute id="3" title="birthplace" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')

# Person nodes
for p in persons:
    c = person_role_color(p["name"], p["current_post"])
    sz = person_size(p["current_post"])
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in orgs:
    c = org_color(o["type"])
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('          <attvalue for="2" value=""/>')
    lines.append('          <attvalue for="3" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# person → org (worked_at)
for pos in positions:
    eid += 1
    person_id, org_id, title, start, end = pos[0], pos[1], pos[2], pos[3], pos[4]
    period = f"{start}—{end}" if start and end else start or ""
    lines.append(f'      <edge id="{eid}" source="p{person_id}" target="o{org_id}" label="{esc(title)}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person ↔ person (relationships)
for r in relationships:
    eid += 1
    pa, pb, rtype, ctx, org, period = r
    lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF written: {GEXF_PATH}")

# ── Summary ──
print(f"\n📊 Summary:")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(orgs)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")
print(f"  Database: {DB_PATH}")
print(f"  GEXF Graph: {GEXF_PATH}")
print("Done.")
