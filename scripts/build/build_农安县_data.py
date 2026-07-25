#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 农安县 (Nong'an County), 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_农安县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - nongan.gov.cn (农安县人民政府官网) — 政府领导 page (confirmed as-of 2026-07-25)
    - 李冠辉 (县长): confirmed via official leadership page
    - 冯玮, 彪兵, 陈娅, 王海辉, 姜玉权, 朱培源, 张春龙 (副县长): confirmed
    - 郑庆明 (开发区书记/主任): confirmed
    - 王昭, 王大宇 (挂职副县长): confirmed
  - nongan.gov.cn news articles — 白松巍 (县委书记): confirmed via multiple official news items
    - 白松巍: 县委书记, confirmed July 2026 articles (1970s?)
    - 任利峰: 县委副书记, confirmed via flood control meeting July 2026
    - 冯玮: 县委常委、常务副县长, confirmed July 2026
    - 彪兵: 县委常委、副县长, confirmed July 2026
    - 单大维: 县委常委、组织部部长, confirmed July 23, 2026
  - nongan.gov.cn 人大常委会公告 (July 16, 2026) — personnel changes confirmed
    - 周德库: 人大常委会主任
    - 张淑梅, 李忠勇: 人大常委会副主任
    - 徐志刚: 人大常委会党组副书记
    - 裴杉: 人大常委会党组成员
    - 李宾: 新任监察委员会代理主任 (原主任崔可锋辞职)
    - 张春龙: 新任副县长 (July 16, 2026)

Confidence notes:
  - 白松巍 (县委书记): confirmed via official news (multiple articles July 2026); detailed career history unverified
  - 李冠辉 (县长): confirmed via official government leadership page; detailed career history unverified
  - 任利峰 (县委副书记): confirmed via official news (July 2026)
  - Party committee leadership roster names confirmed but detailed biographies unavailable
  - All current posts confirmed as of July 2026
  - Predecessor/successor relationships: documented where known
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "农安县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "build_农安县_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "白松巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共农安县委员会",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260708_3499166.html"
    },
    {
        "id": 2,
        "name": "李冠辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    # ═══════ County Party Committee ═══════
    {
        "id": 3,
        "name": "任利峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共农安县委员会",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260713_3500217.html"
    },
    {
        "id": 4,
        "name": "冯玮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    {
        "id": 5,
        "name": "彪兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    {
        "id": 6,
        "name": "单大维",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共农安县委员会组织部",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260723_3502403.html"
    },
    # ═══════ Deputy County Mayors ═══════
    {
        "id": 7,
        "name": "陈娅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    {
        "id": 8,
        "name": "王海辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    {
        "id": 9,
        "name": "姜玉权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    {
        "id": 10,
        "name": "朱培源",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    {
        "id": 11,
        "name": "张春龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    # ═══════开发区 ═══════
    {
        "id": 12,
        "name": "郑庆明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共长春农安经济开发区工作委员会书记、管委会主任",
        "current_org": "长春农安经济开发区",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    # ═══════ 挂职副县长 ═══════
    {
        "id": 13,
        "name": "王昭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    {
        "id": 14,
        "name": "王大宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "农安县人民政府",
        "source": "http://www.nongan.gov.cn/zw/zfld/"
    },
    # ═══════ 人大领导 ═══════
    {
        "id": 15,
        "name": "周德库",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "农安县人大常委会",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html"
    },
    {
        "id": 16,
        "name": "张淑梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "农安县人大常委会",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html"
    },
    {
        "id": 17,
        "name": "李忠勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "农安县人大常委会",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html"
    },
    # ═══════ 监察委 ═══════
    {
        "id": 18,
        "name": "李宾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县监察委员会代理主任",
        "current_org": "农安县监察委员会",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html"
    },
    # ═══════ 前任领导（用于关系图谱）═══════
    {
        "id": 19,
        "name": "崔可锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已辞去县监委主任",
        "current_org": "",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html"
    },
    {
        "id": 20,
        "name": "蔡佳锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已免去副县长",
        "current_org": "",
        "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
orgs = [
    {"id": 1, "name": "中共农安县委员会", "type": "党委"},
    {"id": 2, "name": "农安县人民政府", "type": "政府"},
    {"id": 3, "name": "中共农安县委员会组织部", "type": "党委"},
    {"id": 4, "name": "农安县人大常委会", "type": "人大"},
    {"id": 5, "name": "农安县监察委员会", "type": "党委"},
    {"id": 6, "name": "长春农安经济开发区", "type": "开发区"},
    {"id": 7, "name": "政协农安县委员会", "type": "政协"},
    {"id": 8, "name": "中共农安县纪律检查委员会", "type": "党委"},
    {"id": 9, "name": "中共长春市委", "type": "党委"},
    {"id": 10, "name": "长春市人民政府", "type": "政府"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 白松巍相关
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260708_3499166.html",
     "confidence": "confirmed"},
    # 李冠辉相关
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    # 任利峰
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260713_3500217.html",
     "confidence": "confirmed"},
    # 冯玮
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    # 彪兵
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    # 单大维
    {"person_id": 6, "org_id": 3, "title": "县委常委、组织部部长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260723_3502403.html",
     "confidence": "confirmed"},
    # 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "2026-07-16", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    # 郑庆明
    {"person_id": 12, "org_id": 6, "title": "开发区党工委书记、管委会主任", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    # 挂职副县长
    {"person_id": 13, "org_id": 2, "title": "副县长（挂职）", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person_id": 14, "org_id": 2, "title": "副县长（挂职）", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    # 人大
    {"person_id": 15, "org_id": 4, "title": "县人大常委会主任", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    {"person_id": 16, "org_id": 4, "title": "县人大常委会副主任", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    {"person_id": 17, "org_id": 4, "title": "县人大常委会副主任", "start": "未知", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    # 监察委
    {"person_id": 18, "org_id": 5, "title": "县监察委员会代理主任", "start": "2026-07-16", "end": "至今",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    # 前任
    {"person_id": 19, "org_id": 5, "title": "县监察委员会主任（已辞）", "start": "未知", "end": "2026-07-16",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    {"person_id": 20, "org_id": 2, "title": "副县长（已免）", "start": "未知", "end": "2026-07-16",
     "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 白松巍——李冠辉：党政搭档
    {"person1_id": 1, "person2_id": 2, "type": "党政搭档",
     "strength": "strong", "org": "中共农安县委员会/农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260723_3502403.html",
     "confidence": "confirmed"},
    # 白松巍——任利峰：上下级（书记-副书记）
    {"person1_id": 1, "person2_id": 3, "type": "上下级",
     "strength": "strong", "org": "中共农安县委员会",
     "period": "至今", "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260713_3500217.html",
     "confidence": "confirmed"},
    # 白松巍——冯玮：上下级
    {"person1_id": 1, "person2_id": 4, "type": "上下级",
     "strength": "strong", "org": "中共农安县委员会",
     "period": "至今", "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260708_3499166.html",
     "confidence": "confirmed"},
    # 白松巍——单大维：上下级
    {"person1_id": 1, "person2_id": 6, "type": "上下级",
     "strength": "strong", "org": "中共农安县委员会",
     "period": "至今", "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260723_3502403.html",
     "confidence": "confirmed"},
    # 李冠辉——冯玮：上下级（县长-常务副县长）
    {"person1_id": 2, "person2_id": 4, "type": "上下级",
     "strength": "strong", "org": "农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    # 李冠辉——所有副县长：上下级
    {"person1_id": 2, "person2_id": 5, "type": "上下级",
     "strength": "strong", "org": "农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person1_id": 2, "person2_id": 7, "type": "上下级",
     "strength": "strong", "org": "农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person1_id": 2, "person2_id": 8, "type": "上下级",
     "strength": "strong", "org": "农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person1_id": 2, "person2_id": 9, "type": "上下级",
     "strength": "strong", "org": "农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person1_id": 2, "person2_id": 10, "type": "上下级",
     "strength": "strong", "org": "农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/zw/zfld/",
     "confidence": "confirmed"},
    {"person1_id": 2, "person2_id": 11, "type": "上下级",
     "strength": "strong", "org": "农安县人民政府",
     "period": "2026-07-16至今", "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    # 崔可锋→李宾：前任-继任（监委主任）
    {"person1_id": 19, "person2_id": 18, "type": "前任_继任",
     "strength": "strong", "org": "农安县监察委员会",
     "period": "2026-07-16交接", "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260716_3501086.html",
     "confidence": "confirmed"},
    # 任利峰——彪兵：工作搭档（共同防汛）
    {"person1_id": 3, "person2_id": 5, "type": "工作搭档",
     "strength": "strong", "org": "农安县人民政府",
     "period": "至今", "source": "http://www.nongan.gov.cn/dtxx/zwdt/202607/t20260717_3501205.html",
     "confidence": "confirmed"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string for a person based on their role."""
    title = p.get("current_post", "")
    if "书记" in title and "县委" in title:
        return "255,50,50"
    elif "县长" in title or "副县长" in title:
        return "50,100,255"
    elif "纪委" in title or "监察" in title:
        return "255,165,0"
    else:
        return "100,100,100"


def is_top_leader(p):
    """Return True if this person is the party secretary or county mayor."""
    title = p.get("current_post", "")
    return "县委书记" in title or "县长" in title


def org_color(o):
    """Return 'r,g,b' string for an organization based on its type."""
    ot = o.get("type", "")
    if "党委" in ot:
        return "255,200,200"
    elif "政府" in ot:
        return "200,200,255"
    elif "开发区" in ot:
        return "200,255,200"
    elif "人大" in ot:
        return "200,255,255"
    elif "政协" in ot:
        return "255,240,200"
    else:
        return "200,200,200"


# ── Build GEXF ─────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>农安县（Nong\'an County, 吉林省长春市）领导团队与组织关系网络图谱。调查日期：{AS_OF}</description>')
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
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in orgs:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("confidence", "plausible"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationships), weight="2.0"
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person1_id"]}" target="p{rel["person2_id"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("confidence", "plausible"))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ── Build SQLite ───────────────────────────────────────────────────────────
def build_db():
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT DEFAULT '',
            end TEXT DEFAULT '',
            source TEXT DEFAULT '',
            confidence TEXT DEFAULT 'plausible',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            person1_id INTEGER,
            person2_id INTEGER,
            type TEXT,
            strength TEXT DEFAULT 'medium',
            org TEXT DEFAULT '',
            period TEXT DEFAULT '',
            source TEXT DEFAULT '',
            confidence TEXT DEFAULT 'plausible',
            FOREIGN KEY (person1_id) REFERENCES persons(id),
            FOREIGN KEY (person2_id) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in orgs:
        c.execute("INSERT OR REPLACE INTO organizations (id, name, type) VALUES (?,?,?)",
                  (o["id"], o["name"], o.get("type", "")))

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (person_id, org_id, title, start, end, source, confidence)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("source", ""), pos.get("confidence", "plausible")))

    for rel in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (person1_id, person2_id, type, strength, org, period, source, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person1_id"], rel["person2_id"], rel["type"],
             rel.get("strength", "medium"), rel.get("org", ""),
             rel.get("period", ""), rel.get("source", ""),
             rel.get("confidence", "plausible")))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH}")


# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    build_db()
    build_gexf()
    print("Done.")
