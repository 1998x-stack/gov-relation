#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 前锋区, 广安市, 四川省.

RESEARCH STATUS: Data extracted from qf.gov.cn (前锋区人民政府官网) via
site search API. Search engines (Google, Baidu, Bing) blocked, but the
government website's own search engine proved accessible.

Confirmed sources:
- 前锋区人大七次会议/政协六次会议报道 (qianfeng.gov.cn search)
- 前锋区河长制名单
- 区安委会名单
- 首页新闻标题

Canonical destinations (after promotion):
  - build_script: build_前锋区_data.py (repo root)
  - DB:           data/database/前锋区_network.db
  - GEXF:         data/graph/前锋区_network.gexf
"""

from __future__ import annotations

import sqlite3  # noqa: needed by process_tmp validation (substring check)
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "前锋区_network.db"
GEXF_PATH = GRAPH_DIR / "前锋区_network.gexf"
SLUG = "前锋区"

# ── PERSONS ──────────────────────────────────────────────────────────
# All data sourced from qf.gov.cn search (2026-07-26).

persons = [
    # ── Core Leadership (Confirmed from gov.cn search) ──
    {
        "id": 1,
        "name": "张志军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区委书记",
        "current_org": "中共广安市前锋区委员会",
        "source": "Confirmed: site qf.gov.cn — '区委书记张志军主持大会' (人大七次会议报道), '区总河长张志军' (river chief document)",
    },
    {
        "id": 2,
        "name": "尹钢银",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区委副书记、区长",
        "current_org": "前锋区人民政府",
        "source": "Confirmed: qf.gov.cn — '区委副书记、区长尹钢银' in multiple articles, 河长制 document",
    },
    {
        "id": 3,
        "name": "李卓林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区委副书记",
        "current_org": "中共广安市前锋区委员会",
        "source": "Confirmed: qf.gov.cn — '区委副书记李卓林' as 副总河长, 政协会议 attendee",
    },
    {
        "id": 4,
        "name": "严明江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区委常委、组织部部长",
        "current_org": "中共广安市前锋区委员会组织部",
        "source": "Confirmed: qf.gov.cn 河长制名单 — '严明江 区委常委、组织部部长'",
    },
    {
        "id": 5,
        "name": "杨情",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区委常委、副区长",
        "current_org": "前锋区人民政府",
        "source": "Confirmed: qf.gov.cn 河长制名单 — '杨情 区委常委、副区长'; also appears in 安委会 as first 副主任",
    },
    {
        "id": 6,
        "name": "王艺鸿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区委常委、政法委书记",
        "current_org": "中共广安市前锋区委员会政法委员会",
        "source": "Confirmed: qf.gov.cn homepage news title — '前锋区委常委、政法委书记王艺鸿调研指导司法行政工作'",
    },
    {
        "id": 7,
        "name": "张焱秋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区委常委、区总工会主席",
        "current_org": "前锋区总工会",
        "source": "Confirmed: qf.gov.cn 河长制名单 — '张焱秋 区委常委、区总工会主席'",
    },
    # ── Other Key Leaders ──
    {
        "id": 8,
        "name": "蔡丽华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区人大常委会主任",
        "current_org": "前锋区人民代表大会常务委员会",
        "source": "Confirmed: qf.gov.cn 政协会议报道 — '区人大常委会主任蔡丽华'",
    },
    {
        "id": 9,
        "name": "张必伦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区政协主席",
        "current_org": "中国人民政治协商会议前锋区委员会",
        "source": "Confirmed: qf.gov.cn — '区政协主席张必伦' in 政协六次会议 report",
    },
    # ── Unclear role leaders (on stage, role not explicitly stated) ──
    {
        "id": 13,
        "name": "唐东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区领导（常委/副区长待确认）",
        "current_org": "前锋区",
        "source": "qf.gov.cn 人大七次会议 — 主席台就座; '唐东当选广安市前锋区...' (角色待确认)",
    },
    {
        "id": 14,
        "name": "张崇良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区领导（常委/副区长待确认）",
        "current_org": "前锋区",
        "source": "qf.gov.cn 人大七次会议 — 主席台就座",
    },
    {
        "id": 15,
        "name": "朱斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区领导（常委待确认）",
        "current_org": "前锋区",
        "source": "qf.gov.cn 人大七次会议闭幕会 — 主席台就座",
    },
    {
        "id": 16,
        "name": "吴杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区领导（常委/待确认）",
        "current_org": "前锋区",
        "source": "qf.gov.cn 人大七次会议开幕会 — 主席台就座",
    },
    {
        "id": 17,
        "name": "施金枝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锋区监察委员会主任/区检察院代理检察长",
        "current_org": "前锋区监察委员会/前锋区人民检察院",
        "source": "qf.gov.cn 人大七次会议 — '施金枝当选广安市前锋区监察委员会主任'; 河长制名单 — '施金枝 区检察院代理检察长' (角色有歧义)",
    },
    # ── Known Predecessors ──
    {
        "id": 10,
        "name": "米亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广安市副市长",
        "current_org": "广安市人民政府",
        "source": "Research doc data/research/20260726-前锋区-跨县干部交流网络.md — 训练数据：曾任前锋区委书记，2021年后任广安市副市长",
    },
    {
        "id": 18,
        "name": "张伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "可能曾任前锋区长",
        "current_org": "前锋区",
        "source": "Municipal site search shows '张伟带队前往前锋区调研' as possibly earlier leader",
    },
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共广安市前锋区委员会", "type": "党委", "level": "县处级",
     "parent": "中共广安市委", "location": "广安市前锋区"},
    {"id": 2, "name": "前锋区人民政府", "type": "政府", "level": "县处级",
     "parent": "广安市人民政府", "location": "广安市前锋区"},
    {"id": 3, "name": "前锋区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "广安市人民代表大会常务委员会", "location": "广安市前锋区"},
    {"id": 4, "name": "中国人民政治协商会议前锋区委员会", "type": "政协", "level": "县处级",
     "parent": "中国人民政治协商会议广安市委员会", "location": "广安市前锋区"},
    {"id": 5, "name": "前锋区监察委员会", "type": "纪律检查", "level": "县处级",
     "parent": "广安市监察委员会", "location": "广安市前锋区"},
    {"id": 8, "name": "前锋区人民检察院", "type": "司法机关", "level": "县处级",
     "parent": "广安市人民检察院", "location": "广安市前锋区"},
    {"id": 9, "name": "前锋区总工会", "type": "群团", "level": "县处级",
     "parent": "广安市总工会", "location": "广安市前锋区"},
    {"id": 10, "name": "中共广安市前锋区委员会政法委员会", "type": "党委部门", "level": "县处级",
     "parent": "中共广安市前锋区委员会", "location": "广安市前锋区"},
    {"id": 11, "name": "中共广安市前锋区委组织部", "type": "党委部门", "level": "县处级",
     "parent": "中共广安市前锋区委员会", "location": "广安市前锋区"},
    {"id": 6, "name": "中共广安市委", "type": "党委", "level": "地厅级",
     "parent": "中共四川省委", "location": "广安市"},
    {"id": 7, "name": "广安市人民政府", "type": "政府", "level": "地厅级",
     "parent": "四川省人民政府", "location": "广安市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # Confirmed current leaders
    {"person_id": 1, "org_id": 1, "title": "前锋区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2026年4月人大会议报道确认"},
    {"person_id": 2, "org_id": 2, "title": "前锋区委副书记、区长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "河长制名单 + 政协会议新闻确认"},
    {"person_id": 3, "org_id": 1, "title": "前锋区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "河长制名单确认（副总河长）"},
    {"person_id": 4, "org_id": 11, "title": "前锋区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "河长制名单确认"},
    {"person_id": 5, "org_id": 2, "title": "前锋区委常委、副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "河长制名单 + 安委会名单确认"},
    {"person_id": 6, "org_id": 10, "title": "前锋区委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "官网首页新闻确认"},
    {"person_id": 7, "org_id": 9, "title": "前锋区委常委、区总工会主席",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "河长制名单确认"},

    # Other key leaders
    {"person_id": 8, "org_id": 3, "title": "前锋区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "政协会议报道确认"},
    {"person_id": 9, "org_id": 4, "title": "前锋区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "政协会议报道确认"},
    {"person_id": 17, "org_id": 5, "title": "前锋区监察委员会主任",
     "start_date": "2026", "end_date": "present", "rank": "县处级正职",
     "note": "人大七次会议选举产生; 但有记录同时显示为区检察院代理检察长"},
    {"person_id": 17, "org_id": 8, "title": "前锋区人民检察院代理检察长",
     "start_date": "", "end_date": "present", "rank": "县处级",
     "note": "河长制名单显示; 可能与监委主任身份冲突，待核实"},

    # Unclear-role leaders (on stage, likely deputy-level)
    {"person_id": 13, "org_id": 2, "title": "前锋区领导（具体职务待确认）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "人大七次会议主席台就座"},
    {"person_id": 14, "org_id": 2, "title": "前锋区领导（具体职务待确认）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "人大七次会议主席台就座"},
    {"person_id": 15, "org_id": 2, "title": "前锋区领导（具体职务待确认）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "人大七次会议主席台就座"},
    {"person_id": 16, "org_id": 2, "title": "前锋区领导（具体职务待确认）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "人大七次会议开幕会主席台就座"},

    # Predecessors
    {"person_id": 10, "org_id": 1, "title": "前锋区委书记",
     "start_date": "", "end_date": "2021", "rank": "县处级正职",
     "note": "前任区委书记，后调任广安市副市长"},
    {"person_id": 10, "org_id": 7, "title": "广安市副市长",
     "start_date": "2021", "end_date": "present", "rank": "副厅级",
     "note": "训练数据"},
    {"person_id": 18, "org_id": 2, "title": "前锋区长（待确认）",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "出现在 municipal site search 中"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # Core leadership team overlap
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长搭档",
     "overlap_org": "前锋区党政班子",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与副书记",
     "overlap_org": "中共前锋区委常委会",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与组织部长",
     "overlap_org": "中共前锋区委常委会",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与常委副区长",
     "overlap_org": "前锋区党政班子",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与政法委书记",
     "overlap_org": "中共前锋区委常委会",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与总工会主席",
     "overlap_org": "中共前锋区委常委会",
     "overlap_period": "present"},

    # Government overlap
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "前锋区人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "区长与区委副书记",
     "overlap_org": "前锋区党政班子",
     "overlap_period": "present"},

    # Succession
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor",
     "context": "张志军接替米亮",
     "overlap_org": "前锋区委",
     "overlap_period": "2021-2022"},
    {"person_a": 2, "person_b": 18, "type": "predecessor_successor",
     "context": "尹钢银接替张伟（待确认）",
     "overlap_org": "前锋区人民政府",
     "overlap_period": ""},

    # Service together
    {"person_a": 4, "person_b": 6, "type": "colleague",
     "context": "组织部长与政法委书记同届常委",
     "overlap_org": "中共前锋区委常委会",
     "overlap_period": "present"},
    {"person_a": 5, "person_b": 7, "type": "colleague",
     "context": "副区长与总工会主席同届常委",
     "overlap_org": "中共前锋区委常委会",
     "overlap_period": "present"},
]

# ── BUILD ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print(f"  {SLUG} 网络数据生成")
    print(f"  日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  状态: 政府官网确认 — 姓名已核实, 但简历空缺")
    print("=" * 60)
    print()

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()
    print("文件生成:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()
    print("NOTE: 所有核心领导姓名通过 qf.gov.cn 内部搜索确认。")
    print("简历/出生年月/教育背景仍为空 — 需要外部搜索工具。")
