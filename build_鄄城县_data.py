#!/usr/bin/env python3
"""鄄城县领导班子关系网络数据构建脚本。

生成:
  - data/tmp/shandong_鄄城县/鄄城县_network.db (SQLite)
  - data/tmp/shandong_鄄城县/鄄城县_network.gexf (GEXF)

调查日期: 2026-07-25
调查范围: 县委书记、县长及县委领导班子
数据来源: 公开资料、政府网站、任免公示
置信度: 部分信息经多渠道交叉验证，部分待补充
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

# 将项目根目录加入路径
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# 临时输出目录
TMP_DIR = REPO_ROOT / "data" / "tmp" / "shandong_鄄城县"
DB_PATH = TMP_DIR / "鄄城县_network.db"
GEXF_PATH = TMP_DIR / "鄄城县_network.gexf"

# ── 人员 ──────────────────────────────────────────────────────────
persons = [
    # === 县委领导 ===
    {
        "id": 1,
        "name": "孙伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共鄄城县委员会",
        "source": "鄄城县人民政府官网; 菏泽市委组织部任前公示",
    },
    {
        "id": 2,
        "name": "邓兆朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "鄄城县人民政府",
        "source": "鄄城县人民政府官网; 菏泽市委组织部任前公示",
    },
    {
        "id": 3,
        "name": "尚彦龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共鄄城县委员会",
        "source": "鄄城县人民政府官网",
    },
    {
        "id": 4,
        "name": "李沉静",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "鄄城县人民政府",
        "source": "鄄城县人民政府官网; 菏泽市委组织部任前公示",
    },
    {
        "id": 5,
        "name": "温雪梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共鄄城县纪律检查委员会",
        "source": "菏泽市纪委监委官网; 鄄城县人民政府官网",
    },
    {
        "id": 6,
        "name": "黄金果",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共鄄城县委组织部",
        "source": "鄄城县人民政府官网; 菏泽市委组织部任前公示",
    },
    {
        "id": 7,
        "name": "王海龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共鄄城县委宣传部",
        "source": "鄄城县人民政府官网",
    },
    {
        "id": 8,
        "name": "庞红宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共鄄城县委政法委员会",
        "source": "鄄城县人民政府官网",
    },
    {
        "id": 9,
        "name": "张伯新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共鄄城县委办公室",
        "source": "鄄城县人民政府官网",
    },
    {
        "id": 10,
        "name": "王志荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共鄄城县委统一战线工作部",
        "source": "鄄城县人民政府官网",
    },
    # === 副县长 ===
    {
        "id": 11,
        "name": "曹传杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "鄄城县人民政府",
        "source": "鄄城县人民政府官网",
    },
    {
        "id": 12,
        "name": "赵少林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "鄄城县公安局",
        "source": "鄄城县人民政府官网",
    },
    {
        "id": 13,
        "name": "张广兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "鄄城县人民政府",
        "source": "鄄城县人民政府官网",
    },
    # === 前任领导 ===
    {
        "id": 14,
        "name": "袁红兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "菏泽市委组织部任免公示; 鄄城县人民政府官网",
    },
]

# ── 组织 ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鄄城县委员会", "type": "党委", "level": "县级", "parent": "中共菏泽市委", "location": "鄄城县"},
    {"id": 2, "name": "鄄城县人民政府", "type": "政府", "level": "县级", "parent": "菏泽市人民政府", "location": "鄄城县"},
    {"id": 3, "name": "中共鄄城县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共菏泽市纪委", "location": "鄄城县"},
    {"id": 4, "name": "鄄城县监察委员会", "type": "政府", "level": "县级", "parent": "鄄城县人民政府", "location": "鄄城县"},
    {"id": 5, "name": "中共鄄城县委组织部", "type": "党委", "level": "县级", "parent": "中共鄄城县委员会", "location": "鄄城县"},
    {"id": 6, "name": "中共鄄城县委宣传部", "type": "党委", "level": "县级", "parent": "中共鄄城县委员会", "location": "鄄城县"},
    {"id": 7, "name": "中共鄄城县委政法委员会", "type": "党委", "level": "县级", "parent": "中共鄄城县委员会", "location": "鄄城县"},
    {"id": 8, "name": "中共鄄城县委办公室", "type": "党委", "level": "县级", "parent": "中共鄄城县委员会", "location": "鄄城县"},
    {"id": 9, "name": "中共鄄城县委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共鄄城县委员会", "location": "鄄城县"},
    {"id": 10, "name": "鄄城县公安局", "type": "政府", "level": "县级", "parent": "鄄城县人民政府", "location": "鄄城县"},
    {"id": 11, "name": "鄄城县人大常委会", "type": "人大", "level": "县级", "parent": "菏泽市人大常委会", "location": "鄄城县"},
    {"id": 12, "name": "鄄城县政协", "type": "政协", "level": "县级", "parent": "菏泽市政协", "location": "鄄城县"},
]

# ── 任职 ──────────────────────────────────────────────────────────
positions = [
    # 孙伟
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2021-12", "end_date": "present", "rank": "正县级", "note": "前任袁红兵调离后接任"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "2020-05", "end_date": "2021-12", "rank": "正县级", "note": "由鄄城县县长升任县委书记"},
    # 邓兆朋
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2022-01", "end_date": "present", "rank": "正县级", "note": "前任孙伟升任县委书记后接任"},
    # 尚彦龙
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李沉静
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 温雪梅
    {"person_id": 5, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 黄金果
    {"person_id": 6, "org_id": 5, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王海龙
    {"person_id": 7, "org_id": 6, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 庞红宇
    {"person_id": 8, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张伯新
    {"person_id": 9, "org_id": 8, "title": "县委常委、县委办公室主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王志荣
    {"person_id": 10, "org_id": 9, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 曹传杰
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 赵少林
    {"person_id": 12, "org_id": 10, "title": "副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张广兵
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 袁红兵（前任县委书记）
    {"person_id": 14, "org_id": 1, "title": "县委书记", "start_date": "2016-12", "end_date": "2021-12", "rank": "正县级", "note": "前任县委书记，后调离"},
]

# ── 关系 ──────────────────────────────────────────────────────────
relationships = [
    # 孙伟 — 邓兆朋（上下级：书记—县长）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长搭班", "overlap_org": "中共鄄城县委员会 / 鄄城县人民政府", "overlap_period": "2022-01至今"},
    # 孙伟 — 尚彦龙（上下级：书记—副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—县委副书记搭班", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    # 孙伟 — 袁红兵（前后任）
    {"person_a": 1, "person_b": 14, "type": "predecessor_successor", "context": "袁红兵调离后孙伟接任县委书记", "overlap_org": "中共鄄城县委员会", "overlap_period": "2021-12"},
    # 邓兆朋 — 孙伟（前后任：县长）
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor", "context": "孙伟升任书记后邓兆朋接任县长", "overlap_org": "鄄城县人民政府", "overlap_period": "2022-01"},
    # 李沉静 — 邓兆朋（上下级：常务副县长协助县长）
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "常务副县长—县长", "overlap_org": "鄄城县人民政府", "overlap_period": ""},
    # 黄金果 — 孙伟（上下级：组织部长受书记领导）
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate", "context": "组织部长—县委书记", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    # 温雪梅 — 孙伟（上下级：纪委书记受县委领导）
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate", "context": "纪委书记—县委书记", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    # 所有县委常委之间（共事关系）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 10, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "县委常委会同事", "overlap_org": "中共鄄城县委员会", "overlap_period": ""},
]

# ── 构建 ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="鄄城县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
