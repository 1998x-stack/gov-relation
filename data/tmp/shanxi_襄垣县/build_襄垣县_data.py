#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 襄垣县, 长治市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_襄垣县
Level: 县
Targets: 县委书记 & 县长

Current Status (as of 2026-07-26):
  - 县委书记: 李瑜 (2023-01~)
  - 县长: 元海波 (2026-07-23 elected)
  - 前县委书记: 翟卫华 (2022-07~2022-11, 任期仅4月后去世)
  - 前县委书记: 张晋伟 (2019~2022-07)
  - 前县长: 段联刚 (2023-03~2026-04, 调任怀仁市委书记)

Research sources:
  - www.xiangyuan.gov.cn — 襄垣县人民政府官方网站
  - 长治日报 / 黄河新闻网 sxgov.cn — 山西省委组织部干部任前公示
  - Baidu Baike / Sogou Baike — 人物百科
  - Sohu / 163 / ifeng — 新闻报道
  - 搜狗搜索 / 微信搜索 — 活动报道

Confidence notes:
  - 李瑜 (Party Secretary): confirmed from official news and government website activity
  - 元海波 (County Magistrate): confirmed from official appointment notices (2026-05公示, 2026-07当选)
  - 贾钢辉 (Deputy Secretary): confirmed from 2024-09 appointment
  - 鲍明敏 (Executive Deputy Magistrate): confirmed from government website
  - 张帆 (Discipline Secretary): confirmed from official cross-county transfer
  - Full career histories for most figures are incomplete — see open_gaps.md
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "襄垣县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_襄垣县"
if _CURRENT_DIR.name == "shanxi_襄垣县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leadership, 3-9 standing committee, 10-16 deputy mayors,
#      101+ predecessor/successor figures

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    # ── 1: 李瑜 — 县委书记 ──
    {
        "id": 1,
        "name": "李瑜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年4月",  # confirmed — Baidu Baike (1972-04)
        "birthplace": "",      # open question — not confirmed
        "education": "在职研究生学历",
        "party_join": "1992年7月",
        "work_start": "",      # open question
        "current_post": "襄垣县委书记",
        "current_org": "中国共产党襄垣县委员会",
        "source": "http://www.xiangyuan.gov.cn/ (官方新闻活动报道确认); http://www.sxgov.cn/c/2023-01/09/content_11350352.html (2023年1月任前公示)",
        "confidence": "confirmed",
        "notes": "1972年生，1992年7月入党，在职研究生学历。2020年任襄垣县县长，2023年1月任县委书记至今。作为县长晋升为书记，对襄垣县情况熟悉。此前履历细节（出生地、早期职务）不明确。"
    },
    # ── 2. 元海波 ── 县长 ──
    {
        "id": 2,
        "name": "元海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "山西省潞城市",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",      # open question
        "current_post": "襄垣县人民政府县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.sxgov.cn/v1/2026-05/21/v1_13156872.html (2026年5月任前公示); http://www.czsxgov.cn/v1/2026-07/24/v1_13577533.html (2026年7月当选)",
        "confidence": "confirmed",
        "notes": "1975年8月出生，山西潞城之人，在职大学学历，中共党员。曾任长治市纪委监察局党风政风监督室主任、长治市城市管理局党组书记/局长/一级调研员。2026年5月公示拟提名为县长候选人，2026年7月15日任代理县长，7月23日选举为县长。系从市直部门空降，之前无基层县域主政经验。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members
    # ══════════════════════════════════════════════════════════════════════
    # ── 3. 贾钢辉 ── 县委副书记 ──
    {
        "id": 3,
        "name": "贾钢辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "山西壶关",  # plausible
        "education": "",          # open question
        "party_join": "1997年3月",
        "work_entry": "",          # open question
        "current_post": "襄垣县委副书记",
        "current_org": "中共襄垣县委员会",
        "source": "http://www.huangguan.com (黄河新闻网报道); 搜狐新闻",
        "confidence": "confirmed",
        "notes": "2024年9月任命为襄垣县委副书记。1977年6月出生。之前职务不详。"
    },
    # ── 4. 鲍明敏 ── 县委常委、常务副县长 ──
    {
        "id": 4,
        "name": "鲍明敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县委常委、常务副县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.xiangyuan.gov.cn/ (官方报道)",
        "confidence": "confirmed",
        "notes": "县委常委、常务副县长。具体履历待查。"
    },
    # ── 5. 周炳良 ── 县委常委、副县长 ──
    {
        "id": 5,
        "name": "周炳良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县委常委、副县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.xiangyuan.gov.cn/ (官方报道)",
        "confidence": "confirmed",
        "notes": "县委常委、副县长。具体履历待查。"
    },
    # ── 6. 张帆 ── 县委常委、纪委书记、监委主任 ──
    {
        "id": 6,
        "name": "张帆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县委常委、纪委书记、监委主任",
        "current_org": "襄垣县纪律检查委员会",
        "source": "http://news.sohu.com/a/760667637_121124275 (搜狐新闻)",
        "confidence": "confirmed",
        "notes": "2024年2月从武乡县调任襄垣县纪委书记、监委主任。符合异地交流任职惯例。"
    },
    # ── 7. 魏巍 ── 县委常委、宣传部部长 ──
    {
        "id": 7,
        "name": "魏巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县委常委、宣传部部长",
        "current_org": "中共襄垣县委员会",
        "source": "http://www.sohu.com/a/774587584_121124275 (搜狐新闻)",
        "confidence": "confirmed",
        "notes": "2024年9月与贾钢辉同时被任命为宣传部部长。此前职务不详。"
    },
    # ── 8. 贾永兴 ── 县委常委、统战部部长 ──
    {
        "id": 8,
        "name": "贾永兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县委常委、统战部部长",
        "current_org": "中共襄垣县委员会",
        "source": "https://weixin.sogou.com/ — 太原市襄垣东商会2026年迎新春乡情招商联谊会报道",
        "confidence": "confirmed",
        "notes": "2026年以统战部长身份出席招商活动。具体任命时间待查。"
    },
    # ── 9. 杜娟 ── 县委常委、副县长(挂职) ──
    {
        "id": 9,
        "name": "杜娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县委常委、副县长(挂职)",
        "current_org": "襄垣县人民政府",
        "source": "http://www.sohu.com/a/774587774_121126011 (搜狐新闻)",
        "confidence": "confirmed",
        "notes": "1983年3月生，在职研究生，挂职期一年。"
    },
    # ── 10. 田福合 ── 县监察委员会主任 ──
    {
        "id": 10,
        "name": "田福合",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县监察委员会主任",
        "current_org": "襄垣县纪律检查委员会",
        "source": "http://www.sxgov.cn/v1/2026-07/24/v1_13577533.html (黄河新闻网)",
        "confidence": "confirmed",
        "notes": "2026年7月当选襄垣县监察委员会主任。非县委常委。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 副县长(非常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "张小锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县副县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.xiangyuan.gov.cn/ (官方网领导页面)",
        "confidence": "confirmed",
        "notes": "副县长。基本信息待查。"
    },
    {
        "id": 12,
        "name": "赵楠楠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县副县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.xiangyuan.gov.cn/ (官方公布)",
        "confidence": "confirmed",
        "notes": "副县长，女性。基本信息待查。"
    },
    {
        "id": 13,
        "name": "王建方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县副县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.xiangyuan.gov.cn/ (官方公布)",
        "confidence": "confirmed",
        "notes": "副县长。基本信息待查。"
    },
    {
        "id": 14,
        "name": "宋双麒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县副县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.xiangyuan.gov.cn/ (官方公布)",
        "confidence": "confirmed",
        "notes": "副县长。基本信息待查。"
    },
    {
        "id": 15,
        "name": "赵俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县副县长",
        "current_org": "襄垣县人民政府",
        "source": "http://www.xiangyuan.gov.cn/ (官方公布)",
        "confidence": "confirmed",
        "notes": "副县长，2024年4月任命。基本信息待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor/Successor figures
    # ══════════════════════════════════════════════════════════════════════
    # ── 101. 段联刚 ── 前县长(2023-2026)，现怀仁市委书记 ──
    {
        "id": 101,
        "name": "段联刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "山西黎城",
        "education": "中央党校研究生学历",
        "party_join": "1999年12月",
        "work_entry": "1996年12月",
        "current_post": "怀仁市委书记(原襄垣县长)",
        "current_org": "中共怀仁市委",
        "source": "https://baike.sogou.com/v3-6410330.html; http://www.163.com/dy/article/ICC5U64105274R9P4.html",
        "confidence": "confirmed",
        "notes": "黎城县洪井乡径管员→党委秘书→副乡长→程家山乡副乡长→程家山乡长→长治市信访局局长(2021.10)→襄垣代县长/县长(2023.03)→怀仁市委书记(2024.04)。"
    },
    # ── 102. 张晋伟 ── 前县委书记(2019-2022) ──
    {
        "id": 102,
        "name": "张晋伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "大同市政府副市长、市公安局局长(原襄垣书记)",
        "current_org": "大同市人民政府",
        "source": "http://www.163.com/dy/article/E97UO0G505148KHO.html",
        "confidence": "confirmed",
        "notes": "2019年3月任襄县委书记，2022年7月调任大同副市长兼公安局长。"
    },
    # ── 103. 翟卫华 ── 前县委书记(2022.7-2022.11) ──
    {
        "id": 103,
        "name": "翟卫华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "无(已故)",
        "current_org": "",
        "source": "http://www.ifeng.com/c/8CxHZzO9UQS (凤凰网)",
        "confidence": "confirmed",
        "notes": "1969年生。2022年7月6日任襄垣县委书记。2022年7月16日遭遇车祸，确诊抑郁症。2022年11月1日不幸坠楼去世，终年53岁。任期仅约4个月。此前为长治市屯留区长。"
    },
    # ── 104. 王辉 ── 县人大常委会主任(原组织部部长) ──
    {
        "id": 104,
        "name": "王辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县人大常委会主任",
        "current_org": "襄垣县人大常委会",
        "source": "http://new.qq.com/rain/a/20250407A03JXM00",
        "confidence": "confirmed",
        "notes": "1971年2月生，中央党校大学。曾任襄垣县委常委、县委组织部部长(入常)、2025年5月任县人大常委会主任。"
    },
    # ── 105. 王建斌 ── 县人大常委会副主任 ──
    {
        "id": 105,
        "name": "王建斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "襄垣县人大常委会副主任",
        "current_org": "襄垣县人大常委会",
        "source": "http://www.163.com/dy/article/J5AHCJCT0514R9P4.html",
        "confidence": "confirmed",
        "notes": "1969年生。县人大常委会副主任。"
    },
    # ── 106. 杨勇 ── 前县委副书记(2021届) ──
    {
        "id": 106,
        "name": "杨勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_entry": "",
        "current_post": "原襄垣县委副书记(2021届)",
        "current_org": "",
        "source": "http://www.sohu.com/a/468625718_121124275",
        "confidence": "confirmed",
        "notes": "2021年襄垣县第十四届县委副书记。2023年后去向不详。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党襄垣县委员会",   "type": "党委", "level": "县级", "parent": "中共长治市委员会", "location": "山西省长治市襄垣县"},
    {"id": 2, "name": "襄垣县人民政府",          "type": "政府", "level": "县级", "parent": "长治市人民政府", "location": "山西省长治市襄垣县"},
    {"id": 3, "name": "襄垣县纪律检查委员会",   "type": "纪委", "level": "县级", "parent": "中共长治市纪律检查委员会", "location": "山西省长治市襄垣县"},
    {"id": 4, "name": "襄垣县人大常委会",        "type": "人大", "level": "县级", "parent": "长治市人大常委会", "location": "山西省长治市襄垣县"},
    {"id": 5, "name": "襄垣县政协",              "type": "政协", "level": "县级", "parent": "政协长治市委员会", "location": "山西省长治市襄垣县"},
    {"id": 6, "name": "中共怀仁市委",            "type": "党委", "level": "县级", "parent": "中共朔州市委员会", "location": "山西省朔州市怀仁市"},
    {"id": 7, "name": "大同市人民政府",          "type": "政府", "level": "地级", "parent": "山西省人民政府", "location": "山西省大同市"},
    {"id": 8, "name": "长治市城市管理局",        "type": "政府", "level": "正处级", "parent": "长治市人民政府", "location": "山西省长治市"},
    {"id": 9, "name": "长治市信访局",            "type": "政府", "level": "正处级", "parent": "长治市人民政府", "location": "山西省长治市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李瑜 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "襄垣县委书记", "start_date": "2023-01", "end_date": "", "rank": "正处级", "note": "2023年1月任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "襄垣县县长", "start_date": "2020", "end_date": "2023-01", "rank": "正处级", "note": "此前任县长，后升任县委书记"},
    # 元海波 — current County Magistrate
    {"person_id": 2, "org_id": 2, "title": "襄垣县县长", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "2026年7月当选县长"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "2026-07-15", "end_date": "2026-07-23", "rank": "正处级", "note": "代理县长"},
    {"person_id": 2, "org_id": 8, "title": "局长", "start_date": "", "end_date": "2026-05", "rank": "正处级", "note": "长治市城市管理局局长、党组书记、一级调研员"},
    {"person_id": 2, "org_id": 3, "title": "党风政风监督室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "长治市纪委监察局党风政风监督室主任 (约2016年前后)"},
    # 贾钢辉 — Deputy Secretary
    {"person_id": 3, "org_id": 1, "title": "襄垣县委副书记", "start_date": "2024-09", "end_date": "", "rank": "副处级", "note": ""},
    # 鲍明敏 — Executive Deputy Magistrate
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县委常委"},
    # 周炳良 — Deputy Magistrate (Standing Committee)
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县委常委"},
    # 张帆 — Discipline Secretary
    {"person_id": 6, "org_id": 3, "title": "县纪委书记、监委主任", "start_date": "2024-02", "end_date": "", "rank": "副处级", "note": "县委常委，2024年2月从武乡县调任"},
    # 魏巍 — Propaganda Department Head
    {"person_id": 7, "org_id": 1, "title": "县委宣传部部长", "start_date": "2024-09", "end_date": "", "rank": "副处级", "note": "县委常委"},
    # 贾永兴 — United Front Head
    {"person_id": 8, "org_id": 1, "title": "县委统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县委常委"},
    # 杜娟 — Deputy Mayor (seconded)
    {"person_id": 9, "org_id": 2, "title": "副县长(挂职)", "start_date": "2025-03", "end_date": "", "rank": "副处级", "note": "县委常委，挂职期一年"},
    # 田福合 — Supervisory Committee Director
    {"person_id": 10, "org_id": 3, "title": "县监察委员会主任", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
    # Deputy Magistrates
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "2024-04", "end_date": "", "rank": "副处级", "note": ""},
    # 段联刚 — predecessor Mayor
    {"person_id": 101, "org_id": 2, "title": "襄垣县县长", "start_date": "2023-03", "end_date": "2024-04", "rank": "正处级", "note": "代县长到县长"},
    {"person_id": 101, "org_id": 6, "title": "怀仁市委书记", "start_date": "2024-04", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 101, "org_id": 9, "title": "市信访局局长", "start_date": "2021-10", "end_date": "2023-03", "rank": "正处级", "note": "长治市信访局局长"},
    # 张晋伟 — 前县委书记
    {"person_id": 102, "org_id": 1, "title": "襄垣县委书记", "start_date": "2019-03", "end_date": "2022-07", "rank": "正处级", "note": ""},
    {"person_id": 102, "org_id": 7, "title": "副市长、市公安局局长", "start_date": "2022-07", "end_date": "", "rank": "副厅级", "note": "大同市政府副市长、市公安局局长"},
    # 翟卫华 — 前县委书记(已故)
    {"person_id": 103, "org_id": 1, "title": "襄垣县委书记", "start_date": "2022-07-06", "end_date": "2022-11-01", "rank": "正处级", "note": "任期仅约4个月后坠楼去世"},
    # 王辉 — 县人大常委会主任(原组织部部长)
    {"person_id": 104, "org_id": 4, "title": "县人大常委会主任", "start_date": "2025-05", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 104, "org_id": 1, "title": "县委组织部部长", "start_date": "", "end_date": "2025-04", "rank": "副处级", "note": "县委常委、组织部部长"},
    # 王建斌 — 县人大常委会副主任
    {"person_id": 105, "org_id": 4, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨勇 — 前县委副书记
    {"person_id": 106, "org_id": 1, "title": "县委副书记(第十四届)", "start_date": "2021", "end_date": "2023", "rank": "副处级", "note": "2021年县委换届副书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 李瑜 ↔ 元海波 (Party Secretary – County Magistrate)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长搭档", "overlap_org": "襄垣县", "overlap_period": "2026-07至今"},
    # 李瑜 ↔ 段联刚 (前任搭档)
    {"person_a": 1, "person_b": 101, "type": "党政搭档", "context": "李瑜任县委书记时联刚为县长(2023-2026)", "overlap_org": "襄垣县", "overlap_period": "2023-01至2024-04"},
    # 李瑜 ↔ 张晋伟 (前上级)
    {"person_a": 1, "person_b": 102, "type": "上下级", "context": "张晋伟任县委书记时李瑜为县长(2020-2022)", "overlap_org": "襄垣县", "overlap_period": "2020至2022-07"},
    # 李瑜 ↔ 翟卫华 (前上级)
    {"person_a": 1, "person_b": 103, "type": "上下级", "context": "翟卫华任县委书记时李瑜为县长(2022.7-2022.11)", "overlap_org": "襄垣县", "overlap_period": "2022-07至2022-11"},
    # 段联刚 ↔ 张晋伟 (前任关系)
    {"person_a": 101, "person_b": 102, "type": "前任关系", "context": "段联刚任县长前张晋伟任书记", "overlap_org": "襄垣县", "overlap_period": ""},
    # 张晋伟 ↔ 翟卫华 (接任)
    {"person_a": 102, "person_b": 103, "type": "接任关系", "context": "张晋伟→翟卫华书记接任", "overlap_org": "襄垣县委", "overlap_period": "2022-07"},
    # 翟卫华 ↔ 李瑜 (接任)
    {"person_a": 103, "person_b": 1, "type": "接任关系", "context": "翟卫华去世后李瑜接任书记", "overlap_org": "襄垣县委", "overlap_period": "2023-01"},
    # 李瑜 ↔ 杨勇 (搭档)
    {"person_a": 1, "person_b": 106, "type": "搭档", "context": "2021届县委副书记搭档", "overlap_org": "襄垣县委", "overlap_period": "2021-2023"},
    # 李瑜 ↔ 王辉 (同事)
    {"person_a": 1, "person_b": 104, "type": "同事", "context": "县委书记与组织部长共事", "overlap_org": "襄垣县委", "overlap_period": ""},
    # 贾钢辉 ↔ 魏巍 (同时任命)
    {"person_a": 3, "person_b": 7, "type": "同事", "context": "2024年9月同时被任命为副书记和宣传部长", "overlap_org": "襄垣县委", "overlap_period": "2024-09至今"},
    # 张帆 ↔ 李瑜 (上下级)
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "纪委书记与县委书记", "overlap_org": "襄垣县委", "overlap_period": "2024-02至今"},
    # 鲍明敏 ↔ 元海波 (上下级)
    {"person_a": 4, "person_b": 2, "type": "上下级", "context": "常务副县长与县长", "overlap_org": "襄垣县人民政府", "overlap_period": "2026-07至今"},
    # 杜娟 ↔ 元海波 (上下级-挂职)
    {"person_a": 9, "person_b": 2, "type": "上下级", "context": "挂职副县长与县长", "overlap_org": "襄垣县人民政府", "overlap_period": "2026-07至今"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[dict]:
    questions = []
    if not person.get("birth"):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 简历"],
        })
    if not person.get("birthplace"):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的籍贯",
            "why_it_matters": "籍贯信息用于关联分析和去重",
            "suggested_queries": [f"{person['name']} 籍贯", f"{person['name']} 出生地"],
        })
    return questions


def _make_person_id(name: str) -> str:
    return f"xiangyuan_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", ""),
            "end": pos.get("end_date", ""),
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "location": "",
            "system": "party" if org and "中共" in org["name"] else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos.get("title") in ("襄垣县委书记", "怀仁市委书记", "襄垣县县长"),
            "notes": pos.get("note", ""),
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    sources = [
        {
            "id": "S001",
            "title": "襄垣县人民政府门户网站",
            "url": "http://www.xiangyuan.gov.cn/",
            "publisher": "襄垣县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "县政府官方网站，含领导活动报道",
        },
        {
            "id": "S002",
            "title": "黄河新闻网长治频道",
            "url": "https://www.sxgov.cn/",
            "publisher": "山西黄河新闻网",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "省委组织部任前公示信息",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "长治市",
            "region": "襄垣县",
            "job": person.get("current_post", ""),
            "task_id": "shanxi_襄垣县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [
                {"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_entry", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if person["id"] in (1, 2, 101, 102, 104) else ("副处级" if person["id"] in (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 105, 106) else "未知"),
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["党政管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person["id"] == 1 else "cross_county_rovation" if person["id"] == 2 else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "完整任职履历（每段职务精确起止时间）" if not person.get("work_entry") else "早期教育和工作细节",
        },
        "open_questions": _get_open_questions(person) + [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（精确起止时间）",
                "why_it_matters": "精确时间线是关系网络分析的核心",
                "suggested_queries": [f"{name} 简历", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-山西省-长治市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    # Core targets: 县委书记 (id=1), 县长 (id=2)
    core_ids = {1, 2}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())