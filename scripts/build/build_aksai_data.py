#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Aksai (阿克塞) cross-county cadre exchange network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/aksai_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/aksai_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ── Aksai County current and recent leaders ──
    {"id": 1, "name": "张桐", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿克塞县委书记", "current_org": "中共阿克塞县委员会",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E6%A1%90"},
    {"id": 2, "name": "库美斯剑", "gender": "女", "ethnicity": "哈萨克族",
     "birth": "1980-04", "birthplace": "", "education": "在职大学/省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿克塞县委副书记、县长", "current_org": "阿克塞县人民政府",
     "source": "https://www.aksai.gov.cn/zhengwu/ldzc/202407/t20240703_126106.htm"},
    {"id": 3, "name": "陶涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "", "education": "大学学历，农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "酒泉市人民政府党组成员、副市长", "current_org": "酒泉市人民政府",
     "source": "https://baike.baidu.com/item/%E9%99%B6%E6%B6%9B"},
    {"id": 4, "name": "张金荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-05", "birthplace": "甘肃酒泉", "education": "中央党校大学",
     "party_join": "1991-11", "work_start": "1984-07",
     "current_post": "酒泉市政协党组副书记、一级巡视员", "current_org": "酒泉市政协",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E9%87%91%E8%8D%A3"},
    {"id": 5, "name": "银雁", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "1966", "birthplace": "新疆巴里坤", "education": "",
     "party_join": "中共党员", "work_start": "1985",
     "current_post": "原阿克塞县长（被查）", "current_org": "",
     "source": "https://www.sohu.com/a/526768950_121331367"},
    {"id": 6, "name": "张鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1980", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "2005",
     "current_post": "阿克塞县委常委、常务副县长人选", "current_org": "中共阿克塞县委员会",
     "source": "https://www.sohu.com/a/774076523_121331367"},
    {"id": 7, "name": "张健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿克塞县委常委、宣传部部长", "current_org": "中共阿克塞县委员会",
     "source": "https://www.sohu.com/a/767655798_121331367"},
    {"id": 8, "name": "毛学文", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-11", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拟任县(市、区)党委副书记", "current_org": "",
     "source": "https://www.thepaper.cn/newsDetail_forward_10503054"},
    {"id": 9, "name": "白振林", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-06", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拟任市属国有企业正职", "current_org": "",
     "source": "https://www.thepaper.cn/newsDetail_forward_10503054"},
    {"id": 10, "name": "武海龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿克塞县政府副县长、县公安局局长", "current_org": "阿克塞县人民政府",
     "source": "https://www.sohu.com/a/704134652_121331367"},
    {"id": 11, "name": "钟兴鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-04", "birthplace": "", "education": "大学，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拟提名为县(市、区)政府副县(市、区)长人选", "current_org": "",
     "source": "https://www.thepaper.cn/newsDetail_forward_10503054"},
    {"id": 12, "name": "李珊珊", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "", "education": "大学，文学学士",
     "party_join": "无党派", "work_start": "",
     "current_post": "拟提名为市级群团组织正职候选人", "current_org": "",
     "source": "https://www.baidu.com/s?wd=阿克塞县+酒泉市+肃州区+敦煌市+调任+副县长+任职"},
    {"id": 13, "name": "张洪亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "", "education": "在职大学/在职研究生，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿克塞县委常委、组织部部长、统战部部长", "current_org": "中共阿克塞县委员会",
     "source": "https://www.aksai.gov.cn"},
    {"id": 14, "name": "塞力泰", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "1978-05", "birthplace": "新疆巴里坤", "education": "省委党校研究生",
     "party_join": "2003-05", "work_start": "2000-12",
     "current_post": "酒泉市侨联党组书记、主席", "current_org": "酒泉市归国华侨联合会",
     "source": "https://aiqicha.baidu.com"},
    {"id": 15, "name": "屈存军", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-10", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拟提名为县(市、区)政协副主席候选人", "current_org": "",
     "source": "https://www.baidu.com/s?wd=阿克塞+敦煌+玉门+瓜州+干部+调任"},
    {"id": 16, "name": "冯辉昌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿克塞县人大常委会党组书记、主任", "current_org": "阿克塞县人大常委会",
     "source": "https://www.aksai.gov.cn"},
]

organizations = [
    # ── Aksai County orgs ──
    {"id": 1, "name": "中共阿克塞县委员会", "type": "党委", "level": "县级",
     "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市阿克塞县"},
    {"id": 2, "name": "阿克塞县人民政府", "type": "政府", "level": "县级",
     "parent": "酒泉市人民政府", "location": "甘肃省酒泉市阿克塞县"},
    {"id": 3, "name": "阿克塞县人大常委会", "type": "人大", "level": "县级",
     "parent": "酒泉市人大常委会", "location": "甘肃省酒泉市阿克塞县"},
    {"id": 4, "name": "阿克塞县公安局", "type": "政府", "level": "县级",
     "parent": "阿克塞县人民政府", "location": "甘肃省酒泉市阿克塞县"},
    {"id": 5, "name": "阿克塞县住建局", "type": "政府", "level": "县级",
     "parent": "阿克塞县人民政府", "location": "甘肃省酒泉市阿克塞县"},

    # ── Jiuquan City orgs ──
    {"id": 6, "name": "中共酒泉市纪律检查委员会", "type": "党委", "level": "市级",
     "parent": "中共甘肃省纪律检查委员会", "location": "甘肃省酒泉市"},
    {"id": 7, "name": "酒泉市人民政府", "type": "政府", "level": "市级",
     "parent": "甘肃省人民政府", "location": "甘肃省酒泉市"},
    {"id": 8, "name": "酒泉市政协", "type": "政协", "level": "市级",
     "parent": "甘肃省政协", "location": "甘肃省酒泉市"},
    {"id": 9, "name": "中共酒泉市委组织部", "type": "党委", "level": "市级",
     "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市"},
    {"id": 10, "name": "中共酒泉市委政法委员会", "type": "党委", "level": "市级",
     "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市"},
    {"id": 11, "name": "酒泉市生态环境局", "type": "政府", "level": "市级",
     "parent": "酒泉市人民政府", "location": "甘肃省酒泉市"},
    {"id": 12, "name": "酒泉市归国华侨联合会", "type": "群团", "level": "市级",
     "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市"},

    # ── Suzhou District ──
    {"id": 13, "name": "中共酒泉市肃州区委员会", "type": "党委", "level": "区级",
     "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市肃州区"},
    {"id": 14, "name": "肃州区人民政府", "type": "政府", "level": "区级",
     "parent": "酒泉市人民政府", "location": "甘肃省酒泉市肃州区"},
    {"id": 15, "name": "中共肃州区委统战部", "type": "党委", "level": "区级",
     "parent": "中共肃州区委员会", "location": "甘肃省酒泉市肃州区"},

    # ── Subei County ──
    {"id": 16, "name": "中共肃北蒙古族自治县委员会", "type": "党委", "level": "县级",
     "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市肃北县"},

    # ── Dunhuang ──
    {"id": 17, "name": "敦煌市人民政府", "type": "政府", "level": "县级",
     "parent": "酒泉市人民政府", "location": "甘肃省酒泉市敦煌市"},

    # ── Yumen ──
    {"id": 18, "name": "玉门市人民政府", "type": "政府", "level": "县级",
     "parent": "酒泉市人民政府", "location": "甘肃省酒泉市玉门市"},
]

# Position data: person → org with time ranges
positions = [
    # ── 陶涛 (3) ──
    {"id": 1, "person_id": 3, "org_id": 6, "title": "酒泉市纪委副书记、市监察局副局长",
     "start": "", "end": "2018-03", "rank": "副处级", "note": ""},
    {"id": 2, "person_id": 3, "org_id": 1, "title": "阿克塞县委书记",
     "start": "2021", "end": "2025", "rank": "正处级",
     "note": "调任阿克塞县委书记，后晋升一级调研员"},
    {"id": 3, "person_id": 3, "org_id": 7, "title": "酒泉市人民政府党组成员、副市长",
     "start": "2025", "end": "", "rank": "副厅级",
     "note": "从阿克塞县委书记升任酒泉市副市长"},

    # ── 张金荣 (4) ──
    {"id": 4, "person_id": 4, "org_id": 9, "title": "酒泉市委组织部副部长",
     "start": "2011-04", "end": "2014-08", "rank": "副处级",
     "note": "兼市委党建工作领导小组办公室主任"},
    {"id": 5, "person_id": 4, "org_id": 9, "title": "酒泉市委组织部常务副部长",
     "start": "2014-08", "end": "2016-08", "rank": "正处级", "note": ""},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "阿克塞县委书记",
     "start": "2016-08", "end": "2020-12", "rank": "正处级",
     "note": "任期内晋升一级调研员、二级巡视员"},
    {"id": 7, "person_id": 4, "org_id": 8, "title": "酒泉市政协副主席候选人→副主席",
     "start": "2020-12", "end": "2025", "rank": "副厅级",
     "note": "保留阿克塞县委书记至2021"},
    {"id": 8, "person_id": 4, "org_id": 8, "title": "酒泉市政协党组副书记、一级巡视员",
     "start": "2025", "end": "", "rank": "正厅级巡视员", "note": ""},

    # ── 张桐 (1) ──
    {"id": 9, "person_id": 1, "org_id": 11, "title": "酒泉市生态环境局党组书记、局长，市核安全局局长（兼）",
     "start": "", "end": "2026-01", "rank": "正处级", "note": ""},
    {"id": 10, "person_id": 1, "org_id": 1, "title": "阿克塞县委书记、县人武部党委第一书记",
     "start": "2026-01", "end": "", "rank": "正处级",
     "note": "2026年1月任现职"},

    # ── 库美斯剑 (2) ──
    {"id": 11, "person_id": 2, "org_id": 2, "title": "阿克塞县委副书记、县长",
     "start": "", "end": "", "rank": "正处级",
     "note": "女性，哈萨克族，长期在阿克塞工作"},

    # ── 银雁 (5) ──
    {"id": 12, "person_id": 5, "org_id": 2, "title": "阿克塞县教育局/民族小学/民族中学教师",
     "start": "1985", "end": "1995", "rank": "科员级", "note": "1985年分配至阿克塞"},
    {"id": 13, "person_id": 5, "org_id": 2, "title": "阿克塞县物价委/计划经贸局/县委组织部副部长",
     "start": "1995", "end": "2001", "rank": "副科级→正科级", "note": ""},
    {"id": 14, "person_id": 5, "org_id": 2, "title": "阿克塞县财政局局长",
     "start": "2001", "end": "", "rank": "正科级", "note": ""},
    {"id": 15, "person_id": 5, "org_id": 1, "title": "阿克塞县委常委、政法委书记",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 16, "person_id": 5, "org_id": 2, "title": "阿克塞县委常委、副县长",
     "start": "", "end": "2011-10", "rank": "副处级", "note": ""},
    {"id": 17, "person_id": 5, "org_id": 2, "title": "阿克塞县委副书记、县长",
     "start": "2011-10", "end": "~2016", "rank": "正处级",
     "note": "2025年8月被查"},

    # ── 张鹏 (6) ──
    {"id": 18, "person_id": 6, "org_id": 10, "title": "酒泉市委政法委科员/副科长/科长",
     "start": "2005", "end": "2017-12", "rank": "正科级",
     "note": "2005年省委组织部选调生"},
    {"id": 19, "person_id": 6, "org_id": 10, "title": "酒泉市委防范和处理邪教问题领导小组办公室副主任",
     "start": "2017-12", "end": "2019", "rank": "副处级", "note": ""},
    {"id": 20, "person_id": 6, "org_id": 13, "title": "肃州区（任职）",
     "start": "2019", "end": "2024-04", "rank": "副处级", "note": "在肃州区工作"},
    {"id": 21, "person_id": 6, "org_id": 1, "title": "阿克塞县委常委、常务副县长人选",
     "start": "2024-04", "end": "", "rank": "副处级",
     "note": "从肃州区调任阿克塞"},

    # ── 张健 (7) ──
    {"id": 22, "person_id": 7, "org_id": 13, "title": "肃州区委组织部副部长",
     "start": "", "end": "", "rank": "正科级", "note": "长期在肃州区工作"},
    {"id": 23, "person_id": 7, "org_id": 14, "title": "肃州区上坝镇党委副书记、镇长",
     "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 24, "person_id": 7, "org_id": 14, "title": "肃州区金佛寺镇党委书记",
     "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 25, "person_id": 7, "org_id": 13, "title": "肃州区委办公室主任",
     "start": "", "end": "2023-03", "rank": "正科级", "note": ""},
    {"id": 26, "person_id": 7, "org_id": 2, "title": "阿克塞县副县长",
     "start": "2023-03", "end": "2024-04", "rank": "副处级",
     "note": "从肃州区调任阿克塞"},
    {"id": 27, "person_id": 7, "org_id": 1, "title": "阿克塞县委常委、宣传部部长",
     "start": "2024-04", "end": "", "rank": "副处级", "note": ""},

    # ── 毛学文 (8) ──
    {"id": 28, "person_id": 8, "org_id": 1, "title": "阿克塞县委常委、常务副县长、二级调研员",
     "start": "", "end": "2024-04", "rank": "副处级",
     "note": ""},
    {"id": 29, "person_id": 8, "org_id": 1, "title": "拟任县(市、区)党委副书记",
     "start": "2024-04", "end": "", "rank": "副处级",
     "note": "2024年4月酒泉市委组织部公示"},

    # ── 白振林 (9) ──
    {"id": 30, "person_id": 9, "org_id": 1, "title": "阿克塞县委副书记、三级调研员",
     "start": "", "end": "2024-04", "rank": "副处级", "note": ""},
    {"id": 31, "person_id": 9, "org_id": 7, "title": "拟任市属国有企业正职",
     "start": "2024-04", "end": "", "rank": "正处级",
     "note": "2024年4月酒泉市委组织部公示"},

    # ── 武海龙 (10) ──
    {"id": 32, "person_id": 10, "org_id": 2, "title": "阿克塞县政府副县长、县公安局局长人选→局长",
     "start": "2024-01", "end": "", "rank": "副处级",
     "note": "2024年1月任命"},

    # ── 钟兴鹏 (11) ──
    {"id": 33, "person_id": 11, "org_id": 5, "title": "阿克塞县住建局党组书记、局长",
     "start": "", "end": "2024-04", "rank": "正科级", "note": ""},
    {"id": 34, "person_id": 11, "org_id": 2, "title": "拟提名为县(市、区)政府副县(市、区)长人选",
     "start": "2024-04", "end": "", "rank": "副处级",
     "note": "1988年生，年轻干部"},

    # ── 李珊珊 (12) ──
    {"id": 35, "person_id": 12, "org_id": 2, "title": "阿克塞县政府副县长",
     "start": "", "end": "2026-04", "rank": "副处级", "note": "无党派"},
    {"id": 36, "person_id": 12, "org_id": 7, "title": "拟提名为市级群团组织正职候选人",
     "start": "2026-04", "end": "", "rank": "正处级",
     "note": "2026年4月公示"},

    # ── 张洪亮 (13) ──
    {"id": 37, "person_id": 13, "org_id": 1, "title": "阿克塞县委常委、组织部部长、统战部部长",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 塞力泰 (14) ──
    {"id": 38, "person_id": 14, "org_id": 15, "title": "肃州区委常委、统战部部长、三级调研员",
     "start": "", "end": "2026-03", "rank": "副处级", "note": ""},
    {"id": 39, "person_id": 14, "org_id": 12, "title": "酒泉市侨联党组书记、主席",
     "start": "2026-03", "end": "", "rank": "正处级",
     "note": "哈萨克族，阿克塞相邻县区民族干部"},

    # ── 屈存军 (15) ──
    {"id": 40, "person_id": 15, "org_id": 1, "title": "阿克塞县委办公室主任、县工信局党组书记、四级调研员",
     "start": "", "end": "2024-09", "rank": "正科级", "note": ""},
    {"id": 41, "person_id": 15, "org_id": 2, "title": "拟提名为县(市、区)政协副主席候选人",
     "start": "2024-09", "end": "", "rank": "副处级", "note": ""},

    # ── 冯辉昌 (16) ──
    {"id": 42, "person_id": 16, "org_id": 3, "title": "阿克塞县人大常委会党组书记、主任",
     "start": "", "end": "", "rank": "正处级", "note": ""},
]

# Relationships: person↔person
relationships = [
    # ── Succession relationships ──
    {"id": 1, "person_a": 1, "person_b": 3, "type": "职务接替",
     "context": "张桐接替陶涛出任阿克塞县委书记",
     "overlap_org": "中共阿克塞县委员会",
     "overlap_period": "2026-01（前后任）"},
    {"id": 2, "person_a": 3, "person_b": 4, "type": "职务接替",
     "context": "陶涛接替张金荣出任阿克塞县委书记",
     "overlap_org": "中共阿克塞县委员会",
     "overlap_period": "2021（前后任）"},

    # ── Jiuquan City → Aksai channel ──
    {"id": 3, "person_a": 3, "person_b": 4, "type": "酒泉市委组织部→阿克塞通道",
     "context": "张金荣（酒泉市委组织部常务副部长→阿克塞县委书记）和陶涛（酒泉市纪委副书记→阿克塞县委书记）均从酒泉市直机关调任阿克塞县委书记",
     "overlap_org": "酒泉市直机关→阿克塞",
     "overlap_period": "2016-2025"},
    {"id": 4, "person_a": 1, "person_b": 4, "type": "酒泉市直→阿克塞通道",
     "context": "张桐（酒泉市生态环境局局长→阿克塞县委书记）延续了从酒泉市直机关调任阿克塞县委书记的模式",
     "overlap_org": "酒泉市生态环境局→阿克塞",
     "overlap_period": "2026"},

    # ── Suzhou District → Aksai channel ──
    {"id": 5, "person_a": 6, "person_b": 7, "type": "肃州区→阿克塞通道",
     "context": "张鹏（肃州区任职→阿克塞县委常委）和张健（肃州区长年工作→阿克塞县委常委）均从肃州区调任阿克塞",
     "overlap_org": "肃州区→阿克塞县",
     "overlap_period": "2023-2024"},
    {"id": 6, "person_a": 7, "person_b": 6, "type": "肃州同事的可能",
     "context": "张健在肃州区任区委办公室主任时，张鹏也在肃州区任职，二人可能在肃州区有工作交集",
     "overlap_org": "肃州区",
     "overlap_period": "2019-2023"},

    # ── Aksai → promoted out ──
    {"id": 7, "person_a": 8, "person_b": 9, "type": "阿克塞→其他县区/市企",
     "context": "毛学文（阿克塞常务副县长→拟任县党委副书记）和白振林（阿克塞县委副书记→拟任市属国企正职）同时期公示从阿克塞调出",
     "overlap_org": "阿克塞县",
     "overlap_period": "2024-04"},
    {"id": 8, "person_a": 8, "person_b": 3, "type": "阿克塞同事",
     "context": "毛学文任阿克塞常务副县长时，陶涛任县委书记，二人是党政搭档",
     "overlap_org": "阿克塞县",
     "overlap_period": "~2021-2024"},
    {"id": 9, "person_a": 9, "person_b": 3, "type": "阿克塞同事",
     "context": "白振林任阿克塞县委副书记时，陶涛任县委书记，为直接下属",
     "overlap_org": "阿克塞县",
     "overlap_period": "~2021-2024"},

    # ── Kazakh ethnic network ──
    {"id": 10, "person_a": 2, "person_b": 5, "type": "哈萨克族干部",
     "context": "库美斯剑（哈萨克族女县长）和银雁（哈萨克族前县长）均为阿克塞县长，属哈萨克族干部",
     "overlap_org": "阿克塞县人民政府",
     "overlap_period": "2010s-2020s"},
    {"id": 11, "person_a": 2, "person_b": 14, "type": "哈萨克族网络",
     "context": "库美斯剑（阿克塞县长）和塞力泰（肃州区委统战部长→酒泉侨联主席）均为哈萨克族干部担任酒泉市辖县区重要职务",
     "overlap_org": "酒泉市",
     "overlap_period": "2020s"},
    {"id": 12, "person_a": 5, "person_b": 14, "type": "哈萨克族+巴里坤同乡",
     "context": "银雁（新疆巴里坤人，哈萨克族）和塞力泰（新疆巴里坤人，哈萨克族）同为从新疆到甘肃的哈萨克族干部",
     "overlap_org": "新疆巴里坤→酒泉",
     "overlap_period": "同乡关系"},

    # ── Local cadre in Aksai ──
    {"id": 13, "person_a": 2, "person_b": 16, "type": "阿克塞本地搭档",
     "context": "库美斯剑（县长）与冯辉昌（人大常委会主任）为阿克塞县现职正县级搭档",
     "overlap_org": "阿克塞县",
     "overlap_period": "现任"},
    {"id": 14, "person_a": 2, "person_b": 1, "type": "党政搭档",
     "context": "张桐（县委书记）与库美斯剑（县长）为2026年1月起的新任党政搭档",
     "overlap_org": "阿克塞县",
     "overlap_period": "2026-01至今"},

    # ── Cross-county flow patterns ──
    {"id": 15, "person_a": 11, "person_b": 15, "type": "阿克塞内部晋升",
     "context": "钟兴鹏（住建局局长→拟提副县区长）和屈存军（县委办主任→拟提政协副主席）均从阿克塞县中层晋升",
     "overlap_org": "阿克塞县",
     "overlap_period": "2024"},
]

# ── BUILD SQLITE ────────────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
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
);

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    "end" TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);

CREATE INDEX IF NOT EXISTS idx_positions_person ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_positions_org ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
              (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
               pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
              (r["id"], r["person_a"], r["person_b"], r["type"],
               r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
print(f"SQLite DB written: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

conn.close()

# ── BUILD GEXF ─────────────────────────────────────────────────────────────

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    post_str = str(post)
    if "县委书记" in post_str or "区委书记" in post_str:
        return "255,50,50"  # Red for party secretary
    elif "县长" in post_str and ("副书记" not in post_str or "拟" in post_str):
        return "50,100,255"  # Blue for county magistrate
    elif "常务副" in post_str:
        return "50,150,255"  # Light blue for executive deputy
    elif "副县长" in post_str:
        return "100,100,255"  # Lighter blue for deputy
    elif "纪委书记" in post_str or "监委" in post_str:
        return "255,165,0"  # Orange for discipline
    elif "组织部" in post_str:
        return "200,100,200"  # Purple for org dept
    elif "副书记" in post_str:
        return "200,100,50"  # Brown for deputy secretary
    elif "政协" in post_str:
        return "255,150,50"  # Orange for political advisory
    elif "人大" in post_str:
        return "200,200,100"  # Yellow/gold for people's congress
    else:
        return "100,100,100"  # Grey


def org_color(otype):
    m = {"党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
         "乡镇": "255,255,200", "事业单位": "220,220,220", "政协": "255,240,200",
         "人大": "200,255,255", "群团": "255,220,255"}
    return m.get(otype, "200,200,200")


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>甘肃省酒泉市阿克塞县跨县干部交流网络 — 基于公开信息生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
for aid, atitle, atype in [("0", "type", "string"), ("1", "birth", "string"),
                            ("2", "birthplace", "string"), ("3", "current_post", "string"),
                            ("4", "entity_type", "string"), ("5", "level", "string"),
                            ("6", "ethnicity", "string")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="{atype}"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
for aid, atitle, atype in [("0", "type", "string"), ("1", "start", "string"),
                            ("2", "end", "string"), ("3", "context", "string")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="{atype}"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p.get("current_post", ""))
    is_top = ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "")) or \
             ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", ""))
    sz = "20.0" if is_top else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("birthplace",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="4" value="person"/>')
    lines.append(f'          <attvalue for="5" value=""/>')
    lines.append(f'          <attvalue for="6" value="{esc(p.get("ethnicity",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o.get("type", ""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value=""/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("location",""))}"/>')
    lines.append(f'          <attvalue for="3" value=""/>')
    lines.append(f'          <attvalue for="4" value="organization"/>')
    lines.append(f'          <attvalue for="5" value="{esc(o.get("level",""))}"/>')
    lines.append(f'          <attvalue for="6" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0
for pos in positions:
    edge_id += 1
    lines.append(f'      <edge id="{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("start",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos.get("end",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(pos.get("note",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    edge_id += 1
    ov = r.get("overlap_period", "")
    ov_start = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{edge_id}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(ov_start)}"/>')
    lines.append(f'          <attvalue for="2" value=""/>')
    lines.append(f'          <attvalue for="3" value="{esc(r.get("context",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
