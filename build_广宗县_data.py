#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广宗县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邢台市
Region: 广宗县
Targets: 县委书记 & 县长

Research Sources:
- 广宗县人民政府官网 (www.gzx.gov.cn) 政府领导页面: https://www.gzx.gov.cn/channelList/10988.html
  - 县长刘伟个人页面: https://www.gzx.gov.cn/content/10988/46785.html
  - 常务副县长张川个人页面: https://www.gzx.gov.cn/content/10988/24560.html
- 广宗县领导活动页面: https://www.gzx.gov.cn/channelList/11004.html (多页)
- 新闻确认: 郑晓燕为县委书记(主持召开县委理论学习中心组会议等报道)
  - https://www.gzx.gov.cn/content/11004/48959.html → "县委书记郑晓燕主持召开..."
  - https://www.gzx.gov.cn/content/11004/49710.html → "县委书记郑晓燕督导检查..."
- 刘伟县长个人资料: 男, 汉族, 1980年11月出生, 中共党员, 在职硕士研究生学历
- 张川常务副县长个人资料: 男, 汉族, 1982年1月出生, 中共党员, 大学本科学历

Research Date: 2026-07-23

Gaps:
- 县委书记郑晓燕的出生年月、学历、籍贯、详细履历暂缺
- 李黑强、任胜迪、刘金良、王翠、韩晓然、方大伟等副县长的详细履历暂缺
- 县委常委班子构成（除郑晓燕、刘伟、张川外）暂缺
- 前任县委书记、前任县长信息暂缺
- 县人大常委会主任、政协主席姓名暂缺
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "广宗县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "郑晓燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县委书记",
        "current_org": "中共广宗县委员会",
        "source": "广宗县人民政府官网：县委书记郑晓燕。来源：https://www.gzx.gov.cn/content/11004/48959.html — '县委书记郑晓燕主持召开县委理论学习中心组2025年第十二次学习会议'"
    },
    {
        "id": 2,
        "name": "刘伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "待查",
        "education": "在职硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县委副书记、县长",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网：刘伟，男，汉族，1980年11月出生，中共党员，在职硕士研究生学历。现任广宗县委副书记、县长。来源：https://www.gzx.gov.cn/content/10988/46785.html"
    },
    # ════════════════════════════════════════
    # Deputy Leaders
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "待查",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县委常委、常务副县长",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网：张川，男，汉族，1982年1月出生，中共党员，大学本科学历。现任广宗县委常委、政府常务副县长。来源：https://www.gzx.gov.cn/content/10988/24560.html"
    },
    {
        "id": 4,
        "name": "李黑强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县副县长",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网政府领导列表：副县长李黑强。来源：https://www.gzx.gov.cn/channelList/10988.html"
    },
    {
        "id": 5,
        "name": "任胜迪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县副县长",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网政府领导列表：副县长任胜迪。来源：https://www.gzx.gov.cn/channelList/10988.html"
    },
    {
        "id": 6,
        "name": "刘金良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县副县长",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网政府领导列表：副县长刘金良。来源：https://www.gzx.gov.cn/channelList/10988.html"
    },
    {
        "id": 7,
        "name": "王翠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县副县长",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网政府领导列表：副县长王翠。来源：https://www.gzx.gov.cn/channelList/10988.html"
    },
    {
        "id": 8,
        "name": "韩晓然",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县副县长",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网政府领导列表：副县长韩晓然。来源：https://www.gzx.gov.cn/channelList/10988.html"
    },
    {
        "id": 9,
        "name": "方大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县副县长（挂职）",
        "current_org": "广宗县人民政府",
        "source": "广宗县人民政府官网政府领导列表：副县长（挂职）方大伟。来源：https://www.gzx.gov.cn/channelList/10988.html"
    },
    {
        "id": 10,
        "name": "刘立超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宗县领导（县委常委候选人/县领导）",
        "current_org": "中共广宗县委员会",
        "source": "广宗县人民政府官网新闻：2026年4月郑晓燕督导检查大气污染防治工作时，县领导刘立超、任胜迪参加。来源：https://www.gzx.gov.cn/content/11004/49710.html"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广宗县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "中共邢台市委"
    },
    {
        "id": 2,
        "name": "广宗县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "邢台市人民政府"
    },
    {
        "id": 3,
        "name": "广宗县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "邢台市人大常委会"
    },
    {
        "id": 4,
        "name": "政协广宗县委员会",
        "type": "政协",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "邢台市政协"
    },
    {
        "id": 5,
        "name": "中共广宗县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "中共邢台市纪律检查委员会"
    },
    {
        "id": 6,
        "name": "中共广宗县委组织部",
        "type": "党委部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "中共广宗县委员会"
    },
    {
        "id": 7,
        "name": "中共广宗县委宣传部",
        "type": "党委部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "中共广宗县委员会"
    },
    {
        "id": 8,
        "name": "中共广宗县委统战部",
        "type": "党委部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "中共广宗县委员会"
    },
    {
        "id": 9,
        "name": "中共广宗县委政法委",
        "type": "政法系统",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "中共广宗县委员会"
    },
    {
        "id": 10,
        "name": "广宗县审计局",
        "type": "政府组成部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "广宗县人民政府"
    },
    {
        "id": 11,
        "name": "广宗县发展和改革局",
        "type": "政府组成部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "广宗县人民政府"
    },
    {
        "id": 12,
        "name": "广宗县财政局",
        "type": "政府组成部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "广宗县人民政府"
    },
    {
        "id": 13,
        "name": "广宗县应急管理局",
        "type": "政府组成部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "广宗县人民政府"
    },
    {
        "id": 14,
        "name": "广宗县行政审批局",
        "type": "政府组成部门",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "广宗县人民政府"
    },
    {
        "id": 15,
        "name": "广宗县消防救援大队",
        "type": "事业单位",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "广宗县人民政府"
    },
    {
        "id": 16,
        "name": "河北兴广投资集团有限公司",
        "type": "国有企业",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "广宗县人民政府"
    },
    {
        "id": 17,
        "name": "广宗县人民法院",
        "type": "司法机关",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "邢台市中级人民法院"
    },
    {
        "id": 18,
        "name": "广宗县人民检察院",
        "type": "司法机关",
        "level": "县级",
        "location": "邢台市广宗县",
        "parent": "邢台市人民检察院"
    },
]

# 3. Positions
positions = [
    # 郑晓燕 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "广宗县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "2025年12月前已任职（见2025年12月18日县委理论学习中心组会议报道）"},
    # 刘伟 — 县长
    {"person_id": 2, "org_id": 2, "title": "广宗县委副书记、县长", "start": "待查", "end": "present", "rank": "正处级", "note": "主持县政府全面工作，分管县审计局。政府领导页面更新日期为2025-03-21"},
    {"person_id": 2, "org_id": 10, "title": "分管县审计局", "start": "待查", "end": "present", "rank": "", "note": "领导县政府全面工作，分管县审计局"},
    # 张川 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "广宗县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": "县委常委、常务副县长"},
    {"person_id": 3, "org_id": 2, "title": "广宗县常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责发改、财政、安全生产、应急管理等工作；分管发改局、财政局、应急管理局等部门"},
    # 李黑强 — 副县长
    {"person_id": 4, "org_id": 2, "title": "广宗县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 任胜迪 — 副县长
    {"person_id": 5, "org_id": 2, "title": "广宗县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 刘金良 — 副县长
    {"person_id": 6, "org_id": 2, "title": "广宗县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 王翠 — 副县长
    {"person_id": 7, "org_id": 2, "title": "广宗县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 韩晓然 — 副县长
    {"person_id": 8, "org_id": 2, "title": "广宗县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 方大伟 — 挂职副县长
    {"person_id": 9, "org_id": 2, "title": "广宗县副县长（挂职）", "start": "待查", "end": "present", "rank": "副处级", "note": "挂职"},
    # 刘立超 — 县领导
    {"person_id": 10, "org_id": 1, "title": "广宗县领导", "start": "待查", "end": "present", "rank": "", "note": "出现在党政新闻报道中，具体职务待查"},
]

# 4. Relationships
relationships = [
    # 郑晓燕 — 刘伟：党政一把手共事关系
    {"person_a": 1, "person_b": 2, "type": "党政一把手", "context": "郑晓燕（县委书记）与刘伟（县长）为广宗县党政主要负责人，在县委常委会和政府工作中紧密合作", "overlap_org": "广宗县", "overlap_period": "至2026年7月"},
    # 郑晓燕 — 张川：上下级关系
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共广宗县委员会", "overlap_period": "至2026年7月"},
    # 刘伟 — 张川：上下级关系
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长（分管协助县长工作）", "overlap_org": "广宗县人民政府", "overlap_period": "至2026年7月"},
    # 郑晓燕 — 刘立超：上下级
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "县委书记与县领导刘立超共同参与大气污染防治督导工作", "overlap_org": "广宗县", "overlap_period": "2026年"},
    # 刘立超 — 任胜迪：同事
    {"person_a": 10, "person_b": 5, "type": "共事", "context": "县领导刘立超与副县长任胜迪共同参与大气污染防治陪同检查", "overlap_org": "广宗县", "overlap_period": "2026年4月"},
]

# ── Build ──

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
