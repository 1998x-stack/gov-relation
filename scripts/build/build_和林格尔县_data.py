#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 和林格尔县 leadership network.

和林格尔县隶属内蒙古自治区呼和浩特市。县域与国家级开发区——内蒙古和林格尔新区
（含呼和浩特和林格尔乳业开发区、盛乐经济园区、大数据产业园区/中国"东数西算"数据中心
集群）深度联动，是呼和浩特市重点产业承载县。

Current leadership (confirmed 2026-08-06 from helin.gov.cn 领导之窗,
和中国共产党和林格尔县第十六次代表大会公报 2026-07-30, 呼和浩特市委组织部任前公示):
- 县委书记: 张志魁 (2026-05 任前公示拟任旗县党委书记，现任县委书记兼县人武部党委第一书记)
- 县委副书记、政府党组书记、代县长: 王孛 (和林格尔乳业开发区党工委书记)

前情(时间线)：
- 前任县委书记: 李六小 (2021.05 至 2025 在任, 后调呼和浩特市国防动员办公室党组书记)
- 更早前任县委书记: 张永文
- 前任县长: 高峰 (2024-05 因工作调整辞职) -> 张志魁 (2024-05 代县长 -> 2024-12 县长 -> 2026-05 县委书记)
- 现任县长: 王孛 (2026-07 代县长/县长提名人选)

参考构建：scripts/build/build_托克托县_data.py (同属呼和浩特市县域)。
"""

import sys
import os
import sqlite3  # noqa: F401  (used via gov_relation.runner.run_build)

# Robustly add repo root to path (works from staging dir, scripts/build/, or repo root)
from pathlib import Path

_REPO = Path(__file__).resolve().parent
while not (_REPO / "gov_relation").is_dir():
    if _REPO == _REPO.parent:
        break
    _REPO = _REPO.parent
sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "和林格尔县"
DB_PATH = DATABASE_DIR / "和林格尔县_network.db"
GEXF_PATH = GRAPH_DIR / "和林格尔县_network.gexf"

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共和林格尔县委员会", "type": "党委", "level": "县处级", "parent": "中共呼和浩特市委", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 2, "name": "和林格尔县人民政府", "type": "政府", "level": "县处级", "parent": "呼和浩特市人民政府", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 3, "name": "和林格尔县人大常委会", "type": "人大", "level": "县处级", "parent": "呼和浩特市人大常委会", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 4, "name": "和林格尔县政协", "type": "政协", "level": "县处级", "parent": "呼和浩特市政协", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 5, "name": "中共和林格尔县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共呼和浩特市纪委", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 6, "name": "中共和林格尔县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共和林格尔县委员会", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 7, "name": "中共和林格尔县委组织部", "type": "党委", "level": "县处级", "parent": "中共和林格尔县委员会", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 8, "name": "中共和林格尔县委宣传部", "type": "党委", "level": "县处级", "parent": "中共和林格尔县委员会", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 9, "name": "中共和林格尔县委统战部", "type": "党委", "level": "县处级", "parent": "中共和林格尔县委员会", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 10, "name": "和林格尔县人民武装部", "type": "事业单位", "level": "县处级", "parent": "呼和浩特警备区", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 11, "name": "和林格尔县公安局", "type": "政府", "level": "县处级", "parent": "和林格尔县人民政府", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 12, "name": "和林格尔县人民法院", "type": "事业单位", "level": "县处级", "parent": "呼和浩特市中级人民法院", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 13, "name": "和林格尔县人民检察院", "type": "事业单位", "level": "县处级", "parent": "呼和浩特市人民检察院", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 14, "name": "呼和浩特和林格尔乳业开发区（园区）", "type": "开发区", "level": "县处级", "parent": "和林格尔县人民政府", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 15, "name": "中共和林格尔县委办公室", "type": "党委", "level": "县处级", "parent": "中共和林格尔县委员会", "location": "内蒙古自治区呼和浩特市和林格尔县"},
    {"id": 16, "name": "和林格尔县纪律检查委员会监察委员会", "type": "纪委", "level": "县处级", "parent": "中共和林格尔县纪律检查委员会", "location": "内蒙古自治区呼和浩特市和林格尔县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ 县委领导 ═══
    # 1 — 张志魁 — 县委书记
    {"id": 1, "name": "张志魁", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年5月", "birthplace": "山东省单县",
     "education": "山东省委党校研究生/文学学士",
     "party_join": "2004年5月", "work_start": "2005年7月",
     "current_post": "和林格尔县委书记", "current_org": "中共和林格尔县委员会",
     "source": "helin.gov.cn/百度百科/呼和浩特市委组织部2026-05任前公示"},
    # 2 — 王孛 — 县委副书记、县长
    {"id": 2, "name": "王孛", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年6月", "birthplace": "待查",
     "education": "大学",
     "party_join": "2003年11月", "work_start": "2001年9月",
     "current_post": "和林格尔县委副书记、县政府党组书记、县长提名人选（代县长）", "current_org": "和林格尔县人民政府",
     "source": "helin.gov.cn/领导之窗 2026-07-20"},
    # 3 — 李慧梅 — 县委副书记（专职）
    {"id": 3, "name": "李慧梅", "gender": "女", "ethnicity": "待查",
     "birth": "1981年1月", "birthplace": "内蒙古呼和浩特市",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委副书记（专职）", "current_org": "中共和林格尔县委员会",
     "source": "百度百科/十六大公报 2026-07"},
    # 4 — 杜小光 — 县委常委、县委办主任
    {"id": 4, "name": "杜小光", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1982年8月", "birthplace": "内蒙古赤峰市松山区",
     "education": "大学",
     "party_join": "2003年6月", "work_start": "2004年7月",
     "current_post": "和林格尔县委常委、县委办主任", "current_org": "中共和和县委办公室",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 5 — 郝玉峰 — 县委常委、纪委书记、监委代主任
    {"id": 5, "name": "郝玉峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年8月", "birthplace": "待查",
     "education": "中央党校大学，经济学学士",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委、县纪委书记、监委代主任", "current_org": "和县委监委",
     "source": "百度百科/县纪委监察委网站"},
    # 6 — 康绍鹏 — 县委常委、组织部部长
    {"id": 6, "name": "康绍鹏", "gender": "男", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委、组织部部长", "current_org": "和县委组织部",
     "source": "helin.gov.cn 县级领导接访日程表 2025"},
    # 7 — 郭晓虎 — 县委常委
    {"id": 7, "name": "郭晓虎", "gender": "男", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委", "current_org": "中共和林格尔县委员会",
     "source": "百度百科/十六大公报 2026-07"},
    # 8 — 柴斌 — 县委常委、人武部政委
    {"id": 8, "name": "柴斌", "gender": "男", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委、人武部政委", "current_org": "和林格尔县人民武装部",
     "source": "helin.gov.cn 人武部第一书记任职大会 2026-07"},
    # 9 — 刘斌 — 县委常委
    {"id": 9, "name": "刘斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年8月", "birthplace": "待查",
     "education": "研究生，公共管理硕士",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委", "current_org": "中共和林格尔县委员会",
     "source": "百度百科"},
    # 10 — 贾微 — 县委常委、副县长
    {"id": 10, "name": "贾微", "gender": "男", "ethnicity": "满族",
     "birth": "1985年1月", "birthplace": "内蒙古翁牛特旗",
     "education": "工学士",
     "party_join": "2006年6月", "work_start": "2007年8月",
     "current_post": "和林格尔县委常委、副县长", "current_org": "和林格尔县人民政府",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 11 — 呼静 — 常务副县长
    {"id": 11, "name": "呼静", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委、常务副县长", "current_org": "和林格尔县人民政府",
     "source": "和林格尔县政府 2025-04 分工通知"},
    # 12 — 麻永华 — 副县长（挂职）
    {"id": 12, "name": "麻永华", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年7月", "birthplace": "河南省平舆县",
     "education": "大学",
     "party_join": "2017年8月", "work_start": "2002年7月",
     "current_post": "和林格尔县委常委、副县长（挂职）", "current_org": "和林格尔县人民政府",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 13 — 赵剑青 — 副县长
    {"id": 13, "name": "赵剑青", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年7月", "birthplace": "呼和浩特市赛罕区",
     "education": "研究生",
     "party_join": "2002年7月", "work_start": "1995年12月",
     "current_post": "和林格尔县政府党组成员、副县长", "current_org": "和林格尔县人民政府",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 14 — 徐鹏 — 副县长
    {"id": 14, "name": "徐鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年10月", "birthplace": "内蒙古托克托县",
     "education": "大学",
     "party_join": "2012年7月", "work_start": "2008年8月",
     "current_post": "和林格尔县政府党组成员、副县长", "current_org": "和林格尔县人民政府",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 15 — 张晶 — 副县长
    {"id": 15, "name": "张晶", "gender": "女", "ethnicity": "回族",
     "birth": "1985年9月", "birthplace": "内蒙古呼和浩特市",
     "education": "大学",
     "party_join": "2012年6月", "work_start": "2008年10月",
     "current_post": "和林格尔县政府党组成员、副县长", "current_org": "和林格尔县人民政府",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 16 — 张永胜 — 副县长兼公安局局长
    {"id": 16, "name": "张永胜", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年11月", "birthplace": "待查",
     "education": "大学",
     "party_join": "2002年6月", "work_start": "1997年9月",
     "current_post": "和林格尔县政府副县长、公安局局长", "current_org": "和林格尔县公安局",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 17 — 白皓 — 政府党组成员
    {"id": 17, "name": "白皓", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年3月", "birthplace": "内蒙古和林格尔县",
     "education": "大学",
     "party_join": "2006年6月", "work_start": "1998年9月",
     "current_post": "和林格尔县政府党组成员", "current_org": "和林格尔县人民政府",
     "source": "helin.gov.cn 领导之窗 bio"},
    # 18 — 魏斌 — 常委、副县长、乳业开发区主任
    {"id": 18, "name": "魏斌", "gender": "男", "ethnicity": "满族",
     "birth": "1970年2月", "birthplace": "待查",
     "education": "大学",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委、副县长，呼和浩特和林格尔乳业开发区管委会主任（拟任县政协主席）", "current_org": "和林格尔县人民政府",
     "source": "呼和浩特市委组织部 2026-01 任前公示"},
    # 19 — 刘宁 — 县委常委、统战部部长
    {"id": 19, "name": "刘宁", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县委常委、统战部部长、政协党组副书记", "current_org": "和林格尔县委统战部",
     "source": "和林格尔县政协十届五次会议报道 2026-01"},
    # 20 — 张全胜 — 人大常委会主任
    {"id": 20, "name": "张全胜", "gender": "男", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县人大常委会主任", "current_org": "和林格尔县人大常委会",
     "source": "和林格尔县十六届人大五次会议 2026-01"},
    # 21 — 王来柱 — 政协主席
    {"id": 21, "name": "王来柱", "gender": "男", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "和林格尔县政协主席", "current_org": "和林格尔县政协",
     "source": "和林格尔县政协十届五次会议 2026-01"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张志魁
    {"person_id": 1, "org_id": 1, "title": "和林格尔县委副书记、代理县长", "start_date": "2024-05", "end_date": "2024-12", "rank": "县处级正职", "note": "2024-05-31 县人大常委会任命为副县长、代理县长"},
    {"person_id": 1, "org_id": 2, "title": "和林格尔县人民政府县长", "start_date": "2024-12", "end_date": "2026-05", "rank": "县处级正职", "note": "2024-12 县十六届人大四次会议当选县长"},
    {"person_id": 1, "org_id": 1, "title": "和林格尔县委书记", "start_date": "2026-05", "end_date": "present", "rank": "县处级正职", "note": "2026-05 呼和浩特市委公示拟任旗县党委书记；现任县委书记、县人武部第一书记"},
    # 王孛
    {"person_id": 2, "org_id": 1, "title": "和林格尔县委副书记", "start_date": "2026年", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "和林格尔县政府党组书记、县长提名人选（代县长）", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职", "note": "helin.gov.cn 领导之窗 2026-07-20"},
    {"person_id": 2, "org_id": 14, "title": "和林格尔乳业开发区党工委书记", "start_date": "2026年", "end_date": "present", "rank": "", "note": ""},
    # 李慧梅
    {"person_id": 3, "org_id": 1, "title": "和林格尔县委副书记（专职）", "start_date": "2026-07", "end_date": "present", "rank": "县处级副职", "note": "2026-07-30 十六届县委一次全会选举副书记"},
    # 杜小光
    {"person_id": 4, "org_id": 1, "title": "和林格尔县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "和林格尔县委办主任", "start_date": "2023", "end_date": "present", "rank": "", "note": "2024-03 报道：县委常委、县委办主任杜小光"},
    # 郝玉峰
    {"person_id": 5, "org_id": 5, "title": "和林格尔县委常委、县纪委书记、监委代主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 康绍鹏
    {"person_id": 6, "org_id": 7, "title": "和林格尔县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2025-03 接访日程：康绍鹏 主任组织部部长"},
    # 郭晓虎
    {"person_id": 7, "org_id": 1, "title": "和林格尔县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 柴斌
    {"person_id": 8, "org_id": 1, "title": "和林格尔县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "和林格尔县人武部政委", "start_date": "", "end_date": "present", "rank": "", "note": "2026-07-24 人武部第一书记任职大会由柴斌主持"},
    # 刘斌
    {"person_id": 9, "org_id": 1, "title": "和林格尔县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 贾微
    {"person_id": 10, "org_id": 1, "title": "和林格尔县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "和林格尔县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 呼静
    {"person_id": 11, "org_id": 2, "title": "和林格尔县委常委、常务副县长", "start_date": "2025-04", "end_date": "present", "rank": "县处级副职", "note": "2025-04 县政府分工通知"},
    # 麻永华
    {"person_id": 12, "org_id": 1, "title": "和林格尔县委常委（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "和林格尔县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 赵剑青
    {"person_id": 13, "org_id": 2, "title": "和林格尔县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 徐鹏
    {"person_id": 14, "org_id": 2, "title": "和林格尔县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张晶
    {"person_id": 15, "org_id": 2, "title": "和林格尔县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张永胜
    {"person_id": 16, "org_id": 2, "title": "和林格尔县政府副县长、公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管公安"},
    # 白皓
    {"person_id": 17, "org_id": 2, "title": "和林格尔县政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 魏斌
    {"person_id": 18, "org_id": 1, "title": "和林格尔县委常委、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "内蒙古和林格尔新区党工委委员"},
    {"person_id": 18, "org_id": 4, "title": "和林格尔县政协主席（提名人选）", "start_date": "2026-01", "end_date": "present", "rank": "县处级正职", "note": "2026-01 呼和浩特市委公示拟提县级政协主席"},
    # 刘宁
    {"person_id": 19, "org_id": 9, "title": "和林格尔县委常委、统战部部长、政协党组副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-01-30 政协联组讨论"},
    # 张全胜
    {"person_id": 20, "org_id": 3, "title": "和林格尔县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-01-28 十六届人大五次会议"},
    # 王来柱
    {"person_id": 21, "org_id": 4, "title": "和林格尔县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-01 政协十届五次会议"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政正职：书记与县长
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "和林格尔县党政正职搭档：县委书记与代县长", "overlap_org": "和林格尔县委员会/政府", "overlap_period": "2026-07—present"},
    # 张志魁与王孛（副转正/继任：张志魁由县长转书记，王孛接任县长）
    {"person_a": 1, "person_b": 2, "type": "promotion_chain", "context": "张志魁由县长升任县委书记，王孛继任县长（predecessor_successor）", "overlap_org": "和林格尔县人民政府", "overlap_period": "2026"},
    # 书记-副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与专职副书记（县委班子）", "overlap_org": "和林格尔县委员会", "overlap_period": "2026-07-present"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县委副书记班子成员", "overlap_org": "和林格尔县委员会", "overlap_period": "2026-07-present"},
    # 书记-常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委常委会：书记与县委办主任杜小光", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委常委会：书记与纪委书记郝玉峰", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委常委会：书记与组织部部长康绍鹏", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委常委会：书记与郭晓虎", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委常委会：书记与人武部政委柴斌", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委常委会：书记与刘斌", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    # 县长-副县长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与常务副县长呼静", "overlap_org": "和林格尔县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长与县委常委、副县长贾微", "overlap_org": "和林格尔县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与挂职副县长", "overlap_org": "和林格尔县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长与副县长、公安局长张永胜", "overlap_org": "和林格尔县人民政府", "overlap_period": "present"},
    # 常委互连（并列班子）
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委办与组织部（常委）", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "纪委与组织部（常委互连）", "overlap_org": "和林格尔县委员会", "overlap_period": "present"},
    {"person_a": 10, "person_b": 18, "type": "overlap", "context": "副县长同僚（工业/开发区）", "overlap_org": "和林格尔县人民政府", "overlap_period": "present"},
    # 政协与统战
    {"person_a": 21, "person_b": 18, "type": "predecessor_successor", "context": "政协主席王来柱与政协主席提名人选魏某（继任关系）", "overlap_org": "和林格尔县政协", "overlap_period": "2026"},
    {"person_a": 19, "person_b": 21, "type": "superior_subordinate", "context": "统战部部长（政协党组副书记）与政协主席", "overlap_org": "和林格尔县政协/统战部", "overlap_period": "present"},
    ]

# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
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
    print("Build complete.")