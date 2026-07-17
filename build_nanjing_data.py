#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 南京市 (Nanjing City) leadership network.

Covers: City-level leadership (市委书记, 市长, 副市长, etc.),
all 11 districts (区委书记 + 区长), predecessors, and
the city-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/nanjing_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/nanjing_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委 ──
    # 周红波 — 江苏省委常委、南京市委书记
    {"id":1,"name":"周红波","gender":"男","ethnicity":"汉族","birth":"1970-10","birthplace":"广西临桂","education":"南京农业大学、中国农业大学在职研究生","party_join":"","work_start":"","current_post":"江苏省委常委、南京市委书记","current_org":"中共南京市委员会","source":"https://zh.wikipedia.org/wiki/%E5%91%A8%E7%BA%A2%E6%B3%A2"},
    # 李忠军 — 南京市委副书记、代市长
    {"id":2,"name":"李忠军","gender":"男","ethnicity":"汉族","birth":"1972-06","birthplace":"待查","education":"中国人民大学经济学硕士","party_join":"","work_start":"","current_post":"南京市委副书记、代市长","current_org":"南京市人民政府","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E5%BF%A0%E5%86%9B"},
    # 林涛 — 南京市委常委、常务副市长（兼江宁区委书记）
    {"id":3,"name":"林涛","gender":"男","ethnicity":"汉族","birth":"1970-01","birthplace":"江苏海安","education":"","party_join":"","work_start":"","current_post":"南京市委常委、常务副市长","current_org":"南京市人民政府","source":"https://zh.wikipedia.org/wiki/%E6%9E%97%E6%B6%9B_(1970%E5%B9%B4%EF%BC%89"},
    # 许峰 — 南京市副市长
    {"id":4,"name":"许峰","gender":"男","ethnicity":"汉族","birth":"1973-10","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"南京市副市长","current_org":"南京市人民政府","source":"https://zh.wikipedia.org/wiki/%E8%AE%B8%E5%B3%B0_(1973%E5%B9%B4)"},
    # 张蕴 — 南京市副市长
    {"id":5,"name":"张蕴","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"南京市副市长","current_org":"南京市人民政府","source":""},
    # 蒋敏 — 南京市副市长（女）
    {"id":6,"name":"蒋敏","gender":"女","ethnicity":"汉族","birth":"1978-02","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"南京市副市长","current_org":"南京市人民政府","source":""},
    # 孙百军 — 南京市副市长（党外）
    {"id":7,"name":"孙百军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"南京市副市长","current_org":"南京市人民政府","source":""},
    # 徐大勇 — 南京市副市长
    {"id":8,"name":"徐大勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"南京市副市长","current_org":"南京市人民政府","source":""},

    # ── Predecessor — 市长 ──
    # 陈之常 — 前任南京市长→内蒙古包头市委书记
    {"id":9,"name":"陈之常","gender":"男","ethnicity":"汉族","birth":"1974-12","birthplace":"四川大竹","education":"中国政法大学","party_join":"","work_start":"","current_post":"内蒙古自治区党委常委、包头市委书记（原南京市长）","current_org":"中共内蒙古包头市委员会","source":"https://zh.wikipedia.org/wiki/%E9%99%88%E4%B9%8B%E5%B8%B8"},

    # ── 11 Districts — 区委书记 + 区长 ──

    # 玄武区
    {"id":10,"name":"闵一峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"玄武区委书记","current_org":"中共玄武区委员会","source":"https://zh.wikipedia.org/wiki/%E9%97%B5%E4%B8%80%E5%B3%B0"},
    {"id":11,"name":"玄武区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"玄武区区长","current_org":"玄武区人民政府","source":""},

    # 秦淮区
    {"id":12,"name":"王生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"秦淮区委书记","current_org":"中共秦淮区委员会","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E7%94%9F"},
    {"id":13,"name":"秦淮区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"秦淮区区长","current_org":"秦淮区人民政府","source":""},

    # 建邺区
    {"id":14,"name":"姜宸","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"建邺区委书记","current_org":"中共建邺区委员会","source":"https://zh.wikipedia.org/wiki/%E5%A7%9C%E5%AE%B8"},
    {"id":15,"name":"建邺区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"建邺区区长","current_org":"建邺区人民政府","source":""},

    # 鼓楼区
    {"id":16,"name":"王安伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"鼓楼区委书记","current_org":"中共鼓楼区委员会","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E5%AE%89%E4%BC%9F"},
    {"id":17,"name":"鼓楼区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"鼓楼区区长","current_org":"鼓楼区人民政府","source":""},

    # 浦口区
    {"id":18,"name":"陆卫东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"浦口区委书记","current_org":"中共浦口区委员会","source":"https://zh.wikipedia.org/wiki/%E9%99%86%E5%8D%AB%E4%B8%9C"},
    {"id":19,"name":"浦口区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"浦口区区长","current_org":"浦口区人民政府","source":""},

    # 栖霞区
    {"id":20,"name":"孙海东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"栖霞区委书记","current_org":"中共栖霞区委员会","source":"https://zh.wikipedia.org/wiki/%E5%AD%99%E6%B5%B7%E4%B8%9C"},
    {"id":21,"name":"栖霞区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"栖霞区区长","current_org":"栖霞区人民政府","source":""},

    # 雨花台区
    {"id":22,"name":"张连春","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"雨花台区委书记","current_org":"中共雨花台区委员会","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E8%BF%9E%E6%98%A5"},
    {"id":23,"name":"李方毅","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"雨花台区区长","current_org":"雨花台区人民政府","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%96%B9%E6%AF%85"},

    # 江宁区
    {"id":24,"name":"林涛(江宁)","gender":"男","ethnicity":"汉族","birth":"1970-01","birthplace":"江苏海安","education":"","party_join":"","work_start":"","current_post":"江宁区委书记（兼南京市委常委、常务副市长）","current_org":"中共江宁区委员会","source":"https://zh.wikipedia.org/wiki/%E6%9E%97%E6%B6%9B_(1970%E5%B9%B4%EF%BC%89"},
    {"id":25,"name":"江宁区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"江宁区区长","current_org":"江宁区人民政府","source":""},

    # 六合区
    {"id":26,"name":"周勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"六合区委书记","current_org":"中共六合区委员会","source":"https://zh.wikipedia.org/wiki/%E5%91%A8%E5%8B%87"},
    {"id":27,"name":"六合区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"六合区区长","current_org":"六合区人民政府","source":""},

    # 溧水区
    {"id":28,"name":"张蕴(溧水)","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"溧水区委书记","current_org":"中共溧水区委员会","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E8%95%B4"},
    {"id":29,"name":"溧水区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"溧水区区长","current_org":"溧水区人民政府","source":""},

    # 高淳区
    {"id":30,"name":"刘伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"高淳区委书记","current_org":"中共高淳区委员会","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E4%BC%9F"},
    {"id":31,"name":"高淳区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"高淳区区长","current_org":"高淳区人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Nanjing city-level core ──
    {"id":1,"name":"中共南京市委员会","type":"党委","level":"副省级","parent":"中共江苏省委员会","location":"江苏省南京市"},
    {"id":2,"name":"南京市人民政府","type":"政府","level":"副省级","parent":"江苏省人民政府","location":"江苏省南京市"},
    {"id":3,"name":"南京市人大常委会","type":"人大","level":"副省级","parent":"","location":"江苏省南京市"},
    {"id":4,"name":"政协南京市委员会","type":"政协","level":"副省级","parent":"","location":"江苏省南京市"},
    {"id":5,"name":"中共南京市纪律检查委员会","type":"党委","level":"副省级","parent":"中共南京市委员会","location":"江苏省南京市"},
    {"id":6,"name":"南京市公安局","type":"政府","level":"副省级","parent":"南京市人民政府","location":"江苏省南京市"},

    # ── 11 Districts — Party committees ──
    {"id":7,"name":"中共玄武区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市玄武区"},
    {"id":8,"name":"中共秦淮区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市秦淮区"},
    {"id":9,"name":"中共建邺区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市建邺区"},
    {"id":10,"name":"中共鼓楼区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市鼓楼区"},
    {"id":11,"name":"中共浦口区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市浦口区"},
    {"id":12,"name":"中共栖霞区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市栖霞区"},
    {"id":13,"name":"中共雨花台区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市雨花台区"},
    {"id":14,"name":"中共江宁区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市江宁区"},
    {"id":15,"name":"中共六合区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市六合区"},
    {"id":16,"name":"中共溧水区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市溧水区"},
    {"id":17,"name":"中共高淳区委员会","type":"党委","level":"地级","parent":"中共南京市委员会","location":"江苏省南京市高淳区"},

    # ── 11 Districts — Governments ──
    {"id":18,"name":"玄武区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市玄武区"},
    {"id":19,"name":"秦淮区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市秦淮区"},
    {"id":20,"name":"建邺区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市建邺区"},
    {"id":21,"name":"鼓楼区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市鼓楼区"},
    {"id":22,"name":"浦口区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市浦口区"},
    {"id":23,"name":"栖霞区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市栖霞区"},
    {"id":24,"name":"雨花台区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市雨花台区"},
    {"id":25,"name":"江宁区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市江宁区"},
    {"id":26,"name":"六合区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市六合区"},
    {"id":27,"name":"溧水区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市溧水区"},
    {"id":28,"name":"高淳区人民政府","type":"政府","level":"地级","parent":"南京市人民政府","location":"江苏省南京市高淳区"},

    # ── External / other orgs needed ──
    {"id":29,"name":"中共内蒙古包头市委员会","type":"党委","level":"地级","parent":"中共内蒙古自治区委员会","location":"内蒙古自治区包头市"},
    {"id":30,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":31,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":32,"name":"中共广西壮族自治区委员会","type":"党委","level":"省级","parent":"","location":"广西壮族自治区南宁市"},
    {"id":33,"name":"中共海南省委员会","type":"党委","level":"省级","parent":"","location":"海南省海口市"},
    {"id":34,"name":"中共三亚市委员会","type":"党委","level":"地级","parent":"中共海南省委员会","location":"海南省三亚市"},
    {"id":35,"name":"中国东方电气集团","type":"事业单位","level":"国家级","parent":"国务院","location":"四川省成都市"},
    {"id":36,"name":"中共海南省委员会","type":"党委","level":"省级","parent":"","location":"海南省海口市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 周红波 ──
    {"id":1,"person_id":1,"org_id":1,"title":"江苏省委常委、南京市委书记","start":"2024-12","end":"","rank":"副部级","note":"2024.12从海南调任南京市委书记"},
    {"id":2,"person_id":1,"org_id":34,"title":"海南省委常委、三亚市委书记","start":"2021-01","end":"2024-12","rank":"副部级","note":""},
    {"id":3,"person_id":1,"org_id":32,"title":"广西壮族自治区人民政府副主席","start":"2016-11","end":"2021-01","rank":"副部级","note":"兼南宁市长至2020"},
    {"id":4,"person_id":1,"org_id":32,"title":"南宁市市长","start":"2011-08","end":"2020-03","rank":"副省级","note":"在广西工作，长期在农业系统，后任南宁市长近9年"},
    {"id":5,"person_id":1,"org_id":32,"title":"广西农业系统工作","start":"1992-07","end":"2006-09","rank":"","note":"1992年参加工作，从技术员晋升"},

    # ── 李忠军 ──
    {"id":6,"person_id":2,"org_id":2,"title":"南京市委副书记、代市长","start":"2025-11","end":"","rank":"副部级","note":"2025.11从央企调任南京代市长"},
    {"id":7,"person_id":2,"org_id":35,"title":"中国东方电气集团领导职务","start":"","end":"2025-11","rank":"","note":"此前在央企（东方电气）工作"},

    # ── 林涛 ──
    {"id":8,"person_id":3,"org_id":2,"title":"南京市委常委、常务副市长","start":"","end":"","rank":"副部级","note":""},
    {"id":9,"person_id":3,"org_id":14,"title":"江宁区委书记（兼）","start":"","end":"","rank":"","note":"兼任江宁区委书记"},

    # ── 许峰 ──
    {"id":10,"person_id":4,"org_id":2,"title":"南京市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 张蕴（副市长） ──
    {"id":11,"person_id":5,"org_id":2,"title":"南京市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 蒋敏 ──
    {"id":12,"person_id":6,"org_id":2,"title":"南京市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 孙百军 ──
    {"id":13,"person_id":7,"org_id":2,"title":"南京市副市长","start":"","end":"","rank":"副部级","note":"党外人士"},

    # ── 徐大勇 ──
    {"id":14,"person_id":8,"org_id":2,"title":"南京市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 陈之常 ──
    {"id":15,"person_id":9,"org_id":29,"title":"内蒙古自治区党委常委、包头市委书记","start":"2025-10","end":"","rank":"副部级","note":"从南京市长调任包头市委书记"},
    {"id":16,"person_id":9,"org_id":2,"title":"南京市市长","start":"2023-01","end":"2025-10","rank":"副部级","note":"约2年9个月"},
    {"id":17,"person_id":9,"org_id":1,"title":"南京市委副书记","start":"2023-01","end":"2025-10","rank":"副部级","note":""},

    # ── 闵一峰（玄武区委书记） ──
    {"id":18,"person_id":10,"org_id":7,"title":"玄武区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 玄武区长（placeholder） ──
    {"id":19,"person_id":11,"org_id":18,"title":"玄武区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 王生（秦淮区委书记） ──
    {"id":20,"person_id":12,"org_id":8,"title":"秦淮区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 秦淮区长（placeholder） ──
    {"id":21,"person_id":13,"org_id":19,"title":"秦淮区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 姜宸（建邺区委书记） ──
    {"id":22,"person_id":14,"org_id":9,"title":"建邺区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 建邺区长（placeholder） ──
    {"id":23,"person_id":15,"org_id":20,"title":"建邺区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 王安伟（鼓楼区委书记） ──
    {"id":24,"person_id":16,"org_id":10,"title":"鼓楼区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 鼓楼区长（placeholder） ──
    {"id":25,"person_id":17,"org_id":21,"title":"鼓楼区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 陆卫东（浦口区委书记） ──
    {"id":26,"person_id":18,"org_id":11,"title":"浦口区委书记","start":"","end":"","rank":"正厅级","note":"浦口区2025.12与江北新区一体化运行"},

    # ── 浦口区长（placeholder） ──
    {"id":27,"person_id":19,"org_id":22,"title":"浦口区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 孙海东（栖霞区委书记） ──
    {"id":28,"person_id":20,"org_id":12,"title":"栖霞区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 栖霞区长（placeholder） ──
    {"id":29,"person_id":21,"org_id":23,"title":"栖霞区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 张连春（雨花台区委书记） ──
    {"id":30,"person_id":22,"org_id":13,"title":"雨花台区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 李方毅（雨花台区区长） ──
    {"id":31,"person_id":23,"org_id":24,"title":"雨花台区区长","start":"","end":"","rank":"正厅级","note":""},

    # ── 林涛（江宁区委书记，兼市领导） ──
    {"id":32,"person_id":24,"org_id":14,"title":"江宁区委书记","start":"","end":"","rank":"正厅级","note":"兼任南京市委常委、常务副市长"},

    # ── 江宁区长（placeholder） ──
    {"id":33,"person_id":25,"org_id":25,"title":"江宁区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 周勇（六合区委书记） ──
    {"id":34,"person_id":26,"org_id":15,"title":"六合区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 六合区长（placeholder） ──
    {"id":35,"person_id":27,"org_id":26,"title":"六合区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 张蕴（溧水区委书记） ──
    {"id":36,"person_id":28,"org_id":16,"title":"溧水区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 溧水区长（placeholder） ──
    {"id":37,"person_id":29,"org_id":27,"title":"溧水区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 刘伟（高淳区委书记） ──
    {"id":38,"person_id":30,"org_id":17,"title":"高淳区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 高淳区长（placeholder） ──
    {"id":39,"person_id":31,"org_id":28,"title":"高淳区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 周红波 ↔ 李忠军（党政搭档） ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"周红波（南京市委书记）与李忠军（代市长）为南京市党政一把手搭档","overlap_org":"南京市","overlap_period":"2025-11至今"},

    # ── 陈之常→李忠军（前后任市长） ──
    {"id":2,"person_a":9,"person_b":2,"type":"前后任","context":"陈之常（2023-2025南京市长）→ 李忠军（2025.11接任代市长）。陈之常调任包头市委书记","overlap_org":"南京市人民政府","overlap_period":"不重叠（前后任）"},

    # ── 周红波跨省（桂→琼→苏） ──
    {"id":3,"person_a":1,"person_b":32,"type":"跨省交流","context":"周红波（桂→琼→苏）从广西→海南→江苏，三省份跨省交流","overlap_org":"广西/海南/江苏","overlap_period":"2024-12至今"},

    # ── 林涛兼任江宁关系 ──
    {"id":4,"person_a":3,"person_b":24,"type":"同一人","context":"林涛 = 林涛(江宁)，同一人兼任南京市常务副市长和江宁区委书记","overlap_org":"南京市","overlap_period":""},

    # ── 林涛（市领导）与江宁区政府关系 ──
    {"id":5,"person_a":3,"person_b":25,"type":"党政搭档","context":"林涛（江宁区委书记/市常务副市长）与江宁区区长党政搭档","overlap_org":"江宁区","overlap_period":""},

    # ── 张蕴副市长 vs 张蕴溧水（同名不同人提示） ──
    {"id":6,"person_a":5,"person_b":28,"type":"同名不同人","context":"张蕴（南京市副市长）与张蕴（溧水区委书记）为同名不同人，注意区分","overlap_org":"南京市","overlap_period":""},

    # ── 各区委书记↔区长（党政搭档，placeholder区长） ──
    {"id":7,"person_a":10,"person_b":11,"type":"党政搭档","context":"闵一峰（玄武区委书记）与玄武区区长党政搭档","overlap_org":"玄武区","overlap_period":""},
    {"id":8,"person_a":12,"person_b":13,"type":"党政搭档","context":"王生（秦淮区委书记）与秦淮区区长党政搭档","overlap_org":"秦淮区","overlap_period":""},
    {"id":9,"person_a":14,"person_b":15,"type":"党政搭档","context":"姜宸（建邺区委书记）与建邺区区长党政搭档","overlap_org":"建邺区","overlap_period":""},
    {"id":10,"person_a":16,"person_b":17,"type":"党政搭档","context":"王安伟（鼓楼区委书记）与鼓楼区区长党政搭档","overlap_org":"鼓楼区","overlap_period":""},
    {"id":11,"person_a":18,"person_b":19,"type":"党政搭档","context":"陆卫东（浦口区委书记）与浦口区区长党政搭档","overlap_org":"浦口区","overlap_period":""},
    {"id":12,"person_a":20,"person_b":21,"type":"党政搭档","context":"孙海东（栖霞区委书记）与栖霞区区长党政搭档","overlap_org":"栖霞区","overlap_period":""},
    {"id":13,"person_a":22,"person_b":23,"type":"党政搭档","context":"张连春（雨花台区委书记）与李方毅（雨花台区区长）党政搭档","overlap_org":"雨花台区","overlap_period":""},
    {"id":14,"person_a":26,"person_b":27,"type":"党政搭档","context":"周勇（六合区委书记）与六合区区长党政搭档","overlap_org":"六合区","overlap_period":""},
    {"id":15,"person_a":28,"person_b":29,"type":"党政搭档","context":"张蕴（溧水区委书记）与溧水区区长党政搭档","overlap_org":"溧水区","overlap_period":""},
    {"id":16,"person_a":30,"person_b":31,"type":"党政搭档","context":"刘伟（高淳区委书记）与高淳区区长党政搭档","overlap_org":"高淳区","overlap_period":""},

    # ── 市区联系：各区委向市委汇报 ──
    {"id":17,"person_a":1,"person_b":10,"type":"隶属关系","context":"周红波（市委书记）领导闵一峰（玄武区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":18,"person_a":1,"person_b":12,"type":"隶属关系","context":"周红波（市委书记）领导王生（秦淮区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":19,"person_a":1,"person_b":14,"type":"隶属关系","context":"周红波（市委书记）领导姜宸（建邺区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":20,"person_a":1,"person_b":16,"type":"隶属关系","context":"周红波（市委书记）领导王安伟（鼓楼区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":21,"person_a":1,"person_b":18,"type":"隶属关系","context":"周红波（市委书记）领导陆卫东（浦口区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":22,"person_a":1,"person_b":20,"type":"隶属关系","context":"周红波（市委书记）领导孙海东（栖霞区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":23,"person_a":1,"person_b":22,"type":"隶属关系","context":"周红波（市委书记）领导张连春（雨花台区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":24,"person_a":1,"person_b":24,"type":"隶属关系","context":"周红波（市委书记）领导林涛（江宁区委书记/常委副市长）","overlap_org":"南京市","overlap_period":""},
    {"id":25,"person_a":1,"person_b":26,"type":"隶属关系","context":"周红波（市委书记）领导周勇（六合区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":26,"person_a":1,"person_b":28,"type":"隶属关系","context":"周红波（市委书记）领导张蕴（溧水区委书记）","overlap_org":"南京市","overlap_period":""},
    {"id":27,"person_a":1,"person_b":30,"type":"隶属关系","context":"周红波（市委书记）领导刘伟（高淳区委书记）","overlap_org":"南京市","overlap_period":""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "市委书记" in post and "省委" not in post:
        return "200,30,30"  # deep red for district party secretary
    if "市委书记" in post:
        return "200,30,30"
    if "市长" in post or "区长" in post:
        return "30,80,200"  # deep blue for mayor/district head
    if "副书记" in post:
        return "220,60,60"
    if "副市长" in post or "副区长" in post:
        return "60,120,220"
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"
    if "组织部长" in post or "统战部长" in post or "宣传部长" in post or "政法委" in post:
        return "180,90,180"
    if "政协" in post:
        return "180,160,220"
    if "人大" in post:
        return "160,200,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>南京市（副省级）领导班子 + 11区工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
