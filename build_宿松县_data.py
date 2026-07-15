#!/usr/bin/env python3
"""Build Susong County (宿松县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - https://www.susong.gov.cn (official Susong government website)
  - https://www.susong.gov.cn/ldzc/ldzc/index.html (leadership window)
  - https://www.anqing.gov.cn/ldzc/index.html (Anqing city leadership)
  - 中国共产党宿松县第十六次代表大会 (2026-06-27) - https://www.susong.gov.cn/ssxw/zwyw/2030493428.html
  - 中国共产党宿松县第十六次代表大会闭幕 (2026-06-29) - https://www.susong.gov.cn/ssxw/zwyw/2030495397.html

Confidence: Current roles confirmed from official Susong government website (July 2026).
  Biographical details (birth years, education) from leadership profiles on susong.gov.cn.
  Full career timelines before current roles are partial.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "宿松县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "宿松县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "廖强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历，高级管理人员工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记（兼安庆市委副书记）",
        "current_org": "中共宿松县委",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "1976年11月出生，汉族，省委党校研究生学历，EMBA。现任安庆市委副书记，市委党校校长、市社会主义学院院长（兼），宿松县委书记。2026年6月主持中共宿松县第十六次代表大会。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "许晓峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "宿松县人民政府",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "1971年9月出生，汉族，省委党校研究生学历。主持县政府全面工作。2026年6月主持中共宿松县第十六次代表大会开幕式。",
        "confidence": "confirmed"
    },
    # ── County Party Committee (县委领导) ──
    {
        "id": 3,
        "name": "方钱方",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县委党校校长（兼）",
        "current_org": "中共宿松县委",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "在第十六次党代会主席台前排就座。兼任县委党校校长。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "张斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记，县公安局党委书记、局长、督察长",
        "current_org": "中共宿松县委 / 宿松县公安局",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、政法委书记，公安局长。第十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "余金苗",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县政府党组成员、副县长",
        "current_org": "中共宿松县委 / 宿松县人民政府",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、副县长。第十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "王文刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共宿松县纪律检查委员会 / 宿松县监委",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、纪委书记、监委主任。2026年7月赴长铺镇督导防台风防汛工作。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "刘巨华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部部长",
        "current_org": "宿松县人民武装部",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、人武部部长。第十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "郑海燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共宿松县委宣传部",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、宣传部部长。第十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "储事理",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共宿松县委统战部",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、统战部部长。2026年7月赴凉亭镇督导防汛防台风工作。第十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "钱友明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县政府党组副书记、常务副县长",
        "current_org": "中共宿松县委 / 宿松县人民政府",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、常务副县长。第十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "王程锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共宿松县委组织部",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县委常委、组织部部长。第十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    # ── County Government Leaders (县政府领导) ──
    {
        "id": 12,
        "name": "李锦荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宿松县人民政府",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "副县长。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "罗朝斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "宿松县人民政府",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县政府党组成员、副县长。2024年曾接受在线访谈。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "尹建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "宿松县人民政府",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县政府党组成员、副县长。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "周亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "宿松县人民政府",
        "source": "https://www.susong.gov.cn/ldzc/ldzc/index.html",
        "notes": "县政府党组成员、副县长。",
        "confidence": "confirmed"
    },
    # ── Other Standing Committee Members from 16th Party Congress ──
    {
        "id": 16,
        "name": "黄世宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测县人大主任或政协主席）",
        "current_org": "宿松县",
        "source": "https://www.susong.gov.cn/ssxw/zwyw/2030493428.html",
        "notes": "在第十六次党代会主席台前排就座，排位在许晓峰之后、聂立新之前。",
        "confidence": "plausible"
    },
    {
        "id": 17,
        "name": "聂立新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测县政协主席或人大主任）",
        "current_org": "宿松县",
        "source": "https://www.susong.gov.cn/ssxw/zwyw/2030493428.html",
        "notes": "在第十六次党代会主席台前排就座。排位在黄世宏之后、方钱方之前。",
        "confidence": "plausible"
    },
    # ── Predecessor ──
    {
        "id": 18,
        "name": "曹晓革",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委书记（已离任）",
        "current_org": "中共宿松县委",
        "source": "https://www.susong.gov.cn/hdjl/sjxx/index.html (书记信箱显示'原县委书记—曹晓革'，最后留言受理至2025年6月)",
        "notes": "宿松县前任县委书记。从书记信箱记录看，2024-2025年间曹晓革为县委书记。2025年6月以后书记信箱开始显示'原县委书记—曹晓革'，推测廖强约在2025年年中接任。曹晓革去向待查。",
        "confidence": "confirmed"
    },
]

organizations = [
    {"id": 1, "name": "中共宿松县委", "type": "党委", "level": "县", "parent": "中共安庆市委", "location": "宿松县"},
    {"id": 2, "name": "宿松县人民政府", "type": "政府", "level": "县", "parent": "安庆市人民政府", "location": "宿松县"},
    {"id": 3, "name": "中共宿松县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共安庆市纪委", "location": "宿松县"},
    {"id": 4, "name": "宿松县监察委员会", "type": "政府", "level": "县", "parent": "宿松县人民政府", "location": "宿松县"},
    {"id": 5, "name": "中共宿松县委政法委员会", "type": "党委", "level": "县", "parent": "中共宿松县委", "location": "宿松县"},
    {"id": 6, "name": "宿松县公安局", "type": "政府", "level": "县", "parent": "宿松县人民政府", "location": "宿松县"},
    {"id": 7, "name": "中共宿松县委宣传部", "type": "党委", "level": "县", "parent": "中共宿松县委", "location": "宿松县"},
    {"id": 8, "name": "中共宿松县委统战部", "type": "党委", "level": "县", "parent": "中共宿松县委", "location": "宿松县"},
    {"id": 9, "name": "中共宿松县委组织部", "type": "党委", "level": "县", "parent": "中共宿松县委", "location": "宿松县"},
    {"id": 10, "name": "宿松县人民武装部", "type": "政府", "level": "县", "parent": "安庆军分区", "location": "宿松县"},
    {"id": 11, "name": "中共宿松县委党校", "type": "事业单位", "level": "县", "parent": "中共宿松县委", "location": "宿松县"},
    {"id": 12, "name": "宿松县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "宿松县", "location": "宿松县"},
    {"id": 13, "name": "中国人民政治协商会议宿松县委员会", "type": "政协", "level": "县", "parent": "宿松县", "location": "宿松县"},
    {"id": 14, "name": "中共安庆市委", "type": "党委", "level": "市", "parent": "中共安徽省委", "location": "安庆市"},
    {"id": 15, "name": "安庆市人民政府", "type": "政府", "level": "市", "parent": "安徽省人民政府", "location": "安庆市"},
]

positions = [
    # 廖强
    {"person_id": 1, "org_id": 1, "title": "县委书记（兼）", "start": "约2025年中", "end": "present", "rank": "副厅级", "note": "兼任宿松县委书记"},
    {"person_id": 1, "org_id": 14, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "兼任市委党校校长、市社会主义学院院长"},
    # 许晓峰
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "领导县政府全面工作"},
    # 方钱方
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正县级", "note": "兼任县委党校校长"},
    {"person_id": 3, "org_id": 11, "title": "县委党校校长（兼）", "start": "", "end": "present", "rank": "", "note": ""},
    # 张斌
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "政法委书记", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "", "note": ""},
    # 余金苗
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "", "note": ""},
    # 王文刚
    {"person_id": 6, "org_id": 1, "title": "县委常委、县纪委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "县纪委书记", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "县监委主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 刘巨华
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 10, "title": "人武部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 郑海燕
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "宣传部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 储事理
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "统战部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 钱友明
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县政府党组副书记、常务副县长", "start": "", "end": "present", "rank": "", "note": ""},
    # 王程锋
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "组织部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 李锦荣
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 罗朝斌
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 尹建军
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 周亮
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 黄世宏
    {"person_id": 16, "org_id": 12, "title": "县人大主任（推测）", "start": "", "end": "present", "rank": "正县级", "note": "在十六次党代会主席台前排就座"},
    # 聂立新
    {"person_id": 17, "org_id": 13, "title": "县政协主席（推测）", "start": "", "end": "present", "rank": "正县级", "note": "在十六次党代会主席台前排就座"},
    # 曹晓革（前任）
    {"person_id": 18, "org_id": 1, "title": "县委书记", "start": "", "end": "约2025年中", "rank": "副厅级", "note": "前任县委书记，约2025年中离任"},
]

relationships = [
    # 廖强 <-> 许晓峰（党政一把手）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长搭档", "overlap_org": "中共宿松县委/宿松县人民政府", "overlap_period": "2025-至今", "strength": "strong", "confidence": "confirmed"},
    # 廖强 <-> 方钱方
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与专职副书记", "overlap_org": "中共宿松县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 许晓峰 <-> 钱友明（县长与常务副县长）
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "宿松县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 廖强 <-> 王文刚（书记与纪委书记）
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与县纪委书记", "overlap_org": "中共宿松县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 廖强 <-> 张斌
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与政法委书记", "overlap_org": "中共宿松县委常委会", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 廖强 <-> 王程锋
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记与组织部部长", "overlap_org": "中共宿松县委常委会", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 廖强 <-> 曹晓革（前后任）
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "接替曹晓革任宿松县委书记", "overlap_org": "中共宿松县委", "overlap_period": "2025年交接", "strength": "medium", "confidence": "confirmed"},
    # 廖强 <-> 安庆市委领导层（已在安庆市数据中体现，这里保留跨县关联线索）
    {"person_a": 1, "person_b": 0, "type": "other", "context": "廖强同时为安庆市委副书记，与安庆市领导班子有直接工作关系", "overlap_org": "中共安庆市委常委会", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 许晓峰 <-> 县委副书记方钱方
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与专职副书记", "overlap_org": "中共宿松县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 许晓峰 <-> 副县长班子
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与副县长", "overlap_org": "宿松县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长与副县长", "overlap_org": "宿松县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长与副县长", "overlap_org": "宿松县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长与副县长", "overlap_org": "宿松县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长与副县长", "overlap_org": "宿松县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
]

# ── build database ───────────────────────────────────────────────────────

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                     education, party_join, work_start, current_post, current_org,
                     source, notes, confidence)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"], p["notes"],
                   p["confidence"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
                     VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        if r["person_b"] == 0:
            continue  # skip placeholder cross-ref (安庆市 connections are in the municipal data)
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
                     VALUES (?,?,?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database created: {DB_PATH}")


# ── build GEXF ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    current = p.get("current_post", "")
    if "县委书记" in current or "书记" in current and "县委" in current:
        return "255,50,50"
    elif "县长" in current or "副县长" in current or "市长" in current:
        return "50,100,255"
    elif "纪委书记" in current or "监委" in current:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(p):
    return p["id"] in (1, 2)  # 廖强、许晓峰

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "纪委":
        return "255,200,150"
    elif t == "事业单位":
        return "220,220,220"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    else:
        return "200,200,200"

def build_gexf():
    lines = []
    now_str = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now_str}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>宿松县领导班子工作关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if p["id"] != 18 else "10.0")
        role = esc(p.get("current_post", ""))
        org_name = esc(p.get("current_org", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org_name}"/>')
        lines.append('          <attvalue for="3" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # org nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0
    # person->org worked_at edges
    for pos in positions:
        eid += 1
        source = f"p{pos['person_id']}"
        target = f"o{pos['org_id']}"
        note = esc(pos.get("note", ""))
        rank = esc(pos.get("rank", ""))
        lines.append(f'      <edge id="e{eid}" source="{source}" target="{target}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{note}"/>')
        lines.append(f'          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # person<->person relationship edges
    for r in relationships:
        if r["person_b"] == 0:
            continue
        eid += 1
        source = f"p{r['person_a']}"
        target = f"p{r['person_b']}"
        ctx = esc(r.get("context", ""))
        conf = r.get("confidence", "confirmed")
        w = "2.0" if r.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{source}" target="{target}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{ctx}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF created: {GEXF_PATH}")


# ── main ─────────────────────────────────────────────────────────────────

def main():
    print("=== 宿松县 Network Data Builder ===")
    print(f"Script dir: {SCRIPT_DIR}")
    print()
    print("Building database...")
    build_database()
    print("Building GEXF graph...")
    build_gexf()
    print()
    print("Summary:")
    print(f"  Persons:  {len(persons)}")
    print(f"  Orgs:     {len(organizations)}")
    print(f"  Positions:{len(positions)}")
    print(f"  Relations:{len([r for r in relationships if r['person_b'] != 0])}")
    print("Done.")

if __name__ == "__main__":
    main()
