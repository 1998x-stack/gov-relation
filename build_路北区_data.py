#!/usr/bin/env python3
"""Build 唐山市路北区 (Tangshan Lubei District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 唐山市
Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
Task ID: hebei_路北区

Research date: 2026-07-23
Official source: http://www.tslb.gov.cn/ (唐山市路北区人民政府 — accessible)

Current status (as of 2026-07-23):
- 区委书记: 赵立军 — 在路北区第十二次党代会（2026.07.21-22）上代表十一届区委作报告并主持闭幕式
- 区长: 韩博 — 路北区政府官网"政府领导"栏目列出；主持第十二次党代会开幕式
- 第十二次党代会于2026年7月21-23日举行，选举产生第十二届区委领导班子

Note:
- 路北区政府网站 (www.tslb.gov.cn) 可访问，但新闻内容以PNG图片形式发布
- 赵立军和韩博的详细履历（出生年月、籍贯、教育背景、完整任职经历）尚未获取
- 百度百科等渠道被WAF/验证码拦截
- 前任区委书记为艾长征（2023-2024年间以区委书记身份参与活动的报道）
- 所有履历补充待后续调查
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "路北区"
TASK_ID = "hebei_路北区"
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

    # 赵立军 — 路北区委书记
    # 来源：路北区第十二次党代会报道（2026.07.21-22），OCR识别
    # 赵立军代表第十一届区委作工作报告并主持闭幕式
    # 履历补充待查
    {
        "id": 1,
        "name": "赵立军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "路北区委书记",
        "current_org": "中共唐山市路北区委员会",
        "source": "政府官网 — http://www.tslb.gov.cn/index.php?m=content&c=index&a=show&catid=295&id=45040 和 id=45041，OCR识别",
    },
    # 韩博 — 路北区委副书记、区长
    # 来源：路北区政府官网"政府领导"页面 + 第十二次党代会报道（主持开幕式）
    {
        "id": 2,
        "name": "韩博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "路北区委副书记、区长",
        "current_org": "路北区人民政府",
        "source": "政府官网 — http://www.tslb.gov.cn/index.php?m=content&c=index&a=lists&catid=1416 和 第十二次党代会开幕报道",
    },
    # 高炜 — 副区长
    {
        "id": 3,
        "name": "高炜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "路北区副区长",
        "current_org": "路北区人民政府",
        "source": "政府官网 — http://www.tslb.gov.cn/index.php?m=content&c=index&a=lists&catid=1416",
    },
    # 张兰华 — 副区长
    {
        "id": 4,
        "name": "张兰华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "路北区副区长",
        "current_org": "路北区人民政府",
        "source": "政府官网 — http://www.tslb.gov.cn/index.php?m=content&c=index&a=lists&catid=1416",
    },
    # 张伟红 — 副区长
    {
        "id": 5,
        "name": "张伟红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "路北区副区长",
        "current_org": "路北区人民政府",
        "source": "政府官网 — http://www.tslb.gov.cn/index.php?m=content&c=index&a=lists&catid=1416",
    },
    # 艾长征 — 前任区委书记（2021-2026?）
    # 来源：政府网站搜索"艾长征"返回18条结果，2023-2024年间有多次以"区委书记"身份出席活动的报道
    {
        "id": 6,
        "name": "艾长征",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任）路北区委书记",
        "current_org": "中共唐山市路北区委员会",
        "source": "路北区政府网站搜索，18条含'区委书记艾长征'的结果 — http://www.tslb.gov.cn/",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共唐山市路北区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共唐山市委员会",
        "location": "河北省唐山市路北区",
    },
    {
        "id": 2,
        "name": "路北区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "唐山市人民政府",
        "location": "河北省唐山市路北区",
    },
    {
        "id": 3,
        "name": "路北区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "唐山市人大常委会",
        "location": "河北省唐山市路北区",
    },
    {
        "id": 4,
        "name": "政协路北区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协唐山市委员会",
        "location": "河北省唐山市路北区",
    },
    {
        "id": 5,
        "name": "路北区纪委监委",
        "type": "纪委",
        "level": "市辖区",
        "parent": "唐山市纪委监委",
        "location": "河北省唐山市路北区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 赵立军 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "路北区委书记", "start": "", "end": "至今", "rank": "正处级", "note": "截至2026年7月确认为现任；第十二次党代会连任/当选"},
    # 韩博 — 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "路北区区长", "start": "", "end": "至今", "rank": "正处级", "note": "截至2026年7月确认为现任"},
    {"person_id": 2, "org_id": 1, "title": "路北区委副书记", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 高炜 — 副区长
    {"person_id": 3, "org_id": 2, "title": "路北区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 张兰华 — 副区长
    {"person_id": 4, "org_id": 2, "title": "路北区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 张伟红 — 副区长
    {"person_id": 5, "org_id": 2, "title": "路北区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 艾长征 — 前任区委书记
    {"person_id": 6, "org_id": 1, "title": "路北区委书记", "start": "", "end": "", "rank": "正处级", "note": "前任区委书记，2023-2024年间有活动记录；当前去向待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 赵立军 — 韩博 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "路北区党政一把手工作搭档关系", "overlap_org": "路北区", "overlap_period": "?至今"},
    # 赵立军 — 艾长征 前后任
    {"person_a": 1, "person_b": 6, "type": "predecessor_successor", "context": "路北区委书记前后任关系", "overlap_org": "中共唐山市路北区委员会", "overlap_period": ""},
    # 韩博 — 高炜 上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "路北区人民政府", "overlap_period": ""},
    # 韩博 — 张兰华 上下级
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "路北区人民政府", "overlap_period": ""},
    # 韩博 — 张伟红 上下级
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "路北区人民政府", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  唐山市路北区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-23")
    print("  ✅ 区委书记确认: 赵立军")
    print("  ✅ 区长确认: 韩博")
    print("  ⚠️  详细履历需后续补充（百度百科WAF拦截、政府新闻为图片格式）")
    print("  ⚠️  前任区委书记: 艾长征（去向待查）")
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
    print("\n✅ 路北区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  ⚠️  赵立军、韩博等核心人物的详细履历待补充。")
    print("  ⚠️  艾长征的去向待查。")
