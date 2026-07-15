#!/usr/bin/env python3
"""
Build 寻乌县 (Xunwu County) government personnel network database and GEXF graph.

寻乌县 is a county under 赣州市, 江西省.
Researched 2026-07-15 via Baidu Baike, 寻乌县政府网站, news reports.

Current leadership (as of 2026-07-15):
- 黄斌: 寻乌县委书记 (appointed ~2026-07, born 1983)
  - Previously: 崇义县长, 寻乌县委常委/宣传部长, 共青团赣州市委副书记
- 何善祥: 寻乌县委副书记、县长 (since 2021.08)
  - Previously: 全南县委副书记, 上犹县委常委/副县长

Previous leaders:
- 蓝贤林: 寻乌县委书记 2021.08-2026, promoted to 瑞金市委书记
- 柯岩松: 寻乌县委书记 ~2016-2021
- 杨永飞: 寻乌县长 ~2016-2021

Key cross-county connections:
- 韩相云: started in 寻乌 (副县长→常委/政法委), now 大余县委书记
- 黄斌: from 崇义县长 → 寻乌县委书记 (incoming cross-county)
- 蓝贤林: from 寻乌县委书记 → 瑞金市委书记 (outgoing promotion)
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in BASE:
    # Running from staging directory
    REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
    DB_PATH = os.path.join(BASE, "寻乌县_network.db")
    GEXF_PATH = os.path.join(BASE, "寻乌县_network.gexf")
else:
    # Running from repo root (canonical)
    REPO_ROOT = BASE
    DB_PATH = os.path.join(REPO_ROOT, "data/database/寻乌县_network.db")
    GEXF_PATH = os.path.join(REPO_ROOT, "data/graph/寻乌县_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# DATA
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

persons = [
    # ---- Current Core Leaders ----
    {
        "id": 1,
        "name": "黄斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983",
        "birthplace": "江西",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委书记",
        "current_org": "中共寻乌县委员会",
        "source": "网易新闻2026-07-10报道 + 寻乌县政府网站 xunwu.gov.cn",
    },
    {
        "id": 2,
        "name": "何善祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "江西赣州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委副书记、县长",
        "current_org": "寻乌县人民政府",
        "source": "新浪财经2024-08-20报道 + 寻乌县政府网站",
    },
    # ---- Former Core Leaders ----
    {
        "id": 3,
        "name": "蓝贤林",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1979-10",
        "birthplace": "江西南康",
        "education": "法学硕士（中南财经政法大学）",
        "party_join": "中共党员（2001-12）",
        "work_start": "2005-09",
        "current_post": "瑞金市委书记、瑞金经开区党工委书记",
        "current_org": "中共瑞金市委员会",
        "source": "百度百科 baike.baidu.com/item/蓝贤林 — 2026-07-15 verified",
    },
    {
        "id": 4,
        "name": "柯岩松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任寻乌县委书记）",
        "current_org": "",
        "source": "江西发布2021-08-04：柯岩松不再兼任寻乌县委书记；公开报道2016-2021在任",
    },
    {
        "id": 5,
        "name": "杨永飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任寻乌县长）",
        "current_org": "",
        "source": "2021-08何善祥接任寻乌县长报道；2016-2021在任",
    },
    # ---- Standing Committee (县委常委) ----
    {
        "id": 6,
        "name": "王子康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委副书记",
        "current_org": "中共寻乌县委员会",
        "source": "百度百科——中国共产党寻乌县委员会",
    },
    {
        "id": 7,
        "name": "王冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委常委、常务副县长",
        "current_org": "寻乌县人民政府",
        "source": "寻乌县人民政府网公开报道",
    },
    {
        "id": 8,
        "name": "钟琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委常委、组织部部长",
        "current_org": "中共寻乌县委组织部",
        "source": "寻乌县人民政府网公开报道",
    },
    {
        "id": 9,
        "name": "曹欣欣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委常委、纪委书记",
        "current_org": "中共寻乌县纪律检查委员会",
        "source": "寻乌县人民政府网公开报道",
    },
    {
        "id": 10,
        "name": "谢欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委常委、政法委书记",
        "current_org": "中共寻乌县委政法委员会",
        "source": "寻乌县人民政府网公开报道",
    },
    {
        "id": 11,
        "name": "彭晨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委常委、宣传部部长",
        "current_org": "中共寻乌县委宣传部",
        "source": "寻乌县人民政府网公开报道",
    },
    {
        "id": 12,
        "name": "应锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "",
        "education": "研究生硕士学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寻乌县委常委、人武部政委",
        "current_org": "寻乌县人民武装部",
        "source": "寻乌县人民政府网站 xunwu.gov.cn — 2026-04-13",
    },
    # ---- Cross-county connections ----
    {
        "id": 13,
        "name": "韩相云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-07",
        "birthplace": "江西寻乌",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1995-08",
        "current_post": "大余县委书记",
        "current_org": "中共大余县委员会",
        "source": "data/persons/20260715-江西省-赣州市-县委书记-韩相云.json",
    },
]

organizations = [
    {"id": 1, "name": "中共寻乌县委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州寻乌"},
    {"id": 2, "name": "寻乌县人民政府", "type": "政府", "level": "县处级",
     "parent": "赣州市人民政府", "location": "江西赣州寻乌"},
    {"id": 3, "name": "中共寻乌县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共寻乌县委员会", "location": "江西赣州寻乌"},
    {"id": 4, "name": "中共寻乌县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共寻乌县委员会", "location": "江西赣州寻乌"},
    {"id": 5, "name": "中共寻乌县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共寻乌县委员会", "location": "江西赣州寻乌"},
    {"id": 6, "name": "中共寻乌县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共寻乌县委员会", "location": "江西赣州寻乌"},
    {"id": 7, "name": "寻乌县人民武装部", "type": "事业单位", "level": "县处级",
     "parent": "赣州军分区", "location": "江西赣州寻乌"},
    {"id": 8, "name": "中共瑞金市委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州瑞金"},
    {"id": 9, "name": "瑞金经济技术开发区", "type": "开发区", "level": "国家级经开区",
     "parent": "瑞金市人民政府", "location": "江西赣州瑞金"},
    {"id": 10, "name": "中共大余县委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州大余"},
    {"id": 11, "name": "中共崇义县委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州崇义"},
    {"id": 12, "name": "共青团赣州市委员会", "type": "群团", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州"},
]

positions = [
    # 黄斌 — current 寻乌县委书记
    {"id": 1, "person_id": 1, "org_id": 12, "title": "共青团赣州市委副书记、党组成员", "start": "", "end": "",
     "rank": "县处级副职", "note": "早期团口任职"},
    {"id": 2, "person_id": 1, "org_id": 6, "title": "寻乌县委常委、宣传部部长", "start": "", "end": "2021-08",
     "rank": "县处级副职", "note": "在原柯岩松/蓝贤林班子时期任宣传部长"},
    {"id": 3, "person_id": 1, "org_id": 11, "title": "崇义县委副书记、代县长→县长", "start": "2021-08", "end": "2026-07",
     "rank": "县处级正职", "note": "2021-08任代县长，次月当选县长"},
    {"id": 4, "person_id": 1, "org_id": 1, "title": "寻乌县委书记", "start": "2026-07", "end": "",
     "rank": "县处级正职", "note": "2026-07-07已以书记身份调研；接替蓝贤林"},
    # 何善祥 — current 县长
    {"id": 5, "person_id": 2, "org_id": 2, "title": "寻乌县委副书记、县长", "start": "2021-08", "end": "",
     "rank": "县处级正职", "note": "现任；2021-08提名为县长候选人"},
    {"id": 6, "person_id": 2, "org_id": 2, "title": "上犹县委常委、副县长", "start": "2016-08", "end": "2020-07",
     "rank": "县处级副职", "note": "上犹县委常委、副县长候选人→副县长"},
    {"id": 7, "person_id": 2, "org_id": 1, "title": "全南县委副书记", "start": "2020-07", "end": "2021-08",
     "rank": "县处级副职", "note": "任全南县委副书记一年后调任寻乌"},
    # 蓝贤林 — former 书记, now 瑞金市委书记
    {"id": 8, "person_id": 3, "org_id": 1, "title": "寻乌县委书记", "start": "2021-08", "end": "2026-06",
     "rank": "县处级正职", "note": "2021-08至~2026-06；后升任瑞金市委书记"},
    {"id": 9, "person_id": 3, "org_id": 8, "title": "瑞金市委书记", "start": "2026", "end": "",
     "rank": "县处级正职", "note": "现任；兼任瑞金经开区党工委书记"},
    {"id": 10, "person_id": 3, "org_id": 9, "title": "瑞金经开区党工委书记", "start": "2026", "end": "",
     "rank": "县处级正职", "note": "兼任"},
    # 蓝贤林 — earlier career
    {"id": 11, "person_id": 3, "org_id": 2, "title": "兴国县委常委、宣传部部长", "start": "2015-05", "end": "2018-06",
     "rank": "县处级副职", "note": "期间2016-2017挂职深圳福田区福田街道党工委副书记"},
    {"id": 12, "person_id": 3, "org_id": 2, "title": "赣州市政府副秘书长、办公室党组成员", "start": "2018-06", "end": "2019-11",
     "rank": "县处级副职", "note": "市政府办公厅党组成员→办公室党组成员"},
    {"id": 13, "person_id": 3, "org_id": 8, "title": "瑞金市委副书记、市长", "start": "2019-11", "end": "2021-08",
     "rank": "县处级正职", "note": "瑞金市委副书记→副市长/代市长→市长，兼瑞金经开区党工委副书记/管委会主任"},
    # 柯岩松 — 前任书记
    {"id": 14, "person_id": 4, "org_id": 1, "title": "寻乌县委书记", "start": "2016", "end": "2021-08",
     "rank": "县处级正职", "note": "前任书记；蓝贤林接任；具体去向待查"},
    # 杨永飞 — 前任县长
    {"id": 15, "person_id": 5, "org_id": 2, "title": "寻乌县长", "start": "2016", "end": "2021-08",
     "rank": "县处级正职", "note": "前任县长；何善祥接任；具体去向待查"},
    # Standing Committee 常委
    {"id": 16, "person_id": 6, "org_id": 1, "title": "寻乌县委副书记", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 7, "org_id": 2, "title": "寻乌县委常委、常务副县长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 18, "person_id": 8, "org_id": 3, "title": "寻乌县委常委、组织部部长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 19, "person_id": 9, "org_id": 4, "title": "寻乌县委常委、纪委书记", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 20, "person_id": 10, "org_id": 5, "title": "寻乌县委常委、政法委书记", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 21, "person_id": 11, "org_id": 6, "title": "寻乌县委常委、宣传部部长", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 22, "person_id": 12, "org_id": 7, "title": "寻乌县委常委、人武部政委", "start": "2021-10", "end": "",
     "rank": "县处级副职", "note": "现任；2021-10至今"},
    # 韩相云 — from 寻乌 to 大余
    {"id": 23, "person_id": 13, "org_id": 2, "title": "寻乌县副县长", "start": "2013", "end": "2016",
     "rank": "县处级副职", "note": "起家在寻乌"},
    {"id": 24, "person_id": 13, "org_id": 5, "title": "寻乌县委常委、政法委书记", "start": "2016", "end": "2020-03",
     "rank": "县处级副职", "note": "寻乌县委常委"},
    {"id": 25, "person_id": 13, "org_id": 10, "title": "大余县委副书记、县长→县委书记", "start": "2020", "end": "",
     "rank": "县处级正职", "note": "跨县晋升"},
]

relationships = [
    # 黄斌 × 何善祥 — 党政搭档（新一届）
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "黄斌（县委书记）与何善祥（县长）在寻乌县党政搭档（2026-07起）",
     "overlap_org": "寻乌县", "overlap_period": "2026-07至今"},
    # 黄斌的寻乌渊源 — 他之前就在寻乌当宣传部长
    {"id": 2, "person_a_id": 1, "person_b_id": 4, "type": "superior_subordinate",
     "context": "黄斌曾在柯岩松任县委书记期间任寻乌县委常委、宣传部部长",
     "overlap_org": "中共寻乌县委员会", "overlap_period": ""},
    # 蓝贤林 × 何善祥 — 前任党政搭档
    {"id": 3, "person_a_id": 3, "person_b_id": 2, "type": "党政搭档",
     "context": "蓝贤林（县委书记）与何善祥（县长）在寻乌县党政搭档（2021-2026）",
     "overlap_org": "寻乌县", "overlap_period": "2021-08至2026-06"},
    # 黄斌 × 蓝贤林 — 前后任书记
    {"id": 4, "person_a_id": 1, "person_b_id": 3, "type": "predecessor_successor",
     "context": "黄斌接替蓝贤林任寻乌县委书记",
     "overlap_org": "中共寻乌县委员会", "overlap_period": "2026-07"},
    # 蓝贤林 × 柯岩松 — 前后任书记
    {"id": 5, "person_a_id": 3, "person_b_id": 4, "type": "predecessor_successor",
     "context": "蓝贤林接替柯岩松任寻乌县委书记",
     "overlap_org": "中共寻乌县委员会", "overlap_period": "2021-08"},
    # 何善祥 × 杨永飞 — 前后任县长
    {"id": 6, "person_a_id": 2, "person_b_id": 5, "type": "predecessor_successor",
     "context": "何善祥接替杨永飞任寻乌县长",
     "overlap_org": "寻乌县人民政府", "overlap_period": "2021-08"},
    # 蓝贤林 × 黄斌 — 前后任书记
    {"id": 7, "person_a_id": 3, "person_b_id": 1, "type": "overlap",
     "context": "黄斌在蓝贤林任寻乌县委书记期间未直接共事（黄斌当时在崇义任县长），但两人之前在赣州体系有交叉",
     "overlap_org": "赣州市", "overlap_period": ""},
    # 蓝贤林 × 韩相云 — 寻乌前后继任
    {"id": 8, "person_a_id": 3, "person_b_id": 13, "type": "overlap",
     "context": "韩相云2013-2020在寻乌任副县长、常委；蓝贤林2021年起任书记，前后相接但未直接共事",
     "overlap_org": "寻乌县", "overlap_period": ""},
    # 何善祥 × 韩相云 — 寻乌先后任职
    {"id": 9, "person_a_id": 2, "person_b_id": 13, "type": "overlap",
     "context": "何善祥2021年起任寻乌县长；韩相云此前在寻乌任职（2013-2020），未直接共事",
     "overlap_org": "寻乌县", "overlap_period": ""},
    # 蓝贤林上级关系 with 班子成员
    {"id": 10, "person_a_id": 3, "person_b_id": 7, "type": "superior_subordinate",
     "context": "蓝贤林（书记）与王冬（常务副县长）在寻乌县党政班子共事",
     "overlap_org": "寻乌县", "overlap_period": "2021-2026"},
    {"id": 11, "person_a_id": 3, "person_b_id": 8, "type": "superior_subordinate",
     "context": "蓝贤林（书记）与钟琳（组织部长）在寻乌县委班子共事",
     "overlap_org": "中共寻乌县委员会", "overlap_period": "2021-2026"},
    {"id": 12, "person_a_id": 3, "person_b_id": 9, "type": "superior_subordinate",
     "context": "蓝贤林（书记）与曹欣欣（纪委书记）在寻乌县委班子共事",
     "overlap_org": "中共寻乌县委员会", "overlap_period": "2021-2026"},
    # 黄斌与班子成员的关系
    {"id": 13, "person_a_id": 1, "person_b_id": 7, "type": "superior_subordinate",
     "context": "黄斌（书记）与王冬（常务副县长）在寻乌县党政班子共事",
     "overlap_org": "寻乌县", "overlap_period": "2026-07至今"},
    {"id": 14, "person_a_id": 1, "person_b_id": 8, "type": "superior_subordinate",
     "context": "黄斌（书记）与钟琳（组织部长）在寻乌县委班子共事",
     "overlap_org": "中共寻乌县委员会", "overlap_period": "2026-07至今"},
    # 黄斌的跨县调任
    {"id": 15, "person_a_id": 1, "person_b_id": 4, "type": "predecessor_successor",
     "context": "黄斌之前在崇义县长任上，被调回寻乌任县委书记（他曾在寻乌任宣传部长）",
     "overlap_org": "寻乌县/崇义县", "overlap_period": "2026-07"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_sqlite():
    """Create SQLite database from data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("DROP TABLE IF EXISTS relationships")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS persons")
    
    c.execute("""CREATE TABLE persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT,
        source TEXT
    )""")
    c.execute("""CREATE TABLE organizations(
        id INTEGER PRIMARY KEY, name TEXT, type TEXT,
        level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY, person_a_id INTEGER, person_b_id INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")
    
    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"],
                   o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"],
                   pos["title"], pos["start"], pos["end"],
                   pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"],
                   r["type"], r["context"], r["overlap_org"],
                   r["overlap_period"]))
    
    conn.commit()
    
    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()
    
    return counts


def pcolor_viz(post):
    """Return viz:color RGB string based on post title."""
    post = post or ""
    if "县长" in post or "区长" in post or "市长" in post:
        if "副" not in post:
            return "50,100,230"
        return "80,140,230"
    if "书记" in post and ("区委" in post or "县委" in post or "市委" in post):
        return "230,50,50"
    if "书记" in post:
        return "230,50,50"
    if "常委" in post:
        return "180,100,180"
    return "120,120,120"


def ocolor_viz(otype):
    return {"党委": "255,200,200", "政府": "200,200,255",
            "开发区": "200,255,200", "群团": "255,220,255",
            "事业单位": "220,220,220"}.get(otype, "200,200,200")


def build_gexf():
    """Build GEXF graph file."""
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus-junior</creator>')
    lines.append(f'    <description>寻乌县领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    
    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        c = pcolor_viz(p.get("current_post",""))
        pid = p["id"]
        if pid in [1, 2]:
            sz = "20.0"
        elif pid in [3, 4, 5]:
            sz = "15.0"
        else:
            sz = "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes - Organizations
    for o in organizations:
        c = ocolor_viz(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0","organization"),("1",""),("2",o.get("location","")),("3","")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0",r["type"]),("1",""),("2",""),("3",r.get("context",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(f"寻乌县 (Xunwu County) — Government Personnel Network Builder")
    print(f"Date: {today}")
    print("=" * 70)
    
    # SQLite
    print(f"\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ DB: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")
    
    # GEXF
    print(f"\n▶ Building GEXF graph...")
    tn, te = build_gexf()
    print(f"  ✓ GEXF: {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")
    
    # Verify
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"DB not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF not created: {GEXF_PATH}")
    
    if errors:
        print(f"\n✗ ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
        exit(1)
    else:
        print(f"\n✓ BUILD COMPLETE — all files created successfully")
