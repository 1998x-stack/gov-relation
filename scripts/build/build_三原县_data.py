#!/usr/bin/env python3
"""
三原县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

三原县是陕西省咸阳市下辖的县，位于关中平原中部。
数据来源：三原县政府网站 (www.snsanyuan.gov.cn) 领导之窗页面
采集日期：2026-07-25
"""
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Use the gov_relation runner when available
USING_RUNNER = False
try:
    from gov_relation.runner import run_build  # noqa
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa
    USING_RUNNER = True
except ImportError:
    pass

SLUG = "三原县"
DATE = "2026-07-25"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
persons = [
    # --- 县委领导 (10人) ---
    (1, "赵俊强", "男", "汉族", "", "", "", "中共党员", "",
     "县委书记", "中共三原县委",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (2, "杨红刚", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记、县长", "三原县人民政府",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (3, "段朋泊", "男", "汉族", "1979-10", "", "在职研究生", "中共党员", "",
     "县委副书记（专职）", "中共三原县委",
     "baike.baidu.com/item/段朋泊/58772370"),
    (4, "曹博", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、常务副县长", "三原县人民政府",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (5, "刘晖", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、宣传部部长", "中共三原县委宣传部",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (6, "田广军", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、县纪委书记、县监委主任", "中共三原县纪委/县监委",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (7, "李科显", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、副县长", "三原县人民政府",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (8, "许超莹", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、政法委书记", "中共三原县委政法委",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (9, "李超", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、组织部部长", "中共三原县委组织部",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (10, "田成博", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、县人武部部长", "三原县人武部",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),

    # --- 县人大领导 (5人) ---
    (11, "蒙小卫", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会党组书记、主任", "三原县人大常委会",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (12, "倪新刚", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "三原县人大常委会",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (13, "程宁", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "三原县人大常委会",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (14, "李鹏科", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "三原县人大常委会",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (15, "蔺永芳", "女", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "三原县人大常委会",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),

    # --- 县政府领导 (含县长和常委副县长已在上方列出，此处只列出非县委常委的副县长) ---
    # 杨红刚(2)和曹博(4)已在县委领导部分列出
    (16, "尚科", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "三原县人民政府",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (17, "常俊鸿", "男", "汉族", "", "", "", "中共党员", "",
     "副县长、县公安局局长", "三原县公安局",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (18, "陈飞", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "三原县人民政府",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (19, "魏书威", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "三原县人民政府",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),

    # --- 县政协领导 (4人) ---
    (20, "李学军", "男", "汉族", "", "", "", "中共党员", "",
     "县政协主席", "三原县政协",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (21, "张永刚", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "三原县政协",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (22, "钱滨", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "三原县政协",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
    (23, "姚青勋", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "三原县政协",
     "snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共三原县委", "党委", "县级", "中共咸阳市委", "陕西省咸阳市三原县"),
    (2, "三原县人民政府", "政府", "县级", "咸阳市人民政府", "陕西省咸阳市三原县"),
    (3, "中共三原县纪律检查委员会", "纪委", "县级", "中共三原县委", "陕西省咸阳市三原县"),
    (4, "三原县监察委员会", "监察", "县级", "三原县人民政府", "陕西省咸阳市三原县"),
    (5, "三原县人大常委会", "人大", "县级", "", "陕西省咸阳市三原县"),
    (6, "三原县政协", "政协", "县级", "", "陕西省咸阳市三原县"),
    (7, "中共三原县委宣传部", "党委部门", "县级", "中共三原县委", "陕西省咸阳市三原县"),
    (8, "中共三原县委政法委", "党委部门", "县级", "中共三原县委", "陕西省咸阳市三原县"),
    (9, "中共三原县委组织部", "党委部门", "县级", "中共三原县委", "陕西省咸阳市三原县"),
    (10, "三原县人武部", "军事", "县级", "咸阳军分区", "陕西省咸阳市三原县"),
    (11, "三原县公安局", "政府", "县级", "咸阳市公安局", "陕西省咸阳市三原县"),
]

# ===== 任职数据 =====
# (person_id, org_id, title, start, end, rank, note)
positions = [
    # 县委领导
    (1, 1, "县委书记", "", "", "正县级", ""),
    (2, 1, "县委副书记", "", "", "正县级", "兼任县长"),
    (2, 2, "县长", "", "", "正县级", ""),
    (3, 1, "县委副书记", "", "", "副县级", "专职副书记"),
    (4, 1, "县委常委", "", "", "副县级", ""),
    (4, 2, "常务副县长", "", "", "副县级", ""),
    (5, 1, "县委常委", "", "", "副县级", ""),
    (5, 7, "宣传部部长", "", "", "副县级", ""),
    (6, 1, "县委常委", "", "", "副县级", ""),
    (6, 3, "县纪委书记", "", "", "副县级", ""),
    (6, 4, "县监委主任", "", "", "副县级", ""),
    (7, 1, "县委常委", "", "", "副县级", ""),
    (7, 2, "副县长", "", "", "副县级", ""),
    (8, 1, "县委常委", "", "", "副县级", ""),
    (8, 8, "政法委书记", "", "", "副县级", ""),
    (9, 1, "县委常委", "", "", "副县级", ""),
    (9, 9, "组织部部长", "", "", "副县级", ""),
    (10, 1, "县委常委", "", "", "副县级", ""),
    (10, 10, "人武部部长", "", "", "副县级", ""),

    # 人大领导
    (11, 5, "党组书记、主任", "", "", "正县级", ""),
    (12, 5, "副主任", "", "", "副县级", ""),
    (13, 5, "副主任", "", "", "副县级", ""),
    (14, 5, "副主任", "", "", "副县级", ""),
    (15, 5, "副主任", "", "", "副县级", ""),

    # 县政府领导（非县委常委）
    (16, 2, "副县长", "", "", "副县级", ""),
    (17, 2, "副县长", "", "", "副县级", "兼任公安局长"),
    (17, 11, "局长", "", "", "副县级", ""),
    (18, 2, "副县长", "", "", "副县级", ""),
    (19, 2, "副县长", "", "", "副县级", ""),

    # 政协领导
    (20, 6, "主席", "", "", "正县级", ""),
    (21, 6, "副主席", "", "", "副县级", ""),
    (22, 6, "副主席", "", "", "副县级", ""),
    (23, 6, "副主席", "", "", "副县级", ""),

    # 段朋泊此前在秦都区的任职
    (3, 2, "秦都区副区长", "2022-03-19", "2025-11", "副县级", "此前任职"),
]

# ===== 关系数据 =====
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    # 县委常委班子成员关系
    (1, 2, "同事", "县委书记与县长搭档", "中共三原县委常委会", "2026年"),
    (1, 3, "同事", "县委书记与专职副书记共事", "中共三原县委常委会", "2026年"),
    (1, 4, "同事", "县委书记与常务副县长共事", "中共三原县委常委会", "2026年"),
    (1, 5, "同事", "县委书记与宣传部长共事", "中共三原县委常委会", "2026年"),
    (1, 6, "同事", "县委书记与纪委书记共事", "中共三原县委常委会", "2026年"),
    (1, 7, "同事", "县委书记与副县长共事", "中共三原县委常委会", "2026年"),
    (1, 8, "同事", "县委书记与政法委书记共事", "中共三原县委常委会", "2026年"),
    (1, 9, "同事", "县委书记与组织部长共事", "中共三原县委常委会", "2026年"),
    (1, 10, "同事", "县委书记与人武部长共事", "中共三原县委常委会", "2026年"),

    (2, 3, "同事", "县长与专职副书记共事", "中共三原县委常委会", "2026年"),
    (2, 4, "同事", "县长与常务副县长共事", "三原县人民政府", "2026年"),
    (2, 7, "同事", "县长与副县长共事", "三原县人民政府", "2026年"),
    (2, 16, "同事", "县长与副县长共事", "三原县人民政府", "2026年"),
    (2, 17, "同事", "县长与副县长共事", "三原县人民政府", "2026年"),
    (2, 18, "同事", "县长与副县长共事", "三原县人民政府", "2026年"),
    (2, 19, "同事", "县长与副县长共事", "三原县人民政府", "2026年"),

    (4, 7, "同事", "常务副县长与副县长共事", "三原县人民政府", "2026年"),
    (4, 16, "同事", "常务副县长与副县长共事", "三原县人民政府", "2026年"),
    (4, 17, "同事", "常务副县长与副县长共事", "三原县人民政府", "2026年"),
    (4, 18, "同事", "常务副县长与副县长共事", "三原县人民政府", "2026年"),
    (4, 19, "同事", "常务副县长与副县长共事", "三原县人民政府", "2026年"),

    # 人大主任列席常委会
    (11, 1, "同事", "人大主任列席县委常委会", "中共三原县委常委会", "2026年"),
    (11, 2, "同事", "人大主任与县长共事", "三原县", "2026年"),

    # 政协主席列席常委会
    (20, 1, "同事", "政协主席列席县委常委会", "中共三原县委常委会", "2026年"),
    (20, 2, "同事", "政协主席与县长共事", "三原县", "2026年"),

    # 段朋泊与秦都区政府的过往联系
    (3, 4, "可能交集", "段朋泊曾任秦都区副区长（至2025年11月），曹博现为三原常务副县长，是否曾在咸阳市政府系统有交集待查", "", "待查"),
]


def build_standalone():
    """Standalone build without the gov_relation runner."""
    STAGING = Path(__file__).parent
    DB_PATH = STAGING / "三原县_network.db"
    GEXF_PATH = STAGING / "三原县_network.gexf"

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    # Create tables
    conn.executescript("""
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
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
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert data
    conn.executemany(
        "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        persons,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
        organizations,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
        positions,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
        relationships,
    )
    conn.commit()

    print(f"DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    conn.close()

    # Generate GEXF
    name_map = {p[0]: p[1] for p in persons}
    title_map = {}
    role_map = {}
    gender_map = {}
    for p in persons:
        title_map[p[0]] = p[9]
        role_map[p[0]] = p[9]
        gender_map[p[0]] = p[2]

    org_name_map = {o[0]: o[1] for o in organizations}
    org_type_map = {o[0]: o[2] for o in organizations}

    org_nodes = {}
    for pid, org_id, title, *_ in positions:
        if pid not in org_nodes:
            org_nodes[pid] = []
        org_nodes[pid].append(org_id)

    gexf_parts = []
    gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_parts.append('<graph defaultedgetype="undirected">')

    # Nodes
    gexf_parts.append('<nodes>')
    pid_offset = 0
    oid_offset = 100000

    for p in persons:
        pid = p[0]
        name = p[1]
        title = p[9]

        # Color by role
        if '书记' in title and '副' not in title:
            color = '#E03C31'  # Red - party secretary
            size = 20.0
        elif '县长' in title and '副' not in title and '副书记' not in title:
            color = '#2979FF'  # Blue - county chief
            size = 20.0
        elif '副' in title and ('书记' in title or '县长' in title):
            color = '#2979FF'  # Blue - deputy secretary/magistrate
            size = 16.0
        elif '纪委书记' in title or '监委' in title:
            color = '#FF8C00'  # Orange - discipline
            size = 16.0
        elif '人大' in title:
            color = '#9C27B0'  # Purple - people's congress
            size = 14.0
        elif '政协' in title:
            color = '#00BCD4'  # Cyan - political consultative
            size = 14.0
        elif '县委常委' in title:
            color = '#FF7043'  # Deep orange - standing committee
            size = 16.0
        elif '副县长' in title:
            color = '#42A5F5'  # Light blue - deputy county chief
            size = 14.0
        else:
            color = '#9E9E9E'  # Grey - other
            size = 12.0

        gexf_parts.append(f'<node id="{pid + pid_offset}" label="{escape(name)}">')
        gexf_parts.append(f'<attvalues>')
        gexf_parts.append(f'<attvalue for="role" value="{escape(title)}"/>')
        gexf_parts.append(f'<attvalue for="type" value="person"/>')
        birth = p[4] or ''
        gexf_parts.append(f'<attvalue for="birth" value="{escape(birth)}"/>')
        gexf_parts.append(f'</attvalues>')
        gexf_parts.append(f'<viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>')
        gexf_parts.append(f'<viz:size value="{size}"/>')
        if title:
            gexf_parts.append(f'<viz:position x="0" y="0" z="0"/>')
        gexf_parts.append('</node>')

    for o in organizations:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        if otype in ('党委', '党委部门', '纪委'):
            color = '#E03C31'
        elif otype == '政府':
            color = '#2979FF'
        elif otype in ('人大',):
            color = '#9C27B0'
        elif otype == '政协':
            color = '#00BCD4'
        elif otype == '军事':
            color = '#4CAF50'
        else:
            color = '#9E9E9E'

        gexf_parts.append(f'<node id="{oid + oid_offset}" label="{escape(oname)}">')
        gexf_parts.append('<attvalues>')
        gexf_parts.append(f'<attvalue for="role" value="{escape(oname)}"/>')
        gexf_parts.append(f'<attvalue for="type" value="organization"/>')
        gexf_parts.append('</attvalues>')
        gexf_parts.append(f'<viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>')
        gexf_parts.append('<viz:size value="8.0"/>')
        gexf_parts.append('</node>')

    gexf_parts.append('</nodes>')

    # Edges
    gexf_parts.append('<edges>')
    edge_id = 0

    for pos in positions:
        pid, oid = pos[0], pos[1]
        gexf_parts.append(
            f'<edge id="{edge_id}" source="{pid + pid_offset}" target="{oid + oid_offset}" '
            f'label="{escape(pos[2])}" type="directed">'
        )
        gexf_parts.append('<attvalues>')
        gexf_parts.append(f'<attvalue for="type" value="worked_at"/>')
        if pos[3]:
            gexf_parts.append(f'<attvalue for="start" value="{escape(pos[3])}"/>')
        if pos[4]:
            gexf_parts.append(f'<attvalue for="end" value="{escape(pos[4])}"/>')
        gexf_parts.append('</attvalues>')
        gexf_parts.append(f'<viz:color r="180" g="180" b="180"/>')
        gexf_parts.append(f'<viz:thickness value="1.0"/>')
        gexf_parts.append('</edge>')
        edge_id += 1

    for rel in relationships:
        pa, pb = rel[0], rel[1]
        rtype = rel[2]
        context = rel[3]

        if '同事' in rtype:
            color = '#C9A94E'
            thickness = 2.0
        elif '可能交集' in rtype:
            color = '#64B5F6'
            thickness = 1.0
        else:
            color = '#9E9E9E'
            thickness = 1.5

        gexf_parts.append(
            f'<edge id="{edge_id}" source="{pa + pid_offset}" target="{pb + pid_offset}" '
            f'label="{escape(rtype)}">'
        )
        gexf_parts.append('<attvalues>')
        gexf_parts.append(f'<attvalue for="type" value="relationship"/>')
        gexf_parts.append(f'<attvalue for="context" value="{escape(context)}"/>')
        if rel[5]:
            gexf_parts.append(f'<attvalue for="period" value="{escape(rel[5])}"/>')
        gexf_parts.append('</attvalues>')
        gexf_parts.append(f'<viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>')
        gexf_parts.append(f'<viz:thickness value="{thickness}"/>')
        gexf_parts.append('</edge>')
        edge_id += 1

    gexf_parts.append('</edges>')

    # Attributes
    gexf_parts.append('<attributes class="node">')
    gexf_parts.append('<attribute id="role" title="Role" type="string"/>')
    gexf_parts.append('<attribute id="type" title="Type" type="string"/>')
    gexf_parts.append('<attribute id="birth" title="Birth" type="string"/>')
    gexf_parts.append('</attributes>')
    gexf_parts.append('<attributes class="edge">')
    gexf_parts.append('<attribute id="type" title="Type" type="string"/>')
    gexf_parts.append('<attribute id="context" title="Context" type="string"/>')
    gexf_parts.append('<attribute id="start" title="Start" type="string"/>')
    gexf_parts.append('<attribute id="end" title="End" type="string"/>')
    gexf_parts.append('<attribute id="period" title="Period" type="string"/>')
    gexf_parts.append('</attributes>')

    gexf_parts.append('</graph>')
    gexf_parts.append('</gexf>')

    with open(GEXF_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(gexf_parts))

    print(f"GEXF: {GEXF_PATH}")
    print(f"Built successfully: {SLUG}")


def main():
    if USING_RUNNER:
        persons_dict = [
            {"id": str(p[0]), "name": p[1], "gender": p[2], "ethnicity": p[3],
             "birth": p[4], "birthplace": p[5], "education": p[6],
             "party_join": p[7], "work_start": p[8], "current_post": p[9],
             "current_org": p[10], "source": p[11]}
            for p in persons
        ]
        orgs_dict = [
            {"id": str(o[0]), "name": o[1], "type": o[2], "level": o[3],
             "parent": o[4], "location": o[5]}
            for o in organizations
        ]
        positions_dict = [
            {"person_id": str(pos[0]), "org_id": str(pos[1]), "title": pos[2],
             "start": pos[3] or "", "end": pos[4] or "", "rank": pos[5] or "", "note": pos[6] or ""}
            for pos in positions
        ]
        rels_dict = [
            {"person_a": str(rel[0]), "person_b": str(rel[1]), "type": rel[2],
             "context": rel[3], "overlap_org": rel[4], "overlap_period": rel[5]}
            for rel in relationships
        ]
        run_build(
            slug=SLUG,
            persons=persons_dict,
            organizations=orgs_dict,
            positions=positions_dict,
            relationships=rels_dict,
            db_path=DATABASE_DIR / "三原县_network.db",
            gexf_path=GRAPH_DIR / "三原县_network.gexf",
        )
    else:
        build_standalone()


if __name__ == "__main__":
    main()
