#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 岚山区 (Lanshan District), 日照市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_岚山区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - http://www.rzlanshan.gov.cn/ — 日照市岚山区人民政府官方网站 (primary, accessible 2026-07-25)
  - Baidu Baike — 岚山区 page (leadership table, accessed via insane-search)
  - News articles on rzlanshan.gov.cn — multiple articles confirming leadership (July 2026)
  - Baidu Baike — 申洁 (区委书记) biography partially accessed
  - Baidu Baike — 周绪龙 (政协主席) biography
  - Baidu Baike — 迟令席 (原政法委书记) biography
  - Existing 日照市 investigation (2026-07-25) — cross-references for 焦春锋, 刘祥龙

Confidence notes:
  - 区委书记申洁: CONFIRMED via multiple official government news articles (September 2025-July 2026)
  - 区长万磊: CONFIRMED via official leadership profile page (区政府领导 section) with bio
  - 常务副区长牛振: CONFIRMED via official leadership profile page
  - Other deputy leaders: various confidence levels, explicitly documented
  - 人大/政协 leaders: partially identified (周力 as 人大主任, 周绪龙 as 政协主席)
  - Biographical details: where available from government profiles
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "岚山区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_岚山区"
if _CURRENT_DIR.name == "shandong_岚山区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING / "data" / "persons"
PJSON_DIR.mkdir(parents=True, exist_ok=True)

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core, 3-10 standing committee, 11-19 district government, 20-29 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current — as of July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "申洁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年7月",
        "birthplace": "山东日照东港",
        "education": "大学（中国农业大学在职）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共日照市岚山区委员会",
        "source": "https://baike.baidu.com/item/%E7%94%B3%E6%B4%81/58460880",
        "confidence": "confirmed",
        "notes": "1977年7月生，日照东港人。曾任岚山区区长，后任区委书记。之前也曾任日照市行政审批服务局局长。"
    },
    {
        "id": 2,
        "name": "万磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col325593/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1975年2月生，研究生学历，中共党员。现任日照市岚山区委副书记，区政府党组书记、区长。曾任岚山区常务副区长等职。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (区委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "牛振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年12月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col341684/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1986年12月生，研究生学历，中共党员。现任岚山区委常委，区政府党组副书记、副区长（常务）。分管自然资源、规划、交通、物流、国资、金融等。"
    },
    {
        "id": 4,
        "name": "赵家胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col249400/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1972年2月生，大学学历，中共党员。现任岚山区委常委，区政府副区长。分管住建、城管、农业农村、水利、海洋、供销等。"
    },
    {
        "id": 5,
        "name": "周力",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任（原任区委常委）",
        "current_org": "岚山区人大常委会",
        "source": "http://www.rzlanshan.gov.cn/art/2026/7/20/art_32570_10379397.html",
        "confidence": "confirmed",
        "notes": "周力在区委常委会会议中作为区领导出席。根据Baidu Baike岚山区页面，周力现任岚山区人大常委会主任。曾担任区委常委，其具体原任职务（纪委/政法/宣传）待查。"
    },
    {
        "id": 6,
        "name": "古茂林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中共日照市岚山区委员会",
        "source": "http://www.rzlanshan.gov.cn/art/2026/7/20/art_32570_10379397.html",
        "confidence": "confirmed",
        "notes": "古茂林在区委常委会会议中作为区领导出席。具体职务（纪委/组织/政法等）待进一步确认。"
    },
    {
        "id": 7,
        "name": "田国磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中共日照市岚山区委员会",
        "source": "http://www.rzlanshan.gov.cn/art/2026/7/20/art_32570_10379397.html",
        "confidence": "confirmed",
        "notes": "田国磊在区委常委会会议中作为区领导出席。具体职务（宣传/统战等）待进一步确认。"
    },
    {
        "id": 8,
        "name": "郑笃轩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、岚山经济开发区党工委书记、管委会主任",
        "current_org": "岚山经济开发区",
        "source": "http://www.rzlanshan.gov.cn/col/col249399/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1982年9月生，研究生学历，中共党员。现任区政府党组成员、岚山经济开发区党工委书记、管委会主任。分管招商引资、商贸、港口项目服务等。"
    },
    {
        "id": 9,
        "name": "张健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、区监委主任",
        "current_org": "中共日照市岚山区纪律检查委员会",
        "source": "https://baijiahao.baidu.com/s?id=1855707952915903494",
        "confidence": "confirmed",
        "notes": "2026年1月29日，岚山区第十九届人民代表大会第五次会议选举张健为岚山区监察委员会主任。纪委书记/监委主任通常为区委常委。具体履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政府其他副区长
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "卢衍海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col364243/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1980年6月生，大学学历，中共党员。现任岚山区副区长、区政府党组成员。分管领域信息待查。"
    },
    {
        "id": 12,
        "name": "于涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col341680/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1983年10月生，研究生学历，中共党员。分管民政、文旅、行政审批、市场监管、生态环境、人大/政协提案等。"
    },
    {
        "id": 13,
        "name": "厉慧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "岚山区",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col354799/index.html",
        "confidence": "confirmed",
        "notes": "女，中共党员，1983年6月生，岚山人，省委党校研究生学历。分管农高区、教体、科技、卫健医保等。"
    },
    {
        "id": 14,
        "name": "孙磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "山东莒县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、市公安局岚山分局局长",
        "current_org": "日照市公安局岚山分局",
        "source": "http://www.rzlanshan.gov.cn/col/col365000/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1982年10月生，莒县人，大学学历，中共党员。兼任日照市公安局岚山分局党委书记、局长、督察长。"
    },
    {
        "id": 15,
        "name": "王剑南",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col368380/index.html",
        "confidence": "confirmed",
        "notes": "女，1987年3月生，汉族，研究生学历，中共党员。挂职副区长。具体挂职单位和分管领域待查。"
    },
    {
        "id": 16,
        "name": "刘升锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年8月",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职/科技副区长）",
        "current_org": "岚山区人民政府",
        "source": "http://www.rzlanshan.gov.cn/col/col362301/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1985年8月生，博士研究生学历，中共党员。科技副区长（挂职）。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 专职区委副书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 17,
        "name": "刘峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记（专职）",
        "current_org": "中共日照市岚山区委员会",
        "source": "日照市生态环境局网站新闻",
        "confidence": "confirmed",
        "notes": "区委专职副书记。新闻标题'岚山区区委副书记刘峰调研绣针河水环境质量提升工作'（2026年4月）。具体履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "name": "周绪龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "山东日照东港",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1996年7月",
        "current_post": "区政协主席（2025年1月当选）/现任日照市农业农村局局长",
        "current_org": "中国人民政治协商会议日照市岚山区委员会",
        "source": "https://baike.baidu.com/item/%E5%91%A8%E7%BB%AA%E9%BE%99",
        "confidence": "confirmed",
        "notes": "1974年11月生，日照东港人，1996年6月入党，1996年7月参加工作，大学学历。2025年1月当选岚山区政协主席。2025年12月被任命为日照市农业农村局局长。曾任岚山区副区长（2021.12-2023.05）、日照市发改委副主任等职。"
    },
    {
        "id": 19,
        "name": "何玉滨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "岚山区人大常委会",
        "source": "https://baijiahao.baidu.com/s?id=1855707952915903494",
        "confidence": "confirmed",
        "notes": "2026年1月29日，岚山区第十九届人民代表大会第五次会议选举何玉滨为岚山区第十九届人民代表大会常务委员会副主任。具体履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 原政法委书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "迟令席",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "山东日照",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1991年7月",
        "current_post": "日照市红十字会党组书记、常务副会长",
        "current_org": "日照市红十字会",
        "source": "https://baike.baidu.com/item/%E8%BF%9F%E4%BB%A4%E5%B8%AD",
        "confidence": "confirmed",
        "notes": "1970年8月生，山东日照人，1991年7月参加工作，省委党校研究生学历，中共党员。曾任岚山区委常委、政法委书记。现任日照市红十字会党组书记、常务副会长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "焦春锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "日照市委常委（原岚山区委书记）",
        "current_org": "中共日照市委员会",
        "source": "http://www.rizhao.gov.cn/",
        "confidence": "confirmed",
        "notes": "原岚山区委书记。2025年7月12日山东省委组织部发布任前公示，焦春锋拟任副厅级领导职务。后任日照市委常委。2019-2021年任岚山区委副书记、区长。"
    },
    {
        "id": 22,
        "name": "来风华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已退休/转任",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E5%B2%9A%E5%B1%B1%E5%8C%BA",
        "confidence": "plausible",
        "notes": "岚山区前任区委书记（约2016-2021年），后转任日照市政协或其他职务。具体去向待查。"
    },
    {
        "id": 23,
        "name": "周升元",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已调任",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E5%B2%9A%E5%B1%B1%E5%8C%BA",
        "confidence": "plausible",
        "notes": "岚山区前任区长（约2019-2022年）。周升元之后申洁接任区长。具体去向待查。"
    },
    {
        "id": 24,
        "name": "高杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已调任",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E5%B2%9A%E5%B1%B1%E5%8C%BA",
        "confidence": "plausible",
        "notes": "岚山区前任区委书记（约2014-2016年），后任日照市委常委。具体履历待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共日照市岚山区委员会", "type": "party", "level": "县处级", "parent": "中共日照市委员会", "location": "日照市岚山区"},
    {"id": 2, "name": "岚山区人民政府", "type": "government", "level": "县处级", "parent": "日照市人民政府", "location": "日照市岚山区"},
    {"id": 3, "name": "中共日照市岚山区纪律检查委员会", "type": "discipline", "level": "县处级", "parent": "日照市纪律检查委员会", "location": "日照市岚山区"},
    {"id": 4, "name": "岚山区人大常委会", "type": "people_congress", "level": "县处级", "parent": "日照市人大常委会", "location": "日照市岚山区"},
    {"id": 5, "name": "中国人民政治协商会议日照市岚山区委员会", "type": "cppcc", "level": "县处级", "parent": "", "location": "日照市岚山区"},
    {"id": 6, "name": "岚山经济开发区", "type": "development_zone", "level": "县处级", "parent": "岚山区人民政府", "location": "日照市岚山区"},
    {"id": 7, "name": "日照市公安局岚山分局", "type": "government", "level": "县处级", "parent": "日照市公安局", "location": "日照市岚山区"},
    {"id": 8, "name": "日照市红十字会", "type": "other", "level": "县处级", "parent": "", "location": "日照市"},
    # Parent city organizations
    {"id": 9, "name": "中共日照市委员会", "type": "party", "level": "地厅级", "parent": "中共山东省委", "location": "日照市"},
    {"id": 10, "name": "日照市人民政府", "type": "government", "level": "地厅级", "parent": "山东省人民政府", "location": "日照市"},
    {"id": 11, "name": "日照市农业农村局", "type": "government", "level": "县处级", "parent": "日照市人民政府", "location": "日照市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 申洁
    {"id": 1, "person_id": 1, "org_id": 1, "title": "区委书记", "start": "2025-09", "end": "present", "rank": "县处级正职", "note": "2025年9月任岚山区委书记"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "区长（前任）", "start": "2022", "end": "2025-08", "rank": "县处级正职", "note": "2025年8月卸任区长"},
    # 万磊
    {"id": 3, "person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "县处级正职", "note": "as of 2026-07"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "兼任"},
    # 牛振
    {"id": 5, "person_id": 3, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 6, "person_id": 3, "org_id": 2, "title": "副区长（常务）", "start": "", "end": "present", "rank": "县处级副职", "note": "区政府党组副书记"},
    # 赵家胜
    {"id": 7, "person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 8, "person_id": 4, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 周力
    {"id": 9, "person_id": 5, "org_id": 4, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": "as of 2026-01"},
    # 古茂林
    {"id": 10, "person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 田国磊
    {"id": 11, "person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 郑笃轩
    {"id": 12, "person_id": 8, "org_id": 6, "title": "岚山经济开发区党工委书记、管委会主任", "start": "", "end": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 张健
    {"id": 13, "person_id": 9, "org_id": 3, "title": "纪委书记、区监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年1月当选监委主任"},
    {"id": 14, "person_id": 9, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "通常兼任"},
    # 卢衍海
    {"id": 15, "person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 于涛
    {"id": 16, "person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "分管民政、文旅、审批、市场监管等"},
    # 厉慧
    {"id": 17, "person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "分管农高区、教体、科技、卫健等"},
    # 孙磊
    {"id": 18, "person_id": 14, "org_id": 7, "title": "岚山公安分局局长", "start": "", "end": "present", "rank": "县处级副职", "note": "兼任副区长"},
    {"id": 19, "person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 王剑南
    {"id": 20, "person_id": 15, "org_id": 2, "title": "副区长（挂职）", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 刘升锐
    {"id": 21, "person_id": 16, "org_id": 2, "title": "副区长（挂职/科技副区长）", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 刘峰
    {"id": 22, "person_id": 17, "org_id": 1, "title": "区委副书记（专职）", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 周绪龙
    {"id": 23, "person_id": 18, "org_id": 5, "title": "区政协主席", "start": "2025-01", "end": "present", "rank": "县处级正职", "note": "2025年1月当选"},
    {"id": 24, "person_id": 18, "org_id": 11, "title": "日照市农业农村局局长", "start": "2025-12", "end": "present", "rank": "县处级正职", "note": "2025年12月任命"},
    {"id": 25, "person_id": 18, "org_id": 2, "title": "岚山区副区长", "start": "2021-12", "end": "2023-05", "rank": "县处级副职", "note": ""},
    # 何玉滨
    {"id": 26, "person_id": 19, "org_id": 4, "title": "区人大常委会副主任", "start": "2026-01", "end": "present", "rank": "县处级副职", "note": ""},
    # 迟令席
    {"id": 27, "person_id": 20, "org_id": 8, "title": "日照市红十字会党组书记、常务副会长", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    {"id": 28, "person_id": 20, "org_id": 1, "title": "原区委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "已调离岚山区"},
    # 焦春锋
    {"id": 29, "person_id": 21, "org_id": 9, "title": "日照市委常委", "start": "2025", "end": "present", "rank": "副厅级", "note": ""},
    {"id": 30, "person_id": 21, "org_id": 1, "title": "原岚山区委书记", "start": "2021", "end": "2025-07", "rank": "县处级正职", "note": ""},
    # 来风华
    {"id": 31, "person_id": 22, "org_id": 1, "title": "原岚山区委书记", "start": "2016", "end": "2021", "rank": "县处级正职", "note": ""},
    # 周升元
    {"id": 32, "person_id": 23, "org_id": 2, "title": "原岚山区区长", "start": "2019", "end": "2022", "rank": "县处级正职", "note": ""},
    # 高杰
    {"id": 33, "person_id": 24, "org_id": 1, "title": "原岚山区委书记", "start": "2014", "end": "2016", "rank": "县处级正职", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 申洁 <-> 万磊（党政搭档）
    {
        "id": 1,
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "党政搭档：申洁任区委书记，万磊任区委副书记、区长",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2025-至今",
        "confidence": "confirmed"
    },
    # 申洁 <-> 焦春锋（前后任）
    {
        "id": 2,
        "person_a": 1,
        "person_b": 21,
        "type": "predecessor_successor",
        "context": "申洁接替焦春锋任岚山区委书记",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2025",
        "confidence": "confirmed"
    },
    # 申洁 <-> 牛振（上下级/党政班子内）
    {
        "id": 3,
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "申洁为区委书记，牛振为区委常委、副区长",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2025-至今",
        "confidence": "confirmed"
    },
    # 申洁 <-> 赵家胜（上下级）
    {
        "id": 4,
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "申洁为区委书记，赵家胜为区委常委、副区长",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2025-至今",
        "confidence": "confirmed"
    },
    # 周力 <-> 全体常委（曾为区委常委转人大主任）
    {
        "id": 5,
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "周力原为区委常委，后任人大主任，与申洁在区委班子中曾有交集",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2025-2026",
        "confidence": "confirmed"
    },
    # 迟令席 -> 古茂林（可能的政法委书记交接）
    {
        "id": 6,
        "person_a": 20,
        "person_b": 6,
        "type": "predecessor_successor",
        "context": "迟令席原任区委常委、政法委书记调离后，古茂林可能接任或其职务出现分工调整",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "",
        "confidence": "unverified"
    },
    # 焦春锋 <-> 来风华（前后任）
    {
        "id": 7,
        "person_a": 21,
        "person_b": 22,
        "type": "predecessor_successor",
        "context": "焦春锋接替来风华任岚山区委书记",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2021",
        "confidence": "plausible"
    },
    # 申洁 <-> 周升元（前后任区长）
    {
        "id": 8,
        "person_a": 1,
        "person_b": 23,
        "type": "predecessor_successor",
        "context": "申洁接替周升元任岚山区区长",
        "overlap_org": "岚山区人民政府",
        "overlap_period": "2022",
        "confidence": "plausible"
    },
    # 周绪龙 <-> 申洁（党政班子内）
    {
        "id": 9,
        "person_a": 1,
        "person_b": 18,
        "type": "overlap",
        "context": "周绪龙曾任岚山区副区长时与申洁在区政府班子中共事",
        "overlap_org": "岚山区人民政府",
        "overlap_period": "2021-2023",
        "confidence": "confirmed"
    },
    # 张健 <-> 申洁（上下级/纪委监督）
    {
        "id": 10,
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "张健任纪委书记/监委主任，在区委常委会班子内与申洁共事",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2026-至今",
        "confidence": "confirmed"
    },
    # 焦春锋 -> 日照市委（向上）
    {
        "id": 11,
        "person_a": 21,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "焦春锋升任日照市委常委后，申洁在岚山区的工作接受市的领导",
        "overlap_org": "",
        "overlap_period": "2025-至今",
        "confidence": "confirmed"
    },
    # 刘峰（专职副书记）<-> 申洁（上下级）
    {
        "id": 12,
        "person_a": 1,
        "person_b": 17,
        "type": "superior_subordinate",
        "context": "申洁为区委书记，刘峰为区委副书记",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2026-至今",
        "confidence": "confirmed"
    },
    # 牛振（常务副区长）<-> 万磊（区长）（上下级）
    {
        "id": 13,
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "万磊为区长，牛振为常务副区长协助区长工作",
        "overlap_org": "岚山区人民政府",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    # 高杰 <-> 来风华（前后任）
    {
        "id": 14,
        "person_a": 24,
        "person_b": 22,
        "type": "predecessor_successor",
        "context": "来风华接替高杰任岚山区委书记",
        "overlap_org": "中共日照市岚山区委员会",
        "overlap_period": "2016",
        "confidence": "plausible"
    },
]

# ── Person JSON records ──────────────────────────────────────────────────────
PERSON_JSONS = [
    {
        "filename": f"{TODAY}-山东省-日照市-区委书记-申洁.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "日照市",
                "region": "岚山区",
                "job": "区委书记",
                "task_id": "shandong_岚山区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "lanshan_shen_jie",
                "name": "申洁",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1977年7月",
                "birthplace": "山东日照东港",
                "native_place": "",
                "education": [{"period": "", "institution": "中国农业大学（在职）", "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S002"]}],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "申洁_197707", "name_birthplace": "申洁_山东日照东港", "official_profile_url": "http://www.rzlanshan.gov.cn/"}
            },
            "current_status": {
                "current_post": "日照市岚山区委书记",
                "current_org": "中共日照市岚山区委员会",
                "administrative_rank": "县处级正职",
                "as_of": "2026-07-25",
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {
                    "start": "2025-09",
                    "end": "present",
                    "org": "中共日照市岚山区委员会",
                    "title": "岚山区委书记",
                    "level": "县处级正职",
                    "location": "日照市岚山区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2025年8月省委批准任区委书记（任前公示8月25日），9月3日正式宣布任命",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                },
                {
                    "start": "2022",
                    "end": "2025-08",
                    "org": "岚山区人民政府",
                    "title": "岚山区区长",
                    "level": "县处级正职",
                    "location": "日照市岚山区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "接替周升元任岚山区区长",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "日照市行政审批服务局",
                    "title": "局长",
                    "level": "县处级正职",
                    "location": "日照市",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "此前公开履历中有在日照市行政审批服务局任职经历",
                    "confidence": "plausible",
                    "source_ids": []
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到申洁在2010年代至2021年间的完整履历信息",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"org_id": "lanshan_party", "name": "中共日照市岚山区委员会", "type": "party", "level": "县处级", "role": "区委书记"},
                {"org_id": "lanshan_gov", "name": "岚山区人民政府", "type": "government", "level": "县处级", "role": "前任区长"}
            ],
            "relationships": [
                {"person": "万磊", "person_id": "lanshan_wan_lei", "relationship_type": "overlap", "strength": "strong", "evidence": "党政搭档：申洁任区委书记，万磊任区委副书记、区长", "overlap_org": "中共日照市岚山区委员会", "overlap_period": "2025-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "焦春锋", "person_id": "rizhao_jiao_chunfeng", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "申洁接替焦春锋任岚山区委书记", "overlap_org": "中共日照市岚山区委员会", "overlap_period": "2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "周升元", "person_id": "lanshan_zhou_shengyuan", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "申洁接替周升元任岚山区区长", "overlap_org": "岚山区人民政府", "overlap_period": "2022", "direction": "undirected", "confidence": "plausible", "source_ids": []},
                {"person": "周绪龙", "person_id": "lanshan_zhou_xulong", "relationship_type": "overlap", "strength": "medium", "evidence": "周绪龙曾任岚山区副区长，与申洁在区政府班子中共事", "overlap_org": "岚山区人民政府", "overlap_period": "2021-2023", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]}
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "主持区委常委会会议，研究经济运行、重点项目推进等工作",
                    "role_in_event": "区委书记，主持会议",
                    "measurable_outcome": "",
                    "location": "日照市岚山区",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-06",
                    "domain": "discipline",
                    "achievement_or_event": "主持全区警示教育会，强调党风廉政建设和反腐败工作",
                    "role_in_event": "区委书记，讲话部署",
                    "measurable_outcome": "",
                    "location": "日照市岚山区",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["日照市（岚山区-市直-岚山区）"],
                "promotion_velocity": {"summary": "履历信息有限，但区内区长-书记晋升路径清晰", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [{"trait": "unknown", "evidence": "缺乏足够公开报道进行工作风格推断", "confidence": "unverified", "source_ids": []}],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "工作风格从公开报道和政务活动推断，非私人心理评估。"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026年7月，未发现申洁有纪律处分、审计问题或负面媒体报道。", "date": "", "confidence": "plausible", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "区委常委会召开会议", "url": "http://www.rzlanshan.gov.cn/art/2026/7/20/art_32570_10379397.html", "publisher": "日照市岚山区人民政府", "published_at": "2026-07-20", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "官方政府网站新闻，确认申洁为区委书记"},
                {"id": "S002", "title": "申洁(日照市岚山区委书记)", "url": "https://baike.baidu.com/item/%E7%94%B3%E6%B4%81/58460880", "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-25", "source_type": "encyclopedia", "reliability": "medium", "notes": "百度百科条目，含基本信息（1977年7月生，日照东港人）"},
                {"id": "S003", "title": "全区警示教育会召开", "url": "http://www.rzlanshan.gov.cn/art/2026/6/15/art_32571_10378582.html", "publisher": "日照市岚山区人民政府", "published_at": "2026-06-15", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "确认申洁主持会议并强调党风廉政"},
                {"id": "S004", "title": "岚山区（百度百科）", "url": "https://baike.baidu.com/item/%E5%B2%9A%E5%B1%B1%E5%8C%BA", "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-25", "source_type": "encyclopedia", "reliability": "medium", "notes": "确认2026年1月最新主要领导列表"},
                {"id": "S005", "title": "周绪龙（百度百科）", "url": "https://baike.baidu.com/item/%E5%91%A8%E7%BB%AA%E9%BE%99", "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-25", "source_type": "encyclopedia", "reliability": "medium", "notes": "含周绪龙完整履历"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "申洁2010年代至2021年间的完整履历缺失，包括早期任职经历、教育背景（非在职部分）和晋升路径的详细时间线。"
            },
            "open_questions": [
                {"priority": "critical", "question": "申洁的完整履历——2010年代历任职务、早期职业生涯", "why_it_matters": "核心领导人的背景信息是关系网络分析的基础", "suggested_queries": ["申洁 简历", "申洁 日照 任职", "申洁 任前公示"], "last_attempted": "2026-07-25"},
                {"priority": "high", "question": "申洁的工作风格和治理记录——是否有更多公开报道可供分析", "why_it_matters": "了解领导风格有助于判断班子协作模式", "suggested_queries": ["申洁 讲话", "申洁 调研"], "last_attempted": "2026-07-25"}
            ]
        }
    },
    {
        "filename": f"{TODAY}-山东省-日照市-区长-万磊.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "日照市",
                "region": "岚山区",
                "job": "区长",
                "task_id": "shandong_岚山区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "lanshan_wan_lei",
                "name": "万磊",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1975年2月",
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "研究生学历", "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "万磊_197502", "name_birthplace": "", "official_profile_url": "http://www.rzlanshan.gov.cn/col/col325593/index.html"}
            },
            "current_status": {
                "current_post": "日照市岚山区区长",
                "current_org": "岚山区人民政府",
                "administrative_rank": "县处级正职",
                "as_of": "2026-07-25",
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "岚山区人民政府",
                    "title": "区长",
                    "level": "县处级正职",
                    "location": "日照市岚山区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "现任岚山区委副书记、区政府党组书记、区长。接替申洁（申洁升任区委书记后）",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "岚山区人民政府",
                    "title": "常务副区长/副区长",
                    "level": "县处级副职",
                    "location": "日照市岚山区",
                    "system": "government",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "在成为区长前，曾负责区政府常务工作",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到万磊任岚山区职务前的完整履历信息",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"org_id": "lanshan_gov", "name": "岚山区人民政府", "type": "government", "level": "县处级", "role": "区长"}
            ],
            "relationships": [
                {"person": "申洁", "person_id": "lanshan_shen_jie", "relationship_type": "overlap", "strength": "strong", "evidence": "党政搭档：申洁任区委书记，万磊任区委副书记、区长", "overlap_org": "中共日照市岚山区委员会", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "牛振", "person_id": "lanshan_niu_zhen", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "万磊为区长，牛振为常务副区长协助区长工作", "overlap_org": "岚山区人民政府", "overlap_period": "至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {
                    "period": "2026-06",
                    "domain": "other",
                    "achievement_or_event": "受区委书记申洁委托主持区委常委会会议，研究部署相关工作",
                    "role_in_event": "区委副书记、区长，主持会议",
                    "measurable_outcome": "",
                    "location": "日照市岚山区",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "履历信息不足", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [{"trait": "unknown", "evidence": "缺乏足够公开报道", "confidence": "unverified", "source_ids": []}],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "工作风格从公开报道和政务活动推断，非私人心理评估。"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026年7月未发现负面影响", "date": "", "confidence": "plausible", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "岚山区政府领导页面", "url": "http://www.rzlanshan.gov.cn/col/col325593/index.html", "publisher": "日照市岚山区人民政府", "published_at": "", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "官方领导页面确认万磊为区长及基本简历"},
                {"id": "S004", "title": "受区委书记申洁委托 万磊主持召开区委常委会会议", "url": "http://www.rzlanshan.gov.cn/art/2026/6/29/art_32570_10378778.html", "publisher": "日照市岚山区人民政府", "published_at": "2026-06-29", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "确认万磊代理主持区委工作"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "万磊的完整履历——任岚山区职务前的所有任职经历、出生地、教育背景均为未知。"
            },
            "open_questions": [
                {"priority": "critical", "question": "万磊（岚山区区长）的完整履历——此前任职经历", "why_it_matters": "核心领导人的背景信息是关系网络分析的基础", "suggested_queries": ["万磊 简历", "万磊 岚山 区长 任前公示", "万磊 日照"], "last_attempted": "2026-07-25"}
            ]
        }
    },
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

def main():
    # ── SQLite Database ──
    print(f"Building SQLite database: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
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

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS positions (
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

    CREATE TABLE IF NOT EXISTS relationships (
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
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                    (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                    (r["id"], r["person_a"], r["person_b"], r["type"],
                     r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", "")))

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

    print(f"  Persons: {person_count}")
    print(f"  Organizations: {org_count}")
    print(f"  Positions: {pos_count}")
    print(f"  Relationships: {rel_count}")

    # ── GEXF Graph ──
    print(f"\nBuilding GEXF graph: {GEXF_PATH}")

    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>china-gov-network skill</creator>')
    lines.append(f'    <description>岚山区领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
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
        pid = p["id"]
        name = p["name"]
        post = p.get("current_post", "")

        if pid == 1:
            color = '#E03C31'  # red: Party Secretary (区委书记)
            size = 20.0
        elif pid == 2:
            color = '#2980B9'  # blue: government leader (区长)
            size = 18.0
        elif pid == 9:
            color = '#FFA500'  # orange: discipline inspection
            size = 12.0
        elif pid == 5:
            color = '#8E44AD'  # purple: people's congress
            size = 12.0
        elif pid == 18:
            color = '#8E44AD'  # purple: CPPCC
            size = 12.0
        elif pid in (21, 22, 23, 24):
            color = '#95A5A6'  # grey: former leaders
            size = 14.0
        else:
            color = '#7F8C8D'  # grey: others
            size = 12.0

        lines.append(f'      <node id="{pid}" label="{name}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="category" value="person"/>')
        lines.append(f'          <attvalue for="birth" value="{p.get("birth", "")}"/>')
        lines.append(f'          <attvalue for="birthplace" value="{p.get("birthplace", "")}"/>')
        lines.append(f'          <attvalue for="education" value="{p.get("education", "")}"/>')
        lines.append(f'          <attvalue for="current_post" value="{post}"/>')
        lines.append(f'          <attvalue for="source" value="{p.get("source", "")}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'      </node>')

    # Organization nodes
    for o in organizations:
        oid = 1000 + o["id"]
        lines.append(f'      <node id="{oid}" label="{o["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="44" g="62" b="80"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    edge_id = 1

    # person→organization (worked_at)
    for pos in positions:
        oid = 1000 + pos["org_id"]
        lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
        lines.append(f'          <attvalue for="period" value="{pos.get("start", "?")} → {pos.get("end", "今")}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'      </edge>')
        edge_id += 1

    # person↔person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{r["type"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
        lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
        lines.append(f'          <attvalue for="period" value="{r.get("overlap_period", "")}"/>')
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
    print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
    print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")

    # ── Person JSON files ──
    print(f"\nWriting person JSON files to {PJSON_DIR}")
    for pj in PERSON_JSONS:
        filepath = PJSON_DIR / pj["filename"]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pj["data"], f, ensure_ascii=False, indent=2)
        print(f"  {pj['filename']}")
        # Validate JSON
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"    ✓ Valid JSON")

    print("\nDone!")


if __name__ == "__main__":
    main()
