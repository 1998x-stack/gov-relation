#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 乌达区 (Wuda District),
乌海市 (Wuhai City), 内蒙古自治区.

Investigation date: 2026-08-11
Task ID: inner_mongolia_乌达区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.wuda.gov.cn — 乌达区人民政府官方网站 (primary, current as of 2026-08-11)
    * 区委领导之窗: https://www.wuda.gov.cn/c/2026-05-26/8663.shtml (刘虎书记bio, 7名区委领导)
    * 政府领导之窗: https://www.wuda.gov.cn/c/2026-06-13/187762.shtml (马恺代区长bio, 9名政府领导)
    * 第十届党代会公报: https://www.wuda.gov.cn/c/2026-07-29/192348.shtml
    * 2026-03-04 任免通知: https://www.wuda.gov.cn/c/2026-03-04/186333.shtml
  - http://www.wuhai.gov.cn/wuhai/swdwgk/ldbz70/* — 乌海市委党务公开·干部任免 (乌海党建网, 官方档案)
    * 第243次会议 (2026-06-04): 马强任乌达区委副书记等
    * 第241次会议 (2026-05-16): 刘勐任乌达区委副书记, 董旭任常委
    * 第232次会议 (2026-04-02): 贾飞任乌达区委常委
    * 第229次会议 (2026-03-04): 刘娜仁任乌达区委常委
    * 第197次会议 (2025-08-05): 延文龙任乌达高新区党工委书记, 刘虎转副书记
    * 及 2023-2024 历次常委会记录 (颜闻君/国世龙/张卫东/韩志林/何鹰/张立明等任免)
  - 百度百科—延文龙词条 (2026-08-11 访问): 前任区委书记完整履历

Confirmed current leaders (2026-08-11):
  - 区委书记: 刘虎 (男, 汉族, 1980-09生, 大学学历; 2026-05-26 干部大会宣布任区委书记, 2026-07 党代会连任)
  - 区委副书记、政府代区长/区长候选人: 马强 (男, 汉族, 1983-07生, 本科+MPA; 2026-06-04 自海南区委副书记调任)
  - 区委副书记、政法委书记: 刘勐 (男, 汉族, 1978-10生, 硕士; 2026-05-16 任)
  - 其余常委: 李春艳(纪委书记, 女, 1978-09, 2023-09 任), 刘娜仁(统战部长, 女, 蒙古族, 1977-11, 2026-03-04任常委),
    何鹰(宣传部长, 1985-04, 2024 中调入), 韩志林(常务副区长, 1983-12, 2024-07-02 调入),
    杨得超(区委办主任, 1982-04); 另 贾飞(2026-04-02任, 试用期), 董旭(2026-05-16任, 试用期, 原市委组织部副部长)

Confidence notes:
  - Current roles & 领导班子 roster: confirmed via 官方领导之窗/政府网站新闻 (2026-08-11)
  - 班子成员出生年月/民族/学历: 官方 bios (2026-05-26 领导之窗系列页, checkpoint 2026-08-06 记录)
  - 前任书记延文龙: confirmed (百度百科 + 官方任免记录), 完整履历
  - 前任区长: 即现任书记刘虎 (区长→书记 2026-05)
  - 前委员变动时间线: confirmed via 乌海市委常委会记录 (2023-09 至 2026-06)
  - 刘虎任区长起止、马强任海南区委副书记起止、延文龙卸任去向: 待查 (open questions)
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
SLUG = "乌达区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-11"
PROVINCE = "内蒙古自治区"
CITY = "乌海市"
REGION = "乌达区"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_乌达区"
if _CURRENT_DIR.name == "inner_mongolia_乌达区":
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
# IDs: 1-2 核心领导 (书记/代区长), 3-10 区委班子, 11-19 政府/人大/政协, 20-26 前任领导
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导 (现任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共乌海市乌达区委员会",
        "source": "https://www.wuda.gov.cn/c/2026-05-26/8663.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1980年9月生，大学学历，中共党员；2026-05-26 全区干部大会宣布任乌达区委书记（自治区党委决定），2026-07 乌达区第十次党代会连任区委书记；此前任乌达区委副书记、区长（至2026-05）；兼任区委党校校长、乌海乌达高新技术产业开发区党工委书记；任区长前早期履历待查",
    },
    {
        "id": 2,
        "name": "马恺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-07",
        "birthplace": "",
        "education": "大学本科，公共管理硕士（MPA）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政府代区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-06-13/187762.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1983年7月生，大学本科学历，公共管理硕士学位（MPA），中共党员；2026-06-04 市委常委会第243次会议决定任乌达区委委员、常委、副书记、乌达高新区党工委副书记，不再担任海南区委副书记、常委、委员（海南区委副书记起始时间待查）；2026-06 起任区政府党组书记、代区长/区长候选人",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 其他区委领导 (领导班子)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "刘勐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "",
        "education": "硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共乌海市乌达区委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/ldbz70/2447640/index.html",
        "confidence": "confirmed",
        "notes": "男，汉族，1978年10月生，硕士；2026-05-16 市委第213次会议任乌达区委副书记（此前职务待查），现任乌达区委副书记、政法委书记",
    },
    {
        "id": 4,
        "name": "李春艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-09",
        "birthplace": "",
        "education": "MPA",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "乌达区纪委监委",
        "source": "https://www.wuda.gov.cn/c/2026-05-26/8663.shtml",
        "confidence": "confirmed",
        "notes": "女，汉族，1978年9月生，MPA；2023-09-18 市委第102次会议任乌达区委常委、纪委书记（此前任市审计局党组成员）；已任乌达区监委主任，第十届纪委换届续任",
    },
    {
        "id": 5,
        "name": "刘娜仁",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共乌海市乌达区委员会",
        "source": "https://www.wuhai.gov.cn/wuhai/swhdwmwk/ldbz70/2418033/index.html",
        "confidence": "confirmed",
        "notes": "女，蒙古族，1977年11月生，大学学历；2026-03-04 市委第219次常委会任乌达区委常委；现任区委常委、政协党组副申记、统战部部长、区社会主义学校校长（2026-05 领导之窗）",
    },
    {
        "id": 6,
        "name": "何鹰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共乌海市乌达区委员会",
        "source": "https://www.wuda.gov.cn/c/2026-05-26/8663.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1985年4月生，大学学历；2024年屆由市委编办副主任调任乌达区委常委；现任宣传部部长",
    },
    {
        "id": 7,
        "name": "韩志林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-12",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政府党组副书记、副区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-05-26/8663.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1983年12月生，研究生；2024-07-02 市委第会议任乌达区委常委（原市财政局党组成员）；现任区委常委、政府党组副书记、常务副区长、区红十字会会长（2026-06 领导之窗）",
    },
    {
        "id": 8,
        "name": "杨得超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、办公室主任",
        "current_org": "中共乌海市乌达区委员会",
        "source": "https://www.wuda.gov.cn/c/2026-05-26/8663.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1982年4月生，大学学历；现任乌达区委常委、区委办公室主任",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政府 副区长 (非常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "张晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-06-13/187762.shtml",
        "confidence": "confirmed",
        "notes": "乌达区人民政府党组成员、副区长（官方领导之窗 2026-06-13；此前任市工信局党组成员，2026-03-04 卸任，同年入乌达）",
    },
    {
        "id": 12,
        "name": "田杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-06-13/187762.shtml",
        "confidence": "confirmed",
        "notes": "乌达区人民政府副区长（官方领导名单）",
    },
    {
        "id": 13,
        "name": "冯智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-06-13/187762.shtml",
        "confidence": "confirmed",
        "notes": "乌达区人民政府党组成员、副区长",
    },
    {
        "id": 14,
        "name": "胡天文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuhai.gov.cn/wuhai/swdw/ldbz70/2337838/index.html",
        "confidence": "confirmed",
        "notes": "乌达区人民政府党组成员、副区长；2025-08-05 市委常委会第197次会议任乌海乌达高新区党工委副书记（兼任）",
    },
    {
        "id": 15,
        "name": "郑源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-06-13/187762.shtml",
        "confidence": "confirmed",
        "notes": "乌达区人民政府党组成员、副区长",
    },
    {
        "id": 16,
        "name": "周春来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-06-13/187762.shtml",
        "confidence": "confirmed",
        "notes": "乌达区人民政府党组成员、副区长",
    },
    {
        "id": 17,
        "name": "刘春生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长人选",
        "current_org": "乌达区人民政府",
        "source": "https://www.wuda.gov.cn/c/2026-06-13/187762.shtml",
        "confidence": "confirmed",
        "notes": "乌达区人民政府党组成员、副区长人选（2026-06 名单）",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大 / 政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "name": "郝利平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "乌达区人大常委会",
        "source": "https://www.wuda.gov.cn/search/wd (郝利平 bio, 2024-08-13)",
        "confidence": "confirmed",
        "notes": "男，汉族，1970年9月生，大学学历；现任乌达区人大常委会党组书记、主任；2023-12 前曾任乌达区委常委（2023-12 不再担任）",
    },
    {
        "id": 19,
        "name": "高铁男",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-04",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协党组副书记、主席",
        "current_org": "政协乌达区委员会",
        "source": "https://www.wuda.gov.cn/search/wd (高铁男 bio 2024-08-13)",
        "confidence": "confirmed",
        "notes": "男，汉族，1968年4月生，研究生学历；现任乌达区政协党组副书记、主席，主持区政协日常履职工作",
    },
    {
        "id": 20,
        "name": "薛峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协党组书记、主席候选人",
        "current_org": "乌达区政协",
        "source": "https://www.wuda.gov.cn/c/2026-05-27? (薛峰 bio 2026-05-27)",
        "confidence": "confirmed",
        "notes": "男，汉族，1972年5月生，大学本科；现任乌达区政协党组书记、主席候选人；此前历任：市审计局党组书记（至2023-11）、市人社局党组书记（2023-11 ~ 2026-04-02 免）",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "延文龙",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1978",
        "birthplace": "内蒙古喀喇沁旗",
        "education": "公共管理硕士",
        "party_join": "中共党员",
        "work_start": "2002-07",
        "current_post": "前任区委书记",
        "current_org": "中共乌海市乌达区委员会（前任）",
        "source": "https://baike.baidu.com/item/延文龙",
        "confidence": "confirmed",
        "notes": "男，蒙古族，1978年生，内蒙喀喇沁旗人；2002-07 参加工作，2006-05 入党；2021-06-15 干部大会宣布任乌达区委书记，2026-05 卸任（2026-06-04 免职）；完整履历见百度百科；自治区第十四届人大代表；卸任后去向待查",
    },
    {
        "id": 22,
        "name": "国世龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委副书记",
        "current_org": "中共乌海市乌达区委员会（前任）",
        "source": "https://www.wuhai.gov.cn/wuhai/swdwg/ldbz70/1823272/index.html",
        "confidence": "plausible",
        "notes": "2024-02-03 由海勃湾区委常委调任乌达区委副书记；2025-04 仍以区领导身份参加政法工作调研；2026 不在现任班子之列，离任时间与去向待查",
    },
    {
        "id": 23,
        "name": "张卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委常委",
        "current_org": "中共乌海市乌达区委员会（前任）",
        "source": "https://www.wuhai.gov.cn/ggj/swdwgk/ldbz70/1823272/index.html",
        "confidence": "confirmed",
        "notes": "2024-02-03 由市纪委监委组织部部长调任乌达区委常委；2026-05-16 不再担任乌达区委常委、委员（去向待查）",
    },
    {
        "id": 24,
        "name": "颜闻君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委副书记",
        "current_org": "乌海市人民检察院（现任）",
        "source": "https://www.wuhai.gov.cn/wuhai/swdgk/ldbz70/1556137/index.html",
        "confidence": "confirmed",
        "notes": "原乌达区纪委书记；2023-09-18 任乌达区委副书记；2024-02-03 转任市人民检察院党组副书记",
    },
    {
        "id": 25,
        "name": "贾飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（2026-04-02 任，试用期一年）",
        "current_org": "中共乌海市乌达区委员会",
        "source": "https://www.wuhai.gov.cn/wuhai/swdwgk/ldbz70/2424255/index.html",
        "confidence": "confirmed",
        "notes": "2026-04-02 市委第232次会议任乌达区委委员、常委（试用期一年）；2024-09-11 不再担任海南区委常委；中间岗位待查",
    },
    {
        "id": 26,
        "name": "董旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（2026-05-16 任，试用期一年）",
        "current_org": "中共乌海市乌达区委员会",
        "source": "https://www.wuhai.gov.cn/wuhai/swdwgk/ldgsz70/2447640/index.html",
        "confidence": "confirmed",
        "notes": "2026-05-16 市委第241次会议任乌达区委委员、常委（试用期一年）；此前曾任市委组织部副部长、市公务员局局长（2024-06 免任）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共乌海市乌达区委员会", "type": "党委", "level": "市辖区", "parent": "中共乌海市委员会", "location": "内蒙古乌海市乌达区"},
    {"id": 2, "name": "乌达区人民政府", "type": "政府", "level": "市辖区", "parent": "乌海市人民政府", "location": "内蒙古乌海市乌达区"},
    {"id": 3, "name": "中共乌达区纪律检查委员会（区监委）", "type": "党委", "level": "市辖区", "parent": "乌海市纪委监委", "location": "内蒙古乌海市乌达区"},
    {"id": 4, "name": "乌达区人大常委会", "type": "人大", "level": "市辖区", "parent": "乌海市人大常委会", "location": "内蒙古乌海市乌达区"},
    {"id": 5, "name": "中国人民政治协商会议乌达区委员会", "type": "政协", "level": "市辖区", "parent": "乌海市政协", "location": "内蒙古乌海市乌达区"},
    {"id": 6, "name": "乌海乌达高新技术产业开发区管委会", "type": "开发区", "level": "市辖区", "parent": "乌海市人民政府", "location": "内蒙古乌海市乌达区"},
    {"id": 7, "name": "中共乌达区委员会党校（行政学校）", "type": "事业单位", "level": "市辖区", "parent": "中共乌海市乌达区委员会", "location": "内蒙古乌海市乌达区"},
    {"id": 8, "name": "中共乌海市海南区委员会", "type": "党委", "level": "市辖区", "parent": "中共乌海市委员会", "location": "内蒙古乌海市海南区"},
    {"id": 9, "name": "海南区人民政府", "type": "政府", "level": "市辖区", "parent": "乌海市人民政府", "location": "内蒙古乌海市海南区"},
    {"id": 10, "name": "中共乌海市海勃湾区委员会", "type": "党委", "level": "市辖区", "parent": "中共乌海市委员会", "location": "内蒙古乌海市海勃湾区"},
    {"id": 11, "name": "乌海市财政局", "type": "政府", "level": "地级市", "parent": "乌海市人民政府", "location": "乌海市"},
    {"id": 12, "name": "乌海市审计局", "type": "政府", "level": "地级市", "parent": "乌海市人民政府", "location": "乌海市"},
    {"id": 13, "name": "中共乌海市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共乌海市委员会", "location": "乌海市"},
    {"id": 14, "name": "中共乌海市委机构编制委员会办公室", "type": "党委", "level": "地级市", "parent": "中共乌海市委员会", "location": "乌海市"},
    {"id": 15, "name": "中共乌海市委组织部", "type": "党委", "level": "地级市", "parent": "中共乌海市委员会", "location": "乌海市"},
    {"id": 16, "name": "乌海市人民检察院", "type": "政法", "level": "地级市", "parent": "内蒙古自治区人民检察院", "location": "乌海市"},
    {"id": 17, "name": "乌海市人力资源和社会保障局", "type": "政府", "level": "地级市", "parent": "乌海市人民政府", "location": "乌海市"},
    {"id": 18, "name": "乌海市海南区水务局", "type": "政府", "level": "市辖区", "parent": "海南区人民政府", "location": "内蒙古乌海市海南区"},
    {"id": 19, "name": "中共乌海市委办公厅（市委办公室）", "type": "党委", "level": "地级市", "parent": "中共乌海市委员会", "location": "乌海市"},
    {"id": 20, "name": "乌海市水务开发集团有限责任公司", "type": "国企", "level": "地级市", "parent": "乌海市人民政府", "location": "乌海市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘虎
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026-05-26", "end": "", "rank": "县处级", "note": "2026-05-26 全区干部大会宣布（自治区党委决定）；2026-07 第十次党代会连任区委书记"},
    {"person_id": 1, "org_id": 7, "title": "区委党校（行政学校）校长", "start": "2026-05", "end": "", "rank": "县处级", "note": "兼任"},
    {"person_id": 1, "org_id": 6, "title": "高新区党工委书记", "start": "2026-06-04", "end": "", "rank": "县处级", "note": "2026-06-04 市委常委会第243次会议决定"},
    {"person_id": 1, "org_id": 6, "title": "高新区党工委书记", "start": "2024-07", "end": "2025-08", "rank": "县处级", "note": "2024-07 任；2025-08-05 调整为党工委副书记"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "2024? ", "end": "2026-05", "rank": "县处级", "note": "最迟2024-06 在任（官方要闻）；2025-12-11 仍任；2026-05 任书记后离任；确切任职起始待查"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start": "2024?", "end": "2026-05", "rank": "副处级", "note": "任区长期间兼区委副书记"},
    # 马恺
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2026-06-04", "end": "", "rank": "副处级", "note": "2026-06-04 市委第243次会议决定"},
    {"person_id": 2, "org_id": 2, "title": "政府代区长（区长候选人）", "start": "2026-06", "end": "", "rank": "县处级", "note": "2026-06-13 领导之窗列为区长候选人；2026-07 以代区长名义活动"},
    {"person_id": 2, "org_id": 6, "title": "高新区党工委副书记", "start": "2026-06-04", "end": "", "rank": "县处级", "note": "2026-06-04 市委第243次会议决定"},
    {"person_id": 2, "org_id": 8, "title": "区委副书记", "start": "2024?", "end": "2026-06", "rank": "副处级", "note": "2026-06-04 免去海南区委副书记职务；任职起始待查"},
    # 刘勐
    {"person_id": 3, "org_id": 1, "title": "区委副书记、政法委书记", "start": "2026-05-16", "end": "", "rank": "副处级", "note": "2026-05-16 市委第213次会议任区委副书记"},
    # 李春艳
    {"person_id": 4, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start": "2023-09-18", "end": "", "rank": "副处级", "note": "2023-09-18 市委第102次会议决定；区监委主任"},
    # 刘娜仁
    {"person_id": 5, "org_id": 1, "title": "区委常委、统战部部长、政协党组副书记", "start": "2026-03-04", "end": "", "rank": "副处级", "note": "2026-03-04 市委第229次会议任区委常委"},
    # 何鹰
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长", "start": "2024-09", "end": "", "rank": "副处级", "note": "2024年由市委编办副主任调任"},
    # 韩志林
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "2024-07-02", "end": "", "rank": "副处级", "note": "2024-07-02 市委常委会决定"},
    {"person_id": 7, "org_id": 2, "title": "常务副区长（政府党组副书记）", "start": "2024-07", "end": "", "rank": "县处级", "note": "2024-07-02 自市财政局党组成员调入；2026-06 名单仍为区委常委、政府党组副书记、副区长"},
    # 杨得超
    {"person_id": 8, "org_id": 1, "title": "区委常委、办公室主任", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # 副区长们
    {"person_id": 11, "org_id": 2, "title": "政府党组成员、副区长", "start": "2026-03", "end": "", "rank": "县处级", "note": "2026-06-13 官方名单；此前 2026-03-04 免市工信局党组成员"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "县处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "政府党组成员、副区长", "start": "", "end": "", "rank": "县处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "政府党组成员、副区长", "start": "", "end": "", "rank": "县处级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "高新区党工委副书记", "start": "2025-08-05", "end": "", "rank": "县处级", "note": "兼任"},
    {"person_id": 15, "org_id": 2, "title": "政府党组成员、副区长", "start": "", "end": "", "rank": "县处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "政府党组成员、副区长", "start": "", "end": "", "rank": "县处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "政府党组成员、副区长人选", "start": "2026-06", "end": "", "rank": "县处级", "note": ""},
    # 人大 / 政协
    {"person_id": 18, "org_id": 4, "title": "区人大常委会党组书记、主任", "start": "2023-12", "end": "", "rank": "县处级", "note": "2023-12 不再任区委常委后转人大"},
    {"person_id": 18, "org_id": 1, "title": "区委常委", "start": "", "end": "2023-12", "rank": "副处级", "note": "2023-12-11 卸任常委"},
    {"person_id": 19, "org_id": 5, "title": "区政协党组副书记、主席", "start": "", "end": "", "rank": "县处级", "note": "主持日常履职"},
    {"person_id": 20, "org_id": 5, "title": "区政协党组书记、主席候选人", "start": "2026-04", "end": "", "rank": "县处级", "note": "2026-04-02 免市人社局党组书记后转任"},
    {"person_id": 20, "org_id": 17, "title": "市人社局党组书记", "start": "2023-11", "end": "2026-04", "rank": "县处级", "note": "2023-11-08 任（自市审计局党组书记）"},
    # 前任书记 延文龙（完整履历）
    {"person_id": 21, "org_id": 1, "title": "区委书记", "start": "2021-06-15", "end": "2026-05", "rank": "县处级", "note": "2021-06-15 干部大会宣布任；2026-06-04 免职"},
    {"person_id": 21, "org_id": 6, "title": "高新区党工委书记", "start": "2025-08-05", "end": "2026-06-04", "rank": "县处级", "note": "2025-08-05 市委第197次会议任；2026-06-04 免"},
    {"person_id": 21, "org_id": 2, "title": "区长", "start": "2021-03", "end": "2021-06", "rank": "县处级", "note": "2020-07 起代区长，2021-03 转正"},
    {"person_id": 21, "org_id": 2, "title": "常务副区长", "start": "2018-11", "end": "2020-07", "rank": "县处级", "note": "区委常委、政府党组副书记、副区长"},
    {"person_id": 21, "org_id": 1, "title": "区委常委（宣传部长/副区长）", "start": "2013-08", "end": "2018-11", "rank": "副处级", "note": "2013-08 起常委、宣传部长；2016-08 起常委、副区长"},
    {"person_id": 21, "org_id": 20, "title": "乌海市水务开发集团副总经理/党委书记", "start": "2010-08", "end": "2013-08", "rank": "国企", "note": "集团副总经理兼污水处理厂董事长；2011-09 起党委书记、纪委书记、常务副总经理"},
    {"person_id": 21, "org_id": 19, "title": "市委办公厅秘书", "start": "2006-05", "end": "2010-08", "rank": "乡科级", "note": "2010.02-2010.05 挂职华水务集团公司总助"},
    {"person_id": 21, "org_id": 9, "title": "海南区政府办公室秘书", "start": "2004-11", "end": "2006-05", "rank": "乡科级", "note": ""},
    {"person_id": 21, "org_id": 18, "title": "海南区水务局干部", "start": "2002-07", "end": "2004-11", "rank": "乡科级", "note": ""},
    # 前任
    {"person_id": 22, "org_id": 1, "title": "区委副书记", "start": "2024-02-03", "end": "2025/2026", "rank": "副处级", "note": "2024-02-03 由海勃湾区委常委调任；2025-04 仍在任；2026 卸任，去向待查"},
    {"person_id": 23, "org_id": 1, "title": "区委常委", "start": "2024-02-03", "end": "2026-05-16", "rank": "副处级", "note": "2024-02 自市纪委组织部部长调任；2026-05-16 免职"},
    {"person_id": 24, "org_id": 1, "title": "区委副书记", "start": "2023-09-18", "end": "2024-02", "rank": "副处级", "note": "2023-09-18 由区纪委书记转副书记"},
    {"person_id": 24, "org_id": 3, "title": "区纪委书记", "start": "", "end": "2023-09-18", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 16, "title": "市人民检察院党组副书记", "start": "2024-02-03", "end": "", "rank": "县处级", "note": "转任"},
    {"person_id": 25, "org_id": 1, "title": "区委常委", "start": "2026-04-02", "end": "", "rank": "副处级", "note": "试用期一年"},
    {"person_id": 25, "org_id": 8, "title": "海南区委常委", "start": "", "end": "2024-09-11", "rank": "副处级", "note": "2024-09-11 免任"},
    {"person_id": 26, "org_id": 1, "title": "区委常委", "start": "2026-05-16", "end": "", "rank": "副处级", "note": "试用期一年"},
    {"person_id": 26, "org_id": 15, "title": "市委组织部副部长、市公务员局局长", "start": "", "end": "2024-06", "rank": "县处级", "note": "2024-06-05 免任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—代区长（党政搭档）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2026-06-"},
    # 前任接续
    {"person_a": 21, "person_b": 1, "type": "交接", "context": "前任区委书记→现任区委书记（2026-05 交接）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2026-05"},
    {"person_a": 1, "person_b": 2, "type": "交接", "context": "前任区长（刘虎）→代区长（马恺）；并共同构成新任书记-区长班子", "overlap_org": "乌达区人民政府", "overlap_period": "2026-06"},
    {"person_a": 21, "person_b": 1, "type": "交接", "context": "高新区党工委书记 2024-07 刘虎 ↔ 2025-08 延文龙 ↔ 2026-06 刘虎 轮换", "overlap_org": "乌海乌达高新技术产业开发区管委会", "overlap_period": "2024-2026"},
    # 书记—常委
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记（政法委）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2026-05-"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共乌达区纪律检查委员会", "overlap_period": "2026-05-"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2026-05-"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—宣传部长（老搭档，何鹰 2024 调入）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记（前任区长）—常务副区长（2024-07-2026-05 政府班子直接上下级）", "overlap_org": "乌达区人民政府", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—办公室主任", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2026-05-"},
    # 代区长—政府
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "代区长—常务副区长", "overlap_org": "乌达区人民政府", "overlap_period": "2026-06-"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "代区长—副区长", "overlap_org": "乌达区人民政府", "overlap_period": "2026-06-"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "代区长—副区长", "overlap_org": "乌达区人民政府", "overlap_period": "2026-06-"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "代区长—副区长（同兼高新区党工委副书记）", "overlap_org": "乌海乌达高新技术产业开发区管委会", "overlap_period": "2026-06-"},
    # 前任书记 延文龙 ↔ 班子
    {"person_a": 21, "person_b": 7, "type": "共事", "context": "前任书记—常务副区长（2024-07 至 2026-05）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2024-2026"},
    {"person_a": 21, "person_b": 18, "type": "共事", "context": "前任书记—曾任常委（郝利平 2023-12 离任常委转人大）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2021-2023"},
    {"person_a": 21, "person_b": 24, "type": "共事", "context": "前任书记—前任副书记（颜闻君 2023-2024）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2023-2024"},
    {"person_a": 21, "person_b": 22, "type": "共事", "context": "前任书记—前任副书记（国世龙 2024-2025）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2024-2025"},
    {"person_a": 21, "person_b": 23, "type": "共事", "context": "前任书记—前任常委（张卫东 2024-2026-05）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2024-2026"},
    {"person_a": 21, "person_b": 4, "type": "共事", "context": "前任书记—纪委书记（李春艳 2023-09 起）", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2023-2026"},
    {"person_a": 21, "person_b": 6, "type": "共事", "context": "前任书记—宣传部长", "overlap_org": "中共乌海市乌达区委员会", "overlap_period": "2024-2026"},
    # 马恺 与 海南区 前任同事（跨区）
    {"person_a": 2, "person_b": 25, "type": "共事", "context": "马恺（海南区副书记）与 贾飞（海南区委常委至2024-09）曾同区", "overlap_org": "中共乌海市海南区委员会", "overlap_period": "2024"},
    {"person_a": 21, "person_b": 25, "type": "交接", "context": "海南区 与 乌达区 班子人员互换（贾飞 2026-04 调入乌达）", "overlap_org": "中共乌海市海南区委员会", "overlap_period": "2024-2026"},
    # 市直-区 调入线（组建班子轨迹）
    {"person_a": 7, "person_b": 11, "type": "共事", "context": "常务副区长—副区长（张晓明 2026-03 自市工信局）", "overlap_org": "乌达区人民政府", "overlap_period": "2026-"},
    {"person_a": 7, "person_b": 12, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "乌达区人民政府", "overlap_period": "2026-"},
    {"person_a": 7, "person_b": 14, "type": "共事", "context": "常务副区长—副区长（胡天文 兼任高新区党工委副书记）", "overlap_org": "乌达区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "代区长—办公室主任（杨得超）", "overlap_org": "乌达区人民政府", "overlap_period": "2026-06-"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════════
def slugify_name(name: str) -> str:
    return name.replace(" ", "")


CORE_IDS = {1, 2}  # 核心领导 (书记、代区长)


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"wuhai_wuda_{name}"
    post_label = person.get("current_post", "")

    # 文件名: YYYYMMDD-内蒙古自治区-乌海市-{job}-{name}.json
    fname = f"{TODAY}-{PROVINCE}-{CITY}-{post_label}-{name}.json"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            career_timeline.append({
                "start": pos.get("start", ""),
                "end": pos.get("end", ""),
                "org": org["name"] if org else "",
                "title": pos.get("title", ""),
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if (org and org["type"] == "党委") else ("government" if (org and (org["type"] in {"政府", "人大", "政协"})) else "other"),
                "rank": pos.get("rank", ""),
                "is_key_promotion": pos.get("title") in ("区委书记", "政府代区长（区长候选人）", "区长"),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
                "source_ids": ["S002"],
            })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"wuhai_wuda_{other_name}",
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
        {"id": "S001", "title": "乌达区人民政府—领导之窗",
         "url": "https://www.wuda.gov.cn/c/2026-05-26/8663.shtml",
         "publisher": "乌达区人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "官网访问，确认现任领导职务、出生年月、民族、学历"},
        {"id": "S002", "title": "个人领导简介页",
         "url": source_url, "publisher": "乌达区人民政府/乌海市党务公开", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "个人简介/任职档案确认信息"},
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": REGION,
            "job": post_label,
            "task_id": "inner_mongolia_乌达区",
            "time_focus": "2024-2026年",
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
            "administrative_rank": "县处级" if pid in (1, 2, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S002"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]}
                          for o in organizations
                          if o["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == pid}],
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
                "description": "搜索范围为官方领导页与公开新闻，未发现针对所记人物的纪律或舆情风险信号（截至2026-08-11）。",
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
            "biggest_gap": "任现职前完整履历与前任去向待查" if pid in (1, 2, 21) else "",
        },
        "open_questions": [
            {
                "priority": "critical" if pid == 1 else "high",
                "question": "刘虎任乌达区长/代区长的确切起始时间及此前履历（2024 前在何单位任处级）",
                "why_it_matters": "书记完整晋升链条是全区网络核心",
                "suggested_queries": ["刘虎 任 乌达区区长", "刘虎 任前公示 乌海", "刘虎 简历 乌达"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high" if pid == 2 else "medium",
                "question": "马恺任海南区委副书记的起始时间与来源（此前单位/职务）",
                "why_it_matters": "跨区流动链条核心节点",
                "suggested_queries": ["马恺 海南区 副书记", "马恺 乌海 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "延文龙卸任区委书记后的去向（2026-06 免职后新职务）",
                "why_it_matters": "乌海市职平台人物流向",
                "suggested_queries": ["延文龙 卸任 去向 2026", "延文龙 乌海 新职务"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": f"{name} 出生地/籍贯与毕业院校"
                if person.get("birthplace") in ("", None) else f"{name} 履历细节补全",
                "why_it_matters": "身份信息完善",
                "suggested_queries": [f"{name} 籍贯", f"{name} 毕业院校 乌海"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


def person_label(person: dict) -> str:
    label = person.get("current_post", "")
    return label


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
    for p in persons:
        if p["id"] in CORE_IDS:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())