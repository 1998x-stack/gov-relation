#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Jiangxi Province (江西省) leadership network.

Covers: Provincial Party Secretary (省委书记), Governor (省长), predecessors,
succession chains, key deputy leaders (省委副书记, 常务副省长, 纪委书记, 组织部长等),
and the provincial-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/jiangxi_province_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/jiangxi_province_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 尹弘 — 江西省委书记 (as of 2022.12)
    {"id":1,"name":"尹弘","gender":"男","ethnicity":"汉族","birth":"1963-06","birthplace":"浙江湖州","education":"上海工业大学工学学士、上海交通大学法学学士","party_join":"1985-07","work_start":"1985-07","current_post":"江西省委书记、省人大常委会主任","current_org":"中共江西省委员会","source":"https://baike.baidu.com/item/%E5%B0%B9%E5%BC%98/23641479"},
    # 叶建春 — 江西省省长
    {"id":2,"name":"叶建春","gender":"男","ethnicity":"汉族","birth":"1965-07","birthplace":"福建周宁","education":"华东水利学院（河海大学）陆地水文专业","party_join":"1985-12","work_start":"1984-08","current_post":"江西省委副书记、省长","current_org":"江西省人民政府","source":"https://baike.baidu.com/item/%E5%8F%B6%E5%BB%BA%E6%98%A5/64860029"},

    # ── Provincial leadership (省委常委会成员) ──
    {"id":3,"name":"陈永奇","gender":"男","ethnicity":"汉族","birth":"1967-11","birthplace":"山西怀仁","education":"山西师范大学理学学士、东北财经大学经济学博士","party_join":"1992-03","work_start":"1989-07","current_post":"江西省委副书记","current_org":"中共江西省委员会","source":"https://baike.baidu.com/item/%E9%99%88%E6%B0%B8%E5%A5%87/25832406"},
    {"id":4,"name":"梁桂","gender":"男","ethnicity":"汉族","birth":"1964-12","birthplace":"安徽合肥","education":"中国协和医科大学博士（生物化学）、复旦大学经济学博士后","party_join":"1993-06","work_start":"1984-07","current_post":"江西省委常委、常务副省长","current_org":"江西省人民政府","source":"https://baike.baidu.com/item/%E6%A2%81%E6%A1%82/10768941"},
    {"id":5,"name":"马森述","gender":"男","ethnicity":"汉族","birth":"1966-10","birthplace":"山东乳山","education":"吉林大学法学院法学硕士","party_join":"中共党员","work_start":"1991-03","current_post":"江西省委常委、省纪委书记、省监委主任","current_org":"中共江西省纪律检查委员会","source":"https://baike.baidu.com/item/%E9%A9%AC%E6%A3%AE%E8%BF%B0/55861036"},
    {"id":6,"name":"吴浩","gender":"男","ethnicity":"汉族","birth":"1972-02","birthplace":"河南南阳","education":"教授级高级工程师，博士","party_join":"2003-07","work_start":"1994-07","current_post":"江西省委常委、省委组织部部长","current_org":"中共江西省委员会","source":"https://baike.baidu.com/item/%E5%90%B4%E6%B5%A9/19782192"},
    {"id":7,"name":"庄兆林","gender":"男","ethnicity":"汉族","birth":"1969-02","birthplace":"江苏扬州","education":"省委党校研究生","party_join":"1990-08","work_start":"1987-08","current_post":"江西省委常委、省委宣传部部长","current_org":"中共江西省委员会","source":"https://baike.baidu.com/item/%E5%BA%84%E5%85%86%E6%9E%97/58534834"},
    {"id":8,"name":"黃喜忠","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"广东揭阳","education":"华南师范大学","party_join":"1992-06","work_start":"1993-07","current_post":"江西省委常委、省委统战部部长","current_org":"中共江西省委员会","source":"https://baike.baidu.com/item/%E9%BB%84%E5%96%9C%E5%BF%A0/23381763"},
    {"id":9,"name":"罗小云","gender":"男","ethnicity":"汉族","birth":"1965-05","birthplace":"江西吉水","education":"武汉水利电力学院","party_join":"1996-06","work_start":"1986-08","current_post":"江西省委常委、省委政法委书记","current_org":"中共江西省委员会","source":"https://baike.baidu.com/item/%E7%BD%97%E5%B0%8F%E4%BA%91/24419842"},
    {"id":10,"name":"任珠峰","gender":"男","ethnicity":"汉族","birth":"1970-09","birthplace":"四川剑阁","education":"中央财经大学经济学学士、博士生","party_join":"1993-02","work_start":"1991-06","current_post":"江西省委常委、副省长","current_org":"江西省人民政府","source":"https://baike.baidu.com/item/%E4%BB%BB%E7%8F%A0%E5%B3%B0/58941986"},
    {"id":11,"name":"鲍泽敏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"江西省委常委、省军区政委","current_org":"江西省军区","source":"https://www.jiangxi.gov.cn"},

    # ── Other vice governors (副省长) ──
    {"id":12,"name":"孙洪山","gender":"男","ethnicity":"汉族","birth":"1968-01","birthplace":"山东昌邑","education":"中国刑警学院","party_join":"中共党员","work_start":"1990-08","current_post":"江西省副省长、省公安厅厅长","current_org":"江西省人民政府","source":"https://baike.baidu.com/item/%E5%AD%99%E6%B4%AA%E5%B1%B1/63171353"},
    {"id":13,"name":"史可","gender":"男","ethnicity":"汉族","birth":"1968-01","birthplace":"","education":"研究生","party_join":"农工党","work_start":"","current_post":"江西省副省长","current_org":"江西省人民政府","source":"https://baike.baidu.com/item/%E5%8F%B2%E5%8F%AF"},
    {"id":14,"name":"夏文勇","gender":"男","ethnicity":"汉族","birth":"1972-11","birthplace":"江西永新","education":"北京科技大学工学博士","party_join":"2001-08","work_start":"1996-08","current_post":"江西省副省长","current_org":"江西省人民政府","source":"https://baike.baidu.com/item/%E5%A4%8F%E6%96%87%E5%8B%87/62001011"},
    {"id":15,"name":"万广明","gender":"男","ethnicity":"汉族","birth":"1967-01","birthplace":"江西余干","education":"研究生，工学硕士","party_join":"中共党员","work_start":"","current_post":"江西省副省长","current_org":"江西省人民政府","source":"https://www.wikidata.org/wiki/Q111693436"},

    # ── 省人大 / 省政协 ──
    {"id":16,"name":"唐一军","gender":"男","ethnicity":"汉族","birth":"1961-03","birthplace":"山东莒县","education":"中央党校研究生","party_join":"1985-10","work_start":"1977-07","current_post":"江西省政协党组书记、主席","current_org":"政协江西省委员会","source":"https://baike.baidu.com/item/%E5%94%90%E4%B8%80%E5%86%9B/9123016"},

    # ── Predecessors — 省委书记 ──
    {"id":17,"name":"易炼红","gender":"男","ethnicity":"汉族","birth":"1959-09","birthplace":"湖南涟源","education":"湖南师范大学经济学硕士","party_join":"1985-06","work_start":"1976-08","current_post":"（原江西省委书记，已调浙江省委书记）","current_org":"","source":"https://baike.baidu.com/item/%E6%98%93%E7%82%BC%E7%BA%A2/16202426"},
    {"id":18,"name":"刘奇","gender":"男","ethnicity":"汉族","birth":"1957-09","birthplace":"山东沂水","education":"西安交通大学在职研究生、工学博士","party_join":"1976-10","work_start":"1974-03","current_post":"（原江西省委书记，已离任）","current_org":"","source":"https://baike.baidu.com/item/%E5%88%98%E5%A5%87/20887216"},
    {"id":19,"name":"鹿心社","gender":"男","ethnicity":"汉族","birth":"1956-11","birthplace":"山东巨野","education":"武汉水利电力学院农田水利工程专业","party_join":"1985-07","work_start":"1982-08","current_post":"（原江西省委书记，已离任）","current_org":"","source":"https://baike.baidu.com/item/%E9%B9%BF%E5%BF%83%E7%A4%BE/11002596"},
    {"id":20,"name":"强卫","gender":"男","ethnicity":"汉族","birth":"1953-03","birthplace":"江苏无锡","education":"中国科技大学","party_join":"1975-03","work_start":"1969-01","current_post":"（原江西省委书记，已离任）","current_org":"","source":"https://baike.baidu.com/item/%E5%BC%BA%E5%8D%AB/10859546"},

    # ── Predecessors — 省长 ──
    {"id":21,"name":"毛伟明","gender":"男","ethnicity":"汉族","birth":"1961-05","birthplace":"浙江衢州","education":"浙江大学","party_join":"1985-09","work_start":"1982-08","current_post":"湖南省委副书记、省长（原江西省长）","current_org":"湖南省人民政府","source":"https://baike.baidu.com/item/%E6%AF%9B%E4%BC%9F%E6%98%8E/19245811"},
    {"id":22,"name":"易炼红","gender":"男","ethnicity":"汉族","birth":"1959-09","birthplace":"湖南涟源","education":"湖南师范大学经济学硕士","party_join":"1985-06","work_start":"1976-08","current_post":"（原江西省长，后任省委书记）","current_org":"","source":"https://baike.baidu.com/item/%E6%98%93%E7%82%BC%E7%BA%A2/16202426"},
    {"id":23,"name":"刘奇","gender":"男","ethnicity":"汉族","birth":"1957-09","birthplace":"山东沂水","education":"西安交通大学在职研究生、工学博士","party_join":"1976-10","work_start":"1974-03","current_post":"（原江西省长，后任省委书记）","current_org":"","source":"https://baike.baidu.com/item/%E5%88%98%E5%A5%87/20887216"},

    # ── Key provincial leaders — former ──
    {"id":24,"name":"李红军","gender":"男","ethnicity":"汉族","birth":"1965-09","birthplace":"湖北当阳","education":"华中师范大学","party_join":"1986-10","work_start":"1987-06","current_post":"（原江西省委常委、南昌市委书记，已调任）","current_org":"","source":"https://baike.baidu.com/item/%E6%9D%8E%E7%BA%A2%E5%86%9B/42024554"},
    {"id":25,"name":"殷美根","gender":"男","ethnicity":"汉族","birth":"1963-08","birthplace":"江西南昌","education":"省委党校研究生","party_join":"1985-05","work_start":"1985-07","current_post":"（原江西省委常委、常务副省长，2023年被查）","current_org":"","source":"https://baike.baidu.com/item/%E6%AE%B7%E7%BE%8E%E6%A0%B9/10923755"},
    {"id":26,"name":"张鸿星","gender":"男","ethnicity":"汉族","birth":"1967-08","birthplace":"江西婺源","education":"中央党校大学","party_join":"1992-05","work_start":"1985-08","current_post":"（原江西省委常委、省委政法委书记，已调任）","current_org":"","source":"https://baike.baidu.com/item/%E5%BC%A0%E9%B8%BF%E6%98%9F/24860039"},
    {"id":27,"name":"赵力平","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"（原江西省委常委、组织部部长）","current_org":"","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":2,"name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":3,"name":"江西省人大常委会","type":"人大","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":4,"name":"政协江西省委员会","type":"政协","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":5,"name":"中共江西省纪律检查委员会","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":6,"name":"江西省军区","type":"党委","level":"省级","parent":"中央军委","location":"江西省南昌市"},

    # Key provincial departments
    {"id":7,"name":"江西省公安厅","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":8,"name":"中共江西省委组织部","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":9,"name":"中共江西省委宣传部","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":10,"name":"中共江西省委统战部","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":11,"name":"中共江西省委政法委","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},

    # Other provinces (for predecessor info)
    {"id":12,"name":"中共浙江省委员会","type":"党委","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":13,"name":"浙江省人民政府","type":"政府","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":14,"name":"中共河南省委员会","type":"党委","level":"省级","parent":"","location":"河南省郑州市"},
    {"id":15,"name":"中共上海市委员会","type":"党委","level":"省级","parent":"","location":"上海市"},
    {"id":16,"name":"中共湖南省委员会","type":"党委","level":"省级","parent":"","location":"湖南省长沙市"},
    {"id":17,"name":"湖南省人民政府","type":"政府","level":"省级","parent":"","location":"湖南省长沙市"},
    {"id":18,"name":"中共陕西省委员会","type":"党委","level":"省级","parent":"","location":"陕西省西安市"},
    {"id":19,"name":"中共甘肃省委员会","type":"党委","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":20,"name":"中共青海省委员会","type":"党委","level":"省级","parent":"","location":"青海省西宁市"},
    {"id":21,"name":"国家国防科技工业局","type":"政府","level":"国家级","parent":"中华人民共和国工业和信息化部","location":"北京市"},

    # 尹弘 earlier work units
    {"id":22,"name":"上海工业大学","type":"事业单位","level":"","parent":"","location":"上海市"},
    {"id":23,"name":"中共上海市委办公厅","type":"党委","level":"省级","parent":"中共上海市委员会","location":"上海市"},
    {"id":24,"name":"上海市长宁区","type":"政府","level":"区级","parent":"上海市人民政府","location":"上海市长宁区"},
    {"id":25,"name":"上海市闸北区","type":"政府","level":"区级","parent":"上海市人民政府","location":"上海市闸北区"},
    {"id":26,"name":"上海市援藏干部联络组","type":"事业单位","level":"","parent":"上海市人民政府","location":"西藏自治区"},
    {"id":27,"name":"中共上海市委","type":"党委","level":"省级","parent":"","location":"上海市"},
    {"id":28,"name":"上海市人民政府","type":"政府","level":"省级","parent":"","location":"上海市"},
    {"id":29,"name":"上海第二工业大学","type":"事业单位","level":"","parent":"","location":"上海市"},

    # 叶建春 earlier work units
    {"id":30,"name":"水利部太湖流域管理局","type":"事业单位","level":"国家级","parent":"水利部","location":"上海市"},
    {"id":31,"name":"水利部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":32,"name":"水利部财务司","type":"政府","level":"国家级","parent":"水利部","location":"北京市"},

    # 梁桂 earlier
    {"id":33,"name":"复旦大学","type":"事业单位","level":"","parent":"","location":"上海市"},
    {"id":34,"name":"上海浦东新区科技局","type":"政府","level":"区级","parent":"上海市浦东新区人民政府","location":"上海市浦东新区"},
    {"id":35,"name":"国家科学技术部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":36,"name":"中共陕西省委宣传部","type":"党委","level":"省级","parent":"中共陕西省委员会","location":"陕西省西安市"},
    {"id":37,"name":"中共咸阳市委","type":"党委","level":"地级","parent":"中共陕西省委员会","location":"陕西省咸阳市"},

    # 马森述 earlier
    {"id":38,"name":"国务院法制办","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":39,"name":"中央纪委国家监委","type":"党委","level":"国家级","parent":"","location":"北京市"},

    # 吴浩 earlier
    {"id":40,"name":"河南省交通运输厅","type":"政府","level":"省级","parent":"河南省人民政府","location":"河南省郑州市"},
    {"id":41,"name":"河南省公路局","type":"事业单位","level":"省级","parent":"河南省交通运输厅","location":"河南省郑州市"},

    # 任珠峰 earlier
    {"id":42,"name":"中国五矿集团公司","type":"事业单位","level":"国家级","parent":"国务院国资委","location":"北京市"},

    # 黄喜忠 earlier
    {"id":43,"name":"中共佛山市委员会","type":"党委","level":"地级","parent":"中共广东省委员会","location":"广东省佛山市"},

    # 庄兆林 earlier
    {"id":44,"name":"中共徐州市委","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省徐州市"},
    {"id":45,"name":"中共铜陵市委","type":"党委","level":"地级","parent":"中共安徽省委员会","location":"安徽省铜陵市"},

    # 夏文勇 earlier
    {"id":46,"name":"新余钢铁集团","type":"事业单位","level":"","parent":"江西省国资委","location":"江西省新余市"},

    # 唐一军 earlier
    {"id":47,"name":"中共宁波市委","type":"党委","level":"副省级","parent":"中共浙江省委员会","location":"浙江省宁波市"},
    {"id":48,"name":"浙江省政协","type":"政协","level":"省级","parent":"","location":"浙江省杭州市"},
    {"id":49,"name":"辽宁省人民政府","type":"政府","level":"省级","parent":"","location":"辽宁省沈阳市"},
    {"id":50,"name":"司法部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},

    # City-level relevant
    {"id":51,"name":"中共南昌市委员会","type":"党委","level":"副省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":52,"name":"中共赣州市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省赣州市"},
    {"id":53,"name":"江西省发展和改革委员会","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":54,"name":"江西省财政厅","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 尹弘 ──
    {"id":1,"person_id":1,"org_id":1,"title":"江西省委书记、省人大常委会主任","start":"2022-12","end":"","rank":"正部级","note":"2022.12从上海市市长调任江西省委书记；2023.01兼任省人大常委会主任"},
    {"id":2,"person_id":1,"org_id":28,"title":"上海市市长","start":"2021-10","end":"2022-12","rank":"正部级","note":"2021.10任代市长，2022.01正式当选上海市市长"},
    {"id":3,"person_id":1,"org_id":27,"title":"上海市委副书记、政法委书记","start":"2019-12","end":"2021-10","rank":"副部级","note":"2019.12任上海市委副书记；2020.02兼任政法委书记"},
    {"id":4,"person_id":1,"org_id":14,"title":"河南省委副书记","start":"2019-04","end":"2019-12","rank":"副部级","note":"约8个月"},
    {"id":5,"person_id":1,"org_id":14,"title":"河南省委常委、省委秘书长","start":"2017-03","end":"2019-04","rank":"副部级","note":"此前任河南省委组织部常务副部长（正厅级）"},
    {"id":6,"person_id":1,"org_id":24,"title":"上海市长宁区委书记","start":"2012-05","end":"2017-03","rank":"正厅级","note":"任职近5年"},
    {"id":7,"person_id":1,"org_id":25,"title":"上海市闸北区委副书记、区长","start":"2007-07","end":"2012-05","rank":"正厅级","note":""},
    {"id":8,"person_id":1,"org_id":26,"title":"上海市援藏干部联络组组长","start":"2004-06","end":"2007-03","rank":"副厅级","note":"援藏任西藏日喀则地区行署副专员"},
    {"id":9,"person_id":1,"org_id":23,"title":"上海市委办公厅副主任","start":"2001-07","end":"2004-06","rank":"副厅级","note":""},
    {"id":10,"person_id":1,"org_id":29,"title":"上海第二工业大学党委副书记、副校长","start":"1999-03","end":"2001-07","rank":"正处级","note":""},
    {"id":11,"person_id":1,"org_id":22,"title":"上海工业大学团委书记","start":"1994-05","end":"1999-03","rank":"正处级","note":"1985年留校工作，历任团委副书记、书记等职"},

    # ── 叶建春 ──
    {"id":12,"person_id":2,"org_id":2,"title":"江西省委副书记、省长","start":"2021-10","end":"","rank":"正部级","note":"2021.10任代省长；2022.01正式当选省长"},
    {"id":13,"person_id":2,"org_id":1,"title":"江西省委副书记","start":"2021-02","end":"2021-10","rank":"副部级","note":"2021.02任省委副书记约8个月后接任省长"},
    {"id":14,"person_id":2,"org_id":31,"title":"水利部副部长、党组成员","start":"2017-08","end":"2021-02","rank":"副部级","note":"兼应急管理部副部长（2018年后）"},
    {"id":15,"person_id":2,"org_id":31,"title":"水利部总规划师","start":"2016-06","end":"2017-08","rank":"正厅级","note":""},
    {"id":16,"person_id":2,"org_id":31,"title":"水利部规划计划司司长","start":"2015-05","end":"2016-06","rank":"正厅级","note":""},
    {"id":17,"person_id":2,"org_id":30,"title":"水利部太湖流域管理局局长、党组书记","start":"2011-07","end":"2015-05","rank":"正厅级","note":""},
    {"id":18,"person_id":2,"org_id":30,"title":"水利部太湖流域管理局副局长","start":"2005-06","end":"2011-07","rank":"副厅级","note":"1984年参加工作，在太湖局从技术员逐步晋升"},
    {"id":19,"person_id":2,"org_id":30,"title":"水利部太湖流域管理局工作","start":"1984-08","end":"2005-06","rank":"技术员→副处长→处长","note":"华东水利学院（河海大学）毕业即分配到太湖局"},

    # ── 陈永奇 ──
    {"id":20,"person_id":3,"org_id":1,"title":"江西省委副书记","start":"2024-10","end":"","rank":"副部级","note":"从西藏调任江西，跨省交流干部"},
    {"id":21,"person_id":3,"org_id":20,"title":"西藏自治区党委常委、组织部部长","start":"2021-01","end":"2024-10","rank":"副部级","note":"后任西藏自治区党委副书记、自治区政府常务副主席"},
    {"id":22,"person_id":3,"org_id":19,"title":"甘肃省副省长","start":"2018-01","end":"2021-01","rank":"副部级","note":"从山西调任甘肃"},
    {"id":23,"person_id":3,"org_id":18,"title":"山西省阳泉市委书记","start":"2015-11","end":"2018-01","rank":"正厅级","note":""},
    {"id":24,"person_id":3,"org_id":18,"title":"山西省政府副秘书长、省政府办公厅主任","start":"2013-02","end":"2015-11","rank":"正厅级","note":""},

    # ── 梁桂 ──
    {"id":25,"person_id":4,"org_id":2,"title":"江西省委常委、常务副省长","start":"2021-09","end":"","rank":"副部级","note":"2021.09任省委常委，2022.06任常务副省长"},
    {"id":26,"person_id":4,"org_id":36,"title":"陕西省委常委、宣传部部长","start":"2020-03","end":"2021-09","rank":"副部级","note":""},
    {"id":27,"person_id":4,"org_id":37,"title":"咸阳市委书记","start":"2016-12","end":"2020-03","rank":"正厅级","note":""},
    {"id":28,"person_id":4,"org_id":34,"title":"上海市浦东新区副区长、张江高科技园区管委会主任","start":"2010-01","end":"2012-02","rank":"副厅级","note":""},
    {"id":29,"person_id":4,"org_id":33,"title":"复旦大学党委副书记","start":"2006-01","end":"2010-01","rank":"正处级","note":""},

    # ── 马森述 ──
    {"id":30,"person_id":5,"org_id":5,"title":"江西省委常委、省纪委书记、省监委主任","start":"2021-11","end":"","rank":"副部级","note":"2021.11任命"},
    {"id":31,"person_id":5,"org_id":39,"title":"中央纪委国家监委副部级巡视专员","start":"2019-05","end":"2021-11","rank":"副部级","note":"此前任中央纪委国家监委法规室主任"},
    {"id":32,"person_id":5,"org_id":38,"title":"国务院法制办","start":"1991-03","end":"2018-02","rank":"","note":"从法制办到中纪委，长期从事法规工作"},

    # ── 吴浩 ──
    {"id":33,"person_id":6,"org_id":8,"title":"江西省委常委、组织部部长","start":"2021-12","end":"","rank":"副部级","note":"原江西省委常委、省委秘书长"},
    {"id":34,"person_id":6,"org_id":1,"title":"江西省委常委、省委秘书长","start":"2021-05","end":"2021-12","rank":"副部级","note":"2021.05晋升省委常委"},
    {"id":35,"person_id":6,"org_id":40,"title":"河南省副省长","start":"2020-07","end":"2021-05","rank":"副部级","note":""},
    {"id":36,"person_id":6,"org_id":41,"title":"河南省交通运输厅党组书记、厅长","start":"2017-11","end":"2020-07","rank":"正厅级","note":""},
    {"id":37,"person_id":6,"org_id":41,"title":"河南省交通运输厅副厅长","start":"2015-08","end":"2017-11","rank":"副厅级","note":""},

    # ── 庄兆林 ──
    {"id":38,"person_id":7,"org_id":9,"title":"江西省委常委、宣传部部长","start":"2021-11","end":"","rank":"副部级","note":"从江苏调任江西"},
    {"id":39,"person_id":7,"org_id":44,"title":"徐州市委书记","start":"2021-07","end":"2021-11","rank":"正厅级","note":"约4个月"},
    {"id":40,"person_id":7,"org_id":45,"title":"铜陵市委书记","start":"2018-04","end":"2021-07","rank":"正厅级","note":"从江苏省调任安徽省铜陵市委书记（跨省交流）"},
    {"id":41,"person_id":7,"org_id":44,"title":"徐州市委副书记、市长","start":"2015-12","end":"2018-04","rank":"正厅级","note":""},

    # ── 黄喜忠 ──
    {"id":42,"person_id":8,"org_id":10,"title":"江西省委常委、统战部部长","start":"2023-06","end":"","rank":"副部级","note":""},
    {"id":43,"person_id":8,"org_id":51,"title":"南昌市委副书记、市长","start":"2019-12","end":"2021-02","rank":"副省级","note":"约1年"},
    {"id":44,"person_id":8,"org_id":43,"title":"佛山市市长（广东）","start":"2018-03","end":"2019-12","rank":"正厅级","note":"跨省交流到江西前"},
    {"id":45,"person_id":8,"org_id":43,"title":"佛山市委常委、统战部部长","start":"2016-12","end":"2018-03","rank":"副厅级","note":""},

    # ── 罗小云 ──
    {"id":46,"person_id":9,"org_id":11,"title":"江西省委常委、政法委书记","start":"2022-06","end":"","rank":"副部级","note":"从江西省副省长升任"},
    {"id":47,"person_id":9,"org_id":2,"title":"江西省副省长","start":"2020-06","end":"2022-06","rank":"副部级","note":"分管水利等"},
    {"id":48,"person_id":9,"org_id":53,"title":"江西省水利厅厅长","start":"2015-05","end":"2020-06","rank":"正厅级","note":"在江西水利系统工作30年"},

    # ── 任珠峰 ──
    {"id":49,"person_id":10,"org_id":2,"title":"江西省委常委、副省长","start":"2022-05","end":"","rank":"副部级","note":"2021.03任副省长，2022.05任省委常委"},
    {"id":50,"person_id":10,"org_id":42,"title":"中国五矿集团副总经理","start":"~2019","end":"2021-03","rank":"副部级央企副职","note":""},
    {"id":51,"person_id":10,"org_id":42,"title":"中国五矿集团总经理助理","start":"~2015","end":"~2019","rank":"正厅级央企","note":""},

    # ── 鲍泽敏 ──
    {"id":52,"person_id":11,"org_id":6,"title":"江西省委常委、省军区政委","start":"~2021","end":"","rank":"副部级","note":"少将军衔"},

    # ── 孙洪山 ──
    {"id":53,"person_id":12,"org_id":7,"title":"江西省副省长、省公安厅厅长","start":"2022-05","end":"","rank":"副部级","note":""},
    {"id":54,"person_id":12,"org_id":2,"title":"江西省副省长","start":"2021-04","end":"2022-05","rank":"副部级","note":""},

    # ── 夏文勇 ──
    {"id":55,"person_id":14,"org_id":2,"title":"江西省副省长","start":"2023-01","end":"","rank":"副部级","note":""},
    {"id":56,"person_id":14,"org_id":46,"title":"新余钢铁集团董事长","start":"~2016","end":"2023-01","rank":"正厅级","note":"江西省属重点国企"},

    # ── 万广明 ──
    {"id":57,"person_id":15,"org_id":2,"title":"江西省副省长","start":"~2025-02","end":"","rank":"副省级","note":"从南昌市长晋升"},
    {"id":58,"person_id":15,"org_id":51,"title":"南昌市委副书记、市长","start":"2021-03","end":"~2025-02","rank":"副省级","note":""},
    {"id":59,"person_id":15,"org_id":54,"title":"江西省财政厅厅长","start":"~2019","end":"2021-03","rank":"正厅级","note":""},

    # ── 唐一军 ──
    {"id":60,"person_id":16,"org_id":50,"title":"司法部部长、党组书记","start":"2020-04","end":"2023-02","rank":"正部级","note":""},
    {"id":61,"person_id":16,"org_id":49,"title":"辽宁省省长","start":"2018-01","end":"2020-04","rank":"正部级","note":"从浙江调任辽宁"},
    {"id":62,"person_id":16,"org_id":48,"title":"浙江省政协主席","start":"2016-01","end":"2018-01","rank":"正部级","note":""},
    {"id":63,"person_id":16,"org_id":4,"title":"江西省政协党组书记、主席","start":"2023-03","end":"","rank":"正部级","note":"2023.03任命"},
    {"id":64,"person_id":16,"org_id":47,"title":"宁波市政协主席","start":"2011-02","end":"2016-01","rank":"副部级","note":""},

    # ── Predecessors — 省委书记 ──
    {"id":65,"person_id":17,"org_id":12,"title":"浙江省委书记","start":"2022-12","end":"","rank":"正部级","note":"2022.12从江西调任浙江"},
    {"id":66,"person_id":17,"org_id":1,"title":"江西省委书记","start":"2021-10","end":"2022-12","rank":"正部级","note":"约14个月"},
    {"id":67,"person_id":17,"org_id":2,"title":"江西省省长","start":"2018-10","end":"2021-10","rank":"正部级","note":"后接任省委书记"},
    {"id":68,"person_id":17,"org_id":18,"title":"陕西省委副书记","start":"2015-05","end":"2017-07","rank":"副部级","note":""},
    {"id":69,"person_id":17,"org_id":18,"title":"陕西省委常委、省委秘书长","start":"2013-05","end":"2015-05","rank":"副部级","note":""},

    {"id":70,"person_id":18,"org_id":1,"title":"江西省委书记","start":"2018-03","end":"2021-10","rank":"正部级","note":"约3年半"},
    {"id":71,"person_id":18,"org_id":2,"title":"江西省省长","start":"2016-07","end":"2018-08","rank":"正部级","note":""},

    {"id":72,"person_id":19,"org_id":20,"title":"广西壮族自治区党委书记","start":"2022-01","end":"","rank":"正部级","note":"从江西调任广西"},
    {"id":73,"person_id":19,"org_id":1,"title":"江西省委书记","start":"2016-06","end":"2018-03","rank":"正部级","note":""},
    {"id":74,"person_id":19,"org_id":2,"title":"江西省省长","start":"2011-06","end":"2016-07","rank":"正部级","note":""},

    {"id":75,"person_id":20,"org_id":1,"title":"江西省委书记","start":"2013-03","end":"2016-06","rank":"正部级","note":""},

    # ── Predecessors — 省长 ──
    {"id":76,"person_id":21,"org_id":16,"title":"湖南省委副书记、省长","start":"2021-10","end":"","rank":"正部级","note":"从江西省长调任湖南省长"},
    {"id":77,"person_id":21,"org_id":2,"title":"江西省省长","start":"2020-11","end":"2021-10","rank":"正部级","note":"约11个月"},
    {"id":78,"person_id":21,"org_id":21,"title":"工信部副部长、国防科工局局长","start":"2015-09","end":"2020-11","rank":"副部级","note":""},

    # ── 李红军 ──
    {"id":79,"person_id":24,"org_id":51,"title":"江西省委常委、南昌市委书记","start":"2021-07","end":"2026-06","rank":"副部级","note":"盛秋平接替"},

    # ── 殷美根（被查） ──
    {"id":80,"person_id":25,"org_id":2,"title":"江西省委常委、常务副省长","start":"2020-03","end":"2023-03","rank":"副部级","note":"2023.03被查"},
    {"id":81,"person_id":25,"org_id":51,"title":"江西省委常委、南昌市委书记","start":"2016-11","end":"2020-03","rank":"副部级","note":""},

    # ── 张鸿星 ──
    {"id":82,"person_id":26,"org_id":11,"title":"江西省委常委、政法委书记","start":"2021-12","end":"2022-05","rank":"副部级","note":""},
    {"id":83,"person_id":26,"org_id":52,"title":"赣州市委书记（地级）","start":"~2018","end":"2021-12","rank":"正厅级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 尹弘 ↔ 叶建春（党政搭档） ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"尹弘（省委书记）与叶建春（省长）为江西省党政一把手搭档","overlap_org":"江西省","overlap_period":"2022-12至今"},

    # ── 省委书记接班人 ──
    {"id":2,"person_a":17,"person_b":1,"type":"前后任","context":"易炼红（2021-2022江西省委书记）→ 尹弘（2022.12接任）。易炼红调任浙江省委书记","overlap_org":"中共江西省委员会","overlap_period":"不重叠（前后任）"},
    {"id":3,"person_a":18,"person_b":17,"type":"前后任","context":"刘奇（2018-2021江西省委书记）→ 易炼红（2021.10接任）","overlap_org":"中共江西省委员会","overlap_period":"不重叠（前后任）"},
    {"id":4,"person_a":19,"person_b":18,"type":"前后任","context":"鹿心社（2016-2018江西省委书记）→ 刘奇（2018.03接任）","overlap_org":"中共江西省委员会","overlap_period":"不重叠（前后任）"},

    # ── 省长接班人 ──
    {"id":5,"person_a":21,"person_b":2,"type":"前后任","context":"毛伟明（2020-2021江西省长）→ 叶建春（2021.10接任）。毛伟明调任湖南省长","overlap_org":"江西省人民政府","overlap_period":"不重叠（前后任）"},
    {"id":6,"person_a":17,"person_b":21,"type":"前后任","context":"易炼红（2018-2021省长）→ 毛伟明（2020.11接任省长）","overlap_org":"江西省人民政府","overlap_period":"不重叠（前后任）"},

    # ── 省长→书记 晋升 ──
    {"id":7,"person_a":17,"person_b":18,"type":"省长→书记","context":"易炼红（省长→省委书记）。省内在省长任上约3年，后接任省委书记","overlap_org":"江西省","overlap_period":"2018-2021(省长搭档刘奇书记)"},
    {"id":8,"person_a":18,"person_b":19,"type":"省长→书记","context":"刘奇（省长→省委书记）。鹿心社调任广西后，省长刘奇接任省委书记","overlap_org":"江西省","overlap_period":"2016-2018"},

    # ── 尹弘跨省交流链 ──
    {"id":9,"person_a":1,"person_b":24,"type":"上海系统","context":"尹弘在上海工作37年（1985-2022），从大学团委到上海市长。李红军是尹弘在江西的下属（南昌市委书记）","overlap_org":"江西/上海","overlap_period":"2022-12至今"},

    # ── 叶建春水利部系统 ──
    {"id":10,"person_a":2,"person_b":1,"type":"党政搭档","context":"叶建春（水利系统35年+副部3年）与尹弘（上海37年+河南1年）形成跨系统搭档——水利技术官僚与地方行政官僚的组合","overlap_org":"江西省","overlap_period":"2022-12至今"},

    # ── 省委常委会关系网 ──
    {"id":11,"person_a":4,"person_b":1,"type":"省委班子搭档","context":"梁桂（常务副省长，复旦+浦东背景）与尹弘（上海系统出身）同为在上海有长期工作经历的干部","overlap_org":"江西省","overlap_period":"2021-09至今"},
    {"id":12,"person_a":5,"person_b":39,"type":"中纪委系统","context":"马森述（省纪委书记）长期在中央纪委工作，属中纪委系统空降干部","overlap_org":"中央纪委","overlap_period":"2019-2021"},
    {"id":13,"person_a":6,"person_b":40,"type":"河南系统","context":"吴浩（组织部长）与尹弘均有河南工作经历——尹弘曾任河南省委副书记（2019），吴浩曾任河南省副省长、交通厅长","overlap_org":"河南省","overlap_period":"2017-2021（吴在河南）"},
    {"id":14,"person_a":8,"person_b":43,"type":"广东→江西跨省","context":"黄喜忠（统战部长，佛山市长→南昌市长→江西省委统战部长）是广东系统跨省交流到江西的典型案例","overlap_org":"广东/江西","overlap_period":"2019-12至今"},
    {"id":15,"person_a":7,"person_b":45,"type":"江苏→安徽→江西跨省","context":"庄兆林（宣传部长，徐州→铜陵→江西）经历了苏皖赣三省的跨省交流，路径独特","overlap_org":"江苏/安徽/江西","overlap_period":"2018-2021"},

    # ── 纪委书记链 ──
    {"id":16,"person_a":5,"person_b":25,"type":"前后任纪委书记/被查","context":"殷美根（原省委常委、常务副省长）2023.03被查，是马森述任省纪委书记后的重要落马案件","overlap_org":"江西省","overlap_period":"2021-2023"},

    # ── 唐一军（江西省政协主席） ──
    {"id":17,"person_a":16,"person_b":50,"type":"政法系统→政协","context":"唐一军（司法部长→辽宁省长→江西省政协主席），曾任宁波市政协主席、浙江省委副书记、辽宁省长、司法部长，履历横跨浙辽赣三省及中央政法系统","overlap_org":"全国/浙江/辽宁","overlap_period":"2016-2023"},

    # ── 常务副省长接替 ──
    {"id":18,"person_a":4,"person_b":25,"type":"前后任","context":"梁桂2021.09接替殷美根（2023被查）任常务副省长。殷美根被查后，梁桂正式补位","overlap_org":"江西省人民政府","overlap_period":"2021-09至今"},

    # ── 南昌市委书记接班人 ──
    {"id":19,"person_a":25,"person_b":24,"type":"前后任","context":"殷美根（2016-2020南昌市委书记）→ 李红军（2021-2026南昌市委书记）→ 盛秋平（2026.06任）。殷美根被查（2023）","overlap_org":"南昌市","overlap_period":"不重叠"},

    # ── 夏文勇企业→政府 ──
    {"id":20,"person_a":14,"person_b":46,"type":"国企→政府","context":"夏文勇（副省长）从新余钢铁集团董事长直接晋升江西省副省长，是典型的企业家型干部","overlap_org":"新余钢铁→省政府","overlap_period":"2023-01至今"},

    # ── 外来与本土 ──
    {"id":21,"person_a":9,"person_b":46,"type":"本土干部","context":"罗小云（政法委书记，原省水利厅长）与夏文勇（新余钢铁→副省长）均为江西省内成长的本土干部，与跨省空降的梁桂、庄兆林等人形成对比","overlap_org":"江西省","overlap_period":"2022-06至今"},

    # ── 陈永奇跨省：山西→甘肃→西藏→江西 ──
    {"id":22,"person_a":3,"person_b":20,"type":"跨省交流","context":"陈永奇（江西省委副书记）经历了山西→甘肃→西藏→江西的四省跨省交流路径，履历跨越东中西部","overlap_org":"山西/甘肃/西藏/江西","overlap_period":"2018-2025"},

    # ── 万广明本地晋升链 ──
    {"id":23,"person_a":15,"person_b":54,"type":"本土晋升","context":"万广明（副省长）从江西省财政厅长→南昌市长→江西省副省长，是典型的省级财政系统→地方主官→省级领导的本地晋升路径","overlap_org":"江西省","overlap_period":"~2019-2026"},
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
lines.append('    <description>江西省（省级）领导班子工作关系网络 — 2026年7月14日生成</description>')
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
