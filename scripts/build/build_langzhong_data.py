#!/usr/bin/env python3
"""阆中市领导班子关系网络数据生成脚本"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "阆中市"

# Use integer IDs as required by schema (INTEGER PRIMARY KEY)
persons = [
    {"id": 1, "name": "杨德宇", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委书记", "current_org": "中共阆中市委员会",
     "source": "https://www.langzhong.gov.cn/xwdt/tttj/202607/t20260717_2347947.html"},
    {"id": 2, "name": "唐硕", "gender": "男", "ethnicity": "汉族", "birth": "1980-12", "birthplace": "四川南充",
     "education": "西华师范大学,公共事业管理", "party_join": "2005-06", "work_start": "1999-08",
     "current_post": "市委副书记、市长", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/sz/ts/202204/t20220401_600010.html"},
    {"id": 3, "name": "张小林", "gender": "男", "ethnicity": "汉族", "birth": "1978-05", "birthplace": "四川营山",
     "education": "四川师范大学,汉语言文学", "party_join": "1999-06", "work_start": "2000-08",
     "current_post": "市委常委、常务副市长", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/zxl/202604/t20260422_2327917.html"},
    {"id": 4, "name": "李新建", "gender": "男", "ethnicity": "汉族", "birth": "1979-11", "birthplace": "浙江仙居",
     "education": "硕士", "party_join": "2001-05", "work_start": "2002-08",
     "current_post": "市委常委、副市长（挂职）", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/lxj/202408/t20240801_2000564.html"},
    {"id": 5, "name": "杜小兵", "gender": "男", "ethnicity": "汉族", "birth": "1970-09", "birthplace": "四川南部",
     "education": "省委党校,法律", "party_join": "1996-12", "work_start": "1991-08",
     "current_post": "副市长、公安局长", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/dxb/202204/t20220401_601071.html"},
    {"id": 6, "name": "杜敏", "gender": "男", "ethnicity": "汉族", "birth": "1976-06", "birthplace": "四川阆中",
     "education": "四川师范大学,应用化学", "party_join": "1999-04", "work_start": "1998-02",
     "current_post": "副市长", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/dm/202502/t20250217_2092426.html"},
    {"id": 7, "name": "杨劲松", "gender": "男", "ethnicity": "汉族", "birth": "1982-03", "birthplace": "四川阆中",
     "education": "四川大学,法律", "party_join": "2000-05", "work_start": "2001-09",
     "current_post": "副市长", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/yjs/202204/t20220401_601457.html"},
    {"id": 8, "name": "张松", "gender": "男", "ethnicity": "汉族", "birth": "1981-07", "birthplace": "四川阆中",
     "education": "四川师范大学,汉语言文学", "party_join": "2002-07", "work_start": "2000-09",
     "current_post": "副市长", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/zsld/202204/t20220401_601585.html"},
    {"id": 9, "name": "邓雁城", "gender": "男", "ethnicity": "汉族", "birth": "1979-04", "birthplace": "河南延津",
     "education": "山东大学,数学,硕士", "party_join": "", "work_start": "2000-07",
     "current_post": "副市长（挂职）", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/dyc/202510/t20251022_2274722.html"},
    {"id": 10, "name": "何姝睿", "gender": "女", "ethnicity": "汉族", "birth": "1988-01", "birthplace": "四川营山",
     "education": "西华师范大学,公共管理,硕士", "party_join": "", "work_start": "2011-05",
     "current_post": "副市长", "current_org": "阆中市人民政府",
     "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/hdr/202510/t20251022_2274730.html"},
]

organizations = [
    {"id": 1, "name": "中共阆中市委员会", "type": "党委", "level": "县级", "parent": "中共南充市委员会", "location": "四川省南充市阆中市"},
    {"id": 2, "name": "阆中市人民政府", "type": "政府", "level": "县级", "parent": "南充市人民政府", "location": "四川省南充市阆中市"},
    {"id": 3, "name": "阆中市公安局", "type": "政府机构", "level": "县级", "parent": "阆中市人民政府", "location": "四川省南充市阆中市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "东西部协作"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "来自中国电子信息"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "目前在请假"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "书记-市长党政正职合作", "overlap_org": "中共阆中市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 2, "type": "上下级", "context": "常务副市长为市长副手", "overlap_org": "阆中市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "AB角", "context": "常务副市长与公安局长为AB角配对", "overlap_org": "阆中市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "AB角", "context": "杜敏与张松为AB角配对", "overlap_org": "阆中市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "AB角", "context": "李新建与杨劲松为AB角配对", "overlap_org": "阆中市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "同级挂职", "context": "均为外地挂职副市长", "overlap_org": "阆中市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "同为阆中本地籍干部", "overlap_org": "阆中市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "同为阆中本地籍干部", "overlap_org": "阆中市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "同乡", "context": "同为营山籍干部", "overlap_org": "阆中市人民政府", "overlap_period": ""},
]

if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DATABASE_DIR / f"{slug}_network.db"),
        gexf_path=str(GRAPH_DIR / f"{slug}_network.gexf"),
        overwrite=True,
    )
    print(f"Done! DB: {DATABASE_DIR / f'{slug}_network.db'}")
    print(f"GEXF: {GRAPH_DIR / f'{slug}_network.gexf'}")
