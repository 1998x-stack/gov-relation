#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Nanchang City (南昌市) leadership network.

Covers: city-level leaders (mayor, party secretary, vice mayors, party committee),
plus the predecessor chain and key connections to districts/counties.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/nanchang_city_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/nanchang_city_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current leadership (city-level) ──
    {"id":1,"name":"盛秋平","gender":"男","ethnicity":"汉族","birth":"1968-09","birthplace":"浙江新昌","education":"专科（上海应用技术学院化工分析）+ MPA（美国肯恩大学）","party_join":"1989-01","work_start":"1989-08","current_post":"江西省委常委、南昌市委书记、赣江新区党工委书记","current_org":"中共南昌市委员会","source":"https://en.wikipedia.org/wiki/Sheng_Qiuping"},
    {"id":2,"name":"高世文","gender":"男","ethnicity":"汉族","birth":"1974-06","birthplace":"山东青州","education":"研究生学历","party_join":"中共党员","work_start":"","current_post":"南昌市委副书记、市长（2026年2月起长期未公开露面）","current_org":"南昌市人民政府","source":"WeChat公众号\"三里河小吏杂谈\"等"},
    {"id":3,"name":"赵捷","gender":"男","ethnicity":"汉族","birth":"1983-06","birthplace":"","education":"研究生学历","party_join":"中共党员","work_start":"","current_post":"南昌市委常委、常务副市长（党组副书记）","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/zhaojie/202201/66e82b227ecf40168c6452ed0ae773c4.shtml"},
    {"id":4,"name":"安宝军","gender":"男","ethnicity":"汉族","birth":"1971-07","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市委常委、副市长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/abj/202108/68d58e9d6a3648bdac7bb81da051b219.shtml"},
    {"id":5,"name":"马煜洲","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"","education":"研究生学历","party_join":"中共党员","work_start":"","current_post":"南昌市委常委、副市长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/myz/202201/d514bb446ed24bd5b486e7a26ecad466.shtml"},
    {"id":6,"name":"陈鹏辉","gender":"男","ethnicity":"汉族","birth":"1973-03","birthplace":"","education":"研究生学历","party_join":"中共党员","work_start":"","current_post":"南昌市副市长、市公安局局长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/xiaotj/202110/fe6d85a440874b87bf23aaaed54b286c.shtml"},
    {"id":7,"name":"徐鹤飞","gender":"男","ethnicity":"汉族","birth":"1980-09","birthplace":"","education":"在职研究生","party_join":"中共党员","work_start":"","current_post":"南昌市副市长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/xhf/202201/8db963bbe1b64e7e892d492c5ea966e5.shtml"},
    {"id":8,"name":"江新洪","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市副市长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/szfld/2021_ld_collection.shtml"},
    {"id":9,"name":"余红艳","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"南昌市副市长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/szfld/2021_ld_collection.shtml"},
    {"id":10,"name":"彭开先","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市副市长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/szfld/2021_ld_collection.shtml"},
    {"id":11,"name":"高辉红","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市副市长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/szfld/2021_ld_collection.shtml"},
    {"id":12,"name":"王成久","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市政府秘书长","current_org":"南昌市人民政府","source":"https://www.nc.gov.cn/ncszf/szfld/2021_ld_collection.shtml"},

    # ── City party committee other key members ──
    {"id":13,"name":"李镇发","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市人大常委会主任","current_org":"南昌市人大常委会","source":"https://www.ncnews.com.cn/xwzx/ncxw/szxw/"},
    {"id":14,"name":"王爱东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市政协主席","current_org":"政协南昌市委员会","source":"https://www.ncnews.com.cn/xwzx/ncxw/szxw/"},
    {"id":15,"name":"饶绍清","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市委常委（统战部部长？）","current_org":"中共南昌市委员会","source":"https://www.ncnews.com.cn/xwzx/ncxw/szxw/"},

    # ── Predecessors (mayors) ──
    {"id":16,"name":"万广明","gender":"男","ethnicity":"汉族","birth":"1967-01","birthplace":"江西余干","education":"研究生，工学硕士","party_join":"中共党员","work_start":"","current_post":"江西省副省长","current_org":"江西省人民政府","source":"https://www.wikidata.org/wiki/Q111693436"},
    {"id":17,"name":"黄喜忠","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"广东揭阳","education":"","party_join":"中共党员","work_start":"","current_post":"江西省委常委、统战部部长","current_org":"中共江西省委员会","source":"https://baike.baidu.com/item/%E9%BB%84%E5%96%9C%E5%BF%A0"},
    {"id":18,"name":"郭安","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"（原鹰潭市委书记→省人大）","current_org":"","source":""},

    # ── Previous Party Secretary (predecessor of 盛秋平) ──
    {"id":19,"name":"李红军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"（原南昌市委书记，已调离）","current_org":"","source":""},

    # ── Cross-district key connectors (already in other dbs, city-relevant) ──
    {"id":20,"name":"熊振强","gender":"男","ethnicity":"汉族","birth":"1972-03","birthplace":"江西奉新","education":"大学","party_join":"1992-12","work_start":"1991-09","current_post":"进贤县委书记（原南昌市交通局局长）","current_org":"中共进贤县委员会","source":"https://baike.baidu.com/item/%E7%86%8A%E6%8C%AF%E5%BC%BA/7691320"},
    {"id":21,"name":"徐强","gender":"男","ethnicity":"汉族","birth":"1974-11","birthplace":"江西南昌县","education":"南昌航空工业学院+江西财大MPA","party_join":"1996-06","work_start":"1996-09","current_post":"新建区委书记（原进贤县委书记）","current_org":"中共南昌市新建区委员会","source":"https://baike.baidu.com/item/%E5%BE%90%E5%BC%BA/50081202"},
    {"id":22,"name":"刘光荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"江西南昌县","education":"","party_join":"中共党员","work_start":"1995","current_post":"东湖区委书记（南昌县21年工作经历）","current_org":"中共南昌市东湖区委员会","source":"https://dhq.nc.gov.cn"},
    {"id":23,"name":"贾彧超","gender":"男","ethnicity":"汉族","birth":"1976-09","birthplace":"湖北襄阳","education":"中国科学技术大学管理学学士","party_join":"2002-09","work_start":"2000-07","current_post":"南昌县委书记、小蓝经开区党工委书记","current_org":"中共南昌县委员会","source":"https://baike.baidu.com/item/%E8%B4%BE%E5%BD%A7%E8%B6%85/20265811"},
    {"id":24,"name":"杨育星","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"青山湖区委书记（原青山湖区区长）","current_org":"中共南昌市青山湖区委员会","source":""},
    {"id":25,"name":"罗国栋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"青云谱区委书记（原安义县县长）","current_org":"中共南昌市青云谱区委员会","source":""},
    {"id":26,"name":"陈奕蒙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"红谷滩区委书记（原新建区委书记）","current_org":"中共南昌市红谷滩区委员会","source":""},
    {"id":27,"name":"熊辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"安义县委书记（原进贤县县长）","current_org":"中共安义县委员会","source":""},
    {"id":28,"name":"邓之武","gender":"男","ethnicity":"汉族","birth":"1976-02","birthplace":"江西万年","education":"浙江大学茶学学士+江西财大MBA","party_join":"中共党员","work_start":"1998-08","current_post":"东湖区委副书记、代区长","current_org":"中共南昌市东湖区委员会","source":"https://baike.baidu.com/item/%E9%82%93%E4%B9%8B%E6%AD%A6/19426611"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # City-level
    {"id":1,"name":"中共南昌市委员会","type":"党委","level":"副省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":2,"name":"南昌市人民政府","type":"政府","level":"副省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":3,"name":"南昌市人大常委会","type":"人大","level":"副省级","parent":"江西省人大常委会","location":"江西省南昌市"},
    {"id":4,"name":"政协南昌市委员会","type":"政协","level":"副省级","parent":"政协江西省委员会","location":"江西省南昌市"},
    {"id":5,"name":"赣江新区管委会","type":"新区","level":"国家级","parent":"江西省人民政府","location":"江西省南昌市/九江市"},
    {"id":6,"name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":7,"name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":8,"name":"中华人民共和国商务部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":9,"name":"浙江省商务厅","type":"政府","level":"省级","parent":"浙江省人民政府","location":"浙江省杭州市"},
    {"id":10,"name":"中共义乌市委","type":"党委","level":"县级","parent":"中共金华市委","location":"浙江省金华市义乌市"},
    {"id":11,"name":"金华市人民政府","type":"政府","level":"地级","parent":"浙江省人民政府","location":"浙江省金华市"},
    {"id":12,"name":"浙江省人民政府","type":"政府","level":"省级","parent":"","location":"浙江省杭州市"},

    # District/county orgs (for connections)
    {"id":13,"name":"中共进贤县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市进贤县"},
    {"id":14,"name":"进贤县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市进贤县"},
    {"id":15,"name":"中共南昌市新建区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市新建区"},
    {"id":16,"name":"中共南昌市东湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市东湖区"},
    {"id":17,"name":"中共南昌县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市南昌县"},
    {"id":18,"name":"南昌县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市南昌县"},
    {"id":19,"name":"中共南昌市青山湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市青山湖区"},
    {"id":20,"name":"中共南昌市青云谱区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市青云谱区"},
    {"id":21,"name":"中共安义县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市安义县"},
    {"id":22,"name":"中共南昌市红谷滩区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市红谷滩区"},
    {"id":23,"name":"南昌市交通局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 盛秋平 ──
    {"id":1,"person_id":1,"org_id":7,"title":"江西省委常委","start":"2026-06","end":"","rank":"副省级","note":"2026年6月29日任命"},
    {"id":2,"person_id":1,"org_id":1,"title":"南昌市委书记","start":"2026-06","end":"","rank":"副省级","note":"兼任赣江新区党工委书记"},
    {"id":3,"person_id":1,"org_id":5,"title":"赣江新区党工委书记","start":"2026-06","end":"","rank":"副省级","note":""},
    {"id":4,"person_id":1,"org_id":8,"title":"商务部副部长、党组成员","start":"2021-12","end":"2026-06","rank":"副部级","note":"2021.12部长助理，2022.05升副部长"},
    {"id":5,"person_id":1,"org_id":9,"title":"浙江省商务厅厅长、党组书记","start":"2018-03","end":"2021-12","rank":"正厅级","note":""},
    {"id":6,"person_id":1,"org_id":10,"title":"金华市委常委、义乌市委书记","start":"2015-12","end":"2018-02","rank":"副厅级→正厅级","note":"主政义乌期间外贸逆势增长43%"},
    {"id":7,"person_id":1,"org_id":11,"title":"金华市副市长、义乌市代市长→市长","start":"2014-06","end":"2015-12","rank":"副厅级","note":""},
    {"id":8,"person_id":1,"org_id":12,"title":"永嘉县委书记（温州市）","start":"2011-07","end":"2014-06","rank":"正处级","note":""},
    {"id":9,"person_id":1,"org_id":10,"title":"嵊州市委书记→市长","start":"2006-12","end":"2011-07","rank":"正处级","note":"2007.02正式任市长"},
    {"id":10,"person_id":1,"org_id":12,"title":"绍兴县委常委、常务副县长","start":"2004-12","end":"2006-12","rank":"副处级","note":""},

    # ── 高世文 ──
    {"id":11,"person_id":2,"org_id":2,"title":"南昌市委副书记、市长","start":"2024-08","end":"","rank":"副省级","note":"2026年2月2日后未再公开露面"},
    {"id":12,"person_id":2,"org_id":12,"title":"江西省工信厅厅长","start":"~2023","end":"2024-08","rank":"正厅级","note":"航天科技集团背景"},
    {"id":13,"person_id":2,"org_id":6,"title":"挂职赣州市副市长","start":"~2021","end":"~2023","rank":"副厅级","note":"航天科技集团挂职地方"},

    # ── 赵捷 ──
    {"id":14,"person_id":3,"org_id":1,"title":"南昌市委常委","start":"2022-01","end":"","rank":"副厅级","note":""},
    {"id":15,"person_id":3,"org_id":2,"title":"南昌市常务副市长、党组副书记","start":"2022-01","end":"","rank":"副厅级","note":"高世文缺席期间主持政府日常工作"},

    # ── 安宝军 ──
    {"id":16,"person_id":4,"org_id":1,"title":"南昌市委常委","start":"","end":"","rank":"副厅级","note":""},
    {"id":17,"person_id":4,"org_id":2,"title":"南昌市副市长","start":"","end":"","rank":"副厅级","note":"分管商务、外事、对台事务、合作交流"},

    # ── 马煜洲 ──
    {"id":18,"person_id":5,"org_id":1,"title":"南昌市委常委","start":"","end":"","rank":"副厅级","note":""},
    {"id":19,"person_id":5,"org_id":2,"title":"南昌市副市长","start":"","end":"","rank":"副厅级","note":"分管科技、工信、中小企业服务"},

    # ── 陈鹏辉 ──
    {"id":20,"person_id":6,"org_id":2,"title":"南昌市副市长、市公安局局长","start":"","end":"","rank":"副厅级","note":"兼江西省公安厅党委委员"},

    # ── 徐鹤飞 ──
    {"id":21,"person_id":7,"org_id":2,"title":"南昌市副市长","start":"","end":"","rank":"副厅级","note":"分管金融、数据、国有资产"},

    # ── 万广明 ──
    {"id":22,"person_id":16,"org_id":6,"title":"江西省副省长","start":"~2025-02","end":"","rank":"副省级","note":"从南昌市长晋升"},
    {"id":23,"person_id":16,"org_id":2,"title":"南昌市委副书记、市长","start":"2021-03","end":"~2025-02","rank":"副省级","note":"此前任江西省财政厅厅长"},
    {"id":24,"person_id":16,"org_id":6,"title":"江西省财政厅厅长","start":"~2019","end":"2021-03","rank":"正厅级","note":""},

    # ── 黄喜忠 ──
    {"id":25,"person_id":17,"org_id":7,"title":"江西省委常委、统战部部长","start":"~2023","end":"","rank":"副省级","note":"跨省交流干部（广东→江西）"},
    {"id":26,"person_id":17,"org_id":2,"title":"南昌市委副书记、市长","start":"2019-12","end":"2020-12","rank":"副省级","note":"约1年"},
    {"id":27,"person_id":17,"org_id":7,"title":"鹰潭市委书记","start":"2021-01","end":"~2023","rank":"正厅级","note":"从南昌市长转任"},

    # ── 郭安 ──
    {"id":28,"person_id":18,"org_id":2,"title":"南昌市委副书记、市长","start":"2015-03","end":"2018-03","rank":"副省级","note":"约3年"},
    {"id":29,"person_id":18,"org_id":7,"title":"鹰潭市委书记","start":"2018","end":"2021","rank":"正厅级","note":"从南昌市长平级重用"},

    # ── Cross-district connections ──
    {"id":30,"person_id":20,"org_id":13,"title":"进贤县委书记","start":"2026-06","end":"","rank":"正处级","note":"原南昌市交通局局长"},
    {"id":31,"person_id":20,"org_id":23,"title":"南昌市交通局局长","start":"~2021","end":"2026-06","rank":"正处级","note":""},
    {"id":32,"person_id":21,"org_id":15,"title":"新建区委书记","start":"2026-06","end":"","rank":"正处级","note":"原进贤县委书记→新建区委书记（提级）"},
    {"id":33,"person_id":21,"org_id":13,"title":"进贤县委书记","start":"2021-08","end":"2026-06","rank":"正处级","note":""},
    {"id":34,"person_id":22,"org_id":16,"title":"东湖区委书记","start":"2025-02","end":"","rank":"正处级","note":"南昌县21年工作经历"},
    {"id":35,"person_id":23,"org_id":17,"title":"南昌县委书记","start":"2025-02","end":"","rank":"副厅级","note":""},
    {"id":36,"person_id":24,"org_id":19,"title":"青山湖区委书记","start":"2026","end":"","rank":"正处级","note":"原区长晋升"},
    {"id":37,"person_id":25,"org_id":20,"title":"青云谱区委书记","start":"2026-07","end":"","rank":"正处级","note":"原安义县长调任"},
    {"id":38,"person_id":26,"org_id":22,"title":"红谷滩区委书记","start":"2026-06","end":"","rank":"正处级","note":"原新建区委书记→红谷滩（提级）"},
    {"id":39,"person_id":27,"org_id":21,"title":"安义县委书记","start":"2026-06","end":"","rank":"正处级","note":"原进贤县长晋升"},
    {"id":40,"person_id":28,"org_id":16,"title":"东湖区委副书记、代区长","start":"2026-07","end":"","rank":"正处级","note":"原南昌县委副书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # City-level leadership
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"盛秋平（市委书记）与高世文（市长）为南昌市党政一把手。但高世文自2026年2月起长期缺席，盛秋平6月到任后尚未正式与高世文公开同台","overlap_org":"南昌市","overlap_period":"2026-06至今（名义上）"},
    {"id":2,"person_a":1,"person_b":3,"type":"直接上下级","context":"盛秋平（书记）领导赵捷（常务副市长）。高世文缺席期间，赵捷主持政府日常工作","overlap_org":"南昌市","overlap_period":"2026-06至今"},
    {"id":3,"person_a":3,"person_b":2,"type":"代行职务","context":"赵捷（常务副市长）在高世文（市长）长期缺席期间，以常务副市长身份主持大量政府工作会议","overlap_org":"南昌市人民政府","overlap_period":"2026-02至今"},

    # Mayor succession chain
    {"id":4,"person_a":16,"person_b":2,"type":"前后任","context":"万广明（2021-2025市长）→ 高世文（2024/2025接任市长）。万广明升任副省长","overlap_org":"南昌市人民政府","overlap_period":"不重叠（前后任）"},
    {"id":5,"person_a":17,"person_b":16,"type":"前后任","context":"黄喜忠（2019-2020市长）→ 万广明（2021-2025市长）","overlap_org":"南昌市人民政府","overlap_period":"不重叠（前后任）"},
    {"id":6,"person_a":18,"person_b":17,"type":"前后任","context":"郭安（2015-2018市长）→ 黄喜忠（2019-2020市长）","overlap_org":"南昌市人民政府","overlap_period":"不重叠（前后任）"},

    # Party Secretary succession
    {"id":7,"person_a":19,"person_b":1,"type":"前后任","context":"李红军（前任南昌市委书记）→ 盛秋平（2026年6月接任）。盛秋平系从商务部空降","overlap_org":"中共南昌市委员会","overlap_period":"不重叠（前后任）"},

    # 盛秋平's network (Zhejiang system)
    {"id":8,"person_a":1,"person_b":8,"type":"中央-地方","context":"盛秋平在商务部任副部长4年半（2021-2026），后空降南昌市委书记。其在商务部的人脉网络是重要的跨系统资源","overlap_org":"商务部","overlap_period":"2021-12至2026-06"},
    {"id":9,"person_a":1,"person_b":9,"type":"浙江省系统","context":"盛秋平在浙江工作32年（1989-2021），曾任浙江省商务厅长、义乌市委书记等职","overlap_org":"浙江省","overlap_period":"1989至2021"},

    # Cross-district → City connections
    {"id":10,"person_a":10,"person_b":21,"type":"安义→副市长","context":"彭开先（副市长）曾任安义县委书记（约2019-2021），是典型的从县区主官晋升市级领导的路径","overlap_org":"安义县→南昌市政府","overlap_period":"~2019-2021（安义）"},
    {"id":11,"person_a":11,"person_b":22,"type":"东湖→副市长","context":"高辉红（副市长）曾任东湖区委书记，后升任南昌市副市长","overlap_org":"东湖区→南昌市政府","overlap_period":""},
    {"id":12,"person_a":20,"person_b":23,"type":"县区→市直→县区","context":"熊振强（进贤县委书记）此前曾任南昌市交通局局长，属'市直→县'的交流路径","overlap_org":"南昌市交通局→进贤县","overlap_period":"~2021至2026"},
    {"id":13,"person_a":21,"person_b":26,"type":"递进晋升链","context":"徐强（进贤→新建区委书记）的晋升使得陈奕蒙（新建→红谷滩）随之梯次递补，形成'进贤→新建→红谷滩'的递进链条","overlap_org":"新建区","overlap_period":"2026-06"},
    {"id":14,"person_a":21,"person_b":27,"type":"进贤系统","context":"徐强（原进贤书记）与熊辉（原进贤县长→安义书记）在进贤县搭班子","overlap_org":"进贤县","overlap_period":"2021至2026-06"},
    {"id":15,"person_a":22,"person_b":28,"type":"南昌县系","context":"刘光荣（东湖书记，南昌县21年）与邓之武（东湖代区长，原南昌县委副书记）均为南昌县系统出身，构成东湖区的'南昌县双人组'","overlap_org":"南昌县→东湖区","overlap_period":"2026-07至今"},
    {"id":16,"person_a":25,"person_b":27,"type":"安义→青云谱","context":"罗国栋（原安义县长→青云谱书记）与熊辉（原进贤县长→安义书记）形成安义县→青云谱区的交流通道","overlap_org":"安义县","overlap_period":"~2024至2026-06"},

    # Notable 2026-07 batch adjustment
    {"id":17,"person_a":21,"person_b":20,"type":"2026年7月大调整","context":"2026年7月六县区联动调整：徐强(进贤→新建)→陈奕蒙(新建→红谷滩)，熊振强(市交通局长→进贤书记)补徐强的缺，熊辉(进贤县长→安义书记)","overlap_org":"南昌市","overlap_period":"2026-06至2026-07"},

    # Mayor situation: the big unknown
    {"id":18,"person_a":1,"person_b":16,"type":"前任→后任（非直接）","context":"盛秋平（2026.06任书记）与万广明（前市长，2025初升副省长）在南昌市时间上不重叠，但均属省级安排的重要岗位","overlap_org":"南昌市","overlap_period":"不重叠"},
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
    if "书记" in post and ("市委" in post or "县委书记" in post or "区委书记" in post):
        return "230,50,50"  # red for top party secretary
    if "常务副市长" in post or "市长" in post:
        return "50,100,230"  # blue for gov leaders
    if "副市长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"  # orange for discipline
    if "人大" in post:
        return "180,200,255"
    if "政协" in post:
        return "200,180,255"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255","政协":"230,200,255",
            "新区":"200,255,200","开发区":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>南昌市（市级）领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","市委书记"]) else "12.0"
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
    lines.append('        <viz:size value="8.0"/>')
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
