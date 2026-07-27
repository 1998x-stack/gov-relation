#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 永吉县, 吉林市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_永吉县
Research sources:
  - Yongji County Government Website (www.jlyj.gov.cn) — official leadership page
  - County government meeting records / news articles
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "永吉县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Committee
    # ══════════════════════════════════════════════════════════════════════════

    # 高飞 — 县委书记 (confirmed as of May 2025, latest meeting record)
    # Source: jlyj.gov.cn meeting records
    {"id": 1, "name": "高飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共永吉县委员会",
     "source": "http://www.jlyj.gov.cn/xxgk/hyxx/202505/t20250512_1266323.html",
     "notes": "Confirmed县委书记as of 2025-05. Previous meeting record 2024-12. No 2026 records found on county website."},

    # 徐兴 — 县委副书记、县长 (as of May 2026)
    {"id": 2, "name": "徐兴", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年9月", "birthplace": "", "education": "博士研究生",
     "party_join": "中共党员", "work_start": "2008年8月",
     "current_post": "县委副书记、县长", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/xz/201903/t20190311_548812.html",
     "notes": "Also serves as 吉林市冰雪试验区党工委书记、管委会主任"},

    # 滕慧阳 — 县委常委、常务副县长
    {"id": 3, "name": "滕慧阳", "gender": "男", "ethnicity": "汉族",
     "birth": "1987年4月", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "2010年7月",
     "current_post": "县委常委、副县长（常务）", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz/201903/t20190311_548815.html",
     "notes": "三级调研员"},

    # ══════════════════════════════════════════════════════════════════════════
    # County Government — Deputy Leaders
    # ══════════════════════════════════════════════════════════════════════════

    # 郭林华 — 副县长 (女)
    {"id": 4, "name": "郭林华", "gender": "女", "ethnicity": "汉族",
     "birth": "1981年12月", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "2004年9月",
     "current_post": "副县长", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz4/201903/t20190311_548826.html",
     "notes": "县政府党组成员"},

    # 刘震 — 副县长、县公安局局长
    {"id": 5, "name": "刘震", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年3月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "1991年7月",
     "current_post": "副县长、县公安局局长", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz2/202210/t20221012_1076667.html",
     "notes": "县政府党组成员"},

    # 郝大涌 — 副县长
    {"id": 6, "name": "郝大涌", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年10月", "birthplace": "", "education": "工程硕士",
     "party_join": "中共党员", "work_start": "2009年9月",
     "current_post": "副县长", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz7/202412/t20241209_1240548.html",
     "notes": "县政府党组成员"},

    # 初征 — 副县长（挂职，女，中储粮系统）
    {"id": 7, "name": "初征", "gender": "女", "ethnicity": "汉族",
     "birth": "1982年8月", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "2005年7月",
     "current_post": "副县长（挂职）", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz8/202512/t20251218_1299659.html",
     "notes": "县政府党组成员。来自中国储备粮管理集团有限公司吉林分公司"},

    # 胡昕彤 — 副县长（挂职，女，吉林出版集团）
    {"id": 8, "name": "胡昕彤", "gender": "女", "ethnicity": "汉族",
     "birth": "1989年3月", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "2011年8月",
     "current_post": "副县长（挂职）", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz9/202512/t20251218_1299660.html",
     "notes": "县政府党组成员。来自吉林东北亚出版传媒集团有限公司"},

    # 李占军 — 副县长
    {"id": 9, "name": "李占军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年9月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "1994年",
     "current_post": "副县长", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz5/201903/t20190311_548828.html",
     "notes": "永吉县本地提拔干部"},

    # 王银立 — 副县长
    {"id": 10, "name": "王银立", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年5月", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1999年7月",
     "current_post": "副县长", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/xzfld/fxz3/201903/t20190311_548824.html",
     "notes": ""},

    # ══════════════════════════════════════════════════════════════════════════
    # Other Key Leaders
    # ══════════════════════════════════════════════════════════════════════════

    # 孟庆新 — 永吉经济开发区党工委书记、管委会主任
    {"id": 11, "name": "孟庆新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永吉经济开发区党工委书记、管委会主任", "current_org": "永吉经济开发区",
     "source": "http://www.jlyj.gov.cn/xxgk/jryj/202607/t20260717_1329225.html",
     "notes": "出席2026年7月徐兴调研活动"},

    # 杨瑜春 — 县人大常委会主任
    {"id": 12, "name": "杨瑜春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "永吉县人大常委会",
     "source": "http://www.jlyj.gov.cn/xxgk/jryj/202508/t20250827_1282948.html",
     "notes": ""},

    # 滕凤臣 — 县政协主席
    {"id": 13, "name": "滕凤臣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席", "current_org": "政协永吉县委员会",
     "source": "http://www.jlyj.gov.cn/xxgk/hyxx/202412/t20241205_1239249.html",
     "notes": ""},

    # ══════════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════════

    # 朴贞玉 — 前任县委书记 (prior to 高飞)
    {"id": 14, "name": "朴贞玉", "gender": "女", "ethnicity": "朝鲜族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任县委书记", "current_org": "中共永吉县委员会",
     "source": "http://www.jlyj.gov.cn/xxgk/hyxx/",
     "notes": "前任县委书记，2024年底前由高飞接替。去向待查。朝鲜族姓名特点。"},

    # 林海策 — 前任县长 (before 徐兴)
    {"id": 15, "name": "林海策", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任县长", "current_org": "永吉县人民政府",
     "source": "http://www.jlyj.gov.cn/xxgk/hyxx/202505/t20250512_1266323.html",
     "notes": "前任县长，2025年底前由徐兴接替。去向待查。"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共永吉县委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市委", "location": "永吉县"},
    {"id": 2, "name": "永吉县人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "永吉县"},
    {"id": 3, "name": "永吉县人大常委会", "type": "人大", "level": "县处级", "parent": "吉林市人大常委会", "location": "永吉县"},
    {"id": 4, "name": "政协永吉县委员会", "type": "政协", "level": "县处级", "parent": "政协吉林市委", "location": "永吉县"},
    {"id": 5, "name": "永吉经济开发区", "type": "政府", "level": "县处级", "parent": "永吉县人民政府", "location": "永吉县"},
    {"id": 6, "name": "永吉县公安局", "type": "政府", "level": "正科级", "parent": "永吉县人民政府", "location": "永吉县"},
    {"id": 7, "name": "吉林市冰雪试验区", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "吉林市"},
    {"id": 8, "name": "中共舒兰市委", "type": "党委", "level": "县处级", "parent": "中共吉林市委", "location": "舒兰市"},
    {"id": 9, "name": "舒兰市人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "舒兰市"},
    {"id": 10, "name": "中共蛟河市委", "type": "党委", "level": "县处级", "parent": "中共吉林市委", "location": "蛟河市"},
    {"id": 11, "name": "蛟河市人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "蛟河市"},
    {"id": 12, "name": "中共桦甸市委", "type": "党委", "level": "县处级", "parent": "中共吉林市委", "location": "桦甸市"},
    {"id": 13, "name": "桦甸市人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "桦甸市"},
    {"id": 14, "name": "吉林市船营区人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "船营区"},
    {"id": 15, "name": "吉林市公安局", "type": "政府", "level": "地厅级", "parent": "吉林市人民政府", "location": "吉林市"},
    {"id": 16, "name": "吉林省委办公厅", "type": "党委", "level": "地厅级", "parent": "中共吉林省委", "location": "长春市"},
    {"id": 17, "name": "吉林省纪委监委", "type": "党委", "level": "地厅级", "parent": "中共吉林省纪委", "location": "长春市"},
    {"id": 18, "name": "吉林高新技术产业开发区", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "吉林市"},
    {"id": 19, "name": "共青团舒兰市委员会", "type": "群团", "level": "正科级", "parent": "共青团吉林市委", "location": "舒兰市"},
    {"id": 20, "name": "舒兰市朝阳镇", "type": "乡镇", "level": "乡科级", "parent": "舒兰市人民政府", "location": "舒兰市"},
    {"id": 21, "name": "中央储备粮永吉直属库有限公司", "type": "事业单位", "level": "正科级", "parent": "中储粮吉林分公司", "location": "永吉县"},
    {"id": 22, "name": "吉林东北亚出版传媒集团有限公司", "type": "事业单位", "level": "地厅级", "parent": "吉林省委宣传部", "location": "长春市"},
    {"id": 23, "name": "岔路河镇", "type": "乡镇", "level": "乡科级", "parent": "永吉县人民政府", "location": "永吉县"},
    {"id": 24, "name": "吉林中新食品区管理委员会", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "永吉县"},
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # 高飞 — 县委书记
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "2024", "end": "present",
     "rank": "县处级正职", "note": "2024年底或更早就任，2024年12月首次出现在会议记录"},

    # 徐兴 — 县长（兼任多项职务）
    {"person_id": "p2", "org_id": 2, "title": "县长", "start": "2025年11月", "end": "present",
     "rank": "县处级正职", "note": "2025年11月任代县长，后转正"},
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start": "2025年11月", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": "p2", "org_id": 7, "title": "党工委书记、管委会主任", "start": "2025", "end": "present",
     "rank": "县处级正职", "note": "兼任吉林市冰雪试验区党工委书记、管委会主任"},
    {"person_id": "p2", "org_id": 18, "title": "管委会副主任、党工委委员", "start": "2024", "end": "2025年",
     "rank": "县处级副职", "note": "吉林高新技术产业开发区"},
    {"person_id": "p2", "org_id": 17, "title": "法规室副主任、三级高级监察官", "start": "", "end": "2024",
     "rank": "县处级副职", "note": "吉林省纪委监委"},
    {"person_id": "p2", "org_id": 16, "title": "综合一处（调研室）副处长", "start": "", "end": "",
     "rank": "县处级副职", "note": "吉林省委办公厅"},
    {"person_id": "p2", "org_id": 16, "title": "综合一处（调研室）主任科员", "start": "2008年8月", "end": "",
     "rank": "正科级", "note": ""},

    # 滕慧阳 — 常务副县长
    {"person_id": "p3", "org_id": 2, "title": "县委常委、副县长（常务）", "start": "", "end": "present",
     "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": "p3", "org_id": 10, "title": "市委常委、副市长", "start": "", "end": "",
     "rank": "县处级副职", "note": "蛟河市"},
    {"person_id": "p3", "org_id": 11, "title": "副市长", "start": "", "end": "",
     "rank": "县处级副职", "note": "蛟河市"},
    {"person_id": "p3", "org_id": 20, "title": "党委书记", "start": "", "end": "",
     "rank": "乡科级正职", "note": "舒兰市朝阳镇"},
    {"person_id": "p3", "org_id": 20, "title": "党委书记、一级主任科员", "start": "", "end": "",
     "rank": "乡科级正职", "note": "舒兰市朝阳镇"},
    {"person_id": "p3", "org_id": 9, "title": "吉舒街道党工委副书记、办事处主任", "start": "", "end": "",
     "rank": "乡科级正职", "note": "舒兰经开区党工委委员"},
    {"person_id": "p3", "org_id": 19, "title": "共青团舒兰市委书记", "start": "", "end": "",
     "rank": "乡科级正职", "note": ""},

    # 郭林华 — 副县长
    {"person_id": "p4", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "县政府党组成员"},
    {"person_id": "p4", "org_id": 14, "title": "大东街道办事处党工委书记", "start": "", "end": "",
     "rank": "乡科级正职", "note": "船营区"},
    {"person_id": "p4", "org_id": 14, "title": "黄旗街道办事处主任", "start": "", "end": "",
     "rank": "乡科级正职", "note": "船营区"},
    {"person_id": "p4", "org_id": 14, "title": "青岛街道党工委副书记、纪委书记、副主任", "start": "", "end": "",
     "rank": "乡科级副职", "note": "船营区"},

    # 刘震 — 副县长、公安局长
    {"person_id": "p5", "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "县政府党组成员"},
    {"person_id": "p5", "org_id": 15, "title": "龙潭分局政委", "start": "", "end": "",
     "rank": "乡科级正职", "note": "吉林市公安局"},
    {"person_id": "p5", "org_id": 10, "title": "公安局政委", "start": "", "end": "",
     "rank": "乡科级正职", "note": "蛟河市"},
    {"person_id": "p5", "org_id": 15, "title": "龙潭分局副局长兼政治处主任", "start": "", "end": "",
     "rank": "乡科级副职", "note": "吉林市公安局"},
    {"person_id": "p5", "org_id": 15, "title": "政治部组织处副处长", "start": "", "end": "",
     "rank": "乡科级副职", "note": "吉林市公安局"},

    # 郝大涌 — 副县长
    {"person_id": "p6", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "县政府党组成员"},
    {"person_id": "p6", "org_id": 13, "title": "二道甸子镇党委书记", "start": "", "end": "",
     "rank": "乡科级正职", "note": "桦甸市"},
    {"person_id": "p6", "org_id": 13, "title": "二道甸子镇党委副书记、镇长", "start": "", "end": "",
     "rank": "乡科级正职", "note": "桦甸市"},
    {"person_id": "p6", "org_id": 12, "title": "编制综合处副处长", "start": "", "end": "",
     "rank": "乡科级副职", "note": "吉林市委编办"},

    # 初征（挂职）
    {"person_id": "p7", "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present",
     "rank": "县处级副职", "note": "中储粮系统挂职"},
    {"person_id": "p7", "org_id": 21, "title": "（中储粮永吉直属库）", "start": "", "end": "",
     "rank": "", "note": "中储粮吉林分公司多部门任职"},

    # 胡昕彤（挂职）
    {"person_id": "p8", "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present",
     "rank": "县处级副职", "note": "吉林出版集团挂职"},
    {"person_id": "p8", "org_id": 22, "title": "出版传媒部副部长", "start": "", "end": "",
     "rank": "", "note": "吉林东北亚出版传媒集团"},

    # 李占军 — 副县长
    {"person_id": "p9", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "永吉县本地提拔"},
    {"person_id": "p9", "org_id": 2, "title": "卫健局党组书记、局长", "start": "", "end": "",
     "rank": "乡科级正职", "note": "永吉县"},
    {"person_id": "p9", "org_id": 2, "title": "政府办公室主任", "start": "", "end": "",
     "rank": "乡科级正职", "note": "永吉县"},
    {"person_id": "p9", "org_id": 2, "title": "农业农村局党组书记、局长", "start": "", "end": "",
     "rank": "乡科级正职", "note": "永吉县"},
    {"person_id": "p9", "org_id": 2, "title": "林业局党组书记、局长", "start": "", "end": "",
     "rank": "乡科级正职", "note": "永吉县"},
    {"person_id": "p9", "org_id": 23, "title": "口前镇党委副书记、镇长", "start": "", "end": "",
     "rank": "乡科级正职", "note": "永吉县"},
    {"person_id": "p9", "org_id": 5, "title": "开发区管委会副主任", "start": "", "end": "",
     "rank": "乡科级副职", "note": "永吉县"},

    # 王银立 — 副县长
    {"person_id": "p10", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": "p10", "org_id": 24, "title": "党政综合办公室主任", "start": "", "end": "",
     "rank": "", "note": "吉林中新食品区"},
    {"person_id": "p10", "org_id": 24, "title": "办公室主任", "start": "", "end": "",
     "rank": "", "note": "吉林中新食品区"},
    {"person_id": "p10", "org_id": 23, "title": "武装部长", "start": "", "end": "",
     "rank": "乡科级副职", "note": "岔路河镇"},

    # 孟庆新
    {"person_id": "p11", "org_id": 5, "title": "党工委书记、管委会主任", "start": "", "end": "present",
     "rank": "县处级", "note": "永吉经济开发区"},

    # 杨瑜春
    {"person_id": "p12", "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},

    # 滕凤臣
    {"person_id": "p13", "org_id": 4, "title": "县政协主席", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},

    # 朴贞玉 — 前任县委书记
    {"person_id": "p14", "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "2024",
     "rank": "县处级正职", "note": "2024年底前离任"},

    # 林海策 — 前任县长
    {"person_id": "p15", "org_id": 2, "title": "县长（前任）", "start": "", "end": "2025年下半年",
     "rank": "县处级正职", "note": "2025年下半年离任"},
    {"person_id": "p15", "org_id": 1, "title": "县委副书记（前任）", "start": "", "end": "2025年下半年",
     "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # ===== Top Leader + Mayor =====
    {"person_a": "p1", "person_b": "p2", "type": "党政正职搭档",
     "context": "高飞（县委书记）与徐兴（县长）为2025年底后形成的新党政正职搭档",
     "overlap_org": "中共永吉县委员会/永吉县人民政府", "overlap_period": "2025-至今",
     "confidence": "confirmed"},

    # ===== 高飞 + 前任县长林海策 =====
    {"person_a": "p1", "person_b": "p15", "type": "党政正职搭档（前任）",
     "context": "高飞（县委书记）与林海策（县长）为2024-2025年搭档",
     "overlap_org": "中共永吉县委员会/永吉县人民政府", "overlap_period": "2024-2025",
     "confidence": "confirmed"},

    # ===== 徐兴 + 滕慧阳（常务副） =====
    {"person_a": "p2", "person_b": "p3", "type": "政府正副职搭档",
     "context": "徐兴（县长）与滕慧阳（常务副县长）为政府正副职搭档",
     "overlap_org": "永吉县人民政府", "overlap_period": "2025-至今",
     "confidence": "confirmed"},

    # ===== 朴贞玉 + 林海策 =====
    {"person_a": "p14", "person_b": "p15", "type": "党政正职搭档（前任）",
     "context": "朴贞玉（前任县委书记）与林海策（前任县长）曾经搭档",
     "overlap_org": "中共永吉县委员会/永吉县人民政府", "overlap_period": "2024年前",
     "confidence": "confirmed"},

    # ===== 高飞 + 滕慧阳 =====
    {"person_a": "p1", "person_b": "p3", "type": "党政协同",
     "context": "高飞（县委书记）与滕慧阳（县委常委、副县长）在常委会共事",
     "overlap_org": "中共永吉县委常委会", "overlap_period": "2024-至今",
     "confidence": "confirmed"},

    # ===== 滕慧阳 — 舒兰市经历交集（跨县关系线索） =====
    # 滕慧阳曾在舒兰市任团市委书记、朝阳镇党委书记
    # 这是跨县调动线索，但与永吉其他人在舒兰有交集尚不明确

    # ===== 滕慧阳 + 刘震 — 蛟河市经历交集 =====
    {"person_a": "p3", "person_b": "p5", "type": "地域共事（蛟河市）",
     "context": "滕慧阳曾任蛟河市副市长、市委常委、副市长；刘震曾任蛟河市公安局政委。两人不同时期在蛟河市工作",
     "overlap_org": "蛟河市", "overlap_period": "",
     "confidence": "plausible"},

    # ===== 郭林华 — 船营区经历 =====
    # 郭林华曾在船营区三个街道办事处任职

    # ===== 郝大涌 — 桦甸市经历 =====
    # 郝大涌曾在桦甸市二道甸子镇任职

    # ===== 徐兴 — 省直机关背景 =====
    # 徐兴曾在省委办公厅、省纪委监委任职，与县级成长起来的干部形成互补

    # ===== 王银立 — 岔路河镇/中新食品区本地成长 =====
]

# ── Build ──────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    # Normalize person ids: strip "p" prefix for DB
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid("p" + str(p["id"])), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and "县长" in post:
            return ("100,150,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
        "群团": ("255,220,255", 8.0),
        "乡镇": ("255,255,200", 8.0),
        "事业单位": ("220,220,220", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>永吉县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"永吉县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
