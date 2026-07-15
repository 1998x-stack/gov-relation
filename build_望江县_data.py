#!/usr/bin/env python3
"""Build Wangjiang County (望江县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.wangjiang.gov.cn/ldzc/ (official Wangjiang county government leadership page, accessed 2026-07-15)
  - 望江县人民政府关于县政府负责同志工作分工的通知 (望政〔2026〕7号, 2026-05-19)
  - 全力打造长三角港产城联动发展纺织强县滨江新城——专访望江县委书记汪久清 (2026-01-06)
  - www.anqing.gov.cn/ldzc/ (Anqing city government leadership page)

Confidence: Current roles confirmed from official Wangjiang county government leadership page
  (wangjiang.gov.cn/ldzc/). 毛万青 succeeded 汪久清 as Party Secretary sometime between
  January and July 2026. Biographical details for most deputies are partial; career
  histories largely unknown.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "望江县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "望江县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "毛万青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共望江县委",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "1975年2月生，大学学历，中共党员。主持县委全面工作。接替前任汪久清任望江县委书记（汪久清2026年1月6日仍以县委书记身份接受专访）。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "朱显璋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-03",
        "birthplace": "",
        "native_place": "",
        "education": "大学，医学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县政府党组书记、县长",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/xwzx/wjyw/2030508446.html (招商考察, 2026-07-08)",
        "notes": "1987年3月出生，大学学历，医学学士，中共党员。领导县政府全面工作。2026年已以县长身份多次主持召开县政府常务会（第56-58次），率队赴杭州招商。87后县长。",
        "confidence": "confirmed"
    },
    # ── Standing Committee (县委常委) ────────────────────────────────────
    {
        "id": 3,
        "name": "倪文主",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共望江县委",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "县委副书记（专职）。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "都宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监察委员会主任",
        "current_org": "中共望江县纪律检查委员会 / 望江县监察委员会",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、县纪委书记、监委主任。纪检监察系统负责人。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "方夏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县政府党组副书记、常务副县长",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/public/19635638/2030437797.html (县政府工作分工, 2026-05-19)",
        "notes": "县委常委，县政府党组副书记、常务副县长。负责开发区、发改、财政、人社、文旅、应急、统计、金融等。县委常委与县政府班子交叉任职。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "周晓霞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共望江县委统一战线工作部",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、统战部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "徐冬冬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县政府党组成员、副县长",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/public/19635638/2030437797.html (县政府工作分工, 2026-05-19)",
        "notes": "县委常委，县政府党组成员、副县长。负责科技工信、生态环保、教育、招商引资、企业服务、营商环境等。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "金鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共望江县委政法委员会",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、政法委书记。政法系统负责人。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "周祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共望江县委宣传部",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、宣传部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "骆顺鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共望江县委组织部",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、组织部部长。组织人事系统负责人。",
        "confidence": "confirmed"
    },
    # ── County Government (县政府领导) ─────────────────────────────────────
    {
        "id": 11,
        "name": "王小节",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/public/19635638/2030437797.html (县政府工作分工, 2026-05-19)",
        "notes": "县政府党组成员、副县长。负责住建、重点工程、自然资源和规划、城管、交通等。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "储爱星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/public/19635638/2030437797.html (县政府工作分工, 2026-05-19)",
        "notes": "县政府副县长。负责卫生健康、医保、市场监管等。未标注党员，推定可能为非党副县长（党外干部）。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "吴挺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长，县公安局党委书记、局长、督察长",
        "current_org": "望江县县人民政府 / 望江县公安局",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/public/19635638/2030437797.html (县政府工作分工, 2026-05-19)",
        "notes": "县政府党组成员、副县长，县公安局党委书记、局长、督察长。负责公安、司法、退役军人、信访等。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "刘正虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/public/19635638/2030437797.html (县政府工作分工, 2026-05-19)",
        "notes": "县政府党组成员、副县长。负责商务、数据资源、民政、残联等，协助安全生产工作。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "刘汪洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长（挂职）",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15); https://www.wangjiang.gov.cn/public/19635638/2030437797.html (县政府工作分工, 2026-05-19)",
        "notes": "县政府党组成员、副县长（挂职）。负责农业农村、乡村振兴、水务、林业、供销等。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "高广飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长（挂职）",
        "current_org": "望江县人民政府",
        "source": "https://www.wangjiang.gov.cn/ldzc/ (望江县领导之窗, accessed 2026-07-15)",
        "notes": "县政府党组成员、副县长（挂职）。分工未在2026年5月工作分工通知中列出，推定为新近到任或分管专项工作。",
        "confidence": "confirmed"
    },
    # ── 人大 / 政协 ─────────────────────────────────────────────────────
    # 人大、政协主要领导未在领导之窗页面直接列出，待补
    # ── Predecessors ─────────────────────────────────────────────────────
    {
        "id": 17,
        "name": "汪久清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原望江县委书记，去向待查）",
        "current_org": "",
        "source": "https://www.wangjiang.gov.cn/content/article/2030247056 (专访望江县委书记汪久清, 2026-01-06)",
        "notes": "前任望江县委书记。2026年1月6日仍以县委书记身份接受新年专访。约2026年上半年被毛万青接替。去向待查。",
        "confidence": "confirmed"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共望江县委", "type": "党委", "level": "县", "parent": "中共安庆市委", "location": "望江县"},
    {"id": 2, "name": "望江县人民政府", "type": "政府", "level": "县", "parent": "安庆市人民政府", "location": "望江县"},
    {"id": 3, "name": "中共望江县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共望江县委", "location": "望江县"},
    {"id": 4, "name": "望江县监察委员会", "type": "政府", "level": "县", "parent": "望江县人民政府", "location": "望江县"},
    {"id": 5, "name": "中共望江县委宣传部", "type": "党委", "level": "县", "parent": "中共望江县委", "location": "望江县"},
    {"id": 6, "name": "中共望江县委组织部", "type": "党委", "level": "县", "parent": "中共望江县委", "location": "望江县"},
    {"id": 7, "name": "中共望江县委政法委员会", "type": "党委", "level": "县", "parent": "中共望江县委", "location": "望江县"},
    {"id": 8, "name": "中共望江县委统一战线工作部", "type": "党委", "level": "县", "parent": "中共望江县委", "location": "望江县"},
    {"id": 9, "name": "望江县公安局", "type": "政府", "level": "县", "parent": "望江县人民政府", "location": "望江县"},
    {"id": 10, "name": "望江县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "望江县", "location": "望江县"},
    {"id": 11, "name": "中国人民政治协商会议望江县委员会", "type": "政协", "level": "县", "parent": "望江县", "location": "望江县"},
    {"id": 12, "name": "望江经济开发区", "type": "开发区", "level": "县", "parent": "望江县人民政府", "location": "望江县"},
]

# ── Positions ─────────────────────────────────────────────────────────────

positions = [
    # 毛万青
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作。1975年2月生。接替前任汪久清。"},
    # 朱显璋
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "领导县政府全面工作。1987年3月生，医学学士。"},
    # 倪文主
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "专职副书记"},
    # 都宏
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 方夏
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责发改、财政、人社、文旅、金融等"},
    # 周晓霞
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 徐冬冬
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责科技工信、生态环保、教育、招商等"},
    # 金鑫
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周祥
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 骆顺鑫
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王小节
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员，负责住建、自然资源、城管、交通等"},
    # 储爱星
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "推定党外干部，负责卫健、医保、市场监管等"},
    # 吴挺
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 13, "org_id": 9, "title": "县公安局局长", "start": "", "end": "present", "rank": "", "note": "县公安局党委书记、局长、督察长"},
    # 刘正虎
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员，负责商务、数据资源、民政等"},
    # 刘汪洋
    {"person_id": 15, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员，负责农业农村、乡村振兴、水务等"},
    # 高广飞
    {"person_id": 16, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 汪久清 (前县委书记)
    {"person_id": 17, "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "前任县委书记。2026年1月6日仍在任。去向待查。"},
]

# ── Relationships ─────────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap (县委常委会)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记和县长，县委县政府双核心搭档", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记和县委副书记（专职）", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记和县委常委、纪委书记", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记和县委常委、常务副县长", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记和县委常委、统战部部长", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记和县委常委、副县长", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记和县委常委、政法委书记", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记和县委常委、宣传部部长", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记和县委常委、组织部部长", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 县长 with deputies
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长和常务副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长和副县长（县委常委）", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长和副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长和副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长和副县长兼公安局长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长和副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长和挂职副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县长和挂职副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 专职副书记 connections
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委副书记和纪委书记，同为县委班子成员", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "县委副书记和组织部长，党建系统共事", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # 纪委书记 with 政法委书记
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "纪委和政法委，纪律与法治系统", "overlap_org": "中共望江县委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # 政法委书记 with 公安局长
    {"person_a": 8, "person_b": 13, "type": "overlap", "context": "政法委书记和公安局长，政法系统上下级", "overlap_org": "望江县政法系统", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 常务副县长 with other 副县长
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "常务副县长和副县长（常委）", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "常务副县长和副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 14, "type": "overlap", "context": "常务副县长和副县长", "overlap_org": "望江县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # Predecessor-successor: 汪久清 → 毛万青
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor", "context": "毛万青接替汪久清任望江县委书记", "overlap_org": "中共望江县委", "overlap_period": "2025/2026", "strength": "strong", "confidence": "confirmed"},
]


# ══════════════════════════════════════════════════════════════════════════
# Database + GEXF generation
# ══════════════════════════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org, source, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"], p["confidence"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")
    print(f"      Persons: {len(persons)}")
    print(f"      Organizations: {len(organizations)}")
    print(f"      Positions: {len(positions)}")
    print(f"      Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "县委" in role and "副" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "县长" in role and "副" not in role:
        return "50,100,255"  # Blue for County Mayor
    if "纪委" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "人大" in role:
        return "200,255,255"  # Cyan for People's Congress
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on rank."""
    role = person.get("current_post", "")
    if "县委书记" in role and "副" not in role:
        return "20.0"
    if "县长" in role and "副" not in role:
        return "20.0"
    if "人大" in role or "政协" in role:
        return "15.0"
    if "常委" in role:
        return "15.0"
    return "12.0"


def org_color(org):
    """Return 'r,g,b' string for organization type."""
    t = org.get("type", "")
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_colors.get(t, "200,200,200")


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>望江县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="rank" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        role = esc(p.get("current_post", ""))
        org = esc(p.get("current_org", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization edges (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["strength"]}"/>')
        lines.append(f'          <attvalue for="3" value="{r["overlap_period"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph created: {GEXF_PATH}")
    print(f"      Person nodes: {len(persons)}")
    print(f"      Organization nodes: {len(organizations)}")
    print(f"      Worked-at edges: {len(positions)}")
    print(f"      Relationship edges: {len(relationships)}")


def main():
    print("=" * 60)
    print("  望江县领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
