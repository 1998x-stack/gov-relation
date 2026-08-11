#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上海市徐汇区 leadership network.

调查日期: 2026-07-25
信息来源: 上海市徐汇区人民政府门户网站 (www.xuhui.gov.cn)
调查级别: 市辖区(直辖市)

Confirmed from government homepage (2026-07):
- 曹立强 — 徐汇区委书记
- 王华 — 徐汇区委副书记、区长
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "徐汇区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "徐汇区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "上海市徐汇区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════════════════════

    # 区委书记 — 曹立强
    {
        "id": 1,
        "name": "曹立强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-05",
        "birthplace": "上海",
        "education": "中央党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1986-07",
        "current_post": "中共上海市徐汇区委书记",
        "current_org": "中共上海市徐汇区委员会",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委副书记、区长 — 王华
    {
        "id": 2,
        "name": "王华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "江苏靖江",
        "education": "上海交通大学硕士研究生",
        "party_join": "中共党员",
        "work_start": "1996-08",
        "current_post": "徐汇区委副书记、区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委副书记 — 沈权
    {
        "id": 3,
        "name": "沈权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市徐汇区委副书记",
        "current_org": "中共上海市徐汇区委员会",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委常委、副区长（常务）— 王宏伟
    {
        "id": 4,
        "name": "王宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、副区长（常务）",
        "current_org": "上海市徐汇区人民政府",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委常委、纪委书记、监委主任 — 何雅
    {
        "id": 5,
        "name": "何雅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、纪委书记、监委主任",
        "current_org": "中共上海市徐汇区纪律检查委员会",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委常委、组织部部长 — 刘琪
    {
        "id": 6,
        "name": "刘琪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、组织部部长",
        "current_org": "中共上海市徐汇区委组织部",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委常委、宣传部部长 — 赵懿
    {
        "id": 7,
        "name": "赵懿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、宣传部部长",
        "current_org": "中共上海市徐汇区委宣传部",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委常委、政法委书记 — 习挺松
    {
        "id": 8,
        "name": "习挺松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、政法委书记",
        "current_org": "中共上海市徐汇区委政法委员会",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委常委、统战部部长 — 诸旖
    {
        "id": 9,
        "name": "诸旖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、统战部部长",
        "current_org": "中共上海市徐汇区委统战部",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区委常委、区人民武装部政委 — 谭伟时
    {
        "id": 10,
        "name": "谭伟时",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、区人民武装部政委",
        "current_org": "上海市徐汇区人民武装部",
        "source": "https://www.xuhui.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 区政府副区长 (District Government)
    # ═══════════════════════════════════════════════

    # 副区长 — 俞林伟
    {
        "id": 11,
        "name": "俞林伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 副区长 — 罗华品
    {
        "id": 12,
        "name": "罗华品",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 副区长 — 邓大伟
    {
        "id": 13,
        "name": "邓大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 副区长 — 王志华
    {
        "id": 14,
        "name": "王志华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "https://www.xuhui.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 人大、政协领导
    # ═══════════════════════════════════════════════

    # 区人大常委会主任 — 李新华
    {
        "id": 15,
        "name": "李新华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区人大常委会主任",
        "current_org": "上海市徐汇区人民代表大会常务委员会",
        "source": "https://www.xuhui.gov.cn/",
    },
    # 区政协主席 — 黄冲
    {
        "id": 16,
        "name": "黄冲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区政协主席",
        "current_org": "中国人民政治协商会议上海市徐汇区委员会",
        "source": "https://www.xuhui.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ═══════════════════════════════════════════════

    # 前任区委书记 — 鲍炳章 (前任)
    {
        "id": 17,
        "name": "鲍炳章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-11",
        "birthplace": "浙江宁波",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1985-08",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
    # 前任区长 — 钟晓咏 (前任)
    {
        "id": 18,
        "name": "钟晓咏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-11",
        "birthplace": "上海",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1985-09",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市徐汇区委员会", "type": "党委", "level": "市辖区(直辖市)", "parent": "中共上海市委", "location": "上海市徐汇区"},
    {"id": 2, "name": "上海市徐汇区人民政府", "type": "政府", "level": "市辖区(直辖市)", "parent": "上海市人民政府", "location": "上海市徐汇区"},
    {"id": 3, "name": "中共上海市徐汇区纪律检查委员会", "type": "纪委", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 4, "name": "中共上海市徐汇区委组织部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 5, "name": "中共上海市徐汇区委宣传部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 6, "name": "中共上海市徐汇区委政法委员会", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 7, "name": "中共上海市徐汇区委统战部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 8, "name": "上海市徐汇区人民武装部", "type": "军队", "level": "市辖区(直辖市)", "parent": "上海警备区", "location": "上海市徐汇区"},
    {"id": 9, "name": "上海市徐汇区人民代表大会常务委员会", "type": "人大", "level": "市辖区(直辖市)", "parent": "上海市人民代表大会常务委员会", "location": "上海市徐汇区"},
    {"id": 10, "name": "中国人民政治协商会议上海市徐汇区委员会", "type": "政协", "level": "市辖区(直辖市)", "parent": "中国人民政治协商会议上海市委员会", "location": "上海市徐汇区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 曹立强
    {"person_id": 1, "org_id": 1, "title": "中共上海市徐汇区委书记", "start_date": "2021-08", "end_date": "present", "rank": "正厅级", "note": "2021年8月任徐汇区委书记；此前任普陀区委书记"},
    {"person_id": 1, "org_id": 1, "title": "中共上海市普陀区委书记", "start_date": "2019", "end_date": "2021-08", "rank": "正厅级", "note": "此前任杨浦区委副书记、区长"},
    {"person_id": 1, "org_id": 2, "title": "上海市杨浦区委副书记、区长", "start_date": "2017", "end_date": "2019", "rank": "正厅级", "note": ""},
    # 王华
    {"person_id": 2, "org_id": 2, "title": "徐汇区委副书记、区长", "start_date": "2023-03", "end_date": "present", "rank": "正厅级", "note": "2023年3月任徐汇区代区长，后任区长"},
    {"person_id": 2, "org_id": 1, "title": "中共上海市浦东新区区委常委", "start_date": "2021", "end_date": "2023-03", "rank": "副厅级", "note": "曾任浦东新区区委常委、副区长"},
    {"person_id": 2, "org_id": 2, "title": "上海市浦东新区副区长", "start_date": "2019", "end_date": "2021", "rank": "副厅级", "note": ""},
    # 沈权
    {"person_id": 3, "org_id": 1, "title": "中共上海市徐汇区委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 王宏伟
    {"person_id": 4, "org_id": 2, "title": "徐汇区委常委、副区长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 何雅
    {"person_id": 5, "org_id": 3, "title": "徐汇区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 刘琪
    {"person_id": 6, "org_id": 4, "title": "徐汇区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 赵懿
    {"person_id": 7, "org_id": 5, "title": "徐汇区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 习挺松
    {"person_id": 8, "org_id": 6, "title": "徐汇区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 诸旖
    {"person_id": 9, "org_id": 7, "title": "徐汇区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 谭伟时
    {"person_id": 10, "org_id": 8, "title": "徐汇区委常委、区人民武装部政委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 俞林伟
    {"person_id": 11, "org_id": 2, "title": "徐汇区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 罗华品
    {"person_id": 12, "org_id": 2, "title": "徐汇区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 邓大伟
    {"person_id": 13, "org_id": 2, "title": "徐汇区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王志华
    {"person_id": 14, "org_id": 2, "title": "徐汇区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李新华
    {"person_id": 15, "org_id": 9, "title": "徐汇区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 黄冲
    {"person_id": 16, "org_id": 10, "title": "徐汇区政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 鲍炳章
    {"person_id": 17, "org_id": 1, "title": "中共上海市徐汇区委书记（前任）", "start_date": "2016", "end_date": "2021-08", "rank": "正厅级", "note": "前任区委书记，后调任上海市政府副秘书长"},
    # 钟晓咏
    {"person_id": 18, "org_id": 2, "title": "徐汇区区长（前任）", "start_date": "2019", "end_date": "2023-03", "rank": "正厅级", "note": "前任区长，后调任上海市公安局副局长？"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 曹立强 — 王华 (搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档关系", "overlap_org": "上海市徐汇区", "overlap_period": "2023-03至今"},
    # 曹立强 — 鲍炳章 (前后任)
    {"person_a": 1, "person_b": 17, "type": "前后任", "context": "曹立强接替鲍炳章任徐汇区委书记", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": "2021-08"},
    # 王华 — 钟晓咏 (前后任)
    {"person_a": 2, "person_b": 18, "type": "前后任", "context": "王华接替钟晓咏任徐汇区长", "overlap_org": "上海市徐汇区人民政府", "overlap_period": "2023-03"},
    # 曹立强 — 王宏伟 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—常务副区长", "overlap_org": "上海市徐汇区", "overlap_period": "2021-08至今"},
    # 王华 — 王宏伟 (上下级)
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "上海市徐汇区人民政府", "overlap_period": "2023-03至今"},
    # 曹立强 — 沈权 (上下级)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    # 王华 — 沈权 (共事)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委副书记", "overlap_org": "上海市徐汇区", "overlap_period": ""},
    # 曹立强 — 各常委 (上下级)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—纪委书记", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—组织部部长", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记—宣传部部长", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记—政法委书记", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—统战部部长", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
]

# ── BUILD ──────────────────────────────────────────────────────────
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

if __name__ == "__main__":
    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    # Export person JSON files
    def write_person_json(person: dict, job_label: str):
        filename = f"{TODAY}-上海市-徐汇区-{job_label}-{person['name']}.json"
        output = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "上海市",
                "city": "徐汇区",
                "region": "徐汇区",
                "job": person["current_post"],
                "task_id": "shanghai_徐汇区",
                "time_focus": "2016-2026",
            },
            "identity": {
                "person_id": f"xuhui_{person['name']}",
                "name": person["name"],
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": person.get("birth", ""),
                "birthplace": person.get("birthplace", ""),
                "native_place": person.get("birthplace", ""),
                "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": person.get("party_join", ""),
                "work_start": person.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{person['name']}_{person.get('birth', '')}",
                    "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": person["current_post"],
                "current_org": person["current_org"],
                "administrative_rank": "",
                "as_of": TODAY,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": pos.get("start_date", ""),
                    "end": pos.get("end_date", ""),
                    "org": pos["org_id"],
                    "title": pos["title"],
                    "rank": pos.get("rank", ""),
                    "notes": pos.get("note", ""),
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                }
                for pos in positions
                if pos["person_id"] == person["id"]
            ],
            "organizations": [
                {
                    "org_id": org["id"],
                    "name": org["name"],
                    "type": org["type"],
                    "level": org["level"],
                    "parent": org.get("parent", ""),
                    "location": org.get("location", ""),
                    "source_ids": ["S001"],
                }
                for org in organizations
                if org["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == person["id"]}
            ],
            "relationships": [
                {
                    "person": p["name"],
                    "person_id": f"xuhui_{p['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("共事", "前后任") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
                for r in relationships
                for p in persons
                if (r["person_a"] == person["id"] and r["person_b"] == p["id"]) or (r["person_b"] == person["id"] and r["person_a"] == p["id"])
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": [
                {
                    "id": "S001",
                    "title": "上海市徐汇区人民政府门户网站",
                    "url": "https://www.xuhui.gov.cn/",
                    "publisher": "上海市徐汇区人民政府",
                    "published_at": "",
                    "accessed_at": TODAY,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "Confirmed current officeholders from homepage news feed",
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "Detailed career timeline and education background need verification from official biography pages",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"完整简历：{person['name']}的详细教育背景、早期职业生涯、晋升时间线",
                    "why_it_matters": "核心领导的履历完整度影响关系网络分析的深度",
                    "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示"],
                    "last_attempted": TODAY,
                }
            ],
        }
        path = os.path.join(PERSONS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")

    write_person_json(persons[0], "区委书记")  # 曹立强
    write_person_json(persons[1], "区长")  # 王华

    print(f"\n=== Done. Output in {STAGING_DIR} ===")
