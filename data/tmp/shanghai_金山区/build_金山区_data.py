#!/usr/bin/env python3
"""金山区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区(直辖市)
调查日期: 2026-07-25
信息来源:
  - 上海市金山区人民政府网站 (www.jinshan.gov.cn)
  - 金山区融媒体中心官方报道
"""

from __future__ import annotations

import json
import sys
import os
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).resolve().parent

# Find project root
PROJECT_ROOT = HERE
for _ in range(10):
    if (PROJECT_ROOT / "gov_relation").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    PROJECT_ROOT = HERE.parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import sqlite3  # noqa: used by gov_relation.runner internally
from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "金山区"
TODAY = "2026-07-25"

STAGING = HERE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# Canonical destinations
CANONICAL_DB = PROJECT_ROOT / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = PROJECT_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = PROJECT_ROOT / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_ROOT_BUILD = PROJECT_ROOT / f"build_{SLUG}_data.py"

# ── Research Data Summary ──────────────────────────────────────────────────────
# 区委书记: 袁罡 (confirmed from government news, July 2026)
# 区委副书记、代理区长: 杨元飞 (confirmed from government news, July 2026)
# 前任区委书记: 刘健 (as of Jan 2026 interview; replaced by 袁罡 in early-mid 2026)
# 区人大常委会主任: 王宏伟 (former区委常委、副区长)
# 区委常委、统战部部长: 张恂
# 其他区委常委(从官方报道中确认): 刘豫峰、俞旻骁、吉维、陈卫国、柴亚华、姜伟良、张斌
# 副区长: 罗明陨
# 区法院院长: 余剑
# 区检察院检察长: 张征
# 区人大常委会副主任: 蒋雅红、潘军、陈莽、柴亚华、余雷
# 区领导: 郭建利、王明法

# ── Persons ──────────────────────────────────────────────────────────────────
# ID ranges: 1xxx = party, 2xxx = government, 3xxx = congress,
#            4xxx = cppcc, 5xxx = judiciary

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 区委领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 袁罡 — 区委书记
    {
        "id": 1001,
        "name": "袁罡",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委书记",
        "current_org": "中共上海市金山区委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877972.html",
    },
    # 2. 杨元飞 — 区委副书记、代理区长
    {
        "id": 1002,
        "name": "杨元飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委副书记、代理区长",
        "current_org": "上海市金山区人民政府",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877971.html",
    },
    # 3. 刘豫峰 — 区委常委
    {
        "id": 1003,
        "name": "刘豫峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委",
        "current_org": "中共上海市金山区委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # 4. 张恂 — 区委常委、统战部部长
    {
        "id": 1004,
        "name": "张恂",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委、统战部部长",
        "current_org": "中共上海市金山区委员会统战部",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260723/877960.html",
    },
    # 5. 俞旻骁 — 区委常委
    {
        "id": 1005,
        "name": "俞旻骁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委",
        "current_org": "中共上海市金山区委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # 6. 吉维 — 区委常委
    {
        "id": 1006,
        "name": "吉维",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委",
        "current_org": "中共上海市金山区委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # 7. 陈卫国 — 区委常委
    {
        "id": 1007,
        "name": "陈卫国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委",
        "current_org": "中共上海市金山区委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # 8. 柴亚华 — 区委常委、区人大常委会副主任
    {
        "id": 1008,
        "name": "柴亚华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委、区人大常委会副主任",
        "current_org": "金山区人民代表大会常务委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # 9. 姜伟良 — 区委常委
    {
        "id": 1009,
        "name": "姜伟良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委",
        "current_org": "中共上海市金山区委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # 10. 张斌 — 区委常委
    {
        "id": 1010,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区委常委",
        "current_org": "中共上海市金山区委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 区政府领导
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 罗明陨 — 副区长
    {
        "id": 2001,
        "name": "罗明陨",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区副区长",
        "current_org": "上海市金山区人民政府",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877968.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 区人大常委会
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 王宏伟 — 主任
    {
        "id": 3001,
        "name": "王宏伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人大常委会主任",
        "current_org": "金山区人民代表大会常务委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877968.html",
    },
    # 13. 蒋雅红 — 副主任
    {
        "id": 3002,
        "name": "蒋雅红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人大常委会副主任",
        "current_org": "金山区人民代表大会常务委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877968.html",
    },
    # 14. 潘军 — 副主任
    {
        "id": 3003,
        "name": "潘军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人大常委会副主任",
        "current_org": "金山区人民代表大会常务委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877968.html",
    },
    # 15. 陈莽 — 副主任
    {
        "id": 3004,
        "name": "陈莽",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人大常委会副主任",
        "current_org": "金山区人民代表大会常务委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877968.html",
    },
    # 16. 余雷 — 副主任
    {
        "id": 3005,
        "name": "余雷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人大常委会副主任",
        "current_org": "金山区人民代表大会常务委员会",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877968.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 区法院 & 区检察院
    # ═══════════════════════════════════════════════════════════════════════
    # 17. 余剑 — 法院院长
    {
        "id": 5001,
        "name": "余剑",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人民法院院长",
        "current_org": "上海市金山区人民法院",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # 18. 张征 — 检察院检察长
    {
        "id": 5002,
        "name": "张征",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人民检察院检察长",
        "current_org": "上海市金山区人民检察院",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877973.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 其他区领导
    # ═══════════════════════════════════════════════════════════════════════
    # 19. 郭建利
    {
        "id": 6001,
        "name": "郭建利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区领导",
        "current_org": "上海市金山区",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260724/877971.html",
    },
    # 20. 王明法
    {
        "id": 6002,
        "name": "王明法",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区领导",
        "current_org": "上海市金山区",
        "source": "https://www.jinshan.gov.cn/ywdt-zhxx/20260703/877670.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 前任领导
    # ═══════════════════════════════════════════════════════════════════════
    # 21. 刘健 — 前任区委书记 (until early 2026)
    {
        "id": 9001,
        "name": "刘健",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.jinshan.gov.cn/hd-zxft/20260123/875229.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共上海市金山区委员会",
        "type": "党委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市委员会",
        "location": "上海市金山区",
    },
    {
        "id": 2,
        "name": "上海市金山区人民政府",
        "type": "政府",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民政府",
        "location": "上海市金山区",
    },
    {
        "id": 3,
        "name": "金山区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民代表大会常务委员会",
        "location": "上海市金山区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议上海市金山区委员会",
        "type": "政协",
        "level": "市辖区(直辖市)",
        "parent": "中国人民政治协商会议上海市委员会",
        "location": "上海市金山区",
    },
    {
        "id": 5,
        "name": "中共上海市金山区纪律检查委员会",
        "type": "纪委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市纪律检查委员会",
        "location": "上海市金山区",
    },
    {
        "id": 6,
        "name": "上海市金山区人民法院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市高级人民法院",
        "location": "上海市金山区",
    },
    {
        "id": 7,
        "name": "上海市金山区人民检察院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民检察院",
        "location": "上海市金山区",
    },
    {
        "id": 8,
        "name": "中共上海市金山区委员会统战部",
        "type": "党委部门",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市金山区委员会",
        "location": "上海市金山区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Party Committee
    {"person_id": 1001, "org_id": 1, "title": "金山区委书记", "start_date": "", "end_date": "present", "rank": "正局级", "note": "2026年7月在任，接替刘健"},
    {"person_id": 1002, "org_id": 1, "title": "金山区委副书记", "start_date": "", "end_date": "present", "rank": "正局级", "note": "兼任代理区长"},
    {"person_id": 1002, "org_id": 2, "title": "金山区代理区长", "start_date": "", "end_date": "present", "rank": "正局级", "note": "区政府党组书记（代理）"},
    {"person_id": 1003, "org_id": 1, "title": "金山区委常委", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1004, "org_id": 8, "title": "金山区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1005, "org_id": 1, "title": "金山区委常委", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1006, "org_id": 1, "title": "金山区委常委", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1007, "org_id": 1, "title": "金山区委常委", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1008, "org_id": 3, "title": "金山区委常委、区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1009, "org_id": 1, "title": "金山区委常委", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1010, "org_id": 1, "title": "金山区委常委", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    # Government
    {"person_id": 2001, "org_id": 2, "title": "金山区副区长", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    # People's Congress
    {"person_id": 3001, "org_id": 3, "title": "金山区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正局级", "note": "党组书记"},
    {"person_id": 3002, "org_id": 3, "title": "金山区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 3003, "org_id": 3, "title": "金山区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 3004, "org_id": 3, "title": "金山区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 3005, "org_id": 3, "title": "金山区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1008, "org_id": 3, "title": "金山区人大常委会副主任（兼常委）", "start_date": "", "end_date": "present", "rank": "副局级", "note": "兼任区委常委"},
    # Judiciary
    {"person_id": 5001, "org_id": 6, "title": "金山区人民法院院长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组书记"},
    {"person_id": 5002, "org_id": 7, "title": "金山区人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组书记"},
    # Other leaders
    {"person_id": 6001, "org_id": 1, "title": "金山区领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 6002, "org_id": 1, "title": "金山区领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # Predecessors
    {"person_id": 9001, "org_id": 1, "title": "金山区委书记（前任）", "start_date": "", "end_date": "2026", "rank": "正局级", "note": "至2026年初，由袁罡接任"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # Top leadership partnership
    {"person_a": 1001, "person_b": 1002, "type": "superior_subordinate", "context": "区委书记—代理区长搭班子", "overlap_org": "金山区", "overlap_period": "2026-present"},
    {"person_a": 1001, "person_b": 1003, "type": "colleague", "context": "区委书记—区委常委", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1004, "type": "colleague", "context": "区委书记—统战部长", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1005, "type": "colleague", "context": "区委书记—区委常委", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1006, "type": "colleague", "context": "区委书记—区委常委", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1007, "type": "colleague", "context": "区委书记—区委常委", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1008, "type": "colleague", "context": "区委书记—区委常委/人大副主任", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1009, "type": "colleague", "context": "区委书记—区委常委", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1010, "type": "colleague", "context": "区委书记—区委常委", "overlap_org": "区委常委会", "overlap_period": "present"},
    # Predecessor succession
    {"person_a": 1001, "person_b": 9001, "type": "predecessor_successor", "context": "袁罡接替刘健任金山区委书记", "overlap_org": "中共上海市金山区委员会", "overlap_period": "2026"},
    # Government team
    {"person_a": 1002, "person_b": 2001, "type": "superior_subordinate", "context": "代理区长—副区长", "overlap_org": "区政府", "overlap_period": "present"},
    # Congress leadership
    {"person_a": 3001, "person_b": 3002, "type": "colleague", "context": "人大主任—副主任", "overlap_org": "区人大常委会", "overlap_period": "present"},
    {"person_a": 3001, "person_b": 3003, "type": "colleague", "context": "人大主任—副主任", "overlap_org": "区人大常委会", "overlap_period": "present"},
    {"person_a": 3001, "person_b": 3004, "type": "colleague", "context": "人大主任—副主任", "overlap_org": "区人大常委会", "overlap_period": "present"},
    {"person_a": 3001, "person_b": 3005, "type": "colleague", "context": "人大主任—副主任", "overlap_org": "区人大常委会", "overlap_period": "present"},
    {"person_a": 3001, "person_b": 1008, "type": "colleague", "context": "人大主任—副主任（兼常委）", "overlap_org": "区人大常委会", "overlap_period": "present"},
]


def write_person_json(person: dict, job_label: str):
    """Write a detailed per-person graph JSON file to staging."""
    filename = f"{TODAY.replace('-', '')}-上海市-金山区-{job_label}-{person['name']}.json"
    person_id_slug = f"jinshan_{person['name']}"
    
    # Build career timeline from positions
    career = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for org in organizations:
                if org["id"] == pos["org_id"]:
                    org_name = org["name"]
                    break
            career.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": org_name,
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "上海市金山区",
                "system": "party" if pos["org_id"] < 2000 else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": False,
                "notes": pos.get("note", ""),
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })
    
    # Build relationships
    rels = []
    for r in relationships:
        related_person_id = None
        related_name = None
        if r["person_a"] == person["id"]:
            related_person_id = r["person_b"]
        elif r["person_b"] == person["id"]:
            related_person_id = r["person_a"]
        if related_person_id:
            for p in persons:
                if p["id"] == related_person_id:
                    related_name = p["name"]
                    break
            if related_name:
                rels.append({
                    "person": related_name,
                    "person_id": f"jinshan_{related_name}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("superior_subordinate", "predecessor_successor") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                })
    
    output = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "上海市",
            "city": "上海市",
            "region": "金山区",
            "job": person["current_post"],
            "task_id": "shanghai_金山区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": person_id_slug,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正局级" if person["id"] in (1001, 1002, 3001) else "副局级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career,
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
        "relationships": rels,
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
                "title": "上海市金山区人民政府门户网站 - 领导活动报道",
                "url": "https://www.jinshan.gov.cn/",
                "publisher": "上海市金山区人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "Confirmed current officeholders from news articles (2026年7月)",
            },
            {
                "id": "S002",
                "title": "金山区委书记访谈 - 对话区委书记",
                "url": "https://www.jinshan.gov.cn/hd-zxft/20260123/875229.html",
                "publisher": "上海市金山区人民政府",
                "published_at": "2026-01-23",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "前任区委书记刘健出席, 2026年1月在任",
            },
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"完整履历：{person['name']}的详细教育背景、出生年月、籍贯、早期职业生涯和晋升时间线均需进一步核实",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"完整简历：{person['name']}的详细教育背景、出生年月、籍贯、早期职业履历",
                "why_it_matters": "核心领导的履历完整度影响关系网络分析的深度",
                "suggested_queries": [f"{person['name']} 简历 金山区", f"{person['name']} 任前公示", f"{person['name']} 百度百科"],
                "last_attempted": TODAY,
            }
        ],
    }
    path = STAGING / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filename}")


def main() -> None:
    print(f"\n{'='*60}")
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区(直辖市)")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 金山区人民政府网站 (jinshan.gov.cn)")
    print(f"{'='*60}")

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

    # Generate per-person graph JSON for core leaders
    write_person_json(persons[0], "区委书记")  # 袁罡
    write_person_json(persons[1], "代理区长")  # 杨元飞

    # Copy to canonical destinations
    for dst in [CANONICAL_DB, CANONICAL_GEXF]:
        if dst.exists():
            dst.unlink()
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)

    print(f"\n{'='*60}")
    print(f"  金山区 数据构建完成")
    print(f"  DB:   {DB_PATH} -> {CANONICAL_DB}")
    print(f"  GEXF: {GEXF_PATH} -> {CANONICAL_GEXF}")
    print(f"  Persons:     {len(persons)}")
    print(f"  Orgs:        {len(organizations)}")
    print(f"  Positions:   {len(positions)}")
    print(f"  Relations:   {len(relationships)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
