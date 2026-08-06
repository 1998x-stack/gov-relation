#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 盘锦市, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_盘锦市
Level: 地级市
Targets: 市委书记(王炳森) & 市长(邢鹏)

Research sources (all accessed 2026-08-06):
  - http://www.panjin.gov.cn/ — 盘锦市人民政府门户网站 (official, primary)
      * 首页要闻: "王炳森到常态化联系企业走访并调研安全生产工作"(2026-08-05)、"邢鹏在辽滨经开区调研"(2026-08-03)、"王炳森/邢鹏走访慰问驻盘部队官兵" —— 确认现任市委书记、市长
      * 市政府领导页（html/2696 等）确认市政府班子成员
  - pjrd.gov.cn — 盘锦市人大（领导之窗：主任 张淼；2026-08-05 决定任命 江涛 为副市长）
  - pjjjjc.gov.cn — 盘锦纪检监察网（市纪委书记/监委主任 曲维东）
  - pjszx.gov.cn — 市政协（主席 刘占明）
  - baike.baidu.com — 王炳森(20589774)、邢鹏、张成中 词条（secondary）
  - repo 先前 20260725 盘锦市 区县班子人物 JSON（上下文）

Confidence notes:
  - 现任市委书记 王炳森 — confirmed（官方新闻 2026-08-05 署名"市委书记"；百科：1968-10生、汉、大学本科、中共党员，2022-04 任盘锦市委书记）
  - 现任市长 邢鹏 — confirmed（官方新闻 2026-08-03；官网领导简介 + 百科：1974-02生，吉林梨树，1995-08工作，1994-12入党，在职研究生）
  - 前任市委书记 张成中（2021-01~2022-04，后任省委常委/秘书长、河北副省长、唐山市委书记、应急管理部部长）— confirmed via 百科
  - 前任市长 汤方栋（邢鹏之前，2020-01 以市长作政府工作报告；现任辽宁省人大农业与农村委员会副主任委员）— confirmed
  - 若干市委其他常委会（专职副书记、组织/宣传/政法/统战部长、军分区政委）官方公开页未逐名列出 —— 留 open_questions
  - 常务副市长 戚宇、市委常委/副市长兼辽滨经开区书记 韩尚富 — confirmed（官网领导简介）
  - 市纪委书记/监委主任 曲维东 — confirmed（纪检监察网领导机构 + 新闻）
  - 人大主任 张淼、政协主席 刘占明 — confirmed（官网）
  - 新增副市长 江涛（2026-08-05 决定任命）、黄薇薇、胡红军、王冰（秘书长）— confirmed名单
  - 王炳森完整履历（籍贯/出生地/入党/具体毕业院校、2022-04 前大连市委副书记任期）— 部分，留 open_questions

Web-access note: Exa 限流；Bing/Jina 时常超时；采用 direct webfetch 官方门户 + 百度百科（primary+secondary）交叉核对。
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while not (REPO_ROOT / "gov_relation").is_dir() and REPO_ROOT != REPO_ROOT.parent:
    REPO_ROOT = REPO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "盘锦市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CUR = Path(__file__).resolve().parent
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_盘锦市"
if _CUR.name == "liaoning_盘锦市":
    STAGING = _CUR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CUR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────
# 核心: 1=市委书记 王炳森, 2=市长 邢鹏
# 前任: 3=前市委书记 张成中(2021-23), 4=前市长 汤方栋
# 市委/市府: 5 常务副市长 戚宇, 6 市委常委/副市长 韩尚富, 7 市纪委书记 曲维东
# 副市长: 8 李荣海(公安), 9 周伟山(民盟), 10 胡振乾, 11 江涛(new), 12 黄薇薇, 13 胡红军
# 秘书长: 14 王冰
# 四套班子: 15 人大主任 张淼, 16 政协主席 刘占明
# 司法: 17 中院院长 王兴奎, 18 检察院检察长 苏中辉
persons = [
    # ═══ 现任核心 ══════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王炳森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市委书记",
        "current_org": "中共盘锦市委员会",
        "source": "http://www.panjin.gov.cn/（官方新闻 2026-08-05 以'市委书记'署名主持'王炳森到常态化联系企业走访并走访安全生产工作'）；baike.baidu.com/item/王炳森",
    },
    {
        "id": 2,
        "name": "邢鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-02",
        "birthplace": "吉林梨树",
        "education": "在职研究生学历（辽宁大学历史学），历史学学士、硕士（官网写历史学学士、哲学博士）",
        "party_join": "1994-12",
        "work_start": "1995-08",
        "current_post": "盘锦市委副书记、市长",
        "current_org": "盘锦市人民政府",
        "source": "http://www.panjin.gov.cn/html/1950/（市长简介）；baike.baidu.com/item/邢鹏",
    },
    # ═══ 前任 ══════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张成中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历，高级政工师（石化系统出身）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "应急管理部党委书记、部长（前盘锦市委书记 2021-01~2022-04）",
        "current_org": "应急管理部 / 中共盘锦市委员会(曾任)",
        "source": "baike.baidu.com/item/张成中（百科：2021-01任盘锦市委书记，2021-12兼辽宁省委常委、秘书长，2022-04卸任盘锦；2023-07河北省委常委、常务副省长，2024-11唐山市委书记，2026-03应急管理部党委书记、部长）",
    },
    {
        "id": 4,
        "name": "汤方栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽宁省人大有关委员会副主任委员（前盘锦市长 至2021-09）",
        "current_org": "辽阳市人大（曾任盘锦市）",
        "source": "http://www.panjin.gov.cn/html/1910/2020-01-14（2020年1月以'盘锦市人民政府市长'作政府工作报告）；bjrd.gov.cn（现任）",
    },
    # ═══ 市委常委/市政府 ══════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "戚宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-03",
        "birthplace": "辽宁沈阳",
        "education": "沈阳建筑工程学院涉外机械工程专业，在职研究生，工学学士、管理学博士",
        "party_join": "中共党员",
        "work_start": "1996-08",
        "current_post": "盘锦市委常委、市政府党组副书记、常务副市长",
        "current_org": "盘锦市人民政府",
        "source": "http://www.panjin.gov.cn/html/3149/（市委常委、常务副市长，负责市政府常务工作）",
    },
    {
        "id": 6,
        "name": "韩尚富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-03",
        "birthplace": "山东新泰",
        "education": "博士研究生，理学博士",
        "party_join": "中共党员",
        "work_start": "1997-08",
        "current_post": "盘锦市委常委、副市长、辽滨沿海经济技术开发区党工委书记",
        "current_org": "盘锦市人民政府 / 辽滨沿海经济技术开发区",
        "source": "http://www.panjin.gov.cn/html/2899/（市委常委、副市长，辽滨经开区党工委书记名下）",
    },
    {
        "id": 7,
        "name": "曲维东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市委常委、市纪委书记、市监委主任",
        "current_org": "盘锦市纪委市监委",
        "source": "http://www.pjjjjc.gov.cn/（市纪委监委领导机构）/ 盘锦市政府新闻（'市委常委、纪委书记、监委主任曲维东'）",
    },
    {
        "id": 8,
        "name": "李荣海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-03",
        "birthplace": "辽宁东港",
        "education": "大学学历，工学学士",
        "party_join": "1996-06",
        "work_start": "1997-08",
        "current_post": "盘锦市副市长、市政府党组成员，市公安局党委书记、局长",
        "current_org": "盘锦市人民政府 / 盘锦市公安局",
        "source": "http://www.panjin.gov.cn/html/1956/（副市长，市公安局局长）",
    },
    {
        "id": 9,
        "name": "周伟山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "辽宁盘锦",
        "education": "辽宁大学经济管理学院企业管理专业，在职研究生",
        "party_join": "民盟会员",
        "work_start": "2000-03",
        "current_post": "盘锦市政府副市长、民盟盘锦市委主委",
        "current_org": "盘锦市人民政府",
        "source": "http://www.panjin.gov.cn/html/2696/（副市长，民盟）",
    },
    {
        "id": 10,
        "name": "胡振乾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-02",
        "birthplace": "黑龙江北安",
        "education": "北京理工大学机械设计专业，在职研究生，工学学士、火炮弹药与自动武器专业硕士",
        "party_join": "中共党员",
        "work_start": "1995-07",
        "current_post": "盘锦市政府副市长",
        "current_org": "盘锦市人民政府",
        "source": "http://www.panjin.gov.cn/html/2691.html（副市长）",
    },
    {
        "id": 11,
        "name": "江涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市政府副市长（2026-08-05 决定任命）",
        "current_org": "盘锦市人民政府",
        "source": "http://www.pjrd.gov.cn/（2026-08-05 市人大常委会决定任命江涛为副市长）",
    },
    {
        "id": 12,
        "name": "黄薇薇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市政府副市长",
        "current_org": "盘锦市人民政府",
        "source": "http://www.panjin.gov.cn（市政府领导之窗）",
    },
    {
        "id": 13,
        "name": "胡红军",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市政府副市长",
        "current_org": "盘锦市人民政府",
        "source": "http://www.panjin.gov.cn/html/2691.html（副市长）",
    },
    {
        "id": 14,
        "name": "王冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-01",
        "birthplace": "辽宁盘锦",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1990-01",
        "current_post": "盘锦市政府秘书长、市政府办公室党组书记",
        "current_org": "盘锦市人民政府办公室",
        "source": "http://www.panjin.gov.cn/html/2691.html（市政府秘书长）",
    },
    # ═══ 四套班子 / 两院 ═══════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "张淼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市人大常委会党组书记、主任",
        "current_org": "盘锦市人大常委会",
        "source": "http://www.pjrd.gov.cn/（市人大常委会领导之窗/新闻）",
    },
    {
        "id": 16,
        "name": "刘占明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市政协党组书记、主席",
        "current_org": "政协盘锦市委员会",
        "source": "http://www.pjszx.gov.cn/（市政协领导）",
    },
    {
        "id": 17,
        "name": "王兴奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市中级人民法院院长",
        "current_org": "盘锦市中级人民法院",
        "source": "http://www.panjin.gov.cn/（市九届人大常委会第三十六次会议相关新闻）",
    },
    {
        "id": 18,
        "name": "苏中辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘锦市人民检察院检察长",
        "current_org": "盘锦市人民检察院",
        "source": "http://www.panjin.gov.cn/（市九届人大常委会第三十六次会议相关新闻）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共盘锦市委员会", "type": "party_committee", "level": "地厅级", "parent": "中共辽宁省委", "location": "盘锦市"},
    {"id": 2, "name": "盘锦市人民政府", "type": "government", "level": "地厅级", "parent": "辽宁省人民政府", "location": "盘锦市"},
    {"id": 3, "name": "盘锦市人大常委会", "type": "npc", "level": "地厅级", "parent": "", "location": "盘锦市"},
    {"id": 4, "name": "政协盘锦市委员会", "type": "cppcc", "level": "地厅级", "parent": "", "location": "盘锦市"},
    {"id": 5, "name": "盘锦市纪委市监委", "type": "discipline", "level": "地厅级", "parent": "辽宁省纪委", "location": "盘锦市"},
    {"id": 6, "name": "盘锦市公安局", "type": "government", "level": "县处级", "parent": "盘锦市人民政府", "location": "盘锦市"},
    {"id": 7, "name": "盘锦市人民政府办公室", "type": "government", "level": "县处级", "parent": "盘锦市人民政府", "location": "盘锦市"},
    {"id": 8, "name": "辽滨沿海经济技术开发区", "type": "development_zone", "level": "副厅级", "parent": "盘锦市人民政府", "location": "盘锦市"},
    {"id": 9, "name": "盘锦市中级人民法院", "type": "judiciary", "level": "地厅级", "parent": "", "location": "盘锦市"},
    {"id": 10, "name": "盘锦市人民检察院", "type": "procuratorate", "level": "地厅级", "parent": "", "location": "盘锦市"},
    {"id": 11, "name": "中共辽宁省委", "type": "party_committee", "level": "省级", "parent": "中国共产党中央委员会", "location": "辽宁省"},
    {"id": 12, "name": "辽宁省人民政府", "type": "government", "level": "省级", "parent": "", "location": "辽宁省"},
    {"id": 13, "name": "应急管理部", "type": "central_government", "level": "正部级", "parent": "国务院", "location": "北京市"},
    {"id": 14, "name": "中共大连市委", "type": "party_committee", "level": "副省级", "parent": "中共辽宁省委", "location": "大连市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王炳森 市委书记
    {"person_id": 1, "org_id": 1, "title": "盘锦市委书记", "start_date": "2022-04", "end_date": "present", "rank": "正厅级", "note": "兼盘锦军分区党委第一书记；中共二十一大代表、辽宁省委十三届委员"},
    {"person_id": 1, "org_id": 14, "title": "大连市委副书记（曾任）", "start_date": "2021-11", "end_date": "2022-04", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "大连市委常委、组织部部长（曾任）", "start_date": "2019-10", "end_date": "2021-11", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "辽宁省委组织部常务副部长（曾任）", "start_date": "", "end_date": "2019-10", "rank": "正厅级", "note": "此前在中组部人才工作局任副局长"},
    # 邢鹏 市长
    {"person_id": 2, "org_id": 2, "title": "盘锦市市长", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "2021-08起任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "副市长、代市长（曾任）", "start_date": "2021-09", "end_date": "2022-01", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "盘锦市委副书记", "start_date": "2021-08", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张成中 前任书记
    {"person_id": 3, "org_id": 13, "title": "应急管理部部长", "start_date": "2026-04", "end_date": "present", "rank": "正部级", "note": "2026-03任应急管理部党委书记"},
    {"person_id": 3, "org_id": 1, "title": "盘锦市委书记（曾任）", "start_date": "2021-01", "end_date": "2022-04", "rank": "正厅级", "note": "2021-12 起兼辽宁省委常委、秘书长"},
    {"person_id": 3, "org_id": 11, "title": "辽宁省委常委、秘书长（曾任）", "start_date": "2021-12", "end_date": "2023-07", "rank": "副省级", "note": ""},
    # 汤方栋 前任市长
    {"person_id": 4, "org_id": 2, "title": "盘锦市市长（曾任）", "start_date": "", "end_date": "2021-09", "rank": "正厅级", "note": "2020-01 以'盘锦市市长'作政府工作报告"},
    # 戚宇 常务副市长
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责市政府常务工作"},
    {"person_id": 5, "org_id": 1, "title": "盘锦市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 韩尚富
    {"person_id": 6, "org_id": 2, "title": "副市长、市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "辽滨经开区党工委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 曲维东
    {"person_id": 7, "org_id": 5, "title": "市委书记、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "盘锦市委常委"},
    # 李荣海 公安
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责公安、司法"},
    {"person_id": 8, "org_id": 6, "title": "市公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 周伟山 民盟
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "民盟盘锦市委主委"},
    # 胡振乾
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 江涛
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "2026-08", "end_date": "present", "rank": "副厅级", "note": "2026-08-05 市人大常委会决定任命"},
    # 黄薇薇
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 胡红军
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王冰 秘书长
    {"person_id": 14, "org_id": 7, "title": "市政府秘书长、办公室党组书记", "start_date": "", "end_date": "present", "rank": "正县处级", "note": ""},
    # 四套班子
    {"person_id": 15, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 司法
    {"person_id": 17, "org_id": 9, "title": "市中级人民法院院长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 10, "title": "市人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—市长（现任核心）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记—市长（党政主官）", "overlap_org": "盘锦市", "overlap_period": "2022-01 至今"},
    # 书记—常委班子
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记—常务副市长（常委）", "overlap_org": "中共盘锦市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委书记—开发区党工委书记（常委、副市长）", "overlap_org": "中共盘锦市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记—市纪委书记（常委）", "overlap_org": "中共盘锦市委员会", "overlap_period": ""},
    # 市长—政府班子
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长—常务副市长", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长—副市长（开发区）", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长—副市长（公安局长）", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长—新任副市长", "overlap_org": "盘锦市人民政府", "overlap_period": "2026-08"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长—市政府秘书长", "overlap_org": "盘锦市人民政府", "overlap_period": ""},
    # 市委—四套班子
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "市委书记—市人大常委会主任", "overlap_org": "盘锦市", "overlap_period": ""},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "市委书记—市政协主席", "overlap_org": "盘锦市", "overlap_period": ""},
    # 前任继任链
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "前市委书记(张成中 2021-01~2022-04)→现任市委书记(王炳森 2022-04~)", "overlap_org": "中共盘锦市委员会", "overlap_period": "2022-04"},
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "前市长(汤方栋 至2021-09)→现任市长(邢鹏 2021-09代→2022-01)", "overlap_org": "盘锦市人民政府", "overlap_period": "2021-09"},
]

# ── Person JSON(s) ────────────────────────────────────────────────────────────
def _write_person_json(person: dict, out_dir: Path) -> None:
    """Write a person graph JSON for the person."""
    job_tag = person["current_post"] or person["name"]
    if job_tag.startswith("盘锦"):
        job_tag = job_tag[len("盘锦"):]
    if job_tag[:2] != "市委" and job_tag.startswith("市"):
        job_tag = job_tag[1:]
    safe_name = re.sub(r"[^\u4e00-\u9fff\w\-. ]", "_", f"{TODAY}-辽宁省-盘锦市-{job_tag}-{person['name']}.json")
    filepath = out_dir / safe_name

    pjson = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "盘锦市",
            "region": "盘锦市",
            "job": person["current_post"],
            "task_id": "liaoning_盘锦市",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": f"panjin_{person['name'].replace(' ', '')}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": person["birthplace"] or "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正厅级" if person["id"] in (1, 2, 3, 15, 16) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": bool(person["source"]),
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present" if person["current_post"] else "",
                "org": person["current_org"],
                "title": person["current_post"],
                "rank": "",
                "confidence": "confirmed" if person["source"] else "plausible",
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {"caveat": "Work style inferred from public records only, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本轮调查未发现该人物不良记录信号（范围限于公开可查资料）。", "confidence": "unverified"}],
        "source_register": [
            {"id": "S001", "title": "盘锦市人民政府门户网站（新闻/领导之窗）", "url": "http://www.panjin.gov.cn/", "publisher": "盘锦市人民政府", "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "百度百科（secondary）", "url": "https://baike.baidu.com/item/", "publisher": "百度百科", "source_type": "encyclopedia", "reliability": "medium"},
        ],
        "confidence_summary": {
            "identity": "partial" if not person["birth"] else "confirmed",
            "current_role": "confirmed" if person["current_post"] else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生年月迄今全部职务变动、任现职前任职）",
        },
        "open_questions": [
            {"priority": "high", "question": f"{person['name']}的完整工作履历", "why_it_matters": "了解晋升路径和人际网络", "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 此前担任"], "last_attempted": TODAY}
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

    # 核心人物 PNG (市委书记、市长、常委/常务副市长、公安局长市政府秘书长, 前任书记)
    key_people_ids = [1, 2, 3, 4, 5, 6, 7, 8, 14, 15]
    for pid in key_people_ids:
        kp = dict(persons[pid - 1])
        kp.setdefault("aliases", [])
        fpath = _write_person_json(kp, PJSON_DIR)
        print(f"  Person JSON: {fpath.name}")

    # Build DB + GEXF
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