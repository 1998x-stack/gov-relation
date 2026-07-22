#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 华亭市 (Huating City, Gansu) leadership network.

华亭市 is a county-level city under 平凉市, Gansu Province.
Covers: Party Secretary (市委书记), Mayor (市长), their predecessors/successors,
Standing Committee members, key deputy leaders, and cross-city exchange patterns.

Research date: 2026-07-22
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_华亭市")
DB_PATH = os.path.join(STAGING, "华亭市_network.db")
GEXF_PATH = os.path.join(STAGING, "华亭市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership (as of mid-2026) ──
    # 刘小平 — 华亭市委书记 (from 崇信县长, ~2026)
    {"id":1,"name":"刘小平","gender":"男","ethnicity":"汉族","birth":"1975-12","birthplace":"甘肃","education":"大学","party_join":"中共党员","work_start":"","current_post":"华亭市委书记","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn/zfxxgk/fdzdgknr/jgjj/ldzc/SWLD/art/2026/art_dde499837fa3404fb9a9341fdb5e1e0b.html"},
    # 何东京 — 华亭市委副书记、市长
    {"id":2,"name":"何东京","gender":"男","ethnicity":"汉族","birth":"1985-05","birthplace":"甘肃","education":"大学","party_join":"中共党员","work_start":"","current_post":"华亭市委副书记、市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn/zfxxgk/fdzdgknr/jgjj/ldzc/ZFLD/art/2022/art_e88bc13251f94a6e8ce9d98ce1e2bcb0.html"},

    # ── Predecessors: 市委书记 ──
    # 景晓东 — 原华亭市委书记, 现任平凉市副市长 (as of 2026)
    {"id":3,"name":"景晓东","gender":"男","ethnicity":"汉族","birth":"1974-03","birthplace":"甘肃灵台","education":"甘肃省委党校研究生学历","party_join":"1994-06","work_start":"1992-07","current_post":"平凉市副市长（原华亭市委书记）","current_org":"平凉市人民政府","source":"https://m.baike.com/wikiid/1260314645162393678"},
    # 孟小金 — 原华亭县委书记、市委书记（2011-2019）
    {"id":4,"name":"孟小金","gender":"男","ethnicity":"汉族","birth":"1962-01","birthplace":"甘肃灵台","education":"甘肃省委党校函授工商管理专业研究生","party_join":"1985-05","work_start":"1981-07","current_post":"已退休","current_org":"","source":"https://hotelaah.com/liren/gansu_pingliang_huating.html"},

    # ── Predecessors: 市长/县长 ──
    # 张晓刚 — 原华亭市长, 拟提名为政协副主席
    {"id":5,"name":"张晓刚","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"甘肃","education":"大学学历农学学士","party_join":"中共党员","work_start":"","current_post":"原华亭市委副书记、市长","current_org":"","source":"http://renshi.people.com.cn/n1/2026/0104/c139617-40638178.html"},
    # 王宏林 — 原华亭县长/市长（2011-2018）
    {"id":6,"name":"王宏林","gender":"男","ethnicity":"汉族","birth":"1966-08","birthplace":"甘肃崇信","education":"研究生","party_join":"1991-03","work_start":"1985-07","current_post":"原华亭市人民政府市长","current_org":"","source":"https://hotelaah.com/liren/gansu_pingliang_huating.html"},

    # ── Standing Committee Members (as of 2026) ──
    {"id":7,"name":"李锋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委副书记","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":8,"name":"李旭栋","gender":"男","ethnicity":"汉族","birth":"1981-12","birthplace":"","education":"大学","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、组织部部长","current_org":"中共华亭市委组织部","source":"http://www.gsht.gov.cn/zfxxgk/fdzdgknr/jgjj/ldzc/SWLD/art/2025/art_fdd056b35bde45b49622b36539ffa093.html"},
    {"id":9,"name":"海英","gender":"女","ethnicity":"回族","birth":"1978-08","birthplace":"","education":"在职研究生","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、宣传部部长","current_org":"中共华亭市委宣传部","source":"http://www.gsht.gov.cn/zfxxgk/fdzdgknr/jgjj/ldzc/SWLD/art/2022/art_f71524e7b6bc4f4aad2e0db5a42c8486.html"},
    {"id":10,"name":"刘贵明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、政法委书记","current_org":"中共华亭市委政法委","source":"http://www.gsht.gov.cn"},
    {"id":11,"name":"王宁宁","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、市纪委书记、市监委主任","current_org":"中共华亭市纪律检查委员会","source":"http://www.gsht.gov.cn"},
    {"id":12,"name":"郭建辉","gender":"男","ethnicity":"汉族","birth":"1972-02","birthplace":"","education":"在职大学","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、市政府常务副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn/zfxxgk/fdzdgknr/jgjj/ldzc/ZFLD/art/2022/art_b83d180854814a92a2db212ac4a67a10.html"},
    {"id":13,"name":"郭辉","gender":"男","ethnicity":"汉族","birth":"1983-11","birthplace":"","education":"大学","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、市政府副市长（常务）、党组副书记","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn/zfxxgk/fdzdgknr/jgjj/ldzc/ZFLD/art/2026/art_97338052fdad4370b4408d4086d20596.html"},
    {"id":14,"name":"石佩奇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
    {"id":15,"name":"张锐龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":16,"name":"李小云","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":17,"name":"王珺","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":18,"name":"宋红妍","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":19,"name":"李中尧","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},

    # ── Deputy Mayors / Government Leaders ──
    {"id":20,"name":"田福","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市副市长、市公安局局长","current_org":"华亭市公安局","source":"http://www.gsht.gov.cn"},
    {"id":21,"name":"党雪菁","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
    {"id":22,"name":"孙浩伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
    {"id":23,"name":"李晓峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
    {"id":24,"name":"杨明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
    {"id":25,"name":"段锦博","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},

    # ── Previous Standing Committee (in transition) ──
    {"id":26,"name":"张骞","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委副书记（原）","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":27,"name":"赵小灵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、组织部部长（原）","current_org":"中共华亭市委组织部","source":"http://www.gsht.gov.cn"},
    {"id":28,"name":"鱼洁波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市领导","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":29,"name":"陈海贵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":30,"name":"王宁宁","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委（原纪委书记）","current_org":"中共华亭市委员会","source":"http://www.gsht.gov.cn"},
    {"id":31,"name":"杨本县","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、常务副市长（原）","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
    {"id":32,"name":"肖蔚","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委常委、市政府副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
    {"id":33,"name":"李文环","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市副市长","current_org":"华亭市人民政府","source":"http://www.gsht.gov.cn"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共华亭市委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市华亭市"},
    {"id":2,"name":"华亭市人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市华亭市"},
    {"id":3,"name":"中共华亭市纪律检查委员会","type":"党委","level":"县级","parent":"中共华亭市委员会","location":"甘肃省平凉市华亭市"},
    {"id":4,"name":"华亭市人大常委会","type":"人大","level":"县级","parent":"平凉市人大常委会","location":"甘肃省平凉市华亭市"},
    {"id":5,"name":"政协华亭市委员会","type":"政协","level":"县级","parent":"政协平凉市委员会","location":"甘肃省平凉市华亭市"},
    {"id":6,"name":"中共华亭市委组织部","type":"党委","level":"县级","parent":"中共华亭市委员会","location":"甘肃省平凉市华亭市"},
    {"id":7,"name":"中共华亭市委宣传部","type":"党委","level":"县级","parent":"中共华亭市委员会","location":"甘肃省平凉市华亭市"},
    {"id":8,"name":"中共华亭市委政法委","type":"党委","level":"县级","parent":"中共华亭市委员会","location":"甘肃省平凉市华亭市"},
    {"id":9,"name":"华亭市公安局","type":"政府","level":"县级","parent":"华亭市人民政府","location":"甘肃省平凉市华亭市"},
    {"id":10,"name":"中共崇信县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市崇信县"},
    {"id":11,"name":"崇信县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市崇信县"},
    {"id":12,"name":"平凉市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省平凉市"},
    {"id":13,"name":"华亭工业园区党委","type":"党委","level":"县级","parent":"中共华亭市委员会","location":"甘肃省平凉市华亭市"},
    {"id":14,"name":"平凉市工业和信息化局","type":"政府","level":"地级","parent":"平凉市人民政府","location":"甘肃省平凉市"},
    {"id":15,"name":"华亭县人民代表大会常务委员会","type":"人大","level":"县级","parent":"平凉市人大常委会","location":"甘肃省平凉市华亭县"},
    {"id":16,"name":"灵台县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市灵台县"},
    {"id":17,"name":"平凉市崆峒区人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市崆峒区"},
    {"id":18,"name":"中共同心县委员会","type":"党委","level":"县级","parent":"中共吴忠市委员会","location":"宁夏吴忠市同心县"},
    {"id":19,"name":"中共平凉市委统战部","type":"党委","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 刘小平 (id=1) 华亭市委书记 ──
    {"pid":1,"org":1,"title":"华亭市委书记","start":"2026","end":"至今","rank":"正处级","note":"主持市委全面工作"},
    {"pid":1,"org":10,"title":"崇信县委副书记、县长","start":"2023-11","end":"2026","rank":"正处级","note":"2023年11月任崇信代县长"},
    {"pid":1,"org":14,"title":"平凉市工业和信息化局党组书记、局长","start":"","end":"2023-11","rank":"正处级","note":""},
    {"pid":1,"org":2,"title":"华亭市委常委、市政府党组副书记、常务副市长","start":"","end":"","rank":"副处级","note":"三级调研员"},
    {"pid":1,"org":8,"title":"华亭市委常委、政法委书记","start":"","end":"","rank":"副处级","note":""},
    {"pid":1,"org":13,"title":"华亭工业园区党委书记","start":"","end":"","rank":"副处级","note":""},

    # ── 何东京 (id=2) 华亭市长 ──
    {"pid":2,"org":2,"title":"华亭市委副书记、市长、市政府党组书记","start":"2026","end":"至今","rank":"正处级","note":"主持市政府全面工作"},
    {"pid":2,"org":1,"title":"华亭市委副书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 景晓东 (id=3) 前市委书记 ──
    {"pid":3,"org":12,"title":"平凉市副市长","start":"2026","end":"至今","rank":"副厅级","note":"2026年任前公示拟提名为市州政府副市州长人选；分管工信、自然资源、住建"},
    {"pid":3,"org":1,"title":"华亭市委书记、市人武部党委第一书记","start":"2020","end":"2026","rank":"正处级","note":"约2020年从市长升任书记"},
    {"pid":3,"org":2,"title":"华亭市委副书记、市长","start":"2020-04","end":"2020","rank":"正处级","note":"2020年4月任前公示拟提名为县长候选人"},
    {"pid":3,"org":2,"title":"华亭市委常委、市政府党组副书记、常务副市长","start":"2015-07","end":"2020-04","rank":"副处级","note":"2015年7月调任华亭县委常委、常务副县长；2018年12月撤县设市后改任市委常委、常务副市长"},
    {"pid":3,"org":18,"title":"中共同心县委常委、纪委书记","start":"2011-09","end":"2015-07","rank":"副处级","note":"宁夏同心县挂职或任职"},
    {"pid":3,"org":10,"title":"中共崇信县委常委、纪委书记","start":"2010-04","end":"2011-09","rank":"副处级","note":""},
    {"pid":3,"org":16,"title":"灵台县工作","start":"1992-07","end":"2010-04","rank":"","note":"1992.07-1998.09先后在灵台县星火中学任教、共青团县委、县委组织部工作；1998-2010在灵台县历任多职"},
    {"pid":3,"org":16,"title":"平凉师范学生","start":"1989-09","end":"1992-07","rank":"","note":""},

    # ── 孟小金 (id=4) 前县委书记 ──
    {"pid":4,"org":1,"title":"华亭县委书记（撤县设市后市委书记）","start":"2011-09","end":"2019","rank":"正处级","note":"2016年11月起兼任平凉市副市长"},
    {"pid":4,"org":12,"title":"平凉市人民政府副市长（兼）","start":"2016-11","end":"2019","rank":"副厅级","note":"兼任华亭县委书记"},
    {"pid":4,"org":17,"title":"平凉市崆峒区委副书记、区长","start":"","end":"2011-09","rank":"正处级","note":""},

    # ── 张晓刚 (id=5) 前市长 ──
    {"pid":5,"org":2,"title":"华亭市委副书记、市长、二级巡视员","start":"","end":"2026-01","rank":"正处级","note":"2026年1月拟提名为市州政协副主席候选人"},
    {"pid":5,"org":1,"title":"华亭市委副书记","start":"","end":"2026","rank":"副处级","note":""},

    # ── 王宏林 (id=6) 前县长/市长 ──
    {"pid":6,"org":2,"title":"华亭市人民政府市长","start":"2011-10","end":"2018-12","rank":"正处级","note":"2011.10任县长，2018.12撤县设市后任市长"},
    {"pid":6,"org":2,"title":"华亭县委副书记、代县长","start":"2011-09","end":"2011-10","rank":"正处级","note":""},
    {"pid":6,"org":12,"title":"平凉市政府副秘书长、市外事侨务办公室主任","start":"","end":"2011-09","rank":"正处级","note":""},

    # ── 李锋 (id=7) 市委副书记 ──
    {"pid":7,"org":1,"title":"华亭市委副书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李旭栋 (id=8) 组织部长 ──
    {"pid":8,"org":6,"title":"华亭市委常委、组织部部长","start":"","end":"至今","rank":"副处级","note":"负责市委组织工作"},

    # ── 海英 (id=9) 宣传部长 ──
    {"pid":9,"org":7,"title":"华亭市委常委、宣传部部长、市新时代文明实践中心办公室主任（兼）","start":"","end":"至今","rank":"副处级","note":"负责市委宣传思想和意识形态工作"},

    # ── 刘贵明 (id=10) 政法委书记 ──
    {"pid":10,"org":8,"title":"华亭市委常委、政法委书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 王宁宁 (id=11) 纪委书记 ──
    {"pid":11,"org":3,"title":"华亭市委常委、市纪委书记、市监委主任","start":"","end":"至今","rank":"副处级","note":""},

    # ── 郭建辉 (id=12) 常务副市长 ──
    {"pid":12,"org":2,"title":"华亭市委常委、市政府常务副市长、党组副书记","start":"","end":"至今","rank":"副处级","note":"负责市政府日常工作"},

    # ── 郭辉 (id=13) 常务副市长(新) ──
    {"pid":13,"org":2,"title":"华亭市委常委、市政府副市长（常务）、党组副书记","start":"","end":"至今","rank":"副处级","note":"负责市政府日常工作、发展改革、项目建设、工信、财税金融等"},

    # ── 石佩奇 (id=14) 副市长 ──
    {"pid":14,"org":2,"title":"华亭市委常委、副市长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张锐龙 (id=15) 市委常委 ──
    {"pid":15,"org":1,"title":"华亭市委常委","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李小云 (id=16) 市委常委 ──
    {"pid":16,"org":1,"title":"华亭市委常委","start":"","end":"至今","rank":"副处级","note":""},

    # ── 王珺 (id=17) 市委常委 ──
    {"pid":17,"org":1,"title":"华亭市委常委","start":"","end":"至今","rank":"副处级","note":""},

    # ── 宋红妍 (id=18) 市委常委 ──
    {"pid":18,"org":1,"title":"华亭市委常委","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李中尧 (id=19) 市委常委 ──
    {"pid":19,"org":1,"title":"华亭市委常委","start":"","end":"至今","rank":"副处级","note":""},

    # ── 田福 (id=20) 副市长兼公安局长 ──
    {"pid":20,"org":9,"title":"华亭市副市长、市公安局局长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 党雪菁 (id=21) 副市长 ──
    {"pid":21,"org":2,"title":"华亭市副市长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 孙浩伟 (id=22) 副市长 ──
    {"pid":22,"org":2,"title":"华亭市副市长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李晓峰 (id=23) 副市长 ──
    {"pid":23,"org":2,"title":"华亭市副市长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 杨明 (id=24) 副市长 ──
    {"pid":24,"org":2,"title":"华亭市副市长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 段锦博 (id=25) 副市长 ──
    {"pid":25,"org":2,"title":"华亭市副市长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张骞 (id=26) 原市委副书记 ──
    {"pid":26,"org":1,"title":"华亭市委副书记","start":"","end":"","rank":"副处级","note":""},

    # ── 赵小灵 (id=27) 原组织部长 ──
    {"pid":27,"org":6,"title":"华亭市委常委、组织部部长","start":"","end":"","rank":"副处级","note":""},

    # ── 鱼洁波 (id=28) ──
    {"pid":28,"org":1,"title":"华亭市领导","start":"","end":"","rank":"","note":""},

    # ── 陈海贵 (id=29) ──
    {"pid":29,"org":1,"title":"华亭市委常委","start":"","end":"","rank":"副处级","note":""},

    # ── 杨本县 (id=31) 原常务副市长 ──
    {"pid":31,"org":2,"title":"华亭市委常委、常务副市长","start":"","end":"","rank":"副处级","note":""},

    # ── 肖蔚 (id=32) ⚠️ special char in name, using id ──
    {"pid":32,"org":2,"title":"华亭市委常委、市政府副市长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李文环 (id=33) 原副市长 ──
    {"pid":33,"org":2,"title":"华亭市副市长","start":"","end":"","rank":"副处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 刘小平 ↔ 何东京 (current party-government duo)
    {"a":1,"b":2,"type":"overlap","context":"刘小平任市委书记，何东京任市长，党政搭档","overlap_org":"中共华亭市委员会、华亭市人民政府","overlap_period":"2026~至今","strength":"strong","confidence":"confirmed"},

    # 刘小平 ↔ 景晓东 (predecessor-successor, party secretary)
    {"a":1,"b":3,"type":"predecessor_successor","context":"刘小平接替景晓东任华亭市委书记","overlap_org":"中共华亭市委员会","overlap_period":"2026","strength":"strong","confidence":"confirmed"},

    # 景晓东 ↔ 孟小金 (predecessor-successor, party secretary)
    {"a":3,"b":4,"type":"predecessor_successor","context":"景晓东接替孟小金任华亭市委书记","overlap_org":"中共华亭市委员会","overlap_period":"2020","strength":"strong","confidence":"confirmed"},

    # 何东京 ↔ 张晓刚 (predecessor-successor, mayor)
    {"a":2,"b":5,"type":"predecessor_successor","context":"何东京接替张晓刚任华亭市长","overlap_org":"华亭市人民政府","overlap_period":"2026","strength":"strong","confidence":"confirmed"},

    # 张晓刚 ↔ 王宏林 (predecessor-successor, mayor)
    {"a":5,"b":6,"type":"predecessor_successor","context":"张晓刚接替王宏林任华亭市长","overlap_org":"华亭市人民政府","overlap_period":"","strength":"strong","confidence":"confirmed"},

    # 景晓东 ↔ 张晓刚 (previous party-government duo)
    {"a":3,"b":5,"type":"overlap","context":"景晓东任市委书记期间张晓刚任市长，党政搭档","overlap_org":"中共华亭市委员会、华亭市人民政府","overlap_period":"~2020~2025","strength":"strong","confidence":"confirmed"},

    # 孟小金 ↔ 王宏林 (previous party-government duo)
    {"a":4,"b":6,"type":"overlap","context":"孟小金任县委书记期间王宏林任县长，党政搭档","overlap_org":"中共华亭县委员会、华亭县人民政府","overlap_period":"2011-2018","strength":"strong","confidence":"confirmed"},

    # 刘小平 ↔ 李锋 (市委班子)
    {"a":1,"b":7,"type":"overlap","context":"刘小平任市委书记，李锋任市委副书记，市委班子搭档","overlap_org":"中共华亭市委员会","overlap_period":"2026~至今","strength":"strong","confidence":"confirmed"},

    # 刘小平 ↔ 李旭栋 (市委班子)
    {"a":1,"b":8,"type":"superior_subordinate","context":"刘小平任市委书记，李旭栋任组织部部长","overlap_org":"中共华亭市委员会","overlap_period":"2026~至今","strength":"medium","confidence":"confirmed"},

    # 刘小平 ↔ 何东京 ↔ 郭建辉 (政府班子)
    {"a":2,"b":12,"type":"overlap","context":"何东京任市长，郭建辉任常务副市长","overlap_org":"华亭市人民政府","overlap_period":"2026~至今","strength":"strong","confidence":"confirmed"},

    # 何东京 ↔ 郭辉 (政府班子)
    {"a":2,"b":13,"type":"overlap","context":"何东京任市长，郭辉任常务副市长（新任）","overlap_org":"华亭市人民政府","overlap_period":"2026~至今","strength":"strong","confidence":"confirmed"},

    # 刘小平曾在华亭任常务副市长，与景晓东共事
    {"a":1,"b":3,"type":"overlap","context":"刘小平任华亭常务副市长期间，景晓东先后任市长、市委书记","overlap_org":"华亭市人民政府、中共华亭市委员会","overlap_period":"2015~2020","strength":"strong","confidence":"confirmed"},

    # 刘小平与景晓东在崇信曾有交集（崇信县委常委+纪委书记 times）
    {"a":1,"b":3,"type":"same_system","context":"刘小平在崇信任职期间，景晓东曾任崇信县委常委、纪委书记","overlap_org":"中共崇信县委员会","overlap_period":"2010~2011","strength":"medium","confidence":"confirmed"},

    # 孟小金与景晓东同籍灵台
    {"a":4,"b":3,"type":"same_native_place","context":"孟小金与景晓东均为甘肃灵台人","overlap_org":"","overlap_period":"","strength":"weak","confidence":"confirmed"},

    # 景晓东曾在崇信任职（与刘小平可能有交集）
    {"a":3,"b":1,"type":"overlap","context":"景晓东曾任崇信县委常委、纪委书记，后刘小平从崇信县长升任华亭书记","overlap_org":"中共崇信县委员会","overlap_period":"2010~2011","strength":"medium","confidence":"plausible"},

    # 王宏林→平凉市政府背景
    {"a":6,"b":4,"type":"overlap","context":"王宏林任华亭县长期间，孟小金任县委书记","overlap_org":"华亭县","overlap_period":"2011-2018","strength":"strong","confidence":"confirmed"},

    # 张晓刚→景晓东
    {"a":5,"b":3,"type":"overlap","context":"张晓刚任市长期间，景晓东任市委书记","overlap_org":"中共华亭市委员会、华亭市人民政府","overlap_period":"~2020~2026","strength":"strong","confidence":"confirmed"},

    # 刘小平→平凉市工信局（景晓东现为平凉市副市长，可能在工作系统中有交集）
    {"a":1,"b":3,"type":"same_system","context":"刘小平曾任平凉市工信局局长，景晓东现任平凉市副市长分管工信","overlap_org":"平凉市人民政府","overlap_period":"","strength":"weak","confidence":"plausible"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["pid"], str(pos["org"]), pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["a"], r["b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")

    # Stats
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    print(f"  Persons: {conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        current = p.get("current_post", "")
        name = p["name"]
        if "书记" in current and "纪委" not in current and "人大" not in current and "政协" not in current:
            return "255,50,50"  # Red — party secretary
        if "市长" in current or "副县长" in current or "副市长" in current:
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "人大" in current:
            return "200,255,255"  # Cyan — NPC
        if "政协" in current:
            return "255,240,200"  # Cream — CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        # Top leaders
        if name in ("刘小平", "何东京", "景晓东", "张晓刚"):
            return "20.0"
        # Vice party secretaries & standing committee
        if name in ("孟小金", "王宏林", "李锋", "李旭栋", "海英", "刘贵明", "王宁宁", "郭建辉", "郭辉", "石佩奇", "张锐龙", "李小云", "王珺", "宋红妍", "李中尧"):
            return "15.0"
        return "12.0"

    def org_color(o):
        t = o.get("type", "")
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        if "群团" in t:
            return "255,220,255"
        if "开发" in t or "工业" in o.get("name", ""):
            return "200,255,200"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>华亭市领导班子工作关系网络 — 中共华亭市委、华亭市人民政府及平凉市域人事交流</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "未知")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        oid = str(o["id"]) if isinstance(o["id"], int) else o["id"]
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Position edges: person -> organization
    for pos in positions:
        eid += 1
        oid = str(pos["org"]) if isinstance(pos["org"], int) else pos["org"]
        period = f"{pos['start']} - {pos['end']}" if pos['start'] else ""
        lines.append(f'      <edge id="e{eid}" source="p{pos["pid"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges: person <-> person
    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["a"]}" target="p{r["b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}")
    print(f"  Edges: {eid}")


if __name__ == "__main__":
    build_database()
    build_gexf()
    print("\nDone. Generated artifacts:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
