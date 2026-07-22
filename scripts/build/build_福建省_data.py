#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Fujian Province (福建省) leadership network.

Covers: Provincial Party Secretary (省委书记), Governor (省长), predecessors,
succession chains, key deputy leaders (省委常委会成员, 副省长等),
and the provincial-level leadership structure.

Sources:
- Fujian Provincial Government official website (www.fujian.gov.cn) — current leaders
- Baidu Baike — biographical data for Zhou Zuyi, Zhao Long
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/福建省_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/福建省_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 周祖翼 — 福建省委书记、省人大常委会主任 (as of 2022.11)
    {"id":1,"name":"周祖翼","gender":"男","ethnicity":"汉族","birth":"1965-01","birthplace":"浙江天台","education":"浙江大学地质学系理学学士、同济大学理学博士","party_join":"1984-06","work_start":"1989-10","current_post":"福建省委书记、省人大常委会主任","current_org":"中共福建省委员会","source":"https://baike.baidu.com/item/%E5%91%A8%E7%A5%96%E7%BF%BC/3311477"},
    # 赵龙 — 福建省省长
    {"id":2,"name":"赵龙","gender":"男","ethnicity":"汉族","birth":"1967-09","birthplace":"辽宁盘锦","education":"中国人民大学土地管理系土地管理专业本科、北京大学与国家行政学院公共管理硕士","party_join":"1988-12","work_start":"1989-07","current_post":"福建省委副书记、省长","current_org":"福建省人民政府","source":"https://baike.baidu.com/item/%E8%B5%B5%E9%BE%99/4302261"},

    # ── Provincial leadership (省委常委会成员) ──
    # Based on known appointments
    {"id":3,"name":"王永礼","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省委常委、常务副省长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":4,"name":"李建成","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省委常委、副省长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":5,"name":"林瑞良","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省委常委、副省长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":6,"name":"王金福","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省副省长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":7,"name":"江尔雄","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省副省长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":8,"name":"赵增连","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省副省长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":9,"name":"魏晓奎","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省副省长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":10,"name":"伍斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省人民政府党组成员","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":11,"name":"康涛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省人民政府党组成员","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},
    {"id":12,"name":"李斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省人民政府秘书长","current_org":"福建省人民政府","source":"https://www.fujian.gov.cn"},

    # ── Predecessors — 省委书记 ──
    {"id":13,"name":"尹力","gender":"男","ethnicity":"汉族","birth":"1962-08","birthplace":"山东临邑","education":"山东医科大学医学硕士、俄罗斯医学科学院博士","party_join":"","work_start":"","current_post":"中央宣传部部长（原福建省委书记）","current_org":"中共中央宣传部","source":"https://baike.baidu.com/item/%E5%B0%B9%E5%8A%9B"},
    {"id":14,"name":"于伟国","gender":"男","ethnicity":"汉族","birth":"1955-10","birthplace":"","education":"","party_join":"","work_start":"","current_post":"全国人大（原福建省委书记）","current_org":"全国人大常委会","source":"https://baike.baidu.com/item/%E4%BA%8E%E4%BC%9F%E5%9B%BD"},
    {"id":15,"name":"尤权","gender":"男","ethnicity":"汉族","birth":"1954-01","birthplace":"","education":"","party_join":"","work_start":"","current_post":"中央统战部原部长（原福建省委书记）","current_org":"中共中央统战部","source":"https://baike.baidu.com/item/%E5%B0%A4%E6%9D%83"},
    {"id":16,"name":"孙春兰","gender":"女","ethnicity":"汉族","birth":"1955-05","birthplace":"","education":"","party_join":"","work_start":"","current_post":"国务院原副总理（原福建省委书记）","current_org":"国务院","source":"https://baike.baidu.com/item/%E5%AD%99%E6%98%A5%E5%85%B0"},

    # ── Predecessors — 省长 ──
    {"id":17,"name":"王宁","gender":"男","ethnicity":"汉族","birth":"1961-04","birthplace":"湖南湘乡","education":"","party_join":"","work_start":"","current_post":"中央金融委员会办公室（原福建省省长）","current_org":"中央金融委员会","source":"https://baike.baidu.com/item/%E7%8E%8B%E5%AE%81"},
    {"id":18,"name":"唐登杰","gender":"男","ethnicity":"汉族","birth":"1964-06","birthplace":"","education":"","party_join":"","work_start":"","current_post":"民政部原部长（原福建省省长）","current_org":"民政部","source":"https://baike.baidu.com/item/%E5%94%90%E7%99%BB%E6%9D%B0"},
    {"id":19,"name":"于伟国","gender":"男","ethnicity":"汉族","birth":"1955-10","birthplace":"","education":"","party_join":"","work_start":"","current_post":"全国人大（原福建省省长、省委书记）","current_org":"全国人大常委会","source":"https://baike.baidu.com/item/%E4%BA%8E%E4%BC%9F%E5%9B%BD"},

    # ── Other key provincial leaders ──
    {"id":20,"name":"张彦","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省委常委、宣传部部长（原）","current_org":"中共福建省委宣传部","source":"https://www.fujian.gov.cn"},
    {"id":21,"name":"迟耀云","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省委常委、省纪委书记（原）","current_org":"中共福建省纪律检查委员会","source":"https://www.fujian.gov.cn"},
    {"id":22,"name":"邢善萍","gender":"女","ethnicity":"汉族","birth":"1968-05","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省委副书记（原）","current_org":"中共福建省委员会","source":"https://www.fujian.gov.cn"},
    {"id":23,"name":"罗东川","gender":"男","ethnicity":"汉族","birth":"1965-10","birthplace":"","education":"","party_join":"","work_start":"","current_post":"福建省委副书记、政法委书记（原）","current_org":"中共福建省委员会","source":"https://www.fujian.gov.cn"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Fujian provincial core
    {"id":1,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
    {"id":2,"name":"福建省人民政府","type":"政府","level":"省级","parent":"","location":"福建省福州市"},
    {"id":3,"name":"福建省人大常委会","type":"人大","level":"省级","parent":"","location":"福建省福州市"},
    {"id":4,"name":"政协福建省委员会","type":"政协","level":"省级","parent":"","location":"福建省福州市"},
    {"id":5,"name":"中共福建省纪律检查委员会","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},

    # Key provincial departments
    {"id":6,"name":"中共福建省委组织部","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":7,"name":"中共福建省委宣传部","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":8,"name":"中共福建省委统战部","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":9,"name":"中共福建省委政法委","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":10,"name":"福建省公安厅","type":"政府","level":"省级","parent":"福建省人民政府","location":"福建省福州市"},
    {"id":11,"name":"福建省审计厅","type":"政府","level":"省级","parent":"福建省人民政府","location":"福建省福州市"},

    # Key cities (副省级/地级)
    {"id":12,"name":"中共厦门市委员会","type":"党委","level":"副省级","parent":"中共福建省委员会","location":"福建省厦门市"},
    {"id":13,"name":"厦门市人民政府","type":"政府","level":"副省级","parent":"福建省人民政府","location":"福建省厦门市"},
    {"id":14,"name":"中共福州市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":15,"name":"福州市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省福州市"},
    {"id":16,"name":"中共泉州市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省泉州市"},
    {"id":17,"name":"泉州市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省泉州市"},

    # Central / national orgs
    {"id":18,"name":"中共中央宣传部","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":19,"name":"全国人大常委会","type":"人大","level":"国家级","parent":"","location":"北京市"},
    {"id":20,"name":"中共中央统战部","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":21,"name":"国务院","type":"政府","level":"国家级","parent":"","location":"北京市"},
    {"id":22,"name":"中央金融委员会","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":23,"name":"民政部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":24,"name":"中央政治局","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":25,"name":"国家土地管理局","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":26,"name":"国土资源部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":27,"name":"自然资源部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":28,"name":"国家土地督察济南局","type":"政府","level":"国家级","parent":"国土资源部","location":"山东省济南市"},
    {"id":29,"name":"中央组织部","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":30,"name":"中央机构编制委员会办公室","type":"党委","level":"国家级","parent":"","location":"北京市"},
    {"id":31,"name":"人力资源和社会保障部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":32,"name":"同济大学","type":"事业单位","level":"","parent":"教育部","location":"上海市"},
    {"id":33,"name":"浙江大学","type":"事业单位","level":"","parent":"教育部","location":"浙江省杭州市"},
    {"id":34,"name":"中国人民大学","type":"事业单位","level":"","parent":"教育部","location":"北京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Zhou Zuyi (周祖翼) — Party Secretary
    {"person_id":1,"org_id":1,"title":"福建省委书记","start":"2022-11","end":"present","rank":"正省级","note":"第二十届中央委员，2023年1月起兼任省人大常委会主任"},
    {"person_id":1,"org_id":3,"title":"福建省人大常委会主任","start":"2023-01","end":"present","rank":"正省级","note":""},
    {"person_id":1,"org_id":31,"title":"人力资源和社会保障部党组书记、部长","start":"2022-05","end":"2022-11","rank":"正部级","note":"2022年5月任党组书记，6月任部长"},
    {"person_id":1,"org_id":30,"title":"中央机构编制委员会办公室主任","start":"2019-05","end":"2022-04","rank":"正部级","note":"兼任中央组织部副部长"},
    {"person_id":1,"org_id":29,"title":"中央组织部副部长","start":"2016-10","end":"2022-04","rank":"副部级","note":"2016.10任部务委员兼干部二局局长，2019.05明确为正部长级"},
    {"person_id":1,"org_id":29,"title":"中央组织部部务委员兼干部二局局长","start":"2014-08","end":"2016-10","rank":"副部级","note":""},
    {"person_id":1,"org_id":32,"title":"同济大学党委书记","start":"2011-11","end":"2014-08","rank":"副部长级","note":""},
    {"person_id":1,"org_id":29,"title":"上海市委组织部副部长","start":"2008-11","end":"2011-11","rank":"正局级","note":"从同济大学调任"},
    {"person_id":1,"org_id":32,"title":"同济大学党委常务副书记（正局级）兼副校长","start":"2007-06","end":"2008-11","rank":"正局级","note":""},
    {"person_id":1,"org_id":32,"title":"同济大学党委副书记兼副校长","start":"2004-12","end":"2007-06","rank":"副局级","note":""},
    {"person_id":1,"org_id":32,"title":"同济大学党委副书记","start":"2002-07","end":"2004-12","rank":"副局级","note":""},
    {"person_id":1,"org_id":32,"title":"同济大学理学院党委书记兼海洋地质与地球物理系主任","start":"1998-08","end":"2002-07","rank":"","note":"2000年8月起兼任系主任；2002年7月至2004年4月兼任海洋与地球科学学院院长"},
    {"person_id":1,"org_id":32,"title":"同济大学海洋地质与地球物理系研究员、副系主任、系党总支书记","start":"1994-04","end":"1998-08","rank":"","note":"1996年1月受聘为博士生导师"},
    {"person_id":1,"org_id":32,"title":"同济大学海洋地质与地球物理系副教授、副系主任","start":"1992-1993","end":"1994-04","rank":"","note":"其间1993-1994为英国威尔士大学皇家学会访问学者"},
    {"person_id":1,"org_id":32,"title":"同济大学任教","start":"1989-10","end":"1992","rank":"","note":"获理学博士学位后留校任教"},

    # Zhao Long (赵龙) — Governor
    {"person_id":2,"org_id":2,"title":"福建省省长","start":"2022-01","end":"present","rank":"正省级","note":"2021年10月任代省长，2022年1月当选省长"},
    {"person_id":2,"org_id":2,"title":"福建省代省长","start":"2021-10","end":"2022-01","rank":"正省级","note":""},
    {"person_id":2,"org_id":12,"title":"福建省委常委、厦门市委书记","start":"2021-01","end":"2021-10","rank":"副省级","note":""},
    {"person_id":2,"org_id":2,"title":"福建省常务副省长","start":"2020-07","end":"2021-01","rank":"副省级","note":"省委常委、副省长、党组副书记"},
    {"person_id":2,"org_id":27,"title":"自然资源部副部长、党组成员","start":"2018-03","end":"2020-07","rank":"副部级","note":"第24届冬奥会工作领导小组成员（2020.02任）"},
    {"person_id":2,"org_id":26,"title":"国土资源部副部长、党组成员","start":"2016-06","end":"2018-03","rank":"副部级","note":""},
    {"person_id":2,"org_id":26,"title":"国土资源部规划司司长","start":"2015-06","end":"2016-06","rank":"正局级","note":""},
    {"person_id":2,"org_id":28,"title":"国家土地督察济南局局长、党组书记","start":"2009-12","end":"2015-06","rank":"正局级","note":"2009.03-2009.12任局长"},
    {"person_id":2,"org_id":26,"title":"国土资源部地籍管理司副司长","start":"2001-12","end":"2009-03","rank":"副局级","note":"其间：2004-2005挂职四川省广安市委常委、副市长"},
    {"person_id":2,"org_id":26,"title":"国土资源部地籍管理司登记处处长","start":"1998-12","end":"2001-12","rank":"正处级","note":""},
    {"person_id":2,"org_id":26,"title":"国土资源部地籍管理司登记处副处长（主持工作）","start":"1998-08","end":"1998-12","rank":"副处级","note":""},
    {"person_id":2,"org_id":25,"title":"国家土地管理局办公室副处级秘书、综合处副处长","start":"1997-01","end":"1998-08","rank":"副处级","note":""},
    {"person_id":2,"org_id":25,"title":"国家土地管理局科技宣教司教育处、办公室综合处科员、正科级秘书","start":"1989-07","end":"1997-01","rank":"科员-正科","note":"1989.09-1990.09辽宁省大连市土地管理局锻炼"},

    # Vice Governors
    {"person_id":3,"org_id":2,"title":"福建省常务副省长","start":"","end":"present","rank":"副省级","note":"省委常委"},
    {"person_id":4,"org_id":2,"title":"福建省副省长","start":"","end":"present","rank":"副省级","note":"省委常委"},
    {"person_id":5,"org_id":2,"title":"福建省副省长","start":"","end":"present","rank":"副省级","note":"省委常委"},
    {"person_id":6,"org_id":2,"title":"福建省副省长","start":"","end":"present","rank":"副省级","note":""},
    {"person_id":7,"org_id":2,"title":"福建省副省长","start":"","end":"present","rank":"副省级","note":""},
    {"person_id":8,"org_id":2,"title":"福建省副省长","start":"","end":"present","rank":"副省级","note":""},
    {"person_id":9,"org_id":2,"title":"福建省副省长","start":"","end":"present","rank":"副省级","note":""},
    {"person_id":10,"org_id":2,"title":"福建省人民政府党组成员","start":"","end":"present","rank":"副省级","note":""},
    {"person_id":11,"org_id":2,"title":"福建省人民政府党组成员","start":"","end":"present","rank":"副省级","note":""},
    {"person_id":12,"org_id":2,"title":"福建省人民政府秘书长","start":"","end":"present","rank":"正厅级","note":""},

    # Predecessors — 省委书记
    {"person_id":13,"org_id":1,"title":"福建省委书记","start":"2020-12","end":"2022-11","rank":"正省级","note":"接替于伟国；后调任中央宣传部部长"},
    {"person_id":14,"org_id":1,"title":"福建省委书记","start":"2017-10","end":"2020-12","rank":"正省级","note":"接替尤权；此前任福建省省长"},
    {"person_id":15,"org_id":1,"title":"福建省委书记","start":"2012-12","end":"2017-10","rank":"正省级","note":"接替孙春兰"},
    {"person_id":16,"org_id":1,"title":"福建省委书记","start":"2009-11","end":"2012-12","rank":"正省级","note":"接替卢展工"},

    # Predecessors — 省长
    {"person_id":17,"org_id":2,"title":"福建省省长","start":"2020-07","end":"2021-10","rank":"正省级","note":"接替唐登杰；后调任中央金融委员会"},
    {"person_id":18,"org_id":2,"title":"福建省省长","start":"2018-01","end":"2020-07","rank":"正省级","note":"接替于伟国"},
    {"person_id":19,"org_id":2,"title":"福建省省长","start":"2016-01","end":"2018-01","rank":"正省级","note":"接替苏树林；后升任省委书记"},

    # Other provincial leaders
    {"person_id":20,"org_id":7,"title":"福建省委常委、宣传部部长","start":"","end":"","rank":"副省级","note":""},
    {"person_id":21,"org_id":5,"title":"福建省委常委、省纪委书记","start":"","end":"","rank":"副省级","note":""},
    {"person_id":22,"org_id":1,"title":"福建省委副书记","start":"","end":"","rank":"副省级","note":""},
    {"person_id":23,"org_id":9,"title":"福建省委政法委书记","start":"","end":"","rank":"副省级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Succession chains — 省委书记
    {"person_a":1,"person_b":13,"type":"predecessor_successor","context":"周祖翼接替尹力任福建省委书记","overlap_org":"中共福建省委员会","overlap_period":"2022-11","strength":"strong","direction":"person_to_other"},
    {"person_a":13,"person_b":14,"type":"predecessor_successor","context":"尹力接替于伟国任福建省委书记","overlap_org":"中共福建省委员会","overlap_period":"2020-12","strength":"strong","direction":"person_to_other"},

    # Succession chains — 省长
    {"person_a":2,"person_b":17,"type":"predecessor_successor","context":"赵龙接替王宁任福建省省长","overlap_org":"福建省人民政府","overlap_period":"2021-10","strength":"strong","direction":"person_to_other"},

    # Party Secretary <-> Governor overlap
    {"person_a":1,"person_b":2,"type":"overlap","context":"周祖翼（省委书记）与赵龙（省长）在福建省共事","overlap_org":"中共福建省委员会","overlap_period":"2022-11至今","strength":"strong","direction":"undirected"},

    # Zhao Long -> Xiamen connection
    {"person_a":2,"person_b":12,"type":"overlap","context":"赵龙曾任厦门市委书记","overlap_org":"中共厦门市委员会","overlap_period":"2021-01至2021-10","strength":"strong","direction":"person_to_other"},

    # Zhou Zuyi -> Tongji system
    {"person_a":1,"person_b":32,"type":"overlap","context":"周祖翼在同济大学工作20余年","overlap_org":"同济大学","overlap_period":"1989-2014","strength":"strong","direction":"person_to_other"},

    # Zhao Long -> land administration system
    {"person_a":2,"person_b":25,"type":"overlap","context":"赵龙从国家土地管理局起步","overlap_org":"国家土地管理局","overlap_period":"1989-1998","strength":"strong","direction":"person_to_other"},
    {"person_a":2,"person_b":26,"type":"overlap","context":"赵龙在国土资源部工作约18年","overlap_org":"国土资源部","overlap_period":"1998-2016","strength":"strong","direction":"person_to_other"},

    # Zhou Zuyi -> Central Organization Department
    {"person_a":1,"person_b":29,"type":"overlap","context":"周祖翼在中央组织部工作约8年","overlap_org":"中央组织部","overlap_period":"2014-2022","strength":"strong","direction":"person_to_other"},
]

# =========================================================================
# SQLITE BUILD
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations(
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions(
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships(
        id INTEGER PRIMARY KEY,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for i, pos in enumerate(positions, 1):
        c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (i, pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))
    for i, rel in enumerate(relationships, 1):
        c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (i, rel["person_a"], rel["person_b"], rel["type"],
                   rel["context"], rel["overlap_org"], rel["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")

# =========================================================================
# GEXF BUILD
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = (p.get("current_post") or "")
    if "省委书记" in title or "省人大常委会主任" in title:
        return "255,50,50"
    if "省长" in title:
        return "50,100,255"
    if "省纪委书记" in title:
        return "255,165,0"
    if "副省长" in title or "常务副省长" in title:
        return "50,100,255"
    if "省委副书记" in title:
        return "50,150,255"
    return "100,100,100"

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

def is_top_leader(p):
    title = (p.get("current_post") or "")
    return "省委书记" in title or "省长" in title

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>福建省领导关系网络 — Party Secretary, Governor, provincial leadership</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('          <attvalue for="2" value="province"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> org (worked_at)
    for pos in positions:
        eid += 1
        note = esc(pos.get("note", ""))
        period = f"{pos['start']}–{pos['end']}"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{period}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> person (relationships)
    for rel in relationships:
        eid += 1
        ctx = esc(rel.get("context", ""))
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{ctx}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
