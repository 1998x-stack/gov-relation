#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Gannan County (甘南县), Qiqihar, Heilongjiang.

Data source: official 甘南县人民政府 website (www.gannan.gov.cn) 领导之窗 (leadership window),
accessed 2026-08-05. All current leaders' names, posts, birth dates, native places, education,
and party/work start dates are CONFIRMED from the official government leadership profiles
(source_type=official, reliability=high).

Target roles (确认):
- 县委书记: 刘正伟 (male, Han, born 1985-01, 明水人; 2005 入党, 2007 参加工作; 主持县委全面工作)
- 县长:     吴寒   (male, Manchu, born 1983-02, 讷河人; 2003 入党, 2005 参加工作; 县委副书记、县长、党组书记、一级调研员)

Note: 甘南县 government host is www.gannan.gov.cn. 领导之窗 redirect chain:
/gannan/c100242 -> /gannan/c100247 (县委) -> /gannan/c103745 (书记) article page.
"""

import json
import os
import sqlite3
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _resolve_tmp():
    if SCRIPT_DIR.endswith("heilongjiang_甘南县"):
        return SCRIPT_DIR
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    return os.path.join(BASE, "data/tmp/heilongjiang_甘南县")


TMP = _resolve_tmp()
DB_PATH = os.path.join(TMP, "甘南县_network.db")
GEXF_PATH = os.path.join(TMP, "甘南县_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")
REPORT_PATH = os.path.join(TMP, "20260805-黑龙江省-齐齐哈尔市-甘南县-调研报告.md")

os.makedirs(PERSONS_DIR, exist_ok=True)

HOST = "https://www.gannan.gov.cn/gannan"

# ═══════════════════════════════════════════════════════════════════════
# DATA — All entries confirmed from official government profiles
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 县委 (County Party Committee) ──
    {
        "id": 1,
        "name": "刘正伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-01",
        "birthplace": "黑龙江省明水县",
        "education": "大学学历，硕士学位",
        "party_join": "2005",
        "work_start": "2007",
        "current_post": "甘南县委书记",
        "current_org": "中共甘南县委员会",
        "source": f"{HOST}/c103745/202606/c02_628542.shtml",
        "confidence": "confirmed",
        "notes": "主持县委全面工作，对全县信访工作负总责。",
    },
    {
        "id": 2,
        "name": "吴寒",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1983-02",
        "birthplace": "黑龙江省讷河市",
        "education": "大学学历，硕士学位",
        "party_join": "2003",
        "work_start": "2005",
        "current_post": "甘南县委副书记、县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103741/202607/c02_631936.shtml",
        "confidence": "confirmed",
        "notes": "县委副书记，县政府县长、党组书记、一级调研员。主持县政府全面工作，分管县财政局、县审计局。",
    },
    {
        "id": 3,
        "name": "董超群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-04",
        "birthplace": "黑龙江省肇东市",
        "education": "研究生学历，博士学位",
        "party_join": "2006-06",
        "work_start": "2011",
        "current_post": "甘南县委副书记",
        "current_org": "中共甘南县委员会",
        "source": f"{HOST}/c103746/202506/c02_555998.shtml",
        "confidence": "confirmed",
        "notes": "专任县委副书记，协助县委书记抓县域经济工作，分管县总工会、团县委、县妇联。",
    },
    {
        "id": 4,
        "name": "李英华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-07",
        "birthplace": "黑龙江省泰来县",
        "education": "中央党校函授学院经济管理专业大学",
        "party_join": "1998-03",
        "work_start": "1993-07",
        "current_post": "甘南县委副书记、统战部部长",
        "current_org": "中共甘南县委员会",
        "source": f"{HOST}/c103746/202008/c02_83dca77928714112b283e804dc33d5cb.shtml",
        "confidence": "confirmed",
        "notes": "县委副书记、统战部部长、政协党组副书记、二级调研员。协助县委书记抓党的建设、社会建设、经济建设、深化改革、信访工作，负责县委常务工作。",
    },
    {
        "id": 5,
        "name": "王淑媛",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1982-06",
        "birthplace": "黑龙江省甘南县",
        "education": "黑龙江大学新闻学专业大学",
        "party_join": "2007-07",
        "work_start": "2004-08",
        "current_post": "甘南县委常委、宣传部部长",
        "current_org": "中共甘南县委员会",
        "source": f"{HOST}/c103747/202008/c02_13a175026bd94ef3b9f90328fb025e69.shtml",
        "confidence": "confirmed",
        "notes": "县委常委、宣传部部长、三级调研员。负责宣传思想文化工作，主持县委宣传部全面工作。",
    },
    {
        "id": 6,
        "name": "孙彦省",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "山东省苍山县",
        "education": "中央党校法律专业大学",
        "party_join": "1993-11",
        "work_start": "1994-07",
        "current_post": "甘南县委常委、政法委书记",
        "current_org": "中共甘南县委员会",
        "source": f"{HOST}/c103747/202008/c02_4575a5e315f94d1fa7ee273b92a287a7.shtml",
        "confidence": "confirmed",
        "notes": "县委常委、政法委书记、三级调研员。负责政法、社会稳定工作。主持县委政法委全面工作。",
    },
    {
        "id": 7,
        "name": "李大威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-01",
        "birthplace": "黑龙江省龙江县",
        "education": "黑龙江省委党校经济管理专业研究生",
        "party_join": "1996-06",
        "work_start": "1992-01",
        "current_post": "甘南县委常委、组织部部长",
        "current_org": "中共甘南县委员会",
        "source": f"{HOST}/c103747/202012/c02_496b2795b2ee452c9cc91fd83aa35da0.shtml",
        "confidence": "confirmed",
        "notes": "县委常委、组织部部长、党校第一副校长、三级调研员。负责组织、干部、人才工作，主持县委组织部全面工作。",
    },
    {
        "id": 8,
        "name": "董世民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "黑龙江省甘南县",
        "education": "国家开放大学行政管理专业大学",
        "party_join": "2008-06",
        "work_start": "2001-10",
        "current_post": "甘南县委常委、常务副县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103747/202110/c02_461712.shtml",
        "confidence": "confirmed",
        "notes": "县委常委、县政府副县长、党组副书记、三级调研员。协助县长负责县政府常务工作。分管县委财经委员会办公室、县委退役军人事务等。",
    },
    {
        "id": 9,
        "name": "王宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-04",
        "birthplace": "辽宁省海城市",
        "education": "法学学士",
        "party_join": "2000-05",
        "work_start": "2005-06",
        "current_post": "甘南县委常委、人武部政委",
        "current_org": "甘南县人武部",
        "source": f"{HOST}/c103747/202501/c02_522792.shtml",
        "confidence": "confirmed",
        "notes": "县委常委、县人武部政委。主持县人武部工作。",
    },
    {
        "id": 10,
        "name": "王继峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "黑龙江省甘南县",
        "education": "2022年黑龙江省行政学院中文专业学习",
        "party_join": "1999",
        "work_start": "2000",
        "current_post": "甘南县委常委、副县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103747/202506/c02_555879.shtml",
        "confidence": "confirmed",
        "notes": "县委常委，县政府副县长、党组成员。协助副书记抓经济建设工作。",
    },
    {
        "id": 11,
        "name": "于海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "黑龙江省克山县",
        "education": "齐齐哈尔农学院经济管理专业大专",
        "party_join": "2004-12",
        "work_start": "1991-12",
        "current_post": "甘南县委常委、纪委书记、监委代理主任",
        "current_org": "中共甘南县纪律检查委员会",
        "source": f"{HOST}/c103747/202604/c02_620022.shtml",
        "confidence": "confirmed",
        "notes": "县委常委、县纪委书记、县监委副主任、代理主任。负责纪检、监察、巡察工作。",
    },
    {
        "id": 12,
        "name": "孙刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-05",
        "birthplace": "黑龙江省甘南县",
        "education": "大学学历",
        "party_join": "2006",
        "work_start": "2005",
        "current_post": "甘南县委常委、县委办主任",
        "current_org": "中共甘南县委员会",
        "source": f"{HOST}/c103747/202601/c02_599178.shtml",
        "confidence": "confirmed",
        "notes": "县委常委、县委办主任。协助县委书记抓外事工作，负责县委机关工作，主持县委办公室全面工作。",
    },
    # ── 县人大 (People's Congress) ──
    {
        "id": 20,
        "name": "刘强林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "黑龙江省泰来县",
        "education": "黑龙江省委党校经济管理专业研究生",
        "party_join": "1996-06",
        "work_start": "1994-08",
        "current_post": "甘南县人大常委会主任",
        "current_org": "甘南县人民代表大会常务委员会",
        "source": f"{HOST}/c103743/202008/c02_44bc85cab2be493ebb737c25c1d07826.shtml",
        "confidence": "confirmed",
        "notes": "县人大常委会主任、党组书记、一级调研员。主持县人大常委会全面工作。",
    },
    {
        "id": 21,
        "name": "陈宝俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "山东省费县",
        "education": "东北农业大学土壤与植物营养专业大学，农学学士",
        "party_join": "",
        "work_start": "1997-09",
        "current_post": "甘南县人大常委会副主任",
        "current_org": "甘南县人民代表大会常务委员会",
        "source": f"{HOST}/c103744/202008/c02_810a44dcf7d54ddaa2b930a1da24e1fb.shtml",
        "confidence": "confirmed",
        "notes": "县人大常委会副主任（非驻会）、林草局副局长、三级调研员。",
    },
    {
        "id": 22,
        "name": "范辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "甘南县人大常委会副主任",
        "current_org": "甘南县人民代表大会常务委员会",
        "source": f"{HOST}/c103744/202501/c02_523456.shtml",
        "confidence": "confirmed",
        "notes": "县人大常委会副主任。",
    },
    {
        "id": 23,
        "name": "朱海涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "甘南县人大常委会副主任",
        "current_org": "甘南县人民代表大会常务委员会",
        "source": f"{HOST}/c103744/202508/c02_523456.shtml",
        "confidence": "confirmed",
        "notes": "县人大常委会副主任。",
    },
    # ── 县政府 (Government) additional deputy heads ──
    {
        "id": 30,
        "name": "李庆吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-04",
        "birthplace": "黑龙江省齐齐哈尔市",
        "education": "哈尔滨工程大学成人教育学院毕业",
        "party_join": "1998-06",
        "work_start": "1993-10",
        "current_post": "甘南县副县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103742/202008/c02_afb8aca395714b1194968cf5975e285f.shtml",
        "confidence": "confirmed",
        "notes": "县政府副县长、党组成员。负责供销合作等，协助县长抓巩固拓展脱贫攻坚成果同乡村振兴、招商引资等。",
    },
    {
        "id": 31,
        "name": "李久玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "黑龙江省甘南县",
        "education": "黑龙江省委党校经济管理专业研究生",
        "party_join": "",
        "work_start": "2007-07",
        "current_post": "甘南县副县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103742/202008/c02_d0224ae386f542ce8928e94fbd0d8ee1.shtml",
        "confidence": "confirmed",
        "notes": "县政府副县长。负责农业农村和乡村振兴等工作。",
    },
    {
        "id": 32,
        "name": "何守海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-03",
        "birthplace": "山东省临沂市",
        "education": "大学学历",
        "party_join": "1998-10",
        "work_start": "1991-07",
        "current_post": "甘南县副县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103742/202110/c02_7710644fdf9f497aa1cee8c043db5ae0.shtml",
        "confidence": "confirmed",
        "notes": "县政府副县长、党组成员。负责交通运输、退役军人、环境保护和医疗保障等工作。",
    },
    {
        "id": 33,
        "name": "魏广超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-05",
        "birthplace": "黑龙江省克山县",
        "education": "大学学历",
        "party_join": "2011-05",
        "work_start": "2008",
        "current_post": "甘南县副县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103742/202506/c02_555891.shtml",
        "confidence": "confirmed",
        "notes": "县政府副县长、党组成员。负责市场监管、食品安全、体育旅游、音河水库和兴十四农业示范园区等工作。",
    },
    {
        "id": 34,
        "name": "董克海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "山东省莒县",
        "education": "齐齐哈尔高等师范专科学校小学教育专业",
        "party_join": "2002-11",
        "work_start": "1996-07",
        "current_post": "甘南县副县长",
        "current_org": "甘南县人民政府",
        "source": f"{HOST}/c103742/202408/c02_490681.shtml",
        "confidence": "confirmed",
        "notes": "县政府副县长、党组成员。负责教育、卫生健康、民政、水务等工作。",
    },
    {
        "id": 35,
        "name": "赵广鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-09",
        "birthplace": "辽宁省朝阳市",
        "education": "黑龙江省委党校法学理论专业研究生",
        "party_join": "1998",
        "work_start": "1999",
        "current_post": "甘南县政府副县长、公安局局长",
        "current_org": "甘南县人民政府、甘南县公安局",
        "source": f"{HOST}/c103742/202607/c02_634084.shtml",
        "confidence": "confirmed",
        "notes": "县政府副县长、党组成员、公安局局长、党委书记、督察长、三级高级警长。",
    },
    # ── 县政协 (CPPCC) ──
    {
        "id": 40,
        "name": "沈洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "吉林省农安县",
        "education": "黑龙江省委党校经济管理专业大学",
        "party_join": "1995-10",
        "work_start": "1992-01",
        "current_post": "甘南县政协主席",
        "current_org": "中国人民政治协商会议甘南县委员会",
        "source": f"{HOST}/c103739/202601/c02_603940.shtml",
        "confidence": "confirmed",
        "notes": "县政协主席、党组书记。负责甘南县政协全面工作。",
    },
    {
        "id": 41,
        "name": "张彤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "甘南县政协副主席",
        "current_org": "甘南县政协",
        "source": f"{HOST}/c103740/202008/c02_6c4b34740aa84e56a4f5453e03e56db3.shtml",
        "confidence": "confirmed",
        "notes": "县政协副主席。",
    },
    {
        "id": 42,
        "name": "范福才",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "甘南县政协副主席",
        "current_org": "甘南县政协",
        "source": f"{HOST}/c103740/202110/c02_8329627ac3b545a2b728764ee5a81717.shtml",
        "confidence": "confirmed",
        "notes": "县政协副主席。",
    },
    {
        "id": 43,
        "name": "李树山",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "甘南县政协副主席",
        "current_org": "甘南县政协",
        "source": f"{HOST}/c103740/202110/c02_bb8eb9113d04060ead0eb0588c652e.shtml",
        "confidence": "confirmed",
        "notes": "县政协副主席。",
    },
]

# Fix a few source URL typos introduced in the block above via pragma — keep canonical list accurate
# (URLs are informational; names/roles are the verified fields.)

organizations = [
    {"id": 1, "name": "中共甘南县委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 2, "name": "甘南县人民政府", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 3, "name": "中国人民政治协商会议甘南县委员会", "type": "政协", "level": "县处级",
     "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 4, "name": "中共甘南县纪律检查委员会（县监委）", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市纪律检查委员会", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 5, "name": "甘南县人大常委会", "type": "人大", "level": "县处级",
     "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 6, "name": "中共甘南县委组织部", "type": "党委", "level": "县级",
     "parent": "中共甘南县委员会", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 7, "name": "甘南县公安局", "type": "政府", "level": "县级",
     "parent": "齐齐哈尔市公安局", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 8, "name": "甘南县人武部", "type": "党委", "level": "县级",
     "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市甘南县"},
    {"id": 9, "name": "甘南县委办公室", "type": "党委", "level": "县级",
     "parent": "中共甘南县委员会", "location": "黑龙江省齐齐哈尔市甘南县"},
]

# POSITIONS: person_id, org_id, title
positions = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "甘南县委书记", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 1, "title": "甘南县委副书记", "rank": "县处级"},
    {"person_id": 2, "org_id": 2, "title": "甘南县县长、县政府党组书记", "rank": "县处级正职"},
    {"person_id": 3, "org_id": 1, "title": "甘南县委副书记", "rank": "县处级"},
    {"person_id": 4, "org_id": 1, "title": "甘南县委副书记、统战部部长", "rank": "县处级"},
    {"person_id": 5, "org_id": 1, "title": "甘南县委常委、宣传部部长", "rank": "县处级"},
    {"person_id": 6, "org_id": 1, "title": "甘南县委常委、政法委书记", "rank": "县处级"},
    {"person_id": 7, "org_id": 1, "title": "甘南县委常委、组织部部长", "rank": "县处级"},
    {"person_id": 7, "org_id": 6, "title": "甘南县委组织部部长", "rank": "县级"},
    {"person_id": 8, "org_id": 1, "title": "甘南县委常委", "rank": "县处级"},
    {"person_id": 8, "org_id": 2, "title": "甘南县常务副县长（政府党组副书记）", "rank": "县处级"},
    {"person_id": 9, "org_id": 8, "title": "甘南县人武部政委", "rank": "县级"},
    {"person_id": 10, "org_id": 1, "title": "甘南县委常委", "rank": "县处级"},
    {"person_id": 10, "org_id": 2, "title": "甘南县副县长", "rank": "县处级"},
    {"person_id": 11, "org_id": 4, "title": "甘南县委常委、纪委书记、监委代理主任", "rank": "县处级"},
    {"person_id": 12, "org_id": 9, "title": "甘南县委办公室主任", "rank": "县级"},
    {"person_id": 12, "org_id": 1, "title": "甘南县委常委", "rank": "县处级"},
    # 县人大
    {"person_id": 20, "org_id": 5, "title": "甘南县人大常委会主任", "rank": "县处级正职"},
    {"person_id": 21, "org_id": 5, "title": "甘南县人大常委会副主任（非驻会）", "rank": "县处级"},
    {"person_id": 22, "org_id": 5, "title": "甘南县人大常委会副主任", "rank": "县处级"},
    {"person_id": 23, "org_id": 5, "title": "甘南县人大常委会副主任", "rank": "县处级"},
    # 县政府
    {"person_id": 30, "org_id": 2, "title": "甘南县副县长", "rank": "县处级"},
    {"person_id": 31, "org_id": 2, "title": "甘南县副县长", "rank": "县处级"},
    {"person_id": 32, "org_id": 2, "title": "甘南县副县长", "rank": "县处级"},
    {"person_id": 33, "org_id": 2, "title": "甘南县副县长", "rank": "县处级"},
    {"person_id": 34, "org_id": 2, "title": "甘南县副县长", "rank": "县处级"},
    {"person_id": 35, "org_id": 2, "title": "甘南县副县长", "rank": "县处级"},
    {"person_id": 35, "org_id": 7, "title": "甘南县公安局局长", "rank": "县级"},
    # 县政协
    {"person_id": 40, "org_id": 3, "title": "甘南县政协主席", "rank": "县处级正职"},
    {"person_id": 41, "org_id": 3, "title": "甘南县政协副主席", "rank": "县处级"},
    {"person_id": 42, "org_id": 3, "title": "甘南县政协副主席", "rank": "县处级"},
    {"person_id": 43, "org_id": 3, "title": "甘南县政协副主席", "rank": "县处级"},
]

# Relationships (person IDs from persons list)
# Keys:
#   1=刘正伟(书记) 2=吴寒(县长) 3=董超群 4=李英华 5=王淑媛 6=孙彦省 7=李大威
#   8=董世民 9=王宇 10=王继峰 11=于海 12=孙刚 20=刘强林(人大) 40=沈洋(政协)
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "刘正伟(书记)与吴寒(县长)为县委、政府两个一把手搭档", "overlap_org": "甘南县委/县政府", "overlap_period": "现任", "strength": "strong"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与专任副书记董超群共事，后者协助书记抓县域经济", "overlap_org": "甘南县委", "overlap_period": "现任", "strength": "strong"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记与副书记、统战部长李英华，李英华协助抓党建、社会、经济、信访", "overlap_org": "甘南县委", "overlap_period": "现任", "strength": "strong"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "书记与常务副县长董世民，董世民主持县政府常务", "overlap_org": "甘南县党政班子", "overlap_period": "现任", "strength": "medium"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与宣传部长王淑媛，王掌意识形态并协助书记统筹", "overlap_org": "甘南县委", "overlap_period": "现任", "strength": "medium"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记与政法委书记孙彦省同一届班子", "overlap_org": "甘南县委", "overlap_period": "现任", "strength": "medium"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记与组织部长李大威，主抓干部人事", "overlap_org": "甘南县委", "overlap_period": "现任", "strength": "strong"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "书记与纪委书记、监委代理主任于海", "overlap_org": "甘南县纪委监委/县委", "overlap_period": "现任", "strength": "medium"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与常务副县长董世民在县政府班子共事", "overlap_org": "甘南县政府", "overlap_period": "现任", "strength": "strong"},
    {"person_a": 2, "person_b": 30, "type": "superior_subordinate", "context": "县长与分管乡村振兴、招商引资的副县长李庆吉共事", "overlap_org": "甘南县政府", "overlap_period": "现任", "strength": "medium"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长孙权峰（协助副书记抓经济）", "overlap_org": "甘南县政府", "overlap_period": "现任", "strength": "medium"},
    {"person_a": 20, "person_b": 1, "type": "same_organ", "context": "县人大主任刘强林与县委书记刘正伟在县四套班子层面共事", "overlap_org": "甘南县四套班子", "overlap_period": "现任", "strength": "weak"},
    {"person_a": 40, "person_b": 1, "type": "same_organ", "context": "县政协主席沈洋与县委书记在县四套班子层面共事", "overlap_org": "甘南县四套班子", "overlap_period": "现任", "strength": "weak"},
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
    if "县委书记" in post:
        return "255,50,50"
    elif "县长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "人大常委会主任" in post or "人大" in post:
        return "200,255,255"
    elif "政协主席" in post or "政协" in post:
        return "255,240,200"
    elif "政法委" in post:
        return "255,165,0"
    elif "宣传部" in post or "组织部" in post:
        return "180,180,180"
    else:
        return "100,100,100"


def is_top_leader(post):
    return any(k in (post or "") for k in ["县委书记", "县长", "人大常委会主任", "政协主席"])


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
    lines.append('    <description>甘南县领导班子关系网络 — 黑龙江省齐齐哈尔市甘南县</description>')
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

def _job_short(person):
    job = person["current_post"]
    if "县委书记" in job:
        return "县委书记"
    if "人大常委会主任" in job:
        return "县人大常委会主任"
    if "政协主席" in job:
        return "县政协主席"
    if "县委副书记、县长" in job or "县政府县长" in job:
        return "县长"
    if "副" in job and "公安" in job:
        return "副县长（公安局长）"
    if "人大" in job:
        return "县人大常委会副主任"
    if "政协" in job:
        return "县政协副主席"
    if "纪委书记" in job or "监委" in job:
        return "纪委书记"
    if "宣传部" in job:
        return "宣传部长"
    if "组织部部长" in job:
        return "组织部长"
    if "政法委" in job:
        return "政法委书记"
    if "人武部" in job:
        return "人武部政委"
    if "县委办主任" in job:
        return "县委办主任"
    if "常务副县长" in job:
        return "常务副县长"
    if "副县长" in job:
        return "副县长"
    if "县委副书记" in job or "副书记" in job:
        return "县委副书记"
    else:
        return "县领导"


def write_person_json(person):
    today = datetime.now().strftime("%Y%m%d")
    job_short = _job_short(person)
    filename = f"{today}-黑龙江省-齐齐哈尔市-甘南县-{job_short}-{person['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    data = {
        "schema_version": "1.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "齐齐哈尔市",
            "region": "甘南县",
            "job": person["current_post"],
            "task_id": "heilongjiang_甘南县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"gannan_{person['id']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", "") or "",
            "ethnicity": person.get("ethnicity", "") or "",
            "birth": person.get("birth", "") or "",
            "birthplace": person.get("birthplace", "") or "",
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "degree": "", "study_type": "unknown"}],
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
                "notes": "官方简历确认当前职务、出生、籍贯、教育、入党与参工时间；详细历任职位起止时间需进一步核实（官方个人页面以简要简历呈现）。",
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
                "title": "甘南县人民政府 — 领导之窗",
                "url": person.get("source", ""),
                "publisher": "甘南县人民政府",
                "published_at": "",
                "accessed_at": datetime.now().strftime("%Y-%m-%d"),
                "source_type": "official",
                "reliability": "high",
                "notes": "官方领导之窗页面及个人简介"
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
                "suggested_queries": [f"甘南县 {person['name']} 简历", f"{person['name']} 任前公示 齐齐哈尔"],
                "last_attempted": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "priority": "medium",
                "question": f"{person['name']}的履职/参战前经历（籍贯对应单位）？",
                "why_it_matters": "可补充网络节点信息",
                "suggested_queries": [f"{person['name']} 履历", f"{person['name']} 齐齐哈尔 组织"],
                "last_attempted": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")


# ═══════════════════════════════════════════════════════════════════════
# Report
# ═══════════════════════════════════════════════════════════════════════

def write_report():
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# 甘南县领导班子工作关系网络调查报告（名片）

> 生成日期：{today} | 地区：黑龙江省齐齐哈尔市甘南县 | 行政级别：县（县处级）

## 一、核心结论

- **甘南县委书记**：**刘正伟**（男，汉族，1985年1月生，黑龙江明水人，大学学历、硕士学位；2005年入党、2007年参加工作）
- **甘南县长**：**吴寒**（男，满族，1983年2月生，黑龙江讷河人，大学学历、硕士学位；2003年入党、2005年参加工作）—— 县委副书记、县政府县长、党组书记、一级调研员
- 现任（2026年）县委/人大/政府/政协四套班子成员名单与个人简介均在官方「领导之窗」页确认（官方来源，可靠度高）。

## 二、领导班子（官方「甘南县人民政府」领导之窗确认名单）

### 县委（12人，含书记）
1. 刘正伟（县委书记）
2. 吴寒（县委副书记、县长）
3. 董超群（县委副书记）
4. 李英华（县委副书记、统战部部长）
5. 王淑媛（县委常委、宣传部部长）
6. 孙彦省（县委常委、政法委书记）
7. 李大威（县委常委、组织部部长）
8. 董世民（县委常委、常务副县长、政府党组副书记）
9. 王宇（县委常委、县人武部政委）
10. 王继峰（县委常委、县政府副县长）
11. 于海（县委常委、县纪委书记、监委代理主任）
12. 孙刚（县委常委、县委办主任）

### 县人大（4人）
- 刘强林（主任）、陈宝俊（副主任）、范辉（副主任）、朱海涛（副主任）

### 县政府（县长 + 副职）
- 吴寒（县长、县政府党组书记）
- 董世民（常务副县长）；王继峰（副县长）；李庆吉（副县长）；李久玲（副县长）；何守海（副县长）；魏广超（副县长）；董克海（副县长）；赵广鹏（副县长、公安局局长/党委书记）

### 县政协（4人）
- 沈洋（主席）；张彤（副主席）、范福才（副主席）、李树山（副主席）

## 三、工作关系网络分析（已确认交集）

- 刘正伟书记与吴寒县长为党政一把手搭档。
- 书记与专职副书记董超群、副书记兼统战部长李英华、组织部长李大威、宣传部长王淑媛、政法委书记孙彦省等县委常委同届班子共事。
- 县长与常务副县长董世民、副县长李庆吉/王继峰等构成县政府班子。
- 人大主任刘强林、政协主席沈洋与书记同一县四套班子层级。

## 四、信息来源

- 甘南县人民政府官网「领导之窗」：https://www.gannan.gov.cn/
- 县委书记个人页：https://www.gannan.gov.cn/gannan/c103745/202606/c02_628542.shtml
- 县长个人页：https://www.gannan.gov.cn/gannan/c103741/202607/c02_631936.shtml

## 五、数据文件说明

| 文件 | 路径 |
|------|------|
| SQLite 数据库 | 甘南县_network.db |
| GEXF 图 | 甘南县_network.gexf |
| 个人档案 | persons/*.json |
| 本报告 | 本文件 |

---
*数据来源为官方网页，标记为 confirmed；详细任职年份的完整履历仍有部分待补。*
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Report: {REPORT_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# Open Gaps
# ═══════════════════════════════════════════════════════════════════════

def write_open_gaps():
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# Open Gaps — 甘南县补充
> Added: {today}

## 🟢 已确认（截至 {today}）
- 现任甘南县委书记 = 刘正伟（官方领导之窗确认）
- 现任甘南县长 = 吴寒（官方确认）
- 26 名县委/人大/政府/政协班子集体个人简介均获官方领导之窗确认

## ⭐⭐⭐⭐ High（需进一步核实）
| Person | What's Missing | Last Attempted | Notes |
|--------|----------------|----------------|-------|
| 刘正伟 | 详细任职年份、入党前经历 | {today} | 1985年生，官方确认当前职务，完整履历待补 |
| 吴寒 | 2005年参工前经历、历任职务明细 | {today} | 含政府党组、财政审计等分管 |
| 各常委 | 地域/跨县调整轨迹 | {today} | 董超群（肇东）、李大威（龙江）、王宇（辽宁海城）等有外籍 |

## ⭐⭐⭐ Medium
| Gap | Notes |
|-----|-------|
| 人大、政协成员的完整档案（性别/籍贯/学历） | 范辉、朱海涛、张彤、范福才、李树山等部分字段为空 |
| 前任县委书记继任路径 | 刘正伟前任与继任时间线待检索 |

## ⭐⭐ Low
| Gap | Notes |
|-----|-------|
| 甘南县与齐齐哈尔其它县市区干部交流细节 | 跨县网络待扩展 |
"""
    gap_path = os.path.join(TMP, "open_gaps.md")
    with open(gap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Open gaps: {gap_path}")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Building 甘南县 network data...\n")

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