#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Guixi City (贵溪市) leadership network.

贵溪市 is a county-level city under Yingtan City (鹰潭市), Jiangxi Province.
It is a major economic hub due to Jiangxi Copper (江铜集团) headquarters.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/贵溪市_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/贵溪市_network.gexf")
STAGING_DB = os.path.join(BASE, "data/tmp/jiangxi_贵溪市/贵溪市_network.db")
STAGING_GEXF = os.path.join(BASE, "data/tmp/jiangxi_贵溪市/贵溪市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (市委书记) ──
    {"id": 1, "name": "曾宝柱", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委书记、市人武部党委第一书记", "current_org": "中共贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/9/art_6225_1601287.html",
     "note": "2026年7月新任, 接替陈敏(曾兼任)"},

    # ── Mayor (市长) ──
    {"id": 2, "name": "潘磊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委副书记、市长", "current_org": "贵溪市人民政府",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html",
     "note": "主持市政府全面工作"},

    # ── Deputy Party Secretary (市委副书记) ──
    {"id": 3, "name": "黄建军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委副书记", "current_org": "中共贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html",
     "note": "协助书记抓党建"},

    # ── Executive Vice Mayor (常务副市长) ──
    {"id": 4, "name": "张相生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委、常务副市长", "current_org": "贵溪市人民政府",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html",
     "note": "负责市政府常务工作"},

    # ── Political & Legal Affairs Secretary (政法委书记) ──
    {"id": 5, "name": "乐雪飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委、政法委书记", "current_org": "中共贵溪市委政法委员会",
     "source": "http://www.guixi.gov.cn/art/2026/5/16/art_6225_1590079.html",
     "note": "分管政法、综治、扫黑除恶"},

    # ── Standing Committee members (市委常委) ──
    {"id": 6, "name": "冷颖峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委", "current_org": "中共贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html"},

    {"id": 7, "name": "张秀娥", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委", "current_org": "中共贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html"},

    {"id": 8, "name": "宋春水", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委、市人武部上校政委", "current_org": "贵溪市人民武装部",
     "source": "http://www.guixi.gov.cn/art/2026/7/9/art_6225_1601287.html"},

    {"id": 9, "name": "熊远先", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委", "current_org": "中共贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html",
     "note": "分管高标准农田建设"},

    {"id": 10, "name": "刘峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委", "current_org": "中共贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html"},

    {"id": 11, "name": "李海东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市委常委", "current_org": "中共贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html"},

    # ── Vice Mayors (副市长) ──
    {"id": 12, "name": "王建生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市副市长", "current_org": "贵溪市人民政府",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html"},

    {"id": 13, "name": "张世洪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市副市长", "current_org": "贵溪市人民政府",
     "source": "http://www.guixi.gov.cn/art/2026/5/16/art_6225_1590079.html",
     "note": "分管安全生产"},

    # ── NPC Standing Committee Director (人大常委会主任) ──
    {"id": 14, "name": "王华光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市人大常委会主任", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html"},

    # ── CPPCC Chairman (政协主席) ──
    {"id": 15, "name": "侯剑锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵溪市政协主席", "current_org": "政协贵溪市委员会",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html"},

    # ── Predecessors ──
    {"id": 16, "name": "陈敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市政府副市长（原兼任贵溪市委书记）", "current_org": "鹰潭市人民政府",
     "source": "http://www.guixi.gov.cn/art/2026/7/2/art_6225_1599513.html",
     "note": "此前兼任贵溪市委书记, 2026年7月不再兼任, 由曾宝柱接任"},

    # ── Other notable figures from official reports ──
    {"id": 17, "name": "郑国华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人武部上校部长", "current_org": "贵溪市人民武装部",
     "source": "http://www.guixi.gov.cn/art/2026/7/9/art_6225_1601287.html"},

    {"id": 18, "name": "徐志锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人大常委会党组成员", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html"},

    # NPC Standing Committee副主任
    {"id": 19, "name": "许由华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人大常委会副主任", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html"},

    {"id": 20, "name": "吕剑林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人大常委会副主任", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html"},

    {"id": 21, "name": "钱忠贤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人大常委会副主任", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html"},

    {"id": 22, "name": "程蕾", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人大常委会副主任", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html"},

    {"id": 23, "name": "彭先荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人大常委会副主任", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html"},

    {"id": 24, "name": "项国华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市人大常委会党组成员", "current_org": "贵溪市人大常委会",
     "source": "http://www.guixi.gov.cn/art/2026/7/1/art_6225_1599505.html"},

    # Others mentioned in 扫黑除恶 meeting
    {"id": 25, "name": "张海燕", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市（职务待确认）", "current_org": "",
     "source": "http://www.guixi.gov.cn/art/2026/5/16/art_6225_1590079.html"},

    {"id": 26, "name": "魏鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市（职务待确认）", "current_org": "",
     "source": "http://www.guixi.gov.cn/art/2026/5/16/art_6225_1590079.html"},

    {"id": 27, "name": "梁波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市（职务待确认）", "current_org": "",
     "source": "http://www.guixi.gov.cn/art/2026/5/16/art_6225_1590079.html"},

    {"id": 28, "name": "葛星亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵溪市（职务待确认）", "current_org": "",
     "source": "http://www.guixi.gov.cn/art/2026/5/16/art_6225_1590079.html"},

    # ── Cross-reference: 蔡江 from 鹰潭——贵溪籍 ──
    {"id": 29, "name": "蔡江", "gender": "女", "ethnicity": "汉族",
     "birth": "1968-03", "birthplace": "江西贵溪", "education": "省委党校研究生",
     "party_join": "1994-07", "work_start": "1989-08",
     "current_post": "鹰潭市委常委、统战部部长", "current_org": "中共鹰潭市委统战部",
     "source": "https://www.163.com/dy/article/ISJ2C3U90514A0A7.html",
     "note": "贵溪籍, 鹰潭市领导——贵溪籍贯的重要连接节点"},
]

# ── Organizations ──
orgs = [
    {"id": 1, "name": "中共贵溪市委员会", "type": "党委", "level": "县级市", "parent": "中共鹰潭市委员会", "location": "鹰潭市贵溪市"},
    {"id": 2, "name": "贵溪市人民政府", "type": "政府", "level": "县级市", "parent": "鹰潭市人民政府", "location": "鹰潭市贵溪市"},
    {"id": 3, "name": "中共贵溪市委政法委员会", "type": "党委", "level": "县级市", "parent": "中共贵溪市委员会", "location": "鹰潭市贵溪市"},
    {"id": 4, "name": "贵溪市人大常委会", "type": "人大", "level": "县级市", "parent": "鹰潭市人大常委会", "location": "鹰潭市贵溪市"},
    {"id": 5, "name": "政协贵溪市委员会", "type": "政协", "level": "县级市", "parent": "政协鹰潭市委员会", "location": "鹰潭市贵溪市"},
    {"id": 6, "name": "贵溪市人民武装部", "type": "事业单位", "level": "县级市", "parent": "鹰潭军分区", "location": "鹰潭市贵溪市"},
    {"id": 7, "name": "中共贵溪市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共贵溪市委员会", "location": "鹰潭市贵溪市"},
    {"id": 8, "name": "中共鹰潭市委统战部", "type": "党委", "level": "地级市", "parent": "中共鹰潭市委员会", "location": "鹰潭市"},
    {"id": 9, "name": "鹰潭市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "鹰潭市"},
    {"id": 10, "name": "中共鹰潭市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "鹰潭市"},
]

# ── Positions (person_id, org_id, title, start, end, rank, note) ──
positions = [
    # 曾宝柱
    (1, 1, "贵溪市委书记", "2026-07", "至今", "正处级", "新任"),
    (1, 6, "贵溪市人武部党委第一书记", "2026-07", "至今", "", "兼任"),

    # 潘磊
    (2, 2, "贵溪市委副书记、市长", "至今", "至今", "正处级", "主持市政府全面工作"),
    (2, 1, "贵溪市委副书记", "至今", "至今", "副处级", "兼任"),

    # 黄建军
    (3, 1, "贵溪市委副书记", "至今", "至今", "副处级", "协助书记抓党建"),

    # 张相生
    (4, 2, "贵溪市委常委、常务副市长", "至今", "至今", "副处级", "负责市政府常务工作"),
    (4, 1, "贵溪市委常委", "至今", "至今", "副处级", ""),

    # 乐雪飞
    (5, 3, "贵溪市委常委、政法委书记", "至今", "至今", "副处级", "分管政法、综治"),
    (5, 1, "贵溪市委常委", "至今", "至今", "副处级", ""),

    # 冷颖峰
    (6, 1, "贵溪市委常委", "至今", "至今", "副处级", ""),

    # 张秀娥
    (7, 1, "贵溪市委常委", "至今", "至今", "副处级", ""),

    # 宋春水
    (8, 6, "贵溪市委常委、市人武部上校政委", "至今", "至今", "副处级", ""),
    (8, 1, "贵溪市委常委", "至今", "至今", "副处级", ""),

    # 熊远先
    (9, 1, "贵溪市委常委", "至今", "至今", "副处级", "分管高标准农田建设"),

    # 刘峰
    (10, 1, "贵溪市委常委", "至今", "至今", "副处级", ""),

    # 李海东
    (11, 1, "贵溪市委常委", "至今", "至今", "副处级", ""),

    # 王建生
    (12, 2, "贵溪市副市长", "至今", "至今", "副处级", ""),

    # 张世洪
    (13, 2, "贵溪市副市长", "至今", "至今", "副处级", "分管安全生产"),

    # 王华光
    (14, 4, "贵溪市人大常委会主任", "至今", "至今", "正处级", ""),

    # 侯剑锋
    (15, 5, "贵溪市政协主席", "至今", "至今", "正处级", ""),

    # 陈敏（前任书记）
    (16, 9, "鹰潭市政府副市长", "至今", "至今", "副厅级", "仍任鹰潭市副市长"),
    (16, 1, "贵溪市委书记（兼任）", "约2024", "2026-07", "正处级", "不再兼任"),
    (16, 10, "中共鹰潭市委常委（推定）", "至今", "至今", "副厅级", ""),

    # 郑国华
    (17, 6, "贵溪市人武部上校部长", "至今", "至今", "", ""),

    # NPC相关
    (18, 4, "贵溪市人大常委会党组成员", "至今", "至今", "", ""),
    (19, 4, "贵溪市人大常委会副主任", "至今", "至今", "副处级", ""),
    (20, 4, "贵溪市人大常委会副主任", "至今", "至今", "副处级", ""),
    (21, 4, "贵溪市人大常委会副主任", "至今", "至今", "副处级", ""),
    (22, 4, "贵溪市人大常委会副主任", "至今", "至今", "副处级", ""),
    (23, 4, "贵溪市人大常委会副主任", "至今", "至今", "副处级", ""),
    (24, 4, "贵溪市人大常委会党组成员", "至今", "至今", "", ""),

    # 蔡江
    (29, 8, "鹰潭市委常委、统战部部长", "2021-09", "至今", "副厅级", "贵溪籍"),
]

# ── Relationships (person_a, person_b, type, context, overlap_org, overlap_period) ──
relationships = [
    # 核心党政搭档
    (1, 2, "党政搭档", "市委书记与市长搭档", "贵溪市", "2026-07至今"),

    # 前后任书记
    (1, 16, "前后任", "曾宝柱接替陈敏为市委书记", "中共贵溪市委员会", "2026-07"),

    # 市长与副手
    (2, 4, "上下级", "市长与常务副市长", "贵溪市人民政府", "至今"),
    (2, 3, "党政副手", "市长与市委副书记", "贵溪市", "至今"),

    # 常委间关系
    (4, 5, "常委同僚", "常务副市长与政法委书记", "中共贵溪市委员会", "至今"),
    (5, 13, "工作关系", "政法委书记与分管安全生产的副市长", "贵溪市", "至今"),

    # 人大/政协与党委
    (14, 1, "党政军—人大", "市委书记与人大常委会主任", "贵溪市", "至今"),
    (15, 1, "党政军—政协", "市委书记与政协主席", "贵溪市", "至今"),

    # 军地关系
    (1, 8, "军地搭档", "第一书记与人武部政委", "贵溪市人武部", "2026-07至今"),

    # 贵溪籍鹰潭市级领导连接
    (29, 1, "同籍贯连接", "蔡江（贵溪籍）与贵溪市委书记", "贵溪市/鹰潭市", "至今"),
    (29, 2, "同籍贯连接", "蔡江（贵溪籍）与贵溪市长", "贵溪市/鹰潭市", "至今"),
    (29, 16, "上下级", "蔡江（鹰潭市委常委）与陈敏（鹰潭市副市长）", "中共鹰潭市委员会", "至今"),

    # 陈敏与鹰潭市层面的连接
    (16, 1, "前后任/上下级", "陈敏兼贵溪书记时与曾宝柱交接", "贵溪市", "2026-07"),
    (16, 2, "上下级", "陈敏（鹰潭副市长、原贵溪书记）与潘磊（贵溪市长）", "贵溪市", "至今"),
]

# ── Helpers ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_role_color(name, post):
    """Return R,G,B color string based on role."""
    post = post or ""
    if "书记" in post and "纪委" not in post and "政法" not in post:
        return "255,50,50"
    if "市长" in post or "副市长" in post or "区长" in post:
        return "50,100,255"
    if "纪委" in post or "监委" in post:
        return "255,165,0"
    if "政协" in post:
        return "180,100,200"
    if "人大" in post:
        return "100,150,200"
    return "100,100,100"

def is_top_leader(post):
    post = post or ""
    return ("市委书记" in post or "市长" in post or "人大常委会主任" in post or "政协主席" in post) and "副" not in post

def person_size(post):
    return 20.0 if is_top_leader(post) else 12.0

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

def build_db(db_path):
    """Build SQLite database."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"],
              p["birth"], p["birthplace"], p["education"],
              p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in orgs:
        cur.execute("""
            INSERT OR REPLACE INTO organizations
            VALUES (?,?,?,?,?,?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)
        """, pos)

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)
        """, r)

    conn.commit()
    conn.close()
    print(f"✅ Database written: {db_path}")

def build_gexf(gexf_path):
    """Build GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>贵溪市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_role_color(p["name"], p.get("current_post", ""))
        sz = str(person_size(p.get("current_post", "")))
        role = esc(p.get("current_post", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_node_ids = {}
    for o in orgs:
        oid = f"o{o['id']}"
        org_node_ids[o['id']] = oid
        c = org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person → Organization (worked_at edges)
    for pos in positions:
        person_id, org_id = pos[0], pos[1]
        if org_id not in org_node_ids:
            continue
        eid += 1
        src = f"p{person_id}"
        tgt = org_node_ids[org_id]
        label = esc(pos[3])  # title
        lines.append(f'      <edge id="{eid}" source="{src}" target="{tgt}" label="{label}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{label}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship edges)
    for r in relationships:
        pa, pb, rtype, context = r[0], r[1], r[2], r[3]
        eid += 1
        src = f"p{pa}"
        tgt = f"p{pb}"
        label = esc(rtype)
        ctx = esc(context)
        weight = "2.0" if "党政搭档" in rtype or "前后任" in rtype else "1.5"
        lines.append(f'      <edge id="{eid}" source="{src}" target="{tgt}" label="{label}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{ctx}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(gexf_path), exist_ok=True)
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF written: {gexf_path}")


if __name__ == "__main__":
    import sys
    target_db = STAGING_DB
    target_gexf = STAGING_GEXF
    if "--prod" in sys.argv:
        target_db = DB_PATH
        target_gexf = GEXF_PATH
        print("⚠️  Writing to PRODUCTION paths")
    else:
        print("📦 Writing to staging paths (use --prod for production)")

    build_db(target_db)
    build_gexf(target_gexf)

    # Summary
    print(f"\n📊 Summary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(orgs)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\nFiles:")
    print(f"  DB:    {target_db}")
    print(f"  GEXF:  {target_gexf}")
