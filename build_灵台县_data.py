#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 灵台县 (Lingtai County, Pingliang City, Gansu Province) leadership network.

Covers: Party Secretary (县委书记), County Mayor (县长), their predecessors/successors,
key deputy leaders, and cross-county exchange patterns.
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_灵台县")
DB_PATH = os.path.join(STAGING, "灵台县_network.db")
GEXF_PATH = os.path.join(STAGING, "灵台县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 马创成 — 灵台县委书记 (as of 2026), 回族
    {"id":1,"name":"马创成","gender":"男","ethnicity":"回族","birth":"1982-07","birthplace":"甘肃张家川（推测）","education":"在职研究生学历","party_join":"中共党员","work_start":"2003-03","current_post":"灵台县委书记","current_org":"中共灵台县委员会","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/xwld/art/2022/art_d19c283a7914463b9945223dbe2f044e.html"},
    # 王立满 — 灵台县委副书记、县长 (as of 2026), 工学博士
    {"id":2,"name":"王立满","gender":"男","ethnicity":"汉族","birth":"1987-01","birthplace":"","education":"研究生、工学博士","party_join":"中共党员","work_start":"","current_post":"灵台县委副书记、县长","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/xzfld/art/2022/art_779b15766af949919cc3f9508f4951fa.html"},

    # ── Predecessors — 县委书记 ──
    # 王度林 — 曾任灵台县委书记，现平凉市委常委、副市长
    {"id":3,"name":"王度林","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、副市长（曾任灵台县委书记）","current_org":"平凉市人民政府","source":"https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},

    # ── Predecessors — 县长 ──
    # 文斌 — 原灵台县长（姓名待最终确认）
    {"id":4,"name":"文斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原灵台县长","current_org":"","source":"https://www.pingliang.gov.cn/"},

    # ── 县委领导班子成员（从官方领导之窗页面确认）──
    {"id":5,"name":"牛犇","gender":"男","ethnicity":"汉族","birth":"1984-10","birthplace":"","education":"大学、法学学士","party_join":"中共党员","work_start":"","current_post":"灵台县委副书记","current_org":"中共灵台县委员会","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":6,"name":"江小兵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、常务副县长","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":7,"name":"杨定国","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、宣传部部长","current_org":"中共灵台县委宣传部","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":8,"name":"王璟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、纪委书记、县监委代理主任","current_org":"中共灵台县纪律检查委员会","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":9,"name":"李丽云","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、统战部部长","current_org":"中共灵台县委统战部","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":10,"name":"刘贵明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、政法委书记","current_org":"中共灵台县委政法委","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":11,"name":"张文博","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、组织部部长","current_org":"中共灵台县委组织部","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":12,"name":"陈邑","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、人武部部长","current_org":"灵台县人民武装部","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":13,"name":"姚思俊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、副县长","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":14,"name":"李欢","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、副县长（挂职）","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":15,"name":"高军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县委常委、副县长（挂职）","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},

    # ── 县政府其他副县长 ──
    {"id":16,"name":"赵真","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县副县长","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zwdt/ltyw/art/2026/art_5dbffeae8d6e49cd9069d55f6213d886.html"},
    {"id":17,"name":"刘晶晶","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县副县长","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":18,"name":"王海涛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县副县长","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},
    {"id":19,"name":"范夕程","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"灵台县副县长","current_org":"灵台县人民政府","source":"https://www.lingtai.gov.cn/zfxxgk/fdzdgknr/jgjj/xzfld/index.html"},

    # ── 灵台籍在外任职人员（跨县交流）──
    {"id":20,"name":"刘懿平","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"甘肃灵台","education":"省委党校研究生、农业推广硕士","party_join":"中共党员","work_start":"1995-07","current_post":"泾川县委书记（灵台籍）","current_org":"中共泾川县委员会","source":"https://baike.baidu.com/item/%E5%88%98%E6%87%BF%E5%B9%B3/3553790"},
    {"id":21,"name":"于宏勤","gender":"男","ethnicity":"汉族","birth":"1971-03","birthplace":"甘肃灵台","education":"中央党校函授经济管理专业","party_join":"1997-05","work_start":"","current_post":"平凉市人大常委会党组成员、副主任（灵台籍）","current_org":"平凉市人大常委会","source":"https://baike.baidu.com/item/%E4%BA%8E%E5%AE%8F%E5%8B%A4"},
    {"id":22,"name":"景晓东","gender":"男","ethnicity":"汉族","birth":"1974-03","birthplace":"甘肃灵台","education":"","party_join":"中共党员","work_start":"","current_post":"华亭市委书记（灵台籍）","current_org":"中共华亭市委员会","source":"https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共灵台县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市灵台县"},
    {"id":2,"name":"灵台县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市灵台县"},
    {"id":3,"name":"灵台县人大常委会","type":"人大","level":"县级","parent":"平凉市人大常委会","location":"甘肃省平凉市灵台县"},
    {"id":4,"name":"政协灵台县委员会","type":"政协","level":"县级","parent":"政协平凉市委员会","location":"甘肃省平凉市灵台县"},
    {"id":5,"name":"中共灵台县纪律检查委员会","type":"党委","level":"县级","parent":"中共灵台县委员会","location":"甘肃省平凉市灵台县"},
    {"id":6,"name":"中共灵台县委组织部","type":"党委","level":"县级","parent":"中共灵台县委员会","location":"甘肃省平凉市灵台县"},
    {"id":7,"name":"中共灵台县委宣传部","type":"党委","level":"县级","parent":"中共灵台县委员会","location":"甘肃省平凉市灵台县"},
    {"id":8,"name":"中共灵台县委统战部","type":"党委","level":"县级","parent":"中共灵台县委员会","location":"甘肃省平凉市灵台县"},
    {"id":9,"name":"中共灵台县委政法委","type":"党委","level":"县级","parent":"中共灵台县委员会","location":"甘肃省平凉市灵台县"},
    {"id":10,"name":"灵台县公安局","type":"政府","level":"县级","parent":"灵台县人民政府","location":"甘肃省平凉市灵台县"},

    # 马创成前工作相关机构（张家川县/天水市）
    {"id":11,"name":"中共天水市张家川县委","type":"党委","level":"县级","parent":"中共天水市委员会","location":"甘肃省天水市张家川县"},
    {"id":12,"name":"张家川县人民政府","type":"政府","level":"县级","parent":"天水市人民政府","location":"甘肃省天水市张家川县"},
    {"id":13,"name":"张家川县川王乡","type":"乡镇","level":"乡镇","parent":"张家川县人民政府","location":"甘肃省天水市张家川县"},
    {"id":14,"name":"中共张家川县委组织部","type":"党委","level":"县级","parent":"中共天水市张家川县委","location":"甘肃省天水市张家川县"},
    {"id":15,"name":"张家川县大阳镇","type":"乡镇","level":"乡镇","parent":"张家川县人民政府","location":"甘肃省天水市张家川县"},
    {"id":16,"name":"天水市张家川镇","type":"乡镇","level":"乡镇","parent":"张家川县人民政府","location":"甘肃省天水市张家川县"},

    # 跨县交流相关机构
    {"id":17,"name":"中共泾川县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市泾川县"},
    {"id":18,"name":"平凉市人大常委会","type":"人大","level":"地级","parent":"甘肃省人大常委会","location":"甘肃省平凉市"},
    {"id":19,"name":"中共华亭市委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市华亭市"},
    {"id":20,"name":"平凉市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省平凉市"},
    {"id":21,"name":"中共平凉市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省平凉市"},
    {"id":22,"name":"灵台县人民武装部","type":"政府","level":"县级","parent":"平凉军分区","location":"甘肃省平凉市灵台县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 马创成 (id=1) — 灵台县委书记，回族，1982.07生 ──
    {"pid":1,"org":1,"title":"灵台县委书记","start":"","end":"至今","rank":"正处级","note":"此前任张家川县委副书记、县长；跨市交流从天水到平凉"},
    {"pid":1,"org":11,"title":"张家川县委副书记、县长","start":"2021-11","end":"","rank":"正处级","note":"张家川县委副书记、县政府党组书记、县长"},
    {"pid":1,"org":12,"title":"张家川县副县长（兼张家川镇党委书记）","start":"2019-04","end":"2021-11","rank":"副处级","note":"张家川县人民政府党组成员"},
    {"pid":1,"org":16,"title":"张家川镇党委书记","start":"2017-12","end":"2019-04","rank":"正科级","note":"精准扶贫工作站站长"},
    {"pid":1,"org":15,"title":"大阳镇党委书记","start":"2016-05","end":"2017-12","rank":"正科级","note":""},
    {"pid":1,"org":15,"title":"大阳乡党委副书记、乡长","start":"2013-03","end":"2016-05","rank":"正科级","note":""},
    {"pid":1,"org":14,"title":"张家川县委组织部组织员","start":"2010-12","end":"2013-03","rank":"","note":""},
    {"pid":1,"org":13,"title":"张家川县川王乡计生办公室主任","start":"2009-12","end":"2010-12","rank":"","note":""},
    {"pid":1,"org":13,"title":"张家川县川王乡干部","start":"2003-03","end":"2009-12","rank":"","note":""},

    # ── 王立满 (id=2) — 灵台县长，汉族，1987.01生，工学博士 ──
    {"pid":2,"org":2,"title":"灵台县委副书记、县长","start":"","end":"至今","rank":"正处级","note":"县政府党组书记，主持县政府全面工作，主管审计局"},

    # ── 王度林 (id=3) — 前任灵台县委书记 ──
    {"pid":3,"org":20,"title":"平凉市委常委、副市长","start":"2025-12","end":"至今","rank":"副厅级","note":""},
    {"pid":3,"org":21,"title":"平凉市委常委","start":"2025-12","end":"至今","rank":"副厅级","note":""},
    {"pid":3,"org":1,"title":"灵台县委书记（曾任）","start":"","end":"","rank":"正处级","note":"曾任灵台县委书记，具体时间待确认"},

    # ── 文斌 (id=4) — 前任灵台县长 ──
    {"pid":4,"org":2,"title":"灵台县长（曾任）","start":"","end":"","rank":"正处级","note":"前任灵台县长，具体时间待确认"},

    # ── 牛犇 (id=5) — 县委副书记，1984.10生 ──
    {"pid":5,"org":1,"title":"灵台县委副书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 江小兵 (id=6) — 常务副县长 ──
    {"pid":6,"org":2,"title":"灵台县委常委、常务副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 杨定国 (id=7) — 宣传部部长 ──
    {"pid":7,"org":7,"title":"灵台县委常委、宣传部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 王璟 (id=8) — 纪委书记 ──
    {"pid":8,"org":5,"title":"灵台县委常委、纪委书记、县监委代理主任","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李丽云 (id=9) — 统战部部长 ──
    {"pid":9,"org":8,"title":"灵台县委常委、统战部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 刘贵明 (id=10) — 政法委书记 ──
    {"pid":10,"org":9,"title":"灵台县委常委、政法委书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张文博 (id=11) — 组织部部长 ──
    {"pid":11,"org":6,"title":"灵台县委常委、组织部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 陈邑 (id=12) — 人武部部长 ──
    {"pid":12,"org":22,"title":"灵台县委常委、人武部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 姚思俊 (id=13) — 副县长 ──
    {"pid":13,"org":2,"title":"灵台县委常委、副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李欢 (id=14) — 挂职副县长 ──
    {"pid":14,"org":2,"title":"灵台县委常委、副县长（挂职）","start":"","end":"至今","rank":"副处级","note":""},

    # ── 高军 (id=15) — 挂职副县长 ──
    {"pid":15,"org":2,"title":"灵台县委常委、副县长（挂职）","start":"","end":"至今","rank":"副处级","note":""},

    # ── 赵真 (id=16) — 副县长 ──
    {"pid":16,"org":2,"title":"灵台县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 刘晶晶 (id=17) — 副县长 ──
    {"pid":17,"org":2,"title":"灵台县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 王海涛 (id=18) — 副县长 ──
    {"pid":18,"org":2,"title":"灵台县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 范夕程 (id=19) — 副县长 ──
    {"pid":19,"org":2,"title":"灵台县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 刘懿平 (id=20) — 灵台籍，泾川县委书记 ──
    {"pid":20,"org":17,"title":"泾川县委书记","start":"2024-12","end":"至今","rank":"正处级（二级巡视员）","note":""},
    {"pid":20,"org":17,"title":"泾川县委副书记、县长","start":"","end":"2024-12","rank":"正处级","note":""},

    # ── 于宏勤 (id=21) — 灵台籍，平凉市人大副主任 ──
    {"pid":21,"org":18,"title":"平凉市人大常委会党组成员、副主任","start":"2025-02","end":"至今","rank":"副厅级","note":""},
    {"pid":21,"org":17,"title":"泾川县委书记","start":"2021-08","end":"2024-12","rank":"正处级","note":""},

    # ── 景晓东 (id=22) — 灵台籍，华亭市委书记 ──
    {"pid":22,"org":19,"title":"华亭市委书记","start":"","end":"至今","rank":"正处级","note":"1974.03生，甘肃灵台人"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 马创成 ↔ 王立满 (current party secretary - county mayor)
    {"a":1,"b":2,"type":"overlap","context":"马创成任灵台县委书记，王立满任县长，党政搭档","overlap_org":"中共灵台县委员会、灵台县人民政府","overlap_period":"至今","strength":"strong","confidence":"confirmed"},

    # 马创成 ↔ 王度林 (predecessor-successor, 县委书记)
    {"a":1,"b":3,"type":"predecessor_successor","context":"马创成接替王度林担任灵台县委书记","overlap_org":"中共灵台县委员会","overlap_period":"","strength":"strong","confidence":"plausible"},

    # 王立满 ↔ 文斌 (predecessor-successor, 县长)
    {"a":2,"b":4,"type":"predecessor_successor","context":"王立满接替文斌担任灵台县长","overlap_org":"灵台县人民政府","overlap_period":"","strength":"strong","confidence":"plausible"},

    # 马创成 ↔ 牛犇 (县委书记 - 县委副书记)
    {"a":1,"b":5,"type":"superior_subordinate","context":"马创成任县委书记，牛犇任县委副书记","overlap_org":"中共灵台县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 马创成 ↔ 江小兵 (县委书记 - 常务副县长)
    {"a":1,"b":6,"type":"superior_subordinate","context":"马创成任县委书记，江小兵任常务副县长","overlap_org":"中共灵台县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 马创成 ↔ 王璟 (县委书记 - 纪委书记)
    {"a":1,"b":8,"type":"superior_subordinate","context":"马创成任县委书记，王璟任县纪委书记","overlap_org":"中共灵台县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 马创成 ↔ 杨定国 (县委书记 - 宣传部部长)
    {"a":1,"b":7,"type":"superior_subordinate","context":"马创成任县委书记，杨定国任宣传部部长","overlap_org":"中共灵台县委员会","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 王立满 ↔ 江小兵 (县长 - 常务副县长)
    {"a":2,"b":6,"type":"superior_subordinate","context":"王立满任县长，江小兵任常务副县长","overlap_org":"灵台县人民政府","overlap_period":"至今","strength":"medium","confidence":"confirmed"},

    # 刘懿平 ↔ 于宏勤 (同籍贯灵台，先后任泾川县委书记)
    {"a":20,"b":21,"type":"same_native","context":"刘懿平与于宏勤均为灵台人，先后任泾川县委书记","overlap_org":"","overlap_period":"","strength":"weak","confidence":"confirmed"},

    # 刘懿平 ↔ 景晓东 (同籍贯灵台)
    {"a":20,"b":22,"type":"same_native","context":"刘懿平与景晓东均为灵台人","overlap_org":"","overlap_period":"","strength":"weak","confidence":"confirmed"},

    # 于宏勤 ↔ 景晓东 (同籍贯灵台)
    {"a":21,"b":22,"type":"same_native","context":"于宏勤与景晓东均为灵台人","overlap_org":"","overlap_period":"","strength":"weak","confidence":"confirmed"},
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
        if "书记" in current and "纪委" not in current and "人大" not in current and "政协" not in current:
            return "255,50,50"  # Red — party secretary
        if "县长" in current or "市长" in current or "副市长" in current or "人大" in current:
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "政协" in current:
            return "255,240,200"  # Cream - CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        if name in ("马创成", "王立满", "王度林"):
            return "20.0"
        if name in ("刘懿平", "于宏勤", "景晓东", "文斌"):
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
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>灵台县领导班子工作关系网络 — 中共灵台县委、灵台县人民政府及跨县人事交流</description>')
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

    # Nodes - persons
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

    # Nodes - organizations
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
