#!/usr/bin/env python3
"""
Build SQLite databases + GEXF graphs for ALL remaining county/district-level
sub-divisions of 赣州市, Jiangxi province (18 divisions).

For each division, includes at minimum the current party secretary and
government head (区长/县长/市长/区委书记/县委书记/市委书记),
plus predecessor chains where available.

Divisions: 章贡区, 南康区, 赣县区, 信丰县, 大余县, 上犹县,
崇义县, 安远县, 定南县, 全南县, 宁都县, 于都县, 兴国县,
会昌县, 寻乌县, 石城县, 瑞金市, 龙南市
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# Division Config — each entry defines a sub-division with its data
# =========================================================================

divisions = []

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 章贡区 (Zhanggong District)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "章贡区",
    "db": "zhanggong_network.db",
    "gexf": "zhanggong_network.gexf",
    "label": "章贡区领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"连天浪", "gender":"男", "ethnicity":"汉族",
         "birth":"1969-03", "birthplace":"江西信丰", "education":"大学学历",
         "party_join":"1987-06", "work_start":"1987-08",
         "current_post":"赣州市副市长（原章贡区委书记）", "current_org":"赣州市人民政府",
         "source":"https://www.ganzhou.gov.cn/gzszf/ltl/zw_sz.shtml"},
        {"id":2, "name":"刘志怀", "gender":"男", "ethnicity":"汉族",
         "birth":"1970-10", "birthplace":"江西安远", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"章贡区委副书记、区长", "current_org":"章贡区人民政府",
         "source":"https://www.zgq.gov.cn"},
        {"id":3, "name":"刘文华", "gender":"男", "ethnicity":"汉族",
         "birth":"", "birthplace":"", "education":"",
         "party_join":"中共党员", "work_start":"",
         "current_post":"（原章贡区委书记→赣州市委副书记、统战部长）", "current_org":"中共赣州市委员会",
         "source":"公开报道"},
    ],
    "orgs": [
        {"id":1, "name":"中共章贡区委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州章贡"},
        {"id":2, "name":"章贡区人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州章贡"},
        {"id":3, "name":"赣州市人民政府", "type":"政府", "level":"地级", "parent":"江西省人民政府", "location":"江西赣州"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"章贡区委书记", "start":"", "end":"", "rank":"县处级正职", "note":"后升任赣州市副市长"},
        {"id":2, "person_id":1, "org_id":3, "title":"赣州市副市长", "start":"", "end":"", "rank":"副厅级", "note":"现任"},
        {"id":3, "person_id":2, "org_id":2, "title":"章贡区委副书记、区长", "start":"", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":4, "person_id":3, "org_id":1, "title":"章贡区委书记", "start":"2016", "end":"2020", "rank":"县处级正职", "note":"前任"},
    ],
    "relationships": [
        {"id":1, "person_a_id":1, "person_b_id":2, "type":"党政搭档", "context":"连天浪与刘志怀在章贡区党政搭档", "overlap_org":"章贡区", "overlap_period":""},
    ],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 南康区 (Nankang District)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "南康区",
    "db": "nankang_network.db",
    "gexf": "nankang_network.gexf",
    "label": "南康区领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"何善锦", "gender":"男", "ethnicity":"汉族",
         "birth":"1968-09", "birthplace":"江西信丰", "education":"省委党校研究生",
         "party_join":"1991-10", "work_start":"1989-08",
         "current_post":"赣州市委常委、南康区委书记", "current_org":"中共南康区委员会",
         "source":"https://www.nkjx.gov.cn"},
        {"id":2, "name":"李赣兴", "gender":"男", "ethnicity":"汉族",
         "birth":"1974-11", "birthplace":"江西赣县", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"",
         "current_post":"南康区委副书记、区长", "current_org":"南康区人民政府",
         "source":"https://www.nkjx.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共南康区委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州南康"},
        {"id":2, "name":"南康区人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州南康"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"南康区委书记（赣州市委常委兼任）", "start":"2021", "end":"", "rank":"副厅级", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"南康区委副书记、区长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 赣县区 (Ganxian District)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "赣县区",
    "db": "ganxian_network.db",
    "gexf": "ganxian_network.gexf",
    "label": "赣县区领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"廖永平", "gender":"男", "ethnicity":"汉族",
         "birth":"1971-07", "birthplace":"江西宁都", "education":"大学学历/MPA",
         "party_join":"1993-12", "work_start":"1992-08",
         "current_post":"赣县区委书记", "current_org":"中共赣县区委员会",
         "source":"https://www.ganxian.gov.cn"},
        {"id":2, "name":"刘文彦", "gender":"男", "ethnicity":"汉族",
         "birth":"1970-10", "birthplace":"江西宁都", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"赣县区委副书记、区长", "current_org":"赣县区人民政府",
         "source":"https://www.ganxian.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共赣县区委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州赣县"},
        {"id":2, "name":"赣县区人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州赣县"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"赣县区委书记", "start":"2020", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"赣县区委副书记、区长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 信丰县 (Xinfeng County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "信丰县",
    "db": "xinfeng_network.db",
    "gexf": "xinfeng_network.gexf",
    "label": "信丰县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"袁炎", "gender":"男", "ethnicity":"汉族",
         "birth":"1972-09", "birthplace":"江西赣州", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"1990-07",
         "current_post":"信丰县委书记", "current_org":"中共信丰县委员会",
         "source":"https://www.jxxf.gov.cn"},
        {"id":2, "name":"张琳", "gender":"男", "ethnicity":"汉族",
         "birth":"1974-10", "birthplace":"江西兴国", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"信丰县委副书记、县长", "current_org":"信丰县人民政府",
         "source":"https://www.jxxf.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共信丰县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州信丰"},
        {"id":2, "name":"信丰县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州信丰"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"信丰县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"信丰县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. 大余县 (Dayu County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "大余县",
    "db": "dayu_network.db",
    "gexf": "dayu_network.gexf",
    "label": "大余县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"韩相云", "gender":"男", "ethnicity":"汉族",
         "birth":"1974-07", "birthplace":"江西寻乌", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"",
         "current_post":"大余县委书记", "current_org":"中共大余县委员会",
         "source":"https://www.jxdy.gov.cn"},
        {"id":2, "name":"曾志平", "gender":"男", "ethnicity":"汉族",
         "birth":"1976-05", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"大余县委副书记、县长", "current_org":"大余县人民政府",
         "source":"https://www.jxdy.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共大余县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州大余"},
        {"id":2, "name":"大余县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州大余"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"大余县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"大余县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. 上犹县 (Shangyou County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "上犹县",
    "db": "shangyou_network.db",
    "gexf": "shangyou_network.gexf",
    "label": "上犹县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"刘洪梅", "gender":"女", "ethnicity":"汉族",
         "birth":"1974-11", "birthplace":"江西赣州", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"",
         "current_post":"上犹县委书记", "current_org":"中共上犹县委员会",
         "source":"https://www.shangyou.gov.cn"},
        {"id":2, "name":"钟晓斌", "gender":"男", "ethnicity":"汉族",
         "birth":"1974-12", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"上犹县委副书记、县长", "current_org":"上犹县人民政府",
         "source":"https://www.shangyou.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共上犹县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州上犹"},
        {"id":2, "name":"上犹县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州上犹"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"上犹县委书记", "start":"2023", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"上犹县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. 崇义县 (Chongyi County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "崇义县",
    "db": "chongyi_network.db",
    "gexf": "chongyi_network.gexf",
    "label": "崇义县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"李国泉", "gender":"男", "ethnicity":"汉族",
         "birth":"1974-08", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"崇义县委书记", "current_org":"中共崇义县委员会",
         "source":"https://www.chongyi.gov.cn"},
        {"id":2, "name":"黄斌", "gender":"男", "ethnicity":"汉族",
         "birth":"1976-05", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"崇义县委副书记、县长", "current_org":"崇义县人民政府",
         "source":"https://www.chongyi.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共崇义县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州崇义"},
        {"id":2, "name":"崇义县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州崇义"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"崇义县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"崇义县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. 安远县 (Anyuan County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "安远县",
    "db": "anyuan_network.db",
    "gexf": "anyuan_network.gexf",
    "label": "安远县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"杨有谷", "gender":"男", "ethnicity":"汉族",
         "birth":"1975-11", "birthplace":"江西赣州", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"安远县委书记", "current_org":"中共安远县委员会",
         "source":"https://www.ay.gov.cn"},
        {"id":2, "name":"钟小刚", "gender":"男", "ethnicity":"汉族",
         "birth":"1977-11", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"安远县委副书记、县长", "current_org":"安远县人民政府",
         "source":"https://www.ay.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共安远县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州安远"},
        {"id":2, "name":"安远县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州安远"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"安远县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"安远县委副书记、县长", "start":"2023", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. 定南县 (Dingnan County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "定南县",
    "db": "dingnan_network.db",
    "gexf": "dingnan_network.gexf",
    "label": "定南县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"龙小东", "gender":"男", "ethnicity":"汉族",
         "birth":"1971-11", "birthplace":"江西赣州", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"",
         "current_post":"定南县委书记", "current_org":"中共定南县委员会",
         "source":"https://www.dingnan.gov.cn"},
        {"id":2, "name":"陈钰滢", "gender":"女", "ethnicity":"汉族",
         "birth":"1977-12", "birthplace":"江西赣州", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"",
         "current_post":"定南县委副书记、县长", "current_org":"定南县人民政府",
         "source":"https://www.dingnan.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共定南县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州定南"},
        {"id":2, "name":"定南县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州定南"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"定南县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"定南县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. 全南县 (Quannan County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "全南县",
    "db": "quannan_network.db",
    "gexf": "quannan_network.gexf",
    "label": "全南县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"曾平", "gender":"男", "ethnicity":"汉族",
         "birth":"1970-11", "birthplace":"江西赣州", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"全南县委书记", "current_org":"中共全南县委员会",
         "source":"https://www.quannan.gov.cn"},
        {"id":2, "name":"边建忠", "gender":"男", "ethnicity":"汉族",
         "birth":"1976-09", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"全南县委副书记、县长", "current_org":"全南县人民政府",
         "source":"https://www.quannan.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共全南县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州全南"},
        {"id":2, "name":"全南县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州全南"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"全南县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"全南县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 11. 宁都县 (Ningdu County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "宁都县",
    "db": "ningdu_network.db",
    "gexf": "ningdu_network.gexf",
    "label": "宁都县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"傅小新", "gender":"男", "ethnicity":"汉族",
         "birth":"1973-10", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"宁都县委书记", "current_org":"中共宁都县委员会",
         "source":"https://www.ningdu.gov.cn"},
        {"id":2, "name":"何国杰", "gender":"男", "ethnicity":"汉族",
         "birth":"1975-11", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"宁都县委副书记、县长", "current_org":"宁都县人民政府",
         "source":"https://www.ningdu.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共宁都县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州宁都"},
        {"id":2, "name":"宁都县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州宁都"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"宁都县委书记", "start":"2023", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"宁都县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 12. 于都县 (Yudu County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "于都县",
    "db": "yudu_network.db",
    "gexf": "yudu_network.gexf",
    "label": "于都县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"黄法", "gender":"男", "ethnicity":"汉族",
         "birth":"1970-08", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"于都县委书记", "current_org":"中共于都县委员会",
         "source":"https://www.yudu.gov.cn"},
        {"id":2, "name":"李松柏", "gender":"男", "ethnicity":"汉族",
         "birth":"1976-12", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"于都县委副书记、县长", "current_org":"于都县人民政府",
         "source":"https://www.yudu.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共于都县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州于都"},
        {"id":2, "name":"于都县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州于都"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"于都县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"于都县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 13. 兴国县 (Xingguo County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "兴国县",
    "db": "xingguo_network.db",
    "gexf": "xingguo_network.gexf",
    "label": "兴国县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"赖晓军", "gender":"男", "ethnicity":"汉族",
         "birth":"1974-07", "birthplace":"江西赣州", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"兴国县委书记", "current_org":"中共兴国县委员会",
         "source":"https://www.xingguo.gov.cn"},
        {"id":2, "name":"刘章宏", "gender":"男", "ethnicity":"汉族",
         "birth":"1976-12", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"兴国县委副书记、县长", "current_org":"兴国县人民政府",
         "source":"https://www.xingguo.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共兴国县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州兴国"},
        {"id":2, "name":"兴国县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州兴国"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"兴国县委书记", "start":"2023", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"兴国县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 14. 会昌县 (Huichang County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "会昌县",
    "db": "huichang_network.db",
    "gexf": "huichang_network.gexf",
    "label": "会昌县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"潘金城", "gender":"男", "ethnicity":"汉族",
         "birth":"1975-12", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"会昌县委书记", "current_org":"中共会昌县委员会",
         "source":"https://www.huichang.gov.cn"},
        {"id":2, "name":"李德伟", "gender":"男", "ethnicity":"汉族",
         "birth":"1976-04", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"会昌县委副书记、县长", "current_org":"会昌县人民政府",
         "source":"https://www.huichang.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共会昌县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州会昌"},
        {"id":2, "name":"会昌县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州会昌"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"会昌县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"会昌县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 15. 寻乌县 (Xunwu County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "寻乌县",
    "db": "xunwu_network.db",
    "gexf": "xunwu_network.gexf",
    "label": "寻乌县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"蓝贤林", "gender":"男", "ethnicity":"畲族",
         "birth":"1973-10", "birthplace":"江西赣州", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"寻乌县委书记", "current_org":"中共寻乌县委员会",
         "source":"https://www.xunwu.gov.cn"},
        {"id":2, "name":"何善祥", "gender":"男", "ethnicity":"汉族",
         "birth":"1973-11", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"寻乌县委副书记、县长", "current_org":"寻乌县人民政府",
         "source":"https://www.xunwu.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共寻乌县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州寻乌"},
        {"id":2, "name":"寻乌县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州寻乌"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"寻乌县委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"寻乌县委副书记、县长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 16. 石城县 (Shicheng County)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "石城县",
    "db": "shicheng_network.db",
    "gexf": "shicheng_network.gexf",
    "label": "石城县领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"张小川", "gender":"男", "ethnicity":"汉族",
         "birth":"1973-10", "birthplace":"江西赣州", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"",
         "current_post":"石城县委书记", "current_org":"中共石城县委员会",
         "source":"https://www.shicheng.gov.cn"},
        {"id":2, "name":"刘诗河", "gender":"男", "ethnicity":"汉族",
         "birth":"1975-09", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"石城县委副书记、县长", "current_org":"石城县人民政府",
         "source":"https://www.shicheng.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共石城县委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州石城"},
        {"id":2, "name":"石城县人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州石城"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"石城县委书记", "start":"2023", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"石城县委副书记、县长", "start":"2022", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 17. 瑞金市 (Ruijin City — county-level city)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "瑞金市",
    "db": "ruijin_network.db",
    "gexf": "ruijin_network.gexf",
    "label": "瑞金市领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"尹忠", "gender":"男", "ethnicity":"汉族",
         "birth":"1970-12", "birthplace":"江西赣州", "education":"省委党校研究生",
         "party_join":"中共党员", "work_start":"",
         "current_post":"瑞金市委书记", "current_org":"中共瑞金市委员会",
         "source":"https://www.ruijin.gov.cn"},
        {"id":2, "name":"刘春林", "gender":"男", "ethnicity":"汉族",
         "birth":"1975-09", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"瑞金市委副书记、市长", "current_org":"瑞金市人民政府",
         "source":"https://www.ruijin.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共瑞金市委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州瑞金"},
        {"id":2, "name":"瑞金市人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州瑞金"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"瑞金市委书记", "start":"2023", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"瑞金市委副书记、市长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 18. 龙南市 (Longnan City — county-level city)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
divisions.append({
    "name": "龙南市",
    "db": "longnan_network.db",
    "gexf": "longnan_network.gexf",
    "label": "龙南市领导班子工作关系网络",
    "persons": [
        {"id":1, "name":"钟旭辉", "gender":"男", "ethnicity":"汉族",
         "birth":"1968-11", "birthplace":"江西赣州", "education":"大学学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"龙南市委书记", "current_org":"中共龙南市委员会",
         "source":"https://www.jxln.gov.cn"},
        {"id":2, "name":"彭江闽", "gender":"男", "ethnicity":"汉族",
         "birth":"1975-07", "birthplace":"江西赣州", "education":"研究生学历",
         "party_join":"中共党员", "work_start":"",
         "current_post":"龙南市委副书记、市长", "current_org":"龙南市人民政府",
         "source":"https://www.jxln.gov.cn"},
    ],
    "orgs": [
        {"id":1, "name":"中共龙南市委员会", "type":"党委", "level":"县处级", "parent":"中共赣州市委员会", "location":"江西赣州龙南"},
        {"id":2, "name":"龙南市人民政府", "type":"政府", "level":"县处级", "parent":"赣州市人民政府", "location":"江西赣州龙南"},
    ],
    "positions": [
        {"id":1, "person_id":1, "org_id":1, "title":"龙南市委书记", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
        {"id":2, "person_id":2, "org_id":2, "title":"龙南市委副书记、市长", "start":"2021", "end":"", "rank":"县处级正职", "note":"现任"},
    ],
    "relationships": [],
})


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_sqlite(div):
    """Build SQLite database for one division."""
    db_name = div["db"]
    db_path = os.path.join(BASE, "data/database", db_name)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in div["persons"]:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in div["orgs"]:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in div["positions"]:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in div["relationships"]:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    return db_path, counts


def pcolor_viz(post):
    """Return viz:color RGB string based on post title."""
    post = post or ""
    if "书记" in post and ("区委" in post or "县委" in post or "市委" in post):
        return "230,50,50"  # red for party secretary
    if "区长" in post or "县长" in post or "市长" in post or "副市长" in post:
        if "副" not in post:
            return "50,100,230"  # blue for gov head
        return "80,140,230"  # lighter blue for deputies
    return "120,120,120"  # grey


def ocolor_viz(otype):
    return {"党委":"255,200,200","政府":"200,200,255"}.get(otype, "200,200,200")


def build_gexf(div):
    """Build GEXF graph file for one division."""
    gexf_name = div["gexf"]
    gexf_path = os.path.join(BASE, "data/graph", gexf_name)
    os.makedirs(os.path.dirname(gexf_path), exist_ok=True)

    persons = div["persons"]
    orgs = div["orgs"]
    positions = div["positions"]
    relationships = div["relationships"]

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus-junior</creator>')
    lines.append(f'    <description>{div["label"]} - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0","type"), ("1","birth"), ("2","birthplace"), ("3","current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0","type"), ("1","start"), ("2","end"), ("3","context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = pcolor_viz(p.get("current_post",""))
        sz = "20.0" if p["id"] <= 2 else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0","person"), ("1",p.get("birth","")), ("2",p.get("birthplace","")), ("3",p.get("current_post",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in orgs:
        c = ocolor_viz(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0","organization"), ("1",""), ("2",o.get("location","")), ("3","")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0","worked_at"), ("1",pos.get("start","")), ("2",pos.get("end","")), ("3",pos.get("note",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0",r["type"]), ("1",""), ("2",""), ("3",r.get("context",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(orgs)
    te = len(positions) + len(relationships)
    return gexf_path, tn, te


# =========================================================================
# MAIN: Build all 18 divisions
# =========================================================================

print("=" * 70)
print(f"Building databases for ALL remaining 赣州市 county/district-level divisions")
print(f"Date: {today}")
print("=" * 70)

total_db = 0
total_gexf = 0
all_db_ok = True

for div in divisions:
    div_name = div["name"]
    print(f"\n{'─'*50}")
    print(f"▶ {div_name} ({div['db']})")

    # SQLite
    db_path, counts = build_sqlite(div)
    print(f"  ✓ SQLite: {db_path}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    # GEXF
    gexf_path, tn, te = build_gexf(div)
    print(f"  ✓ GEXF: {gexf_path}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    # Verify
    if not os.path.exists(db_path):
        print(f"  ✗ ERROR: DB file not created!")
        all_db_ok = False
    else:
        total_db += 1
    if not os.path.exists(gexf_path):
        print(f"  ✗ ERROR: GEXF file not created!")
        all_db_ok = False
    else:
        total_gexf += 1

print(f"\n{'='*70}")
print(f"BUILD COMPLETE")
print(f"  Databases: {total_db}/18")
print(f"  GEXF graphs: {total_gexf}/18")
print(f"  Status: {'✓ ALL OK' if all_db_ok else '✗ SOME FAILED'}")
print(f"{'='*70}")
