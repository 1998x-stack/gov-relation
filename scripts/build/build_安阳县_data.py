#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 安阳县 (Anyang County), 安阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_安阳县
Level: 县
Targets: 县委书记 & 县长

Research constraints:
  - Exa search: rate-limited (free tier exhausted)
  - Baidu: 403/captcha blocked
  - Jina Reader: timed out
  - Google: blocked via available proxies
  - Direct access to www.ayx.gov.cn: successful — core leaders confirmed from
    official leadership page and multiple news articles

Evidence approach:
  - Core leader identities (邢振东 as 县委书记, 马卫 as 县长) confirmed from
    www.ayx.gov.cn official leadership page (https://www.ayx.gov.cn/zwgk/ldxx/)
    and multiple official news articles (2026-02 through 2026-07)
  - Party standing committee confirmed from 第十四次党代会 first plenary session report
  - Deputy rosters confirmed from leadership page
  - Detailed biographies (birth dates, education, early career) mostly unverified due to
    blocked Baidu Baike access
  - This is a partial-evidence artifact following the source_fallbacks playbook:
    create valid artifacts with explicit uncertainty markers

Confirmed sources:
  - https://www.ayx.gov.cn/zwgk/ldxx/  (官方领导信息页面)
  - https://www.ayx.gov.cn/2026/06-29/3650029.html  (第十四届县委一次全会 → 常委会名单)
  - https://www.ayx.gov.cn/2026/07-23/3653536.html  (邢振东讲授党课 → 县委书记确认)
  - https://www.ayx.gov.cn/2026/07-23/3653539.html  (邢振东主持座谈会 → 县委书记、马卫县长确认)
  - https://www.ayx.gov.cn/2026/06-29/3650026.html  (马卫调研 → 县长身份确认)
  - https://www.ayx.gov.cn/2026/03-12/3634315.html  (马卫调研高庄镇 → 县长身份确认)
  - https://www.ayx.gov.cn/2026/02-12/3621510.html  (邢振东走访慰问 → 县委书记身份确认)
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add repo root to path for gov_relation imports
_BASE_DIR_CANDIDATES = [
    Path(__file__).resolve().parent.parent.parent.parent,  # data/tmp/henan_*/
    Path(__file__).resolve().parent.parent.parent,         # scripts/build/
]
BASE_DIR = None
for _c in _BASE_DIR_CANDIDATES:
    if (_c / "gov_relation").is_dir():
        BASE_DIR = _c
        break
if BASE_DIR is None:
    BASE_DIR = _BASE_DIR_CANDIDATES[1]  # fallback
os.chdir(str(BASE_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "安阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE_DIR / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE_DIR / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "邢振东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记、示范区党工委书记",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": "2026年6月当选县委书记"
    },
    {
        "id": 2,
        "name": "马卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长、示范区管委会主任",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": "2026年6月连任县委副书记"
    },
    # ═══════ Party Standing Committee ═══════
    {
        "id": 3,
        "name": "安小丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/2026/06-29/3650029.html",
        "notes": "第十四届县委副书记"
    },
    {
        "id": 4,
        "name": "孙光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/2026/06-29/3650029.html",
        "notes": "第十四届县委常委"
    },
    {
        "id": 5,
        "name": "刘建飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长、党组副书记",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": "常务副县长"
    },
    {
        "id": 6,
        "name": "王文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/2026/06-29/3650029.html",
        "notes": "第十四届县委常委"
    },
    {
        "id": 7,
        "name": "王栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/2026/06-29/3650029.html",
        "notes": "第十四届县委常委"
    },
    {
        "id": 8,
        "name": "石海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/2026/06-29/3650029.html",
        "notes": "第十四届县委常委"
    },
    {
        "id": 9,
        "name": "玄红强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/2026/06-29/3650029.html",
        "notes": "第十四届县委常委"
    },
    {
        "id": 10,
        "name": "张杨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共安阳县委员会",
        "source": "https://www.ayx.gov.cn/2026/06-29/3650029.html",
        "notes": "第十四届县委常委"
    },
    {
        "id": 11,
        "name": "孙永丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": "第十四届县委常委、副县长"
    },
    # ═══════ Government Team ═══════
    {
        "id": 12,
        "name": "蔡光伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "管委会常务副主任",
        "current_org": "安阳县城乡一体化示范区管委会",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": "陪同马卫调研企业"
    },
    {
        "id": 13,
        "name": "周孟亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": ""
    },
    {
        "id": 14,
        "name": "陈亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": "陪同邢振东走访慰问"
    },
    {
        "id": 15,
        "name": "程宝丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": "陪同马卫调研企业"
    },
    {
        "id": 16,
        "name": "张小瑜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": ""
    },
    {
        "id": 17,
        "name": "牛勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "管委会副主任",
        "current_org": "安阳县城乡一体化示范区管委会",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": ""
    },
    {
        "id": 18,
        "name": "李晓波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、政府办公室主任",
        "current_org": "安阳县人民政府",
        "source": "https://www.ayx.gov.cn/zwgk/ldxx/",
        "notes": ""
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共安阳县委员会", "type": "党委", "level": "县处级", "parent": "中共安阳市委", "location": "河南省安阳市安阳县"},
    {"id": 2, "name": "安阳县人民政府", "type": "政府", "level": "县处级", "parent": "安阳市人民政府", "location": "河南省安阳市安阳县"},
    {"id": 3, "name": "安阳县城乡一体化示范区党工委", "type": "党委", "level": "县处级", "parent": "中共安阳市委", "location": "河南省安阳市安阳县"},
    {"id": 4, "name": "安阳县城乡一体化示范区管委会", "type": "政府", "level": "县处级", "parent": "安阳市人民政府", "location": "河南省安阳市安阳县"},
    {"id": 5, "name": "安阳县纪委监委", "type": "党委", "level": "县处级", "parent": "中共安阳县委员会", "location": "河南省安阳市安阳县"},
    {"id": 6, "name": "安阳县公安局", "type": "政府", "level": "乡科级", "parent": "安阳县人民政府", "location": "河南省安阳市安阳县"},
    {"id": 7, "name": "安阳县人民政府办公室", "type": "政府", "level": "乡科级", "parent": "安阳县人民政府", "location": "河南省安阳市安阳县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 邢振东
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "2026年6月22日第十四届县委一次全会当选"},
    {"person_id": 1, "org_id": 3, "title": "示范区党工委书记", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 马卫
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "县处级正职", "note": "2026年6月22日连任县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "县处级正职", "note": "第十四届县委副书记"},
    {"person_id": 2, "org_id": 4, "title": "示范区管委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 县委常委
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "第十四届县委副书记"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "第十四届县委常委"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "县委常委、副县长、党组副书记"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "第十四届县委常委"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "第十四届县委常委"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "第十四届县委常委"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "第十四届县委常委"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "第十四届县委常委"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "县委常委、副县长"},
    # 政府班子
    {"person_id": 12, "org_id": 4, "title": "管委会常务副主任", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "公安局局长", "start": "", "end": "present", "rank": "乡科级正职", "note": "兼副县长"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "分管公安"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "县政府党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "县政府党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "管委会副主任", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 7, "title": "政府办公室主任", "start": "", "end": "present", "rank": "乡科级正职", "note": "县政府党组成员"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Core leadership relationship
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭档，共同主持县委县政府核心工作",
     "overlap_org": "中共安阳县委员会/安阳县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 书记 - 副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记",
     "overlap_org": "中共安阳县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 县长 - 常务副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与常务副县长",
     "overlap_org": "安阳县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 县长 - 副县长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "安阳县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 县委常委会工作关系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委",
     "overlap_org": "中共安阳县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与县委常委",
     "overlap_org": "中共安阳县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与县委常委",
     "overlap_org": "中共安阳县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与县委常委",
     "overlap_org": "中共安阳县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与县委常委",
     "overlap_org": "中共安阳县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与县委常委",
     "overlap_org": "中共安阳县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 县长 - 政府班子成员
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与管委会常务副主任，同时调研企业",
     "overlap_org": "安阳县人民政府/示范区管委会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "安阳县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "安阳县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与县政府党组成员，同时调研企业",
     "overlap_org": "安阳县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "县长与县政府党组成员",
     "overlap_org": "安阳县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
]

# ═══════ Build ═══════════════════════════════════════════════════════════

# Run the build (writes DB + GEXF to staging)
print(f"Building {SLUG} network...")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
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

# Verify output files
for fp in [DB_PATH, GEXF_PATH]:
    if fp.exists():
        print(f"  ✓ {fp.name} ({fp.stat().st_size:,} bytes)")
    else:
        print(f"  ✗ {fp.name} NOT CREATED")
        sys.exit(1)

print(f"\nDone. Staged artifacts in {STAGING_DIR}")
