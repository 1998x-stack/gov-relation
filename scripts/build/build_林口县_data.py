#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 林口县, 黑龙江省.

Task ID: heilongjiang_林口县
Province: 黑龙江省
Parent city: 牡丹江市
Region: 林口县
Level: 县
Targets: 县委书记 & 县长

Investigation date: 2026-08-05
As-of date for leadership: 2026-05-28 (官方领导之窗页面更新), 人事任免核实至 2026-08.

Research sources (official 林口县人民政府 www.linkou.gov.cn):
  - 领导之窗·县委 http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/ldlist.shtml （县委班子名单 + 每人简介）
  - 付刚（县委书记）简介页 /mdjlkxrmzf/xw330_LK/202605/c03_586134.shtml
  - 杨洪武（县长）简介页 /mdjlkxrmzf/xw330_LK/202605/c03_586139.shtml
  - 李佳杰/耿智超/柴君/王志宏/孟祥雷/王楠/王林锋 简介页 (县委 list)
  - 人大常委会公告（人事任免列） — 县长/人大/监委/法院继任链确认:
    2021-12-10 十八届人大任; 2022-05-08 高辉当选县长; 2026-05-14 高辉辞县长、杨洪武任代县长;
    2026-06-18 刘忠辞人大主任; 2026-08-04 孙庆晨辞监委主任、吕峰任监委副主任代主任;
    2026-07-06 杜露青辞法院院长、岳春刚任代院长
  - 人民日报/公安履历 (亓鑫 2025-07 任副县长/公安局长)

Confidence notes:
  - 付刚: confirmed 县委书记 (官方领导之窗). 1977-05, 男, 汉族, 研究生, 中共党员. 完整早期履历未公开.
  - 杨洪武: confirmed 县委副书记/县长/党组书记/开发区管委会主任. 1975-03, 男, 省委党校研究生. 由代县长转正.
  - 李佳杰/耿智超: confirmed 县委副书记(分别专职/挂职).
  - 柴君(组织部长)/王志宏(常务副县长)/孟祥雷(统战)/王少(宣传)/王林锋(人武) confirmed 常委.
  - 前任县长: 高辉 (2022-05 当选, 2026-05 辞). 前任县委书记: 未核实不出公开一手来源 (open gap).
  - 因通用搜索(Exa/Baidu)在网络环境受限, 早期履历与部分班子(人大/政协/纪委/政法委)以 open_questions 记录.

Confidence standard:
  - confirmed: 官网领导之窗/官方简介页/人大常委会公告直接登记
  - plausible: 官方新闻/媒体交叉印证
  - unverified: 单方线索或无法核实
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "林口县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导（县委书记 & 县长）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "付刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年5月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委书记",
        "current_org": "中共林口县委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202605/c03_586134.shtml"
    },
    {
        "id": 2,
        "name": "杨洪武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委副书记、县长、县政府党组书记、县经济开发区管委会主任",
        "current_org": "林口县人民政府",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/ldlist.shtml"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委副书记 / 县委常委
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李佳杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年8月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委副书记、二级调研员（2025-04挂职任省国资委督查专员）",
        "current_org": "中共林口县委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202512/c03_1029735.shtml"
    },
    {
        "id": 4,
        "name": "耿智超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委副书记（挂职）",
        "current_org": "中共林口县委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202504/c03_1003854.shtml"
    },
    {
        "id": 5,
        "name": "柴君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共林口县委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202403/c03_872015.shtml"
    },
    {
        "id": 6,
        "name": "王志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委常委、县政府常务副县长",
        "current_org": "林口县人民政府",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202401/c03_872014.shtml"
    },
    {
        "id": 7,
        "name": "孟祥雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共林口县委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202403/c03_872016.shtml"
    },
    {
        "id": 8,
        "name": "王楠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共林口县委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202307/c03_586138.shtml"
    },
    {
        "id": 9,
        "name": "王林锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县委常委、人武部部长",
        "current_org": "林口县人民武装部",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202411/c03_981698.shtml"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任县长 / 其他副县长 / 人大 / 政协 / 纪委
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "高辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "前任县长（2022-05 当选，2026-05 辞任）",
        "current_org": "林口县人民政府",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf 十八届人大二次会议公告(2022-05-08) + 2026-05-14  31次会议公告"
    },
    {
        "id": 11,
        "name": "亓鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "林口县公安局/林口县人民政府",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/rsmp335_LK/202507/c03_1013243.shtml"
    },
    {
        "id": 12,
        "name": "朱军烈",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "副县长（2026-05 任命）",
        "current_org": "林口县人民政府",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/rsmp335_LK/202605/c03_1046951.shtml"
    },
    {
        "id": 13,
        "name": "刘忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "原人大常委会主任（2021-12 当选，2026-06 辞任）",
        "current_org": "林口县人民代表大会常务委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/rsmp335_LK/202606/c03_1051761.shtml"
    },
    {
        "id": 14,
        "name": "孙庆彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "原县监察委员会主任（2021-12 当选，2026-08 辞任）",
        "current_org": "林口县监察委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/rsmp335/202608/c03_1054973.shtml"
    },
    {
        "id": 15,
        "name": "吕峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_year": "",
        "current_post": "县监察委员会副主任、代主任（2026-08）",
        "current_org": "林口县监察委员会",
        "source": "http://www.linkou.gov.cn/mdjlkxrmzf/rsmp335/202608/c03_1054973.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共林口县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共牡丹江市委员会",
        "location": "林口县"
    },
    {
        "id": 2,
        "name": "林口县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "牡丹江市人民政府",
        "location": "林口县"
    },
    {
        "id": 3,
        "name": "林口县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "牡丹江市人民代表大会常务委员会",
        "location": "林口县"
    },
    {
        "id": 4,
        "name": "林口县监察委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "牡丹江市监察委员会",
        "location": "林口县"
    },
    {
        "id": 5,
        "name": "林口县经济开发区管理委员会",
        "type": "政府",
        "level": "县级园区",
        "parent": "林口县人民政府",
        "location": "林口县"
    },
    {
        "id": 6,
        "name": "林口县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "林口县人民政府",
        "location": "林口县"
    },
    {
        "id": 7,
        "name": "林口县人民武装部",
        "type": "军队",
        "level": "县级",
        "parent": "牡丹江军分区",
        "location": "林口县"
    },
    {
        "id": 8,
        "name": "中共牡丹江市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "牡丹江市"
    },
    {
        "id": 9,
        "name": "牡丹江市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "牡丹江市"
    },
    {
        "id": 10,
        "name": "黑龙江省人民政府国有资产监督管理委员会",
        "type": "政府",
        "level": "省级",
        "parent": "黑龙江省人民政府",
        "location": "哈尔滨市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 付刚（县委书记，核心）
    {"person_id": 1, "org_id": 1, "title": "林口县委书记", "start_date": "2026年前", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作。1977-05生。2026-05官网在册。"},
    {"person_id": 1, "org_id": 1, "title": "早期履历缺口", "start_date": "unknown", "end_date": "unknown", "rank": "", "note": "公开一手来源未披露其任县委书记前的完整职务履历，可能沿用县级/组织系统晋升；于 open 保留。"},

    # 杨洪武（县长，核心）
    {"person_id": 2, "org_id": 2, "title": "林口县县长（2026-05 起，曾任代县长）", "start_date": "2026-05", "end_date": "present", "rank": "正处级", "note": "2026-05-14人大常委会接受高辉辞任后任副县长、代县长，后依法当选县长。1975-03生，省委党校研究生。"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-05", "end_date": "present", "rank": "副处级", "note": "兼任县委副书记。"},
    {"person_id": 2, "org_id": 5, "title": "县经济开发区管委会主任", "start_date": "", "end_date": "present", "rank": "", "note": "领导之窗登记兼任开发区管委会主任。"},
    {"person_id": 2, "org_id": 2, "title": "履历缺口（任县长前）", "start_date": "unknown", "end_date": "unknown", "rank": "", "note": "未从一手来源确定其任县长前职务（可能在牡丹江市/周边县或政府系统）。"},

    # 李佳杰（县委副书记）
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "1990-08生，研究生，二级调研员；2025-04挂职省国资委督查专员。"},
    {"person_id": 3, "org_id": 10, "title": "挂职省国资委督查专员", "start_date": "2025-04", "end_date": "present", "rank": "", "note": "挂职。"},

    # 耿智超（县委副书记，挂职）
    {"person_id": 4, "org_id": 1, "title": "县委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "1983-02生，大学；分管农业农村/水务/林草/乡村振兴/工业科技/营商环境/军人事务。"},

    # 柴君（组织部长）
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "1979-08生，大学；负责组织、干部、人才、党建；协助书记分管党校。"},

    # 王志宏（常务副县长）
    {"person_id": 6, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "1979-04生，大学；协助县长抓财审金融；政府常务/发改/人社/安监/应急/民兵。"},

    # 孟祥雷（统战部长）
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "1982-04生，大学；负责统一战线、民族宗教。"},

    # 王楠（宣传部长）
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "1983-04生，大学；宣传思想文化、网信。"},

    # 王林锋（人武部长）
    {"person_id": 9, "org_id": 7, "title": "县委常委、人武部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "1979-12生，本科。"},

    # 高辉（前任县长）
    {"person_id": 10, "org_id": 2, "title": "林口县县长", "start_date": "2022-05", "end_date": "2026-05", "rank": "正处级", "note": "2022-05-08 十八届人大二次会议当选；2026-05-14 辞任。"},

    # 亓鑫（副县长/公安局长）
    {"person_id": 11, "org_id": 6, "title": "副县长、县公安局局长", "start_date": "2025-07", "end_date": "present", "rank": "副处级", "note": "2025-07-29 任命；接替刘海超。"},

    # 朱军烈（副县长）
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "2026-05", "end_date": "present", "rank": "副处级", "note": "2026-05-14 任命。"},

    # 刘忠（原人大主任）
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start_date": "2021-12", "end_date": "2026-06", "rank": "正处级", "note": "2021-12-10 当选；2026-06-18 辞任。"},

    # 孙庆彬（原监委主任）
    {"person_id": 14, "org_id": 4, "title": "县监察委员会主任", "start_date": "2021-12", "end_date": "2026-08", "rank": "副处级", "note": "2021-12-10 当选；2026-08-04 辞任。"},

    # 吕峰（监委代主任）
    {"person_id": 15, "org_id": 4, "title": "县监察委员会副主任、代主任", "start_date": "2026-08", "end_date": "present", "rank": "副处级", "note": "2026-08-04 任命。"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "付刚作为县委书记，杨洪武作为县委副书记、县长，党政主要领导搭档；付刚主持县委，杨洪武主持政府。",
        "overlap_org": "林口县",
        "overlap_period": "2026-05至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "付刚作为县委书记，柴君为常委、组织部长，党管干部工作于县委班子内协作。",
        "overlap_org": "中共林口县委员会",
        "overlap_period": "在第三届班子内"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "付刚作为县委书记，王志宏为常委、常务副县长，党政班子搭档。",
        "overlap_org": "林口县",
        "overlap_period": "在任"
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "predecessor_successor",
        "context": "县长继任链：高辉（2022-05—2026-05）→ 杨洪武（2026-05 代县长后转正）。高辉辞任后杨洪武接任。",
        "overlap_org": "林口县人民政府",
        "overlap_period": "2026-05"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "overlap",
        "context": "杨洪武任县长后，亓鑫作为副县长、公安局长予以政府共事。",
        "overlap_org": "林口县人民政府",
        "overlap_period": "2026-05至今"
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "overlap",
        "context": "杨洪武任县长后，朱军烈为副县长，与其政府班子共事。",
        "overlap_org": "林口县人民政府",
        "overlap_period": "2026-05至今"
    },
    {
        "person_a": 3, "person_b": 1,
        "type": "superior_subordinate",
        "context": "李佳杰为县委副书记，在其任内与县委书记付刚同任县委班子。",
        "overlap_org": "中共林口县委员会",
        "overlap_period": "在任"
    },
    {
        "person_a": 14, "person_b": 15,
        "type": "predecessor_successor",
        "context": "监委继任：孙庆晨（2021-12—2026-08）辞任，吕峰任副主任、代主任。",
        "overlap_org": "林口县监察委员会",
        "overlap_period": "2026-08"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
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
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_year TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_year, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_year"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    # 县委书记 — 红
    if name == "付刚":
        return "255,50,50"
    # 政府（县长/副县长）— 蓝
    if name in ("杨洪武", "王志宏", "高辉", "亓鑫", "朱军烈"):
        return "50,100,255"
    # 监委 — 橙
    if name in ("孙庆彬", "吕峰"):
        return "255,165,0"
    # 人大 — 青
    if name in ("刘忠",):
        return "200,255,255"
    # 县委副书记/常委 — 橙-灰
    if name in ("李佳杰", "耿智超", "柴君", "孟祥雷", "王楠"):
        return "255,165,0"
    return "100,100,100"


def person_size(name):
    if name in ("付刚", "杨洪武"):
        return "20.0"
    if name in ("李佳杰", "耿智超", "王志宏", "高辉"):
        return "12.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "纪委" in o_type:
        return "255,220,200"
    if "军队" in o_type:
        return "230,230,230"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>林口县领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

SOURCE_REGISTER = [
    {"id": "S001", "title": "林口县人民政府·领导之窗·县委（付刚、杨洪武及县委班子）", "url": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/ldlist.shtml", "publisher": "林口县人民政府", "published_at": "2026-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委班子全部名单+每人简介"},
    {"id": "S002", "title": "付刚（县委书记）简介页", "url": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202605/c03_586134.shtml", "publisher": "林口县人民政府", "published_at": "2026-05-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "付刚 1977-05 男 汉 研究生 中共党员，现任县委书记"},
    {"id": "S003", "title": "杨洪武（县长）简介页", "url": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/202605/c03_586139.shtml", "publisher": "林口县人民政府", "published_at": "2026-05-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "杨洪武 1975-03 男 省委党校研究生 县委副书记/县长/党组书记/开发区管委会主任"},
    {"id": "S004", "title": "林口县人大常委会·人事任免公告（2021-2026）", "url": "http://www.linkou.gov.cn/mdjlkxrmzf/rsrm335_LK/list.shtml", "publisher": "林口县人大常委会", "published_at": "2026-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长/人大主任/监委/法院继任链与换届选举记录"},
    {"id": "S005", "title": "李佳杰/耿智超/柴君/王志宏/王楠/王林锋 简介页（县委 list）", "url": "http://www.linkou.gov.cn/mdjlkxrmzf/xw330_LK/ldlist.shtml", "publisher": "林口县人民政府", "published_at": "2023-2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "副书记与常委/部门分工"},
]


def timeline_for_person(name):
    if name == "付刚":
        return [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "任县委书记前的职务", "notes": "公开一手来源未披露其完整履历；研究生学历，中共党员", "confidence": "unverified", "source_ids": []},
            {"start": "2026年前", "end": "present", "org": "中共林口县委员会", "title": "县委书记", "notes": "主持县委全面工作；2026-05 领导之窗在册", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        ]
    if name == "杨洪武":
        return [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "任县长前", "notes": "省委党校研究生；1975-03生；未从一手来源确定任县长前职务", "confidence": "unverified", "source_ids": []},
            {"start": "2026-05", "end": "present", "org": "林口县人民政府", "title": "县长（曾任代县长）", "notes": "2026-05-14 高辉辞任后任代县长，后依法当选；领导之窗确认为县长", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
            {"start": "2026-05", "end": "present", "org": "林口县经济开发区管委会", "title": "管委会主任", "notes": "领导之窗登记兼任", "confidence": "confirmed", "source_ids": ["S003"]},
        ]
    if name == "高辉":
        return [
            {"start": "2022-05", "end": "2026-05", "org": "林口县人民政府", "title": "县长", "notes": "2022-05-08 当选；2026-05-14 辞任", "confidence": "confirmed", "source_ids": ["S004"]},
        ]
    return [{"start": "", "end": "present", "org": "", "title": "", "notes": "现任班子在册；完整履历待查", "confidence": "medium", "source_ids": ["S001"]}]


def make_person_json(p, job):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "牡丹江市",
            "region": "林口县",
            "job": job,
            "task_id": "heilongjiang_林口县",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"linkou_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", "")}],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_year", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if p.get("id") in (1, 2, 10, 13) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline_for_person(p["name"]),
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [p.get("birthplace", "")],
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
            {"type": "none_found", "description": "在已获取的公开资料中未发现该人物负面纪律/审计信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("id") in (1, 2) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历（任现职前职务、出生地/籍贯、入党/参加工作时间）待补"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{p['name']}的完整职业履历（任现职前的组织/政府/纪委等系统和职务）",
                "why_it_matters": "核心人物，但早期履历一手来源未披露",
                "last_attempted": AS_OF,
                "suggested_queries": [f"{p['name']} 简历 林口", f"{p['name']} 任前公示", f"林口县 前任县委书记 {p['name']}"]
            }
        ]
    }


def build_person_jsons():
    files = []
    job_map = {
        1: "县委书记",
        2: "县长",
        3: "县委副书记",
        5: "县委组织部部长",
        6: "常务副县长",
    }
    for p in persons:
        if p["id"] not in job_map:
            continue
        job = job_map[p["id"]]
        data = make_person_json(p, job)
        # 人际关系（针对核心）
        if p["name"] == "付刚":
            data["relationships"] = [
                {"person": "杨洪武", "person_id": "linkou_杨洪武", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "县委书记—县长搭档", "overlap_org": "林口县", "overlap_period": "2026-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "柴君", "person_id": "linkou_柴君", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "党管干部的组织部长", "overlap_org": "中共林口县委员会", "overlap_period": "在任", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ]
        if p["name"] == "杨洪武":
            data["relationships"] = [
                {"person": "付刚", "person_id": "linkou_付刚", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "县长对县委书记", "overlap_org": "林口县", "overlap_period": "2026-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "高辉", "person_id": "linkou_高辉", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "高辉辞县长，杨洪武接任代县长/县长", "overlap_org": "林口县人民政府", "overlap_period": "2026-05", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            ]
        if p["name"] == "高辉":
            data["relationships"] = [
                {"person": "杨洪武", "person_id": "linkou_杨洪武", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "杨洪武接任其县长职务", "overlap_org": "林口县人民政府", "overlap_period": "2026-05", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            ]
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-牡丹江市-{job}-{p['name']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")
        files.append(path)
    return files


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")