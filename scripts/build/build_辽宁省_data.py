#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 辽宁省领导班子 (Liaoning Province Leadership Network).
Investigation date: 2026-07-25

Current 辽宁省委书记: 郝鹏 (as of 2022.11)
Current 辽宁省省长: 李乐成 (as of 2021.10)
"""

import os
import sqlite3
import sys
from pathlib import Path

# Add repo root to path
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))
os.chdir(str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "辽宁省_network.db"
GEXF_PATH = GRAPH_DIR / "辽宁省_network.gexf"

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

persons = [
    # ── 郝鹏 - 辽宁省委书记 (Party Secretary) ──
    {"id": 1, "name": "郝鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1960-07", "birthplace": "陕西凤翔", "education": "西北工业大学飞行器制造工程系毕业，工程硕士，高级经济师",
     "party_join": "1982-03", "work_start": "1976-01",
     "current_post": "辽宁省委书记、省人大常委会主任", "current_org": "中共辽宁省委",
     "source": "https://baike.baidu.com/item/%E9%83%9D%E9%B9%8F"},

    # ── 李乐成 - 辽宁省省长 (Governor) ──
    {"id": 2, "name": "李乐成", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-03", "birthplace": "湖北监利", "education": "华中工学院（华中科技大学）机械工程一系毕业，大学学历，工学学士",
     "party_join": "1984-12", "work_start": "1984-08",
     "current_post": "辽宁省委副书记、省长", "current_org": "辽宁省人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E4%B9%90%E6%88%90"},

    # ── 前前任辽宁省委书记: 张国清 (2020-2022) ──
    {"id": 3, "name": "张国清", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-08", "birthplace": "河南罗山", "education": "长春光学精密机械学院（长春理工大学）电子工程系，清华大学经济管理学院数量经济学专业博士研究生",
     "party_join": "1984-07", "work_start": "1985-09",
     "current_post": "中央政治局委员、重庆市委书记", "current_org": "中共重庆市委",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%9B%BD%E6%B8%85"},

    # ── 前任辽宁省委书记: 陈求发 (2017-2020) ──
    {"id": 4, "name": "陈求发", "gender": "男", "ethnicity": "苗族",
     "birth": "1954-12", "birthplace": "湖南城步", "education": "国防科技大学",
     "party_join": "1974-01", "work_start": "1973-03",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E9%99%88%E6%B1%82%E5%8F%91"},

    # ── 前任辽宁省省长: 刘宁 (2020-2021) ──
    {"id": 5, "name": "刘宁", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-01", "birthplace": "辽宁凌源", "education": "清华大学水利工程系毕业，工学博士",
     "party_join": "1983-06", "work_start": "1983-07",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%88%98%E5%AE%81/24654757"},

    # ── 前任辽宁省省长: 唐一军 (2017-2020) ──
    {"id": 6, "name": "唐一军", "gender": "男", "ethnicity": "汉族",
     "birth": "1961-03", "birthplace": "山东莒县", "education": "浙江省委党校研究生",
     "party_join": "1985-10", "work_start": "1977-07",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%94%90%E4%B8%80%E5%86%9B"},

    # ── 省委副书记: 王新伟 ──
    {"id": 7, "name": "王新伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-08", "birthplace": "河南宝丰", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委副书记、沈阳市委书记", "current_org": "中共沈阳市委",
     "source": "https://baike.baidu.com/item/%E7%8E%8B%E6%96%B0%E4%BC%9F"},

    # ── 省委常委、省纪委书记: 李猛 ──
    {"id": 8, "name": "李猛", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-02", "birthplace": "安徽凤台", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、省纪委书记、省监委主任", "current_org": "中共辽宁省纪律检查委员会",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E7%8C%9B"},

    # ── 省委常委、常务副省长: 王健 ──
    {"id": 9, "name": "王健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、常务副省长", "current_org": "辽宁省人民政府",
     "source": "https://baike.baidu.com/item/%E7%8E%8B%E5%81%A5/23970335"},

    # ── 省委常委、组织部部长: 蒋天宝 ──
    {"id": 10, "name": "蒋天宝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、组织部部长", "current_org": "中共辽宁省委组织部",
     "source": "https://baike.baidu.com/item/%E8%92%8B%E5%A4%A9%E5%AE%9D"},

    # ── 省委常委、宣传部部长: 刘慧晏 ──
    {"id": 11, "name": "刘慧晏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、宣传部部长", "current_org": "中共辽宁省委宣传部",
     "source": "https://baike.baidu.com/item/%E5%88%98%E6%85%A7%E6%99%8F"},

    # ── 省委常委、政法委书记: 霍步刚 ──
    {"id": 12, "name": "霍步刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、政法委书记", "current_org": "中共辽宁省委政法委",
     "source": "https://baike.baidu.com/item/%E9%9C%8D%E6%AD%A5%E5%88%9A"},

    # ── 省委常委、统战部部长: 隋青 ──
    {"id": 13, "name": "隋青", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、统战部部长", "current_org": "中共辽宁省委统战部",
     "source": "https://baike.baidu.com/item/%E9%9A%8B%E9%9D%92"},

    # ── 省委常委、大连市委书记: 熊茂平 ──
    {"id": 14, "name": "熊茂平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、大连市委书记", "current_org": "中共大连市委",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E8%8C%82%E5%B9%B3"},

    # ── 省委常委、省委秘书长: 姜有为 ──
    {"id": 15, "name": "姜有为", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、省委秘书长", "current_org": "中共辽宁省委办公厅",
     "source": "https://baike.baidu.com/item/%E5%A7%9C%E6%9C%89%E4%B8%BA"},

    # ── 省军区司令员: 王河 ──
    {"id": 16, "name": "王河", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省委常委、省军区司令员", "current_org": "辽宁省军区",
     "source": "https://www.ln.gov.cn"},

    # ── 副省长1: 高涛 ──
    {"id": 17, "name": "高涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省副省长", "current_org": "辽宁省人民政府",
     "source": "https://baike.baidu.com/item/%E9%AB%98%E6%B6%9B"},

    # ── 副省长2: 郑艺 ──
    {"id": 18, "name": "郑艺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省副省长、省公安厅厅长", "current_org": "辽宁省人民政府/省公安厅",
     "source": "https://baike.baidu.com/item/%E9%83%91%E8%89%BA"},

    # ── 副省长3: 王利波 ──
    {"id": 19, "name": "王利波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省副省长", "current_org": "辽宁省人民政府",
     "source": "https://baike.baidu.com/item/%E7%8E%8B%E5%88%A9%E6%B3%A2"},

    # ── 副省长4: 单义 ──
    {"id": 20, "name": "单义", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省副省长", "current_org": "辽宁省人民政府",
     "source": "https://baike.baidu.com/item/%E5%8D%95%E4%B9%89"},

    # ── 副省长5: 郭彩云 ──
    {"id": 21, "name": "郭彩云", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "辽宁省副省长", "current_org": "辽宁省人民政府",
     "source": "https://baike.baidu.com/item/%E9%83%AD%E5%BD%A9%E4%BA%91"},

    # ── 省政协主席: 周波 ──
    {"id": 22, "name": "周波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "辽宁省政协主席", "current_org": "辽宁省政协",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E6%B3%A2/24704558"},

    # ── 省人大常委会主任（郝鹏兼）已由id=1覆盖 ──
]

organizations = [
    {"id": 1, "name": "中共辽宁省委", "type": "党委", "level": "省级", "parent": "", "location": "沈阳"},
    {"id": 2, "name": "辽宁省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "沈阳"},
    {"id": 3, "name": "中共辽宁省纪律检查委员会", "type": "纪委", "level": "省级", "parent": "中共辽宁省委", "location": "沈阳"},
    {"id": 4, "name": "中共辽宁省委组织部", "type": "党委部门", "level": "省级", "parent": "中共辽宁省委", "location": "沈阳"},
    {"id": 5, "name": "中共辽宁省委宣传部", "type": "党委部门", "level": "省级", "parent": "中共辽宁省委", "location": "沈阳"},
    {"id": 6, "name": "中共辽宁省委统战部", "type": "党委部门", "level": "省级", "parent": "中共辽宁省委", "location": "沈阳"},
    {"id": 7, "name": "中共辽宁省委政法委", "type": "党委部门", "level": "省级", "parent": "中共辽宁省委", "location": "沈阳"},
    {"id": 8, "name": "中共辽宁省委办公厅", "type": "党委部门", "level": "省级", "parent": "中共辽宁省委", "location": "沈阳"},
    {"id": 9, "name": "中共沈阳市委", "type": "党委", "level": "副省级", "parent": "中共辽宁省委", "location": "沈阳"},
    {"id": 10, "name": "中共大连市委", "type": "党委", "level": "副省级", "parent": "中共辽宁省委", "location": "大连"},
    {"id": 11, "name": "辽宁省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "沈阳"},
    {"id": 12, "name": "辽宁省政协", "type": "政协", "level": "省级", "parent": "", "location": "沈阳"},
    {"id": 13, "name": "辽宁省公安厅", "type": "政府", "level": "省级", "parent": "辽宁省人民政府", "location": "沈阳"},
    {"id": 14, "name": "辽宁省军区", "type": "军队", "level": "省级", "parent": "", "location": "沈阳"},
]

positions = [
    # 郝鹏
    {"person_id": 1, "org_id": 1, "title": "辽宁省委书记", "start_date": "2022-11", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "辽宁省人大常委会主任", "start_date": "2023-01", "end_date": "present", "rank": "正省级", "note": "由省委书记兼任"},
    # 郝鹏前任经历
    {"person_id": 1, "org_id": 1, "title": "国务院国有资产监督管理委员会党委书记、主任", "start_date": "2019-05", "end_date": "2022-11", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "青海省省长", "start_date": "2016-12", "end_date": "2019-05", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "西藏自治区党委副书记、常务副主席", "start_date": "2012-04", "end_date": "2016-12", "rank": "副省级", "note": ""},

    # 李乐成
    {"person_id": 2, "org_id": 2, "title": "辽宁省省长", "start_date": "2021-10", "end_date": "present", "rank": "正省级", "note": "辽宁省委副书记、省长"},
    # 李乐成前任经历
    {"person_id": 2, "org_id": 1, "title": "湖北省委常委、常务副省长", "start_date": "2020-02", "end_date": "2021-10", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "湖北省委常委、襄阳市委书记", "start_date": "2013-05", "end_date": "2020-02", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "湖北省发展和改革委员会主任", "start_date": "2008-02", "end_date": "2013-05", "rank": "正厅级", "note": ""},

    # 张国清
    {"person_id": 3, "org_id": 1, "title": "辽宁省委书记", "start_date": "2020-08", "end_date": "2022-11", "rank": "正省级", "note": "前任省委书记"},
    {"person_id": 3, "org_id": 1, "title": "辽宁省省长", "start_date": "2017-10", "end_date": "2020-08", "rank": "正省级", "note": ""},

    # 陈求发
    {"person_id": 4, "org_id": 1, "title": "辽宁省委书记", "start_date": "2017-10", "end_date": "2020-08", "rank": "正省级", "note": "前任省委书记"},

    # 刘宁
    {"person_id": 5, "org_id": 2, "title": "辽宁省省长", "start_date": "2020-07", "end_date": "2021-10", "rank": "正省级", "note": "前任省长"},
    {"person_id": 5, "org_id": 2, "title": "青海省省长", "start_date": "2018-08", "end_date": "2020-07", "rank": "正省级", "note": "调任辽宁前在青海任职"},

    # 唐一军
    {"person_id": 6, "org_id": 2, "title": "辽宁省省长", "start_date": "2017-10", "end_date": "2020-04", "rank": "正省级", "note": "前任省长"},

    # 王新伟
    {"person_id": 7, "org_id": 1, "title": "辽宁省委副书记、沈阳市委书记", "start_date": "2024-03", "end_date": "present", "rank": "副省级", "note": "省委副书记兼任沈阳市委书记"},
    {"person_id": 7, "org_id": 1, "title": "辽宁省委常委、沈阳市委书记", "start_date": "2021-10", "end_date": "2024-03", "rank": "副省级", "note": ""},

    # 李猛
    {"person_id": 8, "org_id": 3, "title": "辽宁省纪委书记、省监委主任", "start_date": "2022-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 王健
    {"person_id": 9, "org_id": 2, "title": "辽宁省委常委、常务副省长", "start_date": "2022-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 蒋天宝
    {"person_id": 10, "org_id": 4, "title": "辽宁省委组织部部长", "start_date": "2023-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 刘慧晏
    {"person_id": 11, "org_id": 5, "title": "辽宁省委宣传部部长", "start_date": "2020-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 霍步刚
    {"person_id": 12, "org_id": 7, "title": "辽宁省委政法委书记", "start_date": "2023-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 隋青
    {"person_id": 13, "org_id": 6, "title": "辽宁省委统战部部长", "start_date": "2024-04", "end_date": "present", "rank": "副省级", "note": ""},

    # 熊茂平
    {"person_id": 14, "org_id": 10, "title": "大连市委书记", "start_date": "2024-04", "end_date": "present", "rank": "副省级", "note": "省委常委兼任"},

    # 姜有为
    {"person_id": 15, "org_id": 8, "title": "辽宁省委秘书长", "start_date": "2023-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 王河
    {"person_id": 16, "org_id": 14, "title": "辽宁省军区司令员", "start_date": "", "end_date": "present", "rank": "副省级", "note": "省委常委兼任"},

    # 副省长们
    {"person_id": 17, "org_id": 2, "title": "辽宁省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "辽宁省副省长、省公安厅厅长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "辽宁省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "辽宁省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "辽宁省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},

    # 周波
    {"person_id": 22, "org_id": 12, "title": "辽宁省政协主席", "start_date": "2023-01", "end_date": "present", "rank": "正省级", "note": ""},
]

relationships = [
    # 郝鹏 — 李乐成（省委书记—省长搭班）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "省委书记—省长搭班", "overlap_org": "辽宁省", "overlap_period": "2022-11至今"},
    # 郝鹏 — 张国清（前任继任）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "接替张国清任辽宁省委书记", "overlap_org": "中共辽宁省委", "overlap_period": "2022-11"},
    # 张国清 — 陈求发（前任继任）
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "接替陈求发任辽宁省委书记", "overlap_org": "中共辽宁省委", "overlap_period": "2020-08"},
    # 李乐成 — 刘宁（前任继任）
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor", "context": "接替刘宁任辽宁省省长", "overlap_org": "辽宁省人民政府", "overlap_period": "2021-10"},
    # 刘宁 — 唐一军（前任继任）
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "接替唐一军任辽宁省省长", "overlap_org": "辽宁省人民政府", "overlap_period": "2020-07"},
    # 郝鹏 — 王新伟（上下级）
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "省委书记—省委副书记/沈阳市委书记", "overlap_org": "中共辽宁省委", "overlap_period": "2022-11至今"},
    # 郝鹏 — 李猛（上下级）
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "省委书记—省纪委书记", "overlap_org": "中共辽宁省委", "overlap_period": "2022-11至今"},
    # 郝鹏 — 熊茂平（上下级）
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "省委书记—省委常委/大连市委书记", "overlap_org": "中共辽宁省委", "overlap_period": "2022-11至今"},
    # 李乐成 — 王健（上下级）
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "省长—常务副省长", "overlap_org": "辽宁省人民政府", "overlap_period": "2022-01至今"},
    # 李乐成 — 王新伟（搭班）
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "省长—省委副书记同班子", "overlap_org": "辽宁省", "overlap_period": "2021-10至今"},
    # 张国清 — 刘宁（前任书记省长搭班）
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "前任省委书记—前任省长搭班", "overlap_org": "辽宁省", "overlap_period": "2020-08至2021-10"},
    # 陈求发 — 唐一军（前任书记省长搭班）
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "前任省委书记—前任省长搭班", "overlap_org": "辽宁省", "overlap_period": "2017-10至2020-04"},
]

# ═══════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="辽宁省",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done: 辽宁省 network built.")
