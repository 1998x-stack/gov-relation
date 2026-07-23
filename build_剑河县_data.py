#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for 剑河县 (Jianhe County, Qiandongnan, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Targets: 县委书记 & 县长

Research Note (2026-07-23):
  Web sources partially accessible:
  - Baidu Baike (剑河县 entry): accessed successfully — listed leadership as of 2024.10
  - Official site www.jianhe.gov.cn: unreachable (timeout on both http/https)
  - Baidu Baike (individual person entries): 403 blocked
  - Jina Reader: timed out
  - Exa: rate-limited
  - Google/Bing: traffic blocked or timeout

  Key findings from Baidu Baike 剑河县 entry ("政治" section, updated 2024.10):
  - 县委书记: 杨胜朝
  - 县委副书记、县长: 陈林
  - 县委副书记: 吴小勇、金枫
  - 副县长: 黄琦
  - 县人大常委会主任: 龙景灿
  - 县委常委、宣传部部长、统战部部长: 肖宗燕
  - 县委常委、组织部部长: 况再猛
  - 县政协主席: 吴政富
  - 县政协副主席: 胡朝庭、谢建梅、龙寻、龙家菊、夏永忠、邰纲敏

  Note: Many biographical details (birth year, birthplace, education, ethnicity,
  party join date, full career timeline) remain unknown. These are marked as gaps.
"""

import sqlite3  # noqa: used by gov_relation.runner
import sys
from pathlib import Path

# Ensure project root is on sys.path so gov_relation module can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "杨胜朝",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县委书记",
        "current_org": "中共剑河县委员会",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    {
        "id": 2,
        "name": "陈林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县委副书记、县长",
        "current_org": "剑河县人民政府",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    {
        "id": 3,
        "name": "吴小勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县委副书记",
        "current_org": "中共剑河县委员会",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    {
        "id": 4,
        "name": "金枫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县委副书记",
        "current_org": "中共剑河县委员会",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    # ── Other Key Leaders ──
    {
        "id": 5,
        "name": "龙景灿",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县人大常委会主任",
        "current_org": "剑河县人大常委会",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    {
        "id": 6,
        "name": "黄琦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县副县长",
        "current_org": "剑河县人民政府",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    {
        "id": 7,
        "name": "肖宗燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县委常委、宣传部部长、统战部部长",
        "current_org": "中共剑河县委员会",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    {
        "id": 8,
        "name": "况再猛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县委常委、组织部部长",
        "current_org": "中共剑河县委员会",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
    {
        "id": 9,
        "name": "吴政富",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "剑河县政协主席",
        "current_org": "政协剑河县委员会",
        "source": "百度百科 剑河县词条 政治栏目 (更新于2024.10)",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共剑河县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黔东南苗族侗族自治州委员会",
        "location": "贵州省黔东南苗族侗族自治州剑河县",
    },
    {
        "id": 2,
        "name": "剑河县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黔东南苗族侗族自治州人民政府",
        "location": "贵州省黔东南苗族侗族自治州剑河县",
    },
    {
        "id": 3,
        "name": "剑河县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "黔东南苗族侗族自治州人大常委会",
        "location": "贵州省黔东南苗族侗族自治州剑河县",
    },
    {
        "id": 4,
        "name": "政协剑河县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协黔东南苗族侗族自治州委员会",
        "location": "贵州省黔东南苗族侗族自治州剑河县",
    },
]

POSITIONS = [
    # ── 杨胜朝 ──
    {
        "person_id": 1,
        "org_id": 1,
        "title": "剑河县委书记",
        "start": "unknown",
        "end": "present",
        "rank": "正县级",
        "note": "截至2024年10月在任，具体任命时间待查",
    },
    # ── 陈林 ──
    {
        "person_id": 2,
        "org_id": 2,
        "title": "剑河县委副书记、县长",
        "start": "unknown",
        "end": "present",
        "rank": "正县级",
        "note": "截至2024年10月在任，具体任命时间待查",
    },
    # ── 吴小勇 ──
    {
        "person_id": 3,
        "org_id": 1,
        "title": "剑河县委副书记",
        "start": "unknown",
        "end": "present",
        "rank": "副县级",
        "note": "截至2024年10月在任",
    },
    # ── 金枫 ──
    {
        "person_id": 4,
        "org_id": 1,
        "title": "剑河县委副书记",
        "start": "unknown",
        "end": "present",
        "rank": "副县级",
        "note": "截至2024年10月在任",
    },
    # ── 龙景灿 ──
    {
        "person_id": 5,
        "org_id": 3,
        "title": "剑河县人大常委会主任",
        "start": "unknown",
        "end": "present",
        "rank": "正县级",
        "note": "截至2024年10月在任",
    },
    # ── 黄琦 ──
    {
        "person_id": 6,
        "org_id": 2,
        "title": "剑河县副县长",
        "start": "unknown",
        "end": "present",
        "rank": "副县级",
        "note": "截至2024年10月在任",
    },
    # ── 肖宗燕 ──
    {
        "person_id": 7,
        "org_id": 1,
        "title": "剑河县委常委、宣传部部长、统战部部长",
        "start": "unknown",
        "end": "present",
        "rank": "副县级",
        "note": "截至2024年10月在任",
    },
    # ── 况再猛 ──
    {
        "person_id": 8,
        "org_id": 1,
        "title": "剑河县委常委、组织部部长",
        "start": "unknown",
        "end": "present",
        "rank": "副县级",
        "note": "截至2024年10月在任",
    },
    # ── 吴政富 ──
    {
        "person_id": 9,
        "org_id": 4,
        "title": "剑河县政协主席",
        "start": "unknown",
        "end": "present",
        "rank": "正县级",
        "note": "截至2024年10月在任",
    },
]

RELATIONSHIPS = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班子",
        "overlap_org": "剑河县四套班子",
        "overlap_period": "2024年至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共剑河县委员会",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共剑河县委员会",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "colleague",
        "context": "县委—县人大协作",
        "overlap_org": "剑河县四套班子",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "剑河县人民政府",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "colleague",
        "context": "县长与县委副书记",
        "overlap_org": "剑河县四套班子",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "colleague",
        "context": "县长与县委副书记",
        "overlap_org": "剑河县四套班子",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与宣传部长",
        "overlap_org": "中共剑河县委员会",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与组织部长",
        "overlap_org": "中共剑河县委员会",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "colleague",
        "context": "县委—县政协协作",
        "overlap_org": "剑河县四套班子",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 7,
        "person_b": 8,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共剑河县委员会",
        "overlap_period": "截至2024年10月",
    },
    {
        "person_a": 5,
        "person_b": 9,
        "type": "colleague",
        "context": "人大—政协正职",
        "overlap_org": "剑河县四套班子",
        "overlap_period": "截至2024年10月",
    },
]

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

SLUG = "剑河县"
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
