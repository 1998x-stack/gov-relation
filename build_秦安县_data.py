#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 秦安县 (Qin'an County), 天水市, 甘肃省.

秦安县 — 甘肃省天水市下辖县, 位于天水市北部, 葫芦河下游.
Covers current County Party Secretary (王德全), County Magistrate (张恒刚),
their predecessors, and leadership team.

Current leadership as of 2026-07:
  - 王德全 (县委书记, appointed ~April 2026)
  - 张恒刚 (县长, since ~late 2025/early 2026)

Reference sources:
  - 秦安县人民政府官网领导之窗: https://www.qinan.gov.cn/ldzc1/ldjj.htm
  - 秦安县人民政府新闻中心: https://www.qinan.gov.cn/xwzx/qaxw.htm
  - 天水在线/每日甘肃/中国甘肃网: 人事任免报道
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_秦安县")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "秦安县_network.db")
GEXF_PATH = os.path.join(TMP, "秦安县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS
    # ═══════════════════════════════════════════════════════════

    # 王德全 — 秦安县委书记 (as of 2026.04)
    {"id": 1, "name": "王德全", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委书记",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm; 秦安新闻2026-04-09首次以县委书记身份主持常委会"},

    # 张恒刚 — 秦安县委副书记、县长 (as of 2026.02)
    {"id": 2, "name": "张恒刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委副书记、县长",
     "current_org": "秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm; 秦安新闻2026-02-14以县长身份出席活动"},

    # 张俊义 — 秦安县委副书记（专职）
    {"id": 3, "name": "张俊义", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委副书记（专职）",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 刘云桂 — 县委常委、副县长
    {"id": 4, "name": "刘云桂", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委、副县长",
     "current_org": "中共秦安县委员会/秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 庞胜前 — 县委常委
    {"id": 5, "name": "庞胜前", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 马昊莹 — 县委常委
    {"id": 6, "name": "马昊莹", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 高小强 — 县委常委
    {"id": 7, "name": "高小强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 包振国 — 县委常委、副县长
    {"id": 8, "name": "包振国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委、副县长",
     "current_org": "中共秦安县委员会/秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 夏子文 — 县委常委
    {"id": 9, "name": "夏子文", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 杨涛 — 县委常委、副县长
    {"id": 10, "name": "杨涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委、副县长",
     "current_org": "中共秦安县委员会/秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 党晓军 — 县委常委
    {"id": 11, "name": "党晓军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 陈升 — 县委常委
    {"id": 12, "name": "陈升", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县委常委",
     "current_org": "中共秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # ═══════════════════════════════════════════════════════════
    # PREDECESSORS — 县委书记
    # ═══════════════════════════════════════════════════════════

    # 周济 — 前任秦安县委书记 (~2021-2026.03)
    {"id": 13, "name": "周济", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原秦安县委书记",
     "current_org": "原中共秦安县委员会",
     "source": "秦安新闻2025-04-30; 秦安新闻2026-02-14; 秦安新闻2026-03-03"},

    # 王龙强 — 前任秦安县县长 (~2021-2025)
    {"id": 14, "name": "王龙强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原秦安县委副书记、县长",
     "current_org": "原秦安县人民政府",
     "source": "秦安新闻2025-04-30; 秦安新闻2022-07-12"},

    # ═══════════════════════════════════════════════════════════
    # FOUR MAJOR LEADERSHIP
    # ═══════════════════════════════════════════════════════════

    # 马顺祥 — 县人大常委会主任
    {"id": 15, "name": "马顺祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县人大常委会主任",
     "current_org": "秦安县人民代表大会常务委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 杨喜春 — 县政协主席
    {"id": 16, "name": "杨喜春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县政协主席",
     "current_org": "中国人民政治协商会议秦安县委员会",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # ═══════════════════════════════════════════════════════════
    # OTHER DEPUTIES — 副县长 (not 县委常委)
    # ═══════════════════════════════════════════════════════════

    # 赵智彦 — 副县长
    {"id": 17, "name": "赵智彦", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秦安县副县长",
     "current_org": "秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 蒋露 — 副县长
    {"id": 18, "name": "蒋露", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "秦安县副县长",
     "current_org": "秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 张小军 — 副县长
    {"id": 19, "name": "张小军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "秦安县副县长",
     "current_org": "秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 郑博 — 副县长
    {"id": 20, "name": "郑博", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "秦安县副县长",
     "current_org": "秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 张百年 — 副县长
    {"id": 21, "name": "张百年", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "秦安县副县长",
     "current_org": "秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},

    # 张兴博 — 副县长
    {"id": 22, "name": "张兴博", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "秦安县副县长",
     "current_org": "秦安县人民政府",
     "source": "https://www.qinan.gov.cn/ldzc1/ldjj.htm"},
]

organizations = [
    {"id": 1, "name": "中共秦安县委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市秦安县"},
    {"id": 2, "name": "秦安县人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市秦安县"},
    {"id": 3, "name": "秦安县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "天水市人大常委会", "location": "甘肃省天水市秦安县"},
    {"id": 4, "name": "中国人民政治协商会议秦安县委员会", "type": "政协", "level": "县处级",
     "parent": "天水市政协", "location": "甘肃省天水市秦安县"},
    {"id": 5, "name": "中共天水市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
    {"id": 6, "name": "天水市人民政府", "type": "政府", "level": "地厅级",
     "parent": "甘肃省人民政府", "location": "甘肃省天水市"},
]

positions = [
    # ── 王德全 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "秦安县委书记", "start": "2026-04", "end": "present", "rank": "副厅级",
     "note": "2026年4月任秦安县委书记（首次以县委书记身份主持县委常委会会议）"},

    # ── 张恒刚 (id=2) ──
    {"person_id": 2, "org_id": 2, "title": "秦安县委副书记、县长", "start": "~2025-12", "end": "present", "rank": "正处级",
     "note": "2026年2月以县长身份参加活动，推测2025年底至2026年初接任"},

    # ── 张俊义 (id=3) ──
    {"person_id": 3, "org_id": 1, "title": "秦安县委副书记（专职）", "start": "", "end": "present", "rank": "副处级",
     "note": "专职副书记"},

    # ── 刘云桂 (id=4) ──
    {"person_id": 4, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 4, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "同时任副县长"},

    # ── 庞胜前 (id=5) ──
    {"person_id": 5, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 马昊莹 (id=6) ──
    {"person_id": 6, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 高小强 (id=7) ──
    {"person_id": 7, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 包振国 (id=8) ──
    {"person_id": 8, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 8, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "同时任副县长"},

    # ── 夏子文 (id=9) ──
    {"person_id": 9, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 杨涛 (id=10) ──
    {"person_id": 10, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 10, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "同时任副县长"},

    # ── 党晓军 (id=11) ──
    {"person_id": 11, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 陈升 (id=12) ──
    {"person_id": 12, "org_id": 1, "title": "秦安县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 周济 (id=13) ──
    {"person_id": 13, "org_id": 1, "title": "秦安县委书记", "start": "", "end": "2026-03", "rank": "副厅级",
     "note": "前任县委书记，2026年3月仍在任，4月由王德全接任"},

    # ── 王龙强 (id=14) ──
    {"person_id": 14, "org_id": 2, "title": "秦安县委副书记、县长", "start": "", "end": "2025", "rank": "正处级",
     "note": "前任县长，2025年4月仍在任，后由张恒刚接任"},

    # ── 马顺祥 (id=15) ──
    {"person_id": 15, "org_id": 3, "title": "秦安县人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": ""},

    # ── 杨喜春 (id=16) ──
    {"person_id": 16, "org_id": 4, "title": "秦安县政协主席", "start": "", "end": "present", "rank": "正处级",
     "note": ""},

    # ── 赵智彦 (id=17) ──
    {"person_id": 17, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 蒋露 (id=18) ──
    {"person_id": 18, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 张小军 (id=19) ──
    {"person_id": 19, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 郑博 (id=20) ──
    {"person_id": 20, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 张百年 (id=21) ──
    {"person_id": 21, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 张兴博 (id=22) ──
    {"person_id": 22, "org_id": 2, "title": "秦安县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
]

relationships = [
    # ── Current top leaders ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "王德全作为县委书记, 张恒刚作为县长, 是党政一把手搭档关系",
     "overlap_org": "中共秦安县委员会/秦安县人民政府",
     "overlap_period": "2026-04~present", "confidence": "confirmed"},

    # ── Succession chain: 县委书记 ──
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor", "strength": "strong",
     "context": "王德全接替周济任秦安县委书记",
     "overlap_org": "中共秦安县委员会",
     "overlap_period": "2026-04", "confidence": "confirmed"},

    # ── Succession chain: 县长 ──
    {"person_a": 2, "person_b": 14, "type": "predecessor_successor", "strength": "strong",
     "context": "张恒刚接替王龙强任秦安县县长",
     "overlap_org": "秦安县人民政府",
     "overlap_period": "2025底~2026初", "confidence": "confirmed"},

    # ── Top leaders + Four major leadership ──
    {"person_a": 1, "person_b": 15, "type": "overlap", "strength": "medium",
     "context": "王德全与马顺祥在秦安县党政班子共事",
     "overlap_org": "中共秦安县委员会/秦安县人大常委会",
     "overlap_period": "2026-04~present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 16, "type": "overlap", "strength": "medium",
     "context": "王德全与杨喜春在秦安县党政班子共事",
     "overlap_org": "中共秦安县委员会/秦安县政协",
     "overlap_period": "2026-04~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 15, "type": "overlap", "strength": "medium",
     "context": "张恒刚与马顺祥在秦安县党政班子共事",
     "overlap_org": "秦安县人民政府/秦安县人大常委会",
     "overlap_period": "~2025底~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 16, "type": "overlap", "strength": "medium",
     "context": "张恒刚与杨喜春在秦安县党政班子共事",
     "overlap_org": "秦安县人民政府/秦安县政协",
     "overlap_period": "~2025底~present", "confidence": "confirmed"},

    # ── 县委班子内部关系 ──
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "strength": "strong",
     "context": "王德全作为县委书记, 张俊义作为专职副书记, 是县委班子搭档",
     "overlap_org": "中共秦安县委员会",
     "overlap_period": "2026-04~present", "confidence": "confirmed"},

    # ── 前任搭档关系 ──
    {"person_a": 13, "person_b": 14, "type": "superior_subordinate", "strength": "strong",
     "context": "周济与王龙强为前任党政一把手搭档",
     "overlap_org": "中共秦安县委员会/秦安县人民政府",
     "overlap_period": "~2021~2025", "confidence": "confirmed"},
]


# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role and "副书记" in role:
        return "50,100,255"
    elif "县长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "原" in role:
        return "160,160,160"  # predecessor gray
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role or ("县长" in role and "副书记" in role)


def person_size(p):
    return "20.0" if is_top_leader(p) else ("14.0" if "原" not in p["current_post"] else "10.0")


# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
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
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>秦安县领导班子工作关系网络 - 甘肃省天水市秦安县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
