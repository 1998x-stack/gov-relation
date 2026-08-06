#!/usr/bin/env python3
"""Build script for 武汉市 (Wuhan) cadre leadership network.

Task: hubei_武汉市 — targets 市委书记 & 市长 (city-level, 副省级城市).
As-of date: 2026-08-06.

Key sources:
- 武汉市人民政府门户 https://www.wuhan.gov.cn/ (official; current roster via 时政要闻 2026-08-06)
- Baidu Baike: 郭元强 (predecessor 市委书记 2021.09–2025.10)
- Local repo: build_宜昌市_data.py / data/persons (熊征宇 was 宜昌市委书记 before 武汉)
- Local repo: report/20260806-湖北省… (王忠林 武汉市委书记 2020-2021)

CONFIDENCE NOTES
- 熊征宇 = 现任武汉市委书记 (confirmed: official portal 2026-08-06 参与调研/会议; was 宜昌市委书记)
- 盛阅春 = 现任武汉市长 (confirmed: official portal 2026-08-06)
- 郭元强 = 前任武汉市委书记 (2021.09–2025.10), 现省人大常委会副主任 (confirmed via Baike)
- 程用文 = 更早武汉市长 (~2021–2023), 履历推断
- 王忠林 = 更早武汉市委书记 (2020–2021), 后省长/省委书记/省人大主任 (confirmed via Hubei report)
- 熊征宇 exact appointment date & 盛阅春 exact appointment date = OPEN GAP
"""

import json
import sqlite3
import sys
from pathlib import Path

# Locate repo root (holds gov_relation/) robustly across staging/scripts/build/root locations.
_root = Path(__file__).resolve()
while not (_root / "gov_relation").is_dir() and _root != _root.parent:
    _root = _root.parent
sys.path.insert(0, str(_root))

from gov_relation.runner import run_build

AS_OF = "2026-08-06"
SLUG = "武汉市"

TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "武汉市_network.db"
GEXF_PATH = TMP / "武汉市_network.gexf"

persons = [
    # ── 现任 ──
    {
        "id": 10,
        "name": "熊征宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武汉市委书记",
        "current_org": "中共武汉市委员会",
        "source": "https://www.wuhan.gov.cn/",
    },
    {
        "id": 11,
        "name": "盛阅春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964",
        "birthplace": "浙江萧山",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武汉市长",
        "current_org": "武汉市人民政府",
        "source": "https://www.wuhan.gov.cn/",
    },
    # ── 前任 ──
    {
        "id": 12,
        "name": "郭元强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-07",
        "birthplace": "河南光山",
        "education": "研究生学历，在职工学博士",
        "party_join": "1986-06",
        "work_start": "1988-07",
        "current_post": "湖北省人大常委会副主任",
        "current_org": "湖北省人大常委会",
        "source": "百度百科（郭元强）",
    },
    {
        "id": 13,
        "name": "程用文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任武汉市长",
        "current_org": "武汉市人民政府",
        "source": "武汉市人民政府门户（历任信息）",
    },
    {
        "id": 14,
        "name": "王忠林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-08",
        "birthplace": "山东费县",
        "education": "法学学士、管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湖北省人大常委会主任",
        "current_org": "湖北省人大常委会",
        "source": "data/persons/20260806-湖北省-...王忠林.json",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共武汉市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中国共产党湖北省委员会",
        "location": "武汉市",
    },
    {
        "id": 2,
        "name": "武汉市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "湖北省人民政府",
        "location": "武汉市",
    },
    {
        "id": 3,
        "name": "湖北省人大常委会",
        "type": "人大",
        "level": "省级",
        "parent": "中国共产党湖北省委员会",
        "location": "武汉市",
    },
    {
        "id": 4,
        "name": "中共宜昌市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党湖北省委员会",
        "location": "宜昌市",
    },
    {
        "id": 5,
        "name": "中国共产党湖北省委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "武汉市",
    },
]

positions = [
    # 熊征宇 — 现任武汉市委书记
    {"person_id": 10, "org_id": 1, "title": "武汉市委书记", "start_date": "", "end_date": "present", "rank": "副省级", "note": "现号；曾任宜昌市委书记"},
    {"person_id": 10, "org_id": 4, "title": "宜昌市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "已于黄剑雄接任；此前任职"},
    # 盛阅春 — 现任武汉市长
    {"person_id": 11, "org_id": 2, "title": "武汉市长", "start_date": "", "end_date": "present", "rank": "副省级", "note": "现任职"},
    # 郭元强 — 前任武汉市委书记
    {"person_id": 12, "org_id": 1, "title": "武汉市委书记", "start_date": "2021-09", "end_date": "2025-10", "rank": "副省级", "note": "曾兼湖北省委常委"},
    {"person_id": 12, "org_id": 3, "title": "湖北省人大常委会副主任", "start_date": "2026-01", "end_date": "present", "rank": "副省级", "note": "2025-10后转任省人大"},
    # 程用文 — 前任武汉市长
    {"person_id": 13, "org_id": 2, "title": "武汉市长", "start_date": "", "end_date": "", "rank": "副省级", "note": "前任市长"},
    # 王忠林 — 更早武汉市委书记
    {"person_id": 14, "org_id": 1, "title": "武汉市委书记", "start_date": "2020-02", "end_date": "2021-04", "rank": "副省级", "note": "疫情期间临危受命"},
    {"person_id": 14, "org_id": 3, "title": "湖北省人大常委会主任", "start_date": "2025-01", "end_date": "present", "rank": "正部级", "note": "后任省长/省委书记"},
]

relationships = [
    # 现任党政一把手搭档
    {"person_a": 10, "person_b": 11, "type": "党政搭档",
     "context": "熊征宇（市委书记）与盛阅春（市长）组成现武汉党政一把手搭档",
     "overlap_org": "中共武汉市委员会/武汉市人民政府", "overlap_period": "2025至今"},
    # 党政正职继任链（书记线）
    {"person_a": 10, "person_b": 12, "type": "predecessor_successor",
     "context": "熊征宇接任郭元强（2025-10）为武汉市委书记",
     "overlap_org": "中共武汉市委员会", "overlap_period": "2025"},
    {"person_a": 12, "person_b": 14, "type": "predecessor_successor",
     "context": "郭元强接任王忠林（2021）为武汉市委书记",
     "overlap_org": "中共武汉市委员会", "overlap_period": "2021"},
    # 党政正职继任链（市长线）
    {"person_a": 11, "person_b": 13, "type": "predecessor_successor",
     "context": "盛阅春任武汉市长，程用文为前任市长",
     "overlap_org": "武汉市人民政府", "overlap_period": ""},
    # 跨市/同级调任
    {"person_a": 10, "person_b": 13, "type": "cross_city_transfer",
     "context": "熊征宇先后主政宜昌、武汉两地（跨市干部），与市长线干部同属湖北省级干部序列",
     "overlap_org": "中国共产党湖北省委员会", "overlap_period": ""},
    # 省级与市级关系
    {"person_a": 14, "person_b": 13, "type": "superior_subordinate",
     "context": "王忠林任武汉市委书记（2020-2021）期间，程用文任武汉市市长代理/就任，受其领导",
     "overlap_org": "中共武汉市委员会", "overlap_period": "2020-2021"},
]

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
    conn = sqlite3.connect(str(DB_PATH))
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("persons", "organizations", "positions", "relationships")}
    conn.close()
    print(f"Built {DB_PATH} and {GEXF_PATH}")
    print(f"persons={len(persons)} orgs={len(organizations)} positions={len(positions)} relationships={len(relationships)}")
    print("DB counts:", counts)