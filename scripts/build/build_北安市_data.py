#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 北安市 (Bei'an City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_北安市
Level: 县级市 (county-level city)
Parent city: 黑河市
Province: 黑龙江省
Targets: 市委书记 & 市长

Research sources:
  - 北安市政府官网 (www.hljba.gov.cn) — 市领导页面: 孟凡晶（书记/市长）, 张如东（常务副市长）等
  - 北安新闻: 孟凡晶主持召开市委常委会 (2026-07-20) — 确认孟凡晶为市委书记
  - 北安市人大常委会第四十六次会议 (2026-07-24) — 任命李海军为代市长
  - 北安市政府第8次常务会议 (2026-07-24) — 李海军以"市委副书记、副市长、代市长"身份出席

Key findings:
  - 孟凡晶: 1981年8月生，此前同时担任市委书记和市长（党政一肩挑）
  - 李海军: 2026年7月23日被任命为副市长、代市长，与孟凡晶分设
  - 市政府领导班子: 1正（代市长）+ 8副（常务副市长1+副市长7）
  - 另有市人大常委会、市政协、市纪委监委领导
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
sys.path.insert(0, os.path.abspath("."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Constants ─────────────────────────────────────────────────────────────
SLUG = "北安市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Source URLs
SRC_GOV = "https://www.hljba.gov.cn/bas/c101116/ldlist.shtml"
SRC_NEWS_1 = "https://www.hljba.gov.cn/bas/c100749/202607/c11_356919.shtml"  # 市委常委会
SRC_NEWS_2 = "https://www.hljba.gov.cn/bas/c100749/202607/c11_357076.shtml"  # 人大常委会任命代市长
SRC_NEWS_3 = "https://www.hljba.gov.cn/bas/c102582/202607/c11_357091.shtml"  # 市政府常务会议

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. Core Leadership
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "孟凡晶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "education": "黑龙江省委党校经济管理专业，在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记、黑龙江北安经济开发区党工委书记、管委会主任",
        "current_org": "中共北安市委员会",
        "source": SRC_GOV
    },
    {
        "id": 2,
        "name": "李海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、副市长、代市长",
        "current_org": "北安市人民政府",
        "source": SRC_NEWS_2
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. Government Leadership (市政府)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张如东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "黑龙江省委党校公共管理研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    {
        "id": 4,
        "name": "生震涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "黑龙江省委党校经济管理专业毕业",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    {
        "id": 5,
        "name": "韩海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    {
        "id": 6,
        "name": "薛海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    {
        "id": 7,
        "name": "陈义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    {
        "id": 8,
        "name": "郝朝会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "中国农业机械化科学研究院机械设计及理论，研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    {
        "id": 9,
        "name": "朱兴成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    {
        "id": 10,
        "name": "谢艳丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1989年9月",
        "birthplace": "",
        "education": "黑龙江省委党校经济管理专业，研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "北安市人民政府",
        "source": SRC_GOV
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. People's Congress (市人大常委会)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "褚云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任（主持工作）",
        "current_org": "北安市人民代表大会常务委员会",
        "source": SRC_NEWS_2
    },
    {
        "id": 12,
        "name": "庞喜玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "北安市人民代表大会常务委员会",
        "source": SRC_NEWS_2
    },
    {
        "id": 13,
        "name": "张华峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "北安市人民代表大会常务委员会",
        "source": SRC_NEWS_2
    },
    {
        "id": 14,
        "name": "闫忠友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "北安市人民代表大会常务委员会",
        "source": SRC_NEWS_2
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. Other leaders mentioned in government meetings
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "李卫桥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "北安市",
        "source": SRC_NEWS_3
    },
    {
        "id": 16,
        "name": "任程远",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "北安市",
        "source": SRC_NEWS_3
    },
    {
        "id": 17,
        "name": "时映琨",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "北安市",
        "source": SRC_NEWS_3
    },
    {
        "id": 18,
        "name": "闫海龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人民法院院长",
        "current_org": "北安市人民法院",
        "source": SRC_NEWS_2
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共北安市委员会", "type": "党委", "level": "县级", "location": "北安市"},
    {"id": 2, "name": "北安市人民政府", "type": "政府", "level": "县级", "location": "北安市"},
    {"id": 3, "name": "北安市人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "北安市"},
    {"id": 4, "name": "中国人民政治协商会议北安市委员会", "type": "政协", "level": "县级", "location": "北安市"},
    {"id": 5, "name": "北安市纪委监委", "type": "党委", "level": "县级", "location": "北安市"},
    {"id": 6, "name": "北安市人民法院", "type": "政府", "level": "县级", "location": "北安市"},
    {"id": 7, "name": "北安市人民检察院", "type": "政府", "level": "县级", "location": "北安市"},
    {"id": 8, "name": "北安市公安局", "type": "政府", "level": "县级", "location": "北安市"},
    {"id": 9, "name": "黑龙江北安经济开发区", "type": "开发区", "level": "县级", "location": "北安市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 孟凡晶
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "经开区党工委书记、管委会主任", "start": "", "end": "present", "rank": "", "note": "兼任"},
    # 李海军
    {"person_id": 2, "org_id": 2, "title": "副市长、代市长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月23日市人大常委会任命"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2026-07", "end": "present", "rank": "", "note": ""},
    # 张如东
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 生震涛
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 韩海军
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "公安局局长", "start": "", "end": "present", "rank": "", "note": ""},
    # 薛海峰
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈义
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郝朝会
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 朱兴成
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 谢艳丽
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 11, "org_id": 3, "title": "副主任（主持工作）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 法院
    {"person_id": 18, "org_id": 6, "title": "院长", "start": "", "end": "present", "rank": "", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政正职之间
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "孟凡晶原兼任市长，2026年7月李海军接任代市长", "overlap_org": "北安市人民政府", "overlap_period": "2026-07"},
    # 党政正职与常务副职
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与常务副市长", "overlap_org": "中共北安市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "北安市人民政府", "overlap_period": "2026-07"},
    # 市委领导
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为市委常委", "overlap_org": "中共北安市委员会", "overlap_period": ""},
    # 政府班子
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同为市政府领导", "overlap_org": "北安市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同为市政府领导", "overlap_org": "北安市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "同为市政府领导", "overlap_org": "北安市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "同为市政府领导", "overlap_org": "北安市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "同为市政府领导", "overlap_org": "北安市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "同为市政府领导", "overlap_org": "北安市人民政府", "overlap_period": ""},
    # 人大班子
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "同为市人大常委会副主任", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 13, "type": "overlap", "context": "同为市人大常委会副主任", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 14, "type": "overlap", "context": "同为市人大常委会副主任", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "同为市人大常委会副主任", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 14, "type": "overlap", "context": "同为市人大常委会副主任", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "同为市人大常委会副主任", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": ""},
    # 政府与人大交叉
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "代市长向人大常委会做供职报告", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": "2026-07"},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "张如东列席人大常委会会议", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": "2026-07"},
    {"person_a": 3, "person_b": 12, "type": "overlap", "context": "张如东列席人大常委会会议", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": "2026-07"},
    # 政府与法院
    {"person_a": 3, "person_b": 18, "type": "overlap", "context": "张如东列席人大常委会会议，闫海龙同时出席", "overlap_org": "北安市人民代表大会常务委员会", "overlap_period": "2026-07"},
]

# ── Build ──────────────────────────────────────────────────────────────────
def main():
    db_path = DATABASE_DIR / f"{SLUG}_network.db"
    gexf_path = GRAPH_DIR / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\n✅ Build complete for {SLUG}")
    print(f"   Database: {db_path}")
    print(f"   GEXF:     {gexf_path}")
    print(f"   Persons:  {len(persons)}")
    print(f"   Orgs:     {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relations: {len(relationships)}")


if __name__ == "__main__":
    main()
