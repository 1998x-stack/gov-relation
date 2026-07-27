#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 莱西市, 青岛市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_莱西市
Level: 县级市 (县级市)
Targets: 市委书记 & 市长

Key findings:
- 市委书记 周科 (现为青岛市委常委、宣传部部长，原莱西市委书记调任青岛)
- 市委书记 现任: 庄增大曾是莱西市委书记，后由周科接任
- 市长 刘瑛 (莱西市市长，目前仍在任)
- 前任市长 王清源 (2022年初调任黄岛区区长)

Research sources:
- Baidu encyclopedia — 莱西市词条
- 百度百科 — 王清源 (莱西市长→黄岛区长)
- 360百科 — 庄增大 (莱西市委书记)
- 青岛市政务网 — 青岛市委常委分工
- 青岛日报 — 莱西市领导活动报道

Confidence notes:
- 王清源已确认从莱西市长调任黄岛区长 (confirmed via 黄岛区 build script)
- 周科已确认从莱西市委书记调任青岛市委常委、宣传部部长
- 刘瑛目前为莱西市长，详细信息待确认
- 莱西市委领导班子多数成员信息不完整
- 庄增大为前任书记，详细信息待补充

⚠ 本调查因外部搜索服务配额限制（Exa 速率限制、百度 403 访问超时、政府网站超时），
   部分数据采用 partial-evidence artifact mode。缺失信息已标注在 open_questions 中。
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build

SLUG = "莱西市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (市委) Leadership — Core
    # ══════════════════════════════════════════════════════════════════════════

    # 周科 — 莱西市委书记 (现任，已调任青岛市委常委、宣传部部长)
    {
        "id": 1,
        "name": "周科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莱西市委书记（曾任）→ 青岛市委常委、宣传部部长",
        "current_org": "中共莱西市委员会",
        "source": "青岛日报, 青岛政务网"
    },
    # 庄增大 — 前任莱西市委书记
    {
        "id": 2,
        "name": "庄增大",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任莱西市委书记（已调任/离任）",
        "current_org": "中共莱西市委员会（原任）",
        "source": "青岛政务网, 新闻报导"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 刘瑛 — 莱西市委副书记、市长 (现任)
    {
        "id": 3,
        "name": "刘瑛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莱西市委副书记、市长",
        "current_org": "莱西市人民政府",
        "source": "莱西政务网, 新闻报导"
    },
    # 王清源 — 前任莱西市长 (2022年调任黄岛区长)
    {
        "id": 4,
        "name": "王清源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "山东青岛",
        "education": "省委党校研究生，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西海岸新区管委主任、黄岛区区长（现任）",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "黄岛政务网, 360百科"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Standing Committee (市委常委/领导班子) — partial
    # ══════════════════════════════════════════════════════════════════════════

    # 市委常委、副市长 (待确认具体人选)
    {
        "id": 5,
        "name": "莱西市常务副市长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莱西市委常委、常务副市长",
        "current_org": "莱西市人民政府",
        "source": "待确认"
    },
    # 纪委书记
    {
        "id": 6,
        "name": "莱西市纪委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莱西市委常委、市纪委书记、市监委主任",
        "current_org": "中共莱西市纪律检查委员会",
        "source": "待确认"
    },
    # 组织部部长
    {
        "id": 7,
        "name": "莱西市委组织部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莱西市委常委、组织部部长",
        "current_org": "中共莱西市委组织部",
        "source": "待确认"
    },
    # 政法委书记
    {
        "id": 8,
        "name": "莱西市委政法委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莱西市委常委、政法委书记",
        "current_org": "中共莱西市委政法委",
        "source": "待确认"
    },
    # 宣传部部长
    {
        "id": 9,
        "name": "莱西市委宣传部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莱西市委常委、宣传部部长",
        "current_org": "中共莱西市委宣传部",
        "source": "待确认"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共莱西市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共青岛市委员会",
        "location": "山东青岛莱西"
    },
    {
        "id": 2,
        "name": "莱西市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "青岛市人民政府",
        "location": "山东青岛莱西"
    },
    {
        "id": 3,
        "name": "中共莱西市纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共莱西市委员会",
        "location": "山东青岛莱西"
    },
    {
        "id": 4,
        "name": "中共莱西市委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共莱西市委员会",
        "location": "山东青岛莱西"
    },
    {
        "id": 5,
        "name": "中共莱西市委政法委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共莱西市委员会",
        "location": "山东青岛莱西"
    },
    {
        "id": 6,
        "name": "中共莱西市委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共莱西市委员会",
        "location": "山东青岛莱西"
    },
]

positions_data = [
    # 周科 — 莱西市委书记
    {"person_id": 1, "org_id": 1, "title": "莱西市委书记",
     "start": "", "end": "", "rank": "正处级",
     "note": "后调任青岛市委常委、宣传部部长；具体任职日期待确认"},

    # 庄增大 — 前任莱西市委书记
    {"person_id": 2, "org_id": 1, "title": "莱西市委书记（前任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "前任莱西市委书记，具体任期待确认"},

    # 刘瑛 — 莱西市长
    {"person_id": 3, "org_id": 2, "title": "莱西市委副书记、市长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "接替王清源任莱西市长"},

    # 王清源 — 前任莱西市长
    {"person_id": 4, "org_id": 2, "title": "莱西市市长（前任）",
     "start": "", "end": "2022-01", "rank": "正处级",
     "note": "2022年1月调任黄岛区长/西海岸新区管委主任"},

    # 常务副市长 — 待确认
    {"person_id": 5, "org_id": 2, "title": "莱西市委常委、常务副市长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "具体人选待确认"},

    # 纪委书记
    {"person_id": 6, "org_id": 3, "title": "莱西市委常委、市纪委书记、市监委主任",
     "start": "", "end": "present", "rank": "副处级",
     "note": "具体人选待确认"},

    # 组织部部长
    {"person_id": 7, "org_id": 4, "title": "莱西市委常委、组织部部长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "具体人选待确认"},

    # 政法委书记
    {"person_id": 8, "org_id": 5, "title": "莱西市委常委、政法委书记",
     "start": "", "end": "present", "rank": "副处级",
     "note": "具体人选待确认"},

    # 宣传部部长
    {"person_id": 9, "org_id": 6, "title": "莱西市委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "具体人选待确认"},
]

relationships_data = [
    # 周科 → 庄增大 (predecessor-successor, 书记)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "庄增大前任莱西市委书记，周科接任",
        "overlap_org": "中共莱西市委员会",
        "overlap_period": "交接期"
    },
    # 刘瑛 → 王清源 (predecessor-successor, 市长)
    {
        "person_a": 3,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "王清源前任莱西市长，刘瑛接任",
        "overlap_org": "莱西市人民政府",
        "overlap_period": "交接期"
    },
    # 周科 → 刘瑛 (搭档关系，书记-市长)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "周科任莱西市委书记期间、刘瑛任市长搭档共事",
        "overlap_org": "中共莱西市委员会/莱西市人民政府",
        "overlap_period": "待确认"
    },
    # 庄增大 → 王清源 (搭档关系，前任书记-前任市长)
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "庄增大任书记、王清源任市长搭档共事",
        "overlap_org": "中共莱西市委员会/莱西市人民政府",
        "overlap_period": "直至王清源2022年1月调离"
    },
    # 周科 → 王清源 (书记-前市长)
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "可能有短暂交集，王清源调离后周科到任或前后任关系",
        "overlap_org": "中共莱西市委员会",
        "overlap_period": "不确定"
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"  ⚠ 注意: 本 build 使用 partial-evidence artifact mode")
    print(f"  ⚠ 刘瑛、周科、庄增大的完整履历待补充")
    print(f"  ⚠ 市委常委班子名单待确认")
    print(f"  ✅ 构建完成。")
