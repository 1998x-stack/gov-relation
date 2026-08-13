#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兴安区（黑龙江省鹤岗市）领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件
(schema via gov_relation.schema → sqlite3)

Level: 市辖区
Province: 黑龙江省
Parent City: 鹤岗市
Region: 兴安区
Targets: 区委书记 & 区长

Data Sources:
- 兴安区人民政府官网 http://www.hgxa.gov.cn/ (confirmed active, ICP: 黑ICP备17007900号-1)
- 向阳区人民政府官网 https://www.hgxyq.gov.cn/
- 鹤岗市人民政府官网 https://www.hegang.gov.cn/
- 百度搜索任前公示摘要
- 澎湃新闻报道

Key Finding: 王洪江系2024年10月从区长直接晋升为区委书记（内部晋升通道）。
兴安区与向阳区领导模式不同：兴安区为书记/区长分设，向阳区为一肩挑。

Research Date: 2026-07-24

Gaps:
1. 王洪江2024年10月前完整履历
2. 袁锐完整履历、籍贯、出生年月
3. 王洪江的前任兴安区委书记是谁、去向
4. 袁锐的前任兴安区长是谁、去向
"""

import os
import sys
import sqlite3  # noqa: F401 — used via gov_relation

_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, "../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from gov_relation.runner import run_build

SLUG = "兴安区"
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# --- Data ---

persons = [
    # ── 区委领导 (Party Committee Leaders) ──
    {
        "id": 1,
        "name": "王洪江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "鹤岗市兴安区委书记",
        "current_org": "中共鹤岗市兴安区委员会",
        "source": "confirmed - hgxa.gov.cn 2026年5-7月新闻; 2024年10月任前公示",
        "notes": "原兴安区委副书记、区长（2024年10月前）；2024年10月拟任县市区党委书记公示期；籍贯待查"
    },
    {
        "id": 2,
        "name": "袁锐",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区委副书记、政府区长",
        "current_org": "鹤岗市兴安区人民政府",
        "source": "confirmed - hgxa.gov.cn 2025-2026年政府会议报道; 2026年1月补选市人大代表",
        "notes": "主持区政府全面工作，分管区审计局；完整履历待查"
    },
    {
        "id": 3,
        "name": "殷兆霞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区人大常委会主任",
        "current_org": "鹤岗市兴安区人民代表大会常务委员会",
        "source": "confirmed - 澎湃新闻2025年2月春节慰问报道; hgxa.gov.cn",
        "notes": "完整履历待查"
    },
    # ── 区政府领导 (Government Leaders) ──
    {
        "id": 4,
        "name": "李林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区委常委、政府副区长",
        "current_org": "鹤岗市兴安区人民政府",
        "source": "confirmed - hgxa.gov.cn 政府领导分工页面",
        "notes": "负责安全生产、财税、发改、信访、统计、机关事务；分管应急管理局、财政局、发改局、园区办、信访局、统计局、机关事务服务中心"
    },
    {
        "id": 5,
        "name": "缪泽明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区委常委、政府副区长",
        "current_org": "鹤岗市兴安区人民政府",
        "source": "confirmed - hgxa.gov.cn 政府领导分工页面",
    },
    {
        "id": 6,
        "name": "韩洋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区委常委、政府副区长",
        "current_org": "鹤岗市兴安区人民政府",
        "source": "confirmed - hgxa.gov.cn 政府领导分工页面",
    },
    {
        "id": 7,
        "name": "高云龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区政府副区长",
        "current_org": "鹤岗市兴安区人民政府",
        "source": "confirmed - hgxa.gov.cn 2026年7月陪同区委书记调研城建新闻",
        "notes": "分管城建、街政"
    },
    {
        "id": 8,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区政府副区长、公安兴安分局局长",
        "current_org": "鹤岗市公安局兴安分局",
        "source": "confirmed - hgxa.gov.cn 政府领导分工页面",
        "notes": "兼任公安分局局长"
    },
    {
        "id": 9,
        "name": "陈钊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区政府副区长",
        "current_org": "鹤岗市兴安区人民政府",
        "source": "confirmed - hgxa.gov.cn 政府领导分工页面",
    },
    {
        "id": 10,
        "name": "朱士河",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市兴安区领导（级别待确认）",
        "current_org": "鹤岗市兴安区人民政府",
        "source": "hgxa.gov.cn 2026年1月乡村振兴会议报道",
        "notes": "具体职务待确认"
    },
]

organizations = [
    {"id": 1, "name": "中共鹤岗市兴安区委员会", "type": "党委", "level": "县处级",
     "parent": "中共鹤岗市委员会", "location": "黑龙江省鹤岗市兴安区"},
    {"id": 2, "name": "鹤岗市兴安区人民政府", "type": "政府", "level": "县处级",
     "parent": "鹤岗市人民政府", "location": "黑龙江省鹤岗市兴安区"},
    {"id": 3, "name": "鹤岗市兴安区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "鹤岗市人大常委会", "location": "黑龙江省鹤岗市兴安区"},
    {"id": 4, "name": "中国人民政治协商会议鹤岗市兴安区委员会", "type": "政协", "level": "县处级",
     "parent": "鹤岗市政协", "location": "黑龙江省鹤岗市兴安区"},
    {"id": 5, "name": "中共鹤岗市兴安区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共鹤岗市纪律检查委员会", "location": "黑龙江省鹤岗市兴安区"},
    {"id": 6, "name": "鹤岗市公安局兴安分局", "type": "政府", "level": "县处级",
     "parent": "鹤岗市公安局", "location": "黑龙江省鹤岗市兴安区"},
]

positions = [
    # 王洪江
    {"person_id": 1, "org_id": 1, "title": "鹤岗市兴安区委书记",
     "start_date": "2024年10月", "end_date": "present", "rank": "县处级正职",
     "note": "2024年10月任前公示期满后上任；此前为区长"},
    {"person_id": 1, "org_id": 1, "title": "鹤岗市兴安区委副书记",
     "start_date": "", "end_date": "2024年10月", "rank": "县处级正职",
     "note": "此前担任区长期间兼任区委副书记"},
    {"person_id": 1, "org_id": 2, "title": "鹤岗市兴安区政府区长（原）",
     "start_date": "", "end_date": "2024年10月", "rank": "县处级正职",
     "note": "晋升书记前的职务"},
    # 袁锐
    {"person_id": 2, "org_id": 1, "title": "鹤岗市兴安区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 2, "title": "鹤岗市兴安区政府区长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "主持区政府全面工作，分管审计局"},
    # 殷兆霞
    {"person_id": 3, "org_id": 3, "title": "鹤岗市兴安区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职"},
    # 李林
    {"person_id": 4, "org_id": 2, "title": "鹤岗市兴安区政府副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责安全生产、财税、发改、信访、统计、机关事务"},
    {"person_id": 4, "org_id": 1, "title": "鹤岗市兴安区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 缪泽明
    {"person_id": 5, "org_id": 2, "title": "鹤岗市兴安区政府副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 5, "org_id": 1, "title": "鹤岗市兴安区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 韩洋
    {"person_id": 6, "org_id": 2, "title": "鹤岗市兴安区政府副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 6, "org_id": 1, "title": "鹤岗市兴安区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 高云龙
    {"person_id": 7, "org_id": 2, "title": "鹤岗市兴安区政府副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管城建、街政"},
    # 张涛
    {"person_id": 8, "org_id": 2, "title": "鹤岗市兴安区政府副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 8, "org_id": 6, "title": "鹤岗市公安局兴安分局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任"},
    # 陈钊
    {"person_id": 9, "org_id": 2, "title": "鹤岗市兴安区政府副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 朱士河
    {"person_id": 10, "org_id": 2, "title": "鹤岗市兴安区领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "具体职务和级别待确认"},
]

relationships = [
    # 党政核心
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政正职搭档",
     "overlap_org": "中共鹤岗市兴安区委员会/鹤岗市兴安区人民政府", "overlap_period": "2024年至今"},
    # 区委书记与各常委副区长
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与常委副区长",
     "overlap_org": "中共鹤岗市兴安区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与常委副区长",
     "overlap_org": "中共鹤岗市兴安区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与常委副区长",
     "overlap_org": "中共鹤岗市兴安区委员会", "overlap_period": "至今"},
    # 区委书记与人大
    {"person_a": 1, "person_b": 3, "type": "党政人大", "context": "区委书记与人大常委会主任",
     "overlap_org": "中共鹤岗市兴安区委员会/鹤岗市兴安区人大常委会", "overlap_period": "至今"},
    # 区长与副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与常务副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
    # 前后任（内部晋升）
    {"person_a": 1, "person_b": 2, "type": "前后任", "context": "王洪江原为区长，袁锐接任区长；王洪江晋升书记",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "2024年交接"},
    # 同僚关系
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "同为常委副区长",
     "overlap_org": "中共鹤岗市兴安区委员会", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "同为常委副区长",
     "overlap_org": "中共鹤岗市兴安区委员会", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "同为常委副区长",
     "overlap_org": "中共鹤岗市兴安区委员会", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "同为政府副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "同为政府副区长",
     "overlap_org": "鹤岗市兴安区人民政府", "overlap_period": "至今"},
]

# --- Build ---

if __name__ == "__main__":
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
    print(f"✅ {SLUG} — Build complete!")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
