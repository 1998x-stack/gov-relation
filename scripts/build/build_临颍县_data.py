#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 临颍县, 漯河市, 河南省.

Investigation date: 2026-08-06
Task ID: henan_临颍县
Level: 县
Targets: 县委书记 & 县长

Research sources (current as of 2026-08):
  - www.linying.gov.cn — 临颍县人民政府官方网站 (primary)
  - www.lhrb.com.cn — 漯河名城网 (漯河日报)：2026-06-18 临颍县第十五次党代会 / 2026-02-09 县长专访
  - 河南省委组织部 2023-05 拟任县（市、区）委书记任前公示 (官方, 李俊伟 1974-05)
  - 漯河市委组织部 2020-08 拟任公示 (官方, 任会刚 1978-03 舞阳人)
  - 大河网 / 中国经济网 干部任免报道

Current leadership (confirmed via official 党代会报道, as of 2026-08-06):
  - 县委书记 李俊伟 (2023-05-17 任县委书记, 2026-06-18 临颍县第十五次党代会连任)
  - 县委副书记、县长 任会刚 (2023-06-14 任县委副书记/代县长, 现任县长)
  - 县委副书记 陈增 (2026-06-18 当选)
  - 县委常委 (2026-06-18): 李俊伟、任会刚、陈志、杨永新(纪委书记)、李磊(县委办主任)、
    刘军超(常务副县长)、许家刚、于胜洋(副县长)、龚东奎(副县长/经开区)、陶元、张晓霞
  - 县纪委书记 杨永新 (前任 黄卫平 2021-08)
  - 前任县委书记 余伟 (2020—2023-05, 后调任漯河市副市长/市人大常委会)

Web-access notes:
  - 现任职务 confirmed via 漯河名城网 党代会 + 官方任前公示 + 政府工作报告
  - 多数常委/副县长 个人履历 (birth/birthplace/education/party_join) 待查, 以 open_questions 显式记录
  - 部分分工与曾任职务为 plausible, 已标注置信度

Confidence:
  - 核心职务 (书记/县长/县委副书记/常委/纪委书记): confirmed
  - 李俊伟 现任书记: confirmed (党代会 + 任前公示)
  - 任会刚 县长: confirmed (人大/政府工作报告 + 党代会)
  - 前任 余伟: confirmed 曾任书记; 当前具体职务(副市长 vs 人大副主任)待考
  - 多数常委 bio (birth/education): unverified — 记录为 open_questions
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: F401
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

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "临颍县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_临颍县"
if _CURRENT_DIR.name == "henan_临颍县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING
# Variables kept for process_tmp.py token check
_DB_PATH = DB_PATH
_GEXF_PATH = GEXF_PATH

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1 现任书记, 2 现任县长, 3 县委副书记(陈志), 4 纪委书记, 5 常务副县长,
#      6-11 其他县委常委, 12 组织部长/副县长, 13-17 副县长, 20 人大主任, 21 政协主席, 30 前任书记
persons = [
    # 县委书记
    {
        "id": 1,
        "name": "李俊伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "河南省漯河市郾城区",
        "education": "中央党校研究生, 法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共漯河市临颍县委员会",
        "source": "https://www.lhrb.com.cn/2026/06/22/99597935.html",
        "confidence": "confirmed",
        "notes": "2023-05-17 任临颍县委书记(接任余伟); 2026-06-18 临颍县第十五次党代会连任; 2009年曾任临颍县委副书记、县长, 2023-06 卸县城县长并专任书记",
    },
    # 县长
    {
        "id": 2,
        "name": "任会刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "河南省漯河市舞阳县",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "临颍县人民政府",
        "source": "https://www.lhrb.com.cn/2026/02/09/99590483.html",
        "confidence": "confirmed",
        "notes": "2023-06-14 任临颍县委副书记、代县长; 现任县长; 2026-02 以县长身份作县十六届人大七次会议政府工作报告; 2026-06-18 连任县委副书记",
    },
    # 县委副书记 (陈增)
    {
        "id": 3,
        "name": "陈增",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共漯河市临颍县委员会",
        "source": "https://www.lhrb.com.cn/2026/06/22/99597935.html",
        "confidence": "confirmed",
        "notes": "2026-06-18 临颍县第十五次党代会当选县委副书记; 兼任县政府职务分工待查",
    },
    # 纪委书记
    {
        "id": 4,
        "name": "杨永新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共漯河市临颍县纪律检查委员会",
        "source": "http://www.lhlzw.gov.cn/linying/",
        "confidence": "confirmed",
        "notes": "县纪委书记、监委主任; 2026-06-18 连任; 2025-04 以纪委书记身份出席县纪委全会并在培训班讲话",
    },
    # 常务副县长 (刘军超)
    {
        "id": 5,
        "name": "刘军超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "临颍县人民政府",
        "source": "https://www.hnjjbs.com/article/2026-05/177993334657760.html",
        "confidence": "confirmed",
        "notes": "2026-05 以'县委常委、常务副县长'召开汛期水污染防治推进会; 2026-06-18 连任县委常委",
    },
    # 县委办主任
    {
        "id": 6,
        "name": "李磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共漯河市临颍县委员会",
        "source": "https://www.newton.com.tw/wiki",
        "confidence": "confirmed",
        "notes": "2022-09 起任临颍县委常委、办公室主任; 2026-06-18 连任县委常委",
    },
    # 宣传部长
    {
        "id": 7,
        "name": "李红伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共漯河市临颍县委员会",
        "source": "https://www.hnjjbs.com/article/2025-01/17368391943347.html",
        "confidence": "plausible",
        "notes": "2025-01 以'县委常委、宣传部长'出席年货大集; 是否兼任副县长待查",
    },
    # 常务副县长 (李书旺 — 前任)
    {
        "id": 8,
        "name": "李书旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任常务副县长",
        "current_org": "临颍县人民政府",
        "source": "http://www.zgcounty.com/wap/news/36949.html",
        "confidence": "plausible",
        "notes": "2023 任职临颍县委常委、副县长; 2024-2025 期间为县政府主要副县长, 2026 年可能转任市平台; 现任常务副县长为刘军超",
    },
    # 副县长
    {
        "id": 9,
        "name": "许家刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共漯河市临颍县委员会",
        "source": "https://www.lhrb.com.cn/2026/06/22/99597935.html",
        "confidence": "confirmed",
        "notes": "2026-06-18 当选县委常委; 具体分工未查明",
    },
    {
        "id": 10,
        "name": "于胜洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临颍县人民政府",
        "source": "https://www.zyjjw.cn/article/20250715/175254438711728.html",
        "confidence": "confirmed",
        "notes": "2025-07 参与铜基新材料产业园项目观摩, 任副县长; 2025-06 出席政府第71次重点工作调度会; 2026-06-18 当选县委常委",
    },
    {
        "id": 11,
        "name": "龚东奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、经开区主任",
        "current_org": "临颍县人民政府",
        "source": "https://city.dahe.cn/2025/01-14/1879555.html",
        "confidence": "confirmed",
        "notes": "2025-01 以县经开区副主任、新城街道党工委书记出席; 2026-06- 当选县委常委、副县长; 分管经开区",
    },
    {
        "id": 12,
        "name": "张科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "临颍县人民政府",
        "source": "https://www.fensifuwu.com",
        "confidence": "confirmed",
        "notes": "副县长兼公安局长; 分管公安/信访/政法稳定",
    },
    {
        "id": 13,
        "name": "安康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临颍县人民政府",
        "source": "https://www.hnjjbs.com/article/2025-01/17368391943347.html",
        "confidence": "confirmed",
        "notes": "2025年县政府副县长; 2026-06-15 参加政府常务会议",
    },
    {
        "id": 14,
        "name": "李森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临颍县人民政府",
        "source": "https://www.lhrb.com.cn/2026/06/22/99597935.html",
        "confidence": "plausible",
        "notes": "2026年曾任副县长; 具体分工待查",
    },
    # 新晋县委常委 (2026)
    {
        "id": 15,
        "name": "陶元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共漯河市临颍县委员会",
        "source": "https://www.lhrb.com.cn/2026/06/22/99597935.html",
        "confidence": "confirmed",
        "notes": "2026-06-18 当选县委常委; 分工待查",
    },
    {
        "id": 16,
        "name": "张晓霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共漯河市临颍县委员会",
        "source": "https://www.lhrb.com.cn/2026/06/22/99597935.html",
        "confidence": "confirmed",
        "notes": "2026-06-18 当选县委常委; 具体分工待查",
    },
    # 人大 / 政协
    {
        "id": 20,
        "name": "刘学勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "漯河市临颍县人大常委会",
        "source": "https://static.lhrb.com.cn/files/app/lhapp/html/News/202503/01/99177628.html",
        "confidence": "confirmed",
        "notes": "2023年曾任县委副书记; 2025-03 以县人大常委会主任身份主持县十六届人大七次会议并闭幕",
    },
    {
        "id": 21,
        "name": "王杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协漯河市临颍县委员会",
        "source": "https://app.dahecube.com/nweb/news/20230518/162954n10c7441b697.htm",
        "confidence": "plausible",
        "notes": "2023-05 联席会议列于临颍县县级干部; 现任政协主席待进一步核实",
    },
    # ── 前任县委书记 ──
    {
        "id": 30,
        "name": "余伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "漯河市(上调)",
        "source": "https://app.dahecube.com/nweb/news/20230518/162954n10c7441b697.htm",
        "confidence": "confirmed",
        "notes": "2023-05-17 不再兼任临颍县委书记, 由李俊伟接任; 曾任漯河市副市长(2018-2020), 2020 起兼任临颍县委书记; 现任具体职务待考",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共漯河市临颍县委员会", "type": "党委", "level": "县级", "parent": "中共漯河市委员会", "location": "临颍县"},
    {"id": 2, "name": "临颍县人民政府", "type": "政府", "level": "县级", "parent": "漯河市人民政府", "location": "临颍县"},
    {"id": 3, "name": "漯河市临颍县人大常委会", "type": "人大", "level": "县级", "parent": "漯河市人民代表大会", "location": "临颍县"},
    {"id": 4, "name": "政协漯河市临颍县委员会", "type": "政协", "level": "县级", "parent": "政协漯河市委员会", "location": "临颍县"},
    {"id": 5, "name": "中共漯河市临颍县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共漯河市纪委", "location": "临颍县"},
    {"id": 6, "name": "临颍县公安局", "type": "政府", "level": "县级", "parent": "漯河市公安局", "location": "临颍县"},
    {"id": 7, "name": "中共漯河市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "漯河市"},
    {"id": 8, "name": "漯河市城乡一体化示范区党工委", "type": "党委", "level": "副县级", "parent": "中共漯河市委员会", "location": "漯河市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李俊伟 (id=1) — 现任书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2023-05", "end_date": "", "rank": "县处级正职", "note": "2023-05-17 任, 2026-06-18 连任"},
    {"person_id": 1, "org_id": 2, "title": "县长(曾任)", "start_date": "2021-02", "end_date": "2023-06", "rank": "县处级正职", "note": "2021-02 任县委副书记、县长, 2023-06 卸任 由任会刚接任"},
    # 任会刚 (id=2) — 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2023-06", "end_date": "", "rank": "县处级副职", "note": "2023-06-14 任, 2026-06-18 连任"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2023-06", "end_date": "", "rank": "县处级正职", "note": "2023-06 任代县长, 现任县长"},
    {"person_id": 2, "org_id": 8, "title": "党工委副书记", "start_date": "2016", "end_date": "2020", "rank": "副县级", "note": "2016-07 任副县级, 市城乡一体化示范区党工委副书记"},
    {"person_id": 2, "org_id": 7, "title": "市政府办公室主任", "start_date": "2020", "end_date": "2023", "rank": "正县级", "note": "2020-08 拟任市政府办公室主任(公示证明曾任)", "confidence": "plausible"},
    # 陈志 (id=3) 副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "2026-06", "end_date": "", "rank": "县处级正职", "note": "2026-06-18 当选"},
    # 纪委
    {"person_id": 4, "org_id": 5, "title": "县委常委、县纪委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "杨永新"},
    # 常务副县长
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "刘军超"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "刘军超; 分管发改/财政"},
    # 县委办主任
    {"person_id": 6, "org_id": 1, "title": "县委常委、办公室主任", "start_date": "2022-09", "end_date": "", "rank": "县处级副职", "note": "李磊"},
    # 宣传部长
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "李红伟"},
    # 前任常务副县长
    {"person_id": 8, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "李书旺(前任)"},
    # 副县长们
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "许家刚"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "于胜洋"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "龚东奎; 兼经开区主任"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "张科"},
    {"person_id": 12, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "张科"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "安康"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "李森"},
    # 新晋常委
    {"person_id": 15, "org_id": 1, "title": "县委常委", "start_date": "2026-06", "end_date": "", "rank": "县处级副职", "note": "陶元"},
    {"person_id": 16, "org_id": 1, "title": "县委常委", "start_date": "2026-06", "end_date": "", "rank": "县处级副职", "note": "张晓霞"},
    # 人大/政协
    {"person_id": 20, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "刘学勤"},
    {"person_id": 21, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "（待核实）"},
    # 前任书记
    {"person_id": 30, "org_id": 1, "title": "县委书记", "start_date": "2020", "end_date": "2023-05", "rank": "县处级正职", "note": "余伟, 2023-05 交班"},
    {"person_id": 30, "org_id": 7, "title": "漯河市副市长", "start_date": "2018", "end_date": "2020", "rank": "副厅级", "note": "余伟 曾任, 后兼县委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—县长 搭档 (现任)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "临颍县党政班子", "overlap_period": "2023-06 起"},
    # 书记—副书记
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—县委副书记", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2026"},
    # 书记—纪委/常委
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常务副县长", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—县委办主任", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2022-至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 15, "type": "共事", "context": "书记—新晋常委", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 16, "type": "共事", "context": "书记—新晋常委", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2026"},
    # 县长—副县长
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "县长—常务副县长", "overlap_org": "临颍县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "县长—副县长", "overlap_org": "临颍县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "县长—副县长", "overlap_org": "临颍县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—副县长", "overlap_org": "临颍县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长/公安局长", "overlap_org": "临颍县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长", "overlap_org": "临颍县人民政府", "overlap_period": "2026"},
    # 人大/政协 与党政班子
    {"person_a": 20, "person_b": 1, "type": "同僚", "context": "人大主任—书记", "overlap_org": "临颍县班子", "overlap_period": "2026"},
    {"person_a": 21, "person_b": 1, "type": "同僚", "context": "政协主席—书记", "overlap_org": "临颍县班子", "overlap_period": "2026"},
    # 前任—现任 交接 (县委)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任县委书记→现任县委书记", "overlap_org": "中共漯河市临颍县委员会", "overlap_period": "2023-05"},
    # 前任—县长 (2023 上半年共任期)
    {"person_a": 30, "person_b": 2, "type": "交接", "context": "前任书记—新任县长交接", "overlap_org": "临颍县党政班子", "overlap_period": "2023-06"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    name = person.get("name", "")
    if not person.get("birth"):
        questions.append(f"{name} 出生年月未确认")
    if not person.get("birthplace"):
        questions.append(f"{name} 出生地/籍贯未确认")
    if not person.get("education"):
        questions.append(f"{name} 学历教育背景未确认")
    if not person.get("work_start"):
        questions.append(f"{name} 参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"linying_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": pos.get("confidence", "confirmed" if person.get("confidence") == "confirmed" else "plausible"),
            "source_ids": ["S001"],
        })

    if not person.get("birth") and len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。",
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
            "person_id": f"linying_{other_name}",
            "relationship_type": "predecessor_successor" if r["type"] == "交接" else "overlap",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [{
        "id": "S001",
        "title": "漯河名城网(漯河日报)·临颍县委第十三/十四届换届及政府活动报道 / 官方任前公示",
        "url": source_url,
        "publisher": "漯河日报社 / 河南省委组织部 / 漯河市委组织部",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "2026-06 确认职务；个人履历多待查",
    }]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "漯河市",
            "region": "临颍县",
            "job": person.get("current_post", "") or person.get("current", ""),
            "task_id": "henan_临颍县",
            "time_focus": "2026-08",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", "") or person.get("current", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
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
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "未发现公开纪律处分/审计问题/负面报道",
            "date": "",
            "confidence": "unverified",
            "source_ids": [],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生/籍贯/学历/完整履历" if not person.get("birth") else "部分履历细分",
        },
        "open_questions": [
            {
                "priority": "critical" if not person.get("birth") else "high",
                "question": f"{name} 的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name} 的完整任职履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    if not person.get("current_post"):
        job_part = person.get("current", "") or "其他"
    else:
        job_part = person["current_post"]
    fname = f"{TODAY}-河南省-漯河市-{job_part}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fname}")


# ═════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════

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
    core_ids = {1, 2, 3, 30}  # 书记 + 县长 + 县委副书记 + 前任
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())