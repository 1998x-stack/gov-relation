#!/usr/bin/env python3
"""六盘水市领导班子工作关系网络生成脚本.

基于六盘水市人民政府门户网站 (www.gzlps.gov.cn) 领导之窗发布的现任领导班子名单，
构建六盘水市委、市政府、市人大、市政协核心领导的 SQLite 数据库与 GEXF 关系图。

数据时间锚点：截至 2026-08-05
核心现任任职信息以六盘水市人民政府门户「领导之窗」（官方、confirmed）为直接依据；
早期履历细节因外部检索受限，仅收录官方所确认的锚点，其余列入 open_questions。

来源：
- 六盘水市人民政府门户 领导之窗（https://www.gzlps.gov.cn/zwgk/jcxxgk/ldzc/，2026-08-05 访问）
- 六盘水市人民政府新闻频道（领导活动 / 今日凉都）
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# 项目根目录（脚本位于 data/tmp/<task>/ 时向上三级；被 scripts/process_tmp.py
# 复制到 scripts/build/ 后，再向上两级即可回到仓库根目录）
_HERE = Path(__file__).resolve().parent
if _HERE.name == "build":
    _PROJECT_ROOT = _HERE.parents[1].resolve()
else:
    _PROJECT_ROOT = _HERE.parents[2].resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "六盘水市"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

DB_PATH = _HERE / "六盘水市_network.db"
GEXF_PATH = _HERE / "六盘水市_network.gexf"
URL_LDZC = "https://www.gzlps.gov.cn/zwgk/jcxxgk/ldzc/"

# ── Persons ───────────────────────────────────────────────────────────────
# 1-8：市委班子；9-14：市政府班子；15-16：人大/政协主要领导
PERSONS = [
    # 1 现任市委书记
    {
        "id": 1,
        "name": "李巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "大学、工商管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委书记、六盘水军分区党委第一书记",
        "current_org": "中共六盘水市委员会",
        "source": URL_LDZC + "sw/lw/index.html",
    },
    # 2 现任市委副书记、代理市长
    {
        "id": 2,
        "name": "臧侃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "education": "大学、文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委副书记、市政府党组书记、市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "szf/zk/index.html",
    },
    # 3-9 市委常委会班子
    {
        "id": 3,
        "name": "冯晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委常委",
        "current_org": "中共六盘水市委员会",
        "source": URL_LDZC + "sw/index.html",
    },
    {
        "id": 4,
        "name": "曾晓芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委常委",
        "current_org": "中共六盘水市委员会",
        "source": URL_LDZC + "sw/index.html",
    },
    {
        "id": 5,
        "name": "杨涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委常委、市委秘书长",
        "current_org": "中共六盘水市委员会",
        "source": URL_LDZC + "sw/index.html",
    },
    {
        "id": 6,
        "name": "王银兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委常委",
        "current_org": "中共六盘水市委员会",
        "source": URL_LDZC + "sw/index.html",
    },
    {
        "id": 7,
        "name": "张永嵩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委常委",
        "current_org": "中共六盘水市委员会",
        "source": URL_LDZC + "sw/index.html",
    },
    {
        "id": 8,
        "name": "鲍吉克",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委常委、副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "sw/index.html",
    },
    {
        "id": 9,
        "name": "王相宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委常委、副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "sw/index.html",
    },
    # 10-15 市政府副市长（非常委者）
    {
        "id": 10,
        "name": "方裕谦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "szf/index.html",
    },
    {
        "id": 11,
        "name": "香萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "szf/index.html",
    },
    {
        "id": 12,
        "name": "刘江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "szf/index.html",
    },
    {
        "id": 13,
        "name": "王斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "szf/index.html",
    },
    {
        "id": 14,
        "name": "李大旺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "szf/index.html",
    },
    {
        "id": 15,
        "name": "赵庆强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市副市长",
        "current_org": "六盘水市人民政府",
        "source": URL_LDZC + "szf/index.html",
    },
    # 16 市人大常委会主任
    {
        "id": 16,
        "name": "蒋兴勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市人大常委会主任",
        "current_org": "六盘水市人民代表大会常务委员会",
        "source": URL_LDZC + "srd/index.html",
    },
    # 17 市政协主席
    {
        "id": 17,
        "name": "张二宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市政协主席",
        "current_org": "中国人民政治协商会议六盘水市委员会",
        "source": URL_LDZC + "szx/index.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共六盘水市委员会", "type": "党委", "level": "地厅级", "parent": "中共贵州省委", "location": "贵州省六盘水市"},
    {"id": 2, "name": "六盘水市人民政府", "type": "政府", "level": "地厅级", "parent": "贵州省人民政府", "location": "贵州省六盘水市"},
    {"id": 3, "name": "六盘水市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "贵州省人大常委会", "location": "贵州省六盘水市"},
    {"id": 4, "name": "中国人民政治协商会议六盘水市委员会", "type": "政协", "level": "地厅级", "parent": "贵州省政协", "location": "贵州省六盘水市"},
    {"id": 5, "name": "六盘水军分区", "type": "军事", "level": "师级", "parent": "贵州省军区", "location": "贵州省六盘水市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    # 李巍 — 市委书记（兼任军分区党委第一书记）
    {"person_id": 1, "org_id": 1, "title": "六盘水市委书记", "start_date": "present", "end_date": "present", "rank": "正厅级", "note": "现任；主持市委全面工作，履行全面从严治党'第一责任人'职责"},
    {"person_id": 1, "org_id": 5, "title": "六盘水军分区党委第一书记", "start_date": "present", "end_date": "present", "rank": "正厅级", "note": "官方'宣布六盘水军分区党委第一书记任职大会'报道确认（official）"},
    # 臧侃 — 市委副书记、市长（代理）
    {"person_id": 2, "org_id": 1, "title": "六盘水市委副书记", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "六盘水市政府党组书记、市长", "start_date": "present", "end_date": "present", "rank": "正厅级", "note": "官方'领导之窗'列为市长；新闻报道为'市委副书记、代市长'眉歌（代理市长）"},
    # 市委常委会
    {"person_id": 3, "org_id": 1, "title": "六盘水市委常委", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "六盘水市委常委", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "六盘水市委常委、市委秘书长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 6, "org_id": 1, "title": "六盘水市委常委", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 7, "org_id": 1, "title": "六盘水市委常委", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    # 兼任市委常委的副市长
    {"person_id": 8, "org_id": 2, "title": "六盘水市委常委、副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 9, "org_id": 2, "title": "六盘水市委常委、副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    # 市政府副市长
    {"person_id": 10, "org_id": 2, "title": "六盘水市副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 11, "org_id": 2, "title": "六盘水市副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 12, "org_id": 2, "title": "六盘水市副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 13, "org_id": 2, "title": "六盘水市副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 14, "org_id": 2, "title": "六盘水市副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 15, "org_id": 2, "title": "六盘水市副市长", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "现任"},
    # 人大 / 政协
    {"person_id": 16, "org_id": 3, "title": "六盘水市人大常委会主任", "start_date": "present", "end_date": "present", "rank": "正厅级", "note": "现任"},
    {"person_id": 17, "org_id": 4, "title": "六盘水市政协主席", "start_date": "present", "end_date": "present", "rank": "正厅级", "note": "现任"},
]

# ── Relationships (person <-> person) ─────────────────────────────────────
RELATIONSHIPS = [
    # 市委书记 — 市长（党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "李巍任六盘水市委书记，与市委副书记、代理市长臧侃组成党政一把手搭档", "overlap_org": "六盘水市", "overlap_period": "present"},
    # 书记 — 人大常委会主任（四套班子）
    {"person_a": 1, "person_b": 16, "type": "共事", "context": "市委书记李巍与市人大常委会主任蒋兴勇同为市领导层，共同走访慰问等公务活动", "overlap_org": "六盘水市", "overlap_period": "present"},
    # 书记 — 政协主席（四套班子）
    {"person_a": 1, "person_b": 17, "type": "共事", "context": "市委书记李巍与市政协主席张二宏同为市四套班子主要领导", "overlap_org": "六盘水市", "overlap_period": "present"},
    # 书记 — 各市委常委（市委常委会）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "李巍任市委书记，冯晓明为市委常委，同属市委常委会", "overlap_org": "中共六盘水市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "李巍任市委书记，曾晓芳为市委常委，同属市委常委会", "overlap_org": "中共六盘水市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "李巍任市委书记，杨涛为市委常委兼市委秘书长", "overlap_org": "中共六盘水市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "李巍任市委书记，王银兵为市委常委", "overlap_org": "中共六盘水市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "李巍任市委书记，张永嵩为市委常委", "overlap_org": "中共六盘水市委员会", "overlap_period": "present"},
    # 市长 — 常务副职/副市长（市政府班子）
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "臧侃任市政府党组书记、市长，鲍吉克为市委常委、副市长", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "臧侃任市政府党组书记、市长，王相宇为市委常委、副市长", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "臧侃（市长）与副市长方裕谦同属市政府班子", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "臧侃（市长）与副市长香萍同属市政府班子", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "臧侃（市长）与副市长刘江同属市政府班子", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "臧侃（市长）与副市长王斌同属市政府班子", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "臧侃（市长）与副市长李大旺同属市政府班子", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "臧侃（市长）与副市长赵庆强同属市政府班子", "overlap_org": "六盘水市人民政府", "overlap_period": "present"},
    # 书记 — 市长（党政班子日常工作交集，佐证共同走访慰问）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "2026-07-31李巍、臧侃连同人大、政协主要领导走访慰问驻市部队官兵", "overlap_org": "六盘水市", "overlap_period": "2026-07"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    print("Building Liupanshui (六盘水市) leadership network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    for p in [db_path, gexf_path]:
        if p.exists():
            print(f"  OK {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  MISSING {p.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()