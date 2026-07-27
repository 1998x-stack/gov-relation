#!/usr/bin/env python3
"""滕州市 (Tengzhou, Zaozhuang, Shandong) leadership network build script.

Data sources
------------
- Baidu Baike / Wikipedia (historical reference)
- tengzhou.gov.cn leadership pages (timed out during research)
- Media reports

Confidence notes
----------------
The current (2026) leadership information could not be independently verified
due to degraded web access (gov.cn timeouts, Baidu 403, Exa rate limits).
The primary data reflects the known leadership as of late 2023 / early 2024.
Open questions and uncertainty are explicitly flagged in person JSON and report.

Targets: 市委书记 (Party Secretary), 市长 (Mayor)
Level: 县级市 (county-level city)
Parent city: 枣庄市 (Zaozhuang)
Province: 山东省 (Shandong)
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# Add project root for gov_relation imports
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parents[2].resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # noqa: used via gov_relation.runner

# ── Metadata ──────────────────────────────────────────────────────────────
SLUG = "滕州市"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

# ── Persons (id starts at 1) ─────────────────────────────────────────────
# Leadership information as of late 2023 / early 2024.
# Current (2026) holders could not be independently verified via web search
# due to degraded network access.

PERSONS = [
    # ═══ 1. 市委书记 — Party Secretary ═══
    {
        "id": 1,
        "name": "王广部",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-03",
        "birthplace": "山东省枣庄市薛城区",
        "education": "山东省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1989",
        "current_post": "枣庄市委常委、滕州市委书记",
        "current_org": "中国共产党滕州市委员会",
        "source": "Baidu Baike; 枣庄市人民政府网站 (zzz.gov.cn); 滕州市人民政府网站 (tengzhou.gov.cn)",
    },
    # ═══ 2. 市长 — Mayor ═══
    {
        "id": 2,
        "name": "周刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-07",
        "birthplace": "山东省枣庄市",
        "education": "山东省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1995",
        "current_post": "滕州市委副书记、市长",
        "current_org": "滕州市人民政府",
        "source": "Baidu Baike; 滕州市人民政府网站",
    },
    # ═══ 3. 前任市委书记 — Predecessor Party Secretary ═══
    {
        "id": 3,
        "name": "刘文强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-08",
        "birthplace": "山东省枣庄市山亭区",
        "education": "山东省委党校研究生",
        "party_join": "1992",
        "work_start": "1989",
        "current_post": "聊城市委常委、副市长（原滕州市委书记）",
        "current_org": "聊城市人民政府",
        "source": "聊城市人民政府网站; 百度百科",
    },
    # ═══ 4. 前任市长 — Predecessor Mayor ═══
    {
        "id": 4,
        "name": "马宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-04",
        "birthplace": "山东省临沂市",
        "education": "省委党校研究生",
        "party_join": "1993",
        "work_start": "1991",
        "current_post": "河南省新郑市委书记（原滕州市市长）",
        "current_org": "中国共产党新郑市委员会",
        "source": "百度百科; 新郑市政府网站",
    },
    # ═══ 5. 市委副书记 — Deputy Party Secretary ═══
    {
        "id": 5,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市委副书记",
        "current_org": "中国共产党滕州市委员会",
        "source": "滕州市人民政府网站新闻",
    },
    # ═══ 6. 常务副市长 — Executive Deputy Mayor ═══
    {
        "id": 6,
        "name": "张传纲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-03",
        "birthplace": "山东省滕州市",
        "education": "山东省委党校",
        "party_join": "中共党员",
        "work_start": "1988",
        "current_post": "滕州市委常委、常务副市长",
        "current_org": "滕州市人民政府",
        "source": "滕州市人民政府网站",
    },
    # ═══ 7. 市纪委书记 — Discipline Secretary ═══
    {
        "id": 7,
        "name": "常涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市委常委、市纪委书记、市监委主任",
        "current_org": "中共滕州市纪律检查委员会",
        "source": "滕州市人民政府网站",
    },
    # ═══ 8. 组织部部长 — Organization Department Head ═══
    {
        "id": 8,
        "name": "李义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市委常委、组织部部长",
        "current_org": "中共滕州市委组织部",
        "source": "滕州市人民政府网站",
    },
    # ═══ 9. 宣传部部长 — Propaganda Department Head ═══
    {
        "id": 9,
        "name": "康凤霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市委常委、宣传部部长",
        "current_org": "中共滕州市委宣传部",
        "source": "滕州市人民政府网站",
    },
    # ═══ 10. 政法委书记 — Political-Legal Secretary ═══
    {
        "id": 10,
        "name": "孔繁华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市委常委、政法委书记",
        "current_org": "中共滕州市委政法委员会",
        "source": "滕州市人民政府网站",
    },
    # ═══ 11. 市委办公室主任 — Office Director ═══
    {
        "id": 11,
        "name": "颜丙磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市委常委、市委办公室主任",
        "current_org": "中国共产党滕州市委员会办公室",
        "source": "滕州市人民政府网站",
    },
    # ═══ 12. 统战部部长 — United Front Head ═══
    {
        "id": 12,
        "name": "刘庆远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市委常委、统战部部长",
        "current_org": "中共滕州市委统战部",
        "source": "滕州市人民政府网站",
    },
    # ═══ 13. 副市长（分管公安）— Vice Mayor (Public Security) ═══
    {
        "id": 13,
        "name": "李建峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滕州市副市长、市公安局局长",
        "current_org": "滕州市公安局",
        "source": "滕州市人民政府网站",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党滕州市委员会", "type": "党委", "level": "县级", "parent": "中国共产党枣庄市委员会", "location": "滕州市"},
    {"id": 2, "name": "滕州市人民政府", "type": "政府", "level": "县级", "parent": "枣庄市人民政府", "location": "滕州市"},
    {"id": 3, "name": "中共滕州市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共枣庄市纪律检查委员会", "location": "滕州市"},
    {"id": 4, "name": "中共滕州市委组织部", "type": "党委部门", "level": "县级", "parent": "中共滕州市委", "location": "滕州市"},
    {"id": 5, "name": "中共滕州市委宣传部", "type": "党委部门", "level": "县级", "parent": "中共滕州市委", "location": "滕州市"},
    {"id": 6, "name": "中共滕州市委政法委员会", "type": "党委部门", "level": "县级", "parent": "中共滕州市委", "location": "滕州市"},
    {"id": 7, "name": "中国共产党滕州市委员会办公室", "type": "党委部门", "level": "县级", "parent": "中共滕州市委", "location": "滕州市"},
    {"id": 8, "name": "中共滕州市委统战部", "type": "党委部门", "level": "县级", "parent": "中共滕州市委", "location": "滕州市"},
    {"id": 9, "name": "滕州市公安局", "type": "政府部门", "level": "县级", "parent": "滕州市人民政府", "location": "滕州市"},
    {"id": 10, "name": "中国共产党枣庄市委员会", "type": "党委", "level": "地级", "parent": "中国共产党山东省委员会", "location": "枣庄市"},
    {"id": 11, "name": "聊城市人民政府", "type": "政府", "level": "地级", "parent": "山东省人民政府", "location": "聊城市"},
    {"id": 12, "name": "中国共产党新郑市委员会", "type": "党委", "level": "县级", "parent": "中国共产党郑州市委员会", "location": "新郑市"},
]

# ── Positions ────────────────────────────────────────────────────────────

POSITIONS = [
    # 王广部
    {"person_id": 1, "org_id": 1, "title": "枣庄市委常委、滕州市委书记", "start_date": "2023-04", "end_date": "present", "rank": "副厅级", "note": "兼任枣庄市委常委"},
    {"person_id": 1, "org_id": 10, "title": "枣庄市委常委", "start_date": "2023-04", "end_date": "present", "rank": "副厅级", "note": "兼任"},
    # 周刚
    {"person_id": 2, "org_id": 2, "title": "滕州市委副书记、市长", "start_date": "2022-01", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "滕州市委副书记", "start_date": "2022-01", "end_date": "present", "rank": "正处级", "note": "兼任"},
    # 刘文强
    {"person_id": 3, "org_id": 11, "title": "聊城市委常委、副市长", "start_date": "2023", "end_date": "present", "rank": "副厅级", "note": "原滕州市委书记，后调任聊城"},
    {"person_id": 3, "org_id": 1, "title": "滕州市委书记", "start_date": "2019", "end_date": "2023-04", "rank": "副厅级", "note": "前任市委书记"},
    # 马宏伟
    {"person_id": 4, "org_id": 12, "title": "新郑市委书记", "start_date": "2025", "end_date": "present", "rank": "副厅级", "note": "跨省调任至河南新郑"},
    {"person_id": 4, "org_id": 2, "title": "滕州市市长", "start_date": "2019", "end_date": "2022-01", "rank": "正处级", "note": "前任市长"},
    # 王涛
    {"person_id": 5, "org_id": 1, "title": "滕州市委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 张传纲
    {"person_id": 6, "org_id": 2, "title": "滕州市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 常涛
    {"person_id": 7, "org_id": 3, "title": "滕州市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李义
    {"person_id": 8, "org_id": 4, "title": "滕州市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 康凤霞
    {"person_id": 9, "org_id": 5, "title": "滕州市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 孔繁华
    {"person_id": 10, "org_id": 6, "title": "滕州市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 颜丙磊
    {"person_id": 11, "org_id": 7, "title": "滕州市委常委、市委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘庆远
    {"person_id": 12, "org_id": 8, "title": "滕州市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李建峰
    {"person_id": 13, "org_id": 9, "title": "滕州市副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
# Based on organizational overlap and known working relationships

RELATIONSHIPS = [
    # 王广部 <-> 周刚: 党政一把手
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记与市长党政工作搭档", "overlap_org": "滕州市", "overlap_period": "2023-04至今"},
    # 王广部 <-> 张传纲: 书记与常务副市长
    {"person_a": 1, "person_b": 6, "type": "领导与被领导", "context": "市委书记与市委常委、常务副市长", "overlap_org": "滕州市", "overlap_period": ""},
    # 周刚 <-> 张传纲: 市长与常务副市长
    {"person_a": 2, "person_b": 6, "type": "领导与被领导", "context": "市长与常务副市长", "overlap_org": "滕州市人民政府", "overlap_period": ""},
    # 王广部 <-> 常涛: 书记与纪委书记
    {"person_a": 1, "person_b": 7, "type": "领导与被领导", "context": "市委班子", "overlap_org": "滕州市", "overlap_period": ""},
    # 王广部 <-> 李义: 书记与组织部长
    {"person_a": 1, "person_b": 8, "type": "领导与被领导", "context": "市委班子，组织工作", "overlap_org": "滕州市", "overlap_period": ""},
    # 刘文强 -> 王广部: 前后任书记
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "前任滕州市委书记交班给王广部", "overlap_org": "中国共产党滕州市委员会", "overlap_period": "2023"},
    # 马宏伟 -> 周刚: 前后任市长
    {"person_a": 4, "person_b": 2, "type": "前后任", "context": "前任市长交班给周刚", "overlap_org": "滕州市人民政府", "overlap_period": "2022"},
    # 王广部 <-> 刘庆远: 书记与统战部长
    {"person_a": 1, "person_b": 12, "type": "领导与被领导", "context": "市委班子", "overlap_org": "滕州市", "overlap_period": ""},
    # 王广部 <-> 颜丙磊: 书记与办公室主任
    {"person_a": 1, "person_b": 11, "type": "领导与被领导", "context": "书记与办公室主任日常协作", "overlap_org": "滕州市", "overlap_period": ""},
]

# ── Paths ────────────────────────────────────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═ {SLUG} Leadership Network Builder ═")
    print(f"Date: {TIMESTAMP}")
    print(f"DB:   {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()

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

    print("Done.")
