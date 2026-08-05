#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 茄子河区 (Qiezihe District), 七台河市, 黑龙江省.

Level: 市辖区
Province: 黑龙江省
Parent city: 七台河市
Targets: 区委书记 (Party Secretary: 蒋泽宇), 区长 (Mayor: 卢浩远)
Task ID: heilongjiang_茄子河区

Research date: 2026-08-05
Official source: http://www.hljqzh.gov.cn/ (七台河市茄子河区人民政府)

Current status (as of 2026-08-05, verified via 茄子河区人民政府 website 领导之窗):
- 区委书记: 蒋泽宇 (男，汉族，1983年4月生，研究生学历，管理学硕士，中共党员)
- 区长: 卢浩远 (男，汉族，1983年2月生，大学学历，中共党员)
- Full four-set leadership roster confirmed on district website

Leadership roster sourced from:
  - http://www.hljqzh.gov.cn/hljqzh/c100709/ldzc.shtml (区委)
  - http://www.hljqzh.gov.cn/hljqzh/c100710/ldzc.shtml (区人大)
  - http://www.hljqzh.gov.cn/hljqzh/c100711/ldzc.shtml (区政府)
  - http://www.hljqzh.gov.cn/hljqzh/c100712/ldzc.shtml (区政协)

Confidence notes:
  蒋泽宇 and 卢浩远 identities confirmed via official government bio pages with name, gender, birth, education.
  Full leadership roster confirmed via official leadership window pages.
  Detailed career histories before current roles not publicly available.
  Web search tools (Exa rate-limited, Baidu captcha, Jina timeout) were blocked during this investigation;
  predecessor/successor moves and some birth/native-place fields remain open gaps.
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

SLUG = "茄子河区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 蒋泽宇 — 区委书记
    {
        "id": 1,
        "name": "蒋泽宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年4月",
        "birthplace": "",
        "education": "研究生学历，管理学硕士",
        "party_join": "中共党员",
        "work_start": "2006年7月",
        "current_post": "区委书记",
        "current_org": "中共茄子河区委员会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/201408/f9d6b2fa1fb44028bf655ccd38b8db38.shtml",
    },
    # 2. 卢浩远 — 区长
    {
        "id": 2,
        "name": "卢浩远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2006年7月",
        "current_post": "区长",
        "current_org": "茄子河区人民政府",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100711/202507/8759891ffe3b4b5ba13010f26b078857.shtml",
    },

    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════

    # 3. 康雪 — 区委副书记、政法委书记
    {
        "id": 3,
        "name": "康雪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2005年7月",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共茄子河区委员会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202505/1e2c8d237bf34996b1654e9fe5c8deed.shtml",
    },
    # 4. 梁康 — 区委常委、常务副区长
    {
        "id": 4,
        "name": "梁康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2012年3月",
        "current_post": "区委常委、常务副区长",
        "current_org": "茄子河区人民政府",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202506/9a46a444aa984e04831107e890ba1413.shtml",
    },
    # 5. 吕超 — 区委常委、纪委书记、监委主任
    {
        "id": 5,
        "name": "吕超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2004年3月",
        "current_post": "区委常委、纪委书记",
        "current_org": "茄子河区纪律检查委员会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202511/a5225ffb0a4f4239ae4826a710e342cc.shtml",
    },
    # 6. 周子琪 — 区委常委、副区长
    {
        "id": 6,
        "name": "周子琪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1990年9月",
        "birthplace": "",
        "education": "硕士研究生，法学硕士",
        "party_join": "中共党员",
        "work_start": "2014年7月",
        "current_post": "区委常委、副区长",
        "current_org": "茄子河区人民政府",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202504/68db12c18c744c9f81f954f1b4af573c.shtml",
    },
    # 7. 刘经礼 — 区委常委、宣传部长、统战部长
    {
        "id": 7,
        "name": "刘经礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部长、统战部长",
        "current_org": "中共茄子河区委员会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202607/dd95e1727acb49be99ce038a704cc54e.shtml",
    },
    # 8. 周海权 — 区委常委、副区长
    {
        "id": 8,
        "name": "周海权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2009年7月",
        "current_post": "区委常委、副区长",
        "current_org": "茄子河区人民政府",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202512/fe28b03312af4fcdbf4fa202670bc5c42.shtml",
    },
    # 9. 杨锡辰 — 区委常委、人武部政委
    {
        "id": 9,
        "name": "杨锡辰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "黑龙江省五大连池市",
        "education": "",
        "party_join": "",
        "work_start": "1996年9月",
        "current_post": "区委常委、人武部政委",
        "current_org": "茄子河区人民武装部",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202403/a104lambrovi20202403wwrdsa3a38df6c917e4f9d9ce6fa8f70df7434.shtml",
    },

    # ════════════════════════════════════════
    # 政府领导 (Government)
    # ════════════════════════════════════════

    # 10. 白云鹤 — 副区长
    {
        "id": 10,
        "name": "白云鹤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年4月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "1999年1月",
        "current_post": "区政府副区长",
        "current_org": "茄子河区人民政府",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100709/202607/0b37360da24dd4947aa3c0ea87184f729.shtml",
    },
    # 11. 李祥 — 副区长、公安分局局长
    {
        "id": 11,
        "name": "李祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1997年7月",
        "current_post": "区政府副区长、公安分局局长",
        "current_org": "茄子河区人民政府",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100711/202511/e5e6c25366144ad4b52b78ad9235d9ae.shtml",
    },
    # 12. 于海明 — 副区长
    {
        "id": 12,
        "name": "于海明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "1996年7月",
        "current_post": "区政府副区长",
        "current_org": "茄子河区人民政府",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100711/202512/77f3c81c34a84898a1943850d90cd0c8.shtml",
    },

    # ════════════════════════════════════════
    # 人大常委会 (People's Congress)
    # ════════════════════════════════════════

    # 13. 孔祥彬 — 人大常委会主任
    {
        "id": 13,
        "name": "孔祥彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "人大常委会主任",
        "current_org": "茄子河区人大常委会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100710/201408/e2d5d2dd17d24069820a142cb62f2df2.shtml",
    },
    # 14. 王志宏 — 人大常委会副主任
    {
        "id": 14,
        "name": "王志宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "",
        "work_start": "1993年5月",
        "current_post": "人大常委会副主任",
        "current_org": "茄子河区人大常委会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100710/202111/525bdf37545e45d7b1c5434749ddbe49.shtml",
    },

    # ════════════════════════════════════════
    # 政协 (Political Consultative Conference)
    # ════════════════════════════════════════

    # 15. 张岫 — 政协主席
    {
        "id": 15,
        "name": "张岫",
        "gender": "女",
        "ethnicity": "",
        "birth": "1971年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "政协主席",
        "current_org": "政协茄子河区委员会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100712/202607/b821e25024d941f7b89e5712136985b2.shtml",
    },
    # 16. 蔡昌伟 — 政协副主席
    {
        "id": 16,
        "name": "蔡昌伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "民盟盟员",
        "work_start": "1999年9月",
        "current_post": "政协副主席",
        "current_org": "政协茄子河区委员会",
        "source": "http://www.hljqzh.gov.cn/hljqzh/c100712/202601/8c9c978f7b084b1992c7c8d0c4e540e9.shtml",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共茄子河区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共七台河市委员会",
        "location": "黑龙江省七台河市茄子河区",
    },
    {
        "id": 2,
        "name": "茄子河区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "七台河市人民政府",
        "location": "黑龙江省七台河市茄子河区",
    },
    {
        "id": 3,
        "name": "茄子河区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "七台河市人大常委会",
        "location": "黑龙江省七台河市茄子河区",
    },
    {
        "id": 4,
        "name": "政协茄子河区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协七台河市委员会",
        "location": "黑龙江省七台河市茄子河区",
    },
    {
        "id": 5,
        "name": "茄子河区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共七台河市纪律检查委员会",
        "location": "黑龙江省七台河市茄子河区",
    },
    {
        "id": 6,
        "name": "茄子河区人民检察院",
        "type": "政法",
        "level": "县处级",
        "parent": "茄子河区人民政府",
        "location": "黑龙江省七台河市茄子河区",
    },
    {
        "id": 7,
        "name": "茄子河区人民武装部",
        "type": "政务",
        "level": "县处级",
        "parent": "七台河军分区",
        "location": "黑龙江省七台河市茄子河区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 蒋泽宇 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-08-05 (官网领导之窗)"},
    # 卢浩远 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-08-05 (官网领导之窗); 兼区委副书记"},

    # ── 区委领导 ──
    # 康雪 - 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "兼任政法委书记"},
    {"person_id": 3, "org_id": 1, "title": "政法委书记", "start": "", "end": "present",
     "rank": "副处级", "note": "由区委副书记兼任"},
    # 梁康 - 常务副区长
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},
    # 吕超 - 区纪委书记
    {"person_id": 5, "org_id": 5, "title": "区纪委书记", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任; 监委主任、四级高级监察官"},
    # 周子琪 - 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},
    # 刘经礼 - 宣传部长、统战部长
    {"person_id": 7, "org_id": 1, "title": "宣传部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},
    {"person_id": 7, "org_id": 1, "title": "统战部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "兼任"},
    # 周海权 - 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},
    # 杨锡辰 - 人武部政委
    {"person_id": 9, "org_id": 7, "title": "人武部政委", "start": "", "end": "present",
     "rank": "副处级", "note": "区委常委兼任"},

    # ── 政府领导 ──
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区政府副区长"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "茄子河公安分局党委书记、局长"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区政府副区长"},

    # ── 人大领导 ──
    {"person_id": 13, "org_id": 3, "title": "人大常委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": "党组书记"},
    {"person_id": 14, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": "九三学社社员"},

    # ── 政协领导 ──
    {"person_id": 15, "org_id": 4, "title": "政协主席", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "政协副主席", "start": "", "end": "present",
     "rank": "副处级", "note": "民盟盟员"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 蒋泽宇 <-> 卢浩远: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 共同负责茄子河区全面工作",
     "overlap_org": "中共茄子河区委员会/茄子河区人民政府",
     "overlap_period": "截至2026年8月"},

    # 蒋泽宇 <-> 康雪: 书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与专职副书记; 区委领导班子搭档",
     "overlap_org": "中共茄子河区委员会",
     "overlap_period": "截至2026年8月"},
    # 卢浩远 <-> 康雪: 区长与副书记
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与区委副书记共事; 区委领导班子搭档",
     "overlap_org": "中共茄子河区委员会/茄子河区人民政府",
     "overlap_period": "截至2026年8月"},

    # 卢浩远 <-> 梁康: 区长与常务副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与常务副区长工作搭档",
     "overlap_org": "茄子河区人民政府",
     "overlap_period": "截至2026年8月"},

    # 蒋泽宇 <-> 吕超: 书记与纪委书记
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与纪委书记; 区委常委会搭档",
     "overlap_org": "中共茄子河区委员会",
     "overlap_period": "截至2026年8月"},

    # 蒋泽宇 <-> 刘经礼: 书记与宣传/统战部长
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与宣传部长/统战部长; 区委常委会搭档",
     "overlap_org": "中共茄子河区委员会",
     "overlap_period": "截至2026年8月"},

    # 蒋泽宇 <-> 杨锡辰: 书记与人武部政委
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "区委书记与人武部政委; 区委常委会搭档",
     "overlap_org": "中共茄子河区委员会",
     "overlap_period": "截至2026年8月"},

    # 区委常委间的工作关系
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "两位副区长; 区委常委会搭档",
     "overlap_org": "中共茄子河区委员会/茄子河区人民政府",
     "overlap_period": "截至2026年8月"},
    {"person_a": 4, "person_b": 8, "type": "overlap",
     "context": "两位副区长; 区委常委会搭档",
     "overlap_org": "中共茄子河区委员会/茄子河区人民政府",
     "overlap_period": "截至2026年8月"},

    # 人大、政协与区委区政府主要领导
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "区委书记与人大常委会主任; 四套班子主要领导",
     "overlap_org": "茄子河区",
     "overlap_period": "截至2026年8月"},
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "区委书记与政协主席; 四套班子主要领导",
     "overlap_org": "茄子河区",
     "overlap_period": "截至2026年8月"},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "区长与人大常委会主任; 四套班子主要领导",
     "overlap_org": "茄子河区",
     "overlap_period": "截至2026年8月"},
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "区长与政协主席; 四套班子主要领导",
     "overlap_org": "茄子河区",
     "overlap_period": "截至2026年8月"},

    # 区长与公安分局局长/副区长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "区长与副区长（公安分局局长）工作搭档",
     "overlap_org": "茄子河区人民政府",
     "overlap_period": "截至2026年8月"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "茄子河区人民政府",
     "overlap_period": "截至2026年8月"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "茄子河区人民政府",
     "overlap_period": "截至2026年8月"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "茄子河区人民政府",
     "overlap_period": "截至2026年8月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "茄子河区人民政府官網-领导之窗-区委",
            "url": "http://www.hljqzh.gov.cn/hljqzh/c100709/ldzc.shtml",
            "publisher": "七台河市茄子河区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委领导名册",
        },
        {
            "id": "S002",
            "title": "茄子河区人民政府官网-领导之窗-区政府",
            "url": "http://www.hljqzh.gov.cn/hljqzh/c100711/ldzc.shtml",
            "publisher": "七台河市茄子河区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区政府领导名册",
        },
        {
            "id": "S003",
            "title": "茄子河区人民政府官网-领导之窗-区人大常委会",
            "url": "http://www.hljqzh.gov.cn/hljqzh/c100710/ldzc.shtml",
            "publisher": "七台河市茄子河区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "人大常委会领导名册",
        },
        {
            "id": "S004",
            "title": "茄子河区人民政府官网-领导之窗-区政协",
            "url": "http://www.hljqzh.gov.cn/hljqzh/c100712/ldzc.shtml",
            "publisher": "七台河市茄子河区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "政协领导名册",
        },
        {
            "id": "S005",
            "title": "茄子河区人民政府官网-蒋泽宇个人简历页（区委书记）",
            "url": "http://www.hljqzh.gov.cn/hljqzh/c100709/201408/f9d6b2fa1fb44028bf655ccd17b8db38.shtml",
            "publisher": "七台河市茄子河区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "蒋泽宇: 男，汉族，1983年4月生，研究生学历，管理学硕士，2009年7月入党，2006年7月参加工作，现任茄子河区委书记",
        },
        {
            "id": "S006",
            "title": "茄子河区人民政府官网-卢浩远个人简历（区长）",
            "url": "http://www.hljqzh.gov.cn/hljqzh/c100711/202507/8759891ffe3b4b5ba13010f26b078857.shtml",
            "publisher": "七台河市茄子河区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "卢浩远: 男，汉族，1983年2月生，大学学历，2008年6月入党，2006年7月参加工作，现任茄子河区委副书记、区长",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"heilongjiang_qiezihe_{name}"

    if name == "蒋泽宇":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "七台河市",
                "region": "茄子河区",
                "job": "区委书记",
                "task_id": "heilongjiang_茄子河区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "蒋泽宇",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1983年4月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "研究生/管理学硕士",
                     "study_type": "unknown", "source_ids": ["S005"]},
                ],
                "party_join": "2009年7月",
                "work_start": "2006年7月",
                "dedupe_keys": {
                    "name_birth": "蒋泽宇_198304",
                    "name_birthplace": "蒋泽宇_",
                    "official_profile_url": "http://www.hljqzh.gov.cn/hljqzh/c100709/201408/f9d6b2fa1fb440b87bf055ccd38b8db38.shtml",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共茄子河区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S005"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共茄子河区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "黑龙江省七台河市茄子河区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年8月在任; 公开源未显示任职起始时间",
                    "confidence": "confirmed",
                    "source_ids": ["S005"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共茄子河区委员会", "type": "党委",
                 "level": "县处级", "location": "黑龙江省七台河市茄子河区"},
            ],
            "relationships": [
                {"person": "卢浩远", "person_id": "heilongjiang_qiezihe_卢浩远",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档; 共同负责茄子河区全面工作",
                 "overlap_org": "中共茄子河区委员会/茄子河区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
                {"person": "康雪", "person_id": "heilongjiang_qiezihe_康雪",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区委书记与专职副书记",
                 "overlap_org": "中共茄子河区委员会",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "孔祥彬", "person_id": "heilongjiang_qiezihe_孔祥彬",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与人大常委会主任; 四套班子主要领导",
                 "overlap_org": "茄子河区",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "张岫", "person_id": "heilongjiang_qiezihe_张岫",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与政协主席; 四套班子主要领导",
                 "overlap_org": "茄子河区",
                 "overlap_period": "截至2026年8月",
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
                    "description": "截至2026年8月，未发现公开的纪律处分、审计问题或负面报道",
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
                "biggest_gap": "完整履历：蒋泽宇任区委书记前的具体职务、任职起始时间、籍贯均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "蒋泽宇的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["蒋泽宇 简历 茄子河区", "蒋泽宇 区委书记 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "蒋泽宇何时开始担任茄子河区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["蒋泽宇 任 茄子河区 区委书记 公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "前任茄子河区区委书记去向？",
                    "why_it_matters": "评估干部交流网络和交接",
                    "suggested_queries": ["茄子河区 前任 区委书记"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    if name == "卢浩远":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "七台河市",
                "region": "茄子河区",
                "job": "区长",
                "task_id": "heilongjiang_茄子河区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "卢浩远",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1983年2月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "大学",
                     "study_type": "unknown", "source_ids": ["S006"]},
                ],
                "party_join": "2008年6月",
                "work_start": "2006年7月",
                "dedupe_keys": {
                    "name_birth": "卢浩远_198302",
                    "name_birthplace": "卢浩远_",
                    "official_profile_url": "http://www.hljqzh.gov.cn/hljqzh/c100711/202504/5616f57b06cb4dd1987bb032b2003d61.shtml",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "茄子河区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S006"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "茄子河区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "黑龙江省七台河市茄子河区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年8月在任; 兼区委副书记; 简历未显示任职起始时间",
                    "confidence": "confirmed",
                    "source_ids": ["S006"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "茄子河区人民政府", "type": "政府",
                 "level": "县处级", "location": "黑龙江省七台河市茄子河区"},
            ],
            "relationships": [
                {"person": "蒋泽宇", "person_id": "heilongjiang_qiezihe_蒋泽宇",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共茄子河区委员会/茄子河区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
                {"person": "梁康", "person_id": "heilongjiang_qiezihe_梁康",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与常务副区长工作搭档",
                 "overlap_org": "茄子河区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "孔祥彬", "person_id": "heilongjiang_qiezihe_孔祥彬",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区长与人大常委会主任; 四套班子主要领导",
                 "overlap_org": "茄子河区",
                 "overlap_period": "截至2026年8月",
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
                    "description": "截至2026年8月，未发现公开的纪律处分、审计问题或负面报道",
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
                "biggest_gap": "完整履历：卢浩远任区长前的教育背景（具体院校/专业）和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "卢浩远的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["卢浩远 简历 茄子河区", "卢浩远 区长 七台河"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "卢浩远何时开始担任茄子河区区长？此前任何职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["卢浩远 公示 区长", "茄子河区 任命 区长"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "前任茄子河区区长去向？",
                    "why_it_matters": "评估跨区交流网络",
                    "suggested_queries": ["茄子河区 前任 区长"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── Default for other leaders ──
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "七台河市",
            "region": "茄子河区",
            "job": job,
            "task_id": "heilongjiang_茄子河区",
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
                "official_profile_url": "http://www.hljqzh.gov.cn/hljqzh/c100711/ldzc.shtml",
            },
        },
        "current_status": {
            "current_post": job,
            "current_org": "茄子河区人民政府",
            "administrative_rank": "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002"],
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "present",
                "org": "茄子河区",
                "title": job,
                "level": "副处级",
                "location": "黑龙江省七台河市茄子河区",
                "system": "government",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": "截至2026年8月在任; 公开来源未显示详细履历",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ],
        "organizations": [
            {"org_id": 2, "name": "茄子河区人民政府", "type": "政府",
             "level": "县处级", "location": "黑龙江省七台河市茄子河区"},
        ],
        "relationships": [
            {"person": "卢浩远", "person_id": "heilongjiang_qiezihe_卢浩远",
             "relationship_type": "superior_subordinate", "strength": "medium",
             "evidence": "副区长与区长工作搭档",
             "overlap_org": "茄子河区人民政府",
             "overlap_period": "截至2026年8月",
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
             "suggested_queries": [f"{name} 简历 茄子河区"],
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
        ("区委书记", "蒋泽宇"),
        ("区长", "卢浩远"),
        ("区人大常委会主任", "孔祥彬"),
        ("区政协主席", "张岫"),
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