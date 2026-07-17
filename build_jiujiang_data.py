#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 九江市 (Jiujiang City) leadership network.

Covers: city-level leaders (party secretary, mayor, vice mayors, party committee),
plus key predecessors and cross-city connections.
"""
import os, sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data/database/jiujiang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/jiujiang_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# ID convention: jiujiang_{name_pinyin} for city-level figures
persons = [
    # ── Current leadership (city-level) ──
    {"id":"jiujiang_chen_yun","name":"陈云","gender":"男","ethnicity":"汉族",
     "birth":"1976-12","birthplace":"江西南昌","education":"江西师范大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"九江市委书记","current_org":"中共九江市委员会",
     "source":"https://zh.wikipedia.org/wiki/陈云_(1976年)"},
    {"id":"jiujiang_deng_yongxiang","name":"邓永翔","gender":"男","ethnicity":"汉族",
     "birth":"1977-02","birthplace":"江西南昌","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"九江市委副书记、市长","current_org":"九江市人民政府",
     "source":"https://zh.wikipedia.org/wiki/九江市"},
    {"id":"jiujiang_liao_qizhi","name":"廖奇志","gender":"女","ethnicity":"汉族",
     "birth":"1969-06","birthplace":"江西赣州","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"九江市人大常委会主任","current_org":"九江市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/九江市"},
    {"id":"jiujiang_zhan_yong","name":"占勇","gender":"男","ethnicity":"汉族",
     "birth":"1966-10","birthplace":"江西鹰潭","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"九江市政协主席","current_org":"政协九江市委员会",
     "source":"https://zh.wikipedia.org/wiki/九江市"},
    {"id":"jiujiang_du_shaohua","name":"杜少华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"九江市副市长","current_org":"九江市人民政府",
     "source":"http://www.jiujiang.gov.cn (2026年7月政务资讯)"},
    {"id":"jiujiang_ma_haiwei","name":"马海威","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"九江市副市长","current_org":"九江市人民政府",
     "source":"http://www.jiujiang.gov.cn (2026年7月政务资讯)"},

    # ── Predecessors ──
    {"id":"jiujiang_liu_wenhua","name":"刘文华","gender":"男","ethnicity":"汉族",
     "birth":"1968","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原九江市委书记，已离任）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/九江市"},
    {"id":"jiujiang_jiang_wending","name":"蒋文定","gender":"男","ethnicity":"汉族",
     "birth":"1975","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原九江市市长，已离任）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/九江市"},
    {"id":"jiujiang_xie_laifa","name":"谢来发","gender":"男","ethnicity":"汉族",
     "birth":"1967","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原九江市委书记，已落马）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/谢来发_(1967年)"},
    {"id":"jiujiang_yang_wenbin","name":"杨文斌","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原九江市市长，已落马）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/九江市"},
    {"id":"jiujiang_xie_yiping","name":"谢一平","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"江西省人大教科文卫委主任委员（原九江市长→省商务厅厅长）","current_org":"江西省人民代表大会",
     "source":"https://zh.wikipedia.org/wiki/九江市"},
    {"id":"jiujiang_lin_binyang","name":"林彬杨","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原九江市长→书记，已离任）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/林彬杨"},

    # ── Cross-city connections ──
    {"id":"jiujiang_liu_shuo","name":"刘烁","gender":"男","ethnicity":"汉族",
     "birth":"1970-02","birthplace":"山东诸城","education":"南开大学双学士",
     "party_join":"","work_start":"",
     "current_post":"上饶市委书记（原萍乡市长/书记→上饶书记，与陈云交接上饶）","current_org":"中共上饶市委员会",
     "source":"https://zh.wikipedia.org/wiki/刘烁"},
    {"id":"jiujiang_qiu_xiangjun","name":"邱向军","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"上饶市委副书记、市长（接替陈云）","current_org":"上饶市人民政府",
     "source":"https://zh.wikipedia.org/wiki/邱向军"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":"org_jj_party","name":"中共九江市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省九江市"},
    {"id":"org_jj_gov","name":"九江市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省九江市"},
    {"id":"org_jj_npc","name":"九江市人大常委会","type":"人大","level":"地市级","parent":"江西省人大常委会","location":"江西省九江市"},
    {"id":"org_jj_cppcc","name":"政协九江市委员会","type":"政协","level":"地市级","parent":"政协江西省委员会","location":"江西省九江市"},
    {"id":"org_jj_discipline","name":"中共九江市纪律检查委员会","type":"党委","level":"地市级","parent":"中共江西省纪律检查委员会","location":"江西省九江市"},

    # Provincial
    {"id":"org_jx_party","name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":"org_jx_gov","name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":"org_jx_npc","name":"江西省人民代表大会","type":"人大","level":"省级","parent":"","location":"江西省南昌市"},

    # Cross-city
    {"id":"org_sr_party","name":"中共上饶市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省上饶市"},
    {"id":"org_sr_gov","name":"上饶市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省上饶市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 陈云 (Chen Yun) ──
    {"person_id":"jiujiang_chen_yun","org_id":"org_jj_party","title":"九江市委书记","start":"2026-05","end":"","rank":"正厅级","note":"2026年5月6日上任"},
    {"person_id":"jiujiang_chen_yun","org_id":"org_sr_party","title":"上饶市委书记","start":"2021-12","end":"2026-05","rank":"正厅级","note":"接替史文斌"},
    {"person_id":"jiujiang_chen_yun","org_id":"org_sr_gov","title":"上饶市委副书记、市长","start":"2020-01","end":"2021-12","rank":"正厅级","note":"接替谢来发"},
    {"person_id":"jiujiang_chen_yun","org_id":"org_sr_gov","title":"上饶市代市长","start":"2019-12","end":"2020-01","rank":"正厅级","note":""},
    # 陈云 earlier career: details limited from public sources
    # He was a Jiangxi Normal University graduate, likely worked up through provincial system
    # before becoming Shangrao mayor. Exact earlier positions need more research.

    # ── 邓永翔 (Deng Yongxiang) ──
    {"person_id":"jiujiang_deng_yongxiang","org_id":"org_jj_gov","title":"九江市委副书记、市长","start":"2026-05","end":"","rank":"正厅级","note":"2026年5月上任"},
    # 邓永翔 earlier career: details limited from public sources
    # Known: Born in Nanchang 1977-02, became Jiujiang mayor in 2026-05.
    # Earlier positions not found in available public sources.

    # ── 廖奇志 (Liao Qizhi) ──
    {"person_id":"jiujiang_liao_qizhi","org_id":"org_jj_npc","title":"九江市人大常委会主任","start":"2021-10","end":"","rank":"正厅级","note":"女性，江西赣州人"},

    # ── 占勇 (Zhan Yong) ──
    {"person_id":"jiujiang_zhan_yong","org_id":"org_jj_cppcc","title":"九江市政协主席","start":"2021-01","end":"","rank":"正厅级","note":"江西鹰潭人"},

    # ── 杜少华 ──
    {"person_id":"jiujiang_du_shaohua","org_id":"org_jj_gov","title":"九江市副市长","start":"","end":"","rank":"副厅级","note":"现任；2026年7月见诸政务报道"},

    # ── 马海威 ──
    {"person_id":"jiujiang_ma_haiwei","org_id":"org_jj_gov","title":"九江市副市长","start":"","end":"","rank":"副厅级","note":"现任；2026年7月见诸政务报道"},

    # ── 刘文华 (predecessor party secretary) ──
    {"person_id":"jiujiang_liu_wenhua","org_id":"org_jj_party","title":"九江市委书记","start":"2022-11","end":"2026-05","rank":"正厅级","note":"接替谢来发"},
    {"person_id":"jiujiang_liu_wenhua","org_id":"org_jx_gov","title":"江西省审计厅厅长","start":"~2021","end":"2022-11","rank":"正厅级","note":"调任九江前职务"},

    # ── 蒋文定 (predecessor mayor) ──
    {"person_id":"jiujiang_jiang_wending","org_id":"org_jj_gov","title":"九江市委副书记、市长","start":"2023-05","end":"2026-05","rank":"正厅级","note":"接替杨文斌"},
    {"person_id":"jiujiang_jiang_wending","org_id":"org_jj_gov","title":"九江市代市长","start":"2023-04","end":"2023-05","rank":"正厅级","note":""},

    # ── 谢来发 ──
    {"person_id":"jiujiang_xie_laifa","org_id":"org_jj_party","title":"九江市委书记","start":"2021-03","end":"2022-05","rank":"正厅级","note":"任上落马"},
    {"person_id":"jiujiang_xie_laifa","org_id":"org_jj_gov","title":"九江市委副书记、市长","start":"2019-12","end":"2021-09","rank":"正厅级","note":"接替谢一平"},

    # ── 杨文斌 ──
    {"person_id":"jiujiang_yang_wenbin","org_id":"org_jj_gov","title":"九江市委副书记、市长","start":"2021-09","end":"2023-03","rank":"正厅级","note":"任上落马"},

    # ── 谢一平 ──
    {"person_id":"jiujiang_xie_yiping","org_id":"org_jj_gov","title":"九江市委副书记、市长","start":"2018-03","end":"2019-12","rank":"正厅级","note":""},
    {"person_id":"jiujiang_xie_yiping","org_id":"org_jx_npc","title":"江西省人大教科文卫委主任委员","start":"~2023","end":"","rank":"正厅级","note":"此前任省商务厅厅长"},

    # ── 林彬杨 ──
    {"person_id":"jiujiang_lin_binyang","org_id":"org_jj_gov","title":"九江市委副书记、市长","start":"2015-07","end":"2018-03","rank":"正厅级","note":""},
    {"person_id":"jiujiang_lin_binyang","org_id":"org_jj_party","title":"九江市委书记","start":"2018-03","end":"2021-03","rank":"正厅级","note":"由市长升任书记"},

    # ── Cross-city: 陈云 ↔ 刘烁 (上饶交接) ──
    {"person_id":"jiujiang_liu_shuo","org_id":"org_sr_party","title":"上饶市委书记","start":"2026-05","end":"","rank":"正厅级","note":"接替陈云调任九江后的空缺；原萍乡市委书记"},
    # 邱向军
    {"person_id":"jiujiang_qiu_xiangjun","org_id":"org_sr_gov","title":"上饶市委副书记、市长","start":"2021-12","end":"","rank":"正厅级","note":"接替陈云升书记后的市长空缺"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政一把手 ──
    {"person_a":"jiujiang_chen_yun","person_b":"jiujiang_deng_yongxiang",
     "type":"党政搭档","context":"陈云（市委书记）与邓永翔（市长）为九江市党政一把手",
     "overlap_org":"九江市","overlap_period":"2026-05至今"},

    # ── Mayor succession chain ──
    {"person_a":"jiujiang_deng_yongxiang","person_b":"jiujiang_jiang_wending",
     "type":"前后任","context":"邓永翔（2026.05接任市长）→ 蒋文定（2023-2026市长）",
     "overlap_org":"九江市人民政府","overlap_period":"不重叠（前后任）"},
    {"person_a":"jiujiang_jiang_wending","person_b":"jiujiang_yang_wenbin",
     "type":"前后任","context":"蒋文定（2023.05接任市长）→ 杨文斌（2021-2023市长，落马）",
     "overlap_org":"九江市人民政府","overlap_period":"不重叠（前后任）"},
    {"person_a":"jiujiang_yang_wenbin","person_b":"jiujiang_xie_laifa",
     "type":"前后任","context":"杨文斌（2021.09接任市长）→ 谢来发（2019-2021市长，升书记后落马）",
     "overlap_org":"九江市人民政府","overlap_period":"不重叠（前后任）"},
    {"person_a":"jiujiang_xie_laifa","person_b":"jiujiang_xie_yiping",
     "type":"前后任","context":"谢来发（2019.12接任市长）→ 谢一平（2018-2019市长）",
     "overlap_org":"九江市人民政府","overlap_period":"不重叠（前后任）"},
    {"person_a":"jiujiang_xie_yiping","person_b":"jiujiang_lin_binyang",
     "type":"前后任","context":"谢一平（2018.03接任市长）→ 林彬杨（2015-2018市长，升书记）",
     "overlap_org":"九江市人民政府","overlap_period":"不重叠（前后任）"},

    # ── Party secretary succession ──
    {"person_a":"jiujiang_chen_yun","person_b":"jiujiang_liu_wenhua",
     "type":"前后任","context":"陈云（2026.05接任书记）→ 刘文华（2022-2026书记）",
     "overlap_org":"中共九江市委员会","overlap_period":"不重叠（前后任）"},
    {"person_a":"jiujiang_liu_wenhua","person_b":"jiujiang_xie_laifa",
     "type":"前后任","context":"刘文华（2022.11接任书记）→ 谢来发（2021-2022书记，落马）",
     "overlap_org":"中共九江市委员会","overlap_period":"不重叠（前后任）"},
    {"person_a":"jiujiang_xie_laifa","person_b":"jiujiang_lin_binyang",
     "type":"前后任","context":"谢来发（2021.03接任书记）→ 林彬杨（2018-2021书记）",
     "overlap_org":"中共九江市委员会","overlap_period":"不重叠（前后任）"},

    # ── 四套班子关系 ──
    {"person_a":"jiujiang_chen_yun","person_b":"jiujiang_liao_qizhi",
     "type":"工作关系","context":"陈云（市委书记）与廖奇志（人大主任）为四套班子关系",
     "overlap_org":"九江市","overlap_period":"2026-05至今"},
    {"person_a":"jiujiang_deng_yongxiang","person_b":"jiujiang_liao_qizhi",
     "type":"工作关系","context":"邓永翔（市长）与廖奇志（人大主任）为四套班子关系",
     "overlap_org":"九江市","overlap_period":"2026-05至今"},
    {"person_a":"jiujiang_chen_yun","person_b":"jiujiang_zhan_yong",
     "type":"工作关系","context":"陈云（市委书记）与占勇（政协主席）为四套班子关系",
     "overlap_org":"九江市","overlap_period":"2026-05至今"},

    # ── 谢来发/杨文斌 落马 ──
    {"person_a":"jiujiang_xie_laifa","person_b":"jiujiang_yang_wenbin",
     "type":"同节点落马","context":"谢来发（2022.05落马）与杨文斌（2023.03落马）为九江前后任接连落马，引发江西官场震动",
     "overlap_org":"九江市","overlap_period":"2021-2023"},

    # ── Cross-city: 陈云 ↔ 上饶系统 ──
    {"person_a":"jiujiang_chen_yun","person_b":"jiujiang_liu_shuo",
     "type":"接替关系","context":"陈云先后任上饶市长、书记；刘烁从萍乡书记调任上饶书记交接陈云。属赣东北-赣北干部交流通道",
     "overlap_org":"上饶市→九江市","overlap_period":"2021-2026"},
    {"person_a":"jiujiang_chen_yun","person_b":"jiujiang_qiu_xiangjun",
     "type":"党政搭档（前任）","context":"邱向军（上饶市长）与陈云（上饶书记）曾搭班子（2021.12起）",
     "overlap_org":"上饶市","overlap_period":"2021-12至今（邱向军仍在任）"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT, org_id TEXT, title TEXT, start TEXT,
    end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT, person_b TEXT, type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_person ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_org ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons(id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations(id,name,type,level,parent,location) VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(?,?,?,?,?,?,?)",
              (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(?,?,?,?,?,?)",
              (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for tbl in ["persons","organizations","positions","relationships"]:
    counts[tbl] = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "书记" in post and "副" not in post and "副书记" not in post:
        return "230,50,50"  # red for top party secretary
    if "市长" in post and "副" not in post:
        return "50,100,230"  # blue for government leader
    if "副市长" in post:
        return "80,140,230"  # lighter blue for deputy mayor
    if "人大" in post:
        return "180,200,255"  # light blue for NPC
    if "政协" in post:
        return "200,180,255"  # purple for CPPCC
    if "原" in post:
        return "150,150,150"  # grey for predecessors
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255","政协":"230,200,255"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>九江市（地市级）领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    c_ = pcolor(p.get("current_post","")).split(",")
    sz = "20.0" if ("书记" in p.get("current_post","") and "副" not in p.get("current_post","") and "副书记" not in p.get("current_post","")) or ("市长" in p.get("current_post","") and "副" not in p.get("current_post","")) else "12.0"
    lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_[0]}" g="{c_[1]}" b="{c_[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c_ = ocolor(o.get("type","")).split(",")
    lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_[0]}" g="{c_[1]}" b="{c_[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
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
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
