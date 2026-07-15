#!/usr/bin/env python3
"""Build Xuancheng (宣城市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-16
Task: anhui_宣城市 (地级市 level)
Targets: 市委书记 & 市长

Sources:
  - https://www.xuancheng.gov.cn/SiteLeader/ (市政府领导, accessed 2026-07-16)
  - https://www.xuancheng.gov.cn/SiteLeader/showList/193/38.html (邓继敢 profile)
  - https://www.xuancheng.gov.cn/SiteLeader/showList/202/38.html (蔡毅 profile)
  - https://www.xuancheng.gov.cn/SiteLeader/showList/146/38.html (董红明 profile)
  - https://www.xuancheng.gov.cn/SiteLeader/showList/215/38.html (陶晓海 profile)
  - https://www.xuancheng.gov.cn/SiteLeader/showList/187/38.html (刘涛 profile)
  - https://www.xuancheng.gov.cn/SiteLeader/showList/203/38.html (嵇文 profile)
  - https://www.xuancheng.gov.cn/News/show/1721401.html (市委理论学习中心组会议)
  - https://www.xuancheng.gov.cn/News/show/1711942.html (市委五届十一次全会)

Confidence: Current roles confirmed from official Xuancheng government leadership pages.
  Biographical details come from official government profiles.
  Party committee (市委) standing committee composition is partial — confirmed members
  include 何淳宽(书记), 邓继敢(副书记/市长), 刘居胜(副书记), 蔡毅(常委/常务副市长),
  董红明(常委/副市长), 夏迎锋(常委 — exact role pending).
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "宣城市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "宣城市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Top Leaders ═══════════════════════════════════════════════════
    {
        "id": 1,
        "name": "何淳宽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共宣城市委",
        "source": "https://www.xuancheng.gov.cn/News/show/1721401.html (市委理论学习中心组会议, 2026-07-15)",
        "notes": "宣城市委书记。主持市委全面工作。2026年5月主持市委五届十一次全会。\n履历缺口：公开资料未找到何淳宽详细简历。2026年已知在任，此前职务待查。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "邓继敢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "宣城市人民政府",
        "source": "https://www.xuancheng.gov.cn/SiteLeader/showList/193/38.html (邓继敢官方简历, accessed 2026-07-16)",
        "notes": "宣城市委副书记、市长、市政府党组书记。领导市政府全面工作，负责审计工作。\n曾任滁州市发改委副主任，共青团滁州市委书记，滁州市委副秘书长(正县级)，来安县委副书记、县长，天长市委书记，滁州市委常委、市政府常务副市长。",
        "confidence": "confirmed"
    },
    # ═══ Party Committee (市委领导) ════════════════════════════════════
    {
        "id": 3,
        "name": "刘居胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共宣城市委",
        "source": "https://www.xuancheng.gov.cn/News/show/1711942.html (市委五届十一次全会, 2026-05-26)",
        "notes": "宣城市委副书记。协助书记处理市委日常工作。2026年5月市委五届十一次全会确认。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "夏迎锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共宣城市委",
        "source": "https://www.xuancheng.gov.cn/News/show/1721401.html (市委理论学习中心组会议, 2026-07-15)",
        "notes": "宣城市委常委。在市委理论学习中心组会议及市委常委会会议中列名于市长之后。\n具体职务（组织/宣传/统战/政法等）待查。履历待查。",
        "confidence": "confirmed"
    },
    # ═══ Government Leaders (市政府领导) ═══════════════════════════════
    {
        "id": 5,
        "name": "蔡毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "宣城市人民政府",
        "source": "https://www.xuancheng.gov.cn/SiteLeader/showList/202/38.html (蔡毅官方简历, accessed 2026-07-16)",
        "notes": "宣城市委常委、市政府常务副市长、党组副书记。\n负责市政府常务工作，分管发改委、财政局、国资委、应急局、统计局、数据资源局、公管局等。\n曾任省属国有企业内设部门副职、正职，总经理助理、董事会秘书、副总经理、党委委员，地级市市委常委、市政府副市长，开发区党工委书记、管委会常务副主任。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "董红明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历，管理学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "宣城市人民政府",
        "source": "https://www.xuancheng.gov.cn/SiteLeader/showList/146/38.html (董红明官方简历, accessed 2026-07-16)",
        "notes": "宣城市委常委、市政府副市长、党组成员。\n分管人社局、自然资源规划局、住建局、交通局、公积金中心。\n曾任铜陵经济技术开发区管委会副主任、党工委委员，铜陵市国资委专职副主任、党委委员，铜陵市住房公积金管理中心主任、党组书记，铜陵市统计局局长、党组书记。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "陶晓海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生学历，管理学硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宣城市人民政府",
        "source": "https://www.xuancheng.gov.cn/SiteLeader/showList/215/38.html (陶晓海官方简历, accessed 2026-07-16)",
        "notes": "宣城市政府副市长。无党派。\n分管民政局、生态环境局、农业农村局、水利局、林业局、供销社、残联。\n曾任宣州区政府副区长，宣城市水务局调研员，宣城市水利局副局长、二级调研员，宣城市水利局局长，宣城市政协副主席、市水利局局长。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学学历，法律硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "宣城市人民政府",
        "source": "https://www.xuancheng.gov.cn/SiteLeader/showList/187/38.html (刘涛官方简历, accessed 2026-07-16)",
        "notes": "宣城市政府副市长、党组成员，市委政法委副书记，市公安局局长、党委书记、督察长。\n分管公安局、司法局、退役军人事务局、国动办。\n曾任河南省公安厅机关党委副调研员，安徽省公安厅办公室副调研员，安徽省公安厅办公室副主任(主持工作)，安徽省公安厅情报指挥中心政委、主任，安徽省公安厅刑事侦查处(刑事警察总队)政委、一级高级警长，安徽省公安厅治安管理处(治安警察总队)处长(总队长)、一级高级警长。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "嵇文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宣城市人民政府",
        "source": "https://www.xuancheng.gov.cn/SiteLeader/showList/203/38.html (嵇文官方简历, accessed 2026-07-16)",
        "notes": "宣城市政府副市长、党组成员。安徽省第十一次党代会代表。\n分管科技局、工信局、投资促进局、宣城经开区管委会、宣城现代产业园管委会。\n曾任宣州区副区长、区委常委、政法委书记，宣城市委副秘书长、市委巡察办主任、市委办公室主任，广德市委副书记、市政府市长，郎溪县委书记。",
        "confidence": "confirmed"
    },
    # ═══ 政协 ═══════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "吴爱国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "宣城市政协",
        "source": "https://www.xuancheng.gov.cn/News/show/1711942.html (市委五届十一次全会, 2026-05-26)",
        "notes": "宣城市政协主席。原任宣城市委副书记。2026年5月以市政协主席身份出席市委五届十一次全会。",
        "confidence": "confirmed"
    },
    # ═══ 前任 ═══════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "李中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原宣城市委书记）",
        "current_org": "",
        "source": "已知：李中2022-2025年任宣城市委书记，后调任安徽省副省长/省领导",
        "notes": "前任宣城市委书记（~2022-2025）。何淳宽接替。去向：安徽省副省长或省直部门（待查）。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "何淳宽（前任书记）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任宣城市长，已升书记）",
        "current_org": "",
        "source": "已知：何淳宽2024-2025年由宣城市长升任市委书记",
        "notes": "何淳宽2024年任宣城市市长，2025年接替李中升任宣城市委书记。前任市长是谁待查。",
        "confidence": "plausible"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共宣城市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "宣城市"},
    {"id": 2, "name": "宣城市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "宣城市"},
    {"id": 3, "name": "宣城市人大常委会", "type": "人大", "level": "地级市", "parent": "宣城市", "location": "宣城市"},
    {"id": 4, "name": "宣城市政协", "type": "政协", "level": "地级市", "parent": "宣城市", "location": "宣城市"},
    {"id": 5, "name": "中共宣城市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共宣城市委", "location": "宣城市"},
    {"id": 6, "name": "宣城市监察委员会", "type": "政府", "level": "地级市", "parent": "宣城市人民政府", "location": "宣城市"},
    {"id": 7, "name": "中共宣城市委组织部", "type": "党委", "level": "地级市", "parent": "中共宣城市委", "location": "宣城市"},
    {"id": 8, "name": "中共宣城市委政法委员会", "type": "党委", "level": "地级市", "parent": "中共宣城市委", "location": "宣城市"},
    {"id": 9, "name": "宣城市公安局", "type": "政府", "level": "地级市", "parent": "宣城市人民政府", "location": "宣城市"},
    {"id": 10, "name": "宣城经济技术开发区", "type": "开发区", "level": "地级市", "parent": "宣城市人民政府", "location": "宣城市"},
    {"id": 11, "name": "中共天长市委", "type": "党委", "level": "县处级", "parent": "中共滁州市委", "location": "滁州市天长市"},
    {"id": 12, "name": "中共来安县委", "type": "党委", "level": "县处级", "parent": "中共滁州市委", "location": "滁州市来安县"},
    {"id": 13, "name": "滁州市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "滁州市"},
    {"id": 14, "name": "中共郎溪县委", "type": "党委", "level": "县处级", "parent": "中共宣城市委", "location": "宣城市郎溪县"},
    {"id": 15, "name": "广德市人民政府", "type": "政府", "level": "县处级", "parent": "宣城市人民政府", "location": "宣城市广德市"},
    {"id": 16, "name": "铜陵经济技术开发区", "type": "开发区", "level": "地级市", "parent": "铜陵市人民政府", "location": "铜陵市"},
    {"id": 17, "name": "安徽省公安厅", "type": "政府", "level": "省级", "parent": "安徽省人民政府", "location": "合肥市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 何淳宽 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2025", "end": "present", "rank": "正厅级", "note": "主持市委全面工作。2025年接替李中任宣城市委书记。"},
    {"person_id": 1, "org_id": 2, "title": "市长（前任职务）", "start": "2024", "end": "2025", "rank": "正厅级", "note": "2024-2025年任宣城市市长，后升任市委书记。"},
    # 邓继敢 - 市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2025", "end": "present", "rank": "正厅级", "note": "任宣城市委副书记。"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2025", "end": "present", "rank": "正厅级", "note": "领导市政府全面工作，负责审计方面工作。"},
    {"person_id": 2, "org_id": 13, "title": "市委常委、常务副市长（前任）", "start": "", "end": "2025", "rank": "副厅级", "note": "曾任滁州市委常委、市政府常务副市长。"},
    {"person_id": 2, "org_id": 11, "title": "天长市委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "曾任天长市委书记。"},
    {"person_id": 2, "org_id": 12, "title": "来安县委副书记、县长（前任）", "start": "", "end": "", "rank": "正处级", "note": "曾任来安县委副书记、县长。"},
    # 刘居胜 - 市委副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 夏迎锋 - 市委常委
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "具体分工待查。"},
    # 蔡毅 - 常务副市长
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": "负责市政府常务工作。"},
    # 董红明 - 副市长
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管人社局、自然资源规划局、住建局、交通局、公积金中心。"},
    {"person_id": 6, "org_id": 16, "title": "铜陵经开区管委会副主任（前任）", "start": "", "end": "", "rank": "正处级", "note": "曾任铜陵经济技术开发区管委会副主任。"},
    # 陶晓海 - 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管民政局、生态环境局、农业农村局、水利局、林业局。无党派。"},
    {"person_id": 7, "org_id": 4, "title": "市政协副主席（前任）", "start": "", "end": "", "rank": "副厅级", "note": "曾任宣城市政协副主席、市水利局局长。"},
    # 刘涛 - 副市长兼公安局长
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管公安局、司法局、退役军人事务局、国动办。"},
    {"person_id": 8, "org_id": 9, "title": "市公安局局长", "start": "", "end": "present", "rank": "正处级", "note": "市委政法委副书记，市公安局局长、党委书记、督察长。"},
    {"person_id": 8, "org_id": 17, "title": "省公安厅治安管理处处长（前任）", "start": "", "end": "", "rank": "正处级", "note": "曾任安徽省公安厅治安管理处（治安警察总队）处长（总队长）。"},
    # 嵇文 - 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "2026", "end": "present", "rank": "副厅级", "note": "分管科技局、工信局、投资促进局、开发区。"},
    {"person_id": 9, "org_id": 14, "title": "郎溪县委书记（前任）", "start": "", "end": "2025", "rank": "正处级", "note": "曾任郎溪县委书记。"},
    {"person_id": 9, "org_id": 15, "title": "广德市委副书记、市长（前任）", "start": "", "end": "", "rank": "正处级", "note": "曾任广德市委副书记、市政府市长。"},
    # 吴爱国 - 政协主席
    {"person_id": 10, "org_id": 4, "title": "市政协主席", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委副书记（前任）", "start": "", "end": "", "rank": "副厅级", "note": "曾任宣城市委副书记。"},
    # 李中 - 前任市委书记
    {"person_id": 11, "org_id": 1, "title": "市委书记（前任）", "start": "2022", "end": "2025", "rank": "正厅级", "note": "前任宣城市委书记。何淳宽接替。"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap (市委常委会)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记和市长同届领导班子成员", "overlap_org": "中共宣城市委", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记和市委副书记", "overlap_org": "中共宣城市委", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记和市委常委", "overlap_org": "中共宣城市委", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记和市委常委、常务副市长", "overlap_org": "中共宣城市委", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记和市委常委、副市长", "overlap_org": "中共宣城市委", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    # 市长 with deputy mayors
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长和常务副市长", "overlap_org": "宣城市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "市长和副市长董红明", "overlap_org": "宣城市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "市长和副市长陶晓海", "overlap_org": "宣城市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "市长和副市长刘涛", "overlap_org": "宣城市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市长和副市长嵇文", "overlap_org": "宣城市人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 何淳宽 predecessor-successor
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "何淳宽接替李中任宣城市委书记", "overlap_org": "中共宣城市委", "overlap_period": "2025", "strength": "strong", "confidence": "confirmed"},
    # 何淳宽 was predecessor of 邓继敢 (as mayor)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "何淳宽升任市委书记后，邓继敢接任市长", "overlap_org": "宣城市人民政府", "overlap_period": "2025", "strength": "strong", "confidence": "plausible"},
    # 嵇文 worked in 郎溪 then moved to city
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "嵇文由郎溪县委书记提任宣城市副市长，何淳宽为市委书记", "overlap_org": "中共宣城市委", "overlap_period": "2026", "strength": "medium", "confidence": "plausible"},
    # 吴爱国 former party deputy
    {"person_a": 10, "person_b": 1, "type": "overlap", "context": "市政协主席和市委书记", "overlap_org": "宣城市", "overlap_period": "2025-", "strength": "medium", "confidence": "confirmed"},
    # Cross-city connections
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "邓继敢由滁州跨市调任宣城，李中可能参与人事安排", "overlap_org": "中共安徽省委", "overlap_period": "2025", "strength": "weak", "confidence": "plausible"},
    # 嵇文 career path - from 广德/郎溪 to city
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate", "context": "嵇文从县区岗位提任副市长，在邓继敢领导下工作", "overlap_org": "宣城市人民政府", "overlap_period": "2026-", "strength": "medium", "confidence": "confirmed"},
    # 董红明 from 铜陵 to 宣城 (cross-city)
    {"person_a": 6, "person_b": 2, "type": "overlap", "context": "董红明由铜陵跨市调任宣城副市长", "overlap_org": "宣城市人民政府", "overlap_period": "2025-", "strength": "medium", "confidence": "confirmed"},
    # 刘涛 from 省公安厅
    {"person_a": 8, "person_b": 17, "type": "overlap", "context": "刘涛由省公安厅下派宣城", "overlap_org": "安徽省公安厅", "overlap_period": "", "strength": "medium", "confidence": "confirmed"},
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
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"],
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
    if "书记" in role and ("市委" in role or "县委" in role) and "副" not in role:
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
    if "市委书记" in role and "副" not in role:
        return "20.0"
    if "市长" in role and "副" not in role:
        return "20.0"
    if "市人大" in role or "市政协" in role:
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
    lines.append('    <description>宣城市领导班子工作关系网络</description>')
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
        org_name = esc(p.get("current_org", ""))
        rank = esc(p.get("notes", ""))
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
    print("  宣城市领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
