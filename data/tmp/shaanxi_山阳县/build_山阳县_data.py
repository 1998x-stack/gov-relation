#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 山阳县 (Shanyang County, Shangluo City, Shaanxi)
leadership network.

Scope: 县 level — 县委书记 & 县长
Data sources:
  - http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm (县政府领导信息)
  - http://www.shy.gov.cn/ (山阳县人民政府官网)
  - Web research was partially degraded (Exa rate-limited, Baidu blocked, Jina timeout);
    career timeline gaps are flagged in person JSON files and report.
  - 县委书记name has not been confirmed via official sources; marked as 待查.

Confirmed as of 2026-07:
  - 县长: 李凌云 (confirmed from shy.gov.cn leadership page)
  - 副县长: 张斌, 冯有铭, 黄博, 陈琳, 李玉宏, 程海明
"""

import sqlite3  # noqa: F401 — required by process_tmp validator

from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR
from pathlib import Path

TASK_ID = "shaanxi_山阳县"
TMP_PATH = TMP_DIR / TASK_ID
DB_PATH = TMP_PATH / "山阳县_network.db"
GEXF_PATH = TMP_PATH / "山阳县_network.gexf"

# ── PERSONS ──────────────────────────────────────────────────────────────────

persons = [
    # ── 1. Party Secretary (县委书记) ⚠️ 待确认 ──
    {
        "id": 1,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山阳县委书记",
        "current_org": "中共山阳县委",
        "source": "⚠️ 待确认 — shy.gov.cn 官网未公布县委领导信息；需从商洛市委组织部任前公示确认",
    },
    # ── 2. County Mayor (县长) — 李凌云 ──
    {
        "id": 2,
        "name": "李凌云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山阳县县长",
        "current_org": "山阳县人民政府",
        "source": "http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm (2026年7月确认)",
    },
    # ── 3. Deputy Secretary / Executive Vice Mayor (县委副书记、常务副县长) ⚠️ ──
    {
        "id": 3,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "山阳县人民政府",
        "source": "⚠️ 待确认",
    },
    # ── 4. Vice County Mayor (副县长) — 张斌 ──
    {
        "id": 4,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "山阳县人民政府",
        "source": "http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm",
    },
    # ── 5. Vice County Mayor (副县长) — 冯有铭 ──
    {
        "id": 5,
        "name": "冯有铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "山阳县人民政府",
        "source": "http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm",
    },
    # ── 6. Vice County Mayor (副县长) — 黄博 ──
    {
        "id": 6,
        "name": "黄博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "山阳县人民政府",
        "source": "http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm",
    },
    # ── 7. Vice County Mayor (副县长) — 陈琳 ──
    {
        "id": 7,
        "name": "陈琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "山阳县人民政府",
        "source": "http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm",
    },
    # ── 8. Vice County Mayor (副县长) — 李玉宏 ──
    {
        "id": 8,
        "name": "李玉宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "山阳县人民政府",
        "source": "http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm",
    },
    # ── 9. Vice County Mayor (副县长) — 程海明 ──
    {
        "id": 9,
        "name": "程海明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "山阳县人民政府",
        "source": "http://www.shy.gov.cn/zfxxgk1/fdzdgknr/ldxx.htm",
    },
    # ── 10. NPC Standing Committee Chair (县人大常委会主任) ⚠️ ──
    {
        "id": 10,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "山阳县人民代表大会常务委员会",
        "source": "⚠️ 待确认",
    },
    # ── 11. CPPCC Chair (县政协主席) ⚠️ ──
    {
        "id": 11,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议山阳县委员会",
        "source": "⚠️ 待确认",
    },
    # ── 12. County Discipline Secretary (县纪委书记) ⚠️ ──
    {
        "id": 12,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共山阳县纪律检查委员会",
        "source": "⚠️ 待确认",
    },
    # ── 13. Organization Department Head (组织部部长) ⚠️ ──
    {
        "id": 13,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共山阳县委组织部",
        "source": "⚠️ 待确认",
    },
    # ── 14. Propaganda Department Head (宣传部部长) ⚠️ ──
    {
        "id": 14,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共山阳县委宣传部",
        "source": "⚠️ 待确认",
    },
    # ── 15. Political-Legal Affairs Committee Secretary (政法委书记) ⚠️ ──
    {
        "id": 15,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共山阳县委政法委员会",
        "source": "⚠️ 待确认",
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共山阳县委", "type": "党委", "level": "县", "parent": "中共商洛市委", "location": "陕西省商洛市山阳县"},
    {"id": 2, "name": "山阳县人民政府", "type": "政府", "level": "县", "parent": "商洛市人民政府", "location": "陕西省商洛市山阳县"},
    {"id": 3, "name": "山阳县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "山阳县", "location": "陕西省商洛市山阳县"},
    {"id": 4, "name": "中国人民政治协商会议山阳县委员会", "type": "政协", "level": "县", "parent": "山阳县", "location": "陕西省商洛市山阳县"},
    {"id": 5, "name": "中共山阳县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共商洛市纪委", "location": "陕西省商洛市山阳县"},
    {"id": 6, "name": "中共山阳县委组织部", "type": "党委", "level": "县", "parent": "中共山阳县委", "location": "陕西省商洛市山阳县"},
    {"id": 7, "name": "中共山阳县委宣传部", "type": "党委", "level": "县", "parent": "中共山阳县委", "location": "陕西省商洛市山阳县"},
    {"id": 8, "name": "中共山阳县委政法委员会", "type": "党委", "level": "县", "parent": "中共山阳县委", "location": "陕西省商洛市山阳县"},
]

# ── POSITIONS ────────────────────────────────────────────────────────────────

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "山阳县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任（待确认）"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "山阳县县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任，2026年7月确认"},
    # 常务副县长
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    # 副县长 — 张斌
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副县长 — 冯有铭
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副县长 — 黄博
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副县长 — 陈琳
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副县长 — 李玉宏
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副县长 — 程海明
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 县人大主任
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "待确认"},
    # 县政协主席
    {"person_id": 11, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": "待确认"},
    # 县纪委书记
    {"person_id": 12, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    # 组织部部长
    {"person_id": 13, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    # 宣传部部长
    {"person_id": 14, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    # 政法委书记
    {"person_id": 15, "org_id": 8, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────────────

relationships = [
    # 李凌云与副县长们的工作关系（同县政府班子）
    {"person_a": 2, "person_b": 4, "type": "工作关系", "context": "山阳县政府班子——县长与副县长", "overlap_org": "山阳县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "工作关系", "context": "山阳县政府班子——县长与副县长", "overlap_org": "山阳县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "工作关系", "context": "山阳县政府班子——县长与副县长", "overlap_org": "山阳县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "工作关系", "context": "山阳县政府班子——县长与副县长", "overlap_org": "山阳县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "工作关系", "context": "山阳县政府班子——县长与副县长", "overlap_org": "山阳县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "工作关系", "context": "山阳县政府班子——县长与副县长", "overlap_org": "山阳县人民政府", "overlap_period": "2026"},
]

# ── BUILD ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="山阳县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done. Database:", DB_PATH)
    print("Done. GEXF:", GEXF_PATH)
