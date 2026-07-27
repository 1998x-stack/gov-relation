#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 沁源县 (Qinyuan County, Changzhi, Shanxi) leadership network.

Task: shanxi_沁源县
Targets: 县委书记 崔峥岭, 县长 郭立东
Province: 山西省
Parent City: 长治市
Level: 县
Generated: 2026-07-26
As-of: 2026-07-26 (sourced from qinyuan.gov.cn)
"""

from pathlib import Path
import sys

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # noqa: F401

SLUG = "沁源县"

# Staging paths
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────
persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "崔峥岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、县委书记",
        "current_org": "中共沁源县委员会",
        "source": "https://www.qinyuan.gov.cn/xwdt/zwyw/202607/t20260724_3189560.html (news article confirms title 市委常委、县委书记)",
    },
    {
        "id": 2,
        "name": "郭立东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-04",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "沁源县人民政府",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/zzxz/202606/t20260618_3177919.html",
    },
    # ── Government Deputies ──
    {
        "id": 3,
        "name": "高淘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "山西省柳林县",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "沁源县人民政府",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/zzfxzgt/",
    },
    {
        "id": 4,
        "name": "赵飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "北京市顺义区",
        "education": "在职大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "沁源县人民政府",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/zzfxzzf/",
    },
    {
        "id": 5,
        "name": "张中武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "山西省长治市沁源县",
        "education": "本科学历",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沁源县人民政府",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/zzfxz02/",
    },
    {
        "id": 6,
        "name": "原恒伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "山西省长治市潞城区",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沁源县人民政府",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/zzfxz03/",
    },
    {
        "id": 7,
        "name": "刘晓慧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "山西省黎城县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沁源县人民政府",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/zzfxzlxh/",
    },
    {
        "id": 8,
        "name": "李洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-09",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "沁源县人民政府",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/zzfxz01/",
    },
    # ── 县政府办公室主任 ──
    {
        "id": 9,
        "name": "张晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-07",
        "birthplace": "山西省长治市沁源县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、县政府办公室主任",
        "current_org": "沁源县人民政府办公室",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/zfld/bgszr123/",
    },
    # ── Predecessor ──
    {
        "id": 10,
        "name": "郭晓方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县长（已辞职）",
        "current_org": "",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/gsgg/202606/t20260618_3177904.html",
    },
    {
        "id": 11,
        "name": "魏小祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原副县长（已免职）",
        "current_org": "",
        "source": "https://www.qinyuan.gov.cn/qyxxgk/zfxxgk/zfxxgkml/gsgg/202606/t20260618_3177902.html",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共沁源县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市沁源县",
    },
    {
        "id": 2,
        "name": "沁源县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市沁源县",
    },
    {
        "id": 3,
        "name": "沁源县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "沁源县人民政府",
        "location": "山西省长治市沁源县",
    },
    {
        "id": 4,
        "name": "沁源县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "沁源县",
        "location": "山西省长治市沁源县",
    },
    {
        "id": 5,
        "name": "中共长治市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "山西省",
        "location": "山西省长治市",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────────
positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "沁源县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed on official news articles as 市委常委、县委书记"},
    {"person_id": 1, "org_id": 5, "title": "长治市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "concurrently serves as Changzhi city party standing committee member"},
    # Mayor
    {"person_id": 2, "org_id": 2, "title": "沁源县县长", "start_date": "2026-06-18", "end_date": "present", "rank": "正处级", "note": "appointed acting mayor on 2026-06-18; official profile as of 2026-07-25"},
    {"person_id": 2, "org_id": 1, "title": "沁源县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed on official profile"},
    # Deputies
    {"person_id": 3, "org_id": 2, "title": "沁源县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-07-26"},
    {"person_id": 4, "org_id": 2, "title": "沁源县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-07-26; Beijing Shunyi native"},
    {"person_id": 5, "org_id": 2, "title": "沁源县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile; 沁源 native, 无党派"},
    {"person_id": 6, "org_id": 2, "title": "沁源县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-07-26"},
    {"person_id": 7, "org_id": 2, "title": "沁源县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile as of 2026-07-26; female"},
    {"person_id": 8, "org_id": 2, "title": "沁源县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official profile; 挂职"},
    {"person_id": 9, "org_id": 3, "title": "沁源县人民政府办公室主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": "official profile as of 2026-07-26"},
    # Predecessor positions
    {"person_id": 10, "org_id": 2, "title": "沁源县县长（原）", "start_date": "", "end_date": "2026-06-18", "rank": "正处级", "note": "resigned 2026-06-18 per 县人大常委会"},
    {"person_id": 11, "org_id": 2, "title": "沁源县副县长（原）", "start_date": "", "end_date": "2026-06-18", "rank": "副处级", "note": "removed 2026-06-18 per 县人大常委会"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────
relationships = [
    # 崔峥岭 <-> 郭立东: party secretary and mayor
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档", "overlap_org": "沁源县委县政府", "overlap_period": "2026-06-至今"},
    # 崔峥岭 <-> 高淘: secretary and executive deputy
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—常务副县长班子", "overlap_org": "沁源县委", "overlap_period": ""},
    # 郭立东 <-> 高淘: mayor and executive deputy
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—常务副县长工作搭档", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06-至今"},
    # 赵飞 <-> 崔峥岭: both county party committee members
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委常委班子", "overlap_org": "沁源县委", "overlap_period": ""},
    # Predecessor-successor relationship for mayor
    {"person_a": 10, "person_b": 2, "type": "predecessor_successor", "context": "郭晓方辞职，郭立东接任县长", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06"},
    # All deputies overlap at 沁源县人民政府
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长—副县长（赵飞）", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06-至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长—副县长（张中武）", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06-至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长—副县长（原恒伟）", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06-至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长—副县长（刘晓慧）", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06-至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长—挂职副县长（李洋）", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06-至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长—政府办主任（张晓东）", "overlap_org": "沁源县人民政府", "overlap_period": "2026-06-至今"},
    # Same native place connections
    {"person_a": 5, "person_b": 9, "type": "same_native_place", "context": "张中武与张晓东均为沁源县人", "overlap_org": "", "overlap_period": ""},
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
    print(f"✅ 沁源县 network built: {DB_PATH}, {GEXF_PATH}")