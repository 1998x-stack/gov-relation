#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 安顺市 leadership network (地级市).

Targets: 市委书记 (刘永升) & 市长 (尹恒斌)
Data as of: 2026-08-05
Sources:
- 安顺市人民政府门户 www.anshun.gov.cn — 政务公开·政府领导 (市长、副市长、秘书长简历)
- 安顺市人民政府门户 安顺要闻 2026-07/08 — 市委常委会、军事日活动、领导调研新闻
- 紫云县跨县干部交流调查（本仓库 2026-07-23）
- 安顺市各县区现有数据库（西秀/平坝/普定/关岭/紫云，本仓库 2026-07-23）

Verification status:
- 现任核心领导（书记/市长/人大/政协/副书记/各副市长/秘书长）身份 confirmed（官方政府网站）
- 纪委书记、组织部长、宣传部长、政法委书记 姓名未获官方公开源确认 → 不作猜测
- 前任书记/市长完整交接 及 刘永升/高晓昀/韩佐芝/陈健 详细履历 → 待查（列入 open gaps）
"""

import os
import re
import sqlite3
from datetime import datetime

# Staging directory
TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(TMP_DIR, "..", "..", "..")
DB_PATH = os.path.join(TMP_DIR, "安顺市_network.db")
GEXF_PATH = os.path.join(TMP_DIR, "安顺市_network.gexf")

# ── Data ──────────────────────────────────────────────────────────────────
# person ids: 1-20 city-level; 21+ county officials that link to city
persons = [
    # === 市级核心班子（身份 confirmed：官方政府网站）===
    {
        "id": 1, "name": "刘永升", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "安顺市委书记、安顺军分区党委第一书记",
        "current_org": "中共安顺市委员会",
        "source": "安顺市人民政府网·安顺要闻 2026-07-24/2026-07-30",
    },
    {
        "id": 2, "name": "尹恒斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年9月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市委副书记、市人民政府市长、市政府党组书记",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/sz_1/202407/t20240719_85136274.html",
    },
    {
        "id": 3, "name": "陈健", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市人大常委会党组书记、主任",
        "current_org": "安顺市人大常委会",
        "source": "安顺市人民政府网·安顺要闻 2026-07-24（市委常委会报道）",
    },
    {
        "id": 4, "name": "韩佐芝", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市政协党组书记",
        "current_org": "政协安顺市委员会",
        "source": "安顺市人民政府网·安顺要闻 2026-07-24/2026-07-30",
    },
    {
        "id": 5, "name": "高晓昀", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市委副书记",
        "current_org": "中共安顺市委员会",
        "source": "安顺市人民政府网·安顺要闻 2026-07-24（市委常委会报道）",
    },
    # === 市政府领导（官方政务公开/领导）===
    {
        "id": 6, "name": "林松", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年5月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市委常委、常务副市长、市政府党组副书记",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202410/t20241015_85940327.html",
    },
    {
        "id": 7, "name": "周彬", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年2月", "birthplace": "", "education": "大学学历，管理学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市委常委、副市长（挂职）",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202410/t20241015_85940350.html",
    },
    {
        "id": 8, "name": "贺未泓", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年6月", "birthplace": "", "education": "大学学历",
        "party_join": "九三学社社员", "work_start": "",
        "current_post": "安顺市人民政府副市长",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202501/t20250120_86652979.html",
    },
    {
        "id": 9, "name": "栾雁", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年12月", "birthplace": "", "education": "大学学历，经济学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市人民政府副市长",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202410/t20241015_85940394.html",
    },
    {
        "id": 10, "name": "潘登岭", "gender": "女", "ethnicity": "苗族",
        "birth": "1973年1月", "birthplace": "", "education": "研究生学历，法学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市人民政府副市长",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202410/t20241015_85940402.html",
    },
    {
        "id": 11, "name": "石藩", "gender": "男", "ethnicity": "汉族",
        "birth": "1985年11月", "birthplace": "", "education": "大学学历，工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市人民政府副市长",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202501/t20250121_86657156.html",
    },
    {
        "id": 12, "name": "赵温跃", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年5月", "birthplace": "", "education": "大学学历，工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市人民政府副市长",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202410/t20241015_85940455.html",
    },
    {
        "id": 13, "name": "吴贵森", "gender": "男", "ethnicity": "彝族",
        "birth": "1973年5月", "birthplace": "", "education": "中央党校学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "安顺市人民政府副市长、市公安局局长",
        "current_org": "安顺市人民政府 / 安顺市公安局",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/fsz_1/202505/t20250515_87875021.html",
    },
    {
        "id": 14, "name": "胡成虎", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "安顺市人民政府秘书长",
        "current_org": "安顺市人民政府",
        "source": "https://www.anshun.gov.cn/zfxxgk/fdzdgknr/jgjj/zfld/",
    },
    # === 市级领导（新闻提及，职务待确认）===
    {
        "id": 15, "name": "王勋勇", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "安顺市领导",
        "current_org": "中共安顺市委员会",
        "source": "安顺市人民政府网 2026-07-15 刘永升到紫云调研（陪同领导）",
    },
    {
        "id": 16, "name": "王瑛", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "安顺市领导",
        "current_org": "中共安顺市委员会",
        "source": "安顺市人民政府网 2026-07-15 刘永升到紫云调研（陪同领导）",
    },
    {
        "id": 17, "name": "张翼", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "安顺市领导",
        "current_org": "中共安顺市委员会",
        "source": "安顺市人民政府网 2026-07-15 刘永升到紫云调研（陪同领导）",
    },
    # === 县（区）负责干部（本市网络延伸；身份 confirmed：各县区数据库）===
    {
        "id": 21, "name": "朱煜", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "安顺市委常委、西秀区委书记",
        "current_org": "中共安顺市委员会 / 中共安顺市西秀区委员会",
        "source": "本仓库 西秀区数据库（2026-07-17 到岗）",
    },
    {
        "id": 22, "name": "黄浩洋", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年5月", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "紫云苗族布依族自治县委书记",
        "current_org": "中共紫云苗族布依族自治县委员会",
        "source": "本仓库 data/persons 20260723-安顺紫云县（2026-07）",
    },
    {
        "id": 23, "name": "王埝", "gender": "", "ethnicity": "",
        "birth": "1980年9月", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "（原关岭县委书记，2026年调任遵义市副市长）",
        "current_org": "中共关岭布依族苗族自治县委员会（2026年离任）",
        "source": "本仓库 data/persons 20260723-关岭 + 遵义市build脚本（2026-08）",
    },
]

organizations = [
    {"id": 1, "name": "中共安顺市委员会", "type": "党委",
     "level": "地级市", "parent": "中共贵州省委员会", "location": "贵州省安顺市"},
    {"id": 2, "name": "安顺市人民政府", "type": "政府",
     "level": "地级市", "parent": "贵州省人民政府", "location": "贵州省安顺市"},
    {"id": 3, "name": "安顺市人大常委会", "type": "人大",
     "level": "地级市", "parent": "贵州省人大常委会", "location": "贵州省安顺市"},
    {"id": 4, "name": "政协安顺市委员会", "type": "政协",
     "level": "地级市", "parent": "政协贵州省委员会", "location": "贵州省安顺市"},
    {"id": 5, "name": "安顺市公安局", "type": "政府",
     "level": "地级市", "parent": "安顺市人民政府", "location": "贵州省安顺市"},
    {"id": 6, "name": "中共贵州省委员会", "type": "党委",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 7, "name": "贵州省人民政府", "type": "政府",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 8, "name": "中共安顺市西秀区委员会", "type": "党委",
     "level": "县处级", "parent": "中共安顺市委员会", "location": "贵州省安顺市西秀区"},
    {"id": 9, "name": "中共紫云苗族布依族自治县委员会", "type": "党委",
     "level": "县处级", "parent": "中共安顺市委员会", "location": "贵州省安顺市紫云县"},
    {"id": 10, "name": "中共关岭布依族苗族自治县委员会", "type": "党委",
     "level": "县处级", "parent": "中共安顺市委员会", "location": "贵州省安顺市关岭县"},
    {"id": 11, "name": "政协贵州省委员会", "type": "政协",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 12, "name": "贵州省人大常委会", "type": "人大",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
]

positions = [
    # 市级党委班子
    {"person_id": 1, "org_id": 1, "title": "安顺市委书记、安顺军分区党委第一书记", "start": "2024", "end": "present", "rank": "正厅级", "note": "2026-07 报道多次确认；到任期约2024"},
    {"person_id": 2, "org_id": 1, "title": "安顺市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "安顺市人民政府市长、市政府党组书记", "start": "", "end": "present", "rank": "正厅级", "note": "负责市审计、粮食工作，分管市审计局"},
    {"person_id": 5, "org_id": 1, "title": "安顺市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "安顺市人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "安顺市政协党组书记", "start": "", "end": "present", "rank": "正厅级", "note": "主席职务待确认"},
    # 市政府班子
    {"person_id": 6, "org_id": 2, "title": "安顺市委常委、常务副市长、市政府党组副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "安顺市委常委、副市长（挂职）", "start": "", "end": "present", "rank": "副厅级", "note": "中央单位定点帮扶挂职"},
    {"person_id": 8, "org_id": 2, "title": "安顺市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "民主党派（九三学社）"},
    {"person_id": 9, "org_id": 2, "title": "安顺市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "安顺市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "苗族女性领导"},
    {"person_id": 11, "org_id": 2, "title": "安顺市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "安顺市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "安顺市人民政府副市长、市公安局局长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "安顺市公安局局长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "安顺市人民政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 市级领导（新闻提及，职务待确认）
    {"person_id": 15, "org_id": 1, "title": "安顺市领导", "start": "", "end": "present", "rank": "", "note": "陪同刘永升到紫云调研"},
    {"person_id": 16, "org_id": 1, "title": "安顺市领导", "start": "", "end": "present", "rank": "", "note": "陪同刘永升到紫云调研"},
    {"person_id": 17, "org_id": 1, "title": "安顺市领导", "start": "", "end": "present", "rank": "", "note": "陪同刘永升到紫云调研"},
    # 县（区）干部
    {"person_id": 21, "org_id": 1, "title": "安顺市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 21, "org_id": 8, "title": "西秀区委书记", "start": "2024", "end": "present", "rank": "正处级", "note": "以安顺市委常委兼任"},
    {"person_id": 22, "org_id": 9, "title": "紫云自治县委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 10, "title": "关岭自治县委书记（曾任）", "start": "2025-02", "end": "2026", "rank": "正处级", "note": "2026年调任遵义市副市长（待确认）"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政一把手搭档",
     "context": "刘永升（市委书记）与尹恒斌（市委副书记、市长）为安顺党政一把手搭档关系",
     "overlap_org": "中共安顺市委员会 / 安顺市人民政府",
     "overlap_period": "2024至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "刘永升与陈健（市人大常委会主任）共事，出席市委常委会",
     "overlap_org": "安顺市四套班子/市委常委会",
     "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "刘永升与韩佐芝（市政协党组书记）共同出席市委常委会/军事日活动",
     "overlap_org": "安顺市四套班子/政协安顺市委员会",
     "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "刘永升（书记）与高晓昀（市委副书记）为直接上下级，共同出席市委常委会",
     "overlap_org": "中共安顺市委员会",
     "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 21, "type": "上下级",
     "context": "朱煜（安顺市委常委、西秀区委书记）为刘永升担任的安顺市委市委常委，受市委统一领导",
     "overlap_org": "中共安顺市委员会",
     "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "林松（市委常委、常务副市长）受市委和市委书记领导",
     "overlap_org": "中共安顺市委员会",
     "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "领导下属",
     "context": "尹恒斌（市长）与常务副市长林松在市政府工作中为领导下属关系",
     "overlap_org": "安顺市人民政府",
     "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "领导下属",
     "context": "尹恒斌与副市长（挂职）周彬在市政府工作中为领导下属关系",
     "overlap_org": "安顺市人民政府",
     "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "领导下属",
     "context": "尹恒斌与副市长贺未泓（九三学社）在市政府班子中共事",
     "overlap_org": "安顺市人民政府",
     "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "领导下属",
     "context": "尹恒斌与市公安局局长吴贵森在市政府及公安系统工作中上下级共事",
     "overlap_org": "安顺市人民政府/安顺市公安局",
     "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 6, "type": "同班子",
     "context": "高晓昀（市委副书记）与常务副市长林松同为市委班子/市政府分管领导，共同参与市委常委会",
     "overlap_org": "中共安顺市委员会",
     "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 21, "person_b": 2, "type": "上下级",
     "context": "朱煜（西秀区委书记）作为市委常委，与市长尹恒斌同属市委班子（双方直接互动报道较少，关系从组织架构推断）",
     "overlap_org": "中共安顺市委员会",
     "overlap_period": "2026", "strength": "weak", "confidence": "plausible"},
]

# ═══════════════════════════════════════════════════════
#  Build SQLite DB
# ═══════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    strength TEXT, confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

cur.executemany(
    "INSERT OR REPLACE INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)",
    persons,
)
cur.executemany(
    "INSERT OR REPLACE INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)",
    organizations,
)
cur.executemany(
    "INSERT INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)",
    positions,
)
cur.executemany(
    "INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period,:strength,:confidence)",
    relationships,
)

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
psc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc = cur.fetchone()[0]
conn.close()

print(f"Database: {DB_PATH}")
print(f"  Persons: {pc}, Organizations: {oc}, Positions: {psc}, Relationships: {rc}")

# ═══════════════════════════════════════════════════════
#  Build GEXF Graph
# ═══════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    title = p.get("current_post", "")
    if "市委书记" in title:
        return "255,50,50"
    if "市长" in title and "副" not in title:
        return "50,100,255"
    if "纪委书记" in title or "纪委" in title:
        return "255,165,0"
    if "人大" in title:
        return "200,255,255"
    if "政协" in title:
        return "255,240,200"
    if "副市长" in title or "秘书长" in title:
        return "100,100,255"
    return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    title = p.get("current_post", "")
    return "市委书记" in title or ("市长" in title and "副" not in title)


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append("    <creator>Gov Relation Research Agent</creator>")
lines.append(f"    <description>安顺市领导班子关系网络 — 数据截至 {datetime.now().strftime('%Y-%m-%d')}</description>")
lines.append("  </meta>")
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="education" type="string"/>')
lines.append("    </attributes>")

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="confidence" type="string"/>')
lines.append("    </attributes>")

# Nodes
lines.append("    <nodes>")
for p in persons:
    pid = p["id"]
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p.get("education",""))}"/>')
    lines.append("        </attvalues>")
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append("      </node>")

for o in organizations:
    oid = o["id"]
    c = org_color(o)
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
    lines.append("        </attvalues>")
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append("      </node>")

lines.append("    </nodes>")

# Edges
lines.append("    <edges>")
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
    lines.append('          <attvalue for="2" value="confirmed"/>')
    lines.append("        </attvalues>")
    lines.append("      </edge>")

for r in relationships:
    eid += 1
    w = "2.0" if r.get("strength") == "strong" else "1.0"
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type",""))}" weight="{w}">')
    lines.append("        <attvalues>")
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence",""))}"/>')
    lines.append("        </attvalues>")
    lines.append("      </edge>")

lines.append("    </edges>")
lines.append("  </graph>")
lines.append("</gexf>")

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"GEXF: {GEXF_PATH}")
print(f"  Total edges: {eid}")

print("\nDone.")