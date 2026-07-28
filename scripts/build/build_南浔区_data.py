#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Nanxun District (南浔区), Huzhou, Zhejiang."""

import sys
import os
import sqlite3
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Staging paths ──────────────────────────────────────────────
BASE = Path(__file__).resolve().parents[3]
TMP = BASE / "data/tmp/zhejiang_南浔区"
DB_PATH = TMP / "南浔区_network.db"
GEXF_PATH = TMP / "南浔区_network.gexf"

# ── DATA ───────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    # ── Current Top Leaders ──
    {"id": 1, "name": "程佳", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-02", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委书记", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn/art/2025/3/3/art_1229211118_116701.html"},
    {"id": 2, "name": "杨国志", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-10", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委副书记、区长", "current_org": "湖州市南浔区人民政府",
     "source": "http://www.nanxun.gov.cn/art/2025/4/12/art_1229211119_175410.html"},

    # ── Previous Leaders ──
    {"id": 3, "name": "温建飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原南浔区委书记（前任）", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn"},

    # ── Standing Committee Members ──
    {"id": 4, "name": "张文斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-03", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委副书记", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn/art/2025/3/3/art_1229211121_119400.html"},
    {"id": 5, "name": "熊卓越", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-06", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委、常务副区长", "current_org": "湖州市南浔区人民政府",
     "source": "http://www.nanxun.gov.cn/art/2025/3/3/art_1229211127_161962.html"},
    {"id": 6, "name": "杨雪伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn"},
    {"id": 7, "name": "翟海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn"},
    {"id": 8, "name": "姚骅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn"},
    {"id": 9, "name": "钱国强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委、纪委书记", "current_org": "中共湖州市南浔区纪律检查委员会",
     "source": "http://www.nanxun.gov.cn/col/col1229211161/index.html"},
    {"id": 10, "name": "吴冠宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn"},
    {"id": 11, "name": "丁一平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn"},
    {"id": 12, "name": "韩士博", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区委常委", "current_org": "中共湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn"},

    # ── Legislative Leaders ──
    {"id": 13, "name": "陆卫良", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区人大常委会主任", "current_org": "湖州市南浔区人民代表大会常务委员会",
     "source": "http://www.nanxun.gov.cn"},
    {"id": 14, "name": "徐娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南浔区政协主席", "current_org": "中国人民政治协商会议湖州市南浔区委员会",
     "source": "http://www.nanxun.gov.cn/col/col1229211155/index.html"},
]

organizations = [
    {"id": 1, "name": "中共湖州市南浔区委员会", "type": "党委", "level": "县处级",
     "parent": "中共湖州市委员会", "location": "浙江省湖州市南浔区"},
    {"id": 2, "name": "湖州市南浔区人民政府", "type": "政府", "level": "县处级",
     "parent": "湖州市人民政府", "location": "浙江省湖州市南浔区"},
    {"id": 3, "name": "中共湖州市南浔区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共湖州市纪律检查委员会", "location": "浙江省湖州市南浔区"},
    {"id": 4, "name": "湖州市南浔区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "湖州市人大常委会", "location": "浙江省湖州市南浔区"},
    {"id": 5, "name": "中国人民政治协商会议湖州市南浔区委员会", "type": "政协", "level": "县处级",
     "parent": "湖州市政协", "location": "浙江省湖州市南浔区"},
]

positions = [
    # ── 程佳's Career ──
    {"person_id": 1, "org_id": 1, "title": "南浔区委书记", "start": "unknown", "end": "present",
     "rank": "副厅级", "note": "现任南浔区委书记。1980年2月生，研究生学历。"},
    {"person_id": 1, "org_id": 2, "title": "南浔区长", "start": "unknown", "end": "",
     "rank": "正县级", "note": "曾任南浔区长，后晋升区委书记。2025年3月官方页面仍标注'区委书记、区长：程佳'，此后职务已分开。"},

    # ── 杨国志's Career ──
    {"person_id": 2, "org_id": 2, "title": "南浔区委副书记、区长、区政府党组书记", "start": "unknown", "end": "present",
     "rank": "正县级", "note": "现任南浔区长。1980年10月生，省委党校研究生学历。"},

    # ── 温颖飞 (Predecessor Party Secretary) ──
    {"person_id": 3, "org_id": 1, "title": "南浔区委书记", "start": "unknown", "end": "2024",
     "rank": "副厅级", "note": "前任南浔区委书记。2023年5月仍有公开活动报道。"},

    # ── 张文斌 (Deputy Party Secretary) ──
    {"person_id": 4, "org_id": 1, "title": "南浔区委副书记、社工部部长、政法委书记", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "协助书记分管党建工作。1979年3月生，省委党校研究生。"},

    # ── 熊卓越 (Standing Committee / Executive Deputy Mayor) ──
    {"person_id": 5, "org_id": 2, "title": "南浔区委常委、常务副区长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "负责区政府常务工作。1988年6月生，研究生。"},

    # ── Other Standing Committee Members ──
    {"person_id": 6, "org_id": 1, "title": "南浔区委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "杨雪伟"},
    {"person_id": 7, "org_id": 1, "title": "南浔区委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "翟海峰"},
    {"person_id": 8, "org_id": 1, "title": "南浔区委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "姚骅"},
    {"person_id": 9, "org_id": 3, "title": "南浔区委常委、纪委书记", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "钱国强"},
    {"person_id": 10, "org_id": 1, "title": "南浔区委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "吴冠宇"},
    {"person_id": 11, "org_id": 1, "title": "南浔区委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "丁一平"},
    {"person_id": 12, "org_id": 1, "title": "南浔区委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "韩士博"},

    # ── Legislative Leaders ──
    {"person_id": 13, "org_id": 4, "title": "南浔区人大常委会主任", "start": "unknown", "end": "present",
     "rank": "正县级", "note": "陆卫良"},
    {"person_id": 14, "org_id": 5, "title": "南浔区政协主席", "start": "unknown", "end": "present",
     "rank": "正县级", "note": "徐娟（女）"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "程佳作为区委书记，杨国志作为区长，是党政一把手搭档关系",
     "overlap_org": "中共湖州市南浔区委员会/湖州市南浔区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "程佳接替温颖飞任南浔区委书记",
     "overlap_org": "中共湖州市南浔区委员会",
     "overlap_period": "2024", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "程佳与张文斌在区委班子共事，张文斌任区委副书记",
     "overlap_org": "中共湖州市南浔区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "程佳与熊卓越在区委区政府共事，熊卓越任常委、常务副区长",
     "overlap_org": "中共湖州市南浔区委员会/湖州市南浔区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "strength": "strong",
     "context": "程佳与钱国强在区委班子共事，钱国强任纪委书记",
     "overlap_org": "中共湖州市南浔区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "杨国志与张文斌在区委区政府共事",
     "overlap_org": "中共湖州市南浔区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "杨国志作为区长，熊卓越作为常务副区长，是政府班子搭档",
     "overlap_org": "湖州市南浔区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "程佳与杨雪伟在区委班子共事",
     "overlap_org": "中共湖州市南浔区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "medium",
     "context": "程佳与翟海峰在区委班子共事",
     "overlap_org": "中共湖州市南浔区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "程佳与姚骅在区委班子共事",
     "overlap_org": "中共湖州市南浔区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
]


# ── MAIN ─────────────────────────────────────────────────────┐

def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    # Standard build via runner (creates DB + GEXF)
    run_build(
        slug="南浔区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )

    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    main()