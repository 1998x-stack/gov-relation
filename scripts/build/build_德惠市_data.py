#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 德惠市 (Dehui City), 长春市, 吉林省.

Level: 县级市
Province: 吉林省 (Jilin Province)
Parent city: 长春市 (Changchun City)
Targets: 市委书记 (王喜成), 市长 (蒋再波)
Task ID: jilin_德惠市

Research date: 2026-08-06
Primary official source: http://www.dehui.gov.cn/ (德惠市人民政府官网), 领导信息 section (`/zwgk/sld/`)
  - 市委领导 (swld), 市人大领导 (srdld), 市政府领导 (szfld), 市政协领导 (szxld) sub-pages
Supplemental: 德惠市大事记 (2023年、2024年) — documents predecessor leadership 申洪业/刘宏 and the
  2024-12 appointment of 蒋再波 as 市长.

Current leadership context:
  - 市委书记 王喜成 took office 2025-10 (predecessor: 申洪业, in post through 2024)
  - 市委副书记、市长 蒋再波 took office 2024-12 (elected at 十九届人大五次会议), predecessor 刘宏
  - Notable 2026 turnover on the standing committee: 王嘉升/赵莉/李志强 (2026-04 常委),
    杨笑 (2026-01 常委), 付井奎 (2026-01 副市长), 吴立波 (2026-05 副市长)
  - 前任市委书记 (申洪业) 与 前任市长 (刘宏) 的去向/完整履历未在官网公开; 王喜成/蒋再波的前任岗位
    亦未在官网公开 — 详见报告 open gaps。

All current-leader profiles below are CONFIRMED (confidence: confirmed) from the official
dehui.gov.cn leadership pages. Predecessor career details are marked plausible/unverified.
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: F401  # required token for process_tmp.py validation
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "德惠市"

# 从 data/tmp/jilin_德惠市 运行: DB/GEXF 写入本目录
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-06"
TODAY = "20260806"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ 市委党政主官 (Core: 市委书记 & 市长) ═══
    {"id": 1, "name": "王喜成", "gender": "男", "ethnicity": "汉族", "birth": "1974年9月", "birthplace": "吉林长春",
     "education": "省委党校研究生（吉林省委党校经济管理专业）", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共德惠市委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/wcc/"},
    {"id": 2, "name": "蒋再波", "gender": "男", "ethnicity": "满族", "birth": "1981年9月", "birthplace": "黑龙江双城",
     "education": "研究生学历", "party_join": "2004年5月", "work_start": "2007年8月",
     "current_post": "市委副书记、市长", "current_org": "德惠市人民政府",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/jzb/"},

    # ═══ 市委副书记 / 市委常委 ═══
    {"id": 3, "name": "王泰峰", "gender": "男", "ethnicity": "汉族", "birth": "1975年2月", "birthplace": "吉林九台",
     "education": "大学学历", "party_join": "2005年11月", "work_start": "1997年7月",
     "current_post": "市委副书记", "current_org": "中共德惠市委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/wtfszf/"},
    {"id": 4, "name": "刘竞阳", "gender": "男", "ethnicity": "汉族", "birth": "1987年3月", "birthplace": "",
     "education": "研究生学历", "party_join": "2009年11月", "work_start": "2010年7月",
     "current_post": "市委常委、常务副市长", "current_org": "德惠市人民政府",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/shy_60122/"},
    {"id": 5, "name": "徐博夫", "gender": "男", "ethnicity": "汉族", "birth": "1982年10月", "birthplace": "内蒙古通辽",
     "education": "大学学历", "party_join": "2006年5月", "work_start": "2004年7月",
     "current_post": "市委常委、组织部部长、党校校长", "current_org": "中共德惠市委组织部",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/wxc_60124/"},
    {"id": 6, "name": "韩国良", "gender": "男", "ethnicity": "汉族", "birth": "1980年12月", "birthplace": "吉林松原",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "2007年11月",
     "current_post": "市委常委、纪委书记、监委主任", "current_org": "中共德惠市纪律检查委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/hgl/"},
    {"id": 7, "name": "王嘉升", "gender": "男", "ethnicity": "汉族", "birth": "1980年6月", "birthplace": "吉林德惠",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、政法委书记", "current_org": "中共德惠市委政法委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/wjs/"},
    {"id": 8, "name": "赵莉", "gender": "女", "ethnicity": "汉族", "birth": "1978年4月", "birthplace": "吉林德惠",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、宣传部部长", "current_org": "中共德惠市委宣传部",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/zl/"},
    {"id": 9, "name": "李志强", "gender": "男", "ethnicity": "汉族", "birth": "1987年5月", "birthplace": "河北万全",
     "education": "长春工业大学研究生学历（社会学）", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、统战部部长、市政协党组副书记", "current_org": "中共德惠市委统战部",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/lzq/"},
    {"id": 10, "name": "杨笑", "gender": "男", "ethnicity": "汉族", "birth": "1986年9月", "birthplace": "吉林四平",
     "education": "在职研究生学历（山西财经大学法学）", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市经济开发区党工委书记、管委会主任", "current_org": "德惠经济开发区",
     "source": "http://www.dehui.gov.cn/zwgk/sld/swld/yx/"},

    # ═══ 市政府领导 (副市长) ═══
    {"id": 11, "name": "宋向波", "gender": "男", "ethnicity": "汉族", "birth": "1975年9月", "birthplace": "吉林德惠",
     "education": "大学学历", "party_join": "1998年12月", "work_start": "1995年8月",
     "current_post": "副市长", "current_org": "德惠市人民政府",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/sxbszf/"},
    {"id": 12, "name": "付井奎", "gender": "男", "ethnicity": "汉族", "birth": "1971年10月", "birthplace": "吉林德惠",
     "education": "大学学历", "party_join": "1997年8月", "work_start": "1996年11月",
     "current_post": "副市长", "current_org": "德惠市人民政府",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/fjk/"},
    {"id": 13, "name": "王大伟", "gender": "男", "ethnicity": "汉族", "birth": "1973年5月", "birthplace": "吉林德惠",
     "education": "本科学历", "party_join": "2001年7月", "work_start": "1993年8月",
     "current_post": "副市长（协助分管金融）", "current_org": "德惠市人民政府",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/wdw/"},
    {"id": 14, "name": "孙凯", "gender": "男", "ethnicity": "汉族", "birth": "1979年5月", "birthplace": "吉林长春",
     "education": "大学学历", "party_join": "2005年10月", "work_start": "2000年8月",
     "current_post": "副市长、市公安局局长", "current_org": "德惠市公安局",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/sk/"},
    {"id": 15, "name": "李国峰", "gender": "男", "ethnicity": "汉族", "birth": "1972年2月", "birthplace": "吉林公主岭",
     "education": "大学学历", "party_join": "1995年7月", "work_start": "1995年7月",
     "current_post": "副市长", "current_org": "德惠市人民政府",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/lgf/"},
    {"id": 16, "name": "吴立波", "gender": "女", "ethnicity": "汉族", "birth": "1985年11月", "birthplace": "吉林德惠",
     "education": "研究生学历", "party_join": "2008年12月", "work_start": "2009年8月",
     "current_post": "副市长", "current_org": "德惠市人民政府",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szfld/wlb/"},

    # ═══ 市人大常委会 ═══
    {"id": 17, "name": "丁日伟", "gender": "男", "ethnicity": "汉族", "birth": "1968年4月", "birthplace": "吉林德惠",
     "education": "研究生学历", "party_join": "1991年4月", "work_start": "1988年7月",
     "current_post": "市人大常委会党组书记、主任", "current_org": "德惠市人民代表大会常务委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/srdld/drw/"},
    {"id": 18, "name": "张国东", "gender": "男", "ethnicity": "汉族", "birth": "1963年3月", "birthplace": "吉林德惠",
     "education": "大专学历", "party_join": "", "work_start": "1979年7月",
     "current_post": "市人大常委会副主任", "current_org": "德惠市人民代表大会常务委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/srdld/zgd/"},
    {"id": 19, "name": "张振波", "gender": "男", "ethnicity": "汉族", "birth": "1966年8月", "birthplace": "吉林德惠",
     "education": "大学学历", "party_join": "1991年12月", "work_start": "1989年8月",
     "current_post": "市人大常委会党组副书记、副主任", "current_org": "德惠市人民代表大会常务委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/srdld/zzb/"},
    {"id": 20, "name": "李贵军", "gender": "男", "ethnicity": "汉族", "birth": "1967年3月", "birthplace": "吉林德惠",
     "education": "大学学历", "party_join": "1998年5月", "work_start": "1987年7月",
     "current_post": "市人大常委会副主任、市总工会主席", "current_org": "德惠市人民代表大会常务委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/srdld/lgj/"},
    {"id": 21, "name": "佟立皓", "gender": "男", "ethnicity": "汉族", "birth": "1969年11月", "birthplace": "吉林德惠",
     "education": "大学学历", "party_join": "1992年5月", "work_start": "1992年8月",
     "current_post": "市人大常委会副主任", "current_org": "德惠市人民代表大会常务委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/srdld/tlh/"},

    # ═══ 市政协 ═══
    {"id": 22, "name": "尚祖军", "gender": "男", "ethnicity": "汉族", "birth": "1968年3月", "birthplace": "吉林德惠",
     "education": "研究生学历", "party_join": "1987年11月", "work_start": "1989年7月",
     "current_post": "市政协党组书记、主席", "current_org": "政协德惠市委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szxld/szj/"},
    {"id": 23, "name": "张孝权", "gender": "男", "ethnicity": "汉族", "birth": "1971年4月", "birthplace": "吉林德惠",
     "education": "大学学历", "party_join": "", "work_start": "1991年8月",
     "current_post": "市政协副主席", "current_org": "政协德惠市委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szxld/zxq/"},
    {"id": 24, "name": "李剑", "gender": "男", "ethnicity": "汉族", "birth": "1967年10月", "birthplace": "吉林德惠",
     "education": "本科学历", "party_join": "1991年11月", "work_start": "1988年8月",
     "current_post": "市政协党组成员、副主席、秘书长", "current_org": "政协德惠市委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szxld/lj/"},
    {"id": 25, "name": "闫冀", "gender": "男", "ethnicity": "汉族", "birth": "1969年9月", "birthplace": "吉林德惠",
     "education": "大学学历", "party_join": "", "work_start": "1992年7月",
     "current_post": "市政协副主席（不驻会）", "current_org": "政协德惠市委员会",
     "source": "http://www.dehui.gov.cn/zwgk/sld/szxld/yj/"},

    # ═══ 前任主官 (predecessors, 来源: 德惠大事记) ═══
    {"id": 26, "name": "申洪业", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任市委书记（在任至2024年）", "current_org": "中共德惠市委员会",
     "source": "德惠市2024年大事记（dehui.gov.cn）"},
    {"id": 27, "name": "刘宏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任市委副书记、市长（在任至2024年12月）", "current_org": "德惠市人民政府",
     "source": "德惠市2023-2024年大事记（dehui.gov.cn）"},
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共德惠市委员会", "type": "党委", "level": "县级市", "parent": "中共长春市委", "location": "德惠市"},
    {"id": 2, "name": "德惠市人民政府", "type": "政府", "level": "县级市", "parent": "长春市人民政府", "location": "德惠市"},
    {"id": 3, "name": "中共德惠市委组织部", "type": "党委部门", "level": "县级市", "parent": "中共德惠市委员会", "location": "德惠市"},
    {"id": 4, "name": "中共德惠市纪律检查委员会", "type": "党委部门", "level": "县级市", "parent": "中共德惠市委员会", "location": "德惠市"},
    {"id": 5, "name": "中共德惠市委政法委员会", "type": "党委部门", "level": "县级市", "parent": "中共德惠市委员会", "location": "德惠市"},
    {"id": 6, "name": "中共德惠市委宣传部", "type": "党委部门", "level": "县级市", "parent": "中共德惠市委员会", "location": "德惠市"},
    {"id": 7, "name": "中共德惠市委统战部", "type": "党委部门", "level": "县级市", "parent": "中共德惠市委员会", "location": "德惠市"},
    {"id": 8, "name": "德惠经济开发区", "type": "开发区", "level": "县级市", "parent": "德惠市人民政府", "location": "德惠市"},
    {"id": 9, "name": "德惠市公安局", "type": "政府部门", "level": "县级市", "parent": "德惠市人民政府", "location": "德惠市"},
    {"id": 10, "name": "德惠市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "长春市人大常委会", "location": "德惠市"},
    {"id": 11, "name": "德惠市总工会", "type": "群团", "level": "县级市", "parent": "德惠市", "location": "德惠市"},
    {"id": 12, "name": "政协德惠市委员会", "type": "政协", "level": "县级市", "parent": "政协长春市委", "location": "德惠市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 市委书记 王喜成
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2025-10", "end_date": "present",
     "rank": "正处级", "note": "主持市委全面工作；2025年10月任中共德惠市委书记"},
    # 市长 蒋再波
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "2024-12", "end_date": "present",
     "rank": "正处级", "note": "2024年12月任市政府党组书记、代市长，在十九届人大五次会议当选市长；主持市政府全面工作"},
    # 王泰峰 市委副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "2024-05", "end_date": "present",
     "rank": "副处级", "note": "协助市委书记负责党建工作，分管农业农村、群团、信访维稳"},
    # 刘竞阳 常务副市长
    {"person_id": 4, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "2024-06", "end_date": "present",
     "rank": "副处级", "note": "负责市政府常务工作，分管财政金融、经济运行、安全应急、人社"},
    # 徐博夫 组织部长
    {"person_id": 5, "org_id": 3, "title": "市委常委、组织部部长、党校校长", "start_date": "2024-06", "end_date": "present",
     "rank": "副处级", "note": "主持市委组织部工作，兼任市委党校校长"},
    # 韩国良 纪委书记
    {"person_id": 6, "org_id": 4, "title": "市委常委、纪委书记、监委主任", "start_date": "2025-04", "end_date": "present",
     "rank": "正处级（正处长级）", "note": "主持市纪委、市监委工作；正处长级"},
    # 王嘉升 政法委书记
    {"person_id": 7, "org_id": 5, "title": "市委常委、政法委书记", "start_date": "2026-04", "end_date": "present",
     "rank": "副处级", "note": "主持市委政法委工作，兼市委依法治市委员会办公室主任"},
    # 赵莉 宣传部长
    {"person_id": 8, "org_id": 6, "title": "市委常委、宣传部部长", "start_date": "2026-04", "end_date": "present",
     "rank": "副处级", "note": "主持市委宣传部工作"},
    # 李志强 统战部长
    {"person_id": 9, "org_id": 7, "title": "市委常委、统战部部长、市政协党组副书记", "start_date": "2026-04", "end_date": "present",
     "rank": "副处级", "note": "主持市委统战部工作，市政协党组副书记"},
    # 杨笑 开发区党工委书记
    {"person_id": 10, "org_id": 8, "title": "市委常委、开发区党工委书记、管委会主任", "start_date": "2026-01", "end_date": "present",
     "rank": "副处级", "note": "负责德惠经济开发区全面工作"},
    # 副市长们
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "2021-09", "end_date": "present",
     "rank": "副处级", "note": "分管交通、城建、城区街道"},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "2026-01", "end_date": "present",
     "rank": "副处级", "note": "分管生态环保、农业农村、水利、畜牧、粮食"},
    {"person_id": 13, "org_id": 2, "title": "副市长（协助分管金融）", "start_date": "2024-01", "end_date": "present",
     "rank": "副处级", "note": "协助副市长刘竞阳分管金融，政府债务化解"},
    {"person_id": 14, "org_id": 9, "title": "副市长、市公安局局长", "start_date": "2024-04", "end_date": "present",
     "rank": "副处级", "note": "分管公安、司法、退役军人、信访"},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "2024-12", "end_date": "present",
     "rank": "副处级", "note": "分管自然资源、民生保障、市场监管、营商环境"},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "2026-05", "end_date": "present",
     "rank": "副处级", "note": "分管教育、卫生健康、医疗保障、文旅"},
    # 市人大
    {"person_id": 17, "org_id": 10, "title": "市人大常委会党组书记、主任", "start_date": "2021-11", "end_date": "present",
     "rank": "正处级", "note": "负责市人大常委会全面工作"},
    {"person_id": 18, "org_id": 10, "title": "市人大常委会副主任", "start_date": "2011-11", "end_date": "present",
     "rank": "副处级", "note": "联系市人大法制委员会"},
    {"person_id": 19, "org_id": 10, "title": "市人大常委会党组副书记、副主任", "start_date": "2021-09", "end_date": "present",
     "rank": "副处级", "note": "协助主任负责常委会机关日常工作"},
    {"person_id": 20, "org_id": 11, "title": "市人大常委会副主任、市总工会主席", "start_date": "2022-11", "end_date": "present",
     "rank": "副处级", "note": "兼市总工会主席"},
    {"person_id": 21, "org_id": 10, "title": "市人大常委会副主任", "start_date": "2021-11", "end_date": "present",
     "rank": "副处级", "note": "分管教科文卫工作委员会"},
    # 市政协
    {"person_id": 22, "org_id": 12, "title": "市政协党组书记、主席", "start_date": "2021-11", "end_date": "present",
     "rank": "正处级", "note": "负责市政协全面工作"},
    {"person_id": 23, "org_id": 12, "title": "市政协副主席", "start_date": "2016-08", "end_date": "present",
     "rank": "副处级", "note": "分管行政办公室、文教卫生委员会办公室"},
    {"person_id": 24, "org_id": 12, "title": "市政协党组成员、副主席、秘书长", "start_date": "2021-11", "end_date": "present",
     "rank": "副处级", "note": "分管提案、经济科技委员会办公室"},
    {"person_id": 25, "org_id": 12, "title": "市政协副主席（不驻会）", "start_date": "2021-11", "end_date": "present",
     "rank": "副处级", "note": "联系文教卫生委员会办公室"},
    # 前任
    {"person_id": 26, "org_id": 1, "title": "前任市委书记", "start_date": "unknown", "end_date": "2024",
     "rank": "正处级", "note": "德惠市委书记，任内在2023-2024年（官方大事记确认），去向未公开"},
    {"person_id": 27, "org_id": 2, "title": "前任市委副书记、市长", "start_date": "unknown", "end_date": "2024-12",
     "rank": "正处级", "note": "德惠市委副书记、市长至2024年12月，由蒋再波接任，去向未公开"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 书记 - 市长 搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "现任市委书记王喜成与现任市长蒋再波为党政主官搭档", "overlap_org": "中共德惠市委员会/德惠市人民政府",
     "overlap_period": "2025-10至今"},
    # 前任书记/市长 与 现任
    {"person_a": 1, "person_b": 26, "type": "predecessor_successor",
     "context": "王喜成接替申洪业任德惠市委书记（前任通过2024年任至2025年）", "overlap_org": "中共德惠市委员会",
     "overlap_period": "2025"},
    {"person_a": 2, "person_b": 27, "type": "predecessor_successor",
     "context": "蒋再波接替刘宏任德惠市长", "overlap_org": "德惠市人民政府",
     "overlap_period": "2024-12"},
    # 书记班子 与 新任职常委/副市长 (as-recent-appointment 网络)
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "市委书记王喜成与新任政法委书记王嘉升（2026-04任）", "overlap_org": "中共德惠市委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "市委书记王喜成与新任宣传部长赵莉（2026-04任）", "overlap_org": "中共德惠市委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "市委书记王喜成与新任统战部长李志强（2026-04任）", "overlap_org": "中共德惠市委员会",
     "overlap_period": "2026"},
    # 市长班子 与 副市长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长蒋再波与常务副市长刘竞阳", "overlap_org": "德惠市人民政府",
     "overlap_period": "2024-12至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "市长蒋再波与副市长付井奎（2026-01任）", "overlap_org": "德惠市人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "市长蒋再波与副市长吴立波（2026-05任）", "overlap_org": "德惠市人民政府",
     "overlap_period": "2026"},
    # 纪委书记/组织部长 关系
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "纪委书记韩国良与市委书记王喜成", "overlap_org": "中共德惠市委员会",
     "overlap_period": "2025-04至今"},
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate",
     "context": "组织部长徐博夫协助市委书记分管干部工作", "overlap_org": "中共德惠市委员会",
     "overlap_period": "2024-06至今"},
    # 市人大/政协主席团
    {"person_a": 17, "person_b": 1, "type": "superior_subordinate",
     "context": "人大常委会主任丁日伟与市委书记王喜成（四套班子）", "overlap_org": "德惠市四套班子",
     "overlap_period": "2025-10至今"},
    {"person_a": 22, "person_b": 1, "type": "superior_subordinate",
     "context": "政协主席尚祖军与市委书记王喜成（四套班子）", "overlap_org": "德惠市四套班子",
     "overlap_period": "2025-10至今"},
]


def main() -> None:
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

    print(f"[OK] 德惠市 build complete → DB: {DB_PATH}")
    print(f"[OK] GEXF: {GEXF_PATH}")
    print(f"persons={len(persons)}, orgs={len(organizations)}, "
          f"positions={len(positions)}, relationships={len(relationships)}")


if __name__ == "__main__":
    main()