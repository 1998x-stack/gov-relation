#!/usr/bin/env python3
"""Build script for 洛阳市 (Luoyang City), Henan Province.

Generated: 2026-08-05
Task ID: henan_洛阳市
Targets: 市委书记 & 市长
Data sources:
- Official Luoyang gov website (www.ly.gov.cn) — leadership roster, content search API, 2025-2026
- 洛阳网 www.lyd.com.cn
Confidence: current roster = confirmed (official); career-bio deep fields = plausible/unverified
(open questions encoded in person JSON).
"""

import sys
import sqlite3  # noqa: F401  (used by gov_relation.schema; kept for process_tmp validation)
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ── Slug ──────────────────────────────────────────────────────────────
SLUG = "洛阳市"

# ── Integer IDs (required by gov_relation.schema) ──────────────────────
_PID = 0
def _pid():
    global _PID
    _PID += 1
    return _PID

# Person IDs
P_CHEN_CHUNJIANG    = _pid()  # 1  市委书记
P_ZHANG_YUJIE       = _pid()  # 2  市长
P_LI_BAOGUO         = _pid()  # 3  市人大主任
P_SUN_YANWEN        = _pid()  # 4  市政协主席
P_WANG_SEN          = _pid()  # 5  市委副书记、政法委
P_PAN_KAIMING       = _pid()  # 6  常务副市长
P_REN_LIJUN         = _pid()  # 7  副市长
P_LI_XINHONG        = _pid()  # 8  副市长
P_WANG_TAIGANG      = _pid()  # 9  副市长
P_CHU_GUOJIAN      = _pid()  # 10 副市长、公安局长
P_LI_GANG           = _pid()  # 11 副市长
P_YUAN_JIAN         = _pid()  # 12 市政府秘书长
P_WANG_LI           = _pid()  # 13 市委常委
P_JIANG_LING        = _pid()  # 14 前任市委书记
P_LI_YA             = _pid()  # 15 更早前任书记
P_XU_YIYAN          = _pid()  # 16 前任市长
P_LIU_WAN_KANG      = _pid()  # 17 前任市长
P_YANG_XIAO         = _pid()  # 18 前任市委副书记

# Org IDs
O_PARTY = 1
O_GOV   = 2
O_NPC   = 3
O_PPCC  = 4
O_CDC   = 5
O_PFZF  = 6
O_GA    = 7

# ── Person list ────────────────────────────────────────────────────────
persons = [
    {"id": P_CHEN_CHUNJIANG,  "name": "陈春江", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "省委常委、洛阳市委书记", "current_org": "中共洛阳市委员会",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_ZHANG_YUJIE,     "name": "张玉杰", "gender": "男", "ethnicity": "满族", "birth": "1975年2月", "birthplace": "",
     "party_join": "中共党员", "current_post": "市委副书记、市长", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/zyjg/"},
    {"id": P_LI_BAOGUO,    "name": "李保国", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "市人大常委会主任", "current_org": "洛阳市人民代表大会常务委员会",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_SUN_YANWEN,      "name": "孙延文", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "市政协主席", "current_org": "中国人民政治协商会议洛阳市委员会",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_WANG_SEN,        "name": "王森",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "市委副书记、政法委书记", "current_org": "中共洛阳市委员会",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_PAN_KAIMING,     "name": "潘开名", "gender": "男", "ethnicity": "汉族", "birth": "1973年8月", "birthplace": "",
     "party_join": "中共党员", "current_post": "市委常委、常务副市长", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/pkm/"},
    {"id": P_REN_LIJUN,       "name": "任丽君", "gender": "女", "ethnicity": "汉族", "birth": "1967年4月", "birthplace": "",
     "party_join": "民进成员", "current_post": "副市长", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/rlj/"},
    {"id": P_LI_XINHONG,      "name": "李新红", "gender": "男", "ethnicity": "汉族", "birth": "1967年2月", "birthplace": "",
     "party_join": "中共党员", "current_post": "副市长", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/lxh/"},
    {"id": P_WANG_TAIGANG,    "name": "王太钢", "gender": "男", "ethnicity": "汉族", "birth": "1981年6月", "birthplace": "",
     "party_join": "中共党员", "current_post": "副市长（兼市国资委党委书记）", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/wtg/"},
    {"id": P_CHU_GUOJIAN,       "name": "楚国剑", "gender": "男", "ethnicity": "汉族", "birth": "1969年6月", "birthplace": "",
     "party_join": "中共党员", "current_post": "副市长、市公安局局长", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/cgj/"},
    {"id": P_LI_GANG,         "name": "李刚",   "gender": "男", "ethnicity": "汉族", "birth": "1974年4月", "birthplace": "",
     "party_join": "中共党员", "current_post": "副市长", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/lg/"},
    {"id": P_YUAN_JIAN,       "name": "袁剑",   "gender": "男", "ethnicity": "汉族", "birth": "1971年4月", "birthplace": "",
     "party_join": "中共党员", "current_post": "市政府秘书长", "current_org": "洛阳市人民政府",
     "source": "https://www.ly.gov.cn/zwgk/zfld/yj/"},
    {"id": P_WANG_LI,         "name": "王丽",   "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "市委常委", "current_org": "中共洛阳市委员会",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_JIANG_LING,      "name": "江凌",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "", "current_org": "",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_LI_YA,           "name": "李亚",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "", "current_org": "",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_XU_YIYAN,        "name": "徐衣显", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "", "current_org": "",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_LIU_WAN_KANG,     "name": "刘宛康", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "", "current_org": "",
     "source": "https://www.ly.gov.cn/ "},
    {"id": P_YANG_XIAO,      "name": "杨骁",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "party_join": "中共党员", "current_post": "", "current_org": "",
     "source": "https://www.ly.gov.cn/ "},
]

organizations = [
    {"id": O_PARTY, "name": "中共洛阳市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委", "location": "河南省洛阳市"},
    {"id": O_GOV,   "name": "洛阳市人民政府",   "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省洛阳市"},
    {"id": O_NPC,   "name": "洛阳市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "河南省人大常委会", "location": "河南省洛阳市"},
    {"id": O_PPCC,  "name": "中国人民政治协商会议洛阳市委员会", "type": "政协", "level": "地级", "parent": "河南省政协", "location": "河南省洛阳市"},
    {"id": O_CDC,   "name": "中共洛阳市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共洛阳市委员会", "location": "河南省洛阳市"},
    {"id": O_PFZF,  "name": "中共洛阳市委政法委员会", "type": "党委", "level": "地级", "parent": "中共洛阳市委员会", "location": "河南省洛阳市"},
    {"id": O_GA,    "name": "洛阳市公安局",     "type": "政协", "level": "地级", "parent": "洛阳市人民政府", "location": "河南省洛阳市"},
]

positions = [
    # — 市委书记沿革 —
    {"person_id": P_CHEN_CHUNJIANG, "org_id": O_PARTY, "title": "市委书记", "start_date": "2025-10-19", "end_date": "present", "rank": "省委常委、正厅级", "note": "2025-10-19洛阳市领导干部会议宣布，前任江凌不再担任"},
    {"person_id": P_JIANG_LING,   "org_id": O_PARTY, "title": "市委书记", "start_date": "2021",          "end_date": "2025-10",     "rank": "正厅级", "note": "2025-01当选河南省人大常委会副主任，仍兼书记至2025-10"},
    {"person_id": P_LI_YA,        "org_id": O_PARTY, "title": "市委书记", "start_date": "2016",          "end_date": "2021",        "rank": "正厅级", "note": "前任书记"},
    # — 市长沿革 —
    {"person_id": P_ZHANG_YUJIE,  "org_id": O_GOV,   "title": "市长",     "start_date": "2025-01",       "end_date": "present",     "rank": "正厅级", "note": "原常务副市长，接徐衣显任市长"},
    {"person_id": P_ZHANG_YUJIE,  "org_id": O_PARTY, "title": "市委副书记", "start_date": "2025-01",     "end_date": "present",     "rank": "副厅级", "note": ""},
    {"person_id": P_XU_YIYAN,     "org_id": O_GOV,   "title": "市长",     "start_date": "2021",          "end_date": "2025-01",     "rank": "正厅级", "note": "末篇官方以市长身份报道约2025-01-02，去向待核"},
    {"person_id": P_LIU_WAN_KANG,  "org_id": O_GOV,   "title": "市长",     "start_date": "2018",          "end_date": "2021",        "rank": "正厅级", "note": "前任市长"},
    # — 现任领导班子 —
    {"person_id": P_LI_BAOGUO, "org_id": O_NPC,   "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": P_SUN_YANWEN,   "org_id": O_PPCC,  "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": P_WANG_SEN,     "org_id": O_PARTY, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_WANG_SEN,     "org_id": O_PFZF,  "title": "市委政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_PAN_KAIMING,  "org_id": O_GOV,   "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市委常委、市政府党组副书记"},
    {"person_id": P_PAN_KAIMING,  "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_REN_LIJUN,    "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "民进成员"},
    {"person_id": P_LI_XINHONG,   "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_WANG_TAIGANG, "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼市国资委党委书记"},
    {"person_id": P_CHU_GUOJIAN,    "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_CHU_GUOJIAN,    "org_id": O_GA,    "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_LI_GANG,      "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_YUAN_JIAN,    "org_id": O_GOV,   "title": "市政府秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": P_WANG_LI,      "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "具体职务待核"},
    {"person_id": P_YANG_XIAO,    "org_id": O_PARTY, "title": "市委副书记", "start_date": "", "end_date": "2024",  "rank": "副厅级", "note": "前任副书记"},
]

relationships = [
    # 书记 - 市长 (党政主要负责人)
    {"person_a": P_CHEN_CHUNJIANG, "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "党政主要负责人（市委书记×市长）搭档", "overlap_org": "中共洛阳市委员会", "overlap_period": "2025-10至今"},
    # 书记前继
    {"person_a": P_CHEN_CHUNJIANG, "person_b": P_JIANG_LING,  "type": "predecessor_successor", "context": "陈春江2025-10-19接替江凌任市委书记", "overlap_org": "中共洛阳市委员会", "overlap_period": "2025-10"},
    {"person_a": P_JIANG_LING,     "person_b": P_LI_YA,       "type": "predecessor_successor", "context": "江凌约2021接替李亚任市委书记", "overlap_org": "中共洛阳市委员会", "overlap_period": "2021"},
    # 市长前继
    {"person_a": P_ZHANG_YUJIE,    "person_b": P_XU_YIYAN,    "type": "predecessor_successor", "context": "张玉杰约2025年初接替徐衣显任市长", "overlap_org": "洛阳市人民政府", "overlap_period": "2025"},
    {"person_a": P_XU_YIYAN,       "person_b": P_LIU_WAN_KANG, "type": "predecessor_successor", "context": "徐衣显约2021接替刘宛康任市长", "overlap_org": "洛阳市人民政府", "overlap_period": "2021"},
    # 常委会共事
    {"person_a": P_WANG_SEN,       "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "市委副书记（王森政法委×张玉杰市长）", "overlap_org": "中共洛阳市委员会", "overlap_period": "至今"},
    {"person_a": P_PAN_KAIMING,    "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "市政府领导班子（常务×市长）", "overlap_org": "洛阳市人民政府", "overlap_period": "至今"},
    {"person_a": P_REN_LIJUN,      "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "市政府领导班子", "overlap_org": "洛阳市人民政府", "overlap_period": "至今"},
    {"person_a": P_LI_XINHONG,     "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "市政府领导班子", "overlap_org": "洛阳市人民政府", "overlap_period": "至今"},
    {"person_a": P_WANG_TAIGANG,   "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "市政府领导班子", "overlap_org": "洛阳市人民政府", "overlap_period": "至今"},
    {"person_a": P_CHU_GUOJIAN,      "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "市政府领导班子", "overlap_org": "洛阳市人民政府", "overlap_period": "至今"},
    {"person_a": P_LI_GANG,        "person_b": P_ZHANG_YUJIE, "type": "overlap", "context": "市政府领导班子", "overlap_org": "洛阳市人民政府", "overlap_period": "至今"},
]

# ── Main ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    staging = REPO_ROOT / "data" / "tmp" / "henan_洛阳市"
    DB_PATH = staging / f"{SLUG}_network.db"
    GEXF_PATH = staging / f"{SLUG}_network.gexf"

    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    print(f"\n✅ Database: {DB_PATH}")
    print(f"✅ GEXF graph: {GEXF_PATH}")
    assert DB_PATH.exists()
    assert GEXF_PATH.exists()
    print("✅ Complete.")