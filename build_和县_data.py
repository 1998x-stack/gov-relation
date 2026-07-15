#!/usr/bin/env python3
"""Build Hexian County (和县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Primary source: https://www.hx.gov.cn/ldzc/ (和县人民政府官网领导之窗)
As of: 2026-07-15

Confirmed from official government website:
  - 马永 — 县委书记
  - 汪学峰 — 县委副书记、县长
  - 11-member Standing Committee (县委常委)
  - 7-member Government leadership (县政府)

Confidence: Current roles confirmed from official government website.
  Biographical details (birth years beyond 马永, education, early career) are
  incomplete for most figures — web search engines (Exa rate-limited) and Baidu
  Baike (403 blocked) were unavailable during this research cycle.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "和县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "和县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "马永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-08",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历，农学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共和县委员会",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "1974年8月出生，研究生学历，农学硕士。主持县委全面工作。完整前任履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "汪学峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "和县人民政府",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委副书记、县长。主持县政府全面工作。履历待查。",
        "confidence": "confirmed"
    },
    # ── Standing Committee Members (县委常委) ──
    {
        "id": 3,
        "name": "王磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共和县委员会",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委副书记，兼任县委党校校长。协助县委书记抓党的建设工作。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "周永宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部政委",
        "current_org": "和县人民武装部",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、人武部政委。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "马恒生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "和县人民政府",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、常务副县长。负责县政府常务工作。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "向清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长，县经开区党工委书记、管委会主任",
        "current_org": "和县经济开发区",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、副县长，兼任县经济开发区党工委书记、管委会主任。负责经开区全面工作。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "赵宗军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、县监委主任",
        "current_org": "中共和县纪律检查委员会",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、纪委书记、县监委主任。负责纪检监察工作和县委巡察工作。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "袁庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长，县政协党组副书记（兼）",
        "current_org": "中共和县县委统战部",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、统战部部长，兼任县政协党组副书记。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "王皖东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共和县县委组织部",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、组织部部长。负责组织工作、人才工作、老干部工作。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "武军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共和县县委政法委员会",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、政法委书记。负责政法、信访、维护稳定工作。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "张文杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共和县县委宣传部",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县委常委、宣传部部长。负责宣传思想文化工作、意识形态工作。履历待查。",
        "confidence": "confirmed"
    },
    # ── Other Government Leaders ──
    {
        "id": 12,
        "name": "熊英华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和县人民政府",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "副县长。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "朱迎一",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和县人民政府",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "副县长。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "李珊珊",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和县人民政府",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "副县长（女性）。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "秦军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和县人民政府",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "副县长。履历待查。",
        "confidence": "confirmed"
    },
    # ── Predecessors (to be filled) ──
    {
        "id": 16,
        "name": "（前县委书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共和县委员会（已离任）",
        "source": "",
        "notes": "马永的前任县委书记。信息待查——公开资料中马永似乎已长期担任县委书记，此前或为县长或由市级调任。",
        "confidence": "unverified"
    },
    {
        "id": 17,
        "name": "（前县长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "和县人民政府（已离任）",
        "source": "",
        "notes": "汪学峰的前任县长。信息待查——搜索受限，无法确认前任县长姓名及去向。",
        "confidence": "unverified"
    },
    # ──人大主要领导和政协主席（作为图节点加入）──
    {
        "id": 18,
        "name": "倪进宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "和县人大常委会",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县人大常委会主任。履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 19,
        "name": "贾相洲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "政协和县委员会",
        "source": "https://www.hx.gov.cn/ldzc/",
        "notes": "县政协主席。履历待查。",
        "confidence": "confirmed"
    },
]

organizations = [
    {"id": 1, "name": "中共和县委员会", "type": "党委", "level": "县处级", "parent": "中共马鞍山市委", "location": "和县"},
    {"id": 2, "name": "和县人民政府", "type": "政府", "level": "县处级", "parent": "马鞍山市人民政府", "location": "和县"},
    {"id": 3, "name": "中共和县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共和县委员会", "location": "和县"},
    {"id": 4, "name": "和县人民武装部", "type": "政府", "level": "县处级", "parent": "马鞍山军分区", "location": "和县"},
    {"id": 5, "name": "中共和县县委组织部", "type": "党委部门", "level": "县处级", "parent": "中共和县委员会", "location": "和县"},
    {"id": 6, "name": "中共和县县委宣传部", "type": "党委部门", "level": "县处级", "parent": "中共和县委员会", "location": "和县"},
    {"id": 7, "name": "中共和县县委统战部", "type": "党委部门", "level": "县处级", "parent": "中共和县委员会", "location": "和县"},
    {"id": 8, "name": "中共和县县委政法委员会", "type": "党委部门", "level": "县处级", "parent": "中共和县委员会", "location": "和县"},
    {"id": 9, "name": "和县经济开发区", "type": "开发区", "level": "县处级", "parent": "和县人民政府", "location": "和县"},
    {"id": 10, "name": "中共和县县委党校", "type": "事业单位", "level": "县处级", "parent": "中共和县委员会", "location": "和县"},
    {"id": 11, "name": "和县人大常委会", "type": "人大", "level": "县处级", "parent": "马鞍山市人大常委会", "location": "和县"},
    {"id": 12, "name": "政协和县委员会", "type": "政协", "level": "县处级", "parent": "政协马鞍山市委员会", "location": "和县"},
]

positions = [
    # 马永
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作。任现职时间待查。"},
    # 汪学峰
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作。任现职时间待查。"},
    # 王磊
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start": "", "end": "present", "rank": "副处级", "note": "兼任县委党校校长。协助县委书记抓党的建设工作。"},
    {"person_id": 3, "org_id": 10, "title": "县委党校校长（兼）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周永宏
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "人武部政委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 马恒生
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府常务工作。"},
    # 向清
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 9, "title": "经开区党工委书记、管委会主任（兼）", "start": "", "end": "present", "rank": "副处级", "note": "负责经济开发区全面工作。"},
    # 赵宗军
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级", "note": "负责纪检监察工作和县委巡察工作。"},
    # 袁庆
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "兼任县政协党组副书记。"},
    # 王皖东
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "负责组织工作、人才工作。"},
    # 武军
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "负责政法、信访、维护稳定工作。"},
    # 张文杰
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "负责宣传思想文化工作、意识形态工作。"},
    # 熊英华
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认。"},
    # 朱迎一
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认。"},
    # 李珊珊
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认。"},
    # 秦军
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认。"},
    # 前县委书记（待查）
    {"person_id": 16, "org_id": 1, "title": "前县委书记", "start": "", "end": "", "rank": "正处级", "note": "信息待查。"},
    # 前县长（待查）
    {"person_id": 17, "org_id": 2, "title": "前县长", "start": "", "end": "", "rank": "正处级", "note": "信息待查。"},
    # 倪进宏
    {"person_id": 18, "org_id": 11, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 贾相洲
    {"person_id": 19, "org_id": 12, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    # 马永 → 汪学峰（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "马永任县委书记，汪学峰任县长，党政正职搭档",
     "overlap_org": "和县党政领导班子",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 马永 → 王磊（书记-专职副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "马永任县委书记，王磊任专职副书记，协助抓党建工作",
     "overlap_org": "中共和县委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 马永 → 各常委（书记-常委）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "周永宏任县委常委，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "马恒生任县委常委、常务副县长，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "向清任县委常委、副县长，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "赵宗军任县委常委、纪委书记，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "袁庆任县委常委、统战部长，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "王皖东任县委常委、组织部长，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "武军任县委常委、政法委书记，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "张文杰任县委常委、宣传部长，接受县委书记马永领导",
     "overlap_org": "中共和县常务委员会",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 汪学峰 → 马恒生（县长-常务副县长）
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "马恒生任常务副县长，协助县长汪学峰工作",
     "overlap_org": "和县人民政府",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 汪学峰 → 其他副县长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "向清任副县长，受县长汪学峰领导",
     "overlap_org": "和县人民政府",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "熊英华任副县长，受县长汪学峰领导",
     "overlap_org": "和县人民政府",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "朱迎一任副县长，受县长汪学峰领导",
     "overlap_org": "和县人民政府",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "李珊珊任副县长，受县长汪学峰领导",
     "overlap_org": "和县人民政府",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "秦军任副县长，受县长汪学峰领导",
     "overlap_org": "和县人民政府",
     "overlap_period": "至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 马永 → 前任（待确认）
    {"person_a": 1, "person_b": 16, "type": "predecessor_successor",
     "context": "马永接替前任任和县县委书记",
     "overlap_org": "中共和县委员会",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "unverified"},
    # 汪学峰 → 前任县长（待确认）
    {"person_a": 2, "person_b": 17, "type": "predecessor_successor",
     "context": "汪学峰接替前任任和县县长",
     "overlap_org": "和县人民政府",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "unverified"},
    # 马永 → 倪进宏（书记-人大主任）
    {"person_a": 1, "person_b": 18, "type": "colleague",
     "context": "马永任县委书记，倪进宏任县人大常委会主任，党委与人大主要领导",
     "overlap_org": "和县四大班子",
     "overlap_period": "至今",
     "strength": "medium",
     "confidence": "confirmed"},
    # 马永 → 贾相洲（书记-政协主席）
    {"person_a": 1, "person_b": 19, "type": "colleague",
     "context": "马永任县委书记，贾相洲任县政协主席，党委与政协主要领导",
     "overlap_org": "和县四大班子",
     "overlap_period": "至今",
     "strength": "medium",
     "confidence": "confirmed"},
]


# ======================================================================
#  SQLite Builder
# ======================================================================

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT,
            overlap_period TEXT, strength TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"],
             p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"],
             r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Orgs:    {len(organizations)}")
    print(f"    Pos:     {len(positions)}")
    print(f"    Rel:     {len(relationships)}")


# ======================================================================
#  GEXF Builder (string-format to avoid ElementTree namespace issues)
# ======================================================================

def esc(s):
    """XML-escape."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def role_color(p):
    """Color by role."""
    post = p["current_post"]
    if "书记" in post and ("县委" in post or "市委" in post):
        return "255,50,50"    # red — Party Secretary
    if "县长" in post or "区长" in post:
        return "50,100,255"   # blue — Government leader
    if "纪委书记" in post:
        return "255,165,0"    # orange — Discipline
    if "政法委" in post:
        return "200,200,100"  # yellow-brown
    if "组织" in post:
        return "150,100,200"  # purple
    if "宣传" in post:
        return "100,150,200"  # blue-grey
    if "统战" in post:
        return "180,130,180"  # mauve
    if "政协" in post:
        return "200,200,200"  # grey
    if "人大" in post:
        return "200,255,255"  # cyan
    if "人武部" in post:
        return "150,180,100"  # olive
    if "前任" in post:
        return "180,180,180"  # light grey for predecessors
    return "100,100,100"      # grey

def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,220,180"
    if "政协" in t:
        return "255,240,200"
    if "人大" in t:
        return "200,255,255"
    if "开发区" in t:
        return "200,255,200"
    if "党委部门" in t or "党委部门" in t:
        return "240,220,240"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"

def is_top(p):
    return p["id"] in (1, 2, 3)  # 马永, 汪学峰, 王磊

def build_gexf():
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>和县领导班子工作关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = role_color(p)
        sz = "20.0" if is_top(p) else "12.0"
        conf = p.get("confidence", "unverified")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{conf}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        cs = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── edges ──
    lines.append('    <edges>')
    eid = 0

    # person→organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF: {GEXF_PATH}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {eid}")


# ======================================================================
#  Main
# ======================================================================

if __name__ == "__main__":
    print(f"Building 和县 leadership network data...")
    build_database()
    build_gexf()
    print("Done.")
