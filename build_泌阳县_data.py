#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 泌阳县 (Biyang County), 驻马店市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_泌阳县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.biyang.gov.cn/ — official government website
  - 县委书记李勇带队深入开发区现场办公: /zwyw/tpxw/202607/t20260721_713250.html (2026-07-16)
  - 县政府领导信息页面: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/ (7 leaders with official bios)
  - 陈广平 (县长) bio: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319925.html
  - 狄艳松 (常务副县长) bio: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202512/t20251226_679992.html
  - 吴娟 (宣传部长/副县长) bio: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319924.html
  - 刘涛 (副县长) bio: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319923.html
  - 闫明 (副县长/公安局长) bio: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319922.html
  - 邱士用 (副县长/财政局长) bio: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319920.html
  - 崔兰阁 (副县长) bio: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319919.html
  - 春节走访慰问活动 (朱东升任县委书记时): /zwyw/tpxw/202602/t20260211_688924.html (2026-02-07)
  - 泌阳县委理论学习中心组: /zwyw/tpxw/202508/t20250825_649080.html

Confidence notes:
  - 李勇 (县委书记): confirmed via July 2026 official articles. Previous role and full bio unverified.
  - 朱东升 (前任县委书记): confirmed as 县委书记 in Feb 2026 article. Transitioned between Feb-July 2026. Whereabouts unknown.
  - 陈广平 (县长): confirmed via official bio (1980.12, 河南正阳人, 2002.11参加工作, 大学本科).
  - 狄艳松 (常委、副县长): confirmed via official bio (1986.01, 河北河间人, 中国地质大学在职研究生).
  - 吴娟 (常委、宣传部长、副县长): confirmed via official bio (1982.03, 河南驿城区人, 大学本科).
  - 刘涛 (副县长): confirmed via official bio (1982.07, 河南平舆人, 郑州大学在职研究生).
  - 闫明 (副县长/公安局长): confirmed via official bio (1979.04, 河南驻马店人, 研究生).
  - 邱士用 (副县长/财政局长): confirmed via official bio (1972.12, 河南泌阳人, 大学本科).
  - 崔兰阁 (副县长): confirmed via official bio (1986.05, 河南民权人, 2010.07参加工作, 大学本科).
  - 朱瑞霞 (县委副书记): confirmed via Feb 2026 article.
  - 张万兵 (县人大常委会主任): confirmed via Feb 2026 article.
  - 安生 (县政协主席): confirmed via Feb 2026 article.
  - 李勇's full bio (birth year, birthplace, education) and prior career are unverified.
  - 朱东升's current whereabouts and full bio are unverified.
  - Party standing committee detailed role assignments (组织部长, 纪委书记, 政法委书记, 统战部长, 县委办公室主任) are unknown.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "泌阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "李勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共泌阳县委员会",
        "source": "Confirmed via 泌阳政府网 (2026-07-16): 县委书记李勇带队深入县先进制造业开发区开展现场办公. Transitioned between Feb-July 2026 (predecessor 朱东升 in Feb 2026)."
    },
    {
        "id": 2,
        "name": "陈广平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980.12",
        "birthplace": "河南正阳",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2002.11",
        "current_post": "县委副书记、县长",
        "current_org": "泌阳县人民政府",
        "source": "Official bio: https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319925.html — 陈广平，男，汉族，1980年12月生，河南正阳人，2002年11月参加工作，中共党员，大学本科学历。主持县政府全面工作。"
    },
    {
        "id": 3,
        "name": "朱东升",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共泌阳县委员会",
        "source": "Confirmed via 泌阳政府网 (2026-02-07): 县委书记朱东升..开展春节前走访慰问活动. Transitioned between Feb-July 2026 — 李勇 replaced 朱东升."
    },
    # ═══════ Government Leadership ═══════
    {
        "id": 4,
        "name": "狄艳松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986.01",
        "birthplace": "河北省河间市",
        "education": "中国地质大学在职研究生",
        "party_join": "中共党员",
        "work_start": "2009.11",
        "current_post": "县委常委、县政府副县长（负责常务工作）",
        "current_org": "泌阳县人民政府",
        "source": "Official bio: https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202512/t20251226_679992.html — 狄艳松，男，汉族，1986年1月出生，河北省河间市人，2009年11月参加工作，中共党员，中国地质大学在职研究生学历。"
    },
    {
        "id": 5,
        "name": "吴娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982.03",
        "birthplace": "河南省驿城区",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、县政府副县长",
        "current_org": "中共泌阳县委宣传部",
        "source": "Official bio: https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319924.html — 吴娟，女，汉族，1982年3月出生，河南省驿城区人，大学本科学历，中共党员。"
    },
    {
        "id": 6,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982.07",
        "birthplace": "河南平舆",
        "education": "郑州大学在职研究生",
        "party_join": "中共党员",
        "work_start": "2006.09",
        "current_post": "县政府党组成员、副县长",
        "current_org": "泌阳县人民政府",
        "source": "Official bio: https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319923.html — 刘涛，男，汉族，1982年07月生，河南平舆人，2006年9月参加工作，中共党员，郑州大学在职研究生学历。"
    },
    {
        "id": 7,
        "name": "闫明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979.04",
        "birthplace": "河南驻马店",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2000.03",
        "current_post": "县政府副县长、县公安局局长",
        "current_org": "泌阳县公安局",
        "source": "Official bio: https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319922.html — 闫明，男，汉族，1979年4月生，河南驻马店人，2000年3月参加工作，中共党员，研究生学历。"
    },
    {
        "id": 8,
        "name": "邱士用",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972.12",
        "birthplace": "河南泌阳",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、县财政局局长",
        "current_org": "泌阳县人民政府",
        "source": "Official bio: https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319920.html — 邱士用，男，汉族，1972年12月出生，河南省泌阳县人，大学本科学历，中共党员。"
    },
    {
        "id": 9,
        "name": "崔兰阁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986.05",
        "birthplace": "河南民权",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2010.07",
        "current_post": "县政府副县长",
        "current_org": "泌阳县人民政府",
        "source": "Official bio: https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319919.html — 崔兰阁，女，汉族，1986年5月出生，河南省民权县人，2010年7月参加工作，大学本科学历，中共党员。"
    },
    # ═══════ Other Key Leaders ═══════
    {
        "id": 10,
        "name": "朱瑞霞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共泌阳县委员会",
        "source": "Confirmed as 县委副书记 via 泌阳政府网 (2026-02-07): 春节走访慰问活动 article."
    },
    {
        "id": 11,
        "name": "张万兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "泌阳县人大常委会",
        "source": "Confirmed as 县人大常委会主任 via 泌阳政府网 (2026-02-07): 春节走访慰问活动 article."
    },
    {
        "id": 12,
        "name": "安生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "泌阳县政协",
        "source": "Confirmed as 县政协主席 via 泌阳政府网 (2026-02-07): 春节走访慰问活动 article."
    },
    {
        "id": 13,
        "name": "李培明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "泌阳县",
        "source": "Mentioned as 县领导 in 2026-07-16 article accompanying 李勇's site visit."
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共泌阳县委员会", "type": "党委", "level": "县处级", "parent": "中共驻马店市委", "location": "泌阳县"},
    {"id": 2, "name": "泌阳县人民政府", "type": "政府", "level": "县处级", "parent": "驻马店市人民政府", "location": "泌阳县"},
    {"id": 3, "name": "泌阳县人大常委会", "type": "人大", "level": "县处级", "parent": "驻马店市人大常委会", "location": "泌阳县"},
    {"id": 4, "name": "泌阳县政协", "type": "政协", "level": "县处级", "parent": "驻马店市政协", "location": "泌阳县"},
    {"id": 5, "name": "泌阳县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "驻马店市纪委监委", "location": "泌阳县"},
    {"id": 6, "name": "中共泌阳县委组织部", "type": "党委", "level": "县处级", "parent": "中共泌阳县委", "location": "泌阳县"},
    {"id": 7, "name": "中共泌阳县委宣传部", "type": "党委", "level": "县处级", "parent": "中共泌阳县委", "location": "泌阳县"},
    {"id": 8, "name": "泌阳县公安局", "type": "政府", "level": "县处级", "parent": "泌阳县人民政府", "location": "泌阳县"},
    {"id": 9, "name": "泌阳县财政局", "type": "政府", "level": "县处级", "parent": "泌阳县人民政府", "location": "泌阳县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 李勇 (id=1) — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "2026年（约2-7月间）到任，接替朱东升。此前职务待查。"},
    # 陈广平 (id=2) — 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作。到任时间待查。"},
    # 朱东升 (id=3) — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "县委书记（前任）", "start_date": "", "end_date": "~2026年初", "rank": "县处级正职", "note": "前任泌阳县委书记，2026年2月仍在任，后由李勇接替。去向待查。"},
    # 狄艳松 (id=4) — 常务副县长
    {"person_id": 4, "org_id": 2, "title": "县委常委、县政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县政府常务工作。2025年12月更新bio。"},
    # 吴娟 (id=5) — 宣传部长/副县长
    {"person_id": 5, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任副县长。"},
    # 刘涛 (id=6) — 副县长
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责办公室、政务公开、交通、文教、卫生、民政等。"},
    # 闫明 (id=7) — 副县长/公安局长
    {"person_id": 7, "org_id": 2, "title": "县政府副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公安、信访、司法等。"},
    {"person_id": 7, "org_id": 8, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 邱士用 (id=8) — 副县长/财政局长
    {"person_id": 8, "org_id": 2, "title": "县政府副县长、县财政局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责财政、自然资源、住建、应急管理等。"},
    {"person_id": 8, "org_id": 9, "title": "县财政局局长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 崔兰阁 (id=9) — 副县长
    {"person_id": 9, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责商务、工信、科技、市场管理、文旅等。"},
    # 朱瑞霞 (id=10) — 县委副书记
    {"person_id": 10, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张万兵 (id=11) — 人大主任
    {"person_id": 11, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 安生 (id=12) — 政协主席
    {"person_id": 12, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 李培明 (id=13) — 县领导
    {"person_id": 13, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "具体职务待查"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 李勇 ↔ 陈广平（党政搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "李勇任县委书记，陈广平任县长，为泌阳县当前党政正职搭档",
        "overlap_org": "泌阳县",
        "overlap_period": "2026—"
    },
    # 李勇 → 朱东升（前后任书记）
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "朱东升为前任泌阳县委书记，李勇于2026年接任",
        "overlap_org": "中共泌阳县委员会",
        "overlap_period": "2026"
    },
    # 陈广平 ↔ 狄艳松（政府正副职搭档）
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "陈广平为县长，狄艳松为常务副县长，为泌阳县政府正副职搭档",
        "overlap_org": "泌阳县人民政府",
        "overlap_period": "当前"
    },
    # 陈广平 ↔ 吴娟（政府班子成员）
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "陈广平为县长，吴娟为县委常委、副县长",
        "overlap_org": "泌阳县人民政府",
        "overlap_period": "当前"
    },
    # 李勇 ↔ 朱瑞霞（县委正副书记）
    {
        "person_a": 1, "person_b": 10,
        "type": "superior_subordinate",
        "context": "李勇为县委书记，朱瑞霞为县委副书记",
        "overlap_org": "中共泌阳县委员会",
        "overlap_period": "2026—"
    },
    # 李勇 ↔ 狄艳松（班子成员）
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "李勇为县委书记，狄艳松为县委常委、副县长",
        "overlap_org": "泌阳县委常委班子",
        "overlap_period": "当前"
    },
    # 李勇 ↔ 吴娟（班子成员）
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "李勇为县委书记，吴娟为县委常委、宣传部部长",
        "overlap_org": "泌阳县委常委班子",
        "overlap_period": "当前"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "李勇",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "驻马店市",
                "region": "泌阳县",
                "job": "县委书记",
                "task_id": "henan_泌阳县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_biyang_liyong",
                "name": "李勇",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "李勇_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共泌阳县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "未知",
                    "title": "早前任职",
                    "level": "",
                    "location": "",
                    "system": "unknown",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "李勇来泌阳县之前的任职经历未查到公开资料",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "~2026",
                    "end": "present",
                    "org": "中共泌阳县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "泌阳县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "2026年（约2-7月间）任命为泌阳县委书记，接替朱东升。首次以县委书记身份出现在2026年7月16日官方报道中。",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "organizations": [
                {"name": "中共泌阳县委员会", "role": "县委书记", "period": "2026—", "source_ids": ["S001"]}
            ],
            "relationships": [
                {
                    "person": "陈广平",
                    "person_id": "henan_biyang_chenguangping",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "李勇任县委书记，陈广平任县长，为泌阳县当前党政正职搭档",
                    "overlap_org": "泌阳县",
                    "overlap_period": "2026—",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "person": "朱东升",
                    "person_id": "henan_biyang_zhudongsheng",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "朱东升为前任泌阳县委书记，李勇于2026年接任",
                    "overlap_org": "中共泌阳县委员会",
                    "overlap_period": "2026",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "带队深入县先进制造业开发区开展现场办公，调研企业生产、项目建设",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "泌阳县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["泌阳县"],
                "promotion_velocity": {
                    "summary": "",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": ["项目为王", "服务企业就是服务发展"],
                "management_signals": ["现场办公、一线办公机制"],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "泌阳县委书记李勇带队深入县先进制造业开发区开展现场办公", "url": "https://www.biyang.gov.cn/zwyw/tpxw/202607/t20260721_713250.html", "publisher": "泌阳县人民政府", "published_at": "2026-07-16", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李勇为泌阳县委书记"},
                {"id": "S003", "title": "泌阳县四个班子领导开展春节前走访慰问活动（确认朱东升为前任书记）", "url": "https://www.biyang.gov.cn/zwyw/tpxw/202602/t20260211_688924.html", "publisher": "泌阳县人民政府", "published_at": "2026-02-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2026年2月朱东升仍在县委书记岗位"}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "李勇的完整履历（出生年份、籍贯、教育背景、来泌阳前任职经历、入党时间、参加工作时间）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "李勇的出生年份、籍贯、教育背景是什么？",
                    "why_it_matters": "作为当前一把手，基本信息对建立完整人物档案至关重要",
                    "suggested_queries": ["李勇 泌阳县委书记 简历", "李勇 出生年月", "李勇 任前公示"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "李勇在来泌阳县之前的任职经历是什么？从哪个岗位调任泌阳县委书记？",
                    "why_it_matters": "理解其晋升路径和关系网络来源",
                    "suggested_queries": ["李勇 驻马店 任职", "李勇 工作经历", "李勇 此前 担任"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "李勇何时正式到任泌阳县委书记？具体的任命时间？",
                    "why_it_matters": "精确时间线有助于理解交接节奏",
                    "suggested_queries": ["泌阳县 县委书记 任命 2026", "李勇 任泌阳县委书记"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "陈广平",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "驻马店市",
                "region": "泌阳县",
                "job": "县长",
                "task_id": "henan_泌阳县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_biyang_chenguangping",
                "name": "陈广平",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1980.12",
                "birthplace": "河南正阳",
                "native_place": "河南省正阳县",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": "大学本科",
                        "study_type": "unknown",
                        "source_ids": ["S002"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "2002.11",
                "dedupe_keys": {
                    "name_birth": "陈广平_198012",
                    "name_birthplace": "陈广平_正阳",
                    "official_profile_url": "https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319925.html"
                }
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "泌阳县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "泌阳县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "泌阳县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "现任泌阳县委副书记、县长。主持县政府全面工作。到任时间待查。",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "start": "2002.11",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "来泌阳县前任职",
                    "level": "",
                    "location": "",
                    "system": "unknown",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "公开资料未找到陈广平来泌阳县之前的完整任职经历。已知2002年11月参加工作，正阳县人，可能在正阳县等驻马店其他县区有任职经历。",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"name": "泌阳县人民政府", "role": "县长", "period": "至今", "source_ids": ["S002"]},
                {"name": "中共泌阳县委员会", "role": "县委副书记", "period": "至今", "source_ids": ["S002"]}
            ],
            "relationships": [
                {
                    "person": "李勇",
                    "person_id": "henan_biyang_liyong",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "陈广平任县长，李勇任县委书记，为泌阳县当前党政正职搭档",
                    "overlap_org": "泌阳县",
                    "overlap_period": "2026—",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                },
                {
                    "person": "狄艳松",
                    "person_id": "henan_biyang_diyansong",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "陈广平为县长，狄艳松为常务副县长协助其工作",
                    "overlap_org": "泌阳县人民政府",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026",
                    "domain": "economic_development",
                    "achievement_or_event": "主持县政府全面工作，分管审计局",
                    "role_in_event": "县长",
                    "measurable_outcome": "",
                    "location": "泌阳县",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": ["正阳县", "泌阳县"],
                "promotion_velocity": {
                    "summary": "现任泌阳县县长（正处级），1980年出生，为正阳县人，2002年参加工作。",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "县委书记李勇带队深入县先进制造业开发区开展现场办公", "url": "https://www.biyang.gov.cn/zwyw/tpxw/202607/t20260721_713250.html", "publisher": "泌阳县人民政府", "published_at": "2026-07-16", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "陈广平以县长身份陪同参加"},
                {"id": "S002", "title": "陈广平 — 泌阳县政府领导信息", "url": "https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319925.html", "publisher": "泌阳县人民政府", "published_at": "2024-10-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "含陈广平简历：1980.12，河南正阳，2002.11参加工作，中共党员，大学本科学历"},
                {"id": "S004", "title": "狄艳松 — 泌阳县政府领导信息", "url": "https://www.biyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202512/t20251226_679992.html", "publisher": "泌阳县人民政府", "published_at": "2025-12-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "狄艳松为常务副县长，协助陈广平工作"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "陈广平的完整履历（来泌阳前任职经历、教育院校专业）大部分缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "陈广平在来泌阳县之前的任职经历是什么？从哪个岗位调任泌阳县长？",
                    "why_it_matters": "理解其职业背景和关系网络来源。正阳人，可能曾在正阳县或驻马店市直单位任职。",
                    "suggested_queries": ["陈广平 正阳 任职", "陈广平 驻马店 任职", "陈广平 工作经历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "陈广平的教育经历的具体院校和专业是什么？",
                    "why_it_matters": "有助于教育背景分析和校友关系追踪",
                    "suggested_queries": ["陈广平 大学", "陈广平 毕业院校"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "陈广平何时到任泌阳县长？具体调任时间？",
                    "why_it_matters": "理清职务交接时间线",
                    "suggested_queries": ["泌阳县 县长 任命 陈广平"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 3,
        "name": "朱东升",
        "job": "前任县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "驻马店市",
                "region": "泌阳县",
                "job": "县委书记",
                "task_id": "henan_泌阳县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_biyang_zhudongsheng",
                "name": "朱东升",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "朱东升_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "未知（前任县委书记）",
                "current_org": "",
                "administrative_rank": "",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": ["S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "~2026年初",
                    "org": "中共泌阳县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "泌阳县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "2026年2月仍在泌阳县委书记岗位。其后由李勇接替。",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到朱东升的完整履历、来泌阳前任职经历及调任后的去向",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"name": "中共泌阳县委员会", "role": "县委书记（前任）", "period": "至~2026年初", "source_ids": ["S003"]}
            ],
            "relationships": [
                {
                    "person": "李勇",
                    "person_id": "henan_biyang_liyong",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "朱东升为前任泌阳县委书记，李勇于2026年接任",
                    "overlap_org": "中共泌阳县委员会",
                    "overlap_period": "2026",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003"]
                },
                {
                    "person": "陈广平",
                    "person_id": "henan_biyang_chenguangping",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "朱东升任县委书记期间，陈广平任县长",
                    "overlap_org": "泌阳县",
                    "overlap_period": "",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["泌阳县"],
                "promotion_velocity": {
                    "summary": "",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S003", "title": "泌阳县四个班子领导开展春节前走访慰问活动", "url": "https://www.biyang.gov.cn/zwyw/tpxw/202602/t20260211_688924.html", "publisher": "泌阳县人民政府", "published_at": "2026-02-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认朱东升2026年2月以县委书记身份带队慰问"}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "朱东升的完整履历（出生年份、籍贯、教育、来泌阳前任职经历、调任后去向）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "朱东升离开泌阳县委书记岗位后的去向是什么？",
                    "why_it_matters": "关键的前任去向信息，直接影响对班子交接和晋升路径的理解",
                    "suggested_queries": ["朱东升 调任", "朱东升 驻马店", "朱东升 现任"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "朱东升的出生年份、籍贯、教育背景是什么？何时起任泌阳县委书记？",
                    "why_it_matters": "建立完整人物档案",
                    "suggested_queries": ["朱东升 简历", "朱东升 出生年月"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
]


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    written_person_files = []
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-驻马店市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        written_person_files.append(path)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"  Person JSON count: {len(written_person_files)}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()
