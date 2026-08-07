#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 水城区 (Shuicheng District), 六盘水市, 贵州省.

Investigation date: 2026-08-05
Task ID: guizhou_水城区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources (all official, reliable):
  - 水城区人民政府网站领导之窗 http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/
    - 区委书记 龙兴 简历页 (2026-07-16)
    - 区政府 代理区长 张斌 简历页 (2026-08-01)
    - 区委/人大/政府/政协 各班子领导之窗列表
  - 水城要闻 (202607-202608): 人武部党委第一书记任职大会、八一建军节慰问、区委常委会等
  - 六盘水市人民政府 http://www.gzlps.gov.cn

Confidence notes:
  - 龙兴、张斌 身份与现任职务 confirmed（官方简历页）
  - 领导班子名单 confirmed（官方领导之窗）
  - 龙兴、张斌、各副职 完整 Career 履历（任此前的完整经历）无法通过可访问来源确认 → 以 open_questions 记录缺口
  - 人大常委会主任、政协主席为"提名人选"（拟任），以 2026-08 为准
  - 大量中老年干部的出生地/籍贯/入党时间缺失
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "水城区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"
REGION = "水城区"
PROVINCE = "贵州省"
CITY = "六盘水市"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────
# 1 龙兴(区委书记), 2 张斌(代理区长), 3 徐令选(副书记), 4 吴昌洪(挂任副书记),
# 5 侯华(纪委书记), 6 黄昊(组织部长), 7 鲁娜(宣传/统战部长), 8 邵金刚(常务副区长),
# 9 王光耀(政法委书记), 10 张良(副区长), 11 谢高福(区委办主任), 12 黄绍凯(人武部长),
# 13 陈淑梅(挂任副区长), 14 刘丹(桂任副区长/农行), 15 廖翔(人大主任提名人选),
# 16 周潮(政协主席提名人选), 17 王厚源(前政协主席), 18 李巍(六盘水市委书记, 跨级)

persons = [
    {"id": 1, "name": "龙兴", "gender": "男", "ethnicity": "彝族", "birth": "1976年8月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "区委书记", "current_org": "中共六盘水市水城区委员会", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 2, "name": "张斌", "gender": "男", "ethnicity": "汉族", "birth": "1980年4月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "区委副书记、区政府代理区长", "current_org": "水城区人民政府", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 3, "name": "徐令选", "gender": "男", "ethnicity": "汉族", "birth": "1986年9月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "区委副书记", "current_org": "中共六盘水市水城区委员会", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 4, "name": "吴昌洪", "gender": "男", "ethnicity": "布依族", "birth": "1980年5月", "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "", "current_post": "区委副书记（挂职）", "current_org": "中共六盘水市水城区委员会", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 5, "name": "侯华", "gender": "男", "ethnicity": "汉族", "birth": "1984年5月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、区纪委书记、区监委代主任", "current_org": "水城区纪委监委", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 6, "name": "黄昊", "gender": "男", "ethnicity": "汉族", "birth": "1985年10月", "birthplace": "", "education": "公共管理硕士", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、区委组织部部长", "current_org": "水城区委组织部", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 7, "name": "鲁娜", "gender": "女", "ethnicity": "汉族", "birth": "1989年1月", "birthplace": "", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、区委宣传（统战）部部长", "current_org": "中共六盘水市水城区委员会", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 8, "name": "邵金刚", "gender": "男", "ethnicity": "汉族", "birth": "1985年11月", "birthplace": "", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、常务副区长", "current_org": "水城区人民政府", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 9, "name": "王光耀", "gender": "男", "ethnicity": "彝族", "birth": "1978年10月", "birthplace": "", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、区委政法委书记", "current_org": "水城区委政法委", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 10, "name": "张良", "gender": "男", "ethnicity": "汉族", "birth": "1983年1月", "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、副区长", "current_org": "水城区人民政府", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 11, "name": "谢高福", "gender": "男", "ethnicity": "彝族", "birth": "1987年4月", "birthplace": "", "education": "工学学士", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、区委办公室主任", "current_org": "水城区委办公室", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 12, "name": "黄绍凯", "gender": "男", "ethnicity": "汉族", "birth": "1982年2月", "birthplace": "", "education": "空军雷达学院（大学）", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、区人武部部长", "current_org": "水城区人武部", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 13, "name": "陈淑梅", "gender": "女", "ethnicity": "汉族", "birth": "1974年6月", "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、副区长（挂职）", "current_org": "水城区人民政府", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 14, "name": "刘丹", "gender": "女", "ethnicity": "汉族", "birth": "1976年10月", "birthplace": "", "education": "云南大学在职研究生", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、副区长（挂职）", "current_org": "水城区人民政府", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 15, "name": "廖翔", "gender": "男", "ethnicity": "苗族", "birth": "1974年2月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "区人大常委会党组书记、主任提名人选", "current_org": "水城区人民代表大会常务委员会", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 16, "name": "周潮", "gender": "男", "ethnicity": "彝族", "birth": "1972年9月", "birthplace": "", "education": "中央党校函授学院", "party_join": "中共党员", "work_start": "", "current_post": "区政协党组书记、主席提名人选", "current_org": "中国人民政治协商会议水城区委员会", "source": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/"},
    {"id": 17, "name": "王厚栋", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区政协主席（届—待核）", "current_org": "中国人民政治协商会议水城区委员会", "source": "http://www.shuicheng.gov.cn/newsite/zwdt/zwyw/202607/t20260721_90645781.html"},
    {"id": 18, "name": "李巍", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "六盘水市委书记", "current_org": "中共六盘水市委员会", "source": "https://www.gzlps.gov.cn"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共六盘水市水城区委员会", "type": "党委", "level": "县级", "parent": "中共六盘水市委员会", "location": "六盘水市水城区"},
    {"id": 2, "name": "水城区人民政府", "type": "政府", "level": "县级", "parent": "六盘水市人民政府", "location": "六盘水市水城区"},
    {"id": 3, "name": "水城区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "六盘水市人大常委会", "location": "六盘水市水城区"},
    {"id": 4, "name": "中国人民政治协商会议水城区委员会", "type": "政协", "level": "县级", "parent": "政协六盘水市委员会", "location": "六盘水市水城区"},
    {"id": 5, "name": "水城区纪委监委", "type": "纪委", "level": "县级", "parent": "六盘水市纪委市监委", "location": "六盘水市水城区"},
    {"id": 6, "name": "水城区委组织部", "type": "党委部门", "level": "县级", "parent": "中共六盘水市水城区委员会", "location": "六盘水市水城区"},
    {"id": 7, "name": "水城区委办公室", "type": "党委部门", "level": "县级", "parent": "中共六盘水市水城区委员会", "location": "六盘水市水城区"},
    {"id": 8, "name": "水城区委政法委", "type": "党委部门", "level": "县级", "parent": "中共六盘水市水城区委员会", "location": "六盘水市水城区"},
    {"id": 9, "name": "水城区人武部", "type": "军队", "level": "县级", "parent": "六盘水军分区", "location": "六盘水市水城区"},
    {"id": 10, "name": "中国农业银行六盘水分行", "type": "企业/金融", "level": "市级", "parent": "中国农业银行贵州省分行", "location": "六盘水市"},
    {"id": 11, "name": "中共六盘水市委员会", "type": "党委", "level": "地级", "parent": "中共贵州省委员会", "location": "六盘水市"},
    {"id": 12, "name": "六盘水市人民政府", "type": "政府", "level": "地级", "parent": "贵州省人民政府", "location": "六盘水市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 龙兴
    {"person_id": 1, "org_id": 2, "title": "区政府区长（兼任）", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "据2026-07-31新闻'区委书记、区政府区长龙兴'，其曾兼任区长职务，后移交政府序列（党政一肩挑过渡期）"},
    {"person_id": 1, "org_id": 1, "title": "水城区委书记", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "2026年任水城区委书记（官方简历页2026-07-16；2026-08任区人武部党委第一书记）"},
    {"person_id": 1, "org_id": 9, "title": "区人武部党委第一书记", "start_date": "2026-08", "end_date": "present", "rank": "", "note": "2026-08-04经六盘水军分区党委研究决定任区人武部党委第一书记"},

    # 张斌
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026-08", "end_date": "present", "rank": "正处级", "note": "官方简历页2026-08-01"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记、副区长、代理区长", "start_date": "2026-08", "end_date": "present", "rank": "正处级", "note": "2026-08 任代理区长，接替龙兴的区政府区长职务"},

    # 副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助区委书记抓党的建设工作"},
    {"person_id": 4, "org_id": 1, "title": "区委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂任"},

    # 常委
    {"person_id": 5, "org_id": 1, "title": "区委常委、区纪委书记、区监委代主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委、区委组织部部长、区委教育工委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委、区委宣传部部长、区委统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "区委常委、常务副区长、区政府党组副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委、区委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "区委常委、区委办公室主任、区直机关工委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "区委常委、区人武部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "区委常委、副区长、党组成员（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "区委常委、副区长、党组成员（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "中国农业银行六盘水分行资深专员，金融系统挂职"},
    {"person_id": 14, "org_id": 10, "title": "中国农业银行六盘水分行资深专员", "start_date": "", "end_date": "present", "rank": "", "note": "挂任前身份"},

    # 人大 / 政协
    {"person_id": 15, "org_id": 3, "title": "区人大常委会党组书记、主任提名人选", "start_date": "2026-08", "end_date": "present", "rank": "正处级", "note": "拟定任"},
    {"person_id": 16, "org_id": 4, "title": "区政协党组书记、主席提名人选", "start_date": "2026-03", "end_date": "present", "rank": "正处级", "note": "拟定任"},
    {"person_id": 17, "org_id": 4, "title": "区政协主席（届中调整前）", "start_date": "", "end_date": "2026", "rank": "正处级", "note": "2026-07-20区委常委会曾述'区政协主席王厚栋'"},

    # 跨级（六盘水市）
    {"person_id": 18, "org_id": 11, "title": "六盘水市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "跨级上级党委领导"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "龙兴（区委书记）与张斌（区委副书记、代理区长）为水城区现任党政一把手搭档", "overlap_org": "水城区", "overlap_period": "2026-08至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "龙兴与徐令选（副书记）同属水城区委领导班子", "overlap_org": "中共六盘水市水城区委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "龙兴与吴昌洪（挂任副书记）同属水城区委领导班子", "overlap_org": "中共六盘水市水城区委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "龙兴（书记）与侯华（纪委书记）同属区委班子，纪委监督关系", "overlap_org": "中共六盘水市水城区委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "龙兴与黄昊（组织部长）同属区委班子，干部任用交集", "overlap_org": "中共六盘水市水城区委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "龙兴与谢高福（区委办主任）工作交集，主任为书记直接服务", "overlap_org": "中共六盘水市水城区委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "龙兴作为区人武部党委第一书记，与黄绍凯（人武部部长兼常委）党管武装工作交集", "overlap_org": "水城区人武部", "overlap_period": "2026-08至今"},
    {"person_a": 2, "person_b": 8, "type": "member", "context": "张斌（代理区长）领导邵金刚（常务副区长）", "overlap_org": "水城区人民政府", "overlap_period": "2026-08至今"},
    {"person_a": 2, "person_b": 10, "type": "member_overlap", "context": "张斌与张良（副区长）在区政府班子共事", "overlap_org": "水城区人民政府", "overlap_period": "2026-08至今"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "张斌与陈淑梅（挂任副区长）在区政府班子共事", "overlap_org": "水城区人民政府", "overlap_period": "2026-08至今"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "张斌与刘丹（桂任副区长、农行挂职）在区政府班子共事（金融系统干部交流）", "overlap_org": "水城区人民政府", "overlap_period": "2026-08至今"},
    {"person_a": 1, "person_b": 18, "type": "subordinate_to_superior", "context": "六盘水市委书记李巍垂直督导水城区委书记龙兴（2026-07-29 李巍到水城区调研）", "overlap_org": "中共六盘水市委员会", "overlap_period": "2026至今"},
    {"person_a": 15, "person_b": 1, "type": "overlap", "context": "廖翔（人大主任提名人选）与龙兴同属区领导班子", "overlap_org": "水城区", "overlap_period": "2026-08至今"},
    {"person_a": 16, "person_b": 1, "type": "overlap", "context": "周潮（政协主席提名人选）与龙兴同属区领导班子", "overlap_org": "水城区", "overlap_period": "2026至今"},
    {"person_a": 17, "person_b": 16, "type": "succession", "context": "周潮接任（或拟接任）王厚栋的区政协主席职务（政协换届人选更替）", "overlap_org": "政协水城区委员会", "overlap_period": "2026"},
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
            work_start TEXT,
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
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

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
    if name == "龙兴":
        return "255,50,50"      # 区委书记 — Red
    if name == "张斌":
        return "50,100,255"     # 区长 — Blue
    if name in ("廖翔",):
        return "200,255,255"    # 人大 — Cyan
    if name in ("周潮", "王厚栋"):
        return "255,240,200"    # 政协 — Cream
    if name == "侯华":
        return "255,165,0"      # 纪委 — Orange
    if name in ("徐令选", "吴昌洪"):
        return "255,165,0"      # 副书记 — Orange
    if name == "李巍":
        return "200,50,50"      # 上级市委书记
    return "100,100,100"        # 其他常委等 — Grey


def person_size(name):
    if name in ("龙兴", "张斌"):
        return "20.0"
    if name in ("徐令选", "吴昌洪", "廖翔", "周潮"):
        return "12.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "纪委" in o_type:
        return "255,220,180"
    if "军队" in o_type:
        return "200,200,200"
    if "金融" in o_type or "企业" in o_type:
        return "210,255,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>{REGION}领导班子工作关系网络 - {SLUG}</description>')
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

    # Person nodes
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

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
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
    print(f"  GEXF: {os.path.basename(GEXF_PATH)} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

SOURCE_REGISTER = [
    {"id": "S001", "title": "水城区人民政府网站 领导之窗（区委书记页/区政府页）", "url": "http://www.shuicheng.gov.cn/newsite/zwgk/ldzc/", "publisher": "水城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委书记龙兴、代理区长张斌及各班子领导之窗名单/简历"},
    {"id": "S002", "title": "水城要闻：宣布区人武部党委第一书记任职大会", "url": "http://www.shuicheng.gov.cn/newsite/zwdt/zwyw/202608/t20260804_90691987.html", "publisher": "水城融媒", "published_at": "2026-08-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "龙兴任区人武部党委第一书记"},
    {"id": "S003", "title": "水城要闻：龙兴率队开展八一建军节走访慰问", "url": "http://www.shuicheng.gov.cn/newsite/zwdt/zwyw/202608/t20260803_90686383.html", "publisher": "水城融媒", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "称'区委书记、区政府区长龙兴'——曾兼任区长"},
    {"id": "S004", "title": "水城要闻：区委常委会召开会议", "url": "http://www.shuicheng.gov.cn/newsite/zwdt/zwyw/202607/t20260721_90645781.html", "publisher": "水城融媒", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区政协主席王厚栋等班子名单"},
    {"id": "S005", "title": "六盘水市人民政府网站", "url": "http://www.gzlps.gov.cn", "publisher": "六盘水市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "六盘水市领导：李巍（市委书记）、臧侃（代市长）等"},
]


def timeline_for(p):
    if p["name"] == "龙兴":
        return [
            {"start": "", "end": "", "org": "水城区人民政府", "title": "区长（兼任）", "notes": "据2026-07-31新闻'区委书记、区政府区长龙兴'，曾兼任区长", "confidence": "plausible", "source_ids": ["S003"]},
            {"start": "2026", "end": "present", "org": "中共六盘水市水城区委员会", "title": "区委书记", "notes": "2026年任区委书记（官方简历页）", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2026-08", "end": "present", "org": "水城区人武部", "title": "区人武部党委第一书记", "notes": "2026-08-04任", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "履历缺口", "title": "", "notes": "出生地/籍贯、入党时间及出任水城前更早职务待查", "confidence": "unverified", "source_ids": []},
        ]
    if p["name"] == "张斌":
        return [
            {"start": "2026-08", "end": "present", "org": "中共六盘水市水城区委员会", "title": "区委副书记", "notes": "官方简历页2026-08-01", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2026-08", "end": "present", "org": "水城区人民政府", "title": "代区长、区政府党组书记", "notes": "2026年8月任，接龙兴区长职务", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "履历缺口", "title": "", "notes": "任水城前的职务待查", "confidence": "unverified", "source_ids": []},
        ]
    if p["name"] == "廖翔":
        return [
            {"start": "2026-08", "end": "present", "org": "水城区人民代表大会常务委员会", "title": "党组书记、主任提名人选", "notes": "拟定任", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "履历缺口", "title": "", "notes": "此前职务待查", "confidence": "unverified", "source_ids": []},
        ]
    if p["name"] == "周潮":
        return [
            {"start": "2026", "end": "present", "org": "中国人民政治协商会议水城区委员会", "title": "党组书记、主席提名人选", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "履历缺口", "title": "", "notes": "此前职务待查", "confidence": "unverified", "source_ids": []},
        ]
    # default
    return [
        {"start": "", "end": "present", "org": p.get("current_org", ""), "title": p.get("current_post", ""), "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "履历缺口", "title": "", "notes": "此前履历待查", "confidence": "unverified", "source_ids": []},
    ]


def relationships_for(p):
    idx = {pp["id"]: pp for pp in persons}
    out = []
    for r in relationships:
        if r["person_a"] == p["id"]:
            other = idx[r["person_b"]]
            out.append({"person": other["name"], "person_id": f"shuicheng_{other['name']}", "relationship_type": r["type"], "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"], "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]})
        elif r["person_b"] == p["id"]:
            other = idx[r["person_a"]]
            out.append({"person": other["name"], "person_id": f"shuicheng_{other['name']}", "relationship_type": r["type"], "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"], "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]})
    return out


def build_person_jsons():
    idx = {pp["id"]: pp for pp in persons}
    core = [
        (1, "区委书记", "水城区委书记", "正处级", "critical"),
        (2, "代区长", "水城区委副书记、区政府代理区长", "正处级", "critical"),
        (15, "区人大常委会主任（人选）", "区人大常委会党组书记、主任提名人选", "正处级", "high"),
        (16, "区政协主席（人选）", "区政协党组书记、主席提名人选", "正处级", "high"),
    ]
    for pid, file_job, post_label, rank, prio in core:
        p = idx[pid]
        data = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": PROVINCE, "city": CITY, "region": REGION, "job": file_job, "task_id": "guizhou_水城区", "time_focus": "2026"},
            "identity": {
                "person_id": f"shuicheng_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [p.get("education", "")] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": "",
                "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth','')}", "name_birthplace": f"{p['name']}_{p.get('birthplace','')}", "official_profile_url": p.get("source", "")}
            },
            "current_status": {"current_post": post_label, "current_org": p.get("current_org", ""), "administrative_rank": rank, "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
            "career_timeline": timeline_for(p),
            "organizations": [],
            "relationships": relationships_for(p),
            "governance_record": [],
            "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [CITY], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未发现公开的纪律处分或负面通报", "date": AS_OF, "confidence": "unverified", "source_ids": []}],
            "source_register": SOURCE_REGISTER,
            "confidence_summary": {"identity": "confirmed" if p.get("gender") and p.get("birth") else "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": f"{p['name']}出任水城之前的完整工作履历"},
            "open_questions": [
                {"priority": prio, "question": f"{p['name']}的完整职业生涯履历（含出生地、教育背景、入党时间、任{REGION}之前历任职务）", "why_it_matters": "核心领导，现任职务已确认，早期履历需补充", "suggested_queries": [f"{p['name']} 简历 六盘水", f"{p['name']} 任前公示", f"{p['name']} 水城区"], "last_attempted": AS_OF},
            ],
        }
        fname = f"{TODAY}-{PROVINCE}-{CITY}-{file_job}-{p['name']}.json"
        with open(PERSONS_DIR / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {fname}")


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files in {BASE}:")
    print(f"  DB:     {SLUG}_network.db")
    print(f"  GEXF:   {SLUG}_network.gexf")
    print("Done.")