#!/usr/bin/env python3
"""额尔古纳市领导班子关系网络数据生成脚本.

核心人物：市委书记 王波；市委副书记、市长 耿浩；前任书记 闫立志、文进磊；
前任市委副书记/政法委书记 布尔金（现扎赉诺尔区委书记）等。
证据来源：额尔古纳市人民政府官网（www.eegn.gov.cn）领导之窗、政府班子分工通知(2026-03-30)、
六届人大会议政务新闻、自治区党委任前公示(2024-05)等。
"""

import os
import sys
import sqlite3  # noqa: F401  (standard library; DB written via gov_relation.schema)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "额尔古纳市"

DB_PATH = DATABASE_DIR / f"{slug}_network.db"
GEXF_PATH = GRAPH_DIR / f"{slug}_network.gexf"

# ---------------------------------------------------------------------------
# persons
# ---------------------------------------------------------------------------
persons = [
    # ---- 现任主官 ----
    {"id": 1, "name": "王波", "gender": "男", "ethnicity": "汉族", "birth": "1981-05", "birthplace": "待查",
     "education": "大学学历", "party_join": "待查", "work_start": "待查",
     "current_post": "市委书记", "current_org": "中共额尔古纳市委员会",
     "source": "http://www.eegn.gov.cn/Leader/show/283/1064.html"},
    {"id": 2, "name": "耿浩", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委副书记、市长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/OpennessContent/show/560245.html"},
    # 市委班子
    {"id": 3, "name": "郭金双", "gender": "男", "ethnicity": "汉族", "birth": "1979-08", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委副书记、政法委书记", "current_org": "中共额尔古纳市委员会",
     "source": "http://www.eegn.gov.cn/Leader/show/283/1056.html"},
    {"id": 4, "name": "王兴扬", "gender": "男", "ethnicity": "汉族", "birth": "1976-08", "birthplace": "待查",
     "education": "内蒙古党校研究生、文学学士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、常务副市长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/Leader/show/283/915.html"},
    {"id": 5, "name": "高云", "gender": "女", "ethnicity": "汉族", "birth": "1967-01", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、市纪委书记、监委主任", "current_org": "中共额尔古纳市纪律检查委员会",
     "source": "http://www.eegn.gov.cn/Leader/show/283/554.html"},
    {"id": 6, "name": "王福国", "gender": "男", "ethnicity": "汉族", "birth": "1979-10", "birthplace": "待查",
     "education": "大学/工学、理学双学士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、组织部部长", "current_org": "中共额尔古纳市委员会",
     "source": "http://www.eegn.gov.cn/Leader/show/283/1040.html"},
    {"id": 7, "name": "夏玉杰", "gender": "女", "ethnicity": "汉族", "birth": "1977-10", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、宣传部部长", "current_org": "中共额尔古纳市委员会",
     "source": "http://www.eegn.gov.cn/Leader/show/283/549.html"},
    {"id": 8, "name": "张晓峰", "gender": "男", "ethnicity": "蒙古族", "birth": "1986-09", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、统战部部长、副市长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/Leader/show/283/" + "1130.html"},
    {"id": 9, "name": "王雪松", "gender": "男", "ethnicity": "待查", "birth": "1982-04", "birthplace": "待查",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、办公室主任", "current_org": "中共额尔古纳市委员会",
     "source": "http://www.eegn.gov.cn/Leader/show/283/" + "1050.html"},
    {"id": 10, "name": "杨利", "gender": "男", "ethnicity": "汉族", "birth": "1978-10", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市委常委、市人民武装部上校部长", "current_org": "额尔古纳市人民武装部",
     "source": "http://www.eegn.gov.cn/Leader/show/283/" + "1000.html"},
    # ---- 政府副市长 ----
    {"id": 11, "name": "钱翀", "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长、市公安局党委书记局长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/OpennessContent/show/560245.html"},
    {"id": 12, "name": "李建兰", "gender": "女", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/OpennessContent/show/560245.html"},
    {"id": 13, "name": "游钎", "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/OpennessContent/show/560245.html"},
    {"id": 14, "name": "刘博学", "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/OpennessContent/show/560245.html"},
    {"id": 15, "name": "闫浩", "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "副市长", "current_org": "额尔古纳市人民政府",
     "source": "http://www.eegn.gov.cn/OpennessContent/show/560245.html"},
    # ---- 人大 / 政协 ----
    {"id": 16, "name": "闫淑霞", "gender": "女", "ethnicity": "汉族", "birth": "1971-09", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市人大常委会党组书记、主任", "current_org": "额尔古纳市人大常委会",
     "source": "http://www.eegn.gov.cn/Leader/show/284/" + "700.html"},
    {"id": 17, "name": "邱革评", "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市政协党组书记、主席", "current_org": "中国人民政治协商会议额尔古纳市委员会",
     "source": "http://www.eegn.gov.cn/Leader/show/286/" + "800.html"},
    # ---- 前任主官 ----
    {"id": 18, "name": "闫立志", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "呼伦贝尔市委常委、宣传部部长", "current_org": "中共呼伦贝尔市委员会",
     "source": "https://www.hlbe.gov.cn/"},
    {"id": 19, "name": "文进磊", "gender": "男", "ethnicity": "蒙古族", "birth": "1974-04", "birthplace": "待查",
     "education": "在职研究生、法学博士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "呼伦贝尔市副市长", "current_org": "呼伦贝尔市人民政府",
     "source": "https://www.hlbe.gov.cn/"},
    {"id": 20, "name": "布尔金", "gender": "男", "ethnicity": "蒙古族", "birth": "1976-11", "birthplace": "待查",
     "education": "博士研究生", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委书记", "current_org": "中共扎赉诺尔区委员会",
     "source": "../persons/20260806-内蒙古自治区-呼伦贝尔市-区委书记-布尔金.json"},
    {"id": 21, "name": "阿晋勒", "gender": "男", "ethnicity": "蒙古族", "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "呼伦贝尔市财政局局长", "current_org": "呼伦贝尔市财政局",
     "source": "https://www.hlbe.gov.cn/"},
]

# ---------------------------------------------------------------------------
# organizations
# ---------------------------------------------------------------------------
organizations = [
    {"id": 1, "name": "中共额尔古纳市委员会", "type": "党委", "level": "县级", "parent": "中共呼伦贝尔市委员会", "location": "内蒙古自治区呼伦贝尔市额尔古纳市"},
    {"id": 2, "name": "额尔古纳市人民政府", "type": "政府", "level": "县级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市额尔古纳市"},
    {"id": 3, "name": "额尔古纳市人大常委会", "type": "人大", "level": "县级", "parent": "呼伦贝尔市人大常委会", "location": "内蒙古自治区呼伦贝尔市额尔古纳市"},
    {"id": 4, "name": "政协额尔古纳市委员会", "type": "政协", "level": "县级", "parent": "政协呼伦贝尔市委员会", "location": "内蒙古自治区呼伦贝尔市额尔古纳市"},
    {"id": 5, "name": "中共呼伦贝尔市委员会", "type": "党委", "level": "地级", "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区呼伦贝尔市海拉尔区"},
    {"id": 6, "name": "呼伦贝尔市人民政府", "type": "政府", "level": "地级", "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区呼伦贝尔市海拉尔区"},
    {"id": 7, "name": "呼伦贝尔市财政局", "type": "政府机构", "level": "地级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市海拉尔区"},
    {"id": 8, "name": "中共扎赉诺尔区委员会", "type": "党委", "level": "县级", "parent": "中共呼伦贝尔市委员会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
]

# ---------------------------------------------------------------------------
# positions
# ---------------------------------------------------------------------------
positions = [
    # 现任
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-03", "end_date": "present", "rank": "正处级", "note": "主持市委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2021", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作，五届人大六次会议当选，六届连任"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "2023-05", "end_date": "present", "rank": "副处级", "note": "接替布尔金"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "市委班子成员分工，分管发改、财政、招商、应急"},
    {"person_id": 5, "org_id": 1, "title": "市委常委、市纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市委常委、办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委（市人武部部长）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管法治、社会稳定，主持公安局"},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管民政、卫健、教育科技、医保"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管林农牧业、乡村振兴、住建、自然资源"},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管水利、政务、城管、交通、机场铁路"},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管市场监管、文旅体、口岸商务"},
    # 人大 / 政协
    {"person_id": 16, "org_id": 3, "title": "人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ---------------------------------------------------------------------------
# relationships
# ---------------------------------------------------------------------------
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "书书记-市长党政正职搭档，主抓额尔古纳全面工作", "overlap_org": "中共额尔古纳市委员会", "overlap_period": "2026—present"},
    {"person_a": 18, "person_b": 1, "type": "前后任", "context": "闫立志任书书记后由王波接替（2026.03前后交接）", "overlap_org": "中共额尔古纳市委员会", "overlap_period": "2026"},
    {"person_a": 19, "person_b": 18, "type": "前后任", "context": "文进磊前往呼伦贝尔市副市长后，由闫立志兼任书书记（市委宣传部部长兼）", "overlap_org": "中共额尔古纳市委员会", "overlap_period": "2024-2026"},
    {"person_a": 19, "person_b": 2, "type": "前后任/同僚", "context": "文进磊任书书记期间耿浩任市长，六届党政搭档；文进磊后任呼伦贝尔市副市长", "overlap_org": "额尔古纳市人民政府", "overlap_period": "2021-2024"},
    {"person_a": 20, "person_b": 19, "type": "上下级", "context": "布尔金任市委副书记、政法委书记期间，文进磊为书书记", "overlap_org": "中共额尔古纳市委员会", "overlap_period": "2021-2023.05"},
    {"person_a": 20, "person_b": 3, "type": "前后任", "context": "布尔金2023.05离任政法委后，由郭金双接任", "overlap_org": "中共额尔古纳市委员会", "overlap_period": "2023.05"},
    {"person_a": 21, "person_b": 2, "type": "前后任", "context": "阿晋勒任前市长（五届），耿浩在五届人大六次会议补选接任市长", "overlap_org": "额尔古纳市人民政府", "overlap_period": "2021"},
    {"person_a": 21, "person_b": 19, "type": "上下级", "context": "阿晋勒任市长期间文进磊为书书记（2021前后）", "overlap_org": "额尔古纳市人民政府", "overlap_period": "2021"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "市长-常务副市长为AB角/正副手配对", "overlap_org": "额尔古纳市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 11, "type": "AB角", "context": "常务副市长与公安局长为AB角配对（分管应急与社会稳定）", "overlap_org": "额尔古纳市人民政府", "overlap_period": ""},
]

if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print(f"Done! DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")