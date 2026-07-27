#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 洛南县 (Luonan County, Shaanxi)
leadership network.

Scope: 县 level — 县委书记 & 县长
Data source: Luonan County government official website (luonan.gov.cn)
Web research was partially degraded (Exa rate-limited, Baidu blocked);
career timeline gaps are flagged in person JSON files.
"""

from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR
from pathlib import Path

TASK_ID = "shaanxi_洛南县"
TMP_PATH = TMP_DIR / TASK_ID
DB_PATH = TMP_PATH / "洛南县_network.db"
GEXF_PATH = TMP_PATH / "洛南县_network.gexf"

# ── PERSONS ──────────────────────────────────────────────────────────────────

persons = [
    # ── 1. Party Secretary (县委书记) ──
    {
        "id": 1,
        "name": "杨长江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委书记",
        "current_org": "中共洛南县委",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 2. County Mayor (县长) ──
    {
        "id": 2,
        "name": "方德军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县长",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 3. Deputy Secretary (县委副书记) ──
    {
        "id": 3,
        "name": "彭书旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委副书记",
        "current_org": "中共洛南县委",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 4. Deputy Secretary (县委副书记) ──
    {
        "id": 4,
        "name": "胡大志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委副书记",
        "current_org": "中共洛南县委",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 5. Standing Committee / Propaganda (县委常委) ──
    {
        "id": 5,
        "name": "刘雪锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委常委",
        "current_org": "中共洛南县委",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 6. Standing Committee / Discipline (县委常委、纪委书记) ──
    {
        "id": 6,
        "name": "李福军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委常委、纪委书记",
        "current_org": "中共洛南县纪律检查委员会",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 7. Standing Committee / Organization (县委常委、组织部) ──
    {
        "id": 7,
        "name": "林萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委常委、组织部部长",
        "current_org": "中共洛南县委组织部",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 8. Standing Committee (县委常委) ──
    {
        "id": 8,
        "name": "杨新良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委常委",
        "current_org": "中共洛南县委",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 9. Standing Committee / Deputy Mayor (县委常委、副县长) ──
    {
        "id": 9,
        "name": "郑光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委常委、副县长",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 10. Standing Committee / Deputy Mayor (县委常委、副县长) ──
    {
        "id": 10,
        "name": "陈利剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县委常委、副县长",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 11. County Party Spokesperson / County Gov (县政府党组成员、三级调研员) ──
    {
        "id": 11,
        "name": "景建民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县政府党组成员、三级调研员",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 12. Deputy Mayor (副县长、公安局长) ──
    {
        "id": 12,
        "name": "秦立争",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县副县长、公安局长",
        "current_org": "洛南县公安局",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 13. Deputy Mayor (副县长) ──
    {
        "id": 13,
        "name": "张翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县副县长",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 14. Deputy Mayor (副县长) ──
    {
        "id": 14,
        "name": "张玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县副县长",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 15. Deputy Mayor (副县长) ──
    {
        "id": 15,
        "name": "宋少辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县副县长",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 16. Deputy Mayor (副县长) ──
    {
        "id": 16,
        "name": "王金良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县副县长",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 17. Researcher (调研员) ──
    {
        "id": 17,
        "name": "何云兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛南县政府调研员",
        "current_org": "洛南县人民政府",
        "source": "https://www.luonan.gov.cn/zfxxgk/fdzdgk1/ldxx.htm",
    },
    # ── 18. County People's Congress (人大常委会主任 — 空缺?未列明) ──
    # Skipping as the position seems vacant / not listed separately
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共洛南县委", "type": "党委", "level": "县", "parent": "中共商洛市委", "location": "陕西省商洛市洛南县"},
    {"id": 2, "name": "洛南县人民政府", "type": "政府", "level": "县", "parent": "商洛市人民政府", "location": "陕西省商洛市洛南县"},
    {"id": 3, "name": "中共洛南县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共洛南县委", "location": "陕西省商洛市洛南县"},
    {"id": 4, "name": "中共洛南县委组织部", "type": "党委", "level": "县", "parent": "中共洛南县委", "location": "陕西省商洛市洛南县"},
    {"id": 5, "name": "洛南县公安局", "type": "政府", "level": "县", "parent": "洛南县人民政府", "location": "陕西省商洛市洛南县"},
]

# ── POSITIONS ────────────────────────────────────────────────────────────────

positions = [
    # 杨长江 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "洛南县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任，confirmed as of 2026-07"},
    # 方德军 — 县长
    {"person_id": 2, "org_id": 2, "title": "洛南县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任，confirmed as of 2026-07"},
    # 方德军 — 县委副书记（兼职）
    {"person_id": 2, "org_id": 1, "title": "洛南县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "县委副书记兼县长"},
    # 彭书旺 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "洛南县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 胡大志 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "洛南县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘雪锋 — 县委常委
    {"person_id": 5, "org_id": 1, "title": "洛南县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李福军 — 县委常委、纪委书记
    {"person_id": 6, "org_id": 1, "title": "洛南县委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "洛南县纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 林萍 — 县委常委、组织部部长
    {"person_id": 7, "org_id": 1, "title": "洛南县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "洛南县委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨新良 — 县委常委
    {"person_id": 8, "org_id": 1, "title": "洛南县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 郑光 — 县委常委、副县长
    {"person_id": 9, "org_id": 1, "title": "洛南县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "洛南县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈利剑 — 县委常委、副县长
    {"person_id": 10, "org_id": 1, "title": "洛南县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "洛南县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 景建民 — 县政府党组成员、三级调研员
    {"person_id": 11, "org_id": 2, "title": "洛南县政府党组成员、三级调研员", "start_date": "", "end_date": "", "rank": "三级调研员", "note": ""},
    # 秦立争 — 副县长（公安局长）
    {"person_id": 12, "org_id": 2, "title": "洛南县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "洛南县公安局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张翔 — 副县长
    {"person_id": 13, "org_id": 2, "title": "洛南县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张玉 — 副县长
    {"person_id": 14, "org_id": 2, "title": "洛南县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 宋少辉 — 副县长
    {"person_id": 15, "org_id": 2, "title": "洛南县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王金良 — 副县长
    {"person_id": 16, "org_id": 2, "title": "洛南县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 何云兰 — 调研员
    {"person_id": 17, "org_id": 2, "title": "洛南县政府调研员", "start_date": "", "end_date": "", "rank": "调研员", "note": ""},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────────────

relationships = [
    # 杨长江 ↔ 方德军（书记与县长）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "杨长江为县委书记，方德军为县长兼县委副书记，党政一把手配合", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    # 杨长江 ↔ 彭书旺（书记与副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委正副书记", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    # 杨长江 ↔ 胡大志（书记与副书记）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委正副书记", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    # 方德军 ↔ 彭书旺（同为副书记）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "方德军为副书记兼县长，彭书旺为专职副书记", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    # 方德军 ↔ 胡大志（同为副书记）
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "方德军为副书记兼县长，胡大志为专职副书记", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    # 彭书旺 ↔ 胡大志（同为副书记）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为县委专职副书记", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    # 杨长江 ↔ 各常委（县委常委班子）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委常委会领导班子", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委常委会领导班子", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委常委会领导班子", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委常委会领导班子", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委常委会领导班子", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委常委会领导班子", "overlap_org": "中共洛南县委", "overlap_period": "当前"},
    # 方德军 ↔ 副县长们（县政府班子）
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与党组成员", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长（公安局长）", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "洛南县人民政府", "overlap_period": "当前"},
]

# ── BUILD ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="洛南县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {TMP_PATH / 'persons/'}")
