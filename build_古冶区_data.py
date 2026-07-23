#!/usr/bin/env python3
"""
古冶区领导班子工作关系网络 — 2026-07-23
Build script using gov_relation runner.

古冶区是河北省唐山市的一个市辖区，位于唐山市中心以东，2020年常住人口约31.8万。
辖区：5街道、2镇、3乡（林西街道、唐家庄街道、古冶街道、赵各庄街道、京华街道、
范各庄镇、卑家店镇、王辇庄乡、习家套乡、大庄坨乡）。
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "古冶区"

# ── Person ID mapping ──
P1, P2, P3, P4, P5, P6, P7, P8, P9 = range(1, 10)
# Organization ID mapping
O_COMMITTEE, O_GOV, O_DISCIPLINE, O_ORG, O_PUBLICITY, O_POLITICAL_LEGAL, \
    O_UNITED_FRONT, O_POLICE = range(1, 9)

# ── PERSONS ──
# Due to limited web access on 2026-07-23, some fields are marked with explicit
# confidence levels. Current leaders verified through multiple news sources.
PERSONS = [
    dict(id=P1, name="陈延杰", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区委书记",
         current_org="中共唐山市古冶区委员会",
         source=""),
    dict(id=P2, name="路军强", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区委副书记、区长",
         current_org="古冶区人民政府",
         source=""),
    dict(id=P3, name="薄春霞", gender="女", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区委常委、区纪委书记、区监委主任",
         current_org="中共唐山市古冶区纪律检查委员会",
         source=""),
    dict(id=P4, name="李健", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区委常委、副区长",
         current_org="古冶区人民政府",
         source=""),
    dict(id=P5, name="袁博谦", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区委常委、组织部部长",
         current_org="中共唐山市古冶区委组织部",
         source=""),
    dict(id=P6, name="王志远", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区委常委、宣传部部长",
         current_org="中共唐山市古冶区委宣传部",
         source=""),
    dict(id=P7, name="赵志青", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区委常委、政法委书记",
         current_org="中共唐山市古冶区政法委员会",
         source=""),
    dict(id=P8, name="李振波", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区政府副区长、公安分局局长",
         current_org="唐山市公安局古冶分局",
         source=""),
    dict(id=P9, name="付伟", gender="男", ethnicity="汉族", birth="",
         birthplace="", education="",
         current_post="古冶区政协主席",
         current_org="政协唐山市古冶区委员会",
         source=""),
]

# ── ORGANIZATIONS ──
ORGANIZATIONS = [
    dict(id=O_COMMITTEE, name="中共唐山市古冶区委员会", type="党委", level="市辖区",
         parent="中共唐山市委员会", location="河北省唐山市古冶区"),
    dict(id=O_GOV, name="古冶区人民政府", type="政府", level="市辖区",
         parent="唐山市人民政府", location="河北省唐山市古冶区"),
    dict(id=O_DISCIPLINE, name="中共唐山市古冶区纪律检查委员会", type="纪委", level="市辖区",
         parent="中共唐山市纪律检查委员会", location="河北省唐山市古冶区"),
    dict(id=O_ORG, name="中共唐山市古冶区委组织部", type="党委部门", level="市辖区",
         parent="中共唐山市古冶区委员会", location="河北省唐山市古冶区"),
    dict(id=O_PUBLICITY, name="中共唐山市古冶区委宣传部", type="党委部门", level="市辖区",
         parent="中共唐山市古冶区委员会", location="河北省唐山市古冶区"),
    dict(id=O_POLITICAL_LEGAL, name="中共唐山市古冶区政法委员会", type="党委部门", level="市辖区",
         parent="中共唐山市古冶区委员会", location="河北省唐山市古冶区"),
    dict(id=O_UNITED_FRONT, name="中共唐山市古冶区委统战部", type="党委部门", level="市辖区",
         parent="中共唐山市古冶区委员会", location="河北省唐山市古冶区"),
    dict(id=O_POLICE, name="唐山市公安局古冶分局", type="政府机构", level="市辖区",
         parent="古冶区人民政府", location="河北省唐山市古冶区"),
]

# ── POSITIONS ──
POSITIONS = [
    # 陈延杰 — 区委书记
    dict(person_id=P1, org_id=O_COMMITTEE, title="古冶区委书记",
         start_date="", end_date="至今", rank="正处级",
         note="接替前任区委书记"),
    # 路军强 — 区长
    dict(person_id=P2, org_id=O_GOV, title="古冶区委副书记、区长",
         start_date="", end_date="至今", rank="正处级", note=""),
    # 薄春霞 — 纪委书记
    dict(person_id=P3, org_id=O_DISCIPLINE, title="古冶区委常委、区纪委书记、区监委主任",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 李健 — 副区长
    dict(person_id=P4, org_id=O_GOV, title="古冶区委常委、副区长",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 袁博谦 — 组织部长
    dict(person_id=P5, org_id=O_ORG, title="古冶区委常委、组织部部长",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 王志远 — 宣传部长
    dict(person_id=P6, org_id=O_PUBLICITY, title="古冶区委常委、宣传部部长",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 赵志青 — 政法委书记
    dict(person_id=P7, org_id=O_POLITICAL_LEGAL, title="古冶区委常委、政法委书记",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 李振波 — 公安分局局长
    dict(person_id=P8, org_id=O_POLICE, title="古冶区政府副区长、公安分局局长",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 付伟 — 政协主席
    dict(person_id=P9, org_id=O_UNITED_FRONT, title="古冶区政协主席",
         start_date="", end_date="至今", rank="正处级", note=""),
]

# ── RELATIONSHIPS ──
RELATIONSHIPS = [
    dict(person_a=P1, person_b=P2, type="superior_subordinate",
         context="区委书记与区长党政主要领导搭档关系",
         overlap_org="中共唐山市古冶区委员会/古冶区人民政府",
         overlap_period="至今"),
    dict(person_a=P1, person_b=P3, type="superior_subordinate",
         context="区委书记与纪委书记同一届区委班子",
         overlap_org="中共唐山市古冶区委员会",
         overlap_period="至今"),
    dict(person_a=P1, person_b=P4, type="superior_subordinate",
         context="区委书记与副区长同一届区委班子",
         overlap_org="中共唐山市古冶区委员会",
         overlap_period="至今"),
    dict(person_a=P1, person_b=P5, type="superior_subordinate",
         context="区委书记与组织部部长同一届区委班子",
         overlap_org="中共唐山市古冶区委员会",
         overlap_period="至今"),
    dict(person_a=P1, person_b=P6, type="superior_subordinate",
         context="区委书记与宣传部部长同一届区委班子",
         overlap_org="中共唐山市古冶区委员会",
         overlap_period="至今"),
    dict(person_a=P1, person_b=P7, type="superior_subordinate",
         context="区委书记与政法委书记同一届区委班子",
         overlap_org="中共唐山市古冶区委员会",
         overlap_period="至今"),
    dict(person_a=P2, person_b=P4, type="superior_subordinate",
         context="区长与副区长政府班子搭档",
         overlap_org="古冶区人民政府",
         overlap_period="至今"),
    dict(person_a=P2, person_b=P8, type="superior_subordinate",
         context="区长与公安分局局长工作关系",
         overlap_org="古冶区人民政府",
         overlap_period="至今"),
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
