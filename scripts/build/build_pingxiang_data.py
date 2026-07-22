#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 萍乡市 (Pingxiang) mayoral/leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/pingxiang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/pingxiang_network.gexf")

PERSONS = [
    # Current top leaders
    {"id":"px_yu_zhengkun","name":"余正琨","gender":"男","ethnicity":"汉族","birth":"1971-01","birthplace":"江西共青城","education":"","party_join":"","work_start":"","current_post":"萍乡市委书记","current_org":"中共萍乡市委员会","source":"https://zh.wikipedia.org/wiki/萍乡市"},
    {"id":"px_fu_zhenghua","name":"傅正华","gender":"男","ethnicity":"汉族","birth":"1969-08","birthplace":"江西吉安县","education":"南昌大学/法学学士","party_join":"1998-12","work_start":"1992-08","current_post":"萍乡市委副书记、市长","current_org":"萍乡市人民政府","source":"https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"},
    {"id":"px_bao_fengting","name":"鲍峰庭","gender":"男","ethnicity":"汉族","birth":"1968-03","birthplace":"江西万载","education":"江西农业大学/大学，工程硕士","party_join":"1989-06","work_start":"1990-07","current_post":"萍乡市委专职副书记","current_org":"中共萍乡市委员会","source":"https://zh.wikipedia.org/wiki/鲍峰庭"},
    {"id":"px_yan_xiaolong","name":"颜小龙","gender":"男","ethnicity":"汉族","birth":"1968-01","birthplace":"江西芦溪","education":"","party_join":"","work_start":"","current_post":"萍乡市人大常委会主任","current_org":"萍乡市人大常委会","source":"https://district.ce.cn/newarea/sddy/202501/09/t20250109_39261308.shtml"},
    {"id":"px_nie_xiaokui","name":"聂晓葵","gender":"女","ethnicity":"汉族","birth":"1966-01","birthplace":"江西芦溪","education":"","party_join":"","work_start":"","current_post":"萍乡市政协主席","current_org":"政协萍乡市委员会","source":"https://district.ce.cn/newarea/sddy/202110/23/t20211023_37022788.shtml"},
    {"id":"px_peng_haibao","name":"彭海宝","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"萍乡市委常委、市纪委书记","current_org":"中共萍乡市纪律检查委员会","source":"https://zh.wikipedia.org/wiki/江西省监察委员会"},
    # Predecessors: Mayors
    {"id":"px_xiong_yunlang","name":"熊运浪","gender":"男","ethnicity":"汉族","birth":"1968-11","birthplace":"江西南昌","education":"","party_join":"","work_start":"","current_post":"江西省委政法委副书记（原萍乡市长）","current_org":"中共江西省委政法委员会","source":"https://zh.wikipedia.org/wiki/熊运浪"},
    {"id":"px_liu_shuo","name":"刘烁","gender":"男","ethnicity":"汉族","birth":"1970-02","birthplace":"山东诸城","education":"南开大学双学士","party_join":"","work_start":"","current_post":"上饶市委书记（原萍乡市长/书记）","current_org":"中共上饶市委员会","source":"https://zh.wikipedia.org/wiki/刘烁"},
    {"id":"px_li_jianghe","name":"李江河","gender":"男","ethnicity":"汉族","birth":"1963-10","birthplace":"河南内乡","education":"浙江大学/计算机硕士","party_join":"","work_start":"","current_post":"江西省人大社会建设委员会副主任委员（原萍乡市长）","current_org":"江西省人民代表大会","source":"https://zh.wikipedia.org/wiki/李江河"},
    {"id":"px_li_xiaobao","name":"李小豹","gender":"男","ethnicity":"汉族","birth":"1968-08","birthplace":"湖南永兴","education":"","party_join":"","work_start":"","current_post":"（原萍乡市长/书记，2022年主动投案/落马）","current_org":"","source":"https://zh.wikipedia.org/wiki/李小豹"},
    # Cross-city connections
    {"id":"px_yan_ganhui","name":"颜赣辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原萍乡副书记→景德镇市长→宜春书记，2020落马/判11年）","current_org":"","source":"https://zh.wikipedia.org/wiki/颜赣辉"},
    {"id":"px_deng_baosheng","name":"邓保生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原景德镇市委书记→宜春市委书记","current_org":"","source":"https://zh.wikipedia.org/wiki/邓保生"},
]

ORGANIZATIONS = [
    {"id":"px_party","name":"中共萍乡市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省萍乡市"},
    {"id":"px_gov","name":"萍乡市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省萍乡市"},
    {"id":"px_discipline","name":"中共萍乡市纪律检查委员会","type":"党委","level":"地市级","parent":"中共江西省纪律检查委员会","location":"江西省萍乡市"},
    {"id":"px_npc","name":"萍乡市人大常委会","type":"人大","level":"地市级","parent":"江西省人大常委会","location":"江西省萍乡市"},
    {"id":"px_cppcc","name":"政协萍乡市委员会","type":"政协","level":"地市级","parent":"政协江西省委员会","location":"江西省萍乡市"},
    {"id":"px_jiangxi_political_legal","name":"中共江西省委政法委员会","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":"px_shangrao_party","name":"中共上饶市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省上饶市"},
    {"id":"px_yichun_party","name":"中共宜春市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省宜春市"},
    {"id":"px_jiangxi_npc","name":"江西省人民代表大会","type":"人大","level":"省级","parent":"","location":"江西省南昌市"},
]

POSITIONS = [
    # 余正琨
    ("px_yu_zhengkun","px_party","萍乡市委书记","2026-05","至今","正厅级","接替刘烁"),
    # 傅正华（完整生涯）
    ("px_fu_zhenghua","px_gov","萍乡市委副书记、市长","2026-06","至今","正厅级","2026.06.25正式当选"),
    ("px_fu_zhenghua","px_gov","萍乡市代市长","2026-05","2026-06","正厅级","2026.05.28人大任命"),
    ("px_fu_zhenghua","px_gov","吉安市委常委、井冈山经开区党工委书记","~2024","2026-05","副厅级","2025.03以该身份出席央视"),
    ("px_fu_zhenghua","px_gov","吉安市副市长、井冈山管理局党工委书记、井冈山市委书记","~2021","~2024","副厅级","首次主政县级市"),
    ("px_fu_zhenghua","px_gov","吉安市财政局局长","~2019","~2021","正处级",""),
    ("px_fu_zhenghua","px_gov","吉安市统计局局长","~2016","~2019","正处级",""),
    ("px_fu_zhenghua","px_gov","峡江县委副书记、政法委书记","~2010s","~2016","副县级",""),
    ("px_fu_zhenghua","px_gov","峡江县委常委、副县长","~2010s","~2010s","副县级",""),
    ("px_fu_zhenghua","px_gov","吉安市政府办公室副主任","?","?","正科级","具体年份待查"),
    ("px_fu_zhenghua","px_gov","井冈山报社干部","1992-08","?","科员","职业生涯起步"),
    # 鲍峰庭（完整生涯）
    ("px_bao_fengting","px_party","萍乡市委专职副书记","2021-03","至今","副厅级",""),
    ("px_bao_fengting","px_gov","赣州市人大常委会副主任（兼石城县委书记）","2020","2021","副厅级","获评全国脱贫攻坚先进个人"),
    ("px_bao_fengting","px_gov","石城县委书记","2014","2020","正处级",""),
    ("px_bao_fengting","px_gov","石城县委副书记、县长","2011","2014","正处级",""),
    ("px_bao_fengting","px_gov","抚州市委副秘书长、市接待办主任","2008","2011","正处级",""),
    ("px_bao_fengting","px_gov","乐安县委常委、组织部部长兼统战部部长","2006","2008","副县级",""),
    ("px_bao_fengting","px_gov","崇仁县人民政府副县长","2005","2006","副县级",""),
    ("px_bao_fengting","px_party","江西省委农办综合处主任科员、改革处助理调研员","1998","2005","主任科员",""),
    ("px_bao_fengting","px_party","宜春地区行署办公室科员、副科长","1990","1998","科员",""),
    # 颜小龙
    ("px_yan_xiaolong","px_npc","萍乡市人大常委会主任","2025-01","至今","正厅级",""),
    # 聂晓葵
    ("px_nie_xiaokui","px_cppcc","萍乡市政协主席","2021-10","至今","正厅级",""),
    # 彭海宝
    ("px_peng_haibao","px_discipline","萍乡市委常委、市纪委书记","?","至今","副厅级","省监委→萍乡"),
    # 前市长们
    ("px_xiong_yunlang","px_gov","萍乡市长","2023-04","2026-05","正厅级",""),
    ("px_xiong_yunlang","px_jiangxi_political_legal","江西省委政法委副书记","2026-06","至今","正厅级",""),
    ("px_liu_shuo","px_gov","萍乡市长","2021-09","2023-03","正厅级",""),
    ("px_liu_shuo","px_party","萍乡市委书记","2023-03","2026-05","正厅级",""),
    ("px_liu_shuo","px_shangrao_party","上饶市委书记","2026-05","至今","正厅级",""),
    ("px_li_jianghe","px_gov","萍乡市长","2016-03","2021-09","正厅级",""),
    ("px_li_jianghe","px_jiangxi_npc","江西省人大社会建设委员会副主任委员","2021-09","至今","正厅级",""),
    ("px_li_xiaobao","px_gov","萍乡市长","2013-08","2016-03","正厅级",""),
    ("px_li_xiaobao","px_party","萍乡市委书记","2016-03","2021","正厅级","2022年主动投案"),
    # 跨市连接
    ("px_yan_ganhui","px_party","萍乡市委副书记","2011-08","2013-09","副厅级","赣西环线关键节点"),
    ("px_deng_baosheng","px_party","景德镇市委书记→宜春市委书记","2011-2013","~2013","正厅级",""),
]

RELATIONSHIPS = [
    ("px_fu_zhenghua","px_liu_shuo","职务接替","傅正华接替刘烁—但刘烁先升书记，熊运浪接任市长，傅正华接熊运浪","萍乡市人民政府","2023-2026"),
    ("px_xiong_yunlang","px_fu_zhenghua","职务接替","熊运浪→傅正华（萍乡市长前后任）","萍乡市人民政府","2026"),
    ("px_liu_shuo","px_xiong_yunlang","职务接替","刘烁升书记→熊运浪接市长","萍乡市人民政府","2023"),
    ("px_li_jianghe","px_liu_shuo","职务接替","李江河→刘烁（萍乡市长前后任）","萍乡市人民政府","2021"),
    ("px_li_xiaobao","px_li_jianghe","职务接替","李小豹→李江河（萍乡市长前后任）","萍乡市人民政府","2016"),
    ("px_fu_zhenghua","px_bao_fengting","党政搭档","市长×副书记","中共萍乡市委员会","2026-至今"),
    ("px_liu_shuo","px_yan_ganhui","跨市连接","刘烁（上饶书记）与颜赣辉（原上饶市长+宜春书记）在上饶市直管有交集","","2026"),
    ("px_yan_ganhui","px_deng_baosheng","跨市连接","颜赣辉路径（宜春→萍乡→景德镇→上饶→宜春）与邓保生（景德镇→宜春）形成赣西环线","","2011-2020"),
]

# ── BUILD DATABASE ──
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT, source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT, FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT, FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id));
""")

for p in PERSONS:
    c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in ORGANIZATIONS:
    c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in POSITIONS:
    c.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)", pos)
for r in RELATIONSHIPS:
    c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)", r)
conn.commit()

# ── GEXF ──
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def clr(post):
    if "书记" in post and "纪委" not in post and "副" not in post: return "255,50,50"
    if "市长" in post and "副" not in post: return "50,100,255"
    if "纪委" in post: return "255,165,0"
    if "人大" in post: return "100,150,200"
    if "政协" in post: return "150,100,200"
    return "100,100,100"

org_colors = {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200"}

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>萍乡市领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node"><attribute id="0" title="type" type="string"/><attribute id="1" title="role" type="string"/></attributes>')
lines.append('    <attributes class="edge"><attribute id="0" title="type" type="string"/><attribute id="1" title="label" type="string"/></attributes>')
lines.append('    <nodes>')
for p in PERSONS:
    c_ = clr(p["current_post"]).split(",")
    sz = "20.0" if ("市委书记" in p["current_post"] and "纪委" not in p["current_post"]) or ("市长" in p["current_post"] and "副" not in p["current_post"]) else "12.0"
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues><attvalue for="0" value="person"/><attvalue for="1" value="%s"/></attvalues>' % esc(p["current_post"]))
    lines.append(f'        <viz:color r="{c_[0]}" g="{c_[1]}" b="{c_[2]}"/><viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in ORGANIZATIONS:
    oc = org_colors.get(o["type"],"200,200,200").split(",")
    lines.append(f'      <node id="{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues><attvalue for="0" value="organization"/><attvalue for="1" value="%s"/></attvalues>' % esc(o["type"]))
    lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/><viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes><edges>')
eid = 0
for pos in POSITIONS:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="{pos[0]}" target="{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
    lines.append('        <attvalues><attvalue for="0" value="worked_at"/><attvalue for="1" value="%s"/></attvalues>' % esc(pos[2]))
    lines.append('      </edge>')
for r in RELATIONSHIPS:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="{r[0]}" target="{r[1]}" label="{esc(r[2])}" weight="2.0">')
    lines.append('        <attvalues><attvalue for="0" value="relationship"/><attvalue for="1" value="%s"/></attvalues>' % esc(r[3]))
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()
print(f"✅ DB: {DB_PATH}")
print(f"✅ GEXF: {GEXF_PATH}")
print(f"   Persons: {len(PERSONS)}, Orgs: {len(ORGANIZATIONS)}, Positions: {len(POSITIONS)}, Relationships: {len(RELATIONSHIPS)}")
