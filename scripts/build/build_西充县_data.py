#!/usr/bin/env python3
"""
西充县 (Xichong County, Nanchong City, Sichuan Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-26
数据来源:
  - 西充县人民政府官网领导信息 (www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/)
  - 西充县新闻网领导活动栏目

置信度说明:
  - 来自官网领导页的信息标为 confirmed
  - 来自新闻报道的信息标为 confirmed（有具体报道日期）
  - 履历早期信息难以从外网获取，标为 plausible 或 unverified
"""

import sqlite3
import os
import sys
from datetime import datetime

TODAY = "2026-07-26"
SLUG = "西充县"
PROVINCE = "四川省"
PARENT_CITY = "南充市"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "西充县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "西充县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共西充县委员会", "type": "党委", "level": "县级", "parent": "中共南充市委", "location": "四川省南充市西充县"},
    {"id": 2, "name": "西充县人民政府", "type": "政府", "level": "县级", "parent": "南充市人民政府", "location": "四川省南充市西充县"},
    {"id": 3, "name": "中共西充县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共西充县委员会", "location": "四川省南充市西充县"},
    {"id": 4, "name": "西充县监察委员会", "type": "政府", "level": "县级", "parent": "西充县人民政府", "location": "四川省南充市西充县"},
    {"id": 5, "name": "西充县委政法委员会", "type": "党委", "level": "县级", "parent": "中共西充县委员会", "location": "四川省南充市西充县"},
    {"id": 6, "name": "中共西充县委组织部", "type": "党委", "level": "县级", "parent": "中共西充县委员会", "location": "四川省南充市西充县"},
    {"id": 7, "name": "中共西充县委宣传部", "type": "党委", "level": "县级", "parent": "中共西充县委员会", "location": "四川省南充市西充县"},
    {"id": 8, "name": "中共西充县委统战部", "type": "党委", "level": "县级", "parent": "中共西充县委员会", "location": "四川省南充市西充县"},
    {"id": 9, "name": "西充县公安局", "type": "政府", "level": "县级", "parent": "西充县人民政府", "location": "四川省南充市西充县"},
    {"id": 10, "name": "西充县人民武装部", "type": "政府", "level": "县级", "parent": "南充军分区", "location": "四川省南充市西充县"},
    {"id": 11, "name": "西充县总工会", "type": "群团", "level": "县级", "parent": "中共西充县委员会", "location": "四川省南充市西充县"},
]

# ── Persons ──
persons = [
    # 1. 县委书记
    {
        "id": 1,
        "name": "何鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共西充县委员会",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/sj/hp/202410/t20241012_2025375.html",
    },
    # 2. 县长
    {
        "id": 2,
        "name": "张洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "西充县人民政府",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/fsj/zhb_12261/202209/t20220914_1724743.html",
    },
    # 3: 县委专职副书记
    {
        "id": 3,
        "name": "张洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共西充县委员会",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/fsj/zh/202508/t20250813_2241050.html",
    },
    # 4: 县委常委、副县长（常务）
    {
        "id": 4,
        "name": "龚诚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "西充县人民政府",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/gc/t_1141545.html",
    },
    # 5: 县委常委、政法委书记
    {
        "id": 5,
        "name": "屠继东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共西充县委政法委员会",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/tjd/t_2259909.html",
    },
    # 6: 县委常委、统战部部长
    {
        "id": 6,
        "name": "涂开美",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共西充县委统战部",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/tkm/202205/t20220508_1141544.html",
    },
    # 7: 县委常委、总工会主席
    {
        "id": 7,
        "name": "姚艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、总工会主席",
        "current_org": "西充县总工会",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/yy/202311/t20231129_1904089.html",
    },
    # 8: 县委常委、人武部部长
    {
        "id": 8,
        "name": "彭永金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、人武部部长",
        "current_org": "西充县人民武装部",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/pyj/202402/t20240201_1935441.html",
    },
    # 9: 县委常委、组织部部长
    {
        "id": 9,
        "name": "赵全昱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共西充县委组织部",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/zqy/t_2259921.html",
    },
    # 10: 县委常委、宣传部部长
    {
        "id": 10,
        "name": "黄永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共西充县委宣传部",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/hyq/202406/t20240620_1985274.html",
    },
    # 11: 县委常委、纪委书记（监委代主任）
    {
        "id": 11,
        "name": "冯敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "西充县纪律检查委员会",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/fm/202509/t20250908_2261079.html",
    },
    # 12: 县委常委、副县长（挂职）
    {
        "id": 12,
        "name": "苏茂科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "西充县人民政府",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xw/cw/smk/202509/t20250908_2261080.html",
    },
    # 13: 副县长、公安局局长
    {
        "id": 13,
        "name": "兰耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "西充县公安局",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xzf/fxz/ly/202205/t20220508_1141558.html",
    },
    # 14: 副县长
    {
        "id": 14,
        "name": "李红霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "西充县人民政府",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xzf/fxz/lhx/202205/t20220508_1141559.html",
    },
    # 15: 副县长
    {
        "id": 15,
        "name": "朱佳宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "西充县人民政府",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xzf/fxz/zjy/202205/t20220508_1141560.html",
    },
    # 16: 副县长
    {
        "id": 16,
        "name": "李灵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "西充县人民政府",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xzf/fxz/liling/202512/t20251202_2287837.html",
    },
    # 17: 副县长
    {
        "id": 17,
        "name": "王洪林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "西充县人民政府",
        "source": "https://www.xichong.gov.cn/zwgk/fdzdgknr/dwjj/ldxx/xzf/fxz/whl/202501/t20250108_2063950.html",
    },
]

# ── Positions ──
positions = [
    # 何鹏
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "2024年10月官网显示为县委书记，2026-07-20 仍有活动报道"},
    # 张洪波
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "县政府党组书记，2026-07 现任"},
    {"person_id": 2, "org_id": 1, "title": "县政府党组书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 张洪
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start": "", "end": "present", "rank": "副县级", "note": "协助党建、处理县委日常事务，2025-08 任命"},
    # 龚诚
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长（常务）", "start": "", "end": "present", "rank": "副县级", "note": "负责常务工作、发展改革、财税金融等"},
    # 屠继东
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 涂开美
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "统战部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 姚艳
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 11, "title": "总工会主席", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 彭永金
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "人武部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 赵全昱
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副县级", "note": "2025-09 任命"},
    # 黄永强
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 冯敏
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": "2025-09 任命"},
    {"person_id": 11, "org_id": 3, "title": "纪委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "监委代主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 苏茂科
    {"person_id": 12, "org_id": 1, "title": "县委常委（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "2025-09 挂职"},
    {"person_id": 12, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 兰耀
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 9, "title": "公安局局长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李红霞
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 朱佳宇
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李灵
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "2025-12 任命"},
    # 王洪林
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "2025-01 任命"},
]

# ── Relationships ──
relationships = [
    # 何鹏 - 张洪波：党政一把手协作
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政正职协作", "overlap_org": "中共西充县委员会/西充县人民政府",
     "overlap_period": "2024-"},
    # 何鹏 - 张洪：县委正副书记协作
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与专职副书记领导关系", "overlap_org": "中共西充县委员会",
     "overlap_period": "2025-"},
    # 何鹏 - 各常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与县委常委、政法委书记", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与县委常委、统战部部长", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与县委常委、总工会主席", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与县委常委、人武部部长", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与县委常委、组织部部长", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与县委常委、宣传部部长", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记与县委常委、纪委书记", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记与挂职常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    # 张洪波 - 副县长们
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长", "overlap_org": "西充县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长、公安局局长", "overlap_org": "西充县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "西充县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "西充县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "西充县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "西充县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与挂职副县长", "overlap_org": "西充县人民政府",
     "overlap_period": ""},
    # 张洪波 - 张洪：副书记协作
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县委副书记、县长与专职副书记协作", "overlap_org": "中共西充县委员会",
     "overlap_period": "2025-"},
    # 常委交叉
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "overlap",
     "context": "组织部部长与宣传部部长同为县委系统", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
    {"person_a": 11, "person_b": 9, "type": "overlap",
     "context": "纪委书记与组织部部长同为常委", "overlap_org": "中共西充县委员会",
     "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════
# SQLite
# ═══════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
              p.get("birth",""), p.get("birthplace",""), p.get("education",""),
              p.get("party_join",""), p.get("work_start",""),
              p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent",""), o.get("location","")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"    Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")


# ═══════════════════════════════════════════════════════════════════════
# GEXF
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "副书记" not in role:
        return "255,50,50"    # Red: Party secretary
    elif "县长" in role or "区长" in role:
        return "50,100,255"   # Blue: Government head
    else:
        return "100,100,100"  # Grey: Other

def org_color(o):
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

def person_node_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_node_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue type="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worker_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue type="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue type="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    print("Done.")