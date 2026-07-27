#!/usr/bin/env python3
"""Build 左权县 (Zuoquan County) personnel network database + GEXF graph."""

import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'shanxi_左权县':
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

DB_PATH = os.path.join(PROJECT_ROOT, "data/database/左权县_network.db")
GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/左权县_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# ========== DATA ==========

persons = [
    # === Core Leaders ===
    {"id": "zuoquan_shi_yong", "name": "石勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年12月", "birthplace": "山西省忻州市",
     "education": "大学学历，山西农业大学农业推广硕士",
     "party_join": "1995年1月", "work_start": "1995年12月",
     "current_post": "县委书记", "current_org": "中共左权县委员会",
     "source": "https://baike.baidu.com/item/%E7%9F%B3%E5%8B%87/9470984"},
    {"id": "zuoquan_guo_fenghui", "name": "郭丰慧", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年11月", "birthplace": "山西省太谷县",
     "education": "省委党校研究生学历",
     "party_join": "1998年7月", "work_start": "1995年11月",
     "current_post": "县委副书记、县长", "current_org": "左权县人民政府",
     "source": "https://baike.baidu.com/item/%E9%83%AD%E4%B8%B0%E6%85%A7/4812801"},
    {"id": "zuoquan_chen_cheng", "name": "陈成", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年11月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、统战部部长", "current_org": "中共左权县委员会",
     "source": "http://www.jzzq.gov.cn/zwgkzy/fdzdgknr/zldzc/xwld/"},
    {"id": "zuoquan_zheng_liyong", "name": "郑力勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、纪委书记、监委主任", "current_org": "左权县纪律检查委员会",
     "source": "http://jzjjjc.gov.cn/"},
    {"id": "zuoquan_ju_xiaohua", "name": "巨晓华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长（常务）", "current_org": "左权县人民政府",
     "source": "http://www.jzzq.gov.cn/zwgkzy/fdzdgknr/zldzc/xwld/"},
    {"id": "zuoquan_wang_xianwei", "name": "王贤伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "左权县人民政府",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_ren_rui", "name": "任睿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "左权县人民政府",
     "source": "http://www.jzzq.gov.cn/zwgkzy/fdzdgknr/zldzc/xwld/"},
    {"id": "zuoquan_wang_yadong", "name": "王亚东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共左权县委组织部",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_geng_hua", "name": "耿华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共左权县委统战部",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_qin_guoying", "name": "秦国英", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共左权县委宣传部",
     "source": "http://www.jzzq.gov.cn/zwgkzy/fdzdgknr/zldzc/xwld/"},
    {"id": "zuoquan_cao_fengyun", "name": "曹峰云", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共左权县委政法委员会",
     "source": "http://www.jzzq.gov.cn/zwgkzy/fdzdgknr/zldzc/xwld/"},
    {"id": "zuoquan_cheng_zhenhua", "name": "程振华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "左权县人民政府",
     "source": "https://www.sohu.com/"},
    {"id": "zuoquan_feng_ruibin", "name": "冯瑞斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "左权县人民政府",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_wang_fei", "name": "王斐", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、公安局局长", "current_org": "左权县公安局",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_han_tao", "name": "韩滔", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "左权县人民政府",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_zhang_shihua", "name": "张世华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "左权县人大常委会",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_gao_rulin", "name": "高儒林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原县人大常委会主任", "current_org": "左权县人大常委会",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_lv_aihong", "name": "吕爱鸿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席", "current_org": "政协左权县委员会",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_li_zuohong", "name": "李左红", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原县政协主席", "current_org": "政协左权县委员会",
     "source": "http://www.jzzq.gov.cn/"},
    {"id": "zuoquan_wang_bing", "name": "王兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋中市委常委、宣传部部长", "current_org": "中共晋中市委宣传部",
     "source": "https://baike.baidu.com/"},
    {"id": "zuoquan_zhao_hongzhong", "name": "赵宏钟", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年9月", "birthplace": "山西省襄垣县",
     "education": "省委党校研究生，公共管理硕士",
     "party_join": "1997年7月", "work_start": "1988年8月",
     "current_post": "晋中市政协副主席、寿阳县委书记", "current_org": "寿阳县委",
     "source": "https://baike.baidu.com/"},
]

organizations = [
    {"id": "zuoquan_party_committee", "name": "中共左权县委员会", "type": "party", "level": "county", "parent": "晋中市委", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_gov", "name": "左权县人民政府", "type": "government", "level": "county", "parent": "晋中市政府", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_discipline", "name": "左权县纪律检查委员会", "type": "discipline", "level": "county", "parent": "晋中市纪委监委", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_org_dept", "name": "中共左权县委组织部", "type": "party_dept", "level": "county", "parent": "左权县委", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_propaganda_dept", "name": "中共左权县委宣传部", "type": "party_dept", "level": "county", "parent": "左权县委", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_uf_dept", "name": "中共左权县委统战部", "type": "party_dept", "level": "county", "parent": "左权县委", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_political_legal", "name": "中共左权县委政法委员会", "type": "party_dept", "level": "county", "parent": "左权县委", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_public_security", "name": "左权县公安局", "type": "government", "level": "county", "parent": "左权县政府", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_congress", "name": "左权县人大常委会", "type": "congress", "level": "county", "parent": "左权县", "location": "山西省晋中市左权县"},
    {"id": "zuoquan_cppcc", "name": "政协左权县委员会", "type": "cppcc", "level": "county", "parent": "左权县", "location": "山西省晋中市左权县"},
    {"id": "jinzhong_party_committee", "name": "中共晋中市委员会", "type": "party", "level": "prefecture", "parent": "山西省委", "location": "山西省晋中市"},
    {"id": "jinzhong_propaganda", "name": "中共晋中市委宣传部", "type": "party_dept", "level": "prefecture", "parent": "晋中市委", "location": "山西省晋中市"},
    {"id": "shouyang_party_committee", "name": "中共寿阳县委员会", "type": "party", "level": "county", "parent": "晋中市委", "location": "山西省晋中市寿阳县"},
    {"id": "jinzhong_gov", "name": "晋中市人民政府", "type": "government", "level": "prefecture", "parent": "山西省政府", "location": "山西省晋中市"},
    {"id": "zuoquan_eco_tourism", "name": "左权生态文化旅游示范区管委会", "type": "development_zone", "level": "county", "parent": "左权县政府", "location": "山西省晋中市左权县"},
]

positions = [
    # 石勇
    {"person_id": "zuoquan_shi_yong", "org_id": "zuoquan_party_committee", "title": "县委书记", "start": "2021-02", "end": "", "rank": "正处级", "note": "现任"},
    # 郭丰慧
    {"person_id": "zuoquan_guo_fenghui", "org_id": "zuoquan_party_committee", "title": "县委副书记", "start": "2022-01", "end": "", "rank": "正处级", "note": "现任"},
    {"person_id": "zuoquan_guo_fenghui", "org_id": "zuoquan_gov", "title": "县长", "start": "2022-02-09", "end": "", "rank": "正处级", "note": "现任"},
    {"person_id": "zuoquan_guo_fenghui", "org_id": "jinzhong_gov", "title": "市乡村振兴局局长", "start": "2021-08", "end": "2022-01", "rank": "正处级", "note": ""},
    {"person_id": "zuoquan_guo_fenghui", "org_id": "jinzhong_gov", "title": "市扶贫办主任", "start": "2019-01", "end": "2021-08", "rank": "正处级", "note": ""},
    # 陈成
    {"person_id": "zuoquan_chen_cheng", "org_id": "zuoquan_party_committee", "title": "县委副书记、统战部部长", "start": "2025-02", "end": "", "rank": "副处级", "note": ""},
    # 郑力勇
    {"person_id": "zuoquan_zheng_liyong", "org_id": "zuoquan_discipline", "title": "县委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 巨晓华
    {"person_id": "zuoquan_ju_xiaohua", "org_id": "zuoquan_party_committee", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_ju_xiaohua", "org_id": "zuoquan_gov", "title": "副县长（常务）", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 王贤伟
    {"person_id": "zuoquan_wang_xianwei", "org_id": "zuoquan_party_committee", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_wang_xianwei", "org_id": "zuoquan_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 任睿
    {"person_id": "zuoquan_ren_rui", "org_id": "zuoquan_party_committee", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_ren_rui", "org_id": "zuoquan_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 王亚东
    {"person_id": "zuoquan_wang_yadong", "org_id": "zuoquan_party_committee", "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_wang_yadong", "org_id": "zuoquan_org_dept", "title": "组织部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 耿华
    {"person_id": "zuoquan_geng_hua", "org_id": "zuoquan_party_committee", "title": "县委常委、统战部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_geng_hua", "org_id": "zuoquan_uf_dept", "title": "统战部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 秦国英
    {"person_id": "zuoquan_qin_guoying", "org_id": "zuoquan_party_committee", "title": "县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_qin_guoying", "org_id": "zuoquan_propaganda_dept", "title": "宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 曹峰云
    {"person_id": "zuoquan_cao_fengyun", "org_id": "zuoquan_party_committee", "title": "县委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_cao_fengyun", "org_id": "zuoquan_political_legal", "title": "政法委书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 程振华
    {"person_id": "zuoquan_cheng_zhenhua", "org_id": "zuoquan_gov", "title": "副县长", "start": "2025-03", "end": "", "rank": "副处级", "note": ""},
    # 冯瑞斌
    {"person_id": "zuoquan_feng_ruibin", "org_id": "zuoquan_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 王斐
    {"person_id": "zuoquan_wang_fei", "org_id": "zuoquan_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zuoquan_wang_fei", "org_id": "zuoquan_public_security", "title": "公安局局长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 韩滔
    {"person_id": "zuoquan_han_tao", "org_id": "zuoquan_gov", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 张世华
    {"person_id": "zuoquan_zhang_shihua", "org_id": "zuoquan_congress", "title": "县人大常委会主任", "start": "2025-02", "end": "", "rank": "正处级", "note": ""},
    {"person_id": "zuoquan_zhang_shihua", "org_id": "zuoquan_eco_tourism", "title": "生态文旅示范区管委会主任", "start": "", "end": "2025-02", "rank": "正处级", "note": ""},
    # 高儒林
    {"person_id": "zuoquan_gao_rulin", "org_id": "zuoquan_congress", "title": "县人大常委会主任（原任）", "start": "", "end": "2025-02", "rank": "正处级", "note": ""},
    # 吕爱鸿
    {"person_id": "zuoquan_lv_aihong", "org_id": "zuoquan_cppcc", "title": "县政协主席", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 李左红
    {"person_id": "zuoquan_li_zuohong", "org_id": "zuoquan_cppcc", "title": "县政协主席（原任）", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 王兵
    {"person_id": "zuoquan_wang_bing", "org_id": "zuoquan_party_committee", "title": "县委书记（原任）", "start": "2016-09", "end": "2021-02", "rank": "正处级", "note": "晋中市委常委兼"},
    {"person_id": "zuoquan_wang_bing", "org_id": "jinzhong_propaganda", "title": "市委宣传部部长", "start": "2021-09", "end": "", "rank": "正厅级", "note": ""},
    # 赵宏钟
    {"person_id": "zuoquan_zhao_hongzhong", "org_id": "zuoquan_gov", "title": "县长（原任）", "start": "2013-03", "end": "2022-01", "rank": "正处级", "note": ""},
    {"person_id": "zuoquan_zhao_hongzhong", "org_id": "shouyang_party_committee", "title": "县委书记", "start": "2021-12", "end": "", "rank": "正处级", "note": "兼晋中市政协副主席"},
]

relationships = [
    ("zuoquan_shi_yong", "zuoquan_guo_fenghui", "colleague", "书记与县长搭班", "中共左权县委员会", "2022-至今"),
    ("zuoquan_shi_yong", "zuoquan_wang_bing", "predecessor_successor", "前后任县委书记", "中共左权县委员会", "2016-2021"),
    ("zuoquan_guo_fenghui", "zuoquan_zhao_hongzhong", "predecessor_successor", "前后任县长", "左权县人民政府", "2013-2022"),
    ("zuoquan_shi_yong", "zuoquan_chen_cheng", "colleague", "书记与副书记搭班", "中共左权县委员会", "2025-至今"),
    ("zuoquan_shi_yong", "zuoquan_ju_xiaohua", "colleague", "书记与常务副县长", "左权县委常委会", ""),
    ("zuoquan_shi_yong", "zuoquan_wang_yadong", "colleague", "书记与组织部长", "左权县委常委会", ""),
    ("zuoquan_shi_yong", "zuoquan_zheng_liyong", "colleague", "书记与纪委书记", "左权县委常委会", ""),
    ("zuoquan_shi_yong", "zuoquan_qin_guoying", "colleague", "书记与宣传部长", "左权县委常委会", ""),
    ("zuoquan_shi_yong", "zuoquan_cao_fengyun", "colleague", "书记与政法委书记", "左权县委常委会", ""),
    ("zuoquan_shi_yong", "zuoquan_geng_hua", "colleague", "书记与统战部长", "左权县委常委会", ""),
    ("zuoquan_shi_yong", "zuoquan_wang_xianwei", "colleague", "书记与副县长", "左权县委常委会", ""),
    ("zuoquan_shi_yong", "zuoquan_ren_rui", "colleague", "书记与副县长", "左权县委常委会", ""),
    ("zuoquan_guo_fenghui", "zuoquan_ju_xiaohua", "colleague", "县长与常务副县长", "左权县人民政府", ""),
    ("zuoquan_guo_fenghui", "zuoquan_cheng_zhenhua", "colleague", "县长与副县长", "左权县人民政府", "2025-03至今"),
    ("zuoquan_guo_fenghui", "zuoquan_wang_fei", "colleague", "县长与公安局局长", "左权县人民政府", ""),
    ("zuoquan_guo_fenghui", "zuoquan_feng_ruibin", "colleague", "县长与副县长", "左权县人民政府", ""),
    ("zuoquan_guo_fenghui", "zuoquan_han_tao", "colleague", "县长与副县长", "左权县人民政府", ""),
    ("zuoquan_shi_yong", "zuoquan_zhang_shihua", "colleague", "书记与人大会主任", "左权县四套班子", ""),
    ("zuoquan_shi_yong", "zuoquan_lv_aihong", "colleague", "书记与政协主席", "左权县四套班子", ""),
    ("zuoquan_gao_rulin", "zuoquan_zhang_shihua", "predecessor_successor", "前后任人大主任", "左权县人大常委会", "2025-02"),
    ("zuoquan_li_zuohong", "zuoquan_lv_aihong", "predecessor_successor", "前后任政协主席", "政协左权县委员会", "2024"),
    ("zuoquan_wang_bing", "zuoquan_zhao_hongzhong", "colleague", "书记与县长搭班", "中共左权县委员会", "2016-2021"),
]

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

for ra in relationships:
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
lines.append('    <description>左权县领导班子工作关系网络 - 2026年7月</description>')
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
    if "县委书记" in post:
        color = "255,50,50"
        sz = "20.0"
    elif "书记" in post and "纪委" not in post and "县长" in post:
        color = "50,100,255"
        sz = "20.0"
    elif "县长" in post:
        color = "50,100,255"
        sz = "20.0"
    elif "纪委书记" in post or "纪委" in post:
        color = "255,165,0"
        sz = "12.0"
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
    "development_zone": "200,255,200"
}
for o in organizations:
    oc = org_colors.get(o.get("type", ""), "200,200,200")
    lines.append(f'      <node id="{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue type="type" value="organization"/>')
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

for ra in relationships:
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
print("[Done] build_左权县_data.py completed.")