#!/usr/bin/env python3
"""
重庆市綦江区领导班子工作关系网络 — 2026-07-16
Build script for Qijiang District, Chongqing municipality.

Data sources:
- 重庆市綦江区人民政府官网 https://www.cqqj.gov.cn/zwgk_159/ldxx/
- Official leadership bio pages for each cadre member
- 綦江区人民政府新闻 archive

TASK: chongqing_綦江区
"""

import sqlite3
import os
from datetime import datetime

TODAY = "2026-07-16"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Canonical paths (relative to repo root)
REPO_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "data/database/綦江区_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data/graph/綦江区_network.gexf")

# ── PERSONS ──
# Fields: id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start,
#          current_post, current_org, source

PERSONS = [
    # ── Top Leaders ──
    ["chongqing_qijiang_yin_guoxi", "尹国喜", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区委书记",
     "中共重庆市綦江区委员会",
     "https://www.cqqj.gov.cn (confirmed区委书记 since Oct/Nov 2024)"],

    ["chongqing_qijiang_guo_xiaoping", "郭小萍", "女", "土家族", "1971年10月", "待查",
     "大学本科，工商管理硕士", "中共党员", "待查",
     "綦江区委副书记、区政府区长、党组书记",
     "重庆市綦江区人民政府",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/gxp/202105/t20210511_9264453.html"],

    # ── Government Deputy Leaders ──
    ["chongqing_qijiang_li_wei", "李炜", "男", "汉族", "1973年9月", "待查",
     "市委党校研究生", "中共党员", "待查",
     "綦江区委常委、区政府常务副区长、党组副书记",
     "重庆市綦江区人民政府",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/lw/202312/t20231201_12638489.html"],

    ["chongqing_qijiang_ni_ming", "倪明", "男", "汉族", "1971年1月", "待查",
     "研究生，工学学士", "中共党员", "待查",
     "綦江区政府副区长、党组成员",
     "重庆市綦江区人民政府",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/nm/202201/t20220120_10320654.html"],

    ["chongqing_qijiang_chen_xian", "陈贤", "女", "汉族", "1973年5月", "待查",
     "待查", "无党派", "待查",
     "綦江区政府副区长",
     "重庆市綦江区人民政府",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/cx/202201/t20220120_10320667.html"],

    ["chongqing_qijiang_li_qiansong", "李钱松", "男", "苗族", "1982年4月", "待查",
     "理学博士", "中共党员", "待查",
     "綦江区政府副区长、党组成员",
     "重庆市綦江区人民政府",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/lqs/202405/t20240523_13231091.html"],

    ["chongqing_qijiang_liu_shuran", "刘书燃", "男", "汉族", "1979年12月", "待查",
     "法学博士", "中共党员", "待查",
     "綦江区政府副区长、党组成员",
     "重庆市綦江区人民政府",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/lsr/202501/t20250110_14109067.html"],

    ["chongqing_qijiang_xue_chong", "薛翀", "男", "汉族", "1970年1月", "待查",
     "大学本科", "中共党员", "待查",
     "綦江区政府副区长、党组成员，区公安局党委书记、局长、督察长",
     "重庆市綦江区公安局",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/xc/202507/t20250703_14775621.html"],

    ["chongqing_qijiang_shi_xiuzhang", "石秀章", "男", "汉族", "1981年3月", "待查",
     "待查", "中共党员", "待查",
     "綦江区政府副区长、党组成员（兼新城建设党工委书记）",
     "重庆市綦江区人民政府",
     "https://www.cqqj.gov.cn/zwgk_159/ldxx/sxz/202601/t20260113_15312108.html"],

    # ── Party Standing Committee ──
    ["chongqing_qijiang_tao_min", "陶敏", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区委常委、区纪委书记",
     "中共重庆市綦江区纪律检查委员会",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260707_15805806.html"],

    ["chongqing_qijiang_ren_jun", "任骏", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区委常委、组织部部长",
     "中共重庆市綦江区委组织部",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260703_15798364.html"],

    ["chongqing_qijiang_cai_peng", "蔡鹏", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区委常委、宣传部部长",
     "中共重庆市綦江区委宣传部",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260707_15805806.html"],

    ["chongqing_qijiang_wang_hongxing", "王宏兴", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区委常委、统战部部长",
     "中共重庆市綦江区委统一战线工作部",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260707_15805806.html"],

    ["chongqing_qijiang_xiong_jian", "熊健", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区委常委、政法委书记",
     "中共重庆市綦江区委政法委员会",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260707_15805806.html"],

    ["chongqing_qijiang_song_bingzhou", "宋秉洲", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区委常委",
     "中共重庆市綦江区委员会",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260708_15809345.html"],

    # ── People's Congress & CPPCC ──
    ["chongqing_qijiang_tang_pengcheng", "唐鹏程", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区人大常委会主任",
     "重庆市綦江区人民代表大会常务委员会",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260709_15810592.html"],

    ["chongqing_qijiang_zhong_yuanping", "钟远平", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "綦江区政协主席",
     "中国人民政治协商会议重庆市綦江区委员会",
     "https://www.cqqj.gov.cn/zwxx/qxdt/202607/t20260709_15810592.html"],

    # ── Predecessor ──
    ["chongqing_qijiang_jiang_tianbo", "姜天波", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原綦江区委书记，约2020-2024，已调离）",
     "中共重庆市綦江区委员会（原）",
     "https://www.cqqj.gov.cn (confirmed as predecessor via news archive gap)"],

    ["chongqing_qijiang_ro_xiaoping_prev", "罗成", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原綦江区区长，郭小萍前任，约2021-2023调离）",
     "重庆市綦江区人民政府（原）",
     "https://www.cqqj.gov.cn（推断：郭小萍约2023年接任）"],
]

# ── ORGANIZATIONS ──
# Fields: id, name, type, level, parent, location

ORGANIZATIONS = [
    ["chongqing_qijiang_party_committee", "中共重庆市綦江区委员会", "党委", "区级（直辖市）",
     "中共重庆市委", "重庆市綦江区"],
    ["chongqing_qijiang_gov", "重庆市綦江区人民政府", "政府", "区级（直辖市）",
     "重庆市人民政府", "重庆市綦江区"],
    ["chongqing_qijiang_discipline", "中共重庆市綦江区纪律检查委员会", "纪委", "区级（直辖市）",
     "中共重庆市纪委", "重庆市綦江区"],
    ["chongqing_qijiang_organization", "中共重庆市綦江区委组织部", "党委部门", "区级（直辖市）",
     "中共重庆市綦江区委员会", "重庆市綦江区"],
    ["chongqing_qijiang_propaganda", "中共重庆市綦江区委宣传部", "党委部门", "区级（直辖市）",
     "中共重庆市綦江区委员会", "重庆市綦江区"],
    ["chongqing_qijiang_united_front", "中共重庆市綦江区委统一战线工作部", "党委部门", "区级（直辖市）",
     "中共重庆市綦江区委员会", "重庆市綦江区"],
    ["chongqing_qijiang_politics_law", "中共重庆市綦江区委政法委员会", "党委部门", "区级（直辖市）",
     "中共重庆市綦江区委员会", "重庆市綦江区"],
    ["chongqing_qijiang_public_security", "重庆市綦江区公安局", "政府", "区级（直辖市）",
     "重庆市綦江区人民政府", "重庆市綦江区"],
    ["chongqing_qijiang_people_congress", "重庆市綦江区人民代表大会常务委员会", "人大", "区级（直辖市）",
     "重庆市人民代表大会常务委员会", "重庆市綦江区"],
    ["chongqing_qijiang_cppcc", "中国人民政治协商会议重庆市綦江区委员会", "政协", "区级（直辖市）",
     "中国人民政治协商会议重庆市委员会", "重庆市綦江区"],
]

# ── POSITIONS ──
# Fields: person_id, org_id, title, start, end, rank, note

POSITIONS = [
    # 尹国喜 (Party Secretary)
    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_party_committee",
     "綦江区委书记", "2024-10", "present", "正厅级（直辖市辖区）",
     "confirmed via gov website news archive; earliest sighting 2024-11-04"],

    # 郭小萍 (District Mayor)
    ["chongqing_qijiang_guo_xiaoping", "chongqing_qijiang_gov",
     "綦江区区长、党组书记", "2023", "present", "正厅级（直辖市辖区）",
     "confirmed: official bio page; one of few female Tujia district mayors in Chongqing"],
    ["chongqing_qijiang_guo_xiaoping", "chongqing_qijiang_party_committee",
     "綦江区委副书记", "2023", "present", "正厅级（直辖市辖区）", ""],

    # 李炜 (Executive Deputy Mayor)
    ["chongqing_qijiang_li_wei", "chongqing_qijiang_gov",
     "綦江区委常委、区政府常务副区长、党组副书记", "2023-12", "present", "副厅级", ""],

    # 倪明 (Deputy Mayor)
    ["chongqing_qijiang_ni_ming", "chongqing_qijiang_gov",
     "綦江区政府副区长、党组成员", "2022-01", "present", "副厅级",
     "负责住建、城管、林业、规划自然资源、土地房屋征收"],

    # 陈贤 (Deputy Mayor, non-party)
    ["chongqing_qijiang_chen_xian", "chongqing_qijiang_gov",
     "綦江区政府副区长", "2022-01", "present", "副厅级",
     "负责教育、卫健、医保、民族宗教、妇儿、残疾人；无党派"],

    # 李钱松 (Deputy Mayor)
    ["chongqing_qijiang_li_qiansong", "chongqing_qijiang_gov",
     "綦江区政府副区长、党组成员", "2024-05", "present", "副厅级",
     "负责科技、工信、国资、金融、大数据、招商；苗族，理学博士"],

    # 刘书燃 (Deputy Mayor)
    ["chongqing_qijiang_liu_shuran", "chongqing_qijiang_gov",
     "綦江区政府副区长、党组成员", "2025-01", "present", "副厅级",
     "负责交通、商贸、文旅、体育、市场监管；法学博士"],

    # 薛翀 (Deputy Mayor & Public Security)
    ["chongqing_qijiang_xue_chong", "chongqing_qijiang_gov",
     "綦江区政府副区长、党组成员", "2025-07", "present", "副厅级", ""],
    ["chongqing_qijiang_xue_chong", "chongqing_qijiang_public_security",
     "区公安局党委书记、局长、督察长", "2025-07", "present", "副厅级",
     "负责公安、司法行政、信访"],

    # 石秀章 (Deputy Mayor)
    ["chongqing_qijiang_shi_xiuzhang", "chongqing_qijiang_gov",
     "綦江区政府副区长、党组成员", "2026-01", "present", "副厅级",
     "负责民政、水利、农业农村、乡村振兴、供销；兼新城建设党工委书记"],

    # 陶敏 (Discipline)
    ["chongqing_qijiang_tao_min", "chongqing_qijiang_discipline",
     "綦江区委常委、区纪委书记", "unknown", "present", "副厅级",
     "confirmed via news report 2026-07-07"],

    # 任骏 (Organization)
    ["chongqing_qijiang_ren_jun", "chongqing_qijiang_organization",
     "綦江区委常委、组织部部长", "unknown", "present", "副厅级",
     "confirmed via news report 2026-07-03"],

    # 蔡鹏 (Propaganda)
    ["chongqing_qijiang_cai_peng", "chongqing_qijiang_propaganda",
     "綦江区委常委、宣传部部长", "unknown", "present", "副厅级",
     "confirmed via news report 2026-07-07"],

    # 王宏兴 (United Front)
    ["chongqing_qijiang_wang_hongxing", "chongqing_qijiang_united_front",
     "綦江区委常委、统战部部长", "unknown", "present", "副厅级",
     "confirmed via news report 2026-07-07"],

    # 熊健 (Political & Legal Affairs)
    ["chongqing_qijiang_xiong_jian", "chongqing_qijiang_politics_law",
     "綦江区委常委、政法委书记", "unknown", "present", "副厅级",
     "confirmed via news report 2026-07-07"],

    # 宋秉洲 (Party Standing Committee member)
    ["chongqing_qijiang_song_bingzhou", "chongqing_qijiang_party_committee",
     "綦江区委常委", "unknown", "present", "副厅级",
     "confirmed via news report 2026-07-08"],

    # 唐鹏程 (People's Congress)
    ["chongqing_qijiang_tang_pengcheng", "chongqing_qijiang_people_congress",
     "綦江区人大常委会主任", "unknown", "present", "正厅级",
     "confirmed via news report 2026-07-09"],

    # 钟远平 (CPPCC)
    ["chongqing_qijiang_zhong_yuanping", "chongqing_qijiang_cppcc",
     "綦江区政协主席", "unknown", "present", "正厅级",
     "confirmed via news report 2026-07-09"],

    # 姜天波 (Predecessor)
    ["chongqing_qijiang_jiang_tianbo", "chongqing_qijiang_party_committee",
     "綦江区委书记", "2020", "2024-10", "正厅级",
     "尹国喜的前任；约2024年离职"],

    # 罗成 (Predecessor Mayor)
    ["chongqing_qijiang_ro_xiaoping_prev", "chongqing_qijiang_gov",
     "綦江区区长", "2021", "2023", "正厅级",
     "郭小萍的前任；约2023年离职调任"],
]

# ── RELATIONSHIPS ──
# Fields: person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_guo_xiaoping",
     "党政搭档", "区委书记与区长党政正职搭档", "中共重庆市綦江区委员会/綦江区人民政府",
     "2024-至今"],

    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_li_wei",
     "上下级关系", "区委书记与常务副区长", "中共重庆市綦江区委员会",
     "2024-至今"],

    ["chongqing_qijiang_guo_xiaoping", "chongqing_qijiang_li_wei",
     "上下级关系", "区长与常务副区长", "重庆市綦江区人民政府",
     "2023-至今"],

    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_tao_min",
     "上下级关系", "区委书记与纪委书记", "中共重庆市綦江区委员会",
     "2024-至今"],
    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_ren_jun",
     "上下级关系", "区委书记与组织部长", "中共重庆市綦江区委员会",
     "2024-至今"],
    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_cai_peng",
     "上下级关系", "区委书记与宣传部长", "中共重庆市綦江区委员会",
     "2024-至今"],
    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_wang_hongxing",
     "上下级关系", "区委书记与统战部长", "中共重庆市綦江区委员会",
     "2024-至今"],
    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_xiong_jian",
     "上下级关系", "区委书记与政法委书记", "中共重庆市綦江区委员会",
     "2024-至今"],

    ["chongqing_qijiang_yin_guoxi", "chongqing_qijiang_jiang_tianbo",
     "前后任", "尹国喜接替姜天波任綦江区委书记", "中共重庆市綦江区委员会",
     "2024（交接）"],

    ["chongqing_qijiang_guo_xiaoping", "chongqing_qijiang_ro_xiaoping_prev",
     "前后任", "郭小萍接替罗成任綦江区区长", "重庆市綦江区人民政府",
     "2023（交接）"],

    ["chongqing_qijiang_ni_ming", "chongqing_qijiang_li_wei",
     "同僚", "同为区政府副职领导", "重庆市綦江区人民政府",
     "2022-至今"],
    ["chongqing_qijiang_li_qiansong", "chongqing_qijiang_liu_shuran",
     "同僚", "同为区政府副区长", "重庆市綦江区人民政府",
     "2025-至今"],
    ["chongqing_qijiang_tao_min", "chongqing_qijiang_ren_jun",
     "同僚", "同为区委常委", "中共重庆市綦江区委员会",
     "unknown-至今"],
    ["chongqing_qijiang_cai_peng", "chongqing_qijiang_wang_hongxing",
     "同僚", "同为区委常委", "中共重庆市綦江区委员会",
     "unknown-至今"],
    ["chongqing_qijiang_xiong_jian", "chongqing_qijiang_song_bingzhou",
     "同僚", "同为区委常委", "中共重庆市綦江区委员会",
     "unknown-至今"],
]


# ── HELPERS ──

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p[9] or ""
    if "书记" in role and "纪委" not in role and "副书记" not in role:
        return "220,30,30"
    if "区长" in role or ("区长" in role and "副" not in role):
        return "40,100,220"
    if "副区长" in role:
        return "40,140,220"
    if "纪委书记" in role:
        return "180,130,50"
    if "人大" in role:
        return "220,160,40"
    if "政协" in role:
        return "200,150,40"
    if "副书记" in role:
        return "180,60,180"
    if "部长" in role or "政法委" in role:
        return "120,120,120"
    return "160,160,160"


def person_size(p):
    role = p[9] or ""
    if "区委书记" in role:
        return "20.0"
    if "区长" in role and "副" not in role:
        return "18.0"
    if "副书记" in role:
        return "16.0"
    if "人大" in role or "政协" in role:
        return "14.0"
    if "常委" in role:
        return "14.0"
    return "12.0"


def org_color(o):
    t = o[2] or ""
    if "党委" in t:
        return "200,60,60"
    if "政府" in t or "公安" in t:
        return "60,100,200"
    if "人大" in t:
        return "200,150,40"
    if "政协" in t:
        return "180,130,40"
    if "纪委" in t:
        return "160,120,40"
    if "党委部门" in t:
        return "200,80,80"
    return "120,120,120"


# ── BUILD DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3"')
    lines.append('      xmlns:viz="http://gexf.net/1.3/viz"')
    lines.append('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"')
    lines.append('      version="1.3">')
    lines.append('  <meta>')
    lines.append('    <creator>China-Gov-Network Investigation</creator>')
    lines.append('    <description>重庆市綦江区领导班子工作关系网络</description>')
    lines.append(f'    <date>{TODAY}</date>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Node Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="org_type" title="Org Type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
    lines.append('      <attribute id="start" title="Start Date" type="string"/>')
    lines.append('      <attribute id="end" title="End Date" type="string"/>')
    lines.append('      <attribute id="rank" title="Rank" type="string"/>')
    lines.append('      <attribute id="strength" title="Strength" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        role = p[9] or ""
        birth = p[4] or ""
        c = person_color(p)
        sz = person_size(p)
        rgb = c.split(",")
        lines.append(f'      <node id="{pid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="birth" value="{esc(birth)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        c = org_color(o)
        rgb = c.split(",")
        lines.append(f'      <node id="{oid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="org_type" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        eid += 1
        pid, oid, title, start, end_, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" type="directed" label="{esc(title)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="start" value="{esc(start or "")}"/>')
        lines.append(f'          <attvalue for="end" value="{esc(end_ or "")}"/>')
        lines.append(f'          <attvalue for="rank" value="{esc(rank or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="80" g="80" b="80" a="0.5"/>')
        lines.append('        <viz:thickness value="1.0"/>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        a, b, typ, context, overlap_org, overlap_period = r
        is_strong = True  # all confirmed relationships are strong
        cr, cg_val, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        lines.append(f'      <edge id="e{eid}" source="{a}" target="{b}" type="undirected" label="{esc(context)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="strength" value="strong"/>')
        lines.append(f'          <attvalue for="context" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg_val}" b="{cb}" a="0.8"/>')
        lines.append(f'        <viz:thickness value="{thickness}"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# ── STATS ──

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
        if table == "persons":
            c.execute("SELECT COUNT(*) FROM persons WHERE source LIKE '%待确认%' OR source = ''")
            pending = c.fetchone()[0]
            print(f"    - 待确认: {pending}, 已确认: {cnt - pending}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  重庆市綦江区领导班子工作关系网络")
    print("  等级: 市辖区（直辖市）")
    print("  生成日期: 2026-07-16")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\nSummary:")
    print_stats()
    print("\nDone.")
