#!/usr/bin/env python3
"""Build Huairen City (怀仁市) personnel network database + GEXF graph."""

import sqlite3
import os
import xml.etree.ElementTree as ET

DB_PATH = "data/database/怀仁市_network.db"
GEXF_PATH = "data/graph/怀仁市_network.gexf"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# ========== DATA ==========

persons = [
    {
        "id": "huairen_ding_yu",
        "name": "丁裕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": "在职研究生（山西农业大学函授农林经济管理专业，农业推广硕士）",
        "party_join": None,
        "work_start": None,
        "current_post": "市委书记（原任）",
        "current_org": "中共怀仁市委员会",
        "source": "http://baike.sogou.com/v202108424.htm"
    },
    {
        "id": "huairen_wang_guowen",
        "name": "王国文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "朔州市",
        "education": "中央党校法律专业",
        "party_join": "中共党员",
        "work_start": "1999年9月",
        "current_post": "市委副书记、市长",
        "current_org": "怀仁市人民政府",
        "source": "http://www.zghr.gov.cn/xxgk/ldzc/xz/202205/t20220520_393703.html"
    },
    {
        "id": "huairen_liu_hongwu",
        "name": "刘宏武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年12月",
        "birthplace": None,
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "原任市委副书记（2022年拟任市直单位正职）",
        "current_org": "怀仁市委员会（已调离）",
        "source": "http://www.szswzzb.gov.cn/"
    },
    {
        "id": "huairen_xuan_yong",
        "name": "宣勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "怀仁市纪律检查委员会",
        "source": "http://www.szsjwjcj.gov.cn/"
    },
    {
        "id": "huairen_tian_yong",
        "name": "田勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "市委常委、常务副市长",
        "current_org": "怀仁市人民政府",
        "source": "http://www.zghr.gov.cn/xxgk/ldzc/fxz_16585/"
    },
    {
        "id": "huairen_liu_ruidong",
        "name": "刘瑞栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "市委常委、组织部部长（推测）",
        "current_org": "中共怀仁市委组织部",
        "source": "https://mp.weixin.qq.com/s/nBZnyIBOkPzvmKsR4ojE1A"
    },
    {
        "id": "huairen_ren_rui",
        "name": "任瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "副市长",
        "current_org": "怀仁市人民政府",
        "source": "http://www.zghr.gov.cn/xxgk/ldzc/fxz/202604/t20260422_770242.html"
    },
    {
        "id": "huairen_liu_peng",
        "name": "刘鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "副市长",
        "current_org": "怀仁市人民政府",
        "source": "http://www.zghr.gov.cn/xxgk/ldzc/fxz/202011/t20201103_308378.html"
    },
    {
        "id": "huairen_yang_lianggui",
        "name": "杨良贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "副市长",
        "current_org": "怀仁市人民政府",
        "source": "http://www.zghr.gov.cn/xxgk/ldzc/fxz/202104/t20210425_333325.html"
    },
    {
        "id": "huairen_zhang_rihong",
        "name": "张日宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "副市长",
        "current_org": "怀仁市人民政府",
        "source": "http://www.zghr.gov.cn/xxgk/ldzc/fxz/201806/t20180628_194150.html"
    },
    {
        "id": "huairen_pan_yafei",
        "name": "潘亚非",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": None,
        "education": "大学",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "副市长（原怀仁市委办公室主任）",
        "current_org": "怀仁市人民政府",
        "source": "http://www.zghr.gov.cn/xxgk/ldzc/fxz/202604/t20260422_770243.html"
    },
    {
        "id": "huairen_yu_suwen",
        "name": "于素文",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "总监制（融媒体中心）",
        "current_org": "怀仁市融媒体中心",
        "source": "https://mp.weixin.qq.com/s/COHLmEXYp1f-Vzz6189bpA"
    },
]

organizations = [
    {"id": "huairen_city_committee", "name": "中共怀仁市委员会", "type": "party", "level": "county-level city", "parent": "朔州市委", "location": "朔州市怀仁市"},
    {"id": "huairen_gov", "name": "怀仁市人民政府", "type": "government", "level": "county-level city", "parent": "朔州市政府", "location": "朔州市怀仁市"},
    {"id": "huairen_discipline", "name": "怀仁市纪律检查委员会", "type": "discipline", "level": "county-level city", "parent": "朔州市纪委监委", "location": "朔州市怀仁市"},
    {"id": "huairen_org_dept", "name": "中共怀仁市委组织部", "type": "party_dept", "level": "county-level city", "parent": "怀仁市委", "location": "朔州市怀仁市"},
    {"id": "huairen_media", "name": "怀仁市融媒体中心", "type": "media", "level": "county-level city", "parent": "怀仁市委", "location": "朔州市怀仁市"},
    {"id": "shuozhou_gov", "name": "朔州市委市政府接待办", "type": "government", "level": "prefecture", "parent": None, "location": "朔州市"},
    {"id": "shuozhou_affairs", "name": "朔州市直属机关事务服务中心", "type": "government", "level": "prefecture", "parent": None, "location": "朔州市"},
    {"id": "shanyin_county", "name": "山阴县委员会", "type": "party", "level": "county", "parent": "朔州市委", "location": "朔州市山阴县"},
}

positions = [
    # Ding Yu
    {"person_id": "huairen_ding_yu", "org_id": "hua_ren_city_committee", "title": "市委书记", "start": "2021?", "end": "2026?", "rank": "county-level", "note": "原任，有搜狗百科条目"},
    
    # Wang Guowen
    {"person_id": "huairen_wang_guowen", "org_id": "shuozhou_gov", "title": "党组书记（接待办）", "start": None, "end": None, "rank": None, "note": ""},
    {"person_id": "huairen_wang_guowen", "org_id": "shuozhou_affairs", "title": "主任（机关事务服务中心）", "start": None, "end": None, "rank": None, "note": ""},
    {"person_id": "huairen_wang_guowen", "org_id": "shanyin_county", "title": "县委副书记", "start": None, "end": None, "rank": "county-level", "note": "此前任职"},
    {"person_id": "huairen_wang_guowen", "org_id": "huairen_city_committee", "title": "市委副书记、市长", "start": "2021-04?", "end": None, "rank": "county-level", "note": "现任"},
    {"person_id": "huairen_wang_guowen", "org_id": "huairen_gov", "title": "市长", "start": "2021-04?", "end": None, "rank": "county-level", "note": "现任"},
    
    # Liu Hongwu - former deputy secretary
    {"person_id": "huairen_liu_hongwu", "org_id": "huairen_city_committee", "title": "市委副书记", "start": None, "end": "2022-04", "rank": "county-level", "note": "公示拟任市直单位正职"},
    
    # Xuan Yong - discipline secretary
    {"person_id": "huairen_xuan_yong", "org_id": "huairen_discipline", "title": "市纪委书记、市监委主任", "start": None, "end": None, "rank": "county-level", "note": "市纪委监委网站登记领导"},
    
    # Tian Yong - executive vice mayor
    {"person_id": "huairen_tian_yong", "org_id": "huairen_gov", "title": "市委常委、常务副市长", "start": None, "end": None, "rank": "county-level", "note": "负责常务工作"},
    
    # Liu Ruidong - likely organization head
    {"person_id": "huairen_liu_ruidong", "org_id": "huairen_org_dept", "title": "市委常委、组织部部长（推测）", "start": None, "end": None, "rank": "county-level", "note": "巡视拟任职干部任前法律考试"},
    
    # Ren Rui
    {"person_id": "huairen_ren_rui", "org_id": "huairen_gov", "title": "副市长", "start": "2026-04?", "end": None, "rank": "deputy-county", "note": ""},
    
    # Liu Peng
    {"person_id": "huairen_liu_peng", "org_id": "huairen_gov", "title": "副市长", "start": None, "end": None, "rank": "deputy-county", "note": ""},
    
    # Yang Lianggui
    {"person_id": "huairen_yang_lianggui", "org_id": "huairen_gov", "title": "副市长", "start": None, "end": None, "rank": "deputy-county", "note": ""},
    
    # Zhang Rihong
    {"person_id": "huairen_zhang_rihong", "org_id": "huairen_gov", "title": "副市长", "start": None, "end": None, "rank": "deputy-county", "note": ""},
    
    # Pan Yafei
    {"person_id": "huairen_pan_yafei", "org_id": "huairen_city_committee", "title": "市委办公室主任", "start": None, "end": "2024-02", "rank": None, "note": "2024年2月公示拟提名为副县（市、区）长人选"},
    {"person_id": "huairen_pan_yafei", "org_id": "huairen_gov", "title": "副市长", "start": "2026-04?", "end": None, "rank": "deputy-county", "note": ""},
    
    # Yu Suwen
    {"person_id": "huairen_yu_suwen", "org_id": "huairen_media", "title": "总监制", "start": None, "end": None, "rank": None, "note": "融媒体中心总监制"},
]

relationships = [
    ("huairen_ding_yu", "huairen_wang_guowen", "colleague", "搭班合作：市委书记与市长", "怀仁市委", "2021-2026"),
    ("huairen_wang_guowen", "huairen_tian_yong", "colleague", "市长与常务副市长搭班", "怀仁市政府", None),
    ("huairen_wang_guowen", "huairen_ren_rui", "colleague", "市长与副市长", "怀仁市政府", None),
    ("huairen_xuan_yong", "huairen_wang_guowen", "colleague", "纪委监督与被监督关系", "怀仁市委常委会", None),
    ("huairen_liu_ruidong", "huairen_wang_guowen", "colleague", "组织与政府领导工作关系", "怀仁市委常委会", None),
]

# ========== BUILD DATABASE ==========

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create tables
cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

GEXF文档关于不是项目（node）撰写题案！ creating directories if not exists.

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"], p["party_join"],
                 p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["name"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("INSERT OR REPLACE INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for ra in relationships:
    cur.execute("INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (ra[0], ra[1], ra[2], ra[3], ra[4], ra[5]))

conn.commit()

print(f"[DB] Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
print(f"[DB] Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
print(f"[DB] Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
print(f"[DB] Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

# ========== BUILD GEXF ==========

GEXF_XML = '<?xml version="1.0" encoding="UTF-8"?>\n'
GEXF_XML += '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">\n'
GEXF_XML += '  <meta>\n'
GEXF_XML += '    <creator>gov-relation research agent</creator>\n'
GEXF_XML += '    <description>怀仁市领导班子工作关系网络 - 2026年7月</description>\n'
GEXF_XML += '  </meta>\n'
GEXF_XML += '  <graph mode="static" defaultedgetype="undirected">\n'

# Nodes (persons + orgs)
GEXF_XML += '    <nodes>\n'
# Persons first
for p in persons:
    role_color = {
        "市委书记": "#E03C31" if "书记" in (p["current_post"] or "") else "",
        "市长": "#3178E0" if "市长" in (p["current_post"] or "") else "",
        "纪委书记": "#FF8C00" if "纪委" in (p["current_post"] or "") else "",
    }
    color = "#E03C31" if "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") else \
            "#3178E0" if "市长" in (p["current_post"] or "") else \
            "#FF8C00" if "纪委" in (p["current_post"] or "") else \
            "#808080"
    size = 15.0 if "书记" in (p["current_post"] or "") or "市长" in (p["current_post"] or "") else 10.0
    GEXF_XML += f'      <node id="{p["id"]}" label="{p["name"]}">\n'
    GEXF_XML += f'        <attvalues>\n'
    GEXF_XML += f'          <attvalue for="type" value="person"/>\n'
    GEXF_XML += f'          <attvalue for="role" value="{p["current_post"] or "未知"}"/>\n'
    GEXF_XML += f'        </attvalues>\n'
    GEXF_XML += f'        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>\n'
    GEXF_XML += f'        <viz:size value="{size}"/>\n'
    GEXF_XML += f'      </node>\n'
# Then orgs
for o in organizations:
    org_color = "#4a4a4a"
    GEXF_XML += f'      <node id="{o["name"]}" label="{o["name"]}">\n'
    GEXF_XML += f'        <attvalues>\n'
    GEXF_XML += f'          <attvalue type="type" value="organization"/>\n'
    GEXF_XML += f'          <attvalue for="org_type" value="{o["type"]}"/>\n'
    GEXF_XML += f'        </attvalues>\n'
    GEXF_XML += f'        <viz:color r="74" g="74" b="74"/>\n'
    GEXF_XML += f'        <viz:size value="8.0"/>\n'
    GEXF_XML += f'      </node>\n'
GEXF_XML += '    </nodes>\n'

# Edges
GEXF_XML += '    <edges>\n'
edge_id = 0
for pos in positions:
    edge_id += 1
    p = next((x for x in persons if x["id"] == pos["person_id"]), None)
    o = next((x for x in organizations if x["name"] == pos["org_id"]), None)
    if p and o:
        GEXF_XML += f'      <edge id="e{edge_id}" source="{p["id"]}" target="{o["name"]}" type="directed" label="worked_at">\n'
        GEXF_XML += f'        <attvalues>\n'
        GEXF_XML += f'          <attvalue for="relation_type" value="worked_at"/>\n'
        GEXF_XML += f'          <attvalue for="title" value="{pos["title"]}"/>\n'
        if pos["start"]:
            GEXF_XML += f'          <attvalue for="start" value="{pos["start"]}"/>\n'
        if pos["end"]:
            GEXF_XML += f'          <attvalue for="end" value="{pos["end"]}"/>\n'
        GEXF_XML += f'        </attvalues>\n'
        GEXF_XML += f'      </edge>\n'
for ra in relationships:
    edge_id += 1
    GEXF_XML += f'      <edge id="e{edge_id}" source="{ra[0]}" target="{ra[1]}" type="undirected" label="{ra[2]}">\n'
    GEXF_XML += f'        <attvalues>\n'
    GEXF_XML += f'          <attvalue for="relation_type" value="{ra[2]}"/>\n'
    GEXF_XML += f'          <attvalue for="context" value="{ra[3]}"/>\n'
    if ra[5]:
        GEXF_XML += f'          <attvalue for="overlap_period" value="{ra[5]}"/>\n'
    GEXF_XML += f'        </attvalues>\n'
    GEXF_XML += f'      </edge>\n'
GEXF_XML += '    </edges>\n'
GEXF_XML += '  </graph>\n'
GEXF_XML += '</gexf>\n'

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(GEXF_XML)

print(f"[GEXF] Written to: {GEXF_PATH}")

import stat
os.chmod("./build_怀仁市_data.py", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
print("[Done] build_怀仁市_data.py was executed. Check output files.")
