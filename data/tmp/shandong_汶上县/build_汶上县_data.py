#!/usr/bin/env python3
"""Build script for 汶上县 (Wenshang County, Shandong) government personnel network.

Data sourced from:
  - wenshang.gov.cn official news articles (2025-2026)
  - 汶上县第十九届人民代表大会第六次会议 records
  - 政协第十届汶上县委员会第五次会议 records
  - Various county meeting reports

Confidence: official/government website (confirmed for current roles).
Biographical details (birth, education, party_join) are unverified where noted.
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from pathlib import Path

SLUG = "汶上县"
STAGING = Path("data/tmp/shandong_汶上县")
DB_PATH = STAGING / "汶上县_network.db"
GEXF_PATH = STAGING / "汶上县_network.gexf"
CANONICAL_DB = DATABASE_DIR / "汶上县_network.db"
CANONICAL_GEXF = GRAPH_DIR / "汶上县_network.gexf"

# ============================================================
# Persons
# ============================================================
PERSONS = [
    # --- 县委 (County Party Committee) ---
    {
        "id": 1,
        "name": "李强",
        "current_post": "县委书记",
        "current_org": "中共汶上县委员会",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-07-15 article: 全县村(社区)党组织书记培训)",
    },
    {
        "id": 2,
        "name": "李家亮",
        "current_post": "县委副书记、县长",
        "current_org": "汶上县人民政府",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (multiple 2026 articles)",
    },
    {
        "id": 3,
        "name": "周传林",
        "current_post": "县委副书记",
        "current_org": "中共汶上县委员会",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-07-02, 2026-01-15 articles)",
    },
    {
        "id": 4,
        "name": "张钦国",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共汶上县委员会",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-15 人大闭幕 article, 2026-04-06 article)",
    },
    {
        "id": 5,
        "name": "乔明",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共汶上县委员会",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-07-15 article: 乔明主持培训班仪式)",
        "note": "Note: 张钦国 also listed as 组织部部长 in Jan 2026; 乔明 listed as 组织部部长 in Jul 2026 - possible change in role",
    },
    {
        "id": 6,
        "name": "赵红雨",
        "current_post": "县委常委、副县长",
        "current_org": "汶上县人民政府",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-06-12 全民健身活动, 2026-06-03 防汛督导 articles)",
    },
    {
        "id": 7,
        "name": "李红",
        "current_post": "县委常委、副县长",
        "current_org": "汶上县人民政府",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2025-11-14 消防安全, 2026-01-13 人大开幕 articles)",
    },
    {
        "id": 8,
        "name": "裴艳昌",
        "current_post": "县委常委、办公室主任",
        "current_org": "中共汶上县委员会",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-03-16 视察项目, 2025-12-31 走访慰问 articles)",
    },
    {
        "id": 9,
        "name": "周丽莎",
        "current_post": "县委常委、宣传部部长、统战部部长",
        "current_org": "中共汶上县委员会",
        "gender": "女",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
    # --- 县人大 (County People's Congress) ---
    {
        "id": 10,
        "name": "李保江",
        "current_post": "县人大常委会主任",
        "current_org": "汶上县人大常委会",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (multiple 2026 articles)",
    },
    {
        "id": 11,
        "name": "武文忠",
        "current_post": "县人大常委会副主任",
        "current_org": "汶上县人大常委会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-15 人大闭幕 article)",
    },
    {
        "id": 12,
        "name": "刘爱华",
        "current_post": "县人大常委会副主任",
        "current_org": "汶上县人大常委会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-15 人大闭幕 article)",
    },
    {
        "id": 13,
        "name": "刘峰",
        "current_post": "县人大常委会副主任",
        "current_org": "汶上县人大常委会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-15 人大闭幕 article)",
    },
    {
        "id": 14,
        "name": "李振生",
        "current_post": "县人大常委会副主任",
        "current_org": "汶上县人大常委会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-15 人大闭幕 article)",
    },
    {
        "id": 15,
        "name": "房体建",
        "current_post": "县人大常委会副主任",
        "current_org": "汶上县人大常委会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-15 人大闭幕 article)",
    },
    # --- 县政府 (County Government) ---
    {
        "id": 16,
        "name": "刘海韵",
        "current_post": "副县长",
        "current_org": "汶上县人民政府",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-06-03 防汛, 2025-11-07 招商引资 articles)",
    },
    {
        "id": 17,
        "name": "葛虎",
        "current_post": "副县长",
        "current_org": "汶上县人民政府",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-05-18 港航对接, 2025-12-31 走访 articles)",
    },
    # --- 县政协 (County PPCC) ---
    {
        "id": 18,
        "name": "张德平",
        "current_post": "县政协主席",
        "current_org": "政协汶上县委员会",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "source": "wenshang.gov.cn (multiple 2026 articles)",
    },
    {
        "id": 19,
        "name": "姬广乐",
        "current_post": "县政协副主席",
        "current_org": "政协汶上县委员会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
    {
        "id": 20,
        "name": "李春生",
        "current_post": "县政协副主席",
        "current_org": "政协汶上县委员会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
    {
        "id": 21,
        "name": "赵娟",
        "current_post": "县政协副主席",
        "current_org": "政协汶上县委员会",
        "gender": "女",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
    {
        "id": 22,
        "name": "张明鲁",
        "current_post": "县政协副主席",
        "current_org": "政协汶上县委员会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
    {
        "id": 23,
        "name": "苏祥群",
        "current_post": "县政协副主席",
        "current_org": "政协汶上县委员会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
    {
        "id": 24,
        "name": "王春芳",
        "current_post": "县政协副主席",
        "current_org": "政协汶上县委员会",
        "gender": "女",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
    {
        "id": 25,
        "name": "马洪联",
        "current_post": "县政协秘书长",
        "current_org": "政协汶上县委员会",
        "gender": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "source": "wenshang.gov.cn (2026-01-14 政协闭幕 article)",
    },
]

# ============================================================
# Organizations
# ============================================================
ORGANIZATIONS = [
    {"id": 1, "name": "中共汶上县委员会", "type": "党委", "level": "县处级", "parent": "中共济宁市委", "location": "汶上县"},
    {"id": 2, "name": "汶上县人民政府", "type": "政府", "level": "县处级", "parent": "济宁市人民政府", "location": "汶上县"},
    {"id": 3, "name": "汶上县人大常委会", "type": "人大", "level": "县处级", "parent": "济宁市人大常委会", "location": "汶上县"},
    {"id": 4, "name": "政协汶上县委员会", "type": "政协", "level": "县处级", "parent": "政协济宁市委员会", "location": "汶上县"},
    {"id": 5, "name": "中共汶上县纪律检查委员会", "type": "纪律检查", "level": "县处级", "parent": "中共济宁市纪律检查委员会", "location": "汶上县"},
    {"id": 6, "name": "汶上县人民法院", "type": "政法", "level": "县处级", "parent": "济宁市人民法院", "location": "汶上县"},
    {"id": 7, "name": "汶上县人民检察院", "type": "政法", "level": "县处级", "parent": "济宁市人民检察院", "location": "汶上县"},
]

# ============================================================
# Positions
# ============================================================
POSITIONS = [
    # 李强
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "Confirmed as of 2026-07-15"},
    # 李家亮
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Deputy Party Secretary"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "County Mayor, confirmed as of 2026-07"},
    # 周传林
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Confirmed as of 2026-07"},
    # 张钦国
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "Position held as of Jan 2026; role may have been transitioned to 乔明 by Jul 2026"},
    # 赵红雨
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Confirmed as of 2026-06"},
    # 李红
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Confirmed as of 2025-11"},
    # 裴艳昌
    {"person_id": 8, "org_id": 1, "title": "县委常委、办公室主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Confirmed as of 2026-03"},
    # 周丽莎
    {"person_id": 9, "org_id": 1, "title": "县委常委、宣传部部长、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Confirmed as of 2026-01; also serves as 县政协党组副书记"},
    # 李保江
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "Confirmed as of 2026-01"},
    # 人大副主任
    {"person_id": 11, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘海韵
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Confirmed as of 2026-06"},
    # 葛虎
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Confirmed as of 2026-05"},
    # 政协
    {"person_id": 18, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "Confirmed as of 2026-01"},
    {"person_id": 19, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "县政协秘书长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ============================================================
# Relationships (working overlaps confirmed through news articles)
# ============================================================
RELATIONSHIPS = [
    # Leadership team working relationships
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长，汶上县党政主要领导工作搭档", "overlap_org": "汶上县", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委副书记，共同出席多次县委会议", "overlap_org": "中共汶上县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记与县人大常委会主任，共同出席人大会议", "overlap_org": "汶上县", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "县委书记与县政协主席，共同出席政协会议", "overlap_org": "汶上县", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记，党政班子领导成员", "overlap_org": "中共汶上县委员会", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长在人大会议上作政府工作报告", "overlap_org": "汶上县", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "县长与政协主席共同出席会议", "overlap_org": "汶上县", "overlap_period": "2025-2026"},
    # 县委常委 relationships
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县委常委/组织部长张钦国", "overlap_org": "中共汶上县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与县委常委/副县长赵红雨", "overlap_org": "中共汶上县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与县委常委/副县长李红", "overlap_org": "中共汶上县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与县委常委/办公室主任裴艳昌", "overlap_org": "中共汶上县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记与县委常委/宣传部部长周丽莎", "overlap_org": "中共汶上县委员会", "overlap_period": "2026"},
    # 县长 with deputies
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长与县委常委/副县长赵红雨，共同参加防汛督导", "overlap_org": "汶上县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长与县委常委/副县长李红", "overlap_org": "汶上县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县长与副县长刘海韵共同参加活动", "overlap_org": "汶上县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "县长与副县长葛虎共同参加走访活动", "overlap_org": "汶上县人民政府", "overlap_period": "2025-2026"},
    # PMO relationships between deputies
    {"person_a": 6, "person_b": 16, "type": "overlap", "context": "县委常委/副县长赵红雨与副县长刘海韵共同参加防汛督导", "overlap_org": "汶上县人民政府", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 17, "type": "overlap", "context": "县委常委/副县长李红与副县长葛虎共同参加走访", "overlap_org": "汶上县人民政府", "overlap_period": "2025-2026"},
    # 人大内部
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "县人大主任与副主任", "overlap_org": "汶上县人大常委会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 12, "type": "overlap", "context": "县人大主任与副主任", "overlap_org": "汶上县人大常委会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 13, "type": "overlap", "context": "县人大主任与副主任", "overlap_org": "汶上县人大常委会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 14, "type": "overlap", "context": "县人大主任与副主任", "overlap_org": "汶上县人大常委会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 15, "type": "overlap", "context": "县人大主任与副主任", "overlap_org": "汶上县人大常委会", "overlap_period": "2026"},
    # 政协内部
    {"person_a": 18, "person_b": 19, "type": "overlap", "context": "县政协主席与副主席", "overlap_org": "政协汶上县委员会", "overlap_period": "2026"},
    {"person_a": 18, "person_b": 20, "type": "overlap", "context": "县政协主席与副主席", "overlap_org": "政协汶上县委员会", "overlap_period": "2026"},
    {"person_a": 18, "person_b": 21, "type": "overlap", "context": "县政协主席与副主席", "overlap_org": "政协汶上县委员会", "overlap_period": "2026"},
    {"person_a": 18, "person_b": 22, "type": "overlap", "context": "县政协主席与副主席", "overlap_org": "政协汶上县委员会", "overlap_period": "2026"},
    {"person_a": 18, "person_b": 23, "type": "overlap", "context": "县政协主席与副主席", "overlap_org": "政协汶上县委员会", "overlap_period": "2026"},
    {"person_a": 18, "person_b": 24, "type": "overlap", "context": "县政协主席与副主席", "overlap_org": "政协汶上县委员会", "overlap_period": "2026"},
    {"person_a": 18, "person_b": 25, "type": "overlap", "context": "县政协主席与秘书长", "overlap_org": "政协汶上县委员会", "overlap_period": "2026"},
    # 党政 cross links
    {"person_a": 3, "person_b": 18, "type": "overlap", "context": "县委副书记与政协主席共同参加县委中心组学习", "overlap_org": "中共汶上县委员会", "overlap_period": "2025-2026"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "组织部长与宣传部长同为县委常委", "overlap_org": "中共汶上县委员会", "overlap_period": "2026"},
]


# ============================================================
# Main
# ============================================================
def main():
    for db_path, gexf_path in [(DB_PATH, GEXF_PATH)]:
        run_build(
            slug=SLUG,
            persons=PERSONS,
            organizations=ORGANIZATIONS,
            positions=POSITIONS,
            relationships=RELATIONSHIPS,
            db_path=db_path,
            gexf_path=gexf_path,
            overwrite=True,
        )
    print("Done. To promote: python3 scripts/process_tmp.py data/tmp/shandong_汶上县 --apply")


if __name__ == "__main__":
    main()
