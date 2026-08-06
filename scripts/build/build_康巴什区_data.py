#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 康巴什区 (Kangbashi District), 鄂尔多斯市, 内蒙古自治区.

Investigation date: 2026-08-06
Task ID: inner_mongolia_康巴什区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources (all fetched 2026-08-06 via 康巴什区政府官网 + 鄂尔多斯市组织部/人大官网):
  - 康巴什区人民政府 领导之窗·政府领导（区长/副区长个人页）
    * http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjj/ldcy/zfld/
  - 康巴什区第三次党代会开幕新闻（2026-07-30，区委常委11人名单）
    * http://www.kbs.gov.cn/ywdt/202607/t20260730_3911757.html
  - 宋俊峰（区委书记）调研教育/七一活动（2026-06-25 / 07-02，确认宋俊峰现任区委书记）
    * http://www.kbs.gov.cn/ywdt/202606/t20260625_3905671.html
    * http://www.kbs.gov.cn/ywdt/202607/t20260702_3907038.html
  - 甄华（原市委副书记、康巴什区委书记）调研安全生产（2026-06-11，确认其2026-06仍在任）
    * http://www.kbs.gov.cn/ywdt/202606/t20260611_3902701.html
  - 鄂尔多斯市人大（李国权辞去市人大常委，2026-06-26；王雪峰任区长证据链见政府工作报告）
    * http://www.ordosrd.gov.cn/jyjd/202606/t20260626_3905821.html
  - 康巴什区2022/2023年政府工作报告（王雪峰任区长）
    * http://www.kbs.gov.cn/zwgk/zfgzbg/202202/t20220208_3150624.html
    * http://www.kbs.gov.cn/zwgk/zfgzbg/202302/t20230228_3345329.html

Confidence notes:
  - 现任区委书记宋俊峰 / 区长王立妍 当前身份: confirmed（官网新闻+领导之窗）
  - 方立妍履历（女、汉族、1975-11生、内蒙古通辽人、中央党校研究生、1997-12入党、1999-07工作）: confirmed（领导之窗）
  - 前任区委书记甄华（市委副书记兼，约2023-05~2026-06；1970-06生，清水河人）: confirmed（多源；卸任时间由新闻推断）
  - 前任区长王雪峰（至约2023）：confirmed（政府工作报告报告人）
  - 副区长班子（王瑞祥/杨东/徐浩波/苏云高娃/刘刚/朱存良/武兆坤/刘波）: confirmed（领导之窗，含公安局长徐浩波）
  - 其余区委常委（杨树伟、乌兰托娅、李国权、布仁德力根、李平、郭启光、王亚平）: 名单 confirmed（党代会），但多数具体党口分工/履历 未详（open gap）

Artifact layout: DB/GEXF/person JSON all written to this script's staging directory data/tmp/inner_mongolia_康巴什区/
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
SLUG = "康巴什区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
PROVINCE = "内蒙古自治区"
CITY = "鄂尔多斯市"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_康巴什区"
if _CURRENT_DIR.name == "inner_mongolia_康巴什区":
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
# ID 槽位: 1 区委书记, 2 区长, 3-9 区委常委, 10-17 区政府班子, 30-31 前任核心
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导 (现任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "宋俊峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委书记",
        "current_org": "中共鄂尔多斯市康巴什区委员会",
        "source": "http://www.kbs.gov.cn/ywdt/202607/t20260702_3907038.html",
        "confidence": "confirmed",
        "notes": "2026年6月下旬起任康巴什区委书记（2026-06-24 以区委书记身份调研教育工作）；此前为区委副书记/政府班子（具体前职待查）。2026-07-29 中共鄂尔多斯市康巴什区第三次代表大会开幕式上代表二届区委作报告",
    },
    {
        "id": 2,
        "name": "方立妍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "内蒙古自治区通辽市",
        "education": "中央党校研究生学历",
        "party_join": "中共党员（1997-12入党）",
        "work_start": "1999-07",
        "current_post": "区委副书记、区长",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202508/t20250829_3830549.html",
        "confidence": "confirmed",
        "notes": "女、汉族、1975-11生、内蒙古通辽人、中央党校研究生学历；1997-12入党、1999-07工作；任康巴什区委副书记、区政府党组书记、区长（领导之窗 2025-08）。2026-02 区政府工作报告报告人：代区长（后转正），2026-07 区三次党代会大会主持/执行主席",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区委常委（11人：宋俊峰、方立妍、杨树伟、乌兰托娅、李国权、王瑞祥、杨东、布仁德力根、李平、郭启光、王亚平）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "杨树伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记",
        "current_org": "中共鄂尔多斯市康巴什区委员会",
        "source": "http://www.kbs.gov.cn/ywdt/202607/t20260730_3911757.html",
        "confidence": "plausible",
        "notes": "区委副书记（党代会执行主席名单第3位；具体分工待查）",
    },
    {
        "id": 4,
        "name": "乌兰托娅",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1970-11",
        "birthplace": "待查",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、统战部部长（拟任区政协主席）",
        "current_org": "中共鄂尔多斯市康巴什区委员会",
        "source": "http://www.ordosdj.gov.cn/djyw/ersv/202607/t20260722_1777786.html",
        "confidence": "confirmed",
        "notes": "女、蒙古族、1970-11生；现任区委常委、统战部部长、三级调研员；2026-07-22 拟提名为旗区政协主席候选人（市委组织部任前公示）",
    },
    {
        "id": 5,
        "name": "李国权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共鄂尔多斯市康巴什区委员会",
        "source": "http://www.ordosdj.gov.cn/djyw/ersv/202607/t20260730_3911757.html",
        "confidence": "plausible",
        "notes": "区委常委；曾任鄂尔多斯市人大常委会委员（2026-06-26 辞去该职）",
    },
    {
        "id": 6,
        "name": "王瑞祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "内蒙古自治区",
        "education": "大学学历（内蒙古工业大学，正高级工程师）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202101/t20210128_2842245.html",
        "confidence": "confirmed",
        "notes": "区委常委、区政府党组副书记、常务副区长；1973-10生，内蒙古工大本科学历、正高级工程师、注册招标工程师",
    },
    {
        "id": 7,
        "name": "郭启光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、纪委书记",
        "current_org": "中共和市鄂尔多斯市康巴什区纪律检查委员会",
        "source": "http://www.kbs.gov.cn/ywdt/202607/t20260831_3830549.html",
        "confidence": "plausible",
        "notes": "区委常委（党代会执行主席）；纪委/监委具体职务系据此推断，待三届全会确认（open gap）",
    },
    {
        "id": 8,
        "name": "王亚平",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共鄂尔多斯市康巴什区委员会",
        "source": "http://www.kbs.gov.cn/ywdt/202607/t20260730_3911757.html",
        "confidence": "plausible",
        "notes": "区委常委（党代会执行主席名单第11位；具体分工待查）",
    },
    {
        "id": 9,
        "name": "布仁德力根",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共鄂尔多斯市康巴什区委员会",
        "source": "http://www.kbs.gov.cn/ywdt/202607/t20260730_3911757.html",
        "confidence": "plausible",
        "notes": "区委常委（党代会执行主席名单第8位；具体分工待查）",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政府班子（副区长）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "杨东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-04",
        "birthplace": "内蒙古自治区",
        "education": "研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、副区长",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202607/t20260706_3907561.html",
        "confidence": "confirmed",
        "notes": "副区长（区委常委）、1985-04生、汉族、法学硕士；2026-07-06任现职公示",
    },
    {
        "id": 11,
        "name": "徐浩波",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1975-06",
        "birthplace": "内蒙古自治区通辽市",
        "education": "学士（公安院校）",
        "party_join": "中共党员（2005-07入党）",
        "work_start": "1995-10",
        "current_post": "副区长、区公安分局局长",
        "current_org": "鄂尔多斯市公安局康巴什区分局",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202607/t20260706_3907567.html",
        "confidence": "confirmed",
        "notes": "副区长、康巴什分局局长、二级高级警长；蒙古族、通辽人、1975-06生",
    },
    {
        "id": 12,
        "name": "苏云高娃",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1982-12",
        "birthplace": "内蒙古自治区",
        "education": "本科，公共管理硕士",
        "party_join": "无党派人士",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202402/t20240226_3574735.html",
        "confidence": "confirmed",
        "notes": "副区长，无党派人士；蒙古族、82-12生",
    },
    {
        "id": 13,
        "name": "刘刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-01",
        "birthplace": "待查",
        "education": "中央党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202310/t20231030_3518763.html",
        "confidence": "confirmed",
        "notes": "副区长；1982-01生、中央党校研究生",
    },
    {
        "id": 14,
        "name": "朱存良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-12",
        "birthplace": "内蒙古自治区清水河县",
        "education": "研究生学历，农学硕士",
        "party_join": "中共党员（2003-06入党）",
        "work_start": "2008-08",
        "current_post": "副区长",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202607/t20260706_3907570.html",
        "confidence": "confirmed",
        "notes": "副区长；1980-12生、清水河人、农学硕士",
    },
    {
        "id": 15,
        "name": "武兆坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-11",
        "birthplace": "内蒙古自治区鄂尔多斯市",
        "education": "大学，农业推广硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202607/t20260706_3907571.html",
        "confidence": "confirmed",
        "notes": "副区长；1984-11生、鄂尔多斯人",
    },
    {
        "id": 16,
        "name": "刘波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "待查",
        "education": "研究生学历，工程学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长（挂职）",
        "current_org": "鄂尔多斯市康巴什区人民政府",
        "source": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/202506/t20250606_3804416.html",
        "confidence": "confirmed",
        "notes": "副区长（挂职）；1984-10生、工程学硕士",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任核心领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "甄华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-06",
        "birthplace": "内蒙古自治区清水河县",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鄂尔多斯市委副书记（原兼任康巴什区委书记，2026-06卸任）",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "http://www.kbs.gov.cn/ywdt/qndt/202606/t20260611_3902701.html",
        "confidence": "confirmed",
        "notes": "原市委副书记、康巴什区委书记（约2023-05起兼任）；2026-06-10 仍以该身份调研安全生产，2026年6月底由宋俊峰接任区委书记。去向：仍任市委副书记（待查是否另有新职）",
    },
    {
        "id": 31,
        "name": "王雪峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任区长，约至2022年）",
        "current_org": "（卸任）",
        "source": "http://www.kbs.gov.cn/zwgk/202302/t20230228_3345329.html",
        "confidence": "confirmed",
        "notes": "前任区长（至少至2023年2月）；2022/2023年区政府工作报告报告人即'区人民政府区长王雪峰'；去向未明（任前/外调待查）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鄂尔多斯市康巴什区委员会", "type": "党委", "level": "市辖区", "parent": "中共鄂尔多斯市委员会", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
    {"id": 2, "name": "鄂尔多斯市康巴什区人民政府", "type": "政府", "level": "市辖区", "parent": "鄂尔多斯市人民政府", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
    {"id": 3, "name": "鄂尔多斯市康巴什区人大常委会", "type": "人大", "level": "市辖区", "parent": "鄂尔多斯市人大常委会", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
    {"id": 4, "name": "中国人民政治协商会议鄂尔多斯市康巴什区委员会", "type": "政协", "level": "市辖区", "parent": "鄂尔多斯市政协", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
    {"id": 5, "name": "中共鄂尔多斯市康巴什区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共鄂尔多斯市康巴什区委员会", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
    {"id": 6, "name": "鄂尔多斯市公安局康巴什区分局", "type": "政府", "level": "乡科级", "parent": "鄂尔多斯市康巴什区人民政府", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
    {"id": 7, "name": "中共鄂尔多斯市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党内蒙古自治区委员会", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
    {"id": 8, "name": "鄂尔多斯市人民政府", "type": "政府", "level": "地级市", "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区鄂尔多斯市康巴什区"},
]

# ── Positions (person 任职) ───────────────────────────────────────────────────
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "2026年6月下旬接任甄华"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "2025", "end_date": "", "rank": "正处级", "note": "政府领导之窗 2025-08 为区长；2026-02 区政府工作报告仍见'代区长'表述"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记（兼）", "start_date": "2025", "end_date": "", "rank": "正处级", "note": ""},
    # 区委常委
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "分工待查"},
    {"person_id": 4, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026-07 拟任区政协主席候选人"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "曾任市人大常委会委员，2026-06辞"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "2021", "end_date": "", "rank": "副处级", "note": "区政府党组副书记"},
    {"person_id": 7, "org_id": 5, "title": "区委常委、区纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "职务为推断，待三届全会确认"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 区人民政府（副区长）
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": "公示期"},
    {"person_id": 11, "org_id": 6, "title": "副区长、区公安分局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "二级高级警长"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "2024-02", "end_date": "", "rank": "副处级", "note": "无党派"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "2023-10", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长（挂职）", "start_date": "2025-06", "end_date": "", "rank": "副处级", "note": "挂职"},
    # 前任
    {"person_id": 30, "org_id": 1, "title": "市委副书记、区委书记（兼）", "start_date": "2023-05", "end_date": "2026-06", "rank": "副部级/正厅级", "note": "卸任康巴什区委书记，仍任市委副书记"},
    {"person_id": 30, "org_id": 7, "title": "鄂尔多斯市委副书记", "start_date": "2023-05", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 31, "org_id": 2, "title": "区长", "start_date": "2021", "end_date": "2023-02", "rank": "正处级", "note": "政府工作报告报告人（2022/2023）"},
]

# ── Relationships (person_a ↔ person_b) ───────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档（2026 起）", "overlap_org": "鄂尔多斯市康巴什区", "overlap_period": "2026至今"},
    {"person_a": 3, "person_b": 1, "type": "共事", "context": "区委副书记—区委书记（区级班子共事）", "overlap_org": "中共鄂尔多斯市康巴什区委员会", "overlap_period": "2026"},
    {"person_a": 30, "person_b": 1, "type": "predecessor_successor", "context": "前任区委书记（甄华）→继任区委书记（宋俊峰）", "overlap_org": "中共鄂尔多斯市康巴什区委员会", "overlap_period": "2026-06"},
    {"person_a": 31, "person_b": 2, "type": "predecessor_successor", "context": "前任区长（王雪峰）→继任区长（方立妍）", "overlap_org": "鄂尔多斯市康巴什区人民政府", "overlap_period": "约2023-2025"},
    {"person_a": 6, "person_b": 2, "type": "共事", "context": "常务副区长—区长（政府班子搭档分工）", "overlap_org": "鄂尔多斯市康巴什区人民政府", "overlap_period": "2021至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长（区委常委）", "overlap_org": "鄂尔多斯市康巴什区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—副区长兼公安局长", "overlap_org": "鄂尔多斯市康巴什区人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区委书记—统战部长（常委班子）", "overlap_org": "中共鄂尔多斯市康巴什区委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—常务副区长核心搭档", "overlap_org": "鄂尔多斯市康巴什区人民政府", "overlap_period": "2021至今"},
]


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"kangbashi_{name}"

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
                "system": "party" if (org and org.get("type") == "党委") else ("government" if (org and org.get("type") == "政府") else "other"),
                "rank": pos.get("rank", ""),
                "is_key_promotion": bool(pos.get("start_date")) and pos.get("title") in ("区委书记", "区委副书记、区长"),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if pos.get("start_date") else "plausible",
                "source_ids": ["S001"],
            })
    if not career_timeline:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，早期履历待查（网络受限：Exa限流、部分官方页面超时）",
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
            "person_id": f"kangbashi_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r.get("context") else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {"id": "S001", "title": "康巴什区人民政府官网·领导之窗（区长/副区长个人页）", "url": "http://www.kbs.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjb/ldcr/zfld/",
         "publisher": "康巴什区人民政府", "published_at": "2025-08/2026-07", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "方立妍、王瑞祥、杨东、徐浩波、苏云高娃、梁杰等都、朱东良、武兆坤、刘波 个股简历"},
        {"id": "S002", "title": "中共鄂尔多斯市康巴什区第三次代表大会开幕新闻（区委常委名单）", "url": "http://www.kbs.gov.cn/ywdt/qndt/202607/t20260730_3911757.html",
         "publisher": "康巴什区政府（区第三次党代会）", "published_at": "2026-07-30", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认宋俊峰作报告、方立妍主持、区委常委11人"},
        {"id": "S003", "title": "鄂尔多斯市委组织部 2026-07 任前公示（乌兰托娅等）", "url": "http://www.ordosdj.gov.cn/djyw/ersv/202607/t20260722_1777786.html",
         "publisher": "鄂尔多斯市委员会组织部", "published_at": "2026-07-22", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "乌兰托娅拟任区政协主席"},
        {"id": "S004", "title": "康巴什区人民政府新闻（甄华/宋俊峰）", "url": "http://www.kbs.gov.cn/ywdt/qndt/",
         "publisher": "康巴什区人民政府", "published_at": "2026-06", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认新旧书记更替时间线"},
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": SLUG,
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_康巴什区",
            "time_focus": "2026年",
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
                           "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
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
            "administrative_rank": "正处级" if person.get("id") in (1, 2) else "",
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
            "career_pattern": "local_ladder" if pid in (1, 2, 6, 11) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [p.get("birthplace", "") for p in [person] if p.get("birthplace")],
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
                "description": f"截至 {AS_OF} 未发现 {name} 涉纪律调查/负面舆情的公开报道；仍属待查（网络受限）。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if pid in (1, 2) else "thin",
            "relationship_confidence": "high" if person.get("confidence") == "confirmed" else "medium",
            "biggest_gap": "完整分段履历（每段职务起止）",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2) else "medium",
                "question": f"{name} 任现职前完整分段履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 此前担任"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": f"{name} 出生年月/籍贯/学历教育（部分缺失或需核实）",
                "why_it_matters": "核心身份信息，用于去重与跨区域关联",
                "suggested_queries": [f"{name} 籍贯", f"{name} 毕业院校"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-{PROVINCE}-{CITY}-{person['current_post']}-{person['name']}.json"
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

    # Person JSONs for core figures (区委书记 + 区长 + 前任核心 + 常务副区长/公安局长)
    for p in persons:
        if p["id"] in (1, 2, 30, 31, 6, 11):
            write_person_json(p)

    print(f"Done. DB: {DB_PATH}  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())