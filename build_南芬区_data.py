#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 南芬区, 本溪市, 辽宁省."""

import os
import sys
from datetime import date
from pathlib import Path

# Add project root to path so gov_relation module is importable
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths (staging) ────────────────────────────────────────────────────
TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / "南芬区_network.db"
GEXF_PATH = TMP_DIR / "南芬区_network.gexf"

# ── DATA ───────────────────────────────────────────────────────────────

TODAY = date.today().strftime("%Y-%m-%d")

# ── Persons ────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    # 区委书记 吴建 (confirmed from official site)
    {"id": 1, "name": "吴建", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南芬区委书记", "current_org": "中国共产党本溪市南芬区委员会",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_663826"},

    # 区长 秦学兵 (confirmed from official site)
    {"id": 2, "name": "秦学兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南芬区区长", "current_org": "南芬区人民政府",
     "source": "http://www.nanfen.gov.cn/zwgk/"},

    # ── Deputy Leaders ──
    {"id": 3, "name": "沙莎", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南芬区委常委、副区长", "current_org": "南芬区人民政府",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_663139"},

    {"id": 4, "name": "徐长清", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南芬区副区长", "current_org": "南芬区人民政府",
     "source": "http://www.nanfen.gov.cn/zwgk/"},

    {"id": 5, "name": "李洪", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南芬区副区长", "current_org": "南芬区人民政府",
     "source": "http://www.nanfen.gov.cn/zwgk/"},

    {"id": 6, "name": "王瑞", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南芬区副区长", "current_org": "南芬区人民政府",
     "source": "http://www.nanfen.gov.cn/zwgk/"},

    {"id": 7, "name": "何志伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南芬区副区长", "current_org": "南芬区人民政府",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_658899"},

    # ── Predecessors ──
    {"id": 8, "name": "董培峥", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（前任）南芬区委书记", "current_org": "中国共产党本溪市南芬区委员会（前任）",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_608471"},

    {"id": 9, "name": "张健", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（前前任）南芬区委书记", "current_org": "中国共产党本溪市南芬区委员会（前前任）",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_346764"},

    {"id": 10, "name": "丛茂昆", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（前任）南芬区委副书记、代区长", "current_org": "南芬区人民政府（前任）",
     "source": "http://www.nanfen.gov.cn/publicity/qzfxx/jyta/98628"},

    # ── Historical Leaders ──
    {"id": 11, "name": "王文国", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（历史）南芬区委书记", "current_org": "中国共产党本溪市南芬区委员会（历史）",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_344676"},

    {"id": 12, "name": "王立男", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（历史）南芬区委常委、副区长", "current_org": "南芬区人民政府（历史）",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_587252"},

    {"id": 13, "name": "赵多", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（历史）南芬区委常委、常务副区长", "current_org": "南芬区人民政府（历史）",
     "source": "http://www.nanfen.gov.cn/gzdt/zwyw/content_557999"},
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党本溪市南芬区委员会", "type": "党委",
     "level": "县区级", "parent": "中国共产党本溪市委员会", "location": "辽宁省本溪市南芬区"},
    {"id": 2, "name": "南芬区人民政府", "type": "政府",
     "level": "县区级", "parent": "本溪市人民政府", "location": "辽宁省本溪市南芬区"},
    {"id": 3, "name": "本溪南芬经济开发区", "type": "开发区",
     "level": "县区级", "parent": "南芬区人民政府", "location": "辽宁省本溪市南芬区"},
    {"id": 4, "name": "南芬区审计局", "type": "政府",
     "level": "县区级", "parent": "南芬区人民政府", "location": "辽宁省本溪市南芬区"},
    {"id": 5, "name": "南芬区应急管理局", "type": "政府",
     "level": "县区级", "parent": "南芬区人民政府", "location": "辽宁省本溪市南芬区"},
    {"id": 6, "name": "本溪宏大矿业有限公司", "type": "企业",
     "level": "", "parent": "", "location": "辽宁省本溪市南芬区"},
    {"id": 7, "name": "云新矿业有限公司", "type": "企业",
     "level": "", "parent": "", "location": "辽宁省本溪市南芬区"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 吴建
    {"person_id": 1, "org_id": 1, "title": "南芬区委书记",
     "start": "2026-01", "end": "至今", "rank": "正处级",
     "note": "已见于2026年1月5日公开报道"},
    # 秦学兵
    {"person_id": 2, "org_id": 2, "title": "南芬区区长",
     "start": "2024", "end": "至今", "rank": "正处级",
     "note": "主持区政府全面工作，负责经开区、招商、审计"},
    {"person_id": 2, "org_id": 3, "title": "负责本溪南芬经济开发区",
     "start": "", "end": "", "rank": "",
     "note": "区长分工中明确负责经开区"},
    {"person_id": 2, "org_id": 4, "title": "分管区审计局",
     "start": "", "end": "", "rank": "",
     "note": "区长分工中明确分管审计"},
    # 沙莎
    {"person_id": 3, "org_id": 2, "title": "南芬区委常委、副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": "2026年6月陪同区长检查矿山安全"},
    # 徐长清
    {"person_id": 4, "org_id": 2, "title": "南芬区副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": "多次参与调研和招商"},
    # 李洪
    {"person_id": 5, "org_id": 2, "title": "南芬区副区长",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    # 王瑞
    {"person_id": 6, "org_id": 2, "title": "南芬区副区长",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    # 何志伟
    {"person_id": 7, "org_id": 2, "title": "南芬区副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": "多次陪同吴建和秦学兵调研"},
    # 董培峥
    {"person_id": 8, "org_id": 1, "title": "南芬区委书记（前任）",
     "start": "2023", "end": "2025", "rank": "正处级",
     "note": "2023-2024年多次以区委书记身份公开活动"},
    # 张健
    {"person_id": 9, "org_id": 1, "title": "南芬区委书记（前前任）",
     "start": "2017", "end": "2022", "rank": "正处级",
     "note": "2017年有公开报道"},
    # 丛茂昆
    {"person_id": 10, "org_id": 2, "title": "南芬区委副书记、代区长",
     "start": "2021", "end": "2023", "rank": "正处级",
     "note": "2021年12月以代区长身份主持会议"},
    # 王文国
    {"person_id": 11, "org_id": 1, "title": "南芬区委书记（历史）",
     "start": "2015", "end": "2016", "rank": "正处级",
     "note": "2015-2016年有公开报道"},
    # 王立男
    {"person_id": 12, "org_id": 2, "title": "南芬区委常委、副区长（历史）",
     "start": "2022", "end": "", "rank": "副处级",
     "note": "2022年11月有公开报道"},
    # 赵多
    {"person_id": 13, "org_id": 2, "title": "南芬区委常委、常务副区长（历史）",
     "start": "2021", "end": "", "rank": "副处级",
     "note": "2021年12月有公开报道"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # 吴建 ↔ 秦学兵 (党政正职)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长，搭建区委、区政府党政正职配合",
     "overlap_org": "南芬区", "overlap_period": "2026-至今"},
    # 吴建 → 董培峥 (前后任)
    {"person_a": 1, "person_b": 8, "type": "predecessor_successor",
     "context": "吴建接任董培峥的南芬区委书记职务",
     "overlap_org": "中国共产党本溪市南芬区委员会",
     "overlap_period": "接任"},
    # 吴建 ↔ 何志伟 (上下级)
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "副区长何志伟多次陪同区委书记吴建调研",
     "overlap_org": "南芬区", "overlap_period": "2026"},
    # 吴建 ↔ 沙莎 (上下级)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委常委、副区长沙莎在区委领导下工作",
     "overlap_org": "南芬区", "overlap_period": "2026"},
    # 秦学兵 ↔ 沙莎 (上下级)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "副区长沙莎在区长领导下工作",
     "overlap_org": "南芬区人民政府", "overlap_period": "2026"},
    # 秦学兵 ↔ 何志伟 (上下级)
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "副区长何志伟在区长领导下工作",
     "overlap_org": "南芬区人民政府", "overlap_period": "2026"},
    # 秦学兵 → 丛茂昆 (前后任区长)
    {"person_a": 2, "person_b": 10, "type": "predecessor_successor",
     "context": "丛茂昆曾任南芬区委副书记、代区长，秦学兵接任区长",
     "overlap_org": "南芬区人民政府",
     "overlap_period": "接任"},
    # 秦学兵 ↔ 徐长清 (上下级)
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "副区长徐长清在区长领导下工作",
     "overlap_org": "南芬区人民政府", "overlap_period": "2022-2026"},
    # 董培峥 → 张健 (前后任)
    {"person_a": 8, "person_b": 9, "type": "predecessor_successor",
     "context": "董培峥接任张健的南芬区委书记职务",
     "overlap_org": "中国共产党本溪市南芬区委员会",
     "overlap_period": "接任"},
    # 丛茂昆 ↔ 赵多 (同事)
    {"person_a": 10, "person_b": 13, "type": "overlap",
     "context": "代区长丛茂昆与常务副区长赵多同期任职",
     "overlap_org": "南芬区人民政府",
     "overlap_period": "2021"},
]

# ── Run Build ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="南芬区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
