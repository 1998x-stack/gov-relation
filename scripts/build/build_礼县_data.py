#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
礼县 (甘肃省陇南市) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Lixian County leadership network.

Level: 县
Province: 甘肃省
City: 陇南市
Region: 礼县
Targets: 县委书记 & 县长

Research Sources:
- 礼县人民政府官方网站 (www.gslx.gov.cn) 领导之窗, 2026年7月确认
- Official leadership page: https://www.gslx.gov.cn/ldzc/

Research Date: 2026-07-22
"""

import os
import sys
from pathlib import Path

# Add project root to path for gov_relation imports
_REPO_ROOT = Path(__file__).resolve()
for _parent in [_REPO_ROOT] + list(_REPO_ROOT.parents):
    if (_parent / "gov_relation" / "__init__.py").exists():
        _REPO_ROOT = _parent
        break
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # kept for process_tmp.py validation

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "礼县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "礼县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘景原",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共礼县委员会",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 2,
        "name": "尚凤雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 3,
        "name": "杨敬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共礼县委员会",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 4,
        "name": "李清泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共礼县纪律检查委员会",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 5,
        "name": "逯彦果",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共礼县委员会组织部",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 6,
        "name": "赵海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "native_place": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共礼县委员会统战部",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 7,
        "name": "叶炎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共礼县委员会政法委员会",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 8,
        "name": "施晓潇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 9,
        "name": "漆宝瓶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 10,
        "name": "雷若冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "",
        "native_place": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 11,
        "name": "徐伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大学文化程度",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 县政府其他领导（非县委常委）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "朱晓凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 13,
        "name": "杨峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 14,
        "name": "牟蓉",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1981年9月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 15,
        "name": "罗俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    {
        "id": 16,
        "name": "孔隽琦",
        "gender": "女",
        "ethnicity": "土族",
        "birth": "1989年11月",
        "birthplace": "",
        "native_place": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "礼县人民政府",
        "source": "https://www.gslx.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 前任领导（待核实具体信息）
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "礼县前任县委书记（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任",
        "current_org": "",
        "source": "需进一步从陇南市委组织部任前公示和新闻中核实",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共礼县委员会", "type": "党委", "level": "县", "parent": "中共陇南市委员会", "location": "甘肃省陇南市礼县"},
    {"id": 2, "name": "礼县人民政府", "type": "政府", "level": "县", "parent": "陇南市人民政府", "location": "甘肃省陇南市礼县"},
    {"id": 3, "name": "中共礼县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共礼县委员会", "location": "甘肃省陇南市礼县"},
    {"id": 4, "name": "中共礼县委员会组织部", "type": "党委", "level": "县", "parent": "中共礼县委员会", "location": "甘肃省陇南市礼县"},
    {"id": 5, "name": "中共礼县委员会统战部", "type": "党委", "level": "县", "parent": "中共礼县委员会", "location": "甘肃省陇南市礼县"},
    {"id": 6, "name": "中共礼县委员会政法委员会", "type": "党委", "level": "县", "parent": "中共礼县委员会", "location": "甘肃省陇南市礼县"},
    {"id": 7, "name": "礼县公安局", "type": "政府", "level": "县", "parent": "礼县人民政府", "location": "甘肃省陇南市礼县"},
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 刘景原 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "至今", "rank": "正处级", "note": "主持县委全面工作，兼管人民武装工作"},
    # 尚凤雷 - 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "至今", "rank": "正处级", "note": "主持县政府全面工作，负责审计方面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 杨敬 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "协助书记处理县委日常工作，分管乡村振兴、群团等工作"},
    # 李清泉 - 纪委书记
    {"person_id": 4, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "至今", "rank": "副处级", "note": "负责纪检监察和巡察工作"},
    # 逯彦果 - 组织部部长
    {"person_id": 5, "org_id": 4, "title": "县委常委、组织部部长", "start": "", "end": "至今", "rank": "副处级", "note": "负责党建、组织、干部、人才工作"},
    # 赵海军 - 统战部部长
    {"person_id": 6, "org_id": 5, "title": "县委常委、统战部部长", "start": "", "end": "至今", "rank": "副处级", "note": "负责县委统战及民族宗教工作"},
    # 叶炎 - 政法委书记
    {"person_id": 7, "org_id": 6, "title": "县委常委、政法委书记", "start": "", "end": "至今", "rank": "副处级", "note": "负责政法、信访和社会稳定工作"},
    # 施晓潇 - 常务副县长
    {"person_id": 8, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责县政府日常事务、发改、财政、人社、应急等工作"},
    # 漆宝瓶 - 副县长
    {"person_id": 9, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责住建、城市管理、自然资源、民政等工作"},
    # 雷若冰 - 副县长
    {"person_id": 10, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责国家市场监管总局定点帮扶礼县工作"},
    # 徐伟 - 副县长
    {"person_id": 11, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责东西部协作和青岛市崂山区对口帮扶礼县工作"},
    # 朱晓凯 - 副县长
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责工业信息化、交通、生态环境、市场监管等工作"},
    # 杨峰 - 副县长
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责农业农村、乡村振兴、水利、商务等工作"},
    # 牟蓉 - 副县长
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责教育、文旅、体育、卫健、医保等工作"},
    # 罗俊杰 - 副县长
    {"person_id": 15, "org_id": 7, "title": "副县长、县公安局局长", "start": "", "end": "至今", "rank": "副处级", "note": "负责公安、司法、退役军人事务、信访维稳等工作"},
    # 孔隽琦 - 副县长
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "负责科技、供销工作"},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 书记-县长：党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档关系", "overlap_org": "礼县县委、县政府", "overlap_period": "至今"},
    # 书记-副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委副书记上下级关系", "overlap_org": "中共礼县委员会", "overlap_period": "至今"},
    # 县长-常务副县长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与常务副县长工作搭档", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    # 县长-副县长（班子成员）
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长与县委常委、副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长与县委常委、副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长与县委常委、副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长与副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长与副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长与副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长与副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县长与副县长班子成员关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    # 县委常委间关系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与纪委书记工作关系", "overlap_org": "中共礼县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与组织部部长工作关系", "overlap_org": "中共礼县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与统战部部长工作关系", "overlap_org": "中共礼县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与政法委书记工作关系", "overlap_org": "中共礼县委员会", "overlap_period": "至今"},
    # 常务副县长分管联系
    {"person_a": 8, "person_b": 12, "type": "overlap", "context": "常务副县长与副县长工作配合关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 13, "type": "overlap", "context": "常务副县长与副县长工作配合关系", "overlap_org": "礼县人民政府", "overlap_period": "至今"},
    # 政法委书记-公安局长
    {"person_a": 7, "person_b": 15, "type": "superior_subordinate", "context": "政法委书记与县公安局局长业务指导关系", "overlap_org": "礼县政法系统", "overlap_period": "至今"},
    # 组织部部长-县委副书记（党建）
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县委副书记与组织部部长党建工作配合", "overlap_org": "中共礼县委员会", "overlap_period": "至今"},
]


# ═══════════════════════════════════════════════
# 运行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="礼县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Done.")
