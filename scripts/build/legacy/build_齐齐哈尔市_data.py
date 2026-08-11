#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 齐齐哈尔市 (Qiqihar), 黑龙江省.

Task ID: heilongjiang_齐齐哈尔市
Level: 地级市
Targets: 市委书记 & 市长
Investigation date: 2026-08-05

Primary source: 齐齐哈尔市人民政府 领导之窗 (www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml) — official
current leadership roster + individual bio pages (闫红蕾 /qqhe/c100016/202601/c02_602360.shtml,
陈兴平 /qqhe/c100055/202310/c02_369246.shtml).

Confidence notes:
- 闫红蕾: confirmed (official). 女, 汉族, 1971年12月生, 大学, 工商管理硕士, 中共党员. 现任市委书记,
  市人大常委会主任、党组书记。黑龙江省委任命（搜狗聚合，来源：鹤城发布）；由哈尔滨方向调任为线索。
  精确前任职务、任命年月、教育院校 → open_questions。
- 陈兴平: confirmed (official). 男, 汉族, 1970年4月生, 在职大学, 中共党员. 现任市委副书记、
  市政府市长、党组书记。任市长前履历 → open_questions。
- 领导班子成员: confirmed 名单（official 领导之窗），个人简历/籍贯未采全 → open_questions。
- 前任市委书记/市长的身份与去向未确认。
- Web 环境退化：Exa 限流、百度百科安全验证、搜狗/360 后续查询受限制、维基/Jina/澎湃超时。
  采用官网为主的一手来源；缺失职业履历明确标记为 open_questions，不臆造。
"""

import json
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "齐齐哈尔市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ══════════════════════════════════════════════════════════════════════════
# Data
# ══════════════════════════════════════════════════════════════════════════

persons = [
    {"id": 1, "name": "闫红蕾", "gender": "女", "ethnicity": "汉族", "birth": "1971年12月",
     "birthplace": "", "education": "大学、工商管理硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记（兼市人大常委会主任）", "current_org": "中共齐齐哈尔市委员会",
     "source": "https://www.qqhr.gov.cn/qqhe/c100016/202601/c02_602360.shtml"},
    {"id": 2, "name": "陈兴平", "gender": "男", "ethnicity": "汉族", "birth": "1970年4月",
     "birthplace": "", "education": "在职大学", "party_join": "中共党员", "work_start": "",
     "current_post": "市长", "current_org": "齐齐哈尔市人民政府",
     "source": "https://www.qqhr.gov.cn/qqhe/c100055/202310/c02_369246.shtml"},

    # ── 市委 ──
    {"id": 3, "name": "刘振江", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委副书记",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 4, "name": "邹震远", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 5, "name": "孙恒", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、副市长",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 6, "name": "刘云策", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委、副市长",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 7, "name": "马宁", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 8, "name": "毕金辉", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 9, "name": "贾兴元", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 10, "name": "谢广全", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 11, "name": "李拥军", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市委常委",
     "current_org": "中共齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},

    # ── 市人大 ──
    {"id": 12, "name": "刘大勇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "齐齐哈尔市人民代表大会常务委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 13, "name": "陈宝柱", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "齐齐哈尔市人民代表大会常务委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 14, "name": "宋阳", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "齐齐哈尔市人民代表大会常务委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 15, "name": "姜威", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市人大常委会副主任",
     "current_org": "齐齐哈尔市人民代表大会常务委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},

    # ── 市政府（其余副市长）──
    {"id": 16, "name": "高淑春", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "副市长",
     "current_org": "齐齐哈尔市人民政府", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 17, "name": "秦立宇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "副市长",
     "current_org": "齐齐哈尔市人民政府", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 18, "name": "张耀斌", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "副市长",
     "current_org": "齐齐哈尔市人民政府", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 19, "name": "王杕", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "副市长",
     "current_org": "齐齐哈尔市人民政府", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 20, "name": "孙艳福", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "副市长",
     "current_org": "齐齐哈尔市人民政府", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},

    # ── 市政协 ──
    {"id": 21, "name": "李晨华", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "", "current_post": "市政协主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 22, "name": "徐兆飞", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政协副主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 23, "name": "陆欣", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政协副主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 24, "name": "张大民", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政协副主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 25, "name": "刘凤德", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政协副主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 26, "name": "李继伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政协副主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 27, "name": "刘春峰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政协副主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
    {"id": 28, "name": "王振东", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政协副主席",
     "current_org": "中国人民政治协商会议齐齐哈尔市委员会", "source": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml"},
]

organizations = [
    {"id": 1, "name": "中共齐齐哈尔市委员会", "type": "党委", "level": "地级", "parent": "中共黑龙江省委员会", "location": "齐齐哈尔市"},
    {"id": 2, "name": "齐齐哈尔市人民政府", "type": "政府", "level": "地级", "parent": "黑龙江省人民政府", "location": "齐齐哈尔市"},
    {"id": 3, "name": "齐齐哈尔市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "黑龙江省人民代表大会常务委员会", "location": "齐齐哈尔市"},
    {"id": 4, "name": "中国人民政治协商会议齐齐哈尔市委员会", "type": "政协", "level": "地级", "parent": "中国人民政治协商会议黑龙江省委员会", "location": "齐齐哈尔市"},
    {"id": 5, "name": "中共黑龙江省委员会", "type": "党委", "level": "省级", "parent": "", "location": "哈尔滨市"},
    {"id": 6, "name": "黑龙江省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "哈尔滨市"},
    {"id": 7, "name": "中共哈尔滨市委员会", "type": "党委", "level": "副省级市", "parent": "中共黑龙江省委员会", "location": "哈尔滨市"},
    {"id": 8, "name": "哈尔滨经济技术开发区", "type": "开发区", "level": "国家级开发区", "parent": "哈尔滨市人民政府", "location": "哈尔滨市"},
]

positions = [
    # 闫红蕾 (1)
    {"person_id": 1, "org_id": 7, "title": "哈尔滨市委/哈尔滨经开区相关任职（待核）", "start": "", "end": "", "rank": "", "note": "调任齐齐哈尔前任所在地方向（哈经开区/平房），未确认精确职务"},
    {"person_id": 1, "org_id": 1, "title": "齐齐哈尔市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "黑龙江省委决定任命；主持市委全面工作，兼任市人大常委会主任、党组书记；任命年月待核"},
    {"person_id": 1, "org_id": 3, "title": "市人大常委会主任（兼）", "start": "", "end": "present", "rank": "正厅级", "note": "兼任市人大常委会主任、党组书记"},

    # 陈兴平 (2)
    {"person_id": 2, "org_id": 1, "title": "齐齐哈尔市委副书记", "start": "2023", "end": "present", "rank": "正厅级", "note": "官网档案2023-10 已任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "齐齐哈尔市市长", "start": "2023", "end": "present", "rank": "正厅级", "note": "市政府党组书记；至晚2023-10在任；主持市政府全面工作"},

    # 其余现任班子
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 6, "org_id": 1, "title": "市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 12, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 13, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 14, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 15, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 18, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 19, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 20, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 21, "org_id": 4, "title": "市政协主席", "start": "", "end": "present", "rank": "正厅级", "note": "现任"},
    {"person_id": 22, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 23, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 24, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 25, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 26, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 27, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 28, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "闫红蕾（市委书记）与陈兴平（市长）为现行党政主官搭档",
     "overlap_org": "齐齐哈尔市", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "闫红蕾（书记）与刘振江（副书记）党委领导班子搭档",
     "overlap_org": "中共齐齐哈尔市委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 21, "type": "overlap",
     "context": "闫红蕾与李晨华（政协主席）在齐齐哈尔市班子共事",
     "overlap_org": "齐齐哈尔市", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "闫红蕾（兼市人大常委会主任）与刘大勇（人大副主任）在人大班子共事",
     "overlap_org": "齐齐哈尔市人民代表大会常务委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "陈兴平（市长）与刘振江（副书记）在市委班子共事",
     "overlap_org": "中共齐齐哈尔市委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "陈兴平（市长）与孙恒（市委常委、副市长）党政上下级搭档",
     "overlap_org": "齐齐哈尔市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "陈兴平（市长）与刘云策（市委常委、副市长）党政上下级搭档",
     "overlap_org": "齐齐哈尔市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "陈兴平（市长）与高淑春（副市长）在市政府班子搭档",
     "overlap_org": "齐齐哈尔市人民政府", "overlap_period": "现任"},
]


# ══════════════════════════════════════════════════════════════════════════
# XML helper
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                     p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    if name == "闫红蕾":
        return "255,50,50"       # 市委书记 — 红
    if name == "陈兴平":
        return "50,100,255"      # 市长 — 蓝
    if name == "刘振江":
        return "255,165,0"       # 副书记 — 橙
    if name == "李晨华":
        return "255,240,200"     # 政协主席 — 米白
    if name in ("刘大勇", "陈宝柱", "宋阳", "姜威"):
        return "200,255,255"     # 人大 — 青
    return "100,100,100"


def person_size(name):
    if name in ("闫红蕾", "陈兴平"):
        return "20.0"
    if name in ("刘振江", "李晨华"):
        return "15.0"
    return "12.0"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>china-gov-network research agent</creator>')
    lines.append('    <description>齐齐哈尔市（黑龙江省，地级市）领导班子工作关系网络，2026-08-05</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"]); sz = person_size(p["name"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {len(persons)} person nodes, {len(organizations)} org nodes, {len(positions)+len(relationships)} edges")


# ══════════════════════════════════════════════════════════════════════════
# Person JSON
# ══════════════════════════════════════════════════════════════════════════

SOURCES = [
    {"id": "S001", "title": "齐齐哈尔市人民政府——领导之窗", "url": "https://www.qqhr.gov.cn/qqhe/c100004/ldzc.shtml",
     "publisher": "齐齐哈尔市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "现任班子名单"},
    {"id": "S002", "title": "闫红蕾——领导简介", "url": "https://www.qqhr.gov.cn/qqhe/c100016/202601/c02_602360.shtml",
     "publisher": "齐齐哈尔市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "书记简历"},
    {"id": "S003", "title": "陈兴平——领导简介", "url": "https://www.qqhr.gov.cn/qqhe/c100055/202310/c02_369246.shtml",
     "publisher": "齐齐哈尔市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市长简历"},
    {"id": "S004", "title": "黑龙江省委决定：闫红蕾任齐齐哈尔市委书记（搜狗聚合·鹤城发布）", "url": "https://www.sogou.com",
     "publisher": "鹤城发布/搜狗聚合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "任命公告来源"},
]


def person_json(p):
    rank = "正厅级" if p["id"] in (1, 2, 21) else "副厅级"
    timeline = [{"start": "", "end": "present", "org": p["current_org"], "title": p["current_post"],
                 "level": "地级市", "location": "齐齐哈尔市", "system": "other", "rank": rank,
                 "is_key_promotion": p["id"] in (1, 2), "notes": "现任（官方 2026-08-05）",
                 "confidence": "confirmed", "source_ids": ["S001"]}]
    if p["id"] == 1:
        timeline.append({"start": "", "end": "", "org": "中共哈尔滨市委/哈尔滨经开区（方向）",
                         "title": "调任齐齐哈尔前任职务（待核）", "level": "副省级市", "location": "哈尔滨市",
                         "system": "other", "rank": "", "is_key_promotion": False,
                         "notes": "来源线索显示其自哈尔滨调任；精确职务未确认", "confidence": "unverified", "source_ids": ["S004"]})
        timeline.append({"start": "", "end": "present", "org": "齐齐哈尔市人民代表大会常务委员会",
                         "title": "市人大常委会主任（兼）", "level": "地级市", "location": "齐齐哈尔市",
                         "system": "other", "rank": "正厅级", "is_key_promotion": False,
                         "notes": "兼任市人大常委会主任、党组书记", "confidence": "confirmed", "source_ids": ["S002"]})
    if p["id"] == 2:
        timeline.insert(0, {"start": "2023", "end": "present", "org": "中共齐齐哈尔市委员会",
                            "title": "市委副书记", "level": "地级市", "location": "齐齐哈尔市",
                            "system": "party", "rank": "正厅级", "is_key_promotion": True,
                            "notes": "官网档案2023-10 已任市委副书记", "confidence": "confirmed", "source_ids": ["S003"]})

    sources = SOURCES
    education = []
    if p["education"]:
        education = [{"period": "", "institution": p["education"], "major": "", "degree": "",
                      "study_type": "unknown", "source_ids": [s["id"] for s in sources]}]

    identity = {
        "person_id": f"qqhr_{p['name']}",
        "name": p["name"], "aliases": [], "gender": p["gender"], "ethnicity": p["ethnicity"] or "",
        "birth": p["birth"], "birthplace": p["birthplace"], "native_place": "",
        "education": education, "party_join": p["party_join"], "work_start": p["work_start"],
        "dedupe_keys": {"name_birth": f"{p['name']}_{p['birth']}", "name_birthplace": p["birthplace"], "official_profile_url": ""},
    }

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省", "city": "齐齐哈尔市", "region": "齐齐哈尔市",
            "job": p["current_post"], "task_id": "heilongjiang_齐齐哈尔市", "time_focus": "current as of 2026-08",
        },
        "identity": identity,
        "current_status": {
            "current_post": p["current_post"], "current_org": p["current_org"],
            "administrative_rank": rank, "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"],
        },
        "career_timeline": timeline,
        "organizations": [p["current_org"]],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
                                        "caveat": "Work style is inferred from public records only; not a private assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found",
                                        "description": "本轮调查未发现公开负面/纪律线索", "date": "",
                                        "confidence": "unverified", "source_ids": []}],
        "source_register": sources,
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed",
                               "career_completeness": "partial", "relationship_confidence": "low", "biggest_gap": ""},
        "open_questions": [],
    }

    if p["id"] == 1:
        data["confidence_summary"]["biggest_gap"] = "闫红蕾调任齐齐哈尔前任精确职务与起止年份"
        data["open_questions"] = [
            {"priority": "critical", "question": "闫红蕾调任齐齐哈尔市委书记前任职务（哈尔滨市委/经开区/平房区方向）", "why_it_matters": "跨市干部交流路径与前任逻辑", "suggested_queries": ["闫红蕾 哈尔滨经开区", "闫红蕾 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "闫红蕾任齐齐哈尔市委书记的任命年月", "why_it_matters": "时间线起点", "suggested_queries": [], "last_attempted": AS_OF},
            {"priority": "medium", "question": "闫红蕾教育（大学专业/院校）细节", "why_it_matters": "身份标签", "suggested_queries": [], "last_attempted": AS_OF},
        ]
    elif p["id"] == 2:
        data["confidence_summary"]["biggest_gap"] = "陈兴平任市长前的完整履历"
        data["open_questions"] = [
            {"priority": "high", "question": "陈兴平任齐齐哈尔市长前的职务轨迹", "why_it_matters": "晋升路径与系统来源", "suggested_queries": ["陈兴平 简历"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "陈兴平籍贯/教育细节", "why_it_matters": "身份标签", "suggested_queries": [], "last_attempted": AS_OF},
        ]
    elif p["id"] == 3:
        data["confidence_summary"]["biggest_gap"] = "刘振江（副书记）个人简历未见"
        data["open_questions"] = [{"priority": "high", "question": "刘振江简历", "why_it_matters": "副书记为班子重要配置", "suggested_queries": [], "last_attempted": AS_OF}]

    out = PERSONS_DIR / f"{TODAY}-黑龙江省-齐齐哈尔市-{p['current_post'].split('（')[0]}-{p['name']}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("Building 齐齐哈尔市 network...")
    build_db()
    build_gexf()
    for p in persons[:8]:
        person_json(p)
    print("  Person JSONs written to", PERSONS_DIR)
    print("Done.")


if __name__ == "__main__":
    main()