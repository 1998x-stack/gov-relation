#!/usr/bin/env python3
"""石龙区（平顶山市）领导班子工作关系网络构建脚本"""

import sys
import sqlite3
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

PERSONS = [
    {"id": 1, "name": "李明", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石龙区委书记", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/5152/751214.html"},
    {"id": 2, "name": "张晓鼎", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石龙区委副书记、区长", "current_org": "平顶山市石龙区人民政府", "source": "http://www.shilongqu.gov.cn/contents/36489/441753.html"},
    {"id": 3, "name": "陈延宾", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石龙区委副书记", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/5152/751480.html"},
    {"id": 4, "name": "康乐", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委、常务副区长", "current_org": "平顶山市石龙区人民政府", "source": "http://www.shilongqu.gov.cn/contents/36489/403697.html"},
    {"id": 5, "name": "熊志刚", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委、宣传部长、副区长", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/36489/297697.html"},
    {"id": 6, "name": "孙晓飞", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委、纪委书记、监委主任", "current_org": "中共平顶山市石龙区纪律检查委员会", "source": "http://www.shilongqu.gov.cn/contents/5152/751480.html"},
    {"id": 7, "name": "车昱茜", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/5152/748284.html"},
    {"id": 8, "name": "陶少琳", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/5152/748284.html"},
    {"id": 9, "name": "王延辉", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/5152/748284.html"},
    {"id": 10, "name": "李保民", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/5152/748284.html"},
    {"id": 11, "name": "马鹏飞", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区委常委、组织部部长", "current_org": "中共平顶山市石龙区委", "source": "http://www.shilongqu.gov.cn/contents/5152/751480.html"},
    {"id": 12, "name": "王勇", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府副区长", "current_org": "平顶山市石龙区人民政府", "source": "http://www.shilongqu.gov.cn/contents/36489/326249.html"},
    {"id": 13, "name": "崔国杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府副区长、区公安局局长", "current_org": "平顶山市石龙区人民政府", "source": "http://www.shilongqu.gov.cn/contents/36489/326251.html"},
    {"id": 14, "name": "李红超", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府副区长", "current_org": "平顶山市石龙区人民政府", "source": "http://www.shilongqu.gov.cn/contents/36489/327802.html"},
    {"id": 15, "name": "袁东娜", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "区政府副区长", "current_org": "平顶山市石龙区人民政府", "source": "http://www.shilongqu.gov.cn/contents/36489/468001.html"},
    {"id": 16, "name": "姚桃叶", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石龙区人大常委会主任(推定)", "current_org": "石龙区人大常委会", "source": "http://www.shilongqu.gov.cn/contents/5152/748284.html"},
    {"id": 17, "name": "刘向阳", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石龙区政协主席(推定)", "current_org": "政协石龙区委员会", "source": "http://www.shilongqu.gov.cn/contents/5152/748284.html"},
    {"id": 18, "name": "王伟", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石龙区人大常委会副主任", "current_org": "石龙区人大常委会", "source": "http://www.shilongqu.gov.cn/contents/5152/743804.html"},
    {"id": 19, "name": "孙增友", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "石龙区人大常委会副主任", "current_org": "石龙区人大常委会", "source": "http://www.shilongqu.gov.cn/contents/5152/743804.html"},
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共平顶山市石龙区委", "type": "党委", "level": "县处级", "parent": "中共平顶山市委", "location": "平顶山市石龙区"},
    {"id": 2, "name": "平顶山市石龙区人民政府", "type": "政府", "level": "县处级", "parent": "平顶山市人民政府", "location": "平顶山市石龙区"},
    {"id": 3, "name": "中共平顶山市石龙区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共平顶山市石龙区委", "location": "平顶山市石龙区"},
    {"id": 4, "name": "石龙区人大常委会", "type": "人大", "level": "县处级", "parent": "石龙区", "location": "平顶山市石龙区"},
    {"id": 5, "name": "政协石龙区委员会", "type": "政协", "level": "县处级", "parent": "石龙区", "location": "平顶山市石龙区"},
    {"id": 6, "name": "石龙区公安局", "type": "政府", "level": "乡科级", "parent": "平顶山市石龙区人民政府", "location": "平顶山市石龙区"},
]

POSITIONS = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "石龙区委书记", "start": "", "end": "", "rank": "正县级", "note": "第七届区委书记, 2026年6月当选"},
    {"person_id": 2, "org_id": 1, "title": "石龙区委副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "石龙区区长", "start": "", "end": "", "rank": "正县级", "note": "区政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "石龙区委副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "石龙区委常委", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start": "", "end": "", "rank": "副县级", "note": "区政府党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "石龙区委常委、宣传部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 纪委
    {"person_id": 6, "org_id": 3, "title": "石龙区纪委书记、监委主任", "start": "", "end": "", "rank": "副县级", "note": "区委常委"},
    {"person_id": 6, "org_id": 1, "title": "石龙区委常委", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 其他常委
    {"person_id": 7, "org_id": 1, "title": "石龙区委常委", "start": "", "end": "", "rank": "副县级", "note": "第七届区委常委"},
    {"person_id": 8, "org_id": 1, "title": "石龙区委常委", "start": "", "end": "", "rank": "副县级", "note": "第七届区委常委"},
    {"person_id": 9, "org_id": 1, "title": "石龙区委常委", "start": "", "end": "", "rank": "副县级", "note": "第七届区委常委"},
    {"person_id": 10, "org_id": 1, "title": "石龙区委常委", "start": "", "end": "", "rank": "副县级", "note": "第七届区委常委"},
    {"person_id": 11, "org_id": 1, "title": "石龙区委常委、组织部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 政府副区长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县级", "note": "负责工业、招商、开发区"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县级", "note": "负责公安、司法、信访"},
    {"person_id": 13, "org_id": 6, "title": "区公安局局长、督察长", "start": "", "end": "", "rank": "正科级", "note": "区公安局党委书记"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县级", "note": "负责自然资源、城建、交通"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副县级", "note": "负责农业农村、教育、卫健"},
    # 人大政协
    {"person_id": 16, "org_id": 4, "title": "人大常委会主任(推定)", "start": "", "end": "", "rank": "正县级", "note": "推定：区党代会主席团成员"},
    {"person_id": 17, "org_id": 5, "title": "政协主席(推定)", "start": "", "end": "", "rank": "正县级", "note": "推定：区党代会主席团成员"},
    {"person_id": 18, "org_id": 4, "title": "人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长", "overlap_org": "石龙区委", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 3, "type": "直接上下级", "context": "区委书记—区委副书记", "overlap_org": "石龙区委", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "区委副书记（同为书记副手）", "overlap_org": "石龙区委", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 4, "type": "直接上下级", "context": "区委书记—区委常委", "overlap_org": "石龙区委常委会", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 4, "type": "直接上下级", "context": "区长—常务副区长", "overlap_org": "石龙区政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 5, "type": "直接上下级", "context": "区长—副区长", "overlap_org": "石龙区政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 12, "type": "直接上下级", "context": "区长—副区长", "overlap_org": "石龙区政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 13, "type": "直接上下级", "context": "区长—副区长", "overlap_org": "石龙区政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 14, "type": "直接上下级", "context": "区长—副区长", "overlap_org": "石龙区政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 15, "type": "直接上下级", "context": "区长—副区长", "overlap_org": "石龙区政府", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 6, "type": "同僚", "context": "区委常委会同僚", "overlap_org": "石龙区委常委会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 11, "type": "直接上下级", "context": "区委书记—组织部部长", "overlap_org": "石龙区委常委会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 5, "type": "同僚", "context": "区委常委会同僚", "overlap_org": "石龙区委常委会", "overlap_period": "2026—"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "区委常委同僚", "overlap_org": "石龙区委常委会", "overlap_period": "2026—"},
    {"person_a": 11, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "石龙区委常委会", "overlap_period": "2026—"},
]

SLUG = "石龙区"
DB_PATH = DATABASE_DIR / "石龙区_network.db"
GEXF_PATH = GRAPH_DIR / "石龙区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")