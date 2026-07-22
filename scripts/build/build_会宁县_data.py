#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 会宁县 (Huining County, Gansu Province).

Task: gansu_会宁县 — 县委书记 & 县长
Province: 甘肃省
Parent city: 白银市
Region: 会宁县
Level: 县
Research date: 2026-07-17
Model intent: iagent

Confirmed officeholders (as of 2026-07-17, from www.huining.gov.cn + www.baiyin.gov.cn):
- 县委书记: 许伟民 (also 白银市副市长)
- 县长: 李桐 (县委副书记、县长)

县政府领导班子 (from www.huining.gov.cn 领导之窗):
- 狄国嘉 (县委常委、常务副县长)
- 杨国明 (县委常委、副县长，挂职)
- 王永泰 (县委常委、副县长)
- 项歌德 (县委常委、副县长)
- 强明生 (副县长、公安局局长)
- 何晓峰 (副县长)
- 裴世琪 (副县长)
- 徐世争 (副县长，挂职)
- 叶慧昕 (副县长，女，民进会员)

Sources:
- www.huining.gov.cn (会宁县人民政府官网 领导之窗, accessed 2026-07-17)
- www.baiyin.gov.cn (白银市人民政府官网 领导之窗, accessed 2026-07-17)
- 会宁县融媒体中心 news articles on www.huining.gov.cn
- www.baiyin.gov.cn build_白银市_data.py (existing research artifact)
"""

import sqlite3
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    GOV_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "gansu_会宁县")
DB_PATH = os.path.join(STAGING, "会宁县_network.db")
GEXF_PATH = os.path.join(STAGING, "会宁县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

# ══════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # Core Leader: 县委书记
    {
        "id": "huining_xu_weimin",
        "name": "许伟民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生（工程硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市副市长、会宁县委书记",
        "current_org": "中共会宁县委员会",
        "source": "www.baiyin.gov.cn (领导之窗); www.huining.gov.cn (新闻2026-07-07)",
        "notes": "1984年6月出生，研究生学历，工程硕士，中共党员。现任白银市政府副市长、党组成员，会宁县委书记。负责会宁县委全面工作。兼任白银市副市长（副厅级）。属于市领导兼县一把手跨级任职模式。",
        "confidence": "confirmed",
    },
    # Core Leader: 县长
    {
        "id": "huining_li_tong",
        "name": "李桐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "会宁县委副书记、县长",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗县长简介)",
        "notes": "1976年6月出生，省委党校研究生学历，中共党员。现任会宁县委副书记，县政府县长、党组书记。主持县政府全面工作。",
        "confidence": "confirmed",
    },
    # 常务副县长
    {
        "id": "huining_di_guojia",
        "name": "狄国嘉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年1月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（理学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗狄国嘉简介)",
        "notes": "1983年1月出生，大学学历，理学学士，中共党员。现任会宁县委常委，常务副县长、党组成员。",
        "confidence": "confirmed",
    },
    # 常委副县长（挂职）
    {
        "id": "huining_yang_guoming",
        "name": "杨国明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗杨国明简介)",
        "notes": "1976年6月出生，研究生学历，中共党员。现任会宁县委常委，县政府副县长、党组成员（挂职）。",
        "confidence": "confirmed",
    },
    # 常委副县长
    {
        "id": "huining_wang_yongtai",
        "name": "王永泰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（农学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗王永泰简介)",
        "notes": "1981年4月出生，大学学历，农学学士，中共党员。现任会宁县委常委，县政府副县长、党组成员。",
        "confidence": "confirmed",
    },
    # 常委副县长
    {
        "id": "huining_xiang_gede",
        "name": "项歌德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",
        "native_place": "",
        "education": "工学经济学双硕西方经济学博士应用经济学博士后",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗项歌德简介)",
        "notes": "1979年1月出生，工学经济学双硕士，西方经济学博士，应用经济学博士后，高级经济师，中共党员。现任会宁县委常委，县政府副县长、党组成员。学历背景突出，有高级经济师职称。",
        "confidence": "confirmed",
    },
    # 副县长/公安局局长
    {
        "id": "huining_qiang_mingsheng",
        "name": "强明生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "会宁县公安局",
        "source": "www.huining.gov.cn (领导之窗强明生简介)",
        "notes": "1975年10月出生，大学学历，中共党员。现任会宁县政府副县长、县公安局党委书记。",
        "confidence": "confirmed",
    },
    # 副县长
    {
        "id": "huining_he_xiaofeng",
        "name": "何晓峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（法学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗何晓峰简介)",
        "notes": "1986年10月出生，大学学历，法学学士，中共党员。现任会宁县政府副县长、党组成员。",
        "confidence": "confirmed",
    },
    # 副县长
    {
        "id": "huining_pei_shiqi",
        "name": "裴世琪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗裴世琪简介)",
        "notes": "1982年7月出生，研究生学历，中共党员。现任会宁县政府副县长、党组成员。",
        "confidence": "confirmed",
    },
    # 副县长（挂职）
    {
        "id": "huining_xu_shizheng",
        "name": "徐世争",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年8月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（文学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗徐世争简介)",
        "notes": "1983年8月出生，大学学历，文学学士，中共党员。现任会宁县政府副县长、党组成员（挂职）。",
        "confidence": "confirmed",
    },
    # 副县长（非党）
    {
        "id": "huining_ye_huixin",
        "name": "叶慧昕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年12月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（管理学学士）",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "会宁县人民政府",
        "source": "www.huining.gov.cn (领导之窗叶慧昕简介)",
        "notes": "1985年12月出生，大学学历，管理学学士，民进会员。现任会宁县副县长。非中共党员（民进会员）。",
        "confidence": "confirmed",
    },
]

organizations = [
    {"id": "cpc_huining", "name": "中共会宁县委员会", "type": "党委", "level": "县", "parent": "中共白银市委员会", "location": "甘肃省白银市会宁县"},
    {"id": "gov_huining", "name": "会宁县人民政府", "type": "政府", "level": "县", "parent": "白银市人民政府", "location": "甘肃省白银市会宁县"},
    {"id": "psb_huining", "name": "会宁县公安局", "type": "政府", "level": "县", "parent": "会宁县人民政府", "location": "甘肃省白银市会宁县"},
    {"id": "gov_baiyin", "name": "白银市人民政府", "type": "政府", "level": "地级市", "parent": "甘肃省人民政府", "location": "甘肃省白银市"},
]

positions = [
    # 许伟民
    {"person_id": "huining_xu_weimin", "org_id": "cpc_huining", "title": "会宁县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作"},
    {"person_id": "huining_xu_weimin", "org_id": "gov_baiyin", "title": "白银市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员兼任会宁县委书记"},
    # 李桐
    {"person_id": "huining_li_tong", "org_id": "gov_huining", "title": "会宁县县长", "start": "", "end": "present", "rank": "正处级", "note": "县委副书记县政府党组书记"},
    {"person_id": "huining_li_tong", "org_id": "cpc_huining", "title": "会宁县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 狄国嘉
    {"person_id": "huining_di_guojia", "org_id": "gov_huining", "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委县政府党组成员"},
    {"person_id": "huining_di_guojia", "org_id": "cpc_huining", "title": "会宁县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 杨国明
    {"person_id": "huining_yang_guoming", "org_id": "gov_huining", "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "县委常委县政府党组成员挂职"},
    {"person_id": "huining_yang_guoming", "org_id": "cpc_huining", "title": "会宁县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王永泰
    {"person_id": "huining_wang_yongtai", "org_id": "gov_huining", "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委县政府党组成员"},
    {"person_id": "huining_wang_yongtai", "org_id": "cpc_huining", "title": "会宁县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 项歌德
    {"person_id": "huining_xiang_gede", "org_id": "gov_huining", "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委县政府党组成员"},
    {"person_id": "huining_xiang_gede", "org_id": "cpc_huining", "title": "会宁县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 强明生
    {"person_id": "huining_qiang_mingsheng", "org_id": "gov_huining", "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县公安局党委书记"},
    {"person_id": "huining_qiang_mingsheng", "org_id": "psb_huining", "title": "公安局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 何晓峰
    {"person_id": "huining_he_xiaofeng", "org_id": "gov_huining", "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 裴世琪
    {"person_id": "huining_pei_shiqi", "org_id": "gov_huining", "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 徐世争
    {"person_id": "huining_xu_shizheng", "org_id": "gov_huining", "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员挂职"},
    # 叶慧昕
    {"person_id": "huining_ye_huixin", "org_id": "gov_huining", "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

relationships = [
    # 许伟民 <-> 李桐 (党政一把手搭档)
    ("huining_xu_weimin", "huining_li_tong", "党政搭档", "confirmed", "中共会宁县委员会/会宁县人民政府", "present", "许伟民（县委书记）与李桐（县长）为会宁县党政一把手搭档关系共同负责县委和县政府工作来源www.huining.gov.cn"),
    # 许伟民 <-> 县委常委
    ("huining_xu_weimin", "huining_di_guojia", "上下级", "confirmed", "中共会宁县委员会", "present", ""),
    ("huining_xu_weimin", "huining_yang_guoming", "上下级", "confirmed", "中共会宁县委员会", "present", ""),
    ("huining_xu_weimin", "huining_wang_yongtai", "上下级", "confirmed", "中共会宁县委员会", "present", ""),
    ("huining_xu_weimin", "huining_xiang_gede", "上下级", "confirmed", "中共会宁县委员会", "present", ""),
    # 李桐 <-> 县政府班子成员
    ("huining_li_tong", "huining_di_guojia", "上下级", "confirmed", "会宁县人民政府", "present", "县长与常务副县长"),
    ("huining_li_tong", "huining_yang_guoming", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_li_tong", "huining_wang_yongtai", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_li_tong", "huining_xiang_gede", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_li_tong", "huining_qiang_mingsheng", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_li_tong", "huining_he_xiaofeng", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_li_tong", "huining_pei_shiqi", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_li_tong", "huining_xu_shizheng", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_li_tong", "huining_ye_huixin", "同事", "confirmed", "会宁县人民政府", "present", ""),
    # 狄国嘉 <-> 其他副县长
    ("huining_di_guojia", "huining_yang_guoming", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_di_guojia", "huining_wang_yongtai", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_di_guojia", "huining_xiang_gede", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_di_guojia", "huining_qiang_mingsheng", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_di_guojia", "huining_he_xiaofeng", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_di_guojia", "huining_pei_shiqi", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_di_guojia", "huining_xu_shizheng", "同事", "confirmed", "会宁县人民政府", "present", ""),
    ("huining_di_guojia", "huining_ye_huixin", "同事", "confirmed", "会宁县人民政府", "present", ""),
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ══════════════════════════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA journal_mode=WAL")

cur.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        ethnicity TEXT,
        birth TEXT,
        birthplace TEXT,
        education TEXT,
        party_join TEXT,
        work_start TEXT,
        current_post TEXT,
        current_org TEXT,
        source TEXT,
        confidence TEXT
    );
    CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        strength TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source,confidence) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"],p["name"],p["gender"],p["ethnicity"],p.get("birth",""),p.get("birthplace",""),p.get("education",""),p.get("party_join",""),p.get("work_start",""),p.get("current_post",""),p.get("current_org",""),p.get("source",""),p.get("confidence","")))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

for pos in positions:
    cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))

for r in relationships:
    if r[0]==r[1]: continue
    cur.execute("INSERT INTO relationships (person_a,person_b,type,strength,overlap_org,overlap_period,context) VALUES (?,?,?,?,?,?,?)",
                (r[0],r[1],r[2],r[3],r[4],r[5],r[6]))

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
pc=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
jpc=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc=cur.fetchone()[0]
conn.close()
print(f"DB: {DB_PATH}")
print(f"Persons:{pc} Orgs:{oc} Positions:{jpc} Relationships:{rc}")

# ══════════════════════════════════════════════════════════════════════════
# GEXF GRAPH
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(pid):
    m={"huining_xu_weimin":"255,50,50","huining_li_tong":"50,100,255","huining_di_guojia":"50,100,255","huining_yang_guoming":"50,100,255","huining_wang_yongtai":"50,100,255","huining_xiang_gede":"50,100,255","huining_qiang_mingsheng":"50,100,255","huining_he_xiaofeng":"50,100,255","huining_pei_shiqi":"50,100,255","huining_xu_shizheng":"50,100,255","huining_ye_huixin":"50,100,255"}
    return m.get(pid,"100,100,100")

def psize(pid):
    big={"huining_xu_weimin","huining_li_tong"}
    return "20.0" if pid in big else "12.0"

def ocolor(t):
    c={"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","事业单位":"220,220,220"}
    return c.get(t,"200,200,200")

lines=[]
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'<meta lastmodifieddate="{TODAY}"><creator>Sisyphus</creator><description>会宁县领导班子工作关系网络白银市会宁县</description></meta>')
lines.append('<graph mode="static" defaultedgetype="undirected">')
lines.append('<attributes class="node"><attribute id="0" title="type" type="string"/><attribute id="1" title="role" type="string"/><attribute id="2" title="org" type="string"/></attributes>')
lines.append('<attributes class="edge"><attribute id="0" title="type" type="string"/><attribute id="1" title="confidence" type="string"/><attribute id="2" title="period" type="string"/></attributes>')
lines.append('<nodes>')
for p in persons:
    pid=p["id"];c=pcolor(pid);sz=psize(pid)
    lines.append(f'<node id="p{pid}" label="{esc(p["name"])}"><attvalues><attvalue for="0" value="person"/><attvalue for="1" value="{esc(p.get("current_post",""))}"/><attvalue for="2" value="{esc(p.get("current_org",""))}"/></attvalues><viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/><viz:size value="{sz}"/></node>')
for o in organizations:
    oc_=ocolor(o["type"])
    lines.append(f'<node id="o{o["id"]}" label="{esc(o["name"])}"><attvalues><attvalue for="0" value="organization"/><attvalue for="1" value="{esc(o["type"])}"/><attvalue for="2" value="{esc(o["parent"])}"/></attvalues><viz:color r="{oc_.split(",")[0]}" g="{oc_.split(",")[1]}" b="{oc_.split(",")[2]}"/><viz:size value="8.0"/></node>')
lines.append('</nodes><edges>')
eid=0
for pos in positions:
    eid+=1
    lines.append(f'<edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0"><attvalues><attvalue for="0" value="worked_at"/><attvalue for="1" value="{esc(pos.get("rank","") or "")}"/><attvalue for="2" value="{esc(pos.get("start","") or "")}-{esc(pos.get("end","") or "")}"/></attvalues></edge>')

for r in relationships:
    if r[0]==r[1]:continue
    eid+=1
    w="2.0" if r[3]=="confirmed" else "1.5" if r[3]=="plausible" else "1.0"
    lines.append(f'<edge id="e{eid}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[2])}" weight="{w}"><attvalues><attvalue for="0" value="relationship"/><attvalue for="1" value="{esc(r[3])}"/><attvalue for="2" value="{esc(r[5] or "")}"/></attvalues></edge>')

lines.append('</edges></graph></gexf>')

with open(GEXF_PATH,"w",encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF: {GEXF_PATH} Edges:{eid} Done.")
