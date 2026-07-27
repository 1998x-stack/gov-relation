#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Hainan Province (海南省) leadership network.

Covers: Provincial Party Secretary (省委书记 冯飞), Governor (省长 刘小明),
predecessors (沈晓明), succession chains, key deputy leaders (省委常委会成员,
副省长), and the provincial-level leadership structure.

Sources: Wikipedia (zh.wikipedia.org), official government websites.
"""
import sqlite3, os, sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hainan_province")
DB_PATH = os.path.join(STAGING, "海南省_network.db")
GEXF_PATH = os.path.join(STAGING, "海南省_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 冯飞 — 海南省委书记 (as of 2023.03)
    {"id":1,"name":"冯飞","gender":"男","ethnicity":"汉族","birth":"1962-12","birthplace":"江西都昌","education":"天津大学电力及自动化工程系电力系统及其自动化专业本科、硕士、博士","party_join":"1985-07","work_start":"1991-11","current_post":"海南省委书记、省人大常委会主任","current_org":"中共海南省委员会","source":"https://zh.wikipedia.org/wiki/%E5%86%AF%E9%A3%9E"},
    # 刘小明 — 海南省省长
    {"id":2,"name":"刘小明","gender":"男","ethnicity":"汉族","birth":"1964-09","birthplace":"江苏扬中","education":"北京工业大学土木工程系道路工程专业本科、硕士研究生","party_join":"","work_start":"1988","current_post":"海南省委副书记、省长","current_org":"海南省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E5%B0%8F%E6%98%8E"},

    # ── Provincial leadership (省委常委会成员) ──
    {"id":3,"name":"杨晋柏","gender":"男","ethnicity":"汉族","birth":"1973-04","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委副书记、政法委书记","current_org":"中共海南省委政法委员会","source":"https://zh.wikipedia.org/wiki/%E6%9D%A8%E6%99%8B%E6%9F%8F"},
    {"id":4,"name":"陈国猛","gender":"男","ethnicity":"汉族","birth":"1966-10","birthplace":"福建晋江","education":"厦门大学法律系法学专业学士","party_join":"1989","work_start":"1989-07","current_post":"海南省委常委、省纪委书记、省监委主任","current_org":"中共海南省纪律检查委员会","source":"https://zh.wikipedia.org/wiki/%E9%99%88%E5%9B%BD%E7%8C%9B"},
    {"id":5,"name":"王斌","gender":"男","ethnicity":"汉族","birth":"1971","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、宣传部部长","current_org":"中共海南省委宣传部","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E6%96%8C_(1971%E5%B9%B4)"},
    {"id":6,"name":"巴特尔","gender":"男","ethnicity":"蒙古族","birth":"1967-02","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、常务副省长","current_org":"海南省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%B7%B4%E7%89%B9%E5%B0%94_(1967%E5%B9%B4)"},
    {"id":7,"name":"王祺扬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、三亚市委书记","current_org":"中共三亚市委员会","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E7%A5%BA%E6%89%AC"},
    {"id":8,"name":"王培杰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、省军区司令员","current_org":"海南省军区","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E5%9F%B9%E6%9D%B0"},
    {"id":9,"name":"纳云德","gender":"男","ethnicity":"傈僳族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、组织部部长","current_org":"中共海南省委组织部","source":"https://zh.wikipedia.org/wiki/%E7%BA%B3%E4%BA%91%E5%BE%B7"},
    {"id":10,"name":"范少军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、海口市委书记","current_org":"中共海口市委员会","source":"https://zh.wikipedia.org/wiki/%E8%8C%83%E5%B0%91%E5%86%9B"},
    {"id":11,"name":"尹丽波","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、统战部部长","current_org":"中共海南省委统战部","source":"https://zh.wikipedia.org/wiki/%E5%B0%B9%E4%B8%BD%E6%B3%A2"},
    {"id":12,"name":"邹广","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省委常委、儋州市委书记","current_org":"中共儋州市委员会","source":"https://zh.wikipedia.org/wiki/%E9%84%92%E5%BB%A3"},

    # ── Vice governors (副省长) ──
    {"id":13,"name":"谢京","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省副省长","current_org":"海南省人民政府","source":"https://zh.wikipedia.org/wiki/%E8%B0%A2%E4%BA%AC"},
    {"id":14,"name":"李锋","gender":"男","ethnicity":"汉族","birth":"1973","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省副省长","current_org":"海南省人民政府","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E9%94%8B_(1973%E5%B9%B4)"},
    {"id":15,"name":"赵峰","gender":"男","ethnicity":"汉族","birth":"1972","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省副省长","current_org":"海南省人民政府","source":"https://zh.wikipedia.org/wiki/%E8%B5%B5%E5%B3%B0_(1972%E5%B9%B4)"},
    {"id":16,"name":"杨国强","gender":"男","ethnicity":"汉族","birth":"1970","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省副省长","current_org":"海南省人民政府","source":"https://zh.wikipedia.org/wiki/%E6%9D%A8%E5%9B%BD%E5%BC%BA_(1970%E5%B9%B4)"},
    {"id":17,"name":"刘平治","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省政府党组成员","current_org":"海南省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E5%B9%B3%E6%B2%BB"},

    # ── Predecessors — 省委书记 ──
    {"id":18,"name":"沈晓明","gender":"男","ethnicity":"汉族","birth":"1963-05","birthplace":"浙江上虞","education":"温州医学院儿科系本科、硕士，上海第二医科大学儿科系博士","party_join":"1984-08","work_start":"1987-07","current_post":"湖南省委书记（原海南省委书记）","current_org":"中共湖南省委员会","source":"https://zh.wikipedia.org/wiki/%E6%B2%88%E6%99%93%E6%98%8E"},
    {"id":19,"name":"刘赐贵","gender":"男","ethnicity":"汉族","birth":"1955","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原海南省委书记、省长）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E8%B5%90%E8%B4%B5"},
    {"id":20,"name":"罗保铭","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原海南省委书记）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E7%BD%97%E4%BF%9D%E9%93%AD"},

    # ── Other key provincial leaders ──
    {"id":21,"name":"李荣灿","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省政协主席","current_org":"政协海南省委员会","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E8%8D%A3%E7%81%BF"},
    {"id":22,"name":"苻彩香","gender":"女","ethnicity":"黎族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省人大常委会副主任（党组书记）","current_org":"海南省人大常委会","source":"https://zh.wikipedia.org/wiki/%E8%8B%BB%E5%BD%A9%E9%A6%99"},
    {"id":23,"name":"孙大海","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省人大常委会副主任","current_org":"海南省人大常委会","source":"https://zh.wikipedia.org/wiki/%E5%AD%99%E5%A4%A7%E6%B5%B7"},
    {"id":24,"name":"闫希军","gender":"男","ethnicity":"","birth":"1963","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省人大常委会副主任、省总工会主席","current_org":"海南省人大常委会","source":"https://zh.wikipedia.org/wiki/%E9%97%AB%E5%B8%8C%E5%86%9B_(1963%E5%B9%B4)"},
    {"id":25,"name":"宋健","gender":"男","ethnicity":"","birth":"1966","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省人大常委会副主任","current_org":"海南省人大常委会","source":"https://zh.wikipedia.org/wiki/%E5%AE%8B%E5%81%A5_(1966%E5%B9%B4)"},
    {"id":26,"name":"戴军","gender":"男","ethnicity":"","birth":"1968","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省高级人民法院院长","current_org":"海南省高级人民法院","source":"https://zh.wikipedia.org/wiki/%E6%88%B4%E5%86%9B_(1968%E5%B9%B4)"},
    {"id":27,"name":"张毅","gender":"男","ethnicity":"","birth":"1967","birthplace":"","education":"","party_join":"","work_start":"","current_post":"海南省人民检察院检察长","current_org":"海南省人民检察院","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E6%AF%85_(1967%E5%B9%B4)"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Hainan provincial core
    {"id":1,"name":"中共海南省委员会","type":"党委","level":"省级","parent":"","location":"海南省海口市"},
    {"id":2,"name":"海南省人民政府","type":"政府","level":"省级","parent":"","location":"海南省海口市"},
    {"id":3,"name":"海南省人大常委会","type":"人大","level":"省级","parent":"","location":"海南省海口市"},
    {"id":4,"name":"政协海南省委员会","type":"政协","level":"省级","parent":"","location":"海南省海口市"},
    {"id":5,"name":"中共海南省纪律检查委员会","type":"党委","level":"省级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":6,"name":"海南省监察委员会","type":"党委","level":"省级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":7,"name":"海南省高级人民法院","type":"党委","level":"省级","parent":"","location":"海南省海口市"},
    {"id":8,"name":"海南省人民检察院","type":"党委","level":"省级","parent":"","location":"海南省海口市"},

    # Provincial departments
    {"id":9,"name":"中共海南省委政法委员会","type":"党委","level":"省级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":10,"name":"中共海南省委宣传部","type":"党委","level":"省级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":11,"name":"中共海南省委组织部","type":"党委","level":"省级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":12,"name":"中共海南省委统战部","type":"党委","level":"省级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":13,"name":"海南省军区","type":"党委","level":"省级","parent":"中央军委","location":"海南省海口市"},

    # Key cities
    {"id":14,"name":"中共海口市委员会","type":"党委","level":"地级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":15,"name":"中共三亚市委员会","type":"党委","level":"地级","parent":"中共海南省委员会","location":"海南省三亚市"},
    {"id":16,"name":"中共儋州市委员会","type":"党委","level":"地级","parent":"中共海南省委员会","location":"海南省儋州市"},

    # Central / national orgs
    {"id":17,"name":"中共湖南省委员会","type":"党委","level":"省级","parent":"","location":"湖南省长沙市"},
    {"id":18,"name":"中央军委","type":"党委","level":"国家级","parent":"","location":"北京市"},

    # 冯飞 earlier work units
    {"id":19,"name":"国务院发展研究中心","type":"事业单位","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":20,"name":"工业和信息化部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":21,"name":"浙江省人民政府","type":"政府","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":22,"name":"中共浙江省委员会","type":"党委","level":"省级","parent":"","location":"浙江省杭州市"},

    # 刘小明 earlier work units
    {"id":23,"name":"北京工业大学","type":"事业单位","level":"","parent":"北京市人民政府","location":"北京市"},
    {"id":24,"name":"北京市交通委员会","type":"政府","level":"","parent":"北京市人民政府","location":"北京市"},
    {"id":25,"name":"交通运输部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":26,"name":"中共广西壮族自治区委员会","type":"党委","level":"省级","parent":"","location":"广西壮族自治区南宁市"},

    # 沈晓明 earlier work units
    {"id":27,"name":"上海第二医科大学/交通大学医学院","type":"事业单位","level":"","parent":"","location":"上海市"},
    {"id":28,"name":"上海市人民政府","type":"政府","level":"省级","parent":"","location":"上海市"},
    {"id":29,"name":"中共上海市浦东新区委员会","type":"党委","level":"","parent":"中共上海市委员会","location":"上海市浦东新区"},
    {"id":30,"name":"教育部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":31,"name":"海南省人民政府（前）","type":"政府","level":"省级","parent":"","location":"海南省海口市"},

    # 陈国猛 earlier work units
    {"id":32,"name":"厦门市中级人民法院","type":"党委","level":"","parent":"","location":"福建省厦门市"},
    {"id":33,"name":"中共福建省委政法委","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":34,"name":"浙江省高级人民法院","type":"党委","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":35,"name":"中央纪委案件审理室","type":"党委","level":"国家级","parent":"中央纪委","location":"北京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 冯飞 (id=1) ──
    {"person_id":1,"org_id":1,"title":"海南省委书记","start":"2023-03","end":"present","rank":"正部级","note":"接替沈晓明"},
    {"person_id":1,"org_id":3,"title":"海南省人大常委会主任","start":"2023-05","end":"present","rank":"正部级","note":""},
    {"person_id":1,"org_id":2,"title":"海南省省长","start":"2020-12","end":"2023-04","rank":"正部级","note":"前任沈晓明，后任刘小明"},
    {"person_id":1,"org_id":22,"title":"浙江省委常委、常务副省长","start":"2017-04","end":"2020-12","rank":"副部级","note":""},
    {"person_id":1,"org_id":21,"title":"浙江省副省长","start":"2016-08","end":"2017-04","rank":"副部级","note":""},
    {"person_id":1,"org_id":20,"title":"工业和信息化部副部长","start":"2015-10","end":"2016-08","rank":"副部级","note":""},
    {"person_id":1,"org_id":20,"title":"工信部产业政策司司长","start":"2014-01","end":"2015-10","rank":"正厅级","note":""},
    {"person_id":1,"org_id":19,"title":"国务院发展研究中心产业经济研究部部长","start":"2004-09","end":"2014-01","rank":"正厅级","note":""},

    # ── 刘小明 (id=2) ──
    {"person_id":2,"org_id":2,"title":"海南省省长","start":"2023-04","end":"present","rank":"正部级","note":"2023年4月任代省长，5月当选"},
    {"person_id":2,"org_id":1,"title":"海南省委副书记","start":"2023-04","end":"present","rank":"正部级","note":""},
    {"person_id":2,"org_id":26,"title":"广西壮族自治区党委副书记","start":"2021-03","end":"2023-04","rank":"副部级","note":"专职副书记"},
    {"person_id":2,"org_id":25,"title":"交通运输部副部长","start":"2016-07","end":"2021-03","rank":"副部级","note":""},
    {"person_id":2,"org_id":25,"title":"交通运输部运输服务司司长","start":"2015-04","end":"2016-07","rank":"正厅级","note":""},
    {"person_id":2,"org_id":24,"title":"北京市交通委员会主任","start":"2008-02","end":"2014-03","rank":"正厅级","note":""},
    {"person_id":2,"org_id":24,"title":"北京市交通委员会副主任","start":"2003-03","end":"2008-02","rank":"副厅级","note":""},
    {"person_id":2,"org_id":23,"title":"北京工业大学副校长","start":"2000","end":"2003-03","rank":"","note":""},

    # ── 杨晋柏 (id=3) ──
    {"person_id":3,"org_id":1,"title":"海南省委副书记、政法委书记","start":"","end":"present","rank":"副部级","note":""},

    # ── 陈国猛 (id=4) ──
    {"person_id":4,"org_id":5,"title":"海南省纪委书记","start":"2021-04","end":"present","rank":"副部级","note":""},
    {"person_id":4,"org_id":6,"title":"海南省监委主任","start":"2021-06","end":"present","rank":"副部级","note":""},
    {"person_id":4,"org_id":35,"title":"中央纪委案件审理室主任","start":"2017-09","end":"2021-04","rank":"副部级","note":""},
    {"person_id":4,"org_id":34,"title":"浙江省高级人民法院院长","start":"2016-01","end":"2017-11","rank":"副部级","note":""},
    {"person_id":4,"org_id":33,"title":"福建省委政法委副书记","start":"2015-06","end":"2016-10","rank":"副厅级","note":""},

    # ── 王斌 (id=5) ──
    {"person_id":5,"org_id":10,"title":"海南省委宣传部部长","start":"","end":"present","rank":"副部级","note":""},

    # ── 巴特尔 (id=6) ──
    {"person_id":6,"org_id":2,"title":"海南省常务副省长","start":"","end":"present","rank":"副部级","note":""},

    # ── 王祺扬 (id=7) ──
    {"person_id":7,"org_id":15,"title":"三亚市委书记","start":"","end":"present","rank":"副部级","note":""},

    # ── 王培杰 (id=8) ──
    {"person_id":8,"org_id":13,"title":"海南省军区司令员","start":"","end":"present","rank":"正师级","note":""},

    # ── 纳云德 (id=9) ──
    {"person_id":9,"org_id":11,"title":"海南省委组织部部长","start":"","end":"present","rank":"副部级","note":""},

    # ── 范少军 (id=10) ──
    {"person_id":10,"org_id":14,"title":"海口市委书记","start":"","end":"present","rank":"副部级","note":""},

    # ── 尹丽波 (id=11) ──
    {"person_id":11,"org_id":12,"title":"海南省委统战部部长","start":"","end":"present","rank":"副部级","note":""},

    # ── 邹广 (id=12) ──
    {"person_id":12,"org_id":16,"title":"儋州市委书记","start":"","end":"present","rank":"副厅级","note":""},

    # ── Vice governors ──
    {"person_id":13,"org_id":2,"title":"海南省副省长","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":14,"org_id":2,"title":"海南省副省长","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":15,"org_id":2,"title":"海南省副省长","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":16,"org_id":2,"title":"海南省副省长","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":17,"org_id":2,"title":"海南省政府党组成员","start":"","end":"present","rank":"副部级","note":""},

    # ── Predecessors ──
    {"person_id":18,"org_id":1,"title":"海南省委书记","start":"2020-12","end":"2023-03","rank":"正部级","note":"接替刘赐贵，后任冯飞"},
    {"person_id":18,"org_id":2,"title":"海南省省长","start":"2017-04","end":"2020-12","rank":"正部级","note":""},
    {"person_id":19,"org_id":1,"title":"海南省委书记","start":"","end":"2020-12","rank":"正部级","note":""},
    {"person_id":19,"org_id":2,"title":"海南省省长","start":"","end":"","rank":"正部级","note":""},

    # ── 李荣灿 ──
    {"person_id":21,"org_id":4,"title":"海南省政协主席","start":"","end":"present","rank":"正部级","note":""},

    # ── 人大 ──
    {"person_id":22,"org_id":3,"title":"海南省人大常委会副主任","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":23,"org_id":3,"title":"海南省人大常委会副主任","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":24,"org_id":3,"title":"海南省人大常委会副主任","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":25,"org_id":3,"title":"海南省人大常委会副主任","start":"","end":"present","rank":"副部级","note":""},

    # ── 两院 ──
    {"person_id":26,"org_id":7,"title":"海南省高级人民法院院长","start":"","end":"present","rank":"副部级","note":""},
    {"person_id":27,"org_id":8,"title":"海南省人民检察院检察长","start":"","end":"present","rank":"副部级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 冯飞 ↔ 刘小明 (successor-predecessor at 省长 → now work together)
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"冯飞任省委书记，刘小明任省长，党政一把手搭档","overlap_org":"中共海南省委员会","overlap_period":"2023-04至今","strength":"strong","confidence":"confirmed"},

    # 冯飞 ↔ 沈晓明 (predecessor-successor)
    {"person_a":1,"person_b":18,"type":"predecessor_successor","context":"冯飞接替沈晓明任海南省委书记","overlap_org":"中共海南省委员会","overlap_period":"2020-2023","strength":"strong","confidence":"confirmed"},

    # 沈晓明 ↔ 刘小明 (predecessor-successor at 省长)
    {"person_a":18,"person_b":2,"type":"predecessor_successor","context":"沈晓明任书记时刘小明接任省长","overlap_org":"海南省人民政府","overlap_period":"2023-04","strength":"strong","confidence":"confirmed"},

    # 冯飞 ↔ 刘赐贵 (predecessor chain)
    {"person_a":1,"person_b":19,"type":"predecessor_successor","context":"冯飞接替刘赐贵后任序列","overlap_org":"中共海南省委员会","overlap_period":"","strength":"medium","confidence":"plausible"},

    # 冯飞 ↔ 陈国猛 (work together - party committee members)
    {"person_a":1,"person_b":4,"type":"overlap","context":"同在海南省委常委会工作","overlap_org":"中共海南省委员会","overlap_period":"2021-04至今","strength":"strong","confidence":"confirmed"},

    # 刘小明 ↔ 陈国猛 (work together)
    {"person_a":2,"person_b":4,"type":"overlap","context":"同在海南省委常委会工作","overlap_org":"中共海南省委员会","overlap_period":"2023-04至今","strength":"strong","confidence":"confirmed"},

    # 巴特尔 ↔ 刘小明 (government team)
    {"person_a":2,"person_b":6,"type":"superior_subordinate","context":"省长与常务副省长工作关系","overlap_org":"海南省人民政府","overlap_period":"","strength":"strong","confidence":"confirmed"},

    # 陈国猛 ↔ 蓝佛安 (predecessor)
    {"person_a":4,"person_b":-1,"type":"predecessor_successor","context":"陈国猛接替蓝佛安任海南省纪委书记","strength":"medium","confidence":"confirmed","note":"蓝佛安不在本次数据集中"},

    # 沈晓明 ↔ 刘赐贵 (predecessor-successor)
    {"person_a":18,"person_b":19,"type":"predecessor_successor","context":"沈晓明接替刘赐贵任海南省委书记/省长","overlap_org":"中共海南省委员会","overlap_period":"2017-2020","strength":"strong","confidence":"confirmed"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS persons
        (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
         birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
         work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS organizations
        (id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
         parent TEXT, location TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS positions
        (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER,
         org_id INTEGER, title TEXT, start TEXT, end TEXT,
         rank TEXT, note TEXT,
         FOREIGN KEY(person_id) REFERENCES persons(id),
         FOREIGN KEY(org_id) REFERENCES organizations(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS relationships
        (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER,
         person_b INTEGER, type TEXT, context TEXT,
         overlap_org TEXT, overlap_period TEXT,
         strength TEXT, confidence TEXT,
         FOREIGN KEY(person_a) REFERENCES persons(id),
         FOREIGN KEY(person_b) REFERENCES persons(id))''')

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                   p["birthplace"],p["education"],p["party_join"],
                   p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
    for r in relationships:
        if r["person_b"] > 0:  # skip placeholder
            c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence) VALUES (?,?,?,?,?,?,?,?)",
                      (r["person_a"],r["person_b"],r["type"],r["context"],r.get("overlap_org",""),r.get("overlap_period",""),r["strength"],r["confidence"]))

    conn.commit()

    # Summary
    print(f"Database: {DB_PATH}")
    print(f"  Persons: {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()

def person_color(p):
    """Return r,g,b string based on role."""
    role = p.get("current_post","")
    name = p.get("name","")
    if "书记" in role and "纪委" not in role and name in ("冯飞",):
        return "255,50,50"  # Red — Party Secretary
    if "省长" in role and name in ("刘小明",):
        return "50,100,255"  # Blue — Governor
    if "纪委书记" in role or "纪委" in role:
        return "255,165,0"  # Orange — Discipline
    if "书记" in role:
        return "220,80,80"  # Light red — Other party secretaries
    if "省长" in role or "副省长" in role or "常务副省长" in role:
        return "80,130,255"  # Light blue — Gov leaders
    return "100,100,100"    # Grey — Others

def is_top_leader(p):
    return p["name"] in ("冯飞","刘小明")

def org_color(ot):
    colors = {
        "党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
        "政协":"255,240,200","事业单位":"220,220,220",
    }
    return colors.get(ot, "200,200,200")

def build_gexf():
    now = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>海南省领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="organization_type" type="string"/>')
    lines.append('      <attribute id="2" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        title = pos.get("title","")
        start = pos.get("start","")
        end_ = pos.get("end","")
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(end_)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        if r["person_b"] <= 0:
            continue
        eid += 1
        ctx = r.get("context","")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")
