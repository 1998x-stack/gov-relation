#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 九江市濂溪区 (Lianxi District) leadership network.

濂溪区 is a district of Jiujiang City, Jiangxi Province.
Covers: current party secretary (区委书记), mayor (区长), deputy mayors,
standing committee members, predecessors, and key relationships.
"""
import os, sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data/database/lianxi_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/lianxi_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# ID convention: lianxi_{surname_givenname}
persons = [
    # ── Current leadership ──
    {"id":"lianxi_zhang_ning","name":"张宁","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委书记","current_org":"中共濂溪区委员会",
     "source":"https://www.lianxi.gov.cn（区委书记，2026年7月上任）"},

    {"id":"lianxi_yu_hualin","name":"余华林","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委副书记、区长","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260714_7274407.html"},

    {"id":"lianxi_shao_yang","name":"邵阳","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委副书记","current_org":"中共濂溪区委员会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271142.html"},

    {"id":"lianxi_wang_jianrong","name":"王健蓉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委常委","current_org":"中共濂溪区委员会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271146.html"},

    {"id":"lianxi_zhu_lifeng","name":"朱立峰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委常委","current_org":"中共濂溪区委员会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271146.html"},

    {"id":"lianxi_hu_jian","name":"胡剑","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委常委","current_org":"中共濂溪区委员会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271146.html"},

    {"id":"lianxi_xiong_zhifang","name":"熊志芳","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委常委","current_org":"中共濂溪区委员会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271142.html"},

    {"id":"lianxi_li_lei","name":"李蕾","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委常委、副区长","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    {"id":"lianxi_li_zhangbo","name":"李章波","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区委常委","current_org":"中共濂溪区委员会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271146.html"},

    # ── Deputy Mayors (副区长) ──
    {"id":"lianxi_mei_guohuang","name":"梅国煌","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区副区长、公安分局局长","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    {"id":"lianxi_liao_yunjian","name":"廖云剑","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区副区长","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    {"id":"lianxi_feng_wen","name":"冯文","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区副区长","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    {"id":"lianxi_ye_ning","name":"叶宁","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区副区长","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    {"id":"lianxi_li_jingyu","name":"李竞宇","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"濂溪区副区长（挂职）","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    # ── Predecessors ──
    {"id":"lianxi_zhao_heping","name":"赵和平","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原濂溪区委书记，去向待查）","current_org":"",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202606/t20260609_7250448.html"},

    # ── Key cross-district figures ──
    {"id":"lianxi_ouyang_dongzhen","name":"欧阳东振","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区政协主席","current_org":"政协濂溪区委员会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271146.html"},

    {"id":"lianxi_hu_guoguang","name":"户国光","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区人大常委会副主任、区委办主任","current_org":"濂溪区人大常委会",
     "source":"https://www.lianxi.gov.cn/zwzx/lxsx/202607/t20260708_7271142.html"},

    # ── Government functionaries (党组) ──
    {"id":"lianxi_wang_chuanhong","name":"汪传鸿","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区政府党组成员","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    {"id":"lianxi_jiang_fengwen","name":"蒋丰文","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区政府党组成员","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},

    {"id":"lianxi_ding_xiaolin","name":"丁小林","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"濂溪区政府党组成员","current_org":"濂溪区人民政府",
     "source":"https://www.lianxi.gov.cn/fdzdxxgk/01/00/01/202604/t20260410_7219421.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":"org_lx_party","name":"中共濂溪区委员会","type":"党委","level":"县级",
     "parent":"中共九江市委员会","location":"江西省九江市濂溪区"},
    {"id":"org_lx_gov","name":"濂溪区人民政府","type":"政府","level":"县级",
     "parent":"九江市人民政府","location":"江西省九江市濂溪区"},
    {"id":"org_lx_npc","name":"濂溪区人大常委会","type":"人大","level":"县级",
     "parent":"九江市人大常委会","location":"江西省九江市濂溪区"},
    {"id":"org_lx_cppcc","name":"政协濂溪区委员会","type":"政协","level":"县级",
     "parent":"政协九江市委员会","location":"江西省九江市濂溪区"},
    {"id":"org_lx_discipline","name":"中共濂溪区纪律检查委员会","type":"党委","level":"县级",
     "parent":"中共九江市纪律检查委员会","location":"江西省九江市濂溪区"},
    {"id":"org_lx_public_security","name":"九江市公安局濂溪分局","type":"政府","level":"正科级",
     "parent":"九江市公安局","location":"江西省九江市濂溪区"},
    {"id":"org_lx_peoples_armed","name":"濂溪区人民武装部","type":"军队","level":"县级",
     "parent":"九江军分区","location":"江西省九江市濂溪区"},

    # Higher-level orgs
    {"id":"org_jj_party","name":"中共九江市委员会","type":"党委","level":"地市级",
     "parent":"中共江西省委员会","location":"江西省九江市"},
    {"id":"org_jj_gov","name":"九江市人民政府","type":"政府","level":"地市级",
     "parent":"江西省人民政府","location":"江西省九江市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 张宁 (Zhang Ning) — 区委书记 ──
    {"person_id":"lianxi_zhang_ning","org_id":"org_lx_party",
     "title":"区委书记","start":"~2026-07","end":"","rank":"正县级",
     "note":"接替赵和平任濂溪区委书记"},

    # ── 赵和平 (Zhao Heping) — 前区委书记 ──
    {"person_id":"lianxi_zhao_heping","org_id":"org_lx_party",
     "title":"区委书记","start":"~2024","end":"2026-06","rank":"正县级",
     "note":"前任区委书记，去向待查"},

    # ── 余华林 (Yu Hualin) — 区长 ──
    {"person_id":"lianxi_yu_hualin","org_id":"org_lx_gov",
     "title":"区委副书记、区长","start":"","end":"","rank":"正县级",
     "note":"区政府区长、党组书记，负责区政府全面工作"},

    # ── 邵阳 (Shao Yang) — 区委副书记 ──
    {"person_id":"lianxi_shao_yang","org_id":"org_lx_party",
     "title":"区委副书记","start":"","end":"","rank":"副县级",
     "note":"协助区委书记工作"},

    # ── Standing Committee ──
    {"person_id":"lianxi_wang_jianrong","org_id":"org_lx_party",
     "title":"区委常委","start":"","end":"","rank":"副县级","note":""},
    {"person_id":"lianxi_zhu_lifeng","org_id":"org_lx_party",
     "title":"区委常委","start":"","end":"","rank":"副县级","note":""},
    {"person_id":"lianxi_hu_jian","org_id":"org_lx_party",
     "title":"区委常委","start":"","end":"","rank":"副县级","note":""},
    {"person_id":"lianxi_xiong_zhifang","org_id":"org_lx_party",
     "title":"区委常委","start":"","end":"","rank":"副县级","note":""},
    {"person_id":"lianxi_li_zhangbo","org_id":"org_lx_party",
     "title":"区委常委","start":"","end":"","rank":"副县级","note":""},

    # ── 李蕾 (Li Lei) — 常委副区长 ──
    {"person_id":"lianxi_li_lei","org_id":"org_lx_gov",
     "title":"区委常委、副区长","start":"","end":"","rank":"副县级",
     "note":"分管发改、财税、金融、人社、规划建设、文旅、民政等"},

    # ── 梅国煌 (Mei Guohuang) — 副区长/公安 ──
    {"person_id":"lianxi_mei_guohuang","org_id":"org_lx_gov",
     "title":"副区长","start":"","end":"","rank":"副县级",
     "note":"分管公安、司法、信访、保密"},
    {"person_id":"lianxi_mei_guohuang","org_id":"org_lx_public_security",
     "title":"公安分局局长","start":"","end":"","rank":"正科/副县","note":"兼"},

    # ── 廖云剑 (Liao Yunjian) — 副区长 ──
    {"person_id":"lianxi_liao_yunjian","org_id":"org_lx_gov",
     "title":"副区长","start":"","end":"","rank":"副县级",
     "note":"分管农业农村、水利、乡村振兴、卫健、医保等"},

    # ── 冯文 (Feng Wen) — 副区长 ──
    {"person_id":"lianxi_feng_wen","org_id":"org_lx_gov",
     "title":"副区长","start":"","end":"","rank":"副县级",
     "note":"分管营商环境、应急管理、工业信息化、科技、商务、市场监管等"},

    # ── 叶宁 (Ye Ning) — 副区长 ──
    {"person_id":"lianxi_ye_ning","org_id":"org_lx_gov",
     "title":"副区长","start":"","end":"","rank":"副县级",
     "note":"分管行政审批、城管、生态环境、教育体育、交通运输等"},

    # ── 李竞宇 (Li Jingyu) — 挂职副区长 ──
    {"person_id":"lianxi_li_jingyu","org_id":"org_lx_gov",
     "title":"副区长（挂职）","start":"","end":"","rank":"副县级",
     "note":"挂职期间配合抓好招商等相关工作"},

    # ── 欧阳东振 — 政协主席 ──
    {"person_id":"lianxi_ouyang_dongzhen","org_id":"org_lx_cppcc",
     "title":"区政协主席","start":"","end":"","rank":"正县级","note":""},

    # ── 户国光 — 人大副主任/区委办主任 ──
    {"person_id":"lianxi_hu_guoguang","org_id":"org_lx_npc",
     "title":"区人大常委会副主任","start":"","end":"","rank":"副县级",
     "note":"兼区委办主任"},

    # ── Government functionaries ──
    {"person_id":"lianxi_wang_chuanhong","org_id":"org_lx_gov",
     "title":"区政府党组成员","start":"","end":"","rank":"正科",
     "note":"负责处理区政府日常工作"},
    {"person_id":"lianxi_jiang_fengwen","org_id":"org_lx_gov",
     "title":"区政府党组成员","start":"","end":"","rank":"正科",
     "note":"联系鄱阳湖生态科技城"},
    {"person_id":"lianxi_ding_xiaolin","org_id":"org_lx_gov",
     "title":"区政府党组成员","start":"","end":"","rank":"正科",
     "note":"联系鄱阳湖生态科技城"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政一把手 ──
    {"person_a":"lianxi_zhang_ning","person_b":"lianxi_yu_hualin",
     "type":"党政搭档","context":"张宁（区委书记）与余华林（区长）为濂溪区党政一把手",
     "overlap_org":"濂溪区","overlap_period":"~2026-07至今"},

    # ── 书记前后任 ──
    {"person_a":"lianxi_zhang_ning","person_b":"lianxi_zhao_heping",
     "type":"前后任","context":"张宁（~2026-07接任书记）→ 赵和平（前任书记）",
     "overlap_org":"中共濂溪区委员会","overlap_period":"不重叠（前后任）"},

    # ── 区长与前任书记搭档 ──
    {"person_a":"lianxi_yu_hualin","person_b":"lianxi_zhao_heping",
     "type":"党政搭档（前任）","context":"余华林（区长）与赵和平（前任书记）曾党政搭档",
     "overlap_org":"濂溪区","overlap_period":"~2024-2026-06"},

    # ── 区委班子内部 ──
    {"person_a":"lianxi_shao_yang","person_b":"lianxi_zhang_ning",
     "type":"工作关系","context":"邵阳（区委副书记）为张宁（书记）主要副手",
     "overlap_org":"濂溪区委","overlap_period":"~2026-07至今"},
    {"person_a":"lianxi_shao_yang","person_b":"lianxi_yu_hualin",
     "type":"工作关系","context":"邵阳与余华林为区委班子同事",
     "overlap_org":"濂溪区委","overlap_period":"至今"},

    # ── 常委与副区长重叠 ──
    {"person_a":"lianxi_li_lei","person_b":"lianxi_yu_hualin",
     "type":"工作关系","context":"李蕾（常委副区长）为余华林（区长）班子成员",
     "overlap_org":"濂溪区政府","overlap_period":"至今"},

    # ── 副区长之间 ──
    {"person_a":"lianxi_mei_guohuang","person_b":"lianxi_liao_yunjian",
     "type":"AB岗搭档","context":"梅国煌与廖云剑互为AB岗（2026年分工）",
     "overlap_org":"濂溪区政府","overlap_period":"2026-04至今"},
    {"person_a":"lianxi_li_lei","person_b":"lianxi_feng_wen",
     "type":"AB岗搭档","context":"李蕾与冯文互为AB岗（2026年分工）",
     "overlap_org":"濂溪区政府","overlap_period":"2026-04至今"},
    {"person_a":"lianxi_ye_ning","person_b":"lianxi_wang_chuanhong",
     "type":"AB岗搭档","context":"叶宁与汪传鸿互为AB岗（2026年分工）",
     "overlap_org":"濂溪区政府","overlap_period":"2026-04至今"},

    # ── 四套班子 ──
    {"person_a":"lianxi_zhang_ning","person_b":"lianxi_ouyang_dongzhen",
     "type":"工作关系","context":"张宁（区委书记）与欧阳东振（政协主席）为四套班子关系",
     "overlap_org":"濂溪区","overlap_period":"~2026-07至今"},
    {"person_a":"lianxi_yu_hualin","person_b":"lianxi_ouyang_dongzhen",
     "type":"工作关系","context":"余华林（区长）与欧阳东振（政协主席）为四套班子关系",
     "overlap_org":"濂溪区","overlap_period":"至今"},
    {"person_a":"lianxi_zhang_ning","person_b":"lianxi_hu_guoguang",
     "type":"工作关系","context":"张宁（区委书记）与户国光（人大副主任/区委办主任）直接上下级",
     "overlap_org":"濂溪区委","overlap_period":"~2026-07至今"},

    # ── 纪委与班子 ──
    {"person_a":"lianxi_hu_jian","person_b":"lianxi_zhang_ning",
     "type":"工作关系","context":"胡剑（区委常委/纪委）与张宁（书记）工作关系",
     "overlap_org":"濂溪区委","overlap_period":"~2026-07至今"},

    # ── 跨区联系 ──
    {"person_a":"lianxi_zhao_heping","person_b":"lianxi_yu_hualin",
     "type":"党政搭档（前任）","context":"赵和平与余华林曾为濂溪区党政搭档",
     "overlap_org":"濂溪区","overlap_period":"~2024-2026-06"},
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
        return "230,50,50"   # red for party secretary
    if "区长" in post and "副" not in post:
        return "50,100,230"  # blue for government leader
    if "副区长" in post or "副局长" in post:
        return "80,140,230"  # lighter blue for deputies
    if "副书记" in post:
        return "150,80,200"  # purple for deputy secretary
    if "政协" in post:
        return "200,180,255" # purple for CPPCC
    if "人大" in post:
        return "180,200,255" # light blue for NPC
    if "原" in post or "前" in post:
        return "150,150,150" # grey for predecessors
    if "常委" in post:
        return "200,100,100" # pink-red for standing committee
    if "党组" in post:
        return "120,120,120" # grey for party group
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255",
            "政协":"230,200,255","军队":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>九江市濂溪区领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    # Size: 20 for top leaders, 14 for deputies, 12 for others
    post = p.get("current_post","")
    if ("书记" in post and "副" not in post and "副书记" not in post) or \
       ("区长" in post and "副" not in post):
        sz = "20.0"
    elif "副" in post or "副书记" in post:
        sz = "14.0"
    else:
        sz = "12.0"
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
    lines.append(f'        <viz:size value="8.0"/>')
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
