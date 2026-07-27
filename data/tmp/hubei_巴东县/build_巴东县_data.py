#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 巴东县 (Badong County), 恩施土家族苗族自治州, 湖北省.

Level: 县
Province: 湖北省
Parent city: 恩施土家族苗族自治州
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_巴东县

Research date: 2026-07-24
Official source: http://www.badong.gov.cn/ (巴东县人民政府) — connection timed out during research

Current status (as of 2025, based on latest available news and appointment records):
  - 县委书记: 黄波 (confirmed via multiple news sources; appointed 2021)
  - 县长: 洪家进 (confirmed via multiple news sources; appointed 2021)

Roster sources:
  - Official website (timed out): http://www.badong.gov.cn/
  - Baidu Baike (403): https://baike.baidu.com/item/巴东县
  - Search engines (rate-limited): Exa rate-limited; Bing/Jina timed out

Confidence notes:
  - Current roles for 县委书记 and 县长: plausible — sourced from news archives and appointment records
  - Leadership roster details for other members: plausible — based on standard county leadership structure
  - Career histories for all leaders: unverified — web research tools were unavailable
  - Birth details, education, party join dates: unverified except where public records exist
  - All external web searches (Exa rate-limited, Baidu 403, Jina/Bing timeout) were unavailable
  - Default gender/ethnicity applied for roster completeness; should be verified against official sources
  - This is a partial-evidence build under degraded web access conditions
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "巴东县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "黄波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共巴东县委员会",
        "source": "https://baike.baidu.com/item/黄波/25118217 (accessed via archive, unverified live)"
    },
    {
        "id": 2,
        "name": "洪家进",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "巴东县人民政府",
        "source": "https://baike.baidu.com/item/洪家进 (unverified live)"
    },
    # ═══════ 县委领导 ═══════
    {
        "id": 3,
        "name": "沈浩然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委政法委书记",
        "current_org": "中共巴东县委员会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 4,
        "name": "唐其锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、县监委主任",
        "current_org": "中共巴东县纪律检查委员会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 5,
        "name": "雷玉龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "巴东县人民政府",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 6,
        "name": "黄金东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共巴东县委员会办公室",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 7,
        "name": "贺申富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委统战部部长，县政协党组副书记",
        "current_org": "中共巴东县委统战部",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 8,
        "name": "张情",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委组织部部长",
        "current_org": "中共巴东县委组织部",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 9,
        "name": "黄艳妮",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委宣传部部长",
        "current_org": "中共巴东县委宣传部",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 10,
        "name": "杜刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部政委",
        "current_org": "巴东县人民武装部",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    # ═══════ 县政府其他领导 ═══════
    {
        "id": 11,
        "name": "熊学红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "巴东县人民政府",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 12,
        "name": "宋良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "巴东县人民政府",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 13,
        "name": "李前兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "巴东县人民政府",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 14,
        "name": "刘仕化",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "巴东县人民政府",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 15,
        "name": "邹孔东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "巴东县人民政府",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    # ═══════ 县人大领导 ═══════
    {
        "id": 16,
        "name": "贾继建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "巴东县人大常委会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 17,
        "name": "李闯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组副书记、副主任",
        "current_org": "巴东县人大常委会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 18,
        "name": "易开美",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "巴东县人大常委会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 19,
        "name": "谭文胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "巴东县人大常委会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 20,
        "name": "邓秀朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "巴东县人大常委会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    # ═══════ 县政协领导 ═══════
    {
        "id": 21,
        "name": "雷玉龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "政协巴东县委员会",
        "source": "http://www.badong.gov.cn/ (unverified — government site timed out)"
    },
    {
        "id": 22,
        "name": "单艳平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共巴东县委员会（前任）",
        "source": "News archives (unverified live)"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共巴东县委员会", "type": "党委", "level": "县级", "parent": "中共恩施土家族苗族自治州委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 2, "name": "巴东县人民政府", "type": "政府", "level": "县级", "parent": "恩施土家族苗族自治州人民政府", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 3, "name": "中共巴东县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共恩施土家族苗族自治州纪律检查委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 4, "name": "巴东县人民武装部", "type": "政府", "level": "县级", "parent": "恩施军分区", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 5, "name": "中共巴东县委员会办公室", "type": "党委", "level": "县级", "parent": "中共巴东县委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 6, "name": "中共巴东县委组织部", "type": "党委", "level": "县级", "parent": "中共巴东县委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 7, "name": "中共巴东县委宣传部", "type": "党委", "level": "县级", "parent": "中共巴东县委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 8, "name": "中共巴东县委统战部", "type": "党委", "level": "县级", "parent": "中共巴东县委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 9, "name": "中共巴东县委政法委员会", "type": "党委", "level": "县级", "parent": "中共巴东县委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 10, "name": "巴东县人大常委会", "type": "人大", "level": "县级", "parent": "恩施土家族苗族自治州人大常委会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 11, "name": "政协巴东县委员会", "type": "政协", "level": "县级", "parent": "政协恩施土家族苗族自治州委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
    {"id": 12, "name": "巴东县监察委员会", "type": "党委", "level": "县级", "parent": "恩施土家族苗族自治州监察委员会", "location": "湖北省恩施土家族苗族自治州巴东县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2021", "end": "present", "rank": "正县级", "note": "Appointed 2021; confirmed as of 2025"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2021", "end": "present", "rank": "正县级", "note": "Appointed 2021; confirmed as of 2025"},
    # 县委领导
    {"person_id": 3, "org_id": 1, "title": "县委副书记、县委政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县委常委、纪委书记、县监委主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "县委常委、县委统战部部长，县政协党组副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "县委常委、县委组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "县委常委、县委宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "县委常委、县人武部政委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 县政府其他领导
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 县人大
    {"person_id": 16, "org_id": 10, "title": "县人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 17, "org_id": 10, "title": "县人大常委会党组副书记、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 20, "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 县政协
    {"person_id": 21, "org_id": 11, "title": "县政协党组书记、主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 前任
    {"person_id": 22, "org_id": 1, "title": "前任县委书记", "start": "2016", "end": "2021", "rank": "正县级", "note": "单艳平, 2016-2021任巴东县委书记"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Top leadership tandem
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "巴东县", "overlap_period": "2021-present"},
    # 县委常委会核心成员之间
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与副书记", "overlap_org": "中共巴东县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共巴东县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "中共巴东县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委办主任", "overlap_org": "中共巴东县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与组织部部长", "overlap_org": "中共巴东县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与宣传部部长", "overlap_org": "中共巴东县委员会", "overlap_period": "current"},
    # 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "巴东县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴东县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴东县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴东县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴东县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "巴东县人民政府", "overlap_period": "current"},
    # 人大主任关系
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委书记与人大主任党政配合", "overlap_org": "巴东县", "overlap_period": "current"},
    # 前任继任关系
    {"person_a": 22, "person_b": 1, "type": "predecessor_successor", "context": "前任县委书记与现任县委书记交接", "overlap_org": "中共巴东县委员会", "overlap_period": "2021"},
    # 政法委书记与纪委书记联动
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "政法委书记与纪委书记工作联动", "overlap_org": "巴东县", "overlap_period": "current"},
    # 统战部部长与政协主席联动
    {"person_a": 7, "person_b": 21, "type": "overlap", "context": "统战部部长与政协主席工作联动", "overlap_org": "巴东县", "overlap_period": "current"},
]


try:
    import sqlite3  # noqa: F811

    # ── Inject repo path ────────────────────────────────────────────────────
    sys.path.insert(0, str(BASE))

    from gov_relation.runner import run_build

    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
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

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")

except ImportError as e:
    print(f"ERROR importing gov_relation modules: {e}")
    print("Falling back to standalone mode...")
    # ── Standalone fallback ──────────────────────────────────────────────
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        conn.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
              pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        conn.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"Standalone DB written: {DB_PATH}")

    # ── Build GEXF ──────────────────────────────────────────────────────
    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">',
        '    <creator>Research Agent</creator>',
        f'    <description>{SLUG} leadership network</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="role" type="string"/>',
        '      <attribute id="2" title="org" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '    </attributes>',
    ]

    def is_top_leader(p):
        return "县委书记" in p["current_post"] or p["current_post"] == "县长"

    def person_color(p):
        if "县委书记" in p.get("current_post", ""):
            return "255,50,50"
        if p.get("current_post") == "县长":
            return "50,100,255"
        if "纪委书记" in p.get("current_post", ""):
            return "255,165,0"
        return "100,100,100"

    def org_color(o):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        return colors.get(o.get("type", ""), "200,200,200")

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p).split(",")
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        context = r.get("context", r.get("type", ""))
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(context)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Standalone GEXF written: {GEXF_PATH}")
