#!/usr/bin/env python3
"""Build SQLite, GEXF, and person JSONs for 自贡市 (Zigong)."""

import json
import os
import sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "自贡市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"
DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

PERSONS = [
    [1, "曾洪扬", "男", "汉族", "1972年2月", "四川省广汉市", "", "中共党员", "1994年", "市委书记", "中共自贡市委员会"],
    [2, "石钢", "男", "汉族", "1970年7月", "四川省渠县", "", "中共党员", "", "前市长(2026.6辞职)", "自贡市人民政府"],
    [3, "肖冰东", "男", "汉族", "1979年2月", "湖北省松滋市", "硕士", "中共党员", "2002年7月", "常务副市长", "自贡市人民政府"],
    [4, "朱云", "男", "汉族", "1971年12月", "重庆市", "大学/公共管理硕士", "中共党员", "", "原专职副书记(2026.2调离)", "四川省供销社"],
    [5, "唐鑫", "男", "汉族", "", "", "", "中共党员", "", "纪委书记", "自贡市纪委监委"],
    [6, "刘建贤", "男", "汉族", "1977年1月", "四川省", "在职硕士研究生", "中共党员", "", "组织部部长", "自贡市委组织部"],
    [7, "陈张铭", "男", "汉族", "1977年7月", "", "医学硕士", "九三学社", "", "副市长", "自贡市人民政府"],
    [8, "聂海波", "男", "汉族", "1971年10月", "", "大学", "中共党员", "", "副市长/公安局长", "自贡市人民政府"],
    [9, "韩明祝", "男", "汉族", "1969年10月", "", "工学学士", "中共党员", "", "副市长", "自贡市人民政府"],
    [10, "李文波", "男", "汉族", "1979年6月", "", "经济学硕士", "中共党员", "", "副市长", "自贡市人民政府"],
    [11, "张洪涛", "男", "", "", "", "", "", "", "", "副市长", "自贡市人民政府"],
    [12, "张颖", "女", "黎族", "1976年9月", "", "大学", "民革党员", "", "副市长(挂职)", "自贡市人民政府"],
    [13, "黄如贝", "男", "汉族", "1970年2月", "", "党校研究生", "中共党员", "", "秘书长", "自贡市人民政府办公室"],
    [14, "谭豹", "男", "汉族", "", "", "", "中共党员", "", "人大主任", "自贡市人大常委会"],
    [15, "王猛", "男", "汉族", "1964年", "", "", "中共党员", "", "政协主席", "政协自贡市委员会"],
    [16, "范波", "男", "汉族", "", "", "", "中共党员", "", "前市委书记", ""],
    [17, "何礼", "男", "汉族", "", "", "", "中共党员", "", "前市委书记(2023卸任)", ""],
    [18, "李刚", "男", "汉族", "", "", "", "中共党员", "", "前市委书记/副省长", ""],
]

ORGS = [
    [100001, "中共自贡市委员会", "党委", "地级市", "中共四川省委", "自贡市"],
    [100002, "自贡市人民政府", "政府", "地级市", "四川省人民政府", "自贡市"],
    [100003, "自贡市纪委监委", "纪委", "副厅级", "四川省纪委监委", "自贡市"],
    [100004, "中共自贡市委组织部", "党委", "正处级", "中共自贡市委", "自贡市"],
    [100005, "自贡市公安局", "政府", "正处级", "自贡市人民政府", "自贡市"],
    [100006, "自贡市人民政府办公室", "政府", "正处级", "自贡市人民政府", "自贡市"],
    [100007, "自贡市人大常委会", "人大", "正厅级", "四川省人大常委会", "自贡市"],
    [100008, "政协自贡市委员会", "政协", "正厅级", "四川省政协", "自贡市"],
    [100009, "四川省供销合作社联合社", "事业单位", "正厅级", "四川省人民政府", "成都市"],
]

POSITIONS = [
    [1, 1, 100002, "市长", "2021", "2023", "正厅级", "乐山副书记调任"],
    [2, 1, 100001, "市委书记", "2023", "present", "正厅级", "现任"],
    [3, 2, 100002, "市长", "2023", "2026.06", "正厅级", "2026年6月25日辞职"],
    [4, 3, 100002, "常务副市长", "2021.09", "present", "副厅级", "兼市委常委"],
    [5, 4, 100001, "副书记/政法委书记", "2024.12", "2026.02", "副厅级", "调离"],
    [6, 4, 100009, "党组副书记", "2026.02", "present", "正厅级", "省供销社"],
    [7, 5, 100003, "纪委书记", "2025.03", "present", "副厅级", ""],
    [8, 6, 100004, "组织部部长", "2024.12", "present", "副厅级", ""],
    [9, 7, 100002, "副市长", "unknown", "present", "副厅级", "九三学社"],
    [10, 8, 100005, "副市长/公安局长", "unknown", "present", "副厅级", ""],
    [11, 9, 100002, "副市长", "unknown", "present", "副厅级", ""],
    [12, 10, 100002, "副市长", "unknown", "present", "副厅级", ""],
    [13, 11, 100002, "副市长", "unknown", "present", "副厅级", ""],
    [14, 12, 100002, "副市长(挂职)", "unknown", "present", "副厅级", ""],
    [15, 13, 100006, "秘书长", "unknown", "present", "正处级", ""],
    [16, 14, 100007, "人大主任", "unknown", "present", "正厅级", ""],
    [17, 15, 100008, "政协主席", "unknown", "present", "正厅级", ""],
]

RELS = [
    [1, 2, "predecessor_successor", "曾洪扬升书记后石钢接任市长", "自贡市政府", "2021-2023"],
    [16, 1, "predecessor_successor", "范波前任书记/曾洪扬接任", "中共自贡市委", "2021-2023"],
    [17, 16, "predecessor_successor", "何礼前任书记/范波接任", "中共自贡市委", "2019-2021"],
    [18, 17, "predecessor_successor", "李刚前任书记/何礼接任", "中共自贡市委", "2016-2019"],
]

def mb(s):
    return s if s else ""

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)
    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (p[0], p[1], p[2], p[3], mb(p[4]), mb(p[5]), mb(p[6]), mb(p[7]), mb(p[8]), p[9], p[10]))
    for o in ORGS:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o[0], o[1], o[2], o[3], o[4], o[5]))
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6]))
    for r in RELS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r[0], r[1], r[2], r[3], r[4], r[5]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(PERSONS)} persons, {len(ORGS)} orgs, {len(POSITIONS)} positions, {len(RELS)} relations")

def build_gexf():
    from datetime import datetime as dt
    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
    def pcolor(post):
        if "纪委书记" in post or "监委" in post: return (255,165,0)
        if "组织部" in post: return (255,165,0)
        if "书记" in post and "纪委" not in post: return (255,50,50)
        if "市长" in post: return (50,100,255)
        return (100,100,100)
    def ocolor(typ):
        d = {"党委":(255,200,200),"政府":(200,200,255),"纪委":(255,200,100),
             "人大":(200,255,255),"政协":(255,240,200)}
        return d.get(typ, (200,200,200))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
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
    for p in PERSONS:
        c = pcolor(p[9])
        sz = "20.0" if ("书记" in p[9] and "纪委" not in p[9] and "组织部" not in p[9]) else "12.0"
        lines.append(f'      <node id="p{p[0]}" label="{esc(p[1])}">')
        lines.append(f'        <attvalues><attvalue for="0" value="person"/><attvalue for="1" value="{esc(p[9])}"/></attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/><viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in ORGS:
        c = ocolor(o[2])
        lines.append(f'      <node id="o{o[0]}" label="{esc(o[1])}">')
        lines.append(f'        <attvalues><attvalue for="0" value="org"/><attvalue for="1" value="{esc(o[2])}"/></attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/><viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append(f'        <attvalues><attvalue for="0" value="worked_at"/><attvalue for="1" value="{esc(pos[3])}-{esc(pos[4])}"/></attvalues>')
        lines.append('      </edge>')
    for r in RELS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[3])}" weight="2.0">')
        lines.append(f'        <attvalues><attvalue for="0" value="{esc(r[2])}"/><attvalue for="1" value="{esc(r[3])}"/></attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {eid} edges")

def person_jsons():
    for p in PERSONS:
        fname = f"{TODAY}-四川省-{SLUG}-{p[9].replace('/','_').replace(' ','')}-{p[1]}.json"
        fpath = os.path.join(BASE, fname)
        conf = "confirmed" if mb(p[4]) else "plausible"
        data = {
            "schema_version": "1.0", "generated_at": TODAY,
            "investigation_scope": {"province":"四川省","city":SLUG,"region":SLUG,"job":p[9],"task_id":"sichuan_自贡市","time_focus":"2021-2026"},
            "identity": {
                "person_id": f"zigong_{p[1]}", "name": p[1], "aliases": [], "gender": p[2],
                "ethnicity": p[3], "birth": mb(p[4]), "birthplace": mb(p[5]),
                "party_join": mb(p[7]), "work_start": mb(p[8]),
                "dedupe_keys": {"name_birth": f"{p[1]}_{mb(p[4])}"}
            },
            "current_status": {"current_post": p[9], "current_org": mb(p[10]), "as_of": AS_OF},
            "source_register": [
                {"id":"S001","title":"自贡市政府网站","url":"https://www.zg.gov.cn/","source_type":"official"},
                {"id":"S002","title":"Wikipedia","url":"https://zh.wikipedia.org/zh-cn/自贡市","source_type":"encyclopedia"}
            ],
            "confidence_summary": {"identity": conf, "current_role": "confirmed"}
        }
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {fname}")

if __name__ == "__main__":
    print("Building 自贡市 network...")
    print("1. Person JSONs:")
    person_jsons()
    print("2. Database:")
    build_db()
    print("3. GEXF:")
    build_gexf()
    print("Done.")
