#!/usr/bin/env python3
"""Build 志丹县 leadership network — SQLite DB + GEXF graph."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Output paths ──────────────────────────────────────────────────────────────
DB_PATH = DATABASE_DIR / "志丹县_network.db"
GEXF_PATH = GRAPH_DIR / "志丹县_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
PERSONS = [
    # ── Top leaders ──
    {
        "id": 1,
        "name": "李永军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共志丹县委员会",
        "source": "https://www.zhidan.gov.cn/ | 县委常委会(扩大)会议报道 (2026-07-11)",
    },
    {
        "id": 2,
        "name": "刘晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "",
        "education": "经济管理学研究生学历、理学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/grjl/1922830736117903361.html",
    },
    # ── County Party Committee Standing Members ──
    {
        "id": 3,
        "name": "叶二凹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/1.html",
    },
    {
        "id": 4,
        "name": "师淑丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共志丹县纪律检查委员会",
        "source": "志丹县第十九届人大第四次会议报道 (2025-05-13)",
    },
    {
        "id": 5,
        "name": "赵伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "志丹县人民政府",
        "source": "志丹县第十九届人大第四次会议报道 (2025-05-13)",
    },
    {
        "id": 6,
        "name": "冯栋平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共志丹县委员会",
        "source": "志丹县第十九届人大第四次会议报道 (2025-05-13)",
    },
    {
        "id": 7,
        "name": "杜彬荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共志丹县委统战部",
        "source": "志丹县经济社会运行通报会报道 (2025-11-19)",
    },
    {
        "id": 8,
        "name": "袁小强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共志丹县委宣传部",
        "source": "志丹县科协第四次代表大会 (2023-07-12)",
    },
    # ── Deputy County Mayors ──
    {
        "id": 9,
        "name": "李梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/1.html",
    },
    {
        "id": 10,
        "name": "杨海东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/1.html",
    },
    {
        "id": 11,
        "name": "梁炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "志丹县公安局",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/1.html | 人武部党委第一书记任职大会 (2025-05-16)",
    },
    {
        "id": 12,
        "name": "谢春荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/1.html | 县人大调研报道 (2026-07-24)",
    },
    {
        "id": 13,
        "name": "刘小勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/1.html",
    },
    {
        "id": 14,
        "name": "郝煜东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/1.html",
    },
    # ── Legislature & Consultative ──
    {
        "id": 15,
        "name": "刘建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "志丹县人大常委会",
        "source": "志丹县第十九届人大第四次会议 (2025-05-13)",
    },
    {
        "id": 16,
        "name": "白保明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协志丹县委员会",
        "source": "志丹县第十九届人大第四次会议 (2025-05-13)",
    },
    {
        "id": 17,
        "name": "尤淑萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "志丹县人大常委会",
        "source": "县人大调研报道 (2026-07-24)",
    },
    {
        "id": 18,
        "name": "王怀安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共志丹县委政法委",
        "source": "志丹县第十九届人大第四次会议报道 (2025-05-13)",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共志丹县委员会", "type": "党委", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 2, "name": "志丹县人民政府", "type": "政府", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 3, "name": "中共志丹县纪律检查委员会", "type": "党委", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 4, "name": "志丹县监察委员会", "type": "党委", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 5, "name": "中共志丹县委统战部", "type": "党委", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 6, "name": "中共志丹县委宣传部", "type": "党委", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 7, "name": "中共志丹县委政法委", "type": "党委", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 8, "name": "中共志丹县委组织部", "type": "党委", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 9, "name": "志丹县公安局", "type": "政府", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 10, "name": "志丹县人大常委会", "type": "人大", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 11, "name": "政协志丹县委员会", "type": "政协", "level": "县级", "location": "陕西省延安市志丹县"},
    {"id": 12, "name": "延安市纪律检查委员会", "type": "党委", "level": "地市级", "location": "陕西省延安市"},
    {"id": 13, "name": "延安市委宣传部", "type": "党委", "level": "地市级", "location": "陕西省延安市"},
    {"id": 14, "name": "延安市委网信办", "type": "党委", "level": "地市级", "location": "陕西省延安市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
POSITIONS = [
    # 李永军
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "current as of 2026-07"},
    # 刘晓军
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2025-05", "end": "present", "rank": "正县级", "note": "elected May 2025 at 县第十九届人大第四次会议"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2025-05", "end": "present", "rank": "副县级", "note": "县委副书记、县长"},
    {"person_id": 2, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "", "note": "prior role per official resume"},
    {"person_id": 2, "org_id": 12, "title": "市纪委办公室主任、秘书长", "start": "", "end": "", "rank": "", "note": "prior role per official resume"},
    {"person_id": 2, "org_id": 13, "title": "市委宣传部副部长", "start": "", "end": "", "rank": "", "note": "prior role per official resume"},
    {"person_id": 2, "org_id": 14, "title": "市委网信办主任", "start": "", "end": "", "rank": "", "note": "prior role per official resume"},
    # 叶二凹
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "current as of 2026"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 师淑丽
    {"person_id": 4, "org_id": 3, "title": "纪委书记", "start": "", "end": "present", "rank": "副县级", "note": "current as of 2025-05"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 赵伟
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 冯栋平
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 杜彬荣
    {"person_id": 7, "org_id": 5, "title": "统战部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 袁小强
    {"person_id": 8, "org_id": 6, "title": "宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "served since at least 2023"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # Deputy Mayors
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "公安局局长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # Legislature & Consultative
    {"person_id": 15, "org_id": 10, "title": "主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 16, "org_id": 11, "title": "主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 17, "org_id": 10, "title": "副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 王怀安
    {"person_id": 18, "org_id": 7, "title": "政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Leadership team overlaps — all serve in the same county leadership
RELATIONSHIPS = [
    # Core top-2
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档", "overlap_org": "中共志丹县委员会/志丹县人民政府", "overlap_period": "2025-05至今"},
    # Party committee standing members — overlapping roles
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—常务副县长", "overlap_org": "中共志丹县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—纪委书记", "overlap_org": "中共志丹县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记—副县长(县委常委)", "overlap_org": "中共志丹县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记—县委常委", "overlap_org": "中共志丹县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记—统战部长", "overlap_org": "中共志丹县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记—宣传部长", "overlap_org": "中共志丹县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "县委书记—政法委书记", "overlap_org": "中共志丹县委员会", "overlap_period": "至今"},
    # Government team — working under the mayor
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—常务副县长", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长—副县长(县委常委)", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长—副县长", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长—副县长", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长—副局长(公安)", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长—副县长", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长—副县长", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长—副县长", "overlap_org": "志丹县人民政府", "overlap_period": "至今"},
    # Discipline inspection — 刘晓军 previously held 师淑丽's current role
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "刘晓军曾任县纪委书记/监委主任, 师淑丽继任", "overlap_org": "中共志丹县纪律检查委员会", "overlap_period": ""},
    # Cross-system leadership team
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记—人大主任", "overlap_org": "志丹县", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委书记—政协主席", "overlap_org": "志丹县", "overlap_period": "至今"},
    {"person_a": 15, "person_b": 17, "type": "overlap", "context": "人大主任—副主任", "overlap_org": "志丹县人大常委会", "overlap_period": "至今"},
]


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    run_build(
        slug="志丹县领导班子关系图",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()
