#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汝阳县 (Ruyang County), 洛阳市, 河南省.

Investigation date: 2026-08-05
Task ID: henan_汝阳县
Level: 县
Targets: 县委书记 & 县长

Research sources (confirmed 2026-08-05, degraded-web partial-evidence build):
  - 百度百科「赵书政」(baike.baidu.com/item/赵书政) — 现任汝阳县委书记完整履历
  - 百度百科「姬素娟」(baike.baidu.com/item/姬素娟) — 前任县长(2022-2026),2026-07-03任洛阳市司法局局长
  - 百度百科「汝阳县人民政府」(baike.baidu.com/item/汝阳县人民政府) — 现任县长耿笑及副县长名单
  - 百度百科「中国共产党汝阳县委员会」(baike.baidu.com/item/中国共产党汝阳县委员会) — 第十四届县委常委会名单
  - 百度百科「赵振峰」(baike.baidu.com/item/赵振峰) — 前任县委书记(2022-2023),2024-02任洛阳市政协副主席
  - 搜狗搜索「姬素娟当选汝阳县人民政府县长」结果 (2026-08-05)
  - 洛阳广播电视台/老城区政官网 — 赵书政履历交叉印证

Confirmed roster / timeline:
- 赵书政(现任县委书记): 1976-01, 汉族, 河南嵩县人, 大学学历, 2001-08入党, 1996-04参加工作;
  栾川基层(1996-2005)→洛阳市文联/市委统战部(2005-2011)→汝阳县副县长(2011-2016)→吉利区委常委、组织部部长(2016-2017)→
  洛阳市政府副秘书长(2017-2019)→洛阳市住建局党组书记、局长(2019-2021)→老城区长(2021-2023)→老城区委书记(2023-2026)→
  2026-04-01 汝阳县全面领导干部会议宣布任汝阳县委书记 → 2026-05-09 兼县人武部党委第一书记. 河南省第十四届人大代表.
- 耿笑(现任县长): 曾任汝阳县委常委、组织部部长(第十四届常委会), 现任中共汝阳县委副书记、汝阳县人民政府县长(据汝阳县人民政府词条).
  履历细节公开资料有限(待查). 疑似 2026 年中接任前任县长姬素娟.
- 姬素娟(前任县长, 2022-05~2026-06): 女, 1973-01, 河南伊川人, 河南省委党校大学学历, 党员;
  历任中共伊川县委委员、常委、政法委书记(2016-07副县级)→洛阳市委乡村振兴局局长(2021-08~2022-05)→
  2022-05 汝阳县委副书记、副县长、代县长→县长(2022-下半年至2026-06, 洛阳市十四届人大代表) → 2026-07-03 任洛阳市司法局局长.
- 赵振峰(前任县委书记, 2022-01~2023): 男, 1969-01, 河南偃师人, 在职研究生/管理学硕士, 中共党员;
  曾是汝阳县长(2021-08~2022-01)→2022-01-29 汝阳县委书记(不再任县长)→2024-02 任洛阳市政协党组成员、副主席(现任).
- 潘峰(更早县委书记, 2021-08~2022-01): 2021-08-15 当选中共汝阳县委第十四届委员会书记(详细履历待核)。
- 汝阳县委第十四届常委会: 书记 赵书政, 副书记 姬素娟(离任)、耿笑、韩海卿;
  常委: 张步涛(常务副县长)、娄军峰(统战部长)、王为民(政法委书记)、刘冰(人武部长)、杨静波(内埠镇党委书记)、
  李楠(宣传部部长、副县长)、王晓辉(办公室主任兼常务副县长/县政府党组副书记——据政府条目)、吴彦(县纪委书记、县监委主任)。
- 县政府现任副县长: 王晓辉(常务), 刘喜(政府党组成员、副县长、公安局长)、王飞、张根生、胡武勋、何晓刚、胡晨、师小丽(女)、李尚宇。

Gaps flagged in person JSON `open_questions`:
  - 耿笑出生/民族/籍贯/教育/入党/工作起始及完整履历; 其当选/任命为县长日期及投票佐证
  - 耿笑与艳阳姬素娟交接的确切时间线; 谁在2023-2026.04接任县委书记(赵书政之前的历任县城书记链)
  - 接替赵振峰(2023)至赵书政(2026.04)这期间的县委先生书记姓名及履历
  - 各常委完整履历(张步涛、娄军峰、王为民、吴彦、韩海卿等)
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "汝阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# Staging paths (written by this script; promoted by scripts/process_tmp.py)
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══ Core Leadership ═══
    {
        "id": 1,
        "name": "赵书政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "河南嵩县",
        "education": "大学学历",
        "party_join": "2001年8月",
        "work_start": "1996年4月",
        "current_post": "县委书记",
        "current_org": "中共汝阳县委员会",
        "source": "百度百科「赵书政」(2026-08); 汝阳县全县领导干部会议(2026-04-01宣布任书记)",
    },
    {
        "id": 2,
        "name": "耿笑",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "汝阳县人民政府",
        "source": "百度百科「汝阳县人民政府」(现任县长:耿笑);百度百科「中国共产党汝阳县委员会」(曾任县委组织部部长)",
    },
    # ═══ Predecessors ═══
    {
        "id": 3,
        "name": "姬素娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "河南伊川",
        "education": "河南省委党校大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛阳市司法局局长",
        "current_org": "洛阳市司法局",
        "source": "百度百科「姬素娟」(2026-07-03任洛阳市司法局局长;曾任汝阳县县长)",
    },
    {
        "id": 4,
        "name": "赵振峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年1月",
        "birthplace": "河南偃师",
        "education": "在职研究生、管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛阳市政协副主席",
        "current_org": "洛阳市政协",
        "source": "百度百科「赵振峰」(曾任汝阳县委书记;2024-02任洛阳政协副主席)",
    },
    # ═══ Current 常委会成员 ═══
    {
        "id": 5,
        "name": "韩海卿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共汝阳县委员会",
        "source": "百度百科「中国共产党汝阳县委员会」(县委副书记)",
    },
    {
        "id": 7,
        "name": "王晓辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常委副县长、县政府党组副书记",
        "current_org": "汝阳县人民政府",
        "source": "百度百科「汝阳县人民政府」(副县长、县政府党组副书记);「中共汝阳县委员会」(办公室主任)",
    },
    {
        "id": 6,
        "name": "吴彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "汝阳县纪委监委",
        "source": "百度百科「中国共产党第十七届汝阳县委员会」(县纪委书记、县监委主任)",
    },
    {
        "id": 8,
        "name": "娄军峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共汝阳县委员会",
        "source": "百度百科「中国共产党第十七届汝阳县委员会」(常委、统战部)",
    },
    {
        "id": 9,
        "name": "王为民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共汝阳县委员会",
        "source": "百度百科「中国共产党第十七届汝阳县委员会」(常委、政法)",
    },
    {
        "id": 10,
        "name": "李楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共汝阳县委员会",
        "source": "百度百科「中国共产党第十七届汝阳县委员会」(常委、宣传部长、副县长)",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共汝阳县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "汝阳县"},
    {"id": 2, "name": "汝阳县人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "汝阳县"},
    {"id": 3, "name": "汝阳县人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "汝阳县"},
    {"id": 4, "name": "汝阳县政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "汝阳县"},
    {"id": 5, "name": "汝阳县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "汝阳县"},
    {"id": 6, "name": "汝阳县监察委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市监委", "location": "汝阳县"},
    {"id": 7, "name": "洛阳市司法局", "type": "政府", "level": "地厅级", "parent": "洛阳市人民政府", "location": "洛阳市"},
    {"id": 8, "name": "洛阳市政协", "type": "政协", "level": "地厅级", "parent": "河南省政协", "location": "洛阳市"},
    {"id": 9, "name": "中共洛阳市老城区委", "type": "党委", "level": "县级区委", "parent": "中共洛阳市委", "location": "洛阳市"},
    {"id": 10, "name": "洛阳市住房和城乡建设局", "type": "政府", "level": "地厅级部门", "parent": "洛阳市人民政府", "location": "洛阳市"},
    {"id": 11, "name": "洛阳市人民政府", "type": "政府", "level": "地厅级", "parent": "河南省人民政府", "location": "洛阳市"},
    {"id": 12, "name": "中共洛阳市吉利区委", "type": "党委", "level": "县级区委", "parent": "中共洛阳市委", "location": "洛阳市"},
    {"id": 13, "name": "中共洛阳市委统战部", "type": "党委", "level": "地厅级部门", "parent": "中共洛阳市委", "location": "洛阳市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 赵书政
    {"person_id": 1, "org_id": 13, "title": "洛阳市委统战部理论宣传科科长", "start_date": "2008", "end_date": "2011", "rank": "县处级副职", "note": "2003-2007借调市委组织部组织科"},
    {"person_id": 1, "org_id": 2, "title": "汝阳县副县长", "start_date": "2011-05", "end_date": "2016-06", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "吉利区委常委、组织部部长", "start_date": "2016-06", "end_date": "2017-06", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "洛阳市政府副秘书长", "start_date": "2017-06", "end_date": "2019-03", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "洛阳市住建局党组书记、局长", "start_date": "2019-03", "end_date": "2021-06", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "洛阳市老城区委副书记、区长", "start_date": "2021-06", "end_date": "2023-06", "rank": "县处级正职", "note": "兼洛阳古城党工委书记"},
    {"person_id": 1, "org_id": 9, "title": "洛阳市老城区委书记", "start_date": "2023-05", "end_date": "2026-04", "rank": "县处级正职", "note": "2023-06起兼区人武部党委第一书记"},
    {"person_id": 1, "org_id": 1, "title": "汝阳县委书记", "start_date": "2026-04-01", "end_date": "present", "rank": "县处级正职", "note": "2026-05-09起兼县人武部党委第一书记"},
    # 耿笑 — 现任县长
    {"person_id": 2, "org_id": 1, "title": "汝阳县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县委第十四届常委会委员;具体时间待核"},
    {"person_id": 2, "org_id": 2, "title": "汝阳县县长", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "现任汝阳县长(據汝阳县人民政府词条);上任时间/会议佐证待核"},
    # 姬素娟 — 前任县长
    {"person_id": 3, "org_id": 1, "title": "汝阳县委副书记", "start_date": "2022-05", "end_date": "2026-06", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "汝阳县副县长、代县长", "start_date": "2022-05", "end_date": "2022-06", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "汝阳县县长", "start_date": "2022-06", "end_date": "2026-06", "rank": "县处级正职", "note": "2026-07提任市司法局局长"},
    {"person_id": 3, "org_id": 7, "title": "洛阳市司法局局长", "start_date": "2026-07-03", "end_date": "present", "rank": "地厅级正职", "note": "洛阳市第十六届人大常委会第三十一次会议通过"},
    # 赵振峰 — 前任书记
    {"person_id": 4, "org_id": 2, "title": "汝阳县县长", "start_date": "2021-08", "end_date": "2022-01", "rank": "县处级正职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "汝阳县委书记", "start_date": "2022-01", "end_date": "2023", "rank": "县处级正职", "note": "2024-02不再任县委"},
    {"person_id": 4, "org_id": 8, "title": "洛阳市政协副主席", "start_date": "2024-02", "end_date": "present", "rank": "地厅级副职", "note": "政协第十四届洛阳市委员会副主席"},
    # 韩海卿 — 副书记
    {"person_id": 5, "org_id": 1, "title": "汝阳县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王晓辉 — 常务副县长
    {"person_id": 7, "org_id": 1, "title": "汝阳县委常委、办公室主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "汝阳县副县长、县政府党组副书记(常务)", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 吴彦 — 纪委书记
    {"person_id": 6, "org_id": 1, "title": "汝阳县委常委、县纪委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "汝阳县监委主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 娄军峰 — 统战部长
    {"person_id": 8, "org_id": 1, "title": "汝阳县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王为民 — 政法委书记
    {"person_id": 9, "org_id": 1, "title": "汝阳县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李楠 — 宣传部长
    {"person_id": 10, "org_id": 1, "title": "汝阳县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "汝阳县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 赵书政 ↔ 耿笑(现任党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "赵书政任县委书记,耿笑任县长,汝阳县党政正职搭档", "overlap_org": "汝阳县", "overlap_period": "2026至今"},
    # 赵书政 ↔ 姬素娟(前任县长)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "赵书政2026-04任书记,姬素娟同年6月离任县长前同班子", "overlap_org": "汝阳县", "overlap_period": "2026"},
    # 耿笑 ↔ 姬素娟(前后任县长)
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "姬素娟2022-2026任县长,耿笑接任县长", "overlap_org": "汝阳县人民政府", "overlap_period": "2022-2026"},
    # 赵书政 ↔ 赵振峰(前后任县委书记)
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "赵振峰2022-2023任县委书记,赵书政2026接任县委书记;两者均自洛阳市委/城区/市直系统成长", "overlap_org": "中共汝阳县委员会", "overlap_period": "2022-2026"},
    # 姬素娟 ↔ 赵振峰(前后任领导关系:赵任书记时姬任县长)
    {"person_a": 3, "person_b": 4, "type": "superior_subordinate", "context": "赵振峰2022-2023任县委书记时,姬素娟任县长,党政正职搭档", "overlap_org": "汝阳县", "overlap_period": "2022-2023"},
    # 县委书记—班子成员
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共汝阳县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共汝阳县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "汝阳县人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与统战部长", "overlap_org": "中共汝阳县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与政法委书记", "overlap_org": "中共汝阳县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记与宣传部长", "overlap_org": "中共汝阳县委员会", "overlap_period": "当前"},
    # 县长—县政府成员
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "汝阳县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长(宣传部长)", "overlap_org": "汝阳县人民政府", "overlap_period": "当前"},
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "赵书政",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "洛阳市", "region": "汝阳县",
                "job": "县委书记", "task_id": "henan_汝阳县", "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_ruyang_zhaoshuzheng",
                "name": "赵书政", "aliases": [],
                "gender": "男", "ethnicity": "汉族",
                "birth": "1976年1月", "birthplace": "河南嵩县", "native_place": "河南嵩县",
                "education": [{"period": "", "institution": "大学(未明确学校)", "major": "", "degree": "大学", "study_type": "full_time", "source_ids": ["S001"]}],
                "party_join": "2001年8月", "work_start": "1996年4月",
                "dedupe_keys": {"name_birth": "赵书政_1976年1月", "name_birthplace": "赵书政_河南嵩县", "official_profile_url": "https://baike.baidu.com/item/赵书政"}
            },
            "current_status": {
                "current_post": "县委书记", "current_org": "中共汝阳县委员会",
                "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {"start": "1996-04", "end": "2001-12", "org": "栾川县老君山林场", "title": "干部", "level": "基层", "location": "栾川县", "system": "government", "rank": "科员", "is_key_promotion": False, "notes": "2000-2001抽调县旅游工作委员会", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2003-05", "end": "2005-08", "org": "栾川县文学艺术界联合会", "title": "副主席", "level": "县区级", "location": "栾川县", "system": "other", "rank": "副科", "is_key_promotion": False, "notes": "含2001-2003县水利局水资办干部", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2005-12", "end": "2011-05", "org": "中共洛阳市委统战部", "title": "科长(理论宣传科)", "level": "地厅级部门", "location": "洛阳市", "system": "party", "rank": "正科", "is_key_promotion": False, "notes": "前期借调市委组织部组织科", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2011-05", "end": "2016-06", "org": "汝阳县人民政府", "title": "副县长", "level": "县处级副职", "location": "汝阳县", "system": "government", "rank": "县处级副职", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2016-06", "end": "2017-06", "org": "中共洛阳市吉利区委", "title": "常委、组织部部长", "level": "县处级副职", "location": "洛阳市", "system": "organization", "rank": "县处级副职", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2017-06", "end": "2019-03", "org": "洛阳市人民政府", "title": "副秘书长", "level": "地厅级机关", "location": "洛阳市", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2019-03", "end": "2021-06", "org": "洛阳市住房和城乡建设局", "title": "党组书记、局长", "level": "地厅级部门", "location": "洛阳市", "system": "government", "rank": "县处级正职", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2021-06", "end": "2023-05", "org": "中共洛阳市老城区委/老城区人民政府", "title": "区委副书记、区长", "level": "县处级正职", "location": "洛阳市", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "兼洛阳古城党工委书记", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2023-05", "end": "2026-04", "org": "中共洛阳市老城区委", "title": "区委书记", "level": "县处级正职", "location": "洛阳市", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "兼区人武部党委第一书记", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2026-04-01", "end": "present", "org": "中共汝阳县委员会", "title": "县委书记", "level": "县处级正职", "location": "汝阳县", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-04-01全县领导干部会议宣布;2026-05-09兼县人武部党委第一书记", "confidence": "confirmed", "source_ids": ["S001", "S002"]}
            ],
            "organizations": [
                {"name": "中共汝阳县委员会", "role": "县委书记", "period": "2026-04至今", "source_ids": ["S001", "S002"]},
                {"name": "中共洛阳市老城区委", "role": "区委书记/区长", "period": "2021-06~2026-04", "source_ids": ["S001"]},
                {"name": "洛阳市住建局", "role": "党组书记、局长", "period": "2019-03~2021-06", "source_ids": ["S001"]},
                {"name": "汝阳县人民政府", "role": "副县长", "period": "2011-05~2016-06", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "耿笑", "person_id": "henan_ruyang_gengxiao", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "赵书政任书记,耿笑任县长,党政正职搭档", "overlap_org": "汝阳县", "overlap_period": "2026至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "姬素娟", "person_id": "henan_ruyang_jisujuan", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "赵书政2026-04任书记,姬素娟2026年6月离任县长,曾同班子", "overlap_org": "汝阳县", "overlap_period": "2026", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001", "S003"]},
                {"person": "赵振峰", "person_id": "henan_ruyang_zhaozhenfeng", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "赵振峰2022-2024任汝阳县委书记,赵书政2026年4月接任", "overlap_org": "中共汝阳县委员会", "overlap_period": "2022-2026", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S004"]}
            ],
            "governance_record": [
                {"period": "2021-2026", "domain": "urban_construction", "achievement_or_event": "老城区委书记任内城市更新/洛阳古城开发管理", "role_in_event": "区委书记/区长", "measurable_outcome": "", "location": "洛阳市老城区", "confidence": "plausible", "source_ids": ["S001"]},
                {"period": "2019-2021", "domain": "urban_construction", "achievement_or_event": "洛阳市住建局党组书记、局长;获'全国住房和城乡建设系统抗击新冠疫情先进个人'拟表彰(2020-12)", "role_in_event": "局长", "measurable_outcome": "入选拟表彰名单", "location": "洛阳市", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "professional_profile": {
                "primary_specializations": ["urban_construction", "party_leadership"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government", "organization", "urban_construction"],
                "geographic_pattern": ["嵩县(籍)", "栾川县", "洛阳市(统战/政府/住建/老城区)", "汝阳县"],
                "promotion_velocity": {
                    "summary": "由栾川基层科员逐步升迁:统战部→汝阳副县长→吉利区委常委→市政府副秘书长→市住建局长→老城区长/书记→汝阳县委书记,约30年完成县域主政",
                    "notable_fast_promotions": ["2016-2021五年内从区委组织部长升任市直正处级局长", "老城区区长→区委书记(2021-2023)"]
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "起步于栾川林场/基层一线,履历涵盖林场、水利、文旅、组织、住建等多领域", "confidence": "plausible", "source_ids": ["S001"]},
                    {"trait": "organization_track", "evidence": "曾任吉利区委组织部部长,并借调市委组织部", "confidence": "plausible", "source_ids": ["S001"]}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息;2020-12入选全国住房城乡建设系统抗疫先进个人拟表彰名单(正面)", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "百度百科「赵书政」", "url": "https://baike.baidu.com/item/赵书政", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "官方履历式人物信息"},
                {"id": "S002", "title": "汝阳县全县领导干部会议/县人武部任职宣布大会", "url": "", "publisher": "汝阳县/洛阳市委组织部", "published_at": "2026-04-01/2026-05-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "宣布赵书政任汝阳县委书记;兼任人武部第一书记"}
            ],
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete",
                "relationship_confidence": "high", "biggest_gap": "赵书政在教育/major 学历的具体学校与专业未明确"
            },
            "open_questions": [
                {"priority": "medium", "question": "赵书政的大学就读院校与专业具体是什么?", "why_it_matters": "补全学历背景", "suggested_queries": ["赵书政 学历 院学校洛阳"], "last_attempted": AS_OF},
                {"priority": "low", "question": "赵书政在汝阳县委书记任上的施政方向?", "why_it_matters": "了解其治理重点", "suggested_queries": ["赵书政 汝阳 部署"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "耿笑",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "洛阳市", "region": "汝阳县",
                "job": "县长", "task_id": "henan_汝阳县", "time_focus": "2026"
            },
            "identity": {
                "current_id": "henan_ruyang_gengxiao",
                "name": "耿笑", "aliases": [],
                "gender": "", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": "https://baike.baidu.com/item/耿笑"}
            },
            "current_status": {
                "current_post": "县委副书记、县长", "current_org": "汝阳县人民政府",
                "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "", "end": "", "org": "中共汝阳县委员会", "title": "汝阳县委常委、组织部部长", "level": "县处级副职", "location": "汝阳县", "system": "organization", "rank": "县处级副职", "is_key_promotion": False, "notes": "汝阳县委第十四届常委会成员", "confidence": "confirmed", "source_ids": ["S002"]},
                {"start": "2026", "end": "present", "org": "汝阳县人民政府", "title": "县委副书记、县长", "level": "县处级正职", "location": "汝阳县", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "接任姬素娟县长职;具体当选日期待核", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "出生、籍贯、教育、入党/工作起点及完整履历未获公开资料", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "汝阳县人民政府", "role": "县长", "period": "2026至今", "source_ids": ["S001"]},
                {"name": "中共汝阳县委员会", "role": "常委/组织部部长", "period": "", "source_ids": ["S002"]}
            ],
            "relationships": [
                {"person": "赵书政", "person_id": "henan_ruyang_zhaoshuzheng", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "耿笑任县长,赵书政任县委书记,党政正职正面", "overlap_org": "汝阳县", "overlap_period": "2026至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "姬素娟", "person_id": "henan_ruyang_jisujuan", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "姬素娟任县长(2022-2026),耿笑接任县长", "overlap_org": "汝阳县人民政府", "overlap_period": "2022-2026", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S003"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown",
                "systems_experience": ["organization", "government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [], "speech_themes": [], "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现相关公开负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "百度百科「汝阳县人民政府」(现任县长)耿笑", "url": "https://baike.baidu.com/item/汝阳县人民政府", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "词条'现任领导'栏:县长耿笑;含副县长名单"},
                {"id": "S002", "title": "百度百科「中国共产党汝阳县委员会」", "url": "https://baike.baidu.com/item/中国共产党汝阳县委员会", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "耿笑(原为组织部部长)"},
                {"id": "S003", "title": "百度百科「姬素娟」", "url": "https://baike.baidu.com/item/姬素娟", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "姬素娟卸任县长,2026-07-03任洛阳市司法局局长"}
            ],
            "confidence_summary": {
                "identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                "relationship_confidence": "medium", "biggest_gap": "耿笑出生/教育/完整履历与任县长批准时间均未获取"
            },
            "open_questions": [
                {"priority": "critical", "question": "耿笑任汝阳县长的任命时间、批准机关(人大)与履历背景?", "why_it_matters": "确认党政正职搭档链条与完整履历", "suggested_queries": ["耿笑 汝阳 县长 任命", "耿笑 简历"], "last_attempted": AS_OF},
                {"priority": "high", "question": "耿笑此前从事经历(是否长期任汝阳组织部长后升任县长)?", "why_it_matters": "还原其成长路径", "suggested_queries": ["耿笑 汝阳 组织部 部长"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 3,
        "name": "姬素娟",
        "job": "前任县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "洛阳市", "region": "汝阳县",
                "job": "前任县长", "task_id": "henan_汝阳县", "time_focus": "2026"
            },
            "identity": {
                "current_id": "henan_ruyang_jisujuan",
                "name": "姬素娟", "aliases": [],
                "gender": "女", "ethnicity": "汉族",
                "birth": "1973年1月", "birthplace": "河南伊川", "native_place": "河南伊川",
                "education": [{"period": "", "institution": "河南省委党校", "major": "", "degree": "大学(党校)", "study_type": "party_school", "source_ids": ["S001"]}],
                "party_join": "中共党员", "work_start": "",
                "dedupe_keys": {"name_birth": "姬素娟_1973年1月", "name_birthplace": "姬素娟_河南伊川", "official_profile_url": "https://baike.baidu.com/item/姬素娟"}
            },
            "current_status": {
                "current_post": "洛阳市司法局局长", "current_org": "洛阳市司法局",
                "administrative_rank": "地级市局长(正职)", "as_of": AS_OF, "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "2016-07", "end": "2021-08", "org": "中共伊川县委", "title": "县委常委、政法委书记", "level": "县处级副职", "location": "伊川县", "system": "party", "rank": "县处级副职", "is_key_promotion": True, "notes": "曾任伊川县委委员、常委、政法委书记", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2021-08", "end": "2022-05", "org": "洛阳市乡村振兴局", "title": "局长", "level": "地厅级部门", "location": "洛阳市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2022-05", "end": "2022-06", "org": "汝阳县人民政府", "title": "县委副书记、副县长、代县长", "level": "县处级正职", "location": "汝阳县", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2022-06", "end": "2026-06", "org": "汝阳县人民政府", "title": "县长", "level": "县处级正职", "location": "汝阳县", "system": "government", "rank": "县处级正职", "is_key_promotion": False, "notes": "河南省第十四届人大代表", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2026-07-03", "end": "present", "org": "洛阳市司法局", "title": "局长", "level": "地厅级正职", "location": "洛阳市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2026-07-03洛阳市第十六届人大常委会第三十一次会议任命", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [
                {"name": "洛阳市司法局", "role": "局长", "period": "2026-07至今", "source_ids": ["S001"]},
                {"name": "汝阳县人民政府", "role": "县长", "period": "2022-05~2026-06", "source_ids": ["S001"]},
                {"name": "洛阳市乡村振兴局", "role": "局长", "period": "2021-08~2022-05", "source_ids": ["S001"]},
                {"name": "中共伊川县委", "role": "常委、政法委书记", "period": "2016-07~2021-08", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "耿笑", "person_id": "henan_ruyang_gengxiao", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "姬素娟任县长(2022-2026),耿笑接任县长", "overlap_org": "汝阳县人民政府", "overlap_period": "2022-2026", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "赵振峰", "person_id": "henan_ruyang_zhaozhenfeng", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "赵振峰任县委书记(2022-2023)时姬任县长", "overlap_org": "汝阳县", "overlap_period": "2022-2023", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {"period": "2022-2026", "domain": "economic_development", "achievement_or_event": "汝阳县长任内县域发展", "role_in_event": "政府主要负责人", "measurable_outcome": "", "location": "汝阳县", "confidence": "unverified", "source_ids": []}
            ],
            "professional_profile": {
                "primary_specializations": ["public_security", "judicial"], "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["party", "government", "public_security", "judicial"],
                "geographic_pattern": ["伊川", "洛阳市", "汝阳县"],
                "promotion_velocity": {"summary": "伊川政法委书记→市乡村振兴局局长→汝阳县长→洛阳市司法局长,跨系统/跨县域历练后进入市直部门", "notable_fast_promotions": ["2022半年内由乡村振兴局长转任县长"]}
            },
            "work_style_and_personality": {
                "public_style_indicators": [{"trait": "discipline_oriented", "evidence": "出身政法委、政法/司法系统履历", "confidence": "plausible", "source_ids": ["S001"]}],
                "speech_themes": [], "management_signals": [],
                "caveat": "Work style is inferred from public records, not a psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "百度百科「姬素娟」", "url": "https://baike.baidu.com/item/姬素娟", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "现任洛阳市司法局局长;曾任汝阳县长(2022-2026);全履历记录"}
            ],
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete",
                "relationship_confidence": "high", "biggest_gap": "姬素娟2008-2016间具体基层履历未逐一列示"
            },
            "open_questions": [
                {"priority": "low", "question": "姬素娟2008年以前基层履历及其中任政法口的具体情况?", "why_it_matters": "补全早期关系", "suggested_queries": ["姬素娟 伊川 政法委书记 此前"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 4,
        "name": "赵振峰",
        "job": "前任县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "洛阳市", "region": "汝阳县",
                "job": "前任县委书记", "task_id": "henan_汝阳县", "time_focus": "2026"
            },
            "identity": {
                "current_id": "henan_ruyang_zhaozhenfeng",
                "name": "赵振峰", "aliases": [],
                "gender": "男", "ethnicity": "汉族",
                "birth": "1969年1月", "birthplace": "河南偃师", "native_place": "河南偃师",
                "education": [{"period": "", "institution": "在职研究生", "major": "管理学", "degree": "硕士", "study_type": "part_time", "source_ids": ["S001"]}],
                "party_join": "中共党员", "work_start": "",
                "dedupe_keys": {"name_birth": "赵振峰_1969年1月", "name_birthplace": "赵振峰_河南偃师", "official_profile_url": "https://baike.baidu.com/item/赵振峰"}
            },
            "current_status": {
                "current_post": "洛阳市政协副主席", "current_org": "洛阳市政协",
                "administrative_rank": "地厅级副职", "as_of": AS_OF, "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "2021-08", "end": "2022-01", "org": "汝阳县人民政府", "title": "县长", "level": "县处级正职", "location": "汝阳县", "system": "government", "rank": "县处级正职", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2022-01", "end": "2023", "org": "中共汝阳县委员会", "title": "县委书记", "level": "县处级正职", "location": "汝阳县", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2022-01-29全县干部大会宣布任县委书记", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2024-02", "end": "present", "org": "洛阳市政协", "title": "党组成员、副主席", "level": "地厅级副职", "location": "洛阳市", "system": "other", "rank": "地厅级副职", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [
                {"name": "洛阳市政协", "role": "副主席", "period": "2024-02至今", "source_ids": ["S001"]},
                {"name": "中共汝阳县委员会", "role": "县委书记", "period": "2022-2023", "source_ids": ["S001"]},
                {"name": "汝阳县人民政府", "role": "县长", "period": "2021-2022", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "赵书政", "person_id": "henan_ruyang_zhaoshuzheng", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "赵振峰任县委书记,赵书政2026接任", "overlap_org": "中共汝阳县委员会", "overlap_period": "2022-2026", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "姬素娟", "person_id": "henan_ruyang_jisujuan", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "赵振峰任书记时姬任县长", "overlap_org": "汝阳县", "overlap_period": "2022-2023", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [], "secondary_specializations": [], "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"], "geographic_pattern": ["偃师", "汝阳县", "洛阳市"],
                "promotion_velocity": {"summary": "汝阳县长→县委书记→洛阳政协副主席,由县到市", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "work style is inferred from public records, not a psychological assessment."},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
            "source_register": [
                {"id": "S001", "title": "百度百科「赵振峰」", "url": "https://baike.baidu.com/item/赵振峰", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "现任洛阳市政协副主席;曾任汝阳县委书记"}
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "赵振峰2013年前在偃师等地的早期履历及具体任职时间分段待查"},
            "open_questions": [
                {"priority": "medium", "question": "赵振峰 2020 年前在偃师的基层经历与洛阳市内的任职轨迹?", "why_it_matters": "还原其晋升路径", "suggested_queries": ["赵振峰 偃师 简历 任职"], "last_attempted": AS_OF}
            ]
        }
    },
]

# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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

    # Write person JSON files (staging)
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    print(f"\n✅ Done — {SLUG} staging build complete.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print("   Promote with: python3 scripts/process_tmp.py data/tmp/henan_汝阳县 --apply")


if __name__ == "__main__":
    main()