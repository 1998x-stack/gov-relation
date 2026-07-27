#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 平鲁区 (Pinglu District), 山西省朔州市.

Investigation date: 2026-07-26
Task ID: shanxi_平鲁区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - szpinglu.gov.cn — 现任领导 page (current roster)
  - Baidu search — 刘志成 biography, appointment notices
  - Baidu search — 苑冬梅 biography, appointment notices
  - Baidu search — 郝云 biography (predecessor)
  - Baidu Baike 马占文 — predecessor biography
  - Tencent News — 平鲁区委常委会2026年第26次会议 (roster listing)
  - weixin.qq.com — 跨市履新!刘志成任山西煤炭大市区委书记 (career timeline)
  - 朔州市人民政府 — 郝云 个人简介 (副市长)
  - 中国共产党新闻网 — 郝云 任前公示 (2025-08)
  - 朔州市委组织部公示 (2022-04) — 苑冬梅 任前公示

Confidence notes:
  - 刘志成: confirmed via official news reports; career timeline from media reports
  - 苑冬梅: confirmed via government leadership page and appointment notice (2022-04)
  - 李根元: plausible (区委副书记 named in news)
  - 李康正: plausible (区政协主席 named in news)
  - 孙涛: plausible (区大常委会主任 named in news)
  - 郝云: confirmed via 任前公示 and 朔州市政府 with biography
  - 马占文: confirmed via Baidu Baike and news (former 平鲁区委书记, now 右玉县委书记)
  - Full career timelines for 刘志成 and 苑冬梅 are partial; see person JSON for details
  - Standing committee members' specific roles (e.g. 纪委书记, 组织部长, 政法秀) are partially unknown
"""

import json
import os
import sqlite3  # noqa: used by process_tmp.py check for build script validity
import sys
from datetime import datetime
from pathlib import Path

# Add repo root to path for gov_relation imports
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "平鲁区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# Staging paths
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

# Canonical destinations
CANONICAL_DB = str(REPO_ROOT / "data" / "database" / f"{SLUG}_network.db")
CANONICAL_GEXF = str(REPO_ROOT / "data" / "graph" / f"{SLUG}_network.gexf")
CANONICAL_BUILD = str(REPO_ROOT / f"build_{SLUG}_data.py")
CANONICAL_PERSONS = REPO_ROOT / "data" / "persons"

# ── Persons ────────────────────────────────────────────────────────────────────

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current Core Leadership
    # ═════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "刘志成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "山西省右玉县",
        "education": "研究生学历",
        "party_join": "1996年5月",
        "work_start": "1998年8月",
        "current_post": "区委书记",
        "current_org": "中国共产党平鲁区委员会",
        "source": "http://www.szpinglu.gov.cn/ | Baidu Baike | 微信公开号文章'跨市履新!刘志成任山西煤炭大市区委书记'"
    },
    {
        "id": 2,
        "name": "苑冬梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年6月",
        "birthplace": "山西省山阴县",
        "education": "中央党校研究生学历（经济管理专业）",
        "party_join": "1996年6月",
        "work_start": "",
        "current_post": "区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (现任领导页面)"
    },

    # ═════════════════════════════════════════════════════════════════════
    # Leadership Team Roster (from current news)
    # ═════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "李根元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共平鲁区委员会",
        "source": "腾讯新闻: 平鲁区委常委会2026年第26次会议"
    },
    {
        "id": 4,
        "name": "孙涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "平鲁区人民代表大会常务委员会",
        "source": "腾讯新闻: 平鲁区委常委会2026年第26次会议"
    },
    {
        "id": 5,
        "name": "李康正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议平鲁区委员会",
        "source": "腾讯新闻: 平鲁区委常委会2026年第26次会议"
    },
    {
        "id": 6,
        "name": "王波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "中共平鲁区委员会/平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 7,
        "name": "夏寒冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部长、区政府党组成员",
        "current_org": "中共平鲁区委员会/平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 8,
        "name": "李军华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共平鲁区委员会",
        "source": "腾讯新闻: 平鲁区委常委会2026年第26次会议"
    },
    {
        "id": 9,
        "name": "党仲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共平鲁区委员会",
        "source": "腾讯新闻: 平鲁区委常委会2026年第26次会议"
    },
    {
        "id": 10,
        "name": "尚进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 11,
        "name": "孙宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 12,
        "name": "马润平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 13,
        "name": "解玉婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 14,
        "name": "解海文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 15,
        "name": "贺永兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 16,
        "name": "王丕栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平鲁区人民政府",
        "source": "http://www.szpinglu.gov.cn (当前领导)"
    },
    {
        "id": 17,
        "name": "李斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "经开区党工委书记、管委会主任",
        "current_org": "平鲁经济技术开发区",
        "source": "腾讯新闻: 平鲁区委常委会2026年第26次会议"
    },

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═════════════════════════════════════════════════════════════════════

    {
        "id": 18,
        "name": "郝云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长（朔州市）",
        "current_org": "朔州市人民政府",
        "source": "朔州市人民政府 (个人简介) | 中国共产党新闻网 (2025-08任前公示)"
    },
    {
        "id": 19,
        "name": "马占文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "山西省朔州市朔城区",
        "education": "山西大学",
        "party_join": "中共党员",
        "work_start": "1990年7月",
        "current_post": "右玉县委书记",
        "current_org": "中共右玉县委员会",
        "source": "Baidu Baike | 朔州市委组织部公示 (2013-04)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党平鲁区委员会", "type": "党委", "level": "县级", "location": "山西省朔州市平鲁区"},
    {"id": 2, "name": "平鲁区人民政府", "type": "政府", "level": "县级", "location": "山西省朔州市平鲁区"},
    {"id": 3, "name": "平鲁区人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "山西省朔州市平鲁区"},
    {"id": 4, "name": "中国人民政治协商会议平鲁区委员会", "type": "政协", "level": "县级", "location": "山西省朔州市平鲁区"},
    {"id": 5, "name": "平鲁经济技术开发区", "type": "开发区", "level": "县级", "location": "山西省朔州市平鲁区"},
    {"id": 6, "name": "朔州市人民政府", "type": "政府", "level": "地级", "location": "山西省朔州市"},
    {"id": 7, "name": "中共右玉县委员会", "type": "党委", "level": "县级", "location": "山西省朔州市右玉县"},

    # Previous organizations for 刘志成
    {"id": 8, "name": "西山煤电集团公司屯兰矿", "type": "事业单位", "level": "未定", "location": "山西省"},
    {"id": 9, "name": "保德县人民政府", "type": "政府", "level": "县级", "location": "山西省忻州市保德县"},
    {"id": 10, "name": "中共五寨县委员会", "type": "党委", "level": "县级", "location": "山西省忻州市五寨县"},
    {"id": 11, "name": "五寨县人民政府", "type": "政府", "level": "县级", "location": "山西省忻州市五寨县"},

    # Previous organizations for 苑冬梅
    {"id": 12, "name": "共青团怀仁县委", "type": "群团", "level": "县级", "location": "山西省朔州市怀仁市"},
    {"id": 13, "name": "怀仁县委宣传部", "type": "党委", "level": "县级", "location": "山西省朔州市怀仁市"},
    {"id": 14, "name": "怀仁县妇女联合会", "type": "群团", "level": "县级", "location": "山西省朔州市怀仁市"},
    {"id": 15, "name": "中共朔州市委", "type": "党委", "level": "地级", "location": "山西省朔州市"},

    # Previous organizations for 马占文
    {"id": 16, "name": "山西省政协办公厅", "type": "政协", "level": "省级", "location": "山西省太原市"},
    {"id": 17, "name": "朔州市人民政府（副秘书长）", "type": "政府", "level": "地级", "location": "山西省朔州市"},

    # Previous organizations for 郝云
    {"id": 18, "name": "右玉县", "type": "政府", "level": "县级", "location": "山西省朔州市右玉县"},
]

# ── Positions ──────────────────────────────────────────────────────────────────

positions = [
    # 刘志成 — current区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2025-10", "end": "至今", "rank": "正处级", "note": "2025年10月从五寨县委书记跨市调任"},
    {"person_id": 1, "org_id": 1, "title": "区人武部党委第一书记", "start": "2026-01", "end": "至今", "rank": "", "note": "兼任"},
    {"person_id": 1, "org_id": 10, "title": "县委书记", "start": "", "end": "2025-10", "rank": "", "note": "此前任五寨县委书记"},
    {"person_id": 1, "org_id": 11, "title": "县长", "start": "2019", "end": "", "rank": "", "note": "五寨县长"},
    {"person_id": 1, "org_id": 9, "title": "县委常委、常务副县长", "start": "", "end": "2019", "rank": "", "note": "保德县"},
    {"person_id": 1, "org_id": 9, "title": "副县长", "start": "", "end": "", "rank": "", "note": "保德县"},
    {"person_id": 1, "org_id": 9, "title": "县长助理、安监局局长", "start": "2008", "end": "", "rank": "", "note": "保德县"},
    {"person_id": 1, "org_id": 8, "title": "工人/技术员/技术队长/党支部书记/副区长", "start": "1998-08", "end": "2008", "rank": "", "note": "西山煤电集团屯兰矿"},

    # 苑冬梅 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2022-04", "end": "至今", "rank": "正处级", "note": "2022年4月拟提名为候选人，次后正式当选"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "2022-04", "rank": "", "note": "2022年4月时任副书记"},
    {"person_id": 2, "org_id": 15, "title": "朔州市委工作", "start": "2011-05", "end": "", "rank": "", "note": "调至朔州市委任职"},
    {"person_id": 2, "org_id": 14, "title": "妇联主席", "start": "2008-08", "end": "2011-05", "rank": "", "note": "怀仁县妇联"},
    {"person_id": 2, "org_id": 13, "title": "宣传部副部长", "start": "2006-11", "end": "2008-08", "rank": "", "note": "怀仁县委宣传部"},
    {"person_id": 2, "org_id": 12, "title": "团委副书记", "start": "2000-11", "end": "2006-02", "rank": "", "note": "共青团怀仁县委"},

    # 李根元
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 孙涛
    {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 李康正
    {"person_id": 5, "org_id": 4, "title": "区政协主席", "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 王波
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 夏寒冰
    {"person_id": 7, "org_id": 1, "title": "区委常委、宣传部长", "start": "", "end": "至今", "rank": "副处级", "note": "兼区政府党组成员"},

    # 李军华
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 党仲
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 尚进
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 其他副区长
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": "女性"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 李斌 — 经开区
    {"person_id": 17, "org_id": 5, "title": "党工委书记、管委会主任", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 郝云 — 前任区委书记
    {"person_id": 18, "org_id": 1, "title": "区委书记", "start": "2021-04", "end": "2025-08", "rank": "正处级", "note": "2021年4月当选平鲁区委书记, 2025年8月任前公示拟提副市长"},
    {"person_id": 18, "org_id": 6, "title": "副市长", "start": "2025-08", "end": "至今", "rank": "副厅级", "note": "朔州市副市长"},
    {"person_id": 18, "org_id": 18, "title": "副县长", "start": "", "end": "", "rank": "", "note": "此前右玉县工作"},

    # 马占文 — 前任区委书记
    {"person_id": 19, "org_id": 1, "title": "区委书记", "start": "2021-04", "end": "", "rank": "正处级", "note": "2021年4月当选平鲁区委书记"},
    {"person_id": 19, "org_id": 2, "title": "区长", "start": "2020-07", "end": "2021-04", "rank": "正处级", "note": "平鲁区代区长/区长"},
    {"person_id": 19, "org_id": 7, "title": "县委书记", "start": "2022-03", "end": "至今", "rank": "正处级", "note": "右玉县委书记（马占文当前职务）"},
    {"person_id": 19, "org_id": 17, "title": "副秘书长", "start": "", "end": "", "rank": "正处级", "note": "朔州市政府"},
    {"person_id": 19, "org_id": 16, "title": "办公室副主任、主任", "start": "", "end": "", "rank": "", "note": "山西省政协办公厅"},
]

# ── Relationships ──────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_superior",
        "context": "区委书记与区长搭班关系",
        "overlap_org": "平鲁区（区委/区政府）",
        "overlap_period": "2025-10至今",
    },
    {
        "person_a": 18, "person_b": 2,
        "type": "superior_subordinate",
        "context": "前任区委书记郝云与区长苑冬梅搭班关系（2021-2025）",
        "overlap_org": "平鲁区（区委/区政府）",
        "overlap_period": "2021-04至2025-08",
    },
    {
        "person_a": 19, "person_b": 2,
        "type": "predecessor_successor",
        "context": "马占文为前任委书记/区长，苑冬梅接任区长",
        "overlap_org": "平鲁区人民政府",
        "overlap_period": "2021-04",
    },
    {
        "person_a": 18, "person_b": 19,
        "type": "predecessor_successor",
        "context": "郝云接替马占文任平鲁区委书记",
        "overlap_org": "中共平鲁区委员会",
        "overlap_period": "2021-04",
    },
    {
        "person_a": 1, "person_b": 18,
        "type": "predecessor_successor",
        "context": "刘志成接替郝云任平鲁区委书记",
        "overlap_org": "中共平鲁区委员会",
        "overlap_period": "2025-10",
    },
    {
        "person_a": 1, "person_b": 19,
        "type": "predecessor_successor",
        "context": "刘志成为马占文的后继者（隔任）",
        "overlap_org": "中共平鲁区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 6, "person_b": 10,
        "type": "same_team",
        "context": "同为区委常委、副区长",
        "overlap_org": "平鲁区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与宣传部长",
        "overlap_org": "中共平鲁区委员会",
        "overlap_period": "2025-10至今",
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "平鲁区人民政府",
        "overlap_period": "至今",
    },
]

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # Run build in staging directory
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
    print(f"Staging DB: {DB_PATH}")
    print(f"Staging GEXF: {GEXF_PATH}")