#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 青云谱区 leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/qingyunpu_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/qingyunpu_network.gexf")

# ── PERSONS ──
persons = [
    # Current 区委
    {"id":1,"name":"罗国栋","gender":"男","ethnicity":"汉族","birth":"1981-10","birthplace":"江西吉水","education":"中央党校研究生","party_join":"2001-06","work_start":"2003-07","current_post":"青云谱区委书记","current_org":"中共南昌市青云谱区委员会","source":"https://qyp.nc.gov.cn"},
    {"id":2,"name":"洪略","gender":"男","ethnicity":"汉族","birth":"1991-01","birthplace":"江西余干","education":"法学博士","party_join":"","work_start":"2018-08","current_post":"青云谱区委副书记、代区长","current_org":"南昌市青云谱区人民政府","source":"https://qyp.nc.gov.cn"},
    {"id":3,"name":"林峰","gender":"男","ethnicity":"汉族","birth":"1978-10","birthplace":"江西玉山","education":"在职研究生/工商管理硕士","party_join":"","work_start":"","current_post":"青云谱区委副书记","current_org":"中共南昌市青云谱区委员会","source":"https://qyp.nc.gov.cn"},
    {"id":4,"name":"黄华辉","gender":"男","ethnicity":"汉族","birth":"1978-01","birthplace":"江西临川","education":"研究生/法律硕士","party_join":"","work_start":"","current_post":"青云谱区委常委、政法委书记","current_org":"中共南昌市青云谱区委员会","source":"https://qyp.nc.gov.cn"},
    {"id":5,"name":"滕作鹏","gender":"男","ethnicity":"汉族","birth":"1975-11","birthplace":"江西新建","education":"中央党校在职大学","party_join":"","work_start":"","current_post":"青云谱区委常委、宣传部部长","current_org":"中共南昌市青云谱区委员会","source":"https://qyp.nc.gov.cn"},
    {"id":6,"name":"杨柳","gender":"女","ethnicity":"汉族","birth":"1984-11","birthplace":"江西南昌","education":"研究生","party_join":"","work_start":"","current_post":"青云谱区委常委、组织部部长","current_org":"中共南昌市青云谱区委员会","source":"https://qyp.nc.gov.cn"},
    {"id":7,"name":"李军","gender":"男","ethnicity":"汉族","birth":"1981-09","birthplace":"江西南昌","education":"研究生","party_join":"","work_start":"","current_post":"青云谱区委常委、纪委书记、监委主任","current_org":"中共南昌市青云谱区纪律检查委员会","source":"https://qyp.nc.gov.cn"},
    {"id":8,"name":"廖子君","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"研究生","party_join":"","work_start":"","current_post":"青云谱区委常委、统战部部长","current_org":"中共南昌市青云谱区委员会","source":"https://qyp.nc.gov.cn"},
    {"id":9,"name":"聂剑波","gender":"男","ethnicity":"汉族","birth":"1979-10","birthplace":"江西丰城","education":"解放军通信工程学院","party_join":"","work_start":"","current_post":"青云谱区委常委、人武部政委","current_org":"南昌市青云谱区人民武装部","source":"https://qyp.nc.gov.cn"},

    # Current 政府
    {"id":10,"name":"聂洪明","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"江西南昌","education":"在职大学/经济学学士","party_join":"","work_start":"","current_post":"青云谱区副区长","current_org":"南昌市青云谱区人民政府","source":"https://qyp.nc.gov.cn"},
    {"id":11,"name":"夏玉龙","gender":"男","ethnicity":"汉族","birth":"1971-02","birthplace":"江西南昌","education":"省委党校研究生","party_join":"","work_start":"","current_post":"青云谱区副区长、公安分局局长","current_org":"南昌市公安局青云谱分局","source":"https://qyp.nc.gov.cn"},
    {"id":12,"name":"胡启明","gender":"女","ethnicity":"汉族","birth":"1977-05","birthplace":"江西吉安","education":"法律本科","party_join":"民革","work_start":"","current_post":"青云谱区副区长","current_org":"南昌市青云谱区人民政府","source":"https://qyp.nc.gov.cn"},
    {"id":13,"name":"徐冀","gender":"男","ethnicity":"汉族","birth":"1983-07","birthplace":"","education":"硕士研究生","party_join":"","work_start":"","current_post":"青云谱区副区长","current_org":"南昌市青云谱区人民政府","source":"https://qyp.nc.gov.cn"},

    # Predecessors
    {"id":14,"name":"叶修堂","gender":"男","ethnicity":"汉族","birth":"1974-01","birthplace":"江西永修","education":"博士研究生","party_join":"1997-05","work_start":"1995-09","current_post":"南昌市人大常委会办公室主任","current_org":"南昌市人大常委会","source":"https://baike.baidu.com/item/%E5%8F%B6%E4%BF%AE%E5%A0%82/18718448"},
    {"id":15,"name":"汪众华","gender":"男","ethnicity":"汉族","birth":"1979-11","birthplace":"江西都昌","education":"研究生（江西财经大学人力资源+省委党校区域经济学）","party_join":"2003-11","work_start":"2003-06","current_post":"南昌市文联党组书记","current_org":"南昌市文学艺术界联合会","source":"https://baike.baidu.hk/item/%E6%B1%AA%E4%BC%97%E5%8D%8E"},

    # Cross-district connections with Qingyunpu history
    {"id":16,"name":"帅志","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"江西南昌","education":"省委党校研究生，法学学士","party_join":"2001-06","work_start":"1996-09","current_post":"南昌县委副书记、县长","current_org":"南昌县人民政府","source":"https://baike.baidu.com/item/%E5%B8%85%E5%BF%97"},
    {"id":17,"name":"徐志勇","gender":"男","ethnicity":"汉族","birth":"1981-07","birthplace":"江西丰城","education":"南昌大学在职研究生（公共管理）","party_join":"2002-01","work_start":"2002-07","current_post":"南昌县委常委、常务副县长","current_org":"南昌县人民政府","source":"https://baike.baidu.com/item/%E5%BE%90%E5%BF%97%E5%8B%87/55781241"},
    {"id":18,"name":"熊辉","gender":"男","ethnicity":"汉族","birth":"1981-03","birthplace":"江西奉新","education":"博士研究生","party_join":"","work_start":"","current_post":"安义县委书记","current_org":"中共安义县委员会","source":"https://baike.baidu.com/item/%E7%86%8A%E8%BE%89"},
    {"id":19,"name":"陈翔","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"江西樟树","education":"江西财经大学工业经济学学士","party_join":"1997-01","work_start":"1992-08","current_post":"南昌市政府二级巡视员","current_org":"南昌市人民政府","source":"https://baike.baidu.com/item/%E9%99%88%E7%BF%94/1774035"},
    {"id":20,"name":"聂红兵","gender":"男","ethnicity":"汉族","birth":"1980-11","birthplace":"江西南昌县","education":"省委党校在职研究生","party_join":"1999-05","work_start":"1999-08","current_post":"进贤县委常委、副县长","current_org":"进贤县人民政府","source":"https://baike.baidu.com/item/%E8%81%82%E7%BA%A2%E5%85%B5/64020468"},
    {"id":21,"name":"吴江辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原青云谱区委书记，去向待查）","current_org":"","source":"https://news.sina.com.cn/c/2021-07-24/doc-ikqciyzk5825981.shtml"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共南昌市青云谱区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市青云谱区"},
    {"id":2,"name":"南昌市青云谱区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市青云谱区"},
    {"id":3,"name":"南昌市青云谱区纪律检查委员会","type":"党委","level":"区级","parent":"南昌市纪律检查委员会","location":"江西省南昌市青云谱区"},
    {"id":4,"name":"南昌市公安局青云谱分局","type":"政府","level":"区级","parent":"南昌市公安局","location":"江西省南昌市青云谱区"},
    {"id":5,"name":"南昌市青云谱区人民武装部","type":"政府","level":"区级","parent":"南昌警备区","location":"江西省南昌市青云谱区"},
    {"id":6,"name":"南昌市人大常委会","type":"人大","level":"市级","parent":"","location":"江西省南昌市"},
    {"id":7,"name":"南昌市文学艺术界联合会","type":"群团","level":"市级","parent":"","location":"江西省南昌市"},
    {"id":8,"name":"南昌市人民政府","type":"政府","level":"市级","parent":"","location":"江西省南昌市"},
    {"id":9,"name":"中共南昌市委员会","type":"党委","level":"市级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":10,"name":"南昌县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市南昌县"},
    {"id":11,"name":"中共南昌县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市南昌县"},
    {"id":12,"name":"中共安义县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市安义县"},
    {"id":13,"name":"安义县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市安义县"},
    {"id":14,"name":"进贤县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市进贤县"},
    {"id":15,"name":"中共进贤县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市进贤县"},
    {"id":16,"name":"江西省工业和信息化委员会","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":17,"name":"南昌日报社","type":"事业单位","level":"市级","parent":"中共南昌市委员会","location":"江西省南昌市"},
    {"id":18,"name":"南昌经济技术开发区","type":"开发区","level":"国家级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":19,"name":"南昌市信访局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":20,"name":"南昌市纪委监委","type":"党委","level":"市级","parent":"中共南昌市委员会","location":"江西省南昌市"},
]

# ── POSITIONS ──
positions = [
    # 罗国栋(1) — current 区委书记
    {"id":1,"person_id":1,"org_id":16,"title":"省工信委对外交流合作处处长","start":"~2017","end":"2020-06","rank":"正处级","note":""},
    {"id":2,"person_id":1,"org_id":11,"title":"南昌县委副书记（正县级）","start":"2020-06","end":"2021-08","rank":"正县级","note":""},
    {"id":3,"person_id":1,"org_id":13,"title":"安义县委副书记、代县长→县长","start":"2021-08","end":"2026-07","rank":"正处级","note":"2021.08任安义代县长，后当选县长"},
    {"id":4,"person_id":1,"org_id":1,"title":"青云谱区委书记","start":"2026-07-07","end":"","rank":"副厅级","note":"2026年7月南昌六县区联动调整上任"},

    # 洪略(2) — current 代区长
    {"id":5,"person_id":2,"org_id":9,"title":"[2018-2026年履历待查] 2018年8月参加工作，法学博士","start":"2018-08","end":"~2026","rank":"","note":"极其快速的晋升：8年从科员至副厅级代区长。1991年生，江西余干人，法学博士。"},
    {"id":6,"person_id":2,"org_id":1,"title":"青云谱区委副书记、代区长","start":"~2026-06","end":"","rank":"副厅级","note":"接替汪众华任代区长（待人大正式任命）"},

    # 林峰(3) — 区委副书记
    {"id":7,"person_id":3,"org_id":2,"title":"青云谱区委常委、副区长","start":"~2021","end":"~2026","rank":"副处级","note":"搜狗百科有收录"},
    {"id":8,"person_id":3,"org_id":1,"title":"青云谱区委副书记","start":"~2026","end":"","rank":"副处级","note":"晋升为专职副书记"},

    # 黄华辉(4) — 政法委书记
    {"id":9,"person_id":4,"org_id":1,"title":"青云谱区委常委、政法委书记","start":"","end":"","rank":"副处级","note":"江西临川人，1978年生，法律硕士背景"},

    # 滕作鹏(5) — 宣传部部长
    {"id":10,"person_id":5,"org_id":1,"title":"青云谱区委常委、宣传部部长","start":"","end":"","rank":"副处级","note":"江西新建人（本地晋升），1975年生"},

    # 杨柳(6) — 组织部部长
    {"id":11,"person_id":6,"org_id":1,"title":"青云谱区委常委、组织部部长","start":"","end":"","rank":"副处级","note":"女，1984年生，南昌人，年轻女性组工干部"},

    # 李军(7) — 纪委书记
    {"id":12,"person_id":7,"org_id":3,"title":"青云谱区委常委、纪委书记、监委主任","start":"","end":"","rank":"副处级","note":"1981年生，南昌人"},

    # 聂剑波(9) — 人武部政委
    {"id":13,"person_id":9,"org_id":5,"title":"青云谱区委常委、人武部政委","start":"","end":"","rank":"副处级","note":"1979年生，丰城人"},

    # 叶修堂(14) — former 区委书记
    {"id":14,"person_id":14,"org_id":17,"title":"南昌日报社党委书记、社长、总编辑","start":"~2008","end":"~2016","rank":"正处级","note":"高级编辑职称"},
    {"id":15,"person_id":14,"org_id":18,"title":"南昌经济技术开发区工委副书记、管委会副主任（挂职）","start":"2015-07","end":"2016-07","rank":"正处级","note":""},
    {"id":16,"person_id":14,"org_id":14,"title":"进贤县委副书记、代县长→县长","start":"~2016","end":"~2019","rank":"副厅级","note":""},
    {"id":17,"person_id":14,"org_id":1,"title":"青云谱区委书记","start":"~2019","end":"2026-07","rank":"副厅级","note":"任职约7年"},
    {"id":18,"person_id":14,"org_id":6,"title":"南昌市人大常委会办公室主任","start":"2026-07-10","end":"","rank":"正处级","note":"市十六届人大常委会第四十三次会议任命"},

    # 汪众华(15) — former 区长
    {"id":19,"person_id":15,"org_id":19,"title":"南昌市信访局副局长","start":"2011-12","end":"2015-07","rank":"副处级","note":"曾在南昌县委挂职"},
    {"id":20,"person_id":15,"org_id":11,"title":"南昌县委常委、农工部部长","start":"2015-07","end":"2016-09","rank":"副处级","note":""},
    {"id":21,"person_id":15,"org_id":11,"title":"南昌县委常委、宣传部部长","start":"2016-09","end":"~2020","rank":"副处级","note":""},
    {"id":22,"person_id":15,"org_id":1,"title":"青云谱区委副书记、副区长、代区长","start":"2021-08","end":"2021-10","rank":"正处级","note":""},
    {"id":23,"person_id":15,"org_id":2,"title":"青云谱区委副书记、区长","start":"2021-10","end":"~2026-06","rank":"正处级","note":"约5年任期"},
    {"id":24,"person_id":15,"org_id":7,"title":"南昌市文联党组书记","start":"~2026-07","end":"","rank":"正处级","note":"从区长调任文联——偏文化系统的平级调动"},

    # 帅志(16) — former 三家店街道书记 → 南昌县长
    {"id":25,"person_id":16,"org_id":1,"title":"青云谱区三家店街道党工委书记","start":"~2008","end":"2016","rank":"正科级","note":""},

    # 徐志勇(17) — former 青云谱常务副区长
    {"id":26,"person_id":17,"org_id":1,"title":"青云谱区委常委、纪委书记→常务副区长","start":"2021-09","end":"2024-10","rank":"副处级","note":""},
    {"id":27,"person_id":17,"org_id":11,"title":"南昌县委常委、常务副县长","start":"2024-10-25","end":"","rank":"副处级","note":""},

    # 熊辉(18) — former 青云谱区副区长→组织部长
    {"id":28,"person_id":18,"org_id":9,"title":"南昌市委组织部调研处副处长/处长","start":"2009","end":"2016","rank":"正科级","note":""},
    {"id":29,"person_id":18,"org_id":2,"title":"青云谱区副区长→区委常委、组织部长","start":"2016","end":"~2020","rank":"副处级","note":""},
    {"id":30,"person_id":18,"org_id":15,"title":"进贤县委副书记、县长","start":"~2021","end":"2026-07","rank":"正处级","note":""},
    {"id":31,"person_id":18,"org_id":12,"title":"安义县委书记","start":"2026-07","end":"","rank":"正处级","note":"2026年7月联动调整"},

    # 陈翔(19) — former 青云谱区委组织部长
    {"id":32,"person_id":19,"org_id":1,"title":"青云谱区委组织部长","start":"~2011","end":"~2014","rank":"副处级","note":""},
    {"id":33,"person_id":19,"org_id":11,"title":"南昌县委常委、常务副县长→县长→县委书记","start":"2014-11","end":"2025-02","rank":"副厅级","note":""},

    # 聂红兵(20) — former 青云谱区委办
    {"id":34,"person_id":20,"org_id":1,"title":"青云谱区委办公室副主任→主任","start":"~2007","end":"2017-05","rank":"正科级","note":"2011年因拉票被处分"},

    # 吴江辉(21) — former 青云谱区长→区委书记
    {"id":35,"person_id":21,"org_id":2,"title":"青云谱区委副书记、区长","start":"~2016","end":"~2021-07","rank":"正处级","note":""},
    {"id":36,"person_id":21,"org_id":1,"title":"（原青云谱区委书记，去向待查）","start":"~2021-08","end":"~2022","rank":"副厅级","note":"2021.07公示拟任县区党委正职"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 现任党政班子
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"罗国栋（区委书记）与洪略（代区长）为青云谱区党政一把手搭档，2026年7月新组成","overlap_org":"青云谱区","overlap_period":"2026-07至今"},
    {"id":2,"person_a":2,"person_b":15,"type":"职务接替","context":"洪略（代区长）接替汪众华（原区长）任青云谱区政府负责人","overlap_org":"青云谱区人民政府","overlap_period":"不重叠（前后任）"},
    {"id":3,"person_a":1,"person_b":14,"type":"职务接替","context":"罗国栋（区委书记）接替叶修堂（原区委书记）任青云谱区委负责人","overlap_org":"中共青云谱区委","overlap_period":"不重叠（前后任）"},

    # 前任区委书记→去向
    {"id":4,"person_a":14,"person_b":21,"type":"职务接替","context":"叶修堂接替吴江辉任青云谱区委书记（约2021年）","overlap_org":"青云谱区委","overlap_period":"不重叠（前后任）"},

    # 青云谱区→南昌县通道
    {"id":5,"person_a":17,"person_b":16,"type":"青云谱→南昌县","context":"徐志勇（青云谱常务副区长→南昌县常务副县长）与帅志（青云谱三家店街道书记→南昌县长）均从青云谱调南昌县","overlap_org":"青云谱区→南昌县","overlap_period":"2024-10至今（南昌县同事）"},
    {"id":6,"person_a":19,"person_b":15,"type":"南昌县→青云谱","context":"陈翔（青云谱组织部长→南昌县委书记）与汪众华（南昌县委常委→青云谱区长）曾在南昌县共事","overlap_org":"南昌县","overlap_period":"2015-2016"},
    {"id":7,"person_a":16,"person_b":15,"type":"南昌县委同事","context":"帅志（南昌县县长）与汪众华（南昌县委宣传部部长）曾在南昌县委班子共事","overlap_org":"南昌县委","overlap_period":"2016-2020"},

    # 青云谱→安义通道
    {"id":8,"person_a":1,"person_b":18,"type":"安义→青云谱双向通道","context":"罗国栋（安义县长→青云谱书记）与熊辉（青云谱组织部长→安义县委书记）形成青云谱与安义之间的干部双向交流","overlap_org":"青云谱区/安义县","overlap_period":"2026-07至今"},

    # 青云谱→进贤通道
    {"id":9,"person_a":14,"person_b":20,"type":"进贤→青云谱→进贤","context":"叶修堂（进贤县长→青云谱书记）与聂红兵（青云谱区委办→进贤副县长）均在进贤与青云谱之间流动","overlap_org":"进贤县/青云谱区","overlap_period":"~2016-2019"},
    {"id":10,"person_a":1,"person_b":18,"type":"安义同城","context":"罗国栋（安义县长）与熊辉（进贤县长→安义书记）在2026年7月联动调整后均抵达安义/青云谱","overlap_org":"安义县","overlap_period":"2021-2026"},
]

# ── BUILD SQLITE ──
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# ── BUILD GEXF ──
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "区委书记" in post: return "255,50,50"
    elif "区长" in post or "副区长" in post or "代区长" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    elif "政法委" in post: return "150,100,200"
    elif "宣传部" in post: return "100,200,150"
    elif "组织部" in post: return "200,150,100"
    elif "统战部" in post: return "200,100,150"
    elif "人武部" in post: return "100,150,100"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","群团":"255,220,255","事业单位":"220,220,220","开发区":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>青云谱区领导班子工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = "20.0" if "书记" in p.get("current_post","") and "区委" in p.get("current_post","") else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalue>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalue>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
