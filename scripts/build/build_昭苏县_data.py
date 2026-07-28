#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 昭苏县 (Zhaosu County) leadership network.

Data sources (all official from zhaosu.gov.cn):
- 领导之窗 page: https://www.zhaosu.gov.cn/zsx/c113849/leader_list.shtml (accessed 2026-07-28)
- Individual leader profile pages (detailed bios with education, work start, etc.)
- News articles on zhaosu.gov.cn listing additional party committee leaders

Confidence levels:
- confirmed = official government source
- plausible = cross-referenced news reports/indirect evidence
- unverified = insufficient corroboration
"""

import os
import sqlite3
import sys
from pathlib import Path

_script_path = Path(__file__).resolve()
# data/tmp/xinjiang_昭苏县/build_昭苏县_data.py -> 4 levels up to repo root
_repo_root = _script_path.parents[3]
sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build

# ── SLUG ──────────────────────────────────────────────────────────────────

SLUG = "昭苏县"

# ── PATHS ─────────────────────────────────────────────────────────────────

STAGING_DIR = _repo_root / "data/tmp/xinjiang_昭苏县"
DB_PATH = STAGING_DIR / "昭苏县_network.db"
GEXF_PATH = STAGING_DIR / "昭苏县_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# PERSONS
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "何江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "昭苏县委书记",
        "current_org": "中共昭苏县委员会",
        "source": "www.zhaosu.gov.cn 新闻 (2026-07-21 1356发展路径推进会; 2026-07-02 七一慰问)",
    },
    {
        "id": 2,
        "name": "海拉提·阿里木",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1981年1月",
        "birthplace": "待查",
        "education": "大学（新疆农业大学草业科学专业）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "昭苏县委副书记、代县长",
        "current_org": "昭苏县人民政府",
        "source": "https://www.zhaosu.gov.cn/zsx/c113849/202306/6199464e31ec4caeb461b47352da614d.shtml",
    },
    # ── Key Deputies ─────────────────────────────────────────────────────
    {
        "id": 3,
        "name": "樊剑章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年5月",
        "birthplace": "新疆奎屯",
        "education": "全日制研究生学历（新疆大学化学化工学院化学工程与技术专业）",
        "party_join": "中共党员",
        "work_start": "2013年7月",
        "current_post": "昭苏县委常委、常务副县长候选人",
        "current_org": "昭苏县人民政府",
        "source": "https://www.zhaosu.gov.cn/zsx/c113849/202306/4a7b3e5a4703427b85183bc598f42325.shtml",
    },
    {
        "id": 4,
        "name": "周明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "江苏泰兴",
        "education": "大学（2008年6月东南大学交通工程专业）",
        "party_join": "中共党员",
        "work_start": "2008年7月",
        "current_post": "昭苏县委常委、副县长、第十二批泰州援疆工作组副组长",
        "current_org": "昭苏县人民政府",
        "source": "https://www.zhaosu.gov.cn/zsx/c113849/202306/ca8115c60940435981868ac9e57640c0.shtml",
    },
    {
        "id": 5,
        "name": "帕提曼·夏力甫汗",
        "gender": "女",
        "ethnicity": "哈萨克族",
        "birth": "1976年9月",
        "birthplace": "新疆察布查尔县",
        "education": "大学（1999年7月新疆农业大学林学专业）",
        "party_join": "中共党员",
        "work_start": "1999年11月",
        "current_post": "昭苏县政府党组成员、副县长",
        "current_org": "昭苏县人民政府",
        "source": "https://www.zhaosu.gov.cn/zsx/c113849/202306/8b4079c2c06c43f7929d05ea4b303e92.shtml",
    },
    {
        "id": 6,
        "name": "热孜万古力·亚尔买买提",
        "gender": "女",
        "ethnicity": "维吾尔族",
        "birth": "1972年11月",
        "birthplace": "新疆伊犁",
        "education": "在职大学（四川大学继续教育学院行政管理专业）",
        "party_join": "中共党员",
        "work_start": "1995年4月",
        "current_post": "昭苏县人民政府副县长",
        "current_org": "昭苏县人民政府",
        "source": "https://www.zhaosu.gov.cn/zsx/c113849/202306/c2827f4754954680abacaf2ac8e573a5.shtml",
    },
    {
        "id": 7,
        "name": "范伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年8月",
        "birthplace": "四川西充",
        "education": "中央广播电视大学法学专业",
        "party_join": "中共党员",
        "work_start": "2009年8月",
        "current_post": "昭苏县人民政府副县长人选",
        "current_org": "昭苏县人民政府",
        "source": "https://www.zhaosu.gov.cn/zsx/c113849/202306/210bde87112746b4983cfa7646389fc4.shtml",
    },
    # ── Other Leaders (from news articles on zhaosu.gov.cn) ─────────────
    {
        "id": 8,
        "name": "施康振",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭苏县委领导",
        "current_org": "中共昭苏县委员会",
        "source": "zhaosu.gov.cn news articles (2026-06-18 livestock competition; 2026-07-16 convention)",
    },
    {
        "id": 9,
        "name": "夏徽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭苏县委常委、副县长（挂职）",
        "current_org": "昭苏县人民政府",
        "source": "zhaosu.gov.cn news (2026-06-26, 2026-07-24 articles)",
    },
    {
        "id": 10,
        "name": "加依娜·跃进",
        "gender": "女",
        "ethnicity": "哈萨克族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭苏县委常委、宣传部部长",
        "current_org": "中共昭苏县委员会",
        "source": "zhaosu.gov.cn news (2026-07-02 fair conduct inspection; 2026-06-26 article)",
    },
    {
        "id": 11,
        "name": "高辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭苏县人大党组书记、副主任",
        "current_org": "昭苏县人民代表大会常务委员会",
        "source": "zhaosu.gov.cn news (2026-07-02, 2026-07-01 convention and visit articles)",
    },
    {
        "id": 12,
        "name": "努尔古丽·居马德力",
        "gender": "女",
        "ethnicity": "哈萨克族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭苏县人大常委会主任",
        "current_org": "昭苏县人民代表大会常务委员会",
        "source": "zhaosu.gov.cn news (2026-07-02 fair conduct inspection article)",
    },
    {
        "id": 13,
        "name": "波拉提江·哈布里",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭苏县领导",
        "current_org": "中共昭苏县委员会",
        "source": "zhaosu.gov.cn news (2026-07-01 livestock improvement article)",
    },
    {
        "id": 14,
        "name": "尼木加甫·巴音得尔格",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭苏县政府党组成员",
        "current_org": "昭苏县人民政府",
        "source": "zhaosu.gov.cn news (2026-07-16 enterprise research article)",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共昭苏县委员会", "type": "党委", "level": "县处级", "parent": "中共伊犁哈萨克自治州委员会", "location": "昭苏县"},
    {"id": 2, "name": "昭苏县人民政府", "type": "政府", "level": "县处级", "parent": "伊犁哈萨克自治州人民政府", "location": "昭苏县"},
    {"id": 3, "name": "昭苏县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "昭苏县", "location": "昭苏县"},
    {"id": 4, "name": "中国人民政治协商会议昭苏县委员会", "type": "政协", "level": "县处级", "parent": "昭苏县", "location": "昭苏县"},
    {"id": 5, "name": "中共昭苏县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "昭苏县", "location": "昭苏县"},
    {"id": 6, "name": "中共伊犁哈萨克自治州委员会", "type": "党委", "level": "地厅级", "parent": "中国共产党新疆维吾尔自治区委员会", "location": "伊宁市"},
    {"id": 7, "name": "伊犁哈萨克自治州人民政府", "type": "政府", "level": "地厅级", "parent": "新疆维吾尔自治区人民政府", "location": "伊宁市"},
    {"id": 8, "name": "泰州市人民政府", "type": "政府", "level": "地厅级", "parent": "江苏省人民政府", "location": "江苏省泰州市"},
]

# ═══════════════════════════════════════════════════════════════════════════
# POSITIONS
# ═══════════════════════════════════════════════════════════════════════════

positions = [
    # Top leaders
    {"person_id": 1, "org_id": 1, "title": "昭苏县委书记",
     "start_date": "待查", "end_date": "至今", "rank": "正处级",
     "note": "主持县委全面工作; confirmed active as of 2026-07-21"},
    {"person_id": 2, "org_id": 2, "title": "昭苏县委副书记、代县长",
     "start_date": "待查（profile updated 2026-06-02）", "end_date": "至今", "rank": "正处级",
     "note": "主持县政府全面工作"},

    # Government leadership team
    {"person_id": 3, "org_id": 2, "title": "昭苏县委常委、常务副县长候选人",
     "start_date": "待查（profile published 2026-05-18）", "end_date": "至今", "rank": "副处级",
     "note": "待人大常委会任命"},
    {"person_id": 4, "org_id": 2, "title": "昭苏县委常委、副县长、第十二批泰州援疆工作组副组长",
     "start_date": "待查（profile published 2026-05-18）", "end_date": "至今", "rank": "副处级",
     "note": "江苏泰州援疆干部"},
    {"person_id": 5, "org_id": 2, "title": "昭苏县政府党组成员、副县长",
     "start_date": "待查（profile published 2026-05-18）", "end_date": "至今", "rank": "副处级",
     "note": ""},
    {"person_id": 6, "org_id": 2, "title": "昭苏县人民政府副县长",
     "start_date": "待查（profile published 2026-05-18）", "end_date": "至今", "rank": "副处级",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "昭苏县人民政府副县长人选",
     "start_date": "待查（profile published 2026-05-18）", "end_date": "至今", "rank": "副处级",
     "note": "待人大任命"},

    # Other party/government leaders (dates unknown)
    {"person_id": 8, "org_id": 1, "title": "昭苏县领导",
     "start_date": "待查", "end_date": "至今", "rank": "副处级",
     "note": "在新闻报道中出现; likely 县委副书记或副县长"},
    {"person_id": 9, "org_id": 2, "title": "昭苏县委常委、副县长（挂职）",
     "start_date": "待查", "end_date": "至今", "rank": "副处级",
     "note": "挂职干部"},
    {"person_id": 10, "org_id": 1, "title": "昭苏县委常委、宣传部部长",
     "start_date": "待查", "end_date": "至今", "rank": "副处级",
     "note": ""},
    {"person_id": 11, "org_id": 3, "title": "昭苏县人大党组书记、副主任",
     "start_date": "待查", "end_date": "至今", "rank": "正处级",
     "note": ""},
    {"person_id": 12, "org_id": 3, "title": "昭苏县人大常委会主任",
     "start_date": "待查", "end_date": "至今", "rank": "正处级",
     "note": ""},
    {"person_id": 13, "org_id": 1, "title": "昭苏县领导",
     "start_date": "待查", "end_date": "至今", "rank": "",
     "note": ""},
    {"person_id": 14, "org_id": 2, "title": "昭苏县政府党组成员",
     "start_date": "待查", "end_date": "至今", "rank": "副处级",
     "note": ""},
]

# ═══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════════════

relationships = [
    # Core leadership team interactions
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与代县长搭班领导昭苏县",
     "overlap_org": "昭苏县",
     "overlap_period": "2025/2026至今",
     "confidence": "confirmed"},

    # Government team overlaps
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "代县长与常务副县长候选人同在一届政府班子",
     "overlap_org": "昭苏县人民政府",
     "overlap_period": "2026至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "代县长与援疆副县长同在一届政府班子",
     "overlap_org": "昭苏县人民政府",
     "overlap_period": "2026至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "代县长与副县长同在一届政府班子",
     "overlap_org": "昭苏县人民政府",
     "overlap_period": "2026至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "代县长与副县长同在一届政府班子",
     "overlap_org": "昭苏县人民政府",
     "overlap_period": "2026至今",
     "confidence": "confirmed"},

    # Party committee overlaps
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与宣传部长同属县委常委会",
     "overlap_org": "中共昭苏县委员会",
     "overlap_period": "2025/2026至今",
     "confidence": "confirmed"},

    # Cross-government and party committee
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与县委常委（挂职副县长）同属县委常委会",
     "overlap_org": "中共昭苏县委员会",
     "overlap_period": "2025/2026至今",
     "confidence": "confirmed"},

    # County People's Congress
    {"person_a": 11, "person_b": 12, "type": "overlap",
     "context": "县人大党组书记（副主任）与人大常委会主任同属人大班子",
     "overlap_org": "昭苏县人民代表大会常务委员会",
     "overlap_period": "2026至今",
     "confidence": "plausible"},

    # News-confirmed relationships
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "同时在2026-07-01走访慰问活动出席",
     "overlap_org": "昭苏县",
     "overlap_period": "2026至今",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "同时在2026-07-02相关工作检查出席",
     "overlap_org": "昭苏县",
     "overlap_period": "2026至今",
     "confidence": "confirmed"},
]

# ═══════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(str(STAGING_DIR), exist_ok=True)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
    )
    print(f"\nDone. Files written to {STAGING_DIR}/")