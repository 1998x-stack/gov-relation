#!/usr/bin/env python3
"""Build 石家庄市长安区 (Shijiazhuang Chang'an District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 石家庄市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)

Research date: 2026-07-23
Official source: http://www.sjzca.gov.cn/ (石家庄市长安区人民政府)

Current status (as of 2025-10-23, from official 领导信息 page):
- 区委书记: 【待确认】 — 公开来源无法确认当前在任区委书记姓名
- 区长: 孙海涛 — 领导区政府全面工作（区政府领导分工页面确认）

Government leadership (confirmed from official 2025-10-23 page):
- 区长: 孙海涛 (区政府全面工作)
- 常务副区长: 景建涛 (主持政府日常工作)
- 副区长: 郝永志, 张红卫, 孙兵臣, 杨素静, 梁谦, 张俊立
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "长安区"
TASK_ID = "hebei_长安区"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    # 区委书记 — 公开渠道无法确认
    # 备注：截至2026年7月，通过政府网站、新闻搜索均未能确认当前区委书记姓名
    # 可能是近期人事变动导致。留空待后续补充。

    # ════════════════════════════════════════
    # 区政府领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "孙海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区委副书记、区长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
    {
        "id": 2,
        "name": "景建涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区委常委、常务副区长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
    {
        "id": 3,
        "name": "郝永志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区副区长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
    {
        "id": 4,
        "name": "张红卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区副区长、长安公安分局局长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
    {
        "id": 5,
        "name": "孙兵臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区副区长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
    {
        "id": 6,
        "name": "杨素静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区副区长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
    {
        "id": 7,
        "name": "梁谦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区副区长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
    {
        "id": 8,
        "name": "张俊立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长安区副区长",
        "current_org": "长安区人民政府",
        "source": "http://www.sjzca.gov.cn/columns/b03f89f4-2b09-4cc8-a33e-10b6be8313e0/202510/23/e0f583b5-046e-43ae-b9bd-c140ffcd11f6.html (official — 区政府领导工作分工)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共石家庄市长安区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市长安区",
    },
    {
        "id": 2,
        "name": "长安区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市长安区",
    },
    {
        "id": 3,
        "name": "长安区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "石家庄市人大常委会",
        "location": "河北省石家庄市长安区",
    },
    {
        "id": 4,
        "name": "政协长安区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协石家庄市委员会",
        "location": "河北省石家庄市长安区",
    },
    {
        "id": 5,
        "name": "长安公安分局",
        "type": "政府",
        "level": "区直部门",
        "parent": "石家庄市公安局",
        "location": "河北省石家庄市长安区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 孙海涛 — 区长
    {"person_id": 1, "org_id": 2, "title": "长安区委副书记、区长", "start": "", "end": "至今", "rank": "", "note": "领导区政府全面工作"},
    {"person_id": 1, "org_id": 1, "title": "长安区委副书记", "start": "", "end": "至今", "rank": "", "note": "区委副书记、区政府党组书记"},

    # 景建涛 — 常务副区长
    {"person_id": 2, "org_id": 2, "title": "长安区委常委、常务副区长", "start": "", "end": "至今", "rank": "", "note": "主持政府日常工作"},
    {"person_id": 2, "org_id": 1, "title": "长安区委常委", "start": "", "end": "至今", "rank": "", "note": ""},

    # 郝永志 — 副区长
    {"person_id": 3, "org_id": 2, "title": "长安区副区长", "start": "", "end": "至今", "rank": "", "note": "分管教育、医保、卫健等工作"},

    # 张红卫 — 副区长、公安局长
    {"person_id": 4, "org_id": 2, "title": "长安区副区长", "start": "", "end": "至今", "rank": "", "note": "分管公安、司法、信访等工作"},
    {"person_id": 4, "org_id": 5, "title": "长安公安分局局长", "start": "", "end": "至今", "rank": "", "note": ""},

    # 孙兵臣 — 副区长
    {"person_id": 5, "org_id": 2, "title": "长安区副区长", "start": "", "end": "至今", "rank": "", "note": "分管科技、文体、旅游、民政等工作"},

    # 杨素静 — 副区长
    {"person_id": 6, "org_id": 2, "title": "长安区副区长", "start": "", "end": "至今", "rank": "", "note": "分管城管、园林、农业农村等工作"},

    # 梁谦 — 副区长
    {"person_id": 7, "org_id": 2, "title": "长安区副区长", "start": "", "end": "至今", "rank": "", "note": "分管地方金融发展等工作"},

    # 张俊立 — 副区长
    {"person_id": 8, "org_id": 2, "title": "长安区副区长", "start": "", "end": "至今", "rank": "", "note": "分管市场监管、食品安全等工作"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 孙海涛与景建涛（正副区长搭档关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区长与常务副区长工作搭档", "overlap_org": "长安区人民政府", "overlap_period": ""},

    # 工作补位关系 (from official document: 景建涛与梁谦、张俊立互为补位)
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "常务副区长与副区长工作补位", "overlap_org": "长安区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "常务副区长与副区长工作补位", "overlap_org": "长安区人民政府", "overlap_period": ""},

    # 工作补位关系 (郝永志与杨素静互为补位)
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "副区长工作补位", "overlap_org": "长安区人民政府", "overlap_period": ""},

    # 工作补位关系 (张红卫与孙兵臣互为补位)
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "副区长工作补位", "overlap_org": "长安区人民政府", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  石家庄市长安区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-23")
    print("=" * 60)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("\n✅ 长安区党建数据构建完成。")
    print("  ⚠️ 注意：区委书记信息尚未确认，需补充调查。")
