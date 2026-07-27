#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
班玛县 (青海省果洛藏族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Banma County leadership network.

Level: 县
Province: 青海省
Prefecture: 果洛藏族自治州
Region: 班玛县
Targets: 县委书记 & 县长

Research Sources (2026-07-25):
- 班玛县人民政府官方网站 (www.banma.gov.cn) — 2026-07-25 成功访问
  - 领导信息页面: /zwgk/fdzdgknr/jgjj/ldxx/
  - 县委领导页面: /zwgk/fdzdgknr/jgjj/ldxx/xwld/
  - 政府领导页面: /zwgk/fdzdgknr/jgjj/ldxx/zfld/
  - 人大领导页面: /zwgk/fdzdgknr/jgjj/ldxx/rdld/
  - 政协领导页面: /zwgk/fdzdgknr/jgjj/ldxx/zxld/
- 班玛要闻 (2026-07-13): 关却扎西主持召开县委常委会第108次会议
- 班玛要闻 (2026-07-02): 县政府办公室传达学习县委书记张效勇批示精神
- 扎西东智简历: /xwld/zxdz/202506/t20250620_262433.html

Confidence:
- 官方领导信息页面确认的当前任职信息为 "confirmed" 级别
- 新闻中出现的官员信息为 "confirmed"
- 个人履历信息（仅包含基础身份信息）为 "confirmed"
- 个人详细履历（早期职位）为 "plausible" 或 "unverified"
- 组织机构和职位关系基于官方页面确认

Note: 县委书记一栏存在差异——官方领导信息页面显示祁宝业为县委书记(2025年6月照片),
但2026年7月的新闻提到"县委书记张效勇"。可能有近期领导变更,领导信息页面尚未更新。
本脚本同时包含两人并标注不确定性。

Note on 关却扎西: 2026年7月13日的新闻中,"受县委书记张效勇委托,县委副书记关却扎西
主持召开县委常委会第108次会议"。关却扎西是县委副书记,具体职务不详(可能挂职或援青干部)。

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
DB_PATH = os.path.join(STAGING_DIR, "班玛县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "班玛县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "祁宝业",
        "gender": "男",
        "ethnicity": "",  # 官方页面未提供
        "birth": "",  # 官方页面未提供出生年份
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委书记（据2025年6月官方领导信息页面）",
        "current_org": "中共班玛县委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/qby/",
    },
    {
        "id": 2,
        "name": "张效勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委书记（2026年7月新闻确认）",
        "current_org": "中共班玛县委员会",
        "source": "http://www.banma.gov.cn/xwdt/bmyw/202607/t20260702_408275.html",
    },
    {
        "id": 3,
        "name": "扎西东智",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "",
        "party_join": "1997年12月",
        "work_start": "1996年7月",
        "current_post": "班玛县委副书记、县人民政府县长",
        "current_org": "班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/zxdz/202506/t20250620_262433.html",
    },
    {
        "id": 4,
        "name": "关却扎西",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委副书记（2026年7月新闻确认）",
        "current_org": "中共班玛县委员会",
        "source": "http://www.banma.gov.cn/xwdt/bmyw/202607/t20260713_408884.html",
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "时亚坤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委副书记、县人民政府副县长",
        "current_org": "中共班玛县委员会/班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/syk/",
    },
    {
        "id": 6,
        "name": "庞冲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委常委、宣传部部长",
        "current_org": "中共班玛县委员会宣传部",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/pc/",
    },
    {
        "id": 7,
        "name": "沙群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "果洛州班玛县委副书记",
        "current_org": "中共班玛县委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/sq/",
    },
    {
        "id": 8,
        "name": "沈激",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委副书记、县人民政府副县长",
        "current_org": "中共班玛县委员会/班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/sj/",
    },
    {
        "id": 9,
        "name": "班玛南杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委常委、组织部部长",
        "current_org": "中共班玛县委员会组织部",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/bmnj/",
    },
    {
        "id": 10,
        "name": "鲍桂兰",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委常委、总工会主席、宣传部部长",
        "current_org": "中共班玛县委员会/班玛县总工会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/bgl/",
    },
    {
        "id": 11,
        "name": "昂保",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委常委、政法委书记",
        "current_org": "中共班玛县委员会政法委",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/ab/",
    },
    {
        "id": 12,
        "name": "当周才郎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委常委、县纪委书记、监委主任",
        "current_org": "中共班玛县纪律检查委员会/班玛县监察委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/dzcl/",
    },
    {
        "id": 13,
        "name": "才白",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县委委员、常委、统战部部长",
        "current_org": "中共班玛县委员会统战部",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/cb/",
    },
    {
        "id": 14,
        "name": "夏红梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人民政府常务副县长",
        "current_org": "班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/xwld/xhm/",
    },
    # ════════════════════════════════════════
    # 人大领导
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "扎西",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人大常委会主任",
        "current_org": "班玛县人民代表大会常务委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/rdld/zx/",
    },
    {
        "id": 16,
        "name": "董强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人大常委会副主任",
        "current_org": "班玛县人民代表大会常务委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/rdld/",
    },
    {
        "id": 17,
        "name": "赵顺才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人大常委会副主任",
        "current_org": "班玛县人民代表大会常务委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/rdld/",
    },
    {
        "id": 18,
        "name": "尕措南杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人大常委会副主任",
        "current_org": "班玛县人民代表大会常务委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/rdld/",
    },
    # ════════════════════════════════════════
    # 政协领导
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "杨金凤",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县政协主席",
        "current_org": "中国人民政治协商会议班玛县委员会",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zxld/yjf/",
    },
    # ════════════════════════════════════════
    # 政府副县长（从政府领导页面确认）
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "公保才让",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人民政府副县长",
        "current_org": "班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/",
    },
    {
        "id": 21,
        "name": "翟泽浩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人民政府副县长",
        "current_org": "班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/",
    },
    {
        "id": 22,
        "name": "宁格加",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人民政府副县长",
        "current_org": "班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/",
    },
    {
        "id": 23,
        "name": "班玛尖参",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人民政府副县长",
        "current_org": "班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/",
    },
    {
        "id": 24,
        "name": "杨峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "班玛县人民政府副县长",
        "current_org": "班玛县人民政府",
        "source": "http://www.banma.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/zfld/",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    # 党委
    {"id": 1, "name": "中共班玛县委员会", "type": "党委", "level": "县", "parent": "中共果洛藏族自治州委员会", "location": "青海省果洛州班玛县"},
    {"id": 2, "name": "中共班玛县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共班玛县委员会", "location": "青海省果洛州班玛县"},
    {"id": 3, "name": "中共班玛县委宣传部", "type": "党委", "level": "县", "parent": "中共班玛县委员会", "location": "青海省果洛州班玛县"},
    {"id": 4, "name": "中共班玛县委组织部", "type": "党委", "level": "县", "parent": "中共班玛县委员会", "location": "青海省果洛州班玛县"},
    {"id": 5, "name": "中共班玛县委政法委", "type": "党委", "level": "县", "parent": "中共班玛县委员会", "location": "青海省果洛州班玛县"},
    {"id": 6, "name": "中共班玛县委统战部", "type": "党委", "level": "县", "parent": "中共班玛县委员会", "location": "青海省果洛州班玛县"},
    # 政府
    {"id": 7, "name": "班玛县人民政府", "type": "政府", "level": "县", "parent": "果洛藏族自治州人民政府", "location": "青海省果洛州班玛县"},
    {"id": 8, "name": "班玛县监察委员会", "type": "政府", "level": "县", "parent": "班玛县人民政府", "location": "青海省果洛州班玛县"},
    {"id": 9, "name": "班玛县总工会", "type": "群团", "level": "县", "parent": "中共班玛县委员会", "location": "青海省果洛州班玛县"},
    # 人大
    {"id": 10, "name": "班玛县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "班玛县", "location": "青海省果洛州班玛县"},
    # 政协
    {"id": 11, "name": "中国人民政治协商会议班玛县委员会", "type": "政协", "level": "县", "parent": "班玛县", "location": "青海省果洛州班玛县"},
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 祁宝业 -> 县委
    {"person_id": 1, "org_id": 1, "title": "班玛县委书记", "start": "", "end": "", "rank": "正县级", "note": "据2025年6月官方领导信息页面；可能已离任由张效勇接替"},
    # 张效勇 -> 县委
    {"person_id": 2, "org_id": 1, "title": "班玛县委书记", "start": "", "end": "", "rank": "正县级", "note": "2026年7月新闻确认在任"},
    # 扎西东智 -> 县委 + 政府
    {"person_id": 3, "org_id": 1, "title": "班玛县委副书记", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 7, "title": "班玛县人民政府县长", "start": "", "end": "", "rank": "正县级", "note": "主持县政府全盘工作。分管县审计局、社会综合治理工作。联系县人大常委会、县政协委员会。"},
    # 关却扎西 -> 县委
    {"person_id": 4, "org_id": 1, "title": "班玛县委副书记", "start": "", "end": "", "rank": "", "note": "2026年7月13日受县委书记张效勇委托主持县委常委会"},
    # 时亚坤 -> 县委 + 政府
    {"person_id": 5, "org_id": 1, "title": "班玛县委副书记", "start": "", "end": "", "rank": "", "note": "负责林业草原、三江源自然保护、移民安置等工作"},
    {"person_id": 5, "org_id": 7, "title": "班玛县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": "分管三江源自然保护地班玛县管理局、县移民安置局"},
    # 庞冲 -> 宣传部
    {"person_id": 6, "org_id": 3, "title": "班玛县委常委、宣传部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 沙群 -> 县委
    {"person_id": 7, "org_id": 1, "title": "果洛州班玛县委副书记", "start": "", "end": "", "rank": "", "note": ""},
    # 沈激 -> 县委 + 政府
    {"person_id": 8, "org_id": 1, "title": "班玛县委副书记", "start": "", "end": "", "rank": "", "note": "负责招商、上海对口支援等工作"},
    {"person_id": 8, "org_id": 7, "title": "班玛县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": "分管商务局，协调对口支援和东西部协作"},
    # 班玛南杰 -> 组织部
    {"person_id": 9, "org_id": 4, "title": "班玛县委常委、组织部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 鲍桂兰 -> 宣传部 + 总工会
    {"person_id": 10, "org_id": 3, "title": "班玛县委常委、宣传部部长", "start": "", "end": "", "rank": "副县级", "note": "与庞冲同为宣传部长，可能为不同时期或分工调整"},
    {"person_id": 10, "org_id": 9, "title": "班玛县总工会主席", "start": "", "end": "", "rank": "", "note": ""},
    # 昂保 -> 政法委
    {"person_id": 11, "org_id": 5, "title": "班玛县委常委、政法委书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 当周才郎 -> 纪委 + 监委
    {"person_id": 12, "org_id": 2, "title": "班玛县委常委、县纪委书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 8, "title": "班玛县监察委员会主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 才白 -> 统战部
    {"person_id": 13, "org_id": 6, "title": "班玛县委常委、统战部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 夏红梅 -> 政府（常务副县长）
    {"person_id": 14, "org_id": 7, "title": "班玛县人民政府常务副县长", "start": "", "end": "", "rank": "副县级", "note": "负责县人民政府常务工作、财政、发改、工信、应急管理等"},
    # 人大
    {"person_id": 15, "org_id": 10, "title": "班玛县人大常委会主任", "start": "", "end": "", "rank": "正县级", "note": "领导并主持县人大常委会全面工作"},
    {"person_id": 16, "org_id": 10, "title": "班玛县人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 10, "title": "班玛县人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 10, "title": "班玛县人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 政协
    {"person_id": 19, "org_id": 11, "title": "班玛县政协主席", "start": "", "end": "", "rank": "正县级", "note": "主持委员会全盘工作，开展慈善工作"},
    # 副县长
    {"person_id": 20, "org_id": 7, "title": "班玛县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 21, "org_id": 7, "title": "班玛县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 22, "org_id": 7, "title": "班玛县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 7, "title": "班玛县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 24, "org_id": 7, "title": "班玛县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 祁宝业 <-> 张效勇（前后任）
    {
        "person_a": 1, "person_b": 2,
        "type": "predecessor_successor",
        "context": "祁宝业与张效勇可能为前后任县委书记关系",
        "overlap_org": "中共班玛县委员会",
        "overlap_period": "",
        "strength": "weak",
    },
    # 祁宝业 <-> 扎西东智（县委班子搭档）
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委书记祁宝业与县长扎西东智为县委班子搭档",
        "overlap_org": "中共班玛县委员会",
        "overlap_period": "",
        "strength": "strong",
    },
    # 张效勇 <-> 扎西东智（县委班子搭档）
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "县委书记张效勇与县长扎西东智为县委班子搭档（2026年7月）",
        "overlap_org": "中共班玛县委员会",
        "overlap_period": "",
        "strength": "strong",
    },
    # 张效勇 <-> 关却扎西（上下级）
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "关却扎西受县委书记张效勇委托主持县委常委会",
        "overlap_org": "中共班玛县委员会",
        "overlap_period": "2026-07",
        "strength": "strong",
    },
    # 扎西东智 <-> 关却扎西（县委班子）
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "同为县委班子成员",
        "overlap_org": "中共班玛县委员会",
        "overlap_period": "",
        "strength": "medium",
    },
    # 扎西东智 <-> 夏红梅（政府正副职）
    {
        "person_a": 3, "person_b": 14,
        "type": "superior_subordinate",
        "context": "夏红梅作为常务副县长协助县长扎西东智工作",
        "overlap_org": "班玛县人民政府",
        "overlap_period": "",
        "strength": "strong",
    },
    # 扎西东智 <-> 时亚坤（政府正副职）
    {
        "person_a": 3, "person_b": 5,
        "type": "superior_subordinate",
        "context": "时亚坤作为副县长协助县长扎西东智工作",
        "overlap_org": "班玛县人民政府",
        "overlap_period": "",
        "strength": "medium",
    },
    # 扎西东智 <-> 沈激（政府正副职）
    {
        "person_a": 3, "person_b": 8,
        "type": "superior_subordinate",
        "context": "沈激作为副县长协助县长扎西东智工作",
        "overlap_org": "班玛县人民政府",
        "overlap_period": "",
        "strength": "medium",
    },
    # 扎西东智 <-> 其他副县长
    {"person_a": 3, "person_b": 20, "type": "superior_subordinate", "context": "副县长公保才让协助县长扎西东智工作", "overlap_org": "班玛县人民政府", "overlap_period": "", "strength": "medium"},
    {"person_a": 3, "person_b": 21, "type": "superior_subordinate", "context": "副县长翟泽浩协助县长扎西东智工作", "overlap_org": "班玛县人民政府", "overlap_period": "", "strength": "medium"},
    {"person_a": 3, "person_b": 22, "type": "superior_subordinate", "context": "副县长宁格加协助县长扎西东智工作", "overlap_org": "班玛县人民政府", "overlap_period": "", "strength": "medium"},
    {"person_a": 3, "person_b": 23, "type": "superior_subordinate", "context": "副县长班玛尖参协助县长扎西东智工作", "overlap_org": "班玛县人民政府", "overlap_period": "", "strength": "medium"},
    {"person_a": 3, "person_b": 24, "type": "superior_subordinate", "context": "副县长杨峰协助县长扎西东智工作", "overlap_org": "班玛县人民政府", "overlap_period": "", "strength": "medium"},
    # 当周才郎 <-> 扎西（纪委监督人大）
    {
        "person_a": 12, "person_b": 15,
        "type": "overlap",
        "context": "纪委书记与人大常委会主任为班子同级成员",
        "overlap_org": "班玛县",
        "overlap_period": "",
        "strength": "weak",
    },
    # 县委常委之间（同一届常委班子）
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 6, "person_b": 11, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 12, "person_b": 9, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 12, "person_b": 11, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 13, "person_b": 12, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 13, "person_b": 11, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
    {"person_a": 13, "person_b": 9, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共班玛县委员会", "overlap_period": "", "strength": "medium"},
]

# ═══════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="班玛县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Build complete: 班玛县_network.db and 班玛县_network.gexf")
