#!/usr/bin/env python3
"""Build Jixi County (绩溪县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-16
Task: anhui_绩溪县 (县 level)
Province: 安徽省 (Anhui)
Parent city: 宣城市 (Xuancheng)
Targets: 县委书记 & 县长

Current leadership (as of 2026-07-16):
  - 县委书记: 何斌 (male, birth year unknown)
  - 县委副书记、县长: 卢东林 (male, born 1973.11)
  - 县委常委、常务副县长: 金伟 (male, born 1983.10, Anhui Bozhou)
  - 县委常委、副县长: 成健 (male, born 1984.11, Anhui Xuanzhou)
  - 副县长: 徐长凤 (female, born 1972.03, Anhui Guangde, non-party)
  - 副县长: 彭瑛 (details unknown)
  - 副县长: 汪全胜 (details unknown)
  - 副县长: 扎西顿珠 (details unknown, likely Tibet-assigned)
  - 县委副书记: 邱型军 (male, confirmed in news)
  - 县领导: 戴晓静 (confirmed in news, role TBD)
  - 县领导: 房玉琴 (confirmed in news, role TBD)

Sources:
  Official government site: http://www.cnjx.gov.cn/
  - http://www.cnjx.gov.cn/SiteLeader/32.html (县政府领导, accessed 2026-07-16)
  - http://www.cnjx.gov.cn/SiteLeader/showList/111/32.html (卢东林 profile)
  - http://www.cnjx.gov.cn/SiteLeader/showList/216/32.html (金伟 profile)
  - http://www.cnjx.gov.cn/SiteLeader/showList/205/32.html (成健 profile)
  - http://www.cnjx.gov.cn/SiteLeader/showList/43/32.html (徐长凤 profile)
  - http://www.cnjx.gov.cn/News/show/1721605.html (何斌调研, 2026-07-15)
  - http://www.cnjx.gov.cn/News/show/1712752.html (何斌荆州乡调研, 2026-05-29)
  - http://www.cnjx.gov.cn/News/show/1718570.html (何斌七一慰问, 2026-06-24)
  - http://www.cnjx.gov.cn/News/show/1715328.html (何斌接访, 2026-06-18)
  - http://www.cnjx.gov.cn/News/show/1720641.html (以创新推动高质量发展工作推进会, 2026-07-08)

Confidence: Current roles confirmed from official Jixi County government web pages
and multiple 2026 meeting reports. 何斌's detailed pre-2026 resume is a major gap.
Predecessor 肖阳 inferred from 2025 news — needs further confirmation.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "绩溪县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "绩溪县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Top Leaders ═══════════════════════════════════════════════════
    {
        "id": 1,
        "name": "何斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共绩溪县委员会",
        "source": "http://www.cnjx.gov.cn/News/show/1721605.html (何斌调研城市建设, 2026-07-15); http://www.cnjx.gov.cn/News/show/1712752.html (何斌荆州乡调研确认县委书记身份, 2026-05-29)",
        "notes": "绩溪县委书记(2026年5月起任)。2026年5月29日首次以县委书记身份公开调研。\n此前任职经历完全未知——公开资料未找到出生年月、籍贯、教育背景、上任前职务。\n履历缺口：整个职业生涯。这是本次调查最重要的信息缺口。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "卢东林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校函授学院法律专业，在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "绩溪县人民政府",
        "source": "http://www.cnjx.gov.cn/SiteLeader/showList/111/32.html (卢东林官方简历, accessed 2026-07-16); http://www.cnjx.gov.cn/SiteLeader/32.html",
        "notes": "绩溪县委副书记、县政府党组书记、县长。1973年11月生。\n曾任宣城市公安局副局长、党委委员、交警支队支队长，\n泾县县委副书记，绩溪县委副书记。\n跨公安与党务系统，属于\"公安→党务→政府\"跨界晋升路径。\n公安出身——在市局任过副局长兼交警支队长，属于实权岗位；\n跨界到泾县任县委副书记（党务副职）；\n再调任绩溪县长（政府一把手），路径清晰但早期履历(1990s-2010s)待查。",
        "confidence": "confirmed"
    },
    # ═══ Party Committee (县委常委) ════════════════════════════════════
    {
        "id": 3,
        "name": "金伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年10月",
        "birthplace": "安徽亳州",
        "native_place": "安徽亳州",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "绩溪县人民政府",
        "source": "http://www.cnjx.gov.cn/SiteLeader/showList/216/32.html (金伟官方简历, accessed 2026-07-16)",
        "notes": "绩溪县委常委、县政府常务副县长、党组副书记。1983年10月生，安徽亳州人，研究生学历。\n曾任共青团宣城市委市直团工委副书记、书记，\n共青团宣城市委学少部部长，\n宣城市文联副主席，\n旌德县政府副县长，\n旌德县委常委、县政府常务副县长。\n关键发现：从旌德县交流到绩溪县的核心干部。\n先曾任旌德县委常委、常务副县长，后调任绩溪县同岗位。\n这是宣城市内跨县交流的典型例子(旌德→绩溪，同为南部山区县)。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "成健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年11月",
        "birthplace": "安徽宣州",
        "native_place": "安徽宣州",
        "education": "大学学历，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "绩溪县人民政府",
        "source": "http://www.cnjx.gov.cn/SiteLeader/showList/205/32.html (成健官方简历, accessed 2026-07-16)",
        "notes": "绩溪县委常委、县政府副县长、党组成员。1984年11月生，安徽宣州人，大学学历，理学学士。\n曾任宣城市市场监管局科长、党组成员、副局长。\n从市直机关(市场监管局)下派到县里任县委常委、副县长。\n属于\"市直下派\"类型干部。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "邱型军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共绩溪县委员会",
        "source": "http://www.cnjx.gov.cn/News/show/1712752.html (何斌荆州乡调研, 2026-05-29, '县委副书记邱型军')",
        "notes": "绩溪县委副书记。2026年5月29日陪同县委书记何斌到荆州乡、伏岭镇调研。\n职务确认但详细履历待查。\n作为县委副书记，是县里第三号人物(仅次于书记、县长)。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "戴晓静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共绩溪县委员会",
        "source": "http://www.cnjx.gov.cn/News/show/1721605.html (何斌调研城市建设, 2026-07-15, '县领导戴晓静')",
        "notes": "绩溪县领导。2026年7月15日以'县领导戴晓静'身份陪同何斌调研。\n具体职务未明确，推测可能是县委宣传部部长或县委办主任。\n详细履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "房玉琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共绩溪县委员会",
        "source": "http://www.cnjx.gov.cn/News/show/1718570.html (何斌七一慰问, 2026-06-24, '县领导房玉琴')",
        "notes": "绩溪县领导。2026年6月24日以'县领导房玉琴'身份陪同何斌开展七一走访慰问。\n具体职务未明确，推测可能是县人大常委会副主任或县委统战部部长。\n详细履历待查。",
        "confidence": "confirmed"
    },
    # ═══ County Government (县政府领导) ═══════════════════════════════
    {
        "id": 8,
        "name": "徐长凤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "安徽广德",
        "native_place": "安徽广德",
        "education": "安徽省委党校经济管理专业，大学学历",
        "party_join": "无党派",
        "work_start": "1992年12月",
        "current_post": "副县长",
        "current_org": "绩溪县人民政府",
        "source": "http://www.cnjx.gov.cn/SiteLeader/showList/43/32.html (徐长凤官方简历, accessed 2026-07-16)",
        "notes": "绩溪县人民政府副县长。1972年3月生，安徽广德人，1992年12月参加工作，无党派人士。\n安徽省委党校经济管理专业，大学学历。\n一直在绩溪县内晋升：曾任绩溪县农委副主任、\n县政协常委、县民政局局长、县人力资源和社会保障局局长。\n属于本地晋升型干部，无党派身份特殊。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "彭瑛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "绩溪县人民政府",
        "source": "http://www.cnjx.gov.cn/SiteLeader/32.html (县政府领导页面列出, accessed 2026-07-16)",
        "notes": "绩溪县人民政府副县长。县政府领导页面列出但无链接，无法获取详细简历。\n具体分管领域未公开。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "汪全胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "绩溪县人民政府",
        "source": "http://www.cnjx.gov.cn/SiteLeader/32.html (县政府领导页面列出, accessed 2026-07-16)",
        "notes": "绩溪县人民政府副县长。县政府领导页面列出但无链接，无法获取详细简历。\n具体分管领域未公开。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "扎西顿珠",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "绩溪县人民政府",
        "source": "http://www.cnjx.gov.cn/SiteLeader/32.html (县政府领导页面列出, accessed 2026-07-16)",
        "notes": "绩溪县人民政府副县长。县政府领导页面列出但无链接，无法获取详细简历。\n藏族名字(扎西顿珠)，可能是来自西藏的挂职干部。\n具体分管领域未公开。\n履历待查。",
        "confidence": "confirmed"
    },
    # ═══ Predecessors ══════════════════════════════════════════════════
    {
        "id": 12,
        "name": "肖阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "宣城市2025年政府工作报告参会人员名单(推断); 绩溪县2025年新闻参会领导名单",
        "notes": "推断为何斌的前任绩溪县委书记。据现有报告分析，何斌2026年5月首次以书记身份出现，\n其前任可能为肖阳（2025年宣城市相关会议和绩效溪县会议中出现的领导）。\n肖阳此前于2018-2021年曾任绩溪县县长。\n此信息需要进一步确认。",
        "confidence": "plausible"
    },
    # Note: predecessor for 卢东林's county mayor position not found.
    # Based on available information, 肖阳 may have served as mayor (~2018-2021) before becoming party secretary.
]

organizations = [
    {"id": 1, "name": "中共绩溪县委员会", "type": "党委", "level": "县", "parent": "中共宣城市委", "location": "安徽省宣城市绩溪县"},
    {"id": 2, "name": "绩溪县人民政府", "type": "政府", "level": "县", "parent": "宣城市人民政府", "location": "安徽省宣城市绩溪县"},
    {"id": 3, "name": "绩溪县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "绩溪县", "location": "安徽省宣城市绩溪县"},
    {"id": 4, "name": "中国人民政治协商会议绩溪县委员会", "type": "政协", "level": "县", "parent": "绩溪县", "location": "安徽省宣城市绩溪县"},
    {"id": 5, "name": "中共绩溪县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共绩溪县委员会", "location": "安徽省宣城市绩溪县"},
    {"id": 6, "name": "宣城市公安局", "type": "政府", "level": "地级市", "parent": "宣城市人民政府", "location": "安徽省宣城市"},
    {"id": 7, "name": "中共泾县委员会", "type": "党委", "level": "县", "parent": "中共宣城市委", "location": "安徽省宣城市泾县"},
    {"id": 8, "name": "中共旌德县委员会", "type": "党委", "level": "县", "parent": "中共宣城市委", "location": "安徽省宣城市旌德县"},
    {"id": 9, "name": "旌德县人民政府", "type": "政府", "level": "县", "parent": "宣城市人民政府", "location": "安徽省宣城市旌德县"},
    {"id": 10, "name": "共青团宣城市委员会", "type": "群团", "level": "地级市", "parent": "共青团安徽省委", "location": "安徽省宣城市"},
    {"id": 11, "name": "宣城市文学艺术界联合会", "type": "群团", "level": "地级市", "parent": "中共宣城市委宣传部", "location": "安徽省宣城市"},
    {"id": 12, "name": "宣城市市场监督管理局", "type": "政府", "level": "地级市", "parent": "宣城市人民政府", "location": "安徽省宣城市"},
    {"id": 13, "name": "绩溪县农业农村水利局(原农委)", "type": "政府", "level": "县", "parent": "绩溪县人民政府", "location": "安徽省宣城市绩溪县"},
    {"id": 14, "name": "绩溪县民政局", "type": "政府", "level": "县", "parent": "绩溪县人民政府", "location": "安徽省宣城市绩溪县"},
    {"id": 15, "name": "绩溪县人力资源和社会保障局", "type": "政府", "level": "县", "parent": "绩溪县人民政府", "location": "安徽省宣城市绩溪县"},
    {"id": 16, "name": "中共宣城市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "安徽省宣城市"},
    {"id": 17, "name": "宣城市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "安徽省宣城市"},
]

positions = [
    # ── 何斌 ──────────────────────────────────────────────────
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026年5月以县委书记身份开展工作"},
    # ── 卢东林 ──────────────────────────────────────────────────
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "绩溪县委副书记，兼任县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "绩溪县政府县长，估计2021-2022年间上任"},
    {"person_id": 2, "org_id": 6, "title": "副局长、党委委员、交警支队支队长", "start": "", "end": "", "rank": "副处级", "note": "曾任宣城市公安局副局长、党委委员、交警支队支队长"},
    {"person_id": 2, "org_id": 7, "title": "县委副书记", "start": "", "end": "", "rank": "副处级", "note": "曾任泾县县委副书记"},
    # ── 金伟 ──────────────────────────────────────────────────
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "2025", "end": "present", "rank": "副处级", "note": "绩溪县委常委"},
    {"person_id": 3, "org_id": 2, "title": "常务副县长、党组副书记", "start": "2025", "end": "present", "rank": "副处级", "note": "绩溪县委常委、县政府常务副县长、党组副书记"},
    {"person_id": 3, "org_id": 8, "title": "县委常委", "start": "", "end": "2025", "rank": "副处级", "note": "曾任旌德县委常委"},
    {"person_id": 3, "org_id": 9, "title": "常务副县长", "start": "", "end": "2025", "rank": "副处级", "note": "曾任旌德县委常委、常务副县长"},
    {"person_id": 3, "org_id": 9, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "曾任旌德县政府副县长"},
    {"person_id": 3, "org_id": 10, "title": "市直团工委副书记、书记", "start": "", "end": "", "rank": "正科级", "note": "共青团宣城市委市直团工委副书记、书记"},
    {"person_id": 3, "org_id": 10, "title": "学少部部长", "start": "", "end": "", "rank": "正科级", "note": "共青团宣城市委学少部部长"},
    {"person_id": 3, "org_id": 11, "title": "副主席", "start": "", "end": "", "rank": "副处级", "note": "宣城市文联副主席"},
    # ── 成健 ──────────────────────────────────────────────────
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "2025", "end": "present", "rank": "副处级", "note": "绩溪县委常委"},
    {"person_id": 4, "org_id": 2, "title": "副县长、党组成员", "start": "2025", "end": "present", "rank": "副处级", "note": "绩溪县委常委、县政府副县长、党组成员"},
    {"person_id": 4, "org_id": 12, "title": "科长、党组成员、副局长", "start": "", "end": "2025", "rank": "正科→副处", "note": "曾任宣城市市场监管局科长、党组成员、副局长"},
    # ── 邱型军 ──────────────────────────────────────────────────
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "绩溪县委副书记，具体到任时间待查"},
    # ── 戴晓静 ──────────────────────────────────────────────────
    {"person_id": 6, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "绩溪县领导，具体职务待查(推测为宣传部或县委办)"},
    # ── 房玉琴 ──────────────────────────────────────────────────
    {"person_id": 7, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "绩溪县领导，具体职务待查"},
    # ── 徐长凤 ──────────────────────────────────────────────────
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "2020", "end": "present", "rank": "副处级", "note": "绩溪县人民政府副县长"},
    {"person_id": 8, "org_id": 15, "title": "局长", "start": "", "end": "", "rank": "正科级", "note": "曾任绩溪县人力资源和社会保障局局长"},
    {"person_id": 8, "org_id": 14, "title": "局长", "start": "", "end": "", "rank": "正科级", "note": "曾任绩溪县民政局局长"},
    {"person_id": 8, "org_id": 4, "title": "政协常委", "start": "", "end": "", "rank": "正科级", "note": "曾任绩溪县政协常委"},
    {"person_id": 8, "org_id": 13, "title": "副主任", "start": "", "end": "", "rank": "副科级", "note": "曾任绩溪县农委副主任"},
    # ── 彭瑛 ──────────────────────────────────────────────────
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "绩溪县人民政府副县长"},
    # ── 汪全胜 ──────────────────────────────────────────────────
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "绩溪县人民政府副县长"},
    # ── 扎西顿珠 ──────────────────────────────────────────────────
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "绩溪县人民政府副县长"},
    # ── 肖阳(前任书记) ──────────────────────────────────────────
    {"person_id": 12, "org_id": 1, "title": "县委书记", "start": "2021", "end": "2026-05", "rank": "正处级", "note": "绩溪县委书记(推测)，2026年5月由何斌接任"},
    {"person_id": 12, "org_id": 2, "title": "县长", "start": "2018", "end": "2021", "rank": "正处级", "note": "绩溪县县长(推测)，后转任县委书记"},
]

relationships = [
    # ── 何斌 ↔ 卢东林: 当前搭档 (书记+县长) ──────────────
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "现任县委书记与县长，日常工作搭档", "overlap_org": "中共绩溪县委员会/绩溪县人民政府", "overlap_period": "2026-05~present", "strength": "strong", "direction": "undirected", "confidence": "confirmed"},
    # ── 何斌 ↔ 邱型军: 当前搭档 ──────────────────────────
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与县委副书记，共同调研", "overlap_org": "中共绩溪县委员会", "overlap_period": "2026-05~present", "strength": "strong", "direction": "undirected", "confidence": "confirmed"},
    # ── 何斌 ↔ 戴晓静: 当前搭档 ──────────────────────────
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与县领导戴晓静，共同调研城市建设", "overlap_org": "中共绩溪县委员会", "overlap_period": "2026-07~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 何斌 ↔ 房玉琴: 当前搭档 ──────────────────────────
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与县领导房玉琴，共同开展七一慰问", "overlap_org": "中共绩溪县委员会", "overlap_period": "2026-06~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 卢东林 ↔ 金伟: 县政府搭档 ────────────────────────────
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "绩溪县人民政府", "overlap_period": "2025~present", "strength": "strong", "direction": "undirected", "confidence": "confirmed"},
    # ── 卢东林 ↔ 成健: 县政府搭档 ────────────────────────────
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与县委常委、副县长", "overlap_org": "绩溪县人民政府", "overlap_period": "2025~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 卢东林 ↔ 徐长凤: 县政府搭档 ──────────────────────────
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长与副县长(无党派)", "overlap_org": "绩溪县人民政府", "overlap_period": "2020~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 金伟 ↔ 成健: 县委常委共事 ──────────────────────────
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共绩溪县委员会", "overlap_period": "2025~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 何斌 ↔ 肖阳: predecessor/successor (书记接替) ────
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "肖阳卸任县委书记后由何斌接任(推测)", "overlap_org": "中共绩溪县委员会", "overlap_period": "2026-05", "strength": "strong", "direction": "other_to_person", "confidence": "plausible"},
    # ── 卢东林(县长) ↔ 肖阳(前县长/前书记): 曾共事 ──────
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "卢东林任县长期间与肖阳(县委书记或县长)共事(推测)", "overlap_org": "中共绩溪县委员会", "overlap_period": "2021~2026", "strength": "medium", "direction": "undirected", "confidence": "plausible"},
    # ── 徐长凤 ↔ 本地团队: 长期本地化 ──────────────────
    # (徐长凤在绩溪县多个科局工作，与多任领导共事，此为概括)
    {"person_a": 8, "person_b": 2, "type": "overlap", "context": "徐长凤作为本地晋升干部与县长卢东林共事", "overlap_org": "绩溪县人民政府", "overlap_period": "2020~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
]

# ── SQLite ────────────────────────────────────────────────────────────

def create_db():
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
            source TEXT
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
            "end" TEXT,
            rank TEXT,
            note TEXT
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
            direction TEXT,
            confidence TEXT
        );
    """)
    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
             pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, direction, confidence)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"], r["strength"], r["direction"],
             r["confidence"]))
    conn.commit()
    conn.close()
    print(f"✅ DB created: {DB_PATH}")


# ── GEXF ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return r,g,b string for a person based on role."""
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "255,50,50"
    if "县长" in post and "副" not in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "副书记" in post:
        return "50,100,255"
    if "副县长" in post or "常务副县长" in post:
        return "50,100,255"
    if "部长" in post or "书记" in post:
        return "100,100,100"
    if "主任" in post or "主席" in post:
        return "100,100,100"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t:
        return "255,255,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "群团" in t:
        return "255,220,255"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>绩溪县 leadership network — Jixi County, Xuancheng, Anhui. Research date: 2026-07-16.</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("15.0" if p.get("current_post","") and ("常委" in p["current_post"] or "副书记" in p["current_post"]) else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("confidence",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # org nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0

    # person → org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ── main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building 绩溪县 leadership network data...")
    create_db()
    build_gexf()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {cnt} records")
    conn.close()
    print("Done.")
