#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 铁东区, 四平市, 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_铁东区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL WEB ACCESS
  - 铁东区政府网站 (tdq.siping.gov.cn): accessible (HTTP), official leader pages + work reports
  - Exa web search: rate-limited
  - 百度/百度百科: 403
  - 区委独立网站: 未开放（党委领导不在政府网站上展示）

Confirmed official sources (铁东区政府网站 http://tdq.siping.gov.cn/):
  - 区长赵明 profile: http://tdq.siping.gov.cn/qz/wdjl/
  - 常务副区长田枫: http://tdq.siping.gov.cn/qz/wdts/tf/
  - 副区长薛英辉: http://tdq.siping.gov.cn/qz/wdts/xyh/
  - 副区长李论: http://tdq.siping.gov.cn/qz/wdts/ll/
  - 副区长叶晓斌: http://tdq.siping.gov.cn/qz/wdts/yxb/
  - 副区长徐峰: http://tdq.siping.gov.cn/qz/wdts/hjw_21378/
  - 副区长岳楠: http://tdq.siping.gov.cn/qz/wdts/yn/
  - 副区长杨嘉龙: http://tdq.siping.gov.cn/qz/wdts/yjl/
  - 2025 政府工作报告(代区长赵明): http://tdq.siping.gov.cn/zw/jcxxgk/gzbg/202601/t20260106_757300.html
  - 2024 政府工作报告(区长常波): http://tdq.siping.gov.cn/zw/jcxxgk/gzbg/202501/t20250108_728457.html
  - 铁东概况: http://tdq.siping.gov.cn/qq/qq/202203/t20220317_613941.html
  - 乡镇街道: http://tdq.siping.gov.cn/qzf/zfjg/gxzjd/

Confidence notes:
  - 区委书记常波: CONFIRMED — 铁东发布(区官方微信)2026-07-17/07-28/08-03多篇点名'区委书记常波'; 曾为区长(至2025-10)
  - 区长赵明: confirmed via official gov profile + work report (代区长2025-12 → 区长)
  - 前任区长(常波)→现任区委书记 就地转任: confirmed (区长→书记, 2025-12~2026上半年)
  - 前任区委书记: NOT confirmed — 姓名/去向待查, open gap
  - 7 副区长: all confirmed via official profiles
  - 区委常委会成员: 部分副区长兼任(田枫=区委常委), 其余待查

跨区交流线索 (官方履历佐证, 强):
  - 薛英辉(副区长): 铁东区叶赫满族镇→山门镇→区信访局 → 铁西区政府副区长 → 回铁东区副区长 (铁东↔铁西 跨区交流)
  - 岳楠(副区长): 四平市扶贫办 → 双辽市王奔镇镇长 → 铁东区副区长 (双辽→铁东)
  - 赵明(区长): 四平市发改委/扶贫办/乡村振兴局 → 市委政研室主任 → 伊通县委副书记(正县长级) → 铁东区区长 (市→县→区)
  - 杨嘉龙(副区长): 四平市工信局 → 伊通县靠山镇镇长、莫里青乡党委书记 → 铁东区副区长 (伊通→铁东)
  - 李论(副区长): 中共吉林省委党校(省行政学院)教务处 → 州/区挂职
  - 叶晓斌(副区长): 北京电子科技学院教务处 → 州/区挂职

铁东区 (四平市):
  - 辖 城东乡、山门镇、叶赫满族镇、石岭镇 1乡3镇 + 8街道；46个社区、54个行政村；904.99 km² 位于吉林省西南部, 与辽源市、梨树县、铁西区、辽宁省铁岭市昌图县/西丰县接壤.
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

import sqlite3  # noqa: F401  (used by gov_relation.runner via import)
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "铁东区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_铁东区"
if _CURRENT_DIR.name == "jilin_铁东区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Source Register ──────────────────────────────────────────────────────────
SOURCES = [
    {
        "id": "S001",
        "title": "四平市铁东区人民政府——政府领导(区长赵明简历)",
        "url": "http://tdq.siping.gov.cn/qz/wdjl/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "赵明，男，汉族，1981年12月生，中共党员，省委党校研究生。曾任市发改委副主任、市扶贫办副主任、市乡村振兴局副局长、市委政研室主任、伊通县委副书记(正县长级)。现任区长，主持政府全面工作。",
    },
    {
        "id": "S002",
        "title": "四平市铁东区人民政府——常务副区长田枫",
        "url": "http://tdq.siping.gov.cn/qz/wdts/tf/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "田枫，男，汉族，1976年9月生，省委党校研究生；曾任市政府办系统(综合科、应急办、督查室、秘书科、外事办副主任)。现任区委常委、副区长(常务)。",
    },
    {
        "id": "S003",
        "title": "四平市铁东区人民政府——副区长叶晓斌",
        "url": "http://tdq.siping.gov.cn/qz/wdts/yxb/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "叶晓斌，男，汉族，1984年5月生；曾任北京电子科技学院教务处、研究生部职务；现任铁东区政府党组成员、副区长(挂钩人社、发改)。",
    },
    {
        "id": "S004",
        "title": "四平市铁东区人民政府——副区长李论",
        "url": "http://tdq.siping.gov.cn/qz/wdts/ll/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "李论，男，1981年3月生，省委党校公共管理专业在职研究生；曾任中共吉林省委党校(省行政学院)教务处副处长、处长；现任铁东区副区长。",
    },
    {
        "id": "S005",
        "title": "四平市铁东区人民政府——副区长薛英辉",
        "url": "http://tdq.siping.gov.cn/qz/wdts/xyh/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "薛英辉，男，满族，1975年9月生，本科学历；叶赫满族镇副镇长/党委副书记纪委书记、经开区合作局局长、山门镇党委书记、区信访局局长、铁西区政府副区长、铁东区政府副区长。铁东↔铁西跨区交流案例。",
    },
    {
        "id": "S006",
        "title": "四平市铁东区人民政府——副区长徐峰",
        "url": "http://tdq.siping.gov.cn/qz/wdts/hjw_21378/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "徐峰，男，汉族，1979年7月生，研究生，农工党党员；曾任四平市政协教科文卫体委员会办公室主任、农工党四平市委专职副主任委员；现任铁东区副区长(党外干部)。",
    },
    {
        "id": "S007",
        "title": "四平市铁东区人民政府——副区长岳楠",
        "url": "http://tdq.siping.gov.cn/qz/wdts/yn/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "岳楠，女，汉族，1990年6月生，研究生，中共党员；曾任四平市农机推广站副站长、扶贫办社会科副科长/党支部专职副书记、双辽市王奔镇镇长；现任铁东区副区长。",
    },
    {
        "id": "S008",
        "title": "四平市铁东区人民政府——副区长杨嘉龙",
        "url": "http://tdq.siping.gov.cn/qz/wdts/yjl/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-07-31",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "杨嘉龙，男，汉族，1987年4月生，法学硕士；历任四平市工信局科员→副主任科员→(减负办)副科长；伊通县靠山镇镇长→莫里青乡党委书记；现任铁东区副区长。",
    },
    {
        "id": "S009",
        "title": "2025年四平市铁东区人民政府工作报告(代区长赵明)",
        "url": "http://tdq.siping.gov.cn/zw/jcxxgk/gzbg/202601/t20260106_757300.html",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2026-01-06",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "2025年12月26日在十届人大六次会议上，代区长赵明作报告，确认赵明于2025年12月任代区长。",
    },
    {
        "id": "S010",
        "title": "2024年四平市铁东区人民政府工作报告(区长常波)",
        "url": "http://tdq.siping.gov.cn/zw/jcxxgk/gzbg/202501/t20250108_728457.html",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2025-01-08",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "2024年12月27日在十届人大五次会议，区长常波作报告，确认前任区长为常波。",
    },
    {
        "id": "S011",
        "title": "铁东概况",
        "url": "http://tdq.siping.gov.cn/qq/qq/202203/t20220317_613941.html",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2025-03-03",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "铁东区建制沿革(1983-12-22设区)、辖区、乡镇街道、面积等区情。",
    },
    {
        "id": "S012",
        "title": "各乡镇街道",
        "url": "http://tdq.siping.gov.cn/qzf/zfjg/gxzjd/",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2023-01-11",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "城东乡、山门镇、叶赫满族镇、石岭镇与8个街道办直属机构。",
    },
    {
        "id": "S013",
        "title": "铁东发布(官方微信)——2026年第12次区委常委会会议",
        "url": "https://mp.weixin.qq.com/s/yuAYsba2Ji3njPaRxxp9Lw",
        "publisher": "铁东发布(四平市铁东区委)",
        "published_at": "2026-07-17",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认现任区委书记=常波：'区委书记常波主持召开2026年第12次区委常委会会议'(2026-07-17)。",
    },
    {
        "id": "S014",
        "title": "铁东发布(官方微信)——2026年第13次区委常委会会议",
        "url": "https://mp.weixin.qq.com/s/JTDUMUaCnnFNwm4coF_AEQ",
        "publisher": "铁东发布(四平市铁东区)",
        "published_at": "2026-08-03",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认现任区委书记=常波(2026-08-03)。",
    },
    {
        "id": "S015",
        "title": "铁东发布(官方公众号)——7月28日八一走访 & 8月3日区委财经委员会",
        "url": "https://mp.weixin.qq.com/s/a4Lk7UBIgY-6h4lz3IZO4w",
        "publisher": "铁东发布(四平市铁东区)",
        "published_at": "2026-07-28",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "'区委书记常波带领相关区级领导参加走访慰问'(07-28)；'区委书记常波出席会议并讲话'(08-03财经委)。",
    },
    {
        "id": "S016",
        "title": "铁东区政府网站——常波任区长核查(归档)",
        "url": "http://tdq.siping.gov.cn/qz/wdgz/202510/t20251027_751031.html",
        "publisher": "四平市铁东区人民政府",
        "published_at": "2025-10-27",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "'10月24日，区委副书记、区长常波…调研专业化物业服务小区'——证实常波2025-10仍是区长，2026年转任区委书记。前任书记在此之前。",
    },
    {
        "id": "S990",
        "title": "中共四平市铁东区委（党委网站）",
        "url": "http://tdq.siping.gov.cn/",
        "publisher": "中共四平市铁东区委员会",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "unverified",
        "reliability": "unknown",
        "notes": "铁东区委领导名单(区委书记等)不在区人民政府网站展示；党委独立网站/四平市委组织部任前公示未能在当前网络环境下访问。区委书记信息待查。",
    },
]

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs:
#   core: 1=区委书记(待查), 2=区长(赵明), 3=常务副区长(田枫)
#   gov 副区: 4=叶晓斌, 5=李论, 6=薛英辉, 7=徐峰, 8=曹楠, 9=杨嘉龙
#   前任: 10=常波(前任区长)
#   跨区关联: 11=常波關係? no. 11 reserved
persons = [
    # ── 区委书记 (NOT confirmed) ──
    {
        "id": 1,
        "name": "常波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共四平市铁东区委员会",
        "source": "confirmed(现任) —— 铁东发布(区官方微信)2026-07-17/07-28/08-03 多篇常委会与走访报道点名'区委书记常波'；离任区长身份来自铁东区政府网站归档文(2025-10)。",
        "notes": "常波，四平市铁东区委书记（confirmed, as of 2026-08-03）。曾任铁东区委副书记、区长（2025-10-24仍是：见政府网归档《常波调研专业化物业服务小区》），2026年升任区委书记（区长→书记就地晋升）。出生年份、民族、学历等身份细节待查(opengap)。",
    },
    # ── 区长 赵明 (CONFIRMED) ──
    {
        "id": 2,
        "name": "赵明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 铁东区政府官网领导页 + 2025政府工作报告(代区长赵明)",
        "notes": "赵明，男，汉族，1981年12月生，中共党员，省委党校研究生。曾任四平市发展和改革委员会副主任、党组成员；市扶贫开发办公室党组成员、副主任、三级调研员；市乡村振兴局党组成员、副局长、三级调研员；市委政策研究室（市委全面深化改革领导小组办公室）主任；伊通满族自治县委副书记（正县长级）、县委党校校长、县委教工委书记、营城子镇党委书记。2025年12月以代区长身份作报告，现任四平市铁东区人民政府区长。主持区政府全面工作，分管区审计局。",
    },
    # ── 常务副区长 田枫 (CONFIRMED) ──
    {
        "id": 3,
        "name": "田枫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 铁东区政府官网领导页",
        "notes": "田枫，男，汉族，1976年9月生，中共党员，省委党校研究生。曾任四平市政府办公室综合科主任科员、市政府应急管理办公室(市长公开电话办、市政府总值班室)副主任(正科长级)、市政府督查室专职督查员(正科长级)、市政府办公室秘书科科长、市政府办公室(市政府外事办公室)党组成员、副主任、三级调研员。现任四平市铁东区委常委、常务副区长。负责政府常务工作（发改、财政、应急、住建、平台公司等）。",
    },
    # ── 副区长 叶晓斌 (CONFIRMED) ──
    {
        "id": 4,
        "name": "叶晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年5月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 官网领导页",
        "notes": "叶晓斌，男，汉族，1984年5月生，中共党员。历任北京电子科技学院教务处教务科科长、研究生部学办主任、研究生部副主任、研究生部教工党支部副书记；现任铁东区政府党组成员、副区长。负责人力资源和社会保障、协助田枫分管发改。挂职背景(中央院校→地方)明显。",
    },
    # ── 副区长 李论 (CONFIRMED) ──
    {
        "id": 5,
        "name": "李论",
        "gender": "男",
        "ethnicity": "",
        "birth": "1981年3月",
        "birthplace": "",
        "education": "省委党校公共管理专业在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 官网领导页",
        "notes": "李论，男，1981年3月生，中共党员，省委党校公共管理专业在职研究生。曾任中共吉林省委党校（省行政学院）教务处副主任、主任科员、副处长、处长。现任铁东区副区长。负责司法、地方志，协助杨嘉龙分管商务(招商引资)。",
    },
    # ── 副区长 薛英辉 (CONFIRMED) ──
    {
        "id": 6,
        "name": "薛英辉",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 官网领导页",
        "notes": "薛英辉，男，满族，1975年9月生，本科，中共党员。叶赫满族镇副镇长→党委副书记、纪委书记→吉林铁东经济开发区合作局局长→山门镇党委书记→区(区政府)信访局党组书记、局长→铁西区政府党组成员、副区长→铁东区政府党组成员、副区长。铁东↔铁西跨区交流，农业农村/乡镇领域。",
    },
    # ── 副区长 徐峰 (CONFIRMED, 党外干部) ──
    {
        "id": 7,
        "name": "徐峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年7月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "农工党党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 官网领导页",
        "notes": "徐峰，男，汉族，1979年7月生，研究生，农工党党员。曾任四平市政协教科文卫体委员会文史办公室主任、农工党四平市委员会专职副主任委员。现任铁东区副区长。负责教育、卫生健康、文化旅游、残联、退役军人事务、妇女儿童等(党外干部)。",
    },
    # ── 副区长 岳楠 (CONFIRMED, 女) ──
    {
        "id": 8,
        "name": "岳楠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1990年6月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 官网领导页",
        "notes": "岳楠，女，汉族，1990年6月生，研究生，中共党员。历任四平市农机推广站副站长；四平市扶贫开发办公室社会和行业扶贫科副科长；扶贫办公室机关党支部专职副书记(人事科科长)；四平市双辽市王奔镇党委副书记、镇长；现任铁东区副区长。负责政务服务/数字化、民政、信访、自然资源、街道等(双辽→铁东跨区交流)。",
    },
    # ── 副区长 杨嘉龙 (CONFIRMED) ──
    {
        "id": 9,
        "name": "杨嘉龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年4月",
        "birthplace": "",
        "education": "法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "confirmed —— 官网领导页",
        "notes": "杨嘉龙，男，汉族，1987年4月生，法学硕士，中共党员。历任四平市工业和信息化局科员、副主任科员、四级主任科员、经济运行科(减负办)副科长(副主任)、三级主任科员；伊通满族自治县靠山镇党委副书记、镇长；莫离合乡党委书记、一级主任科员；现任铁东区副区长，负责工信、商务(招商引资)、城管执法。",
    },
    # ── 前任区委书记 (NOT confirmed) — 常波的前任 ──
    {
        "id": 10,
        "name": "前任区委书记(待查)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未知（已离任）",
        "current_org": "",
        "source": "unverified —— 常波在2025-10仍为区长,故前任区委书记在2024-2025年在职、2025年底~2026年初离任；姓名与去向未检索到。",
        "notes": "铁东区前任区委书记（常波之前）。常波2025-10仍任区长，故前任书记在2025年底-2026年初离任。其姓名、去向、离任时间、任前公示均未能获取。可能外调/退休/交流，属推测。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共四平市铁东区委员会", "type": "党委", "level": "县处级",
     "parent": "中共四平市委员会", "location": "吉林省四平市铁东区"},
    {"id": 2, "name": "铁东区人民政府", "type": "政府", "level": "县处级",
     "parent": "四平市人民政府", "location": "吉林省四平市铁东区开发区大路469号"},
    {"id": 3, "name": "中共四平市铁东区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共四平市纪律检查委员会", "location": "吉林省四平市铁东区"},
    {"id": 4, "name": "四平市铁东区监察委员会", "type": "纪委", "level": "县处级",
     "parent": "四平市监察委员会", "location": "吉林省四平市铁东区"},
    {"id": 5, "name": "铁东区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "四平市人民代表大会常务委员会", "location": "吉林省四平市铁东区"},
    {"id": 6, "name": "中国人民政治协商会议四平市铁东区委员会", "type": "政协", "level": "县处级",
     "parent": "政协四平市委员会", "location": "吉林省四平市铁东区"},
    {"id": 7, "name": "中共四平市铁东区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共四平市铁东区委员会", "location": "吉林省四平市铁东区"},
    {"id": 8, "name": "中共四平市铁东区委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共四平市铁东区委员会", "location": "吉林省四平市铁东区"},
    {"id": 9, "name": "中共四平市铁东区委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共四平市铁东区委员会", "location": "吉林省四平市铁东区"},
    {"id": 10, "name": "四平市发展和改革委员会", "type": "政府", "level": "地厅级",
     "parent": "四平市人民政府", "location": "吉林省四平市"},
    {"id": 11, "name": "四平市人民政府办公室", "type": "政府", "level": "地厅级",
     "parent": "四平市人民政府", "location": "吉林省四平市"},
    {"id": 12, "name": "四平市乡村振兴局", "type": "政府", "level": "地厅级",
     "parent": "四平市人民政府", "location": "吉林省四平市"},
    {"id": 13, "name": "中共伊通满族自治县委员会", "type": "党委", "level": "县处级",
     "parent": "中共四平市委员会", "location": "吉林省四平市伊通满族自治县"},
    {"id": 14, "name": "四平市双辽市王奔镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "四平市双辽市人民政府", "location": "吉林省四平市双辽市"},
    {"id": 15, "name": "四平市铁西区人民政府", "type": "政府", "level": "县处级",
     "parent": "四平市人民政府", "location": "吉林省四平市铁西区"},
    {"id": 16, "name": "中共吉林省委党校(省行政学院)", "type": "党委", "level": "省厅级",
     "parent": "中共吉林省委", "location": "吉林省长春市"},
    {"id": 17, "name": "北京电子科技学院", "type": "其他", "level": "院校",
     "parent": "", "location": "北京市"},
    {"id": 18, "name": "四平市政协", "type": "政协", "level": "地厅级",
     "parent": "中共四平市委", "location": "吉林省四平市"},
    {"id": 19, "name": "农工党四平市委", "type": "政协", "level": "县处级",
     "parent": "中国农工民主党吉林省委", "location": "吉林省四平市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记",
     "start": "2026", "end": "present", "rank": "县处级正职",
     "note": "现任区委书记(confirmed, 铁东发布2026-07/08多篇点名)。区长→书记就地晋升。"},
    {"person_id": 1, "org_id": 2, "title": "区长",
     "start": "unknown", "end": "2025-12", "rank": "县处级正职",
     "note": "前任区长(2025-10-24仍为此职)，2025-12后由赵明接任区长，常波转任区委书记。"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记",
     "start": "unknown", "end": "2025-12", "rank": "县处级副职",
     "note": "常波任区长期间兼任区委副书记。"},
    # 前任区委书记 — 常波的前任
    {"person_id": 10, "org_id": 1, "title": "区委书记",
     "start": "unknown", "end": "2025", "rank": "县处级正职",
     "note": "前任区委书记，2025年底前在职，姓名/去向待查."},
    # 赵明 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start": "2025-12", "end": "present", "rank": "县处级正职",
     "note": "2025-12以代区长身份作报告，现任区长。接替常波。"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记",
     "start": "2025-12", "end": "present", "rank": "县处级副职",
     "note": "赵明兼任区委副书记(区长惯例)。"},
    # 田枫 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "副区长(常务)",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "区委常委、区政府党组副书记、常务副区长。负责发改、财政、应急、住建等。"},
    {"person_id": 3, "org_id": 1, "title": "区委常委",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "区委常委。"},
    {"person_id": 3, "org_id": 11, "title": "市政府办公室副主任/党组成员",
     "start": "unknown", "end": "unknown", "rank": "县处级副职",
     "note": "曾任市直履历（市政府办系统）。"},
    # 叶晓斌
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "区政府党组成员。负责社会保障、发改。"},
    {"person_id": 4, "org_id": 17, "title": "北京电子科技学院研究生部副主任",
     "start": "unknown", "end": "unknown", "rank": "", "note": "中央院校下派/挂职背景。"},
    # 李论
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责司法、地方志，协助杨嘉龙商务招商。"},
    {"person_id": 5, "org_id": 16, "title": "省委党校教务处处长",
     "start": "unknown", "end": "unknown", "rank": "", "note": "省党校系统→区下派。"},
    # 薛英辉
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责农业农村、交通、林业、水利、乡镇。"},
    {"person_id": 6, "org_id": 15, "title": "铁西区政府副区长",
     "start": "unknown", "end": "unknown", "rank": "县处级副职",
     "note": "铁东→铁西→铁东 跨区交流。"},
    # 徐峰(党外)
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "农工党党员。负责教育、卫生、文旅、退役军人等。"},
    {"person_id": 7, "org_id": 19, "title": "农工党四平市委专职副主任委员",
     "start": "unknown", "end": "unknown", "rank": "", "note": "党外干部，政协系统背景。"},
    # 岳楠(女)
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责政务数字化、民政、信访、自然资源、街道。"},
    {"person_id": 8, "org_id": 14, "title": "双辽市王奔镇镇长",
     "start": "unknown", "end": "unknown", "rank": "乡科级正职",
     "note": "双辽→铁东 跨区交流。"},
    # 杨嘉龙
    {"person_id": 9, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责工信、商务、城管执法。"},
    {"person_id": 9, "org_id": 13, "title": "伊通县莫里青乡党委书记",
     "start": "unknown", "end": "unknown", "rank": "乡科级正职",
     "note": "伊通县→铁东 跨区交流。"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政领导搭档",
        "context": "区委书记与区长，党政主要负责人关系",
        "overlap_org": "中共四平市铁东区委员会/铁东区人民政府",
        "overlap_period": "2025-12至今",
        "confidence": "unverified",
    },
# 区长交接 (赵明 ← 常波, 常波后转书记)
    {
        "person_a": 2, "person_b": 1,
        "type": "predecessor_successor",
        "context": "赵明接替常波任区长（常波转任区委书记）",
        "overlap_org": "铁东区人民政府",
        "overlap_period": "2025-12",
        "confidence": "confirmed",
    },
    # 区委书记交接 (常波 ← 前任书记)
    {
        "person_a": 1, "person_b": 10,
        "type": "predecessor_successor",
        "context": "常波接任区委书记（前任书记未定）",
        "overlap_org": "中共四平市铁东区委员会",
        "overlap_period": "2026",
        "confidence": "unverified",
    },
    # 区长与常务副区长
    {"person_a": 2, "person_b": 3, "type": "政府领导班子", "context": "区长与常务副区长(政府核心搭档)",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 区长与各副区长
    {"person_a": 2, "person_b": 4, "type": "政府领导班子", "context": "区长与副区长(叶晓斌)",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "政府领导班子", "context": "区长与副区长(李论)",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "政府领导班子", "context": "区长与副区长(薛英辉)",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "政府领导班子", "context": "区长与副区长(徐峰)",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "政府领导班子", "context": "区长与副区长(岳楠)",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "政府领导班子", "context": "区长与副区长(杨嘉龙)",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 常务副区长与各副区长
    {"person_a": 3, "person_b": 4, "type": "政府领导班子", "context": "常务副区长与副区长",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "政府领导班子", "context": "常务副区长与副区长",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "政府领导班子", "context": "常务副区长与副区长",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "政府领导班子", "context": "常务副区长与副区长",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "政府领导班子", "context": "常务副区长与副区长",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 9, "type": "政府领导班子", "context": "常务副区长与副区长",
     "overlap_org": "铁东区人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 跨区交流（official resume）
    {"person_a": 6, "person_b": 15, "type": "cross_region_transfer", "context": "薛英辉铁东→铁西→铁东跨区交流",
     "overlap_org": "四平市铁西区人民政府", "overlap_period": "待查", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 14, "type": "cross_region_transfer", "context": "岳楠自双辽王奔镇长调任铁东副区长",
     "overlap_org": "四平市双辽市", "overlap_period": "待查", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 13, "type": "cross_region_transfer", "context": "杨嘉龙自伊通莫里青乡党委书记调任铁东副区长",
     "overlap_org": "中共伊通满族自治县委员会", "overlap_period": "待查", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "cross_region_transfer", "context": "赵明曾任伊通县委副书记，后任铁东区长",
     "overlap_org": "中共伊通满族自治县委员会", "overlap_period": "待查", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 11, "type": "career_origin", "context": "田枫自市政府办公室系统升任铁东常务副区长",
     "overlap_org": "四平市人民政府办公室", "overlap_period": "待查", "confidence": "confirmed"},
    # 同源 (省党校、中央院校)
    {"person_a": 5, "person_b": 16, "type": "career_origin", "context": "李论自省委党校下派",
     "overlap_org": "中共吉林省委党校", "overlap_period": "待查", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 17, "type": "career_origin", "context": "叶晓斌自北京电子科技学院下派/挂职",
     "overlap_org": "北京电子科技学院", "overlap_period": "待查", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 18, "type": "career_origin", "context": "徐峰(农工党)：市政协会教科文委背景",
     "overlap_org": "四平市政协", "overlap_period": "待查", "confidence": "confirmed"},
]


# ══════════════════════════════════════════════════════════════════════════════
# Person JSON Generator
# ══════════════════════════════════════════════════════════════════════════════


def make_person_json(p, rel_list):
    """Generate person JSON for a core figure."""
    is_top = p["id"] in (1, 2)
    rank = "县处级正职" if is_top else "县处级副职"
    is_confirmed = p["id"] != 10  # Only 前任区委书记(id 10) is unconfirmed; id 1(常波)现任书记已确认

    name_slug = p["name"].replace("（", "_").replace("）", "_")
    person_id = f"siping_tiedong_{name_slug}"

    identity = {
        "person_id": person_id,
        "name": p["name"],
        "aliases": [],
        "gender": p.get("gender", ""),
        "ethnicity": p.get("ethnicity", ""),
        "birth": p.get("birth", ""),
        "birthplace": p.get("birthplace", ""),
        "native_place": "",
        "education": [],
        "party_join": p.get("party_join", ""),
        "work_start": p.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{p['name']}_{p.get('birth', '')}",
            "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
            "official_profile_url": "tdq.siping.gov.cn",
        },
    }
    if p.get("education"):
        identity["education"].append({
            "period": "",
            "institution": "",
            "major": "",
            "degree": p["education"],
            "study_type": "unknown",
            "source_ids": ["S001"] if is_confirmed else [],
        })

    career_items = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
            career_items.append({
                "start": pos["start"],
                "end": pos["end"],
                "org": org_name,
                "title": pos["title"],
                "level": pos["rank"],
                "location": "吉林省四平市铁东区",
                "system": "party" if "委" in org_name and "政府" not in org_name else "government",
                "rank": pos["rank"],
                "is_key_promotion": is_top,
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if is_confirmed else "unverified",
                "source_ids": ["S001"] if is_confirmed else [],
            })
    if not career_items:
        career_items.append({
            "start": "unknown", "end": "present",
            "org": p["current_org"], "title": p["current_post"],
            "level": rank, "location": "吉林省四平市铁东区",
            "system": "party" if "委" in p["current_org"] and "政府" not in p["current_org"] else "government",
            "rank": rank, "is_key_promotion": is_top,
            "notes": "因网络受限，详细履历暂未查到。", "confidence": "unverified", "source_ids": [],
        })

    rels_out = []
    for r in rel_list:
        other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
        other = next((x for x in persons if x["id"] == other_id), None)
        if other:
            rels_out.append({
                "person": other["name"],
                "person_id": f"siping_tiedong_{other['name']}",
                "relationship_type": r["type"],
                "strength": "medium" if r["confidence"] == "confirmed" else "weak",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": r["confidence"],
                "source_ids": ["S001"],
            })

    src_ids = ["S001", "S002", "S003", "S004", "S005", "S006", "S007", "S008"]
    if p["id"] == 1:
        src_ids = ["S013", "S014", "S015"]
    elif p["id"] == 2:
        src_ids = ["S001", "S009", "S010", "S011", "S012"]
    elif p["id"] == 10:
        src_ids = ["S016"]

    biggest_gap = "前任区委书记姓名与去向未知" if p["id"] == 10 else ""
    if p["id"] == 1:
        biggest_gap = "常波的出生年份、民族、学历及任区委书记具体日期"
    if p["id"] == 2:
        biggest_gap = "赵明任区长前的完整任职时间线(各职务起止年份)未在公开简历中逐段标注"

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "吉林省", "city": "四平市", "region": "铁东区",
            "job": p["current_post"], "task_id": "jilin_铁东区", "time_focus": "2026年8月",
        },
        "identity": identity,
        "current_status": {
            "current_post": p["current_post"], "current_org": p["current_org"],
            "administrative_rank": rank, "as_of": AS_OF,
            "is_current_confirmed": is_confirmed, "source_ids": src_ids,
        },
        "career_timeline": career_items,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": [],
            "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": SOURCES,
        "confidence_summary": {
            "identity": "confirmed" if is_confirmed else "unverified",
            "current_role": "confirmed" if is_confirmed else "unverified",
            "career_completeness": "partial" if is_confirmed else "thin",
            "relationship_confidence": "high" if is_confirmed else "low",
            "biggest_gap": biggest_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "前任区委书记的姓名、去向与离任时间",
                "why_it_matters": "常波在2025-10仍为区长，故前任书记于2025年底~2026年初离任；其身份是补全书记更替链的关键",
                "suggested_queries": ["四平铁东区委书记 任前公示", "铁东区委书记 离任", "site:siping.gov.cn 铁东 书记"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"常波(现任区委书记)的出生年份、民族、学历及任书记具体日期",
                "why_it_matters": "常波是当前党政一把手，需要完整身份与晋升时间线",
                "suggested_queries": ["常波 铁东区委书记 简历", "常波 四平 任前公示", "常波 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"四平市铁东区{p['current_post']}的完整履历(各职务起止时间)",
                "why_it_matters": "履历是精确时间线和关系强度的基础",
                "suggested_queries": [f"四平市 铁东区 {p['name']} 简历", f"{p['name']} 任前公示", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "四平市铁东区委常委班子完整名单",
                "why_it_matters": "需组织部长、宣传部长、政法书记、纪委书记等构建完整权力网络",
                "suggested_queries": ["铁东区委 常委会 成员", "铁东区 纪委书记", "铁东区 组织部长"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return result


def write_person_jsons():
    """Write per-person JSON files for core leaders."""
    person_relationships = {p["id"]: [] for p in persons}
    for r in relationships:
        if r["person_a"] in person_relationships:
            person_relationships[r["person_a"]].append(r)
        if r["person_b"] in person_relationships and r["person_b"] != r["person_a"]:
            rev_r = dict(r)
            rev_r["person_a"], rev_r["person_b"] = r["person_b"], r["person_a"]
            person_relationships[r["person_b"]].append(rev_r)

    for p in persons:
        if p["id"] > 10:
            continue
        rels = person_relationships.get(p["id"], [])
        pjson = make_person_json(p, rels)
        job_short = p["current_post"].replace("/", "_").replace("、", "_").replace("，", "_").replace(" ", "_")
        fname = f"{TODAY}-吉林省-四平市-{job_short}-{p['name']}.json"
        path = PJSON_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


def main():
    print(f"\n{'='*60}")
    print("四平市铁东区 Network Build (partial-evidence mode)")
    print('='*60)
    print(f"Date: {AS_OF}")
    print("Web access: PARTIAL — 政府侧官网确认 + 铁东发布微信确认区委书记")
    print()

    print("Building database and GEXF...")
    run_build(
        slug="铁东区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("\nWriting person JSONs...")
    write_person_jsons()

    print(f"\n{'='*60}")
    print("Build complete.")
    print('='*60)
    print(f"DB:      {DB_PATH}")
    print(f"GEXF:    {GEXF_PATH}")
    print(f"Persons: {PJSON_DIR}/")
    print()
    print("Confirmed data:")
    print("  区委书记 常波 (2026 转任, 此前为区长; 铁东发布微信多篇确认)")
    print("  区长:     赵明 (1981年生, 省委党校研究生, 曾任伊通县委副书记正县长级)")
    print("  前任区长→现任书记 常波 (2025-12 前后: 区长→书记)")
    print("  常务副区长: 田枫 (1976, 市政府办系统)")
    print("  副区长: 叶晓斌(1984,北电院), 李论(1981,省委党校), 薛英辉(1975/满族/铁西交流),")
    print("         徐峰(1979/农工党), 岳楠(1990/女/双辽), 杨嘉龙(1987/伊素)")
    print()
    print("⚠️  Missing data (opengaps):")
    print("   1. 常波(区委书记)的出生/民族/学历及任书记具体日期")
    print("   2. 前任区委书记姓名/去向/离任时间")
    print("   3. 区委常委班子成员完整名单")
    print("   4. 各副区长完整当今一轮/任前公示")
    print("   5. 人大主任/政协主席确认")


if __name__ == "__main__":
    main()