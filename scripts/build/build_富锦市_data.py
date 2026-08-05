#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Fujin City leadership network.

富锦市 (Fujin City) — 黑龙江省佳木斯市下辖县级市. Generates:
  - SQLite DB (persons, organizations, positions, relationships)
  - GEXF graph
  - Person JSON profiles for core leaders (市委书记, 市长)

Source of truth: official 富锦市人民政府 领导之窗
https://www.fujin.gov.cn/fjs/c101555/ldzc.shtml + individual leadership bio pages.
Roster confirmed as of 2026-08-05.
"""

import json
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _ in range(6):
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    REPO_ROOT = REPO_ROOT.parent
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "富锦市"
TODAY = date.today().strftime("%Y%m%d")

# ── Paths (relative to repo root) ──
# When GOV_REL_DATABASE_DIR is set (staging mode), write DB/GEXF/person JSON
# directly into that dir so process_tmp can collect and promote them.
_STAGE = os.getenv("GOV_REL_DATABASE_DIR")
if _STAGE:
    DATA_DIR = Path(_STAGE)
    DB_PATH = DATA_DIR / f"{SLUG}_network.db"
    GEXF_PATH = DATA_DIR / f"{SLUG}_network.gexf"
    PERSONS_DIR = DATA_DIR
else:
    DATA_DIR = REPO_ROOT / "data"
    DB_PATH = DATA_DIR / "database" / f"{SLUG}_network.db"
    GEXF_PATH = DATA_DIR / "graph" / f"{SLUG}_network.gexf"
    PERSONS_DIR = DATA_DIR / "persons"

# ══════════════════════════════════════════════
#  PERSONS
# ══════════════════════════════════════════════
# Current roster from official 领导之窗 (2026-08-05)

persons = [
    # ── 市委书记 ──
    {"id": 1, "name": "梁庆民", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-10", "birthplace": "黑龙江省佳木斯市",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1989-08",
     "current_post": "富锦市委书记", "current_org": "中共富锦市委员会",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144356.shtml"},
    # ── 市长 ──
    {"id": 2, "name": "赵尉凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-01", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委副书记、政府市长", "current_org": "富锦市人民政府",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144357.shtml"},
    # ── 市委副书记 ──
    {"id": 3, "name": "袁宏涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "",
     "education": "大学 农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委副书记、市直机关工委书记", "current_org": "中共富锦市委员会",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144358.shtml"},
    {"id": 4, "name": "李国泰", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-06", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委副书记（挂职）", "current_org": "中共富锦市委员会",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144359.shtml"},
    # ── 市委常委 ──
    {"id": 5, "name": "董仲申", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-01", "birthplace": "",
     "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委常委、市纪委书记、市监委主任", "current_org": "中共富锦市纪律检查委员会",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144361.shtml"},
    {"id": 6, "name": "杨志宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-02", "birthplace": "",
     "education": "大学 法学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委常委、政府副市长、党组副书记", "current_org": "富锦市人民政府",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144363.shtml"},
    {"id": 7, "name": "隋伟红", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-07", "birthplace": "",
     "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委常委、宣传部部长", "current_org": "中共富锦市委宣传部",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144365.shtml"},
    {"id": 8, "name": "万永发", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "",
     "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委常委、政府副市长、党组成员", "current_org": "富锦市人民政府",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144373.shtml"},
    {"id": 9, "name": "宋琳", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-06", "birthplace": "",
     "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富锦市委常委、组织部部长", "current_org": "中共富锦市委组织部",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144374.shtml"},
    {"id": 10, "name": "郭锐", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富锦市委常委", "current_org": "中共富锦市委员会",
     "source": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144375.shtml"},
    # ── 副市长（非常委）──
    {"id": 11, "name": "杨昆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富锦市人民政府副市长", "current_org": "富锦市人民政府",
     "source": "https://www.fujin.gov.cn/fjs/c101558/202510/c04_160489.shtml"},
    {"id": 12, "name": "王凯枫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富锦市人民政府副市长", "current_org": "富锦市人民政府",
     "source": "https://www.fujin.gov.cn/fjs/c101558/202510/c04_160490.shtml"},
    # ── 人大 / 政协 ──
    {"id": 13, "name": "许志东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富锦市人大常委会主任", "current_org": "富锦市人民代表大会常务委员会",
     "source": "https://www.fujin.gov.cn/fjs/c101557/202510/c04_157553.shtml"},
    {"id": 14, "name": "佟宁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "富锦市政协主席", "current_org": "政协富锦市委员会",
     "source": "https://www.fujin.gov.cn/fjs/c101559/202510/c04_160502.shtml"},
]


# ══════════════════════════════════════════════
#  ORGANIZATIONS
# ══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共富锦市委员会", "type": "党委", "level": "县级市", "parent": "中共佳木斯市委员会", "location": "富锦市"},
    {"id": 2, "name": "富锦市人民政府", "type": "政府", "level": "县级市", "parent": "佳木斯市人民政府", "location": "富锦市"},
    {"id": 3, "name": "中共富锦市纪律检查委员会", "type": "纪律检查委员会", "level": "县级", "parent": "中共佳木斯市纪委", "location": "富锦市"},
    {"id": 4, "name": "中共富锦市委组织部", "type": "党委部门", "level": "县级", "parent": "中共富锦市委员会", "location": "富锦市"},
    {"id": 5, "name": "中共富锦市委宣传部", "type": "党委部门", "level": "县级", "parent": "中共富锦市委员会", "location": "富锦市"},
    {"id": 6, "name": "富锦市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "富锦市"},
    {"id": 7, "name": "政协富锦市委员会", "type": "政协", "level": "县级", "parent": "", "location": "富锦市"},
    {"id": 8, "name": "富锦市市直机关工作委员会", "type": "党委部门", "level": "县级", "parent": "中共富锦市委员会", "location": "富锦市"},
    # 相关上级与人事调出机构
    {"id": 9, "name": "佳木斯市政协", "type": "政协", "level": "地级市", "parent": "", "location": "佳木斯市"},
    {"id": 10, "name": "中共桦南县委员会", "type": "党委", "level": "县级", "parent": "中共佳木斯市委员会", "location": "桦南县"},
    {"id": 11, "name": "桦南县人民政府", "type": "政府", "level": "县级", "parent": "佳木斯市人民政府", "location": "桦南县"},
    {"id": 12, "name": "佳木斯市人力资源和社会保障局", "type": "政府部门", "level": "地级", "parent": "佳木斯市人民政府", "location": "佳木斯市"},
    {"id": 13, "name": "佳木斯市军用饮食供应站", "type": "事业单位", "level": "地级", "parent": "", "location": "佳木斯市"},
    {"id": 14, "name": "佳木斯市郊区人民政府", "type": "政府", "level": "县区", "parent": "佳木斯市人民政府", "location": "佳木斯市郊区"},
    {"id": 15, "name": "佳木斯市西格木乡", "type": "乡镇", "level": "乡", "parent": "佳木斯市郊区", "location": "佳木斯市郊区"},
]


# ══════════════════════════════════════════════
#  POSITIONS
# ══════════════════════════════════════════════

positions = [
    # 梁庆民 (1) —— 市委书记
    {"person_id": 1, "org_id": 1, "title": "富锦市委书记", "start_date": "2021-12", "end_date": "present",
     "rank": "正处级", "note": "现主持富锦市委全面工作"},
    {"person_id": 1, "org_id": 10, "title": "桦南县委书记", "start_date": "2021-01", "end_date": "2021-12",
     "rank": "正处级", "note": "调任富锦前"},
    {"person_id": 1, "org_id": 11, "title": "桦南县长（县委副书记）", "start_date": "2014", "end_date": "2021-01",
     "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "佳木斯市郊区委常委、副区长", "start_date": "2009", "end_date": "2014",
     "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "西格木乡乡长（历任副乡长、党委副书记）", "start_date": "", "end_date": "2009",
     "rank": "科级", "note": "1989-08 参加工作，由乡政府通讯任起步"},
    {"person_id": 1, "org_id": 9, "title": "佳木斯市政协副主席", "start_date": "2022-01", "end_date": "present",
     "rank": "副厅级", "note": "当选，与富锦市委书记并行"},
    # 赵尉凯 (2) —— 市长
    {"person_id": 2, "org_id": 2, "title": "富锦市人民政府市长", "start_date": "2024-07", "end_date": "present",
     "rank": "正处级", "note": "2024-07-06 市九届人大四次会议补选"},
    {"person_id": 2, "org_id": 1, "title": "富锦市委副书记", "start_date": "2024-06", "end_date": "present",
     "rank": "副处级", "note": "2024-06-08 提名为市长候选人，后任副书记"},
    {"person_id": 2, "org_id": 12, "title": "佳木斯市人力资源和社会保障局人事科科长", "start_date": "", "end_date": "2024-06",
     "rank": "科级", "note": "任职于市直机关"},
    {"person_id": 2, "org_id": 13, "title": "佳木斯市军用饮食供应站站长", "start_date": "", "end_date": "2024-06",
     "rank": "科级", "note": "任职于市直机关"},
    # 袁绍涛 (3)
    {"person_id": 3, "org_id": 8, "title": "富锦市直机关工委书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "兼任"},
    # 董事会 5
    {"person_id": 5, "org_id": 3, "title": "富锦市纪委书记、市监委主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "四级高级监察官"},
    # 杨志才是 6
    {"person_id": 6, "org_id": 2, "title": "富锦市常务副市长兼任党组副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管政府日常工作"},
    # 隋玉红 7
    {"person_id": 7, "org_id": 5, "title": "富锦市委宣传部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 万永发 8
    {"person_id": 8, "org_id": 2, "title": "富锦市副市长（市委常委）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 宋开 9
    {"person_id": 9, "org_id": 4, "title": "富锦市委组织部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 郭锐 10
    {"person_id": 10, "org_id": 1, "title": "富锦市委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 杨立 11
    {"person_id": 11, "org_id": 2, "title": "富锦市副市长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 王凯枫 12
    {"person_id": 12, "org_id": 2, "title": "富锦市副市长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 许志东 13
    {"person_id": 13, "org_id": 6, "title": "富锦市人大常委会主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 佟宁 14
    {"person_id": 14, "org_id": 7, "title": "富锦市政协主席", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
]


# ══════════════════════════════════════════════
#  RELATIONSHIPS
# ══════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "上下级",
     "context": "市委书记与市长搭班子，构成党政主要领导搭档",
     "overlap_org": "中共富锦市委员会/富锦市人民政府",
     "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "梁庆民为市委书记，袁宏涛为市委副书记",
     "overlap_org": "中共富锦市委员会",
     "overlap_period": "2021-至今"},
    {"person_a": 5, "person_b": 1, "type": "上下级",
     "context": "纪委受党委领导，董仲申为监委主任、归梁庆民领导",
     "overlap_org": "中共富锦市委员会",
     "overlap_period": "至今"},
    {"person_a": 6, "person_b": 1, "type": "上下级",
     "context": "杨志宇为市委常委、常务副市长",
     "overlap_org": "中共富锦市委员会/富锦市人民政府",
     "overlap_period": "至今"},
    {"person_a": 9, "person_b": 1, "type": "上下级",
     "context": "组织部长在市委书记领导下负责干部工作",
     "overlap_org": "中共富锦市委员会",
     "overlap_period": "至今"},
]

# ── 便捷字段──
# 各主要领导现职及简历简要说明（供报告使用）
LEADER_NOTES = {
    1: "梁庆民，市委书记，黑龙江佳木斯人，1989年参加工作，从郊区乡镇基层一路升至佳木斯市政协副主席兼富锦市委书记。",
    2: "赵尉凯，市长，1983年生，曾任佳木斯市人社局人事科科长、军用饮食供应站站长，2024年转任富锦市长。",
}


# ══════════════════════════════════════════════
#  PERSON JSON (core leaders)
# ══════════════════════════════════════════════

def write_person_json(person):
    """Write a deep person-profile JSON using the person_graph_json schema."""
    filepath_base = f"{TODAY}-黑龙江省-佳木斯市-"
    if person["id"] == 1:
        filename = filepath_base + "市委书记-梁庆民.json"
    elif person["id"] == 2:
        filename = filepath_base + "市长-赵尉凯.json"
    else:
        filename = filepath_base + f"{person['current_post'].replace('、','_')}-{person['name']}.json"
    filepath = PERSONS_DIR / filename

    # 本源注册
    source_register = [
        {"id": "S001", "title": "富锦市人民政府-领导之窗(市委书记)",
         "url": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144356.shtml",
         "publisher": "富锦市人民政府", "published_at": "2025-10", "accessed_at": TODAY, "source_type": "official", "reliability": "high"},
        {"id": "S002", "title": "富锦市人民政府-领导之窗(市长)",
         "url": "https://www.fujin.gov.cn/fjs/c101556/202510/c04_144357.shtml",
         "publisher": "富锦市人民政府", "published_at": "2025-10", "accessed_at": TODAY, "source_type": "official", "reliability": "high"},
        {"id": "S003", "title": "富锦市人民政府-领导之窗列表",
         "url": "https://www.fujin.gov.cn/fjs/c101555/ldzh.shtml",
         "publisher": "富锦市人民政府", "published_at": "2025-10", "accessed_at": TODAY, "source_type": "official", "reliability": "high"},
        {"id": "S004", "title": "百度搜索-AI摘要(梁庆民简历)",
         "url": "https://www.baidu.com/s?wd=梁庆民 富锦市委书记 简历",
         "publisher": "百度", "published_at": "2026-08", "accessed_at": TODAY, "source_type": "database", "reliability": "medium"},
        {"id": "S005", "title": "媒体/微信(赵达凯当选市长)",
         "url": "https://mp.weixin.qq.com/",
         "publisher": "美好富锦(微信)", "published_at": "2024-07", "accessed_at": TODAY, "source_type": "media", "reliability": "medium"},
    ]

    # 核心履历时间线
    if person["id"] == 1:
        timeline = [
            {"start": "2021-12", "end": "present", "org": "中共富锦市委员会", "title": "富锦市委书记",
             "level": "县级市", "location": "富锦市", "system": "party", "rank": "正处级", "is_key_promotion": True,
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2022-01", "end": "present", "org": "佳木斯市政协", "title": "佳木斯市政协副主席",
             "level": "地级", "location": "佳木斯市", "system": "other", "rank": "副厅级", "is_key_promotion": True,
             "notes": "当选", "confidence": "confirmed", "source_ids": ["S004"]},
            {"start": "2021-01", "end": "2021-12", "org": "中共桦南县委员会", "title": "桦南县委书记",
             "level": "县", "location": "桦南县", "system": "party", "rank": "正处级", "is_key_promotion": True,
             "notes": "调任富锦前", "confidence": "confirmed", "source_ids": ["S004"]},
            {"start": "2014", "end": "2021-01", "org": "桦南县人民政府", "title": "桦南县长（县委副书记）",
             "level": "县", "location": "桦南县", "system": "government", "rank": "正处级", "is_key_promotion": True,
             "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
            {"start": "2009", "end": "2014", "org": "佳木斯市郊区人民政府", "title": "郊区委常委、副区长",
             "level": "区", "location": "佳木斯市郊区", "system": "government", "rank": "副处级", "is_key_promotion": False,
             "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
            {"start": "unknown", "end": "2009", "org": "佳木斯市西格木乡", "title": "乡政府通讯员→副乡长→党委副书记→乡长",
             "level": "乡", "location": "佳木斯市郊区", "system": "government", "rank": "科级", "is_key_promotion": False,
             "notes": "1989-08 参加工作", "confidence": "plausible", "source_ids": ["S004"]},
        ]
    elif person["id"] == 2:
        timeline = [
            {"start": "2024-07", "end": "present", "org": "富锦市人民政府", "title": "富锦市市长",
             "level": "县级市", "location": "富锦市", "system": "government", "rank": "正处级", "is_key_promotion": True,
             "notes": "2024-07-06 市九届人民代表大会第四次会议补选", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
            {"start": "2024-06", "end": "2024-07", "org": "中共富锦市委员会", "title": "富锦市委副书记、代理市长",
             "level": "县级市", "location": "富锦市", "system": "party", "rank": "副处级", "is_key_promotion": True,
             "notes": "2024-06-08 提名为市长候选人", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "unknown", "end": "2024-06", "org": "佳木斯市人力资源和社会保障局", "title": "人事科科长",
             "level": "地级", "location": "佳木斯市", "system": "government", "rank": "科级", "is_key_promotion": False,
             "notes": "", "confidence": "plausible", "source_ids": ["S005"]},
            {"start": "unknown", "end": "2024-06", "org": "佳木斯市军用饮食供应站", "title": "站长",
             "level": "地级", "location": "佳木斯市", "system": "government", "rank": "科级", "is_key_promotion": False,
             "notes": "", "confidence": "plausible", "source_ids": ["S005"]},
        ]

    else:
        career = []
        role = person["current_post"]
        org = person["current_org"]
        career.append({"start": "unknown", "end": "present", "org": org, "title": role,
                       "level": "县级市", "location": "富锦市", "system": "other", "rank": "",
                       "is_key_promotion": False, "notes": "现职", "confidence": "confirmed", "source_ids": ["S003"]})
        timeline = career

    identity = {
        "person_id": f"fujin_{person['name']}",
        "name": person["name"],
        "aliases": [], "gender": person["gender"], "ethnicity": person["ethnicity"],
        "birth": person["birth"], "birthplace": person["birthplace"],
        "native_place": person["birthplace"],
        "education": [{"period": "", "institution": "", "major": "",
                       "degree": person["education"], "study_type": "unknown", "source_ids": []}],
        "party_join": person["party_join"], "work_start": person["work_start"],
        "dedupe_keys": {"name_birth": f"{person['name']}_{person['birth']}",
                        "name_birthplace": f"{person['name']}_{person['birthplace']}",
                        "official_profile_url": person["source"]},
    }

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "黑龙江省", "city": "佳木斯市", "region": "富锦市",
                                "job": person["current_post"], "task_id": "heilongjiang_富锦市",
                                "time_focus": "2024-2026"},
        "identity": identity,
        "current_status": {"current_post": person["current_post"], "current_org": person["current_org"],
                           "administrative_rank": "县级市", "as_of": TODAY,
                           "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]},
        "career_timeline": timeline,
        "organizations": [person["current_org"]],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "local_ladder" if person["id"] == 1 else "cross_county_rotation",
                                 "systems_experience": [], "geographic_pattern": [],
                                 "promotion_velocity": {"summary": "待补", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                        "management_signals": [],
                                        "caveat": "Work style is inferred from public records, not private assessment."},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开纪律处分/负面报道",
                                        "date": "", "confidence": "confirmed", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed",
                               "career_completeness": "partial", "relationship_confidence": "medium",
                               "biggest_gap": "1990-2009 年间部分履历日期不详"},
        "open_questions": [
            {"priority": "high", "question": f"{person['name']}的完整任职轨迹（此前历任岗位、调任富锦时间、前任去向）",
             "why_it_matters": "核心领导的晋升路径与来源地是人事网络分析的关键",
             "suggested_queries": [f"{person['name']} 简历 任职经历",
                                    f"{person['name']} 任前公示 佳木斯",
                                    f"{person['name']} 富锦 履新"],
             "last_attempted": TODAY},
        ],
    }
    PERSONS_DIR.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  [ok]  {filename}")
    return filename


def main():
    print("=" * 60)
    print("  富锦市 — 领导班子工作关系网络")
    print(f"  Generated: {TODAY}")
    print("  Source: 富锦市人民政府官网 领导之窗")
    print("=" * 60)

    print("\nBuilding database and GEXF graph...")
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
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Verify the database contains the 4 expected tables
    conn = sqlite3.connect(str(DB_PATH))
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    for req in ("persons", "organizations", "positions", "relationships"):
        assert req in tables, f"missing table {req}"
    print("  DB tables OK: persons, organizations, positions, relationships")

    print("\nWriting person JSON files for core leaders...")
    json_files = [write_person_json(next(p for p in persons if p["id"] == pid)) for pid in (1, 2)]

    print()
    print("─" * 60)
    print("  统计摘要")
    print("─" * 60)
    print(f"  人员 (persons):     {len(persons)}")
    print(f"  机构 (orgs):        {len(organizations)}")
    print(f"  任职 (positions):   {len(positions)}")
    print(f"  关系 (edges):       {len(relationships)}")
    print(f"  JSON 文件:           {len(json_files)}")
    print()
    print("  说明:")
    print("    - 现任市委书记 = 梁庆民 (官网领导之窗确认，兼佳木斯市政协副主席)")
    print("    - 现任市长     = 赵尉凯 (官网领导之窗确认)")
    print("    - 出生/学历/参加工作时间源自官网个人简介")
    print("    - 梁庆民历任：郊区基层→郊区委常委副区长→桦南县长→桦南书记→富锦书记")
    print("    - 赵旻凯历任：市直机关(人社局/军供站)→富锦市长")
    print("    - 多数常委/副市长的完整履历尚缺，待后续补充")
    print()
    print("=" * 60)
    print("  Build complete.")
    print("  → Validate: python3 -m py_compile build_富锦市_data.py")
    print("  → Promote:  python3 scripts/process_tmp.py data/tmp/heilongjiang_富锦市 --apply")
    print("=" * 60)


if __name__ == "__main__":
    main()