#!/usr/bin/env python3
"""宜昌市猇亭区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源: 猇亭区人民政府网站 (xiaoting.gov.cn, 领导之窗页面直接获取)
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation package is importable
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "猇亭区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government, 3xxx =人大/政协
# Sources: 猇亭区人民政府网站 (http://www.xiaoting.gov.cn/list-1326-1.html)
#           (http://www.xiaoting.gov.cn/list-1328-1.html)
#           (http://www.xiaoting.gov.cn/list-1327-1.html)
#           (http://www.xiaoting.gov.cn/list-1329-1.html)

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 左晓 — 区委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "左晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "education": "研究生、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委书记",
        "current_org": "中共宜昌市猇亭区委员会",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 郑劢 — 区委副书记、区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "郑劢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区委副书记、区政府区长、党组书记，兼任三峡临空经济区管理办公室主任",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 张翔 — 区委副书记、政法委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "张翔",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1981年9月",
        "birthplace": "",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委副书记、政法委书记、区法学会会长",
        "current_org": "中共宜昌市猇亭区委员会",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 鲁武 — 区委常委、宣传部部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "鲁武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委常委、宣传部部长、区总工会主席",
        "current_org": "中共宜昌市猇亭区委宣传部",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 谭湘华 — 区委常委、组织部部长、统战部部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "谭湘华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委常委、组织部部长、统战部部长、区政协党组副书记（兼）",
        "current_org": "中共宜昌市猇亭区委组织部",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 张锐 — 区委常委、纪委书记、监委主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "张锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "",
        "education": "大学、省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委常委、纪委书记、监委主任",
        "current_org": "中共宜昌市猇亭区纪律检查委员会",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 田开春 — 区委常委、区委办公室主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "田开春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "",
        "education": "大学、经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委常委、区委办公室主任",
        "current_org": "中共宜昌市猇亭区委办公室",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 程刚 — 区委常委、区人武部部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "程刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "大学、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委常委、区人武部部长",
        "current_org": "猇亭区人民武装部",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 谭本相 — 区委常委、常务副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "谭本相",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1982年4月",
        "birthplace": "",
        "education": "研究生、历史学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市猇亭区委常委、区政府副区长（协助区长负责政府日常工作）",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1326-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 郑晓军 — 副区长、公安分局局长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "郑晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区人民政府副区长、党组成员，市公安局猇亭区分局党委书记、局长",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1328-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 鲍剑飞 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1011,
        "name": "鲍剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "猇亭区人民政府副区长",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1328-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 向光富 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1012,
        "name": "向光富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "大学、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区人民政府副区长、党组成员",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1328-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 李迎鑫 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1013,
        "name": "李迎鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区人民政府副区长、党组成员",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1328-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 14. 王功赵 — 副区长（援藏）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1014,
        "name": "王功赵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年12月",
        "birthplace": "",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区人民政府副区长、党组成员（援藏对口支援）",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1328-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 15. 梅峰 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1015,
        "name": "梅峰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年4月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区人民政府副区长、党组成员、区红十字会党组书记、会长",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1328-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 16. 崔家兴 — 副区长（挂职）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1016,
        "name": "崔家兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年2月",
        "birthplace": "",
        "education": "研究生、管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区人民政府副区长、党组成员（挂职两年）",
        "current_org": "宜昌市猇亭区人民政府",
        "source": "http://www.xiaoting.gov.cn/list-1328-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 17. 刘伟 — 区人大常委会主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "刘伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区人大常委会主任、党组书记",
        "current_org": "猇亭区人大常委会",
        "source": "http://www.xiaoting.gov.cn/list-1327-1.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 18. 尹德斌 — 区政协主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "尹德斌",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1971年4月",
        "birthplace": "",
        "education": "在职大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区政协主席、党组书记",
        "current_org": "猇亭区政协",
        "source": "http://www.xiaoting.gov.cn/list-1329-1.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共宜昌市猇亭区委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市委员会", "location": "宜昌市猇亭区"},
    {"id": 2, "name": "宜昌市猇亭区人民政府", "type": "政府", "level": "县处级",
     "parent": "宜昌市人民政府", "location": "宜昌市猇亭区"},
    {"id": 3, "name": "猇亭区人大常委会", "type": "人大", "level": "县处级",
     "parent": "宜昌市人大常委会", "location": "宜昌市猇亭区"},
    {"id": 4, "name": "猇亭区政协", "type": "政协", "level": "县处级",
     "parent": "宜昌市政协", "location": "宜昌市猇亭区"},
    {"id": 5, "name": "中共宜昌市猇亭区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市纪律检查委员会", "location": "宜昌市猇亭区"},
    {"id": 6, "name": "中共宜昌市猇亭区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共宜昌市猇亭区委员会", "location": "宜昌市猇亭区"},
    {"id": 7, "name": "中共宜昌市猇亭区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共宜昌市猇亭区委员会", "location": "宜昌市猇亭区"},
    {"id": 8, "name": "中共宜昌市猇亭区委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共宜昌市猇亭区委员会", "location": "宜昌市猇亭区"},
    {"id": 9, "name": "猇亭区人民武装部", "type": "党委", "level": "县处级",
     "parent": "宜昌军分区", "location": "宜昌市猇亭区"},
    {"id": 10, "name": "宜昌市公安局猇亭区分局", "type": "政府", "level": "乡科级",
     "parent": "宜昌市公安局", "location": "宜昌市猇亭区"},
    {"id": 11, "name": "三峡临空经济区管理办公室", "type": "政府", "level": "县处级",
     "parent": "宜昌市人民政府", "location": "宜昌市猇亭区"},
    {"id": 12, "name": "猇亭区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共宜昌市猇亭区委员会", "location": "宜昌市猇亭区"},
    {"id": 13, "name": "猇亭区总工会", "type": "群团", "level": "乡科级",
     "parent": "宜昌市总工会", "location": "宜昌市猇亭区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 左晓 — 区委书记
    {"person_id": 1001, "org_id": 1, "title": "中共宜昌市猇亭区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职（一级调研员）",
     "note": "1982年11月生，研究生、公共管理硕士，中共党员。一级调研员。"},
    # 郑劢 — 区长
    {"person_id": 1002, "org_id": 2, "title": "猇亭区人民政府区长、党组书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "1980年7月生，省委党校研究生，中共党员。兼任三峡临空经济区管理办公室主任。"},
    {"person_id": 1002, "org_id": 11, "title": "三峡临空经济区管理办公室主任（兼）",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 张翔 — 区委副书记、政法委书记
    {"person_id": 1003, "org_id": 1, "title": "区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1981年9月生，土家族，大学、法学学士，中共党员。"},
    {"person_id": 1003, "org_id": 12, "title": "区委政法委书记、区法学会会长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 鲁武 — 宣传部部长
    {"person_id": 1004, "org_id": 6, "title": "区委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1981年6月生，汉族，大学、法学学士，中共党员。兼任区总工会主席。"},
    {"person_id": 1004, "org_id": 13, "title": "区总工会主席（兼）",
     "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 谭湘华 — 组织部部长
    {"person_id": 1005, "org_id": 7, "title": "区委常委、组织部部长、统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1975年5月生，汉族，大学、法学学士，中共党员。兼区政协党组副书记。"},
    # 张锐 — 纪委书记
    {"person_id": 1006, "org_id": 5, "title": "区委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1978年2月生，汉族，大学、省委党校研究生，中共党员。四级高级监察官。"},
    # 田开春 — 区委办公室主任
    {"person_id": 1007, "org_id": 8, "title": "区委常委、区委办公室主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1976年3月生，汉族，大学、经济学学士，中共党员。"},
    # 程刚 — 人武部部长
    {"person_id": 1008, "org_id": 9, "title": "区委常委、区人武部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1979年6月生，汉族，大学、工学学士，中共党员。"},
    # 谭本相 — 常务副区长
    {"person_id": 1009, "org_id": 1, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1982年4月生，土家族，研究生、历史学硕士，中共党员。"},
    {"person_id": 1009, "org_id": 2, "title": "副区长（协助区长负责政府日常工作）、党组副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 郑晓军 — 副区长、公安分局局长
    {"person_id": 1010, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职（二级高级警长）",
     "note": "1968年1月生，汉族，在职大学，中共党员。"},
    {"person_id": 1010, "org_id": 10, "title": "市公安局猇亭区分局党委书记、局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 鲍剑飞 — 副区长
    {"person_id": 1011, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1979年10月生，汉族，在职大学。"},
    # 向光富 — 副区长
    {"person_id": 1012, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1972年7月生，汉族，大学、工学学士，中共党员。"},
    # 李迎鑫 — 副区长
    {"person_id": 1013, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1979年1月生，汉族，大学，中共党员。"},
    # 王功赵 — 副区长（援藏）
    {"person_id": 1014, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职（三级调研员）",
     "note": "1982年12月生，汉族，大学、法学学士，中共党员。赴西藏山南市加查县对口支援。"},
    # 梅峰 — 副区长
    {"person_id": 1015, "org_id": 2, "title": "副区长、党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1986年4月生，女，汉族，省委党校研究生，中共党员。兼区红十字会党组书记、会长。"},
    # 崔家兴 — 副区长（挂职）
    {"person_id": 1016, "org_id": 2, "title": "副区长、党组成员（挂职两年）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1990年2月生，汉族，研究生、管理学博士，中共党员。"},
    # 刘伟 — 区人大常委会主任
    {"person_id": 2001, "org_id": 3, "title": "区人大常委会主任、党组书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "1970年6月生，汉族，在职大学，中共党员。2026年接替高亚华担任。"},
    # 尹德斌 — 区政协主席
    {"person_id": 2002, "org_id": 4, "title": "区政协主席、党组书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职（一级调研员）",
     "note": "1971年4月生，土家族，在职大专，中共党员。"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 左晓 ←→ 郑劢: 党政正职搭档
    {"person_a": 1001, "person_b": 1002, "type": "overlap",
     "context": "党政正职搭档：区委书记—区长",
     "overlap_org": "中共宜昌市猇亭区委员会／猇亭区人民政府",
     "overlap_period": "2024年至今"},
    # 左晓 ←→ 张翔: 区委正副书记
    {"person_a": 1001, "person_b": 1003, "type": "superior_subordinate",
     "context": "区委书记—副书记工作关系",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    # 左晓 — 各区委常委
    {"person_a": 1001, "person_b": 1004, "type": "superior_subordinate",
     "context": "区委书记—宣传部部长",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    {"person_a": 1001, "person_b": 1005, "type": "superior_subordinate",
     "context": "区委书记—组织部部长",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    {"person_a": 1001, "person_b": 1006, "type": "superior_subordinate",
     "context": "区委书记—纪委书记",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    {"person_a": 1001, "person_b": 1007, "type": "superior_subordinate",
     "context": "区委书记—区委办公室主任",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    {"person_a": 1001, "person_b": 1008, "type": "superior_subordinate",
     "context": "区委书记—人武部部长",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    {"person_a": 1001, "person_b": 1009, "type": "superior_subordinate",
     "context": "区委书记—常务副区长（区委常委）",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    # 郑劢 ←→ 谭本相: 正副区长
    {"person_a": 1002, "person_b": 1009, "type": "superior_subordinate",
     "context": "区长—常务副区长",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    # 郑劢 — 各副区长
    {"person_a": 1002, "person_b": 1010, "type": "superior_subordinate",
     "context": "区长—副区长（公安）",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 1011, "type": "superior_subordinate",
     "context": "区长—副区长",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 1012, "type": "superior_subordinate",
     "context": "区长—副区长",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 1013, "type": "superior_subordinate",
     "context": "区长—副区长",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 1014, "type": "superior_subordinate",
     "context": "区长—副区长（援藏）",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 1015, "type": "superior_subordinate",
     "context": "区长—副区长",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 1016, "type": "superior_subordinate",
     "context": "区长—副区长（挂职）",
     "overlap_org": "猇亭区人民政府",
     "overlap_period": "推定"},
    # 张翔 ←→ 左晓 已在上方；张翔 —— 郑劢: 党政正副职
    {"person_a": 1002, "person_b": 1003, "type": "overlap",
     "context": "区长—区委副书记",
     "overlap_org": "中共宜昌市猇亭区委员会",
     "overlap_period": "推定"},
    # 人大、政协与区领导
    {"person_a": 1001, "person_b": 2001, "type": "overlap",
     "context": "区委书记—人大常委会主任",
     "overlap_org": "猇亭区",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 2001, "type": "overlap",
     "context": "区长—人大常委会主任",
     "overlap_org": "猇亭区",
     "overlap_period": "推定"},
    {"person_a": 1001, "person_b": 2002, "type": "overlap",
     "context": "区委书记—政协主席",
     "overlap_org": "猇亭区",
     "overlap_period": "推定"},
    {"person_a": 1002, "person_b": 2002, "type": "overlap",
     "context": "区长—政协主席",
     "overlap_org": "猇亭区",
     "overlap_period": "推定"},
]

# ── Main ─────────────────────────────────────────────────────────────────────


def write_person_json(person: dict) -> None:
    """Write a person graph JSON file to the staging directory."""
    safe_name = person["name"]
    # Build a short job slug
    post = person["current_post"]
    if "区委书记" in post:
        job_slug = "区委书记"
    elif "区长" in post:
        job_slug = "区长"
    elif "副书记" in post:
        job_slug = "区委副书记"
    elif "副区长" in post:
        job_slug = "副区长"
    elif "人大常委会主任" in post:
        job_slug = "人大常委会主任"
    elif "政协主席" in post:
        job_slug = "政协主席"
    else:
        job_slug = post.split("，")[0][:12]

    filename = f"{TODAY.replace('-', '')}-湖北省-宜昌市-{job_slug}-{safe_name}.json"
    filepath = STAGING / filename

    # Determine primary system
    if "区委书记" in post or "副书记" in post:
        primary_system = "party"
    elif "区长" in post or "副区长" in post:
        primary_system = "government"
    elif "人大" in post:
        primary_system = "other"
    elif "政协" in post:
        primary_system = "other"
    else:
        primary_system = "other"

    # Determine career pattern
    career_pattern = "cross_county_rotation" if "挂职" in post else "local_ladder"
    is_top_leader = "区委书记" in post or "区长" in post

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "宜昌市",
            "region": "猇亭区",
            "job": post,
            "task_id": "hubei_猇亭区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"hubei_yichang_xiaoting_{safe_name}",
            "name": safe_name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
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
                "name_birth": f"{safe_name}_{person.get('birth', '')}",
                "name_birthplace": f"{safe_name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": post,
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if is_top_leader or "正" in post else "县处级副职",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": person["current_org"],
                "title": post,
                "level": "",
                "location": "宜昌市猇亭区",
                "system": primary_system,
                "rank": "",
                "is_key_promotion": is_top_leader,
                "notes": "待补充详细履历——因搜索受限无法获取完整职业生涯历史",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [
            {
                "period": TODAY,
                "domain": "other",
                "achievement_or_event": "在任猇亭区相关职务（具体成果待补充）",
                "role_in_event": "现职",
                "measurable_outcome": "",
                "location": "宜昌市猇亭区",
                "confidence": "unverified",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": career_pattern,
            "systems_experience": [primary_system],
            "geographic_pattern": ["宜昌市"],
            "promotion_velocity": {
                "summary": "因搜索受限，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "网络搜索受限，无法获取足够公开资料推断工作风格",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因网络搜索受限，未发现风险信号。需后续在有网络条件下排查。",
                "date": TODAY,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "猇亭区人民政府网站—领导之窗",
                "url": "http://www.xiaoting.gov.cn/list-1326-1.html",
                "publisher": "猇亭区人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方政府网站领导之窗页面，包含完整领导班子名单",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺乏早年履历、出生地、籍贯、入党时间、工作起始时间等信息；" +
                          "无法获取前任领导信息及跨县区交流情况",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{safe_name}的完整履历——任职前的职业生涯、晋升路径？",
                "why_it_matters": "这是构建完整个人图谱和进行网络分析的基础数据",
                "suggested_queries": [
                    f"{safe_name} 简历",
                    f"{safe_name} 任前公示",
                    f"{safe_name} 猇亭 任命",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": f"{safe_name}的出生地、籍贯、入党时间、工作起始时间？",
                "why_it_matters": "用于身份去重和关系分析",
                "suggested_queries": [
                    f"{safe_name} 出生",
                    f"{safe_name} 籍贯",
                ],
                "last_attempted": TODAY,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ── Build database & GEXF ────────────────────────────────────────────
    print(f"Building {SLUG} network data…")
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
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # ── Person JSON files ────────────────────────────────────────────────
    print("Writing person graph JSON files…")

    # Write person JSON for the two core leaders
    core_leaders = [p for p in persons if p["id"] in (1001, 1002)]  # 左晓 and 郑劢
    for p in core_leaders:
        write_person_json(p)

    print("Done.")
