#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build script for 合山市 (Heshan City, Laibin, Guangxi) leadership network.

Generated: 2026-07-23
Level: 县级市
Province: 广西壮族自治区
Parent City: 来宾市
Targets: 市委书记 & 市长

Research Notes:
  Current Party Secretary: 徐钊 (confirmed as of Jul 2026, party secretary)
  Current Mayor: 陈波 (listed on government leadership page)
  Previous Mayor: 谭小春 (mentioned in Apr 2026 news article)
  People's Congress Chair: 覃武仕 (confirmed Jul 2026)
  CPPCC Chair: 韦干稳 (confirmed Jun-Jul 2026)

  Confirmed facts:
  - 徐钊: 合山市委书记，2026年7月讲授专题党课
  - 陈波: 合山市市长 (listed on official leadership page)
  - 覃武仕: 市人大常委会主任
  - 韦干稳: 市政协主席
  - 李树宇: 市委常委、统战部部长、市政协党组副书记
  - 蒙洁: 副市长
  - 韦龙云: 副市长
  - 李琼莹: 副市长
  - 兰秀鸾: 副市长
  - 谭小春: 原市长 (2026年4月以市长身份出席活动)
  - 区丽群: 市政协副主席
  - 蓝天华: 市政协副主席

  GAPS:
  - 徐钊来合山前的完整履历未知 (曾任职务、出生年月等)
  - 陈波的完整履历未知 (出生年月、籍贯、教育背景等)
  - 谭小春的去向未知
  - 各副市长的具体分工和分管领域
  - 市委班子其他成员 (副书记、纪委书记、组织部长等)
  - 各领导的具体出生年月、籍贯、学历等个人信息

  Sources:
  - http://www.heshanshi.gov.cn/xxgk/fdzhdgknr/szfld/ (政府领导页面)
  - http://www.heshanshi.gov.cn/zwdt/hsxw/t27901535.shtml (徐钊讲授专题党课 2026-07-15)
  - http://www.heshanshi.gov.cn/zwdt/hsxw/t27852360.shtml (七一走访慰问 2026-07-01)
  - http://www.heshanshi.gov.cn/zwdt/hsxw/t27826164.shtml (政协调研 2026-06-25)
"""

import os
import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, DATA_DIR
from gov_relation.runner import run_build

# ── 暂存路径 ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "合山市"

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "徐钊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "合山市委",
        "source": "http://www.heshanshi.gov.cn/zwdt/hsxw/t27901535.shtml; http://www.heshanshi.gov.cn/zwdt/hsxw/t27852360.shtml",
    },
    {
        "id": 2,
        "name": "陈波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "合山市政府",
        "source": "http://www.heshanshi.gov.cn/xxgk/fdzhdgknr/szfld/",
    },
    {
        "id": 3,
        "name": "覃武仕",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "合山市人大常委会",
        "source": "http://www.heshanshi.gov.cn/zwdt/hsxw/t27852360.shtml",
    },
    {
        "id": 4,
        "name": "韦干稳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "合山市政协",
        "source": "http://www.heshanshi.gov.cn/zwdt/hsxw/t27826164.shtml",
    },
    {
        "id": 5,
        "name": "李树宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长、市政协党组副书记",
        "current_org": "合山市委",
        "source": "http://www.heshanshi.gov.cn/zwdt/hsxw/t27826164.shtml",
    },
    {
        "id": 6,
        "name": "蒙洁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "合山市政府",
        "source": "http://www.heshanshi.gov.cn/xxgk/fdzhdgknr/szfld/",
    },
    {
        "id": 7,
        "name": "韦龙云",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "合山市政府",
        "source": "http://www.heshanshi.gov.cn/xxgk/fdzhdgknr/szfld/",
    },
    {
        "id": 8,
        "name": "李琼莹",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "合山市政府",
        "source": "http://www.heshanshi.gov.cn/xxgk/fdzhdgknr/szfld/",
    },
    {
        "id": 9,
        "name": "兰秀鸾",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "合山市政府",
        "source": "http://www.heshanshi.gov.cn/xxgk/fdzhdgknr/szfld/",
    },
    {
        "id": 10,
        "name": "谭小春",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市长（已离任）",
        "current_org": "合山市政府",
        "source": "http://www.heshanshi.gov.cn/xxgk/fdzhdgknr/szfld/sz/ (市长活动日历显示谭小春曾为市长)",
    },
    {
        "id": 11,
        "name": "区丽群",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "合山市政协",
        "source": "http://www.heshanshi.gov.cn/zwdt/hsxw/t27826164.shtml",
    },
    {
        "id": 12,
        "name": "蓝天华",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "合山市政协",
        "source": "http://www.heshanshi.gov.cn/zwdt/hsxw/t27826164.shtml",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共合山市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共来宾市委员会",
        "location": "合山市",
    },
    {
        "id": 2,
        "name": "合山市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "来宾市人民政府",
        "location": "合山市",
    },
    {
        "id": 3,
        "name": "合山市人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "来宾市人大常委会",
        "location": "合山市",
    },
    {
        "id": 4,
        "name": "合山市政协",
        "type": "政协",
        "level": "县级",
        "parent": "来宾市政协",
        "location": "合山市",
    },
    {
        "id": 5,
        "name": "中共来宾市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "来宾市",
    },
    {
        "id": 6,
        "name": "来宾市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "广西壮族自治区人民政府",
        "location": "来宾市",
    },
]

POSITIONS = [
    # 徐钊
    {"person_id": 1, "org_id": 1, "title": "合山市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年7月已就任市委书记；来合山前履历待查"},

    # 陈波
    {"person_id": 2, "org_id": 2, "title": "合山市市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "在官方领导页面列为市长；履历待查"},

    # 覃武仕
    {"person_id": 3, "org_id": 3, "title": "合山市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年7月参加七一慰问活动"},

    # 韦干稳
    {"person_id": 4, "org_id": 4, "title": "合山市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年6月率队调研研学游"},

    # 李树宇
    {"person_id": 5, "org_id": 1, "title": "市委常委、统战部部长、市政协党组副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年6月参加政协调研"},

    # 蒙洁
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方领导页面列出"},

    # 韦龙云
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方领导页面列出"},

    # 李琼莹
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方领导页面列出"},

    # 兰秀鸾
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方领导页面列出"},

    # 谭小春（原市长）
    {"person_id": 10, "org_id": 2, "title": "合山市市长（原）", "start_date": "", "end_date": "2026", "rank": "正处级", "note": "2026年4月仍以市长身份出席活动 (谭小春率队开展清明节前安全检查)；后由陈波接任"},

    # 区丽群
    {"person_id": 11, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 蓝天华
    {"person_id": 12, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

RELATIONSHIPS = [
    # 徐钊—陈波：书记-市长搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长党政一把手搭档", "overlap_org": "合山市四家班子", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 徐钊—覃武仕：书记-人大主任
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记与市人大常委会主任共事", "overlap_org": "合山市四家班子", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 徐钊—韦干稳：书记-政协主席
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记与市政协主席共事", "overlap_org": "合山市四家班子", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 陈波—蒙洁：市长-副市长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "合山市政府", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 陈波—韦龙云：市长-副市长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "合山市政府", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 陈波—李琼莹：市长-副市长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "合山市政府", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 陈波—兰秀鸾：市长-副市长
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "合山市政府", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 谭小春—陈波：前后任市长
    {"person_a": 10, "person_b": 2, "type": "predecessor_successor", "context": "谭小春卸任后陈波接任合山市市长", "overlap_org": "合山市政府", "overlap_period": "2026", "confidence": "confirmed"},

    # 韦干稳—区丽群：政协主席-副主席
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "政协主席与副主席共事", "overlap_org": "合山市政协", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 韦干稳—蓝天华：政协主席-副主席
    {"person_a": 4, "person_b": 12, "type": "overlap", "context": "政协主席与副主席共事", "overlap_org": "合山市政协", "overlap_period": "2026至今", "confidence": "confirmed"},

    # 李树宇—韦干稳：统战部长与政协主席工作关联
    {"person_a": 5, "person_b": 4, "type": "overlap", "context": "李树宇任统战部长、政协党组副书记，与政协主席韦干稳密切协作", "overlap_org": "合山市政协/市委", "overlap_period": "2026至今", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

# ═══════════════════════════════════════════════════
# 暂存路径（staging → promoted by process_tmp.py）
# ═══════════════════════════════════════════════════

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# 推广后的目标路径（用于验证参考）
CANONICAL_DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"


def main() -> None:
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
    print(f"\nStaged DB:   {DB_PATH}")
    print(f"Staged GEXF: {GEXF_PATH}")
    print(f"\nCanonical paths after promotion:")
    print(f"  DB:   {CANONICAL_DB_PATH}")
    print(f"  GEXF: {CANONICAL_GEXF_PATH}")


if __name__ == "__main__":
    main()
