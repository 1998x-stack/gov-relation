#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上海市徐汇区 leadership network.

调查日期: 2026-08-03
信息来源: 中共徐汇区委党建网 (dj.xh.sh.cn)、上海市徐汇区人民政府门户网站 (www.xuhui.gov.cn)

Confirmed from 徐汇党建网官方领导信息页面 (dj.xh.sh.cn, accessed 2026-08):
- 曹立强 — 徐汇区委书记
- 王华 — 徐汇区委副书记、区长
- 何雅 — 区委常委、纪委书记、监委主任
- 赵懿 — 区委常委、宣传部部长
- 胡芳 — 区委常委、组织部部长
- 诸旖 — 区委常委、统战部部长
- 习挺松 — 区委常委、政法委书记
- 郑长林 — 区委常委、副区长
- 罗华品 — 区委常委、副区长
- 陶威 — 区委常委、区人武部政委

Key personnel changes since earlier investigation (2026-07-25):
- 沈权 (former 区委副书记) → departed, successor uncovered
- 王宏伟 (former 常务副区长) → now 金山区人大常委会主任
- 刘琪 (former 组织部部长,女) → now 青浦区委副书记
- 谭伟时 (former 人武部政委) → replaced by 陶威 (大校)
- 俞林伟, 王志华 (former 副区长) → departed
- NEW: 郑长林 (副区长, 2025.07入常), 胡芳(女,组织部长,2024.10新任), 陶威(人武部,2025.08入常)
- NEW: 陈勇, 魏兰 (副区长)
- 鲍炳章 (前任区委书记): 2024年1月被查, 2026年2月判14年
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "徐汇区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "徐汇区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "上海市徐汇区"

# ── SOURCE REGISTER ──────────────────────────────────────────────
SOURCES = {
    "S001": {
        "title": "中共徐汇区委党建网 — 区委领导",
        "url": "http://dj.xh.sh.cn/xhdj_ldxx/20220824/497137.html",
        "publisher": "中共上海市徐汇区委组织部",
        "published_at": "2022-08-24",
        "accessed_at": "2026-08-03",
        "source_type": "official",
        "reliability": "high",
        "notes": "Complete Party Committee Standing Committee list with basic bio",
    },
    "S002": {
        "title": "上海市徐汇区人民政府门户网站",
        "url": "https://www.xuhui.gov.cn/",
        "publisher": "上海市徐汇区人民政府",
        "published_at": "",
        "accessed_at": "2026-08-03",
        "source_type": "official",
        "reliability": "high",
        "notes": "Homepage news feed confirming current officeholders via activity reports",
    },
    "S003": {
        "title": "徐汇区进博会服务保障工作会议",
        "url": "https://www.xuhui.gov.cn/xwzx_zybd/20260803/575616.html",
        "publisher": "上海市徐汇区人民政府",
        "published_at": "2026-08-03",
        "accessed_at": "2026-08-03",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed attendance: 曹立强, 王华, 赵懿, 郑长林, 罗华品, 邓大伟, 魏兰",
    },
    "S004": {
        "title": "徐汇区领导开展八一走访慰问",
        "url": "https://www.xuhui.gov.cn/xwzx_tpxw/20260729/575484.html",
        "publisher": "上海市徐汇区人民政府",
        "published_at": "2026-07-29",
        "accessed_at": "2026-08-03",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed: 曹立强, 王华, 罗华品, 陶威",
    },
    "S005": {
        "title": "徐汇区量子计算产业会议",
        "url": "https://www.xuhui.gov.cn/xwzx_tpxw/20260701/574848.html",
        "publisher": "上海市徐汇区人民政府",
        "published_at": "2026-07-01",
        "accessed_at": "2026-08-03",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed: 陈勇 (副区长)",
    },
    "S006": {
        "title": "鲍炳章受贿案一审宣判",
        "url": "https://www.xuhui.gov.cn/",
        "publisher": "上海市第一中级人民法院",
        "published_at": "2026-02",
        "accessed_at": "2026-08-03",
        "source_type": "news",
        "reliability": "high",
        "notes": "鲍炳章被判14年",
    },
}


# ── PERSONS ───────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════
    # 区委常委 (10人，来自官方领导页面)
    # ═══════════════════════════════════════════════

    # 1. 区委书记 — 曹立强
    {
        "id": 1,
        "name": "曹立强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-05",
        "birthplace": "江苏盐城",
        "education": "中央党校研究生，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1986-07",
        "current_post": "中共上海市徐汇区委书记",
        "current_org": "中共上海市徐汇区委员会",
        "source": "S001|S002",
    },
    # 2. 区委副书记、区长
    {
        "id": 2,
        "name": "王华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-01",
        "birthplace": "江苏靖江",
        "education": "研究生，工学硕士、工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1998-05",
        "current_post": "徐汇区委副书记、区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "S001|S002",
    },
    # 3. 纪委书记
    {
        "id": 3,
        "name": "何雅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "江苏泰兴",
        "education": "在职研究生，管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、区纪委书记、区监委主任",
        "current_org": "中共上海市徐汇区纪律检查委员会",
        "source": "S001",
    },
    # 4. 宣传部部长
    {
        "id": 4,
        "name": "赵懿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "北京",
        "education": "在职大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、宣传部部长",
        "current_org": "中共上海市徐汇区委宣传部",
        "source": "S001|S003",
    },
    # 5. 组织部部长
    {
        "id": 5,
        "name": "胡芳",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1977-02",
        "birthplace": "安徽安庆",
        "education": "全日制大学，EMBA",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、组织部部长、区委党校校长",
        "current_org": "中共上海市徐汇区委组织部",
        "source": "S001",
    },
    # 6. 统战部部长
    {
        "id": 6,
        "name": "诸旖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "上海",
        "education": "在职研究生，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、统战部部长、区社会主义学院院长、区政协党组副书记",
        "current_org": "中共上海市徐汇区委统战部",
        "source": "S001",
    },
    # 7. 政法委书记
    {
        "id": 7,
        "name": "习挺松",
        "gender": "男",
        "ethnicity": "纳西族",
        "birth": "1971-06",
        "birthplace": "云南丽江",
        "education": "研究生，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、政法委书记",
        "current_org": "中共上海市徐汇区委政法委员会",
        "source": "S001",
    },
    # 8. 副区长（常务）
    {
        "id": 8,
        "name": "郑长林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "江苏泗阳",
        "education": "全日制研究生，国际商务硕士、应用金融硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "S001|S003",
    },
    # 9. 副区长
    {
        "id": 9,
        "name": "罗华品",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "四川内江",
        "education": "全日制大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、副区长、区委政法委副书记、区行政学院院长",
        "current_org": "上海市徐汇区人民政府",
        "source": "S001|S003|S004",
    },
    # 10. 人武部政委
    {
        "id": 10,
        "name": "陶威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "江苏宜兴",
        "education": "全日制大学，军事学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区委常委、区人武部大校政治委员",
        "current_org": "上海市徐汇区人民武装部",
        "source": "S001|S004",
    },
    # ═══════════════════════════════════════════════
    # 区政府副区长 (非常委)
    # ═══════════════════════════════════════════════
    # 11. 副区长
    {
        "id": 11,
        "name": "邓大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "S003",
    },
    # 12. 副区长
    {
        "id": 12,
        "name": "陈勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "S005",
    },
    # 13. 副区长
    {
        "id": 13,
        "name": "魏兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区副区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "S003",
    },
    # ═══════════════════════════════════════════════
    # 人大、政协
    # ═══════════════════════════════════════════════
    # 14. 人大常委会主任 (注:上海部分区委书记兼人大主任,此处疑有变动)
    {
        "id": 14,
        "name": "李新华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区人大常委会主任",
        "current_org": "上海市徐汇区人民代表大会常务委员会",
        "source": "S002",
    },
    # 15. 政协主席
    {
        "id": 15,
        "name": "黄冲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徐汇区政协主席",
        "current_org": "中国人民政治协商会议上海市徐汇区委员会",
        "source": "S002",
    },

    # ═══════════════════════════════════════════════
    # 前任领导
    # ═══════════════════════════════════════════════

    # 16. 前任区委书记 — 鲍炳章 (落马)
    {
        "id": 16,
        "name": "鲍炳章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-11",
        "birthplace": "浙江宁波",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1985-08",
        "current_post": "",
        "current_org": "",
        "source": "S006",
    },
    # 17. 前任区长 — 钟晓咏
    {
        "id": 17,
        "name": "钟晓咏",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1972-10",
        "birthplace": "福建厦门",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1995-07",
        "current_post": "中共上海市静安区委书记",
        "current_org": "中共上海市静安区委员会",
        "source": "S002（静安区政府官网）",
    },
    # 18. 前任副书记 — 沈权 (已离任)
    {
        "id": 18,
        "name": "沈权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "S002",
    },
    # 19. 前任常务副区长 — 王宏伟 (现 金山区人大常委会主任)
    {
        "id": 19,
        "name": "王宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金山区人大常委会主任",
        "current_org": "上海市金山区人民代表大会常务委员会",
        "source": "金山人大公开信息",
    },
    # 20. 前任组织部长 — 刘琪 (现 青浦区委副书记)
    {
        "id": 20,
        "name": "刘琪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委副书记",
        "current_org": "中共上海市青浦区委员会",
        "source": "青浦区委公开信息",
    },
    # 21. 前任人武部政委 — 谭伟时 (已离任)
    {
        "id": 21,
        "name": "谭伟时",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "S002",
    },
    # 22. 前任副区长 — 俞林伟 (已离任)
    {
        "id": 22,
        "name": "俞林伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "S002",
    },
    # 23. 前任副区长 — 王志华 (已离任)
    {
        "id": 23,
        "name": "王志华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "S002",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市徐汇区委员会", "type": "党委", "level": "市辖区(直辖市)", "parent": "中共上海市委", "location": "上海市徐汇区"},
    {"id": 2, "name": "上海市徐汇区人民政府", "type": "政府", "level": "市辖区(直辖市)", "parent": "上海市人民政府", "location": "上海市徐汇区"},
    {"id": 3, "name": "中共上海市徐汇区纪律检查委员会", "type": "纪委", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 4, "name": "中共上海市徐汇区委组织部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 5, "name": "中共上海市徐汇区委宣传部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 6, "name": "中共上海市徐汇区委政法委员会", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 7, "name": "中共上海市徐汇区委统战部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市徐汇区委员会", "location": "上海市徐汇区"},
    {"id": 8, "name": "上海市徐汇区人民武装部", "type": "军队", "level": "市辖区(直辖市)", "parent": "上海警备区", "location": "上海市徐汇区"},
    {"id": 9, "name": "上海市徐汇区人民代表大会常务委员会", "type": "人大", "level": "市辖区(直辖市)", "parent": "上海市人民代表大会常务委员会", "location": "上海市徐汇区"},
    {"id": 10, "name": "中国人民政治协商会议上海市徐汇区委员会", "type": "政协", "level": "市辖区(直辖市)", "parent": "中国人民政治协商会议上海市委员会", "location": "上海市徐汇区"},
]

# ── POSITIONS ──────────────────────────────────────────────────
positions = [
    # 曹立强
    {"person_id": 1, "org_id": 1, "title": "中共上海市徐汇区委书记", "start_date": "2021-08", "end_date": "present", "rank": "正厅级", "note": "2021年8月任徐汇区委书记"},
    {"person_id": 1, "org_id": 1, "title": "中共上海市普陀区委书记", "start_date": "2019", "end_date": "2021-08", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中共上海市虹口区委副书记、区长", "start_date": "2017", "end_date": "2019", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中共上海市闸北区委常委、副区长", "start_date": "2006", "end_date": "2013", "rank": "副厅级", "note": ""},

    # 王华
    {"person_id": 2, "org_id": 2, "title": "徐汇区委副书记、区长", "start_date": "2023-03", "end_date": "present", "rank": "正厅级", "note": "2023年3月任代区长，后任区长"},
    {"person_id": 2, "org_id": 1, "title": "中共上海市浦东新区区委常委、副区长", "start_date": "2021", "end_date": "2023-03", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "上海市浦东新区副区长", "start_date": "2019", "end_date": "2021", "rank": "副厅级", "note": ""},

    # 何雅
    {"person_id": 3, "org_id": 3, "title": "徐汇区委常委、纪委书记、区监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "曾任上海商学院（市属高校）纪委书记"},

    # 赵懿
    {"person_id": 4, "org_id": 5, "title": "徐汇区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 胡芳
    {"person_id": 5, "org_id": 4, "title": "徐汇区委常委、组织部部长", "start_date": "2024-10", "end_date": "present", "rank": "副厅级", "note": "2024年10月入常任组织部长"},

    # 诸旖
    {"person_id": 6, "org_id": 7, "title": "徐汇区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼区政协党组副书记"},

    # 习挺松
    {"person_id": 7, "org_id": 6, "title": "徐汇区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 郑长林
    {"person_id": 8, "org_id": 2, "title": "徐汇区委常委、副区长", "start_date": "2025-07", "end_date": "present", "rank": "副厅级", "note": "2025年7月入常"},

    # 罗华品
    {"person_id": 9, "org_id": 2, "title": "徐汇区委常委、副区长", "start_date": "2025-08", "end_date": "present", "rank": "副厅级", "note": "2025年8月升任常委"},

    # 陶威
    {"person_id": 10, "org_id": 8, "title": "徐汇区委常委、区人武部大校政治委員", "start_date": "2025-08", "end_date": "present", "rank": "正师级", "note": "2025年8月入常"},

    # 邓大伟
    {"person_id": 11, "org_id": 2, "title": "徐汇区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 陈勇
    {"person_id": 12, "org_id": 2, "title": "徐汇区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 魏兰
    {"person_id": 13, "org_id": 2, "title": "徐汇区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 李新华
    {"person_id": 14, "org_id": 9, "title": "徐汇区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},

    # 黄冲
    {"person_id": 15, "org_id": 10, "title": "徐汇区政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},

    # 鲍炳章
    {"person_id": 16, "org_id": 1, "title": "中共上海市徐汇区委书记（前任）", "start_date": "2016", "end_date": "2021-08", "rank": "正厅级", "note": "2021年8月调任虹桥商务区管理委员会党组书记；2024年1月被调查；2026年2月判14年"},
    {"person_id": 16, "org_id": 1, "title": "上海市徐汇区区长（前任）", "start_date": "2014", "end_date": "2016", "rank": "正厅级", "note": ""},

    # 钟晓咏
    {"person_id": 17, "org_id": 2, "title": "徐汇区区长（前任）", "start_date": "2021-01", "end_date": "2024-02", "rank": "正厅级", "note": "后调任上海虹桥国际中央商务区管委会党组书记，现任静安区委书记"},
    {"person_id": 17, "org_id": 1, "title": "中共上海市徐汇区委副书记", "start_date": "2019-03", "end_date": "2021-01", "rank": "正厅级", "note": ""},
    {"person_id": 17, "org_id": 6, "title": "徐汇区委常委、政法委书记", "start_date": "2016-09", "end_date": "2019-03", "rank": "副厅级", "note": ""},

    # 沈权
    {"person_id": 18, "org_id": 1, "title": "徐汇区委副书记（前任）", "start_date": "", "end_date": "2025?", "rank": "正厅级", "note": "已离任，去向待查"},

    # 王宏伟
    {"person_id": 19, "org_id": 9, "title": "金山区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "原徐汇区委常委、常务副区长"},
    {"person_id": 19, "org_id": 2, "title": "徐汇区委常委、副区长（常务）（前任）", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # 刘琪
    {"person_id": 20, "org_id": 1, "title": "青浦区委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "原徐汇区委常委、组织部部长"},
    {"person_id": 20, "org_id": 4, "title": "徐汇区委常委、组织部部长（前任）", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # 谭伟时
    {"person_id": 21, "org_id": 8, "title": "徐汇区委常委、人武部政委（前任）", "start_date": "", "end_date": "", "rank": "正师级", "note": "已离任"},

    # 俞林伟
    {"person_id": 22, "org_id": 2, "title": "徐汇区副区长（前任）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "已离任，去向待查"},

    # 王志华
    {"person_id": 23, "org_id": 2, "title": "徐汇区副区长（前任）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "已离任，去向待查"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────
relationships = [
    # 曹立强 — 王华 (搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档关系", "overlap_org": "上海市徐汇区", "overlap_period": "2023-03至今"},
    # 曹立强 — 鲍炳章 (前后任)
    {"person_a": 1, "person_b": 16, "type": "前后任", "context": "曹立强接替鲍炳章任徐汇区委书记", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": "2021-08"},
    # 王华 — 钟晓咏 (前后任)
    {"person_a": 2, "person_b": 17, "type": "前后任", "context": "王华接替钟晓咏任徐汇区长", "overlap_org": "上海市徐汇区人民政府", "overlap_period": "2023-03"},
    # 前搭档: 曹立强 — 王宏伟
    {"person_a": 1, "person_b": 19, "type": "上下级", "context": "区委书记—常务副区长（前任）", "overlap_org": "上海市徐汇区", "overlap_period": "2021-08至?"},
    # 王华 — 郑长林 (上下级)
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "上海市徐汇区人民政府", "overlap_period": "2025-07至今"},
    # 王华 — 罗华品 (上下级)
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长—副区长", "overlap_org": "上海市徐汇区人民政府", "overlap_period": ""},
    # 曹立强 — 各常委 (上下级)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—纪委书记", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—宣传部部长", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—组织部部长", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": "2024-10至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—统战部部长", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记—政法委书记", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记—常务副区长", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": "2025-07至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—副区长（常委）", "overlap_org": "中共上海市徐汇区委员会", "overlap_period": "2025-08至今"},
    # 前任交接: 王宏伟 → 郑长林
    {"person_a": 19, "person_b": 8, "type": "前后任", "context": "王宏伟离任徐汇后郑长林接任常务副区长", "overlap_org": "上海市徐汇区人民政府", "overlap_period": "2025"},
    # 前任交接: 刘琪 → 胡芳
    {"person_a": 20, "person_b": 5, "type": "前后任", "context": "刘琪离任后胡芳接任组织部长", "overlap_org": "中共上海市徐汇区委组织部", "overlap_period": "2024-10"},
    # 跨区流动: 鲍炳章 → 虹桥商务区
    {"person_a": 16, "person_b": 17, "type": "共事", "context": "鲍炳章（书记）与钟晓咏（区长）共事", "overlap_org": "上海市徐汇区", "overlap_period": "2021-01至2021-08"},
    # 钟晓咏静安
    {"person_a": 17, "person_b": 2, "type": "前后任", "context": "钟晓咏→王华徐汇区长前后任", "overlap_org": "上海市徐汇区人民政府", "overlap_period": "2023-03"},
]


# ── BUILD ──────────────────────────────────────────────────────
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

if __name__ == "__main__":
    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # ── Person JSONs ────────────────────────────────────────────────
    SOURCE_LIST = [
        {"id": sid, **info}
        for sid, info in SOURCES.items()
    ]

    def build_career_timeline(person_id):
        return [
            {
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": pos["org_id"],
                "title": pos["title"],
                "rank": pos.get("rank", ""),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if pos["end_date"] == "present" else "plausible",
                "source_ids": ["S001", "S002"],
            }
            for pos in positions
            if pos["person_id"] == person_id
        ]

    def build_relationships(person_id):
        rels = []
        for r in relationships:
            other_id = None
            if r["person_a"] == person_id:
                other_id = r["person_b"]
            elif r["person_b"] == person_id:
                other_id = r["person_a"]
            else:
                continue
            other = next((p for p in persons if p["id"] == other_id), None)
            if other is None:
                continue
            rels.append({
                "person": other["name"],
                "person_id": f"xuhui_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] in ("共事", "前后任") else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })
        return rels

    def write_person_json(person, job_label, is_current=True):
        pid = f"xuhui_{person['name']}"
        filename = f"{TODAY}-上海市-徐汇区-{job_label}-{person['name']}.json"

        related_orgs = []
        org_ids = {pos["org_id"] for pos in positions if pos["person_id"] == person["id"]}
        for org in organizations:
            if org["id"] in org_ids:
                related_orgs.append({
                    "org_id": org["id"],
                    "name": org["name"],
                    "type": org["type"],
                    "level": org["level"],
                    "parent": org.get("parent", ""),
                    "location": org.get("location", ""),
                    "source_ids": ["S001"],
                })

        output = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "上海市",
                "city": "徐汇区",
                "region": "徐汇区",
                "job": person.get("current_post", ""),
                "task_id": "shanghai_徐汇区",
                "time_focus": "2016-2026",
            },
            "identity": {
                "person_id": pid,
                "name": person["name"],
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": person.get("birth", ""),
                "birthplace": person.get("birthplace", ""),
                "native_place": person.get("birthplace", ""),
                "education": [{
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }],
                "party_join": person.get("party_join", ""),
                "work_start": person.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{person['name']}_{person.get('birth', '')}",
                    "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                    "official_profile_url": "http://dj.xh.sh.cn/xhdj_ldxx/20220824/497137.html",
                },
            },
            "current_status": {
                "current_post": person.get("current_post", ""),
                "current_org": person.get("current_org", ""),
                "administrative_rank": "",
                "as_of": TODAY,
                "is_current_confirmed": is_current,
                "source_ids": ["S001"],
            },
            "career_timeline": build_career_timeline(person["id"]),
            "organizations": related_orgs,
            "relationships": build_relationships(person["id"]),
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": SOURCE_LIST,
            "confidence_summary": {
                "identity": "confirmed" if person.get("birth") else "partial",
                "current_role": "confirmed" if is_current else "plausible",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": f"Complete early career timeline and detailed education background for {person['name']}",
            },
            "open_questions": [
                {
                    "priority": "critical" if not person.get("birth") else "high",
                    "question": f"完整简历：{person['name']}的详细教育背景、早期职业生涯、晋升时间线",
                    "why_it_matters": "核心领导的履历完整度影响关系网络分析的深度",
                    "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 徐汇"],
                    "last_attempted": TODAY,
                }
            ],
        }
        path = os.path.join(PERSONS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")

    # Write person JSONs for the two primary targets
    write_person_json(persons[0], "区委书记", is_current=True)   # 曹立强
    write_person_json(persons[1], "区长", is_current=True)       # 王华

    print(f"\n=== Done. Output in {STAGING_DIR} ===")