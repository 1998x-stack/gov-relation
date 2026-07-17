#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Gansu Province (甘肃省) leadership network.

Covers: Provincial Party Secretary (省委书记), Governor (省长), predecessors,
succession chains, key deputy leaders (省委常委会成员, 副省长等),
and the provincial-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/甘肃省_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/甘肃省_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 胡昌升 — 甘肃省委书记 (as of 2022.12)
    {"id":1,"name":"胡昌升","gender":"男","ethnicity":"汉族","birth":"1963-12","birthplace":"江西高安","education":"成都地质学院（成都理工大学）资源与经济系、四川联合大学、山东大学历史学博士","party_join":"1986-01","work_start":"1986-07","current_post":"甘肃省委书记、省人大常委会主任","current_org":"中共甘肃省委员会","source":"https://zh.wikipedia.org/wiki/%E8%83%A1%E6%98%8C%E5%8D%87"},
    # 任振鹤 — 甘肃省省长
    {"id":2,"name":"任振鹤","gender":"男","ethnicity":"土家族","birth":"1964-02","birthplace":"湖北鹤峰","education":"恩施地区财经学校、华中工学院技术经济专业、中央党校思想政治教育在职研究生","party_join":"1984-12","work_start":"1982-09","current_post":"甘肃省委副书记、省长","current_org":"甘肃省人民政府","source":"https://zh.wikipedia.org/wiki/%E4%BB%BB%E6%8C%AF%E9%B9%A4"},

    # ── Provincial leadership (省委常委会成员) ──
    {"id":3,"name":"石谋军","gender":"男","ethnicity":"苗族","birth":"1968-02","birthplace":"湖南沅陵","education":"湖南农学院（湖南农业大学）作物专业、农业推广硕士","party_join":"1990-06","work_start":"1991-07","current_post":"甘肃省委副书记","current_org":"中共甘肃省委员会","source":"https://zh.wikipedia.org/wiki/%E7%9F%B3%E8%B0%8B%E5%86%9B"},
    {"id":4,"name":"雷东生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、省委秘书长","current_org":"中共甘肃省委员会","source":"https://www.gansu.gov.cn"},
    {"id":5,"name":"程晓波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、常务副省长","current_org":"甘肃省人民政府","source":"https://www.gansu.gov.cn"},
    {"id":6,"name":"孙雪涛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、统战部部长","current_org":"中共甘肃省委员会","source":"https://www.gansu.gov.cn"},
    {"id":7,"name":"刘长根","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、政法委书记","current_org":"中共甘肃省委员会","source":"https://www.gansu.gov.cn"},
    {"id":8,"name":"张永霞","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、宣传部部长","current_org":"中共甘肃省委员会","source":"https://www.gansu.gov.cn"},
    {"id":9,"name":"张晓强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、兰州市委书记","current_org":"中共兰州市委员会","source":"https://www.gansu.gov.cn"},
    {"id":10,"name":"靳国卫","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、省纪委书记、省监委主任","current_org":"中共甘肃省纪律检查委员会","source":"https://www.gansu.gov.cn"},
    {"id":11,"name":"刘建伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、省军区司令员","current_org":"甘肃省军区","source":"https://www.gansu.gov.cn"},
    {"id":12,"name":"王兵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省委常委、副省长","current_org":"甘肃省人民政府","source":"https://www.gansu.gov.cn"},

    # ── Vice governors (副省长) ──
    {"id":13,"name":"王钧","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省副省长","current_org":"甘肃省人民政府","source":"https://www.gansu.gov.cn"},
    {"id":14,"name":"王旭","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"甘肃省副省长","current_org":"甘肃省人民政府","source":"https://www.gansu.gov.cn"},
    {"id":15,"name":"葛建团","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"民建","work_start":"","current_post":"甘肃省副省长","current_org":"甘肃省人民政府","source":"https://www.gansu.gov.cn"},

    # ── Predecessors — 省委书记 ──
    {"id":16,"name":"尹弘","gender":"男","ethnicity":"汉族","birth":"1963-06","birthplace":"浙江湖州","education":"","party_join":"","work_start":"","current_post":"江西省委书记（原甘肃省委书记）","current_org":"中共江西省委员会","source":"https://zh.wikipedia.org/wiki/%E5%B0%B9%E5%BC%98"},
    {"id":17,"name":"林铎","gender":"男","ethnicity":"汉族","birth":"1956-03","birthplace":"山东菏泽","education":"","party_join":"","work_start":"","current_post":"全国人大华侨委员会副主任委员（原甘肃省委书记）","current_org":"全国人大常委会","source":"https://baike.baidu.com/item/%E6%9E%97%E9%93%8E"},
    {"id":18,"name":"王三运","gender":"男","ethnicity":"汉族","birth":"1952-12","birthplace":"山东单县","education":"","party_join":"","work_start":"","current_post":"原甘肃省委书记（已落马）","current_org":"","source":"https://baike.baidu.com/item/%E7%8E%8B%E4%B8%89%E8%BF%90"},

    # ── Predecessors — 省长 ──
    {"id":19,"name":"唐仁健","gender":"男","ethnicity":"汉族","birth":"1962-08","birthplace":"重庆","education":"西南财经大学政治经济学博士","party_join":"1991-03","work_start":"1983-08","current_post":"原农业农村部部长（已落马，原甘肃省省长）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E5%94%90%E4%BB%81%E5%81%A5"},
    {"id":20,"name":"刘伟平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原甘肃省省长","current_org":"","source":"https://baike.baidu.com"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Gansu provincial core
    {"id":1,"name":"中共甘肃省委员会","type":"党委","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":2,"name":"甘肃省人民政府","type":"政府","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":3,"name":"甘肃省人大常委会","type":"人大","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":4,"name":"政协甘肃省委员会","type":"政协","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":5,"name":"中共甘肃省纪律检查委员会","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":6,"name":"甘肃省军区","type":"党委","level":"省级","parent":"中央军委","location":"甘肃省兰州市"},

    # Key provincial departments
    {"id":7,"name":"中共甘肃省委组织部","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":8,"name":"中共甘肃省委宣传部","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":9,"name":"中共甘肃省委统战部","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":10,"name":"中共甘肃省委政法委","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":11,"name":"中共甘肃省委办公厅","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},

    # Key city
    {"id":12,"name":"中共兰州市委员会","type":"党委","level":"副省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},

    # Central / national orgs
    {"id":13,"name":"国务院","type":"政府","level":"国家级","parent":"","location":"北京市"},
    {"id":14,"name":"全国人大常委会","type":"人大","level":"国家级","parent":"","location":"北京市"},
    {"id":15,"name":"中央军委","type":"党委","level":"国家级","parent":"","location":"北京市"},

    # 胡昌升 earlier work units
    {"id":16,"name":"成都地质学院（成都理工大学）","type":"事业单位","level":"","parent":"","location":"四川省成都市"},
    {"id":17,"name":"成都市锦江区人民政府","type":"政府","level":"副省级","parent":"成都市人民政府","location":"四川省成都市"},
    {"id":18,"name":"中共荥经县委员会","type":"党委","level":"县级","parent":"中共雅安市委员会","location":"四川省雅安市荥经县"},
    {"id":19,"name":"中共雅安市委员会","type":"党委","level":"地级","parent":"中共四川省委员会","location":"四川省雅安市"},
    {"id":20,"name":"中共汉源县委员会","type":"党委","level":"县级","parent":"中共雅安市委员会","location":"四川省雅安市汉源县"},
    {"id":21,"name":"中共遂宁市委员会","type":"党委","level":"地级","parent":"中共四川省委员会","location":"四川省遂宁市"},
    {"id":22,"name":"遂宁市人民政府","type":"政府","level":"地级","parent":"四川省人民政府","location":"四川省遂宁市"},
    {"id":23,"name":"中共甘孜藏族自治州委员会","type":"党委","level":"地级","parent":"中共四川省委员会","location":"四川省甘孜藏族自治州"},
    {"id":24,"name":"中共青海省委员会","type":"党委","level":"省级","parent":"","location":"青海省西宁市"},
    {"id":25,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
    {"id":26,"name":"中共厦门市委员会","type":"党委","level":"副省级","parent":"中共福建省委员会","location":"福建省厦门市"},
    {"id":27,"name":"中共黑龙江省委员会","type":"党委","level":"省级","parent":"","location":"黑龙江省哈尔滨市"},
    {"id":28,"name":"黑龙江省人民政府","type":"政府","level":"省级","parent":"","location":"黑龙江省哈尔滨市"},
    {"id":29,"name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},

    # 任振鹤 earlier work units
    {"id":30,"name":"鹤峰县民族贸易局","type":"政府","level":"县级","parent":"鹤峰县人民政府","location":"湖北省恩施州鹤峰县"},
    {"id":31,"name":"中共利川市委员会","type":"党委","level":"县级","parent":"中共恩施州委员会","location":"湖北省恩施州利川市"},
    {"id":32,"name":"利川市人民政府","type":"政府","level":"县级","parent":"湖北省人民政府","location":"湖北省恩施州利川市"},
    {"id":33,"name":"恩施土家族苗族自治州人民政府","type":"政府","level":"地级","parent":"湖北省人民政府","location":"湖北省恩施州"},
    {"id":34,"name":"中共黄冈市委员会","type":"党委","level":"地级","parent":"中共湖北省委员会","location":"湖北省黄冈市"},
    {"id":35,"name":"中共咸宁市委员会","type":"党委","level":"地级","parent":"中共湖北省委员会","location":"湖北省咸宁市"},
    {"id":36,"name":"咸宁市人民政府","type":"政府","level":"地级","parent":"湖北省人民政府","location":"湖北省咸宁市"},
    {"id":37,"name":"湖北省人民政府","type":"政府","level":"省级","parent":"","location":"湖北省武汉市"},
    {"id":38,"name":"中共湖北省委员会","type":"党委","level":"省级","parent":"","location":"湖北省武汉市"},
    {"id":39,"name":"中共襄阳市委员会","type":"党委","level":"地级","parent":"中共湖北省委员会","location":"湖北省襄阳市"},
    {"id":40,"name":"中共浙江省委员会","type":"党委","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":41,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},

    # 石谋军 earlier
    {"id":42,"name":"湖南省人民政府","type":"政府","level":"省级","parent":"","location":"湖南省长沙市"},
    {"id":43,"name":"西藏自治区人民政府","type":"政府","level":"省级","parent":"","location":"西藏自治区拉萨市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 胡昌升 ──
    {"id":1,"person_id":1,"org_id":1,"title":"甘肃省委书记","start":"2022-12","end":"","rank":"正部级","note":"2022.12从黑龙江调任甘肃省委书记；2023.01兼任省人大常委会主任"},
    {"id":2,"person_id":1,"org_id":28,"title":"黑龙江省省长","start":"2021-02","end":"2022-12","rank":"正部级","note":"2021.02任黑龙江省代省长，后当选省长"},
    {"id":3,"person_id":1,"org_id":27,"title":"黑龙江省委副书记、省政府党组书记","start":"2021-01","end":"2021-02","rank":"正部级","note":"2021.01从福建调任黑龙江"},
    {"id":4,"person_id":1,"org_id":26,"title":"福建省委副书记、厦门市委书记","start":"2020-09","end":"2021-01","rank":"副部级","note":""},
    {"id":5,"person_id":1,"org_id":25,"title":"福建省委常委、厦门市委书记","start":"2019-02","end":"2020-09","rank":"副部级","note":""},
    {"id":6,"person_id":1,"org_id":25,"title":"福建省委常委、组织部部长","start":"2017-07","end":"2019-06","rank":"副部级","note":""},
    {"id":7,"person_id":1,"org_id":24,"title":"青海省委常委、组织部部长","start":"2015-06","end":"2017-07","rank":"副部级","note":""},
    {"id":8,"person_id":1,"org_id":23,"title":"甘孜州委书记","start":"2012-04","end":"2015-06","rank":"正厅级","note":"2012.04任甘孜州委副书记，同年任州委书记"},
    {"id":9,"person_id":1,"org_id":22,"title":"遂宁市市长","start":"2006-11","end":"2012-04","rank":"正厅级","note":"2006.11任代市长，2007.02当选市长"},
    {"id":10,"person_id":1,"org_id":20,"title":"雅安市委常委、汉源县委书记","start":"2005-10","end":"2006-11","rank":"副厅级","note":""},
    {"id":11,"person_id":1,"org_id":19,"title":"雅安市委常委、组织部部长","start":"2004-02","end":"2005-10","rank":"副厅级","note":""},
    {"id":12,"person_id":1,"org_id":18,"title":"荥经县委书记","start":"2002-11","end":"2004-02","rank":"正处级","note":"2003.01兼任县人大常委会主任"},
    {"id":13,"person_id":1,"org_id":17,"title":"成都市锦江区副区长","start":"1998-12","end":"2002-11","rank":"副厅级","note":""},
    {"id":14,"person_id":1,"org_id":16,"title":"成都地质学院（成都理工大学）教师","start":"1986-07","end":"1998-12","rank":"","note":"历任教师、团总支书记、党总支副书记、书记等职务"},

    # ── 任振鹤 ──
    {"id":15,"person_id":2,"org_id":2,"title":"甘肃省省长","start":"2020-12","end":"","rank":"正部级","note":"2020.12任代省长，2021.01当选省长"},
    {"id":16,"person_id":2,"org_id":41,"title":"江苏省委副书记","start":"2019-07","end":"2020-12","rank":"副部级","note":""},
    {"id":17,"person_id":2,"org_id":40,"title":"浙江省委常委、纪委书记、省监委主任","start":"2018-05","end":"2019-07","rank":"副部级","note":"2018.05任省监委副主任、代主任，2019.01当选主任"},
    {"id":18,"person_id":2,"org_id":40,"title":"浙江省委常委、组织部部长","start":"2017-02","end":"2018-07","rank":"副部级","note":""},
    {"id":19,"person_id":2,"org_id":39,"title":"湖北省委常委、襄阳市委书记","start":"2016-12","end":"2017-02","rank":"副部级","note":""},
    {"id":20,"person_id":2,"org_id":37,"title":"湖北省副省长","start":"2015-05","end":"2017-01","rank":"副部级","note":""},
    {"id":21,"person_id":2,"org_id":35,"title":"咸宁市委书记","start":"2012-08","end":"2015-05","rank":"正厅级","note":""},
    {"id":22,"person_id":2,"org_id":36,"title":"咸宁市市长","start":"2008-04","end":"2012-08","rank":"正厅级","note":"2008.04任代市长，2008.06当选市长"},
    {"id":23,"person_id":2,"org_id":34,"title":"黄冈市委副书记","start":"2006-08","end":"2008-03","rank":"副厅级","note":""},
    {"id":24,"person_id":2,"org_id":33,"title":"恩施州副州长","start":"2003-06","end":"2006-08","rank":"副厅级","note":""},
    {"id":25,"person_id":2,"org_id":31,"title":"利川市委书记","start":"1998-12","end":"2001-11","rank":"正处级","note":""},
    {"id":26,"person_id":2,"org_id":32,"title":"利川市代市长、市长","start":"1996-11","end":"1998-12","rank":"正处级","note":""},
    {"id":27,"person_id":2,"org_id":30,"title":"鹤峰县民族贸易局/县政府工作","start":"1982-09","end":"1996-11","rank":"","note":"从统计员逐步晋升至县委常委、副县长、县委副书记"},

    # ── 石谋军 ──
    {"id":28,"person_id":3,"org_id":1,"title":"甘肃省委副书记","start":"2023-12","end":"","rank":"副部级","note":""},
    {"id":29,"person_id":3,"org_id":7,"title":"甘肃省委组织部部长","start":"2022-01","end":"2024-02","rank":"副部级","note":""},
    {"id":30,"person_id":3,"org_id":2,"title":"甘肃省常务副省长","start":"2021-07","end":"2022-01","rank":"副部级","note":""},
    {"id":31,"person_id":3,"org_id":11,"title":"甘肃省委常委、省委秘书长","start":"2020-07","end":"2022-06","rank":"副部级","note":""},
    {"id":32,"person_id":3,"org_id":43,"title":"西藏自治区副主席","start":"2017-02","end":"2020-07","rank":"副部级","note":""},

    # ── Predecessors — 省委书记 ──
    {"id":33,"person_id":16,"org_id":1,"title":"甘肃省委书记","start":"2021","end":"2022-12","rank":"正部级","note":"后调任江西省委书记"},
    {"id":34,"person_id":17,"org_id":1,"title":"甘肃省委书记","start":"2017","end":"2021","rank":"正部级","note":""},
    {"id":35,"person_id":18,"org_id":1,"title":"甘肃省委书记","start":"2011","end":"2017","rank":"正部级","note":"已落马"},

    # ── Predecessors — 省长 ──
    {"id":36,"person_id":19,"org_id":2,"title":"甘肃省省长","start":"2017-04","end":"2020-12","rank":"正部级","note":"后任农业农村部部长；2024年落马"},
    {"id":37,"person_id":20,"org_id":2,"title":"甘肃省省长","start":"","end":"2017","rank":"正部级","note":""},

    # ── Current Standing Committee members (basic) ──
    {"id":38,"person_id":4,"org_id":11,"title":"甘肃省委常委、省委秘书长","start":"","end":"","rank":"副部级","note":""},
    {"id":39,"person_id":5,"org_id":2,"title":"甘肃省委常委、常务副省长","start":"","end":"","rank":"副部级","note":""},
    {"id":40,"person_id":6,"org_id":9,"title":"甘肃省委常委、统战部部长","start":"","end":"","rank":"副部级","note":""},
    {"id":41,"person_id":7,"org_id":10,"title":"甘肃省委常委、政法委书记","start":"","end":"","rank":"副部级","note":""},
    {"id":42,"person_id":8,"org_id":8,"title":"甘肃省委常委、宣传部部长","start":"","end":"","rank":"副部级","note":""},
    {"id":43,"person_id":9,"org_id":12,"title":"甘肃省委常委、兰州市委书记","start":"","end":"","rank":"副部级","note":""},
    {"id":44,"person_id":10,"org_id":5,"title":"甘肃省委常委、省纪委书记、省监委主任","start":"","end":"","rank":"副部级","note":""},
    {"id":45,"person_id":11,"org_id":6,"title":"甘肃省委常委、省军区司令员","start":"","end":"","rank":"副部级","note":""},
    {"id":46,"person_id":12,"org_id":2,"title":"甘肃省委常委、副省长","start":"","end":"","rank":"副部级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 胡昌升 -> 任振鹤 (current top duo)
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate","context":"胡昌升任甘肃省委书记，任振鹤任甘肃省省长，两人为当前甘肃党政主要领导搭档","overlap_org":"中共甘肃省委员会、甘肃省人民政府","overlap_period":"2022.12至今","strength":"strong","confidence":"confirmed"},
    # 胡昌升 -> 尹弘 (predecessor-successor, 省委书记)
    {"id":2,"person_a":16,"person_b":1,"type":"predecessor_successor","context":"尹弘2021-2022.12任甘肃省委书记，胡昌升2022.12接任","overlap_org":"中共甘肃省委员会","overlap_period":"2021-2022","strength":"strong","confidence":"confirmed"},
    # 尹弘 -> 林铎
    {"id":3,"person_a":17,"person_b":16,"type":"predecessor_successor","context":"林铎2017-2021任甘肃省委书记，尹弘2021接任","overlap_org":"中共甘肃省委员会","overlap_period":"2017-2021","strength":"strong","confidence":"confirmed"},
    # 任振鹤 -> 唐仁健 (predecessor-successor, 省长)
    {"id":4,"person_a":19,"person_b":2,"type":"predecessor_successor","context":"唐仁健2017-2020.12任甘肃省省长，任振鹤2020.12接任","overlap_org":"甘肃省人民政府","overlap_period":"2017-2020","strength":"strong","confidence":"confirmed"},
    # 胡昌升 -> 石谋军 (superior-subordinate)
    {"id":5,"person_a":1,"person_b":3,"type":"superior_subordinate","context":"胡昌升任书记，石谋军任副书记","overlap_org":"中共甘肃省委员会","overlap_period":"2023.12至今","strength":"strong","confidence":"confirmed"},
    # 任振鹤 -> 石谋军 (colleagues in provincial leadership)
    {"id":6,"person_a":2,"person_b":3,"type":"overlap","context":"任振鹤任省长，石谋军任副书记，同届甘肃省委领导班子成员","overlap_org":"中共甘肃省委员会","overlap_period":"2023.12至今","strength":"strong","confidence":"confirmed"},
    # 胡昌升 -> 唐仁健 (no direct Gansu overlap, but both served as provincial leaders)
    {"id":7,"person_a":1,"person_b":19,"type":"predecessor_successor","context":"胡昌升就任甘肃省委书记前，唐仁健已任甘肃省长（2017-2020），两人任期无直接重叠，但与尹弘、林铎形成完整任期链条","overlap_org":"甘肃省","overlap_period":"","strength":"weak","confidence":"unverified"},
    # 胡昌升曾在福建、青海、四川等地任职，与甘肃本地干部无直接前共事关系
]

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# Color by role/type
def person_color(p):
    name = p["name"]
    current = p.get("current_post", "")
    is_party_sec = "书记" in current and "副" not in current.split("书记")[0]
    is_gov_head = "省长" in current and "副" not in current
    is_discipline = "纪委书记" in current or "监委" in current
    if is_party_sec:
        return "255,50,50"
    elif is_gov_head:
        return "50,100,255"
    elif is_discipline:
        return "255,165,0"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(p):
    name = p["name"]
    current = p.get("current_post", "")
    return ("书记" in current and "副" not in current.split("书记")[0]) or ("省长" in current and "副" not in current)

# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
                   p.get("birth",""), p.get("birthplace",""), p.get("education",""),
                   p.get("party_join",""), p.get("work_start",""),
                   p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o.get("type",""), o.get("level",""),
                   o.get("parent",""), o.get("location","")))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start",""), pos.get("end",""), pos.get("rank",""),
                   pos.get("note","")))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    from datetime import datetime

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>甘肃省领导关系网络 - Provincial Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship), weight="2.0"
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
