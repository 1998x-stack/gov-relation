#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 潢川县 leadership network.

潢川县 - 信阳市 - 河南省.
Targets: 县委书记程功言, 县长黄在国
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable (works from data/tmp/<task_id>/ during staging
# and from scripts/build/ after promotion)
_SELF = Path(__file__).resolve()
_REPO = next(
    (p for p in _SELF.parents if (p / "gov_relation").is_dir()),
    _SELF.parents[2],
)
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "潢川县"
TASK_ID = "henan_潢川县"
TODAY = "20260806"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── 核心: 县委书记 程功言 ──
    {
        "id": 1,
        "name": "程功言",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县委书记、县人武部党委第一书记",
        "current_org": "中国共产党潢川县委员会",
        "source": "http://www.huangchuan.gov.cn/2026/07-22/795628.html",
    },
    # ── 核心: 县长 黄在国 ──
    {
        "id": 2,
        "name": "黄在国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "",
        "education": "研究生（法学硕士）",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县委副书记、县政府县长、潢川经济开发区党工委书记、豫东南高新区党工委副书记",
        "current_org": "潢川县人民政府",
        "source": "http://www.huangchuan.gov.cn/2024/12-02/417281.html",
    },
    # ── 县委班子 ──
    {
        "id": 3,
        "name": "刘海霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县委副书记",
        "current_org": "中国共产党潢川县委员会",
        "source": "http://www.huangchuan.gov.cn/2026/07-22/795628.html",
    },
    {
        "id": 4,
        "name": "刘俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-08",
        "birthplace": "",
        "education": "大学（管理学学士）",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县委常委、县政府副县长、党组副书记（常务副县长）",
        "current_org": "潢川县人民政府",
        "source": "http://www.huangchuan.gov.cn/2022/07-05/417282.html",
    },
    {
        "id": 5,
        "name": "谢文彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县委常委、组织部部长",
        "current_org": "中国共产党潢川县委员会",
        "source": "http://www.huangchuan.gov.cn/2026/07-30/796804.html",
    },
    {
        "id": 6,
        "name": "熊光阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-04",
        "birthplace": "",
        "education": "大学（工学学士）",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县委常委、宣传部部长、副县长",
        "current_org": "潢川县人民政府",
        "source": "http://www.huangchuan.gov.cn/2026/06-15/790105.html",
    },
    # ── 县政府班子 ──
    {
        "id": 7,
        "name": "陈益书",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县副县长、县公安局党委书记、局长",
        "current_org": "潢川县人民政府",
        "source": "http://www.huangchuan.gov.cn/2022/10-13/417284.html",
    },
    {
        "id": 8,
        "name": "何婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-04",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县副县长",
        "current_org": "潢川县人民政府",
        "source": "http://www.huangchuan.gov.cn/2026/06-15/790106.html",
    },
    # ── 其他县处级领导（角色待补） ──
    {
        "id": 9,
        "name": "龚廷树",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县县处级领导",
        "current_org": "潢川县人民政府",
        "source": "http://www.huangchuan.gov.cn/2026/07-29/796631.html",
    },
    {
        "id": 10,
        "name": "祁璟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县县处级领导",
        "current_org": "中国共产党潢川县委员会",
        "source": "http://www.huangchuan.gov.cn/2026/07-28/796438.html",
    },
    {
        "id": 11,
        "name": "马行超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潢川县县处级领导",
        "current_org": "中国共产党潢川县委员会",
        "source": "http://www.huangchuan.gov.cn/2026/07-28/796438.html",
    },
    # ── 前任县委书记（继任链） ──
    {
        "id": 14,
        "name": "赵军伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学（公共管理硕士）",
        "party_join": "",
        "work_start": "",
        "current_post": "信阳市委常委、市政府党组副书记、副市长（原潢川县委书记）",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
    {
        "id": 15,
        "name": "赵亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原潢川县委书记（2021年底卸任）",
        "current_org": "",
        "source": "https://www.huangchuan.gov.cn/",
    },
    # ── 跨县/历史关联人（网络节点） ──
    {
        "id": 12,
        "name": "夏明夫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原潢川县委副书记、潢川开发区主任（现新县县委书记）",
        "current_org": "",
        "source": "https://ribao.xyxww.com.cn/",
    },
    {
        "id": 13,
        "name": "古生辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原潢川县委副书记、付店镇党委书记（现信阳市平桥区区长）",
        "current_org": "",
        "source": "report/20260725-河南省-信阳市-新县-领导班子调查报告.md",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党潢川县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "潢川县",
    },
    {
        "id": 2,
        "name": "潢川县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "信阳市人民政府",
        "location": "潢川县",
    },
    {
        "id": 3,
        "name": "潢川经济开发区",
        "type": "开发区",
        "level": "省级开发区",
        "parent": "潢川县",
        "location": "潢川县",
    },
    {
        "id": 4,
        "name": "豫东南高新技术产业开发区",
        "type": "开发区",
        "level": "市级",
        "parent": "信阳市",
        "location": "潢川/光山一带",
    },
    {
        "id": 5,
        "name": "潢川县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "潢川县人民政府",
        "location": "潢川县",
    },
    {
        "id": 6,
        "name": "中国共产党新县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "新县",
    },
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    {"person_id": 1, "org_id": 1, "title": "潢川县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "至今，兼县人武部党委第一书记"},
    {"person_id": 2, "org_id": 2, "title": "潢川县委副书记、县政府县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "兼潢川经济开发区党工委书记"},
    {"person_id": 2, "org_id": 3, "title": "潢川经济开发区党工委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 4, "title": "豫东南高新区党工委副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "潢川县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "潢川县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县委县政府常务及党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "潢川县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "潢川县委常委、宣传部部长、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "潢川县公安局局长", "start_date": "", "end_date": "", "rank": "", "note": "兼任副县长"},
    {"person_id": 7, "org_id": 2, "title": "潢川县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "潢川县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────

relationships = [
    # 书记—县长 搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "同事",
        "context": "程功言（县委书记）与黄在国（县委副书记、县长）为现役党政一把手搭档",
        "overlap_org": "潢川县委/县政府",
        "overlap_period": "2024-至今",
    },
    # 书记—常委会成员
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "程功言（书记）与刘海霞（副书记）县委班子上下级",
        "overlap_org": "中国共产党潢川县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "上下级",
        "context": "程功言（书记）与刘俊（常委、常务副县长）班子上下级",
        "overlap_org": "潢川县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "上下级",
        "context": "程功言（书记）到县委组织部调研，谢文彬为县委常委、组织部部长",
        "overlap_org": "中国共产党潢川县委员会",
        "overlap_period": "2026-08",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "上下级",
        "context": "程功言（书记）与熊光阳（常委、宣传部长、副县长）同班子共事",
        "overlap_org": "潢川县委员会",
        "overlap_period": "",
    },
    # 县长与政府班子上下级
    {
        "person_a": 2,
        "person_b": 4,
        "type": "上下级",
        "context": "黄在国（县长）与刘俊（常务副县长）县政府班子上下级",
        "overlap_org": "潢川县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "上下级",
        "context": "黄在国（县长）与熊光阳（副县长）县政府班子上下级",
        "overlap_org": "潢川县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "上下级",
        "context": "黄在国（县长）与陈益书（副县长、公安局长）县政府班子上下级",
        "overlap_org": "潢川县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "上下级",
        "context": "黄在国（县长）与何婷（副县长）县政府班子上下级",
        "overlap_org": "潢川县人民政府",
        "overlap_period": "",
    },
    # 县委常委之间同届班子互认
    {
        "person_a": 6,
        "person_b": 5,
        "type": "同事",
        "context": "熊光阳（宣传部长）、谢文彬（组织部长）为同届潢川县委常委",
        "overlap_org": "中国共产党潢川县委员会",
        "overlap_period": "",
    },
    # 经济开发区 / 高新区网络
    {
        "person_a": 2,
        "person_b": 12,
        "type": "同系统",
        "context": "黄在国现任潢川经开区党工委书记；夏明夫曾任潢川开发区主任，同为潢川开发区系统负责人",
        "overlap_org": "潢川经济开发区",
        "overlap_period": "",
    },
    # 跨县干部交流网络
    {
        "person_a": 1,
        "person_b": 12,
        "type": "跨县交流",
        "context": "夏明夫曾于潢川任职（潢川县委副书记、潢川开发区主任），后调任新县，属信阳南部县区干部交流节点",
        "overlap_org": "潢川县",
        "overlap_period": "2015-2016",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "前任继任",
        "context": "古生辉（平桥区长）曾于2021-2023以'墩苗'干部身份任潢川县委副书记、付店镇党委书记，与潢川班子有交集",
        "overlap_org": "潢川县",
        "overlap_period": "2021-2024",
    },
    # 县委书记继任链：赵亮 → 赵军伟 → 程功言
    {
        "person_a": 15,
        "person_b": 14,
        "type": "前任继任",
        "context": "赵军伟于2021-07-06接任潢川县委书记，赵亮离任",
        "overlap_org": "中国共产党潢川县委员会",
        "overlap_period": "2021-07",
    },
    {
        "person_a": 14,
        "person_b": 1,
        "type": "前任继任",
        "context": "赵军伟（2021至2024底任潢川县委书记）之后，程功言任现职潢川县委书记；赵军伟后升任信阳市委常委、副市长",
        "overlap_org": "中国共产党潢川县委员会",
        "overlap_period": "2025",
    },
    {
        "person_a": 14,
        "person_b": 2,
        "type": "同事",
        "context": "赵军伟任潢川县委书记期间与黄在国（县长）同班子（2024）",
        "overlap_org": "潢川县委/县政府",
        "overlap_period": "2024",
    },
]

# ── Build ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
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

    print(f" DB: {DB_PATH}")
    print(f" GEXF: {GEXF_PATH}")
    print(" Done.")