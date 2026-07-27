#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 珙县 (宜宾市, 四川省) leadership."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "珙县"
DB = DATABASE_DIR / "gongxian_network.db"
GFX = GRAPH_DIR / "gongxian_network.gexf"

persons = [
    {"id": 1,  "name": "沙之杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县委书记", "current_org": "中共珙县县委", "source": "https://baike.baidu.com/item/珙县"},
    {"id": 2,  "name": "高果",   "gender": "男", "ethnicity": "汉族", "birth": "1978-06", "birthplace": "", "education": "研究生", "party_join": "", "work_start": "", "current_post": "县委副书记、县长", "current_org": "珙县人民政府", "source": "https://www.gongxian.gov.cn/zfld/xz/gg/"},
    {"id": 3,  "name": "侯杰",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县委副书记", "current_org": "中共珙县县委", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260629_2237980.html"},
    {"id": 4,  "name": "杨杰",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县委常委、政法委书记", "current_org": "中共珙县县委政法委", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202605/t20260511_2226204.html"},
    {"id": 5,  "name": "赵静",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县委常委、宣传部部长", "current_org": "中共珙县县委宣传部", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202607/t20260714_2242032.html"},
    {"id": 6,  "name": "胡正元", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县委常委、统战部部长、经开区党工委书记", "current_org": "中共珙县县委统战部", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202605/t20260509_2225878.html"},
    {"id": 7,  "name": "龚勋",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县委常委、常务副县长", "current_org": "珙县人民政府", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260610_2234262.html"},
    {"id": 8,  "name": "谢建文", "gender": "男", "ethnicity": "汉族", "birth": "1988-07", "birthplace": "四川省南溪区", "education": "研究生", "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "珙县人民政府", "source": "https://www.gongxian.gov.cn/zfld/fxz/xjw/"},
    {"id": 9,  "name": "贾泽鑫", "gender": "男", "ethnicity": "汉族", "birth": "1978-02", "birthplace": "", "education": "大学", "party_join": "", "work_start": "", "current_post": "副县长（兼巡场镇党委书记）", "current_org": "珙县人民政府", "source": "https://www.gongxian.gov.cn/zfld/fxz/jzx/"},
    {"id": 10, "name": "李文举", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "副县长、县公安局局长", "current_org": "珙县公安局", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202605/t20260529_2231663.html"},
    {"id": 11, "name": "严宏",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县人大常委会主任", "current_org": "珙县人大常委会", "source": "https://baike.baidu.com/item/珙县"},
    {"id": 12, "name": "李智",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县政协主席", "current_org": "珙县政协", "source": "https://baike.baidu.com/item/珙县"},
    {"id": 13, "name": "张春元", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县领导", "current_org": "珙县", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260618_2236122.html"},
    {"id": 14, "name": "张金伟", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县领导", "current_org": "珙县", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260618_2236122.html"},
    {"id": 15, "name": "罗道戡", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县领导", "current_org": "珙县", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260618_2236122.html"},
    {"id": 16, "name": "陈凌",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县领导", "current_org": "珙县", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260618_2236122.html"},
    {"id": 17, "name": "万强",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县领导", "current_org": "珙县", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260618_2236122.html"},
    {"id": 18, "name": "吕沐洋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "县领导", "current_org": "珙县", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260618_2236122.html"},
    {"id": 19, "name": "杨勇",   "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "（原）县委常委、宣传部部长", "current_org": "中共珙县县委宣传部", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260602_2232573.html"},
    {"id": 20, "name": "何银波", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "珙县人民政府", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202605/t20260508_2225657.html"},
    {"id": 21, "name": "陈欣",   "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "珙县人民政府", "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202604/t20260424_2222989.html"},
]

orgs = [
    {"id": 1,  "name": "中共珙县县委",              "type": "党委",     "level": "县级", "parent": "中共宜宾市委",     "location": "珙县"},
    {"id": 2,  "name": "珙县人民政府",              "type": "政府",     "level": "县级", "parent": "宜宾市人民政府",    "location": "珙县"},
    {"id": 3,  "name": "珙县人大常委会",             "type": "人大",     "level": "县级", "parent": "珙县",              "location": "珙县"},
    {"id": 4,  "name": "珙县政协",                   "type": "政协",     "level": "县级", "parent": "珙县",              "location": "珙县"},
    {"id": 5,  "name": "中共珙县县委政法委",         "type": "党委部门", "level": "县级", "parent": "中共珙县县委",      "location": "珙县"},
    {"id": 6,  "name": "中共珙县县委宣传部",         "type": "党委部门", "level": "县级", "parent": "中共珙县县委",      "location": "珙县"},
    {"id": 7,  "name": "中共珙县县委统战部",         "type": "党委部门", "level": "县级", "parent": "中共珙县县委",      "location": "珙县"},
    {"id": 8,  "name": "珙县公安局",                 "type": "政府机构", "level": "县级", "parent": "珙县人民政府",      "location": "珙县"},
    {"id": 9,  "name": "珙县经济开发区管委会",       "type": "派出机构", "level": "县级", "parent": "珙县人民政府",      "location": "珙县"},
    {"id": 10, "name": "珙县巡场镇党委",             "type": "党委",     "level": "乡科级", "parent": "中共珙县县委",    "location": "珙县巡场镇"},
    {"id": 11, "name": "中共珙县纪委监委",           "type": "纪委",     "level": "县级", "parent": "中共珙县县委",      "location": "珙县"},
]

positions = [
    {"person_id": 1,  "org_id": 1,  "title": "县委书记",            "start_date": "", "end_date": "", "rank": "正处级", "note": "县委一把手"},
    {"person_id": 2,  "org_id": 1,  "title": "县委副书记",          "start_date": "2023-12", "end_date": "", "rank": "正处级", "note": "同时任县政府党组书记、县长"},
    {"person_id": 2,  "org_id": 2,  "title": "县长",                "start_date": "2023-12", "end_date": "", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": 3,  "org_id": 1,  "title": "县委副书记",          "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4,  "org_id": 5,  "title": "县委常委、政法委书记","start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5,  "org_id": 6,  "title": "县委常委、宣传部部长","start_date": "2026-07", "end_date": "", "rank": "副处级", "note": "2026年6-7月间到任"},
    {"person_id": 6,  "org_id": 7,  "title": "县委常委、统战部部长","start_date": "", "end_date": "", "rank": "副处级", "note": "兼任县经开区党工委书记"},
    {"person_id": 7,  "org_id": 2,  "title": "县委常委、常务副县长","start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 8,  "org_id": 2,  "title": "副县长",              "start_date": "2025-12", "end_date": "", "rank": "副处级", "note": "兼任县自规局党组书记、局长"},
    {"person_id": 9,  "org_id": 2,  "title": "副县长",              "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": "兼任巡场镇党委书记"},
    {"person_id": 9,  "org_id": 10, "title": "巡场镇党委书记",      "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 2,  "title": "副县长",              "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8,  "title": "县公安局局长",         "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 11, "org_id": 3,  "title": "县人大常委会主任",     "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 4,  "title": "县政协主席",           "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 6,  "title": "（原）县委常委、宣传部部长","start_date": "", "end_date": "2026-06", "rank": "副处级", "note": "2026年7月由赵静接任"},
]

relationships = [
    {"person_a": 1,  "person_b": 2,  "type": "正副搭档", "context": "县委书记与县长搭档",             "overlap_org": "中共珙县县委/珙县政府", "overlap_period": ""},
    {"person_a": 1,  "person_b": 3,  "type": "正副搭档", "context": "书记与专职副书记",               "overlap_org": "中共珙县县委", "overlap_period": ""},
    {"person_a": 2,  "person_b": 3,  "type": "同级",     "context": "县长与副书记",                   "overlap_org": "中共珙县县委", "overlap_period": ""},
    {"person_a": 2,  "person_b": 7,  "type": "上下级",   "context": "县长与常务副县长",               "overlap_org": "珙县人民政府", "overlap_period": ""},
    {"person_a": 2,  "person_b": 8,  "type": "上下级",   "context": "县长与副县长",                   "overlap_org": "珙县人民政府", "overlap_period": ""},
    {"person_a": 2,  "person_b": 9,  "type": "上下级",   "context": "县长与副县长",                   "overlap_org": "珙县人民政府", "overlap_period": ""},
    {"person_a": 2,  "person_b": 10, "type": "上下级",   "context": "县长与副县长",                   "overlap_org": "珙县人民政府", "overlap_period": ""},
    {"person_a": 4,  "person_b": 1,  "type": "下属→上级", "context": "政法委书记向书记汇报",           "overlap_org": "中共珙县县委", "overlap_period": ""},
    {"person_a": 5,  "person_b": 1,  "type": "下属→上级", "context": "宣传部长向书记汇报",             "overlap_org": "中共珙县县委", "overlap_period": ""},
    {"person_a": 6,  "person_b": 1,  "type": "下属→上级", "context": "统战部长向书记汇报",             "overlap_org": "中共珙县县委", "overlap_period": ""},
    {"person_a": 7,  "person_b": 1,  "type": "下属→上级", "context": "常务副县长向书记汇报",           "overlap_org": "中共珙县县委/珙县政府", "overlap_period": ""},
    {"person_a": 7,  "person_b": 2,  "type": "下属→上级", "context": "常务副县长向县长汇报",           "overlap_org": "珙县人民政府", "overlap_period": ""},
    {"person_a": 4,  "person_b": 5,  "type": "常委同事",   "context": "政法委书记与宣传部长同为县委常委", "overlap_org": "中共珙县县委常委会", "overlap_period": ""},
    {"person_a": 4,  "person_b": 6,  "type": "常委同事",   "context": "政法委书记与统战部长同为县委常委", "overlap_org": "中共珙县县委常委会", "overlap_period": ""},
    {"person_a": 5,  "person_b": 6,  "type": "常委同事",   "context": "宣传部长与统战部长同为县委常委", "overlap_org": "中共珙县县委常委会", "overlap_period": ""},
    {"person_a": 5,  "person_b": 7,  "type": "常委同事",   "context": "宣传部长与常务副县长同为县委常委", "overlap_org": "中共珙县县委常委会", "overlap_period": ""},
    {"person_a": 4,  "person_b": 7,  "type": "常委同事",   "context": "政法委书记与常务副县长同为县委常委", "overlap_org": "中共珙县县委常委会", "overlap_period": ""},
    {"person_a": 19, "person_b": 5,  "type": "交接",       "context": "前宣传部部长与现任宣传部长的交接", "overlap_org": "中共珙县县委宣传部", "overlap_period": "2026-06/07"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=orgs,
        positions=positions,
        relationships=relationships,
        db_path=DB,
        gexf_path=GFX,
        overwrite=True,
    )
    print("Done: DB + GEXF built.")
