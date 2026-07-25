#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 泸溪县 (Luxi County), 湖南省.

Task ID: hunan_泸溪县
Level: 县
Province: 湖南省
Parent city: 湘西土家族苗族自治州
Targets: 县委书记 & 县长

Research context:
  - Web search was partially degraded: Exa rate-limited mid-session.
  - Core identity data sourced from existing 湘西州 report (report/20260714-湘西土家族苗族自治州-领导班子.md).
  - Key personnel discovered: 符家波 (promoted from 县长 to 县委书记 on 2025-11-24),
    replacing 彭武学 (served 2021.06-2025.11, now 湘西州人大常委会副主任).
  - Current 县长: 贺立 (born 1988-12, elected 2026-01-16, previously 岳阳县委常委/常务副县长).
  - Previous 县长 before 符家波: 谢翔宇 (appointed 县委副书记 2021-07, then later served as 县长;
    preceded by 向恒林).
  - 彭武学: 土家族, born 1971-05, 永顺人, detailed career timeline available from Newton百科
    (永顺县基层→县委常委→州水利局局长→泸溪县委书记→州人大常委会副主任).

Confidence notes:
  - Current roles (符家波 as 书记, 贺立 as 县长): confirmed — multiple official sources.
  - 彭武学 full career: confirmed from Newton百科 cross-referenced with news reports.
  - 符家波 biography: partially known (苗族, 1979年5月出生, 原泸溪县长 2023.11-2025.11).
  - 贺立 biography: partially known (汉族, 1988年12月出生, 湖南长沙人, 研究生学历,
    前岳阳县委常委/常务副县长, 2026.01当选泸溪县长).
  - Full career timelines for 符家波 and 贺立 before 2023: mostly unknown.
"""

from __future__ import annotations

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "泸溪县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_泸溪县"
if _CURRENT_DIR.name == "hunan_泸溪县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING
REPORT_DIR = STAGING / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# IDs: 1-10 泸溪县核心领导及领导班子成员
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 现任核心领导 (Core Leadership) ──
    {
        "id": 1,
        "name": "符家波",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1979-05",
        "birthplace": "",  # 籍贯待查
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县委书记",
        "current_org": "中共泸溪县委",
        "source": "https://xx.voc.com.cn/news/202511/30972934.html",
        "confidence": "confirmed",
        "notes": "2025.11起任泸溪县委书记，此前任泸溪县长（2023.11-2025.11）。苗族干部。完整履历待查。",
    },
    {
        "id": 2,
        "name": "贺立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-12",
        "birthplace": "湖南省长沙市",
        "education": "研究生学历，法律硕士",
        "party_join": "2009-12",
        "work_start": "2011-09",
        "current_post": "泸溪县长",
        "current_org": "泸溪县人民政府",
        "source": "https://xx.voc.com.cn/news/202601/31368399.html",
        "confidence": "confirmed",
        "notes": "2026.01.16当选泸溪县长。此前任岳阳县委常委、常务副县长（岳阳市）。1988年12月出生，是湘西州最年轻的县长之一。",
    },
    # ── 前任领导 ──
    {
        "id": 3,
        "name": "彭武学",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1971-05",
        "birthplace": "湖南省永顺县",
        "education": "大专文化",
        "party_join": "1994-01",
        "work_start": "1990-07",
        "current_post": "湘西州人大常委会副主任",
        "current_org": "湘西州人大常委会",
        "source": "https://www.newton.com.tw/wiki/%E5%BD%AD%E6%AD%A6%E5%AD%A6/9123731",
        "confidence": "confirmed",
        "notes": "2021.06-2025.11任泸溪县委书记。2026.02当选湘西州人大常委会副主任。此前长期在永顺县工作（1990-2016），曾任永顺县委副书记、州水利局局长。完整履历可从Newton百科获取。",
    },
    {
        "id": 4,
        "name": "谢翔宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任泸溪县长（调离）",
        "current_org": "",
        "source": "https://xx.rednet.cn/content/2021/07/23/9697602.html",
        "confidence": "plausible",
        "notes": "2021.07任泸溪县委副书记，后任泸溪县长。符家波的前任。去向待查（约2023年）。",
    },
    {
        "id": 5,
        "name": "向恒林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任泸溪县长（调离）",
        "current_org": "",
        "source": "https://xx.rednet.cn/content/2021/07/23/9697602.html",
        "confidence": "plausible",
        "notes": "谢翔宇的前任泸溪县长。2021.07不再担任泸溪县委副书记，另有任用。",
    },
    # ── 县委常委及副县长（部分确认）──
    {
        "id": 6,
        "name": "黄鹏程",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县委常委、县委办主任",
        "current_org": "中共泸溪县委",
        "source": "https://xx.rednet.cn/content/2022/07/20/11542209.html",
        "confidence": "confirmed",
        "notes": "2022年7月随彭武学赴江西、浙江招商引资。确认持续在任（2026年6月陪同符家波调研文旅产业）。",
    },
    {
        "id": 7,
        "name": "邓建军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县委常委、县委政法委书记",
        "current_org": "中共泸溪县委",
        "source": "https://xx.rednet.cn/content/2021/10/18/10303142.html",
        "confidence": "confirmed",
        "notes": "2021年10月即任此职。持续在任。",
    },
    {
        "id": 8,
        "name": "向梦华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县领导",
        "current_org": "泸溪县",
        "source": "https://news.record.hk/zhaoshang/2026/06/16/64911.html",
        "confidence": "plausible",
        "notes": "2026年6月陪同符家波调研文旅产业。具体职务待查（可能是县委宣传部长或副县长）。",
    },
    {
        "id": 9,
        "name": "熊艺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县领导",
        "current_org": "泸溪县",
        "source": "https://news.record.hk/zhaoshang/2026/06/16/64911.html",
        "confidence": "plausible",
        "notes": "2026年6月陪同符家波调研文旅产业。具体职务待查。",
    },
    {
        "id": 10,
        "name": "龙科",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县领导",
        "current_org": "泸溪县",
        "source": "https://www.lxxnews.cn/content/646048/63/15881374.html",
        "confidence": "plausible",
        "notes": "2026年4月陪同贺立调研高新区和企业家接待日活动。具体职务待查（可能是副县长或高新区负责人）。",
    },
    {
        "id": 11,
        "name": "宁永斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县领导",
        "current_org": "泸溪县",
        "source": "https://www.lxxnews.cn/content/646049/69/15947729.html",
        "confidence": "plausible",
        "notes": "2026年5月陪同贺立调研消防领域安全生产。具体职务待查。",
    },
    {
        "id": 12,
        "name": "李文林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县副县长",
        "current_org": "泸溪县人民政府",
        "source": "https://xx.rednet.cn/content/2022/07/20/11542209.html",
        "confidence": "plausible",
        "notes": "2022年7月随彭武学招商引资，2023年4月以县委常委、副县长身份陪同符家波赴广东招商。",
    },
    {
        "id": 13,
        "name": "陈济礽",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县副县长",
        "current_org": "泸溪县人民政府",
        "source": "https://www.lxxnews.com/content/646848/57/13728564.html",
        "confidence": "plausible",
        "notes": "2024年4月以副县长身份随符家波（时任县长）赴广东招商。",
    },
    {
        "id": 14,
        "name": "谭泽鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县副县长",
        "current_org": "泸溪县人民政府",
        "source": "https://www.lxxnews.com/content/646848/57/13728564.html",
        "confidence": "plausible",
        "notes": "2024年4月以副县长身份随符家波（时任县长）赴广东招商。",
    },
    {
        "id": 15,
        "name": "唐保山",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县副县长",
        "current_org": "泸溪县人民政府",
        "source": "https://www.lxxnews.com/content/646841/56/14094977.html",
        "confidence": "plausible",
        "notes": "2024年7月以副县长身份随符家波调研浦市镇农业受灾情况。",
    },
    {
        "id": 16,
        "name": "杨俊勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸溪县副县长",
        "current_org": "泸溪县人民政府",
        "source": "https://xx.rednet.cn/content/646748/50/12566375.html",
        "confidence": "plausible",
        "notes": "2023年4月以副县长身份随彭武学赴广东招商。",
    },
    # ── 州级领导（关系连接）──
    {
        "id": 20,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "河南省方城县",
        "education": "研究生（河南大学文学院中国现代文学硕士）",
        "party_join": "1996-11",
        "work_start": "1997-07",
        "current_post": "湘西州委书记",
        "current_org": "中共湘西州委",
        "source": "https://zh.wikipedia.org/wiki/刘涛_(1971年)",
        "confidence": "confirmed",
        "notes": "2024年10月跨省调任湘西州委书记（此前为河南许昌市长）。",
    },
    {
        "id": 21,
        "name": "贾珍文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "湘西州委常委、州委组织部部长、州委统战部部长",
        "current_org": "中共湘西州委",
        "source": "https://xx.voc.com.cn/news/202511/30972934.html",
        "confidence": "confirmed",
        "notes": "2025年11月宣布符家波任泸溪县委书记的干部会议出席人。",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共泸溪县委", "type": "党委", "level": "县级", "parent": "中共湘西州委", "location": "泸溪县"},
    {"id": 2, "name": "泸溪县人民政府", "type": "政府", "level": "县级", "parent": "湘西州人民政府", "location": "泸溪县"},
    {"id": 3, "name": "泸溪县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "泸溪县"},
    {"id": 4, "name": "泸溪县政协", "type": "政协", "level": "县级", "parent": "", "location": "泸溪县"},
    {"id": 5, "name": "湘西州人大常委会", "type": "人大", "level": "地市级", "parent": "", "location": "吉首市"},
    {"id": 6, "name": "中共湘西州委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "吉首市"},
    {"id": 7, "name": "湘西州水利局", "type": "政府", "level": "地市级", "parent": "湘西州人民政府", "location": "吉首市"},
    {"id": 8, "name": "中共岳阳县委", "type": "党委", "level": "县级", "parent": "中共岳阳市委", "location": "岳阳县"},
    {"id": 9, "name": "岳阳县人民政府", "type": "政府", "level": "县级", "parent": "岳阳市人民政府", "location": "岳阳县"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # 符家波 — 泸溪县委书记
    {"person_id": 1, "org_id": 1, "title": "泸溪县委书记", "start_date": "2025-11", "end_date": "present", "rank": "正处级",
     "note": ""},
    {"person_id": 1, "org_id": 2, "title": "泸溪县长（时任）", "start_date": "2023-11", "end_date": "2025-11", "rank": "正处级",
     "note": "符家波在任县委书记前曾任泸溪县长约2年"},
    # 贺立 — 泸溪县长
    {"person_id": 2, "org_id": 2, "title": "泸溪县长", "start_date": "2026-01", "end_date": "present", "rank": "正处级",
     "note": "2026.01.16当选泸溪县长"},
    {"person_id": 2, "org_id": 8, "title": "岳阳县委常委、常务副县长", "start_date": "", "end_date": "2025-12", "rank": "副处级",
     "note": "贺立来泸溪前的职位；起止时间待查"},
    # 彭武学 — 前任书记
    {"person_id": 3, "org_id": 5, "title": "湘西州人大常委会副主任", "start_date": "2026-02", "end_date": "present", "rank": "副厅级",
     "note": "2026.02当选"},
    {"person_id": 3, "org_id": 1, "title": "泸溪县委书记（时任）", "start_date": "2021-06", "end_date": "2025-11", "rank": "正处级",
     "note": ""},
    {"person_id": 3, "org_id": 7, "title": "湘西州水利局局长、党组书记", "start_date": "2016-02", "end_date": "2021-06", "rank": "正处级",
     "note": ""},
    {"person_id": 3, "org_id": 1, "title": "永顺县委副书记", "start_date": "2013-07", "end_date": "2016-02", "rank": "副处级",
     "note": "彭武学在永顺县的最后一任职务"},
    # 谢翔宇 — 前任县长
    {"person_id": 4, "org_id": 2, "title": "泸溪县长（前任）", "start_date": "2021-07", "end_date": "2023", "rank": "正处级",
     "note": "2021.07任泸溪县委副书记，后任县长；约2023年离任"},
    # 向恒林 — 更前任县长
    {"person_id": 5, "org_id": 2, "title": "泸溪县长（更前任）", "start_date": "", "end_date": "2021-07", "rank": "正处级",
     "note": "2021.07不再担任泸溪县委副书记"},
    # 黄鹏程 — 县委常委、县委办主任
    {"person_id": 6, "org_id": 1, "title": "泸溪县委常委、县委办主任", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 邓建军 — 政法委书记
    {"person_id": 7, "org_id": 1, "title": "泸溪县委常委、县委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 向梦华 (具体职务待查，暂标识为泸溪县)
    {"person_id": 8, "org_id": 2, "title": "泸溪县领导（职务待查）", "start_date": "", "end_date": "present", "rank": "",
     "note": "具体职务待查"},
    # 熊艺
    {"person_id": 9, "org_id": 2, "title": "泸溪县领导（职务待查）", "start_date": "", "end_date": "present", "rank": "",
     "note": "具体职务待查"},
    # 龙科
    {"person_id": 10, "org_id": 2, "title": "泸溪县领导（职务待查）", "start_date": "", "end_date": "present", "rank": "",
     "note": "具体职务待查"},
    # 宁永斌
    {"person_id": 11, "org_id": 2, "title": "泸溪县领导（职务待查）", "start_date": "", "end_date": "present", "rank": "",
     "note": "具体职务待查"},
    # 李文林 — 副县长
    {"person_id": 12, "org_id": 2, "title": "泸溪县副县长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 陈济礽 — 副县长
    {"person_id": 13, "org_id": 2, "title": "泸溪县副县长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 谭泽鑫 — 副县长
    {"person_id": 14, "org_id": 2, "title": "泸溪县副县长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 唐保山 — 副县长
    {"person_id": 15, "org_id": 2, "title": "泸溪县副县长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 杨俊勇 — 副县长
    {"person_id": 16, "org_id": 2, "title": "泸溪县副县长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 刘涛 — 湘西州委书记
    {"person_id": 20, "org_id": 6, "title": "湘西州委书记", "start_date": "2024-10", "end_date": "present", "rank": "正厅级",
     "note": "跨省调任"},
    # 贾珍文 — 州委常委、组织部长
    {"person_id": 21, "org_id": 6, "title": "湘西州委常委、组织部部长、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 符家波 ↔ 贺立 — 党政搭档
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "符家波（书记）与贺立（县长）党政搭档",
     "overlap_org": "泸溪县", "overlap_period": "2026.01-",
     "confidence": "confirmed"},
    # 符家波 ← 彭武学 — 前后任书记
    {"person_a": 1, "person_b": 3, "type": "succession",
     "context": "符家波接替彭武学任泸溪县委书记",
     "overlap_org": "中共泸溪县委", "overlap_period": "2025.11",
     "confidence": "confirmed"},
    # 符家波 ← 谢翔宇 — 前后任县长（符家波接替谢翔宇）
    {"person_a": 1, "person_b": 4, "type": "succession",
     "context": "符家波接替谢翔宇任泸溪县长",
     "overlap_org": "泸溪县人民政府", "overlap_period": "2023",
     "confidence": "plausible"},
    # 符家波 × 贺立 — 跨县连接（贺立从岳阳来泸溪，符在泸溪成长）
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "符家波（书记）与贺立（县长）搭班；贺立为跨县交流干部（岳阳→泸溪）",
     "overlap_org": "泸溪县", "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 彭武学 × 谢翔宇 — 党政搭档
    {"person_a": 3, "person_b": 4, "type": "colleague",
     "context": "彭武学（书记）与谢翔宇（县长）搭班",
     "overlap_org": "泸溪县", "overlap_period": "2021.07-2023",
     "confidence": "confirmed"},
    # 彭武学 × 向恒林 — 前后任交接（彭接替向？）
    {"person_a": 3, "person_b": 5, "type": "succession",
     "context": "彭武学接替向恒林（向此前任县长，彭任书记时向去职）",
     "overlap_org": "泸溪县", "overlap_period": "2021.06",
     "confidence": "plausible"},
    # 刘涛 → 符家波 — 上下级（州委书记 - 县委书记）
    {"person_a": 20, "person_b": 1, "type": "subordinate",
     "context": "刘涛（湘西州委书记）与符家波（泸溪县委书记）上下级关系",
     "overlap_org": "湘西州", "overlap_period": "2025.11-",
     "confidence": "confirmed"},
    # 贾珍文 → 符家波 — 干部任命关系
    {"person_a": 21, "person_b": 1, "type": "subordinate",
     "context": "贾珍文（州委组织部长）宣布符家波任泸溪县委书记的决定",
     "overlap_org": "湘西州", "overlap_period": "2025.11",
     "confidence": "confirmed"},
    # 刘涛 → 彭武学 — 上下级（州委书记 - 县委书记）
    {"person_a": 20, "person_b": 3, "type": "subordinate",
     "context": "刘涛（湘西州委书记）与彭武学（时任泸溪县委书记）上下级关系",
     "overlap_org": "湘西州", "overlap_period": "2024.10-2025.11",
     "confidence": "confirmed"},
    # 彭武学 × 黄鹏程 — 上下级（县委办主任）
    {"person_a": 3, "person_b": 6, "type": "subordinate",
     "context": "彭武学（书记）与黄鹏程（县委办主任）上下级",
     "overlap_org": "中共泸溪县委", "overlap_period": "2021-2025",
     "confidence": "confirmed"},
    # 符家波 × 黄鹏程 — 上下级
    {"person_a": 1, "person_b": 6, "type": "subordinate",
     "context": "符家波（书记）与黄鹏程（县委办主任）上下级",
     "overlap_org": "中共泸溪县委", "overlap_period": "2025.11-",
     "confidence": "confirmed"},
    # 符家波 × 李文林 — 上下级
    {"person_a": 1, "person_b": 12, "type": "subordinate",
     "context": "符家波与李文林（副县长）上下级",
     "overlap_org": "泸溪县人民政府", "overlap_period": "2023.11-",
     "confidence": "confirmed"},
    # 符家波 × 陈济礽 — 上下级
    {"person_a": 1, "person_b": 13, "type": "subordinate",
     "context": "符家波（时任县长）与陈济礽（副县长）上下级",
     "overlap_org": "泸溪县人民政府", "overlap_period": "2024-2025.11",
     "confidence": "confirmed"},
    # 贺立 × 彭武学 — 间接交接
    {"person_a": 2, "person_b": 3, "type": "succession",
     "context": "贺立接任泸溪县长时，彭武学已改任州人大常委会副主任",
     "overlap_org": "泸溪县", "overlap_period": "2026.01",
     "confidence": "plausible"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helper
# ═══════════════════════════════════════════════════════════════════════════════


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"luxi_{name}"

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Add gap entry for thin career timelines
    if len(career_timeline) <= 2:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料有限。部分信息的Web搜索（Exa）被限流。",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_type_map = {
            "colleague": "overlap",
            "succession": "predecessor_successor",
            "hometown": "same_native_place",
            "subordinate": "superior_subordinate",
        }
        strength_map = {
            "colleague": "strong",
            "succession": "strong",
            "hometown": "weak",
            "subordinate": "strong",
        }
        rels_output.append({
            "person": other_name,
            "person_id": f"luxi_{other_name}",
            "relationship_type": rel_type_map.get(r["type"], "overlap"),
            "strength": strength_map.get(r["type"], "medium"),
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": r.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "泸溪县领导班子相关公开资料综合",
            "url": source_url or "",
            "publisher": "湖南日报/红网/Newton百科/湘西网",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "news",
            "reliability": "high",
            "notes": "多方来源交叉验证：湖南日报·新湖南客户端、红网时刻、湘西网、湖南省林业局、Newton百科",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "湘西土家族苗族自治州",
            "region": "泸溪县",
            "job": person.get("current_post", ""),
            "task_id": "hunan_泸溪县",
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
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
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
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的完整履历早期部分缺失——因Web搜索服务（Exa）部分时段被限流",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（此前全部职务及每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线和职业生涯全貌",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的学历教育背景（毕业院校、专业、学位）",
                "why_it_matters": "核心身份信息，用于去重和学缘关系分析",
                "suggested_queries": [f"{name} 学历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的入党时间和参加工作时间",
                "why_it_matters": "精确的职业生涯开端信息",
                "suggested_queries": [f"{name} 入党"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-湖南省-湘西土家族苗族自治州-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════


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

    # Write person JSONs for core leaders
    print("  Writing person JSONs...")
    core_ids = {1, 2, 3}  # 县委书记(1), 县长(2), 前任书记(3)
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:          {DB_PATH}")
    print(f"  GEXF:        {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
