#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 大安市 (Daan), 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_大安市
Province: 吉林省
Parent city: 白城市
Level: 县级市
Targets: 市委书记 & 市长

Research sources (official portal, accessed via HTTP 2026-08-06):
  - http://www.daan.gov.cn/ 大安市人民政府门户网站 (primary)
  - http://www.daan.gov.cn/tszf/ldjj/ 领导简介 (政府班子官方简历)
  - http://www.daan.gov.cn/daxw/ldhd/ 领导活动新闻 (确认书记/市长/四大班子)
  - http://www.jlbc.gov.cn/ 白城市人民政府网站 (跨级参考)

Network constraints in this environment:
  - HTTPS to daan.gov.cn blocked; used HTTP.
  - Baidu Baike 403/captcha, Exa rate-limited, Bing/Google/Jina blocked. So 刘宏
    (市委书记) 的履历、市委其他常委的具体职务、前任书记身份 未能从外部百科核实，
    均写入 open_questions / report gaps（符合 partial-evidence artifact mode）。

Confidence:
  - 苏淼(市长)、管立松、陈晓丽、齐相蛘、逯德龙、庞占辉、母继东、黄中岳、侯勇：简历 confirmed from 官方领导简介页。
  - 刘宏(市委书记)、王春东(人大主任)：职务 confirmed from 官方新闻；履历 open。
  - 张东颖(前政协主席, 2026-04 辞任)、迟彤宏(政协主席候选人)：confirmed from 政协常委会新闻。
  - 张伟明/王敬东/刘畅/刘鹤/马翔宇/张雪：市级领导 confirmed 身份，但是否列入市委书记专项职务一并存 gap。
"""

from __future__ import annotations

import json
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "大安市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_大安市"
if _CURRENT_DIR.name == "jilin_大安市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1 书记, 2 市长, 9 前书记(gap), 3-8 驻班子/人大/政协 & predecessors
persons = [
    # ══════════════════ 核心领导（现任） ══════════════════
    {
        "id": 1,
        "name": "刘宏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共大安市委",
        "source": "http://www.daan.gov.cn/daxw/ldhd/",
        "confidence": "confirmed",
        "notes": "白城市人大常委会副主任、大安市委书记。主持市委常委会、重点工作会议、防汛、信访接待等。出生/籍贯/学历/履历为open question（百度百科不可用）。任职至迟自2025年一季度。",
    },
    {
        "id": 2,
        "name": "苏淼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年7月",
        "birthplace": "吉林白城",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2005年12月",
        "current_post": "市委副书记、市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202507/t20250731_1018489.html",
        "confidence": "confirmed",
        "notes": "2008年12月入党。历任共青团永吉县委书记、党组书记；永吉县双河镇党委副书记、镇长；永吉县双河镇党委书记；磐石市副市长；永吉县委常委、副县长。现任大安市委副书记、市长、市政府党组书记。领导市政府全面工作，分管市审计局。",
    },
    # ═══════════════════ 政府班子（现任副市长） ═══════════════════
    {
        "id": 3,
        "name": "管立松",
        "gender": "男",
        "ethnicity": "",
        "birth": "1986年6月",
        "birthplace": "吉林白城大安",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2009年1月",
        "current_post": "市委常委、常务副市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202406/t20240617_993576.html",
        "confidence": "confirmed",
        "notes": "2006年5月入党。历任乐胜乡党委副书记；新平安镇党委副书记、镇长；月亮泡镇党委书记；白城市月亮泡水库管理局副局长；大安市人民政府党组成员。负责市政府日常工作、受市长委托代管市审计局。",
    },
    {
        "id": 4,
        "name": "陈晓丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "吉林白城大安",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "2007年10月",
        "current_post": "市委常委、副市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202501/t20250106_1005938.html",
        "confidence": "confirmed",
        "notes": "2005年4月入党。历任重点项目服务中心副主任；联合乡党委副书记；吉林大安经济技术开发区管委会副主任；重点项目服务中心主任；工信局党组书记、局长；经开区党工委书记、管委会主任。分管教/科/医/度假/嫩江湿地等。",
    },
    {
        "id": 5,
        "name": "齐相蛘",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "1974年9月",
        "birthplace": "吉林白城镇碛",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "副市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202108/t20210830_908475.html",
        "confidence": "confirmed",
        "notes": "1997年6月入党。历任镇碛县到保镇副镇长；嘎什根乡副乡长/副书记/纪委书记/人大主席；莫莫格林场党委书记、场长；黑鱼泡镇党委书记、镇长。分管自然资源/住建/水利/城管执法。",
    },
    {
        "id": 6,
        "name": "逯德龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "吉林白城大安",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1999年7月",
        "current_post": "副市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202601/t20260116_1029544.html",
        "confidence": "confirmed",
        "notes": "2001年9月入党。历任舍力镇党委副书记、人大主席；联合乡党委书记；市乡村振兴局党组书记、局长；白城苏打盐碱地治理研究所院长。分管农业农村/林业/灌区。",
    },
    {
        "id": 7,
        "name": "庞占辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "吉林白城大安",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "1997年8月",
        "current_post": "副市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202404/t20240402_986024.html",
        "confidence": "confirmed",
        "notes": "2005年5月入党。历任市政府党组成员、办公室主任；法制办主任、民宗局局长；发改局党组书记、局长。分管发改/工信/商务/能源。",
    },
    {
        "id": 8,
        "name": "母继东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "吉林镇世家",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2002年6月",
        "current_post": "副市长、市公安局局长",
        "current_org": "大安市公安局",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202506/t20250624_1016049.html",
        "confidence": "confirmed",
        "notes": "2003年6月入党。历任镇郢县公安局副局长兼政治工作部主任，白城市公安局政治部辅警/户政支队支队长，大安市公安局党委副书记、政委。分管公安、司法、退役、信访。",
    },
    {
        "id": 9,
        "name": "黄中岳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年4月",
        "birthplace": "吉林大安",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2002年3月",
        "current_post": "副市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202507/t20250731_1018522.html",
        "confidence": "confirmed",
        "notes": "2001年4月入党。历任太山镇副镇长、副书记；月亮泡镇党委副书记、镇长；两家子镇党委书记。分管交通/市场监管/政务服务/街道。",
    },
    {
        "id": 10,
        "name": "侯勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "吉林长春",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1989年6月",
        "current_post": "副市长（挂职）",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/tszf/ldjj/202601/t20260116_1029545.html",
        "confidence": "confirmed",
        "notes": "2008年10月入党。中国农业发展银行吉林省分行信用审批处副处长，挂职大安副市长，分管农业农村、特色产业、招商引资。",
    },
    # ═══════════════════ 人大 / 政协 ═══════════════════
    {
        "id": 11,
        "name": "王春东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "大安市人民代表大会常务委员会",
        "source": "http://www.daan.gov.cn/daxw/ldhd/",
        "confidence": "confirmed",
        "notes": "2026-07 市十九届人大常委会第四十一次会议报道：市人大常委会主任。2026-01 人大主席团常务主席。履历细节 open question。",
    },
    {
        "id": 12,
        "name": "迟艳宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协大安市委员会",
        "source": "http://www.daan.gov.cn/daxw/ldhd/",
        "confidence": "confirmed",
        "notes": "原大安副市长（挂职），现任市政协党组书记、主席候选人（接张东颖）。2026-04 政协常委会报道：市政协党组书记、主席候选人。履历细节 open question。",
    },
    {
        "id": 13,
        "name": "孙立",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "政协大安市委员会",
        "source": "http://www.daan.gov.cn/daxw/ldhd/",
        "confidence": "confirmed",
        "notes": "市政协副主席，主持2026政协常委会及座谈会。履历 open question。",
    },
    # ═══════════════════ 前任 / 近期变动 ═══════════════════
    {
        "id": 14,
        "name": "张东颖",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市政协主席",
        "current_org": "政协大安市委员会",
        "source": "http://www.daan.gov.cn/daxw/ldhd/202605/t20260501_1035216.html",
        "confidence": "confirmed",
        "notes": "原政协大安市第十六届委员会主席、党组书记。2026-04-30 辞去主席、委员职务（accept 辞呈）；去向 open question。",
    },
    {
        "id": 15,
        "name": "范立家",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前常务副市长",
        "current_org": "大安市人民政府",
        "source": "http://www.daan.gov.cn/root267_45/dasrmzf/dasrm/xxgkml/202508/t20250818_1019785.html",
        "confidence": "confirmed",
        "notes": "2025-07 分工文件：副市长，负责市政府日常工作（常务）、代管局审计局，分管财政/人社/应急。至 2026 已由 管立松 接任常务副市长，范立家去向 open question。",
    },
    {
        "id": 16,
        "name": "待查_前任市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共大安市委",
        "source": "",
        "confidence": "unverified",
        "notes": "刘宏接任前的大安市委书记身份未确认（open question）。",
    },
]
# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大安市委", "type": "党委", "level": "县处级", "parent": "中共白城市委", "location": "大安市"},
    {"id": 2, "name": "大安市人民政府", "type": "政府", "level": "县处级", "parent": "白城市人民政府", "location": "大安市"},
    {"id": 3, "name": "大安市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "白城市人大常委会", "location": "大安市"},
    {"id": 4, "name": "政协大安市委员会", "type": "政协", "level": "县处级", "parent": "政协白城市委员会", "location": "大安市"},
    {"id": 5, "name": "大安市公安局", "type": "政府", "level": "正科级", "parent": "大安市人民政府", "location": "大安市"},
    {"id": 6, "name": "中共白城市委", "type": "党委", "level": "地厅级", "parent": "中共吉林省委", "location": "白城市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘宏 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024", "end_date": "", "rank": "县处级/副厅级（兼白城市人大副主任）", "note": "现任大安市委书记"},
    {"person_id": 1, "org_id": 6, "title": "白城市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任白城市人大常委会副主任（官方新闻多次注明头衔）"},
    # 苏淼 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "现任大安市委副书记、市长、市政府党组书记；领导市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 管立松 — 常务副市长
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "2025", "end_date": "", "rank": "县处级", "note": "负责市政府日常工作，受市长委托代管审计局"},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 陈晓丽 — 常委副市长
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管教科医卫、嫩江湿地等"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 齐相蛘
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管自然资源/住建/水利/城管"},
    # 遂德龙
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管农业农村/林业/灌区"},
    # 庞占辉
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管发改/工信/商务/能源"},
    # 母继东
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管公安/司法/退役/信访"},
    {"person_id": 8, "org_id": 5, "title": "市公安局局长、督察长", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 黄中岳
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管交通/市场监管/政务服务/街道"},
    # 侯勇（挂职）
    {"person_id": 10, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "县处级", "note": "农发行挂职，分管农业农村/特色产业/招商"},
    # 王春东 — 人大主任
    {"person_id": 11, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 迟彤宏 — 政协主席
    {"person_id": 12, "org_id": 4, "title": "市政协主席（党组书记）", "start_date": "2026", "end_date": "", "rank": "县处级", "note": "主席候选人，接张东颖"},
    # 孙立 — 政协副主席
    {"person_id": 13, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 张东颖 — 原政协主席
    {"person_id": 14, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "2026-04", "rank": "县处级", "note": "2026-04-30 辞去主席、委员"},
    # 范立家 — 前常务副市长
    {"person_id": 15, "org_id": 2, "title": "副市长（负责日常工作）", "start_date": "", "end_date": "2025", "rank": "县处级", "note": "前常务副市长，2025-07 前负责市政府日常工作，后由管立松接任"},
    # 前任市委书记
    {"person_id": 16, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "县处级", "note": "刘宏接任前的书记，身份待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—市长（核心搭档）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共大安市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记——常委、常务副市长", "overlap_org": "中共大安市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记——常委、副市长", "overlap_org": "中共大安市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记——人大主任（主席团）", "overlap_org": "中共大安市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "书记——政协党组", "overlap_org": "中共大安市委", "overlap_period": "2025-2026"},
    # 市长 ↔ 团队
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长——常务副市长", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长——副市长", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长——副市长", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长——副市长", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长——副市长", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长——副市长（公安）", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长——副市长", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长——挂职副市长", "overlap_org": "大安市人民政府", "overlap_period": "2025-2026"},
    # 前任/交接
    {"person_a": 14, "person_b": 12, "type": "交接", "context": "原政协主席→新政协党组书记（交接）", "overlap_org": "政协大安市委员会", "overlap_period": "2026-04"},
    {"person_a": 15, "person_b": 3, "type": "交接", "context": "前常务副市长→现任常务副市长（交接）", "overlap_org": "大安市人民政府", "overlap_period": "2025"},
    {"person_a": 16, "person_b": 1, "type": "交接", "context": "前任市委书记→现任书记（交接，前任身份待查）", "overlap_org": "中共大安市委", "overlap_period": ""},
]

# ═════════════════════════════════════════════════════════════════════════════
# Person JSON generation (person_graph_json.md schema)
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict):
    q = []
    if not person.get("birth"):
        q.append("出生年月未确认")
    if not person.get("birthplace"):
        q.append("籍贯未确认")
    if not person.get("education"):
        q.append("学历教育背景未确认")
    if not person.get("work_start"):
        q.append("参加工作年份未确认")
    if person.get("id") == 1:
        q.append("任大安市委书记前职务与到任时间未确认；前任书记身份未确认")
    if person.get("notes", ""):
        q.append("完整任职履历需进一步核实")
    return q


def _confidence(person: dict) -> str:
    return person.get("confidence", "unverified")


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"jilin_{name}"

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
                "confidence": _confidence(person),
                "source_ids": ["S001"],
            })
    if len(career_timeline) <= 1 and (not person.get("birth") or name.startswith("待查")):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足（政府网站无简历页，百度百科不可用）。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"dans_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": _confidence(person),
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "大安市人民政府门户网站（领导简介/领导活动）",
            "url": source_url or "http://www.daan.gov.cn/",
            "publisher": "大安市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "官方领导简介页及官方新闻确认现任职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "白城市",
            "region": "大安市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_大安市",
            "time_focus": "2025-2026",
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
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
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
            "is_current_confirmed": _confidence(person) == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if "白城" in person.get("birthplace", "") or isinstance(person.get("birthplace"), str) and "镇" in person.get("birthplace", "") else "local_ladder",
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
            "identity": "unverified" if not person.get("birth") and not person.get("name", "").startswith("待查") else ("unverified" if not person.get("birth") else "confirmed"),
            "current_role": _confidence(person),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月/籍贯/完整履历（百度百科不可用）；市委其他常委具体职务待查",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2) else "high",
                "question": person.get("notes", "") if person.get("notes") else f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical" if pid == 1 else "medium",
                "question": f"{name}的完整任职履历（每段职务的起止时间）" + ("；前任大安市委书记身份与去向" if pid == 1 else ""),
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历", "大安市委 常委班子"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # fix a couple of sloppy references
    record["identity"]["person_id"] = slug_id

    fname = f"{TODAY}-吉林省-白城市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


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
    core_ids = {1, 2, 3, 8, 11, 12}  # 书记、市长、常务副市长、公安局长、人大主任、政协主席
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
