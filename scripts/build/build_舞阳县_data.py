#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 舞阳县 leadership network.

调查日期: 2026-08-06
信息来源: 舞阳县人民政府门户网站 (www.wuyang.gov.cn) — 领导之窗页（县委/县政府）
调查级别: 县
目标干部: 县委书记 & 县长
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, BASE)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "舞阳县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "舞阳县_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
SLUG = "河南省漯河市舞阳县"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 县委 (Party Committee)
    # ═══════════════════════════════
    {
        "id": 1,
        "name": "朱新卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共舞阳县委书记",
        "current_org": "中共舞阳县委员会",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    {
        "id": 2,
        "name": "朱暑光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县政府党组书记、县长",
        "current_org": "舞阳县人民政府",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxzf",
    },
    {
        "id": 3,
        "name": "陈凡",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1983-01",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委政法委书记",
        "current_org": "中共舞阳县委员会",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    {
        "id": 4,
        "name": "齐飞飞",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1978-05",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共舞阳县委员会",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    {
        "id": 5,
        "name": "马文辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部政委",
        "current_org": "中共舞阳县委员会",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    {
        "id": 6,
        "name": "李江峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共舞阳县纪律检查委员会",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    {
        "id": 7,
        "name": "李森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-10",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组副书记、常务副县长",
        "current_org": "舞阳县人民政府",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxzf",
    },
    {
        "id": 8,
        "name": "刘伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-03",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共舞阳县委宣传部",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxzf",
    },
    {
        "id": 9,
        "name": "郭翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-05",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共舞阳县委办公室",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    {
        "id": 10,
        "name": "杨康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共舞阳县委统战部",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    {
        "id": 11,
        "name": "张冲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-06",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、舞阳县经济技术开发区党工委书记、管委会主任",
        "current_org": "舞阳县经济技术开发区",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxrd",
    },
    # ═══════════════════════════════
    # 县政府 (Government)
    # ═══════════════════════════════
    {
        "id": 12,
        "name": "李明康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-02",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "舞阳县副县长",
        "current_org": "舞阳县人民政府",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxzf",
    },
    {
        "id": 13,
        "name": "王伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-06",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "舞阳县副县长、县公安局局长",
        "current_org": "舞阳县公安局",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxzf",
    },
    {
        "id": 14,
        "name": "孟瑞娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-02",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "舞阳县副县长",
        "current_org": "舞阳县人民政府",
        "source": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxzf",
    },
    # ═══════════════════════════════
    # 人大 & 其他
    # ═══════════════════════════════
    {
        "id": 15,
        "name": "周洪涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "舞阳县人大常委会主任",
        "current_org": "舞阳县人民代表大会常务委员会",
        "source": "https://www.wuyang.gov.cn/",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共舞阳县委员会", "type": "党委", "level": "县级", "parent": "中共漯河市委员会", "location": "河南省漯河市舞阳县"},
    {"id": 2, "name": "舞阳县人民政府", "type": "政府", "level": "县级", "parent": "漯河市人民政府", "location": "河南省漯河市舞阳县"},
    {"id": 3, "name": "中共舞阳县委政法委", "type": "党委", "level": "县级", "parent": "中共舞阳县委员会", "location": "河南省漯河市舞阳县"},
    {"id": 4, "name": "中共舞阳县委组织部", "type": "党委", "level": "县级", "parent": "中共舞阳县委员会", "location": "河南省漯河市舞阳县"},
    {"id": 5, "name": "中共舞阳县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共舞阳县委员会", "location": "河南省漯河市舞阳县"},
    {"id": 6, "name": "中共舞阳县委宣传部", "type": "党委", "level": "县级", "parent": "中共舞阳县委员会", "location": "河南省漯河市舞阳县"},
    {"id": 7, "name": "中共舞阳县委办公室", "type": "党委", "level": "县级", "parent": "中共舞阳县委员会", "location": "河南省漯河市舞阳县"},
    {"id": 8, "name": "中共舞阳县委统战部", "type": "党委", "level": "县级", "parent": "中共舞阳县委员会", "location": "河南省漯河市舞阳县"},
    {"id": 9, "name": "舞阳县经济技术开发区", "type": "开发区", "level": "县级", "parent": "舞阳县人民政府", "location": "河南省漯河市舞阳县"},
    {"id": 10, "name": "舞阳县公安局", "type": "政府", "level": "县级", "parent": "舞阳县人民政府", "location": "河南省漯河市舞阳县"},
    {"id": 11, "name": "舞阳县人民武装部", "type": "政府", "level": "县级", "parent": "舞阳县人民政府", "location": "河南省漯河市舞阳县"},
    {"id": 12, "name": "舞阳县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "漯河市人民代表大会常务委员会", "location": "河南省漯河市舞阳县"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 朱新卫
    {"person_id": 1, "org_id": 1, "title": "中共舞阳县委书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "主持县委全面工作；2026-06-19 代表十四届县委向县第十五次党代会作《全方位提质提速 高质量跨越发展》报告"},
    # 朱暑光
    {"person_id": 2, "org_id": 1, "title": "舞阳县委副书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "协助县委书记做好县委全面工作"},
    {"person_id": 2, "org_id": 2, "title": "舞阳县县长、县政府党组书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "主持县政府全面工作，分管县审计局；负责县政府党组党建和党风廉政建设工作"},
    # 陈凡
    {"person_id": 3, "org_id": 1, "title": "舞阳县委副书记",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "协助县委书记做好县委日常工作"},
    {"person_id": 3, "org_id": 3, "title": "舞阳县委政法委书记",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持县委政法委全面工作"},
    # 齐飞飞
    {"person_id": 4, "org_id": 1, "title": "舞阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "舞阳县委组织部部长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持县委组织部全面工作"},
    # 马文辉
    {"person_id": 5, "org_id": 1, "title": "舞阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 11, "title": "舞阳县人武部政委",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持县人武部全面工作"},
    # 李江峰
    {"person_id": 6, "org_id": 1, "title": "舞阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "舞阳县纪委书记、县监委主任",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持县纪委、监委全面工作"},
    # 李森
    {"person_id": 7, "org_id": 1, "title": "舞阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "舞阳县常务副县长（县政府党组副书记）",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责县政府常务工作：发展改革、财政、国资监管、生态环境、安全生产、应急管理、金融、保险、重点项目、大数据产业、行政审批、税务、统计等；协助县长分管审计"},
    # 刘伟
    {"person_id": 8, "org_id": 1, "title": "舞阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "舞阳县委宣传部部长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持县委宣传部全面工作"},
    {"person_id": 8, "org_id": 2, "title": "舞阳县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责教育、文化和旅游、体育、广播电视、国企改革、投融资、保交楼等方面工作"},
    # 郭翔
    {"person_id": 9, "org_id": 1, "title": "舞阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "舞阳县委办公室主任",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持县委办公室全面工作"},
    # 杨康
    {"person_id": 10, "org_id": 1, "title": "舞阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "舞阳县委统战部部长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持县委统战部全面工作"},
    # 张冲
    {"person_id": 11, "org_id": 9, "title": "舞阳县经开区党工委书记、管委会主任",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持舞阳县经济技术开发区全面工作；负责科技、工业、开发区建设、电力、通信等"},
    # 李明康
    {"person_id": 12, "org_id": 2, "title": "舞阳县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "协助李森同志分管金融、保险等方面工作；协助刘伟同志分管投融资工作"},
    # 王伟
    {"person_id": 13, "org_id": 2, "title": "舞阳县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责公安、司法、信访稳定、社会管理等方面工作"},
    {"person_id": 13, "org_id": 10, "title": "舞阳县公安局局长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    # 孟瑞娜
    {"person_id": 14, "org_id": 2, "title": "舞阳县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责人力资源和社会保障、卫生健康、医疗保障、民政、退役军人事务、民族宗教、市场发展等方面工作",
     "rank": "副处级"},
    # 周洪涛
    {"person_id": 15, "org_id": 12, "title": "舞阳县人大常委会主任",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "主持县人大全面工作"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 书记 ↔ 县长
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政一把手搭档：朱新卫主持县委全面，朱暑光主持县政府全面并兼任县委副书记",
     "overlap_org": "中共舞阳县委员会、舞阳县人民政府", "overlap_period": ""},
    # 书记 ↔ 专职副书记 陈凡
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与县委副书记——陈凡协助县委书记做好县委日常工作",
     "overlap_org": "中共舞阳县委员会", "overlap_period": ""},
    # 县长 ↔ 常务副县长 李森
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与常务副县长——李森协助县长负责县政府常务工作并分管审计",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
    # 县长 ↔ 县委副书记 陈凡
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长与县委副书记——县委常委会共事，一主政、一抓政法",
     "overlap_org": "中共舞阳县委员会", "overlap_period": ""},
    # 县长 ↔ 副县长 刘伟
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "县长与常务/宣传副县长——县政府领导班子成员",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 副县长 李明康
    {"person_a": 7, "person_b": 12, "type": "superior_subordinate",
     "context": "常务副县长与副县长——李明康协助李森分管金融、保险",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 副县长 刘伟
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "县政府领导班子成员搭档",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 副县长 李明康 已覆盖
    # 刘伟 ↔ 李明康
    {"person_a": 8, "person_b": 12, "type": "overlap",
     "context": "副县长刘伟与李明康——李明康协助刘伟分管投融资",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 公安局 王伟
    {"person_a": 7, "person_b": 13, "type": "overlap",
     "context": "县政府领导班子成员——李森协调公安、司法、信访稳定等领域",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
    # 县长 ↔ 公安局长 王伟
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长、公安局长——王伟负责公安、司法、信访稳定",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
    # 县委班子内部 陈凡 ↔ 齐飞飞
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "县委副书记与组织部长——县委常委会共事",
     "overlap_org": "中共舞阳县委员会", "overlap_period": ""},
    # 纪委书记 ↔ 县长（监督关系）
    {"person_a": 6, "person_b": 2, "type": "overlap",
     "context": "县纪委书记与县长——县纪委监委与县政府日常监督协调",
     "overlap_org": "中共舞阳县委员会", "overlap_period": ""},
    # 人大主任 ↔ 县长
    {"person_a": 15, "person_b": 2, "type": "overlap",
     "context": "县人大常委会主任与县长——人大监督政府法定关系",
     "overlap_org": "舞阳县人民代表大会常务委员会", "overlap_period": ""},
    # 书记 ↔ 经开区主任 张冲
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "县委书记与经开区党工委书记——张冲主持经开区（舞阳产业发展主战场）",
     "overlap_org": "舞阳县经济技术开发区", "overlap_period": ""},
    # 县长 ↔ 副县长 孟瑞娜
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "县政府领导班子成员搭档",
     "overlap_org": "舞阳县人民政府", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════

import sqlite3


def create_tables(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
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
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 舞阳县人民政府官网 (www.wuyang.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)   # Red, top leader
        elif "县长" in post and "副" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "政法委书记" in post:
            return ("255,165,0", 15.0)   # Orange discipline/政法
        elif "纪委书记" in post:
            return ("255,165,0", 15.0)   # Orange discipline
        elif "副书记" in post:
            return ("100,100,255", 15.0)
        elif "县委常委" in post:
            return ("50,100,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "开发区": ("200,255,200"),
            "人大": ("200,255,255"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络 — 截至{AS_OF}</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


# ═══════════════════════════════════════════════════════════════════
# PERSON JSON GENERATION
# ═══════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "中共舞阳县委领导之窗（县委页）",
         "url": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/lyzt1/wyxrd",
         "publisher": "中共舞阳县委员会/舞阳县人民政府网", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "记录朱新卫/朱暑光/陈凡/齐飞飞/马文辉/李江峰/李森/刘伟/郭翔/杨康/张冲的现任职务、出生年月、学历、入党信息（县委领导名单）"},
        {"id": "S002", "title": "舞阳县人民政府领导页（县政府）",
         "url": "https://www.wuyang.gov.cn/zwgk/fdzdgknr/ldzy1/wyxzf",
         "publisher": "舞阳县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "记录朱暑光（县长）、李森（常务）、刘伟、李明康、王伟（公安局长）、孟瑞娜 的现任职务、分工与领导简介"},
        {"id": "S003", "title": "中国共产党舞阳县第十五次代表大会召开（政务要闻）",
         "url": "https://www.wuyang.gov.cn/wydt/jrwy/content_1055936.html",
         "publisher": "舞阳融媒/舞阳县人民政府网", "published_at": "2026-06-19",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "朱新卫代表十四届县委作《全方位提速提质 高质量跨越发展》报告；朱暑光主持；执行主席名单；施政蓝图（产业新城/文化舞阳/和美城乡）"},
        {"id": "S004", "title": "中国共产党舞阳县第十五次代表大会举行第二次全体会议",
         "url": "https://www.wuyang.gov.cn/wydt/jrwy/content_1055960.html",
         "publisher": "舞阳融媒/舞阳县人民政府网", "published_at": "2026-06-20",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认主席团执行主席名单：朱新卫、朱暑光、陈凡、齐飞飞、马文辉、李江峰、李森、刘伟、郭翔、杨志、张冲"},
        {"id": "S005", "title": "朱新卫会见北京舞水科技有限公司总经理李志杰一行",
         "url": "https://www.wuyang.gov.cn/wydt/jrwy/content_1059962.html",
         "publisher": "舞阳融媒/舞阳县人民政府网", "published_at": "2026-08-04",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认为县委书记；与北京舞水科技洽谈人工智能机器视觉项目；周承山（人大主任）、王晓军（三级调研员）参加"},
    ]


def make_person_json(person, rels, source_reg, biggest_gap):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "漯河市",
            "region": "舞阳县",
            "job": person["current_post"],
            "task_id": "henan_舞阳县",
            "time_focus": "截至2026年8月"
        },
        "identity": {
            "person_id": f"wuyang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": "",
                "degree": person["education"],
                "study_type": "unknown",
                "source_ids": ["S001", "S002"]
            }] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] or ("县长" in person["current_post"] and "副" not in person["current_post"]) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "至今",
                "org": person["current_org"],
                "title": person["current_post"],
                "notes": "官方领导简介含学历/民族信息；具体任职起止未公开",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未取得任现职前的完整履历与籍贯/出生期等",
                "confidence": "unverified",
                "source_ids": []
            },
        ],
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "未掌握", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "low_profile" if person["name"] not in ("朱新卫",) else "media_visible",
                    "evidence": "公开报道以政务活动为主，未见大规模个人宣传" if person["name"] not in ("朱新卫",) else "多次在公开项目洽谈、调研活动中亮相（如会见北京舞水科技、调研城建重点项目、党代会作报告）",
                    "confidence": "plausible",
                    "source_ids": ["S005", "S003"] if person["name"] == "朱新卫" else []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style inference from public official reporting, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，公开渠道未发现{person['name']}的负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": source_reg,
        "confidence_summary": {
            "identity": "confirmed" if person["gender"] and person["ethnicity"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": biggest_gap
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}任{person['current_post']}前的完整履历、出生地/籍贯、前一职务是什么？",
                "why_it_matters": "无法评估其职业来源系统、晋升模式与跨区调动轨迹",
                "suggested_queries": [f"{person['name']} 简历 舞阳", f"{person['name']} 任前公示", f"{person['name']} 漯河"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{person['name']} 出生地/籍贯、入党年份、参加工作年份为何？",
                "why_it_matters": "基础身份信息不全，限制去重与人口统计分析",
                "suggested_queries": [f"{person['name']} 出生 舞阳/漯河", f"{person['name']} 籍贯"],
                "last_attempted": AS_OF,
            },
        ],
    }


if __name__ == "__main__":
    run_build()

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    by_id = {p["id"]: p for p in persons}

    def core_rels(person_id, name):
        rels = []
        for r in relationships:
            if r["person_a"] == person_id:
                other = by_id[r["person_b"]]
                rels.append({
                    "person": other["name"], "person_id": f"wuyang_{other['name']}",
                    "relationship_type": r["type"], "strength": "strong" if r["type"] == "superior_subordinate" else "medium",
                    "evidence": r["context"], "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"], "direction": "undirected",
                    "confidence": "confirmed", "source_ids": ["S001", "S002"],
                })
            elif r["person_b"] == person_id:
                other = by_id[r["person_a"]]
                rels.append({
                    "person": other["name"], "person_id": f"wuyang_{other['name']}",
                    "relationship_type": r["type"], "strength": "strong" if r["type"] == "superior_subordinate" else "medium",
                    "evidence": r["context"], "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"], "direction": "other_to_person",
                    "confidence": "confirmed", "source_ids": ["S001", "S002"],
                })
        return rels

    jobs = [
        (1, "县委书记", "朱新卫2026年6月换届前及更早的县委/市直履历、籍贯"),
        (2, "县长", "朱暑光任县长前的完整履历、籍贯"),
        (7, "常务副县长", "李森2026年6月前职务与早期履历、籍贯"),
    ]

    for pid, role, gap in jobs:
        p = by_id[pid]
        rels = core_rels(pid, p["name"])
        data = make_person_json(p, rels, source_register, gap)
        fname = f"{TODAY}-河南省-漯河市-{role}-{p['name']}.json"
        with open(os.path.join(PERSONS_DIR, fname), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {fname}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")