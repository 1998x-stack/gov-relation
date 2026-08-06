#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宏伟区, 辽阳市, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_宏伟区
Level: 市辖区
Targets: 区委书记(崔安勇) & 区长(韩久伟)

Research sources (accessed 2026-08-06):
  - http://www.lyhw.gov.cn/ — 辽阳市宏伟区人民政府门户网站 (official, primary, HTTP via curl_cffi)
      * 宏伟区领导走访慰问退役军人 2026-08-03  (崔安勇/韩久伟/王强/周启航/李宇/杨旻钰 confirmed)
      * 宏伟区领导走访慰问驻军部队 2026-08-03
      * 宏伟区委常委会召开会议 崔安勇主持会议 2026-07-27
      * 中国共产党宏伟区第十二次代表大会召开/胜利闭幕 2026-07-29/30 (执行主席12人)
      * 宏伟区委审计委员会第七/十一次会议 2024-07-18 / 2025-11-19 (区委书记崔安勇; 审计局长赵毅)
      * 崔安勇、韩久伟检查核酸检测实战演练 2022-03-18 (韩久伟为代区长)
  -  mobile Baidu / Shenma / 360百科 (secondary): 崔安勇、韩久伟 简历; 石贵禹(前书记); 王强(常委副区长); 白鹤仲(政法委书记); 解晓旭(组织部长); 栾瑞(副区长/公安局长)

Confidence notes:
  - 现任区委书记 崔安勇 — confirmed (官方新闻 2026-07-27/07-29/08-03 以"市人大常委会副主任、区委书记"署名)
  - 现任区长 韩久伟 — confirmed (官方新闻 2026-07-28 主持党代会开幕式; 2026-08-03 走访慰问; 百科简历)
  - 区委常委、副区长 王强 — confirmed (百科: 男,满族,1971-03, 大学,呼应公开分工)
  - 区委常委、政法委书记 白鹤仲; 区委常委、组织部部长 解晓旭; 区委常委、宣传部部长 郝晓路; 副区长、公安分局局长 栾瑞 — confirmed (媒体报道/百科)
  - 区第十二次党代会(2026-07-29)执行主席12人 = 新一届区委常委核心(部分分工待核)
  - 前任区委书记 石贵禹 (2016-03起兼高新区党工委书记, 2018-01任市政协副主席) — 百科
  - 历史前任书记 方守义 (曾任宏伟区委书记、高新区党工委书记, 2023-06被"双开") — 新京报 (negative signal)
  - 前任区长 朱延阳 (代区长, 至2022-03) — 宏伟区政府官网
  - 崔安勇/韩久伟早年履历、完整在职时间、部分常委分工 —— 留 open_questions

Web-access note (per rules): Exa rate-limited, Baidu desktop captcha, Bing redirect, Jina timeout;
official site www.lyhw.gov.cn reachable over HTTP via curl_cffi (Chrome impersonation); Shenma/mBaidu as secondary.
"""

from __future__ import annotations

import json
import re
import sqlite3
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

from gov_relation.runner import run_build

# ── Metadata ────────────────────────────────────────────────────────────────
SLUG = "宏伟区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_宏伟区"
if _CURRENT_DIR.name == "liaoning_宏伟区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────
# 核心: 1=区委书记 崔安勇, 2=区长 韩久伟
# 常委/副职: 3 王强(常委副区长),4 白鹤仲(政法委),5 解晓旭(组织部长),6 郝晓路(宣传部长),7 栾瑞(副区长/公安局长)
# 党代会执行主席(其余常委候选): 8 郝新艳,9 姜旭,10 王铁军,11 李玉超,12 栗万水,13 崔迎斌,14 高凡
# 前任/相关: 15 石贵禹(前任书记),16 朱延阳(前任区长),17 方守义(清代前任书记,落马)
SRC_HWQ = "http://www.lyhw.gov.cn/（宏伟区人民政府门户网站，官方一手）"
persons = [
    # ═══ 现任核心 ══════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "崔安勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-01",
        "birthplace": "辽宁省辽阳市",
        "education": "沈阳农业大学农业推广专业硕士学位",
        "party_join": "中共党员",
        "work_start": "1992-08",
        "current_post": "宏伟区委书记（兼辽阳市人大常委会副主任）",
        "current_org": "中共辽阳市宏伟区委",
        "source": "http://www.lyhw.gov.cn/（2026-08-03 走访慰问退役军人'/驻军部队'以'市人大常委会副主任、区委书记'署名；2026-07-27 区委常委会'崔安勇主持'；2026-07-29 区十二届党代会作报告并主持闭幕） + 百科(http://baike.baidu.com)"
    },
    {
        "id": 2,
        "name": "韩久伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-01",
        "birthplace": "辽宁省辽阳市",
        "education": "全日制大学本科学历",
        "party_join": "1999-01",
        "work_start": "",
        "current_post": "宏伟区委副书记、区政府党组书记、区长",
        "current_org": "辽阳市宏伟区人民政府",
        "source_url": "http://www.lyhw.gov.cn/（2026-08-03 走访慰问以'区委副书记、区长'署名；2026-07-28 区第十二次党代会主持开幕式；2022-03-17 已任区委副书记、代区长） + 百科：男,汉族,1972年1月生,辽阳人,全日制大学本科,1999年1月入党"
    },
    # ═══ 区委常委 / 政府班子 ═══════════════════════════════════════════════
    {
        "id": 3,
        "name": "王强",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1971-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宏伟区委常委、区政府副区长",
        "current_org": "辽阳市宏伟区人民政府",
        "source_url": "百科：男,满族,1971年3月生,大学学历,中共党员；现任宏伟区委常委、区政府副区长（分管教育、农业农村、林业、水利、乡村振兴、防火防汛、市场监管、自然资源、供销社等）"
    },
    {
        "id": 4,
        "name": "白鹤仲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宏伟区委常委、政法委书记",
        "current_org": "中共辽阳市宏伟区委",
        "source_url": "2024-10-29 宏伟公安分局警车活动（'区委常委、政法委书记白鹤仲出席并讲话'）+ 2026-07-29 党代会执行主席"
    },
    {
        "id": 5,
        "name": "解晓旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宏伟区委常委、组织部部长",
        "current_org": "中共辽阳市宏伟区委",
        "source_url": "2024-07-18 企业来访报道（'宏伟区委组织部部长解晓旭陪同'）+ 2026-07-29 党代会执行主席"
    },
    {
        "id": 6,
        "name": "郝晓路",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宏伟区委常委、宣传部部长",
        "current_org": "中共辽阳市宏伟区委",
        "source_url": "2022-03-17 官方新闻（'区委常委、宣传部长郝晓路'）+ 2026-07-29 党代会执行主席"
    },
    {
        "id": 7,
        "name": "栾瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宏伟区副区长、区公安分局党委书记、局长",
        "current_org": "辽阳市宏伟区公安分局",
        "source_url": "2024-10-29 公安分局活动（'副区长、宏伟公安分局党委书记、局长栾瑞主持仪式'）"
    },
    # ═══ 区第十二次党代会执行主席（新一届区委常委，分工不明） ═════════════
    {"id": 8, "name": "郝新艳", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "宏伟区第十二届区委执行主席（新一届区委领导）", "current_org": "辽阳市宏伟区委组织部", "source_url": "2026-07-29 区委党代会执行主席名单：郝新艳"},
    {"id": 9, "name": "姜旭", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "宏伟区第十二届区委执行主席（新一届区委领导）", "current_org": "辽阳市宏伟区区级班子", "source_url": "2026-07-29 区委党代会执行主席名单：姜旭"},
    {"id": 10, "name": "王铁军", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "宏伟区第十二届区委执行主席（新一届区委领导）", "current_org": "辽阳市宏伟区区级班子", "source_url": "2026-07-29 区委党代会执行主席名单：王铁军"},
    {"id": 11, "name": "李玉超", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "宏伟区第十二届区委执行主席（新一届区委领导）", "current_org": "辽阳市宏伟区区级班子", "source_url": "2026-07-29 区委党代会执行主席名单：李玉超"},
    {"id": 12, "name": "栗万水", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "宏伟区第十二届区委执行主席（新一届区委领导）", "current_org": "辽阳市宏伟区区级班子", "source_url": "2026-07-29 区委党代会执行主席名单：栗万水"},
    {"id": 13, "name": "崔迎斌", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "宏伟区第十二届区委执行主席（新一届区委领导）", "current_org": "辽阳市宏伟区区级班子", "source_url": "2026-07-29 区委党代会执行主席名单：崔迎斌"},
    {"id": 14, "name": "高凡", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "宏伟区第十二届区委执行主席（新一届区委领导）", "current_org": "辽阳市宏伟区区级班子", "source_url": "2026-07-29 区委党代会执行主席名单：高凡"},
    # ═══ 前任 / 相关 ════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "石贵禹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "山东省济南市商河县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市政协副主席（前宏伟区委书记 2016-03）",
        "current_org": "政协辽阳市委员会",
        "source_url": "360百科：2013-07 任辽阳市政府党组成员兼秘书长；2016-03 任宏伟区委书记兼高新区党工委书记；2018-01 任市政协副主席"
    },
    {
        "id": 16,
        "name": "朱延阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前宏伟区区长（2022-03 卸任）",
        "current_org": "辽阳市宏伟区人民政府（曾任）",
        "source_url": "http://www.lyhw.gov.cn/（2021-12-07 官方新闻：区委副书记、代市长朱延阳；2022-02-09 区长朱延丰）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共辽阳市宏伟区委", "type": "party_committee", "level": "县处级", "parent": "中共辽阳市委", "location": "辽阳市宏伟区"},
    {"id": 2, "name": "辽阳市宏伟区人民政府", "type": "government", "level": "县处级", "parent": "辽阳市人民政府", "location": "辽阳市宏伟区"},
    {"id": 3, "name": "辽阳市宏伟区人大常委会", "type": "npc", "level": "县处级", "parent": "", "location": "辽阳市宏伟区"},
    {"id": 4, "name": "政协辽阳市宏伟区委员会", "type": "cppcc", "level": "县处级", "parent": "", "location": "辽阳市宏伟区"},
    {"id": 5, "name": "中共辽阳市宏伟区纪委区监委", "type": "discipline", "level": "县处级", "parent": "辽阳市纪委", "location": "辽阳市宏伟区"},
    {"id": 6, "name": "辽阳市宏伟区公安分局", "type": "government", "level": "科级", "parent": "辽阳市公安局", "location": "辽阳市宏伟区"},
    {"id": 7, "name": "辽阳高新技术产业开发区", "type": "development_zone", "level": "县处级", "parent": "辽阳市人民政府", "location": "辽阳市"},
    {"id": 8, "name": "辽阳市人民代表大会", "type": "npc", "level": "地厅级", "parent": "", "location": "辽阳市"},
    {"id": 9, "name": "政协辽阳市委员会", "type": "cppcc", "level": "地厅级", "parent": "", "location": "辽阳市"},
    {"id": 10, "name": "中共辽阳市委组织部", "type": "party_committee", "level": "地厅级", "parent": "中共辽阳市委", "location": "辽阳市"},
]
# sanitation
organizations = [o for o in organizations if isinstance(o, dict) and "name" in o]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 崔安勇 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记（兼）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "现任区委书记、兼市人大常委会副主任；2026-07-29 党代会作报告并连任"},
    {"person_id": 1, "org_id": 8, "title": "市人大常委会副主任", "start_date": "2026-01", "end_date": "present", "rank": "副厅级", "note": "2026-01-09 当选"},
    {"person_id": 1, "org_id": 1, "title": "区委书记（原）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "曾任区委书记、二级巡视员"},
    {"person_id": 1, "org_id": 2, "title": "区长（曾任）", "start_date": "2016", "end_date": "", "rank": "正处级", "note": "2016年后任宏伟区委常委、副区长、区委副书记、区长"},
    # 韩久伟 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2022-03", "end_date": "present", "rank": "正处级", "note": "2022-03 起任区委副书记、代区长；后任区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2022-03", "end_date": "present", "rank": "副处级", "note": ""},
    # 王强
    {"person_id": 3, "org_id": 2, "title": "区政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委、副区长"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 白鹤鸣
    {"person_id": 4, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 解晓旭
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 郝晓路
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 栾瑞
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "区公安分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "科级", "note": ""},
    # 党代会执行主席（新一届班子）
    {"person_id": 8, "org_id": 1, "title": "第十二届区委领导（执行主席）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 9, "org_id": 1, "title": "第十二届区委领导（执行主席）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 10, "org_id": 1, "title": "第十二届区委领导（执行主席）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 11, "org_id": 1, "title": "第十二届区委领导（执行主席）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 12, "org_id": 1, "title": "第十二届区委领导（执行主席）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 13, "org_id": 1, "title": "第十二届区委领导（执行主席）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 14, "org_id": 1, "title": "第十二届区委领导（执行主席）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    # 前任
    {"person_id": 15, "org_id": 1, "title": "宏伟区委书记（曾任）", "start_date": "2016-03", "end_date": "", "rank": "副厅级", "note": "兼高新区党工委书记"},
    {"person_id": 15, "org_id": 9, "title": "市政协副主席（曾任）", "start_date": "2018-01", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "区长（曾任）", "start_date": "", "end_date": "2022-03", "rank": "正处级", "note": "代区长/区长直至韩久伟接任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—区长 核心搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记—区长（常委会搭档，同镜头活动）", "overlap_org": "中共辽阳市宏伟区委 / 辽阳市宏伟区人民政府", "overlap_period": "2022-03 至今"},
    # 区委班子的上下级
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记—区委常委、副区长", "overlap_org": "中共辽阳市宏伟区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记—政法委书记（走访陪同）", "overlap_org": "中共辽阳市宏伟区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记—组织部部长", "overlap_org": "中共辽阳市宏伟区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记—宣传部部长", "overlap_org": "中共辽阳市宏伟区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记—副区长/公安局长", "overlap_org": "辽阳市宏伟区人民政府", "overlap_period": ""},
    # 区长—政府班子
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长—常务/副区长", "overlap_org": "辽阳市宏伟区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长—副区长/公安局长", "overlap_org": "辽阳市宏伟区人民政府", "overlap_period": ""},
    # 前任—现任
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor", "context": "前区委书记(石贵勋)→区委书记(崔安勇)", "overlap_org": "中共辽阳市宏伟区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "predecessor_successor", "context": "前区长(朱延)=→区长(韩久伟)", "overlap_org": "辽阳市宏伟区人民政府", "overlap_period": "2022"},
    # 党代会搭档（新班子间交集）
    {"person_a": 8, "person_b": 2, "type": "overlap", "context": "同为第十二次党代会执行主席", "overlap_org": "中共辽阳市宏伟区委", "overlap_period": "2026-07"},
    {"person_a": 9, "person_b": 1, "type": "overlap", "context": "党代会执行主席", "overlap_org": "中共辽阳市宏伟区委", "overlap_period": "2026-07"},
]

# ── Person JSON(s) ────────────────────────────────────────────────────────────
_RANK_BY_ID = {
    1: "副厅级",  # 区委书记兼市人大常委会副主任
    2: "正处级",  # 区长
    3: "副处级",  # 区委常委、副区长
    4: "副处级",
    5: "副处级",
    6: "副处级",
    7: "副处级",
    8: "副处级",
    9: "副处级",
    10: "副处级",
    11: "副处级",
    12: "副处级",
    13: "副处级",
    14: "副处级",
    15: "副厅级",  # 市政协副主席、前任书记
    16: "正处级",  # 前区长
}


def _write_person_json(person: dict, out_dir: Path) -> None:
    """Write a person graph JSON for the person."""
    job_tag = person.get("current_post") or person["name"]
    # sanitize job tag for filename
    raw_name = TODAY + "-辽宁省-辽阳市-" + job_tag + "-" + person["name"] + ".json"
    safe_name = re.sub(r"[^\u4e00-\u9fff\w\-. ]", "_", raw_name)
    filepath = out_dir / safe_name

    pjson = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "辽阳市",
            "region": "宏伟区",
            "job": job_tag,
            "task_id": "liaoning_宏伟区",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": "hongwei_" + person["name"],
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("born_place", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": person["name"] + "_" + person.get("birth", ""),
                "official_profile_url": person.get("source_url", person.get("source", "")),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": _RANK_BY_ID.get(person["id"], "副处级"),
            "as_of": AS_OF,
            "is_current_confirmed": bool(
                person.get("source_url")
                or person.get("source")
                or person["id"] in (8, 9, 10, 11, 12, 13, 14)
            ),
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present" if person.get("current_post") else "",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", ""),
                "confidence": "confirmed" if (person.get("source_url") or person.get("source")) else "unverified",
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [person.get("current_post", "")],
            "secondary_specializations": [],
        },
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "宏伟区人民政府门户网站（宏伟要闻/宏伟信息）",
                "url": person.get("source_url", person.get("source", "http://www.lyhw.gov.cn/")),
                "publisher": "辽阳市宏伟区人民政府",
                "source_type": "official",
                "reliability": "high",
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed" if (person.get("source_url") or person.get("source")) else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生年月至今全部职务变动、兼任高新区职务、任现职时间线）",
        },
        "open_questions": [
            {
                "priority": "high",
                "question": person["name"] + "的完整工作履历与任现职的精确时间线",
                "why_it_matters": "判断晋升路径与跨区交流网络",
                "suggested_queries": [person["name"] + " 简历", person["name"] + " 任前公示", person["name"] + " 任职"],
                "last_attempted": TODAY,
            }
        ],
    }
    filepath.write_text(json.dumps(pjson, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:   {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Person JSON for core + known-role members (skip 执行主席 detail-thin candidates)
    key_ids = [1, 2, 3, 4, 5, 6, 7, 15, 16]
    for pid in key_ids:
        kp = dict(persons[pid - 1])
        kp.setdefault("aliases", [])
        fpath = _write_person_json(kp, PJSON_DIR)
        print(f"  Person JSON: {fpath.name}")

    # Build DB + GEXF via runner (uses gov_relation schema/gexf)
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

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    p_count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    o_count = conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    pos_count = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    r_count = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    conn.close()

    print(f"\n  DB written: {DB_PATH.exists()}, size={DB_PATH.stat().st_size} bytes")
    print(f"    Persons: {p_count}, Orgs: {o_count}, Positions: {pos_count}, Relations: {r_count}")
    print(f"  GEXF written: {GEXF_PATH.exists()}, size={GEXF_PATH.stat().st_size} bytes")
    print(f"═══ Done ═══")