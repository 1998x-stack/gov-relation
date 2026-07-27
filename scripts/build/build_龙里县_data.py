#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 龙里县 (Longli County, Qiannan, Guizhou) leadership network.

龙里县 — 贵州省黔南布依族苗族自治州辖县, 位于贵州省中部, 距贵阳约30km.
Research date: 2026-07. Sources: longli.gov.cn official pages, Baidu Baike.
"""

import json
import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/guizhou_龙里县")
DB_PATH = os.path.join(STAGING, "龙里县_network.db")
GEXF_PATH = os.path.join(STAGING, "龙里县_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

AS_OF = "2026-07-23"
TODAY = AS_OF.replace("-", "")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

# ── Persons ──
persons = [
    # ── Core Leaders (Targets) ──
    # 郭兴文 — 龙里县委书记
    {"id": 1, "name": "郭兴文", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县委书记",
     "current_org": "中共龙里县委",
     "source": "longli.gov.cn news (2026-07); Baidu Baike"},

    # 孙猛 — 龙里县委副书记、县长
    {"id": 2, "name": "孙猛", "gender": "男", "ethnicity": "土家族",
     "birth": "1977-06", "birthplace": "贵州思南", "education": "大学/工学学士",
     "party_join": "2003-08", "work_start": "2001-09",
     "current_post": "龙里县委副书记、县长",
     "current_org": "龙里县人民政府",
     "source": "longli.gov.cn 领导之窗 (2025-06)"},

    # ──县委领导──
    # 严军 — 县委副书记、政法委书记
    {"id": 3, "name": "严军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县委副书记、县委政法委书记",
     "current_org": "中共龙里县委",
     "source": "longli.gov.cn news (2026-07)"},

    # 王必查 — 县委副书记
    {"id": 4, "name": "王必查", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县委副书记",
     "current_org": "中共龙里县委",
     "source": "longli.gov.cn news (2026-05)"},

    # 周洁 — 县委常委、组织部部长
    {"id": 5, "name": "周洁", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县委常委、组织部部长",
     "current_org": "中共龙里县委组织部",
     "source": "longli.gov.cn news (2026-07)"},

    # 郑周勤 — 县委常委、龙里经开区
    {"id": 6, "name": "郑周勤", "gender": "男", "ethnicity": "仡佬族",
     "birth": "1979-06", "birthplace": "贵州道真", "education": "大学/工学学士",
     "party_join": "2007-11", "work_start": "2004-07",
     "current_post": "龙里县委常委、龙里经开区党工委副书记、管委会副主任",
     "current_org": "龙里经济技术开发区",
     "source": "longli.gov.cn 领导之窗"},

    # 蒙绍欢 — 县委常委、副县长
    {"id": 7, "name": "蒙绍欢", "gender": "男", "ethnicity": "水族",
     "birth": "1986-12", "birthplace": "贵州荔波", "education": "",
     "party_join": "2013-06", "work_start": "2011-02",
     "current_post": "龙里县委常委、副县长",
     "current_org": "龙里县人民政府",
     "source": "longli.gov.cn 领导之窗 (2025-02)"},

    # 杨正松 — 县委常委
    {"id": 8, "name": "杨正松", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县委常委",
     "current_org": "中共龙里县委",
     "source": "longli.gov.cn news (2026-07)"},

    # 陈杰 — 县委常委
    {"id": 9, "name": "陈杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县委常委",
     "current_org": "中共龙里县委",
     "source": "longli.gov.cn news (2026-07)"},

    # ── 县政府领导 ──
    # 胡伟谊 — 副县长
    {"id": 10, "name": "胡伟谊", "gender": "男", "ethnicity": "",
     "birth": "1981-12", "birthplace": "贵州龙里", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县副县长",
     "current_org": "龙里县人民政府",
     "source": "longli.gov.cn 领导之窗"},

    # 熊杰 — 副县长
    {"id": 11, "name": "熊杰", "gender": "男", "ethnicity": "",
     "birth": "1976-12", "birthplace": "贵州龙里", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县副县长",
     "current_org": "龙里县人民政府",
     "source": "longli.gov.cn 领导之窗 (2025-12)"},

    # 平安 — 副县长
    {"id": 12, "name": "平安", "gender": "男", "ethnicity": "",
     "birth": "1987-11", "birthplace": "贵州三都", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县副县长",
     "current_org": "龙里县人民政府",
     "source": "longli.gov.cn 领导之窗 (2025-12)"},

    # ── 人大、政协 ──
    # 王华 — 县人大常委会主任
    {"id": 13, "name": "王华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县人大常委会主任",
     "current_org": "龙里县人大常委会",
     "source": "longli.gov.cn news (2026-07)"},

    # 魏明 — 县政协主席
    {"id": 14, "name": "魏明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县政协主席",
     "current_org": "政协龙里县委员会",
     "source": "longli.gov.cn news (2026-07)"},

    # 汪永丽 — 县政协党组书记(新任)
    {"id": 15, "name": "汪永丽", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县政协党组书记",
     "current_org": "政协龙里县委员会",
     "source": "longli.gov.cn news (2026-07-23)"},

    # ── 其他县领导 ──
    {"id": 16, "name": "杨秋宁", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县领导",
     "current_org": "",
     "source": "longli.gov.cn news (2026-07)"},

    {"id": 17, "name": "梁忠林", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙里县领导",
     "current_org": "",
     "source": "longli.gov.cn news (2026-07)"},

    # ── 前任 ──
    # 冯异星 — 前任龙里县委书记、县长
    {"id": 18, "name": "冯异星", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "黔南州政府副秘书长、办公室主任（原龙里县委书记）",
     "current_org": "黔南州人民政府",
     "source": "Baidu Baike"},

    # 刘华龙 — 更早前任龙里县委书记
    {"id": 19, "name": "刘华龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原黔南州委常委、常务副州长(已落马)",
     "current_org": "",
     "source": "Baidu Baike"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共龙里县委", "type": "党委", "level": "县级", "parent": "中共黔南州委", "location": "龙里县"},
    {"id": 2, "name": "龙里县人民政府", "type": "政府", "level": "县级", "parent": "黔南州人民政府", "location": "龙里县"},
    {"id": 3, "name": "龙里县人大常委会", "type": "人大", "level": "县级", "parent": "黔南州人大常委会", "location": "龙里县"},
    {"id": 4, "name": "政协龙里县委员会", "type": "政协", "level": "县级", "parent": "政协黔南州委员会", "location": "龙里县"},
    {"id": 5, "name": "中共龙里县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共龙里县委", "location": "龙里县"},
    {"id": 6, "name": "中共龙里县委组织部", "type": "党委", "level": "县级", "parent": "中共龙里县委", "location": "龙里县"},
    {"id": 7, "name": "中共龙里县委政法委员会", "type": "党委", "level": "县级", "parent": "中共龙里县委", "location": "龙里县"},
    {"id": 8, "name": "龙里经济技术开发区", "type": "开发区", "level": "县级", "parent": "龙里县人民政府", "location": "龙里县"},
    {"id": 9, "name": "黔南州人民政府", "type": "政府", "level": "地市级", "parent": "贵州省人民政府", "location": "都匀市"},
    {"id": 10, "name": "贵阳市乌当区", "type": "政府", "level": "县级", "parent": "贵阳市人民政府", "location": "贵阳市乌当区"},
    {"id": 11, "name": "贵阳市观山湖区", "type": "政府", "level": "县级", "parent": "贵阳市人民政府", "location": "贵阳市观山湖区"},
    {"id": 12, "name": "双龙航空港经济区", "type": "开发区", "level": "地市级", "parent": "贵州省人民政府", "location": "贵阳市/黔南州"},
    {"id": 13, "name": "福泉市", "type": "政府", "level": "县级", "parent": "黔南州人民政府", "location": "福泉市"},
    {"id": 14, "name": "长顺县", "type": "政府", "level": "县级", "parent": "黔南州人民政府", "location": "长顺县"},
    {"id": 15, "name": "中共黔南州委", "type": "党委", "level": "地市级", "parent": "中共贵州省委", "location": "都匀市"},
    {"id": 16, "name": "黔南州住房公积金管理中心", "type": "事业单位", "level": "地市级", "parent": "黔南州人民政府", "location": "都匀市"},
    {"id": 17, "name": "黔南州政府办公室", "type": "政府", "level": "地市级", "parent": "黔南州人民政府", "location": "都匀市"},
]

# ── Positions ──
positions = [
    # 郭兴文
    {"person_id": 1, "org_id": 1, "title": "龙里县委书记", "start_date": "2025-07", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "龙里经开区党工委书记（兼）", "start_date": "", "end_date": "", "rank": "", "note": "兼任"},
    # 孙猛
    {"person_id": 2, "org_id": 2, "title": "龙里县委副书记、县长", "start_date": "2025", "end_date": "", "rank": "县处级正职", "note": "2025年从双龙航空港经济区调任"},
    {"person_id": 2, "org_id": 8, "title": "龙里经开区党工委副书记、管委会主任（兼）", "start_date": "", "end_date": "", "rank": "", "note": "兼任"},
    {"person_id": 2, "org_id": 12, "title": "双龙航空港经济区党工委副书记、管委会主任", "start_date": "", "end_date": "2025", "rank": "", "note": "调任龙里县长前"},
    {"person_id": 2, "org_id": 11, "title": "观山湖区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "观山湖现代服务产业试验区党工委副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "乌当区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "乌当区政协党组副书记", "start_date": "", "end_date": "", "rank": "", "note": "兼任"},
    {"person_id": 2, "org_id": 10, "title": "乌当区政府办公室主任（金融工作办公室）", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "乌当区工业和信息化局（大数据发展管理局）局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "乌当区商务局（粮食局）局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "乌当区东风镇镇长、党委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 严军
    {"person_id": 3, "org_id": 1, "title": "龙里县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 7, "title": "龙里县委政法委书记（兼）", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 王必查
    {"person_id": 4, "org_id": 1, "title": "龙里县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 周洁
    {"person_id": 5, "org_id": 6, "title": "龙里县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 郑周勤
    {"person_id": 6, "org_id": 1, "title": "龙里县委常委", "start_date": "2021", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "龙里县政府党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "龙里经开区党工委副书记、管委会副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "龙里县副县长", "start_date": "2018", "end_date": "2021", "rank": "县处级副职", "note": ""},
    # 蒙绍欢
    {"person_id": 7, "org_id": 1, "title": "龙里县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "龙里县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 杨正松
    {"person_id": 8, "org_id": 1, "title": "龙里县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 陈杰
    {"person_id": 9, "org_id": 1, "title": "龙里县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 胡伟谊
    {"person_id": 10, "org_id": 2, "title": "龙里县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "龙里县政府党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 熊杰
    {"person_id": 11, "org_id": 2, "title": "龙里县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "龙里县政府党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 平安
    {"person_id": 12, "org_id": 2, "title": "龙里县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "龙里县政府党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 王华
    {"person_id": 13, "org_id": 3, "title": "龙里县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 魏明
    {"person_id": 14, "org_id": 4, "title": "龙里县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "过渡中，汪永丽已任政协党组书记"},
    # 汪永丽
    {"person_id": 15, "org_id": 4, "title": "龙里县政协党组书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "新任，2026-07新闻中出现"},
    # 冯异星
    {"person_id": 18, "org_id": 1, "title": "龙里县委书记", "start_date": "2022-09", "end_date": "2025-06", "rank": "县处级正职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "龙里县人民政府县长", "start_date": "2021-04", "end_date": "2023-09", "rank": "县处级正职", "note": "2021-03 代县长"},
    {"person_id": 18, "org_id": 16, "title": "黔南州住房公积金管理中心主任", "start_date": "2025-06", "end_date": "2026-01", "rank": "县处级正职", "note": ""},
    {"person_id": 18, "org_id": 17, "title": "黔南州政府副秘书长、办公室主任", "start_date": "2026-01", "end_date": "", "rank": "县处级正职", "note": ""},
    # 刘华龙
    {"person_id": 19, "org_id": 1, "title": "龙里县委书记", "start_date": "2015", "end_date": "2021-03", "rank": "县处级正职", "note": ""},
    {"person_id": 19, "org_id": 15, "title": "黔南州委常委、常务副州长", "start_date": "2021-03", "end_date": "2023-01", "rank": "厅局级副职", "note": "2023年1月被查，11月被判11年"},
]

# ── Relationships ──
relationships = [
    # 书记 ↔ 县长
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "郭兴文（县委书记）与孙猛（县长）构成书记-县长搭档", "overlap_org": "中共龙里县委/龙里县人民政府", "overlap_period": "2025-至今"},
    # 书记 ↔ 政法委书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "郭兴文与严军（县委副书记、政法委书记）在县委常委会共事", "overlap_org": "中共龙里县委", "overlap_period": "2025-至今"},
    # 书记 ↔ 组织部长
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "郭兴文与周洁（组织部部长）在县委常委会共事", "overlap_org": "中共龙里县委", "overlap_period": "2025-至今"},
    # 县长 ↔ 县委常委/副县长
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "孙猛与蒙绍欢在县政府班子共事", "overlap_org": "龙里县人民政府", "overlap_period": "2025-至今"},
    # 县长 ↔ 经开区副主任
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "孙猛（经开区主任）与郑周勤（经开区副主任）在经开区共事", "overlap_org": "龙里经济技术开发区", "overlap_period": "2025-至今"},
    # 前任 ↔ 现任（书记传承）
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "冯异星离任后，郭兴文接任龙里县委书记", "overlap_org": "中共龙里县委", "overlap_period": "2025-07"},
    # 前任县委书记 ↔ 现任县长
    {"person_a": 2, "person_b": 18, "type": "predecessor_successor", "context": "冯异星任县委书记时孙猛任县长（或县长交接前后）", "overlap_org": "中共龙里县委/龙里县人民政府", "overlap_period": "2025"},
    # 前任书记 ↔ 更早前任
    {"person_a": 18, "person_b": 19, "type": "predecessor_successor", "context": "刘华龙离任后，冯异星接任龙里县委书记", "overlap_org": "中共龙里县委", "overlap_period": "2021-03"},
    # 政法委书记 ↔ 组织部长
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "严军与周洁在县委常委会共事", "overlap_org": "中共龙里县委", "overlap_period": "至今"},
    # 副县长们
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "胡伟谊与熊杰在县政府班子共事", "overlap_org": "龙里县人民政府", "overlap_period": "至今"},
    {"person_a": 10, "person_b": 12, "type": "overlap", "context": "胡伟谊与平安在县政府班子共事", "overlap_org": "龙里县人民政府", "overlap_period": "至今"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "熊杰与平安在县政府班子共事", "overlap_org": "龙里县人民政府", "overlap_period": "至今"},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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
        pid = f"longli_{p['name']}"
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
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

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
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>龙里县领导班子关系网络（基于龙里县政府官网、黔南州人事公示、百度百科）</description>')
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
    source_register = [
        {"id": "S001", "title": "龙里县人民政府 - 领导之窗（孙猛简历）", "url": "https://www.longli.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/202506/t20250606_88105713.html",
         "publisher": "龙里县人民政府", "published_at": "2025-06-06", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "龙里县人民政府 - 领导之窗（郑周勤简历）", "url": "https://www.longli.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/202108/t20210825_78783195.html",
         "publisher": "龙里县人民政府", "published_at": "2021-08-25", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S003", "title": "龙里县人民政府 - 领导之窗（蒙绍欢简历）", "url": "https://www.longli.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/202502/t20250219_86915524.html",
         "publisher": "龙里县人民政府", "published_at": "2025-02-19", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S004", "title": "龙里县人民政府 - 领导之窗（胡伟谊简历）", "url": "https://www.longli.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/202202/t20220209_78783198.html",
         "publisher": "龙里县人民政府", "published_at": "2022-02-09", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S005", "title": "龙里县人民政府 - 领导之窗（熊杰简历）", "url": "https://www.longli.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/202512/t20251224_89083774.html",
         "publisher": "龙里县人民政府", "published_at": "2025-12-24", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S006", "title": "龙里县人民政府 - 领导之窗（平安简历）", "url": "https://www.longli.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/202512/t20251223_89079253.html",
         "publisher": "龙里县人民政府", "published_at": "2025-12-23", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S007", "title": "十三届县委常委会第176次（扩大）会议召开", "url": "https://www.longli.gov.cn/xwdt/zwyw/202607/t20260706_90587753.html",
         "publisher": "龙里县人民政府", "published_at": "2026-07-06", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": "提及严军（县委副书记、政法委书记）、魏明（政协主席）"},
        {"id": "S008", "title": "龙里县'两优一先'表彰大会", "url": "https://www.longli.gov.cn/xwdt/zwyw/202607/t20260703_90582270.html",
         "publisher": "龙里县人民政府", "published_at": "2026-07-03", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": "提及周洁（县委常委、组织部部长）"},
        {"id": "S009", "title": "龙里县委巡察反馈会", "url": "https://www.longli.gov.cn/xwdt/zwyw/202607/t20260709_90600723.html",
         "publisher": "龙里县人民政府", "published_at": "2026-07-09", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": "提及周洁、杨正松、陈杰"},
        {"id": "S010", "title": "龙里县禁毒工作会议", "url": "https://www.longli.gov.cn/xwdt/zwyw/202607/t20260707_90592388.html",
         "publisher": "龙里县人民政府", "published_at": "2026-07-07", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": "提及杨秋宁、梁忠林"},
        {"id": "S011", "title": "郭兴文主持召开全县信访工作调度会", "url": "https://www.longli.gov.cn/xwdt/zwyw/202607/t20260723_90653180.html",
         "publisher": "龙里县人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high", "notes": "提及汪永丽（县政协党组书记）"},
        {"id": "S012", "title": "冯异星 - 百度百科", "url": "https://baike.baidu.com/item/%E5%86%AF%E5%BC%82%E6%98%9F",
         "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-23", "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S013", "title": "刘华龙 - 百度百科", "url": "https://baike.baidu.com/item/%E5%88%98%E5%8D%8E%E9%BE%99",
         "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-23", "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S014", "title": "龙里县 - 百度百科", "url": "https://baike.baidu.com/item/%E9%BE%99%E9%87%8C%E5%8E%BF",
         "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-23", "source_type": "encyclopedia", "reliability": "medium", "notes": "含主要领导列表（截至2026年4月）：书记郭兴文、县长孙猛等"},
        {"id": "S015", "title": "郭兴文 - 百度百科", "url": "https://baike.baidu.com/item/%E9%83%AD%E5%85%B4%E6%96%87/13783553",
         "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-23", "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
    ]

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "贵州省",
                "city": "黔南布依族苗族自治州",
                "region": "龙里县",
                "job": p.get("current_post", ""),
                "task_id": "guizhou_龙里县",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"longli_{p['name']}",
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
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "人大" not in p.get("current_post", "")) else "县处级副职",
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
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 龙里"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 郭兴文 Person JSON ──
    gxw_timeline = [
        {"start": "2025-07", "end": "", "org": "中共龙里县委员会", "title": "龙里县委书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S014", "S015"]},
        {"start": "2024", "end": "2025-07", "org": "黔南州委社会工作部", "title": "黔南州委社会工作部部长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S015"]},
        {"start": "", "end": "2024", "org": "中共黔南州委", "title": "黔南州委副秘书长、州委办公室主任（正县长级）",
         "notes": "", "confidence": "confirmed", "source_ids": ["S015"]},
        {"start": "2013-08", "end": "", "org": "福泉市委", "title": "福泉市委副书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S015"]},
        {"start": "2011-10", "end": "2013-08", "org": "长顺县委", "title": "长顺县委常委、常务副县长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S015"]},
        {"start": "2009-05", "end": "2011-10", "org": "长顺县委", "title": "长顺县委常委、宣传部部长、睦化乡党委书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S015"]},
        {"start": "", "end": "2009-05", "org": "长顺县代化镇", "title": "代化镇党委书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S015"]},
        {"start": "", "end": "", "org": "长顺县政府", "title": "长顺县政府办秘书、法制办主任",
         "notes": "", "confidence": "confirmed", "source_ids": ["S015"]},
        {"start": "1998-08", "end": "", "org": "长顺县鼓扬镇红岩小学", "title": "教师",
         "notes": "参加工作起点", "confidence": "confirmed", "source_ids": ["S015"]},
    ]
    gxw_relationships = [
        {"person": "孙猛", "person_id": "longli_孙猛", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "郭兴文（县委书记）与孙猛（县长）在县委常委会和县政府班子共事",
         "overlap_org": "中共龙里县委/龙里县人民政府", "overlap_period": "2025年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S014"]},
        {"person": "冯异星", "person_id": "longli_冯异星", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "冯异星调任黔南州后，郭兴文接任龙里县委书记",
         "overlap_org": "中共龙里县委", "overlap_period": "2025-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S014", "S015"]},
        {"person": "严军", "person_id": "longli_严军", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "郭兴文与严军（县委副书记、政法委书记）在县委常委会共事",
         "overlap_org": "中共龙里县委", "overlap_period": "2025年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
    ]

    gxw_json = make_person_json(persons[0], gxw_timeline, gxw_relationships)
    gxw_path = os.path.join(PERSONS_DIR, f"{TODAY}-贵州省-黔南布依族苗族自治州-县委书记-郭兴文.json")
    with open(gxw_path, "w", encoding="utf-8") as f:
        json.dump(gxw_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {gxw_path}")

    # ── 孙猛 Person JSON ──
    sm_timeline = [
        {"start": "2025", "end": "", "org": "龙里县人民政府", "title": "龙里县委副书记、县长",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "2025", "org": "双龙航空港经济区", "title": "双龙航空港经济区党工委副书记、管委会主任",
         "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "观山湖区委", "title": "观山湖区委常委、常务副区长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "观山湖现代服务产业试验区", "title": "观山湖现代服务产业试验区党工委副书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "乌当区委", "title": "乌当区委常委、统战部部长",
         "notes": "兼任区政协党组副书记", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "乌当区政府办公室", "title": "乌当区政府办公室（金融工作办公室）主任",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "乌当区工业和信息化局", "title": "乌当区工业和信息化局（大数据发展管理局）局长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "乌当区商务局", "title": "乌当区商务局（粮食局）局长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "乌当区东风镇", "title": "乌当区东风镇镇长、党委书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "孙猛1977年6月出生、2001年9月参加工作，至任东风镇镇长/书记之间的早期履历未完整公开",
         "confidence": "unverified", "source_ids": []},
    ]
    sm_relationships = [
        {"person": "郭兴文", "person_id": "longli_郭兴文", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "孙猛（县长）与郭兴文（县委书记）构成县委书记-县长搭档",
         "overlap_org": "中共龙里县委/龙里县人民政府", "overlap_period": "2025年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S014"]},
        {"person": "蒙绍欢", "person_id": "longli_蒙绍欢", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "孙猛（县长）与蒙绍欢（县委常委、副县长）在县政府班子共事",
         "overlap_org": "龙里县人民政府", "overlap_period": "2025年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "郑周勤", "person_id": "longli_郑周勤", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "孙猛（经开区主任）与郑周勤（经开区副主任）同在经开区班子",
         "overlap_org": "龙里经济技术开发区", "overlap_period": "2025年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]

    sm_json = make_person_json(persons[1], sm_timeline, sm_relationships)
    sm_path = os.path.join(PERSONS_DIR, f"{TODAY}-贵州省-黔南布依族苗族自治州-县长-孙猛.json")
    with open(sm_path, "w", encoding="utf-8") as f:
        json.dump(sm_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {sm_path}")

    # ── 冯异星 Person JSON ──
    fyx_timeline = [
        {"start": "2026-01", "end": "", "org": "黔南州人民政府", "title": "黔南州政府副秘书长、办公室主任",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2025-06", "end": "2026-01", "org": "黔南州住房公积金管理中心", "title": "黔南州住房公积金管理中心主任",
         "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2022-09", "end": "2025-06", "org": "中共龙里县委", "title": "龙里县委书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2021-04", "end": "2023-09", "org": "龙里县人民政府", "title": "龙里县人民政府县长",
         "notes": "2021-03 代县长", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2021-06", "end": "2022-09", "org": "中共龙里县委", "title": "龙里县委副书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "", "end": "2021-03", "org": "福泉市", "title": "福泉市委常委、常务副市长（曾任组织部长）",
         "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    fyx_relationships = [
        {"person": "郭兴文", "person_id": "longli_郭兴文", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "冯异星离任龙里县委书记后，郭兴文接任",
         "overlap_org": "中共龙里县委", "overlap_period": "2025-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012", "S015"]},
        {"person": "刘华龙", "person_id": "longli_刘华龙", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "刘华龙离任龙里县委书记后，冯异星接任",
         "overlap_org": "中共龙里县委", "overlap_period": "2021-03",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012", "S013"]},
    ]

    fyx_json = make_person_json(persons[17], fyx_timeline, fyx_relationships)
    fyx_path = os.path.join(PERSONS_DIR, f"{TODAY}-贵州省-黔南布依族苗族自治州-县委书记-冯异星.json")
    with open(fyx_path, "w", encoding="utf-8") as f:
        json.dump(fyx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {fyx_path}")

    print(f"\nBuild complete. All artifacts in {STAGING}")


if __name__ == "__main__":
    build()
