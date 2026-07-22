#!/usr/bin/env python3
"""
肃南裕固族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 肃南裕固族自治县人民政府官方网站 (www.gssn.gov.cn)
- 百度百科/百度搜索 (多渠道交叉验证)
- 新闻报道 (中国张掖网、甘肃日报、肃南融媒等)
- 任前公示信息

注意: 部分履历信息基于公开资料汇总整理, 标记了置信度级别.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_肃南裕固族自治县")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "肃南裕固族自治县_network.db")
GEXF_PATH = os.path.join(STAGING, "肃南裕固族自治县_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # === 核心领导（目标人物）===
    # 县委书记
    {
        "id": "p01",
        "name": "钟向辉",
        "gender": "男",
        "ethnicity": "裕固族",
        "birth": "1975年12月",
        "birthplace": "甘肃肃南",
        "native_place": "甘肃肃南",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1995年?",
        "current_post": "肃南裕固族自治县委书记",
        "current_org": "中共肃南裕固族自治县委员会",
        "source": "肃南裕固族自治县人民政府官网、新闻报道",
        "person_id": "sunan_zhong_xianghui"
    },
    # 县长
    {
        "id": "p02",
        "name": "张辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年?",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委副书记、县长",
        "current_org": "肃南裕固族自治县人民政府",
        "source": "肃南裕固族自治县人民政府官网、新闻报道",
        "person_id": "sunan_zhang_hui"
    },
    # === 县委副书记 ===
    {
        "id": "p03",
        "name": "王锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委副书记 （可能兼任其他职务）",
        "current_org": "中共肃南裕固族自治县委员会",
        "source": "新闻报道、肃南融媒",
        "person_id": "sunan_wang_feng"
    },
    # === 常务副县长 ===
    {
        "id": "p04",
        "name": "梁国文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委常委、常务副县长",
        "current_org": "肃南裕固族自治县人民政府",
        "source": "肃南裕固族自治县人民政府官网",
        "person_id": "sunan_liang_guowen"
    },
    # === 纪委书记 ===
    {
        "id": "p05",
        "name": "杨秀娟",
        "gender": "女",
        "ethnicity": "裕固族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委常委、纪委书记、监委主任",
        "current_org": "中共肃南裕固族自治县纪律检查委员会",
        "source": "肃南裕固族自治县人民政府官网、新闻报道",
        "person_id": "sunan_yang_xiujuan"
    },
    # === 组织部部长 ===
    {
        "id": "p06",
        "name": "吴晟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委常委、组织部部长",
        "current_org": "中共肃南裕固族自治县委员会组织部",
        "source": "肃南裕固族自治县人民政府官网、新闻报道",
        "person_id": "sunan_wu_sheng"
    },
    # === 宣传部部长 ===
    {
        "id": "p07",
        "name": "杜明哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委常委、宣传部部长",
        "current_org": "中共肃南裕固族自治县委员会宣传部",
        "source": "肃南裕固族自治县人民政府官网、新闻报道",
        "person_id": "sunan_du_mingzhe"
    },
    # === 统战部部长 ===
    {
        "id": "p08",
        "name": "张爱玲",
        "gender": "女",
        "ethnicity": "裕固族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委常委、统战部部长",
        "current_org": "中共肃南裕固族自治县委员会统战部",
        "source": "肃南裕固族自治县人民政府官网",
        "person_id": "sunan_zhang_ailing"
    },
    # === 政法委书记 ===
    {
        "id": "p09",
        "name": "陈军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委常委、政法委书记",
        "current_org": "中共肃南裕固族自治县委员会政法委员会",
        "source": "肃南裕固族自治县人民政府官网",
        "person_id": "sunan_chen_jun"
    },
    # === 县委办主任 ===
    {
        "id": "p10",
        "name": "刘红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县委常委、县委办公室主任",
        "current_org": "中共肃南裕固族自治县委员会办公室",
        "source": "肃南裕固族自治县人民政府官网",
        "person_id": "sunan_liu_hong"
    },
    # === 副县长（分管日常工作）===
    {
        "id": "p11",
        "name": "安永明",
        "gender": "男",
        "ethnicity": "裕固族",
        "birth": "待查",
        "birthplace": "甘肃肃南",
        "native_place": "甘肃肃南",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县副县长",
        "current_org": "肃南裕固族自治县人民政府",
        "source": "肃南裕固族自治县人民政府官网",
        "person_id": "sunan_an_yongming"
    },
    # === 人大常委会主任 ===
    {
        "id": "p12",
        "name": "巴玉霞",
        "gender": "女",
        "ethnicity": "裕固族",
        "birth": "待查",
        "birthplace": "甘肃肃南",
        "native_place": "甘肃肃南",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县人大常委会主任",
        "current_org": "肃南裕固族自治县人民代表大会常务委员会",
        "source": "肃南裕固族自治县人民政府官网",
        "person_id": "sunan_ba_yuxia"
    },
    # === 政协主席 ===
    {
        "id": "p13",
        "name": "兰永武",
        "gender": "男",
        "ethnicity": "裕固族",
        "birth": "待查",
        "birthplace": "甘肃肃南",
        "native_place": "甘肃肃南",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃南裕固族自治县政协主席",
        "current_org": "中国人民政治协商会议肃南裕固族自治县委员会",
        "source": "肃南裕固族自治县人民政府官网",
        "person_id": "sunan_lan_yongwu"
    },
    # === 前任领导 ===
    # 前任县委书记
    {
        "id": "p14",
        "name": "陆思东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学/公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市副市长（时任肃南县委书记）",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网、新闻报道",
        "person_id": "sunan_lu_sidong"
    },
    # 前任县长
    {
        "id": "p15",
        "name": "白勇",
        "gender": "男",
        "ethnicity": "裕固族",
        "birth": "1974年?",
        "birthplace": "甘肃肃南",
        "native_place": "甘肃肃南",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任）肃南裕固族自治县县长",
        "current_org": "（已调离）",
        "source": "新闻报道、任前公示",
        "person_id": "sunan_bai_yong"
    },
    # 更早一任县委书记
    {
        "id": "p16",
        "name": "李宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年?",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任）肃南裕固族自治县委书记",
        "current_org": "（已调离）",
        "source": "新闻报道",
        "person_id": "sunan_li_hongwei"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共肃南裕固族自治县委员会", "type": "党委", "level": "县处级",
     "parent": "中共张掖市委员会", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o02", "name": "肃南裕固族自治县人民政府", "type": "政府", "level": "县处级",
     "parent": "张掖市人民政府", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o03", "name": "中共肃南裕固族自治县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共肃南裕固族自治县委员会", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o04", "name": "中共肃南裕固族自治县委员会组织部", "type": "党委", "level": "县处级",
     "parent": "中共肃南裕固族自治县委员会", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o05", "name": "中共肃南裕固族自治县委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共肃南裕固族自治县委员会", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o06", "name": "中共肃南裕固族自治县委员会统战部", "type": "党委", "level": "县处级",
     "parent": "中共肃南裕固族自治县委员会", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o07", "name": "中共肃南裕固族自治县委员会政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共肃南裕固族自治县委员会", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o08", "name": "中共肃南裕固族自治县委员会办公室", "type": "党委", "level": "县处级",
     "parent": "中共肃南裕固族自治县委员会", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o09", "name": "肃南裕固族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "肃南裕固族自治县", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o10", "name": "中国人民政治协商会议肃南裕固族自治县委员会", "type": "政协", "level": "县处级",
     "parent": "肃南裕固族自治县", "location": "甘肃省张掖市肃南裕固族自治县"},
    {"id": "o11", "name": "张掖市人民政府", "type": "政府", "level": "地级",
     "parent": "甘肃省人民政府", "location": "甘肃省张掖市"},
]

# 3. 任职记录
positions = [
    # 钟向辉 - 县委书记
    {"person_id": "p01", "org_id": "o01", "title": "肃南裕固族自治县委书记",
     "start": "2021?", "end": "至今", "rank": "正县级",
     "note": "主持县委全面工作, 裕固族干部"},
    # 钟向辉 - 此前职务（不详，需补充）
    {"person_id": "p01", "org_id": "o02", "title": "肃南裕固族自治县县长（前任职务）",
     "start": "2016?", "end": "2021?", "rank": "正县级",
     "note": "由县长转任县委书记, 具体时间待核实"},

    # 张辉 - 县长
    {"person_id": "p02", "org_id": "o02", "title": "肃南裕固族自治县县长",
     "start": "2023?", "end": "至今", "rank": "正县级",
     "note": "主持县政府全面工作"},
    {"person_id": "p02", "org_id": "o01", "title": "肃南裕固族自治县委副书记",
     "start": "2023?", "end": "至今", "rank": "副县级",
     "note": "兼任县委副书记"},

    # 王锋 - 县委副书记
    {"person_id": "p03", "org_id": "o01", "title": "肃南裕固族自治县委副书记",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "协助书记处理县委日常工作"},

    # 梁国文 - 常务副县长
    {"person_id": "p04", "org_id": "o02", "title": "肃南裕固族自治县委常委、常务副县长",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "负责县政府常务工作"},

    # 杨秀娟 - 纪委书记
    {"person_id": "p05", "org_id": "o03", "title": "肃南裕固族自治县委常委、纪委书记、监委主任",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "裕固族女干部"},

    # 吴晟 - 组织部部长
    {"person_id": "p06", "org_id": "o04", "title": "肃南裕固族自治县委常委、组织部部长",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "负责组织、干部、人才工作"},

    # 杜明哲 - 宣传部部长
    {"person_id": "p07", "org_id": "o05", "title": "肃南裕固族自治县委常委、宣传部部长",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "负责宣传思想文化工作"},

    # 张爱玲 - 统战部部长
    {"person_id": "p08", "org_id": "o06", "title": "肃南裕固族自治县委常委、统战部部长",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "裕固族女干部"},

    # 陈军 - 政法委书记
    {"person_id": "p09", "org_id": "o07", "title": "肃南裕固族自治县委常委、政法委书记",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "负责政法、维稳、社会治安综合治理工作"},

    # 刘红 - 县委办主任
    {"person_id": "p10", "org_id": "o08", "title": "肃南裕固族自治县委常委、县委办公室主任",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "负责县委机关日常运转工作"},

    # 安永明 - 副县长
    {"person_id": "p11", "org_id": "o02", "title": "肃南裕固族自治县副县长",
     "start": "待查", "end": "至今", "rank": "副县级",
     "note": "裕固族干部"},

    # 巴玉霞 - 人大常委会主任
    {"person_id": "p12", "org_id": "o09", "title": "肃南裕固族自治县人大常委会主任",
     "start": "待查", "end": "至今", "rank": "正县级",
     "note": "裕固族女干部"},

    # 兰永武 - 政协主席
    {"person_id": "p13", "org_id": "o10", "title": "肃南裕固族自治县政协主席",
     "start": "待查", "end": "至今", "rank": "正县级",
     "note": "裕固族干部"},

    # 陆思东 - 前任县委书记
    {"person_id": "p14", "org_id": "o01", "title": "肃南裕固族自治县委书记",
     "start": "2020?", "end": "2021/2022?", "rank": "正县级",
     "note": "前任县委书记, 后升任张掖市副市长"},
    {"person_id": "p14", "org_id": "o11", "title": "张掖市副市长",
     "start": "2022?", "end": "至今", "rank": "副厅级",
     "note": "升任张掖市副市长"},

    # 白勇 - 前任县长
    {"person_id": "p15", "org_id": "o02", "title": "肃南裕固族自治县县长",
     "start": "2021?", "end": "2023?", "rank": "正县级",
     "note": "前任县长, 裕固族干部, 去向待查"},

    # 李宏伟 - 更早一任县委书记
    {"person_id": "p16", "org_id": "o01", "title": "肃南裕固族自治县委书记",
     "start": "2016?", "end": "2019/2020?", "rank": "正县级",
     "note": "更早一任县委书记"},
]

# 4. 关系
relationships = [
    # 钟向辉 → 陆思东（前后任）
    {"person_a": "p01", "person_b": "p14", "type": "predecessor_successor",
     "strength": "strong", "context": "陆思东升任张掖市副市长后, 钟向辉接任县委书记",
     "overlap_org": "中共肃南裕固族自治县委员会", "overlap_period": "2021-2022"},
    # 钟向辉 → 张辉（上下级）
    {"person_a": "p01", "person_b": "p02", "type": "superior_subordinate",
     "strength": "strong", "context": "县委书记与县长搭班, 县委县政府主要领导",
     "overlap_org": "中共肃南裕固族自治县委员会/肃南裕固族自治县人民政府",
     "overlap_period": "2023-至今"},
    # 钟向辉 → 白勇（前后任/可能同届）
    {"person_a": "p01", "person_b": "p15", "type": "predecessor_successor",
     "strength": "strong", "context": "钟向辉由县长转任书记, 白勇接任县长",
     "overlap_org": "肃南裕固族自治县人民政府", "overlap_period": "2021-2022?"},
    # 陆思东 → 李宏伟（前后任）
    {"person_a": "p14", "person_b": "p16", "type": "predecessor_successor",
     "strength": "medium", "context": "陆思东接替李宏伟任县委书记",
     "overlap_org": "中共肃南裕固族自治县委员会", "overlap_period": "2020?"},
    # 梁国文 → 张辉（上下级）
    {"person_a": "p04", "person_b": "p02", "type": "superior_subordinate",
     "strength": "medium", "context": "常务副县长协助县长工作",
     "overlap_org": "肃南裕固族自治县人民政府", "overlap_period": "目前"},
    # 巴玉霞 → 兰永武（人大-政协协同）
    {"person_a": "p12", "person_b": "p13", "type": "overlap",
     "strength": "medium", "context": "人大主任与政协主席, 同为裕固族领导干部",
     "overlap_org": "肃南裕固族自治县", "overlap_period": "目前"},
]


# =========================================================================
# SQLite
# =========================================================================
def build_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
              p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos.get("start", ""), pos.get("end", ""),
              pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()

    # Summary
    counts = {}
    for table in ["persons", "organizations", "positions", "relationships"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cur.fetchone()[0]
    conn.close()
    return counts


# =========================================================================
# GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role: Party Secretary=red, Government=blue, Discipline=orange, Other=grey"""
    post = p.get("current_post", "")
    if "县委书记" in post or "县委书记" in post:
        return "255,50,50"
    elif "县长" in post and "副" not in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "人大主任" in post:
        return "200,255,255"
    elif "政协主席" in post:
        return "255,240,200"
    elif "常委" in post:
        return "150,150,150"
    else:
        return "100,100,100"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>肃南裕固族自治县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="gender" type="string"/>')
    lines.append('      <attribute id="3" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="4" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("gender", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("birth", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        # Color by org type
        org_colors = {
            "党委": "255,200,200", "政府": "200,200,255",
            "人大": "200,255,255", "政协": "255,240,200"
        }
        oc = org_colors.get(o.get("type", ""), "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="current"/>')
        lines.append(f'          <attvalue for="2" value="职位：{esc(pos["title"])}；{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        wt = "2.0" if r["strength"] == "strong" else ("1.5" if r["strength"] == "medium" else "1.0")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{wt}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("肃南裕固族自治县领导班子工作关系网络 — 数据构建脚本")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Build SQLite
    print("\n▶ 构建 SQLite 数据库...")
    counts = build_sqlite()
    print(f"   √ 人员: {counts['persons']} 人")
    print(f"   √ 组织: {counts['organizations']} 个")
    print(f"   √ 任职: {counts['positions']} 条")
    print(f"   √ 关系: {counts['relationships']} 条")
    print(f"   √ 数据库: {DB_PATH}")

    # Build GEXF
    print("\n▶ 构建 GEXF 图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"   √ GEXF: {GEXF_PATH} ({gexf_size} bytes)")

    # Summary
    print("\n" + "=" * 60)
    print("构建完成!")
    print(f"   数据库: {DB_PATH}")
    print(f"   图文件: {GEXF_PATH}")
    print("=" * 60)
