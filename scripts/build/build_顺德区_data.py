#!/usr/bin/env python3
"""Build script for 顺德区 (Shunde District, Foshan, Guangdong) leadership network.

Generated: 2026-07-22
Sources:
  - www.shunde.gov.cn (official government website - 领导班子 page)
  - zh.wikipedia.org/wiki/顺德区
"""

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    {
        "id": 1,
        "name": "陈新文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "顺德区委书记",
        "current_org": "中共佛山市顺德区委员会",
        "source": "https://zh.wikipedia.org/wiki/顺德区#政治 (verified as current区委书记)",
    },
    {
        "id": 2,
        "name": "吕园园",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "顺德区区长",
        "current_org": "佛山市顺德区人民政府",
        "source": "https://www.shunde.gov.cn/sdqrmzf/zwgk/jgzn/ldbz/index.html",
    },
    {
        "id": 3,
        "name": "李健荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "大学学历，工学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "佛山市顺德区人民政府",
        "source": "https://www.shunde.gov.cn/sdqrmzf/zwgk/jgzn/ldbz/index.html",
    },
    {
        "id": 4,
        "name": "叶永辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（兼区公安局局长）",
        "current_org": "佛山市顺德区人民政府",
        "source": "https://www.shunde.gov.cn/sdqrmzf/zwgk/jgzn/ldbz/index.html",
    },
    {
        "id": 5,
        "name": "朱凌霞",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1981年2月",
        "birthplace": "",
        "education": "大学学历，法学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "佛山市顺德区人民政府",
        "source": "https://www.shunde.gov.cn/sdqrmzf/zwgk/jgzn/ldbz/index.html",
    },
    {
        "id": 6,
        "name": "陈振浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "在职研究生学历，工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（兼容桂街道党工委书记）",
        "current_org": "佛山市顺德区人民政府",
        "source": "https://www.shunde.gov.cn/sdqrmzf/zwgk/jgzn/ldbz/index.html",
    },
    {
        "id": 7,
        "name": "何翔威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "在职研究生学历，工商管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "佛山市顺德区人民政府",
        "source": "https://www.shunde.gov.cn/sdqrmzf/zwgk/jgzn/ldbz/index.html",
    },
    {
        "id": 8,
        "name": "王德华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "大学学历，文学学士、法学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（兼北滘镇党委书记）",
        "current_org": "佛山市顺德区人民政府",
        "source": "https://www.shunde.gov.cn/sdqrmzf/zwgk/jgzn/ldbz/index.html",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共佛山市顺德区委员会", "type": "党委", "level": "正处级", "parent": "中共佛山市委员会", "location": "佛山市顺德区"},
    {"id": 2, "name": "佛山市顺德区人民政府", "type": "政府", "level": "正处级", "parent": "佛山市人民政府", "location": "佛山市顺德区"},
    {"id": 3, "name": "佛山市公安局顺德分局", "type": "政府", "level": "正科级", "parent": "佛山市公安局", "location": "佛山市顺德区"},
    {"id": 4, "name": "容桂街道党工委", "type": "党委", "level": "正科级", "parent": "中共佛山市顺德区委员会", "location": "佛山市顺德区容桂街道"},
    {"id": 5, "name": "北滘镇党委", "type": "党委", "level": "正科级", "parent": "中共佛山市顺德区委员会", "location": "佛山市顺德区北滘镇"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "顺德区委书记", "start_date": "", "end_date": "present", "rank": "正处级/副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "顺德区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时兼任区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "顺德区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "顺德区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任区公安局局长"},
    {"person_id": 4, "org_id": 3, "title": "区公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "民建会员，非中共党员"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "容桂街道党工委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "北滘镇党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

# Relationships based on organizational overlap and working proximity
RELATIONSHIPS = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记-区长党政正职搭档", "overlap_org": "顺德区四套班子", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    # 区委书记与区委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委常委", "overlap_org": "顺德区委常委会", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    # 区长与常务副区长
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "区长—常务副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    # 区长与其他副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—副区长（公安）", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长—副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    # 同一届政府班子的副区长之间
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "常务副区长与副区长（公安）", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "常务副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "副区长（公安）与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "副区长（公安）与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "副区长（公安）与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "副区长（公安）与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "顺德区人民政府", "overlap_period": "现任", "source": "", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "顺德区_network.db"
GEXF_PATH = GRAPH_DIR / "顺德区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="顺德区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
