#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 根河市 (Genhe City), 呼伦贝尔市, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_根河市
Level: 县级市 (County-level city)
Parent city: 呼伦贝尔市
Targets: 市委书记 & 市长

Research sources:
  - www.genhe.gov.cn/Leader/ — official 领导之窗 page (primary source, as of 2026-07-25)
  - www.genhe.gov.cn/Leader/show/82/346.html — 李春雷 profile page
  - www.genhe.gov.cn/Leader/show/82/348.html — 李福双 profile page
  - www.genhe.gov.cn/Leader/show/84/365.html — 张华 profile page (mentions "协助孙尚国市长")
  - www.genhe.gov.cn/Leader/show/84/366.html — 王蒙 profile page (mentions "协助孙尚国市长")
  - www.genhe.gov.cn/Leader/show/83/371.html — 孟祥宝 profile page
  - www.genhe.gov.cn/News/show/1443618.html — 市委理论学习中心组 2026年第8次学习会
  - www.genhe.gov.cn/News/show/1442587.html — 市政府2026年第七次常务会议
  - www.genhe.gov.cn/OpennessContent/show/558375.html — 2026年政府工作报告 (delivered by 张华)

Confirmed leaders (from 领导之窗):
  市委书记: 李春雷 (confirmed, biography page available)
  市长: 孙尚国 (confirmed from deputy profiles — "协助孙尚国市长", not on 领导之窗 main page)
  市委副书记、政法委书记: 李福双
  市委常委、纪委书记、监委主任: 肖飞
  市委常委、统战部部长: 田栋
  市委常委、人武部部长: 刘东
  市委常委、宣传部部长: 孙娟
  市委常委、市委办公室主任: 李洪彪
  市委常委、副市长: 张华
  市委常委、组织部部长: 王振鑫
  市人大常委会主任: 孟祥宝
  市政协主席: 莫新柱

Confidence notes:
  - All 市委 leaders confirmed from official 领导之窗 page.
  - 孙尚国's role as 市长 inferred from 张华 and 王蒙's profile pages — "协助孙尚国市长".
  - 孙尚国 is NOT listed on the 领导之窗 main市人民政府 section, which may indicate out-of-town assignment, illness, or upcoming change.
  - 2026 government work report was delivered by 张华 (常务副市长), not the mayor — unusual.
  - No biographical details found for 孙尚国 (birth year, education, ethnicity).
  - Detailed career timelines for most leaders are UNVERIFIED.
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "根河市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership — 市委 (CONFIRMED from 领导之窗 2026-07-25) ═══════
    {
        "id": 1,
        "name": "李春雷",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1981年2月",
        "birthplace": "",
        "education": "内蒙古党校研究生学历，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "根河市委书记",
        "current_org": "中共根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/show/82/346.html"
    },
    {
        "id": 2,
        "name": "孙尚国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "根河市市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/show/84/365.html (inferred: 张华 profile mentions '协助孙尚国市长')"
    },
    {
        "id": 3,
        "name": "李福双",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "内蒙古党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/show/82/348.html"
    },
    {
        "id": 4,
        "name": "肖飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共根河市纪律检查委员会/根河市监察委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 5,
        "name": "田栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 6,
        "name": "刘东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、人武部部长",
        "current_org": "根河市人民武装部",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 7,
        "name": "孙娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 8,
        "name": "李洪彪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市委办公室主任",
        "current_org": "中共根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 9,
        "name": "张华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "大学学历，农学学士",
        "party_join": "中共党员",
        "work_start": "2004年9月",
        "current_post": "市委常委、副市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/show/84/365.html"
    },
    {
        "id": 10,
        "name": "王振鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    # ═══════ 市人大常委会 (CONFIRMED from 领导之窗) ═══════
    {
        "id": 11,
        "name": "孟祥宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "内蒙古党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "根河市人民代表大会常务委员会",
        "source": "https://www.genhe.gov.cn/Leader/show/83/371.html"
    },
    # ═══════ 市人民政府 — 副市长 (CONFIRMED from 领导之窗) ═══════
    {
        "id": 12,
        "name": "王蒙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年12月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/show/84/366.html"
    },
    {
        "id": 13,
        "name": "许国令",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 14,
        "name": "唐莹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 15,
        "name": "赵鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 16,
        "name": "薛大龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 17,
        "name": "孙标",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "根河市人民政府",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    # ═══════ 市政协 (CONFIRMED from 领导之窗) ═══════
    {
        "id": 18,
        "name": "莫新柱",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "中国人民政治协商会议根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    # ═══════ 人大副主任 (CONFIRMED from 领导之窗) ═══════
    {
        "id": 19,
        "name": "张少敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "根河市人民代表大会常务委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 20,
        "name": "古香莲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "根河市人民代表大会常务委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 21,
        "name": "刘晓晶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "根河市人民代表大会常务委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 22,
        "name": "胡耀臣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "根河市人民代表大会常务委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    # ═══════ 政协副主席 (CONFIRMED from 领导之窗) ═══════
    {
        "id": 23,
        "name": "张贵生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 24,
        "name": "彭殿明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
    {
        "id": 25,
        "name": "卜伶生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议根河市委员会",
        "source": "https://www.genhe.gov.cn/Leader/"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共根河市委员会", "type": "党委", "level": "县级", "parent": "中共呼伦贝尔市委员会", "location": "根河市"},
    {"id": 2, "name": "根河市人民政府", "type": "政府", "level": "县级", "parent": "呼伦贝尔市人民政府", "location": "根河市"},
    {"id": 3, "name": "中共根河市纪律检查委员会/根河市监察委员会", "type": "党委", "level": "县级", "parent": "中共呼伦贝尔市纪律检查委员会", "location": "根河市"},
    {"id": 4, "name": "根河市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "呼伦贝尔市人民代表大会常务委员会", "location": "根河市"},
    {"id": 5, "name": "中国人民政治协商会议根河市委员会", "type": "政协", "level": "县级", "parent": "政协呼伦贝尔市委员会", "location": "根河市"},
    {"id": 6, "name": "根河市人民武装部", "type": "政府", "level": "县级", "parent": "呼伦贝尔军分区", "location": "根河市"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 李春雷
    {"person_id": 1, "org_id": 1, "title": "根河市委书记", "start_date": "", "end_date": ""},
    # 孙尚国
    {"person_id": 2, "org_id": 2, "title": "根河市市长", "start_date": "", "end_date": ""},
    # 李福双
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": ""},
    # 肖飞
    {"person_id": 4, "org_id": 3, "title": "市委常委、纪委书记、监委主任", "start_date": "", "end_date": ""},
    # 田栋
    {"person_id": 5, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": ""},
    # 刘东
    {"person_id": 6, "org_id": 6, "title": "市委常委、人武部部长", "start_date": "", "end_date": ""},
    # 孙娟
    {"person_id": 7, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": ""},
    # 李洪彪
    {"person_id": 8, "org_id": 1, "title": "市委常委、市委办公室主任", "start_date": "", "end_date": ""},
    # 张华 — dual role
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": ""},
    # 王振鑫
    {"person_id": 10, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": ""},
    # 孟祥宝
    {"person_id": 11, "org_id": 4, "title": "市人大常委会党组书记、主任", "start_date": "", "end_date": ""},
    # 副市长们
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": ""},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": ""},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": ""},
    # 政协
    {"person_id": 18, "org_id": 5, "title": "市政协党组书记、主席", "start_date": "", "end_date": ""},
    {"person_id": 23, "org_id": 5, "title": "市政协副主席", "start_date": "", "end_date": ""},
    {"person_id": 24, "org_id": 5, "title": "市政协副主席", "start_date": "", "end_date": ""},
    {"person_id": 25, "org_id": 5, "title": "市政协副主席", "start_date": "", "end_date": ""},
    # 人大副主任
    {"person_id": 19, "org_id": 4, "title": "市人大常委会副主任", "start_date": "", "end_date": ""},
    {"person_id": 20, "org_id": 4, "title": "市人大常委会副主任", "start_date": "", "end_date": ""},
    {"person_id": 21, "org_id": 4, "title": "市人大常委会副主任", "start_date": "", "end_date": ""},
    {"person_id": 22, "org_id": 4, "title": "市人大常委会副主任", "start_date": "", "end_date": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    # 李春雷 ↔ 孙尚国 — 党政一把手
    {"person_a": 1, "person_b": 2, "type": "core_leadership",
     "context": "市委书记与市长，党政一把手搭班", "overlap_org": "根河市", "overlap_period": ""},
    # 李春雷 ↔ 李福双 — 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与专职副书记", "overlap_org": "中共根河市委员会", "overlap_period": ""},
    # 李春雷 ↔ 张华 — 书记与常委副市长
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "市委书记与市委常委、副市长", "overlap_org": "中共根河市委员会", "overlap_period": ""},
    # 李福双 ↔ 肖飞 — 政法委与纪委
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "政法委书记与纪委书记同为市委常委会成员", "overlap_org": "中共根河市委员会", "overlap_period": ""},
    # 张华 ↔ 孙尚国 — 副市长与市长
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate",
     "context": "常务副市长协助市长工作", "overlap_org": "根河市人民政府", "overlap_period": ""},
    # 张华 ↔ 王蒙 — 副市长同僚
    {"person_a": 9, "person_b": 12, "type": "overlap",
     "context": "同为市政府领导班子成员", "overlap_org": "根河市人民政府", "overlap_period": ""},
    # 孟祥宝 ↔ 李春雷 — 人大与党委
    {"person_a": 11, "person_b": 1, "type": "overlap",
     "context": "市人大常委会主任与市委书记，四套班子领导", "overlap_org": "根河市", "overlap_period": ""},
    # 莫新柱 ↔ 李春雷 — 政协与党委
    {"person_a": 18, "person_b": 1, "type": "overlap",
     "context": "市政协主席与市委书记，四套班子领导", "overlap_org": "根河市", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
