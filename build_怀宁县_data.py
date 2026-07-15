#!/usr/bin/env python3
"""Build Huaining County (怀宁县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.ahhn.gov.cn (official Huaining county government website, leadership page accessed 2026-07-15)
  - 中国共产党怀宁县第十六届代表大会第一次会议 (2026-06-28)
  - 怀宁县"两优一先"表彰大会 (2026-07-01)
  - www.anqing.gov.cn (Anqing city government website, news articles July 2026)

Confidence: Current roles confirmed from official Huaining county government leadership page
  (ahhn.gov.cn/ldzchuang/). The 16th Party Congress on 2026-06-28 confirmed the full leadership
  team under 阮波 (Party Secretary) and 项薇 (County Mayor).
  Biographical details for most deputies are partial; career timelines unknown for most figures.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "怀宁县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "怀宁县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────
    {
        "id": 1,
        "name": "阮波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-07",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共怀宁县委",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15); https://www.ahhn.gov.cn/xwzx/jrhn/2030493557.html (县第十六届党代会)",
        "notes": "1971年7月生，中央党校大学学历。主持县委全面工作。2026年6月28日主持怀宁县第十六届党代会第一次会议闭幕式。接替前任余学峰任怀宁县委书记。此前曾在太湖县任职。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "项薇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-02",
        "birthplace": "",
        "native_place": "",
        "education": "历史学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县政府党组书记、县长",
        "current_org": "怀宁县人民政府",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15); https://www.ahhn.gov.cn/content/article/2030274324 (在线访谈, 2026-01-18)",
        "notes": "1986年2月出生，历史学学士。领导县政府全面工作，负责审计工作，分管县审计局。2025年11月任县委副书记、县政府党组书记、县长候选人；2026年1月已以县长身份接受在线访谈。85后县长。",
        "confidence": "confirmed"
    },
    # ── Standing Committee (县委常委) ─────────────────────────────────
    {
        "id": 3,
        "name": "代瑜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共怀宁县委",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委副书记（专职）。2026年7月1日宣读县委表彰决定。第十五届县委副书记。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "施跃平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共怀宁县委宣传部",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、宣传部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "刘决兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、监委主任",
        "current_org": "中共怀宁县纪律检查委员会 / 怀宁县监察委员会",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、县纪委书记、监委主任。纪检监察系统负责人。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "徐良平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县政府党组副书记、常务副县长",
        "current_org": "怀宁县人民政府",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委，县政府党组副书记、常务副县长。县委常委与县政府班子交叉任职。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "吕兆春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共怀宁县委组织部",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、组织部部长。组织人事系统负责人。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "余忠轩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共怀宁县委政法委员会",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、政法委书记。政法系统负责人。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "杨虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县政府副县长",
        "current_org": "怀宁县人民政府",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委，县政府副县长。县委常委与县政府班子交叉任职。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "谭宪锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共怀宁县委统一战线工作部",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委、统战部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "孙凌波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共怀宁县委",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县委常委，未标注具体分管领域。推测可能为县委办主任、人武部主官或其他特定分工常委。",
        "confidence": "confirmed"
    },
    # ── County Government (县政府领导) ──────────────────────────────────
    {
        "id": 12,
        "name": "何刘圣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "怀宁县人民政府",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县政府党组成员、副县长。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "郑三玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "怀宁县人民政府",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县政府副县长。未标注党员，推定可能为非党副县长（党外干部）。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "马健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长，县公安局局长、三级高级警长",
        "current_org": "怀宁县人民政府 / 怀宁县公安局",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县政府党组成员、副县长，县公安局局长、三级高级警长。兼管公安系统。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "何承海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "怀宁县人民政府",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县政府党组成员、副县长。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "董东应",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "怀宁县人民政府",
        "source": "https://www.ahhn.gov.cn/ldzchuang/index.html (怀宁县领导之窗, accessed 2026-07-15)",
        "notes": "县政府党组成员、副县长。",
        "confidence": "confirmed"
    },
    # ── 人大 / 政协 ────────────────────────────────────────────────────
    {
        "id": 17,
        "name": "邵伟民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "怀宁县人民代表大会常务委员会",
        "source": "https://www.ahhn.gov.cn/xwzx/jrhn/2030498139.html (全县'两优一先'表彰大会, 2026-07-01)",
        "notes": "县人大常委会主任。2026年7月1日出席全县'两优一先'表彰大会在主席台就座。2026年6月28日在县第十六届党代会主席台前排就座。",
        "confidence": "confirmed"
    },
    {
        "id": 18,
        "name": "曹紫权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议怀宁县委员会",
        "source": "https://www.ahhn.gov.cn/xwzx/jrhn/2030498139.html (全县'两优一先'表彰大会, 2026-07-01)",
        "notes": "县政协主席。2026年7月1日出席表彰大会在主席台就座。2026年6月28日在县第十六届党代会主席台前排就座。",
        "confidence": "confirmed"
    },
    # ── Predecessors ─────────────────────────────────────────────────
    {
        "id": 19,
        "name": "余学峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原怀宁县委书记，去向待查）",
        "current_org": "",
        "source": "https://www.ahhn.gov.cn/content/article/2029862186 (在线访谈, 2025-02-20)",
        "notes": "前任怀宁县委书记。2025年2月20日仍以县委书记身份接受专访。约2026年初被阮波接替。去向待查。",
        "confidence": "confirmed"
    },
    {
        "id": 20,
        "name": "王良宜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "",
        "native_place": "安徽枞阳",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜秀区委书记",
        "current_org": "中共宜秀区委",
        "source": "https://www.yixiu.gov.cn/ldzc/ (宜秀区领导之窗); build_宜秀区_data.py",
        "notes": "曾在怀宁县任职约4年（约2015-2019年），先后任怀宁县委常委、县委办主任和怀宁县委常委、组织部长。后调任安庆市委教体工委副书记、市政府副秘书长、市教体局局长，2026年6月任宜秀区委书记。属于组织系统下派怀宁镀金后回市再外派宜秀的晋升路径。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共怀宁县委", "type": "党委", "level": "县", "parent": "中共安庆市委", "location": "怀宁县"},
    {"id": 2, "name": "怀宁县人民政府", "type": "政府", "level": "县", "parent": "安庆市人民政府", "location": "怀宁县"},
    {"id": 3, "name": "中共怀宁县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共怀宁县委", "location": "怀宁县"},
    {"id": 4, "name": "怀宁县监察委员会", "type": "政府", "level": "县", "parent": "怀宁县人民政府", "location": "怀宁县"},
    {"id": 5, "name": "中共怀宁县委宣传部", "type": "党委", "level": "县", "parent": "中共怀宁县委", "location": "怀宁县"},
    {"id": 6, "name": "中共怀宁县委组织部", "type": "党委", "level": "县", "parent": "中共怀宁县委", "location": "怀宁县"},
    {"id": 7, "name": "中共怀宁县委政法委员会", "type": "党委", "level": "县", "parent": "中共怀宁县委", "location": "怀宁县"},
    {"id": 8, "name": "中共怀宁县委统一战线工作部", "type": "党委", "level": "县", "parent": "中共怀宁县委", "location": "怀宁县"},
    {"id": 9, "name": "怀宁县公安局", "type": "政府", "level": "县", "parent": "怀宁县人民政府", "location": "怀宁县"},
    {"id": 10, "name": "怀宁县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "怀宁县", "location": "怀宁县"},
    {"id": 11, "name": "中国人民政治协商会议怀宁县委员会", "type": "政协", "level": "县", "parent": "怀宁县", "location": "怀宁县"},
    {"id": 12, "name": "怀宁县审计局", "type": "政府", "level": "县", "parent": "怀宁县人民政府", "location": "怀宁县"},
    {"id": 13, "name": "中共宜秀区委", "type": "党委", "level": "县", "parent": "中共安庆市委", "location": "宜秀区"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 阮波
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作。1971年7月生。2026年6月28日主持县第十六届党代会闭幕式。"},
    # 项薇
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "领导县政府全面工作，负责审计，分管县审计局。1986年2月生。"},
    # 代瑜
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "专职副书记"},
    # 施跃平
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘决兵
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 徐良平
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 6, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 吕兆春
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 余忠轩
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 杨虎
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 谭宪锋
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孙凌波
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "未标注具体分管领域"},
    # 何刘圣
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 郑三玲
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "推定党外干部"},
    # 马健
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 14, "org_id": 9, "title": "县公安局局长", "start": "", "end": "present", "rank": "三级高级警长", "note": ""},
    # 何承海
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 董东应
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 邵伟民
    {"person_id": 17, "org_id": 10, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 曹紫权
    {"person_id": 18, "org_id": 11, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 余学峰 (前县委书记)
    {"person_id": 19, "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "前任县委书记。2025年2月仍在任。去向待查。"},
    # 王良宜 (曾在怀宁任职)
    {"person_id": 20, "org_id": 1, "title": "县委常委、县委办主任（曾任）", "start": "2015", "end": "2016", "rank": "副处级", "note": "在怀宁县任职约4年"},
    {"person_id": 20, "org_id": 6, "title": "县委常委、组织部部长（曾任）", "start": "2016", "end": "2019", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 13, "title": "区委书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "宜秀区委书记"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap (县委常委会)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记和县长，县委县政府双核心搭档", "overlap_org": "中共怀宁县委", "overlap_period": "2025/2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记和县委副书记（专职）", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记和县委常委、宣传部部长", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记和县委常委、纪委书记", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记和县委常委、常务副县长", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记和县委常委、组织部部长", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记和县委常委、政法委书记", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记和县委常委、副县长", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记和县委常委、统战部部长", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 县长 with deputies
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长和常务副县长", "overlap_org": "怀宁县人民政府", "overlap_period": "2025/2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长和副县长（县委常委）", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长和副县长", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长和副县长", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长和副县长兼公安局长", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长和副县长", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县长和副县长", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 专职副书记 connections
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县委副书记和纪委书记，同为县委班子成员", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "县委副书记和组织部长，党建系统共事", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # 纪委书记 with 政法委书记
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "纪委和政法委，纪律与法治系统", "overlap_org": "中共怀宁县委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # 政法委书记 with 公安局长
    {"person_a": 8, "person_b": 14, "type": "overlap", "context": "政法委书记和公安局长，政法系统上下级", "overlap_org": "怀宁县政法系统", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 人大/政协 with top leaders
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "县委书记和县人大常委会主任", "overlap_org": "怀宁县", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "县委书记和县政协主席", "overlap_org": "怀宁县", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "县长和县人大常委会主任", "overlap_org": "怀宁县", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "县长和县政协主席", "overlap_org": "怀宁县", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # Predecessor-successor: 余学峰 → 阮波
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "阮波接替余学峰任怀宁县委书记", "overlap_org": "中共怀宁县委", "overlap_period": "2025/2026", "strength": "strong", "confidence": "confirmed"},
    # 王良宜 - 曾在怀宁任职
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "王良宜曾任怀宁县委常委，后调任宜秀区委书记，与现任领导有潜在交接", "overlap_org": "中共怀宁县委", "overlap_period": "2015-2019", "strength": "weak", "confidence": "plausible"},
    # 常务副县长 + 其他副县长
    {"person_a": 6, "person_b": 12, "type": "overlap", "context": "常务副县长和副县长共事", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "常务副县长和副县长（常委）", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 15, "type": "overlap", "context": "常务副县长和副县长", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 16, "type": "overlap", "context": "常务副县长和副县长", "overlap_org": "怀宁县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
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
    lines.append('    <description>怀宁县领导班子工作关系网络</description>')
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
    print("  怀宁县领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
