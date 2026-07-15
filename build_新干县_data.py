#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 新干县 (江西省吉安市) leadership network.

⚠️  LIMITATION NOTES:
- Web search tools (Exa, Baidu, Bing) were all blocked/unavailable from the build environment.
- The official xingan.gov.cn website uses AJAX-loaded content that could not be programmatically
  accessed (returns empty data arrays without browser session state).
- Therefore, the current 县委书记 and 县长 names could NOT be confirmed from any online source.
- All person data is marked with confidence="unverified" or "待查" where unknown.
- This creates a structurally valid shell that documents the known gaps and can be filled in
  once web search or the official website becomes accessible.
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
# When run from staging dir
if "data/tmp" in BASE:
    DB_PATH = os.path.join(BASE, "新干县_network.db")
    GEXF_PATH = os.path.join(BASE, "新干县_network.gexf")
else:
    # Canonical paths after promotion
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(PROJECT_ROOT, "data/database/新干县_network.db")
    GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/新干县_network.gexf")

KNOWN_DATE = "2026-07-15"

# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── 县委书记 (Party Secretary) ──
    # ⚠️  CURRENT NAME UNKNOWN. Could not access xingan.gov.cn leadership page
    #    or Baidu Baike from the build environment. All web search tools blocked.
    {
        "id": 1,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "中共新干县委书记",
        "current_org": "中共新干县委员会",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 县长 (County Mayor) ──
    # ⚠️  CURRENT NAME UNKNOWN. Same reason as above.
    {
        "id": 2,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县人民政府县长",
        "current_org": "新干县人民政府",
        "source": "http://www.xingan.gov.cn/xxgk-list-xzfld.html"
    },

    # ── 县委副书记 (Deputy Party Secretary) ──
    {
        "id": 3,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委副书记",
        "current_org": "中共新干县委员会",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 常务副县长 (Executive Deputy Mayor) ──
    {
        "id": 4,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委常委、常务副县长",
        "current_org": "新干县人民政府",
        "source": "http://www.xingan.gov.cn/xxgk-list-xzfld.html"
    },

    # ── 纪委书记 (Discipline Inspection Secretary) ──
    {
        "id": 5,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委常委、县纪委书记、县监委主任",
        "current_org": "中共新干县纪律检查委员会",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 组织部长 (Organization Department Head) ──
    {
        "id": 6,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委常委、组织部部长",
        "current_org": "中共新干县委组织部",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 宣传部长 (Propaganda Department Head) ──
    {
        "id": 7,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委常委、宣传部部长",
        "current_org": "中共新干县委宣传部",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 政法委书记 (Politics & Law Commission Secretary) ──
    {
        "id": 8,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委常委、政法委书记",
        "current_org": "中共新干县委政法委员会",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 统战部长 (United Front Work Department Head) ──
    {
        "id": 9,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委常委、统战部部长",
        "current_org": "中共新干县委统一战线工作部",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 人武部主官 (Armed Forces Dept Head) ──
    # By convention, either the political commissar or commander enters the standing committee
    {
        "id": 10,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县委常委、人武部政委（或部长）",
        "current_org": "新干县人民武装部",
        "source": "http://www.xingan.gov.cn/xxgk-list-xwld.html"
    },

    # ── 副县长 (Deputy Mayors) ──
    {
        "id": 11,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县副县长",
        "current_org": "新干县人民政府",
        "source": "http://www.xingan.gov.cn/xxgk-list-xzfld.html"
    },
    {
        "id": 12,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县副县长",
        "current_org": "新干县人民政府",
        "source": "http://www.xingan.gov.cn/xxgk-list-xzfld.html"
    },
    {
        "id": 13,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县副县长",
        "current_org": "新干县人民政府",
        "source": "http://www.xingan.gov.cn/xxgk-list-xzfld.html"
    },
    {
        "id": 14,
        "name": "（待确认）",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县副县长",
        "current_org": "新干县人民政府",
        "source": "http://www.xingan.gov.cn/xxgk-list-xzfld.html"
    },

    # ── 县人大常委会主任 (NPC Standing Committee Chair) ──
    {
        "id": 15,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县人大常委会主任",
        "current_org": "新干县人民代表大会常务委员会",
        "source": "http://www.xingan.gov.cn/xxgk-list-xrdld.html"
    },

    # ── 县政协主席 (CPPCC Chair) ──
    {
        "id": 16,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "新干县政协主席",
        "current_org": "中国人民政治协商会议新干县委员会",
        "source": "http://www.xingan.gov.cn/xxgk-list-xzxld.html"
    },

    # ── 吉安市领导 (Jian Municipal Leaders) ──
    # Source: report/20260714-吉安市-领导班子.md
    {
        "id": 17,
        "name": "严允",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "江西石城",
        "education": "南昌大学中文系汉语言文学专业（大学学历）",
        "party_join": "1993-11",
        "work_start": "1994-07",
        "current_post": "吉安市委书记",
        "current_org": "中共吉安市委",
        "source": "report/20260714-吉安市-领导班子.md"
    },
    {
        "id": 18,
        "name": "（空缺）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉安市市长（空缺）",
        "current_org": "吉安市人民政府",
        "source": "report/20260714-吉安市-领导班子.md"
    },
    {
        "id": 19,
        "name": "吴艳玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吉安市委副书记",
        "current_org": "中共吉安市委",
        "source": "report/20260714-吉安市-领导班子.md"
    },
    {
        "id": 20,
        "name": "陈定宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吉安市委常委、市纪委书记、市监委主任",
        "current_org": "中共吉安市纪委",
        "source": "report/20260714-吉安市-领导班子.md"
    },
    {
        "id": 21,
        "name": "龚平秋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-06",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吉安市委常委、组织部部长",
        "current_org": "中共吉安市委组织部",
        "source": "report/20260714-吉安市-领导班子.md"
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共新干县委员会", "type": "党委", "level": "县处级", "parent": "中共吉安市委", "location": "江西省吉安市新干县"},
    {"id": 2, "name": "新干县人民政府", "type": "政府", "level": "县处级", "parent": "吉安市人民政府", "location": "江西省吉安市新干县"},
    {"id": 3, "name": "中共新干县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "吉安市纪委监委", "location": "江西省吉安市新干县"},
    {"id": 4, "name": "中共新干县委组织部", "type": "党委部门", "level": "乡科级", "parent": "中共新干县委", "location": "江西省吉安市新干县"},
    {"id": 5, "name": "中共新干县委宣传部", "type": "党委部门", "level": "乡科级", "parent": "中共新干县委", "location": "江西省吉安市新干县"},
    {"id": 6, "name": "中共新干县委政法委员会", "type": "党委部门", "level": "乡科级", "parent": "中共新干县委", "location": "江西省吉安市新干县"},
    {"id": 7, "name": "中共新干县委统一战线工作部", "type": "党委部门", "level": "乡科级", "parent": "中共新干县委", "location": "江西省吉安市新干县"},
    {"id": 8, "name": "新干县人民武装部", "type": "军事", "level": "县处级", "parent": "吉安军分区", "location": "江西省吉安市新干县"},
    {"id": 9, "name": "新干县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "吉安市人大常委会", "location": "江西省吉安市新干县"},
    {"id": 10, "name": "中国人民政治协商会议新干县委员会", "type": "政协", "level": "县处级", "parent": "吉安市政协", "location": "江西省吉安市新干县"},
    {"id": 11, "name": "中共吉安市委", "type": "党委", "level": "地级市", "parent": "中共江西省委", "location": "吉安市"},
    {"id": 12, "name": "吉安市人民政府", "type": "政府", "level": "地级市", "parent": "江西省人民政府", "location": "吉安市"},
    {"id": 13, "name": "中共吉安市纪委/监委", "type": "纪委", "level": "地级市", "parent": "中共吉安市委", "location": "吉安市"},
    {"id": 14, "name": "中共吉安市委组织部", "type": "党委部门", "level": "地级市", "parent": "中共吉安市委", "location": "吉安市"},
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共新干县委书记", "start": "待查", "end": "", "rank": "县处级正职", "note": "⚠️ 姓名待确认。"},
    # 县长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "新干县人民政府县长", "start": "待查", "end": "", "rank": "县处级正职", "note": "⚠️ 姓名待确认。"},
    # 县委副书记
    {"id": 3, "person_id": 3, "org_id": 1, "title": "新干县委副书记（专职）", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。"},
    # 常务副县长
    {"id": 4, "person_id": 4, "org_id": 2, "title": "新干县委常委、常务副县长", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。"},
    # 纪委书记
    {"id": 5, "person_id": 5, "org_id": 3, "title": "新干县委常委、县纪委书记、县监委主任", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。"},
    # 组织部长
    {"id": 6, "person_id": 6, "org_id": 4, "title": "新干县委常委、组织部部长", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。"},
    # 宣传部长
    {"id": 7, "person_id": 7, "org_id": 5, "title": "新干县委常委、宣传部部长", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。"},
    # 政法委书记
    {"id": 8, "person_id": 8, "org_id": 6, "title": "新干县委常委、政法委书记", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。"},
    # 统战部长
    {"id": 9, "person_id": 9, "org_id": 7, "title": "新干县委常委、统战部部长", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。"},
    # 人武部主官
    {"id": 10, "person_id": 10, "org_id": 8, "title": "新干县委常委、人武部政委（或部长）", "start": "待查", "end": "", "rank": "县处级副职", "note": "⚠️ 姓名待确认。按照惯例，人武部主官之一进入县委常委。"},
    # 副县长
    {"id": 11, "person_id": 11, "org_id": 2, "title": "新干县副县长", "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},
    {"id": 12, "person_id": 12, "org_id": 2, "title": "新干县副县长", "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},
    {"id": 13, "person_id": 13, "org_id": 2, "title": "新干县副县长", "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},
    {"id": 14, "person_id": 14, "org_id": 2, "title": "新干县副县长", "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},
    # 人大主任
    {"id": 15, "person_id": 15, "org_id": 9, "title": "新干县人大常委会主任", "start": "待查", "end": "", "rank": "县处级正职", "note": "⚠️ 姓名待确认。"},
    # 政协主席
    {"id": 16, "person_id": 16, "org_id": 10, "title": "新干县政协主席", "start": "待查", "end": "", "rank": "县处级正职", "note": "⚠️ 姓名待确认。"},

    # 吉安市领导
    {"id": 17, "person_id": 17, "org_id": 11, "title": "吉安市委书记", "start": "2026-04", "end": "", "rank": "正厅级", "note": "现任；从宜春市委书记调任"},
    {"id": 18, "person_id": 18, "org_id": 12, "title": "吉安市市长（空缺）", "start": "", "end": "", "rank": "正厅级", "note": "前任王亚联2026年1月离任，至今未补"},
    {"id": 19, "person_id": 19, "org_id": 11, "title": "吉安市委副书记", "start": "~2022-11", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 20, "person_id": 20, "org_id": 13, "title": "吉安市委常委、市纪委书记", "start": "~2022", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 21, "person_id": 20, "org_id": 13, "title": "吉安市监委主任", "start": "~2022", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 22, "person_id": 21, "org_id": 11, "title": "吉安市委常委、组织部部长", "start": "~2025-10", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 23, "person_id": 21, "org_id": 14, "title": "吉安市委组织部部长", "start": "~2025-10", "end": "", "rank": "正处级", "note": "现任"},
]

# ── Relationships ────────────────────────────────────────────────────

relationships = [
    # 党政正职搭档关系
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "工作关系", "context": "县委书记与县长为新干县党政正职搭档关系", "overlap_org": "新干县", "overlap_period": "至2026年"},

    # 县委书记与市级领导
    {"id": 2, "person_a_id": 1, "person_b_id": 17, "type": "上下级关系", "context": "县委书记受吉安市委领导，严允为吉安市委书记", "overlap_org": "中共吉安市委-新干县", "overlap_period": "2026-04至今"},
    {"id": 3, "person_a_id": 1, "person_b_id": 21, "type": "上下级关系", "context": "县管干部工作关系：县委书记与市委组织部部长在干部选拔任用中存在工作互动", "overlap_org": "吉安市-新干县干部体系", "overlap_period": ""},
    {"id": 4, "person_a_id": 1, "person_b_id": 20, "type": "监督关系", "context": "县委书记与市纪委书记为同级党委-纪委关系", "overlap_org": "吉安市-新干县监督体系", "overlap_period": ""},
    {"id": 5, "person_a_id": 1, "person_b_id": 19, "type": "上下级关系", "context": "县委受市委领导，县书记与市委副书记为上下级工作关系", "overlap_org": "吉安市", "overlap_period": ""},

    # 县级班子关系
    {"id": 6, "person_a_id": 1, "person_b_id": 5, "type": "工作关系", "context": "县委书记与县纪委书记为同级党委-纪委关系", "overlap_org": "中共新干县委员会", "overlap_period": "至2026年"},
    {"id": 7, "person_a_id": 1, "person_b_id": 4, "type": "工作关系", "context": "县委书记与常务副县长为常委会班子关系", "overlap_org": "中共新干县委员会", "overlap_period": "至2026年"},
    {"id": 8, "person_a_id": 1, "person_b_id": 6, "type": "工作关系", "context": "县委书记与组织部部长为常委会班子关系", "overlap_org": "中共新干县委员会", "overlap_period": "至2026年"},
    {"id": 9, "person_a_id": 1, "person_b_id": 7, "type": "工作关系", "context": "县委书记与宣传部部长为常委会班子关系", "overlap_org": "中共新干县委员会", "overlap_period": "至2026年"},
    {"id": 10, "person_a_id": 1, "person_b_id": 8, "type": "工作关系", "context": "县委书记与政法委书记为常委会班子关系", "overlap_org": "中共新干县委员会", "overlap_period": "至2026年"},
    {"id": 11, "person_a_id": 1, "person_b_id": 9, "type": "工作关系", "context": "县委书记与统战部部长为常委会班子关系", "overlap_org": "中共新干县委员会", "overlap_period": "至2026年"},

    # 县长与市级领导
    {"id": 12, "person_a_id": 2, "person_b_id": 17, "type": "上下级关系", "context": "县长受市委领导，市委书记严允为吉安市最高党政负责人", "overlap_org": "吉安市", "overlap_period": "2026-04至今"},

    # 人大政协
    {"id": 13, "person_a_id": 15, "person_b_id": 1, "type": "工作关系", "context": "县人大常委会主任与县委书记为四套班子关系", "overlap_org": "新干县", "overlap_period": "至2026年"},
    {"id": 14, "person_a_id": 16, "person_b_id": 1, "type": "工作关系", "context": "县政协主席与县委书记为四套班子关系", "overlap_org": "新干县", "overlap_period": "至2026年"},
]


# ══════════════════════════════════════════════════════════════════════
# BUILD SQLite DATABASE
# ══════════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ══════════════════════════════════════════════════════════════════════
# BUILD GEXF GRAPH
# ══════════════════════════════════════════════════════════════════════

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>新干县领导班子工作关系网络 - {today}</description>')
lines.append('    <description>⚠️ 所有核心人物姓名待确认 - web search tools unavailable during build</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    if p["id"] == 1:
        color = (231, 76, 60)   # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = (52, 152, 219)  # blue: government leader
        size = 20.0
    elif p["id"] in (5,):       # discipline
        color = (230, 126, 34)  # orange
        size = 16.0
    elif p["id"] in (4, 6, 7, 8, 9, 10, 3):  # other standing committee
        color = (149, 165, 166) # grey
        size = 12.0
    elif p["id"] in (11, 12, 13, 14):  # deputy mayors
        color = (149, 165, 166)
        size = 12.0
    elif p["id"] in (15, 16):   # NPC/CPPCC
        color = (149, 165, 166)
        size = 12.0
    elif p["id"] == 17:         # 市委书记
        color = (192, 57, 43)
        size = 18.0
    elif p["id"] == 18:         # 市长（空缺）
        color = (100, 100, 100)
        size = 14.0
    elif p["id"] == 19:         # 市委副书记
        color = (149, 165, 166)
        size = 14.0
    elif p["id"] == 20:         # 纪委书记
        color = (230, 126, 34)
        size = 14.0
    elif p["id"] == 21:         # 组织部长
        color = (149, 165, 166)
        size = 14.0
    else:
        color = (149, 165, 166)
        size = 12.0

    lines.append(f'      <node id="p{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{color[0]}" g="{color[1]}" b="{color[2]}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
org_color_map = {
    "党委": (255, 200, 200),
    "政府": (200, 200, 255),
    "纪委": (255, 220, 200),
    "党委部门": (255, 230, 230),
    "军事": (220, 220, 220),
    "人大": (200, 255, 255),
    "政协": (255, 240, 200),
}

for o in organizations:
    oid = 1000 + o["id"]
    c = org_color_map.get(o["type"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="p{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")

print("\n" + "=" * 60)
print("⚠️  IMPORTANT: All 新干县 local person names are placeholders.")
print("   Web search tools (Exa, Baidu, Bing) were all blocked during build.")
print("   The xingan.gov.cn leadership page requires browser JS rendering.")
print("   Person JSON files were NOT created because names are unknown.")
print("   To complete this investigation: run again with working web search")
print("   after filling in the actual names from the official source.")
print("=" * 60)
print("\nDone!")
