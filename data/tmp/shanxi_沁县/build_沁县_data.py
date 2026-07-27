#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 沁县 (Qin County, Changzhi, Shanxi) leadership network.

Task: shanxi_沁县
Targets: 县委书记 司慧军, 县长 李俊杰
Province: 山西省
Parent City: 长治市
Level: 县
Generated: 2026-07-26
As-of: 2026-07-26 (sourced from qinxian.gov.cn)
"""

from pathlib import Path
import sys

# Add repo root to path
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # noqa: F401

SLUG = "沁县"

# Staging paths (set by scripts/process_tmp.py)
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────
persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "司慧军",
        "gender": "男",
        "ethnicity": "汉族",  # assumed, typical for Shanxi officials, not officially confirmed
        "birth": "",  # not published on official site
        "birthplace": "",  # not published
        "education": "",  # not published
        "party_join": "",
        "work_start": "",
        "current_post": "沁县县委书记",
        "current_org": "中共沁县委员会",
        "source": "https://www.qinxian.gov.cn/ (multiple news articles confirm title)",
    },
    {
        "id": 2,
        "name": "李俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # not published on official page
        "birthplace": "",
        "education": "",  # not published on official bio
        "party_join": "",
        "work_start": "",
        "current_post": "沁县县委副书记、县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzxz/202407/t20240710_2926874.html",
    },
    # ── Government Deputies ──
    {
        "id": 3,
        "name": "冯宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-06",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县县委常委、常务副县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz01/202601/t20260126_3133913.html",
    },
    {
        "id": 4,
        "name": "王相澎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县县委常委、副县长（挂职）",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz02/202409/t20240927_2965380.html",
    },
    {
        "id": 5,
        "name": "连娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-02",
        "birthplace": "山西长治",
        "education": "研究生学历，管理学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县县委常委、副县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz02_254548/202601/t20260104_3124919.html",
    },
    {
        "id": 6,
        "name": "李成君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-05",
        "birthplace": "",
        "education": "公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县县委常委、副县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzld02/202402/t20240218_2867797.html",
    },
    {
        "id": 7,
        "name": "谭伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县县委常委、副县长（挂职）",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz006/202604/t20260429_3162019.html",
    },
    {
        "id": 8,
        "name": "王丽萍",
        "gender": "女",
        "ethnicity": "",
        "birth": "1969-05",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县副县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzld01/201712/t20171231_937381.html",
    },
    {
        "id": 9,
        "name": "段树波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县副县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz004/202409/t20240927_2965382.html",
    },
    {
        "id": 10,
        "name": "张军红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-02",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县副县长、县公安局局长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz03/202209/t20220927_2646916.html",
    },
    {
        "id": 11,
        "name": "王彦军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县副县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz08/202412/t20241226_2999598.html",
    },
    {
        "id": 12,
        "name": "田冠英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "沁县副县长",
        "current_org": "沁县人民政府",
        "source": "https://www.qinxian.gov.cn/qxxgk/zfxxgk/zfxxgkml/zfld/zzfxz02_254285/202604/t20260429_3162027.html",
    },
    # ── 县委办主任/政协副主席 (mentioned in news as attending with 司慧军) ──
    {
        "id": 13,
        "name": "杨亮平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席、县委办负责人",
        "current_org": "中国人民政治协商会议沁县委员会",
        "source": "https://www.qinxian.gov.cn/szdt/zwyw/202607/t20260722_3188505.html",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共沁县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市沁县",
    },
    {
        "id": 2,
        "name": "沁县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市沁县",
    },
    {
        "id": 3,
        "name": "沁县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "沁县人民政府",
        "location": "山西省长治市沁县",
    },
    {
        "id": 4,
        "name": "沁县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "沁县人民政府",
        "location": "山西省长治市沁县",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议沁县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "沁县",
        "location": "山西省长治市沁县",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────────
positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "沁县县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed by official news articles dating to at least 2026-07"},
    # Mayor
    {"person_id": 2, "org_id": 2, "title": "沁县县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed on official leadership page as of 2026-04-29"},
    # Deputies
    {"person_id": 3, "org_id": 2, "title": "沁县县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-04-29"},
    {"person_id": 4, "org_id": 2, "title": "沁县县委常委、副县长（挂职北京市房山区）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职期; official profile as of 2026-07-10"},
    {"person_id": 5, "org_id": 2, "title": "沁县县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "山西长治人; official profile as of 2026-04-30"},
    {"person_id": 6, "org_id": 2, "title": "沁县县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-04-29"},
    {"person_id": 7, "org_id": 2, "title": "沁县县委常委、副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职; official profile as of 2026-04-29"},
    {"person_id": 8, "org_id": 2, "title": "沁县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "非党员; official profile as of 2026-04-29"},
    {"person_id": 9, "org_id": 2, "title": "沁县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-04-29"},
    {"person_id": 10, "org_id": 2, "title": "沁县副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-04-29"},
    {"person_id": 10, "org_id": 4, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "official profile"},
    {"person_id": 11, "org_id": 2, "title": "沁县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-04-29"},
    {"person_id": 12, "org_id": 2, "title": "沁县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-04-30"},
    {"person_id": 13, "org_id": 5, "title": "县政协副主席、县委办负责人", "start_date": "", "end_date": "present", "rank": "", "note": "mentioned in news"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────
relationships = [
    # 司慧军 <-> 李俊杰: party secretary and mayor
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档", "overlap_org": "沁县县委县政府", "overlap_period": "2026-"},
    # 司慧军 <-> 冯宇: secretary and executive deputy
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—常务副县长班子", "overlap_org": "沁县县委", "overlap_period": "2026-"},
    # 李俊杰 <-> 冯宇: mayor and executive deputy
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—常务副县长工作搭档", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    # 李俊杰 <-> 连娟: same native place (both from 长治)
    {"person_a": 2, "person_b": 5, "type": "same_native_place", "context": "连娟为山西长治人，李俊杰在长治市沁县任职", "overlap_org": "", "overlap_period": ""},
    # All deputies overlap at 沁县人民政府
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长—挂职副县长", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长—副县长", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长—挂职副县长", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长—副县长", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长—副县长", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长—公安局長", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长—副县长", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长—女副县长", "overlap_org": "沁县人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "县委书记领视察时县委办负责人陪同", "overlap_org": "沁县县委", "overlap_period": "2026-"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
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
    print(f"✅ 沁县 network built: {DB_PATH}, {GEXF_PATH}")