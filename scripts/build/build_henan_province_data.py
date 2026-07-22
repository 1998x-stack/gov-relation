#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Henan Province (河南省) leadership network.

Covers: Provincial Party Secretary (省委书记), Governor (省长), predecessors,
succession chains, key deputy leaders (省委常委会成员, 副省长等),
and the provincial-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/henan_province_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/henan_province_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 刘宁 — 河南省委书记 (as of 2024.12)
    {"id":1,"name":"刘宁","gender":"男","ethnicity":"汉族","birth":"1962-01","birthplace":"辽宁丹东（籍贯吉林临江）","education":"清华大学水利系水工结构专业本科、武汉大学管理学硕士/工学博士","party_join":"1990-08","work_start":"1983-07","current_post":"河南省委书记、省人大常委会主任","current_org":"中共河南省委员会","source":"https://zh.wikipedia.org/wiki/%E5%8A%89%E5%AF%A7_(1962%E5%B9%B4)"},
    # 王凯 — 河南省省长
    {"id":2,"name":"王凯","gender":"男","ethnicity":"汉族","birth":"1962-07","birthplace":"河南洛阳","education":"山西大学政治经济学本科、中国人民大学政治经济学硕士、武汉大学经济学博士","party_join":"1984-12","work_start":"1983-10","current_post":"河南省委副书记、省长","current_org":"河南省人民政府","source":"https://en.wikipedia.org/wiki/Wang_Kai_(politician)"},

    # ── Provincial leadership (省委常委会成员) ──
    {"id":3,"name":"张巍","gender":"男","ethnicity":"汉族","birth":"1968-11","birthplace":"湖北松滋","education":"武汉大学、中国人民大学","party_join":"1991","work_start":"","current_post":"河南省委副书记、政法委书记、教育工委书记","current_org":"中共河南省委员会","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%B7%8D_(1968%E5%B9%B4)"},
    {"id":4,"name":"安伟","gender":"男","ethnicity":"汉族","birth":"1966-05","birthplace":"河南镇平","education":"河南大学政治系本科、兰州大学世界近现代史硕士","party_join":"1988-05","work_start":"1991-06","current_post":"河南省委常委、郑州市委书记","current_org":"中共郑州市委员会","source":"https://zh.wikipedia.org/wiki/%E5%AE%89%E4%BC%9F_(%E6%94%BF%E6%B2%BB%E4%BA%BA%E7%89%A9)"},
    {"id":5,"name":"秦国文","gender":"男","ethnicity":"汉族","birth":"1967-07","birthplace":"江西南昌","education":"湘潭矿业学院采矿工程、湖南大学MBA","party_join":"1989","work_start":"1991","current_post":"河南省委常委、省纪委书记、省监委主任","current_org":"中共河南省纪律检查委员会","source":"https://zh.wikipedia.org/wiki/%E7%A7%A6%E5%9B%BD%E6%96%87"},
    {"id":6,"name":"王刚","gender":"男","ethnicity":"汉族","birth":"1969-09","birthplace":"宁夏同心","education":"北京农业大学动物遗传育种专业","party_join":"1994-02","work_start":"1991","current_post":"河南省委常委、组织部部长","current_org":"中共河南省委组织部","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E5%88%9A_(1969%E5%B9%B4)"},
    {"id":7,"name":"张雷明","gender":"男","ethnicity":"汉族","birth":"1966-06","birthplace":"河南淇县","education":"北京农业工程大学（现中国农业大学）","party_join":"1987-04","work_start":"1988-07","current_post":"河南省委常委、统战部部长","current_org":"中共河南省委统战部","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E9%9B%B7%E6%98%8E"},
    {"id":8,"name":"张敏","gender":"女","ethnicity":"汉族","birth":"1970-11","birthplace":"山东齐河","education":"华东工学院、陕西财经学院会计学硕士","party_join":"","work_start":"","current_post":"河南省委常委、常务副省长","current_org":"河南省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E6%95%8F_(1970%E5%B9%B4)"},
    {"id":9,"name":"王崧","gender":"男","ethnicity":"汉族","birth":"1971-02","birthplace":"江西南康（籍贯江西安福）","education":"西安交通大学动力机械工程本科/硕士、清华大学工程热物理博士","party_join":"1990-12","work_start":"2000-05","current_post":"河南省委常委、宣传部部长","current_org":"中共河南省委宣传部","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E5%B4%A7_(1971%E5%B9%B4)"},
    {"id":10,"name":"陈春江","gender":"男","ethnicity":"蒙古族","birth":"1971-05","birthplace":"内蒙古科左中旗","education":"待补充","party_join":"","work_start":"","current_post":"河南省委常委、洛阳市委书记","current_org":"中共洛阳市委员会","source":"https://zh.wikipedia.org/wiki/%E9%99%88%E6%98%A5%E6%B1%9F"},
    {"id":11,"name":"李涛","gender":"男","ethnicity":"汉族","birth":"1970-05","birthplace":"河南邓州","education":"郑州大学微电子技术专业","party_join":"1996-05","work_start":"1993-07","current_post":"河南省委常委、省委秘书长、副省长","current_org":"中共河南省委员会","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%B6%9B_(1970%E5%B9%B4)"},

    # ── Vice Governors (副省长) ──
    {"id":12,"name":"刘玉江","gender":"男","ethnicity":"汉族","birth":"1970s","birthplace":"","education":"","party_join":"","work_start":"","current_post":"河南省副省长","current_org":"河南省人民政府","source":"https://zh.wikipedia.org/wiki/%E6%B2%B3%E5%8D%97%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C"},
    {"id":13,"name":"宋争辉","gender":"男","ethnicity":"汉族","birth":"1966","birthplace":"","education":"","party_join":"","work_start":"","current_post":"河南省副省长","current_org":"河南省人民政府","source":"https://zh.wikipedia.org/wiki/%E6%B2%B3%E5%8D%97%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C"},
    {"id":14,"name":"郑海洋","gender":"男","ethnicity":"汉族","birth":"1968","birthplace":"","education":"","party_join":"","work_start":"","current_post":"河南省副省长、省公安厅厅长","current_org":"河南省公安厅","source":"https://zh.wikipedia.org/wiki/%E6%B2%B3%E5%8D%97%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C"},
    {"id":15,"name":"李酌","gender":"男","ethnicity":"汉族","birth":"1968","birthplace":"","education":"","party_join":"","work_start":"","current_post":"河南省副省长","current_org":"河南省人民政府","source":"https://zh.wikipedia.org/wiki/%E6%B2%B3%E5%8D%97%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C"},
    {"id":16,"name":"吕国范","gender":"男","ethnicity":"汉族","birth":"1960s","birthplace":"","education":"","party_join":"无党派","work_start":"","current_post":"河南省副省长（无党派）","current_org":"河南省人民政府","source":"https://zh.wikipedia.org/wiki/%E6%B2%B3%E5%8D%97%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C"},

    # ── Predecessors — 省委书记 ──
    {"id":17,"name":"楼阳生","gender":"男","ethnicity":"汉族","birth":"1959-10","birthplace":"浙江浦江","education":"浙江师范大学数学系","party_join":"1981-11","work_start":"","current_post":"（原河南省委书记，已卸任）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E6%A5%BC%E9%98%B3%E7%94%9F"},
    {"id":18,"name":"王国生","gender":"男","ethnicity":"汉族","birth":"1956-12","birthplace":"山东东阿","education":"山东大学","party_join":"","work_start":"","current_post":"全国人大社会建设委员会副主任委员（原河南省委书记）","current_org":"全国人大常委会","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E5%9B%BD%E7%94%9F_(1956%E5%B9%B4)"},
    {"id":19,"name":"谢伏瞻","gender":"男","ethnicity":"汉族","birth":"1954-08","birthplace":"湖北天门","education":"华中科技大学、机械工业部","party_join":"","work_start":"","current_post":"原中国社科院院长（原河南省委书记）","current_org":"中国社会科学院","source":"https://zh.wikipedia.org/wiki/%E8%B0%A2%E4%BC%8F%E7%9E%BB"},

    # ── Predecessors — 省长 ──
    {"id":20,"name":"尹弘","gender":"男","ethnicity":"汉族","birth":"1963-06","birthplace":"浙江湖州","education":"上海工业大学工学学士、上海交通大学法学学士","party_join":"","work_start":"","current_post":"江西省委书记（原河南省省长）","current_org":"中共江西省委员会","source":"https://zh.wikipedia.org/wiki/%E5%B0%B9%E5%BC%98"},
    {"id":21,"name":"陈润儿","gender":"男","ethnicity":"汉族","birth":"1957-10","birthplace":"湖南茶陵","education":"","party_join":"","work_start":"","current_post":"全国人大农业农村委员会副主任委员（原河南省省长）","current_org":"全国人大常委会","source":"https://zh.wikipedia.org/wiki/%E9%99%88%E6%B6%A6%E5%84%BF"},

    # ── Key personnel in predecessor/successor chains ──
    {"id":22,"name":"李亚","gender":"男","ethnicity":"汉族","birth":"1963","birthplace":"河南永城","education":"","party_join":"","work_start":"","current_post":"河南省人大常委会副主任、党组书记","current_org":"河南省人大常委会","source":"https://zh.wikipedia.org/wiki/%E6%B2%B3%E5%8D%97%E7%9C%81%E4%BA%BA%E6%B0%91%E4%BB%A3%E8%A1%A8%E5%A4%A7%E4%BC%9A"},
    {"id":23,"name":"孔昌生","gender":"男","ethnicity":"汉族","birth":"1963-02","birthplace":"甘肃静宁","education":"","party_join":"","work_start":"","current_post":"河南省政协主席","current_org":"政协河南省委员会","source":"https://zh.wikipedia.org/wiki/%E5%AD%94%E6%98%8C%E7%94%9F"},

    # ── Cross-province network figures ──
    {"id":24,"name":"信长星","gender":"男","ethnicity":"汉族","birth":"1963-12","birthplace":"山东惠民","education":"","party_join":"","work_start":"","current_post":"江苏省委书记（原青海省省长，刘宁青海继任者）","current_org":"中共江苏省委员会","source":"https://zh.wikipedia.org/wiki/%E4%BF%A1%E9%95%BF%E6%98%9F"},
    {"id":25,"name":"王建军","gender":"男","ethnicity":"汉族","birth":"1958","birthplace":"","education":"","party_join":"","work_start":"","current_post":"原青海省委书记（刘宁青海搭档）","current_org":"","source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E5%BB%BA%E5%86%9B_(1958%E5%B9%B4)"},
    {"id":26,"name":"蓝天立","gender":"男","ethnicity":"壮族","birth":"1962","birthplace":"","education":"","party_join":"","work_start":"","current_post":"广西壮族自治区政府主席（刘宁广西搭档）","current_org":"广西壮族自治区人民政府","source":"https://zh.wikipedia.org/wiki/%E8%93%9D%E5%A4%A9%E7%AB%8B"},
    {"id":27,"name":"金湘军","gender":"男","ethnicity":"汉族","birth":"1964-07","birthplace":"湖南江华","education":"","party_join":"","work_start":"","current_post":"原山西省省长（王凯玉林前任，已调查）","current_org":"","source":"https://en.wikipedia.org/wiki/Jin_Xiangjun"},
    {"id":28,"name":"林武","gender":"男","ethnicity":"汉族","birth":"1962-02","birthplace":"福建闽侯","education":"","party_join":"","work_start":"","current_post":"山东省委书记（王凯吉林组织部长前任）","current_org":"中共山东省委员会","source":"https://en.wikipedia.org/wiki/Lin_Wu"},
    {"id":29,"name":"王晓萍","gender":"女","ethnicity":"汉族","birth":"1964-03","birthplace":"湖北黄冈","education":"","party_join":"","work_start":"","current_post":"人力资源和社会保障部部长（王凯吉林组工继任者）","current_org":"人力资源和社会保障部","source":"https://en.wikipedia.org/wiki/Wang_Xiaoping"},
    {"id":30,"name":"叶建春","gender":"男","ethnicity":"汉族","birth":"1963","birthplace":"","education":"","party_join":"","work_start":"","current_post":"江西省省长（水利部同僚）","current_org":"江西省人民政府","source":"https://zh.wikipedia.org/wiki/%E5%8F%B6%E5%BB%BA%E6%98%A5"},
    {"id":31,"name":"孙守刚","gender":"男","ethnicity":"汉族","birth":"1965","birthplace":"山东利津","education":"","party_join":"","work_start":"","current_post":"河南省人大常委会副主任（原常务副省长）","current_org":"河南省人大常委会","source":"https://zh.wikipedia.org/wiki/%E6%B2%B3%E5%8D%97%E7%9C%81%E4%BA%BA%E6%B0%91%E4%BB%A3%E8%A1%A8%E5%A4%A7%E4%BC%9A"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Henan provincial core
    {"id":1,"name":"中共河南省委员会","type":"党委","level":"省级","parent":"","location":"河南省郑州市"},
    {"id":2,"name":"河南省人民政府","type":"政府","level":"省级","parent":"","location":"河南省郑州市"},
    {"id":3,"name":"河南省人大常委会","type":"人大","level":"省级","parent":"","location":"河南省郑州市"},
    {"id":4,"name":"政协河南省委员会","type":"政协","level":"省级","parent":"","location":"河南省郑州市"},
    {"id":5,"name":"中共河南省纪律检查委员会","type":"党委","level":"省级","parent":"中共河南省委员会","location":"河南省郑州市"},
    {"id":6,"name":"河南省公安厅","type":"政府","level":"省级","parent":"河南省人民政府","location":"河南省郑州市"},

    # Key provincial departments
    {"id":7,"name":"中共河南省委组织部","type":"党委","level":"省级","parent":"中共河南省委员会","location":"河南省郑州市"},
    {"id":8,"name":"中共河南省委宣传部","type":"党委","level":"省级","parent":"中共河南省委员会","location":"河南省郑州市"},
    {"id":9,"name":"中共河南省委统战部","type":"党委","level":"省级","parent":"中共河南省委员会","location":"河南省郑州市"},
    {"id":10,"name":"中共河南省委政法委","type":"党委","level":"省级","parent":"中共河南省委员会","location":"河南省郑州市"},
    {"id":11,"name":"中共郑州市委员会","type":"党委","level":"副省级","parent":"中共河南省委员会","location":"河南省郑州市"},
    {"id":12,"name":"中共洛阳市委员会","type":"党委","level":"地级","parent":"中共河南省委员会","location":"河南省洛阳市"},

    # Central / national orgs
    {"id":13,"name":"全国人大常委会","type":"人大","level":"国家级","parent":"","location":"北京市"},
    {"id":14,"name":"中国社会科学院","type":"事业单位","level":"国家级","parent":"","location":"北京市"},

    # 刘宁 earlier work units
    {"id":15,"name":"水利部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":16,"name":"长江水利委员会","type":"事业单位","level":"国家级","parent":"水利部","location":"湖北省武汉市"},
    {"id":17,"name":"南水北调规划设计管理局","type":"事业单位","level":"国家级","parent":"水利部","location":"北京市"},
    {"id":18,"name":"中共青海省委员会","type":"党委","level":"省级","parent":"","location":"青海省西宁市"},
    {"id":19,"name":"青海省人民政府","type":"政府","level":"省级","parent":"","location":"青海省西宁市"},
    {"id":20,"name":"中共辽宁省委员会","type":"党委","level":"省级","parent":"","location":"辽宁省沈阳市"},
    {"id":21,"name":"辽宁省人民政府","type":"政府","level":"省级","parent":"","location":"辽宁省沈阳市"},
    {"id":22,"name":"中共广西壮族自治区委员会","type":"党委","level":"省级","parent":"","location":"广西壮族自治区南宁市"},
    {"id":23,"name":"广西壮族自治区人民政府","type":"政府","level":"省级","parent":"","location":"广西壮族自治区南宁市"},

    # 王凯 earlier work units
    {"id":24,"name":"中央纪律检查委员会","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":25,"name":"中共梧州市委员会","type":"党委","level":"地级","parent":"中共广西壮族自治区委员会","location":"广西壮族自治区梧州市"},
    {"id":26,"name":"中共玉林市委员会","type":"党委","level":"地级","parent":"中共广西壮族自治区委员会","location":"广西壮族自治区玉林市"},
    {"id":27,"name":"中共吉林省委员会","type":"党委","level":"省级","parent":"","location":"吉林省长春市"},
    {"id":28,"name":"中共长春市委员会","type":"党委","level":"副省级","parent":"中共吉林省委员会","location":"吉林省长春市"},

    # Cross-province orgs
    {"id":29,"name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":30,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":31,"name":"中共山东省委员会","type":"党委","level":"省级","parent":"","location":"山东省济南市"},
    {"id":32,"name":"中共山西省委员会","type":"党委","level":"省级","parent":"","location":"山西省太原市"},
    {"id":33,"name":"人力资源和社会保障部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 刘宁 ──
    {"id":1,"person_id":1,"org_id":1,"title":"河南省委书记","start":"2024-12","end":"","rank":"正部级","note":"2024.12.31从广西党委书记调任河南省委书记"},
    {"id":2,"person_id":1,"org_id":3,"title":"河南省人大常委会主任","start":"2025-01","end":"","rank":"正部级","note":"2025.1.21当选省人大常委会主任"},
    {"id":3,"person_id":1,"org_id":22,"title":"广西壮族自治区党委书记","start":"2021-10","end":"2024-12","rank":"正部级","note":"约3年2个月"},
    {"id":4,"person_id":1,"org_id":23,"title":"广西壮族自治区人大常委会主任","start":"2022-01","end":"2025-01","rank":"正部级","note":"兼任"},
    {"id":5,"person_id":1,"org_id":21,"title":"辽宁省省长","start":"2020-07","end":"2021-10","rank":"正部级","note":"约15个月"},
    {"id":6,"person_id":1,"org_id":19,"title":"青海省省长","start":"2018-08","end":"2020-07","rank":"正部级","note":"约2年"},
    {"id":7,"person_id":1,"org_id":18,"title":"青海省委副书记、政法委书记","start":"2017-05","end":"2018-08","rank":"副部级","note":"2017.05任省委副书记，08月兼任政法委书记"},
    {"id":8,"person_id":1,"org_id":15,"title":"水利部副部长","start":"2009-02","end":"2017-05","rank":"副部级","note":"兼任国家防汛抗旱总指挥部秘书长"},
    {"id":9,"person_id":1,"org_id":15,"title":"水利部总工程师","start":"2003-02","end":"2009-02","rank":"正厅级","note":"指挥唐家山堰塞湖抢险"},
    {"id":10,"person_id":1,"org_id":17,"title":"南水北调规划设计管理局总工程师","start":"2001-12","end":"2003-02","rank":"","note":""},
    {"id":11,"person_id":1,"org_id":16,"title":"长江水利委员会副总工程师","start":"1998-07","end":"2001-12","rank":"副局级","note":"从基层技术员逐步晋升"},
    {"id":12,"person_id":1,"org_id":16,"title":"长江水利委员会技术干部","start":"1983-07","end":"1998-07","rank":"","note":"1983年清华毕业后进入长江委工作15年"},

    # ── 王凯 ──
    {"id":13,"person_id":2,"org_id":2,"title":"河南省省长","start":"2021-04","end":"","rank":"正部级","note":"2021.04.02任代省长，后当选省长"},
    {"id":14,"person_id":2,"org_id":28,"title":"长春市委书记","start":"2019-04","end":"2021-03","rank":"副部级","note":"约2年"},
    {"id":15,"person_id":2,"org_id":27,"title":"吉林省委常委、组织部部长","start":"2017-03","end":"2019-04","rank":"副部级","note":"约2年"},
    {"id":16,"person_id":2,"org_id":22,"title":"广西壮族自治区党委常委、玉林市委书记","start":"2016-11","end":"2017-03","rank":"副部级","note":"晋升副部级"},
    {"id":17,"person_id":2,"org_id":26,"title":"玉林市委书记","start":"2014-01","end":"2016-11","rank":"正厅级","note":""},
    {"id":18,"person_id":2,"org_id":26,"title":"玉林市市长","start":"2013-01","end":"2014-01","rank":"正厅级","note":""},
    {"id":19,"person_id":2,"org_id":25,"title":"梧州市市长","start":"2008-02","end":"2013-01","rank":"正厅级","note":"约5年"},
    {"id":20,"person_id":2,"org_id":25,"title":"梧州市委副书记","start":"2006-09","end":"2008-02","rank":"副厅级","note":""},
    {"id":21,"person_id":2,"org_id":25,"title":"梧州市委常委、组织部部长","start":"2003-08","end":"2006-09","rank":"副厅级","note":""},
    {"id":22,"person_id":2,"org_id":25,"title":"梧州市副市长","start":"2001-04","end":"2003-08","rank":"副厅级","note":"从中纪委下派挂职后留任"},
    {"id":23,"person_id":2,"org_id":24,"title":"中央纪委案件审理室调研处处长","start":"1999-06","end":"2002-11","rank":"正处级","note":"在中纪委工作约10年"},
    {"id":24,"person_id":2,"org_id":24,"title":"中央纪委干部","start":"1991-07","end":"1999-06","rank":"","note":"1991年人大硕士毕业后进入中纪委"},

    # ── 张巍 ──
    {"id":25,"person_id":3,"org_id":1,"title":"河南省委副书记、政法委书记","start":"2025-05","end":"","rank":"副部级","note":"从省纪委书记转任副书记"},
    {"id":26,"person_id":3,"org_id":5,"title":"河南省纪委书记","start":"2023-12","end":"2025-05","rank":"副部级","note":"从黑龙江调任河南"},
    {"id":27,"person_id":3,"org_id":10,"title":"河南省委政法委书记","start":"2025-05","end":"","rank":"副部级","note":"兼任政法委书记"},

    # ── 安伟 ──
    {"id":28,"person_id":4,"org_id":11,"title":"河南省委常委、郑州市委书记","start":"2022-01","end":"","rank":"副部级","note":"2022.01任"},
    {"id":29,"person_id":4,"org_id":1,"title":"河南省委常委","start":"2021-10","end":"","rank":"副部级","note":"当选第十一届省委常委"},

    # ── 秦国文 ──
    {"id":30,"person_id":5,"org_id":5,"title":"河南省纪委书记、省监委主任","start":"2025-08","end":"","rank":"副部级","note":"从湖南调任河南"},
    {"id":31,"person_id":5,"org_id":1,"title":"湖南省委常委、省委秘书长","start":"2024-01","end":"2025-08","rank":"副部级","note":""},

    # ── 王刚 ──
    {"id":32,"person_id":6,"org_id":7,"title":"河南省委组织部部长","start":"2023-05","end":"","rank":"副部级","note":"从宁夏调任河南"},

    # ── 张雷明 ──
    {"id":33,"person_id":7,"org_id":9,"title":"河南省委统战部部长","start":"2022-12","end":"","rank":"副部级","note":""},

    # ── 张敏 ──
    {"id":34,"person_id":8,"org_id":2,"title":"河南省常务副省长","start":"2026-04","end":"","rank":"副部级","note":"从建设银行副行长调任政府"},
    {"id":35,"person_id":8,"org_id":2,"title":"河南省副省长","start":"2023-01","end":"2026-04","rank":"副部级","note":""},

    # ── 王崧 ──
    {"id":36,"person_id":9,"org_id":8,"title":"河南省委宣传部部长","start":"2025-04","end":"","rank":"副部级","note":"从中央网信办调任河南"},
    {"id":37,"person_id":9,"org_id":15,"title":"中央网信办副主任","start":"2023-07","end":"2025-04","rank":"副部级","note":""},

    # ── 陈春江 ──
    {"id":38,"person_id":10,"org_id":12,"title":"河南省委常委、洛阳市委书记","start":"2025-10","end":"","rank":"副部级","note":"从陕西副省长调任河南"},

    # ── 李涛 ──
    {"id":39,"person_id":11,"org_id":1,"title":"河南省委常委、省委秘书长","start":"2026-06","end":"","rank":"副部级","note":"同时任副省长"},
    {"id":40,"person_id":11,"org_id":2,"title":"河南省副省长","start":"2025-04","end":"","rank":"副部级","note":""},

    # ── 刘玉江 ──
    {"id":41,"person_id":12,"org_id":2,"title":"河南省副省长","start":"2020-06","end":"","rank":"副部级","note":""},

    # ── 宋争辉 ──
    {"id":42,"person_id":13,"org_id":2,"title":"河南省副省长","start":"2022-06","end":"","rank":"副部级","note":""},

    # ── 郑海洋 ──
    {"id":43,"person_id":14,"org_id":6,"title":"河南省副省长、省公安厅厅长","start":"2023-01","end":"","rank":"副部级","note":""},

    # ── 李酌 ──
    {"id":44,"person_id":15,"org_id":2,"title":"河南省副省长","start":"2023-07","end":"","rank":"副部级","note":""},

    # ── 吕国范 ──
    {"id":45,"person_id":16,"org_id":2,"title":"河南省副省长（无党派）","start":"2025-04","end":"","rank":"副部级","note":"无党派人士"},

    # ── Predecessors — 省委书记 ──
    {"id":46,"person_id":17,"org_id":1,"title":"河南省委书记","start":"2021-06","end":"2024-12","rank":"正部级","note":"约3年7个月，到龄卸任"},
    {"id":47,"person_id":18,"org_id":1,"title":"河南省委书记","start":"2018-03","end":"2021-06","rank":"正部级","note":"约3年2个月，后调全国人大"},
    {"id":48,"person_id":18,"org_id":13,"title":"全国人大社会建设委员会副主任委员","start":"2021","end":"","rank":"正部级","note":""},
    {"id":49,"person_id":19,"org_id":1,"title":"河南省委书记","start":"2016-03","end":"2018-03","rank":"正部级","note":"约2年，后升任中国社科院院长"},
    {"id":50,"person_id":19,"org_id":14,"title":"中国社会科学院院长","start":"2018","end":"2022","rank":"正部级","note":""},

    # ── Predecessors — 省长 ──
    {"id":51,"person_id":20,"org_id":2,"title":"河南省省长","start":"2019-12","end":"2021-03","rank":"正部级","note":"约1年4个月"},
    {"id":52,"person_id":20,"org_id":29,"title":"江西省委书记","start":"2022-12","end":"","rank":"正部级","note":"现任"},
    {"id":53,"person_id":21,"org_id":2,"title":"河南省省长","start":"2016-04","end":"2019-10","rank":"正部级","note":"约3年6个月"},

    # ── 孙守刚（原常务副省长） ──
    {"id":54,"person_id":31,"org_id":3,"title":"河南省人大常委会副主任","start":"2026-01","end":"","rank":"副部级","note":"原常务副省长转任人大"},
    {"id":55,"person_id":31,"org_id":2,"title":"河南省常务副省长","start":"2021-11","end":"2026-01","rank":"副部级","note":""},

    # ── Cross-province figures ──
    {"id":56,"person_id":27,"org_id":32,"title":"山西省省长","start":"2022-12","end":"2025","rank":"正部级","note":"王凯玉林前任，2025年被调查"},
    {"id":57,"person_id":28,"org_id":31,"title":"山东省委书记","start":"2022-12","end":"","rank":"正部级","note":"王凯吉林组织部长前任"},
    {"id":58,"person_id":29,"org_id":33,"title":"人力资源和社会保障部部长","start":"2022-12","end":"","rank":"正部级","note":"王凯吉林组工继任者"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 刘宁 ↔ 王凯（党政搭档） ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"刘宁（省委书记）与王凯（省长）为河南省党政一把手搭档","overlap_org":"河南省","overlap_period":"2024-12至今"},

    # ── 省委书记接班人 ──
    {"id":2,"person_a":17,"person_b":1,"type":"前后任","context":"楼阳生（2021-2024河南省委书记）→ 刘宁（2024.12接任）。楼阳生到龄卸任","overlap_org":"中共河南省委员会","overlap_period":"不重叠（前后任）"},
    {"id":3,"person_a":18,"person_b":17,"type":"前后任","context":"王国生（2018-2021河南省委书记）→ 楼阳生（2021.06接任）","overlap_org":"中共河南省委员会","overlap_period":"不重叠（前后任）"},
    {"id":4,"person_a":19,"person_b":18,"type":"前后任","context":"谢伏瞻（2016-2018河南省委书记）→ 王国生（2018.03接任）","overlap_org":"中共河南省委员会","overlap_period":"不重叠（前后任）"},

    # ── 省长接班人 ──
    {"id":5,"person_a":20,"person_b":2,"type":"前后任","context":"尹弘（2019-2021河南省长）→ 王凯（2021.04接任）。尹弘调任甘肃、江西省委书记","overlap_org":"河南省人民政府","overlap_period":"不重叠（前后任）"},
    {"id":6,"person_a":21,"person_b":20,"type":"前后任","context":"陈润儿（2016-2019河南省长）→ 尹弘（2019.12接任）","overlap_org":"河南省人民政府","overlap_period":"不重叠（前后任）"},

    # ── 刘宁跨省网络 ──
    {"id":7,"person_a":1,"person_b":24,"type":"前后任","context":"刘宁（青海省长）→ 信长星（青海接任省长）。两人分别接掌河南/江苏","overlap_org":"青海省","overlap_period":"不重叠（前后任）"},
    {"id":8,"person_a":1,"person_b":25,"type":"党政搭档","context":"刘宁（青海省长）与王建军（青海省委书记）为青海党政搭档","overlap_org":"青海省","overlap_period":"2018-2020"},
    {"id":9,"person_a":1,"person_b":26,"type":"党政搭档","context":"刘宁（广西党委书记）与蓝天立（广西政府主席）为广西党政搭档","overlap_org":"广西壮族自治区","overlap_period":"2021-2024"},
    {"id":10,"person_a":1,"person_b":30,"type":"水利部同僚","context":"刘宁与叶建春均在水利部任副部长，后叶建春任江西省省长","overlap_org":"水利部","overlap_period":"2009-2017"},
    {"id":11,"person_a":1,"person_b":18,"type":"青海→河南路径","context":"王国生（青海省委书记→河南省委书记）→ 刘宁（广西党委书记→河南省委书记）。两人均从青海/广西调任河南","overlap_org":"河南/青海","overlap_period":"不重叠（前后任）"},

    # ── 王凯跨省网络 ──
    {"id":12,"person_a":2,"person_b":27,"type":"前后任","context":"金湘军（玉林书记前任）→ 王凯继任。金湘军升山西省省长后被调查","overlap_org":"玉林市","overlap_period":"不重叠（前后任）"},
    {"id":13,"person_a":2,"person_b":28,"type":"前后任","context":"林武（吉林组织部长前任）→ 王凯继任。两人均升任正部级","overlap_org":"吉林省","overlap_period":"不重叠（前后任）"},
    {"id":14,"person_a":2,"person_b":29,"type":"前后任","context":"王凯（吉林组织部长）→ 王晓萍继任。王晓萍现为人力资源和社会保障部部长","overlap_org":"吉林省","overlap_period":"不重叠（前后任）"},
    {"id":15,"person_a":2,"person_b":26,"type":"广西同僚","context":"王凯在广西工作期间，蓝天立时任广西政府副主席","overlap_org":"广西","overlap_period":"2016-2017"},

    # ── 孙守刚转任 ──
    {"id":16,"person_a":31,"person_b":8,"type":"前后任常务副省长","context":"孙守刚（常务副省长2021-2026）→ 张敏（常务副省长2026-）。孙守刚转任省人大","overlap_org":"河南省人民政府","overlap_period":"不重叠（前后任）"},

    # ── 省委常委会关系 ──
    {"id":17,"person_a":1,"person_b":3,"type":"省委班子搭档","context":"刘宁（省委书记）与张巍（省委副书记、政法委书记）共同构成省委核心班子","overlap_org":"河南省","overlap_period":"2024-12至今"},
    {"id":18,"person_a":2,"person_b":8,"type":"省长-常务副省长","context":"王凯（省长）与张敏（常务副省长，金融背景）的经济管理搭档","overlap_org":"河南省","overlap_period":"2026-04至今"},

    # ── 本土干部 vs 外调干部 ──
    {"id":19,"person_a":4,"person_b":7,"type":"本土干部","context":"安伟（郑州书记）与张雷明均为河南本土成长干部，全部履历在河南","overlap_org":"河南省","overlap_period":"长期"},
    {"id":20,"person_a":9,"person_b":10,"type":"外调干部","context":"王崧（清华博士，宣传部长）与陈春江（蒙古族，洛阳书记）均为近年从中央/外省调任河南","overlap_org":"河南省","overlap_period":"2025至今"},
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
lines.append('    <description>河南省（省级）领导班子工作关系网络 — 2026年7月15日生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["省委书记","省长","省委副书记","省长、省政府党组书记"]) else "12.0"
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
