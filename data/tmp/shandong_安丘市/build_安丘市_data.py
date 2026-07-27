#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Anqiu City (安丘市) leadership network.

安丘市 is a county-level city (县级市) under Weifang City (潍坊市), Shandong Province (山东省).
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ── DATA ─────────────────────────────────────────────────────────────

# Person IDs: 1-10 for 安丘 leaders
persons = [
    # ══ Top Leaders ══
    {
        "id": 1,
        "name": "乔日升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市委书记",
        "current_org": "中共安丘市委员会",
        "source": "http://www.anqiu.gov.cn/yw/snyw/202607/t20260716_737774.html",
    },
    {
        "id": 2,
        "name": "谭明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "",
        "education": "工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市委副书记、市长",
        "current_org": "安丘市人民政府",
        "source": "http://www.anqiu.gov.cn/xxgk/xxgk/szfld/tm/",
    },
    {
        "id": 3,
        "name": "王强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市委副书记、副市长",
        "current_org": "安丘市人民政府",
        "source": "http://www.anqiu.gov.cn/xxgk/xxgk/szfld/wq/",
    },
    # ══ Standing Committee Members (市委常委) ══
    {
        "id": 4,
        "name": "于浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-09",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市委常委、常务副市长",
        "current_org": "安丘市人民政府",
        "source": "http://www.anqiu.gov.cn/xxgk/xxgk/szfld/yh/",
    },
    {
        "id": 5,
        "name": "刘娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "",
        "education": "公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市委常委、副市长",
        "current_org": "安丘市人民政府",
        "source": "http://www.anqiu.gov.cn/xxgk/xxgk/szfld/ln/",
    },
    # ══ Deputy Mayors (副市长) ══
    {
        "id": 6,
        "name": "王磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市副市长、市公安局局长",
        "current_org": "安丘市人民政府",
        "source": "http://www.anqiu.gov.cn/xxgk/xxgk/szfld/wl/",
    },
    {
        "id": 7,
        "name": "张海宁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985-10",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市副市长",
        "current_org": "安丘市人民政府",
        "source": "http://www.anqiu.gov.cn/xxgk/xxgk/szfld/zhn/",
    },
    {
        "id": 8,
        "name": "朱伟欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-07",
        "birthplace": "",
        "education": "工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市副市长",
        "current_org": "安丘市人民政府",
        "source": "http://www.anqiu.gov.cn/xxgk/xxgk/szfld/zwx/",
    },
    # ══ Other Leaders Mentioned in News (unconfirmed exact roles) ══
    {
        "id": 9,
        "name": "冯启波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市领导",
        "current_org": "安丘市",
        "source": "http://www.anqiu.gov.cn/yw/snyw/202607/t20260716_737774.html",
    },
    {
        "id": 10,
        "name": "孔德奎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市领导",
        "current_org": "安丘市",
        "source": "http://www.anqiu.gov.cn/yw/snyw/202607/t20260716_737774.html",
    },
    {
        "id": 11,
        "name": "孙志堂",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安丘市领导",
        "current_org": "安丘市",
        "source": "http://www.anqiu.gov.cn/yw/snyw/202607/t20260716_737774.html",
    },
    {
        "id": 12,
        "name": "王洪书",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安丘市领导",
        "current_org": "安丘市",
        "source": "http://www.anqiu.gov.cn/yw/snyw/202607/t20260716_737774.html",
    },
    {
        "id": 13,
        "name": "任瑞波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安丘市领导",
        "current_org": "安丘市",
        "source": "http://www.anqiu.gov.cn/yw/snyw/202607/t20260716_737774.html",
    },
]

organizations = [
    {"id": 1, "name": "中共安丘市委员会", "type": "党委", "level": "县级", "parent": "中共潍坊市委员会", "location": "安丘市"},
    {"id": 2, "name": "安丘市人民政府", "type": "政府", "level": "县级", "parent": "潍坊市人民政府", "location": "安丘市"},
    {"id": 3, "name": "安丘市公安局", "type": "政府", "level": "正科级", "parent": "安丘市人民政府", "location": "安丘市"},
]

# Positions: person_id, org_id mapping
positions = [
    # 乔日升 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "安丘市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "书记主持市委全面工作"},
    # 谭明 - Mayor
    {"person_id": 2, "org_id": 2, "title": "安丘市市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "安丘市委副书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 王强 - Deputy Secretary + Deputy Mayor
    {"person_id": 3, "org_id": 1, "title": "安丘市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "安丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管自然资源和规划、住建、城管、综合执法"},
    # 于浩 - Executive Deputy Mayor
    {"person_id": 4, "org_id": 1, "title": "安丘市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "安丘市常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管发改、人社、金融、应急、统计、审批"},
    # 刘娜 - Deputy Mayor + Standing Committee
    {"person_id": 5, "org_id": 1, "title": "安丘市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "安丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管农业农村、水利、乡村振兴、市场监管、文旅"},
    # 王磊 - Deputy Mayor + Public Security
    {"person_id": 6, "org_id": 2, "title": "安丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "安丘市公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 张海宁 - Deputy Mayor
    {"person_id": 7, "org_id": 2, "title": "安丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管工信、商务、卫健、医保、开发区、大数据"},
    # 朱伟欣 - Deputy Mayor
    {"person_id": 8, "org_id": 2, "title": "安丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管招商引资、科技、教育、体育、生态环境"},
    # Other leaders (placeholder positions)
    {"person_id": 9, "org_id": 1, "title": "安丘市领导", "start_date": "", "end_date": "present", "rank": "", "note": "身份待确认"},
    {"person_id": 10, "org_id": 1, "title": "安丘市领导", "start_date": "", "end_date": "present", "rank": "", "note": "身份待确认"},
    {"person_id": 11, "org_id": 1, "title": "安丘市领导", "start_date": "", "end_date": "present", "rank": "", "note": "身份待确认"},
    {"person_id": 12, "org_id": 2, "title": "安丘市领导", "start_date": "", "end_date": "present", "rank": "", "note": "身份待确认"},
    {"person_id": 13, "org_id": 2, "title": "安丘市领导", "start_date": "", "end_date": "present", "rank": "", "note": "身份待确认"},
]

# Relationships between key leaders
relationships = [
    # 乔日升 - 谭明: 党政一把手共事关系
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "安丘市党政一把手", "overlap_org": "安丘市", "overlap_period": "2026-"},
    # 乔日升 - 王强: 书记+副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记与市委副书记", "overlap_org": "中共安丘市委员会", "overlap_period": "2026-"},
    # 谭明 - 王强: 市长+副市长/副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "市长/副市长与副书记", "overlap_org": "安丘市人民政府", "overlap_period": "2026-"},
    # 于浩 - 谭明: 常务副市长配合市长工作
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "常务副市长协助市长工作", "overlap_org": "安丘市人民政府", "overlap_period": "2026-"},
    # 于浩 - 刘娜: 同届市委常委+副市长
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同届市委常委、副市长", "overlap_org": "安丘市人民政府", "overlap_period": "2026-"},
    # 王磊 - 谭明: 公安局长兼副市长属市长分管
    {"person_a": 6, "person_b": 2, "type": "overlap", "context": "副市长与市长", "overlap_org": "安丘市人民政府", "overlap_period": "2026-"},
    # 张海宁 - 谭明
    {"person_a": 7, "person_b": 2, "type": "overlap", "context": "副市长与市长", "overlap_org": "安丘市人民政府", "overlap_period": "2026-"},
    # 朱伟欣 - 谭明
    {"person_a": 8, "person_b": 2, "type": "overlap", "context": "副市长与市长", "overlap_org": "安丘市人民政府", "overlap_period": "2026-"},
]


# ── BUILD ────────────────────────────────────────────────────────────

SLUG = "安丘市"
OUTPUT_DIR = PROJECT_ROOT / "data/tmp/shandong_安丘市"
DB_PATH = str(OUTPUT_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(OUTPUT_DIR / f"{SLUG}_network.gexf")

if __name__ == "__main__":
    # This imports sqlite3 via gov_relation.runner
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
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
