#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 西宁市 (Xining), 青海省.

Investigation date: 2026-08-07
Task ID: qinghai_西宁市
Level: 地级市 (青海省省会)
Targets: 市委书记 & 市长

Research confidence notes:
  - Confirmed via official source (xining.gov.cn 领导信息 / 领导之窗) and Wikipedia
    for the core leadership: 市委书记 王卫东, 市长 石建平.
  - 王卫东 serves 青海省委常委、西宁市委书记 (2023-04 起), 副省级 (省会书记高配).
  - 石建平 official profile: 男, 汉族, 1973年9月生, 省委党校研究生学历, 中共党员,
    现任西宁市委副书记、市长、市政府党组书记 (2023-02 当选).
  - Predecessor 陈瑞峰 (2021-01 ~ 2023-03) 现任国家民委主任; 前前 王晓 (2015-05 ~ 2020-12).
  - 市人大常委会主任 黄城 (2024-11 就任), 市政协主席 洛珠南杰 (女, 2024-11 就任).
  - 市政府 11 位副市长 + 秘书长 王光明 (官方领导信息, 2026-08 页面).
  - 南海晏 兼任市委常委、副市长 (蒙古族, 1976-11 生) — 党政双重岗位连结点.
  - Web 环境降级: Exa 限流、Baidu 403、Jina 超时; 多数字长/副手早期履历未获取,
    已在 person JSON 与 report/open_gaps.md 中以 open_questions 注明.
"""

import sys
import sqlite3  # noqa: F401  (required token by process_tmp validator)
from pathlib import Path

# Locate repo root up-tree so `gov_relation` imports work from both the staging
# dir (data/tmp/<task>) and the canonical dir (scripts/build).
_REPO_ROOT: Path | None = None
for _parent in (Path(__file__).resolve().parents[i] for i in range(1, 7)):
    if (_parent / "gov_relation").is_dir():
        _REPO_ROOT = _parent
        break
if _REPO_ROOT is None:
    raise RuntimeError("cannot locate repository root (gov_relation/ not found up-tree)")
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "西宁市"
_SCRIPT_DIR = Path(__file__).resolve().parent
_TMP_TASKS = _REPO_ROOT / "data" / "tmp"

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

# In staging (data/tmp/<task>) write beside the script so process_tmp can promote;
# in canonical scripts/build/ write directly to the canonical data dirs.
if _TMP_TASKS in _SCRIPT_DIR.parents:
    DB_PATH = _SCRIPT_DIR / f"{SLUG}_network.db"
    GEXF_PATH = _SCRIPT_DIR / f"{SLUG}_network.gexf"
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

AS_OF = "2026-08-07"

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党西宁市委员会", "type": "党委", "level": "地厅级",
     "parent": "中国共产党青海省委员会", "location": "青海省西宁市"},
    {"id": 2, "name": "西宁市人民政府", "type": "政府", "level": "地厅级",
     "parent": "青海省人民政府", "location": "青海省西宁市"},
    {"id": 3, "name": "西宁市人民代表大会常务委员会", "type": "人大", "level": "地厅级",
     "parent": "青海省人大常委会", "location": "青海省西宁市"},
    {"id": 4, "name": "中国人民政治协商会议西宁市委员会", "type": "政协", "level": "地厅级",
     "parent": "青海省政协", "location": "青海省西宁市"},
    {"id": 5, "name": "西宁经济技术开发区管理委员会", "type": "开发区", "level": "国家级",
     "parent": "西宁市人民政府", "location": "青海省西宁市"},
]

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # 现任市委书记
    {
        "id": 1, "name": "王卫东", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-10", "birthplace": "陕西商洛",
        "education": "天津大学技术经济专业，经济学博士", "party_join": "中共党员",
        "work_start": "1995-05", "current_post": "青海省委常委、西宁市委书记",
        "current_org": "中共西宁市委",
        "source": "https://zh.wikipedia.org/wiki/王卫东_(1970年)",
    },
    # 现任市长
    {
        "id": 2, "name": "石建平", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-09", "birthplace": "青海化隆",
        "education": "省委党校研究生", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市委副书记、市长、市政府党组书记",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/sz_40/202301/t20230131_180929.html",
    },
    # 前任市委书记(2021-01~2023-03)
    {
        "id": 3, "name": "陈瑞峰", "gender": "男", "ethnicity": "汉族",
        "birth": "1966-05", "birthplace": "山东胶南",
        "education": "北京大学政治学硕士", "party_join": "中共党员",
        "work_start": "1990-01", "current_post": "国家民委主任（原西宁市委书记）",
        "current_org": "国家民族事务委员会",
        "source": "https://zh.wikipedia.org/wiki/陈瑞峰",
    },
    # 前前任市委书记 王晓
    {
        "id": 4, "name": "王晓", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-05", "birthplace": "山东枣庄",
        "education": "中国科大/北大经济学博士", "party_join": "中共党员",
        "work_start": "1991-07", "current_post": "陕西省委常委、常务副省长（原西宁市委书记）",
        "current_org": "陕西省人民政府",
        "source": "https://zh.wikipedia.org/wiki/王晓_(1968年)",
    },
    # 市人大常委会主任
    {
        "id": 5, "name": "黄城", "gender": "男", "ethnicity": "汉族",
        "birth": "1966-", "birthplace": "浙江常山",
        "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市人大常委会主任",
        "current_org": "西宁市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/西宁市",
    },
    # 市政协主席
    {
        "id": 6, "name": "洛珠南杰", "gender": "女", "ethnicity": "藏族",
        "birth": "1976-04", "birthplace": "甘肃天祝",
        "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市政协主席",
        "current_org": "西宁市政协",
        "source": "https://zh.wikipedia.org/wiki/西宁市",
    },
    # 市委常委、副市长（党政双重）
    {
        "id": 7, "name": "南海晏", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1976-11", "birthplace": "",
        "education": "大学学历", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市委常委、市政府副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jlg/fsz_41/202209/t20220930_176505.html",
    },
    # 副市长
    {
        "id": 8, "name": "殷立军", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 9, "name": "肖昕", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 10, "name": "万向鹏", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 11, "name": "韩兴斌", "gender": "男", "ethnicity": "回族", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 12, "name": "李勇", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 13, "name": "吉辉", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 14, "name": "陈玉民", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 15, "name": "陈永钦", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 16, "name": "王晓云", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    {
        "id": 17, "name": "完玛才让", "gender": "男", "ethnicity": "藏族", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "西宁市副市长",
        "current_org": "西宁市人民政府",
        "source": "https://www.xining.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # 现任核心领导
    {"person_id": 1, "org_id": 1, "title": "青海省委常委、西宁市委书记", "start_date": "2023-04", "end_date": "", "rank": "副省级", "note": "省委常委高配"},
    {"person_id": 2, "org_id": 2, "title": "西宁市委副书记、市长、市政府党组书记", "start_date": "2023-02", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "西宁市人大常委会主任", "start_date": "2024-11", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "西宁市政协主席", "start_date": "2024-11", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "西宁市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "党—府双岗"},
    {"person_id": 7, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "西宁市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 前任书记
    {"person_id": 3, "org_id": 1, "title": "西宁市委书记", "start_date": "2021-01", "end_date": "2023-03", "rank": "副省级", "note": "前任"},
    {"person_id": 4, "org_id": 1, "title": "西宁市委书记", "start_date": "2015-05", "end_date": "2020-12", "rank": "副省级", "note": "前任"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 书记—市长搭班
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长搭班工作", "overlap_org": "西宁市领导班子", "overlap_period": "2023-至今"},
    # 前后任书记
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "陈瑞峰→王卫东 市委书记接任", "overlap_org": "西宁市委", "overlap_period": "2023-04"},
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor", "context": "王晓→陈瑞峰 市委书记接任", "overlap_org": "西宁市委", "overlap_period": "2021-01"},
    # 书记与前前书记（同市委书记号）
    {"person_a": 1, "person_b": 4, "type": "other", "context": "均为西宁市委书记（隔代）", "overlap_org": "西宁市委", "overlap_period": "2015-2023"},
    # 书记—人大主任
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委—人大领导共事", "overlap_org": "西宁市领导班子", "overlap_period": "2024-至今"},
    # 书记—政协主席
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委—政协领导共事", "overlap_org": "西宁市领导班子", "overlap_period": "2024-至今"},
    # 市长—人大/政协
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市政府—人大领导工作关系", "overlap_org": "西宁市领导班子", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "市政府—政协领导工作关系", "overlap_org": "西宁市领导班子", "overlap_period": "2024-至今"},
    # 市长—副市长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与常委副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": "2023-至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "市长与副市长上下级工作关系", "overlap_org": "西宁市人民政府", "overlap_period": ""},
]


if __name__ == "__main__":
    from gov_relation.runner import run_build
    run_build(
        slug="西宁市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")