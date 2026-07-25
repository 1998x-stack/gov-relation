#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 湘西土家族苗族自治州.

Task ID: hunan_湘西土家族苗族自治州
Level: 地级市
Province: 湖南省
Targets: 市委书记 & 市长

Data sourced from:
- 中国经济网: http://district.ce.cn/newarea/sddy/202606/t20260622_3044364.shtml
- 湘西网: http://www.xxnet.com.cn/news/
- 腾讯新闻: https://news.qq.com/rain/a/20250219A004RG00
- 百度百科 (刘涛/虢正贵/陈华/尚生龙)
- jendow百科 (尚生龙完整履历): https://www.jendow.com.tw/wiki/%E5%B0%9A%E7%94%9F%E9%BE%8D
- 新湖南: https://m.voc.com.cn/xhn/news/202502/27771467.html
- 湖南省政府: http://www.hunan.gov.cn/topic/2026ybg/202602/t20260209_33913164.html
- Wikipedia (湘西州): https://zh.wikipedia.org/wiki/湘西土家族苗族自治州
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for pc in [2, 3, 4, 5]:
    c = Path(__file__).resolve().parents[pc]
    if (c / "gov_relation").is_dir():
        REPO_ROOT = c
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "湘西土家族苗族自治州"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────
_CURRENT = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_湘西土家族苗族自治州"
STAGING = _CURRENT if _CURRENT.name == "hunan_湘西土家族苗族自治州" else _STAGING_CANDIDATE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ══════════════════════════════════════════════════════════════════════
# RAW DATA
# ══════════════════════════════════════════════════════════════════════

S = lambda s: f"xx_{s}"

persons = [
    {"id": S("liu_tao"), "name": "刘涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-06", "birthplace": "河南省方城县",
     "education": "研究生（河南大学中国现代文学硕士）",
     "party_join": "1996-11", "work_start": "1997-07",
     "current_post": "湘西州委书记", "current_org": "中共湘西土家族苗族自治州委员会",
     "source": "https://baike.baidu.com/item/%E5%88%98%E6%B6%9B"},

    {"id": S("shang_shenglong"), "name": "尚生龙", "gender": "男", "ethnicity": "土家族",
     "birth": "1975-02", "birthplace": "湖南省桑植县",
     "education": "省委党校在职研究生（法学理论）",
     "party_join": "1996-01", "work_start": "1997-07",
     "current_post": "湘西州代理州长", "current_org": "湘西土家族苗族自治州人民政府",
     "source": "https://baike.baidu.com/item/%E5%B0%9A%E7%94%9F%E9%BE%99/9023713"},

    {"id": S("guo_zhenggui"), "name": "虢正贵", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-09", "birthplace": "湖南省长沙市望城区",
     "education": "大专（长沙基础大学物理专业）",
     "party_join": "1984-06", "work_start": "1984-07",
     "current_post": "湖南省政协副主席", "current_org": "湖南省政协",
     "source": "https://baike.baidu.com/item/%E8%99%A2%E6%AD%A3%E8%B4%B5"},

    {"id": S("chen_hua"), "name": "陈华", "gender": "女", "ethnicity": "土家族",
     "birth": "1967-12", "birthplace": "湖南省石门县",
     "education": "中央党校研究生（经济管理）",
     "party_join": "1990-06", "work_start": "1990-07",
     "current_post": "前任湘西州州长（另有任用）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E9%99%88%E5%8D%8E/20117663"},

    {"id": S("gong_minghan"), "name": "龚明汉", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-09", "birthplace": "湖南省张家界市永定区",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州人大常委会主任", "current_org": "湘西土家族苗族自治州人大常委会",
     "source": "https://zh.wikipedia.org/wiki/湘西土家族苗族自治州"},

    {"id": S("xiang_bangwei"), "name": "向邦伟", "gender": "男", "ethnicity": "土家族",
     "birth": "1969-03", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州政协主席", "current_org": "政协湘西土家族苗族自治州委员会",
     "source": "https://zh.wikipedia.org/wiki/湘西土家族苗族自治州"},

    {"id": S("zhou_lizhi"), "name": "周立志", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-05", "birthplace": "湖南省永州市",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "吉首市委书记", "current_org": "中共吉首市委员会",
     "source": "https://zh.wikipedia.org/wiki/吉首市"},

    {"id": S("fu_jiasheng"), "name": "符家盛", "gender": "男", "ethnicity": "苗族",
     "birth": "1973-04", "birthplace": "湖南省龙山县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "吉首市市长", "current_org": "吉首市人民政府",
     "source": "https://zh.wikipedia.org/wiki/吉首市"},

    {"id": S("fu_jiabo"), "name": "符家波", "gender": "男", "ethnicity": "苗族",
     "birth": "1979-05", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "泸溪县委书记", "current_org": "中共泸溪县委员会",
     "source": "https://zh.wikipedia.org/wiki/泸溪县"},

    {"id": S("he_li"), "name": "贺立", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-12", "birthplace": "湖南省长沙县",
     "education": "研究生", "party_join": "", "work_start": "",
     "current_post": "泸溪县县长", "current_org": "泸溪县人民政府",
     "source": "https://zh.wikipedia.org/wiki/泸溪县"},

    {"id": S("mao_jia"), "name": "毛家", "gender": "男", "ethnicity": "土家族",
     "birth": "1973-10", "birthplace": "湖南省永顺县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "凤凰县委书记", "current_org": "中共凤凰县委员会",
     "source": "https://zh.wikipedia.org/wiki/凤凰县"},

    {"id": S("fan_zhongqing"), "name": "樊忠清", "gender": "男", "ethnicity": "苗族",
     "birth": "1975-10", "birthplace": "湖南省花垣县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "凤凰县县长", "current_org": "凤凰县人民政府",
     "source": "https://zh.wikipedia.org/wiki/凤凰县"},

    {"id": S("wang_jinghai"), "name": "王京海", "gender": "男", "ethnicity": "土家族",
     "birth": "1975-09", "birthplace": "湖南省慈利县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "花垣县委书记兼县长", "current_org": "中共花垣县委员会",
     "source": "https://zh.wikipedia.org/wiki/花垣县"},

    {"id": S("zhou_jianwu"), "name": "周建武", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-11", "birthplace": "湖南省涟源市",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "保靖县委书记", "current_org": "中共保靖县委员会",
     "source": "https://zh.wikipedia.org/wiki/保靖县"},

    {"id": S("guo_yingxiang"), "name": "郭应湘", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-06", "birthplace": "湖南省桂东县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "保靖县县长", "current_org": "保靖县人民政府",
     "source": "https://zh.wikipedia.org/wiki/保靖县"},

    {"id": S("teng_zhaohui"), "name": "滕朝辉", "gender": "男", "ethnicity": "土家族",
     "birth": "1974-10", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古丈县委书记", "current_org": "中共古丈县委员会",
     "source": "https://zh.wikipedia.org/wiki/古丈县"},

    {"id": S("chen_jianxin"), "name": "陈建新", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-06", "birthplace": "湖南省衡东县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古丈县县长", "current_org": "古丈县人民政府",
     "source": "https://zh.wikipedia.org/wiki/古丈县"},

    {"id": S("xiang_jiamao"), "name": "向加茂", "gender": "男", "ethnicity": "苗族",
     "birth": "1973-02", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "永顺县委书记兼县长", "current_org": "中共永顺县委员会",
     "source": "https://zh.wikipedia.org/wiki/永顺县"},

    {"id": S("shi_rongfen"), "name": "时荣芬", "gender": "女", "ethnicity": "苗族",
     "birth": "1976-12", "birthplace": "湖南省花垣县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "龙山县县委书记", "current_org": "中共龙山县委员会",
     "source": "https://zh.wikipedia.org/wiki/龙山县"},

    {"id": S("zhou_shengyi"), "name": "周胜益", "gender": "男", "ethnicity": "苗族",
     "birth": "1972-09", "birthplace": "湖南省保靖县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "龙山县县长", "current_org": "龙山县人民政府",
     "source": "https://zh.wikipedia.org/wiki/龙山县"},
]

organizations = [
    {"id": S("zhouwei"), "name": "中共湘西土家族苗族自治州委员会", "type": "party_committee", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},
    {"id": S("zhouzhengfu"), "name": "湘西土家族苗族自治州人民政府", "type": "government", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},
    {"id": S("rd"), "name": "湘西土家族苗族自治州人大常委会", "type": "npc", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},
    {"id": S("zx"), "name": "政协湘西土家族苗族自治州委员会", "type": "cppcc", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},
    {"id": S("jishou_sw"), "name": "中共吉首市委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "吉首市"},
    {"id": S("jishou_zf"), "name": "吉首市人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "吉首市"},
    {"id": S("luxi_xw"), "name": "中共泸溪县委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "泸溪县"},
    {"id": S("luxi_zf"), "name": "泸溪县人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "泸溪县"},
    {"id": S("fh_xw"), "name": "中共凤凰县委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "凤凰县"},
    {"id": S("fh_zf"), "name": "凤凰县人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "凤凰县"},
    {"id": S("hy_xw"), "name": "中共花垣县委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "花垣县"},
    {"id": S("hy_zf"), "name": "花垣县人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "花垣县"},
    {"id": S("bj_xw"), "name": "中共保靖县委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "保靖县"},
    {"id": S("bj_zf"), "name": "保靖县人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "保靖县"},
    {"id": S("gz_xw"), "name": "中共古丈县委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "古丈县"},
    {"id": S("gz_zf"), "name": "古丈县人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "古丈县"},
    {"id": S("ys_xw"), "name": "中共永顺县委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "永顺县"},
    {"id": S("ys_zf"), "name": "永顺县人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "永顺县"},
    {"id": S("ls_xw"), "name": "中共龙山县委员会", "type": "county_party", "level": "county", "parent": S("zhouwei"), "location": "龙山县"},
    {"id": S("ls_zf"), "name": "龙山县人民政府", "type": "county_gov", "level": "county", "parent": S("zhouzhengfu"), "location": "龙山县"},
]

positions = [
    {"pid": S("liu_tao"), "oid": S("zhouwei"), "title": "州委书记", "start": "2024-10", "end": "", "rank": "正厅级"},
    {"pid": S("shang_shenglong"), "oid": S("zhouzhengfu"), "title": "代理州长", "start": "2026-06", "end": "", "rank": "正厅级"},
    {"pid": S("guo_zhenggui"), "oid": S("zhouwei"), "title": "前任州委书记", "start": "2021-03", "end": "2024-10", "rank": "正厅级"},
    {"pid": S("chen_hua"), "oid": S("zhouzhengfu"), "title": "前任州长", "start": "2023-01", "end": "2026-06", "rank": "正厅级"},
    {"pid": S("gong_minghan"), "oid": S("rd"), "title": "州人大常委会主任", "start": "2021-01", "end": "", "rank": "正厅级"},
    {"pid": S("xiang_bangwei"), "oid": S("zx"), "title": "州政协主席", "start": "2026-02", "end": "", "rank": "正厅级"},
    {"pid": S("zhou_lizhi"), "oid": S("jishou_sw"), "title": "市委书记", "start": "2023-10", "end": "", "rank": "正处级"},
    {"pid": S("fu_jiasheng"), "oid": S("jishou_zf"), "title": "市长", "start": "2020-04", "end": "", "rank": "正处级"},
    {"pid": S("fu_jiabo"), "oid": S("luxi_xw"), "title": "县委书记", "start": "2025-11", "end": "", "rank": "正处级"},
    {"pid": S("he_li"), "oid": S("luxi_zf"), "title": "县长", "start": "2026-01", "end": "", "rank": "正处级"},
    {"pid": S("mao_jia"), "oid": S("fh_xw"), "title": "县委书记", "start": "2022-01", "end": "", "rank": "正处级"},
    {"pid": S("fan_zhongqing"), "oid": S("fh_zf"), "title": "县长", "start": "2022-03", "end": "", "rank": "正处级"},
    {"pid": S("wang_jinghai"), "oid": S("hy_xw"), "title": "县委书记", "start": "2025-02", "end": "", "rank": "正处级"},
    {"pid": S("wang_jinghai"), "oid": S("hy_zf"), "title": "县长", "start": "2022-03", "end": "", "rank": "正处级"},
    {"pid": S("zhou_jianwu"), "oid": S("bj_xw"), "title": "县委书记", "start": "2024-06", "end": "", "rank": "正处级"},
    {"pid": S("guo_yingxiang"), "oid": S("bj_zf"), "title": "县长", "start": "2024-07", "end": "", "rank": "正处级"},
    {"pid": S("teng_zhaohui"), "oid": S("gz_xw"), "title": "县委书记", "start": "2023-12", "end": "", "rank": "正处级"},
    {"pid": S("chen_jianxin"), "oid": S("gz_zf"), "title": "县长", "start": "2024-07", "end": "", "rank": "正处级"},
    {"pid": S("xiang_jiamao"), "oid": S("ys_xw"), "title": "县委书记", "start": "2025-02", "end": "", "rank": "正处级"},
    {"pid": S("xiang_jiamao"), "oid": S("ys_zf"), "title": "县长", "start": "2021-10", "end": "", "rank": "正处级"},
    {"pid": S("shi_rongfen"), "oid": S("ls_xw"), "title": "县委书记", "start": "2022-01", "end": "", "rank": "正处级"},
    {"pid": S("zhou_shengyi"), "oid": S("ls_zf"), "title": "县长", "start": "2022-03", "end": "", "rank": "正处级"},
]

relationships = [
    {"a": S("guo_zhenggui"), "b": S("liu_tao"), "type": "predecessor_successor",
     "context": "虢正贵2024年10月卸任后刘涛接任湘西州委书记", "org": S("zhouwei"), "period": "2024-10"},
    {"a": S("chen_hua"), "b": S("shang_shenglong"), "type": "predecessor_successor",
     "context": "陈华2026年6月卸任后尚生龙接任代理州长", "org": S("zhouzhengfu"), "period": "2026-06"},
    {"a": S("liu_tao"), "b": S("shang_shenglong"), "type": "colleague",
     "context": "刘涛（州委书记）与尚生龙（代理州长）搭班", "org": S("zhouwei"), "period": "2026-06起"},
    {"a": S("guo_zhenggui"), "b": S("chen_hua"), "type": "colleague",
     "context": "虢正贵（州委书记）与陈华（州长）搭班约1年9个月", "org": S("zhouwei"), "period": "2023-01至2024-10"},
    {"a": S("liu_tao"), "b": S("chen_hua"), "type": "colleague",
     "context": "刘涛（州委书记）与陈华（州长）搭班约1年半", "org": S("zhouwei"), "period": "2024-10至2026-06"},
    {"a": S("zhou_lizhi"), "b": S("fu_jiasheng"), "type": "colleague",
     "context": "搭班：吉首书记-市长", "org": S("jishou_sw"), "period": "2023-10起"},
    {"a": S("fu_jiabo"), "b": S("he_li"), "type": "colleague",
     "context": "搭班：泸溪书记-县长", "org": S("luxi_xw"), "period": "2026-01起"},
    {"a": S("mao_jia"), "b": S("fan_zhongqing"), "type": "colleague",
     "context": "搭班：凤凰书记-县长", "org": S("fh_xw"), "period": "2022-03起"},
    {"a": S("zhou_jianwu"), "b": S("guo_yingxiang"), "type": "colleague",
     "context": "搭班：保靖书记-县长", "org": S("bj_xw"), "period": "2024-07起"},
    {"a": S("teng_zhaohui"), "b": S("chen_jianxin"), "type": "colleague",
     "context": "搭班：古丈书记-县长", "org": S("gz_xw"), "period": "2024-07起"},
    {"a": S("shi_rongfen"), "b": S("zhou_shengyi"), "type": "colleague",
     "context": "搭班：龙山书记-县长", "org": S("ls_xw"), "period": "2022-03起"},
    {"a": S("fan_zhongqing"), "b": S("shi_rongfen"), "type": "same_native_place",
     "context": "樊忠清与时荣芬同为中国湖南省花垣县人", "org": "", "period": ""},
]

# ══════════════════════════════════════════════════════════════════════
# BUILD SQLite
# ══════════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE persons (id TEXT PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT, source TEXT);
CREATE TABLE organizations (id TEXT PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT);
CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT, title TEXT, start TEXT, end TEXT, rank TEXT, FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id));
CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT, FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id));
""")

for org in organizations:
    c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
              (org["id"], org["name"], org["type"], org["level"], org["parent"], org["location"]))

for p in persons:
    c.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
               p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for pos in positions:
    c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank) VALUES (?,?,?,?,?,?)",
              (pos["pid"], pos["oid"], pos["title"], pos["start"], pos["end"] or None, pos["rank"]))

for r in relationships:
    c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
              (r["a"], r["b"], r["type"], r["context"], r["org"] or None, r["period"] or None))

conn.commit()
conn.close()
print(f"SQLite DB: {DB_PATH}")

# ══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    post = p["current_post"]
    if "州委书记" in post: return "255,50,50"
    if "书记" in post: return "255,50,50"
    if "州长" in post or "县长" in post or "市长" in post: return "50,100,255"
    if "主任" in post: return "255,165,0"
    if "主席" in post: return "180,100,180"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    if "party" in t: return "255,200,200"
    if "gov" in t: return "200,200,255"
    if "npc" in t: return "200,255,255"
    if "cppcc" in t: return "255,240,200"
    return "200,200,200"

def node_size(p):
    post = p["current_post"]
    if "州委书记" in post or "州长" in post: return 20.0
    if "书记" in post or "县长" in post or "市长" in post: return 14.0
    if "主任" in post or "主席" in post: return 12.0
    return 10.0

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
         '  <meta>',
         '    <creator>gov-relation investigator</creator>',
         f'    <description>湘西土家族苗族自治州领导班子工作关系网络 (updated {TODAY})</description>',
         f'    <date>{TODAY}</date>',
         '  </meta>',
         '  <graph mode="static" defaultedgetype="undirected">',
         '    <attributes class="node">',
         '      <attribute id="type" title="Type" type="string"/>',
         '      <attribute id="role" title="Role" type="string"/>',
         '      <attribute id="birth" title="Birth" type="string"/>',
         '      <attribute id="birthplace" title="Birthplace" type="string"/>',
         '      <attribute id="current_post" title="Current Post" type="string"/>',
         '      <attribute id="source" title="Source" type="string"/>',
         '    </attributes>',
         '    <attributes class="edge">',
         '      <attribute id="type" title="Type" type="string"/>',
         '      <attribute id="context" title="Context" type="string"/>',
         '      <attribute id="period" title="Period" type="string"/>',
         '    </attributes>',
         '    <nodes>']
for p in persons:
    c_str = person_color(p)
    sz = node_size(p)
    rgb = c_str.split(",")
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues><attvalue for="type" value="person"/><attvalue for="role" value="{esc(p["current_post"])}"/><attvalue for="birth" value="{esc(p["birth"])}"/><attvalue for="birthplace" value="{esc(p["birthplace"])}"/><attvalue for="current_post" value="{esc(p["current_post"])}"/><attvalue for="source" value="{esc(p["source"])}"/></attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append(f'      </node>')
for o in organizations:
    c_str = org_color(o)
    rgb = c_str.split(",")
    lines.append(f'      <node id="{o["id"]}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues><attvalue for="type" value="organization"/><attvalue for="role" value="{esc(o["type"])}"/><attvalue for="current_post" value=""/><attvalue for="source" value=""/></attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    end_s = pos["end"] or "今"
    lines.append(f'      <edge id="e{eid}" source="{pos["pid"]}" target="{pos["oid"]}" type="directed">')
    lines.append(f'        <attvalues><attvalue for="type" value="worked_at"/><attvalue for="context" value="{esc(pos["title"])} ({esc(pos["start"])}~{esc(end_s)})"/><attvalue for="period" value="{esc(pos["start"])}~{esc(end_s)}"/></attvalues>')
    lines.append(f'        <viz:color r="180" g="180" b="180"/><viz:thickness value="1.0"/>')
    lines.append(f'      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="{r["a"]}" target="{r["b"]}">')
    lines.append(f'        <attvalues><attvalue for="type" value="{esc(r["type"])}"/><attvalue for="context" value="{esc(r["context"])}"/><attvalue for="period" value="{esc(r["period"])}"/></attvalues>')
    if r["type"] == "colleague":
        lines.append(f'        <viz:color r="201" g="169" b="78"/><viz:thickness value="2.5"/>')
    else:
        lines.append(f'        <viz:color r="100" g="150" b="255"/><viz:thickness value="1.5"/>')
    lines.append(f'      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF graph: {GEXF_PATH}")

print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
