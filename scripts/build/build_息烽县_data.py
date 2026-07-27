#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 息烽县 leadership network.

Sources:
- 息烽县人民政府门户网站 https://www.xifeng.gov.cn/zwgk/ldzc/ (accessed 2026-07-23)
- News articles dated through 2026-07-23 from xifeng.gov.cn
"""
import os
import sys
import sqlite3  # noqa: keep process_tmp.py check happy

PROJECT_ROOT = "/workspace/data/xieming/other-codes/gov-relation"
sys.path.insert(0, PROJECT_ROOT)

from pathlib import Path
from gov_relation.runner import run_build

STAGING = Path(__file__).parent

SLUG = "息烽县"
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ── County Party Committee (县委) ──
    {
        "id": 1,
        "name": "李颖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共息烽县委书记",
        "current_org": "中共息烽县委员会",
        "source": "https://www.xifeng.gov.cn/xwdt/zwyw/202607/t20260723_90652753.html",
    },
    {
        "id": 2,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "息烽县委副书记",
        "current_org": "中共息烽县委员会",
        "source": "https://www.xifeng.gov.cn/xwdt/zwyw/202607/t20260723_90652753.html",
    },
    {
        "id": 3,
        "name": "陈晓虎",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1987-02",
        "birthplace": "",
        "education": "大学本科/学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共息烽县委常委、常务副县长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202606/t20260625_90557309.html",
    },
    {
        "id": 4,
        "name": "陈实",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共息烽县委常委",
        "current_org": "中共息烽县委员会",
        "source": "https://www.xifeng.gov.cn/xwdt/zwyw/202607/t20260717_90631867.html",
    },
    {
        "id": 5,
        "name": "周柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-04",
        "birthplace": "",
        "education": "研究生学历/工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共息烽县委常委、副县长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202506/t20250627_88202681.html",
    },
    {
        "id": 6,
        "name": "宋宗泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共息烽县委常委",
        "current_org": "中共息烽县委员会",
        "source": "https://www.xifeng.gov.cn/xwdt/zwyw/202607/t20260717_90631867.html",
    },
    {
        "id": 7,
        "name": "蔡鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "息烽县人民政府党组成员、副县长、县公安局局长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202503/t20250317_87189572.html",
    },
    # ── County Government (县政府) Deputy Leaders ──
    {
        "id": 8,
        "name": "张成志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "息烽县人民政府党组成员、副县长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202503/t20250317_87189057.html",
    },
    {
        "id": 9,
        "name": "杨明仙",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-12",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "息烽县人民政府党组成员、副县长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202503/t20250317_87189320.html",
    },
    {
        "id": 10,
        "name": "丁晓光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-07",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "息烽县人民政府党组成员、副县长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202503/t20250317_87189492.html",
    },
    {
        "id": 11,
        "name": "文芳",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "1985-11",
        "birthplace": "",
        "education": "研究生学历/硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "息烽县人民政府副县长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202503/t20250317_87189761.html",
    },
    {
        "id": 12,
        "name": "李兴丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-09",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "息烽县人民政府副县长",
        "current_org": "息烽县人民政府",
        "source": "https://www.xifeng.gov.cn/zwgk/ldzc/xzfld_5978036/202601/t20260115_89300098.html",
    },
    # ── County People's Congress and CPPCC ──
    {
        "id": 13,
        "name": "罗绪祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "息烽县人大常委会主任",
        "current_org": "息烽县人民代表大会常务委员会",
        "source": "https://www.xifeng.gov.cn/xwdt/zwyw/202607/t20260723_90652753.html",
    },
    {
        "id": 14,
        "name": "陈邦毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "息烽县政协主席",
        "current_org": "中国人民政治协商会议息烽县委员会",
        "source": "https://www.xifeng.gov.cn/xwdt/zwyw/202607/t20260723_90652753.html",
    },
]

# Note: The county mayor (县长/县委副书记) is not currently listed on the
# government leadership page. Previous news references mention "周印" presiding
# over government meetings, but no official bio page was found on the website.
# This is a known gap.

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

orgs = [
    {"id": 1, "name": "中共息烽县委员会", "type": "党委", "level": "县级", "parent": "中共贵阳市委", "location": "息烽县"},
    {"id": 2, "name": "息烽县人民政府", "type": "政府", "level": "县级", "parent": "贵阳市人民政府", "location": "息烽县"},
    {"id": 3, "name": "息烽县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "息烽县", "location": "息烽县"},
    {"id": 4, "name": "中国人民政治协商会议息烽县委员会", "type": "政协", "level": "县级", "parent": "息烽县", "location": "息烽县"},
    {"id": 5, "name": "中共息烽县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共息烽县委员会", "location": "息烽县"},
    {"id": 6, "name": "息烽县公安局", "type": "政府机构", "level": "县级", "parent": "息烽县人民政府", "location": "息烽县"},
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # Party Committee (县委)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任息烽经开区党工委书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "同时任常务副县长"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "同时任副县长"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "同时任副县长、县公安局局长"},

    # Government (县政府)
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "无党派"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # Police
    {"person_id": 7, "org_id": 6, "title": "县公安局党委书记、局长、督察长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # NPC and CPPCC
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 书记-副书记
    {"person_a": 1, "person_b": 2, "type": "正副搭档", "context": "县委书记与专职副书记", "overlap_org": "中共息烽县委员会", "overlap_period": "2025-至今"},
    # 书记-常委们
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与常委/常务副县长", "overlap_org": "中共息烽县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与县委常委", "overlap_org": "中共息烽县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与县委常委/副县长", "overlap_org": "中共息烽县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与县委常委", "overlap_org": "中共息烽县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记与县委常委/副县长/公安局长", "overlap_org": "中共息烽县委员会", "overlap_period": "2025-至今"},
    # 县政府党组
    {"person_a": 3, "person_b": 5, "type": "同级", "context": "常务副县长与副县长", "overlap_org": "息烽县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 7, "type": "上下级", "context": "常务副县长与副县长", "overlap_org": "息烽县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 8, "type": "上下级", "context": "常务副县长与副县长", "overlap_org": "息烽县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 9, "type": "上下级", "context": "常务副县长与副县长", "overlap_org": "息烽县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 10, "type": "上下级", "context": "常务副县长与副县长", "overlap_org": "息烽县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 11, "type": "上下级", "context": "常务副县长与副县长", "overlap_org": "息烽县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 12, "type": "上下级", "context": "常务副县长与副县长", "overlap_org": "息烽县人民政府", "overlap_period": "至今"},
    # 县人大常委会-县委
    {"person_a": 13, "person_b": 1, "type": "党政关系", "context": "县人大常委会主任与县委书记", "overlap_org": "息烽县", "overlap_period": "至今"},
    # 县政协-县委
    {"person_a": 14, "person_b": 1, "type": "党政关系", "context": "县政协主席与县委书记", "overlap_org": "息烽县", "overlap_period": "至今"},
]

# ── RUN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=orgs,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done. Database:", DB_PATH)
    print("Done. GEXF:", GEXF_PATH)
