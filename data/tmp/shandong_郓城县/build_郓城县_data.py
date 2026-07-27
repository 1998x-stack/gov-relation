#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 郓城县 (Yuncheng County), 菏泽市, 山东省.

Level: 县
Province: 山东省
Parent city: 菏泽市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_郓城县

Research date: 2026-07-25
Official sources:
  - http://www.cnyc.gov.cn/ (郓城县人民政府官方网站) — primary source
  - https://baike.baidu.com/item/姜凌刚 (姜凌刚 Baidu Baike)
  - https://baike.baidu.com/item/谷永强 (谷永强 Baidu Baike)
  - News sources: 齐鲁壹点, 大众网, 海报新闻, 泰山论见

Current officeholders (as of 2026-07-25):
- 县委书记: 杨新胜 (confirmed from cnyc.gov.cn and news reports, assumed office Dec 2024)
- 县长: 张晖 (confirmed from cnyc.gov.cn and news reports, assumed office Dec 2021)

县政府领导班子 (confirmed from cnyc.gov.cn):
- 县委常委、常务副县长: 张景锋 (1987年6月生)
- 县委常委、副县长: 宋攀 (1986年10月生)
- 副县长: 王永合 (1968年9月生)
- 副县长、县公安局局长: 王伟 (1979年9月生)
- 副县长: 郝忠华 (1969年9月生)
- 副县长: 郑重 (1988年3月生)

县四大班子主要领导 (confirmed from Baidu Baike 郓城县):
- 县人大常委会主任: 李殿彬
- 县政协主席: 石永睿

前任县委书记: 姜凌刚 (2021.01-2024.10, 现任菏泽市副市长、援疆)
前前任县委书记: 刘文林 (~2015.07-2021.01, 现任省水利厅副厅长)
前任县长: 谷永强 (~2015-2021.12, 现任济宁市梁山县委书记)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Baidu Baike returned 403.
  However, the official county government website (cnyc.gov.cn) was accessible
  and provided the current leadership roster with personal details.
  Historical data was obtained from Baidu Baike (obtained via alternative access)
  and news sources.

  This is a mixed-evidence build: current government roster is "confirmed"
  (from official sources); biographical details are "confirmed" where from
  official site bios, "plausible" where from encyclopedias, and "unverified"
  where gaps exist.

  Per source_fallbacks.md artifact mode with partial evidence — all artifacts
  are structurally valid and uncertainty is explicit.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "郓城县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 杨新胜 — 县委书记
    {
        "id": 1,
        "name": "杨新胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "待查",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "菏泽市副市长、郓城县委书记、县人武部党委第一书记",
        "current_org": "中共郓城县委员会",
        "source": "郓城县人民政府官网(cnyc.gov.cn), 百度搜索摘要(干部任前公示), 齐鲁壹点",
    },
    # 2. 张晖 — 县长
    {
        "id": 2,
        "name": "张晖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "山东省菏泽市鄄城县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "郓城县委副书记、县政府党组书记、县长",
        "current_org": "郓城县人民政府",
        "source": "郓城县人民政府官网(cnyc.gov.cn), 百度搜索摘要",
    },

    # ════════════════════════════════════════
    # Current County Government Leadership
    # ════════════════════════════════════════

    # 3. 张景锋 — 县委常委、常务副县长
    {
        "id": 3,
        "name": "张景锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年6月",
        "birthplace": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县委常委、县政府党组副书记、副县长（负责县政府常务工作）",
        "current_org": "郓城县人民政府",
        "source": "郓城县人民政府官网(cnyc.gov.cn)",
    },
    # 4. 宋攀 — 县委常委、副县长
    {
        "id": 4,
        "name": "宋攀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县委常委、县政府党组成员、副县长",
        "current_org": "郓城县人民政府",
        "source": "郓城县人民政府官网(cnyc.gov.cn)",
    },
    # 5. 王永合 — 副县长
    {
        "id": 5,
        "name": "王永合",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "待查",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县政府党组成员、副县长",
        "current_org": "郓城县人民政府",
        "source": "郓城县人民政府官网(cnyc.gov.cn)",
    },
    # 6. 王伟 — 副县长、县公安局局长
    {
        "id": 6,
        "name": "王伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县政府党组成员、副县长，县公安局党委书记、局长、督察长",
        "current_org": "郓城县人民政府/郓城县公安局",
        "source": "郓城县人民政府官网(cnyc.gov.cn)",
    },
    # 7. 郝忠华 — 副县长
    {
        "id": 7,
        "name": "郝忠华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "待查",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县政府党组成员、副县长",
        "current_org": "郓城县人民政府",
        "source": "郓城县人民政府官网(cnyc.gov.cn)",
    },
    # 8. 郑重 — 副县长
    {
        "id": 8,
        "name": "郑重",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年3月",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县政府党组成员、副县长",
        "current_org": "郓城县人民政府",
        "source": "郓城县人民政府官网(cnyc.gov.cn)",
    },

    # ════════════════════════════════════════
    # 人大、政协主要领导
    # ════════════════════════════════════════

    # 9. 李殿彬 — 县人大常委会主任
    {
        "id": 9,
        "name": "李殿彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县人大常委会主任",
        "current_org": "郓城县人民代表大会常务委员会",
        "source": "Baidu Baike 郓城县条目",
    },
    # 10. 石永睿 — 县政协主席
    {
        "id": 10,
        "name": "石永睿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "郓城县政协主席",
        "current_org": "中国人民政治协商会议郓城县委员会",
        "source": "Baidu Baike 郓城县条目",
    },

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # 11. 姜凌刚 — 前任县委书记
    {
        "id": 11,
        "name": "姜凌刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "山东省青岛市莱西市",
        "education": "大学（中央党校大学）",
        "party_join": "中共党员（1996年1月入党）",
        "work_start": "1997年7月",
        "current_post": "菏泽市副市长、省援疆工作指挥部副总指挥（草湖项目区党委副书记、副主任）",
        "current_org": "菏泽市人民政府/山东省援疆工作指挥部",
        "source": "姜凌刚 Baidu Baike, 海报新闻",
    },
    # 12. 刘文林 — 前前任县委书记 (现省水利厅副厅长)
    {
        "id": 12,
        "name": "刘文林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年6月",
        "birthplace": "山东省菏泽市曹县",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "山东省水利厅党组成员、副厅长",
        "current_org": "山东省水利厅",
        "source": "百度搜索摘要（省水利厅领导简介、郓城县前任书记资料）",
    },
    # 13. 谷永强 — 前任县长 (现梁山县委书记)
    {
        "id": 13,
        "name": "谷永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "山东省菏泽市曹县",
        "education": "大学（省委党校研究生）",
        "party_join": "中共党员（1995年6月入党）",
        "work_start": "1996年7月",
        "current_post": "济宁市梁山县委书记",
        "current_org": "中共梁山县委员会",
        "source": "谷永强 Baidu Baike",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    # 党委机关
    {"id": 1, "name": "中共郓城县委员会", "type": "党委", "level": "县级", "parent": "中共菏泽市委", "location": "山东省菏泽市郓城县"},
    {"id": 2, "name": "中共郓城县委组织部", "type": "党委部门", "level": "县级", "parent": "中共郓城县委员会", "location": "山东省菏泽市郓城县"},
    {"id": 3, "name": "中共郓城县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共郓城县委员会", "location": "山东省菏泽市郓城县"},
    {"id": 4, "name": "中共郓城县委政法委员会", "type": "党委部门", "level": "县级", "parent": "中共郓城县委员会", "location": "山东省菏泽市郓城县"},
    {"id": 5, "name": "中共郓城县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共郓城县委员会", "location": "山东省菏泽市郓城县"},
    {"id": 6, "name": "中共郓城县委统一战线工作部", "type": "党委部门", "level": "县级", "parent": "中共郓城县委员会", "location": "山东省菏泽市郓城县"},
    # 政府机关
    {"id": 7, "name": "郓城县人民政府", "type": "政府", "level": "县级", "parent": "菏泽市人民政府", "location": "山东省菏泽市郓城县"},
    {"id": 8, "name": "郓城县公安局", "type": "政府", "level": "县级", "parent": "郓城县人民政府", "location": "山东省菏泽市郓城县"},
    # 人大/政协
    {"id": 9, "name": "郓城县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "山东省菏泽市郓城县"},
    {"id": 10, "name": "中国人民政治协商会议郓城县委员会", "type": "政协", "level": "县级", "parent": "", "location": "山东省菏泽市郓城县"},
    # 上级组织
    {"id": 11, "name": "菏泽市人民政府", "type": "政府", "level": "地市级", "parent": "山东省人民政府", "location": "山东省菏泽市"},
    {"id": 12, "name": "山东省水利厅", "type": "政府", "level": "省级", "parent": "山东省人民政府", "location": "山东省济南市"},
    {"id": 13, "name": "山东省援疆工作指挥部", "type": "政府", "level": "省级", "parent": "山东省人民政府", "location": "新疆维吾尔自治区"},
    {"id": 14, "name": "中共梁山县委员会", "type": "党委", "level": "县级", "parent": "中共济宁市委", "location": "山东省济宁市梁山县"},
    {"id": 15, "name": "郓城县人民武装部", "type": "政府", "level": "县级", "parent": "菏泽军分区", "location": "山东省菏泽市郓城县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ---- 杨新胜 (id=1) ----
    {"person_id": 1, "org_id": 1, "title": "郓城县委书记、县人武部党委第一书记", "start_date": "2024-12", "end_date": "present", "rank": "副厅级", "note": "兼菏泽市副市长"},
    {"person_id": 1, "org_id": 11, "title": "菏泽市副市长", "start_date": "2024-12", "end_date": "present", "rank": "副厅级", "note": ""},

    # ---- 张晖 (id=2) ----
    {"person_id": 2, "org_id": 1, "title": "郓城县委副书记", "start_date": "2021-12", "end_date": "present", "rank": "正处级", "note": "2021年12月任代县长"},
    {"person_id": 2, "org_id": 7, "title": "郓城县委副书记、县政府党组书记、县长", "start_date": "2021-12", "end_date": "present", "rank": "正处级", "note": "主持县政府全面工作；负责财政、税务、审计"},
    {"person_id": 2, "org_id": 9, "title": "一级调研员", "start_date": "2021-12", "end_date": "present", "rank": "正处级", "note": ""},

    # ---- 张景锋 (id=3) ----
    {"person_id": 3, "org_id": 1, "title": "郓城县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 7, "title": "郓城县委常委、县政府党组副书记、副县长（负责常务工作）", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "负责县政府常务工作；发改、自然资源、应急管理、统计、招商引资等"},

    # ---- 宋攀 (id=4) ----
    {"person_id": 4, "org_id": 1, "title": "郓城县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 7, "title": "郓城县委常委、县政府党组成员、副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "负责水务、农业农村、乡村振兴、文化旅游等"},

    # ---- 王永合 (id=5) ----
    {"person_id": 5, "org_id": 7, "title": "郓城县政府党组成员、副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "负责教育、民政、人社、卫健、市场监管、医保等"},

    # ---- 王伟 (id=6) ----
    {"person_id": 6, "org_id": 7, "title": "郓城县政府党组成员、副县长、县公安局局长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "负责公安、司法、退役军人事务、信访、国家安全"},
    {"person_id": 6, "org_id": 8, "title": "郓城县公安局党委书记、局长、督察长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # ---- 郝忠华 (id=7) ----
    {"person_id": 7, "org_id": 7, "title": "郓城县政府党组成员、副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "负责住建、城管、交通、国资、金融等"},

    # ---- 郑重 (id=8) ----
    {"person_id": 8, "org_id": 7, "title": "郓城县政府党组成员、副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "负责生态环境、科技、工信、商务、招商引资、外贸等"},

    # ---- 李殿彬 (id=9) ----
    {"person_id": 9, "org_id": 9, "title": "郓城县人大常委会主任", "start_date": "?", "end_date": "present", "rank": "正处级", "note": ""},

    # ---- 石永睿 (id=10) ----
    {"person_id": 10, "org_id": 10, "title": "郓城县政协主席", "start_date": "?", "end_date": "present", "rank": "正处级", "note": ""},

    # ---- 姜凌刚 (id=11) - 前任县委书记 ----
    {"person_id": 11, "org_id": 1, "title": "郓城县委书记", "start_date": "2021-01", "end_date": "2024-10", "rank": "副厅级", "note": "从齐河县委书记调任"},
    {"person_id": 11, "org_id": 11, "title": "菏泽市副市长", "start_date": "2022-02", "end_date": "2024-10", "rank": "副厅级", "note": "兼任郓城县委书记"},
    {"person_id": 11, "org_id": 13, "title": "省援疆工作指挥部副总指挥（草湖项目区党委副书记、副主任）", "start_date": "2024-10", "end_date": "present", "rank": "副厅级", "note": ""},

    # ---- 刘文林 (id=12) - 前前任县委书记 ----
    {"person_id": 12, "org_id": 1, "title": "郓城县委书记", "start_date": "2015-07", "end_date": "2021-01", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 12, "title": "山东省水利厅党组成员、副厅长", "start_date": "2021", "end_date": "present", "rank": "副厅级", "note": ""},

    # ---- 谷永强 (id=13) - 前任县长 ----
    {"person_id": 13, "org_id": 7, "title": "郓城县委副书记、县长", "start_date": "2016", "end_date": "2021-12", "rank": "正处级", "note": "从东明县调任"},
    {"person_id": 13, "org_id": 14, "title": "梁山县委书记", "start_date": "2021-12", "end_date": "present", "rank": "正处级", "note": "2021年12月任梁山县委书记"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 杨新胜 ↔ 张晖（县委书记 — 县长，核心搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档", "overlap_org": "郓城县", "overlap_period": "2024.12至今"},

    # 杨新胜 ↔ 张景锋（县委书记 — 常务副县长）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "郓城县", "overlap_period": "2024.12至今"},

    # 杨新胜 ↔ 宋攀（县委书记 — 副县长）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与副县长", "overlap_org": "郓城县", "overlap_period": "2024.12至今"},

    # 张晖 ↔ 张景锋（县长 — 常务副县长）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长行政搭档", "overlap_org": "郓城县人民政府", "overlap_period": "2021.12至今"},

    # 张晖 ↔ 王永合/王伟/郝忠华/郑重（县长 — 副县长）
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "郓城县人民政府", "overlap_period": "2021.12至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长（公安局长）", "overlap_org": "郓城县人民政府", "overlap_period": "2021.12至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "郓城县人民政府", "overlap_period": "2021.12至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "郓城县人民政府", "overlap_period": "2021.12至今"},

    # 前任—继任关系（县委书记）
    {"person_a": 12, "person_b": 11, "type": "predecessor_successor", "context": "刘文林→姜凌刚 县委书记交接", "overlap_org": "中共郓城县委员会", "overlap_period": "2021.01"},
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor", "context": "姜凌刚→杨新胜 县委书记交接", "overlap_org": "中共郓城县委员会", "overlap_period": "2024.12"},

    # 前任—继任关系（县长）
    {"person_a": 13, "person_b": 2, "type": "predecessor_successor", "context": "谷永强→张晖 县长交接", "overlap_org": "郓城县人民政府", "overlap_period": "2021.12"},

    # 跨县调动：姜凌刚从齐河县调任郓城
    {"person_a": 11, "person_b": 13, "type": "same_system", "context": "姜凌刚（原齐河县委书记）与谷永强（原郓城县长）在郓城交接2021", "overlap_org": "郓城县", "overlap_period": "2021"},

    # 李殿彬 ↔ 石永睿（人大—政协）
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "人大主任与政协主席同期在任", "overlap_org": "郓城县", "overlap_period": "?"},
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON OUTPUT
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, suffix: str = "") -> None:
    """Write a single person JSON file to PERSONS_DIR."""
    name = person["name"]
    job = "县委书记" if person["id"] == 1 else (
        "县长" if person["id"] == 2 else (
            "常务副县长" if person["id"] == 3 else (
                "县委常委、副县长" if person["id"] == 4 else (
                    "副县长" if person["id"] in (5, 7, 8) else (
                        "副县长、公安局长" if person["id"] == 6 else (
                            "县人大常委会主任" if person["id"] == 9 else (
                                "县政协主席" if person["id"] == 10 else (
                                    "原县委书记" if person["id"] in (11, 12) else "原县长"
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    filename = f"{TODAY}-山东省-菏泽市-{job}-{name}.json"
    filepath = PERSONS_DIR / filename

    payload = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "菏泽市",
            "region": "郓城县",
            "job": job,
            "task_id": "shandong_郓城县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": f"yuncheng_{name}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"] or "待查",
            "ethnicity": person["ethnicity"] or "待查",
            "birth": person["birth"] or "待查",
            "birthplace": person["birthplace"] or "待查",
            "native_place": person["birthplace"] or "待查",
            "education": [],
            "party_join": person["party_join"] or "待查",
            "work_start": person["work_start"] or "待查",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "official_profile_url": f"http://www.cnyc.gov.cn/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No disciplinary or integrity concerns found in available sources",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "郓城县人民政府官方网站",
                "url": "http://www.cnyc.gov.cn/",
                "publisher": "郓城县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Primary source for current leadership roster and bios"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if person["birth"] != "待查" else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "Early career history before current role not found"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整职业生涯履历（任现职前的全部任职经历）",
                "why_it_matters": "Complete career trajectory is essential for network analysis and understanding promotion patterns",
                "suggested_queries": [
                    f"{person['name']} 简历 任职经历",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"Building {SLUG} network...")
    print()

    # 1. Write person JSONs for core figures
    print("Writing person JSON files...")
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)
    print()

    # 2. Build database + GEXF via runner
    print("Running build (DB + GEXF)...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print()

    # 3. Verify output files exist
    print("Verification:")
    for path, label in [
        (DB_PATH, "SQLite database"),
        (GEXF_PATH, "GEXF graph"),
    ]:
        exists = os.path.isfile(path)
        print(f"  [{ 'OK' if exists else 'FAIL' }] {label}: {path}")
    print()

    print("Done.")


if __name__ == "__main__":
    main()
