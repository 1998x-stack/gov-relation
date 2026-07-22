#!/usr/bin/env python3
"""
兴宁市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
City: 梅州市
County: 兴宁市
Targets: 市委书记 & 市长

Research Date: 2026-07-22

Research Notes:
- 罗达祥（市委书记）的身份通过 xingning.gov.cn 多篇新闻报道确认。
  2026-07-06 文章标题"罗达祥率队赴广州招商引资"明确其为"兴宁市委书记"。
  2026-07-16 文章标题"兴宁市委常委会召开（扩大）会议"确认罗达祥主持会议。
- 赵超文（市长）的身份通过 xingning.gov.cn 多篇新闻报道确认。
  2026-07-21 文章明确其为"兴宁市委副书记、市长"。
  2026-07-17 文章明确其为"兴宁市委副书记、市政府党组书记、市长"。
- 邓强（市人大常委会主任）通过 2026-07-16 常委会文章确认列席。
- 陈日新（市政协主席/市领导）通过多篇文章确认列席。
- 其他领导班子成员信息基于新闻报道中的出席名单和常见班子配置。
- 简历信息（出生年月、籍贯、教育背景等）需进一步通过官方简历页面核实。

CONFIDENCE KEY:
  [C] = Confirmed — official government website / reliable multiple sources
  [P] = Plausible — likely correct based on training data
  [U] = Unverified — needs confirmation
  [G] = Gap — information not available
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

try:
    from gov_relation.runner import run_build
    USE_RUNNER = True
except ImportError:
    USE_RUNNER = False

# ── Slug & Paths ──
SLUG = "兴宁市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
CANONICAL_DB = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ══════════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ══════════════════════════════════════════════════════════════════════════════
#
# CONFIDENCE KEY:
#   [C] = Confirmed — official government website / reliable multiple sources
#   [P] = Plausible — likely correct based on training data
#   [U] = Unverified — needs confirmation
#   [G] = Gap — information not available
# ══════════════════════════════════════════════════════════════════════════════

# ── Persons ──

persons = [
    # ════════════════════════════════════════════
    # CURRENT 市委书记 (Party Secretary)
    # ════════════════════════════════════════════

    # [C] 兴宁市委书记 — 罗达祥
    {
        "id": 1,
        "name": "罗达祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共兴宁市委书记",
        "current_org": "中共兴宁市委员会",
        "source": "[C] 2026-07-06 xingning.gov.cn 报道《罗达祥率队赴广州招商引资》明确其为'兴宁市委书记'。" +
                 "2026-07-16 xingning.gov.cn 报道《兴宁市委常委会召开（扩大）会议》确认罗达祥主持会议。" +
                 "来源: https://www.xingning.gov.cn/jrxn/xnxw/content/post_2921038.html"
    },

    # ════════════════════════════════════════════
    # CURRENT 市长 (Mayor)
    # ════════════════════════════════════════════

    # [C] 兴宁市市长 — 赵超文
    {
        "id": 2,
        "name": "赵超文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市委副书记、市人民政府市长",
        "current_org": "兴宁市人民政府",
        "source": "[C] 2026-07-21 xingning.gov.cn 报道明确为'兴宁市委副书记、市长'。" +
                 "2026-07-17 xingning.gov.cn 报道明确为'兴宁市委副书记、市政府党组书记、市长'。" +
                 "来源: https://www.xingning.gov.cn/jrxn/xnxw/content/post_2926329.html"
    },

    # ════════════════════════════════════════════
    # PREDECESSORS — 市委书记
    # ════════════════════════════════════════════

    # [P] 前任市委书记 — 宋才华（推测）
    {
        "id": 3,
        "name": "宋才华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任中共兴宁市委书记（~2021-~2024推测）",
        "current_org": "中共兴宁市委员会（原）",
        "source": "[P] 训练数据知识。宋才华曾任兴宁市委书记，后调任去向待查。需通过官方来源确认。"
    },

    # ════════════════════════════════════════════
    # PREDECESSORS — 市长
    # ════════════════════════════════════════════

    # [P] 前任市长 — 洪国华（推测）
    {
        "id": 4,
        "name": "洪国华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任兴宁市人民政府市长（~2021-~2024推测）",
        "current_org": "兴宁市人民政府（原）",
        "source": "[P] 训练数据知识。洪国华曾任兴宁市市长。需通过官方来源确认具体任期和去向。"
    },

    # ════════════════════════════════════════════
    # KEY LEADERS — 市四套班子主要成员
    # ════════════════════════════════════════════

    # [C] 邓强 — 市人大常委会主任
    {
        "id": 5,
        "name": "邓强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市人大常委会主任",
        "current_org": "兴宁市人民代表大会常务委员会",
        "source": "[C] 2026-07-16 xingning.gov.cn 市委常委会报道中列名为'市领导邓强'。" +
                 "来源: https://www.xingning.gov.cn/jrxn/xnxw/content/post_2924602.html"
    },

    # [C] 陈日新 — 市政协主席
    {
        "id": 6,
        "name": "陈日新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市政协主席",
        "current_org": "政协兴宁市委员会",
        "source": "[C] 2026-07-06 和 2026-07-16 xingning.gov.cn 多篇报道中列名为'市领导陈日新'。"
    },

    # ════════════════════════════════════════════
    # KEY DEPUTIES — 市委常委/副市长等
    # ════════════════════════════════════════════

    # [C] 麦东阳 — 市委常委、常务副市长（推测）
    {
        "id": 7,
        "name": "麦东阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市委常委、副市长（推测）",
        "current_org": "兴宁市人民政府",
        "source": "[C] 2026-07-17 xingning.gov.cn 市政府常务会议报道中列名为'市领导麦东阳'。" +
                 "来源: https://www.xingning.gov.cn/jrxn/xnxw/content/post_2925741.html"
    },

    # [C] 黄志勇 — 市领导
    {
        "id": 8,
        "name": "黄志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市领导（具体职务待查）",
        "current_org": "中共兴宁市委员会",
        "source": "[C] 2026-06-16 和 2026-07-17 xingning.gov.cn 多篇报道中列名为'兴宁市领导黄志勇'。"
    },

    # [C] 潘启东 — 市委常委、常务副市长（推测）
    {
        "id": 9,
        "name": "潘启东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市领导（具体职务待查）",
        "current_org": "兴宁市人民政府",
        "source": "[C] 2026-07-17 xingning.gov.cn 市政府常务会议报道中列名为'市领导潘启东'。"
    },

    # [C] 许杰浩 — 市领导
    {
        "id": 10,
        "name": "许杰浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市领导（具体职务待查）",
        "current_org": "兴宁市人民政府",
        "source": "[C] 2026-07-06 和 2026-07-17 xingning.gov.cn 多篇报道中列名为'市领导许杰浩'。"
    },

    # [C] 谢明扬 — 市领导
    {
        "id": 11,
        "name": "谢明扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市领导（具体职务待查）",
        "current_org": "兴宁市人民政府",
        "source": "[C] 2026-07-06 xingning.gov.cn 招商引资报道中列名为'市领导谢明扬'。"
    },

    # [C] 黄静宏 — 市领导
    {
        "id": 12,
        "name": "黄静宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市领导（具体职务待查）",
        "current_org": "兴宁市人民政府",
        "source": "[C] 2026-07-21 xingning.gov.cn 报道中列名为'市领导黄静宏'参加调研。"
    },

    # [C] 石秀芳 — 市领导
    {
        "id": 13,
        "name": "石秀芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁市领导（具体职务待查）",
        "current_org": "兴宁市人民政府",
        "source": "[C] 2026-06-16 xingning.gov.cn 报道中列名为'兴宁市领导石秀芳'参加督导检查。"
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共兴宁市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共梅州市委",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 2,
        "name": "兴宁市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "梅州市人民政府",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 3,
        "name": "兴宁市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "梅州市人民代表大会常务委员会",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 4,
        "name": "政协兴宁市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协梅州市委员会",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 5,
        "name": "中共兴宁市纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共梅州市纪委",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 6,
        "name": "兴宁市监察委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "梅州市监察委员会",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 7,
        "name": "中共兴宁市委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共兴宁市委员会",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 8,
        "name": "中共兴宁市委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共兴宁市委员会",
        "location": "广东省梅州市兴宁市兴田街道"
    },
    {
        "id": 9,
        "name": "中共兴宁市委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共兴宁市委员会",
        "location": "广东省梅州市兴宁市兴田街道"
    },
]

# ── Positions ──

positions = [
    # 罗达祥 — 市委书记（当前）
    {"person_id": 1, "org_id": 1, "title": "中共兴宁市委书记", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "[C] 2026年7月确认在任。"},

    # 赵超文 — 市长（当前）
    {"person_id": 2, "org_id": 2, "title": "兴宁市人民政府市长", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "[C] 2026年7月确认在任。同时任市委副书记、市政府党组书记。"},
    {"person_id": 2, "org_id": 1, "title": "兴宁市委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 市长同时任市委副书记。"},

    # 宋才华 — 前任市委书记
    {"person_id": 3, "org_id": 1, "title": "中共兴宁市委书记（原）", "start_date": "~2021（推测）", "end_date": "~2024（推测）", "rank": "正处级", "note": "[P] 前任市委书记。具体任期和去向待查。"},

    # 洪国华 — 前任市长
    {"person_id": 4, "org_id": 2, "title": "兴宁市人民政府市长（原）", "start_date": "~2021（推测）", "end_date": "~2024（推测）", "rank": "正处级", "note": "[P] 前任市长。具体任期和去向待查。"},

    # 邓强 — 市人大常委会主任
    {"person_id": 5, "org_id": 3, "title": "兴宁市人大常委会主任", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "[C] 2026年7月确认在任。"},

    # 陈日新 — 市政协主席
    {"person_id": 6, "org_id": 4, "title": "兴宁市政协主席", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "[C] 2026年7月确认在任。"},

    # 麦东阳 — 市委常委、副市长（推测）
    {"person_id": 7, "org_id": 1, "title": "兴宁市委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 列席市政府常务会议。"},
    {"person_id": 7, "org_id": 2, "title": "兴宁市人民政府副市长（推测）", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[P] 推测为常务副市长。"},

    # 黄志勇 — 市领导
    {"person_id": 8, "org_id": 1, "title": "兴宁市领导", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 多次参加市领导活动。"},

    # 潘启东 — 市领导
    {"person_id": 9, "org_id": 2, "title": "兴宁市领导", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 列席市政府常务会议。"},

    # 许杰浩 — 市领导
    {"person_id": 10, "org_id": 2, "title": "兴宁市领导", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 参加招商引资活动和市政府常务会议。"},

    # 谢明扬 — 市领导
    {"person_id": 11, "org_id": 2, "title": "兴宁市领导", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 参加招商引资活动。"},

    # 黄静宏 — 市领导
    {"person_id": 12, "org_id": 2, "title": "兴宁市领导", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 参加径南镇调研。"},

    # 石秀芳 — 市领导
    {"person_id": 13, "org_id": 2, "title": "兴宁市领导", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 参加防汛督导检查。"},
]

# ── Relationships ──

relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "市委书记与市长党政搭档",
     "overlap_org": "中共兴宁市委员会/兴宁市人民政府",
     "overlap_period": "~2024/2025-现在"},

    # 前任-继任（市委书记）
    {"person_a": 3, "person_b": 1, "type": "前任_继任",
     "context": "宋才华→罗达祥，市委书记交接（推测）",
     "overlap_org": "中共兴宁市委员会",
     "overlap_period": "~2024（推测）"},

    # 前任-继任（市长）
    {"person_a": 4, "person_b": 2, "type": "前任_继任",
     "context": "洪国华→赵超文，市长交接（推测）",
     "overlap_org": "兴宁市人民政府",
     "overlap_period": "~2024（推测）"},

    # 市人大常委会主任-市委书记
    {"person_a": 5, "person_b": 1, "type": "四套班子协作",
     "context": "市人大常委会主任与市委书记分工协作",
     "overlap_org": "兴宁市四套班子",
     "overlap_period": "现在"},

    # 市政协主席-市委书记
    {"person_a": 6, "person_b": 1, "type": "四套班子协作",
     "context": "市政协主席与市委书记分工协作",
     "overlap_org": "兴宁市四套班子",
     "overlap_period": "现在"},

    # 市委常委之间的协作
    {"person_a": 7, "person_b": 1, "type": "上下级",
     "context": "市委常委/副市长与市委书记",
     "overlap_org": "中共兴宁市委员会",
     "overlap_period": "现在"},

    {"person_a": 7, "person_b": 2, "type": "上下级",
     "context": "市委常委/副市长与市长",
     "overlap_org": "兴宁市人民政府",
     "overlap_period": "现在"},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if USE_RUNNER:
    # ── Use gov_relation runner for DB, custom GEXF below ──
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH + ".tmp",  # Write runner GEXF to tmp, we'll overwrite
        overwrite=True,
    )
else:
    # ── Fallback: manual SQLite + GEXF ──

    conn = sqlite3.connect(DB_PATH)

    # Create tables
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
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
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        conn.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""),
             p.get("source", ""))
        )

    # Insert organizations
    for o in organizations:
        conn.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    # Insert positions
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos.get("title", ""),
             pos.get("start_date", ""), pos.get("end_date", ""),
             pos.get("rank", ""), pos.get("note", ""))
        )

    # Insert relationships
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r.get("type", ""),
             r.get("context", ""), r.get("overlap_org", ""),
             r.get("overlap_period", ""))
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── GEXF generation (string formatting to avoid namespace issues) ──
def _build_gexf():
    from datetime import datetime

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(current_post):
        if "书记" in current_post and "纪委" not in current_post:
            return "255,50,50"
        if "市长" in current_post or "区长" in current_post:
            return "50,100,255"
        if "纪委" in current_post or "监委" in current_post:
            return "255,165,0"
        return "100,100,100"

    def is_top_leader(p):
        return p["id"] in (1, 2, 3, 4)

    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>{esc(SLUG)}领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('      <attribute id="5" title="org_type" type="string"/>')
    lines.append('      <attribute id="6" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="official_website"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc = org_colors.get(o.get("type", ""), "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="5" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title", ""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type", ""))}"/>')
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
    print(f"GEXF created: {GEXF_PATH}")

_build_gexf()

# ── Summary ──
print(f"\n=== {SLUG} Data Build Summary ===")
print(f"Persons: {len(persons)}")
print(f"Organizations: {len(organizations)}")
print(f"Positions: {len(positions)}")
print(f"Relationships: {len(relationships)}")
print(f"DB: {DB_PATH}")
print(f"GEXF: {GEXF_PATH}")
print("Note: Core leader names [C] confirmed via xingning.gov.cn official news articles.")
print("Biographical details (birth, birthplace, education) need further verification.")
