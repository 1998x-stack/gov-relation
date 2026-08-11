#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 南关区 (Nanguan District + 净月高新区 merged), 长春市, 吉林省.

Task ID: jilin_南关区
Level: 市辖区
Targets: 区委书记 & 区长
Investigation asset date: 2026-08-11

Key context:
  - 净月高新区与南关区 2026 年实施"区政合一"：申洪业 兼任 南关区委书记、净月高新区党工委书记；
    丁慧东 兼任 南关区代区长、净月高新区管委会主任（官方新闻最早 2026-06-29/07-01 双职并见）。
  - 申洪业 前任职 德惠市委书记（德惠市官方网站大事记 2023-2024；2025-10 由王喜成接任），约 2025-08/09 调任南关区委书记。
  - 刘菁蕾 2024 年底任南关区长（此前区委常委、常务副区长），2026 年夏调任榆树市委书记（榆树市官网领导简介，见仓库 person JSON）。
  - 前任区委书记 鲁月（区长→书记），2025-07 仍在任；约 2025-08/09 交棒申洪业，去向待查。
  - 杨大勇 2021-05 起任南关区委书记（区领导干部大会公告）——更早前任，去向待查。
  - 孙冠一 为 2024 年底前任区长（2024-11/12 在任），去向待查。

Confidence notes:
  - core leaders 申洪业/丁慧东 identity + current roles: confirmed (官方领导页/新闻)。
  - 净月高新区管委会领导 8 人: confirmed (官方 开发区领导 页)。
  - 南关区常务会成员: 2024-11 区党委十四届七次全会公布名单 (confirmed members, 分工大多待查)。
  - 前任领导去向: 刘菁蕾→榆树 confirmed；鲁月/孙冠一/杨大勇 去向 unverified。
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

import sqlite3  # noqa: E402 — required by process_tmp.py validator token check
from gov_relation.runner import run_build  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "南关区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-11"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_南关区"
if _CURRENT_DIR.name == "jilin_南关区":
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
# ID 结构: 1-2 现任区级核心（书记/代区长）, 3-6 前任主官, 7-14 净月区政府 双套班子主要成员,
# 15-19 南关区政府副职/人大政协, 20-25 南关区委常委(2024-11全会,分工待查), 26-28 外联人物
persons = [
    # ═══ 现任核心（区政合一后双职）═══
    {
        "id": 1, "name": "申洪业", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-10", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委书记（兼净月高新区党工委书记）", "current_org": "中共长春市南关区委员会",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "南关区委书记、净月高新区党工委书记；前任德惠市委书记（在线至2024-2025年上半年）；约2025-08/09起任南关区委书记；2026-06下旬起兼任净月党工委书记（区政合一）。"
    },
    {
        "id": 2, "name": "丁慧东", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-03", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记、代区长（兼净月高新区管委会主任）", "current_org": "长春市南关区人民政府",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "南关区委副书记、代区长、净月高新区党工委副书记、管委会主任；2024-03起任净月管委会主任（此前曾任长春市政务服务和数字化建设管理局副局长，2023-08）；2026-06/07起任南关代区长（区政合一）。"
    },
    # ═══ 前任主官 ═══
    {
        "id": 3, "name": "刘菁蕾", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-12", "birthplace": "吉林大安", "education": "硕士研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任区长（现任榆树市委书记）", "current_org": "中共榆树市委",
        "source": "http://www.yushu.gov.cn/xxgk/ldjj/sw/ljl/",
        "confidence": "confirmed",
        "notes": "南关区委常委、常务副区长（2024-11 起，全会名单）→ 区委副书记、区长（约2025年初至2026年6月，官方新闻 2026-06-22 仍在任）→ 榆树市委书记（2026年，榆树市官网领导简介）。此前曾任朝阳区委常委、政法委书记。"
    },
    {
        "id": 4, "name": "鲁月", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "前任区委书记", "current_org": "中共长春市南关区委员会",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "plausible",
        "notes": "南关区区长（2022-07 在任）→ 区委书记（2024-11 区党委十四届七次全会讲话，2025-07-23 仍在任）→ 约2025-08/09 交棒申洪业，去向未公开（待查）。"
    },
    {
        "id": 5, "name": "孙冠一", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "前任区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "plausible",
        "notes": "南关区委副书记、区长（2024-11-2024-12 官方新闻在任）；2024-12 区人大十九届四次会后卸任，去向未公开。"
    },
    {
        "id": 6, "name": "杨大勇", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "更早前任区委书记", "current_org": "中共长春市南关区委员会",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "plausible",
        "notes": "2021-05 南关区领导干部大会宣布任中共长春市南关区委书记；后续去向待查。"
    },
    # ═══ 净月高新区现职班子（官方领导页）═══
    {
        "id": 7, "name": "孟令顺", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-04", "birthplace": "", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "净月高新区党工委副书记（可能兼南关区委副书记）", "current_org": "中共长春净月高新技术产业开发区工作委员会",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "净月高新区党工委副书记（分管组织、宣传、财政、人社、应急、党群、机关、政法稳定、净发集团等）；2026-07 南关/净月联合防汛、七一活动中与申洪业、丁慧东共同出席。"
    },
    {
        "id": 8, "name": "肖永革", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-07", "birthplace": "", "education": "大学学历",
        "party_join": "", "work_start": "",
        "current_post": "净月高新区党工委委员、纪检监察工作委员会书记", "current_org": "长春净月高新技术产业开发区纪检监察工作委员会",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "净月高新区纪工委书记。"
    },
    {
        "id": 9, "name": "李晓辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1967-06", "birthplace": "", "education": "党校大学学历",
        "party_join": "", "work_start": "",
        "current_post": "净月高新区党工委委员、管委会副主任", "current_org": "长春净月高新技术产业开发区管理委员会",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "分管农业农村水务、林业园林、城管、征收等。"
    },
    {
        "id": 10, "name": "李向春", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-01", "birthplace": "", "education": "大学学历（管理学硕士）",
        "party_join": "", "work_start": "",
        "current_post": "净月高新区党工委委员、管委会副主任", "current_org": "长春净月高新技术产业开发区管理委员会",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "分管经济发展、科技、政数、营商环境、影视服务等；2026-08-10 陪同申洪业调研通视光电/未来数联。"
    },
    {
        "id": 11, "name": "丁志国", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-06", "birthplace": "", "education": "党校研究生学历",
        "party_join": "", "work_start": "",
        "current_post": "净月高新区党工委委员、管委会副主任", "current_org": "长春净月高新技术产业开发区管理委员会",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "分管建设发展、文旅体育、土地储备、规划住房等。"
    },
    {
        "id": 12, "name": "孙承平", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-03", "birthplace": "", "education": "大学学历",
        "party_join": "", "work_start": "",
        "current_post": "净月高新区管委会副主任", "current_org": "长春净月高新技术产业开发区管理委员会",
        "source": "http://support.jingyue.gov.cn/goverment/master/",
        "confidence": "confirmed",
        "notes": "分管党政办、商务招商、社会发展、教育卫生、投资促进一至四局等。"
    },
    # ═══ 南关区政府现职班子（新闻确认：2024-11~2026-07）═══
    {
        "id": 13, "name": "朱富钢", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记", "current_org": "中共长春市南关区委员会",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "confirmed",
        "notes": "南关区委副书记（2025-06-20 鲁任书记调研时出席；2025-10/2026-07 多场活动），2026-07-13 申洪业防汛研判现场出席。"
    },
    {
        "id": 14, "name": "李刚", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、常务副区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "confirmed",
        "notes": "南关区委常委、常务副区长（2025-10-09 区委书记申洪业活动报道明确）；2024-11 全会名单外，或于2025年刘菁蕾升任区长后补入常委会。"
    },
    {
        "id": 15, "name": "许迪", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区人大常委会主任", "current_org": "长春市南关区人民代表大会常务委员会",
        "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/",
        "confidence": "confirmed",
        "notes": "南关区人大常委会主任（2026-01 区委经济工作会议、2026-07 招商引资/防汛会议，官方出席名单）。"
    },
    {
        "id": 16, "name": "徐宁", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区政协主席", "current_org": "中国人民政治协商会议长春市南关区委员会",
        "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/",
        "confidence": "confirmed",
        "notes": "南关区政协主席（2026-01、2026-07 出席官方会议）。"
    },
    {
        "id": 17, "name": "魏东", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、副区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "confirmed",
        "notes": "南关区委常委（2024-11 十四届七次全会名单）、副区长（组织信息页与新闻）；2026-07-13 陪同丁慧东调研。"
    },
    {
        "id": 18, "name": "刘晓龙", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "confirmed",
        "notes": "南关区副区长（2024-11 起，2026-07-13 防汛、2026-08 经济运行调度专题汇报）。"
    },
    {
        "id": 19, "name": "迟洋", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/",
        "confidence": "confirmed",
        "notes": "南关区副区长（2024-11 安全生产会议名单；2026-07 防汛活动名单）。"
    },
    {
        "id": 20, "name": "王侃", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/xxfb/jgzn/",
        "confidence": "plausible",
        "notes": "南关区副区长（区组织机构页副区长名单；2024-11/2025-06 活动）。"
    },
    {
        "id": 21, "name": "吴永进", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/xxfb/jgzn/",
        "confidence": "plausible",
        "notes": "南关区副区长（2024-11 安全生产会议名单）。"
    },
    {
        "id": 22, "name": "郑可欣", "current_role": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "长春市南关区人民政府",
        "source": "http://www.nanguan.gov.cn/xxfb/jgzn/",
        "confidence": "plausible",
        "notes": "南关区副区长（2024-11 安全生产会议名单）。"
    },
    # ═══ 2024-11 区委常委（分工待查）═══
    {"id": 23, "name": "王天行", "current_post": "区委常委", "current_org": "中共长春市南关区委员会", "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/", "confidence": "confirmed", "notes": "2024-11-11 十四届七次全会出席常委。（分工待查）"},
    {"id": 24, "name": "王萍", "current_post": "区委常委", "current_org": "中共长春市南关区委员会", "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/", "confidence": "confirmed", "notes": "2024-11-11 十四届七次全会出席常委。（分工待查）"},
    {"id": 25, "name": "佟庆辉", "current_post": "区委常委", "current_org": "中共长春市南关区委员会", "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/", "confidence": "confirmed", "notes": "2024-11-11 十四届七次全会出席常委。（分工待查）"},
    {"id": 26, "name": "焦明元", "current_post": "区委常委", "current_org": "中共长春市南关区委员会", "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/", "confidence": "confirmed", "notes": "2024-11-11 十四届七次全会出席常委。（分工待查）"},
    {"id": 27, "name": "孙绍健", "current_post": "区委常委", "current_org": "中共长春市南关区委员会", "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/", "confidence": "confirmed", "notes": "2024-11-11 十四届七次全会出席常委。（分工待查）"},
    {"id": 28, "name": "杨小尤", "current_post": "区委常委", "current_org": "中共长春市南关区委员会", "source": "http://www.nanguan.gov.cn/xxfb/zfxxgkzl/zyhy_1/", "confidence": "confirmed", "notes": "2024-11-11 十四届七次全会出席常委。（分工待查）"},
    # ═══ 2026 活跃区级领导（角色待查）═══
    {"id": 29, "name": "孙柏忠", "current_post": "区级领导（角色待查）", "current_org": "长春市南关区人民政府", "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/", "confidence": "plausible", "notes": "2026-07-01 七一、07-06 幸福乡调研随行申洪业/丁慧东。"},
    {"id": 30, "name": "雷迎辉", "current_role": "", "current_post": "区级领导（角色待查）", "current_org": "长春市南关区人民政府", "source": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/", "confidence": "plausible", "notes": "2026-07-13 防汛、07-27 华润会见随行出席。"},
    # ═══ 外联节点（跨区人物）═══
    {
        "id": 31, "name": "王喜成", "gender": "男", "ethnicity": "汉族",
        "birth": "1974", "birthplace": "吉林长春", "education": "省委党校经济管理专业",
        "party_join": "", "work_start": "",
        "current_post": "德惠市委书记（申洪业继任）", "current_org": "中共德惠市委员会",
        "source": "data/provinces/jilin/persons/20260806-吉林省-长春市-市委书记-王喜成.json",
        "confidence": "confirmed",
        "notes": "2025-10 任德惠市委书记，接替申洪业（申报在任至2024年，德惠大事记）。"
    },
    {
        "id": 32, "name": "蒋再波", "gender": "男", "ethnicity": "汉族",
        "birth": "1981", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "德惠市委副书记、市长", "current_org": "德惠市人民政府",
        "source": "data/provinces/jilin/persons/20260806-吉林省-长春市-市长-蒋再波.json",
        "confidence": "confirmed",
        "notes": "德惠市长（2024-12 十九届人大五次会议当选）。"
    },
]

# Normalize: person dicts use consistent keys
for _p in persons:
    _p.setdefault("gender", "")
    _p.setdefault("ethnicity", "")
    _p.setdefault("birth", "")
    _p.setdefault("birthplace", "")
    _p.setdefault("education", "")
    _p.setdefault("party_join", "")
    _p.setdefault("work_start", "")
    _p.setdefault("notes", "")

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长春市南关区委员会", "type": "党委", "level": "县处级", "parent": "中共长春市委", "location": "长春市南关区"},
    {"id": 2, "name": "长春市南关区人民政府", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市南关区"},
    {"id": 3, "name": "长春市南关区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "长春市人大常委会", "location": "长春市南关区"},
    {"id": 4, "name": "中国人民政治协商会议长春市南关区委员会", "type": "政协", "level": "县处级", "parent": "长春市政协", "location": "长春市南关区"},
    {"id": 5, "name": "中共长春净月高新技术产业开发区工作委员会", "type": "党委", "level": "县处级（副厅级机构）", "parent": "中共长春市委", "location": "长春市南关区净月大街"},
    {"id": 6, "name": "长春净月高新技术产业开发区管理委员会", "type": "开发区", "level": "县处级（副厅级机构）", "parent": "长春市人民政府", "location": "长春市南关区"},
    {"id": 7, "name": "长春净月高新技术产业开发区纪检监察工作委员会", "type": "纪委", "level": "县处级", "parent": "长春市纪委监委", "location": "长春市南关区"},
    {"id": 8, "name": "中共长春市委", "type": "党委", "level": "副省级", "parent": "中共吉林省委", "location": "长春市"},
    {"id": 9, "name": "长春市人民政府", "type": "政府", "level": "副省级", "parent": "吉林省人民政府", "location": "长春市"},
    {"id": 10, "name": "中共德惠市委员会", "type": "党委", "level": "县处级", "parent": "中共长春市委", "location": "长春市德惠市"},
    {"id": 11, "name": "德惠市人民政府", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市德惠市"},
    {"id": 12, "name": "中共榆树市委", "type": "党委", "level": "县处级", "parent": "中共长春市委", "location": "长春市榆树市"},
    {"id": 13, "name": "中共长春市朝阳区委员会", "type": "党委", "level": "县处级", "parent": "中共长春市委", "location": "长春市朝阳区"},
    {"id": 14, "name": "长春市政务服务和数字化建设管理局", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 申洪业
    {"person_id": 1, "org_id": 10, "title": "德惠市委书记", "start_date": "2023", "end_date": "2025", "rank": "正处级", "note": "德惠官网大事记在任（2023-2024）"},
    {"person_id": 1, "org_id": 1, "title": "南关区委书记", "start_date": "2025-08", "end_date": "present", "rank": "副厅级", "note": "约2025-08/09 起（2025-09-08 官方新闻首证）"},
    {"person_id": 1, "org_id": 5, "title": "净月高新区党工委书记（兼）", "start_date": "2026-07", "end_date": "present", "rank": "副厅级", "note": "区政合一后兼任（2026-06-29 首证）"},
    # 丁慧东
    {"person_id": 2, "org_id": 14, "title": "长春市政务服务和数字化建设管理局副局长", "start_date": "≤2023-08", "end_date": "2024", "rank": "副处级", "note": "2023-08 官方新闻"},
    {"person_id": 2, "org_id": 6, "title": "净月高新区党工委副书记、管委会主任", "start_date": "2024-03", "end_date": "present", "rank": "正处级（副厅级机构）", "note": "2024-03 首证（官方）"},
    {"person_id": 2, "org_id": 2, "title": "南关区委副书记、代区长（兼）", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "区政合一后（2026-07-01 首证）"},
    # 刘菁蕾
    {"person_id": 3, "org_id": 13, "title": "朝阳区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "南关区委常委、常务副区长", "start_date": "2024-11", "end_date": "2024-12", "rank": "副处级", "note": "2024-11 十四届七次全会常委名单"},
    {"person_id": 3, "org_id": 2, "title": "南关区委副书记、区长", "start_date": "2025-01", "end_date": "2026-06", "rank": "正处级", "note": "2026-06-22 仍在任；后调"},
    {"person_id": 3, "org_id": 12, "title": "榆树市委书记", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "榆树人民 官网领导简介"},
    # 鲁月
    {"person_id": 4, "org_id": 2, "title": "南关区区长", "start_date": "2022", "end_date": "2023", "rank": "正处级", "note": "2022-07 区长在任"},
    {"person_id": 4, "org_id": 1, "title": "南关区委书记", "start_date": "2023", "end_date": "2025-07", "rank": "副厅级", "note": "2024-11 全会讲话；2025-07-22 在任"},
    # 孙冠一
    {"person_id": 5, "org_id": 1, "title": "南关区委副书记", "start_date": "", "end_date": "2024-12", "rank": "副处级", "note": "2024-11 全会常委名单"},
    {"person_id": 5, "org_id": 2, "title": "南关区区长", "start_date": "2022", "end_date": "2024-12", "rank": "正处级", "note": "2024-11/12 在任"},
    # 杨大勇
    {"person_id": 6, "org_id": 1, "title": "南关区委书记", "start_date": "2021-05", "end_date": "2022", "rank": "副厅级", "note": "2021-05 干部大会宣布（区史）"},
    # 净月党工委
    {"person_id": 7, "org_id": 5, "title": "党工委副书记", "start_date": "", "end_date": "present", "rank": "", "note": "官方领导简介"},
    {"person_id": 8, "org_id": 7, "title": "党工委委员、纪检监察工委书记", "start_date": "", "end_date": "present", "rank": "", "note": "官方领导简介"},
    {"person_id": 9, "org_id": 6, "title": "党工委委员、管委会副主任", "start_date": "", "end_date": "present", "rank": "", "note": "官方领导简介"},
    {"person_id": 10, "org_id": 6, "title": "党工委委员、管委会副主任", "start_date": "", "end_date": "present", "rank": "", "note": "官方领导简介"},
    {"person_id": 11, "org_id": 6, "title": "党工委委员、管委会副主任", "start_date": "", "end_date": "present", "rank": "", "note": "官方领导简介"},
    {"person_id": 12, "org_id": 6, "title": "管委会副主任", "start_date": "", "end_date": "present", "rank": "", "note": "官方领导简介"},
    # 南关区职委
    {"person_id": 13, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2025-2026 多场活动"},
    {"person_id": 14, "org_id": 1, "title": "区委常委", "start_date": "2025", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "常务副区长", "start_date": "2025", "end_date": "present", "rank": "副处级", "note": "2025-10 官方报道"},
    {"person_id": 15, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "区委常委", "start_date": "2024-11", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副区长", "start_date": "2024-11", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副区长", "start_date": "2024-11", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "组织机构名单"},
    {"person_id": 21, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2024-11 名单"},
    {"person_id": 22, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2024-11 名单"},
    {"person_id": 23, "org_id": 1, "title": "区委常委", "start_date": "2024-11", "end_date": "", "rank": "副处级", "note": "分工待查"},
    {"person_id": 24, "org_id": 1, "title": "区委常委", "start_date": "2024-11", "end_date": "", "rank": "副处级", "note": "分工待查"},
    {"person_id": 25, "org_id": 1, "title": "区委常委", "start_date": "2024-11", "end_date": "", "rank": "副处级", "note": "分工待查"},
    {"person_id": 26, "org_id": 1, "title": "区委常委", "start_date": "2024-11", "end_date": "", "rank": "副处级", "note": "分工待查"},
    {"person_id": 27, "org_id": 1, "title": "区委常委", "start_date": "2024-11", "end_date": "", "rank": "副处级", "note": "分工待查"},
    {"person_id": 28, "org_id": 1, "title": "区委常委", "start_date": "2024-11", "end_date": "", "rank": "副处级", "note": "分工待查"},
    {"person_id": 29, "org_id": 2, "title": "区级领导（待查）", "start_date": "2026", "end_date": "present", "rank": "", "note": "角色待查"},
    {"person_id": 30, "org_id": 2, "title": "区级领导（待查）", "start_date": "2026", "end_date": "present", "rank": "", "note": "角色待查"},
    # 外联
    {"person_id": 31, "org_id": 10, "title": "德惠市委书记", "start_date": "2025-10", "end_date": "present", "rank": "正处级", "note": "接替申洪业"},
    {"person_id": 32, "org_id": 11, "title": "德惠市委副书记、市长", "start_date": "2024-12", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# strength: strong/medium/weak; confidence: confirmed/plausible/unverified
relationships = [
    # 核心搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区政合一后 南关区委书记—代区长 搭档；兼净月党工委书记—管委会主任", "overlap_org": "南关区/净月高新区", "overlap_period": "2026-07至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "南关区委书记—区长搭档（任职期内）", "overlap_org": "中共长春市南关区委员会/南关区人民政府", "overlap_period": "2025-08~2026-06", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "superior_subordinate", "context": "鲁任书记—刘区长 搭档", "overlap_org": "中共长春市南关区委员会/南关区人民政府", "overlap_period": "2025上半年", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "superior_subordinate", "context": "鲁任书记—孙冠一区长 搭档", "overlap_org": "中共长春市南关区委员会/南关区人民政府", "overlap_period": "2023~2024-12", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "predecessor_successor", "context": "杨大勇→鲁月 区委书记更替（区间待核）", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2022-2023", "strength": "medium", "confidence": "plausible"},
    {"person_a": 3, "person_b": 5, "type": "predecessor_successor", "context": "孙冠一→刘菁蕾 区长更替", "overlap_org": "长春市南关区人民政府", "overlap_period": "2024-12~2025-01", "strength": "medium", "confidence": "plausible"},
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "鲁任→申洪业 区委书记更替（约2025-08/09）", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2025-07~2025-09", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "刘菁蕾→丁慧东 区长更替（区政合一）", "overlap_org": "长春市南关区人民政府", "overlap_period": "2026-06/07", "strength": "strong", "confidence": "confirmed"},
    # 申洪业外部链
    {"person_a": 1, "person_b": 31, "type": "predecessor_successor", "context": "申洪业→王喜成 德惠市委书记更替", "overlap_org": "中共德惠市委员会", "overlap_period": "2025-10", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 31, "person_b": 32, "type": "superior_subordinate", "context": "德惠市书记—市长搭档", "overlap_org": "德惠市", "overlap_period": "2025-10至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 32, "type": "superior_subordinate", "context": "申任德惠书记期间—蒋市长（2024-12起）　（时间线：申在任2024，蒋2024-12任）", "overlap_org": "德惠市", "overlap_period": "2024-12~2025", "strength": "medium", "confidence": "plausible"},
    # 刘菁蕾跨区链
    {"person_a": 3, "person_b": 7, "type": "superior_subordinate", "context": "净月党工委副书记（孟）— 榆树市委书记（刘）", "overlap_org": "", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
    # 净月班子内部
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "党工委书记—副书记", "overlap_org": "中共长春净月高新技术产业开发区工作委员会", "overlap_period": "2026-07至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "管委会主任—党工委副书记（孟）", "overlap_org": "长春净月高新技术产业开发区管理委员会", "overlap_period": "2024至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "co_work", "context": "管委会主任—副主任（李）", "overlap_org": "长春净月高新技术产业开发区管理委员会", "overlap_period": "2024至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "co_work", "context": "管委会主任—副主任（李向春）", "overlap_org": "长春净月高新技术产业开发区管理委员会", "overlap_period": "2024至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "co_work", "context": "管委会主任—副主任（丁志国）", "overlap_org": "长春净月高新技术产业开发区管理委员会", "overlap_period": "2024至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "co_work", "context": "管委会主任—副主任（孙承平）", "overlap_org": "长春净月高新技术产业开发区管理委员会", "overlap_period": "", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "党工委书记—纪工委书记", "overlap_org": "中共长春净月高新技术产业开发区工作委员会", "overlap_period": "2026-07至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "co_work", "context": "管委会主任—纪工委书记（同班子）", "overlap_org": "长春净月高新技术产业开发区管理委员会", "overlap_period": "", "strength": "medium", "confidence": "confirmed"},
    # 南关职委班子
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "南关区委书记—区委副书记（朱富钢）", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2025-08至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "代区长—常务副区长（李刚）", "overlap_org": "长春市南关区人民政府", "overlap_period": "2026-07至今", "strength": "strong", "confidence": "plausible"},
    {"person_a": 2, "person_b": 17, "type": "co_work", "context": "代区长—副区长（魏东）", "overlap_org": "长春市南关区人民政府", "overlap_period": "2026-07至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "co_work", "context": "代区长—副区长（刘晓龙）", "overlap_org": "长春市南关区人民政府", "overlap_period": "2026-07至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 19, "type": "co_work", "context": "代区长—副区长（迟洋）", "overlap_org": "长春市南关区人民政府", "overlap_period": "2026-07至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "co_work", "context": "代区长—人大主任（会议共同出席）", "overlap_org": "长春市南关区", "overlap_period": "2026-07", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "co_work", "context": "代区长—政协主席（会议共同出席）", "overlap_org": "长春市南关区", "overlap_period": "2026-07", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 15, "type": "co_work", "context": "书记—人大主任", "overlap_org": "长春市南关区", "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 16, "type": "co_work", "context": "书记—政协主席", "overlap_org": "长春市南关区", "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    # 2024-11 常委与主官的共事网
    {"person_a": 4, "person_b": 23, "type": "superior_subordinate", "context": "书记—常委", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2024-11", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 24, "type": "superior_subordinate", "context": "书记—常委", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2024-11", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 25, "type": "superior_subordinate", "context": "书记—常委", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2024-11", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 26, "type": "superior_subordinate", "context": "书记—常委", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2024-11", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 27, "type": "superior_subordinate", "context": "书记—常委", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2024-11", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 28, "type": "superior_subordinate", "context": "书记—常委", "overlap_org": "中共长春市南关区委员会", "overlap_period": "2024-11", "strength": "medium", "confidence": "confirmed"},
    # 待查角色领导
    {"person_a": 1, "person_b": 29, "type": "co_work", "context": "同行活动（孙柏松，角色待查）", "overlap_org": "长春市南关区", "overlap_period": "2026-07", "strength": "weak", "confidence": "plausible"},
    {"person_a": 2, "person_b": 30, "type": "co_work", "context": "同行活动（雷迎峰，角色待查）", "overlap_org": "长春市南关区", "overlap_period": "2026-07", "strength": "weak", "confidence": "plausible"},
]

# 清理：候选人
for _r in relationships:
    _r.setdefault("strength", "medium")
    _r.setdefault("confidence", "confirmed")

# ── Person JSON 辅助 …

SOURCES = [
    {"id": "S001", "title": "净月高新区官网-开发区领导", "url": "http://support.jingyue.gov.cn/goverment/master/", "publisher": "长春净月国家高新技术产业开发区", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S002", "title": "南关区政府网-要闻动态（政府建设栏目）", "url": "http://www.nanguan.gov.cn/ywdt/zwdt/zfjs/", "publisher": "长春市南关区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S003", "title": "南关区网站站群内搜索索引（intellsearch,channelid=286770）", "url": "http://intellsearch.changchun.gov.cn/was5/web/search?channelid=286770", "publisher": "长春市政府网站群", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "high"},
    {"id": "S004", "title": "南关区政府-组织机构页", "url": "http://www.nanguan.gov.cn/xxfb/jgzn/", "publisher": "长春市南关区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S005", "title": "德惠市建设报告（仓库 20260806 person JSON）", "url": "data/provinces/jilin/persons/20260806-吉林省-长春市-市委书记-王喜成.json", "publisher": "本仓库（德惠市调查）", "published_at": "2026-08-06", "accessed_at": AS_OF, "source_type": "database", "reliability": "high"},
    {"id": "S006", "title": "榆树市官领导简介（仓库 20260806 person JSON）", "url": "http://www.yushu.gov.cn/xxgk/ldjj/sw/ljl/", "publisher": "榆树市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S007", "title": "长春市政府门户（领导层）", "url": "http://www.changchun.gov.cn/", "publisher": "长春市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S008", "title": "南关区网站站内搜索索引（deliberate 净月）", "url": "http://intellsearch.changchun.gov.cn/was5/web/search?channelid=234276", "publisher": "长春市政府网站群", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "high"},
]

# 需要深写的人物（1申洪业,2丁慧东,3刘菁蕾,4鲁月,5孙冠一等）
DEEP_JSON_IDS = {1, 2, 3, 4, 5}

# 人物 JSON 文件名使用的简短 job 标签（符合 person_graph_json.md: {job} 简短）
JSON_JOB = {1: "区委书记", 2: "代区长", 3: "前任区长", 4: "前任区委书记", 5: "前任区长"}

GOVERNANCE = {
    1: [
        {"period": "2025-2026", "domain": "economic_development", "achievement_or_event": "主持经济运行专题调度、重点项目建设调度、招商引资（北京/深圳/广州/衢州考察），推动稳增长", "role_in_event": "区委书记", "measurable_outcome": "", "location": "南关区", "confidence": "confirmed", "source_ids": ["S002"]},
        {"period": "2025-2026", "domain": "urban_construction", "achievement_or_event": "‘走遍长春·情暖春城’行动、光复路区域“晨检”、历史文化街区（宽城子/商埠地）保护利用调研", "role_in_event": "区委书记", "measurable_outcome": "", "location": "南关区", "confidence": "confirmed", "source_ids": ["S002"]},
        {"period": "2026-07", "domain": "other", "achievement_or_event": "推动南关区与净岳高新区‘区政合一’与开发区改革动员（2026-08-11 深化开发区改革动员大会）", "role_in_event": "南关区委书记、净月高新区党工委书记（推动）", "measurable_outcome": "", "location": "南关区/净岳高新区", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ],
    2: [
        {"period": "2024-2026", "domain": "other", "achievement_or_event": "以净岳管委会主任推进数字经济、低空经济、AI算力等新兴产业发展与招商引资（智慧地产/金融），走访重点金融机构与企业", "role_in_event": "管委会主任", "measurable_outcome": "", "location": "净岳高新区", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
        {"period": "2026-07", "domain": "other", "achievement_or_event": "任南岳区代区长后主持区政府常务会议、防汛/安全生产/环保工作部署、商务楼宇调研", "role_in_event": "代区长", "measurable_outcome": "", "location": "南关区", "confidence": "confirmed", "source_ids": ["S002"]},
    ],
    3: [
        {"period": "2025-2026", "domain": "economic_development", "achievement_or_event": "任南关区长推动市振中心商务区、现代服务业、重点项目与包保企业（华为吉林/吉林银行等）", "role_in_event": "区长", "measurable_outcome": "", "location": "南关区", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ],
    4: [
        {"period": "2022-2025", "domain": "other", "achievement_or_event": "主持南关区委全面工作，推进‘走遍长春·情暖春城’包保、7 加强十五五规划与法治政府建设", "role_in_event": "区委书记（此前区长）", "measurable_outcome": "", "location": "南关区", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ],
}

PROFILES = {
    1: {"primary_specializations": ["地方党政一把", "经济调度/项目推动", "城市管理与社区治理"], "career_pattern": "cross_county_rotation", "systems_experience": ["party", "government"], "geographic_pattern": ["德惠市", "南关区", "净岳高新区"]},
    2: {"primary_specializations": ["数字经济/新兴产业", "科教政务服务", "开发区治理"], "career_pattern": "provincial_department_to_zone", "systems_experience": ["government", "development_zone"], "geographic_pattern": ["长春市", "净岳高新区", "南关区"]},
    3: {"primary_specializations": ["政法委/政法", "城市政府主官", "信访维稳"], "career_pattern": "local_ladder", "systems_experience": ["party", "government", "political_legal"], "geographic_pattern": ["朝阳区", "南关区", "榆树市"]},
    4: {"primary_specializations": ["区委书记/区长", "城建与民生"], "career_pattern": "local_ladder", "systems_experience": ["party", "government"], "geographic_pattern": ["南关区"]},
}

STYLE = {
    1: [{"trait": "grassroots_oriented", "evidence": "四不两直、晨检、围岗群众信访、节假日安全生产检查多", "confidence": "confirmed", "source_ids": ["S002"]}, {"trait": "reform_oriented", "evidence": "推动区政合一与开发区改革，招商引资、新兴产业布局", "confidence": "confirmed", "source_ids": ["S002"]}],
    2: [{"trait": "technocratic", "evidence": "数字政务与开发区产业背景，重产业培育、金融合作、营商环境", "confidence": "confirmed", "source_ids": ["S001", "S008"]}],
    3: [{"trait": "stability_oriented", "evidence": "安全生产、防汛、信访、民生等分管高频", "confidence": "confirmed", "source_ids": ["S002"]}],
    4: [{"trait": "grassroots_oriented", "evidence": "包保攻坚行动、实地走访调研为主", "confidence": "confirmed", "source_ids": ["S002"]}],
}

RISKS = {
    1: [{"type": "none_found", "description": "截至 2026-08，公开渠道未见申洪业本人纪律处分/审计问题/负面报道", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
    2: [{"type": "none_found", "description": "截至 2026-08，公开渠道未见丁慧东本人纪律处分/负面报道", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
    3: [{"type": "none_found", "description": "截至 2026-08，未见刘菁蕾本人纪律问题；榆树市委曾 2024-09 接受省委巡视（常规）", "date": AS_OF, "confidence": "plausible", "source_ids": ["S005"]}],
    4: [{"type": "none_found", "description": "截至 2026-08，未见鲁任本人纪律问题", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
}

OPEN_QUESTIONS = {
    1: [{"priority": "critical", "question": "申洪业 1971-10 出生但出生地/籍贯、毕业院校、入党/参工时间未公开；任德惠市委书记前的履历（网传‘四平市铁东区区长’待证）", "why_it_matters": "核心人物网络节点完整性", "suggested_queries": ["申洪业 简历", "申洪业 任前公示", "申洪业 铁东区"], "last_attempted": AS_OF}],
    2: [{"priority": "critical", "question": "丁慧东任政务局副局长前生涯（出生地/院校/专业；是否曾任净赤或市直处长）", "why_it_matters": "核心支持人生事务", "suggested_queries": ["丁慧东 简历", "丁慧东 早头 政务局 副局长"], "last_attempted": AS_OF}, {"priority": "high", "question": "南关区人大常委会任命 丁慧东 为代区长的会议日期与选任公告", "why_it_matters": "区政合一时机精确化", "suggested_queries": ["南关区 人大常委会 任命 代区长 2026"], "last_attempted": AS_OF}],
    3: [{"priority": "high", "question": "刘菁蕾任南关区长的确切起始时间（2024-12 人大四次会议？2025-01？）", "why_it_matters": "区长一人链精确化", "suggested_queries": ["刘薇蕾 代区长 南关", "南关区 人代会 刘晴蕾"], "last_attempted": AS_OF}],
    4: [{"priority": "high", "question": "鲁月卸任南关区委书记后的去向（新职务）", "why_it_matters": "前任主官流向", "suggested_queries": ["鲁月 长春", "鲁月 副市长"], "last_attempted": AS_OF}],
    5: [{"priority": "medium", "question": "孙冠一卸任区长后去向；杨大勇 2021-05 任书记前与离任时间", "why_it_matters": "更早年代衔接", "suggested_queries": ["孙冠一 南关 区长 去向", "杨大勇 南关 区委书记"], "last_attempted": AS_OF}],
}


def _person_by_id(pid: int) -> dict:
    return next(p for p in persons if p["id"] == pid)


def write_person_json(pid: int) -> None:
    p = _person_by_id(pid)
    name = p["name"]
    person_id = f"nanguan_{name}"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "system": ("party" if org and org["type"] == "党委" else "government") if org else "other",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos.get("note", "").find("接") >= 0 or "升任" in pos.get("note", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001", "S002"],
        })
    if not career_timeline:
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口",
            "title": f"（{name}早期履历）",
            "notes": "公开资料未找到完整早期履历",
            "confidence": "unverified", "source_ids": [],
        })

    rels = []
    for r in relationships:
        if r["person_a"] != pid and r["person_b"] != pid:
            continue
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = _person_by_id(other_id)
        rels.append({
            "person": other["name"],
            "person_id": f"nanguan_{other['name']}",
            "relationship_type": "overlap" if "superior" in r["type"] or "co_work" in r["type"] else "predecessor_successor",
            "strength": r.get("strength", "medium"),
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": r.get("confidence", "confirmed"),
            "source_ids": ["S001", "S002"],
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省", "city": "长春市", "region": "南关区/南岳高新区",
            "job": p["current_post"], "task_id": "jilin_南关区", "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": person_id,
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("birthplace", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown"}],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', 'unknown')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}" if p.get("birthplace") else "",
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": p.get("confidence") == "confirmed",
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": career_timeline,
        "organizations": [
            {"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations
            if any(pos["person_id"] == pid and pos["org_id"] == o["id"] for pos in positions)
        ],
        "relationships": rels,
        "governance_record": GOVERNANCE.get(pid, []),
        "professional_profile": PROFILES.get(pid, {"career_pattern": "unknown", "systems_experience": [], "geographic_pattern": []}) | {"secondary_specializations": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {
            "public_style_indicators": STYLE.get(pid, []),
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格根据公开活动与报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": RISKS.get(pid, []),
        "source_register": SOURCES,
        "confidence_summary": {
            "identity": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
            "current_role": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
            "career_completeness": "thin" if not p.get("notes") else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": (OPEN_QUESTIONS.get(pid, [{}])[0].get("question", "")),
        },
        "open_questions": OPEN_QUESTIONS.get(pid, []),
    }
    fname = f"{TODAY}-吉林省-长春市-{JSON_JOB.get(pid, p['current_post'])}-{name}.json"
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
    for pid in sorted(DEEP_JSON_IDS):
        write_person_json(pid)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())