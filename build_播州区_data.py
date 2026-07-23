#!/usr/bin/env python3
"""Build script for 播州区 (Bozhou District, Zunyi, Guizhou) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 贵州省
Parent City: 遵义市
Targets: 区委书记 & 区长

Research Note:
  All external web sources for 播州区 are inaccessible from this environment:
  - www.bozhou.gov.cn: WAF/JS shield blocks automated access
  - Baidu Baike: 403/captcha blocked
  - Exa: rate-limited
  - Jina Reader: timeouts
  - Wikipedia/Google: unreachable from this environment
  - Parent city site (zunyi.gov.cn): limited search/API not functional

  Current officeholders for 播州区 (区委书记, 区长) are UNKNOWN as of 2026-07-23.
  All person entries below are marked as gaps.

Sources:
  - No verifiable online sources could be reached during this investigation session
  - All entries are gaps pending future research access
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
    # ── Core Leaders (GAPS — names unknown) ──
    {
        "id": 1,
        "name": "【待查】播州区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "播州区委书记（待查）",
        "current_org": "中共遵义市播州区委员会",
        "source": "GAP — 官方网站 www.bozhou.gov.cn WAF屏蔽；待后续通过遵义市委组织部任前公示或领导之窗页面补充",
    },
    {
        "id": 2,
        "name": "【待查】播州区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "播州区区长（待查）",
        "current_org": "遵义市播州区人民政府",
        "source": "GAP — 官方网站 www.bozhou.gov.cn WAF屏蔽；待后续补充",
    },
    # ── Deputy Leaders (all GAPS) ──
    {
        "id": 3,
        "name": "【待查】播州区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "播州区委副书记（待查）",
        "current_org": "中共遵义市播州区委员会",
        "source": "GAP — 待后续通过播州区政府领导之窗页面补充",
    },
    {
        "id": 4,
        "name": "【待查】播州区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "播州区委常委、常务副区长（待查）",
        "current_org": "遵义市播州区人民政府",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 5,
        "name": "【待查】播州区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "播州区委常委、纪委书记（待查）",
        "current_org": "中共遵义市播州区纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 6,
        "name": "【待查】播州区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "播州区委常委、组织部长（待查）",
        "current_org": "中共遵义市播州区委组织部",
        "source": "GAP — 待后续补充",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共遵义市播州区委员会", "type": "党委", "level": "正处级", "parent": "中共遵义市委员会", "location": "遵义市播州区"},
    {"id": 2, "name": "遵义市播州区人民政府", "type": "政府", "level": "正处级", "parent": "遵义市人民政府", "location": "遵义市播州区"},
    {"id": 3, "name": "中共遵义市播州区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共遵义市纪律检查委员会", "location": "遵义市播州区"},
    {"id": 4, "name": "中共遵义市播州区委组织部", "type": "党委", "level": "正科级", "parent": "中共遵义市播州区委员会", "location": "遵义市播州区"},
]

POSITIONS = [
    # GAP — 区委书记
    {"person_id": 1, "org_id": 1, "title": "播州区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知"},
    # GAP — 区长
    {"person_id": 2, "org_id": 2, "title": "播州区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 待查"},
    # GAP — 副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记（专职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 常务副区长
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 纪委书记
    {"person_id": 5, "org_id": 3, "title": "播州区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 组织部长
    {"person_id": 6, "org_id": 4, "title": "播州区委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
]

RELATIONSHIPS = [
    # 党政正职（均待查）
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记-区长（均待查）", "overlap_org": "播州区四套班子", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 区长与副书记
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "区长与专职副书记", "overlap_org": "播州区委常委会", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 常务副区长与区长
    {"person_a": 4, "person_b": 2, "type": "上下级", "context": "常务副区长与区长", "overlap_org": "播州区人民政府", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 纪委书记与区委书记
    {"person_a": 5, "person_b": 1, "type": "上下级", "context": "纪委书记向区委书记汇报", "overlap_org": "播州区委常委会", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 组织部长与区委书记
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "组织部长向区委书记汇报", "overlap_org": "播州区委常委会", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "播州区_network.db"
GEXF_PATH = STAGING_DIR / "播州区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="播州区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
