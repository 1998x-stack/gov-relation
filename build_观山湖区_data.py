#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 贵阳市观山湖区 leadership network.

Data sources:
- www.guanshanhu.gov.cn (official government website)
- 领导之窗 (leadership window)
- 360百科 for 罗杨 biography
- News articles from guanshanhu.gov.cn

Information currency: 2026-07 (current as of July 2026)
"""
import sys
import sqlite3
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "观山湖区"

DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

AS_OF = "2026-07-23"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # ── 区委 (District Party Committee) ──
    {
        "id": 1, "name": "罗杨", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-09", "birthplace": "四川富顺", "education": "大学/研究生（中央党校经济学）",
        "party_join": "1998-05", "work_start": "1995-08",
        "current_post": "区委书记",
        "current_org": "中共观山湖区委员会",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202503/t20250319_87204472.html",
    },
    {
        "id": 2, "name": "秦永康", "gender": "男", "ethnicity": "侗族",
        "birth": "1976-04", "birthplace": "", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "观山湖区人民政府",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202503/t20250319_87204471.html",
    },
    {
        "id": 3, "name": "王兴文", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记（专职）",
        "current_org": "中共观山湖区委员会",
        "source": "https://www.guanshanhu.gov.cn/xwzx/gshyw/202607/t20260720_90637845.html",
    },
    {
        "id": 4, "name": "赵砚飞", "gender": "女", "ethnicity": "汉族",
        "birth": "1982-05", "birthplace": "", "education": "在职研究生",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "观山湖区人民政府",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202503/t20250319_87204470.html",
    },
    # ── 区政府 (District Government) ──
    {
        "id": 5, "name": "吴勇", "gender": "男", "ethnicity": "苗族",
        "birth": "1975-01", "birthplace": "", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "观山湖区人民政府",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202503/t20250319_87204468.html",
    },
    {
        "id": 6, "name": "曹洋", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-07", "birthplace": "", "education": "中央党校大学",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "观山湖区人民政府",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202503/t20250319_87204467.html",
    },
    {
        "id": 7, "name": "杨波", "gender": "男", "ethnicity": "汉族",
        "birth": "1969-05", "birthplace": "", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "观山湖区人民政府",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202503/t20250319_87204456.html",
    },
    {
        "id": 8, "name": "耿立波", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-09", "birthplace": "", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "观山湖区人民政府",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202503/t20250319_87204455.html",
    },
    {
        "id": 9, "name": "朱应川", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-07", "birthplace": "", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "观山湖区人民政府",
        "source": "https://www.guanshanhu.gov.cn/zwgk/ldzc_5979020/202604/t20260410_89982549.html",
    },
    # ── 区人大 (People's Congress) ──
    {
        "id": 10, "name": "邱斌", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "观山湖区人民代表大会常务委员会",
        "source": "https://www.guanshanhu.gov.cn/xwzx/gshyw/202607/t20260720_90637845.html",
    },
    # ── 前任区委书记 (Predecessor) ──
    {
        "id": 11, "name": "汤辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1969-11", "birthplace": "江苏无锡", "education": "大学",
        "party_join": "1991-04", "work_start": "1991-08",
        "current_post": "安顺市委书记",
        "current_org": "中共安顺市委员会",
        "source": "https://baike.baidu.com/item/%E6%B1%A4%E8%BE%89/23293946",
    },
    # ── 前任区长 (Predecessor) ──
    {
        "id": 12, "name": "李毅", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "（前任区长）",
        "current_org": "",
        "source": "",
    },
]

# ── Organizations ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共观山湖区委员会", "type": "党委", "level": "县处级", "parent": "中共贵阳市委", "location": "贵阳市观山湖区"},
    {"id": 2, "name": "观山湖区人民政府", "type": "政府", "level": "县处级", "parent": "贵阳市人民政府", "location": "贵阳市观山湖区"},
    {"id": 3, "name": "观山湖区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "贵阳市人大常委会", "location": "贵阳市观山湖区"},
    {"id": 4, "name": "观山湖区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共观山湖区委员会", "location": "贵阳市观山湖区"},
    {"id": 5, "name": "政协观山湖区委员会", "type": "政协", "level": "县处级", "parent": "政协贵阳市委员会", "location": "贵阳市观山湖区"},
    {"id": 6, "name": "观山湖现代服务产业试验区", "type": "开发区", "level": "县处级", "parent": "贵阳市人民政府", "location": "贵阳市观山湖区"},
    {"id": 7, "name": "贵阳国家高新技术产业开发区", "type": "开发区", "level": "副厅级", "parent": "贵阳市人民政府", "location": "贵阳市"},
    {"id": 8, "name": "清镇市人民政府", "type": "政府", "level": "县处级", "parent": "贵阳市人民政府", "location": "贵阳市清镇市"},
    {"id": 9, "name": "观山湖区公安分局", "type": "政府", "level": "乡科级", "parent": "观山湖区人民政府", "location": "贵阳市观山湖区"},
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 罗杨 - 区委书记 (full career from 360百科)
    {"person_id": 1, "org_id": 99, "title": "西南政法大学法律系学习", "start_date": "1991-09", "end_date": "1995-08", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 99, "title": "贵阳市人大农村经济民族宗教委员会办公室科员", "start_date": "1995-08", "end_date": "1998-12", "rank": "", "note": "1996.05-1997.05在乌当区偏坡乡挂职任乡长助理"},
    {"person_id": 1, "org_id": 99, "title": "贵阳市人大选举任免联络委员会办公室副主任", "start_date": "1998-12", "end_date": "2001-12", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 99, "title": "贵阳市人大常委会办公厅人事处处长", "start_date": "2001-12", "end_date": "2003-07", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 99, "title": "贵阳市人大常委会办公厅秘书处处长", "start_date": "2003-07", "end_date": "2005-01", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 99, "title": "贵阳市人大常委会办公厅副县级干部、秘书处处长", "start_date": "2005-01", "end_date": "2005-03", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 99, "title": "贵阳市人大常委会办公厅副县级干部、信访处处长", "start_date": "2005-03", "end_date": "2006-09", "rank": "副县级", "note": "2005.09-2008.07中央党校经济学专业学习"},
    {"person_id": 1, "org_id": 8, "title": "清镇市人民政府副市长", "start_date": "2006-09", "end_date": "2009-07", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "清镇市委常委、副市长", "start_date": "2009-07", "end_date": "2012-08", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "清镇市委常委、常务副市长", "start_date": "2012-08", "end_date": "2014-11", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 99, "title": "贵阳金阳建设投资(集团)有限公司党委副书记、总经理", "start_date": "2014-11", "end_date": "2017-04", "rank": "正县级", "note": "企业任职"},
    {"person_id": 1, "org_id": 99, "title": "贵阳市城市建设投资(集团)有限公司党委书记、董事长", "start_date": "2017-04", "end_date": "2019-01", "rank": "正县级", "note": "企业任职"},
    {"person_id": 1, "org_id": 99, "title": "贵阳市交通投资发展集团有限公司党委书记、董事长", "start_date": "2019-01", "end_date": "2019-07", "rank": "正县级", "note": "企业任职"},
    {"person_id": 1, "org_id": 1, "title": "中共观山湖区委副书记、区长候选人", "start_date": "2019-07", "end_date": "2019-08", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "观山湖区人民政府副区长、代区长", "start_date": "2019-08", "end_date": "2019-09", "rank": "正县级", "note": "兼观山湖现代服务产业试验区党工委副书记、管委会主任"},
    {"person_id": 1, "org_id": 2, "title": "观山湖区人民政府区长", "start_date": "2019-09", "end_date": "2021-04", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中共观山湖区委书记", "start_date": "2021-04", "end_date": "", "rank": "正县级", "note": "兼观山湖现代服务产业试验区党工委书记、区百花新城建设开发办公室党委书记"},
    {"person_id": 1, "org_id": 7, "title": "贵阳国家高新技术开发区党工委书记", "start_date": "2023", "end_date": "", "rank": "副厅级", "note": "兼"},
    # 秦永康 - 区长
    {"person_id": 2, "org_id": 2, "title": "观山湖区人民政府区长", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "中共观山湖区委副书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "兼"},
    # 王兴文 - 专职副书记
    {"person_id": 3, "org_id": 1, "title": "中共观山湖区委副书记（专职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 赵砚飞 - 常务副区长
    {"person_id": 4, "org_id": 2, "title": "观山湖区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 吴勇
    {"person_id": 5, "org_id": 2, "title": "观山湖区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 曹洋
    {"person_id": 6, "org_id": 2, "title": "观山湖区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 杨波
    {"person_id": 7, "org_id": 2, "title": "观山湖区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 7, "org_id": 9, "title": "观山湖区公安分局党委书记、局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼"},
    # 耿立波
    {"person_id": 8, "org_id": 2, "title": "观山湖区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 朱应川
    {"person_id": 9, "org_id": 2, "title": "观山湖区人民政府副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # 邱斌 - 人大主任
    {"person_id": 10, "org_id": 3, "title": "观山湖区人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    # 汤辉 - 前任区委书记
    {"person_id": 11, "org_id": 1, "title": "中共观山湖区委书记", "start_date": "2014", "end_date": "2021-04", "rank": "正县级", "note": "前任"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # 罗杨 ↔ 秦永康 (书记-区长搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "罗杨（区委书记）与秦永康（区长）构成书记-区长搭档", "overlap_org": "中共观山湖区委员会/观山湖区人民政府", "overlap_period": "2021至今"},
    # 罗杨 ↔ 王兴文 (书记-副书记)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "罗杨（区委书记）与王兴文（专职副书记）在区委常委会共事", "overlap_org": "中共观山湖区委员会", "overlap_period": ""},
    # 罗杨 ↔ 赵砚飞 (书记-常务副区长)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "罗杨（区委书记）与赵砚飞（常务副区长）在区委常委会/区政府班子共事", "overlap_org": "中共观山湖区委员会/观山湖区人民政府", "overlap_period": ""},
    # 秦永康 ↔ 赵砚飞 (区长-常务副区长)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "秦永康（区长）与赵砚飞（常务副区长）在区政府班子共事", "overlap_org": "观山湖区人民政府", "overlap_period": ""},
    # 汤辉 → 罗杨 (前任区委书记-继任者)
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor", "context": "汤辉调任安顺市委书记后，罗杨接任观山湖区委书记", "overlap_org": "中共观山湖区委员会", "overlap_period": "2021-04"},
    # 秦永康 ↔ 副区长们 (区长-副区长关系)
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "秦永康（区长）与吴勇（副区长）在区政府班子共事", "overlap_org": "观山湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "秦永康（区长）与曹洋（副区长）在区政府班子共事", "overlap_org": "观山湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "秦永康（区长）与杨波（副区长）在区政府班子共事", "overlap_org": "观山湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "秦永康（区长）与耿立波（副区长）在区政府班子共事", "overlap_org": "观山湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "秦永康（区长）与朱应川（副区长）在区政府班子共事", "overlap_org": "观山湖区人民政府", "overlap_period": ""},
    # 罗杨 ↔ 邱斌 (区委-人大)
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "罗杨（区委书记）与邱斌（区人大常委会主任）在区四套班子共事", "overlap_org": "中共观山湖区委员会/观山湖区人大常委会", "overlap_period": ""},
]

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

    print(f"\nBuild complete for {SLUG} as of {AS_OF}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
