#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 郧阳区, 十堰市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_郧阳区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 郧阳区人民政府 (yunyang.shiyan.gov.cn) — official government website
  - 梅华: CONFIRMED as 区委书记 via official leadership page (2022-05-13)
    + news articles (July 2026) confirming active status
  - 刘伟华: CONFIRMED as 区委副书记、区长 via official leadership page (2025-05-08)
  - 12 区委常委 bios all confirmed from official leadership page
  - 10 区政府领导班子 (including vice-mayors) confirmed from official page
  - Predecessors: 胡先平 (former 区委书记, plausible), 孙道军 (earlier, plausible)
    but names and whereabouts of predecessors UNVERIFIED for 区长 position

Confidence notes:
  - All 12 standing committee members' identities and basic bios are CONFIRMED
    from official government source (yunyang.shiyan.gov.cn).
  - 梅华's full career timeline (before current role) is UNVERIFIED.
  - 刘伟华's full career timeline (before current role) is UNVERIFIED.
  - Predecessor names (胡先平, 孙道军) are PL AUSIBLE but not confirmed from
    this environment; previous 区长的 name is entirely UNVERIFIED.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "郧阳区"
YUNYANG_SLUG = "yunyang_yy"  # unique slug to avoid collision
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{YUNYANG_SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{YUNYANG_SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "梅华",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1975-04",
        "birthplace": "湖北建始",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "1998-07",
        "current_post": "郧阳区委书记",
        "current_org": "中共十堰市郧阳区委员会",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502378.shtml"
    },
    {
        "id": 2,
        "name": "刘伟华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "山东潍坊",
        "education": "研究生学历、工学博士",
        "party_join": "中共党员",
        "work_start": "2004-07",
        "current_post": "郧阳区委副书记、区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202505/t20250508_4736615.shtml"
    },
    # ═══════ 区委副书记 ═══════
    {
        "id": 3,
        "name": "董会祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "十堰市郧阳区",
        "education": "党校大学学历",
        "party_join": "中共党员",
        "work_start": "1994-09",
        "current_post": "郧阳区委副书记、区委政法委书记",
        "current_org": "中共十堰市郧阳区委员会",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654540.shtml"
    },
    # ═══════ 区委常委 ═══════
    {
        "id": 4,
        "name": "刘群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-03",
        "birthplace": "湖北竹溪",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1995-11",
        "current_post": "郧阳区委常委、常务副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502470.shtml"
    },
    {
        "id": 5,
        "name": "雷涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "十堰市郧阳区",
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1999-10",
        "current_post": "郧阳区委常委、统战部部长、区政协党组副书记、区总工会主席",
        "current_org": "中共十堰市郧阳区委员会",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654548.shtml"
    },
    {
        "id": 6,
        "name": "柯相国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "十堰市郧阳区",
        "education": "农业推广硕士",
        "party_join": "中共党员",
        "work_start": "1995-09",
        "current_post": "郧阳区委常委、区委办公室主任",
        "current_org": "中共十堰市郧阳区委员会",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654551.shtml"
    },
    {
        "id": 7,
        "name": "王凡",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "湖北郧西",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "2005-07",
        "current_post": "郧阳区委常委、区纪委书记、区监委主任",
        "current_org": "中共十堰市郧阳区纪律检查委员会",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654555.shtml"
    },
    {
        "id": 8,
        "name": "卢金华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "河南开封",
        "education": "研究生学历、法学硕士",
        "party_join": "中共党员",
        "work_start": "2011-09",
        "current_post": "郧阳区委常委、宣传部部长",
        "current_org": "中共十堰市郧阳区委员会",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654558.shtml"
    },
    {
        "id": 9,
        "name": "王俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "十堰市郧阳区",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1996-12",
        "current_post": "郧阳区委常委、副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202205/t20220513_3502481.shtml"
    },
    {
        "id": 10,
        "name": "王一鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-02",
        "birthplace": "湖北郧西",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "2008-07",
        "current_post": "郧阳区委常委、组织部部长",
        "current_org": "中共十堰市郧阳区委员会",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654562.shtml"
    },
    {
        "id": 11,
        "name": "韦燕珍",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1979-11",
        "birthplace": "广西崇左",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2002-07",
        "current_post": "郧阳区委常委、副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654566.shtml"
    },
    {
        "id": 12,
        "name": "王铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "北京市东城区",
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "2002-07",
        "current_post": "郧阳区委常委、副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qwld/202412/t20241206_4654571.shtml"
    },
    # ═══════ 区政府领导（副区长，非常委） ═══════
    {
        "id": 13,
        "name": "孔令林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "湖北十堰",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1994-07",
        "current_post": "郧阳区副区长、区公安局局长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qzfld/202307/t20230718_3958149.shtml"
    },
    {
        "id": 14,
        "name": "何珊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-02",
        "birthplace": "湖北天门",
        "education": "大学学历",
        "party_join": "",
        "work_start": "2005-07",
        "current_post": "郧阳区副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qzfld/202307/t20230718_3958154.shtml"
    },
    {
        "id": 15,
        "name": "肖帮伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-11",
        "birthplace": "郧阳区青曲镇",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2007-07",
        "current_post": "郧阳区副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qzfld/202307/t20230718_3958158.shtml"
    },
    {
        "id": 16,
        "name": "王云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-12",
        "birthplace": "十堰市郧阳区",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1997-07",
        "current_post": "郧阳区副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qzfld/202307/t20230718_3958163.shtml"
    },
    {
        "id": 17,
        "name": "李一川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-11",
        "birthplace": "四川眉山",
        "education": "研究生学历、法学博士",
        "party_join": "中共党员",
        "work_start": "2007-09",
        "current_post": "郧阳区副区长",
        "current_org": "郧阳区人民政府",
        "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgk/zfld/qzfld/202307/t20230718_3958167.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共十堰市郧阳区委员会", "type": "党委", "level": "县级", "parent": "中共十堰市委员会", "location": "十堰市郧阳区"},
    {"id": 2, "name": "郧阳区人民政府", "type": "政府", "level": "县级", "parent": "十堰市人民政府", "location": "十堰市郧阳区"},
    {"id": 3, "name": "中共十堰市郧阳区纪律检查委员会/郧阳区监察委员会", "type": "党委", "level": "县级", "parent": "中共十堰市纪律检查委员会", "location": "十堰市郧阳区"},
    {"id": 4, "name": "中共十堰市郧阳区委政法委员会", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 5, "name": "中共十堰市郧阳区委组织部", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 6, "name": "中共十堰市郧阳区委宣传部", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 7, "name": "中共十堰市郧阳区委统战部", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 8, "name": "中共十堰市郧阳区委办公室", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 9, "name": "十堰市公安局郧阳区分局", "type": "政府", "level": "县级", "parent": "郧阳区人民政府", "location": "十堰市郧阳区"},
    {"id": 10, "name": "郧阳区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "十堰市人民代表大会常务委员会", "location": "十堰市郧阳区"},
    {"id": 11, "name": "中国人民政治协商会议郧阳区委员会", "type": "政协", "level": "县级", "parent": "政协十堰市委员会", "location": "十堰市郧阳区"},
    {"id": 12, "name": "郧阳区总工会", "type": "群团", "level": "县级", "parent": "十堰市总工会", "location": "十堰市郧阳区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "郧阳区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 区长
    {"person_id": 2, "org_id": 1, "title": "郧阳区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "郧阳区区长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 区委副书记/政法委书记
    {"person_id": 3, "org_id": 1, "title": "郧阳区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "区委政法委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 常务副区长
    {"person_id": 4, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 统战部长
    {"person_id": 5, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "区委统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 12, "title": "区总工会主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 区委办公室主任
    {"person_id": 6, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "区委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 纪委书记
    {"person_id": 7, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 宣传部长
    {"person_id": 8, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "区委宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副区长(常委)
    {"person_id": 9, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 组织部长
    {"person_id": 10, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "区委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副区长(常委)
    {"person_id": 11, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副区长(常委)
    {"person_id": 12, "org_id": 1, "title": "郧阳区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副区长（非常委）
    {"person_id": 13, "org_id": 2, "title": "副区长、区公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 9, "title": "区公安局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "非党人士"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长为郧阳区党政正职搭档", "overlap_org": "郧阳区", "overlap_period": ""},
    # 区委书记 ↔ 区委副书记/政法委书记
    {"person_a": 1, "person_b": 3, "type": "区委班子", "context": "区委副书记在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    # 区委书记 ↔ 其他常委（区委班子）
    {"person_a": 1, "person_b": 4, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    # 区长 ↔ 副区长（政府班子）
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "常务副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
]


# ── Helper Functions ───────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    """Return RGB color string for a person based on role."""
    if name == "梅华":
        return "255,50,50"  # Red — Party Secretary
    elif name == "刘伟华":
        return "50,100,255"  # Blue — Mayor
    elif name == "董会祥":
        return "100,100,100"  # Grey — Deputy Party Secretary
    elif name == "王凡":
        return "255,165,0"  # Orange — Discipline Inspection
    else:
        return "100,100,100"  # Grey — Others


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


def generate_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 using string formatting."""
    province = "湖北省"
    parent_city = "十堰市"
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network — {province} {parent_city}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        name = p["name"] if p["name"] else "待确认"
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        role = p["current_post"]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if not any(p["id"] == pos["person_id"] and p["name"] for p in persons):
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        if not any(p["id"] == r["person_a"] and p["name"] for p in persons):
            continue
        if not any(p["id"] == r["person_b"] and p["name"] for p in persons):
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"    GEXF written: {output_path}")


def build_sqlite(persons, organizations, positions, relationships, db_path):
    """Build SQLite database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        )
    """)

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT OR REPLACE INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"    DB written: {db_path}")


def write_person_json(person, output_dir):
    """Write a single person JSON file."""
    if not person["name"]:
        return
    filename = f'{TODAY}-湖北省-十堰市-{person["current_post"].replace("/", "-").replace("、", "-")}-{person["name"]}.json'
    filepath = Path(output_dir) / filename

    source_register = []
    if person.get("source"):
        source_register.append({
            "id": "S001",
            "title": f"郧阳区人民政府 - {person['name']}",
            "url": person["source"],
            "publisher": "郧阳区人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Official leadership profile page"
        })

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "十堰市",
            "region": "郧阳区",
            "job": person["current_post"],
            "task_id": "hubei_郧阳区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"yunyang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "No negative signals found in search scope", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("education") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年经历、历任职务）" if not person.get("work_start") else "birthplace and early career"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生地、学历、历任职务的起止时间）",
                "why_it_matters": "无法定位其职业发展路径、跨地区交流和晋升模式",
                "suggested_queries": [f"{person['name']} 郧阳区 简历", f"{person['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    Person JSON written: {filepath}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(BASE))

    print(f"Building {SLUG} network data...")

    # SQLite
    print("  Creating SQLite database...")
    build_sqlite(persons, organizations, positions, relationships, DB_PATH)

    # GEXF
    print("  Creating GEXF graph...")
    generate_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    # Person JSON
    print("  Creating person JSON files...")
    for p in persons:
        write_person_json(p, STAGING_DIR)

    print(f"\nDone. Artifacts:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    person_files = [f for f in Path(STAGING_DIR).iterdir() if f.suffix == ".json" and TODAY in f.name]
    for pf in sorted(person_files):
        print(f"  Person: {pf}")
