#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 槐荫区 (Huaiyin District), 济南市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济南市
Targets: 区委常委会 members + 区政府 leadership
Task ID: shandong_槐荫区

Research date: 2026-07-25
Official source: http://www.huaiyin.gov.cn/ (槐荫区人民政府)
"""

from __future__ import annotations

import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "槐荫区"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委常委会 (District Party Standing Committee) ──
    {
        "id": 1,
        "name": "孙常建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年7月",
        "birthplace": "",
        "education": "中央党校研究生, 工学学士",
        "party_join": "1991年9月",
        "work_start": "1993年8月",
        "current_post": "中共济南市槐荫区委书记、区委党校校长",
        "current_org": "中共槐荫区委",
        "source": "http://www.huaiyin.gov.cn, 大众日报(2025.01), 山东省委组织部任前公示(2024.12)"
    },
    {
        "id": 2,
        "name": "曲京鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年2月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共槐荫区委副书记、区长、区政府党组书记",
        "current_org": "槐荫区人民政府",
        "source": "百度百科, 槐荫人大(2026.06), 济南日报(2026.05), 人民日报"
    },
    {
        "id": 3,
        "name": "韩卫英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共槐荫区委副书记、统战部部长",
        "current_org": "中共槐荫区委",
        "source": "百度百科, 济南市槐荫区人民政府官网"
    },
    {
        "id": 4,
        "name": "张新村",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区委常委（原副区长，2025年5月辞去副区长）",
        "current_org": "中共槐荫区委",
        "source": "百度百科, 济南日报(2025.05), 新黄河"
    },
    {
        "id": 5,
        "name": "徐冬梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区委常委、宣传部部长",
        "current_org": "中共槐荫区委",
        "source": "新浪财经(2023.08), 槐荫区政府官网, 民主与法制网(2024.12)"
    },
    {
        "id": 6,
        "name": "高太吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区委常委",
        "current_org": "中共槐荫区委",
        "source": "百度百科, 澎湃新闻(2022.02)"
    },
    {
        "id": 7,
        "name": "鹿霆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "济南市纪委常委（原槐荫区委常委、纪委书记、监委主任）",
        "current_org": "中共济南市纪委",
        "source": "百度百科, 槐荫区人大常委会(2025.12)"
    },
    {
        "id": 8,
        "name": "王永华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区委常委、区委办公室主任、青年公园街道党工委书记",
        "current_org": "中共槐荫区委",
        "source": "百度百科, 槐荫区政府官网"
    },
    {
        "id": 9,
        "name": "王振国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区委常委、政法委书记、匡山街道党工委书记",
        "current_org": "中共槐荫区委",
        "source": "槐荫区纪委监察委, 中共济南市委统战部, 大众网"
    },
    {
        "id": 10,
        "name": "谷长军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区委常委、副区长、区政府党组成员",
        "current_org": "槐荫区人民政府",
        "source": "百度百科, 槐荫区政府官网"
    },
    {
        "id": 11,
        "name": "何小刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "",
        "education": "研究生，工商管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区委常委、副区长（原组织部部长、党校校长）",
        "current_org": "槐荫区人民政府",
        "source": "百度百科, 槐荫区政府官网, 济南日报(2025.05)"
    },
    # ── 区政府其他副区长 ──
    {
        "id": 12,
        "name": "杨飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区人民政府副区长",
        "current_org": "槐荫区人民政府",
        "source": "百度百科, 槐荫区人大常委会(2026.02), 爱济南客户端"
    },
    {
        "id": 13,
        "name": "葛方强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区人民政府副区长",
        "current_org": "槐荫区人民政府",
        "source": "爱济南(2026.02), 济南市委组织部任前公示(2026.02)"
    },
    {
        "id": 14,
        "name": "李君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区人民政府副区长",
        "current_org": "槐荫区人民政府",
        "source": "鲁网(2025.06)"
    },
    {
        "id": 15,
        "name": "张宗勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区人民政府科技副区长（挂职一年）",
        "current_org": "槐荫区人民政府",
        "source": "槐荫区人大常委会(2025.12)"
    },
    # ── 原区领导（已离任） ──
    {
        "id": 16,
        "name": "刘敬涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年10月",
        "birthplace": "山东潍坊",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济南市行政审批服务局党组书记（原槐荫区区长）",
        "current_org": "济南市行政审批服务局",
        "source": "百度百科, 槐荫人大(2026.06)"
    },
    {
        "id": 17,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（原槐荫区委副书记）",
        "current_org": "",
        "source": "舜网(2022.02), 闪电新闻(2022.02)"
    },
    # ── 其他重要区级领导 ──
    {
        "id": 18,
        "name": "韩军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区政协主席",
        "current_org": "政协槐荫区委员会",
        "source": "槐荫区政府官网新闻"
    },
    {
        "id": 19,
        "name": "张济",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济南国际医学中心党工委副书记、管委会主任",
        "current_org": "济南国际医学中心",
        "source": "济南日报(2026.05)"
    },
    {
        "id": 20,
        "name": "刘磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区监察委员会主任（新任）",
        "current_org": "槐荫区纪委监委",
        "source": "槐荫区人大常委会(2025.12)"
    },
    {
        "id": 21,
        "name": "傅海卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区公安分局党委书记、局长",
        "current_org": "济南市公安局槐荫分局",
        "source": "槐荫区政府官网新闻"
    },
    {
        "id": 22,
        "name": "付国斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区副区长级领导",
        "current_org": "槐荫区人民政府",
        "source": "槐荫区政府官网"
    },
    {
        "id": 23,
        "name": "王堃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "槐荫区副区长级领导",
        "current_org": "槐荫区人民政府",
        "source": "槐荫区政府官网"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共槐荫区委", "type": "党委", "level": "县级", "parent": "中共济南市委", "location": "济南市槐荫区"},
    {"id": 2, "name": "槐荫区人民政府", "type": "政府", "level": "县级", "parent": "济南市人民政府", "location": "济南市槐荫区"},
    {"id": 3, "name": "槐荫区纪委监委", "type": "党委", "level": "县级", "parent": "中共槐荫区委", "location": "济南市槐荫区"},
    {"id": 4, "name": "政协槐荫区委员会", "type": "政协", "level": "县级", "parent": "政协济南市委员会", "location": "济南市槐荫区"},
    {"id": 5, "name": "济南国际医学中心", "type": "事业单位", "level": "市级", "parent": "济南市人民政府", "location": "济南市槐荫区"},
    {"id": 6, "name": "济南市公安局槐荫分局", "type": "政府", "level": "县级", "parent": "济南市公安局", "location": "济南市槐荫区"},
    {"id": 7, "name": "中共济南市纪委", "type": "党委", "level": "市级", "parent": "中共济南市委", "location": "济南市"},
    {"id": 8, "name": "济南市行政审批服务局", "type": "政府", "level": "市级", "parent": "济南市人民政府", "location": "济南市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 孙常建
    {"person_id": 1, "org_id": 1, "title": "中共槐荫区委书记、区委党校校长", "start_date": "2022-02", "end_date": "", "rank": "1", "note": "2024.12拟任正厅级，2025.01兼市人大常委会副主任"},
    {"person_id": 1, "org_id": 2, "title": "槐荫区区长（曾任）", "start_date": "2021-03", "end_date": "2022-02", "rank": "1", "note": "曾任代理区长后转正"},
    # 曲京鹏
    {"person_id": 2, "org_id": 1, "title": "中共槐荫区委副书记", "start_date": "2026-05", "end_date": "", "rank": "2", "note": "2026.05任副书记"},
    {"person_id": 2, "org_id": 2, "title": "槐荫区区长、区政府党组书记", "start_date": "2026-06", "end_date": "", "rank": "2", "note": "2026.06.18当选区长"},
    {"person_id": 2, "org_id": 2, "title": "槐荫区副区长、代区长（曾任）", "start_date": "2026-05", "end_date": "2026-06", "rank": "2", "note": ""},
    # 韩卫英
    {"person_id": 3, "org_id": 1, "title": "中共槐荫区委副书记、统战部部长", "start_date": "2022-02", "end_date": "", "rank": "3", "note": ""},
    # 张新村
    {"person_id": 4, "org_id": 1, "title": "槐荫区委常委", "start_date": "2022-02", "end_date": "", "rank": "4", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "槐荫区副区长（曾任）", "start_date": "", "end_date": "2025-05", "rank": "4", "note": "2025年5月辞去副区长"},
    # 徐冬梅
    {"person_id": 5, "org_id": 1, "title": "槐荫区委常委、宣传部部长", "start_date": "2022-02", "end_date": "", "rank": "5", "note": ""},
    # 高太吉
    {"person_id": 6, "org_id": 1, "title": "槐荫区委常委", "start_date": "2022-02", "end_date": "", "rank": "6", "note": "具体分管领域待查"},
    # 鹿霆
    {"person_id": 7, "org_id": 1, "title": "槐荫区委常委、纪委书记、监委主任（曾任）", "start_date": "2022-02", "end_date": "2025-12", "rank": "7", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "济南市纪委常委", "start_date": "2025-12", "end_date": "", "rank": "7a", "note": "上调市纪委"},
    # 王永华
    {"person_id": 8, "org_id": 1, "title": "槐荫区委常委、区委办公室主任", "start_date": "2022-02", "end_date": "", "rank": "8", "note": "兼青年公园街道党工委书记"},
    # 王振国
    {"person_id": 9, "org_id": 1, "title": "槐荫区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "9", "note": "兼匡山街道党工委书记"},
    # 谷长军
    {"person_id": 10, "org_id": 2, "title": "槐荫区委常委、副区长、区政府党组成员", "start_date": "2022-02", "end_date": "", "rank": "10", "note": "常务副区长"},
    # 何小刚
    {"person_id": 11, "org_id": 2, "title": "槐荫区委常委、副区长", "start_date": "2025-05", "end_date": "", "rank": "11", "note": "原组织部部长"},
    {"person_id": 11, "org_id": 1, "title": "槐荫区委常委、组织部部长（曾任）", "start_date": "2022-02", "end_date": "2025-05", "rank": "11a", "note": ""},
    # 杨飞
    {"person_id": 12, "org_id": 2, "title": "槐荫区副区长", "start_date": "2026-02", "end_date": "", "rank": "13", "note": ""},
    # 葛方强
    {"person_id": 13, "org_id": 2, "title": "槐荫区副区长", "start_date": "2026-02", "end_date": "", "rank": "14", "note": "原市公安局南部山区分局局长"},
    # 李君
    {"person_id": 14, "org_id": 2, "title": "槐荫区副区长", "start_date": "2025-06", "end_date": "", "rank": "15", "note": "分管食品药品安全"},
    # 张宗勇
    {"person_id": 15, "org_id": 2, "title": "槐荫区科技副区长（挂职）", "start_date": "2025-12", "end_date": "2026-12", "rank": "16", "note": "挂职一年，分管科技"},
    # 刘敬涛
    {"person_id": 16, "org_id": 2, "title": "槐荫区区长（曾任）", "start_date": "2021-03", "end_date": "2026-05", "rank": "2", "note": "已离任"},
    {"person_id": 16, "org_id": 8, "title": "济南市行政审批服务局党组书记", "start_date": "2026-05", "end_date": "", "rank": "2a", "note": "新去向"},
    # 李强
    {"person_id": 17, "org_id": 1, "title": "槐荫区委副书记（曾任）", "start_date": "2022-02", "end_date": "", "rank": "3", "note": "去向待查"},
    # 韩军
    {"person_id": 18, "org_id": 4, "title": "槐荫区政协主席", "start_date": "", "end_date": "", "rank": "1", "note": ""},
    # 张济
    {"person_id": 19, "org_id": 5, "title": "济南国际医学中心党工委副书记、管委会主任", "start_date": "", "end_date": "", "rank": "1", "note": ""},
    # 刘磊
    {"person_id": 20, "org_id": 3, "title": "槐荫区监察委员会主任", "start_date": "2025-12", "end_date": "", "rank": "1", "note": "新任"},
    # 傅海卫
    {"person_id": 21, "org_id": 6, "title": "槐荫区公安分局党委书记、局长", "start_date": "", "end_date": "", "rank": "1", "note": ""},
    # 付国斌
    {"person_id": 22, "org_id": 2, "title": "槐荫区副区长级领导", "start_date": "", "end_date": "", "rank": "17", "note": "具体职务待查"},
    # 王堃
    {"person_id": 23, "org_id": 2, "title": "槐荫区副区长级领导", "start_date": "", "end_date": "", "rank": "18", "note": "具体职务待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政正职搭档", "overlap_org": "槐荫区委/区政府", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记领导副书记", "overlap_org": "中共槐荫区委", "overlap_period": "2022-02至今"},
    {"person_a": 2, "person_b": 3, "type": "同级协作", "context": "同为区委副书记", "overlap_org": "中共槐荫区委", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "书记与常委兼副区长", "overlap_org": "中共槐荫区委", "overlap_period": "2022-02至今"},
    {"person_a": 2, "person_b": 10, "type": "党政搭档", "context": "区长与常务副区长", "overlap_org": "槐荫区人民政府", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "书记与区委办主任", "overlap_org": "中共槐荫区委", "overlap_period": "2022-02至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "何小刚先后任组织部长、副区长", "overlap_org": "中共槐荫区委", "overlap_period": "2022-02至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长", "overlap_org": "槐荫区人民政府", "overlap_period": "2026-06至今"},
    {"person_a": 16, "person_b": 2, "type": "交接", "context": "刘敬涛卸任→曲京鹏接任区长", "overlap_org": "槐荫区人民政府", "overlap_period": "2026-05至2026-06"},
    {"person_a": 7, "person_b": 20, "type": "交接", "context": "鹿霆卸任→刘磊接任监委主任", "overlap_org": "槐荫区纪委监委", "overlap_period": "2025-12"},
    {"person_a": 1, "person_b": 16, "type": "党政搭档", "context": "孙常建任书记、刘敬涛任区长（前任搭档）", "overlap_org": "槐荫区委/区政府", "overlap_period": "2022-02至2026-05"},
    {"person_a": 12, "person_b": 13, "type": "同级协作", "context": "2026年2月同期任命为副区长", "overlap_org": "槐荫区人民政府", "overlap_period": "2026-02至今"},
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
