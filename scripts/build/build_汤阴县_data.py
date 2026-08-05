#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汤阴县 leadership network.

调查日期: 2026-08-05
信息来源: 汤阴县人民政府网站 (tangyin.gov.cn 政府领导/汤阴要闻)
调查级别: 县
目标人物: 县委书记 路录平、县长 胡玮
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
# data/tmp/henan_汤阴县/ -> repo root requires 3 levels up
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "汤阴县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "汤阴县_network.gexf")

SLUG = "河南省安阳市汤阴县"

# ── PERSON ID 约定 ──────────────────────────────────────────────────
# 使用 person_id 一致：tangyin_<name>
PID = {
    "路录平": 1,
    "胡玮": 2,
    "叶丁": 3,
    "石超敏": 4,
    "李锦辉": 5,
    "陈利勇": 6,
    "郭晓彤": 7,
    "石磊": 8,
    "姬卫军": 9,
    "刘全生": 10,
    "张存富": 11,
    "马卫红": 12,
    "杨波": 13,
    "朱震晓": 14,
    "张海波": 15,
    "张文有": 16,
    "王鹏": 17,
}

# ── ORGANIZATIONS ─────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共汤阴县委员会", "type": "党委", "level": "县处级", "parent": "中共安阳市委", "location": "河南省安阳市汤阴县", "source": ""},
    {"id": 2, "name": "汤阴县人民政府", "type": "政府", "level": "县处级", "parent": "安阳市人民政府", "location": "河南省安阳市汤阴县", "source": ""},
    {"id": 3, "name": "汤阴县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南省安阳市汤阴县", "source": ""},
    {"id": 4, "name": "中国人民政治协商会议汤阴县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河南省安阳市汤阴县", "source": ""},
    {"id": 5, "name": "汤阴县公安局", "type": "政府", "level": "乡科级", "parent": "汤阴县人民政府", "location": "河南省安阳市汤阴县", "source": ""},
]

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══ 县委领导 (Party Committee) ═══
    {
        "id": 1, "name": "路录平", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共汤阴县委书记",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/08-04/3655023.html (县政府网 汤阴要闻 2026-08-04)",
    },
    {
        "id": 2, "name": "胡玮", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-02", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "汤阴县委副书记、县长、县政府党组书记",
        "current_org": "汤阴县人民政府",
        "source": "https://www.tangyin.gov.cn/2025/05-12/3520560.html (县政府网 领导简介 2026-07-22)",
    },
    # ═══ 县政府领导 ═══
    {
        "id": 3, "name": "叶丁", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-08", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "汤阴县委常委、县政府副县长、党组副书记",
        "current_org": "汤阴县人民政府",
        "source": "https://www.tangyin.gov.cn/2025/05-12/3520562.html (县政府网 领导简介 2025-07-22)",
    },
    {
        "id": 4, "name": "石超敏", "gender": "男", "ethnicity": "汉族",
        "birth": "1984-09", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "汤阴县委常委、县政府副县长",
        "current_org": "汤阴县人民政府",
        "source": "https://www.tangyin.gov.cn/2025/05-12/3520563.html (县政府网 领导简介 2025-07-22)",
    },
    {
        "id": 5, "name": "李锦辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-09", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "汤阴县人民政府副县长、县公安局局长",
        "current_org": "汤阴县公安局",
        "source": "https://www.tangyin.gov.cn/2025/05-12/3520565.html (县政府网 领导简介)",
    },
    {
        "id": 6, "name": "陈利勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-08", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "汤阴县人民政府副县长",
        "current_org": "汤阴县人民政府",
        "source": "https://www.tangyin.gov.cn/2025/05-12/3520566.html (县政府网 领导简介)",
    },
    {
        "id": 7, "name": "郭晓彤", "gender": "女", "ethnicity": "汉族",
        "birth": "1979-10", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "汤阴县人民政府副县长",
        "current_org": "汤阴县人民政府",
        "source": "https://www.tangyin.gov.cn/2025/05-12/3520567.html (县政府网 领导简介)",
    },
    # ═══ 其他县领导（副处级，具体职级待进一步公开渠道确认）═══
    {
        "id": 8, "name": "石磊", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "汤阴县县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654575.html (慈善一日捐工作会与会县领导名单 2026-07-31)",
    },
    {
        "id": 9, "name": "姬卫军", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654575.html",
    },
    {
        "id": 10, "name": "刘全生", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654575.html",
    },
    {
        "id": 11, "name": "张存富", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654575.html",
    },
    {
        "id": 12, "name": "马卫红", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654575.html",
    },
    {
        "id": 13, "name": "杨波", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654575.html",
    },
    {
        "id": 14, "name": "朱震晓", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654575.html",
    },
    {
        "id": 15, "name": "张海波", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/07-31/3654576.html",
    },
    {
        "id": 16, "name": "张文有", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/08-04/3655023.html",
    },
    {
        "id": 17, "name": "王鹏", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导（副县级）",
        "current_org": "中共汤阴县委员会",
        "source": "https://www.tangyin.gov.cn/2026/08-04/3655023.html",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "中共汤阴县委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "现状截至 2026-08; 十五届县委 (2026 年党代会后) 连任/任职"},
    {"person_id": 2, "org_id": 1, "title": "汤阴县委副书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "汤阴县县长、县政府党组书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "汤阴县委常委、县政府常务副县长、党组副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "汤阴县委常委、县政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "汤阴县公安局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼副县长"},
    {"person_id": 5, "org_id": 2, "title": "汤阴县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "汤阴县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "汤阴县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "领导关系", "context": "县委书记与县长搭档，共同主持县党政工作、慈善大会同期出席", "overlap_org": "中共汤阴县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长（党组副书记）", "overlap_org": "汤阴县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与副县长（县委常委）", "overlap_org": "汤阴县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "汤阴县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "汤阴县人民政府", "overlap_period": "至今"},
]

# ── BUILD ──────────────────────────────────────────────────────────
def build() -> None:
    from gov_relation.runner import run_build

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

    # 打印统计
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    print("persons: ", conn.execute("select count(*) from persons").fetchone()[0])
    print("organizations: ", conn.execute("select count(*) from organizations").fetchone()[0])
    print("positions: ", conn.execute("select count(*) from positions").fetchone()[0])
    print("relationships: ", conn.execute("select count(*) from relationships").fetchone()[0])
    conn.close()
    print("DB_PATH:", DB_PATH)
    print("GEXF_PATH:", GEXF_PATH)


if __name__ == "__main__":
    build()