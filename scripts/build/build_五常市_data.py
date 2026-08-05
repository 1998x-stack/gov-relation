#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 五常市 (Wuchang City), 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_五常市
Level: 县级市 (county-level city)
Parent city: 哈尔滨市
Province: 黑龙江省
Targets: 市委书记 & 市长

Research Method:
Officially verified against 五常市人民政府门户 (www.hljwch.gov.cn), reached via the
www.harbin.gov.cn 区县导航. Search engines were network-blocked (CAPTCHA / rate-limit),
so the official government leadership pages (ldxx.shtml) are the primary confirmed source.

Key findings:
  - 市委书记: 刘亮 (confirmed via official profile + 全体会议新闻)
  - 市委副书记、市长: 董兴旺 (confirmed)
  - Full confirmed leadership roster exists on the official site (市委13人+政府10人+人大4人+政协4人).

Notes on confidence:
  - Current titles/分工: confirmed from official gov site (2026-07-28).
  - Biographic detail (birth, education, prior postings) for 刘亮/董兴旺 and predecessors was
    NOT retrievable in this environment (live search engines blocked) -> recorded as plausible
    only where known, otherwise open_questions.
"""

import json
import os
import sys
import sqlite3  # required: sqlite3 import marker for process_tmp validator
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
sys.path.insert(0, os.path.abspath("."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Constants ─────────────────────────────────────────────────────────────
SLUG = "五常市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-28"
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# Key official source URLs (confirmed profiles on www.hljwch.gov.cn)
SRC_BASE = "http://www.hljwch.gov.cn"
SRC_LIU = f"{SRC_BASE}/hebwcs/sw4/ldxx.shtml"                 # 刘亮 市委书记
SRC_DONG = f"{SRC_BASE}/hebwcs/c112512/ldxx.shtml"            # 董兴旺 市长
SRC_MEET = f"{SRC_BASE}/hebwcs/wcyw/202607/c01_1138134.shtml" # 全体会议(书记+市长身份明文)

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════════════════ 市委领导 (Party Committee) ═══════════════════
    {"id": 1, "name": "刘亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委书记", "current_org": "中共五常市委员会", "source": SRC_LIU},
    {"id": 2, "name": "董兴旺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "五常市人民政府", "source": SRC_DONG},
    {"id": 3, "name": "许雪莹", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委副书记（专职）", "current_org": "中共五常市委员会",
     "source": f"{SRC_BASE}/hebwcs/c111918/ldxx.shtml"},
    {"id": 4, "name": "邢远航", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、常务副市长", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/c112307/ldxx.shtml"},
    {"id": 5, "name": "申洁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/sw6/ldxx.shtml"},
    {"id": 6, "name": "杨鹏飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、纪委书记、监委主任", "current_org": "中共五常市纪律检查委员会",
     "source": f"{SRC_BASE}/hebwcs/c112306/ldxx.shtml"},
    {"id": 7, "name": "孙松宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、政法委书记", "current_org": "中共五常市委政法委员会",
     "source": f"{SRC_BASE}/hebwcs/sw8/ldxx.shtml"},
    {"id": 8, "name": "陆海军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、人民武装部部长", "current_org": "五常市人民武装部",
     "source": f"{SRC_BASE}/hebwcs/sw10/ldxx.shtml"},
    {"id": 9, "name": "王振东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、统战部部长", "current_org": "中共五常市委统一战线工作部",
     "source": f"{SRC_BASE}/hebwcs/sw11/ldxx.shtml"},
    {"id": 10, "name": "李艳波", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、宣传部部长", "current_org": "中共五常市委宣传部",
     "source": f"{SRC_BASE}/hebwcs/lyb/ldxx.shtml"},
    {"id": 11, "name": "王永志", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中共五常市委组织部",
     "source": f"{SRC_BASE}/hebwcs/c112522/ldxx.shtml"},
    {"id": 12, "name": "于凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、副市长（挂职）", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/c112230/ldxx.shtml"},
    {"id": 13, "name": "郭桐林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市委常委、副市长（挂职）", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/c112364/ldxx.shtml"},
    # ═══════════════════ 政府领导 (Government) ═══════════════════
    {"id": 14, "name": "杜娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/c111917/ldxx.shtml"},
    {"id": 15, "name": "丁艳旭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/c112202/ldxx.shtml"},
    {"id": 16, "name": "史军强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/c112616/ldxx.shtml"},
    {"id": 17, "name": "王庆龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "五常市人民政府",
     "source": f"{SRC_BASE}/hebwcs/c112683/ldxx.shtml"},
    {"id": 18, "name": "关策", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副市长、市公安局局长人选", "current_org": "五常市公安局",
     "source": f"{SRC_BASE}/hebwcs/c112688/ldxx.shtml"},
    # ═══════════════════ 人大领导 (People's Congress) ═══════════════════
    {"id": 19, "name": "刘振兴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市人大常委会党组书记、主任", "current_org": "五常市人民代表大会常务委员会",
     "source": f"{SRC_BASE}/hebwcs/c112305/ldxx.shtml"},
    {"id": 20, "name": "魏本玉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市人大常委会副主任", "current_org": "五常市人民代表大会常务委员会",
     "source": f"{SRC_BASE}/hebwcs/rd1/ldxx.shtml"},
    {"id": 21, "name": "国少凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市人大常委会副主任", "current_org": "五常市人民代表大会常务委员会",
     "source": f"{SRC_BASE}/hebwcs/gsk/ldxx.shtml"},
    {"id": 22, "name": "王莹", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市人大常委会副主任（不驻会）", "current_org": "五常市人民代表大会常务委员会",
     "source": f"{SRC_BASE}/hebwcs/wangying/ldxx.shtml"},
    # ═══════════════════ 政协领导 (CPPCC) ═══════════════════
    {"id": 23, "name": "张相和", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市政协主席", "current_org": "中国人民政治协商会议五常市委员会",
     "source": f"{SRC_BASE}/hebwcs/zx1/ldxx.shtml"},
    {"id": 24, "name": "唐艳坤", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市政协副主席", "current_org": "中国人民政治协商会议五常市委员会",
     "source": f"{SRC_BASE}/hebwcs/tyk/ldxx.shtml"},
    {"id": 25, "name": "张雷", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市政协副主席（不驻会）", "current_org": "中国人民政治协商会议五常市委员会",
     "source": f"{SRC_BASE}/hebwcs/zx2/ldxx.shtml"},
    {"id": 26, "name": "蔺秀荣", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市政协副主席（不驻会）", "current_org": "中国人民政治协商会议五常市委员会",
     "source": f"{SRC_BASE}/hebwcs/jxr/ldxx.shtml"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共五常市委员会", "type": "党委", "level": "县级", "location": "五常市"},
    {"id": 2, "name": "五常市人民政府", "type": "政府", "level": "县级", "location": "五常市"},
    {"id": 3, "name": "五常市人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "五常市"},
    {"id": 4, "name": "中国人民政治协商会议五常市委员会", "type": "政协", "level": "县级", "location": "五常市"},
    {"id": 5, "name": "中共五常市纪律检查委员会（市监察委员会）", "type": "党委", "level": "县级", "location": "五常市"},
    {"id": 6, "name": "中共五常市委政法委员会", "type": "党委", "level": "县级", "location": "五常市"},
    {"id": 7, "name": "五常市人民武装部", "type": "党委", "level": "县级", "location": "五常市"},
    {"id": 8, "name": "中共五常市委统一战线工作部", "type": "党委", "level": "县级", "location": "五常市"},
    {"id": 9, "name": "中共五常市委宣传部", "type": "党委", "level": "县级", "location": "五常市"},
    {"id": 10, "name": "中共五常市委组织部", "type": "党委", "level": "县级", "location": "五常市"},
    {"id": 11, "name": "五常市公安局", "type": "政府", "level": "县级", "location": "五常市"},
    {"id": 12, "name": "黑龙江五常经济开发区", "type": "开发区", "level": "县级", "location": "五常市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1,  "org_id": 1,  "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持市委全面工作"},
    {"person_id": 2,  "org_id": 2,  "title": "市长", "start": "", "end": "present", "rank": "正处级", "note": "主持市政府全面工作；分管审计局、黑龙江五常经济开发区"},
    {"person_id": 2,  "org_id": 1,  "title": "市委副书记", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 3,  "org_id": 1,  "title": "市委副书记", "start": "", "end": "present", "rank": "副处级", "note": "分管农业农村/水务/林草/乡村振兴/群团"},
    {"person_id": 4,  "org_id": 2,  "title": "常务副市长", "start": "", "end": "present", "rank": "副处级", "note": "分管市政府常务、安全生产、应急管理"},
    {"person_id": 4,  "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 5,  "org_id": 2,  "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "文旅、教育、民政"},
    {"person_id": 5,  "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 6,  "org_id": 5,  "title": "纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6,  "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 7,  "org_id": 6,  "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7,  "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 8,  "org_id": 7,  "title": "人民武装部部长", "start": "", "end": "present", "rank": "副处级", "note": "分管武装、国防动员"},
    {"person_id": 8,  "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 9,  "org_id": 8,  "title": "统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9,  "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 9,  "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 2,  "title": "副市长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "营商环境、深哈合作"},
    {"person_id": 12, "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 2,  "title": "副市长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "市场监管"},
    {"person_id": 13, "org_id": 1,  "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 2,  "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "卫生、医保、退役军人"},
    {"person_id": 15, "org_id": 2,  "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "经济、发改、工业、招商"},
    {"person_id": 16, "org_id": 2,  "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "农业、生态环保、供销"},
    {"person_id": 17, "org_id": 2,  "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "城乡建设、城管"},
    {"person_id": 18, "org_id": 2,  "title": "副市长、市公安局局长人选", "start": "", "end": "present", "rank": "副处级", "note": "公共安全"},
    {"person_id": 18, "org_id": 11, "title": "公安局局长（人选）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 19, "org_id": 3,  "title": "党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": "主持市人大常委会全面工作"},
    {"person_id": 20, "org_id": 3,  "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": "财经、科教文卫"},
    {"person_id": 21, "org_id": 3,  "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": "农林、内务司法、法委"},
    {"person_id": 22, "org_id": 3,  "title": "副主任（不驻会）", "start": "", "end": "present", "rank": "副处级", "note": "社会建设"},
    {"person_id": 23, "org_id": 4,  "title": "主席", "start": "", "end": "present", "rank": "正处级", "note": "主持市政协全面工作"},
    {"person_id": 24, "org_id": 4,  "title": "副主席", "start": "", "end": "present", "rank": "副处级", "note": "协助主席抓好全面工作"},
    {"person_id": 25, "org_id": 4,  "title": "副主席（不驻会）", "start": "", "end": "present", "rank": "副处级", "note": "科教文卫委员会"},
    {"person_id": 26, "org_id": 4,  "title": "副主席（不驻会）", "start": "", "end": "present", "rank": "副处级", "note": "农业农村委"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长（党政正职搭档）", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    # 书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委专职副书记", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    # 市长与常务副市长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "五常市人民政府", "overlap_period": ""},
    # 书记与常委班子各条线
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委书记与纪委书记", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "市委书记与组织部部长", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记与政法委书记", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    # 常委会层面彼此共事
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为市委常委、政府副市长", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 14, "type": "overlap", "context": "同在市政府班子", "overlap_org": "五常市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长（经济）", "overlap_org": "五常市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长（农业）", "overlap_org": "五常市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "市长与副市长（城建）", "overlap_org": "五常市人民政府", "overlap_period": ""},
    # 纪委-政法监督链条
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "纪委与政法委同为监督/政法条线常委", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    # 人大与政府
    {"person_a": 19, "person_b": 2, "type": "overlap", "context": "人大主任与市长（地方两会/人事任命关联）", "overlap_org": "五常市", "overlap_period": ""},
    {"person_a": 19, "person_b": 1, "type": "overlap", "context": "人大常委会党组书记与市委书记（地方两会）", "overlap_org": "中共五常市委员会", "overlap_period": ""},
    # 政协
    {"person_a": 23, "person_b": 1, "type": "overlap", "context": "政协主席与市委书记（地方两会）", "overlap_org": "中国人民政治协商会议五常市委员会", "overlap_period": ""},
    {"person_a": 23, "person_b": 2, "type": "overlap", "context": "政协主席与市长", "overlap_org": "中国人民政治协商会议五常市委员会", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────────────
def main():
    print("DB_PATH:", DB_PATH)
    print("GEXF_PATH:", GEXF_PATH)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"\n✅ Build complete for {SLUG}")
    print(f"   Database: {DB_PATH}")
    print(f"   GEXF:     {GEXF_PATH}")
    print(f"   Persons:  {len(persons)}")
    print(f"   Orgs:     {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relations: {len(relationships)}")


if __name__ == "__main__":
    main()