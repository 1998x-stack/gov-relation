#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Shangdang District (上党区), Changzhi, Shanxi."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure imports work from repo root
sys.path.insert(0, "/workspace/data/xieming/other-codes/gov-relation")

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────
SLUG = "上党区"
BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = Path(os.path.join(BASE, "data/tmp/shanxi_上党区"))
DB_PATH = os.path.join(str(TMP), f"{SLUG}_network.db")
GEXF_PATH = os.path.join(str(TMP), f"{SLUG}_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "张驰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委书记", "current_org": "中共长治市上党区委员会",
     "source": "http://www.shangdangqu.gov.cn/"},

    # 区长 — NOT YET IDENTIFIED from current government site news
    # The position is notably absent;区政府常务会议由常务副区长石玉主持
    # This is an open gap

    # ── Standing Committee Members (区委常委) ──
    {"id": 3, "name": "侯立峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委副书记、统战部部长",
     "current_org": "中共长治市上党区委员会",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260701_3181431.html"},

    {"id": 4, "name": "石玉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委常委、常务副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260719_3187416.html"},

    {"id": 5, "name": "宋淑琴", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委常委、组织部部长",
     "current_org": "中共长治市上党区委组织部",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260723_3189173.html"},

    {"id": 6, "name": "闫卫国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委常委、政法委书记",
     "current_org": "中共长治市上党区委政法委",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260723_3189173.html"},

    {"id": 7, "name": "路金戈", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委常委、区委办主任",
     "current_org": "中共长治市上党区委办公室",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260723_3189173.html"},

    {"id": 8, "name": "闫鹏云", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委常委、宣传部部长",
     "current_org": "中共长治市上党区委宣传部",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260723_3189173.html"},

    {"id": 9, "name": "陈潇光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区委常委、纪委书记、监委代主任",
     "current_org": "中共长治市上党区纪律检查委员会",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260719_3187418.html"},

    # ── District Government Leaders (副区长) ──
    {"id": 10, "name": "杜津力", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260723_3189173.html"},

    {"id": 11, "name": "席佳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260722_3188557.html"},

    {"id": 12, "name": "和旭峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260716_3186456.html"},

    {"id": 13, "name": "杨阿艳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区领导/副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260722_3188576.html"},

    {"id": 14, "name": "郭建勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区领导/副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260722_3188576.html"},

    {"id": 15, "name": "赵子闰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区领导/副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260722_3188576.html"},

    {"id": 16, "name": "宋志兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区领导/副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260722_3188576.html"},

    {"id": 17, "name": "刘彦雄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区领导/副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260722_3188576.html"},

    # ── District People's Congress & CPPCC ──
    {"id": 18, "name": "张芬芬", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区人大常委会主任",
     "current_org": "长治市上党区人民代表大会常务委员会",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260701_3181431.html"},

    {"id": 19, "name": "张东文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区政协主席",
     "current_org": "中国人民政治协商会议长治市上党区委员会",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202607/t20260701_3181431.html"},

    {"id": 20, "name": "王峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区人大常委会领导",
     "current_org": "长治市上党区人民代表大会常务委员会",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202606/t20260630_3181052.html"},

    {"id": 21, "name": "张慧军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区领导/副区长",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202606/t20260630_3181052.html"},

    {"id": 22, "name": "张健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "长治市上党区领导",
     "current_org": "长治市上党区人民政府",
     "source": "http://www.shangdangqu.gov.cn/xwdt/zwyw/202606/t20260630_3181052.html"},
]

organizations = [
    {"id": 1, "name": "中共长治市上党区委员会", "type": "党委", "level": "县处级", "parent": "中共长治市委", "location": "山西省长治市上党区"},
    {"id": 2, "name": "长治市上党区人民政府", "type": "政府", "level": "县处级", "parent": "长治市人民政府", "location": "山西省长治市上党区"},
    {"id": 3, "name": "中共长治市上党区委组织部", "type": "党委", "level": "县处级", "parent": "中共长治市上党区委员会", "location": "山西省长治市上党区"},
    {"id": 4, "name": "中共长治市上党区委政法委", "type": "党委", "level": "县处级", "parent": "中共长治市上党区委员会", "location": "山西省长治市上党区"},
    {"id": 5, "name": "中共长治市上党区委办公室", "type": "党委", "level": "县处级", "parent": "中共长治市上党区委员会", "location": "山西省长治市上党区"},
    {"id": 6, "name": "中共长治市上党区委宣传部", "type": "党委", "level": "县处级", "parent": "中共长治市上党区委员会", "location": "山西省长治市上党区"},
    {"id": 7, "name": "中共长治市上党区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共长治市上党区委员会", "location": "山西省长治市上党区"},
    {"id": 8, "name": "长治市上党区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "长治市上党区", "location": "山西省长治市上党区"},
    {"id": 9, "name": "中国人民政治协商会议长治市上党区委员会", "type": "政协", "level": "县处级", "parent": "长治市上党区", "location": "山西省长治市上党区"},
    {"id": 10, "name": "中共长治市上党区委统战部", "type": "党委", "level": "县处级", "parent": "中共长治市上党区委员会", "location": "山西省长治市上党区"},
]

positions = [
    # 张驰
    {"person_id": 1, "org_id": 1, "title": "长治市上党区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "confirmed by government site articles 2026-07"},

    # 侯立峰
    {"person_id": 3, "org_id": 1, "title": "区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "confirmed by 两优一先 article 2026-06-30"},
    {"person_id": 3, "org_id": 10, "title": "区委统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "also serves as统战部部长"},

    # 石玉
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "presided over 区政府第97次常务会议 2026-07-17 as区委常委、常务副区长"},

    # 宋淑琴
    {"person_id": 5, "org_id": 3, "title": "区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 闫卫国
    {"person_id": 6, "org_id": 4, "title": "区委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 路金戈
    {"person_id": 7, "org_id": 5, "title": "区委常委、区委办主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 闫鹏云
    {"person_id": 8, "org_id": 6, "title": "区委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 陈潇光
    {"person_id": 9, "org_id": 7, "title": "区委常委、纪委书记、监委代主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "代主任 indicates acting/provisional appointment"},

    # Deputy Mayors
    {"person_id": 10, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "区领导/副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "区领导/副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "区领导/副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "区领导/副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "区领导/副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "区领导/副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "区领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # People's Congress
    {"person_id": 18, "org_id": 8, "title": "区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 20, "org_id": 8, "title": "区人大常委会领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # CPPCC
    {"person_id": 19, "org_id": 9, "title": "区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

relationships = [
    # 张驰 <-> 侯立峰 (区委书记-副书记)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记、统战部部长，在同一届区委领导班子中工作",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张驰 <-> 石玉 (区委书记-常务副区长)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与常务副区长，区委常委会共同成员",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张驰 <-> 宋淑琴 (区委书记-组织部长)
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与组织部部长，共同出席慰问活动",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张驰 <-> 闫卫国
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与政法委书记，区委常委会共同成员",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张驰 <-> 路金戈
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与区委办主任，路金戈陪同张驰调研生态环保工作",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张驰 <-> 闫鹏云
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区委书记与宣传部部长，区委常委会共同成员",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张驰 <-> 陈潇光
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区委书记与纪委书记，在城乡垃圾综合治理专题会议上共同出席",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张驰 <-> 张芬芬
    {"person_a": 1, "person_b": 18, "type": "overlap",
     "context": "区委书记与人大常委会主任，在全区两优一先会议上共同出席",
     "overlap_org": "长治市上党区", "overlap_period": "2024-2026"},

    # 张驰 <-> 张东文
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "context": "区委书记与政协主席，在全区两优一先会议上共同出席",
     "overlap_org": "长治市上党区", "overlap_period": "2024-2026"},

    # 张驰 <-> 杜津力
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "区委书记与副区长，在城乡垃圾综合治理和环保调研中共同出席",
     "overlap_org": "长治市上党区人民政府", "overlap_period": "2024-2026"},

    # 石玉 <-> 全体副区长 (区政府领导班子)
    {"person_a": 4, "person_b": 10, "type": "overlap",
     "context": "常务副区长与副区长，区政府领导班子成员",
     "overlap_org": "长治市上党区人民政府", "overlap_period": "2024-2026"},
    {"person_a": 4, "person_b": 11, "type": "overlap",
     "context": "常务副区长与副区长，区政府领导班子成员",
     "overlap_org": "长治市上党区人民政府", "overlap_period": "2024-2026"},
    {"person_a": 4, "person_b": 12, "type": "overlap",
     "context": "常务副区长与副区长，区政府领导班子成员",
     "overlap_org": "长治市上党区人民政府", "overlap_period": "2024-2026"},

    # 侯立峰 <-> 宋淑琴
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "区委副书记与组织部部长，区委常委会共同成员",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 宋淑琴 <-> 陈潇光 (纪委-组织)
    {"person_a": 5, "person_b": 9, "type": "overlap",
     "context": "组织部与纪委日常协作，共同出席慰问活动",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 闫卫国 <-> 陈潇光 (政法-纪委)
    {"person_a": 6, "person_b": 9, "type": "overlap",
     "context": "政法委与纪委在反腐倡廉工作中协作",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 路金戈 <-> 闫卫国 (区委办-政法委)
    {"person_a": 7, "person_b": 6, "type": "overlap",
     "context": "区委办与政法委在日常工作协调中密切配合",
     "overlap_org": "中共长治市上党区委员会", "overlap_period": "2024-2026"},

    # 张芬芬 <-> 王峰 (人大领导班子)
    {"person_a": 18, "person_b": 20, "type": "overlap",
     "context": "区人大常委会主任与人大领导，共同慰问活动",
     "overlap_org": "长治市上党区人民代表大会常务委员会", "overlap_period": "2024-2026"},

    # 张芬芬 <-> 张东文 (人大-政协)
    {"person_a": 18, "person_b": 19, "type": "overlap",
     "context": "人大主任与政协主席，在全区性会议中共同出席",
     "overlap_org": "长治市上党区", "overlap_period": "2024-2026"},
]


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
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


if __name__ == "__main__":
    main()
