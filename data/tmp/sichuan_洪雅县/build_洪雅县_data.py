#!/usr/bin/env python3
"""Build script for 洪雅县 (眉山市·四川省) government personnel network data.

Generated: 2026-07-26
Sources:
  - Baidu Baike: 李忠云 https://baike.baidu.com/item/%E6%9D%8E%E5%BF%A0%E4%BA%91/20241483
  - Baidu Baike: 周代军 https://baike.baidu.com/item/%E5%91%A8%E4%BB%A3%E5%86%9B/23219420
  - Baidu Baike: 白海涛 https://baike.baidu.com/item/%E7%99%BD%E6%B5%B7%E6%B6%9B/58758143
  - Baidu Baike: 尹斗芳 https://baike.baidu.com/item/%E5%B0%B9%E6%96%97%E8%8A%B3
  - Baidu Baike: 吕文中 https://baike.baidu.com/item/%E5%90%95%E6%96%87%E4%B8%AD
  - Baidu Baike: 洪雅县 https://baike.baidu.com/item/%E6%B4%AA%E9%9B%85%E5%8E%BF/4911377
"""

import os, sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from gov_relation.runner import run_build

SLUG = "洪雅县"
STAGING_DIR = Path(__file__).parent

# ── Persons ──
# id is INTEGER PRIMARY KEY in schema

persons = [
    {"id": 1, "name": "周代军", "gender": "男", "ethnicity": "苗族", "birth": "1974年11月", "birthplace": "重庆彭水", "education": "四川工业学院（西华大学）建筑工程系 大学学历", "party_join": "1995年12月", "work_start": "1998年7月", "current_post": "眉山市副市长、洪雅县委书记", "current_org": "眉山市人民政府/中共洪雅县委", "source": "https://baike.baidu.com/item/%E5%91%A8%E4%BB%A3%E5%86%9B/23219420"},
    {"id": 2, "name": "李忠云", "gender": "男", "ethnicity": "汉族", "birth": "1973年11月", "birthplace": "四川井研", "education": "四川大学行政管理（自考）；省委党校经济管理（本科）", "party_join": "1996年6月", "work_start": "1994年8月", "current_post": "洪雅县委副书记、县长", "current_org": "洪雅县人民政府", "source": "https://baike.baidu.com/item/%E6%9D%8E%E5%BF%A0%E4%BA%91/20241483"},
    {"id": 3, "name": "白海涛", "gender": "男", "ethnicity": "汉族", "birth": "1982年3月", "birthplace": "", "education": "在职硕士，研究生学历", "party_join": "2005年4月", "work_start": "2007年7月", "current_post": "洪雅县委副书记、将军镇党委书记", "current_org": "中共洪雅县委", "source": "https://baike.baidu.com/item/%E7%99%BD%E6%B5%B7%E6%B6%9B/58758143"},
    {"id": 4, "name": "吕文中", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "洪雅县委常委、县纪委书记、县监委主任", "current_org": "洪雅县纪委监委", "source": "https://baike.baidu.com/item/%E5%90%95%E6%96%87%E4%B8%AD"},
    {"id": 5, "name": "黄旭东", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "洪雅县委常委、常务副县长", "current_org": "洪雅县人民政府", "source": "搜狗新闻"},
    {"id": 6, "name": "刘敏", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "洪雅县委常委、统战部部长、总工会主席、柳江古镇景区党工委书记", "current_org": "中共洪雅县委统战部", "source": "搜狗新闻"},
    {"id": 7, "name": "尹斗芳", "gender": "男", "ethnicity": "汉族", "birth": "1966年1月", "birthplace": "四川洪雅", "education": "四川省委党校函授学院行管、法律专业 大学学历", "party_join": "1990年2月", "work_start": "1984年8月", "current_post": "洪雅县人大常委会党组书记、主任", "current_org": "洪雅县人大常委会", "source": "https://baike.baidu.com/item/%E5%B0%B9%E6%96%97%E8%8A%B3"},
    {"id": 8, "name": "李明清", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "洪雅县政协主席", "current_org": "政协洪雅县委员会", "source": "搜狗新闻"},
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共洪雅县委", "type": "党委", "level": "县", "parent": "中共眉山市委", "location": "四川省眉山市洪雅县"},
    {"id": 2, "name": "洪雅县人民政府", "type": "政府", "level": "县", "parent": "眉山市人民政府", "location": "四川省眉山市洪雅县"},
    {"id": 3, "name": "洪雅县人大常委会", "type": "人大", "level": "县", "parent": "眉山市人大常委会", "location": "四川省眉山市洪雅县"},
    {"id": 4, "name": "政协洪雅县委员会", "type": "政协", "level": "县", "parent": "政协眉山市委员会", "location": "四川省眉山市洪雅县"},
    {"id": 5, "name": "洪雅县纪委监委", "type": "纪委", "level": "县", "parent": "中共洪雅县委", "location": "四川省眉山市洪雅县"},
    {"id": 6, "name": "中共洪雅县委统战部", "type": "党委", "level": "县", "parent": "中共洪雅县委", "location": "四川省眉山市洪雅县"},
    {"id": 7, "name": "眉山市人民政府", "type": "政府", "level": "地市", "parent": "四川省人民政府", "location": "四川省眉山市"},
    {"id": 8, "name": "洪雅县将军镇党委", "type": "乡镇", "level": "乡镇", "parent": "中共洪雅县委", "location": "四川省眉山市洪雅县将军镇"},
    {"id": 9, "name": "中共眉山市委", "type": "党委", "level": "地市", "parent": "中共四川省委", "location": "四川省眉山市"},
    {"id": 10, "name": "眉山市委组织部", "type": "党委", "level": "地市", "parent": "中共眉山市委", "location": "四川省眉山市"},
    {"id": 11, "name": "眉山市生态环境局", "type": "政府", "level": "地市", "parent": "眉山市人民政府", "location": "四川省眉山市"},
    {"id": 12, "name": "中共彭山区委", "type": "党委", "level": "县", "parent": "中共眉山市委", "location": "四川省眉山市彭山区"},
    {"id": 13, "name": "彭山区人民政府", "type": "政府", "level": "县", "parent": "眉山市人民政府", "location": "四川省眉山市彭山区"},
    {"id": 14, "name": "青神县人民政府", "type": "政府", "level": "县", "parent": "眉山市人民政府", "location": "四川省眉山市青神县"},
    {"id": 15, "name": "眉山市委宣传部", "type": "党委", "level": "地市", "parent": "中共眉山市委", "location": "四川省眉山市"},
    {"id": 16, "name": "中共洪雅县委政法委", "type": "党委", "level": "县", "parent": "中共洪雅县委", "location": "四川省眉山市洪雅县"},
    {"id": 17, "name": "中共洪雅县委组织部", "type": "党委", "level": "县", "parent": "中共洪雅县委", "location": "四川省眉山市洪雅县"},
    {"id": 18, "name": "洪雅县总工会", "type": "群团", "level": "县", "parent": "中共洪雅县委", "location": "四川省眉山市洪雅县"},
]

# ── Positions ──

positions = [
    # 周代军
    {"person_id": 1, "org_id": 7, "title": "眉山市副市长", "start_date": "2026-06", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "洪雅县委书记", "start_date": "2022-01", "end_date": "present", "rank": "正处级", "note": "2022.01-2022.03兼县长"},
    {"person_id": 1, "org_id": 2, "title": "洪雅县县长", "start_date": "2020-05", "end_date": "2022-01", "rank": "正处级", "note": "2020.03-2020.05代县长"},
    {"person_id": 1, "org_id": 1, "title": "洪雅县委副书记", "start_date": "2020-03", "end_date": "2022-01", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "眉山市生态环境局党组书记、局长", "start_date": "2019-01", "end_date": "2020-03", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "眉山市环境保护局党组书记、局长", "start_date": "2018-09", "end_date": "2019-01", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "眉山市委组织部副部长、市非公有制经济组织和社会组织工作委员会书记", "start_date": "2015-12", "end_date": "2018-09", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "眉山市委组织部副部长", "start_date": "2015-08", "end_date": "2015-12", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "彭山区委常委、组织部长", "start_date": "2012-12", "end_date": "2015-08", "rank": "副处级", "note": "兼党校校长"},
    {"person_id": 1, "org_id": 10, "title": "眉山市委组织部部务委员", "start_date": "2012-06", "end_date": "2012-12", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "眉山市非公有制经济组织和社会组织工作委员会副书记", "start_date": "2010-11", "end_date": "2012-06", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "眉山市委组织部组织科科长", "start_date": "2007-09", "end_date": "2010-09", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "眉山市委组织部组织科副科长", "start_date": "2005-08", "end_date": "2006-12", "rank": "副科级", "note": "2006.12-2007.09党代表联络办主任"},
    {"person_id": 1, "org_id": 10, "title": "眉山市委组织部干部", "start_date": "2002-05", "end_date": "2005-08", "rank": "科级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "共青团眉山市委办公室副主任", "start_date": "2001-11", "end_date": "2002-05", "rank": "副科级", "note": ""},
    # 李忠云
    {"person_id": 2, "org_id": 1, "title": "洪雅县委副书记", "start_date": "2022-03", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "洪雅县县长", "start_date": "2022-03", "end_date": "present", "rank": "正处级", "note": "2022.03.17当选"},
    {"person_id": 2, "org_id": 12, "title": "彭山区委常委、常务副区长", "start_date": "2018-09", "end_date": "2022-03", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "青神县委常委、常务副县长", "start_date": "2016-10", "end_date": "2018-09", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "彭山区委常委、政法委书记", "start_date": "2015-04", "end_date": "2016-10", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "彭山区(县)副区(县)长", "start_date": "2011-11", "end_date": "2015-04", "rank": "副处级", "note": ""},
    # 白海涛
    {"person_id": 3, "org_id": 1, "title": "洪雅县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼将军镇党委书记"},
    {"person_id": 3, "org_id": 17, "title": "洪雅县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "此前曾任"},
    {"person_id": 3, "org_id": 10, "title": "眉山市纪委派驻市委组织部纪检监察组组长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "眉山市委组织部副县级纪检员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 15, "title": "眉山市委宣传部办公室主任", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    # 吕文中
    {"person_id": 4, "org_id": 5, "title": "洪雅县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄旭东
    {"person_id": 5, "org_id": 2, "title": "洪雅县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘敏
    {"person_id": 6, "org_id": 6, "title": "洪雅县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼总工会主席、柳江古镇景区党工委书记"},
    # 尹斗芳
    {"person_id": 7, "org_id": 3, "title": "洪雅县人大常委会党组书记、主任", "start_date": "2020-05", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 16, "title": "洪雅县委常委、政法委书记", "start_date": "2009-07", "end_date": "2020-04", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "洪雅县委办公室主任", "start_date": "2006-08", "end_date": "2009-07", "rank": "正科级", "note": ""},
    {"person_id": 7, "org_id": 17, "title": "洪雅县委组织部副部长、党建办主任", "start_date": "2003-04", "end_date": "2006-08", "rank": "正科级", "note": ""},
    # 李明清
    {"person_id": 8, "org_id": 4, "title": "洪雅县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "周代军（县委书记）与李忠云（县长）——党政一把手搭档", "overlap_org": "洪雅县委/县政府", "overlap_period": "2022-03至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "周代军（县委书记）与白海涛（县委副书记）", "overlap_org": "中共洪雅县委", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "李忠云（县长）与白海涛（县委副书记）在县委班子中共事", "overlap_org": "中共洪雅县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "周代军（县委书记）与黄旭东（常务副县长）", "overlap_org": "洪雅县委常委会", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "李忠云（县长）与黄旭东（常务副县长）", "overlap_org": "洪雅县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "周代军（县委书记）与吕文中（纪委书记）", "overlap_org": "洪雅县委常委会", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "白海涛（曾任组织部长）与尹斗芳（曾任政法委书记）——洪雅县委常委会旧交", "overlap_org": "中共洪雅县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "周代军（县委书记）与刘敏（统战部长）", "overlap_org": "洪雅县委常委会", "overlap_period": ""},
]

# ── Main ──

DB_PATH = STAGING_DIR / "洪雅县_network.db"
GEXF_PATH = STAGING_DIR / "洪雅县_network.gexf"

def main() -> None:
    run_build(slug=SLUG, persons=persons, organizations=organizations, positions=positions, relationships=relationships, db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print(f"✅ DB: {DB_PATH}")
    print(f"✅ GEX: {GEXF_PATH}")
    print(f"   Persons:{len(persons)} Orgs:{len(organizations)} Positions:{len(positions)} Relations:{len(relationships)}")

if __name__ == "__main__":
    main()