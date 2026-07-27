#!/usr/bin/env python3
"""Build script for 汉阴县 (安康市, 陕西省) government network.

Research date: 2026-07-25
Sources:
  - https://www.hanyin.gov.cn/ (official website - 领导之窗, leader profiles)
  - News articles from 汉阴县融媒体中心 2025-2026
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.gexf import GEXFBuilder
from gov_relation.schema import create_tables, insert_organizations, insert_persons, insert_positions, insert_relationships

SLUG = "汉阴县"
DB_PATH = REPO_ROOT / "data/database" / f"{SLUG}_network.db"
GEXF_PATH = REPO_ROOT / "data/graph" / f"{SLUG}_network.gexf"

PERSONS = [
    # Party committee
    {"id": 1, "name": "陈永乐", "gender": "男", "ethnicity": "汉族", "birth": "1974年7月", "birthplace": "陕西平利", "education": "在职大学学历", "party_join": "1995年11月", "work_start": "1991年9月", "current_post": "县委书记", "current_org": "中共汉阴县委员会", "source": "https://www.hanyin.gov.cn/Content-2293684.html"},
    {"id": 2, "name": "吴奎", "gender": "男", "ethnicity": "汉族", "birth": "1979年7月", "birthplace": "", "education": "全日制大学本科/工学学士", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记、县长", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2308878.html"},
    {"id": 3, "name": "王众义", "gender": "男", "ethnicity": "汉族", "birth": "1978年1月", "birthplace": "陕西岚皋", "education": "在职大学学历", "party_join": "2000年8月", "work_start": "1997年7月", "current_post": "县委副书记（正县级）", "current_org": "中共汉阴县委员会", "source": "https://www.hanyin.gov.cn/Content-2310971.html"},
    {"id": 4, "name": "唐如刚", "gender": "男", "ethnicity": "汉族", "birth": "1974年4月", "birthplace": "陕西平利", "education": "在职大学学历", "party_join": "1997年12月", "work_start": "1994年9月", "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共汉阴县纪律检查委员会", "source": "https://www.hanyin.gov.cn/Content-2310972.html"},
    {"id": 5, "name": "李万华", "gender": "男", "ethnicity": "汉族", "birth": "1978年12月", "birthplace": "陕西石泉", "education": "在职大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、组织部部长", "current_org": "中共汉阴县委员会", "source": "https://www.hanyin.gov.cn/Content-2721372.html"},
    {"id": 6, "name": "周星", "gender": "女", "ethnicity": "汉族", "birth": "1981年10月", "birthplace": "陕西镇坪", "education": "在职研究生学历", "party_join": "2000年6月", "work_start": "2000年9月", "current_post": "县委常委、宣传部部长", "current_org": "中共汉阴县委员会", "source": "https://www.hanyin.gov.cn/Content-2310974.html"},
    {"id": 7, "name": "艾昌勇", "gender": "男", "ethnicity": "汉族", "birth": "1973年12月", "birthplace": "湖北荆门", "education": "本科学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县人武部政委", "current_org": "汉阴县人民武装部", "source": "https://www.hanyin.gov.cn/Content-2820911.html"},
    {"id": 8, "name": "陈抨印", "gender": "男", "ethnicity": "汉族", "birth": "1982年2月", "birthplace": "陕西镇坪", "education": "在职大学学历", "party_join": "2001年7月", "work_start": "2001年", "current_post": "县委常委、常务副县长", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2835325.html"},
    {"id": 9, "name": "李莉", "gender": "女", "ethnicity": "汉族", "birth": "1982年4月", "birthplace": "陕西汉滨", "education": "省委党校研究生/经济学学士/工商管理硕士", "party_join": "2001年11月", "work_start": "2004年7月", "current_post": "县委常委、副县长", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2835478.html"},
    {"id": 10, "name": "张林冲", "gender": "男", "ethnicity": "汉族", "birth": "1979年7月", "birthplace": "陕西汉滨", "education": "省委党校研究生学历", "party_join": "2003年6月", "work_start": "1997年12月", "current_post": "县委常委、统战部部长", "current_org": "中共汉阴县委员会", "source": "https://www.hanyin.gov.cn/Content-2835603.html"},
    {"id": 11, "name": "许海军", "gender": "男", "ethnicity": "汉族", "birth": "1985年10月", "birthplace": "江苏阜宁", "education": "大学本科学历", "party_join": "2006年5月", "work_start": "2008年", "current_post": "县委常委、副县长（苏陕协作挂职）", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2840844.html"},
    {"id": 12, "name": "胡轶", "gender": "男", "ethnicity": "汉族", "birth": "1981年2月", "birthplace": "安徽绩溪", "education": "全日制研究生学历/法学硕士", "party_join": "2002年4月", "work_start": "2006年7月", "current_post": "县委常委、副县长（建行挂职）", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2880077.html"},
    # Government deputies
    {"id": 13, "name": "张添", "gender": "男", "ethnicity": "汉族", "birth": "1984年2月", "birthplace": "陕西汉滨", "education": "在职研究生学历", "party_join": "中共党员", "work_start": "", "current_post": "副县长、县公安局局长", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2721051.html"},
    {"id": 14, "name": "宋国卿", "gender": "男", "ethnicity": "汉族", "birth": "1984年10月", "birthplace": "陕西旬阳", "education": "全日制研究生学历", "party_join": "2002年5月", "work_start": "2007年9月", "current_post": "副县长", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2310978.html"},
    {"id": 15, "name": "王侠军", "gender": "男", "ethnicity": "汉族", "birth": "1972年5月", "birthplace": "陕西汉阴", "education": "在职大学学历", "party_join": "1994年12月", "work_start": "1992年7月", "current_post": "副县长（三级调研员）", "current_org": "汉阴县人民政府", "source": "https://www.hanyin.gov.cn/Content-2308898.html"},
    # People's Congress
    {"id": 16, "name": "黄邦平", "gender": "男", "ethnicity": "汉族", "birth": "1967年1月", "birthplace": "陕西汉阴", "education": "在职大学学历", "party_join": "1995年3月", "work_start": "1986年7月", "current_post": "县人大常委会主任", "current_org": "汉阴县人大常委会", "source": "https://www.hanyin.gov.cn/Content-600597.html"},
    # CPPCC
    {"id": 17, "name": "刘定东", "gender": "男", "ethnicity": "汉族", "birth": "1967年6月", "birthplace": "陕西汉阴", "education": "在职研究生学历（西北五省区党校公共管理专业）", "party_join": "1991年5月", "work_start": "1988年12月", "current_post": "县政协主席", "current_org": "政协汉阴县委员会", "source": "https://www.hanyin.gov.cn/Content-2387056.html"},
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共汉阴县委员会", "type": "党委", "level": "县处级", "parent": "中共安康市委", "location": "陕西省安康市汉阴县"},
    {"id": 2, "name": "汉阴县人民政府", "type": "政府", "level": "县处级", "parent": "安康市人民政府", "location": "陕西省安康市汉阴县"},
    {"id": 3, "name": "中共汉阴县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共安康市纪委", "location": "陕西省安康市汉阴县"},
    {"id": 4, "name": "汉阴县人民武装部", "type": "军队", "level": "县处级", "parent": "安康军分区", "location": "陕西省安康市汉阴县"},
    {"id": 5, "name": "汉阴县人大常委会", "type": "人大", "level": "县处级", "parent": "安康市人大常委会", "location": "陕西省安康市汉阴县"},
    {"id": 6, "name": "政协汉阴县委员会", "type": "政协", "level": "县处级", "parent": "政协安康市委员会", "location": "陕西省安康市汉阴县"},
    {"id": 7, "name": "汉阴县公安局", "type": "政府", "level": "乡科级", "parent": "汉阴县人民政府", "location": "陕西省安康市汉阴县"},
]

POSITIONS = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月17日在任"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委副书记（正县级）", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "县委常委、县人武部政委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "苏陕协作挂职干部"},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "中国建设银行挂职干部"},
    # 县政府
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 8, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "苏陕协作"},
    {"person_id": 12, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "建行帮扶"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县公安局局长"},
    {"person_id": 13, "org_id": 7, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "二级高级警长"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长（三级调研员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 16, "org_id": 5, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 政协
    {"person_id": 17, "org_id": 6, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "中共汉阴县委员会/汉阴县人民政府", "overlap_period": "2025-2026"},
    # 县委书记与县委副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与专职副书记", "overlap_org": "中共汉阴县委员会", "overlap_period": "2025-2026"},
    # 县委书记与县委常委
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与纪委书记", "overlap_org": "中共汉阴县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与组织部部长", "overlap_org": "中共汉阴县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与宣传部部长", "overlap_org": "中共汉阴县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与常务副县长", "overlap_org": "中共汉阴县委员会", "overlap_period": "2025-2026"},
    # 县长与副县长（政府领导班子）
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长与常务副县长（政府领导班子）", "overlap_org": "汉阴县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长与副县长（政府领导班子）", "overlap_org": "汉阴县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长与副县长（公安局长）", "overlap_org": "汉阴县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长与副县长（政府领导班子）", "overlap_org": "汉阴县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长与副县长（政府领导班子）", "overlap_org": "汉阴县人民政府", "overlap_period": "2025-2026"},
    # 交叉任职关系：县委常委兼任副县长
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "常务副县长与县委常委兼副县长", "overlap_org": "汉阴县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "挂职副县长（苏陕协作与建行帮扶）", "overlap_org": "汉阴县人民政府", "overlap_period": "2025-2026"},
    # 同乡域关系（同属安康市）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "同乡：陈永乐（平利）、唐如刚（平利）平利籍干部", "overlap_org": "安康市平利县", "overlap_period": "", "strength": "weak"},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "同乡：周星（镇坪）、陈抨印（镇坪）镇坪籍干部", "overlap_org": "安康市镇坪县", "overlap_period": "", "strength": "weak"},
]


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
        create_tables(conn, overwrite=True)
        insert_persons(conn, PERSONS)
        insert_organizations(conn, ORGANIZATIONS)
        insert_positions(conn, POSITIONS)
        insert_relationships(conn, RELATIONSHIPS)
        print(f"DB ready: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(POSITIONS)} positions, {len(RELATIONSHIPS)} relationships")
    finally:
        conn.close()

    builder = GEXFBuilder(title=SLUG)
    for p in PERSONS:
        builder.add_person(
            id=p["id"], name=p["name"], current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""), gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""), birth=p.get("birth", ""),
            source=p.get("source", "")
        )
    for o in ORGANIZATIONS:
        builder.add_organization(
            id=o["id"] + 100000, name=o.get("name", ""),
            org_type=o.get("type", ""), level=o.get("level", ""),
            location=o.get("location", "")
        )
    for r in RELATIONSHIPS:
        builder.add_relationship(
            source=r["person_a"], target=r["person_b"],
            rel_type=r.get("type", ""), context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""), overlap_period=r.get("overlap_period", "")
        )
    builder.write(GEXF_PATH)
    print(f"GEXF ready: {GEXF_PATH}")
    print(f"Done: {DB_PATH}, {GEXF_PATH}")


if __name__ == "__main__":
    main()
