#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 新建区 (Xinjian District) leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/xinjian_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/xinjian_network.gexf")

# ── PERSONS ──
persons = [
    # ── Top leaders ──
    # 徐强 — 区委书记 (2026-07上任)
    {"id":1,"name":"徐强","gender":"男","ethnicity":"汉族","birth":"1974-11","birthplace":"江西南昌县","education":"南昌航空工业学院+江西财大MPA","party_join":"1996-06","work_start":"1996-09","current_post":"新建区委书记","current_org":"中共南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    # 兰杨丽 — 区委副书记、区长
    {"id":2,"name":"兰杨丽","gender":"女","ethnicity":"畲族","birth":"1975-12","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"新建区委副书记、区长","current_org":"南昌市新建区人民政府","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},

    # ── 区委常委 (区委领导) ──
    {"id":3,"name":"彭达兵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委、副区长","current_org":"南昌市新建区人民政府","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":4,"name":"冯健","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委","current_org":"中共南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":5,"name":"贾中强","gender":"男","ethnicity":"汉族","birth":"1984-06","birthplace":"","education":"大学","party_join":"中共党员","work_start":"","current_post":"新建区委常委、常务副区长","current_org":"南昌市新建区人民政府","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":6,"name":"黄永强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委、政法委书记","current_org":"中共南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":7,"name":"吴梅萍","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委、宣传部部长","current_org":"中共南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":8,"name":"戴军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委、纪委书记、监委主任","current_org":"中共南昌市新建区纪律检查委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":9,"name":"夏辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委、组织部部长","current_org":"中共南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":10,"name":"杨文军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委","current_org":"中共南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":11,"name":"李葵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委常委、统战部部长","current_org":"中共南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},

    # ── 区政府副区长 ──
    {"id":12,"name":"胡燕琴","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区副区长","current_org":"南昌市新建区人民政府","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":13,"name":"钱治华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区副区长","current_org":"南昌市新建区人民政府","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":14,"name":"李和风","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区副区长","current_org":"南昌市新建区人民政府","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":15,"name":"王锋海","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区副区长、公安分局局长","current_org":"南昌市公安局新建分局","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":16,"name":"万里晴","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区副区长","current_org":"南昌市新建区人民政府","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},

    # ── 区人大领导 ──
    {"id":17,"name":"涂莉花","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区人大常委会主任","current_org":"南昌市新建区人民代表大会常务委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":18,"name":"陈文辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区人大常委会副主任","current_org":"南昌市新建区人民代表大会常务委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":19,"name":"詹碧涛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区人大常委会副主任","current_org":"南昌市新建区人民代表大会常务委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":20,"name":"夏天明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区人大常委会副主任","current_org":"南昌市新建区人民代表大会常务委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":21,"name":"陈国伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区人大常委会副主任","current_org":"南昌市新建区人民代表大会常务委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":22,"name":"万红玲","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区人大常委会副主任","current_org":"南昌市新建区人民代表大会常务委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":23,"name":"程伟川","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区人大常委会副主任","current_org":"南昌市新建区人民代表大会常务委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},

    # ── 区政协领导 ──
    {"id":24,"name":"黄云松","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区政协主席","current_org":"中国人民政治协商会议南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":25,"name":"刘建新","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区政协副主席","current_org":"中国人民政治协商会议南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":26,"name":"李成星","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区政协副主席","current_org":"中国人民政治协商会议南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":27,"name":"熊有炳","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区政协副主席","current_org":"中国人民政治协商会议南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":28,"name":"朱红英","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区政协副主席","current_org":"中国人民政治协商会议南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":29,"name":"张平凤","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区政协副主席","current_org":"中国人民政治协商会议南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},
    {"id":30,"name":"杜玉琴","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区政协副主席","current_org":"中国人民政治协商会议南昌市新建区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldzc/leader.shtml"},

    # ── Predecessors ──
    {"id":31,"name":"陈奕蒙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"红谷滩区委书记（原新建区委书记）","current_org":"中共南昌市红谷滩区委员会","source":"https://xjq.nc.gov.cn/xjqrmzf/ldhd/202607/67ed144444c742eb93c48fd0615f7360.shtml"},
    {"id":32,"name":"王成久","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"（原新建区委副书记、区长，去向待查）","current_org":"","source":"https://news.sina.com.cn/c/2021-07-24/doc-ikqcfnca6365908.shtml"},
    {"id":33,"name":"李松殿","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"南昌市委常委、宣传部部长（原新建区委书记）","current_org":"中共南昌市委宣传部","source":"https://baike.baidu.com/item/%E6%9D%8E%E6%9D%BE%E6%AE%BF"},
    {"id":34,"name":"饶绍清","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"（原新建区委书记，去向待查）","current_org":"","source":""},

    # ── Cross-district connections ──
    {"id":35,"name":"熊飞","gender":"男","ethnicity":"汉族","birth":"1975-09","birthplace":"江西新建","education":"南昌大学MBA/在职研究生","party_join":"","work_start":"","current_post":"红谷滩区副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn"},
    {"id":36,"name":"毛演斌","gender":"男","ethnicity":"汉族","birth":"1974-07","birthplace":"江西南昌","education":"在职大学","party_join":"中共党员","work_start":"1996-08","current_post":"青山湖区副区长（原新建区住建局长）","current_org":"南昌市青山湖区人民政府","source":"https://baike.baidu.com"},
    {"id":37,"name":"陈建军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"西湖区委书记（原新建区委副书记）","current_org":"中共南昌市西湖区委员会","source":"https://xhq.nc.gov.cn"},
    {"id":38,"name":"余耀武","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"西湖区委副书记、代区长（原新建副区长）","current_org":"南昌市西湖区人民政府","source":"https://xhq.nc.gov.cn"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共南昌市新建区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市新建区"},
    {"id":2,"name":"南昌市新建区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市新建区"},
    {"id":3,"name":"中共南昌市新建区纪律检查委员会","type":"党委","level":"区级","parent":"南昌市纪律检查委员会","location":"江西省南昌市新建区"},
    {"id":4,"name":"南昌市公安局新建分局","type":"政府","level":"区级","parent":"南昌市公安局","location":"江西省南昌市新建区"},
    {"id":5,"name":"南昌市新建区人民代表大会常务委员会","type":"人大","level":"区级","parent":"南昌市人大常委会","location":"江西省南昌市新建区"},
    {"id":6,"name":"中国人民政治协商会议南昌市新建区委员会","type":"政协","level":"区级","parent":"南昌市政协","location":"江西省南昌市新建区"},
    {"id":7,"name":"中共南昌市红谷滩区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市红谷滩区"},
    {"id":8,"name":"南昌市红谷滩区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市红谷滩区"},
    {"id":9,"name":"中共进贤县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市进贤县"},
    {"id":10,"name":"进贤县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市进贤县"},
    {"id":11,"name":"南昌市青山湖区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市青山湖区"},
    {"id":12,"name":"中共南昌市委宣传部","type":"党委","level":"市级","parent":"中共南昌市委员会","location":"江西省南昌市"},
    {"id":13,"name":"中共南昌市青山湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市青山湖区"},
    {"id":14,"name":"中共南昌市委员会","type":"党委","level":"市级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":15,"name":"南昌市人民政府","type":"政府","level":"市级","parent":"","location":"江西省南昌市"},
    {"id":16,"name":"中共南昌市西湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市西湖区"},
    {"id":17,"name":"南昌市西湖区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市西湖区"},
]

# ── POSITIONS ──
positions = [
    # 徐强(1) — 区委书记
    {"id":1,"person_id":1,"org_id":9,"title":"进贤县委书记","start":"2021-08","end":"2026-06","rank":"正处级","note":"2021年8月任进贤县委书记"},
    {"id":2,"person_id":1,"org_id":1,"title":"新建区委书记","start":"2026-07","end":"","rank":"正处级","note":"2026年7月南昌六县区联动调整上任"},
    # 徐强更早的职业生涯未查到——进贤县委书记之前曾在南昌市县区多岗位任职

    # 兰杨丽(2) — 区长
    {"id":3,"person_id":2,"org_id":2,"title":"新建区委副书记、区长","start":"","end":"","rank":"正处级","note":"现任新建区区长"},

    # 彭达兵(3) — 区委常委、副区长
    {"id":4,"person_id":3,"org_id":2,"title":"新建区委常委、常务副区长","start":"","end":"","rank":"副处级","note":""},

    # 冯健(4) — 区委常委
    {"id":5,"person_id":4,"org_id":1,"title":"新建区委常委","start":"","end":"","rank":"副处级","note":""},

    # 贾中强(5) — 区委常委、常务副区长
    {"id":6,"person_id":5,"org_id":1,"title":"新建区委常委","start":"","end":"","rank":"副处级","note":""},
    {"id":7,"person_id":5,"org_id":2,"title":"新建区副区长","start":"","end":"","rank":"副处级","note":""},

    # 黄永强(6) — 政法委书记
    {"id":8,"person_id":6,"org_id":1,"title":"新建区委常委、政法委书记","start":"","end":"","rank":"副处级","note":""},

    # 吴梅萍(7) — 宣传部部长
    {"id":9,"person_id":7,"org_id":1,"title":"新建区委常委、宣传部部长","start":"","end":"","rank":"副处级","note":""},

    # 戴军(8) — 纪委书记
    {"id":10,"person_id":8,"org_id":3,"title":"新建区委常委、纪委书记、监委主任","start":"","end":"","rank":"副处级","note":""},

    # 夏辉(9) — 组织部部长
    {"id":11,"person_id":9,"org_id":1,"title":"新建区委常委、组织部部长","start":"","end":"","rank":"副处级","note":""},

    # 杨文军(10) — 区委常委
    {"id":12,"person_id":10,"org_id":1,"title":"新建区委常委","start":"","end":"","rank":"副处级","note":""},

    # 李葵(11) — 统战部部长
    {"id":13,"person_id":11,"org_id":1,"title":"新建区委常委、统战部部长","start":"","end":"","rank":"副处级","note":""},

    # 胡燕琴(12) — 副区长
    {"id":14,"person_id":12,"org_id":2,"title":"新建区副区长","start":"","end":"","rank":"副处级","note":""},

    # 钱治华(13) — 副区长
    {"id":15,"person_id":13,"org_id":2,"title":"新建区副区长","start":"","end":"","rank":"副处级","note":""},

    # 李和风(14) — 副区长
    {"id":16,"person_id":14,"org_id":2,"title":"新建区副区长","start":"","end":"","rank":"副处级","note":""},

    # 王锋海(15) — 副区长、公安分局长
    {"id":17,"person_id":15,"org_id":2,"title":"新建区副区长、公安分局局长","start":"","end":"","rank":"副处级","note":""},
    {"id":18,"person_id":15,"org_id":4,"title":"新建公安分局局长","start":"","end":"","rank":"正科级","note":""},

    # 万里晴(16) — 副区长
    {"id":19,"person_id":16,"org_id":2,"title":"新建区副区长","start":"","end":"","rank":"副处级","note":""},

    # 区人大
    {"id":20,"person_id":17,"org_id":5,"title":"新建区人大常委会主任","start":"","end":"","rank":"正处级","note":""},
    {"id":21,"person_id":18,"org_id":5,"title":"新建区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":22,"person_id":19,"org_id":5,"title":"新建区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":23,"person_id":20,"org_id":5,"title":"新建区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":24,"person_id":21,"org_id":5,"title":"新建区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":25,"person_id":22,"org_id":5,"title":"新建区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":26,"person_id":23,"org_id":5,"title":"新建区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},

    # 区政协
    {"id":27,"person_id":24,"org_id":6,"title":"新建区政协主席","start":"","end":"","rank":"正处级","note":""},
    {"id":28,"person_id":25,"org_id":6,"title":"新建区政协副主席","start":"","end":"","rank":"副处级","note":""},
    {"id":29,"person_id":26,"org_id":6,"title":"新建区政协副主席","start":"","end":"","rank":"副处级","note":""},
    {"id":30,"person_id":27,"org_id":6,"title":"新建区政协副主席","start":"","end":"","rank":"副处级","note":""},
    {"id":31,"person_id":28,"org_id":6,"title":"新建区政协副主席","start":"","end":"","rank":"副处级","note":""},
    {"id":32,"person_id":29,"org_id":6,"title":"新建区政协副主席","start":"","end":"","rank":"副处级","note":""},
    {"id":33,"person_id":30,"org_id":6,"title":"新建区政协副主席","start":"","end":"","rank":"副处级","note":""},

    # 陈奕蒙(31) — 前任书记
    {"id":34,"person_id":31,"org_id":1,"title":"新建区委书记","start":"~2021","end":"2026-06","rank":"正处级","note":"2021年前后到任新建区委书记"},
    {"id":35,"person_id":31,"org_id":7,"title":"红谷滩区委书记","start":"2026-07","end":"","rank":"正处级","note":"2026年7月南昌六县区联动调整上任"},

    # 王成久(32) — 前任区长
    {"id":36,"person_id":32,"org_id":2,"title":"新建区委副书记、区长","start":"~2021","end":"~2026-06","rank":"正处级","note":"与陈奕蒙搭档的新建区长"},

    # 李松殿(33) — 前任书记
    {"id":37,"person_id":33,"org_id":1,"title":"新建区委书记","start":"~2020","end":"~2021","rank":"副厅级","note":"兼任南昌市委常委、宣传部部长"},
    {"id":38,"person_id":33,"org_id":12,"title":"南昌市委常委、宣传部部长","start":"","end":"","rank":"副厅级","note":"现任"},

    # 饶绍清(34) — 前任书记
    {"id":39,"person_id":34,"org_id":1,"title":"新建区委书记","start":"~2019","end":"~2020","rank":"正处级","note":"李松殿的前任"},

    # 熊飞(35) — 新建籍跨区干部
    {"id":40,"person_id":35,"org_id":8,"title":"红谷滩区副区长","start":"~2021","end":"","rank":"副处级","note":"江西新建人"},
    {"id":41,"person_id":35,"org_id":1,"title":"红谷滩城投集团→红谷滩政府","start":"~2018","end":"~2021","rank":"区属国企→副处级","note":"从城投集团转政府任职"},

    # 毛演斌(36) — 新建→青山湖
    {"id":42,"person_id":36,"org_id":2,"title":"新建区住建局党组书记、局长","start":"~2019","end":"2021-08","rank":"正科级","note":"新建区任职期间"},
    {"id":43,"person_id":36,"org_id":13,"title":"青山湖区副区长","start":"~2021-08","end":"","rank":"副处级","note":"新建→青山湖跨区晋升"},

    # 陈建军(37) — 新建→西湖
    {"id":44,"person_id":37,"org_id":1,"title":"新建区委副书记","start":"~2019","end":"~2019","rank":"副处级","note":"短暂担任新建区委副书记"},
    {"id":45,"person_id":37,"org_id":16,"title":"西湖区委书记","start":"~2025-12","end":"","rank":"正处级","note":"新建→市商务局→西湖"},

    # 余耀武(38) — 新建→西湖
    {"id":46,"person_id":38,"org_id":2,"title":"新建区委常委、副区长","start":"~2021","end":"2025-09","rank":"副处级","note":"新建区溪霞镇党委书记出身"},
    {"id":47,"person_id":38,"org_id":17,"title":"西湖区委副书记、代区长","start":"~2026-07","end":"","rank":"正处级","note":"余耀武从新建副区长→市机关事务管理局→西湖代区长"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"徐强（区委书记）与兰杨丽（区长）为新建区党政一把手","overlap_org":"新建区","overlap_period":"2026-07至今"},
    {"id":2,"person_a":31,"person_b":32,"type":"党政搭档","context":"陈奕蒙（原区委书记）与王成久（原区长）为新建区前任党政搭档","overlap_org":"新建区","overlap_period":"~2021-2026"},

    # 职务接替——书记
    {"id":3,"person_a":34,"person_b":33,"type":"职务接替","context":"饶绍清→李松殿任新建区委书记","overlap_org":"新建区委","overlap_period":"不重叠（前后任）"},
    {"id":4,"person_a":33,"person_b":31,"type":"职务接替","context":"李松殿→陈奕蒙任新建区委书记","overlap_org":"新建区委","overlap_period":"不重叠（前后任）"},
    {"id":5,"person_a":31,"person_b":1,"type":"职务接替","context":"陈奕蒙→徐强任新建区委书记（2026六县区联动调整）","overlap_org":"新建区委","overlap_period":"不重叠（前后任）"},

    # 职务接替——区长
    {"id":6,"person_a":32,"person_b":2,"type":"职务接替","context":"王成久→兰杨丽任新建区长","overlap_org":"新建区政府","overlap_period":"不重叠（前后任）"},

    # 现任班子关系
    {"id":7,"person_a":1,"person_b":3,"type":"党政搭档","context":"徐强（书记）与彭达兵（常务副区长）为现任班子搭档","overlap_org":"新建区","overlap_period":"2026-07至今"},
    {"id":8,"person_a":1,"person_b":4,"type":"现任班子","context":"徐强与冯健为现任区委班子","overlap_org":"新建区委","overlap_period":"2026-07至今"},
    {"id":9,"person_a":1,"person_b":5,"type":"现任班子","context":"徐强与贾中强为现任班子搭档","overlap_org":"新建区委","overlap_period":"2026-07至今"},
    {"id":10,"person_a":1,"person_b":6,"type":"现任班子","context":"徐强与黄永强为现任班子搭档","overlap_org":"新建区委","overlap_period":"2026-07至今"},
    {"id":11,"person_a":1,"person_b":7,"type":"现任班子","context":"徐强与吴梅萍为现任班子搭档","overlap_org":"新建区委","overlap_period":"2026-07至今"},
    {"id":12,"person_a":1,"person_b":8,"type":"现任班子","context":"徐强与戴军为现任班子搭档","overlap_org":"新建区委","overlap_period":"2026-07至今"},
    {"id":13,"person_a":1,"person_b":9,"type":"现任班子","context":"徐强与夏辉为现任班子搭档","overlap_org":"新建区委","overlap_period":"2026-07至今"},
    {"id":14,"person_a":1,"person_b":11,"type":"现任班子","context":"徐强与李葵为现任班子搭档","overlap_org":"新建区委","overlap_period":"2026-07至今"},

    # 区政府班子关系
    {"id":15,"person_a":2,"person_b":3,"type":"政府搭档","context":"兰杨丽（区长）与彭达兵（常务副区长）为区政府正副手","overlap_org":"新建区政府","overlap_period":"至今"},
    {"id":16,"person_a":2,"person_b":5,"type":"政府搭档","context":"兰杨丽（区长）与贾中强（副区长）为区政府班子","overlap_org":"新建区政府","overlap_period":"至今"},
    {"id":17,"person_a":2,"person_b":12,"type":"政府搭档","context":"兰杨丽与胡燕琴为区政府班子","overlap_org":"新建区政府","overlap_period":"至今"},
    {"id":18,"person_a":2,"person_b":13,"type":"政府搭档","context":"兰杨丽与钱治华为区政府班子","overlap_org":"新建区政府","overlap_period":"至今"},
    {"id":19,"person_a":2,"person_b":14,"type":"政府搭档","context":"兰杨丽与李和风为区政府班子","overlap_org":"新建区政府","overlap_period":"至今"},

    # 跨区联系——徐强（进贤→新建）
    {"id":20,"person_a":1,"person_b":31,"type":"2026联动调整","context":"徐强（进贤→新建区委书记）接替陈奕蒙（新建→红谷滩区委书记）——2026六县区联动调整","overlap_org":"新建区","overlap_period":"2026-07"},

    # 跨区联系——新建籍干部
    {"id":21,"person_a":35,"person_b":2,"type":"新建籍干部","context":"熊飞（江西新建人，红谷滩副区长）与现任新建区长兰杨丽为同籍贯","overlap_org":"新建区","overlap_period":"同籍贯"},
    {"id":22,"person_a":36,"person_b":2,"type":"新建→青山湖","context":"毛演斌（原新建区住建局长→青山湖区副区长）曾在新建区政府工作","overlap_org":"新建区住建局","overlap_period":"~2019-2021"},

    # 前任书记——李松殿（市委常委兼）
    {"id":23,"person_a":33,"person_b":31,"type":"前后任","context":"李松殿（市委常委/宣传部长/新建书记）→陈奕蒙接任新建书记","overlap_org":"新建区委","overlap_period":"不重叠（前后任）"},

    # 徐强进贤经历
    {"id":24,"person_a":1,"person_b":32,"type":"前任区县搭档","context":"徐强（前进贤县委书记）在王成久任新建区长期间为进贤→新建关系","overlap_org":"新建区","overlap_period":"~2021-2026"},
    
    # 新建→西湖跨区
    {"id":25,"person_a":37,"person_b":1,"type":"跨区","context":"陈建军（原新建区委副书记→西湖区委书记）曾在新建区委工作","overlap_org":"新建区委","overlap_period":"~2019"},
    {"id":26,"person_a":38,"person_b":2,"type":"跨区","context":"余耀武（原新建副区长→西湖代区长）曾在新建区政府工作","overlap_org":"新建区政府","overlap_period":"~2021-2025-09"},
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
    if "区委书记" in post and "副书记" not in post:
        return "255,50,50"
    elif "区长" in post or "副区长" in post or "代区长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "政法委" in post:
        return "150,100,200"
    elif "宣传部" in post:
        return "100,200,150"
    elif "组织部" in post:
        return "200,150,100"
    elif "统战部" in post:
        return "200,100,150"
    elif "人大" in post:
        return "100,200,200"
    elif "政协" in post:
        return "200,200,100"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","纪委":"255,200,200"}.get(otype,"200,200,200")

def get_node_size(p):
    post = p.get("current_post","")
    if "区委书记" in post and "副书记" not in post:
        return "20.0"
    elif "区长" in post and "副书记" in post:
        return "20.0"
    elif "人大常委会主任" in post or "政协主席" in post:
        return "16.0"
    elif "副区长" in post or "常委" in post or "副主任" in post or "副主席" in post:
        return "12.0"
    return "12.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>南昌市新建区领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    sz = get_node_size(p)
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
