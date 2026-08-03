#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 纳雍县 (Nayong County, Bijie, Guizhou) leadership network.

纳雍县 — 贵州省毕节市辖县, 位于贵州省西北部, 毕节市南部.
Research date: 2026-08. Sources: gznayong.gov.cn official notice (2026-07-03).

This script uses: sqlite3 (via gov_relation.runner), DB_PATH, GEXF_PATH.
"""

import os
import sys
import sqlite3  # noqa: used via gov_relation.runner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, REPO_ROOT
from gov_relation.runner import run_build

SLUG = "纳雍县"
STAGING = REPO_ROOT / "data/tmp/guizhou_纳雍县"
DB_PATH = STAGING / "纳雍县_network.db"
GEXF_PATH = STAGING / "纳雍县_network.gexf"

AS_OF = "2026-08-01"

# ═══════════════════════════════════════════════════════════════════════
# DATA — Source: 纳雍县人民政府门户网站 (www.gznayong.gov.cn)
# 主要来源：2026-07-03 通告《关于公开纳雍县委县政府领导干部分管工作
# 及信访部门相关人员联系方式的通告》
# ═══════════════════════════════════════════════════════════════════════

# ── Persons ──
persons = [
    # ── Core Leaders (Targets) ──
    {
        "id": 1,
        "name": "敖登雪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委书记，贵州纳雍经济开发区党工委书记（兼）",
        "current_org": "中共纳雍县委",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 2,
        "name": "禄斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委副书记、县长、县政府党组书记",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    # ── 县委领导 ──
    {
        "id": 3,
        "name": "张道富",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委副书记",
        "current_org": "中共纳雍县委",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 4,
        "name": "李邮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委副书记（挂职）",
        "current_org": "中共纳雍县委",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 5,
        "name": "李林有",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、宣传部部长",
        "current_org": "中共纳雍县委宣传部",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 6,
        "name": "李劲全",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、统战部部长，县政协党组副书记（兼）",
        "current_org": "中共纳雍县委统战部",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 7,
        "name": "樊顺雄",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、县纪委书记、县监委代理主任",
        "current_org": "中共纳雍县纪委",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 8,
        "name": "潘定科",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、组织部部长",
        "current_org": "中共纳雍县委组织部",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 9,
        "name": "雷彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、政法委书记，县信访局局长（兼）",
        "current_org": "中共纳雍县委政法委",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 10,
        "name": "伍林龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、副县长（分管常务工作）",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 11,
        "name": "刘鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、县人武部政委",
        "current_org": "纳雍县人民武装部",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 12,
        "name": "代思成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、纳雍经开区党工委副书记、管委会副主任，县委办主任",
        "current_org": "贵州纳雍经济开发区",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 13,
        "name": "罗子龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县委常委、副县长（挂职）",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    # ── 政府领导 ──
    {
        "id": 14,
        "name": "林炼深",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人民政府副县长",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 15,
        "name": "罗珍玉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人民政府党组成员、副县长",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 16,
        "name": "安健",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人民政府党组成员、副县长，县公安局党委书记、局长",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 17,
        "name": "马汉波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人民政府党组成员、副县长",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 18,
        "name": "陈森",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人民政府党组成员、副县长",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 19,
        "name": "罗春燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人民政府党组成员",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    {
        "id": 20,
        "name": "戴沙",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人民政府党组成员",
        "current_org": "纳雍县人民政府",
        "source": "gznayong.gov.cn 领导分工通告 (2026-07-03)",
    },
    # ── 人大／政协 ──
    {
        "id": 21,
        "name": "于刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人大常委会主任",
        "current_org": "纳雍县人大常委会",
        "source": "gznayong.gov.cn 新闻报道 (2026-07-31)",
    },
    {
        "id": 22,
        "name": "苏毅",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县政协主席",
        "current_org": "纳雍县政协",
        "source": "gznayong.gov.cn 新闻报道 (2026-07-31)",
    },
    # ── 人武部 ──
    {
        "id": 23,
        "name": "南指革",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "纳雍县人武部部长",
        "current_org": "纳雍县人民武装部",
        "source": "gznayong.gov.cn 新闻报道 (2026-07-31)",
    },
]

# ── Organizations ──
organizations = [
    {
        "id": 1,
        "name": "中共纳雍县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共毕节市委员会",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 2,
        "name": "纳雍县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "毕节市人民政府",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 3,
        "name": "纳雍县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 4,
        "name": "纳雍县政协",
        "type": "政协",
        "level": "县",
        "parent": "",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 5,
        "name": "纳雍县纪委监委",
        "type": "党委",
        "level": "县",
        "parent": "中共纳雍县委员会",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 6,
        "name": "中共纳雍县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共纳雍县委员会",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 7,
        "name": "中共纳雍县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共纳雍县委员会",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 8,
        "name": "中共纳雍县委统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共纳雍县委员会",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 9,
        "name": "中共纳雍县委政法委",
        "type": "党委",
        "level": "县",
        "parent": "中共纳雍县委员会",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 10,
        "name": "贵州纳雍经济开发区",
        "type": "开发区",
        "level": "县",
        "parent": "纳雍县人民政府",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 11,
        "name": "纳雍县人民武装部",
        "type": "政府",
        "level": "县",
        "parent": "",
        "location": "贵州省毕节市纳雍县",
    },
    {
        "id": 12,
        "name": "纳雍县公安局",
        "type": "政府",
        "level": "县",
        "parent": "纳雍县人民政府",
        "location": "贵州省毕节市纳雍县",
    },
]

# ── Positions ──
positions = [
    # 敖登雪
    {"person_id": 1, "org_id": 1, "title": "中共纳雍县委书记", "start": "", "end": "present", "rank": "正县", "note": "主持县委全面工作，兼纳雍经开区党工委书记"},
    # 禄斌
    {"person_id": 2, "org_id": 2, "title": "纳雍县委副书记、县长", "start": "", "end": "present", "rank": "正县", "note": "领导县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "纳雍县委副书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 张道富
    {"person_id": 3, "org_id": 1, "title": "纳雍县委副书记", "start": "", "end": "present", "rank": "副县", "note": "负责县委机关日常工作、农业农村等"},
    # 李邮
    {"person_id": 4, "org_id": 1, "title": "纳雍县委副书记（挂职）", "start": "", "end": "present", "rank": "副县（挂职）", "note": "省政府办公厅派驻乡村振兴工作队"},
    # 李林有
    {"person_id": 5, "org_id": 7, "title": "纳雍县委常委、宣传部部长", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 李劲全
    {"person_id": 6, "org_id": 8, "title": "纳雍县委常委、统战部部长", "start": "", "end": "present", "rank": "副县", "note": "兼县民县宗教事务局局长"},
    {"person_id": 6, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 樊顺雄
    {"person_id": 7, "org_id": 5, "title": "纳雍县委常委、纪委书记、县监委代理主任", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 潘定科
    {"person_id": 8, "org_id": 6, "title": "纳雍县委常委、组织部部长", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 雷彬
    {"person_id": 9, "org_id": 9, "title": "纳雍县委常委、政法委书记", "start": "", "end": "present", "rank": "副县", "note": "兼县信访局局长"},
    {"person_id": 9, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 伍林龙
    {"person_id": 10, "org_id": 2, "title": "纳雍县委常委、常务副县长", "start": "", "end": "present", "rank": "副县", "note": "分管常务工作"},
    {"person_id": 10, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 刘鑫
    {"person_id": 11, "org_id": 11, "title": "纳雍县委常委、人武部政委", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 代思成
    {"person_id": 12, "org_id": 10, "title": "纳雍县委常委、纳雍经开区党工委副书记、管委会副主任", "start": "", "end": "present", "rank": "副县", "note": "分管常务工作"},
    {"person_id": 12, "org_id": 1, "title": "纳雍县委常委、县委办主任", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 罗子龙
    {"person_id": 13, "org_id": 2, "title": "纳雍县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "副县（挂职）", "note": "对接广州天河区对口帮扶"},
    {"person_id": 13, "org_id": 1, "title": "纳雍县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 林炼深
    {"person_id": 14, "org_id": 2, "title": "纳雍县人民政府副县长", "start": "", "end": "present", "rank": "副县", "note": "负责民政、卫生健康、医保、市场监管"},
    # 罗珍玉
    {"person_id": 15, "org_id": 2, "title": "纳雍县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副县", "note": "负责农业农村、林业、乡村振兴等"},
    # 安健
    {"person_id": 16, "org_id": 2, "title": "纳雍县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 16, "org_id": 12, "title": "纳雍县公安局党委书记、局长", "start": "", "end": "present", "rank": "正科", "note": "主持公安局全面工作"},
    # 马汉波
    {"person_id": 17, "org_id": 2, "title": "纳雍县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副县", "note": "负责能源、电力、煤矿安全生产"},
    # 陈森
    {"person_id": 18, "org_id": 2, "title": "纳雍县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副县", "note": "负责交通运输、工信、环保、水利"},
    # 罗春燕
    {"person_id": 19, "org_id": 2, "title": "纳雍县人民政府党组成员", "start": "", "end": "present", "rank": "副县", "note": "负责招商引资、文旅、政务服务"},
    # 戴沙
    {"person_id": 20, "org_id": 2, "title": "纳雍县人民政府党组成员", "start": "", "end": "present", "rank": "副县", "note": "协助农业农村工作"},
    # 于刚
    {"person_id": 21, "org_id": 3, "title": "纳雍县人大常委会主任", "start": "", "end": "present", "rank": "正县", "note": ""},
    # 苏毅
    {"person_id": 22, "org_id": 4, "title": "纳雍县政协主席", "start": "", "end": "present", "rank": "正县", "note": ""},
    # 南指革
    {"person_id": 23, "org_id": 11, "title": "纳雍县人武部部长", "start": "", "end": "present", "rank": "正团", "note": ""},
]

# ── Relationships ──
relationships = [
    # 党政一把手
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长党政一把手搭档关系",
        "overlap_org": "中共纳雍县委常委会",
        "overlap_period": "至2026年8月",
    },
    # 书记与副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与专职副书记上下级",
        "overlap_org": "中共纳雍县委常委会",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与挂职副书记上下级",
        "overlap_org": "中共纳雍县委常委会",
        "overlap_period": "至2026年8月",
    },
    # 县长与副县长
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长与常务副县长上下级",
        "overlap_org": "纳雍县人民政府党组",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "县长与副县长上下级",
        "overlap_org": "纳雍县人民政府",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "县长与女副县长上下级",
        "overlap_org": "纳雍县人民政府",
        "overlap_period": "至2026年8月",
    },
    # 常委间工作交集
    {
        "person_a": 7,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "县纪委书记向县委书记汇报",
        "overlap_org": "中共纳雍县委常委会",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 8,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "组织部部长向县委书记汇报",
        "overlap_org": "中共纳雍县委常委会",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 12,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "县委办主任向县委书记直接汇报",
        "overlap_org": "纳雍县委办公室",
        "overlap_period": "至2026年8月",
    },
    # 公安系统
    {
        "person_a": 16,
        "person_b": 9,
        "type": "overlap",
        "context": "副县长兼公安局长与政法委书记在政法系统协作",
        "overlap_org": "纳雍县政法系统",
        "overlap_period": "至2026年8月",
    },
    # 挂职协作
    {
        "person_a": 4,
        "person_b": 15,
        "type": "overlap",
        "context": "挂职副书记与分管农业副县长协作乡村振兴",
        "overlap_org": "纳雍县乡村振兴工作",
        "overlap_period": "至2026年8月",
    },
    # 经开区团队
    {
        "person_a": 12,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "纳雍经开区日常工作向书记（经开区党工委书记）汇报",
        "overlap_org": "贵州纳雍经济开发区",
        "overlap_period": "至2026年8月",
    },
    # 人大政协与党委
    {
        "person_a": 1,
        "person_b": 21,
        "type": "overlap",
        "context": "县委书记与县人大主任在四家班子中协作",
        "overlap_org": "纳雍县四家班子",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 1,
        "person_b": 22,
        "type": "overlap",
        "context": "县委书记与县政协主席在四家班子中协作",
        "overlap_org": "纳雍县四家班子",
        "overlap_period": "至2026年8月",
    },
    # 军地关系
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县委书记（人武部党委第一书记）与人武部政委",
        "overlap_org": "纳雍县人民武装部",
        "overlap_period": "至2026年8月",
    },
    {
        "person_a": 1,
        "person_b": 23,
        "type": "superior_subordinate",
        "context": "县委书记（人武部党委第一书记）与人武部部长",
        "overlap_org": "纳雍县人民武装部",
        "overlap_period": "至2026年8月",
    },
    # 挂职帮扶
    {
        "person_a": 13,
        "person_b": 15,
        "type": "overlap",
        "context": "挂职副县长与副县长协作广州对口帮扶",
        "overlap_org": "纳雍县对口帮扶工作",
        "overlap_period": "至2026年8月",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"纳雍县级领导班子数据 — 构建SQLite数据库和GEXF图文件")
    print(f"数据来源: 纳雍县人民政府网站 (gznayong.gov.cn)")
    print(f"数据日期: {AS_OF}")
    print(f"人物: {len(persons)}")
    print(f"组织: {len(organizations)}")
    print(f"任职: {len(positions)}")
    print(f"关系: {len(relationships)}")

    run_build(
        slug="纳雍县",
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