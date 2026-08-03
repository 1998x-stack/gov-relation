#!/usr/bin/env python3
"""乐清市 — 领导班子关系网络数据构建脚本

Sources:
- 乐清市政府官网领导之窗: https://www.yueqing.gov.cn/col/col1321311/index.html
- 乐清新闻(市委常委会, 2026-08-03)
- 乐清市人大常委会议新闻(2026-08-03)
- 乐清市政府人事任免通知(2026-07-20)

Generated: 2026-08-04
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "乐清市_network.db"
GEXF_PATH = GRAPH_DIR / "乐清市_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # id=1: 市委书记
    {
        "id": 1,
        "name": "戴旭强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐清市委书记",
        "current_org": "中共乐清市委",
        "source": "乐清市融媒体中心新闻(2026-07/08)",
    },
    # id=2: 市长 胡立左
    {
        "id": 2,
        "name": "胡立左",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市委副书记、市长",
        "current_org": "乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1321311/hlz/index.html",
    },
    # id=3: 林益正
    {
        "id": 3,
        "name": "林益正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市委副书记、常务副市长",
        "current_org": "中共乐清市委/乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1229621879/index.html",
    },
    # id=4: 叶序锋
    {
        "id": 4,
        "name": "叶序锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "",
        "education": "大学学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市委常委、副市长",
        "current_org": "中共乐清市委/乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1229610125/index.html",
    },
    # id=5: 王人骏
    {
        "id": 5,
        "name": "王人骏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市委常委、副市长(挂职)",
        "current_org": "乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1321311/wrj/index.html",
    },
    # id=6: 卓赛龙
    {
        "id": 6,
        "name": "卓赛龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-06",
        "birthplace": "",
        "education": "硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市副市长(对口支援理县)",
        "current_org": "乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1229621883/index.html",
    },
    # id=7: 陈健
    {
        "id": 7,
        "name": "陈健",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-02",
        "birthplace": "",
        "education": "大学学历、硕士学位",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "乐清市副市长",
        "current_org": "乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1229610123/index.html",
    },
    # id=8: 黄伟
    {
        "id": 8,
        "name": "黄伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市副市长、公安局局长",
        "current_org": "乐清市人民政府/乐清市公安局",
        "source": "https://www.yueqing.gov.cn/col/col1321311/hw/index.html",
    },
    # id=9: 陈万钦
    {
        "id": 9,
        "name": "陈万钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-07",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市副市长",
        "current_org": "乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1229621881/index.html",
    },
    # id=10: 陈晓炬
    {
        "id": 10,
        "name": "陈晓炬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市副市长",
        "current_org": "乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1229748344/index.html",
    },
    # id=11: 郑济斌
    {
        "id": 11,
        "name": "郑济斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市副市长",
        "current_org": "乐清市人民政府",
        "source": "https://www.yueqing.gov.cn/col/col1229621885/index.html",
    },
    # id=12: 潘云夫
    {
        "id": 12,
        "name": "潘云夫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市人大常委会主任",
        "current_org": "乐清市人大常委会",
        "source": "乐清市融媒体中心新闻稿(2026-08)",
    },
    # id=13: 陈向东
    {
        "id": 13,
        "name": "陈向东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐清市政协主席",
        "current_org": "乐清市政协",
        "source": "乐清市融媒体中心新闻稿(2026-08)",
    },
    # id=14: 徐建兵 (前任市委书记)
    {
        "id": 14,
        "name": "徐建兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任乐清市委书记）",
        "current_org": "",
        "source": "公开新闻报道/百度百科",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共乐清市委", "type": "党委", "level": "县级", "parent": "中共温州市委", "location": "浙江省温州市乐清市"},
    {"id": 2, "name": "乐清市人民政府", "type": "政府", "level": "县级", "parent": "温州市人民政府", "location": "浙江省温州市乐清市"},
    {"id": 3, "name": "乐清市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "浙江省温州市乐清市"},
    {"id": 4, "name": "乐清市政协", "type": "政协", "level": "县级", "parent": "", "location": "浙江省温州市乐清市"},
    {"id": 5, "name": "乐清市公安局", "type": "政府", "level": "正科级", "parent": "乐清市人民政府/温州市公安局", "location": "浙江省温州市乐清市"},
    {"id": 6, "name": "中共乐清市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共乐清市委/中共温州市纪委", "location": "浙江省温州市乐清市"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 戴旭强
    {"person_id": 1, "org_id": 1, "title": "乐清市委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 胡立左
    {"person_id": 2, "org_id": 1, "title": "乐清市委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "乐清市市长", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 林益正
    {"person_id": 3, "org_id": 1, "title": "乐清市委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "乐清市常务副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 叶序锋
    {"person_id": 4, "org_id": 1, "title": "乐清市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "乐清市副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王人骏
    {"person_id": 5, "org_id": 1, "title": "乐清市委常委(挂职)", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026年7月任命"},
    {"person_id": 5, "org_id": 2, "title": "乐清市副市长(挂职)", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026年7月30日市人大常委会任命"},
    # 卓赛龙
    {"person_id": 6, "org_id": 2, "title": "乐清市副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "对口支援四川省理县"},
    # 陈健
    {"person_id": 7, "org_id": 2, "title": "乐清市副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "九三学社"},
    # 黄伟
    {"person_id": 8, "org_id": 2, "title": "乐清市副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "乐清市公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼市委政法委副书记"},
    # 陈万钦
    {"person_id": 9, "org_id": 2, "title": "乐清市副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 陈晓炬
    {"person_id": 10, "org_id": 2, "title": "乐清市副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 郑济斌
    {"person_id": 11, "org_id": 2, "title": "乐清市副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 潘云夫
    {"person_id": 12, "org_id": 3, "title": "乐清市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 陈向东
    {"person_id": 13, "org_id": 4, "title": "乐清市政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 徐建兵 (前任市委书记)
    {"person_id": 14, "org_id": 1, "title": "乐清市委书记(前任)", "start_date": "", "end_date": "", "rank": "正县级", "note": "戴旭强前任"},
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    # 书记-市长 (党政一把手)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "戴旭强任乐清市委书记，胡立左任市长，党政正职搭档关系", "overlap_org": "中共乐清市委/乐清市人民政府", "overlap_period": ""},
    # 书记-副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "戴旭强与林益正: 书记+市委副书记", "overlap_org": "中共乐清市委", "overlap_period": ""},
    # 市长-常务副
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "胡立左与林益正: 市长+常务副市长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    # 市长-副市长们
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "胡立左与叶序锋: 市长+副市长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "胡立左与王人骏: 市长+副市长(挂职)", "overlap_org": "乐清市人民政府", "overlap_period": "2026-07起"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "胡立左与卓赛龙: 市长+副市长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "胡立左与陈健: 市长+副市长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "胡立左与黄伟: 市长+副市长/公安局长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "胡立左与陈万钦: 市长+副市长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "胡立左与陈晓炬: 市长+副市长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "胡立左与郑济斌: 市长+副市长", "overlap_org": "乐清市人民政府", "overlap_period": ""},
    # 常委班子内部
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "林益正与叶序锋: 市委副书记+常委", "overlap_org": "中共乐清市委", "overlap_period": ""},
    # 人大-政府
    {"person_a": 12, "person_b": 2, "type": "overlap", "context": "潘云夫(人大主任)与胡立左(市长): 一府一委两院监督关系", "overlap_org": "乐清市", "overlap_period": ""},
    # 政协-政府
    {"person_a": 13, "person_b": 2, "type": "overlap", "context": "陈向东(政协主席)与胡立左(市长): 政治协商关系", "overlap_org": "乐清市", "overlap_period": ""},
    # 前任-现任
    {"person_a": 14, "person_b": 1, "type": "predecessor_successor",
     "context": "徐建兵→戴旭强: 乐清市委书记交接", "overlap_org": "中共乐清市委", "overlap_period": ""},
]


# ── Build ────────────────────────────────────────────────────────────
def main():
    from gov_relation.runner import run_build

    run_build(
        slug="乐清市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB:  {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}")
    print(f"Orgs: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")


if __name__ == "__main__":
    main()