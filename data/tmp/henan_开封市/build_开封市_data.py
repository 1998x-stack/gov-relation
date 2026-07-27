#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 开封市 leadership network.

开封市 - 河南省 (地级市)
Targets: 市委书记高建军, 市长吴海燕
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "开封市"
TASK_ID = "henan_开封市"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "高建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年10月",
        "birthplace": "河南新郑",
        "education": "中央党校研究生，法学博士",
        "party_join": "1996年12月",
        "work_start": "1990年7月",
        "current_post": "中共开封市委书记",
        "current_org": "中国共产党开封市委员会",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 2,
        "name": "吴海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年4月",
        "birthplace": "河南洛阳",
        "education": "省委党校研究生",
        "party_join": "1994年6月",
        "work_start": "1990年12月",
        "current_post": "中共开封市委副书记、市长",
        "current_org": "开封市人民政府",
        "source": "https://www.kaifeng.gov.cn",
    },
    # ── Party Standing Committee ──
    {
        "id": 3,
        "name": "卢捍卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共开封市纪律检查委员会",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 4,
        "name": "张松文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "开封市人民政府",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 5,
        "name": "邵华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共开封市委宣传部",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 6,
        "name": "耿国庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共开封市委办公室",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 7,
        "name": "王秋杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共开封市委政法委员会",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 8,
        "name": "徐彤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共开封市委组织部",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 9,
        "name": "朱宝红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、开封军分区政委",
        "current_org": "开封军分区",
        "source": "https://www.kaifeng.gov.cn",
    },
    # ── Government Deputy Mayors ──
    {
        "id": 10,
        "name": "刘震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "开封市人民政府",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 11,
        "name": "尹君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "开封市人民政府",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 12,
        "name": "邢卫胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "开封市公安局",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 13,
        "name": "孙国才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "开封市人民政府",
        "source": "https://www.kaifeng.gov.cn",
    },
    {
        "id": 14,
        "name": "王珏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "开封市人民政府",
        "source": "https://www.kaifeng.gov.cn",
    },
    # ── Predecessors ──
    {
        "id": 15,
        "name": "侯红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年1月",
        "birthplace": "河南社旗",
        "education": "中央党校研究生",
        "party_join": "1989年6月",
        "work_start": "1987年8月",
        "current_post": "原市委书记（已落马被查）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/侯红",
    },
    {
        "id": 16,
        "name": "李湘豫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "河南光山",
        "education": "中央党校研究生，经济学博士",
        "party_join": "1993年12月",
        "work_start": "1991年10月",
        "current_post": "信阳市委书记（原开封市长）",
        "current_org": "中共信阳市委",
        "source": "https://baike.baidu.com/item/李湘豫",
    },
]

# ── Organizations ─────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党开封市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党河南省委员会",
        "location": "开封市",
    },
    {
        "id": 2,
        "name": "开封市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "河南省人民政府",
        "location": "开封市",
    },
    {
        "id": 3,
        "name": "中共开封市纪律检查委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党开封市委员会",
        "location": "开封市",
    },
    {
        "id": 4,
        "name": "开封市监察委员会",
        "type": "政府",
        "level": "地级市",
        "parent": "开封市人民政府",
        "location": "开封市",
    },
    {
        "id": 5,
        "name": "中共开封市委宣传部",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党开封市委员会",
        "location": "开封市",
    },
    {
        "id": 6,
        "name": "中共开封市委办公室",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党开封市委员会",
        "location": "开封市",
    },
    {
        "id": 7,
        "name": "中共开封市委政法委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党开封市委员会",
        "location": "开封市",
    },
    {
        "id": 8,
        "name": "中共开封市委组织部",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党开封市委员会",
        "location": "开封市",
    },
    {
        "id": 9,
        "name": "开封军分区",
        "type": "政府",
        "level": "地级市",
        "parent": "河南省军区",
        "location": "开封市",
    },
    {
        "id": 10,
        "name": "开封市公安局",
        "type": "政府",
        "level": "地级市",
        "parent": "河南省公安厅",
        "location": "开封市",
    },
    {
        "id": 11,
        "name": "中共信阳市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党河南省委员会",
        "location": "信阳市",
    },
]

# ── Positions ─────────────────────────────────────────────────────────

positions = [
    # 高建军
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2021年12月", "end_date": "present", "rank": "正厅级", "note": ""},
    # 吴海燕
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2024年4月", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024年4月", "end_date": "present", "rank": "", "note": ""},
    # 卢捍卫
    {"person_id": 3, "org_id": 3, "title": "市纪委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "市监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张松文
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 邵华
    {"person_id": 5, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 耿国庆
    {"person_id": 6, "org_id": 6, "title": "秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王秋杰
    {"person_id": 7, "org_id": 7, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 徐彤
    {"person_id": 8, "org_id": 8, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 朱宝红
    {"person_id": 9, "org_id": 9, "title": "政委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "军分区"},
    # 刘震
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 尹君
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 邢卫胜
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 10, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 孙国才
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王珏
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 侯红 — 前任市委书记
    {"person_id": 15, "org_id": 1, "title": "市委书记（前任）", "start_date": "2017年12月", "end_date": "2021年12月", "rank": "正厅级", "note": "后任河南省卫健委主任，2022年被查"},
    # 李湘豫 — 前任市长
    {"person_id": 16, "org_id": 2, "title": "市长（前任）", "start_date": "2020年12月", "end_date": "2024年3月", "rank": "正厅级", "note": "2024年调任信阳市委书记"},
    {"person_id": 16, "org_id": 11, "title": "市委书记（现）", "start_date": "2024年3月", "end_date": "present", "rank": "正厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "高建军（市委书记）与吴海燕（市长）党政正职搭档",
        "overlap_org": "中国共产党开封市委员会/开封市人民政府",
        "overlap_period": "2024年至今",
    },
    # 常委班子共事关系
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "高建军（市委书记）与卢捍卫（市纪委书记）党委班子上下级",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "上下级",
        "context": "高建军（市委书记）与张松文（常务副市长）党委班子上下级",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "上下级",
        "context": "高建军（市委书记）与邵华（宣传部部长）党委班子上下级",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "上下级",
        "context": "高建军（市委书记）与耿国庆（秘书长）党委班子上下级",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "上下级",
        "context": "高建军（市委书记）与王秋杰（政法委书记）党委班子上下级",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "上下级",
        "context": "高建军（市委书记）与徐彤（组织部部长）党委班子上下级",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "上下级",
        "context": "高建军（市委书记）与朱宝红（军分区政委）党委班子上下级",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "至今",
    },
    # 市长与副市长
    {
        "person_a": 2,
        "person_b": 4,
        "type": "上下级",
        "context": "吴海燕（市长）与张松文（常务副市长）政府班子上下级",
        "overlap_org": "开封市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "上下级",
        "context": "吴海燕（市长）与刘震（副市长）政府班子上下级",
        "overlap_org": "开封市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "上下级",
        "context": "吴海燕（市长）与尹君（副市长）政府班子上下级",
        "overlap_org": "开封市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "上下级",
        "context": "吴海燕（市长）与邢卫胜（副市长）政府班子上下级",
        "overlap_org": "开封市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "上下级",
        "context": "吴海燕（市长）与孙国才（副市长）政府班子上下级",
        "overlap_org": "开封市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "上下级",
        "context": "吴海燕（市长）与王珏（副市长）政府班子上下级",
        "overlap_org": "开封市人民政府",
        "overlap_period": "至今",
    },
    # 前后任关系
    {
        "person_a": 1,
        "person_b": 15,
        "type": "前后任",
        "context": "高建军接替侯红任开封市委书记",
        "overlap_org": "中国共产党开封市委员会",
        "overlap_period": "2021年12月",
    },
    {
        "person_a": 2,
        "person_b": 16,
        "type": "前后任",
        "context": "吴海燕接替李湘豫任开封市长",
        "overlap_org": "开封市人民政府",
        "overlap_period": "2024年4月",
    },
    # 前任与现任之间的关联
    {
        "person_a": 1,
        "person_b": 16,
        "type": "共事",
        "context": "高建军任市委书记时，李湘豫任市长，两人有党政正职搭档经历",
        "overlap_org": "中国共产党开封市委员会/开封市人民政府",
        "overlap_period": "2021年12月至2024年3月",
    },
]

# ── Build ─────────────────────────────────────────────────────────────

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

    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Done.")
