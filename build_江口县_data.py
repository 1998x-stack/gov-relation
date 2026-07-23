#!/usr/bin/env python3
"""Build script for 江口县 (Jiangkou County, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Research Note (2026-07-23):
  Web sources were partially accessible:
  - Official site www.jiangkou.gov.cn: accessible (homepage, news, leadership activities)
  - Leadership page: no dedicated /zwgk/ldzc/ page found (404)
  - Jina Reader: timed out
  - Baidu Baike: unreachable (403/captcha from this environment)
  - Exa: rate-limited
  - Google/Bing/DuckDuckGo: blocked/transport errors
  - Baidu search: captcha blocked

  Key findings via official site news ("领导活动" column):
  - 县委书记: 辜应强 — confirmed via multiple news articles (讲授思政课, 调研复工复产,
    开展"七一"走访慰问, 调研高考准备工作). Mentioned first/lone in leadership activities,
    pairs with 县长 for major events.
  - 县长: 龙胜文 — confirmed via multiple news articles (主持县政府党组会议和常务会议,
    讲授思政课, 开展走访慰问). Title as 县委副书记、县长 inferred from paired appearances.
  - 县领导: 罗时跃 — appears in 春节/七一走访慰问 (alongside 辜应强、龙胜文、田荣华)
  - 县领导: 田荣华 — appears in same group activities

Sources:
  - https://www.jiangkou.gov.cn/ — official government website (homepage + 领导活动)
  - https://www.jiangkou.gov.cn/xwzx/ldhd/ — leadership activities index
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

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
        "name": "辜应强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江口县委书记",
        "current_org": "中共江口县委员会",
        "source": "江口县政府网 领导活动 2026-07-03《辜应强在江口中学讲授思想政治理论课》; 2026-03《辜应强调研复工复产工作》; 2026-07-01《辜应强龙胜文开展'七一'走访慰问活动》",
    },
    {
        "id": 2,
        "name": "龙胜文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江口县委副书记、县长",
        "current_org": "江口县人民政府",
        "source": "江口县政府网 领导活动 2026-07-07《龙胜文主持召开县政府党组（扩大）会议和常务会议》; 2026-07-06《龙胜文到县第二小学讲授思想政治理论课》",
    },
    {
        "id": 3,
        "name": "罗时跃",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江口县人大常委会主任（推测）",
        "current_org": "江口县人大常委会",
        "source": "江口县政府网 领导活动 2026-07-02《罗时跃走访慰问困难党员、退休基层干部》; 2026-02-14《辜应强龙胜文罗时跃田荣华开展春节走访慰问》",
    },
    {
        "id": 4,
        "name": "田荣华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江口县政协主席（推测）",
        "current_org": "江口县政协",
        "source": "江口县政府网 领导活动 2026-02-14《辜应强龙胜文罗时跃田荣华开展春节走访慰问》",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共江口县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市江口县",
    },
    {
        "id": 2,
        "name": "江口县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市江口县",
    },
    {
        "id": 3,
        "name": "江口县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "铜仁市人大常委会",
        "location": "贵州省铜仁市江口县",
    },
    {
        "id": 4,
        "name": "江口县政协",
        "type": "政协",
        "level": "县",
        "parent": "铜仁市政协",
        "location": "贵州省铜仁市江口县",
    },
]

POSITIONS = [
    # 辜应强 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "江口县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07"},
    # 龙胜文 — 县长
    {"person_id": 2, "org_id": 1, "title": "江口县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "concurrent with 县长 role"},
    {"person_id": 2, "org_id": 2, "title": "江口县县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07"},
    # 罗时跃 — 人大主任（推测）
    {"person_id": 3, "org_id": 3, "title": "江口县人大常委会主任（推测）", "start_date": "", "end_date": "present", "rank": "正县级", "note": "role inferred from activity context; appears after 书记/县长 in official lists"},
    # 田荣华 — 政协主席（推测）
    {"person_id": 4, "org_id": 4, "title": "江口县政协主席（推测）", "start_date": "", "end_date": "present", "rank": "正县级", "note": "role inferred from activity context"},
]

RELATIONSHIPS = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭班子",
        "overlap_org": "中共江口县委员会/江口县人民政府",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委—人大 班子共事",
        "overlap_org": "江口县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "县委—政协 班子共事",
        "overlap_org": "江口县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "政府—人大 班子共事",
        "overlap_org": "江口县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "政府—政协 班子共事",
        "overlap_org": "江口县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "人大—政协 班子共事",
        "overlap_org": "江口县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
]

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

SLUG = "江口县"

TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

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

print(f"Done: {DB_PATH}, {GEXF_PATH}")
