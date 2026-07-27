#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 遵义市汇川区 leadership network.

Data sources:
- www.zyhc.gov.cn (official government website — 遵义国家级经济技术开发区（汇川区）)
- 领导之窗 (leadership window)
- News articles from zyhc.gov.cn

Structure note: 汇川区 operates a "two brands, one team" structure with
遵义国家经济技术开发区 (Zunyi National Economic & Technological Development Zone).
The开发区党工委书记 concurrently serves as 区委书记, and the开发区管委会副主任
concurrently serves as 区长.

Information currency: 2026-07 (current as of July 2026)
"""
import sys
import sqlite3
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "汇川区"

DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

AS_OF = "2026-07-23"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # ── 区委 (District Party Committee) ──
    {
        "id": 1, "name": "徐俊峰", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共汇川区委员会",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260720_90636875.html",
    },
    {
        "id": 2, "name": "朱世斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-10", "birthplace": "", "education": "大学学历，省委党校研究生",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "汇川区人民政府",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/202107/t20210730_76387884.html",
    },
    {
        "id": 3, "name": "潘本善", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记（专职）",
        "current_org": "中共汇川区委员会",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260720_90636875.html",
    },
    {
        "id": 4, "name": "吴健", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记（专职）",
        "current_org": "中共汇川区委员会",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260720_90636875.html",
    },
    {
        "id": 5, "name": "蔡远伟", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共汇川区委员会",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260722_90648120.html",
    },
    {
        "id": 6, "name": "姚青", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共汇川区委员会",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260720_90636875.html",
    },
    # ── 区政府 (District Government) ──
    {
        "id": 7, "name": "谢庆松", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "汇川区人民政府",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/",
    },
    {
        "id": 8, "name": "王乔乔", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "汇川区人民政府",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/",
    },
    {
        "id": 9, "name": "向先涛", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "汇川区人民政府",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/",
    },
    {
        "id": 10, "name": "龚永恒", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "汇川区人民政府",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/",
    },
    {
        "id": 11, "name": "李泽贤", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "汇川区人民政府",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/",
    },
    {
        "id": 12, "name": "李波", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "汇川区人民政府",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/",
    },
    # ── 区人大 (People's Congress) ──
    {
        "id": 13, "name": "唐静", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "汇川区人民代表大会常务委员会",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260720_90636875.html",
    },
    # ── 区政协 (CPPCC) ──
    {
        "id": 14, "name": "戴拥军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协汇川区委员会",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260720_90636875.html",
    },
    # ── 遵义国家经济技术开发区 (Zunyi National ETDZ) ──
    {
        "id": 15, "name": "徐俊峰", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "遵义国家经济技术开发区党工委书记、管委会主任",
        "current_org": "遵义国家经济技术开发区党工委",
        "source": "https://www.zyhc.gov.cn/xwzx/ywtt/202607/t20260722_90648120.html",
    },
    {
        "id": 16, "name": "朱世斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-10", "birthplace": "", "education": "大学学历，省委党校研究生",
        "party_join": "", "work_start": "",
        "current_post": "遵义国家经济技术开发区党工委副书记、管委会副主任",
        "current_org": "遵义国家经济技术开发区党工委",
        "source": "https://www.zyhc.gov.cn/zwgk/jcxxgk/ldzc/202107/t20210730_76387884.html",
    },
]

# ── Organizations ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共汇川区委员会", "type": "党委", "level": "县处级", "parent": "中共遵义市委", "location": "遵义市汇川区"},
    {"id": 2, "name": "汇川区人民政府", "type": "政府", "level": "县处级", "parent": "遵义市人民政府", "location": "遵义市汇川区"},
    {"id": 3, "name": "汇川区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "遵义市人大常委会", "location": "遵义市汇川区"},
    {"id": 4, "name": "政协汇川区委员会", "type": "政协", "level": "县处级", "parent": "政协遵义市委员会", "location": "遵义市汇川区"},
    {"id": 5, "name": "汇川区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共汇川区委员会", "location": "遵义市汇川区"},
    {"id": 6, "name": "遵义国家经济技术开发区（汇川区）", "type": "开发区", "level": "国家级", "parent": "遵义市人民政府", "location": "遵义市汇川区"},
    {"id": 7, "name": "中共汇川区委组织部", "type": "党委", "level": "乡科级", "parent": "中共汇川区委员会", "location": "遵义市汇川区"},
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 徐俊峰 - 区委书记/开发区党工委书记
    {"person_id": 1, "org_id": 1, "title": "中共汇川区委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    {"person_id": 15, "org_id": 6, "title": "遵义国家经济技术开发区党工委书记、管委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任，兼任"},
    # 朱世斌 - 区长/开发区副书记
    {"person_id": 2, "org_id": 2, "title": "汇川区人民政府区长", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "中共汇川区委副书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "兼任"},
    {"person_id": 16, "org_id": 6, "title": "遵义国家经济技术开发区党工委副书记、管委会副主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任，兼任"},
    # 潘本善 - 专职副书记
    {"person_id": 3, "org_id": 1, "title": "中共汇川区委副书记（专职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 吴健 - 专职副书记
    {"person_id": 4, "org_id": 1, "title": "中共汇川区委副书记（专职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 蔡远伟 - 区委常委/开发区副主任
    {"person_id": 5, "org_id": 1, "title": "中共汇川区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 5, "org_id": 6, "title": "遵义国家经济技术开发区管委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼任"},
    # 姚青 - 组织部部长
    {"person_id": 6, "org_id": 7, "title": "中共汇川区委组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任，区委常委兼任"},
    {"person_id": 6, "org_id": 1, "title": "中共汇川区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 谢庆松 - 副区长
    {"person_id": 7, "org_id": 2, "title": "汇川区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 王乔乔 - 副区长
    {"person_id": 8, "org_id": 2, "title": "汇川区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 向先涛 - 副区长
    {"person_id": 9, "org_id": 2, "title": "汇川区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 龚永恒 - 副区长
    {"person_id": 10, "org_id": 2, "title": "汇川区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 李泽贤 - 副区长
    {"person_id": 11, "org_id": 2, "title": "汇川区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 李波 - 副区长
    {"person_id": 12, "org_id": 2, "title": "汇川区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 唐静 - 人大主任
    {"person_id": 13, "org_id": 3, "title": "汇川区人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    # 戴拥军 - 政协主席
    {"person_id": 14, "org_id": 4, "title": "政协汇川区委员会主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # 徐俊峰 ↔ 朱世斌 (书记-区长搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "徐俊峰（区委书记）与朱世斌（区长）构成书记-区长搭档，同时在开发区党工委分别担任书记和副书记", "overlap_org": "中共汇川区委员会/汇川区人民政府/遵义国家经济技术开发区", "overlap_period": ""},
    # 徐俊峰 ↔ 副书记们
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "徐俊峰（区委书记）与潘本善（专职副书记）在区委常委会共事", "overlap_org": "中共汇川区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "徐俊峰（区委书记）与吴健（专职副书记）在区委常委会共事", "overlap_org": "中共汇川区委员会", "overlap_period": ""},
    # 徐俊峰 ↔ 蔡远伟 (区委书记-区委常委/开发区副主任)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "徐俊峰（区委书记/开发区党工委书记）与蔡远伟（区委常委/开发区管委会副主任）在区委和开发区班子共事", "overlap_org": "中共汇川区委员会/遵义国家经济技术开发区", "overlap_period": ""},
    # 徐俊峰 ↔ 姚青 (书记-组织部部长)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "徐俊峰（区委书记）与姚青（组织部部长）在区委常委会共事", "overlap_org": "中共汇川区委员会", "overlap_period": ""},
    # 朱世斌 ↔ 副区长们
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "朱世斌（区长）与谢庆松（副区长）在区政府班子共事", "overlap_org": "汇川区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "朱世斌（区长）与王乔乔（副区长）在区政府班子共事", "overlap_org": "汇川区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "朱世斌（区长）与向先涛（副区长）在区政府班子共事", "overlap_org": "汇川区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "朱世斌（区长）与龚永恒（副区长）在区政府班子共事", "overlap_org": "汇川区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "朱世斌（区长）与李泽贤（副区长）在区政府班子共事", "overlap_org": "汇川区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "朱世斌（区长）与李波（副区长）在区政府班子共事", "overlap_org": "汇川区人民政府", "overlap_period": ""},
    # 徐俊峰 ↔ 唐静 (书记-人大主任)
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "徐俊峰（区委书记）与唐静（区人大常委会主任）在区四套班子共事", "overlap_org": "中共汇川区委员会/汇川区人大常委会", "overlap_period": ""},
    # 徐俊峰 ↔ 戴拥军 (书记-政协主席)
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "徐俊峰（区委书记）与戴拥军（区政协主席）在区四套班子共事", "overlap_org": "中共汇川区委员会/政协汇川区委员会", "overlap_period": ""},
    # 朱世斌 ↔ 唐静 (区长-人大主任)
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "朱世斌（区长）与唐静（区人大常委会主任）在区四套班子共事", "overlap_org": "汇川区人民政府/汇川区人大常委会", "overlap_period": ""},
    # 朱世斌 ↔ 戴拥军 (区长-政协主席)
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "朱世斌（区长）与戴拥军（区政协主席）在区四套班子共事", "overlap_org": "汇川区人民政府/政协汇川区委员会", "overlap_period": ""},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nBuild complete for {SLUG} as of {AS_OF}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
