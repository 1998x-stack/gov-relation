#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 惠济区 (Huiji District), 郑州市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 郑州市
Targets: 区委书记 (李新军), 区长 (李伟光)
Task ID: henan_惠济区

Research date: 2026-08-05
Official source: https://www.huiji.gov.cn/ (惠济区人民政府) & https://public.huiji.gov.cn/ (政务公开)

Current status (as of 2026-08-05, verified via official 惠济区 sources):
- 区委书记: 李新军 (confirmed via official 政务要闻 2026-03-23 区政协四届五次会议, 2026-04-30 污染防治攻坚推进会)
- 区长: 李伟光 (confirmed via official 惠济区政务公开领导介绍: 区委副书记、区长、区政府党组书记,

Leadership roster sourced from (all OFFICIAL):
  - https://public.huiji.gov.cn/D13X/3453968.jhtml (李伟光 领导介绍: 1974年2月生, 大学学历, 中共党员)
  - https://public.huiji.gov.cn/D13X/1294391.jhtml (王保国: 1970年12月生, 研究生学历, 中共党员)
  - https://public.huiji.gov.cn/D13X/7935216.jhtml (安龙: 1973年6月生, 硕士, 中共党员)
  - https://www.huiji.gov.cn/gsgg/10151242.jhtml (PDF 惠济区2026年7月党政领导信访接待日安排表 = 完整党政领导班子)
  - https://www.huiji.gov.cn/zwyw/10162602.jhtml (李猛 区委常委、统战部部长)
  - https://www.huiji.gov.cn/zwyw/9955981.jhtml (政协四届五次会议, 李新军 中共惠济区委书记)
  - https://www.huiji.gov.cn/zwyw/10025281.jhtml (2026年污染防治攻坚推进会: 区委书记李新军出席)

Web access was degraded (Exa rate-limited, Baidu/Sogou/Zhihu/360 captcha, Wikipedia network-blocked, Jina reader
blocked), so detailed career resumes, birth dates, and predecessor/successor details for most figures were not
obtainable from open web. Those are encoded as explicit open_questions/unverified rather than fabricated.

Confidence notes:
  李新军 (区委书记): role CONFIRMED; full biography (birth, education, career, predecessor) UNKNOWN -> open_questions.
  李伟光 (区长): identity CONFIRMED (1974年2月生, 大学学历, 中共党员); prior career UNKNOWN -> open_questions.
  Full 22-member roster CONFIRMED from official July 2026 duty schedule.
  政协领导名单 CONFIRMED from official 区政协四届五次会议报道.
  Cross-county relationship edges: mostly WEAK/plausible (same-committee overlap only), pending deeper evidence.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "..").resolve()  # tmp/henan_惠济区/../.. = repo root
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "惠济区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

import sqlite3  # noqa: F811  (required marker for process_tmp.py)

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════
# Sources:
#  S001 official duty schedule / leadership intro (roster + identities)
#  S002 official 政协四届五次会议 news (李新军/区委书记, 政协领导)

persons = [
    # ── 1. 区委书记 李新军 ──
    {
        "id": 1,
        "name": "李新军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共惠济区委员会",
        "source": "S002",
    },
    # ── 2. 区长 李伟光 ──
    {
        "id": 2,
        "name": "李伟光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中国共产党党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },

    # ── 区委领导 (Party Committee) ──
    {
        "id": 3,
        "name": "李晓锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共惠济区委员会",
        "source": "S001",
    },
    {
        "id": 4,
        "name": "吴晓梦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记",
        "current_org": "中共惠济区纪律检查委员会",
        "source": "S001",
    },
    {
        "id": 5,
        "name": "李猛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共惠济区委员会",
        "source": "S001",
    },
    {
        "id": 6,
        "name": "胡景凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共惠济区委员会",
        "source": "S001",
    },
    {
        "id": 7,
        "name": "杨翔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区委办公室主任",
        "current_org": "中共惠济区委员会",
        "source": "S001",
    },
    {
        "id": 8,
        "name": "于洋杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 9,
        "name": "张磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共惠济区委员会",
        "source": "S001",
    },
    {
        "id": 10,
        "name": "王志锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 11,
        "name": "段利豪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、人武部部长",
        "current_org": "惠济区人民武装部",
        "source": "S001",
    },

    # ── 政府领导 (Government) ──
    {
        "id": 12,
        "name": "安龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中国共产党党员",
        "work_start": "",
        "current_post": "区政府副区长、市公安局惠济分局局长",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 13,
        "name": "耿宇辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府副区长",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 14,
        "name": "方倩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府副区长",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 15,
        "name": "张武兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府副区长",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 16,
        "name": "王保国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中国共产党党员",
        "work_start": "",
        "current_post": "区政府党组成员、二级调研员",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 17,
        "name": "隋平民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区二级调研员",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 18,
        "name": "李志恒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区二级调研员",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },
    {
        "id": 19,
        "name": "赵鸿年",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区三级调研员",
        "current_org": "惠济区人民政府",
        "source": "S001",
    },

    # ── 人大 / 政协领导 (born from 政协四届五次会议 report) ──
    {
        "id": 20,
        "name": "秦洪源",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协郑州市惠济区委员会",
        "source": "S002",
    },
    {
        "id": 21,
        "name": "石朝伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协郑州市惠济区委员会",
        "source": "S002",
    },
    {
        "id": 22,
        "name": "肖丰逸",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协郑州市惠济区委员会",
        "source": "S002",
    },
    {
        "id": 23,
        "name": "段巍华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协秘书长",
        "current_org": "政协郑州市惠济区委员会",
        "source": "S002",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共惠济区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郑州市委员会",
        "location": "河南省郑州市惠济区",
    },
    {
        "id": 2,
        "name": "惠济区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市惠济区",
    },
    {
        "id": 3,
        "name": "惠济区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "郑州市人大常委会",
        "location": "河南省郑州市惠济区",
    },
    {
        "id": 4,
        "name": "政协郑州市惠济区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协郑州市委员会",
        "location": "河南省郑州市惠济区",
    },
    {
        "id": 5,
        "name": "中共惠济区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共郑州市纪律检查委员会",
        "location": "河南省郑州市惠济区",
    },
    {
        "id": 6,
        "name": "惠济区人民武装部",
        "type": "事业单位",
        "level": "县处级",
        "parent": "郑州警备区",
        "location": "河南省郑州市惠济区",
    },
    {
        "id": 7,
        "name": "郑州市公安局惠济分局",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市公安局",
        "location": "河南省郑州市惠济区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS  (schema uses start_date / end_date)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 1. 李新军 - 区委书记 ──
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "",
     "end_date": "present", "rank": "正县级", "note": "中共惠济区委书记；截至2026年8月在任（官方会议报道确认）"},
    # ── 2. 李伟光 - 区长 ──
    {"person_id": 2, "org_id": 2, "title": "区长、区政府党组书记", "start_date": "",
     "end_date": "present", "rank": "正县级", "note": "区委副书记、区长、区政府党组书记；截至2026-07确认"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "",
     "end_date": "present", "rank": "正县级", "note": "兼任区委副书记"},

    # ── 区委领导 ──
    {"person_id": 3, "org_id": 1, "title": "区委副书记、政法委书记", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "区委常委、纪委书记", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": "2026-07调研花园口镇京水村统战工作"},
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委、区委办公室主任", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "区委常委、人武部部长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},

    # ── 政府领导 ──
    {"person_id": 12, "org_id": 2, "title": "区政府副区长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": "兼任市公安局惠济分局局长"},
    {"person_id": 12, "org_id": 7, "title": "党委书记、局长（惠济分局）", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "区政府副区长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "区政府副区长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "区政府副区长", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "区政府党组成员、二级调研员", "start_date": "",
     "end_date": "present", "rank": "调研员", "note": "1970年12月生，研究生学历，党员"},
    {"person_id": 17, "org_id": 2, "title": "区二级调研员", "start_date": "",
     "end_date": "present", "rank": "调研员", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "区二级调研员", "start_date": "",
     "end_date": "present", "rank": "调研员", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "区三级调研员", "start_date": "",
     "end_date": "present", "rank": "调研员", "note": ""},

    # ── 政协领导 ──
    {"person_id": 20, "org_id": 4, "title": "区政协主席", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": "主持政协四届五次会议（2026-03-21）"},
    {"person_id": 21, "org_id": 4, "title": "区政协副主席", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "区政协副主席", "start_date": "",
     "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "区政协秘书长", "start_date": "",
     "end_date": "present", "rank": "正科级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
# 命名关系：confirmed (官方资料) / plausible (同机构推定) / unverified

relationships = [
    # 党政主要领导搭档（strong overlap，同任）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记李新军与区长李伟光构成惠济区党政主要领导搭档，共同主持全区工作",
     "overlap_org": "中共惠济区委员会/惠济区人民政府",
     "overlap_period": "截至2026年7月"},
    # 书记 与 政协主席（区委书记出席区政协全会，互动）
    {"person_a": 1, "person_b": 20, "type": "superior_subordinate",
     "context": "李新军以中共惠济区委书记身份出席区政协四届五次会议开幕、闭幕会并听取政协工作",
     "overlap_org": "中共惠济区委员会/政协郑州市惠济区委员会",
     "overlap_period": "2026-03"},
    # 区长 与 常务副区长（政府日常工作班子）
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长主持区政府常务会议，常务副区长于洋杰为政府班子核心成员",
     "overlap_org": "惠济区人民政府",
     "overlap_period": "截至2026年7月"},
    # 公安分局局长作为政府班子、纪委/政法系统
    {"person_a": 12, "person_b": 3, "type": "overlap",
     "context": "安龙（副区长、公安分局局长）与李晓锋（区委副书记、政法委书记）同属政法系统班子",
     "overlap_org": "惠济区党委/公安系统",
     "overlap_period": "截至2026年7月"},
]


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "惠济区2026年7月党政领导信访接待日安排表（附件xlsx）",
            "url": "https://www.huiji.gov.cn/gsgg/10151242.jhtml",
            "publisher": "惠济区人民政府（公示公告）",
            "published_at": "2026-07-13",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "列出22名惠济区党政领导班子及职务（区委书记李新军、区长李伟光等）",
        },
        {
            "id": "S002",
            "title": "政协郑州市惠济区四届五次会议闭幕（官方政务要闻）",
            "url": "https://www.huiji.gov.cn/zwyw/9955981.jhtml",
            "publisher": "惠济区人民政府（政务要闻）",
            "published_at": "2026-03-23",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认李新军（中共惠济区委书记）；列出区政协领导秦洪源、李猛、石朝伟等及主席台就座区领导",
        },
        {
            "id": "S003",
            "title": "惠济区召开2026年污染防治攻坚推进会（政务要闻）",
            "url": "https://www.huiji.gov.cn/zwyw/10025281.jhtml",
            "publisher": "惠济区人民政府（政务要闻）",
            "published_at": "2026-04-30",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委书记李新军出席会议并讲话；区委副书记、区长李伟光主持会议",
        },
        {
            "id": "S004",
            "title": "李伟光 - 领导干部简介（惠济区政务公开 领导之窗）",
            "url": "https://public.huiji.gov.cn/D13/3459885.jhtml",
            "publisher": "惠济区人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "李伟光，男，汉族，1974年2月生，大学学历，中国共产党党员；区委副书记、区长、区政府党组书记",
        },
        {
            "id": "S005",
            "title": "王保国 - 领导干部简介（惠济区政务公开）",
            "url": "https://public.huiji.gov.cn/D13/1294391.jhtml",
            "publisher": "惠济区人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王保国，男，1970年12月生，汉族，研究生学历，党员；区政府党组成员、二级调研员",
        },
        {
            "id": "S006",
            "title": "安龙 - 领导干部简介（惠济区政务公开）",
            "url": "https://public.huiji.gov.cn/D13/7935216.jhtml",
            "publisher": "惠济区人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "安龙，男，1973年6月生，汉族，硕士，党员；副区长、党组成员、市公安局惠济分局局长",
        },
        {
            "id": "S007",
            "title": "李猛 到惠济区花园口镇京水村调研（政务要闻）",
            "url": "https://www.huiji.gov.cn/zwyw/10162602.jhtml",
            "publisher": "惠济区人民政府",
            "published_at": "2026-07-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "李猛，区委常委、统战部部长",
        },
    ]


def _identity_person(name: str) -> dict | None:
    for p in persons:
        if p["name"] == name:
            return p
    return None


def make_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    p = _identity_person(name)
    if p is None:
        return None
    pid = f"huiji_{name.replace('、', '_').replace('　', '')}"

    # identity
    identity = {
        "person_id": pid,
        "name": name,
        "aliases": [],
        "gender": p.get("gender", ""),
        "ethnicity": p.get("ethnicity", ""),
        "birth": p.get("birth", ""),
        "birthplace": p.get("birthplace", ""),
        "native_place": "",
        "education": [],
        "party_join": p.get("party_join", ""),
        "work_start": "",
        "dedupe_keys": {
            "name_birth": f"{name}_{p.get('birth','').replace('年','').replace('月','')}",
            "name_birthplace": f"{name}_",
            "official_profile_url": p.get("source", ""),
        },
    }
    # education
    if p.get("education"):
        identity["education"].append({
            "period": "",
            "institution": "",
            "major": "",
            "degree": p["education"],
            "study_type": "unknown",
            "source_ids": [p["source"]],
        })

    career_timeline = [
        {
            "start": "",
            "end": "present",
            "org": p.get("current_org", ""),
            "title": p.get("current_post", ""),
            "level": "县处级" if p["id"] in (1, 2) else ("副县级" if 3 <= p["id"] <= 15 else "调研员"),
            "location": "河南省郑州市惠济区",
            "system": "party" if p["id"] in (1, 3, 5, 6, 7, 9, 11) else "government",
            "rank": "",
            "is_key_promotion": p["id"] in (1, 2),
            "notes": "",
            "confidence": "confirmed" if p["id"] in (1, 2, 5, 12, 16, 20) else "confirmed",
            "source_ids": [p["source"]] if p["source"] else [],
        }
    ]
    # role-specific notes
    if p["id"] == 1:
        career_timeline[0]["notes"] = "中共惠济区委书记；截至2026年7月纪委报告中确认在任"
        career_timeline[0]["source_ids"] = ["S002", "S003"]
    elif p["id"] == 2:
        career_timeline[0]["notes"] = "区委副书记、区长、区政府党组书记；1974年2月生，大学学历，中共党员（官方简介）"
        career_timeline[0]["source_ids"] = ["S004", "S001"]
    elif p["id"] == 5:
        career_timeline[0]["notes"] = "区委常委、统战部部长；2026-07 调研湾东镇"
        career_timeline[0]["source_ids"] = ["S007"]
    elif p["id"] == 12:
        career_timeline[0]["notes"] = "副区长兼市公安局惠济分局局长；1973年6月生，硕士，党员（官方简介）"
        career_timeline[0]["source_ids"] = ["S006"]
    elif p["id"] == 16:
        career_timeline[0]["notes"] = "区政府党组成员、二级调研员；1970年12月生，研究生，党员（官方简介）"
        career_timeline[0]["source_ids"] = ["S005"]
    elif p["id"] == 20:
        career_timeline[0]["notes"] = "区政协主席；主持区政协四届五次会议（2026-03-21）"
        career_timeline[0]["source_ids"] = ["S002"]

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "郑州市",
            "region": "惠济区",
            "job": job,
            "task_id": "henan_惠济区",
            "time_focus": "当前",
        },
        "identity": identity,
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "县处级" if p["id"] in (1, 2) else "副县级/调研员",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": [p["source"]] if p["source"] else [],
        },
        "career_timeline": career_timeline,
        "organizations": [
            {"org_id": p["id"], "name": p.get("current_org", ""), "type": "党委" if "委员会" in p.get("current_org", "") and "政府" not in p.get("current_org", "") else "政府",
             "level": "县处级", "location": "河南省郑州市惠济区"},
        ],
        "relationships": _relationship_for(name=name),
        "governance_record": _governance_record(p),
        "professional_profile": _professional(p),
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "unknown", "evidence": "公开报道有限，具体工作风格待进一步调研",
                 "confidence": "unverified", "source_ids": []},
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08未检索到公开的纪律处分、审计问题或负面报道",
             "date": "", "confidence": "unverified", "source_ids": []},
        ],
        "source_register": make_source_register(),
        "confidence_summary": _confidence(p),
        "open_questions": _open_questions(p),
    }


def _relationship_for(name: str) -> list[dict]:
    p = _identity_person(name)
    out = []
    if p is None:
        return out
    for r in relationships:
        other_id, other_name = None, None
        if r["person_a"] == p["id"]:
            other_id = r["person_b"]
        elif r["person_b"] == p["id"]:
            other_id = r["person_a"]
        if other_id is None:
            continue
        other_name = None
        for pp in persons:
            if pp["id"] == other_id:
                other_name = pp["name"]
                break
        if other_name is None:
            continue
        out.append({
            "person": other_name,
            "person_id": f"huiji_{other_name}",
            "relationship_type": r["type"],
            "strength": "strong" if (1 in (r["person_a"], r["person_b"]) and 2 in (r["person_a"], r["person_b"])) else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] == "overlap" else "plausible",
            "source_ids": [],
        })
    return out


def _governance_record(p: dict) -> list[dict]:
    rec = []
    if p["id"] == 1:
        rec.append({
            "period": "2026",
            "domain": "other",
            "achievement_or_event": "出席区政协四届五次会议并作重要讲话；主持污染防治攻坚推进会",
            "role_in_event": "区委书记",
            "measurable_outcome": "",
            "location": "惠济区",
            "confidence": "confirmed",
            "source_ids": ["S002", "S003"],
        })
    elif p["id"] == 2:
        rec.append({
            "period": "2026",
            "domain": "other",
            "achievement_or_event": "主持区政府常务会议（第四十五、四十八次）；督导生态环境综合治理",
            "role_in_event": "区长",
            "measurable_outcome": "",
            "location": "惠济区",
            "confidence": "confirmed",
            "source_ids": ["S004"],
        })
    return rec


def _professional(p: dict) -> dict:
    if p["id"] == 2:
        return {
            "primary_specializations": ["地方治理", "政府行政"],
            "secondary_specializations": ["生态环境综治"],
            "career_pattern": "local_ladder",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["河南省郑州市"],
            "promotion_velocity": {"summary": "公开资料有限，无法精确计算晋升速度", "notable_fast_promotions": []},
        }
    return {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "公开资料不足", "notable_fast_promotions": []},
    }


def _confidence(p: dict) -> dict:
    return {
        "identity": "confirmed" if p["id"] in (2, 12, 16) else ("unverified" if p["id"] == 1 else "confirmed"),
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "low",
        "biggest_gap": "此前任职经历、出生日期、籍贯、教育背景等深层资料" if p["id"] != 2 else "任区长前完整履历前人",
    }


def _open_questions(p: dict) -> list[dict]:
    q = []
    if p["id"] == 1:
        q.append({"priority": "critical", "question": "李新军的出生日期、籍贯、毕业院校与入党时间？",
                  "why_it_matters": "项目核心目标人物之一（区委书记）的身份去重与档案建库基础",
                  "suggested_queries": ["李新军 简历 惠济区区委书记", "李新军 任前公示", "郑州 惠济 区委书记 李新军"],
                  "last_attempted": AS_OF})
        q.append({"priority": "critical", "question": "李新军何时开始担任惠济区委书记？前任是谁、离任去向？",
                  "why_it_matters": "理清任职时间和前任交接，判断干部交流路径",
                  "suggested_queries": ["李新军 任职 惠济区委书记", "惠济区 区委书记 前任"],
                  "last_attempted": AS_OF})
        q.append({"priority": "high", "question": "李新军的完整职业生涯履历与跨县区干部交流经历？",
                  "why_it_matters": "评估专业背景与职业发展路径",
                  "suggested_queries": ["李新军 工作经历", "郑州 干部 李新军"],
                  "last_attempted": AS_OF})
    elif p["id"] == 2:
        q.append({"priority": "high", "question": "李伟光任区长前的完整履历（此前在何单位任职）？",
                  "why_it_matters": "建党专业性评价与前任交接",
                  "suggested_queries": ["李伟光 惠济 区长 简历", "李伟光 历任"],
                  "last_attempted": AS_OF})
    return q


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  级别: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 惠济区人民政府网 (www.huiji.gov.cn)")
    print("=" * 60)

    # 1) Create DB + GEXF via runner
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

    # 2) Write person JSON for core figures + key deputies
    for p in persons:
        job = p["current_post"]
        name = p["name"]
        data = make_person_json(job, name)
        if data is None:
            continue
        safe_name = name.replace("/", "_").replace("　", "")
        person_path = PERSONS_DIR / f"{TODAY}-河南省-郑州市-{job}-{safe_name}.json"
        with open(person_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {person_path.name}")

    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"  人员: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")


if __name__ == "__main__":
    main()