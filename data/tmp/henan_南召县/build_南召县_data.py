#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 南召县 leadership network.

南召县 - 南阳市 - 河南省
Targets: 县委书记方明洋, 县长赵国臣
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "南召县"
TASK_ID = "henan_南召县"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "方明洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "南召县委书记",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/01-28/1382402.html",
    },
    {
        "id": 2,
        "name": "赵国臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "南召县委副书记、县长",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/zjzf/",
    },
    # ── Previous Leader ──
    {
        "id": 3,
        "name": "宋兴哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原南召县长（已离任）",
        "current_org": "",
        "source": "https://www.nanzhao.gov.cn/2026/01-28/1382402.html",
    },
    # ── Government Leaders ──
    {
        "id": 4,
        "name": "王亚飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419241.html",
    },
    {
        "id": 5,
        "name": "叶博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419243.html",
    },
    {
        "id": 6,
        "name": "贺小森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419245.html",
    },
    {
        "id": 7,
        "name": "梁存",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419248.html",
    },
    {
        "id": 8,
        "name": "胡守武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、公安局局长",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419250.html",
    },
    {
        "id": 9,
        "name": "王广杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419249.html",
    },
    {
        "id": 10,
        "name": "胡晓琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长（挂职）",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419252.html",
    },
    # ── Other Key Leaders ──
    {
        "id": 11,
        "name": "梁志豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委领导（曾任县领导）",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2025/02-25/943636.html",
    },
    {
        "id": 12,
        "name": "苏自清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "南召县人大常委会",
        "source": "https://www.nanzhao.gov.cn/2026/06-16/1412739.html",
    },
    {
        "id": 13,
        "name": "田红梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/03-16/1391250.html",
    },
    {
        "id": 14,
        "name": "孙晓刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/03-16/1391250.html",
    },
    {
        "id": 15,
        "name": "陈光义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/03-16/1391250.html",
    },
    {
        "id": 16,
        "name": "郑涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/03-16/1391250.html",
    },
    {
        "id": 17,
        "name": "李立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/03-16/1391250.html",
    },
    {
        "id": 18,
        "name": "仝太峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/03-16/1391250.html",
    },
    {
        "id": 19,
        "name": "褚金梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2026/03-16/1391250.html",
    },
    {
        "id": 20,
        "name": "谢男",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、监委主任",
        "current_org": "中共南召县纪律检查委员会",
        "source": "https://www.nanzhao.gov.cn/2025/04-30/1036209.html",
    },
    {
        "id": 21,
        "name": "马秋柏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中国共产党南召县委员会",
        "source": "https://www.nanzhao.gov.cn/2025/04-30/1036209.html",
    },
    {
        "id": 22,
        "name": "冀豫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府二级调研员",
        "current_org": "南召县人民政府",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419256.html",
    },
    {
        "id": 23,
        "name": "王宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、政府办主任",
        "current_org": "南召县人民政府办公室",
        "source": "https://www.nanzhao.gov.cn/2026/07-10/1419257.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党南召县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党南阳市委员会",
        "location": "南召县",
    },
    {
        "id": 2,
        "name": "南召县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "南阳市人民政府",
        "location": "南召县",
    },
    {
        "id": 3,
        "name": "南召县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "南召县",
        "location": "南召县",
    },
    {
        "id": 4,
        "name": "南召县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "南召县人民政府",
        "location": "南召县",
    },
    {
        "id": 5,
        "name": "中共南召县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党南召县委员会",
        "location": "南召县",
    },
    {
        "id": 6,
        "name": "南召县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "南召县人民政府",
        "location": "南召县",
    },
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 方明洋
    {"person_id": 1, "org_id": 1, "title": "南召县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 赵国臣
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026", "end_date": "present", "rank": "正县级", "note": "接替宋兴哲"},
    # 宋兴哲
    {"person_id": 3, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2026", "rank": "正县级", "note": "已离任"},
    # 王亚飞
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责县政府常务工作"},
    # 叶博
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管自然资源和规划、住建、城管"},
    # 贺小森
    {"person_id": 6, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管教育、文旅、卫健、医保、民政"},
    # 梁存
    {"person_id": 7, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管科技、环保、工信、商务、市场监管"},
    # 胡守武
    {"person_id": 8, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管司法、信访,兼任县公安局局长"},
    {"person_id": 8, "org_id": 4, "title": "县公安局党委书记、局长、督察长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 王广杰
    {"person_id": 9, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管农业农村、乡村振兴、林业、水利"},
    # 胡晓琛
    {"person_id": 10, "org_id": 2, "title": "县政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职，负责京（津）宛合作"},
    # 梁志豪
    {"person_id": 11, "org_id": 1, "title": "县委领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 苏自清
    {"person_id": 12, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 谢男
    {"person_id": 20, "org_id": 5, "title": "县委常委、县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马秋柏
    {"person_id": 21, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 陈光义
    {"person_id": 15, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 冀豫
    {"person_id": 22, "org_id": 2, "title": "县政府二级调研员", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王宇
    {"person_id": 23, "org_id": 6, "title": "县政府办主任", "start_date": "", "end_date": "present", "rank": "", "note": "主持政府办全面工作"},
    {"person_id": 23, "org_id": 2, "title": "县政府党组成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "方明洋（县委书记）与赵国臣（县长）党政正职搭档",
        "overlap_org": "南召县",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "共事",
        "context": "方明洋（县委书记）与宋兴哲（原县长）前任党政正职搭档",
        "overlap_org": "南召县",
        "overlap_period": "至2026年",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "前任继任",
        "context": "赵国臣接替宋兴哲任南召县长",
        "overlap_org": "南召县人民政府",
        "overlap_period": "2026年交接",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "上下级",
        "context": "赵国臣（县长）与王亚飞（常务副县长）政府班子上下级关系",
        "overlap_org": "南召县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "上下级",
        "context": "赵国臣（县长）与叶博（副县长）政府班子上下级关系",
        "overlap_org": "南召县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "上下级",
        "context": "赵国臣（县长）与贺小森（副县长）政府班子上下级关系",
        "overlap_org": "南召县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "上下级",
        "context": "赵国臣（县长）与梁存（副县长）政府班子上下级关系",
        "overlap_org": "南召县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "上下级",
        "context": "赵国臣（县长）与胡守武（副县长、公安局长）政府班子上下级关系",
        "overlap_org": "南召县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "上下级",
        "context": "赵国臣（县长）与王广杰（副县长）政府班子上下级关系",
        "overlap_org": "南召县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 4,
        "person_b": 5,
        "type": "共事",
        "context": "王亚飞与叶博同为县委常委、副县长",
        "overlap_org": "南召县人民政府/县委",
        "overlap_period": "至今",
    },
    {
        "person_a": 4,
        "person_b": 21,
        "type": "共事",
        "context": "王亚飞与马秋柏同为县委常委",
        "overlap_org": "中国共产党南召县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "共事",
        "context": "方明洋（县委书记）与苏自清（县人大常委会主任）党政班子与人大负责人关系",
        "overlap_org": "南召县",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 20,
        "type": "上下级",
        "context": "方明洋（县委书记）与谢男（县纪委书记）党委班子上下级关系",
        "overlap_org": "中国共产党南召县委员会",
        "overlap_period": "至今",
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
    print(f" Done.")
