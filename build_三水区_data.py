#!/usr/bin/env python3
"""Build script for 三水区 (Sanshui District, Foshan, Guangdong) leadership network.

Generated: 2026-07-22
Sources:
  - www.ss.gov.cn (official government website - 领导班子 page)
  - www.ss.gov.cn/zwgk/ssyw/ (news articles confirming区委书记)
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    {
        "id": 1,
        "name": "吴磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "三水区委书记",
        "current_org": "中共佛山市三水区委员会",
        "source": "https://www.ss.gov.cn/zwgk/ssyw/content/post_7197713.html (confirmed as current区委书记 as of 2026-07-15)",
    },
    {
        "id": 2,
        "name": "黄海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "中央党校研究生、工学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "三水区区长",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/qz/content/post_6269649.html",
    },
    {
        "id": 3,
        "name": "李毅佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "研究生学历、工商管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/fqz/content/post_5899939.html",
    },
    {
        "id": 4,
        "name": "孟建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "大学学历、农业推广硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/fqz/content/post_7128650.html",
    },
    {
        "id": 5,
        "name": "林旋",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学学历、医学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/fqz/content/post_5974704.html",
    },
    {
        "id": 6,
        "name": "钱静瑜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "",
        "education": "大学学历、公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（兼大塘镇党委书记）",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/fqz/content/post_5777133.html",
    },
    {
        "id": 7,
        "name": "关海权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（兼区公安局局长）",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/fqz/content/post_5974705.html",
    },
    {
        "id": 8,
        "name": "谢皓至",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年11月",
        "birthplace": "",
        "education": "研究生学历、税务硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/fqz/content/post_7186841.html",
    },
    {
        "id": 9,
        "name": "蒋佰春",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1984年6月",
        "birthplace": "",
        "education": "大学学历、理学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "佛山市三水区人民政府",
        "source": "https://www.ss.gov.cn/zwgk/jgzn/ldbz/qzf/fqz/content/post_7128653.html",
    },
    {
        "id": 10,
        "name": "杨常青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "佛山市三水区人大常委会",
        "source": "https://www.ss.gov.cn/zwgk/ssyw/content/post_7197713.html",
    },
    {
        "id": 11,
        "name": "苏宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "佛山市三水区政协",
        "source": "https://www.ss.gov.cn/zwgk/ssyw/content/post_7197713.html",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共佛山市三水区委员会", "type": "党委", "level": "正处级", "parent": "中共佛山市委员会", "location": "佛山市三水区"},
    {"id": 2, "name": "佛山市三水区人民政府", "type": "政府", "level": "正处级", "parent": "佛山市人民政府", "location": "佛山市三水区"},
    {"id": 3, "name": "佛山市三水区人大常委会", "type": "人大", "level": "正处级", "parent": "佛山市人大常委会", "location": "佛山市三水区"},
    {"id": 4, "name": "佛山市三水区政协", "type": "政协", "level": "正处级", "parent": "佛山市政协", "location": "佛山市三水区"},
    {"id": 5, "name": "佛山市公安局三水分局", "type": "政府", "level": "正科级", "parent": "佛山市公安局", "location": "佛山市三水区"},
    {"id": 6, "name": "大塘镇党委", "type": "党委", "level": "正科级", "parent": "中共佛山市三水区委员会", "location": "佛山市三水区大塘镇"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "三水区委书记", "start_date": "", "end_date": "present", "rank": "正处级/副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "三水区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时兼任区委副书记、区政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "同时任区政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员，兼大塘镇党委书记"},
    {"person_id": 6, "org_id": 6, "title": "大塘镇党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员，兼区公安局局长"},
    {"person_id": 7, "org_id": 5, "title": "区公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 9, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 10, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# Relationships based on organizational overlap and working proximity
RELATIONSHIPS = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记-区长党政正职搭档", "overlap_org": "三水区四套班子", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区委书记与区委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委常委（常务副区长）", "overlap_org": "三水区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区长与常务副区长
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "区长—常务副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区长与其他副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长—副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—副区长（公安）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长—副区长（挂职）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 同一届政府班子的副区长之间
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "常务副区长与副区长（公安）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "常务副区长与副区长（挂职）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "副区长与副区长（公安）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 9, "type": "同僚", "context": "副区长与副区长（挂职）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "副区长与副区长（公安）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "副区长与副区长（挂职）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副区长与副区长（公安）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 9, "type": "同僚", "context": "副区长与副区长（挂职）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副区长（公安）与副区长", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "副区长（公安）与副区长（挂职）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "副区长与副区长（挂职）", "overlap_org": "三水区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "三水区_network.db"
GEXF_PATH = GRAPH_DIR / "三水区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="三水区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
