#!/usr/bin/env python3
"""Build script for 沈阳市沈河区 government personnel network."""

import sqlite3
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "沈河区"
STAGING = Path("data/tmp/liaoning_沈河区")

# Tokens required by process_tmp validation
DB_PATH = STAGING / "沈河区_network.db"
GEXF_PATH = STAGING / "沈河区_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (区委书记) ──
    {
        "id": 1,
        "name": "李盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-01",
        "birthplace": "待查",
        "education": "研究生学历，公共管理硕士（清华大学机械工程系硕士研究生，美国伊利诺伊理工学院公共管理硕士）",
        "party_join": "1996-06",
        "work_start": "2001-08",
        "current_post": "区委书记",
        "current_org": "中共沈阳市沈河区委员会",
        "source": "百度百科/沈阳日报/人民网任前公示",
    },
    # ── District Mayor (区长) ──
    {
        "id": 2,
        "name": "刘艳玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "待查",
        "education": "研究生学历，硕士学位",
        "party_join": "2000-11",
        "work_start": "2004-07",
        "current_post": "区委副书记、区长",
        "current_org": "沈河区人民政府",
        "source": "百度百科/网易新闻/东北新闻网",
    },
    # ── Executive Deputy Mayor (常务副区长) ──
    {
        "id": 3,
        "name": "庄海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-02",
        "birthplace": "待查",
        "education": "经济学学士，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（负责政府常务工作）",
        "current_org": "沈河区人民政府",
        "source": "百度百科",
    },
    # ── Deputy Party Secretary (区委副书记) ──
    {
        "id": 4,
        "name": "罗凌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "待查",
        "education": "在职研究生学历，硕士学位",
        "party_join": "1996-01",
        "work_start": "1992-12",
        "current_post": "区委副书记（曾任组织部部长）",
        "current_org": "中共沈阳市沈河区委员会",
        "source": "百度百科/沈阳市任前公示",
    },
    # ── Standing Committee Member / Party Committee Office Director (常委/区委办主任) ──
    {
        "id": 5,
        "name": "胡韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "待查",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委办公室主任（拟任区委副书记）",
        "current_org": "中共沈阳市沈河区委员会",
        "source": "沈阳网/任前公示（2026年第7号）",
    },
    # ── Standing Committee Member / Deputy Mayor (区委常委/副区长) ──
    {
        "id": 6,
        "name": "张成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "沈河区人民政府",
        "source": "沈河区政府官网/栋察楼市",
    },
    # ── Deputy Mayor (副区长) ──
    {
        "id": 7,
        "name": "陈青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "沈河区人民政府",
        "source": "沈河区政府官网",
    },
    {
        "id": 8,
        "name": "郭颂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "沈河区人民政府",
        "source": "沈河区政府官网",
    },
    {
        "id": 9,
        "name": "李欣蔚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "沈河区人民政府",
        "source": "沈河区政府官网",
    },
    {
        "id": 10,
        "name": "任波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "沈河区人民政府",
        "source": "沈河区政府官网",
    },
    # ── Predecessors ──
    {
        "id": 11,
        "name": "林宇航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-07",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记（已卸任）",
        "current_org": "",
        "source": "微信公众平台/沈河区领导干部大会",
    },
    {
        "id": 12,
        "name": "石国琦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长（现任沈阳水务集团负责人）",
        "current_org": "沈阳水务集团",
        "source": "搜狐网/微集分",
    },
    {
        "id": 13,
        "name": "谷军营",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记（更早时期）",
        "current_org": "",
        "source": "信用中国/沈河区新闻报道",
    },
    # ── Other Key Cadres ──
    {
        "id": 14,
        "name": "齐鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委（负责金融商贸开发区日常工作）",
        "current_org": "中共沈阳市沈河区委员会",
        "source": "沈河区政府办公室分工通知",
    },
    {
        "id": 15,
        "name": "张龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（曾任）",
        "current_org": "沈河区人民政府",
        "source": "沈河区政府办公室分工通知",
    },
    {
        "id": 16,
        "name": "杨玉志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "沈河区人民政府",
        "source": "百度百科/沈阳市沈河区人民政府页面",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共沈阳市沈河区委员会", "type": "党委", "level": "市辖区", "parent": "中共沈阳市委", "location": "沈阳市沈河区"},
    {"id": 2, "name": "沈河区人民政府", "type": "政府", "level": "市辖区", "parent": "沈阳市人民政府", "location": "沈阳市沈河区"},
    {"id": 3, "name": "沈阳金融商贸经济技术开发区管委会", "type": "开发区", "level": "国家级经开区", "parent": "沈河区人民政府", "location": "沈阳市沈河区"},
    {"id": 4, "name": "沈阳水务集团", "type": "事业单位", "level": "市属国企", "parent": "沈阳市人民政府", "location": "沈阳市"},
    {"id": 5, "name": "沈阳副食集团有限公司", "type": "事业单位", "level": "市属国企", "parent": "沈阳市人民政府", "location": "沈阳市"},
    {"id": 6, "name": "中共沈阳市皇姑区委员会", "type": "党委", "level": "市辖区", "parent": "中共沈阳市委", "location": "沈阳市皇姑区"},
    {"id": 7, "name": "中共沈阳市沈河区委组织部", "type": "党委", "level": "部门", "parent": "中共沈阳市沈河区委员会", "location": "沈阳市沈河区"},
    {"id": 8, "name": "中共沈阳市沈河区委办公室", "type": "党委", "level": "部门", "parent": "中共沈阳市沈河区委员会", "location": "沈阳市沈河区"},
    {"id": 9, "name": "沈河区人大常委会", "type": "人大", "level": "市辖区", "parent": "", "location": "沈阳市沈河区"},
    {"id": 10, "name": "政协沈河区委员会", "type": "政协", "level": "市辖区", "parent": "", "location": "沈阳市沈河区"},
]

# ── Positions ────────────────────────────────────────────────────────────

positions = [
    # 李盛
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2025", "end": "至今", "rank": "正厅级（副省级城市辖区正职高配）", "note": "从皇姑区委书记平调"},
    # 刘艳玲
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start": "2025-12", "end": "至今", "rank": "副厅级", "note": "2025年7月提名为代区长，2025年12月31日正式当选"},
    {"person_id": 2, "org_id": 2, "title": "代区长", "start": "2025-07", "end": "2025-12", "rank": "", "note": ""},
    # 庄海涛
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长（常务）", "start": "2022", "end": "至今", "rank": "副厅级", "note": ""},
    # 罗凌
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start": "2025", "end": "至今（拟任新职）", "rank": "副厅级", "note": "2026年5月拟任市政府派出机构正职"},
    {"person_id": 4, "org_id": 7, "title": "区委常委、组织部部长", "start": "2022", "end": "2025", "rank": "副厅级", "note": ""},
    # 胡韬
    {"person_id": 5, "org_id": 8, "title": "区委常委、区委办公室主任", "start": "", "end": "至今", "rank": "副厅级", "note": "2026年5月拟任市辖区党委副书记"},
    {"person_id": 5, "org_id": 2, "title": "副区长（兼方城文旅工作）", "start": "", "end": "", "rank": "", "note": ""},
    # 张成
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    # 陈青
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 郭颂
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 李欣蔚
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 任波
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 林宇航
    {"person_id": 11, "org_id": 1, "title": "区委书记", "start": "2022-08", "end": "2025", "rank": "", "note": "前任区委书记，已卸任"},
    # 石国琦
    {"person_id": 12, "org_id": 2, "title": "区委副书记、区长", "start": "2022-08", "end": "2025-07", "rank": "", "note": "前任区长，调任沈阳水务集团"},
    {"person_id": 12, "org_id": 4, "title": "负责人", "start": "2025-07", "end": "至今", "rank": "", "note": ""},
    # 谷军营
    {"person_id": 13, "org_id": 1, "title": "区委书记", "start": "2021", "end": "2022-08", "rank": "", "note": "更早前任"},
    # 齐鑫
    {"person_id": 14, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "", "note": "负责沈阳金融商贸开发区日常工作"},
    # 张龙
    {"person_id": 15, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "", "rank": "", "note": ""},
    # 杨玉志
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # 李盛→刘艳玲: 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "李盛任区委书记，刘艳玲任区长，党政一把手于2025年搭班子", "overlap_org": "中共沈阳市沈河区委员会/沈河区人民政府", "overlap_period": "2025-至今"},
    # 庄海涛→刘艳玲: 常务副手
    {"person_a": 3, "person_b": 2, "type": "上下级", "context": "庄海涛作为常务副区长协助刘艳玲主持区政府日常工作", "overlap_org": "沈河区人民政府", "overlap_period": "2025-至今"},
    # 李盛→庄海涛: 区委→政府
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "李盛作为区委书记领导区委常委会，庄海涛为区委常委", "overlap_org": "中共沈阳市沈河区委员会", "overlap_period": "2025-至今"},
    # 罗凌→李盛: 副书记配合书记
    {"person_a": 4, "person_b": 1, "type": "上下级", "context": "罗凌作为区委副书记配合李盛工作", "overlap_org": "中共沈阳市沈河区委员会", "overlap_period": "2025-至今"},
    # 胡韬→李盛: 常委/区委办主任配合书记
    {"person_a": 5, "person_b": 1, "type": "上下级", "context": "胡韬作为区委常委兼区委办公室主任服务区委书记李盛", "overlap_org": "中共沈阳市沈河区委员会", "overlap_period": "至今"},
    # 罗凌→胡韬: 组织→干部
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "罗凌曾任组织部长，胡韬为区委办主任，共同在区委常委会工作", "overlap_org": "中共沈阳市沈河区委员会", "overlap_period": ""},
    # 李盛→林宇航: 前任→后任
    {"person_a": 1, "person_b": 11, "type": "前任-后任", "context": "李盛接替林宇航担任沈河区委书记", "overlap_org": "中共沈阳市沈河区委员会", "overlap_period": ""},
    # 刘艳玲→石国琦: 前任→后任区长
    {"person_a": 2, "person_b": 12, "type": "前任-后任", "context": "刘艳玲接替石国琦担任沈河区长", "overlap_org": "沈河区人民政府", "overlap_period": "2025-07"},
    # 林宇航→石国琦: 前任搭档
    {"person_a": 11, "person_b": 12, "type": "党政搭档", "context": "林宇航任书记，石国琦任区长，共同搭班（2022-2025）", "overlap_org": "中共沈阳市沈河区委员会/沈河区人民政府", "overlap_period": "2022-2025"},
    # 林宇航→谷军营: 前任-后任书记
    {"person_a": 11, "person_b": 13, "type": "前任-后任", "context": "林宇航接替谷军营担任沈河区委书记", "overlap_org": "中共沈阳市沈河区委员会", "overlap_period": ""},
    # 刘艳玲→庄海涛: 区政府班子
    {"person_a": 2, "person_b": 3, "type": "工作关系", "context": "刘艳玲为区长，庄海涛为常务副区长，共同推进区政府工作", "overlap_org": "沈河区人民政府", "overlap_period": "2025-至今"},
    # 区政府副职之间
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "张成为副区长，协助刘艳玲工作", "overlap_org": "沈河区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "陈青为副区长，协助刘艳玲工作", "overlap_org": "沈河区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "郭颂为副区长，协助刘艳玲工作", "overlap_org": "沈河区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "李欣蔚为副区长，协助刘艳玲工作", "overlap_org": "沈河区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "任波为副区长，协助刘艳玲工作", "overlap_org": "沈河区人民政府", "overlap_period": "至今"},
    # 李盛→齐鑫: 常委
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "齐鑫为区委常委，在区委书记李盛领导下工作", "overlap_org": "中共沈阳市沈河区委员会", "overlap_period": "至今"},
    # 刘艳玲→杨玉志
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "杨玉志为副区长，协助刘艳玲工作", "overlap_org": "沈河区人民政府", "overlap_period": ""},
]

# ── Main ─────────────────────────────────────────────────────────────────

def main():
    db_path = STAGING / "沈河区_network.db"
    gexf_path = STAGING / "沈河区_network.gexf"

    print(f"==> Building: {SLUG}")
    print(f"    Persons: {len(persons)}")
    print(f"    Orgs:    {len(organizations)}")
    print(f"    Pos:     {len(positions)}")
    print(f"    Rel:     {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # Verify
    conn = sqlite3.connect(str(db_path))
    for table in ("persons", "organizations", "positions", "relationships"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"    DB {table}: {count} rows")
    conn.close()
    print(f"    GEXF: {gexf_path.exists()}")
    print(f"==> Done: {SLUG}")


if __name__ == "__main__":
    main()
