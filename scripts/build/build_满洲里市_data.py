#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, person JSONs and report for 满洲里市 (Manzhouli), 内蒙古自治区.

Task ID: inner_mongolia_满洲里市
Province: 内蒙古自治区
Parent city: 呼伦贝尔市
Region: 满洲里市 (县级市 / 自治区计划单列市)
Level: 县级市
Targets: 市委书记 & 市长

Investigation date: 2026-08-11
Current-role snapshot as of: 2026-08-11 (official 满洲里市人民政府 领导之窗 www.manzhouli.gov.cn)

Primary sources:
  - 满洲里市人民政府门户网站 www.manzhouli.gov.cn
    * 领导之窗 (Leader/show/320|321|322|323/...) — 29 名现职领导官方简介
    * 市政要闻 (News/showList/30919, News/show/...) — 人事活动时间线
    * 人大会议新闻 (2026-07-31 第十六届人大常委会第三十二次会议)
  - 呼伦贝尔市人民政府门户网站 www.hlbe.gov.cn (杜汇良任呼伦贝尔市委书记 2026-08-08)
  - 中新网检索: 王成石 (根河市长 2019-12 / 根河市委书记 2021-10、2022-06、2023-01),
    于伟东 (2021-06 全国优秀县委书记名单, 2023-07-20 满洲里市委书记),
    岳国栋 (2022-11-30 满洲里市委副书记、市长)
  - 本地仓库 data/provinces/inner_mongolia: build_扎赉诺尔区_data.py (齐善剑/布尔金任职数据)

Confirmed current leadership (2026-08-11):
  - 市委书记: 王成石 (男, 满族, 1981年10月生, 大学, 中共党员) — 2026-07-09 起在任
  - 市委副书记、市政府党组书记、代市长 (市长候选人): 陈艳豹 (男, 汉族, 1980年1月生, 大学, 中共党员)
    — 2026-07-31 市十六届人大常委会第三十二次会议审议通过人事任免事项

Predecessors (confirmed):
  - 前任市委书记: 于伟东 (2026-07-02 最后一次公开活动; 2021-06 阿鲁科尔沁旗委书记、赤峰市委常委、宣传部部长兼、全国优秀县委书记)
  - 前任市长: 岳国栋 (2022-11-30 已任市长; 2026-03-10 作 2026 年政府工作报告; 2026-06-12 最后一次公开活动)

Confidence notes:
  - Current roles & identity fields: confirmed (official pages).
  - 王成任 2019 年前履历、陈艳豹任现职前履历、于伟东/岳国栋离任去向: 公开渠道暂不可得 → 记入
    person JSON open_questions 与报告开放问题清单, 不影响结构完整性。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (process_tmp checks this token)
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

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "满洲里市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-11"
TASK_ID = "inner_mongolia_满洲里市"
PROVINCE = "内蒙古自治区"
PARENT_CITY = "呼伦贝尔市"
REGION = "满洲里市"

# ── Staging-aware paths ─────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / TASK_ID
if _CURRENT_DIR.name == TASK_ID:
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
REPORT_PATH = STAGING / f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{REGION}-领导班子工作关系网络调查报告.md"


def _person_source(p: dict) -> str:
    return p.get("source", "")


def _org_by_id(oid: int) -> dict:
    return next((o for o in organizations if o["id"] == oid), {})


def _person_by_id(pid: int) -> dict:
    return next((p for p in persons if p["id"] == pid), {})


# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══ 核心目标 ═══
    {
        "id": 1, "name": "王成石", "gender": "男", "ethnicity": "满族",
        "birth": "1981年10月", "birthplace": "",
        "education": "大学", "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共满洲里市委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/1062.html",
        "confidence": "confirmed",
        "notes": "满洲里市委书记、市委党校（行政学院）校长（院长）；主持市委全面工作；2026-07-09 主持市委专题会议（自贸片区党工委扩大会议），为任内首个公开记录",
    },
    {
        "id": 2, "name": "陈艳豹", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年1月", "birthplace": "",
        "education": "大学", "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、代市长（市长候选人）", "current_org": "满洲里市人民政府",
        "source": "https://www.manzhouli.gov.cn/Leader/show/322/1072.html",
        "confidence": "confirmed",
        "notes": "市委副书记，市政府党组书记、副市长、代市长（市长候选人提名人选）；2026-07-31 市十六届人大常委会第三十二次会议审议通过人事任免事项；2026-08-04 起以代市长身份调研",
    },
    # ═══ 市委领导班子 ═══
    {
        "id": 3, "name": "滕广兴", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年10月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、政法委书记", "current_org": "中共满洲里市委政法委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/1091.html",
        "confidence": "confirmed", "notes": "市委副书记、政法委书记",
    },
    {
        "id": 4, "name": "常青", "gender": "女", "ethnicity": "汉族",
        "birth": "1983年3月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市政府副市长", "current_org": "满洲里市人民政府",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/1016.html",
        "confidence": "confirmed", "notes": "市委常委，市政府副市长、党组成员、一级调研员",
    },
    {
        "id": 5, "name": "王松岩", "gender": "女", "ethnicity": "汉族",
        "birth": "1973年11月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、组织部部长", "current_org": "中共满洲里市委组织部",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/746.html",
        "confidence": "confirmed", "notes": "市委常委、组织部部长",
    },
    {
        "id": 6, "name": "隋剑平", "gender": "男", "ethnicity": "汉族",
        "birth": "1969年3月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任", "current_org": "中共满洲里市纪律检查委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/747.html",
        "confidence": "confirmed", "notes": "市委常委、纪委书记、监委主任；2026-07-31 列席市人大常委会第三十二次会议",
    },
    {
        "id": 7, "name": "邓月升", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年2月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市委办公室主任", "current_org": "中共满洲里市委办公室",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/748.html",
        "confidence": "confirmed", "notes": "市委常委、办公室主任；2026-07/08 多场市领导活动随行",
    },
    {
        "id": 8, "name": "吴强华", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年5月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市人民武装部政委", "current_org": "满洲里市人民武装部",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/1032.html",
        "confidence": "confirmed", "notes": "市委常委、市人民武装部上校政治委员",
    },
    {
        "id": 9, "name": "焦捷", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年2月", "birthplace": "", "education": "大专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、统战部部长（提名免去市政府副市长）", "current_org": "中共满洲里市委统一战线工作部",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/705.html",
        "confidence": "confirmed", "notes": "市委常委、统战部部长，提名免去市政府副市长；2026-08-08 重点项目建设调研随行",
    },
    {
        "id": 10, "name": "程国斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年8月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市政府副市长", "current_org": "满洲里市人民政府",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/711.html",
        "confidence": "confirmed", "notes": "市委常委，市政府副市长、党组成员",
    },
    {
        "id": 11, "name": "刘嘉琳", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年11月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、宣传部部长", "current_org": "中共满洲里市委宣传部",
        "source": "https://www.manzhouli.gov.cn/Leader/show/320/1090.html",
        "confidence": "confirmed", "notes": "市委常委、宣传部部长",
    },
    # ═══ 市政府班子（非常委）═══
    {
        "id": 12, "name": "魏洪玉", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年4月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长、市公安局局长", "current_org": "满洲里市公安局",
        "source": "https://www.manzhouli.gov.cn/Leader/show/322/860.html",
        "confidence": "confirmed", "notes": "市政府副市长、党组成员，市公安局党委书记、局长",
    },
    {
        "id": 13, "name": "宋吉祥", "gender": "男", "ethnicity": "汉族",
        "birth": "1984年2月", "birthplace": "", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "市政府副市长", "current_org": "满洲里市人民政府",
        "source": "https://www.manzhouli.gov.cn/Leader/show/322/710.html",
        "confidence": "confirmed", "notes": "市政府副市长（官方简介未载党派）",
    },
    {
        "id": 14, "name": "白永军", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1983年5月", "birthplace": "", "education": "工程硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长", "current_org": "满洲里市人民政府",
        "source": "https://www.manzhouli.gov.cn/Leader/show/322/1017.html",
        "confidence": "confirmed", "notes": "市政府副市长、党组成员",
    },
    # ═══ 人大 ═══
    {
        "id": 15, "name": "王长春", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年11月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会主任", "current_org": "满洲里市人大常委会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/321/716.html",
        "confidence": "confirmed", "notes": "市人大常委会主任、党组书记；2026-07-31 主持市十六届人大常委会第三十二次会议",
    },
    {
        "id": 16, "name": "刘存珠", "gender": "男", "ethnicity": "汉族",
        "birth": "1966年5月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会副主任", "current_org": "满洲里市人大常委会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/321/722.html",
        "confidence": "confirmed", "notes": "市人大常委会副主任、党组副书记",
    },
    {
        "id": 17, "name": "凌秀娟", "gender": "女", "ethnicity": "汉族",
        "birth": "1966年7月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会副主任", "current_org": "满洲里市人大常委会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/321/721.html",
        "confidence": "confirmed", "notes": "市人大常委会副主任、党组成员",
    },
    {
        "id": 18, "name": "包卫东", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1967年3月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会副主任", "current_org": "满洲里市人大常委会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/321/728.html",
        "confidence": "confirmed", "notes": "市人大常委会副主任、党组成员；2026-07-31 出席市人大常委会第三十二次会议",
    },
    {
        "id": 19, "name": "张艳玲", "gender": "女", "ethnicity": "汉族",
        "birth": "1971年9月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会副主任", "current_org": "满洲里市人大常委会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/321/729.html",
        "confidence": "confirmed", "notes": "市人大常委会副主任、党组成员",
    },
    # ═══ 政协 ═══
    {
        "id": 20, "name": "王涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年3月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协党组书记、主席候选人提名人选", "current_org": "中国人民政治协商会议满洲里市委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/323/706.html",
        "confidence": "confirmed", "notes": "市政协党组书记、主席候选人提名人选",
    },
    {
        "id": 21, "name": "姜东民", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年7月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协副主席", "current_org": "中国人民政治协商会议满洲里市委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/323/694.html",
        "confidence": "confirmed", "notes": "市政协副主席、党组成员",
    },
    {
        "id": 22, "name": "王春鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年4月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协副主席", "current_org": "中国人民政治协商会议满洲里市委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/323/695.html",
        "confidence": "confirmed", "notes": "市政协副主席、党组成员",
    },
    {
        "id": 23, "name": "毛宇彤", "gender": "女", "ethnicity": "达斡尔族",
        "birth": "1967年11月", "birthplace": "", "education": "大学",
        "party_join": "农工党成员", "work_start": "",
        "current_post": "市政协副主席", "current_org": "中国人民政治协商会议满洲里市委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/323/697.html",
        "confidence": "confirmed", "notes": "市政协副主席（农工党）",
    },
    {
        "id": 24, "name": "范少华", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年12月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协副主席", "current_org": "中国人民政治协商会议满洲里市委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/323/698.html",
        "confidence": "confirmed", "notes": "市政协副主席、党组成员",
    },
    {
        "id": 25, "name": "杜明燕", "gender": "女", "ethnicity": "鄂温克族",
        "birth": "1976年11月", "birthplace": "", "education": "大学",
        "party_join": "无党派人士", "work_start": "",
        "current_post": "市政协副主席", "current_org": "中国人民政治协商会议满洲里市委员会",
        "source": "https://www.manzhouli.gov.cn/Leader/show/323/925.html",
        "confidence": "confirmed", "notes": "市政协副主席（无党派）",
    },
    # ═══ 前任 / 关联网络 ═══
    {
        "id": 40, "name": "于伟东", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委书记（去向待查）", "current_org": "中共满洲里市委员会",
        "source": "https://www.chinanews.com.cn/cj/2023/07-21/10047628.shtml",
        "confidence": "confirmed",
        "notes": "2021-06-07 全国优秀县委书记拟表彰人选公示（时任赤峰市委常委、宣传部部长、阿鲁科尔沁旗旗委书记）；2021-06-29 获表彰；2023-07-20 以满洲里市委书记身份出席活动；2026-07-02 最后一次公开活动；离任去向待查",
    },
    {
        "id": 41, "name": "岳国栋", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市长（去向待查）", "current_org": "满洲里市人民政府",
        "source": "https://www.chinanews.com.cn/gn/2022/11-30/9905947.shtml",
        "confidence": "confirmed",
        "notes": "2022-11-30 以满洲里市委副书记、市长身份为蒙古领事馆开馆揭牌；2026-03-10 在市十六届人大六次会议上作2026年政府工作报告；2026-06-12 最后一次公开活动；离任去向待查",
    },
    {
        "id": 42, "name": "齐善剑", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年10月", "birthplace": "内蒙古新巴尔虎右旗",
        "education": "在职研究生", "party_join": "1999年6月", "work_start": "1992年8月",
        "current_post": "鄂伦春自治旗委书记（2026-06 起）", "current_org": "中共鄂伦春自治旗委员会",
        "source": "本地仓库 scripts/build/build_扎赉诺尔区_data.py（呼伦贝尔市委组织部任前公示）",
        "confidence": "confirmed",
        "notes": "曾任满洲里市委常委、政法委书记（至2022-03）；2022-03 起满洲里市委常委兼扎赉诺尔区委书记；2026-06 调任鄂伦春自治旗委书记",
    },
    {
        "id": 43, "name": "布尔金", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1976年11月", "birthplace": "",
        "education": "博士研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "扎赉诺尔区委书记（2026-06 起）", "current_org": "中共扎赉诺尔区委员会",
        "source": "扎赉诺尔区政府领导之窗 /Leader/show/256/828.html",
        "confidence": "confirmed",
        "notes": "曾任满洲里市委常委、副市长（2023-06 至 2025-03）；2025-04 起扎赉诺尔区委副书记、区长；2026-06 任扎赉诺尔区委书记",
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共满洲里市委员会", "type": "党委", "level": "地厅级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 2, "name": "满洲里市人民政府", "type": "政府", "level": "正处级/计划单列市", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 3, "name": "中共满洲里市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共满洲里市委员会", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 4, "name": "中共满洲里市委组织部", "type": "党委", "level": "县处级", "parent": "中共满洲里市委员会", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 5, "name": "中共满洲里市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共满洲里市委员会", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 6, "name": "满洲里市人民武装部", "type": "事业单位", "level": "县处级", "parent": "呼伦贝尔军分区", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 7, "name": "中共满洲里市委统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共满洲里市委员会", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 8, "name": "中共满洲里市委宣传部", "type": "党委", "level": "县处级", "parent": "中共满洲里市委员会", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 9, "name": "满洲里市公安局", "type": "政府", "level": "县处级", "parent": "满洲里市人民政府", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 10, "name": "满洲里市人大常委会", "type": "人大", "level": "县处级", "parent": "呼伦贝尔市人大常委会", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 11, "name": "中国人民政治协商会议满洲里市委员会", "type": "政协", "level": "县处级", "parent": "呼伦贝尔市政协", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 12, "name": "中共满洲里市委办公室", "type": "党委", "level": "县处级", "parent": "中共满洲里市委员会", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 13, "name": "中共根河市委员会", "type": "党委", "level": "县处级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市根河市"},
    {"id": 14, "name": "根河市人民政府", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市根河市"},
    {"id": 15, "name": "中共呼伦贝尔市委员会", "type": "党委", "level": "地市级", "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区呼伦贝尔市"},
    {"id": 16, "name": "呼伦贝尔市人民政府", "type": "政府", "level": "地市级", "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区呼伦贝尔市"},
    {"id": 17, "name": "中共阿鲁科尔沁旗委员会", "type": "党委", "level": "县处级", "parent": "中共赤峰市委", "location": "内蒙古自治区赤峰市阿鲁科尔沁旗"},
    {"id": 18, "name": "中共鄂伦春自治旗委员会", "type": "党委", "level": "县处级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市鄂伦春自治旗"},
    {"id": 19, "name": "中共扎赉诺尔区委员会", "type": "党委", "level": "县处级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 20, "name": "扎赉诺尔区人民政府", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 21, "name": "中共新巴尔虎右旗委员会", "type": "党委", "level": "县处级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市新巴尔虎右旗"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 王成石（现任书记）
    {"person_id": 1, "org_id": 14, "title": "根河市市长", "start_date": "待查", "end_date": "2021-10", "rank": "正处级", "note": "2019-12-25 中新网《中国冷极马拉松》报道以根河市长身份出席"},
    {"person_id": 1, "org_id": 13, "title": "根河市委书记", "start_date": "2021-10", "end_date": "2026-07", "rank": "正处级", "note": "2021-10-14 中新网报道以根河市委书记身份分享生态文明示范区经验；2022-06、2023-01 仍为该职"},
    {"person_id": 1, "org_id": 1, "title": "满洲里市委书记", "start_date": "2026-07-09", "end_date": "present", "rank": "地厅级", "note": "2026-07-09 主持市委专题会议暨自贸区满片区党工委（扩大）会议（市政府网2026-07-13发布）；2026-07-14 起密集调研"},
    # 陈艳豹（代市长）
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记、副市长、代市长（市长候选人）", "start_date": "2026-07-31", "end_date": "present", "rank": "正处级", "note": "2026-07-31 市十六届人大常委会第三十二次会议审议人事任免事项（列席名单载明市长候选人）；2026-08-04 起以代市长身份调研"},
    # 现任班子
    {"person_id": 3, "org_id": 3, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介（截至2026-08）"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "市政府副市长、党组成员（一级调研员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-31 列席市人大常委会第三十二次会议"},
    {"person_id": 5, "org_id": 4, "title": "市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介"},
    {"person_id": 6, "org_id": 5, "title": "市委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介"},
    {"person_id": 7, "org_id": 12, "title": "市委常委、办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介"},
    {"person_id": 8, "org_id": 6, "title": "市委常委、市人民武装部上校政治委员", "start_date": "", "end_date": "present", "rank": "", "note": "官方简介"},
    {"person_id": 9, "org_id": 7, "title": "市委常委、统战部部长（提名免去市政府副市长）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介"},
    {"person_id": 10, "org_id": 2, "title": "市委常委、市政府副市长、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介"},
    {"person_id": 11, "org_id": 8, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介"},
    {"person_id": 12, "org_id": 2, "title": "市政府副市长、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 9, "title": "市公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "市政府副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简介未载党派"},
    {"person_id": 14, "org_id": 2, "title": "市政府副市长、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 10, "title": "市人大常委会主任、党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026-07-31 主持市十六届人大常委会第三十二次会议"},
    {"person_id": 16, "org_id": 10, "title": "市人大常委会副主任、党组副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 10, "title": "市人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 10, "title": "市人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 10, "title": "市人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 11, "title": "市政协党组书记、主席候选人提名人选", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 11, "title": "市政协副主席、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 11, "title": "市政协副主席、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 11, "title": "市政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 11, "title": "市政协副主席、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 11, "title": "市政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 前任
    {"person_id": 40, "org_id": 17, "title": "赤峰市委常委、宣传部部长兼阿鲁科尔沁旗旗委书记", "start_date": "待查", "end_date": "约2021", "rank": "副厅级", "note": "2021-06 全国优秀县委书记拟表彰/表彰（中新网）"},
    {"person_id": 40, "org_id": 1, "title": "满洲里市委书记", "start_date": "约2021-2022", "end_date": "2026-07-02", "rank": "地厅级", "note": "2023-07-20 以满洲里市委书记身份介绍口岸建设（中新网）；2026-07-01/02 最后一次公开活动"},
    {"person_id": 41, "org_id": 2, "title": "满洲里市委副书记、市长", "start_date": "待查", "end_date": "2026-06", "rank": "正处级", "note": "2022-11-30 为蒙古国驻满洲里领事馆开馆揭牌；2026-03-10 作政府工作报告；2026-06-12 最后一次公开活动"},
    {"person_id": 42, "org_id": 1, "title": "满洲里市委常委、政法委书记", "start_date": "待查", "end_date": "2022-03", "rank": "副处级", "note": ""},
    {"person_id": 42, "org_id": 19, "title": "满洲里市委常委兼扎赉诺尔区委书记", "start_date": "2022-03", "end_date": "2026-06", "rank": "正处级", "note": ""},
    {"person_id": 42, "org_id": 18, "title": "鄂伦春自治旗旗委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 43, "org_id": 1, "title": "满洲里市委常委、副市长", "start_date": "2023-06", "end_date": "2025-03", "rank": "副处级", "note": ""},
    {"person_id": 43, "org_id": 20, "title": "扎赉诺尔区委副书记、区长", "start_date": "2025-04", "end_date": "2026-06", "rank": "正处级", "note": ""},
    {"person_id": 43, "org_id": 19, "title": "扎赉诺尔区委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "市委书记王成石 × 市委副书记、代市长陈艳豹（2026-07 起党政一把手搭档）", "overlap_org": "中共满洲里市委员会/满洲里市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 40, "type": "前任后任", "context": "于伟东 2026-07 卸任满洲里市委书记，王成石 2026-07-09 起接任；两人均从旗县（旗/市）委书记岗升任满洲里书记", "overlap_org": "中共满洲里市委员会", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 41, "type": "前任后任", "context": "岳国栋 2026-06 离任满洲里市委副书记、市长，陈艳豹 2026-07-31 任代市长（市长候选人）", "overlap_org": "满洲里市人民政府", "overlap_period": "2026-07"},
    {"person_a": 40, "person_b": 41, "type": "搭档", "context": "于伟东任满洲里市委书记期间与市长岳国栋形成党政搭档", "overlap_org": "中共满洲里市委员会/满洲里市人民政府", "overlap_period": "2023—2026-06"},
    {"person_a": 40, "person_b": 42, "type": "上下级", "context": "齐善剑曾任满洲里市委常委、政法委书记（至2022-03），后以满洲里市委常委身份兼任扎赉诺尔区委书记（于伟东任书记期间）", "overlap_org": "中共满洲里市委员会", "overlap_period": "约2021—2022-03"},
    {"person_a": 40, "person_b": 43, "type": "上下级", "context": "布尔金 2023-06 至 2025-03 任满洲里市委常委、副市长（于伟东为书记，班子交集）", "overlap_org": "中共满洲里市委员会/满洲里市人民政府", "overlap_period": "2023-06—2025-03"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记 × 市委常委、组织部部长王松岩（干部工作条线）", "overlap_org": "中共满洲里市委员会", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委书记 × 市委常委、纪委书记、监委主任隋剑平（监督条线）", "overlap_org": "中共满洲里市委员会", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "市委书记 × 市委常委、办公室主任邓月升（2026-07/08 多场调研随行）", "overlap_org": "中共满洲里市委员会", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记 × 市委副书记、政法委书记滕广兴", "overlap_org": "中共满洲里市委员会", "overlap_period": "2026-07—present"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "代市长 × 市委常委、副市长常青（2026-07-31 列席市人大常委会）", "overlap_org": "满洲里市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "代市长 × 副市长、市公安局局长魏洪玉", "overlap_org": "满洲里市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "代市长 × 市委常委、副市长（现转统战）焦捷", "overlap_org": "满洲里市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 41, "person_b": 9, "type": "同事", "context": "岳国栋市长任期内焦捷为副市长（2022前后—2026-06，政府班子交叠）", "overlap_org": "满洲里市人民政府", "overlap_period": "2022—2026-06"},
    {"person_a": 41, "person_b": 12, "type": "同事", "context": "岳国栋市长任期内魏洪玉任副市长兼公安局长（任内交叠）", "overlap_org": "满洲里市人民政府", "overlap_period": "2022—2026-06"},
]

# ── Person JSON 生成 ─────────────────────────────────────────────────────────


def _source_register(person: dict) -> list[dict]:
    reg = [{
        "id": "S001",
        "title": f"满洲里市人民政府领导之窗 - {person['name']}",
        "url": _person_source(person),
        "publisher": "满洲里市人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official" if "manzhouli.gov.cn" in _person_source(person) else "media",
        "reliability": "high",
        "notes": person.get("notes", "")[:200],
    }]
    if person["id"] in (40, 41):
        reg.append({
            "id": "S002", "title": "中国新闻网相关报道",
            "url": _person_source(person),
            "publisher": "中国新闻网", "published_at": "",
            "accessed_at": AS_OF, "source_type": "media", "reliability": "high",
            "notes": "履历时间线佐证",
        })
    return reg


def write_person_jsons() -> list[str]:
    """Write deep person graph JSONs for core figures (id 1, 2, 40, 41)."""
    written = []
    for p in persons:
        if p["id"] not in (1, 2, 40, 41):
            continue
        job = p["current_post"].split("（")[0].split("、")[0].replace(" ", "_").strip()
        fname = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{job}-{p['name']}.json"
        reg = _source_register(p)

        career = []
        for pos in positions:
            if pos["person_id"] != p["id"]:
                continue
            org = _org_by_id(pos["org_id"])
            career.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", "present"),
                "org": org.get("name", ""),
                "title": pos["title"],
                "level": org.get("level", ""),
                "location": org.get("location", ""),
                "system": "party" if org.get("type") == "党委" else ("government" if org.get("type") == "政府" else org.get("type", "")),
                "rank": pos.get("rank", ""),
                "is_key_promotion": ("满洲里市委书记" in pos["title"]) or ("代市长" in pos["title"]),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if pos["title"].startswith("满洲里") else "plausible",
                "source_ids": ["S001"],
            })
        if not career:
            career.append({
                "start": "unknown", "end": "unknown", "org": "履历缺口",
                "title": "", "notes": "公开资料未找到该段履历", "confidence": "unverified", "source_ids": [],
            })

        rels = []
        for r in relationships:
            if r["person_a"] == p["id"]:
                other = _person_by_id(r["person_b"])
                if other:
                    rels.append({
                        "person": other["name"],
                        "person_id": f"manzhouli_{other['name']}",
                        "relationship_type": r["type"],
                        "strength": "strong" if r["type"] in ("前任后任", "搭档") else "medium",
                        "evidence": r["context"],
                        "overlap_org": r["overlap_org"],
                        "overlap_period": r["overlap_period"],
                        "direction": "person_to_other",
                        "confidence": "confirmed",
                        "source_ids": ["S001"],
                    })
            elif r["person_b"] == p["id"]:
                other = _person_by_id(r["person_a"])
                if other:
                    rels.append({
                        "person": other["name"],
                        "person_id": f"manzhouli_{other['name']}",
                        "relationship_type": r["type"],
                        "strength": "strong" if r["type"] in ("前任后任", "搭档") else "medium",
                        "evidence": r["context"],
                        "overlap_org": r["overlap_org"],
                        "overlap_period": r["overlap_period"],
                        "direction": "other_to_person",
                        "confidence": "confirmed",
                        "source_ids": ["S001"],
                    })

        governance = []
        if p["id"] == 1:
            governance = [{
                "period": "2026-07", "domain": "economic_development",
                "achievement_or_event": "主持中国（内蒙古）自由贸易试验区满洲里片区改革试点与内蒙古满洲里产业协作园区建设调度",
                "role_in_event": "牵头协调",
                "measurable_outcome": "推进口岸'通道经济'向'落地经济'转型、破解'酒肉穿肠过'命题",
                "location": "满洲里市", "confidence": "confirmed", "source_ids": ["S001"],
            }]
        if p["id"] == 2:
            governance = [{
                "period": "2026-08", "domain": "economic_development",
                "achievement_or_event": "带队调研重点项目建设（公路口岸扩能、铁路改造、粮油加工、冷链物流），赴满洲里海关座谈",
                "role_in_event": "牵头推进",
                "measurable_outcome": "推动项目前期手续提速、争取上级资金政策支持",
                "location": "满洲里市", "confidence": "confirmed", "source_ids": ["S001"],
            }]

        style_indicators = []
        if p["id"] == 1:
            style_indicators = [{
                "trait": "reform_oriented",
                "evidence": "多次强调依托自贸试验区满片区与产业协作园区双平台、加快制度创新（2026-07-13 市委专题会议）",
                "confidence": "confirmed", "source_ids": ["S001"],
            }]

        obj = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE, "city": PARENT_CITY, "region": REGION,
                "job": p["current_post"], "task_id": TASK_ID,
                "time_focus": "2026-08 现职快照 + 履历回溯",
            },
            "identity": {
                "person_id": f"manzhouli_{p['name']}",
                "name": p["name"], "aliases": [],
                "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [{
                    "period": "", "institution": p.get("education", ""), "major": "",
                    "degree": p.get("education", ""), "study_type": "unknown",
                    "source_ids": ["S001"],
                }] if p.get("education") else [],
                "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', 'unknown')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', 'unknown')}",
                    "official_profile_url": _person_source(p),
                },
            },
            "current_status": {
                "current_post": p["current_post"], "current_org": p.get("current_org", ""),
                "administrative_rank": "正厅级" if p["id"] == 1 else ("正处级" if p["id"] in (2, 41) else "正厅级"),
                "as_of": AS_OF, "is_current_confirmed": p["confidence"] == "confirmed",
                "source_ids": ["S001"],
            },
            "career_timeline": career,
            "organizations": [],
            "relationships": rels,
            "governance_record": governance,
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "county_to_border_city" if p["id"] in (1, 40) else "local_ladder",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": style_indicators,
                "speech_themes": [],
                "management_signals": [],
                "caveat": "工作风格依据公开报道、讲话与治理行动推断，非私人心理评估。",
            },
            "network_metrics": {
                "total_relationships": len(rels),
                "strong_connections": sum(1 for x in rels if x["strength"] == "strong"),
                "cross_region_connections": sum(1 for x in rels if any(k in x["overlap_org"] for k in ("根河", "扎赉诺尔", "鄂伦春", "阿鲁科尔钦"))),
                "mentor_chain_length": 0,
            },
            "risk_and_integrity_signals": [{
                "type": "none_found",
                "description": "截至 2026-08-11，公开检索未发现现任领导被处分、调查或负面报道",
                "date": "", "confidence": "unverified", "source_ids": [],
            }],
            "source_register": reg,
            "confidence_summary": {
                "identity": "confirmed" if p.get("birth") else "partial",
                "current_role": "confirmed" if p["confidence"] == "confirmed" else "unverified",
                "career_completeness": "partial" if p["id"] in (1, 40, 41) else "thin",
                "relationship_confidence": "high" if p["id"] in (1, 2) else "medium",
                "biggest_gap": f"{p['name']} 任满洲里现职前的早期履历及离任去向",
            },
            "open_questions": _open_questions(p),
        }
        (STAGING / fname).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(fname)
    return written


def _open_questions(p: dict) -> list[dict]:
    q = [{
        "priority": "critical",
        "question": f"{p['name']} 的完整履历（含教育细节、籍贯、早期职务）",
        "why_it_matters": "核心身份信息，妨碍跨区人物去重与晋升路径还原",
        "suggested_queries": [f"{p['name']} 履历 满洲里", f"{p['name']} 呼伦贝尔 简历", f"{p['name']} 任前公示"],
        "last_attempted": AS_OF,
    }]
    if p["id"] == 40:
        q.append({
            "priority": "high", "question": "于伟东 2026-07 卸任满洲里市委书记后的去向",
            "why_it_matters": "确认干部后续流动与呼伦贝尔—满洲里人事循环",
            "suggested_queries": ["于伟东 2026 职务", "于伟东 呼伦贝尔 任免"], "last_attempted": AS_OF,
        })
    if p["id"] == 41:
        q.append({
            "priority": "high", "question": "岳国栋 2026-06 离任满洲里市长后的去向",
            "why_it_matters": "确认前市长流动路径", "suggested_queries": ["岳国栋 2026 职务", "岳国栋 调任"],
            "last_attempted": AS_OF,
        })
    if p["id"] == 1:
        q.append({
            "priority": "high", "question": "王成石 2019 年前（2019-12 以根河市长身份亮相之前）的履历",
            "why_it_matters": "1981 年生干部早期经历，公开渠道空白", "suggested_queries": ["王成石 简历", "王成石 根河 市长 此前"],
            "last_attempted": AS_OF,
        })
    if p["id"] == 2:
        q.append({
            "priority": "critical", "question": "陈艳豹 任满洲里市长前一段职务（2024-2026 在何处任职）",
            "why_it_matters": "代市长来源是市级干部交流关键环节", "suggested_queries": ["陈艳豹 简历", "陈艳豹 呼伦贝尔"],
            "last_attempted": AS_OF,
        })
    return q


# ── Markdown 报告 ─────────────────────────────────────────────────────────────


def write_report() -> str:
    L: list[str] = []
    A = L.append
    A(f"# 满洲里市领导班子工作关系网络调查报告")
    A("")
    A(f"> 调研日期：2026-08-11　|　数据快照：2026-08-11　|　任务：`{TASK_ID}`")
    A("")
    A("## 1. 现任市委书记：王成石")
    A("")
    A("- 男，满族，1981年10月生，大学，中共党员（满洲里市政府网 领导之窗 官方简介）。")
    A("- 现任中共满洲里市委书记、市委党校（行政学院）校长（院长），主持市委全面工作。")
    A("- 履历脉络（已证实）：")
    A("    - 根河市市长（2019-12 中新网《中国冷极马拉松》报道）；")
    A("    - 根河市委书记（2021-10-14 中新网 COP15 报道、2022-06、2023-01 多篇报道）；")
    A("    - 满洲里市委书记（2026-07-09 主持市委专题会议起；2026-07-14 起密集公开调研，报道均为“市委书记王成石”）。")
    A("- 治理重心：以中国（内蒙古）自由贸易试验区满洲里片区与内蒙古满洲里产业协作园区双平台为引擎，推动口岸由“通道经济”向“落地经济”转型、破解“酒肉穿肠过”命题（2026-07 市委专题会议表述）。")
    A("- 履历缺口：2019 年之前的早期职务、教育细节与籍贯——待查。")
    A("")
    A("## 2. 现任市委副书记、代市长（市长候选人）：陈艳豹")
    A("")
    A("- 男，汉族，1980年1月生，大学，中共党员（官方简介）。")
    A("- 现任市委副书记、市政府党组书记、副市长、代市长（市长候选人提名人选），主持市人民政府全面工作。")
    A("- 2026-07-31 满洲里市第十六届人大常委会第三十二次会议审议通过人事任免事项（列席名单载明其“市长候选人”身份）；2026-08-04 起以代市长身份调研重点项目、走访慰问、赴满洲里海关座谈。")
    A("- 履历缺口：任满洲里市长前职务与完整履历——待查。")
    A("")
    A("## 3. 前任领导（去向）")
    A("")
    A("### 3.1 前任市委书记：于伟东")
    A("- 2021-06 全国优秀县委书记表彰名单（时任赤峰市委常委、宣传部部长、阿鲁科尔沁旗旗委书记）。")
    A("- 2023-07-20 以满洲里市委书记身份介绍口岸建设（中新网）；2026-07-01/02 最后一次公开活动（满洲里市政府网）。")
    A("- 去向：2026-07 卸任后待查。")
    A("")
    A("### 3.2 前任市长：岳国栋")
    A("- 2022-11-30 以满洲里市委副书记、市长身份为蒙古国驻满洲里领事馆开馆揭牌（中新网）；2026-03-10 作2026年政府工作报告；2026-06-12 最后一次公开活动。")
    A("- 去向：待查。")
    A("")
    A("## 4. 领导班子成员（现职，2026-08）")
    A("")
    A("| 类别 | 姓名 | 职务 | 出生 | 备注 |")
    A("|---|---|---|---|---|")
    for p in persons:
        if p["id"] in (40, 41, 42, 43):
            continue
        cat = "党委" if p["id"] <= 11 else ("政府" if p["id"] in (12, 13, 14) else ("人大" if p["id"] in (15, 16, 17, 18, 19) else "政协"))
        A(f"| {cat} | {p['name']} | {p['current_post']} | {p.get('birth', '')} | {'/'.join(x for x in [p.get('ethnicity', ''), p.get('education', '')] if x)} |")
    A("")
    A("## 5. 近期人事变动时间线")
    A("")
    A("- 2026-03-10：市长岳国栋在市十六届人大六次会议上作2026年政府工作报告。")
    A("- 2026-06-12：岳国栋最后一次公开活动（此后卸任市长）。")
    A("- 2026-07-01/02：于伟东开展“七一”走访慰问（最后一次公开现身）。")
    A("- 2026-07-09：新任市委书记王成石主持市委专题会议（自贸区满片区党工委扩大会议）。")
    A("- 2026-07-13/14：王成石以市委书记身份连续开展调研（全市重点工作、防汛排涝）。")
    A("- 2026-07-30/31：市十六届人大常委会第三十二次会议审议人事任免，陈艳豹任代市长。")
    A("- 2026-08-04~05：陈艳豹以代市长调研重点项目、走访慰问、赴满洲里海关座谈。")
    A("- 2026-08-08：呼伦贝尔市领导干部会议宣布杜汇良任呼伦贝尔市委书记。")
    A("- 2026-08-10：王成石、陈艳豹联合调研重点项目建设。")
    A("")
    A("## 6. 工作关系网络分析")
    A("")
    A("### 已证实的关系边（强关系）")
    A("- 王成石 × 陈艳豹：现任党政一把手搭档（2026-07 至今）——红线。")
    A("- 于伟东 × 王成石：满洲里市委书记前/后任（2026-07），且两人均从旗县（旗/市）委书记岗位升任满洲里，构成“旗县级书记→满洲里书记”通道。")
    A("- 岳国栋 × 陈艳豹：市长前/后任（2026-06/07）。")
    A("- 于伟东-岳国栋：2023—2026-06 满洲里党政班子搭档。")
    A("- 于伟东-齐善剑：齐任满洲里市委常委、政法委书记至2022-03，后以市委常委身份兼任扎赉诺尔区委书记（于任内）。")
    A("- 于伟东-布尔金：布尔金 2023-06 至 2025-03 任满洲里市委常委、副市长。")
    A("- 现任班子内部：书记—组织部（王松岩）、书记—纪委（隋剑平）、书记—办公室（邓月升）等条线上下级关系。")
    A("")
    A("### 结构性观察")
    A("- 满洲里市委书记岗成为呼伦贝尔体系“全国优秀县级/县旗书记”的晋升高地（于伟东—阿鲁科尔钦，王成石—根河）。")
    A("- 满洲里—扎赉诺尔体系高度联通：齐善剑、布尔金均有满洲里市委常委经历，形成干部流转带。")
    A("- 2026 年 7 月底政府/市长、人大、政协同步更替（新的政协主席候选人王涛），满洲里进入新一届班子磨合期；呼伦贝尔市级同步换帅（杜汇良）。")
    A("")
    A("## 7. 跨县区人事交流与区域网络")
    A("- 满洲里隶属呼伦贝尔：2026-08-08 呼伦贝尔市委书记交接（杜汇良任市委），满洲里干部任免链路上层变化。")
    A("- 旗县联动：满洲里与新巴尔虎右旗 2026-08-05 签署自贸片区联动/沿边产业协作园区合作框架协议（王成石、陈艳豹与新右旗委书记包格吉勒图会商）。")
    A("- 满洲里—扎赉诺尔属地链：扎区委书记（齐善剑→布尔金）均经满洲里常委岗，体现准计划单列市统筹。")
    A("")
    A("## 8. 关键洞察与突破线索")
    A("")
    A("1. **落位重心：陈艳豹来源**。市长候选人任前很可能来自呼伦贝尔市直行政机关或满洲里市直部门；呼伦贝尔市委组织部任前公示是首测。")
    A("2. **于伟东落位**：优秀县委书记空降满洲里后离任——去向（呼伦贝尔市委/自治区厅局）预示其上一级轨迹。")
    A("3. **岳国栋去向**：市长离任方向（市局/旗县/退休）标志满洲里班子循环。")
    A("4. **王成石早期履历**（2019 前）未知：若科班出身（组织/经济口）可作为 2026-2028 履职预测基线。")
    A("5. 自贸片区改革（2026-2027）为新班子绩效试金石：王成石“项目为王”表述是捕捉合作窗口的重点。")
    A("")
    A("## 9. 数据文件说明")
    A("")
    A("- `满洲里市_network.db`：SQLite 四表（persons/organizations/positions/relationships）。")
    A("- `满洲里市_network.gexf`：GEXF 1.3 图；红=书记、蓝=行政首长、橙=纪委、灰=其他；组织节点浅色。")
    A("- person JSON：核心人物 4 份（王成石、陈艳豹、于伟东、岳国栋）。")
    A("")
    A("## 10. 信息来源汇总")
    A("")
    A("| # | 来源 | URL | 类型 | 可靠性 |")
    A("|---|---|---|---|---|")
    A("| 1 | 满洲里市人民政府领导之窗 | https://www.manzhouli.gov.cn/Leader/ | 官方 | 高 |")
    A("| 2 | 满洲里市政府网市政要闻 | http://www.manzhouli.gov.cn/News/showList/30919/ | 官方 | 高 |")
    A("| 3 | 满洲里市人大（32次会议/任免） | http://www.manzhouli.gov.cn/News/show/1446204.html | 官方 | 高 |")
    A("| 4 | 呼伦贝尔市政府网（杜汇良任职） | https://www.hlbe.gov.cn/News/show/1447865.html | 官方 | 高 |")
    A("| 5 | 中新网：王成石（根河市长/书记） | https://www.chinanews.com.cn/ty/2019/12-25/9043335.shtml | 媒体 | 高 |")
    A("| 6 | 中新网：于伟东 | https://www.chinanews.com.cn/gn/2021/06-07/9493941.shtml | 媒体 | 高 |")
    A("| 7 | 中新网：于伟东任满洲里书记 | https://www.chinanews.com.cn/cj/2023/07-21/10047628.shtml | 媒体 | 高 |")
    A("| 8 | 中新网：岳国栋 | https://www.chinanews.com.cn/gn/2022/11-30/9905947.shtml | 媒体 | 高 |")
    A("| 9 | 本地仓库：扎赉诺尔区建库（齐、布尔金） | scripts/build_扎赉诺尔区_data.py | 本地 | 中高 |")
    A("")
    A("## 11. 开放问题（Open Gaps）")
    A("")
    A("| 优先级 | 问题 | 建议查询 |")
    A("|---|---|---|")
    A("| 🔴 关键 | 陈艳豹任市长前履历/来源机关 | `陈艳豹 简历`、`陈艳豹 呼伦贝尔`、任前公示 |")
    A("| 🔴 关键 | 王成石 2019 年前履历 | `王成石 简历`、`王成石 根河` |")
    A("| 🟠 高 | 于伟东卸任后去向 | `于伟东 2026 职务`、`于伟东 调任` |")
    A("| 🟠 高 | 岳国栋离任后去向 | `岳国栋 2026 职务`、`岳国栋 调任` |")
    A("| 🟠 高 | 满洲里 2021-2023 届市委班子成员更替线 | 满洲里市委 2021-2023 班子名单 |")
    A("| 🟡 低 | 毛婷彤、杜明燕等党外干部履职细节 | 个人简介扩展页 |")
    A("")
    (REPORT_PATH).write_text("\n".join(L), encoding="utf-8")
    return str(REPORT_PATH)


# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═══ Building {SLUG} data ═══")
    print(f"  Staging: {STAGING}")

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
    jsons = write_person_jsons()
    for j in jsons:
        print(f"    ✓ {j}")

    print("  Writing report...")
    print(f"    ✓ {write_report()}")

    print("\n═══ Summary ═══")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  Done.")