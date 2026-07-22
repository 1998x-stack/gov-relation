#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 广州市白云区 leadership network.

Data sources:
- www.by.gov.cn (official government website)
- 领导之窗 (leadership window): https://www.by.gov.cn/zwgk/ldzc/
- News articles from 白云时事

Information currency: 2026-07 (current as of July 2026)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "白云区"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: sequential numeric IDs
persons = [
    # ── 区委领导班子 (District Party Committee) ──
    {
        "id": 1, "name": "洪谦", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共广州市白云区委员会",
        "source": "https://www.by.gov.cn/ywdt/zwyw/content/post_10903826.html",
    },
    {
        "id": 2, "name": "邱之仲", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/zwgk/ldzc/qzf/qzz/index.html",
    },
    {
        "id": 3, "name": "周军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/postmeta/i/25190.json",
    },
    {
        "id": 4, "name": "刘国华", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共广州市白云区委统战部",
        "source": "https://www.by.gov.cn/zwgk/ldzc/qzf/ldzclgh/",
    },
    {
        "id": 5, "name": "蔡鹏浩", "gender": "", "ethnicity": "",
        "birth": "1975-11", "birthplace": "广东汕头", "education": "省委党校研究生",
        "party_join": "1996-12", "work_start": "1997-07",
        "current_post": "区委常委、区纪委书记",
        "current_org": "中共广州市白云区纪律检查委员会",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    {
        "id": 6, "name": "唐晚华", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-03", "birthplace": "湖南邵东", "education": "大学",
        "party_join": "1993-01", "work_start": "1991-12",
        "current_post": "区委常委、区武装部部长",
        "current_org": "广州市白云区人民武装部",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    {
        "id": 7, "name": "陈玉云", "gender": "女", "ethnicity": "汉族",
        "birth": "1977-06", "birthplace": "广东汕头", "education": "中央党校研究生",
        "party_join": "1999-01", "work_start": "2001-07",
        "current_post": "区委常委、钟落潭镇党委书记",
        "current_org": "中共广州市白云区钟落潭镇委员会",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    {
        "id": 8, "name": "杨颜泽", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-08", "birthplace": "广东大埔", "education": "研究生/管理学硕士",
        "party_join": "1997-10", "work_start": "1993-08",
        "current_post": "区委常委、区委办公室主任",
        "current_org": "中共广州市白云区委办公室",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    # ── 区政府领导班子 (District Government) ──
    {
        "id": 9, "name": "刘导平", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/zwgk/ldzc/qzf/ldp/",
    },
    {
        "id": 10, "name": "葛林飞", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/zwgk/ldzc/qzf/glf/",
    },
    {
        "id": 11, "name": "陈永俊", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/zwgk/ldzc/qzf/cyj/",
    },
    {
        "id": 12, "name": "王晓杰", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/zwgk/ldzc/qzf/wxj/",
    },
    {
        "id": 13, "name": "刘懿", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/zwgk/ldzc/qzf/ly/",
    },
    # ── 人大 & 政协 leaders ──
    {
        "id": 14, "name": "张建如", "gender": "男", "ethnicity": "汉族",
        "birth": "1965-10", "birthplace": "江西新干", "education": "研究生/哲学博士",
        "party_join": "1998-06", "work_start": "1991-04",
        "current_post": "区人大常委会主任",
        "current_org": "广州市白云区人大常委会",
        "source": "https://www.by.gov.cn/ywdt/zwyw/content/post_10903837.html",
    },
    {
        "id": 15, "name": "袁东华", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议广州市白云区委员会",
        "source": "https://www.by.gov.cn/ywdt/zwyw/content/post_10903837.html",
    },
    # ── 前任领导 (Former leaders from 2020 leadership page data) ──
    {
        "id": 16, "name": "赵军明", "gender": "男", "ethnicity": "汉族",
        "birth": "1965", "birthplace": "浙江诸暨", "education": "研究生/工学硕士",
        "party_join": "1991-05", "work_start": "1990-07",
        "current_post": "前任区委书记(已离任)",
        "current_org": "中共广州市白云区委员会",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    {
        "id": 17, "name": "苏小澎", "gender": "男", "ethnicity": "汉族",
        "birth": "1962-03", "birthplace": "广东汕尾", "education": "省社科院研究生",
        "party_join": "中共党员", "work_start": "1985-01",
        "current_post": "前任区长(已离任)",
        "current_org": "广州市白云区人民政府",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    # ── 原区委常委 (former standing committee members from 2020 data) ──
    {
        "id": 18, "name": "谢素琪", "gender": "女", "ethnicity": "汉族",
        "birth": "1965-04", "birthplace": "广东汕头", "education": "省社科院在职研究生/农业推广硕士",
        "party_join": "1991-06", "work_start": "1985-08",
        "current_post": "前任区委常委、统战部部长(已离任)",
        "current_org": "中共广州市白云区委统战部",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    {
        "id": 19, "name": "吴扬", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-03", "birthplace": "广东饶平", "education": "研究生/管理学硕士",
        "party_join": "1995-01", "work_start": "1992-07",
        "current_post": "前任区委常委（已离任）",
        "current_org": "中共广州市白云区委员会",
        "source": "https://www.by.gov.cn/postmeta/i/25185.json",
    },
    {
        "id": 20, "name": "张叶东", "gender": "男", "ethnicity": "汉族",
        "birth": "1961-12", "birthplace": "广西兴安", "education": "中央党校大学",
        "party_join": "1983-01", "work_start": "1979-12",
        "current_post": "前任区委常委、区纪委书记(已离任)",
        "current_org": "中共广州市白云区纪律检查委员会",
        "source": "https://www.by.gov.cn/postmeta/i/25186.json",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1, "name": "中共广州市白云区委员会",
        "type": "党委", "level": "副厅级", "parent": "中共广州市委",
        "location": "广东省广州市白云区",
    },
    {
        "id": 2, "name": "广州市白云区人民政府",
        "type": "政府", "level": "副厅级", "parent": "广州市人民政府",
        "location": "广东省广州市白云区",
    },
    {
        "id": 3, "name": "中共广州市白云区委统战部",
        "type": "党委部门", "level": "正处级", "parent": "中共广州市白云区委员会",
        "location": "广东省广州市白云区",
    },
    {
        "id": 4, "name": "中共广州市白云区纪律检查委员会",
        "type": "纪委", "level": "副厅级", "parent": "中共广州市纪委",
        "location": "广东省广州市白云区",
    },
    {
        "id": 5, "name": "广州市白云区人民武装部",
        "type": "事业单位", "level": "正处级", "parent": "广州警备区",
        "location": "广东省广州市白云区",
    },
    {
        "id": 6, "name": "中共广州市白云区钟落潭镇委员会",
        "type": "党委", "level": "正处级", "parent": "中共广州市白云区委员会",
        "location": "广东省广州市白云区钟落潭镇",
    },
    {
        "id": 7, "name": "中共广州市白云区委办公室",
        "type": "党委部门", "level": "正处级", "parent": "中共广州市白云区委员会",
        "location": "广东省广州市白云区",
    },
    {
        "id": 8, "name": "广州市白云区人大常委会",
        "type": "人大", "level": "副厅级", "parent": "广州市人大常委会",
        "location": "广东省广州市白云区",
    },
    {
        "id": 9, "name": "中国人民政治协商会议广州市白云区委员会",
        "type": "政协", "level": "副厅级", "parent": "政协广州市委员会",
        "location": "广东省广州市白云区",
    },
    {
        "id": 10, "name": "白云区委组织部（原）",
        "type": "党委部门", "level": "正处级", "parent": "中共广州市白云区委员会",
        "location": "广东省广州市白云区",
    },
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 洪谦 — 区委书记 (current)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "~2024/2025", "end": "至今", "rank": "副厅级", "note": "现任区委书记，主持区委全面工作"},
    # 邱之仲 — 区长 (current)
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2026-01", "end": "至今", "rank": "副厅级", "note": "2026年1月任代区长，后转正"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "~2025", "end": "至今", "rank": "副厅级", "note": ""},
    # 周军 — 区委常委、常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "", "end": "至今", "rank": "正处级", "note": "区委常委、区政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 刘国华 — 区委常委、统战部部长
    {"person_id": 4, "org_id": 3, "title": "统战部部长", "start": "", "end": "至今", "rank": "正处级", "note": "区委常委"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 蔡鹏浩 — 区委常委、区纪委书记
    {"person_id": 5, "org_id": 4, "title": "区纪委书记", "start": "", "end": "至今", "rank": "正处级", "note": "区委常委"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 唐晚华 — 区委常委、武装部部长
    {"person_id": 6, "org_id": 5, "title": "区武装部部长", "start": "", "end": "至今", "rank": "正处级", "note": "区委常委"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 陈玉云 — 区委常委、钟落潭镇党委书记
    {"person_id": 7, "org_id": 6, "title": "镇党委书记", "start": "", "end": "至今", "rank": "正处级", "note": "区委常委兼"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 杨颜泽 — 区委常委、区委办公室主任
    {"person_id": 8, "org_id": 7, "title": "区委办公室主任", "start": "", "end": "至今", "rank": "正处级", "note": "区委常委"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副局级", "note": "区政府党组成员"},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副局级", "note": "区政府党组成员，负责公安"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副局级", "note": "负责司法、民政、文化等"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副局级", "note": "区政府党组成员"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副局级", "note": "区政府党组成员"},
    # 人大 & 政协
    {"person_id": 14, "org_id": 8, "title": "区人大常委会主任", "start": "", "end": "至今", "rank": "正局级", "note": "曾任区委常委、组织部部长"},
    {"person_id": 15, "org_id": 9, "title": "区政协主席", "start": "", "end": "至今", "rank": "正局级", "note": ""},
    # 前任领导
    {"person_id": 16, "org_id": 1, "title": "区委书记", "start": "2017-03", "end": "~2024", "rank": "副厅级", "note": "前任区委书记，2017年3月起任职"},
    {"person_id": 17, "org_id": 2, "title": "区长", "start": "2016-03", "end": "~2025", "rank": "副厅级", "note": "前任区长"},
    {"person_id": 18, "org_id": 3, "title": "统战部部长", "start": "", "end": "~2024", "rank": "正处级", "note": "前任区委常委、统战部部长"},
    {"person_id": 19, "org_id": 1, "title": "区委常委", "start": "", "end": "~2024", "rank": "正处级", "note": "前任区委常委"},
    {"person_id": 20, "org_id": 4, "title": "区纪委书记", "start": "", "end": "~2024", "rank": "正处级", "note": "前任区委常委、区纪委书记"},
]

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    # 区委书记—区长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长",
     "overlap_org": "白云区四套班子", "overlap_period": "2025—"},
    # 区委书记—前任书记（前后任）
    {"person_a": 16, "person_b": 1, "type": "前后任", "context": "前任区委书记→现任区委书记",
     "overlap_org": "中共白云区委", "overlap_period": "~2024交接"},
    # 区长—前任区长（前后任）
    {"person_a": 17, "person_b": 2, "type": "前后任", "context": "前任区长→现任区长",
     "overlap_org": "白云区政府", "overlap_period": "~2025交接"},
    # 区长—常务副区长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长—常务副区长",
     "overlap_org": "白云区政府", "overlap_period": ""},
    # 区长—副区长
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长—副区长",
     "overlap_org": "白云区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长—副区长",
     "overlap_org": "白云区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长—副区长",
     "overlap_org": "白云区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长—副区长",
     "overlap_org": "白云区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长—副区长",
     "overlap_org": "白云区政府", "overlap_period": ""},
    # 区委书记—人大主任
    {"person_a": 1, "person_b": 14, "type": "党政—人大", "context": "区委书记—人大常委会主任",
     "overlap_org": "白云区四套班子", "overlap_period": ""},
    # 区委书记—政协主席
    {"person_a": 1, "person_b": 15, "type": "党政—政协", "context": "区委书记—政协主席",
     "overlap_org": "白云区四套班子", "overlap_period": ""},
    # 区委常委内部同僚关系
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "区委常委",
     "overlap_org": "白云区委常委会", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "区委常委",
     "overlap_org": "白云区委常委会", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "区委常委",
     "overlap_org": "白云区委常委会", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "区委常委",
     "overlap_org": "白云区委常委会", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "区委常委",
     "overlap_org": "白云区委常委会", "overlap_period": ""},
    # 张建如（原组织部长→人大主任）与区委关系
    {"person_a": 14, "person_b": 1, "type": "党政—人大", "context": "人大主任—区委书记",
     "overlap_org": "白云区四套班子", "overlap_period": ""},
]

# ── Run Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "白云区_network.db",
        gexf_path=GRAPH_DIR / "白云区_network.gexf",
        overwrite=True,
    )
    print("Done: 广州市白云区 network built.")
