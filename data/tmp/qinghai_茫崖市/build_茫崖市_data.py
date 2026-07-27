#!/usr/bin/env python3
# Build SQLite database and GEXF graph for 茫崖市 leadership network.

import sys, os
STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(STAGING, "..", "..", ".."))
sys.path.insert(0, BASE)

import sqlite3
from gov_relation.runner import run_build

DB_PATH = os.path.join(STAGING, "茫崖市_network.db")
GEXF_PATH = os.path.join(STAGING, "茫崖市_network.gexf")

persons = [
    {"id": 1, "name": "苏铧烨", "gender": "男", "ethnicity": "汉族",
     "birth": "1990-01", "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市委副书记、市政府党组书记、市长",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/lyy.htm"},
    {"id": 2, "name": "丁忠超", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-04", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市委副书记、副市长（援青）",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/dzc.htm"},
    {"id": 3, "name": "王金龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-02", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市委副书记、副市长（援青）",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/wjl.htm"},
    {"id": 4, "name": "祝元甲", "gender": "男", "ethnicity": "藏族",
     "birth": "1982-10", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市委常委、副市长",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/zyj.htm"},
    {"id": 5, "name": "陈永梅", "gender": "女", "ethnicity": "藏族",
     "birth": "1983-11", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市政府党组成员、副市长",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/cym.htm"},
    {"id": 6, "name": "李琦", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市政府党组成员、副市长",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/lq.htm"},
    {"id": 7, "name": "李浩民", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-01", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市政府党组成员、副市长、市公安局党委书记、局长",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/lhm.htm"},
    {"id": 8, "name": "张泰尊", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-06", "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "茫崖市副市长人选、三级调研员",
     "current_org": "茫崖市人民政府",
     "source": "https://www.mangya.gov.cn/index/ldzc2/ztz.htm"},
]

organizations = [
    {"id": 1, "name": "中共茫崖市委员会", "type": "党委", "level": "县级市", "location": "茫崖市"},
    {"id": 2, "name": "茫崖市人民政府", "type": "政府", "level": "县级市", "location": "茫崖市"},
    {"id": 3, "name": "茫崖市公安局", "type": "政府", "level": "县级市", "location": "茫崖市"},
]

positions = [
    {"person_id": 1, "org_id": 2, "title": "茫崖市委副书记、市政府党组书记、市长"},
    {"person_id": 2, "org_id": 2, "title": "茫崖市委副书记、副市长（援青）"},
    {"person_id": 3, "org_id": 2, "title": "茫崖市委副书记、副市长（援青）"},
    {"person_id": 4, "org_id": 2, "title": "茫崖市委常委、副市长"},
    {"person_id": 5, "org_id": 2, "title": "茫崖市政府党组成员、副市长"},
    {"person_id": 6, "org_id": 2, "title": "茫崖市政府党组成员、副市长"},
    {"person_id": 7, "org_id": 2, "title": "茫崖市政府党组成员、副市长、市公安局党委书记、局长"},
    {"person_id": 7, "org_id": 3, "title": "茫崖市公安局党委书记、局长"},
    {"person_id": 8, "org_id": 2, "title": "茫崖市副市长人选、三级调研员"},
]

relationships = [
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市长与市委常委、副市长工作关系",
     "overlap_org": "茫崖市人民政府", "overlap_period": "2024-2026"},
    {"person_a": 7, "person_b": 3, "type": "superior_subordinate",
     "context": "市公安局党委书记、局长主管公安局",
     "overlap_org": "茫崖市公安局", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(
        slug="茫崖市",
        persons=persons, organizations=organizations,
        positions=positions, relationships=relationships,
        db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True,
    )
    print("Done.")
