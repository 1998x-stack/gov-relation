#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 惠阳区 leadership network.

Data source: www.huiyang.gov.cn (official government website)
Information currency: 2026-07 (current as of July 2026)
"""
import os
from gov_relation.runner import run_build
from gov_relation.paths import REPO_ROOT

SLUG = "惠阳区"

# Canonical paths (used by process_tmp.py validation)
DB_PATH = REPO_ROOT / "data/database/惠阳区_network.db"
GEXF_PATH = REPO_ROOT / "data/graph/惠阳区_network.gexf"

# Write to staging directory for validation before promotion
STAGING = REPO_ROOT / "data/tmp/guangdong_惠阳区"
os.makedirs(STAGING, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════
persons = [
    # ── 区委领导班子 (Party Committee) ──
    {
        "id": 1, "name": "谭星海", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委书记",
        "current_org": "中共惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 2, "name": "何国斌", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委副书记、区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 3, "name": "关瑞华", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委副书记",
        "current_org": "中共惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 4, "name": "欧阳惠鼎", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委、副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 5, "name": "陶伟军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委",
        "current_org": "中共惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 6, "name": "庞海燕", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委",
        "current_org": "中共惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 7, "name": "阳柱", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委",
        "current_org": "中共惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 8, "name": "唐伟", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委",
        "current_org": "中共惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 9, "name": "陈镇城", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委、纪委书记",
        "current_org": "中共惠阳区纪律检查委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 10, "name": "张贤", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委",
        "current_org": "中共惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 11, "name": "罗国庆", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区委常委、副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    # ── 区人大常委会 (People's Congress) ──
    {
        "id": 12, "name": "廖升安", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区人大常委会主任候选人",
        "current_org": "惠阳区人民代表大会常务委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    # ── 区政协 (People's Political Consultative Conference) ──
    {
        "id": 13, "name": "黄智勇", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    # ── 区政府副区长 (Deputy District Mayors) ──
    {
        "id": 14, "name": "林建彬", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 15, "name": "许伟浩", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 16, "name": "李智敏", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 17, "name": "邹清雄", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 18, "name": "邬少英", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 19, "name": "王晓庆", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 20, "name": "丁付平", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区副区长",
        "current_org": "惠阳区人民政府",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    # ── 区人大副主任 (NPC Deputy Chairs) ──
    {
        "id": 21, "name": "杨旭先", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区人大常委会副主任",
        "current_org": "惠阳区人民代表大会常务委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 22, "name": "罗文送", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区人大常委会副主任",
        "current_org": "惠阳区人民代表大会常务委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 23, "name": "杨桂平", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区人大常委会副主任",
        "current_org": "惠阳区人民代表大会常务委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 24, "name": "刘运忠", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区人大常委会副主任",
        "current_org": "惠阳区人民代表大会常务委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 25, "name": "陈忠", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区人大常委会副主任",
        "current_org": "惠阳区人民代表大会常务委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 26, "name": "曾伟荣", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区人大常委会副主任",
        "current_org": "惠阳区人民代表大会常务委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    # ── 区政协副主席 (PPCC Deputy Chairs) ──
    {
        "id": 27, "name": "钟水和", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 28, "name": "胡冠文", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 29, "name": "陈燕雄", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 30, "name": "彭贵和", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 31, "name": "林志标", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 32, "name": "何立", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 33, "name": "周小军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 34, "name": "陈湘", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区政协副主席",
        "current_org": "政协惠阳区委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    # ── 纪委副书记 ──
    {
        "id": 35, "name": "陈兆辉", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区纪委副书记",
        "current_org": "中共惠阳区纪律检查委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 36, "name": "郑雪琼", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "惠阳区纪委副书记",
        "current_org": "中共惠阳区纪律检查委员会",
        "source": "https://www.huiyang.gov.cn/zwgk/ldzc/",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共惠阳区委员会", "type": "党委", "level": "县处级", "parent": "中共惠州市委员会", "location": "惠州市惠阳区"},
    {"id": 2, "name": "惠阳区人民政府", "type": "政府", "level": "县处级", "parent": "惠州市人民政府", "location": "惠州市惠阳区"},
    {"id": 3, "name": "惠阳区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "惠州市人民代表大会常务委员会", "location": "惠州市惠阳区"},
    {"id": 4, "name": "政协惠阳区委员会", "type": "政协", "level": "县处级", "parent": "政协惠州市委员会", "location": "惠州市惠阳区"},
    {"id": 5, "name": "中共惠阳区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共惠州市纪律检查委员会", "location": "惠州市惠阳区"},
]

# ═══════════════════════════════════════════════════════════════════════
# Positions (Current)
# ═══════════════════════════════════════════════════════════════════════
positions = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "惠阳区委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "惠阳区委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任区长"},
    {"person_id": 3, "org_id": 1, "title": "惠阳区委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "惠阳区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任副区长"},
    {"person_id": 5, "org_id": 1, "title": "惠阳区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "惠阳区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "惠阳区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "惠阳区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "惠阳区委常委、纪委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "惠阳区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "惠阳区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任副区长"},
    # 区政府
    {"person_id": 2, "org_id": 2, "title": "惠阳区区长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "惠阳区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 区人大
    {"person_id": 12, "org_id": 3, "title": "惠阳区人大常委会主任候选人", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "惠阳区人大常委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "惠阳区人大常委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "惠阳区人大常委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 3, "title": "惠阳区人大常委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 25, "org_id": 3, "title": "惠阳区人大常委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 26, "org_id": 3, "title": "惠阳区人大常委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 区政协
    {"person_id": 13, "org_id": 4, "title": "惠阳区政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 27, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 29, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 30, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 31, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 32, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 33, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 34, "org_id": 4, "title": "惠阳区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 区纪委
    {"person_id": 9, "org_id": 5, "title": "惠阳区纪委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 35, "org_id": 5, "title": "惠阳区纪委副书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 36, "org_id": 5, "title": "惠阳区纪委副书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
]

# ═══════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════
relationships = [
    # ── 区委书记 ↔ 区长 (core leadership pair) ──
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "谭星海为惠阳区委书记，何国斌为惠阳区委副书记、区长，为区委核心搭档关系",
        "overlap_org": "中共惠阳区委员会",
        "overlap_period": "2026",
    },
    # ── 区委书记 → 区委副书记 ──
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "谭星海与关瑞华在区委领导班子中共事",
        "overlap_org": "中共惠阳区委员会",
        "overlap_period": "2026",
    },
    # ── 区长 → 副区长们 ──
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "何国斌（区长）与欧阳惠鼎（副区长）在区政府中共事",
        "overlap_org": "惠阳区人民政府",
        "overlap_period": "2026",
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "何国斌（区长）与罗国庆（副区长）在区政府中共事",
        "overlap_org": "惠阳区人民政府",
        "overlap_period": "2026",
    },
    # ── 纪委书记隶属于区委 ──
    {
        "person_a": 1, "person_b": 9,
        "type": "superior_subordinate",
        "context": "谭星海（区委书记）与陈镇城（区委常委、纪委书记）在区委领导班子中共事",
        "overlap_org": "中共惠阳区委员会",
        "overlap_period": "2026",
    },
    # ── 区委常委之间 ──
    {
        "person_a": 4, "person_b": 11,
        "type": "overlap",
        "context": "欧阳惠鼎与罗国庆均为区委常委、副区长",
        "overlap_org": "中共惠阳区委员会、惠阳区人民政府",
        "overlap_period": "2026",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# Run Build
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=STAGING / "惠阳区_network.db",
        gexf_path=STAGING / "惠阳区_network.gexf",
    )
