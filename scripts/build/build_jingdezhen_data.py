#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 景德镇市 (Jingdezhen) leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/jingdezhen_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/jingdezhen_network.gexf")

# ── PERSONS ──
persons = [
    # Current 市委
    {"id":1,"name":"陈克龙","gender":"男","ethnicity":"汉族","birth":"1976-12","birthplace":"未公开","education":"研究生，工学硕士","party_join":"","work_start":"","current_post":"景德镇市委书记","current_org":"中共景德镇市委员会","source":"中国经济网 http://district.ce.cn/newarea/sddy/202604/t20260427_2932496.shtml"},
    {"id":2,"name":"吴隽","gender":"男","ethnicity":"汉族","birth":"1969-02","birthplace":"江西都昌","education":"研究生，博士","party_join":"","work_start":"","current_post":"景德镇市委专职副书记","current_org":"中共景德镇市委员会","source":"https://baike.baidu.com/item/%E5%90%B4%E9%9A%BD/10683211"},
    {"id":3,"name":"薛强","gender":"男","ethnicity":"汉族","birth":"1976-03","birthplace":"江西安远","education":"省委党校研究生，工商管理硕士","party_join":"1997-04","work_start":"1997-07","current_post":"景德镇市委常委、常务副市长","current_org":"景德镇市人民政府","source":"https://www.thepaper.cn/newsDetail_forward_29300260"},
    {"id":4,"name":"林蓉","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"景德镇市委常委、组织部部长","current_org":"中共景德镇市委员会","source":"景德镇市政府官网新闻报道"},
    {"id":5,"name":"张龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"景德镇市委常委、宣传部部长（推测）","current_org":"中共景德镇市委员会","source":"景德镇市政府官网"},
    {"id":6,"name":"林卫春","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"景德镇市委常委","current_org":"中共景德镇市委员会","source":"景德镇市政府官网"},
    {"id":7,"name":"肖斐杰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"景德镇市委常委","current_org":"中共景德镇市委员会","source":"景德镇市政府官网"},
    {"id":8,"name":"魏冀","gender":"男","ethnicity":"汉族","birth":"1978-11","birthplace":"","education":"文学博士","party_join":"","work_start":"","current_post":"景德镇市委常委、副市长（挂职）","current_org":"景德镇市人民政府","source":"https://www.jdz.gov.cn/zwgk/glgk/llxx/"},
    {"id":9,"name":"董梅生","gender":"男","ethnicity":"汉族","birth":"1976-07","birthplace":"","education":"大学，法律硕士","party_join":"","work_start":"","current_post":"景德镇市委常委、市纪委书记、市监委主任","current_org":"中共景德镇市纪律检查委员会","source":"江西纪检监察网 2024-03"},
    # Current 政府(除陈克龙/薛强/魏冀外)
    {"id":10,"name":"江民强","gender":"男","ethnicity":"汉族","birth":"1971-09","birthplace":"","education":"工程硕士","party_join":"无党派","work_start":"","current_post":"景德镇市副市长","current_org":"景德镇市人民政府","source":"https://www.jdz.gov.cn/zwgk/glgk/llxx/"},
    {"id":11,"name":"罗文军","gender":"男","ethnicity":"汉族","birth":"1967-04","birthplace":"","education":"大学","party_join":"","work_start":"","current_post":"景德镇市副市长","current_org":"景德镇市人民政府","source":"https://www.jdz.gov.cn/zwgk/glgk/llxx/"},
    {"id":12,"name":"徐辉","gender":"男","ethnicity":"汉族","birth":"1967-03","birthplace":"","education":"硕士研究生","party_join":"","work_start":"","current_post":"景德镇市副市长","current_org":"景德镇市人民政府","source":"https://www.jdz.gov.cn/zwgk/glgk/llxx/"},
    {"id":13,"name":"高晓云","gender":"男","ethnicity":"汉族","birth":"1975-05","birthplace":"","education":"硕士研究生","party_join":"","work_start":"","current_post":"景德镇市副市长","current_org":"景德镇市人民政府","source":"https://www.jdz.gov.cn/zwgk/glgk/llxx/"},
    {"id":14,"name":"黄练","gender":"男","ethnicity":"汉族","birth":"1972-12","birthplace":"","education":"在职研究生","party_join":"","work_start":"","current_post":"景德镇市副市长、市公安局局长","current_org":"景德镇市公安局","source":"https://www.jdz.gov.cn/zwgk/glgk/llxx/"},
    {"id":15,"name":"黄建平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"景德镇市政府秘书长","current_org":"景德镇市人民政府","source":"https://www.jdz.gov.cn/zwgk/glgk/llxx/"},
    # 人大/政协
    {"id":16,"name":"俞小平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"景德镇市政协主席","current_org":"政协景德镇市委员会","source":"景德镇市政府官网"},
    {"id":17,"name":"鄢华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"景德镇市人大常委会主任","current_org":"景德镇市人大常委会","source":"Wikipedia 景德镇市"},
    # Predecessors
    {"id":18,"name":"胡雪梅","gender":"女","ethnicity":"汉族","birth":"1967-08","birthplace":"江西玉山","education":"在职研究生，法学博士","party_join":"","work_start":"","current_post":"江西省委宣传部副部长（原景德镇市委书记）","current_org":"中共江西省委宣传部","source":"https://www.163.com/dy/article/JB63G7VD0534A4SC.html"},
    {"id":19,"name":"刘锋","gender":"男","ethnicity":"汉族","birth":"1964-08","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原景德镇市委书记，2024年9月卸任，去向不明）","current_org":"","source":"https://www.163.com/dy/article/JB68E2J7053469LG.html"},
    {"id":20,"name":"钟志生","gender":"男","ethnicity":"汉族","birth":"1963-06","birthplace":"江西分宜","education":"","party_join":"","work_start":"","current_post":"（原景德镇市委书记，2024年9月被查，2025年2月双开）","current_org":"","source":"https://www.163.com/dy/article/JO4TERN90514R9P4.html"},
    # Cross-city connections
    {"id":21,"name":"姚亚平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原景德镇市委书记→上饶市委书记","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%A7%9A%E4%BA%9A%E5%B9%B3"},
    {"id":22,"name":"颜赣辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原景德镇市长→上饶市长→宜春市委书记（2020年落马）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E9%A2%9C%E8%B5%A3%E8%BE%89"},
    {"id":23,"name":"郭安","gender":"男","ethnicity":"汉族","birth":"1962","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原景德镇市委常委/常务副市长→南昌市长→鹰潭市委书记","current_org":"","source":"https://zh.wikipedia.org/wiki/%E9%83%AD%E5%AE%89_(1962%E5%B9%B4)"},
    {"id":24,"name":"刘祖三","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原景德镇市委副书记→鹰潭市委书记","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E7%A5%96%E4%B8%89"},
    {"id":25,"name":"许爱民","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原景德镇市委书记→省政协（落马）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E8%AE%B8%E7%88%B1%E6%B0%91"},
    {"id":26,"name":"梅亦","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原景德镇市长（2016-2018）→省医保局/文旅厅","current_org":"","source":"https://zh.wikipedia.org/wiki/%E6%A2%85%E4%BA%A6"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共景德镇市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省景德镇市"},
    {"id":2,"name":"景德镇市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省景德镇市"},
    {"id":3,"name":"中共景德镇市纪律检查委员会","type":"党委","level":"地市级","parent":"中共江西省纪律检查委员会","location":"江西省景德镇市"},
    {"id":4,"name":"景德镇市公安局","type":"政府","level":"地市级","parent":"江西省公安厅","location":"江西省景德镇市"},
    {"id":5,"name":"景德镇市人大常委会","type":"人大","level":"地市级","parent":"江西省人大常委会","location":"江西省景德镇市"},
    {"id":6,"name":"政协景德镇市委员会","type":"政协","level":"地市级","parent":"政协江西省委员会","location":"江西省景德镇市"},
    {"id":7,"name":"中共江西省委宣传部","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":8,"name":"工业和信息化部","type":"政府","level":"中央","parent":"国务院","location":"北京市"},
    {"id":9,"name":"景德镇陶瓷大学","type":"事业单位","level":"地市级","parent":"江西省教育厅","location":"江西省景德镇市"},
    {"id":10,"name":"中共上饶市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省上饶市"},
    {"id":11,"name":"中共宜春市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省宜春市"},
]

# ── POSITIONS (career timeline) ──
positions = [
    # 陈克龙 — complete career timeline
    {"person_id":1,"org_id":8,"title":"工业和信息化部规划司投资计划处处长","start":"~2010","end":"2017-12","rank":"正处级","note":"早期生涯未公开"},
    {"person_id":1,"org_id":8,"title":"工业和信息化部规划司副司长","start":"2017-12","end":"2019-12","rank":"副司级","note":""},
    {"person_id":1,"org_id":8,"title":"工业和信息化部装备工业一司副司长","start":"2020","end":"2021","rank":"副司级","note":""},
    {"person_id":1,"org_id":8,"title":"工业和信息化部原材料工业司司长（稀土办公室主任）","start":"2021","end":"2023-05","rank":"正司级","note":""},
    {"person_id":1,"org_id":8,"title":"工业和信息化部规划司司长","start":"2023-05","end":"2024-10","rank":"正司级","note":""},
    {"person_id":1,"org_id":1,"title":"景德镇市委副书记、市政府党组书记、代市长","start":"2024-10","end":"2025-01","rank":"正厅级","note":"央地交流空降"},
    {"person_id":1,"org_id":2,"title":"景德镇市人民政府市长","start":"2025-01","end":"2026-04","rank":"正厅级","note":""},
    {"person_id":1,"org_id":1,"title":"景德镇市委书记","start":"2026-04","end":"至今","rank":"正厅级","note":""},

    # 吴隽 — career timeline
    {"person_id":2,"org_id":9,"title":"景德镇陶瓷学院（现景德镇陶瓷大学）古陶瓷研究所所长","start":"~2007","end":"2009-07","rank":"正处级","note":"此前为教授/研究员，早期教育背景未知"},
    {"person_id":2,"org_id":9,"title":"景德镇陶瓷学院副院长","start":"2009-07","end":"2014-03","rank":"副厅级","note":""},
    {"person_id":2,"org_id":11,"title":"挂职新余市委常委、副市长","start":"2014-03","end":"2016-02","rank":"副厅级","note":"挂职两年"},
    {"person_id":2,"org_id":9,"title":"景德镇陶瓷大学副校长","start":"2016-02","end":"2016-10","rank":"副厅级","note":"学院更名大学"},
    {"person_id":2,"org_id":1,"title":"景德镇市委常委、秘书长","start":"2016-10","end":"2021-09","rank":"副厅级","note":"兼任宣传部部长至2017"},
    {"person_id":2,"org_id":1,"title":"景德镇市委专职副书记","start":"2021-09","end":"至今","rank":"副厅级","note":""},

    # 薛强 — career timeline
    {"person_id":3,"org_id":2,"title":"赣州市国际经济技术合作公司业务员、办公室副主任","start":"1997-07","end":"1999-04","rank":"科员","note":""},
    {"person_id":3,"org_id":2,"title":"大余县计委科员","start":"1999-04","end":"2001-08","rank":"科员","note":""},
    {"person_id":3,"org_id":2,"title":"大余县计委副主任","start":"2001-08","end":"2003-06","rank":"副科级","note":"其中2000.04-2003.06借调赣州市计委/项目办"},
    {"person_id":3,"org_id":2,"title":"赣州市项目办公室副主任","start":"2003-06","end":"2004","rank":"正科级","note":""},
    {"person_id":3,"org_id":2,"title":"赣州市发改委办公室主任","start":"2008-04","end":"2009-07","rank":"正科级","note":""},
    {"person_id":3,"org_id":2,"title":"赣州开发区发展规划局局长","start":"2009-07","end":"2011-05","rank":"副处级","note":""},
    {"person_id":3,"org_id":2,"title":"全南县委书记、县人大常委会主任","start":"2011-05","end":"2013-09","rank":"正处级","note":""},
    {"person_id":3,"org_id":2,"title":"龙南县委书记、龙南经济技术开发区党工委书记","start":"2013-09","end":"2016-08","rank":"副厅级","note":"2015.03-2016.01挂职环保部规划财务司副司长"},
    {"person_id":3,"org_id":2,"title":"赣南苏区振兴发展工作办公室主任","start":"2016-08","end":"2021-09","rank":"副厅级","note":""},
    {"person_id":3,"org_id":2,"title":"抚州市人民政府副市长","start":"2021-09","end":"2024-10","rank":"副厅级","note":""},
    {"person_id":3,"org_id":1,"title":"景德镇市委常委、市政府党组副书记、常务副市长","start":"2024-11","end":"至今","rank":"副厅级","note":"2024年11月13日任命"},

    # 董梅生
    {"person_id":9,"org_id":3,"title":"江西省纪委案件监督管理室副主任","start":"~2010s","end":"~2019","rank":"正处级","note":"早期履历未公开"},
    {"person_id":9,"org_id":3,"title":"江西省纪委监委纪检监察干部监督室主任","start":"~2019","end":"2021-02","rank":"正处级","note":""},
    {"person_id":9,"org_id":3,"title":"江西省纪委省监委案件监督管理室主任","start":"2021-02","end":"2023-11","rank":"正处级","note":""},
    {"person_id":9,"org_id":3,"title":"江西省纪委常委、省监委委员","start":"2023-11","end":"2025-03","rank":"副厅级","note":""},
    {"person_id":9,"org_id":3,"title":"景德镇市委常委、市纪委书记、市监委主任","start":"2025-04","end":"至今","rank":"副厅级","note":""},

    # 胡雪梅
    {"person_id":18,"org_id":2,"title":"景德镇市人民政府市长","start":"2021","end":"2024-09","rank":"正厅级","note":""},
    {"person_id":18,"org_id":1,"title":"景德镇市委书记","start":"2024-09","end":"2026-04","rank":"正厅级","note":""},
    {"person_id":18,"org_id":7,"title":"江西省委宣传部副部长","start":"2026-05","end":"至今","rank":"正厅级","note":""},

    # 刘锋
    {"person_id":19,"org_id":2,"title":"景德镇市人民政府市长","start":"2018","end":"2021-03","rank":"正厅级","note":""},
    {"person_id":19,"org_id":1,"title":"景德镇市委书记","start":"2021-03","end":"2024-09","rank":"正厅级","note":""},

    # 钟志生
    {"person_id":20,"org_id":1,"title":"景德镇市委书记","start":"2015-08","end":"2021-03","rank":"正厅级","note":""},

    # 当前政府班子成员 — 景德镇市人民政府任职
    {"person_id":3,"org_id":2,"title":"景德镇市委常委、常务副市长","start":"2024-11","end":"至今","rank":"副厅级","note":""},
    {"person_id":8,"org_id":2,"title":"景德镇市委常委、副市长（挂职）","start":"","end":"至今","rank":"副厅级","note":""},
    {"person_id":10,"org_id":2,"title":"景德镇市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    {"person_id":11,"org_id":2,"title":"景德镇市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    {"person_id":12,"org_id":2,"title":"景德镇市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    {"person_id":13,"org_id":2,"title":"景德镇市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    {"person_id":14,"org_id":4,"title":"景德镇市副市长、市公安局局长","start":"","end":"至今","rank":"副厅级","note":""},
    {"person_id":15,"org_id":2,"title":"景德镇市政府秘书长","start":"","end":"至今","rank":"正处级","note":""},

    # 俞小平
    {"person_id":16,"org_id":6,"title":"景德镇市政协主席","start":"2021-11","end":"至今","rank":"正厅级","note":""},

    # 鄢华
    {"person_id":17,"org_id":5,"title":"景德镇市人大常委会主任","start":"2026-01","end":"至今","rank":"正厅级","note":""},
]

# ── RELATIONSHIPS ──
relationships = [
    {"person_a":1,"person_b":3,"type":"党政搭档","context":"陈克龙（市委书记）与薛强（常务副市长）2024年11月同时到任景德镇，是同一批组织调配的新班子","overlap_org":"景德镇市人民政府","overlap_period":"2024-至今"},
    {"person_a":1,"person_b":2,"type":"党政搭档","context":"陈克龙（市委书记）与吴隽（专职副书记）是市委核心搭档","overlap_org":"中共景德镇市委员会","overlap_period":"2024-至今"},
    {"person_a":1,"person_b":18,"type":"职务接替","context":"陈克龙接替胡雪梅先后任景德镇市长（2025.01）和市委书记（2026.04），两人相继担任同一职务","overlap_org":"中共景德镇市委员会","overlap_period":"2024-2026"},
    {"person_a":18,"person_b":19,"type":"职务接替","context":"胡雪梅接替刘锋任景德镇市委书记（2024.09）","overlap_org":"中共景德镇市委员会","overlap_period":"2024"},
    {"person_a":19,"person_b":20,"type":"职务接替","context":"刘锋接替钟志生任景德镇市委书记（2021.03）","overlap_org":"中共景德镇市委员会","overlap_period":"2021"},
    {"person_a":20,"person_b":25,"type":"职务接替","context":"钟志生接替许爱民任景德镇市委书记","overlap_org":"中共景德镇市委员会","overlap_period":"2015"},
    {"person_a":21,"person_b":25,"type":"职务接替","context":"姚亚平→许爱民（景德镇市委书记先后任）","overlap_org":"中共景德镇市委员会","overlap_period":"2004"},
    {"person_a":22,"person_b":26,"type":"职务接替","context":"颜赣辉→梅亦（景德镇市长先后任）","overlap_org":"景德镇市人民政府","overlap_period":"2016"},
    {"person_a":22,"person_b":23,"type":"工作关系","context":"颜赣辉（景德镇市长）与郭安（景德镇市委常委/常务副市长）在景德镇政府同年共事","overlap_org":"景德镇市人民政府","overlap_period":"~2013-2016"},
    {"person_a":2,"person_b":16,"type":"工作关系","context":"吴隽与俞小平同为景德镇市四套班子领导成员","overlap_org":"中共景德镇市委员会","overlap_period":"2021-至今"},
    {"person_a":21,"person_b":10,"type":"跨市交流","context":"姚亚平从景德镇市委书记调任上饶市委书记，形成景德镇-上饶旋转门模式","overlap_org":"","overlap_period":"2003"},
    {"person_a":22,"person_b":10,"type":"跨市交流","context":"颜赣辉从景德镇市长调任上饶市长，延续景德镇-上饶旋转门模式","overlap_org":"","overlap_period":"2016"},
    {"person_a":24,"person_b":10,"type":"跨市交流","context":"刘祖三从景德镇市委副书记调往鹰潭市委书记，形成景德镇-鹰潭通道","overlap_org":"","overlap_period":"1994"},
    {"person_a":23,"person_b":10,"type":"跨市交流","context":"郭安在离开景德镇后历任南昌市长→鹰潭市委书记","overlap_org":"","overlap_period":"2011-2021"},
]

# ── BUILD DATABASE ──
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
    birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
         p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))

for o in organizations:
    cur.execute("""INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)""",
        (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)""",
        (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
        (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

conn.commit()

# ── BUILD GEXF ──
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    post = p["current_post"]
    if "书记" in post and ("市委" in post or "县委" in post or "区委" in post):
        if "纪委" not in post: return "255,50,50"  # Red for party secretary
    if "市长" in post or "市长" in post or "区长" in post or "县长" in post or "副县长" in post or "副区长" in post:
        return "50,100,255"  # Blue for government
    if "纪委" in post or "监委" in post:
        return "255,165,0"  # Orange for discipline
    if "人大" in post:
        return "100,150,200"
    if "政协" in post:
        return "150,100,200"
    return "100,100,100"  # Grey

def is_top_leader(p):
    post = p["current_post"]
    if "市委书记" in post and "纪委" not in post: return True
    if "市长" in post and "副市长" not in post: return True
    return False

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>景德镇市领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="label" type="string"/>')
lines.append('    </attributes>')

# Nodes: persons
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append('        </attvalues>')
    cs = c.split(",")
    lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: organizations
org_color_map = {
    "党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
    "政协": "255,240,200", "事业单位": "220,220,220", "群团": "255,220,255"
}
for o in organizations:
    c = org_color_map.get(o["type"], "200,200,200")
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    cs = c.split(",")
    lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges: positions (person -> organization)
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Edges: relationships (person <-> person)
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ── SUMMARY ──
conn.close()
print(f"✅ SQLite DB: {DB_PATH}")
print(f"✅ GEXF graph: {GEXF_PATH}")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")
print(f"   GEXF edges: {eid}")
