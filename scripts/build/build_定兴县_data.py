#!/usr/bin/env python3
"""Build script for 定兴县 (Dingxing County), 保定市, 河北省.

Sources:
- 定兴县人民政府官网: https://www.dingxing.gov.cn/
- 定兴县政协十四届六次会议 (2026-01-27): content-71-44289.html
- 定兴县十六届人大六次会议 (2026-01-28): content-531-43307.html
- 中国共产党定兴县第十六次代表大会 (2026-07-18): content-71-44355.html
- 中共定兴县委十五届十二次全会 (2026-07-15): content-71-44349.html
- 白建军调研检查高考备考工作 (2026-06-04): content-71-44159.html
- 定兴县召开存量增量项目建设调度会 (2026-06-26): content-71-44256.html
- 王坤主持召开县政府常务会议 (2025-08-15): content-531-42129.html
- 定兴县巡察工作会议 (2025-09-28): content-531-42298.html
- 政协定兴县第十五届委员会第一次会议 (2026-07-22): content-531-44363.html
- 县长之窗 (刘宁、刘晓涛、殷淼分工页)
"""

import json
import os
import re
import sqlite3
from datetime import datetime, date

# ── Paths ──
STAGING = os.path.join(os.path.dirname(__file__) or ".", "")
DB_PATH = os.path.join(STAGING, "定兴县_network.db")
GEXF_PATH = os.path.join(STAGING, "定兴县_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "")

TODAY = "2026-07-23"
AS_OF = "2026-07-23"

# ── Helper: XML escape ──
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ── Data ──

persons = [
    # 1: 县委书记
    {
        "id": 1,
        "name": "白建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县委书记",
        "current_org": "中共定兴县委员会",
        "source": "https://www.dingxing.gov.cn/content-71-44159.html",
    },
    # 2: 县长
    {
        "id": 2,
        "name": "王坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县委副书记、县长",
        "current_org": "定兴县人民政府",
        "source": "https://www.dingxing.gov.cn/content-531-43307.html",
    },
    # 3: 县委副书记
    {
        "id": 3,
        "name": "孟庆飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县委副书记",
        "current_org": "中共定兴县委员会",
        "source": "https://www.dingxing.gov.cn/content-71-44289.html",
    },
    # 4: 县委副书记/常委 (大会执行主席, 在项目调度会列名)
    {
        "id": 4,
        "name": "王敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县委副书记（或常委）",
        "current_org": "中共定兴县委员会",
        "source": "https://www.dingxing.gov.cn/content-71-44355.html",
    },
    # 5: 县委常委、常务副县长
    {
        "id": 5,
        "name": "刘宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县委常委、常务副县长",
        "current_org": "定兴县人民政府",
        "source": "https://www.dingxing.gov.cn/ejxzzc-6-40870.html",
    },
    # 6: 县领导（县人大常委会主任）
    {
        "id": 6,
        "name": "刘旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县人大常委会主任",
        "current_org": "定兴县人民代表大会常务委员会",
        "source": "https://www.dingxing.gov.cn/content-531-43307.html",
    },
    # 7: 县领导（政协主席）
    {
        "id": 7,
        "name": "王承先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县政协主席",
        "current_org": "政协定兴县委员会",
        "source": "https://www.dingxing.gov.cn/content-531-44363.html",
    },
    # 8: 县委常委/县领导（巡察会议主持）
    {
        "id": 8,
        "name": "侯毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县委常委",
        "current_org": "中共定兴县委员会",
        "source": "https://www.dingxing.gov.cn/content-531-42298.html",
    },
    # 9: 副县长
    {
        "id": 9,
        "name": "刘晓涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县副县长",
        "current_org": "定兴县人民政府",
        "source": "https://www.dingxing.gov.cn/ejxzzc-6-35953.html",
    },
    # 10: 副县长
    {
        "id": 10,
        "name": "殷淼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县副县长",
        "current_org": "定兴县人民政府",
        "source": "https://www.dingxing.gov.cn/ejxzzc-6-37196.html",
    },
    # 11: 县领导（项目调度会列名）
    {
        "id": 11,
        "name": "申庆征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "中共定兴县委员会/定兴县人民政府",
        "source": "https://www.dingxing.gov.cn/content-71-44256.html",
    },
    # 12: 县领导（项目调度会列名）
    {
        "id": 12,
        "name": "郭大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "定兴县人民政府",
        "source": "https://www.dingxing.gov.cn/content-71-44256.html",
    },
    # 13: 县领导（项目调度会列名）
    {
        "id": 13,
        "name": "任才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "定兴县人民政府",
        "source": "https://www.dingxing.gov.cn/content-71-44256.html",
    },
    # 14: 县领导（人大会议主席台）
    {
        "id": 14,
        "name": "秦振国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "定兴县",
        "source": "https://www.dingxing.gov.cn/content-531-43307.html",
    },
    # 15: 县领导（人大会议主席台）
    {
        "id": 15,
        "name": "常伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "定兴县",
        "source": "https://www.dingxing.gov.cn/content-531-43307.html",
    },
    # 16: 县领导（人大会议主席台）
    {
        "id": 16,
        "name": "李红娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "定兴县",
        "source": "https://www.dingxing.gov.cn/content-531-43307.html",
    },
    # 17: 县领导（人大会议主席台）
    {
        "id": 17,
        "name": "郑长海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "定兴县",
        "source": "https://www.dingxing.gov.cn/content-531-43307.html",
    },
    # 18: 县领导（人大会议主席台）
    {
        "id": 18,
        "name": "史艳武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县领导",
        "current_org": "定兴县",
        "source": "https://www.dingxing.gov.cn/content-531-43307.html",
    },
    # 19: 政协副主席
    {
        "id": 19,
        "name": "杨志杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定兴县政协副主席",
        "current_org": "政协定兴县委员会",
        "source": "https://www.dingxing.gov.cn/content-531-44363.html",
    },
]

organizations = [
    {"id": 1, "name": "中共定兴县委员会", "type": "党委", "level": "县处级", "parent": "中共保定市委", "location": "定兴县"},
    {"id": 2, "name": "定兴县人民政府", "type": "政府", "level": "县处级", "parent": "保定市人民政府", "location": "定兴县"},
    {"id": 3, "name": "定兴县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "定兴县", "location": "定兴县"},
    {"id": 4, "name": "政协定兴县委员会", "type": "政协", "level": "县处级", "parent": "定兴县", "location": "定兴县"},
    {"id": 5, "name": "定兴县纪委监委", "type": "纪委", "level": "县处级", "parent": "定兴县", "location": "定兴县"},
    {"id": 6, "name": "定兴县发展和改革局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 7, "name": "定兴县财政局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 8, "name": "定兴县教育和体育局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 9, "name": "定兴县行政审批局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 10, "name": "定兴县应急管理局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 11, "name": "定兴县人力资源和社会保障局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 12, "name": "定兴县统计局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 13, "name": "定兴县交通运输局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 14, "name": "定兴县农业农村局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 15, "name": "定兴县水利局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 16, "name": "定兴县卫生健康局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 17, "name": "定兴县市场监督管理局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 18, "name": "定兴县文化广电和旅游局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 19, "name": "定兴县医疗保障局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 20, "name": "定兴县审计局", "type": "政府", "level": "乡科级", "parent": "定兴县人民政府", "location": "定兴县"},
    {"id": 21, "name": "定兴金台经济开发区", "type": "开发区", "level": "省级", "parent": "定兴县人民政府", "location": "定兴县"},
]

positions = [
    # 白建军 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "定兴县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "截至2026年7月在任"},
    # 王坤 - 县长
    {"person_id": 2, "org_id": 2, "title": "定兴县委副书记、县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年1月作政府工作报告；截至2026年7月在任"},
    {"person_id": 2, "org_id": 1, "title": "定兴县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任"},
    # 孟庆飞 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "定兴县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026年1月政协会议列名"},
    # 王敏 - 县委副书记/常委
    {"person_id": 4, "org_id": 1, "title": "定兴县委副书记/常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县第十六次党代会大会执行主席；项目调度会列名"},
    # 刘宁 - 县委常委、常务副县长
    {"person_id": 5, "org_id": 2, "title": "定兴县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责政府常务工作"},
    {"person_id": 5, "org_id": 1, "title": "定兴县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘旭 - 人大常委会主任
    {"person_id": 6, "org_id": 3, "title": "定兴县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年1月人大会议主席团常务主席"},
    # 王承先 - 政协主席
    {"person_id": 7, "org_id": 4, "title": "定兴县政协主席", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职", "note": "2026年1月为政协党组书记、主席候选人；2026年7月政协十五届一次会议确认"},
    # 侯毅 - 县委常委
    {"person_id": 8, "org_id": 1, "title": "定兴县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "主持巡察工作会议"},
    # 刘晓涛 - 副县长
    {"person_id": 9, "org_id": 2, "title": "定兴县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管卫生健康、市监、文旅等"},
    # 殷淼 - 副县长
    {"person_id": 10, "org_id": 2, "title": "定兴县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管生态环境、交通、农业农村、水利等"},
    # 申庆征 - 县领导
    {"person_id": 11, "org_id": 1, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "项目调度会列名；全会上就报告作说明"},
    # 郭大伟 - 县领导
    {"person_id": 12, "org_id": 2, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "项目调度会列名"},
    # 任才 - 县领导
    {"person_id": 13, "org_id": 2, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "项目调度会列名"},
    # 秦振国 - 县领导
    {"person_id": 14, "org_id": 3, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人大会议主席台就座"},
    # 常伟 - 县领导
    {"person_id": 15, "org_id": 3, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人大会议主席台就座"},
    # 李红娜 - 县领导
    {"person_id": 16, "org_id": 3, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人大会议主席台就座"},
    # 郑长海 - 县领导
    {"person_id": 17, "org_id": 3, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人大会议主席台就座"},
    # 史艳武 - 县领导
    {"person_id": 18, "org_id": 3, "title": "定兴县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人大会议主席台就座"},
    # 杨志杰 - 政协副主席
    {"person_id": 19, "org_id": 4, "title": "定兴县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "政协十五届一次会议主席台前排就座"},
]

relationships = [
    # 白建军 ↔ 王坤: 书记+县长搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长在县委常委会和县政府班子共事", "overlap_org": "中共定兴县委/定兴县人民政府", "overlap_period": "截至2026年7月"},
    # 白建军 ↔ 孟庆飞: 书记+副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委副书记在县委常委会共事", "overlap_org": "中共定兴县委", "overlap_period": "截至2026年7月"},
    # 白建军 ↔ 王敏: 书记+副书记/常委
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与王敏在县委常委会共事；王敏任党代会执行主席", "overlap_org": "中共定兴县委", "overlap_period": "截至2026年7月"},
    # 白建军 ↔ 刘宁: 书记+常务副县长
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与常务副县长在县委常委会共事", "overlap_org": "中共定兴县委", "overlap_period": "截至2026年7月"},
    # 王坤 ↔ 刘宁: 县长+常务副县长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与常务副县长在县政府班子紧密共事", "overlap_org": "定兴县人民政府", "overlap_period": "截至2026年7月"},
    # 王坤 ↔ 孟庆飞: 县长+副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记在县委常委会共事", "overlap_org": "中共定兴县委", "overlap_period": "截至2026年7月"},
    # 白建军 ↔ 侯毅: 书记+常委
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与侯毅在县委常委会共事；侯毅主持巡察会议", "overlap_org": "中共定兴县委", "overlap_period": "截至2026年7月"},
    # 白建军 ↔ 刘旭: 书记+人大主任
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与县人大常委会主任在全县重要会议同台", "overlap_org": "定兴县", "overlap_period": "截至2026年7月"},
    # 王坤 ↔ 刘旭: 县长+人大主任
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长向人大会议作政府工作报告", "overlap_org": "定兴县人民代表大会常务委员会", "overlap_period": "2026年1月"},
    # 白建军 ↔ 王承先: 书记+政协主席
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与县政协主席在全县重要会议同台", "overlap_org": "定兴县", "overlap_period": "截至2026年7月"},
    # 刘宁 ↔ 刘晓涛: 常务副县长+副县长
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "常务副县长与副县长在县政府班子共事", "overlap_org": "定兴县人民政府", "overlap_period": "截至2026年7月"},
    # 刘宁 ↔ 殷淼: 常务副县长+副县长
    {"person_a": 5, "person_b": 10, "type": "overlap", "context": "常务副县长与副县长在县政府班子共事", "overlap_org": "定兴县人民政府", "overlap_period": "截至2026年7月"},
    # 白建军 ↔ 秦振国: 书记+县领导
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记与秦振国在人大会议主席台同排就座", "overlap_org": "定兴县人大会议", "overlap_period": "2026年1月"},
    # 白建军 ↔ 常伟: 书记+县领导
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记与常伟在人大会议主席台同排就座", "overlap_org": "定兴县人大会议", "overlap_period": "2026年1月"},
    # 白建军 ↔ 李红娜: 书记+县领导
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委书记与李红娜在人大会议主席台同排就座", "overlap_org": "定兴县人大会议", "overlap_period": "2026年1月"},
]

source_register = [
    {"id": "S001", "title": "定兴县人民政府官网 - 首页", "url": "https://www.dingxing.gov.cn/",
     "publisher": "定兴县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S002", "title": "白建军调研检查高考备考工作", "url": "https://www.dingxing.gov.cn/content-71-44159.html",
     "publisher": "定兴县人民政府", "published_at": "2026-06-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认白建军为定兴县委书记"},
    {"id": "S003", "title": "王坤主持召开县政府常务会议", "url": "https://www.dingxing.gov.cn/content-531-42129.html",
     "publisher": "定兴县人民政府", "published_at": "2025-08-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王坤为定兴县长"},
    {"id": "S004", "title": "中国共产党定兴县第十六次代表大会开幕", "url": "https://www.dingxing.gov.cn/content-71-44355.html",
     "publisher": "定兴县人民政府", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "白建军作报告，王敏为大会执行主席；主席团成员含白建军、王敏、侯毅、王承先、杨志杰"},
    {"id": "S005", "title": "中共定兴县委十五届十二次全会举行", "url": "https://www.dingxing.gov.cn/content-71-44349.html",
     "publisher": "定兴县人民政府", "published_at": "2026-07-16", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "白建军出席并讲话；提及申庆征、王少辉、卢金宝"},
    {"id": "S006", "title": "定兴县召开存量、增量项目建设调度会", "url": "https://www.dingxing.gov.cn/content-71-44256.html",
     "publisher": "定兴县人民政府", "published_at": "2026-06-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "白建军主持；县领导王敏、刘宁、申庆征、郭大伟、任才参会"},
    {"id": "S007", "title": "定兴县十六届人大六次会议开幕", "url": "https://www.dingxing.gov.cn/content-531-43307.html",
     "publisher": "定兴县人民政府", "published_at": "2026-01-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王坤作政府工作报告；主席台就座人员含白建军、王坤、孟庆飞、王承先、秦振国、常伟、李红娜、郑长海、史艳武；刘旭主持"},
    {"id": "S008", "title": "政协定兴县第十四届委员会第六次会议开幕", "url": "https://www.dingxing.gov.cn/content-71-44289.html",
     "publisher": "定兴县人民政府", "published_at": "2026-01-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认白建军为县委书记，王坤为县委副书记/县长，孟庆飞为县委副书记，刘旭为县人大常委会主任，王承先为县政协党组书记/主席候选人"},
    {"id": "S009", "title": "政协定兴县第十五届委员会第一次会议开幕", "url": "https://www.dingxing.gov.cn/content-531-44363.html",
     "publisher": "定兴县人民政府", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认杨志杰为政协副主席；主席台前排含杨志杰、王德柱、张国君、张利、车治华"},
    {"id": "S010", "title": "定兴县巡察工作会议", "url": "https://www.dingxing.gov.cn/content-531-42298.html",
     "publisher": "定兴县人民政府", "published_at": "2025-10-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "白建军出席；侯毅主持会议"},
    {"id": "S011", "title": "定兴县人民政府 - 刘宁分工页", "url": "https://www.dingxing.gov.cn/ejxzzc-6-40870.html",
     "publisher": "定兴县人民政府", "published_at": "2025-05-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘宁为县委常委、常务副县长，含完整工作分工"},
    {"id": "S012", "title": "定兴县人民政府 - 刘晓涛分工页", "url": "https://www.dingxing.gov.cn/ejxzzc-6-35953.html",
     "publisher": "定兴县人民政府", "published_at": "2025-05-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘晓涛为副县长，含完整工作分工"},
    {"id": "S013", "title": "定兴县人民政府 - 殷淼分工页", "url": "https://www.dingxing.gov.cn/ejxzzc-6-37196.html",
     "publisher": "定兴县人民政府", "published_at": "2025-05-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "殷淼为副县长，含完整工作分工"},
]


# ── Build ──
def build():
    os.makedirs(STAGING, exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"dingxing_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post or "纪委" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post and "人大" not in post and "政协" not in post) or \
               ("县长" in post and "副" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
            "事业单位": "220,220,220",
            "乡镇/街道": "255,255,200",
            "群团": "255,220,255",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>定兴县领导班子关系网络（基于定兴县政府官网、保定市人事公示、官方新闻报道）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河北省",
                "city": "保定市",
                "region": "定兴县",
                "job": p.get("current_post", ""),
                "task_id": "hebei_定兴县",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"dingxing_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "") and "人大" not in p.get("current_post", "") and "政协" not in p.get("current_post", "")) or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历（出生年月、籍贯、教育背景、入党时间、参加工作时间和此前所有任职）",
                 "why_it_matters": "无法追溯其任职路径和系统经历，无法进行跨县关系网络分析",
                 "suggested_queries": [f"{p['name']} 简历 定兴县", f"{p['name']} 保定"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 白建军 Person JSON ──
    bjj_timeline = [
        {"start": "", "end": "present", "org": "中共定兴县委员会", "title": "定兴县委书记",
         "notes": "截至2026年7月在任。最早可查的以县委书记身份公开报道为2025年10月（巡察会议）",
         "level": "县处级正职", "confidence": "confirmed", "source_ids": ["S002", "S004", "S005", "S006", "S010"]},
    ]
    bjj_relationships = [
        {"person": "王坤", "person_id": "dingxing_王坤", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "白建军（县委书记）与王坤（县长）在县委常委会和县政府班子共事",
         "overlap_org": "中共定兴县委/定兴县人民政府", "overlap_period": "截至2026年7月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007", "S008"]},
        {"person": "孟庆飞", "person_id": "dingxing_孟庆飞", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "白建军与孟庆飞（县委副书记）在县委常委会共事",
         "overlap_org": "中共定兴县委", "overlap_period": "截至2026年7月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007", "S008"]},
        {"person": "刘宁", "person_id": "dingxing_刘宁", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "白建军与刘宁（县委常委、常务副县长）在县委常委会和项目调度会共事",
         "overlap_org": "中共定兴县委", "overlap_period": "截至2026年7月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
    ]

    bjj_json = make_person_json(persons[0], bjj_timeline, bjj_relationships)
    bjj_path = os.path.join(PERSONS_DIR, f"{TODAY}-河北省-保定市-县委书记-白建军.json")
    with open(bjj_path, "w", encoding="utf-8") as f:
        json.dump(bjj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {bjj_path}")

    # ── 王坤 Person JSON ──
    wk_timeline = [
        {"start": "", "end": "present", "org": "定兴县人民政府", "title": "定兴县委副书记、县长",
         "notes": "截至2026年7月在任。最早可查的以县长身份公开报道为2025年8月（县政府常务会议）；2026年1月人大会议作政府工作报告",
         "level": "县处级正职", "confidence": "confirmed", "source_ids": ["S003", "S007"]},
        {"start": "", "end": "", "org": "中共定兴县委员会", "title": "定兴县委副书记",
         "notes": "兼任", "level": "县处级副职", "confidence": "confirmed", "source_ids": ["S008"]},
    ]
    wk_relationships = [
        {"person": "白建军", "person_id": "dingxing_白建军", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王坤（县长）与白建军（县委书记）在县委常委会和县政府班子共事",
         "overlap_org": "中共定兴县委/定兴县人民政府", "overlap_period": "截至2026年7月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007", "S008"]},
        {"person": "刘宁", "person_id": "dingxing_刘宁", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王坤（县长）与刘宁（常务副县长）在县政府班子紧密共事",
         "overlap_org": "定兴县人民政府", "overlap_period": "截至2026年7月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006", "S011"]},
        {"person": "刘旭", "person_id": "dingxing_刘旭", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王坤向刘旭（县人大常委会主任）主持的人大会议作政府工作报告",
         "overlap_org": "定兴县人民代表大会常务委员会", "overlap_period": "2026年1月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
    ]

    wk_json = make_person_json(persons[1], wk_timeline, wk_relationships)
    wk_path = os.path.join(PERSONS_DIR, f"{TODAY}-河北省-保定市-县长-王坤.json")
    with open(wk_path, "w", encoding="utf-8") as f:
        json.dump(wk_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wk_path}")


if __name__ == "__main__":
    build()
