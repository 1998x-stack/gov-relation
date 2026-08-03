#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 德阳市领导班子 (Deyang City Leadership Network).
Investigation date: 2026-08-03
Current 德阳市委书记: 刘光强
Current 德阳市市长: 黄朝阳
"""

import sys
import os

# Resolve repo root: this file is at data/tmp/sichuan_德阳市/build_德阳市_data.py
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "德阳市"
# Write to staging first; process_tmp.py --apply will promote to canonical paths
STAGING_DIR = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(STAGING_DIR, "德阳市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "德阳市_network.gexf")

PERSONS = [
    # ═══ Party Secretary ═══
    {
        "id": 1,
        "name": "刘光强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市委书记",
        "current_org": "中共德阳市委",
        "source": "https://www.deyang.gov.cn/xwdt/dydt/1963704.htm",
    },
    # ═══ Mayor ═══
    {
        "id": 2,
        "name": "黄朝阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-03",
        "birthplace": "",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市委副书记、市长",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/gk/ldzc/hcy/grjl/1863006.htm",
    },
    # ═══ Deputy Party Secretary ═══
    {
        "id": 3,
        "name": "麻常昕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市委常委、组织部部长（拟提名为市（州）党委副书记候选人）",
        "current_org": "中共德阳市委组织部",
        "source": "https://www.deyang.gov.cn/gk/gsgg/bmgg/1963621.htm",
    },
    # ═══ Discipline Inspection Secretary ═══
    {
        "id": 4,
        "name": "赵平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市委常委、市纪委书记、市监委主任",
        "current_org": "中共德阳市纪律检查委员会",
        "source": "https://www.deyang.gov.cn/xwdt/dydt/1961859.htm",
    },
    # ═══ Executive Vice Mayor ═══
    {
        "id": 5,
        "name": "李江波",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1981-10",
        "birthplace": "内蒙古赤峰",
        "education": "清华大学计算机硕士、公共管理博士",
        "party_join": "中共党员",
        "work_start": "2006-07",
        "current_post": "德阳市委常委、常务副市长、党组副书记",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/gk/ldzc/ljb/grjg/1817521.htm",
    },
    # ═══ Political-Legal Committee Secretary ═══
    {
        "id": 6,
        "name": "程朝辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市委常委、政法委书记",
        "current_org": "中共德阳市委政法委员会",
        "source": "https://www.deyang.gov.cn/xwdt/dydt/1963693.htm",
    },
    # ═══ Vice Mayor (seconded) ═══
    {
        "id": 7,
        "name": "罗蓉雪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-11",
        "birthplace": "四川成都",
        "education": "电子科技大学在职研究生",
        "party_join": "中共党员",
        "work_start": "2002-07",
        "current_post": "德阳市委常委、副市长（挂职）",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/gk/ldzc/lrx/grjg/1958788.htm",
    },
    # ═══ United Front Secretary ═══
    {
        "id": 8,
        "name": "卿伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市委常委、统战部部长，市政协党组副书记",
        "current_org": "中共德阳市委统战部",
        "source": "https://www.deyang.gov.cn/xwdt/dydt/1963019.htm",
    },
    # ═══ Party Committee Secretary-General ═══
    {
        "id": 9,
        "name": "魏宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市委秘书长",
        "current_org": "中共德阳市委",
        "source": "https://www.deyang.gov.cn/xwdt/dydt/1962470.htm",
    },
    # ═══ Vice Mayors ═══
    {
        "id": 10,
        "name": "徐春龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "",
        "education": "",
        "party_join": "民盟",
        "work_start": "",
        "current_post": "德阳市副市长",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/info/iList.jsp?tm_id=9",
    },
    {
        "id": 11,
        "name": "蒋挺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市副市长、市公安局局长",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/info/iList.jsp?tm_id=9",
    },
    {
        "id": 12,
        "name": "王洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市副市长",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/info/iList.jsp?tm_id=9",
    },
    {
        "id": 13,
        "name": "王宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市副市长",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/info/iList.jsp?tm_id=9",
    },
    {
        "id": 14,
        "name": "徐创军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市副市长",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/info/iList.jsp?tm_id=9",
    },
    {
        "id": 15,
        "name": "杜尚武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市副市长兼中江县委书记",
        "current_org": "中共中江县委",
        "source": "https://www.deyang.gov.cn/info/iList.jsp?tm_id=9",
    },
    {
        "id": 16,
        "name": "姜丽丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-08",
        "birthplace": "",
        "education": "",
        "party_join": "民建",
        "work_start": "",
        "current_post": "德阳市副市长（挂职）",
        "current_org": "德阳市人民政府",
        "source": "https://www.deyang.gov.cn/info/iList.jsp?tm_id=9",
    },
    # ═══ NPC Standing Committee Chairman ═══
    {
        "id": 17,
        "name": "周鸿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市人大常委会党组书记、主任",
        "current_org": "德阳市人民代表大会常务委员会",
        "source": "https://www.deyang.gov.cn/xwdt/dydt/1963704.htm",
    },
    # ═══ CPPCC Chairman ═══
    {
        "id": 18,
        "name": "苏刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德阳市政协主席、党组书记",
        "current_org": "中国人民政治协商会议德阳市委员会",
        "source": "https://www.deyang.gov.cn/xwdt/dydt/1963704.htm",
    },
    # ═══ Predecessors ═══
    {
        "id": 19,
        "name": "靳磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "河南济源",
        "education": "武汉大学本科，厦门大学金融硕士",
        "party_join": "中共党员",
        "work_start": "1992-07",
        "current_post": "广东省委常委、深圳市委书记",
        "current_org": "中共深圳市委",
        "source": "https://zh.wikipedia.org/wiki/%E9%9D%B3%E7%A3%8A",
    },
    {
        "id": 20,
        "name": "赵世勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（不详）曾任江苏省副省长",
        "current_org": "",
        "source": "report/20260803-德阳市-市委书记市长-前任去向调查报告.md",
    },
    {
        "id": 21,
        "name": "何礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（去向待查）",
        "current_org": "",
        "source": "report/20260803-德阳市-市委书记市长-前任去向调查报告.md",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共德阳市委", "type": "党委", "level": "地级", "parent": "四川省", "location": "德阳"},
    {"id": 2, "name": "德阳市人民政府", "type": "政府", "level": "地级", "parent": "四川省", "location": "德阳"},
    {"id": 3, "name": "中共德阳市纪律检查委员会", "type": "纪委", "level": "地级", "parent": "德阳市委", "location": "德阳"},
    {"id": 4, "name": "德阳市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "德阳市", "location": "德阳"},
    {"id": 5, "name": "政协德阳市委员会", "type": "政协", "level": "地级", "parent": "德阳市", "location": "德阳"},
    {"id": 6, "name": "中共德阳市委组织部", "type": "党委", "level": "地级", "parent": "德阳市委", "location": "德阳"},
    {"id": 7, "name": "中共德阳市委政法委员会", "type": "党委", "level": "地级", "parent": "德阳市委", "location": "德阳"},
    {"id": 8, "name": "中共德阳市委统战部", "type": "党委", "level": "地级", "parent": "德阳市委", "location": "德阳"},
    {"id": 9, "name": "德阳市公安局", "type": "政府", "level": "地级", "parent": "德阳市政府", "location": "德阳"},
    {"id": 10, "name": "中共中江县委", "type": "党委", "level": "县级", "parent": "德阳市委", "location": "中江"},
    {"id": 11, "name": "中共深圳市委", "type": "党委", "level": "副省级", "parent": "广东省", "location": "深圳"},
    {"id": 12, "name": "四川省经济和信息化厅", "type": "政府", "level": "省级", "parent": "四川省", "location": "成都"},
]

POSITIONS = [
    # 刘光强
    {"person_id": 1, "org_id": 1, "title": "德阳市委书记", "start": "2022-07", "end": "present",
     "rank": "正厅级", "note": "接替靳磊"},
    {"person_id": 1, "org_id": 2, "title": "德阳市市长", "start": "2018", "end": "2022-07",
     "rank": "正厅级", "note": "升任市委书记"},
    # 黄朝阳
    {"person_id": 2, "org_id": 2, "title": "德阳市市长", "start": "2024-11", "end": "present",
     "rank": "正厅级", "note": "代市长后转正"},
    {"person_id": 2, "org_id": 1, "title": "德阳市委副书记", "start": "2024-11", "end": "present",
     "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "四川省经济和信息化厅厅长", "start": "", "end": "2024-11",
     "rank": "正厅级", "note": "调任德阳前职务"},
    # 麻常昕
    {"person_id": 3, "org_id": 6, "title": "德阳市委常委、组织部部长", "start": "", "end": "present",
     "rank": "副厅级", "note": "2026年7月拟提名为党委副书记"},
    # 赵平
    {"person_id": 4, "org_id": 3, "title": "德阳市委常委、市纪委书记、市监委主任", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 李江波
    {"person_id": 5, "org_id": 2, "title": "德阳市委常委、常务副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": "清华大学博士"},
    # 程朝辉
    {"person_id": 6, "org_id": 7, "title": "德阳市委常委、政法委书记", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 罗蓉雪
    {"person_id": 7, "org_id": 2, "title": "德阳市委常委、副市长（挂职）", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 卿伟
    {"person_id": 8, "org_id": 8, "title": "德阳市委常委、统战部部长", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "德阳市政协党组副书记", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 魏宇
    {"person_id": 9, "org_id": 1, "title": "德阳市委秘书长", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 徐春龙
    {"person_id": 10, "org_id": 2, "title": "德阳市副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": "民盟"},
    # 蒋挺
    {"person_id": 11, "org_id": 2, "title": "德阳市副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "德阳市公安局局长", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    # 王洪
    {"person_id": 12, "org_id": 2, "title": "德阳市副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 王宏
    {"person_id": 13, "org_id": 2, "title": "德阳市副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 徐创军
    {"person_id": 14, "org_id": 2, "title": "德阳市副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": ""},
    # 杜尚武
    {"person_id": 15, "org_id": 10, "title": "中江县委书记", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "德阳市副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": "兼任"},
    # 姜丽丹
    {"person_id": 16, "org_id": 2, "title": "德阳市副市长（挂职）", "start": "", "end": "present",
     "rank": "副厅级", "note": "民建"},
    # 周鸿
    {"person_id": 17, "org_id": 4, "title": "德阳市人大常委会主任", "start": "", "end": "present",
     "rank": "正厅级", "note": ""},
    # 苏刚
    {"person_id": 18, "org_id": 5, "title": "德阳市政协主席", "start": "", "end": "present",
     "rank": "正厅级", "note": ""},
    # 靳磊
    {"person_id": 19, "org_id": 1, "title": "德阳市委书记", "start": "2019-12", "end": "2022-07",
     "rank": "正厅级", "note": "后升任四川省委常委"},
    {"person_id": 19, "org_id": 11, "title": "深圳市委书记", "start": "2026-03", "end": "present",
     "rank": "副省级", "note": "跨省晋升"},
    # 赵世勇
    {"person_id": 20, "org_id": 1, "title": "德阳市委书记", "start": "", "end": "",
     "rank": "正厅级", "note": "前期书记"},
    # 何礼
    {"person_id": 21, "org_id": 2, "title": "德阳市市长", "start": "", "end": "",
     "rank": "正厅级", "note": "刘光强前任"},
]

RELATIONSHIPS = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长，党政一把手搭档",
     "overlap_org": "德阳市委/市政府", "overlap_period": "2024-11至今"},
    # 书记与组织部
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与组织部部长",
     "overlap_org": "德阳市委", "overlap_period": ""},
    # 书记与纪委书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委书记与纪委书记（监督关系）",
     "overlap_org": "德阳市委/纪委", "overlap_period": ""},
    # 市长与常务副市长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "市长与常务副市长",
     "overlap_org": "德阳市人民政府", "overlap_period": ""},
    # 书记与秘书长
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "市委书记与市委秘书长",
     "overlap_org": "德阳市委", "overlap_period": ""},
    # 政法与公安
    {"person_a": 6, "person_b": 11, "type": "overlap",
     "context": "政法委书记与公安局长（政法系统协作）",
     "overlap_org": "德阳市政法系统", "overlap_period": ""},
    # 前任-继任（书记）
    {"person_a": 19, "person_b": 1, "type": "predecessor_successor",
     "context": "靳磊-刘光强，德阳市委书记交接",
     "overlap_org": "中共德阳市委", "overlap_period": "2022"},
    # 书记-前市长（刘光强自己做过市长）
    {"person_a": 1, "person_b": 21, "type": "predecessor_successor",
     "context": "何礼-刘光强，德阳市长交接",
     "overlap_org": "德阳市人民政府", "overlap_period": ""},
    # 人大-市委
    {"person_a": 17, "person_b": 1, "type": "overlap",
     "context": "市人大常委会主任与市委书记",
     "overlap_org": "德阳市", "overlap_period": ""},
    # 政协-市委
    {"person_a": 18, "person_b": 1, "type": "overlap",
     "context": "市政协主席与市委书记",
     "overlap_org": "德阳市", "overlap_period": ""},
]

if __name__ == "__main__":
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
    print(f"\n✅  Build complete: {SLUG}")
    print(f"   - Persons: {len(PERSONS)}")
    print(f"   - Organizations: {len(ORGANIZATIONS)}")
    print(f"   - Positions: {len(POSITIONS)}")
    print(f"   - Relationships: {len(RELATIONSHIPS)}")
    print(f"   - DB: {DB_PATH}")
    print(f"   - GEXF: {GEXF_PATH}")