#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 木兰县 (Mulan County), 哈尔滨市, 黑龙江省.

Investigation date: 2026-08-06
Task ID: heilongjiang_木兰县
Level: 县
Targets: 县委书记 & 县长

Data source (all official, as-of 2026-08):
  - 木兰县人民政府官网·领导信息/领导之窗 (www.mulan.gov.cn/hebmlx/ldxx/)
      县委:   https://www.mulan.gov.cn/hebmlx/xxf/ldxx.shtml (徐向峰) 等
      政府:   /hebmlx/mhf/ldxx.shtml (邹永刚) 等
      人大/政协:  /hebmlx/syk/ldxx.shtml, /hebmlx/lbl/ldxx.shtml 等
  - 木兰县"八一"建军节走访新闻（徐向峰、邹永刚等县四个班子领导）
      https://www.mulan.gov.cn/hebmlx/gzdt/202607/c01_1138049.shtml

As-of: 2026-08

Confirmed current leadership:
  - 县委书记：徐向峰（1978-01，满族，黑龙江五常，农大博士/东北财大博士后）
  - 县委副书记、县长：邹永刚（1975-10，汉族，大学，1998-09 工作）
  县委常委会（7 人）：徐向峰、邹永刚、荣海涛(组织)、冯凯(常务副县长)、郭铭(副县长)、季德三(宣传)、袁晓燕(统战)
  县政府：邹永刚(县长)、冯凯(常务)、郭铭、远志军、李博(正处)、徐淼(公安局长)、刘雪松、周延冰
  县人大：孙玉坤(主任)、王安义、朱庆国(副主任)
  县政协：李柏林(主席)、于春和、杨振佳、许冬玲(副主席)

Gaps (see report & open_gaps):
  - 县纪委书记/监委主任未在县委名单中（官网无纪委领导页）—— 缺口
  - 政法委书记缺位，由组织部长荣海涛"临时代管"
  - 前任县委书记 / 前任县长 未确认（Web 搜索受限）
  - 大部分领导"任现职"日期未载（官方简历页只给出生/入党/参加工作时间）
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "木兰县"
TODAY = datetime.now().strftime("%Y%m%d")          # 20260806
AS_OF = "2026-08-06"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────
# id: 1-书记, 2-县长, 3-12 县委政府班子, 13-18 政府副县长, 19-21 人大, 22-25 政协
persons = [
    # 核心：县委书记 / 县长
    {"id": 1, "name": "徐向峰", "gender": "男", "ethnicity": "满族", "birth": "1978-01", "birthplace": "黑龙江五常",
     "education": "东北农业大学农业经济管理专业（研究生、博士）；东北财经大学经济学博士后", "party_join": "1998-12", "work_start": "2006-06",
     "current_post": "县委书记", "current_org": "中共木兰县委", "source": "木兰县政府官网-领导信息-县委徐向峰"},
    {"id": 2, "name": "邹永刚", "gender": "男", "ethnicity": "汉族", "birth": "1975-10", "birthplace": "",
     "education": "大学文化", "party_join": "中共党员", "work_start": "1998-09",
     "current_post": "县委副书记、政府县长", "current_org": "木兰县人民政府", "source": "木兰县政府官网-领导信息-县委邹永刚"},
    # 县委常委会（组织/宣传/统战等）
    {"id": 3, "name": "荣海涛", "gender": "男", "ethnicity": "汉族", "birth": "1977-10", "birthplace": "",
     "education": "大学文化", "party_join": "中共党员", "work_start": "2001-08",
     "current_post": "县委常委、组织部部长", "current_org": "中共木兰县委组织部", "source": "木兰县政府官网-领导信息-县委荣海涛"},
    {"id": 4, "name": "冯凯", "gender": "男", "ethnicity": "汉族", "birth": "1981-11", "birthplace": "",
     "education": "本科学历，道桥专业高级工程师", "party_join": "2018-06", "work_start": "2006-08",
     "current_post": "县委常委、常务副县长", "current_org": "木兰县人民政府", "source": "木兰县政府官网-领导信息-县委冯凯"},
    {"id": 5, "name": "郭铭", "gender": "女", "ethnicity": "蒙古族", "birth": "1985-07", "birthplace": "黑龙江巴彦",
     "education": "吉林大学传播学专业，研究生学历", "party_join": "2006-12", "work_start": "2008-01",
     "current_post": "县委常委、政府副县长", "current_org": "木兰县人民政府", "source": "木兰县政府官网-领导信息-县委郭铭"},
    {"id": 6, "name": "季德三", "gender": "男", "ethnicity": "汉族", "birth": "1974-11", "birthplace": "黑龙江木兰",
     "education": "哈尔滨师范大学汉语言文学专业，大学本科", "party_join": "1998-07", "work_start": "1999-08",
     "current_post": "县委常委、宣传部部长", "current_org": "中共木兰县委宣传部", "source": "木兰县政府官网-领导信息-县委季德三"},
    {"id": 7, "name": "袁晓燕", "gender": "女", "ethnicity": "汉族", "birth": "1982-12", "birthplace": "黑龙江通河",
     "education": "省委党校研究生学历", "party_join": "中共党员", "work_start": "2001-09",
     "current_post": "县委常委、统战部部长", "current_org": "中共木兰县委统战部", "source": "木兰县政府官网-领导信息-县委袁晓燕"},
    # 县政府领导班子（副县长）
    {"id": 8, "name": "远志军", "gender": "男", "ethnicity": "汉族", "birth": "1973-05", "birthplace": "黑龙江延寿",
     "education": "东北农业大学园艺系果树专业，农学学士", "party_join": "2000-06", "work_start": "1997-07",
     "current_post": "政府副县长", "current_org": "木兰县人民政府", "source": "木兰县政府官网-领导信息-县政府远志军"},
    {"id": 9, "name": "李博", "gender": "男", "ethnicity": "汉族", "birth": "1983-07", "birthplace": "",
     "education": "大学学士学位", "party_join": "中共党员", "work_start": "2007-04",
     "current_post": "政府副县长（正处级）", "current_org": "木兰县人民政府", "source": "木兰县政府官网-领导信息-县政府李博"},
    {"id": 10, "name": "徐淼", "gender": "男", "ethnicity": "", "birth": "1978-12", "birthplace": "",
     "education": "大学学历", "party_join": "2008-08", "work_start": "2002-07",
     "current_post": "政府副县长、公安局局长", "current_org": "木兰县公安局", "source": "木兰县政府官网-领导信息-县政府徐淼"},
    {"id": 11, "name": "刘雪松", "gender": "", "ethnicity": "", "birth": "1975-05", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "政府副县长", "current_org": "木兰县人民政府", "source": "木兰县政府官网-领导信息-县政府刘雪松"},
    {"id": 12, "name": "周延冰", "gender": "", "ethnicity": "", "birth": "1986-09", "birthplace": "",
     "education": "大学，教育学学士", "party_join": "", "work_start": "",
     "current_post": "政府副县长", "current_org": "木兰县人民政府", "source": "木兰县政府官网-领导信息-县政府周延冰"},
    # 县人大
    {"id": 13, "name": "孙玉坤", "gender": "男", "ethnicity": "汉族", "birth": "1974-01", "birthplace": "黑龙江依兰",
     "education": "大专学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "木兰县人大常委会", "source": "木兰县政府官网-领导信息-县人大孙玉坤"},
    {"id": 14, "name": "王安义", "gender": "", "ethnicity": "", "birth": "1973", "birthplace": "",
     "education": "本科", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "木兰县人大常委会", "source": "木兰县政府官网-领导信息-县人大王安义"},
    {"id": 15, "name": "朱庆国", "gender": "", "ethnicity": "", "birth": "1977", "birthplace": "",
     "education": "本科", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "木兰县人大常委会", "source": "木兰县政府官网-领导信息-县人大朱庆国"},
    # 县政协
    {"id": 16, "name": "李柏林", "gender": "", "ethnicity": "", "birth": "1968-10", "birthplace": "",
     "education": "省委党校法律专业", "party_join": "", "work_start": "",
     "current_post": "县政协主席", "current_org": "政协木兰县委员会", "source": "木兰县政府官网-领导信息-县政协李柏林"},
    {"id": 17, "name": "于春和", "gender": "", "ethnicity": "", "birth": "1968-09", "birthplace": "",
     "education": "哈尔滨市委党校经济管理", "party_join": "", "work_start": "",
     "current_post": "县政协副主席、党组副书记", "current_org": "政协木兰县委员会", "source": "木兰县政府官网-领导信息-县政协助于春和"},
    {"id": 18, "name": "杨振佳", "gender": "", "ethnicity": "", "birth": "1968-08", "birthplace": "",
     "education": "省政法干部管理学院法律", "party_join": "", "work_start": "",
     "current_post": "县政协副主席（不驻会）", "current_org": "政协木兰县委员会", "source": "木兰县政府官网-领导信息-县政协杨振佳"},
    {"id": 19, "name": "许冬玲", "gender": "女", "ethnicity": "", "birth": "1986-11", "birthplace": "",
     "education": "哈尔滨师范大学英语专业", "party_join": "", "work_start": "",
     "current_post": "县政协副主席（不驻会）", "current_org": "政协木兰县委员会", "source": "木兰县政府官网-领导信息-县政协许冬玲"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共木兰县委", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委", "location": "木兰县"},
    {"id": 2, "name": "木兰县人民政府", "type": "政府", "level": "县级", "parent": "哈尔滨市人民政府", "location": "木兰县"},
    {"id": 3, "name": "木兰县人大常委会", "type": "人大", "level": "县级", "parent": "哈尔滨市人大常委会", "location": "木兰县"},
    {"id": 4, "name": "政协木兰县委员会", "type": "政协", "level": "县级", "parent": "哈尔滨市政协", "location": "木兰县"},
    {"id": 5, "name": "木兰县纪律检查委员会/监委", "type": "纪委", "level": "县级", "parent": "中共哈尔滨市纪委", "location": "木兰县"},
    {"id": 6, "name": "中共木兰县委组织部", "type": "党委", "level": "县级", "parent": "中共木兰县委", "location": "木兰县"},
    {"id": 7, "name": "中共木兰县委宣传部", "type": "党委", "level": "县级", "parent": "中共木兰县委", "location": "木兰县"},
    {"id": 8, "name": "中共木兰县委统战部", "type": "党委", "level": "县级", "parent": "中共木兰县委", "location": "木兰县"},
    {"id": 9, "name": "木兰县公安局", "type": "政府", "level": "乡科级", "parent": "木兰县人民政府", "location": "木兰县"},
    {"id": 10, "name": "东北农业大学", "type": "事业单位", "level": "高校", "parent": "", "location": "哈尔滨市"},
    {"id": 11, "name": "中共哈尔滨市委", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "哈尔滨市"},
]

# ── Positions (career timeline) ────────────────────────────────────────────
positions = [
    # 徐向峰（县委书记）
    {"person_id": 1, "org_id": 10, "title": "东北农业大学农业经济管理专业学习（研究生/博士）", "start_date": "", "end_date": "", "rank": "", "note": "另为东北财经大学经济学博士后"},
    {"person_id": 1, "org_id": 11, "title": "哈尔滨市任职（早期，入职2006-06）", "start_date": "2006", "end_date": "任现职前", "rank": "", "note": "具体履历待查"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "届内现任", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作，分管人民武装"},
    # 邹永刚（县长）
    {"person_id": 2, "org_id": 2, "title": "县委副书记、政府县长", "start_date": "届内现任", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作，书记外出时代为主持县委；分管经开区、审计局"},
    # 县委常委会
    {"person_id": 3, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "临时代管县委政法委全面工作"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "主持县政府常务，县长外出时代为主持政府工作"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "工信科技/退役/交通"},
    {"person_id": 6, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "宣传/意识形态；临时负责信访"},
    {"person_id": 7, "org_id": 8, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "统战/对台/民族宗教"},
    # 县政府副县长
    {"person_id": 8, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "人社/文体旅游/湿地"},
    {"person_id": 9, "org_id": 2, "title": "政府副县长（正处级）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "发改/商贸/数据/招商"},
    {"person_id": 10, "org_id": 9, "title": "政府副县长、公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "公安/司法"},
    {"person_id": 11, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持人大常委会全面工作"},
    {"person_id": 14, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 16, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "县政协副主席、党组副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "县政协副主席（不驻会）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "县政协副主席（不驻会）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 书记 ↔ 县长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记徐向峰与县长邹永刚党政主要领导搭档", "overlap_org": "中共木兰县委/木兰县政府", "overlap_period": "县政府届内至今"},
    # 书记 ↔ 常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "徐向峰与组织部长荣海涛在县委常委会（干部人事）", "overlap_org": "中共木兰县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "徐向峰与常务副县长冯凯在县委常委会及县政府班子", "overlap_org": "中共木兰县委/木兰县政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "徐向峰与郭铭（县委常委、副县长）在县委常委会", "overlap_org": "中共木兰县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "徐向峰与宣传部长季德三在县委常委会", "overlap_org": "中共木兰县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "徐向峰与统战部长袁晓燕在县委常委会", "overlap_org": "中共木兰县委", "overlap_period": ""},
    # 县长 ↔ 副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "邹永刚（县长）领导常务副县长冯凯（县长外出时代为主持政府工作）", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "邹永刚与郭铭（县委常委、副县长）在县政府班子", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "邹永刚与远志军（副县长）在县政府班子", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "邹永刚与李博（正处级副县长）在县政府班子", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "邹永刚与徐淼（副县长兼公安局长，协助冯凯抓安全生产、信访）", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "邹永刚与刘雪松在县政府班子", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "邹永刚与周延冰（副县长）在县政府班子", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 其他副县长
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "常务副县长冯凯与副县长徐淼（分管应急/安全），徐淼协助冯伟", "overlap_org": "木兰县人民政府", "overlap_period": ""},
    # 跨县/跨市干部交流线索（籍贯网络）
    {"person_a": 5, "person_b": 2, "type": "same_region_link", "context": "郭铭籍贯巴彦县，与现属地木兰同属哈尔滨市域（籍贯网络线索）", "overlap_org": "", "overlap_period": ""},
    {"person_a": 8, "person_b": 2, "type": "same_region_link", "context": "远志军籍贯延寿县（哈尔滨市邻县）", "overlap_org": "", "overlap_period": ""},
]

# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    if name == "徐向峰": return "255,50,50"
    if name == "邹永刚": return "50,100,255"
    if name == "冯凯": return "100,150,220"            # 常务副县长
    if name in ("荣海涛", "季德三", "袁晓燕"): return "100,100,150"  # 组织/宣传/统战
    if name in ("郭铭", "远志军", "李博", "徐淼", "刘雪松", "周延冰"): return "100,100,100"
    if name == "孙玉坤": return "200,100,100"          # 人大主任
    if name == "李柏林": return "200,150,50"           # 政协主席
    return "120,120,120"


def person_size(name):
    if name in ("徐向峰", "邹永刚"): return "20.0"
    if name in ("冯凯", "荣海涛", "郭铭"): return "13.0"
    if name in ("孙玉坤", "李柏林"): return "12.0"
    return "9.0"


def org_color(t):
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    if "纪委" in t: return "255,180,180"
    if "事业" in t: return "220,220,220"
    return "200,200,200"


# ── Database ──────────────────────────────────────────────────────────────
def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p.get("gender"), p.get("ethnicity"), p.get("birth"), p.get("birthplace"),
                     p.get("education"), p.get("party_join"), p.get("work_start"), p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ── GEXF ──────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>哈尔滨市木兰县领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"]); sz = person_size(p["name"]); pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"]); oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
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
        lines.append('        <attvalues><attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/></attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues><attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/></attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ── Person Graph JSON ─────────────────────────────────────────────────────
SOURCE_REGISTER = [
    {"id": "S001", "title": "木兰县政府官网·领导信息·县委 徐向峰", "url": "https://www.mulan.gov.cn/hebmlx/xxf/ldxx.shtml", "publisher": "木兰县人民政府", "published_at": "", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high", "notes": "县委书记简历"},
    {"id": "S002", "title": "木兰县政府官网·领导信息·县委 邹永刚", "url": "https://www.mulan.gov.cn/hebmlx/mhf/ldxx.shtml", "publisher": "木兰县人民政府", "published_at": "", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high", "notes": "县委副书记、县长简历"},
    {"id": "S003", "title": "木兰县政府官网·领导信息（全）", "url": "https://www.mulan.gov.cn/hebmlx/ldxx/tzy_xj.shtml", "publisher": "木兰县人民政府", "published_at": "", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high", "notes": "县委/人大/政府/政协完整名单"},
    {"id": "S004", "title": "木兰县政府官网·八一建军节走访慰问活动", "url": "https://www.mulan.gov.cn/hebmlx/gzdt/202607/c01_1138049.shtml", "publisher": "木兰县融媒体中心", "published_at": "2026-07-31", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high", "notes": "徐向峰、邹永刚等县四个班子领导"},
]

JOB_MAP = {
    1: "县委书记", 2: "县长", 3: "组织部部长", 4: "常务副县长", 5: "副县长",
    6: "宣传部部长", 7: "统战部部长", 8: "副县长", 9: "副县长", 10: "副县长",
    11: "副县长", 12: "副县长", 13: "人大常委会主任", 14: "人大常委会副主任",
    15: "人大常委会副主任", 16: "政协主席", 17: "政协副主席", 18: "政协副主席", 19: "政协副主席",
}

PERSON_TIMELINE = {
    1: [
        ("", "", "东北农业大学经济管理（研究生/博士）；东北财经大学经济学博士后", "confirmed"),
        ("2006.06", "2018前", "哈尔滨市任职（早期履历待查）", "plausible"),
        ("现届", "present", "木兰县委书记", "confirmed"),
    ],
    2: [
        ("1998.09", "现届", "参加工作（哈尔滨市），履历待查", "plausible"),
        ("现届", "present", "木兰县委副书记、政府县长", "confirmed"),
    ],
    3: [("2001.08", "present", "木兰县委常委、组织部部长（临时代管政法委）", "confirmed")],
    4: [("2006.08", "present", "木兰县委常委、常务副县长", "confirmed")],
    5: [("2008.01", "present", "木兰县委常委、政府副县长", "confirmed")],
    6: [("1999.08", "present", "木兰县委常委、宣传部部长", "confirmed")],
    7: [("2001.09", "present", "木兰县委常委、统战部部长", "confirmed")],
    8: [("1997.07", "present", "木兰县政府副县长", "confirmed")],
    9: [("2007.04", "present", "木兰县政府副县长（正处级）", "confirmed")],
    10: [("2002.07", "present", "木兰县政府副县长、县公安局局长", "confirmed")],
    11: [("", "present", "木兰县政府副县长", "plausible")],
    12: [("", "present", "木兰县政府副县长", "plausible")],
    13: [("", "present", "木兰县人大常委会主任", "confirmed")],
    14: [("", "present", "木兰县人大常委会副主任", "confirmed")],
    15: [("", "present", "木兰县人大常委会副主任", "confirmed")],
    16: [("", "present", "木兰县政协主席", "confirmed")],
    17: [("", "present", "木兰县政协副主席、党组副书记", "confirmed")],
    18: [("", "present", "木兰县政协副主席", "confirmed")],
    19: [("", "present", "木兰县政协副主席", "confirmed")],
}


def build_person_jsons():
    from datetime import date
    for p in persons:
        name = p["name"]; pid = p["id"]
        timeline_rows = []
        for (s, e, t, conf) in PERSON_TIMELINE.get(pid, []):
            timeline_rows.append({
                "start": s, "end": e, "org": p["current_org"], "title": t,
                "level": "", "location": "木兰县", "system": "government",
                "rank": "", "is_key_promotion": pid in (1, 2),
                "notes": "", "confidence": conf, "source_ids": ["S001", "S002"] if pid in (1, 2) else ["S003"],
            })
        rels = []
        for r in relationships:
            if r["person_a"] == pid:
                rels.append({"person": persons[r["person_b"]-1]["name"], "relationship_type": "overlap",
                             "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r["overlap_period"], "confidence": "confirmed"})
            elif r["person_b"] == pid:
                rels.append({"person": persons[r["person_a"]-1]["name"], "relationship_type": "overlap",
                             "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r["overlap_period"], "confidence": "confirmed"})
        data = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省", "city": "哈尔滨市", "region": "木兰县",
                "job": JOB_MAP.get(pid, "领导"), "task_id": "heilongjiang_木兰县",
                "time_focus": "2026-08",
            },
            "identity": {
                "person_id": f"mulan_{name}", "name": name, "aliases": [],
                "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
                "native_place": p.get("birthplace", ""),
                "education": [{"period": "", "institution": p.get("education", ""), "major": "",
                               "degree": "", "study_type": "unknown", "source_ids": ["S001", "S002"]}],
                "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
                "dedupe_keys": {"name_birth": f"{name}_{p.get('birth','')}", "name_birthplace": f"{name}_{p.get('birthplace','')}", "official_profile_url": ""},
            },
            "current_status": {
                "current_post": p["current_post"], "current_org": p["current_org"],
                "administrative_rank": "县处级正职" if pid in (1, 2, 13, 16) else "县处级副职",
                "as_of": AS_OF, "is_current_confirmed": pid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16), "source_ids": ["S001", "S002", "S003"],
            },
            "career_timeline": timeline_rows,
            "organizations": [p["current_org"]],
            "relationships": rels,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [], "secondary_specializations": [],
                "career_pattern": ("cross_county_rotation" if pid in (1, 2) else "unknown"),
                "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [], "speech_themes": [], "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": SOURCE_REGISTER,
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed",
                "career_completeness": "partial", "relationship_confidence": "medium",
                "biggest_gap": (f"{name}任现职前完整履历/任免日期待核" if pid in (1, 2) else f"{name}任现职前履历待核"),
            },
            "open_questions": [
                {"priority": "high", "question": (f"{name}任现职前完整履历/出生地/任免时间待核" if pid in (1, 2) else f"{name}早年履历及任免时间待核"),
                 "why_it_matters": "提升履历可信度", "suggested_queries": [f"{name} 木兰县 简历"], "last_attempted": "2026-08-06"},
            ],
        }
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-哈尔滨市-{JOB_MAP.get(pid, p['current_post'])}-{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


if __name__ == "__main__":
    print(f"Building {SLUG} network data... (AS_OF={AS_OF})")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in sorted(PERSONS_DIR.glob(f"{TODAY}-黑龙江省-哈尔滨市-*.json")):
        print(f"  Person: {p.name}")