#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 九原区 (Jiuyuan District), 包头市, 内蒙古自治区"""
import sqlite3
import os
import sys
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "九原区_network.db")
GEXF_PATH = os.path.join(STAGING, "九原区_network.gexf")

PERSONS = [
    # 区委领导
    {"id": 1, "name": "刘俊义", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委书记", "current_org": "中共包头市九原区委员会"},
    {"id": 2, "name": "刘小平", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府党组书记、区长", "current_org": "九原区人民政府"},
    {"id": 3, "name": "赵宇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委副书记、政法委书记", "current_org": "中共包头市九原区委员会"},
    {"id": 4, "name": "李凯", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委、纪委书记、监委主任", "current_org": "中共包头市九原区纪律检查委员会"},
    {"id": 5, "name": "刘烨", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委、组织部部长", "current_org": "中共包头市九原区委员会"},
    {"id": 6, "name": "高阳", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委、区政府副区长", "current_org": "九原区人民政府"},
    # 区政府领导
    {"id": 7, "name": "梁文", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府党组成员、常务副区长", "current_org": "九原区人民政府"},
    {"id": 8, "name": "王勇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府党组成员、副区长", "current_org": "九原区人民政府"},
    {"id": 9, "name": "李晨伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府党组成员、副区长", "current_org": "九原区人民政府"},
    {"id": 10, "name": "宋丹华", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府党组成员、副区长", "current_org": "九原区人民政府"},
    {"id": 11, "name": "姚振忠", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府副区长（公安）", "current_org": "九原区人民政府"},
    {"id": 12, "name": "赵欣", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府副区长", "current_org": "九原区人民政府"},
    {"id": 13, "name": "赵部军", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府党组成员、中心区建设管理委员会主任", "current_org": "包头市中心区建设管理委员会"},
    # 前任领导（补充到关系网络）
    {"id": 14, "name": "廉冬", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "前任九原区委书记（2021.8-2022.4）", "current_org": "中共包头市九原区委员会"},
    {"id": 15, "name": "刘海泉", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "前任九原区委书记", "current_org": "中共包头市九原区委员会"},
    {"id": 16, "name": "郭文亮", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "原九原区政府副区长（2025.2-2026.4）", "current_org": "九原区人民政府"},
    {"id": 17, "name": "刘文光", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "原九原区监察委员会主任（2025.6辞职）", "current_org": "九原区监察委员会"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共包头市九原区委员会", "type": "党委", "level": "县级", "parent": "中共包头市委员会", "location": "内蒙古自治区包头市九原区"},
    {"id": 102, "name": "九原区人民政府", "type": "政府", "level": "县级", "parent": "包头市人民政府", "location": "内蒙古自治区包头市九原区"},
    {"id": 103, "name": "中共包头市九原区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共包头市纪律检查委员会", "location": "内蒙古自治区包头市九原区"},
    {"id": 104, "name": "中共包头市九原区委政法委员会", "type": "党委部门", "level": "正科级", "parent": "中共包头市九原区委员会", "location": "内蒙古自治区包头市九原区"},
    {"id": 105, "name": "中共包头市九原区委组织部", "type": "党委部门", "level": "正科级", "parent": "中共包头市九原区委员会", "location": "内蒙古自治区包头市九原区"},
    {"id": 106, "name": "包头市中心区建设管理委员会", "type": "事业单位", "level": "正处级", "parent": "包头市人民政府", "location": "内蒙古自治区包头市"},
    {"id": 107, "name": "九原区监察委员会", "type": "监察", "level": "县级", "parent": "包头市监察委员会", "location": "内蒙古自治区包头市九原区"},
]

POSITIONS = [
    # 刘俊义 - 现任区委书记（2022.4至今）
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2022-04", "end": "", "rank": "正处级", "note": "2022年4月5日全区干部大会宣布任职"},
    # 刘小平 - 现任区长
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "区委副书记", "start": "", "end": "", "rank": "副处级", "note": "区长兼任区委副书记"},
    # 赵宇 - 区委副书记、政法委书记
    {"person_id": 3, "org_id": 101, "title": "区委副书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 104, "title": "政法委书记", "start": "", "end": "", "rank": "正科级", "note": "副书记兼任政法委书记"},
    # 李凯 - 区委常委、纪委书记
    {"person_id": 4, "org_id": 101, "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 103, "title": "纪委书记、监委主任", "start": "2025-06", "end": "", "rank": "副处级", "note": "2025年6月任代理主任"},
    # 刘烨 - 区委常委、组织部长
    {"person_id": 5, "org_id": 101, "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 105, "title": "组织部部长", "start": "", "end": "", "rank": "正科级", "note": ""},
    # 高阳 - 区委常委、副区长
    {"person_id": 6, "org_id": 101, "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 102, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 梁文 - 常务副区长
    {"person_id": 7, "org_id": 102, "title": "副区长（常务）", "start": "", "end": "", "rank": "副处级", "note": "负责区人民政府常务工作"},
    # 王勇
    {"person_id": 8, "org_id": 102, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": "分管农业农村、林草、水务"},
    {"person_id": 9, "org_id": 102, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 102, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 102, "title": "副区长（公安）", "start": "2025-02", "end": "", "rank": "副处级", "note": "主持区公安分局工作"},
    {"person_id": 12, "org_id": 102, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 赵部军
    {"person_id": 13, "org_id": 106, "title": "主任", "start": "", "end": "", "rank": "正处级", "note": "中心区建设管理委员会"},
    {"person_id": 13, "org_id": 102, "title": "区政府党组成员", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 前任区委书记
    {"person_id": 14, "org_id": 101, "title": "区委书记", "start": "2021-08", "end": "2022-04", "rank": "正处级", "note": "廉冬，2021年8月任职，任期约8个月"},
    {"person_id": 15, "org_id": 101, "title": "区委书记", "start": "", "end": "2021-08", "rank": "正处级", "note": "刘海泉，前任区委书记"},
    # 原副区长
    {"person_id": 16, "org_id": 102, "title": "副区长", "start": "2025-02", "end": "2026-04", "rank": "副处级", "note": "郭文亮，2025年2月任命，2026年4月免职"},
    # 原监委主任
    {"person_id": 17, "org_id": 107, "title": "监委主任", "start": "", "end": "2025-06", "rank": "副处级", "note": "刘文光，2025年6月因工作调整辞职"},
]

RELATIONSHIPS = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长的党政主要领导工作搭档", "overlap_org": "九原区", "overlap_period": "2022.4至今"},
    # 副书记与书记
    {"person_a": 3, "person_b": 1, "type": "上下级", "context": "区委副书记协助书记工作", "overlap_org": "中共九原区委员会", "overlap_period": "current"},
    # 纪委书记与书记
    {"person_a": 4, "person_b": 1, "type": "上下级", "context": "纪委书记在区委常委会中工作", "overlap_org": "中共九原区委员会", "overlap_period": "current"},
    # 组织部长与书记
    {"person_a": 5, "person_b": 1, "type": "上下级", "context": "组织部长在区委常委会中工作", "overlap_org": "中共九原区委员会", "overlap_period": "current"},
    # 常委副区长与书记
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "区委常委在区委常委会中工作", "overlap_org": "中共九原区委员会", "overlap_period": "current"},
    # 区长与常务副区长
    {"person_a": 2, "person_b": 7, "type": "政府搭档", "context": "常务副区长协助区长主持区政府日常工作", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    # 副区长们与区长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "副区长协助区长工作", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "副区长协助区长工作", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "副区长协助区长工作", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "副区长协助区长工作", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "副区长协助区长工作", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "副区长协助区长工作", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区政府党组成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    # 前任关系
    {"person_a": 14, "person_b": 15, "type": "前后任", "context": "刘海泉→廉冬，区委书记更替", "overlap_org": "中共九原区委员会", "overlap_period": "2021"},
    {"person_a": 14, "person_b": 1, "type": "前后任", "context": "廉冬→刘俊义，区委书记更替（2022年4月）", "overlap_org": "中共九原区委员会", "overlap_period": "2022-04"},
    # 副区长之间
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 10, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 11, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 12, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 11, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 12, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 11, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 12, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 11, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 12, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 12, "type": "同僚", "context": "区政府领导班子成员", "overlap_org": "九原区人民政府", "overlap_period": "current"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
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
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
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
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"]))

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in RELATIONSHIPS:
        if r["person_a"] != r["person_b"]:
            c.execute("""
                INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

    p_count = len(PERSONS)
    o_count = len(ORGANIZATIONS)
    pos_count = len(POSITIONS)
    r_count = len([r for r in RELATIONSHIPS if r["person_a"] != r["person_b"]])
    print(f"DB: {p_count} persons, {o_count} organizations, {pos_count} positions, {r_count} relationships")


def get_person_color(post):
    if "区委书记" == post or "区委书记" in post and "副" not in post and "前任" not in post:
        return (200, 30, 30), 25.0, "square"
    if "区长" in post and "副" not in post and "前任" not in post:
        return (30, 100, 200), 22.0, "square"
    if "副书记" in post and "前任" not in post:
        return (200, 30, 30), 18.0, "triangle"
    if "纪委书记" in post:
        return (230, 150, 30), 18.0, "triangle"
    if "区委常委" in post:
        return (200, 30, 30), 16.0, "triangle"
    if "常务副区长" in post:
        return (30, 100, 200), 16.0, "triangle"
    if "副区长" in post and "前任" not in post:
        return (30, 100, 200), 15.0, "triangle"
    if "党组成员" in post:
        return (30, 100, 200), 14.0, "triangle"
    # 前任领导
    return (150, 150, 150), 12.0, "circle"


def get_org_color(otype):
    colors = {
        "党委": (255, 200, 200),
        "党委部门": (255, 220, 220),
        "政府": (200, 200, 255),
        "纪委": (255, 165, 0),
        "监察": (255, 180, 80),
        "事业单位": (220, 220, 220),
    }
    return colors.get(otype, (200, 200, 200))


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="utf-8"?>')
    lines.append('<gexf xmlns="http://www.gexf.net/1.3"')
    lines.append('      xmlns:viz="http://www.gexf.net/1.3/viz"')
    lines.append('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('      xsi:schemaLocation="http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd"')
    lines.append('      version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>包头市九原区领导班子工作关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('      <attribute id="4" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = f"p{p['id']}"
        r, g, b = (150, 150, 150)
        size = 12.0
        shape = "circle"
        color, sz, shp = get_person_color(p["current_post"])
        r, g, b = color
        size = sz
        shape = shp
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = f"o{o['id']}"
        cr, cg, cb = get_org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1

    # Person -> Organization (worked_at)
    for pos in POSITIONS:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" type="directed" weight="1.0">')
        lines.append(f'        <viz:color r="180" g="180" b="180" a="0.6"/>')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationship)
    seen_pairs = set()
    for r in RELATIONSHIPS:
        if r["person_a"] != r["person_b"]:
            pair = tuple(sorted([r["person_a"], r["person_b"]]))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                a = f"p{r['person_a']}"
                b = f"p{r['person_b']}"
                if "党政" in r["type"]:
                    ec, thickness = "200,30,30", 3.0
                elif "上下级" in r["type"] or "前后任" in r["type"]:
                    ec, thickness = "100,150,200", 2.0
                else:
                    ec, thickness = "180,180,200", 1.5
                lines.append(f'      <edge id="{eid}" source="{a}" target="{b}" type="undirected" weight="{thickness}">')
                lines.append(f'        <viz:color r="{ec.split(",")[0]}" g="{ec.split(",")[1]}" b="{ec.split(",")[2]}" a="0.8"/>')
                lines.append('        <attvalues>')
                lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
                lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
                lines.append('        </attvalues>')
                lines.append('      </edge>')
                eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_nodes = len(PERSONS) + len(ORGANIZATIONS)
    total_edges = len(POSITIONS) + len(seen_pairs)
    print(f"GEXF: {total_nodes} nodes, {total_edges} edges")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print(f"Done. Files in {STAGING}")
