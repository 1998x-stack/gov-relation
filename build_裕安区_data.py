#!/usr/bin/env python3
"""Build Yu'an District (裕安区) leadership network database and GEXF graph.

Targets: 区委书记董永来, 区长李守成
Research date: 2026-07-15
Sources:
  - www.yuan.gov.cn (official district government website)
  - 领导之窗 page: https://www.yuan.gov.cn/ldzc/index.html
  - 裕安区第六届委员会第一次全体会议 (2026-06-24)
  - 裕安区防汛防台风工作调度会议 (2026-07-06)
  - 裕安区政府第102次常务会议 (2026-07-11)
  - 裕安区"两优一先"表彰大会 (2026-06-30)

Confidence: Current roles confirmed from official government website.
  All leadership information sourced from official 裕安区人民政府 website.
  District committee composition confirmed from the 6th committee first plenary session (2026-06-24).
  Biographical details for some leaders incomplete - career histories beyond current role pending.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "裕安区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "裕安区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # === 1. Party Secretary (区委书记) ===
    {
        "id": 1,
        "name": "董永来",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共六安市裕安区委员会",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26555896.html (裕安区第六届委员会第一次全体会议 2026-06-24, 选举为区委书记); https://www.yuan.gov.cn/zwzx/yayw/26562143.html (2026-07-07, 主持防汛防台风调度会); https://www.yuan.gov.cn/zwzx/yayw/26557315.html (2026-06-30, 讲授专题党课)",
        "notes": "董永来，现任中共六安市裕安区委书记。2026年6月24日当选裕安区第六届区委书记。主持区委全面工作。频繁调研党建、防汛、信访等工作。",
        "confidence": "confirmed"
    },
    # === 2. District Mayor (区长) ===
    {
        "id": 2,
        "name": "李守成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/ldzc/index.html (领导之窗 区长信息, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委副书记); https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 主持第102次常务会议)",
        "notes": "李守成，男，汉族，1975年2月出生，大学学历，中共党员。现任裕安区委副书记、区长。领导区政府全面工作，负责审计工作，分管审计局。联系高新区工作。",
        "confidence": "confirmed"
    },
    # === 3. Deputy Party Secretary (区委副书记) ===
    {
        "id": 3,
        "name": "郭明保",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共六安市裕安区委员会",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委副书记); https://www.yuan.gov.cn/zwzx/yayw/26557315.html (2026-07-01, 宣读表彰决定)",
        "notes": "郭明保，裕安区委副书记。2026年6月24日当选区委副书记。",
        "confidence": "confirmed"
    },
    # === 4. Standing Committee Members ===
    {
        "id": 4,
        "name": "马克文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区人武部政委",
        "current_org": "裕安区人民武装部",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委); https://www.yuan.gov.cn/zwzx/yayw/26562143.html (2026-07-07, 出席防汛调度会)",
        "notes": "马克文，区委常委、区人武部政委。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "郑敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共六安市裕安区委员会",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委)",
        "notes": "郑敏，裕安区委常委。具体职务待查。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "王康维",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共六安市裕安区委员会",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委)",
        "notes": "王康维，裕安区委常委。具体职务待查。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "任其平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-01",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=717&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委)",
        "notes": "任其平，男，汉族，1985年1月生，研究生学历，中共党员。主管招商引资工作。负责工业和信息化、民营经济、人力资源和社会保障、文化和旅游、广播电视、生态环境、工业企业改制、金融服务、通信方面工作。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "储著时",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共六安市裕安区委员会组织部",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26564719.html (2026-07-10, 出席区直机关党建会议); https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委)",
        "notes": "储著时，裕安区委常委、组织部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "卢俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共六安市裕安区委员会宣传部",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 列席区政府第102次常务会议); https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委)",
        "notes": "卢俊，裕安区委常委、宣传部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "熊茂林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-05",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长、区政府党组副书记",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=778&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委); https://www.yuan.gov.cn/zwzx/yayw/26562143.html (2026-07-07, 传达会议精神)",
        "notes": "熊茂林，男，汉族，1986年5月生，大学学历，中共党员。负责区政府常务工作，分管发展改革、财政、税务、统计、应急管理、自然资源、规划、营商环境等工作。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "徐尚国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共六安市裕安区委员会",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委)",
        "notes": "徐尚国，裕安区委常委。具体职务待查。",
        "confidence": "confirmed"
    },
    # === 12. Deputy District Mayor (挂职) ===
    {
        "id": 12,
        "name": "郑少游",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长（挂职）",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=785&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 出席区政府常务会议); https://www.yuan.gov.cn/zwzx/yayw/26555896.html (2026-06-24, 当选区委常委)",
        "notes": "郑少游，区委常委、副区长（挂职）。具体分工待查。",
        "confidence": "confirmed"
    },
    # === 13. Deputy District Mayor ===
    {
        "id": 13,
        "name": "王娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "安徽寿县",
        "native_place": "",
        "education": "大学学历",
        "party_join": "九三学社社员",
        "work_start": "2006-10",
        "current_post": "副区长",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=768&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 出席区政府常务会议)",
        "notes": "王娟，女，汉族，寿县人，1982年6月出生，2006年10月参加工作，九三学社社员，大学学历。负责商务、市场监督管理、食品安全、供销等工作。",
        "confidence": "confirmed"
    },
    # === 14. Deputy Mayor / Public Security ===
    {
        "id": 14,
        "name": "陈劲松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、副区长，六安市公安局裕安分局党委书记、局长",
        "current_org": "六安市公安局裕安分局",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=777&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 出席区政府常务会议)",
        "notes": "陈劲松，区政府党组成员、副区长，六安市公安局裕安分局党委书记、局长、三级高级警长。负责公安、信访、司法等方面工作。",
        "confidence": "confirmed"
    },
    # === 15. Deputy Mayor (Agriculture) ===
    {
        "id": 15,
        "name": "魏天虹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-03",
        "birthplace": "",
        "native_place": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=789&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 出席区政府常务会议)",
        "notes": "魏天虹，男，汉族，1981年3月生，本科学历，中共党员。负责农业农村、乡村振兴、水利、气象方面工作。",
        "confidence": "confirmed"
    },
    # === 16. Deputy Mayor (Construction) ===
    {
        "id": 16,
        "name": "程刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-07",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "2008-08",
        "current_post": "区政府党组成员、副区长",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=791&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 出席区政府常务会议)",
        "notes": "程刚，男，汉族，1986年7月出生，大学本科学历，2008年8月参加工作，中共党员。负责住房城乡建设、交通运输、城市管理、征迁安置等工作。",
        "confidence": "confirmed"
    },
    # === 17. Deputy Mayor (Civil Affairs) ===
    {
        "id": 17,
        "name": "姜峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-08",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "裕安区人民政府",
        "source": "https://www.yuan.gov.cn/content/column/6788101?liId=802&tid=21 (领导之窗, accessed 2026-07-15); https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 以副区长人选出席会议)",
        "notes": "姜峰，男，汉族，1981年8月生，大学本科学历，中共党员。负责民政、残疾人事业等方面工作。",
        "confidence": "confirmed"
    },
    # === 18. NPC Director (人大) ===
    {
        "id": 18,
        "name": "王雷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "裕安区人民代表大会常务委员会",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26563528.html (2026-07-09, 主持召开第一招商攻坚组工作推进会); https://www.yuan.gov.cn/zwzx/yayw/26557315.html (2026-07-01, 出席表彰大会)",
        "notes": "王雷，裕安区人大常委会主任。",
        "confidence": "confirmed"
    },
    # === 19. CPPCC Deputy Chair (政协) ===
    {
        "id": 19,
        "name": "魏璇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "裕安区政协",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26566785.html (2026-07-14, 列席区政府第102次常务会议)",
        "notes": "魏璇，裕安区政协副主席。",
        "confidence": "confirmed"
    },
    # === 20. Deputy NPC Director ===
    {
        "id": 20,
        "name": "赵德军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导（区人大常委会/政协）",
        "current_org": "裕安区",
        "source": "https://www.yuan.gov.cn/zwzx/yayw/26557315.html (2026-07-01, 出席表彰大会); https://www.yuan.gov.cn/zwzx/yayw/26550312.html (2026-06-18, 出席区委五届十四次全会)",
        "notes": "赵德军，裕安区领导。从报道中出现在区几大班子领导中，具体职务待确认。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共六安市裕安区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共六安市委员会",
        "location": "六安市裕安区"
    },
    {
        "id": 2,
        "name": "裕安区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "六安市人民政府",
        "location": "六安市裕安区"
    },
    {
        "id": 3,
        "name": "裕安区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "六安市人民代表大会常务委员会",
        "location": "六安市裕安区"
    },
    {
        "id": 4,
        "name": "裕安区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "政协六安市委员会",
        "location": "六安市裕安区"
    },
    {
        "id": 5,
        "name": "中共六安市裕安区委员会组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共六安市裕安区委员会",
        "location": "六安市裕安区"
    },
    {
        "id": 6,
        "name": "中共六安市裕安区委员会宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共六安市裕安区委员会",
        "location": "六安市裕安区"
    },
    {
        "id": 7,
        "name": "裕安区人民武装部",
        "type": "党委",
        "level": "县处级",
        "parent": "六安军分区",
        "location": "六安市裕安区"
    },
    {
        "id": 8,
        "name": "六安市公安局裕安分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "六安市公安局",
        "location": "六安市裕安区"
    },
]

# positions: (person_id, org_id, title, start, end, rank, note)
positions = [
    # Top leaders
    (1, 1, "区委书记", "2026-06", "present", "正处级", "2026年6月24日当选第六届区委书记"),
    (2, 1, "区委副书记", "2026-06", "present", "正处级", "2026年6月24日当选区委副书记"),
    (2, 2, "区长", "", "present", "正处级", "区政府全面工作，负责审计"),
    (3, 1, "区委副书记", "2026-06", "present", "正处级", "2026年6月24日当选区委副书记"),

    # Standing Committee members
    (4, 7, "区委常委、区人武部政委", "", "present", "正处级", ""),
    (5, 1, "区委常委", "", "present", "副处级", ""),
    (6, 1, "区委常委", "", "present", "副处级", ""),
    (7, 1, "区委常委", "2026-06", "present", "副处级", "2026年6月24日当选区委常委"),
    (7, 2, "副区长", "", "present", "副处级", "主管招商引资、工信、文旅等"),
    (8, 5, "区委常委、组织部部长", "", "present", "副处级", ""),
    (9, 6, "区委常委、宣传部部长", "", "present", "副处级", ""),
    (10, 1, "区委常委", "2026-06", "present", "副处级", "2026年6月24日当选区委常委"),
    (10, 2, "常务副区长", "", "present", "副处级", "区政府常务工作"),
    (11, 1, "区委常委", "", "present", "副处级", ""),

    # Deputy Mayors
    (12, 2, "副区长（挂职）", "", "present", "副处级", "挂职"),
    (13, 2, "副区长", "", "present", "副处级", "商务、市场监管、供销"),
    (14, 8, "公安分局局长", "", "present", "副处级", ""),
    (14, 2, "副区长", "", "present", "副处级", "公安、信访、司法"),
    (15, 2, "副区长", "", "present", "副处级", "农业农村、乡村振兴、水利"),
    (16, 2, "副区长", "", "present", "副处级", "住建、交通、城管"),
    (17, 2, "副区长", "", "present", "副处级", "民政、残疾人事业"),

    # NPC
    (18, 3, "区人大常委会主任", "", "present", "正处级", ""),

    # CPPCC
    (19, 4, "区政协副主席", "", "present", "副处级", ""),

    # Other
    (20, 3, "区领导", "", "present", "待确认", ""),
]

# relationships: (person_a, person_b, type, context, overlap_org, overlap_period, strength)
relationships = [
    # 书记 - 区长
    (1, 2, "overlap", "书记与区长搭档，共同主持区委区政府工作", "中共六安市裕安区委员会", "2026-", "strong"),
    # 书记 - 副书记
    (1, 3, "overlap", "书记与副书记搭档", "中共六安市裕安区委员会", "2026-", "strong"),
    # 区长 - 常务副区长
    (2, 10, "overlap", "区长与常务副区长工作搭档", "裕安区人民政府", "2026-", "strong"),
    # 书记 - 各常委（在区委常委会中共事）
    (1, 4, "overlap", "区委常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    (1, 5, "overlap", "区委常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    (1, 6, "overlap", "区委常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    (1, 7, "overlap", "区委常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    (1, 8, "overlap", "书记与组织部部长在常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    (1, 9, "overlap", "书记与宣传部部长在常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    (1, 10, "overlap", "书记与常务副区长在常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    (1, 11, "overlap", "区委常委会中共事", "中共六安市裕安区委员会", "2026-", "medium"),
    # 区政府班子成员之间
    (2, 12, "overlap", "区政府班子", "裕安区人民政府", "2026-", "medium"),
    (2, 13, "overlap", "区政府班子", "裕安区人民政府", "2026-", "medium"),
    (2, 14, "overlap", "区政府班子", "裕安区人民政府", "2026-", "medium"),
    (2, 15, "overlap", "区政府班子", "裕安区人民政府", "2026-", "medium"),
    (2, 16, "overlap", "区政府班子", "裕安区人民政府", "2026-", "medium"),
    (2, 17, "overlap", "区政府班子", "裕安区人民政府", "2026-", "medium"),
    # 人大主任 - 区领导
    (18, 1, "overlap", "人大主任与区委书记在全区工作中配合", "裕安区", "2026-", "medium"),
    # 常委中副区长之间
    (7, 10, "overlap", "同为区委常委、副区长", "裕安区人民政府", "2026-", "medium"),
    (7, 12, "overlap", "同为副区长", "裕安区人民政府", "2026-", "medium"),
    (10, 12, "overlap", "同为副区长", "裕安区人民政府", "2026-", "medium"),
]


# ── build database ──────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON;")

# Drop existing tables (clean build)
cur.execute("DROP TABLE IF EXISTS relationships;")
cur.execute("DROP TABLE IF EXISTS positions;")
cur.execute("DROP TABLE IF EXISTS organizations;")
cur.execute("DROP TABLE IF EXISTS persons;")

cur.execute("""
    CREATE TABLE persons (
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
        source TEXT,
        notes TEXT,
        confidence TEXT DEFAULT 'confirmed'
    );
""")

cur.execute("""
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );
""")

cur.execute("""
    CREATE TABLE positions (
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
    );
""")

cur.execute("""
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER,
        person_b INTEGER,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        strength TEXT DEFAULT 'medium',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute("""
        INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                             education, party_join, work_start, current_post, current_org,
                             source, notes, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
          p["birthplace"], p["native_place"], p["education"],
          p["party_join"], p["work_start"],
          p["current_post"], p["current_org"],
          p["source"], p["notes"], p["confidence"]))

for o in organizations:
    cur.execute("""
        INSERT INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    pid, oid, title, start, end, rank, note = pos
    cur.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pid, oid, title, start, end, rank, note))

for r in relationships:
    pa, pb, rtype, ctx, oorg, operiod, strength = r
    cur.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pa, pb, rtype, ctx, oorg, operiod, strength))

conn.commit()
conn.close()

print(f"✅ Database created: {DB_PATH}")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")

# ── build GEXF graph ────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role."""
    post = p["current_post"]
    if "书记" in post and "副书记" not in post:
        return "255,50,50"  # Red - Party Secretary
    if "区长" in post:
        return "50,100,255"  # Blue - Mayor
    if "副区长" in post or "常务" in post:
        return "50,100,255"  # Blue - Deputy Mayor
    if "人大" in post:
        return "200,255,255"  # Cyan - NPC
    if "政协" in post:
        return "255,240,200"  # Cream - CPPCC
    if "部长" in post:
        return "100,150,255"  # Blue - Department head
    if "副书记" in post:
        return "255,100,100"  # Light Red - Deputy Secretary
    return "100,100,100"  # Grey - Others

def person_size(p):
    """Size by importance."""
    post = p["current_post"]
    if "书记" in post and "副书记" not in post:
        return "20.0"
    if "区长" in post and "副" not in post:
        return "20.0"
    return "12.0"

def org_color(o):
    """Color by org type."""
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>裕安区领导班子工作关系网络 - 六安市裕安区</description>')
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

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = person_size(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges: person→organization (worked_at)
lines.append('    <edges>')
eid = 0
for pos in positions:
    pid, oid, title, start, end, rank, note = pos
    lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(start)}-{esc(end)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

# Edges: person↔person (relationship)
for r in relationships:
    pa, pb, rtype, ctx, oorg, operiod, strength = r
    weight = "2.0" if strength == "strong" else "1.5" if strength == "medium" else "1.0"
    lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{weight}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(operiod)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF graph created: {GEXF_PATH}")
print(f"   Person nodes: {len(persons)}")
print(f"   Organization nodes: {len(organizations)}")
print(f"   Person→Org edges: {len(positions)}")
print(f"   Person↔Person edges: {len(relationships)}")
print(f"   Total edges: {len(positions) + len(relationships)}")
print("")
print("Summary:")
print(f"  Top leaders: 董永来（区委书记）, 李守成（区长）")
print(f"  Standing Committee: {sum(1 for p in persons if '常委' in p['current_post'])} members")
print(f"  Government team: {sum(1 for p in persons if '副区长' in p['current_post'])} deputy mayors")
print(f"  Research as of: {TODAY}")
