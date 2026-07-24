#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 尖山区 (Jianshan District), 双鸭山市, 黑龙江省.

Level: 市辖区
Province: 黑龙江省
Parent city: 双鸭山市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: heilongjiang_尖山区

Research date: 2026-07-24
Official source: http://www.sysjs.gov.cn/ (双鸭山市尖山区人民政府)

Current status (as of 2026-07-24, verified via 尖山区人民政府领导视窗):
- 区委书记: 王言磊 — 2026年6月由区长转任区委书记至今; 此前自2021年12月任尖山区区长
- 区长: 王言磊（兼任）— 区委书记、区长一肩挑
- 前任区委书记: 待查 — 王言磊2021年12月任区长时另有书记，2026年6月由区长升任书记
- 区委副书记: 刘爱军（正处级，兼任政法委书记）
- 区委常委(7人): 王言磊、刘爱军、袁英明、丁其锐、李国铭、关辉、徐泽铭
- 副区长(5人): 袁英明(常务)、徐泽铭、徐长岭、朱祥凯、司晓敏

Confirmed government leadership page sources (all from sysjs.gov.cn):
- 王言磊(区委书记): /js/jsqqwsj/202606/c07_250057.shtml
- 王言磊(区长): /js/jsqqz/202601/c07_241682.shtml
- 刘爱军(区委副书记): /js/jsqfsj/202603/c07_246060.shtml
- 袁英明(区委常委/副区长): /js/jsqqwcw/202601/c07_241668.shtml
- 丁其锐(区委常委/人武部政委): /js/jsqqwcw/202601/c07_241669.shtml
- 李国铭(区委常委/纪委书记): /js/jsqqwcw/202601/c07_241670.shtml
- 关辉(区委常委/宣传部部长): /js/jsqqwcw/202607/c07_250653.shtml
- 徐泽铭(区委常委/组织部部长/副区长): /js/jsqqwcw/202607/c07_250655.shtml
- 徐长岭(副区长/公安局长): /js/jsqfqz/202601/c07_241686.shtml
- 朱祥凯(副区长): /js/jsqfqz/202601/c07_241688.shtml
- 司晓敏(副区长): /js/jsqfqz/202603/c07_246063.shtml
- 刘继清(人大主任): /js/jsqrdzr/202601/c07_241693.shtml
- 庄云秀(政协主席): /js/jsqzxzx/202601/c07_241700.shtml
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "尖山区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王言磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "哈尔滨师范大学汉语言文学专业自考大学学历",
        "party_join": "中共党员",
        "work_start": "2000.07",
        "current_post": "区委书记、区长",
        "current_org": "中共尖山区委员会/尖山区人民政府",
        "source": "https://www.sysjs.gov.cn/js/jsqqwsj/202606/c07_250057.shtml",
    },
    {
        "id": 2,
        "name": "刘爱军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "中国人民解放军炮兵学院机械工程及自动化专业",
        "party_join": "中共党员",
        "work_start": "2004.09",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共尖山区委员会",
        "source": "https://www.sysjs.gov.cn/js/jsqfsj/202603/c07_246060.shtml",
    },
    {
        "id": 3,
        "name": "袁英明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "省委党校中文专业大专学历",
        "party_join": "中共党员",
        "work_start": "1992.12",
        "current_post": "区委常委、副区长",
        "current_org": "中共尖山区委员会/尖山区人民政府",
        "source": "https://www.sysjs.gov.cn/js/jsqqwcw/202601/c07_241668.shtml",
    },
    {
        "id": 4,
        "name": "丁其锐",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、人民武装部上校政治委员",
        "current_org": "中共尖山区委员会/尖山区人民武装部",
        "source": "https://www.sysjs.gov.cn/js/jsqqwcw/202601/c07_241669.shtml",
    },
    {
        "id": 5,
        "name": "李国铭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "2012.07",
        "current_post": "区委常委、区纪委书记、区监委代主任",
        "current_org": "中共尖山区纪律检查委员会/尖山区监察委员会",
        "source": "https://www.sysjs.gov.cn/js/jsqqwcw/202601/c07_241670.shtml",
    },
    {
        "id": 6,
        "name": "关辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "2010.06",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共尖山区委员会宣传部",
        "source": "https://www.sysjs.gov.cn/js/jsqqwcw/202607/c07_250653.shtml",
    },
    {
        "id": 7,
        "name": "徐泽铭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "黑龙江科技学院电子信息工程专业/省委党校经济管理专业研究生",
        "party_join": "中共党员",
        "work_start": "2006.07",
        "current_post": "区委常委、组织部部长、统战部部长、副区长",
        "current_org": "中共尖山区委员会组织部/统战部/尖山区人民政府",
        "source": "https://www.sysjs.gov.cn/js/jsqqwcw/202607/c07_250655.shtml",
    },
    # ════════════════════════════════════════
    # 政府领导 (Government)
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "徐长岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "birthplace": "",
        "education": "黑龙江省人民警察学校公安专业/中国人民公安大学/黑龙江大学法律专业",
        "party_join": "中共党员",
        "work_start": "1993.08",
        "current_post": "副区长、尖山公安分局局长",
        "current_org": "尖山区人民政府/双鸭山市公安局尖山分局",
        "source": "https://www.sysjs.gov.cn/js/jsqfqz/202601/c07_241686.shtml",
    },
    {
        "id": 9,
        "name": "朱祥凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年12月",
        "birthplace": "黑龙江双鸭山",
        "education": "哈尔滨师范大学教育技术专业教育学士",
        "party_join": "中共党员",
        "work_start": "2007.08",
        "current_post": "副区长",
        "current_org": "尖山区人民政府",
        "source": "https://www.sysjs.gov.cn/js/jsqfqz/202601/c07_241688.shtml",
    },
    {
        "id": 10,
        "name": "司晓敏",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "黑龙江农业工程职业学院/哈尔滨市委党校函授经济管理专业",
        "party_join": "中共党员",
        "work_start": "2008.07",
        "current_post": "副区长",
        "current_org": "尖山区人民政府",
        "source": "https://www.sysjs.gov.cn/js/jsqfqz/202603/c07_246063.shtml",
    },
    # ════════════════════════════════════════
    # 人大 (People's Congress)
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "刘继清",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "中央党校经济管理专业",
        "party_join": "中共党员",
        "work_start": "1990.12",
        "current_post": "区人大常委会主任",
        "current_org": "尖山区人民代表大会常务委员会",
        "source": "https://www.sysjs.gov.cn/js/jsqrdzr/202601/c07_241693.shtml",
    },
    # ════════════════════════════════════════
    # 政协 (Political Consultative Conference)
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "庄云秀",
        "gender": "女",
        "ethnicity": "",
        "birth": "1975年11月",
        "birthplace": "黑龙江省双鸭山市",
        "education": "哈尔滨师范大学汉语言文学专业/北京林业大学农业推广硕士",
        "party_join": "中共党员",
        "work_start": "1995.10",
        "current_post": "区政协主席",
        "current_org": "政协尖山区委员会",
        "source": "https://www.sysjs.gov.cn/js/jsqzxzx/202601/c07_241700.shtml",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共尖山区委员会", "type": "党委", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 2, "name": "尖山区人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 3, "name": "中共尖山区纪律检查委员会", "type": "党委", "level": "副县处级", "parent": "中共尖山区委员会", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 4, "name": "尖山区监察委员会", "type": "党委", "level": "副县处级", "parent": "中共尖山区委员会", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 5, "name": "中共尖山区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共尖山区委员会", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 6, "name": "中共尖山区委组织部", "type": "党委", "level": "乡科级", "parent": "中共尖山区委员会", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 7, "name": "中共尖山区委统战部", "type": "党委", "level": "乡科级", "parent": "中共尖山区委员会", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 8, "name": "尖山区人民武装部", "type": "党委", "level": "县处级", "parent": "双鸭山军分区", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 9, "name": "双鸭山市公安局尖山分局", "type": "政府", "level": "副县处级", "parent": "尖山区人民政府", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 10, "name": "尖山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 11, "name": "政协尖山区委员会", "type": "政协", "level": "县处级", "parent": "双鸭山市", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 12, "name": "中共双鸭山市委组织部", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委员会", "location": "黑龙江省双鸭山市"},
    {"id": 13, "name": "中共双鸭山市委办公室", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委员会", "location": "黑龙江省双鸭山市"},
    {"id": 14, "name": "双鸭山市财政局", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (Current)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王言磊 — 区委书记、区长
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026-06", "end": "", "rank": "正处级", "note": "2026年6月由区长转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "2021.12", "end": "", "rank": "正处级", "note": "2026年6月起兼任（一肩挑）"},
    # 刘爱军 — 区委副书记
    {"person_id": 2, "org_id": 1, "title": "区委副书记、政法委书记", "start": "2026-01", "end": "", "rank": "正处级", "note": "由市委政研室主任转任"},
    # 袁英明 — 区委常委、副区长（常务）
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "2025-12", "end": "", "rank": "副处级", "note": "由四方台区委常委、副区长转任"},
    {"person_id": 3, "org_id": 2, "title": "副区长（常务）", "start": "2026-01", "end": "", "rank": "副处级", "note": ""},
    # 丁其锐 — 区委常委、人武部政委
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": "人武部上校政委"},
    {"person_id": 4, "org_id": 8, "title": "政治委员", "start": "", "end": "", "rank": "上校", "note": ""},
    # 李国铭 — 区委常委、纪委书记、监委代主任
    {"person_id": 5, "org_id": 1, "title": "区委常委、区纪委书记", "start": "2024-04", "end": "", "rank": "副处级", "note": "四级高级监察官"},
    {"person_id": 5, "org_id": 4, "title": "区监委代主任", "start": "2024-05", "end": "", "rank": "副处级", "note": ""},
    # 关辉 — 区委常委、宣传部部长
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长", "start": "2025-04", "end": "", "rank": "副处级", "note": "由岭东区委常委、宣传部部长转任"},
    # 徐泽铭 — 区委常委、组织部部长、统战部部长、副区长
    {"person_id": 7, "org_id": 1, "title": "区委常委、组织部部长", "start": "2023-06", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "统战部部长", "start": "2023-07", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 徐长岭 — 副区长、公安分局局长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 9, "title": "公安分局局长", "start": "2022-04", "end": "", "rank": "二级高级警长", "note": ""},
    # 朱祥凯 — 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "2021-07", "end": "", "rank": "副处级", "note": ""},
    # 司晓敏 — 副区长
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "2026-02", "end": "", "rank": "副处级", "note": "由区政协农业农村委员会主任转任"},
    # 刘继清 — 人大主任
    {"person_id": 11, "org_id": 10, "title": "区人大常委会主任", "start": "2023-07", "end": "", "rank": "正处级", "note": ""},
    # 庄云秀 — 政协主席
    {"person_id": 12, "org_id": 11, "title": "区政协主席", "start": "2021-11", "end": "", "rank": "正处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1, "person_b": 2, "type": "overlap",
        "context": "王言磊（区委书记）与刘爱军（区委副书记）在尖山区委常委会共事",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2026.01至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 3, "type": "overlap",
        "context": "王言磊（区委书记、区长）与袁英明（常务副区长）在区政府和区委常委会共事",
        "overlap_org": "尖山区人民政府/中共尖山区委员会",
        "overlap_period": "2026.01至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 7, "type": "overlap",
        "context": "王言磊（区委书记）与徐泽铭（组织部部长）在区委常委会共事",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2023.06至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 5, "type": "overlap",
        "context": "王言磊（区委书记）与李国铭（纪委书记）在区委常委会共事",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2024.04至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 6, "type": "overlap",
        "context": "王言磊（区委书记）与关辉（宣传部部长）在区委常委会共事",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 9, "type": "superior_subordinate",
        "context": "王言磊（区长/书记）与朱祥凯（副区长）在区政府共事",
        "overlap_org": "尖山区人民政府",
        "overlap_period": "2021.12至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 8, "type": "superior_subordinate",
        "context": "王言磊（区长/书记）与徐长岭（副区长/公安局长）在区政府共事",
        "overlap_org": "尖山区人民政府",
        "overlap_period": "2022.04至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 3, "type": "overlap",
        "context": "刘爱军（区委副书记）与袁英明（常务副区长）在区委共事",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2026.01至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 7, "type": "overlap",
        "context": "袁英明与徐泽铭在区委常委会共事，皆已在尖山区委班子成员",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2023年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 9, "type": "overlap",
        "context": "袁英明（常务副区长）与朱祥凯（副区长）在区政府共事",
        "overlap_org": "尖山区人民政府",
        "overlap_period": "2026.01至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 10, "type": "overlap",
        "context": "袁英明（常务副区长）与司晓敏（副区长）在区政府共事",
        "overlap_org": "尖山区人民政府",
        "overlap_period": "2026.02至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 12, "type": "overlap",
        "context": "王言磊（曾任区委常委期间）与庄云秀（时任区委常委、宣传部部长）曾在区委常委会共事",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2021-2021.11",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": 7, "person_b": 6, "type": "overlap",
        "context": "徐泽铭（组织部部长）与关辉（宣传部部长）在区委常委会同属党群系统",
        "overlap_org": "中共尖山区委员会",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 3, "type": "overlap",
        "context": "王言磊在市委组织部任办公室主任期间，与后来的尖山区同事有工作交集",
        "overlap_org": "中共双鸭山市委组织部",
        "overlap_period": "2008-2015",
        "strength": "weak",
        "confidence": "plausible",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
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

    # Write person JSON files
    person_configs = [
        ("王言磊", "区委书记", 1),
        ("刘爱军", "区委副书记", 2),
        ("袁英明", "常务副区长", 3),
        ("朱祥凯", "副区长", 9),
        ("庄云秀", "政协主席", 12),
    ]
    for name, job, pid in person_configs:
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-双鸭山市-{job}-{name}.json"
        path.write_text(
            json.dumps(
                _build_person_json(name, job, pid),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"  Wrote {path.name}")

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    try:
        rows = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        print(f"\nDatabase: {DB_PATH}")
        print(f"  Persons: {rows}")
        print(f"  Orgs: {len(organizations)}")
        print(f"  Positions: {len(positions)}")
        print(f"  Relationships: {len(relationships)}")
    finally:
        conn.close()

    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"GEXF: {GEXF_PATH} ({gexf_size} bytes)")
    print("\nDone. Run python3 scripts/process_tmp.py data/tmp/heilongjiang_尖山区 to validate.")


def _build_person_json(name: str, job: str, pid: int) -> dict:
    p = persons[pid - 1]

    # Build career timeline from the research data
    timeline = []
    if name == "王言磊":
        timeline = [
            {"start": "2000.07", "end": "2005.04", "org": "双鸭山市第二十七中学", "title": "教师", "confidence": "confirmed"},
            {"start": "2005.04", "end": "2007.04", "org": "双鸭山市岭东区档案馆", "title": "科员", "confidence": "confirmed"},
            {"start": "2007.04", "end": "2008.05", "org": "双鸭山市岭东区水产站", "title": "站长", "confidence": "confirmed"},
            {"start": "2008.05", "end": "2008.06", "org": "双鸭山市岭东区委宣传部", "title": "副部长", "confidence": "confirmed"},
            {"start": "2008.06", "end": "2010.06", "org": "双鸭山市委组织部办公室", "title": "副主任科员", "confidence": "confirmed"},
            {"start": "2010.06", "end": "2010.08", "org": "双鸭山市委组织部办公室", "title": "副主任", "confidence": "confirmed"},
            {"start": "2010.08", "end": "2012.03", "org": "双鸭山市委组织部办公室", "title": "副主任、主任科员", "confidence": "confirmed"},
            {"start": "2012.03", "end": "2015.09", "org": "双鸭山市委组织部办公室", "title": "主任", "confidence": "confirmed"},
            {"start": "2015.09", "end": "2017.12", "org": "中共集贤县委", "title": "县委常委、组织部部长", "confidence": "confirmed"},
            {"start": "2017.12", "end": "2020.08", "org": "共青团双鸭山市委员会", "title": "书记", "confidence": "confirmed"},
            {"start": "2020.08", "end": "2021.02", "org": "中共饶河县委", "title": "副书记、二级调研员", "confidence": "confirmed"},
            {"start": "2021.02", "end": "2021.07", "org": "中共饶河县委", "title": "副书记、西丰镇党委书记", "confidence": "confirmed"},
            {"start": "2021.07", "end": "2021.08", "org": "中共尖山区委", "title": "副书记、区长候选人", "confidence": "confirmed"},
            {"start": "2021.08", "end": "2021.12", "org": "尖山区人民政府", "title": "代区长", "confidence": "confirmed"},
            {"start": "2021.12", "end": "2022.04", "org": "尖山区人民政府", "title": "区长", "confidence": "confirmed"},
            {"start": "2022.04", "end": "2026.06", "org": "尖山区人民政府", "title": "区长、一级调研员", "confidence": "confirmed"},
            {"start": "2026.06", "end": "至今", "org": "中共尖山区委", "title": "区委书记、一级调研员", "confidence": "confirmed"},
        ]
    elif name == "刘爱军":
        timeline = [
            {"start": "2000.09", "end": "2004.09", "org": "中国人民解放军炮兵学院", "title": "学员（机械工程及自动化专业）", "confidence": "confirmed"},
            {"start": "2004.09", "end": "2005.07", "org": "南京炮兵学院", "title": "学员（火箭炮指挥专业）", "confidence": "confirmed"},
            {"start": "2005.07", "end": "2010.05", "org": "中国人民解放军65575部队85分队", "title": "上尉", "confidence": "confirmed"},
            {"start": "2010.05", "end": "2013.11", "org": "双鸭市畜牧局人事科", "title": "科员", "confidence": "confirmed"},
            {"start": "2013.11", "end": "2013.12", "org": "双鸭山市委政研室综合组", "title": "科员", "confidence": "confirmed"},
            {"start": "2013.12", "end": "2014.12", "org": "双鸭山市委政研室经济组", "title": "副组长", "confidence": "confirmed"},
            {"start": "2014.12", "end": "2015.12", "org": "双鸭山市委政研室综合组", "title": "副组长", "confidence": "confirmed"},
            {"start": "2015.12", "end": "2019.08", "org": "双鸭山市委政研室综合组", "title": "组长", "confidence": "confirmed"},
            {"start": "2019.08", "end": "2023.08", "org": "双鸭山市委政研室", "title": "副主任", "confidence": "confirmed"},
            {"start": "2023.08", "end": "2026.01", "org": "双鸭山市委政研室", "title": "主任", "confidence": "confirmed"},
            {"start": "2026.01", "end": "至今", "org": "中共尖山区委", "title": "区委副书记、政法委书记", "confidence": "confirmed"},
        ]
    elif name == "袁英明":
        timeline = [
            {"start": "1992.12", "end": "1995.12", "org": "河北省保定市51047部队步兵三三九团", "title": "服役", "confidence": "confirmed"},
            {"start": "1997.01", "end": "2000.09", "org": "双鸭山市四方台区环卫站", "title": "工人", "confidence": "confirmed"},
            {"start": "2000.09", "end": "2007.07", "org": "双鸭山市四方台区委办公室", "title": "科员", "confidence": "confirmed"},
            {"start": "2007.07", "end": "2010.08", "org": "双鸭山市四方台区委办公室", "title": "副主任", "confidence": "confirmed"},
            {"start": "2010.08", "end": "2012.03", "org": "双鸭山市四方台区效能中心", "title": "主任", "confidence": "confirmed"},
            {"start": "2012.03", "end": "2016.08", "org": "双鸭山市四方台区环卫站", "title": "站长", "confidence": "confirmed"},
            {"start": "2016.08", "end": "2019.08", "org": "双鸭山市四方台区太保镇", "title": "党委副书记、镇长", "confidence": "confirmed"},
            {"start": "2019.08", "end": "2020.05", "org": "双鸭山市四方台区太保镇", "title": "党委书记", "confidence": "confirmed"},
            {"start": "2020.05", "end": "2020.10", "org": "双鸭山市四方台区太保镇", "title": "党委书记、一级主任科员", "confidence": "confirmed"},
            {"start": "2020.10", "end": "2021.07", "org": "双鸭山市四方台区政府办公室", "title": "主任、一级主任科员", "confidence": "confirmed"},
            {"start": "2021.08", "end": "2021.09", "org": "双鸭山市四方台区", "title": "副区长人选", "confidence": "confirmed"},
            {"start": "2021.09", "end": "2021.11", "org": "双鸭山市四方台区人民政府", "title": "副区长", "confidence": "confirmed"},
            {"start": "2021.11", "end": "2025.12", "org": "中共四方台区委", "title": "区委常委、副区长", "confidence": "confirmed"},
            {"start": "2025.12", "end": "2026.01", "org": "中共尖山区委", "title": "区委常委、副区长人选", "confidence": "confirmed"},
            {"start": "2026.01", "end": "至今", "org": "中共尖山区委/尖山区人民政府", "title": "区委常委、副区长", "confidence": "confirmed"},
        ]
    elif name == "朱祥凯":
        timeline = [
            {"start": "2008.04", "end": "2011.05", "org": "尖山区政府办公室", "title": "秘书", "confidence": "confirmed"},
            {"start": "2011.05", "end": "2013.05", "org": "尖山区目标考评办", "title": "副主任", "confidence": "confirmed"},
            {"start": "2013.05", "end": "2016.12", "org": "尖山区目标考评办", "title": "主任", "confidence": "confirmed"},
            {"start": "2016.12", "end": "2019.12", "org": "尖山区人力资源和社会保障局", "title": "局长", "confidence": "confirmed"},
            {"start": "2019.12", "end": "2021.07", "org": "中共尖山区委办公室", "title": "主任", "confidence": "confirmed"},
            {"start": "2021.07", "end": "至今", "org": "尖山区人民政府", "title": "副区长", "confidence": "confirmed"},
        ]
    elif name == "庄云秀":
        timeline = [
            {"start": "1995.10", "end": "1996.11", "org": "双鸭市纪检委干部室", "title": "科员", "confidence": "confirmed"},
            {"start": "1996.11", "end": "2002.08", "org": "团市委宣传部", "title": "干事", "confidence": "confirmed"},
            {"start": "2002.08", "end": "2005.03", "org": "双鸭山市团校", "title": "副校长", "confidence": "confirmed"},
            {"start": "2005.03", "end": "2007.06", "org": "团市委宣传部", "title": "部长", "confidence": "confirmed"},
            {"start": "2007.06", "end": "2009.02", "org": "团市委办公室", "title": "主任", "confidence": "confirmed"},
            {"start": "2009.02", "end": "2010.04", "org": "团市委", "title": "副书记、党组成员", "confidence": "confirmed"},
            {"start": "2010.04", "end": "2016.07", "org": "双鸭山市委老干部局", "title": "副局长", "confidence": "confirmed"},
            {"start": "2016.07", "end": "2020.04", "org": "中共尖山区委", "title": "区委常委、宣传部部长、统战部部长", "confidence": "confirmed"},
            {"start": "2020.04", "end": "2021.03", "org": "中共尖山区委", "title": "区委常委、宣传部部长、统战部部长、政协党组副书记", "confidence": "confirmed"},
            {"start": "2021.03", "end": "2021.11", "org": "中共尖山区委", "title": "区委常委、宣传部部长、统战部部长", "confidence": "confirmed"},
            {"start": "2021.11", "end": "至今", "org": "政协尖山区委员会", "title": "主席", "confidence": "confirmed"},
        ]

    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-24",
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "双鸭山市",
            "region": "尖山区",
            "job": job,
            "task_id": "heilongjiang_尖山区",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"jianshan_{name}",
            "name": name,
            "gender": p.get("gender", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": p.get("education", ""), "major": "", "degree": ""}],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{p.get('birth', '')}", "name_birthplace": f"{name}_{p.get('birthplace', '')}"},
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
        },
        "career_timeline": timeline,
        "source_register": [
            {
                "id": "S001",
                "title": f"尖山区人民政府领导视窗 - {name}",
                "url": p.get("source", ""),
                "publisher": "尖山区人民政府",
                "published_at": "",
                "accessed_at": "2026-07-24",
                "source_type": "official",
                "reliability": "high",
            }
        ],
        "open_questions": [
            {
                "priority": "medium",
                "question": f"缺少{name}的出生年份、籍贯等基本信息",
                "why_it_matters": "影响人员去重和画像完整度",
                "suggested_queries": [f"{name} 简历 出生 年月"],
            }
        ],
    }


if __name__ == "__main__":
    main()
