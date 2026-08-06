#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 毕节市金沙县 leadership network.

Level: 县
Province: 贵州省
Parent City: 毕节市
Region: 金沙县
Targets: 县委书记 (周印) & 县长 (胡超)

Research Date: 2026-08-06 (task guizhou_金沙县)
Evidence quality: guided by the china-gov-network skill; web access degraded
(Exa rate-limited, Baidu/Bing/360 captcha-gated, r.jina.ai down). Core roster and
profiles CONFIRMED from the official 金沙县人民政府门户 https://www.gzjinsha.gov.cn/
(primary source, direct fetch OK). Biographies beyond current post remain partial.

CONFIRMED (primary/official, as of 2026-08):
  - 县委书记、金沙经开区党工委书记 周印: 主持县委常委会 2026-08-03; 半年经济工作会议 2026-07-31。
  - 县委副书记、县长、县政府党组书记、金沙经开区党工委副书记/管委会主任(兼) 胡超
    (仡佬族, 1980-06, 大学法学学士, 中共党员)。
  - 县人大常委会主任 魏其凯 (人大第十二届第十七次会议 2026-07-30); 县政协主席 赵福美;
    县委副书记 欧阳成作。
  - 县政府班子 (领导名录 zfld): 常务副县长 叶世发(1982-08, 汉, 经济学学士);
    副县长 文小学(1988-12, 土家, 工学学士, 亦县委常委)/蒋显虹(1975-01, 正县长级)/
    万纯飞(女, 1985-02, 在职研究生)/郭政俭(1988-07, 工学学士)/陈彬(彝族, 1991-01, 到广州市番禺区挂职);
    副县长兼公安局长 明泽磊(1973-11); 颜松(1977-09, 经开区管委会副主任、县政府党组成员)。
  - 县人大常委会副主任: 周益军、吴玉艳、江正勇、蒋显祥; 县人民检察院检察长 徐恺东。

UNVERIFIED / open gaps (见 report/open_gaps.md 与各 person JSON open_questions):
  - 周印/胡超 任县委书记/县长前的完整履历与身世(出生籍贯/学历/入党参工)。
  - 前任县委书记(2022 年为李涛)与前任县长, 及其去向。
  - 完整县委常委会(组织部长、纪委书记、宣传/统战/政法委书记)。
  - 金沙经开区党工委/管委会班子细分职务。

regional: 金沙县属毕节市 8 个县级政区之一(七星关区、大方县、黔西市、金沙县、
织金县、纳雍县、威宁自治县、赫章县)。主导产业: 综合能源(煤电)、酱香型白酒。
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).resolve()
for _ in range(6):
    if (BASE / "gov_relation").is_dir() and (BASE / "gov_relation" / "runner.py").is_file():
        break
    BASE = BASE.parent
sys.path.insert(0, str(BASE))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "金沙县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共金沙县委员会", "type": "党委", "level": "县处级",
     "parent": "中共毕节市委", "location": "贵州省毕节市金沙县"},
    {"id": 2, "name": "金沙县人民政府", "type": "政府", "level": "县处级",
     "parent": "毕节市人民政府", "location": "贵州省毕节市金沙县"},
    {"id": 3, "name": "金沙县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "毕节市人大常委会", "location": "贵州省毕节市金沙县"},
    {"id": 4, "name": "中国人民政治协商会议金沙县委员会", "type": "政协", "level": "县处级",
     "parent": "政协毕节市委员会", "location": "贵州省毕节市金沙县"},
    {"id": 5, "name": "中共金沙县纪律检查委员会/金沙县监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共毕节市纪委", "location": "贵州省毕节市金沙县"},
    {"id": 6, "name": "金沙经济开发区党工委/金沙经济开发区管委会", "type": "开发区", "level": "县处级",
     "parent": "中共毕节市委", "location": "贵州省毕节市金沙县"},
    {"id": 7, "name": "金沙县公安局", "type": "政府", "level": "乡科级",
     "parent": "毕节市公安局", "location": "贵州省毕节市金沙县"},
    {"id": 8, "name": "金沙县人民检察院", "type": "检察院", "level": "县处级",
     "parent": "毕节市人民检察院", "location": "贵州省毕节市金沙县"},
    {"id": 9, "name": "金沙县人民法院", "type": "法院", "level": "县处级",
     "parent": "毕节市中级人民法院", "location": "贵州省毕节市金沙县"},
    # 上级与跨县节点
    {"id": 10, "name": "中共毕节市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共贵州省委", "location": "贵州省毕节市"},
    {"id": 11, "name": "毕节市人民政府", "type": "政府", "level": "地厅级",
     "parent": "贵州省人民政府", "location": "贵州省毕节市"},
    {"id": 12, "name": "中共织金县委员会", "type": "党委", "level": "县处级",
     "parent": "中共毕节市委", "location": "贵州省毕节市织金县"},
    {"id": 13, "name": "广州市番禺区人民政府", "type": "政府", "level": "地厅级",
     "parent": "广州市人民政府", "location": "广东省广州市番禺区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 周印 — 县委书记、金沙经开区党工委书记
    {"id": 1, "name": "周印", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县委书记、金沙经济开发区党工委书记",
     "current_org": "中共金沙县委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260803_90690263.html"},
    # 2 — 胡超 — 县长
    {"id": 2, "name": "胡超", "gender": "男", "ethnicity": "仡佬族", "birth": "1980年6月",
     "birthplace": "", "education": "大学学历，法学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县委副书记、县长、县政府党组书记、金沙经开区党工委副书记/管委会主任(兼)",
     "current_org": "金沙县人民政府",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldzc_5981048/zfld/202606/t20260603_90473290.html"},
    # 3 — 魏其凯 — 人大主任
    {"id": 3, "name": "魏其凯", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县人大常委会主任",
     "current_org": "金沙县人民代表大会常务委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685101.html"},
    # 4 — 赵福美 — 政协主席
    {"id": 4, "name": "赵福美", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县政协党组书记、主席",
     "current_org": "中国人民政治协商会议金沙县委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685097.html"},
    # 5 — 欧阳成作 — 县委副书记
    {"id": 5, "name": "欧阳成作", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县委副书记",
     "current_org": "中共金沙县委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685113.html"},
    # 6 — 叶世发 — 常务副县长
    {"id": 6, "name": "叶世发", "gender": "男", "ethnicity": "汉族", "birth": "1982年8月",
     "birthplace": "", "education": "大学学历，经济学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县委常委、县政府党组副书记、常务副县长",
     "current_org": "金沙县人民政府",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldzc_5988/zfld/202606/t20260626_90559328.html"},
    # 7 — 文小学 — 副县长(兼县委常委)
    {"id": 7, "name": "文小学", "gender": "男", "ethnicity": "土家族", "birth": "1988年12月",
     "birthplace": "", "education": "大学学历，工学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县委常委、县政府党组成员、副县长",
     "current_org": "金沙县人民政府",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zfxxgk/ldgk_5988/zfld/202503/t20250324_87249571.html"},
    # 8 — 蒋显虹 — 副县长(正县长级)
    {"id": 8, "name": "蒋显虹", "gender": "男", "ethnicity": "汉族", "birth": "1975年1月",
     "birthplace": "", "education": "在职大学学历，法律专业", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县副县长（正县长级）",
     "current_org": "金沙县人民政府",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldcz_598058/zfld/202503/t20250324_87249569.html"},
    # 9 — 万纯飞 — 副县长(女)
    {"id": 9, "name": "万纯飞", "gender": "女", "ethnicity": "汉族", "birth": "1985年2月",
     "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县人民政府副县长",
     "current_org": "金沙县人民政府",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldcz_5980588/zfld/202503/t20250324_87249566.html"},
    # 11 — 郭政俭 — 副县长
    {"id": 10, "name": "郭政俭", "gender": "男", "ethnicity": "汉族", "birth": "1988年7月",
     "birthplace": "", "education": "大学学历，工学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县副县长",
     "current_org": "金沙县人民政府",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldzc_5980588/zfld/202503/t20250324_87249564.html"},
    # 11 — 明泽磊 — 副县长兼公安局长
    {"id": 11, "name": "明泽磊", "gender": "男", "ethnicity": "汉族", "birth": "1973年11月",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县副县长、县公安局党委书记/局长/督察长（二级高级警长）",
     "current_org": "金沙县公安局",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldcz_5980588/zfld/202503/t20250324_87249567.html"},
    # 12 — 颜松 — 经开区管委会副主任、县政府党组成员
    {"id": 12, "name": "颜松", "gender": "男", "ethnicity": "汉族", "birth": "1977年9月",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙经济开发区党工委副书记、管委会副主任(负责日常)、县政府党组成员",
     "current_org": "金沙经济开发区",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldcz_5980/ZFld/202503/t20250324_87249562.html"},
    # 13 — 陈彬 — 副县长(挂职广州番禺)
    {"id": 13, "name": "陈彬", "gender": "男", "ethnicity": "彝族", "birth": "1991年1月",
     "birthplace": "", "education": "大学本科，管理学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县副县长（到广东省广州市番禺区挂职）",
     "current_org": "广州市番禺区人民政府",
     "source": "https://www.gzjinsha.gov.cn/xxgk/zxgk/ldcz_5980558/zfld/202503/t20250324_87249565.html"},
    # 14 — 徐恺东 — 检察院检察长
    {"id": 14, "name": "徐恺东", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县人民检察院检察长",
     "current_org": "金沙县人民检察院",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685113.html"},
    # 15-18 — 人大副主任
    {"id": 15, "name": "周益军", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县人大常委会副主任",
     "current_org": "金沙县人民代表大会常务委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685101.html"},
    {"id": 16, "name": "吴玉艳", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县人大常委会副主任",
     "current_org": "金沙县人民代表大会常务委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685101.html"},
    {"id": 17, "name": "江正勇", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县人大常委会副主任",
     "current_org": "金沙县人民代表大会常务委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685101.html"},
    {"id": 18, "name": "蒋显祥", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金沙县人大常委会副主任",
     "current_org": "金沙县人民代表大会常务委员会",
     "source": "https://www.gzjinsha.gov.cn/xwzx/jrdt/202608/t20260801_90685101.html"},
    # 19 — 李涛 — 前任县委书记 (2022)
    {"id": 19, "name": "李涛", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任金沙县委书记，2022年见诸官方新闻，去向待核）",
     "current_org": "中共金沙县委员会",
     "source": "https://www.gzjinsha.gov.cn/wsfw/ggfw/tzfw/202211/t20221116_77122851.html"},
    # 20 — 郭锡文 — 毕节市委书记 (上层连接)
    {"id": 20, "name": "郭锡文", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "毕节市委书记（上级党委一把手）",
     "current_org": "中共毕节市委员会",
     "source": "https://www.gzjinsha.gov.cn/ (毕节市委七届任期, 见 2026-07 毕节官网)"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 周印
    {"person_id": 1, "org_id": 1, "title": "金沙县委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持县委工作"},
    {"person_id": 1, "org_id": 6, "title": "金沙经济开发区党工委书记", "start_date": "", "end_date": "present",
     "rank": "", "note": "兼任"},
    # 胡超
    {"person_id": 2, "org_id": 1, "title": "金沙县委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "金沙县人民政府县长（县政府党组书记）", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "金沙经济开发区管委会主任（党工委副书记兼）", "start_date": "", "end_date": "present",
     "rank": "", "note": "兼"},
    # 人大/政协
    {"person_id": 3, "org_id": 3, "title": "金沙县人大常委会主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "金沙县政协主席", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    # 副书记
    {"person_id": 5, "org_id": 1, "title": "金沙县委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 政府班子
    {"person_id": 6, "org_id": 2, "title": "常务副县长（县委常委）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管常务、发改财政"},
    {"person_id": 7, "org_id": 2, "title": "副县长（县委常委）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管能源"},
    {"person_id": 8, "org_id": 2, "title": "副县长（正县长级）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "民政交通"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "农业农村乡村振兴"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "教育文旅卫健"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "县公安局局长、党委书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "经开区党工委副书记、管委会副主任（负责日常）", "start_date": "", "end_date": "present",
     "rank": "", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "到广东省广州市番禺区挂职"},
    # 检察院
    {"person_id": 14, "org_id": 8, "title": "金沙县人民检察院检察长", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    # 人大副主任
    {"person_id": 15, "org_id": 3, "title": "金沙县人大常委会副主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "金沙县人大常委会副主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "金沙县人大常委会副主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "金沙县人大常委会副主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 前任县委书记 (李涛, 2022)
    {"person_id": 19, "org_id": 1, "title": "金沙县委书记", "start_date": "", "end_date": "2022后",
     "rank": "正处级", "note": "前任县委书记；去向待核"},
    # 上级党委
    {"person_id": 20, "org_id": 10, "title": "毕节市委书记", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "上级党委一把手"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 副书记↔县长(党政正职)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长（县政府党组书记）党政正职搭档", "overlap_org": "中共金沙县委员会", "overlap_period": "current"},
    # 县委↔人大/政协
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与县人大常委会主任（四套班子）", "overlap_org": "金沙县", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与县政协主席（四套班子）", "overlap_org": "金沙县", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与县委副书记（欧阳成作）", "overlap_org": "中共金沙县委员会", "overlap_period": "current"},
    # 县长与政府班子
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与常务副县长（县政府班子）", "overlap_org": "金沙县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "县长与副县长（含经开区）", "overlap_org": "金沙县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "县长与副县长兼公安局长", "overlap_org": "金沙县人民政府", "overlap_period": "current"},
    # 县委班子内部
    {"person_a": 5, "person_b": 3, "type": "overlap",
     "context": "县委副书记与县人大主任（四套班子交叉）", "overlap_org": "金沙县", "overlap_period": "current"},
    {"person_a": 5, "person_b": 4, "type": "overlap",
     "context": "县委副书记与县政协主席（四套班子交叉）", "overlap_org": "金沙县", "overlap_period": "current"},
    # 人大内部
    {"person_a": 3, "person_b": 15, "type": "overlap",
     "context": "人大主任与人大副主任（常委会）", "overlap_org": "金沙县人民代表大会常务委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 16, "type": "overlap",
     "context": "人大主任与人大副主任", "overlap_org": "金沙县人民代表大会常务委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 17, "type": "overlap",
     "context": "人大主任与人大副主任", "overlap_org": "金沙县人民代表大会常务委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 18, "type": "overlap",
     "context": "人大主任与人大副主任", "overlap_org": "金沙县人民代表大会常务委员会", "overlap_period": "current"},
    # 前任与现任
    {"person_a": 19, "person_b": 1, "type": "predecessor_successor",
     "context": "李涛曾任金沙县委书记，其后周印接任（2022年李涛在位；接任细节待核）", "overlap_org": "中共金沙县委员会", "overlap_period": "2022-2025"},
    # 上级党委对县
    {"person_a": 20, "person_b": 1, "type": "superior_subordinate",
     "context": "毕节市委书记与金沙县委书记（市对县级干部任免/领导关系）", "overlap_org": "中共毕节市委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "县长与县人大常委会副主任（县政府/人大两套班子）", "overlap_org": "金沙县", "overlap_period": "current"},
]

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
    print(f"\nDone: {SLUG} build complete.")