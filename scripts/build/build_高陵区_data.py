#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 高陵区, 西安市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_高陵区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 高陵区人民政府官方网站 (www.gaoling.gov.cn) — confirmed current leadership resumes
  - Government leadership pages for individual leaders (as of 2026-05-14 update)
  - News articles from the official website (various dates through 2026-07-24)

Key findings:
  - 区委书记: 张水利（现任西安市人大常委会副主任兼高陵区委书记）
  - 区长: 贾强（区委副书记、区长、区政府党组书记，兼西安经开区党工委副书记、管委会主任）
  - 区政府领导班子共9人（含挂职1人）全部在政府网站确认
  - 区委常委信息：张水利（书记）、贾强（副书记）、陈灵（常务副区长）、张跃进（副区长）
  - 张子扬为新疆和硕县挂职干部

Confidence notes:
  - 张水利（区委书记）未在区政府领导之窗页面公示，其职务通过新闻"市人大常委会副主任、区委书记张水利"确认
  - 区政府领导（9人）姓名、职务、分工、简历全部在政府网站确认
  - 区委常委名单不完全，仅能确认4位区委常委身份
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401

SLUG = "高陵区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 张水利 — 区委书记、西安市人大常委会副主任
    {
        "id": 1,
        "name": "张水利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记、西安市人大常委会副主任",
        "current_org": "中共西安市高陵区委员会",
        "source": "高陵区政府官网—张跃进领导活动页面引用'市人大常委会副主任、区委书记张水利'"
    },
    # 贾强 — 区委副书记、区长、区政府党组书记
    {
        "id": 2,
        "name": "贾强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长、区政府党组书记",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/jq/1.html"
    },
    # 陈灵 — 区委常委、常务副区长、区政府党组副书记
    {
        "id": 3,
        "name": "陈灵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年12月",
        "birthplace": "",
        "education": "研究生学历，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长、区政府党组副书记",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/cl/1.html"
    },
    # 张跃进 — 区委常委、副区长
    {
        "id": 4,
        "name": "张跃进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年5月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/zyj/1.html"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (区政府) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 贾海军 — 副区长、公安高陵分局局长
    {
        "id": 5,
        "name": "贾海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "大学学历，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安高陵分局局长兼督察长",
        "current_org": "西安市公安局高陵分局",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/jhj/1.html"
    },
    # 李亚省 — 副区长
    {
        "id": 6,
        "name": "李亚省",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "",
        "education": "研究生学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/lys/1.html"
    },
    # 薛霞 — 副区长（非中共党员）
    {
        "id": 7,
        "name": "薛霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年5月",
        "birthplace": "",
        "education": "大学学历，会计硕士",
        "party_join": "致公党",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/xx/1.html"
    },
    # 张敏涛 — 副区长
    {
        "id": 8,
        "name": "张敏涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/zmt/1.html"
    },
    # 樊晓峰 — 副区长
    {
        "id": 9,
        "name": "樊晓峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/fxf/1.html"
    },
    # 张子扬 — 副区长（挂职）
    {
        "id": 10,
        "name": "张子扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "西安市高陵区人民政府",
        "source": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/zzy/1.html"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共西安市高陵区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委员会",
        "location": "西安市高陵区"
    },
    {
        "id": 2,
        "name": "西安市高陵区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市高陵区"
    },
    {
        "id": 3,
        "name": "西安市公安局高陵分局",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市公安局",
        "location": "西安市高陵区"
    },
    {
        "id": 4,
        "name": "西安经济技术开发区管委会",
        "type": "开发区",
        "level": "地厅级",
        "parent": "西安市人民政府",
        "location": "西安市"
    },
    {
        "id": 5,
        "name": "西安市人民代表大会常务委员会",
        "type": "人大",
        "level": "地厅级",
        "parent": "西安市",
        "location": "西安市"
    },
    {
        "id": 6,
        "name": "中共陕西省委政法委",
        "type": "党委",
        "level": "省直",
        "parent": "中共陕西省委员会",
        "location": "西安市"
    },
    {
        "id": 7,
        "name": "西安市阎良区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市阎良区"
    },
    {
        "id": 8,
        "name": "西安市临潼区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市临潼区"
    },
    {
        "id": 9,
        "name": "西安市雁塔区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市雁塔区"
    },
    {
        "id": 10,
        "name": "西安市住房和城乡建设局",
        "type": "政府",
        "level": "地厅级",
        "parent": "西安市人民政府",
        "location": "西安市"
    },
    {
        "id": 11,
        "name": "西安城市基础设施建设投资集团有限公司",
        "type": "事业单位",
        "level": "地厅级",
        "parent": "西安市人民政府",
        "location": "西安市"
    },
    {
        "id": 12,
        "name": "陕西省西咸新区空港新城开发建设集团有限公司",
        "type": "事业单位",
        "level": "地厅级",
        "parent": "西咸新区管委会",
        "location": "西安市"
    },
    {
        "id": 13,
        "name": "西安市高陵区崇皇街道党工委",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共西安市高陵区委员会",
        "location": "西安市高陵区"
    },
    {
        "id": 14,
        "name": "新疆和硕县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "新疆巴音郭楞蒙古自治州人民政府",
        "location": "新疆和硕县"
    },
]

positions_data = [
    # 张水利 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正厅级（兼市级领导）", "note": "confirmed via news: 市人大常委会副主任、区委书记"},
    {"person_id": 1, "org_id": 5, "title": "西安市人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "confirmed via news article"},

    # 贾强 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长、区政府党组书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 2, "org_id": 4, "title": "西安经济技术开发区党工委副书记、管委会主任", "start_date": "unknown", "end_date": "present", "rank": "正厅/副厅", "note": "confirmed via government resume"},
    {"person_id": 2, "org_id": 10, "title": "党组成员、副主任、副局长", "start_date": "unknown", "end_date": "unknown", "rank": "副厅级", "note": "西安市城乡建设委员会党组成员、副主任，西安市住房和城乡建设局党组成员、副局长"},
    {"person_id": 2, "org_id": 11, "title": "党委副书记、副董事长、总经理", "start_date": "unknown", "end_date": "unknown", "rank": "副厅/正处", "note": "西安城市基础设施建设投资集团有限公司"}, 

    # 陈灵 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长、区政府党组副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 3, "org_id": 6, "title": "省委政法委执法监督处副处长、政策研究室主任、执法监督处处长", "start_date": "unknown", "end_date": "unknown", "rank": "正处级", "note": "省委政法委工作经历"},

    # 张跃进 — 副区长
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 4, "org_id": 7, "title": "阎良区新华路街道党工委书记、办事处主任、团区委书记等", "start_date": "unknown", "end_date": "unknown", "rank": "正科→副处", "note": "阎良区基层工作经历"},

    # 贾海军 — 副区长、公安局长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 5, "org_id": 3, "title": "公安高陵分局局长兼督察长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 5, "org_id": 6, "title": "省委政法委执法监督处副处长、维稳工作二处处长", "start_date": "unknown", "end_date": "unknown", "rank": "正处级", "note": "市委政法委工作经历"},

    # 李亚省 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 6, "org_id": 8, "title": "临潼区信用联社党委副书记、主任、理事长", "start_date": "unknown", "end_date": "unknown", "rank": "", "note": "金融系统经历"},
    {"person_id": 6, "org_id": 9, "title": "雁塔区副区长（挂职）、区财政局局长", "start_date": "unknown", "end_date": "unknown", "rank": "副处级", "note": "confirmed"},

    # 薛霞 — 副区长（致公党）
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 7, "org_id": 12, "title": "西咸新区空港新城开发建设集团副总经理", "start_date": "unknown", "end_date": "unknown", "rank": "", "note": "国企经历"},

    # 张敏涛 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 8, "org_id": 8, "title": "临潼区委办公室主任、新丰街道办主任等", "start_date": "unknown", "end_date": "unknown", "rank": "正科→副处", "note": "临潼区工作经历"},

    # 樊晓峰 — 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 9, "org_id": 13, "title": "崇皇街道党工委书记、办事处主任", "start_date": "unknown", "end_date": "unknown", "rank": "正科级", "note": "高陵区本地基层成长"},

    # 张子扬 — 副区长（挂职）
    {"person_id": 10, "org_id": 2, "title": "副区长（挂职）", "start_date": "unknown", "end_date": "present", "rank": "副处级（挂职）", "note": "confirmed"},
    {"person_id": 10, "org_id": 14, "title": "和硕县委副书记、常务副县长（正县级）", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "挂职高陵前职务"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政一把手工作关系", "overlap_org": "中共西安市高陵区委员会", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "区长—常务副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 4, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 5, "type": "党政搭档", "context": "区长—副区长（公安局长）工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 6, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 7, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 8, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 9, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 10, "type": "党政搭档", "context": "区长—挂职副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},

    # 区委常委之间的工作关系
    {"person_a": 1, "person_b": 3, "type": "党政关系", "context": "区委书记与常务副区长（区委常委）", "overlap_org": "中共西安市高陵区委员会", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 4, "type": "党政关系", "context": "区委书记与副区长（区委常委）", "overlap_org": "中共西安市高陵区委员会", "overlap_period": "unknown-present"},
    {"person_a": 3, "person_b": 4, "type": "工作关系", "context": "常务副区长与副区长同为政府班子成员", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 3, "person_b": 5, "type": "工作关系", "context": "常务副区长与副区长（公安局长）工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},

    # 政法委背景关联
    {"person_a": 3, "person_b": 5, "type": "同系统背景", "context": "陈灵（省委政法委）与贾海军（市委政法委）均有政法系统工作经历", "overlap_org": "陕西省/西安市政法委系统", "overlap_period": "unknown"},
    {"person_a": 5, "person_b": 10, "type": "工作关系", "context": "副区长（公安局长）与挂职副区长工作关系", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},

    # 基层经历关联（临潼背景）
    {"person_a": 6, "person_b": 8, "type": "同地域工作经历", "context": "李亚省（临潼区信用联社）与张敏涛（临潼区委办公室）均有临潼区工作经历", "overlap_org": "西安市临潼区", "overlap_period": "unknown"},

    # 高陵本地基层
    {"person_a": 9, "person_b": 4, "type": "工作关系", "context": "樊晓峰（副区长）与张跃进（副区长、区委常委）同为政府班子成员", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 9, "person_b": 6, "type": "工作关系", "context": "樊晓峰与李亚省同为副区长", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 7, "person_b": 8, "type": "工作关系", "context": "薛霞与张敏涛同为副区长", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path

PERSON_FILES = [
    # 区委书记 张水利
    {
        "filename": f"{TODAY}-陕西省-西安市-区委书记-张水利.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "西安市",
                "region": "高陵区",
                "job": "区委书记",
                "task_id": "shaanxi_高陵区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "gaoling_zhang_shuili",
                "name": "张水利",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "unknown",
                "birthplace": "unknown",
                "native_place": "unknown",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张水利_unknown",
                    "name_birthplace": "张水利_unknown",
                    "official_profile_url": "NOT_FOUND"
                }
            },
            "current_status": {
                "current_post": "高陵区委书记、西安市人大常委会副主任",
                "current_org": "中共西安市高陵区委员会",
                "administrative_rank": "正厅级（兼任市级领导）",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "中共西安市高陵区委员会", "title": "区委书记", "level": "县处级", "location": "陕西西安", "system": "party", "rank": "正厅级（兼）", "is_key_promotion": True, "notes": "同时担任西安市人大常委会副主任", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "unknown", "end": "present", "org": "西安市人民代表大会常务委员会", "title": "西安市人大常委会副主任", "level": "地厅级", "location": "陕西西安", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "贾强", "person_id": "gaoling_jia_qiang", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "区委书记—区长党政一把手搭档", "overlap_org": "中共西安市高陵区委员会", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["地区领导"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party", "government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "因公开资料有限，无法评估晋升速度", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "高陵区政府官网—张跃进领导活动页面", "url": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/zyj/1.html", "publisher": "高陵区人民政府", "published_at": "2026-05-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "页面'领导活动'部分引用了'市人大常委会副主任、区委书记张水利'"},
                {"id": "S002", "title": "高陵区人民政府官网新闻", "url": "https://www.gaoling.gov.cn/xwzx/zwyw/", "publisher": "高陵区人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委书记张水利多次出现在官方新闻报道中"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "张水利的完整履历（出生、籍贯、教育背景、完整职业生涯）在公开信息中未找到"
            },
            "open_questions": [
                {"priority": "critical", "question": "张水利的出生年份、籍贯、教育背景", "why_it_matters": "区委书记是核心人物，缺少基本身份信息", "suggested_queries": ["张水利 简历 高陵", "张水利 西安市人大 任职"], "last_attempted": AS_OF},
                {"priority": "high", "question": "张水利何时开始担任高陵区委书记", "why_it_matters": "明确党政搭档时间起始点", "suggested_queries": ["张水利 任高陵区委书记"], "last_attempted": AS_OF},
                {"priority": "high", "question": "张水利的前任区委书记是谁、去向如何", "why_it_matters": "分析领导更替模式", "suggested_queries": ["高陵区 前任区委书记"], "last_attempted": AS_OF}
            ]
        }
    },
    # 区长 贾强
    {
        "filename": f"{TODAY}-陕西省-西安市-区长-贾强.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "西安市",
                "region": "高陵区",
                "job": "区长",
                "task_id": "shaanxi_高陵区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "gaoling_jia_qiang",
                "name": "贾强",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1973年3月",
                "birthplace": "unknown",
                "native_place": "unknown",
                "education": ["大学学历", "工商管理硕士"],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "贾强_1973年3月",
                    "name_birthplace": "贾强_unknown",
                    "official_profile_url": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/jq/1.html"
                }
            },
            "current_status": {
                "current_post": "高陵区委副书记、区长、区政府党组书记",
                "current_org": "西安市高陵区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "西安市城乡建设委员会", "title": "党组成员、副主任", "level": "地厅级", "location": "陕西西安", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "西安市住房和城乡建设局", "title": "党组成员、副局长", "level": "地厅级", "location": "陕西西安", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "机构改革后的职务", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "西安城市基础设施建设投资集团有限公司", "title": "党委副书记、副董事长、总经理", "level": "地厅级", "location": "陕西西安", "system": "government", "rank": "正厅级国企", "is_key_promotion": True, "notes": "城投集团高管经历", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "present", "org": "西安市高陵区人民政府", "title": "区委副书记、区长、区政府党组书记", "level": "县处级", "location": "陕西西安", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "同时兼任西安经济技术开发区党工委副书记、管委会主任", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "present", "org": "西安经济技术开发区管委会", "title": "党工委副书记、管委会主任", "level": "地厅级", "location": "陕西西安", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "张水利", "person_id": "gaoling_zhang_shuili", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "区长与区委书记党政搭档", "overlap_org": "中共西安市高陵区委员会", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "陈灵", "person_id": "gaoling_chen_ling", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—常务副区长工作搭档", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "张跃进", "person_id": "gaoling_zhang_yuejin", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—副区长工作搭档", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["城市建设", "住房保障", "国企管理"],
                "secondary_specializations": ["开发区管理"],
                "career_pattern": "从市级建设系统到国企高管再到区县主官",
                "systems_experience": ["government", "state_owned_enterprise"],
                "geographic_pattern": ["西安"],
                "promotion_velocity": {"summary": "从市建委副主任到城投集团总经理再到区长，跨系统能力突出", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "高陵区人民政府—贾强简历", "url": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/jq/1.html", "publisher": "高陵区人民政府", "published_at": "2026-05-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "confirmed区长简历"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "各职位具体任职起止时间"
            },
            "open_questions": [
                {"priority": "high", "question": "贾强在西安市建委、住建局、城投集团的具体任职起止时间", "why_it_matters": "精确时间线对关系网络分析重要", "suggested_queries": ["贾强 西安市建委 任职时间", "贾强 城投集团 总经理"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "贾强何时开始担任高陵区长", "why_it_matters": "明确现任岗位起始时间", "suggested_queries": ["贾强 高陵区 区长 任命"], "last_attempted": AS_OF}
            ]
        }
    },
    # 常务副区长 陈灵
    {
        "filename": f"{TODAY}-陕西省-西安市-常务副区长-陈灵.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "西安市",
                "region": "高陵区",
                "job": "常务副区长",
                "task_id": "shaanxi_高陵区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "gaoling_chen_ling",
                "name": "陈灵",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1982年12月",
                "birthplace": "unknown",
                "native_place": "unknown",
                "education": ["研究生学历", "法律硕士"],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "陈灵_1982年12月",
                    "name_birthplace": "陈灵_unknown",
                    "official_profile_url": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/cl/1.html"
                }
            },
            "current_status": {
                "current_post": "高陵区委常委、常务副区长、区政府党组副书记",
                "current_org": "西安市高陵区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "陕西省委政法委", "title": "执法监督处副处长", "level": "省直", "location": "陕西西安", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "陕西省委政法委", "title": "政策研究室主任", "level": "省直", "location": "陕西西安", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "陕西省委政法委", "title": "执法监督处处长", "level": "省直", "location": "陕西西安", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "中共西安市高陵区委员会", "title": "区委常委", "level": "县处级", "location": "陕西西安", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "兼任通远街道党工委书记", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "present", "org": "西安市高陵区人民政府", "title": "区委常委、常务副区长、区政府党组副书记", "level": "县处级", "location": "陕西西安", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "贾强", "person_id": "gaoling_jia_qiang", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—常务副区长工作搭档", "overlap_org": "西安市高陵区人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "张水利", "person_id": "gaoling_zhang_shuili", "relationship_type": "overlap", "strength": "medium", "evidence": "区委常委与区委书记工作关系", "overlap_org": "中共西安市高陵区委员会", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "贾海军", "person_id": "gaoling_jia_haijun", "relationship_type": "same_system", "strength": "medium", "evidence": "陈灵（省委政法委执法监督处）与贾海军（市委政法委执法监督处）均有政法系统工作经历", "overlap_org": "陕西省/西安市政法委系统", "overlap_period": "unknown", "direction": "undirected", "confidence": "plausible", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["政法系统", "政策研究"],
                "secondary_specializations": ["应急管理"],
                "career_pattern": "从省委政法系统到区县领导岗位",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["陕西→西安高陵"],
                "promotion_velocity": {"summary": "1982年出生，省委政法系统历练后到高陵区任常委、常务副区长，属于相对年轻的区领导", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "高陵区人民政府—陈灵简历", "url": "https://www.gaoling.gov.cn/zwgk/qzfxxgkml/ldzc/cl/1.html", "publisher": "高陵区人民政府", "published_at": "2026-05-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "confirmed常务副区长简历"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "各职位具体任职起止时间及省委政法委期间的具体年份"
            },
            "open_questions": [
                {"priority": "high", "question": "陈灵在省委政法委各职位的具体任职起止时间", "why_it_matters": "精确时间线对关系网络分析重要", "suggested_queries": ["陈灵 陕西省委政法委 任职"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "陈灵何时开始担任高陵区委常委、常务副区长", "why_it_matters": "明确起任时间", "suggested_queries": ["陈灵 高陵 常务副区长 任命"], "last_attempted": AS_OF}
            ]
        }
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("Writing person JSON files...")
    for entry in PERSON_FILES:
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_FILES)} person JSONs")
    print("=" * 60)


if __name__ == "__main__":
    main()
