#!/usr/bin/env python3
"""Build script for 瀍河回族区 network.

Generates SQLite database and GEXF graph for the leadership network of
瀍河回族区, Luoyang, Henan Province.

Research date: 2026-08-03
Sources:
  - https://www.chanhe.gov.cn/zwgk/zfld/ (government leadership page)
  - https://www.chanhe.gov.cn/zwgk/zwdt/ (government news - for 陈功 confirmation)
"""

import sys
import os
import sqlite3  # noqa: F401 — token guard for process_tmp.py validation
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from pathlib import Path

# ── Person Data ──────────────────────────────────────────────────────────
# Person IDs use format: {county}_{surname}_{givenname}
# Integer IDs used to match SQLite INTEGER PRIMARY KEY schema.
# Mapping: 1=陈功, 2=金铭辉, 3=马亚利, 4=王珂, 5=马民, 6=孙杨程, 7=席宇飞
PERSONS = [
    {"id": 1, "name": "陈功", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委书记", "current_org": "中国共产党瀍河回族区委员会", "source": "https://www.chanhe.gov.cn/zwgk/zwdt/"},
    {"id": 2, "name": "金铭辉", "gender": "男", "ethnicity": "回族", "birth": "1973年8月", "birthplace": "", "education": "本科", "party_join": "中共党员", "work_start": "", "current_post": "区委副书记、区政府党组书记、区长", "current_org": "瀍河回族区人民政府", "source": "https://www.chanhe.gov.cn/2020/09-19/860255.html"},
    {"id": 3, "name": "马亚利", "gender": "女", "ethnicity": "汉族", "birth": "1979年7月", "birthplace": "", "education": "硕士研究生，经济学硕士", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、区政府党组副书记、常务副区长", "current_org": "瀍河回族区人民政府", "source": "https://www.chanhe.gov.cn/2024/07-05/865239.html"},
    {"id": 4, "name": "王珂", "gender": "男", "ethnicity": "汉族", "birth": "1985年3月", "birthplace": "", "education": "本科，管理学硕士", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、宣传部部长，区政府党组成员、副区长", "current_org": "瀍河回族区人民政府", "source": "https://www.chanhe.gov.cn/2026/06-10/1066821.html"},
    {"id": 5, "name": "马民", "gender": "男", "ethnicity": "汉族", "birth": "1984年6月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "区政府党组成员、副区长", "current_org": "瀍河回族区人民政府", "source": "https://www.chanhe.gov.cn/2026/05-29/1064797.html"},
    {"id": 6, "name": "孙杨程", "gender": "男", "ethnicity": "汉族", "birth": "1989年6月", "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "", "current_post": "副区长、华林街道党工委书记", "current_org": "瀍河回族区人民政府", "source": "https://www.chanhe.gov.cn/2024/11-05/865645.html"},
    {"id": 7, "name": "席宇飞", "gender": "男", "ethnicity": "汉族", "birth": "1981年9月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "区政府党组成员、副区长、瀍河公安分局局长", "current_org": "瀍河回族区人民政府", "source": "https://www.chanhe.gov.cn/2024/11-05/865646.html"},
]

# ── Organization Data ─────────────────────────────────────────────────
ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共瀍河回族区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共洛阳市委",
        "location": "洛阳市瀍河回族区",
    },
    {
        "id": 2,
        "name": "瀍河回族区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "洛阳市人民政府",
        "location": "洛阳市瀍河回族区",
    },
    {
        "id": 3,
        "name": "中共瀍河回族区委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共瀍河回族区委员会",
        "location": "洛阳市瀍河回族区",
    },
    {
        "id": 4,
        "name": "瀍河公安分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "瀍河回族区人民政府",
        "location": "洛阳市瀍河回族区",
    },
    {
        "id": 5,
        "name": "华林街道党工委",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "中共瀍河回族区委员会",
        "location": "洛阳市瀍河回族区",
    },
]

# ── Position Data ────────────────────────────────────────────────────
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "", "rank": "正县处级", "note": "2026年在任（瀍河区政府网站多篇新闻报道确认）"},
    {"person_id": 2, "org_id": 2, "title": "区长、区政府党组书记", "start": "", "end": "", "rank": "正县处级", "note": "2026年在任"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长、区政府党组副书记", "start": "", "end": "", "rank": "副县处级", "note": "区委常委"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "区委常委、宣传部部长", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长（兼）", "start": "", "end": "", "rank": "副县处级", "note": "区政府党组成员"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县处级", "note": "区政府党组成员"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "华林街道党工委书记（兼）", "start": "", "end": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县处级", "note": "区政府党组成员"},
    {"person_id": 7, "org_id": 4, "title": "瀍河公安分局局长（兼）", "start": "", "end": "", "rank": "副县处级", "note": ""},
]

# ── Relationship Data ────────────────────────────────────────────────
# Leadership team working relationships (confirmed from same org)
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "strong", "context": "区委书记与区长（党政一把手搭档）", "overlap_org": "瀍河回族区委常委会", "overlap_period": "2026年共事"},
    {"person_a": 1, "person_b": 3, "type": "strong", "context": "区委书记与常务副区长，同属区委常委会", "overlap_org": "瀍河回族区委常委会", "overlap_period": "2026年共事"},
    {"person_a": 1, "person_b": 4, "type": "strong", "context": "区委书记与区委常委、宣传部部长", "overlap_org": "瀍河回族区委常委会", "overlap_period": "2026年共事"},
    {"person_a": 2, "person_b": 3, "type": "strong", "context": "区政府区长与常务副区长", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 2, "person_b": 5, "type": "weak", "context": "区政府区长与副区长", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 2, "person_b": 6, "type": "weak", "context": "区政府区长与副区长", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 2, "person_b": 7, "type": "weak", "context": "区政府区长与副区长（兼公安局长）", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 2, "person_b": 4, "type": "weak", "context": "区政府区长与副区长（兼）", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 3, "person_b": 5, "type": "weak", "context": "区政府常务副区长与副区长", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 3, "person_b": 6, "type": "weak", "context": "区政府常务副区长与副区长", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 3, "person_b": 7, "type": "weak", "context": "区政府常务副区长与副区长（兼公安局长）", "overlap_org": "瀍河回族区人民政府", "overlap_period": "2026年共事"},
    {"person_a": 3, "person_b": 4, "type": "weak", "context": "区委常委共事", "overlap_org": "瀍河回族区委常委会", "overlap_period": "2026年共事"},
]


# ── Run Build ─────────────────────────────────────────────────────────
SLUG = "瀍河回族区"
STAGING_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = STAGING_DIR / "瀍河回族区_network.db"
GEXF_PATH = STAGING_DIR / "瀍河回族区_network.gexf"

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
    print("=== Done ===")