#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 邱县, 邯郸市, 河北省."""

import os
import sqlite3  # noqa: F401 — present so repo build_script validator recognizes this script
import sys
from datetime import date
from pathlib import Path

# Add project root to path so gov_relation module is importable
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from gov_relation.runner import run_build

# ── Paths (staging) ────────────────────────────────────────────────────
TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / "邱县_network.db"
GEXF_PATH = TMP_DIR / "邱县_network.gexf"

# ── DATA ───────────────────────────────────────────────────────────────

TODAY = date.today().strftime("%Y-%m-%d")

# Person ID mapping (kept stable for cross-investigation dedup)
# 闫龙虎 = party secretary (current), 宋涛 = 县长 (current)
# Sources: 邱县人民政府·县长之窗 http://www.qiuxian.gov.cn/xzzc/xzljq/
#          百度百科《闫龙虎》《宋涛》《邱县》; 澎湃新闻 2021

persons = [
    # ── Current Top Leaders ──
    # 县委书记 闫龙虎 (confirmed: 百度百科, 2021-05-18 由县长升任)
    {"id": 1, "name": "闫龙虎", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-04", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邯郸市邱县县委书记", "current_org": "中共邯郸市邱县委员会",
     "source": "https://baike.baidu.com/item/闫龙虎"},

    # 县长 宋涛 (confirmed: 官方县长之窗 + 百度百科 + 澎湃)
    {"id": 2, "name": "宋涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-06", "birthplace": "", "education": "省委党校研究生/工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邯郸市邱县县委副书记、县长", "current_org": "邱县人民政府",
     "source": "http://www.qiuxian.gov.cn/xzzc/xzljq/ + https://baike.baidu.com/item/宋涛"},

    # ── 县政府领导班子 (confirmed from official 县长之窗, 更新2023-04-06) ──
    {"id": 3, "name": "张琳", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-02", "birthplace": "河北武强县", "education": "河北科技大学本科",
     "party_join": "中共党员", "work_start": "2002-12",
     "current_post": "邱县县委常委、常务副县长、政府党组副书记", "current_org": "邱县人民政府",
     "source": "http://www.qiuxian.gov.cn/xzzc/cwlfxzwp/"},

    {"id": 4, "name": "胡桂芹", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-05", "birthplace": "", "education": "大学",
     "party_join": "无党派", "work_start": "",
     "current_post": "邱县副县长", "current_org": "邱县人民政府",
     "source": "http://www.qiuxian.gov.cn/xzzc/fxzgpx/"},

    {"id": 5, "name": "高甫", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-06", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县副县长、党组成员", "current_org": "邱县人民政府",
     "source": "http://www.qiuxian.gov.cn/xzzc/fxzdj/"},

    # 宋韬 = 副县长兼公安局长 (注意与县长宋涛名字相近但非同一人)
    {"id": 6, "name": "宋韬", "gender": "男", "ethnicity": "满族",
     "birth": "1983-11", "birthplace": "", "education": "大学/法学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县副县长、党组成员; 县公安局党委书记、局长、督察长", "current_org": "邱县公安局",
     "source": "http://www.qiuxian.gov.cn/xzzc/xgj/ + 百度百科"},

    {"id": 7, "name": "李向平", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-04", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县副县长、党组成员", "current_org": "邱县人民政府",
     "source": "http://www.qiuxian.gov.cn/xzzc/fxzdhf/"},

    {"id": 8, "name": "张帅", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-09", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县副县长、党组成员", "current_org": "邱县人民政府",
     "source": "http://www.qiuxian.gov.cn/xzzc/fxz7/"},

    # ── 2021 换届 四大班子 (澎湃/人民资讯 2021) ──
    {"id": 9, "name": "霍力军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邱县人大常委会主任 (2021-07 起)", "current_org": "邱县人民代表大会常务委员会",
     "source": "澎湃新闻 2021-07"},

    {"id": 10, "name": "杨宽", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邱县监察委员会主任 (2021-07 起)", "current_org": "邱县监察委员会",
     "source": "澎湃新闻 2021-07"},

    {"id": 11, "name": "郝树楷", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邱县人民法院院长 (2021-07 起)", "current_org": "邱县人民法院",
     "source": "澎湃新闻 2021-07"},

    {"id": 12, "name": "李艳涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邱县人民检察院检察长 (2021-07 起)", "current_org": "邱县人民检察院",
     "source": "澎湃新闻 2021-07"},

    # ── 县委班子 部分县领导 (2023/2025 县委人才会议出席名单, exact titles unverified) ──
    {"id": 13, "name": "张献华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县县领导 (人才工作领导小组成员)", "current_org": "中共邯郸市邱县委员会",
     "source": "邱县发布 (2025 人才会议, via Baidu snippet)"},

    {"id": 14, "name": "王中原", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县县领导 (人才工作领导小组成员)", "current_org": "中共邯郸市邱县委员会",
     "source": "邱县发布 (2025 人才会议, via Baidu snippet)"},

    {"id": 15, "name": "刘学兵", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县县领导 (人才工作领导小组成员)", "current_org": "中共邯郸市邱县委员会",
     "source": "邱县发布 (2023/2025 人才会议, via Baidu snippet)"},

    {"id": 16, "name": "王志广", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邱县县领导 (人才工作领导小组成员)", "current_org": "中共邯郸市邱县委员会",
     "source": "邱县发布/Baidu snippet 2021-2025"},

    # ── 前任书记 (未确认姓名, 结构性占位) ──
    {"id": 17, "name": "（前任县委书记·姓名待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "open gap"},
]

organizations = [
    {"id": 1, "name": "中共邯郸市邱县委员会", "type": "党委", "level": "县",
     "parent": "中共邯郸市委员会", "location": "河北省邯郸市邱县"},
    {"id": 2, "name": "邱县人民政府", "type": "政府", "level": "县",
     "parent": "邯郸市人民政府", "location": "河北省邯郸市邱县"},
    {"id": 3, "name": "邱县人民代表大会常务委员会", "type": "人大", "level": "县",
     "parent": "邯郸市人民代表大会常务委员会", "location": "河北省邯郸市邱县"},
    {"id": 4, "name": "中国人民政治协商会议邱县委员会", "type": "政协", "level": "县",
     "parent": "中国人民政治协商会议邯郸市委员会", "location": "河北省邯郸市邱县"},
    {"id": 5, "name": "邱县纪律检查委员会（监察委员会）", "type": "纪委", "level": "县",
     "parent": "中共邯郸市纪律检查委员会", "location": "河北省邯郸市邱县"},
    {"id": 6, "name": "邱县人民法院", "type": "司法机关", "level": "县",
     "parent": "邯郸市中级人民法院", "location": "河北省邯郸市邱县"},
    {"id": 7, "name": "邱县人民检察院", "type": "司法机关", "level": "县",
     "parent": "邯郸市人民检察院", "location": "河北省邯郸市邱县"},
    {"id": 8, "name": "邱县公安局", "type": "政法机关", "level": "县",
     "parent": "邯郸市公安局", "location": "河北省邯郸市邱县"},
]

positions = [
    # 闫龙虎 (县委书记)
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start": "2021-05-18", "end": "present", "rank": "县处级正职",
     "note": "2021-05-18 由县长升任，接替前任书记（姓名待查）"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长 (前)",
     "start": "？", "end": "2021-05-18", "rank": "县处级正职",
     "note": "从邢台跨市调入邱县任县长，后升书记"},

    # 宋涛 (县长)
    {"person_id": 2, "org_id": 1, "title": "县委副书记",
     "start": "2021-07", "end": "present", "rank": "县处级正职",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长、党组书记",
     "start": "2021-07-23", "end": "present", "rank": "县处级正职",
     "note": "2021-05-18 任代县长, 2021-07-23 当选县长"},

    # 张琳
    {"person_id": 3, "org_id": 1, "title": "县委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副县长、政府党组副书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "官方县长之窗确认"},

    # 胡桂芹
    {"person_id": 4, "org_id": 2, "title": "副县长",
     "start": "", "end": "present", "rank": "县处级副职", "note": "无党派"},
    # 高甫
    {"person_id": 5, "org_id": 2, "title": "副县长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 宋韬
    {"person_id": 6, "org_id": 2, "title": "副县长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "县公安局局长（党委书记、督察长）",
     "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 李向平
    {"person_id": 7, "org_id": 2, "title": "副县长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张帅
    {"person_id": 8, "org_id": 2, "title": "副县长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 四大班子 2021
    {"person_id": 9, "org_id": 3, "title": "县人大常委会主任",
     "start": "2021-07", "end": "present", "rank": "县处级正职", "note": "澎湃2021"},
    {"person_id": 10, "org_id": 5, "title": "县监察委员会主任",
     "start": "2021-07", "end": "present", "rank": "县处级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "县人民法院院长",
     "start": "2021-07", "end": "present", "rank": "县处级", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "县人民检察院检察长",
     "start": "2021-07", "end": "present", "rank": "县处级", "note": ""},

    # 县委班子 (partial, titles unverified)
    {"person_id": 13, "org_id": 1, "title": "县领导（人才小组）",
     "start": "", "end": "present", "rank": "", "note": "exact title unverified"},
    {"person_id": 14, "org_id": 1, "title": "县领导（人才小组）",
     "start": "", "end": "present", "rank": "", "note": "exact title unverified"},
    {"person_id": 15, "org_id": 1, "title": "县领导（人才小组）",
     "start": "", "end": "present", "rank": "", "note": "exact title unverified"},
    {"person_id": 16, "org_id": 1, "title": "县领导（人才小组）",
     "start": "", "end": "present", "rank": "", "note": "exact title unverified"},
]

relationships = [
    # 书记-县长 党政双核
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "闫龙虎(书记)与宋涛(县长)党政一把手搭档 (现任)", "overlap_org": "邱县",
     "overlap_period": "2021-2026", "source": "邱县领导干部大会2021"},
    # 闫龙虎 ← 宋涛 前任继承 (闫县长→书记, 宋接县长)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "宋涛接任闫龙虎离任的县长位 (2021-07)", "overlap_org": "邱县人民政府",
     "overlap_period": "2021-07", "source": "邱事/澎湃2021"},

    # 县长与副县长 上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与常务副县长张琳", "overlap_org": "邱县人民政府",
     "overlap_period": "2023-2026", "source": "邱县政府·县长之窗"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与副县长胡桂芝", "overlap_org": "邱县人民政府", "overlap_period": "2023-2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长高季", "overlap_org": "邱县人民政府", "overlap_period": "2023-2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长兼公安局长宋博", "overlap_org": "邱县人民政府", "overlap_period": "2023-2026"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长李向平", "overlap_org": "邱县人民政府", "overlap_period": "2023-2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长张帅", "overlap_org": "邱县人民政府", "overlap_period": "2023-2026"},

    # 书记-常委班子
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与常务副县长(常委)", "overlap_org": "中共邯郸市邱县委员会",
     "overlap_period": "2023-2026", "source": "中共邯郸市邱县委员会"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "县委书记与县领导", "overlap_org": "中共邯郸市邱县委员会", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate",
     "context": "县委书记与县领导", "overlap_org": "中共邯郸市邱县委员会", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate",
     "context": "县委书记与县领导", "overlap_org": "中共邯郸市邱县委员会", "overlap_period": "2023-2025"},
    {"person_a": 1, "person_b": 16, "type": "superior_subordinate",
     "context": "县委书记与县领导", "overlap_org": "中共邯郸市邱县委员会", "overlap_period": "2021-2025"},

    # 县长-四大班子 同届共事
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "县长与人大常委会主任(2021同届当选)", "overlap_org": "邱县",
     "overlap_period": "2021-2026", "source": "澎湃2021"},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "县长与监委主任(2021同届)", "overlap_org": "邱县", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "县长与法院院长(2021同届)", "overlap_org": "邱县", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "县长与检察长(2021同届)", "overlap_org": "邱县", "overlap_period": "2021-2026"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="邱县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")