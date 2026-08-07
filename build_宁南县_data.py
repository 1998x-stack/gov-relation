#!/usr/bin/env python3
"""Build script for 宁南县 (凉山彝族自治州·四川省) government personnel network data.

Generated: 2026-07-28
Sources:
  - ningnan.gov.cn 政府领导页面 (http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/)
  - ningnan.gov.cn 宁南要闻 - 常委会报道 (confirms 周肯 as 县委书记, 曾兆菊 as 县长)
  - ningnan.gov.cn 宁南要闻 - 表扬大会报道 (confirms 邰康宁 as 政协主席)
  - ningnan.gov.cn 宁南要闻 - 巡察反馈会 (confirms 王伟 as 组织部部长)
  - ningnan.gov.cn 宁南要闻 - 政协常委会 (confirms 张波 as 县委副书记)
  - ningnan.gov.cn 宁南要闻 - 自然资源调研报道 (confirms 周肯 as 县委书记)
"""

import os, sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "宁南县"
TODAY = "2026-07-28"

# ── Persons ──
# Source: ningnan.gov.cn government leadership page + news articles (confirmed current as of 2026-07-28)

persons = [
    # ═══════════════════════════════════════════════
    # Core leaders
    # ═══════════════════════════════════════════════
    {"id": 1, "name": "周肯", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县委书记",
     "current_org": "中共宁南县委员会",
     "source": "http://www.ningnan.gov.cn/sy/ttxw/202607/t20260721_3003276.html"},

    {"id": 2, "name": "曾兆菊", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县委副书记、县人民政府党组书记、县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    # ═══════════════════════════════════════════════
    # County Party Leadership (县委领导)
    # ═══════════════════════════════════════════════
    {"id": 3, "name": "张波", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县委副书记",
     "current_org": "中共宁南县委员会",
     "source": "http://www.ningnan.gov.cn/nnyw/nnyw_1103/202606/t20260623_2994501.html"},

    {"id": 4, "name": "罗雷", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县委常委、县人民政府常务副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    {"id": 5, "name": "王伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县委常委、组织部部长",
     "current_org": "中共宁南县委组织部",
     "source": "http://www.ningnan.gov.cn/nnyw/nnyw_1103/202606/t20260618_2994007.html"},

    # ═══════════════════════════════════════════════
    # Government Leadership (县政府)
    # ═══════════════════════════════════════════════
    {"id": 6, "name": "赵作黑", "gender": "男", "ethnicity": "彝族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县人民政府副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    {"id": 7, "name": "卢仕文", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县人民政府副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    {"id": 8, "name": "胡麟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县人民政府副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    {"id": 9, "name": "马海燕", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县人民政府副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    {"id": 10, "name": "姚宁", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县人民政府副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    {"id": 11, "name": "曾华", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县人民政府副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},  # also confirmed in 巡察反馈会

    {"id": 12, "name": "覃发超", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县人民政府挂职副县长",
     "current_org": "宁南县人民政府",
     "source": "http://www.ningnan.gov.cn/zfxxgk_31568/zfxxgknr/zfld/"},

    # ═══════════════════════════════════════════════
    # People's Congress & CPPCC (人大、政协)
    # ═══════════════════════════════════════════════
    {"id": 13, "name": "邰康宁", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县政协党组书记、主席",
     "current_org": "政协宁南县委员会",
     "source": "http://www.ningnan.gov.cn/nnyw/nnyw_1103/202606/t20260623_2994501.html"},

    {"id": 14, "name": "勒古子发", "gender": "男", "ethnicity": "彝族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县政协副主席",
     "current_org": "政协宁南县委员会",
     "source": "http://www.ningnan.gov.cn/nnyw/nnyw_1103/202606/t20260623_2994501.html"},

    {"id": 15, "name": "苏鹏先", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县政协副主席",
     "current_org": "政协宁南县委员会",
     "source": "http://www.ningnan.gov.cn/nnyw/nnyw_1103/202606/t20260623_2994501.html"},

    {"id": 16, "name": "范洪", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县政协副主席",
     "current_org": "政协宁南县委员会",
     "source": "http://www.ningnan.gov.cn/nnyw/nnyw_1103/202606/t20260623_2994501.html"},

    {"id": 17, "name": "周正艳", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁南县政协副主席",
     "current_org": "政协宁南县委员会",
     "source": "http://www.ningnan.gov.cn/nnyw/nnyw_1103/202606/t20260623_2994501.html"},
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共宁南县委员会", "type": "党委", "level": "县", "parent": "中共凉山州委", "location": "四川省凉山彝族自治州宁南县"},
    {"id": 2, "name": "宁南县人民政府", "type": "政府", "level": "县", "parent": "凉山州人民政府", "location": "四川省凉山彝族自治州宁南县"},
    {"id": 3, "name": "中共宁南县委组织部", "type": "党委", "level": "县", "parent": "中共宁南县委员会", "location": "四川省凉山彝族自治州宁南县"},
    {"id": 4, "name": "政协宁南县委员会", "type": "政协", "level": "县", "parent": "政协凉山州委员会", "location": "四川省凉山彝族自治州宁南县"},
    {"id": 5, "name": "中共凉山州委", "type": "党委", "level": "地市", "parent": "中共四川省委", "location": "四川省凉山彝族自治州西昌市"},
    {"id": 6, "name": "凉山州人民政府", "type": "政府", "level": "地市", "parent": "四川省人民政府", "location": "四川省凉山彝族自治州西昌市"},
    {"id": 7, "name": "政协凉山州委员会", "type": "政协", "level": "地市", "parent": "四川省政协", "location": "四川省凉山彝族自治州西昌市"},
    {"id": 8, "name": "中共凉山州委组织部", "type": "党委", "level": "地市", "parent": "中共凉山州委", "location": "四川省凉山彝族自治州西昌市"},
]

# ── Positions ──

positions = [
    # 周肯 - party secretary
    {"person_id": 1, "org_id": 1, "title": "宁南县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed active as of 2026-07-20 (chaired县委常委会)"},
    # 曾兆菊 - county magistrate
    {"person_id": 2, "org_id": 2, "title": "宁南县人民政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed active as of 2026-07"},
    {"person_id": 2, "org_id": 1, "title": "宁南县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Concurrent party role"},
    # 张波 - deputy party secretary
    {"person_id": 3, "org_id": 1, "title": "宁南县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 罗雷 - executive deputy magistrate + standing committee
    {"person_id": 4, "org_id": 1, "title": "宁南县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "宁南县人民政府常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王伟 - organization department + standing committee
    {"person_id": 5, "org_id": 1, "title": "宁南县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "宁南县委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # Government deputies
    {"person_id": 6, "org_id": 2, "title": "宁南县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "宁南县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "宁南县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "宁南县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "宁南县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "宁南县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "宁南县人民政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # CPPCC
    {"person_id": 13, "org_id": 4, "title": "县政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──
# Based on documented same-organization and same-period overlaps
# Confirmed from official government leadership page and news reports

relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共宁南县委/宁南县人民政府", "overlap_period": ""},
    # Party committee standing members
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共宁南县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "中共宁南县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与组织部长", "overlap_org": "中共宁南县委", "overlap_period": ""},
    # County magistrate with deputies
    {"person_a": 2, "person_b": 4, "type": "teamwork", "context": "县长与常务副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "teamwork", "context": "县长与县委副书记", "overlap_org": "中共宁南县委", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长赵作黑", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长卢仕文", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长胡麟", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长马海燕", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长姚宁", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长曾华", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与挂职副县长覃发超", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    # Standing committee lateral
    {"person_a": 4, "person_b": 5, "type": "teamwork", "context": "常务副县长与组织部长（同为县委常委）", "overlap_org": "中共宁南县委", "overlap_period": ""},
    # Government team lateral
    {"person_a": 4, "person_b": 6, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 10, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 11, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 12, "type": "teamwork", "context": "常务副县长与挂职副县长", "overlap_org": "宁南县人民政府", "overlap_period": ""},
    # CPPCC relationships
    {"person_a": 1, "person_b": 13, "type": "teamwork", "context": "县委书记与政协主席", "overlap_org": "宁南县四套班子", "overlap_period": ""},
]

# ── Run Build ──

if __name__ == "__main__":
    STAGING_DIR = Path(__file__).parent

    db_path = STAGING_DIR / f"{SLUG}_network.db"
    gexf_path = STAGING_DIR / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"   数据库: {db_path}")
    print(f"   GEXF图: {gexf_path}")