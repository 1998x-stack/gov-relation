#!/usr/bin/env python3
"""Build Anqing (安庆市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.anqing.gov.cn (official government website, leadership page accessed 2026-07-15)
  - www.anqing.gov.cn/ldzc/index.html (市委领导 + 政府领导 listings)
  - www.anqing.gov.cn/xwxx/zwyw/ (news articles July 2026)

Confidence: Current roles confirmed from official Anqing government leadership page
  (anqing.gov.cn/ldzc/). Biographical details for most figures are partial; career
  timelines sourced from official profiles and available public records.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "安庆市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "安庆市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────
    {
        "id": 1,
        "name": "孟景伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "",
        "native_place": "河南汝州",
        "education": "研究生，经济学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共安庆市委",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://en.wikipedia.org/wiki/Anqing",
        "notes": "1974年5月生，河南汝州人，研究生学历，经济学博士学位。此前任北京市通州区委书记。2025年8月跨省调任安庆市委书记。主持市委全面工作。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "张君毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "",
        "native_place": "安徽涡阳",
        "education": "研究生，管理学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "安庆市人民政府",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://www.anqing.gov.cn/public/3902119/2007351992.html",
        "notes": "1970年2月生，安徽涡阳人，研究生学历，管理学硕士学位。2021年8月起任安庆市长。领导市政府全面工作。",
        "confidence": "confirmed"
    },
    # ── Municipal Party Committee (市委领导) ─────────────────────────
    {
        "id": 3,
        "name": "廖强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记（兼），市委党校校长、市社会主义学院院长，宿松县委书记",
        "current_org": "中共安庆市委",
        "source": "https://www.anqing.gov.cn/ldzc/index.html (安庆市领导之窗, accessed 2026-07-15)",
        "notes": "市委副书记，兼任市委党校校长、市社会主义学院院长，同时兼任宿松县委书记。出席市自然资源规划委员会(2026-07-15)。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "周建春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委，市政府党组成员、副市长",
        "current_org": "中共安庆市委 / 安庆市人民政府",
        "source": "https://www.anqing.gov.cn/ldzc/index.html (安庆市领导之窗, accessed 2026-07-15)",
        "notes": "市委常委、副市长。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "徐雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委，市政府党组副书记、常务副市长",
        "current_org": "中共安庆市委 / 安庆市人民政府",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://www.anqing.gov.cn/content/article/2007330626",
        "notes": "市委常委、常务副市长。2026年6月28日参加在线访谈回复市民问题。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "王家权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委，安庆军分区大校司令员",
        "current_org": "中共安庆市委 / 安庆军分区",
        "source": "https://www.anqing.gov.cn/ldzc/index.html (安庆市领导之窗, accessed 2026-07-15)",
        "notes": "市委常委、安庆军分区大校司令员。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "梁龙义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共安庆市委组织部",
        "source": "https://www.anqing.gov.cn/ldzc/index.html (安庆市领导之窗, accessed 2026-07-15)",
        "notes": "市委常委、组织部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "刘婉贞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委，桐城市委书记",
        "current_org": "中共安庆市委 / 中共桐城市委",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://www.anqing.gov.cn/xwxx/qxdt/2007355469.html",
        "notes": "市委常委，同时兼任桐城市委书记。2026年7月13日主持桐城市委常委会会议。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "吴宏波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任候选人",
        "current_org": "中共安庆市纪委 / 安庆市监委",
        "source": "https://www.anqing.gov.cn/ldzc/index.html (安庆市领导之窗, accessed 2026-07-15)",
        "notes": "市委常委、市纪委书记、市监委主任候选人。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "关家涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记，市公安局党委书记、局长、督察长",
        "current_org": "中共安庆市委政法委 / 安庆市公安局",
        "source": "https://www.anqing.gov.cn/ldzc/index.html (安庆市领导之窗, accessed 2026-07-15)",
        "notes": "市委常委、政法委书记，兼公安局党委书记、局长、督察长。",
        "confidence": "confirmed"
    },
    # ── Government Leaders (市政府领导) ──────────────────────────────
    {
        "id": 11,
        "name": "唐厚明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府党组成员、副市长、秘书长",
        "current_org": "安庆市人民政府",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://www.anqing.gov.cn/content/article/2007309128",
        "notes": "副市长、秘书长。2026年4月28日参加在线访谈回复市民问题。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "章洪海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "安庆市人民政府",
        "source": "https://www.anqing.gov.cn/ldzc/index.html (安庆市领导之窗, accessed 2026-07-15)",
        "notes": "副市长。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "李岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "安庆市人民政府",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://www.anqing.gov.cn/content/article/2007261350",
        "notes": "副市长。2025年10月28日参加在线访谈回复市民问题。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "杨旭东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府党组成员，安庆经济技术开发区党工委书记兼管委会主任",
        "current_org": "安庆经济技术开发区",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://www.anqing.gov.cn/xwxx/qxdt/2007355655.html",
        "notes": "市政府党组成员，安庆经开区党工委书记兼管委会主任。2026年7月13日督导经开区防汛防台风工作。",
        "confidence": "confirmed"
    },
    # ── Municipal People's Congress (市人大常委会) ───────────────────
    {
        "id": 15,
        "name": "周东明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "安庆市人大常委会",
        "source": "https://www.anqing.gov.cn/xwxx/zwyw/2007356408.html (市人大常委会党组会议, 2026-07-15)",
        "notes": "2026年7月15日主持市人大常委会党组会议暨理论学习中心组学习会。",
        "confidence": "confirmed"
    },
    # ── Municipal CPPCC (市政协) ─────────────────────────────────────
    {
        "id": 16,
        "name": "花家红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "安庆市政协",
        "source": "https://www.anqing.gov.cn/xwxx/zwyw/2007356402.html (市政协党组理论学习中心组会议, 2026-07-15)",
        "notes": "2026年7月15日主持市政协党组理论学习中心组（扩大）会议。",
        "confidence": "confirmed"
    },
    # ── Predecessors ────────────────────────────────────────────────
    {
        "id": 17,
        "name": "张祥安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安徽省政协副主席",
        "current_org": "安徽省政协",
        "source": "https://en.wikipedia.org/wiki/Anqing",
        "notes": "2021-2025年任安庆市委书记。2025年卸任后任安徽省政协副主席。",
        "confidence": "confirmed"
    },
    {
        "id": 18,
        "name": "陈冰冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安徽省人大常委会社会建设工作委员会主任",
        "current_org": "安徽省人大常委会",
        "source": "https://en.wikipedia.org/wiki/Anqing",
        "notes": "2016-2021年任安庆市长。2021年卸任后任安徽省人大常委会社会建设工作委员会主任。",
        "confidence": "confirmed"
    },
    {
        "id": 19,
        "name": "魏晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安徽省人大常委会副主任",
        "current_org": "安徽省人大常委会",
        "source": "https://en.wikipedia.org/wiki/Anqing",
        "notes": "2013-2016年任安庆市长，2016-2021年任安庆市委书记。现任安徽省人大常委会副主任。",
        "confidence": "confirmed"
    },
    {
        "id": 20,
        "name": "虞爱华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安徽省政协副主席",
        "current_org": "安徽省政协",
        "source": "https://en.wikipedia.org/wiki/Anqing",
        "notes": "2012-2013年任安庆市长，2013-2016年任安庆市委书记。后历任安徽省委宣传部部长、合肥市委书记、省委副书记。现任安徽省政协副主席。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共安庆市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "安庆市"},
    {"id": 2, "name": "安庆市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "安庆市"},
    {"id": 3, "name": "中共安庆市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共安庆市委", "location": "安庆市"},
    {"id": 4, "name": "安庆市监察委员会", "type": "政府", "level": "地级市", "parent": "安庆市人民政府", "location": "安庆市"},
    {"id": 5, "name": "中共安庆市委组织部", "type": "党委", "level": "地级市", "parent": "中共安庆市委", "location": "安庆市"},
    {"id": 6, "name": "中共安庆市委政法委员会", "type": "党委", "level": "地级市", "parent": "中共安庆市委", "location": "安庆市"},
    {"id": 7, "name": "安庆市公安局", "type": "政府", "level": "地级市", "parent": "安庆市人民政府", "location": "安庆市"},
    {"id": 8, "name": "安庆军分区", "type": "政府", "level": "地级市", "parent": "安徽省军区", "location": "安庆市"},
    {"id": 9, "name": "中共桐城市委", "type": "党委", "level": "县级市", "parent": "中共安庆市委", "location": "桐城市"},
    {"id": 10, "name": "中共宿松县委", "type": "党委", "level": "县", "parent": "中共安庆市委", "location": "宿松县"},
    {"id": 11, "name": "中共安庆市委党校", "type": "事业单位", "level": "地级市", "parent": "中共安庆市委", "location": "安庆市"},
    {"id": 12, "name": "安庆市社会主义学院", "type": "事业单位", "level": "地级市", "parent": "中共安庆市委", "location": "安庆市"},
    {"id": 13, "name": "安庆经济技术开发区", "type": "开发区", "level": "地级市", "parent": "安庆市人民政府", "location": "安庆市"},
    {"id": 14, "name": "安庆市人大常委会", "type": "人大", "level": "地级市", "parent": "安庆市", "location": "安庆市"},
    {"id": 15, "name": "安庆市政协", "type": "政协", "level": "地级市", "parent": "安庆市", "location": "安庆市"},
    {"id": 16, "name": "中共安庆市委宣传部", "type": "党委", "level": "地级市", "parent": "中共安庆市委", "location": "安庆市"},
    {"id": 17, "name": "中共安庆市委统一战线工作部", "type": "党委", "level": "地级市", "parent": "中共安庆市委", "location": "安庆市"},
    {"id": 18, "name": "安庆市发展和改革委员会", "type": "政府", "level": "地级市", "parent": "安庆市人民政府", "location": "安庆市"},
    {"id": 19, "name": "安徽省人大常委会", "type": "人大", "level": "省级", "parent": "安徽省", "location": "合肥市"},
    {"id": 20, "name": "安徽省政协", "type": "政协", "level": "省级", "parent": "安徽省", "location": "合肥市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 孟景伟
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "主持市委全面工作。1974年5月生。"},
    # 张君毅
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正厅级", "note": "领导市政府全面工作。1970年2月生。"},
    # 廖强
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "兼任市委党校校长、市社会主义学院院长、宿松县委书记"},
    {"person_id": 3, "org_id": 10, "title": "县委书记（兼）", "start": "", "end": "present", "rank": "副厅级", "note": "宿松县委书记"},
    {"person_id": 3, "org_id": 11, "title": "市委党校校长（兼）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "市社会主义学院院长（兼）", "start": "", "end": "present", "rank": "", "note": ""},
    # 周建春
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 徐雄
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组副书记"},
    # 王家权
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "大校司令员", "start": "", "end": "present", "rank": "", "note": "安庆军分区"},
    # 梁龙义
    {"person_id": 7, "org_id": 1, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘婉贞
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 9, "title": "桐城市委书记", "start": "", "end": "present", "rank": "副厅级", "note": "2026年7月主持桐城市委常委会会议"},
    # 吴宏波
    {"person_id": 9, "org_id": 1, "title": "市委常委、市纪委书记", "start": "", "end": "present", "rank": "副厅级", "note": "市监委主任候选人"},
    {"person_id": 9, "org_id": 3, "title": "市纪委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "市监委主任候选人", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 关家涛
    {"person_id": 10, "org_id": 1, "title": "市委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "党委书记、局长、督察长", "start": "", "end": "present", "rank": "", "note": "市公安局"},
    # 唐厚明
    {"person_id": 11, "org_id": 2, "title": "副市长、秘书长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员"},
    # 章洪海
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员"},
    # 李岩
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 杨旭东
    {"person_id": 14, "org_id": 2, "title": "市政府党组成员", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 13, "title": "党工委书记兼管委会主任", "start": "", "end": "present", "rank": "", "note": "安庆经济技术开发区"},
    # 周东明
    {"person_id": 15, "org_id": 14, "title": "党组书记、主任", "start": "", "end": "present", "rank": "正厅级", "note": "市人大常委会"},
    # 花家红
    {"person_id": 16, "org_id": 15, "title": "党组书记、主席", "start": "", "end": "present", "rank": "正厅级", "note": "市政协"},
    # 张祥安 (前市委书记)
    {"person_id": 17, "org_id": 1, "title": "市委书记（前任）", "start": "2021", "end": "2025", "rank": "正厅级", "note": "前任安庆市委书记"},
    {"person_id": 17, "org_id": 20, "title": "安徽省政协副主席", "start": "2025", "end": "present", "rank": "副省级", "note": "晋升副省级"},
    # 陈冰冰 (前市长)
    {"person_id": 18, "org_id": 2, "title": "市长（前任）", "start": "2016", "end": "2021", "rank": "正厅级", "note": "前任安庆市长"},
    {"person_id": 18, "org_id": 19, "title": "社会建设工作委员会主任", "start": "2021", "end": "present", "rank": "正厅级", "note": ""},
    # 魏晓明
    {"person_id": 19, "org_id": 2, "title": "市长", "start": "2013", "end": "2016", "rank": "正厅级", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "市委书记", "start": "2016", "end": "2021", "rank": "正厅级", "note": ""},
    {"person_id": 19, "org_id": 19, "title": "安徽省人大常委会副主任", "start": "2021", "end": "present", "rank": "副省级", "note": ""},
    # 虞爱华
    {"person_id": 20, "org_id": 2, "title": "市长", "start": "2012", "end": "2013", "rank": "正厅级", "note": ""},
    {"person_id": 20, "org_id": 1, "title": "市委书记", "start": "2013", "end": "2016", "rank": "正厅级", "note": ""},
    {"person_id": 20, "org_id": 20, "title": "安徽省政协副主席", "start": "", "end": "present", "rank": "副省级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap (市委常委会)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记和市长同届领导班子成员", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记和市委副书记（兼宿松县委书记）", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记和市委常委、副市长", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记和市委常委、常务副市长", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委书记和市委常委、组织部部长", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "市委书记和市委常委、市纪委书记", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委书记和市委常委、政法委书记", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 市长 with deputies
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长和常务副市长", "overlap_org": "安庆市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长和副市长（市委常委）", "overlap_org": "安庆市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "市长和副市长、秘书长", "overlap_org": "安庆市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "市长和副市长", "overlap_org": "安庆市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "市长和副市长", "overlap_org": "安庆市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "市长和市政府党组成员、经开区党工委书记", "overlap_org": "安庆市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # Cross-county connection: 刘婉贞 (桐城市委书记) with 廖强 (宿松县委书记)
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "同为安庆市委班子成员，分别兼任宿松县委书记和桐城市委书记", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # 刘婉贞 link with 张君毅
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "市长和市委常委、桐城市委书记", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 关家涛 (政法委/公安) with 吴宏波 (纪委) - discipline and legal system connection
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "市纪委书记和政法委书记，同为市委班子成员", "overlap_org": "中共安庆市委", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # 徐雄 (常务副市长) with 唐厚明 (副市长/秘书长)
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "常务副市长和副市长（秘书长）共事", "overlap_org": "安庆市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 人大/政协 leaders with top leadership
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "市委书记和市人大常委会主任", "overlap_org": "安庆市", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "市委书记和市政协主席", "overlap_org": "安庆市", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # Predecessor-successor chains
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor", "context": "孟景伟接替张祥安任安庆市委书记", "overlap_org": "中共安庆市委", "overlap_period": "2025", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 17, "person_b": 19, "type": "predecessor_successor", "context": "张祥安接替魏晓明任安庆市委书记", "overlap_org": "中共安庆市委", "overlap_period": "2021", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 19, "person_b": 20, "type": "predecessor_successor", "context": "魏晓明接替虞爱华任安庆市委书记", "overlap_org": "中共安庆市委", "overlap_period": "2016", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "predecessor_successor", "context": "张君毅接替陈冰冰任安庆市长", "overlap_org": "安庆市人民政府", "overlap_period": "2021", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 18, "person_b": 19, "type": "predecessor_successor", "context": "陈冰冰接替魏晓明任安庆市长", "overlap_org": "安庆市人民政府", "overlap_period": "2016", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 19, "person_b": 20, "type": "predecessor_successor", "context": "魏晓明接替虞爱华任安庆市长", "overlap_org": "安庆市人民政府", "overlap_period": "2013", "strength": "strong", "confidence": "confirmed"},
    # Internal promotion chain: 市长→市委书记
    {"person_a": 19, "person_b": 20, "type": "promotion_chain", "context": "虞爱华市长升任市委书记；魏晓明市长升任市委书记（均为内部晋升）", "overlap_org": "中共安庆市委", "overlap_period": "2013-2016", "strength": "strong", "confidence": "confirmed"},
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
    name = person.get("name", "")
    if "书记" in role and "市委" in role and "副" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "市长" in role and "副" not in role:
        return "50,100,255"  # Blue for Mayor
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
    if "市委书记" in role and "副" not in role:
        return "20.0"
    if "市长" in role and "副" not in role:
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


def is_top_leader(person_id):
    return person_id in (1, 2)


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>安庆市领导班子工作关系网络</description>')
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
    print("  安庆市领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
