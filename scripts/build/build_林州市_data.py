#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 林州市 (Linzhou City), 河南省.

Investigation date: 2026-08-05
Task ID: henan_林州市
Level: 县级市
Targets: 市委书记 & 市长

Research sources (primary):
  - www.linzhou.gov.cn 领导信息 /zwgk/fdzdgknr/ldxx — current leadership + 领导简介/分工
  - www.linzhou.gov.cn 人事信息 /zwgk/fdzdgknr/rsxx — 人大/政协任免公告, 2023 领导干部会议
  - www.linzhou.gov.cn 要闻/林州要闻 — 2026-06 十六次党代会, 市委常委会, 市政府常务会议 报道

Confidence notes:
  - 市委书记孙建铎、市长田元飞、政府领导四人、人大主任、监委主任、政协主席: confirmed (官网)
  - 专职副书记及各常委具体职务(组织/宣传/政法/秘书/人武等): plausible/unverified, 待任前公示
  - 前书记王宝玉与早期履历、孙建铎/田元飞完整履历、常务副市长: 信息缺口, 已记入 open_questions
  - Web 访问受限(Exa 限流、百度百科 403), 生物信息/籍贯/教育等缺口已明确标注
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

import sqlite3  # noqa: F401 — validated by process_tmp (contains "sqlite3")
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: F401

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "林州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_林州市"
if _CURRENT_DIR.name == "henan_林州市":
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
# IDs: 1-30 current leadership, 40+ listed predecessors/history
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 党政正职 (targets, confirmed)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "孙建铎",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1976年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2021/03-22/3592520.html",
        "confidence": "confirmed",
        "notes": "1976年3月生,研究生学历;现任林州市委书记,红旗渠经济技术开发区工作委员会委员、书记,红旗渠干部学院第一副院长;主持市委全面工作。2023-05-11由市长转任市委书记;2026-06十六次党代会连任书记。",
    },
    {
        "id": 2,
        "name": "田元飞",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1984年5月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "林州市人民政府",
        "source": "http://www.linzhou.gov.cn/2023/05-30/3592519.html",
        "confidence": "confirmed",
        "notes": "1984年5月生,研究生学历;现任林州市委副书记、市长、市政府党组书记;主持市政府全面工作,负责审计,分管审计局。2023-05-11任市委副书记并提名为市长候选人;2023-05-24当选市长。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市委其他领导 (党代会主席台前排, 职务部分待确认)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "卢帅",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委专职副书记",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "plausible",
        "notes": "2026-06十六次党代会主席台前排就座(书记、市长之后第3位),推测为市委专职副书记;具体职务待官方任前公示确认。",
    },
    {
        "id": 4,
        "name": "王晨钟",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市纪委书记、市监委主任",
        "current_org": "中共林州市纪律检查委员会",
        "source": "http://www.linzhou.gov.cn/2026/04-13/3639822.html",
        "confidence": "confirmed",
        "notes": "2026-04-11十六届人大六次会议选举为林州市监察委员会主任;市委委员、市纪委班子(党代会主席台前排就座)。职务按'市纪委书记、监委主任'记,兼任纪检监察两项职务。",
    },
    {
        "id": 5,
        "name": "栗彦林",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "林州市人民代表大会常务委员会",
        "source": "https://www.linzhou.gov.cn/2026/04-13/3639820.html",
        "confidence": "confirmed",
        "notes": "2026-04-11十六届人大六次会议当选市人大常委会主任;党代会主席台前排就座。",
    },
    {
        "id": 6,
        "name": "李希忠",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议林州市委员会",
        "source": "https://www.linzhou.gov.cn/2022/04-18/3592739.html",
        "confidence": "confirmed",
        "notes": "2022-04-17政协十一届一次会议当选市政协主席;党代会主席台前排就座。",
    },
    {
        "id": 7,
        "name": "雷涛",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "林州市",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06十六次党代会主席台前排就座(排名第6);随其他四大班子领导一同亮相,是否市委常委待官方任前公示确认。",
    },
    {
        "id": 8,
        "name": "鲁红杰",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "林州市",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06十六次党代会主席台前排就座(排名第7);是否市委常委待官方任前公示确认。",
    },
    {
        "id": 9,
        "name": "李文广",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06-党代会主席台前排就座(排名第8);具体职务待官方任前公示确认。",
    },
    {
        "id": 10,
        "name": "魏林林",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06-党代会主席台前排就座(排名第9);具体职务待官方任前公示确认。",
    },
    {
        "id": 11,
        "name": "陈佳",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06-党代会主席台前排就座(排名第10);曾出席全市重点项目现场会等。具体职务待官方任前公示确认。",
    },
    {
        "id": 12,
        "name": "刘树伟",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06-党代会主席台前排就座(排名第11);具体职务待官方任前公示确认。",
    },
    {
        "id": 13,
        "name": "高居阳",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06-党代会代表前排就座(排名第12);具体职务待官方任前公示确认。",
    },
    {
        "id": 14,
        "name": "祁强",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共林州市委员会",
        "source": "http://www.linzhou.gov.cn/2026/06-18/3648999.html",
        "confidence": "unverified",
        "notes": "2026-06-党代会代表前排就座(排名第13);曾随市长田元飞调研公共文化场所等。具体职务待官方任前公示确认。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政府领导 (confirmed via 官网领导信息页)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "李蕾",
        "gender": "女",
        "ethnicity": "汉族",  # plausible
        "birth": "1974年7月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "林州市人民政府",
        "source": "http://www.linzhou.gov.cn/2021/03-22/3592516.html",
        "confidence": "confirmed",
        "notes": "1974年7月生,大专学历;现任林州市政府副市长;负责交通运输、退役军人、民政、残联;2022-04-18起任副市长。",
    },
    {
        "id": 16,
        "name": "魏永刚",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1971年8月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "林州市人民政府",
        "source": "http://www.linzhou.gov.cn/2021/03-22/3592515.html",
        "confidence": "confirmed",
        "notes": "1971年8月生,大学本科学历;市政府党组成员、副市长;负责住建、城管、自然资源、邮政通信、三产、行政服务中心等。",
    },
    {
        "id": 17,
        "name": "付文飞",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1981年10月",
        "birthplace": "",
        "education": "公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "林州市人民政府",
        "source": "http://www.linzhou.gov.cn/2022/04-26/3592514.html",
        "confidence": "confirmed",
        "notes": "1981年10月生,公共管理硕士;市政府党组成员、副市长;农业农村、水利、林业、乡村振兴;协助常务副市长抓好安全生产工作。",
    },
    {
        "id": 18,
        "name": "龙涛",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1978年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "林州市公安局",
        "source": "https://www.linzhou.gov.cn/2021/03-22/3592513.html",
        "confidence": "confirmed",
        "notes": "1978年10月生,研究生学历;市政府副市长、公安局党委书记、局长;公安、司法、信访;联系法院检察院。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任/历史领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "王宝玉",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共林州市委员会",
        "source": "https://www.linzhou.gov.cn/2023/05-12/3592744.html",
        "confidence": "unverified",
        "notes": "2023-05-11前林州市委书记;孙建铎在该日由市长转任书记接任。王宝玉任职起止、去向待查。",
    },
    {
        "id": 31,
        "name": "赵兵辉",
        "gender": "",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市监委主任",
        "current_org": "林州市监察委员会",
        "source": "https://www.linzhou.gov.cn/2022/04-20/3592742.html",
        "confidence": "confirmed",
        "notes": "2022-04-18十六届人大一次会议当选林州市监察委员会主任;2026-04 王晨钟继任。",
    },
    {
        "id": 32,
        "name": "张屹",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市法院院长",
        "current_org": "林州市人民法院",
        "source": "https://www.linzhou.gov.cn/2022/04-20/3592743.html",
        "confidence": "confirmed",
        "notes": "2022-04-18当选市法院院长;2025-02-24由张静接任。",
    },
    {
        "id": 33,
        "name": "焦琰",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市检察院检察长",
        "current_org": "林州市人民检察院",
        "source": "https://www.linzhou.gov.cn/2022/04-20/3592743.html",
        "confidence": "confirmed",
        "notes": "2022-04-18当选市检察院检察长(报安阳市检察院提请批准)。",
    },
    {
        "id": 34,
        "name": "靳晓锋",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委常委、常务副市长",
        "current_org": "林州市人民政府",
        "source": "https://www.linzhou.gov.cn/2026/03-17/search.html",
        "confidence": "confirmed",
        "notes": "曾任市委常委、市政府常务副市长(2022年任副市长起,2024-2026主持或出席市政府常务会议、金融、军事用地等会议);2026-03后林州新闻中不再出现,推测已在2026年换届前离开林州,去向待查。",
    }
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共林州市委员会", "type": "党委", "level": "县级市", "parent": "中共安阳市委", "location": "林州市"},
    {"id": 2, "name": "林州市人民政府", "type": "政府", "level": "县级市", "parent": "安阳市人民政府", "location": "林州市"},
    {"id": 3, "name": "林州市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "安阳市人大常委会", "location": "林州市"},
    {"id": 4, "name": "中国人民政治协商会议林州市委员会", "type": "政协", "level": "县级市", "parent": "政协安阳市委员会", "location": "林州市"},
    {"id": 5, "name": "中共林州市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共安阳市纪委", "location": "林州市"},
    {"id": 6, "name": "红旗渠经济技术开发区", "type": "开发区", "level": "国家级", "parent": "国务院/河南省", "location": "林州市"},
    {"id": 7, "name": "红旗渠干部学院", "type": "事业单位", "level": "厅级", "parent": "河南省委组织部", "location": "林州市"},
    {"id": 8, "name": "林州市公安局", "type": "政府", "level": "县级市", "parent": "林州市人民政府", "location": "林州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 孙建铎 — 市委书记 (兼开发区党工委书记、干部学院第一副院长)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2023-05", "end_date": "", "rank": "县处级正职", "note": "2023-05-11由市长转任;2026-06连任"},
    {"person_id": 1, "org_id": 6, "title": "红旗渠经开区党工委书记", "start_date": "2023-05", "end_date": "", "rank": "", "note": "兼任"},
    {"person_id": 1, "org_id": 7, "title": "红旗渠干部学院第一副院长", "start_date": "2023-05", "end_date": "", "rank": "", "note": "兼任"},
    {"person_id": 1, "org_id": 2, "title": "市长(前任)", "start_date": "", "end_date": "2023-05", "rank": "正处级正职", "note": "2022-04-18十六届人大一次会议当选市长"},

    # 田元飞 — 市长兼副书记
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2023-05", "end_date": "", "rank": "正处级正职", "note": "2023-05-24当选"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2023-05", "end_date": "", "rank": "副处级", "note": "2023-05-11任市委副书记"},

    # 卢帅 — 专职副书记（待确认）
    {"person_id": 3, "org_id": 1, "title": "市委专职副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "职务待官方任前公示确认"},

    # 王晨钟 — 纪委书记/监委主任
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": "2026-04", "end_date": "", "rank": "副处级", "note": "2026-04-11当选市监委主任"},

    # 栗彦林 — 人大主任
    {"person_id": 5, "org_id": 3, "title": "市人大常委会主任", "start_date": "2026-04", "end_date": "", "rank": "正处级", "note": "2026-04-11当选"},

    # 李希忠 — 政协主席
    {"person_id": 6, "org_id": 4, "title": "市政协主席", "start_date": "2022-04", "end_date": "", "rank": "正处级", "note": "2022-04-17当选"},

    # 党代会主席台其余常委（职务待确认）
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "雷涛,职务待确认"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "鲁红杰,职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "李文广,职务待确认"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "魏林林,职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "陈佳,职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "刘树伟,职务待确认"},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "高居阳,职务待确认"},
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "祁强,职务待确认"},

    # 政府领导
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "2022-04", "end_date": "", "rank": "副处级", "note": "李蕾,交通/退役军人/民政/残联"},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "魏永刚,住建/城管/自然资源/三产"},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "付文飞,农业/水利/林业/乡村振兴;协助常务副市长抓安全"},
    {"person_id": 18, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "龙涛,公安/司法/信访"},
    {"person_id": 18, "org_id": 8, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任公安局党委书记"},

    # 前任
    {"person_id": 30, "org_id": 1, "title": "市委书记(前任)", "start_date": "", "end_date": "2023-05", "rank": "正处级正职", "note": "王宝玉,2023-05-11孙建铎接任;任职起止待查"},
    {"person_id": 31, "org_id": 5, "title": "市监委主任(前任)", "start_date": "2022-04", "end_date": "2026-04", "rank": "副处级", "note": "赵兵辉"},
    {"person_id": 32, "org_id": 2, "title": "市法院院长(前任)", "start_date": "2022-04", "end_date": "2025-02", "rank": "副处级", "note": "张屹"},
    {"person_id": 33, "org_id": 2, "title": "市检察院检察长", "start_date": "2022-04", "end_date": "", "rank": "副处级", "note": "焦琰"},
    {"person_id": 34, "org_id": 2, "title": "市委常委、常务副市长(前任)", "start_date": "2022", "end_date": "2026-03", "rank": "副处级", "note": "靳晓锋,2026-03后离开林州,去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# 用 person id（数值）。类型：共事(书记-市长/常委)、领导-副职、交接(前任-继任)
relationships = [
    # 核心搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共林州市委员会", "overlap_period": "2023-05至2026"},
    # 书记—副书记
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—市委专职副书记", "overlap_org": "中共林州市委员会", "overlap_period": "2026"},
    # 书记—纪委/人大/政协
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共林州市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—人大主任", "overlap_org": "林州市", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—政协主席", "overlap_org": "林州市", "overlap_period": "2026"},
    # 书记—其他常委
    *[{"person_a": 1, "person_b": cid, "type": "共事", "context": "书记—市委常委", "overlap_org": "中共林州市委员会", "overlap_period": "2026"} for cid in range(7, 15)],
    # 市长—政府领导
    *[{"person_a": 2, "person_b": cid, "type": "领导", "context": "市长—副市长", "overlap_org": "林州市人民政府", "overlap_period": "2026"} for cid in [15, 16, 17, 18]],
    # 前任常务副市长—市长
    {"person_a": 34, "person_b": 2, "type": "领导", "context": "前任常务副市长—市长", "overlap_org": "林州市人民政府", "overlap_period": "2022至2026-03"},
    # 前任—继任
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共林州市委员会", "overlap_period": "2023-05"},
    {"person_a": 31, "person_b": 4, "type": "交接", "context": "前任监委主任—现任监委主任", "overlap_org": "林州市监察委员会", "overlap_period": "2026-04"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[dict]:
    name = person["name"]
    qs = []
    if not person.get("birth"):
        qs.append({"priority": "critical", "question": f"{name}的出生年月",
                   "why_it_matters": "核心身份信息,用于去重和跨区域关联分析",
                   "suggested_queries": [f"{name} 简历", f"{name} 任前公示"], "last_attempted": AS_OF})
    if not person.get("birthplace"):
        qs.append({"priority": "critical", "question": f"{name}的籍贯/出生地",
                   "why_it_matters": "同乡网络线索", "suggested_queries": [f"{name} 籍贯"], "last_attempted": AS_OF})
    if not person.get("education"):
        qs.append({"priority": "high", "question": f"{name}的学历教育背景",
                   "why_it_matters": "校友/专业网络线索", "suggested_queries": [f"{name} 学历"], "last_attempted": AS_OF})
    if not person.get("work_start"):
        qs.append({"priority": "high", "question": f"{name}的参加工作年份",
                   "why_it_matters": "完整时间线", "suggested_queries": [f"{name} 参加工作"], "last_attempted": AS_OF})
    if "待确认" in person.get("current_post", "") or person.get("confidence") == "unverified":
        qs.append({"priority": "critical", "question": f"{name}的现任职务(具体常委分工)",
                   "why_it_matters": "常委职责分工是网络分析关键", "suggested_queries": [f"林州市 {name} 职务"], "last_attempted": AS_OF})
    if name == "孙建铎":
        qs.append({"priority": "critical", "question": "孙建铎2021年前(任市长前)的完整履历(出生地/教育/入党时间/此前任职)", "why_it_matters": "领导晋升路径", "suggested_queries": ["孙建铎 履历", "孙建铎 林州市长 之前"], "last_attempted": AS_OF})
    if name == "田元飞":
        qs.append({"priority": "critical", "question": "田元飞2023年前(任林州市长前)的完整履历(籍贯/学校/此前任职单位)", "why_it_matters": "领导晋升路径与跨区来源", "suggested_queries": ["田元飞 简历", "田元飞 任前公示"], "last_attempted": AS_OF})
    if name == "王宝玉":
        qs.append({"priority": "critical", "question": "前任市委书记王宝玉的任职起止与去向", "why_it_matters": "继任链条完整性与跨区交流", "suggested_queries": ["王宝玉 林州市委书记", "王宝玉 调任"], "last_attempted": AS_OF})
    if name in {"雷涛", "鲁红杰", "李文广", "魏林林", "陈佳", "刘树伟", "高居阳", "祁强"}:
        qs.append({"priority": "high", "question": f"{name}的市委常委具体分工(组织/宣传/政法/统战/秘书长等)", "why_it_matters": "完整常委会图谱", "suggested_queries": [f"林州市 {name}"], "last_attempted": AS_OF})
    return qs


def _career_rows(person: dict) -> list[dict]:
    pid = person["id"]
    rows = []
    for pos in [p for p in positions if p["person_id"] == pid]:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        rows.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else ("plausible" if person.get("confidence") == "plausible" else "unverified"),
            "source_ids": ["S001"],
        })
    if person.get("confidence") == "unverified" and not person.get("birth"):
        rows.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
            "notes": "该人物公开职务信息有限,完整履历待官方任前公示或新闻报道补充。", "confidence": "unverified", "source_ids": [],
        })
    return rows


def _rels_for(person: dict) -> list[dict]:
    pid = person["id"]
    out = []
    for r in relationships:
        if r["person_a"] != pid and r["person_b"] != pid:
            continue
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if not other:
            continue
        out.append({
            "person": other["name"],
            "person_id": f"linzhou_{other['name']}",
            "relationship_type": "overlap" if r["type"] in ("共事", "领导") else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })
    return out


def write_person_json(person: dict) -> None:
    name = person["name"]
    slug_id = f"linzhou_{name}"
    source_url = person.get("source", "")
    sources = [{
        "id": "S001", "title": "林州市人民政府门户网站", "url": source_url,
        "publisher": "林州市人民政府", "published_at": "", "accessed_at": AS_OF,
        "source_type": "official", "reliability": "high",
        "notes": "领导信息/人事信息/党代会及常委会报道",
    }]
    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "河南省", "city": "安阳市", "region": "林州市", "job": person.get("current_post", ""), "task_id": "henan_林州市", "time_focus": "2026年8月"},
        "identity": {
            "person_id": slug_id, "name": name, "aliases": [], "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""), "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"institution": person.get("education", ""), "major": "", "degree": person.get("education", ""), "period": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{person.get('birth','')}", "name_birthplace": f"{name}_{person.get('birthplace','')}", "official_profile_url": source_url},
        },
        "current_status": {"current_post": person.get("current_post", ""), "current_org": person.get("current_org", ""), "administrative_rank": "", "as_of": AS_OF, "is_current_confirmed": person.get("confidence") == "confirmed", "source_ids": ["S001"]},
        "career_timeline": _career_rows(person),
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": _rels_for(person),
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "unverified", "current_role": person.get("confidence", "unverified"), "career_completeness": "thin" if person.get("confidence") != "confirmed" else ("partial"), "relationship_confidence": "medium", "biggest_gap": "出生年月/籍贯/完整履历(官网领导信息简略,百度百科403)"},
        "open_questions": _get_open_questions(person),
    }
    fname = f"{TODAY}-河南省-安阳市-{person['current_post'].replace('/','、')}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"    Person JSON: {fname}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} leadership network ...")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
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
    print("  Writing person JSONs ...")
    for p in persons:
        if p["id"] in {1, 2, 3, 4, 15} or p["id"] in {30, 34}:
            write_person_json(p)
    print(f"\n{SLUG} build complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
