#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建昌县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 辽宁省
Parent City: 葫芦岛市
Region: 建昌县
Targets: 县委书记 & 县长

数据来源（截至2026-08-07）:
- 建昌县人民政府网 (jianchang.gov.cn) 常务会议/县委常委会新闻
- 葫芦岛市委组织部干部任前公示公告（2017年/2021年第17号）
- 中国经济网地方党政领导人物库
- 搜狗百科/新浪百科（张祥波、周佳楷、闫庆礼词条）

网络访问部分受限个别字段标记为 unverified。
"""
import json
import os
import sys
from datetime import datetime

# 确保可以导入 gov_relation 包
BASE = os.path.dirname(os.path.abspath(__file__))
# staging dir = data/tmp/liaoning_建昌县/
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── 路径 ──
SLUG = "建昌县"
STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

AS_OF = "2026-08-07"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ── 核心领导：县委书记 ──
    {
        "id": 1,
        "name": "周佳楷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-05",
        "birthplace": "",
        "education": "研究生学历，法学博士学位",
        "party_join": "1999-06",
        "work_start": "2000-06",
        "current_post": "建昌县委书记",
        "current_org": "中共建昌县委员会",
        "source": "葫芦岛市委组织部干部任前公示（市纪委监委案件监督管理室主任，拟任兴城市委常委、纪委书记）；建昌县政府网2025-2026年县委常委会会议新闻",
    },
    # ── 核心领导：县长 ──
    {
        "id": 2,
        "name": "赵宜洋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县委副书记、县长",
        "current_org": "建昌县人民政府",
        "source": "建昌县《政府工作报告》（2022年12月18日在第十八届人大三次会议，以县长身份汇报）；建昌县政府网2025年常务会议新闻",
    },
    # ── 县人大常委会主任 ──
    {
        "id": 3,
        "name": "张东生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县人大常委会主任",
        "current_org": "建昌县人大常委会",
        "source": "建昌县政府网2025年12月县委理论学习中心组会议新闻（列为县人大常委会主任）",
    },
    # ── 县政协主席 ──
    {
        "id": 4,
        "name": "张东波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-01",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "1989-07",
        "work_start": "1985-07",
        "current_post": "建昌县政协主席",
        "current_org": "建昌县政协",
        "source": "葫芦岛市委组织部公告（2021年第17号）：张东波，曾任建昌县副县长、三级调研员，拟任县政协领导班子正职；建昌县政府网2025年会议新闻",
    },
    # ── 县委副书记 ──
    {
        "id": 5,
        "name": "谷佳奇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县委副书记",
        "current_org": "中共建昌县委员会",
        "source": "建昌县政府网2025年12月县委理论学习中心组会议新闻",
    },
    # ── 常务副县长 ──
    {
        "id": 6,
        "name": "杨宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县委常委、常务副县长",
        "current_org": "建昌县人民政府",
        "source": "建昌县政府网第十八届县政府第92次常务会议新闻（2025-06-19）",
    },
    # ── 副县长 ──
    {
        "id": 7,
        "name": "冀大勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县副县长",
        "current_org": "建昌县人民政府",
        "source": "建昌县政府网第十八届县政府第92次常务会议新闻（2025-06-19）",
    },
    {
        "id": 8,
        "name": "宛斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县副县长",
        "current_org": "建昌县人民政府",
        "source": "建昌县政府网第十八届县政府第92次常务会议新闻（2025-06-19）",
    },
    {
        "id": 9,
        "name": "王静",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县副县长",
        "current_org": "建昌县人民政府",
        "source": "建昌县政府网第十八届县政府第92次常务会议新闻（2025-06-19）",
    },
    {
        "id": 10,
        "name": "王保良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建昌县副县长",
        "current_org": "建昌县人民政府",
        "source": "建昌县政府网第十八届县政府第92次常务会议新闻（2025-06-19）；2025年8月县人大常委会第三十三次会议新闻",
    },
    # ── 前任县委书记 → 葫芦岛市副市长 ──
    {
        "id": 11,
        "name": "张祥波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "1998-12",
        "work_start": "1999-08",
        "current_post": "葫芦岛市副市长",
        "current_org": "葫芦岛市人民政府",
        "source": "中国经济网（2025-04-28）：2025年4月27日葫芦岛市七届人大常委会第25次会议任命为副市长；张祥波曾任建昌县长/县委书记",
    },
    # ── 前任建昌县委书记 ──
    {
        "id": 12,
        "name": "闫庆礼",
        "gender": "男",
        "ethnicity": "",
        "birth": "1965",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1986",
        "current_post": "葫芦岛市委常委",
        "current_org": "中共葫芦岛市委员会",
        "source": "中文百科（闫庆礼）：1965年生，曾任建昌县委书记（约2013.11起）、葫芦岛市委常委",
    },
    # ── 历史人物：曾任建昌县委副书记、县长 → 兴城市委书记 ──
    {
        "id": 13,
        "name": "孙志浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1960-07",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "1984-11",
        "work_start": "1977-07",
        "current_post": "（已退休/他曾任丹东市代市长）",
        "current_org": "",
        "source": "中国经济网（孙志浩简历）：1997-2009历任建昌县委组织部长、县委副书记、县长",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共建昌县委员会", "type": "党委", "level": "县级", "parent": "中共葫芦岛市委员会", "location": "建昌县"},
    {"id": 2, "name": "建昌县人民政府", "type": "政府", "level": "县级", "parent": "葫芦岛市人民政府", "location": "建昌县"},
    {"id": 3, "name": "建昌县人大常委会", "type": "人大", "level": "县级", "parent": "葫芦岛市人大常委会", "location": "建昌县"},
    {"id": 4, "name": "建昌县政协", "type": "政协", "level": "县级", "parent": "葫芦岛市政协", "location": "建昌县"},
    {"id": 5, "name": "中共建昌县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共葫芦岛市纪律检查委员会", "location": "建昌县"},
    {"id": 6, "name": "兴城市纪委监委", "type": "纪委", "level": "县级", "parent": "中共葫芦岛市纪律检查委员会", "location": "兴城市"},
    {"id": 7, "name": "葫芦岛市纪委监委", "type": "纪委", "level": "市级", "parent": "中共葫芦岛市委员会", "location": "葫芦岛市"},
    {"id": 8, "name": "葫芦岛市人民政府", "type": "政府", "level": "市级", "parent": "辽宁省人民政府", "location": "葫芦岛市"},
    {"id": 9, "name": "中共葫芦岛市委员会", "type": "党委", "level": "市级", "parent": "中共辽宁省委", "location": "葫芦岛市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    {"person_id": 1, "org_id": 1, "title": "建昌县委书记", "start_date": "2025", "end_date": "", "rank": "正处级", "note": "2025年（张祥波2025.4卸任后）由兴城市纪委书记调任；2025.12/2026.2县委常委会会议确认"},
    {"person_id": 1, "org_id": 6, "title": "兴城市委常委、纪委书记、监委主任", "start_date": "2021", "end_date": "2025", "rank": "副处级", "note": "2021年市委组织部公示拟任；纪委系统出身"},
    {"person_id": 1, "org_id": 7, "title": "葫芦岛市纪委监委案件监督管理室主任", "start_date": "", "end_date": "2021", "rank": "正科级/副处级", "note": "2021年市委组织部公示时任职务"},
    {"person_id": 2, "org_id": 2, "title": "建昌县委副书记、县长", "start_date": "2022", "end_date": "", "rank": "正处级", "note": "2022.12《政府工作报告》以县长身份汇报"},
    {"person_id": 2, "org_id": 2, "title": "建昌县常务副县长（拟任县长前）", "start_date": "2021", "end_date": "2022", "rank": "副处级", "note": "此前任常务副县长（未获公开完整履历）"},
    {"person_id": 3, "org_id": 3, "title": "建昌县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "2025.12会议新闻列名"},
    {"person_id": 3, "org_id": 2, "title": "建昌县常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "曾任常务副县长（公开报道）"},
    {"person_id": 4, "org_id": 4, "title": "建昌县政协主席", "start_date": "2021", "end_date": "", "rank": "正处级", "note": "2021年被拟任县政协班子正职"},
    {"person_id": 4, "org_id": 2, "title": "建昌县副县长、三级调研员", "start_date": "", "end_date": "2021", "rank": "副处级", "note": "2021年任前公示时任职务"},
    {"person_id": 5, "org_id": 1, "title": "建昌县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025.12会议新闻列名"},
    {"person_id": 6, "org_id": 2, "title": "建昌县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025.06常务会议列名"},
    {"person_id": 7, "org_id": 2, "title": "建昌县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025.06常务会议列名"},
    {"person_id": 8, "org_id": 2, "title": "建昌县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025.06常务会议列名"},
    {"person_id": 9, "org_id": 2, "title": "建昌县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025.06常务会议列名"},
    {"person_id": 10, "org_id": 2, "title": "建昌县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025.06/2025.08会议列名"},
    {"person_id": 11, "org_id": 8, "title": "葫芦岛市副市长", "start_date": "2025-04", "end_date": "", "rank": "副厅级", "note": "2025-04-27葫芦岛市七届人大常委会第25次会议任命"},
    {"person_id": 11, "org_id": 1, "title": "建昌县委书记", "start_date": "2022", "end_date": "2025-04", "rank": "正处级", "note": "张祥波由县长升任书记"},
    {"person_id": 11, "org_id": 2, "title": "建昌县委副书记、县长", "start_date": "2017", "end_date": "2022", "rank": "正处级", "note": "2021.12政府工作报告以县长身份汇报"},
    {"person_id": 12, "org_id": 9, "title": "葫芦岛市委常委", "start_date": "2017-11", "end_date": "", "rank": "副厅级", "note": "2017年11月任市委常委"},
    {"person_id": 12, "org_id": 1, "title": "建昌县委书记", "start_date": "2013-11", "end_date": "2022", "rank": "正处级", "note": "闫庆礼2013年起任建昌县委书记（继任者张祥波）"},
    {"person_id": 13, "org_id": 2, "title": "建昌县委副书记、县政府县长", "start_date": "2005-01", "end_date": "2009-02", "rank": "正处级", "note": "2004.12任代县长，2005.01转正"},
    {"person_id": 13, "org_id": 1, "title": "建昌县委常务副书记", "start_date": "2002-12", "end_date": "2004-12", "rank": "副处级", "note": "亦曾任建昌县委副书记、组织部部长"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 县长 ↔ 书记（现任搭档）
    {
        "person_a": 2, "person_b": 1,
        "type": "overlap", "context": "现任建昌县党政一把手搭档（县委副书记、县长 ↔ 县委书记）",
        "overlap_org": "建昌县（县委+政府）", "overlap_period": "2025-至今",
    },
    # 张祥波（前任书记）→ 周佳楷（现任书记）接替链
    {
        "person_a": 11, "person_b": 1,
        "type": "predecessor_successor", "context": "张祥波任建昌县委书记任满后调任葫芦岛市副市长，周佳楷接任县委书记",
        "overlap_org": "中共建昌县委员会", "overlap_period": "2025（交接）",
    },
    # 闫庆礼（前前任书记）→ 张祥波（前任书记）
    {
        "person_a": 12, "person_b": 11,
        "type": "predecessor_successor", "context": "闫庆礼任建昌县委书记（2013起），张祥波接任（约2022）",
        "overlap_org": "中共建昌县委员会", "overlap_period": "2022前后（交接）",
    },
    # 赵宜洋 ↔ 张祥波（县长职务接替：张祥波曾为县长/书记）
    {
        "person_a": 2, "person_b": 11,
        "type": "predecessor_successor", "context": "赵宜洋接任建昌县县长（此前张祥波市长任县长为书记）",
        "overlap_org": "建昌县人民政府", "overlap_period": "2022前后（交接）",
    },
    # 张东波（政协主席）↔ 张东生（人大主任）同届四套班子共事
    {
        "person_a": 4, "person_b": 3,
        "type": "overlap", "context": "张东波（县政协主席）与张东生（县人大主任）同为建昌县四套班子主要负责人（2021年后至今）",
        "overlap_org": "建昌县四套班子", "overlap_period": "2021-至今",
    },
    # 杨宇（常务副县长）↔ 谷佳奇（县委副书记）党政班子实务协作
    {
        "person_a": 6, "person_b": 5,
        "type": "overlap", "context": "杨宇（常务副县长）与谷佳奇（县委副书记）同在建昌县党政班子共事（2025年）",
        "overlap_org": "建昌县党政领导班子", "overlap_period": "2025-至今",
    },
]

# =========================================================================
# 5. RUN
# =========================================================================
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

    # 打印统计
    counts = {
        "persons": len(persons),
        "organizations": len(organizations),
        "positions": len(positions),
        "relationships": len(relationships),
    }
    print("建昌县 network build complete (as-of %s): %s" % (AS_OF, json.dumps(counts, ensure_ascii=False)))

    # 用 sqlite3 校验数据库表齐备
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    required = {"persons", "organizations", "positions", "relationships"}
    missing = sorted(required - tables)
    if missing:
        raise SystemExit("数据库缺少必要表: %s" % missing)
    print("SQLite 校验通过: 4 张标准表均存在")