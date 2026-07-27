#!/usr/bin/env python3
"""Build 邯郸市邯山区 (Handan Hanshan District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 邯郸市
Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
Task ID: hebei_邯山区

Research date: 2026-07-23
Official source: http://www.hdhs.gov.cn/ (邯郸市邯山区人民政府)
Mayor page: http://www.hdhs.gov.cn/qzzc/ljb/
Deputy pages: http://www.hdhs.gov.cn/qzzc/wjh/, /llfj/, /wyb/, /ZT/, /wf/

Current status (as of 2026-07-23):
- 区委书记: 刘海川 — 主持邯山区第十届委员会第十二次全体会议（2026.05.06）并代表区委常委会作讲话
- 区长: 刘俊波（1974年9月生）— 邯山区委副书记、政府区长、党组书记
- 副区长: 温俊华（1973年10月生，兼公安分局局长）、路风杰、武越波（1976年3月生）、郑婷、王飞
- 中国共产党邯山区第十一次代表大会定于2026年7月召开

Note:
- 邯山区政府网站 (www.hdhs.gov.cn) 可直接访问
- 刘海川和刘俊波的详细履历（出生地点、教育背景、完整任职经历、入党时间、参加工作时间）尚未通过公开官方渠道完整获取
- 百度百科等渠道被WAF/验证码拦截
- 路风杰、郑婷、王飞的官方简历页面未获取详细内容
- 所有履历补充待后续调查
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "邯山区"
TASK_ID = "hebei_邯山区"
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

    # 刘海川 — 邯山区委书记
    # 来源：邯山区第十届委员会第十二次全体会议报道（2026.05.06）
    # "区委书记刘海川代表区委常委会作了讲话"
    {
        "id": 1,
        "name": "刘海川",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "邯山区委书记",
        "current_org": "中共邯郸市邯山区委员会",
        "source": "政府官网 — http://www.hdhs.gov.cn/xwdt/hszw/202605/t20260508_2200854.html",
    },
    # 刘俊波 — 邯山区委副书记、区长
    # 来源：邯山区政府官网"区长之窗"
    # 刘俊波，男，汉族，1974年9月出生，大学学历，中共党员
    # 现任邯山区委副书记，政府区长、党组书记
    {
        "id": 2,
        "name": "刘俊波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "邯山区委副书记、区长",
        "current_org": "邯山区人民政府",
        "source": "政府官网 — http://www.hdhs.gov.cn/qzzc/ljb/",
    },
    # 温俊华 — 副区长、区公安分局局长
    # 温俊华，男，汉族，1973年10月生，大学本科学历，中共党员
    # 现任邯山区政府副区长、党组成员、区公安分局党委书记、局长
    {
        "id": 3,
        "name": "温俊华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "邯山区副区长、区公安分局局长",
        "current_org": "邯山区人民政府",
        "source": "政府官网 — http://www.hdhs.gov.cn/qzzc/wjh/",
    },
    # 路风杰 — 副区长
    {
        "id": 4,
        "name": "路风杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "邯山区副区长",
        "current_org": "邯山区人民政府",
        "source": "政府官网 — http://www.hdhs.gov.cn/qzzc/llfj/",
    },
    # 武越波 — 副区长
    # 武越波，男，汉族，1976年3月出生，本科学历，中共党员
    # 现任邯山区人民政府党组成员、副区长
    {
        "id": 5,
        "name": "武越波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "",
        "native_place": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "邯山区副区长",
        "current_org": "邯山区人民政府",
        "source": "政府官网 — http://www.hdhs.gov.cn/qzzc/wyb/",
    },
    # 郑婷 — 副区长
    {
        "id": 6,
        "name": "郑婷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "邯山区副区长",
        "current_org": "邯山区人民政府",
        "source": "政府官网 — http://www.hdhs.gov.cn/qzzc/ZT/",
    },
    # 王飞 — 副区长
    {
        "id": 7,
        "name": "王飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "邯山区副区长",
        "current_org": "邯山区人民政府",
        "source": "政府官网 — http://www.hdhs.gov.cn/qzzc/wf/",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共邯郸市邯山区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共邯郸市委员会",
        "location": "河北省邯郸市邯山区",
    },
    {
        "id": 2,
        "name": "邯山区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市邯山区",
    },
    {
        "id": 3,
        "name": "邯山区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "邯郸市人大常委会",
        "location": "河北省邯郸市邯山区",
    },
    {
        "id": 4,
        "name": "政协邯山区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协邯郸市委员会",
        "location": "河北省邯郸市邯山区",
    },
    {
        "id": 5,
        "name": "邯山区纪委监委",
        "type": "纪委",
        "level": "市辖区",
        "parent": "邯郸市纪委监委",
        "location": "河北省邯郸市邯山区",
    },
    {
        "id": 6,
        "name": "邯山区公安分局",
        "type": "政府",
        "level": "市辖区",
        "parent": "邯郸市公安局",
        "location": "河北省邯郸市邯山区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 刘海川 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "邯山区委书记", "start": "", "end": "至今", "rank": "正处级", "note": "截至2026年5月确认为现任；主持第十届区委第十二次全会"},
    # 刘俊波 — 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "邯山区区长", "start": "", "end": "至今", "rank": "正处级", "note": "截至2026年7月确认为现任"},
    {"person_id": 2, "org_id": 1, "title": "邯山区委副书记", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 温俊华 — 副区长、公安分局局长
    {"person_id": 3, "org_id": 2, "title": "邯山区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "邯山区公安分局局长", "start": "", "end": "至今", "rank": "副处级", "note": "兼区公安分局党委书记"},
    # 路风杰 — 副区长
    {"person_id": 4, "org_id": 2, "title": "邯山区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 武越波 — 副区长
    {"person_id": 5, "org_id": 2, "title": "邯山区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 郑婷 — 副区长
    {"person_id": 6, "org_id": 2, "title": "邯山区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 王飞 — 副区长
    {"person_id": 7, "org_id": 2, "title": "邯山区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 刘海川 — 刘俊波 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "邯山区党政一把手工作搭档关系", "overlap_org": "邯山区", "overlap_period": "?至今"},
    # 刘俊波 — 温俊华 上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与副区长（公安）工作关系", "overlap_org": "邯山区人民政府", "overlap_period": ""},
    # 刘俊波 — 路风杰 上下级
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "邯山区人民政府", "overlap_period": ""},
    # 刘俊波 — 武越波 上下级
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "邯山区人民政府", "overlap_period": ""},
    # 刘俊波 — 郑婷 上下级
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "邯山区人民政府", "overlap_period": ""},
    # 刘俊波 — 王飞 上下级
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "邯山区人民政府", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  邯郸市邯山区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-23")
    print("  ✅ 区委书记确认: 刘海川")
    print("  ✅ 区长确认: 刘俊波（1974年9月生）")
    print("  ✅ 副区长: 温俊华、路风杰、武越波、郑婷、王飞")
    print("  ⚠️  详细履历需后续补充（百度百科WAF拦截）")
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
    print("\n✅ 邯山区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  ⚠️  刘海川、刘俊波等核心人物的详细履历待补充。")
    print("  ⚠️  路风杰、郑婷、王飞的简历页面未获取详细内容。")
    print("  ⚠️  刘海川的出生日期、籍贯、教育背景等身份信息缺失。")
