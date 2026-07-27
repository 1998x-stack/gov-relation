#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 桃山区 (Taoshan District), 七台河市, 黑龙江省.

Level: 市辖区
Province: 黑龙江省
Parent city: 七台河市
Targets: 区委书记 (Party Secretary: 魏锟), 区长 (Mayor: 张玉)
Task ID: heilongjiang_桃山区

Research date: 2026-07-24
Official source: http://www.hljtsq.gov.cn/ (七台河市桃山区人民政府)

Current status (as of 2026-07-24, verified via 桃山区人民政府 website 领导之窗):
- 区委书记: 魏锟 (男，汉族，1973年7月生，硕士研究生学历，中共党员)
- 区长: 张玉 (女，汉族，1972年7月生，研究生学历，中共党员)
- Full leadership roster confirmed on district website

Leadership roster sourced from:
  - http://www.hljtsq.gov.cn/hljtsq/c100853/ldzc.shtml (区委)
  - http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml (区政府)
  - http://www.hljtsq.gov.cn/hljtsq/c100854/ldzc.shtml (人大)
  - http://www.hljtsq.gov.cn/hljtsq/c100856/ldzc.shtml (政协)

Confidence notes:
  魏锟 and 张玉 identities confirmed via official government bio pages with name, gender, birth, education.
  Full leadership roster confirmed via official leadership window pages.
  Detailed career histories before current roles not publicly available.
  Web search tools (Exa, Baidu, Jina, Google) were rate-limited or timed out during this investigation.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "桃山区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 魏锟 — 区委书记
    {
        "id": 1,
        "name": "魏锟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100853/202108/f116d1a185694761a616212f8ba18689.shtml",
    },
    # 2. 张玉 — 区委副书记、区长
    {
        "id": 2,
        "name": "张玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100853/202201/94e9f50afdb4459e9e5044d298e40a48.shtml",
    },

    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════

    # 3. 李荣美 — 区委副书记、政法委书记
    {
        "id": 3,
        "name": "李荣美",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100853/202606/44a19b22071c48dca363fd2496f24c42.shtml",
    },
    # 4. 秦刚 — 区委常委、区纪委书记、监委主任
    {
        "id": 4,
        "name": "秦刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、监委主任",
        "current_org": "桃山区纪律检查委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100853/202204/6b0b21dbc97b428285411287151fe903.shtml",
    },
    # 5. 李海峰 — 区委常委、组织部部长
    {
        "id": 5,
        "name": "李海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100853/202312/b246f2f4f8a543cd98d918fd9f423679.shtml",
    },
    # 6. 董哲 — 区委常委、副区长
    {
        "id": 6,
        "name": "董哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100853/202312/bf5a71f4cef34546967cc2fc0be3f142.shtml",
    },
    # 7. 刘明磊 — 区委常委、宣传部部长、统战部部长
    {
        "id": 7,
        "name": "刘明磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、统战部部长",
        "current_org": "中共桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100853/202410/4cea2fff8c9c41bba0ba3d47cdc17984.shtml",
    },
    # 8. 刘国胜 — 区委常委、副区长，区政府党组成员
    {
        "id": 8,
        "name": "刘国胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
    },
    # 9. 李铭 — 区委常委、副区长
    {
        "id": 9,
        "name": "李铭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
    },

    # ════════════════════════════════════════
    # 政府领导 (Government)
    # ════════════════════════════════════════

    # 10. 于涛 — 副区长、区政府党组成员
    {
        "id": 10,
        "name": "于涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
    },
    # 11. 姜贵 — 副区长、桃山公安分局局长
    {
        "id": 11,
        "name": "姜贵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、桃山公安分局局长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
    },
    # 12. 韩炜 — 副区长、区政府党组成员
    {
        "id": 12,
        "name": "韩炜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
    },
    # 13. 刘国鑫 — 副区长、区政府党组成员
    {
        "id": 13,
        "name": "刘国鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桃山区人民政府",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
    },

    # ════════════════════════════════════════
    # 人大常委会 (People's Congress)
    # ════════════════════════════════════════

    # 14. 刘永辉 — 人大常委会主任
    {
        "id": 14,
        "name": "刘永辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "人大常委会主任",
        "current_org": "桃山区人大常委会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100854/ldzc.shtml",
    },
    # 15. 郎帝 — 人大常委会副主任
    {
        "id": 15,
        "name": "郎帝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "人大常委会副主任",
        "current_org": "桃山区人大常委会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100854/ldzc.shtml",
    },
    # 16. 林广辉 — 人大常委会副主任
    {
        "id": 16,
        "name": "林广辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "人大常委会副主任",
        "current_org": "桃山区人大常委会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100854/ldzc.shtml",
    },
    # 17. 梁清 — 人大常委会副主任
    {
        "id": 17,
        "name": "梁清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "人大常委会副主任",
        "current_org": "桃山区人大常委会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100854/ldzc.shtml",
    },
    # 18. 王淑英 — 人大常委会副主任
    {
        "id": 18,
        "name": "王淑英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "人大常委会副主任",
        "current_org": "桃山区人大常委会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100854/ldzc.shtml",
    },

    # ════════════════════════════════════════
    # 政协 (Political Consultative Conference)
    # ════════════════════════════════════════

    # 19. 陈玉宝 — 政协主席
    {
        "id": 19,
        "name": "陈玉宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协主席",
        "current_org": "政协桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100856/ldzc.shtml",
    },
    # 20. 于杰 — 政协副主席
    {
        "id": 20,
        "name": "于杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协副主席",
        "current_org": "政协桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100856/ldzc.shtml",
    },
    # 21. 张跃军 — 政协副主席
    {
        "id": 21,
        "name": "张跃军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协副主席",
        "current_org": "政协桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100856/ldzc.shtml",
    },
    # 22. 夏士忠 — 政协副主席
    {
        "id": 22,
        "name": "夏士忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协副主席",
        "current_org": "政协桃山区委员会",
        "source": "http://www.hljtsq.gov.cn/hljtsq/c100856/ldzc.shtml",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共桃山区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共七台河市委员会",
        "location": "黑龙江省七台河市桃山区",
    },
    {
        "id": 2,
        "name": "桃山区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "七台河市人民政府",
        "location": "黑龙江省七台河市桃山区",
    },
    {
        "id": 3,
        "name": "桃山区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "七台河市人大常委会",
        "location": "黑龙江省七台河市桃山区",
    },
    {
        "id": 4,
        "name": "政协桃山区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协七台河市委员会",
        "location": "黑龙江省七台河市桃山区",
    },
    {
        "id": 5,
        "name": "桃山区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共七台河市纪律检查委员会",
        "location": "黑龙江省七台河市桃山区",
    },
    {
        "id": 6,
        "name": "七台河市公安局桃山分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "桃山区人民政府",
        "location": "黑龙江省七台河市桃山区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 魏锟 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-07-24 (官网简历于2021-08-16发布)"},
    # 张玉 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-07-24 (官网简历于2022-01-10发布)"},

    # ── 区委领导 ──
    # 李荣美 - 区委副书记、政法委书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "兼任政法委书记"},
    {"person_id": 3, "org_id": 1, "title": "政法委书记", "start": "", "end": "present",
     "rank": "副处级", "note": "由区委副书记兼任"},
    # 秦刚 - 区纪委书记
    {"person_id": 4, "org_id": 5, "title": "区纪委书记", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任; 同时任监委主任"},
    # 李海峰 - 组织部部长
    {"person_id": 5, "org_id": 1, "title": "组织部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},
    # 董哲 - 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},
    # 刘明磊 - 宣传部部长、统战部部长
    {"person_id": 7, "org_id": 1, "title": "宣传部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任; 兼统战部部长"},
    # 刘国胜 - 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任; 区政府党组成员"},
    # 李铭 - 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},

    # ── 政府领导 ──
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "兼桃山公安分局局长、党委书记; 区政府党组成员"},
    {"person_id": 11, "org_id": 6, "title": "分局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "桃山公安分局局长、党委书记"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区政府党组成员"},

    # ── 人大领导 ──
    {"person_id": 14, "org_id": 3, "title": "人大常委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": "党组书记"},
    {"person_id": 15, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": "党组成员"},
    {"person_id": 17, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": "党组成员"},
    {"person_id": 18, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": "党组成员"},

    # ── 政协领导 ──
    {"person_id": 19, "org_id": 4, "title": "政协主席", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "政协副主席", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "政协副主席", "start": "", "end": "present",
     "rank": "副处级", "note": "党组成员"},
    {"person_id": 22, "org_id": 4, "title": "政协副主席", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 魏锟 <-> 张玉: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 共同负责桃山区全面工作",
     "overlap_org": "中共桃山区委员会/桃山区人民政府",
     "overlap_period": "截至2026年7月"},

    # 魏锟 <-> 李荣美: 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与专职副书记; 区委领导班子搭档",
     "overlap_org": "中共桃山区委员会",
     "overlap_period": "截至2026年7月"},

    # 张玉 <-> 董哲: 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与常务副区长工作搭档",
     "overlap_org": "桃山区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张玉 <-> 于涛: 区长与副区长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "桃山区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张玉 <-> 韩炜: 区长与副区长
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "桃山区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张玉 <-> 刘国鑫: 区长与副区长
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "桃山区人民政府",
     "overlap_period": "截至2026年7月"},

    # 区委常委会成员间的工作关系 (常委间)
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与纪委书记; 区委常委会搭档",
     "overlap_org": "中共桃山区委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与组织部部长; 区委常委会搭档",
     "overlap_org": "中共桃山区委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与宣传部部长; 区委常委会搭档",
     "overlap_org": "中共桃山区委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委书记与区委常委副区长; 区委常委会搭档",
     "overlap_org": "中共桃山区委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "区委书记与区委常委副区长; 区委常委会搭档",
     "overlap_org": "中共桃山区委员会",
     "overlap_period": "截至2026年7月"},

    # 人大、政协与区委区政府主要领导
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "区委书记与人大常委会主任; 四套班子主要领导",
     "overlap_org": "桃山区",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "context": "区委书记与政协主席; 四套班子主要领导",
     "overlap_org": "桃山区",
     "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "区长与人大常委会主任; 四套班子主要领导",
     "overlap_org": "桃山区",
     "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 19, "type": "overlap",
     "context": "区长与政协主席; 四套班子主要领导",
     "overlap_org": "桃山区",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "桃山区人民政府官网-领导之窗-中共桃山区委员会",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/ldzc.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委领导完整名册",
        },
        {
            "id": "S002",
            "title": "桃山区人民政府官网-领导之窗-桃山区人民政府",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区政府领导完整名册",
        },
        {
            "id": "S003",
            "title": "桃山区人民政府官网-领导之窗-桃山区人大常委会",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100854/ldzc.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "人大常委会领导名册",
        },
        {
            "id": "S004",
            "title": "桃山区人民政府官网-领导之窗-政协桃山区委员会",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100856/ldzc.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "政协领导名册",
        },
        {
            "id": "S005",
            "title": "桃山区人民政府官网-魏锟个人简历页",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202108/f116d1a185694761a616212f8ba18689.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "2021-08-16",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "魏锟: 男，汉族，1973年7月生，硕士研究生学历，中共党员",
        },
        {
            "id": "S006",
            "title": "桃山区人民政府官网-张玉个人简历页",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202201/94e9f50afdb4459e9e5044d298e40a48.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "2022-01-10",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "张玉: 女，汉族，1972年7月生，研究生学历，中共党员",
        },
        {
            "id": "S007",
            "title": "桃山区人民政府官网-李荣美个人简历页",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202606/44a19b22071c48dca363fd2496f24c42.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "2026-06-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "李荣美: 女，汉族，1984年8月生，大学学历，中共党员",
        },
        {
            "id": "S008",
            "title": "桃山区人民政府官网-秦刚个人简历页",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202204/6b0b21dbc97b428285411287151fe903.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "2022-04-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "秦刚: 男，汉族，1980年11月生，大学学历，中共党员",
        },
        {
            "id": "S009",
            "title": "桃山区人民政府官网-李海峰个人简历页",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202312/b246f2f4f8a543cd98d918fd9f423679.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "李海峰: 男，汉族，1978年3月生，大学学历，中共党员",
        },
        {
            "id": "S010",
            "title": "桃山区人民政府官网-董哲个人简历页",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202312/bf5a71f4cef34546967cc2fc0be3f142.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "董哲: 男，汉族，1987年9月生，研究生学历，中共党员",
        },
        {
            "id": "S011",
            "title": "桃山区人民政府官网-刘明磊个人简历页",
            "url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202410/4cea2fff8c9c41bba0ba3d47cdc17984.shtml",
            "publisher": "七台河市桃山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "刘明磊: 男，汉族，1988年3月生，大学学历，中共党员",
        },
        {
            "id": "S012",
            "title": "Wikipedia-七台河市",
            "url": "https://zh.wikipedia.org/wiki/七台河市",
            "publisher": "Wikipedia",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "七台河市行政区划信息和市领导信息",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"taoshan_{name}"

    # ── 魏锟 (区委书记) ──
    if name == "魏锟":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "七台河市",
                "region": "桃山区",
                "job": "区委书记",
                "task_id": "heilongjiang_桃山区",
                "time_focus": "2021–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "魏锟",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1973年7月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "硕士研究生",
                     "study_type": "unknown", "source_ids": ["S005"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "魏锟_197307",
                    "name_birthplace": "魏锟_",
                    "official_profile_url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202108/f116d1a185694761a616212f8ba18689.shtml",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共桃山区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S005"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共桃山区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "黑龙江省七台河市桃山区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任; 官网简历于2021-08-16发布，表明至少自2021年起任职",
                    "confidence": "confirmed",
                    "source_ids": ["S005"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共桃山区委员会", "type": "党委",
                 "level": "县处级", "location": "黑龙江省七台河市桃山区"},
            ],
            "relationships": [
                {"person": "张玉", "person_id": "taoshan_张玉",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共桃山区委员会/桃山区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
                {"person": "李荣美", "person_id": "taoshan_李荣美",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区委书记与专职副书记",
                 "overlap_org": "中共桃山区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "刘永辉", "person_id": "taoshan_刘永辉",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与人大常委会主任; 四套班子主要领导",
                 "overlap_org": "桃山区",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "陈玉宝", "person_id": "taoshan_陈玉宝",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与政协主席; 四套班子主要领导",
                 "overlap_org": "桃山区",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "low_profile",
                        "evidence": "无公开新闻报道可确认其具体工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "完整履历：魏锟任区委书记前的教育背景（具体院校/专业）和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "魏锟的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["魏锟 简历 桃山区", "魏锟 出生 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "魏锟何时开始担任桃山区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["魏锟 任 桃山区 区委书记", "魏锟 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "魏锟的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["魏锟 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 张玉 (区长) ──
    if name == "张玉":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "七台河市",
                "region": "桃山区",
                "job": "区长",
                "task_id": "heilongjiang_桃山区",
                "time_focus": "2021–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "张玉",
                "aliases": [],
                "gender": "女",
                "ethnicity": "汉族",
                "birth": "1972年7月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "研究生",
                     "study_type": "unknown", "source_ids": ["S006"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张玉_197207",
                    "name_birthplace": "张玉_",
                    "official_profile_url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202201/94e9f50afdb4459e9e5044d298e40a48.shtml",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "桃山区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S006"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "桃山区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "黑龙江省七台河市桃山区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任; 官网简历于2022-01-10发布",
                    "confidence": "confirmed",
                    "source_ids": ["S006"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "桃山区人民政府", "type": "政府",
                 "level": "县处级", "location": "黑龙江省七台河市桃山区"},
            ],
            "relationships": [
                {"person": "魏锟", "person_id": "taoshan_魏锟",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共桃山区委员会/桃山区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
                {"person": "董哲", "person_id": "taoshan_董哲",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与常务副区长工作搭档",
                 "overlap_org": "桃山区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "刘国胜", "person_id": "taoshan_刘国胜",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长工作搭档",
                 "overlap_org": "桃山区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "刘永辉", "person_id": "taoshan_刘永辉",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区长与人大常委会主任; 四套班子主要领导",
                 "overlap_org": "桃山区",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "low_profile",
                        "evidence": "无公开新闻报道可确认其具体工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "完整履历：张玉任区长前的教育背景（具体院校/专业）和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "张玉的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["张玉 简历 桃山区", "张玉 女 区长 七台河"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "张玉何时开始担任桃山区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["张玉 任 桃山区 区长", "张玉 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "张玉的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["张玉 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 李荣美 (区委副书记) ──
    if name == "李荣美":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "七台河市",
                "region": "桃山区",
                "job": "区委副书记、政法委书记",
                "task_id": "heilongjiang_桃山区",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "李荣美",
                "aliases": [],
                "gender": "女",
                "ethnicity": "汉族",
                "birth": "1984年8月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "大学",
                     "study_type": "unknown", "source_ids": ["S007"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "李荣美_198408",
                    "name_birthplace": "李荣美_",
                    "official_profile_url": "http://www.hljtsq.gov.cn/hljtsq/c100853/202606/44a19b22071c48dca363fd2496f24c42.shtml",
                },
            },
            "current_status": {
                "current_post": "区委副书记、政法委书记",
                "current_org": "中共桃山区委员会",
                "administrative_rank": "副处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S007"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共桃山区委员会",
                    "title": "区委副书记、政法委书记",
                    "level": "副处级",
                    "location": "黑龙江省七台河市桃山区",
                    "system": "party",
                    "rank": "副处级",
                    "is_key_promotion": True,
                    "notes": "官网简历于2026-06-24发布",
                    "confidence": "confirmed",
                    "source_ids": ["S007"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共桃山区委员会", "type": "党委",
                 "level": "县处级", "location": "黑龙江省七台河市桃山区"},
            ],
            "relationships": [
                {"person": "魏锟", "person_id": "taoshan_魏锟",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区委副书记与区委书记",
                 "overlap_org": "中共桃山区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "公开源不足", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": "",
                 "confidence": "unverified", "source_ids": []}
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "李荣美完整履历未知",
            },
            "open_questions": [
                {"priority": "high", "question": "李荣美的籍贯、毕业院校和此前任职经历？",
                 "why_it_matters": "档案建库基础信息",
                 "suggested_queries": ["李荣美 简历 桃山区"],
                 "last_attempted": AS_OF},
            ],
        }

    # ── Default for other leaders ──
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "七台河市",
            "region": "桃山区",
            "job": job,
            "task_id": "heilongjiang_桃山区",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": person_id_str,
            "name": name,
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "http://www.hljtsq.gov.cn/hljtsq/c100855/ldzc.shtml",
            },
        },
        "current_status": {
            "current_post": job,
            "current_org": "桃山区人民政府" if "副" in job else "中共桃山区委员会",
            "administrative_rank": "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002"],
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "present",
                "org": "桃山区",
                "title": job,
                "level": "副处级",
                "location": "黑龙江省七台河市桃山区",
                "system": "government",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": "截至2026年7月在任; 公开来源未显示详细履历",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ],
        "organizations": [
            {"org_id": 2, "name": "桃山区人民政府", "type": "政府",
             "level": "县处级", "location": "黑龙江省七台河市桃山区"},
        ],
        "relationships": [
            {"person": "张玉", "person_id": "taoshan_张玉",
             "relationship_type": "superior_subordinate", "strength": "medium",
             "evidence": "副区长与区长工作搭档",
             "overlap_org": "桃山区人民政府",
             "overlap_period": "截至2026年7月",
             "direction": "undirected", "confidence": "confirmed",
             "source_ids": ["S002"]},
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "公开源不足", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现负面信息", "date": "",
             "confidence": "unverified", "source_ids": []}
        ],
        "source_register": make_source_register(),
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整履历未知",
        },
        "open_questions": [
            {"priority": "high", "question": f"{name}的出生年月、籍贯和完整履历？",
             "why_it_matters": "档案建库基础信息",
             "suggested_queries": [f"{name} 简历 桃山区"],
             "last_attempted": AS_OF},
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network database and GEXF...")
    print(f"  Staging dir: {_STAGING_DIR}")
    print(f"  AS_OF: {AS_OF}")
    print()

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # ── Person JSONs ──
    person_files = []
    person_records = [
        ("区委书记", "魏锟"),
        ("区长", "张玉"),
        ("区委副书记", "李荣美"),
        ("常委副区长", "董哲"),
        ("纪委书记", "秦刚"),
    ]
    for job, name in person_records:
        fname = f"{TODAY}-黑龙江省-七台河市-{job}-{name}.json"
        person_path = _STAGING_DIR / fname
        person_json = generate_person_json(job, name)
        with open(person_path, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        person_files.append(str(person_path))
        print(f"  Person JSON: {person_path.name}")

    db_path = str(DB_PATH)
    gexf_path = str(GEXF_PATH)
    print()
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    for pf in person_files:
        print(f"  JSON: {pf}")
    print("Done.")


if __name__ == "__main__":
    main()
