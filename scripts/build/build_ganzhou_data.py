#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Ganzhou City (赣州市) leadership network.

Covers: city-level leaders (mayor, party secretary, vice mayors, party committee),
plus predecessor chain and key connections.
"""
import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/ganzhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/ganzhou_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    {"id":1, "name":"黄喜忠", "gender":"男", "ethnicity":"汉族", "birth":"1969-11", "birthplace":"广东普宁", "education":"清华大学电机工程与应用电子技术系电气及其自动化专业本科；华南理工大学工商管理硕士、管理学博士", "party_join":"1992-06", "work_start":"1993-07", "current_post":"江西省委常委、赣州市委书记、赣州军分区党委第一书记", "current_org":"中共赣州市委员会", "source":"https://zh.wikipedia.org/wiki/%E9%BB%84%E5%96%9C%E5%BF%A0; https://www.ganzhou.gov.cn"},
    {"id":2, "name":"漆海云", "gender":"男", "ethnicity":"汉族", "birth":"1971-11", "birthplace":"江西丰城", "education":"大学本科学历", "party_join":"1992-12", "work_start":"1993-08", "current_post":"赣州市委副书记、市长、市政府党组书记", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/sz001/zw_sz.shtml; https://zh.wikipedia.org/wiki/%E8%B5%A3%E5%B7%9E"},

    # ── Government vice mayors ──
    {"id":3, "name":"何琦", "gender":"男", "ethnicity":"汉族", "birth":"1970-11", "birthplace":"江西高安", "education":"北京科技大学冶金系钢铁冶金专业，大学学历，工学学士", "party_join":"1999-02", "work_start":"1992-08", "current_post":"赣州市委常委、副市长（常务副市长）", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/gzhq/zw_sz.shtml"},
    {"id":4, "name":"聂兆华", "gender":"男", "ethnicity":"汉族", "birth":"1971-02", "birthplace":"山东肥城", "education":"历史学硕士", "party_join":"1996-06", "work_start":"1996-07", "current_post":"赣州市委常委、副市长（挂职），赣南苏区振兴发展工作办公室副主任", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/dlt/zw_sz.shtml"},
    {"id":5, "name":"刘通", "gender":"男", "ethnicity":"汉族", "birth":"1971-09", "birthplace":"四川通江", "education":"中国人民大学经济学博士，研究员", "party_join":"1997-12", "work_start":"1994-07", "current_post":"赣州市委常委、副市长（挂职），国家发改委国土开发与地区经济研究所副所长", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/dfl/zw_sz.shtml"},
    {"id":6, "name":"罗瑞华", "gender":"男", "ethnicity":"汉族", "birth":"1968-03", "birthplace":"江西瑞金", "education":"农业推广硕士", "party_join":"2000-03", "work_start":"1992-08", "current_post":"赣州市副市长", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/c114522/zw_sz.shtml"},
    {"id":7, "name":"邹治宇", "gender":"男", "ethnicity":"汉族", "birth":"1976-06", "birthplace":"湖北武汉", "education":"研究生学历（武汉大学审计学+日本亚太大学国际合作政策硕士）", "party_join":"1998-11", "work_start":"1999-08", "current_post":"赣州市副市长", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/csl/zw_sz.shtml"},
    {"id":8, "name":"叶新", "gender":"男", "ethnicity":"汉族", "birth":"1971-04", "birthplace":"江西武宁", "education":"中央党校研究生学历", "party_join":"1993-01", "work_start":"1993-07", "current_post":"赣州市副市长、市公安局局长", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/c1024372/zw_sz.shtml"},
    {"id":9, "name":"雷鸣", "gender":"男", "ethnicity":"畲族", "birth":"1976-12", "birthplace":"江西瑞金", "education":"大学本科学历", "party_join":"中国民主建国会", "work_start":"1998-10", "current_post":"赣州市副市长、民建赣州市委会主委（非中共党员）", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/gzslm/zw_sz.shtml"},
    {"id":10, "name":"连天浪", "gender":"男", "ethnicity":"汉族", "birth":"1969-03", "birthplace":"江西信丰", "education":"大学学历", "party_join":"1987-06", "work_start":"1987-08", "current_post":"赣州市副市长", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/ltl/zw_sz.shtml"},
    {"id":11, "name":"谢卫东", "gender":"男", "ethnicity":"汉族", "birth":"1968-09", "birthplace":"江西安远", "education":"大学学历", "party_join":"1994-06", "work_start":"1989-08", "current_post":"赣州市政府秘书长、党组成员", "current_org":"赣州市人民政府", "source":"https://www.ganzhou.gov.cn/gzszf/xwd/zw_sz.shtml"},

    # ── Predecessors (previous party secretaries and mayors) ──
    {"id":12, "name":"吴忠琼", "gender":"女", "ethnicity":"汉族", "birth":"1964-09", "birthplace":"湖北武汉/安徽肥东", "education":"北京航空航天大学（原北京航空学院）固体力学硕士", "party_join":"中共党员", "work_start":"1988-08", "current_post":"江西省人大常委会副主任（原江西省委副书记、赣州市委书记）", "current_org":"江西省人大常委会", "source":"https://zh.wikipedia.org/wiki/%E5%90%B4%E5%BF%A0%E7%90%BC"},
    {"id":13, "name":"李炳军", "gender":"男", "ethnicity":"汉族", "birth":"1963-02", "birthplace":"山东临朐", "education":"山东化工学院（现青岛科技大学）", "party_join":"中共党员", "work_start":"1984-08", "current_post":"贵州省省长", "current_org":"贵州省人民政府", "source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E7%82%B3%E5%86%9B"},
    {"id":14, "name":"曾文明", "gender":"男", "ethnicity":"汉族", "birth":"1963-01", "birthplace":"", "education":"", "party_join":"中共党员", "work_start":"", "current_post":"（原赣州市长→江西省发改委主任→省政协副主席，已退休）", "current_org":"", "source":"公开报道"},
    {"id":15, "name":"许南吉", "gender":"男", "ethnicity":"汉族", "birth":"1973-??", "birthplace":"", "education":"", "party_join":"中共党员", "work_start":"", "current_post":"（原赣州市长→宜春市委书记→福建省副省长？）", "current_org":"（调福建省任职）", "source":"公开报道"},
    {"id":16, "name":"李克坚", "gender":"男", "ethnicity":"汉族", "birth":"1969-06", "birthplace":"河南伊川", "education":"吉安师专体育系+江西省委党校研究生", "party_join":"中共党员", "work_start":"", "current_post":"（原赣州市长→江西省政府秘书长）", "current_org":"江西省人民政府", "source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E5%85%8B%E5%9D%9A"},
    {"id":17, "name":"万凯", "gender":"男", "ethnicity":"汉族", "birth":"1973-09", "birthplace":"江西南昌", "education":"江西省人民警察学校", "party_join":"中共党员", "work_start":"", "current_post":"（原赣州市长→2022年5月被调查）", "current_org":"", "source":"https://zh.wikipedia.org/wiki/%E4%B8%87%E5%87%AF"},
    {"id":18, "name":"史文清", "gender":"男", "ethnicity":"汉族", "birth":"1954-10", "birthplace":"", "education":"", "party_join":"中共党员", "work_start":"", "current_post":"（原赣州市委书记→2018年退休→2022年因受贿被判死缓）", "current_org":"", "source":"公开报道"},
    {"id":19, "name":"冷新生", "gender":"男", "ethnicity":"汉族", "birth":"1964-10", "birthplace":"", "education":"", "party_join":"中共党员", "work_start":"", "current_post":"（原赣州市长→江西省工信委主任→2017年被调查）", "current_org":"", "source":"公开报道"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1, "name":"中共赣州市委员会", "type":"党委", "level":"地级", "parent":"中共江西省委员会", "location":"江西省赣州市"},
    {"id":2, "name":"赣州市人民政府", "type":"政府", "level":"地级", "parent":"江西省人民政府", "location":"江西省赣州市"},
    {"id":3, "name":"赣州市人大常委会", "type":"人大", "level":"地级", "parent":"江西省人大常委会", "location":"江西省赣州市"},
    {"id":4, "name":"政协赣州市委员会", "type":"政协", "level":"地级", "parent":"政协江西省委员会", "location":"江西省赣州市"},
    {"id":5, "name":"江西省人民政府", "type":"政府", "level":"省级", "parent":"", "location":"江西省南昌市"},
    {"id":6, "name":"中共江西省委员会", "type":"党委", "level":"省级", "parent":"", "location":"江西省南昌市"},
    {"id":7, "name":"赣南苏区振兴发展工作办公室", "type":"政府", "level":"省级", "parent":"江西省人民政府", "location":"江西省赣州市"},
    {"id":8, "name":"国家发展和改革委员会", "type":"政府", "level":"国家级", "parent":"国务院", "location":"北京市"},
    {"id":9, "name":"交通运输部", "type":"政府", "level":"国家级", "parent":"国务院", "location":"北京市"},
    {"id":10, "name":"中共中央组织部", "type":"党委", "level":"国家级", "parent":"中共中央", "location":"北京市"},
    {"id":11, "name":"江西省公安厅", "type":"政府", "level":"省级", "parent":"江西省人民政府", "location":"江西省南昌市"},
    {"id":12, "name":"南昌市工业和信息化局", "type":"政府", "level":"市级", "parent":"南昌市人民政府", "location":"江西省南昌市"},
    {"id":13, "name":"鹰潭市", "type":"党委/政府", "level":"地级", "parent":"江西省", "location":"江西省鹰潭市"},
    {"id":14, "name":"中共宜春市委员会", "type":"党委", "level":"地级", "parent":"中共江西省委员会", "location":"江西省宜春市"},
    {"id":15, "name":"贵州省人民政府", "type":"政府", "level":"省级", "parent":"", "location":"贵州省贵阳市"},
    {"id":16, "name":"赣州市公安局", "type":"政府", "level":"市级", "parent":"赣州市人民政府", "location":"江西省赣州市"},
    {"id":17, "name":"江西省政府办公厅（省政府秘书长）", "type":"政府", "level":"省级", "parent":"江西省人民政府", "location":"江西省南昌市"},
    {"id":18, "name":"江西省人大常委会", "type":"人大", "level":"省级", "parent":"", "location":"江西省南昌市"},
    {"id":19, "name":"广东省人民政府", "type":"政府", "level":"省级", "parent":"", "location":"广东省广州市"},
    {"id":20, "name":"江西省公安厅", "type":"政府", "level":"省级", "parent":"江西省人民政府", "location":"江西省南昌市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 黄喜忠 ──
    {"id":1, "person_id":1, "org_id":1, "title":"赣州市委书记（省委常委兼任）", "start":"2024-12", "end":"", "rank":"副省级", "note":"2024年12月16日任命，接替吴忠琼"},
    {"id":2, "person_id":1, "org_id":6, "title":"江西省委常委", "start":"2021-11", "end":"", "rank":"副省级", "note":"第十五届江西省委常委"},
    {"id":3, "person_id":1, "org_id":6, "title":"江西省委统战部部长", "start":"2021-12", "end":"~2025-09", "rank":"副省级", "note":"兼任省政协党组副书记"},
    {"id":4, "person_id":1, "org_id":13, "title":"鹰潭市委书记", "start":"2021-02", "end":"2021-12", "rank":"正厅级", "note":"从南昌市长转任"},
    {"id":5, "person_id":1, "org_id":2, "title":"南昌市委副书记、市长", "start":"2019-12", "end":"2021-02", "rank":"副省级城市市长", "note":"跨省交流至江西后的首个职务"},
    {"id":6, "person_id":1, "org_id":5, "title":"广东省清远市市长", "start":"2018-03", "end":"2019-12", "rank":"正厅级", "note":"广东期间正厅级首任"},
    {"id":7, "person_id":1, "org_id":5, "title":"佛山市委常委、统战部部长", "start":"2016-11", "end":"2018-03", "rank":"副厅级", "note":""},
    {"id":8, "person_id":1, "org_id":5, "title":"佛山市副市长", "start":"2015-09", "end":"2016-11", "rank":"副厅级", "note":""},
    {"id":9, "person_id":1, "org_id":5, "title":"佛山市顺德区委副书记、区长", "start":"2011-04", "end":"2015-09", "rank":"副厅级", "note":"2012年5月起为副厅级"},
    {"id":10, "person_id":1, "org_id":5, "title":"佛山市禅城区委副书记、区长", "start":"2008-08", "end":"2011-04", "rank":"正处级", "note":""},
    {"id":11, "person_id":1, "org_id":5, "title":"佛山市禅城区副区长", "start":"2005", "end":"2008-08", "rank":"副处级", "note":""},
    {"id":12, "person_id":1, "org_id":5, "title":"广东省科技厅（历任）", "start":"1993-07", "end":"2005", "rank":"科员至副处长", "note":"清华毕业后在广东省科技厅体系工作12年"},

    # ── 漆海云 ──
    {"id":13, "person_id":2, "org_id":2, "title":"赣州市市长、党组书记", "start":"~2025-09（代）→2026-01（正式）", "end":"", "rank":"正厅级", "note":"接替李克坚，漆海云此前在江西省任省直机关职务"},
    {"id":14, "person_id":2, "org_id":5, "title":"江西省政府副秘书长（待核实）", "start":"~2022", "end":"~2025-09", "rank":"正厅级", "note":"漆海云2024年前履历待查"},

    # ── 何琦 ──
    {"id":11, "person_id":3, "org_id":1, "title":"赣州市委常委", "start":"2021-10", "end":"", "rank":"副厅级", "note":""},
    {"id":12, "person_id":3, "org_id":2, "title":"赣州市副市长", "start":"2021-10", "end":"", "rank":"副厅级", "note":"实际承担常务副市长职责"},
    {"id":13, "person_id":3, "org_id":5, "title":"江西省工信厅副厅长", "start":"2021-01", "end":"2021-08", "rank":"副厅级", "note":""},
    {"id":14, "person_id":3, "org_id":12, "title":"南昌市工信局局长、党组书记", "start":"2019-02", "end":"2021-01", "rank":"正处级", "note":""},
    {"id":15, "person_id":3, "org_id":12, "title":"南昌市工信委主任、党委书记", "start":"2016-12", "end":"2019-02", "rank":"正处级", "note":""},
    {"id":16, "person_id":3, "org_id":12, "title":"南昌市政府副秘书长", "start":"2016-09", "end":"2016-12", "rank":"正处级", "note":""},
    {"id":17, "person_id":3, "org_id":12, "title":"南昌市政府办公厅副主任", "start":"2015-09", "end":"2016-09", "rank":"副处级", "note":""},
    {"id":18, "person_id":3, "org_id":12, "title":"南昌市工信委总经济师", "start":"2012-10", "end":"2015-09", "rank":"副处级", "note":""},
    {"id":19, "person_id":3, "org_id":12, "title":"南昌市经贸委副调研员", "start":"2008-06", "end":"2012-10", "rank":"副处级", "note":""},
    {"id":20, "person_id":3, "org_id":12, "title":"南昌市经贸委政策法规处处长", "start":"2002-11", "end":"2008-06", "rank":"正科级", "note":""},
    {"id":21, "person_id":3, "org_id":12, "title":"南昌市经贸委信息综合调研科副科长", "start":"2000-12", "end":"2002-11", "rank":"副科级", "note":""},
    {"id":22, "person_id":3, "org_id":12, "title":"南昌市经贸委办公室科员", "start":"1997-03", "end":"2000-12", "rank":"科员", "note":"其间1997.05-1999.06挂职南昌县武阳镇镇长助理"},
    {"id":23, "person_id":3, "org_id":5, "title":"南昌市经委办公室科员", "start":"1995-03", "end":"1997-03", "rank":"科员", "note":""},
    {"id":24, "person_id":3, "org_id":5, "title":"南昌钢铁厂转炉分厂技术科工艺员", "start":"1993-07", "end":"1995-03", "rank":"", "note":"北京科技大学毕业分配"},
    {"id":25, "person_id":3, "org_id":5, "title":"南昌钢铁厂炼铁分厂炉前工", "start":"1992-08", "end":"1993-07", "rank":"", "note":"大学毕业后首份工作"},

    # ── 聂兆华（挂职） ──
    {"id":26, "person_id":4, "org_id":1, "title":"赣州市委常委、副市长（挂职）", "start":"", "end":"", "rank":"副厅级", "note":"中央单位挂职干部"},
    {"id":27, "person_id":4, "org_id":7, "title":"赣南苏区振兴发展工作办公室副主任", "start":"", "end":"", "rank":"", "note":"兼任"},
    {"id":28, "person_id":4, "org_id":10, "title":"中央巡视组副局级巡视专员", "start":"", "end":"", "rank":"副局级", "note":"此前为中组部干部监督局四处处长等"},

    # ── 刘通（挂职） ──
    {"id":29, "person_id":5, "org_id":1, "title":"赣州市委常委、副市长（挂职）", "start":"", "end":"", "rank":"副厅级", "note":"国家发改委挂职"},
    {"id":30, "person_id":5, "org_id":7, "title":"赣南苏区振兴发展工作办公室副主任", "start":"", "end":"", "rank":"", "note":"兼任"},
    {"id":31, "person_id":5, "org_id":8, "title":"国家发改委国土开发与地区经济研究所副所长", "start":"", "end":"", "rank":"", "note":""},

    # ── 罗瑞华 ──
    {"id":32, "person_id":6, "org_id":2, "title":"赣州市副市长", "start":"", "end":"", "rank":"副厅级", "note":"分管民政、人社、农业农村等"},
    {"id":33, "person_id":6, "org_id":5, "title":"赣州市乡村振兴局局长", "start":"~2021", "end":"", "rank":"正处级", "note":""},
    {"id":34, "person_id":6, "org_id":5, "title":"赣州市扶贫办公室主任", "start":"", "end":"~2021", "rank":"正处级", "note":""},
    {"id":35, "person_id":6, "org_id":5, "title":"兴国县委副书记", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":36, "person_id":6, "org_id":5, "title":"石城县委副书记", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":37, "person_id":6, "org_id":5, "title":"宁都县委常委、宣传部部长", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":38, "person_id":6, "org_id":5, "title":"于都县委常委", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":39, "person_id":6, "org_id":5, "title":"于都县政府副县长", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":40, "person_id":6, "org_id":5, "title":"赣州市林业局（历任）", "start":"1992-08", "end":"", "rank":"逐步晋升", "note":"赣州地区林业局起步"},

    # ── 邹治宇 ──
    {"id":41, "person_id":7, "org_id":2, "title":"赣州市副市长", "start":"2023-01", "end":"", "rank":"副厅级", "note":"分管交通、商务、文旅等"},
    {"id":42, "person_id":7, "org_id":9, "title":"交通运输部河北海事局纪检组组长", "start":"2021-06", "end":"2022-09", "rank":"副厅级", "note":""},
    {"id":43, "person_id":7, "org_id":9, "title":"交通运输部机关党委办公室主任", "start":"2018-11", "end":"2019-12", "rank":"正处级", "note":""},
    {"id":44, "person_id":7, "org_id":9, "title":"交通运输部机关党委群众工作部部长", "start":"2014-04", "end":"2018-11", "rank":"正处级", "note":""},
    {"id":45, "person_id":7, "org_id":9, "title":"交通运输部直属机关团委书记", "start":"2012-07", "end":"2018-01", "rank":"正处级", "note":""},
    {"id":46, "person_id":7, "org_id":9, "title":"交通运输部财务司预算管理处副处长", "start":"2011-12", "end":"2012-07", "rank":"副处级", "note":""},

    # ── 叶新 ──
    {"id":47, "person_id":8, "org_id":2, "title":"赣州市副市长、市公安局局长", "start":"2024-02", "end":"", "rank":"副厅级", "note":""},
    {"id":48, "person_id":8, "org_id":11, "title":"江西省公安厅交通管理局局长", "start":"2022-01", "end":"2024-01", "rank":"正处级", "note":""},
    {"id":49, "person_id":8, "org_id":11, "title":"江西省公安厅技术侦察总队总队长", "start":"2020-01", "end":"2022-01", "rank":"正处级", "note":""},
    {"id":50, "person_id":8, "org_id":11, "title":"江西省公安厅新闻舆情处处长", "start":"2015-09", "end":"2020-01", "rank":"正处级", "note":""},
    {"id":51, "person_id":8, "org_id":11, "title":"江西省公安厅指挥调度处政委", "start":"2012-03", "end":"2015-09", "rank":"副处级", "note":""},
    {"id":52, "person_id":8, "org_id":11, "title":"江西省公安厅交警总队直属五支队支队长", "start":"2009-09", "end":"2012-03", "rank":"副处级", "note":""},
    {"id":53, "person_id":8, "org_id":11, "title":"江西省公安厅交警总队（历任）", "start":"1993-07", "end":"2009-09", "rank":"逐步晋升", "note":"从省警校毕业入省交警总队"},

    # ── 雷鸣（非党） ──
    {"id":54, "person_id":9, "org_id":2, "title":"赣州市副市长", "start":"", "end":"", "rank":"副厅级", "note":"教育、体育、市场监管"},
    {"id":55, "person_id":9, "org_id":4, "title":"赣州市政协副主席（曾任）", "start":"", "end":"", "rank":"副厅级", "note":""},
    {"id":56, "person_id":9, "org_id":5, "title":"赣州经开区管委会调研员", "start":"", "end":"", "rank":"正处级", "note":""},
    {"id":57, "person_id":9, "org_id":5, "title":"章贡区副区长", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":58, "person_id":9, "org_id":5, "title":"章贡区检察院副检察长", "start":"", "end":"", "rank":"", "note":""},

    # ── 连天浪 ──
    {"id":59, "person_id":10, "org_id":2, "title":"赣州市副市长", "start":"", "end":"", "rank":"副厅级", "note":"自然资源、住建、卫健等"},
    {"id":60, "person_id":10, "org_id":5, "title":"章贡区委书记", "start":"", "end":"", "rank":"正处级", "note":""},
    {"id":61, "person_id":10, "org_id":5, "title":"章贡区委副书记、区长", "start":"", "end":"", "rank":"正处级", "note":""},
    {"id":62, "person_id":10, "org_id":5, "title":"南康区委常委、常务副区长", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":63, "person_id":10, "org_id":5, "title":"章贡区副区长", "start":"", "end":"", "rank":"副处级", "note":""},
    {"id":64, "person_id":10, "org_id":5, "title":"信丰县西牛镇党委书记", "start":"", "end":"", "rank":"正科级", "note":""},

    # ── 谢卫东（秘书长） ──
    {"id":65, "person_id":11, "org_id":2, "title":"赣州市政府秘书长", "start":"", "end":"", "rank":"正处级", "note":""},
    {"id":66, "person_id":11, "org_id":5, "title":"赣州综合保税区党工委书记", "start":"", "end":"", "rank":"正处级", "note":""},

    # ── Predecessors ──
    {"id":72, "person_id":12, "org_id":1, "title":"赣州市委书记（前任）", "start":"2021-01", "end":"2024-12", "rank":"副省级", "note":"吴忠琼同时担任江西省委副书记"},
    {"id":73, "person_id":12, "org_id":6, "title":"江西省委副书记", "start":"2021-11", "end":"2024-12", "rank":"副省级", "note":"兼任赣州市委书记"},
    {"id":74, "person_id":12, "org_id":5, "title":"江西省副省长", "start":"2018-01", "end":"2021-01", "rank":"副省级", "note":""},
    {"id":75, "person_id":12, "org_id":5, "title":"辽宁省发改委主任", "start":"2015-12", "end":"2018-01", "rank":"正厅级", "note":"跨省交流前在辽宁任职"},
    {"id":76, "person_id":12, "org_id":5, "title":"鞍山市市长", "start":"2013-06", "end":"2015-12", "rank":"正厅级", "note":""},
    {"id":77, "person_id":12, "org_id":5, "title":"辽宁省科技厅厅长", "start":"2010", "end":"2013", "rank":"正厅级", "note":""},
    {"id":78, "person_id":13, "org_id":1, "title":"赣州市委书记", "start":"2015-07", "end":"2020-11", "rank":"副省级", "note":"兼任江西省委副书记"},
    {"id":79, "person_id":13, "org_id":6, "title":"江西省委副书记", "start":"2015-07", "end":"2020-11", "rank":"副省级", "note":""},
    {"id":80, "person_id":13, "org_id":5, "title":"江西省副省长", "start":"2013-07", "end":"2015-07", "rank":"副省级", "note":""},
    {"id":81, "person_id":13, "org_id":15, "title":"贵州省省长", "start":"2020-11", "end":"", "rank":"正省级", "note":"从赣州市委书记直升贵州省省长（特殊晋升路径）"},
    {"id":82, "person_id":14, "org_id":2, "title":"赣州市市长", "start":"2016-09", "end":"2021-02", "rank":"正厅级", "note":"后调任省发改委"},
    {"id":83, "person_id":14, "org_id":5, "title":"江西省发改委主任", "start":"2021-02", "end":"~2022", "rank":"正厅级", "note":""},
    {"id":84, "person_id":14, "org_id":5, "title":"江西省统计局局长", "start":"~2014", "end":"2016-09", "rank":"正厅级", "note":""},
    {"id":85, "person_id":15, "org_id":2, "title":"赣州市市长", "start":"2021-02", "end":"2021-12", "rank":"正厅级", "note":"短暂任职约10个月后调离"},
    {"id":86, "person_id":15, "org_id":14, "title":"宜春市委书记", "start":"2021-12", "end":"~2024-10", "rank":"正厅级", "note":"后调往福建省"},
    {"id":87, "person_id":16, "org_id":2, "title":"赣州市市长", "start":"2022-07（代理）→2022-08（正式）", "end":"2025-09", "rank":"正厅级", "note":"接替被调查的万凯"},
    {"id":88, "person_id":16, "org_id":5, "title":"江西省政府秘书长", "start":"2025-09", "end":"", "rank":"正厅级", "note":"李克坚去向：调任省政府秘书长"},
    {"id":89, "person_id":16, "org_id":5, "title":"吉安市委常委、常务副市长", "start":"2021-09", "end":"2022-01（升任省体育局长）", "rank":"副厅级", "note":""},
    {"id":90, "person_id":16, "org_id":5, "title":"江西省体育局局长", "start":"2022-01", "end":"2022-07", "rank":"正厅级", "note":"短暂任职省体育局后调任赣州"},
    {"id":91, "person_id":17, "org_id":2, "title":"赣州市市长", "start":"2021-12", "end":"2022-05", "rank":"正厅级", "note":"上任仅5个月即被调查"},
    {"id":92, "person_id":17, "org_id":5, "title":"江西省公安厅党委副书记、常务副厅长", "start":"2019-08", "end":"2021-12", "rank":"正厅级", "note":""},
    {"id":93, "person_id":17, "org_id":5, "title":"抚州市副市长、公安局长", "start":"2016-11", "end":"2019-08", "rank":"副厅级", "note":""},
    {"id":94, "person_id":17, "org_id":5, "title":"进贤县委书记", "start":"2013-07", "end":"2016-11", "rank":"正处级", "note":""},
    {"id":95, "person_id":18, "org_id":1, "title":"赣州市委书记", "start":"2010-10", "end":"2015-07", "rank":"副省级", "note":"后退休→2022年因受贿被判处死刑缓期执行"},
    {"id":96, "person_id":18, "org_id":5, "title":"江西省副省长", "start":"~2008", "end":"~2010", "rank":"副省级", "note":""},
    {"id":97, "person_id":19, "org_id":2, "title":"赣州市长", "start":"2011-08", "end":"2016-09", "rank":"正厅级", "note":"后任省工信委主任→2017年被调查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {"id":1, "person_a":1, "person_b":2, "type":"党政搭档", "context":"黄喜忠（市委书记）与漆海云（市长）为赣州市党政一把手", "overlap_org":"赣州市", "overlap_period":"2026-01至今"},
    {"id":2, "person_a":1, "person_b":12, "type":"前后任", "context":"黄喜忠（2024-12）接替吴忠琼（2021-01至2024-12）任赣州市委书记", "overlap_org":"中共赣州市委员会", "overlap_period":"不重叠"},
    {"id":3, "person_a":12, "person_b":13, "type":"前后任", "context":"吴忠琼（2021-01）接替李炳军（2015-07至2020-11）", "overlap_org":"中共赣州市委员会", "overlap_period":"不重叠"},
    {"id":4, "person_a":13, "person_b":18, "type":"前后任", "context":"李炳军接替史文清。史文清已于2022年因受贿被判死缓", "overlap_org":"中共赣州市委员会", "overlap_period":"不重叠"},
    {"id":5, "person_a":2, "person_b":16, "type":"前后任", "context":"漆海云（2026-01正式）接替李克坚（2022-07至2025-09）任赣州市长", "overlap_org":"赣州市人民政府", "overlap_period":"不重叠"},
    {"id":6, "person_a":16, "person_b":17, "type":"前后任", "context":"李克坚接替万凯。万凯2022-05辞职被调查", "overlap_org":"赣州市人民政府", "overlap_period":"不重叠"},
    {"id":7, "person_a":15, "person_b":16, "type":"前后任", "context":"许南吉（~2021-02至2021-12）→被调查后由李克坚接任", "overlap_org":"赣州市人民政府", "overlap_period":"不重叠"},
    {"id":8, "person_a":14, "person_b":15, "type":"前后任", "context":"曾文明（2016-09至2021-02）→许南吉（2021-02至2021-12）", "overlap_org":"赣州市人民政府", "overlap_period":"不重叠"},

    # 何琦 connections
    {"id":7, "person_a":1, "person_b":3, "type":"直接上下级", "context":"黄喜忠（书记）领导何琦（常务副市长）。何琦是市政府实际上的二把手", "overlap_org":"赣州市", "overlap_period":"2021至今"},
    {"id":8, "person_a":2, "person_b":3, "type":"直接上下级", "context":"漆海云（市长）与何琦（常务副市长）为市政府正副手", "overlap_org":"赣州市人民政府", "overlap_period":"~2024至今"},

    # 挂职干部 connections (from central government)
    {"id":9, "person_a":4, "person_b":10, "type":"中央单位挂职", "context":"聂兆华来自中组部，挂职赣州常委、副市长", "overlap_org":"中组部→赣州市", "overlap_period":""},
    {"id":10, "person_a":5, "person_b":8, "type":"中央单位挂职", "context":"刘通来自国家发改委，挂职赣州常委、副市长", "overlap_org":"国家发改委→赣州市", "overlap_period":""},
    {"id":11, "person_a":7, "person_b":9, "type":"中央单位出身", "context":"邹治宇来自交通运输部，曾任交通运输部多个司局职务", "overlap_org":"交通运输部→赣州市", "overlap_period":"2023至今"},

    # 叶新 connections
    {"id":12, "person_a":8, "person_b":11, "type":"公安系统出身", "context":"叶新从江西省公安厅调任赣州任公安局长", "overlap_org":"江西省公安厅", "overlap_period":"1993-2024"},

    # 赣州本地干部 network
    {"id":13, "person_a":6, "person_b":2, "type":"直接上下级", "context":"罗瑞华长期在赣州本地任职，熟悉地方情况", "overlap_org":"赣州市人民政府", "overlap_period":""},
    {"id":14, "person_a":10, "person_b":2, "type":"直接上下级", "context":"连天浪从章贡区委书记升任副市长", "overlap_org":"赣州市人民政府", "overlap_period":""},
    {"id":15, "person_a":10, "person_b":9, "type":"章贡区系统", "context":"连天浪（章贡区委书记）与雷鸣（章贡区副区长/区政协副主席）曾在章贡区共事", "overlap_org":"章贡区", "overlap_period":""},

    # 何琦的南昌connections&跨系统
    {"id":16, "person_a":3, "person_b":12, "type":"南昌系统", "context":"何琦长期在南昌市经委/工信系统工作（1992-2021），后调任赣州", "overlap_org":"南昌市", "overlap_period":"1992-2021"},

    # 黄喜忠与何琦的上下级关系
    {"id":17, "person_a":1, "person_b":4, "type":"党政上下级", "context":"黄喜忠（书记）领导聂兆华（挂职常委副市长）", "overlap_org":"中共赣州市委员会", "overlap_period":""},
    {"id":18, "person_a":1, "person_b":5, "type":"党政上下级", "context":"黄喜忠（书记）领导刘通（挂职常委副市长）", "overlap_org":"中共赣州市委员会", "overlap_period":""},

    # 前任关系 — 市长异常更迭
    {"id":19, "person_a":17, "person_b":16, "type":"异常更迭", "context":"万凯2021-12任赣州市长，仅5个月后2022-05辞职被查。李克坚紧急接任", "overlap_org":"赣州市人民政府", "overlap_period":"不重叠（万凯被查后李克坚接任）"},

    # 李炳军的特殊晋升
    {"id":20, "person_a":13, "person_b":15, "type":"赣州→省级", "context":"李炳军从赣州市委书记直接升任贵州省省长，是赣州走出的最高级别官员之一", "overlap_org":"赣州市", "overlap_period":"2015-2020"},

    # 黄喜忠的广东背景
    {"id":21, "person_a":1, "person_b":5, "type":"跨省交流", "context":"黄喜忠在广东省科技厅、佛山市、清远市工作26年（1993-2019），属广东籍跨省交流干部", "overlap_org":"广东省", "overlap_period":"1993-2019"},
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
    if "书记" in post and ("市委" in post or "县委书记" in post or "区委书记" in post or "市委书记" in post):
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
    if "秘书长" in post:
        return "130,160,200"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255","政协":"230,200,255",
            "新区":"200,255,200","开发区":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>赣州市（市级）领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    cp = p.get("current_post","")
    sz = "20.0" if ("市委书记" in cp and "市委" in cp) or ("市长" in cp and "市" in cp) else "12.0"
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
