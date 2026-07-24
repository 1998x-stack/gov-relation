#!/usr/bin/env python3
"""Build 哈尔滨市道里区 (Daoli District, Harbin, Heilongjiang) leadership network data.

Level: 市辖区
Province: 黑龙江省
Parent city: 哈尔滨市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: heilongjiang_道里区

Research date: 2026-07-24
Official source: http://www.hrbdl.gov.cn/ (哈尔滨市道里区人民政府)

Current status (as of 2026-07-24):
- 区委书记/区长: 于军 — 党政一肩挑（区委书记、区政府区长、人武部党委第一书记）
  7月22日以区委书记、区长身份出席区委"军事日"活动；
  官方简历：1970年11月出生，1993年8月参加工作，中共党员，研究生，管理学学士
- 区委副书记: 杜文曦
- 常务副区长: 王军（负责区政府常务工作、财政、应急、人社）
- 副区长: 王郑新（住建、城管、城市更新）
- 副区长: 王阳（教育、卫生、民政、退役军人）
- 副区长: 玄立三（农业农村、交通、环保、开发区）
- 副区长: 邢高波（公安、司法）
- 副区长: 闫格（招商引资、企业服务）

Key source pages:
- http://www.hrbdl.gov.cn/ (official homepage — lists leadership structure)
- http://www.hrbdl.gov.cn/hebdlq/yujun/ldy.shtml (于军 official bio)
- http://www.hrbdl.gov.cn/hebdlq/c75215/ldy.shtml (王军 official bio)
- http://www.hrbdl.gov.cn/hebdlq/c111863/ldy.shtml (王郑新 official bio)
- http://www.hrbdl.gov.cn/hebdlq/col37/ldy.shtml (王阳 official bio)
- http://www.hrbdl.gov.cn/hebdlq/xls/ldy.shtml (玄立三 official bio)
- http://www.hrbdl.gov.cn/hebdlq/c112310/ldy.shtml (邢高波 official bio)
- http://www.hrbdl.gov.cn/hebdlq/c112311/ldy.shtml (闫格 official bio)
- http://www.hrbdl.gov.cn/hebdlq/col24/202607/c01_1136994.shtml (军事日活动确认于军为书记+区长)
- http://www.hrbdl.gov.cn/hebdlq/col24/202607/c01_1134836.shtml (于军讲授专题党课)
- http://www.hrbdl.gov.cn/hebdlq/col24/list.shtml (道里要闻列表)
- http://www.hrbdl.gov.cn/hebdlq/col24/list_2.shtml (道里要闻列表第2页—确认杜文曦为副书记)
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "道里区"

_STAGING_DIR = _SCRIPT_DIR
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

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
        "name": "于军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生，管理学学士",
        "party_join": "中共党员",
        "work_start": "1993年8月",
        "current_post": "道里区委书记、区长、人武部党委第一书记",
        "current_org": "中共哈尔滨市道里区委员会",
        "source": "http://www.hrbdl.gov.cn/hebdlq/yujun/ldy.shtml (official bio) + http://www.hrbdl.gov.cn/hebdlq/col24/202607/c01_1136994.shtml (confirms dual role as Party Secretary and Mayor)",
    },
    {
        "id": 2,
        "name": "杜文曦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "道里区委副书记",
        "current_org": "中共哈尔滨市道里区委员会",
        "source": "http://www.hrbdl.gov.cn/hebdlq/col24/list_2.shtml (confirmed as 区委副书记 in article '区委副书记杜文曦带队深入外滩1898视听产业园开展专题调研')",
    },
    # ════════════════════════════════════════
    # 区政府领导 (Government)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王军",
        "gender": "男",
        "ethnicity": "",
        "birth": "1973年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大专",
        "party_join": "中共党员（2001年4月入党）",
        "work_start": "1998年8月",
        "current_post": "道里区委常委、常务副区长",
        "current_org": "哈尔滨市道里区人民政府",
        "source": "http://www.hrbdl.gov.cn/hebdlq/c75215/ldy.shtml (official bio — 负责区政府常务工作)",
    },
    {
        "id": 4,
        "name": "王郑新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年1月",
        "birthplace": "辽宁大连",
        "native_place": "辽宁大连",
        "education": "本科，工程硕士",
        "party_join": "中共党员（2001年6月入党）",
        "work_start": "1992年8月",
        "current_post": "道里区副区长",
        "current_org": "哈尔滨市道里区人民政府",
        "source": "http://www.hrbdl.gov.cn/hebdlq/c111863/ldy.shtml (official bio — 住建、城管、城市更新)",
    },
    {
        "id": 5,
        "name": "王阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "江苏丹阳",
        "native_place": "江苏丹阳",
        "education": "大学，黑龙江大学思想政治教育专业，法学学士",
        "party_join": "中共党员（1996年7月入党）",
        "work_start": "1998年7月",
        "current_post": "道里区副区长",
        "current_org": "哈尔滨市道里区人民政府",
        "source": "http://www.hrbdl.gov.cn/hebdlq/col37/ldy.shtml (official bio — 教育、卫生、民政、退役军人)",
    },
    {
        "id": 6,
        "name": "玄立三",
        "gender": "男",
        "ethnicity": "",
        "birth": "1979年3月",
        "birthplace": "",
        "native_place": "",
        "education": "本科，工学学士",
        "party_join": "中共党员（2005年10月入党）",
        "work_start": "2002年12月",
        "current_post": "道里区副区长",
        "current_org": "哈尔滨市道里区人民政府",
        "source": "http://www.hrbdl.gov.cn/hebdlq/xls/ldy.shtml (official bio — 农业农村、交通、环保、开发区)",
    },
    {
        "id": 7,
        "name": "邢高波",
        "gender": "男",
        "ethnicity": "",
        "birth": "1974年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大专",
        "party_join": "中共党员（1994年4月入党）",
        "work_start": "1994年11月",
        "current_post": "道里区副区长",
        "current_org": "哈尔滨市道里区人民政府",
        "source": "http://www.hrbdl.gov.cn/hebdlq/c112310/ldy.shtml (official bio — 公安、司法)",
    },
    {
        "id": 8,
        "name": "闫格",
        "gender": "男",
        "ethnicity": "",
        "birth": "1976年1月",
        "birthplace": "",
        "native_place": "",
        "education": "本科，文学学士",
        "party_join": "中共党员",
        "work_start": "1998年7月",
        "current_post": "道里区副区长",
        "current_org": "哈尔滨市道里区人民政府",
        "source": "http://www.hrbdl.gov.cn/hebdlq/c112311/ldy.shtml (official bio — 招商引资、企业服务)",
    },
    # ════════════════════════════════════════
    # 纪委 (Discipline Inspection) — GAP
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "【待查】道里区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "道里区委常委、纪委书记（待查）",
        "current_org": "中共哈尔滨市道里区纪律检查委员会",
        "source": "GAP — 官方网站领导之窗页面未列出纪委书记信息；待后续通过哈尔滨市纪委监委任免公示补充",
    },
    # ════════════════════════════════════════
    # 组织部长 (Organization Dept) — GAP
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "【待查】道里区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "道里区委常委、组织部长（待查）",
        "current_org": "中共哈尔滨市道里区委组织部",
        "source": "GAP — 官方网站未列出组织部长信息；待后续补充",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共哈尔滨市道里区委员会", "type": "党委", "level": "正处级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市道里区"},
    {"id": 2, "name": "哈尔滨市道里区人民政府", "type": "政府", "level": "正处级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市道里区"},
    {"id": 3, "name": "中共哈尔滨市道里区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共哈尔滨市纪律检查委员会", "location": "哈尔滨市道里区"},
    {"id": 4, "name": "中共哈尔滨市道里区委组织部", "type": "党委", "level": "正科级", "parent": "中共哈尔滨市道里区委员会", "location": "哈尔滨市道里区"},
    {"id": 5, "name": "哈尔滨市道里区人民武装部", "type": "政府", "level": "正处级", "parent": "哈尔滨警备区", "location": "哈尔滨市道里区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 于军 — 区委书记、区长、人武部党委第一书记
    {"person_id": 1, "org_id": 1, "title": "道里区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "党政一肩挑，于军同时兼任区长"},
    {"person_id": 1, "org_id": 2, "title": "道里区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "官方简历确认"},
    {"person_id": 1, "org_id": 5, "title": "人武部党委第一书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "军事日活动确认"},
    # 杜文曦 — 区委副书记
    {"person_id": 2, "org_id": 1, "title": "道里区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年5月以副书记身份带队调研"},
    # 王军 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委、常务副区长"},
    # 王郑新 — 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责住建、城管、城市更新"},
    # 王阳 — 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责教育、卫生、民政、退役军人"},
    # 玄立三 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责农业农村、交通、环保、开发区"},
    # 邢高波 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责公安、司法"},
    # 闫格 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责招商引资、企业服务"},
    # GAP — 纪委书记
    {"person_id": 9, "org_id": 3, "title": "道里区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名和任职时间均未知"},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 组织部长
    {"person_id": 10, "org_id": 4, "title": "道里区委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名和任职时间均未知"},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政正职（于军兼任两职，无搭档关系）
    # 于军与区委副书记
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "道里区委常委会", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 于军与常务副区长
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 于军与各副区长
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区长—副区长", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区长—副区长", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 常务副区长与副区长之间（同在政府班子）
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "道里区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # GAP edges
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—纪委书记（待查）", "overlap_org": "道里区委常委会", "overlap_period": "", "source": "GAP — 纪委书记姓名待查", "confidence": "unverified"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委书记—组织部长（待查）", "overlap_org": "道里区委常委会", "overlap_period": "", "source": "GAP — 组织部长姓名待查", "confidence": "unverified"},
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

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
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}")
    print(f"Orgs: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
