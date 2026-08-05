#!/usr/bin/env python3
"""Build the Xiuwen County (修文县, Guiyang, Guizhou) personnel relation network.

Creates SQLite DB + GEXF graph for 修文县 leadership network.

Investigation: guizhou_修文县  (as of 2026-08-05)
Core targets: 县委书记陈禹 & 县长张传皓
Also covers: 前任书记(谢国波/管庆良)、县委/县政府班子、跨地州交流(黔南→贵阳)。
"""

import sys
from pathlib import Path

_START = Path(__file__).resolve()
for _p in (_START, *_START.parents):
    if (_p / "gov_relation").is_dir():
        sys.path.insert(0, str(_p))
        break

from gov_relation.runner import run_build  # noqa: E402

STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "修文县_network.db"
GEXF_PATH = STAGING / "修文县_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "陈禹",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1977-10",
        "birthplace": "贵州福泉",
        "education": "大学",
        "party_join": "2001-06",
        "work_start": "1998-08",
        "current_post": "县委书记、修文经济开发区党工委书记(兼)",
        "current_org": "中共修文县委",
        "source": "百度百科/澎湃新闻/贵州省管干部任前公示",
    },
    {
        "id": 2,
        "name": "张传皓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "山东长清",
        "education": "法学学士(贵州大学)/工程硕士",
        "party_join": "1996-12",
        "work_start": "1997-07",
        "current_post": "县委副书记、县长、修文经开区党工委副书记/管委会主任(兼)",
        "current_org": "修文县人民政府",
        "source": "百度百科/修文县人民政府门户网",
    },
    {
        "id": 3,
        "name": "谢国波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-06",
        "birthplace": "",
        "education": "大学/工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "贵阳市农业农村局(乡村振兴局、生态移民局)党委委员、副局长(保留正县长级)",
        "current_org": "贵阳市农业农村局",
        "source": "百度百科/澎湃新闻",
    },
    {
        "id": 4,
        "name": "管庆良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "修文县委原书记(2024-05 落马；2024-11 双开)",
        "current_org": "",
        "source": "贵州省纪委监委/中新网",
    },
    {
        "id": 5,
        "name": "邓谦",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "湖北武汉",
        "education": "文学硕士(中国社会科学院)",
        "party_join": "",
        "work_start": "2008-08",
        "current_post": "修文县委原副书记、县长(2021-2023)",
        "current_org": "",
        "source": "网易/贵州网络广播电视台",
    },
    {
        "id": 6,
        "name": "韩禄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-11",
        "birthplace": "河南洛阳",
        "education": "法学博士",
        "party_join": "",
        "work_start": "2012-09",
        "current_post": "贵阳市粮食和物资储备局党组书记、局长",
        "current_org": "贵阳市粮食和物资储备局",
        "source": "百度百科/贵阳市粮食和物资储备局官网",
    },
    {
        "id": 7,
        "name": "吕志强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "修文县人民政府",
        "source": "修文县人民政府门户网/中共贵阳市委统战部",
    },
    {
        "id": 8,
        "name": "唐开文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委宣传部部长",
        "current_org": "中共修文县委",
        "source": "修文县人民政府门户网/中共贵阳市委统战部",
    },
    {
        "id": 9,
        "name": "吴小强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长(2021时期)",
        "current_org": "中共修文县委",
        "source": "修文县人民政府门户网",
    },
    {
        "id": 10,
        "name": "韩远勤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "修文县人民政府",
        "source": "修文县人大常委会决定任免名单",
    },
    {
        "id": 11,
        "name": "刘春祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长(分管自然资源、林业)",
        "current_org": "修文县人民政府",
        "source": "修文县人民政府门户网",
    },
    {
        "id": 12,
        "name": "曾杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "修文县人民政府",
        "source": "修文县人大常委会2025-05任命名单",
    },
    {
        "id": 13,
        "name": "赵明军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长(曾任修文县农业农村局局长)",
        "current_org": "修文县人民政府",
        "source": "百度百科",
    },
    {
        "id": 14,
        "name": "王义飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "修文县人民政府",
        "source": "修文县人民政府门户网",
    },
    {
        "id": 15,
        "name": "冯斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "修文县人大常委会",
        "source": "贵阳人大网",
    },
    {
        "id": 16,
        "name": "冯涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "分管环保副县长(2023时期)",
        "current_org": "修文县人民政府",
        "source": "修文县林长制办公室通知",
    },
    {
        "id": 17,
        "name": "朱启军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原副县长(2025-05 免职)",
        "current_org": "",
        "source": "修文县人大常委会2025-05-28决定任免名单",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共修文县委", "type": "党委", "level": "县", "parent": "中共贵阳市委", "location": "贵州贵阳修文县"},
    {"id": 2, "name": "修文县人民政府", "type": "政府", "level": "县", "parent": "贵阳市人民政府", "location": "贵州贵阳修文县"},
    {"id": 3, "name": "修文县人大常委会", "type": "人大", "level": "县", "parent": "贵阳市人大常委会", "location": "贵州贵阳修文县"},
    {"id": 4, "name": "修文经济开发区", "type": "开发区", "level": "县", "parent": "修文县人民政府", "location": "贵州贵阳修文县"},
    {"id": 5, "name": "黔南州委组织部", "type": "党委", "level": "地市", "parent": "中共黔南州委", "location": "贵州黔南"},
    {"id": 6, "name": "黔南州统计局", "type": "政府", "level": "地市", "parent": "黔南州人民政府", "location": "贵州黔南"},
    {"id": 7, "name": "黔南州发展和改革委员会", "type": "政府", "level": "地市", "parent": "黔南州人民政府", "location": "贵州黔南"},
    {"id": 8, "name": "贵阳市市场监督管理局", "type": "政府", "level": "地市", "parent": "贵阳市人民政府", "location": "贵州贵阳"},
    {"id": 9, "name": "贵阳市农业农村局", "type": "政府", "level": "地市", "parent": "贵阳市人民政府", "location": "贵州贵阳"},
    {"id": 10, "name": "贵阳市粮食和物资储备局", "type": "政府", "level": "地市", "parent": "贵阳市人民政府", "location": "贵州贵阳"},
    {"id": 11, "name": "贵阳市南明区委", "type": "党委", "level": "市辖区", "parent": "中共贵阳市委", "location": "贵州贵阳南明区"},
    {"id": 12, "name": "贵阳市委办公厅", "type": "党委", "level": "地市", "parent": "中共贵阳市委", "location": "贵州贵阳"},
    {"id": 13, "name": "贵州省纪委监委", "type": "纪委", "level": "省", "parent": "", "location": "贵州贵阳"},
]

# ── Positions ─────────────────────────────────────────────────────────────
positions = [
    # 陈禹
    {"person_id": 1, "org_id": 1, "title": "县委书记、修文经开区党工委书记(兼)", "start_date": "2025-03", "end_date": "", "rank": "正县", "note": "2026-08拟任市(州)党委常委"},
    {"person_id": 1, "org_id": 7, "title": "州发改委(粮食和物资储备局、能源局)主任/局长", "start_date": "2023-12", "end_date": "2025-03", "rank": "", "note": "黔南州"},
    {"person_id": 1, "org_id": 6, "title": "州统计局局长", "start_date": "2021-07", "end_date": "2023-12", "rank": "", "note": "黔南州"},
    {"person_id": 1, "org_id": 1, "title": "惠水县委常委、常务副县长", "start_date": "2019", "end_date": "2021-07", "rank": "", "note": "黔南州惠水县"},
    {"person_id": 1, "org_id": 1, "title": "龙里县委常委、组织部部长", "start_date": "2017", "end_date": "2019", "rank": "", "note": "黔南州龙里县", "confidence": "plausible"},
    # 张传皓
    {"person_id": 2, "org_id": 2, "title": "县长(2024-09-19当选)", "start_date": "2024-07", "end_date": "", "rank": "正县", "note": "2024-07-24代县长"},
    {"person_id": 2, "org_id": 2, "title": "县委常委、副县长(常务，正县长级)", "start_date": "2022-10", "end_date": "2024-07", "rank": "正县", "note": "分管常务工作"},
    {"person_id": 2, "org_id": 4, "title": "修文经开区管委会主任", "start_date": "2022", "end_date": "2024", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "贵阳市人民政府副秘书长", "start_date": "2019", "end_date": "2022", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "南明区委组织部(街道起步)", "start_date": "1997", "end_date": "2019", "rank": "", "note": "南明区遵义路街道→区委组织部"},
    # 谢国波
    {"person_id": 3, "org_id": 9, "title": "党委委员、副局长(保留正县长级)", "start_date": "2025-03", "end_date": "", "rank": "正县", "note": "贵阳市农业农村局"},
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2024-06", "end_date": "2025-03", "rank": "正县", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "县委副书记、县长", "start_date": "2023-01", "end_date": "2024-06", "rank": "正县", "note": "接任邓谦"},
    {"person_id": 3, "org_id": 8, "title": "党委书记、局长", "start_date": "2020", "end_date": "2023-01", "rank": "正县", "note": "贵阳市场监督管理局"},
    # 管庆良 (风险信号)
    {"person_id": 4, "org_id": 1, "title": "县委书记", "start_date": "2020", "end_date": "2024-05", "rank": "正县", "note": "2024-05落马"},
    # 邓谦
    {"person_id": 5, "org_id": 2, "title": "县长", "start_date": "2021-06", "end_date": "2023-01", "rank": "正县", "note": "2021-06当选"},
    {"person_id": 5, "org_id": 11, "title": "花溪区委副书记(保留正县级)", "start_date": "2020-12", "end_date": "2021-06", "rank": "正县", "note": ""},
    # 韩禄
    {"person_id": 6, "org_id": 10, "title": "贵阳市粮食和物资储备局局长", "start_date": "2025", "end_date": "", "rank": "正县", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委副书记、县委深改委副主任", "start_date": "2022", "end_date": "2024", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "2021-12", "end_date": "2022", "rank": "", "note": ""},
    # 班子 (分工级)
    {"person_id": 7, "org_id": 2, "title": "常务副县长、县委常委", "start_date": "", "end_date": "", "rank": "", "note": "人事、财政、审计"},
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委、组织部部长(2021)", "start_date": "2021", "end_date": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "2025-05", "end_date": "", "rank": "", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长(自然资源、林业)", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "2025-05", "end_date": "", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长(环保,2023)", "start_date": "2023", "end_date": "", "rank": "", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "2025-05-28", "rank": "", "note": "免职"},
]

# ── Relationships ─────────────────────────────────────────────────────────
relationships = [
    # 县委书记 → 县长 (搭班子)
    {"person_a": 1, "person_b": 2, "type": "搭班子", "context": "2025-03起 陈禹任县委书记、张传皓任县长", "overlap_org": "修文县党政班子", "overlap_period": "2025-03至今"},
    # 前任书记 → 现任书记 (交接)
    {"person_a": 3, "person_b": 1, "type": "交接", "context": "谢国波→陈禹 2025-03 县委书记交接", "overlap_org": "中共修文县委", "overlap_period": "2025-03"},
    # 落马书记 → 继任
    {"person_a": 4, "person_b": 3, "type": "交接/风险", "context": "管庆良落马后谢国波接任县委书记", "overlap_org": "中共修文县委", "overlap_period": "2024-06"},
    # 前任县长
    {"person_a": 5, "person_b": 3, "type": "交接", "context": "邓谦→谢国波 2023-01 县长交接", "overlap_org": "修文县人民政府", "overlap_period": "2023-01"},
    # 常务副县长 → 县长 从属
    {"person_a": 7, "person_b": 2, "type": "从属", "context": "吕志强(常务)协助张传皓(县长)分管人事/财政/审计", "overlap_org": "修文县人民政府", "overlap_period": "2024至今"},
    # 宣传部长 → 县委
    {"person_a": 8, "person_b": 1, "type": "同班", "context": "唐开文组织部内宣传,隶属县委常委会", "overlap_org": "中共修文县委", "overlap_period": "2024至今"},
    # 副书记→县委
    {"person_a": 6, "person_b": 1, "type": "同班", "context": "韩禄曾任县委副书记(2022-2024)", "overlap_org": "中共修文县委", "overlap_period": "2022-2024"},
    # 县人大常委会主任
    {"person_a": 15, "person_b": 2, "type": "政府与人大", "context": "冯斌(人大主任)与县政府班子分工监督", "overlap_org": "修文县人大与政府", "overlap_period": "2025至今"},
]


def main() -> None:
    run_build(
        slug="修文县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    import sqlite3 as _sq
    conn = _sq.connect(str(DB_PATH))
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("persons", "organizations", "positions", "relationships")}
    conn.close()
    print("修文县 network built:", counts)


if __name__ == "__main__":
    main()