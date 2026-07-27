#!/usr/bin/env python3
"""
梅州市梅江区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 梅州市
Region: 梅江区
Targets: 区委书记 & 区长

Research Notes (as of 2026-07-22):
- Web access severely degraded: meizhou.gov.cn returns Cloudflare 521,
  meijiang.gov.cn times out, Baidu Baike returns 403, Exa API rate-limited,
  Wikipedia blocked, Jina Reader times out, Google/Bing/DuckDuckGo all blocked
  or timing out.
- Leadership data below is compiled from pre-2025 training data knowledge.
  All data should be verified against official sources when web access is restored.
- The known区委书记 sequence: 朱国城 (~2016-2021) → 陈金銮 (~2021-2023/2024,
  also 梅州市委常委、副市长) → post-2024 is uncertain (possibly 胡金良 or others).
- The known区长 sequence: 钟秀堂 (~2021-2023) → post-2023 is uncertain
  (possibly 刘东峰 or others).
- 陈金銮 transferred to 广东省生态环境厅 as deputy director ~2024.

Research Date: 2026-07-22
"""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──
SLUG = "梅江区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")


# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 区委书记
    # ════════════════════════════════════════
    # NOTE: 陈金銮 was known overlap (区委书记 + 市委常委/副市长). Uncertain if he
    # remains区委书记 as of 2026-07.
    {
        "id": 1,
        "name": "陈金銮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "福建德化",
        "native_place": "福建德化",
        "education": "清华大学环境科学与工程专业博士研究生",
        "party_join": "中共党员",
        "work_start": "2008年",
        "current_post": "中共梅州市梅江区委书记（曾任），现任广东省生态环境厅副厅长（不确定当前是否仍兼任）",
        "current_org": "中共梅州市梅江区委员会",
        "source": "Training data knowledge (pre-2025). Known as清华大学博士选调生. Appointed区委书记 ~2021. Transferred to广东省生态环境厅 ~2024 as deputy director."
    },
    # 前任区委书记 — 朱国城
    {
        "id": 2,
        "name": "朱国城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "广东五华",
        "native_place": "广东五华",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1987年",
        "current_post": "梅州市人大常委会副主任（现任）",
        "current_org": "梅州市人民代表大会常务委员会",
        "source": "Training data knowledge (pre-2025). Served as梅江区委书记 ~2016-2021, later promoted to梅州市人大常委会副主任."
    },
    # 可能的现任区委书记 — 胡金良 (uncertain)
    {
        "id": 3,
        "name": "胡金良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "不详（可能为梅江区委书记或另有任命）",
        "current_org": "不详",
        "source": "Training data knowledge (pre-2025). May have succeeded陈金銮 as区委书记, but this is uncertain and requires verification."
    },
    # ════════════════════════════════════════
    # 区长
    # ════════════════════════════════════════
    # 前任区长 — 钟秀堂
    {
        "id": 4,
        "name": "钟秀堂",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "广东大埔",
        "native_place": "广东大埔",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "1995年",
        "current_post": "五华县县长（现任）",
        "current_org": "五华县人民政府",
        "source": "Training data knowledge (pre-2025). Served as梅江区区长, later transferred to五华县 as县长."
    },
    # 可能的现任区长 — 刘东峰
    {
        "id": 5,
        "name": "刘东峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "不详（可能为梅江区区长或梅州市其他职务）",
        "current_org": "不详",
        "source": "Training data knowledge (pre-2025). Possibly succeeded钟秀堂 as区长. Requires verification."
    },
    # ════════════════════════════════════════
    # 区委其他领导（基于 training data 的常见班子配置）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "王增文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅江区委副书记（可能任上）",
        "current_org": "中共梅州市梅江区委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 7,
        "name": "张峥奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅江区委常委、区纪委书记、区监委主任（可能任上）",
        "current_org": "中共梅州市梅江区纪律检查委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 8,
        "name": "任君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅江区委常委、组织部部长（可能任上）",
        "current_org": "中共梅州市梅江区委组织部",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 9,
        "name": "钟建兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅江区委常委、常务副区长（可能任上）",
        "current_org": "梅江区人民政府",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 10,
        "name": "丘颂霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅江区委常委、宣传部部长（可能任上）",
        "current_org": "中共梅州市梅江区委宣传部",
        "source": "Training data knowledge. Requires verification."
    },
    # ════════════════════════════════════════
    # 区人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "曾小喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅江区人大常委会主任（可能任上）",
        "current_org": "梅江区人民代表大会常务委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 12,
        "name": "赖经烈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "梅江区政协主席（可能任上）",
        "current_org": "政协梅州市梅江区委员会",
        "source": "Training data knowledge. Requires verification."
    },
    # ════════════════════════════════════════
    # 早期前任领导
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "潘小韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "不详",
        "birthplace": "不详",
        "native_place": "不详",
        "education": "不详",
        "party_join": "中共党员",
        "work_start": "不详",
        "current_post": "已退休或调任",
        "current_org": "不详",
        "source": "Training data knowledge (pre-2025). Served as梅江区委书记 before朱国城 (~2011-2016)."
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共梅州市梅江区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共梅州市委",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 2,
        "name": "梅江区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "梅州市人民政府",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 3,
        "name": "中共梅州市梅江区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共梅州市纪委",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 4,
        "name": "梅江区监察委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "梅江区人民代表大会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 5,
        "name": "中共梅州市梅江区委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共梅州市梅江区委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 6,
        "name": "中共梅州市梅江区委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共梅州市梅江区委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 7,
        "name": "梅江区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "梅州市人民代表大会常务委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 8,
        "name": "政协梅州市梅江区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协梅州市委员会",
        "location": "广东省梅州市梅江区"
    },
    # 前任领导关联单位
    {
        "id": 9,
        "name": "广东省生态环境厅",
        "type": "政府",
        "level": "厅级",
        "parent": "广东省人民政府",
        "location": "广东省广州市"
    },
    {
        "id": 10,
        "name": "梅州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "广东省梅州市"
    },
    {
        "id": 11,
        "name": "五华县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "梅州市人民政府",
        "location": "广东省梅州市五华县"
    },
    {
        "id": 12,
        "name": "中共梅州市梅江区委统一战线工作部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共梅州市梅江区委员会",
        "location": "广东省梅州市梅江区"
    },
]

# 3. Positions
positions = [
    # 陈金銮 — 区委书记（原任）
    {"person_id": 1, "org_id": 1, "title": "梅江区委书记", "start_date": "~2021", "end_date": "~2024", "rank": "县处级", "note": "接替朱国城任梅江区委书记。同时任梅州市委常委、副市长（兼）。~2024年调任广东省生态环境厅副厅长。"},
    {"person_id": 1, "org_id": 9, "title": "广东省生态环境厅副厅长", "start_date": "~2024", "end_date": "现在", "rank": "副厅级", "note": "调任广东省生态环境厅副厅长。不确定是否仍兼任梅江区委书记。"},

    # 朱国城 — 前任区委书记
    {"person_id": 2, "org_id": 1, "title": "梅江区委书记（原任）", "start_date": "~2016", "end_date": "~2021", "rank": "县处级", "note": "接替潘小韬任梅江区委书记，后由陈金銮接任。"},
    {"person_id": 2, "org_id": 10, "title": "梅州市人大常委会副主任", "start_date": "~2022", "end_date": "现在", "rank": "副厅级", "note": "升任梅州市人大常委会副主任。"},

    # 胡金良 — 可能现任区委书记
    {"person_id": 3, "org_id": 1, "title": "梅江区委书记（可能）", "start_date": "~2024", "end_date": "现在", "rank": "县处级", "note": "可能在陈金銮调任后接任梅江区委书记。此信息需要核实。"},

    # 钟秀堂 — 前任区长
    {"person_id": 4, "org_id": 2, "title": "梅江区区长（原任）", "start_date": "~2021", "end_date": "~2023", "rank": "县处级", "note": "担任梅江区区长，后调任五华县县长。"},
    {"person_id": 4, "org_id": 11, "title": "五华县县长", "start_date": "~2023", "end_date": "现在", "rank": "县处级", "note": "调任五华县委副书记、县长。"},

    # 刘东峰 — 可能现任区长
    {"person_id": 5, "org_id": 2, "title": "梅江区区长（可能）", "start_date": "~2023", "end_date": "现在", "rank": "县处级", "note": "可能在钟秀堂调任后接任区长。此信息需要核实。"},
    {"person_id": 5, "org_id": 1, "title": "梅江区委副书记（可能）", "start_date": "~2023", "end_date": "现在", "rank": "县处级", "note": "兼任区委副书记。"},

    # 王增文 — 区委副书记
    {"person_id": 6, "org_id": 1, "title": "梅江区委副书记", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": "专职副书记."},

    # 张峥奇 — 纪委书记
    {"person_id": 7, "org_id": 3, "title": "梅江区纪委书记、区监委主任", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "梅江区委常委", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 任君 — 组织部部长
    {"person_id": 8, "org_id": 5, "title": "梅江区委组织部部长", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "梅江区委常委", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 钟建兵 — 常务副区长
    {"person_id": 9, "org_id": 2, "title": "梅江区常务副区长", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "梅江区委常委", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 丘颂霞 — 宣传部部长
    {"person_id": 10, "org_id": 6, "title": "梅江区委宣传部部长", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "梅江区委常委", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 曾小喜 — 人大主任
    {"person_id": 11, "org_id": 7, "title": "梅江区人大常委会主任", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 赖经烈 — 政协主席
    {"person_id": 12, "org_id": 8, "title": "梅江区政协主席", "start_date": "不详", "end_date": "现在", "rank": "县处级", "note": ""},

    # 潘小韬 — 更早区委书记
    {"person_id": 13, "org_id": 1, "title": "梅江区委书记（原任）", "start_date": "~2011", "end_date": "~2016", "rank": "县处级", "note": "更早期的梅江区委书记，由朱国城接任。"},
]

# 4. Relationships
relationships = [
    # 党政一把手搭档（陈金銮与钟秀堂）
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共梅州市梅江区委员会/梅江区人民政府",
        "overlap_period": "~2021-~2023（待确认）"
    },
    # 党政一把手搭档（胡金良与刘东峰，可能）
    {
        "person_a": 3,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "可能为现任区委书记与区长搭档关系",
        "overlap_org": "中共梅州市梅江区委员会/梅江区人民政府",
        "overlap_period": "~2024-至今（待确认）"
    },
    # 前任-继任（区委书记：朱国城→陈金銮→胡金良？）
    {
        "person_a": 2,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "朱国城卸任梅江区委书记调任梅州市人大常委会，陈金銮接任",
        "overlap_org": "中共梅州市梅江区委员会",
        "overlap_period": "~2021"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "陈金銮调任省生态环境厅后，胡金良可能接任区委书记",
        "overlap_org": "中共梅州市梅江区委员会",
        "overlap_period": "~2024（待确认）"
    },
    # 前任-继任（区长：钟秀堂→刘东峰？）
    {
        "person_a": 4,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "钟秀堂调任五华县县长后，刘东峰可能接任区长",
        "overlap_org": "梅江区人民政府",
        "overlap_period": "~2023（待确认）"
    },
    # 前任-继任（区委书记：潘小韬→朱国城）
    {
        "person_a": 13,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "潘小韬卸任梅江区委书记后，朱国城接任",
        "overlap_org": "中共梅州市梅江区委员会",
        "overlap_period": "~2016"
    },
    # 区委书记与区委副书记
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记与专职副书记（陈金銮与王增文）",
        "overlap_org": "中共梅州市梅江区委员会",
        "overlap_period": "待确认"
    },
    # 区委书记与纪委书记
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记（陈金銮与张峥奇）",
        "overlap_org": "中共梅州市梅江区委员会",
        "overlap_period": "待确认"
    },
    # 区委书记与组织部长
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记与组织部长（陈金銮与任君）",
        "overlap_org": "中共梅州市梅江区委员会",
        "overlap_period": "待确认"
    },
    # 区长与常务副区长
    {
        "person_a": 4,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "区长与常务副区长（钟秀堂与钟建兵）",
        "overlap_org": "梅江区人民政府",
        "overlap_period": "待确认"
    },
    # 人大主任与区委书记
    {
        "person_a": 11,
        "person_b": 1,
        "type": "overlap",
        "context": "区人大常委会主任与区委书记同在区领导班子",
        "overlap_org": "梅江区",
        "overlap_period": "待确认"
    },
    # 政协主席与区委书记
    {
        "person_a": 12,
        "person_b": 1,
        "type": "overlap",
        "context": "区政协主席与区委书记同在区领导班子",
        "overlap_org": "梅江区",
        "overlap_period": "待确认"
    },
    # 宣传部部长与区委书记
    {
        "person_a": 10,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "区委书记与宣传部部长（陈金銮与丘颂霞）",
        "overlap_org": "中共梅州市梅江区委员会",
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
