#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
碌曲县 (甘肃省甘南藏族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Luqu County leadership network.

Level: 县
Province: 甘肃省
City: 甘南藏族自治州
Region: 碌曲县
Targets: 县委书记 & 县长

Research Sources:
- 碌曲县人民政府官方网站 (luqu.gov.cn) — 领导之窗页面，2026-07-22确认
- 中共碌曲县委员会领导之窗: http://www.luqu.gov.cn/ldzc/zglqxwyh.htm
- 碌曲县人民政府领导之窗: http://www.luqu.gov.cn/ldzc/lqxrmzf.htm
- 碌曲县人大常委会领导之窗: http://www.luqu.gov.cn/ldzc/lqxrdcwh.htm
- 政协碌曲县委员会领导之窗: http://www.luqu.gov.cn/ldzc/zxlqxwyh.htm

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
import sqlite3  # used by process_tmp.py validator

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "data/database/碌曲县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "data/graph/碌曲县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════
#
# 数据来源：碌曲县人民政府网站领导之窗页面（2026-07-22确认）
# 详细履历（籍贯、入党时间、工作经历等）待后续调研补充。
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "吴煜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共碌曲县委员会",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 2,
        "name": "旦正昂杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1975年2月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    # ════════════════════════════════════════
    # 县委副书记（专职）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "看召本",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1979年7月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共碌曲县委员会",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "何伟光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、监委主任",
        "current_org": "中共碌曲县纪律检查委员会/碌曲县监察委员会",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 5,
        "name": "扎西华旦",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1986年1月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 6,
        "name": "王定玺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共碌曲县委员会宣传部",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 7,
        "name": "刘洋萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 8,
        "name": "王登辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "1983年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共碌曲县委员会组织部",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 9,
        "name": "旦正才让",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1983年9月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共碌曲县委员会统战部",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 10,
        "name": "当子加",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1984年2月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共碌曲县委员会政法委员会",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 11,
        "name": "方万松",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1985年7月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/zglqxwyh.htm (2026-07-22确认)",
    },
    # ════════════════════════════════════════
    # 县政府副县长（非县委常委）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "拉毛东知",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1983年7月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrmzf.htm (2026-07-22确认)",
    },
    {
        "id": 13,
        "name": "苏奴次旦",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1978年10月",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrmzf.htm (2026-07-22确认)",
    },
    {
        "id": 14,
        "name": "方斌",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1991年7月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrmzf.htm (2026-07-22确认)",
    },
    {
        "id": 15,
        "name": "王博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrmzf.htm (2026-07-22确认)",
    },
    {
        "id": 16,
        "name": "杨龙宝",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1982年3月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "碌曲县人民政府/碌曲县公安局",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrmzf.htm (2026-07-22确认)",
    },
    {
        "id": 17,
        "name": "王仁杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1983年10月",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrmzf.htm (2026-07-22确认)",
    },
    {
        "id": 18,
        "name": "李琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987年1月",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "碌曲县人民政府",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrmzf.htm (2026-07-22确认)",
    },
    # ════════════════════════════════════════
    # 县人大常委会
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "万玛加",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1970年1月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "碌曲县人大常委会",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrdcwh.htm (2026-07-22确认)",
    },
    {
        "id": 20,
        "name": "宗哲加措",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1972年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "碌曲县人大常委会",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrdcwh.htm (2026-07-22确认)",
    },
    {
        "id": 21,
        "name": "马福莲",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1966年8月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "碌曲县人大常委会",
        "source": "http://www.luqu.gov.cn/ldzc/lqxrdcwh.htm (2026-07-22确认)",
    },
    # ════════════════════════════════════════
    # 县政协
    # ════════════════════════════════════════
    {
        "id": 22,
        "name": "黄万民",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1969年6月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协碌曲县委员会",
        "source": "http://www.luqu.gov.cn/ldzc/zxlqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 23,
        "name": "杨月红",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1970年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大专学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协碌曲县委员会",
        "source": "http://www.luqu.gov.cn/ldzc/zxlqxwyh.htm (2026-07-22确认)",
    },
    {
        "id": 24,
        "name": "王建修",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大专学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协碌曲县委员会",
        "source": "http://www.luqu.gov.cn/ldzc/zxlqxwyh.htm (2026-07-22确认)",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共碌曲县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共甘南藏族自治州委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 2,
        "name": "中共碌曲县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共碌曲县委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 3,
        "name": "中共碌曲县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共碌曲县委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 4,
        "name": "中共碌曲县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共碌曲县委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 5,
        "name": "中共碌曲县委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共碌曲县委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 6,
        "name": "碌曲县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "甘南藏族自治州人民政府",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 7,
        "name": "中共碌曲县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共碌曲县委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 8,
        "name": "碌曲县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共碌曲县委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 9,
        "name": "碌曲县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "碌曲县人民政府",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 10,
        "name": "碌曲县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "甘南藏族自治州人大常委会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
    {
        "id": 11,
        "name": "政协碌曲县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协甘南藏族自治州委员会",
        "location": "甘肃省甘南藏族自治州碌曲县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 县委书记 — 吴煜
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "主持县委全面工作"},
    # 县长 — 旦正昂杰
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "主持县政府全面工作，负责审计方面工作"},
    # 专职副书记 — 看召本
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 纪委书记 — 何伟光
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 7, "title": "县纪委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 8, "title": "县监委主任", "start": "", "end": "present", "rank": "副县级", "note": "四级高级监察官"},
    # 常务副县长 — 扎西华旦
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管县发展和改革局、县应急管理局等"},
    # 宣传部部长 — 王定玺
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 副县长 — 刘洋萍
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管县教育局、县文体广旅局等"},
    # 组织部部长 — 王登辉
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 统战部部长 — 旦正才让
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "统战部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 政法委书记 — 当子加
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 挂职副县长 — 方万松
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "负责东西部协作和天津对口支援工作"},
    # 副县长 — 拉毛东知
    {"person_id": 12, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责农业农村、乡村振兴等"},
    # 副县长 — 苏奴次旦
    {"person_id": 13, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管县财政局、县人社局、县交通局等"},
    # 副县长 — 方斌
    {"person_id": 14, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责住房和城乡建设、民政等"},
    # 副县长 — 王博
    {"person_id": 15, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责地震、地方史志、驻村帮扶等"},
    # 副县长/公安局长 — 杨龙宝
    {"person_id": 16, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 9, "title": "县公安局局长", "start": "", "end": "present", "rank": "正科级", "note": "三级高级警长"},
    # 副县长 — 王仁杰
    {"person_id": 17, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "分管县自然资源局、县水务局等"},
    # 副县长 — 李琳
    {"person_id": 18, "org_id": 6, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责县政府办公室、机关事务管理"},
    # 人大主任 — 万玛加
    {"person_id": 19, "org_id": 10, "title": "县人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 人大副主任 — 宗哲加措
    {"person_id": 20, "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 人大副主任 — 马福莲
    {"person_id": 21, "org_id": 10, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 政协主席 — 黄万民
    {"person_id": 22, "org_id": 11, "title": "县政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 政协副主席 — 杨月红
    {"person_id": 23, "org_id": 11, "title": "县政协副主席", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 政协副主席 — 王建修
    {"person_id": 24, "org_id": 11, "title": "县政协副主席", "start": "", "end": "present", "rank": "副县级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════
#
# 来源：luqu.gov.cn 领导之窗及新闻确认。
# 吴煜与旦正昂杰的搭档关系通过多篇新闻报道确认（2026年7月
# 多篇县内要闻显示二人共同调研、共同出席活动）。
# 其他班子成员关系基于县级领导班子结构推断。
# ═══════════════════════════════════════════════

relationships = [
    # 县委书记 — 县长（confirmed搭档）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共碌曲县委员会/碌曲县人民政府", "overlap_period": "—2026"},
    # 县委书记 — 专职副书记
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记", "overlap_org": "中共碌曲县委员会", "overlap_period": "—2026"},
    # 县委书记 — 县委常委班子成员
    {"person_a": 1, "person_b": 4, "type": "监督", "context": "县委书记—纪委书记（同级监督）", "overlap_org": "中共碌曲县委员会", "overlap_period": "—2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共碌曲县委员会/碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共碌曲县委员会", "overlap_period": "—2026"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委书记—副县长", "overlap_org": "中共碌曲县委员会/碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共碌曲县委员会", "overlap_period": "—2026"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—统战部部长", "overlap_org": "中共碌曲县委员会", "overlap_period": "—2026"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共碌曲县委员会", "overlap_period": "—2026"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "县委书记—挂职副县长", "overlap_org": "中共碌曲县委员会/碌曲县人民政府", "overlap_period": "—2026"},
    # 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "县长—常务副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—挂职副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "县长—副县长/公安局长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    # 常务副县长与副县长
    {"person_a": 5, "person_b": 12, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 5, "person_b": 13, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 5, "person_b": 14, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 5, "person_b": 15, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 5, "person_b": 16, "type": "共事", "context": "常务副县长—副县长/公安局长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 5, "person_b": 17, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    {"person_a": 5, "person_b": 18, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "碌曲县人民政府", "overlap_period": "—2026"},
    # 政法委书记与公安局长
    {"person_a": 10, "person_b": 16, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "碌曲县政法系统", "overlap_period": "—2026"},
    # 组织部长与专职副书记
    {"person_a": 3, "person_b": 8, "type": "共事", "context": "专职副书记—组织部部长", "overlap_org": "中共碌曲县委员会", "overlap_period": "—2026"},
    # 人大主任与县委书记
    {"person_a": 1, "person_b": 19, "type": "共事", "context": "县委书记—人大主任", "overlap_org": "碌曲县四套班子", "overlap_period": "—2026"},
    # 政协主席与县委书记
    {"person_a": 1, "person_b": 22, "type": "共事", "context": "县委书记—政协主席", "overlap_org": "碌曲县四套班子", "overlap_period": "—2026"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("碌曲县（甘肃省甘南藏族自治州）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()
    print("调研日期：2026-07-22")
    print("信息来源：碌曲县人民政府官方网站（luqu.gov.cn）领导之窗页面")
    print()
    print("已确认领导（全体24人）：")
    print("  核心领导：")
    print("    - 县委书记：吴煜（1972年1月，汉族，省委党校研究生）")
    print("    - 县长：旦正昂杰（1975年2月，藏族，大学学历）")
    print("    - 专职副书记：看召本（1979年7月，藏族，研究生）")
    print("  县委常委（9人）：")
    print("    - 何伟光（纪委书记、监委主任）")
    print("    - 扎西华旦（常务副县长）")
    print("    - 王定玺（宣传部部长）")
    print("    - 刘洋萍（副县长）")
    print("    - 王登辉（组织部部长）")
    print("    - 旦正才让（统战部部长）")
    print("    - 当子加（政法委书记）")
    print("    - 方万松（挂职副县长）")
    print("  副县长（7人）：拉毛东知、苏奴次旦、方斌、王博、杨龙宝（兼公安局长）、王仁杰、李琳")
    print("  人大（3人）：万玛加（主任）、宗哲加措、马福莲（副主任）")
    print("  政协（3人）：黄万民（主席）、杨月红、王建修（副主席）")
    print()
    print("注意：详细履历（籍贯、入党时间、工作经历等）待后续调研补充。")
    print()

    run_build(
        slug="碌曲县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")
    print("=" * 60)
    print()
    print("✓ 全县四套班子全体24人已确认")
    print("⚠ 详细履历（籍贯、入党时间、此前任职等）待后续调研补充")
