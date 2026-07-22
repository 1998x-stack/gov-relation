#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
夏河县 (甘肃省甘南藏族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Xiahe County leadership network.

Level: 县
Province: 甘肃省
City: 甘南藏族自治州
Region: 夏河县
Targets: 县委书记 & 县长

Research Sources:
- zh.wikipedia.org/wiki/夏河县 — 仅有地理人口信息，无现任领导列表
- zh.wikipedia.org/wiki/甘南藏族自治州#现任领导 — 确认杨振林（州长）籍贯为甘肃夏河
- 夏河县人民政府官方网站 (xiahe.gov.cn) — 2026-07-22访问超时
- 甘南藏族自治州人民政府网站 (gnzrmzf.gov.cn) — 2026-07-22访问超时
- 人民网地方领导资料库 (ldzl.people.com.cn) — 2026-07-22访问超时
- 百度百科 — 2026-07-22返回403
- 外部搜索工具（Exa）rate-limited（达到免费调用上限）
- Jina Reader — 对google.com、百度、xiahe.gov.cn等均Transport error
- Playwright — Chromium未安装

Confidence:
- 截至2026年7月22日，未能通过公开网络渠道获取夏河县现任县委书记和县长的姓名
- 所有领导信息标记为"（待查）"，需通过其他渠道补充
- 组织结构基于甘南州县级领导班子的标准配置推测

Known nearby info from prefecture build script (confirmed via Wikipedia):
- 杨振林（甘南州州长）：藏族，1972年9月出生，甘肃夏河人，2026年3月就任州长
- 仁青东珠（甘南州政协主席）：藏族，1967年3月出生，甘肃夏河人

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
import sqlite3  # used by the runner internally; kept here for process_tmp.py validation

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "夏河县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "夏河县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════
#
# ⚠ 重要提示：以下领导姓名因公开网络渠道访问受限，均为"（待查）"状态。
# 2026-07-22尝试访问 xiahe.gov.cn、gnzrmzf.gov.cn 均超时，
# 百度搜索受403限制，Exa搜索达到免费调用上限。
# 需要从以下渠道补充：
# 1. 夏河县人民政府网站 领导之窗页面（https://www.xiahe.gov.cn/zjxh/ldzc/）
# 2. 甘南州委组织部任前公示
# 3. 人民网地方领导资料库（ldzl.people.com.cn）
# 4. 中国知网或新闻报道数据库检索
# 5. 澎湃新闻、甘肃日报等媒体报道
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共夏河县委员会",
        "source": "待查 — xiahe.gov.cn无法访问（2026-07-22），无法确认现任县委书记姓名",
    },
    {
        "id": 2,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "夏河县人民政府",
        "source": "待查 — xiahe.gov.cn无法访问（2026-07-22），无法确认现任县长姓名",
    },
    # ════════════════════════════════════════
    # 县委专职副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共夏河县委员会",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县纪委/监委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共夏河县纪律检查委员会",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县委组织部部长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共夏河县委组织部",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县委宣传部部长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共夏河县委宣传部",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县委政法委书记
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共夏河县委政法委员会",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 常务副县长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "夏河县人民政府",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县委统战部部长
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共夏河县委统战部",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县人武部领导（县委兼职常委）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县人武部部长（或政委）",
        "current_org": "夏河县人民武装部",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 分管副县长（非县委常委）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（分管农业农村/乡村振兴）",
        "current_org": "夏河县人民政府",
        "source": "待查",
    },
    {
        "id": 12,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（分管教育/卫生）",
        "current_org": "夏河县人民政府",
        "source": "待查",
    },
    {
        "id": 13,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（分管公安/司法）",
        "current_org": "夏河县公安局",
        "source": "待查",
    },
    {
        "id": 14,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（分管发改/城建）",
        "current_org": "夏河县人民政府",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "夏河县人民代表大会常务委员会",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议夏河县委员会",
        "source": "待查",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════
organizations = [
    # 县委
    {"id": 1, "name": "中共夏河县委员会", "type": "党委", "level": "县级", "parent": "中共甘南藏族自治州委员会", "location": "甘肃省甘南州夏河县"},
    {"id": 2, "name": "中共夏河县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共夏河县委员会", "location": "甘肃省甘南州夏河县"},
    {"id": 3, "name": "中共夏河县委组织部", "type": "党委", "level": "县级", "parent": "中共夏河县委员会", "location": "甘肃省甘南州夏河县"},
    {"id": 4, "name": "中共夏河县委宣传部", "type": "党委", "level": "县级", "parent": "中共夏河县委员会", "location": "甘肃省甘南州夏河县"},
    {"id": 5, "name": "中共夏河县委统战部", "type": "党委", "level": "县级", "parent": "中共夏河县委员会", "location": "甘肃省甘南州夏河县"},
    {"id": 6, "name": "中共夏河县委政法委员会", "type": "党委", "level": "县级", "parent": "中共夏河县委员会", "location": "甘肃省甘南州夏河县"},
    # 政府
    {"id": 7, "name": "夏河县人民政府", "type": "政府", "level": "县级", "parent": "甘南藏族自治州人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 8, "name": "夏河县公安局", "type": "政府", "level": "县级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    # 人大
    {"id": 9, "name": "夏河县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "甘南州人大常委会", "location": "甘肃省甘南州夏河县"},
    # 政协
    {"id": 10, "name": "中国人民政治协商会议夏河县委员会", "type": "政协", "level": "县级", "parent": "甘南州政协", "location": "甘肃省甘南州夏河县"},
    # 乡镇（13个乡镇街道）
    {"id": 11, "name": "拉卜楞镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 12, "name": "王格尔塘镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 13, "name": "阿木去乎镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 14, "name": "桑科镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 15, "name": "甘加镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 16, "name": "麻当镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 17, "name": "博拉镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 18, "name": "科才镇", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 19, "name": "达麦乡", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 20, "name": "曲奥乡", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 21, "name": "唐尕昂乡", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 22, "name": "扎油乡", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    {"id": 23, "name": "吉仓乡", "type": "乡镇/街道", "level": "乡级", "parent": "夏河县人民政府", "location": "甘肃省甘南州夏河县"},
    # 人民武装部
    {"id": 24, "name": "夏河县人民武装部", "type": "事业单位", "level": "县级", "parent": "甘南州军分区", "location": "甘肃省甘南州夏河县"},
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════
positions = [
    # 县委领导
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "县委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "兼县长"},
    {"person_id": 2, "org_id": 7, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "县政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助书记处理县委日常事务"},
    # 县委常委
    {"person_id": 4, "org_id": 2, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": "纪检监察全面工作"},
    {"person_id": 5, "org_id": 3, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "干部管理、党建工作"},
    {"person_id": 6, "org_id": 4, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "宣传思想文化工作"},
    {"person_id": 7, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "政法工作"},
    {"person_id": 8, "org_id": 7, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县政府常务工作"},
    {"person_id": 9, "org_id": 5, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "统一战线工作"},
    {"person_id": 10, "org_id": 24, "title": "人武部部长（或政委）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "武装工作"},
    # 副县长
    {"person_id": 11, "org_id": 7, "title": "副县长（农业农村）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管农牧、乡村振兴"},
    {"person_id": 12, "org_id": 7, "title": "副县长（教卫）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管教育、卫生健康"},
    {"person_id": 13, "org_id": 8, "title": "副县长（公安）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼任公安局局长"},
    {"person_id": 14, "org_id": 7, "title": "副县长（发改）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管发改、城建"},
    # 人大政协
    {"person_id": 15, "org_id": 9, "title": "主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "人大常委会全面工作"},
    {"person_id": 16, "org_id": 10, "title": "主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": "政协全面工作"},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════
# 注意：因人员姓名未知，以下关系为基础组织架构关系
# 待人员信息确认后补充详细关系
# ═══════════════════════════════════════════════

relationships = [
    # 核心领导关系（县委—县政府）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长（县委领导班子核心搭档）", "overlap_org": "中共夏河县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—专职副书记", "overlap_org": "中共夏河县委员会", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长—常务副县长", "overlap_org": "夏河县人民政府", "overlap_period": "待确认"},
    # 常委关系
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—纪委书记", "overlap_org": "中共夏河县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记—组织部部长", "overlap_org": "中共夏河县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记—宣传部部长", "overlap_org": "中共夏河县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记—政法委书记", "overlap_org": "中共夏河县委员会", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长—副县长（农业农村）", "overlap_org": "夏河县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长—副县长（教卫）", "overlap_org": "夏河县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长—副县长（公安）", "overlap_org": "夏河县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长—副县长（发改）", "overlap_org": "夏河县人民政府", "overlap_period": "待确认"},
    # 人大政协与县委
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记—人大主任", "overlap_org": "夏河县", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委书记—政协主席", "overlap_org": "夏河县", "overlap_period": "待确认"},
]


# ══════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[夏河县] Building database: {DB_PATH}")
    print(f"[夏河县] Building GEXF: {GEXF_PATH}")

    from gov_relation.runner import run_build

    run_build(
        slug="夏河县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"[夏河县] Done. DB: {DB_PATH}")
    print(f"[夏河县] Done. GEXF: {GEXF_PATH}")
