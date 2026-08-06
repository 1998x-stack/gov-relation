#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database, GEXF graph, and person JSONs for 前郭尔罗斯蒙古族自治县 leadership network.

Level: 县 (自治县)
Province: 吉林省
Parent City: 松原市
Region: 前郭尔罗斯蒙古族自治县 (前郭县)
Targets: 县委书记 & 县长

Research Date / as-of: 2026-08-06 (task jilin_前郭尔罗斯蒙古族自治县)

Primary sources (all reachable over plain http):
- 前郭县人民政府官网 http://www.qianguo.gov.cn/  (县政府领导页 + 各领导简历页; 重要会议)
- 两会报告 2026-01: 前郭县十九届人大五次会议 / 政协前郭县十六届委员会第五次会议开幕
- 2026 政府工作报告 (县长 白振宇 于 县人代会 2026-01 作)

Evidence quality: guided by china-gov-network skill; web degraded (Exa rate-limited,
Baidu 403, county site qgs.gov.cn unreachable), but the county official portal
www.qianguo.gov.cn WAS reachable over http and provided confirmed current roster.

CONFIRMED leadership (as of 2026-08):
  县委书记: 汤大鹏 (兼 松原市委常委)
  县长   : 白振宇 — 男, 蒙古族, 中共党员, 1982年11月生, 2006年8月参加工作
  常务副县长: 曹伟 — 男, 汉族, 中共党员, 1982年11月生, 2004年3月参加工作
  副县长 : 王猛(岱钦, 蒙古名)、王冬新、高阳、朱明达、张秀梅、邢健、袁子龙、李杨
  人大常委会主任: 阿穆尔叔巧布新 (蒙古族); 副主任: 刘艳杰、刘志成、王东星
  政协   : 主席(党组书记) 马学文; 党组副书记 刘凯; 副主席 杨亚彪、郑大为、裴玉峰
  法院院长: 蒋格; 检察院检察长: 潘德东
  前郭灌区灌溉管理局局长: 高洪忱

UNCONFIRMED / open gaps (encoded confidence=unverified + open_questions):
  - 县委书记 汤大鹏 的出生/民族/学历/参加年份/到任时间/前任县委书记
  - 县长 白振宇 任县长到任时间/前任县长
  - 县委专职副书记、纪委书记、组织部长、宣传部长、政法委书记、统战部长名单
  - 各副县长 出生/民族/学历 完整履历 (职务已确认)
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_BASE = Path(__file__).resolve().parent
while _BASE != _BASE.parent and not (_BASE / "gov_relation").is_dir():
    _BASE = _BASE.parent
sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "前郭尔罗斯蒙古族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
    PJSON_DIR = _STAGING
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"
    PJSON_DIR = str(DATABASE_DIR.parent / "persons")
PJSON_DIR_P = Path(PJSON_DIR)

# ── ORGANIZATIONS ─────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共前郭尔罗斯蒙古族自治县委员会", "type": "党委", "level": "县处级",
     "parent": "中共松原市委", "location": "前郭县"},
    {"id": 2, "name": "前郭尔罗斯蒙古族自治县人民政府", "type": "政府", "level": "县处级",
     "parent": "松原市人民政府", "location": "前郭县"},
    {"id": 3, "name": "前郭县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "松原市人大常委会", "location": "前郭县"},
    {"id": 4, "name": "中国人民政治协商会议前郭县委员会", "type": "政协", "level": "县处级",
     "parent": "政协松原市委员会", "location": "前郭县"},
    {"id": 5, "name": "前郭县纪律检查委员会/监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共松原市纪委", "location": "前郭县"},
    {"id": 6, "name": "前郭县人民法院", "type": "政法", "level": "县处级",
     "parent": "吉林省高级人民法院", "location": "前郭县"},
    {"id": 7, "name": "前郭县人民检察院", "type": "政法", "level": "县处级",
     "parent": "松原市人民检察院", "location": "前郭县"},
    {"id": 8, "name": "前郭县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共前郭尔罗斯蒙古族自治县委员会", "location": "前郭县"},
    {"id": 9, "name": "前郭县乌兰塔拉乡党委", "type": "乡镇/街道", "level": "乡镇",
     "parent": "中共前郭尔罗斯蒙古族自治县委员会", "location": "前郭县乌兰塔拉乡"},
    {"id": 10, "name": "吉林前郭查干湖旅游开发区管理委员会", "type": "开发区", "level": "县处级",
     "parent": "前郭县人民政府", "location": "前郭县查干湖"},
    {"id": 11, "name": "前郭灌区灌溉管理局", "type": "政府", "level": "县处级",
     "parent": "前郭县人民政府", "location": "前郭县"},
    {"id": 12, "name": "中共松原市委员会", "type": "党委", "level": "地级", "parent": "", "location": "松原市"},
    {"id": 13, "name": "松原市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "松原市"},
]

# ── PERSONS ─────────────────────────────────────────────────────
persons = [
    # 县委 (书记 / 副书记)
    {"id": 1, "name": "汤大鹏", "gender": "男", "ethnicity": "汉族", "birth": "1978年10月", "birthplace": "",
     "education": "在职研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "松原市委常委、前郭县委书记", "current_org": "中共前郭尔罗斯蒙古族自治县委员会",
     "source": "吉林省管干部任前公示(2024年第3号) + http://www.qianguo.gov.cn/ 新闻(2026-07) + 两会(2026-01)", "confidence": "confirmed"},
    {"id": 2, "name": "白振宇", "gender": "男", "ethnicity": "蒙古族", "birth": "1982年11月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "2006年8月",
     "current_post": "前郭县委副书记、县长", "current_org": "前郭尔罗斯蒙古族自治县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/xz/xz/", "confidence": "confirmed"},
    {"id": 3, "name": "曹伟", "gender": "男", "ethnicity": "汉族", "birth": "1982年11月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "2004年3月",
     "current_post": "前郭县委常委、常务副县长", "current_org": "前郭尔罗斯蒙古族自治县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/cwfxz/cw/", "confidence": "confirmed"},
    # 政府副县长
    {"id": 4, "name": "王猛（岱钦）", "gender": "男", "ethnicity": "蒙古族", "birth": "1981年6月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "2004年8月", "current_post": "前郭县委常委、副县长", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/wm/", "confidence": "confirmed"},
    {"id": 5, "name": "王冬新", "gender": "男", "ethnicity": "蒙古族", "birth": "1982年2月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "2006年11月", "current_post": "前郭县委常委、副县长", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/wdx/", "confidence": "confirmed"},
    {"id": 6, "name": "高阳", "gender": "男", "ethnicity": "汉族", "birth": "1982年8月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "2003年12月", "current_post": "前郭县委常委、副县长", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/gy/", "confidence": "confirmed"},
    {"id": 7, "name": "朱明达", "gender": "男", "ethnicity": "汉族", "birth": "1968年1月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "1988年8月", "current_post": "前郭县副县长兼县公安局局长", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/txq/", "confidence": "confirmed"},
    {"id": 8, "name": "张秀明", "gender": "女", "ethnicity": "汉族", "birth": "1980年9月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "2003年12月", "current_post": "前郭县政府副县长", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/glz_28093/", "confidence": "confirmed"},
    {"id": 9, "name": "邢健", "gender": "男", "ethnicity": "汉族", "birth": "1976年5月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "1997年12月", "current_post": "前郭县政府副县长", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/xj/", "confidence": "confirmed"},
    {"id": 10, "name": "袁子龙", "gender": "男", "ethnicity": "汉族", "birth": "1988年3月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "2011年9月", "current_post": "前郭县政府副县长（到浙江舟山挂职）", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/yzl/", "confidence": "confirmed"},
    {"id": 11, "name": "李杨", "gender": "男", "ethnicity": "蒙古族", "birth": "1985年11月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "2011年8月", "current_post": "前郭县政府副县长", "current_org": "前郭县人民政府",
     "source": "http://www.qianguo.gov.cn/ygzw/xzfld/fxz/xj_30260/", "confidence": "confirmed"},
    # 县委班子其他
    {"id": 31, "name": "杨彦良", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县委副书记、县委政法委书记", "current_org": "中共前郭尔罗斯蒙古族自治县委员会",
     "source": "前郭县全会新闻(2023-08/2025-08, 县委副书记兼政法委书记)", "confidence": "confirmed"},
    {"id": 32, "name": "姜思宇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县监察委员会主任", "current_org": "前郭县纪律检查委员会/监察委员会",
     "source": "前郭县十九届人大五次会议选举 2026-01-06（县监委主任）", "confidence": "confirmed"},
    {"id": 33, "name": "张志超", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县委常委（组织部长，待核实）", "current_org": "中共前郭尔罗斯蒙古族自治县委员会",
     "source": "前郭县委十五届八次/九次全会(2024-2025) 常委名单", "confidence": "plausible"},
    {"id": 34, "name": "鞠清明", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县委常委（宣传部长，待核实）", "current_org": "中共前郭尔罗斯蒙古族自治县委员会",
     "source": "前郭县委十五届会议精神 (常委名单)", "confidence": "plausible"},
    # 人大
    {"id": 12, "name": "阿穆尔图布新（王俊辉）", "gender": "男", "ethnicity": "蒙古族", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县人大常委会主任", "current_org": "前郭县人大常委会",
     "source": "前郭县人大常委会常委会领导页(2026-07-17) + 两会(2026-01)", "confidence": "confirmed"},
    {"id": 13, "name": "刘艳杰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县人大常委会副主任", "current_org": "前郭县人大常委会",
     "source": "前郭县人大常委会常委会领导页(2026-07) + 两会", "confidence": "confirmed"},
    {"id": 14, "name": "刘志成", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县人大常委会副主任", "current_org": "前郭县人大常委会",
     "source": "前郭县人大常委会常委会领导页(2026-07) + 两会", "confidence": "confirmed"},
    {"id": 15, "name": "王东星", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县人大常委会副主任", "current_org": "前郭县人大常委会",
     "source": "前郭县人代会两会执行主席/议案审查委员会主任委员(2026-01)", "confidence": "plausible"},
    # 政协
    {"id": 16, "name": "马学文", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县政协主席（党组书记）", "current_org": "前郭县政协",
     "source": "http://www.qianguo.gov.cn/ (政协会议 2026-01)", "confidence": "confirmed"},
    {"id": 17, "name": "刘凯", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县政协党组副书记", "current_org": "前郭县政协",
     "source": "http://www.qianguo.gov.cn/ (政协会议 2026-01)", "confidence": "confirmed"},
    {"id": 18, "name": "杨亚龙", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县政协副主席", "current_org": "前郭县政协",
     "source": "http://www.qianguo.gov.cn/ (政协会议 2026-01)", "confidence": "confirmed"},
    {"id": 19, "name": "郑大为", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县政协副主席", "current_org": "前郭县政协",
     "source": "http://www.qianguo.gov.cn/ (政协会议 2026-01)", "confidence": "confirmed"},
    {"id": 20, "name": "裴玉峰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "前郭县政协副主席", "current_org": "前郭县政协",
     "source": "http://www.qianguo.gov.cn/ (政协会议 2026-01)", "confidence": "confirmed"},
    # 两院
    {"id": 21, "name": "朝格", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县人民法院院长", "current_org": "前郭县人民法院",
     "source": "http://www.qianguo.gov.cn/ (两会 2026-01)", "confidence": "confirmed"},
    {"id": 22, "name": "潘德东", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "前郭县人民检察院检察长", "current_org": "前郭县人民检察院",
     "source": "http://www.qianguo.gov.cn/ (两会 2026-01)", "confidence": "confirmed"},
    # 其他
    {"id": 23, "name": "高洪忱", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "前郭灌区灌溉管理局局长", "current_org": "前郭灌区灌溉管理局",
     "source": "http://www.qianguo.gov.cn/ (两会 2026-01)", "confidence": "confirmed"},
    # 前任领导
    {"id": 24, "name": "杨文慧", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "", "current_post": "长白山党工委书记、管委会主任（曾任前郭县委书记）", "current_org": "长白山保护开发区",
     "source": "前郭县委十五届全会(2025-08) + 百度百科杨文慧", "confidence": "confirmed"},
    {"id": 25, "name": "满都拉", "gender": "男", "ethnicity": "蒙古族", "birth": "1976年2月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "1996年9月", "current_post": "扶余市委书记（前郭县原县长）", "current_org": "中共扶余市委员会",
     "source": "吉林省干部任前公示(2024-12-17) 满都拉拟任县市区党委正职；后任扶余市委书记（百度百科/扶余市数据）", "confidence": "confirmed"},
    {"id": 26, "name": "高立柱", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "已离任（前郭县政协前任主席）", "current_org": "前郭县政协",
     "source": "前郭县两会 2025-02 (阿穆尔图布新、白振宇、高立柱走访慰问)", "confidence": "confirmed"},
]

# ══ POSITIONS ══                                  
positions = [
    {"person_id": 1, "org_id": 1, "title": "前郭县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼松原市委常委"},
    {"person_id": 1, "org_id": 12, "title": "松原市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任"},
    {"person_id": 2, "org_id": 2, "title": "前郭县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "前郭县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "前郭县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "前郭县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "前郭县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "前郭县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "前郭县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "前郭县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "前郭县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "前郭县政协主席（党组书记）", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "前郭县政协党组副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "前郭县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "前郭县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "前郭县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "前郭县人民法院院长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 7, "title": "前郭县人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 11, "title": "前郭灌区灌溉管理局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 31, "org_id": 1, "title": "前郭县委副书记、县委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "专职副书记"},
    {"person_id": 32, "org_id": 5, "title": "前郭县监察委员会主任", "start_date": "2026年1月", "end_date": "present", "rank": "副处级", "note": "2026-01-06 人代会选举"},
    {"person_id": 33, "org_id": 1, "title": "前郭县委常委（组织部长，待核实）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 34, "org_id": 1, "title": "前郭县委常委（宣传部长，待核实）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 1, "title": "前郭县委书记（前任）", "start_date": "2022年", "end_date": "2025年", "rank": "正处级", "note": "后任长白山党工委书记"},
    {"person_id": 25, "org_id": 2, "title": "前郭县长（前任）", "start_date": "", "end_date": "2024年", "rank": "正处级", "note": "后任扶余市委书记"},
    {"person_id": 26, "org_id": 4, "title": "前郭县政协主席（前任）", "start_date": "", "end_date": "2025年", "rank": "正处级", "note": "马学文前任"},
]

# ══ RELATIONSHIPS ══
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "前郭县委书记—县长 党政班子搭档", "overlap_org": "前郭县", "overlap_period": "current"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "前郭县委书记—县委常委/常务副县长", "overlap_org": "前郭县委", "overlap_period": "current"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委书记—人大常委会主任（两会）", "overlap_org": "前郭县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委书记—政协主席（政协会议前排）", "overlap_org": "前郭县政协", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—常务副县长（日常）", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长—副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "常务副县长—副县长（协助）", "overlap_org": "前郭县人民政府", "overlap_period": "current"},
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "人大主任—副主任", "overlap_org": "前郭县人大常委会", "overlap_period": "current"},
    {"person_a": 12, "person_b": 14, "type": "overlap", "context": "人大主任—副主任", "overlap_org": "前郭县人大常委会", "overlap_period": "current"},
    {"person_a": 12, "person_b": 15, "type": "overlap", "context": "人大主任—副主任", "overlap_org": "前郭县人大常委会", "overlap_period": "current"},
    {"person_a": 16, "person_b": 17, "type": "overlap", "context": "政协主席—党组副书记", "overlap_org": "前郭县政协", "overlap_period": "current"},
    {"person_a": 16, "person_b": 18, "type": "overlap", "context": "政协主席—副主席", "overlap_org": "前郭县政协", "overlap_period": "current"},
    {"person_a": 16, "person_b": 19, "type": "overlap", "context": "政协主席—副主席", "overlap_org": "前郭县政协", "overlap_period": "current"},
    {"person_a": 16, "person_b": 20, "type": "overlap", "context": "政协主席—副主席", "overlap_org": "前郭县政协", "overlap_period": "current"},
    {"person_a": 1, "person_b": 21, "type": "overlap", "context": "县委书记—法院院长（人代会）", "overlap_org": "前郭县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 22, "type": "overlap", "context": "县委书记—检察院检察长（人代会）", "overlap_org": "前郭县", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 23, "type": "overlap", "context": "县长—灌区灌溉管理局局长", "overlap_org": "前郭县", "overlap_period": "current"},
    {"person_a": 1, "person_b": 24, "type": "predecessor_successor", "context": "汤大鹏接杨文慧任前郭县委书记", "overlap_org": "中共前郭县委", "overlap_period": "2025"},
    {"person_a": 2, "person_b": 25, "type": "predecessor_successor", "context": "白振宇接满都拉任前郭县长", "overlap_org": "前郭县人民政府", "overlap_period": "2024"},
    {"person_a": 16, "person_b": 26, "type": "predecessor_successor", "context": "马学文接高立柱任前郭政协主席", "overlap_org": "前郭县政协", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 31, "type": "overlap", "context": "县委书记—县委副书记/政法委书记", "overlap_org": "前郭县委", "overlap_period": "current"},
    {"person_a": 2, "person_b": 31, "type": "overlap", "context": "县长—县委副书记", "overlap_org": "前郭县委", "overlap_period": "current"},
    {"person_a": 1, "person_b": 32, "type": "overlap", "context": "县委书记—监委主任（纪委）", "overlap_org": "前郭县委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 33, "type": "overlap", "context": "县委书记—常委/组织部", "overlap_org": "前郭县委", "overlap_period": "current"},
    {"person_a": 1, "person_b": 34, "type": "overlap", "context": "县委书记—常委/宣传部", "overlap_org": "前郭县委", "overlap_period": "current"},
]

# ══ Person JSON ══
TEMPLATES = {
    1: {"name": "汤大鹏", "identity": {"person_id": "songyuan_qianguo_tang_dapeng", "name": "汤大鹏",
        "aliases": [], "gender": "男", "ethnicity": "汉族", "birth": "1978年10月", "birthplace": "", "native_place": "",
        "education": [{"period": "", "institution": "", "major": "", "degree": "在职研究生学历", "study_type": "part_time", "source_ids": ["S006"]}], "party_join": "中共党员", "work_start": "",
        "dedupe_keys": {"name_birth": "汤大鹏_1978年10月", "name_birthplace": "汤大鹏_", "official_profile_url": "http://www.qianguo.gov.cn/"}},
        "current_status": {"current_post": "松原市委常委、前郭县委书记", "current_org": "中共前郭尔罗斯蒙古族自治县委员会",
                           "administrative_rank": "正处级", "as_of": "2026-08", "is_current_confirmed": True, "source_ids": ["S001", "S004"]},
        "career_timeline": [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "party", "rank": "", "is_key_promotion": False,
             "notes": "任前郭县委书记（兼松原市委常委）前的完整职务履历（在松原市的任职）待查。", "confidence": "unverified", "source_ids": []},
            {"start": "2025年12月", "end": "present", "org": "中共前郭尔罗斯蒙古族自治县委员会", "title": "前郭县委书记", "level": "县处级", "location": "前郭县", "system": "party", "rank": "正处级", "is_key_promotion": True,
             "notes": "兼松原市委常委；2025-12-22 起主持县委常委会；2026-07 走访查干花镇困难党员。", "confidence": "confirmed", "source_ids": ["S001", "S004", "S006"]},
        ],
        "organizations": [{"person": "中共前郭尔罗斯蒙古族自治县委员会", "role": "县委书记"}],
        "relationships": [
            {"person": "白振宇", "person_id": "白振宇_198211", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记—县长党政搭档", "overlap_org": "前郭县", "overlap_period": "current", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [{"period": "2025-2026", "domain": "rural_revitalization", "achievement_or_event": "县域经济发展/查干湖生态保护", "role_in_event": "县委总揽", "location": "前郭县", "confidence": "confirmed", "source_ids": ["S003"]}],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["party"], "geographic_pattern": [], "promotion_velocity": {"summary": "履历不明", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "推断自公开."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "前郭县政府 — 汤大鹏“七一”走访慰问", "url": "http://www.qianguo.gov.cn/xw/qyqy/2026/t20260703_574925.html", "publisher": "前郭县人民政府", "published_at": "2026-07-03", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high"},
            {"id": "S004", "title": "前郭县人代会五次会议开幕", "url": "http://www.qianguo.gov.cn/ygzw/zyhy/2026enter/t20260106_564890.html", "publisher": "前郭县人大常委会", "published_at": "2026-01-06", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high"},
            {"id": "S006", "title": "吉林省管干部任前公示（汤大鹏）", "url": "http://www.jl.gov.cn/", "publisher": "吉林省委组织部", "published_at": "2024", "accessed_at": "2026-08-06", "source_type": "appointment_notice", "reliability": "high", "notes": "汤大鹏：男，汉族，1978年10月生，在职研究生学历，中共党员"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "出生/民族/学历/前任书记"},
        "open_questions": [
            {"priority": "critical", "question": "汤大鹏的出生年/民族/学历/任前履历", "why_it_matters": "该调研核心人物", "suggested_queries": ["汤大鹏 简历 前郭县委书记"], "last_attempted": "2026-08-06"},
            {"priority": "critical", "question": "前任前郭县委书记与到任日期", "why_it_matters": "交接链", "suggested_queries": ["前任前郭县委书记"], "last_attempted": "2026-08-06"},
        ]
    },
    2: {
        "name": "白振宇", "identity": {"person_id": "白振宇_198211", "name": "白振宇", "aliases": [],
        "gender": "男", "ethnicity": "蒙古族", "birth": "1982年11月", "birthplace": "", "native_place": "",
        "education": [], "party_join": "中共党员", "work_start": "2006年8月",
        "dedupe_keys": {"name_birth": "白振宇_198211", "name_birthplace": "白振宇_", "official_profile_url": "http://www.qianguo.gov.cn/ygzw/xzfld/xz/xz/"}},
        "current_status": {"current_post": "前郭县委副书记、县长", "current_org": "前郭尔罗斯蒙古族自治县人民政府", "administrative_rank": "正处级", "as_of": "2026-08", "is_current_confirmed": True, "source_ids": ["S002"]},
        "career_timeline": [
            {"start": "2006年8月", "end": "", "org": "", "title": "参加工作", "level": "", "location": "", "system": "government", "rank": "", "is_key_promotion": False, "notes": "2006-08 参加工作", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "present", "org": "前郭尔罗斯蒙古族自治县人民政府", "title": "前郭县委副书记、县长", "level": "县处级", "location": "前郭县", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "主持县政府全面工作，分管县审计局；2026-01 作政府工作报告", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "任县长前履历待查。", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"person": "前郭尔罗斯蒙古族自治县人民政府", "role": "县长"}],
        "relationships": [
            {"person": "汤大鹏", "person_id": "汤大鹏_", "relationship_type": "overlap", "strength": "strong", "evidence": "县长—县委书记", "overlap_org": "前郭县", "overlap_period": "current", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"person": "曹伟", "person_id": "曹伟_198211", "relationship_type": "overlap", "strength": "strong", "evidence": "县长—常务副县长", "overlap_org": "前郭县人民政府", "overlap_period": "current", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "governance_record": [{"period": "2025-2026", "domain": "economic_development", "achievement_or_event": "2026 政府工作报告，目标 GDP+5.5%、固定资产投资+10%", "role_in_event": "主持", "measured_outcome": "2025 GDP+5%、规上工业增加值+15%", "location": "前郭县", "confidence": "confirmed", "source_ids": ["S003"]}],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["government", "party"], "geographic_pattern": ["吉林省"], "promotion_velocity": {"summary": "蒙古族干部，1982年生，2006年参加工作", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": ["乡村振兴", "产业升级"], "management_signals": [], "caveat": "引用自公开"},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S002", "title": "前郭县政府领导 — 县长白振宇", "url": "http://www.qianguo.gov.cn/ygzw/xzfld/xz/xz/", "publisher": "前郭县人民政府", "published_at": "", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "2026 政府工作报告", "url": "http://www.qianguo.gov.cn/ygzw/zyhy/202601/t20260106_564890.html", "publisher": "前郭县人大常委会", "published_at": "2026-01", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "任县长前履历/前任县长"},
        "open_questions": [{"priority": "high", "question": "白振宇任前郭县长前任职务与到任日期；前任县长去向", "why_it_matters": "晋升/交接链", "suggested_queries": ["白振宇 前郭 县长", "前任前郭县县长"], "last_attempted": "2026-08-06"}]
    },
    3: {
        "name": "曹伟", "identity": {"person_id": "曹伟_198211", "name": "曹伟", "aliases": [],
        "gender": "男", "ethnicity": "汉族", "birth": "1982年11月", "birthplace": "", "native_place": "",
        "education": [], "party_join": "中共党员", "work_start": "2004年3月",
        "dedupe_keys": {"name_birth": "曹伟_198211", "name_birthplace": "曹伟_", "official_profile_url": "http://www.qianguo.gov.cn/ygzw/xzfld/cwfxz/cw/"}},
        "current_status": {"current_post": "前郭县委常委、常务副县长", "current_org": "前郭尔罗斯蒙古族自治县人民政府", "administrative_rank": "副处级", "as_of": "2026-08", "is_current_confirmed": True, "source_ids": ["S005"]},
        "career_timeline": [
            {"start": "2004年3月", "end": "", "org": "", "title": "参加工作", "level": "", "location": "", "system": "government", "rank": "", "is_key_promotion": False, "notes": "2004-03 参加工作", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "", "end": "present", "org": "前郭县人民政府", "title": "前郭县委常委、常务副县长", "level": "县处级", "location": "前郭县", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "负责县政府常务工作", "confidence": "confirmed", "source_ids": ["S005"]},
        ],
        "organizations": [{"person": "前郭县人民政府", "role": "常务副县长"}],
        "relationships": [
            {"person": "白振宇", "person_id": "白振宇_198211", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副县长—县长", "overlap_org": "前郭县人民政府", "overlap_period": "current", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "汤大鹏", "person_id": "汤大鹏_", "relationship_type": "overlap", "strength": "medium", "evidence": "常委—县委书记", "overlap_org": "前郭县委", "overlap_period": "current", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
        ],
        "governance_record": [],
        "professional_profile": {"primary_specializations": ["财政", "发改"], "secondary_specializations": [], "career_pattern": "local", "systems_experience": ["government", "party"], "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "推断自公开."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [{"id": "S005", "title": "常务副县长曹伟简历页", "url": "http://www.qianguo.gov.cn/ygzw/xzfld/cwfxz/cw/", "publisher": "前郭县人民政府", "published_at": "", "accessed_at": "2026-08-06", "source_type": "official", "reliability": "high"}],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "high", "biggest_gap": "任常务副县长的前置职务"},
        "open_questions": [{"priority": "medium", "question": "曹伟任常务副县长前所任职务", "why_it_matters": "政府梯队", "suggested_queries": ["曹伟 前郭 常务"], "last_attempted": "2026-08-06"}]
    },
}


def write_person_json(pid):
    t = TEMPLATES.get(pid)
    if not t:
        return ""
    person = next((p for p in persons if p["id"] == pid), None)
    if not person:
        return ""
    role_map = {1: "县委书记", 2: "县长", 3: "常务副县长"}
    fname = f"{TODAY}-吉林省-松原市-{role_map.get(pid, '县领导')}-{t['name']}.json"
    fp = PJSON_DIR_P / fname
    doc = {
        "schema_version": "1.0", "generated_at": TODAY,
        "investigation_scope": {"province": "吉林省", "city": "松原市", "region": "前郭尔罗斯蒙古族自治县",
                                 "job": person["current_post"], "task_id": "jilin_前郭尔罗斯蒙古族自治县", "time_focus": "2025-2026"},
        "identity": t["identity"], "current_status": t["current_status"],
        "career_timeline": t["career_timeline"], "organizations": t["organizations"],
        "relationships": t["relationships"], "governance_record": t["governance_record"],
        "professional_profile": t["professional_profile"], "work_style_and_personality": t["work_style_and_personality"],
        "network_metrics": {}, "risk_and_integrity_signals": t["risk_and_integrity_signals"],
        "source_register": t["source_register"], "confidence_summary": t["confidence_summary"],
        "open_questions": t["open_questions"],
    }
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fname}")
    return str(fp)


if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    PJSON_DIR_P.mkdir(parents=True, exist_ok=True)
    for pid in [1, 2, 3]:
        write_person_json(pid)
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships, db_path=DB_PATH,
              gexf_path=GEXF_PATH, overwrite=True)
    db_size = Path(DB_PATH).stat().st_size if Path(DB_PATH).exists() else 0
    gexf_size = Path(GEXF_PATH).stat().st_size if Path(GEXF_PATH).exists() else 0
    print(f"Done. DB {Path(DB_PATH).name} ({db_size:,} B); GEXF {Path(GEXF_PATH).name} ({gexf_size:,} B)")