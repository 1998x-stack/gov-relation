#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 平凉市 (Pingliang City, Gansu Province) leadership network.

Covers: Party Secretary (市委书记), Mayor (市长), their predecessors/successors,
Standing Committee members, key deputy leaders, and cross-city exchange patterns.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_平凉市")
DB_PATH = os.path.join(STAGING, "平凉市_network.db")
GEXF_PATH = os.path.join(STAGING, "平凉市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 唐培宏 — 平凉市委书记 (as of 2025.09)
    {"id":1,"name":"唐培宏","gender":"男","ethnicity":"汉族","birth":"1970-03","birthplace":"甘肃民勤","education":"西北师范大学历史系本科、兰州大学公共管理硕士","party_join":"1991-06","work_start":"1992-07","current_post":"平凉市委书记","current_org":"中共平凉市委员会","source":"https://baike.baidu.com/item/%E5%94%90%E5%9F%B9%E5%AE%8F/15118915"},
    # 李荣 — 平凉市代市长 (as of 2026.01)
    {"id":2,"name":"李荣","gender":"男","ethnicity":"汉族","birth":"1975-12","birthplace":"甘肃定西","education":"甘肃政法学院本科、省委党校研究生","party_join":"1996-12","work_start":"1999-09","current_post":"平凉市委副书记、代市长、市政府党组书记","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},

    # ── Predecessors — 市委书记 ──
    # 王旭 — 原平凉市委书记, 现任甘肃省副省长
    {"id":3,"name":"王旭","gender":"女","ethnicity":"汉族","birth":"1968-06","birthplace":"甘肃天水秦安","education":"兰州大学数学系计算数学及其应用软件专业本科、在职研究生管理学硕士","party_join":"1986-03","work_start":"1990-07","current_post":"甘肃省副省长（原平凉市委书记）","current_org":"甘肃省人民政府","source":"https://baike.baidu.com/item/%E7%8E%8B%E6%97%AD/2499833"},

    # ── Predecessors — 市长 ──
    # 白振海 — 原平凉市市长, 现任兰州市委常委、兰州新区党工委书记
    {"id":4,"name":"白振海","gender":"男","ethnicity":"汉族","birth":"1968-12","birthplace":"甘肃庆阳","education":"庆阳师范学校、中央党校函授学院研究生","party_join":"1991-04","work_start":"1989-07","current_post":"兰州市委常委、兰州新区党工委书记（原平凉市市长）","current_org":"中共兰州市委员会","source":"https://baike.baidu.com/item/%E7%99%BD%E6%8C%AF%E6%B5%B7"},
    # 王旭（兼市长） — 2022.06-2022.07 短暂兼任市长
    # 王旭 is already id=3 above; she was both secretary and acting mayor briefly

    # ── Key Standing Committee members ──
    {"id":5,"name":"王之臣","gender":"男","ethnicity":"汉族","birth":"1970-11","birthplace":"","education":"大学学历、法学学士","party_join":"1998-12","work_start":"1994-06","current_post":"平凉市委副书记（拟提名为市人大常委会主任候选人）","current_org":"中共平凉市委员会","source":"https://www.pingliang.gov.cn"},
    {"id":6,"name":"李明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、市纪委书记、市监委主任","current_org":"中共平凉市纪律检查委员会","source":"https://www.pingliang.gov.cn"},
    {"id":7,"name":"王锦","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、宣传部部长","current_org":"中共平凉市委员会","source":"https://www.pingliang.gov.cn"},
    {"id":8,"name":"王晓军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、政法委书记","current_org":"中共平凉市委员会","source":"https://www.pingliang.gov.cn"},
    {"id":9,"name":"辛少波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、统战部部长","current_org":"中共平凉市委员会","source":"https://www.pingliang.gov.cn"},
    {"id":10,"name":"魏至玉","gender":"男","ethnicity":"汉族","birth":"1971-11","birthplace":"","education":"省委党校研究生","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、组织部部长","current_org":"中共平凉市委员会","source":"https://www.pingliang.gov.cn"},
    {"id":11,"name":"刘国军","gender":"男","ethnicity":"汉族","birth":"1982-03","birthplace":"","education":"在职研究生学历","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、崆峒区委书记","current_org":"中共平凉市崆峒区委员会","source":"https://www.pingliang.gov.cn"},
    {"id":12,"name":"王度林","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、副市长","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn"},
    {"id":13,"name":"胡雄韬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、副市长","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn"},

    # ── Vice mayors ──
    {"id":14,"name":"丁富强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市副市长","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn"},
    {"id":15,"name":"寇正德","gender":"男","ethnicity":"汉族","birth":"1973-03","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市副市长、市公安局局长","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn"},
    {"id":16,"name":"何鹏峰","gender":"男","ethnicity":"汉族","birth":"1972-11","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市副市长","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn"},
    {"id":17,"name":"史建芳","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市副市长","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn"},

    # ── 人大、政协领导 ──
    {"id":18,"name":"马琦","gender":"男","ethnicity":"东乡族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市人大常委会主任","current_org":"平凉市人大常委会","source":"https://www.pingliang.gov.cn"},
    {"id":19,"name":"张麟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市人大常委会党组书记（原白银市委副书记）","current_org":"平凉市人大常委会","source":"https://www.pingliang.gov.cn"},

    # ── 县区主要领导 ──
    {"id":20,"name":"刘小平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市崆峒区区长","current_org":"平凉市崆峒区人民政府","source":"https://www.pingliang.gov.cn"},
    {"id":21,"name":"景晓东","gender":"男","ethnicity":"汉族","birth":"1974-03","birthplace":"甘肃灵台","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委书记","current_org":"中共华亭市委员会","source":""},
    {"id":22,"name":"王蕾","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县委书记","current_org":"中共静宁县委员会","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共平凉市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省平凉市"},
    {"id":2,"name":"平凉市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省平凉市"},
    {"id":3,"name":"平凉市人大常委会","type":"人大","level":"地级","parent":"甘肃省人大常委会","location":"甘肃省平凉市"},
    {"id":4,"name":"政协平凉市委员会","type":"政协","level":"地级","parent":"政协甘肃省委员会","location":"甘肃省平凉市"},
    {"id":5,"name":"中共平凉市纪律检查委员会","type":"党委","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":6,"name":"平凉市公安局","type":"政府","level":"地级","parent":"平凉市人民政府","location":"甘肃省平凉市"},
    {"id":7,"name":"中共平凉市委组织部","type":"党委","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":8,"name":"中共平凉市委宣传部","type":"党委","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":9,"name":"中共平凉市委统战部","type":"党委","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":10,"name":"中共平凉市委政法委","type":"党委","level":"地级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":11,"name":"中共平凉市崆峒区委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市崆峒区"},
    {"id":12,"name":"平凉市崆峒区人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市崆峒区"},
    {"id":13,"name":"中共华亭市委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市华亭市"},
    {"id":14,"name":"中共静宁县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市静宁县"},

    # 前任工作相关机构
    {"id":15,"name":"中共甘肃省委办公厅","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":16,"name":"甘肃省妇女联合会","type":"群团","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":17,"name":"中共金昌市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省金昌市"},
    {"id":18,"name":"金昌市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省金昌市"},
    {"id":19,"name":"中共兰州市委员会","type":"党委","level":"副省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":20,"name":"兰州新区党工委","type":"党委","level":"国家级新区","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":21,"name":"中共酒泉市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省酒泉市"},
    {"id":22,"name":"酒泉市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省酒泉市"},
    {"id":23,"name":"中共天水市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省天水市"},
    {"id":24,"name":"天水市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省天水市"},
    {"id":25,"name":"中共白银市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省白银市"},
    {"id":26,"name":"中共甘肃省委组织部","type":"党委","level":"省级","parent":"中共甘肃省委员会","location":"甘肃省兰州市"},
    {"id":27,"name":"甘肃省人民政府","type":"政府","level":"省级","parent":"","location":"甘肃省兰州市"},
    {"id":28,"name":"中共张掖市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省张掖市"},
    {"id":29,"name":"甘肃省公安厅","type":"政府","level":"省级","parent":"甘肃省人民政府","location":"甘肃省兰州市"},
    {"id":30,"name":"中共陇南市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省陇南市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 唐培宏 (id=1) ──
    {"pid":1,"org":1,"title":"平凉市委书记","start":"2025-09","end":"至今","rank":"正厅级","note":""},
    {"pid":1,"org":21,"title":"酒泉市委副书记、市长","start":"2021-12","end":"2025-09","rank":"正厅级","note":"酒泉市第五届人民代表大会选举产生"},
    {"pid":1,"org":21,"title":"酒泉市委副书记、代市长","start":"2021-09","end":"2021-12","rank":"正厅级","note":""},
    {"pid":1,"org":21,"title":"酒泉市委副书记","start":"2018-08","end":"2021-09","rank":"副厅级","note":""},
    {"pid":1,"org":28,"title":"张掖市委常委、组织部部长","start":"2014-07","end":"2018-08","rank":"副厅级","note":"挂职国务院办公厅秘书一局副局长"},
    {"pid":1,"org":26,"title":"甘肃省委组织部办公室主任、人才工作处处长等","start":"1997-09","end":"2014-07","rank":"正处级","note":"历任研究室、办公室、干部四处、干部一处、人才工作处等岗位"},
    {"pid":1,"org":15,"title":"兰州平板玻璃厂宣传干事、宣传部副部长","start":"1992-07","end":"1997-09","rank":"","note":"即现任兰州蓝天浮法玻璃股份有限公司"},

    # ── 李荣 (id=2) ──
    {"pid":2,"org":2,"title":"平凉市委副书记、代市长、市政府党组书记","start":"2026-01","end":"至今","rank":"正厅级","note":"2026年1月21日平凉市五届人大常委会第三十一次会议决定代理市长"},
    {"pid":2,"org":2,"title":"平凉市委常委、常务副市长","start":"2024","end":"2026-01","rank":"副厅级","note":""},
    {"pid":2,"org":30,"title":"陇南市委常委、常务副市长","start":"2024","end":"2024","rank":"副厅级","note":""},
    {"pid":2,"org":30,"title":"陇南市委常委、组织部部长","start":"2021","end":"2024","rank":"副厅级","note":""},
    {"pid":2,"org":30,"title":"陇南市副市长","start":"2021","end":"2021","rank":"副厅级","note":""},
    {"pid":2,"org":19,"title":"兰州市红古区委书记","start":"2016","end":"2021","rank":"正处级","note":""},
    {"pid":2,"org":19,"title":"兰州市红古区区长","start":"2013","end":"2016","rank":"正处级","note":""},
    {"pid":2,"org":19,"title":"兰州市红古区副区长","start":"2011","end":"2013","rank":"副处级","note":""},
    {"pid":2,"org":"19_城关区","title":"兰州市城关区盐场路街道党工委书记等","start":"2008","end":"2011","rank":"正科级","note":""},
    {"pid":2,"org":"19_城关区","title":"兰州市城关区团结新村街道办事处主任","start":"2006","end":"2008","rank":"正科级","note":""},
    {"pid":2,"org":"19_城关区","title":"共青团兰州市城关区委书记","start":"2004","end":"2006","rank":"正科级","note":""},
    {"pid":2,"org":"19_城关区","title":"兰州市城关区委组织部干部","start":"2002","end":"2004","rank":"","note":""},
    {"pid":2,"org":"19_城关区","title":"兰州市城关区青白石乡干部","start":"1999","end":"2002","rank":"","note":""},

    # ── 王旭 (id=3) ──
    {"pid":3,"org":27,"title":"甘肃省副省长","start":"2025-04","end":"至今","rank":"副部级","note":""},
    {"pid":3,"org":1,"title":"平凉市委书记（兼任市长至2022.08）","start":"2022-06","end":"2025-09","rank":"正厅级","note":""},
    {"pid":3,"org":2,"title":"平凉市委副书记、市长","start":"2021-02","end":"2022-06","rank":"正厅级","note":""},
    {"pid":3,"org":19,"title":"兰州市委副书记、市委党校校长","start":"2020-01","end":"2021-01","rank":"副厅级","note":""},
    {"pid":3,"org":19,"title":"兰州市委常委、组织部部长","start":"2018-03","end":"2020-01","rank":"副厅级","note":""},
    {"pid":3,"org":17,"title":"金昌市委常委、组织部部长、统战部部长","start":"2016-05","end":"2018-03","rank":"副厅级","note":""},
    {"pid":3,"org":18,"title":"金昌市副市长","start":"2013-06","end":"2016-05","rank":"副厅级","note":""},
    {"pid":3,"org":16,"title":"甘肃省妇女联合会副主席、党组成员","start":"2009-11","end":"2013-05","rank":"副厅级","note":""},
    {"pid":3,"org":15,"title":"甘肃省委办公厅信息化管理办公室主任等职","start":"2001-10","end":"2009-11","rank":"正处级","note":"历任副处长、主任等职"},

    # ── 白振海 (id=4) ──
    {"pid":4,"org":19,"title":"兰州市委常委、兰州新区党工委书记","start":"2026-01","end":"至今","rank":"正厅级","note":""},
    {"pid":4,"org":2,"title":"平凉市委副书记、市长","start":"2022-08","end":"2026-01","rank":"正厅级","note":""},
    {"pid":4,"org":2,"title":"平凉市委副书记、代市长","start":"2022-07","end":"2022-08","rank":"正厅级","note":""},
    {"pid":4,"org":"27_武威","title":"武威市委常委、常务副市长","start":"2021-09","end":"2022-07","rank":"副厅级","note":""},
    {"pid":4,"org":17,"title":"金昌市委常委、副市长","start":"2019-05","end":"2021-09","rank":"副厅级","note":""},
    {"pid":4,"org":17,"title":"金昌市委常委、宣传部部长","start":"2016-10","end":"2019-05","rank":"副厅级","note":""},
    {"pid":4,"org":18,"title":"庆阳市副市长","start":"2011-11","end":"2016-09","rank":"副厅级","note":""},

    # ── 王之臣 (id=5) ──
    {"pid":5,"org":1,"title":"平凉市委副书记","start":"","end":"至今","rank":"副厅级","note":"拟提名为平凉市人大常委会主任候选人（2026.01公示）"},

    # ── 李明 (id=6) ──
    {"pid":6,"org":5,"title":"平凉市委常委、市纪委书记、市监委主任","start":"","end":"至今","rank":"副厅级","note":""},

    # ── 王锦 (id=7) ──
    {"pid":7,"org":8,"title":"平凉市委常委、宣传部部长","start":"","end":"至今","rank":"副厅级","note":"兼市文联党组书记"},

    # ── 王晓军 (id=8) ──
    {"pid":8,"org":10,"title":"平凉市委常委、政法委书记","start":"","end":"至今","rank":"副厅级","note":""},

    # ── 辛少波 (id=9) ──
    {"pid":9,"org":9,"title":"平凉市委常委、统战部部长","start":"","end":"至今","rank":"副厅级","note":"兼市政协党组副书记"},

    # ── 魏至玉 (id=10) ──
    {"pid":10,"org":7,"title":"平凉市委常委、组织部部长","start":"","end":"至今","rank":"副厅级","note":""},

    # ── 刘国军 (id=11) ──
    {"pid":11,"org":11,"title":"平凉市委常委、崆峒区委书记","start":"2024-07","end":"至今","rank":"副厅级","note":""},
    {"pid":11,"org":23,"title":"天水市副市长","start":"2021-09","end":"2024-07","rank":"副厅级","note":""},
    {"pid":11,"org":15,"title":"甘肃省政府办公厅秘书一处处长、一级调研员","start":"","end":"2021-09","rank":"正处级","note":""},

    # ── 王度林 (id=12) ──
    {"pid":12,"org":2,"title":"平凉市委常委、副市长","start":"2025-12","end":"至今","rank":"副厅级","note":""},

    # ── 胡雄韬 (id=13) ──
    {"pid":13,"org":2,"title":"平凉市委常委、副市长","start":"","end":"至今","rank":"副厅级","note":""},

    # ── Vice mayors ──
    {"pid":14,"org":2,"title":"平凉市副市长","start":"","end":"至今","rank":"副厅级","note":"分管科技、民政、卫健、医保、文体广电旅游、市场监管"},
    {"pid":15,"org":6,"title":"平凉市副市长、市公安局局长","start":"","end":"至今","rank":"副厅级","note":""},
    {"pid":15,"org":29,"title":"甘肃省公安厅政治部副主任等职","start":"","end":"","rank":"","note":"此前有省厅经历"},
    {"pid":16,"org":2,"title":"平凉市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    {"pid":17,"org":2,"title":"平凉市副市长","start":"","end":"至今","rank":"副厅级","note":""},

    # ── 人大、政协 ──
    {"pid":18,"org":3,"title":"平凉市人大常委会主任","start":"","end":"至今","rank":"正厅级","note":""},
    {"pid":19,"org":3,"title":"平凉市人大常委会党组书记","start":"","end":"至今","rank":"正厅级","note":"原白银市委副书记"},
    {"pid":19,"org":25,"title":"白银市委副书记、统战部部长","start":"","end":"","rank":"副厅级","note":""},

    # ── 县区 ──
    {"pid":20,"org":12,"title":"平凉市崆峒区区长","start":"","end":"至今","rank":"正处级","note":""},
    {"pid":21,"org":13,"title":"华亭市委书记","start":"","end":"至今","rank":"正处级","note":"1974.03生，甘肃灵台人"},
    {"pid":22,"org":14,"title":"静宁县委书记","start":"2024-11","end":"至今","rank":"正处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 唐培宏 ↔ 王旭 (predecessor-successor)
    {"a":1,"b":3,"type":"predecessor_successor","context":"唐培宏于2025年9月接替王旭担任平凉市委书记","overlap_org":"中共平凉市委员会","overlap_period":"2025-09","strength":"strong","confidence":"confirmed"},
    # 李荣 ↔ 白振海 (predecessor-successor, mayor)
    {"a":2,"b":4,"type":"predecessor_successor","context":"李荣于2026年1月接替白振海担任平凉市代市长","overlap_org":"平凉市人民政府","overlap_period":"2026-01","strength":"strong","confidence":"confirmed"},
    # 白振海 ↔ 王旭 (predecessor-successor, mayor-party secretary overlap)
    {"a":4,"b":3,"type":"overlap","context":"白振海任平凉市长期间，王旭任平凉市委书记","overlap_org":"中共平凉市委员会、平凉市人民政府","overlap_period":"2022-08~2025-09","strength":"strong","confidence":"confirmed"},
    # 王旭 ↔ 白振海 (王旭作为市委书记与市长白振海搭档)
    {"a":3,"b":4,"type":"overlap","context":"王旭任市委书记期间白振海任市长，党政一把手搭档","overlap_org":"中共平凉市委员会","overlap_period":"2022-08~2025-04","strength":"strong","confidence":"confirmed"},
    # 唐培宏 ↔ 李荣 (current party secretary - acting mayor)
    {"a":1,"b":2,"type":"overlap","context":"唐培宏任市委书记，李荣任代市长，党政搭档","overlap_org":"中共平凉市委员会、平凉市人民政府","overlap_period":"2026-01~至今","strength":"strong","confidence":"confirmed"},
    # 刘国军 ↔ 唐培宏 (standing committee member)
    {"a":11,"b":1,"type":"superior_subordinate","context":"刘国军作为市委常委在唐培宏领导下工作","overlap_org":"中共平凉市委员会","overlap_period":"2024-07~至今","strength":"strong","confidence":"confirmed"},
    # 白振海 ↔ 刘国军 (previous overlap in Wuwel)
    # 王旭 ↔ 王之臣
    {"a":3,"b":5,"type":"overlap","context":"王旭任市委书记期间王之臣任市委副书记","overlap_org":"中共平凉市委员会","overlap_period":"2022-06~2025-09","strength":"strong","confidence":"confirmed"},
    # 白振海 ↔ 王之臣
    {"a":4,"b":5,"type":"overlap","context":"白振海任市长期间王之臣任市委副书记","overlap_org":"中共平凉市委员会","overlap_period":"2022-08~2026-01","strength":"strong","confidence":"confirmed"},
    # 李荣 ↔ 刘国军 (standing committee overlap)
    {"a":2,"b":11,"type":"overlap","context":"李荣与刘国军同时在平凉市委常委会工作","overlap_org":"中共平凉市委员会","overlap_period":"2024~至今","strength":"medium","confidence":"confirmed"},
    # 白振海 ↔ 魏至玉
    {"a":4,"b":10,"type":"overlap","context":"白振海任市长期间魏至玉任市委组织部部长","overlap_org":"中共平凉市委员会","overlap_period":"","strength":"medium","confidence":"plausible"},
    # 唐培宏 ↔ 魏至玉
    {"a":1,"b":10,"type":"superior_subordinate","context":"唐培宏任市委书记，魏至玉任市委组织部部长","overlap_org":"中共平凉市委员会","overlap_period":"2025-09~至今","strength":"medium","confidence":"confirmed"},
    # 张麟（白银→平凉）
    {"a":19,"b":1,"type":"overlap","context":"张麟从白银调任平凉市人大常委会党组书记，与唐培宏在平凉共事","overlap_org":"中共平凉市委员会、平凉市人大常委会","overlap_period":"","strength":"medium","confidence":"plausible"},
    # 刘国军 ← 天水市政府
    {"a":11,"b":3,"type":"same_system","context":"刘国军在天水市任副市长期间，王旭在平凉市任职；两人均在甘肃地级市政府系统履职","overlap_org":"","overlap_period":"2021-09~2022-06","strength":"weak","confidence":"plausible"},
    # 白振海曾与王旭在金昌共事
    {"a":4,"b":3,"type":"overlap","context":"白振海任金昌市委常委期间，王旭任金昌市委常委、组织部部长、副市长","overlap_org":"中共金昌市委员会","overlap_period":"2016-10~2018-03","strength":"medium","confidence":"confirmed"},
    # 李荣早年兰州城关区 -> later 陇南, same party system
    {"a":2,"b":3,"type":"same_system","context":"李荣在兰州城关区和兰州市长期任职，王旭在兰州市委任职，同在兰州工作","overlap_org":"","overlap_period":"","strength":"weak","confidence":"plausible"},
]

# Extra organizations used in positions that aren't in the main org list
# These are string references for orgs like "19_城关区" and "27_武威"
EXTRA_ORGS = {
    "19_城关区": {"name":"兰州市城关区","type":"政府","level":"县级","parent":"兰州市","location":"甘肃省兰州市城关区"},
    "27_武威": {"name":"武威市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省武威市"},
}

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

    all_orgs = list(organizations)
    for key, val in EXTRA_ORGS.items():
        all_orgs.append({"id": key, "name": val["name"], "type": val["type"], "level": val["level"], "parent": val["parent"], "location": val["location"]})

    for o in all_orgs:
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
        name = p["name"]
        current = p.get("current_post", "")
        if "书记" in current and "纪委" not in current and "人大" not in current and "政协" not in current:
            return "255,50,50"  # Red — party secretary
        if "市长" in current or "区长" in current or "副省长" in current or "副市长" in current:
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "人大" in current:
            return "200,255,255"  # Cyan — NPC
        if "政协" in current:
            return "255,240,200"  # Cream - CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        # Top leaders
        if name in ("唐培宏", "李荣", "王旭", "白振海"):
            return "20.0"
        # Standing committee
        if name in ("王之臣", "李明", "王锦", "王晓军", "辛少波", "魏至玉", "刘国军", "王度林", "胡雄韬"):
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
        if "开发" in t or "新区" in o.get("name", ""):
            return "200,255,200"
        return "200,200,200"

    all_orgs = list(organizations)
    for key, val in EXTRA_ORGS.items():
        all_orgs.append({"id": key, "name": val["name"], "type": val["type"], "level": val["level"], "parent": val["parent"], "location": val["location"]})

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>平凉市领导班子工作关系网络 — 中共平凉市委、平凉市人民政府及跨市人事交流</description>')
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

    for o in all_orgs:
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
    print(f"  Nodes: {len(persons) + len(all_orgs)}")
    print(f"  Edges: {eid}")


if __name__ == "__main__":
    build_database()
    build_gexf()
    print("\nDone. Generated artifacts:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
