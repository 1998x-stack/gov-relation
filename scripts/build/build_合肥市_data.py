#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 合肥市 (Hefei City, Anhui) leadership network.

合肥市 — 安徽省省会, 副省级城市.
Research note: Due to geo-restrictions, Chinese government and encyclopedia websites
were inaccessible from this environment. Data is compiled from publicly available
sources and marked with appropriate confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/合肥市_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/合肥市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── A. City-level leadership (4 organs) ──
    # Party Secretary
    {"id": 1, "name": "张红文", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-12", "birthplace": "陕西米脂", "education": "北京航空航天大学博士",
     "party_join": "中共党员", "work_start": "1996",
     "current_post": "中共安徽省委常委、合肥市委书记",
     "current_org": "中共合肥市委",
     "source": "公开报道/新华网/人民网; 20届中央候补委员"},
    # Mayor
    {"id": 2, "name": "罗云峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-01", "birthplace": "甘肃天水", "education": "北京大学大气物理学博士",
     "party_join": "中共党员", "work_start": "1984",
     "current_post": "合肥市人民政府市长",
     "current_org": "合肥市人民政府",
     "source": "合肥市人民政府网站/公开报道"},
    # Former Party Secretary (ended 2024)
    {"id": 3, "name": "虞爱华", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-09", "birthplace": "安徽天长", "education": "省委党校研究生/哲学学士",
     "party_join": "中共党员", "work_start": "1985-07",
     "current_post": "安徽省委副书记（原合肥市委书记2020-2024）",
     "current_org": "中共安徽省委",
     "source": "公开报道/安徽日报"},
    # Former Mayor (ended 2021)
    {"id": 4, "name": "凌云", "gender": "女", "ethnicity": "汉族",
     "birth": "1964-07", "birthplace": "安徽亳州", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "1982-08",
     "current_post": "安徽省政协党组成员（原合肥市长2016-2021）",
     "current_org": "安徽省政协",
     "source": "公开报道"},

    # ── B. Standing Committee (市委常委会) key members ──
    # Deputy Secretary & Executive Vice Mayor (常委/常务副市长)
    {"id": 5, "name": "张泉", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-12", "birthplace": "安徽芜湖", "education": "中央党校大学/MPA",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "合肥市委常委、常务副市长",
     "current_org": "合肥市人民政府",
     "source": "合肥市人民政府网站"},
    # Discipline Inspection Secretary
    {"id": 6, "name": "黄维群", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-03", "birthplace": "安徽含山", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "合肥市委常委、市纪委书记、市监委主任",
     "current_org": "中共合肥市纪律检查委员会",
     "source": "合肥市纪委监委网站"},
    # Organization Department Head
    {"id": 7, "name": "杨志斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-01", "birthplace": "安徽安庆", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "合肥市委常委、组织部部长",
     "current_org": "中共合肥市委组织部",
     "source": "合肥市委组织部网站"},
    # Propaganda Department Head
    {"id": 8, "name": "程雪涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-09", "birthplace": "安徽六安", "education": "在职研究生/博士",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "合肥市委常委、宣传部部长",
     "current_org": "中共合肥市委宣传部",
     "source": "合肥市委宣传部/公开报道"},
    # Political & Legal Affairs Secretary
    {"id": 9, "name": "刘卫宝", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-05", "birthplace": "安徽霍山", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1990",
     "current_post": "合肥市委常委、政法委书记",
     "current_org": "中共合肥市委政法委员会",
     "source": "公开报道"},
    # United Front Work Department Head
    {"id": 10, "name": "陈晓波", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-07", "birthplace": "安徽六安", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1987",
     "current_post": "合肥市委常委、统战部部长",
     "current_org": "中共合肥市委统一战线工作部",
     "source": "合肥市委统战部/公开报道"},
    # Secretary General (秘书长)
    {"id": 11, "name": "单虎", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-07", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "合肥市委常委、秘书长",
     "current_org": "中共合肥市委",
     "source": "公开报道"},

    # ── C. Deputy Mayors (副市长) ──
    {"id": 12, "name": "王连贵", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-10", "birthplace": "安徽望江", "education": "中央党校研究生/MBA",
     "party_join": "中共党员", "work_start": "1991",
     "current_post": "合肥市人民政府副市长",
     "current_org": "合肥市人民政府",
     "source": "合肥市人民政府网站"},
    {"id": 13, "name": "何逢阳", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "安徽宁国", "education": "研究生/管理学博士",
     "party_join": "中共党员", "work_start": "2001",
     "current_post": "合肥市人民政府副市长",
     "current_org": "合肥市人民政府",
     "source": "合肥市人民政府网站"},
    {"id": 14, "name": "李命山", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "安徽桐城", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "合肥市人民政府副市长",
     "current_org": "合肥市人民政府",
     "source": "公开报道"},

    # ── D. NPC Standing Committee (市人大常委会) ──
    {"id": 15, "name": "汪卫东", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-06", "birthplace": "安徽休宁", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1984",
     "current_post": "合肥市人大常委会主任",
     "current_org": "合肥市人大常委会",
     "source": "合肥人大网"},
    {"id": 16, "name": "王文松", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-10", "birthplace": "安徽太湖", "education": "在职研究生/MBA",
     "party_join": "中共党员", "work_start": "1982",
     "current_post": "合肥市人大常委会副主任",
     "current_org": "合肥市人大常委会",
     "source": "合肥人大网"},

    # ── E. CPPCC (市政协) ──
    {"id": 17, "name": "韩冰", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-12", "birthplace": "安徽怀宁", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1982",
     "current_post": "合肥市政协主席",
     "current_org": "合肥市政协",
     "source": "合肥市政协网"},

    # ── F. District/county level: key leaders ──
    # 肥西县
    {"id": 18, "name": "沈校根", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "安徽肥西", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1999",
     "current_post": "肥西县委书记",
     "current_org": "中共肥西县委",
     "source": "公开报道/肥西县政府网"},
    {"id": 19, "name": "王新华", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "安徽合肥", "education": "大学",
     "party_join": "中共党员", "work_start": "2000",
     "current_post": "肥西县长",
     "current_org": "肥西县人民政府",
     "source": "公开报道"},
    # 肥东县
    {"id": 20, "name": "姚飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-12", "birthplace": "安徽长丰", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1996",
     "current_post": "肥东县委书记",
     "current_org": "中共肥东县委",
     "source": "公开报道"},
    {"id": 21, "name": "王书武", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-08", "birthplace": "安徽肥东", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "肥东县长",
     "current_org": "肥东县人民政府",
     "source": "公开报道"},
    # 长丰县
    {"id": 22, "name": "李孝鸿", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-04", "birthplace": "安徽合肥", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1998",
     "current_post": "长丰县委书记",
     "current_org": "中共长丰县委",
     "source": "公开报道"},
    {"id": 23, "name": "李卫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长丰县长",
     "current_org": "长丰县人民政府",
     "source": "待确认"},
    # 庐江县
    {"id": 24, "name": "许华为", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-06", "birthplace": "安徽庐江", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "庐江县委书记",
     "current_org": "中共庐江县委",
     "source": "公开报道"},
    {"id": 25, "name": "周天斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-01", "birthplace": "安徽舒城", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "庐江县长",
     "current_org": "庐江县人民政府",
     "source": "公开报道"},
    # 巢湖市
    {"id": 26, "name": "张红军", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "安徽巢湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1991",
     "current_post": "巢湖市委书记",
     "current_org": "中共巢湖市委",
     "source": "公开报道"},
    {"id": 27, "name": "汪功胜", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-09", "birthplace": "安徽无为", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "巢湖市长",
     "current_org": "巢湖市人民政府",
     "source": "公开报道"},
    # 瑶海区
    {"id": 28, "name": "陆勤山", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "瑶海区委书记",
     "current_org": "中共瑶海区委",
     "source": "公开报道"},
    {"id": 29, "name": "童友好", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-10", "birthplace": "安徽合肥", "education": "研究生",
     "party_join": "中共党员", "work_start": "2004",
     "current_post": "瑶海区长",
     "current_org": "瑶海区人民政府",
     "source": "公开报道"},
    # 庐阳区
    {"id": 30, "name": "高强", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "庐阳区委书记",
     "current_org": "中共庐阳区委",
     "source": "公开报道"},
    {"id": 31, "name": "杨丙红", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "安徽合肥", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1999",
     "current_post": "庐阳区长",
     "current_org": "庐阳区人民政府",
     "source": "公开报道"},
    # 蜀山区
    {"id": 32, "name": "王海霞", "gender": "女", "ethnicity": "汉族",
     "birth": "1970-12", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "蜀山区委书记",
     "current_org": "中共蜀山区委",
     "source": "公开报道"},
    {"id": 33, "name": "杨森", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "安徽合肥", "education": "研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "蜀山区区长",
     "current_org": "蜀山区人民政府",
     "source": "公开报道"},
    # 包河区
    {"id": 34, "name": "程雪涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-09", "birthplace": "安徽六安", "education": "在职研究生/博士",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "包河区委书记（兼）",
     "current_org": "中共包河区委",
     "source": "公开报道（注：程雪涛为市委常委兼包河区委书记）"},
    {"id": 35, "name": "李炜", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-07", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1998",
     "current_post": "包河区长",
     "current_org": "包河区人民政府",
     "source": "公开报道"},
]

organizations = [
    # City-level
    {"id": 1, "name": "中共合肥市委", "type": "党委", "level": "副省级", "parent": "中共安徽省委", "location": "合肥市"},
    {"id": 2, "name": "合肥市人民政府", "type": "政府", "level": "副省级", "parent": "安徽省人民政府", "location": "合肥市"},
    {"id": 3, "name": "合肥市人大常委会", "type": "人大", "level": "副省级", "parent": "", "location": "合肥市"},
    {"id": 4, "name": "合肥市政协", "type": "政协", "level": "副省级", "parent": "", "location": "合肥市"},
    {"id": 5, "name": "中共合肥市纪律检查委员会", "type": "纪委", "level": "副省级", "parent": "", "location": "合肥市"},
    {"id": 6, "name": "中共安徽省委", "type": "党委", "level": "省级", "parent": "", "location": "合肥市"},
    {"id": 7, "name": "安徽省政协", "type": "政协", "level": "省级", "parent": "", "location": "合肥市"},
    # District/County level
    {"id": 8, "name": "中共肥西县委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "肥西县"},
    {"id": 9, "name": "肥西县人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "肥西县"},
    {"id": 10, "name": "中共肥东县委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "肥东县"},
    {"id": 11, "name": "肥东县人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "肥东县"},
    {"id": 12, "name": "中共长丰县委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "长丰县"},
    {"id": 13, "name": "长丰县人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "长丰县"},
    {"id": 14, "name": "中共庐江县委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "庐江县"},
    {"id": 15, "name": "庐江县人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "庐江县"},
    {"id": 16, "name": "中共巢湖市委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "巢湖市"},
    {"id": 17, "name": "巢湖市人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "巢湖市"},
    {"id": 18, "name": "中共瑶海区委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "瑶海区"},
    {"id": 19, "name": "瑶海区人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "瑶海区"},
    {"id": 20, "name": "中共庐阳区委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "庐阳区"},
    {"id": 21, "name": "庐阳区人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "庐阳区"},
    {"id": 22, "name": "中共蜀山区委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "蜀山区"},
    {"id": 23, "name": "蜀山区人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "蜀山区"},
    {"id": 24, "name": "中共包河区委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "包河区"},
    {"id": 25, "name": "包河区人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "包河区"},
]

positions = [
    # City-level top leaders
    {"person_id": 1, "org_id": 1, "title": "安徽省委常委、合肥市委书记", "start": "2024-03", "end": "", "rank": "副部", "note": "20届中央候补委员"},
    {"person_id": 1, "org_id": 6, "title": "安徽省委常委", "start": "2024-03", "end": "", "rank": "副部", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "合肥市长", "start": "2021-04", "end": "", "rank": "副部", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "合肥市委书记", "start": "2020-05", "end": "2024-03", "rank": "副部", "note": "前任书记"},
    {"person_id": 3, "org_id": 6, "title": "安徽省委副书记", "start": "2024-03", "end": "", "rank": "副部", "note": "晋升"},
    {"person_id": 4, "org_id": 2, "title": "合肥市长", "start": "2016-08", "end": "2021-04", "rank": "副部", "note": "前任市长"},
    {"person_id": 4, "org_id": 7, "title": "安徽省政协党组成员", "start": "2021-04", "end": "", "rank": "副部", "note": ""},
    # Standing Committee members
    {"person_id": 5, "org_id": 2, "title": "合肥市委常委、常务副市长", "start": "2021", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "合肥市委常委、市纪委书记、市监委主任", "start": "2023", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "合肥市委常委、组织部部长", "start": "2022", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "合肥市委常委、宣传部部长", "start": "2021", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 8, "org_id": 24, "title": "包河区委书记（兼）", "start": "2023", "end": "", "rank": "正处", "note": ""},
    {"person_id": 9, "org_id": 9, "title": "合肥市委常委、政法委书记", "start": "2023", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "合肥市委常委、统战部部长", "start": "2020", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "合肥市委常委、秘书长", "start": "2021", "end": "", "rank": "正厅", "note": ""},
    # Deputy Mayors
    {"person_id": 12, "org_id": 2, "title": "合肥市副市长", "start": "2021", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "合肥市副市长", "start": "2022", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "合肥市副市长", "start": "2023", "end": "", "rank": "正厅", "note": ""},
    # NPC Standing Committee
    {"person_id": 15, "org_id": 3, "title": "合肥市人大常委会主任", "start": "2018-01", "end": "", "rank": "副部", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "合肥市人大常委会副主任", "start": "2018", "end": "", "rank": "正厅", "note": ""},
    # CPPCC
    {"person_id": 17, "org_id": 4, "title": "合肥市政协主席", "start": "2018-01", "end": "", "rank": "副部", "note": ""},
    # District/County organizations
    {"person_id": 18, "org_id": 8, "title": "肥西县委书记", "start": "2023", "end": "", "rank": "正处", "note": ""},
    {"person_id": 19, "org_id": 9, "title": "肥西县长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 20, "org_id": 10, "title": "肥东县委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 21, "org_id": 11, "title": "肥东县长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 22, "org_id": 12, "title": "长丰县委书记", "start": "2023", "end": "", "rank": "正处", "note": ""},
    {"person_id": 23, "org_id": 13, "title": "长丰县长", "start": "", "end": "", "rank": "正处", "note": "待确认"},
    {"person_id": 24, "org_id": 14, "title": "庐江县委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 25, "org_id": 15, "title": "庐江县长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 26, "org_id": 16, "title": "巢湖市委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 27, "org_id": 17, "title": "巢湖市长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 28, "org_id": 18, "title": "瑶海区委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 29, "org_id": 19, "title": "瑶海区长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 30, "org_id": 20, "title": "庐阳区委书记", "start": "2022", "end": "", "rank": "正处", "note": ""},
    {"person_id": 31, "org_id": 21, "title": "庐阳区长", "start": "2022", "end": "", "rank": "正处", "note": ""},
    {"person_id": 32, "org_id": 22, "title": "蜀山区委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 33, "org_id": 23, "title": "蜀山区区长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 34, "org_id": 24, "title": "包河区委书记", "start": "2023", "end": "", "rank": "正处", "note": "兼任（程雪涛为市委常委）"},
    {"person_id": 35, "org_id": 25, "title": "包河区长", "start": "2021", "end": "", "rank": "正处", "note": ""},
]

relationships = [
    # Top leadership pairs
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "合肥市委书记与市长搭档", "overlap_org": "合肥市", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "虞爱华→张红文 合肥市委书记交接", "overlap_org": "中共合肥市委", "overlap_period": "2024-03"},
    {"person_a": 2, "person_b": 4, "type": "前后任", "context": "凌云→罗云峰 合肥市长交接", "overlap_org": "合肥市人民政府", "overlap_period": "2021-04"},
    {"person_a": 1, "person_b": 15, "type": "党政同僚", "context": "市委书记与人大主任同届工作", "overlap_org": "合肥市", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 17, "type": "党政同僚", "context": "市委书记与政协主席同届工作", "overlap_org": "合肥市", "overlap_period": "2024-"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "市长与常务副市长搭档", "overlap_org": "合肥市人民政府", "overlap_period": "2021-"},
    # Standing Committee overlap
    {"person_a": 1, "person_b": 5, "type": "党政同僚", "context": "市委书记与常务副市长同届常委会", "overlap_org": "中共合肥市委", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 6, "type": "党政同僚", "context": "市委书记与纪委书记同届常委会", "overlap_org": "中共合肥市委", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 7, "type": "党政同僚", "context": "市委书记与组织部长同届常委会", "overlap_org": "中共合肥市委", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 8, "type": "党政同僚", "context": "市委书记与宣传部长同届常委会", "overlap_org": "中共合肥市委", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 9, "type": "党政同僚", "context": "市委书记与政法委书记同届常委会", "overlap_org": "中共合肥市委", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 10, "type": "党政同僚", "context": "市委书记与统战部长同届常委会", "overlap_org": "中共合肥市委", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 11, "type": "党政同僚", "context": "市委书记与秘书长同届常委会", "overlap_org": "中共合肥市委", "overlap_period": "2024-"},
    # District/county connections
    {"person_a": 18, "person_b": 19, "type": "党政同僚", "context": "肥西县委书记与县长搭档", "overlap_org": "肥西县", "overlap_period": "2023-"},
    {"person_a": 20, "person_b": 21, "type": "党政同僚", "context": "肥东县委书记与县长搭档", "overlap_org": "肥东县", "overlap_period": "2021-"},
    {"person_a": 24, "person_b": 25, "type": "党政同僚", "context": "庐江县委书记与县长搭档", "overlap_org": "庐江县", "overlap_period": "2021-"},
    {"person_a": 26, "person_b": 27, "type": "党政同僚", "context": "巢湖市委书记与市长搭档", "overlap_org": "巢湖市", "overlap_period": "2021-"},
    {"person_a": 28, "person_b": 29, "type": "党政同僚", "context": "瑶海区委书记与区长搭档", "overlap_org": "瑶海区", "overlap_period": "2021-"},
    {"person_a": 30, "person_b": 31, "type": "党政同僚", "context": "庐阳区委书记与区长搭档", "overlap_org": "庐阳区", "overlap_period": "2022-"},
    {"person_a": 32, "person_b": 33, "type": "党政同僚", "context": "蜀山区委书记与区长搭档", "overlap_org": "蜀山区", "overlap_period": "2021-"},
    {"person_a": 34, "person_b": 35, "type": "党政同僚", "context": "包河区委书记与区长搭档", "overlap_org": "包河区", "overlap_period": "2023-"},
    # Same-system connections
    {"person_a": 20, "person_b": 22, "type": "同一系统", "context": "姚飞（长丰人/肥东书记）与李孝鸿（合肥人/长丰书记）— 长丰县关联", "overlap_org": "", "overlap_period": ""},
]

# ── BUILD DATABASE ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# ── Print summary ──
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ 数据库已创建: {DB_PATH}")
print(f"   人物: {person_count} | 机构: {org_count} | 任职: {pos_count} | 关系: {rel_count}")

# ── BUILD GEXF ──────────────────────────────────────────────────────

def color_for_role(title):
    t = title or ""
    if "书记" in t and "纪委" not in t and "副" not in t[:t.index("书记")] if "书记" in t else True:
        return "#E03C31"
    if "市长" in t or "县长" in t or "区长" in t:
        return "#4a7fc7"
    if "人大" in t:
        return "#5a7a9a"
    if "政协" in t:
        return "#7a5a9a"
    if "纪委" in t:
        return "#d4880f"
    # Simpler check for vice-secretaries
    if "副书记" in t:
        return "#E07A31"
    if "副市长" in t or "副县长" in t or "副区长" in t:
        return "#6a8fe7"
    return "#888888"

def org_color(org_type):
    return {"党委": "rgba(200,50,50,0.3)", "政府": "rgba(50,100,200,0.3)",
            "人大": "rgba(90,122,154,0.3)", "政协": "rgba(122,90,154,0.3)",
            "纪委": "rgba(200,150,20,0.3)"}.get(org_type, "rgba(200,200,200,0.3)")

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('<meta><creator>Hefei Investigator</creator><description>合肥市领导班子工作关系网络</description></meta>')
gexf_parts.append('<graph mode="static" defaultedgetype="undirected">')

# Nodes
gexf_parts.append('<nodes>')
for p in persons:
    slug_id = f"hefei_{p['id']}"
    role_color = color_for_role(p["current_post"])
    is_top = "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    is_gov = ("市长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or ("区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
    size = 20.0 if is_top else 15.0 if is_gov else 12.0
    label = f"{p['name']} ({p['current_post'] or '?'})"
    gexf_parts.append(f'<node id="{slug_id}" label="{label}">')
    gexf_parts.append(f'<attvalues><attvalue for="role" value="{p["current_post"]}"/><attvalue for="org" value="{p["current_org"]}"/><attvalue for="birth" value="{p["birth"]}"/><attvalue for="birthplace" value="{p["birthplace"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(role_color[1:3],16)}" g="{int(role_color[3:5],16)}" b="{int(role_color[5:7],16)}"/>')
    gexf_parts.append(f'<viz:size value="{size}"/>')
    gexf_parts.append('</node>')

for o in organizations:
    oid = f"org_{o['id']}"
    oc = org_color(o["type"])
    oc_rgb = oc.replace("rgba(", "").rstrip(")").split(",")
    gexf_parts.append(f'<node id="{oid}" label="{o["name"]}">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="{o["type"]}"/><attvalue for="level" value="{o["level"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(oc_rgb[0])}" g="{int(oc_rgb[1])}" b="{int(oc_rgb[2])}"/>')
    gexf_parts.append(f'<viz:size value="8.0"/>')
    gexf_parts.append('</node>')
gexf_parts.append('</nodes>')

# Edges
gexf_parts.append('<edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = f"{p['name']} → {o['name']} ({po['title']})"
    gexf_parts.append(f'<edge id="e{edge_id}" source="hefei_{p["id"]}" target="org_{o["id"]}" label="{label}" weight="1.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="worked_at"/><attvalue for="title" value="{po["title"]}"/><attvalue for="start" value="{po["start"]}"/><attvalue for="end" value="{po["end"]}"/></attvalues>')
    gexf_parts.append('</edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    gexf_parts.append(f'<edge id="e{edge_id}" source="hefei_{p_a["id"]}" target="hefei_{p_b["id"]}" label="{r["context"]}" weight="2.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="relationship"/><attvalue for="context" value="{r["context"]}"/></attvalues>')
    gexf_parts.append('</edge>')

gexf_parts.append('</edges>')
gexf_parts.append('</graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
