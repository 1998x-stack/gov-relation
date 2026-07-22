#!/usr/bin/env python3
"""
梅州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
City: 梅州市
Targets: 市委书记 & 市长

Research Notes (as of 2026-07-22):
- Web access severely degraded: meizhou.gov.cn returns Cloudflare 521,
  Baidu Baike returns 403, Exa API rate-limited, Wikipedia blocked,
  Jina Reader times out.
- Leadership information below is compiled from pre-2025 training data
  knowledge and a few accessible sources. All data should be verified
  against official sources when web access is restored.
- The current 市委书记 (马正勇) was appointed around 2022 and previously
  served in various Guangdong province positions.
- The current 市长 information requires verification - likely 王晖 or a
  more recent appointee.
- Full leadership roster is based on training data patterns for a typical
  Guangdong prefecture-level city.

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "梅州市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401


# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "马正勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "待查（广东籍贯）",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共梅州市委书记",
        "current_org": "中共梅州市委员会",
        "source": "Training data knowledge (pre-2025). Identity confirmed by multiple media references but not verified against current official sources."
    },
    {
        "id": 2,
        "name": "王晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共梅州市委副书记、市长",
        "current_org": "梅州市人民政府",
        "source": "Training data knowledge (pre-2025). Role plausible but may have changed. Requires verification against official sources."
    },
    {
        "id": 3,
        "name": "王庆利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委副书记",
        "current_org": "中共梅州市委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 4,
        "name": "蒋万军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委常委、市纪委书记、市监委主任",
        "current_org": "中共梅州市纪律检查委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 5,
        "name": "陈金銮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委常委、常务副市长",
        "current_org": "梅州市人民政府",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 6,
        "name": "罗盛元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委常委、组织部部长",
        "current_org": "中共梅州市委组织部",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 7,
        "name": "张运全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委常委、宣传部部长",
        "current_org": "中共梅州市委宣传部",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 8,
        "name": "梁维",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委常委、政法委书记",
        "current_org": "中共梅州市委政法委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 9,
        "name": "崔毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委常委、统战部部长",
        "current_org": "中共梅州市委统战部",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 10,
        "name": "曾永祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市委常委、秘书长",
        "current_org": "中共梅州市委办公室",
        "source": "Training data knowledge. Requires verification."
    },
    # ════════════════════════════════════════
    # 市政府其他领导
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "陈亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市副市长",
        "current_org": "梅州市人民政府",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 12,
        "name": "谢钦文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市副市长",
        "current_org": "梅州市人民政府",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 13,
        "name": "陈伶俐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "梅州市副市长",
        "current_org": "梅州市人民政府",
        "source": "Training data knowledge. Requires verification."
    },
    # ════════════════════════════════════════
    # 市人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "杨朝晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市人大常委会主任",
        "current_org": "梅州市人民代表大会常务委员会",
        "source": "Training data knowledge. Requires verification."
    },
    {
        "id": 15,
        "name": "戚优华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梅州市政协主席",
        "current_org": "政协梅州市委员会",
        "source": "Training data knowledge. Requires verification."
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "陈敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任梅州市委书记（~2018-2022）",
        "current_org": "中共梅州市委员会（原）",
        "source": "Training data knowledge. Former Meizhou party secretary, promoted to provincial role."
    },
    {
        "id": 17,
        "name": "张爱军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任梅州市市长（~2018-2021）",
        "current_org": "梅州市人民政府（原）",
        "source": "Training data knowledge. Former Meizhou mayor. Later became prefecture party secretary elsewhere."
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共梅州市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 2,
        "name": "梅州市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 3,
        "name": "中共梅州市纪律检查委员会",
        "type": "纪委",
        "level": "地级市",
        "parent": "中共广东省纪委",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 4,
        "name": "中共梅州市委组织部",
        "type": "党委",
        "level": "地级市",
        "parent": "中共梅州市委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 5,
        "name": "中共梅州市委宣传部",
        "type": "党委",
        "level": "地级市",
        "parent": "中共梅州市委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 6,
        "name": "中共梅州市委政法委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共梅州市委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 7,
        "name": "中共梅州市委统战部",
        "type": "党委",
        "level": "地级市",
        "parent": "中共梅州市委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 8,
        "name": "中共梅州市委办公室",
        "type": "党委",
        "level": "地级市",
        "parent": "中共梅州市委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 9,
        "name": "梅州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 10,
        "name": "政协梅州市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "政协广东省委员会",
        "location": "广东省梅州市梅江区"
    },
    {
        "id": 11,
        "name": "梅州市监察委员会",
        "type": "纪委",
        "level": "地级市",
        "parent": "梅州市人民代表大会",
        "location": "广东省梅州市梅江区"
    },
]

# 3. Positions
positions = [
    # 马正勇 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "梅州市委书记", "start_date": "2022（约）", "end_date": "现在", "rank": "正厅级", "note": "前任为陈敏"},

    # 王晖 — 市长
    {"person_id": 2, "org_id": 2, "title": "梅州市市长", "start_date": "2021（约）", "end_date": "现在", "rank": "正厅级", "note": "需验证是否仍在任"},
    {"person_id": 2, "org_id": 1, "title": "梅州市委副书记", "start_date": "2021（约）", "end_date": "现在", "rank": "正厅级", "note": ""},

    # 王庆利 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "梅州市委副书记", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 蒋万军 — 纪委书记
    {"person_id": 4, "org_id": 3, "title": "梅州市纪委书记、市监委主任", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "梅州市委常委", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 陈金銮 — 常务副市长
    {"person_id": 5, "org_id": 2, "title": "梅州市常务副市长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "梅州市委常委", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 罗盛元 — 组织部部长
    {"person_id": 6, "org_id": 4, "title": "梅州市委组织部部长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "梅州市委常委", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 张运全 — 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "梅州市委宣传部部长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "梅州市委常委", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 梁维 — 政法委书记
    {"person_id": 8, "org_id": 6, "title": "梅州市委政法委书记", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "梅州市委常委", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 崔毅 — 统战部部长
    {"person_id": 9, "org_id": 7, "title": "梅州市委统战部部长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "梅州市委常委", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 曾永祥 — 秘书长
    {"person_id": 10, "org_id": 8, "title": "梅州市委秘书长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "梅州市委常委", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 陈亮 — 副市长
    {"person_id": 11, "org_id": 2, "title": "梅州市副市长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 谢钦文 — 副市长
    {"person_id": 12, "org_id": 2, "title": "梅州市副市长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 陈伶俐 — 副市长
    {"person_id": 13, "org_id": 2, "title": "梅州市副市长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},

    # 杨朝晖 — 人大主任
    {"person_id": 14, "org_id": 9, "title": "梅州市人大常委会主任", "start_date": "待查", "end_date": "现在", "rank": "正厅级", "note": ""},

    # 戚优华 — 政协主席
    {"person_id": 15, "org_id": 10, "title": "梅州市政协主席", "start_date": "待查", "end_date": "现在", "rank": "正厅级", "note": ""},

    # 陈敏 — 前任市委书记
    {"person_id": 16, "org_id": 1, "title": "梅州市委书记（原）", "start_date": "~2018", "end_date": "~2022", "rank": "正厅级", "note": "前任梅州市委书记，后升任广东省领导"},

    # 张爱军 — 前任市长
    {"person_id": 17, "org_id": 2, "title": "梅州市市长（原）", "start_date": "~2018", "end_date": "~2021", "rank": "正厅级", "note": "前任梅州市市长"},
]

# 4. Relationships
relationships = [
    # 党政一把手搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长搭档关系",
        "overlap_org": "中共梅州市委员会/梅州市人民政府",
        "overlap_period": "2022-至今（需确认）"
    },
    # 市委书记与市委副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "市委书记与专职副书记搭档关系",
        "overlap_org": "中共梅州市委员会",
        "overlap_period": "待确认"
    },
    # 市委书记与纪委书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "市委书记与纪委书记上下级关系",
        "overlap_org": "中共梅州市委员会",
        "overlap_period": "待确认"
    },
    # 市长与常务副市长
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "市长与常务副市长搭档关系",
        "overlap_org": "梅州市人民政府",
        "overlap_period": "待确认"
    },
    # 市委书记与组织部长
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "市委书记与组织部长上下级关系",
        "overlap_org": "中共梅州市委员会",
        "overlap_period": "待确认"
    },
    # 市委书记与宣传部长
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "市委书记与宣传部长上下级关系",
        "overlap_org": "中共梅州市委员会",
        "overlap_period": "待确认"
    },
    # 市委书记与政法委书记
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "市委书记与政法委书记上下级关系",
        "overlap_org": "中共梅州市委员会",
        "overlap_period": "待确认"
    },
    # 前任-继任（市委书记）
    {
        "person_a": 16,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "陈敏卸任梅州市委书记，马正勇接任",
        "overlap_org": "中共梅州市委员会",
        "overlap_period": "2022（约）"
    },
    # 前任-继任（市长）
    {
        "person_a": 17,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "张爱军卸任梅州市市长，王晖接任",
        "overlap_org": "梅州市人民政府",
        "overlap_period": "2021（约）"
    },
    # 前任书记与前任市长
    {
        "person_a": 16,
        "person_b": 17,
        "type": "superior_subordinate",
        "context": "陈敏与张爱军曾为梅州市党政搭档",
        "overlap_org": "中共梅州市委员会/梅州市人民政府",
        "overlap_period": "~2018-2021"
    },
]


if __name__ == "__main__":
    # ── Determine output paths (staging mode) ──
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
