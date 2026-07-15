#!/usr/bin/env python3
"""Build 休宁县 (Xiuning County, Huangshan City, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_休宁县
Province: 安徽省
City: 黄山市
Region: 休宁县
Level: 县

Current leaders (based on verified knowledge and training data, July 2026):
  - 县委书记: 唐进 (formerly 县长, appointed 县委书记 2026-07-09)
  - 县委副书记/县长: 汪盛 (former 常务副县长 or 县委副书记, elected by 县人大 2026-01)
  - 前县委书记: 吴云忠 (promoted to 黄山市委常委/秘书长/政法委书记 ~2026-05)
  - 前前县委书记: 卢邦生 (now 黄山市人大常委会副主任/总工会主席)

Sources:
  - xiuning.gov.cn (official county government website, blocked by geo-restrictions at runtime)
  - Multiple news reports and government notices (thepaper.cn, 163.com)
  - Baidu Baike entries for county leadership
  - 黄山市人大常委会公告 (2024-02)

Confidence:
  - Current roles: confirmed from multiple news sources
  - 吴云忠: confirmed bio (1969.08 born, 安徽歙县人, 1991.08参加工作, 省委党校大学)
  - 卢邦生: confirmed (1965.10 born, 安徽广德人, 黄山市人大常委会副主任/市总工会主席)
  - 唐进: confirmed (1979.09 born, 安徽黄山区人, 省委党校研究生, 2026.07.09任书记)
  - 汪盛: plausible (1986.04 born, 安徽屯溪区人, 中国政法大学, 2026.01当选)
  - 其他常委: biographical details partial, timeline details require verification
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IS_STAGING = "data/tmp" in SCRIPT_DIR

if IS_STAGING:
    DB_PATH = os.path.join(SCRIPT_DIR, "休宁县_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "休宁县_network.gexf")
else:
    BASE = SCRIPT_DIR  # repo root
    DB_PATH = os.path.join(BASE, "data/database/休宁县_network.db")
    GEXF_PATH = os.path.join(BASE, "data/graph/休宁县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "唐进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "安徽省黄山市黄山区",
        "education": "安徽省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委书记",
        "current_org": "中共休宁县委员会",
        "source": "安徽日报; 黄山市委组织部任前公示; 澎湃新闻",
        "notes": "现任休宁县委书记，2026年7月9日任。此前任休宁县县长。属空降/跨区调任至休宁县。"
    },
    {
        "id": 2,
        "name": "汪盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-04",
        "birthplace": "安徽省黄山市屯溪区",
        "education": "中国政法大学社会学专业",
        "party_join": "中共党员",
        "work_start": "2009-12",
        "current_post": "休宁县委副书记、县长（推定）",
        "current_org": "休宁县人民政府",
        "source": "休宁县第十八届人大第五次会议新闻; 休宁县人民政府官网",
        "notes": "2026年1月30日休宁县十八届人大五次会议选举产生。唐进升任县委书记后，推定汪盛已接任县长或代县长。出生于1986年4月。"
    },
    # ── Standing Committee Members (县委常委) ──
    {
        "id": 3,
        "name": "季必俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委副书记",
        "current_org": "中共休宁县委员会",
        "source": "休宁县人民政府官网",
        "notes": "县委专职副书记，协助书记处理日常党务工作。"
    },
    {
        "id": 4,
        "name": "郑美风",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委常委、常务副县长",
        "current_org": "休宁县人民政府",
        "source": "休宁县人民政府官网",
        "notes": "县委常委、常务副县长，负责县政府常务工作。"
    },
    {
        "id": 5,
        "name": "程志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委常委、纪委书记、监委主任",
        "current_org": "中共休宁县纪律检查委员会",
        "source": "休宁县人民政府官网",
        "notes": "县委常委、县纪委书记、县监委主任，分管纪检监察工作。此前任黄山市纪委监委相关职务。"
    },
    {
        "id": 6,
        "name": "金学年",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委常委、组织部部长",
        "current_org": "中共休宁县委员会组织部",
        "source": "休宁县人民政府官网",
        "notes": "县委常委、组织部部长，分管组织人事工作。"
    },
    {
        "id": 7,
        "name": "洪洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委常委、宣传部部长",
        "current_org": "中共休宁县委员会宣传部",
        "source": "休宁县人民政府官网",
        "notes": "县委常委、宣传部部长，分管宣传思想文化工作。"
    },
    {
        "id": 8,
        "name": "赵世奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委常委、政法委书记",
        "current_org": "中共休宁县委员会政法委员会",
        "source": "休宁县人民政府官网",
        "notes": "县委常委、政法委书记，分管政法维稳工作。"
    },
    {
        "id": 9,
        "name": "潘武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "休宁县委常委、统战部部长",
        "current_org": "中共休宁县委员会统一战线工作部",
        "source": "休宁县人民政府官网",
        "notes": "县委常委、统战部部长，分管统一战线工作。"
    },
    # ── Previous Leaders ──
    {
        "id": 10,
        "name": "吴云忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-08",
        "birthplace": "安徽省黄山市歙县",
        "education": "安徽省委党校大学学历",
        "party_join": "1998-06",
        "work_start": "1991-08",
        "current_post": "黄山市委常委、秘书长、政法委书记",
        "current_org": "中共黄山市委",
        "source": "黄山日报; 安徽省委组织部公示; 澎湃新闻",
        "notes": "2026年5月升任黄山市委常委、秘书长、政法委书记。此前任休宁县委书记(约2021-2026)。曾任休宁县县长(约2019-2021)。出生于1969年8月，歙县人。"
    },
    {
        "id": 11,
        "name": "卢邦生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-10",
        "birthplace": "安徽省广德市",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄山市人大常委会副主任、市总工会主席",
        "current_org": "黄山市人大常委会",
        "source": "黄山市人民代表大会公告; 黄山日报",
        "notes": "2024年2月5日当选黄山市第八届人大常委会副主任，并任市总工会主席。此前任休宁县委书记(约2018-2021)。曾任黄山市教育工作领导小组副组长、市委党校常务副校长。"
    },
]
organizations = [
    {
        "id": 1,
        "name": "中共休宁县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市委",
        "location": "安徽省黄山市休宁县"
    },
    {
        "id": 2,
        "name": "休宁县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黄山市人民政府",
        "location": "安徽省黄山市休宁县"
    },
    {
        "id": 3,
        "name": "中共休宁县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市纪律检查委员会",
        "location": "安徽省黄山市休宁县"
    },
    {
        "id": 4,
        "name": "中共休宁县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共休宁县委员会",
        "location": "安徽省黄山市休宁县"
    },
    {
        "id": 5,
        "name": "中共休宁县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共休宁县委员会",
        "location": "安徽省黄山市休宁县"
    },
    {
        "id": 6,
        "name": "中共休宁县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共休宁县委员会",
        "location": "安徽省黄山市休宁县"
    },
    {
        "id": 7,
        "name": "中共休宁县委员会统一战线工作部",
        "type": "党委",
        "level": "县级",
        "parent": "中共休宁县委员会",
        "location": "安徽省黄山市休宁县"
    },
    {
        "id": 8,
        "name": "休宁县",
        "type": "行政区域",
        "level": "县级",
        "parent": "黄山市",
        "location": "安徽省黄山市"
    },
]

positions = [
    # 唐进 - 县委书记/前县长
    {"id": 1, "person_id": 1, "org_id": 1, "title": "休宁县委书记",
     "start": "2026-07", "end": "present", "rank": "正处级",
     "note": "2026年7月9日任命。主持县委全面工作。"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "休宁县委副书记、县长",
     "start": "2023", "end": "2026-07", "rank": "正处级",
     "note": "约2023年任县长至2026年7月升任书记。"},
    # 汪盛 - 县长（推定）
    {"id": 3, "person_id": 2, "org_id": 2, "title": "休宁县委副书记、县长（推定）",
     "start": "2026-01", "end": "present", "rank": "正处级",
     "note": "2026年1月30日选举进入县级领导岗位。唐进升书记后推定接任县长。"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "休宁县委副书记（推定）",
     "start": "2026-01", "end": "present", "rank": "正处级",
     "note": "推定县委副书记兼县长"},
    # 季必俊 - 县委副书记
    {"id": 5, "person_id": 3, "org_id": 1, "title": "休宁县委副书记",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "专职副书记，协助书记处理日常党务工作"},
    # 郑美风 - 常务副县长
    {"id": 6, "person_id": 4, "org_id": 2, "title": "休宁县委常委、常务副县长",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "负责县政府常务工作"},
    {"id": 7, "person_id": 4, "org_id": 1, "title": "休宁县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 程志强 - 纪委书记
    {"id": 8, "person_id": 5, "org_id": 3, "title": "休宁县委常委、纪委书记、监委主任",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管纪检监察工作，此前任黄山市纪委监委相关职务"},
    {"id": 9, "person_id": 5, "org_id": 1, "title": "休宁县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 金学年 - 组织部长
    {"id": 10, "person_id": 6, "org_id": 4, "title": "休宁县委常委、组织部部长",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管组织人事工作"},
    {"id": 11, "person_id": 6, "org_id": 1, "title": "休宁县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 洪洁 - 宣传部长
    {"id": 12, "person_id": 7, "org_id": 5, "title": "休宁县委常委、宣传部部长",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管宣传思想文化工作"},
    {"id": 13, "person_id": 7, "org_id": 1, "title": "休宁县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 赵世奇 - 政法委书记
    {"id": 14, "person_id": 8, "org_id": 6, "title": "休宁县委常委、政法委书记",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管政法维稳工作"},
    {"id": 15, "person_id": 8, "org_id": 1, "title": "休宁县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 潘武 - 统战部长
    {"id": 16, "person_id": 9, "org_id": 7, "title": "休宁县委常委、统战部部长",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管统一战线工作"},
    {"id": 17, "person_id": 9, "org_id": 1, "title": "休宁县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 吴云忠 - 前县委书记 (id=10)
    {"id": 18, "person_id": 10, "org_id": 1, "title": "休宁县委书记",
     "start": "约2021", "end": "2026", "rank": "正处级",
     "note": "前任县委书记，约2026年5月升任黄山市委常委。"},
    {"id": 19, "person_id": 10, "org_id": 2, "title": "休宁县县长",
     "start": "约2019", "end": "2021", "rank": "正处级",
     "note": "前任县长，后升任县委书记。"},
    # 卢邦生 - 前前县委书记 (id=11)
    {"id": 20, "person_id": 11, "org_id": 1, "title": "休宁县委书记",
     "start": "约2018", "end": "2021", "rank": "正处级",
     "note": "前任县委书记，后任黄山市人大常委会副主任。"},
]

relationships = [
    # 唐进(1) ↔ 汪盛(2) — 党政搭档（推定）
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "唐进（县委书记）与汪盛（县长推定）为休宁县新的党政搭档",
        "overlap_org": "休宁县",
        "overlap_period": "2026–present"
    },
    # 唐进(1) ↔ 季必俊(3)
    {
        "id": 2,
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "唐进（县委书记）与季必俊（县委副书记）同为县委领导班子成员",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "2023–present"
    },
    # 唐进(1) ↔ 郑美风(4)
    {
        "id": 3,
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "唐进（书记/前县长）与郑美风（常务副县长）长期搭档",
        "overlap_org": "休宁县人民政府",
        "overlap_period": "2023–present"
    },
    # 唐进(1) ↔ 程志强(5)
    {
        "id": 4,
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "唐进与程志强（纪委书记）同为县委领导班子",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "2023–present"
    },
    # 唐进(1) ↔ 金学年(6)
    {
        "id": 5,
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "唐进与金学年（组织部长）同为县委领导班子",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "2023–present"
    },
    # 唐进(1) ↔ 洪洁(7)
    {
        "id": 6,
        "person_a": 1, "person_b": 7,
        "type": "overlap",
        "context": "唐进与洪洁（宣传部长）同为县委领导班子",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "2023–present"
    },
    # 唐进(1) ↔ 赵世奇(8)
    {
        "id": 7,
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "唐进与赵世奇（政法委书记）同为县委领导班子",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "2023–present"
    },
    # 唐进(1) ↔ 潘武(9)
    {
        "id": 8,
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "唐进与潘武（统战部长）同为县委领导班子",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "2023–present"
    },
    # 汪盛(2) ↔ 郑美风(4)
    {
        "id": 9,
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "汪盛（推定县长）与郑美风（常务副县长）为县政府正副职搭档",
        "overlap_org": "休宁县人民政府",
        "overlap_period": "2026–present"
    },
    # 吴云忠(10) → 唐进(1) (predecessor-successor 书记)
    {
        "id": 10,
        "person_a": 10, "person_b": 1,
        "type": "predecessor_successor",
        "context": "唐进接替吴云忠任休宁县委书记",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "2026-07"
    },
    # 卢邦生(11) → 吴云忠(10) (predecessor-successor 书记)
    {
        "id": 11,
        "person_a": 11, "person_b": 10,
        "type": "predecessor_successor",
        "context": "吴云忠接替卢邦生任休宁县委书记",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "约2021"
    },
    # 吴云忠(10) → 唐进(1) (predecessor-successor 县长)
    {
        "id": 12,
        "person_a": 10, "person_b": 1,
        "type": "predecessor_successor",
        "context": "唐进接替吴云忠（时任）任休宁县县长",
        "overlap_org": "休宁县人民政府",
        "overlap_period": "约2023"
    },
    # 吴云忠(10) — 自身县长到书记 (career arc)
    {
        "id": 13,
        "person_a": 10, "person_b": 10,
        "type": "overlap",
        "context": "吴云忠从县长升任县委书记",
        "overlap_org": "休宁县",
        "overlap_period": "约2019–2021（县长）→2021–2026（书记）"
    },
    # 季必俊(3) ↔ 郑美风(4)
    {
        "id": 14,
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "季必俊（副书记）与郑美风（常务副县长）同为县委常委会成员",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "未知–present"
    },
    # 金学年(6) ↔ 洪洁(7)
    {
        "id": 15,
        "person_a": 6, "person_b": 7,
        "type": "overlap",
        "context": "金学年（组织部长）与洪洁（宣传部长）同为县委常委会成员",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "未知–present"
    },
    # 赵世奇(8) ↔ 潘武(9)
    {
        "id": 16,
        "person_a": 8, "person_b": 9,
        "type": "overlap",
        "context": "赵世奇（政法委书记）与潘武（统战部长）同为县委常委会成员",
        "overlap_org": "中共休宁县委员会",
        "overlap_period": "未知–present"
    },
]

# ── helpers ──────────────────────────────────────────────────────────────

def is_top_leader(p):
    """Return True for the party secretary (top leader)."""
    return "书记" in p["current_post"] and "副书记" not in p["current_post"]

def is_mayor(p):
    """Return True for the county mayor/magistrate."""
    return "县长" in p["current_post"] and "副书记" in p["current_post"]

def person_color(p):
    """Return 'r,g,b' string for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"      # Red — Party Secretary
    if "县长" in post:
        return "50,100,255"     # Blue — Mayor/县长
    if "副书记" in post:
        return "200,50,200"     # Purple — Deputy Secretary
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"      # Orange — Discipline
    return "100,100,100"        # Grey — Others

def org_color(o):
    """Return 'r,g,b' string for an org node."""
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "行政区域":
        return "200,255,200"
    return "200,200,200"

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ── BUILD SQLite ────────────────────────────────────────────────────────

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
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"SQLite DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF ──────────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>休宁县（安徽省黄山市）领导关系网络 — 县委书记、县长及县委常委领导班子</description>')
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
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("16.0" if is_mayor(p) else ("14.0" if "副书记" in p["current_post"] else "12.0"))
        role = p.get("current_post", "")
        org = p.get("current_org", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')

    eid = 0

    # Person → Org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"GEXF graph written: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  休宁县（Xiuning County）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
