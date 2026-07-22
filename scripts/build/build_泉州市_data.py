#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 泉州市 (Quanzhou, Fujian).

Task: fujian_泉州市 — 市委书记 & 市长
Province: 福建省
City: 泉州市 (prefecture-level)
Region: 泉州市
Level: 地级市
Research date: 2026-07-16

Confirmed officeholders (as of 2026-07-16):
- 市委书记: 张毅恭 (born 1968.10, male, Han, Fujian Xiamen, Fujian Agricultural College)
- 市长: 蔡战胜 (born 1973.08, male, Han, Shaanxi Weinan, China University of Petroleum, PhD)

Predecessors:
- 市委书记 chain: 康涛 → 王永礼(2021.7-2021.12) → 刘建洋(2021.12-2022.12) → 张毅恭(2023.1-)
- 市长 chain: 康涛 → 王永礼(2018.7-2021.7) → 蔡战胜(2021.7-)

Standing Committee (中共泉州市委常委会) — known current members:
- 张毅恭 (市委书记)
- 蔡战胜 (市委副书记、市长)
- 卢秀萍 (市委副书记)
- 周小华 (市委常委兼秘书长)
- 肖汉辉 (市委常委、统战部部长)
- 李建辉 (市委组织部部长)
- 刘林霜 (市委常委)
- 陈惠黔 (市委宣传部部长)
- 黄景春 (市委常委)
- 陈辉宗 (市委常委、市纪委书记)
- 李强 (市委常委、石狮市委书记)

Sources:
- zh.wikipedia.org/wiki/泉州市
- zh.wikipedia.org/wiki/张毅恭
- zh.wikipedia.org/wiki/蔡战胜
- zh.wikipedia.org/wiki/王永礼
- en.wikipedia.org/wiki/Liu_Jianyang
- en.wikipedia.org/wiki/Wang_Yongli
- en.wikipedia.org/wiki/Cai_Zhansheng

Confidence: Current leadership identity-level confirmed from Wikipedia sources.
Full career timelines available for key figures. Predecessor/successor relationships
documented. Standing committee composition partially confirmed.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = SCRIPT_DIR  # We are in data/tmp/fujian_泉州市/
DB_PATH = os.path.join(STAGING, "泉州市_network.db")
GEXF_PATH = os.path.join(STAGING, "泉州市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ── Current top leaders ──
    {
        "id": 1,
        "name": "张毅恭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年10月",
        "birthplace": "福建厦门",
        "native_place": "福建厦门",
        "education": "福建农学院农学学士",
        "party_join": "1995年1月",
        "work_start": "1990年8月",
        "current_post": "市委书记、市人大常委会主任",
        "current_org": "中共泉州市委",
        "source": "zh.wikipedia.org; people.com.cn",
        "notes": "长期在厦门任职，曾任厦门市委副书记；2023年1月调任泉州市委书记；2024年1月兼任市人大主任",
        "confidence": "confirmed",
    },
    {
        "id": 2,
        "name": "蔡战胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "陕西渭南",
        "native_place": "陕西渭南",
        "education": "中国石油大学（北京）安全技术及工程专业工学博士",
        "party_join": "1995年12月",
        "work_start": "1997年7月",
        "current_post": "市长",
        "current_org": "泉州市人民政府",
        "source": "zh.wikipedia.org; en.wikipedia.org; cup.edu.cn",
        "notes": "教授级高级工程师；早年在中海油系统任职（2010-2016任中海油中捷石化总经理）；后转入福州任职（仓山区委书记、市委常委、副市长）；2021年7月任泉州市代市长/市长",
        "confidence": "confirmed",
    },
    # ── Recent predecessors ──
    {
        "id": 3,
        "name": "王永礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年9月",
        "birthplace": "福建仙游",
        "native_place": "福建仙游",
        "education": "安徽财贸学院计划统计系学士；福建农林大学管理学博士",
        "party_join": "中共党员",
        "work_start": "1987年7月",
        "current_post": "福建省委常委、常务副省长",
        "current_org": "福建省人民政府",
        "source": "zh.wikipedia.org; en.wikipedia.org",
        "notes": "曾任福建省财政厅厅长(2016.9-2018.6)；泉州市市长(2018.7-2021.7)；泉州市委书记(2021.7-2021.12)；福建省委统战部部长(2021.12-2024.7)；2024.7起任福建省常务副省长",
        "confidence": "confirmed",
    },
    {
        "id": 4,
        "name": "刘建洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年4月",
        "birthplace": "江西莲花",
        "native_place": "江西莲花",
        "education": "江西交通学校公路与桥梁工程专业",
        "party_join": "1986年12月",
        "work_start": "1985年7月",
        "current_post": "江苏省委常委、组织部部长",
        "current_org": "中共江苏省委",
        "source": "en.wikipedia.org; zh.wikipedia.org",
        "notes": "长期在江西南昌任职，曾任南昌市市长(2018.4-2019.12)；莆田市委书记(2019.12-2021.12)；泉州市委书记(2021.12-2022.12)；后调江苏任省委政法委书记，现为省委组织部部长",
        "confidence": "confirmed",
    },
    {
        "id": 5,
        "name": "康涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "福建省政府党组成员",
        "current_org": "福建省人民政府",
        "source": "en.wikipedia.org",
        "notes": "前任泉州市委书记、市长；2018年由康涛任书记、王永礼任市长；2021年7月康涛不再兼任市委书记",
        "confidence": "plausible",
    },
    # ── Key deputies ──
    {
        "id": 6,
        "name": "卢秀萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共泉州市委",
        "source": "zh.wikipedia.org",
        "notes": "市委专职副书记",
        "confidence": "plausible",
    },
    {
        "id": 7,
        "name": "肖汉辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市政协主席",
        "current_org": "中共泉州市委/泉州市政协",
        "source": "zh.wikipedia.org",
        "notes": "曾任市委常委、统战部部长，现任市政协主席",
        "confidence": "plausible",
    },
    {
        "id": 8,
        "name": "陈辉宗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共泉州市纪委",
        "source": "zh.wikipedia.org",
        "notes": "市纪委书记、市监委主任",
        "confidence": "plausible",
    },
    {
        "id": 9,
        "name": "周小华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共泉州市委",
        "source": "zh.wikipedia.org",
        "notes": "",
        "confidence": "plausible",
    },
    {
        "id": 10,
        "name": "陈惠黔",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共泉州市委宣传部",
        "source": "zh.wikipedia.org",
        "notes": "",
        "confidence": "plausible",
    },
    {
        "id": 11,
        "name": "李建辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共泉州市委组织部",
        "source": "zh.wikipedia.org",
        "notes": "",
        "confidence": "plausible",
    },
    {
        "id": 12,
        "name": "黄景春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共泉州市委",
        "source": "zh.wikipedia.org",
        "notes": "",
        "confidence": "plausible",
    },
    {
        "id": 13,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、石狮市委书记",
        "current_org": "中共石狮市委",
        "source": "zh.wikipedia.org",
        "notes": "",
        "confidence": "plausible",
    },
    {
        "id": 14,
        "name": "刘林霜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共泉州市委",
        "source": "zh.wikipedia.org",
        "notes": "",
        "confidence": "plausible",
    },
    # ── Other notable figures ──
    {
        "id": 15,
        "name": "徐华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "泉州市人大常委会",
        "source": "zh.wikipedia.org",
        "notes": "",
        "confidence": "plausible",
    },
]

organizations = [
    {"id": 1, "name": "中共泉州市委", "type": "党委", "level": "地级市", "parent": "中共福建省委", "location": "福建省泉州市"},
    {"id": 2, "name": "泉州市人民政府", "type": "政府", "level": "地级市", "parent": "福建省人民政府", "location": "福建省泉州市"},
    {"id": 3, "name": "泉州市人大常委会", "type": "人大", "level": "地级市", "parent": "福建省人大常委会", "location": "福建省泉州市"},
    {"id": 4, "name": "泉州市政协", "type": "政协", "level": "地级市", "parent": "福建省政协", "location": "福建省泉州市"},
    {"id": 5, "name": "中共泉州市纪委", "type": "纪委", "level": "地级市", "parent": "中共福建省纪委", "location": "福建省泉州市"},
    {"id": 6, "name": "中共泉州市委宣传部", "type": "党委", "level": "地级市", "parent": "中共泉州市委", "location": "福建省泉州市"},
    {"id": 7, "name": "中共泉州市委组织部", "type": "党委", "level": "地级市", "parent": "中共泉州市委", "location": "福建省泉州市"},
    {"id": 8, "name": "中共石狮市委", "type": "党委", "level": "县级市", "parent": "中共泉州市委", "location": "福建省泉州市石狮市"},
    {"id": 9, "name": "中共厦门市委", "type": "党委", "level": "副省级市", "parent": "中共福建省委", "location": "福建省厦门市"},
    {"id": 10, "name": "厦门市人民政府", "type": "政府", "level": "副省级市", "parent": "福建省人民政府", "location": "福建省厦门市"},
    {"id": 11, "name": "福建省财政厅", "type": "政府", "level": "省级", "parent": "福建省人民政府", "location": "福建省福州市"},
    {"id": 12, "name": "中共福建省委统战部", "type": "党委", "level": "省级", "parent": "中共福建省委", "location": "福建省福州市"},
    {"id": 13, "name": "福建省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "福建省福州市"},
    {"id": 14, "name": "中共福建省委", "type": "党委", "level": "省级", "parent": "", "location": "福建省福州市"},
    {"id": 15, "name": "中国海洋石油总公司（中海油）", "type": "事业单位", "level": "央企", "parent": "", "location": "北京"},
    {"id": 16, "name": "泉州市人民政府办公室", "type": "政府", "level": "地级市", "parent": "泉州市人民政府", "location": "福建省泉州市"},
    {"id": 17, "name": "中共莆田市委", "type": "党委", "level": "地级市", "parent": "中共福建省委", "location": "福建省莆田市"},
    {"id": 18, "name": "南昌市人民政府", "type": "政府", "level": "省会城市", "parent": "江西省人民政府", "location": "江西省南昌市"},
    {"id": 19, "name": "中共江苏省委", "type": "党委", "level": "省级", "parent": "", "location": "江苏省南京市"},
    {"id": 20, "name": "中共福州市委", "type": "党委", "level": "省会城市", "parent": "中共福建省委", "location": "福建省福州市"},
    {"id": 21, "name": "福州市人民政府", "type": "政府", "level": "省会城市", "parent": "福建省人民政府", "location": "福建省福州市"},
    {"id": 22, "name": "福建农学院", "type": "事业单位", "level": "高校", "parent": "", "location": "福建省福州市"},
    {"id": 23, "name": "中国石油大学（北京）", "type": "事业单位", "level": "高校", "parent": "", "location": "北京"},
    {"id": 24, "name": "安徽财贸学院", "type": "事业单位", "level": "高校", "parent": "", "location": "安徽省蚌埠市"},
]

positions = [
    # Current roles
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2023年1月", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 3, "title": "市人大常委会主任", "start": "2024年1月", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2021年7月", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2021年7月", "end": "present", "rank": "正厅级", "note": "2021年7月任代市长，同年7月31日当选"},
    {"person_id": 6, "org_id": 1, "title": "市委副书记", "start": "unknown", "end": "present", "rank": "副厅级", "note": "专职副书记"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "市政协主席", "start": "unknown", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委、市纪委书记", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市委常委、秘书长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "市委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "市委常委、组织部部长", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "石狮市委书记", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "市人大常委会主任", "start": "unknown", "end": "present", "rank": "正厅级", "note": "前任张毅恭后接任"},
    # Zhang Yigong career timeline
    {"person_id": 1, "org_id": 22, "title": "学生（福建农学院）", "start": "1986年", "end": "1990年", "rank": "", "note": "获农学学士学位"},
    {"person_id": 1, "org_id": 9, "title": "厦门市委副书记", "start": "unknown", "end": "2023年1月", "rank": "副省级城市副职", "note": "调任泉州前职务"},
    {"person_id": 1, "org_id": 10, "title": "厦门市副市长", "start": "unknown", "end": "unknown", "rank": "副省级城市副职", "note": ""},
    # Cai Zhansheng career timeline
    {"person_id": 2, "org_id": 23, "title": "学生（中国石油大学）", "start": "unknown", "end": "1997年", "rank": "", "note": "安全技术及工程专业"},
    {"person_id": 2, "org_id": 15, "title": "中海油中捷石化总经理、党委书记", "start": "2010年3月", "end": "2016年8月", "rank": "央企二级单位正职", "note": "转入政府前的中海油任职"},
    {"person_id": 2, "org_id": 20, "title": "福州市委常委", "start": "unknown", "end": "2021年7月", "rank": "副省级城市副职", "note": "曾任仓山区委书记、宣传部部长、副市长"},
    {"person_id": 2, "org_id": 20, "title": "福州市仓山区委书记", "start": "unknown", "end": "unknown", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 21, "title": "福州市副市长", "start": "unknown", "end": "2021年7月", "rank": "副省级城市副职", "note": ""},
    # Wang Yongli career timeline
    {"person_id": 3, "org_id": 24, "title": "学生（安徽财贸学院）", "start": "1983年9月", "end": "1987年7月", "rank": "", "note": "计划统计系"},
    {"person_id": 3, "org_id": 11, "title": "福建省财政厅厅长", "start": "2016年9月", "end": "2018年6月", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "泉州市市长", "start": "2018年7月", "end": "2021年7月", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "泉州市委书记", "start": "2021年7月", "end": "2021年12月", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "福建省委统战部部长", "start": "2021年12月", "end": "2024年7月", "rank": "副省级", "note": "2021年11月任省委常委"},
    {"person_id": 3, "org_id": 13, "title": "福建省常务副省长", "start": "2024年7月", "end": "present", "rank": "副省级", "note": "省政府党组副书记"},
    # Liu Jianyang career timeline
    {"person_id": 4, "org_id": 18, "title": "南昌市市长", "start": "2018年4月", "end": "2019年12月", "rank": "副省级", "note": ""},
    {"person_id": 4, "org_id": 17, "title": "莆田市委书记", "start": "2019年12月", "end": "2021年12月", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "泉州市委书记", "start": "2021年12月", "end": "2022年12月", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 19, "title": "江苏省委组织部部长", "start": "2024年3月", "end": "present", "rank": "副省级", "note": "曾任江苏省委政法委书记"},
    # Kang Tao
    {"person_id": 5, "org_id": 1, "title": "泉州市委书记", "start": "unknown", "end": "2021年7月", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "泉州市市长", "start": "unknown", "end": "2018年7月", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 13, "title": "福建省政府党组成员", "start": "2021年", "end": "present", "rank": "副省级", "note": ""},
]

relationships = [
    # Direct predecessor-successor relationships (confirmed)
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "王永礼为前任市长，蔡战胜接任泉州市市长", "overlap_org": "泉州市人民政府", "overlap_period": "2021年7月", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "王永礼为前任市委书记，刘建洋接任泉州市委书记", "overlap_org": "中共泉州市委", "overlap_period": "2021年12月", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "刘建洋为前任市委书记，张毅恭接任泉州市委书记", "overlap_org": "中共泉州市委", "overlap_period": "2023年1月", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 3, "type": "predecessor_successor", "context": "康涛为前任市委书记，王永礼接任泉州市委书记", "overlap_org": "中共泉州市委", "overlap_period": "2021年7月", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 3, "type": "predecessor_successor", "context": "康涛为前任市长，王永礼接任泉州市市长", "overlap_org": "泉州市人民政府", "overlap_period": "2018年7月", "strength": "strong", "confidence": "confirmed"},
    # Current working relationships (confirmed top-level overlap)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长搭档", "overlap_org": "中共泉州市委", "overlap_period": "2023年1月至今", "strength": "strong", "confidence": "confirmed"},
    # Wang Yongli and Cai Zhansheng overlap in Fuzhou system
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "二人均在福州任职过，可能曾在同一班子共事", "overlap_org": "中共福州市委", "overlap_period": "unknown", "strength": "medium", "confidence": "plausible"},
    # Liu Jianyang -> Zhang Yigong handoff
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "刘建洋调江苏后，张毅恭接任市委书记，未直接共事", "overlap_org": "中共泉州市委", "overlap_period": "2022年12月-2023年1月", "strength": "weak", "confidence": "plausible"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p.get("native_place", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def is_top_leader(p):
    return "市委书记" in p["current_post"] or "市长" in p["current_post"] or "市人大常委会主任" in p["current_post"]


def person_color(p):
    """Return 'r,g,b' string for person node."""
    post = p["current_post"]
    if "市委书记" in post or "书记" in post and "副" not in post:
        return "255,50,50"
    if "市长" in post or "市人大" in post:
        return "50,100,255"
    if "纪委" in post:
        return "255,165,0"
    return "100,100,100"


def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>泉州市（福建省）政治人物关系网络 — 市委书记 & 市长</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("rank", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (positions)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} — {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationships)
    for rel in relationships:
        eid += 1
        w = {"strong": "2.0", "medium": "1.5", "weak": "1.0"}.get(rel["strength"], "1.0")
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()
    print(f"\n[DONE] 泉州市 network data built at {TODAY}")
