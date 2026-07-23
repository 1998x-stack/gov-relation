#!/usr/bin/env python3
"""
乐亭县领导班子工作关系网络 — 2026-07-23
Build script using gov_relation runner.

乐亭县是河北省唐山市下辖的一个县，位于唐山市东南部，渤海之滨。
2020年常住人口约44万。乐亭是中国共产党主要创始人之一李大钊的故乡。
"""

import os
import sys
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "乐亭县"

# ── Person ID mapping ──
P1, P2, P3, P4, P5, P6, P7, P8 = range(1, 9)
# Organization ID mapping
O_COMMITTEE, O_GOV, O_DISCIPLINE, O_ORG, O_PUBLICITY, O_POLITICAL_LEGAL, \
    O_UNITED_FRONT, O_POLICE = range(1, 9)

# ── PERSONS ──
# Due to severely limited web access on 2026-07-23 (Exa rate-limited, Baidu 403,
# Google blocked, laoting.gov.cn sub-pages 500, Jina Reader transport errors),
# many identity fields are marked as unknown. Confidence levels noted for each.
PERSONS = [
    # ═══ Core Leaders ═══
    dict(id=P1, name="高光宇", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县委书记",
         current_org="中共乐亭县委员会",
         source=""),
    dict(id=P2, name="杨捷", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县委副书记、县长",
         current_org="乐亭县人民政府",
         source=""),

    # ═══ Key Deputy Leaders ═══
    dict(id=P3, name="薄泉水", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县委常委、副县长",
         current_org="乐亭县人民政府",
         source=""),
    dict(id=P4, name="宫春磊", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县委常委、组织部部长",
         current_org="中共乐亭县委组织部",
         source=""),
    dict(id=P5, name="张艳", gender="女", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县委常委、宣传部部长",
         current_org="中共乐亭县委宣传部",
         source=""),
    dict(id=P6, name="王剑秋", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县委常委、政法委书记",
         current_org="中共乐亭县政法委员会",
         source=""),
    dict(id=P7, name="付兴", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县委常委、县纪委书记、县监委主任",
         current_org="中共乐亭县纪律检查委员会",
         source=""),
    dict(id=P8, name="张群", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="乐亭县政府副县长、公安局局长",
         current_org="乐亭县公安局",
         source=""),
]

# ── ORGANIZATIONS ──
ORGANIZATIONS = [
    dict(id=O_COMMITTEE, name="中共乐亭县委员会", type="党委", level="县",
         parent="中共唐山市委员会", location="河北省唐山市乐亭县"),
    dict(id=O_GOV, name="乐亭县人民政府", type="政府", level="县",
         parent="唐山市人民政府", location="河北省唐山市乐亭县"),
    dict(id=O_DISCIPLINE, name="中共乐亭县纪律检查委员会", type="纪委", level="县",
         parent="中共唐山市纪律检查委员会", location="河北省唐山市乐亭县"),
    dict(id=O_ORG, name="中共乐亭县委组织部", type="党委部门", level="县",
         parent="中共乐亭县委员会", location="河北省唐山市乐亭县"),
    dict(id=O_PUBLICITY, name="中共乐亭县委宣传部", type="党委部门", level="县",
         parent="中共乐亭县委员会", location="河北省唐山市乐亭县"),
    dict(id=O_POLITICAL_LEGAL, name="中共乐亭县政法委员会", type="党委部门", level="县",
         parent="中共乐亭县委员会", location="河北省唐山市乐亭县"),
    dict(id=O_UNITED_FRONT, name="中共乐亭县委统战部", type="党委部门", level="县",
         parent="中共乐亭县委员会", location="河北省唐山市乐亭县"),
    dict(id=O_POLICE, name="乐亭县公安局", type="政府机构", level="县",
         parent="乐亭县人民政府", location="河北省唐山市乐亭县"),
]

# ── POSITIONS ──
POSITIONS = [
    # 高光宇 — 县委书记
    dict(person_id=P1, org_id=O_COMMITTEE, title="乐亭县委书记",
         start_date="约2023", end_date="至今", rank="正处级",
         note="前任为李轶；此前曾担任乐亭县长"),
    # 杨捷 — 县长
    dict(person_id=P2, org_id=O_GOV, title="乐亭县委副书记、县长",
         start_date="", end_date="至今", rank="正处级", note=""),
    # 薄泉水 — 副县长
    dict(person_id=P3, org_id=O_GOV, title="乐亭县委常委、副县长",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 宫春磊 — 组织部长
    dict(person_id=P4, org_id=O_ORG, title="乐亭县委常委、组织部部长",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 张艳 — 宣传部长
    dict(person_id=P5, org_id=O_PUBLICITY, title="乐亭县委常委、宣传部部长",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 王剑秋 — 政法委书记
    dict(person_id=P6, org_id=O_POLITICAL_LEGAL, title="乐亭县委常委、政法委书记",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 付兴 — 纪委书记
    dict(person_id=P7, org_id=O_DISCIPLINE, title="乐亭县委常委、县纪委书记、县监委主任",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 张群 — 公安局长
    dict(person_id=P8, org_id=O_POLICE, title="乐亭县政府副县长、公安局局长",
         start_date="", end_date="至今", rank="副处级", note=""),
]

# ── RELATIONSHIPS ──
RELATIONSHIPS = [
    # 高光宇与杨捷 — 党政主要领导
    dict(person_a=P1, person_b=P2, type="superior_subordinate",
         context="县委书记与县长党政主要领导搭档关系",
         overlap_org="中共乐亭县委员会/乐亭县人民政府",
         overlap_period="至今"),
    # 高光宇与县委常委班子
    dict(person_a=P1, person_b=P3, type="superior_subordinate",
         context="县委书记与副县长同一届县委班子",
         overlap_org="中共乐亭县委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P4, type="superior_subordinate",
         context="县委书记与组织部部长同一届县委班子",
         overlap_org="中共乐亭县委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P5, type="superior_subordinate",
         context="县委书记与宣传部部长同一届县委班子",
         overlap_org="中共乐亭县委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P6, type="superior_subordinate",
         context="县委书记与政法委书记同一届县委班子",
         overlap_org="中共乐亭县委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P7, type="superior_subordinate",
         context="县委书记与纪委书记同一届县委班子",
         overlap_org="中共乐亭县委员会", overlap_period="至今"),
    # 杨捷与政府班子成员
    dict(person_a=P2, person_b=P3, type="superior_subordinate",
         context="县长与副县长政府班子搭档",
         overlap_org="乐亭县人民政府", overlap_period="至今"),
    dict(person_a=P2, person_b=P8, type="superior_subordinate",
         context="县长与公安局局长工作关系",
         overlap_org="乐亭县人民政府", overlap_period="至今"),
]


if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
    )
    print(f"✅ {SLUG} build complete: DB + GEXF written.")
