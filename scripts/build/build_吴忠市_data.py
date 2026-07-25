#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 吴忠市 (Wuzhong City) leadership network.

Current as of: 2026-07-25
Data sources:
  - https://www.wuzhong.gov.cn/xxgk/ldzc/ (吴忠市领导之窗 - official leadership listing, primary source)
  - https://www.wuzhong.gov.cn/ (吴忠市人民政府 website)

Confidence notes:
  - Current roles and basic biographical info: CONFIRMED via official government leadership page (July 2026)
  - Biographical details (early career history, education specifics, precise birthplace): mostly unverified
  - All claims labeled with confidence level; gaps explicitly documented
  - The 市长 position is currently vacant/transitioning - 白学贵 is "提名为市长候选人"
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / "吴忠市_network.db"
GEXF_PATH = STAGING / "吴忠市_network.gexf"

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "吴忠市"
TODAY = "2026-07-25"
PROVINCE = "宁夏回族自治区"
LEVEL = "地级市"

# ── Persons ─────────────────────────────────────────────────────────
# IDs: 1-9 core party/government leaders, 10-19 standing committee, 20-29 deputy govt
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════
    {"id": 1, "name": "门立群", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委书记", "current_org": "中共吴忠市委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 2, "name": "白学贵", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-10", "birthplace": "",
     "education": "宁夏党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委副书记、提名为市长候选人", "current_org": "中共吴忠市委员会/吴忠市人民政府",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    # ══════════════════════════════════════════════════════════════════════
    # Other Standing Committee Members (市委常委)
    # ══════════════════════════════════════════════════════════════════════
    {"id": 3, "name": "白小军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-12", "birthplace": "",
     "education": "中央党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委副书记、市委秘书长、政法委书记", "current_org": "中共吴忠市委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 4, "name": "丁建成", "gender": "男", "ethnicity": "回族",
     "birth": "1966-08", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委常委、统战部部长", "current_org": "中共吴忠市委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 5, "name": "万玉忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-04", "birthplace": "",
     "education": "中央党校研究生学历、公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委常委、组织部部长", "current_org": "中共吴忠市委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 6, "name": "苏焕喜", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "",
     "education": "宁夏党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委常委、市人民政府党组副书记、副市长（常务）", "current_org": "中共吴忠市委员会/吴忠市人民政府",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 7, "name": "查碧然", "gender": "男", "ethnicity": "回族",
     "birth": "1975-08", "birthplace": "",
     "education": "在职研究生学历、法学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委常委、纪委书记、监委主任", "current_org": "中共吴忠市纪律检查委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 8, "name": "杨春燕", "gender": "女", "ethnicity": "回族",
     "birth": "1972-08", "birthplace": "",
     "education": "宁夏党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委常委、宣传部部长", "current_org": "中共吴忠市委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 9, "name": "米成坤", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-05", "birthplace": "",
     "education": "研究生学历、公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委常委、市人民政府副市长（挂职）", "current_org": "中共吴忠市委员会/吴忠市人民政府",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 10, "name": "文学智", "gender": "男", "ethnicity": "回族",
     "birth": "1978-03", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市委常委、青铜峡市委书记", "current_org": "中共吴忠市委员会/中共青铜峡市委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership (副市长)
    # ══════════════════════════════════════════════════════════════════════
    {"id": 11, "name": "马同松", "gender": "男", "ethnicity": "回族",
     "birth": "1977-01", "birthplace": "",
     "education": "宁夏大学法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市副市长", "current_org": "吴忠市人民政府",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 12, "name": "李亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市副市长、市公安局局长", "current_org": "吴忠市人民政府/吴忠市公安局",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 13, "name": "马学峰", "gender": "男", "ethnicity": "回族",
     "birth": "1969-07", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市副市长", "current_org": "吴忠市人民政府",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 14, "name": "黄培", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-09", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市副市长", "current_org": "吴忠市人民政府",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 15, "name": "尚自刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-02", "birthplace": "",
     "education": "大学学历",
     "party_join": "农工党党员", "work_start": "",
     "current_post": "吴忠市副市长", "current_org": "吴忠市人民政府",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    {"id": 16, "name": "马泰", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "",
     "education": "党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市人民政府秘书长", "current_org": "吴忠市人民政府办公室",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    # ══════════════════════════════════════════════════════════════════════
    # 人大领导
    # ══════════════════════════════════════════════════════════════════════
    {"id": 17, "name": "兰德明", "gender": "男", "ethnicity": "回族",
     "birth": "1970-03", "birthplace": "",
     "education": "中央党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市人大常委会主任", "current_org": "吴忠市人民代表大会常务委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
    # ══════════════════════════════════════════════════════════════════════
    # 政协领导
    # ══════════════════════════════════════════════════════════════════════
    {"id": 18, "name": "高建博", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-09", "birthplace": "",
     "education": "中央党校大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴忠市政协主席", "current_org": "中国人民政治协商会议吴忠市委员会",
     "source": "https://www.wuzhong.gov.cn/xxgk/ldzc/"},
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共吴忠市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区吴忠市"},
    {"id": 2, "name": "吴忠市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区吴忠市"},
    {"id": 3, "name": "中共吴忠市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "中共宁夏回族自治区纪律检查委员会", "location": "宁夏回族自治区吴忠市"},
    {"id": 4, "name": "吴忠市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "宁夏回族自治区人民代表大会常务委员会", "location": "宁夏回族自治区吴忠市"},
    {"id": 5, "name": "中国人民政治协商会议吴忠市委员会", "type": "政协", "level": "地级市", "parent": "中国人民政治协商会议宁夏回族自治区委员会", "location": "宁夏回族自治区吴忠市"},
    {"id": 6, "name": "吴忠市人民政府办公室", "type": "政府", "level": "正处级", "parent": "吴忠市人民政府", "location": "宁夏回族自治区吴忠市"},
    {"id": 7, "name": "吴忠市公安局", "type": "政府", "level": "正处级", "parent": "吴忠市人民政府", "location": "宁夏回族自治区吴忠市"},
    {"id": 8, "name": "中共青铜峡市委员会", "type": "党委", "level": "县级市", "parent": "中共吴忠市委员会", "location": "宁夏回族自治区吴忠市青铜峡市"},
]

# ── Positions ─────────────────────────────────────────────────────
positions = [
    # 门立群 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "吴忠市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "主持市委全面工作"},
    # 白学贵 - 副书记/代市长
    {"person_id": 2, "org_id": 1, "title": "吴忠市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "提名为市长候选人"},
    # 白小军 - 副书记
    {"person_id": 3, "org_id": 1, "title": "吴忠市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任市委秘书长、政法委书记"},
    # 丁建成 - 市委常委、统战部长
    {"person_id": 4, "org_id": 1, "title": "吴忠市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任统战部部长"},
    # 万玉忠 - 市委常委、组织部长
    {"person_id": 5, "org_id": 1, "title": "吴忠市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任组织部部长"},
    # 苏焕喜 - 市委常委、常务副市长
    {"person_id": 6, "org_id": 1, "title": "吴忠市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市人民政府党组副书记"},
    # 查碧然 - 市委常委、纪委书记
    {"person_id": 7, "org_id": 1, "title": "吴忠市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "吴忠市纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 杨春燕 - 市委常委、宣传部长
    {"person_id": 8, "org_id": 1, "title": "吴忠市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任宣传部部长"},
    # 米成坤 - 市委常委、副市长（挂职）
    {"person_id": 9, "org_id": 1, "title": "吴忠市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 文学智 - 市委常委、青铜峡市委书记
    {"person_id": 10, "org_id": 1, "title": "吴忠市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "青铜峡市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼任青铜峡工业园区党工委书记"},
    # 马同松 - 副市长
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李亮 - 副市长、公安局长
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 马学峰 - 副市长
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 黄培 - 副市长
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 尚自刚 - 副市长
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "农工党党员"},
    # 马泰 - 秘书长
    {"person_id": 16, "org_id": 6, "title": "市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 兰德明 - 人大主任
    {"person_id": 17, "org_id": 4, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 高建博 - 政协主席
    {"person_id": 18, "org_id": 5, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────
relationships = [
    # 书记-市长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长（候选人），党政主要领导工作搭档", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    # 书记-副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与副书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    # 书记-各位常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委常委与市委书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委常委与市委书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委常委与市委书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委常委与市委书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "市委常委与市委书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "市委常委与市委书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委常委与市委书记工作关系", "overlap_org": "中共吴忠市委员会", "overlap_period": "current"},
    # 市长候选人-副市长
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长与市长候选人工作关系", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate", "context": "副市长与市长候选人工作关系", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate", "context": "副市长与市长候选人工作关系", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 13, "person_b": 2, "type": "superior_subordinate", "context": "副市长与市长候选人工作关系", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 14, "person_b": 2, "type": "superior_subordinate", "context": "副市长与市长候选人工作关系", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 15, "person_b": 2, "type": "superior_subordinate", "context": "副市长与市长候选人工作关系", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    # 副市长之间
    {"person_a": 6, "person_b": 11, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    {"person_a": 14, "person_b": 15, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "吴忠市人民政府", "overlap_period": "current"},
    # 人大政协领导与书记
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "市委与市人大工作关系", "overlap_org": "吴忠市", "overlap_period": "current"},
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "市委与市政协工作关系", "overlap_org": "吴忠市", "overlap_period": "current"},
]

# ── SQLite ─────────────────────────────────────────────────────────
def create_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '')""")


def insert_data(conn):
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     [p.get(k, "") for k in ["id","name","gender","ethnicity","birth","birthplace",
                                             "education","party_join","work_start","current_post",
                                             "current_org","source"]])
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     [o.get(k, "") for k in ["id","name","type","level","parent","location"]])
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                     [pos.get(k, "") for k in ["person_id","org_id","title","start_date","end_date","rank","note"]])
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                     [r.get(k, "") for k in ["person_a","person_b","type","context","overlap_org","overlap_period"]])
    conn.commit()


# ── GEXF ───────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    if p["id"] == 1:
        return "255,50,50"      # Red for Party Secretary
    elif p["id"] == 2:
        return "50,100,255"     # Blue for Government Leader
    elif p["current_post"].find("纪委书记") >= 0 or p["current_post"].find("监委") >= 0:
        return "255,165,0"      # Orange for Discipline Inspection
    elif p["current_post"].find("人大") >= 0:
        return "200,255,255"    # Cyan for People's Congress
    elif p["current_post"].find("政协") >= 0:
        return "255,240,200"    # Cream for Political Consultative Conference
    elif p["current_post"].find("常委") >= 0:
        return "150,150,255"    # Light blue for Standing Committee members
    else:
        return "100,100,100"    # Grey for others

def person_size(p):
    if p["id"] in (1, 2):
        return "20.0"
    elif p["current_post"].find("常委") >= 0:
        return "14.0"
    else:
        return "12.0"

def org_color(o):
    mapping = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,100",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return mapping.get(o.get("type", ""), "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Government Personnel Network Investigator</creator>')
    lines.append(f'    <description>{SLUG} leadership network (源自吴忠市人民政府官网领导之窗，2026年7月)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="education" type="string"/>')
    lines.append('      <attribute id="4" title="current_post" type="string"/>')
    lines.append('      <attribute id="5" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("ethnicity",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("education",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="5" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Main ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
        create_tables(conn)
        insert_data(conn)
        print(f"Database: {len(persons)} persons, {len(organizations)} orgs, "
              f"{len(positions)} positions, {len(relationships)} relationships")
    finally:
        conn.close()
    build_gexf()
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")
