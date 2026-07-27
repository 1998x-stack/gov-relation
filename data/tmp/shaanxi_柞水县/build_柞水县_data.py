#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 柞水县 leadership network."""

import sys
import os
from pathlib import Path

# Ensure we can import from the project root
BASE = Path(__file__).resolve().parent.parent.parent  # data/tmp/shaanxi_柞水县/ -> project root
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "柞水县"
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (县委书记) ──
    {"id": 1, "name": "杨勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-09", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共柞水县委书记", "current_org": "中共柞水县委员会",
     "source": "https://www.snzs.gov.cn/info/2212/293874.htm"},

    # ── Current County Mayor (县长) ──
    {"id": 2, "name": "李强", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-07", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柞水县委副书记、县人民政府县长", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247404.htm"},

    # ── Executive Deputy County Mayor (县委常委、常务副县长) ──
    {"id": 3, "name": "冯锐", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-04", "birthplace": "陕西山阳", "education": "经济管理研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柞水县委常委、县政府副县长（常务）", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247444.htm"},

    # ── Party Member / Deputy County Mayor (县委常委、副县长) ──
    {"id": 4, "name": "李浴溱", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柞水县委常委、县政府党组成员、副县长", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247484.htm"},

    # ── Sci-tech Deputy (挂职, from Ministry of Science and Technology) ──
    {"id": 5, "name": "王书华", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-11", "birthplace": "河北衡水", "education": "博士研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柞水县委常委、县政府党组成员、副县长（挂职）", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247414.htm"},

    # ── Deputy County Mayor (副县长) ──
    {"id": 6, "name": "王宁", "gender": "男", "ethnicity": "回族",
     "birth": "1970-06", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柞水县政府党组成员、副县长", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247434.htm"},

    # ── Deputy County Mayor / Public Security (副县长、公安局长) ──
    {"id": 7, "name": "李小军", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-04", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柞水县政府党组成员、副县长、公安局局长", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247464.htm"},

    # ── Deputy County Mayor (副县长) ──
    {"id": 8, "name": "蒋维杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-08", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柞水县政府党组成员、副县长", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247474.htm"},

    # ── Deputy County Mayor (副县长) ──
    {"id": 9, "name": "王茂荣", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-10", "birthplace": "", "education": "省委党校研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "柞水县人民政府副县长", "current_org": "柞水县人民政府",
     "source": "https://www.snzs.gov.cn/info/2222/247454.htm"},

    # ── Previous Party Secretary (predecessor) ──
    {"id": 10, "name": "曹艳萍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原柞水县委书记（~2021-2026.06）", "current_org": "",
     "source": "https://www.snzs.gov.cn/info/2483/292684.htm"},

    # ── Previous County Mayor (predecessor) ──
    {"id": 11, "name": "刘鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原柞水县长（~2021-2025）", "current_org": "",
     "source": "https://www.snzs.gov.cn/info/1061/282914.htm"},
]

orgs = [
    {"id": 1, "name": "中共柞水县委员会", "type": "党委", "level": "县处级", "parent": "中共商洛市委员会", "location": "陕西商洛柞水"},
    {"id": 2, "name": "柞水县人民政府", "type": "政府", "level": "县处级", "parent": "商洛市人民政府", "location": "陕西商洛柞水"},
    {"id": 3, "name": "柞水县公安局", "type": "政府", "level": "乡科级", "parent": "柞水县人民政府", "location": "陕西商洛柞水"},
    {"id": 4, "name": "山阳县漫川关镇", "type": "乡镇", "level": "乡科级", "parent": "山阳县人民政府", "location": "陕西商洛山阳"},
    {"id": 5, "name": "中共镇安县委宣传部", "type": "党委", "level": "县处级", "parent": "中共镇安县委员会", "location": "陕西商洛镇安"},
    {"id": 6, "name": "商洛市公安局", "type": "政府", "level": "地厅级", "parent": "商洛市人民政府", "location": "陕西商洛"},
    {"id": 7, "name": "商洛市市区工程建设处", "type": "事业单位", "level": "乡科级", "parent": "商洛市人民政府", "location": "陕西商洛"},
    {"id": 8, "name": "中国科学技术发展战略研究院", "type": "事业单位", "level": "地厅级", "parent": "科学技术部", "location": "北京"},
    {"id": 9, "name": "清华大学水利工程系", "type": "事业单位", "level": "", "parent": "清华大学", "location": "北京"},
    {"id": 10, "name": "镇安县人民政府", "type": "政府", "level": "县处级", "parent": "商洛市人民政府", "location": "陕西商洛镇安"},
]

positions = [
    # ── 杨勇 (Party Secretary) ──
    {"person_id": 1, "org_id": 1, "title": "中共柞水县委书记", "start_date": "2026-06", "end_date": "", "rank": "县处级正职", "note": "现任"},

    # ── 李强 (County Mayor) ──
    {"person_id": 2, "org_id": 2, "title": "柞水县人民政府县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "柞水县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 冯锐 (Executive Deputy Mayor) ──
    {"person_id": 3, "org_id": 2, "title": "柞水县委常委、县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 3, "org_id": 5, "title": "镇安县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "山阳县漫川关镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "山阳县漫川关镇党委副书记、镇长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "山阳县委办公室副主任、县委调研室主任", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "山阳县政府办副主任科员", "start_date": "", "end_date": "", "rank": "", "note": "早期职务"},

    # ── 李浴溱 (Deputy Mayor) ──
    {"person_id": 4, "org_id": 2, "title": "柞水县委常委、县政府党组成员、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 2, "title": "柞水县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "中共柞水县委保密局副局长", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "柞水县政府办公室副主任", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "柞水县人民政府督查督办室主任", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "柞水牛背梁森林公园筹建处主任/陕西牛背梁国家森林公园管委会主任", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},

    # ── 王书华 (Sci-tech Deputy, 挂职) ──
    {"person_id": 5, "org_id": 2, "title": "柞水县委常委、县政府党组成员、副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 5, "org_id": 8, "title": "中国科学技术发展战略研究院院务委员、院党委委员", "start_date": "", "end_date": "", "rank": "局级", "note": "原单位"},
    {"person_id": 5, "org_id": 8, "title": "中国科学技术发展战略研究院总体研究所所长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "中国科学技术发展战略研究院技术预测与评价研究所所长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "中国科学技术发展战略研究院农村与区域科技发展研究所所长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "中国科学技术发展战略研究院副研究员、研究员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 9, "title": "清华大学水利工程系博士后", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 9, "title": "河北师范大学资源与环境科学学院讲师", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 王宁 (Deputy Mayor) ──
    {"person_id": 6, "org_id": 2, "title": "柞水县政府党组成员、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 6, "org_id": 2, "title": "镇副镇长、党委副书记、镇长、书记，街道党工委书记，市直部门副职", "start_date": "", "end_date": "", "rank": "", "note": "早期履历不完整"},

    # ── 李小军 (Public Security Deputy Mayor) ──
    {"person_id": 7, "org_id": 2, "title": "柞水县政府党组成员、副县长、公安局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 7, "org_id": 6, "title": "商洛市公安局办公室主任", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "商洛市公安局办公室副主任", "start_date": "", "end_date": "", "rank": "乡科级副职", "note": ""},

    # ── 蒋维杰 (Deputy Mayor) ──
    {"person_id": 8, "org_id": 2, "title": "柞水县政府党组成员、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 8, "org_id": 10, "title": "镇安县云盖寺镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "镇安县东川镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "镇安县东川镇党委副书记、镇长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "镇安县人民政府副科级研究员", "start_date": "", "end_date": "", "rank": "乡科级副职", "note": ""},

    # ── 王茂荣 (Deputy Mayor) ──
    {"person_id": 9, "org_id": 2, "title": "柞水县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 7, "title": "商洛市市区工程建设处综合办公室主任", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "商洛市市区工程建设处综合办公室副主任", "start_date": "", "end_date": "", "rank": "乡科级副职", "note": ""},

    # ── 曹艳萍 (Previous Party Secretary) ──
    {"person_id": 10, "org_id": 1, "title": "柞水县委书记", "start_date": "~2021", "end_date": "2026-06", "rank": "县处级正职", "note": ""},

    # ── 刘鹏 (Previous County Mayor) ──
    {"person_id": 11, "org_id": 2, "title": "柞水县人民政府县长", "start_date": "~2021", "end_date": "~2025", "rank": "县处级正职", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "杨勇（书记）与李强（县长）为现任党政一把手搭档", "overlap_org": "柞水县委/县政府", "overlap_period": "2026.06至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "杨勇（书记）与冯锐（常务副县长）为县委班子上下级", "overlap_org": "中共柞水县委", "overlap_period": "2026.06至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "李强（县长）与冯锐（常务副县长）为正副职搭档", "overlap_org": "柞水县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "前后任", "context": "杨勇接替曹艳萍任柞水县委书记", "overlap_org": "中共柞水县委", "overlap_period": "2026.06"},
    {"person_a": 2, "person_b": 11, "type": "前后任", "context": "李强接替刘鹏任柞水县长", "overlap_org": "柞水县人民政府", "overlap_period": "~2025"},
    {"person_a": 10, "person_b": 11, "type": "党政搭档", "context": "曹艳萍（原书记）与刘鹏（原县长）原为党政搭档", "overlap_org": "柞水县委/县政府", "overlap_period": "~2021-~2025"},
    {"person_a": 10, "person_b": 2, "type": "上下级", "context": "曹艳萍曾为书记，李强为现任县长，曾为上下级", "overlap_org": "中共柞水县委", "overlap_period": "~2025-2026"},
    {"person_a": 3, "person_b": 5, "type": "同事", "context": "冯锐与王书华同为柞水县委常委", "overlap_org": "中共柞水县委", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "同事", "context": "冯锐与李浴溱同为柞水县委常委", "overlap_org": "中共柞水县委", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同事", "context": "李浴溱与王宁同为县政府领导班子成员", "overlap_org": "柞水县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同事", "context": "王宁与李小军同为县政府领导班子成员", "overlap_org": "柞水县人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同事", "context": "李小军与蒋维杰同为县政府领导班子成员", "overlap_org": "柞水县人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "同事", "context": "蒋维杰与王茂荣同为县政府领导班子成员", "overlap_org": "柞水县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "跨县同事", "context": "冯锐原为镇安县委常委、宣传部部长，蒋维杰原在镇安县工作，曾在镇安共事", "overlap_org": "镇安县", "overlap_period": ""},
]


# ── MAIN ─────────────────────────────────────────────────────────────

def main():
    from datetime import datetime
    print("=" * 60)
    print("  柞水县（商洛市）领导班子工作关系网络")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(orgs)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=orgs,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print()
    print("📊 Summary:")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Size DB: {os.path.getsize(DB_PATH) if DB_PATH.exists() else 0} bytes")
    print(f"  Size GEXF: {os.path.getsize(GEXF_PATH) if GEXF_PATH.exists() else 0} bytes")
    print()
    print("✅ Done!")


if __name__ == "__main__":
    main()
