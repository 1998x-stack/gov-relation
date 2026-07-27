#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 中站区 (Zhongzhan District, Jiaozuo, Henan) leadership network.

中站区 — 河南省焦作市辖区, 焦作市中心城区之一, 总面积162平方公里,
辖10个街道, 常住人口约12万.

Data sources:
- 中站区人民政府门户网站 (www.jzq.gov.cn) — official bio pages (site unreachable during research)
- Media reports and news articles
- Baidu Baike (secondary, unverified during research due to web access limitations)

Confidence notes:
- Current roles: plausible (based on training data; NOT verified against live official sources)
- Identity data for core leaders: unverified — no web source was reachable during this investigation
- Career timelines: mostly unknown; gaps marked explicitly
- All claims should be treated as unverified/plausible until confirmed against official sources

Research date: 2026-07-24
Web access status during research: Exa rate-limited, Baidu 403, jzq.gov.cn timeout, Jina timeout
"""
import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

import sqlite3  # noqa: used indirectly via gov_relation.runner

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────
# process_tmp.py checks for these variable names

STAGING = BASE / "data/tmp/henan_中站区"
DB_PATH = STAGING / "中站区_network.db"
GEXF_PATH = STAGING / "中站区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 区委书记 程宝成
    # Known from training data: 程宝成 served as 中站区委书记
    # Prior role: 中站区委副书记、区长 (promoted to 区委书记)
    {"id": 1, "name": "程宝成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中站区委书记", "current_org": "中共中站区委",
     "source": "培训数据（未从实时官方来源验证）— 需要任前公示和官方领导之窗页面确认"},

    # 区委副书记、区长
    # Based on training data, 赵保霖 was 区长; after 程宝成 became 书记, the 区长 may have changed
    # Need verification from official sources
    {"id": 2, "name": "赵保霖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中站区委副书记、区长", "current_org": "中站区人民政府",
     "source": "培训数据（未从实时官方来源验证）— 需确认是否仍任区长"},

    # ══════════════════════════════════════════════════════════════════
    # Party Committee Standing Members (partial roster, unverified)
    # ══════════════════════════════════════════════════════════════════

    # 区委副书记 (专职副书记, if known)
    {"id": 3, "name": "中站区委专职副书记（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中站区委副书记（专职）", "current_org": "中共中站区委",
     "source": "待从官方来源确认"},

    # 区委常委、常务副区长
    {"id": 4, "name": "常务副区长（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中站区委常委、常务副区长", "current_org": "中站区人民政府",
     "source": "待从官方来源确认"},

    # 区委常委、组织部部长
    {"id": 5, "name": "组织部长（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中站区委常委、组织部部长", "current_org": "中共中站区委组织部",
     "source": "待从官方来源确认"},

    # 区委常委、区纪委书记
    {"id": 6, "name": "纪委书记（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中站区委常委、区纪委书记", "current_org": "中共中站区纪委",
     "source": "待从官方来源确认"},

    # 区委常委、政法委书记
    {"id": 7, "name": "政法委书记（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中站区委常委、政法委书记", "current_org": "中共中站区委政法委",
     "source": "待从官方来源确认"},

    # ══════════════════════════════════════════════════════════════════
    # Deputy 区长 (partial)
    # ══════════════════════════════════════════════════════════════════

    {"id": 8, "name": "副区长（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中站区副区长", "current_org": "中站区人民政府",
     "source": "待从官方来源确认"},

    # ══════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════

    # 前任区委书记 (prior to 程宝成)
    # May include 董红倜 (served as 中站区委书记 before 程宝成)
    {"id": 9, "name": "董红倜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "已离任（前任中站区委书记）", "current_org": "",
     "source": "培训数据 — 需要确认离任时间"},

    # 前任区长 (prior to 赵保霖)
    {"id": 10, "name": "前任区长（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "已离任", "current_org": "",
     "source": "待查"},
]

organizations = [
    {"id": 1, "name": "中共中站区委", "type": "党委", "level": "县处级",
     "parent": "中共焦作市委", "location": "河南省焦作市中站区"},
    {"id": 2, "name": "中站区人民政府", "type": "政府", "level": "县处级",
     "parent": "焦作市人民政府", "location": "河南省焦作市中站区"},
    {"id": 3, "name": "中共中站区纪委", "type": "党委", "level": "县处级",
     "parent": "中共中站区委", "location": "河南省焦作市中站区"},
    {"id": 4, "name": "中共中站区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共中站区委", "location": "河南省焦作市中站区"},
    {"id": 5, "name": "中共中站区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共中站区委", "location": "河南省焦作市中站区"},
    {"id": 6, "name": "中站区人大常委会", "type": "人大", "level": "县处级",
     "parent": "焦作市人大常委会", "location": "河南省焦作市中站区"},
    {"id": 7, "name": "中站区政协", "type": "政协", "level": "县处级",
     "parent": "政协焦作市委员会", "location": "河南省焦作市中站区"},
]

positions = [
    # 程宝成 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中站区委书记", "start": "",
     "end": "present", "rank": "县处级正职",
     "note": "由区长转任区委书记；具体任命日期待查"},
    {"person_id": 1, "org_id": 2, "title": "中站区区长", "start": "",
     "end": "", "rank": "县处级正职",
     "note": "此前担任区长；转任区委书记前的职务"},

    # 赵保霖 — 区长
    {"person_id": 2, "org_id": 2, "title": "中站区区长", "start": "",
     "end": "present", "rank": "县处级正职", "note": "兼任区委副书记；具体任命日期待查"},
    {"person_id": 2, "org_id": 1, "title": "中站区委副书记", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # 董红倜 — 前任区委书记
    {"person_id": 9, "org_id": 1, "title": "中站区委书记", "start": "",
     "end": "", "rank": "县处级正职",
     "note": "前任区委书记；卸任日期待查"},
]

relationships = [
    # ── 区委班子核心 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长搭档（党政正职）", "overlap_org": "中共中站区委",
     "overlap_period": "至今", "strength": "strong",
     "source": "推测（需官方来源确认现任配置）"},

    # ── 前后任关系 ──
    {"person_a": 9, "person_b": 1, "type": "predecessor_successor",
     "context": "董红倜→程宝成：区委书记前后任", "overlap_org": "中共中站区委",
     "overlap_period": "", "strength": "strong",
     "source": "推测（需确认董红倜离任和程宝成接任时间）"},

    # ── 前任区长→新任书记（程宝成本人从区长升书记） ──
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "程宝成此前曾任区长，赵保霖接任", "overlap_org": "中站区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "推测（需官方来源确认）"},
]


def main():
    print(f"=== Building 中站区 network data ===")
    print(f"Target: 区委书记 & 区长")
    print(f"Research date: 2026-07-24")

    run_build(
        slug="中站区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"\n⚠️  WARNING: All data is unverified/plausible.")
    print(f"   Web sources (jzq.gov.cn, Exa, Baidu) were unreachable during this run.")
    print(f"   Verify all claims against official sources before using this data.")
    print("=== Done ===")


if __name__ == "__main__":
    main()
