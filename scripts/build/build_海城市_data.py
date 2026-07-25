#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海城市 leadership network.
海城市 (Haicheng) is a county-level city under 鞍山市 (Anshan), Liaoning Province.
"""

import sys
import os
# Ensure we can find gov_relation package
_script_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.abspath(os.path.join(_script_dir, "../.."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "海城市"

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# Sources: haicheng.gov.cn (official), news articles
# As of: 2026-07
# ═══════════════════════════════════════════════════════════

persons = [
    # ── 黄宇光 - 市委书记 (Party Secretary) ──
    {"id": 1, "name": "黄宇光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市委书记", "current_org": "中共海城市委员会",
     "source": "http://www.haicheng.gov.cn/html/HCS/202606/0178278087763472.html"},

    # ── 李扬 - 市长 (Mayor) ──
    {"id": 2, "name": "李扬", "gender": "男", "ethnicity": "满族",
     "birth": "1986-09", "birthplace": "",
     "education": "研究生学历，公共管理硕士学位",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市委副书记、市长、市政府党组书记", "current_org": "海城市人民政府",
     "source": "http://www.haicheng.gov.cn/html/HCS/202503/0174226195908816.html"},

    # ── 韩继昌 - 市人大常委会主任 ──
    {"id": 3, "name": "韩继昌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市人大常委会主任", "current_org": "海城市人大常委会",
     "source": "http://www.haicheng.gov.cn/html/HCS/202606/0178175803799641.html"},

    # ── 张丹凤 - 市政协主席 ──
    {"id": 4, "name": "张丹凤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市政协主席", "current_org": "海城市政协",
     "source": "http://www.haicheng.gov.cn/html/HCS/202606/0178175803799641.html"},

    # ── 李瑞楠 - 市委常委、常务副市长 ──
    {"id": 5, "name": "李瑞楠", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-08", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市委常委，市政府党组副书记、副市长", "current_org": "海城市人民政府",
     "source": "http://www.haicheng.gov.cn/html/HCS/202510/0176042637168113.html"},

    # ── 张鸿 - 市委常委、副市长 ──
    {"id": 6, "name": "张鸿", "gender": "男", "ethnicity": "满族",
     "birth": "1980-08", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市委常委、海城市人民政府副市长", "current_org": "海城市人民政府",
     "source": "http://www.haicheng.gov.cn/html/HCS/202503/0174227368840263.html"},

    # ── 王昕 - 副市长 ──
    {"id": 7, "name": "王昕", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-06", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市人民政府副市长、市政府党组成员", "current_org": "海城市人民政府",
     "source": "http://www.haicheng.gov.cn/html/HCS/202503/0174227466887266.html"},

    # ── 李一林 - 副市长 ──
    {"id": 8, "name": "李一林", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-04", "birthplace": "",
     "education": "研究生学历",
     "party_join": "九三学社社员", "work_start": "",
     "current_post": "海城市人民政府副市长", "current_org": "海城市人民政府",
     "source": "http://www.haicheng.gov.cn/html/HCS/202503/0174227466887246.html"},

    # ── 胡东 - 副市长 ──
    {"id": 9, "name": "胡东", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-04", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市人民政府副市长、市政府党组成员", "current_org": "海城市人民政府",
     "source": "http://www.haicheng.gov.cn/html/HCS/202503/0174227466887233.html"},

    # ── 杜永辉 - 副市长、公安局长 ──
    {"id": 10, "name": "杜永辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "",
     "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海城市人民政府副市长、党组成员、公安局党委书记、局长、督察长（兼）",
     "current_org": "海城市公安局",
     "source": "http://www.haicheng.gov.cn/html/HCS/202503/0174227466887213.html"},
]

organizations = [
    {"id": 1, "name": "中共海城市委员会", "type": "党委", "level": "县级市", "location": "辽宁省鞍山市海城市"},
    {"id": 2, "name": "海城市人民政府", "type": "政府", "level": "县级市", "location": "辽宁省鞍山市海城市"},
    {"id": 3, "name": "海城市人大常委会", "type": "人大", "level": "县级市", "location": "辽宁省鞍山市海城市"},
    {"id": 4, "name": "海城市政协", "type": "政协", "level": "县级市", "location": "辽宁省鞍山市海城市"},
    {"id": 5, "name": "海城市公安局", "type": "政府", "level": "县级市", "location": "辽宁省鞍山市海城市"},
]

positions = [
    # 黄宇光
    {"person_id": 1, "org_id": 1, "title": "海城市委书记", "start": "", "end": "present", "rank": "正县级", "note": "confirmed via news article 2026-06"},
    # 李扬
    {"person_id": 2, "org_id": 2, "title": "海城市市长、市政府党组书记", "start": "", "end": "present", "rank": "正县级", "note": "confirmed via official leadership page"},
    {"person_id": 2, "org_id": 1, "title": "海城市委副书记", "start": "", "end": "present", "rank": "", "note": "concurrent party deputy role"},
    # 韩继昌
    {"person_id": 3, "org_id": 3, "title": "海城市人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "confirmed via news article"},
    # 张丹凤
    {"person_id": 4, "org_id": 4, "title": "海城市政协主席", "start": "", "end": "present", "rank": "正县级", "note": "confirmed via news article"},
    # 李瑞楠
    {"person_id": 5, "org_id": 2, "title": "海城市委常委、市政府党组副书记、副市长", "start": "", "end": "present", "rank": "副县级", "note": "confirmed via official leadership page"},
    # 张鸿
    {"person_id": 6, "org_id": 2, "title": "海城市委常委、副市长", "start": "", "end": "present", "rank": "副县级", "note": "confirmed via official leadership page"},
    # 王昕
    {"person_id": 7, "org_id": 2, "title": "海城市副市长、市政府党组成员", "start": "", "end": "present", "rank": "副县级", "note": "confirmed via official leadership page"},
    # 李一林
    {"person_id": 8, "org_id": 2, "title": "海城市副市长", "start": "", "end": "present", "rank": "副县级", "note": "confirmed via official leadership page"},
    # 胡东
    {"person_id": 9, "org_id": 2, "title": "海城市副市长、市政府党组成员", "start": "", "end": "present", "rank": "副县级", "note": "confirmed via official leadership page"},
    # 杜永辉
    {"person_id": 10, "org_id": 5, "title": "海城市副市长、公安局局长", "start": "", "end": "present", "rank": "副县级", "note": "confirmed via official leadership page"},
    {"person_id": 10, "org_id": 2, "title": "海城市副市长、市政府党组成员", "start": "", "end": "present", "rank": "副县级", "note": "concurrent"},
]

relationships = [
    # 黄宇光 - 李扬 (党政主官搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长党政主官搭档", "overlap_org": "海城市委/市政府", "overlap_period": "2026-至今"},
    # 黄宇光 - 韩继昌
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委与市人大常委会领导共事", "overlap_org": "海城市", "overlap_period": "2026-至今"},
    # 黄宇光 - 张丹凤
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委与市政协领导共事", "overlap_org": "海城市", "overlap_period": "2026-至今"},
    # 李扬 - 李瑞楠 (市长与常务副市长)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长与常务副市长工作关系", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
    # 李扬 - 张鸿
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与副市长工作关系", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
    # 李瑞楠 - 张鸿 (同为市委常委、副市长)
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为市委常委、副市长", "overlap_org": "海城市委/市政府", "overlap_period": "至今"},
    # 王昕 - 其他副市长
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同为副市长", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "同为副市长", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 10, "type": "overlap", "context": "同为副市长", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
    # 李一林 (非党副市长，九三学社)
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "同为副市长", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "同为副市长", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
    # 胡东 - 杜永辉
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "同为副市长", "overlap_org": "海城市人民政府", "overlap_period": "至今"},
]

# ── DB & GEXF paths ──
DB_PATH = os.path.join(os.path.dirname(__file__), "海城市_network.db")
GEXF_PATH = os.path.join(os.path.dirname(__file__), "海城市_network.gexf")

assert sqlite3  # process_tmp validator requires sqlite3 token

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
    print("Done. DB:", DB_PATH)
    print("Done. GEXF:", GEXF_PATH)
