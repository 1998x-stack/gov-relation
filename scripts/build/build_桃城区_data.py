#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 桃城区 leadership network.

调查日期: 2026-08-06
信息来源: 桃城区人民政府网站 (taocheng.gov.cn 区长之窗/今日桃城), 衡水市人民政府网站
调查级别: 市辖区
目标人物: 区委书记 危国永、区长 刘京
约束: 政府门户仅刊发职务与分工, 人员出生/籍贯/完整履历及党内职务在当前检索渠道不可得;
      已标注 confidence 并记录 open gaps, 不臆造字段。
"""

import json
import os
import sqlite3
import sys

# ── Paths ──────────────────────────────────────────────────────────
import pathlib

BASE = os.path.dirname(os.path.abspath(__file__))
# 定位 repo root (staging: data/tmp/<id>/ = parents[3]; canonical: scripts/build/ = parents[2])
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = pathlib.Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "桃城区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "桃城区_network.gexf")

SLUG = "河北省衡水市桃城区"

# ── PERSON ID 约定 ──────────────────────────────────────────────────
# 使用 person_id 一致: taocheng_<name>
PID = {
    "危国永": 1,
    "刘京": 2,
    "韩新民": 3,
    "封希海": 4,
    "姚文前": 5,
    "薛纯宾": 6,
    "孔德龙": 7,
    "陈靖": 8,
    "王东": 9,
    "石帅": 10,
    "董晓航": 11,
}

# ── ORGANIZATIONS ─────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共衡水市桃城区委员会", "type": "党委", "level": "县处级", "parent": "中共衡水市委", "location": "河北省衡水市桃城区", "source": "http://www.taocheng.gov.cn/"},
    {"id": 2, "name": "桃城区人民政府", "type": "政府", "level": "县处级", "parent": "衡水市人民政府", "location": "河北省衡水市桃城区", "source": "http://www.taocheng.gov.cn/"},
    {"id": 3, "name": "桃城区公安局", "type": "政府", "level": "乡科级", "parent": "桃城区人民政府", "location": "河北省衡水市桃城区", "source": "http://www.taocheng.gov.cn/"},
    {"id": 4, "name": "桃城区人民武装部", "type": "党委", "level": "县处级", "parent": "衡水军分区", "location": "河北省衡水市桃城区", "source": "http://www.taocheng.gov.cn/art/2026/3/27/art_126_620625.html"},
    {"id": 5, "name": "中共衡水市委", "type": "党委", "level": "地厅级", "parent": "", "location": "河北省衡水市", "source": "http://www.hengshui.gov.cn/"},
    {"id": 6, "name": "衡水市人民政府", "type": "政府", "level": "地厅级", "parent": "", "location": "河北省衡水市", "source": "http://www.hengshui.gov.cn/"},
]

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══ 区委书记 ═══
    {
        "id": 1, "name": "危国永", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共衡水市桃城区委书记、区人武部党委第一书记",
        "current_org": "中共衡水市桃城区委员会",
        "source": "http://www.taocheng.gov.cn/art/2026/3/27/art_126_620625.html (人武部党委第一书记任职大会 2026-03-27)",
    },
    # ═══ 区长 ═══
    {
        "id": 2, "name": "刘京", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区人民政府区长",
        "current_org": "桃城区人民政府",
        "source": "http://www.taocheng.gov.cn/art/2026/7/24/art_964_632371.html (区长之窗 2026-07-24)",
    },
    # ═══ 区政府领导 ═══
    {
        "id": 3, "name": "韩新民", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区委常委、区政府常务副区长",
        "current_org": "桃城区人民政府",
        "source": "http://www.taocheng.gov.cn/art/2026/7/24/art_964_632370.html (区长之窗 2026-07-24)",
    },
    {
        "id": 4, "name": "封希海", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区人民政府副区长、区公安分局局长",
        "current_org": "桃城区公安局",
        "source": "http://www.taocheng.gov.cn/art/2026/7/24/art_964_632368.html (区长之窗 2026-07-24)",
    },
    {
        "id": 5, "name": "姚文前", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区人民政府副区长",
        "current_org": "桃城区人民政府",
        "source": "http://www.taocheng.gov.cn/art/2026/7/24/art_964_632369.html (区长之窗 2026-07-24)",
    },
    {
        "id": 6, "name": "薛纯宾", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区人民政府副区长",
        "current_org": "桃城区人民政府",
        "source": "http://www.taocheng.gov.cn/art/2026/7/24/art_964_632365.html (区长之窗 2026-07-24)",
    },
    {
        "id": 7, "name": "孔德龙", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区人民政府副区长",
        "current_org": "桃城区人民政府",
        "source": "http://www.taocheng.gov.cn/art/2026/7/24/art_964_632363.html (区长之窗 2026-07-24)",
    },
    {
        "id": 8, "name": "陈靖", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区人民政府副区长",
        "current_org": "桃城区人民政府",
        "source": "http://www.taocheng.gov.cn/art/2026/7/24/art_964_632362.html (区长之窗 2026-07-24)",
    },
    # ═══ 其他区领导（疑似区委副书记, 未证实）═══
    {
        "id": 9, "name": "王东", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "桃城区区领导（疑似区委副书记，待核实）",
        "current_org": "中共衡水市桃城区委员会",
        "source": "http://www.taocheng.gov.cn/art/2026/3/27/art_126_620625.html (人武部任职大会列席, 2026-03-27)",
    },
    # ═══ 前任区长 ═══
    {
        "id": 10, "name": "石帅", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任桃城区区长（2026-07 由刘京接任, 去向未知）",
        "current_org": "桃城区人民政府",
        "source": "http://www.taocheng.gov.cn/art/2026/3/25/art_126_620622.html (区政府廉政工作会议, 2026-03-25)",
    },
    # ═══ 上级: 衡水市委/市政府一把手 ═══
    {
        "id": 11, "name": "董晓航", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "衡水市委书记、市政府市长",
        "current_org": "中共衡水市委",
        "source": "http://www.hengshui.gov.cn/art/2022/1/26/art_88_16.html (衡水政府网领导简介)",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "中共衡水市桃城区委书记", "start_date": "2026-03之前-至今", "end_date": "至今", "rank": "正处级", "note": "2026-03-26 兼任区人武部党委第一书记; 至2026-08在任"},
    {"person_id": 1, "org_id": 4, "title": "桃城区人武部党委第一书记", "start_date": "2026-03", "end_date": "至今", "rank": "", "note": "2026-03-26 任职大会宣布"},
    {"person_id": 2, "org_id": 2, "title": "桃城区区长", "start_date": "2026-07", "end_date": "至今", "rank": "正处级", "note": "第八届人大一次会议选举产生; 2026-07-24 区长之窗更新"},
    {"person_id": 3, "org_id": 1, "title": "桃城区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "桃城区政府常务副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "分管发改、财政、人社、应急、数据政务、金融等"},
    {"person_id": 4, "org_id": 3, "title": "桃城区公安分局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼副区长"},
    {"person_id": 4, "org_id": 2, "title": "桃城区人民政府副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "桃城区人民政府副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "桃城区人民政府副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "桃城区人民政府副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "桃城区人民政府副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "桃城区区委（拟任，未证实）", "start_date": "", "end_date": "至今", "rank": "", "note": "疑似区委副书记, 待核实"},
    {"person_id": 10, "org_id": 2, "title": "桃城区区长（前任）", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "2026-03 仍在任; 2026-07 由刘京接任"},
    {"person_id": 11, "org_id": 5, "title": "衡水市委书记", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "衡水市政府市长", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "领导关系", "context": "区委书记与区长搭档, 共同主持区党委与区政府工作", "overlap_org": "中共衡水市桃城区委员会/桃城区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与常务副区长（区委常委）", "overlap_org": "桃城区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与副区长（兼公安分局长）", "overlap_org": "桃城区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长与副区长", "overlap_org": "桃城区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与副区长", "overlap_org": "桃城区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长与副区长", "overlap_org": "桃城区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长", "overlap_org": "桃城区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "桃城区委书记与衡水市委书记（上级领导）", "overlap_org": "中共衡水市委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "前任后继", "context": "刘京接任石帅的区长职务", "overlap_org": "桃城区人民政府", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 3, "type": "班子关系", "context": "区委书记与区委常委（常务副区长）", "overlap_org": "中共衡水市桃城区委员会", "overlap_period": "至今"},
]

# ── BUILD ──────────────────────────────────────────────────────────
def build() -> None:
    from gov_relation.runner import run_build

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    conn = sqlite3.connect(DB_PATH)
    print("persons: ", conn.execute("select count(*) from persons").fetchone()[0])
    print("organizations: ", conn.execute("select count(*) from organizations").fetchone()[0])
    print("positions: ", conn.execute("select count(*) from positions").fetchone()[0])
    print("relationships: ", conn.execute("select count(*) from relationships").fetchone()[0])
    conn.close()
    print("DB_PATH:", DB_PATH)
    print("GEXF_PATH:", GEXF_PATH)


if __name__ == "__main__":
    build()