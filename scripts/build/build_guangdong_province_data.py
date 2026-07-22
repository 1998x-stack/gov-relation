#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Guangdong Province (广东省) leadership network.

Covers: Provincial Party Secretary (省委书记), Governor (省长), predecessors,
succession chains, key deputy leaders (省委常委会成员, 副省长等),
and the provincial-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/guangdong_province_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/guangdong_province_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 黄坤明 — 广东省委书记 (as of 2022.10)
    {"id":1,"name":"黄坤明","gender":"男","ethnicity":"汉族","birth":"1956-11","birthplace":"福建上杭","education":"福建师范大学中文系学士、清华大学马克思主义理论与思想政治教育博士","party_join":"1976-10","work_start":"1974-12","current_post":"中央政治局委员、广东省委书记","current_org":"中共广东省委员会","source":"https://zh.wikipedia.org/wiki/%E9%BB%84%E5%9D%A4%E6%98%8E"},
    # 孟凡利 — 广东省省长
    {"id":2,"name":"孟凡利","gender":"男","ethnicity":"汉族","birth":"1965-09","birthplace":"山东临沂","education":"山东经济学院会计系学士、南开大学会计系硕士、天津财经大学会计学博士","party_join":"1986-03","work_start":"1986-07","current_post":"广东省委副书记、省长","current_org":"广东省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%AD%9F%E5%87%A1%E5%88%A9"},

    # ── Provincial leadership (省委常委会成员) ──
    {"id":3,"name":"马森述","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省委常委、省纪委书记","current_org":"中共广东省纪律检查委员会","source":"https://zh.wikipedia.org/wiki/%E9%A9%AC%E6%A3%AE%E8%BF%B0"},
    {"id":4,"name":"冯忠华","gender":"男","ethnicity":"汉族","birth":"1970-05","birthplace":"辽宁丹东","education":"合肥工业大学资源与环境工程系学士、清华大学建筑学院工程硕士","party_join":"1992-07","work_start":"1993-07","current_post":"广东省委常委、广州市委书记","current_org":"中共广州市委员会","source":"https://zh.wikipedia.org/wiki/%E5%86%AF%E5%BF%A0%E5%8D%8E"},
    {"id":5,"name":"张虎","gender":"男","ethnicity":"汉族","birth":"1967-01","birthplace":"","education":"研究生学历","party_join":"","work_start":"","current_post":"广东省委常委、常务副省长","current_org":"广东省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E8%99%8E_(1967%E5%B9%B4)"},
    {"id":6,"name":"王曦","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省委常委、统战部部长","current_org":"中共广东省委统战部","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E6%9B%A6"},
    {"id":7,"name":"靳磊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省委常委、深圳市委书记","current_org":"中共深圳市委员会","source":"https://zh.wikipedia.org/wiki/%E9%9D%B3%E7%A3%8A"},
    {"id":8,"name":"张国智","gender":"女","ethnicity":"汉族","birth":"1973-06","birthplace":"","education":"研究生学历","party_join":"","work_start":"","current_post":"广东省委常委、副省长","current_org":"广东省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%9B%BD%E6%99%BA"},
    {"id":9,"name":"胡劲军","gender":"男","ethnicity":"汉族","birth":"1967-11","birthplace":"浙江宁波","education":"复旦大学新闻学院","party_join":"1987-01","work_start":"1990-07","current_post":"广东省委常委、宣传部部长","current_org":"中共广东省委宣传部","source":"https://zh.wikipedia.org/wiki/%E8%83%A1%E5%8A%B2%E5%86%9B"},
    {"id":10,"name":"张弓","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省委常委、省军区司令员","current_org":"广东省军区","source":"https://www.gd.gov.cn"},
    {"id":11,"name":"胡帆","gender":"男","ethnicity":"汉族","birth":"1971-09","birthplace":"","education":"在职研究生学历、会计学硕士","party_join":"","work_start":"","current_post":"广东省委常委、组织部部长","current_org":"中共广东省委组织部","source":"https://zh.wikipedia.org/wiki/%E8%83%A1%E5%B8%86"},

    # ── Vice governors (副省长，非常委) ──
    {"id":12,"name":"刘国周","gender":"男","ethnicity":"汉族","birth":"1971-12","birthplace":"河北任县","education":"中国人民大学管理学硕士","party_join":"1993-04","work_start":"1995-07","current_post":"广东省副省长、省公安厅厅长","current_org":"广东省公安厅","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E5%9B%BD%E5%91%A8"},
    {"id":13,"name":"王胜","gender":"男","ethnicity":"汉族","birth":"1968-03","birthplace":"","education":"研究生学历","party_join":"","work_start":"","current_post":"广东省副省长","current_org":"广东省人民政府","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E8%83%9C_(1968%E5%B9%B4)"},
    {"id":14,"name":"李运","gender":"男","ethnicity":"汉族","birth":"1973-09","birthplace":"","education":"研究生学历","party_join":"","work_start":"","current_post":"广东省副省长","current_org":"广东省人民政府","source":"https://baike.baidu.com/item/%E6%9D%8E%E8%BF%90"},
    {"id":15,"name":"唐屹峰","gender":"男","ethnicity":"汉族","birth":"1973-01","birthplace":"","education":"大学学历","party_join":"","work_start":"","current_post":"广东省副省长、佛山市委书记","current_org":"广东省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%94%90%E5%B1%B9%E5%B3%B0"},

    # ── Predecessors — 省委书记 ──
    {"id":16,"name":"李希","gender":"男","ethnicity":"汉族","birth":"1956-10","birthplace":"","education":"","party_join":"","work_start":"","current_post":"中央政治局常委、中央纪委书记（原广东省委书记）","current_org":"中央纪委","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E5%B8%8C_(1956%E5%B9%B4)"},
    {"id":17,"name":"胡春华","gender":"男","ethnicity":"汉族","birth":"1963-04","birthplace":"","education":"","party_join":"","work_start":"","current_post":"全国政协副主席（原广东省委书记）","current_org":"全国政协","source":"https://zh.wikipedia.org/wiki/%E8%83%A1%E6%98%A5%E5%8D%8E"},
    {"id":18,"name":"王伟中","gender":"男","ethnicity":"汉族","birth":"1962-03","birthplace":"","education":"","party_join":"","work_start":"","current_post":"内蒙古自治区党委书记（原广东省省长）","current_org":"中共内蒙古自治区委员会","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E4%BC%9F%E4%B8%AD"},

    # ── Predecessors — 省长 ──
    {"id":19,"name":"马兴瑞","gender":"男","ethnicity":"汉族","birth":"1959-10","birthplace":"","education":"哈尔滨工业大学博士","party_join":"","work_start":"","current_post":"被开除党籍（原新疆党委书记、广东原省长）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E9%A9%AC%E5%85%B4%E7%91%9E"},

    # ── Other key provincial leaders ──
    {"id":20,"name":"陈良贤","gender":"男","ethnicity":"汉族","birth":"1963","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省政府党组成员","current_org":"广东省人民政府","source":"https://zh.wikipedia.org/wiki/%E9%99%88%E8%89%AF%E8%B4%A4"},
    {"id":21,"name":"陈敏","gender":"男","ethnicity":"","birth":"1965","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省政府秘书长","current_org":"广东省人民政府","source":"https://zh.wikipedia.org/wiki/%E9%99%88%E6%95%8F_(1965%E5%B9%B4)"},
    {"id":22,"name":"黄楚平","gender":"男","ethnicity":"汉族","birth":"1961","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省人大常委会主任","current_org":"广东省人大常委会","source":"https://zh.wikipedia.org/wiki/%E9%BB%84%E6%A5%9A%E5%B9%B3"},
    {"id":23,"name":"林克庆","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广东省政协主席","current_org":"政协广东省委员会","source":"https://zh.wikipedia.org/wiki/%E6%9E%97%E5%85%8B%E5%BA%86"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Guangdong provincial core
    {"id":1,"name":"中共广东省委员会","type":"党委","level":"省级","parent":"","location":"广东省广州市"},
    {"id":2,"name":"广东省人民政府","type":"政府","level":"省级","parent":"","location":"广东省广州市"},
    {"id":3,"name":"广东省人大常委会","type":"人大","level":"省级","parent":"","location":"广东省广州市"},
    {"id":4,"name":"政协广东省委员会","type":"政协","level":"省级","parent":"","location":"广东省广州市"},
    {"id":5,"name":"中共广东省纪律检查委员会","type":"党委","level":"省级","parent":"中共广东省委员会","location":"广东省广州市"},

    # Key provincial departments
    {"id":6,"name":"中共广东省委组织部","type":"党委","level":"省级","parent":"中共广东省委员会","location":"广东省广州市"},
    {"id":7,"name":"中共广东省委宣传部","type":"党委","level":"省级","parent":"中共广东省委员会","location":"广东省广州市"},
    {"id":8,"name":"中共广东省委统战部","type":"党委","level":"省级","parent":"中共广东省委员会","location":"广东省广州市"},
    {"id":9,"name":"中共广东省委政法委","type":"党委","level":"省级","parent":"中共广东省委员会","location":"广东省广州市"},
    {"id":10,"name":"广东省公安厅","type":"政府","level":"省级","parent":"广东省人民政府","location":"广东省广州市"},
    {"id":11,"name":"广东省军区","type":"党委","level":"省级","parent":"中央军委","location":"广东省广州市"},

    # Key cities (副省级/地级)
    {"id":12,"name":"中共广州市委员会","type":"党委","level":"副省级","parent":"中共广东省委员会","location":"广东省广州市"},
    {"id":13,"name":"中共深圳市委员会","type":"党委","level":"副省级","parent":"中共广东省委员会","location":"广东省深圳市"},
    {"id":14,"name":"中共佛山市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省佛山市"},
    {"id":15,"name":"中共揭阳市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省揭阳市"},
    {"id":16,"name":"中共云浮市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省云浮市"},

    # Central / national orgs
    {"id":17,"name":"中央纪委","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":18,"name":"全国政协","type":"政协","level":"国家级","parent":"","location":"北京市"},
    {"id":19,"name":"国务院","type":"政府","level":"国家级","parent":"","location":"北京市"},
    {"id":20,"name":"中共中央宣传部","type":"党委","level":"国家级","parent":"中央政治局","location":"北京市"},
    {"id":21,"name":"中共中央办公厅","type":"党委","level":"国家级","parent":"中央政治局","location":"北京市"},
    {"id":22,"name":"中共内蒙古自治区委员会","type":"党委","level":"省级","parent":"","location":"内蒙古自治区呼和浩特市"},
    {"id":23,"name":"全国人大常委会","type":"人大","level":"国家级","parent":"","location":"北京市"},
    {"id":24,"name":"中央政治局","type":"党委","level":"国家级","parent":"","location":"北京市"},

    # 黄坤明 earlier work units — 福建 → 浙江 → 中央 → 广东
    {"id":25,"name":"福建省龙岩地区系统","type":"政府","level":"","parent":"福建省人民政府","location":"福建省龙岩市"},
    {"id":26,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
    {"id":27,"name":"中共厦门市委员会","type":"党委","level":"副省级","parent":"中共福建省委员会","location":"福建省厦门市"},
    {"id":28,"name":"中共浙江省委员会","type":"党委","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":29,"name":"中共湖州市委员会","type":"党委","level":"地级","parent":"中共浙江省委员会","location":"浙江省湖州市"},
    {"id":30,"name":"中共嘉兴市委员会","type":"党委","level":"地级","parent":"中共浙江省委员会","location":"浙江省嘉兴市"},

    # 孟凡利 earlier — 山东 → 内蒙古 → 深圳 → 广东
    {"id":31,"name":"山东省会计系统","type":"政府","level":"省级","parent":"山东省人民政府","location":"山东省济南市"},
    {"id":32,"name":"山东省商业集团","type":"事业单位","level":"","parent":"山东省人民政府","location":"山东省济南市"},
    {"id":33,"name":"山东省鲁信投资控股集团","type":"事业单位","level":"","parent":"山东省人民政府","location":"山东省济南市"},
    {"id":34,"name":"山东省商务厅","type":"政府","level":"省级","parent":"山东省人民政府","location":"山东省济南市"},
    {"id":35,"name":"山东省烟台市系统","type":"政府","level":"地级","parent":"山东省人民政府","location":"山东省烟台市"},
    {"id":36,"name":"中共山东省委员会","type":"党委","level":"省级","parent":"","location":"山东省济南市"},
    {"id":37,"name":"中共烟台市委员会","type":"党委","level":"地级","parent":"中共山东省委员会","location":"山东省烟台市"},
    {"id":38,"name":"中共青岛市委员会","type":"党委","level":"副省级","parent":"中共山东省委员会","location":"山东省青岛市"},
    {"id":39,"name":"中共内蒙古自治区委员会","type":"党委","level":"省级","parent":"","location":"内蒙古自治区呼和浩特市"},
    {"id":40,"name":"内蒙古自治区人民政府","type":"政府","level":"省级","parent":"","location":"内蒙古自治区呼和浩特市"},

    # 冯忠华 earlier — 建设部/住建部 → 海南 → 广东
    {"id":41,"name":"建设部/住房和城乡建设部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":42,"name":"全国人大常委会办公厅","type":"人大","level":"国家级","parent":"全国人大常委会","location":"北京市"},
    {"id":43,"name":"中共海南省委员会","type":"党委","level":"省级","parent":"","location":"海南省海口市"},
    {"id":44,"name":"海南省人民政府","type":"政府","level":"省级","parent":"","location":"海南省海口市"},
    {"id":45,"name":"三亚市系统","type":"政府","level":"地级","parent":"海南省人民政府","location":"海南省三亚市"},

    # 张虎 earlier — 广州 → 深圳 → 省府
    {"id":46,"name":"广州市水利系统","type":"政府","level":"副省级","parent":"广州市人民政府","location":"广东省广州市"},
    {"id":47,"name":"广州市政府办公厅","type":"政府","level":"","parent":"广州市人民政府","location":"广东省广州市"},

    # 刘国周 earlier — 北京公安 → 广东
    {"id":48,"name":"北京市公安系统","type":"政府","level":"","parent":"北京市人民政府","location":"北京市"},
    {"id":49,"name":"深圳市公安系统","type":"政府","level":"副省级","parent":"深圳市人民政府","location":"广东省深圳市"},

    # 张国智 earlier — 重庆 → 广东
    {"id":50,"name":"重庆市系统","type":"政府","level":"省级","parent":"","location":"重庆市"},
    {"id":51,"name":"中共重庆市委员会","type":"党委","level":"省级","parent":"","location":"重庆市"},
    {"id":52,"name":"重庆市大渡口区系统","type":"政府","level":"","parent":"重庆市人民政府","location":"重庆市大渡口区"},
    {"id":53,"name":"重庆市发改委","type":"政府","level":"省级","parent":"重庆市人民政府","location":"重庆市"},

    # 唐屹峰 earlier — 电网系统
    {"id":54,"name":"中国南方电网有限责任公司","type":"事业单位","level":"国家级","parent":"","location":"广东省广州市"},
    {"id":55,"name":"中国南方电网广东电网公司","type":"事业单位","level":"","parent":"中国南方电网有限责任公司","location":"广东省广州市"},

    # 胡劲军 earlier — 上海宣传系统
    {"id":56,"name":"上海市宣传系统","type":"政府","level":"省级","parent":"中共上海市委员会","location":"上海市"},
    {"id":57,"name":"中共上海市委宣传部","type":"党委","level":"省级","parent":"中共上海市委员会","location":"上海市"},
    {"id":58,"name":"上海市人民政府","type":"政府","level":"省级","parent":"","location":"上海市"},

    # 胡帆 earlier — 财政部
    {"id":59,"name":"中华人民共和国财政部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":60,"name":"财政部广西监管局","type":"政府","level":"","parent":"中华人民共和国财政部","location":"广西壮族自治区南宁市"},

    # 李希 earlier — 甘肃 → 陕西 → 上海 → 辽宁 → 广东
    {"id":61,"name":"中共甘肃省委员会","type":"党委","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":62,"name":"中共陕西省委员会","type":"党委","level":"省级","parent":"","location":"陕西省西安市"},
    {"id":63,"name":"中共上海市委员会","type":"党委","level":"省级","parent":"","location":"上海市"},
    {"id":64,"name":"中共辽宁省委员会","type":"党委","level":"省级","parent":"","location":"辽宁省沈阳市"},

    # 胡春华 earlier — 西藏 → 河北 → 广东
    {"id":65,"name":"中共西藏自治区委员会","type":"党委","level":"省级","parent":"","location":"西藏自治区拉萨市"},
    {"id":66,"name":"中共河北省委员会","type":"党委","level":"省级","parent":"","location":"河北省石家庄市"},
    {"id":67,"name":"共青团中央","type":"党委","level":"国家级","parent":"","location":"北京市"},

    # 王伟中 earlier — 科技部 → 山西 → 深圳 → 广东
    {"id":68,"name":"国家科学技术部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":69,"name":"中共山西省委员会","type":"党委","level":"省级","parent":"","location":"山西省太原市"},

    # 马兴瑞 earlier — 哈工大 → 航天 → 工信部 → 广东
    {"id":70,"name":"哈尔滨工业大学","type":"事业单位","level":"国家级","parent":"","location":"黑龙江省哈尔滨市"},
    {"id":71,"name":"中国航天科技集团公司","type":"事业单位","level":"国家级","parent":"","location":"北京市"},
    {"id":72,"name":"国家航天局","type":"政府","level":"国家级","parent":"中华人民共和国工业和信息化部","location":"北京市"},
    {"id":73,"name":"中华人民共和国工业和信息化部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":74,"name":"新疆维吾尔自治区党委","type":"党委","level":"省级","parent":"","location":"新疆维吾尔自治区乌鲁木齐市"},

    # 王曦 earlier — 上海 → 广东
    {"id":75,"name":"上海市浦东新区系统","type":"政府","level":"","parent":"上海市人民政府","location":"上海市浦东新区"},

    # 靳磊 earlier — 河南 → 四川 → 广东
    {"id":76,"name":"中共河南省委员会","type":"党委","level":"省级","parent":"","location":"河南省郑州市"},
    {"id":77,"name":"中共四川省委员会","type":"党委","level":"省级","parent":"","location":"四川省成都市"},
    {"id":78,"name":"中共安阳市委员会","type":"党委","level":"地级","parent":"中共河南省委员会","location":"河南省安阳市"},

    # 林克庆 earlier — 北京
    {"id":79,"name":"中共北京市委员会","type":"党委","level":"省级","parent":"","location":"北京市"},
    {"id":80,"name":"北京市政府办公厅","type":"政府","level":"","parent":"北京市人民政府","location":"北京市"},

    # 黄楚平 earlier — 湖北
    {"id":81,"name":"中共湖北省委员会","type":"党委","level":"省级","parent":"","location":"湖北省武汉市"},
    {"id":82,"name":"湖北省人民政府","type":"政府","level":"省级","parent":"","location":"湖北省武汉市"},
    {"id":83,"name":"湖北省政协","type":"政协","level":"省级","parent":"","location":"湖北省武汉市"},
    {"id":84,"name":"中共咸宁市委员会","type":"党委","level":"地级","parent":"中共湖北省委员会","location":"湖北省咸宁市"},
    {"id":85,"name":"中共宜昌市委员会","type":"党委","level":"地级","parent":"中共湖北省委员会","location":"湖北省宜昌市"},

    # 陈敏 earlier
    {"id":86,"name":"中共梅州市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省梅州市"},
    {"id":87,"name":"广东省人力资源和社会保障厅","type":"政府","level":"省级","parent":"广东省人民政府","location":"广东省广州市"},

    # 陈敏 earlier (江西省)
    {"id":88,"name":"萍乡市系统","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省萍乡市"},
    {"id":89,"name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":90,"name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":91,"name":"中共吉安市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省吉安市"},
    {"id":92,"name":"江西省财政厅","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},

    # 马森述 earlier — 国务院法制办 → 中央纪委
    {"id":93,"name":"国务院法制办公室","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},

    # 王胜 earlier — 揭阳
    {"id":94,"name":"中共惠州市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省惠州市"},

    # 李运 — 农村发展银行/农业银行
    {"id":95,"name":"中国农业银行","type":"事业单位","level":"国家级","parent":"","location":"北京市"},

    # 陈良贤 — 汕头
    {"id":96,"name":"中共汕头市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省汕头市"},
    {"id":97,"name":"中山市系统","type":"政府","level":"地级","parent":"广东省人民政府","location":"广东省中山市"},
    {"id":98,"name":"广东省广晟资产经营有限公司","type":"事业单位","level":"","parent":"广东省人民政府","location":"广东省广州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 黄坤明 ──
    {"id":1,"person_id":1,"org_id":1,"title":"广东省委书记","start":"2022-10","end":"","rank":"正部级","note":"2022.10从中央宣传部调任广东省委书记；2022.10二十大当选中央政治局委员"},
    {"id":2,"person_id":1,"org_id":20,"title":"中央宣传部部长","start":"2014-12","end":"2022-10","rank":"副国级","note":"2014.12任中央宣传部副部长；后任部长约8年"},
    {"id":3,"person_id":1,"org_id":28,"title":"浙江省委常委、宣传部部长","start":"2010-07","end":"2014-12","rank":"副部级","note":"兼杭州市委副书记等职"},
    {"id":4,"person_id":1,"org_id":30,"title":"嘉兴市委书记","start":"2005-09","end":"2010-01","rank":"正厅级","note":""},
    {"id":5,"person_id":1,"org_id":29,"title":"湖州市委书记","start":"2003-05","end":"2005-09","rank":"正厅级","note":""},
    {"id":6,"person_id":1,"org_id":29,"title":"湖州市委副书记、市长","start":"2001-11","end":"2003-05","rank":"正厅级","note":""},
    {"id":7,"person_id":1,"org_id":29,"title":"湖州市委副书记","start":"1999-10","end":"2001-11","rank":"副厅级","note":""},
    {"id":8,"person_id":1,"org_id":27,"title":"厦门市委常委、宣传部部长","start":"1997-03","end":"1999-10","rank":"正厅级","note":"在厦门系统任职多年"},
    {"id":9,"person_id":1,"org_id":27,"title":"厦门市思明区委书记","start":"1994-04","end":"1997-03","rank":"副厅级","note":""},
    {"id":10,"person_id":1,"org_id":26,"title":"福建省委办公厅处长","start":"~1993","end":"1994-04","rank":"正处级","note":""},
    {"id":11,"person_id":1,"org_id":25,"title":"福建省龙岩地区系统工作","start":"1982","end":"~1993","rank":"","note":"1982年福建师大毕业，在龙岩地区任职约11年"},
    {"id":12,"person_id":1,"org_id":25,"title":"福建省龙岩地区行署办公室副科长、科长","start":"~1985","end":"~1993","rank":"","note":""},

    # ── 孟凡利 ──
    {"id":13,"person_id":2,"org_id":2,"title":"广东省委副书记、省长","start":"2025-02","end":"","rank":"正部级","note":"2025.02从深圳市委书记调任广东省代省长，后当选省长"},
    {"id":14,"person_id":2,"org_id":13,"title":"深圳市委书记","start":"2022-04","end":"2025-02","rank":"副部级","note":"2022.04任广东省委副书记、深圳市委书记"},
    {"id":15,"person_id":2,"org_id":1,"title":"广东省委副书记","start":"2022-04","end":"2025-02","rank":"副部级","note":"从内蒙古调任广东省委副书记"},
    {"id":16,"person_id":2,"org_id":40,"title":"内蒙古自治区党委常委、包头市委书记","start":"2021-01","end":"2022-04","rank":"副部级","note":""},
    {"id":17,"person_id":2,"org_id":39,"title":"内蒙古自治区党委常委","start":"2020-06","end":"2021-01","rank":"副部级","note":""},
    {"id":18,"person_id":2,"org_id":39,"title":"内蒙古自治区党委组织部部长","start":"2020-06","end":"2021-01","rank":"副部级","note":""},
    {"id":19,"person_id":2,"org_id":36,"title":"山东省副省长","start":"2017-06","end":"2020-06","rank":"副部级","note":"此前任烟台市委书记"},
    {"id":20,"person_id":2,"org_id":37,"title":"烟台市委书记","start":"2015-07","end":"2017-06","rank":"正厅级","note":""},
    {"id":21,"person_id":2,"org_id":37,"title":"烟台市委副书记、市长","start":"2013-08","end":"2015-07","rank":"正厅级","note":""},
    {"id":22,"person_id":2,"org_id":38,"title":"青岛市委常委、副市长","start":"2005-08","end":"2013-08","rank":"副厅级→正厅级","note":""},
    {"id":23,"person_id":2,"org_id":34,"title":"山东省商务厅厅长","start":"2005-04","end":"2005-08","rank":"正厅级","note":"原山东省外经贸厅改制"},
    {"id":24,"person_id":2,"org_id":34,"title":"山东省外经贸厅副厅长","start":"2002-01","end":"2005-04","rank":"副厅级","note":""},
    {"id":25,"person_id":2,"org_id":33,"title":"山东省鲁信投资控股集团副董事长、总经理","start":"2001-12","end":"2002-01","rank":"","note":"短暂任职"},
    {"id":26,"person_id":2,"org_id":32,"title":"山东省商业集团总经理","start":"2000-09","end":"2001-12","rank":"","note":""},
    {"id":27,"person_id":2,"org_id":31,"title":"山东省会计系统工作","start":"1986-07","end":"2000-09","rank":"","note":"1986年山东经济学院毕业，在山东省财政厅会计系统工作约14年，从科员升至副局长级"},

    # ── 马森述 ──
    {"id":28,"person_id":3,"org_id":5,"title":"广东省委常委、省纪委书记","start":"2021-11","end":"","rank":"副部级","note":"从中央纪委调任广东省纪委书记"},
    {"id":29,"person_id":3,"org_id":17,"title":"中央纪委国家监委副部级巡视专员","start":"~2018","end":"2021-11","rank":"副部级","note":""},
    {"id":30,"person_id":3,"org_id":93,"title":"国务院法制办工作","start":"~1995","end":"~2015","rank":"","note":"长期在国务院法制办工作，后转为中央纪委"},
    {"id":31,"person_id":3,"org_id":17,"title":"中央纪委、中央组织部工作","start":"~2015","end":"2021-11","rank":"","note":""},

    # ── 冯忠华 ──
    {"id":32,"person_id":4,"org_id":12,"title":"广东省委常委、广州市委书记","start":"2025-03","end":"","rank":"副部级","note":"2025.03任广东省委常委、广州市委书记"},
    {"id":33,"person_id":4,"org_id":1,"title":"广东省委常委、省委组织部部长","start":"2024-04","end":"2025-03","rank":"副部级","note":"2024.04任广东省委常委、组织部部长"},
    {"id":34,"person_id":4,"org_id":44,"title":"海南省副省长","start":"2019-06","end":"2024-04","rank":"副部级","note":""},
    {"id":35,"person_id":4,"org_id":42,"title":"全国人大常委会办公厅工作","start":"~2014","end":"2019-06","rank":"正厅级","note":"在全国人大办公厅任职"},
    {"id":36,"person_id":4,"org_id":41,"title":"住建部城乡规划司司长","start":"~2010","end":"~2014","rank":"正厅级","note":"长期在住建部（原建设部）工作"},
    {"id":37,"person_id":4,"org_id":41,"title":"建设部/住建部工作","start":"1993-07","end":"~2010","rank":"","note":"1993年合工大毕业进入建设部，从科员逐步晋升"},

    # ── 张虎 ──
    {"id":38,"person_id":5,"org_id":2,"title":"广东省委常委、常务副省长","start":"~2023","end":"","rank":"副部级","note":""},
    {"id":39,"person_id":5,"org_id":1,"title":"广东省委常委、省委政法委书记","start":"~2021","end":"~2023","rank":"副部级","note":""},
    {"id":40,"person_id":5,"org_id":2,"title":"广东省副省长","start":"~2019","end":"~2021","rank":"副部级","note":""},
    {"id":41,"person_id":5,"org_id":13,"title":"广州市委常委、副市长","start":"~2015","end":"~2019","rank":"正厅级","note":""},
    {"id":42,"person_id":5,"org_id":47,"title":"广州市政府办公厅主任","start":"~2011","end":"~2015","rank":"正局级","note":""},
    {"id":43,"person_id":5,"org_id":46,"title":"广州市水利局副局长","start":"~2002","end":"~2011","rank":"副局级","note":"从广州市水利系统逐步晋升"},

    # ── 王曦 ──
    {"id":44,"person_id":6,"org_id":8,"title":"广东省委常委、统战部部长","start":"~2023","end":"","rank":"副部级","note":""},

    # ── 靳磊 ──
    {"id":45,"person_id":7,"org_id":13,"title":"广东省委常委、深圳市委书记","start":"2025","end":"","rank":"副部级","note":"2025年初任深圳市委书记，此前任四川组织部长"},
    {"id":46,"person_id":7,"org_id":77,"title":"四川省委常委、组织部部长","start":"2022-05","end":"~2025","rank":"副部级","note":""},
    {"id":47,"person_id":7,"org_id":78,"title":"安阳市委书记","start":"2019-12","end":"2022-05","rank":"正厅级","note":""},
    {"id":48,"person_id":7,"org_id":76,"title":"河南省发改委副主任","start":"~2018","end":"2019-12","rank":"副厅级","note":""},

    # ── 张国智 ──
    {"id":49,"person_id":8,"org_id":2,"title":"广东省委常委、副省长","start":"~2024","end":"","rank":"副部级","note":"从重庆市调任广东省委常委、副省长"},
    {"id":50,"person_id":8,"org_id":51,"title":"重庆市副市长","start":"~2023","end":"~2024","rank":"副部级","note":""},
    {"id":51,"person_id":8,"org_id":53,"title":"重庆市发改委副主任","start":"~2018","end":"~2023","rank":"正厅级","note":""},
    {"id":52,"person_id":8,"org_id":52,"title":"重庆市大渡口区委副书记、区长","start":"~2014","end":"~2018","rank":"正厅级","note":""},
    {"id":53,"person_id":8,"org_id":52,"title":"重庆市大渡口区副区长","start":"~2008","end":"~2014","rank":"副厅级","note":""},

    # ── 胡劲军 ──
    {"id":54,"person_id":9,"org_id":7,"title":"广东省委常委、宣传部部长","start":"~2025","end":"","rank":"副部级","note":"从上海调任广东省委宣传部部长"},
    {"id":55,"person_id":9,"org_id":57,"title":"上海市委宣传部副部长","start":"~2019","end":"~2025","rank":"正厅级","note":""},
    {"id":56,"person_id":9,"org_id":58,"title":"上海市文化和旅游局局长","start":"~2018","end":"~2019","rank":"正厅级","note":""},
    {"id":57,"person_id":9,"org_id":56,"title":"上海市宣传系统工作","start":"~1990","end":"~2018","rank":"","note":"1990年复旦新闻系毕业进入上海宣传系统约28年，从记者逐步晋升"},

    # ── 张弓（省军区司令员） ──
    {"id":58,"person_id":10,"org_id":11,"title":"广东省委常委、省军区司令员","start":"~2023","end":"","rank":"副部级","note":"少将军衔"},

    # ── 胡帆 ──
    {"id":59,"person_id":11,"org_id":6,"title":"广东省委常委、组织部部长","start":"2025","end":"","rank":"副部级","note":"从财政部调任广东省委组织部部长"},
    {"id":60,"person_id":11,"org_id":59,"title":"财政部科教和文化司副司长、司长","start":"~2015","end":"~2025","rank":"正厅级","note":"在财政部系统长期工作"},
    {"id":61,"person_id":11,"org_id":60,"title":"财政部驻广西专员办专员","start":"~2012","end":"~2015","rank":"正厅级","note":""},

    # ── 刘国周 ──
    {"id":62,"person_id":12,"org_id":10,"title":"广东省副省长、省公安厅厅长","start":"2023","end":"","rank":"副部级","note":"从深圳市公安局长晋升省公安厅厅长"},
    {"id":63,"person_id":12,"org_id":49,"title":"深圳市副市长、市公安局局长","start":"2020","end":"2023","rank":"正厅级","note":""},
    {"id":64,"person_id":12,"org_id":48,"title":"北京市公安局副局长","start":"~2018","end":"2020","rank":"正厅级","note":""},
    {"id":65,"person_id":12,"org_id":48,"title":"北京市公安系统工作","start":"1995-07","end":"~2018","rank":"","note":"1995年从北京警察学院毕业进入北京公安系统约23年"},

    # ── 王胜 ──
    {"id":66,"person_id":13,"org_id":2,"title":"广东省副省长","start":"~2024","end":"","rank":"副部级","note":"从揭阳市委书记晋升副省长"},
    {"id":67,"person_id":13,"org_id":15,"title":"揭阳市委书记","start":"~2021","end":"~2024","rank":"正厅级","note":""},
    {"id":68,"person_id":13,"org_id":94,"title":"惠州市委副书记","start":"~2018","end":"~2021","rank":"副厅级","note":""},

    # ── 李运 ──
    {"id":69,"person_id":14,"org_id":2,"title":"广东省副省长","start":"~2025","end":"","rank":"副部级","note":"从中国农业银行调任广东省副省长"},
    {"id":70,"person_id":14,"org_id":95,"title":"中国农业银行副行长","start":"~2021","end":"~2025","rank":"副部级央企","note":""},

    # ── 唐屹峰 ──
    {"id":71,"person_id":15,"org_id":2,"title":"广东省副省长","start":"~2025","end":"","rank":"副部级","note":"从佛山市委书记晋升副省长"},
    {"id":72,"person_id":15,"org_id":14,"title":"佛山市委书记","start":"~2024","end":"~2025","rank":"正厅级","note":""},
    {"id":73,"person_id":15,"org_id":55,"title":"南方电网广东电网公司董事长","start":"~2021","end":"~2024","rank":"正厅级央企","note":""},
    {"id":74,"person_id":15,"org_id":54,"title":"南方电网系统工作","start":"~1995","end":"~2024","rank":"","note":"在电网系统工作约30年"},

    # ── Predecessors — 省委书记 ──
    {"id":75,"person_id":16,"org_id":17,"title":"中央政治局常委、中央纪委书记","start":"2022-10","end":"","rank":"正国级","note":"2022.10二十大当选中央政治局常委、中央纪委书记"},
    {"id":76,"person_id":16,"org_id":1,"title":"广东省委书记","start":"2017-10","end":"2022-10","rank":"正部级","note":"约5年"},
    {"id":77,"person_id":16,"org_id":64,"title":"辽宁省委书记","start":"2015-05","end":"2017-10","rank":"正部级","note":""},
    {"id":78,"person_id":16,"org_id":63,"title":"上海市委副书记、市长","start":"2012-12","end":"2015-05","rank":"副部级","note":""},
    {"id":79,"person_id":16,"org_id":63,"title":"上海市委常委、副市长","start":"2010-10","end":"2012-12","rank":"副部级","note":""},
    {"id":80,"person_id":16,"org_id":62,"title":"陕西省委常委、秘书长","start":"2006-08","end":"2010-10","rank":"副部级","note":""},
    {"id":81,"person_id":16,"org_id":61,"title":"甘肃省副省长","start":"2004-12","end":"2006-08","rank":"副部级","note":""},

    {"id":82,"person_id":17,"org_id":18,"title":"全国政协副主席","start":"2023-03","end":"","rank":"副国级","note":"从广东省委书记调任全国政协"},
    {"id":83,"person_id":17,"org_id":1,"title":"广东省委书记","start":"2012-12","end":"2017-10","rank":"正部级","note":"约5年，后调任国务院副总理（2018-2023）"},
    {"id":84,"person_id":17,"org_id":66,"title":"河北省委副书记、省长","start":"2010-01","end":"2012-12","rank":"正部级","note":""},
    {"id":85,"person_id":17,"org_id":67,"title":"共青团中央书记处第一书记","start":"2006-12","end":"2010-01","rank":"正部级","note":""},
    {"id":86,"person_id":17,"org_id":65,"title":"西藏自治区党委常委、秘书长","start":"~2003","end":"2006-12","rank":"副部级","note":""},
    {"id":87,"person_id":17,"org_id":65,"title":"共青团西藏自治区委书记","start":"~1997","end":"~2003","rank":"正厅级","note":""},

    # ── Predecessors — 省长 ──
    {"id":88,"person_id":18,"org_id":22,"title":"内蒙古自治区党委书记","start":"2025","end":"","rank":"正部级","note":"从广东省长调任内蒙古自治区党委书记"},
    {"id":89,"person_id":18,"org_id":2,"title":"广东省省长","start":"2021-12","end":"2025","rank":"正部级","note":"约3年"},
    {"id":90,"person_id":18,"org_id":13,"title":"深圳市委书记","start":"2018-12","end":"2021-12","rank":"副部级","note":""},
    {"id":91,"person_id":18,"org_id":69,"title":"山西省委常委、太原市委书记","start":"2017-03","end":"2018-12","rank":"副部级","note":""},
    {"id":92,"person_id":18,"org_id":68,"title":"科技部副部长","start":"2014-09","end":"2017-03","rank":"副部级","note":""},
    {"id":93,"person_id":18,"org_id":68,"title":"科技部政策法规司司长","start":"~2010","end":"2014-09","rank":"正厅级","note":""},

    {"id":94,"person_id":19,"org_id":74,"title":"新疆党委书记","start":"2021-12","end":"~2024","rank":"正部级","note":"2024年被开除党籍"},
    {"id":95,"person_id":19,"org_id":2,"title":"广东省省长","start":"2017-01","end":"2021-12","rank":"正部级","note":"约5年"},
    {"id":96,"person_id":19,"org_id":1,"title":"广东省委副书记","start":"2016-12","end":"2017-01","rank":"副部级","note":"调任广东"},
    {"id":97,"person_id":19,"org_id":73,"title":"工业和信息化部副部长、国家航天局局长","start":"2013-03","end":"2016-12","rank":"副部级","note":""},
    {"id":98,"person_id":19,"org_id":72,"title":"国家航天局局长","start":"2010-04","end":"2013-03","rank":"副部级","note":""},
    {"id":99,"person_id":19,"org_id":71,"title":"中国航天科技集团公司总经理","start":"2007-08","end":"2013-03","rank":"副部级央企","note":""},
    {"id":100,"person_id":19,"org_id":70,"title":"哈尔滨工业大学副校长","start":"~1996","end":"~2007","rank":"正厅级","note":""},

    # ── 陈良贤 ──
    {"id":101,"person_id":20,"org_id":2,"title":"广东省政府党组成员","start":"~2023","end":"","rank":"副部级","note":"原副省长转任党组成员"},
    {"id":102,"person_id":20,"org_id":2,"title":"广东省副省长","start":"~2018","end":"~2023","rank":"副部级","note":""},
    {"id":103,"person_id":20,"org_id":96,"title":"汕头市委书记","start":"~2016","end":"~2018","rank":"正厅级","note":""},
    {"id":104,"person_id":20,"org_id":97,"title":"中山市委副书记、市长","start":"~2014","end":"~2016","rank":"正厅级","note":""},
    {"id":105,"person_id":20,"org_id":98,"title":"广晟资产经营有限公司董事长","start":"~2011","end":"~2014","rank":"正厅级","note":""},

    # ── 陈敏（省政府秘书长） ──
    {"id":106,"person_id":21,"org_id":2,"title":"广东省政府秘书长","start":"~2023","end":"","rank":"正厅级","note":""},
    {"id":107,"person_id":21,"org_id":92,"title":"江西省财政厅厅长","start":"~2021","end":"~2023","rank":"正厅级","note":""},
    {"id":108,"person_id":21,"org_id":91,"title":"吉安市委书记","start":"~2019","end":"~2021","rank":"正厅级","note":""},
    {"id":109,"person_id":21,"org_id":88,"title":"萍乡市委书记","start":"~2016","end":"~2019","rank":"正厅级","note":""},
    {"id":110,"person_id":21,"org_id":88,"title":"萍乡市市长","start":"~2013","end":"~2016","rank":"正厅级","note":""},

    # ── 黄楚平 ──
    {"id":111,"person_id":22,"org_id":3,"title":"广东省人大常委会主任","start":"2022-01","end":"","rank":"正部级","note":"从广东省政协主席转任"},
    {"id":112,"person_id":22,"org_id":83,"title":"湖北省政协主席","start":"~2018","end":"~2021","rank":"正部级","note":"从湖北调任广东"},
    {"id":113,"person_id":22,"org_id":81,"title":"湖北省委副书记","start":"~2016","end":"~2018","rank":"副部级","note":""},
    {"id":114,"person_id":22,"org_id":82,"title":"湖北省常务副省长","start":"~2012","end":"~2016","rank":"副部级","note":""},
    {"id":115,"person_id":22,"org_id":82,"title":"湖北省副省长","start":"~2010","end":"~2012","rank":"副部级","note":""},
    {"id":116,"person_id":22,"org_id":85,"title":"宜昌市委书记","start":"~2008","end":"~2010","rank":"正厅级","note":""},
    {"id":117,"person_id":22,"org_id":84,"title":"咸宁市委书记","start":"~2006","end":"~2008","rank":"正厅级","note":""},

    # ── 林克庆 ──
    {"id":118,"person_id":23,"org_id":4,"title":"广东省政协主席","start":"2023-01","end":"","rank":"正部级","note":""},
    {"id":119,"person_id":23,"org_id":1,"title":"广东省委常委、常务副省长","start":"~2021","end":"~2023","rank":"副部级","note":""},
    {"id":120,"person_id":23,"org_id":79,"title":"北京市委常委、市委教工委书记","start":"~2019","end":"~2021","rank":"副部级","note":""},
    {"id":121,"person_id":23,"org_id":79,"title":"北京市副市长","start":"~2013","end":"~2019","rank":"副部级","note":""},
    {"id":122,"person_id":23,"org_id":80,"title":"北京市政府副秘书长","start":"~2009","end":"~2013","rank":"正厅级","note":""},
    {"id":123,"person_id":23,"org_id":50,"title":"重庆市大足县委副书记","start":"~2007","end":"~2009","rank":"正处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 黄坤明 ↔ 孟凡利（党政搭档） ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"黄坤明（省委书记）与孟凡利（省长）为广东省党政一把手搭档","overlap_org":"广东省","overlap_period":"2025-02至今"},

    # ── 省委书记接班人 ──
    {"id":2,"person_a":16,"person_b":1,"type":"前后任","context":"李希（2017-2022广东省委书记）→ 黄坤明（2022.10接任）。李希晋升中央政治局常委、中央纪委书记","overlap_org":"中共广东省委员会","overlap_period":"不重叠（前后任）"},
    {"id":3,"person_a":17,"person_b":16,"type":"前后任","context":"胡春华（2012-2017广东省委书记）→ 李希（2017.10接任）。胡春华后任国务院副总理","overlap_org":"中共广东省委员会","overlap_period":"不重叠（前后任）"},

    # ── 省长接班人 ──
    {"id":4,"person_a":18,"person_b":2,"type":"前后任","context":"王伟中（2021-2025广东省长）→ 孟凡利（2025.02接任）。王伟中调任内蒙古自治区党委书记","overlap_org":"广东省人民政府","overlap_period":"不重叠（前后任）"},
    {"id":5,"person_a":19,"person_b":18,"type":"前后任","context":"马兴瑞（2017-2021广东省长）→ 王伟中（2021.12接任省长）。马兴瑞调任新疆党委书记后被开除党籍","overlap_org":"广东省人民政府","overlap_period":"不重叠（前后任）"},

    # ── 省长→书记 晋升 ──
    {"id":6,"person_a":16,"person_b":19,"type":"省长→书记","context":"李希（上海市委副书记→辽宁省委书记→广东省委书记）。马兴瑞（广东省长→新疆党委书记）","overlap_org":"广东省","overlap_period":"2017"},

    # ── 深圳书记→省长 管道 ──
    {"id":7,"person_a":18,"person_b":2,"type":"前后任深圳书记","context":"王伟中（2018-2021深圳书记→广东省长）→ 孟凡利（2022-2025深圳书记→广东省长）。深圳市委书记晋升省长的管道","overlap_org":"深圳市","overlap_period":"不重叠（前后任）"},

    # ── 跨省交流网络 ──
    {"id":8,"person_a":1,"person_b":26,"type":"跨省交流","context":"黄坤明（闽→浙→中央→粤）历经福建、浙江、中央宣传部、广东四省交流","overlap_org":"福建/浙江/中央/广东","overlap_period":"1982-2022"},
    {"id":9,"person_a":2,"person_b":36,"type":"跨省交流","context":"孟凡利（鲁→蒙→粤）从山东→内蒙古→广东，三省份跨省交流","overlap_org":"山东/内蒙古/广东","overlap_period":"1986-2025"},
    {"id":10,"person_a":4,"person_b":43,"type":"跨省交流","context":"冯忠华（建设部/全国人大→琼→粤）北京中央→海南→广东","overlap_org":"北京/海南/广东","overlap_period":"1993-2025"},
    {"id":11,"person_a":8,"person_b":51,"type":"跨省交流","context":"张国智（渝→粤）从重庆调任广东","overlap_org":"重庆/广东","overlap_period":"~2024"},
    {"id":12,"person_a":9,"person_b":57,"type":"跨省交流","context":"胡劲军（沪→粤）从上海宣传系统调任广东","overlap_org":"上海/广东","overlap_period":"~2025"},
    {"id":13,"person_a":7,"person_b":77,"type":"跨省交流","context":"靳磊（豫→川→粤）从河南→四川→广东","overlap_org":"河南/四川/广东","overlap_period":"~2025"},
    {"id":14,"person_a":11,"person_b":59,"type":"跨省交流","context":"胡帆（财政部→粤）从中央部委调任广东省委组织部","overlap_org":"中央/广东","overlap_period":"2025"},

    # ── 央地交流 ──
    {"id":15,"person_a":1,"person_b":20,"type":"央地交流","context":"黄坤明在中央宣传部工作约8年（2014-2022），典型的中央→地方交流","overlap_org":"中央/广东","overlap_period":"2014-2022"},
    {"id":16,"person_a":11,"person_b":59,"type":"央地交流","context":"胡帆在财政部系统工作多年，从中央部委调任广东省，典型的央地交流","overlap_org":"中央/广东","overlap_period":"~2025"},
    {"id":17,"person_a":4,"person_b":41,"type":"央地交流","context":"冯忠华在住建部系统工作约21年（1993-2014），后转任全国人大、海南","overlap_org":"中央/地方","overlap_period":"1993-2024"},
    {"id":18,"person_a":14,"person_b":95,"type":"金融→政府交流","context":"李运从农业银行副行长调任广东省副省长，典型的金融央企→政府交流","overlap_org":"金融/广东","overlap_period":"~2025"},
    {"id":19,"person_a":15,"person_b":54,"type":"企业→政府交流","context":"唐屹峰从南方电网系统调任佛山市委书记、副省长，央企→地方交流","overlap_org":"企业/广东","overlap_period":"~2024"},

    # ── 广东→中央外流 ──
    {"id":20,"person_a":16,"person_b":17,"type":"地方→中央","context":"李希从广东省委书记晋升中央政治局常委、中央纪委书记（正国级）","overlap_org":"广东/中央","overlap_period":"2017-2022"},
    {"id":21,"person_a":17,"person_b":18,"type":"地方→中央","context":"胡春华从广东省委书记调任国务院副总理，后任全国政协副主席","overlap_org":"广东/中央","overlap_period":"2012-2023"},
    {"id":22,"person_a":18,"person_b":22,"type":"省际调动","context":"王伟中从广东省长调任内蒙古自治区党委书记","overlap_org":"广东/内蒙古","overlap_period":"2025"},

    # ── 省委常委会关系 ──
    {"id":23,"person_a":5,"person_b":1,"type":"省委班子搭档","context":"张虎（常务副省长，广州/深圳系统）与黄坤明（中央宣传部系统）搭配","overlap_org":"广东省","overlap_period":"2023至今"},
    {"id":24,"person_a":3,"person_b":1,"type":"省委班子搭档","context":"马森述（纪委书记，中央纪委系统）为黄坤明（省委书记）治下的执纪负责人","overlap_org":"广东省","overlap_period":"2022至今"},
    {"id":25,"person_a":9,"person_b":1,"type":"省委班子搭档","context":"胡劲军（宣传部长，上海宣传系统）与黄坤明（前中宣部长）在宣传系统有相似经历","overlap_org":"广东/宣传系统","overlap_period":"2025至今"},
    {"id":26,"person_a":4,"person_b":7,"type":"省委班子搭档","context":"冯忠华（广州市委书记）与靳磊（深圳市委书记）分别为两大副省级城市一把手","overlap_org":"广东省","overlap_period":"2025至今"},
    {"id":27,"person_a":8,"person_b":13,"type":"省委班子搭档","context":"张国智（副省长）与王胜（副省长）同为省政府班子成员","overlap_org":"广东省人民政府","overlap_period":"~2024至今"},

    # ── 政法/纪检系统 ──
    {"id":28,"person_a":3,"person_b":17,"type":"纪检系统","context":"马森述（广东省纪委书记）曾在中央纪委工作，与中央纪委李希有系统内关系","overlap_org":"中央纪委/广东","overlap_period":"~2018至今"},
    {"id":29,"person_a":12,"person_b":48,"type":"公安系统","context":"刘国周（省公安厅长）长期在北京公安系统工作，后调任广东","overlap_org":"北京/广东公安","overlap_period":"1995-2023"},

    # ── 上下级/秘书 → 主官 ──
    {"id":30,"person_a":17,"person_b":16,"type":"前后任政治局委员","context":"胡春华与李希先后担任广东省委书记，并均进入中央政治局","overlap_org":"广东/中央政治局","overlap_period":"2017（交接）"},
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
    if "省委书记" in post and "中央政治局委员" in post:
        return "180,20,20"  # deepest red for politburo member + party secretary
    if "省委书记" in post:
        return "200,30,30"  # deep red for party secretary
    if "省长" in post and "省委副书记" in post:
        return "30,70,200"  # deep blue for governor
    if "省委副书记" in post:
        return "220,60,60"  # red for deputy party secretary
    if "常务副省长" in post:
        return "50,110,220"  # blue for executive vice governor
    if "副省长" in post:
        return "60,120,220"  # blue for vice governor
    if "纪委书记" in post:
        return "230,150,0"  # orange for discipline
    if "组织部长" in post:
        return "170,80,170"  # purple for organization dept
    if "宣传部长" in post:
        return "160,70,160"  # purple for propaganda
    if "统战部长" in post:
        return "180,90,180"  # purple for united front
    if "政协" in post:
        return "180,160,220"
    if "人大" in post:
        return "160,200,220"
    if "军区" in post:
        return "140,140,140"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>广东省（省级）领导班子工作关系网络 — 2026年7月15日生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["省委书记","省长","省委副书记","政协主席","人大主任"]) else "12.0"
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
