#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 伊美区 (Yimei District), 伊春市, 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_伊美区
Level: 市辖区
Targets: 区委书记 (张正强) & 区长 (张斐)

Research sources (official, primary):
  - 伊美区人民政府门户 http://www.ycym.gov.cn/  (文字新闻/图片新闻/统计公报/政协信息)
  - 伊春市政府门户 http://www.yc.gov.cn/  (用于定位伊美区政务门户)
  - Wikipedia (市级领导与行政区划辅助)

Research Note (partial-evidence artifact mode, source_fallbacks.md):
  www.ycym.gov.cn 完整可访问，确认核心党政一把手及主要班子名单。
  - 现任区委书记：张正强 (二届184/186次常委会、书记专题会、七一慰问、巡河巡林等官方稿确认)
  - 现任区委副书记、区长：张斐 (东升镇党课、表彰大会主持、城市更新调研等官方稿确认)
  - 多名区领导(苏慧明/冯玉龙/朱沛瑶/李佳徽赵书博/金首红)具体职务待细分；区纪委书记/组织部长/政法委书记
    未见官网表单，属履历缺口。
  依 partial-evidence artifact mode，仍产出结构有效产物，并以 confidence/open_questions/report 标记不确定性。
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "伊美区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────

persons = [
    # 核心党政一把手
    {"id": 1, "name": "张正强", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共伊美区委员会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/429559.shtml"},
    {"id": 2, "name": "张斐", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区长", "current_org": "伊美区人民政府",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202607/430202.shtml"},
    # 区委班子
    {"id": 3, "name": "迟鑫", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共伊美区委员会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/429560.shtml"},
    {"id": 4, "name": "王智杰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长、统战部部长", "current_org": "中共伊美区委员会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202607/430203.shtml"},
    {"id": 5, "name": "齐新宇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区人民政府副区长", "current_org": "伊美区人民政府",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428956.shtml"},
    {"id": 6, "name": "谢寒", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、东升镇党委书记", "current_org": "中共伊美区东升镇委员会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202607/430202.shtml"},
    {"id": 7, "name": "宫媛媛", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人民政府副区长", "current_org": "伊美区人民政府",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/428034.shtml"},
    # 区领导，具体职务待细分
    {"id": 8, "name": "苏慧明", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区领导（职务待细分）", "current_org": "伊美区",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/428542.shtml"},
    {"id": 9, "name": "冯玉龙", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区领导（职务待细分）", "current_org": "伊美区",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428033.shtml"},
    {"id": 10, "name": "李佳徽", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区领导（职务待细分）", "current_org": "伊美区",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/428545.shtml"},
    {"id": 11, "name": "赵书博", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区领导（职务待细分）", "current_org": "伊美区",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/428542.shtml"},
    {"id": 12, "name": "朱沛瑶", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区领导（职务待细分）", "current_org": "伊美区",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/428542.shtml"},
    {"id": 13, "name": "金首红", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区领导（职务待细分）", "current_org": "伊美区",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/428035.shtml"},
    # 人大 / 政协
    {"id": 14, "name": "刘玉静", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "伊美区人大常委会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428956.shtml"},
    {"id": 15, "name": "李亮", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "伊美区人大常委会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428956.shtml"},
    {"id": 16, "name": "孙莹", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "伊美区人大常委会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428956.shtml"},
    {"id": 17, "name": "王珺", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "伊美区人大常委会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428956.shtml"},
    {"id": 18, "name": "王英", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政协党组书记、主席", "current_org": "政协伊美区委员会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101961/202607/431113.shtml"},
    {"id": 19, "name": "杨蕾", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区政协副主席", "current_org": "政协伊美区委员会",
     "source": "http://www.ycym.gov.cn/ymqrmzf/c101961/202607/431113.shtml"},
    # 伊春市级领导
    {"id": 20, "name": "董文琴", "gender": "女", "ethnicity": "汉族", "birth": "1972年10月",
     "birthplace": "黑龙江省宾县", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市委书记、市人大常委会主任", "current_org": "中共伊春市委员会",
     "source": "https://zh.wikipedia.org/wiki/伊春市"},
    {"id": 21, "name": "苑芳江", "gender": "男", "ethnicity": "汉族", "birth": "1977年3月",
     "birthplace": "黑龙江省穆棱市", "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市委副书记、市长", "current_org": "伊春市人民政府",
     "source": "https://zh.wikipedia.org/wiki/伊春市"},
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共伊美区委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市伊美区"},
    {"id": 2, "name": "伊美区人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市伊美区"},
    {"id": 3, "name": "伊美区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "伊春市人大常委会", "location": "黑龙江省伊春市伊美区"},
    {"id": 4, "name": "政协伊美区委员会", "type": "政协", "level": "县处级", "parent": "政协伊春市委员会", "location": "黑龙江省伊春市伊美区"},
    {"id": 5, "name": "中共伊美区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共伊春市纪律检查委员会", "location": "黑龙江省伊春市伊美区"},
    {"id": 6, "name": "中共伊美区东升镇委员会", "type": "乡镇", "level": "乡科级", "parent": "中共伊美区委员会", "location": "黑龙江省伊春市伊美区东升镇"},
    {"id": 7, "name": "中共伊春市委员会", "type": "党委", "level": "地市级", "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市伊美区"},
    {"id": 8, "name": "伊春市人民政府", "type": "政府", "level": "地市级", "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市伊美区"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    {"person_id": 1, "org_id": 1, "title": "伊美区委书记", "start": "", "end": "", "rank": "县处级正职", "note": "至迟2026年6月在任；主持二届184/186次常委会、书记专题会、巡察等"},
    {"person_id": 2, "org_id": 1, "title": "伊美区委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "区政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "伊美区长", "start": "", "end": "", "rank": "县处级正职", "note": "区委副书记、区长"},
    {"person_id": 3, "org_id": 1, "title": "伊美区委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委、宣传部部长、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "伊美区委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "伊美区人民政府副区长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "伊美区委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "东升镇党委书记", "start": "", "end": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "伊美区人民政府副区长", "start": "", "end": "", "rank": "县处级副职", "note": "分管教育/招考"},
    {"person_id": 8, "org_id": 1, "title": "区领导（苏慧明）", "start": "", "end": "", "rank": "县处级副职", "note": "疑常务副区长/区委副书记"},
    {"person_id": 9, "org_id": 1, "title": "区领导（冯玉龙）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "区领导（李佳徽）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "区领导（赵书博）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "区领导（朱沛瑶）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "区领导（金首红）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "区政协党组书记、主席", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "区政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 7, "title": "伊春市委书记", "start": "2024年9月", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 20, "org_id": 7, "title": "伊春市人大常委会主任", "start": "2025年1月", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 21, "org_id": 7, "title": "伊春市委副书记", "start": "2024年9月", "end": "", "rank": "地厅级副职", "note": ""},
    {"person_id": 21, "org_id": 8, "title": "伊春市市长", "start": "2024年9月", "end": "", "rank": "地厅级正职", "note": "代市长转正"},
    {"person_id": 20, "org_id": 8, "title": "伊春市市长（前任）", "start": "", "end": "2024-09", "rank": "地厅级正职", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "区委书记与区长党政搭档；常委会/专题会/表彰大会多场同场", "overlap_org": "伊美区", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记领导下辖区委副书记迟鑫", "overlap_org": "中共伊美区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记领导区委常委王智杰", "overlap_org": "中共伊美区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记领导区委常委齐新宇", "overlap_org": "中共伊美区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记领导区委常委谢寒", "overlap_org": "中共伊美区委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长领导副区长宫媛媛", "overlap_org": "伊美区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长领导区委常委副区长齐新宇", "overlap_org": "伊美区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 18, "type": "同僚", "context": "区委与区政协主席王英在招商'一号工程'协作", "overlap_org": "伊美区", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "同僚", "context": "区人大主任刘玉静监督区政府工作", "overlap_org": "伊美区", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 20, "type": "上下级", "context": "伊春市委书记领导伊美区委书记", "overlap_org": "伊春市", "overlap_period": "2024年起"},
    {"person_a": 2, "person_b": 21, "type": "上下级", "context": "伊春市市长领导伊美区长", "overlap_org": "伊春市人民政府", "overlap_period": "2024年起"},
    {"person_a": 20, "person_b": 21, "type": "党政同僚", "context": "市委书记与市长党政搭档", "overlap_org": "中共伊春市委员会", "overlap_period": "2024年9月起"},
]


# ══════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════

esc = lambda s: (str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else "")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT)""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT, rank TEXT, note TEXT)""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT)""")
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                     p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    conn.commit(); conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)}p, {len(organizations)}o, {len(positions)}pos, {len(relationships)}rel)")


# ══════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════

def person_color(post):
    if post and post.strip() == "区委书记":
        return ("255,50,50", 20.0)
    if "区长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    if "副区长" in post or "副书记" in post:
        return ("100,150,255", 12.0)
    if "常委" in post:
        return ("100,150,255", 12.0)
    if "政协" in post or "人大常委会" in post:
        return ("120,180,120", 12.0)
    if "区领导" in post:
        return ("150,150,150", 12.0)
    return ("100,100,100", 12.0)

def org_color(t):
    colors = {"党委":("255,200,200",8.0),"政府":("200,200,255",8.0),"纪委":("255,200,200",8.0),
              "人大":("200,255,255",8.0),"政协":("255,240,200",8.0),"乡镇":("255,255,200",8.0)}
    return colors.get(t, ("200,200,200", 8.0))


def build_gexf():
    from datetime import datetime as _dt
    L = []
    L.append('<?xml version="1.0" encoding="UTF-8"?>')
    L.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    L.append(f'  <meta lastmodifieddate="{_dt.now().strftime("%Y-%m-%d")}">')
    L.append('    <creator>Sisyphus Research Agent</creator>')
    L.append(f'    <description>伊美区领导班子工作关系网络 - {AS_OF}</description>')
    L.append('  </meta>')
    L.append('  <graph mode="static" defaultedgetype="undirected">')
    L.append('    <attributes class="node">')
    L.append('      <attribute id="0" title="type" type="string"/>')
    L.append('      <attribute id="1" title="current_post" type="string"/>')
    L.append('      <attribute id="2" title="current_org" type="string"/>')
    L.append('      <attribute id="3" title="birth" type="string"/>')
    L.append('    </attributes>')
    L.append('    <attributes class="edge">')
    L.append('      <attribute id="0" title="type" type="string"/>')
    L.append('      <attribute id="1" title="context" type="string"/>')
    L.append('    </attributes>')
    L.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        L.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        L.append('        <attvalues>')
        L.append(f'          <attvalue for="0" value="person"/>')
        L.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        L.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        L.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        L.append('        </attvalues>')
        L.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        L.append(f'        <viz:size value="{sz}"/>')
        L.append('      </node>')
    for o in organizations:
        c, sz = org_color(o["type"])
        L.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        L.append('        <attvalues>')
        L.append('          <attvalue for="0" value="organization"/>')
        for i in (1, 2, 3):
            L.append(f'          <attvalue for="{i}" value=""/>')
        L.append('        </attvalues>')
        L.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        L.append(f'        <viz:size value="{sz}"/>')
        L.append('      </node>')
    L.append('    </nodes>')
    L.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        L.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        L.append('        <attvalues>')
        L.append(f'          <attvalue for="0" value="worked_at"/>')
        L.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        L.append('        </attvalues>')
        L.append('      </edge>')
    for r in relationships:
        eid += 1
        L.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        L.append('        <attvalues>')
        L.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        L.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        L.append('        </attvalues>')
        L.append('      </edge>')
    L.append('    </edges>')
    L.append('  </graph>')
    L.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "区委书记张正强开展'七一'节前走访慰问活动", "url": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/429559.shtml", "publisher": "伊美区人民政府", "published_at": "2026-06-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认张正强为区委书记"},
        {"id": "S002", "title": "中共伊美区委召开二届186次常委会会议", "url": "http://www.ycym.gov.cn/ymqrmzf/c101553/202607/430201.shtml", "publisher": "伊美区人民政府办公室", "published_at": "2026-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2026-07-09 区委书记张正强主持"},
        {"id": "S003", "title": "张斐到东升镇讲授树立和践行正确政绩观学习教育专题党课", "url": "http://www.ycym.gov.cn/ymqrmzf/c101553/202607/430202.shtml", "publisher": "伊美区人民政府办公室", "published_at": "2026-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委副书记、区长张斐"},
        {"id": "S004", "title": "中共伊美区委召开二届184次常委会会议", "url": "http://www.ycym.gov.cn/ymqrmzf/c101553/202606/428953.shtml", "publisher": "伊美区人民政府办公室", "published_at": "2026-06-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张正强主持"},
        {"id": "S005", "title": "中央巡视反馈意见整改工作领导小组会议召开", "url": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428033.shtml", "publisher": "伊美区人民政府", "published_at": "2026-06-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张正强主持；张斐、迟鑫、冯玉龙、王智杰、苏慧明、齐新宇、谢寒、李亮、宫媛媛、李佳徽、赵书博出席"},
        {"id": "S006", "title": "伊美区庆祝中国共产党成立105周年暨'两优一先'表彰大会召开", "url": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/429560.shtml", "publisher": "伊美区人民政府办公室", "published_at": "2026-06-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张正强讲话、张斐主持、区委副书记迟鑫宣读表彰决定"},
        {"id": "S007", "title": "伊美区二届人大常委会第三十九次会议召开", "url": "http://www.ycym.gov.cn/ymqrmzf/c101550/202606/428956.shtml", "publisher": "伊美区人民政府办公室", "published_at": "2026-06-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区人大主任刘玉静、副主任李亮·孙莹·王珺；区委常委副区长齐新宇列席"},
        {"id": "S008", "title": "王智杰讲授'勇担宣传使命 端正政绩导向'学习教育专题党课", "url": "http://www.ycym.gov.cn/ymqrmzf/c101550/202607/430203.shtml", "publisher": "伊美区人民政府办公室", "published_at": "2026-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委常委、宣传部部长、统战部部长王智杰"},
        {"id": "S009", "title": "王英主持召开企业委员招商引资座谈会", "url": "http://www.ycym.gov.cn/ymqrmzf/c101961/202607/431113.shtml", "publisher": "伊美区人民政府", "published_at": "2026-07-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区政协党组书记、主席王英"},
        {"id": "S010", "title": "2025年伊美区国民经济和社会发展统计公报", "url": "http://www.ycym.gov.cn/ymqrmzf/c101915/202607/430591.shtml", "publisher": "伊美区统计局", "published_at": "2026-07-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2025 GDP 69.7亿, +2.9%, 三次产业 12.7:9.2:78.1"},
        {"id": "S011", "title": "伊春市—现任领导", "url": "https://zh.wikipedia.org/wiki/伊春市", "publisher": "Wikipedia", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "high", "notes": "伊春市委书记董文琴、市长苑芳江"},
    ]


def make_person_json(p, timeline, rels, src):
    cur_role_confirmed = "待细分" not in p["current_post"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "黑龙江省", "city": "伊春市", "region": "伊美区", "job": p["current_post"], "task_id": "heilongjiang_伊美区", "time_focus": "2026年7月"},
        "identity": {
            "person_id": f"yimeiqu_{p['name']}", "name": p["name"], "aliases": [], "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""), "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": p.get("party_join", "").replace("中共党员", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth','')}", "name_birthplace": f"{p['name']}_{p.get('birthplace','')}", "official_profile_url": p.get("source", "")}
        },
        "current_status": {"current_post": p["current_post"], "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if (("书记" in p["current_post"] and "副" not in p["current_post"]) or "区长" in p["current_post"]) else "县处级副职",
            "as_of": AS_OF, "is_current_confirmed": cur_role_confirmed, "source_ids": []},
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown",
            "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "insufficient", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在公开信息中发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}],
        "source_register": src,
        "confidence_summary": {"identity": "confirmed" if p.get("birth") else "plausible", "current_role": "confirmed" if cur_role_confirmed else "unverified",
            "career_completeness": "partial" if p.get("birth") else "thin", "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历（出生/籍贯/学历/入党/到任日期/任前经历）尚未找到"},
        "open_questions": [
            {"priority": "critical", "question": f"{p['name']}的出生年份、籍贯、学历与入党时间", "why_it_matters": "用于跨区县去重与关系挖掘", "suggested_queries": [f"{p['name']} 简历 伊美区", f"{p['name']} 任前公示"], "last_attempted": AS_OF},
            {"priority": "critical", "question": f"{p['name']} 任{p['current_post']}前的任职路径（前任/接任链）", "why_it_matters": "还原晋升路径与跨区交流网络", "suggested_queries": [f"{p['name']} 此前 担任 伊美"], "last_attempted": AS_OF}
        ]
    }


def build_person_jsons():
    src = make_source_register()

    # 1. 张正强（区委书记）
    j1 = make_person_json(persons[0], [
        {"start": "unknown", "end": "present", "org": "中共伊美区委员会", "title": "区委书记", "level": "县处级", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "至迟2026年6月在任；主持二届184/186次常委会、书记专题会、巡察等", "confidence": "confirmed", "source_ids": ["S001", "S002", "S004"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到任区委书记前的完整履历", "confidence": "unverified", "source_ids": []},
    ], [
        {"person": "张斐", "person_id": "yimeiqu_张斐", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区长党政搭档，多场会议同场", "overlap_org": "伊美区", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S006"]},
        {"person": "迟鑫", "person_id": "yimeiqu_迟鑫", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区委书记领导下区委副书记", "overlap_org": "中共伊美区委员会", "overlap_period": "2026-", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S006"]},
    ], src)
    p1 = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-区委书记-张正强.json"
    with open(p1, "w", encoding="utf-8") as f:
        json.dump(j1, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {p1.name}")

    # 2. 张斐（区长）
    j2 = make_person_json(persons[1], [
        {"start": "unknown", "end": "present", "org": "伊美区人民政府", "title": "区长", "level": "县处级", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "区委副书记、区长；主持区政府全面工作；2026年7月在任", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "present", "org": "中共伊美区委员会", "title": "区委副书记", "level": "县处级", "system": "party", "rank": "县处级副职", "is_key_promotion": False, "notes": "兼任区委副书记", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到任区长的完整履历", "confidence": "unverified", "source_ids": []},
    ], [
        {"person": "张正强", "person_id": "yimeiqu_张正强", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与区委书记党政搭档", "overlap_org": "伊美区", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S006"]},
        {"person": "齐新宇", "person_id": "yimeiqu_齐新宇", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区长领导下区委常委副区长", "overlap_org": "伊美区人民政府", "overlap_period": "2026-", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S007"]},
    ], src)
    p2 = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-区长-张斐.json"
    with open(p2, "w", encoding="utf-8") as f:
        json.dump(j2, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {p2.name}")

    # 3. 迟鑫（区委副书记）
    j3 = make_person_json(persons[3], [
        {"start": "unknown", "end": "present", "org": "中共伊美区委员会", "title": "区委副书记", "notes": "2026-06-28 表彰大会宣读表彰决定", "confidence": "confirmed", "source_ids": ["S006"]},
    ], [
        {"person": "张正强", "person_id": "yimeiqu_张正强", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区委书记领导下区委副书记", "overlap_org": "中共伊美区委员会", "overlap_period": "2026-", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S006"]},
    ], src)
    p3 = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-区委副书记-迟鑫.json"
    with open(p3, "w", encoding="utf-8") as f:
        json.dump(j3, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {p3.name}")


def main():
    print("=" * 60)
    print("  伊美区领导班子工作关系网络")
    print("  等级: 市")
    print("  调查日期: 2026-08-05")
    print("  信息来源: 伊美区人民政府门户")
    print("=" * 60)
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\n✅ 伊美区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)}  机构: {len(organizations)}  任职: {len(positions)}  关系: {len(relationships)}")


if __name__ == "__main__":
    main()