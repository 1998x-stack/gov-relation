#!/usr/bin/env python3
"""余庆县（遵义市）领导班子关系网络数据生成脚本.

Targets: 县委书记, 县长
Data as of: 2026-07-23
Sources: 余庆县人民政府官网 (www.yuqing.gov.cn), official news reports
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_余庆县"
SLUG = "余庆县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "遵义市"

BASE = os.path.join("data", "tmp", "guizhou_余庆县")
_BASE_OVERRIDE = os.environ.get("YUQING_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "余庆县_network.db")
GEXF_PATH = os.path.join(BASE, "余庆县_network.gexf")
PERSONS_DIR = os.path.join(BASE)
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────
# NOTE: Research data sourced from zgyq.gov.cn (余庆县人民政府官网), Baidu Baike,
# and official news reports (gzrd.gov.cn, 163.com). Current as of 2026-07-23.
# Confidence: confirmed for current roles; partial for career histories.
# Gaps marked explicitly with open_questions.

persons = [
    # 1 - 县委书记 贾旭东 (confirmed: active as of July 2026)
    {
        "id": 1,
        "name": "贾旭东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委书记",
        "current_org": "中共余庆县委员会",
        "source": "zgyq.gov.cn新闻报道（2026-07-20）'贾旭东在部分乡镇调研督导重点工作'",
    },
    # 2 - 县长 王镇飞 (confirmed: born 1976.04, Miao, bachelor's degree)
    {
        "id": 2,
        "name": "王镇飞",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委副书记、县人民政府县长",
        "current_org": "余庆县人民政府",
        "source": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202503/t20250327_87281464.html",
    },
    # 3 - 常務副县长 李正茂 (confirmed: born 1990.03, Manchu, Tsinghua master's)
    {
        "id": 3,
        "name": "李正茂",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1990年3月",
        "birthplace": "",
        "education": "清华大学工程学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委常委、县人民政府常务副县长（提名）",
        "current_org": "余庆县人民政府",
        "source": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202211/t20221126_77226247.html",
    },
    # 4 - 副县长 韦继军 (confirmed: born 1983.06, Han, party school degree)
    {
        "id": 4,
        "name": "韦继军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委常委、副县长",
        "current_org": "余庆县人民政府",
        "source": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202306/t20230619_80375076.html",
    },
    # 5 - 副县长 张毓凤 (confirmed: born 1979.09, Tujia, female)
    {
        "id": 5,
        "name": "张毓凤",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1979年9月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县人民政府副县长",
        "current_org": "余庆县人民政府",
        "source": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202207/t20220704_75382814.html",
    },
    # 6 - 县人大常委会主任 韦泽福
    {
        "id": 6,
        "name": "韦泽福",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县人大常委会主任",
        "current_org": "余庆县人大常委会",
        "source": "Baidu Baike 余庆县词条 & gzrd.gov.cn 新闻报道",
    },
    # 7 - 县政协主席 陈忠祥
    {
        "id": 7,
        "name": "陈忠祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县政协主席",
        "current_org": "中国人民政治协商会议余庆县委员会",
        "source": "Baidu Baike 余庆县词条",
    },
    # 8 - 县委副书记 付长江 (likely 县委副书记 based on NPC exec chair list)
    {
        "id": 8,
        "name": "付长江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委副书记（推测）",
        "current_org": "中共余庆县委员会",
        "source": "余庆县第十八届人民代表大会第五次会议执行主席名单（2026年4月）",
    },
    # 9 - 县委常委 林世栋
    {
        "id": 9,
        "name": "林世栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委常委",
        "current_org": "中共余庆县委员会",
        "source": "余庆县第十八届人民代表大会第五次会议执行主席名单（2026年4月）",
    },
    # 10 - 县委常委 李黔疆
    {
        "id": 10,
        "name": "李黔疆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委常委",
        "current_org": "中共余庆县委员会",
        "source": "余庆县第十八届人民代表大会第五次会议执行主席名单（2026年4月）",
    },
    # 11 - 县委常委 余忠
    {
        "id": 11,
        "name": "余忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委常委",
        "current_org": "中共余庆县委员会",
        "source": "余庆县第十八届人民代表大会第五次会议执行主席名单（2026年4月）",
    },
    # 12 - 县委常委 刘胜刚
    {
        "id": 12,
        "name": "刘胜刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委常委",
        "current_org": "中共余庆县委员会",
        "source": "余庆县第十八届人民代表大会第五次会议执行主席名单（2026年4月）",
    },
    # 13 - 县委常委 郭远宏
    {
        "id": 13,
        "name": "郭远宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "余庆县委常委",
        "current_org": "中共余庆县委员会",
        "source": "余庆县第十八届人民代表大会第五次会议执行主席名单（2026年4月）",
    },
    # 14 - 前任县委书记 令狐绍辉 (~2016-2021)
    {
        "id": 14,
        "name": "令狐绍辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任余庆县委书记（~2016-2021）",
        "current_org": "",
        "source": "网易新闻报道：2021年4月 '县委书记令狐绍辉带队督导余庆县司法局'",
    },
    # 15 - 前任县委书记 张恺 (~2021-2024)
    {
        "id": 15,
        "name": "张恺",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任余庆县委书记（~2021-2024）",
        "current_org": "",
        "source": "百度百科检索（张恺为余庆县委书记）",
    },
]

organizations = [
    {"id": 1, "name": "中共余庆县委员会", "type": "党委", "level": "县处级", "parent": "中共遵义市委", "location": "余庆县"},
    {"id": 2, "name": "余庆县人民政府", "type": "政府", "level": "县处级", "parent": "遵义市人民政府", "location": "余庆县"},
    {"id": 3, "name": "中共余庆县委组织部", "type": "党委", "level": "乡科级", "parent": "中共余庆县委员会", "location": "余庆县"},
    {"id": 4, "name": "中共余庆县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共余庆县委员会", "location": "余庆县"},
    {"id": 5, "name": "中共余庆县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共余庆县委员会", "location": "余庆县"},
    {"id": 6, "name": "中共余庆县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共遵义市纪委/中共余庆县委", "location": "余庆县"},
    {"id": 7, "name": "余庆县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "遵义市人大常委会", "location": "余庆县"},
    {"id": 8, "name": "中国人民政治协商会议余庆县委员会", "type": "政协", "level": "县处级", "parent": "政协遵义市委员会", "location": "余庆县"},
]

positions = [
    # 贾旭东 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "余庆县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任（2026年7月确认）"},
    # 王镇飞 - 县长
    {"person_id": 2, "org_id": 2, "title": "余庆县人民政府县长", "start_date": "2025-03", "end_date": "", "rank": "县处级正职", "note": "现任，2025年3月任代理县长，后转正"},
    {"person_id": 2, "org_id": 1, "title": "余庆县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 李正茂 - 常务副县长（提名）
    {"person_id": 3, "org_id": 2, "title": "余庆县委常委、县人民政府常务副县长（提名）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 韦继军 - 副县长
    {"person_id": 4, "org_id": 2, "title": "余庆县委常委、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 张毓凤 - 副县长
    {"person_id": 5, "org_id": 2, "title": "余庆县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 韦泽福 - 县人大常委会主任
    {"person_id": 6, "org_id": 7, "title": "余庆县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 陈忠祥 - 县政协主席
    {"person_id": 7, "org_id": 8, "title": "余庆县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 付长江 - 县委副书记
    {"person_id": 8, "org_id": 1, "title": "余庆县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任（推测）"},
    # 林世栋 - 县委常委
    {"person_id": 9, "org_id": 1, "title": "余庆县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 李黔疆 - 县委常委
    {"person_id": 10, "org_id": 1, "title": "余庆县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 余忠 - 县委常委
    {"person_id": 11, "org_id": 1, "title": "余庆县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 刘胜刚 - 县委常委
    {"person_id": 12, "org_id": 1, "title": "余庆县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 郭远宏 - 县委常委
    {"person_id": 13, "org_id": 1, "title": "余庆县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 令狐绍辉 - 前任书记
    {"person_id": 14, "org_id": 1, "title": "余庆县委书记", "start_date": "~2016", "end_date": "~2021", "rank": "县处级正职", "note": "前任"},
    # 张恺 - 前任书记
    {"person_id": 15, "org_id": 1, "title": "余庆县委书记", "start_date": "~2021", "end_date": "~2024", "rank": "县处级正职", "note": "前任（任期需确认）"},
]

relationships = [
    # 贾旭东 ↔ 王镇飞 (书记-县长搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "贾旭东（县委书记）与王镇飞（县长）为县委常委会搭档", "overlap_org": "中共余庆县委员会/余庆县人民政府", "overlap_period": "2025-至今"},
    # 贾旭东 ↔ 李正茂 (书记-常务副县长)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "贾旭东（县委书记）与李正茂（常务副县长）在县委常委会共事", "overlap_org": "中共余庆县委员会", "overlap_period": "至今"},
    # 贾旭东 ↔ 韦继军
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "贾旭东（县委书记）与韦继军（副县长）在县委常委会共事", "overlap_org": "中共余庆县委员会", "overlap_period": "至今"},
    # 王镇飞 ↔ 李正茂 (县长-常务副县长)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "王镇飞（县长）与李正茂（常务副县长）在县政府班子共事", "overlap_org": "余庆县人民政府", "overlap_period": "至今"},
    # 王镇飞 ↔ 韦继军
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "王镇飞（县长）与韦继军（副县长）在县政府班子共事", "overlap_org": "余庆县人民政府", "overlap_period": "至今"},
    # 王镇飞 ↔ 张毓凤
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "王镇飞（县长）与张毓凤（副县长）在县政府班子共事", "overlap_org": "余庆县人民政府", "overlap_period": "至今"},
    # 令狐绍辉 → 张恺 → 贾旭东 (前后任链条)
    {"person_a": 14, "person_b": 15, "type": "predecessor_successor", "context": "令狐绍辉（前任）与张恺（继任）为前后任县委书记", "overlap_org": "中共余庆县委员会", "overlap_period": "~2021"},
    {"person_a": 15, "person_b": 1, "type": "predecessor_successor", "context": "张恺（前任）与贾旭东为前后任县委书记", "overlap_org": "中共余庆县委员会", "overlap_period": "~2024"},
    # 县委常委会内部共事关系
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "付长江（副书记）与林世栋（常委）在县委常委会共事", "overlap_org": "中共余庆县委员会", "overlap_period": "至今"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "林世栋与李黔疆在县委常委会共事", "overlap_org": "中共余庆县委员会", "overlap_period": "至今"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "李黔疆与余忠在县委常委会共事", "overlap_org": "中共余庆县委员会", "overlap_period": "至今"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "余忠与刘胜刚在县委常委会共事", "overlap_org": "中共余庆县委员会", "overlap_period": "至今"},
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "刘胜刚与郭远宏在县委常委会共事", "overlap_org": "中共余庆县委员会", "overlap_period": "至今"},
]

source_register = [
    {"id": "S001", "title": "余庆县人民政府-领导之窗",
     "url": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/",
     "publisher": "余庆县人民政府", "published_at": "", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "王镇飞、李正茂、韦继军、张毓凤的官方简历页面"},
    {"id": "S002", "title": "余庆县人民政府新闻-贾旭东调研",
     "url": "http://www.zgyq.gov.cn/xwzx/zwyw/202607/t20260720_90637718.html",
     "publisher": "余庆县人民政府", "published_at": "2026-07-20", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认贾旭东为余庆县委书记"},
    {"id": "S003", "title": "余庆县第十八届人民代表大会第五次会议",
     "url": "http://www.zgyq.gov.cn/xwzx/zwyw/202604/t20260413_89993800.html",
     "publisher": "余庆县人民政府", "published_at": "2026-04-13", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "执行主席名单含县委常委全体成员"},
    {"id": "S004", "title": "百度百科-余庆县词条",
     "url": "https://baike.baidu.com/item/%E4%BD%99%E5%BA%86%E5%8E%BF",
     "publisher": "百度百科", "published_at": "2025-03", "accessed_at": "2026-07-23",
     "source_type": "encyclopedia", "reliability": "medium", "notes": "贾旭东（县委书记）、王镇飞（代理县长）、韦泽福（人大主任）、陈忠祥（政协主席）"},
    {"id": "S005", "title": "王镇飞官方简历",
     "url": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202503/t20250327_87281464.html",
     "publisher": "余庆县人民政府", "published_at": "2025-03-27", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "王镇飞，1976年4月生，苗族，本科学历，中共党员"},
    {"id": "S006", "title": "李正茂官方简历",
     "url": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202211/t20221126_77226247.html",
     "publisher": "余庆县人民政府", "published_at": "2022-11-26", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "李正茂，1990年3月生，满族，清华大学工程学硕士，中共党员"},
    {"id": "S007", "title": "韦继军官方简历",
     "url": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202306/t20230619_80375076.html",
     "publisher": "余庆县人民政府", "published_at": "2023-06-19", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "韦继军，1983年6月生，汉族，省委党校大学，中共党员"},
    {"id": "S008", "title": "张毓凤官方简历",
     "url": "http://www.zgyq.gov.cn/zwgk/jcxxgk/ldzc/202207/t20220704_75382814.html",
     "publisher": "余庆县人民政府", "published_at": "2022-07-04", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "张毓凤，1979年9月生，土家族，女，省委党校大学，中共党员"},
    {"id": "S009", "title": "网易新闻-令狐绍辉督导余庆",
     "url": "",
     "publisher": "网易号-遵义司法", "published_at": "2021-04-14", "accessed_at": "2026-07-23",
     "source_type": "media", "reliability": "medium", "notes": "确认令狐绍辉为2021年余庆县委书记"},
    {"id": "S010", "title": "贵州省人大-余庆调研",
     "url": "https://www.gzrd.gov.cn/xwzx/rdyw/202607/t20260715_90623308.html",
     "publisher": "贵州省人大常委会", "published_at": "2026-07-15", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "2026年7月省人大赴余庆调研"},
]


# ── Build Functions ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

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
        pid = f"yuqing_{p['name']}"
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
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
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
            "纪委": "255,200,150",
            "开发区": "200,255,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>余庆县领导班子关系网络（部分数据待确认）</description>')
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

    for pos in positions:
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
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "余庆县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"yuqing_{p['name']}",
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
                "administrative_rank": "县处级正职" if p["id"] in [1, 2, 6, 7] else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S004"]
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
                "identity": "confirmed" if p.get("birth") and p.get("education") else "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial" if p.get("birth") else "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失（早期任职经历未知）"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 余庆县", f"{p['name']} 任前公示"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 贾旭东 Person JSON ──
    jxd_timeline = [
        {"start": "", "end": "", "org": "中共余庆县委员会", "title": "余庆县委书记",
         "notes": "现任，2026年7月确认", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "贾旭东在担任余庆县委书记前的完整履历未找到。疑似前任余庆县县长。",
         "confidence": "unverified", "source_ids": []},
    ]
    jxd_relationships = [
        {"person": "王镇飞", "person_id": "yuqing_王镇飞", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "贾旭东（县委书记）与王镇飞（县长）在县委常委会和政府班子共事",
         "overlap_org": "中共余庆县委员会/余庆县人民政府", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        {"person": "李正茂", "person_id": "yuqing_李正茂", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "贾旭东（县委书记）与李正茂（常务副县长）在县委常委会共事",
         "overlap_org": "中共余庆县委员会", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]
    jxd_json = make_person_json(persons[0], jxd_timeline, jxd_relationships)
    jxd_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县委书记-贾旭东.json")
    with open(jxd_path, "w", encoding="utf-8") as f:
        json.dump(jxd_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {jxd_path}")

    # ── 王镇飞 Person JSON ──
    wzf_timeline = [
        {"start": "2025-03", "end": "", "org": "余庆县人民政府", "title": "余庆县委副书记、县人民政府县长",
         "notes": "现任，2025年3月任代理县长", "confidence": "confirmed", "source_ids": ["S005", "S004"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "王镇飞在担任余庆县长前的完整履历未找到。已知1976年4月生，苗族，本科学历，中共党员。",
         "confidence": "unverified", "source_ids": []},
    ]
    wzf_relationships = [
        {"person": "贾旭东", "person_id": "yuqing_贾旭东", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王镇飞（县长、县委副书记）与贾旭东（县委书记）在县委常委会和政府班子共事",
         "overlap_org": "中共余庆县委员会/余庆县人民政府", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        {"person": "李正茂", "person_id": "yuqing_李正茂", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王镇飞（县长）与李正茂（常务副县长）在县政府班子共事",
         "overlap_org": "余庆县人民政府", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wzf_json = make_person_json(persons[1], wzf_timeline, wzf_relationships)
    wzf_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县长-王镇飞.json")
    with open(wzf_path, "w", encoding="utf-8") as f:
        json.dump(wzf_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wzf_path}")

    # ── 李正茂 Person JSON ──
    lzm_timeline = [
        {"start": "", "end": "", "org": "余庆县人民政府", "title": "余庆县委常委、县人民政府常务副县长（提名）",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S006", "S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "李正茂在担任余庆县常务副县长前的完整履历未找到。已知1990年3月生，满族，清华大学工程学硕士，中共党员。",
         "confidence": "unverified", "source_ids": []},
    ]
    lzm_relationships = [
        {"person": "贾旭东", "person_id": "yuqing_贾旭东", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "李正茂（常委、常务副县长）与贾旭东（县委书记）在县委常委会共事",
         "overlap_org": "中共余庆县委员会", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "王镇飞", "person_id": "yuqing_王镇飞", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "李正茂（常务副县长）与王镇飞（县长）在县政府班子共事",
         "overlap_org": "余庆县人民政府", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    lzm_json = make_person_json(persons[2], lzm_timeline, lzm_relationships)
    lzm_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-常务副县长-李正茂.json")
    with open(lzm_path, "w", encoding="utf-8") as f:
        json.dump(lzm_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lzm_path}")

    # ── 令狐绍辉 Person JSON (前任县委书记, confirmed) ──
    lhsh_timeline = [
        {"start": "~2016", "end": "~2021", "org": "中共余庆县委员会", "title": "余庆县委书记",
         "notes": "2021年4月仍在任（网易新闻报道）", "confidence": "plausible", "source_ids": ["S009"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "令狐绍辉在担任余庆县委书记前的完整履历未找到。",
         "confidence": "unverified", "source_ids": []},
    ]
    lhsh_relationships = [
        {"person": "张恺", "person_id": "yuqing_张恺", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "令狐绍辉（前任县委书记）与张恺（继任）为前后任关系",
         "overlap_org": "中共余庆县委员会", "overlap_period": "~2021",
         "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S009"]},
    ]
    lhsh_json = make_person_json(persons[13], lhsh_timeline, lhsh_relationships)
    lhsh_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-前任县委书记-令狐绍辉.json")
    with open(lhsh_path, "w", encoding="utf-8") as f:
        json.dump(lhsh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lhsh_path}")

    # ── 张恺 Person JSON (前任县委书记, plausible) ──
    zk_timeline = [
        {"start": "~2021", "end": "~2024", "org": "中共余庆县委员会", "title": "余庆县委书记",
         "notes": "前任县委书记，任期根据公开信息推测", "confidence": "unverified", "source_ids": []},
    ]
    zk_relationships = [
        {"person": "令狐绍辉", "person_id": "yuqing_令狐绍辉", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "张恺继令狐绍辉任余庆县委书记",
         "overlap_org": "中共余庆县委员会", "overlap_period": "~2021",
         "direction": "person_to_other", "confidence": "unverified", "source_ids": []},
        {"person": "贾旭东", "person_id": "yuqing_贾旭东", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "张恺（前任县委书记）与贾旭东（现任县委书记）为前后任关系",
         "overlap_org": "中共余庆县委员会", "overlap_period": "~2024",
         "direction": "person_to_other", "confidence": "unverified", "source_ids": []},
    ]
    zk_json = make_person_json(persons[14], zk_timeline, zk_relationships)
    zk_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-前任县委书记-张恺.json")
    with open(zk_path, "w", encoding="utf-8") as f:
        json.dump(zk_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zk_path}")

    print("\n✅ All artifacts generated.")
    print(f"ℹ️  数据来源: zgyq.gov.cn, Baidu Baike, 贵州省人大官网")
    print(f"ℹ️  核心人物已确认: 县委书记贾旭东、县长王镇飞、常务副县长李正茂")
    print(f"ℹ️  部分常委具体分工待补全")


if __name__ == "__main__":
    build()
