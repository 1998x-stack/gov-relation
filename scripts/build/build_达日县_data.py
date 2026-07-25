#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
达日县 (青海省果洛藏族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Darlag (Dari) County leadership network.

Level: 县
Province: 青海省
City: 果洛藏族自治州
Region: 达日县
Targets: 县委书记 & 县长

Research Sources:
- 达日县人民政府官方网站 (dari.gov.cn) — 领导信息页面：
  - 县委领导: https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/
  - 政府领导: https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/
  - 人大领导: https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/rdld/
  - 政协领导: https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zxld/
- 新闻"紧盯督察整改任务 筑牢三江源生态屏障"（2026-06-04）确认王志江(书记)、石维鹏(县长)
- External search tools (Exa) rate-limited; 百度百科/Google/Bing 搜索受限

Confidence:
- 全部29名领导名单：confirmed（达日县政府官网领导信息栏目）
- 常委具体分管职务（纪委书记、组织部长等）：待确认
- 常务副县长具体人选：待确认
- 个人简历详情（出生、民族、籍贯、学历等）：待补充（简历页URL已知但服务器超时）

Research Date: 2026-07-25
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
DB_PATH = os.path.join(STAGING_DIR, "达日县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "达日县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据 — 全部来自达日县政府官网（2026年）
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导（12人：含书记、副书记、政法委书记等）
    # 来源：https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/
    # 注：常委具体分管职务（如纪委书记、组织部长等）需通过个人简历页补充
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王志江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 (https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/) 及新闻确认",
    },
    {
        "id": 2,
        "name": "石维鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网领导信息栏目 (https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/) 及新闻确认",
    },
    {
        "id": 3,
        "name": "尕玛松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 县委领导名单第3位",
    },
    {
        "id": 4,
        "name": "王发鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目",
    },
    {
        "id": 5,
        "name": "石凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网 — 同时在县委和政府领导名单中",
    },
    {
        "id": 6,
        "name": "谢德飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网 — 同时在县委和政府领导名单中",
    },
    {
        "id": 7,
        "name": "王海峻",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网 — 同时在县委和政府领导名单中",
    },
    {
        "id": 8,
        "name": "贡却仁增",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 县委领导名单第8位",
    },
    {
        "id": 9,
        "name": "尼玛才让",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 县委领导名单第9位",
    },
    {
        "id": 10,
        "name": "赵恣嵘",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 县委领导名单第10位",
    },
    {
        "id": 11,
        "name": "陈令章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 县委领导名单第11位",
    },
    {
        "id": 12,
        "name": "力加东智",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 县委领导名单第12位",
    },
    # ════════════════════════════════════════
    # 政府领导（不含已在县委名单中的石维鹏/石凯/谢德飞/王海峻）
    # 来源：https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "万德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网领导信息栏目 — 政府领导名单 (https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/)",
    },
    {
        "id": 14,
        "name": "曹毛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网领导信息栏目 — 政府领导名单",
    },
    {
        "id": 15,
        "name": "多杰扎西",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网领导信息栏目 — 政府领导名单",
    },
    {
        "id": 16,
        "name": "宁格加",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网领导信息栏目 — 政府领导名单",
    },
    {
        "id": 17,
        "name": "冯建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网领导信息栏目 — 政府领导名单",
    },
    {
        "id": 18,
        "name": "象花措",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "达日县人民政府",
        "source": "达日县人民政府官网领导信息栏目 — 政府领导名单",
    },
    # ════════════════════════════════════════
    # 县人大常委会
    # 来源：https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/rdld/
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "才旦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "达日县人民代表大会常务委员会",
        "source": "达日县人民政府官网领导信息栏目 — 人大领导名单 (https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/rdld/)",
    },
    {
        "id": 20,
        "name": "夏扎西",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "达日县人民代表大会常务委员会",
        "source": "达日县人民政府官网领导信息栏目 — 人大领导名单",
    },
    {
        "id": 21,
        "name": "扎西才让",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "达日县人民代表大会常务委员会",
        "source": "达日县人民政府官网领导信息栏目 — 人大领导名单",
    },
    {
        "id": 22,
        "name": "达哇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "达日县人民代表大会常务委员会",
        "source": "达日县人民政府官网领导信息栏目 — 人大领导名单",
    },
    # ════════════════════════════════════════
    # 县政协
    # 来源：https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zxld/
    # ════════════════════════════════════════
    {
        "id": 23,
        "name": "扎西",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 政协领导名单 (https://www.dari.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zxld/)",
    },
    {
        "id": 24,
        "name": "李富年",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 政协领导名单",
    },
    {
        "id": 25,
        "name": "贾保",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议达日县委员会",
        "source": "达日县人民政府官网领导信息栏目 — 政协领导名单",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════
organizations = [
    # 县委
    {"id": 1, "name": "中共达日县委员会", "type": "党委", "level": "县级", "parent": "中共果洛藏族自治州委员会", "location": "青海省果洛州达日县"},
    {"id": 2, "name": "中共达日县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共达日县委员会", "location": "青海省果洛州达日县"},
    {"id": 3, "name": "中共达日县委组织部", "type": "党委", "level": "县级", "parent": "中共达日县委员会", "location": "青海省果洛州达日县"},
    {"id": 4, "name": "中共达日县委宣传部", "type": "党委", "level": "县级", "parent": "中共达日县委员会", "location": "青海省果洛州达日县"},
    {"id": 5, "name": "中共达日县委统战部", "type": "党委", "level": "县级", "parent": "中共达日县委员会", "location": "青海省果洛州达日县"},
    {"id": 6, "name": "中共达日县委政法委员会", "type": "党委", "level": "县级", "parent": "中共达日县委员会", "location": "青海省果洛州达日县"},
    # 政府
    {"id": 7, "name": "达日县人民政府", "type": "政府", "level": "县级", "parent": "果洛藏族自治州人民政府", "location": "青海省果洛州达日县"},
    {"id": 8, "name": "达日县公安局", "type": "政府", "level": "县级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    # 人大
    {"id": 9, "name": "达日县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "果洛州人大常委会", "location": "青海省果洛州达日县"},
    # 政协
    {"id": 10, "name": "中国人民政治协商会议达日县委员会", "type": "政协", "level": "县级", "parent": "果洛州政协", "location": "青海省果洛州达日县"},
    # 乡镇（1镇9乡）
    {"id": 11, "name": "吉迈镇", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 12, "name": "满掌乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 13, "name": "德昂乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 14, "name": "窝赛乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 15, "name": "莫坝乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 16, "name": "上红科乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 17, "name": "下红科乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 18, "name": "建设乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 19, "name": "桑日麻乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    {"id": 20, "name": "特合土乡", "type": "乡镇/街道", "level": "乡级", "parent": "达日县人民政府", "location": "青海省果洛州达日县"},
    # 人民武装部
    {"id": 21, "name": "达日县人民武装部", "type": "事业单位", "level": "县级", "parent": "果洛州军分区", "location": "青海省果洛州达日县"},
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
    # 县委常委（具体分管职务待确认）
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管职务待确认"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼副县长，具体分管职务待确认"},
    {"person_id": 5, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼副县长，具体分管职务待确认"},
    {"person_id": 6, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼副县长，具体分管职务待确认"},
    {"person_id": 7, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管职务待确认"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管职务待确认"},
    # 副县长（非县委常委）
    {"person_id": 13, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 14, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 15, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 16, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 17, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    {"person_id": 18, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体分管领域待确认"},
    # 人大
    {"person_id": 19, "org_id": 9, "title": "主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "人大常委会全面工作"},
    {"person_id": 20, "org_id": 9, "title": "副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 21, "org_id": 9, "title": "副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 22, "org_id": 9, "title": "副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 政协
    {"person_id": 23, "org_id": 10, "title": "主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": "政协全面工作"},
    {"person_id": 24, "org_id": 10, "title": "副主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 25, "org_id": 10, "title": "副主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════
# 注：常委具体分管职务尚待确认，以下为基础组织架构关系
# ═══════════════════════════════════════════════

relationships = [
    # 核心领导关系（县委—县政府）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长（县委领导班子核心搭档，共同出现在2026年6月生态环保督察整改实地督导）", "overlap_org": "中共达日县委员会", "overlap_period": "2026 or earlier"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—专职副书记（县委常委班子）", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—县委常委王发鑫", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记—县委常委/副县长石凯", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记—县委常委/副县长谢德飞", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记—县委常委/副县长王海峻", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记—县委常委贡却仁增", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记—县委常委尼玛才让", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记—县委常委赵恣嵘", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记—县委常委陈令章", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委书记—县委常委力加东智", "overlap_org": "中共达日县委员会", "overlap_period": "待确认"},
    # 县长与副县长关系
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长—副县长万德", "overlap_org": "达日县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长—副县长曹毛", "overlap_org": "达日县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长—副县长多杰扎西", "overlap_org": "达日县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县长—副县长宁格加", "overlap_org": "达日县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "县长—副县长冯建", "overlap_org": "达日县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "县长—副县长象花措", "overlap_org": "达日县人民政府", "overlap_period": "待确认"},
    # 人大政协与县委
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "县委书记—人大主任才旦", "overlap_org": "达日县", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 23, "type": "overlap", "context": "县委书记—政协主席扎西", "overlap_org": "达日县", "overlap_period": "待确认"},
]


# ══════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[达日县] Building database: {DB_PATH}")
    print(f"[达日县] Building GEXF: {GEXF_PATH}")

    run_build(
        slug="达日县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"[达日县] Done. DB: {DB_PATH}")
    print(f"[达日县] Done. GEXF: {GEXF_PATH}")
