#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Tibet Autonomous Region (西藏自治区) leadership network.

Covers: Party Secretary (自治区党委书记), Government Chairman (自治区政府主席),
predecessors, succession chains, key deputy leaders (Standing Committee members),
and the provincial-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/xizang_province")
DB_PATH = os.path.join(STAGING, "西藏自治区_network.db")
GEXF_PATH = os.path.join(STAGING, "西藏自治区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 王君正 — 西藏自治区党委书记 (as of 2021.10)
    {"id":1,"name":"王君正","gender":"男","ethnicity":"汉族","birth":"1963-05-17","birthplace":"山东临沂","education":"山东大学、中国人民大学（马克思主义理论博士）、清华大学（管理学博士）","party_join":"1987-11","work_start":"1985","current_post":"西藏自治区党委书记","current_org":"中共西藏自治区委员会","source":"https://en.wikipedia.org/wiki/Wang_Junzheng"},
    # 嘎玛泽登 — 西藏自治区政府主席
    {"id":2,"name":"嘎玛泽登","gender":"男","ethnicity":"藏族","birth":"1967-12","birthplace":"西藏江达","education":"中央民族大学（民族理论与政策）、四川大学（公共管理硕士）、中央党校","party_join":"1992-05","work_start":"1990-07","current_post":"西藏自治区党委副书记、政府主席","current_org":"西藏自治区人民政府","source":"https://en.wikipedia.org/wiki/Garma_Cedain"},
    # 严金海 — 自治区人大常委会主任、原主席
    {"id":3,"name":"严金海","gender":"男","ethnicity":"藏族","birth":"1962-03","birthplace":"青海民和","education":"青海民族学院（1978-1982）","party_join":"1983-12","work_start":"1982-07","current_post":"西藏自治区人大常委会主任","current_org":"西藏自治区人大常委会","source":"https://en.wikipedia.org/wiki/Yan_Jinhai"},
    # 陈永奇 — 党委副书记（专职党务副书记）
    {"id":4,"name":"陈永奇","gender":"男","ethnicity":"汉族","birth":"1967-11","birthplace":"山西","education":"","party_join":"1985","work_start":"","current_post":"西藏自治区党委副书记","current_org":"中共西藏自治区委员会","source":"https://en.wikipedia.org/wiki/Tibet_Autonomous_Regional_Committee_of_the_Chinese_Communist_Party"},
    # 任维 — 党委常委、常务副主席
    {"id":5,"name":"任维","gender":"男","ethnicity":"汉族","birth":"1976-05","birthplace":"陕西岐山","education":"清华大学（热能动力工程学士、博士）","party_join":"1997-06","work_start":"2003-07","current_post":"西藏自治区党委常委、常务副主席","current_org":"西藏自治区人民政府","source":"https://en.wikipedia.org/wiki/Ren_Wei_(politician)"},
    # 罗布顿珠 — 党委常委、常务副主席
    {"id":6,"name":"罗布顿珠","gender":"男","ethnicity":"藏族","birth":"1960-12","birthplace":"西藏琼结","education":"中央政法干部学校（现中国人民公安大学）","party_join":"","work_start":"1978","current_post":"西藏自治区党委常委、常务副主席","current_org":"西藏自治区人民政府","source":"https://en.wikipedia.org/wiki/Norbu_Dondrup"},
    # 刘江 — 党委副书记、政法委书记
    {"id":7,"name":"刘江","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委副书记、政法委书记","current_org":"中共西藏自治区委员会","source":"https://en.wikipedia.org/wiki/Tibet_Autonomous_Regional_Committee_of_the_Chinese_Communist_Party"},
    # 王卫东 — 党委常委、纪委书记、监委主任
    {"id":8,"name":"王卫东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委、纪委书记、监委主任","current_org":"中共西藏自治区纪律检查委员会","source":"https://en.wikipedia.org/wiki/Tibet_Autonomous_Regional_Committee_of_the_Chinese_Communist_Party"},
    # 赖蛟 — 党委常委、组织部部长
    {"id":9,"name":"赖蛟","gender":"男","ethnicity":"汉族","birth":"1972-04","birthplace":"重庆","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委、组织部部长","current_org":"中共西藏自治区委员会","source":"https://en.wikipedia.org/wiki/Tibet_Autonomous_Regional_Committee_of_the_Chinese_Communist_Party"},
    # 袁红刚 — 党委常委（军区代表）
    {"id":10,"name":"袁红刚","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委","current_org":"中共西藏自治区委员会","source":"https://xzdw.gov.cn"},
    # 才让太 — 党委常委
    {"id":11,"name":"才让太","gender":"男","ethnicity":"藏族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委","current_org":"中共西藏自治区委员会","source":"https://xzdw.gov.cn"},
    # 达娃次仁 — 党委常委
    {"id":12,"name":"达娃次仁","gender":"男","ethnicity":"藏族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委","current_org":"中共西藏自治区委员会","source":"https://xzdw.gov.cn"},
    # 龚会才 — 党委常委
    {"id":13,"name":"龚会才","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委","current_org":"中共西藏自治区委员会","source":"https://xzdw.gov.cn"},
    # 旦巴 — 党委常委
    {"id":14,"name":"旦巴","gender":"男","ethnicity":"藏族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委","current_org":"中共西藏自治区委员会","source":"https://xzdw.gov.cn"},
    # 姜文鹏 — 党委常委
    {"id":15,"name":"姜文鹏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委","current_org":"中共西藏自治区委员会","source":"https://xzdw.gov.cn"},
    # 徐芝文 — 党委常委
    {"id":16,"name":"徐芝文","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西藏自治区党委常委","current_org":"中共西藏自治区委员会","source":"https://xzdw.gov.cn"},

    # ── Predecessors — 党委书记 ──
    {"id":17,"name":"吴英杰","gender":"男","ethnicity":"汉族","birth":"1956-12","birthplace":"山东昌邑","education":"西藏民族大学","party_join":"","work_start":"","current_post":"原西藏自治区党委书记（2024年被查）","current_org":"","source":"https://en.wikipedia.org/wiki/Wu_Yingjie"},
    {"id":18,"name":"陈全国","gender":"男","ethnicity":"汉族","birth":"1955-11","birthplace":"河南平舆","education":"陆军指挥学院","party_join":"","work_start":"","current_post":"原西藏自治区党委书记（后调任新疆）","current_org":"","source":"https://en.wikipedia.org/wiki/Chen_Quanguo"},
    {"id":19,"name":"张庆黎","gender":"男","ethnicity":"汉族","birth":"1951-01","birthplace":"山东东平","education":"","party_join":"","work_start":"","current_post":"原西藏自治区党委书记（后任河北省委书记、全国政协副主席）","current_org":"","source":"https://en.wikipedia.org/wiki/Zhang_Qingli"},
    {"id":20,"name":"杨传堂","gender":"男","ethnicity":"汉族","birth":"1954-05","birthplace":"山东禹城","education":"","party_join":"","work_start":"","current_post":"原西藏自治区党委书记（后任交通部部长、全国政协副主席）","current_org":"","source":"https://en.wikipedia.org/wiki/Yang_Chuantang"},
    {"id":21,"name":"郭金龙","gender":"男","ethnicity":"汉族","birth":"1947-07","birthplace":"江苏南京","education":"南京大学","party_join":"","work_start":"","current_post":"原西藏自治区党委书记（后任安徽省委书记、北京市委书记、中央政治局委员）","current_org":"","source":"https://en.wikipedia.org/wiki/Guo_Jinlong"},
    {"id":22,"name":"陈奎元","gender":"男","ethnicity":"汉族","birth":"1941-01","birthplace":"辽宁康平","education":"","party_join":"","work_start":"","current_post":"原西藏自治区党委书记（后任中国社会科学院院长、全国政协副主席）","current_org":"","source":"https://en.wikipedia.org/wiki/Chen_Kuiyuan"},
    {"id":23,"name":"胡锦涛","gender":"男","ethnicity":"汉族","birth":"1942-12","birthplace":"安徽绩溪","education":"清华大学（水利工程系）","party_join":"","work_start":"","current_post":"原西藏自治区党委书记（后任国家主席、中共中央总书记）","current_org":"","source":"https://en.wikipedia.org/wiki/Hu_Jintao"},

    # ── Predecessors — 政府主席 ──
    {"id":24,"name":"齐扎拉","gender":"男","ethnicity":"藏族","birth":"1958-11","birthplace":"云南香格里拉","education":"中央党校","party_join":"","work_start":"","current_post":"原西藏自治区政府主席（2025年被查，2026年判无期）","current_org":"","source":"https://en.wikipedia.org/wiki/Che_Dalha"},
    {"id":25,"name":"洛桑江村","gender":"男","ethnicity":"藏族","birth":"1957-07","birthplace":"西藏察雅","education":"","party_join":"","work_start":"","current_post":"原西藏自治区政府主席（后任自治区人大常委会主任、全国人大副委员长）","current_org":"","source":"https://en.wikipedia.org/wiki/Losang_Jamcan"},
    {"id":26,"name":"白玛赤林","gender":"男","ethnicity":"藏族","birth":"1952-01","birthplace":"西藏丁青","education":"","party_join":"","work_start":"","current_post":"原西藏自治区政府主席（后任全国人大副委员长）","current_org":"","source":"https://en.wikipedia.org/wiki/Padma_Choling"},
    {"id":27,"name":"向巴平措","gender":"男","ethnicity":"藏族","birth":"1947-04","birthplace":"西藏昌都","education":"","party_join":"","work_start":"","current_post":"原西藏自治区政府主席（后任全国人大副委员长）","current_org":"","source":"https://en.wikipedia.org/wiki/Qiangba_Puncog"},
    {"id":28,"name":"热地","gender":"男","ethnicity":"藏族","birth":"1938-08","birthplace":"西藏比如","education":"","party_join":"","work_start":"","current_post":"原西藏自治区政府主席（后任全国人大副委员长）","current_org":"","source":"https://en.wikipedia.org/wiki/Raqdi"},
    {"id":29,"name":"江村罗布","gender":"男","ethnicity":"藏族","birth":"1932","birthplace":"西藏江达","education":"","party_join":"","work_start":"","current_post":"原西藏自治区政府主席（后任全国人大副委员长）","current_org":"","source":"https://en.wikipedia.org/wiki/Jiangcun_Norbu"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Tibet provincial core
    {"id":1,"name":"中共西藏自治区委员会","type":"党委","level":"省级","parent":"","location":"西藏自治区拉萨市"},
    {"id":2,"name":"西藏自治区人民政府","type":"政府","level":"省级","parent":"","location":"西藏自治区拉萨市"},
    {"id":3,"name":"西藏自治区人大常委会","type":"人大","level":"省级","parent":"","location":"西藏自治区拉萨市"},
    {"id":4,"name":"政协西藏自治区委员会","type":"政协","level":"省级","parent":"","location":"西藏自治区拉萨市"},
    {"id":5,"name":"中共西藏自治区纪律检查委员会","type":"党委","level":"省级","parent":"中共西藏自治区委员会","location":"西藏自治区拉萨市"},
    {"id":6,"name":"西藏自治区高级人民法院","type":"党委","level":"省级","parent":"","location":"西藏自治区拉萨市"},

    # Key provincial departments
    {"id":7,"name":"中共西藏自治区委员会组织部","type":"党委","level":"省级","parent":"中共西藏自治区委员会","location":"西藏自治区拉萨市"},
    {"id":8,"name":"中共西藏自治区委员会宣传部","type":"党委","level":"省级","parent":"中共西藏自治区委员会","location":"西藏自治区拉萨市"},
    {"id":9,"name":"中共西藏自治区委员会统战部","type":"党委","level":"省级","parent":"中共西藏自治区委员会","location":"西藏自治区拉萨市"},
    {"id":10,"name":"中共西藏自治区委员会政法委","type":"党委","level":"省级","parent":"中共西藏自治区委员会","location":"西藏自治区拉萨市"},
    {"id":11,"name":"中共西藏自治区委员会办公厅","type":"党委","level":"省级","parent":"中共西藏自治区委员会","location":"西藏自治区拉萨市"},

    # Earlier work units / former provinces
    {"id":12,"name":"国务院","type":"政府","level":"国家级","parent":"","location":"北京市"},
    {"id":13,"name":"全国人大常委会","type":"人大","level":"国家级","parent":"","location":"北京市"},
    {"id":14,"name":"全国政协","type":"政协","level":"国家级","parent":"","location":"北京市"},
    {"id":15,"name":"北京市","type":"政府","level":"国家级","parent":"","location":"北京市"},
    {"id":16,"name":"中共新疆维吾尔自治区委员会","type":"党委","level":"省级","parent":"","location":"新疆乌鲁木齐"},
    {"id":17,"name":"中共河北省委员会","type":"党委","level":"省级","parent":"","location":"河北省石家庄市"},
    {"id":18,"name":"中共青海省委员会","type":"党委","level":"省级","parent":"","location":"青海省西宁市"},
    {"id":19,"name":"中共安徽省委员会","type":"党委","level":"省级","parent":"","location":"安徽省合肥市"},
    {"id":20,"name":"中共云南省委员会","type":"党委","level":"省级","parent":"","location":"云南省昆明市"},
    {"id":21,"name":"中共湖北省委员会","type":"党委","level":"省级","parent":"","location":"湖北省武汉市"},
    {"id":22,"name":"中国国电集团","type":"事业单位","level":"国家级","parent":"","location":"北京市"},
    {"id":23,"name":"中国大唐集团","type":"事业单位","level":"国家级","parent":"","location":"北京市"},
    {"id":24,"name":"西藏自治区那曲地区","type":"党委","level":"地级","parent":"中共西藏自治区委员会","location":"西藏自治区那曲市"},
    {"id":25,"name":"西藏自治区昌都市","type":"党委","level":"地级","parent":"中共西藏自治区委员会","location":"西藏自治区昌都市"},
    {"id":26,"name":"西藏自治区山南市","type":"党委","level":"地级","parent":"中共西藏自治区委员会","location":"西藏自治区山南市"},
    {"id":27,"name":"拉萨市","type":"党委","level":"地级","parent":"中共西藏自治区委员会","location":"西藏自治区拉萨市"},
    {"id":28,"name":"西藏自治区文化和旅游部（挂职）","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":29,"name":"中共重庆市委员会","type":"党委","level":"省级","parent":"","location":"重庆市"},
    {"id":30,"name":"清华大学","type":"事业单位","level":"","parent":"","location":"北京市"},
    {"id":31,"name":"中央民族大学","type":"事业单位","level":"","parent":"","location":"北京市"},
    {"id":32,"name":"中共山西省委员会","type":"党委","level":"省级","parent":"","location":"山西省太原市"},
    {"id":33,"name":"山东省","type":"政府","level":"省级","parent":"","location":"山东省"},
    {"id":34,"name":"中国社会科委员","type":"事业单位","level":"国家级","parent":"","location":"北京市"},
    {"id":35,"name":"中共新疆生产建设兵团","type":"党委","level":"省级","parent":"","location":"新疆"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 王君正 ──
    {"id":1,"person_id":1,"org_id":1,"title":"西藏自治区党委书记","start":"2021-10","end":"","rank":"正部级","note":"2021.10.18任西藏自治区党委书记"},
    {"id":2,"person_id":1,"org_id":35,"title":"新疆生产建设兵团党委书记、政委","start":"2020-05","end":"2021-10","rank":"正部级","note":""},
    {"id":3,"person_id":1,"org_id":16,"title":"新疆维吾尔自治区党委常委、政法委书记","start":"2019-02","end":"2021-10","rank":"副部级","note":""},
    {"id":4,"person_id":1,"org_id":15,"title":"吉林省委常委、长春市委书记","start":"2016-01","end":"2019-02","rank":"副部级","note":""},
    {"id":5,"person_id":1,"org_id":21,"title":"湖北省委常委、襄阳市委书记","start":"2013-05","end":"2016-01","rank":"副部级","note":""},
    {"id":6,"person_id":1,"org_id":20,"title":"湖北省副省长","start":"2012-09","end":"2013-05","rank":"副部级","note":""},
    {"id":7,"person_id":1,"org_id":28,"title":"丽江市市委书记","start":"2009","end":"2012-09","rank":"正厅级","note":""},
    {"id":8,"person_id":1,"org_id":28,"title":"丽江市市长","start":"2007","end":"2009","rank":"正厅级","note":""},
    {"id":9,"person_id":1,"org_id":20,"title":"云南省高级人民法院副院长","start":"2005","end":"2007","rank":"副厅级","note":""},
    {"id":10,"person_id":1,"org_id":20,"title":"云南省昆明市官渡区委书记","start":"2000","end":"2005","rank":"正处级","note":""},

    # ── 嘎玛泽登 ──
    {"id":11,"person_id":2,"org_id":2,"title":"西藏自治区政府主席","start":"2025-01","end":"","rank":"正部级","note":"2024.11代理，2025.01当选"},
    {"id":12,"person_id":2,"org_id":1,"title":"西藏自治区党委副书记","start":"2024-10","end":"","rank":"副部级","note":""},
    {"id":13,"person_id":2,"org_id":9,"title":"西藏自治区党委统战部部长","start":"2021-12","end":"2024-10","rank":"副部级","note":"兼自治区政协副主席"},
    {"id":14,"person_id":2,"org_id":1,"title":"西藏自治区党委常委","start":"2021-10","end":"","rank":"副部级","note":""},
    {"id":15,"person_id":2,"org_id":28,"title":"文化和旅游部科技教育司司长","start":"2020-10","end":"2021-10","rank":"正厅级","note":"中央挂职"},
    {"id":16,"person_id":2,"org_id":1,"title":"西藏自治区民政厅党组书记","start":"2018-10","end":"2020-10","rank":"正厅级","note":""},
    {"id":17,"person_id":2,"org_id":1,"title":"西藏自治区民政厅党组副书记、厅长","start":"2017-05","end":"2018-10","rank":"正厅级","note":""},
    {"id":18,"person_id":2,"org_id":24,"title":"那曲地委常务副书记","start":"2011-12","end":"2012-10","rank":"副厅级","note":"兼政法委书记、公安处书记"},
    {"id":19,"person_id":2,"org_id":24,"title":"那曲地委委员、行署常务副专员","start":"2008-01","end":"2011-12","rank":"副厅级","note":""},
    {"id":20,"person_id":2,"org_id":24,"title":"那曲地区行署委员、副专员","start":"2005-07","end":"2008-01","rank":"副厅级","note":""},

    # ── 严金海 ──
    {"id":21,"person_id":3,"org_id":3,"title":"西藏自治区人大常委会主任","start":"2025-01","end":"","rank":"正部级","note":""},
    {"id":22,"person_id":3,"org_id":2,"title":"西藏自治区政府主席","start":"2021-10","end":"2024-11","rank":"正部级","note":""},
    {"id":23,"person_id":3,"org_id":1,"title":"西藏自治区党委副书记","start":"2020-07","end":"2024-11","rank":"副部级","note":""},
    {"id":24,"person_id":3,"org_id":18,"title":"青海省委常委、农牧区工作部部长","start":"Filed-","end":"2020-07","rank":"副部级","note":"原在青海省任职多年"},

    # ── 任维 ──
    {"id":25,"person_id":5,"org_id":2,"title":"西藏自治区常务副主席","start":"2021-12","end":"","rank":"副部级","note":""},
    {"id":26,"person_id":5,"org_id":1,"title":"西藏自治区党委常委","start":"2021-11","end":"","rank":"副部级","note":""},
    {"id":27,"person_id":5,"org_id":2,"title":"西藏自治区政府副主席","start":"2020-04","end":"2021-12","rank":"副部级","note":""},
    {"id":28,"person_id":5,"org_id":23,"title":"中国大唐集团副总经理","start":"2018-08","end":"2020-04","rank":"副部级","note":""},
    {"id":29,"person_id":5,"org_id":22,"title":"中国国电集团西藏分公司党组书记、总经理","start":"2016-05","end":"2018-08","rank":"正厅级","note":""},

    # ── 罗布顿珠 ──
    {"id":30,"person_id":6,"org_id":2,"title":"西藏自治区常务副主席","start":"2016-12","end":"","rank":"副部级","note":""},
    {"id":31,"person_id":6,"org_id":25,"title":"昌都市委书记","start":"2011-11","end":"2017-04","rank":"正厅级","note":""},
    {"id":32,"person_id":6,"org_id":6,"title":"西藏自治区高级人民法院院长","start":"2007-01","end":"2013-01","rank":"副部级","note":""},
    {"id":33,"person_id":6,"org_id":27,"title":"拉萨市市长","start":"2002-12","end":"2006-09","rank":"正厅级","note":""},

    # ── 赖蛟 ──
    {"id":34,"person_id":9,"org_id":7,"title":"西藏自治区党委组织部部长","start":"2021-11","end":"","rank":"副部级","note":""},
    {"id":35,"person_id":9,"org_id":1,"title":"西藏自治区党委常委","start":"2021-11","end":"","rank":"副部级","note":""},
    {"id":36,"person_id":9,"org_id":29,"title":"重庆市忠县县委书记","start":"2019","end":"2021-11","rank":"正厅级","note":""},

    # ── 刘江 ──
    {"id":37,"person_id":7,"org_id":10,"title":"西藏自治区党委政法委书记","start":"2023-10","end":"","rank":"副部级","note":"同时担任党委副书记"},
    {"id":38,"person_id":7,"org_id":1,"title":"西藏自治区党委常委","start":"2018-06","end":"","rank":"副部级","note":""},

    # ── 王卫东 ──
    {"id":39,"person_id":8,"org_id":5,"title":"西藏自治区纪委书记、监委主任","start":"2019-07","end":"","rank":"副部级","note":"2019.07代理，2020.01当选"},

    # ── 陈永奇 ──
    {"id":40,"person_id":4,"org_id":1,"title":"西藏自治区党委副书记","start":"2023","end":"","rank":"副部级","note":""},
    {"id":41,"person_id":4,"org_id":7,"title":"西藏自治区党委组织部部长","start":"2018","end":"2023","rank":"副部级","note":"调任党委副书记"},
    {"id":42,"person_id":4,"org_id":1,"title":"西藏自治区党委常委","start":"2018","end":"","rank":"副部级","note":""},

    # ── Predecessors — 党委书记 ──
    {"id":43,"person_id":17,"org_id":1,"title":"西藏自治区党委书记","start":"2016-08","end":"2021-10","rank":"正部级","note":"2024年被查，2025年被判死缓"},
    {"id":44,"person_id":18,"org_id":1,"title":"西藏自治区党委书记","start":"2011-08","end":"2016-08","rank":"正部级","note":"后调任新疆维吾尔自治区党委书记"},
    {"id":45,"person_id":19,"org_id":1,"title":"西藏自治区党委书记","start":"2006-05","end":"2011-08","rank":"正部级","note":"后调任河北省委书记，后任全国政协副主席"},
    {"id":46,"person_id":20,"org_id":1,"title":"西藏自治区党委书记","start":"2004-12","end":"2006-05","rank":"正部级","note":"后任交通部部长，后任全国政协副主席"},
    {"id":47,"person_id":21,"org_id":1,"title":"西藏自治区党委书记","start":"2000-10","end":"2004-12","rank":"正部级","note":"后任北京市委书记，中央政治局委员"},
    {"id":48,"person_id":22,"org_id":1,"title":"西藏自治区党委书记","start":"1992-12","end":"2000-10","rank":"正部级","note":"后任中国社会科学院院长，全国政协副主席"},
    {"id":49,"person_id":23,"org_id":1,"title":"西藏自治区党委书记","start":"1988-12","end":"1992-12","rank":"副部级","note":"后任中共中央总书记、国家主席"},

    # ── Predecessors — 政府前主席 ──
    {"id":50,"person_id":24,"org_id":2,"title":"西藏自治区政府主席","start":"2017-01","end":"2021-10","rank":"正部级","note":"2025年被查，2026年6月判无期徒刑"},
    {"id":51,"person_id":25,"org_id":2,"title":"西藏自治区政府主席","start":"2013-01","end":"2017-01","rank":"正部级","note":"后任全国人大常委会副委员长"},
    {"id":52,"person_id":26,"org_id":2,"title":"西藏自治区政府主席","start":"2010-01","end":"2013-01","rank":"正部级","note":"后任全国人大常委会副委员长"},
    {"id":53,"person_id":27,"org_id":2,"title":"西藏自治区政府主席","start":"2003-03","end":"2010-01","rank":"正部级","note":"后任全国人大常委会副委员长"},
    {"id":54,"person_id":28,"org_id":2,"title":"西藏自治区政府主席","start":"1993-01","end":"2003-03","rank":"正部级","note":"后任全国人大常委会副委员长"},
    {"id":55,"person_id":29,"org_id":2,"title":"西藏自治区政府主席","start":"1990-01","end":"1993-01","rank":"正部级","note":"后任全国人大常委会副委员长"},

    # ── Standing Committee members (basic office record) ──
    {"id":56,"person_id":10,"org_id":1,"title":"西藏自治区党委常委","start":"","end":"","rank":"副部级","note":""},
    {"id":57,"person_id":11,"org_id":1,"title":"西藏自治区党委常委","start":"","end":"","rank":"副部级","note":""},
    {"id":58,"person_id":12,"org_id":1,"title":"西藏自治区党委常委","start":"","end":"","rank":"副部级","note":""},
    {"id":59,"person_id":13,"org_id":1,"title":"西藏自治区党委常委","start":"","end":"","rank":"副部级","note":""},
    {"id":60,"person_id":14,"org_id":1,"title":"西藏自治区党委常委","start":"","end":"","rank":"副部级","note":""},
    {"id":61,"person_id":15,"org_id":1,"title":"西藏自治区党委常委","start":"","end":"","rank":"副部级","note":""},
    {"id":62,"person_id":16,"org_id":1,"title":"西藏自治区党委常委","start":"","end":"","rank":"副部级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王君正 ↔ 嘎玛泽登 (current top duo)
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate","context":"王君正任西藏自治区党委书记，嘎玛泽登任政府主席，党政主要领导搭档","overlap_org":"中共西藏自治区委员会","overlap_period":"2024.10至今","strength":"strong","confidence":"confirmed"},
    # 王君正 ↔ 严金海 (former top duo)
    {"id":2,"person_a":1,"person_b":3,"type":"superior_subordinate","context":"王君正任党委书记，严金海任政府主席（2021.10-2024.11），党政搭档","overlap_org":"中共西藏自治区委员会","overlap_period":"2021.10-2024.11","strength":"strong","confidence":"confirmed"},
    # 严金海 ↔ 嘎玛泽登 (predecessor-successor, 政府主席)
    {"id":3,"person_a":3,"person_b":2,"type":"predecessor_successor","context":"严金海2021.10-2024.11任西藏自治区政府主席，嘎嘎泽登2024.11接任","overlap_org":"西藏自治区人民政府","overlap_period":"2021-2024","strength":"strong","confidence":"confirmed"},
    # 吴英杰 ↔ 王君正 (predecessor-successor, 党委书记)
    {"id":4,"person_a":17,"person_b":1,"type":"predecessor_successor","context":"吴英杰2016-2021.10任党委书记，王君正2021.10接任","overlap_org":"中共西藏自治区委员会","overlap_period":"2021","strength":"strong","confidence":"confirmed"},
    # 陈全国 ↔ 吴英杰 (predecessor-successor, 党委书记)
    {"id":5,"person_a":18,"person_b":17,"type":"predecessor_successor","context":"陈全国2011-2016.08任党委书记，吴英杰2016.08接任","overlap_org":"中共西藏自治区委员会","overlap_period":"2011-2016","strength":"strong","confidence":"confirmed"},
    # 王君正 ↔ 齐扎拉 (brief overlap)
    {"id":6,"person_a":1,"person_b":24,"type":"overlap","context":"王君正2021.10到任时，齐扎拉尚未卸任政府主席（至月底）","overlap_org":"中共西藏自治区委员会","overlap_period":"2021.10","strength":"medium","confidence":"confirmed"},
    # 齐扎拉 ↔ 严金海 (predecessor-successor, 政府主席)
    {"id":7,"person_a":24,"person_b":3,"type":"predecessor_successor","context":"齐扎拉2017-2021.10任政府主席，严金海2021.10接任","overlap_org":"西藏自治区人民政府","overlap_period":"2017-2021","strength":"strong","confidence":"confirmed"},
    # 齐扎拉 ↔ 洛桑江村 (predecessor-successor, 政府主席)
    {"id":8,"person_a":25,"person_b":24,"type":"predecessor_successor","context":"洛桑江村2013-2017任政府主席，齐扎拉2017接任","overlap_org":"西藏自治区人民政府","overlap_period":"2013-2017","strength":"strong","confidence":"confirmed"},
    # 王君正 ↔ 陈永奇 (current superior-subordinate)
    {"id":9,"person_a":1,"person_b":4,"type":"superior_subordinate","context":"王君正任党委书记，陈永奇任党委副书记","overlap_org":"中共西藏自治区委员会","overlap_period":"2023至今","strength":"strong","confidence":"confirmed"},
    # 王君正 ↔ 任维 (superior-subordinate)
    {"id":10,"person_a":1,"person_b":5,"type":"superior_subordinate","context":"王君正任党委书记，任维任常委、常务副主席","overlap_org":"中共西藏自治区委员会","overlap_period":"2021.11至今","strength":"strong","confidence":"confirmed"},
    # 王君正 ↔ 刘江 (superior-subordinate)
    {"id":11,"person_a":1,"person_b":7,"type":"superior_subordinate","context":"王君正任党委书记，刘江任党委副书记、政法委书记","overlap_org":"中共西藏自治区委员会","overlap_period":"2023至今","strength":"strong","confidence":"confirmed"},
    # 嘎玛泽登 ↔ 任维 (same government leadership team)
    {"id":12,"person_a":2,"person_b":5,"type":"overlap","context":"嘎嘎泽登任政府主席，任维任常务副主席","overlap_org":"西藏自治区人民政府","overlap_period":"2024至今","strength":"strong","confidence":"confirmed"},
    # 嘎玛 ↔ 罗布顿珠 (same government team)
    {"id":13,"person_a":2,"person_b":6,"type":"overlap","context":"嘎嘎泽登任政府主席，罗布顿珠任常务副主席","overlap_org":"西藏自治区人民政府","overlap_period":"2024至今","strength":"strong","confidence":"confirmed"},
    # 王君正 ↔ 赖蛟 (superior-subordinate)
    {"id":14,"person_a":1,"person_b":9,"type":"superior_subordinate","context":"王君正任党委书记，赖蛟任常委、组织部部长","overlap_org":"中共西藏自治区委员会","overlap_period":"2021.11至今","strength":"strong","confidence":"confirmed"},
]

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    name = p["name"]
    current = p.get("current_post","")
    is_party_sec = "书记" in current and "副" not in current.split("书记")[0]
    is_gov_head = ("省长" in current or "主席" in current) and "副" not in current
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
    return colors.get(org_type,"200,200,200")

def is_top_leader(p):
    current = p.get("current_post","")
    return ("书记" in current and "副" not in current.split("书记")[0]) or \
           (("省长" in current or "主席" in current) and "副" not in current)

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

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>西藏自治区领导关系网络 - Tibet Autonomous Region Leadership Network</description>')
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
        cc = org_color(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cc.split(",")[0]}" g="{cc.split(",")[1]}" b="{cc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
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