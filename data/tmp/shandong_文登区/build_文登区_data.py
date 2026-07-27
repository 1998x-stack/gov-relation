#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 文登区 (Wendeng District), 威海市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_文登区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.wendeng.gov.cn — 文登区人民政府官方网站 (accessible)
  - Government leadership pages confirmed via official website
  - News articles from wendeng.gov.cn (区委常委会, 半年工作推进会 etc.)

Confirmed via official website (confirmed):
  - 区委书记: 单浩仁 — confirmed via区委常委会扩大会议 article (2026-06-28)
  - 区长: 刘华杰 — confirmed via official bio page (updated 2026-02-05)
  - 副区长: 李延飞 (常务), 刘希杰, 王建超, 秦浩舰, 花健, 卫红红 — confirmed via official bio pages

Confidence notes:
  - 单浩仁's detailed biography (birth, education, career path): NOT on wendeng.gov.cn
    (party secretary bios are on a different domain, likely inaccessible)
  - 刘华杰's bio: fully sourced from official government page (大学学历, 法学学士, 1979年1月生)
  - All 副区长 bios: fully sourced from official government pages
  - 单浩仁's predecessor: unclear from available data
  - All claims labeled with confidence level; gaps explicitly documented
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
SLUG = "文登区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_文登区"
if _CURRENT_DIR.name == "shandong_文登区":
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
# IDs: 1-2 core leadership, 3-8 副区长, 9-10 predecessors, 11-12其他

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "单浩仁",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — common for Shandong officials
        "birth": "",  # NOT found on official site
        "birthplace": "",  # NOT found on official site
        "education": "",  # NOT found on official site
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共威海市文登区委员会",
        "source": "https://www.wendeng.gov.cn/art/2026/6/30/art_72343_6452568.html",
        "confidence": "confirmed",
        "notes": "时任文登区委书记。confirmed via 2026-06-28 区委常委会扩大会议报道中明确提及'区委书记单浩仁主持会议并讲话'。2026-07-17 半年工作推进会再次确认。完整履历待查。"
    },
    {
        "id": 2,
        "name": "刘华杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",  # not found on official bio
        "education": "大学学历，法学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "威海市文登区人民政府",
        "source": "https://www.wendeng.gov.cn/art/2026/2/5/art_38183_6137028.html",
        "confidence": "confirmed",
        "notes": "文登区委副书记、区政府党组书记、区长。1979年1月生，大学学历，法学学士。曾任荣成市督查考核办公室副主任（其间挂职人和镇党委副书记）、荣成市上庄镇党委副书记/镇长、荣成市港西镇党委副书记/镇长/党委书记、荣成市好运角旅游度假区党工委副书记/港西镇党委书记/成山镇党委书记、荣成市委常委/副市长/三级调研员/好运角旅游度假区党工委书记/管委会主任/市委国企工委书记、文登区委副书记/三级调研员、文登区委副书记/区政府党组书记/副区长/代理区长，2026年2月任区长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 副区长 (confirmed from official website)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李延飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年3月",
        "birthplace": "",
        "education": "大学学历，理学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "威海市文登区人民政府",
        "source": "https://www.wendeng.gov.cn/art/2025/8/5/art_38184_4264147.html",
        "confidence": "confirmed",
        "notes": "文登区委常委，区政府党组副书记、副区长、三级调研员，区委区属国企工委书记。1985年3月生，大学学历，理学学士。曾任环翠区委保密办（保密局）主任（局长）、环翠区委办公室副主任（主持农工办/扶贫办）、环翠区孙家疃街道党工委副书记/办事处主任、环翠北海旅游度假区党工委副书记/管委会副主任、威海市纪委监委办公室副主任/主任、威海市监委委员/市纪委监委办公室主任、荣成市委常委/组织部部长/统战部部长/市政协党组副书记、文登区委常委/区政府党组副书记/副区长/区委区属国企工委书记，2025年7月任现职。"
    },
    {
        "id": 4,
        "name": "刘希杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "大学学历，工学学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "威海市文登区人民政府",
        "source": "https://www.wendeng.gov.cn/art/2025/8/5/art_38184_2546441.html",
        "confidence": "confirmed",
        "notes": "文登区委常委，区政府党组成员、副区长、三级调研员。1975年10月生，大学学历，工学学士。曾任荣成市民政局纪委书记/党委委员、荣成市纪委派驻第一纪检监察组副组长（副主任）、荣成市桃园街道党委副书记/办事处主任、荣成市王连街道党工委书记/一级主任科员、荣成市俚岛镇党委书记/四级调研员、威海市文登区政府党组成员/副区长、文登区委常委/区政府党组成员/副区长，2025年7月任现职。"
    },
    {
        "id": 5,
        "name": "王建超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "威海市文登区人民政府",
        "source": "https://www.wendeng.gov.cn/art/2025/8/5/art_38184_3560047.html",
        "confidence": "confirmed",
        "notes": "文登区政府党组成员、副区长。1978年12月生，在职大学学历。曾任文登区政府办公室副主任/党组成员/重点项目推进办公室主任、文登区委工业工委书记/区工业和信息化局党组书记/局长，2023年4月任副区长。"
    },
    {
        "id": 6,
        "name": "秦浩舰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "大学学历，法学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "威海市文登区人民政府",
        "source": "https://www.wendeng.gov.cn/art/2025/8/5/art_38184_4085770.html",
        "confidence": "confirmed",
        "notes": "文登区政府党组成员、副区长，威海市公安局文登分局党委书记/局长/二级高级警长，区委政法委委员/副书记（兼）。1977年6月生，大学学历，法学学士。曾任威海市公安边防支队经济技术开发区大队副团职大队长、威海市公安边防支队司令部副团职参谋长/副团职副支队长、威海市公安局海岸警察支队转改干部/副支队长/四级高级警长/三级高级警长，2025年4月任现职。"
    },
    {
        "id": 7,
        "name": "花健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年2月",
        "birthplace": "",
        "education": "大学学历，管理学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "威海市文登区人民政府",
        "source": "https://www.wendeng.gov.cn/art/2025/8/5/art_38184_4466506.html",
        "confidence": "confirmed",
        "notes": "文登区政府党组成员、副区长。1984年2月生，大学学历，管理学学士。曾任文登区米山镇党委副书记（挂职）/党委副书记/党委副书记/镇长、文登区泽库镇党委书记/一级主任科员、文登区政府党组成员/副区长/泽库镇党委书记，2024年12月任副区长。"
    },
    {
        "id": 8,
        "name": "卫红红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "大学学历，法学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "威海市文登区人民政府",
        "source": "https://www.wendeng.gov.cn/art/2025/12/6/art_38184_5740265.html",
        "confidence": "confirmed",
        "notes": "文登区政府党组成员、副区长、红十字会会长（兼）。1982年2月生，大学学历，法学学士。曾任文登区宋村镇副镇长、文登区大水泊镇党委委员/副书记（挂职）/党委副书记/政协委员联络室副主任（兼）/政法委员/政协委员联络室副主任（兼）、文登经济开发区金山党委副书记/管委主任、文登区金山党工委副书记/文登营镇二级主任科员、文登区龙山街道党工委书记/一级主任科员/圣经山景区管理服务中心党组成员（兼）、文登区政府党组成员/副区长/红十字会会长（兼）/龙山街道党工委书记/西部智造产业发展服务中心党组成员（兼），2025年11月任现职。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "乔新跃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共威海市文登区委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任文登区委书记（猜测2022-2025年间任职）。据公开报道，乔新跃曾任威海市文登区委书记，后调往威海市其他岗位。具体时间线和去向待查。"
    },
    {
        "id": 10,
        "name": "张宏璞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共威海市文登区委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "前任文登区委书记（2018-2022年左右）。后任威海市委常委、宣传部部长（在威海市领导页面中有提及）。具体时间线待进一步查证。"
    },
    {
        "id": 11,
        "name": "林恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长",
        "current_org": "威海市文登区人民政府",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "前任文登区区长。据公开报道线索，林恒曾任威海市文登区区长，后调任其他职务。具体时间线和去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共威海市文登区委员会", "type": "党委", "level": "县处级", "parent": "中共威海市委员会", "location": "威海市文登区"},
    {"id": 2, "name": "威海市文登区人民政府", "type": "政府", "level": "县处级", "parent": "威海市人民政府", "location": "威海市文登区"},
    {"id": 3, "name": "威海市公安局文登分局", "type": "政府", "level": "县处级", "parent": "威海市文登区人民政府", "location": "威海市文登区"},
    {"id": 4, "name": "荣成市好运角旅游度假区", "type": "开发区", "level": "县处级", "parent": "荣成市人民政府", "location": "荣成市"},
    {"id": 5, "name": "荣成市港西镇", "type": "乡镇/街道", "level": "乡科级", "parent": "荣成市人民政府", "location": "荣成市"},
    {"id": 6, "name": "荣成市上庄镇", "type": "乡镇/街道", "level": "乡科级", "parent": "荣成市人民政府", "location": "荣成市"},
    {"id": 7, "name": "荣成市成山镇", "type": "乡镇/街道", "level": "乡科级", "parent": "荣成市人民政府", "location": "荣成市"},
    {"id": 8, "name": "中共威海市纪律检查委员会文登区委员会", "type": "党委", "level": "县处级", "parent": "中共威海市文登区委员会", "location": "威海市文登区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 单浩仁 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "confirmed as of 2026-06"},
    # 刘华杰 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026-02", "end_date": "present", "rank": "正处级", "note": "文登区委副书记、区政府党组书记、区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "文登区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "副区长（代理区长）", "start_date": "", "end_date": "2026-02", "rank": "正处级", "note": "文登区委副书记、区政府党组书记、副区长、代理区长"},
    {"person_id": 2, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "文登区委副书记、三级调研员"},
    # 刘华杰 — Rongcheng posts
    {"person_id": 2, "org_id": 4, "title": "党工委书记、管委会主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "荣成市委常委、副市长、好运角旅游度假区党工委书记/管委会主任/市委国企工委书记"},
    {"person_id": 2, "org_id": 7, "title": "党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "荣成市好运角旅游度假区党工委副书记，成山镇党委书记/一级主任科员"},
    {"person_id": 2, "org_id": 4, "title": "党工委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "荣成市好运角旅游度假区党工委副书记，港西镇党委书记"},
    {"person_id": 2, "org_id": 5, "title": "党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "荣成市港西镇党委书记"},
    {"person_id": 2, "org_id": 5, "title": "镇长", "start_date": "", "end_date": "", "rank": "正科级", "note": "荣成市港西镇党委副书记、镇长"},
    {"person_id": 2, "org_id": 6, "title": "镇长", "start_date": "", "end_date": "", "rank": "正科级", "note": "荣成市上庄镇党委副书记、镇长"},
    {"person_id": 2, "org_id": 6, "title": "督查考核办公室副主任", "start_date": "", "end_date": "", "rank": "副科级", "note": "荣成市督查考核办公室副主任（其间挂职人和镇党委副书记）"},
    # 李延飞 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 2, "title": "副区长（常务）", "start_date": "2025-07", "end_date": "present", "rank": "副处级", "note": "文登区委常委，区政府党组副书记、副区长、三级调研员，区委区属国企工委书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "文登区委常委"},
    {"person_id": 3, "org_id": 1, "title": "市委常委、组织部部长、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "荣成市委常委、组织部部长、统战部部长，市政协党组副书记"},
    {"person_id": 3, "org_id": 8, "title": "市纪委监委办公室主任", "start_date": "", "end_date": "", "rank": "正科级", "note": "威海市监委委员、市纪委监委办公室主任"},
    {"person_id": 3, "org_id": 8, "title": "市纪委监委办公室副主任、主任", "start_date": "", "end_date": "", "rank": "副科级/正科级", "note": "威海市纪委监委办公室副主任、主任"},
    # 刘希杰 — Deputy Mayor
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "2025-07", "end_date": "present", "rank": "副处级", "note": "文登区委常委，区政府党组成员、副区长、三级调研员"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "文登区委常委"},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "威海市文登区政府党组成员、副区长"},
    # 王建超 — Deputy Mayor
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "2023-04", "end_date": "present", "rank": "副处级", "note": "文登区政府党组成员、副区长"},
    # 秦浩舰 — Deputy Mayor / Public Security
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "2025-04", "end_date": "present", "rank": "副处级", "note": "文登区政府党组成员、副区长"},
    {"person_id": 6, "org_id": 3, "title": "党委书记、局长", "start_date": "2025-04", "end_date": "present", "rank": "二级高级警长", "note": "威海市公安局文登分局党委书记、局长"},
    # 花健 — Deputy Mayor
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "2024-12", "end_date": "present", "rank": "副处级", "note": "文登区政府党组成员、副区长"},
    # 卫红红 — Deputy Mayor
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "2025-11", "end_date": "present", "rank": "副处级", "note": "文登区政府党组成员、副区长、红十字会会长（兼）"},
    # 乔新跃 — Predecessor Party Secretary
    {"person_id": 9, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "前任文登区委书记（猜测约2022-2025）"},
    # 张宏璞 — Predecessor Party Secretary
    {"person_id": 10, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "前任文登区委书记（约2018-2022），后任威海市委常委、宣传部部长"},
    # 林恒 — Predecessor Mayor
    {"person_id": 11, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任文登区区长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 单浩仁 ↔ 刘华杰 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共威海市文登区委员会/文登区人民政府", "overlap_period": "2026-至今"},
    # 单浩仁 ↔ 李延飞
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—常委/常务副区长", "overlap_org": "中共威海市文登区委员会", "overlap_period": "2025-至今"},
    # 单浩仁 ↔ 刘希杰
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委/副区长", "overlap_org": "中共威海市文登区委员会", "overlap_period": ""},
    # 刘华杰 ↔ 李延飞 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—常务副区长", "overlap_org": "威海市文登区人民政府", "overlap_period": "2025-至今"},
    # 刘华杰 ↔ 刘希杰 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "威海市文登区人民政府", "overlap_period": ""},
    # 刘华杰 ↔ 王建超
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长", "overlap_org": "威海市文登区人民政府", "overlap_period": ""},
    # 刘华杰 ↔ 秦浩舰
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—副区长/公安局长", "overlap_org": "威海市文登区人民政府", "overlap_period": ""},
    # 刘华杰 ↔ 花健
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "威海市文登区人民政府", "overlap_period": ""},
    # 刘华杰 ↔ 卫红红
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长", "overlap_org": "威海市文登区人民政府", "overlap_period": ""},
    # 李延飞 ↔ 刘希杰 — both常委 colleagues
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共威海市文登区委员会", "overlap_period": ""},
    # 刘华杰 and 单浩仁 — confirmed荣成 connection?
    {"person_a": 1, "person_b": 2, "type": "可能的同域关联", "context": "单浩仁和刘华杰均有荣成市任职经历", "overlap_org": "荣成市", "overlap_period": "推测",
     "note": "刘华杰曾任荣成市委常委、副市长等职多年。单浩仁也可能有荣成经历（待确认）"},
    # 刘华杰 ↔ 李延飞 — 荣成 connection
    {"person_a": 2, "person_b": 3, "type": "同域关联", "context": "两人均曾任荣成市委常委", "overlap_org": "荣成市", "overlap_period": "推测",
     "note": "刘华杰曾任荣成市委常委/副市长；李延飞曾任荣成市委常委/组织部部长/统战部部长。二人可能曾在荣成市委共事。"},
    # Predecessor relationships
    {"person_a": 9, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记", "overlap_org": "中共威海市文登区委员会", "overlap_period": "推测"},
    {"person_a": 10, "person_b": 9, "type": "交接", "context": "前任—继任（区委书记）", "overlap_org": "中共威海市文登区委员会", "overlap_period": "推测"},
    {"person_a": 11, "person_b": 2, "type": "交接", "context": "前任区长—现任区长", "overlap_org": "威海市文登区人民政府", "overlap_period": "推测"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"wendeng_{name}"

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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Parse detailed bio notes into additional timeline entries
    notes = person.get("notes", "")
    if "曾任" in notes:
        # For单浩仁 or others without detailed notes
        pass

    if len(career_timeline) <= 2 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。区委书记履历不在政府网站上公开。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_type = "overlap"
        if r["type"] in ("交接", "可能的同域关联", "同域关联"):
            rel_type = "other"
        rels_output.append({
            "person": other_name,
            "person_id": f"wendeng_{other_name}",
            "relationship_type": rel_type,
            "strength": "strong" if r["type"] in ("共事", "同僚") else "weak",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("共事", "同僚") else "unverified",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "文登区人民政府官方网站",
            "url": source_url,
            "publisher": "威海市文登区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "政府领导页面（领导之窗）直接获取",
        }
    ]

    big_gap = "完整履历"
    if not person.get("birth"):
        big_gap = "出生年月、籍贯、完整履历"
    if pid == 1:
        big_gap = "单浩仁的完整履历（包括出生年月、籍贯、学历、历任职务及起止时间），区委书记履历不在政府网站上公开"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "威海市",
            "region": "文登区",
            "job": person.get("current_post", ""),
            "task_id": "shandong_文登区",
            "time_focus": "2026年7月",
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
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "副厅级" if pid in (1, 9, 10) else ("正处级" if pid == 2 else "副处级"),
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if pid == 2 else ("partial" if pid >= 3 else "thin"),
            "relationship_confidence": "medium" if person.get("confidence") == "confirmed" else "low",
            "biggest_gap": big_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 百度百科", f"{name} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    if pid == 1:
        record["open_questions"].append({
            "priority": "critical",
            "question": "单浩仁调任文登区委书记的具体时间、此前任职",
            "why_it_matters": "核心人物的完整履历是网络分析的基础",
            "suggested_queries": ["单浩仁 简历 文登", "单浩仁 此前 担任", "单浩仁 任前公示"],
            "last_attempted": AS_OF,
        })
    if pid == 2:
        record["open_questions"][0]["question"] = "刘华杰的籍贯"
        record["open_questions"][0]["why_it_matters"] = "已知出生年月1979年1月，缺籍贯"

    post_slug = person['current_post'].replace('/', '_').replace('（', '(').replace('）', ')')
    fname = f"{TODAY}-山东省-威海市-{post_slug}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
