#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 于洪区 leadership network."""

import sys
import os
import sqlite3
from datetime import datetime

# Allow running from repo root or staging dir
BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── DATA ─────────────────────────────────────────────────────────────
# Note: Integer IDs required by gov_relation.runner schema

persons = [
    {"id": 1, "name": "王洪超", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共沈阳市于洪区委员会",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202606/t20260629_5049245.html"},
    {"id": 2, "name": "刘伟", "gender": "男", "ethnicity": "汉族", "birth": "1978-03", "birthplace": "",
     "education": "硕士研究生/硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、副区长、代区长、区政府党组书记", "current_org": "于洪区人民政府",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/qz/202112/t20211220_2266180.html"},
    {"id": 3, "name": "么家伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记（可能已离任）", "current_org": "中共沈阳市于洪区委员会",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202603/t20260313_4999362.html"},
    {"id": 4, "name": "鲁瑶", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共沈阳市于洪区委员会",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260715_5057101.html"},
    {"id": 5, "name": "郝威", "gender": "男", "ethnicity": "汉族", "birth": "1984-12", "birthplace": "",
     "education": "大学/硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、常务副区长、区政府党组副书记", "current_org": "于洪区人民政府",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256864.html"},
    {"id": 6, "name": "王永亮", "gender": "男", "ethnicity": "汉族", "birth": "1971-02", "birthplace": "",
     "education": "在职大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长、区政府党组成员", "current_org": "于洪区人民政府",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3225979.html"},
    {"id": 7, "name": "矫健", "gender": "女", "ethnicity": "汉族", "birth": "1980-11", "birthplace": "",
     "education": "在职大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "于洪区人民政府",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256965.html"},
    {"id": 8, "name": "关伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、统战部部长", "current_org": "中共沈阳市于洪区委员会",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260706_5052641.html"},
    {"id": 9, "name": "周文辉", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "中共沈阳市于洪区委员会",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202605/t20260527_5031883.html"},
    {"id": 10, "name": "冶桂春", "gender": "女", "ethnicity": "回族", "birth": "1975-02", "birthplace": "",
     "education": "研究生/硕士", "party_join": "无党派", "work_start": "",
     "current_post": "副区长", "current_org": "于洪区人民政府",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3257135.html"},
    {"id": 11, "name": "董铁石", "gender": "男", "ethnicity": "汉族", "birth": "1976-10", "birthplace": "",
     "education": "大学/学士", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、区政府党组成员", "current_org": "于洪区人民政府",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256994.html"},
    {"id": 12, "name": "陈嘉宁", "gender": "男", "ethnicity": "汉族", "birth": "1971-09", "birthplace": "",
     "education": "在职大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、区政府党组成员、公安分局局长", "current_org": "沈阳市公安局于洪分局",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256896.html"},
    {"id": 13, "name": "王太文", "gender": "男", "ethnicity": "汉族", "birth": "1976-03", "birthplace": "",
     "education": "大学/学士", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、区政府党组成员", "current_org": "于洪区人民政府",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3236389.html"},
    {"id": 14, "name": "李广杰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "于洪区人大常委会",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"},
    {"id": 15, "name": "张殿军", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政协主席", "current_org": "于洪区政协",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"},
    {"id": 16, "name": "刘成", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政协党组书记", "current_org": "于洪区政协",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"},
    {"id": 17, "name": "高政威", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "原区委书记（已离任，去向待查）", "current_org": "（调离）",
     "source": "https://www.syyh.gov.cn/xwzx/jryh/202512/t20251208_4949972.html"},
    {"id": 18, "name": "张龙", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "原区委常委、常务副区长（已离任）", "current_org": "（调离）",
     "source": "https://www.syyh.gov.cn/zwgk/fdzdgknr/zfwj/syzbfwj/202604/t20260403_5010964.html"},
]

organizations = [
    {"id": 1, "name": "中共沈阳市于洪区委员会", "type": "党委", "level": "县级", "parent": "中共沈阳市委", "location": "沈阳市于洪区"},
    {"id": 2, "name": "于洪区人民政府", "type": "政府", "level": "县级", "parent": "沈阳市人民政府", "location": "沈阳市于洪区"},
    {"id": 3, "name": "于洪区人大常委会", "type": "人大", "level": "县级", "parent": "沈阳市人大常委会", "location": "沈阳市于洪区"},
    {"id": 4, "name": "于洪区政协", "type": "政协", "level": "县级", "parent": "沈阳市政协", "location": "沈阳市于洪区"},
    {"id": 5, "name": "沈阳市公安局于洪分局", "type": "政府", "level": "县级", "parent": "沈阳市公安局", "location": "沈阳市于洪区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-06", "end_date": "", "rank": "current", "note": "2026年6月由区长升任"},
    {"person_id": 1, "org_id": 2, "title": "区委副书记、区长", "start_date": "", "end_date": "2026-06", "rank": "former", "note": "升任书记前曾任于洪区区长"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、副区长、代区长、区政府党组书记", "start_date": "2026-06", "end_date": "", "rank": "current", "note": "2026年6月调任于洪区代区长"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "current", "note": "2026年6月后公开报道中未再出现，可能已调离"},
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "2026-06", "end_date": "", "rank": "current", "note": "2026年7月首次以副书记身份公开亮相"},
    {"person_id": 5, "org_id": 2, "title": "区委常委、常务副区长、区政府党组副书记", "start_date": "", "end_date": "", "rank": "current", "note": "接替张龙任常务副区长"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长、区政府党组成员", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "current", "note": "无党派人士"},
    {"person_id": 11, "org_id": 2, "title": "副区长、区政府党组成员", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "副区长、区政府党组成员、公安分局局长", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长、区政府党组成员", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "区政协党组书记", "start_date": "", "end_date": "", "rank": "current", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "区委书记（原）", "start_date": "", "end_date": "2026-06", "rank": "former", "note": "2026年3月仍在任，6月前离任，去向待查"},
    {"person_id": 18, "org_id": 2, "title": "区委常委、常务副区长（原）", "start_date": "", "end_date": "2026-05", "rank": "former", "note": "最晚2026年5月仍在任，6月被郝威接替，去向待查"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "书记与代区长，党政一把手搭档", "overlap_org": "于洪区委区政府", "overlap_period": "2026-06~"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记与副书记，2026年3月共同出席校地签约", "overlap_org": "于洪区委", "overlap_period": "~2026-06"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记与新任副书记，2026年7月共同检查防汛安置", "overlap_org": "于洪区委", "overlap_period": "2026-06~"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记与常务副区长", "overlap_org": "于洪区党政", "overlap_period": "2026-06~"},
    {"person_a": 17, "person_b": 1, "type": "前后任", "context": "前书记与升任书记（原为区长搭档）", "overlap_org": "于洪区", "overlap_period": "~2026-06"},
    {"person_a": 18, "person_b": 5, "type": "前后任", "context": "常务副区长前后任交接", "overlap_org": "于洪区政府", "overlap_period": "2026-05~06"},
    {"person_a": 1, "person_b": 17, "type": "搭档", "context": "高政威任书记时王洪超任区长，党政搭档", "overlap_org": "于洪区", "overlap_period": "~2026-06"},
    {"person_a": 1, "person_b": 18, "type": "上下级", "context": "王洪超任区长时张龙任常务副区长", "overlap_org": "于洪区政府", "overlap_period": "~2026-05"},
    {"person_a": 14, "person_b": 15, "type": "同僚", "context": "人大主任与政协主席，2026年7月共同出席全区警示教育会", "overlap_org": "于洪区", "overlap_period": "2026-07"},
]

# ── BUILD ─────────────────────────────────────────────────────────────

# Required tokens for process_tmp validation
DB_PATH = os.path.join(BASE, "data/database/于洪区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/于洪区_network.gexf")

if __name__ == "__main__":
    slug = "于洪区"

    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
