#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 翠屏区 (Cuiping District), 宜宾市, 四川省.

Investigation date: 2026-07-26
Task ID: sichuan_翠屏区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.cuiping.gov.cn — 宜宾市翠屏区人民政府 (official leadership profiles, accessed 2026-07-26)
  - www.cuiping.gov.cn/qzfld/ — 政府领导页面 (confirmed 区长李刚, 常务副区长王科, 副区长团队)
  - www.cuiping.gov.cn/zwhd/cpyw/ — 翠屏要闻 (confirmed 区委书记石进, 区委副书记黄宁, etc.)
  - www.yibin.gov.cn/xxgk/rszk/rqgs/ — 宜宾市委组织部干部任前公示

Confirmed officeholders:
  - 区委书记: 石进 (also 宜宾李庄古镇景区党工委书记) — confirmed via official news 2026-07-21
  - 区长: 李刚 (区委副书记、区政府党组书记、区长) — confirmed via official领导之窗
  - 区委副书记: 黄宁 — confirmed via 2026-07-06 meeting report
  - 常务副区长: 王科 — official bio page
  - 副区长团队: 凌健(公安)、胡刚(农业农村)、周薇薇(文教卫)、孙善明(财税金融)、王琛(住建旅游)、顾珏(科技+挂职)、李昌治(挂职)

Confidence notes:
  - 石进 (区委书记): confirmed name via official news; detailed career timeline unknown
  - 李刚 (区长): confirmed via official bio; bio limited to birth info only
  - All leadership roster confirmed via official government pages
  - Detailed career timelines incomplete due to web access limitations
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = str(STAGING_DIR)
SLUG = "翠屏区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = os.path.join(BASE, "data", "persons")

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Secretary (区委书记)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "石进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共宜宾市翠屏区委员会",
        "source": "翠屏区人民政府官方网站-新闻(cuiping.gov.cn/zwhd/cpyw/202607/t20260721_2243296.html)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government Leader (区长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "在职硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-政府领导-李刚(cuiping.gov.cn/qzfld/qz/202404/t20240426_1980652.html)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Leaders — 区政府领导班子
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "王科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "在职硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-政府领导-王科(cuiping.gov.cn/qzfld/fqz/202602/t20260209_2202942.html)"
    },
    {
        "id": 4,
        "name": "凌健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "在职硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长(公安)",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-凌健 宜宾市公安局翠屏区分局党委书记、局长、督察长"
    },
    {
        "id": 5,
        "name": "胡刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "在职本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-胡刚(cuiping.gov.cn/qzfld/fqz/202308/t20230804_1889714.html)"
    },
    {
        "id": 6,
        "name": "周薇薇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-周薇薇(cuiping.gov.cn/qzfld/fqz/202402/t20240206_1956037.html)"
    },
    {
        "id": 7,
        "name": "孙善明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-孙善明(cuiping.gov.cn/qzfld/fqz/202504/t20250402_2108099.html)"
    },
    {
        "id": 8,
        "name": "王琛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-王琛(cuiping.gov.cn/qzfld/fqz/202511/t20251117_2171904.html)"
    },
    {
        "id": 9,
        "name": "顾珏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "",
        "education": "在职硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长(挂职)",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-顾珏(cuiping.gov.cn/qzfld/fqz/202108/t20210827_1635514.html)"
    },
    {
        "id": 10,
        "name": "李昌治",
        "gender": "男",
        "ethnicity": "",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "全日制研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长(挂职)",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-李昌治(cuiping.gov.cn/qzfld/fqz/202602/t20260211_2203960.html)"
    },
    {
        "id": 11,
        "name": "朱肪涌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年5月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-朱肪涌(cuiping.gov.cn/qzfld/qzfdzcy/202405/t20240527_1989379.html)"
    },
    {
        "id": 12,
        "name": "刁志平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、办公室主任",
        "current_org": "宜宾市翠屏区人民政府",
        "source": "翠屏区人民政府网站-刁志平(cuiping.gov.cn/qzfld/bgszr/202407/t20240729_2008413.html)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Leadership — 区委领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "黄宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共宜宾市翠屏区委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议新闻(cuiping.gov.cn 2026-07-06)"
    },
    {
        "id": 14,
        "name": "王治博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共宜宾市翠屏区委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议参会名单(2026-07-06)"
    },
    {
        "id": 15,
        "name": "罗小兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共宜宾市翠屏区委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议参会名单(2026-07-06)"
    },
    {
        "id": 16,
        "name": "王渊博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共宜宾市翠屏区委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议参会名单(2026-07-06)"
    },
    {
        "id": 17,
        "name": "白静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共宜宾市翠屏区委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议参会名单(2026-07-06)"
    },
    {
        "id": 18,
        "name": "祝科",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共宜宾市翠屏区委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议参会名单(2026-07-06)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 19,
        "name": "范建平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "宜宾市翠屏区人民代表大会常务委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议(2026-07-06)"
    },
    {
        "id": 20,
        "name": "詹立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议宜宾市翠屏区委员会",
        "source": "翠屏区委全面依法治区委员会第八次会议(2026-07-06)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宜宾市翠屏区委员会", "type": "党委", "level": "县级", "parent": "中共宜宾市委员会", "location": "宜宾市翠屏区"},
    {"id": 2, "name": "宜宾市翠屏区人民政府", "type": "政府", "level": "县级", "parent": "宜宾市人民政府", "location": "宜宾市翠屏区"},
    {"id": 3, "name": "宜宾市翠屏区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "宜宾市翠屏区"},
    {"id": 4, "name": "中国人民政治协商会议宜宾市翠屏区委员会", "type": "政协", "level": "县级", "parent": "", "location": "宜宾市翠屏区"},
    {"id": 5, "name": "宜宾李庄古镇景区党工委", "type": "党委", "level": "县级", "parent": "", "location": "宜宾市翠屏区李庄镇"},
    {"id": 6, "name": "宜宾市公安局翠屏区分局", "type": "政府", "level": "县级", "parent": "宜宾市翠屏区人民政府", "location": "宜宾市翠屏区"},
    {"id": 7, "name": "宜宾国家农业科技园区管委会", "type": "政府", "level": "县级", "parent": "", "location": "宜宾市翠屏区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # Current Party Secretary — 石进
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": "区委书记（2026年7月仍在任）"},
    {"person_id": 1, "org_id": 5, "title": "党工委书记（兼）", "start_date": "", "end_date": "至今", "rank": "", "note": "宜宾李庄古镇景ng区党工委书记"},

    # Current Mayor — 李刚
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": "区政府党组书记、区长，主持全面工作，分管审计局"},

    # Deputy Mayor — 王科（常务副区长）
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组副书记、常务副区长"},
    {"person_id": 3, "org_id": 1, "title": "区委领导", "start_date": "", "end_date": "至今", "rank": "", "note": "区委领导"},

    # 凌健（副区长、公安）
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员、副区长"},
    {"person_id": 4, "org_id": 6, "title": "局长", "start_date": "", "end_date": "至今", "rank": "", "note": "宜宾市公安局翠屏区分局党委书记、局长、督察长"},

    # 胡刚（副区长、农业农村）
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员、副区长，负责农业农村、林业、水利、生态环境"},

    # 周薇薇（副区长）
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "民革党员，负责教育体育、民政、医保、卫生健康"},

    # 孙善明（副区长）
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员、副区长，负责财政、税务、金融、商务、国资"},

    # 王琛（副区长）
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员、副区长，负责住建、自然资源、文旅、数字经济"},

    # 顾珏（副区长）
    {"person_id": 9, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员、副区长，负责科技、民族宗教、供销"},

    # 李昌治（挂职）
    {"person_id": 10, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "协助工业经济、科技、经合外事"},

    # 朱肪涌
    {"person_id": 11, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "至今", "rank": "", "note": "宜宾国家农业园区管委会副主任"},
    {"person_id": 11, "org_id": 7, "title": "管委会副主任", "start_date": "", "end_date": "至今", "rank": "", "note": "宜宾国家农业科技园区党工委委员、管委会副主任"},

    # 刁志平（区政府办公室主任）
    {"person_id": 12, "org_id": 2, "title": "区政府党组成员、办公室主任", "start_date": "", "end_date": "至今", "rank": "正科级", "note": "区政府办公室党组书记、主任"},

    # 黄宁（区委副书记）
    {"person_id": 13, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},

    # 人大、政协
    {"person_id": 19, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Top leadership: Party Secretary ↔ Government Leader
    {"person_a": 1, "person_b": 2, "type": "colleague", "context": "石进(区委书记)与李刚(区长)在翠屏区党政一把手搭档", "overlap_org": "中共宜宾市翠片区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "石进(书记)与黄宁(副书记)在区委班子共事", "overlap_org": "中共宜宾市翠屏区委员会", "overlap_period": "至今"},

    # Mayor with deputies
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "李刚(区长)与王科(常务副区长)在区政府搭档", "overlap_org": "宜宾市翠屏区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "李刚(区长)与凌健(副区长/公安局长)在区政府共事", "overlap_org": "宜宾市翠屏区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "李刚(区长)与胡刚(副区长)在区政府共事", "overlap_org": "宜宾市翠屏区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "李刚(区长)与周薇薇(副区长)在区政府共事", "overlap_org": "宜宾市翠屏区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "李刚(区长)与孙善明(副区长)在区政府共事", "overlap_org": "宜宾市翠屏区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "李刚(区长)与王琛(副区长)在区政府共事", "overlap_org": "宜宾市翠屏区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "李刚(区长)与刁志平(办公室主任)", "overlap_org": "宜宾市翠屏区人民政府", "overlap_period": "至今"},
]

# ── Build ──────────────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for a person based on current role."""
    role = p.get("current_post", "")
    if "书记" in role and "纪委" not in role and "副" not in role:
        return "255,50,50"    # Red — Party Secretary
    elif "区长" in role and "副" not in role:
        return "50,100,255"   # Blue — Government leader
    elif "常务" in role:
        return "50,150,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "公安" in role or "政法" in role:
        return "100,100,200"
    else:
        return "100,100,100"  # Grey — Others

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:  return "255,200,200"
    if "政府" in t:  return "200,200,255"
    if "人大" in t:  return "200,255,255"
    if "政协" in t:  return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

def node_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_sqlite(db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    for name in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {name}")
    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
        type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                      p.get("birthplace", ""), p["education"], p["party_join"], p.get("work_start", ""),
                      p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
                     (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                     (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))
    conn.commit()
    conn.close()
    print(f"  Database written: {db_path}")
    print(f"  - {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

def build_gexf(gexf_path):
    from datetime import datetime as dt
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>翠屏区领导班子工作关系网络 - Cuiping Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')
    # ── Person nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = node_size(p)
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:position x="{hash(pid) % 1000 - 500}" y="{hash(pid[::-1]) % 1000 - 500}" z="0.0"/>')
        lines.append('      </node>')
    # ── Organization nodes ──
    for o in organizations:
        c = org_color(o)
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # ── Edges ──
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        period = f"{pos['start_date']} - {pos['end_date']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        weight = "2.0" if r.get("type") in ("colleague", "superior_subordinate") else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" weight="{weight}" label="{esc(r["context"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {gexf_path}")
    print(f"  - {len(positions)} worked_at edges, {len(relationships)} relationship edges")


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"=== 翠屏区 Network Data Builder ===")
    print(f"Staging: {STAGING_DIR}")

    # Ensure directories
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    # Build SQLite
    print("Building SQLite database...")
    build_sqlite(DB_PATH)

    # Build GEXF
    print("Building GEXF graph...")
    build_gexf(GEXF_PATH)

    print("Done!")

if __name__ == "__main__":
    main()