#!/usr/bin/env python3
"""乌当区（贵阳市）领导班子工作关系网络生成脚本.

基于乌当区人民政府门户网站 (www.gzwd.gov.cn)、乌当区人大常委会门户 (rd.gzwd.gov.cn)
与贵阳市人民政府门户网站 (www.guiyang.gov.cn) 的官方公开信息，构建乌当区区委、
区政府及区人大、区政协核心领导的 SQLite 数据库与 GEXF 关系图。

数据时间锚点：截至 2026-08-05
核心任职信息以官方区政府"领导之窗"、区人大任免公告为准（confirmed）；
早期履历细节因网络检索受限，仅收录能确认的锚点，其余列入 open questions。

来源：
- 乌当区人民政府门户 www.gzwd.gov.cn（2026-08-05 访问）领导之窗
- 乌当区人大常委会 rd.gzwd.gov.cn（2026-08-05 访问）人事任免/决议决定
- 贵阳市人民政府门户 www.guiyang.gov.cn（2026-08-05 访问）
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# 项目根目录（脚本位于 data/tmp/guizhou_乌当区/ 时向上三级）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parents[2].resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "乌当区"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

DB_PATH = _HERE / "乌当区_network.db"
GEXF_PATH = _HERE / "乌当区_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    # 1 现任区委书记
    {
        "id": 1,
        "name": "肖建波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "乌当区委书记、贵州乌当经开区党工委书记",
        "current_org": "中国共产党贵阳市乌当区委员会",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202602/t20260205_89397479.html",
    },
    # 2 现任代理区长
    {
        "id": 2,
        "name": "张媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-05",
        "birthplace": "",
        "education": "经济学学士、在职工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区政府副区长、代理区长，贵州乌当经济开发区党工委副书记、管委会主任（兼）",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202606/t20260608_90489335.html",
    },
    # 3 前任区长 陈丽（2026-06 辞职）
    {
        "id": 3,
        "name": "陈丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已辞去乌当区区长职务）",
        "current_org": "",
        "source": "https://rd.gzwd.gov.cn/zyfb/jyjd/202606/t20260612_90520862.html",
    },
    # 4 常务副区长 朱明明
    {
        "id": 4,
        "name": "朱明明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-11",
        "birthplace": "",
        "education": "理学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、党组副书记、区政府副区长（常务）",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202503/t20250317_87189184.html",
    },
    # 5 副区长 张海婷
    {
        "id": 5,
        "name": "张海婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-03",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府副区长",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202602/t20260205_89397861.html",
    },
    # 6 副区长（挂职）周炼
    {
        "id": 6,
        "name": "周炼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-02",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区人民政府副区长（挂职）",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202602/t20260205_89400283.html",
    },
    # 7 副区长 黄彬
    {
        "id": 7,
        "name": "黄彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "乌当区人民政府副区长",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202503/t20250317_87189902.html",
    },
    # 8 副区长 祁开鑫
    {
        "id": 8,
        "name": "祁开鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-07",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "乌当区人民政府副区长",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202512/t20251231_89106021.html",
    },
    # 9 副区长 王家星
    {
        "id": 9,
        "name": "王家星",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1979-05",
        "birthplace": "",
        "education": "省委党校本科",
        "party_join": "",
        "work_start": "",
        "current_post": "乌当区人民政府党组成员、副区长",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202503/t20250317_87190602.html",
    },
    # 10 副区长（挂职）李俊洪
    {
        "id": 10,
        "name": "李俊洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-11",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "乌当区人民政府副区长（挂职）",
        "current_org": "乌当区人民政府",
        "source": "https://www.gzwd.gov.cn/zwgk/ldzc_5978032/202602/t20260205_89400485.html",
    },
    # 11 区人大常委会主任 马定武
    {
        "id": 11,
        "name": "马定武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "贵阳市乌当区人大常委会",
        "source": "http://rd.gzwd.gov.cn/rdgl/ldzc_5978153/202503/t20250317_87187041.html",
    },
    # 12 区政协主席 陈玮
    {
        "id": 12,
        "name": "陈玮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协党组书记、主席",
        "current_org": "中国人民政治协商会议贵阳市乌当区委员会",
        "source": "http://rd.gzwd.gov.cn/dbgz/dbhd/202605/t20260515_90177062.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党贵阳市乌当区委员会", "type": "党委", "level": "县处级", "parent": "中国共产党贵阳市委员会", "location": "贵州省贵阳市乌当区"},
    {"id": 2, "name": "乌当区人民政府", "type": "政府", "level": "县处级", "parent": "贵阳市人民政府", "location": "贵州省贵阳市乌当区"},
    {"id": 3, "name": "贵州乌当经济开发区", "type": "开发区", "level": "园区", "parent": "贵阳市", "location": "贵州省贵阳市乌当区"},
    {"id": 4, "name": "乌当区人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "贵州省贵阳市乌当区"},
    {"id": 5, "name": "乌当区政协", "type": "政协", "level": "县处级", "parent": "", "location": "贵州省贵阳市乌当区"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    # 肖建波 — 区委书记（现任）
    {"person_id": 1, "org_id": 1, "title": "乌当区委书记", "start_date": "present", "end_date": "present", "rank": "副厅级", "note": "主持区委全面工作；同时兼任贵州乌当经开区党工委书记（领导之窗，2026-02 页面显示）"},
    {"person_id": 1, "org_id": 3, "title": "贵州乌当经开区党工委书记（兼）", "start_date": "present", "end_date": "present", "rank": "", "note": "区委书记兼任经开区党工委书记"},
    # 张媛 — 区委副书记、代理区长
    {"person_id": 2, "org_id": 1, "title": "乌当区委副书记", "start_date": "2026-06", "end_date": "present", "rank": "副厅级", "note": "2026-06任区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "乌当区政府副区长、代理区长", "start_date": "2026-06-12", "end_date": "present", "rank": "正县级", "note": "2026-06-12乌当区人大常委会决定张媛代理区长；主持区政府全面工作"},
    {"person_id": 2, "org_id": 3, "title": "贵州乌当经开区党工委副书记、管委会主任（兼）", "start_date": "2026-06", "end_date": "present", "rank": "", "note": "经开区管委会主任（兼），2026-07-15主持经开区管委会主任联席会议"},
    # 陈丽 — 前任区长
    {"person_id": 3, "org_id": 2, "title": "乌当区人民政府区长（前任）", "start_date": "present", "end_date": "2026-06-12", "rank": "正县级", "note": "2026-06-12乌当区人大常委会接受陈丽辞去区长职务"},
    # 朱明明 — 常务副区长
    {"person_id": 4, "org_id": 1, "title": "乌当区委常委", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "区委常委、党组副书记"},
    {"person_id": 4, "org_id": 2, "title": "区政府副区长（分管常务工作）", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "负责区人民政府常务工作"},
    # 张海婷 — 副区长
    {"person_id": 5, "org_id": 1, "title": "乌当区委常委", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "区委常委"},
    {"person_id": 5, "org_id": 2, "title": "区政府副区长", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "负责自然资源、住建、城市更新"},
    # 周炼 — 副区长（挂职）
    {"person_id": 6, "org_id": 1, "title": "乌当区委常委", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "区委常委"},
    {"person_id": 6, "org_id": 2, "title": "区政府副区长（挂职）", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "协助常务副区长负责国资、金融"},
    # 黄彬 — 副区长
    {"person_id": 7, "org_id": 2, "title": "区政府副区长", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "负责城市管理、工业、交通"},
    # 祁开鑫 — 副区长
    {"person_id": 8, "org_id": 2, "title": "区政府副区长", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "负责农业农村、乡村振兴"},
    # 王家星 — 副区长
    {"person_id": 9, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "负责教育、社保、民政"},
    # 李俊洪 — 副区长（挂职）
    {"person_id": 10, "org_id": 2, "title": "区政府副区长（挂职）", "start_date": "present", "end_date": "present", "rank": "副县级", "note": "负责机关事务"},
    # 马定武 — 区人大主任
    {"person_id": 11, "org_id": 4, "title": "区人大常委会党组书记、主任", "start_date": "present", "end_date": "present", "rank": "正县级", "note": "十八届区人大常委会主任"},
    # 陈玮 — 区政协主席
    {"person_id": 12, "org_id": 5, "title": "区政协党组书记、主席", "start_date": "present", "end_date": "present", "rank": "正县级", "note": "以人大代表身份走访选区选民"},
]

# ── Relationships (person <-> person) ─────────────────────────────────────
RELATIONSHIPS = [
    # 区委书记 — 代理区长（党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "肖建波任区委书记，张媛任区委副书记、代理区长（2026-06起），构成区委书记—区长党政一把手搭档", "overlap_org": "乌当区", "overlap_period": "2026-06至今"},
    # 区委书记 — 前任区长（前任后任于区政府层面对接）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "肖建波任区委书记，陈丽为前任区长（2026-06辞职）", "overlap_org": "乌当区", "overlap_period": "截至2026-06"},
    # 代理区长 — 前任区长（前任后任）
    {"person_a": 2, "person_b": 3, "type": "前任后任", "context": "陈丽辞去区长职务后，张媛代理乌当区区长（2026-06-12乌当区人大常委会决定）", "overlap_org": "乌当区人民政府", "overlap_period": "2026-06"},
    # 区委书记 — 常务副区长（上下级）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "朱明明为区委常委、常务副区长，在区委书记领导下", "overlap_org": "中国共产党贵阳市乌当区委员会", "overlap_period": "present"},
    # 代理区长 — 常务副区长（区长—常务副职）
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "朱明明作为常务副区长协助代理区长张媛分管人事、审计等工作", "overlap_org": "乌当区人民政府", "overlap_period": "2026-06至今"},
    # 代理区长 — 副区长张海婷（区政府班子）
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "张海婷为区委常委、副区长，区政府班子成员", "overlap_org": "乌当区人民政府", "overlap_period": "present"},
    # 代理区长 — 副区长黄彬
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "黄彬为区政府副区长，区政府班子成员", "overlap_org": "乌当区人民政府", "overlap_period": "present"},
    # 代理区长 — 副区长祁开鑫
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "祁开鑫为区政府副区长，与代理区长同班子", "overlap_org": "乌当区人民政府", "overlap_period": "present"},
    # 代理区长 — 副区长王家星
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "王家星为区政府党组成员、副区长", "overlap_org": "乌当区人民政府", "overlap_period": "present"},
    # 代理区长 — 副区长李俊洪（挂职）
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "李俊洪为区政府挂职副区长", "overlap_org": "乌当区人民政府", "overlap_period": "present"},
    # 区委书记 — 区人大主任
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "区委书记与区人大常委会主任同属区四套班子领导", "overlap_org": "乌当区", "overlap_period": "present"},
    # 区委书记 — 区政协主席
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "区委书记与区政协主席同属区四套班子领导", "overlap_org": "乌当区", "overlap_period": "present"},
    # 代理区长 — 区人大主任（人大任免代理区长）
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "2026-06-12区人大常委会决定张媛任代理区长；区人大常委会主任马定武", "overlap_org": "乌当区人大常委会", "overlap_period": "2026-06"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"Building 乌当区 (Wudang District) leadership network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    for p in [DB_PATH, GEXF_PATH]:
        if p.exists():
            print(f"  OK {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  MISSING {p.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()