#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 威宁彝族回族苗族自治县 (Weining, Bijie, Guizhou) leadership network.

威宁彝族回族苗族自治县 — 贵州省毕节市辖自治县, 位于贵州省西北部, 乌蒙山腹地, 是贵州面积最大的县.
Research date: 2026-08. Sources: gzweining.gov.cn (official), bijie.gov.cn (parent city), 县领导之窗.

This script uses: sqlite3 (via gov_relation.runner), DB_PATH, GEXF_PATH.
Partial Evidence Mode: 县委书记胡敬斌/县长邓林身份与现任班子的官方确认已取得; 二人早年履历与前任去向待补.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.paths import REPO_ROOT
from gov_relation.runner import run_build

SLUG = "威宁彝族回族苗族自治县"
STAGING = REPO_ROOT / "data/tmp/guizhou_威宁彝族回族苗族自治县"
DB_PATH = STAGING / "威宁彝族回族苗族自治县_network.db"
GEXF_PATH = STAGING / "威宁彝族回族苗族自治县_network.gexf"

AS_OF = "2026-08-01"

# ═══════════════════════════════════════════════════════════════════════
# DATA — Source: 威宁彝族回族苗族自治县人民政府门户 (www.gzweining.gov.cn)
# 主要来源：
#  - 2026-06-17 官方会议报道《全县树立和践行正确政绩观学习教育党政"一把手"
#    带头推动整改整治会议召开》→ 现任四大班子名单（胡敬斌/邓林/杨华忠/王凤雏等）
#  - 领导之窗·自治县政府领导专栏 → 县政府班子与履历
#  - 毕节市人民政府门户 (bijie.gov.cn) → 父市背景
# ═══════════════════════════════════════════════════════════════════════

# ── Persons ──
persons = [
    # ── Core Leaders (Targets) ──
    {
        "id": 1,
        "name": "胡敬斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁自治县委书记、县委党的建设工作领导小组组长",
        "current_org": "中共威宁彝族回族苗族自治县委",
        "source": "gzweining.gov.cn 官方会议报道 (2026-06-17)",
    },
    {
        "id": 2,
        "name": "邓林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁自治县委副书记、自治县县长",
        "current_org": "威宁彝族回族苗族自治县人民政府",
        "source": "gzweining.gov.cn 官方会议报道 (2026-06-17)",
    },
    # ── 县委领导 ──
    {
        "id": 3,
        "name": "陈江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁自治县委副书记",
        "current_org": "中共威宁彝族回族苗族自治县委",
        "source": "gzweining.gov.cn 官方会议报道 (2026-06-17)",
    },
    {
        "id": 4,
        "name": "吕刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁自治县委副书记",
        "current_org": "中共威宁彝族回族苗族自治县委",
        "source": "gzweining.gov.cn 官方会议报道 (2026-06-17)",
    },
    # ── 县政府领导 ──
    {
        "id": 5,
        "name": "李永红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "贵州毕节七星关",
        "education": "大学",
        "party_join": "2000-06",
        "work_start": "2000-09",
        "current_post": "威宁自治县委常委、常务副县长、县政府党组副书记",
        "current_org": "威宁彝族回族苗族自治县人民政府",
        "source": "gzweining.gov.cn 领导之窗 (2025-03)",
    },
    {
        "id": 6,
        "name": "汤宗飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "湖北赤壁",
        "education": "中央党校大学",
        "party_join": "1995-04",
        "work_start": "1990-12",
        "current_post": "威宁县政府副县长（挂职）",
        "current_org": "威宁彝族回族苗族自治县人民政府",
        "source": "gzweining.gov.cn 领导之窗 (2025-03)",
    },
    {
        "id": 7,
        "name": "赵诗惠",
        "gender": "女",
        "ethnicity": "白族",
        "birth": "1970-12",
        "birthplace": "贵州黔西",
        "education": "西南政法大学法学专业（在职）",
        "party_join": "",
        "work_start": "1992-08",
        "current_post": "威宁县政府副县长",
        "current_org": "威宁彝族回族苗族自治县人民政府",
        "source": "gzweining.gov.cn 领导之窗 (2025-03)",
    },
    {
        "id": 8,
        "name": "高占武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁县政府党组成员、副县长",
        "current_org": "威宁彝族回族苗族自治县人民政府",
        "source": "gzweining.gov.cn 领导之窗 (2026-02)",
    },
    {
        "id": 9,
        "name": "段雨祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-01",
        "birthplace": "贵州六盘水水城县",
        "education": "",
        "party_join": "2007-12",
        "work_start": "2011-10",
        "current_post": "威宁县政府副县长",
        "current_org": "威宁彝族回族苗族自治县人民政府",
        "source": "gzweining.gov.cn 领导之窗 (2025-03)",
    },
    {
        "id": 10,
        "name": "雷建文",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1982-07",
        "birthplace": "贵州织金",
        "education": "贵州省委党校法律专业",
        "party_join": "2008-08",
        "work_start": "2004-09",
        "current_post": "威宁县政府副县长、县公安局党委书记、局长",
        "current_org": "威宁彝族回族苗族自治县公安局",
        "source": "gzweining.gov.cn 领导之窗 (2025-03)",
    },
    {
        "id": 11,
        "name": "苏云飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁县政府党组成员、副县长",
        "current_org": "威宁彝族回族苗族自治县人民政府",
        "source": "gzweining.gov.cn 领导之窗 (2025-03)",
    },
    # ── 人大／政协 ──
    {
        "id": 12,
        "name": "杨华忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁自治县人大常委会主任",
        "current_org": "威宁彝族回族苗族自治县人大常委会",
        "source": "gzweining.gov.cn 官方会议报道 (2026-06-17)",
    },
    {
        "id": 13,
        "name": "王凤雏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "威宁自治县政协主席",
        "current_org": "中国人民政治协商会议威宁彝族回族苗族自治县委员会",
        "source": "gzweining.gov.cn 官方会议报道 (2026-06-17)",
    },
]

# ── Organizations ──
organizations = [
    {
        "id": 1,
        "name": "中共威宁彝族回族苗族自治县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共毕节市委员会",
        "location": "贵州省毕节市威宁彝族回族苗族自治县",
    },
    {
        "id": 2,
        "name": "威宁彝族回族苗族自治县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "毕节市人民政府",
        "location": "贵州省毕节市威宁彝族回族苗族自治县",
    },
    {
        "id": 3,
        "name": "威宁彝族回族苗族自治县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "",
        "location": "贵州省毕节市威宁彝族回族苗族自治县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议威宁彝族回族苗族自治县委员会",
        "type": "政协",
        "level": "县",
        "parent": "",
        "location": "贵州省毕节市威宁彝族回族苗族自治县",
    },
    {
        "id": 5,
        "name": "威宁彝族回族苗族自治县公安局",
        "type": "政府",
        "level": "县",
        "parent": "威宁彝族回族苗族自治县人民政府",
        "location": "贵州省毕节市威宁彝族回族苗族自治县",
    },
]

# ── Positions ──
positions = [
    # 胡敬斌
    {"person_id": 1, "org_id": 1, "title": "威宁自治县委书记", "start": "", "end": "present", "rank": "正县", "note": "主持县委全面工作，兼县委党的建设工作领导小组组长"},
    # 邓林
    {"person_id": 2, "org_id": 2, "title": "威宁自治县县长", "start": "", "end": "present", "rank": "正县", "note": "领导县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "威宁自治县委副书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 陈江
    {"person_id": 3, "org_id": 1, "title": "威宁自治县委副书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 吕刚
    {"person_id": 4, "org_id": 1, "title": "威宁自治县委副书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 李永红
    {"person_id": 5, "org_id": 2, "title": "威宁县政府党组副书记、常务副县长", "start": "", "end": "present", "rank": "副县", "note": "协助县长负责审计、粮食、草海保护等"},
    {"person_id": 5, "org_id": 1, "title": "威宁县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 汤宗飞
    {"person_id": 6, "org_id": 2, "title": "威宁县政府副县长（挂职）", "start": "", "end": "present", "rank": "副县（挂职）", "note": ""},
    # 赵诗惠
    {"person_id": 7, "org_id": 2, "title": "威宁县政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 高占武
    {"person_id": 8, "org_id": 2, "title": "威宁县政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 段雨祥
    {"person_id": 9, "org_id": 2, "title": "威宁县政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 雷建文
    {"person_id": 10, "org_id": 2, "title": "威宁县政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "威宁县公安局党委书记、局长", "start": "", "end": "present", "rank": "正科", "note": "主持公安工作"},
    # 苏云飞
    {"person_id": 11, "org_id": 2, "title": "威宁县政府党组成员、副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 杨华忠
    {"person_id": 12, "org_id": 3, "title": "威宁自治县人大常委会主任", "start": "", "end": "present", "rank": "正县", "note": ""},
    # 王凤雏
    {"person_id": 13, "org_id": 4, "title": "威宁自治县政协主席", "start": "", "end": "present", "rank": "正县", "note": ""},
]

# ── Relationships ──
relationships = [
    # 党政一把手
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政一把手搭档关系",
        "overlap_org": "中共威宁自治县委常委会、威宁县四家班子",
        "overlap_period": "至2026年8月",
    },
    # 书记与副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与专职副书记上下级",
        "overlap_org": "中共威宁自治县委常委会",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与专职副书记上下级",
        "overlap_org": "中共威宁自治县委常委会",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "县长与县委副书记在县委常委会共事",
        "overlap_org": "中共威宁自治县委常委会",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "县长与县委副书记在县委常委会共事",
        "overlap_org": "中共威宁自治县委常委会",
        "overlap_period": "至2026年8月",
    },
    # 县长与政府班子
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与常务副县长上下级",
        "overlap_org": "威宁县人民政府党组",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与挂职副县长上下级",
        "overlap_org": "威宁县人民政府",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与女副县长上下级",
        "overlap_org": "威宁县人民政府",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长与副县长兼公安局长上下级",
        "overlap_org": "威宁县人民政府",
        "overlap_period": "至2026年8月",
    },
    # 常务与副县长同班子
    {
        "person_a": 5,
        "person_b": 8,
        "type": "overlap",
        "context": "常务副县长与副县长同政府班子",
        "overlap_org": "威宁县人民政府",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 5,
        "person_b": 9,
        "type": "overlap",
        "context": "常务副县长与副县长同政府班子",
        "overlap_org": "威宁县人民政府",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 5,
        "person_b": 11,
        "type": "overlap",
        "context": "常务副县长与副县长同政府班子",
        "overlap_org": "威宁县人民政府",
        "overlap_period": "至2026年8月",
    },
    # 公安系统
    {
        "person_a": 10,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "副县长兼公安局长接受县委书记领导",
        "overlap_org": "威宁县政法系统",
        "overlap_period": "至2026年8月",
    },
    # 人大政协与党委
    {
        "person_a": 1,
        "person_b": 12,
        "type": "overlap",
        "context": "县委书记与县人大主任在四家班子中协作",
        "overlap_org": "威宁县四家班子",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 1,
        "person_b": 13,
        "type": "overlap",
        "context": "县委书记与县政协主席在四家班子中协作",
        "overlap_org": "威宁县四家班子",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "overlap",
        "context": "县长与县人大主任在四家班子中协作",
        "overlap_org": "威宁县四家班子",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "overlap",
        "context": "县长与县政协主席在四家班子中协作",
        "overlap_org": "威宁县四家班子",
        "overlap_period": "至2026年8月",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"威宁彝族回族苗族自治县领导班子数据 — 构建SQLite数据库和GEXF图文件")
    print(f"数据来源: 威宁自治县人民政府网站 (gzweining.gov.cn)")
    print(f"数据日期: {AS_OF}")
    print(f"人物: {len(persons)}")
    print(f"组织: {len(organizations)}")
    print(f"任职: {len(positions)}")
    print(f"关系: {len(relationships)}")

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

    print(f"\n✅ 数据库: {DB_PATH}")
    print(f"✅ GEXF图: {GEXF_PATH}")