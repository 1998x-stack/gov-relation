#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 静宁县 (Jingning County, Pingliang City, Gansu Province) leadership network.

Covers: Party Secretary (县委书记), County Mayor (县长), their predecessors/successors,
key deputy leaders, and cross-county exchange patterns.

Research date: 2026-07-22
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_静宁县")
DB_PATH = os.path.join(STAGING, "静宁县_network.db")
GEXF_PATH = os.path.join(STAGING, "静宁县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 县委书记 — 王蕾 (as of 2024.11-present)
    {"id":1,"name":"王蕾","gender":"女","ethnicity":"汉族","birth":"1978-10","birthplace":"甘肃泾川","education":"省委党校研究生学历","party_join":"2000-04","work_start":"1997-07","current_post":"静宁县委书记","current_org":"中共静宁县委员会","source":"https://baike.baidu.com/item/%E7%8E%8B%E8%95%BE/809858"},
    # 县长 — 杨宏 (as of 2024.12-present)
    {"id":2,"name":"杨宏","gender":"男","ethnicity":"汉族","birth":"1978-03","birthplace":"甘肃","education":"大学学历、法学学士","party_join":"中共党员","work_start":"","current_post":"静宁县委副书记、县长","current_org":"静宁县人民政府","source":"https://baike.baidu.com/item/%E6%9D%A8%E5%AE%8F/61192518"},

    # ── Predecessors — 县委书记 ──
    # 何鹏峰 — 前任县委书记 (2021.10-2024.10), 现平凉市委常委、宣传部部长
    {"id":3,"name":"何鹏峰","gender":"男","ethnicity":"汉族","birth":"1972-11","birthplace":"甘肃","education":"研究生学历","party_join":"中共党员","work_start":"1994-07","current_post":"平凉市委常委、宣传部部长","current_org":"中共平凉市委员会","source":"https://baike.baidu.com/item/%E4%BD%95%E9%B9%8F%E5%B3%B0"},
    # 何鹏峰的前任 — 待查 (已排除王晓军)
    {"id":4,"name":"（待查）","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"前任静宁县委书记（何鹏峰之前），身份待查","current_org":"中共静宁县委员会","source":"待查"},

    # ── Predecessors — 县长 ──
    # 陈景春 — 前任县长 (约2019-2022), 现庄浪县委书记
    {"id":5,"name":"陈景春","gender":"男","ethnicity":"汉族","birth":"1973-11","birthplace":"甘肃泾川","education":"省委党校大学学历","party_join":"中共党员","work_start":"","current_post":"庄浪县委书记","current_org":"中共庄浪县委员会","source":"http://district.ce.cn/newarea/sddy/202003/16/t20200316_34497512.shtml"},

    # ── 县委领导班子成员 (Standing Committee) ──
    # 县委副书记、县长 — 杨宏 (already listed as id=2)
    # 县委副书记（专职）
    # 依据: 2024年1月政府分工通知中未列专职副书记，但360百科显示有县委副书记张兴荣、张薇（历史数据）
    # 目前已知的县委班子成员（包含交叉来源）:

    # 常务副县长 — 靳智德
    {"id":6,"name":"靳智德","gender":"男","ethnicity":"汉族","birth":"1974-02","birthplace":"甘肃华亭","education":"在职大学学历","party_join":"中共党员","work_start":"1994-07","current_post":"静宁县委常委、常务副县长","current_org":"静宁县人民政府","source":"https://baike.baidu.com/item/%E9%9D%B3%E6%99%BA%E5%BE%B7/18891095"},

    # 副县长 — 王利东 (公安)
    {"id":7,"name":"王利东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县副县长、县公安局局长","current_org":"静宁县人民政府","source":"静宁县人民政府办公室关于县政府领导班子成员工作分工的通知 (2024-01-19)"},

    # 副县长 — 赵亮亮 (农业/乡村振兴)
    {"id":8,"name":"赵亮亮","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县副县长（分管农业农村/乡村振兴）","current_org":"静宁县人民政府","source":"同上"},

    # 副县长 — 李刚 (东西协作)
    {"id":9,"name":"李刚","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县副县长（东西部协作帮扶）","current_org":"静宁县人民政府","source":"同上"},

    # 副县长 — 王悉润
    {"id":10,"name":"王悉润","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县副县长（人社/自然资源/商贸/市场监管/招商）","current_org":"静宁县人民政府","source":"同上"},

    # 副县长 — 陈平 (文旅/新闻)
    {"id":11,"name":"陈平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县副县长（乡村振兴帮扶/文旅/新闻媒体）","current_org":"静宁县人民政府","source":"同上"},

    # 副县长 — 孙炳旭 (金融/帮扶)
    {"id":12,"name":"孙炳旭","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县副县长（中央定点帮扶/金融/保险）","current_org":"静宁县人民政府","source":"同上"},

    # 副县长 — 陈小兵 (工信/交通/环保)
    {"id":13,"name":"陈小兵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"甘肃静宁","education":"中央党校大学学历","party_join":"中共党员","work_start":"","current_post":"静宁县副县长（工信/交通/生态环境）","current_org":"静宁县人民政府","source":"同上"},

    # 副县长 — 李宇 (民生/教育/卫健)
    {"id":14,"name":"李宇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县副县长（民族宗教/教育/卫健/民政/科技）","current_org":"静宁县人民政府","source":"同上"},

    # 县委常委、政法委书记 — 马存维 (基于2026年3月新闻)
    # 历史: 2024年分工中王敏曾任政法委书记，目前更新为马存维
    {"id":15,"name":"马存维","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县委常委、政法委书记","current_org":"中共静宁县委政法委","source":"静宁县领导督查非煤矿山企业安全生产工作 (2026-03-13)"},

    # 县人大常委会主任 — 王永平 (基于2024年检察调研新闻)
    {"id":16,"name":"王永平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县人大常委会主任","current_org":"静宁县人大常委会","source":"静宁县四大机关主要领导调研检察工作"},

    # 县政协主席 — 王宁香
    {"id":17,"name":"王宁香","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县政协主席","current_org":"政协静宁县委员会","source":"静宁县四大机关主要领导调研检察工作"},

    # ── 历史关键人物 ──
    # 张兴荣 — 曾任静宁县委副书记、县长(2016年前后)
    {"id":18,"name":"张兴荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"静宁县前任县长","current_org":"","source":"360百科 静宁县词条"},

    # 王晓军 — 平凉市委常委、政法委书记（曾被误认为静宁县委书记）
    {"id":19,"name":"王晓军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"平凉市委常委、政法委书记","current_org":"中共平凉市委员会","source":"项目已有数据（build_平凉市_data.py）"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共静宁县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市静宁县"},
    {"id":2,"name":"静宁县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市静宁县"},
    {"id":3,"name":"静宁县人大常委会","type":"人大","level":"县级","parent":"平凉市人大常委会","location":"甘肃省平凉市静宁县"},
    {"id":4,"name":"政协静宁县委员会","type":"政协","level":"县级","parent":"政协平凉市委员会","location":"甘肃省平凉市静宁县"},
    {"id":5,"name":"中共静宁县委政法委","type":"党委","level":"县级","parent":"中共静宁县委员会","location":"甘肃省平凉市静宁县"},
    {"id":6,"name":"静宁县公安局","type":"政府","level":"科级","parent":"静宁县人民政府","location":"甘肃省平凉市静宁县"},
    {"id":7,"name":"中共平凉市委员会","type":"党委","level":"地市级","parent":"中共甘肃省委员会","location":"甘肃省平凉市"},
    {"id":8,"name":"平凉市人民政府","type":"政府","level":"地市级","parent":"甘肃省人民政府","location":"甘肃省平凉市"},
    {"id":9,"name":"中共庄浪县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市庄浪县"},
    {"id":10,"name":"庄浪县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市庄浪县"},
    {"id":11,"name":"共青团平凉市委员会","type":"群团","level":"地市级","parent":"中共平凉市委员会","location":"甘肃省平凉市"},
    {"id":12,"name":"共青团平凉地委","type":"群团","level":"地市级","parent":"中共平凉地区委员会","location":"甘肃省平凉市"},
    {"id":13,"name":"中共崇信县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市崇信县"},
    {"id":14,"name":"中共泾川县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市泾川县"},
    {"id":15,"name":"泾川县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市泾川县"},
    {"id":16,"name":"平凉市林业和草原局","type":"政府","level":"地市级","parent":"平凉市人民政府","location":"甘肃省平凉市"},
    {"id":17,"name":"共青团泾川县委员会","type":"群团","level":"县级","parent":"中共泾川县委员会","location":"甘肃省平凉市泾川县"},
    {"id":18,"name":"平凉市崆峒区委","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市崆峒区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 王蕾 (id=1) ──
    {"person_id":1,"org_id":12,"title":"共青团平凉地委干部","start":"1997-07","end":"2003-01","rank":"科员级","note":"1997年7月参加工作"},
    {"person_id":1,"org_id":11,"title":"平凉市少先队总辅导员","start":"2003-01","end":"2004-03","rank":"","note":"期间2001.08-2003.12参加中央党校函授学院本科班行政管理专业学习"},
    {"person_id":1,"org_id":11,"title":"共青团平凉市委学少部副部长","start":"2004-03","end":"2006-03","rank":"副科级","note":"期间2004.09-2005.01在甘肃省委组织部第23期女干部培训班学习"},
    {"person_id":1,"org_id":11,"title":"共青团平凉市委学少部部长","start":"2006-03","end":"2009-08","rank":"正科级","note":""},
    {"person_id":1,"org_id":11,"title":"共青团平凉市委副书记","start":"2009-08","end":"2013-04","rank":"副处级","note":""},
    {"person_id":1,"org_id":11,"title":"共青团平凉市委书记","start":"2013-04","end":"2018-06","rank":"正处级","note":"期间2015.03-2015.06在甘肃省委党校第46期中青班学习，2015.11-2016.01在天津市西青区挂职锻炼"},
    {"person_id":1,"org_id":13,"title":"崇信县委副书记（正县级）","start":"2018-06","end":"2021-08","rank":"正处级","note":""},
    {"person_id":1,"org_id":2,"title":"静宁县人民政府副县长、代理县长","start":"2021-08","end":"2021-11","rank":"正处级","note":"2021年8月任代理县长"},
    {"person_id":1,"org_id":2,"title":"静宁县县长（二级巡视员）","start":"2021-11","end":"2024-11","rank":"正处级","note":"2021年11月当选县长；2024年11月拟任县委书记"},
    {"person_id":1,"org_id":1,"title":"静宁县委书记","start":"2024-11","end":"至今","rank":"正处级","note":"2024年11月24日省委组织部任前公示，后正式任职"},

    # ── 杨宏 (id=2) ──
    {"person_id":2,"org_id":15,"title":"泾川县政府副县长、县公安局局长","start":"","end":"2020-12","rank":"副处级","note":"精确起止年月待查"},
    {"person_id":2,"org_id":14,"title":"泾川县委常委、政法委书记","start":"2020-12","end":"","rank":"副处级","note":""},
    {"person_id":2,"org_id":18,"title":"平凉市崆峒区委常委、组织部部长","start":"","end":"2024-03","rank":"副处级","note":"精确起止年月待查"},
    {"person_id":2,"org_id":15,"title":"泾川县委常委、县政府党组副书记、常务副县长","start":"2024-03","end":"2024-12","rank":"副处级","note":""},
    {"person_id":2,"org_id":2,"title":"静宁县人民政府副县长、代理县长","start":"2024-12-03","end":"2024-12-25","rank":"正处级","note":"2024年12月3日县人大常委会任命代理县长"},
    {"person_id":2,"org_id":2,"title":"静宁县县长","start":"2024-12-25","end":"至今","rank":"正处级","note":"2024年12月25日县十八届人大四次会议当选县长"},

    # ── 何鹏峰 (id=3) ──
    {"person_id":3,"org_id":14,"title":"泾川县罗汉洞乡政府干部","start":"1994-07","end":"1995-03","rank":"科员级","note":""},
    {"person_id":3,"org_id":14,"title":"泾川县城建局干部","start":"1995-03","end":"1998-03","rank":"科员级","note":""},
    {"person_id":3,"org_id":14,"title":"中共泾川县委组织部干部","start":"1998-03","end":"2000-12","rank":"科员级","note":""},
    {"person_id":3,"org_id":14,"title":"泾川县委组织员","start":"2000-12","end":"2002-08","rank":"副科级","note":""},
    {"person_id":3,"org_id":17,"title":"共青团泾川县委书记","start":"2002-08","end":"2003-04","rank":"正科级","note":""},
    {"person_id":3,"org_id":11,"title":"共青团平凉市委办公室主任","start":"2003-04","end":"2007-08","rank":"正科级","note":""},
    {"person_id":3,"org_id":11,"title":"共青团平凉市委副书记","start":"2007-08","end":"2010-05","rank":"副处级","note":""},
    {"person_id":3,"org_id":1,"title":"静宁县委常委、组织部部长","start":"2010-05","end":"2013-12","rank":"副处级","note":""},
    {"person_id":3,"org_id":2,"title":"静宁县委常委、常务副县长","start":"2013-12","end":"2016-09","rank":"副处级","note":""},
    {"person_id":3,"org_id":1,"title":"静宁县委副书记、常务副县长","start":"2016-09","end":"2016-10","rank":"副处级","note":""},
    {"person_id":3,"org_id":1,"title":"静宁县委副书记","start":"2016-10","end":"2018-06","rank":"副处级","note":""},
    {"person_id":3,"org_id":16,"title":"平凉市林业局党组书记、局长","start":"2018-06","end":"2019-01","rank":"正处级","note":""},
    {"person_id":3,"org_id":16,"title":"平凉市林业和草原局党组书记、局长","start":"2019-01","end":"2021-10","rank":"正处级","note":""},
    {"person_id":3,"org_id":1,"title":"静宁县委书记、一级调研员","start":"2021-10","end":"2024-10","rank":"正处级","note":""},
    {"person_id":3,"org_id":8,"title":"平凉市副市长、党组成员","start":"2024-10","end":"2025-12","rank":"副厅级","note":""},
    {"person_id":3,"org_id":7,"title":"平凉市委常委、宣传部部长","start":"2025-12","end":"至今","rank":"副厅级","note":""},

    # ── 陈景春 (id=5) ──
    {"person_id":5,"org_id":2,"title":"静宁县委常委、常务副县长（三级调研员）","start":"","end":"2020-03","rank":"副处级","note":"2020年3月任前公示显示为静宁县委常委、常务副县长、三级调研员"},
    {"person_id":5,"org_id":1,"title":"静宁县委副书记","start":"2020-03","end":"2020","rank":"副处级","note":"2020年3月拟任静宁县委副书记，拟提名为县长候选人"},
    {"person_id":5,"org_id":2,"title":"静宁县委副书记、县长","start":"2020","end":"2022","rank":"正处级","note":"精确起止月待查"},
    {"person_id":5,"org_id":9,"title":"庄浪县委书记","start":"2022","end":"至今","rank":"正处级","note":"约2022年起任庄浪县委书记"},

    # ── 靳智德 (id=6) ──
    {"person_id":6,"org_id":14,"title":"华亭市东华镇党委书记","start":"","end":"","rank":"正科级","note":"华亭市（原华亭县）东华镇"},
    {"person_id":6,"org_id":14,"title":"华亭工业园区党委书记","start":"","end":"","rank":"","note":""},
    {"person_id":6,"org_id":14,"title":"华亭市政府副市长","start":"","end":"","rank":"副处级","note":"任前公示: 拟任县（市、区）党委常委"},
    {"person_id":6,"org_id":2,"title":"静宁县委常委、常务副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 王利东 (id=7) ──
    {"person_id":7,"org_id":6,"title":"静宁县副县长、县公安局局长","start":"","end":"至今","rank":"副处级","note":"依据2024年1月政府分工通知确认"},

    # ── 赵亮亮 (id=8) ──
    {"person_id":8,"org_id":2,"title":"静宁县副县长（农业农村/乡村振兴）","start":"","end":"至今","rank":"副处级","note":""},

    # ── 马存维 (id=15) ──
    {"person_id":15,"org_id":5,"title":"静宁县委常委、政法委书记","start":"","end":"至今","rank":"副处级","note":"2026年3月13日新闻显示已任此职"},

    # ── 张兴荣 (id=18) ──
    {"person_id":18,"org_id":2,"title":"静宁县县长","start":"","end":"","rank":"正处级","note":"历史数据，360百科记载"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王蕾 ← 何鹏峰（县委书记继任）
    {"person_a":1,"person_b":3,"type":"predecessor_successor","context":"王蕾接任何鹏峰任静宁县委书记","overlap_org":"中共静宁县委员会","overlap_period":"2024-10~2024-11","strength":"strong","confidence":"confirmed"},
    # 王蕾 ← 陈景春（县长继任）
    {"person_a":1,"person_b":5,"type":"predecessor_successor","context":"王蕾接替陈景春任静宁县县长","overlap_org":"静宁县人民政府","overlap_period":"2022~2024","strength":"strong","confidence":"confirmed"},
    # 王蕾 → 杨宏（县长继任）
    {"person_a":2,"person_b":1,"type":"predecessor_successor","context":"杨宏接替王蕾任静宁县县长（王蕾升任县委书记）","overlap_org":"静宁县人民政府","overlap_period":"2024-12","strength":"strong","confidence":"confirmed"},
    # 何鹏峰 ↔ 陈景春（党政搭档）
    {"person_a":3,"person_b":5,"type":"overlap","context":"何鹏峰任静宁县委书记期间与陈景春（县长）党政搭档","overlap_org":"静宁县","overlap_period":"2021-10~2022","strength":"medium","confidence":"confirmed"},
    # 何鹏峰 ↔ 杨宏（泾川关联）
    {"person_a":3,"person_b":2,"type":"overlap","context":"何鹏峰早年（1994-2003）在泾川县工作，杨宏曾任泾川县副县长/公安局长/常务副县长","overlap_org":"泾川县","overlap_period":"1994-2003 / 2024","strength":"weak","confidence":"plausible"},
    # 王蕾 ↔ 靳智德（党政班子共事）
    {"person_a":1,"person_b":6,"type":"overlap","context":"王蕾任县委书记/县长期间与常务副县长靳智德共事","overlap_org":"静宁县人民政府","overlap_period":"2022~至今","strength":"strong","confidence":"confirmed"},
    # 陈景春 ↔ 靳智德（共事）
    {"person_a":5,"person_b":6,"type":"overlap","context":"陈景春任静宁县县长期间与常务副县长靳智德共事（或交叉）","overlap_org":"静宁县人民政府","overlap_period":"2020~2022","strength":"medium","confidence":"plausible"},
    # 杨宏 ↔ 靳智德（党政班子共事）
    {"person_a":2,"person_b":6,"type":"overlap","context":"杨宏任县长期间与常务副县长靳智德共事","overlap_org":"静宁县人民政府","overlap_period":"2024-12~至今","strength":"strong","confidence":"confirmed"},
    # 张兴荣 → 陈景春（县长继任）
    {"person_a":18,"person_b":5,"type":"predecessor_successor","context":"张兴荣之后陈景春接任静宁县县长","overlap_org":"静宁县人民政府","overlap_period":"","strength":"weak","confidence":"unverified"},
    # 王蕾 → 崇信关联（曾任崇信县委副书记）
    {"person_a":1,"person_b":6,"type":"same_system","context":"王蕾曾任崇信县委副书记，与华亭（靳智德原工作地）同属平凉市","overlap_org":"平凉市","overlap_period":"2018-2021","strength":"weak","confidence":"unverified"},
]

confirmed_relationships = [r for r in relationships if r["confidence"] == "confirmed"]

# =========================================================================
# BUILD DATABASE
# =========================================================================
os.makedirs(STAGING, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript('''
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
    birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER, title TEXT,
    start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER, type TEXT,
    context TEXT, overlap_org TEXT, overlap_period TEXT,
    strength TEXT, confidence TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
''')

for p in persons:
    c.execute('''INSERT OR REPLACE INTO persons
        (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
        (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))

for o in organizations:
    c.execute('''INSERT OR REPLACE INTO organizations
        (id,name,type,level,parent,location)
        VALUES (?,?,?,?,?,?)''',
        (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

for pos in positions:
    c.execute('''INSERT INTO positions
        (person_id,org_id,title,start,end,rank,note)
        VALUES (?,?,?,?,?,?,?)''',
        (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))

for r in relationships:
    c.execute('''INSERT INTO relationships
        (person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence)
        VALUES (?,?,?,?,?,?,?,?)''',
        (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"],r["strength"],r["confidence"]))

conn.commit()
conn.close()

print(f"✅ Database written: {DB_PATH}")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

top_leader_ids = {1,2,3,5}  # 王蕾, 杨宏, 何鹏峰, 陈景春

def person_color(p):
    if p["id"] == 1:
        return "255,50,50"    # 县委书记 — 红色
    elif p["id"] == 2:
        return "50,100,255"   # 县长 — 蓝色
    elif p["id"] == 3:
        return "255,50,50"    # 前任县委书记 — 红色
    elif p["id"] == 5:
        return "50,100,255"   # 前任县长 — 蓝色
    elif p["id"] == 6:
        return "200,100,50"   # 常务副县长 — 橙色
    elif p["id"] == 15:
        return "255,165,0"    # 政法委书记 — 橙色
    else:
        return "100,100,100"  # 其他 — 灰色

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }
    return colors.get(o["type"], "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gansu Gov Relation Research Agent</creator>')
lines.append('    <description>静宁县领导班子工作关系网络 - 甘肃省平凉市静宁县</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="birth" type="string"/>')
lines.append('      <attribute id="3" title="birthplace" type="string"/>')
lines.append('      <attribute id="4" title="education" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="strength" type="string"/>')
lines.append('      <attribute id="2" title="confidence" type="string"/>')
lines.append('      <attribute id="3" title="context" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    if p["id"] == 4:
        continue  # Skip "待查" placeholder
    c_ = person_color(p)
    sz = "20.0" if p["id"] in top_leader_ids else "12.0"
    role_label = p["current_post"][:20] if len(p["current_post"]) > 20 else p["current_post"]
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(role_label)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["education"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    c_ = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('          <attvalue for="2" value=""/>')
    lines.append('          <attvalue for="3" value=""/>')
    lines.append('          <attvalue for="4" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# Person->Organization (worked_at)
for pos in positions:
    # Skip person 4 placeholder
    pp = next((p for p in persons if p["id"] == pos["person_id"]), None)
    if pp and pp["id"] == 4:
        continue
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append('          <attvalue for="1" value="1.0"/>')
    lines.append('          <attvalue for="2" value="confirmed"/>')
    lines.append(f'          <attvalue for="3" value="{esc(pos["title"] + " (" + pos["start"] + " - " + pos["end"] + ")")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person->Person (relationships)
for r in relationships:
    eid += 1
    w = {"strong": "2.0", "medium": "1.5", "weak": "1.0"}.get(r["strength"], "1.0")
    edge_color = "#DAA520" if r["strength"] == "strong" else ("#4169E1" if r["strength"] == "medium" else "#999999")
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{r["strength"]}"/>')
    lines.append(f'          <attvalue for="2" value="{r["confidence"]}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{edge_color[1:3]}" g="{edge_color[3:5]}" b="{edge_color[5:7]}"/>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF written: {GEXF_PATH}")

# =========================================================================
# SUMMARY
# =========================================================================
print(f"\n📊 静宁县 Leadership Network Summary:")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")
print(f"   Confirmed relationships: {len(confirmed_relationships)}")
print(f"\n   Key figures:")
for p in persons:
    if p["id"] in top_leader_ids:
        print(f"     - {p['name']}: {p['current_post']}")
print(f"\n   Cross-county connections:")
print(f"     - 王蕾: 崇信县委副书记 -> 静宁")
print(f"     - 杨宏: 泾川 -> 崆峒 -> 泾川 -> 静宁")
print(f"     - 何鹏峰: 泾川 -> 静宁 -> 平凉市")
print(f"     - 陈景春: 静宁 -> 庄浪")
print(f"     - 靳智德: 华亭 -> 静宁")
