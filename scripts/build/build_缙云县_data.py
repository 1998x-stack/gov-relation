#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 缙云县 (Jinyun County), 丽水市, 浙江省.

Current officeholders as of 2026-07-27:
  - Party Secretary (县委书记): 王正飞 (Wang Zhengfei) — born 1977-03, 浙江青田
  - County Mayor (县长): 王益 (Wang Yi) — born 1976-08, 浙江丽水

Sources confirmed via:
  - Official jinyun.gov.cn news items (2026-07-27)
  - 百度百科 / 360百科 / 人民网 appointment notices
  - Government archived leadership pages (archive.org)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "zhejiang_缙云县"
STAGING = os.path.join(os.path.dirname(os.path.abspath(__file__)).rsplit("data/tmp", 1)[0], "data/tmp", TASK_ID)
DB_PATH = os.path.join(STAGING, "缙云县_network.db")
GEXF_PATH = os.path.join(STAGING, "缙云县_network.gexf")

import sqlite3
from datetime import datetime
os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# Confidence: confirmed = official source verified; plausible = credible media;
#             unverified = not yet verified
# =========================================================================
persons = [
    # ── 王正飞 — 县委书记 ──
    {
        "id": 1,
        "name": "王正飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-03",
        "birthplace": "浙江青田",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1997-10",
        "current_post": "缙云县委书记",
        "current_org": "中共缙云县委员会",
        "source": "Baidu Baike, People's Daily (zj.people.com.cn), Zhejiang Online (zjnews.zjol.com.cn)"
    },
    # ── 王益 — 县长 ──
    {
        "id": 2,
        "name": "王益",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "浙江丽水",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "1995-09",
        "current_post": "缙云县委副书记、县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn official bio (archived), 360百科"
    },
    # ── 张宗渭 — 常务副县长 ──
    {
        "id": 3,
        "name": "张宗渭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县委常委、常务副县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn leadership page, 2026-01 任前公示（拟任市直单位正职）"
    },
    # ── 朱剑成 — 县委副书记 ──
    {
        "id": 4,
        "name": "朱剑成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "浙江青田",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "1998-08",
        "current_post": "缙云县委副书记",
        "current_org": "中共缙云县委员会",
        "source": "newton.com.tw encyclopedia, jinyun.gov.cn news (2025-03-10 县十八届人大四次会议)"
    },
    # ── 赵建铭 — 人大主任 ──
    {
        "id": 5,
        "name": "赵建铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县人大常委会主任",
        "current_org": "缙云县人大常委会",
        "source": "jinyun.gov.cn (2022-02 县十八届人大一次会议 — 当选人大主任)"
    },
    # ── 付勇斐 — 政协主席 ──
    {
        "id": 6,
        "name": "付勇斐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县政协主席",
        "current_org": "中国人民政治协商会议缙云县委员会",
        "source": "jinyun.gov.cn (multiplenews items 2025-03, 2026-01 春节团拜会)"
    },
    # ── 周瑞琛 — 副县长 ──
    {
        "id": 7,
        "name": "周瑞琛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县委常委、副县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn (2022-02 县十八届人大一次会议 — elected副县长)"
    },
    # ── 童晓彬 — 纪委书记 ──
    {
        "id": 8,
        "name": "童晓彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县委常委、纪委书记、监委主任",
        "current_org": "中共缙云县纪律检查委员会",
        "source": "zjsjw.gov.cn (2022-10 article), jinyun.gov.cn (2025-03 县十八届人大四次会议)"
    },
    # ── 潘巧玲 — 组织部长 ──
    {
        "id": 9,
        "name": "潘巧玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-08",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县委常委、组织部部长",
        "current_org": "中共缙云县委组织部",
        "source": "hangzhou.com.cn news (2025-12 任前公示 — 拟任市直单位正职), 中国农业大学 news article"
    },
    # ── 李一波 — 前县委书记（2019.01-2021.11） ──
    {
        "id": 10,
        "name": "李一波",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-01",
        "birthplace": "浙江龙泉",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1991-08",
        "current_post": "丽水市委常委、宣传部部长",
        "current_org": "中共丽水市委宣传部",
        "source": "360百科, zjdpf.org.cn bio"
    },
    # ── 杨秀清 — 前县委书记（2016.11-2019.01） ──
    {
        "id": 11,
        "name": "杨秀清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-03",
        "birthplace": "浙江松阳",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任）原缙云县委书记",
        "current_org": "（已调任）",
        "source": "hotelaah.com listing; renshi.people.com.cn 任前公示"
    },
    # ── 陈帅锋 — 副县长 ──
    {
        "id": 12,
        "name": "陈帅锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县人民政府副县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn (2022-02 县十八届人大一次会议 — elected副县长)"
    },
    # ── 何海龙 — 副县长 ──
    {
        "id": 13,
        "name": "何海龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县人民政府副县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn (2022-02 县十八届人大一次会议 — elected副县长)"
    },
    # ── 楼伟明 — 副县长 ──
    {
        "id": 14,
        "name": "楼伟明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县人民政府副县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn (2022-02 县十八届人大一次会议 — elected副县长)"
    },
    # ── 张捷 — 副县长 ──
    {
        "id": 15,
        "name": "张捷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县人民政府副县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn (2022-02 县十八届人大一次会议 — elected副县长)"
    },
    # ── 邱琳 — 副县长 ──
    {
        "id": 16,
        "name": "邱琳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "缙云县人民政府副县长",
        "current_org": "缙云县人民政府",
        "source": "jinyun.gov.cn (2022-02 县十八届人大一次会议 — elected副县长)"
    },
    # ── 朱芝贵 — 前纪委书记 (2017-era) ──
    {
        "id": 17,
        "name": "朱芝贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "浙江景宁",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1992-08",
        "current_post": "（已离任缙云）",
        "current_org": "",
        "source": "zjdj.com.cn (2017 article)"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共缙云县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丽水市委",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 2,
        "name": "缙云县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "丽水市人民政府",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 3,
        "name": "缙云县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议缙云县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 5,
        "name": "缙云县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 6,
        "name": "中共缙云县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共缙云县委员会",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 7,
        "name": "中共缙云县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共缙云县委员会",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 8,
        "name": "浙江丽缙五金科技产业园管理委员会",
        "type": "开发区",
        "level": "县处级",
        "parent": "",
        "location": "浙江省丽水市缙云县"
    },
    {
        "id": 9,
        "name": "中共丽水市委宣传部",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共丽水市委",
        "location": "浙江省丽水市"
    },
    {
        "id": 10,
        "name": "景宁畲族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "丽水市人民政府",
        "location": "浙江省丽水市景宁畲族自治县"
    },
    {
        "id": 11,
        "name": "中共景宁畲族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丽水市委",
        "location": "浙江省丽水市景宁畲族自治县"
    },
    {
        "id": 12,
        "name": "中共青田县委办公室",
        "type": "党委",
        "level": "县处级",
        "parent": "中共青田县委员会",
        "location": "浙江省丽水市青田县"
    },
    {
        "id": 13,
        "name": "中共青田县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共丽水市委",
        "location": "浙江省丽水市青田县"
    },
    {
        "id": 14,
        "name": "青田县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "丽水市人民政府",
        "location": "浙江省丽水市青田县"
    },
    {
        "id": 15,
        "name": "丽水市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "浙江省人民政府",
        "location": "浙江省丽水市"
    },
    {
        "id": 16,
        "name": "丽水市林业建设发展有限公司",
        "type": "事业单位",
        "level": "",
        "parent": "",
        "location": "浙江省丽水市"
    },
    {
        "id": 17,
        "name": "青田县船寮镇政府",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "青田县人民政府",
        "location": "浙江省丽水市青田县"
    },
    {
        "id": 18,
        "name": "丽水市（原）林场",
        "type": "事业单位",
        "level": "",
        "parent": "",
        "location": "浙江省丽水市"
    },
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 王正飞 — 缙云县委书记 (2021.11-至今)
    {"person_id": 1, "org_id": 1, "title": "缙云县委书记", "start_date": "2021-11", "end_date": "", "rank": "正处级", "note": "2021.11任县委书记，此前为缙云县长"},
    {"person_id": 1, "org_id": 2, "title": "缙云县委副书记、县长", "start_date": "2019-01", "end_date": "2021-11", "rank": "正处级", "note": "2019.01任代县长，后任县长"},
    {"person_id": 1, "org_id": 1, "title": "缙云县委副书记、政法委书记", "start_date": "2016-12", "end_date": "2019-01", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "丽缙园管委会常务副主任、党工委副书记", "start_date": "2017-05", "end_date": "", "rank": "", "note": "2017.05任常务副主任"},
    {"person_id": 1, "org_id": 15, "title": "共青团丽水市委书记、青联主席", "start_date": "", "end_date": "2016-12", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "龙泉市副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "青田县委办副主任、政研室主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "青田县鹤城镇副书记、镇长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "青田县高湖镇党委书记、镇长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "青田县高湖镇党委副书记、镇长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "共青团青田县委书记、县青联主席", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "青田县高市乡党委副书记、副乡长、纪委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "青田县船寮镇政府城建办主任", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # 王益 — 缙云县长 (2022.02)
    {"person_id": 2, "org_id": 2, "title": "缙云县委副书记、县长", "start_date": "2022-02", "end_date": "", "rank": "正处级", "note": "2022.02 elected县长"},
    {"person_id": 2, "org_id": 11, "title": "景宁县委副书记、政法委书记", "start_date": "", "end_date": "2022-02", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "景宁县委常委、常务副县长", "start_date": "2016-05", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "景宁县人民政府副县长", "start_date": "2011-11", "end_date": "2016-05", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "丽水市林业建设发展有限公司总经理", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 18, "title": "丽水市（原）林场技术员、副场长", "start_date": "1995-09", "end_date": "", "rank": "", "note": "1995.09林场技术员起步"},

    # 张宗渭 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "缙云县委常委、常务副县长", "start_date": "", "end_date": "2026-01", "rank": "副处级", "note": "2026.01 拟任市直单位正职（可能已离任）"},

    # 朱剑成 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "缙云县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 赵建铭 — 人大主任
    {"person_id": 5, "org_id": 3, "title": "缙云县人大常委会主任", "start_date": "2022-02", "end_date": "", "rank": "正处级", "note": "elected at 18th NPC session"},

    # 付勇斐 — 政协主席
    {"person_id": 6, "org_id": 4, "title": "缙云县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},

    # 周瑞琛 — 副县长
    {"person_id": 7, "org_id": 2, "title": "缙云县人民政府副县长", "start_date": "2022-02", "end_date": "", "rank": "副处级", "note": ""},

    # 童晓彬 — 纪委书记
    {"person_id": 8, "org_id": 5, "title": "缙云县委常委、纪委书记、监委主任", "start_date": "2022", "end_date": "", "rank": "副处级", "note": "2022年任监委代主任"},

    # 潘巧玲 — 组织部长
    {"person_id": 9, "org_id": 6, "title": "缙云县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025.12 拟任市直单位正职"},

    # 李一波 — 前县委书记
    {"person_id": 10, "org_id": 1, "title": "缙云县委书记", "start_date": "2019-01", "end_date": "2021-11", "rank": "正处级", "note": "此前任缙云县长"},
    {"person_id": 10, "org_id": 2, "title": "缙云县委副书记、县长", "start_date": "2016-04", "end_date": "2019-01", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "丽水市委常委、宣传部部长", "start_date": "2021-11", "end_date": "", "rank": "副厅级", "note": "现任"},

    # 杨秀清 — 前县委书记
    {"person_id": 11, "org_id": 1, "title": "缙云县委书记", "start_date": "2016-11", "end_date": "2019-01", "rank": "正处级", "note": "此前任莲都区委副书记、区长"},
    {"person_id": 11, "org_id": 15, "title": "莲都区委副书记、区长", "start_date": "", "end_date": "2016-11", "rank": "正处级", "note": ""},

    # 陈帅锋 — 副县长
    {"person_id": 12, "org_id": 2, "title": "缙云县人民政府副县长", "start_date": "2022-02", "end_date": "", "rank": "副处级", "note": ""},

    # 何海龙 — 副县长
    {"person_id": 13, "org_id": 2, "title": "缙云县人民政府副县长", "start_date": "2022-02", "end_date": "", "rank": "副处级", "note": ""},

    # 楼伟明 — 副县长
    {"person_id": 14, "org_id": 2, "title": "缙云县人民政府副县长", "start_date": "2022-02", "end_date": "", "rank": "副处级", "note": ""},

    # 张捷 — 副县长
    {"person_id": 15, "org_id": 2, "title": "缙云县人民政府副县长", "start_date": "2022-02", "end_date": "", "rank": "副处级", "note": ""},

    # 邱琳 — 副县长
    {"person_id": 16, "org_id": 2, "title": "缙云县人民政府副县长", "start_date": "2022-02", "end_date": "", "rank": "副处级", "note": ""},

    # 朱芝贵 — 前纪委书记
    {"person_id": 17, "org_id": 5, "title": "缙云县委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "2017年时期任职"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王正飞 ↔ 王益 (当前搭档：书记+县长)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "书记+县长搭档（2022年底至今）", "overlap_org": "中共缙云县委员会/缙云县人民政府", "overlap_period": "2022-至今"},
    # 王正飞 ↔ 李一波 (前任书记与后任：李一波是王正飞的前任书记，王正飞是李一波的前任县长)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "李一波的前任缙云县长是王正飞→王正飞接任书记", "overlap_org": "中共缙云县委员会", "overlap_period": "2019-2021"},
    # 王正飞 ↔ 张宗渭 (书记+常务副县长的领导下属关系)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记+常务副县长工作关系", "overlap_org": "缙云县委/县政府", "overlap_period": "2022-2026年初"},
    # 王益 ↔ 张宗渭 (县长+常务副县长的紧密搭档)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长+常务副县长", "overlap_org": "缙云县人民政府", "overlap_period": "2022-2026"},
    # 朱剑成 ↔ 王正飞 (副书记+书记的班子关系)
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate", "context": "副书记+书记", "overlap_org": "中共缙云县委员会", "overlap_period": ""},
    # 王益 ↔ 李一波 (李一波是王益前任县长作用的延伸——李先任县长，王益继任)
    {"person_a": 2, "person_b": 10, "type": "predecessor_successor", "context": "李一波(2016-2019县长)→王正飞(2019-2021县长)→王益(2022至今县长)", "overlap_org": "缙云县人民政府", "overlap_period": "2022 onward succession path"},
    # 李一波 ↔ 杨秀清 (前任县委书记)
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor", "context": "杨秀清(2016-2019书记)→李一波(2019-2021书记)", "overlap_org": "中共缙云县委员会", "overlap_period": "2016-2021"},
    # 潘巧玲 ↔ 王正飞 (组织部长+书记的班子关系)
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "组织部长+书记", "overlap_org": "中共缙云县委员会", "overlap_period": ""},
    # 朱剑成 ↔ 潘巧玲 (同级委员)
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "均为县委常委", "overlap_org": "中共缙云县委员会", "overlap_period": ""},
    # 王正飞 ↔ 周瑞琛 (书记+副县长班子)
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记+副县长", "overlap_org": "中共缙云县委员会/县政府", "overlap_period": "2022-至今"},
    # 王益 ↔ 周瑞琛 (县长+副县长)
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长+副县长", "overlap_org": "缙云县人民政府", "overlap_period": "2022-至今"},
]

# =========================================================================
# BUILD
# =========================================================================
if __name__ == "__main__":
    run_build(
        slug="缙云县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"\n✅ Build complete!")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons:  {len(persons)}")
    print(f"  Orgs:     {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")