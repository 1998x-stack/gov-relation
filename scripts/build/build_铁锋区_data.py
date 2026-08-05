#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Tiefeng District (铁锋区), Qiqihar, Heilongjiang.

Data source: official 铁锋区人民政府 website (www.tfqzf.gov.cn) leadership window
(领导之窗 /tfq/c101762/szf.shtml) and individual leader profile pages, accessed 2026-08-05.
All 22 leadership rosters (区委/人大/政府/政协) and their biographies are CONFIRMED
from the official government site (source_type=official, reliability=high).

Note: 铁锋区 government host is www.tfqzf.gov.cn (not www.tfq.gov.cn). The Qiqihar
parent-city site (www.qqhr.gov.cn) confirmed this domain.
"""

import json
import os
import sqlite3
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _resolve_tmp():
    if SCRIPT_DIR.endswith("heilongjiang_铁锋区"):
        return SCRIPT_DIR
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    return os.path.join(BASE, "data/tmp/heilongjiang_铁锋区")


TMP = _resolve_tmp()
DB_PATH = os.path.join(TMP, "铁锋区_network.db")
GEXF_PATH = os.path.join(TMP, "铁锋区_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")
REPORT_PATH = os.path.join(TMP, "20260805-黑龙江省-齐齐哈尔市-铁锋区-调研报告.md")

os.makedirs(PERSONS_DIR, exist_ok=True)

OFFICIAL = "https://www.tfqzf.gov.cn/tfq/c101762/szf.shtml"
ROOT = "http://www.tfqzf.gov.cn/"

# ═══════════════════════════════════════════════════════════════════════
# DATA — All entries confirmed from official government profiles
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委 (District Party Committee) ──
    {
        "id": 1,
        "name": "崔亚辉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "黑龙江省依安县",
        "education": "黑龙江省委党校法律专业大学；东北农业大学农村与区域发展专业农业推广硕士",
        "party_join": "1995-06",
        "work_start": "1998-08",
        "current_post": "齐齐哈尔市铁锋区委书记",
        "current_org": "中共齐齐哈尔市铁锋区委员会",
        "source": f"{ROOT}tfq/c101763/202403/c02_458163.shtml",
        "confidence": "confirmed",
        "notes": "现任铁锋区委书记、区委党校校长。主持区委全面工作，分管区委党校。",
    },
    {
        "id": 2,
        "name": "李岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "内蒙古自治区突泉县",
        "education": "黑龙江省委党校社会管理专业研究生；工学学士",
        "party_join": "2010-03",
        "work_start": "2006-09",
        "current_post": "齐齐哈尔市铁锋区委副书记、区长",
        "current_org": "齐齐哈尔市铁锋区人民政府",
        "source": f"{ROOT}tfq/c101763/202403/c02_458166.shtml",
        "confidence": "confirmed",
        "notes": "区委副书记、区长、区政府党组书记、铁锋经济开发区管委会党工委书记、主任。主持区政府全面工作。",
    },
    {
        "id": 3,
        "name": "张慧利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-06",
        "birthplace": "吉林省长春市",
        "education": "齐齐哈尔大学计算机科学与技术；哈尔滨工程大学工商管理硕士",
        "party_join": "2003-02",
        "work_start": "2000-07",
        "current_post": "铁锋区委常委、副区长",
        "current_org": "齐齐哈尔市铁锋区人民政府",
        "source": f"{ROOT}tfq/c101763/202407/c02_483070.shtml",
        "confidence": "confirmed",
        "notes": "区委常委、副区长、区政府党组副书记、光荣街道党工委书记。协助区长抓政府常务工作。",
    },
    {
        "id": 4,
        "name": "刘艳军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "黑龙江省兰西县",
        "education": "中国人民解放军南京陆军指挥学院法律专业",
        "party_join": "1995-12",
        "work_start": "1994-12",
        "current_post": "铁锋区委常委",
        "current_org": "中共齐齐哈尔市铁锋区委员会",
        "source": f"{ROOT}/tfq/c101763/202604/c02_619433.shtml",
        "confidence": "confirmed",
        "notes": "区委常委，负责区人武部工作。",
    },
    {
        "id": 5,
        "name": "孟醒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "山东省掖县",
        "education": "中央广播电视大学法学专业",
        "party_join": "2008-07",
        "work_start": "2006-03",
        "current_post": "铁锋区委常委、政法委书记",
        "current_org": "中共齐齐哈尔市铁锋区委员会",
        "source": f"{ROOT}/tfq/c101763/202403/c02_458105.shtml",
        "confidence": "confirmed",
        "notes": "区委常委、政法委书记。主持区委政法委全面工作，协助副书记抓信访工作。",
    },
    {
        "id": 6,
        "name": "谢岩岩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "黑龙江省齐齐哈尔市",
        "education": "黑龙江省委党校公共管理研究生；齐齐哈尔大学汉语言文学学士",
        "party_join": "2000-12",
        "work_start": "2001-08",
        "current_post": "铁锋区委常委、宣传部部长",
        "current_org": "中共齐齐哈尔市铁锋区委员会",
        "source": f"{ROOT}/tfq/c103763/202403/c02_458122.shtml",
        "confidence": "confirmed",
        "notes": "区委常委、宣传部部长。",
    },
    {
        "id": 7,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "黑龙江省龙江县",
        "education": "哈尔滨工业大学计算机科学与技术；哈尔滨商业大学工商管理硕士",
        "party_join": "1996-05",
        "work_start": "1996-07",
        "current_post": "铁锋区委常委、组织部部长",
        "current_org": "中共齐齐哈尔市铁锋区委员会",
        "source": f"{ROOT}/tfq/c103763/202412/c02_519461.shtml",
        "confidence": "confirmed",
        "notes": "区委常委、组织部部长、党校第一副校长。主持区委组织部（公务员局、老干部局）全面工作。",
    },
    {
        "id": 8,
        "name": "李永顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-05",
        "birthplace": "黑龙江省讷河市",
        "education": "黑龙江省经济管理干部学院法律专业",
        "party_join": "2000-06",
        "work_start": "2001-12",
        "current_post": "铁锋区委常委、纪委书记、监委主任",
        "current_org": "中共齐齐哈尔市铁锋区纪律检查委员会",
        "source": f"{ROOT}/tfq/c103763/202305/c02_494199.shtml",
        "confidence": "confirmed",
        "notes": "区委常委、纪委书记、监委主任。主持区纪律检查委员会、区监察委员会全面工作。",
    },
    {
        "id": 9,
        "name": "陈超哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-07",
        "birthplace": "",
        "education": "哈尔滨理工大学电气工程与自动化；工学学士",
        "party_join": "2011-06",
        "work_start": "2012-07",
        "current_post": "铁锋区委常委、政府副区长（挂职）",
        "current_org": "齐齐哈尔市铁锋区人民政府",
        "source": f"{ROOT}/tfq/c103763/202503/c02_542241.shtml",
        "confidence": "confirmed",
        "notes": "区委常委、副区长（挂职），分管武装工作。",
    },
    # ── 区人大 (People's Congress) ──
    {
        "id": 10,
        "name": "郭永权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-06",
        "birthplace": "辽宁省庄河市",
        "education": "北京大学政治学专业大专",
        "party_join": "1990-11",
        "work_start": "1988-07",
        "current_post": "铁锋区人大常委会主任",
        "current_org": "铁锋区人民代表大会常务委员会",
        "source": f"{ROOT}/tfq/c101764/202204/c02_155501.shtml",
        "confidence": "confirmed",
        "notes": "人大常委会主任、党组书记。负责区人大常委会全面工作。",
    },
    {
        "id": 11,
        "name": "李凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-02",
        "birthplace": "黑龙江省克山县",
        "education": "黑龙江省委党校经济管理专业大学毕业",
        "party_join": "1993-11",
        "work_start": "1989-08",
        "current_post": "铁锋区人大常委会副主任",
        "current_org": "铁锋区人民代表大会常务委员会",
        "source": f"{ROOT}/tfq/c103764/202210/c02_155527.shtml",
        "confidence": "confirmed",
        "notes": "人大常委会副主任、党组副书记。负责人大常务、法制委员会工作。",
    },
    {
        "id": 12,
        "name": "王文元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-11",
        "birthplace": "辽宁省黑山县",
        "work_start": "1989-07",
        "education": "齐齐哈尔师范学院体育教育专业、教育学学士",
        "party_join": "",
        "current_post": "铁锋区人大常委会副主任（不驻会）",
        "current_org": "铁锋区人民代表大会常务委员会",
        "source": f"{ROOT}/tfq/c103764/202306/c02_155536.shtml",
        "confidence": "confirmed",
        "notes": "人大常委会副主任（不驻会）、区工商联主席。无党派人士。",
    },
    {
        "id": 13,
        "name": "王丽萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "辽宁省海城市",
        "education": "黑龙江大学电子政务专业",
        "party_join": "1999-04",
        "work_start": "1996-08",
        "current_post": "铁锋区人大常委会副主任",
        "current_org": "铁锋区人民代表大会常务委员会",
        "source": f"{ROOT}/tfq/c103764/202210/c02_155518.shtml",
        "confidence": "confirmed",
        "notes": "人大常委会副主任、党组成员。负责人大人事代表选举、社会建设及民族宗教等工作。",
    },
    {
        "id": 14,
        "name": "桂阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "黑龙江省齐齐哈尔市",
        "education": "中国人民解放军大连陆军学院军事指挥专业",
        "party_join": "1991-03",
        "work_start": "1989-03",
        "current_post": "铁锋区人大常委会副主任",
        "current_org": "铁锋区人民代表大会常务委员会",
        "source": f"{ROOT}/tfq/c103764/202210/c155581.shtml",
        "confidence": "confirmed",
        "notes": "人大常委会副主任、党组成员。",
    },
    # ── 区政府 (Government) additional deputy mayors ──
    {
        "id": 15,
        "name": "沈红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-04",
        "birthplace": "黑龙江省克山县",
        "education": "国家开放大学行政管理专业",
        "party_join": "2003-05",
        "work_start": "2000-08",
        "current_post": "铁锋区副区长",
        "current_org": "齐齐哈尔市铁锋区人民政府",
        "source": f"{ROOT}/tfq/c103434/202403/c02_458168.shtml",
        "confidence": "confirmed",
        "notes": "副区长、区政府党组成员。负责教育、卫生健康、文体旅游、民政等工作。",
    },
    {
        "id": 16,
        "name": "林连海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "黑龙江省齐齐哈尔市",
        "education": "齐齐哈尔广播电视大学法学专业",
        "party_join": "1999-04",
        "work_start": "1990-02",
        "current_post": "铁锋区副区长、公安分局局长",
        "current_org": "铁锋区人民政府、铁锋公安分局",
        "source": f"{ROOT}/tfq/c103434/202404/c02_466763.shtml",
        "confidence": "confirmed",
        "notes": "副区长、政府党组成员、铁锋公安分局党委书记、局长。负责公安、司法行政和法治政府建设。",
    },
    {
        "id": 17,
        "name": "孙佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "黑龙江省克山县",
        "education": "哈尔滨工程大学公共管理硕士",
        "party_join": "2012-10",
        "work_start": "2009-04",
        "current_post": "铁锋区副区长",
        "current_org": "齐齐哈尔市铁锋区人民政府",
        "source": f"{ROOT}/tfq/c103634/202409/c02_494213.shtml",
        "confidence": "confirmed",
        "notes": "副区长、区政府党组成员。负责农业农村、乡村振兴、林草水利等工作。",
    },
    {
        "id": 18,
        "name": "陈林",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1987-06",
        "birthplace": "黑龙江省齐齐哈尔市",
        "education": "齐齐哈尔大学思想政治教育专业、法学硕士",
        "party_join": "2014-05",
        "work_start": "2010-07",
        "current_post": "铁锋区副区长",
        "current_org": "齐齐哈尔市铁锋区人民政府",
        "source": f"{ROOT}/tfq/c103434/202501/c02_521537.shtml",
        "confidence": "confirmed",
        "notes": "副区长、区政府党组成员。负责经济发展、招商引资、项目工程等工作。",
    },
    # ── 区政协 (CPPCC) ──
    {
        "id": 19,
        "name": "徐振海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-08",
        "birthplace": "黑龙江省富裕县",
        "education": "黑龙江省委党校经济管理专业研究生",
        "party_join": "2003-12",
        "work_start": "1990-07",
        "current_post": "铁锋区政协主席",
        "current_org": "中国人民政治协商会议铁锋区委员会",
        "source": f"{ROOT}/tfq/c103735/202112/c02_155589.shtml",
        "confidence": "confirmed",
        "notes": "政协主席、党组书记。主持区政协党组和区政协全面工作。",
    },
    {
        "id": 20,
        "name": "王丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "辽宁省辽阳市",
        "education": "黑龙江八一农垦大学农业建筑与环境工程专业",
        "party_join": "",
        "work_start": "1993-08",
        "current_post": "铁锋区政协副主席",
        "current_org": "铁锋区政协委员会",
        "source": f"{ROOT}/tfq/c103735/202409/02_494194.shtml",
        "confidence": "confirmed",
        "notes": "区政协副主席，农工党党员。",
    },
    {
        "id": 21,
        "name": "佟琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "辽宁省昌图县",
        "education": "齐齐哈尔大学化学与化工学院精细化工专业",
        "party_join": "2001-03",
        "work_start": "1997-07",
        "current_post": "铁锋区政协副主席",
        "current_org": "铁锋区政协委员会",
        "source": f"{ROOT}/tfq/c101766/202112/1_155604.shtml",
        "confidence": "confirmed",
        "notes": "区政协副主席、党组副书记。",
    },
    {
        "id": 22,
        "name": "赵爽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-01",
        "birthplace": "黑龙江省齐齐哈尔市",
        "education": "黑龙江省委党校经济管理专业研究生",
        "party_join": "1997-06",
        "work_start": "1997-12",
        "current_post": "铁锋区政协副主席",
        "current_org": "铁锋区政协委员会",
        "source": f"{ROOT}/tfq/c102315/202409/c02_494192.shtml",
        "confidence": "confirmed",
        "notes": "区政协副主席、党组成员。",
    },
]

organizations = [
    {"id": 1, "name": "中共齐齐哈尔市铁锋区委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市铁锋区"},
    {"id": 2, "name": "齐齐哈尔市铁锋区人民政府", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市铁锋区"},
    {"id": 3, "name": "中国人民政治协商会议齐齐哈尔市铁锋区委员会", "type": "政协", "level": "县处级",
     "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市铁锋区"},
    {"id": 4, "name": "中共齐齐哈尔市铁锋区纪律检查委员会（区监委）", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市纪律检查委员会", "location": "黑龙江省齐齐哈尔市铁锋区"},
    {"id": 5, "name": "齐齐哈尔市铁锋区人大常委会", "type": "人大", "level": "县处级",
     "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市铁锋区"},
    {"id": 6, "name": "中共齐齐哈尔市铁锋区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市铁锋区委员会", "location": "黑龙江省齐齐哈尔市铁锋区"},
    {"id": 7, "name": "齐齐哈尔市铁锋区人民政府公安分局", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市公安局", "location": "黑龙江省齐齐哈尔市铁锋区"},
    {"id": 8, "name": "铁锋经济开发区管委会", "type": "开发区", "level": "县处级",
     "parent": "齐齐哈尔市铁锋区人民政府", "location": "黑龙江省齐齐哈尔市铁锋区"},
]

# POSITIONS: person_id, org_id, title
positions = [
    # 区委领导班子
    {"person_id": 1, "org_id": 1, "title": "齐齐哈尔市铁锋区委书记", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 1, "title": "铁锋区委副书记", "rank": "县处级"},
    {"person_id": 2, "org_id": 2, "title": "铁锋区区长、区政府党组书记", "rank": "县处级正职"},
    {"person_id": 3, "org_id": 1, "title": "铁锋区委常委", "rank": "县处级"},
    {"person_id": 3, "org_id": 2, "title": "铁锋区常务副区长（区政府党组副书记）", "rank": "县处级"},
    {"person_id": 4, "org_id": 1, "title": "铁锋区委常委（负责人武部）", "rank": "县处级"},
    {"person_id": 5, "org_id": 1, "title": "铁锋区委常委、政法委书记", "rank": "县处级"},
    {"person_id": 6, "org_id": 1, "title": "铁锋区委常委、宣传部部长", "rank": "县处级"},
    {"person_id": 7, "org_id": 1, "title": "铁锋区委常委、组织部部长", "rank": "县处级"},
    {"person_id": 8, "org_id": 4, "title": "铁锋区委常委、纪委书记、监委主任", "rank": "县处级"},
    {"person_id": 9, "org_id": 1, "title": "铁锋区委常委（挂职）", "rank": "县处级"},
    {"person_id": 9, "org_id": 2, "title": "铁锋区副区长（挂职）", "rank": "县处级"},
    # 区人大
    {"person_id": 10, "org_id": 5, "title": "铁锋区人大常委会主任", "rank": "县处级正职"},
    {"person_id": 11, "org_id": 5, "title": "铁锋区人大常委会副主任", "rank": "县处级"},
    {"person_id": 12, "org_id": 5, "title": "铁锋区人大常委会副主任（不驻会）", "rank": "县处级"},
    {"person_id": 13, "org_id": 5, "title": "铁锋区人大常委会副主任", "rank": "县处级"},
    {"person_id": 14, "org_id": 5, "title": "铁锋区人大常委会副主任", "rank": "县处级"},
    # 区政府
    {"person_id": 15, "org_id": 2, "title": "铁锋区副区长", "rank": "县处级"},
    {"person_id": 16, "org_id": 2, "title": "铁锋区副区长", "rank": "县处级"},
    {"person_id": 16, "org_id": 7, "title": "铁锋区公安局局长", "rank": "县处级"},
    {"person_id": 17, "org_id": 2, "title": "铁锋区副区长", "rank": "县处级"},
    {"person_id": 18, "org_id": 2, "title": "铁锋区副区长", "rank": "县处级"},
    # 区政协
    {"person_id": 19, "org_id": 3, "title": "铁锋区政协主席", "rank": "县处级正职"},
    {"person_id": 20, "org_id": 3, "title": "铁锋区政协副主席", "rank": "县处级"},
    {"person_id": 21, "org_id": 3, "title": "铁锋区政协副主席", "rank": "县处级"},
    {"person_id": 22, "org_id": 3, "title": "铁锋区政协副主席", "rank": "县处级"},
]

# Relationships between leaders (person IDs from persons list)
# 1=崔亚辉(书记) 2=李岭(区长) 3=张慧利 4=刘艳军 5=孟醒 6=谢岩岩 7=刘涛 8=李永顺 9=陈超哲
# 10=郭永权(人大主任) 11=李凯 12=王文元 13=王丽萍 14=桂阳
# 15=沈红 16=林连海 17=孙佳 18=陈林 19=徐振海(政协主席) 20=王丽 21=佟琳 22=赵爽
relationships = [
    # 区委书记 与 区委领导班子
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "崔亚辉主持区委全面工作，李岭为区委副书记、区长", "strength": "strong"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委常委、常务副区长共事", "strength": "strong"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与纪委书记同一届班子", "strength": "medium"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与宣传部长共事", "strength": "medium"},
]

# ═══════════════════════════════════════════════════════════════════════
# GEXF Build
# ═══════════════════════════════════════════════════════════════════════


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    post = post or ""
    if "区委书记" in post or "县委书记" in post:
        return "255,50,50"
    elif "区长" in post or "县长" in post or "市长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "人大常委会主任" in post or "人大" in post:
        return "200,255,255"
    elif "政协" in post:
        return "255,240,200"
    else:
        return "100,100,100"


def is_top_leader(post):
    return any(k in (post or "") for k in ["区委书记", "区长", "县长", "市人大常委会主任", "政协主席"])


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p.get("education", ""), p.get("party_join", ""),
                     p.get("work_start", ""), p.get("current_post", ""),
                     p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos.get("title", ""),
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r.get("type", ""),
                     r.get("context", ""), r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"    {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>铁锋区领导班子关系网络 — 黑龙江省齐齐哈尔市铁锋区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if is_top_leader(p.get("current_post", "")) else "12.0"
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('        <viz:shape value="disc"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="220" g="220" b="220"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(r.get("context", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# Person JSON
# ═══════════════════════════════════════════════════════════════════════


def write_person_json(person):
    today = datetime.now().strftime("%Y%m%d")
    # derive a short job for the filename (distinguish 区长 from 副区长)
    job = person["current_post"]
    if "区委书记" in job:
        job_short = "区委书记"
    elif "市长" in job:
        job_short = "市长"
    elif "政协主席" in job:
        job_short = "政协主席"
    elif job.startswith("铁锋区长") or "区长" in job and "副区长" not in job and "委副书记、区长" in job:
        job_short = "区长"
    elif "副区长" in job or "副区长" in person["notes"]:
        job_short = "副区长"
    elif "人大常委会主任" in job:
        job_short = "人大常委会主任"
    elif "人大常委会副主任" in job or "人大" in job:
        job_short = "人大常委会副主任"
    elif "政协副主席" in job:
        job_short = "政协副主席"
    elif "政法委" in job:
        job_short = "政法委书记"
    elif "宣传部" in job:
        job_short = "宣传部部长"
    elif "组织部" in job:
        job_short = "组织部部长"
    elif "纪委书记" in job:
        job_short = "纪委书记"
    else:
        job_short = "区领导"
    filename = f"{today}-黑龙江省-齐齐哈尔市-铁锋区-{job_short}-{person['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    data = {
        "schema_version": "1.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "齐齐哈尔市",
            "region": "铁锋区",
            "job": person["current_post"],
            "task_id": "heilongjiang_铁锋区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"tfq_{person['id']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", "") or "",
            "ethnicity": person.get("ethnicity", "") or "",
            "birth": person.get("birth", "") or "",
            "birthplace": person.get("birthplace", "") or "",
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "degree": "", "study_type": "party_school" }],
            "party_join": person.get("party_join", "") or "",
            "work_start": person.get("work_start", "") or "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职" if is_top_leader(person["current_post"]) else "县处级",
            "as_of": "2026-08-05",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": person.get("birthplace", ""),
                "title": person.get("education", ""),
                "notes": "根据官方简历推断，具体任职经历需进一步核实；官方已确认当前职务及出生、籍贯、教育、入党时间。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {
                "org": person.get("current_org", ""),
                "role": person["current_post"],
                "period": "current",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [person.get("notes", "")],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "铁锋区人民政府 — 领导之窗",
                "url": OFFICIAL,
                "publisher": "铁锋区人民政府",
                "published_at": "",
                "accessed_at": datetime.now().strftime("%Y-%m-%d"),
                "source_type": "official",
                "reliability": "high",
                "notes": "官方领导之窗页面及个人介绍页面"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "详细任职起止年份、native_place、入党前经历未完全核实"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{person['name']}的完整职业履历（历任职位起止时间）是什么？",
                "why_it_matters": "完整履历是分析干部交流网络的基础",
                "suggested_queries": [f"铁锋区 {person['name']} 简历", f"{person['name']} 任前公示 齐齐哈尔"],
                "last_attempted": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "priority": "medium",
                "question": f"{person['name']}的入党前经历（早年任职、籍贯对应单位）？",
                "why_it_matters": "可补充网络节点信息",
                "suggested_queries": [f"{person['name']} 履历", f"{person['name']} 齐齐哈尔 组织"],
                "last_attempted": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")
    return filepath


# ═══════════════════════════════════════════════════════════════════════
# Report
# ═══════════════════════════════════════════════════════════════════════


def write_report():
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# 铁锋区领导班子工作关系网络调查报告（画像）

> 生成日期：{today} | 地区：黑龙江省齐齐哈尔市铁锋区 | 行政级别：市辖区（县处级）

## 一、核心结论

- **铁锋区委书记**：**崔亚辉**（女，汉族，1975年9月生，黑龙江依安人）
- **铁锋区区长**：**李岭**（男，汉族，1981年11月生，黑龙江突泉人）
- **全部 22 名现领导班子成员**（区委 9 人、区人大 5 人、区政协 4 人，另有 4 名未在区委常委序列的副区长）均已在官方「领导之窗」页面确认名单与个人介绍（官方来源，可靠度高）。

## 二、领导班子（官方「领导之窗」确认名单）

### 区委（9人）
1. 崔亚辉（区委书记）
2. 李岭（区委副书记、区长）
3. 张慧利（区委常委、常务副区长、区政府党组副书记）
4. 刘艳军（区委常委，负责人武部工作）
5. 孟醒（区委常委、政法委书记）
6. 谢岩岩（区委常委、宣传部部长）
7. 刘涛（区委常委、组织部部长）
8. 李永顺（区委常委、纪委书记、监委主任）
9. 陈超哲（区委常委、副区长，挂职）

### 区人大（5人）
- 郭永权（主任）
- 李凯（副主任）、王文元（副主任，不驻会）、王丽萍（副主任）、桂阳（副主任）

### 区政府（区长 + 副区长，含与区委交叉任职）
- 李岭（区长、区政府党组书记、区经开区党工委书记/主任）
- 张慧利（常务副区长）；沈红（副区长）；林连海（副区长、公安局长）；孙佳（副区长）；陈林（副区长）；陈超哲（副区长，挂职）

### 区政协（4人）
- 徐振海（主席）
- 王丽（副主席）、佟琳（副主席）、赵爽（副主席）

> 注：本报告基于官方「领导之窗」页面结构梳理。以上均为官方网站确认的当期（2026 年中）任职。

## 三、信息来源

- 铁锋区人民政府官网「领导之窗」：{ROOT}
- 铁锋区人民政府简介：{OFFICIAL}

## 四、数据文件说明

| 文件 | 路径 |
|------|------|
| SQLite 数据库 | 铁锋区_network.db |
| GEXF 图 | 铁锋区_network.gexf |
| 个人档案 | persons/*.json |
| 本报告 | 本文件 |

---
*数据来源为官方网页，标记为 confirmed；详细任职年份的完整履历仍有部分待补。*
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Report: {REPORT_PATH}")


def write_open_gaps():
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# Open Gaps Registry — 铁锋区补充
> Added: {today}

## 🟢 已确认（截至 {today}）
- 现任铁锋区委书记 = 崔亚辉（官方领导之窗确认）
- 现任铁锋区长 = 李岭（官方确认）
- 22 名班子集体个人简介均获官方页面确认

## ⭐⭐⭐⭐ High（需要进一步核实）
| Person | What's Missing | Last Attempted | Notes |
|--------|----------------|----------------|-------|
| 崔亚辉 | 详细任职年份、入党前经历 | {today} | 官方确认当前职务，完整履历待补 |
| 李岭 | 2006年参工前经历、历任职务明细 | {today} | 含政府党组副书记、经开区书记等职责 |
| 各常委 | 地域调任轨迹、跨区交流记录 | {today} | 张慧利（吉林长春）、李永顺（讷河）等有外区（外省）籍背景 |

## ⭐⭐⭐ Medium
| Gap | Last Attempted | Notes |
|-----|----------------|-------|
| 区人大、政协成员完整份数 | {today} | 王桂元、李凯等人大数据部分与政协清单需补全交叉核对 |
| 崔亚辉前任去向（区委书记继任路径） | {today} | 前任书记与继任时间线待检索 |

## ⭐⭐ Low
| Gap | Notes |
|-----|-------|
| 铁锋区与齐齐哈尔其他辖区（龙沙、建华、富拉尔基）干部交流细节 | 跨区网络待扩展 |
"""
    gap_path = os.path.join(TMP, "open_gaps.md")
    with open(gap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Open gaps: {gap_path}")


if __name__ == "__main__":
    print("Building 铁锋区 network data...\n")

    print("[1/6] SQLite database...")
    build_db()

    print("[2/6] GEXF graph...")
    build_gexf()

    print("[3/6] Person JSON files...")
    for p in persons:
        write_person_json(p)

    print("[4/6] Open gaps registry...")
    write_open_gaps()

    print("[5/6] Investigation report...")
    write_report()

    print("\nDone. All artifacts in:", TMP)
    print(f"  DB:      {DB_PATH}")
    print(f"  GEXF:    {GEXF_PATH}")
    print(f"  Persons: {PERSONS_DIR}/")
    print(f"  Report:  {REPORT_PATH}")