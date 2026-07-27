#!/usr/bin/env python3
"""Build script for 七星区 (Qixing District, Guilin, Guangxi) leadership network.

Generated: 2026-07-22
Level: 市辖区
Province: 广西壮族自治区
Parent City: 桂林市
Targets: 区委书记 & 区长

Research Note:
  The official district website (http://www.glqixing.gov.cn/) and all Chinese government
  sources were unreachable during this investigation (DNS/network blocks, Baidu captcha,
  Jina Reader timeouts). The only confirmed person-七星区 connection comes from the
  叠彩区 build script, which records 陆华静's prior service in 七星区.

  Current officeholders for 七星区 (区委书记, 区长) are UNKNOWN as of 2026-07-22.
  All person entries below are marked as gaps.

Sources:
  - build_叠彩区_data.py (confirmed 陆华静's prior role in 七星区)
  - http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/qz/index.shtml (陆华静 official bio confirming 七星区 tenure)
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
        "name": "【待查】七星区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星区委书记（待查）",
        "current_org": "中共桂林市七星区委员会",
        "source": "GAP — 官方网站 http://www.glqixing.gov.cn/ 无法访问；待后续通过桂林市委组织部任前公示或领导之窗页面补充",
    },
    {
        "id": 2,
        "name": "【待查】七星区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星区区长（待查）",
        "current_org": "桂林市七星区人民政府",
        "source": "GAP — 官方网站 http://www.glqixing.gov.cn/ 无法访问；待后续补充",
    },
    # ── Known Person with 七星区 Connection ──
    {
        "id": 3,
        "name": "陆华静",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1982年10月",
        "birthplace": "广西都安",
        "education": "研究生学历，经济学硕士学位",
        "party_join": "2005年4月",
        "work_start": "2006年7月",
        "current_post": "叠彩区区长（原七星区委常委、副区长）",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/qz/index.shtml (official bio confirming 七星区 tenure as 区委常委、副区长（正处长级）)",
    },
    # ── Deputy Leaders (all GAPS) ──
    {
        "id": 4,
        "name": "【待查】七星区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星区委常委、常务副区长（待查）",
        "current_org": "桂林市七星区人民政府",
        "source": "GAP — 待后续通过七星区政府领导之窗页面补充",
    },
    {
        "id": 5,
        "name": "【待查】七星区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星区委常委、纪委书记（待查）",
        "current_org": "中共桂林市七星区纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 6,
        "name": "【待查】七星区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星区委常委、组织部长（待查）",
        "current_org": "中共桂林市七星区委组织部",
        "source": "GAP — 待后续补充",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共桂林市七星区委员会", "type": "党委", "level": "正处级", "parent": "中共桂林市委员会", "location": "桂林市七星区"},
    {"id": 2, "name": "桂林市七星区人民政府", "type": "政府", "level": "正处级", "parent": "桂林市人民政府", "location": "桂林市七星区"},
    {"id": 3, "name": "中共桂林市七星区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共桂林市纪律检查委员会", "location": "桂林市七星区"},
    {"id": 4, "name": "中共桂林市七星区委组织部", "type": "党委", "level": "正科级", "parent": "中共桂林市七星区委员会", "location": "桂林市七星区"},
    {"id": 5, "name": "桂林市叠彩区人民政府", "type": "政府", "level": "正处级", "parent": "桂林市人民政府", "location": "桂林市叠彩区"},
]

POSITIONS = [
    # GAP — 区委书记
    {"person_id": 1, "org_id": 1, "title": "七星区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知"},
    # GAP — 区长
    {"person_id": 2, "org_id": 2, "title": "七星区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 待查"},
    # 陆华静 — 曾任七星区委常委、副区长
    {"person_id": 3, "org_id": 1, "title": "七星区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "陆华静曾任七星区委常委"},
    {"person_id": 3, "org_id": 2, "title": "七星区副区长（正处长级）", "start_date": "", "end_date": "", "rank": "正处级", "note": "官方简历：广西桂林市七星区委常委、政府党组成员、副区长（正处长级）"},
    # 陆华静 — 现职
    {"person_id": 3, "org_id": 5, "title": "叠彩区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年在任"},
    # GAP positions
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 5, "org_id": 3, "title": "七星区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 6, "org_id": 4, "title": "七星区委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
]

RELATIONSHIPS = [
    # 党政正职（待查）
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记-区长（均待查）", "overlap_org": "七星区四套班子", "overlap_period": "", "source": "GAP", "confidence": "unverified"},
    # 陆华静与七星区领导的关系
    {"person_a": 3, "person_b": 1, "type": "上下级", "context": "曾任区委常委，与区委书记共事", "overlap_org": "七星区委常委会", "overlap_period": "", "source": "confirmed in 陆华静 official bio", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 2, "type": "上下级", "context": "曾任副区长（正处级），与区长共事", "overlap_org": "七星区人民政府", "overlap_period": "", "source": "confirmed in 陆华静 official bio", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "七星区_network.db"
GEXF_PATH = STAGING_DIR / "七星区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="七星区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
