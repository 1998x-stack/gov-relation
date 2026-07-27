#!/usr/bin/env python3
"""沂水县领导班子关系网络数据构建脚本。

任务ID: shandong_沂水县
地区: 山东省临沂市沂水县
级别: 县
调研日期: 2026-07-25

核心目标人物:
- 刘铭 — 沂水县委书记（2026年7月24日在临沂市政府新闻中确认现任）
- 葛龙江 — 县委副书记、县长（yishui.gov.cn 政府领导页确认，1975年2月生）
"""

from __future__ import annotations

import sys
from pathlib import Path

# 项目根目录
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── 组织 ──────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党沂水县委员会", "type": "党委", "level": "县处级", "parent": "中国共产党临沂市委员会", "location": "山东省临沂市沂水县"},
    {"id": 2, "name": "沂水县人民政府", "type": "政府", "level": "县处级", "parent": "临沂市人民政府", "location": "山东省临沂市沂水县"},
    {"id": 3, "name": "沂水县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "山东省临沂市沂水县"},
    {"id": 4, "name": "沂水县政协", "type": "政协", "level": "县处级", "parent": "", "location": "山东省临沂市沂水县"},
    {"id": 5, "name": "沂水县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中国共产党沂水县委员会", "location": "山东省临沂市沂水县"},
    {"id": 6, "name": "沂水县委组织部", "type": "党委", "level": "乡科级", "parent": "中国共产党沂水县委员会", "location": "山东省临沂市沂水县"},
    {"id": 7, "name": "沂水县委宣传部", "type": "党委", "level": "乡科级", "parent": "中国共产党沂水县委员会", "location": "山东省临沂市沂水县"},
    {"id": 8, "name": "沂水县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中国共产党沂水县委员会", "location": "山东省临沂市沂水县"},
    {"id": 9, "name": "沂水县人民法院", "type": "政法", "level": "县处级", "parent": "", "location": "山东省临沂市沂水县"},
    {"id": 10, "name": "沂水县人民检察院", "type": "政法", "level": "县处级", "parent": "", "location": "山东省临沂市沂水县"},
]

# ── 人员 ──────────────────────────────────────────────────────────
PERSONS = [
    {
        "id": 1,
        "name": "刘铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党沂水县委员会",
        "source": "http://www.linyi.gov.cn/info/4971/465749.htm",
    },
    {
        "id": 2,
        "name": "葛龙江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "沂水县人民政府",
        "source": "http://www.yishui.gov.cn/zwgk1.htm",
    },
    {
        "id": 3,
        "name": "于民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "沂水县人大常委会",
        "source": "http://www.yishui.gov.cn/info/1006/527700.htm",
    },
    {
        "id": 4,
        "name": "郭忠友",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "沂水县政协",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
    {
        "id": 5,
        "name": "王海娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沂水县人民政府",
        "source": "http://www.yishui.gov.cn/zwgk1.htm",
    },
    {
        "id": 6,
        "name": "王海滨",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沂水县人民政府",
        "source": "http://www.yishui.gov.cn/zwgk1.htm",
    },
    {
        "id": 7,
        "name": "邱照利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沂水县人民政府",
        "source": "http://www.yishui.gov.cn/zwgk1.htm",
    },
    {
        "id": 8,
        "name": "赵如江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沂水县人民政府",
        "source": "http://www.yishui.gov.cn/zwgk1.htm",
    },
    {
        "id": 9,
        "name": "李彦华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沂水县人民政府",
        "source": "http://www.yishui.gov.cn/zwgk1.htm",
    },
    {
        "id": 10,
        "name": "孙翀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沂水县人民政府",
        "source": "http://www.yishui.gov.cn/zwgk1.htm",
    },
    {
        "id": 11,
        "name": "闫从发",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "沂水县委组织部",
        "source": "http://www.yishui.gov.cn/info/1006/526230.htm",
    },
    {
        "id": 12,
        "name": "邱金山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民法院院长",
        "current_org": "沂水县人民法院",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
    {
        "id": 13,
        "name": "卢言海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民检察院检察长",
        "current_org": "沂水县人民检察院",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
    {
        "id": 14,
        "name": "郭春玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "沂水县政协",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
    {
        "id": 15,
        "name": "张希国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "沂水县政协",
        "source": "http://www.yishui.gov.cn/info/1006/527700.htm",
    },
    {
        "id": 16,
        "name": "张洪春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "沂水县政协",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
    {
        "id": 17,
        "name": "王晓娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "沂水县政协",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
    {
        "id": 18,
        "name": "徐守凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "沂水县政协",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
    {
        "id": 19,
        "name": "耿代国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协秘书长",
        "current_org": "沂水县政协",
        "source": "http://www.yishui.gov.cn/info/129380/392252.htm",
    },
]

# ── 任职记录 ─────────────────────────────────────────────────────
POSITIONS = [
    # 刘铭 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "沂水县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年7月24日公开报道确认"},
    # 葛龙江 — 县长
    {"person_id": 2, "org_id": 2, "title": "沂水县人民政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "沂水县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 于民
    {"person_id": 3, "org_id": 3, "title": "沂水县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 郭忠友
    {"person_id": 4, "org_id": 4, "title": "沂水县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 副县长们
    {"person_id": 5, "org_id": 2, "title": "沂水县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "沂水县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "沂水县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "沂水县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "沂水县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责防汛等工作"},
    {"person_id": 10, "org_id": 2, "title": "沂水县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 闫从发
    {"person_id": 11, "org_id": 6, "title": "沂水县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 邱金山
    {"person_id": 12, "org_id": 9, "title": "沂水县人民法院院长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 卢言海
    {"person_id": 13, "org_id": 10, "title": "沂水县人民检察院检察长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 政协
    {"person_id": 14, "org_id": 4, "title": "沂水县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "沂水县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "沂水县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "沂水县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "沂水县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "沂水县政协秘书长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── 关系 ──────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 书记—县长 搭档关系
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "县委书记—县长工作搭档", "overlap_org": "中国共产党沂水县委员会/沂水县人民政府", "overlap_period": "2026"},
    # 书记—人大主任
    {"person_a": 1, "person_b": 3, "type": "党政军", "context": "县委—人大关系", "overlap_org": "中国共产党沂水县委员会", "overlap_period": "2026"},
    # 书记—政协主席
    {"person_a": 1, "person_b": 4, "type": "党政军", "context": "县委—政协关系", "overlap_org": "中国共产党沂水县委员会", "overlap_period": "2026"},
    # 县长—副县长们
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—副县长", "overlap_org": "沂水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "沂水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "沂水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长", "overlap_org": "沂水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长", "overlap_org": "沂水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "沂水县人民政府", "overlap_period": "2026"},
    # 书记—组织部长
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "县委书记—组织部部长（干部管理关系）", "overlap_org": "中国共产党沂水县委员会", "overlap_period": "2026"},
    # 政协主席—副主席们
    {"person_a": 4, "person_b": 14, "type": "上下级", "context": "政协主席—副主席", "overlap_org": "沂水县政协", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 15, "type": "上下级", "context": "政协主席—副主席", "overlap_org": "沂水县政协", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 16, "type": "上下级", "context": "政协主席—副主席", "overlap_org": "沂水县政协", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 17, "type": "上下级", "context": "政协主席—副主席", "overlap_org": "沂水县政协", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 18, "type": "上下级", "context": "政协主席—副主席", "overlap_org": "沂水县政协", "overlap_period": "2026"},
]


def main() -> None:
    staging = Path(__file__).parent
    db_path = staging / "沂水县_network.db"
    gexf_path = staging / "沂水县_network.gexf"

    run_build(
        slug="沂水县领导班子关系网络",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print("Done — 沂水县数据构建完成。")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")


if __name__ == "__main__":
    main()
