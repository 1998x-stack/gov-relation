#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 岚皋县, 安康市, 陕西省."""

import os
import sys
from datetime import date
from pathlib import Path

# Add project root to path so gov_relation module is importable
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

import sqlite3  # noqa: F401 — used by gov_relation.runner internally

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths (staging) ────────────────────────────────────────────────────
TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / "岚皋县_network.db"
GEXF_PATH = TMP_DIR / "岚皋县_network.gexf"

# ── DATA ───────────────────────────────────────────────────────────────

TODAY = date.today().strftime("%Y-%m-%d")

persons = [
    # ── Current Top Leaders ──
    # 县委书记 魏小林 (confirmed from langao.gov.cn leadership page)
    {"id": 1, "name": "魏小林", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-12", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委书记", "current_org": "中共岚皋县委员会",
     "source": "https://www.langao.gov.cn/Content-2711495.html"},

    # 县长 王仁康 (confirmed from langao.gov.cn leadership page)
    {"id": 2, "name": "王仁康", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委副书记、县长", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-2712236.html"},

    # ── 县委常委会成员 ──
    # 县委副书记（专职）王诚 (confirmed from langao.gov.cn)
    {"id": 3, "name": "王诚", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-03", "birthplace": "", "education": "在职研究生，教育学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委副书记、县委党校校长", "current_org": "中共岚皋县委员会",
     "source": "https://www.langao.gov.cn/Content-2811766.html"},

    # 县委副书记（挂职）刘晓康 (from langao.gov.cn)
    {"id": 4, "name": "刘晓康", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-01", "birthplace": "", "education": "研究生，法律硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委副书记（挂职）", "current_org": "中共岚皋县委员会",
     "source": "https://www.langao.gov.cn/Content-2843493.html"},

    # 县委常委、常务副县长 祖白云 (confirmed from langao.gov.cn)
    {"id": 5, "name": "祖白云", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-03", "birthplace": "", "education": "研究生，工商管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、县政府党组副书记、副县长", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-2844947.html"},

    # 县委常委、副县长 郑毅 (confirmed from langao.gov.cn)
    {"id": 6, "name": "郑毅", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-07", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、县政府副县长", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-1659206.html"},

    # 县委常委、宣传部部长 欧阳周菲 (confirmed from langao.gov.cn)
    {"id": 7, "name": "欧阳周菲", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、宣传部部长", "current_org": "中共岚皋县委宣传部",
     "source": "https://www.langao.gov.cn/Content-2310607.html"},

    # 县委常委、县人武部上校政委 唐鑫 (confirmed from langao.gov.cn)
    {"id": 8, "name": "唐鑫", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、县人武部上校政治委员", "current_org": "中国人民解放军岚皋县人武部",
     "source": "https://www.langao.gov.cn/Content-2777234.html"},

    # 县委常委、县纪委书记、县监委主任 李仕阳 (confirmed from langao.gov.cn)
    {"id": 9, "name": "李仕阳", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-01", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、县纪委书记、县监委主任", "current_org": "中共岚皋县纪律检查委员会",
     "source": "https://www.langao.gov.cn/Content-2310609.html"},

    # 县委常委、政法委书记 卢修春 (confirmed from langao.gov.cn)
    {"id": 10, "name": "卢修春", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、政法委书记", "current_org": "中共岚皋县委政法委员会",
     "source": "https://www.langao.gov.cn/Content-1659184.html"},

    # 县委常委、组织部部长 刘妮娜 (confirmed from langao.gov.cn)
    {"id": 11, "name": "刘妮娜", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-11", "birthplace": "", "education": "研究生，文学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、组织部部长、县考核委员会办公室主任", "current_org": "中共岚皋县委组织部",
     "source": "https://www.langao.gov.cn/Content-2310657.html"},

    # 县委常委、统战部部长 张涛 (confirmed from langao.gov.cn)
    {"id": 12, "name": "张涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-09", "birthplace": "", "education": "在职研究生，文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、统战部部长、县政协党组副书记", "current_org": "中共岚皋县委统战部",
     "source": "https://www.langao.gov.cn/Content-2713904.html"},

    # 县委常委、副县长（挂职）周丽娟 (confirmed from langao.gov.cn)
    {"id": 13, "name": "周丽娟", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-08", "birthplace": "", "education": "研究生，管理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县委常委、县政府副县长（挂职）", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-2876823.html"},

    # ── 县政府领导班子（非常委）──
    # 副县长 伍玉兰 (confirmed from langao.gov.cn)
    {"id": 14, "name": "伍玉兰", "gender": "女", "ethnicity": "汉族",
     "birth": "1974-05", "birthplace": "", "education": "本科",
     "party_join": "", "work_start": "",
     "current_post": "岚皋县政府副县长", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-1680097.html"},

    # 副县长、县公安局局长 陈登林 (confirmed from langao.gov.cn)
    {"id": 15, "name": "陈登林", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县政府党组成员、副县长、县公安局党委书记、局长、督察长", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-2310705.html"},

    # 副县长 但功军 (confirmed from langao.gov.cn)
    {"id": 16, "name": "但功军", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县政府党组成员、副县长", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-2310706.html"},

    # 副县长 徐远航 (confirmed from langao.gov.cn)
    {"id": 17, "name": "徐远航", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-05", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县政府党组成员、副县长", "current_org": "岚皋县人民政府",
     "source": "https://www.langao.gov.cn/Content-2310708.html"},

    # ── 人大、政协主要领导 ──
    # 县人大常委会主任 谢荧 (confirmed from langao.gov.cn)
    {"id": 18, "name": "谢荧", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县人大常委会党组书记、主任", "current_org": "岚皋县人大常委会",
     "source": "https://www.langao.gov.cn/Content-2394043.html"},

    # 县政协主席 张永斌 (confirmed from langao.gov.cn)
    {"id": 19, "name": "张永斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-05", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岚皋县政协党组书记、主席", "current_org": "岚皋县政协",
     "source": "https://www.langao.gov.cn/Content-2394042.html"},
]

organizations = [
    {"id": 1, "name": "中共岚皋县委员会", "type": "党委", "level": "县处级",
     "parent": "中共安康市委员会", "location": "陕西省安康市岚皋县"},
    {"id": 2, "name": "岚皋县人民政府", "type": "政府", "level": "县处级",
     "parent": "安康市人民政府", "location": "陕西省安康市岚皋县"},
    {"id": 3, "name": "中共岚皋县委宣传部", "type": "党委", "level": "正科级",
     "parent": "中共岚皋县委员会", "location": "陕西省安康市岚皋县"},
    {"id": 4, "name": "中共岚皋县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共岚皋县委员会", "location": "陕西省安康市岚皋县"},
    {"id": 5, "name": "中共岚皋县委政法委员会", "type": "党委", "level": "正科级",
     "parent": "中共岚皋县委员会", "location": "陕西省安康市岚皋县"},
    {"id": 6, "name": "中共岚皋县委组织部", "type": "党委", "level": "正科级",
     "parent": "中共岚皋县委员会", "location": "陕西省安康市岚皋县"},
    {"id": 7, "name": "中共岚皋县委统战部", "type": "党委", "level": "正科级",
     "parent": "中共岚皋县委员会", "location": "陕西省安康市岚皋县"},
    {"id": 8, "name": "岚皋县公安局", "type": "政府", "level": "正科级",
     "parent": "岚皋县人民政府", "location": "陕西省安康市岚皋县"},
    {"id": 9, "name": "中国人民解放军岚皋县人武部", "type": "政府", "level": "正团级",
     "parent": "安康军分区", "location": "陕西省安康市岚皋县"},
    {"id": 10, "name": "岚皋县人大常委会", "type": "人大", "level": "县处级",
     "parent": "岚皋县", "location": "陕西省安康市岚皋县"},
    {"id": 11, "name": "岚皋县政协", "type": "政协", "level": "县处级",
     "parent": "岚皋县", "location": "陕西省安康市岚皋县"},
    {"id": 12, "name": "中共岚皋县委党校", "type": "事业单位", "level": "正科级",
     "parent": "中共岚皋县委员会", "location": "陕西省安康市岚皋县"},
]

positions = [
    # 魏小林
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "主持县委全面工作，联系县人大常委会、县政协工作"},
    # Earlier: 岚皋县委副书记、代县长、县长
    # Earlier: 宁陕县委常委、副县长、组织部部长
    # Earlier: 安康市委办公室

    # 王仁康
    {"person_id": 2, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "兼任县长"},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "领导县政府全面工作"},
    # Earlier: 安康恒口示范区（试验区）党工委副书记、管委会主任、恒口镇党委书记（兼）
    # Earlier: 石泉县委常委、副县长、纪委书记

    # 王诚
    {"person_id": 3, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "专职副书记，分管党建、三农、县委党校"},
    {"person_id": 3, "org_id": 12, "title": "县委党校校长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},

    # 刘晓康
    {"person_id": 4, "org_id": 1, "title": "县委副书记（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "苏陕对口帮扶协作（来自常州）"},

    # 祖白云
    {"person_id": 5, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "县政府党组副书记"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责政府常务工作"},

    # 郑毅
    {"person_id": 6, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 欧阳周菲
    {"person_id": 7, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 3, "title": "宣传部部长",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": ""},

    # 唐鑫
    {"person_id": 8, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 9, "title": "县人武部上校政治委员",
     "start_date": "", "end_date": "present", "rank": "正团级",
     "note": "负责军事、双拥工作"},

    # 李仕阳
    {"person_id": 9, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 9, "org_id": 4, "title": "县纪委书记、县监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 卢修春
    {"person_id": 10, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 10, "org_id": 5, "title": "政法委书记",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": ""},

    # 刘妮娜
    {"person_id": 11, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 11, "org_id": 6, "title": "组织部部长",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": "兼任县考核委员会办公室主任"},

    # 张涛
    {"person_id": 12, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 12, "org_id": 7, "title": "统战部部长",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": "兼任县政协党组副书记"},

    # 周丽娟
    {"person_id": 13, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "挂职"},
    {"person_id": 13, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "中国建设银行对口帮扶"},

    # 伍玉兰
    {"person_id": 14, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "无党派人士，分管教育体育、卫健、医保等"},

    # 陈登林
    {"person_id": 15, "org_id": 2, "title": "副县长",
     "start_date": "2021-11", "end_date": "present", "rank": "县处级副职",
     "note": "分管公安、信访、司法、生态环境等"},
    {"person_id": 15, "org_id": 8, "title": "县公安局党委书记、局长、督察长",
     "start_date": "2021-11", "end_date": "present", "rank": "正科级",
     "note": ""},

    # 但功军
    {"person_id": 16, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管住建、自然资源、市场监管等"},

    # 徐远航
    {"person_id": 17, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管交通运输、民政等"},

    # 谢荧
    {"person_id": 18, "org_id": 10, "title": "县人大常委会党组书记、主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},

    # 张永斌
    {"person_id": 19, "org_id": 11, "title": "县政协党组书记、主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},
]

relationships = [
    # 书记-县长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政正职搭档", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2023-2026"},

    # 书记-专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与专职副书记搭档", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},

    # 书记-挂职副书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与挂职副书记（苏陕协作）", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},

    # 书记-各常委
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与常务副县长工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与常委副县长工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与宣传部部长工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2023-2026"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与人武部政委（常委）工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与纪委书记工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与政法委书记工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记与组织部部长工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记与统战部部长工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "县委书记与挂职副县长（常委）工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},

    # 县长-各副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与常务副县长工作关系", "overlap_org": "岚皋县人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "岚皋县人民政府",
     "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与挂职副县长工作关系", "overlap_org": "岚皋县人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "岚皋县人民政府",
     "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长兼公安局长工作关系", "overlap_org": "岚皋县人民政府",
     "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "岚皋县人民政府",
     "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "岚皋县人民政府",
     "overlap_period": "2024-2026"},

    # 专职副书记-各常委
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "专职副书记与宣传部部长同届县委常委会", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 9, "type": "overlap",
     "context": "专职副书记与纪委书记同为县委常委会成员", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 10, "type": "overlap",
     "context": "专职副书记与政法委书记同在县委常委会", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 11, "type": "overlap",
     "context": "专职副书记与组织部部长工作关系", "overlap_org": "中共岚皋县委员会",
     "overlap_period": "2025-2026"},

    # 人大主任-政协主席
    {"person_a": 18, "person_b": 19, "type": "overlap",
     "context": "人大主任与政协主席同届工作关系", "overlap_org": "岚皋县",
     "overlap_period": "2022-2026"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="岚皋县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")
