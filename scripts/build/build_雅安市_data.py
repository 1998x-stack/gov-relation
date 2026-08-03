#!/usr/bin/env python3
"""Build script for 雅安市 (Ya'an City), Sichuan Province.

Generated: 2026-08-03
Task ID: sichuan_雅安市
Targets: 市委书记 & 市长
Data sources:
- Ya'an government website (www.yaan.gov.cn) — leadership roster as of 2026-08
- Wikipedia (zh.wikipedia.org/wiki/雅安市) — current leaders, predecessors
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ── Slug ──────────────────────────────────────────────────────────────
SLUG = "雅安市"

# ── Integer IDs (required by gov_relation.schema) ──────────────────────
_PID = 0
def _pid():
    global _PID
    _PID += 1
    return _PID

# Person IDs
P_LIAO_WENBIN    = _pid()  # 1
P_PENG_YINGMEI   = _pid()  # 2
P_BAI_YUN        = _pid()  # 3
P_ZHANG_TONGRONG = _pid()  # 4
P_LI_MING        = _pid()  # 5
P_ZHANG_DAQI     = _pid()  # 6
P_LI_RONG        = _pid()  # 7
P_YANG_QINGLI    = _pid()  # 8
P_HE_LIANJUN     = _pid()  # 9
P_CHEN_WANJIAN   = _pid()  # 10
P_GONG_BING      = _pid()  # 11
P_XIONG_QIRAN    = _pid()  # 12
P_DAI_SIGUO      = _pid()  # 13
P_YU_JICHUAN     = _pid()  # 14
P_DENG_ZHAOJIN   = _pid()  # 15
P_ZHENG_HUYONG   = _pid()  # 16
P_SUN_YUNYI      = _pid()  # 17
P_ZENG_QI        = _pid()  # 18
P_HUANG_ZHIYAN   = _pid()  # 19
P_YU_YUNFENG     = _pid()  # 20
P_LIU_JIANFEI    = _pid()  # 21
P_XIA_FENGJIAN   = _pid()  # 22
P_LI_ZHUO        = _pid()  # 23
P_LAN_KAICHI     = _pid()  # 24
P_ZOU_JIN        = _pid()  # 25

# Org IDs
O_PARTY = 1
O_GOV   = 2
O_NPC   = 3
O_PPCC  = 4
O_CDC   = 5

# ── Person list ────────────────────────────────────────────────────────

persons = [
    {"id": P_LIAO_WENBIN,  "name": "廖文彬", "gender": "男", "ethnicity": "汉族", "birth": "1974年7月", "birthplace": "四川省井研县", "party_join": "中共党员", "current_post": "雅安市委书记", "current_org": "中共雅安市委员会", "source": "https://zh.wikipedia.org/wiki/雅安市"},
    {"id": P_PENG_YINGMEI, "name": "彭映梅", "gender": "女", "ethnicity": "汉族", "birth": "1979年1月", "birthplace": "江西省南昌市", "party_join": "中共党员", "current_post": "雅安市市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn/leader/detail/c112762d-cf15-4304-b13d-16e24aa84d80.html"},
    {"id": P_LI_MING,      "name": "黎明",   "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委副书记", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_BAI_YUN,       "name": "白云",   "gender": "男", "ethnicity": "彝族", "birth": "1969年2月", "birthplace": "四川省雷波县", "party_join": "中共党员", "current_post": "雅安市人大常委会主任", "current_org": "雅安市人民代表大会常务委员会", "source": "https://zh.wikipedia.org/wiki/雅安市"},
    {"id": P_ZHANG_TONGRONG,"name": "张通荣", "gender": "男", "ethnicity": "藏族", "birth": "1970年12月", "birthplace": "四川省金川县", "party_join": "中共党员", "current_post": "雅安市政协主席", "current_org": "中国人民政治协商会议雅安市委员会", "source": "https://zh.wikipedia.org/wiki/雅安市"},
    {"id": P_ZHANG_DAQI,    "name": "张大奇", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委常委", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_LI_RONG,       "name": "李蓉",   "gender": "女", "ethnicity": "汉族", "current_post": "雅安市委常委", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_YANG_QINGLI,   "name": "杨庆利", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委常委", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_HE_LIANJUN,    "name": "何连俊", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委常委", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_CHEN_WANJIAN,  "name": "陈万见", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委常委、副市长", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_GONG_BING,     "name": "龚兵",   "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委常委", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_XIONG_QIRAN,   "name": "熊启然", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委常委", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_DAI_SIGUO,     "name": "戴思国", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市委常委", "current_org": "中共雅安市委员会", "source": "https://www.yaan.gov.cn"},
    {"id": P_YU_JICHUAN,    "name": "于冀川", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_DENG_ZHAOJIN,  "name": "邓朝金", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_ZHENG_HUYONG,  "name": "郑胡勇", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_SUN_YUNYI,     "name": "孙云一", "gender": "女", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_ZENG_QI,       "name": "曾琦",   "gender": "女", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_HUANG_ZHIYAN,  "name": "黄芝晏", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_YU_YUNFENG,    "name": "余云峰", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_LIU_JIANFEI,   "name": "刘剑飞", "gender": "男", "ethnicity": "汉族", "current_post": "雅安市副市长", "current_org": "雅安市人民政府", "source": "https://www.yaan.gov.cn"},
    {"id": P_XIA_FENGJIAN,  "name": "夏凤俭", "gender": "男", "ethnicity": "汉族", "current_post": "", "current_org": "", "source": "https://zh.wikipedia.org/wiki/雅安市"},
    {"id": P_LI_ZHUO,       "name": "李酌",   "gender": "男", "ethnicity": "汉族", "current_post": "", "current_org": "", "source": "https://zh.wikipedia.org/wiki/雅安市"},
    {"id": P_LAN_KAICHI,    "name": "兰开驰", "gender": "男", "ethnicity": "汉族", "current_post": "", "current_org": "", "source": "https://zh.wikipedia.org/wiki/雅安市"},
    {"id": P_ZOU_JIN,       "name": "邹瑾",   "gender": "男", "ethnicity": "汉族", "current_post": "", "current_org": "", "source": "https://zh.wikipedia.org/wiki/雅安市"},
]

organizations = [
    {"id": O_PARTY, "name": "中共雅安市委员会", "type": "党委", "level": "地级", "parent": "中共四川省委", "location": "四川省雅安市"},
    {"id": O_GOV,   "name": "雅安市人民政府",   "type": "政府", "level": "地级", "parent": "四川省人民政府", "location": "四川省雅安市"},
    {"id": O_NPC,   "name": "雅安市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "四川省人大常委会", "location": "四川省雅安市"},
    {"id": O_PPCC,  "name": "中国人民政治协商会议雅安市委员会", "type": "政协", "level": "地级", "parent": "四川省政协", "location": "四川省雅安市"},
    {"id": O_CDC,   "name": "中共雅安市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共雅安市委员会", "location": "四川省雅安市"},
]

positions = [
    {"person_id": P_LIAO_WENBIN,  "org_id": O_PARTY, "title": "市委书记", "start_date": "2025-07", "end_date": "present", "rank": "正厅级", "note": "2025年7月任命"},
    {"person_id": P_PENG_YINGMEI, "org_id": O_GOV,   "title": "市长",     "start_date": "2021-05", "end_date": "present", "rank": "正厅级", "note": "之前任攀枝花市委副书记"},
    {"person_id": P_PENG_YINGMEI, "org_id": O_PARTY, "title": "市委副书记", "start_date": "2021-05", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_BAI_YUN,      "org_id": O_NPC,   "title": "市人大常委会主任", "start_date": "2021-03", "end_date": "present", "rank": "正厅级", "note": "彝族"},
    {"person_id": P_ZHANG_TONGRONG,"org_id": O_PPCC, "title": "市政协主席", "start_date": "2026-01", "end_date": "present", "rank": "正厅级", "note": "藏族"},
    {"person_id": P_LI_MING,      "org_id": O_PARTY, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_ZHANG_DAQI,   "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_LI_RONG,      "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_YANG_QINGLI,  "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_HE_LIANJUN,   "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_CHEN_WANJIAN, "org_id": O_GOV,   "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_GONG_BING,    "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_XIONG_QIRAN,  "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_DAI_SIGUO,    "org_id": O_PARTY, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_YU_JICHUAN,   "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_DENG_ZHAOJIN, "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_ZHENG_HUYONG, "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_SUN_YUNYI,    "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_ZENG_QI,      "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_HUANG_ZHIYAN, "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_YU_YUNFENG,   "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_LIU_JIANFEI,  "org_id": O_GOV,   "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": P_XIA_FENGJIAN, "org_id": O_PARTY, "title": "市委书记", "start_date": "2023-10", "end_date": "2025-07", "rank": "正厅级", "note": "接替李酌；后调离"},
    {"person_id": P_LI_ZHUO,      "org_id": O_PARTY, "title": "市委书记", "start_date": "2021-02", "end_date": "2023-10", "rank": "正厅级", "note": "接替兰开驰"},
    {"person_id": P_LAN_KAICHI,    "org_id": O_PARTY, "title": "市委书记", "start_date": "2017-11", "end_date": "2021-02", "rank": "正厅级", "note": "之前为雅安市市长"},
    {"person_id": P_LAN_KAICHI,    "org_id": O_GOV,   "title": "市长",     "start_date": "2014-02", "end_date": "2017-11", "rank": "正厅级", "note": "后升任市委书记"},
    {"person_id": P_ZOU_JIN,      "org_id": O_GOV,   "title": "市长",     "start_date": "2017-12", "end_date": "2021-05", "rank": "正厅级", "note": "接替兰开驰"},
]

relationships = [
    {"person_a": P_LIAO_WENBIN,  "person_b": P_XIA_FENGJIAN, "type": "predecessor_successor", "context": "廖文彬2025年7月接替夏凤俭", "overlap_org": "中共雅安市委员会", "overlap_period": "2025-07"},
    {"person_a": P_XIA_FENGJIAN, "person_b": P_LI_ZHUO,      "type": "predecessor_successor", "context": "夏凤俭2023年10月接替李酌", "overlap_org": "中共雅安市委员会", "overlap_period": "2023-10"},
    {"person_a": P_LI_ZHUO,      "person_b": P_LAN_KAICHI,    "type": "predecessor_successor", "context": "李酌2021年2月接替兰开驰", "overlap_org": "中共雅安市委员会", "overlap_period": "2021-02"},
    {"person_a": P_PENG_YINGMEI, "person_b": P_ZOU_JIN,      "type": "predecessor_successor", "context": "彭映梅2021年5月接替邹瑾", "overlap_org": "雅安市人民政府", "overlap_period": "2021-05"},
    {"person_a": P_LAN_KAICHI,    "person_b": P_ZOU_JIN,      "type": "predecessor_successor", "context": "兰开驰由市长升书记，邹瑾接任市长", "overlap_org": "雅安市人民政府", "overlap_period": "2017-12"},
    {"person_a": P_LIAO_WENBIN,  "person_b": P_PENG_YINGMEI, "type": "overlap", "context": "党政主要负责人", "overlap_org": "中共雅安市委员会", "overlap_period": "2025-07至今"},
    {"person_a": P_CHEN_WANJIAN, "person_b": P_DAI_SIGUO,    "type": "overlap", "context": "同为市委常委", "overlap_org": "中共雅安市委员会", "overlap_period": "至今"},
    {"person_a": P_DAI_SIGUO,    "person_b": P_PENG_YINGMEI, "type": "overlap", "context": "同为市政府领导班子", "overlap_org": "雅安市人民政府", "overlap_period": "至今"},
    {"person_a": P_CHEN_WANJIAN, "person_b": P_PENG_YINGMEI, "type": "overlap", "context": "同为市政府领导班子", "overlap_org": "雅安市人民政府", "overlap_period": "至今"},
]

# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    staging = REPO_ROOT / "data" / "tmp" / "sichuan_雅安市"
    db_path = staging / f"{SLUG}_network.db"
    gexf_path = staging / f"{SLUG}_network.gexf"

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
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\n✅ Database: {db_path}")
    print(f"✅ GEXF graph: {gexf_path}")
    assert db_path.exists()
    assert gexf_path.exists()
    print("✅ Complete.")