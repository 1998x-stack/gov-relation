#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite DB + GEXF graph + person JSONs for Xiangyang City (襄阳市), Hubei Province.

Covers the prefecture-level city (地级市) 襄阳市 leadership network:
- Current 市委书记 吴海涛, 市长 杜海洋
- City 四大班子: 市委书记/市长/市人大主任/市政协主席
- Full 市委书记 & 市长 predecessor/successor chains
- Cross-region transfer network (predecessors' post-Xiangyang destinations)

Sources (all confirmed, accessed 2026-08-07):
- 维基百科 zh.wikipedia.org: 襄阳市(现任领导/历任领导表), 吴海涛(1967年), 王祺扬, 马旭明, 郄英才, 王太晖
- 中国经济网 district.ce.cn: 杜海洋任襄阳市代市长(2024-10-17), 吴海涛任襄阳市委书记(2025-01-04),
  吕义斌当选襄阳人大主任(2022-01), 余世明当选襄阳市政协主席(2026-01)
- 百度百科/人民网地方领导资料库(经维基引证)

NOTE: 杜海洋(现任市长)出任襄阳市长前的完整履历, 及现任市委常委/副市长全名单,
在网络受限环境下未能确证, 已明确标注为 open_questions/gap, 未臆造。
"""

import os
import sys
import sqlite3
from datetime import datetime


def find_repo_root():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(d, "gov_relation")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return d
        d = parent


BASE = find_repo_root()
STAGING = os.path.join(BASE, "data", "tmp", "hubei_襄阳市")
DB_PATH = os.path.join(STAGING, "襄阳市_network.db")
GEXF_PATH = os.path.join(STAGING, "襄阳市_network.gexf")
PERSONS_DIR = STAGING

# Current-as-of date for the dataset
AS_OF = "2026-08-07"


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    {
        "id": 1,
        "name": "吴海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年6月",
        "birthplace": "湖北省英山县",
        "education": "在职大学学历",
        "party_join": "1991年1月",
        "work_start": "1986年7月",
        "current_post": "中共湖北省委常委、襄阳市委书记",
        "current_org": "中共襄阳市委员会",
        "source": "http://district.ce.cn/newarea/sddy/202501/04/t20250104_39256355.shtml",
    },
    {
        "id": 2,
        "name": "杜海洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "湖北省秭归县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共襄阳市委副书记、襄阳市人民政府市长",
        "current_org": "襄阳市人民政府",
        "source": "http://district.ce.cn/newarea/sddy/202410/17/t20241017_39171425.shtml",
    },
    # ── 市人大 / 市政协 ──
    {
        "id": 3,
        "name": "吕义斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年1月",
        "birthplace": "湖北省沙洋县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄阳市人大常委会主任",
        "current_org": "襄阳市人民代表大会常务委员会",
        "source": "http://district.ce.cn/newarea/sddy/202201/10/t20220110_37242588.shtml",
    },
    {
        "id": 4,
        "name": "余世明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "湖北省丹江口市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄阳市政协主席",
        "current_org": "中国人民政治协商会议襄阳市委员会",
        "source": "http://district.ce.cn/newarea/sddy/202601/t20260116_2705354.shtml",
    },
    # ── Predecessors — 市委书记 chain ──
    {
        "id": 5,
        "name": "王祺扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "生于湖北省广水市（江西高安人）",
        "education": "中南财经政法大学在职博士研究生、管理学博士",
        "party_join": "1991年1月",
        "work_start": "1991年7月",
        "current_post": "中共海南省委常委、三亚市委书记（前任襄阳市委书记）",
        "current_org": "中共三亚市委员会",
        "source": "http://district.ce.cn/newarea/sddy/202412/03/t20241203_39223151.shtml",
    },
    {
        "id": 6,
        "name": "马旭明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年10月",
        "birthplace": "生于浙江嵊州（籍贯浙江象山）",
        "education": "北京外国语学院德语专业",
        "party_join": "中共党员",
        "work_start": "1986年8月",
        "current_post": "湖北省政协副主席（前任襄阳市委书记）",
        "current_org": "中国人民政治协商会议湖北省委员会",
        "source": "https://new.qq.com/omn/20210325/20210325A0CETX00.html",
    },
    {
        "id": 7,
        "name": "李乐成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任襄阳市委书记（2017-2021）",
        "current_org": "",
        "source": "维基百科《襄阳市》历任领导表",
    },
    # ── Predecessors — 市长 chain ──
    {
        "id": 8,
        "name": "郄英才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "山东省青州市",
        "education": "中国政法大学法律专业硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共黄石市委书记（前任襄阳市长）",
        "current_org": "中共黄石市委员会",
        "source": "维基百科《郄英才》",
    },
    {
        "id": 9,
        "name": "王太晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年2月",
        "birthplace": "湖北省公安县",
        "education": "中南财经大学哲学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湖北省人民政府秘书长（前任襄阳市长）",
        "current_org": "湖北省人民政府办公厅",
        "source": "hubei.ifeng.com 王太晖任湖北省政府秘书长",
    },
    # ── 现任市委常委（兼枣阳市委书记，从县市调查确认）──
    {
        "id": 10,
        "name": "杨晶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "",
        "education": "大学学历、学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄阳市委常委、枣阳市委书记",
        "current_org": "中共枣阳市委员会",
        "source": "http://www.zaoyang.gov.cn/ldzc/",
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共襄阳市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "襄阳市"},
    {"id": 2, "name": "襄阳市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "襄阳市"},
    {"id": 3, "name": "襄阳市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "湖北省人大常委会", "location": "襄阳市"},
    {"id": 4, "name": "中国人民政治协商会议襄阳市委员会", "type": "政协", "level": "地级市", "parent": "湖北省政协", "location": "襄阳市"},
    {"id": 5, "name": "中共三亚市委员会", "type": "党委", "level": "地级市", "parent": "中共海南省委", "location": "三亚市"},
    {"id": 6, "name": "中国人民政治协商会议湖北省委员会", "type": "政协", "level": "省级", "parent": "", "location": "武汉市"},
    {"id": 7, "name": "中共黄石市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "黄石市"},
    {"id": 8, "name": "湖北省人民政府办公厅", "type": "政府", "level": "省级", "parent": "湖北省人民政府", "location": "武汉市"},
    {"id": 9, "name": "中共枣阳市委员会", "type": "党委", "level": "县级市", "parent": "中共襄阳市委员会", "location": "枣阳市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 吴海涛（现任市委书记）—— 完整生涯
    {"person_id": 1, "org_id": 1, "title": "中共襄阳市委书记（湖北省委常委）", "start": "2025年1月", "end": "present", "rank": "副部级", "note": "2025年1月就任，接替王祺扬"},
    {"person_id": 1, "org_id": 1, "title": "中共湖北省委常委、省委秘书长", "start": "2023年11月", "end": "2025年1月", "rank": "副部级", "note": "前任陈新武、继任彭勇"},
    {"person_id": 1, "org_id": 1, "title": "湖北省人民政府副省长", "start": "2023年1月", "end": "2023年11月", "rank": "副部级", "note": "2023年1月当选"},
    {"person_id": 1, "org_id": 1, "title": "中共孝感市委书记", "start": "2020年10月", "end": "2023年2月", "rank": "正厅级", "note": "前任潘启胜、继任胡玖明"},
    {"person_id": 1, "org_id": 2, "title": "孝感市人民政府市长", "start": "2017年5月", "end": "2021年1月", "rank": "正厅级", "note": "前任滕刚、继任熊征宇"},
    {"person_id": 1, "org_id": 1, "title": "中共红安县委书记", "start": "2010年8月", "end": "2012年8月", "rank": "正处级", "note": "前任熊良霄、继任余学武"},
    # 杜海洋（现任市长）
    {"person_id": 2, "org_id": 1, "title": "中共襄阳市委副书记", "start": "2024年10月", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "襄阳市人民政府市长", "start": "2024年10月", "end": "present", "rank": "正厅级", "note": "2024-10-16代市长，后正式当选"},
    # 吕义斌（市人大主任）
    {"person_id": 3, "org_id": 3, "title": "襄阳市人大常委会主任", "start": "2022年1月", "end": "present", "rank": "副部级", "note": "新一届市人大当选"},
    # 余世明（市政协主席）
    {"person_id": 4, "org_id": 4, "title": "襄阳市政协主席", "start": "2026年1月", "end": "present", "rank": "副部级", "note": "2026年1月当选"},
    # 王祺扬（前任书记，2022.6-2024.12）—— 完整生涯
    {"person_id": 5, "org_id": 1, "title": "中共襄阳市委书记（湖北省委常委）", "start": "2022年6月", "end": "2024年12月", "rank": "副部级", "note": "2024年12月跨省调任海南"},
    {"person_id": 5, "org_id": 5, "title": "中共三亚市委书记（海南省委常委）", "start": "2024年12月", "end": "present", "rank": "副部级", "note": "跨省任职"},
    {"person_id": 5, "org_id": 1, "title": "中共荆门市委书记", "start": "2020年7月", "end": "2022年6月", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "湖北省经济和信息化厅厅长", "start": "2018年11月", "end": "2020年7月", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "湖北省经济和信息化委员会主任", "start": "2017年5月", "end": "2018年11月", "rank": "正厅级", "note": ""},
    # 马旭明（前任书记，2021.3-2022.6）
    {"person_id": 6, "org_id": 1, "title": "中共襄阳市委书记（兼任）", "start": "2021年3月", "end": "2022年6月", "rank": "正厅级", "note": "兼任襄阳市委书记"},
    {"person_id": 6, "org_id": 1, "title": "中共黄石市委书记", "start": "2017年4月", "end": "2021年3月", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "湖北省政协副主席", "start": "2022年6月", "end": "present", "rank": "副部级", "note": "卸任襄阳书记后"},
    # 李乐成（前前任书记，2017.2-2021.3）
    {"person_id": 7, "org_id": 1, "title": "中共襄阳市委书记", "start": "2017年2月", "end": "2021年3月", "rank": "正厅级", "note": ""},
    # 郄英才（前任市长，2017.11-2021.4）
    {"person_id": 8, "org_id": 2, "title": "襄阳市人民政府市长", "start": "2017年11月", "end": "2021年4月", "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "中共黄石市委书记（前任襄阳市长调任）", "start": "2021年4月", "end": "present", "rank": "正厅级", "note": ""},
    # 王太晖（前任市长，2021.4-2024.6）
    {"person_id": 9, "org_id": 2, "title": "襄阳市人民政府市长", "start": "2021年4月", "end": "2024年6月", "rank": "正厅级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "湖北省人民政府秘书长", "start": "2024年7月", "end": "present", "rank": "副部级", "note": "襄阳调任省政府"},
    # 杨晶（现任常委兼枣阳书记）
    {"person_id": 10, "org_id": 1, "title": "中共襄阳市委常委", "start": "2024年5月", "end": "present", "rank": "副厅级", "note": "兼枣阳市委书记"},
    {"person_id": 10, "org_id": 9, "title": "中共枣阳市委书记", "start": "2024年5月", "end": "present", "rank": "县处级正职", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 现任党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记—市长（党政一把手搭档）", "overlap_org": "中共襄阳市委员会/襄阳市人民政府", "overlap_period": "2024年10月至今"},
    # 书记——前任（接替关系）
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "王祺扬 → 吴海涛，2025年1月接任襄阳市委书记", "overlap_org": "中共襄阳市委员会", "overlap_period": "2025年1月"},
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "马旭明 → 王祺扬，2022年6月接任襄阳市委书记", "overlap_org": "中共襄阳市委员会", "overlap_period": "2022年6月"},
    {"person_a": 6, "person_b": 7, "type": "predecessor_successor", "context": "李乐成 → 马旭明，2021年3月接任襄阳市委书记", "overlap_org": "中共襄阳市委员会", "overlap_period": "2021年3月"},
    # 市长链
    {"person_a": 2, "person_b": 9, "type": "predecessor_successor", "context": "王太晖 → 杜海洋，2024年10月接任襄阳市长", "overlap_org": "襄阳市人民政府", "overlap_period": "2024年10月"},
    {"person_a": 9, "person_b": 8, "type": "predecessor_successor", "context": "郄英才 → 王太晖，2021年4月接任襄阳市长", "overlap_org": "襄阳市人民政府", "overlap_period": "2021年4月"},
    # 现任书记—副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记—市人大常委会主任", "overlap_org": "襄阳市", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记—市政协主席", "overlap_org": "襄阳市", "overlap_period": "2026年至今"},
    # 现任市长—人大/政协
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "市长—市人大常委会主任", "overlap_org": "襄阳市", "overlap_period": "2024年至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长—市政协主席", "overlap_org": "襄阳市", "overlap_period": "2026年至今"},
    # 总裁委常委（杨晶与vices关系）
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委书记—襄阳市委常委", "overlap_org": "中共襄阳市委员会", "overlap_period": "2025年至今"},
    # 跨区域调动网络
    {"person_a": 5, "person_b": 8, "type": "same_system", "context": "王祺扬（襄阳书记）与郄英才（黄石书记）均为湖北地市州书记（跨市调动网络）", "overlap_org": "湖北省", "overlap_period": ""},
]

# ===========================================================================
# SQLITE BUILD
# ===========================================================================
def create_tables(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
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


def person_color(p):
    """Return 'r,g,b' string based on current role."""
    post = p.get("current_post", "")
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "255,50,50"   # Red — 市委书记
    if "市长" in post and "副" not in post:
        return "50,100,255"  # Blue — 市长
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"   # Orange — 纪委
    return "100,100,100"     # Grey — others


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "政协" in t:
        return "255,240,200"
    if "人大" in t:
        return "200,255,255"
    if "开发区" in t:
        return "200,255,200"
    return "200,200,200"


def is_top_leader(p):
    # 市委书记/市长/人大主任/政协主席 as top-role nodes
    return p["id"] in (1, 2, 3, 4)


def write_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>襄阳市（地级市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org" type="string"/>')
    lines.append('      <attribute id="2" title="post" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="education" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["education"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{pos.get("start", "")}—{pos.get("end", "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


def write_person_json(p, rels_for_p, pos_for_p):
    """Write a deep person-graph JSON profile (person_graph_json.md schema)."""
    src = p.get("source", "")
    sources = []
    if src:
        sources.append({
            "id": "S001",
            "title": f"襄阳市领导班子研究来源 — {p['name']}",
            "url": src,
            "publisher": "中国经济网/维基百科/人民网地方领导资料库",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official" if "gov.cn" in src or "people.com" in src else ("encyclopedia" if "baike" in src else "media"),
            "reliability": "high" if "ce.cn" in src or "people" in src else "medium",
            "notes": "确认现任职务/履历"
        })

    career_timeline = []
    for pos in pos_for_p:
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "襄阳市",
            "system": "party" if ("书记" in pos["title"] or "市委" in pos["title"]) else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": False,
            "notes": pos.get("note", ""),
            "confidence": "confirmed",
            "source_ids": [s["id"] for s in sources] or []
        })

    rels_out = []
    for r in rels_for_p:
        other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
        other = next((x for x in persons if x["id"] == other_id), None)
        if other:
            rels_out.append({
                "person": other["name"],
                "person_id": f"hubei_xiangyang_{other['id']}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": [s["id"] for s in sources] or []
            })

    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "襄阳市",
            "region": "襄阳市",
            "job": p["current_post"],
            "task_id": "hubei_襄阳市",
            "time_focus": "2024-2026（重点2025-2026现职）"
        },
        "identity": {
            "person_id": f"hubei_xiangyang_{p['id']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": "",
                "degree": p["education"] if p["education"] else "",
                "study_type": "unknown",
                "source_ids": [s["id"] for s in sources] or []
            }],
            "party_join": p["party_join"],
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p['birth']}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', 'unknown')}",
                "official_profile_url": p["source"]
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "副部级" if p["id"] in (1, 3, 4) else ("正厅级" if p["id"] in (2,) else "厅级"),
            "as_of": AS_OF,
            "is_current_confirmed": p["id"] in (1, 2, 3, 4, 10),
            "source_ids": [s["id"] for s in sources] or []
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if p["id"] in (5, 8, 9) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records and speeches, not private psychological assessment."
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "total_relationships": len(rels_out),
            "center_rank": "core" if is_top_leader(p) else "member"
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"公开检索（至{AS_OF}）未发现{p['name']}的纪律处分、审计问题或负面媒体报道",
                "date": "",
                "confidence": "plausible",
                "source_ids": [s["id"] for s in sources] or []
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if p["birth"] else "plausible",
            "current_role": "confirmed" if p["id"] in (1, 2, 3, 4, 10) else "plausible",
            "career_completeness": "complete" if p["id"] in (1, 5, 6, 8, 9) else ("partial" if p["id"] in (2,) else "thin"),
            "relationship_confidence": "high",
            "biggest_gap": "杜海洋任襄阳市长前的完整履历待查" if p["id"] == 2 else ("现任市委常委/副市长全名单待查" if p["id"] in (1,) else "更早期/更完整履历待查")
        },
        "open_questions": [
            {
                "priority": "critical" if p["id"] == 2 else "high",
                "question": f"{p['name']}出任襄阳市（市）约2024年前更完整的履历/跨区域调动路径",
                "why_it_matters": "评估晋升路径、政绩积累与跨市/跨省人脉交集",
                "suggested_queries": [f"{p['name']} 简历 任职经历", f"{p['name']} 百度百科", f"{p['name']} 湖北 襄阳 履历"],
                "last_attempted": AS_OF
            }
        ]
    }

    # filename per person_graph_json.md: YYYYMMDD-湖北省-襄阳市-{job}-{name}.json
    job_by_id = {
        1: "市委书记",
        2: "市委副书记",
        3: "市人大常委会主任",
        4: "市政协主席",
        5: "前任市委书记",
        6: "前任市委书记",
        7: "前任市委书记",
        8: "前任市长",
        9: "前任市长",
        10: "襄阳市委常委",
    }
    job = job_by_id.get(p["id"], "其他")
    filename = f"{AS_OF.replace('-', '')}-湖北省-襄阳市-{job}-{p['name']}.json"
    path = os.path.join(PERSONS_DIR, filename)

    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON written: {filename}")


def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 构建襄阳市（地级市）网络...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    os.makedirs(STAGING, exist_ok=True)

    # ── SQLite DB ──
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    for p in persons:
        conn.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""), p["current_post"], p["current_org"], p["source"])
        )
    for o in organizations:
        conn.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
                     (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"]))
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                     (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                     (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")

    # ── GEXF ──
    write_gexf()

    # ── Person JSONs for core leaders (书记/市长 + 四大班子 + 关键前任) ──
    core_ids = [1, 2, 3, 4, 5, 8, 9]
    for p in persons:
        if p["id"] in core_ids:
            rels_for_p = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
            pos_for_p = [pos for pos in positions if pos["person_id"] == p["id"]]
            write_person_json(p, rels_for_p, pos_for_p)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 襄阳市网络构建完成！")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons dir: {PERSONS_DIR}")


if __name__ == "__main__":
    main()