#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 锡林郭勒盟 leadership network.

锡林郭勒盟 (Xilingol League) is a prefecture-level league in 内蒙古自治区.

Data sources:
- 锡林郭勒盟行政公署官网 (www.xlgl.gov.cn) search results, accessed 2026-07-25
- 百度百科人物条目

As-of date: 2026-07-25
"""

import os
import sqlite3
import sys

# Calculate BASE: scripts/build/build_*.py -> repo root
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)

from gov_relation.runner import run_build

# Tokens required by process_tmp.py validation
DB_PATH = "data/database/锡林郭勒盟_network.db"
GEXF_PATH = "data/graph/锡林郭勒盟_network.gexf"

AS_OF = "2026-07-25"
SLUG = "锡林郭勒盟"

# ── PERSONS ──────────────────────────────────────────────────────────

persons = [
    # ===== 盟委领导 =====
    # 1. 盟委书记（一把手）
    {
        "id": 1,
        "name": "张佰成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-11",
        "birthplace": "黑龙江肇东",
        "education": "哈尔滨工程大学水声工程专业研究生学历，工学硕士",
        "party_join": "2002-11",
        "work_start": "1998-08",
        "current_post": "内蒙古自治区政协副主席、锡林郭勒盟盟委书记",
        "current_org": "中共锡林郭勒盟委员会",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E4%BD%B0%E6%88%90",
    },
    # 2. 盟长（二把手）
    {
        "id": 2,
        "name": "郭玉峰",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1970-01",
        "birthplace": "",
        "education": "大学学历，文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "锡林郭勒盟盟委副书记、行署党组书记、盟长",
        "current_org": "锡林郭勒盟行政公署",
        "source": "https://www.xlgl.gov.cn/",
    },
    # 3. 盟委委员、秘书长
    {
        "id": 3,
        "name": "杨立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盟委委员、秘书长",
        "current_org": "中共锡林郭勒盟委员会办公室",
        "source": "https://www.xlgl.gov.cn/",
    },
    # 4. 副盟长（从新闻报道中识别）
    {
        "id": 4,
        "name": "张怡",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "行署副盟长",
        "current_org": "锡林郭勒盟行政公署",
        "source": "https://www.xlgl.gov.cn/",
    },
    # 5. 副盟长
    {
        "id": 5,
        "name": "兴安",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "行署副盟长",
        "current_org": "锡林郭勒盟行政公署",
        "source": "https://www.xlgl.gov.cn/",
    },
    # 6. 盟委委员、政法委书记（待确认）
    {
        "id": 6,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盟委委员、政法委书记（待确认）",
        "current_org": "中共锡林郭勒盟委员会政法委员会",
        "source": "",
    },
    # 7. 盟委委员、组织部部长（待确认）
    {
        "id": 7,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盟委委员、组织部部长（待确认）",
        "current_org": "中共锡林郭勒盟委员会组织部",
        "source": "",
    },
    # 8. 盟委委员、宣传部部长（待确认）
    {
        "id": 8,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盟委委员、宣传部部长（待确认）",
        "current_org": "中共锡林郭勒盟委员会宣传部",
        "source": "",
    },
    # 9. 盟委委员、纪委书记、监委主任（待确认）
    {
        "id": 9,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盟委委员、纪委书记、监委主任（待确认）",
        "current_org": "中共锡林郭勒盟纪律检查委员会",
        "source": "",
    },
    # 10. 盟委委员、统战部部长（待确认）
    {
        "id": 10,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盟委委员、统战部部长（待确认）",
        "current_org": "中共锡林郭勒盟委员会统战部",
        "source": "",
    },
    # 11. 副盟长、公安局局长（待确认）
    {
        "id": 11,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "行署副盟长、公安局局长（待确认）",
        "current_org": "锡林郭勒盟公安局",
        "source": "",
    },
    # 12. 盟委委员、锡林浩特市委书记
    {
        "id": 12,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盟委委员、锡林浩特市委书记（待确认）",
        "current_org": "中共锡林浩特市委员会",
        "source": "",
    },

    # ===== 前任领导 =====
    # 13. 前任盟委书记
    {
        "id": 13,
        "name": "么永波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锡林郭勒盟盟委书记",
        "current_org": "未知（已离任）",
        "source": "https://www.xlgl.gov.cn/",
    },
    # 14. 前任盟长（待确认）
    {
        "id": 14,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前锡林郭勒盟盟长（待确认）",
        "current_org": "未知（已离任）",
        "source": "",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共锡林郭勒盟委员会", "type": "党委", "level": "地厅级", "parent": "中共内蒙古自治区委员会", "location": "锡林浩特市"},
    {"id": 2, "name": "锡林郭勒盟行政公署", "type": "政府", "level": "地厅级", "parent": "内蒙古自治区人民政府", "location": "锡林浩特市"},
    {"id": 3, "name": "中共锡林郭勒盟委员会办公室", "type": "党委", "level": "县处级", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
    {"id": 4, "name": "中共锡林郭勒盟委员会政法委员会", "type": "党委", "level": "地厅级", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
    {"id": 5, "name": "中共锡林郭勒盟委员会组织部", "type": "党委", "level": "县处级", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
    {"id": 6, "name": "中共锡林郭勒盟委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
    {"id": 7, "name": "中共锡林郭勒盟纪律检查委员会", "type": "纪委", "level": "地厅级", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
    {"id": 8, "name": "中共锡林郭勒盟委员会统战部", "type": "党委", "level": "县处级", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
    {"id": 9, "name": "锡林郭勒盟公安局", "type": "政府", "level": "县处级", "parent": "锡林郭勒盟行政公署", "location": "锡林浩特市"},
    {"id": 10, "name": "中共锡林浩特市委员会", "type": "党委", "level": "县处级", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # 张佰成
    {"person_id": 1, "org_id": 1, "title": "盟委书记", "start_date": "", "end_date": "present", "rank": "副省级", "note": "同时担任内蒙古自治区政协副主席"},
    # 郭玉峰
    {"person_id": 2, "org_id": 1, "title": "盟委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "行署党组书记、盟长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 杨立
    {"person_id": 3, "org_id": 1, "title": "盟委委员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张怡
    {"person_id": 4, "org_id": 2, "title": "行署副盟长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 兴安
    {"person_id": 5, "org_id": 2, "title": "行署副盟长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 么永波（前任盟委书记）
    {"person_id": 13, "org_id": 1, "title": "前盟委书记", "start_date": "", "end_date": "2023", "rank": "副省级", "note": "2023年前后在任"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "盟委书记与盟长党政搭档关系", "overlap_org": "中共锡林郭勒盟委员会",
     "overlap_period": ""},
    # 盟委书记 ↔ 秘书长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "盟委书记与秘书长在常委会共事", "overlap_org": "中共锡林郭勒盟委员会",
     "overlap_period": ""},
    # 盟长 ↔ 副盟长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "盟长与分管副盟长在行署共事", "overlap_org": "锡林郭勒盟行政公署",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "盟长与分管副盟长在行署共事", "overlap_org": "锡林郭勒盟行政公署",
     "overlap_period": ""},
    # 前任-继任（盟委书记）
    {"person_a": 13, "person_b": 1, "type": "predecessor_successor",
     "context": "么永波为前任盟委书记，张佰成为继任", "overlap_org": "中共锡林郭勒盟委员会",
     "overlap_period": "2023 交接期"},
]


if __name__ == "__main__":
    db_path = os.path.join(BASE, "data/database/锡林郭勒盟_network.db")
    gexf_path = os.path.join(BASE, "data/graph/锡林郭勒盟_network.gexf")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )
