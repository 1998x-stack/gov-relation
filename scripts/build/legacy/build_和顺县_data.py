#!/usr/bin/env python3
"""Build 和顺县 (Heshun County) personnel network database + GEXF graph.

Targets: 县委书记 (李雪), 县长 (马新)
Data sources:
- 和顺县政府官网领导之窗 (https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/)
  -- 县委领导: https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/hsxwld
  -- 政府领导: https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/hszfld
  -- 人大领导: https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/hsrdld
  -- 政协领导: https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/hszxld
- 李雪个人页面: https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/hsxwld/content_67113
- 马新个人页面: https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/hsxwld/content_85487
"""

import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'shanxi_和顺县':
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

DB_PATH = os.path.join(PROJECT_ROOT, "data/database/和顺县_network.db")
GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/和顺县_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# ========== OFFICIAL SOURCE URLS ==========
OFFICIAL_LDZC = "https://www.heshun.gov.cn/zwgk/fdzdgknr/ldzc/"
URL_XWLD = OFFICIAL_LDZC + "hsxwld"
URL_ZFLD = OFFICIAL_LDZC + "hszfld"
URL_RDLD = OFFICIAL_LDZC + "hsrdld"
URL_ZXLD = OFFICIAL_LDZC + "hszxld"
URL_LIXUE = URL_XWLD + "/content_67113"
URL_MAXIN = URL_XWLD + "/content_85487"

# ========== DATA ==========

persons = [
    # === Core Leaders: 县委书记 & 县长 ===
    {"id": "heshun_li_xue", "name": "李雪", "gender": "女", "ethnicity": "汉族",
     "birth": "1975年1月", "birthplace": "山西省平定县",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共和顺县委员会",
     "source": URL_LIXUE},
    {"id": "heshun_ma_xin", "name": "马新", "gender": "男", "ethnicity": "汉族",
     "birth": "1984年5月", "birthplace": "山西省左权县",
     "education": "研究生学历",
     "party_join": "2008年11月", "work_start": "2006年7月",
     "current_post": "县委副书记、县长", "current_org": "和顺县人民政府",
     "source": URL_MAXIN},
    # === 县委常委 ===
    {"id": "heshun_dong_guohua", "name": "董国华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、统战部部长", "current_org": "中共和顺县委员会",
     "source": URL_XWLD},
    {"id": "heshun_zhang_chi", "name": "张弛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县政府常务副县长，政府党组副书记", "current_org": "和顺县人民政府",
     "source": URL_XWLD},
    {"id": "heshun_li_xinxing", "name": "李新兴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长、党校校长", "current_org": "中共和顺县委组织部",
     "source": URL_XWLD},
    {"id": "heshun_tian_jinbin", "name": "田锦斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县纪委书记", "current_org": "中共和顺县纪律检查委员会",
     "source": URL_XWLD},
    {"id": "heshun_zhao_haifeng", "name": "赵海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共和顺县委政法委员会",
     "source": URL_XWLD},
    {"id": "heshun_bai_shibin", "name": "白世斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共和顺县委宣传部",
     "source": URL_XWLD},
    {"id": "heshun_zhao_yao", "name": "赵垚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、人武部上校政治委员", "current_org": "和顺县人民武装部",
     "source": URL_XWLD},
    {"id": "heshun_zhao_wentao", "name": "赵文涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政府副县长（挂职）", "current_org": "和顺县人民政府",
     "source": URL_XWLD},
    # === 县政府领导 ===
    {"id": "heshun_chang_shouyi", "name": "常守义", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "和顺县人民政府",
     "source": URL_ZFLD},
    {"id": "heshun_han_yongkui", "name": "韩永魁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "和顺县人民政府",
     "source": URL_ZFLD},
    {"id": "heshun_zhang_haihai", "name": "张志海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、公安局局长", "current_org": "和顺县公安局",
     "source": URL_ZFLD},
    {"id": "heshun_du_zisong", "name": "杜紫颂", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "和顺县人民政府",
     "source": URL_ZFLD},
    # === 人大领导 ===
    {"id": "heshun_yuan_ruijun", "name": "袁瑞军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "和顺县人大常委会",
     "source": URL_RDLD},
    {"id": "heshun_hou_jianzhong", "name": "侯建忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "和顺县人大常委会",
     "source": URL_RDLD},
    {"id": "heshun_liang_jianhong", "name": "梁建宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任、县总工会主席", "current_org": "和顺县人大常委会",
     "source": URL_RDLD},
    {"id": "heshun_zhang_zhijian", "name": "张志坚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组成员", "current_org": "和顺县人大常委会",
     "source": URL_RDLD},
    {"id": "heshun_guo_qing", "name": "郭庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "和顺县人大常委会",
     "source": URL_RDLD},
    {"id": "heshun_lv_zhipeng", "name": "吕志鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "和顺县人大常委会",
     "source": URL_RDLD},
    # === 政协领导 ===
    {"id": "heshun_yi_junjie", "name": "易俊杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组书记", "current_org": "政协和顺县委员会",
     "source": URL_ZXLD},
    {"id": "heshun_li_ming", "name": "李明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席", "current_org": "政协和顺县委员会",
     "source": URL_ZXLD},
    {"id": "heshun_wang_fumei", "name": "王富梅", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协副主席", "current_org": "政协和顺县委员会",
     "source": URL_ZXLD},
    {"id": "heshun_hao_zhigang", "name": "郝志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协一级调研员", "current_org": "政协和顺县委员会",
     "source": URL_ZXLD},
]

organizations = [
    {"id": "heshun_party_committee", "name": "中共和顺县委员会", "type": "party", "level": "county", "parent": "晋中市委", "location": "山西省晋中市和顺县"},
    {"id": "heshun_gov", "name": "和顺县人民政府", "type": "government", "level": "county", "parent": "晋中市政府", "location": "山西省晋中市和顺县"},
    {"id": "heshun_discipline", "name": "中共和顺县纪律检查委员会", "type": "discipline", "level": "county", "parent": "晋中市纪委监委", "location": "山西省晋中市和顺县"},
    {"id": "heshun_org_dept", "name": "中共和顺县委组织部", "type": "party_dept", "level": "county", "parent": "和顺县委", "location": "山西省晋中市和顺县"},
    {"id": "heshun_propaganda_dept", "name": "中共和顺县委宣传部", "type": "party_dept", "level": "county", "parent": "和顺县委", "location": "山西省晋中市和顺县"},
    {"id": "heshun_uf_dept", "name": "中共和顺县委统战部", "type": "party_dept", "level": "county", "parent": "和顺县委", "location": "山西省晋中市和顺县"},
    {"id": "heshun_political_legal", "name": "中共和顺县委政法委员会", "type": "party_dept", "level": "county", "parent": "和顺县委", "location": "山西省晋中市和顺县"},
    {"id": "heshun_public_security", "name": "和顺县公安局", "type": "government", "level": "county", "parent": "和顺县政府", "location": "山西省晋中市和顺县"},
    {"id": "heshun_military_dept", "name": "和顺县人民武装部", "type": "government", "level": "county", "parent": "晋中军分区", "location": "山西省晋中市和顺县"},
    {"id": "heshun_congress", "name": "和顺县人大常委会", "type": "congress", "level": "county", "parent": "和顺县", "location": "山西省晋中市和顺县"},
    {"id": "heshun_cppcc", "name": "政协和顺县委员会", "type": "cppcc", "level": "county", "parent": "和顺县", "location": "山西省晋中市和顺县"},
]

positions = [
    # === 李雪 ===
    {"person_id": "heshun_li_xue", "org_id": "heshun_party_committee", "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    # === 马新 ===
    {"person_id": "heshun_ma_xin", "org_id": "heshun_party_committee", "title": "县委副书记", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    {"person_id": "heshun_ma_xin", "org_id": "heshun_gov", "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    # === 董国华 ===
    {"person_id": "heshun_dong_guohua", "org_id": "heshun_party_committee", "title": "县委副书记、统战部部长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_dong_guohua", "org_id": "heshun_uf_dept", "title": "统战部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # === 张弛 ===
    {"person_id": "heshun_zhang_chi", "org_id": "heshun_party_committee", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_zhang_chi", "org_id": "heshun_gov", "title": "常务副县长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 李新兴 ===
    {"person_id": "heshun_li_xinxing", "org_id": "heshun_party_committee", "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_li_xinxing", "org_id": "heshun_org_dept", "title": "组织部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # === 田锦斌 ===
    {"person_id": "heshun_tian_jinbin", "org_id": "heshun_party_committee", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_tian_jinbin", "org_id": "heshun_discipline", "title": "县纪委书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    # === 赵海峰 ===
    {"person_id": "heshun_zhao_haifeng", "org_id": "heshun_party_committee", "title": "县委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_zhao_haifeng", "org_id": "heshun_political_legal", "title": "政法委书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    # === 白世斌 ===
    {"person_id": "heshun_bai_shibin", "org_id": "heshun_party_committee", "title": "县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_bai_shibin", "org_id": "heshun_propaganda_dept", "title": "宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # === 赵垚 ===
    {"person_id": "heshun_zhao_yao", "org_id": "heshun_party_committee", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_zhao_yao", "org_id": "heshun_military_dept", "title": "人武部政治委员", "start": "", "end": "", "rank": "上校", "note": ""},
    # === 赵文涛 ===
    {"person_id": "heshun_zhao_wentao", "org_id": "heshun_party_committee", "title": "县委常委（挂职）", "start": "", "end": "", "rank": "副处级", "note": "挂职"},
    {"person_id": "heshun_zhao_wentao", "org_id": "heshun_gov", "title": "副县长（挂职）", "start": "", "end": "", "rank": "副处级", "note": "挂职"},
    # === 常守义 ===
    {"person_id": "heshun_chang_shouyi", "org_id": "heshun_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 韩永魁 ===
    {"person_id": "heshun_han_yongkui", "org_id": "heshun_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 张志海 ===
    {"person_id": "heshun_zhang_haihai", "org_id": "heshun_gov", "title": "副县长、公安局局长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "heshun_zhang_haihai", "org_id": "heshun_public_security", "title": "公安局局长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # === 杜紫颂 ===
    {"person_id": "heshun_du_zisong", "org_id": "heshun_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 袁瑞军 ===
    {"person_id": "heshun_yuan_ruijun", "org_id": "heshun_congress", "title": "县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    # === 侯建忠 ===
    {"person_id": "heshun_hou_jianzhong", "org_id": "heshun_congress", "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 梁建宏 ===
    {"person_id": "heshun_liang_jianhong", "org_id": "heshun_congress", "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 张志坚 ===
    {"person_id": "heshun_zhang_zhijian", "org_id": "heshun_congress", "title": "县人大常委会党组成员", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    # === 郭庆 ===
    {"person_id": "heshun_guo_qing", "org_id": "heshun_congress", "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 吕志鹏 ===
    {"person_id": "heshun_lv_zhipeng", "org_id": "heshun_congress", "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 易俊杰 ===
    {"person_id": "heshun_yi_junjie", "org_id": "heshun_cppcc", "title": "县政协党组书记", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    # === 李明 ===
    {"person_id": "heshun_li_ming", "org_id": "heshun_cppcc", "title": "县政协主席", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    # === 王富梅 ===
    {"person_id": "heshun_wang_fumei", "org_id": "heshun_cppcc", "title": "县政协副主席", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    # === 郝志刚 ===
    {"person_id": "heshun_hao_zhigang", "org_id": "heshun_cppcc", "title": "县政协一级调研员", "start": "", "end": "", "rank": "正处级", "note": "现任"},
]

relationships = [
    # 书记与县长搭班
    ("heshun_li_xue", "heshun_ma_xin", "colleague", "书记与县长搭班", "中共和顺县委常委会", "2026-至今"),
    # 书记与县委常委
    ("heshun_li_xue", "heshun_dong_guohua", "colleague", "书记与副书记", "中共和顺县委常委会", "2026-至今"),
    ("heshun_li_xue", "heshun_zhang_chi", "colleague", "书记与常务副县长", "中共和顺县委常委会", "2026-至今"),
    ("heshun_li_xue", "heshun_li_xingxing", "colleague", "书记与组织部长", "中共和顺县委常委会", ""),
    ("heshun_li_xue", "heshun_tian_jinbin", "colleague", "书记与纪委书记", "中共和顺县委常委会", ""),
    ("heshun_li_xue", "heshun_zhao_haifeng", "colleague", "书记与政法委书记", "中共和顺县委常委会", ""),
    ("heshun_li_xue", "heshun_bai_shibin", "colleague", "书记与宣传部长", "中共和顺县委常委会", ""),
    ("heshun_li_xue", "heshun_zhao_yao", "colleague", "书记与人武部政委", "中共和顺县委常委会", ""),
    ("heshun_li_xue", "heshun_zhao_wentao", "colleague", "书记与挂职副县长", "中共和顺县委常委会", ""),
    # 县长与政府班子成员
    ("heshun_ma_xin", "heshun_zhang_chi", "colleague", "县长与常务副县长", "和顺县人民政府", ""),
    ("heshun_ma_xin", "heshun_chang_shouyi", "colleague", "县长与副县长", "和顺县人民政府", ""),
    ("heshun_ma_xin", "heshun_han_yongkui", "colleague", "县长与副县长", "和顺县人民政府", ""),
    ("heshun_ma_xin", "heshun_zhang_zhihai", "colleague", "县长与公安局长", "和顺县人民政府", ""),
    ("heshun_ma_xin", "heshun_du_zisong", "colleague", "县长与副县长", "和顺县人民政府", ""),
    ("heshun_ma_xin", "heshun_zhao_wentao", "colleague", "县长与挂职副县长", "和顺县人民政府", ""),
    # 四套班子领导
    ("heshun_li_xue", "heshun_yuan_ruijun", "colleague", "书记与人大会主任", "和顺县四套班子", ""),
    ("heshun_li_xue", "heshun_li_ming", "colleague", "书记与政协主席", "和顺县四套班子", ""),
    ("heshun_ma_xin", "heshun_yuan_ruijun", "colleague", "县长与人大会主任", "和顺县四套班子", ""),
    ("heshun_ma_xin", "heshun_li_ming", "colleague", "县长与政协主席", "和顺县四套班子", ""),
]

# Convert tuple relationships to dicts for GEXF builder
relationship_tuples = []
for ra in relationships:
    relationship_tuples.append(ra)

# ========== BUILD DATABASE ==========

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"], p["party_join"],
                 p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for ra in relationship_tuples:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (ra[0], ra[1], ra[2], ra[3], ra[4], ra[5]))

conn.commit()

print(f"[DB] Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
print(f"[DB] Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
print(f"[DB] Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
print(f"[DB] Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

# ========== BUILD GEXF ==========

from datetime import datetime

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>gov-relation research agent</creator>')
lines.append('    <description>和顺县领导班子工作关系网络 - 2026年7月</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="role" title="role" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="relation_type" title="relation_type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('      <attribute id="overlap_period" title="overlap_period" type="string"/>')
lines.append('    </attributes>')

# Nodes: persons
lines.append('    <nodes>')
for p in persons:
    post = p["current_post"] or ""
    if "县委书记" in post and "副书记" not in post:
        color = "255,50,50"
        sz = "20.0"
    elif "县长" in post:
        color = "50,100,255"
        sz = "20.0"
    elif "纪委书记" in post or "县纪委书记" in post:
        color = "255,165,0"
        sz = "12.0"
    elif "副书记" in post:
        color = "50,100,255"
        sz = "15.0"
    else:
        color = "100,100,100"
        sz = "12.0"
    
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{esc(p["current_post"])}"/>')
    lines.append('        </attvalues>')
    r, g, b = color.split(",")
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: organizations
org_colors = {
    "party": "255,200,200", "government": "200,200,255", "discipline": "255,200,200",
    "party_dept": "255,200,200", "congress": "200,255,255", "cppcc": "255,240,200",
}
for o in organizations:
    oc = org_colors.get(o.get("type", ""), "200,200,200")
    lines.append(f'      <node id="{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    r, g, b = oc.split(",")
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for pos in positions:
    if not pos["org_id"]:
        continue
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="worked_at" type="directed">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="relation_type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    if pos["start"]:
        lines.append(f'          <attvalue for="overlap_period" value="{pos["start"]}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for ra in relationship_tuples:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="{ra[0]}" target="{ra[1]}" label="{ra[2]}" type="undirected">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="relation_type" value="{ra[2]}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(ra[3])}"/>')
    if ra[5]:
        lines.append(f'          <attvalue for="overlap_period" value="{ra[5]}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[GEXF] Written to: {GEXF_PATH}")
print("[Done] build_和顺县_data.py completed.")