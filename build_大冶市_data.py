#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大冶市 (Daye City), 黄石市, 湖北省.

Level: 县级市
Province: 湖北省
Parent city: 黄石市
Targets: 市委书记 (Party Secretary) & 市长 (Mayor)
Task ID: hubei_大冶市

Research date: 2026-08-06
Official source: https://www.hbdaye.gov.cn/ (大冶政府网) — accessible
  + 云上大冶 https://www.dayeyun.cn (大冶市融媒体中心官方新闻)

Current status (as of 2026-08-06):
- 市委书记: 孙辄 (confirmed via multiple official 云上大冶 news: 七届市委审计委员会、市委理论学习中心组、市政协七届常委会、市委常委会会议均署名「市委书记孙辄」)
- 市长: 潘小进 (confirmed via official 大冶政府网「政府领导」领导列表 szfld/ 页，任职标识为「市委副书记、市政府市长，高新区党工委书记」)

Confidence notes:
- 现任市委书记、市长身份: confirmed (官方新闻 + 政府网领导之窗)
- 政府班子 (常务副市长、副市长、市政府党组成员)、市人大主任、市政协主席: confirmed via 大冶政府网 szfld 页 + 官方新闻
- 出生年月/籍贯/学历/入党参工时间/简历: unverified — 百度/搜狗/Google/Bing 均反爬受限
- 前任书记/市长去向: unverified — 未获取任前公示/卸任新闻
- 其他市委常委 (组织/宣传/纪委/政法等): 未从官方来源逐一确认个体，标记为待查
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "大冶市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

PROVINCE = "湖北省"
PARENT_CITY = "黄石市"
LOCATION = "湖北省黄石市大冶市"

# Official source URLs collected during research
URL_XW = "https://www.hbdaye.gov.cn/"                                        # 大冶政府网首页
URL_SZF_LD = "https://www.hbdaye.gov.cn/zfxxgk/fdgknr/szfld/"                # 政府领导之窗
URL_SZ_BIO = "https://www.hbdaye.gov.cn/zfxxgk/fdgknr/szfld/sz/202101/t20210111_750500.html"  # 市长简介
URL_CW_BIO = "https://www.hbdaye.gov.cn/zfxxgk/fdgknr/szfld/fsz/202111/t20211110_851300.html"  # 常务副市长简介
URL_YUN = "https://www.dayeyun.cn/"                                          # 云上大冶
URL_AUDIT = "https://www.dayeyun.cn/p/175803.html"                           # 七届市委审计委员会第十二次会议
URL_ZXH = "https://www.hbdaye.gov.cn/xwzx/ttxw/202607/t20260728_1346541.html"  # 市政协七届常委会第二十七次会议
URL_ZXL = "https://www.hbdaye.gov.cn/xwzx/dyyw/202608/t20260802_1347599.html"  # 全市基层人大工作例会
URL_LXX = "https://www.hbdaye.gov.cn/xwzx/ttxw/202608/t20260802_1347608.html"  # 市委常委会会议

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {"id": 1, "name": "孙辄", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共大冶市委员会", "source": URL_YUN},
    {"id": 2, "name": "潘小进", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "大冶市人民政府", "source": URL_SZ_BIO},
    # ═══════ 市政府领导 (政府领导之窗) ═══════
    {"id": 3, "name": "杨早容", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、常务副市长", "current_org": "大冶市人民政府", "source": URL_CW_BIO},
    {"id": 4, "name": "余智彬", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市政府党组成员", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 5, "name": "徐铭", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 6, "name": "辜春华", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 7, "name": "尹朝晖", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 8, "name": "吴飞", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 9, "name": "朱勇强", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 10, "name": "马新国", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 11, "name": "张辉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府党组成员", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 12, "name": "黄小容", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府党组成员", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    {"id": 13, "name": "冯魏良", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府党组成员", "current_org": "大冶市人民政府", "source": URL_SZF_LD},
    # ═══════ 市人大常委会 ═══════
    {"id": 14, "name": "毛文胜", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会党组书记、主任", "current_org": "大冶市人大常委会", "source": URL_ZXL},
    {"id": 15, "name": "黄茂林", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会副主任", "current_org": "大冶市人大常委会", "source": URL_ZXL},
    {"id": 16, "name": "胡卫东", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会党组成员", "current_org": "大冶市人大常委会", "source": URL_ZXL},
    # ═══════ 市政协 ═══════
    {"id": 17, "name": "李祥坤", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政协主席", "current_org": "政协大冶市委员会", "source": URL_ZXH},
    {"id": 18, "name": "梅相东", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市政协秘书长", "current_org": "政协大冶市委员会", "source": URL_ZXH},
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大冶市委员会", "type": "党委", "level": "县级市", "parent": "中共黄石市委员会", "location": LOCATION},
    {"id": 2, "name": "大冶市人民政府", "type": "政府", "level": "县级市", "parent": "黄石市人民政府", "location": LOCATION},
    {"id": 3, "name": "大冶市人大常委会", "type": "人大", "level": "县级市", "parent": "黄石市人大常委会", "location": LOCATION},
    {"id": 4, "name": "政协大冶市委员会", "type": "政协", "level": "县级市", "parent": "政协黄石市委员会", "location": LOCATION},
    {"id": 5, "name": "中共大冶市纪律检查委员会/大冶市监察委员会", "type": "党委", "level": "县级市", "parent": "中共黄石市纪律检查委员会", "location": LOCATION},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": "现任，截至2026-08-06 confirmed"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副处级", "note": "市委副书记、市政府市长"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正处级", "note": "现任，截至2026-08-06 confirmed"},
    {"person_id": 3, "org_id": 2, "title": "市委常委、常务副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "市委常委、市政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "市政府党组成员", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "市政府党组成员", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "市政府党组成员", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "市人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "市人大常委会党组成员", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "市政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "市政协秘书长", "start": "", "end": "present", "rank": "正科级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政主要领导搭档", "overlap_org": "大冶市", "overlap_period": "current"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与常务副市长（同任市委常委）", "overlap_org": "中共大冶市委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与市政府党组成员（同任市委常委）", "overlap_org": "中共大冶市委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "大冶市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "大冶市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "大冶市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "大冶市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "大冶市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "大冶市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "大冶市人民政府", "overlap_period": "current"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "市委书记与市人大常委会主任党政配合", "overlap_org": "大冶市", "overlap_period": "current"},
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "市委书记出席市政协常委会并作讲话", "overlap_org": "大冶市", "overlap_period": "current"},
]


# ── Helper Functions ───────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "")
    if post.startswith("市委书记"):
        return "255,50,50"
    if post == "市委副书记、市长" or post == "市长" or post.startswith("副市长") or "常务副市长" in post:
        return "50,100,255"
    if "市纪委书记" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    post = p.get("current_post", "")
    return post.startswith("市委书记") or post == "市长" or post == "市委副书记、市长"


def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }
    return colors.get(o.get("type", ""), "200,200,200")


def build_db(conn):
    """Create the 4 standard tables and bulk-insert."""
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        conn.execute(
            "INSERT OR REPLACE INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        conn.execute(
            "INSERT OR REPLACE INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r.get("type", ""), r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", "")))
    conn.commit()


def generate_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 using string formatting (avoids ElementTree namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network — {PROVINCE} {PARENT_CITY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p).split(",")
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('          <attvalue for="3" value="县级市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        context = r.get("context", r.get("type", ""))
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(context)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    conn = sqlite3.connect(str(DB_PATH))
    try:
        build_db(conn)
    finally:
        conn.close()
    print(f"DB written: {DB_PATH}")

    generate_gexf(persons, organizations, positions, relationships, GEXF_PATH)
    print(f"GEXF written: {GEXF_PATH}")
    print("=== Done ===")


if __name__ == "__main__":
    main()