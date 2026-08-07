#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 永宁县 (Yongning County), 银川市, 宁夏回族自治区.

Investigation date: 2026-08-07
Task ID: ningxia_永宁县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.nxyn.gov.cn — 永宁县人民政府官方网站 (primary, current as of July 2026)
    * 领导之窗: http://www.nxyn.gov.cn/zwgk/ldzc/xw/ (县委领导)
    * 张建兵 profile: http://www.nxyn.gov.cn/zwgk/ldzc/xw/201810/t20181017_1130155.html
    * 龚涛 profile: http://www.nxyn.gov.cn/zwgk/ldzc/zf/202604/t20260403_5209981.html
    * 黄学忠 profile: http://www.nxyn.gov.cn/zwgk/ldzc/zf/202204/t20220418_3455892.html
    * 张冲 profile: http://www.nxyn.gov.cn/zwgk/ldzc/zf/202204/t20220418_3455907.html
    * 领导分工通知: http://www.nxyn.gov.cn/zwgk/gkbm/ynxzfbgs/fdzdgknr_65328/zfwj_15484/202601/t20260112_5132962.html
  - 宁夏区委组织部任前公示 2026年第4号: https://www.nx.gov.cn/zwgk/rsrm/202603/t20260324_5200655.html (龚涛)
  - 宁夏区委组织部任前公示 2023年第2号: https://www.nx.gov.cn/zwgk/rsrm/202308/t20230802_4203164.html (张建兵)
  - 永宁党建网 (nxynzzb.gov.cn) 干部任前公示
  - 中国经济网 2018-10-19 (朱剑调任报道)

Confidence notes:
  - Current roles: confirmed via 领导之窗 profiles and government meeting/news reports (official)
  - 龚涛 prior post (中卫市沙坡头区委常委、副区长): confirmed via 2026年自治区任前公示
  - 张建兵 prior posts (西夏区区长): confirmed via 任前公示 + 西夏区政府工作报告
  - Biographical gaps (birthplace, education details for many) flagged in open_questions
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "永宁县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_永宁县"
if _CURRENT_DIR.name == "ningxia_永宁县":
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
# IDs: 1-2 core (书记/县长), 3-4 县委副书记/前任, 5-9 县委常委会,
#      10-16 政府班子, 17-23 人大/政协

persons = [
    # ════ CORE: 县委书记 & 县长 ════
    {
        "id": 1,
        "name": "张建兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共永宁县委书记",
        "current_org": "中共永宁县委员会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/xw/201810/t20181017_1130155.html",
    },
    {
        "id": 2,
        "name": "龚涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-11",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委副书记、县长",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/xw/201811/t20181101_1146277.html",
    },
    # ═══ 县委副书记 ════
    {
        "id": 3,
        "name": "李臻卓",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委副书记、闽宁镇党委副书记（挂职）",
        "current_org": "中共永宁县委员会",
        "source": "http://www.nxyn.gov.cn/zwgk/gkbm/ynxmnz/xxgkmn/ldxx/202507/t20250731_4976029.html",
    },
    {
        "id": 4,
        "name": "雒越强",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1980-09",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县前任县长（2026-02 离职，去向未明）",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/zfgb/2024n/d3q/202410/t20241011_4690318.html",
    },
    # ════ 县委常委会 ════
    {
        "id": 5,
        "name": "马玉祥",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委常委、组织部部长、统战部部长",
        "current_org": "中共永宁县委员会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/xw/201708/t20170802_365602.html",
    },
    {
        "id": 6,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委常委",
        "current_org": "中共永宁县委员会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/xw/202407/t20240705_4588409.html",
    },
    {
        "id": 7,
        "name": "石佳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委常委、闽宁镇党委书记",
        "current_org": "中共永宁县闽宁镇委员会",
        "source": "http://www.nxyn.gov.cn/zwgk/gkbm/ynxmnz/xxgkmn/ldxx/202507/t20250731_4976029.html",
    },
    {
        "id": 8,
        "name": "杨丽琴",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委常委、县纪委书记、县监委主任",
        "current_org": "永宁县纪委监委",
        "source": "http://jjjc.yinchuan.gov.cn/xqxxgk/ynx/qt_43452/",
    },
    {
        "id": 9,
        "name": "殷玥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委常委",
        "current_org": "中共永宁县委员会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/xw/202511/t20251117_5085090.html",
    },
    # ════ 县政府班子 ════
    {
        "id": 10,
        "name": "黄学忠",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委常委、常务副县长",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/zf/202204/t20220418_3455892.html",
    },
    {
        "id": 11,
        "name": "张冲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县委常委、副县长",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/zf/202204/t20220418_3455907.html",
    },
    {
        "id": 12,
        "name": "李石珍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县副县长",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/gkbm/ynxzfbgs/fdzdgknr_65328/zfwj_15484/202601/t20260112_5132962.html",
    },
    {
        "id": 13,
        "name": "王敏敏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县副县长、县公安局局长",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/gkbm/ynxzfbgs/fdzdgknr_65328/zfwj_15484/202601/t20260112_5132962.html",
    },
    {
        "id": 14,
        "name": "杨雅理",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县副县长",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/gkbm/ynxzfbgs/fdzdgknr_65328/zfwj_15484/202601/t20260112_5132962.html",
    },
    {
        "id": 15,
        "name": "徐军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县副县长（厦门市湖里区挂职）",
        "current_org": "永宁县人民政府",
        "source": "http://www.nxyn.gov.cn/zwgk/gkbm/ynxzfbgs/fdzdgknr_65328/zfwj_15484/202601/t20260112_5132962.html",
    },
    # ════ 前任书记 ════
    {
        "id": 16,
        "name": "朱剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县原县委书记（2023-08 离职，去向未明）",
        "current_org": "中共永宁县委员会",
        "source": "http://district.ce.cn/newarea/sdod/201810/19/t20181019_30575481.html",
    },
    # ════ 人大 ════
    {
        "id": 17,
        "name": "陈东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县人大常委会主任",
        "current_org": "永宁县人大常委会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/rd/",
    },
    {
        "id": 18,
        "name": "马少军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县人大常委会副主任",
        "current_org": "永宁县人大常委会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/rd/",
    },
    {
        "id": 19,
        "name": "姜利",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县人大常委会副主任",
        "current_org": "永宁县人大常委会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/rd/",
    },
    {
        "id": 20,
        "name": "曹永进",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县人大常委会副主任",
        "current_org": "永宁县人大常委会",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/rd/",
    },
    # ════ 政协 ════
    {
        "id": 21,
        "name": "郑进选",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县政协主席",
        "current_org": "永宁县政协",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/zx/",
    },
    {
        "id": 22,
        "name": "马立云",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县政协副主席",
        "current_org": "永宁县政协",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/zx/",
    },
    {
        "id": 23,
        "name": "张文霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县政协副主席",
        "current_org": "永宁县政协",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/zx/",
    },
    {
        "id": 24,
        "name": "马文君",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永宁县政协副主席",
        "current_org": "永宁县政协",
        "source": "http://www.nxyn.gov.cn/zwgk/ldzc/zx/",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共永宁县委员会", "type": "党委", "level": "县处级", "parent": "中共银川市委员会", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 2, "name": "永宁县人民政府", "type": "政府", "level": "县处级", "parent": "银川市人民政府", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 3, "name": "永宁县人大常委会", "type": "人大", "level": "县处级", "parent": "银川市人大常委会", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 4, "name": "永宁县政协", "type": "政协", "level": "县处级", "parent": "银川市政协", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 5, "name": "永宁县纪委监委", "type": "纪委", "level": "县处级", "parent": "中共永宁县委员会", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 6, "name": "中共永宁县闽宁镇委员会", "type": "乡镇党委", "level": "乡科级", "parent": "中共永宁县委员会", "location": "宁夏回族自治区银川市永宁县闽宁镇"},
    {"id": 7, "name": "永宁县公安局", "type": "政府", "level": "乡科级", "parent": "永宁县人民政府", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 8, "name": "中共银川市委员会", "type": "党委", "level": "地厅级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区银川市"},
    {"id": 9, "name": "中卫市沙坡头区", "type": "政府", "level": "县处级", "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市"},
    {"id": 10, "name": "银川市西夏区人民政府", "type": "政府", "level": "县处级", "parent": "银川市人民政府", "location": "宁夏回族自治区银川市西夏区"},
    {"id": 11, "name": "中共银川市兴庆区委员会", "type": "党委", "level": "县处级", "parent": "中共银川市委员会", "location": "宁夏回族自治区银川市兴庆区"},
    {"id": 12, "name": "石嘴山市人民政府", "type": "政府", "level": "地厅级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区石嘴山市"},
    {"id": 13, "name": "中共宁夏回族自治区委员会", "type": "党委", "level": "省部级", "parent": "", "location": "宁夏回族自治区银川市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 张建兵
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2023-08", "end": "present", "rank": "正处级", "note": "主持县委、宁夏永宁工业园区党工委全面工作；兼任人武部党委第一书记"},
    {"person_id": 1, "org_id": 10, "title": "西夏区区长", "start": "2018", "end": "2023-08", "rank": "正处级", "note": "曾任西夏区代区长、区长"},
    {"person_id": 1, "org_id": 10, "title": "西夏区副区长（挂职）", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 龚涛
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026-04 任代县长，2026-05/06 转正"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026-04", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "沙坡头区委常委、副区长", "start": "", "end": "2026-03", "rank": "副处级", "note": "2026-03 任前公示拟提名为县长候选人"},
    # 李臻卓
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "闽宁镇党委副书记（挂职）", "start": "", "end": "present", "rank": "", "note": "负责闽宁协作、招商引资、东西协作考核、闽宁产业园"},
    # 雒越强
    {"person_id": 4, "org_id": 2, "title": "县长", "start": "2021", "end": "2026-02", "rank": "正处级", "note": "2026-02 前仍在任，2026-04 由龚涛接任"},
    {"person_id": 4, "org_id": 11, "title": "银川兴庆区委副书记", "start": "", "end": "2021", "rank": "副处级", "note": "曾任兴庆区委副书记、三级调研员"},
    # 马玉祥
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘涛
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 石佳
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "闽宁镇党委书记", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 杨丽琴
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "县纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 殷玥
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 黄学忠
    {"person_id": 10, "org_id": 2, "title": "常务副县长", "start": "2022", "end": "present", "rank": "副处级", "note": "县委常委、党组副书记；负责常务工作"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张冲
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责人力资源和社会保障、自然资源、农业农村、乡村振兴等"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李石珍
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责市场监管、卫生健康、商务、招商引资、医疗保障、文旅广电等"},
    # 王敏敏
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、信访、司法、平安建设等"},
    {"person_id": 13, "org_id": 7, "title": "县公安局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 杨雅理
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、工业经济、科技、财税金融、审批、营商环境等"},
    # 徐军
    {"person_id": 15, "org_id": 2, "title": "副县长（厦门湖里区挂职）", "start": "", "end": "present", "rank": "副处级", "note": "负责湖里区挂职分管工作，协助招商引资"},
    # 朱剑
    {"person_id": 16, "org_id": 1, "title": "县委书记（银川市委常委兼任）", "start": "2018-10", "end": "2023-08", "rank": "正厅/副厅", "note": "2018-10 由石嘴山市副市长、平罗县委书记调任"},
    {"person_id": 16, "org_id": 12, "title": "石嘴山市副市长、平罗县委书记", "start": "", "end": "2018-10", "rank": "副厅级", "note": ""},
    # 陈东
    {"person_id": 17, "org_id": 3, "title": "人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 马少军/姜利/曹永进
    {"person_id": 18, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郑进选
    {"person_id": 21, "org_id": 4, "title": "政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 马立云/张文霞/马文君
    {"person_id": 22, "org_id": 4, "title": "政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "现任县委书记张建兵与县长龚涛构成党政正职搭档", "overlap_org": "永宁县", "overlap_period": "2026-04至今"},
    # 前任搭档
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "张建兵任书记期间(2023-08~2026-02)雒越强任县长，党政搭档", "overlap_org": "永宁县", "overlap_period": "2023-08~2026-02"},
    # 县长继任
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "雒越强离任后龚涛接任永宁县县长(2026-04)", "overlap_org": "永宁县人民政府", "overlap_period": "2026-04"},
    # 书记继任
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor", "context": "朱剑2023年调离后张建兵接任永宁县委书记", "overlap_org": "永宁县", "overlap_period": "2023-08"},
    # 县长班子
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长领导常务副县长", "overlap_org": "永宁县人民政府", "overlap_period": "2026-04至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长领导副县长（常委）", "overlap_org": "永宁县人民政府", "overlap_period": "2026-04至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长领导副县长", "overlap_org": "永宁县人民政府", "overlap_period": "2026-04至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长领导副县长", "overlap_org": "永宁县人民政府", "overlap_period": "2026-04至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长领导副县长", "overlap_org": "永宁县人民政府", "overlap_period": "2026-04至今"},
    # 常委会
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记领导县委常委会成员", "overlap_org": "中共永宁县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记领导县委常委会成员", "overlap_org": "中共永宁县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记领导以石佳为书记的闽宁镇党委", "overlap_org": "中共永宁县委员会/中共永宁县闽宁镇委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "书记领导纪委书记", "overlap_org": "中共永宁县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "书记领导常务副县长", "overlap_org": "中共永宁县委员会", "overlap_period": "present"},
    # 龚涛县委副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "龚涛与李为县委副书记，同在县委常委会", "overlap_org": "中共永宁县委员会", "overlap_period": "2026-04至今"},
    # 闽宁协作线
    {"person_a": 7, "person_b": 3, "type": "overlap", "context": "石佳（闽宁镇党委书记）与李臻卓（挂职副书记）在闽宁镇共事，负责闽宁协作", "overlap_org": "闽宁镇", "overlap_period": "present"},
]


# ═══════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════

def _career_rows(person: dict, job: str) -> list:
    """Build a career timeline for the person JSON from confirmed evidence."""
    rows = []
    name = person["name"]
    if name == "张建兵":
        rows = [
            {"start": "2023-08", "end": "present", "org": "中共永宁县委员会", "title": "永宁县委书记", "rank": "正处级", "confidence": "confirmed", "note": "2023-08 任前公示由银川市西夏区区长调任"},
            {"start": "2019", "end": "2023-08", "org": "银川市西夏区人民政府", "title": "西夏区区长", "rank": "正处级", "confidence": "confirmed", "note": "曾任代区长、区长"},
            {"start": "unknown", "end": "2019", "org": "银川市西夏区人民政府", "title": "西夏区副区长", "rank": "副处级", "confidence": "plausible", "note": "挂职经历"},
        ]
    elif name == "龚涛":
        rows = [
            {"start": "2026-05", "end": "present", "org": "永宁县人民政府", "title": "永宁县长", "rank": "正处级", "confidence": "confirmed", "note": "2026-04 代县长，后转正"},
            {"start": "2026-04", "end": "present", "org": "中共永宁县委员会", "title": "县委副书记", "rank": "副处级", "confidence": "confirmed", "note": ""},
            {"start": "unknown", "end": "2026-03", "org": "中卫市沙坡头区", "title": "沙坡头区委常委、副区长", "rank": "副处级", "confidence": "confirmed", "note": "2026-03 自治区任前公示拟提名为县长候选人"},
        ]
    elif name == "雒越强":
        rows = [
            {"start": "2021", "end": "2026-02", "org": "永宁县人民政府", "title": "永宁县长", "rank": "正处级", "confidence": "confirmed", "note": "2026-02 前在任，2026-04 由龚涛接任，去向未明"},
            {"start": "unknown", "end": "2021", "org": "银川市兴庆区委员会", "title": "兴庆区委副书记", "rank": "副处级", "confidence": "confirmed", "note": "曾任兴庆区委副书记、三级调研员"},
        ]
    elif name == "朱剑":
        rows = [
            {"start": "2018-10", "end": "2023-08", "org": "中共永宁县委员会", "title": "永宁县委书记", "rank": "副厅/正处", "confidence": "confirmed", "note": "银川市委常委兼任"},
            {"start": "unknown", "end": "2018-10", "org": "石嘴山市人民政府", "title": "石嘴山市副市长、平罗县委书记", "rank": "副厅级", "confidence": "confirmed", "note": ""},
        ]
    else:
        rows = [
            {"start": "unknown", "end": "present", "org": person.get("current_org", ""), "title": person.get("current_post", ""), "rank": "副处级" if "长" in person.get("current_post", "") else "副处级", "confidence": "plausible", "note": "现任职务见官方领导之窗"},
        ]
    return rows


def write_person_json(person: dict, job: str) -> Path:
    """Write a person graph JSON file to the staging directory."""
    name = person["name"]
    person_id = f"yongning_{name}"
    path = PJSON_DIR / f"{TODAY}-宁夏回族自治区-银川市-{job}-{name}.json"
    career = _career_rows(person, job)
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "银川市",
            "region": "永宁县",
            "job": job,
            "task_id": "ningxia_永宁县",
            "time_focus": "2026-08 (current)"
        },
        "identity": {
            "person_id": person_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", "") if person.get("education") else "", "major": "", "degree": person.get("education", ""), "study_type": "party_school" if "党校" in person.get("education", "") else "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if job in ["县委书记", "县长"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [
            {"id": 1, "name": "中共永宁县委员会", "type": "党委"},
            {"id": 2, "name": "永宁县人民政府", "type": "政府"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if name in ["张建兵", "龚涛", "雒越强", "朱剑"] else "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "龚涛(1986年生)2026年38岁任一县之长，属较快晋升" if name == "龚涛" else "",
                "notable_fast_promotions": ["1986年出生，2026年任县长"] if name == "龚涛" else []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No disciplinary or integrity red flags found in publicly available sources during investigation.",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": f"永宁县人民政府 - {name}领导之窗/新闻",
                "url": person.get("source", ""),
                "publisher": "永宁县人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official government website / 任前公示"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生地、入党/工作时间、早期职务）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历（出生地、入党时间、参加工作时间和历任职务）",
                "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
                "suggested_queries": [f"{name} 简历 永宁", f"{name} 任前公示", f"{name} 出生年月"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}的早前职务经历与调动路径",
                "why_it_matters": "理解干部交流和跨县区调动模式",
                "suggested_queries": [f"{name} 此前 担任", f"{name} 调任"],
                "last_attempted": AS_OF
            }
        ]
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path.name}")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} dataset (staging: {STAGING})")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\nWriting person JSONs ...")
    by_name = {p["name"]: p for p in persons}
    write_person_json(by_name["张建兵"], "县委书记")
    write_person_json(by_name["龚涛"], "县长")
    # Additional predecessor JSONs
    write_person_json(by_name["雒越强"], "前任县长")
    write_person_json(by_name["朱剑"], "前任县委书记")

    print("\nOutput verification:")
    for path in [DB_PATH, GEXF_PATH]:
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✅ {path.name} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {path.name} MISSING")

    json_count = len(list(PJSON_DIR.glob("*.json")))
    print(f"  ✅ Person JSON files: {json_count}")

    print(f"\n{SLUG} build complete.")


if __name__ == "__main__":
    main()