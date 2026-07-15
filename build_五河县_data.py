#!/usr/bin/env python3
"""Build Wuhe County (五河县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.wuhe.gov.cn (official Wuhe government website, news articles July 2026)
  - www.wuhe.gov.cn/bdgk/ldzc2/index.html (leadership window)
  - 县委常委会（扩大）会议 (2026-07-11) - https://www.wuhe.gov.cn/xwzx/bdyw/81379779.html
  - 县委农村工作领导小组会议 (2026-07-11) - https://www.wuhe.gov.cn/xwzx/bdyw/81379776.html
  - 徐立民主持召开县政府常务会议 (2026-07-06) - https://www.wuhe.gov.cn/xwzx/bdyw/81379485.html
  - 全县"两优一先"表彰大会暨"七一"党课报告会 (2026-07-02) - https://www.wuhe.gov.cn/xwzx/bdyw/81379373.html
  - 十五届县委委员、候补委员开展"七一"党性教育活动 (2026-07-02) - https://www.wuhe.gov.cn/xwzx/bdyw/81379372.html
  - 中国共产党五河县第十五届纪律检查委员会第一次全体会议 (2026-06-26) - https://www.wuhe.gov.cn/xwzx/bdyw/81379029.html

Confidence: Current roles confirmed from official Wuhe government news (July 2026).
  Biographical details (birth years, education) from leadership profiles on wuhe.gov.cn.
  Full career timelines before current roles are partial.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "五河县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "五河县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "郑冬冬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共五河县委",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379779.html",
        "notes": "2026年7月主持县委常委会（扩大）会议。十五届县委委员。具体履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "徐立民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "native_place": "",
        "education": "管理学学士",
        "party_join": "",
        "work_start": "2004年8月",
        "current_post": "县委副书记、县长",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=21731051",
        "notes": "1980年12月出生，汉族，管理学学士，2004年8月参加工作，中共党员。领导县政府全面工作。",
        "confidence": "confirmed"
    },
    # ── Other Key Leaders from News ──
    {
        "id": 3,
        "name": "陶振银",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测县人大主任或政协主席）",
        "current_org": "五河县",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379373.html",
        "notes": "在全县'两优一先'表彰大会、县委常委会（扩大）会议及'七一'党性教育活动中与郑冬冬并列出席。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": 4,
        "name": "丁云红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测县政协主席或人大主任）",
        "current_org": "五河县",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379373.html",
        "notes": "在全县'两优一先'表彰大会、县委常委会（扩大）会议及'七一'党性教育活动中与郑冬冬并列出席。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": 5,
        "name": "李陈军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测县委副书记或常务副县长）",
        "current_org": "中共五河县委",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379779.html",
        "notes": "出席县委常委会（扩大）会议和县委农村工作领导小组会议。具体职务待确认。",
        "confidence": "plausible"
    },
    # ── County Government Leaders (政府领导) ──
    {
        "id": 6,
        "name": "陈林",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1986年9月",
        "birthplace": "",
        "native_place": "",
        "education": "理学学士",
        "party_join": "",
        "work_start": "2009年8月",
        "current_post": "县委常委、副县长",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=21731101",
        "notes": "1986年9月出生，回族，理学学士，2009年8月参加工作，中共党员。分管发改、财政、应急、统计、五投集团等。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "朱儒林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1998年9月",
        "current_post": "县委常委、副县长",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=21731061",
        "notes": "1980年7月出生，汉族，大学学历，1998年9月参加工作，中共党员。分管科技、工信、商务、数据资源、招商引资、经开区等。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "杨同波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年2月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "2002年12月",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=21731041",
        "notes": "1984年2月出生，汉族，大学学历，2002年12月参加工作，中共党员。挂职副县长，分管文旅、融媒体等。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "王学美",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "2003年12月",
        "current_post": "副县长",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=43462264",
        "notes": "1976年11月出生，汉族，大学学历，2003年12月参加工作，中共党员。分管农业农村、市场监管、供销等。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "陈晓宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1993年8月",
        "current_post": "副县长",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=21731071",
        "notes": "1973年10月出生，汉族，大学学历，1993年8月参加工作，中共党员。分管民政、人社、卫健、退役军人、医保等。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "苏永松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年5月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "2001年2月",
        "current_post": "副县长",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=43462296",
        "notes": "1983年5月出生，汉族，省委党校研究生学历，2001年2月参加工作，中共党员。分管教育、自然资源、生态环境、交通、沱湖保护等。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "邹振飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年12月",
        "birthplace": "",
        "native_place": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "2011年8月",
        "current_post": "副县长",
        "current_org": "五河县人民政府",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=43462241",
        "notes": "1986年12月出生，汉族，硕士研究生学历，2011年8月参加工作，中共党员。分管住建、城管、水利、重点工程、招商引资协助等。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "何福勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1994年12月",
        "current_post": "副县长、公安局局长",
        "current_org": "五河县公安局",
        "source": "https://www.wuhe.gov.cn/content/column/30604291?liId=21731091",
        "notes": "1976年3月出生，汉族，大学学历，1994年12月参加工作，中共党员。分管公安、司法、信访等。",
        "confidence": "confirmed"
    },
    # ── Discipline Inspection Commission ──
    {
        "id": 14,
        "name": "吴昊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共五河县纪律检查委员会",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379029.html",
        "notes": "2026年6月25日当选为五河县第十五届纪委书记。同时出席县委农村工作领导小组会议。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "朱杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县纪委副书记",
        "current_org": "中共五河县纪律检查委员会",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379029.html",
        "notes": "2026年6月25日当选为县纪委副书记。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "孙远峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县纪委副书记",
        "current_org": "中共五河县纪律检查委员会",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379029.html",
        "notes": "2026年6月25日当选为县纪委副书记。",
        "confidence": "confirmed"
    },
    # ── County Leaders from Rural Work Meeting ──
    {
        "id": 17,
        "name": "宋祖清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "五河县",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379776.html",
        "notes": "出席县委农村工作领导小组会议。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": 18,
        "name": "张晨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "五河县",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379776.html",
        "notes": "出席县委农村工作领导小组会议。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": 19,
        "name": "赵入德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "五河县",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379776.html",
        "notes": "出席县委农村工作领导小组会议。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": 20,
        "name": "孟波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "五河县",
        "source": "https://www.wuhe.gov.cn/xwzx/bdyw/81379776.html",
        "notes": "出席县委农村工作领导小组会议。具体职务待确认。",
        "confidence": "plausible"
    },
]

organizations = [
    {"id": 1, "name": "中共五河县委", "type": "党委", "level": "县处级", "parent": "中共蚌埠市委", "location": "安徽省蚌埠市五河县"},
    {"id": 2, "name": "五河县人民政府", "type": "政府", "level": "县处级", "parent": "蚌埠市人民政府", "location": "安徽省蚌埠市五河县"},
    {"id": 3, "name": "中共五河县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共五河县委", "location": "安徽省蚌埠市五河县"},
    {"id": 4, "name": "五河县公安局", "type": "政府", "level": "乡科级", "parent": "五河县人民政府", "location": "安徽省蚌埠市五河县"},
    {"id": 5, "name": "五河县人大常委会", "type": "人大", "level": "县处级", "parent": "五河县", "location": "安徽省蚌埠市五河县"},
    {"id": 6, "name": "政协五河县委员会", "type": "政协", "level": "县处级", "parent": "五河县", "location": "安徽省蚌埠市五河县"},
]

positions = [
    # 郑冬冬
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 徐立民
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "领导县政府全面工作"},
    # 陶振银
    {"person_id": 3, "org_id": 5, "title": "推测县人大主任或副主任", "start": "", "end": "present", "rank": "", "note": "与郑冬冬在多个活动中并列出席"},
    # 丁云红
    {"person_id": 4, "org_id": 6, "title": "推测县政协主席或副主席", "start": "", "end": "present", "rank": "", "note": "与郑冬冬在多个活动中并列出席"},
    # 李陈军
    {"person_id": 5, "org_id": 1, "title": "县领导（推测县委副书记）", "start": "", "end": "present", "rank": "", "note": ""},
    # 陈林
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管发改、财政、应急、统计、五投集团等"},
    # 朱儒林
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管科技、工信、商务、数据资源、招商引资、经开区等"},
    # 杨同波
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 8, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "分管文旅、融媒体等"},
    # 王学美
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管农业农村、市场监管、供销等"},
    # 陈晓宏
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管民政、人社、卫健、退役军人、医保等"},
    # 苏永松
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管教育、自然资源、生态环境、交通、沱湖保护等"},
    # 邹振飞
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管住建、城管、水利、重点工程等"},
    # 何福勇
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "公安局局长", "start": "", "end": "present", "rank": "乡科级", "note": "分管公安、司法、信访等"},
    # 吴昊
    {"person_id": 14, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "县纪委书记", "start": "2026-06", "end": "present", "rank": "副县级", "note": "2026年6月25日当选"},
    # 朱杰
    {"person_id": 15, "org_id": 3, "title": "县纪委副书记", "start": "2026-06", "end": "present", "rank": "乡科级", "note": "2026年6月25日当选"},
    # 孙远峰
    {"person_id": 16, "org_id": 3, "title": "县纪委副书记", "start": "2026-06", "end": "present", "rank": "乡科级", "note": "2026年6月25日当选"},
]

relationships = [
    # 郑冬冬 <-> 徐立民 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共五河县委", "overlap_period": "2026-"},
    # 郑冬冬 <-> 吴昊 (县委领导与纪委书记)
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共五河县委", "overlap_period": "2026-"},
    # 郑冬冬 <-> 陈林
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共五河县委", "overlap_period": "2026-"},
    # 郑冬冬 <-> 朱儒林
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共五河县委", "overlap_period": "2026-"},
    # 徐立民 <-> 陈林 (县长与常务副县长)
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "五河县人民政府", "overlap_period": "2026-"},
    # 徐立民 <-> 朱儒林
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "五河县人民政府", "overlap_period": "2026-"},
]


# ── helpers ──────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string for a person node by role."""
    post = p.get("current_post", "")
    if "县委书记" in post or "书记" in post and "纪委" not in post:
        return "255,50,50"  # Red — Party Secretary
    if "县长" in post or "副市长" in post or "区长" in post:
        return "50,100,255"  # Blue — Mayor
    if "纪委书记" in post or "纪委" in post:
        return "255,165,0"  # Orange — Discipline
    return "100,100,100"  # Grey — Others


def org_color(o):
    """Return 'r,g,b' string for an organization node by type."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or "县长" in post


# ── build database ───────────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons(id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""), p.get("birthplace",""), p.get("native_place",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""), p["current_post"], p["current_org"], p["source"], p.get("notes",""), p.get("confidence","confirmed")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations(id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent",""), o.get("location","")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions(person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── build gexf ───────────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>五河县领导关系网络 - Party and government leadership network for Wuhe County, Bengbu, Anhui. Research date: 2026-07-15.</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="person"/>')
        lines.append(f'          <attvalue for="4" value="{p.get("confidence","confirmed")}"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# ── main ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
