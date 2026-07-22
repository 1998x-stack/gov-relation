#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 西湖区 (Xihu District) leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/xihu_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/xihu_network.gexf")

# ── PERSONS ──
persons = [
    # Current 区委
    {"id":1,"name":"陈建军","gender":"男","ethnicity":"汉族","birth":"1974年9月","birthplace":"江西南昌","education":"东北财经大学统计学在职研究生","party_join":"1994年6月","work_start":"","current_post":"西湖区委书记","current_org":"中共南昌市西湖区委员会","source":"https://www.xihuqu.gov.cn/zwgk/ldzc/202607/t20260702_10066051.shtml"},
    # Current/outgoing 区长
    {"id":2,"name":"杨燊","gender":"男","ethnicity":"汉族","birth":"1983年4月","birthplace":"江西瑞金","education":"硕士研究生（南昌大学）","party_join":"2005年12月","work_start":"2003年7月","current_post":"（原西湖区委副书记、区长，已离任）","current_org":"","source":"https://baike.baidu.com/item/%E6%9D%A8%E7%87%8A/62602231"},
    # New 代区长
    {"id":3,"name":"余耀武","gender":"男","ethnicity":"汉族","birth":"1978年10月","birthplace":"江西南昌","education":"中央党校大专","party_join":"1999年12月","work_start":"1996年8月","current_post":"西湖区委副书记、代区长","current_org":"南昌市西湖区人民政府","source":"https://www.xihuqu.gov.cn/zwgk/ldzc/202607/t20260702_10066051.shtml"},
    # 常委/纪委书记
    {"id":4,"name":"陈韬","gender":"男","ethnicity":"汉族","birth":"1981年8月","birthplace":"江西进贤","education":"大学","party_join":"2005年6月","work_start":"2003年7月","current_post":"西湖区委常委、纪委书记、监委主任","current_org":"中共南昌市西湖区纪律检查委员会","source":"https://new.qq.com/rain/a/20210925A08A1100"},
    # 常委/统战部长
    {"id":5,"name":"余铭","gender":"男","ethnicity":"汉族","birth":"1971年1月","birthplace":"江西抚州","education":"在职研究生","party_join":"1991年11月","work_start":"1990年3月","current_post":"西湖区委常委、统战部部长","current_org":"中共南昌市西湖区委员会","source":"https://baike.baidu.com/item/%E4%BD%99%E9%93%AD"},
    # 常委/宣传部长
    {"id":6,"name":"郭小玲","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区委常委、宣传部部长","current_org":"中共南昌市西湖区委员会","source":"https://www.xihuqu.gov.cn"},
    # 常委/常务副区长
    {"id":7,"name":"胡海","gender":"男","ethnicity":"汉族","birth":"1976年11月","birthplace":"江西南昌","education":"大学（南昌师范学校）","party_join":"1997年12月","work_start":"1994年8月","current_post":"西湖区委常委、常务副区长","current_org":"南昌市西湖区人民政府","source":"https://baike.baidu.com/item/%E8%83%A1%E6%B5%B7"},
    # 常委
    {"id":8,"name":"吕东锦","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区委常委","current_org":"中共南昌市西湖区委员会","source":"https://www.xihuqu.gov.cn"},
    # 常委
    {"id":9,"name":"李隽","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区委常委","current_org":"中共南昌市西湖区委员会","source":"https://www.xihuqu.gov.cn"},
    # 常委
    {"id":10,"name":"吴斌清","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区委常委","current_org":"中共南昌市西湖区委员会","source":"https://www.xihuqu.gov.cn"},
    # 常委（人武部）
    {"id":11,"name":"徐建云","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区委常委、人武部部长","current_org":"南昌市西湖区人民武装部","source":"https://www.xihuqu.gov.cn"},
    # 副区长
    {"id":12,"name":"杨金平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区副区长","current_org":"南昌市西湖区人民政府","source":"https://www.xihuqu.gov.cn"},
    # 副区长
    {"id":13,"name":"熊珊阳","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区副区长","current_org":"南昌市西湖区人民政府","source":"https://www.xihuqu.gov.cn"},
    # 副区长
    {"id":14,"name":"宋德豪","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区副区长","current_org":"南昌市西湖区人民政府","source":"https://www.xihuqu.gov.cn"},
    # 副区长
    {"id":15,"name":"李辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"西湖区副区长","current_org":"南昌市西湖区人民政府","source":"https://www.xihuqu.gov.cn"},
    # 人大主任
    {"id":16,"name":"闵员根","gender":"男","ethnicity":"汉族","birth":"1969年2月","birthplace":"江西南昌县","education":"省委党校研究生","party_join":"中共党员","work_start":"1990年9月","current_post":"西湖区人大常委会主任","current_org":"西湖区人大常委会","source":"https://baike.baidu.com/item/%E9%97%B5%E5%91%98%E6%A0%B9/23710218"},
    # 原区委书记（前任）
    {"id":17,"name":"陶亿国","gender":"男","ethnicity":"汉族","birth":"1973年8月","birthplace":"江西南昌县","education":"江西农大兽医+江西财大MBA","party_join":"1995年6月","work_start":"1996年12月","current_post":"赣江新区管委会副主任（原西湖区委书记）","current_org":"赣江新区管委会","source":"https://baike.baidu.com/item/%E9%99%B6%E4%BA%BF%E5%9B%BD/14840701"},
    # 原区长更早的前任（陶亿国曾任区长后任书记）
    {"id":18,"name":"黄小燕","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原西湖区委书记，去向待查）","current_org":"","source":"https://news.sina.com.cn"},
    # 原区委副书记/熊振强（已调离）
    {"id":19,"name":"熊振强","gender":"男","ethnicity":"汉族","birth":"1972年3月","birthplace":"江西奉新","education":"大学","party_join":"1992年12月","work_start":"1991年9月","current_post":"进贤县委书记（原西湖区委副书记）","current_org":"中共进贤县委员会","source":"https://baike.baidu.com/item/%E7%86%8A%E6%8C%AF%E5%BC%BA/7691320"},
    # 前副区长江珊（已调东湖）
    {"id":20,"name":"江珊","gender":"女","ethnicity":"汉族","birth":"1983年11月","birthplace":"江西黎川","education":"大学","party_join":"中共党员","work_start":"","current_post":"东湖区副区长（原西湖区街道书记→副区长）","current_org":"南昌市东湖区人民政府","source":"https://dhq.nc.gov.cn"},
    # 前副区长牛浩（已调青山湖）
    {"id":21,"name":"牛浩","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"青山湖区委常委、统战部部长（原西湖区副区长）","current_org":"中共青山湖区委员会","source":"https://qsh.nc.gov.cn"},
    # 前组织部部长王新（原西湖区委常委、组织部部长，已调离）
    {"id":22,"name":"万勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原西湖区委常委、政法委书记，去向待查）","current_org":"","source":"https://www.xihuqu.gov.cn"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共南昌市西湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市西湖区"},
    {"id":2,"name":"南昌市西湖区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市西湖区"},
    {"id":3,"name":"中共南昌市西湖区纪律检查委员会","type":"党委","level":"区级","parent":"南昌市纪律检查委员会","location":"江西省南昌市西湖区"},
    {"id":4,"name":"南昌市西湖区人民武装部","type":"军队","level":"区级","parent":"南昌警备区","location":"江西省南昌市西湖区"},
    {"id":5,"name":"西湖区人大常委会","type":"人大","level":"区级","parent":"南昌市人大常委会","location":"江西省南昌市西湖区"},
    {"id":6,"name":"中共南昌市委员会","type":"党委","level":"市级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":7,"name":"南昌市人民政府","type":"政府","level":"市级","parent":"","location":"江西省南昌市"},
    {"id":8,"name":"赣江新区管委会","type":"开发区","level":"国家级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":9,"name":"中共新建区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市新建区"},
    {"id":10,"name":"新建区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市新建区"},
    {"id":11,"name":"南昌市商务局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":12,"name":"南昌市国有资产监督管理委员会","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":13,"name":"中共湾里区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市湾里区"},  # historical, now 湾里管理局
    {"id":14,"name":"南昌市机关事务管理局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":15,"name":"中共进贤县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市进贤县"},
    {"id":16,"name":"进贤县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市进贤县"},
    {"id":17,"name":"南昌市人民政府驻北京办事处","type":"政府","level":"市级","parent":"南昌市人民政府","location":"北京市"},
    {"id":18,"name":"青云谱区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市青云谱区"},
    {"id":19,"name":"南昌市西湖区朝阳洲街道","type":"乡镇","level":"乡镇级","parent":"西湖区人民政府","location":"江西省南昌市西湖区"},
    {"id":20,"name":"南昌市西湖区教育体育局","type":"政府","level":"区级","parent":"西湖区人民政府","location":"江西省南昌市西湖区"},
    {"id":21,"name":"南昌市公安局西湖分局","type":"政府","level":"区级","parent":"南昌市公安局","location":"江西省南昌市西湖区"},
    {"id":22,"name":"中共青山湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市青山湖区"},
    {"id":23,"name":"南昌市东湖区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市东湖区"},
]

# ── POSITIONS ──
positions = [
    # 陈建军(1) — current 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"西湖区委书记","start":"2025-12","end":"","rank":"正处级","note":"2025年12月任西湖区委书记，此前任南昌市国资委主任"},
    {"id":2,"person_id":1,"org_id":13,"title":"湾里区委常委、纪委书记","start":"~2016","end":"~2019","rank":"副处级","note":""},
    {"id":3,"person_id":1,"org_id":9,"title":"新建区委副书记","start":"~2019-06","end":"~2019","rank":"正处级","note":"2019年6月任新建区委副书记"},
    {"id":4,"person_id":1,"org_id":11,"title":"南昌市商务局党组书记、局长","start":"2019-06","end":"~2022","rank":"正处级","note":"从新建区委副书记调任"},
    {"id":5,"person_id":1,"org_id":12,"title":"南昌市国资委党委书记、主任","start":"~2022","end":"2025-12","rank":"正处级","note":"一级调研员"},
    {"id":6,"person_id":1,"org_id":1,"title":"西湖区委书记、一级调研员","start":"2025-12","end":"","rank":"正处级","note":"2025年11月任前公示，12月到任"},
    # 杨燊(2) — 原区长
    {"id":7,"person_id":2,"org_id":1,"title":"西湖区委副书记、区长","start":"2022-06","end":"2026-07","rank":"正处级","note":"2022年6月代区长，6月25日当选区长"},
    {"id":8,"person_id":2,"org_id":17,"title":"南昌市政府驻北京办事处干部","start":"~2020","end":"2022-06","rank":"","note":"此前在北京办事处工作"},
    # 余耀武(3) — 新任代区长
    {"id":9,"person_id":3,"org_id":1,"title":"西湖区委副书记、代区长","start":"2026-07-07","end":"","rank":"正处级","note":"2026年7月7日人大常委会任命"},
    {"id":10,"person_id":3,"org_id":14,"title":"南昌市机关事务管理局局长","start":"2025-09","end":"2026-07","rank":"正处级","note":"2025年9月任"},
    {"id":11,"person_id":3,"org_id":9,"title":"新建区委常委、副区长","start":"~2021","end":"2025-09","rank":"副处级","note":"新建区委常委、区政府副区长"},
    {"id":12,"person_id":3,"org_id":10,"title":"新建区副区长","start":"~2021","end":"","rank":"副处级","note":"2021年8月任前公示"},
    {"id":13,"person_id":3,"org_id":9,"title":"新建区溪霞镇党委书记","start":"~2016","end":"~2021","rank":"正科级","note":"南昌溪霞国家农业综合开发现代农业园区党工委书记"},
    # 陈韬(4) — 纪委书记
    {"id":14,"person_id":4,"org_id":3,"title":"西湖区委常委、纪委书记、监委主任","start":"2021-09","end":"","rank":"副处级","note":"2021年9月任区委常委、纪委书记，后任监委主任"},
    {"id":15,"person_id":4,"org_id":18,"title":"青山湖区政府副区长","start":"~2020","end":"2021-09","rank":"副处级","note":""},
    {"id":16,"person_id":4,"org_id":9,"title":"新建县大塘坪乡党委副书记、乡长","start":"~2015","end":"~2020","rank":"正科级","note":""},
    {"id":17,"person_id":4,"org_id":16,"title":"进贤县委常委、宣传部部长","start":"~2019","end":"~2020","rank":"副处级","note":""},
    # 余铭(5) — 统战部长
    {"id":18,"person_id":5,"org_id":1,"title":"西湖区委常委、统战部部长","start":"~2021","end":"","rank":"副处级","note":"现任"},
    # 郭小玲(6) — 宣传部长
    {"id":19,"person_id":6,"org_id":1,"title":"西湖区委常委、宣传部部长","start":"~2021","end":"","rank":"副处级","note":"2021年10月起任宣传部部长"},
    # 胡海(7) — 常务副区长
    {"id":20,"person_id":7,"org_id":2,"title":"西湖区委常委、常务副区长","start":"~2023","end":"","rank":"副处级","note":"区委常委、区政府党组副书记、常务副区长"},
    {"id":21,"person_id":7,"org_id":2,"title":"西湖区副区长","start":"~2021-01","end":"~2023","rank":"副处级","note":"2021年1月任"},
    {"id":22,"person_id":7,"org_id":19,"title":"西湖区朝阳洲街道党工委书记","start":"~2019","end":"~2021-01","rank":"正科级","note":""},
    {"id":23,"person_id":7,"org_id":20,"title":"西湖区教育体育局党委委员","start":"~2015","end":"~2019","rank":"","note":"曾任华安学校校长等职"},
    # 吕东锦(8) — 常委
    {"id":24,"person_id":8,"org_id":1,"title":"西湖区委常委","start":"","end":"","rank":"副处级","note":""},
    # 李隽(9) — 常委
    {"id":25,"person_id":9,"org_id":1,"title":"西湖区委常委","start":"","end":"","rank":"副处级","note":""},
    # 吴斌清(10) — 常委
    {"id":26,"person_id":10,"org_id":1,"title":"西湖区委常委","start":"","end":"","rank":"副处级","note":""},
    # 徐建云(11) — 人武部长
    {"id":27,"person_id":11,"org_id":4,"title":"西湖区委常委、人武部部长","start":"","end":"","rank":"副处级","note":""},
    # 杨金平(12) — 副区长
    {"id":28,"person_id":12,"org_id":2,"title":"西湖区副区长","start":"","end":"","rank":"副处级","note":""},
    # 熊珊阳(13) — 副区长
    {"id":29,"person_id":13,"org_id":2,"title":"西湖区副区长","start":"","end":"","rank":"副处级","note":""},
    # 宋德豪(14) — 副区长
    {"id":30,"person_id":14,"org_id":2,"title":"西湖区副区长","start":"","end":"","rank":"副处级","note":""},
    # 李辉(15) — 副区长
    {"id":31,"person_id":15,"org_id":2,"title":"西湖区副区长","start":"","end":"","rank":"副处级","note":""},
    # 闵员根(16) — 人大主任
    {"id":32,"person_id":16,"org_id":5,"title":"西湖区人大常委会主任","start":"2024-11","end":"","rank":"正处级","note":"原南昌县委副书记调任"},
    {"id":33,"person_id":16,"org_id":15,"title":"南昌县委副书记","start":"~2016","end":"2024-10","rank":"副处级","note":"南昌县工作约30年"},
    # 陶亿国(17) — 前任书记
    {"id":34,"person_id":17,"org_id":1,"title":"西湖区委副书记、区长→区委书记","start":"2021-03","end":"2025-08","rank":"正处级","note":"2021年3月任区长，后升任书记至2025年8月"},
    {"id":35,"person_id":17,"org_id":8,"title":"赣江新区管委会副主任","start":"2025-09","end":"","rank":"副厅级","note":"2025年9月调任赣江新区"},
    # 熊振强(19) — 原区委副书记
    {"id":36,"person_id":19,"org_id":1,"title":"西湖区委副书记","start":"~2021","end":"~2024","rank":"副处级","note":"在陶亿国/杨燊班子中任副书记"},
    {"id":37,"person_id":19,"org_id":15,"title":"进贤县委书记","start":"~2025","end":"","rank":"正处级","note":""},
    # 江珊(20) — 原西湖区副区长
    {"id":38,"person_id":20,"org_id":2,"title":"西湖区副区长（曾任街道书记）","start":"~2021","end":"2023-10","rank":"副处级","note":"从西湖区系马桩街办、南浦街道书记升任"},
    {"id":39,"person_id":20,"org_id":23,"title":"东湖区副区长","start":"2023-10","end":"","rank":"副处级","note":"调任东湖区副区长"},
    # 牛浩(21) — 原西湖区副区长
    {"id":40,"person_id":21,"org_id":2,"title":"西湖区副区长","start":"2021-08","end":"2023-07","rank":"副处级","note":""},
    {"id":41,"person_id":21,"org_id":22,"title":"青山湖区委常委、统战部部长","start":"2023-07","end":"","rank":"副处级","note":""},
    # 万勇(22) — 原政法委书记
    {"id":42,"person_id":22,"org_id":1,"title":"西湖区委常委、政法委书记","start":"~2021","end":"~2024","rank":"副处级","note":"2021-2024年任"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 党政搭档
    {"id":1,"person_a":1,"person_b":3,"type":"党政搭档","context":"陈建军（区委书记）与余耀武（代区长）为西湖区党政一把手","overlap_org":"西湖区","overlap_period":"2026-07至今"},
    {"id":2,"person_a":1,"person_b":2,"type":"党政搭档","context":"陈建军（区委书记）与杨燊（原区长）曾为西湖区党政搭档","overlap_org":"西湖区","overlap_period":"2025-12至2026-07"},
    # 职务接替 - 书记
    {"id":3,"person_a":17,"person_b":1,"type":"职务接替","context":"陶亿国（原书记）→ 陈建军任西湖区委书记","overlap_org":"西湖区委","overlap_period":"不重叠（前后任）"},
    # 职务接替 - 区长
    {"id":4,"person_a":2,"person_b":3,"type":"职务接替","context":"杨燊（原区长）→ 余耀武任西湖代区长","overlap_org":"西湖区政府","overlap_period":"不重叠（前后任）"},
    # 常委会班子的强关系
    {"id":5,"person_a":1,"person_b":4,"type":"班子同事","context":"陈建军（书记）与陈韬（纪委书记）为区委班子","overlap_org":"西湖区委","overlap_period":"2025-12至今"},
    {"id":6,"person_a":1,"person_b":5,"type":"班子同事","context":"陈建军（书记）与余铭（统战部长）为区委班子","overlap_org":"西湖区委","overlap_period":"2025-12至今"},
    {"id":7,"person_a":1,"person_b":6,"type":"班子同事","context":"陈建军（书记）与郭小玲（宣传部长）为区委班子","overlap_org":"西湖区委","overlap_period":"2025-12至今"},
    {"id":8,"person_a":1,"person_b":7,"type":"班子同事","context":"陈建军（书记）与胡海（常务副区长）为区委班子","overlap_org":"西湖区","overlap_period":"2025-12至今"},
    # 熊振强与进贤县的联系
    {"id":9,"person_a":19,"person_b":17,"type":"前同僚","context":"熊振强（原西湖区委副书记）与陶亿国（原西湖区委书记）曾在西湖区班子共事","overlap_org":"西湖区委","overlap_period":"~2021-~2024"},
    # 江珊从西湖区调东湖区
    {"id":10,"person_a":20,"person_b":17,"type":"上下级","context":"江珊（原西湖区副区长）曾在陶亿国（原书记）班子中工作","overlap_org":"西湖区政府","overlap_period":"~2021-2023-10"},
    # 牛浩从西湖区调青山湖区
    {"id":11,"person_a":21,"person_b":17,"type":"上下级","context":"牛浩（原西湖区副区长）曾在陶亿国（原书记）班子中工作","overlap_org":"西湖区政府","overlap_period":"2021-08至2023-07"},
    # 闵员根与西湖区
    {"id":12,"person_a":16,"person_b":17,"type":"同僚","context":"闵员根（西湖区人大主任）与陶亿国（原书记）在西湖区共事","overlap_org":"西湖区","overlap_period":"2024-11至2025-08"},
    # 陈建军之前在湾里区/新建区/商务局/国资委的经历
    {"id":13,"person_a":1,"person_b":17,"type":"职务接替（书记）","context":"陈建军接替陶亿国任西湖区委书记","overlap_org":"西湖区委","overlap_period":"不重叠（前后任）"},
    # 余耀武从新建区调来
    {"id":14,"person_a":3,"person_b":2,"type":"职务接替（区长）","context":"余耀武接替杨燊任西湖区代区长","overlap_org":"西湖区政府","overlap_period":"不重叠（前后任）"},
    # 陈韬与进贤县联系
    {"id":15,"person_a":4,"person_b":4,"type":"进贤籍贯","context":"陈韬（纪委书记）与陈韬本人进贤籍；熊振强也是进贤县委书记","overlap_org":"进贤县","overlap_period":""},
    # 胡海长期在西湖区工作
    {"id":16,"person_a":7,"person_b":1,"type":"上下级","context":"胡海（常务副区长）为陈建军（书记）的班子成员","overlap_org":"西湖区","overlap_period":"2025-12至今"},
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
    if "区委书记" in post: return "255,50,50"
    elif "区长" in post or "副区长" in post or "代区长" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    elif "政法委" in post: return "150,100,200"
    elif "宣传部" in post: return "100,200,150"
    elif "组织部" in post: return "200,150,100"
    elif "统战部" in post: return "200,100,150"
    elif "人武部" in post: return "100,150,100"
    elif "人大" in post: return "100,200,200"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","群团":"255,220,255","事业单位":"220,220,220","开发区":"200,255,200","国企":"255,255,200","军队":"180,180,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>南昌市西湖区领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    # Size: party secretary = 20, gov leader = 20, others = 12
    post = p.get("current_post","")
    if "书记" in post and "区委" in post and "纪委" not in post and "人大" not in post:
        sz = "20.0"
    elif "区长" in post or "代区长" in post:
        sz = "20.0"
    elif "副区长" in post:
        sz = "14.0"
    elif "常委" in post:
        sz = "12.0"
    elif "人大" in post:
        sz = "12.0"
    else:
        sz = "12.0"
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
    lines.append('      </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
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
