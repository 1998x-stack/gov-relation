#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Ningming County leadership network.

宁明县 — 广西壮族自治区崇左市辖县
边境县，与越南接壤

Targets: 县委书记, 县长
Research date: 2026-07-23
Web access: partially degraded (Exa rate-limited, Baidu 403, ningming.gov.cn accessible)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(BASE)
DB_PATH = os.path.join(TMP, "宁明县_network.db")
GEXF_PATH = os.path.join(TMP, "宁明县_network.gexf")
PERSONS_DIR = os.path.join(TMP)

AS_OF = "2026-07-23"


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def make_person_json(person, timeline, relationships, source_register, task_id):
    """Build a person graph JSON following person_graph_json.md schema."""
    identity = {
        "person_id": f"ningming_{person['name']}",
        "name": person["name"],
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": person.get("native_place", ""),
        "education": [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{person['name']}_{person.get('birth','')}",
            "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
            "official_profile_url": ""
        }
    }

    current_status = {
        "current_post": person.get("current_post", ""),
        "current_org": person.get("current_org", ""),
        "administrative_rank": "正处级",
        "as_of": AS_OF,
        "is_current_confirmed": person.get("current_confirmed", False),
        "source_ids": ["S001"]
    }

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "崇左市",
            "region": "宁明县",
            "job": person.get("current_post", ""),
            "task_id": task_id,
            "time_focus": "2020-2026"
        },
        "identity": identity,
        "current_status": current_status,
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {},
        "open_questions": []
    }


# ═══════════════════════════════════════════════════════════════════════
# DATA: Persons
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── ID 1: 孙金水 — Current Party Secretary (县委书记) [confirmed] ──
    {
        "id": 1, "name": "孙金水", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县委书记", "current_org": "中共宁明县委员会",
        "source": "http://www.ningming.gov.cn/ (multiple 2026 news articles: 书记孙金水)",
        "current_confirmed": True,
    },
    # ── ID 2: 周诗翔 — Current County Magistrate (县长) [confirmed] ──
    {
        "id": 2, "name": "周诗翔", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县长", "current_org": "宁明县人民政府",
        "source": "http://www.ningming.gov.cn/ (2026-04-07 article: 县长周诗翔主持会议)",
        "current_confirmed": True,
    },
    # ── ID 3: 王伟彬 — Deputy Party Secretary (县委副书记) [confirmed] ──
    {
        "id": 3, "name": "王伟彬", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县委副书记", "current_org": "中共宁明县委员会",
        "source": "http://www.ningming.gov.cn/ (2026-04-07 article: 清廉宁明会议)",
        "current_confirmed": True,
    },
    # ── ID 4: 黄纪民 — Organization Dept Head (县委常委、组织部部长) [confirmed] ──
    {
        "id": 4, "name": "黄纪民", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县委常委、组织部部长", "current_org": "中共宁明县委员会",
        "source": "http://www.ningming.gov.cn/ (2026-03-27 article: 村党组织书记培训班)",
        "current_confirmed": True,
    },
    # ── ID 5: 刘权 — Discipline Inspection Head (县委常委、纪委书记、监委主任) [confirmed] ──
    {
        "id": 5, "name": "刘权", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县委常委、纪委书记、监委主任", "current_org": "中共宁明县纪律检查委员会",
        "source": "http://www.ningming.gov.cn/ (2026-04-07 article: 清廉宁明会议)",
        "current_confirmed": True,
    },
    # ── ID 6: 陆鲜莲 — United Front Work Dept Head (县委常委、统战部部长) [confirmed] ──
    {
        "id": 6, "name": "陆鲜莲", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县委常委、统战部部长", "current_org": "中共宁明县委员会",
        "source": "http://www.ningming.gov.cn/ (2026-04-01 article: 统战工作会议)",
        "current_confirmed": True,
    },
    # ── ID 7: 赵世文 — County leader (县四家班子) [confirmed] ──
    {
        "id": 7, "name": "赵世文", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-07-21 article: 人大代表换届选举)",
        "current_confirmed": True,
    },
    # ── ID 8: 梁俊刚 — County leader (县四家班子) [confirmed] ──
    {
        "id": 8, "name": "梁俊刚", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-07-21 article: 人大代表换届选举)",
        "current_confirmed": True,
    },
    # ── ID 9: 臧劢 — County leader [confirmed] ──
    {
        "id": 9, "name": "臧劢", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-04-07 article: 清廉宁明会议)",
        "current_confirmed": True,
    },
    # ── ID 10: 卢苇 — County leader [confirmed] ──
    {
        "id": 10, "name": "卢苇", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-04-07 article: 清廉宁明会议)",
        "current_confirmed": True,
    },
    # ── ID 11: 李健 — County leader [confirmed] ──
    {
        "id": 11, "name": "李健", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-04-07 article: 清廉宁明会议)",
        "current_confirmed": True,
    },
    # ── ID 12: 匡荣韬 — County leader [confirmed] ──
    {
        "id": 12, "name": "匡荣韬", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-07-20 article: 生产性服务业会议)",
        "current_confirmed": True,
    },
    # ── ID 13: 黄缤文 — County leader [confirmed] ──
    {
        "id": 13, "name": "黄缤文", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-07-20 article: 生产性服务业会议)",
        "current_confirmed": True,
    },
    # ── ID 14: 吴中宪 — County leader [confirmed] ──
    {
        "id": 14, "name": "吴中宪", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-07-20 article: 生产性服务业会议)",
        "current_confirmed": True,
    },
    # ── ID 15: 李慧颖 — County leader [confirmed] ──
    {
        "id": 15, "name": "李慧颖", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "宁明县领导", "current_org": "宁明县",
        "source": "http://www.ningming.gov.cn/ (2026-07-20 article: 生产性服务业会议)",
        "current_confirmed": True,
    },
    # ── ID 16: 前任县委书记（待查）─
    {
        "id": 16, "name": "（前任县委书记待查）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "", "current_org": "",
        "source": "",
        "current_confirmed": False,
    },
    # ── ID 17: 前任县长（待查）─
    {
        "id": 17, "name": "（前任县长待查）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "", "current_org": "",
        "source": "",
        "current_confirmed": False,
    },
]

# ═══════════════════════════════════════════════════════════════════════
# DATA: Organizations
# ═══════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共宁明县委员会", "type": "党委", "level": "县处级", "parent": "中共崇左市委员会", "location": "广西崇左市宁明县"},
    {"id": 2, "name": "宁明县人民政府", "type": "政府", "level": "县处级", "parent": "崇左市人民政府", "location": "广西崇左市宁明县"},
    {"id": 3, "name": "宁明县人大常委会", "type": "人大", "level": "县处级", "parent": "崇左市人大常委会", "location": "广西崇左市宁明县"},
    {"id": 4, "name": "宁明县政协", "type": "政协", "level": "县处级", "parent": "崇左市政协", "location": "广西崇左市宁明县"},
    {"id": 5, "name": "中共宁明县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共崇左市纪律检查委员会", "location": "广西崇左市宁明县"},
    {"id": 6, "name": "中共宁明县委组织部", "type": "党委", "level": "县处级", "parent": "中共宁明县委员会", "location": "广西崇左市宁明县"},
    {"id": 7, "name": "中共宁明县委统战部", "type": "党委", "level": "县处级", "parent": "中共宁明县委员会", "location": "广西崇左市宁明县"},
    {"id": 8, "name": "中共崇左市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西崇左市"},
    {"id": 9, "name": "崇左市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西崇左市"},
    {"id": 10, "name": "城中镇", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县城中镇"},
    {"id": 11, "name": "明江镇", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县明江镇"},
    {"id": 12, "name": "海渊镇", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县海渊镇"},
    {"id": 13, "name": "爱店镇", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县爱店镇（边境口岸镇）"},
    {"id": 14, "name": "桐棉镇", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县桐棉镇"},
    {"id": 15, "name": "那堪镇", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县那堪镇"},
    {"id": 16, "name": "寨安乡", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县寨安乡"},
    {"id": 17, "name": "峙浪乡", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县峙浪乡"},
    {"id": 18, "name": "板棍乡", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县板棍乡"},
    {"id": 19, "name": "东安乡", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县东安乡"},
    {"id": 20, "name": "北江乡", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县北江乡"},
    {"id": 21, "name": "那楠乡", "type": "乡镇/街道", "level": "乡科级", "parent": "宁明县", "location": "宁明县那楠乡"},
    {"id": 22, "name": "宁明县融媒体中心", "type": "事业单位", "level": "乡科级", "parent": "宁明县", "location": "广西崇左市宁明县"},
    {"id": 23, "name": "派阳山林场", "type": "事业单位", "level": "乡科级", "parent": "宁明县", "location": "宁明县"},
]

# ═══════════════════════════════════════════════════════════════════════
# DATA: Positions
# ═══════════════════════════════════════════════════════════════════════

positions = [
    # 孙金水 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "宁明县委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "2026年3月至7月以县委书记身份多次公开活动（村支书培训班、高考调研、七一慰问、防汛会议等）"},
    # 周诗翔 — 县长
    {"person_id": 2, "org_id": 2, "title": "宁明县长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "2026年4月主持清廉宁明会议、7月主持生产性服务业高质量发展专题研究会"},
    # 王伟彬 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "宁明县委副书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "2026年4月出席清廉宁明建设会议并就有文件作说明"},
    # 黄纪民 — 县委常委、组织部部长
    {"person_id": 4, "org_id": 6, "title": "宁明县委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年3月主持村（社区）党组织书记培训班"},
    # 刘权 — 县委常委、纪委书记、监委主任
    {"person_id": 5, "org_id": 5, "title": "宁明县委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年4月传达清廉广西、清廉崇左建设会议精神"},
    # 陆鲜莲 — 县委常委、统战部部长
    {"person_id": 6, "org_id": 7, "title": "宁明县委常委、统战部部长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年4月主持统战工作会议并传达上级精神"},
    # 赵世文 — 县领导
    {"person_id": 7, "org_id": 1, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "县四家班子领导成员"},
    # 梁俊刚 — 县领导
    {"person_id": 8, "org_id": 1, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "县四家班子领导成员"},
    # 臧劢 — 县领导
    {"person_id": 9, "org_id": 1, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "出席清廉宁明建设会议"},
    # 卢苇 — 县领导
    {"person_id": 10, "org_id": 1, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "出席清廉宁明建设会议"},
    # 李健 — 县领导
    {"person_id": 11, "org_id": 1, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "出席清廉宁明建设会议"},
    # 匡荣韬 — 县领导
    {"person_id": 12, "org_id": 2, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "出席生产性服务业会议"},
    # 黄缤文 — 县领导
    {"person_id": 13, "org_id": 2, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "出席生产性服务业会议"},
    # 吴中宪 — 县领导
    {"person_id": 14, "org_id": 2, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "出席生产性服务业会议"},
    # 李慧颖 — 县领导
    {"person_id": 15, "org_id": 2, "title": "宁明县领导",
     "start_date": "", "end_date": "present", "rank": "", "note": "出席生产性服务业会议"},
]

# ═══════════════════════════════════════════════════════════════════════
# DATA: Relationships
# ═══════════════════════════════════════════════════════════════════════

relationships = [
    # 孙金水 ↔ 周诗翔 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "孙金水（县委书记）与周诗翔（县长）为宁明县党政主要搭档",
     "overlap_org": "宁明县党政班子",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 孙金水 ↔ 王伟彬 (上下级)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "孙金水（县委书记）与王伟彬（县委副书记）为县委班子上下级关系",
     "overlap_org": "中共宁明县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 孙金水 ↔ 黄纪民 (上下级)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "黄纪民（县委常委、组织部部长）在孙金水领导下工作",
     "overlap_org": "中共宁明县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 孙金水 ↔ 刘权 (上下级)
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "孙金水（县委书记）与刘权（县纪委书记）为县委班子上下级",
     "overlap_org": "中共宁明县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 孙金水 ↔ 陆鲜莲 (上下级)
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "陆鲜莲（县委常委、统战部部长）在孙金水领导下工作",
     "overlap_org": "中共宁明县委员会",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 周诗翔 ↔ 匡荣韬 (上下级)
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "周诗翔（县长）与匡荣韬（县领导）为县政府班子成员",
     "overlap_org": "宁明县人民政府",
     "overlap_period": "2026-",
     "confidence": "confirmed"},
    # 孙金水 ← 前任县委书记 (前后任)
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor",
     "context": "孙金水接任宁明县委书记（前任书记姓名待查）",
     "overlap_org": "中共宁明县委员会",
     "overlap_period": "",
     "confidence": "unverified"},
    # 周诗翔 ← 前任县长 (前后任)
    {"person_a": 17, "person_b": 2, "type": "predecessor_successor",
     "context": "周诗翔接任宁明县长（前任县长姓名待查）",
     "overlap_org": "宁明县人民政府",
     "overlap_period": "",
     "confidence": "unverified"},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

def build():
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r.get("context", ""), r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>宁明县领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        if p["name"].startswith("（"):
            continue  # skip placeholder persons in GEXF
        pid = p["id"]
        post = p.get("current_post", "")
        is_secretary = "书记" in post and "副" not in post and "纪委" not in post
        is_mayor = "县长" in post and "副" not in post
        is_discipline = "纪委" in post

        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        else:
            color = "100,100,100"

        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        if otype == "党委":
            ocolor = "255,200,200"
        elif otype == "政府":
            ocolor = "200,200,255"
        elif otype == "人大":
            ocolor = "200,255,255"
        elif otype == "政协":
            ocolor = "255,240,200"
        elif otype == "纪委":
            ocolor = "255,200,150"
        elif otype == "开发区":
            ocolor = "200,255,200"
        elif otype == "乡镇/街道":
            ocolor = "255,255,200"
        elif otype == "事业单位":
            ocolor = "220,220,220"
        else:
            ocolor = "200,200,200"

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        # Skip positions for placeholder persons
        person = next((p for p in persons if p["id"] == pos["person_id"]), None)
        if person and person["name"].startswith("（"):
            continue
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        # Skip relationships involving placeholders
        person_a = next((p for p in persons if p["id"] == r["person_a"]), None)
        person_b = next((p for p in persons if p["id"] == r["person_b"]), None)
        if (person_a and person_a["name"].startswith("（")) or (person_b and person_b["name"].startswith("（")):
            continue
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")

    source_register = [
        {"id": "S001", "title": "宁明县人民政府门户网站", "url": "http://www.ningming.gov.cn/",
         "publisher": "宁明县人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2026年多篇政务新闻确认县委书记孙金水、县长周诗翔在任。领导之窗页面未找到"},
        {"id": "S002", "title": "清廉宁明建设工作专班2026年第一次全体会议", "url": "http://www.ningming.gov.cn/xwzx/zwyw/t27447870.shtml",
         "publisher": "宁明县融媒体中心", "published_at": "2026-04-07", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认孙金水为县委书记、周诗翔为县长，同时列出县四家班子领导成员"},
        {"id": "S003", "title": "宁明县村（社区）党组织书记培训班开班！县委书记孙金水讲授开班第一课",
         "url": "http://www.ningming.gov.cn/xwzx/zwyw/t27407379.shtml",
         "publisher": "宁明县融媒体中心", "published_at": "2026-03-27", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认孙金水为县委书记、黄纪民为组织部部长"},
        {"id": "S004", "title": "宁明县2026年统战工作会议",
         "url": "http://www.ningming.gov.cn/xwzx/zwyw/t27430150.shtml",
         "publisher": "宁明县融媒体中心", "published_at": "2026-04-01", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认孙金水、王伟彬、陆鲜莲在任"},
        {"id": "S005", "title": "宁明县召开生产性服务业高质量发展专题研究会",
         "url": "http://www.ningming.gov.cn/xwzx/zwyw/t27939555.shtml",
         "publisher": "宁明县融媒体中心", "published_at": "2026-07-21", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认周诗翔（县长）在任，列出席领导匡荣韬、黄缤文、吴中宪、李慧颖"},
    ]

    # 孙金水 person JSON
    sjs_timeline = [
        {"start": "", "end": "present", "org": "中共宁明县委员会", "title": "宁明县委书记",
         "level": "正处级", "location": "广西宁明县", "system": "party", "rank": "正处级",
         "is_key_promotion": True,
         "notes": "2026年3月至7月以县委书记身份公开活动（村支书培训班、高考调研、七一慰问、防汛会议、党代会报告征求意见等）",
         "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到孙金水任宁明县委书记前的任何早期履历信息。身份细节（出生年、籍贯、教育、入党时间、工作起始等）均为未知",
         "confidence": "unverified", "source_ids": []},
    ]
    sjs_relationships = [
        {"person": "周诗翔", "person_id": "ningming_周诗翔", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "孙金水（县委书记）与周诗翔（县长）为宁明县党政主要搭档，共同出席多次会议",
         "overlap_org": "宁明县党政班子",
         "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"person": "王伟彬", "person_id": "ningming_王伟彬", "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "孙金水（县委书记）与王伟彬（县委副书记）为县委班子上下级关系",
         "overlap_org": "中共宁明县委员会",
         "overlap_period": "2026-",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"person": "黄纪民", "person_id": "ningming_黄纪民", "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "黄纪民（县委常委、组织部部长）在孙金水领导下主持村支书培训班",
         "overlap_org": "中共宁明县委员会",
         "overlap_period": "2026-",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "刘权", "person_id": "ningming_刘权", "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "刘权（县委常委、纪委书记）在孙金水领导下传达上级精神",
         "overlap_org": "中共宁明县委员会",
         "overlap_period": "2026-",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "陆鲜莲", "person_id": "ningming_陆鲜莲", "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "陆鲜莲（县委常委、统战部部长）在孙金水领导下工作",
         "overlap_org": "中共宁明县委员会",
         "overlap_period": "2026-",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"person": "（前任县委书记）", "person_id": "ningming_previous_secretary", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "孙金水接任宁明县委书记（前任书记姓名待查）",
         "overlap_org": "中共宁明县委员会",
         "overlap_period": "",
         "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
    ]
    sjs_json = make_person_json(persons[0], sjs_timeline, sjs_relationships, source_register, "guangxi_宁明县")
    sjs_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-崇左市-县委书记-孙金水.json")
    with open(sjs_path, "w", encoding="utf-8") as f:
        json.dump(sjs_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {sjs_path}")

    # 周诗翔 person JSON
    zsx_timeline = [
        {"start": "", "end": "present", "org": "宁明县人民政府", "title": "宁明县长",
         "level": "正处级", "location": "广西宁明县", "system": "government", "rank": "正处级",
         "is_key_promotion": True,
         "notes": "2026年4月主持清廉宁明会议、7月主持生产性服务业高质量发展专题研究会",
         "confidence": "confirmed", "source_ids": ["S001", "S002", "S005"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到周诗翔任宁明县长前的任何早期履历信息。身份细节（出生年、籍贯、教育、入党时间、工作起始等）均为未知",
         "confidence": "unverified", "source_ids": []},
    ]
    zsx_relationships = [
        {"person": "孙金水", "person_id": "ningming_孙金水", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "周诗翔（县长）与孙金水（县委书记）为宁明县党政主要搭档",
         "overlap_org": "宁明县党政班子",
         "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"person": "匡荣韬", "person_id": "ningming_匡荣韬", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "匡荣韬（县领导）在周诗翔主持的生产性服务业会议上作为出席领导",
         "overlap_org": "宁明县人民政府",
         "overlap_period": "2026-",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "（前任县长）", "person_id": "ningming_previous_mayor", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "周诗翔接任宁明县长（前任县长姓名待查）",
         "overlap_org": "宁明县人民政府",
         "overlap_period": "",
         "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
    ]
    zsx_json = make_person_json(persons[1], zsx_timeline, zsx_relationships, source_register, "guangxi_宁明县")
    zsx_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-崇左市-县长-周诗翔.json")
    with open(zsx_path, "w", encoding="utf-8") as f:
        json.dump(zsx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zsx_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
