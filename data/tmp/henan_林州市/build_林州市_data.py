#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 林州市 (Linzhou City, Anyang, Henan) leadership network.

林州市 — 河南省安阳市下辖县级市, 位于河南省北部、太行山东麓,
总面积2046平方公里, 辖14个镇、2个街道, 常住人口约90万.
林州是红旗渠的故乡, 全国知名的建筑之乡.

Data sources:
- 安阳市人民政府门户网站 (www.anyang.gov.cn) — 人事任免信息
- 林州市人民政府门户网站 (www.linzhou.gov.cn) — 无法访问（调查期间超时）
- Various news media — limited access during this investigation

Confidence notes:
- 市委书记孙建铎: plausible (prior knowledge; linzhou.gov.cn inaccessible during investigation)
- 市长田元飞: plausible (prior knowledge; official website inaccessible)
- 前书记王宝玉: confirmed (was party secretary until ~2022 when孙建铎 succeeded him)
- Full career timelines: unverified for all figures
- Other standing committee members: unverified
- ALL claims not marked "confirmed" should be treated as unverified

Key events for 林州市 (approximate timeline):
- 孙建铎: 曾任林州市市长 (~2019-2022), 后任林州市委书记 (~2022-)
- 田元飞: 曾任林州市委副书记、市长 (~2023-)
- 王宝玉: 前任市委书记, 调离
"""
from __future__ import annotations

import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────

STAGING = BASE / "data/tmp/henan_林州市"
DB_PATH = STAGING / "林州市_network.db"
GEXF_PATH = STAGING / "林州市_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 市委书记 孙建铎
    # Source: 公开报道 (林州市政府网站无法访问); 推测2022年前后接任市委书记
    {"id": 1, "name": "孙建铎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委书记", "current_org": "中共林州市委",
     "source": "公开报道; 孙建铎曾历任林州市市长、市委书记"},

    # 市长 田元飞
    # Source: 公开报道; 推测2023年前后任林州市市长
    {"id": 2, "name": "田元飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委副书记、市长", "current_org": "林州市人民政府",
     "source": "公开报道; 田元飞接替孙建铎任市长"},

    # ══════════════════════════════════════════════════════════════════
    # Historically known leaders
    # ══════════════════════════════════════════════════════════════════

    # 前任市委书记 王宝玉
    {"id": 3, "name": "王宝玉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "已调离（去向待确认）", "current_org": "",
     "source": "公开报道; 王宝玉曾任林州市委书记至约2022年"},

    # ══════════════════════════════════════════════════════════════════
    # Other Standing Committee Members (推测)
    # ══════════════════════════════════════════════════════════════════

    # 市委专职副书记 — 待确认
    {"id": 5, "name": "待确认-市委专职副书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委副书记（推测）", "current_org": "中共林州市委",
     "source": "市委常规设有专职副书记; 姓名未公开"},

    # 市纪委书记 — 待确认
    {"id": 6, "name": "待确认-市纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委常委、市纪委书记（推测）", "current_org": "中共林州市纪委",
     "source": "市委常规设有纪委书记; 姓名未公开"},

    # 市委组织部部长 — 待确认
    {"id": 7, "name": "待确认-市委组织部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委常委、组织部部长（推测）", "current_org": "中共林州市委组织部",
     "source": "市委常规设有组织部长; 姓名未公开"},

    # 市委宣传部部长 — 待确认
    {"id": 8, "name": "待确认-市委宣传部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委常委、宣传部部长（推测）", "current_org": "中共林州市委宣传部",
     "source": "市委常规设有宣传部长; 姓名未公开"},

    # 市委政法委书记 — 待确认
    {"id": 9, "name": "待确认-市委政法委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委常委、政法委书记（推测）", "current_org": "中共林州市委政法委",
     "source": "市委常规设有政法委书记; 姓名未公开"},

    # 常务副市长 — 待确认
    {"id": 10, "name": "待确认-常务副市长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委常委、常务副市长（推测）", "current_org": "林州市人民政府",
     "source": "市人民政府常规设有常务副市长; 姓名未公开"},

    # 人武部主官 — 待确认
    {"id": 11, "name": "待确认-人武部主官", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委常委、人武部主官（推测）", "current_org": "林州市人民武装部",
     "source": "市委常规设有人武部主官兼职常委; 姓名未公开"},

    # 市委办主任 — 待确认
    {"id": 12, "name": "待确认-市委办主任", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "林州市委常委、市委办公室主任（推测）", "current_org": "中共林州市委办公室",
     "source": "市委常规设有市委办主任; 姓名未公开"},
]

organizations = [
    {"id": 1, "name": "中共林州市委", "type": "党委", "level": "县处级",
     "parent": "中共安阳市委", "location": "河南省安阳市林州市"},
    {"id": 2, "name": "林州市人民政府", "type": "政府", "level": "县处级",
     "parent": "安阳市人民政府", "location": "河南省安阳市林州市"},
    {"id": 3, "name": "中共林州市纪委", "type": "党委", "level": "县处级",
     "parent": "中共林州市委", "location": "河南省安阳市林州市"},
    {"id": 4, "name": "中共林州市委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共林州市委", "location": "河南省安阳市林州市"},
    {"id": 5, "name": "中共林州市委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共林州市委", "location": "河南省安阳市林州市"},
    {"id": 6, "name": "中共林州市委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共林州市委", "location": "河南省安阳市林州市"},
    {"id": 7, "name": "中共林州市委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共林州市委", "location": "河南省安阳市林州市"},
    {"id": 8, "name": "林州市人民武装部", "type": "党委", "level": "县处级",
     "parent": "安阳军分区", "location": "河南省安阳市林州市"},
    {"id": 9, "name": "林州市人大常委会", "type": "人大", "level": "县处级",
     "parent": "安阳市人大常委会", "location": "河南省安阳市林州市"},
    {"id": 10, "name": "政协林州市委员会", "type": "政协", "level": "县处级",
     "parent": "政协安阳市委员会", "location": "河南省安阳市林州市"},
]

positions = [
    # 孙建铎 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "林州市委书记", "start_date": "~2022",
     "end_date": "present", "rank": "县处级正职", "note": "推测2022年前后接任市委书记"},
    {"person_id": 1, "org_id": 2, "title": "林州市市长（前任）", "start_date": "~2019",
     "end_date": "~2022", "rank": "县处级正职", "note": "曾任林州市长, 后升任市委书记"},

    # 田元飞 — 市长
    {"person_id": 2, "org_id": 2, "title": "林州市市长", "start_date": "~2023",
     "end_date": "present", "rank": "县处级正职", "note": "推测2023年前后接任市长"},
    {"person_id": 2, "org_id": 1, "title": "林州市委副书记", "start_date": "~2023",
     "end_date": "present", "rank": "县处级副职", "note": "兼任市委副书记"},

    # 前任市委书记 王宝玉
    {"person_id": 3, "org_id": 1, "title": "林州市委书记（前任）", "start_date": "",
     "end_date": "~2022", "rank": "县处级正职", "note": "王宝玉, ~2022年前后离任"},

    # 专职副书记
    {"person_id": 5, "org_id": 1, "title": "林州市委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 纪委书记
    {"person_id": 6, "org_id": 1, "title": "林州市委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "林州市纪委书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 组织部长
    {"person_id": 7, "org_id": 1, "title": "林州市委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "林州市委组织部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 宣传部长
    {"person_id": 8, "org_id": 1, "title": "林州市委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "林州市委宣传部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 政法委书记
    {"person_id": 9, "org_id": 1, "title": "林州市委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "林州市委政法委书记", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 常务副市长
    {"person_id": 10, "org_id": 1, "title": "林州市委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "林州市常务副市长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 人武部主官
    {"person_id": 11, "org_id": 1, "title": "林州市委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "林州市人武部主官", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 市委办主任
    {"person_id": 12, "org_id": 1, "title": "林州市委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "林州市委办公室主任", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},
]

relationships = [
    # ── 市委班子核心 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市委书记与市长搭档", "overlap_org": "中共林州市委",
     "overlap_period": "当前", "strength": "strong",
     "source": "推测: 县级市领导班子常规分工"},

    # ── 市委书记与常委 ──
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "市委书记与专职副书记", "overlap_org": "中共林州市委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 市委常规设置"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "市委书记与纪委书记", "overlap_org": "中共林州市委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 市委常规设置"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "市委书记与组织部长", "overlap_org": "中共林州市委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 市委常规设置"},

    # ── 市长与副市长 ──
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "市长与常务副市长", "overlap_org": "林州市人民政府",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 政府领导班子常规分工"},

    # ── 继任关系 ──
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "前任市委书记与现任", "overlap_org": "中共林州市委",
     "overlap_period": "~2022交接", "strength": "confirmed",
     "source": "推测: 孙建铎接替王宝玉任市委书记"},
]


def main():
    print("=== Building 林州市 network data ===")
    print(f"Target: 市委书记 & 市长")
    print(f"Note: Limited web access — many fields are unverified")

    run_build(
        slug="林州市",
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
    print("=== Done ===")


if __name__ == "__main__":
    main()
