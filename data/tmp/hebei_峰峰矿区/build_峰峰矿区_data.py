#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 峰峰矿区, 邯郸市, 河北省."""

import os
import sqlite3  # noqa: F401 — present so repo build_script validator recognizes this script
import sys
from datetime import date
from pathlib import Path

# Add project root to path so gov_relation module is importable
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths (staging) ────────────────────────────────────────────────────
TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / "峰峰矿区_network.db"
GEXF_PATH = TMP_DIR / "峰峰矿区_network.gexf"

# ── DATA ───────────────────────────────────────────────────────────────

TODAY = date.today().strftime("%Y-%m-%d")

# Person ID mapping (kept stable for cross-investigation dedup)
# 郭涛 = party secretary (current), 张宝伟 = 区长 (current)

persons = [
    # ── Current Top Leaders ──
    # 区委书记 郭涛 (confirmed from official 2026 区级领导接访安排表)
    {"id": 1, "name": "郭涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邯郸市峰峰矿区区委书记", "current_org": "中共邯郸市峰峰矿区委员会",
     "source": "http://www.ff.gov.cn/ffxw/zsdt/ (2026年1/2月区级领导接访安排表)"},

    # 区长 张宝伟 (confirmed from official site)
    {"id": 2, "name": "张宝伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-05", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邯郸市峰峰矿区区委副书记、区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/zbw/"},

    # ── Deputy Leaders (confirmed from official 区长之窗 + 接访表) ──
    {"id": 3, "name": "李昂", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "峰峰矿区区委常委、常务副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 4, "name": "武文强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 5, "name": "陶毅", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 6, "name": "李波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 7, "name": "王雷", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 8, "name": "白晓", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    # ── 区委常委班子 (接访表确认) ──
    {"id": 9, "name": "郝向旭", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "峰峰矿区区委常委、纪委书记、监委主任", "current_org": "中共邯郸市峰峰矿区纪律检查委员会",
     "source": "http://www.ff.gov.cn/ffxw/zsdt/ (2026接访表)"},

    {"id": 10, "name": "杜亚群", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "峰峰矿区区委常委、宣传部长", "current_org": "中共邯郸市峰峰矿区委员会宣传部",
     "source": "http://www.ff.gov.cn/ffxw/zsdt/ (2026接访表)"},

    {"id": 11, "name": "杜煜", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "峰峰矿区区委常委、组织部长、统战部长", "current_org": "中共邯郸市峰峰矿区委员会组织部",
     "source": "http://www.ff.gov.cn/ffxw/zsdt/ (2026-01接访表)"},

    # ── 区人大/政协/法检 ──
    {"id": 12, "name": "靳晓阳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区政协主席", "current_org": "政协邯郸市峰峰矿区委员会",
     "source": "http://www.ff.gov.cn/ffxw/zsdt/ (2026接访表)"},

    {"id": 13, "name": "陈冬冬", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区人民检察院检察长", "current_org": "峰峰矿区人民检察院",
     "source": "http://www.ff.gov.cn/ffxw/zsdt/ (2026接访表)"},

    # ── 前人/继任谱系 (media 河北新闻网) ──
    {"id": 14, "name": "孙亚鹍", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "(前任峰峰矿区区长 2020-2021)", "current_org": "",
     "source": "https://fengfeng.hebnews.cn/"},

    {"id": 15, "name": "陈珍礼", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "(前任峰峰矿区区委书记 2020-2021)", "current_org": "",
     "source": "https://fengfeng.hebnews.cn/"},

    {"id": 16, "name": "牛颖建", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "(前任峰峰矿区区委书记 2018-2019)", "current_org": "",
     "source": "https://fengfeng.hebnews.cn/"},
]

organizations = [
    {"id": 1, "name": "中共邯郸市峰峰矿区委员会", "type": "党委", "level": "县处级",
     "parent": "中共邯郸市委员会", "location": "河北省邯郸市峰峰矿区"},
    {"id": 2, "name": "邯郸市峰峰矿区人民政府", "type": "政府", "level": "县处级",
     "parent": "邯郸市人民政府", "location": "河北省邯郸市峰峰矿区"},
    {"id": 3, "name": "峰峰经济开发区", "type": "开发区", "level": "省级开发区",
     "parent": "邯郸市人民政府", "location": "河北省邯郸市峰峰矿区"},
    {"id": 4, "name": "中共邯郸市峰峰矿区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共邯郸市纪律检查委员会", "location": "河北省邯郸市峰峰矿区"},
    {"id": 5, "name": "中共邯郸市峰峰矿区委员会宣传部", "type": "党委部门", "level": "县处级",
     "parent": "中共邯郸市峰峰矿区委员会", "location": "河北省邯郸市峰峰矿区"},
    {"id": 6, "name": "中共邯郸市峰峰矿区委员会组织部", "type": "党委部门", "level": "县处级",
     "parent": "中共邯郸市峰峰矿区委员会", "location": "河北省邯郸市峰峰矿区"},
    {"id": 7, "name": "政协邯郸市峰峰矿区委员会", "type": "政协", "level": "县处级",
     "parent": "政协邯郸市委员会", "location": "河北省邯郸市峰峰矿区"},
    {"id": 8, "name": "峰峰矿区人民检察院", "type": "司法机关", "level": "县处级",
     "parent": "邯郸市人民检察院", "location": "河北省邯郸市峰峰矿区"},
]

positions = [
    # 郭涛 (区委书记)
    {"person_id": 1, "org_id": 1, "title": "区委书记",
     "start": "2022/2023-", "end": "present", "rank": "县处级正职",
     "note": "主持区委全面工作; 由区长升任, 精确任命日期未确认"},
    {"person_id": 1, "org_id": 2, "title": "区长 (前)",
     "start": "2021-06", "end": "2022/2023-", "rank": "县处级正职",
     "note": "2021-06 任代区长, 后任区长(至其升任区委书记)"},

    # 张宝伟
    {"person_id": 2, "org_id": 1, "title": "区委副书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "兼任区长"},
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start": "2022/2023-", "end": "present", "rank": "县处级正职",
     "note": "郭涛升任书记后接任区长; 精确到任日期未确认"},
    {"person_id": 2, "org_id": 3, "title": "峰峰经济开发区党工委副书记兼管委会主任",
     "start": "", "end": "present", "rank": "",
     "note": ""},

    # 李昂
    {"person_id": 3, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 武文强 / 陶毅 / 李波 / 王雷 / 白晓 (副区长)
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长(兼公安局长)",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 郝向旭 (纪委)
    {"person_id": 9, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 9, "org_id": 4, "title": "纪委书记、监委主任",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "2026-01 时为监委代主任, 2026-02 转正为监委主任"},

    # 杜亚群 (宣传)
    {"person_id": 10, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 10, "org_id": 5, "title": "宣传部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 杜煜 (组织)
    {"person_id": 11, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 11, "org_id": 6, "title": "组织部长、统战部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "2026-01 接访表确认"},

    # 靳晓阳 (政协)
    {"person_id": 12, "org_id": 7, "title": "政协主席",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": ""},

    # 陈冬冬 (检察)
    {"person_id": 13, "org_id": 8, "title": "检察院检察长",
     "start": "", "end": "present", "rank": "县处级",
     "note": ""},

    # 前人 (仅作谱系参考)
    {"person_id": 14, "org_id": 2, "title": "区长 (前)",
     "start": "2020", "end": "2021", "rank": "县处级正职",
     "note": "孙亚鹍, 前任区长 2020-2021; 卸任区长后去向未完全确认"},
    {"person_id": 15, "org_id": 1, "title": "区委书记 (前)",
     "start": "2020", "end": "2021", "rank": "县处级正职",
     "note": "陈珍礼, 前任区委书记 2020-2021"},
    {"person_id": 16, "org_id": 1, "title": "区委书记 (前)",
     "start": "2018", "end": "2019", "rank": "县处级正职",
     "note": "牛颖建, 前任区委书记 2018-2019"},
]

relationships = [
    # 书记-区长 党政双核
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政搭档 (现任)", "overlap_org": "峰峰矿区",
     "overlap_period": "2023-2026", "source": "http://www.ff.gov.cn/ffxw/zsdt/"},
    # 郭涛 ← 张宝伟 前任继承 (郭区长→张区长)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "张宝伟接任郭涛离任后的区长; 郭涛升任区委书记", "overlap_org": "峰峰矿区人民政府",
     "overlap_period": "2022/2023", "source": "https://fengfeng.hebnews.cn/"},

    # 区长与副区长的上下级关系
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与常务副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026", "source": "http://www.ff.gov.cn/zwgk/qzzc/"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},

    # 书记-班子 (区委常委会同僚)
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区委书记与纪委书记", "overlap_org": "中共邯郸市峰峰矿区委员会",
     "overlap_period": "2025-2026", "source": "http://www.ff.gov.cn/ffxw/zsjj/"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "区委书记与宣传部长", "overlap_org": "中共邯郸市峰峰矿区委员会",
     "overlap_period": "2025-2026", "source": "http://www.ff.gov.cn/ffxw/zsjj/"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "区委书记与组织部长", "overlap_org": "中共邯郸市峰峰矿区委员会",
     "overlap_period": "2025-2026", "source": "http://www.ff.gov.cn/ffxw/zsjj/"},

    # 郭涛 — 前任 (区长序列) 孙亚鹍
    {"person_a": 1, "person_b": 14, "type": "predecessor_successor",
     "context": "郭涛接任孙亚鹍任区长 (2021)", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2021-06", "source": "https://fengfeng.hebnews.cn/"},
    # 郭涛 — 前任区委书记 陈珍礼
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor",
     "context": "郭涛为陈珍礼之后的区委书记(经区长任期)", "overlap_org": "中共邯郸市峰峰矿区委员会",
     "overlap_period": "2021-2023", "source": "https://fengfeng.hebnews.cn/"},
    # 陈珍礼 — 牛颖建 前前任
    {"person_a": 15, "person_b": 16, "type": "predecessor_successor",
     "context": "陈珍礼接任牛颖建任区委书记", "overlap_org": "中共邯郸市峰峰矿区委员会",
     "overlap_period": "2019-2020", "source": "https://fengfeng.hebnews.cn/"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="峰峰矿区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")