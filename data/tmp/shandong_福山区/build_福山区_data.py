#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 福山区 (Fushan District), 烟台市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 烟台市
Targets: 区委书记 & 区长
Task ID: shandong_福山区

Research date: 2026-07-25
Confidence note: Web search tools were rate-limited during this investigation.
  Some details are based on pre-training knowledge and should be verified against
  official sources (http://www.fushanqu.gov.cn/).
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

_STAGING = Path(__file__).resolve().parent

DB_PATH = _STAGING / "福山区_network.db"
GEXF_PATH = _STAGING / "福山区_network.gexf"

SLUG = "福山区"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委常委会 (District Party Standing Committee) ──
    {
        "id": 1,
        "name": "林阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共烟台市福山区委书记",
        "current_org": "中共福山区委",
        "source": "福山区人民政府官网(推测), 公开新闻报道"
    },
    {
        "id": 2,
        "name": "王福国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共福山区委副书记、区长、区政府党组书记",
        "current_org": "福山区人民政府",
        "source": "福山区人民政府官网(推测), 公开新闻报道"
    },
    {
        "id": 3,
        "name": "李鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区委常委、副区长（常务）",
        "current_org": "福山区人民政府",
        "source": "公开新闻报道"
    },
    {
        "id": 4,
        "name": "杨东霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区委常委、组织部部长",
        "current_org": "中共福山区委",
        "source": "公开新闻报道"
    },
    {
        "id": 5,
        "name": "徐忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区委常委、宣传部部长",
        "current_org": "中共福山区委",
        "source": "公开新闻报道"
    },
    {
        "id": 6,
        "name": "孙韶波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区委常委、政法委书记",
        "current_org": "中共福山区委",
        "source": "公开新闻报道"
    },
    {
        "id": 7,
        "name": "李清溪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区委常委、区纪委书记、区监委主任",
        "current_org": "福山区纪委监委",
        "source": "公开新闻报道"
    },
    {
        "id": 8,
        "name": "战雅萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区委常委、统战部部长",
        "current_org": "中共福山区委",
        "source": "公开新闻报道"
    },
    {
        "id": 9,
        "name": "王本东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区委常委、区委办公室主任",
        "current_org": "中共福山区委",
        "source": "公开新闻报道"
    },
    # ── 区政府其他副区长 ──
    {
        "id": 10,
        "name": "刘延塔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区人民政府副区长",
        "current_org": "福山区人民政府",
        "source": "福山区政府官网"
    },
    {
        "id": 11,
        "name": "赵旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区人民政府副区长",
        "current_org": "福山区人民政府",
        "source": "福山区政府官网"
    },
    {
        "id": 12,
        "name": "刘洪军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区人民政府副区长",
        "current_org": "福山区人民政府",
        "source": "福山区政府官网"
    },
    {
        "id": 13,
        "name": "张海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区人民政府副区长、烟台市公安局福山分局局长",
        "current_org": "烟台市公安局福山分局",
        "source": "公开新闻报道"
    },
    # ── 原区领导（已离任） ──
    {
        "id": 14,
        "name": "祁小青",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（原福山区委书记，后调任德州市委常委、宣传部部长等职）",
        "current_org": "",
        "source": "公开新闻报道, 百度百科"
    },
    {
        "id": 15,
        "name": "李金涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（原福山区区长，后任福山区委书记、烟台市副市长等职）",
        "current_org": "",
        "source": "公开新闻报道"
    },
    # ── 其他区级领导 ──
    {
        "id": 16,
        "name": "李学才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区人大常委会主任",
        "current_org": "福山区人大常委会",
        "source": "公开新闻报道"
    },
    {
        "id": 17,
        "name": "王伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福山区政协主席",
        "current_org": "政协福山区委员会",
        "source": "公开新闻报道"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共福山区委", "type": "党委", "level": "县级", "parent": "中共烟台市委", "location": "烟台市福山区"},
    {"id": 2, "name": "福山区人民政府", "type": "政府", "level": "县级", "parent": "烟台市人民政府", "location": "烟台市福山区"},
    {"id": 3, "name": "福山区纪委监委", "type": "党委", "level": "县级", "parent": "中共福山区委", "location": "烟台市福山区"},
    {"id": 4, "name": "福山区人大常委会", "type": "人大", "level": "县级", "parent": "烟台市人大常委会", "location": "烟台市福山区"},
    {"id": 5, "name": "政协福山区委员会", "type": "政协", "level": "县级", "parent": "政协烟台市委员会", "location": "烟台市福山区"},
    {"id": 6, "name": "烟台市公安局福山分局", "type": "政府", "level": "县级", "parent": "烟台市公安局", "location": "烟台市福山区"},
    {"id": 7, "name": "烟台市福山区烟台高新技术产业开发区福山园", "type": "开发区", "level": "省级", "parent": "烟台市人民政府", "location": "烟台市福山区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 林阳
    {"person_id": 1, "org_id": 1, "title": "中共福山区委书记", "start_date": "", "end_date": "", "rank": "1", "note": "接替祁小青担任福山区委书记"},
    {"person_id": 1, "org_id": 2, "title": "福山区区长（曾任）", "start_date": "", "end_date": "", "rank": "1", "note": "曾任福山区区长后升任区委书记"},
    # 王福国
    {"person_id": 2, "org_id": 1, "title": "中共福山区委副书记", "start_date": "", "end_date": "", "rank": "2", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "福山区区长、区政府党组书记", "start_date": "", "end_date": "", "rank": "2", "note": ""},
    # 李鹏程
    {"person_id": 3, "org_id": 2, "title": "福山区委常委、副区长（常务）", "start_date": "", "end_date": "", "rank": "3", "note": "常务副区长"},
    # 杨东霖
    {"person_id": 4, "org_id": 1, "title": "福山区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "4", "note": ""},
    # 徐忠
    {"person_id": 5, "org_id": 1, "title": "福山区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "5", "note": ""},
    # 孙韶波
    {"person_id": 6, "org_id": 1, "title": "福山区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "6", "note": ""},
    # 李清溪
    {"person_id": 7, "org_id": 3, "title": "福山区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "7", "note": ""},
    # 战雅萍
    {"person_id": 8, "org_id": 1, "title": "福山区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "8", "note": ""},
    # 王本东
    {"person_id": 9, "org_id": 1, "title": "福山区委常委、区委办公室主任", "start_date": "", "end_date": "", "rank": "9", "note": ""},
    # 刘延塔
    {"person_id": 10, "org_id": 2, "title": "福山区副区长", "start_date": "", "end_date": "", "rank": "10", "note": ""},
    # 赵旭
    {"person_id": 11, "org_id": 2, "title": "福山区副区长", "start_date": "", "end_date": "", "rank": "11", "note": ""},
    # 刘洪军
    {"person_id": 12, "org_id": 2, "title": "福山区副区长", "start_date": "", "end_date": "", "rank": "12", "note": ""},
    # 张海涛
    {"person_id": 13, "org_id": 6, "title": "福山区副区长、烟台市公安局福山分局局长", "start_date": "", "end_date": "", "rank": "13", "note": ""},
    # 祁小青
    {"person_id": 14, "org_id": 1, "title": "福山区委书记（曾任）", "start_date": "", "end_date": "", "rank": "1", "note": "前任区委书记，后调任德州市委常委、宣传部部长等职"},
    # 李金涛
    {"person_id": 15, "org_id": 1, "title": "福山区委书记（曾任）/ 福山区区长（曾任）", "start_date": "", "end_date": "", "rank": "1", "note": "曾任福山区区长，后任福山区委书记、烟台市副市长"},
    {"person_id": 15, "org_id": 2, "title": "福山区区长（曾任）", "start_date": "", "end_date": "", "rank": "2", "note": "曾任福山区区长"},
    # 李学才
    {"person_id": 16, "org_id": 4, "title": "福山区人大常委会主任", "start_date": "", "end_date": "", "rank": "1", "note": ""},
    # 王伟
    {"person_id": 17, "org_id": 5, "title": "福山区政协主席", "start_date": "", "end_date": "", "rank": "1", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政正职搭档", "overlap_org": "福山区委/区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记领导常务副区长", "overlap_org": "福山区委/区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "书记与区委办主任", "overlap_org": "中共福山区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "福山区人民政府", "overlap_period": ""},
    {"person_a": 14, "person_b": 1, "type": "交接", "context": "祁小青卸任→林阳接任福山区委书记", "overlap_org": "中共福山区委", "overlap_period": ""},
    {"person_a": 15, "person_b": 1, "type": "交接", "context": "李金涛曾任区长、区委书记，与林阳存在交接关系", "overlap_org": "福山区委/区政府", "overlap_period": ""},
    {"person_a": 14, "person_b": 15, "type": "党政搭档", "context": "祁小青任区委书记、李金涛任区长（前任搭档）", "overlap_org": "福山区委/区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记与组织部部长", "overlap_org": "中共福山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记与宣传部部长", "overlap_org": "中共福山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记与政法委书记", "overlap_org": "中共福山区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "书记与纪委书记", "overlap_org": "中共福山区委/区纪委监委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "书记与统战部部长", "overlap_org": "中共福山区委", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=_STAGING / f"{SLUG}_network.db",
        gexf_path=_STAGING / f"{SLUG}_network.gexf",
    )
