#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Duchang County (都昌县) leadership network.

Current leadership (as of July 2026):
  县委书记: 徐翔 (formerly county magistrate, succeeded 邱舰 who was investigated)
  代县长: 韩政兴 (appointed July 13, 2026)
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/duchang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/duchang_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (县委书记) ──
    {"id": 1, "name": "徐翔", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-07", "birthplace": "江西湖口", "education": "大学（南昌大学法律专业）",
     "party_join": "1997-07", "work_start": "1997-08",
     "current_post": "中共都昌县委书记", "current_org": "中共都昌县委员会",
     "source": "https://www.duchang.gov.cn/zwzx/ttxw/202607/t20260710_7271851.html"},
    
    # ── Current Acting County Magistrate (代县长) ──
    {"id": 2, "name": "韩政兴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人民政府代县长", "current_org": "都昌县人民政府",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    # ── County People's Congress Chairman ──
    {"id": 3, "name": "叶长青", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人大常委会主任", "current_org": "都昌县人民代表大会常务委员会",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    # ── County PPCC Chairman ──
    {"id": 4, "name": "谭四明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县政协主席", "current_org": "政协都昌县委员会",
     "source": "https://www.duchang.gov.cn/"},
    
    # ── Organization Department Head ──
    {"id": 5, "name": "沈承峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县委常委、组织部部长", "current_org": "中共都昌县委员会",
     "source": "https://www.duchang.gov.cn/zwzx/dcyw/202607/t20260713_7272932.html"},
    
    # ── County Leader (副县长级) ──
    {"id": 6, "name": "梅中华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县领导", "current_org": "都昌县人民政府",
     "source": "https://www.duchang.gov.cn/zwzx/ttxw/202607/t20260710_7271851.html"},
    
    # ── PPCC Vice Chair / Party Committee Office Director ──
    {"id": 7, "name": "余琦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县政协副主席、县委办公室主任", "current_org": "政协都昌县委员会",
     "source": "https://www.duchang.gov.cn/zwzx/dcyw/202607/t20260710_7271847.html"},
    
    # ── NPC Vice Chairs ──
    {"id": 8, "name": "陈长虹", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人大常委会副主任", "current_org": "都昌县人民代表大会常务委员会",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    {"id": 9, "name": "江东海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人大常委会副主任", "current_org": "都昌县人民代表大会常务委员会",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    {"id": 10, "name": "江康侥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人大常委会副主任", "current_org": "都昌县人民代表大会常务委员会",
     "source": "https://www.duchang.gov.cn/zwzx/dcyw/202607/t20260713_7272932.html"},
    
    {"id": 11, "name": "梅水荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人大常委会副主任", "current_org": "都昌县人民代表大会常务委员会",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    {"id": 12, "name": "邵新生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人大常委会副主任", "current_org": "都昌县人民代表大会常务委员会",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    # ── Court & Procuratorate newly appointed ──
    {"id": 13, "name": "刘小伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人民法院代理院长", "current_org": "都昌县人民法院",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    {"id": 14, "name": "万钧", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "都昌县人民检察院代理检察长", "current_org": "都昌县人民检察院",
     "source": "https://www.duchang.gov.cn/zwzx/tpbd/202607/t20260714_7273832.html"},
    
    # ── PREVIOUS Party Secretary (邱舰 - investigated Nov 2025) ──
    {"id": 15, "name": "邱舰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原都昌县委书记（被查）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E9%82%B1%E8%88%B0/65573526"},
    
    # ── PREVIOUS County Mayor (万述幼 - predecessor to 徐翔) ──
    {"id": 16, "name": "万述幼", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原都昌县县长", "current_org": "",
     "source": "https://www.jiujiang.gov.cn/zwzx/bmdt/202601/t20260114_7149223.html"},
    
    # ── Previous Party Secretary before 邱舰 ──
    {"id": 24, "name": "肖立新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原都昌县委书记", "current_org": "",
     "source": "https://www.jiujiang.gov.cn/"},
    
    # ── Cross-network figures (known from other investigations) ──
    # 江训开 - from Duchang, currently 鹰潭常务副市长
    {"id": 17, "name": "江训开", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-09", "birthplace": "江西都昌", "education": "省委党校研究生",
     "party_join": "", "work_start": "",
     "current_post": "鹰潭市委常委、常务副市长", "current_org": "鹰潭市人民政府",
     "source": "https://baike.baidu.com/item/%E6%B1%9F%E8%AE%AD%E5%BC%80/23746796"},
    
    # 吴隽 - from Duchang, currently 景德镇副书记
    {"id": 18, "name": "吴隽", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-02", "birthplace": "江西都昌", "education": "博士/教授",
     "party_join": "", "work_start": "",
     "current_post": "景德镇市委专职副书记", "current_org": "中共景德镇市委员会",
     "source": "https://baike.baidu.com/item/%E5%90%B4%E9%9A%BD/10653311"},
    
    # 付磊 - from Duchang, currently 青山湖组织部长
    {"id": 19, "name": "付磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-10", "birthplace": "江西都昌", "education": "华中科技大学新闻学",
     "party_join": "", "work_start": "",
     "current_post": "青山湖区委常委、组织部部长", "current_org": "中共青山湖区委员会",
     "source": "https://www.ncqsh.gov.cn/"},
    
    # 江龙 - from Duchang, currently 红谷滩常务副区长
    {"id": 20, "name": "江龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "江西都昌", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "红谷滩区委常委、常务副区长", "current_org": "红谷滩区人民政府",
     "source": "https://hgt.nc.gov.cn/"},
    
    # 谭翼直 - from Duchang, currently 安义县委常委、常务副县长
    {"id": 21, "name": "谭翼直", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-05", "birthplace": "江西都昌", "education": "在职研究生/工商管理硕士",
     "party_join": "2007-12", "work_start": "2010-08",
     "current_post": "安义县委常委、常务副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202307/17d36c36095f485ea22916e78ee99042.shtml"},
    
    # 余超 - from Duchang, currently 安义县委常委、副县长
    {"id": 22, "name": "余超", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-08", "birthplace": "江西都昌", "education": "硕士研究生",
     "party_join": "2004-05", "work_start": "2008-06",
     "current_post": "安义县委常委、副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202504/db551054acbd43cea5283a58933dc8a7.shtml"},
    
    # 汪众华 - from Duchang, currently 南昌市文联党组书记
    {"id": 23, "name": "汪众华", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "江西都昌", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南昌市文学艺术界联合会党组书记", "current_org": "南昌市文学艺术界联合会",
     "source": "https://baike.baidu.com/item/%E6%B1%AA%E4%BC%97%E5%8D%8E"},
]

organizations = [
    {"id": 1, "name": "中共都昌县委员会", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西九江都昌"},
    {"id": 2, "name": "都昌县人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江都昌"},
    {"id": 3, "name": "都昌县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "九江市人民代表大会常务委员会", "location": "江西九江都昌"},
    {"id": 4, "name": "政协都昌县委员会", "type": "政协", "level": "县处级", "parent": "政协九江市委员会", "location": "江西九江都昌"},
    {"id": 5, "name": "都昌县人民法院", "type": "司法机关", "level": "县处级", "parent": "", "location": "江西九江都昌"},
    {"id": 6, "name": "都昌县人民检察院", "type": "司法机关", "level": "县处级", "parent": "", "location": "江西九江都昌"},
    {"id": 7, "name": "鹰潭市人民政府", "type": "政府", "level": "厅级", "parent": "江西省人民政府", "location": "江西鹰潭"},
    {"id": 8, "name": "中共景德镇市委员会", "type": "党委", "level": "厅级", "parent": "中共江西省委", "location": "江西景德镇"},
    {"id": 9, "name": "中共青山湖区委员会", "type": "党委", "level": "县处级", "parent": "中共南昌市委员会", "location": "江西南昌青山湖"},
    {"id": 10, "name": "红谷滩区人民政府", "type": "政府", "level": "县处级", "parent": "南昌市人民政府", "location": "江西南昌红谷滩"},
    {"id": 11, "name": "安义县人民政府", "type": "政府", "level": "县处级", "parent": "南昌市人民政府", "location": "江西南昌安义"},
    {"id": 12, "name": "中共安义县委员会", "type": "党委", "level": "县处级", "parent": "中共南昌市委员会", "location": "江西南昌安义"},
    {"id": 13, "name": "南昌市文学艺术界联合会", "type": "群团", "level": "县处级", "parent": "", "location": "江西南昌"},
    {"id": 14, "name": "中共九江市委员会", "type": "党委", "level": "厅级", "parent": "中共江西省委", "location": "江西九江"},
    {"id": 15, "name": "九江市人民政府", "type": "政府", "level": "厅级", "parent": "江西省人民政府", "location": "江西九江"},
    {"id": 16, "name": "九江经济技术开发区", "type": "开发区", "level": "厅级", "parent": "九江市人民政府", "location": "江西九江"},
]

positions = [
    # ── Xu Xiang (徐翔) career timeline ──
    # Current: Party Secretary
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共都昌县委书记", "start": "2026-01", "end": "", "rank": "县处级正职", "note": "现任，2026年1月13日任县委书记"},
    # Previous: County Magistrate
    {"id": 26, "person_id": 1, "org_id": 2, "title": "都昌县人民政府县长", "start": "2024-07", "end": "2026-01", "rank": "县处级正职", "note": "2024年7月24日当选县长，2026年1月卸任"},
    # Before Duchang: Jiujiang Economic Development Zone
    {"id": 27, "person_id": 1, "org_id": 16, "title": "九江经济技术开发区领导职务", "start": "2021", "end": "2024-06", "rank": "县处级", "note": "2021年后在九江经济技术开发区工作"},
    # Before: Lianxi District (formerly 庐山区)
    {"id": 28, "person_id": 1, "org_id": 1, "title": "濂溪区（原庐山区）领导职务", "start": "", "end": "2021", "rank": "县处级副职", "note": "曾在庐山区、濂溪区任职"},
    # Early career: De'an County
    {"id": 29, "person_id": 1, "org_id": 2, "title": "德安县磨溪乡等乡镇任职", "start": "2006", "end": "", "rank": "乡科级", "note": "2006年起在德安县磨溪乡等地任职"},
    # Early career: Jiujiang city departments
    {"id": 30, "person_id": 1, "org_id": 15, "title": "九江市对外经济技术合作办、招商协作局、审计局任职", "start": "", "end": "2006", "rank": "", "note": "在九江市多个部门工作"},
    # Earliest: Teacher
    {"id": 31, "person_id": 1, "org_id": 15, "title": "江西省化学工业技工学校教师", "start": "1997-08", "end": "", "rank": "", "note": "最早职业为技校教师"},
    
    # ── Han Zhengxing (韩政兴) career ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "都昌县人民政府代县长", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "新任代县长，2026年7月13日任命"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "都昌县人民政府副县长", "start": "2026-07", "end": "", "rank": "县处级副职", "note": "同时被任命为副县长（代县长过渡）"},
    
    # ── Ye Changqing (叶长青) ──
    {"id": 4, "person_id": 3, "org_id": 3, "title": "都昌县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    
    # ── Tan Siming (谭四明) ──
    {"id": 5, "person_id": 4, "org_id": 4, "title": "都昌县政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    
    # ── Shen Chengfeng (沈承峰) ──
    {"id": 6, "person_id": 5, "org_id": 1, "title": "都昌县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    
    # ── Mei Zhonghua (梅中华) ──
    {"id": 7, "person_id": 6, "org_id": 2, "title": "都昌县领导", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    
    # ── Yu Qi (余琦) ──
    {"id": 8, "person_id": 7, "org_id": 4, "title": "都昌县政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 7, "org_id": 1, "title": "都昌县委办公室主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任（兼任）"},
    
    # ── NPC Vice Chairs ──
    {"id": 10, "person_id": 8, "org_id": 3, "title": "都昌县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 9, "org_id": 3, "title": "都昌县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 10, "org_id": 3, "title": "都昌县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 13, "person_id": 11, "org_id": 3, "title": "都昌县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 12, "org_id": 3, "title": "都昌县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    
    # ── Court & Procuratorate ──
    {"id": 15, "person_id": 13, "org_id": 5, "title": "都昌县人民法院代理院长", "start": "2026-07", "end": "", "rank": "县处级副职", "note": "新任，2026年7月13日任命"},
    {"id": 16, "person_id": 14, "org_id": 6, "title": "都昌县人民检察院代理检察长", "start": "2026-07", "end": "", "rank": "县处级副职", "note": "新任，2026年7月13日任命"},
    
    # ── Previous leaders ──
    {"id": 17, "person_id": 15, "org_id": 1, "title": "中共都昌县委书记", "start": "", "end": "2025-11", "rank": "县处级正职", "note": "前任县委书记，2025年11月被查（涉嫌严重违纪违法）"},
    {"id": 18, "person_id": 16, "org_id": 2, "title": "都昌县人民政府县长", "start": "", "end": "2024-06", "rank": "县处级正职", "note": "前任县长，2024年6月卸任"},
    {"id": 32, "person_id": 24, "org_id": 1, "title": "中共都昌县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "前任县委书记（早于邱舰）"},
    
    # ── Cross-network figures ──
    {"id": 19, "person_id": 17, "org_id": 7, "title": "鹰潭市委常委、常务副市长", "start": "", "end": "", "rank": "厅级副职", "note": "现任，都昌籍"},
    {"id": 20, "person_id": 18, "org_id": 8, "title": "景德镇市委专职副书记", "start": "", "end": "", "rank": "厅级副职", "note": "现任，都昌籍"},
    {"id": 21, "person_id": 19, "org_id": 9, "title": "青山湖区委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任，都昌籍"},
    {"id": 22, "person_id": 20, "org_id": 10, "title": "红谷滩区委常委、常务副区长", "start": "", "end": "", "rank": "县处级副职", "note": "现任，都昌籍"},
    {"id": 23, "person_id": 21, "org_id": 11, "title": "安义县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任，都昌籍"},
    {"id": 24, "person_id": 22, "org_id": 11, "title": "安义县委常委、副县长", "start": "2025", "end": "", "rank": "县处级副职", "note": "现任，都昌籍"},
    {"id": 25, "person_id": 23, "org_id": 13, "title": "南昌市文联党组书记", "start": "", "end": "", "rank": "县处级正职", "note": "都昌籍，原青云谱区长"},
]

relationships = [
    # ── Party Secretary + Acting Mayor ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "徐翔（县委书记）与韩政兴（代县长）组成党政班子",
     "overlap_org": "都昌县", "overlap_period": "2026-07至今"},
    
    # ── Predecessor-Successor: Party Secretary ──
    {"id": 2, "person_a_id": 15, "person_b_id": 1, "type": "交接",
     "context": "邱舰（被查）→徐翔 都昌县委书记交接（2026年1月）",
     "overlap_org": "中共都昌县委员会", "overlap_period": "2026"},
    
    # ── Predecessor-Successor: County Mayor ──
    {"id": 3, "person_a_id": 16, "person_b_id": 1, "type": "交接",
     "context": "万述幼→徐翔 都昌县长交接（2024年7月）",
     "overlap_org": "都昌县人民政府", "overlap_period": "2024-07"},
    
    # ── Xu Xiang took over from 万述幼 as magistrate, then succeeded 邱舰 as secretary ──
    {"id": 18, "person_a_id": 1, "person_b_id": 16, "type": "前任继任",
     "context": "徐翔接替万述幼任都昌县长",
     "overlap_org": "都昌县人民政府", "overlap_period": "2024-07"},
    
    # ── Current leadership team ──
    {"id": 4, "person_a_id": 1, "person_b_id": 5, "type": "上下级",
     "context": "徐翔（书记）与沈承峰（组织部长）",
     "overlap_org": "中共都昌县委员会", "overlap_period": ""},
    
    {"id": 5, "person_a_id": 1, "person_b_id": 3, "type": "四套班子",
     "context": "县委书记与人大常委会主任",
     "overlap_org": "都昌县", "overlap_period": ""},
    
    {"id": 6, "person_a_id": 1, "person_b_id": 4, "type": "四套班子",
     "context": "县委书记与政协主席",
     "overlap_org": "都昌县", "overlap_period": ""},
    
    {"id": 7, "person_a_id": 1, "person_b_id": 7, "type": "上下级",
     "context": "徐翔（书记）与余琦（县委办主任）",
     "overlap_org": "中共都昌县委员会", "overlap_period": ""},
    
    {"id": 8, "person_a_id": 3, "person_b_id": 8, "type": "同僚",
     "context": "叶长青（主任）与陈长虹（副主任）",
     "overlap_org": "都昌县人民代表大会常务委员会", "overlap_period": ""},
    
    {"id": 9, "person_a_id": 3, "person_b_id": 9, "type": "同僚",
     "context": "叶长青与江东海均为人大常委会领导",
     "overlap_org": "都昌县人民代表大会常务委员会", "overlap_period": ""},
    
    {"id": 10, "person_a_id": 8, "person_b_id": 9, "type": "同僚",
     "context": "陈长虹与江东海均为人常委会副主任",
     "overlap_org": "都昌县人民代表大会常务委员会", "overlap_period": ""},
    
    # ── Former party secretary and former magistrate pair ──
    {"id": 17, "person_a_id": 15, "person_b_id": 16, "type": "前党政搭档",
     "context": "邱舰（原县委书记）与万述幼（原县长）为前任党政班子",
     "overlap_org": "都昌县", "overlap_period": ""},
    
    # ── Succession chain: 肖立新 → 邱舰 → 徐翔 ──
    {"id": 19, "person_a_id": 24, "person_b_id": 15, "type": "前任继任",
     "context": "肖立新→邱舰 都昌县委书记交接",
     "overlap_org": "中共都昌县委员会", "overlap_period": ""},
    
    # ── Cross-county connections: Duchang natives in other cities ──
    {"id": 11, "person_a_id": 17, "person_b_id": 18, "type": "都昌籍",
     "context": "江训开（鹰潭常务副市长）与吴隽（景德镇副书记）均为都昌籍厅级干部",
     "overlap_org": "", "overlap_period": ""},
    
    {"id": 12, "person_a_id": 19, "person_b_id": 20, "type": "都昌籍",
     "context": "付磊（青山湖组织部长）与江龙（红谷滩常务副区长）均为都昌籍南昌任职",
     "overlap_org": "", "overlap_period": ""},
    
    {"id": 13, "person_a_id": 21, "person_b_id": 22, "type": "都昌籍同乡",
     "context": "谭翼直与余超均为都昌籍，同在安义县任县委常委",
     "overlap_org": "中共安义县委员会", "overlap_period": ""},
    
    {"id": 14, "person_a_id": 21, "person_b_id": 23, "type": "都昌籍",
     "context": "谭翼直（安义常委）与汪众华（原青云谱区长）均都昌籍",
     "overlap_org": "", "overlap_period": ""},
    
    {"id": 15, "person_a_id": 23, "person_b_id": 22, "type": "都昌籍",
     "context": "汪众华与余超均为都昌籍",
     "overlap_org": "", "overlap_period": ""},
    
    # ── Cross-county exchange: Xu Xiang is from Hukou (湖口) ──
    {"id": 20, "person_a_id": 1, "person_b_id": 17, "type": "都昌籍/湖口籍关联",
     "context": "徐翔（湖口人）与江训开（都昌人）均在九江体系任职；徐翔从湖口附近跨县调任都昌",
     "overlap_org": "", "overlap_period": ""},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
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
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>都昌县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    # Color by role
    if p["id"] == 1:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = '#2980B9'  # blue: government leader (county mayor)
        size = 20.0
    elif p["id"] == 3:
        color = '#5a7a9a'  # blue-grey: NPC
        size = 16.0
    elif p["id"] == 4:
        color = '#7a5a9a'  # purple: PPCC
        size = 16.0
    elif p["id"] in [15, 24]:
        color = '#95A5A6'  # grey: former leaders
        size = 14.0
    elif p["id"] == 16:
        color = '#95A5A6'  # grey: former magistrate
        size = 14.0
    elif p["id"] in [17, 18]:
        color = '#2980B9'  # blue: cross-county officials (gov)
        size = 14.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
