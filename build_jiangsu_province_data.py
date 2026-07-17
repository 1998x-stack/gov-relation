#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Jiangsu Province (江苏省) leadership network.

Covers: Provincial Party Secretary (省委书记), Governor (省长), predecessors,
succession chains, key deputy leaders (省委常委会成员, 副省长等),
and the provincial-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/jiangsu_province_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/jiangsu_province_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 信长星 — 江苏省委书记 (as of 2023.01)
    {"id":1,"name":"信长星","gender":"男","ethnicity":"汉族","birth":"1963-12","birthplace":"山东惠民","education":"曲阜师范大学（曲阜师大）经济学学士、华中师范大学硕士研究生","party_join":"1986-06","work_start":"1986-07","current_post":"江苏省委书记","current_org":"中共江苏省委员会","source":"https://zh.wikipedia.org/wiki/%E4%BF%A1%E9%95%BF%E6%98%9F"},
    # 刘小涛 — 江苏省省长
    {"id":2,"name":"刘小涛","gender":"男","ethnicity":"汉族","birth":"1970-07","birthplace":"广东兴宁","education":"中国人民大学劳动人事学院本科、在职研究生","party_join":"1991-12","work_start":"1992-07","current_post":"江苏省委副书记、省长","current_org":"江苏省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E5%B0%8F%E6%B6%9B"},

    # ── Provincial leadership (省委常委会成员) ──
    {"id":3,"name":"张忠","gender":"男","ethnicity":"汉族","birth":"1968-03","birthplace":"山东莱州","education":"","party_join":"1991","work_start":"","current_post":"江苏省委常委、省纪委书记、省监委主任","current_org":"中共江苏省纪律检查委员会","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%BF%A0_(1968%E5%B9%B4)"},
    {"id":4,"name":"周红波","gender":"男","ethnicity":"汉族","birth":"1970-10","birthplace":"广西临桂","education":"南京农业大学、中国农业大学在职研究生","party_join":"","work_start":"","current_post":"江苏省委常委、南京市委书记","current_org":"中共南京市委员会","source":"https://zh.wikipedia.org/wiki/%E5%91%A8%E7%BA%A2%E6%B3%A2"},
    {"id":5,"name":"刘建洋","gender":"男","ethnicity":"汉族","birth":"1966-04","birthplace":"江西莲花","education":"中专","party_join":"1986","work_start":"1985-07","current_post":"江苏省委常委、省委组织部部长","current_org":"中共江苏省委员会","source":"https://zh.wikipedia.org/wiki/%E5%88%98%E5%BB%BA%E6%B4%8B"},
    {"id":6,"name":"马欣","gender":"男","ethnicity":"汉族","birth":"1967-11","birthplace":"天津","education":"同济大学、中国人民大学、北京交通大学","party_join":"1989","work_start":"1990","current_post":"江苏省委常委、常务副省长","current_org":"江苏省人民政府","source":"https://zh.wikipedia.org/wiki/%E9%A9%AC%E6%AC%A3"},
    {"id":7,"name":"张国成","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"江苏省委常委、省军区政委","current_org":"江苏省军区","source":"https://www.jiangsu.gov.cn"},
    {"id":8,"name":"范波","gender":"男","ethnicity":"汉族","birth":"1969-10","birthplace":"湖北洪湖","education":"吉林工业大学（吉林工大）、中欧国际工商学院MBA","party_join":"","work_start":"","current_post":"江苏省委常委、苏州市委书记","current_org":"中共苏州市委员会","source":"https://zh.wikipedia.org/wiki/%E8%8C%83%E6%B3%A2"},
    {"id":9,"name":"徐缨","gender":"女","ethnicity":"汉族","birth":"1967-09","birthplace":"江苏常州","education":"","party_join":"","work_start":"","current_post":"江苏省委常委、宣传部部长","current_org":"中共江苏省委员会","source":"https://baike.baidu.com/item/%E5%BE%90%E7%BC%A8"},
    {"id":10,"name":"李耀光","gender":"男","ethnicity":"汉族","birth":"1970-10","birthplace":"北京","education":"首都师范大学、北京工业大学在职博士","party_join":"","work_start":"","current_post":"江苏省委常委、政法委书记","current_org":"中共江苏省委员会","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E8%80%80%E5%85%89"},
    {"id":11,"name":"陈忠伟","gender":"男","ethnicity":"汉族","birth":"1969-06","birthplace":"广东潮州","education":"徐州师范大学","party_join":"","work_start":"","current_post":"江苏省委常委、省委秘书长","current_org":"中共江苏省委员会","source":"https://baike.baidu.com/item/%E9%99%88%E5%BF%A0%E4%BC%9F"},

    # ── Vice governors (副省长) ──
    {"id":12,"name":"赵岩","gender":"男","ethnicity":"满族","birth":"1973-08","birthplace":"北京","education":"","party_join":"","work_start":"","current_post":"江苏省副省长","current_org":"江苏省人民政府","source":"https://baike.baidu.com/item/%E8%B5%B5%E5%B2%A9/64807453"},
    {"id":13,"name":"马士光","gender":"男","ethnicity":"汉族","birth":"1969-09","birthplace":"江苏邳州","education":"","party_join":"","work_start":"","current_post":"江苏省副省长","current_org":"江苏省人民政府","source":"https://baike.baidu.com/item/%E9%A9%AC%E5%A3%AB%E5%85%89/64536531"},
    {"id":14,"name":"胡彬郴","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"江苏省副省长、省公安厅厅长","current_org":"江苏省公安厅","source":"https://baike.baidu.com/item/%E8%83%A1%E5%BD%AC%E9%83%B4"},
    {"id":15,"name":"沈剑荣","gender":"男","ethnicity":"汉族","birth":"1969-03","birthplace":"江苏苏州","education":"南京工业大学（南工大）、南京大学博士","party_join":"","work_start":"","current_post":"江苏省副省长","current_org":"江苏省人民政府","source":"https://baike.baidu.com/item/%E6%B2%88%E5%89%91%E8%8D%A3"},

    # ── Predecessors — 省委书记 ──
    {"id":16,"name":"吴政隆","gender":"男","ethnicity":"汉族","birth":"1964-11","birthplace":"浙江宁波","education":"","party_join":"","work_start":"","current_post":"国务委员、国务院秘书长（原江苏省委书记、省长）","current_org":"国务院办公厅","source":"https://zh.wikipedia.org/wiki/%E5%90%B4%E6%94%BF%E9%9A%86"},
    {"id":17,"name":"娄勤俭","gender":"男","ethnicity":"汉族","birth":"1956-12","birthplace":"贵州桐梓","education":"","party_join":"","work_start":"","current_post":"全国人大常委会委员（原江苏省委书记）","current_org":"全国人大常委会","source":"https://zh.wikipedia.org/wiki/%E5%A8%84%E5%8B%A4%E4%BF%AD"},
    {"id":18,"name":"李强","gender":"男","ethnicity":"汉族","birth":"1959-07","birthplace":"浙江瑞安","education":"","party_join":"","work_start":"","current_post":"国务院总理（原江苏省委书记）","current_org":"国务院","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E5%BC%BA_(1959%E5%B9%B4)"},

    # ── Predecessors — 省长 ──
    {"id":19,"name":"许昆林","gender":"男","ethnicity":"汉族","birth":"1965-","birthplace":"","education":"","party_join":"","work_start":"","current_post":"辽宁省委书记（原江苏省省长）","current_org":"中共辽宁省委员会","source":"https://zh.wikipedia.org/wiki/%E8%AE%B8%E6%98%86%E6%9E%97"},
    {"id":20,"name":"石泰峰","gender":"男","ethnicity":"汉族","birth":"1956-09","birthplace":"山西榆社","education":"","party_join":"","work_start":"","current_post":"中共中央政治局委员、中央组织部部长（原江苏省省长）","current_org":"中央组织部","source":"https://zh.wikipedia.org/wiki/%E7%9F%B3%E6%B3%B0%E5%B3%B0"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Jiangsu provincial core
    {"id":1,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":2,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":3,"name":"江苏省人大常委会","type":"人大","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":4,"name":"政协江苏省委员会","type":"政协","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":5,"name":"中共江苏省纪律检查委员会","type":"党委","level":"省级","parent":"中共江苏省委员会","location":"江苏省南京市"},
    {"id":6,"name":"江苏省军区","type":"党委","level":"省级","parent":"中央军委","location":"江苏省南京市"},

    # Key provincial departments
    {"id":7,"name":"江苏省公安厅","type":"政府","level":"省级","parent":"江苏省人民政府","location":"江苏省南京市"},
    {"id":8,"name":"中共江苏省委组织部","type":"党委","level":"省级","parent":"中共江苏省委员会","location":"江苏省南京市"},
    {"id":9,"name":"中共江苏省委宣传部","type":"党委","level":"省级","parent":"中共江苏省委员会","location":"江苏省南京市"},
    {"id":10,"name":"中共江苏省委统战部","type":"党委","level":"省级","parent":"中共江苏省委员会","location":"江苏省南京市"},
    {"id":11,"name":"中共江苏省委政法委","type":"党委","level":"省级","parent":"中共江苏省委员会","location":"江苏省南京市"},

    # Key cities (副省级)
    {"id":12,"name":"中共南京市委员会","type":"党委","level":"副省级","parent":"中共江苏省委员会","location":"江苏省南京市"},
    {"id":13,"name":"中共苏州市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省苏州市"},

    # Central / national orgs
    {"id":14,"name":"国务院","type":"政府","level":"国家级","parent":"","location":"北京市"},
    {"id":15,"name":"国务院办公厅","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":16,"name":"中央组织部","type":"党委","level":"国家级","parent":"中央政治局","location":"北京市"},
    {"id":17,"name":"全国人大常委会","type":"人大","level":"国家级","parent":"","location":"北京市"},
    {"id":18,"name":"人力资源和社会保障部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":19,"name":"国家公务员局","type":"政府","level":"国家级","parent":"人力资源和社会保障部","location":"北京市"},
    {"id":20,"name":"中央纪委国家监委","type":"党委","level":"国家级","parent":"","location":"北京市"},

    # 信长星 earlier work units
    {"id":21,"name":"国家劳动部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":22,"name":"中共安徽省委员会","type":"党委","level":"省级","parent":"","location":"安徽省合肥市"},
    {"id":23,"name":"中共青海省委员会","type":"党委","level":"省级","parent":"","location":"青海省西宁市"},
    {"id":24,"name":"青海省人民政府","type":"政府","level":"省级","parent":"","location":"青海省西宁市"},

    # 刘小涛 earlier work units
    {"id":25,"name":"广东省劳动系统","type":"政府","level":"省级","parent":"广东省人民政府","location":"广东省广州市"},
    {"id":26,"name":"中共茂名市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省茂名市"},
    {"id":27,"name":"中共汕头市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省汕头市"},
    {"id":28,"name":"中共潮州市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省潮州市"},
    {"id":29,"name":"广东省政府","type":"政府","level":"省级","parent":"","location":"广东省广州市"},
    {"id":30,"name":"浙江省政府","type":"政府","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":31,"name":"中共温州市委员会","type":"党委","level":"地级","parent":"中共浙江省委员会","location":"浙江省温州市"},

    # 马欣 earlier
    {"id":32,"name":"国家开发银行","type":"事业单位","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":33,"name":"国开行天津分行","type":"事业单位","level":"","parent":"国家开发银行","location":"天津市"},
    {"id":34,"name":"国开行青海分行","type":"事业单位","level":"","parent":"国家开发银行","location":"青海省西宁市"},
    {"id":35,"name":"国开行广西分行","type":"事业单位","level":"","parent":"国家开发银行","location":"广西壮族自治区南宁市"},

    # 张忠 earlier
    {"id":36,"name":"中共吉林省纪律检查委员会","type":"党委","level":"省级","parent":"中共吉林省委员会","location":"吉林省长春市"},

    # 刘建洋 earlier
    {"id":37,"name":"南昌市城市建设系统","type":"政府","level":"","parent":"中共南昌市委员会","location":"江西省南昌市"},
    {"id":38,"name":"中共莆田市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省莆田市"},
    {"id":39,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
    {"id":40,"name":"中共泉州市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省泉州市"},

    # 周红波 earlier
    {"id":41,"name":"广西农业系统","type":"政府","level":"省级","parent":"广西壮族自治区人民政府","location":"广西壮族自治区南宁市"},
    {"id":42,"name":"中共广西壮族自治区委员会","type":"党委","level":"省级","parent":"","location":"广西壮族自治区南宁市"},
    {"id":43,"name":"中共海南省委员会","type":"党委","level":"省级","parent":"","location":"海南省海口市"},
    {"id":44,"name":"中共三亚市委员会","type":"党委","level":"地级","parent":"中共海南省委员会","location":"海南省三亚市"},

    # 范波 earlier
    {"id":45,"name":"中国农业机械化科学研究院","type":"事业单位","level":"国家级","parent":"","location":"北京市"},
    {"id":46,"name":"国家机械工业部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":47,"name":"国家发展和改革委员会","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":48,"name":"中共四川省委员会","type":"党委","level":"省级","parent":"","location":"四川省成都市"},
    {"id":49,"name":"中共自贡市委员会","type":"党委","level":"地级","parent":"中共四川省委员会","location":"四川省自贡市"},
    {"id":50,"name":"中共山东省委员会","type":"党委","level":"省级","parent":"","location":"山东省济南市"},

    # 李耀光 earlier
    {"id":51,"name":"北京政法系统","type":"政府","level":"","parent":"中共北京市委员会","location":"北京市"},

    # 沈剑荣 earlier (本地晋升)
    {"id":52,"name":"南京市各级系统","type":"政府","level":"副省级","parent":"江苏省人民政府","location":"江苏省南京市"},

    # 许昆林 / 石泰峰 / 吴政隆 earlier
    {"id":53,"name":"中共辽宁省委员会","type":"党委","level":"省级","parent":"","location":"辽宁省沈阳市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 信长星 ──
    {"id":1,"person_id":1,"org_id":1,"title":"江苏省委书记","start":"2023-01","end":"","rank":"正部级","note":"2023.01从青海省委书记调任江苏省委书记"},
    {"id":2,"person_id":1,"org_id":23,"title":"青海省委书记","start":"2022-03","end":"2023-01","rank":"正部级","note":"约10个月"},
    {"id":3,"person_id":1,"org_id":24,"title":"青海省省长","start":"2020-07","end":"2022-03","rank":"正部级","note":"2020.07任青海省代省长，后当选省长"},
    {"id":4,"person_id":1,"org_id":22,"title":"安徽省委副书记","start":"2016-09","end":"2020-07","rank":"副部级","note":"2016.09任安徽省委副书记"},
    {"id":5,"person_id":1,"org_id":19,"title":"国家公务员局副局长","start":"2010-09","end":"2016-09","rank":"副部级","note":"2010.09任国家公务员局副局长、党组成员"},
    {"id":6,"person_id":1,"org_id":18,"title":"人力资源和社会保障部官员","start":"2008-03","end":"2010-09","rank":"","note":"人社部成立后转入，历任职位"},
    {"id":7,"person_id":1,"org_id":21,"title":"劳动部（劳动保障部）官员","start":"1986-07","end":"2008-03","rank":"","note":"1986年从曲阜师大毕业后进入劳动部工作，从科员逐步晋升至司局级，历时22年"},

    # ── 刘小涛 ──
    {"id":8,"person_id":2,"org_id":2,"title":"江苏省委副书记、省长","start":"2025-01","end":"","rank":"正部级","note":"2025.01从苏州市委书记晋升江苏省省长"},
    {"id":9,"person_id":2,"org_id":13,"title":"苏州市委书记","start":"2023-10","end":"2025-01","rank":"副部级","note":"2023.10任江苏省委常委、苏州市委书记"},
    {"id":10,"person_id":2,"org_id":1,"title":"江苏省委常委","start":"2023-10","end":"2025-01","rank":"副部级","note":"2023.10从浙江调任江苏省委常委"},
    {"id":11,"person_id":2,"org_id":31,"title":"温州市委书记","start":"2021-08","end":"2023-10","rank":"副部级","note":"2021.08任浙江省委常委、温州市委书记"},
    {"id":12,"person_id":2,"org_id":30,"title":"浙江省副省长","start":"2020-04","end":"2021-08","rank":"副部级","note":"2020.04任浙江省副省长"},
    {"id":13,"person_id":2,"org_id":29,"title":"广东省政府秘书长","start":"2019-05","end":"2020-04","rank":"正厅级","note":"2019.05任广东省政府秘书长"},
    {"id":14,"person_id":2,"org_id":28,"title":"潮州市委书记","start":"2017-06","end":"2019-05","rank":"正厅级","note":""},
    {"id":15,"person_id":2,"org_id":27,"title":"汕头市委书记","start":"2016-04","end":"2017-06","rank":"正厅级","note":""},
    {"id":16,"person_id":2,"org_id":26,"title":"茂名市委常委、副市长","start":"2014-04","end":"2016-04","rank":"副厅级","note":""},
    {"id":17,"person_id":2,"org_id":26,"title":"茂名市副市长","start":"2012-08","end":"2014-04","rank":"副厅级","note":""},
    {"id":18,"person_id":2,"org_id":25,"title":"广东省劳动系统工作","start":"1992-07","end":"2012-08","rank":"","note":"1992年从人大毕业进入广东省劳动局，此后在广东劳动系统工作20年"},

    # ── 张忠 ──
    {"id":19,"person_id":3,"org_id":5,"title":"江苏省委常委、省纪委书记、省监委主任","start":"2023-07","end":"","rank":"副部级","note":"2023.07从吉林省纪委书记调任江苏省纪委书记"},
    {"id":20,"person_id":3,"org_id":36,"title":"吉林省委常委、省纪委书记","start":"2019-11","end":"2023-07","rank":"副部级","note":""},
    {"id":21,"person_id":3,"org_id":20,"title":"中央组织部工作","start":"","end":"2019-11","rank":"","note":"长期在中央组织部工作，后调任吉林省纪委书记"},

    # ── 周红波 ──
    {"id":22,"person_id":4,"org_id":12,"title":"江苏省委常委、南京市委书记","start":"2024-12","end":"","rank":"副部级","note":"2024.12从海南调任南京市委书记"},
    {"id":23,"person_id":4,"org_id":43,"title":"海南省委常委、三亚市委书记","start":"2021-01","end":"2024-12","rank":"副部级","note":""},
    {"id":24,"person_id":4,"org_id":42,"title":"广西壮族自治区人民政府副主席","start":"2016-11","end":"2021-01","rank":"副部级","note":"兼南宁市长至2020"},
    {"id":25,"person_id":4,"org_id":42,"title":"南宁市市长","start":"2011-08","end":"2020-03","rank":"副省级","note":"在广西工作，长期在农业系统，后任南宁市长近9年"},
    {"id":26,"person_id":4,"org_id":41,"title":"广西农业系统工作","start":"1992-07","end":"2006-09","rank":"","note":"1992年参加工作，从技术员晋升"},

    # ── 刘建洋 ──
    {"id":27,"person_id":5,"org_id":8,"title":"江苏省委常委、省委组织部部长","start":"2024-02","end":"","rank":"副部级","note":"2024.02从省委政法委书记转任组织部部长"},
    {"id":28,"person_id":5,"org_id":11,"title":"江苏省委常委、省委政法委书记","start":"2022-12","end":"2024-02","rank":"副部级","note":"2022.12从福建调任江苏省委常委、政法委书记"},
    {"id":29,"person_id":5,"org_id":39,"title":"福建省委常委、泉州市委书记","start":"2021-10","end":"2022-12","rank":"副部级","note":""},
    {"id":30,"person_id":5,"org_id":38,"title":"莆田市委书记","start":"2019-12","end":"2021-10","rank":"正厅级","note":""},
    {"id":31,"person_id":5,"org_id":37,"title":"南昌市市长","start":"2018-03","end":"2019-12","rank":"副省级","note":"在南昌城建系统工作超30年"},
    {"id":32,"person_id":5,"org_id":37,"title":"南昌市城市建设系统","start":"1985-07","end":"2018-03","rank":"","note":"1985年中专毕业后进入南昌市城市建设系统，历任多职"},

    # ── 马欣 ──
    {"id":33,"person_id":6,"org_id":2,"title":"江苏省委常委、常务副省长","start":"2023-09","end":"","rank":"副部级","note":"2023.09任省委常委、常务副省长"},
    {"id":34,"person_id":6,"org_id":2,"title":"江苏省副省长","start":"2020-04","end":"2023-09","rank":"副部级","note":"2020.04从国家开发银行调任江苏副省长"},
    {"id":35,"person_id":6,"org_id":32,"title":"国家开发银行副行长","start":"~2018","end":"2020-04","rank":"副部级央企","note":""},
    {"id":36,"person_id":6,"org_id":35,"title":"国开行广西分行行长","start":"~2015","end":"~2018","rank":"正厅级","note":""},
    {"id":37,"person_id":6,"org_id":34,"title":"国开行青海分行行长","start":"~2012","end":"~2015","rank":"正厅级","note":""},
    {"id":38,"person_id":6,"org_id":33,"title":"国开行天津分行副行长","start":"~2009","end":"~2012","rank":"副厅级","note":""},
    {"id":39,"person_id":6,"org_id":32,"title":"国家开发银行系统工作","start":"1994","end":"~2009","rank":"","note":"1994年进入国开行系统，从基层逐步晋升"},

    # ── 张国成（省军区政委） ──
    {"id":40,"person_id":7,"org_id":6,"title":"江苏省委常委、省军区政委","start":"~2022","end":"","rank":"副部级","note":"少将军衔"},

    # ── 范波 ──
    {"id":41,"person_id":8,"org_id":13,"title":"江苏省委常委、苏州市委书记","start":"2025-03","end":"","rank":"副部级","note":"2025.03从山东调任苏州"},
    {"id":42,"person_id":8,"org_id":50,"title":"山东省副省长","start":"2022-07","end":"2025-03","rank":"副部级","note":""},
    {"id":43,"person_id":8,"org_id":49,"title":"自贡市委书记","start":"2017-09","end":"2022-07","rank":"正厅级","note":""},
    {"id":44,"person_id":8,"org_id":48,"title":"四川省发改委主任","start":"2016-03","end":"2017-09","rank":"正厅级","note":""},
    {"id":45,"person_id":8,"org_id":47,"title":"国家发改委工作","start":"2003-07","end":"2016-03","rank":"","note":"在国家发改委系统工作约13年"},
    {"id":46,"person_id":8,"org_id":45,"title":"中国农机院/机械部工作","start":"1991-08","end":"2003-07","rank":"","note":"1991年进入中国农机院，后转入机械部、国家计委等工作"},

    # ── 徐缨 ──
    {"id":47,"person_id":9,"org_id":9,"title":"江苏省委常委、宣传部部长","start":"2024-05","end":"","rank":"副部级","note":"2024.05从江苏省副省长转任宣传部长"},
    {"id":48,"person_id":9,"org_id":2,"title":"江苏省副省长","start":"2023-01","end":"2024-05","rank":"副部级","note":"此前任常州市委书记"},

    # ── 李耀光 ──
    {"id":49,"person_id":10,"org_id":11,"title":"江苏省委常委、政法委书记","start":"2024-11","end":"","rank":"副部级","note":"2024.11任省委政法委书记"},
    {"id":50,"person_id":10,"org_id":7,"title":"江苏省副省长、省公安厅厅长","start":"2022-05","end":"2024-11","rank":"副部级","note":"2022.05从北京调任江苏公安厅长"},
    {"id":51,"person_id":10,"org_id":51,"title":"北京政法系统工作","start":"~1992","end":"2022-05","rank":"","note":"长期在北京政法系统工作，约30年"},

    # ── 陈忠伟 ──
    {"id":52,"person_id":11,"org_id":1,"title":"江苏省委常委、省委秘书长","start":"2024-11","end":"","rank":"副部级","note":"2024.11任省委常委、省委秘书长"},

    # ── 赵岩（副省长，满族） ──
    {"id":53,"person_id":12,"org_id":2,"title":"江苏省副省长","start":"2023-09","end":"","rank":"副部级","note":"从工信部国家工业信息安全发展研究中心调任"},

    # ── 马士光（副省长） ──
    {"id":54,"person_id":13,"org_id":2,"title":"江苏省副省长","start":"2024-11","end":"","rank":"副部级","note":"从连云港市委书记晋升"},

    # ── 胡彬郴（副省长/公安厅长） ──
    {"id":55,"person_id":14,"org_id":7,"title":"江苏省副省长、省公安厅厅长","start":"2025-01","end":"","rank":"副部级","note":"2025.01任"},

    # ── 沈剑荣（副省长） ──
    {"id":56,"person_id":15,"org_id":2,"title":"江苏省副省长","start":"2024-11","end":"","rank":"副部级","note":"从南京市领导晋升"},

    # ── Predecessors — 省委书记 ──
    {"id":57,"person_id":16,"org_id":15,"title":"国务委员、国务院秘书长","start":"2023-03","end":"","rank":"副国级","note":"从江苏省委书记晋升国务委员"},
    {"id":58,"person_id":16,"org_id":1,"title":"江苏省委书记","start":"2021-10","end":"2022-12","rank":"正部级","note":"约14个月"},
    {"id":59,"person_id":16,"org_id":2,"title":"江苏省省长","start":"2017-05","end":"2021-10","rank":"正部级","note":"后接任省委书记"},
    {"id":60,"person_id":16,"org_id":53,"title":"辽宁省委副书记、沈阳市委书记","start":"2016-10","end":"2017-05","rank":"副部级","note":"从重庆调任辽宁"},

    {"id":61,"person_id":17,"org_id":17,"title":"全国人大常委会委员","start":"~2023","end":"","rank":"正部级","note":"（原江苏省委书记）"},
    {"id":62,"person_id":17,"org_id":1,"title":"江苏省委书记","start":"2017-10","end":"2021-10","rank":"正部级","note":"约4年"},
    {"id":63,"person_id":17,"org_id":2,"title":"陕西省省长","start":"2012-12","end":"2016-03","rank":"正部级","note":"（原陕西省长调任江苏）"},

    {"id":64,"person_id":18,"org_id":14,"title":"国务院总理","start":"2023-03","end":"","rank":"正国级","note":"现任国务院总理"},
    {"id":65,"person_id":18,"org_id":1,"title":"江苏省委书记","start":"2016-06","end":"2017-10","rank":"正部级","note":"约16个月"},
    {"id":66,"person_id":18,"org_id":2,"title":"浙江省省长","start":"2012-12","end":"2016-06","rank":"正部级","note":"调任江苏前为浙江省长"},

    # ── Predecessors — 省长 ──
    {"id":67,"person_id":19,"org_id":53,"title":"辽宁省委书记","start":"2025-01","end":"","rank":"正部级","note":"从江苏省长调任辽宁省委书记"},
    {"id":68,"person_id":19,"org_id":2,"title":"江苏省省长","start":"2021-10","end":"2025-01","rank":"正部级","note":"约3年多"},
    {"id":69,"person_id":19,"org_id":13,"title":"苏州市委书记","start":"2020-09","end":"2021-10","rank":"副部级","note":"此前任江苏省副省长"},

    {"id":70,"person_id":20,"org_id":16,"title":"中央组织部部长（政治局委员）","start":"2023-04","end":"","rank":"副国级","note":"现任政治局委员、中组部部长"},
    {"id":71,"person_id":20,"org_id":2,"title":"江苏省省长","start":"2015-11","end":"2017-04","rank":"正部级","note":"约17个月"},
    {"id":72,"person_id":20,"org_id":13,"title":"苏州市委书记","start":"2014-06","end":"2015-11","rank":"副部级","note":"从苏州书记升省长"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 信长星 ↔ 刘小涛（党政搭档） ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"信长星（省委书记）与刘小涛（省长）为江苏省党政一把手搭档","overlap_org":"江苏省","overlap_period":"2025-01至今"},

    # ── 省委书记接班人 ──
    {"id":2,"person_a":16,"person_b":1,"type":"前后任","context":"吴政隆（2021-2022江苏省委书记）→ 信长星（2023.01接任）。吴政隆晋升国务委员","overlap_org":"中共江苏省委员会","overlap_period":"不重叠（前后任）"},
    {"id":3,"person_a":17,"person_b":16,"type":"前后任","context":"娄勤俭（2017-2021江苏省委书记）→ 吴政隆（2021.10接任）","overlap_org":"中共江苏省委员会","overlap_period":"不重叠（前后任）"},
    {"id":4,"person_a":18,"person_b":17,"type":"前后任","context":"李强（2016-2017江苏省委书记）→ 娄勤俭（2017.10接任）。李强调任中央","overlap_org":"中共江苏省委员会","overlap_period":"不重叠（前后任）"},

    # ── 省长接班人 ──
    {"id":5,"person_a":19,"person_b":2,"type":"前后任","context":"许昆林（2021-2025江苏省长）→ 刘小涛（2025.01接任）。许昆林调任辽宁省委书记","overlap_org":"江苏省人民政府","overlap_period":"不重叠（前后任）"},
    {"id":6,"person_a":20,"person_b":19,"type":"前后任","context":"石泰峰（2015-2017省长）→ 吴政隆（2017接任省长）→ 许昆林（2021接任省长）","overlap_org":"江苏省人民政府","overlap_period":"不重叠（前后任）"},

    # ── 省长→书记 晋升 ──
    {"id":7,"person_a":16,"person_b":20,"type":"省长→书记","context":"吴政隆（省长→省委书记）。省内在省长任上约4年半，后接任省委书记","overlap_org":"江苏省","overlap_period":"2017-2021"},
    {"id":8,"person_a":19,"person_b":2,"type":"前后任市长","context":"许昆林与刘小涛先后担任苏州市委书记，延续苏州书记→省长的政治管道","overlap_org":"苏州市","overlap_period":"不重叠（前后任）"},

    # ── 苏州书记→省长 管道 ──
    {"id":9,"person_a":20,"person_b":19,"type":"前后任苏州书记","context":"石泰峰（2014-2015苏州书记→省长）→ 许昆林（2020-2021苏州书记→省长）→ 刘小涛（2023-2025苏州书记→省长），苏州书记升任省长的传统","overlap_org":"苏州市","overlap_period":"不重叠（前后任）"},

    # ── 跨省交流网络 ──
    {"id":10,"person_a":2,"person_b":1,"type":"跨省交流","context":"刘小涛（粤→浙→苏）历经广东、浙江、江苏三省交流","overlap_org":"广东/浙江/江苏","overlap_period":"2023至今"},
    {"id":11,"person_a":4,"person_b":42,"type":"跨省交流","context":"周红波（桂→琼→苏）从广西→海南→江苏，三省份跨省交流","overlap_org":"广西/海南/江苏","overlap_period":"2024-12至今"},
    {"id":12,"person_a":5,"person_b":39,"type":"跨省交流","context":"刘建洋（赣→闽→苏）从江西→福建→江苏，三省份跨省交流","overlap_org":"江西/福建/江苏","overlap_period":"2022-12至今"},
    {"id":13,"person_a":8,"person_b":50,"type":"跨省交流","context":"范波（川→鲁→苏）从四川→山东→江苏，三省份跨省交流","overlap_org":"四川/山东/江苏","overlap_period":"2025至今"},

    # ── 央地交流 ──
    {"id":14,"person_a":1,"person_b":21,"type":"央地交流","context":"信长星在劳动系统（国家部委）工作约24年（1986-2010），后转赴地方任职（安徽→青海→江苏），典型的央地交流干部","overlap_org":"中央部委/地方","overlap_period":"1986-2023"},
    {"id":15,"person_a":6,"person_b":32,"type":"央地交流","context":"马欣在国开行系统工作26年，从国开行副行长调任江苏省副省长，典型的金融央企→地方政府交流","overlap_org":"国开行/江苏","overlap_period":"2020至今"},

    # ── 中组部/纪检系统 ──
    {"id":16,"person_a":3,"person_b":20,"type":"纪检系统","context":"张忠在中组部工作多年，后任吉林纪委书记→江苏纪委书记，中组部→地方纪委的交流路径","overlap_org":"中央/吉林/江苏","overlap_period":"2019至今"},

    # ── 江苏→中央外流 ──
    {"id":17,"person_a":18,"person_b":14,"type":"地方→中央","context":"李强从江苏省委书记晋升国务院总理（正国级）","overlap_org":"江苏/中央","overlap_period":"2017-2023"},
    {"id":18,"person_a":16,"person_b":15,"type":"地方→中央","context":"吴政隆从江苏省委书记晋升国务委员、国务院秘书长（副国级）","overlap_org":"江苏/中央","overlap_period":"2022-2023"},
    {"id":19,"person_a":20,"person_b":16,"type":"地方→中央","context":"石泰峰从江苏省省长升任政治局委员、中央组织部部长","overlap_org":"江苏/中央","overlap_period":"2017-2023"},

    # ── 省委常委会关系 ──
    {"id":20,"person_a":6,"person_b":1,"type":"省委班子搭档","context":"马欣（常务副省长，国开行系统）与信长星（劳动部系统）共同构成江苏经济管理班子","overlap_org":"江苏省","overlap_period":"2023至今"},
    {"id":21,"person_a":9,"person_b":1,"type":"省委班子搭档","context":"徐缨（宣传部长，江苏本土成长）与信长星（外省调任）的搭配","overlap_org":"江苏省","overlap_period":"2024至今"},
    {"id":22,"person_a":10,"person_b":51,"type":"政法系统","context":"李耀光（政法委书记）长期在北京政法系统工作，后调任江苏","overlap_org":"北京/江苏","overlap_period":"2022至今"},
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
    if "省委书记" in post:
        return "200,30,30"  # deep red for party secretary
    if "省长" in post:
        return "30,80,200"  # deep blue for governor
    if "省委副书记" in post:
        return "220,60,60"  # red for deputy party secretary
    if "常务副省长" in post or "副省长" in post:
        return "60,120,220"  # blue for vice governor
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"  # orange for discipline
    if "组织部长" in post or "统战部长" in post or "宣传部长" in post or "政法委" in post:
        return "180,90,180"  # purple for party department heads
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
lines.append('    <description>江苏省（省级）领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["省委书记","省长","省委副书记"]) else "12.0"
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
