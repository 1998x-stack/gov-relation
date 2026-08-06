#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 海南区 (Hainan District),
乌海市 (Wuhai City), 内蒙古自治区.

Investigation date: 2026-08-06
Task ID: inner_mongolia_海南区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.hainanqu.gov.cn — 乌海市海南区人民政府官方网站 (primary, current as of 2026-08-06)
    * 领导之窗(区政府): https://www.hainanqu.gov.cn/zwgk/ldzc/lb/ (李斌代理区长)
    * 党务公开·区委领导: https://www.hainanqu.gov.cn/dwgk/qwld/ (郑琳琥书记; 全体区委常委)
    * 领导活动: https://www.hainanqu.gov.cn/zwgk/ldhd/
    * 区委动态: https://www.hainanqu.gov.cn/dwgk/qwdt/

Confirmed current leaders (2026-08-06):
  - 区委书记: 郑琳琥 (男, 1977-12生, 党校研究生; 2026-07月中接替刘宝成; 官方bio 2026-07-21)
  - 区委副书记、政府代理区长: 李斌 (男, 汉族, 1986-07生, 本科/硕士; 2026年中接替白春雷)
  - 区委副书记、政法委书记: 秀芳 (女, 蒙古族, 1982-11生, 研究生)
  - 常务委员会: 李娜(宣传部长), 刘天庆(副区长), 马志高(纪委书记), 徐科(办公室主任),
    张泽宇(组织部长), 张宁(常务副区长), 单长波(统战部长), 顾亮亮(人武部长)

Confidence notes:
  - Current roles & 领导班子 roster: confirmed via 官方海南区人民政府网站 领导之窗/区委领导 (2026-08-06)
  - Birth/ethnicity/education of all core leaders: confirmed from official bios
  - 区委书记 郑琳琥→刘宝成: 刘宝成 2026-07-10 仍任区委书记; 郑琳琥 bio 2026-07-21, 07-19起以书记出席
    因此交接约在 2026-07月中旬. 刘宝成去向 open question.
  - 区长 李斌→白春雷: 白春雷领导活动至2026-06-15; 李斌自2026-06-22以代理区长身份活动. 
  - Full career histories prior to current roles: 各领导官网仅现任 b b信息，早期履历待查.
  - All claims labeled with confidence; gaps explicitly documented in report/open_gaps.md
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401 — used by gov_relation.runner via import
from gov_relation.runner import run_build  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "海南区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
PROVINCE = "内蒙古自治区"
CITY = "乌海市"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_海南区"
if _CURRENT_DIR.name == "inner_mongolia_海南区":
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
# IDs: 1-2 核心领导 (书记/区长), 3-11 班子成员, 12-15 政府副区长, 20-29 前任领导
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导 (现任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "郑琳琥",
        "gender": "男",
        "ethnicity": "",
        "birth": "1977-12",
        "birthplace": "",
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共乌海市海南区委员会",
        "source": "https://www.hainanqu.gov.cn/c/2026-07-21/191601.shtml",
        "confidence": "confirmed",
        "notes": "男，1977年12月生，党校研究生学历，中共党员；2026年7月接替刘宝成任海南区委书记（官方bio 2026-07-21）；任现职前完整履历待查",
    },
    {
        "id": 2,
        "name": "李斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-07",
        "birthplace": "",
        "education": "本科学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政府代理区长",
        "current_org": "海南区人民政府",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldzc/lb/",
        "confidence": "confirmed",
        "notes": "男，汉族，1986年7月生，本科学历，硕士学位；现任海南区委副书记、政府代理区长；领导区政府全面工作，负责审计，分管审计局",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 其他区委领导 (学生班子)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "秀芳",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1982-11",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共海南区委员会",
        "source": "https://www.hainanqu.gov.cn/c/2025-09-29/125861.shtml",
        "confidence": "confirmed",
        "notes": "女，蒙古族，1982年11月生，研究生学历，中共党员；区委副书记、政法委书记",
    },
    {
        "id": 4,
        "name": "李娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "",
        "education": "研究生学历，文学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共海南区委员会",
        "source": "https://www.hainanqu.gov.cn/c/2025-09-29/125860.shtml",
        "confidence": "confirmed",
        "notes": "女，汉族，1981年11月生，研究生学历，文学硕士，中共党员；区委常委、宣传部部长",
    },
    {
        "id": 5,
        "name": "刘天庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-02",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "中共海南区委员会/海南区人民政府",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldzc/ltq/",
        "confidence": "confirmed",
        "notes": "男，汉族，1984年2月生，研究生学历，中共党员；区委常委、副区长（常务副区长职责：发展改革、财政、税务、金融、国资、应急等）",
    },
    {
        "id": 6,
        "name": "马志高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-09",
        "birthplace": "",
        "education": "大学学历，文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、区监委主任",
        "current_org": "中共海南区纪律检查委员会",
        "source": "https://www.hainanqu.gov.cn/c/2025-09-29/125863.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1983年9月生，大学学历，文学学士，中共党员；区委常委、纪委书记、监委主任",
    },
    {
        "id": 7,
        "name": "徐科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-09",
        "birthplace": "",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、办公室主任",
        "current_org": "中共海南区委员会",
        "source": "https://www.hainanqu.gov.cn/c/2025-09-29/125864.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1989年9月生，大学学历，工学学士，中共党员；区委常委、办公室主任（较年轻常委）",
    },
    {
        "id": 8,
        "name": "张泽宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-04",
        "birthplace": "",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共海南区委员会",
        "source": "https://www.hainanqu.gov.cn/c/2025-09-29/125865.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1985年4月生，大学学历，工学学士，中共党员；区委常委、组织部部长（干部工作关键岗位）",
    },
    {
        "id": 9,
        "name": "张宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-10",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "中共海南区委员会/海南区人民政府",
        "source": "https://www.hainanqu.gov.cn/c/2024-08-09/188958.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1987年10月生，大学学历，中共党员；区委常委、区政府副区长",
    },
    {
        "id": 10,
        "name": "单长波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-03",
        "birthplace": "",
        "education": "研究生学历，硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共海南区委员会",
        "source": "https://www.hainanqu.gov.cn/c/2026-01-04/174686.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1984年3月生，研究生学历，硕士，中共党员；区委常委、统战部部长",
    },
    {
        "id": 11,
        "name": "顾亮亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、人武部部长",
        "current_org": "海南区人民武装部",
        "source": "https://www.hainanqu.gov.cn/c/2026-04-23/184898.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1979年11月生，大学学历，中共党员；区委常委、人武部部长",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政府 副区长 (非常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "刘建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、海南公安分局局长",
        "current_org": "海南区人民政府/海南公安分局",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldzc/ljp/",
        "confidence": "confirmed",
        "notes": "男，汉族，1974年9月生，大学学历，中共党员；副区长、海南公安分局局长；协助维护社会稳定、司法、退役军人事务",
    },
    {
        "id": 13,
        "name": "张松林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "海南区人民政府",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldzc/zsl/",
        "confidence": "confirmed",
        "notes": "男，汉族，1981年1月生，大学学历，中共党员；副区长；工业经济、科技创新、招商引资、生态环境；负责海南高新技术产业开发区管委会",
    },
    {
        "id": 14,
        "name": "杨泽宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "海南区人民政府",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldzc/whc/",
        "confidence": "confirmed",
        "notes": "男，汉族，1985年2月生，大学学历，中共党员；副区长；城市规划建设、智慧城市、交通",
    },
    {
        "id": 15,
        "name": "梁海东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长人选、西卓子山街道党工委书记",
        "current_org": "海南区人民政府",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldzc/lhd/",
        "confidence": "confirmed",
        "notes": "男，汉族，1983年1月生，大学学历，中共党员；副区长人选、西卓子山街道党工委书记；教育、商贸、能源、政务服务等 (bio 2026-08-04)",
    },
    {
        "id": 16,
        "name": "张一冉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长人选、拉僧仲街道党工委副书记/办事处主任",
        "current_org": "海南区人民政府",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldzc/zyr/",
        "confidence": "confirmed",
        "notes": "女，汉族，1984年4月生，大学学历，中共党员；副区长人选、拉僧仲街道党工委副书记/办事处主任；民族事务、农牧、乡村振兴、文旅等 (bio 2026-08-04)",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任核心领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "刘宝成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共海南区委员会（前任）",
        "source": "https://www.hainanqu.gov.cn/c/2026-07-13/191314.shtml",
        "confidence": "plausible",
        "notes": "2026-07-10仍以区委书记身份调研全区重点项目及防汛减灾工作；约2026年7月中旬由郑琳琳卸任；离任去向待查",
    },
    {
        "id": 21,
        "name": "白春雷",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长",
        "current_org": "海南区人民政府（前任）",
        "source": "https://www.hainanqu.gov.cn/zwgk/ldhd/",
        "confidence": "plausible",
        "notes": "领导活动记录至2026-06-15（调研煤矿安全）；约2026年6月由李斌接任（代理区长）；正式职务与去向待查",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共海南区委员会", "type": "党委", "level": "市辖区", "parent": "中共乌海市委员会", "location": "内蒙古乌海市海南区"},
    {"id": 2, "name": "海南区人民政府", "type": "政府", "level": "市辖区", "parent": "乌海市人民政府", "location": "内蒙古乌海市海南区"},
    {"id": 3, "name": "中共海南区纪律检查委员会/海南区监察委员会", "type": "党委", "level": "市辖区", "parent": "乌海市纪委监委", "location": "内蒙古乌海市海南区"},
    {"id": 4, "name": "海南公安分局", "type": "政府", "level": "市辖区", "parent": "乌海市公安局", "location": "内蒙古乌海市海南区"},
    {"id": 5, "name": "海南区人民武装部", "type": "党委", "level": "市辖区", "parent": "乌海军分区", "location": "内蒙古乌海市海南区"},
    {"id": 6, "name": "海南高新技术产业开发区管委会", "type": "开发区", "level": "市辖区", "parent": "海南区人民政府", "location": "内蒙古乌海市海南区"},
    {"id": 7, "name": "西卓子山街道党工委", "type": "党委", "level": "街道", "parent": "中共海南区委员会", "location": "内蒙古乌海市海南区西卓子山街道"},
    {"id": 8, "name": "拉僧仲街道党工委/办事处", "type": "政府", "level": "街道", "parent": "海南区人民政府", "location": "内蒙古乌海市海南区拉僧仲街道"},
    {"id": 9, "name": "中共乌海市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党内蒙古自治区委员会", "location": "乌海市"},
    {"id": 10, "name": "乌海市人民政府", "type": "政府", "level": "地级市", "parent": "内蒙古自治区人民政府", "location": "乌海市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 郑琳琥 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "", "rank": "县处级", "note": "2026-07月中旬接替刘宝成任区委书记"},
    # 李斌 — 区委副书记、政府代理区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "政府代理区长", "start_date": "2026-06", "end_date": "", "rank": "县处级", "note": "2026年6月左右接替白春雷任代理区长"},
    # 秀英 — 副书记、政法委书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李娜 — 宣传部部长
    {"person_id": 4, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘天庆 — 区委常委、副区长
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "常务（发改、财政、税务、金融、国资、应急等）"},
    # 马志高 — 纪委书记
    {"person_id": 6, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 徐科 — 办公室主任
    {"person_id": 7, "org_id": 1, "title": "区委常委、办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张泽宇 — 组织部部长
    {"person_id": 8, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张宁 — 区委常委、副区长
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 单长波 — 统战部部长
    {"person_id": 10, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 顾亮亮 — 人武部部长
    {"person_id": 11, "org_id": 5, "title": "区委常委、人武部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘建平 — 副区长、公安分局局长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 12, "org_id": 4, "title": "海南公安分局局长", "start_date": "", "end_date": "", "rank": "县处级", "note": "政法系统岗位"},
    # 张松林 — 副区长
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "工业经济、科技创新、开发区"},
    # 杨泽宇 — 副区长
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "城建、智慧城市、交通"},
    # 梁海东 — 副区长人选
    {"person_id": 15, "org_id": 2, "title": "副区长人选", "start_date": "2026-08", "end_date": "", "rank": "县处级", "note": "拟任副区长（2026-08-04 bio）"},
    {"person_id": 15, "org_id": 7, "title": "西卓子山街道党工委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 张一冉 — 副区长人选
    {"person_id": 16, "org_id": 2, "title": "副区长人选", "start_date": "2026-08", "end_date": "", "rank": "县处级", "note": "拟任副区长（2026-08-04 bio）"},
    {"person_id": 16, "org_id": 8, "title": "拉僧仲街道党工委副书记/办事处主任", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    # 前任
    {"person_id": 20, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "2026-07", "rank": "县处级", "note": "前任区委书记（2026-07中旬离任）"},
    {"person_id": 21, "org_id": 2, "title": "区长", "start_date": "", "end_date": "2026-06", "rank": "县处级", "note": "前任区长（2026年6月离任）"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 郑琳琳 ↔ 李斌 (书记—区长搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    # 郑琳琳 ↔ 各班子成员
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记（政法委）", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委（宣传部）", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委（副区长）", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—办公室主人", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—常委（副区长）", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—人武部长", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07-"},
    # 李斌 ↔ 区政府
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长（代）—副区长", "overlap_org": "海南区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长（代）—副区长", "overlap_org": "海南区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "区长（代）—副区长/公安分局长", "overlap_org": "海南区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "区长（代）—副区长", "overlap_org": "海南区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "区长（代）—副区长", "overlap_org": "海南区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "区长（代）—副区长人选", "overlap_org": "海南区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "区长（代）—副区长人选", "overlap_org": "海南区人民政府", "overlap_period": "2026-"},
    # 前任交接
    {"person_a": 20, "person_b": 1, "type": "交接", "context": "前任区委书记→现任区委书记", "overlap_org": "中共海南区委员会", "overlap_period": "2026-07"},
    {"person_a": 21, "person_b": 2, "type": "交接", "context": "前任区长→现任代区长", "overlap_org": "海南区人民政府", "overlap_period": "2026-06"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════════
def slugify(name: str) -> str:
    return name.replace(" ", "")


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"wuhai_hainan_{name}"

    # current_post resolution
    post_label = person.get("current_post", "")
    region_label = "海南区"
    fname = f"{TODAY}-{PROVINCE}-{CITY}-{post_label}-{name}.json"

    # Identity → career_timeline from positions
    career_timeline = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            career_timeline.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": org["name"] if org else "",
                "title": pos.get("title", ""),
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if (org and org["type"] == "党委") else ("government" if (org and org["type"] == "政府") else "other"),
                "rank": pos.get("rank", ""),
                "is_key_promotion": pos.get("title") in ("区委书记", "政府代理区长", "区长"),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
                "source_ids": ["S002"],
            })

    # Collect relationships
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"wuhai_hainan_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S002"],
        })

    source_url = person.get("source", "")
    sources = [
        {"id": "S001", "title": "海南区人民政府—领导之窗/区委领导",
         "url": "https://www.hainanqu.gov.cn/zwgk/ldzc/lb/",
         "publisher": "海南区人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "官网访问，确认现任领导职务、出生年月、民族、学历"},
        {"id": "S002", "title": "海南区人民政府—区委领导/党务公开官方bio",
         "url": source_url, "publisher": "海南区人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "个人领导介绍页确认信息"},
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": "海南区",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_海南区",
            "time_focus": "2025-2026年",
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
            "education": [{"period": "", "institution": person.get("education", ""), "major": "",
                           "degree": "", "study_type": "unknown", "source_ids": ["S002"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级" if pid in (1, 2, 5, 9, 12, 13, 14, 15, 16) else ("副处级" if pid in (3, 4, 6, 7, 8, 10, 11) else ""),
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S002"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations if o["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == pid}],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["内蒙古自治区"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "搜索范围为官方领导页与公开新闻，未发现针对所记人物的纪律或舆情风险信号（截至2026-08-06）。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S002"],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "任现职前完整履历与去向待查" if pid in (1, 2, 20, 21) else "",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2, 20, 21) else "medium",
                "question": f"{name} 任现职前完整职业履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确时间线",
                "suggested_queries": [f"{name} 简历 海南区", f"{name} 乌海", f"{name} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high" if pid in (1, 2) else "medium",
                "question": f"{name} 出生地、籍贯及详细教育背景（{person.get('birth','为空')}）",
                "why_it_matters": "核心身份信息，用于去重与跨区域关联",
                "suggested_queries": [f"{name} 籍贯", f"{name} 毕业院校"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high" if pid == 20 else "low",
                "question": "刘宝成卸任区委书记后的去向",
                "why_it_matters": "仲裁书记人员流动链条",
                "suggested_queries": ["刘宝成 卸任 去向", "刘宝成 乌海"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high" if pid == 21 else "low",
                "question": "白春雷卸任区长后的去向与是否任现职",
                "why_it_matters": "区长人员任免链条",
                "suggested_queries": ["白春雷 区长 去向", "白春雷 乌海"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fpath = PJSON_DIR / fname
    # Keep JSON valid regardless of region handling with hard-coded region field
    record["investigation_scope"]["region"] = "海南区"
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
    core_ids = {1, 2}  # 核心领导 (书记、区长)
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())