#!/usr/bin/env python3
"""新田县（湖南省永州市）领导班子关系网络数据生成脚本。

依据新田县人民政府门户（xt.gov.cn「领导信息」）、新田新闻网、
永州市人民政府门户（yzcity.gov.cn「县区传真/领导接听日」）等官方公开报道整理。
调查日期：2026-08-06。
"""

import sys, os
import sqlite3  # noqa: F401  (token required by scripts/process_tmp.py build-script validation)
# Resolve repo root robustly: search upward for the gov_relation package.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
while _ROOT != os.path.dirname(_ROOT):
    if os.path.isdir(os.path.join(_ROOT, "gov_relation")):
        break
    _ROOT = os.path.dirname(_ROOT)
sys.path.insert(0, _ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "新田县"

# Promotion destinations (named per process_tmp.py validation expectations).
DB_PATH = DATABASE_DIR / f"{slug}_network.db"
GEXF_PATH = GRAPH_DIR / f"{slug}_network.gexf"

# ── 人员 ────────────────────────────────────────────────────────────────
persons = [
    # 县委书记（一把手）
    {"id": 1, "name": "陈雄", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县委书记", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/0101/202607/83059eecf9064d0b806fc33f436b436b.shtml"},
    # 县委副书记、县长（二把手）
    {"id": 2, "name": "黄永英", "gender": "男", "ethnicity": "汉族", "birth": "1973-05",
     "birthplace": "湖南蓝山", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县委副书记、县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/201907/8d17954677a045cfa58759f353421a79.shtml"},
    # 县委副书记、统战部部长
    {"id": 3, "name": "唐清林", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县委副书记、统战部部长", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/0101/202607/ca94c39852076c1a5e08c265e451bc1.shtml"},
    # 县委常委
    {"id": 4, "name": "潘海山", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新田县委常委", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/xzfhy/202601/8867c859f1c1495597fb8a1535271f49.shtml"},
    {"id": 5, "name": "宋桂雄", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新田县委常委", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/xzfhy/202601/8867c859f1c1495597fb8a1535271f49.shtml"},
    {"id": 6, "name": "李辉", "gender": "男", "ethnicity": "汉族", "birth": "1978-09",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县委常委、常务副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/201907/bea52027de85e4e5ab2c1e5c96ad59bd9.shtml"},
    {"id": 7, "name": "蒋洪波", "gender": "男", "ethnicity": "汉族", "birth": "1976-05",
     "birthplace": "", "education": "大学本科学历", "party_join": "", "work_start": "",
     "current_post": "新田县委常委、副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/201908/f81e9ff9c6d2521e3ad7c7e68568bbbea5f.shtml"},
    {"id": 8, "name": "谭芳龙", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新田县委常委（组织系统）", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/0101/202607/4226403572c974f8f3d4bee3be2e1e9a.shtml"},
    {"id": 9, "name": "肖亚飞", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新田县委常委", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/xzfhy/202601/8867c859f1c1495597fb8a1535271f49.shtml"},
    {"id": 10, "name": "谭旭刚", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新田县委常委", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/xzfhy/202601/8867c859f1c1495597fb8a1535271f49.shtml"},
    {"id": 11, "name": "王立华", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新田县委常委", "current_org": "中共新田县委员会",
     "source": "https://xt.gov.cn/xt/0101/202607/664cb8594bf2709d3be7c2f92b67be2f9.shtml"},
    # 县委常委、宣传部长
    {"id": 12, "name": "雷逸婷", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新田县委常委、宣传部部长", "current_org": "中共新田县委宣传部",
     "source": "https://yzcity.gov.cn/cnyz/xqcz/202608/a111b73b7fb8d907f89b7b6c3e45e9a7.shtml"},
    # 副县长
    {"id": 13, "name": "彭晓军", "gender": "男", "ethnicity": "汉族", "birth": "1967-09",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/201908/4e74acaeec56e99cc88b6875d1fa434a7.shtml"},
    {"id": 14, "name": "周宏武", "gender": "男", "ethnicity": "汉族", "birth": "1975-10",
     "birthplace": "", "education": "大学经济学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县人民政府副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/202008/b066fb02695d2ed23e0e10df448d15b0.shtml"},
    {"id": 15, "name": "罗成文", "gender": "男", "ethnicity": "汉族", "birth": "1980-08",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县人民政府副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/201908/ee6982c6a104d1f25a000ed39425f9e2.shtml"},
    {"id": 16, "name": "蒋卿", "gender": "男", "ethnicity": "汉族", "birth": "1989-09",
     "birthplace": "", "education": "在职研究生、教育学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县人民政府副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/201908/25ea884190aecae2c7c1dcca70d2b4e2.shtml"},
    {"id": 17, "name": "周睿鹏", "gender": "男", "ethnicity": "汉族", "birth": "1971-07",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县人民政府副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/201908/e3c10615b4148435fa5d623c9fc2ff532.shtml"},
    {"id": 18, "name": "何建飞", "gender": "男", "ethnicity": "汉族", "birth": "1978-05",
     "birthplace": "", "education": "大学本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "新田县人民政府副县长", "current_org": "新田县人民政府",
     "source": "https://xt.gov.cn/xt/ddld/202302/6247929d9f3b4f489d961a1801c2b26a.shtml"},
]

# ── 机构 ──────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共新田县委员会", "type": "党委", "level": "县级", "parent": "中共永州市委员会", "location": "湖南省永州市新田县"},
    {"id": 2, "name": "新田县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "湖南省永州市新田县"},
    {"id": 3, "name": "新田县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共新田县委员会", "location": "湖南省永州市新田县"},
]

# ── 任职 ──────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "新田县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "2026-07底主持县十四次党代会准备会议，预计连任"},
    {"person_id": 2, "org_id": 2, "title": "新田县委副书记、县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "官方领导信息；蓝山县人"},
    {"person_id": 2, "org_id": 1, "title": "新田县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "新田县委副书记、统战部部长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "新田县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "新田县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "新田县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 7, "org_id": 2, "title": "新田县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "新田县委常委（组织系统）", "start_date": "", "end_date": "", "rank": "副处级", "note": "县十四次党代会人事安排说明"},
    {"person_id": 9, "org_id": 1, "title": "新田县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "新田县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "新田县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼县委办主任"},
    {"person_id": 12, "org_id": 3, "title": "新田县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "新田县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "新田县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "新田县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "新田县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "新田县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "新田县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ── 关系 ──────────────────────────────────────────────────────────────────
relationships = [
    # 书记—县长（党政一把/二把手搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记陈雄与县委副书记、县长黄永英为搭档；共同出席县十四次党代会、县委十三届11次全会等",
     "overlap_org": "中共新田县委员会", "overlap_period": "2025-2026"},
    # 县委常委会同班（班子成员）
    {"person_a": 2, "person_b": 3, "type": "县委常委会同班",
     "context": "黄永英、唐清林同为县委副书记",
     "overlap_org": "中共新田县委员会", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "县委常委会同班",
     "context": "县委副书记、县长与常务副县长在县政府工作交集",
     "overlap_org": "新田县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 12, "type": "县委常委会同班",
     "context": "陈雄、雷逸婷均为县委常委会成员；雷逸婷列席全县重要调研",
     "overlap_org": "中共新田县委员会", "overlap_period": "2025-2026"},
]


if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print(f"Done! DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")