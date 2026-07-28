#!/usr/bin/env python3
"""Build script for 石棉县 (雅安市·四川省) government personnel network data.

Generated: 2026-07-28
Sources:
  - shimian.gov.cn 石棉县人民政府领导页面 (https://www.shimian.gov.cn/leader.html)
  - shimian.gov.cn 政务信息 - 领导活动 (confirmed 周船 as 县委书记, 张瑜锋 as 县长)
  - shimian.gov.cn 站内搜索 (周船、张瑜锋活动报道)
"""

import os, sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "石棉县"
TODAY = "2026-07-28"

# ── Persons ──
# Source: shimian.gov.cn/leader.html (confirmed current as of 2026-07-28)

persons = [
    # Core leaders (IDs 1-11 = 县委领导)
    {"id": 1, "name": "周船", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委书记", "current_org": "中共石棉县委", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 2, "name": "张瑜锋", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委副书记、县人民政府党组书记、县长", "current_org": "石棉县人民政府", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 3, "name": "向正森", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委副书记", "current_org": "中共石棉县委", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 4, "name": "张思敏", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委、县人民政府常务副县长", "current_org": "石棉县人民政府", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 5, "name": "张喆", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委、县总工会主席", "current_org": "石棉县总工会", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 6, "name": "王成海", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委、宣传部部长", "current_org": "中共石棉县委宣传部", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 7, "name": "阎宇新", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委、县纪委书记、县监委主任", "current_org": "石棉县纪委监委", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 8, "name": "蔡珩", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委、统战部部长", "current_org": "中共石棉县委统战部", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 9, "name": "宋鹤麟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委、政法委书记", "current_org": "中共石棉县委政法委", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 10, "name": "范东平", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委", "current_org": "中共石棉县委", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 11, "name": "兰勇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县委常委、县人民武装部政委", "current_org": "石棉县人民武装部", "source": "https://www.shimian.gov.cn/leader.html"},

    # Government leaders (IDs 12-18)
    {"id": 12, "name": "张玲", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县人民政府党组成员、副县长", "current_org": "石棉县人民政府", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 13, "name": "吴大斌", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县人民政府副县长", "current_org": "石棉县人民政府", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 14, "name": "曹冀", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县人民政府副县长", "current_org": "石棉县人民政府", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 15, "name": "李挺", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县人民政府党组成员、副县长", "current_org": "石棉县人民政府", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 16, "name": "竹朝斌", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县人民政府党组成员、副县长，县公安局局长", "current_org": "石棉县公安局", "source": "https://www.shimian.gov.cn/leader.html"},
    {"id": 17, "name": "姜磊", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石棉县人民政府党组成员、副县长", "current_org": "石棉县人民政府", "source": "https://www.shimian.gov.cn/leader.html"},
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共石棉县委", "type": "党委", "level": "县", "parent": "中共雅安市委", "location": "四川省雅安市石棉县"},
    {"id": 2, "name": "石棉县人民政府", "type": "政府", "level": "县", "parent": "雅安市人民政府", "location": "四川省雅安市石棉县"},
    {"id": 3, "name": "石棉县纪委监委", "type": "纪委", "level": "县", "parent": "中共石棉县委", "location": "四川省雅安市石棉县"},
    {"id": 4, "name": "中共石棉县委宣传部", "type": "党委", "level": "县", "parent": "中共石棉县委", "location": "四川省雅安市石棉县"},
    {"id": 5, "name": "中共石棉县委统战部", "type": "党委", "level": "县", "parent": "中共石棉县委", "location": "四川省雅安市石棉县"},
    {"id": 6, "name": "中共石棉县委政法委", "type": "党委", "level": "县", "parent": "中共石棉县委", "location": "四川省雅安市石棉县"},
    {"id": 7, "name": "石棉县总工会", "type": "群团", "level": "县", "parent": "中共石棉县委", "location": "四川省雅安市石棉县"},
    {"id": 8, "name": "石棉县人民武装部", "type": "军队", "level": "县", "parent": "雅安军分区", "location": "四川省雅安市石棉县"},
    {"id": 9, "name": "石棉县公安局", "type": "政府", "level": "县", "parent": "石棉县人民政府", "location": "四川省雅安市石棉县"},
    {"id": 10, "name": "中共雅安市委", "type": "党委", "level": "地市", "parent": "中共四川省委", "location": "四川省雅安市"},
    {"id": 11, "name": "雅安市人民政府", "type": "政府", "level": "地市", "parent": "四川省人民政府", "location": "四川省雅安市"},
]

# ── Positions ──

positions = [
    # 周船 - party secretary
    {"person_id": 1, "org_id": 1, "title": "石棉县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed active as of 2026-07"},
    # 张瑜锋 - county magistrate
    {"person_id": 2, "org_id": 2, "title": "石棉县人民政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed active as of 2026-07"},
    {"person_id": 2, "org_id": 1, "title": "石棉县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Concurrent party role"},
    # 向正森 - deputy party secretary
    {"person_id": 3, "org_id": 1, "title": "石棉县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张思敏 - executive deputy magistrate
    {"person_id": 4, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "石棉县人民政府常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张喆 - union chair
    {"person_id": 5, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "石棉县总工会主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王成海 - propaganda
    {"person_id": 6, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "石棉县委宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 阎宇新 - discipline
    {"person_id": 7, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "石棉县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 蔡珩 - united front
    {"person_id": 8, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "石棉县委统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 宋鹤麟 - political-legal
    {"person_id": 9, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "石棉县委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 范东平 - general
    {"person_id": 10, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "无明确分工"},
    # 兰勇 - military
    {"person_id": 11, "org_id": 1, "title": "石棉县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "石棉县人民武装部政委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张玲 - deputy magistrate
    {"person_id": 12, "org_id": 2, "title": "石棉县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 吴大斌 - deputy magistrate
    {"person_id": 13, "org_id": 2, "title": "石棉县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 曹冀 - deputy magistrate
    {"person_id": 14, "org_id": 2, "title": "石棉县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李挺 - deputy magistrate
    {"person_id": 15, "org_id": 2, "title": "石棉县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 竹朝斌 - deputy magistrate + police bureau
    {"person_id": 16, "org_id": 2, "title": "石棉县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县公安局局长"},
    {"person_id": 16, "org_id": 9, "title": "石棉县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 姜磊 - deputy magistrate
    {"person_id": 17, "org_id": 2, "title": "石棉县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──
# Based on documented same-organization and same-period overlaps
# Confirmed from official government leadership page

relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共石棉县委/石棉县人民政府", "overlap_period": ""},
    # Party committee standing members working together
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共石棉县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "中共石棉县委", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "teamwork_subordinate", "context": "县长与常务副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "teamwork", "context": "县长与县委副书记", "overlap_org": "中共石棉县委", "overlap_period": ""},
    # Discipline inspection
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共石棉县委", "overlap_period": ""},
    # Political-legal committee
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与政法委书记", "overlap_org": "中共石棉县委", "overlap_period": ""},
    # Propaganda
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与宣传部长", "overlap_org": "中共石棉县委", "overlap_period": ""},
    # United front
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与统战部长", "overlap_org": "中共石棉县委", "overlap_period": ""},
    # Military
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委书记与人武部政委", "overlap_org": "中共石棉县委", "overlap_period": ""},
    # Government team: county magistrate + deputies
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长与副县长/公安局长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    # Standing committee interactions
    {"person_a": 4, "person_b": 12, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 13, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 14, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 15, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 16, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 17, "type": "teamwork", "context": "常务副县长与副县长", "overlap_org": "石棉县人民政府", "overlap_period": ""},
    # Standing committee lateral relationships
    {"person_a": 6, "person_b": 7, "type": "teamwork", "context": "宣传部长与纪委书记（同为县委常委）", "overlap_org": "中共石棉县委", "overlap_period": ""},
    {"person_a": 7, "person_b": 9, "type": "teamwork", "context": "纪委书记与政法委书记（同为县委常委）", "overlap_org": "中共石棉县委", "overlap_period": ""},
    {"person_a": 8, "person_b": 5, "type": "teamwork", "context": "统战部长与总工会主席（同为县委常委）", "overlap_org": "中共石棉县委", "overlap_period": ""},
]

# ── Run Build ──

if __name__ == "__main__":
    STAGING_DIR = Path(__file__).parent

    db_path = STAGING_DIR / f"{SLUG}_network.db"
    gexf_path = STAGING_DIR / f"{SLUG}_network.gexf"

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

    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"   数据库: {db_path}")
    print(f"   GEXF图: {gexf_path}")