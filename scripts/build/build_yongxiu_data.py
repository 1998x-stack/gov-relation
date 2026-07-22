#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yongxiu County (永修县) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yongxiu_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yongxiu_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (一把手) ──
    {"id": 1, "name": "朱超", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年3月", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共永修县委书记", "current_org": "中共永修县委员会",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwsj/zc/"},

    # ── Current Acting County Mayor (二把手) ──
    {"id": 2, "name": "袁立", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年10月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永修县委副书记、代理县长", "current_org": "永修县人民政府",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwfsj/yl/"},

    # ── Deputy Party Secretary ──
    {"id": 3, "name": "万祥", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年5月", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "永修县委副书记（正县级）", "current_org": "中共永修县委员会",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwfsj/wx/"},

    # ── Standing Committee Members ──
    {"id": 4, "name": "喻建华", "gender": "男", "ethnicity": "汉族",
     "birth": "1984年8月", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永修县委常委、县政府常务副县长", "current_org": "永修县人民政府",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/yjh/"},

    {"id": 5, "name": "赵书楼", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年4月", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "永修县委常委、县人武部政委", "current_org": "永修县人民武装部",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/zsl/"},

    {"id": 6, "name": "刘伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年3月", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "永修县委常委、县纪委书记、县监委主任", "current_org": "中共永修县纪律检查委员会",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/liuwei/"},

    {"id": 7, "name": "余晓芳", "gender": "女", "ethnicity": "汉族",
     "birth": "1979年3月", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "永修县委常委、组织部部长", "current_org": "中共永修县委组织部",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/ll/"},

    {"id": 8, "name": "淦家寨", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年8月", "birthplace": "", "education": "省委党校研究生",
     "party_join": "", "work_start": "",
     "current_post": "永修县委常委、宣传部部长", "current_org": "中共永修县委宣传部",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/gjz/"},

    {"id": 9, "name": "李荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年10月", "birthplace": "", "education": "省委党校研究生",
     "party_join": "", "work_start": "",
     "current_post": "永修县委常委、政法委书记", "current_org": "中共永修县委政法委",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/lr/"},

    {"id": 10, "name": "万顺华", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年11月", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永修县委常委、统战部部长", "current_org": "中共永修县委统战部",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/wsh/"},

    {"id": 11, "name": "袁扬勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年9月", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永修县委常委、县政府副县长", "current_org": "永修县人民政府",
     "source": "https://www.yongxiu.gov.cn/zwgkx/01_298277/jggk/ldzc_186182/xwld/xwcw_186390/yyy/"},

    # ── Predecessor: Previous Party Secretary ──
    {"id": 12, "name": "秦岭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原永修县委书记（去向待查）", "current_org": "",
     "source": "https://www.yongxiu.gov.cn/xzwzx/tpxw/t_7253696.html"},

    # ── County NPC Chair (from news articles) ──
    {"id": 13, "name": "袁汝琴", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永修县人大常委会主任", "current_org": "永修县人民代表大会常务委员会",
     "source": "https://www.yongxiu.gov.cn/xzwzx/zwyw_186114/t_7273250.html"},

    # ── County PPCC Chair (from news articles) ──
    {"id": 14, "name": "张义红", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "政协永修县委员会主席", "current_org": "政协永修县委员会",
     "source": "https://www.yongxiu.gov.cn/xzwzx/zwyw_186114/t_7273250.html"},

    # ── Other figures mentioned in news ──
    {"id": 15, "name": "章友娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "赣江新区永修组团管委会副主任", "current_org": "赣江新区永修组团管委会",
     "source": "https://www.yongxiu.gov.cn/xzwzx/tpxw/t_7269888.html"},

    {"id": 16, "name": "黄黎明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "九江组织干部学院副院长", "current_org": "九江组织干部学院",
     "source": "https://www.yongxiu.gov.cn/xzwzx/tpxw/t_7269888.html"},

    {"id": 17, "name": "戴彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "云山经开区党工委书记", "current_org": "云山经开区党工委",
     "source": "https://www.yongxiu.gov.cn/xzwzx/tpxw/t_7269888.html"},
]

organizations = [
    {"id": 1, "name": "中共永修县委员会", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西九江永修"},
    {"id": 2, "name": "永修县人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江永修"},
    {"id": 3, "name": "永修县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "九江市人民代表大会常务委员会", "location": "江西九江永修"},
    {"id": 4, "name": "政协永修县委员会", "type": "政协", "level": "县处级", "parent": "政协九江市委员会", "location": "江西九江永修"},
    {"id": 5, "name": "永修县人民武装部", "type": "军事", "level": "县处级", "parent": "", "location": "江西九江永修"},
    {"id": 6, "name": "中共永修县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共永修县委员会", "location": "江西九江永修"},
    {"id": 7, "name": "中共永修县委组织部", "type": "党委部门", "level": "县处级", "parent": "中共永修县委员会", "location": "江西九江永修"},
    {"id": 8, "name": "中共永修县委宣传部", "type": "党委部门", "level": "县处级", "parent": "中共永修县委员会", "location": "江西九江永修"},
    {"id": 9, "name": "中共永修县委政法委", "type": "党委部门", "level": "县处级", "parent": "中共永修县委员会", "location": "江西九江永修"},
    {"id": 10, "name": "中共永修县委统战部", "type": "党委部门", "level": "县处级", "parent": "中共永修县委员会", "location": "江西九江永修"},
    {"id": 11, "name": "赣江新区永修组团管委会", "type": "政府派出机构", "level": "县处级", "parent": "永修县人民政府", "location": "江西九江永修"},
    {"id": 12, "name": "九江组织干部学院", "type": "事业单位", "level": "县处级", "parent": "", "location": "江西九江永修"},
    {"id": 13, "name": "云山经开区党工委", "type": "党委", "level": "县处级", "parent": "中共永修县委员会", "location": "江西九江永修"},
    {"id": 14, "name": "中共九江市委员会", "type": "党委", "level": "厅级", "parent": "中共江西省委", "location": "江西九江"},
    {"id": 15, "name": "九江市人民政府", "type": "政府", "level": "厅级", "parent": "江西省人民政府", "location": "江西九江"},
    {"id": 16, "name": "永修县人民法院", "type": "司法机关", "level": "县处级", "parent": "", "location": "江西九江永修"},
    {"id": 17, "name": "永修县人民检察院", "type": "司法机关", "level": "县处级", "parent": "", "location": "江西九江永修"},
]

positions = [
    # ── Zhu Chao (朱超) career timeline ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共永修县委书记", "start": "2026-07", "end": "", "rank": "县处级正职",
     "note": "2026年7月初接替秦岭任县委书记（确认来源：2026-07-03新闻标题称县委书记朱超）"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "永修县委副书记、县人民政府县长", "start": "此前", "end": "2026-07", "rank": "县处级正职",
     "note": "前任县长；2026年6月5日仍以县长身份召开县政府常务会议"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "永修县委常委", "start": "此前", "end": "2026-07", "rank": "县处级副职",
     "note": "晋升县长前先进入县委常委会"},

    # ── Yuan Li (袁立) career timeline ──
    {"id": 4, "person_id": 2, "org_id": 2, "title": "永修县委副书记、代理县长", "start": "2026-07", "end": "", "rank": "县处级正职",
     "note": "2026年7月初任代县长（县长提名人选）；2026年7月5日新闻称'县长提名人选'，官方简历称'代理县长'"},
    {"id": 5, "person_id": 2, "org_id": 1, "title": "中共永修县委副书记", "start": "2026-07", "end": "", "rank": "县处级副职",
     "note": "代理县长兼任县委副书记"},

    # ── Wan Xiang (万祥) career ──
    {"id": 6, "person_id": 3, "org_id": 1, "title": "永修县委副书记（正县级）", "start": "", "end": "", "rank": "县处级正职",
     "note": "现任，正县级县委副书记"},

    # ── Standing Committee Members' current positions ──
    {"id": 7, "person_id": 4, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 4, "org_id": 2, "title": "永修县政府党组副书记、常务副县长", "start": "", "end": "", "rank": "县处级副职",
     "note": "现任；协助县长分管政府常务工作"},

    {"id": 9, "person_id": 5, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 5, "org_id": 5, "title": "永修县人武部政委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    {"id": 11, "person_id": 6, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 6, "org_id": 6, "title": "永修县纪委书记、县监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    {"id": 13, "person_id": 7, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 7, "org_id": 7, "title": "永修县委组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    {"id": 15, "person_id": 8, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 8, "org_id": 8, "title": "永修县委宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    {"id": 17, "person_id": 9, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 18, "person_id": 9, "org_id": 9, "title": "永修县委政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    {"id": 19, "person_id": 10, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 20, "person_id": 10, "org_id": 10, "title": "永修县委统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    {"id": 21, "person_id": 11, "org_id": 1, "title": "永修县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 22, "person_id": 11, "org_id": 2, "title": "永修县人民政府副县长", "start": "", "end": "", "rank": "县处级副职",
     "note": "现任；分管城乡规划、自然资源、住建等"},

    # ── Predecessor: Qin Ling (秦岭) ──
    {"id": 23, "person_id": 12, "org_id": 1, "title": "中共永修县委书记", "start": "", "end": "2026-06", "rank": "县处级正职",
     "note": "前任县委书记；2026年6月9日主持会议，6月26日走访慰问老党员；2026年7月初卸任（去向待查）"},

    # ── NPC Chair ──
    {"id": 24, "person_id": 13, "org_id": 3, "title": "永修县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── PPCC Chair ──
    {"id": 25, "person_id": 14, "org_id": 4, "title": "政协永修县委员会主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── Other figures ──
    {"id": 26, "person_id": 15, "org_id": 11, "title": "赣江新区永修组团管委会副主任", "start": "", "end": "", "rank": "县处级", "note": "现任"},
    {"id": 27, "person_id": 16, "org_id": 12, "title": "九江组织干部学院副院长", "start": "", "end": "", "rank": "县处级", "note": "现任"},
    {"id": 28, "person_id": 17, "org_id": 13, "title": "云山经开区党工委书记", "start": "", "end": "", "rank": "县处级", "note": "现任"},
]

relationships = [
    # ── Party Secretary + Acting County Mayor (党政搭档) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "朱超（县委书记）与袁立（代理县长）组成新一届党政班子；朱超由县长转任书记，袁立接任代县长",
     "overlap_org": "永修县", "overlap_period": "2026-07至今"},

    # ── Party Secretary + Deputy Secretary ──
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "上下级",
     "context": "朱超（县委书记）与万祥（专职副书记）",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    {"id": 3, "person_a_id": 2, "person_b_id": 3, "type": "同僚",
     "context": "袁立（副书记、代县长）与万祥（专职副书记）",
     "overlap_org": "中共永修县委员会", "overlap_period": "2026-07至今"},

    # ── Predecessor-Successor: Party Secretary ──
    {"id": 4, "person_a_id": 12, "person_b_id": 1, "type": "前任继任",
     "context": "秦岭→朱超 永修县委书记交接（2026年7月初）",
     "overlap_org": "中共永修县委员会", "overlap_period": "2026-07"},

    # ── Previous leadership team: Qin Ling + Zhu Chao (former 党政搭档) ──
    {"id": 5, "person_a_id": 12, "person_b_id": 1, "type": "前任党政搭档",
     "context": "秦岭（原县委书记）与朱超（原县长）为前任党政班子（交接前）",
     "overlap_org": "永修县", "overlap_period": "至2026-06"},

    # ── Zhu Chao in Standing Committee ──
    {"id": 6, "person_a_id": 1, "person_b_id": 4, "type": "上下级",
     "context": "朱超（书记）与喻建华（常务副县长）",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    {"id": 7, "person_a_id": 1, "person_b_id": 7, "type": "上下级",
     "context": "朱超（书记）与余晓芳（组织部长）",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    {"id": 8, "person_a_id": 1, "person_b_id": 6, "type": "上下级",
     "context": "朱超（书记）与刘伟（纪委书记）",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    {"id": 9, "person_a_id": 1, "person_b_id": 9, "type": "上下级",
     "context": "朱超（书记）与李荣（政法委书记）",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    # ── Standing Committee internal relations ──
    {"id": 10, "person_a_id": 4, "person_b_id": 11, "type": "同僚",
     "context": "喻建华（常务副县长）与袁扬勇（副县长）均为县政府领导干部",
     "overlap_org": "永修县人民政府", "overlap_period": ""},

    {"id": 11, "person_a_id": 8, "person_b_id": 10, "type": "同僚",
     "context": "淦家寨（宣传部长）与万顺华（统战部长）均为党委部门负责人",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    # ── NPC + PPCC ──
    {"id": 12, "person_a_id": 1, "person_b_id": 13, "type": "四套班子",
     "context": "县委书记朱超与人大常委会主任袁汝琴",
     "overlap_org": "永修县", "overlap_period": ""},

    {"id": 13, "person_a_id": 1, "person_b_id": 14, "type": "四套班子",
     "context": "县委书记朱超与政协主席张义红",
     "overlap_org": "永修县", "overlap_period": ""},

    {"id": 14, "person_a_id": 13, "person_b_id": 14, "type": "四套班子",
     "context": "袁汝琴（人大主任）与张义红（政协主席）",
     "overlap_org": "永修县", "overlap_period": ""},

    # ── Yuan Li with other county leaders ──
    {"id": 15, "person_a_id": 2, "person_b_id": 4, "type": "上下级",
     "context": "袁立（代县长）与喻建华（常务副县长）为县长-副县长关系",
     "overlap_org": "永修县人民政府", "overlap_period": ""},

    {"id": 16, "person_a_id": 2, "person_b_id": 13, "type": "四套班子",
     "context": "袁立（代县长）与袁汝琴（人大主任）",
     "overlap_org": "永修县", "overlap_period": ""},

    {"id": 17, "person_a_id": 2, "person_b_id": 14, "type": "四套班子",
     "context": "袁立（代县长）与张义红（政协主席）",
     "overlap_org": "永修县", "overlap_period": ""},

    # ── Standing Committee member interconnections ──
    {"id": 18, "person_a_id": 7, "person_b_id": 5, "type": "同僚",
     "context": "余晓芳（组织部长）与赵书楼（人武部政委）均为常委",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    {"id": 19, "person_a_id": 9, "person_b_id": 6, "type": "同僚",
     "context": "李荣（政法委书记）与刘伟（纪委书记）均为常委",
     "overlap_org": "中共永修县委员会", "overlap_period": ""},

    # ── Leadership transition team ──
    {"id": 20, "person_a_id": 12, "person_b_id": 3, "type": "上下级",
     "context": "原书记秦岭与专职副书记万祥（留任）",
     "overlap_org": "中共永修县委员会", "overlap_period": "至2026-06"},

    {"id": 21, "person_a_id": 12, "person_b_id": 7, "type": "上下级",
     "context": "原书记秦岭与组织部长余晓芳（留任）",
     "overlap_org": "中共永修县委员会", "overlap_period": "至2026-06"},
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
lines.append(f'    <description>永修县领导班子工作关系网络 - {today}</description>')
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
    elif p["id"] == 12:
        color = '#E67E22'  # orange: previous party secretary
        size = 16.0
    elif p["id"] == 13:
        color = '#7a5a9a'  # purple: NPC
        size = 16.0
    elif p["id"] == 14:
        color = '#5a7a9a'  # blue-grey: PPCC
        size = 16.0
    elif p["id"] in (3,):
        color = '#2ECC71'  # green: deputy secretary
        size = 16.0
    elif p["id"] in (4, 5, 6, 7, 8, 9, 10, 11):
        color = '#95A5A6'  # grey: standing committee members
        size = 14.0
    else:
        color = '#95A5A6'  # grey: other figures
        size = 12.0

    lines.append(f'      <node id="P{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
org_colors = {
    "党委": ('#C0392B', 8.0),
    "政府": ('#2980B9', 8.0),
    "人大": ('#7a5a9a', 8.0),
    "政协": ('#5a7a9a', 8.0),
    "纪委": ('#E67E22', 8.0),
    "军事": ('#27AE60', 8.0),
}
default_org_color = ('#7F8C8D', 8.0)

for o in organizations:
    oc, osize = org_colors.get(o["type"], default_org_color)
    lines.append(f'      <node id="O{o["id"]}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'          <attvalue for="source" value=""/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(oc[1:3],16)}" g="{int(oc[3:5],16)}" b="{int(oc[5:7],16)}"/>')
    lines.append(f'        <viz:size value="{osize}"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# ── Edges: Person → Organization (worked_at) ──
lines.append('    <edges>')
edge_id = 1
for pos in positions:
    lines.append(f'      <edge id="E{edge_id}" source="P{pos["person_id"]}" target="O{pos["org_id"]}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]} ({pos["start"]} - {pos["end"]})"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"]} - {pos["end"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# ── Edges: Person ↔ Person (relationship) ──
for r in relationships:
    lines.append(f'      <edge id="E{edge_id}" source="P{r["person_a_id"]}" target="P{r["person_b_id"]}" label="{r["type"]}">')
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

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"GEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons) + len(organizations)} ({len(persons)} persons, {len(organizations)} organizations)")
print(f"  Edges: {edge_id - 1} ({len(positions)} person→org, {len(relationships)} person↔person)")
print("\nDone!")
