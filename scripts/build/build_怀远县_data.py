#!/usr/bin/env python3
"""Build Huaiyuan County (怀远县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.ahhy.gov.cn (official Huaiyuan government website, news articles July 2026)
  - 中国共产党怀远县第十五届委员会第一次全体会议 (2026-06-25)
  - 中国共产党怀远县第十五次代表大会 (2026-06-23)
  - 怀远县2026年7月份党政领导干部接访计划安排表 (2026-06-30)

Confirmed from 15th Party Congress (2026-06-24):
  - 李波 elected as Party Secretary (县委书记)
  - 张亮 elected as Deputy Secretary (县委副书记) and appointed as Acting Magistrate (代理县长)
  - 王岂 elected as Deputy Secretary (县委副书记)
  - 11-member Standing Committee elected

Confidence: Current roles confirmed from official government news.
  Biographical details (birth years, education) for some figures are incomplete.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "怀远县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "怀远县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "李波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、县委书记",
        "current_org": "中共怀远县委",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379044.html",
        "notes": "2026年6月24日在怀远县第十五届委员会第一次全体会议上当选为县委书记。同时任蚌埠市委常委。此前曾任怀远县长或市委另有任职。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "张亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、代理县长",
        "current_org": "怀远县人民政府",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379803.html",
        "notes": "2026年6月24日当选为县委副书记，后任代理县长。负责县政府全面工作。前期履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "王岂",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共怀远县委",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379044.html",
        "notes": "2026年6月24日当选为县委副书记。协助李波同志抓党的建设工作，负责党的农村工作、群团工作。",
        "confidence": "confirmed"
    },
    # ── Standing Committee Members (县委常委) ──
    {
        "id": 4,
        "name": "赵亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "怀远县人民政府",
        "source": "https://www.ahhy.gov.cn/xwzx/tzgg/81379519.html",
        "notes": "负责县政府常务工作，分管发改、财政、国资、金融、税务、应急管理、统计等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "丁辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共怀远县纪律检查委员会",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379044.html",
        "notes": "县纪委书记、县监委副主任、代理主任。负责纪检监察工作和县委巡察工作。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "夏孟贤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共怀远县委政法委员会",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379044.html",
        "notes": "负责政法、信访、维护稳定工作。联系县法院、县检察院。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "何振良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共怀远县委",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379044.html",
        "notes": "2026年6月24日当选为县委常委。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "杨杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员",
        "current_org": "怀远经济开发区",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379044.html",
        "notes": "怀远经济开发区党工委第一书记。负责经济开发区全面工作。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "李志军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长、统战部部长",
        "current_org": "中共怀远县委组织部",
        "source": "https://www.ahhy.gov.cn/xwzx/tzgg/81379519.html",
        "notes": "负责组织工作、统一战线工作、老干部工作、公务员工作、县委人才工作。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "蔡明星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共怀远县委宣传部",
        "source": "https://www.ahhy.gov.cn/xwzx/tzgg/81379519.html",
        "notes": "负责县委宣传思想文化工作、意识形态工作、文化产业发展工作、精神文明建设工作。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "程磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "怀远县人民政府",
        "source": "https://www.ahhy.gov.cn/xwzx/jrhy/81379044.html",
        "notes": "负责自然资源和规划、城乡建设、交通运输、城市管理、重点工程、环保等工作。",
        "confidence": "confirmed"
    },
    # ── Other Government Leaders ──
    {
        "id": 12,
        "name": "王瑛珏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "怀远县人民政府",
        "source": "https://www.ahhy.gov.cn/xwzx/tzgg/81379519.html",
        "notes": "负责教育、科技、商务、文旅、卫健、市场监管、医保等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "周彤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "怀远县人民政府",
        "source": "https://www.ahhy.gov.cn/xwzx/tzgg/81379519.html",
        "notes": "负责民政、人社、农业农村、水利、乡村振兴、供销等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "朱江涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、公安局局长",
        "current_org": "怀远县公安局",
        "source": "https://www.ahhy.gov.cn/xwzx/tzgg/81379519.html",
        "notes": "负责公安、司法、退役军人、信访维稳等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "范磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "怀远县人民政府",
        "source": "https://www.ahhy.gov.cn/xwzx/tzgg/81379519.html",
        "notes": "负责工业经济、民营经济、招商引资、经济开发区等工作。",
        "confidence": "confirmed"
    },
    # ── Predecessors ──
    {
        "id": 16,
        "name": "（前任县委书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共怀远县委（已离任）",
        "source": "",
        "notes": "李波的前任县委书记信息待查。李波2026年6月新当选为县委书记，此前他可能担任县长或其他职务。",
        "confidence": "unverified"
    },
    {
        "id": 17,
        "name": "（前任县长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "怀远县人民政府（已离任）",
        "source": "",
        "notes": "张亮的前任县长信息待查。张亮2026年7月以代理县长身份履职，此前县长职位空缺或由他人担任。",
        "confidence": "unverified"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共怀远县委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共蚌埠市委",
        "location": "怀远县"
    },
    {
        "id": 2,
        "name": "怀远县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "蚌埠市人民政府",
        "location": "怀远县"
    },
    {
        "id": 3,
        "name": "中共怀远县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共怀远县委",
        "location": "怀远县"
    },
    {
        "id": 4,
        "name": "中共怀远县委政法委员会",
        "type": "党委部门",
        "level": "县处级",
        "parent": "中共怀远县委",
        "location": "怀远县"
    },
    {
        "id": 5,
        "name": "中共怀远县委组织部",
        "type": "党委部门",
        "level": "县处级",
        "parent": "中共怀远县委",
        "location": "怀远县"
    },
    {
        "id": 6,
        "name": "中共怀远县委宣传部",
        "type": "党委部门",
        "level": "县处级",
        "parent": "中共怀远县委",
        "location": "怀远县"
    },
    {
        "id": 7,
        "name": "怀远经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "怀远县人民政府",
        "location": "怀远县"
    },
    {
        "id": 8,
        "name": "怀远县公安局",
        "type": "政府",
        "level": "县处级",
        "parent": "怀远县人民政府",
        "location": "怀远县"
    },
    {
        "id": 9,
        "name": "怀远县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "蚌埠市人大常委会",
        "location": "怀远县"
    },
    {
        "id": 10,
        "name": "政协怀远县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协蚌埠市委员会",
        "location": "怀远县"
    },
]

positions = [
    # 李波 - 市委书记、县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-06", "end": "present", "rank": "正处级（高配副厅级）", "note": "2026年6月24日怀远县第十五届委员会第一次全体会议当选为县委书记，同时任蚌埠市委常委（副厅级）"},
    # 李波前任职务 - 信息待补充
    {"person_id": 1, "org_id": 2, "title": "县长（前任职务，推测）", "start": "", "end": "2026-06", "rank": "正处级", "note": "李波在此次换届前可能担任怀远县长或其他职务，待查。从党代会由李波作十四届县委工作报告可确认他是上届县委主要领导人"},
    # 张亮
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月24日当选为县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月任怀远县代理县长，主持县政府全面工作"},
    # 王岂
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月24日当选为县委副书记。协助李波同志抓党的建设工作，分管县委办公室、县委社会工作部、县委党校等"},
    # 赵亮
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    # 丁辉
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "县纪委书记、县监委副主任、代理主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 夏孟贤
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 何振良
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    # 杨杰
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "经济开发区党工委第一书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李志军
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "组织部部长、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 蔡明星
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 程磊
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王瑛珏
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周彤
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 朱江涛
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 8, "title": "公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 范磊
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 前任县委书记（待查）
    {"person_id": 16, "org_id": 1, "title": "前任县委书记", "start": "", "end": "2026-06", "rank": "正处级", "note": "李波的前任，信息待查"},
    # 前任县长（待查）
    {"person_id": 17, "org_id": 2, "title": "前任县长", "start": "", "end": "2026-06/07", "rank": "正处级", "note": "张亮的前任，信息待查"},
]

relationships = [
    # 李波 → 张亮（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "李波任县委书记，张亮任代理县长，党政正职搭档",
     "overlap_org": "怀远县党政领导班子",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 李波 → 王岂（书记-副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "李波任县委书记，王岂任县委副书记，协助抓党建工作",
     "overlap_org": "中共怀远县委",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 李波 → 丁辉（书记-纪委书记）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "丁辉任县委常委、县纪委书记，接受县委书记李波领导",
     "overlap_org": "中共怀远县常务委员会",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 李波 → 夏孟贤（书记-政法委书记）
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "夏孟贤任县委常委、政法委书记，接受县委书记李波领导",
     "overlap_org": "中共怀远县常务委员会",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 李波 → 李志军（书记-组织部长）
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "李志军任县委常委、组织部长、统战部长，接受县委书记李波领导",
     "overlap_org": "中共怀远县常务委员会",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 李波 → 蔡明星（书记-宣传部长）
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "蔡明星任县委常委、宣传部长，接受县委书记李波领导",
     "overlap_org": "中共怀远县常务委员会",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 李波 → 其他常委
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "何振良任县委常委，接受县委书记李波领导",
     "overlap_org": "中共怀远县常务委员会",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "杨杰任县委常委、县政府党组成员，接受县委书记李波领导",
     "overlap_org": "中共怀远县常务委员会",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 张亮 → 赵亮（县长-常务副县长）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "赵亮任县委常委、常务副县长，协助代理县长张亮工作",
     "overlap_org": "怀远县人民政府",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 张亮 → 副县长们
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "程磊任县委常委、副县长，协助代理县长张亮工作",
     "overlap_org": "怀远县人民政府",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "王瑛珏任副县长，受代理县长张亮领导",
     "overlap_org": "怀远县人民政府",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "周彤任副县长，受代理县长张亮领导",
     "overlap_org": "怀远县人民政府",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "朱江涛任副县长、公安局长，受代理县长张亮领导",
     "overlap_org": "怀远县人民政府",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "范磊任副县长，受代理县长张亮领导",
     "overlap_org": "怀远县人民政府",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 李波 → 前任（未确认）
    {"person_a": 1, "person_b": 16, "type": "predecessor_successor",
     "context": "李波接替前任任怀远县委书记",
     "overlap_org": "中共怀远县委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "unverified"},
    # 张亮 → 前任县长（未确认）
    {"person_a": 2, "person_b": 17, "type": "predecessor_successor",
     "context": "张亮接替前任任怀远县长（代理）",
     "overlap_org": "怀远县人民政府",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "unverified"},
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
    if "政协" in post:
        return "200,200,200"  # grey
    if "人大" in post:
        return "200,255,255"  # cyan
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
    return "200,200,200"

def is_top(p):
    return p["id"] in (1, 2, 3)  # 李波, 张亮, 王岂

def build_gexf():
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>怀远县领导班子工作关系网络 - 2026年7月</description>')
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
    print(f"Building 怀远县 leadership network data...")
    build_database()
    build_gexf()
    print("Done.")
