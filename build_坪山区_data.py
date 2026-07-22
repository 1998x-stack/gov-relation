#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 坪山区 (Pingshan District), Shenzhen, Guangdong leadership network.

Data sources:
  - https://www.szpsq.gov.cn/zwgk/ldcy/index.html (official government website)
  - https://zh.wikipedia.org/zh-cn/%E5%9D%AA%E5%B1%B1%E5%8C%BA (encyclopedia)
Information currency: 2026-07 (current as of July 2026)
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "坪山区"
BASE = "/workspace/data/xieming/other-codes/gov-relation/data/tmp/guangdong_坪山区"
DB_PATH = f"{BASE}/坪山区_network.db"
GEXF_PATH = f"{BASE}/坪山区_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # ── District Party Secretary ──
    {
        "id": 10, "name": "赵嘉", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区委书记",
        "current_org": "中共深圳市坪山区委员会",
        "source": "https://zh.wikipedia.org/zh-cn/%E5%9D%AA%E5%B1%B1%E5%8C%BA",
    },
    # ── District Mayor (区长) ──
    {
        "id": 1, "name": "张茜", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年8月", "birthplace": "", "education": "研究生学历、经济学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区委副书记、区长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    # ── Executive Deputy Mayor (常务副区长) ──
    {
        "id": 2, "name": "袁虎勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年6月", "birthplace": "", "education": "在职研究生学历、工学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区委常委、常务副区长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    # ── Deputy Mayors ──
    {
        "id": 3, "name": "杨涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年11月", "birthplace": "", "education": "大学学历、经济学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区委常委、副区长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    {
        "id": 4, "name": "林良沛", "gender": "男", "ethnicity": "汉族",
        "birth": "1966年12月", "birthplace": "", "education": "在职研究生学历、管理学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区二级巡视员",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    {
        "id": 5, "name": "费晓愈", "gender": "女", "ethnicity": "汉族",
        "birth": "1971年12月", "birthplace": "", "education": "大学学历、经济学学士",
        "party_join": "民建会员", "work_start": "",
        "current_post": "坪山区人民政府副区长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    {
        "id": 6, "name": "吴志柳", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年7月", "birthplace": "", "education": "研究生学历、史学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区人民政府副区长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    {
        "id": 7, "name": "刘理", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年6月", "birthplace": "", "education": "在职研究生学历、法学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区人民政府副区长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    {
        "id": 8, "name": "金良富", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年6月", "birthplace": "", "education": "研究生学历、理学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区人民政府副区长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
    {
        "id": 9, "name": "赖培勤", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "坪山区人民政府副区长、公安分局局长",
        "current_org": "深圳市坪山区人民政府",
        "source": "https://www.szpsq.gov.cn/zwgk/ldcy/index.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共深圳市坪山区委员会", "type": "党委", "level": "县处级",
     "parent": "中共深圳市委员会", "location": "广东省深圳市坪山区"},
    {"id": 2, "name": "深圳市坪山区人民政府", "type": "政府", "level": "县处级",
     "parent": "深圳市人民政府", "location": "广东省深圳市坪山区"},
    {"id": 3, "name": "坪山区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "深圳市人大常委会", "location": "广东省深圳市坪山区"},
    {"id": 4, "name": "中国人民政治协商会议坪山区委员会", "type": "政协", "level": "县处级",
     "parent": "深圳市政协", "location": "广东省深圳市坪山区"},
    {"id": 5, "name": "中共深圳市坪山区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "", "location": "广东省深圳市坪山区"},
    {"id": 6, "name": "中共深圳市坪山区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共深圳市坪山区委员会", "location": "广东省深圳市坪山区"},
    {"id": 7, "name": "坪山区坪山街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市坪山区人民政府", "location": "广东省深圳市坪山区"},
    {"id": 8, "name": "坪山区坑梓街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市坪山区人民政府", "location": "广东省深圳市坪山区"},
    {"id": 9, "name": "坪山区马峦街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市坪山区人民政府", "location": "广东省深圳市坪山区"},
    {"id": 10, "name": "坪山区碧岭街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市坪山区人民政府", "location": "广东省深圳市坪山区"},
    {"id": 11, "name": "坪山区石井街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市坪山区人民政府", "location": "广东省深圳市坪山区"},
    {"id": 12, "name": "坪山区龙田街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市坪山区人民政府", "location": "广东省深圳市坪山区"},
    {"id": 13, "name": "深圳市公安局坪山分局", "type": "政府", "level": "乡科级",
     "parent": "深圳市公安局", "location": "广东省深圳市坪山区"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 赵嘉 — 区委书记
    {"person_id": 10, "org_id": 1, "title": "坪山区委书记",
     "start_date": "", "end_date": "", "rank": "正局级", "note": ""},
    # 张茜 — 区长/区委副书记
    {"person_id": 1, "org_id": 2, "title": "坪山区委副书记、区长、党组书记",
     "start_date": "2024?", "end_date": "", "rank": "正局级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "坪山区委副书记",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 袁虎勇 — 常务副区长
    {"person_id": 2, "org_id": 2, "title": "区委常委、常务副区长、党组副书记",
     "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    # 杨涛 — 副区长
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长、党组成员",
     "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    # 林良沛 — 二级巡视员
    {"person_id": 4, "org_id": 2, "title": "二级巡视员",
     "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    # 费晓愈 — 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "", "rank": "副局级", "note": "民建会员"},
    # 吴志柳 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    # 刘理 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    # 金良富 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    # 赖培勤 — 副区长兼公安分局局长
    {"person_id": 9, "org_id": 2, "title": "副区长、党组成员，公安分局局长",
     "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    {"person_id": 9, "org_id": 13, "title": "党委书记、局长、督察长",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    # 张茜(区长) — 赵嘉(区委书记)：党政搭档
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "区委书记-区长搭档", "overlap_org": "坪山区委", "overlap_period": ""},
    # 张茜(区长) — 袁虎勇(常务副区长)：工作关系
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区长-常务副区长工作关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    # 张茜(区长) — 各副区长：上下级关系
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "上下级关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "上下级关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "上下级关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "上下级关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "上下级关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "上下级关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "上下级关系", "overlap_org": "坪山区政府", "overlap_period": ""},
    # 袁虎勇(常务副区长) — 赵嘉(区委书记)：区委常委关系
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "区委常委关系", "overlap_org": "坪山区委", "overlap_period": ""},
    # 赖培勤 —— 公安分局：分管公安工作
    {"person_a": 9, "person_b": 13, "type": "overlap",
     "context": "分管公安工作", "overlap_org": "坪山区政府", "overlap_period": ""},
]

# ── Run Build ────────────────────────────────────────────────────────────
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
    print(f"Done: {SLUG} network built.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
