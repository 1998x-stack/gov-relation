#!/usr/bin/env python3
"""Build script for 泸县 (Lux County) leadership network — 泸州市, 四川省."""

import sys
from pathlib import Path

# The script lives in scripts/build/, need to go up to repo root
_BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR


# ── Persons (id must be integer, unique across this script) ──────────────

persons = [
    # 1–2: Top leaders
    {
        "id": 1,
        "name": "李仁军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共泸县委员会",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 2,
        "name": "张程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "泸州纳溪",
        "education": "党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    # 3–12: 县委/县政府/人大/政协 leaders
    {
        "id": 3,
        "name": "吕先",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共泸县委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409091",
    },
    {
        "id": 4,
        "name": "周仁树",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 5,
        "name": "熊茂材",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共泸县委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409160",
    },
    {
        "id": 6,
        "name": "王先奎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共泸县委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409183",
    },
    {
        "id": 7,
        "name": "章磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "泸县人民代表大会常务委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409136",
    },
    {
        "id": 8,
        "name": "吴雪松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议泸县委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409091",
    },
    # 9–16: Other county vice-mayors (from gov website)
    {
        "id": 9,
        "name": "高烨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 10,
        "name": "侯雪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 11,
        "name": "文静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 12,
        "name": "马晋宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 13,
        "name": "刘静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 14,
        "name": "向阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 15,
        "name": "徐波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸县人民政府",
        "source": "https://www.luxian.gov.cn/ldzc",
    },
    {
        "id": 16,
        "name": "王斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸县委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409091",
    },
    {
        "id": 17,
        "name": "蔡飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸县委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409091",
    },
    {
        "id": 18,
        "name": "田林峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸县委员会",
        "source": "https://www.luxian.gov.cn/zwgk/zwdt/zwyw/content_409091",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共泸县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共泸州市委员会",
        "location": "四川省泸州市泸县",
    },
    {
        "id": 2,
        "name": "泸县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "泸州市人民政府",
        "location": "四川省泸州市泸县",
    },
    {
        "id": 3,
        "name": "泸县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "",
        "location": "四川省泸州市泸县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议泸县委员会",
        "type": "政协",
        "level": "县",
        "parent": "",
        "location": "四川省泸州市泸县",
    },
    {
        "id": 5,
        "name": "泸县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "",
        "location": "四川省泸州市泸县",
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议泸县委员会",
        "type": "政协",
        "level": "县",
        "parent": "",
        "location": "四川省泸州市泸县",
    },
    {
        "id": 7,
        "name": "泸州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "",
        "location": "四川省泸州市",
    },
]

# ── Positions (Many-to-Many person→org) ─────────────────────────────────

positions = [
    # 李仁军
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "同时担任泸州市人大常委会副主任"},
    {"person_id": 1, "org_id": 7, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼职"},
    # 张程
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "县委副书记、县长"},
    # 吕先
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 周仁树
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 熊茂材
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王先奎
    {"person_id": 6, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 章磊
    {"person_id": 7, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 吴雪松
    {"person_id": 8, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 高烨
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 侯雪
    {"person_id": 10, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职"},
    # 文静
    {"person_id": 11, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职"},
    # 马晋宇
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘静
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 向阳
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 徐波
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王斌
    {"person_id": 16, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 蔡飞
    {"person_id": 17, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 田林峰
    {"person_id": 18, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ── Relationships (person↔person) ────────────────────────────────────────

relationships = [
    # Core leadership team: 李仁军 & 张程
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档", "overlap_org": "泸县", "overlap_period": "2026年前后"},
    # 李仁军 & 吕先
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—县委副书记", "overlap_org": "中共泸县委员会", "overlap_period": "2026年前后"},
    # 张程 & 周仁树
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长—常务副县长", "overlap_org": "泸县人民政府", "overlap_period": "2026年前后"},
    # 李仁军 & 熊茂材
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记—政法委书记", "overlap_org": "中共泸县委员会", "overlap_period": "2026年前后"},
    # 李仁军 & 王先奎
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记—统战部长", "overlap_org": "中共泸县委员会", "overlap_period": "2026年前后"},
    # 李仁军 & 章磊
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记—人大主任", "overlap_org": "泸县", "overlap_period": "2026年前后"},
    # 李仁军 & 吴雪松
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记—政协主席", "overlap_org": "泸县", "overlap_period": "2026年前后"},
    # 张程 & 吕先
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县委副书记—县长（党政班子）", "overlap_org": "中共泸县委员会/泸县人民政府", "overlap_period": "2026年前后"},
    # 周仁树 & 其他副县长
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "常务副县长—副县长", "overlap_org": "泸县人民政府", "overlap_period": "2026年前后"},
    {"person_a": 4, "person_b": 12, "type": "overlap", "context": "常务副县长—副县长", "overlap_org": "泸县人民政府", "overlap_period": "2026年前后"},
    {"person_a": 4, "person_b": 13, "type": "overlap", "context": "常务副县长—副县长", "overlap_org": "泸县人民政府", "overlap_period": "2026年前后"},
    {"person_a": 4, "person_b": 14, "type": "overlap", "context": "常务副县长—副县长", "overlap_org": "泸县人民政府", "overlap_period": "2026年前后"},
    {"person_a": 4, "person_b": 15, "type": "overlap", "context": "常务副县长—副县长", "overlap_org": "泸县人民政府", "overlap_period": "2026年前后"},
    # 县委常委班子
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共泸县委员会", "overlap_period": "2026年前后"},
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共泸县委员会", "overlap_period": "2026年前后"},
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共泸县委员会", "overlap_period": "2026年前后"},
]

# ── Execute ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    run_build(
        slug="泸县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "泸县_network.db",
        gexf_path=GRAPH_DIR / "泸县_network.gexf",
        overwrite=True,
    )
    print("Build complete.")
    print(f"  DB:   {DATABASE_DIR / '泸县_network.db'}")
    print(f"  GEXF: {GRAPH_DIR / '泸县_network.gexf'}")