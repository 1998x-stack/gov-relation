#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 乌兰县 (Wulan County),
海西蒙古族藏族自治州 (Haixi Prefecture), 青海省 (Qinghai Province).

Task ID: qinghai_乌兰县
Level: 县
Targets: 县委书记 & 县长
Investigation date: 2026-08-07
Confidence basis: 官方网站 www.wulanxian.gov.cn (直接抓取, 一手来源) ——
  2026年7月 乌兰县第十六次党代会 + 县第十八届人民代表大会第一次会议 + 政协十届一次会议
  换届完整报告; 人事任免通知; 领导之窗个别简况。

CURRENT OFFICEHOLDERS (2026-07换届后, 确认):
  - 县委书记: 潘立清 (2026-07起; 此前 2020/21-2026 任 县长)
  - 县长: 秦永娟 (2026-07-25 当选; 此前任 副县长、代理县长)

SUCCESSION:
  - 前任县委书记: 蒋冬梅 (2021-04-08 任职, 汉族/1979-12/四川大英, 青海民族大学+省委党校研究生,
    一级调研员; ~2026换届卸任)
  - 前任县长: 潘立清 (县长→县委书记 晋升典型)

NOTES:
  - Web 访问受限环境 (Exa/Jina/Baidu/Bing 被限或需JS/403), 主要依赖政府门户一手报告 +
    360百科 + 搜狐等二手交叉验证.
  - 官方"领导之窗"页面为 JS/AJAX 渲染, 潘立清/秦永娟 完整简历未直接抓取; 身份与职务均
    由 2026-07 官方大会报告直接确认.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "乌兰县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_乌兰县"
if _CURRENT_DIR.name == "qinghai_乌兰县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────
# id: 1-5 书记/前任, 6-10 政府, 11-15 人大/政协/两院, 16-20 常委/部门
persons = [
    # ═══ 县委书记 (Party Secretary) & predecessor ═══
    {
        "id": 1,
        "name": "潘立清",
        "gender": "男",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县委书记",
        "current_org": "中共乌兰县委员会",
        "source": "2026-07 县第十六届党代会执行主席/致闭幕词; 县政协十届一次会议(2026-07-24)报道明确'中共乌兰县委书记潘立清'. www.wulanxian.gov.cn",
    },
    {
        "id": 2,
        "name": "秦永娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县委副书记、县长",
        "current_org": "乌兰县人民政府",
        "source": "2026-07-25 县十八届人大一次会议当选县长; 2026-07-28 十八届县政府党组第1次会议由'县政府党组书记、代理县长秦永娟'主持并任县长. www.wulanxian.gov.cn",
    },
    {
        "id": 3,
        "name": "蒋冬梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-12",
        "birthplace": "四川大英",
        "education": "青海民族学院(2000.07 管理科学与经济秘书专业)+省委党校研究生",
        "party_join": "1999-12",
        "work_start": "2001",
        "current_post": "前乌兰县委书记(2021.04-2026.07)",
        "current_org": "中共乌兰县委员会",
        "source": "2021-04-08 海西州委干部大会宣布蒋冬梅任乌兰县委书记(替代李元兴); 百度百科/360百科; 一级调研员; 2025 仍有公开活动. 官方一手报道见 wulanxian.gov.cn 有关换届新闻.",
    },
    # ═══ 政府 (县长 + 常务副县长 + 援青副县长) ═══
    {
        "id": 4,
        "name": "管成权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-07",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县委常委、县政府党组副书记、副县长",
        "current_org": "乌兰县人民政府",
        "source": "乌兰县委常委、县人民政府党组副书记、副县长管成权同志简况 (2025-04-30). www.wulanxian.gov.cn",
    },
    {
        "id": 5,
        "name": "唐松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县委副书记、县政府党组成员、副县长(援青)",
        "current_org": "乌兰县人民政府",
        "source": "乌兰县委副书记、县人民政府党组成员、副县长(援青)唐松同志简况 (2025-09-10). 正处级. wulanxian.gov.cn",
    },
    {
        "id": 6,
        "name": "姬诚诚",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县委副书记、县政府党组成员、副县长(援青)",
        "current_org": "乌兰县人民政府",
        "source": "乌兰县人民政府领导之窗序列 (紧随管成权之后); 2026 党代会执行主席名单含'姬诚诚'. www.wulanxian.gov.cn",
    },
    # ═══ 县人大 / 政协 / 两院 ═══
    {
        "id": 7,
        "name": "任俊",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县人大常委会党组书记、主任",
        "current_org": "乌兰县人大常委会",
        "source": "县十八届人大一次会议执行主席/主持三次会议; 县政协十届一次会议报道'县人大常委会党组书记、主任任俊'. www.wulanxian.gov.cn",
    },
    {
        "id": 8,
        "name": "李永庆",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县政协主席",
        "current_org": "中国人民政治协商会议乌兰县委员会",
        "source": "2026-07-24 县政协十届一次会议当选主席; 曾任党代会执行主席. www.wulanxian.gov.cn",
    },
    {
        "id": 9,
        "name": "哈斯朝鲁",
        "gender": "男",
        "ethnicity": "蒙古族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县人民法院院长",
        "current_org": "乌兰县人民法院",
        "source": "2026-07-23 县十八届人大二次会议作法院工作报告; 法院院长. www.wulanxian.gov.cn",
    },
    {
        "id": 10,
        "name": "赵曼",
        "gender": "女(推测)",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌兰县人民检察院副检察长、代理检察长",
        "current_org": "乌兰县人民检察院",
        "source": "2026-07-23 人大会议作检察院工作报告; 副检察长、代理检察长. www.wulanxian.gov.cn",
    },
    # ═══ 其他 常委 / 主席团成员 (身份不明, 待补) ═══
    {
        "id": 11,
        "name": "杨珍果",
        "gender": "未知",
        "ethnicity": "未知", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乌兰县领导(党代会+人大执行主席)",
        "current_org": "乌兰县委员会/人大常委会",
        "source": "党代会及十八届人大执行主席名单 (2026-07). www.wulanxian.gov.cn",
    },
    {
        "id": 12,
        "name": "李娜",
        "gender": "未知", "ethnicity": "未知", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乌兰县领导(党代会+人大主席团成员)",
        "current_org": "乌兰县委员会/人大常委会",
        "source": "党代会及十八届人大主席团/执委会名单 (2026-07). www.wulanxian.gov.cn",
    },
    {
        "id": 13,
        "name": "陈植发",
        "gender": "未知", "ethnicity": "未知", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乌兰县领导(党代会执行主席)",
        "current_org": "中共乌兰县委员会",
        "source": "十六届党代会执行总裁副席 (2026-07-11). www.wulanxian.gov.cn",
    },
    {
        "id": 14,
        "name": "释嘉才让",
        "gender": "男", "ethnicity": "藏族(推测)", "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "乌兰县领导(党代会执行主席/统战宗教界)",
        "current_org": "乌兰县委/政协",
        "source": "十六届党代会执行主席名单 (2026-07-11). www.wulanxian.gov.cn",
    },
    # ═══ 政府部门负责人 (任免通知) ═══
    {
        "id": 15,
        "name": "索亚",
        "gender": "男", "ethnicity": "未知", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乌兰县民政局一级主任科员",
        "current_org": "乌兰县民政局",
        "source": "乌兰县人事任免通知 (2024-10-22). www.wulanxian.gov.cn",
    },
    {
        "id": 16,
        "name": "蔡贵梅",
        "gender": "女", "ethnicity": "未知", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乌兰县农牧和科技局副局长、三级主任科员",
        "current_org": "乌兰县农牧和科技局",
        "source": "乌兰县人事任免通知 (2024-10-22). www.wulanxian.gov.cn",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共乌兰县委员会", "type": "党委", "level": "县级",
     "parent": "中共海西蒙古族藏族自治州委员会", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 2, "name": "乌兰县人民政府", "type": "政府", "level": "县级",
     "parent": "海西蒙古族藏族自治州人民政府", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 3, "name": "乌兰县人大常委会", "type": "人大", "level": "县级",
     "parent": "海西蒙古族藏族自治州人大常委会", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 4, "name": "中国人民政治协商会议乌兰县委员会", "type": "政协", "level": "县级",
     "parent": "中国人民政治协商会议海西蒙古族藏族自治州委员会", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 5, "name": "中共乌兰县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共海西蒙古族藏族自治州纪委", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 6, "name": "乌兰县监察委员会", "type": "政府", "level": "县级", "parent": "", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 7, "name": "乌兰县人民法院", "type": "政府", "level": "县级", "parent": "", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 8, "name": "乌兰县人民检察院", "type": "政府", "level": "县级", "parent": "", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 9, "name": "乌兰县民政局", "type": "政府", "level": "县级", "parent": "乌兰县人民政府", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 10, "name": "乌兰县农牧和科技局", "type": "政府", "level": "县级", "parent": "乌兰县人民政府", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 11, "name": "乌兰县公安局", "type": "政府", "level": "县级", "parent": "乌兰县人民政府", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 12, "name": "乌兰县委组织部", "type": "党委", "level": "县级", "parent": "中共乌兰县委员会", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 13, "name": "乌兰县委宣传部", "type": "党委", "level": "县级", "parent": "中共乌兰县委员会", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 14, "name": "乌兰县委统战部", "type": "党委", "level": "县级", "parent": "中共乌兰县委员会", "location": "青海省海西州乌兰县希里沟镇"},
    # 乡镇
    {"id": 15, "name": "希里沟镇", "type": "乡镇", "level": "乡科级", "parent": "乌兰县人民政府", "location": "青海省海西州乌兰县希里沟镇"},
    {"id": 16, "name": "茶卡镇", "type": "乡镇", "level": "乡科级", "parent": "乌兰县人民政府", "location": "青海省海西州乌兰县茶卡镇"},
    {"id": 17, "name": "柯柯镇", "type": "乡镇", "level": "乡科级", "parent": "乌兰县人民政府", "location": "青海省海西州乌兰县柯柯镇"},
    {"id": 18, "name": "铜普镇", "type": "乡镇", "level": "乡科级", "parent": "乌兰县人民政府", "location": "青海省海西州乌兰县铜普镇"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "乌兰县委书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级",
     "note": "2026-07 第十六届党代会换届后任职; 此前任县长."},
    {"person_id": 1, "org_id": 2, "title": "乌兰县县长(前任职务)", "start_date": "2020/21", "end_date": "2026-07", "rank": "正处级",
     "note": "县长→县委书记 典型晋升; 2020-07 县委任免通知提到潘立清."},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "乌兰县委副书记、县长", "start_date": "2026-07-25", "end_date": "present", "rank": "正处级",
     "note": "2026-07-25 县十八届人大一次会议当选; 此前任副县长、代理县长."},
    {"person_id": 2, "org_id": 2, "title": "乌兰县人民政府副县长、代理县长", "start_date": "", "end_date": "2026-07-25", "rank": "副处级",
     "note": "换届前职(副县长→代理县长)."},
    {"person_id": 2, "org_id": 1, "title": "乌兰县委副书记", "start_date": "2026", "end_date": "present", "rank": "正处级",
     "note": "县委副书记、县长 双职."},
    # 前任书记 (Historical)
    {"person_id": 3, "org_id": 1, "title": "乌兰县委书记(前任)", "start_date": "2021-04-08", "end_date": "2026-07", "rank": "正处级",
     "note": "2021-04-08 任; 至2026换届卸任; 一级调研员."},
    {"person_id": 3, "org_id": 4, "title": "中共德令哈市委副书记(海西州属市)", "start_date": "~2018", "end_date": "2020", "rank": "副处级",
     "note": "任乌兰书记前职务(360百科确认)."},
    {"person_id": 3, "org_id": 20, "title": "共青团海西州委书记", "start_date": "~2016", "end_date": "2017", "rank": "正处级",
     "note": "2016-2017 团地委书记; 360百科/天峻发布."},
    {"person_id": 3, "org_id": 21, "title": "海西州人民政府副秘书长", "start_date": "2012-02-20", "end_date": "~2015", "rank": "副处级",
     "note": "2012-02-20 海西州政府任免 (大柴旦行委转载)."},
    # 政府领导
    {"person_id": 4, "org_id": 2, "title": "乌兰县委常委、县政府党组副书记、副县长(常务)", "start_date": "~2023", "end_date": "present", "rank": "正处级",
     "note": "2025-04-30 简况; 现任常务副县长."},
    {"person_id": 5, "org_id": 2, "title": "乌兰县委副书记、县政府党组成员、副县长(援青)", "start_date": "~2025", "end_date": "present", "rank": "正处级",
     "note": "2025-09-10 简况; 援青干部, 博士."},
    {"person_id": 6, "org_id": 2, "title": "乌兰县委副书记、县政府党组成员、副县长(援青)", "start_date": "~2025", "end_date": "present", "rank": "副处级",
     "note": "援青干部; 党代会执行主席名录."},
    # 人大/政协/两院
    {"person_id": 7, "org_id": 3, "title": "乌兰县人大常委会党组书记、主任", "start_date": "~2021", "end_date": "present", "rank": "正处级",
     "note": "2026-07 主持十八届人大会议; 政协会议报道确认党组/主任."},
    {"person_id": 8, "org_id": 4, "title": "乌兰县政协主席", "start_date": "2026-07-24", "end_date": "present", "rank": "正处级",
     "note": "县政协十届一次会议当选主席."},
    {"person_id": 9, "org_id": 7, "title": "乌兰县人民法院院长", "start_date": "~2021", "end_date": "present", "rank": "副处级",
     "note": "2026-07-23 作法院工作报告."},
    {"person_id": 10, "org_id": 8, "title": "乌兰县人民检察院副检察长、代理检察长", "start_date": "2026", "end_date": "present", "rank": "副处级",
     "note": "2026-07-23 作检察院代理工作报告."},
    # 其他常委/主席团
    {"person_id": 11, "org_id": 1, "title": "乌兰县领导(执行主席)", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "党代会及人大执行主席(2026-07)."},
    {"person_id": 12, "org_id": 1, "title": "乌兰县领导(主席团)", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "党代会及人大主席团/执行主席(2026-07)."},
    {"person_id": 13, "org_id": 1, "title": "乌兰县领导(党代会执行主席)", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "十六届党代会执行主席(2026-07-11)."},
    {"person_id": 14, "org_id": 1, "title": "乌兰县领导(统战宗教界)", "start_date": "", "end_date": "present", "rank": "",
     "note": "十六届党代会执行主席/统战宗教界(推测)."},
    # 部门
    {"person_id": 15, "org_id": 9, "title": "县民政局一级主任科员", "start_date": "2024-10", "end_date": "present", "rank": "一级主任科员",
     "note": "2024-10-22 任免通知."},
    {"person_id": 16, "org_id": 10, "title": "县农牧和科技局副局长、三级主任科员", "start_date": "2024-10", "end_date": "present", "rank": "三级主任科员",
     "note": "2024-10-22 任免通知."},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # 1. 书记×县长 (核心搭班子)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭班子(2026-07 换届后)", "overlap_org": "中共乌兰县委员会/乌兰县人民政府", "overlap_period": "2026-07起"},
    # 2. 书记×人大
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与人大主任同为换届大会执行主席/主持人", "overlap_org": "乌兰县第十八届人民代表大会", "overlap_period": "2026-07"},
    # 3. 县长×人大
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "县长在县人大会议上作政府工作报告并当选", "overlap_org": "乌兰县第十八届人民代表大会", "overlap_period": "2026-07"},
    # 4. 前任书记→现任书记 (交接)
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "蒋冬梅卸任乌兰县委书记, 潘立清接任(2026-07 换届)", "overlap_org": "中共乌兰县委员会", "overlap_period": "2026-07"},
    # 5. 前任县长→现任县长 (交接)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "潘立清由县长晋升书记, 秦永娟由代理县长当选县长", "overlap_org": "乌兰县人民政府", "overlap_period": "2026-07"},
    # 6. 书记×常务副县长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与常务副县长(政府党组副书记)", "overlap_org": "中共乌兰县委员会/乌兰县人民政府", "overlap_period": "2023-2026"},
    # 7. 县长×常务副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长搭班子", "overlap_org": "乌兰县人民政府", "overlap_period": "2026-07起"},
    # 8. 书记×政协主席
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记在政协十届一次会议作闭幕讲话(党委领导政协)", "overlap_org": "政协乌兰县委员会", "overlap_period": "2026-07"},
    # 9. 县长×政协主席
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "县长应邀莅临政协会议指导", "overlap_org": "政协乌兰县委员会", "overlap_period": "2026-07"},
    # 10. 书记×援青副县长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与援青县委副书记/副县长(上下级)", "overlap_org": "中共乌兰县委员会/乌兰县人民政府", "overlap_period": "2025-2026"},
    # 11. 援青搭档 唐松×姬诚诚
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "两位援青县委副书记/副县长同搭政府班子", "overlap_org": "乌兰县人民政府", "overlap_period": "2025-2026"},
    # 12. 人大×两院
    {"person_a": 7, "person_b": 9, "type": "superior_subordinate",
     "context": "县人大听取法院工作报告并强化表决通过", "overlap_org": "乌兰县第十八届人民代表大会", "overlap_period": "2026-07"},
    {"person_a": 7, "person_b": 10, "type": "superior_subordinate",
     "context": "县人大听取检察院工作报告并强化表决通过", "overlap_org": "乌兰县第十八届人民代表大会", "overlap_period": "2026-07"},
]

# ── Person JSON Builders ───────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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


def _write_person_jsons_main() -> None:
    configs = [
        ("县委书记", "潘立清", _build_pan_liqing_json()),
        ("县长", "秦永娟", _build_qin_yongjuan_json()),
        ("前任县委书记", "蒋冬梅", make_jiang_dongmei_json()),
    ]
    for job, name, data in configs:
        filename = f"{TODAY}-青海省-海西蒙古族藏族自治州-{job}-{name}.json"
        filepath = PJSON_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")


def _common_scope(job: str) -> dict:
    return {
        "province": "青海省",
        "city": "海西蒙古族藏族自治州",
        "region": "乌兰县",
        "job": job,
        "task_id": "qinghai_乌兰县",
        "time_focus": "2021-2026",
    }


def _build_pan_liqing_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _common_scope("县委书记"),
        "identity": {
            "person_id": "qinghai_wulanxian_panliqing",
            "name": "潘立清",
            "aliases": [],
            "gender": "男",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "潘立清_", "name_birthplace": "潘立清_",
                            "official_profile_url": "http://www.wulanxian.gov.cn"},
        },
        "current_status": {
            "current_post": "乌兰县委书记",
            "current_org": "中共乌兰县委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-08-07",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S005"],
        },
        "career_timeline": [
            {"start": "2026-07", "end": "present", "org": "中共乌兰县委员会", "title": "乌兰县委书记",
             "level": "正处级", "location": "青海省海西州乌兰县", "system": "party", "rank": "正处级",
             "is_key_promotion": True,
             "notes": "2026年7月第十六届党代会换届后任县委书记; 于党委人大政协全会致/主持." ,
             "confidence": "confirmed", "source_ids": ["S001", "S005"]},
            {"start": "2020-2021", "end": "2026-07", "org": "乌兰县人民政府", "title": "乌兰县委副书记、县长",
             "level": "正处级", "location": "青海省海西州乌兰县", "system": "government", "rank": "正处级",
             "is_key_promotion": True,
             "notes": "此前任乌兰县县长(县长→书记晋升) .2020-07 县委任免通知提到潘立清.",
             "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "notes": "公开资料未找到潘立清任县长前的完整履历(出生/教育/更早职务待补).",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [
            {"org_id": 1, "org_name": "中共乌兰县委员会", "role": "县委书记", "period": "2026-07至"},
            {"org_id": 2, "org_name": "乌兰县人民政府", "role": "县长(前任)", "period": "2021-2026"},
        ],
        "relationships": [
            {"person": "秦永娟", "person_id": "qinghai_huangxian_qinyongjuan", "relationship_type": "superior_subordinate",
             "strength": "strong", "evidence": "县委书记与县长(新班子搭档)",
             "overlap_org": "中共乌兰县委员会/乌兰县人民政府", "overlap_period": "2026-07起",
             "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
            {"person": "蒋冬梅", "person_id": "qinghai_huangxian_jiangdongmei", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "蒋冬梅卸任, 潘立清接任县委书记(2026换届)",
             "overlap_org": "中共乌兰县委员会", "overlap_period": "2026-07",
             "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
            {"person": "任俊", "person_id": "qinghai_huangxian_renjun", "relationship_type": "overlap",
             "strength": "medium", "evidence": "书记与人大主任共为换届大会/执行主席",
             "overlap_org": "乌兰县第十八届人民代表大会", "overlap_period": "2026-07",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "other", "achievement_or_event": "主持/领导乌兰县第十六届党代会及十八届人大换届",
             "role_in_event": "县委书记", "measurable_outcome": "完成县委、政府换届选举",
             "location": "乌兰县", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["青海省", "海西州"],
            "promotion_velocity": {"summary": "县长→县委书记(2026) 晋升", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "stability_oriented", "evidence": "换届大会强调围绕县委部署抓落实, 保持换届新气象", "confidence": "plausible", "source_ids": ["S001"]}],
            "speech_themes": ["生态保护", "产业兴县", "小而美", "乡村振兴"],
            "management_signals": [],
            "caveat": "Work style inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "当前公开检索未见潘立清负面/纪律信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "中国共产党乌兰县第十六次代表大会胜利闭幕", "url": "http://www.wulanxian.gov.cn/info/1385/69528.htm",
             "publisher": "乌兰发布/乌兰县人民政府", "published_at": "2026-07-12", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "潘立清主持闭幕并致词(县委书记)"},
            {"id": "S002", "title": "乌兰县第十八届人民代表大会第一次会议隆重开幕", "url": "http://www.wulanxian.gov.cn/info/1385/69584.htm",
             "publisher": "乌兰发布", "published_at": "2026-07-22", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "县长秦永娟作政府工作报告; 潘立清执行主席"},
            {"id": "S005", "title": "中国人民政协会议乌兰县第十届委员会第一次会议胜利闭幕", "url": "http://www.wulanxian.gov.cn/info/1385/69610.htm",
             "publisher": "乌兰发布", "published_at": "2026-07-24", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "明确'中共乌兰县委书记潘立清'作讲话"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "partial",
                               "relationship_confidence": "medium", "biggest_gap": "潘立清出生年份、籍贯、教育及任县长前完整履历"},
        "open_questions": [
            {"priority": "critical", "question": "潘立清的出生年份、籍贯、教育背景?", "why_it_matters": "去重与网络匹配",
             "suggested_queries": ["潘立清 简历 乌兰", "潘立清 青海 县长", "潘立清 海西州"], "last_attempted": AS_OF},
            {"priority": "high", "question": "潘立清任乌兰县长之前的职务、何时到任乌兰?", "why_it_matters": "判断职业轨迹与潜在任职交集",
             "suggested_queries": ["潘立清 任职 乌兰 县长 历任"], "last_attempted": AS_OF},
        ],
    }


def _build_qin_yongjuan_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _common_scope("县长"),
        "identity": {
            "person_id": "qinghai_huangxian_qinyongjuan",
            "name": "秦永娟",
            "aliases": [],
            "gender": "女",
            "ethnicity": "",
            "birth": "", "birthplace": "", "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "秦永娟_", "name_birthplace": "秦永娟_", "official_profile_url": "http://www.wulanxian.gov.cn"},
        },
        "current_status": {
            "current_post": "乌兰县委副书记、县长",
            "current_org": "乌兰县人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-08-07",
            "is_current_confirmed": True,
            "source_ids": ["S002", "S006"],
        },
        "career_timeline": [
            {"start": "2026-07-25", "end": "present", "org": "乌兰县人民政府", "title": "乌兰县委副书记、县长",
             "level": "正处级", "location": "青海省海西州乌兰县", "system": "government", "rank": "正处级",
             "is_key_promotion": True, "notes": "2026-07-25 县十八届人大一次会议当选县长; 出任县政府党组书记. 2026-07-28 主持十八届县政府党组第一次会议.",
             "confidence": "confirmed", "source_ids": ["S002", "S006"]},
            {"start": "unknown", "end": "2026-07-25", "org": "乌兰县人民政府", "title": "乌兰县人民政府副县长、代理县长",
             "level": "副处级", "location": "青海省海西州乌兰县", "system": "government", "rank": "副处级",
             "is_key_promotion": True, "notes": "换届前为副县长, 后任代理县长, 在人大会上做政府工作报告.",
             "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "notes": "秦永娟任副县长前的完整履历(出生、教育、先前职务)待补.",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [
            {"org_id": 2, "org_name": "乌兰县人民政府", "role": "县长(当选)", "period": "2026-07-25至"},
            {"org_id": 1, "org_name": "中共乌兰县委员会", "role": "县委副书记", "period": "2026-07至"},
        ],
        "relationships": [
            {"person": "潘立清", "person_id": "qinghai_huangxian_panliqing", "relationship_type": "superior_subordinate",
             "strength": "strong", "evidence": "县长在县委领导下, 政府党组书记/县长搭档",
             "overlap_org": "中共乌兰县委员会/乌兰县人民政府", "overlap_period": "2026-07起",
             "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002", "S006"]},
            {"person": "任俊", "person_id": "qinghai_huangxian_renjun", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县长在县人大作政府工作报告并当选; 人大主席主持",
             "overlap_org": "乌兰县第十八届人民代表大会", "overlap_period": "2026-07-25",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "governance_record": [
            {"period": "2026-07-22", "domain": "economic_development", "achievement_or_event": "县十八届人大一次会议作政府工作报告(过去五年, 未来五年)",
             "role_in_event": "县长", "measurable_outcome": "'十四五'收官; 提出 2026 生态、产业等八方面部署",
             "location": "乌兰县", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown",
            "systems_experience": ["government"], "geographic_pattern": ["青海省", "海西州"],
            "promotion_velocity": {"summary": "副县长→代理县长→县长(2026) 晋升", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "pragmatic", "evidence": "政府工作报强调项目投资、民生实事、落实政策", "confidence": "plausible", "source_ids": ["S002"]}],
            "speech_themes": ["生态", "项目投资", "乡村振兴", "民生福祉"],
            "management_signals": [], "caveat": "Work style inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "当前公开检索未发现秦永娟负面/纪律信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S002", "title": "乌兰县第十八届人民代表大会第一次会议隆重开幕", "url": "http://www.wulanxian.gov.cn/info/1385/69584.htm",
             "publisher": "乌兰发布", "published_at": "2026-07-22", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "代县长秦永娟作政府工作报告"},
            {"id": "S006", "title": "十八届县政府召开党组第1次会议", "url": "http://www.wulanxian.gov.cn/info/1025/69636.htm",
             "publisher": "乌兰发布", "published_at": "2026-07-29", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "县政府党组书记、县长秦永娟主持"},
            {"id": "S005", "title": "政协乌兰县第十届委员会第一次会议胜利闭幕", "url": "http://www.wulanxian.gov.cn/info/1385/69610.htm",
             "publisher": "乌兰发布", "published_at": "2026-07-24", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "县委副书记、县政府党组书记、副县长、代县长秦永娟"},
        ],
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "秦永娟出生年月、教育、任副县长前履历"},
        "open_questions": [
            {"priority": "critical", "question": "秦永娟的出生年月、籍贯、教育背景?", "why_it_matters": "身份去重与个人画像",
             "suggested_queries": ["秦永娟 简历 乌兰", "秦永娟 青海 县长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "秦永娟任乌兰县代理县长前任何职、何时调任乌兰?", "why_it_matters": "职业轨迹与前职关系",
             "suggested_queries": ["秦永娟 副县长 任命 乌兰"], "last_attempted": AS_OF},
        ],
    }


def make_jiang_dongmei_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _common_scope("前任县委书记"),
        "identity": {
            "person_id": "qinghai_huangxian_jiangdongmei",
            "name": "蒋冬梅",
            "aliases": [],
            "gender": "女", "ethnicity": "汉族", "birth": "1979-12", "birthplace": "四川大英", "native_place": "四川大英",
            "education": [{"period": "1998.09-2000.07", "institution": "青海民族学院管理科学系", "degree": "大专/本?",
                           "major": "经济(文秘)", "study_type": "full_time", "source_ids": ["S101"]},
                          {"period": "", "institution": "中共青海省委党校", "degree": "研究生", "study_type": "party_school", "source_ids": ["S102"]}],
            "party_join": "1999-12", "work_start": "2001",
            "dedupe_keys": {"name_birth": "蒋冬梅_1979", "name_birthplace": "蒋冬梅_四川大英", "official_profile_url": "baike.baidu.com"},
        },
        "current_status": {
            "current_post": "卸任乌兰县委书记(2026.07)",
            "current_org": "中共乌兰县委员会",
            "administrative_rank": "一级调研员",
            "as_of": "2026-08-07",
            "is_current_confirmed": False,
            "source_ids": ["S100"],
        },
        "career_timeline": [
            {"start": "2001", "end": "2012", "org": "海西州政府系统", "title": "州政府办公室/秘书岗位(履历待补)", "level": "",
             "location": "德令哈", "system": "government", "rank": "", "is_key_promotion": False,
             "notes": "2001年参加工作; 早期具体职务未见.",
             "confidence": "unverified", "source_ids": []},
            {"start": "2012-02-20", "end": "~2015", "org": "海西蒙古族藏族自治州人民政府", "title": "海西州人民政府副秘书长", "level": "副处级",
             "location": "德令哈市", "system": "government", "rank": "副处级", "is_key_promotion": True,
             "notes": "2012-02-20 海西州政府任免. 2012-10 仍为州政府副秘书长.",
             "confidence": "confirmed", "source_ids": ["S103"]},
            {"start": "~2016", "end": "2017", "org": "共青团海西蒙古族州委", "title": "共青团海西州委书记", "level": "正处级",
             "location": "德令哈市", "system": "other", "rank": "正处级", "is_key_promotion": True,
             "notes": "2016-12 赴天峻检查; 2017-02 主持团州委工作.",
             "confidence": "confirmed", "source_ids": ["S104", "S105"]},
            {"start": "~2018", "end": "2020", "org": "中共德令哈市委员会", "title": "德令哈市委副书记", "level": "副处级",
             "location": "德令哈市", "system": "party", "rank": "副处级", "is_key_promotion": True,
             "notes": "查看360. 360'已出任中共德令哈市委副书记'. 任乌兰书记前职(履历缺口时界 2018-2020).",
             "confidence": "plausible", "source_ids": ["S102"]},
            {"start": "2021-04-08", "end": "2026-07", "org": "中共乌兰县委员会", "title": "乌兰县委书记", "level": "正处级",
             "location": "青海省海西州乌兰县", "system": "party", "rank": "正处级", "is_key_promotion": True,
             "notes": "担任至 2026 换届; 期间百货(一级调研员). 曾检在任至2026-07.",
             "confidence": "confirmed", "source_ids": ["S100", "S106"]},
        ],
        "organizations": [
            {"org_id": 1, "org_name": "中共乌兰县委员会", "role": "县委书记", "period": "2021.04-2026.07"},
            {"org_id": 19, "org_name": "中共德令哈市委员会", "role": "德令哈市委副书记", "period": "~2018-2020"},
            {"org_id": 20, "org_name": "共青团海西州委", "role": "团州委书记", "period": "2016-2017"},
            {"org_id": 21, "org_name": "海西州人民政府", "role": "州政府副秘书长", "period": "2012-~2015"},
        ],
        "relationships": [
            {"person": "潘立清", "person_id": "qinghai_huangxian_panliqing", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "蒋卸任乌兰书记, 潘接任(2026换届)",
             "overlap_org": "中共乌兰县委员会", "overlap_period": "2026-07",
             "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S100", "S106"]},
        ],
        "governance_record": [
            {"period": "2021-2026", "domain": "other", "achievement_or_event": "任乌兰县委书记五年(完成'十四五'收官与换届)", "role_in_event": "县委书记",
             "measurable_outcome": "乌兰县'十四五'建设, 生态/盐湖文旅发展", "location": "乌兰县", "confidence": "confirmed", "source_ids": ["S106"]},
        ],
        "professional_profile": {"primary_specializations": ["行政", "共青团", "县域治理"], "secondary_specializations": [],
                                 "career_pattern": "cross_county_rotation", "systems_experience": ["government", "party", "other"],
                                 "geographic_pattern": ["四川(籍)", "青海省海西州"], "promotion_velocity": {"summary": "州府副秘书长→团州委书记→德哈市委副书记→县委书记", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
                                       "caveat": "Work style inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "检索未发现蒋冬梅任内被处/负面的于乌兰事件(前任李元兴被查为接任前的事)", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S100", "title": "乌兰县委书记蒋冬梅同志简况/新闻", "url": "baike.baidu.com", "publisher": "百度百科",
             "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "青年青海乌兰县委书记, 一级调研员"},
            {"id": "S101", "title": "青海民族师范学院干嘛经济秘书专业", "url": "baike.baidu.com (课程/人物履历)", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF,
             "source_type": "encyclopedia", "reliability": "medium", "notes": "2000.07毕业"},
            {"id": "S102", "title": "蒋冬梅(中共德令哈市委副书记)", "url": "https://baike.so.com/doc/2316697-26850971.html", "publisher": "360百科",
             "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "省委党校研究生; 德哈市委副书记"},
            {"id": "S103", "title": "海西州政府任免通知(蒋冬梅)", "url": "www.dachaidan.gov.cn", "publisher": "大柴旦行委转载(海西州政府)", "published_at": "2012-02-20", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "任命为州政府副秘书长"},
            {"id": "S104", "title": "共青团海西州委书记蒋冬梅赴天峻调研", "url": "", "publisher": "天峻发布(微信)", "published_at": "2016-12-15", "accessed_at": AS_OF,
             "source_type": "media", "reliability": "medium", "notes": "团州委书记"},
            {"id": "S106", "title": "2021-04-08 海西州委在乌兰干部大会宣布", "url": "", "publisher": "手机搜狐/新闻", "published_at": "2021-04-08", "accessed_at": AS_OF,
             "source_type": "media", "reliability": "medium", "notes": "李元兴不再任县委书记, 蒋冬梅任"},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "plausible(卸任)", "career_completeness": "partial",
                               "relationship_confidence": "medium", "biggest_gap": "2017-2020 德令哈市委副书记与乌兰之间的精确时间及 2001-2011 早期职"},
        "open_questions": [
            {"priority": "high", "question": "蒋冬梅 2017-2020 从团州委书记到德令哈市委副书记的具体职务与时间?", "why_it_matters": "跨市履历轨迹",
             "suggested_queries": ["蒋冬梅 德令哈 市委副书记 任命"], "last_attempted": AS_OF},
            {"priority": "high", "question": "蒋冬梅 2001-2011 早期具体岗位(州政府办公室?)", "why_it_matters": "早期职业轨迹",
             "suggested_queries": ["蒋冬梅 海西州 2001 分配", "蒋冬梅 州政府秘书"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "蒋冬梅 2026 换届卸任去向(是否留任州级)?", "why_it_matters": "干部流向",
             "suggested_queries": ["蒋冬梅 2026 任命"], "last_attempted": AS_OF},
        ],
    }


_write_person_jsons_main()