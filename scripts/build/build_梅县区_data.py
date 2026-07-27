#!/usr/bin/env python3
"""
梅州市梅县区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 梅州市
Region: 梅县区
Targets: 区委书记 & 区长

Research Notes (as of 2026-07-22):
- Web access severely degraded: meizhou.gov.cn returns Cloudflare 521,
  meixian.gov.cn times out, Baidu Baike returns 403, Exa API rate-limited,
  Wikipedia blocked, Jina Reader times out, Google/Bing/DuckDuckGo all blocked
  or timing out.
- Leadership data below is compiled from pre-2025 training data knowledge.
  All data should be verified against official sources when web access is restored.
- The current 区委书记 (温助民) was previously the 区长 and succeeded 吴泽桐 ~2021.
- The current 区长 (王锋) succeeded 温助民 around 2021 when 温助民 was promoted.
- 吴泽桐 (former 区委书记) went on to become 云浮常务副市长 then 珠海市长.

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──
SLUG = "梅县区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")


# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "温助民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "中共梅州市梅县区委书记",
        "current_org": "中共梅州市梅县区委员会",
        "source": "Training data knowledge (pre-2025). Appointed区委书记 ~2021, previously served as 梅县区区长. Requires verification against official sources."
    },
    {
        "id": 2,
        "name": "王锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅县区区长",
        "current_org": "梅县区人民政府",
        "source": "Training data knowledge (pre-2025). Appointed 区长 ~2021, previously served as deputy/district leader. Requires verification."
    },
    # ════════════════════════════════════════
    # 区委其他领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张小兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅县区委副书记",
        "current_org": "中共梅州市梅县区委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 4,
        "name": "冯振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅县区委常委、区纪委书记、区监委主任",
        "current_org": "中共梅州市梅县区纪律检查委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 5,
        "name": "吕瑜泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅县区委常委、组织部部长",
        "current_org": "中共梅州市梅县区委组织部",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 6,
        "name": "赖启忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅县区委常委、常务副区长",
        "current_org": "梅县区人民政府",
        "source": "Training data knowledge. Requires verification."
    },
    # ════════════════════════════════════════
    # 区人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "曾庆辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅县区人大常委会主任",
        "current_org": "梅县区人民代表大会常务委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 8,
        "name": "罗时亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅县区政协主席",
        "current_org": "政协梅州市梅县区委员会",
        "source": "Training data knowledge. Requires verification."
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "吴泽桐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "广东汕头（籍贯海南定安）",
        "native_place": "海南定安",
        "education": "华南理工大学管理学学士、法学学士、管理学硕士；美国匹兹堡州立大学MBA",
        "party_join": "中共党员",
        "work_start": "2002年",
        "current_post": "珠海市市长（现任）",
        "current_org": "珠海市人民政府",
        "source": "wikipedia;media_reports. Confirmed by build_珠海市_data.py and data/persons/20260722-广东省-珠海市-市长-吴泽桐.json"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共梅州市梅县区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共梅州市委",
        "location": "广东省梅州市梅县区"
    },
    {
        "id": 2,
        "name": "梅县区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "梅州市人民政府",
        "location": "广东省梅州市梅县区"
    },
    {
        "id": 3,
        "name": "中共梅州市梅县区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共梅州市纪委",
        "location": "广东省梅州市梅县区"
    },
    {
        "id": 4,
        "name": "梅县区监察委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "梅县区人民代表大会",
        "location": "广东省梅州市梅县区"
    },
    {
        "id": 5,
        "name": "中共梅州市梅县区委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共梅州市梅县区委员会",
        "location": "广东省梅州市梅县区"
    },
    {
        "id": 6,
        "name": "梅县区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "梅州市人民代表大会常务委员会",
        "location": "广东省梅州市梅县区"
    },
    {
        "id": 7,
        "name": "政协梅州市梅县区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协梅州市委员会",
        "location": "广东省梅州市梅县区"
    },
    # 前任领导关联单位
    {
        "id": 8,
        "name": "珠海市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "广东省珠海市"
    },
    {
        "id": 9,
        "name": "云浮市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "广东省云浮市"
    },
]

# 3. Positions
positions = [
    # 温助民 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "梅县区委书记", "start_date": "~2021", "end_date": "现在", "rank": "县处级", "note": "接替吴泽桐任梅县区委书记。此前任梅县区区长，具体任职起止时间待查。"},
    {"person_id": 1, "org_id": 2, "title": "梅县区区长（原任）", "start_date": "不详", "end_date": "~2021", "rank": "县处级", "note": "温助民在升任区委书记前曾任梅县区区长"},

    # 王锋 — 区长
    {"person_id": 2, "org_id": 2, "title": "梅县区区长", "start_date": "~2021", "end_date": "现在", "rank": "县处级", "note": "接替温助民任梅县区区长"},
    {"person_id": 2, "org_id": 1, "title": "梅县区委副书记", "start_date": "~2021", "end_date": "现在", "rank": "县处级", "note": "兼任区委副书记"},

    # 张小兰 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "梅县区委副书记", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 冯振 — 纪委书记
    {"person_id": 4, "org_id": 3, "title": "梅县区纪委书记、区监委主任", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "梅县区委常委", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 吕瑜泉 — 组织部部长
    {"person_id": 5, "org_id": 5, "title": "梅县区委组织部部长", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "梅县区委常委", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 赖启忠 — 常务副区长
    {"person_id": 6, "org_id": 2, "title": "梅县区常务副区长", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "梅县区委常委", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 曾庆辉 — 人大主任
    {"person_id": 7, "org_id": 6, "title": "梅县区人大常委会主任", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 罗时亮 — 政协主席
    {"person_id": 8, "org_id": 7, "title": "梅县区政协主席", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 吴泽桐 — 前任区委书记
    {"person_id": 9, "org_id": 1, "title": "梅县区委书记（原任）", "start_date": "~2019", "end_date": "~2021", "rank": "县处级", "note": "吴泽桐此前任梅县区委书记，后调任云浮市委常委、常务副市长，现任珠海市长"},
    {"person_id": 9, "org_id": 8, "title": "珠海市市长（现任）", "start_date": "2025-02", "end_date": "现在", "rank": "正厅级", "note": "2024年12月任代市长，2025年2月当选市长"},
]

# 4. Relationships
relationships = [
    # 党政一把手搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共梅州市梅县区委员会/梅县区人民政府",
        "overlap_period": "~2021-至今（待确认）"
    },
    # 区委书记与区委副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与专职副书记搭档关系",
        "overlap_org": "中共梅州市梅县区委员会",
        "overlap_period": "待确认"
    },
    # 区委书记与纪委书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记上下级关系",
        "overlap_org": "中共梅州市梅县区委员会",
        "overlap_period": "待确认"
    },
    # 区长与常务副区长
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长与常务副区长搭档关系",
        "overlap_org": "梅县区人民政府",
        "overlap_period": "待确认"
    },
    # 区委书记与组织部长
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与组织部长上下级关系",
        "overlap_org": "中共梅州市梅县区委员会",
        "overlap_period": "待确认"
    },
    # 前任-继任（区委书记）
    {
        "person_a": 9,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "吴泽桐卸任梅县区委书记调任云浮，温助民接任",
        "overlap_org": "中共梅州市梅县区委员会",
        "overlap_period": "~2021"
    },
    # 区委书记原为区长时的前后任关系（温助民→王锋）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "温助民升任区委书记后，王锋接任区长",
        "overlap_org": "梅县区人民政府",
        "overlap_period": "~2021"
    },
    # 人大主任与区委书记
    {
        "person_a": 7,
        "person_b": 1,
        "type": "overlap",
        "context": "区人大常委会主任与区委书记同在区领导班子",
        "overlap_org": "梅县区",
        "overlap_period": "待确认"
    },
    # 政协主席与区委书记
    {
        "person_a": 8,
        "person_b": 1,
        "type": "overlap",
        "context": "区政协主席与区委书记同在区领导班子",
        "overlap_org": "梅县区",
        "overlap_period": "待确认"
    },
]


if __name__ == "__main__":
    # ── Output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
        overwrite=True,
    )
    print()
    print(f"=== {SLUG} 网络数据构建完成 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")
    print(f"数据库: {db}")
    print(f"GEXF: {gexf}")
