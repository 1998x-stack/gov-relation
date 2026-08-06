#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 建始县, 湖北省恩施土家族苗族自治州.

Current leadership (as of 2026-07-27):
- 县委书记: 李永太
- 代理县长: 周霆 (appointed 2026-07-23)
Sources:
  - 建始县人民政府门户网站 http://www.hbjs.gov.cn (政府领导之窗, 领导简介, 人大会议新闻)
  - 建始网 (县人大常委会会议新闻)
"""

import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────
_STAGING = str(Path(__file__).resolve().parent)
DB_PATH = os.path.join(_STAGING, "建始县_network.db")
GEXF_PATH = os.path.join(_STAGING, "建始县_network.gexf")
os.makedirs(_STAGING, exist_ok=True)

# ── DATA ──────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    # 李永太: 现任县委书记（2026-07-09起），此前任建始县长至2026-07
    {"id": 1, "name": "李永太", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委书记", "current_org": "中共建始县委员会",
     "source": "http://www.hbjs.gov.cn/"},
    # 周霆: 代理县长（2026-07-23），曾于2025年起以代理/主持身份履职
    {"id": 2, "name": "周霆", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-09", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "2006-08",
     "current_post": "建始县委副书记、县人民政府代理县长", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/202607/t20260727_1822202.shtml"},

    # ── 前任县委书记 张渊平（2024→2026-06，去向待查）──
    {"id": 13, "name": "张渊平", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任建始县委书记（约2026-06离任）", "current_org": "中共建始县委员会",
     "source": "http://www.hbjs.gov.cn/"},

    # ── 县委常委会成员（confirmed） ──
    {"id": 14, "name": "张媛", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委副书记（专职）", "current_org": "中共建始县委员会",
     "source": "http://www.hbjs.gov.cn/"},
    {"id": 15, "name": "蒋涛", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委常委、组织部部长", "current_org": "中共建始县委组织部",
     "source": "http://www.hbjs.gov.cn/"},
    {"id": 16, "name": "龙慧", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委常委、宣传部部长", "current_org": "中共建始县委宣传部",
     "source": "http://www.hbjs.gov.cn/"},
    {"id": 17, "name": "牟取", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委常委、纪委书记、县监委主任", "current_org": "建始县监察委员会",
     "source": "http://www.hbjs.gov.cn/"},
    {"id": 18, "name": "金鑫", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委常委、县委办公室主任、县委政法委书记", "current_org": "中共建始县委员会",
     "source": "http://www.hbjs.gov.cn/"},
    {"id": 19, "name": "姚永红", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县政协主席", "current_org": "中国人民政治协商会议建始县委员会",
     "source": "http://www.hbjs.gov.cn/"},
    {"id": 20, "name": "常忠远", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委常委、县人武部部长", "current_org": "建始县人民武装部",
     "source": "http://www.hbjs.gov.cn/"},

    # ── Government leadership ──
    {"id": 3, "name": "谭明", "gender": "男", "ethnicity": "土家族",
     "birth": "1971-11", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县委常委、常务副县长", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/"},
    {"id": 4, "name": "周敏", "gender": "男", "ethnicity": "土家族",
     "birth": "1974-02", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县副县长、县公安局局长", "current_org": "建始县公安局",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/"},
    {"id": 5, "name": "向帆", "gender": "男", "ethnicity": "土家族",
     "birth": "1969-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县副县长", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/"},
    {"id": 6, "name": "何平", "gender": "男", "ethnicity": "土家族",
     "birth": "1975-09", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县副县长", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/202503/t20250326_1682321.shtml"},
    {"id": 7, "name": "瞿勇", "gender": "男", "ethnicity": "土家族",
     "birth": "1983-07", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "建始县副县长", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/202503/t20250326_1682329.shtml"},
    {"id": 8, "name": "刘春全", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-01", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县副县长（挂职）", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/202510/t20251022_1746115.shtml"},
    {"id": 9, "name": "赵佳", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-03", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县副县长（挂职）", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/202510/t20251022_1746118.shtml"},
    {"id": 10, "name": "姚代松", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-05", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县副县长", "current_org": "建始县人民政府",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/202409/t20240920_1617008.shtml"},
    {"id": 11, "name": "陶伟", "gender": "男", "ethnicity": "土家族",
     "birth": "1975-08", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县人民政府党组成员、县政府办公室主任", "current_org": "建始县人民政府办公室",
     "source": "http://www.hbjs.gov.cn/xxgk/gkml/zfld/202409/t20240920_1617010.shtml"},

    # ── 人大常委会 ──
    {"id": 12, "name": "曾凡忠", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "建始县人大常委会主任", "current_org": "建始县人民代表大会常务委员会",
     "source": "http://www.hbjs.gov.cn/sybt/202607/t20260724_1821824.shtml"},
]

organizations = [
    {"id": 1, "name": "中共建始县委员会", "type": "党委", "level": "县处级",
     "parent": "中共恩施州委员会", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 2, "name": "建始县人民政府", "type": "政府", "level": "县处级",
     "parent": "恩施州人民政府", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 3, "name": "建始县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "恩施州人大常委会", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 4, "name": "中国人民政治协商会议建始县委员会", "type": "政协", "level": "县处级",
     "parent": "恩施州政协", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 5, "name": "建始县监察委员会", "type": "纪委", "level": "县处级",
     "parent": "恩施州监察委员会", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 6, "name": "中共建始县委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共建始县委员会", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 7, "name": "中共建始县委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共建始县委员会", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 8, "name": "建始县公安局", "type": "政府", "level": "乡科级",
     "parent": "恩施州公安局", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 9, "name": "建始工业园区", "type": "开发区", "level": "乡科级",
     "parent": "建始县人民政府", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 10, "name": "建始县人民法院", "type": "法院", "level": "县处级",
     "parent": "恩施州中级人民法院", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 11, "name": "建始县人民检察院", "type": "检察院", "level": "县处级",
     "parent": "恩施州人民检察院", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 12, "name": "建始县人民政府办公室", "type": "政府", "level": "乡科级",
     "parent": "建始县人民政府", "location": "湖北省恩施土家族苗族自治州建始县"},
    {"id": 13, "name": "中共恩施州委员会", "type": "党委", "level": "地厅级",
     "parent": "中共湖北省委", "location": "湖北省恩施土家族苗族自治州"},
    {"id": 14, "name": "恩施州人民政府", "type": "政府", "level": "地厅级",
     "parent": "湖北省人民政府", "location": "湖北省恩施土家族苗族自治州"},
    {"id": 15, "name": "建始县人民武装部", "type": "党委", "level": "乡科级",
     "parent": "恩施军分区", "location": "湖北省恩施土家族苗族自治州建始县"},
]

positions = [
    # ── 李永太 ──
    {"person_id": 1, "org_id": 2, "title": "建始县人民政府县长", "start_date": "", "end_date": "2026-07", "rank": "正县级", "note": "出任县委书记前担任县长（2026-01新年献词以县长身份署名）"},
    {"person_id": 1, "org_id": 1, "title": "建始县委书记", "start_date": "2026-07", "end_date": "present", "rank": "正县级", "note": "最迟2026-07-09以县委书记身份主持工作，接替离任的张渊平"},

    # ── 前任县委书记 张渊平 ──
    {"person_id": 13, "org_id": 1, "title": "建始县委书记", "start_date": "2024", "end_date": "2026-06", "rank": "正县级", "note": "约2026年6月底离任，去向待查"},

    # ── 周霆 ──
    {"person_id": 2, "org_id": 2, "title": "建始县委副书记、县人民政府代理县长", "start_date": "2026-07", "end_date": "present", "rank": "正县级", "note": "2026-07-23县人大常委会第三十八次会议决定为代理县长；2025年起以代理/主持身份履职"},

    # ── 县委常委会成员 ──
    {"person_id": 14, "org_id": 1, "title": "建始县委副书记（专职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "建始县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "建始县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 5, "title": "建始县委常委、纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2025年12月当选县监委主任"},
    {"person_id": 18, "org_id": 1, "title": "建始县委常委、县委办公室主任、县委政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "建始县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 20, "org_id": 15, "title": "建始县委常委、县人武部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},

    # ── Government leadership ──
    {"person_id": 3, "org_id": 2, "title": "建始县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 8, "title": "建始县副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "主持县公安局全面工作"},
    {"person_id": 5, "org_id": 2, "title": "建始县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管自然资源规划/住建/城管"},
    {"person_id": 6, "org_id": 2, "title": "建始县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管交通运输/文旅/民族宗教"},
    {"person_id": 7, "org_id": 2, "title": "建始县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管农业农村/水利/林业/乡村"},
    {"person_id": 8, "org_id": 2, "title": "建始县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "华中农业大学对口支援挂职"},
    {"person_id": 9, "org_id": 2, "title": "建始县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "省直部门定点帮扶挂职"},
    {"person_id": 10, "org_id": 9, "title": "建始县副县长/工业园区管委会主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼任建始工业园区党工委副书记、管委会主任"},
    {"person_id": 11, "org_id": 12, "title": "建始县政府党组成员、县政府办公室主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},

    # ── 人大 ──
    {"person_id": 12, "org_id": 3, "title": "建始县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持2026-07-23人大常委会第三十八次会议"},
]

relationships = [
    # 党政搭档（现任）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "李永太（县委书记）与周霆（代理县长）为现任党政主官搭档", "overlap_org": "建始县", "overlap_period": "2026"},
    # 前后任：书记（张渊平→李永太）
    {"person_a": 13, "person_b": 1, "type": "前任继任",
     "context": "张渊平卸任建始县委书记后由李永太接任（约2026年7月）", "overlap_org": "中共建始县委员会", "overlap_period": "2026"},
    # 前后任：县长（李永太→周霆）
    {"person_a": 1, "person_b": 2, "type": "前任继任",
     "context": "李永太由县长升任县委书记，县长职由周霆代理", "overlap_org": "建始县人民政府", "overlap_period": "2026"},
    # 县党政主官与专职副书记
    {"person_a": 1, "person_b": 14, "type": "班子共事",
     "context": "书记与专职副书记张媛在县委班子共事", "overlap_org": "中共建始县委员会", "overlap_period": "2026"},
    # 县长与常务副县长
    {"person_a": 2, "person_b": 3, "type": "直属上下级",
     "context": "代理县长与常务副县长谭明在县政府班子共事", "overlap_org": "建始县人民政府", "overlap_period": ""},
    # 公安局长与县长
    {"person_a": 2, "person_b": 4, "type": "班子共事",
     "context": "代理县长与公安局长周敏在县政府工作班子共事", "overlap_org": "建始县人民政府", "overlap_period": ""},
]

# ── BUILD ─────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS relationships;
    DROP TABLE IF EXISTS positions;
    DROP TABLE IF EXISTS organizations;
    DROP TABLE IF EXISTS persons;
    CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '');
    CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '', level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '');
    CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '');
    CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '');
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""), p.get("birthplace",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""), p.get("current_post",""), p.get("current_org",""), p.get("source","")))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)", (o["id"], o["name"], o.get("type",""), o.get("level",""), o.get("parent",""), o.get("location","")))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)", (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date",""), pos.get("end_date",""), pos.get("rank",""), pos.get("note","")))
    for rel in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)", (rel["person_a"], rel["person_b"], rel["type"], rel["context"], rel["overlap_org"], rel["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


def person_color(p):
    post = p.get("current_post", "")
    if "书记" in post:
        return "255,50,50"
    if "县长" in post or "副" in post:
        return "50,100,255"
    return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    return {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255", "政协": "255,240,200", "开发区": "200,255,200", "纪委": "255,165,0"}.get(t, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>建始县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if ("书记" in p.get("current_post","") or "县长" in p.get("current_post","")) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for rel in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Build complete (staging).")