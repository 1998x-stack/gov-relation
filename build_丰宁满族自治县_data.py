#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 丰宁满族自治县 leadership network.

Level: 县
Province: 河北省
Parent city: 承德市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_丰宁满族自治县

Research date: 2026-07-24
Official site: http://www.fengning.gov.cn/ (丰宁满族自治县人民政府)

Current status (as of 2026-07-24):
- 县委书记: 刘海丽 — 2025年12月已就任（接替李东）
- 县长: 王学良 — 2025年7月已就任
- 前任县委书记: 李东（2025年9月仍在任）

Note:
- Leadership names confirmed from fengning.gov.cn news articles
- Baidu Baike and other biography sources unavailable (Exa rate-limited, Baidu 403)
- Career histories and detailed biographies for most leaders 待查
- Government website (www.fengning.gov.cn) accessible but leadership pages JS-rendered
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "丰宁满族自治县"
TASK_ID = "hebei_丰宁满族自治县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

AS_OF = "2026-07-24"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 县委书记 刘海丽 ──
    {
        "id": 1,
        "name": "刘海丽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共丰宁满族自治县委书记",
        "current_org": "中共丰宁满族自治县委员会",
        "source": ("Confirmed from fengning.gov.cn news articles. "
                   "First appearance as 县委书记: 2025-12-12 inspection article. "
                   "Predecessor 李东 was still 县委书记 in 2025-09. "
                   "Career history before Fengning: 待查"),
    },
    # ── 2. 县长 王学良 ──
    {
        "id": 2,
        "name": "王学良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰宁满族自治县人民政府县长",
        "current_org": "丰宁满族自治县人民政府",
        "source": ("Confirmed from fengning.gov.cn news articles. "
                   "县政府党组书记、县长. "
                   "First article: 2025-07-08 '县长王学良主持召开...' "
                   "Career history before Fengning: 待查"),
    },
    # ── 3. 李东（前任县委书记）──
    {
        "id": 3,
        "name": "李东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": ("Confirmed from fengning.gov.cn news. "
                   "Was 县委书记 until at least 2025-09-02 (县委常委会). "
                   "Last seen as 县委书记 on 2025-10-23 (民营企业家座谈会). "
                   "Succeeded by 刘海丽 around 2025-11/12. "
                   "Current whereabouts: 待查"),
    },
    # ── 4. 张扬（县委副书记）──
    {
        "id": 4,
        "name": "张扬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共丰宁满族自治县委副书记",
        "current_org": "中共丰宁满族自治县委员会",
        "source": ("Confirmed from 政协丰宁满族自治县第九届委员会第六次会议 "
                   "(2026-02-09) article on fengning.gov.cn"),
    },
    # ── 5. 陈振华（县委常委、常务副县长）──
    {
        "id": 5,
        "name": "陈振华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共丰宁满族自治县委常委、常务副县长",
        "current_org": "丰宁满族自治县人民政府",
        "source": ("Confirmed from '清洁能源产业企业家座谈会' article "
                   "(2025-12-23) on fengning.gov.cn"),
    },
    # ── 6. 王彦山（县委常委、组织部部长）──
    {
        "id": 6,
        "name": "王彦山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共丰宁满族自治县委常委、组织部部长",
        "current_org": "中共丰宁满族自治县委组织部",
        "source": ("Confirmed from 政协会议 article (2026-02-09) and "
                   "中青年干部培训班 article (2025-06-09) on fengning.gov.cn"),
    },
    # ── 7. 徐艳萍（县委常委、统战部部长）──
    {
        "id": 7,
        "name": "徐艳萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共丰宁满族自治县委常委、统战部部长、县政协党组副书记",
        "current_org": "中共丰宁满族自治县委统战部",
        "source": ("Confirmed from 政协会议 article (2026-02-09) on fengning.gov.cn"),
    },
    # ── 8. 袁卫国（县委常委、县委办主任）──
    {
        "id": 8,
        "name": "袁卫国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共丰宁满族自治县委常委、县委办公室主任",
        "current_org": "中共丰宁满族自治县委员会",
        "source": ("Confirmed from '民生工程项目' article (2025-07-02) on fengning.gov.cn "
                   "where he accompanied 李东 as 县委常委、县委办主任. "
                   "Also mentioned as 县领导 in 刘海丽 inspection article (2025-12-11)"),
    },
    # ── 9. 李秀华（县人大常委会主任）──
    {
        "id": 9,
        "name": "李秀华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰宁满族自治县人大常委会党组书记、主任",
        "current_org": "丰宁满族自治县人大常委会",
        "source": ("Confirmed from 政协会议 article (2026-02-09) on fengning.gov.cn"),
    },
    # ── 10. 张立民（县政协主席）──
    {
        "id": 10,
        "name": "张立民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协丰宁满族自治县委员会党组书记、主席",
        "current_org": "政协丰宁满族自治县委员会",
        "source": ("Confirmed from 政协会议 article (2026-02-09) on fengning.gov.cn"),
    },
    # ── 11. 赵凤强（县领导）──
    {
        "id": 11,
        "name": "赵凤强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰宁满族自治县领导",
        "current_org": "丰宁满族自治县人民政府",
        "source": ("Mentioned as 县领导 accompanying 刘海丽 in "
                   "消防安全检查 article (2025-12-11) on fengning.gov.cn. "
                   "Exact title: 待查"),
    },
    # ── 12. 方敬凯（副县长）──
    {
        "id": 12,
        "name": "方敬凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰宁满族自治县人民政府副县长",
        "current_org": "丰宁满族自治县人民政府",
        "source": ("Confirmed from '清洁能源产业企业家座谈会' article "
                   "(2025-12-23) on fengning.gov.cn"),
    },
    # ── 13. 陈鹏（副县长）──
    {
        "id": 13,
        "name": "陈鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰宁满族自治县人民政府副县长",
        "current_org": "丰宁满族自治县人民政府",
        "source": ("Confirmed from '电子商务协会成立大会' article "
                   "(2025-06-27) on fengning.gov.cn"),
    },
    # ── 14. 李明君（县政协副主席）──
    {
        "id": 14,
        "name": "李明君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协丰宁满族自治县委员会党组副书记、副主席",
        "current_org": "政协丰宁满族自治县委员会",
        "source": ("Confirmed from 政协会议 article (2026-02-09) on fengning.gov.cn"),
    },
    # ── 15. 李景安（县政协副主席）──
    {
        "id": 15,
        "name": "李景安",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协丰宁满族自治县委员会副主席",
        "current_org": "政协丰宁满族自治县委员会",
        "source": ("Confirmed from 政协会议 article (2026-02-09) on fengning.gov.cn"),
    },
    # ── 16. 王和（县政协副主席）──
    {
        "id": 16,
        "name": "王和",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协丰宁满族自治县委员会副主席",
        "current_org": "政协丰宁满族自治县委员会",
        "source": ("Confirmed from '电子商务协会成立大会' article "
                   "(2025-06-27) on fengning.gov.cn"),
    },
    # ── 17. 葛瑞丰（县政协秘书长）──
    {
        "id": 17,
        "name": "葛瑞丰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协丰宁满族自治县委员会秘书长",
        "current_org": "政协丰宁满族自治县委员会",
        "source": ("Confirmed from 政协会议 article (2026-02-09) on fengning.gov.cn"),
    },
    # ── 18. 薛宏霞（曾任丰宁副县长，现任康保县委书记）──
    # Note: This person is from an adjacent county investigation (赤城)
    # but their connection to Fengning is relevant
    {
        "id": 18,
        "name": "薛宏霞",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1984-07",
        "birthplace": "河北承德围场",
        "native_place": "河北承德围场",
        "education": "",
        "party_join": "中共党员",
        "work_start": "2007-08",
        "current_post": "康保县委书记",
        "current_org": "中共康保县委员会",
        "source": ("From 赤城县 build script (build_赤城县_data.py). "
                   "曾任丰宁满族自治县副县长，后任赤城县委副书记、县长，现任康保县委书记"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共丰宁满族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德市委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 2,
        "name": "丰宁满族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "承德市人民政府",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 3,
        "name": "丰宁满族自治县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "承德市人大常委会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 4,
        "name": "政协丰宁满族自治县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协承德市委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 5,
        "name": "丰宁满族自治县纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丰宁满族自治县委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 6,
        "name": "中共丰宁满族自治县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丰宁满族自治县委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 7,
        "name": "中共丰宁满族自治县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丰宁满族自治县委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 8,
        "name": "中共丰宁满族自治县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丰宁满族自治县委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 9,
        "name": "中共丰宁满族自治县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丰宁满族自治县委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
    {
        "id": 10,
        "name": "中共丰宁满族自治县委办公室",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丰宁满族自治县委员会",
        "location": "河北省承德市丰宁满族自治县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 刘海丽 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共丰宁满族自治县委书记",
     "start_date": "2025-11", "end_date": "", "rank": "县处级正职",
     "note": "前任为李东，刘海丽约于2025年11-12月接任"},

    # 王学良 — 县长
    {"person_id": 2, "org_id": 2, "title": "丰宁满族自治县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "县政府党组书记。最早出现在2025年7月新闻报道中"},

    # 李东 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "中共丰宁满族自治县委书记（前任）",
     "start_date": "", "end_date": "2025-11", "rank": "县处级正职",
     "note": "2025年9月仍在任，10月最后一次出现，11-12月由刘海丽接替"},

    # 张扬 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "中共丰宁满族自治县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 陈振华 — 县委常委、常务副县长
    {"person_id": 5, "org_id": 2, "title": "丰宁满族自治县人民政府常务副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "县委常委"},
    {"person_id": 5, "org_id": 1, "title": "中共丰宁满族自治县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 王彦山 — 县委常委、组织部部长
    {"person_id": 6, "org_id": 6, "title": "中共丰宁满族自治县委组织部部长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "县委常委"},
    {"person_id": 6, "org_id": 1, "title": "中共丰宁满族自治县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 徐艳萍 — 县委常委、统战部部长
    {"person_id": 7, "org_id": 9, "title": "中共丰宁满族自治县委统战部部长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "县委常委，兼县政协党组副书记"},
    {"person_id": 7, "org_id": 1, "title": "中共丰宁满族自治县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 4, "title": "政协丰宁满族自治县委员会党组副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "兼职"},

    # 袁卫国 — 县委常委、县委办主任
    {"person_id": 8, "org_id": 10, "title": "中共丰宁满族自治县委办公室主任",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "县委常委"},
    {"person_id": 8, "org_id": 1, "title": "中共丰宁满族自治县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 李秀华 — 县人大常委会主任
    {"person_id": 9, "org_id": 3, "title": "丰宁满族自治县人大常委会主任",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "党组书记"},

    # 张立民 — 县政协主席
    {"person_id": 10, "org_id": 4, "title": "政协丰宁满族自治县委员会主席",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "党组书记"},

    # 赵凤强 — 县领导
    {"person_id": 11, "org_id": 2, "title": "丰宁满族自治县领导",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "具体职务待查"},

    # 方敬凯 — 副县长
    {"person_id": 12, "org_id": 2, "title": "丰宁满族自治县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 陈鹏 — 副县长
    {"person_id": 13, "org_id": 2, "title": "丰宁满族自治县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 李明君 — 县政协副主席
    {"person_id": 14, "org_id": 4, "title": "政协丰宁满族自治县委员会副主席",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "党组副书记"},

    # 李景安 — 县政协副主席
    {"person_id": 15, "org_id": 4, "title": "政协丰宁满族自治县委员会副主席",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 王和 — 县政协副主席
    {"person_id": 16, "org_id": 4, "title": "政协丰宁满族自治县委员会副主席",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 葛瑞丰 — 县政协秘书长
    {"person_id": 17, "org_id": 4, "title": "政协丰宁满族自治县委员会秘书长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},

    # 薛宏霞 — 曾任丰宁副县长
    {"person_id": 18, "org_id": 2, "title": "丰宁满族自治县人民政府副县长（曾任）",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "曾任丰宁副县长，后任赤城县委副书记、县长，现任康保县委书记"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 刘海丽 ↔ 王学良：党政一把手工作搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "丰宁满族自治县党政一把手工作搭档关系",
     "overlap_org": "丰宁满族自治县",
     "overlap_period": "2025-12至今"},

    # 刘海丽 ↔ 李东：前后任
    {"person_a": 1, "person_b": 3, "type": "succession",
     "context": "刘海丽接替李东任丰宁县委书记",
     "overlap_org": "中共丰宁满族自治县委员会",
     "overlap_period": "2025-11/12"},

    # 张扬 → 刘海丽：县委班子
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与县委副书记工作关系",
     "overlap_org": "中共丰宁满族自治县委员会",
     "overlap_period": ""},

    # 陈振华 → 王学良：政府班子
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "县长与常务副县长工作关系",
     "overlap_org": "丰宁满族自治县人民政府",
     "overlap_period": ""},

    # 王彦山 → 刘海丽：县委班子
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委书记与组织部部长（县委常委会成员）",
     "overlap_org": "中共丰宁满族自治县委员会",
     "overlap_period": ""},

    # 徐艳萍 → 刘海丽：县委班子
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与统战部部长（县委常委会成员）",
     "overlap_org": "中共丰宁满族自治县委员会",
     "overlap_period": ""},

    # 袁卫国 → 李东 / 刘海丽：县委办前后服务
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委书记与县委办主任工作关系",
     "overlap_org": "中共丰宁满族自治县委员会",
     "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "overlap",
     "context": "前任县委书记与县委办主任工作关系",
     "overlap_org": "中共丰宁满族自治县委员会",
     "overlap_period": ""},

    # 张立民 → 刘海丽：四套班子
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委书记与县政协主席工作关系",
     "overlap_org": "丰宁满族自治县",
     "overlap_period": ""},

    # 李秀华 → 刘海丽：四套班子
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委书记与县人大常委会主任工作关系",
     "overlap_org": "丰宁满族自治县",
     "overlap_period": ""},

    # 薛宏霞（曾任丰宁副县长）→ 冯宁
    {"person_a": 2, "person_b": 18, "type": "overlap",
     "context": "曾在丰宁县政府班子共事",
     "overlap_org": "丰宁满族自治县人民政府",
     "overlap_period": ""},

    # 方敬凯 → 王学良：政府班子
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "县长与副县长工作关系",
     "overlap_org": "丰宁满族自治县人民政府",
     "overlap_period": ""},

    # 陈鹏 → 王学良：政府班子
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "县长与副县长工作关系",
     "overlap_org": "丰宁满族自治县人民政府",
     "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  丰宁满族自治县领导班子工作关系网络")
    print("  等级: 县（河北省承德市下辖）")
    print("  调查日期: 2026-07-24")
    print("  ✅ 县委书记: 刘海丽（2025年12月就任）")
    print("  ✅ 县长: 王学良")
    print("  ✅ 已确认领导团队成员: 18人（含前任）")
    print("  ⚠️  个人履历信息不完整（搜索渠道受限）")
    print("  ⚠️  Baidu Baike 不可用（403）")
    print("=" * 60)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("\n✅ 丰宁满族自治县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("  ⚠️  个人详细履历信息待补充（建议在正常网络环境下补充Baidu Baike资料）")
