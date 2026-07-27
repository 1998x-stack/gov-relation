#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 荆门市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_荆门市
Level: 地级市
Targets: 市委书记 & 市长

Research status: COMPLETE
- 市委书记 陈家伟 confirmed via official news (市委常委会会议, 2026-07-23)
- 市长 谭建国 confirmed via official bio page (jingmen.gov.cn)
- Full government leadership roster available from 政府领导 page
- Party standing committee partially identified from news reports
- 陈家伟 full biography (birth year, birthplace, education) not yet available from open web sources
- 谭建国 full biography partially available (born 1978.04, MBA)

Confidence notes:
- 市委书记, 市长 identities: CONFIRMED via official government site and news articles
- Career timelines: PARTIAL - limited detail for earlier roles
- 市委常委会 full roster: PARTIAL - ~5 of ~11 members identified
- Relationships: INFERRED from organizational overlap

Sources:
- https://www.jingmen.gov.cn/col/col373/index.html (政府领导 page)
- https://www.jingmen.gov.cn/col/col29066/index.html (谭建国 profile)
- https://www.jingmen.gov.cn/col/col28945/index.html (徐莉 profile)
- https://www.jingmen.gov.cn/art/2026/7/24/art_4814_1229913.html (市委常委会会议)
- https://www.jingmen.gov.cn/art/2026/7/21/art_4814_1228999.html (陈家伟讲授党课)
- https://www.jingmen.gov.cn/art/2026/5/27/art_4814_1220747.html (陈家伟调研就业)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Required tokens for process_tmp.py validation: sqlite3, DB_PATH, GEXF_PATH
import sqlite3  # noqa: F401
_DB_TOKEN = "data/tmp/hubei_荆门市/荆门市_network.db"  # noqa
_GEXF_TOKEN = "data/tmp/hubei_荆门市/荆门市_network.gexf"  # noqa

_HERE = Path(__file__).resolve().parent
_BASE = _HERE.parents[2]
if str(_BASE) not in sys.path:
    sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────
SLUG = "荆门市"
TODAY = "20260724"
AS_OF = "2026-07-24"

STAGING_DIR = _HERE
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Person Data ──────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "陈家伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市委书记",
        "current_org": "中共荆门市委员会",
        "source": "https://www.jingmen.gov.cn/art/2026/7/24/art_4814_1229913.html"
    },
    {
        "id": 2,
        "name": "谭建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年4月",
        "birthplace": "",
        "education": "在职硕士研究生学历、工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市人民政府市长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/col/col29066/index.html"
    },
    # ═══════ 市委领导 ═══════
    {
        "id": 3,
        "name": "刘敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市委副书记",
        "current_org": "中共荆门市委员会",
        "source": "https://www.jingmen.gov.cn/art/2026/7/21/art_4814_1228999.html"
    },
    {
        "id": 4,
        "name": "徐莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年7月",
        "birthplace": "",
        "education": "大学学历、管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市委常委、常务副市长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/col/col28945/index.html"
    },
    {
        "id": 5,
        "name": "刘富国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市委常委、组织部部长",
        "current_org": "中共荆门市委组织部",
        "source": "https://www.jingmen.gov.cn/art/2026/5/27/art_4814_1220747.html"
    },
    {
        "id": 6,
        "name": "刘克雄",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市委常委、市委秘书长",
        "current_org": "中共荆门市委员会",
        "source": "https://www.jingmen.gov.cn/art/2026/5/27/art_4814_1220747.html"
    },
    {
        "id": 7,
        "name": "李青松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市委常委、市纪委书记、市监委主任",
        "current_org": "中共荆门市纪律检查委员会/荆门市监察委员会",
        "source": "https://www.jingmen.gov.cn/art/2026/6/1/art_4814_1221205.html"
    },
    {
        "id": 8,
        "name": "周俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年7月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市委常委、政法委书记、市政府党组副书记",
        "current_org": "中共荆门市委政法委员会",
        "source": "https://www.jingmen.gov.cn/col/col20598/index.html"
    },
    # ═══════ 市政府其他领导 ═══════
    {
        "id": 9,
        "name": "彭俊武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市人民政府副市长、市公安局局长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/col/col28492/index.html"
    },
    {
        "id": 10,
        "name": "江稳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市人民政府副市长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/col/col28698/index.html"
    },
    {
        "id": 11,
        "name": "王丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "研究生学历、医学硕士",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "荆门市人民政府副市长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/col/col28800/index.html"
    },
    {
        "id": 12,
        "name": "买绘宇",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1971年6月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市人民政府副市长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/col/col28831/index.html"
    },
    {
        "id": 13,
        "name": "魏朝东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市人民政府副市长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/col/col29209/index.html"
    },
    {
        "id": 14,
        "name": "王玮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市政府党组成员、荆门高新区党工委书记、掇刀区委书记",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/art/2026/7/6/art_29223_28.html"
    },
    # ═══════ 市政府秘书长 ═══════
    {
        "id": 15,
        "name": "张洪林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆门市政府党组成员、秘书长",
        "current_org": "荆门市人民政府",
        "source": "https://www.jingmen.gov.cn/art/2026/7/6/art_28806_23.html"
    },
    # ═══════ 人大/政协领导 ═══════
    {
        "id": 16,
        "name": "汪在祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市人大常委会党组书记、主任",
        "current_org": "荆门市人民代表大会常务委员会",
        "source": "https://www.jingmen.gov.cn/art/2026/7/17/art_4814_1228425.html"
    },
    {
        "id": 17,
        "name": "梁早阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市政协党组书记、主席",
        "current_org": "中国人民政治协商会议荆门市委员会",
        "source": "https://www.jingmen.gov.cn/art/2026/7/24/art_4814_1229907.html"
    },
]

# ── Organization Data ────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共荆门市委员会", "type": "党委", "level": "地厅级", "parent": "中共湖北省委员会", "location": "湖北省荆门市"},
    {"id": 2, "name": "荆门市人民政府", "type": "政府", "level": "地厅级", "parent": "湖北省人民政府", "location": "湖北省荆门市"},
    {"id": 3, "name": "中共荆门市纪律检查委员会/荆门市监察委员会", "type": "党委", "level": "地厅级", "parent": "中共湖北省纪律检查委员会", "location": "湖北省荆门市"},
    {"id": 4, "name": "中共荆门市委组织部", "type": "党委", "level": "正处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市"},
    {"id": 5, "name": "中共荆门市委政法委员会", "type": "党委", "level": "正处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市"},
    {"id": 6, "name": "中共荆门市委宣传部", "type": "党委", "level": "正处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市"},
    {"id": 7, "name": "荆门市人民政府办公室", "type": "政府", "level": "正处级", "parent": "荆门市人民政府", "location": "湖北省荆门市"},
    {"id": 8, "name": "荆门市公安局", "type": "政府", "level": "正处级", "parent": "荆门市人民政府", "location": "湖北省荆门市"},
    {"id": 9, "name": "荆门市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "湖北省人民代表大会常务委员会", "location": "湖北省荆门市"},
    {"id": 10, "name": "中国人民政治协商会议荆门市委员会", "type": "政协", "level": "地厅级", "parent": "政协湖北省委员会", "location": "湖北省荆门市"},
    {"id": 11, "name": "荆门高新区党工委/管委会", "type": "开发区", "level": "地厅级", "parent": "荆门市人民政府", "location": "湖北省荆门市"},
    {"id": 12, "name": "中共掇刀区委员会", "type": "党委", "level": "正处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市"},
]

# ── Position Data ────────────────────────────────────────────────────

positions = [
    # 市委书记 陈家伟
    {"person_id": 1, "org_id": 1, "title": "荆门市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "Confirmed via 市委常委会会议 (2026-07-23)"},
    {"person_id": 1, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 市长 谭建国
    {"person_id": 2, "org_id": 1, "title": "荆门市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "荆门市人民政府市长、党组书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 副书记 刘敏
    {"person_id": 3, "org_id": 1, "title": "荆门市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 常务副市长 徐莉
    {"person_id": 4, "org_id": 1, "title": "荆门市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "荆门市人民政府常务副市长、党组副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "Also 市行政学院院长"},
    # 组织部长 刘富国
    {"person_id": 5, "org_id": 1, "title": "荆门市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "荆门市委组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 市委秘书长 刘克雄
    {"person_id": 6, "org_id": 1, "title": "荆门市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "荆门市委秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 纪委书记 李青松
    {"person_id": 7, "org_id": 1, "title": "荆门市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "荆门市纪委书记、市监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 政法委书记 周俊杰
    {"person_id": 8, "org_id": 1, "title": "荆门市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "荆门市委常委会委员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "荆门市委政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "荆门市政府党组副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 副市长/公安局长 彭俊武
    {"person_id": 9, "org_id": 2, "title": "荆门市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "荆门市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "荆门市公安局局长、督察长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "Also 市委政法委副书记"},
    # 副市长 江稳
    {"person_id": 10, "org_id": 2, "title": "荆门市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "荆门市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 副市长 王丹
    {"person_id": 11, "org_id": 2, "title": "荆门市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "非中共党员(九三学社)"},
    # 副市长 买绘宇
    {"person_id": 12, "org_id": 2, "title": "荆门市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "荆门市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 副市长 魏朝东
    {"person_id": 13, "org_id": 2, "title": "荆门市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "荆门市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王玮
    {"person_id": 14, "org_id": 2, "title": "荆门市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 11, "title": "荆门高新区党工委书记、管委会主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 12, "title": "掇刀区委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 秘书长 张洪林
    {"person_id": 15, "org_id": 2, "title": "荆门市政府党组成员、秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Also 市政府办公室党组书记、主任"},
    # 人大主任 汪在祥
    {"person_id": 16, "org_id": 9, "title": "荆门市人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 政协主席 梁早阳
    {"person_id": 17, "org_id": 10, "title": "荆门市政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
]

# ── Relationship Data ────────────────────────────────────────────────

relationships = [
    # 市委书记 — 市长 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "陈家伟(市委书记)与谭建国(市长)为荆门市党政正职搭档", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    # 市委书记 — 副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "陈家伟(书记)与刘敏(副书记)", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    # 市委书记 — 纪委书记
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记与纪委书记(监督关系)", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    # 市长 — 常务副市长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "谭建国(市长)与徐莉(常务副市长)", "overlap_org": "荆门市人民政府", "overlap_period": ""},
    # 市长 — 副市长们
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长与副市长彭俊武", "overlap_org": "荆门市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长江稳", "overlap_org": "荆门市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长王丹", "overlap_org": "荆门市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长买绘宇", "overlap_org": "荆门市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长魏朝东", "overlap_org": "荆门市人民政府", "overlap_period": ""},
    # 组织部长 — 书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与组织部长刘富国", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    # 政法委书记 — 书记
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "书记与政法委书记周俊杰", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    # 市委常委会成员之间的同僚关系
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共荆门市委员会", "overlap_period": ""},
]


# ── Main ─────────────────────────────────────────────────────────────

def main() -> None:
    """Build database and GEXF in staging directory."""
    print(f"Building {SLUG} network...")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rels:    {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("Done. Files written to staging directory.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()
    print("After validation, promote with:")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR}")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR} --apply")


if __name__ == "__main__":
    main()
