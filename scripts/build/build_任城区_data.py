#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 任城区 (Rencheng District), 济宁市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济宁市
Targets: 区委常委会 members + 区政府 leadership
Task ID: shandong_任城区

Research date: 2026-07-25
Official source: http://www.rencheng.gov.cn/ (任城区人民政府)
                  http://qw.rencheng.gov.cn/ (任城区委)
"""

from __future__ import annotations

import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "任城区"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委常委会 (District Party Standing Committee) ──
    {
        "id": 1,
        "name": "张令华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济宁市任城区委书记",
        "current_org": "中共任城区委",
        "source": "http://qw.rencheng.gov.cn/col/col59840/index.html, 任城区政府门户网站新闻(2026.07)"
    },
    {
        "id": 2,
        "name": "高晓华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年2月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共任城区委副书记、区长、区政府党组书记",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col108951/index.html"
    },
    {
        "id": 3,
        "name": "程庆辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、区纪委书记、区监委主任",
        "current_org": "中共任城区纪委/任城区监委",
        "source": "http://qw.rencheng.gov.cn/col/col76643/index.html"
    },
    {
        "id": 4,
        "name": "王健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、组织部部长",
        "current_org": "中共任城区委",
        "source": "任城区政府门户网站新闻(2026.07)"
    },
    {
        "id": 5,
        "name": "罗会涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年7月",
        "birthplace": "",
        "education": "研究生工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、副区长（常务）",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col108272/index.html"
    },
    {
        "id": 6,
        "name": "朱涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、办公室主任、统战部部长",
        "current_org": "中共任城区委",
        "source": "http://qw.rencheng.gov.cn/col/col76646/index.html"
    },
    {
        "id": 7,
        "name": "时慧芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、宣传部部长",
        "current_org": "中共任城区委",
        "source": "http://qw.rencheng.gov.cn/col/col76647/index.html"
    },
    {
        "id": 8,
        "name": "李俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、政法委书记",
        "current_org": "中共任城区委",
        "source": "http://qw.rencheng.gov.cn/col/col76648/index.html"
    },
    {
        "id": 9,
        "name": "惠令峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年1月",
        "birthplace": "",
        "education": "全日制大专，在职省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、副区长",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col76892/index.html"
    },
    {
        "id": 10,
        "name": "赵风雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、人武部部长",
        "current_org": "任城区人武部",
        "source": "http://qw.rencheng.gov.cn/col/col108956/index.html"
    },
    {
        "id": 11,
        "name": "孙大鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区委常委、副区长",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col109068/index.html"
    },
    # ── 区政府其他副区长 ──
    {
        "id": 12,
        "name": "张方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年1月",
        "birthplace": "",
        "education": "省委党校研究生学历，理学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区人民政府副区长、任城公安分局局长",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col76890/index.html"
    },
    {
        "id": 13,
        "name": "王胜男",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区人民政府副区长",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col76891/index.html"
    },
    {
        "id": 14,
        "name": "盛振亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区人民政府副区长",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col107029/index.html"
    },
    {
        "id": 15,
        "name": "高斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区人民政府副区长",
        "current_org": "任城区人民政府",
        "source": "http://www.rencheng.gov.cn/col/col109836/index.html"
    },
    # ── 区人大、政协主要领导 ──
    {
        "id": 16,
        "name": "李翠玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任城区人大常委会主任（推测）",
        "current_org": "任城区人大常委会",
        "source": "任城区政府门户网站新闻(2026.07.16), 区委理论学习中心组集体学习研讨"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共任城区委", "type": "党委", "level": "县级", "parent": "中共济宁市委", "location": "济宁市任城区"},
    {"id": 2, "name": "任城区人民政府", "type": "政府", "level": "县级", "parent": "济宁市人民政府", "location": "济宁市任城区"},
    {"id": 3, "name": "中共任城区纪委/任城区监委", "type": "党委", "level": "县级", "parent": "中共任城区委", "location": "济宁市任城区"},
    {"id": 4, "name": "任城区人大常委会", "type": "人大", "level": "县级", "parent": "济宁市人大常委会", "location": "济宁市任城区"},
    {"id": 5, "name": "政协任城区委员会", "type": "政协", "level": "县级", "parent": "政协济宁市委员会", "location": "济宁市任城区"},
    {"id": 6, "name": "任城区人武部", "type": "政府", "level": "县级", "parent": "济宁军分区", "location": "济宁市任城区"},
    {"id": 7, "name": "任城公安分局", "type": "政府", "level": "县级", "parent": "济宁市公安局", "location": "济宁市任城区"},
    {"id": 8, "name": "济宁运河经济开发区管委会", "type": "开发区", "level": "县级", "parent": "任城区人民政府", "location": "济宁市任城区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张令华 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共任城区委书记", "start_date": "", "end_date": "", "rank": "1", "note": "主持区委全面工作。分管干部工作和区委党校等工作。截至2026年7月仍在任。"},
    # 高晓华 — 区长
    {"person_id": 2, "org_id": 1, "title": "中共任城区委副书记", "start_date": "", "end_date": "", "rank": "2", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "任城区区长、区政府党组书记", "start_date": "", "end_date": "", "rank": "2", "note": "主持区政府全面工作。负责财政、审计等工作。"},
    # 程庆辉 — 纪委书记
    {"person_id": 3, "org_id": 1, "title": "任城区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "3", "note": "分管区委巡察办等工作"},
    {"person_id": 3, "org_id": 3, "title": "任城区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "3", "note": ""},
    # 王健 — 组织部长
    {"person_id": 4, "org_id": 1, "title": "任城区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "4", "note": ""},
    # 罗会涛 — 常务副区长
    {"person_id": 5, "org_id": 1, "title": "任城区委常委", "start_date": "", "end_date": "", "rank": "5", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "任城区副区长（常务）", "start_date": "", "end_date": "", "rank": "5", "note": "负责区政府常务工作，分管发展改革、应急管理、行政审批、统计、开发区等工作"},
    # 朱涛 — 区委办主任、统战部长
    {"person_id": 6, "org_id": 1, "title": "任城区委常委、办公室主任、统战部部长", "start_date": "", "end_date": "", "rank": "6", "note": "主持区委办公室、区委统战部工作"},
    # 时慧芬 — 宣传部长
    {"person_id": 7, "org_id": 1, "title": "任城区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "7", "note": "主持区委宣传部工作"},
    # 李俊杰 — 政法委书记
    {"person_id": 8, "org_id": 1, "title": "任城区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "8", "note": "主持区委政法委工作，协助高晓华同志分管稳定、信访工作"},
    # 惠令峰 — 副区长
    {"person_id": 9, "org_id": 1, "title": "任城区委常委", "start_date": "", "end_date": "", "rank": "9", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "任城区副区长", "start_date": "", "end_date": "", "rank": "9", "note": "负责税务、金融保险、国资监管等工作"},
    # 赵风雨 — 人武部长
    {"person_id": 10, "org_id": 1, "title": "任城区委常委、人武部部长", "start_date": "", "end_date": "", "rank": "10", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "任城区人武部部长", "start_date": "", "end_date": "", "rank": "10", "note": ""},
    # 孙大鹏 — 副区长
    {"person_id": 11, "org_id": 1, "title": "任城区委常委", "start_date": "", "end_date": "", "rank": "11", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "任城区副区长", "start_date": "", "end_date": "", "rank": "11", "note": "协助惠令峰同志负责金融保险、投融资管理方面的工作"},
    # 张方 — 副区长/公安局长
    {"person_id": 12, "org_id": 2, "title": "任城区副区长", "start_date": "", "end_date": "", "rank": "12", "note": "负责公安、司法、退役军人、信访等工作"},
    {"person_id": 12, "org_id": 7, "title": "任城公安分局局长", "start_date": "", "end_date": "", "rank": "12", "note": "主持任城公安分局工作"},
    # 王胜男 — 副区长
    {"person_id": 13, "org_id": 2, "title": "任城区副区长", "start_date": "", "end_date": "", "rank": "13", "note": "负责科技、工信、商务、文旅、市场监管、招商引资等工作"},
    # 盛振亮 — 副区长
    {"person_id": 14, "org_id": 2, "title": "任城区副区长", "start_date": "", "end_date": "", "rank": "14", "note": "负责教育体育、民政、水务、农业农村、乡村振兴、卫生健康等工作"},
    # 高斌 — 副区长
    {"person_id": 15, "org_id": 2, "title": "任城区副区长", "start_date": "", "end_date": "", "rank": "15", "note": "负责自然资源和规划、住建、交通、综合执法、生态环境等工作"},
    # 李翠玲 — 人大常委会主任
    {"person_id": 16, "org_id": 4, "title": "任城区人大常委会主任（推测）", "start_date": "", "end_date": "", "rank": "16", "note": "2026年7月16日参加区委理论学习中心组集体学习研讨，具体职务待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政正职搭档", "overlap_org": "任城区委/区政府", "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记领导纪委书记", "overlap_org": "中共任城区委", "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记领导常委副区长", "overlap_org": "中共任城区委", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 5, "type": "党政搭档", "context": "区长与常务副区长", "overlap_org": "任城区人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "李俊杰协助高晓华分管稳定、信访工作", "overlap_org": "中共任城区委/区政府", "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记领导区委办主任", "overlap_org": "中共任城区委", "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记领导组织部长", "overlap_org": "中共任城区委", "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记领导宣传部长", "overlap_org": "中共任城区委", "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记领导政法委书记", "overlap_org": "中共任城区委", "overlap_period": "截至2026年7月"},
    {"person_a": 9, "person_b": 11, "type": "协作", "context": "孙大鹏协助惠令峰负责金融保险工作", "overlap_org": "任城区人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长领导副区长", "overlap_org": "任城区人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长领导副区长", "overlap_org": "任城区人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长领导副区长", "overlap_org": "任城区人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "区长领导副区长", "overlap_org": "任城区人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长领导副区长兼公安局长", "overlap_org": "任城区人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 16, "type": "同级协作", "context": "区委书记与人大常委会主任", "overlap_org": "任城区四套班子", "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
    )
