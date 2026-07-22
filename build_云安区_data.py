#!/usr/bin/env python3
"""Build Yun'an (云安区) leadership network data.

Level: 市辖区
Province: 广东省
Parent city: 云浮市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)

Research date: 2026-07-22
Official source: https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (领导班子页面)

Current status (as of 2026-07-22):
- 区委书记: 梁玉莉（女，1976年3月生，汉族，大学学历）
- 区长: 谢国才（男，1975年5月生，汉族，在职大学学历）

Key deputies:
- 专职副书记: 孙诚博（1987年7月生，全日制研究生，正处职）
- 挂职副书记: 杜绮敏（女，1978年10月生）
- 常务副区长: 陈伟权（1980年6月生，区委常委，在职研究生）
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "云安区"
TASK_ID = "guangdong_云安区"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "梁玉莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委书记，云浮新区（高新区）党工委书记",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/qwsj/content/post_1519542.html (official — 梁玉莉个人简历)",
    },
    {
        "id": 2,
        "name": "谢国才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "在职大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委副书记、区长、区政府党组书记，云浮新区（高新区）党工委副书记、管委会主任",
        "current_org": "云安区人民政府",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qzfld/qz/content/post_1519548.html (official — 谢国才个人简历)",
    },
    {
        "id": 3,
        "name": "孙诚博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年7月",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "全日制研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委副书记（正处职）、统战部部长，兼任云浮新区（高新区）党工委副书记",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/qwfsj/content/post_2010988.html (official — 孙诚博个人简历)",
    },
    {
        "id": 4,
        "name": "杜绮敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "挂任云安区委副书记、区政府党组成员",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/qwfsj/content/post_1947272.html (official — 杜绮敏个人简历)",
    },
    {
        "id": 5,
        "name": "谢敬洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "在职大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委常委、宣传部部长",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/qwcw/content/post_1947279.html (official — 谢敬洪个人简历)",
    },
    {
        "id": 6,
        "name": "陈伟权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "在职研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委常委，区政府党组副书记、副区长",
        "current_org": "云安区人民政府",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qzfld/fqz/content/post_1947491.html (official — 陈伟权个人简历)",
    },
    {
        "id": 7,
        "name": "刘方华",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委常委",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/index.html (official — 区委领导列表)",
    },
    {
        "id": 8,
        "name": "梁金龙",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委常委",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/index.html (official — 区委领导列表)",
    },
    {
        "id": 9,
        "name": "游志锋",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委常委",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/index.html (official — 区委领导列表)",
    },
    {
        "id": 10,
        "name": "张炳文",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区委常委",
        "current_org": "中共云浮市云安区委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qwld/index.html (official — 区委领导列表)",
    },
    # ════════════════════════════════════════
    # 区政府领导（副区长）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "詹学源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "在职研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区政府党组成员、副区长，区红十字会会长",
        "current_org": "云安区人民政府",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qzfld/fqz/content/post_1947292.html (official — 詹学源个人简历)",
    },
    {
        "id": 12,
        "name": "谢华荣",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区副区长",
        "current_org": "云安区人民政府",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qzfld/index.html (official — 区政府领导列表)",
    },
    {
        "id": 13,
        "name": "阎文乾",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区副区长",
        "current_org": "云安区人民政府",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qzfld/index.html (official — 区政府领导列表)",
    },
    {
        "id": 14,
        "name": "朱宇飞",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区副区长",
        "current_org": "云安区人民政府",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/qzfld/index.html (official — 区政府领导列表)",
    },
    # ════════════════════════════════════════
    # 区人大领导
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "刘永星",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区人大常委会主任",
        "current_org": "云安区人民代表大会常务委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区人大领导列表)",
    },
    {
        "id": 16,
        "name": "李桂光",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区人大常委会副主任",
        "current_org": "云安区人民代表大会常务委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区人大领导列表)",
    },
    {
        "id": 17,
        "name": "陈均宜",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区人大常委会副主任",
        "current_org": "云安区人民代表大会常务委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区人大领导列表)",
    },
    {
        "id": 18,
        "name": "温谨圣",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区人大常委会副主任",
        "current_org": "云安区人民代表大会常务委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区人大领导列表)",
    },
    {
        "id": 19,
        "name": "伦佩珍",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区人大常委会副主任",
        "current_org": "云安区人民代表大会常务委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区人大领导列表)",
    },
    {
        "id": 20,
        "name": "张国雄",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区人大常委会副主任",
        "current_org": "云安区人民代表大会常务委员会",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区人大领导列表)",
    },
    # ════════════════════════════════════════
    # 区政协领导
    # ════════════════════════════════════════
    {
        "id": 21,
        "name": "房坚祥",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区政协主席",
        "current_org": "云安区政协",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区政协领导列表)",
    },
    {
        "id": 22,
        "name": "潘捷瑜",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区政协副主席",
        "current_org": "云安区政协",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区政协领导列表)",
    },
    {
        "id": 23,
        "name": "廖伟",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区政协副主席",
        "current_org": "云安区政协",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区政协领导列表)",
    },
    {
        "id": 24,
        "name": "黎学明",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区政协副主席",
        "current_org": "云安区政协",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区政协领导列表)",
    },
    {
        "id": 25,
        "name": "刘爱连",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区政协副主席",
        "current_org": "云安区政协",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区政协领导列表)",
    },
    {
        "id": 26,
        "name": "温振明",
        "gender": "unknown",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云安区政协副主席",
        "current_org": "云安区政协",
        "source": "https://www.yunan.gov.cn/yaqrmzf/ldbz/index.html (official — 区政协领导列表)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共云浮市云安区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共云浮市委员会",
        "location": "广东省云浮市云安区",
    },
    {
        "id": 2,
        "name": "云安区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "云浮市人民政府",
        "location": "广东省云浮市云安区",
    },
    {
        "id": 3,
        "name": "云安区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "云浮市人民代表大会常务委员会",
        "location": "广东省云浮市云安区",
    },
    {
        "id": 4,
        "name": "云安区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "云浮市政协",
        "location": "广东省云浮市云安区",
    },
    {
        "id": 5,
        "name": "云浮新区（高新区）党工委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共云浮市委员会",
        "location": "广东省云浮市云安区",
    },
    {
        "id": 6,
        "name": "云浮新区（高新区）管委会",
        "type": "政府",
        "level": "县处级",
        "parent": "云浮市人民政府",
        "location": "广东省云浮市云安区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 梁玉莉 — 区委书记（兼新区党工委书记）
    {
        "person_id": 1,
        "org_id": 1,
        "title": "区委书记",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed current 区委书记 as of July 2026. Also serves as 云浮新区（高新区）党工委书记.",
    },
    {
        "person_id": 1,
        "org_id": 5,
        "title": "云浮新区（高新区）党工委书记",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Concurrent position noted on official profile.",
    },
    # 谢国才 — 区长（兼新区副书记、管委会主任）
    {
        "person_id": 2,
        "org_id": 2,
        "title": "区长",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed current 区长 as of July 2026. Also serves as 区政府党组书记.",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "区委副书记",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed 区委副书记 on official profile.",
    },
    {
        "person_id": 2,
        "org_id": 6,
        "title": "云浮新区（高新区）管委会主任",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Concurrent position.",
    },
    # 孙诚博 — 专职副书记（正处职）
    {
        "person_id": 3,
        "org_id": 1,
        "title": "区委副书记（正处职）",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed 区委副书记（正处职）, also 统战部部长, 兼云浮新区（高新区）党工委副书记.",
    },
    # 杜绮敏 — 挂职副书记
    {
        "person_id": 4,
        "org_id": 1,
        "title": "挂任区委副书记",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "挂职, also 区政府党组成员.",
    },
    # 谢敬洪 — 宣传部部长
    {
        "person_id": 5,
        "org_id": 1,
        "title": "区委常委、宣传部部长",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Confirmed on official profile.",
    },
    # 陈伟权 — 常务副区长
    {
        "person_id": 6,
        "org_id": 1,
        "title": "区委常委",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Confirmed on official profile.",
    },
    {
        "person_id": 6,
        "org_id": 2,
        "title": "常务副区长、区政府党组副书记",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Confirmed 常务副区长 on official profile.",
    },
    # 刘方华、梁金龙、游志锋、张炳文 — 区委常委
    {
        "person_id": 7,
        "org_id": 1,
        "title": "区委常委",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official 区委领导 page.",
    },
    {
        "person_id": 8,
        "org_id": 1,
        "title": "区委常委",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official 区委领导 page. Confirmed attending inspection with 梁玉莉 on 2026-07-15.",
    },
    {
        "person_id": 9,
        "org_id": 1,
        "title": "区委常委",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official 区委领导 page.",
    },
    {
        "person_id": 10,
        "org_id": 1,
        "title": "区委常委",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official 区委领导 page.",
    },
    # 副区长
    {
        "person_id": 11,
        "org_id": 2,
        "title": "副区长",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Confirmed on official profile.",
    },
    {
        "person_id": 12,
        "org_id": 2,
        "title": "副区长",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official 区政府领导 page.",
    },
    {
        "person_id": 13,
        "org_id": 2,
        "title": "副区长",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official 区政府领导 page.",
    },
    {
        "person_id": 14,
        "org_id": 2,
        "title": "副区长",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official 区政府领导 page.",
    },
    # 区人大
    {
        "person_id": 15,
        "org_id": 3,
        "title": "区人大常委会主任",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 16,
        "org_id": 3,
        "title": "区人大常委会副主任",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 17,
        "org_id": 3,
        "title": "区人大常委会副主任",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 18,
        "org_id": 3,
        "title": "区人大常委会副主任",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 19,
        "org_id": 3,
        "title": "区人大常委会副主任",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 20,
        "org_id": 3,
        "title": "区人大常委会副主任",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    # 区政协
    {
        "person_id": 21,
        "org_id": 4,
        "title": "区政协主席",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 22,
        "org_id": 4,
        "title": "区政协副主席",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 23,
        "org_id": 4,
        "title": "区政协副主席",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 24,
        "org_id": 4,
        "title": "区政协副主席",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 25,
        "org_id": 4,
        "title": "区政协副主席",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
    {
        "person_id": 26,
        "org_id": 4,
        "title": "区政协副主席",
        "start": "unknown",
        "end": "present",
        "rank": "副处级",
        "note": "Listed on official page.",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 梁玉莉 <-> 谢国才: 党政主要领导搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "梁玉莉 is 区委书记 (party secretary) and 谢国才 is 区长 (mayor/区党委副书记) — 云安区党政主要领导搭档. Both hold concurrent posts at 云浮新区（高新区）.",
        "overlap_org": "云安区党政领导班子",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    # 区委书记与副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "孙诚博 serves as 专职副书记 under 区委书记 梁玉莉.",
        "overlap_org": "中共云浮市云安区委员会",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "杜绮敏 serves as 挂职副书记 under 区委书记 梁玉莉.",
        "overlap_org": "中共云浮市云安区委员会",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    # 区长与常务副区长
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "陈伟权 serves as 常务副区长 under 区长 谢国才.",
        "overlap_org": "云安区人民政府",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    # 梁玉莉与梁金龙 — 共同出席活动
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "梁金龙陪同梁玉莉 '四不两直' 督导检查人居环境提升2.0版工作 on 2026-07-15.",
        "overlap_org": "云安区领导班子",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    # 区委常委之间的同僚关系
    {
        "person_a": 5,
        "person_b": 6,
        "type": "overlap",
        "context": "Both serve as 区委常委 in the 云安区委常委会.",
        "overlap_org": "中共云浮市云安区委员会",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    {
        "person_a": 7,
        "person_b": 8,
        "type": "overlap",
        "context": "Both serve as 区委常委 in the 云安区委常委会.",
        "overlap_org": "中共云浮市云安区委员会",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    {
        "person_a": 9,
        "person_b": 10,
        "type": "overlap",
        "context": "Both serve as 区委常委 in the 云安区委常委会.",
        "overlap_org": "中共云浮市云安区委员会",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    # 新区岗位关联: 梁玉莉、谢国才、孙诚博 同时在新区分管
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "Both hold concurrent posts at 云浮新区（高新区）— 梁玉莉 as 党工委书记, 孙诚博 as 党工委副书记.",
        "overlap_org": "云浮新区（高新区）",
        "overlap_period": "confirmed overlap as of July 2026",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "Both hold concurrent posts at 云浮新区（高新区）— 谢国才 as 党工委副书记/管委会主任, 孙诚博 as 党工委副书记.",
        "overlap_org": "云浮新区（高新区）",
        "overlap_period": "confirmed overlap as of July 2026",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")
    print(f"Persons:  {len(persons)}")
    print(f"Orgs:     {len(organizations)}")
    print(f"Positions:{len(positions)}")
    print(f"Relations:{len(relationships)}")
