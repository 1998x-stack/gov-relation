#!/usr/bin/env python3
"""Build 张家口市桥西区 (Zhangjiakou Qiaoxi District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 张家口市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hebei_桥西区

Research date: 2026-07-24
Official source: http://www.zjkqxq.gov.cn/ (张家口市桥西区人民政府)
Staging build: data/tmp/hebei_桥西区/ → promoted by process_tmp.py

Current status (as of 2026-07-24):
- 区委书记: 左克平 — 2026年6月前后由区长转任区委书记；
  7月1日以区委书记身份出席全区"两优一先"表彰大会；
  7月18日区第十二次党代会代表十一届区委作报告，7月19日主持闭幕大会，连任
  左克平目前仍兼任区长
- 区长: 戈录伟 — 新任区长，7月18日第十二次党代会执行主席并主持开幕式
- 前任区委书记: 尚秀伟 — 2021年5月至2026年6月任桥西区委书记，后调离（去向待查）
- 原副区长黄向义 — 2026年6月已调任张家口市住房公积金管理中心主任

Key source pages:
- http://www.zjkqxq.gov.cn/single/98/45066.html (左克平任区长时页面)
- http://www.zjkqxq.gov.cn/single/12/96126.html (第十二次党代会开幕)
- http://www.zjkqxq.gov.cn/single/11/96120.html (第十二次党代会闭幕)
- http://www.zjkqxq.gov.cn/single/22/96118.html (纪委第一次全会)
- http://www.zjkqxq.gov.cn/single/22/96017.html (两优一先表彰大会)
- http://www.zjkqxq.gov.cn/single/22/94810.html (冬春招商座谈会)
- http://www.zjkqxq.gov.cn/single/22/95505.html (尚秀伟5月仍为书记)
- http://www.zjkqxq.gov.cn/single/22/94768.html (政协十届七次会议)
- http://www.zjkqxq.gov.cn/single/98/45062.html (陈建民副区长分工)
- http://www.zjkqxq.gov.cn/single/98/45063.html (杨巍洁常务副区长分工)
- https://baike.baidu.com/item/左克平/60803340 (左克平百度百科)
- https://baike.baidu.com/item/戈录伟 (戈录伟百度百科)
- https://baike.baidu.com/item/尚秀伟 (尚秀伟百度百科)
- https://baike.baidu.hk/item/黄向义 (黄向义百度百科)
- https://baike.baidu.hk/item/杨巍洁/62303530 (杨巍洁百度百科)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "桥西区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "左克平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "河北阳原",
        "native_place": "河北阳原",
        "education": "大学",
        "party_join": "中共党员（1996年6月入党）",
        "work_start": "1997年9月",
        "current_post": "桥西区委书记（兼区长）",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("百度百科: https://baike.baidu.com/item/左克平/60803340; "
                    "官方: http://www.zjkqxq.gov.cn/single/11/96120.html"),
    },
    {
        "id": 2,
        "name": "戈录伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桥西区委副书记、区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (党代会主持); "
                    "百度百科: https://baike.baidu.com/item/戈录伟"),
    },
    {
        "id": 3,
        "name": "吉树强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会执行主席)"),
    },
    {
        "id": 4,
        "name": "胡海飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会执行主席)"),
    },
    {
        "id": 5,
        "name": "马玉红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会执行主席)"),
    },
    {
        "id": 6,
        "name": "杨建章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会执行主席)"),
    },
    {
        "id": 7,
        "name": "孙丹峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记",
        "current_org": "中共张家口市桥西区纪律检查委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/22/96118.html (纪委十二届一次全会当选书记)"),
    },
    {
        "id": 8,
        "name": "卢宗生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会执行主席)"),
    },
    {
        "id": 9,
        "name": "李艳娇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会执行主席)"),
    },
    {
        "id": 10,
        "name": "刘建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会执行主席)"),
    },
    {
        "id": 11,
        "name": "刘海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html (十二次党代会主席团成员)"),
    },
    {
        "id": 12,
        "name": "杨巍洁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45063.html (常务副区长分工及履历); "
                    "百度百科: https://baike.baidu.hk/item/杨巍洁/62303530"),
    },
    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "黄向义",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1981年11月",
        "birthplace": "",
        "native_place": "",
        "education": "河北省委党校函授法律专业",
        "party_join": "中共党员",
        "work_start": "2002年7月",
        "current_post": "原桥西区副区长（已调任市住房公积金管理中心主任）",
        "current_org": "张家口市住房公积金管理中心",
        "source": ("百度百科: https://baike.baidu.hk/item/黄向义; "
                    "官方: http://www.zjkqxq.gov.cn/single/98/55582.html"),
    },
    {
        "id": 14,
        "name": "陈建民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45062.html"),
    },
    {
        "id": 15,
        "name": "王平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（区政府党组成员）",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/60237.html"),
    },
    {
        "id": 16,
        "name": "倪明远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/55577.html (非中共党员)"),
    },
    {
        "id": 17,
        "name": "王则栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（区政府党组成员）",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45061.html"),
    },
    # ════════════════════════════════════════
    # 前任领导 & 政协
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "尚秀伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "山东德州",
        "native_place": "山东德州",
        "education": "大连理工大学动力系热能专业（工学学士）；省委党校经济管理专业研究生（在读）",
        "party_join": "中共党员（1998年6月入党）",
        "work_start": "1998年7月",
        "current_post": "前任桥西区委书记（已离任，2021.05-2026.06，去向待查）",
        "current_org": "待查（去向不明）",
        "source": ("快懂百科: https://www.baike.com/wiki/尚秀伟; "
                    "百度百科: https://baike.baidu.com/item/尚秀伟; "
                    "官方: http://www.zjkqxq.gov.cn/single/22/95505.html"),
    },
    {
        "id": 19,
        "name": "高军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/22/94768.html (政协桥西区十届七次会议)"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共张家口市桥西区委员会", "type": "党委", "level": "市辖区", "parent": "中共张家口市委员会", "location": "河北省张家口市桥西区"},
    {"id": 2, "name": "桥西区人民政府", "type": "政府", "level": "市辖区", "parent": "张家口市人民政府", "location": "河北省张家口市桥西区"},
    {"id": 3, "name": "中共张家口市桥西区纪律检查委员会", "type": "纪委", "level": "市辖区", "parent": "中共张家口市纪律检查委员会", "location": "河北省张家口市桥西区"},
    {"id": 4, "name": "桥西区人大常委会", "type": "人大", "level": "市辖区", "parent": "张家口市人大常委会", "location": "河北省张家口市桥西区"},
    {"id": 5, "name": "政协桥西区委员会", "type": "政协", "level": "市辖区", "parent": "政协张家口市委员会", "location": "河北省张家口市桥西区"},
    {"id": 6, "name": "张家口市公安局桥西分局", "type": "政府", "level": "区直部门", "parent": "张家口市公安局", "location": "河北省张家口市桥西区"},
    {"id": 7, "name": "张家口市住房公积金管理中心", "type": "事业单位", "level": "市直", "parent": "张家口市人民政府", "location": "河北省张家口市"},
    {"id": 8, "name": "中共张家口市宣化区委员会", "type": "党委", "level": "市辖区", "parent": "中共张家口市委员会", "location": "河北省张家口市宣化区"},
    {"id": 9, "name": "中共张家口市桥东区委员会", "type": "党委", "level": "市辖区", "parent": "中共张家口市委员会", "location": "河北省张家口市桥东区"},
    {"id": 10, "name": "张家口经济技术开发区", "type": "开发区", "level": "国家级", "parent": "张家口市人民政府", "location": "河北省张家口市"},
    {"id": 11, "name": "中共张家口市委社会工作部", "type": "党委", "level": "市直部门", "parent": "中共张家口市委员会", "location": "河北省张家口市"},
    {"id": 12, "name": "张家口市信访局", "type": "政府", "level": "市直部门", "parent": "张家口市人民政府", "location": "河北省张家口市"},
    {"id": 13, "name": "张家口市财政局", "type": "政府", "level": "市直部门", "parent": "张家口市人民政府", "location": "河北省张家口市"},
    {"id": 14, "name": "张家口市桥东区人民政府", "type": "政府", "level": "市辖区", "parent": "张家口市人民政府", "location": "河北省张家口市桥东区"},
    {"id": 15, "name": "空港经济开发区", "type": "开发区", "level": "省级", "parent": "张家口市人民政府", "location": "河北省张家口市桥东区"},
    {"id": 16, "name": "中共蔚县委员会", "type": "党委", "level": "县", "parent": "中共张家口市委员会", "location": "河北省张家口市蔚县"},
    {"id": 17, "name": "沽源县", "type": "政府", "level": "县", "parent": "张家口市人民政府", "location": "河北省张家口市沽源县"},
    {"id": 18, "name": "塞北管理区", "type": "开发区", "level": "县级", "parent": "张家口市人民政府", "location": "河北省张家口市塞北管理区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 左克平 — 完整履历
    {"person_id": 1, "org_id": 8, "title": "宣化区委常委、区委办公室主任", "start": "", "end": "", "rank": "副处级", "note": "区直机关党工委书记"},
    {"person_id": 1, "org_id": 8, "title": "宣化区委常委、政法委书记、统战部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "桥东区委常委、组织部长", "start": "", "end": "", "rank": "副处级", "note": "河北省桥东区驻文创商街营地指挥长"},
    {"person_id": 1, "org_id": 10, "title": "张家口经济技术开发区工委副书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "市委社会工作部副部长", "start": "", "end": "2025-02", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "市信访局局长", "start": "", "end": "2025-02", "rank": "正处级", "note": "同时任市委社工部副部长"},
    {"person_id": 1, "org_id": 1, "title": "桥西区委副书记", "start": "2025-03", "end": "2026-06", "rank": "副处级", "note": "任区长时同时任副书记"},
    {"person_id": 1, "org_id": 2, "title": "桥西区区长", "start": "2025-03", "end": "至今", "rank": "正处级", "note": "2025年3月由市委社工部副部长/信访局长调任"},
    {"person_id": 1, "org_id": 1, "title": "桥西区委书记", "start": "2026-06", "end": "至今", "rank": "正处级", "note": "2026年6月前后由区长转任；7月第十二次党代会连任；目前仍兼区长"},
    # 戈录伟 — 完整履历
    {"person_id": 2, "org_id": 16, "title": "蔚县县委常委、组织部部长", "start": "", "end": "2024-12", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "蔚县驻冬奥保障团队临时联合党委书记", "start": "", "end": "2022-04", "rank": "", "note": "蔚县包联酒店组长；冬奥会先进个人"},
    {"person_id": 2, "org_id": 1, "title": "桥西区委副书记", "start": "2025-01", "end": "至今", "rank": "副处级", "note": "2025年1月以区委副书记身份参加老干部情况通报会"},
    {"person_id": 2, "org_id": 2, "title": "桥西区区长", "start": "2026-07", "end": "至今", "rank": "正处级", "note": "第十二次党代会执行主席并主持开幕式"},
    # 区委常委
    {"person_id": 3, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 4, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 5, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 6, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 7, "org_id": 3, "title": "桥西区纪委书记", "start": "", "end": "至今", "rank": "副处级", "note": "十二届纪委第一次全会当选"},
    {"person_id": 7, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 9, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 10, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 11, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 12, "org_id": 13, "title": "市财政局农业科科长", "start": "", "end": "2022-09", "rank": "正科级", "note": ""},
    {"person_id": 12, "org_id": 13, "title": "市财政局副局长", "start": "2022-10", "end": "2024-11", "rank": "副处级", "note": "2022年10月26日市政府任命"},
    {"person_id": 12, "org_id": 2, "title": "桥西区常务副区长", "start": "2024-12", "end": "至今", "rank": "副处级", "note": "市财政局副局长转任；区委常委、区政府党组副书记"},
    {"person_id": 12, "org_id": 1, "title": "桥西区委常委", "start": "2024-12", "end": "至今", "rank": "副处级", "note": ""},
    # 副区长
    {"person_id": 13, "org_id": 17, "title": "沽源县委办公室科员", "start": "2002-07", "end": "2008-11", "rank": "科员", "note": "其间参加河北自考法律专业和省委党校函授法律专业学习"},
    {"person_id": 13, "org_id": 17, "title": "沽源县第三纪工委副书记、副局长", "start": "2008-11", "end": "2011-03", "rank": "副科级", "note": ""},
    {"person_id": 13, "org_id": 17, "title": "共青团沽源县委书记", "start": "2011-03", "end": "2015-03", "rank": "正科级", "note": ""},
    {"person_id": 13, "org_id": 17, "title": "黄盖淖镇党委副书记、镇长", "start": "2015-03", "end": "2017-09", "rank": "正科级", "note": ""},
    {"person_id": 13, "org_id": 17, "title": "高山堡乡党委书记", "start": "2017-09", "end": "2021-06", "rank": "正科级", "note": "获河北省脱贫攻坚先进个人"},
    {"person_id": 13, "org_id": 18, "title": "塞北管理区党工委委员、管委会副主任", "start": "2021-06", "end": "2023-01", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "桥西区副区长", "start": "2023", "end": "2026-06", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 13, "org_id": 7, "title": "市住房公积金管理中心主任", "start": "2026-06", "end": "至今", "rank": "正处级", "note": "2026年6月12日市政府任命"},
    {"person_id": 14, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员，兼公安分局局长"},
    {"person_id": 14, "org_id": 6, "title": "桥西公安分局局长", "start": "", "end": "至今", "rank": "正科级", "note": "党委书记、局长、督察长"},
    {"person_id": 15, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 16, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "非中共党员"},
    {"person_id": 17, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员"},
    # 前任 & 政协
    {"person_id": 18, "org_id": 14, "title": "桥东区委副书记、区长", "start": "", "end": "2021-04", "rank": "正处级", "note": "兼空港经济开发区工委副书记、管委会主任"},
    {"person_id": 18, "org_id": 15, "title": "空港经济开发区工委副书记、管委会主任", "start": "", "end": "2021-04", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "桥西区委书记", "start": "2021-05", "end": "2026-06", "rank": "正处级", "note": "2026年5月13日仍为书记；约6月离任；去向待查"},
    {"person_id": 19, "org_id": 5, "title": "桥西区政协主席", "start": "", "end": "至今", "rank": "正处级", "note": "政协桥西区第十届委员会主席、党组书记"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档关系，共同担任第十二次党代会执行主席", "overlap_org": "桥西区", "overlap_period": "2026-"},
    # 前任书记关系
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "左克平接替尚秀伟任桥西区委书记", "overlap_org": "中共桥西区委", "overlap_period": "2026-06"},
    {"person_a": 18, "person_b": 1, "type": "superior_subordinate", "context": "尚秀伟为区委书记时左克平为区长", "overlap_org": "中共桥西区委/区政府", "overlap_period": "2025-03至2026-06"},
    # 左克平 — 组织部与宣化系
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "左克平曾任桥东区委组织部长，杨建章在桥东系任职可能相关", "overlap_org": "桥东区", "overlap_period": ""},
    # 戈录伟 — 蔚县系
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "戈录伟曾任蔚县常委，王平分工涉及农业农村与桥西区下辖的东窑子镇", "overlap_org": "", "overlap_period": ""},
    # 区委书记与常委班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与纪委书记", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委书记与常务副区长", "overlap_org": "中共桥西区委/区政府", "overlap_period": ""},
    # 区长与副区长
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区长与常务副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区长与副区长工作搭档（黄向义已调离）", "overlap_org": "桥西区政府", "overlap_period": "至2026-06"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    # 前任书记与班子成员
    {"person_a": 18, "person_b": 12, "type": "overlap", "context": "前任书记与常务副区长", "overlap_org": "中共桥西区委", "overlap_period": ""},
    # 杨巍洁与财政局系统
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "常务副区长与副区长，市政府系统先后关系", "overlap_org": "张家口市政府", "overlap_period": ""},
    # 尚秀伟的桥东区系 — 他与左克平曾在同一区工作
    {"person_a": 18, "person_b": 1, "type": "same_system", "context": "尚秀伟曾任桥东区长，左克平曾任桥东区委组织部长，但时间是否重叠待查", "overlap_org": "桥东区", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    """Build source register from existing build script sources."""
    return [
        {"id":"S001","title":"桥西区政府—左克平页","url":"http://www.zjkqxq.gov.cn/single/98/45066.html","publisher":"桥西区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S002","title":"第十二次党代会开幕","url":"http://www.zjkqxq.gov.cn/single/12/96126.html","publisher":"桥西区人民政府","published_at":"2026-07-18","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"左克平作报告，戈录伟主持"},
        {"id":"S003","title":"第十二次党代会闭幕","url":"http://www.zjkqxq.gov.cn/single/11/96120.html","publisher":"桥西区人民政府","published_at":"2026-07-19","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"左克平主持闭幕大会"},
        {"id":"S004","title":"纪委第一次全会","url":"http://www.zjkqxq.gov.cn/single/22/96118.html","publisher":"桥西区人民政府","published_at":"2026-07-19","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"孙丹峰当选纪委书记"},
        {"id":"S005","title":"两优一先表彰大会","url":"http://www.zjkqxq.gov.cn/single/22/96017.html","publisher":"桥西区人民政府","published_at":"2026-07-01","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"左克平以书记身份出席"},
        {"id":"S006","title":"冬春招商座谈会","url":"http://www.zjkqxq.gov.cn/single/22/94810.html","publisher":"桥西区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S007","title":"尚秀伟5月仍为书记","url":"http://www.zjkqxq.gov.cn/single/22/95505.html","publisher":"桥西区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S008","title":"政协十届七次会议","url":"http://www.zjkqxq.gov.cn/single/22/94768.html","publisher":"桥西区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S009","title":"陈建民副区长分工","url":"http://www.zjkqxq.gov.cn/single/98/45062.html","publisher":"桥西区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S010","title":"杨巍洁常务副区长分工","url":"http://www.zjkqxq.gov.cn/single/98/45063.html","publisher":"桥西区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S011","title":"左克平百度百科","url":"https://baike.baidu.com/item/左克平/60803340","publisher":"百度百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":""},
        {"id":"S012","title":"戈录伟百度百科","url":"https://baike.baidu.com/item/戈录伟","publisher":"百度百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":""},
        {"id":"S013","title":"尚秀伟百度百科","url":"https://baike.baidu.com/item/尚秀伟","publisher":"百度百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":""},
        {"id":"S014","title":"黄向义百度百科","url":"https://baike.baidu.hk/item/黄向义","publisher":"百度百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":""},
        {"id":"S015","title":"杨巍洁百度百科","url":"https://baike.baidu.hk/item/杨巍洁/62303530","publisher":"百度百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":""},
    ]

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "张家口市",
            "region": "桥西区",
            "job": p.get("current_post",""),
            "task_id": "hebei_桥西区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"qiaoxiqu_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": p.get("native_place",""),
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p.get("current_post",""),
            "current_org": p.get("current_org",""),
            "administrative_rank": "县处级正职" if ("书记" in p.get("current_post","") and "副" not in p.get("current_post","") and "纪委" not in p.get("current_post","")) or ("区长" in p.get("current_post","") and "副" not in p.get("current_post","") and "人大" not in p.get("current_post","")) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"confirmed","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息有待补充" if not p.get("birth") else f"{p['name']}早期职业生涯需确认"
        },
        "open_questions": [
            {"priority":"critical" if not p.get("birth") else "medium",
             "question": f"{p['name']}的完整职业生涯履历",
             "why_it_matters": "无法追溯其任职路径和系统经历",
             "suggested_queries": [f"{p['name']} 简历 桥西区",f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  张家口市桥西区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24（三次调查，含完整履历更新）")
    print("  信息来源: 桥西区政府网站 + 百度百科")
    print("=" * 60)

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
    print(f"\n✅ 桥西区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 左克平 (区委书记兼区长)
    zuo_timeline = [
        {"start":"","end":"","org":"中共张家口市宣化区委员会","title":"宣化区委常委、区委办公室主任","notes":"区直机关党工委书记","confidence":"confirmed","source_ids":["S011"]},
        {"start":"","end":"","org":"中共张家口市宣化区委员会","title":"宣化区委常委、政法委书记、统战部部长","notes":"","confidence":"confirmed","source_ids":["S011"]},
        {"start":"","end":"","org":"中共张家口市桥东区委员会","title":"桥东区委常委、组织部长","notes":"","confidence":"confirmed","source_ids":["S011"]},
        {"start":"","end":"","org":"张家口经济技术开发区","title":"张家口经济技术开发区工委副书记","notes":"","confidence":"confirmed","source_ids":["S011"]},
        {"start":"","end":"2025-02","org":"中共张家口市委社会工作部","title":"市委社会工作部副部长","notes":"","confidence":"confirmed","source_ids":["S011"]},
        {"start":"","end":"2025-02","org":"张家口市信访局","title":"市信访局局长","notes":"同时任市委社工部副部长","confidence":"confirmed","source_ids":["S011"]},
        {"start":"2025-03","end":"2026-06","org":"中共张家口市桥西区委员会","title":"桥西区委副书记","notes":"任区长时同时任副书记","confidence":"confirmed","source_ids":["S001","S011"]},
        {"start":"2025-03","end":"","org":"桥西区人民政府","title":"桥西区区长","notes":"2025年3月由市委社工部副部长/信访局长调任","confidence":"confirmed","source_ids":["S001","S011"]},
        {"start":"2026-06","end":"","org":"中共张家口市桥西区委员会","title":"桥西区委书记","notes":"2026年6月由区长转任；7月第十二次党代会连任；目前仍兼区长","confidence":"confirmed","source_ids":["S002","S003","S005","S011"]},
    ]
    zuo_relationships = [
        {"person":"戈录伟","person_id":"qiaoxiqu_戈录伟","relationship_type":"overlap","strength":"strong","evidence":"区委书记与区长党政工作搭档关系，共同担任第十二次党代会执行主席","overlap_org":"桥西区","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"尚秀伟","person_id":"qiaoxiqu_尚秀伟","relationship_type":"predecessor_successor","strength":"strong","evidence":"左克平接替尚秀伟任桥西区委书记","overlap_org":"中共桥西区委","overlap_period":"2026-06","direction":"undirected","confidence":"confirmed","source_ids":["S003","S007"]},
        {"person":"尚秀伟","person_id":"qiaoxiqu_尚秀伟","relationship_type":"superior_subordinate","strength":"strong","evidence":"尚秀伟为区委书记时左克平为区长","overlap_org":"中共桥西区委/区政府","overlap_period":"2025-03至2026-06","direction":"other_to_person","confidence":"confirmed","source_ids":["S001","S007"]},
        {"person":"杨巍洁","person_id":"qiaoxiqu_杨巍洁","relationship_type":"overlap","strength":"strong","evidence":"区委书记与常务副区长工作搭档","overlap_org":"中共桥西区委/区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S010"]},
    ]
    zuo_json = make_person_json(persons[0], zuo_timeline, zuo_relationships, source_register)
    zuo_path = PERSONS_DIR / f"{TODAY}-河北省-张家口市-区委书记-左克平.json"
    with open(zuo_path, "w", encoding="utf-8") as f:
        json.dump(zuo_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zuo_path.name}")

    # 2. 戈录伟 (区长)
    ge_timeline = [
        {"start":"","end":"2024-12","org":"中共蔚县委员会","title":"蔚县县委常委、组织部部长","notes":"","confidence":"confirmed","source_ids":["S002","S012"]},
        {"start":"","end":"2022-04","org":"中共蔚县委员会","title":"蔚县驻冬奥保障团队临时联合党委书记","notes":"蔚县包联酒店组长；冬奥会先进个人","confidence":"confirmed","source_ids":["S012"]},
        {"start":"2025-01","end":"","org":"中共张家口市桥西区委员会","title":"桥西区委副书记","notes":"2025年1月以区委副书记身份参加老干部情况通报会","confidence":"confirmed","source_ids":["S012"]},
        {"start":"2026-07","end":"","org":"桥西区人民政府","title":"桥西区区长","notes":"第十二次党代会执行主席并主持开幕式","confidence":"confirmed","source_ids":["S002"]},
    ]
    ge_relationships = [
        {"person":"左克平","person_id":"qiaoxiqu_左克平","relationship_type":"overlap","strength":"strong","evidence":"区长与区委书记党政工作搭档","overlap_org":"桥西区","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"杨巍洁","person_id":"qiaoxiqu_杨巍洁","relationship_type":"overlap","strength":"medium","evidence":"区长与常务副区长工作搭档","overlap_org":"桥西区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S010"]},
    ]
    ge_json = make_person_json(persons[1], ge_timeline, ge_relationships, source_register)
    ge_path = PERSONS_DIR / f"{TODAY}-河北省-张家口市-区长-戈录伟.json"
    with open(ge_path, "w", encoding="utf-8") as f:
        json.dump(ge_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {ge_path.name}")

    # 3. 尚秀伟 (前任区委书记)
    shang_timeline = [
        {"start":"","end":"2021-04","org":"张家口市桥东区人民政府","title":"桥东区委副书记、区长","notes":"兼空港经济开发区工委副书记、管委会主任","confidence":"confirmed","source_ids":["S013"]},
        {"start":"","end":"2021-04","org":"空港经济开发区","title":"空港经济开发区工委副书记、管委会主任","notes":"","confidence":"confirmed","source_ids":["S013"]},
        {"start":"2021-05","end":"2026-06","org":"中共张家口市桥西区委员会","title":"桥西区委书记","notes":"2026年5月13日仍为书记；约6月离任","confidence":"confirmed","source_ids":["S007","S013"]},
    ]
    shang_relationships = [
        {"person":"左克平","person_id":"qiaoxiqu_左克平","relationship_type":"superior_subordinate","strength":"strong","evidence":"尚秀伟为区委书记时左克平为区长","overlap_org":"中共桥西区委/区政府","overlap_period":"2025-03至2026-06","direction":"person_to_other","confidence":"confirmed","source_ids":["S001","S007"]},
    ]
    shang_json = make_person_json(persons[17], shang_timeline, shang_relationships, source_register)
    shang_path = PERSONS_DIR / f"{TODAY}-河北省-张家口市-区委书记-尚秀伟.json"
    with open(shang_path, "w", encoding="utf-8") as f:
        json.dump(shang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {shang_path.name}")

    # 4. 黄向义 (原副区长，已调任)
    huang_timeline = [
        {"start":"2002-07","end":"2008-11","org":"沽源县委办公室","title":"科员","notes":"参加河北自考法律专业和省委党校函授法律专业学习","confidence":"confirmed","source_ids":["S014"]},
        {"start":"2008-11","end":"2011-03","org":"沽源县第三纪工委","title":"副书记、副局长","notes":"","confidence":"confirmed","source_ids":["S014"]},
        {"start":"2011-03","end":"2015-03","org":"共青团沽源县委","title":"书记","notes":"","confidence":"confirmed","source_ids":["S014"]},
        {"start":"2015-03","end":"2017-09","org":"沽源县黄盖淖镇","title":"党委副书记、镇长","notes":"","confidence":"confirmed","source_ids":["S014"]},
        {"start":"2017-09","end":"2021-06","org":"沽源县高山堡乡","title":"党委书记","notes":"获河北省脱贫攻坚先进个人","confidence":"confirmed","source_ids":["S014"]},
        {"start":"2021-06","end":"2023-01","org":"塞北管理区","title":"党工委委员、管委会副主任","notes":"","confidence":"confirmed","source_ids":["S014"]},
        {"start":"2023","end":"2026-06","org":"桥西区人民政府","title":"桥西区副区长","notes":"区政府党组成员","confidence":"confirmed","source_ids":["S014"]},
        {"start":"2026-06","end":"","org":"张家口市住房公积金管理中心","title":"主任","notes":"2026年6月12日市政府任命","confidence":"confirmed","source_ids":["S014"]},
    ]
    huang_relationships = [
        {"person":"戈录伟","person_id":"qiaoxiqu_戈录伟","relationship_type":"overlap","strength":"medium","evidence":"区长与副区长工作搭档","overlap_org":"桥西区政府","overlap_period":"至2026-06","direction":"undirected","confidence":"confirmed","source_ids":["S014"]},
    ]
    huang_json = make_person_json(persons[12], huang_timeline, huang_relationships, source_register)
    huang_path = PERSONS_DIR / f"{TODAY}-河北省-张家口市-副区长-黄向义.json"
    with open(huang_path, "w", encoding="utf-8") as f:
        json.dump(huang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {huang_path.name}")

    # 5. 杨巍洁 (常务副区长)
    yang_timeline = [
        {"start":"","end":"2022-09","org":"张家口市财政局","title":"农业科科长","notes":"","confidence":"confirmed","source_ids":["S010","S015"]},
        {"start":"2022-10","end":"2024-11","org":"张家口市财政局","title":"副局长","notes":"2022年10月26日市政府任命","confidence":"confirmed","source_ids":["S010","S015"]},
        {"start":"2024-12","end":"","org":"桥西区人民政府","title":"常务副区长","notes":"市财政局副局长转任；区委常委、区政府党组副书记","confidence":"confirmed","source_ids":["S010","S015"]},
    ]
    yang_relationships = [
        {"person":"左克平","person_id":"qiaoxiqu_左克平","relationship_type":"overlap","strength":"medium","evidence":"常务副区长与区委书记工作搭档","overlap_org":"中共桥西区委/区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S010"]},
        {"person":"戈录伟","person_id":"qiaoxiqu_戈录伟","relationship_type":"overlap","strength":"medium","evidence":"常务副区长与区长工作搭档","overlap_org":"桥西区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S010"]},
    ]
    yang_json = make_person_json(persons[11], yang_timeline, yang_relationships, source_register)
    yang_path = PERSONS_DIR / f"{TODAY}-河北省-张家口市-常务副区长-杨巍洁.json"
    with open(yang_path, "w", encoding="utf-8") as f:
        json.dump(yang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {yang_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")

if __name__ == "__main__":
    build()
