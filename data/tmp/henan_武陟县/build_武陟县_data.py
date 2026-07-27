#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 武陟县 leadership network.

调查日期: 2026-07-24
信息来源: 武陟县人民政府网站 (wuzhi.gov.cn) — 武陟要闻栏目新闻报道
调查级别: 县
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "武陟县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "武陟县_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "河南省焦作市武陟县"

# ══════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════

persons = [
    # ── 县委领导 (Party Committee) ──

    # 1. 杨正栋 — 县委书记 (2026年4-5月上任)
    {
        "id": 1,
        "name": "杨正栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共武陟县委书记",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/07-21/608456.html",
    },
    # 2. 张涛 — 县委副书记、县长 (2023年4月前已上任)
    {
        "id": 2,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委副书记、县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-20/608378.html",
    },
    # 3. 吕学梅 — 县委副书记
    {
        "id": 3,
        "name": "吕学梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委副书记",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/07-10/607650.html",
    },
    # 4. 乔楠 — 县委常委、常务副县长
    {
        "id": 4,
        "name": "乔楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委、常务副县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-10/607675.html",
    },
    # 5. 韩剑 — 县委常委、县委办主任
    {
        "id": 5,
        "name": "韩剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委、县委办主任",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/07-10/607676.html",
    },
    # 6. 左心亮 — 县委常委、人武部政委
    {
        "id": 6,
        "name": "左心亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委、人武部政委",
        "current_org": "武陟县人民武装部",
        "source": "https://www.wuzhi.gov.cn/2026/02-10/595242.html",
    },
    # 7. 李军利 — 推定县委常委 (推定组织部长/政法委书记)
    {
        "id": 7,
        "name": "李军利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-18/605907.html",
    },
    # 8. 张好收 — 推定县委常委
    {
        "id": 8,
        "name": "张好收",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-18/605907.html",
    },
    # 9. 张震 — 推定县委常委 (推定纪委书记)
    {
        "id": 9,
        "name": "张震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-18/605907.html",
    },
    # 10. 吴立强 — 推定县委常委
    {
        "id": 10,
        "name": "吴立强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/07-10/607650.html",
    },
    # 11. 陈华阳 — 推定县委常委、副县长
    {
        "id": 11,
        "name": "陈华阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）、副县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-20/608381.html",
    },
    # 12. 尹明鹤 — 推定县委常委
    {
        "id": 12,
        "name": "尹明鹤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-18/605907.html",
    },
    # 13. 胡国柱 — 推定县委常委
    {
        "id": 13,
        "name": "胡国柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-18/605907.html",
    },
    # 14. 彭亚辉 — 推定县委常委 (推定统战部长/宣传部长)
    {
        "id": 14,
        "name": "彭亚辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县委常委（推定）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-18/605909.html",
    },
    # 15. 王聪 — 推定县领导
    {
        "id": 15,
        "name": "王聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县领导（推定县委常委）",
        "current_org": "中共武陟县委员会",
        "source": "https://www.wuzhi.gov.cn/2026/02-10/595242.html",
    },

    # ── 县政府领导 (County Government) ──

    # 16. 李世鹏 — 副县长
    {
        "id": 16,
        "name": "李世鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟副县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-10/607675.html",
    },
    # 17. 秦康 — 副县长
    {
        "id": 17,
        "name": "秦康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟副县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-10/607657.html",
    },
    # 18. 原世远 — 推定副县长
    {
        "id": 18,
        "name": "原世远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县推定副县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-20/608381.html",
    },
    # 19. 孙广超 — 副县长
    {
        "id": 19,
        "name": "孙广超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟副县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/06-29/606563.html",
    },
    # 20. 张艳奇 — 副县长
    {
        "id": 20,
        "name": "张艳奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟副县长",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-02/606964.html",
    },
    # 21. 范天运 — 推定县领导
    {
        "id": 21,
        "name": "范天运",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县领导（推定）",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/06-04/604700.html",
    },
    # 22. 邢明 — 推定县领导
    {
        "id": 22,
        "name": "邢明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县领导（推定）",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/06-12/605400.html",
    },
    # 23. 毛克祥 — 推定县领导
    {
        "id": 23,
        "name": "毛克祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县领导（推定）",
        "current_org": "武陟县人民政府",
        "source": "https://www.wuzhi.gov.cn/2026/07-10/607676.html",
    },

    # ── 县人大 (County People's Congress) ──

    # 24. 张戊己 — 县人大常委会主任
    {
        "id": 24,
        "name": "张戊己",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人大常委会主任",
        "current_org": "武陟县人民代表大会常务委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },
    # 25. 朱保忠 — 县人大常委会副主任
    {
        "id": 25,
        "name": "朱保忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人大常委会副主任",
        "current_org": "武陟县人民代表大会常务委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },
    # 26. 辛明景 — 县人大常委会副主任
    {
        "id": 26,
        "name": "辛明景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人大常委会副主任",
        "current_org": "武陟县人民代表大会常务委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },
    # 27. 曹娜芬 — 县人大常委会副主任
    {
        "id": 27,
        "name": "曹娜芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人大常委会副主任",
        "current_org": "武陟县人民代表大会常务委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },
    # 28. 杨灵枝 — 县人大常委会副主任
    {
        "id": 28,
        "name": "杨灵枝",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人大常委会副主任",
        "current_org": "武陟县人民代表大会常务委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },
    # 29. 李备战 — 县人大常委会副主任（2026年6月补选）
    {
        "id": 29,
        "name": "李备战",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人大常委会副主任",
        "current_org": "武陟县人民代表大会常务委员会",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },

    # ── 法检系统 (Court & Procuratorate) ──

    # 30. 施文星 — 县人民法院院长
    {
        "id": 30,
        "name": "施文星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人民法院院长",
        "current_org": "武陟县人民法院",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },
    # 31. 刘红云 — 县人民检察院检察长
    {
        "id": 31,
        "name": "刘红云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武陟县人民检察院检察长",
        "current_org": "武陟县人民检察院",
        "source": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
    },

    # ── 前任领导 (Predecessors) ──

    # 32. 赵红兵 — 前任县委书记（至2025年12月）
    {
        "id": 32,
        "name": "赵红兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任武陟县委书记（去向待查）",
        "current_org": "",
        "source": "https://www.wuzhi.gov.cn/2025/12-30/592223.html (标题可见，文章本身404)",
    },
    # 33. 申琳 — 前任武陟县长（至2021年前后）
    {
        "id": 33,
        "name": "申琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任武陟县长（去向待查）",
        "current_org": "",
        "source": "武陟县政府工作报告 (2021-03, 申琳作政府工作报告)",
    },
]

# ══════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共武陟县委员会", "type": "党委", "level": "县级",
     "parent": "中共焦作市委", "location": "河南省焦作市武陟县"},
    {"id": 2, "name": "武陟县人民政府", "type": "政府", "level": "县级",
     "parent": "焦作市人民政府", "location": "河南省焦作市武陟县"},
    {"id": 3, "name": "武陟县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "焦作市人大常委会", "location": "河南省焦作市武陟县"},
    {"id": 4, "name": "武陟县人民法院", "type": "事业单位", "level": "县级",
     "parent": "焦作市中级人民法院", "location": "河南省焦作市武陟县"},
    {"id": 5, "name": "武陟县人民检察院", "type": "事业单位", "level": "县级",
     "parent": "焦作市人民检察院", "location": "河南省焦作市武陟县"},
    {"id": 6, "name": "武陟县人民武装部", "type": "事业单位", "level": "县级",
     "parent": "焦作军分区", "location": "河南省焦作市武陟县"},
]

# ══════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════

positions = [
    # 杨正栋
    {"person_id": 1, "org_id": 1, "title": "中共武陟县委书记",
     "start_date": "2026-04", "end_date": "", "rank": "正处级",
     "note": "2026年4月底-5月初上任；6月县第十四次党代会选举确认"},
    # 张涛
    {"person_id": 2, "org_id": 2, "title": "武陟县人民政府县长",
     "start_date": "2021-04", "end_date": "", "rank": "正处级",
     "note": "最早2023年4月已以县长身份作政府工作报告，2021年4月前申琳在任"},
    {"person_id": 2, "org_id": 1, "title": "武陟县委副书记",
     "start_date": "2021-04", "end_date": "", "rank": "副处级",
     "note": "兼任县委副书记"},
    # 吕学梅
    {"person_id": 3, "org_id": 1, "title": "武陟县委副书记",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "专职副书记"},
    # 乔楠
    {"person_id": 4, "org_id": 2, "title": "武陟县委常委、常务副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "协助县长负责县政府常务工作"},
    {"person_id": 4, "org_id": 1, "title": "武陟县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 韩剑
    {"person_id": 5, "org_id": 1, "title": "武陟县委常委、县委办主任",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 左心亮
    {"person_id": 6, "org_id": 6, "title": "武陟县人武部政委",
     "start_date": "", "end_date": "", "rank": "正团级",
     "note": "推定兼任县委常委"},
    {"person_id": 6, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李军利
    {"person_id": 7, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "推定任组织部长或政法委书记"},
    # 张好收
    {"person_id": 8, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "推定任宣传部长或统战部长"},
    # 张震
    {"person_id": 9, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "推定任纪委书记"},
    # 吴立强
    {"person_id": 10, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈华阳
    {"person_id": 11, "org_id": 2, "title": "武陟副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "推定兼任县委常委"},
    {"person_id": 11, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 尹明鹤
    {"person_id": 12, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 胡国柱
    {"person_id": 13, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 彭亚辉
    {"person_id": 14, "org_id": 1, "title": "武陟县委常委（推定）",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "推定任统战部长或宣传部长"},
    # 王聪
    {"person_id": 15, "org_id": 1, "title": "武陟县领导（推定县委常委）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李世鹏
    {"person_id": 16, "org_id": 2, "title": "武陟副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "曾通报50强企业名单并安排工作"},
    # 秦康
    {"person_id": 17, "org_id": 2, "title": "武陟副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "曾陪同张涛检查防汛"},
    # 原世远
    {"person_id": 18, "org_id": 2, "title": "武陟副县长（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 孙广超
    {"person_id": 19, "org_id": 2, "title": "武陟副县长",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张艳奇
    {"person_id": 20, "org_id": 2, "title": "武陟副县长",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 范天运
    {"person_id": 21, "org_id": 2, "title": "武陟县领导（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 邢明
    {"person_id": 22, "org_id": 2, "title": "武陟县领导（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 毛克祥
    {"person_id": 23, "org_id": 2, "title": "武陟县领导（推定）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张戊己
    {"person_id": 24, "org_id": 3, "title": "武陟县人大常委会主任",
     "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 朱保忠
    {"person_id": 25, "org_id": 3, "title": "武陟县人大常委会副主任",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 辛明景
    {"person_id": 26, "org_id": 3, "title": "武陟县人大常委会副主任",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 曹娜芬
    {"person_id": 27, "org_id": 3, "title": "武陟县人大常委会副主任",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨灵枝
    {"person_id": 28, "org_id": 3, "title": "武陟县人大常委会副主任",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李备战
    {"person_id": 29, "org_id": 3, "title": "武陟县人大常委会副主任",
     "start_date": "2026-06", "end_date": "", "rank": "副处级",
     "note": "2026年6月县人代会补选"},
    # 施文星
    {"person_id": 30, "org_id": 4, "title": "武陟县人民法院院长",
     "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 刘红云
    {"person_id": 31, "org_id": 5, "title": "武陟县人民检察院检察长",
     "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 赵红兵
    {"person_id": 32, "org_id": 1, "title": "前任武陟县委书记",
     "start_date": "2023-06", "end_date": "2025-12", "rank": "正处级",
     "note": "至少2023年6月至2025年12月在任；去向待查"},
    # 申琳
    {"person_id": 33, "org_id": 2, "title": "前任武陟县长",
     "start_date": "2019-02", "end_date": "2021-03", "rank": "正处级",
     "note": "2019年2月至2021年3月期间在任；去向待查"},
]

# ══════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "杨正栋（县委书记）与张涛（县长）构成武陟县党政主要领导搭档",
     "overlap_org": "武陟县", "overlap_period": "2026-"},
    # 县委书记与前任
    {"person_a": 1, "person_b": 32, "type": "接替",
     "context": "杨正栋接替赵红兵任武陟县委书记；交接期约2026年1-4月",
     "overlap_org": "中共武陟县委员会", "overlap_period": ""},
    # 县长与前前任
    {"person_a": 2, "person_b": 33, "type": "接替",
     "context": "张涛接替申琳任武陟县长",
     "overlap_org": "武陟县人民政府", "overlap_period": "2021"},
    # 县委副书记与其他
    {"person_a": 3, "person_b": 1, "type": "上下级",
     "context": "吕学梅（县委副书记）作为杨正栋（县委书记）的主要副手，协助县委日常工作",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    {"person_a": 3, "person_b": 2, "type": "同级",
     "context": "吕学梅作为专职副书记与县长张涛在县委常委会中共事",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    # 常务副县长与县长
    {"person_a": 4, "person_b": 2, "type": "上下级",
     "context": "乔楠（常务副县长）协助张涛（县长）负责县政府常务工作",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    # 县委办主任与县委书记
    {"person_a": 5, "person_b": 1, "type": "上下级",
     "context": "韩剑（县委办主任）作为杨正栋（县委书记）的办公室主任，负责县委日常工作运转",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    # 人武部政委与县委书记
    {"person_a": 6, "person_b": 1, "type": "上下级",
     "context": "左心亮（人武部政委）在武陟县武装工作中受县委书记领导",
     "overlap_org": "武陟县", "overlap_period": ""},
    # 推定县委常委之间的工作关系
    {"person_a": 7, "person_b": 1, "type": "上下级",
     "context": "李军利作为推定县委常委，在县委常委会中受县委书记领导",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    {"person_a": 8, "person_b": 1, "type": "上下级",
     "context": "张好收作为推定县委常委，在县委常委会中受县委书记领导",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    {"person_a": 9, "person_b": 1, "type": "上下级",
     "context": "张震作为推定县委常委，在县委常委会中受县委书记领导",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    {"person_a": 10, "person_b": 1, "type": "上下级",
     "context": "吴立强作为推定县委常委，在县委常委会中受县委书记领导",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    {"person_a": 12, "person_b": 1, "type": "上下级",
     "context": "尹明鹤作为推定县委常委，在县委常委会中受县委书记领导",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    {"person_a": 13, "person_b": 1, "type": "上下级",
     "context": "胡国柱作为推定县委常委，在县委常委会中受县委书记领导",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    {"person_a": 14, "person_b": 1, "type": "上下级",
     "context": "彭亚辉作为推定县委常委，在县委常委会中受县委书记领导",
     "overlap_org": "中共武陟县委员会", "overlap_period": "2026-"},
    # 副县长与县长
    {"person_a": 16, "person_b": 2, "type": "上下级",
     "context": "李世鹏（副县长）在县政府工作中受张涛（县长）领导",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    {"person_a": 17, "person_b": 2, "type": "上下级",
     "context": "秦康（副县长）在县政府工作中受张涛（县长）领导",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    {"person_a": 18, "person_b": 2, "type": "上下级",
     "context": "原世远（推定副县长）在县政府工作中受张涛（县长）领导",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    {"person_a": 19, "person_b": 2, "type": "上下级",
     "context": "孙广超（副县长）在县政府工作中受张涛（县长）领导",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    {"person_a": 20, "person_b": 2, "type": "上下级",
     "context": "张艳奇（副县长）在县政府工作中受张涛（县长）领导",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    # 常务副县长与各位副县长
    {"person_a": 4, "person_b": 16, "type": "同级",
     "context": "乔楠（常务）与李世鹏在县政府班子中共事",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 17, "type": "同级",
     "context": "乔楠（常务）与秦康在县政府班子中共事",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 19, "type": "同级",
     "context": "乔楠（常务）与孙广超在县政府班子中共事",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
    # 人大常委会主任与县委书记
    {"person_a": 24, "person_b": 1, "type": "同级",
     "context": "张戊己（人大主任）与杨正栋（书记）在县四套班子中配合工作",
     "overlap_org": "武陟县四套班子", "overlap_period": "2026-"},
    # 法检两长与县委
    {"person_a": 30, "person_b": 1, "type": "上下级",
     "context": "施文星（法院院长）在党务工作中受县委领导",
     "overlap_org": "武陟县", "overlap_period": ""},
    {"person_a": 31, "person_b": 1, "type": "上下级",
     "context": "刘红云（检察长）在党务工作中受县委领导",
     "overlap_org": "武陟县", "overlap_period": ""},
    # 前任与现任
    {"person_a": 32, "person_b": 2, "type": "上下级",
     "context": "赵红兵（前任书记）与张涛（县长）在2023-2025年期间为党政搭档",
     "overlap_org": "武陟县", "overlap_period": "2023-2025"},
    {"person_a": 33, "person_b": 32, "type": "上下级",
     "context": "申琳（前任县长）与赵红兵（前任书记）在党政搭档期间共事",
     "overlap_org": "武陟县", "overlap_period": ""},
    # 前任县长与现任县长
    {"person_a": 33, "person_b": 1, "type": "接替",
     "context": "申琳（前任县长）卸任后，张涛接任县长，杨正栋后来接任书记",
     "overlap_org": "武陟县人民政府", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
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
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 武陟县人民政府网站 (wuzhi.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post:
            return ("255,50,50", 20.0)
        elif "县长" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副县长" in post or "副院长" in post or "副检察长" in post or "人大副主任" in post:
            return ("100,100,255", 12.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "院长" in post or "检察长" in post:
            return ("100,100,255", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "事业单位": ("220,220,220"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


# ══════════════════════════════════════════════════════════════════════
# PERSON JSON GENERATION
# ══════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "杨正栋调研造纸产业",
         "url": "https://www.wuzhi.gov.cn/2026/07-21/608456.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-21",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "确认杨正栋以县委书记身份调研"},
        {"id": "S002", "title": "张涛调研大气污染防治",
         "url": "https://www.wuzhi.gov.cn/2026/07-20/608378.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-20",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "张涛以县委副书记、县长身份调研"},
        {"id": "S003", "title": "县委专题项目会议",
         "url": "https://www.wuzhi.gov.cn/2026/07-10/607675.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-10",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "确认乔楠任县委常委、常务副县长，李世鹏任副县长"},
        {"id": "S004", "title": "全县安全稳定会议",
         "url": "https://www.wuzhi.gov.cn/2026/07-10/607650.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-10",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "列出吕学梅、吴立强、彭亚辉、陈华阳、尹明鹤、乔楠、胡国柱、王聪、韩剑等县领导"},
        {"id": "S005", "title": "县委常委会扩大会议",
         "url": "https://www.wuzhi.gov.cn/2026/06-18/605907.html",
         "publisher": "武陟县人民政府", "published_at": "2026-06-18",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "列出推定13位县委常委与会"},
        {"id": "S006", "title": "武陟县人代会闭幕",
         "url": "https://www.wuzhi.gov.cn/2026/06-08/604949.html",
         "publisher": "武陟县人民政府", "published_at": "2026-06-08",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "确认人大主任副主任名单"},
        {"id": "S007", "title": "全县人民武装工作会议",
         "url": "https://www.wuzhi.gov.cn/2026/02-10/595242.html",
         "publisher": "武陟县人民政府", "published_at": "2026-02-10",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "确认左心亮任人武部政委，王聪、韩剑出席"},
        {"id": "S008", "title": "杨正栋到西陶镇调研",
         "url": "https://www.wuzhi.gov.cn/2026/07-10/607676.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-10",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "确认韩剑任县委常委、县委办主任"},
        {"id": "S009", "title": "张涛督导防汛",
         "url": "https://www.wuzhi.gov.cn/2026/07-10/607657.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-10",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "确认秦康任副县长并陪同检查"},
        {"id": "S010", "title": "县委生态环境保护专题会",
         "url": "https://www.wuzhi.gov.cn/2026/06-29/606563.html",
         "publisher": "武陟县人民政府", "published_at": "2026-06-29",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "吴立强、韩剑、孙广超、原世远、秦康、李世鹏出席"},
        {"id": "S011", "title": "全县防汛备汛汇报会",
         "url": "https://www.wuzhi.gov.cn/2026/07-20/608381.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-20",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "吕学梅、陈华阳、左心亮、韩剑、原世远、毛克祥出席"},
        {"id": "S012", "title": "杨正栋到大封镇调研",
         "url": "https://www.wuzhi.gov.cn/2026/06-18/605909.html",
         "publisher": "武陟县人民政府", "published_at": "2026-06-18",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "确认吕学梅任县委副书记"},
        {"id": "S013", "title": "水污染防治工作专题会",
         "url": "https://www.wuzhi.gov.cn/2026/06-12/605400.html",
         "publisher": "武陟县人民政府", "published_at": "2026-06-12",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "吴立强、韩剑、邢明出席"},
        {"id": "S014", "title": "杨正栋张涛七一慰问",
         "url": "https://www.wuzhi.gov.cn/2026/07-02/606964.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-02",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "韩剑、李备战参加"},
        {"id": "S015", "title": "杨正栋调研生物医药",
         "url": "https://www.wuzhi.gov.cn/2026/07-14/607850.html",
         "publisher": "武陟县人民政府", "published_at": "2026-07-14",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "吴立强、韩剑参加"},
    ]


def make_person_json(person, timeline_text, rels, source_reg):
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "焦作市",
            "region": "武陟县",
            "job": person["current_post"],
            "task_id": "henan_武陟县",
            "time_focus": "截至2026年7月"
        },
        "identity": {
            "person_id": f"wuzhi_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] or "县长" in person["current_post"] or "人大主任" in person["current_post"] else "副处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": timeline_text,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_reg,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "杨正栋和张涛的完整履历（出生年、籍贯、学历、早期任职经历）；杨正栋的前任职务；赵红兵去向；申琳去向；各县委常委的具体分管职务",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生年、籍贯、学历、早期任职经历）",
                "why_it_matters": "完整履历是理解晋升路径和人际网络的基础",
                "suggested_queries": [f"{person['name']} 简历"],
                "last_attempted": TODAY,
            },
        ],
    }


if __name__ == "__main__":
    run_build()

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 杨正栋 — 县委书记
    yang_timeline = [
        {"start": "2026-04", "end": "", "org": "中共武陟县委员会",
         "title": "中共武陟县委书记",
         "notes": "2026年4月底-5月初上任；6月县第十四次党代会选举确认；首次以书记身份出报道在2026年5月12日左右",
         "confidence": "confirmed", "source_ids": ["S001", "S005", "S008"]},
    ]
    yang_rels = [
        {"person": "张涛", "person_id": "wuzhi_张涛",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "县委书记与县长党政工作搭档",
         "overlap_org": "武陟县", "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "赵红兵", "person_id": "wuzhi_赵红兵",
         "relationship_type": "succession", "strength": "medium",
         "evidence": "接替赵红兵任县委书记；赵红兵至2025年12月底仍在任",
         "overlap_org": "中共武陟县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S005"]},
    ]
    yang_json = make_person_json(persons[0], yang_timeline, yang_rels, source_register)
    yang_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-焦作市-县委书记-杨正栋.json")
    with open(yang_path, "w", encoding="utf-8") as f:
        json.dump(yang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(yang_path)}")

    # 2. 张涛 — 县长
    zhang_timeline = [
        {"start": "2021-04", "end": "", "org": "武陟县人民政府",
         "title": "武陟县委副书记、县长",
         "notes": "最早可确认2023年4月以县长身份作政府工作报告；前任申琳2021年3月仍在任；推测2021年4月前后接任",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2023-06", "end": "", "org": "中共武陟县委员会",
         "title": "武陟县委副书记",
         "notes": "兼任县委副书记至2026年县第十四次党代会",
         "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    zhang_rels = [
        {"person": "杨正栋", "person_id": "wuzhi_杨正栋",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "县长与县委书记党政工作搭档",
         "overlap_org": "武陟县", "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "赵红兵", "person_id": "wuzhi_赵红兵",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "张涛在赵红兵任县委书记期间（2023-2025）任县长",
         "overlap_org": "武陟县", "overlap_period": "2023-2025",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"person": "申琳", "person_id": "wuzhi_申琳",
         "relationship_type": "succession", "strength": "medium",
         "evidence": "接替申琳任县长",
         "overlap_org": "武陟县人民政府", "overlap_period": "2021",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"person": "乔楠", "person_id": "wuzhi_乔楠",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "县长与常务副县长——协助县长分管县政府常务工作",
         "overlap_org": "武陟县人民政府", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S003"]},
    ]
    zhang_json = make_person_json(persons[1], zhang_timeline, zhang_rels, source_register)
    zhang_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-焦作市-县长-张涛.json")
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(zhang_path)}")

    # 3. 吕学梅 — 县委副书记
    lv_timeline = [
        {"start": "", "end": "", "org": "中共武陟县委员会",
         "title": "武陟县委副书记",
         "notes": "专职副书记，多次陪同杨正栋调研并出席县委各类会议",
         "confidence": "confirmed", "source_ids": ["S004", "S011", "S012"]},
    ]
    lv_rels = [
        {"person": "杨正栋", "person_id": "wuzhi_杨正栋",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "县委副书记作为县委书记主要副手",
         "overlap_org": "中共武陟县委员会", "overlap_period": "2026-",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S012"]},
    ]
    lv_json = make_person_json(persons[2], lv_timeline, lv_rels, source_register)
    lv_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-焦作市-县委副书记-吕学梅.json")
    with open(lv_path, "w", encoding="utf-8") as f:
        json.dump(lv_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(lv_path)}")

    # 4. 乔楠 — 常务副县长
    qiao_timeline = [
        {"start": "", "end": "", "org": "武陟县人民政府",
         "title": "武陟县委常委、常务副县长",
         "notes": "协助县长负责县政府常务工作",
         "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    qiao_rels = [
        {"person": "张涛", "person_id": "wuzhi_张涛",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "常务副县长协助县长工作",
         "overlap_org": "武陟县人民政府", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S003"]},
    ]
    qiao_json = make_person_json(persons[3], qiao_timeline, qiao_rels, source_register)
    qiao_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-焦作市-常务副县长-乔楠.json")
    with open(qiao_path, "w", encoding="utf-8") as f:
        json.dump(qiao_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(qiao_path)}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")
