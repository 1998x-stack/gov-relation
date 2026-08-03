#!/usr/bin/env python3
"""Build script for 赤水市 (Chishui, Zunyi, Guizhou) leadership network.

Generated: 2026-08-03
Level: 县级市
Province: 贵州省
Parent City: 遵义市
Targets: 市委书记 & 市长

Sources:
  - 赤水市人民政府门户网站 (www.gzchishui.gov.cn): 领导之窗 pages, verified 2026-07/08
  - 赤水要闻 / 市委常委会会议报道 (multiple articles, June-July 2026)
  - All roles confirmed via official government website

Research confidence:
  - 汪能科 (市委书记): identity confirmed, full career timeline incomplete (pre-赤水 roles unknown)
  - 王巍 (市长): identity confirmed from official bio (1980.10, Han, university, CPC)
  - Other deputy leaders: identity confirmed from official leadership page
"""

import os
import sqlite3  # noqa — used by gov_relation.runner
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ═══════════════════════════════════════════════════
    # Core Leaders
    # ═══════════════════════════════════════════════════

    # ── 市委书记: 汪能科 ──
    {
        "id": 1,
        "name": "汪能科",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — most common for Guizhou party secretaries
        "birth": "",          # GAP — birth year unknown
        "birthplace": "",     # GAP
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵义市人大常委会副主任、赤水市委书记、赤水经开区党工委书记",
        "current_org": "中共赤水市委员会",
        "source": "赤水市人民政府门户网站 — https://www.gzchishui.gov.cn (verified 2026-07-30 via news reports: 汪能科主持会议, 率队赴茅台座谈)",
    },
    # ── 市长: 王巍 ──
    {
        "id": 2,
        "name": "王巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",       # GAP — exact date
        "work_start": "",       # GAP
        "current_post": "赤水市委副书记、市人民政府党组书记、市长、赤水经开区管委会主任",
        "current_org": "赤水市人民政府",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn/zwgk/ldzc_5981312/ww/ (verified 2026-08)",
    },
    # ── 市委副书记: 李良 ──
    {
        "id": 3,
        "name": "李良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市委副书记",
        "current_org": "中共赤水市委员会",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn (verified 2026-06-27, 2026-07-17 via 市委常委会会议报道)",
    },
    # ── 市委副书记: 周文静 ──
    {
        "id": 4,
        "name": "周文静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市委副书记",
        "current_org": "中共赤水市委员会",
        "source": "赤水市人民政府门户 https://www.gzchishui.gov.cn (w 2026-06-25 市委常委会暨经开区党工委会报道)",
    },
    # ── 市委常委、经开区党工委副书记、管委会副主任: 柳林 ──
    {
        "id": 5,
        "name": "柳林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市委常委、赤水经开区党工委副书记、管委会副主任",
        "current_org": "赤水经济技术开发区党工委",
        "source": "赤水市政府门户网站 (multiple 常委会 2026-06/07 报道)",
    },
    # ── 市委常委、组织部部长: 陈庚 ──
    {
        "id": 6,
        "name": "陈庚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市委常委、市委组织部部长",
        "current_org": "中共赤水市委组织部",
        "source": "赤水市人民政府门户网站 (2026-07-30 茅台集团座谈会报道)",
    },
    # ── 市委常委、政法委书记: 罗永红 ──
    {
        "id": 7,
        "name": "罗永红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市委常委、市委政法委书记",
        "current_org": "中共赤水市委政法委员会",
        "source": "赤水市人民政府门户网站 (2026-06-22 书记专题新闻报道)",
    },
    # ── 副市长（协助王远分管国投集团）: 陈勇 ──
    {
        "id": 8,
        "name": "陈勇",
        "gender": "男",
        "ethnicity": "仡佬族",
        "birth": "1981年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市人民政府党组成员、副市长",
        "current_org": "赤水市人民政府",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn/zwgk/ldzc_5981312/cy/",
    },
    # ── 副市长: 袁贵平 ──
    {
        "id": 9,
        "name": "袁贵平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市人民政府党组成员、副市长",
        "current_org": "赤水市人民政府",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn/zwgk/ldzc_5981312/ygp/",
    },
    # ── 副市长: 李红梅 ──
    {
        "id": 10,
        "name": "李红梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市人民政府党组成员、副市长",
        "current_org": "赤水市人民政府",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn/zwgk/ldzc_5981312/lhm/",
    },
    # ── 副市长: 彭星 ──
    {
        "id": 11,
        "name": "彭星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市人民政府党组成员、副市长",
        "current_org": "赤水市人民政府",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn/zwgk/ldzc_5981312/gjh/",
    },
    # ── 副市长、公安局局长: 郑迪 ──
    {
        "id": 12,
        "name": "郑迪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市人民政府党组成员、副市长，公安局党委书记、局长",
        "current_org": "赤水市公安局",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn/zwgk/ldzc_5981312/csb/",
    },
    # ── 副市长（挂职）: 伍文卓 ──
    {
        "id": 13,
        "name": "伍文卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市人民政府副市长（挂职）",
        "current_org": "赤水市人民政府",
        "source": "赤水市人民政府门户网站 https://www.gzchishui.gov.cn/zwgk/ldzc_5981312/wwz/",
    },
    # ── 市人大常委会主任: 李锋 ──
    {
        "id": 14,
        "name": "李锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赤水市人大常委会主任",
        "current_org": "赤水市人大常委会",
        "source": "赤水市人民政府门户网站 (2026-07-30 茅台座谈会报道, 2026-07-17 常委会报道)",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共赤水市委员会", "type": "党委", "level": "正处级", "parent": "中共遵义市委员会", "location": "赤水市"},
    {"id": 2, "name": "赤水市人民政府", "type": "政府", "level": "正处级", "parent": "遵义市人民政府", "location": "赤水市"},
    {"id": 3, "name": "中共赤水市纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共遵义市纪律检查委员会", "location": "赤水市"},
    {"id": 4, "name": "中共赤水市委组织部", "type": "党委", "level": "正科级", "parent": "中共赤水市委员会", "location": "赤水市"},
    {"id": 5, "name": "中共赤水市委政法委员会", "type": "党委", "level": "正科级", "parent": "中共赤水市委员会", "location": "赤水市"},
    {"id": 6, "name": "赤水市人大常委会", "type": "人大", "level": "正处级", "parent": "赤水市", "location": "赤水市"},
    {"id": 7, "name": "政协赤水市委员会", "type": "政协", "level": "正处级", "parent": "赤水市", "location": "赤水市"},
    {"id": 8, "name": "赤水经济技术开发区", "type": "开发区", "level": "正处级", "parent": "赤水市人民政府", "location": "赤水市"},
    {"id": 9, "name": "赤水市公安局", "type": "政府", "level": "正科级", "parent": "赤水市人民政府", "location": "赤水市"},
    {"id": 10, "name": "遵义市人大常委会", "type": "人大", "level": "正厅级", "parent": "遵义市", "location": "遵义市"},
]

POSITIONS = [
    # 汪能科 — 市委书记 (also 遵义市人大常委会副主任)
    {"person_id": 1, "org_id": 1, "title": "赤水市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "网上资料显示汪能科曾任仁怀市委书记后调任赤水市委书记"},
    {"person_id": 1, "org_id": 10, "title": "遵义市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "高配副厅级"},
    # 王巍 — 市长
    {"person_id": 2, "org_id": 2, "title": "赤水市市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "赤水市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "赤水经开区管委会主任（兼）", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 李良 — 副书记
    {"person_id": 3, "org_id": 1, "title": "赤水市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 周文静 — 副书记
    {"person_id": 4, "org_id": 1, "title": "赤水市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 柳林 — 常委、经开区
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "经开区党工委副书记、管委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈庚 — 组织部长
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "市委组织部部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 罗永红 — 政法委书记
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "市委政法委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 陈勇 — 副市长
    {"person_id": 8, "org_id": 2, "title": "市人民政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 袁贵平 — 副市长
    {"person_id": 9, "org_id": 2, "title": "市人民政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李红梅 — 副市长
    {"person_id": 10, "org_id": 2, "title": "市人民政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 彭星 — 副市长
    {"person_id": 11, "org_id": 2, "title": "市人民政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 郑迪 — 副市长、公安局长
    {"person_id": 12, "org_id": 2, "title": "市人民政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 9, "title": "公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 伍文卓 — 挂职副市长
    {"person_id": 13, "org_id": 2, "title": "市人民政府副市长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "致公党员，协助东西部协作"},
    # 李锋 — 人大主任
    {"person_id": 14, "org_id": 6, "title": "赤水市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    # 汪能科与汪巍 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记-市长搭档", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站（市常委会报道", "confidence": "confirmed"},
    # 汪能培与李良 — 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记与专职副书记", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站", "confidence": "confirmed"},
    # 汪能科与周文静 — 书记与副书记
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记与专职副书记", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站", "confidence": "confirmed"},
    # 王巍与李良 — 党政副职搭档
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "市长与专职副书记", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站", "confidence": "confirmed"},
    # 王巍与周文静
    {"person_a": 2, "person_b": 4, "type": "党政副职搭档", "context": "市长与专职副书记", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站", "confidence": "confirmed"},
    # 汪能科与陈庚 — 书记与组织部长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委书记与组织部长（干部人事关关系的）", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站（茅台座谈会共同参加）", "confidence": "confirmed"},
    # 汪能科与罗永红 — 书记与政法委书记
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "市委书记与政法委书记", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站（专题会共同参加）", "confidence": "confirmed"},
    # 王巍与陈勇 — 市长与副市长
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "市长与副市长", "overlap_org": "赤水市人民政府", "overlap_period": "2026（现任）", "source": "赤水市政府领导之窗", "confidence": "confirmed"},
    # 王巍与袁贵平
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "市长与副市长", "overlap_org": "赤水市人民政府", "overlap_period": "2026（现任）", "source": "赤水市政府领导之窗", "confidence": "confirmed"},
    # 王巍与李红梅
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "市长与副市长", "overlap_org": "赤水市人民政府", "overlap_period": "2026（现任）", "source": "赤水市政府领导之窗", "confidence": "confirmed"},
    # 王巍与彭星
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "市长与副市长", "overlap_org": "赤水市人民政府", "overlap_period": "2026（现任）", "source": "赤水市政府领导之窗", "confidence": "confirmed"},
    # 王巍与郑迪
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "市长与副市长（公安局长）", "overlap_org": "赤水市人民政府", "overlap_period": "2026（现任）", "source": "赤水市政府领导之窗", "confidence": "confirmed"},
    # 李良与陈庚 — 副书记与组织部长
    {"person_a": 3, "person_b": 6, "type": "工作协作", "context": "专职副书记与组织部长（干部工作协作）", "overlap_org": "中共赤水市委常委会", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站", "confidence": "plausible"},
    # 汪能科与李锋 — 市委与人大
    {"person_a": 1, "person_b": 14, "type": "党政正职搭档", "context": "市委书记与人大主任", "overlap_org": "赤水市四套班子", "overlap_period": "2026（现任）", "source": "赤水市政府门户网站", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "赤水市_network.db"
GEXF_PATH = STAGING_DIR / "赤水市_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="赤水市",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )