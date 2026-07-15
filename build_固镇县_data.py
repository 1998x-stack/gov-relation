#!/usr/bin/env python3
"""Build Guzhen County (固镇县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.guzhen.gov.cn (official Guzhen government website)
  - 中国共产党固镇县第十二届委员会第一次全体会议 (2026-06-25)
    https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html
  - 中国共产党固镇县第十二次代表大会胜利闭幕 (2026-06-25)
    https://www.guzhen.gov.cn/gzdt/gzyw/81379143.html
  - 中国共产党固镇县第十二次代表大会举行预备会议 (2026-06-23)
    https://www.guzhen.gov.cn/gzdt/gzyw/81378899.html
  - 全县"两优一先"表彰暨专题党课报告会 (2026-07-01)
    https://www.guzhen.gov.cn/gzdt/gzyw/81379314.html
  - 县十三届人民政府第99次常务会议 (2026-06-27)
    https://www.guzhen.gov.cn/gzdt/gzyw/81379140.html
  - 汤伟同志讲授树立和践行正确政绩观学习教育专题党课 (2026-07-06)
    https://www.guzhen.gov.cn/gzdt/bmdt/81379723.html
  - Government leadership profiles (as of 2026-06-01):
    https://www.guzhen.gov.cn/zfxxgk/public/29641/52715824.html (蓝佳勇)
    https://www.guzhen.gov.cn/zfxxgk/public/29641/53244709.html (杨军)
    https://www.guzhen.gov.cn/zfxxgk/public/29641/53272603.html (姚军)
    https://www.guzhen.gov.cn/zfxxgk/public/29641/49387811.html (戴传捷)
    https://www.guzhen.gov.cn/zfxxgk/public/29641/52885786.html (王勇)
    https://www.guzhen.gov.cn/zfxxgk/public/29641/51302062.html (赵磊)
    https://www.guzhen.gov.cn/zfxxgk/public/29641/52885798.html (阿旺伦珠)

Confidence: Current roles confirmed from official Guzhen government news (July 2026).
  Biographical details (birth years, education) from government leadership profiles.
  Full career timelines before current roles are partial.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "固镇县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "固镇县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "徐松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日在固镇县第十二届委员会第一次全体会议上当选为县委书记。代表十一届县委作工作报告。主持县委全面工作。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "蓝佳勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn/zfxxgk/public/29641/52715824.html",
        "notes": "1978年10月出生，汉族，大学学历，中共党员。领导县政府全面工作。负责经济开发区、审计等方面工作。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "汤伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日当选为县委副书记。兼任县委党校校长、县经开区党工委副书记。主持开发区专题党课。",
        "confidence": "confirmed"
    },
    # ── Other Standing Committee Members ──
    {
        "id": 4,
        "name": "姚军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长人选",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn/zfxxgk/public/29641/53272603.html",
        "notes": "1976年12月出生，汉族，省委党校大学学历，中共党员。负责科技、工业和信息化、市场监管、自然资源、规划、生态环境等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "杨军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn/zfxxgk/public/29641/53244709.html",
        "notes": "1984年10月出生，汉族，省委党校研究生学历，中共党员。负责县政府常务工作。分管发展改革、财政、住建、应急、统计、金融等。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "王小兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日当选为县委常委。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "魏兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日当选为县委常委。在全县'两优一先'表彰大会上以县领导身份出席。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "钱玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日当选为县委常委。在全县'两优一先'表彰大会上以县领导身份出席。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "窦凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日当选为县委常委。在全县'两优一先'表彰大会上以县领导身份出席。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "韩冬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日当选为县委常委。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "廖立华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共固镇县委",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "2026年6月25日当选为县委常委。在全县'两优一先'表彰大会上以县领导身份出席。具体职务待确认。",
        "confidence": "confirmed"
    },
    # ── Other Government Leaders ──
    {
        "id": 12,
        "name": "戴传捷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn/zfxxgk/public/29641/49387811.html",
        "notes": "1971年9月出生，汉族，省委党校本科学历，中共党员。负责教育、人力资源和社会保障、交通运输等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn/zfxxgk/public/29641/52885786.html",
        "notes": "1976年11月出生，汉族，大学学历，中共党员。负责公安、司法、信访、退役军人事务等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "赵磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn/zfxxgk/public/29641/51302062.html",
        "notes": "1978年5月出生，汉族，省委党校研究生学历，中共党员。负责民政、农业农村、乡村振兴、水利、城市管理等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "阿旺伦珠",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1988年1月",
        "birthplace": "",
        "native_place": "",
        "education": "西藏自治区委员会党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn/zfxxgk/public/29641/52885798.html",
        "notes": "1988年1月出生，藏族，西藏自治区委员会党校研究生学历，中共党员。挂职副县长。负责数据资源管理、供销、融媒体等工作。",
        "confidence": "confirmed"
    },
    # ── Other Key Leaders ──
    {
        "id": 16,
        "name": "邹光玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测人大主任）",
        "current_org": "固镇县",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "多次在党代会主席台就座。排序在常委之后，推测为县人大主任。",
        "confidence": "plausible"
    },
    {
        "id": 17,
        "name": "沈明星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测政协主席）",
        "current_org": "固镇县",
        "source": "https://www.guzhen.gov.cn/gzdt/gzyw/81379146.html",
        "notes": "多次在党代会主席台就座。排序在常委之后，推测为县政协主席。",
        "confidence": "plausible"
    },
    {
        "id": 18,
        "name": "蔡腊梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（推测）",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn (政风行风热线)",
        "notes": "2025年1月以副县长身份参与政风行风热线。当前是否仍为副县长待确认。",
        "confidence": "unverified"
    },
    {
        "id": 19,
        "name": "王敬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委常委、常务副县长",
        "current_org": "固镇县人民政府",
        "source": "https://www.guzhen.gov.cn (政风行风热线)",
        "notes": "2024年8月以县委常委、常务副县长身份参与政风行风热线。现已被杨军接替常务副县长职务。去向待查。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共固镇县委",
        "type": "党委",
        "level": "县",
        "parent": "中共蚌埠市委",
        "location": "安徽省蚌埠市固镇县"
    },
    {
        "id": 2,
        "name": "固镇县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "蚌埠市人民政府",
        "location": "安徽省蚌埠市固镇县"
    },
    {
        "id": 3,
        "name": "固镇县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "蚌埠市人大常委会",
        "location": "安徽省蚌埠市固镇县"
    },
    {
        "id": 4,
        "name": "固镇县政协",
        "type": "政协",
        "level": "县",
        "parent": "蚌埠市政协",
        "location": "安徽省蚌埠市固镇县"
    },
    {
        "id": 5,
        "name": "固镇县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共固镇县委",
        "location": "安徽省蚌埠市固镇县"
    },
    {
        "id": 6,
        "name": "固镇经济开发区",
        "type": "开发区",
        "level": "县",
        "parent": "固镇县人民政府",
        "location": "安徽省蚌埠市固镇县"
    },
    {
        "id": 7,
        "name": "固镇县公安局",
        "type": "政府",
        "level": "县",
        "parent": "固镇县人民政府",
        "location": "安徽省蚌埠市固镇县"
    },
]

positions = [
    # 徐松
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-06-25", "end": "present", "rank": "正县级", "note": "第十二届县委第一次全会当选"},
    # 蓝佳勇
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present", "rank": "正县级", "note": "第十二届县委第一次全会当选副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "unknown", "end": "present", "rank": "正县级", "note": "领导县政府全面工作"},
    # 汤伟
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": "兼任县委党校校长、县经开区党工委副书记"},
    {"person_id": 3, "org_id": 6, "title": "经开区党工委副书记", "start": "unknown", "end": "present", "rank": "", "note": ""},
    # 姚军
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长人选", "start": "unknown", "end": "present", "rank": "副县级", "note": "尚未经人大正式任命"},
    # 杨军
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "unknown", "end": "present", "rank": "副县级", "note": "负责县政府常务工作"},
    # 王小兵
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": "具体分工待确认"},
    # 魏兵
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": "具体分工待确认"},
    # 钱玉
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": "具体分工待确认"},
    # 窦凯
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": "具体分工待确认"},
    # 韩冬
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": "具体分工待确认"},
    # 廖立华
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "2026-06-25", "end": "present", "rank": "副县级", "note": "具体分工待确认"},
    # 戴传捷
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副县级", "note": "负责教育、人社、交通等"},
    # 王勇
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副县级", "note": "负责公安、司法、信访等"},
    {"person_id": 13, "org_id": 7, "title": "分管公安局", "start": "unknown", "end": "present", "rank": "", "note": "负责公安局"},
    # 赵磊
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副县级", "note": "负责民政、农业农村、乡村振兴、水利等"},
    # 阿旺伦珠
    {"person_id": 15, "org_id": 2, "title": "副县长（挂职）", "start": "unknown", "end": "present", "rank": "副县级", "note": "挂职。负责数据资源、供销、融媒体等"},
    # 邹光玉
    {"person_id": 16, "org_id": 3, "title": "县人大主任（推测）", "start": "unknown", "end": "present", "rank": "正县级", "note": "推测"},
    # 沈明星
    {"person_id": 17, "org_id": 4, "title": "县政协主席（推测）", "start": "unknown", "end": "present", "rank": "正县级", "note": "推测"},
    # 蔡腊梅
    {"person_id": 18, "org_id": 2, "title": "副县长（推测）", "start": "unknown", "end": "unknown", "rank": "副县级", "note": "2025年1月仍在任"},
    # 王敬
    {"person_id": 19, "org_id": 2, "title": "原常务副县长", "start": "unknown", "end": "~2025/2026", "rank": "副县级", "note": "被杨军接替"},
]

relationships = [
    # 徐松 ↔ 蓝佳勇
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委班子搭档：书记+县长", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    # 徐松 ↔ 汤伟
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委班子正副书记", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    # 蓝佳勇 ↔ 汤伟
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县委副书记（县长+专职副书记）", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    # 杨军 → 王敬（接替）
    {"person_a": 5, "person_b": 19, "type": "predecessor_successor", "context": "杨军接替王敬任常务副县长", "overlap_org": "固镇县人民政府", "overlap_period": "~2025/2026", "confidence": "plausible"},
    # 徐松 ↔ 全体常委
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委常委班子", "overlap_org": "中共固镇县委", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    # 蓝佳勇 ↔ 政府班子成员
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "政府班子：县长+常务副县长", "overlap_org": "固镇县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "政府班子：县长+副县长", "overlap_org": "固镇县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "政府班子：县长+副县长", "overlap_org": "固镇县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "政府班子：县长+副县长", "overlap_org": "固镇县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "政府班子：县长+副县长", "overlap_org": "固镇县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "政府班子：县长+挂职副县长", "overlap_org": "固镇县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
]

# ── build database ──────────────────────────────────────────────────────

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT,
        gender TEXT,
        ethnicity TEXT,
        birth TEXT,
        birthplace TEXT,
        native_place TEXT,
        education TEXT,
        party_join TEXT,
        work_start TEXT,
        current_post TEXT,
        current_org TEXT,
        source TEXT
    )""")

    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        org_id INTEGER,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER,
        person_b INTEGER,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                     native_place, education, party_join, work_start, current_post, current_org, source)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["native_place"], p["education"],
                   p["party_join"], p["work_start"], p["current_post"],
                   p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")


# ── build GEXF ──────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_role_color(name, post):
    """Determine node color based on role."""
    if "书记" in post and "县委" in post:
        return "255,50,50"  # Red - Party Secretary
    if "县长" in post and "县委副书记" in post:
        return "50,100,255"  # Blue - Government leader
    if "副书记" in post:
        return "50,100,255"  # Blue - Deputy Secretary
    if "常务" in post:
        return "50,100,255"  # Blue
    if "副县长" in post or "副县长人选" in post:
        return "50,100,255"  # Blue
    if "纪律检查" in post or "纪委书记" in post:
        return "255,165,0"  # Orange - Discipline
    if "人大" in post:
        return "200,255,255"  # Cyan
    if "政协" in post:
        return "255,240,200"  # Cream
    return "100,100,100"  # Grey

def is_top_leader(person_id):
    return person_id in (1, 2)  # 徐松 and 蓝佳勇

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>固镇县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p["current_post"]
        org = p["current_org"]
        role_color = person_role_color(name, post)
        sz = "20.0" if is_top_leader(pid) else "12.0"

        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        col = role_color.split(",")
        lines.append(f'        <viz:color r="{col[0]}" g="{col[1]}" b="{col[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        oid = o["id"]
        org_name = o["name"]
        org_type = o["type"]
        type_colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "开发区": "200,255,200",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        col = type_colors.get(org_type, "200,200,200").split(",")

        lines.append(f'      <node id="o{oid}" label="{esc(org_name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(org_type)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{col[0]}" g="{col[1]}" b="{col[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person->Person (relationships)
    for r in relationships:
        eid += 1
        conf_weight = "2.0" if r["confidence"] == "confirmed" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{conf_weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


# ── main ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_database()
    build_gexf()
    print("✅ Done!")
    print(f"   Database: {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
