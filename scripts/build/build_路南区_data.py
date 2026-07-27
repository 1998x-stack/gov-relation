#!/usr/bin/env python3
"""
唐山市路南区领导班子工作关系网络 — 2026-07-23
Build script using gov_relation runner.
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "路南区"

# ── Person ID mapping ──
# Integer IDs as required by the schema
P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12 = range(1, 13)
# Organization ID mapping (offset by 100000 per runner convention)
O_PARTY, O_GOV, O_CJ, O_ZZB, O_TYZ, O_GAJ = range(1, 7)

# ── PERSONS ──
PERSONS = [
    dict(id=P1, name="张静", gender="女", ethnicity="汉族", birth="1982-03",
         birthplace="", education="", current_post="路南区委书记",
         current_org="中共唐山市路南区委员会",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20210811/1220612.html"),
    dict(id=P2, name="孟祥中", gender="男", ethnicity="汉族", birth="1973-07",
         birthplace="", education="省委党校大学", current_post="路南区委常委、常务副区长",
         current_org="路南区人民政府",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20220909/1460260.html"),
    dict(id=P3, name="赵颖", gender="", ethnicity="", birth="",
         birthplace="", education="", current_post="路南区委常委、区纪委书记、区监委主任",
         current_org="中共唐山市路南区纪律检查委员会",
         source="http://www.lunan.gov.cn/lunanqu/jinrilunan/20260213/1211620462.html"),
    dict(id=P4, name="付征", gender="", ethnicity="", birth="",
         birthplace="", education="", current_post="路南区委常委、组织部部长、统战部部长",
         current_org="中共唐山市路南区委组织部",
         source="http://www.lunan.gov.cn/lunanqu/jinrilunan/20260408/1211624548.html"),
    dict(id=P5, name="李俊朝", gender="男", ethnicity="", birth="",
         birthplace="", education="", current_post="路南区委原书记（已离任）",
         current_org="中共唐山市路南区委员会",
         source="http://www.lunan.gov.cn/lunanqu/jinrilunan/20260213/1211620462.html"),
    dict(id=P6, name="刘红梅", gender="女", ethnicity="汉族", birth="1977-08",
         birthplace="", education="省委党校研究生", current_post="路南区政府副区长",
         current_org="路南区人民政府",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20210802/873976.html"),
    dict(id=P7, name="叶术山", gender="男", ethnicity="汉族", birth="1970-09",
         birthplace="", education="大学，农学学士", current_post="路南区政府副区长、三级调研员",
         current_org="路南区人民政府",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20210802/1135963.html"),
    dict(id=P8, name="孙鑫", gender="男", ethnicity="汉族", birth="1986-06",
         birthplace="", education="研究生，法学硕士", current_post="路南区政府副区长",
         current_org="路南区人民政府",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20240105/1141584017.html"),
    dict(id=P9, name="余礼请", gender="男", ethnicity="汉族", birth="1990-05",
         birthplace="", education="研究生，法律硕士", current_post="路南区政府副区长",
         current_org="路南区人民政府",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20250415/1211591296.html"),
    dict(id=P10, name="王清华", gender="男", ethnicity="汉族", birth="1979-08",
         birthplace="", education="省委党校研究生", current_post="路南区政府副区长、公安分局局长",
         current_org="唐山市公安局路南分局",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20250415/1211591298.html"),
    dict(id=P11, name="吕斌", gender="男", ethnicity="汉族", birth="1981-05",
         birthplace="", education="研究生，经济学硕士", current_post="路南区政府副区长（挂职）",
         current_org="路南区人民政府",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20251230/1211616250.html"),
    dict(id=P12, name="张国伟", gender="", ethnicity="", birth="",
         birthplace="", education="", current_post="路南区政府党组成员、城南经济开发区管委会",
         current_org="路南区政府",
         source="http://www.lunan.gov.cn/lunanqu/tslunanquzhengfulingdao/20250415/1211591300.html"),
]

# ── ORGANIZATIONS ──
ORGANIZATIONS = [
    dict(id=O_PARTY, name="中共唐山市路南区委员会", type="党委", level="市辖区",
         parent="中共唐山市委员会", location="河北省唐山市路南区"),
    dict(id=O_GOV, name="路南区人民政府", type="政府", level="市辖区",
         parent="唐山市人民政府", location="河北省唐山市路南区"),
    dict(id=O_CJ, name="中共唐山市路南区纪律检查委员会", type="纪委", level="市辖区",
         parent="中共唐山市纪律检查委员会", location="河北省唐山市路南区"),
    dict(id=O_ZZB, name="中共唐山市路南区委组织部", type="党委部门", level="市辖区",
         parent="中共唐山市路南区委员会", location="河北省唐山市路南区"),
    dict(id=O_TYZ, name="中共唐山市路南区委统战部", type="党委部门", level="市辖区",
         parent="中共唐山市路南区委员会", location="河北省唐山市路南区"),
    dict(id=O_GAJ, name="唐山市公安局路南分局", type="政府机构", level="市辖区",
         parent="路南区人民政府", location="河北省唐山市路南区"),
]

# ── POSITIONS ──
POSITIONS = [
    # 张静
    dict(person_id=P1, org_id=O_PARTY, title="路南区委书记",
         start_date="2026-07", end_date="至今", rank="正处级",
         note="2026年7月由区长升任区委书记"),
    dict(person_id=P1, org_id=O_GOV, title="路南区委副书记、区长",
         start_date="2021-08", end_date="2026-07", rank="正处级",
         note="原任区长，后升书记"),
    # 孟祥中
    dict(person_id=P2, org_id=O_GOV, title="路南区委常委、常务副区长",
         start_date="2022-09", end_date="至今", rank="副处级",
         note="区政府党组副书记、三级调研员"),
    dict(person_id=P2, org_id=O_PARTY, title="路南区委常委",
         start_date="2022-09", end_date="至今", rank="副处级", note=""),
    # 赵颖
    dict(person_id=P3, org_id=O_CJ, title="路南区委常委、区纪委书记、区监委主任",
         start_date="", end_date="至今", rank="副处级", note=""),
    dict(person_id=P3, org_id=O_PARTY, title="路南区委常委",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 付征
    dict(person_id=P4, org_id=O_ZZB, title="路南区委常委、组织部部长",
         start_date="", end_date="至今", rank="副处级", note=""),
    dict(person_id=P4, org_id=O_TYZ, title="路南区委统战部部长",
         start_date="", end_date="至今", rank="", note="兼任"),
    dict(person_id=P4, org_id=O_PARTY, title="路南区委常委",
         start_date="", end_date="至今", rank="副处级", note=""),
    # 李俊朝
    dict(person_id=P5, org_id=O_PARTY, title="路南区委书记",
         start_date="", end_date="2026-06", rank="正处级",
         note="前任区委书记，2026年7月前已离任"),
    # 刘红梅
    dict(person_id=P6, org_id=O_GOV, title="路南区政府副区长",
         start_date="2021-08", end_date="至今", rank="副处级", note=""),
    # 叶术山
    dict(person_id=P7, org_id=O_GOV, title="路南区政府副区长",
         start_date="2021-08", end_date="至今", rank="副处级", note="三级调研员"),
    # 孙鑫
    dict(person_id=P8, org_id=O_GOV, title="路南区政府副区长",
         start_date="2024-01", end_date="至今", rank="副处级", note=""),
    # 余礼请
    dict(person_id=P9, org_id=O_GOV, title="路南区政府副区长",
         start_date="2025-04", end_date="至今", rank="副处级", note=""),
    # 王清华
    dict(person_id=P10, org_id=O_GAJ, title="路南区政府副区长、公安分局局长",
         start_date="2025-04", end_date="至今", rank="副处级", note=""),
    dict(person_id=P10, org_id=O_GOV, title="路南区政府副区长",
         start_date="2025-04", end_date="至今", rank="副处级", note=""),
    # 吕斌
    dict(person_id=P11, org_id=O_GOV, title="路南区政府副区长（挂职）",
         start_date="2025-12", end_date="至今", rank="副处级", note="挂职"),
    # 张国伟
    dict(person_id=P12, org_id=O_GOV, title="路南区政府党组成员",
         start_date="", end_date="至今", rank="", note="协助区长负责开发区日常工作"),
]

# ── RELATIONSHIPS ──
RELATIONSHIPS = [
    # 前后任书记
    dict(person_a=P5, person_b=P1, type="前后任",
         context="李俊朝为前任区委书记，张静接任",
         overlap_org="中共唐山市路南区委员会",
         overlap_period="2026年交接"),
    # 张静与孟祥中（区长-常务副区长搭档）
    dict(person_a=P1, person_b=P2, type="上下级",
         context="张静任区长时孟祥中为常务副区长",
         overlap_org="路南区人民政府",
         overlap_period="2022-2026"),
    # 张静与赵颖（常委会同僚）
    dict(person_a=P1, person_b=P3, type="同僚",
         context="区委常委会共事",
         overlap_org="中共唐山市路南区委员会",
         overlap_period=""),
    # 张静与付征（上下级）
    dict(person_a=P1, person_b=P4, type="上下级",
         context="区委书记与组织部长",
         overlap_org="中共唐山市路南区委员会",
         overlap_period=""),
    # 李俊朝与赵颖（区委书记-纪委书记搭档）
    dict(person_a=P5, person_b=P3, type="上下级",
         context="李俊朝任区委书记时赵颖为纪委书记",
         overlap_org="中共唐山市路南区委员会",
         overlap_period=""),
    # 孟祥中与各位副区长（政府班子）
    dict(person_a=P2, person_b=P6, type="同僚",
         context="区政府领导班子", overlap_org="路南区人民政府", overlap_period=""),
    dict(person_a=P2, person_b=P7, type="同僚",
         context="区政府领导班子", overlap_org="路南区人民政府", overlap_period=""),
    dict(person_a=P2, person_b=P8, type="同僚",
         context="区政府领导班子", overlap_org="路南区人民政府", overlap_period=""),
    dict(person_a=P2, person_b=P9, type="同僚",
         context="区政府领导班子", overlap_org="路南区人民政府", overlap_period=""),
    dict(person_a=P2, person_b=P10, type="同僚",
         context="区政府领导班子", overlap_org="路南区人民政府", overlap_period=""),
    dict(person_a=P2, person_b=P11, type="同僚",
         context="区政府领导班子", overlap_org="路南区人民政府", overlap_period=""),
    # 张静与各副区长
    dict(person_a=P1, person_b=P6, type="上下级",
         context="区长-副区长", overlap_org="路南区人民政府", overlap_period="2021-2026"),
    dict(person_a=P1, person_b=P7, type="上下级",
         context="区长-副区长", overlap_org="路南区人民政府", overlap_period="2021-2026"),
    dict(person_a=P1, person_b=P8, type="上下级",
         context="区长-副区长", overlap_org="路南区人民政府", overlap_period="2024-2026"),
    dict(person_a=P1, person_b=P9, type="上下级",
         context="区长-副区长", overlap_org="路南区人民政府", overlap_period="2025-2026"),
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
        overwrite=True,
    )
