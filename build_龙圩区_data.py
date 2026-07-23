#!/usr/bin/env python3
"""Build script for 龙圩区 (Longxu District, Wuzhou, Guangxi) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 广西壮族自治区
Parent City: 梧州市
Targets: 区委书记 & 区长

Research Summary:
  - 区委书记: 吴情操（1985年生，北大选调生，2025年7月由区长升任）
  - 区长: 暂缺（吴情操升任书记后兼任，新区长尚未任命）
  - 前任区委书记: 赖启第（1968年生，壮族，已升梧州市政协副主席）
  - 前任区长: 吴情操（2021-2025年任区长，后升书记）
  - 常务副区长: 赵云（女，瑶族，1981年生）
  - 领导班子较为完整

Sources:
  - 腾讯新闻/澎湃新闻: 吴情操履新报道 (2025.07.20)
  - 北京大学校友网: 吴情操简历 (2021.09.22)
  - 百度百科: 赖启第词条
  - 广西纪检监察网: 巡视动员会 (2025.04.18)
  - 龙圩区政府官网领导之窗 (2023年版本)
  - 中国县域网: 龙圩区领导信息 (2023.09.15)
  - 广西县域经济网: 历次任前公示
  - 龙圩区委组织部: 干部任前公示（2025-2026年）
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "吴情操",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-12",
        "birthplace": "江西高安",
        "education": "研究生，法学硕士（北京大学社会学系）",
        "party_join": "2005-12",
        "work_start": "2011-07",
        "current_post": "龙圩区委书记（2025.07-），原区长（2021-2025）",
        "current_org": "中共梧州市龙圩区委员会",
        "source": "腾讯新闻/澎湃新闻 2025.07.20报道；北京大学校友网2021.09.22简历；广西2025年区委书记任前公示",
    },
    {
        "id": 2,
        "name": "赖启第",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1968-06",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "梧州市政协副主席（2025-），原龙圩区委书记（~2025.07）",
        "current_org": "中国人民政治协商会议梧州市委员会",
        "source": "百度百科：赖启第词条；梧州市政协官网",
    },
    {
        "id": 3,
        "name": "赵云",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1981-08",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区委常委、常务副区长",
        "current_org": "梧州市龙圩区人民政府",
        "source": "龙圩区政府官网领导之窗（2023年版本）；负责发改、教育、商务、招商、文旅等",
    },
    {
        "id": 4,
        "name": "严建洲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区委副书记（2022年已任）",
        "current_org": "中共梧州市龙圩区委员会",
        "source": "龙圩区2022年公开报道",
    },
    {
        "id": 5,
        "name": "陈宏燕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区委常委、组织部部长（2024年确认）",
        "current_org": "中共梧州市龙圩区委组织部",
        "source": "龙圩区委组织部2024年8月公开报道",
    },
    {
        "id": 6,
        "name": "董亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区委常委、政法委书记（2024年确认）",
        "current_org": "中共梧州市龙圩区委员会政法委员会",
        "source": "龙圩区2024年公开报道；前龙圩镇党委书记升任",
    },
    {
        "id": 7,
        "name": "甘忠义",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1974-08",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区委常委、副区长（兼广西驻村工作队队长）",
        "current_org": "梧州市龙圩区人民政府",
        "source": "龙圩区政府官网领导之窗",
    },
    {
        "id": 8,
        "name": "【待查】龙圩区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区委常委、纪委书记（姓名待查）",
        "current_org": "中共梧州市龙圩区纪律检查委员会",
        "source": "GAP — 成杰曾任此职（~2021年），后调任区委副书记；继任者待查",
    },
    {
        "id": 9,
        "name": "邹海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-01",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区副区长、龙圩公安分局局长",
        "current_org": "梧州市公安局龙圩分局",
        "source": "龙圩区政府官网领导之窗",
    },
    {
        "id": 10,
        "name": "杨颖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区副区长",
        "current_org": "梧州市龙圩区人民政府",
        "source": "龙圩区政府官网领导之窗；分管人社、工信、自然资源、住建、城管等",
    },
    {
        "id": 11,
        "name": "王冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-11",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区副区长",
        "current_org": "梧州市龙圩区人民政府",
        "source": "龙圩区政府官网领导之窗；分管民政、交通、卫健、退役军人、大数据等",
    },
    {
        "id": 12,
        "name": "莫振明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区副区长",
        "current_org": "梧州市龙圩区人民政府",
        "source": "龙圩区政府官网领导之窗；分管水利、农业、林业、乡村振兴等",
    },
    {
        "id": 13,
        "name": "马泽森",
        "gender": "男",
        "ethnicity": "",
        "birth": "1966-02",
        "birthplace": "广西平南",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区人大常委会主任",
        "current_org": "梧州市龙圩区人大常委会",
        "source": "龙圩区公开报道",
    },
    {
        "id": 14,
        "name": "李国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "龙圩区政协主席（2022-2026年确认在任）",
        "current_org": "政协梧州市龙圩区委员会",
        "source": "龙圩区公开报道",
    },
    {
        "id": 15,
        "name": "成杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原龙圩区委常委、纪委书记（~2021年调离）",
        "current_org": "",
        "source": "2021年梧州市领导干部任前公示；拟任县（市、区）党委副书记",
    },
    {
        "id": 16,
        "name": "于新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原龙圩区委常委、政法委书记（~2020年）",
        "current_org": "",
        "source": "龙圩区公开报道；董亮接任",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共梧州市龙圩区委员会", "type": "党委", "level": "正处级", "parent": "中共梧州市委员会", "location": "梧州市龙圩区"},
    {"id": 2, "name": "梧州市龙圩区人民政府", "type": "政府", "level": "正处级", "parent": "梧州市人民政府", "location": "梧州市龙圩区"},
    {"id": 3, "name": "中共梧州市龙圩区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共梧州市纪律检查委员会", "location": "梧州市龙圩区"},
    {"id": 4, "name": "中共梧州市龙圩区委组织部", "type": "党委", "level": "正科级", "parent": "中共梧州市龙圩区委员会", "location": "梧州市龙圩区"},
    {"id": 5, "name": "中共梧州市龙圩区委政法委员会", "type": "党委", "level": "正科级", "parent": "中共梧州市龙圩区委员会", "location": "梧州市龙圩区"},
    {"id": 6, "name": "梧州市公安局龙圩分局", "type": "政府", "level": "正科级", "parent": "梧州市公安局", "location": "梧州市龙圩区"},
    {"id": 7, "name": "梧州市龙圩区人大常委会", "type": "人大", "level": "正处级", "parent": "梧州市人大常委会", "location": "梧州市龙圩区"},
    {"id": 8, "name": "政协梧州市龙圩区委员会", "type": "政协", "level": "正处级", "parent": "政协梧州市委员会", "location": "梧州市龙圩区"},
    {"id": 9, "name": "中国人民政治协商会议梧州市委员会", "type": "政协", "level": "正厅级", "parent": "政协广西壮族自治区委员会", "location": "梧州市"},
]

POSITIONS = [
    # 吴情操 — 区委书记（2025.07-），原区长（2021-2025）
    {"person_id": 1, "org_id": 1, "title": "龙圩区委书记", "start_date": "2025-07", "end_date": "present", "rank": "正处级", "note": "2025年7月由区长升任，公示期后正式任职"},
    {"person_id": 1, "org_id": 1, "title": "龙圩区委副书记", "start_date": "2021-06", "end_date": "2025-07", "rank": "副处级", "note": "任区长期间兼任"},
    {"person_id": 1, "org_id": 2, "title": "龙圩区区长", "start_date": "2021-07", "end_date": "present", "rank": "正处级", "note": "升书记后仍兼任区长至新区长任命"},
    # 赖启第 — 原区委书记（~2025.07），今市政协副主席
    {"person_id": 2, "org_id": 1, "title": "龙圩区委书记", "start_date": "2021-07", "end_date": "2025-07", "rank": "正处级", "note": "2021年7月至2025年7月任龙圩区委书记"},
    {"person_id": 2, "org_id": 9, "title": "梧州市政协副主席", "start_date": "2025-04", "end_date": "present", "rank": "副厅级", "note": "2024年12月提名为副主席人选，2025年4月正式任职"},
    # 赵云 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "龙圩区常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管发改、教育、商务、招商、文旅、应急、统计、金融等"},
    {"person_id": 3, "org_id": 1, "title": "龙圩区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 严建洲 — 区委副书记
    {"person_id": 4, "org_id": 1, "title": "龙圩区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2022年已任"},
    # 陈宏燕 — 组织部长
    {"person_id": 5, "org_id": 4, "title": "龙圩区委组织部部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "2024年确认任职"},
    {"person_id": 5, "org_id": 1, "title": "龙圩区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 董亮 — 政法委书记
    {"person_id": 6, "org_id": 5, "title": "龙圩区委政法委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "前龙圩镇党委书记升任，2024年确认在任"},
    {"person_id": 6, "org_id": 1, "title": "龙圩区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 甘忠义 — 常委/副区长
    {"person_id": 7, "org_id": 2, "title": "龙圩区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼广西驻村工作队队长"},
    {"person_id": 7, "org_id": 1, "title": "龙圩区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 纪委书记（GAP）
    {"person_id": 8, "org_id": 3, "title": "龙圩区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名待查"},
    {"person_id": 8, "org_id": 1, "title": "龙圩区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP"},
    # 邹海 — 副区长/公安局长
    {"person_id": 9, "org_id": 6, "title": "龙圩公安分局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "龙圩区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管司法、信访、维稳"},
    # 杨颖 — 副区长
    {"person_id": 10, "org_id": 2, "title": "龙圩区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管人社、工信、自然资源、住建、城管、生态环境、征地拆迁"},
    # 王冰 — 副区长
    {"person_id": 11, "org_id": 2, "title": "龙圩区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管民政、交通、卫健、退役军人、大数据"},
    # 莫振明 — 副区长
    {"person_id": 12, "org_id": 2, "title": "龙圩区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管水利、农业、林业、乡村振兴"},
    # 马泽森 — 人大主任
    {"person_id": 13, "org_id": 7, "title": "龙圩区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "1966年生，广西平南人"},
    # 李国 — 政协主席
    {"person_id": 14, "org_id": 8, "title": "龙圩区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2022-2026年确认在任"},
    # 成杰 — 前纪委书记
    {"person_id": 15, "org_id": 3, "title": "龙圩区纪委书记（前任）", "start_date": "", "end_date": "2021", "rank": "副处级", "note": "2021年拟任县（市、区）党委副书记"},
    {"person_id": 15, "org_id": 1, "title": "龙圩区委常委（前任）", "start_date": "", "end_date": "2021", "rank": "副处级", "note": ""},
    # 于新 — 前政法委书记
    {"person_id": 16, "org_id": 5, "title": "龙圩区委政法委书记（前任）", "start_date": "", "end_date": "~2020", "rank": "正科级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "龙圩区委常委（前任）", "start_date": "", "end_date": "~2020", "rank": "副处级", "note": ""},
]

RELATIONSHIPS = [
    # 党政正职
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记-常务副区长", "overlap_org": "龙圩区委常委会", "overlap_period": "", "source": "区委常委会成员", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记-区委副书记", "overlap_org": "龙圩区委常委会", "overlap_period": "2022-2025", "source": "区委常委会成员", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记-组织部长", "overlap_org": "龙圩区委常委会", "overlap_period": "", "source": "区委常委会成员", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记-政法委书记", "overlap_org": "龙圩区委常委会", "overlap_period": "", "source": "区委常委会成员", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记-常委副区长", "overlap_org": "龙圩区委常委会", "overlap_period": "", "source": "区委常委会成员", "confidence": "confirmed"},
    # 书记-前任书记（接任关系）
    {"person_a": 1, "person_b": 2, "type": "接任", "context": "吴情操接替赖启第任龙圩区委书记", "overlap_org": "中共梧州市龙圩区委员会", "overlap_period": "2025-07", "source": "2025年区委书记调整公示", "confidence": "confirmed"},
    # 区长-前任区长（同一人，升任书记，故不重复）
    # 区长-政府班子
    {"person_a": 1, "person_b": 3, "type": "党政正职搭档", "context": "区长-常务副区长", "overlap_org": "龙圩区人民政府", "overlap_period": "2021-2025", "source": "龙圩区政府领导班子", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区长-副区长/公安局长", "overlap_org": "龙圩区人民政府", "overlap_period": "", "source": "龙圩区政府领导班子", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区长-副区长", "overlap_org": "龙圩区人民政府", "overlap_period": "", "source": "龙圩区政府领导班子", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "区长-副区长", "overlap_org": "龙圩区人民政府", "overlap_period": "", "source": "龙圩区政府领导班子", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "区长-副区长", "overlap_org": "龙圩区人民政府", "overlap_period": "", "source": "龙圩区政府领导班子", "confidence": "confirmed"},
    # 前任书记-成杰（上下级）
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "区委书记-纪委书记", "overlap_org": "龙圩区委常委会", "overlap_period": "~2021", "source": "区委常委会成员", "confidence": "confirmed"},
    # 前任书记-于新（上下级）
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "区委书记-政法委书记", "overlap_org": "龙圩区委常委会", "overlap_period": "~2020", "source": "区委常委会成员", "confidence": "confirmed"},
    # 前任前后任
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "纪委书记-政法委书记（前任班子）", "overlap_org": "龙圩区委常委会", "overlap_period": "~2020", "source": "前任区委常委会成员", "confidence": "plausible"},
    # 人大-政府
    {"person_a": 13, "person_b": 1, "type": "同级别协作", "context": "人大主任-区长/书记", "overlap_org": "龙圩区四套班子", "overlap_period": "", "source": "人大监督政府工作关系", "confidence": "plausible"},
    # 政协-政府
    {"person_a": 14, "person_b": 1, "type": "同级别协作", "context": "政协主席-区长/书记", "overlap_org": "龙圩区四套班子", "overlap_period": "", "source": "政协协商政府工作关系", "confidence": "plausible"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD (using staging dir paths)
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "龙圩区_network.db"
GEXF_PATH = STAGING_DIR / "龙圩区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="龙圩区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
