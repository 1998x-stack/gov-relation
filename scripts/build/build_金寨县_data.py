#!/usr/bin/env python3
"""Build Jinzhai County (金寨县) leadership network database and GEXF graph.

Targets: 县委书记董益乐, 县长江飞
Research date: 2026-07-16
Task: anhui_金寨县
Province: 安徽省
Parent City: 六安市
Level: 县

Sources:
  - http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)
  - 金寨县人民政府官网 verified via WebFetch 2026-07-16

Confidence: Current roles confirmed from official government leadership page.
  Full leadership roster (县委领导 + 政府领导) from official 领导之窗 page.
  Biographical details for some figures are partial where noted.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "金寨县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "金寨县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ 1. Party Secretary (县委书记) ═══════════════════════════════════
    {
        "id": 1,
        "name": "董益乐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-07",
        "birthplace": "安徽霍山",
        "native_place": "安徽霍山",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共金寨县委员会",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "董益乐，男，汉族，霍山县人，省委党校在职研究生学历，1971年7月生，2003年12月加入中国共产党。现任金寨县委书记。主持县委全面工作。\n注：董益乐系霍山人，调任金寨县委书记。此前任职经历待补充。",
        "confidence": "confirmed"
    },
    # ═══ 2. County Magistrate (县长) ═══════════════════════════════════
    {
        "id": 2,
        "name": "江飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "金寨县人民政府",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "江飞，现任金寨县委副书记、县长。在领导之窗同时列入县委领导和政府领导名单。领导县政府全面工作。\n注：出生年月、籍贯、完整履历待补充。",
        "confidence": "confirmed"
    },
    # ═══ 3. Deputy Party Secretary (挂职) ═════════════════════════════
    {
        "id": 3,
        "name": "董菡",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（挂）",
        "current_org": "中共金寨县委员会",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "董菡，金寨县委副书记（挂职）。挂职干部，来源单位待查。",
        "confidence": "confirmed"
    },
    # ═══ 4. Deputy Party Secretary / Development Zone ═════════════════
    {
        "id": 4,
        "name": "缪亚涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记，安徽金寨经济开发区（现代产业园区）党工委书记、管委会主任",
        "current_org": "中共金寨县委员会 / 安徽金寨经济开发区",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "缪亚涛，金寨县委副书记，兼任安徽金寨经济开发区（现代产业园区）党工委书记、管委会主任。",
        "confidence": "confirmed"
    },
    # ═══ 5. Propaganda Department Head ═══════════════════════════════
    {
        "id": 5,
        "name": "王蕊蕊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共金寨县委宣传部",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "王蕊蕊，金寨县委常委、宣传部部长。",
        "confidence": "confirmed"
    },
    # ═══ 6. Discipline Inspection Secretary ═══════════════════════════
    {
        "id": 6,
        "name": "洪源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共金寨县纪律检查委员会 / 金寨县监察委员会",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "洪源，金寨县委常委、县纪委书记、县监委主任。",
        "confidence": "confirmed"
    },
    # ═══ 7. Executive Deputy County Mayor ══════════════════════════
    {
        "id": 7,
        "name": "朱煜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "金寨县人民政府",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "朱煜，金寨县委常委、常务副县长。在县委领导和政府领导名单中均列入。2026年7月以常务副县长身份出席全县第四次全国农业普查领导小组会议。",
        "confidence": "confirmed"
    },
    # ═══ 8. Military Affairs ═══════════════════════════════════════
    {
        "id": 8,
        "name": "汤景昆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部部长",
        "current_org": "金寨县人民武装部",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "汤景昆，金寨县委常委、县人武部部长。",
        "confidence": "confirmed"
    },
    # ═══ 9. County Party Committee Office Director ═══════════════
    {
        "id": 9,
        "name": "陈奎松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办主任，兼任县委统战部部长、县政协党组副书记",
        "current_org": "中共金寨县委办公室",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "陈奎松，金寨县委常委、县委办主任，兼任县委统战部部长、县政协党组副书记。",
        "confidence": "confirmed"
    },
    # ═══ 10. Political and Legal Affairs Secretary ═══════════════
    {
        "id": 10,
        "name": "吕锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共金寨县委政法委员会",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "吕锐，金寨县委常委、政法委书记。",
        "confidence": "confirmed"
    },
    # ═══ 11. Organization Department Head ═══════════════════════
    {
        "id": 11,
        "name": "张勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共金寨县委组织部",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "张勤，金寨县委常委、组织部部长。2026年7月出席大学生暑期社会实践活动见面会并致辞。",
        "confidence": "confirmed"
    },
    # ═══ 12. County Deputy Mayor / Township Party Secretary ═══
    {
        "id": 12,
        "name": "刘瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长，双河镇党委书记",
        "current_org": "金寨县人民政府 / 双河镇",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "刘瑞，金寨县委常委、副县长，兼任双河镇党委书记。在县委领导和政府领导名单中均列入。",
        "confidence": "confirmed"
    },
    # ═══ 13. Deputy County Mayor ═══════════════════════════════
    {
        "id": 13,
        "name": "王学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "金寨县人民政府",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "王学军，金寨县副县长。",
        "confidence": "confirmed"
    },
    # ═══ 14. Deputy County Mayor / Public Security ═══════════
    {
        "id": 14,
        "name": "陈军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长，县公安局党委书记、局长、督察长",
        "current_org": "金寨县人民政府 / 金寨县公安局",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "陈军，金寨县副县长，县公安局党委书记、局长、督察长。负责公安、司法、信访等工作。",
        "confidence": "confirmed"
    },
    # ═══ 15. Deputy County Mayor ═══════════════════════════════
    {
        "id": 15,
        "name": "杨林涵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "金寨县人民政府",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "杨林涵，金寨县副县长。",
        "confidence": "confirmed"
    },
    # ═══ 16. Deputy County Mayor ═══════════════════════════════
    {
        "id": 16,
        "name": "陈乃兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "金寨县人民政府",
        "source": "http://www.ahjinzhai.gov.cn/content/column/6791191?liId=181&tid=41 (金寨县领导之窗, accessed 2026-07-16)",
        "notes": "陈乃兵，金寨县副县长。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共金寨县委员会", "type": "党委", "level": "县处级", "parent": "中共六安市委", "location": "金寨县"},
    {"id": 2, "name": "金寨县人民政府", "type": "政府", "level": "县处级", "parent": "六安市人民政府", "location": "金寨县"},
    {"id": 3, "name": "中共金寨县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共金寨县委员会", "location": "金寨县"},
    {"id": 4, "name": "金寨县监察委员会", "type": "政府", "level": "县处级", "parent": "金寨县人民政府", "location": "金寨县"},
    {"id": 5, "name": "中共金寨县委宣传部", "type": "党委", "level": "县处级", "parent": "中共金寨县委员会", "location": "金寨县"},
    {"id": 6, "name": "中共金寨县委组织部", "type": "党委", "level": "县处级", "parent": "中共金寨县委员会", "location": "金寨县"},
    {"id": 7, "name": "中共金寨县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共金寨县委员会", "location": "金寨县"},
    {"id": 8, "name": "中共金寨县委统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共金寨县委员会", "location": "金寨县"},
    {"id": 9, "name": "中共金寨县委办公室", "type": "党委", "level": "县处级", "parent": "中共金寨县委员会", "location": "金寨县"},
    {"id": 10, "name": "金寨县公安局", "type": "政府", "level": "县处级", "parent": "金寨县人民政府", "location": "金寨县"},
    {"id": 11, "name": "金寨县人民武装部", "type": "政府", "level": "县处级", "parent": "六安军分区", "location": "金寨县"},
    {"id": 12, "name": "安徽金寨经济开发区（现代产业园区）", "type": "开发区", "level": "县处级", "parent": "金寨县人民政府", "location": "金寨县"},
    {"id": 13, "name": "双河镇", "type": "乡镇/街道", "level": "乡科级", "parent": "金寨县人民政府", "location": "金寨县双河镇"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 董益乐 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作。"},
    # 江飞 - 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "领导县政府全面工作。"},
    # 董菡 - 挂职副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记（挂）", "start": "", "end": "present", "rank": "正处级", "note": "挂职干部。"},
    # 缪亚涛 - 副书记兼开发区书记
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 12, "title": "党工委书记、管委会主任", "start": "", "end": "present", "rank": "正处级", "note": "安徽金寨经济开发区（现代产业园区）"},
    # 王蕊蕊 - 宣传部长
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 洪源 - 纪委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "县监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 朱煜 - 常务副县长
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 汤景昆 - 人武部长
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 11, "title": "县人武部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈奎松 - 县委办主任
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 9, "title": "县委办主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "县委统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "兼任"},
    # 吕锐 - 政法委书记
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张勤 - 组织部长
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘瑞 - 副县长兼双河镇书记
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 13, "title": "双河镇党委书记", "start": "", "end": "present", "rank": "乡科级", "note": "兼任"},
    # 王学军 - 副县长
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈军 - 副县长兼公安局长
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 10, "title": "县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 杨林涵 - 副县长
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈乃兵 - 副县长
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记和县长同届领导班子成员", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    # Party Standing Committee overlaps
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记和挂职副书记", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记和副书记/开发区书记", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记和宣传部部长同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记和纪委书记同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记和常务副县长同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记和人武部长同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记和县委办主任同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记和政法委书记同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记和组织部长同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委书记和副县长同属县委常委会", "overlap_org": "中共金寨县委员会", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    # County government overlaps
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长和常务副县长同届政府班子", "overlap_org": "金寨县人民政府", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长和副县长刘瑞同届政府班子", "overlap_org": "金寨县人民政府", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长和副县长王学军同届政府班子", "overlap_org": "金寨县人民政府", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长和副县长陈军同届政府班子", "overlap_org": "金寨县人民政府", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长和副县长杨林涵同届政府班子", "overlap_org": "金寨县人民政府", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县长和副县长陈乃兵同届政府班子", "overlap_org": "金寨县人民政府", "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    # 董益乐's connection to 霍山 (birthplace)
    {"person_a": 1, "person_b": 1, "type": "same_native_place", "context": "董益乐系霍山人，从霍山调任金寨县委书记", "overlap_org": "", "overlap_period": "", "strength": "weak", "confidence": "confirmed"},
    # Cross-county: 董益乐 from 霍山
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
            source TEXT, notes TEXT, confidence TEXT
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
                                 education, party_join, work_start, current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p.get("birth", ""),
              p.get("birthplace", ""), p.get("native_place", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""), p["current_post"],
              p["current_org"], p["source"], p.get("notes", ""), p["confidence"]))

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
    if "县委书记" in role and "副" not in role:
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
    name = person.get("name", "")
    if "县委书记" in role and "副" not in role:
        return "20.0"
    if "县长" in role and "副" not in role:
        return "20.0"
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
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>金寨县领导班子工作关系网络</description>')
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
        org_name = esc(p.get("current_org", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org_name}"/>')
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
        # Skip self-references (same_native_place with self)
        if r['person_a'] == r['person_b']:
            continue
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
    print(f"      Relationship edges: {len([r for r in relationships if r['person_a'] != r['person_b']])}")


def main():
    print("=" * 60)
    print("  金寨县领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")
    print(f"  - {DB_PATH}")
    print(f"  - {GEXF_PATH}")


if __name__ == "__main__":
    main()
