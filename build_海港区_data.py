#!/usr/bin/env python3
"""Build 秦皇岛市海港区 (Qinhuangdao Haigang District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 秦皇岛市
Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
Task ID: hebei_海港区

Research date: 2026-07-23
Official source: http://www.qhdhgq.gov.cn/ (秦皇岛市海港区人民政府 — partially accessible as of July 2026)

Current status (as of 2026-07-23):
- 区委书记: 张士兆 — 1969年1月出生，河北滦南人；2026年3月仍以区委书记身份出席活动（区委党校春季学期开学典礼）
- 区长: 尹勃 — 2026年1月在海港区第十六届人民代表大会第六次会议上作政府工作报告

Note:
- 海港区政府网站 (www.qhdhgq.gov.cn) 部分可访问
- 张士兆和尹勃的详细履历部分获取（张士兆已获取百度百科摘要信息）
- 前任区长: 鲍成超
- 区委副书记: 庞海涛（出现在政府会议报道中）
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "海港区"
TASK_ID = "hebei_海港区"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

AS_OF = "2026-07-23"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════

    # 张士兆 — 海港区委书记
    # 来源：百度百科摘要 + 多家新闻媒体报道（2026年1月、3月均有活动记录）
    {
        "id": 1,
        "name": "张士兆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-01",
        "birthplace": "河北滦南",
        "native_place": "河北滦南",
        "education": "大学",
        "party_join": "1995-10",
        "work_start": "1991-07",
        "current_post": "海港区委书记",
        "current_org": "中共秦皇岛市海港区委员会",
        "source": "百度百科摘要 — 张士兆，男，汉族，1969年1月出生，河北滦南人，1991年7月参加工作，1995年10月加入中国共产党，大学文化。现任河北省秦皇岛市海港区委书记。",
    },
    # 尹勃 — 海港区委副书记、区长
    # 来源：海港区政府官网（www.qhdhgq.gov.cn）文章"尹勃召开征求意见座谈会"（2026.01.22）
    # 海港区第十六届人民代表大会第六次会议（尹勃作政府工作报告）
    {
        "id": 2,
        "name": "尹勃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海港区委副书记、区长",
        "current_org": "海港区人民政府",
        "source": "海港区政府官网 — https://www.qhdhgq.gov.cn/article_show.aspx?id=20260 （尹勃召开征求意见座谈会，2026.01.22）；海港区第十六届人民代表大会第六次会议（尹勃作政府工作报告）",
    },
    # 鲍成超 — 前任区长
    {
        "id": 3,
        "name": "鲍成超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任）海港区区长",
        "current_org": "海港区人民政府",
        "source": "多家媒体报道中提及曾担任海港区区长",
    },
    # 庞海涛 — 常务副区长/区委常委
    # 来源：海港区政府官网报道中提及"海港区领导庞海涛参加"
    {
        "id": 4,
        "name": "庞海涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海港区委常委、副区长（推测）",
        "current_org": "海港区人民政府",
        "source": '海港区政府官网 — https://www.qhdhgq.gov.cn/article_show.aspx?id=20260 (海港区领导庞海涛参加)',
    },
    # 孙贺 — 区委常委、区委办公室主任
    # 来源：东北大学秦皇岛分校新闻网报道校地合作活动中"区委常委、区委办公室主任孙贺参加"
    {
        "id": 5,
        "name": "孙贺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海港区委常委、区委办公室主任",
        "current_org": "中共秦皇岛市海港区委员会",
        "source": "东北大学秦皇岛分校新闻网 — 校地合作活动报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共秦皇岛市海港区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共秦皇岛市委员会",
        "location": "河北省秦皇岛市海港区",
    },
    {
        "id": 2,
        "name": "海港区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "秦皇岛市人民政府",
        "location": "河北省秦皇岛市海港区",
    },
    {
        "id": 3,
        "name": "海港区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "秦皇岛市人大常委会",
        "location": "河北省秦皇岛市海港区",
    },
    {
        "id": 4,
        "name": "政协海港区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协秦皇岛市委员会",
        "location": "河北省秦皇岛市海港区",
    },
    {
        "id": 5,
        "name": "海港区纪委监委",
        "type": "纪委",
        "level": "市辖区",
        "parent": "秦皇岛市纪委监委",
        "location": "河北省秦皇岛市海港区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张士兆 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "海港区委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "截至2026年7月确认为现任；区人武部党委第一书记"},
    # 尹勃 — 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "海港区区长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "截至2026年7月确认为现任；2026年1月区人代会上作政府工作报告"},
    {"person_id": 2, "org_id": 1, "title": "海港区委副书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 鲍成超 — 前任区长
    {"person_id": 3, "org_id": 2, "title": "海港区区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任区长；当前去向待查"},
    # 庞海涛 — 区委常委、副区长
    {"person_id": 4, "org_id": 2, "title": "海港区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "出现在政府会议报道中，具体分管领域待查"},
    {"person_id": 4, "org_id": 1, "title": "海港区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 孙贺 — 区委常委、区委办公室主任
    {"person_id": 5, "org_id": 1, "title": "海港区委常委、区委办公室主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "出现在校地合作活动报道中"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张士兆 — 尹勃 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "海港区党政一把手工作搭档关系", "overlap_org": "海港区", "overlap_period": "?至今"},
    # 尹勃 — 鲍成超 前后任
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "海港区区长前后任关系", "overlap_org": "海港区人民政府", "overlap_period": ""},
    # 张士兆 — 庞海涛 上下级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委/副区长工作关系", "overlap_org": "中共海港区委员会/海港区人民政府", "overlap_period": ""},
    # 尹勃 — 庞海涛 上下级
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "海港区人民政府", "overlap_period": ""},
    # 张士兆 — 孙贺 上下级
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与区委办公室主任工作关系", "overlap_org": "中共海港区委员会", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  秦皇岛市海港区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-23")
    print("  ✅ 区委书记确认: 张士兆")
    print("  ✅ 区长确认: 尹勃")
    print("  ⚠️  详细履历需后续补充（百度百科WAF拦截、政府新闻部分不可达）")
    print("  ⚠️  前任区长: 鲍成超（去向待查）")
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
    print("\n✅ 海港区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  ⚠️  张士兆、尹勃等核心人物的详细履历待补充。")
    print("  ⚠️  鲍成超的去向待查。")
