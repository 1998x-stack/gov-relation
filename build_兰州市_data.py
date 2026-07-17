#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 兰州市 (Lanzhou City, Gansu) leadership network.

兰州市 — 甘肃省省会, 地级市 (副省级).
Covers current Party Secretary (张晓强), Mayor (刘建勋), their predecessors,
key Standing Committee members, and district-level leaders.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
# NOTE: These paths will be adjusted by process_tmp.py during promotion.
# For staging, they point to the tmp directory.
# After promotion, they will be updated to canonical paths.
STAGING = os.path.join(BASE, "data/tmp/gansu_兰州市")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "兰州市_network.db")
GEXF_PATH = os.path.join(STAGING, "兰州市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. City-level top leadership ──

    # 张晓强 — 甘肃省委常委、兰州市委书记 (as of 2023.07)
    {"id":1,"name":"张晓强","gender":"男","ethnicity":"汉族",
     "birth":"1975-11","birthplace":"浙江庆元",
     "education":"浙江林学院（浙江农林大学）林学专业、美国肯恩大学公共管理硕士",
     "party_join":"1996-06","work_start":"1996-08",
     "current_post":"甘肃省委常委、兰州市委书记",
     "current_org":"中共兰州市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E6%99%93%E5%BC%BA_(1975%E5%B9%B4)"},

    # 刘建勋 — 兰州市市长 (as of 2023.03)
    {"id":2,"name":"刘建勋","gender":"男","ethnicity":"汉族",
     "birth":"1970-03","birthplace":"甘肃武威",
     "education":"",  # 待查
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市人民政府市长",
     "current_org":"兰州市人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E5%85%B0%E5%B7%9E%E5%B8%82"},

    # 胡雄韬 — 兰州市人大常委会主任 (as of 2026.06)
    {"id":3,"name":"胡雄韬","gender":"男","ethnicity":"汉族",
     "birth":"1970-12","birthplace":"甘肃古浪",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市人大常委会主任",
     "current_org":"兰州市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E5%85%B0%E5%B7%9E%E5%B8%82"},

    # 王鸿岳 — 兰州市政协主席 (as of 2026.06)
    {"id":4,"name":"王鸿岳","gender":"男","ethnicity":"汉族",
     "birth":"1971-05","birthplace":"甘肃天水",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市政协主席",
     "current_org":"兰州市政协",
     "source":"https://zh.wikipedia.org/wiki/%E5%85%B0%E5%B7%9E%E5%B8%82"},

    # ── B. Predecessors ──

    # 朱天舒 — 前任兰州市委书记 (2021.06-2023.07), 现任宁夏政法委书记
    {"id":5,"name":"朱天舒","gender":"男","ethnicity":"汉族",
     "birth":"1968-05","birthplace":"江苏宿迁",
     "education":"南京粮食经济学院会计学、吉林工业大学/吉林大学经济学硕士",
     "party_join":"1994-09","work_start":"1990-07",
     "current_post":"宁夏回族自治区党委常委、政法委书记（原兰州市委书记）",
     "current_org":"中共宁夏回族自治区委员会",
     "source":"https://zh.wikipedia.org/wiki/%E6%9C%B1%E5%A4%A9%E8%88%92"},

    # 李荣灿 — 更早前任兰州市委书记 (2016-2021)
    {"id":6,"name":"李荣灿","gender":"男","ethnicity":"汉族",
     "birth":"1966-09","birthplace":"浙江绍兴",
     "education":"江西财经学院",
     "party_join":"中共党员","work_start":"1989-08",
     "current_post":"甘肃省政协主席（原兰州市委书记）",
     "current_org":"甘肃省政协",
     "source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E8%8D%A3%E7%81%BF"},

    # 张伟文 — 前任兰州市长 (2021-2023)
    {"id":7,"name":"张伟文","gender":"男","ethnicity":"汉族",
     "birth":"1966-07","birthplace":"湖南醴陵",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"甘肃省人民政府秘书长（原兰州市长）",
     "current_org":"甘肃省人民政府",
     "source":"公开报道"},

    # ── C. Standing Committee key members (市委常委会) ──

    # 常务副市长
    {"id":8,"name":"潘喆","gender":"男","ethnicity":"汉族",
     "birth":"1983-08","birthplace":"浙江永嘉",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市委常委、常务副市长",
     "current_org":"兰州市人民政府",
     "source":"公开报道"},
    # 纪委书记
    {"id":9,"name":"王志坚","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市委常委、市纪委书记、市监委主任",
     "current_org":"中共兰州市纪律检查委员会",
     "source":"公开报道"},
    # 组织部部长
    {"id":10,"name":"王鸿岳","gender":"男","ethnicity":"汉族",
     "birth":"1971-05","birthplace":"甘肃天水",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市委常委、组织部部长（兼市政协主席）",
     "current_org":"中共兰州市委组织部",
     "source":"公开报道"},
    # 宣传部部长
    {"id":11,"name":"刘伟红","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市委常委、宣传部部长",
     "current_org":"中共兰州市委宣传部",
     "source":"公开报道"},
    # 政法委书记
    {"id":12,"name":"魏晋文","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市委常委、政法委书记",
     "current_org":"中共兰州市委政法委员会",
     "source":"公开报道"},
    # 统战部部长
    {"id":13,"name":"张泽武","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市委常委、统战部部长",
     "current_org":"中共兰州市委统一战线工作部",
     "source":"公开报道"},
    # 市委秘书长
    {"id":14,"name":"陶正茂","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市委常委、秘书长",
     "current_org":"中共兰州市委员会",
     "source":"公开报道"},

    # ── D. District/county level key leaders ──

    # 城关区
    {"id":15,"name":"刘凤恒","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市城关区委书记",
     "current_org":"中共兰州市城关区委",
     "source":"公开报道"},
    {"id":16,"name":"李长江","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"兰州市城关区区长",
     "current_org":"城关区人民政府",
     "source":"公开报道"},
    # 七里河区
    {"id":17,"name":"芮文刚","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"七里河区委书记",
     "current_org":"中共七里河区委",
     "source":"公开报道"},
    {"id":18,"name":"孙洋","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"七里河区区长",
     "current_org":"七里河区人民政府",
     "source":"公开报道"},
    # 西固区
    {"id":19,"name":"赵同庆","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"西固区委书记",
     "current_org":"中共西固区委",
     "source":"公开报道"},
    {"id":20,"name":"毛玉铎","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"西固区区长",
     "current_org":"西固区人民政府",
     "source":"公开报道"},
    # 安宁区
    {"id":21,"name":"王立山","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"安宁区委书记",
     "current_org":"中共安宁区委",
     "source":"公开报道"},
    {"id":22,"name":"曹宏亮","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"安宁区区长",
     "current_org":"安宁区人民政府",
     "source":"公开报道"},
    # 红古区
    {"id":23,"name":"薛蕾","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"红古区委书记",
     "current_org":"中共红古区委",
     "source":"公开报道"},
    {"id":24,"name":"肖正明","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"红古区区长",
     "current_org":"红古区人民政府",
     "source":"公开报道"},
    # 永登县
    {"id":25,"name":"王彦群","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"永登县委书记",
     "current_org":"中共永登县委",
     "source":"公开报道"},
    {"id":26,"name":"贾文涛","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"永登县县长",
     "current_org":"永登县人民政府",
     "source":"公开报道"},
    # 榆中县
    {"id":27,"name":"崔峰巍","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"榆中县委书记",
     "current_org":"中共榆中县委",
     "source":"公开报道"},
    {"id":28,"name":"魏孔毅","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"榆中县县长",
     "current_org":"榆中县人民政府",
     "source":"公开报道"},
    # 皋兰县
    {"id":29,"name":"康石","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"皋兰县委书记",
     "current_org":"中共皋兰县委",
     "source":"公开报道"},
    {"id":30,"name":"范仲阔","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"皋兰县县长",
     "current_org":"皋兰县人民政府",
     "source":"公开报道"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # City-level
    {"id":1,"name":"中共兰州市委员会","type":"党委","level":"副省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":2,"name":"兰州市人民政府","type":"政府","level":"副省级","parent":"甘肃省人民政府","location":"甘肃省兰州市"},
    {"id":3,"name":"兰州市人大常委会","type":"人大","level":"副省级","parent":"","location":"甘肃省兰州市"},
    {"id":4,"name":"兰州市政协","type":"政协","level":"副省级","parent":"","location":"甘肃省兰州市"},
    {"id":5,"name":"中共兰州市纪律检查委员会","type":"纪委","level":"副省级","parent":"","location":"甘肃省兰州市"},
    {"id":6,"name":"中共兰州市委组织部","type":"党委","level":"副省级","parent":"中共兰州市委员会","location":"甘肃省兰州市"},
    {"id":7,"name":"中共兰州市委宣传部","type":"党委","level":"副省级","parent":"中共兰州市委员会","location":"甘肃省兰州市"},
    {"id":8,"name":"中共兰州市委政法委员会","type":"党委","level":"副省级","parent":"中共兰州市委员会","location":"甘肃省兰州市"},
    {"id":9,"name":"中共兰州市委统一战线工作部","type":"党委","level":"副省级","parent":"中共兰州市委员会","location":"甘肃省兰州市"},

    # Provincial-level
    {"id":10,"name":"中共甘肃省委员会","type":"党委","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":11,"name":"甘肃省人民政府","type":"政府","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":12,"name":"甘肃省政协","type":"政协","level":"省级","parent":"","location":"甘肃省兰州市"},

    # District/County-level
    {"id":13,"name":"中共兰州市城关区委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市城关区"},
    {"id":14,"name":"城关区人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市城关区"},
    {"id":15,"name":"中共七里河区委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市七里河区"},
    {"id":16,"name":"七里河区人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市七里河区"},
    {"id":17,"name":"中共西固区委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市西固区"},
    {"id":18,"name":"西固区人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市西固区"},
    {"id":19,"name":"中共安宁区委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市安宁区"},
    {"id":20,"name":"安宁区人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市安宁区"},
    {"id":21,"name":"中共红古区委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市红古区"},
    {"id":22,"name":"红古区人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市红古区"},
    {"id":23,"name":"中共永登县委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市永登县"},
    {"id":24,"name":"永登县人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市永登县"},
    {"id":25,"name":"中共榆中县委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市榆中县"},
    {"id":26,"name":"榆中县人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市榆中县"},
    {"id":27,"name":"中共皋兰县委","type":"党委","level":"县级","parent":"中共兰州市委员会","location":"兰州市皋兰县"},
    {"id":28,"name":"皋兰县人民政府","type":"政府","level":"县级","parent":"兰州市人民政府","location":"兰州市皋兰县"},
]

# =========================================================================
# POSITIONS (current and historical)
# =========================================================================
positions = [
    # City-level top leaders
    {"person_id":1,"org_id":1,"title":"甘肃省委常委、兰州市委书记","start":"2023-07","end":"","rank":"副部","note":"时任全国最年轻省会城市党委书记"},
    {"person_id":1,"org_id":10,"title":"甘肃省委常委","start":"2023-07","end":"","rank":"副部","note":""},
    {"person_id":2,"org_id":2,"title":"兰州市市长","start":"2023-03","end":"","rank":"副部","note":"政协甘肃省委员会人口资源环境委员会副主任"},
    {"person_id":3,"org_id":3,"title":"兰州市人大常委会主任","start":"2026-06","end":"","rank":"副部","note":""},
    {"person_id":4,"org_id":4,"title":"兰州市政协主席","start":"2026-06","end":"","rank":"副部","note":""},

    # Predecessors
    {"person_id":5,"org_id":1,"title":"兰州市委书记","start":"2021-06","end":"2023-07","rank":"副部","note":"前任，调任宁夏政法委书记"},
    {"person_id":5,"org_id":10,"title":"甘肃省委常委","start":"2021-06","end":"2023-07","rank":"副部","note":""},
    {"person_id":6,"org_id":1,"title":"兰州市委书记","start":"2016-10","end":"2021-06","rank":"副部","note":"前任"},
    {"person_id":6,"org_id":10,"title":"甘肃省委常委","start":"2016-10","end":"2021-06","rank":"副部","note":""},
    {"person_id":7,"org_id":2,"title":"兰州市市长","start":"2021-01","end":"2023-03","rank":"副部","note":"前任，调任甘肃省政府秘书长"},

    # Standing Committee members
    {"person_id":8,"org_id":2,"title":"兰州市委常委、常务副市长","start":"","end":"","rank":"正厅","note":""},
    {"person_id":9,"org_id":5,"title":"兰州市委常委、市纪委书记、市监委主任","start":"","end":"","rank":"正厅","note":""},
    {"person_id":10,"org_id":6,"title":"兰州市委常委、组织部部长","start":"","end":"","rank":"正厅","note":"兼市政协主席"},
    {"person_id":10,"org_id":4,"title":"兰州市政协主席","start":"2026-06","end":"","rank":"副部","note":""},
    {"person_id":11,"org_id":7,"title":"兰州市委常委、宣传部部长","start":"","end":"","rank":"正厅","note":""},
    {"person_id":12,"org_id":8,"title":"兰州市委常委、政法委书记","start":"","end":"","rank":"正厅","note":""},
    {"person_id":13,"org_id":9,"title":"兰州市委常委、统战部部长","start":"","end":"","rank":"正厅","note":""},
    {"person_id":14,"org_id":1,"title":"兰州市委常委、秘书长","start":"","end":"","rank":"正厅","note":""},

    # District/county top pairs
    {"person_id":15,"org_id":13,"title":"城关区委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":16,"org_id":14,"title":"城关区区长","start":"","end":"","rank":"正处","note":""},
    {"person_id":17,"org_id":15,"title":"七里河区委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":18,"org_id":16,"title":"七里河区区长","start":"","end":"","rank":"正处","note":""},
    {"person_id":19,"org_id":17,"title":"西固区委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":20,"org_id":18,"title":"西固区区长","start":"","end":"","rank":"正处","note":""},
    {"person_id":21,"org_id":19,"title":"安宁区委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":22,"org_id":20,"title":"安宁区区长","start":"","end":"","rank":"正处","note":""},
    {"person_id":23,"org_id":21,"title":"红古区委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":24,"org_id":22,"title":"红古区区长","start":"","end":"","rank":"正处","note":""},
    {"person_id":25,"org_id":23,"title":"永登县委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":26,"org_id":24,"title":"永登县县长","start":"","end":"","rank":"正处","note":""},
    {"person_id":27,"org_id":25,"title":"榆中县委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":28,"org_id":26,"title":"榆中县县长","start":"","end":"","rank":"正处","note":""},
    {"person_id":29,"org_id":27,"title":"皋兰县委书记","start":"","end":"","rank":"正处","note":""},
    {"person_id":30,"org_id":28,"title":"皋兰县县长","start":"","end":"","rank":"正处","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Top leadership pairs
    {"person_a":1,"person_b":2,"type":"党政同僚","context":"兰州市委书记与市长搭档","overlap_org":"兰州市","overlap_period":"2023-"},
    {"person_a":1,"person_b":5,"type":"前后任","context":"朱天舒→张晓强 兰州市委书记交接","overlap_org":"中共兰州市委员会","overlap_period":"2023-07"},
    {"person_a":5,"person_b":6,"type":"前后任","context":"李荣灿→朱天舒 兰州市委书记交接","overlap_org":"中共兰州市委员会","overlap_period":"2021-06"},
    {"person_a":2,"person_b":7,"type":"前后任","context":"张伟文→刘建勋 兰州市长交接","overlap_org":"兰州市人民政府","overlap_period":"2023-03"},

    # City-level four-bank leadership
    {"person_a":1,"person_b":3,"type":"党政同僚","context":"市委书记与人大主任同届工作","overlap_org":"兰州市","overlap_period":"2023-"},
    {"person_a":1,"person_b":4,"type":"党政同僚","context":"市委书记与政协主席同届工作","overlap_org":"兰州市","overlap_period":"2023-"},
    {"person_a":2,"person_b":3,"type":"党政同僚","context":"市长与人大主任同届工作","overlap_org":"兰州市","overlap_period":"2023-"},

    # Standing Committee overlap
    {"person_a":1,"person_b":8,"type":"党政同僚","context":"市委书记与常务副市长同届常委会","overlap_org":"中共兰州市委员会","overlap_period":"2023-"},
    {"person_a":1,"person_b":9,"type":"党政同僚","context":"市委书记与纪委书记同届常委会","overlap_org":"中共兰州市委员会","overlap_period":"2023-"},
    {"person_a":1,"person_b":10,"type":"党政同僚","context":"市委书记与组织部长同届常委会","overlap_org":"中共兰州市委员会","overlap_period":"2023-"},
    {"person_a":1,"person_b":11,"type":"党政同僚","context":"市委书记与宣传部长同届常委会","overlap_org":"中共兰州市委员会","overlap_period":"2023-"},
    {"person_a":1,"person_b":12,"type":"党政同僚","context":"市委书记与政法委书记同届常委会","overlap_org":"中共兰州市委员会","overlap_period":"2023-"},
    {"person_a":1,"person_b":13,"type":"党政同僚","context":"市委书记与统战部长同届常委会","overlap_org":"中共兰州市委员会","overlap_period":"2023-"},
    {"person_a":1,"person_b":14,"type":"党政同僚","context":"市委书记与秘书长同届常委会","overlap_org":"中共兰州市委员会","overlap_period":"2023-"},

    # District/county pairs
    {"person_a":15,"person_b":16,"type":"党政同僚","context":"城关区委书记与区长搭档","overlap_org":"城关区","overlap_period":""},
    {"person_a":17,"person_b":18,"type":"党政同僚","context":"七里河区委书记与区长搭档","overlap_org":"七里河区","overlap_period":""},
    {"person_a":19,"person_b":20,"type":"党政同僚","context":"西固区委书记与区长搭档","overlap_org":"西固区","overlap_period":""},
    {"person_a":21,"person_b":22,"type":"党政同僚","context":"安宁区委书记与区长搭档","overlap_org":"安宁区","overlap_period":""},
    {"person_a":23,"person_b":24,"type":"党政同僚","context":"红古区委书记与区长搭档","overlap_org":"红古区","overlap_period":""},
    {"person_a":25,"person_b":26,"type":"党政同僚","context":"永登县委书记与县长搭档","overlap_org":"永登县","overlap_period":""},
    {"person_a":27,"person_b":28,"type":"党政同僚","context":"榆中县委书记与县长搭档","overlap_org":"榆中县","overlap_period":""},
    {"person_a":29,"person_b":30,"type":"党政同僚","context":"皋兰县委书记与县长搭档","overlap_org":"皋兰县","overlap_period":""},
]

# =========================================================================
# BUILD DATABASE
# =========================================================================
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

# Print summary
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

# =========================================================================
# BUILD GEXF
# =========================================================================

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
gexf_parts.append('<meta><creator>Gansu Lanzhou Investigator</creator><description>兰州市领导班子工作关系网络</description></meta>')
gexf_parts.append('<graph mode="static" defaultedgetype="undirected">')

# Nodes
gexf_parts.append('<nodes>')
for p in persons:
    slug_id = f"lanzhou_{p['id']}"
    role_color = color_for_role(p["current_post"])
    is_top = "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    is_gov = ("市长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or \
             ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or \
             ("区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
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
    gexf_parts.append(f'<edge id="e{edge_id}" source="lanzhou_{p["id"]}" target="org_{o["id"]}" label="{label}" weight="1.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="worked_at"/><attvalue for="title" value="{po["title"]}"/><attvalue for="start" value="{po["start"]}"/><attvalue for="end" value="{po["end"]}"/></attvalues>')
    gexf_parts.append('</edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    gexf_parts.append(f'<edge id="e{edge_id}" source="lanzhou_{p_a["id"]}" target="lanzhou_{p_b["id"]}" label="{r["context"]}" weight="2.0">')
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
