#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 商水县 (Shangshui County), 周口市, 河南省.

Investigation date: 2026-08-03
Task ID: henan_商水县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.shangshui.gov.cn/ — official government website
  - Official leadership page: /sitesources/ssx/page_pc/zwgk/ldzc/list1.html (5 government leaders)
  - News article confirming 刘贡献 as 县委书记: /sitesources/ssx/page_pc/xwdt/ssyw/article046dc2ec33f448459fe5378d581ad2a2.html
  - News articles confirming 张丽娜 as 县长 via multiple 县政府常务会议 reports (2026-06 through 2026-07)
  - Bio pages for 张丽娜, 金溪, 王宾, 潘子建, 郭威 on official leadership page

Confidence notes:
  - 刘贡献 (县委书记): confirmed via official government news article dated 2026-07-27.
    No biographical details (birth year, education, career timeline) available — official site does not publish party secretary bios.
  - 张丽娜 (县长): confirmed via official bio page and multiple news articles (2026-06-16 through 2026-07-16).
    No biographical details (birth year, birthplace, education, career timeline) available.
  - Government deputy leadership: 5 confirmed from official site with work division, no biographical details.
  - Party Standing Committee: partial — 刘贡献, 张丽娜, 金溪 confirmed as 常委; others unknown.
  - Full biographical detail is unavailable from any accessible source (Baidu Baike blocked, government bios lack personal details).
  - This is a partial-evidence artifact: leader identities and government team are confirmed.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "商水县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "刘贡献",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共商水县委员会",
        "source": "Confirmed via official news 2026-07-27: 刘贡献 as 县委书记 调研农业生产: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/xwdt/ssyw/article046dc2ec33f448459fe5378d581ad2a2.html"
    },
    {
        "id": 2,
        "name": "张丽娜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "商水县人民政府",
        "source": "Official bio: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/zwgk/ldzc/article2f8bf3b80d53459293617ecb42217261.html | Leadership page: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/zwgk/ldzc/list1.html"
    },
    # ═══════ Government Leadership ═══════
    {
        "id": 3,
        "name": "金溪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府常务副县长",
        "current_org": "商水县人民政府",
        "source": "Official bio: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/zwgk/ldzc/article9BBF0FDDD3B54834B72788F95F2AAFF1.html"
    },
    {
        "id": 4,
        "name": "王宾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "商水县人民政府",
        "source": "Official bio: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/zwgk/ldzc/articlee5061eba928044ed89f82a1268edf80c.html"
    },
    {
        "id": 5,
        "name": "潘子建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、县公安局长",
        "current_org": "商水县人民政府",
        "source": "Official bio: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/zwgk/ldzc/article8db3fc6302d742768f4ac3c011b2baef.html"
    },
    {
        "id": 6,
        "name": "郭威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、县政府办公室主任",
        "current_org": "商水县人民政府",
        "source": "Official bio: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/zwgk/ldzc/article3648E6F05AAB4ED0AE8A7A9850BED336.html"
    },
    # ═══════ Meeting-Attending Leaders (roles not fully specified) ═══════
    {
        "id": 7,
        "name": "陈方方",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "商水县人民政府",
        "source": "Attended 2026-06-16 县政府常务会议, listed alongside 金溪 et al.: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/xwdt/ssyw/article987fb94bb57e4e4da8316566a9025175.html"
    },
    {
        "id": 8,
        "name": "董志伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "商水县人民政府",
        "source": "Attended 2026-07-01 meeting and 2026-06-16 县政府常务会议. Listed alongside 金溪 et al."
    },
    {
        "id": 9,
        "name": "朱宏伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "商水县人民政府",
        "source": "Attended 2026-06-16 县政府常务会议: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/xwdt/ssyw/article987fb94bb57e4e4da8316566a9025175.html"
    },
    {
        "id": 10,
        "name": "张彦兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "商水县人民政府",
        "source": "Attended 2026-06-16 县政府常务会议: Same source as 朱宏伟"
    },
    {
        "id": 11,
        "name": "马三华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "商水县人民政府",
        "source": "Attended 2026-07-01 全县工作会议: https://www.shangshui.gov.cn/sitesources/ssx/page_pc/xwdt/ssyw/article394cf4b10ea04878a32e59bf48d9b95d.html"
    },
    {
        "id": 12,
        "name": "张庆华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共商水县委员会",
        "source": "Listed at 2026-07-01 全县工作会议 alongside 金溪 et al: Same source as 马三华. Exact title unknown - may be 县委副书记 or other leadership role."
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {
        "id": ORG_OFFSET + 1,
        "name": "中共商水县委员会",
        "type": "party",
        "level": "县",
        "parent": "中共周口市委",
        "location": "河南省周口市商水县"
    },
    {
        "id": ORG_OFFSET + 2,
        "name": "商水县人民政府",
        "type": "government",
        "level": "县",
        "parent": "周口市人民政府",
        "location": "河南省周口市商水县"
    },
    {
        "id": ORG_OFFSET + 3,
        "name": "商水县公安局",
        "type": "government",
        "level": "县",
        "parent": "商水县人民政府",
        "location": "河南省周口市商水县"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 刘贡献
    {"person_id": 1, "org_id": ORG_OFFSET + 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "Confirmed active as of 2026-07-27"},
    # 张丽娜
    {"person_id": 2, "org_id": ORG_OFFSET + 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "Confirmed as of 2026-05-29 bio page"},
    {"person_id": 2, "org_id": ORG_OFFSET + 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 金溪
    {"person_id": 3, "org_id": ORG_OFFSET + 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王宾
    {"person_id": 4, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 潘子建
    {"person_id": 5, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": ORG_OFFSET + 3, "title": "公安局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郭威
    {"person_id": 6, "org_id": ORG_OFFSET + 2, "title": "县政府党组成员、办公室主任", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 陈方方 (县政府领导)
    {"person_id": 7, "org_id": ORG_OFFSET + 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "Specific title not confirmed"},
    # 董志伟
    {"person_id": 8, "org_id": ORG_OFFSET + 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "Specific title not confirmed"},
    # 朱宏伟
    {"person_id": 9, "org_id": ORG_OFFSET + 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "Specific title not confirmed"},
    # 张彦兵
    {"person_id": 10, "org_id": ORG_OFFSET + 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "Specific title not confirmed"},
    # 马三华
    {"person_id": 11, "org_id": ORG_OFFSET + 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "Specific title not confirmed"},
    # 张庆华
    {"person_id": 12, "org_id": ORG_OFFSET + 1, "title": "县领导", "start": "", "end": "present", "rank": "副处级", "note": "Likely party committee role, specific title unknown"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Leadership team works together (all officers of the same county government)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档",
        "overlap_org": "中共商水县委员会",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # Core leadership team overlaps
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长",
        "overlap_org": "中共商水县委员会",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # All government team members overlap
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "县长与副县长王宾共同任职",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "县长与副县长潘子建共同任职",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "县长与县政府办主任共事",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # Cross-deputy overlaps (working together in government meetings)
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "王宾与潘子建在县政府常务会议共事",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 4, "person_b": 3,
        "type": "overlap",
        "context": "王宾与金溪在县政府共事",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 5, "person_b": 3,
        "type": "overlap",
        "context": "潘子建与金溪在县政府共事",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # Other attending leaders with core team
    {
        "person_a": 7, "person_b": 2,
        "type": "overlap",
        "context": "陈方方出席县长主持的县政府常务会议",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-06",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 8, "person_b": 2,
        "type": "overlap",
        "context": "董志伟出席县长主持的全县工作会议",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 9, "person_b": 2,
        "type": "overlap",
        "context": "朱宏伟出席县长主持的县政府常务会议",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-06",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 10, "person_b": 2,
        "type": "overlap",
        "context": "张彦兵出席县长主持的县政府常务会议",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-06",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 11, "person_b": 2,
        "type": "overlap",
        "context": "马三华出席县长主持的全县工作会议",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 12, "person_b": 2,
        "type": "overlap",
        "context": "张庆华出席县长主持的全县工作会议",
        "overlap_org": "商水县人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "plausible"
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Database + GEXF build
# ═══════════════════════════════════════════════════════════════════════════

def build():
    """Build SQLite database and GEXF graph."""
    sys.path.insert(0, str(STAGING_DIR.parents[2]))
    from gov_relation.runner import run_build

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )


def verify():
    """Verify output files exist and have correct structure."""
    import sqlite3
    errors = []

    # Check DB exists and has expected tables
    if not DB_PATH.exists():
        errors.append(f"Database not found: {DB_PATH}")
    else:
        conn = sqlite3.connect(str(DB_PATH))
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )]
        expected = ["persons", "organizations", "positions", "relationships"]
        for t in expected:
            if t not in tables:
                errors.append(f"Missing table: {t}")
        count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        print(f"  Persons: {count}")
        count = conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
        print(f"  Organizations: {count}")
        count = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
        print(f"  Positions: {count}")
        count = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        print(f"  Relationships: {count}")
        conn.close()

    # Check GEXF
    if not GEXF_PATH.exists():
        errors.append(f"GEXF not found: {GEXF_PATH}")
    else:
        content = GEXF_PATH.read_text("utf-8")
        if '<gexf' not in content:
            errors.append("GEXF missing <gexf> tag")
        if '<nodes>' not in content:
            errors.append("GEXF missing <nodes>")
        if '</gexf>' not in content:
            errors.append("GEXF missing closing </gexf>")

    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        return False
    print("  Verification: PASSED")
    return True


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    build()
    print("\nVerifying...")
    if verify():
        print("\nDone. Files created:")
        print(f"  DB:    {DB_PATH}")
        print(f"  GEXF:  {GEXF_PATH}")
    else:
        print("\nFAILED: verification errors")
        sys.exit(1)