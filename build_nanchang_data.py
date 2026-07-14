#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Nanchang County leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/nanchang_county_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/nanchang_county_network.gexf")

persons = [
    {"id":1,"name":"贾彧超","gender":"男","ethnicity":"汉族","birth":"1976-09","birthplace":"湖北襄阳","education":"中国科学技术大学管理学学士","party_join":"2002-09","work_start":"2000-07","current_post":"南昌县委书记、小蓝经开区党工委书记","current_org":"中共南昌县委员会","source":"https://baike.baidu.com/item/%E8%B4%BE%E5%BD%A7%E8%B6%85/20265811"},
    {"id":2,"name":"帅志","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"江西南昌","education":"省委党校研究生，法学学士","party_join":"2001-06","work_start":"1996-09","current_post":"南昌县委副书记、县长","current_org":"南昌县人民政府","source":"https://baike.baidu.com/item/%E5%B8%85%E5%BF%97"},
    {"id":3,"name":"邓之武","gender":"男","ethnicity":"汉族","birth":"1976-02","birthplace":"江西万年","education":"浙江大学茶学学士+江西财大MBA","party_join":"中共党员","work_start":"1998-08","current_post":"东湖区委副书记、代区长（原南昌县委副书记）","current_org":"中共南昌市东湖区委员会","source":"https://baike.baidu.com/item/%E9%82%93%E4%B9%8B%E6%AD%A6/19426611"},
    {"id":4,"name":"陈翔","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"江西樟树","education":"江西财经大学工业经济学学士","party_join":"1997-01","work_start":"1992-08","current_post":"南昌市政府二级巡视员（原南昌县委书记）","current_org":"南昌市人民政府","source":"https://baike.baidu.com/item/%E9%99%88%E7%BF%94/1774035"},
    {"id":5,"name":"徐志勇","gender":"男","ethnicity":"汉族","birth":"1981-07","birthplace":"江西丰城","education":"南昌大学在职研究生（公共管理）","party_join":"2002-01","work_start":"2002-07","current_post":"南昌县委常委、常务副县长","current_org":"南昌县人民政府","source":"https://baike.baidu.com/item/%E5%BE%90%E5%BF%97%E5%8B%87/55781241"},
    {"id":6,"name":"邬春华","gender":"男","ethnicity":"汉族","birth":"1971-02","birthplace":"江西丰城","education":"在职大学","party_join":"2007-02","work_start":"1990-08","current_post":"南昌县委常委、组织部部长","current_org":"中共南昌县委员会","source":"https://baike.baidu.com/item/%E9%82%AC%E6%98%A5%E5%8D%8E/54012365"},
    {"id":7,"name":"皮钧","gender":"女","ethnicity":"汉族","birth":"1980-11","birthplace":"","education":"江西师范大学文学学士","party_join":"中共党员","work_start":"","current_post":"南昌县委常委、统战部部长","current_org":"中共南昌县委员会","source":"https://baike.baidu.com/item/%E7%9A%AE%E9%92%A7/18045271"},
    {"id":8,"name":"胡朝辉","gender":"男","ethnicity":"汉族","birth":"1973-02","birthplace":"江西南昌县","education":"大专","party_join":"中共党员","work_start":"","current_post":"南昌县委常委、宣传部部长","current_org":"中共南昌县委员会","source":"https://baike.baidu.com/item/%E8%83%A1%E6%9C%9D%E8%BE%89/7389917"},
    {"id":9,"name":"万向阳","gender":"男","ethnicity":"汉族","birth":"1976-01","birthplace":"江西南昌县","education":"大学","party_join":"中共党员","work_start":"","current_post":"南昌县委常委、副县长","current_org":"南昌县人民政府","source":"http://ncx.nc.gov.cn"},
    {"id":10,"name":"黄淦明","gender":"男","ethnicity":"汉族","birth":"1979-10","birthplace":"","education":"大学","party_join":"中共党员","work_start":"","current_post":"南昌县委常委、纪委书记、监委主任","current_org":"中共南昌县委员会","source":"https://www.thepaper.cn/newsDetail_forward_30517254"},
    {"id":11,"name":"马合木江·艾合买提","gender":"男","ethnicity":"维吾尔族","birth":"1986-06","birthplace":"新疆伊宁","education":"博士（水资源）","party_join":"中共党员","work_start":"","current_post":"南昌县委常委、副县长","current_org":"南昌县人民政府","source":"http://ncx.nc.gov.cn"},
    {"id":12,"name":"程家华","gender":"男","ethnicity":"汉族","birth":"1973-03","birthplace":"江西南昌","education":"大学","party_join":"中共党员","work_start":"","current_post":"南昌县委常委、政法委书记","current_org":"中共南昌县委员会","source":"http://ncx.nc.gov.cn"},
    {"id":13,"name":"廖淑敏","gender":"男","ethnicity":"汉族","birth":"1977-10","birthplace":"江西南昌县","education":"研究生","party_join":"中共党员","work_start":"","current_post":"南昌县副县长","current_org":"南昌县人民政府","source":"http://ncx.nc.gov.cn"},
    {"id":14,"name":"易才宏","gender":"男","ethnicity":"汉族","birth":"1976-04","birthplace":"江西安义","education":"研究生","party_join":"中共党员","work_start":"","current_post":"南昌县副县长、公安局局长","current_org":"南昌县人民政府","source":"http://ncx.nc.gov.cn"},
    {"id":15,"name":"涂超","gender":"男","ethnicity":"汉族","birth":"1977-11","birthplace":"江西南昌","education":"大学","party_join":"中共党员","work_start":"","current_post":"南昌县副县长","current_org":"南昌县人民政府","source":"http://ncx.nc.gov.cn"},
    {"id":16,"name":"余佳琦","gender":"女","ethnicity":"汉族","birth":"1982-12","birthplace":"江西南昌","education":"大学","party_join":"民建","work_start":"","current_post":"南昌县副县长","current_org":"南昌县人民政府","source":"http://ncx.nc.gov.cn"},
    {"id":17,"name":"薛凯喜","gender":"男","ethnicity":"汉族","birth":"1981-09","birthplace":"山东沂水","education":"博士（工程）","party_join":"中共党员","work_start":"","current_post":"南昌县副县长","current_org":"南昌县人民政府","source":"http://ncx.nc.gov.cn"},
    {"id":18,"name":"熊运浪","gender":"男","ethnicity":"汉族","birth":"1968-11","birthplace":"江西南昌县","education":"省委党校研究生","party_join":"中共党员","work_start":"","current_post":"江西省委政法委副书记（正厅长级）","current_org":"江西省委政法委","source":"https://baike.baidu.com"},
    {"id":19,"name":"闵员根","gender":"男","ethnicity":"汉族","birth":"1969-02","birthplace":"江西南昌县","education":"省委党校研究生","party_join":"中共党员","work_start":"1990-09","current_post":"西湖区人大常委会主任（原南昌县委副书记）","current_org":"西湖区人大常委会","source":"https://baike.baidu.com/item/%E9%97%B5%E5%91%98%E6%A0%B9/23710218"},
    {"id":20,"name":"陶亿国","gender":"男","ethnicity":"汉族","birth":"1973-08","birthplace":"江西南昌县","education":"江西农大兽医+江西财大MBA","party_join":"1995-06","work_start":"1996-12","current_post":"赣江新区管委会副主任（原西湖区委书记）","current_org":"赣江新区管委会","source":"https://baike.baidu.com/item/%E9%99%B6%E4%BA%BF%E5%9B%BD/14840701"},
    {"id":21,"name":"付向宇","gender":"男","ethnicity":"汉族","birth":"1979-09","birthplace":"江西进贤","education":"研究生","party_join":"2000-08","work_start":"1998-12","current_post":"南昌市商务局局长（原南昌县常务副县长）","current_org":"南昌市商务局","source":"https://baike.sogou.com/v183372574.htm"},
    {"id":22,"name":"熊军","gender":"男","ethnicity":"汉族","birth":"1976-05","birthplace":"江西南昌县","education":"省委党校研究生MPA","party_join":"中共党员","work_start":"1996-12","current_post":"进贤县副县长","current_org":"进贤县人民政府","source":"https://baike.baidu.com/item/%E7%86%8A%E5%86%9B/58350224"},
    {"id":23,"name":"徐永钢","gender":"男","ethnicity":"汉族","birth":"1981-04","birthplace":"江西丰城","education":"宁波大学经济学学士","party_join":"中共党员","work_start":"2004-04","current_post":"进贤县委常委、组织部部长","current_org":"中共进贤县委员会","source":"https://baike.baidu.com/item/%E5%BE%90%E6%B0%B8%E9%92%A2/55600127"},
    {"id":24,"name":"聂红兵","gender":"男","ethnicity":"汉族","birth":"1980-11","birthplace":"江西南昌县","education":"省委党校在职研究生","party_join":"1999-05","work_start":"1999-08","current_post":"进贤县委常委、副县长","current_org":"进贤县人民政府","source":"https://baike.baidu.com/item/%E8%81%82%E7%BA%A2%E5%85%B5/64020468"},
    {"id":25,"name":"熊振强","gender":"男","ethnicity":"汉族","birth":"1972-03","birthplace":"江西奉新","education":"大学","party_join":"1992-12","work_start":"1991-09","current_post":"进贤县委书记","current_org":"中共进贤县委员会","source":"https://baike.baidu.com/item/%E7%86%8A%E6%8C%AF%E5%BC%BA/7691320"},
    {"id":26,"name":"雷桥亮","gender":"男","ethnicity":"汉族","birth":"1980-11","birthplace":"江西井冈山","education":"研究生，经济学硕士","party_join":"中共党员","work_start":"","current_post":"进贤县委副书记、代县长","current_org":"进贤县人民政府","source":"https://baike.baidu.com/item/%E9%9B%B7%E6%A1%A5%E4%BA%AE/61369190"},
    {"id":27,"name":"徐强","gender":"男","ethnicity":"汉族","birth":"1974-11","birthplace":"江西南昌县","education":"南昌航空工业学院+江西财大MPA","party_join":"1996-06","work_start":"1996-09","current_post":"新建区委书记（原进贤县委书记）","current_org":"中共南昌市新建区委员会","source":"https://baike.baidu.com/item/%E5%BE%90%E5%BC%BA/50081202"},
    {"id":28,"name":"刘志伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"安义县委副书记、代县长（原南昌县幽兰镇书记）","current_org":"安义县人民政府","source":"https://baike.baidu.com/item/%E5%88%98%E5%BF%97%E4%BC%9F/50360138"},
    {"id":29,"name":"肖玉文","gender":"男","ethnicity":"汉族","birth":"1967-03","birthplace":"江西南昌","education":"浙江大学+上海交大MBA","party_join":"中共党员","work_start":"","current_post":"南昌市政协原主席（2025.11被查）","current_org":"","source":"https://baike.baidu.com/item/%E8%82%96%E7%8E%89%E6%96%87/72517"},
    {"id":30,"name":"刘光荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"江西南昌县","education":"","party_join":"中共党员","work_start":"1995","current_post":"东湖区委书记（南昌县21年工作经历）","current_org":"中共南昌市东湖区委员会","source":"http://dhq.nc.gov.cn"},
]

organizations = [
    {"id":1,"name":"中共南昌县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市南昌县"},
    {"id":2,"name":"南昌县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市南昌县"},
    {"id":3,"name":"小蓝经济技术开发区","type":"开发区","level":"国家级","parent":"南昌市人民政府","location":"江西省南昌市南昌县"},
    {"id":4,"name":"南昌市发展和改革委员会","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":5,"name":"共青团江西省委","type":"群团","level":"省级","parent":"共青团中央","location":"江西省南昌市"},
    {"id":6,"name":"中共南昌市东湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市东湖区"},
    {"id":7,"name":"南昌市纪律检查委员会","type":"党委","level":"市级","parent":"中共南昌市委员会","location":"江西省南昌市"},
    {"id":8,"name":"中共进贤县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市进贤县"},
    {"id":9,"name":"进贤县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市进贤县"},
    {"id":10,"name":"南昌市投资促进局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":11,"name":"南昌市外经贸委","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":12,"name":"安义县","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市安义县"},
    {"id":13,"name":"中共安义县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市安义县"},
    {"id":14,"name":"南昌县黄马乡","type":"乡镇","level":"乡镇级","parent":"南昌县人民政府","location":"江西省南昌市南昌县"},
    {"id":15,"name":"南昌县武阳镇","type":"乡镇","level":"乡镇级","parent":"南昌县人民政府","location":"江西省南昌市南昌县"},
    {"id":16,"name":"中共南昌市西湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市西湖区"},
    {"id":17,"name":"中共南昌市青云谱区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市青云谱区"},
    {"id":18,"name":"南昌市湾里区","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市湾里区"},
    {"id":19,"name":"南昌市红谷滩区","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市红谷滩区"},
    {"id":20,"name":"中共南昌市新建区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市新建区"},
    {"id":21,"name":"南昌高新区","type":"开发区","level":"国家级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":22,"name":"南昌市城乡建设局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":23,"name":"南昌市交通运输局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":24,"name":"南昌市公路事业发展中心","type":"事业单位","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":25,"name":"南昌市西湖区","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市西湖区"},
    {"id":26,"name":"南昌市青云谱区","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市青云谱区"},
    {"id":27,"name":"江西省委政法委","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":28,"name":"南昌县幽兰镇","type":"乡镇","level":"乡镇级","parent":"南昌县人民政府","location":"江西省南昌市南昌县"},
]

positions = [
    # ── 贾彧超 ──
    {"id":1,"person_id":1,"org_id":5,"title":"共青团江西省委宣传部科员→部长（13年）","start":"2004-08","end":"2017-11","rank":"科员→正县级","note":""},
    {"id":2,"person_id":1,"org_id":6,"title":"东湖区委副书记（正县级）","start":"2017-11","end":"2020-11","rank":"正县级","note":""},
    {"id":3,"person_id":1,"org_id":4,"title":"南昌市发改委党组书记、主任","start":"2020-12","end":"2021-07","rank":"正处级","note":""},
    {"id":4,"person_id":1,"org_id":2,"title":"南昌县委副书记、县长（兼小蓝经开区管委会主任）","start":"2021-08","end":"2025-02","rank":"副厅级","note":""},
    {"id":5,"person_id":1,"org_id":1,"title":"南昌县委书记、小蓝经开区党工委书记","start":"2025-02","end":"","rank":"副厅级","note":"2025.02.14任前公示，02.27首次以书记身份主持"},

    # ── 帅志 ──
    {"id":6,"person_id":2,"org_id":17,"title":"青云谱区三家店街道党工委书记","start":"~2008","end":"2016","rank":"正科级","note":""},
    {"id":7,"person_id":2,"org_id":7,"title":"南昌市纪委办公厅主任","start":"2016","end":"2017-11","rank":"副县级","note":""},
    {"id":8,"person_id":2,"org_id":18,"title":"湾里区委常委、纪委书记、监委主任","start":"2017-11","end":"~2021","rank":"副处级","note":"2018.01监委成立"},
    {"id":9,"person_id":2,"org_id":19,"title":"红谷滩区委常委、纪委书记","start":"~2021","end":"2021-09","rank":"副处级","note":"区划调整后过渡"},
    {"id":10,"person_id":2,"org_id":7,"title":"南昌市纪委副书记、监委副主任","start":"2021-09","end":"2025-12","rank":"副厅级","note":"2025.12.26免去监委副主任"},
    {"id":11,"person_id":2,"org_id":1,"title":"南昌县委副书记","start":"2025-12","end":"","rank":"副厅级","note":""},
    {"id":12,"person_id":2,"org_id":2,"title":"南昌县县长（兼小蓝经开区管委会主任）","start":"2026-01-09","end":"","rank":"副厅级","note":"2026.01.09县人大十七届六次当选"},

    # ── 邓之武 ──
    {"id":13,"person_id":3,"org_id":11,"title":"南昌市外经贸委区域合作处副处长→投资促进处处长（~9年）","start":"2002-05","end":"2015-09","rank":"科级","note":""},
    {"id":14,"person_id":3,"org_id":10,"title":"南昌市投资促进局副局长","start":"2015-09","end":"2019-06","rank":"副处级","note":"2017-2018借调南昌高新区"},
    {"id":15,"person_id":3,"org_id":8,"title":"进贤县委常委→组织部长→常务副县长","start":"2019-06","end":"2025-01","rank":"副处级","note":"2021.08组织部长，2023.02常务副县长"},
    {"id":16,"person_id":3,"org_id":1,"title":"南昌县委副书记","start":"2025-01","end":"2026-07","rank":"副厅级","note":"在贾彧超领导下工作约6个月"},
    {"id":17,"person_id":3,"org_id":6,"title":"东湖区委副书记、代区长","start":"2026-07","end":"","rank":"正处级","note":"2026.07.07任命"},

    # ── 陈翔 ──
    {"id":18,"person_id":4,"org_id":22,"title":"南昌市经贸委→新建县副县长→青云谱区委组织部长","start":"1992","end":"2014","rank":"科级→副处级","note":""},
    {"id":19,"person_id":4,"org_id":2,"title":"南昌县委常委、副县长（常务）","start":"2014-11","end":"2016-07","rank":"副处级","note":""},
    {"id":20,"person_id":4,"org_id":2,"title":"南昌县委副书记、县长","start":"2016-07","end":"2021-07","rank":"副厅级","note":""},
    {"id":21,"person_id":4,"org_id":1,"title":"南昌县委书记、小蓝经开区党工委书记","start":"2021-07","end":"2025-02","rank":"副厅级","note":"贾彧超接替"},

    # ── 徐志勇 ──
    {"id":22,"person_id":5,"org_id":12,"title":"安义县长埠镇镇长→书记→安义县委办主任→审计局长","start":"~2012","end":"2021-01","rank":"正科级","note":"在安义县工作约8年；2016-2021与熊振强同县重叠5年"},
    {"id":23,"person_id":5,"org_id":25,"title":"西湖区副区长","start":"2021-01","end":"2021-09","rank":"副处级","note":""},
    {"id":24,"person_id":5,"org_id":17,"title":"青云谱区委常委、纪委书记→常务副区长","start":"2021-09","end":"2024-10","rank":"副处级","note":""},
    {"id":25,"person_id":5,"org_id":2,"title":"南昌县委常委、常务副县长","start":"2024-10-25","end":"","rank":"副处级","note":""},

    # ── 邬春华 ──
    {"id":26,"person_id":6,"org_id":19,"title":"红谷滩新区管委会办公室副主任→主任→党群工作部部长","start":"2003-02","end":"2021-08","rank":"科级→正科级","note":"在红谷滩工作18年"},
    {"id":27,"person_id":6,"org_id":1,"title":"南昌县委常委、组织部部长","start":"2021-09","end":"","rank":"副处级","note":"兼县委党校校长；丰城人，与徐永钢同乡"},

    # ── 熊运浪 ──
    {"id":28,"person_id":18,"org_id":1,"title":"南昌县委书记（2019.12-2021.08）","start":"2019-12","end":"2021-08","rank":"副厅级","note":"全国优秀县委书记（2021）"},
    {"id":29,"person_id":18,"org_id":27,"title":"江西省委政法委副书记（正厅长级）","start":"2025","end":"","rank":"正厅级","note":"南昌市委常委→赣州市委副书记→萍乡市长→省委政法委"},

    # ── 闵员根 ──
    {"id":30,"person_id":19,"org_id":1,"title":"南昌县委常委、政法委书记→县委副书记","start":"2016","end":"2024-10","rank":"副处级","note":"南昌县工作30年"},
    {"id":31,"person_id":19,"org_id":16,"title":"西湖区人大常委会主任","start":"2024-11","end":"","rank":"正处级","note":""},

    # ── 陶亿国 ──
    {"id":32,"person_id":20,"org_id":2,"title":"南昌县副县长→县委常委、常务副县长","start":"2015","end":"2021-02","rank":"副处级","note":"南昌县工作25年"},
    {"id":33,"person_id":20,"org_id":16,"title":"西湖区委副书记、区长→区委书记","start":"2021-03","end":"2025-08","rank":"正处级","note":""},

    # ── 付向宇 ──
    {"id":34,"person_id":21,"org_id":9,"title":"进贤县法院→政法委→李渡镇→白圩乡书记","start":"1998","end":"2016","rank":"科员→正科级","note":"进贤县工作18年"},
    {"id":35,"person_id":21,"org_id":2,"title":"南昌县副县长→常务副县长","start":"2016-08","end":"2023-07","rank":"副处级","note":"进贤籍，在南昌县任职7年"},
    {"id":36,"person_id":21,"org_id":7,"title":"南昌市商务局党组书记、局长","start":"2024-12","end":"","rank":"正处级","note":""},

    # ── 熊军 ──
    {"id":37,"person_id":22,"org_id":14,"title":"南昌县黄马乡党委书记","start":"2016-06","end":"2021-03","rank":"正科级","note":"与徐永钢（乡长）搭班子3年（2016-2019）"},
    {"id":38,"person_id":22,"org_id":9,"title":"进贤县副县长","start":"2021-10","end":"","rank":"副处级","note":"南昌县→进贤县 黄马线"},

    # ── 徐永钢 ──
    {"id":39,"person_id":23,"org_id":14,"title":"南昌县黄马乡党委副书记、乡长","start":"2016-06","end":"2019-03","rank":"正科级","note":"与熊军（书记）搭班子3年"},
    {"id":40,"person_id":23,"org_id":15,"title":"南昌县武阳镇党委书记","start":"2020-11","end":"2021-01","rank":"正科级","note":""},
    {"id":41,"person_id":23,"org_id":9,"title":"进贤县副县长","start":"2021-01","end":"2023-05","rank":"副处级","note":"南昌县→进贤县 黄马线"},
    {"id":42,"person_id":23,"org_id":8,"title":"进贤县委常委、组织部部长","start":"2023-05","end":"","rank":"副处级","note":"丰城人，与邬春华同乡"},

    # ── 聂红兵 ──
    {"id":43,"person_id":24,"org_id":3,"title":"小蓝经开区招商中心主任→招商局局长","start":"2017-05","end":"2024-01","rank":"正科级→副处级","note":"小蓝位于南昌县境内"},
    {"id":44,"person_id":24,"org_id":9,"title":"进贤县委常委、副县长","start":"2024-02","end":"","rank":"副处级","note":"小蓝→进贤 开发区桥"},

    # ── 徐强 ──
    {"id":45,"person_id":27,"org_id":1,"title":"进贤县委书记","start":"2021-08","end":"2026-06","rank":"正处级","note":"南昌县籍"},
    {"id":46,"person_id":27,"org_id":20,"title":"新建区委书记","start":"2026-06","end":"","rank":"正处级","note":""},

    # ── 熊振强 ──
    {"id":47,"person_id":25,"org_id":13,"title":"安义县委常委、工业园区党工委书记→政法委书记","start":"2016-07","end":"2021-09","rank":"副处级","note":"与徐志勇在安义县重叠5年"},
    {"id":48,"person_id":25,"org_id":8,"title":"进贤县委书记","start":"2026-06","end":"","rank":"正处级","note":""},

    # ── 雷桥亮 ──
    {"id":49,"person_id":26,"org_id":21,"title":"南昌高新区党工委委员、管委会副主任","start":"2022-05","end":"2022-12","rank":"副处级","note":""},
    {"id":50,"person_id":26,"org_id":4,"title":"南昌市发改委党组书记、主任","start":"2022-12","end":"2026-06","rank":"正处级","note":"贾彧超离开后，中间隔张平、雷强两任"},
    {"id":51,"person_id":26,"org_id":9,"title":"进贤县委副书记、代县长","start":"2026-07","end":"","rank":"正处级","note":""},

    # ── 肖玉文 ──
    {"id":52,"person_id":29,"org_id":2,"title":"南昌县委常委、常务副县长→县长→县委书记","start":"2004-04","end":"2011-09","rank":"副处级→正处级","note":"2025.11被查"},

    # ── 刘志伟 ──
    {"id":53,"person_id":28,"org_id":28,"title":"南昌县幽兰镇党委书记","start":"","end":"2020","rank":"正科级","note":""},
    {"id":54,"person_id":28,"org_id":12,"title":"安义县副县长→县委副书记、代县长","start":"2020-04","end":"","rank":"副处级→正处级","note":"南昌县→安义县"},

    # ── 刘光荣 ──
    {"id":55,"person_id":30,"org_id":6,"title":"东湖区委书记","start":"2025-02","end":"","rank":"正处级","note":"南昌县21年工作经历→东湖区"},
]

relationships = [
    {"id":1,"person_a":1,"person_b":3,"type":"直接上下级","context":"贾彧超（南昌县委书记）直接领导邓之武（南昌县委副书记）约6个月（2025.01-2025.07），之后邓升任东湖区代区长","overlap_org":"南昌县","overlap_period":"2025-01至2025-07"},
    {"id":2,"person_a":1,"person_b":2,"type":"党政搭档","context":"贾彧超（县委书记）与帅志（县长）为南昌县党政一把手搭档","overlap_org":"南昌县","overlap_period":"2026-01至今"},
    {"id":3,"person_a":1,"person_b":4,"type":"职务接替","context":"贾彧超2025.02接替陈翔任南昌县委书记（陈翔调南昌市政府）","overlap_org":"南昌县","overlap_period":"不重叠（前后任）"},
    {"id":4,"person_a":2,"person_b":5,"type":"县政府搭档","context":"帅志（县长）与徐志勇（常务副县长）搭档","overlap_org":"南昌县人民政府","overlap_period":"2026-01至今"},
    {"id":5,"person_a":5,"person_b":25,"type":"安义县重叠5年","context":"徐志勇在安义县工作期间（~2012-2021），与熊振强（安义县委常委2016-2021）重叠约5年。2017年二人曾共同陪同安义县委书记李松殿赴深圳考察","overlap_org":"安义县","overlap_period":"2016-07至2021-01"},
    {"id":6,"person_a":6,"person_b":23,"type":"丰城同乡","context":"邬春华（1971，丰城人）与徐永钢（1981，丰城人）同为丰城籍，目前分别担任南昌县委组织部长和进贤县委组织部长","overlap_org":"无直接共事","overlap_period":"无重叠"},
    {"id":7,"person_a":22,"person_b":23,"type":"⭐直接上下级+黄马线","context":"熊军（书记）与徐永钢（乡长）在南昌县黄马乡搭班子3年（2016-2019），后二人先后调入进贤县","overlap_org":"南昌县黄马乡","overlap_period":"2016-06至2019-03"},
    {"id":8,"person_a":22,"person_b":23,"type":"进贤县同事","context":"熊军与徐永钢在进贤县政府班子重叠约2年（2021.10-2023.05），徐之后升任组织部长","overlap_org":"进贤县","overlap_period":"2021-10至2023-05"},
    {"id":9,"person_a":24,"person_b":3,"type":"小蓝→进贤桥","context":"聂红兵（小蓝经开区招商局长→进贤副县长2024.02）","overlap_org":"小蓝经开区","overlap_period":"不直接重叠"},
    {"id":10,"person_a":3,"person_b":27,"type":"进贤→东湖→新建三国","context":"邓之武（进贤常务副县长→南昌县委副书记→东湖代区长）、徐强（进贤书记→新建书记）均为进贤系统出身","overlap_org":"进贤县","overlap_period":"2019至2024（邓在进贤，徐在进贤）"},
    {"id":11,"person_a":1,"person_b":26,"type":"市发改委前后任","context":"贾彧超（市发改委主任2020-2021）与雷桥亮（市发改委主任2022-2026）中间隔着张平、雷强两任，无直接关系","overlap_org":"南昌市发改委","overlap_period":"不重叠"},
    {"id":12,"person_a":2,"person_b":10,"type":"市纪委系统关系","context":"帅志（市纪委副书记2021-2025）与黄淦明（市纪委市监委第九室主任→南昌县纪委书记2025）曾在市纪委共事","overlap_org":"南昌市纪委","overlap_period":"2021至2025"},
    {"id":13,"person_a":21,"person_b":22,"type":"进贤→南昌县→进贤","context":"付向宇（进贤籍，南昌县常务副县长→市商务局长）走了进贤→南昌县→市直的路径，与熊军相反方向","overlap_org":"进贤/南昌县","overlap_period":"不重叠"},
    {"id":14,"person_a":18,"person_b":1,"type":"南昌县委书记接替链","context":"熊运浪（2019-2021）→陈翔（2021-2025）→贾彧超（2025-）——南昌县委书记三年一换已成规律","overlap_org":"南昌县","overlap_period":"不重叠（前后任）"},
    {"id":15,"person_a":28,"person_b":12,"type":"南昌县→安义县通道","context":"刘志伟（南昌县幽兰镇书记→安义副县长→代县长）是南昌县乡镇主官输送到安义县的典型案例","overlap_org":"南昌县→安义县","overlap_period":"2020-04至今"},
    {"id":16,"person_a":3,"person_b":1,"type":"邓之武18个月三级跳","context":"邓之武2025.01进贤常务副县长→2025.01南昌县委副书记→2026.07东湖区代区长，仅18个月","overlap_org":"南昌县/东湖区","overlap_period":"2025-01至2026-07"},
    {"id":17,"person_a":5,"person_b":25,"type":"安义→南昌县→进贤三角","context":"徐志勇（安义→南昌县常务副县长）与熊振强（安义→进贤县委书记）在安义重叠5年后分赴两个县的关键岗位","overlap_org":"安义县","overlap_period":"2016-2021"},
    {"id":18,"person_a":4,"person_b":1,"type":"前任→南昌市政府","context":"陈翔辞去南昌县委书记后调任南昌市政府二级巡视员","overlap_org":"南昌县","overlap_period":"不重叠（前后任）"},
]

# ── BUILD SQLITE ──
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

# ── BUILD GEXF ──
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "县委书记" in post and "县委" in post: return "255,50,50"
    elif "县长" in post or "副县长" in post or "代县长" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200","乡镇":"255,255,200","事业单位":"220,220,220","群团":"255,220,255","人大":"200,255,255","政协":"255,240,200","新区":"255,220,220"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>南昌县领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    sz = "20.0" if "书记" in p.get("current_post","") and "县委" in p.get("current_post","") else "12.0"
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
