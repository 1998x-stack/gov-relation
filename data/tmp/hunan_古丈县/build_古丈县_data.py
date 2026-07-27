#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 古丈县 leadership network."""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "古丈县_network.db")
GEXF_PATH = os.path.join(BASE, "古丈县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── 1: 县委书记（现任）──
    {
        "id": 1,
        "name": "陈建新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "湖南省衡东县",
        "education": "省委党校研究生，文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委书记（2026年6月任）",
        "current_org": "中共古丈县委员会",
        "source": "https://hunan.voc.com.cn/news/202606/32862985.html"
    },
    # ── 2: 县委书记（前任）──
    {
        "id": 2,
        "name": "滕朝辉",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1974-10",
        "birthplace": "湖南省古丈县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委原书记（2023.12-2026.06，另有任用）",
        "current_org": "中共古丈县委员会",
        "source": "https://hunan.voc.com.cn/news/202606/32862985.html"
    },
    # ── 3: 县委副书记（彭君，可能任县长）──
    {
        "id": 3,
        "name": "彭君",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委委员、常委、副书记（2026年6月任）",
        "current_org": "中共古丈县委员会",
        "source": "https://hunan.voc.com.cn/news/202606/32862985.html"
    },
    # ── 4: 县委副书记（麻学清）──
    {
        "id": 4,
        "name": "麻学清",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委副书记",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/12259185.html"
    },
    # ── 5: 县人大常委会主任（郑良武，2025年初任职）──
    {
        "id": 5,
        "name": "郑良武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县人大常委会主任",
        "current_org": "古丈县人民代表大会常务委员会",
        "source": "https://m.voc.com.cn/rmt/article/12653380.html"
    },
    # ── 6: 县人大常委会原主任（曾传文）──
    {
        "id": 6,
        "name": "曾传文",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1965-05",
        "birthplace": "湖南省古丈县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县人大常委会原主任（2016.11-2024）",
        "current_org": "古丈县人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/zh-hans/%E5%8F%A4%E4%B8%88%E5%8E%BF"
    },
    # ── 7: 县政协主席（宋祖林）──
    {
        "id": 7,
        "name": "宋祖林",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1975-05",
        "birthplace": "湖南省古丈县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县政协主席",
        "current_org": "中国人民政治协商会议古丈县委员会",
        "source": "https://zh.wikipedia.org/zh-hans/%E5%8F%A4%E4%B8%88%E5%8E%BF"
    },
    # ── 8: 县委常委、宣传部部长（粟丽波）──
    {
        "id": 8,
        "name": "粟丽波",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委、宣传部部长",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/10270850.html"
    },
    # ── 9: 县委常委、组织部部长（聂仁军）──
    {
        "id": 9,
        "name": "聂仁军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委、组织部部长",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/10270850.html"
    },
    # ── 10: 县委常委、县委统战部部长（向上）──
    {
        "id": 10,
        "name": "向上",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委、统战部部长",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/10270850.html"
    },
    # ── 11: 县委常委（彭波）──
    {
        "id": 11,
        "name": "彭波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/12728435.html"
    },
    # ── 12: 县委常委、县委办主任（刘学书）──
    {
        "id": 12,
        "name": "刘学书",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委、县委办主任",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/12828705.html"
    },
    # ── 13: 县委常委（陈雷）──
    {
        "id": 13,
        "name": "陈雷",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委",
        "current_org": "中共古丈县委员会",
        "source": "https://m-xhncloud.voc.com.cn/portal/news/show?id=12728435"
    },
    # ── 14: 县委常委（郜晓丽）──
    {
        "id": 14,
        "name": "郜晓丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委",
        "current_org": "中共古丈县委员会",
        "source": "https://m-xhncloud.voc.com.cn/portal/news/show?id=12728435"
    },
    # ── 15: 县委常委（周大钊）──
    {
        "id": 15,
        "name": "周大钊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/12828705.html"
    },
    # ── 16: 县委常委、县纪委书记（尚高）──
    {
        "id": 16,
        "name": "尚高",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委、县纪委书记",
        "current_org": "中共古丈县纪律检查委员会",
        "source": "https://m.voc.com.cn/rmt/article/15281670.html"
    },
    # ── 17: 县委常委（王申强）──
    {
        "id": 17,
        "name": "王申强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/15281670.html"
    },
    # ── 18: 县委常委（文少亮）──
    {
        "id": 18,
        "name": "文少亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县委常委",
        "current_org": "中共古丈县委员会",
        "source": "https://m.voc.com.cn/rmt/article/15281670.html"
    },
    # ── 19: 前任县长（陈瑞，2021.5-2024.7）──
    {
        "id": 19,
        "name": "陈瑞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县原县长（2021.5-2024.7）",
        "current_org": "古丈县人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E4%B8%88%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C"
    },
    # ── 20: 前任县长（邓晓东，2013.4-2021.5）──
    {
        "id": 20,
        "name": "邓晓东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "古丈县原县长（2013.4-2021.5）",
        "current_org": "古丈县人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E4%B8%88%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C"
    },
    # ── 21: 前任县委书记：毛家（凤凰）-- pattern for predecessor check ──
    # Note: 滕朝辉的前任是 who before 2023.12? Need more research.
]

organizations = [
    {
        "id": 1,
        "name": "中共古丈县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共湘西土家族苗族自治州委员会",
        "location": "湖南省湘西州古丈县"
    },
    {
        "id": 2,
        "name": "古丈县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "湘西土家族苗族自治州人民政府",
        "location": "湖南省湘西州古丈县古阳路32号"
    },
    {
        "id": 3,
        "name": "古丈县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "",
        "location": "湖南省湘西州古丈县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议古丈县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "",
        "location": "湖南省湘西州古丈县"
    },
    {
        "id": 5,
        "name": "中共古丈县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共湘西土家族苗族自治州纪律检查委员会",
        "location": "湖南省湘西州古丈县"
    },
    {
        "id": 6,
        "name": "中共古丈县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共古丈县委员会",
        "location": "湖南省湘西州古丈县"
    },
    {
        "id": 7,
        "name": "中共古丈县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共古丈县委员会",
        "location": "湖南省湘西州古丈县"
    },
    {
        "id": 8,
        "name": "中共古丈县委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共古丈县委员会",
        "location": "湖南省湘西州古丈县"
    },
    {
        "id": 9,
        "name": "中共古丈县委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共古丈县委员会",
        "location": "湖南省湘西州古丈县"
    },
]

positions = [
    # 陈建新 - 县委书记（2026.6至今）
    {"person_id": 1, "org_id": 1, "title": "古丈县委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026年6月9日省委决定任命"},
    # 陈建新 - 古丈县长（2024.7-2026.6）
    {"person_id": 1, "org_id": 2, "title": "古丈县长", "start_date": "2024-07", "end_date": "2026-06", "rank": "正处级", "note": ""},
    # 滕朝辉 - 古丈县委书记（2023.12-2026.6）
    {"person_id": 2, "org_id": 1, "title": "古丈县委书记", "start_date": "2023-12", "end_date": "2026-06", "rank": "正处级", "note": "另有任用"},
    # 彭君 - 县委副书记（2026.6至今）
    {"person_id": 3, "org_id": 1, "title": "古丈县委副书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级/副处级", "note": "可能兼任县长"},
    # 麻学清 - 县委副书记
    {"person_id": 4, "org_id": 1, "title": "古丈县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "任职时间待确认"},
    # 郑良武 - 县人大常委会主任
    {"person_id": 5, "org_id": 3, "title": "古丈县人大常委会主任", "start_date": "2025-01", "end_date": "present", "rank": "正处级", "note": ""},
    # 曾传文 - 县人大常委会原主任
    {"person_id": 6, "org_id": 3, "title": "古丈县人大常委会主任", "start_date": "2016-11", "end_date": "2024", "rank": "正处级", "note": ""},
    # 宋祖林 - 县政协主席
    {"person_id": 7, "org_id": 4, "title": "古丈县政协主席", "start_date": "2021-10", "end_date": "present", "rank": "正处级", "note": ""},
    # 粟丽波 - 县委常委、宣传部部长
    {"person_id": 8, "org_id": 6, "title": "古丈县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 聂仁军 - 县委常委、组织部部长
    {"person_id": 9, "org_id": 7, "title": "古丈县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 向上 - 县委常委、统战部部长
    {"person_id": 10, "org_id": 8, "title": "古丈县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 彭波 - 县委常委
    {"person_id": 11, "org_id": 1, "title": "古丈县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘学书 - 县委常委、县委办主任
    {"person_id": 12, "org_id": 9, "title": "古丈县委常委、县委办主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈雷 - 县委常委
    {"person_id": 13, "org_id": 1, "title": "古丈县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 郜晓丽 - 县委常委
    {"person_id": 14, "org_id": 1, "title": "古丈县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 周大钊 - 县委常委
    {"person_id": 15, "org_id": 1, "title": "古丈县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 尚高 - 县委常委、纪委书记
    {"person_id": 16, "org_id": 5, "title": "古丈县委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王申强 - 县委常委
    {"person_id": 17, "org_id": 1, "title": "古丈县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 文少亮 - 县委常委
    {"person_id": 18, "org_id": 1, "title": "古丈县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈瑞 - 原县长
    {"person_id": 19, "org_id": 2, "title": "古丈县长", "start_date": "2021-05", "end_date": "2024-07", "rank": "正处级", "note": ""},
    # 邓晓东 - 原县长
    {"person_id": 20, "org_id": 2, "title": "古丈县长", "start_date": "2013-04", "end_date": "2021-05", "rank": "正处级", "note": ""},
]

relationships = [
    # 陈建新 → 滕朝辉（前后任县委书记）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "陈建新接替滕朝辉任古丈县委书记（2026年6月）", "overlap_org": "中共古丈县委员会", "overlap_period": "2024.07-2026.06"},
    # 陈建新 → 彭君（党政搭档关系）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委班子同事（2026年6月起）", "overlap_org": "中共古丈县委员会", "overlap_period": "2026.06-present"},
    # 陈建新 → 麻学清（县委班子同事）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委班子同事", "overlap_org": "中共古丈县委员会", "overlap_period": ""},
    # 陈建新 → 郑良武（县委/人大同事）
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "党政班子同事", "overlap_org": "古丈县", "overlap_period": "2025-present"},
    # 陈建新 → 宋祖林（县委/政协同事）
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县四套班子同事", "overlap_org": "古丈县", "overlap_period": "2024.07-present"},
    # 陈建新 → 陈瑞（前后任县长）
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "陈建新接替陈瑞任古丈县长", "overlap_org": "古丈县人民政府", "overlap_period": "2024.07"},
    # 滕朝辉 → 麻学清（县委班子同事）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "时任书记与副书记", "overlap_org": "中共古丈县委员会", "overlap_period": ""},
    # 滕朝辉 → 粟丽波（宣传部长）
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "时任书记与宣传部长", "overlap_org": "中共古丈县委员会", "overlap_period": ""},
    # 滕朝辉 → 聂仁军（组织部长）
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "时任书记与组织部长", "overlap_org": "中共古丈县委员会", "overlap_period": ""},
    # 郑良武 → 曾传文（前后任人大主任）
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "郑良武接替曾传文任县人大常委会主任", "overlap_org": "古丈县人民代表大会常务委员会", "overlap_period": "2025"},
    # 陈建新 → 陈瑞（前任县长）
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "接任古丈县长", "overlap_org": "古丈县人民政府", "overlap_period": ""},
    # 陈瑞 → 邓晓东（前后任县长）
    {"person_a": 19, "person_b": 20, "type": "predecessor_successor", "context": "接任邓晓东任古丈县长", "overlap_org": "古丈县人民政府", "overlap_period": ""},
]


# ── BUILD ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' color string based on role."""
    post = p.get("current_post", "")
    name = p.get("name", "")
    # Party Secretary (县委书记) - Red
    if "书记" in post and "县委" in post and "纪委" not in post and "宣传" not in post and "组织" not in post and "统战" not in post and "办主任" not in post:
        if name in ("陈建新", "滕朝辉"):
            return "255,50,50"
    # County Mayor/县长 - Blue
    if "县长" in post:
        return "50,100,255"
    # Discipline Inspection - Orange
    if "纪委" in post:
        return "255,165,0"
    # Congress/Political Consultative - Dark green
    if "人大" in post or "政协" in post:
        return "0,150,0"
    # Others - Grey
    return "100,100,100"


def org_color(o):
    """Return 'r,g,b' color for organization type."""
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
    name = p.get("name", "")
    return name in ("陈建新", "滕朝辉")


def build_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop existing tables
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    # Create tables
    cur.execute("""
        CREATE TABLE persons (
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
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT ''
        )
    """)

    # Insert data
    for p in persons:
        cur.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  Database created: {DB_PATH}")
    print(f"    Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")


def build_gexf():
    lines = []
    today = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>古丈县 Leadership Network — 书记/县长/县委常委/人大/政协</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
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
        sz = "20.0" if is_top_leader(p) else ("15.0" if p["id"] in (3, 4, 5, 6, 7) else "12.0")
        role = p.get("current_post", "")
        org = p.get("current_org", "")
        src = p.get("source", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(src)}"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person → Organization (worked at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos["title"]
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person → Person (relationships)
    for r in relationships:
        pa = r["person_a"]
        pb = r["person_b"]
        ctx = r.get("context", "")
        rtype = r.get("type", "")
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF created: {GEXF_PATH}")


if __name__ == "__main__":
    print("Building 古丈县 network data...")
    build_database()
    build_gexf()
    print("Done.")
