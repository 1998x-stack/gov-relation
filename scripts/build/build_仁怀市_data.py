#!/usr/bin/env python3
"""Build script for 仁怀市 (Renhuai, Zunyi, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县级市
Province: 贵州省
Parent City: 遵义市
Targets: 市委书记 & 市长

Research Note:
  All external web sources for 仁怀市 are inaccessible from this environment:
  - www.renhuai.gov.cn: unreachable (firewall/WAF blocks this environment)
  - Baidu Baike: 403/captcha blocked
  - Exa: rate-limited  
  - Jina Reader: timeouts
  - Wikipedia/Google News: unreachable
  - Parent city site (zunyi.gov.cn): leadership page (ldzc) 404

  Current officeholders for 仁怀市 as of 2026-07-23 cannot be confirmed.
  All person entries below include gap markers and metadata from pre-2024
  training data. Current (2025-2026) incumbents are UNKNOWN.

  Historical figures (pre-2024) sourced from LLM training data memory.
  These are marked as "plausible" or "unverified" — not confirmed.
  The current (2026) 市委书记 and 市长 roles have placeholders pending
  future investigation with working web access.

Sources:
  - No verifiable online sources could be reached during this investigation session
  - Historical names based on pre-2024 training data (unverified for current status)
  - All entries without recent source verification are marked with appropriate confidence
"""

import os
import sys
import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

# Ensure the repo root is on sys.path so gov_relation can be imported
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ═══════════════════════════════════════════════════
    # Core Leaders  
    # ═══════════════════════════════════════════════════

    # ── 市委书记 (GAP — current incumbent unknown) ──
    {
        "id": 1,
        "name": "【待查】仁怀市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "仁怀市委书记（待查）",
        "current_org": "中共仁怀市委员会",
        "source": "GAP — 官方网站 www.renhuai.gov.cn 无法访问；历史人物中常文松（~2021-2024在任）、芦忠于（~2018-2021）曾任该职，但2025-2026年现任未知。待后续通过遵义市委组织部任前公示或领导之窗页面补充。",
    },
    # ── 市长 (GAP — current incumbent unknown) ──
    {
        "id": 2,
        "name": "【待查】仁怀市市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "仁怀市市长（待查）",
        "current_org": "仁怀市人民政府",
        "source": "GAP — 官方网站 www.renhuai.gov.cn 无法访问；历史人物中李颖曾任该职，但2025-2026年现任未知。待后续补充。",
    },
    # ── 市委专职副书记 (GAP) ──
    {
        "id": 3,
        "name": "【待查】仁怀市委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "仁怀市委副书记（待查）",
        "current_org": "中共仁怀市委员会",
        "source": "GAP — 待后续通过仁怀市政府领导之窗页面补充",
    },
    # ── 常务副市长 (GAP) ──
    {
        "id": 4,
        "name": "【待查】仁怀市常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "仁怀市委常委、常务副市长（待查）",
        "current_org": "仁怀市人民政府",
        "source": "GAP — 待后续补充",
    },
    # ── 纪委书记 (GAP) ──
    {
        "id": 5,
        "name": "【待查】仁怀市纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "仁怀市委常委、纪委书记（待查）",
        "current_org": "中共仁怀市纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    # ── 组织部长 (GAP) ──
    {
        "id": 6,
        "name": "【待查】仁怀市委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "仁怀市委常委、组织部长（待查）",
        "current_org": "中共仁怀市委组织部",
        "source": "GAP — 待后续补充",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共仁怀市委员会", "type": "党委", "level": "正处级", "parent": "中共遵义市委员会", "location": "仁怀市"},
    {"id": 2, "name": "仁怀市人民政府", "type": "政府", "level": "正处级", "parent": "遵义市人民政府", "location": "仁怀市"},
    {"id": 3, "name": "中共仁怀市纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共遵义市纪律检查委员会", "location": "仁怀市"},
    {"id": 4, "name": "中共仁怀市委组织部", "type": "党委", "level": "正科级", "parent": "中共仁怀市委员会", "location": "仁怀市"},
    {"id": 5, "name": "仁怀市人大常委会", "type": "人大", "level": "正处级", "parent": "仁怀市", "location": "仁怀市"},
    {"id": 6, "name": "政协仁怀市委员会", "type": "政协", "level": "正处级", "parent": "仁怀市", "location": "仁怀市"},
]

POSITIONS = [
    # GAP — 市委书记
    {"person_id": 1, "org_id": 1, "title": "仁怀市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知；常文松曾任此职至约2024年"},
    # GAP — 市长
    {"person_id": 2, "org_id": 2, "title": "仁怀市市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知；李颖曾任此职"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 待查"},
    # GAP — 副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记（专职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 常务副市长
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 纪委书记
    {"person_id": 5, "org_id": 3, "title": "仁怀市纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 组织部长
    {"person_id": 6, "org_id": 4, "title": "仁怀市委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
]

RELATIONSHIPS = [
    # 党政正职（均待查）
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记-市长（均待查）", "overlap_org": "仁怀市四套班子", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 市长与副书记
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "市长与专职副书记", "overlap_org": "仁怀市委常委会", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 常务副市长与市长
    {"person_a": 4, "person_b": 2, "type": "上下级", "context": "常务副市长与市长", "overlap_org": "仁怀市人民政府", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 纪委书记与市委书记
    {"person_a": 5, "person_b": 1, "type": "上下级", "context": "纪委书记向市委书记汇报", "overlap_org": "仁怀市委常委会", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 组织部长与市委书记
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "组织部长向市委书记汇报", "overlap_org": "仁怀市委常委会", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "仁怀市_network.db"
GEXF_PATH = STAGING_DIR / "仁怀市_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="仁怀市",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
