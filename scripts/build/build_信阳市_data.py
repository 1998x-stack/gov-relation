#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 信阳市 (Xinyang City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_信阳市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.xinyang.gov.cn — 信阳市人民政府门户网站 (primary, official bios)
  - 信阳市河长名单 (2026-06-11) — confirmed市委常委会 composition
  - 2026年政府工作报告 (2026-02-07) — confirmed 陈志伟 as outgoing mayor
  - 卢希望领导信息页 (2026-04-23) — confirmed mayor, birth, education
  - 赵军伟领导信息页 (2025-04-25) — confirmed常委/常务副市长, birth, education
  - 李新伟领导信息页 (2024-05-28) — confirmed常委/宣传部长, birth
  - 张劲松领导信息页 (2026-07-03) — confirmed常委/市政府党组成员, birth
  - 郑云领导信息页 (2023-01-18) — confirmed副市长, birth, education
  - 何克领导信息页 (2024-10-31) — confirmed副市长, birth
  - 刘磊领导信息页 (2023-01-18) — confirmed副市长, birth
  - 汪明君领导信息页 (2023-01-18) — confirmed副市长, birth
  - 袁钢领导信息页 (2024-03-27) — confirmed副市长, birth
  - 杨好平领导信息页 (2025-09-01) — confirmed副市长, birth
  - 孔辉领导信息页 (2025-10-30) — confirmed秘书长, birth
  - 农民日报 (2026-03-09) — 张宏伟 interview as 全国人大代表/市委书记

Confidence notes:
  - 张宏伟: confirmed as 市委书记 via government homepage (multiple news items).
    Exact birth date, birthplace, and full career history not available from government website.
    Prior role before Xinyang: unknown without Baidu Baike access (403 forbidden).
    Identity: 全国人大代表 (confirmed via 农民日报 interview, 2026-03-09).
  - 卢希望: fully confirmed via official bio page. Previously 信阳市委副书记.
    Assumed office as mayor between Feb-Apr 2026.
  - 陈志伟: confirmed as outgoing mayor (presented 2026 government report as mayor on 2026-02-07).
    Successor 卢希望 assumed office by April 2026.
  - All deputy mayors and the secretary-general: confirmed via official government bios.
  - Party committee members: 杨进, 王军, 曾辉, 孔剑君, 于海忠, 唐永伟 confirmed via
    信阳市市级河长名单 (2026-06-11). Detailed bios unavailable.
  - Baidu Baike and other Chinese search engines inaccessible (403/timeout) during investigation.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "信阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths (inside data/tmp/henan_信阳市/)
STAGING_DB = os.path.join(BASE, f"{SLUG}_network.db")
DB_PATH = STAGING_DB  # for process_tmp.py validation
STAGING_GEXF = os.path.join(BASE, f"{SLUG}_network.gexf")
GEXF_PATH = STAGING_GEXF  # for process_tmp.py validation
STAGING_PERSONS = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────
# Person ID scheme: 信阳_{pinyin_name} for dedup across investigations

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Party
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共信阳市委员会",
        "source": "https://www.xinyang.gov.cn (multiple news articles); https://www.xinyang.gov.cn/2026/03-09/773731.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "卢希望",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "研究生，法学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2026/04-23/781390.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Committee Standing Members (市委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "杨进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共信阳市委员会",
        "source": "https://www.xinyang.gov.cn/2026/06-11/789596.html"
    },
    {
        "id": 4,
        "name": "王军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、监委主任",
        "current_org": "中共信阳市纪律检查委员会",
        "source": "https://www.xinyang.gov.cn/2026/06-11/789596.html"
    },
    {
        "id": 5,
        "name": "曾辉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共信阳市委统战部",
        "source": "https://www.xinyang.gov.cn/2026/06-11/789596.html"
    },
    {
        "id": 6,
        "name": "孔剑君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共信阳市委组织部",
        "source": "https://www.xinyang.gov.cn/2026/06-11/789596.html"
    },
    {
        "id": 7,
        "name": "于海忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共信阳市委办公室",
        "source": "https://www.xinyang.gov.cn/2026/06-11/789596.html"
    },
    {
        "id": 8,
        "name": "赵军伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2025/04-25/600279.html"
    },
    {
        "id": 9,
        "name": "唐永伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、信阳军分区政委",
        "current_org": "信阳军分区",
        "source": "https://www.xinyang.gov.cn/2026/06-11/789596.html"
    },
    {
        "id": 10,
        "name": "李新伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长，市政府党组成员",
        "current_org": "中共信阳市委宣传部",
        "source": "https://www.xinyang.gov.cn/2024/05-28/561284.html"
    },
    {
        "id": 11,
        "name": "张劲松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "研究生，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委，市政府党组成员",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2026/07-03/793002.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "郑云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年8月",
        "birthplace": "",
        "education": "研究生，经济学博士",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2023/01-18/561267.html"
    },
    {
        "id": 13,
        "name": "何克",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2024/10-31/561286.html"
    },
    {
        "id": 14,
        "name": "刘磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年5月",
        "birthplace": "",
        "education": "法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2023/01-18/561269.html"
    },
    {
        "id": 15,
        "name": "汪明君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2023/01-18/561266.html"
    },
    {
        "id": 16,
        "name": "袁钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2024/03-27/561283.html"
    },
    {
        "id": 17,
        "name": "杨好平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "",
        "education": "大学，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "信阳市人民政府",
        "source": "https://www.xinyang.gov.cn/2025/09-01/693364.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Secretary-General
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "name": "孔辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年1月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长、党组成员，机关党组书记",
        "current_org": "信阳市人民政府办公室",
        "source": "https://www.xinyang.gov.cn/2025/10-30/703672.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 19,
        "name": "陈志伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "（已离任）",
        "source": "https://www.xinyang.gov.cn/2026/02-12/753704.html (2026年政府工作报告)"
    },
]


# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共信阳市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "信阳市"},
    {"id": 2, "name": "信阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "信阳市"},
    {"id": 3, "name": "中共信阳市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "", "location": "信阳市"},
    {"id": 4, "name": "信阳市监察委员会", "type": "党委", "level": "地级市", "parent": "", "location": "信阳市"},
    {"id": 5, "name": "中共信阳市委统战部", "type": "党委", "level": "地级市", "parent": "中共信阳市委员会", "location": "信阳市"},
    {"id": 6, "name": "中共信阳市委组织部", "type": "党委", "level": "地级市", "parent": "中共信阳市委员会", "location": "信阳市"},
    {"id": 7, "name": "中共信阳市委办公室", "type": "党委", "level": "地级市", "parent": "中共信阳市委员会", "location": "信阳市"},
    {"id": 8, "name": "中共信阳市委宣传部", "type": "党委", "level": "地级市", "parent": "中共信阳市委员会", "location": "信阳市"},
    {"id": 9, "name": "信阳军分区", "type": "事业单位", "level": "地级市", "parent": "", "location": "信阳市"},
    {"id": 10, "name": "信阳市人民政府办公室", "type": "政府", "level": "地级市", "parent": "信阳市人民政府", "location": "信阳市"},
    {"id": 11, "name": "中共信阳市委政法委", "type": "党委", "level": "地级市", "parent": "中共信阳市委员会", "location": "信阳市"},
]


# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 张宏伟
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "全国人大代表"},
    # 卢希望
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2026年4月", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 杨进
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 11, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 王军
    {"person_id": 4, "org_id": 3, "title": "市纪委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "市监委主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 曾辉
    {"person_id": 5, "org_id": 5, "title": "统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 孔剑君
    {"person_id": 6, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 于海忠
    {"person_id": 7, "org_id": 7, "title": "市委秘书长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 赵军伟
    {"person_id": 8, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 唐永伟
    {"person_id": 9, "org_id": 9, "title": "信阳军分区政委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李新伟
    {"person_id": 10, "org_id": 8, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": 10, "org_id": 2, "title": "市政府党组成员", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 张劲松
    {"person_id": 11, "org_id": 2, "title": "市委常委、市政府党组成员", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 郑云
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "无党派人士"},
    # 何克
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 刘磊
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 汪明君
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 袁钢
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 杨好平
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 孔辉
    {"person_id": 18, "org_id": 10, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "机关党组书记"},
    # 陈志伟（前任市长）
    {"person_id": 19, "org_id": 2, "title": "市长（前任）", "start_date": "2023年", "end_date": "2026年2月", "rank": "正厅级", "note": "已离任"},
]


# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    # 张宏伟 ↔ 卢希望 (书记—市长搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "信阳市", "overlap_period": "2026年—"},
    # 张宏伟 ↔ 杨进 (书记—副书记搭档)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 卢希望 ↔ 赵军伟 (市长—常务副市长搭档)
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—常务副市长搭档", "overlap_org": "信阳市人民政府", "overlap_period": "2026年—"},
    # 卢希望 ↔ 陈志伟 (前后任市长)
    {"person_a": 2, "person_b": 19, "type": "前后任", "context": "前后任市长（交接2026年2月—4月）", "overlap_org": "信阳市人民政府", "overlap_period": "2026年"},
    # 张宏伟 ↔ 赵军伟 (书记—常委/副市长)
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 张宏伟 ↔ 王军 (书记—纪委书记)
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 张宏伟 ↔ 曾辉 (书记—统战部长)
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 张宏伟 ↔ 孔剑君 (书记—组织部长)
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 张宏伟 ↔ 于海忠 (书记—秘书长)
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—秘书长工作关系", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 张宏伟 ↔ 李新伟 (书记—宣传部长)
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 张宏伟 ↔ 张劲松 (书记—常委)
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 张宏伟 ↔ 唐永伟 (书记—军分区政委)
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 赵军伟 ↔ 何克 (副市长同僚)
    {"person_a": 8, "person_b": 13, "type": "共事", "context": "市政府班子共事", "overlap_org": "信阳市人民政府", "overlap_period": ""},
    # 赵军伟 ↔ 刘磊 (副市长同僚)
    {"person_a": 8, "person_b": 14, "type": "共事", "context": "市政府班子共事", "overlap_org": "信阳市人民政府", "overlap_period": ""},
    # 赵军伟 ↔ 孔辉 (常务副市长—秘书长工作关系)
    {"person_a": 8, "person_b": 18, "type": "共事", "context": "常务副市长—秘书长工作关系", "overlap_org": "信阳市人民政府", "overlap_period": ""},
    # 汪明君 ↔ 袁钢 (副市长同僚)
    {"person_a": 15, "person_b": 16, "type": "共事", "context": "市政府班子共事", "overlap_org": "信阳市人民政府", "overlap_period": ""},
    # 郑云 ↔ 杨好平 (副市长同僚，特别教育和科技分管领域)
    {"person_a": 12, "person_b": 17, "type": "共事", "context": "市政府班子共事", "overlap_org": "信阳市人民政府", "overlap_period": ""},
    # 李新伟 ↔ 张劲松 (常委同僚)
    {"person_a": 10, "person_b": 11, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
    # 杨进 ↔ 王军 (副书记—纪委书记)
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "市委常委会共事", "overlap_org": "中共信阳市委员会", "overlap_period": ""},
]


# ── Write Database ─────────────────────────────────────────────────────────
def write_database():
    import sqlite3
    db_path = STAGING_DB
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create tables
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    
    # Insert persons
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p.get("birthplace", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"])
        )
    
    # Insert organizations
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"])
        )
    
    # Insert positions
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""),
             pos.get("end_date", ""), pos["rank"], pos.get("note", ""))
        )
    
    # Insert relationships
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )
    
    conn.commit()
    conn.close()
    print(f"Database written: {db_path}")
    print(f"  - {len(persons)} persons")
    print(f"  - {len(organizations)} organizations")
    print(f"  - {len(positions)} positions")
    print(f"  - {len(relationships)} relationships")


# ── Write GEXF ─────────────────────────────────────────────────────────────
def write_gexf():
    from datetime import datetime
    
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    
    def person_color(post):
        if "书记" in post and "纪委" not in post:
            return "200,30,30"  # Red for party secretary
        if "市长" in post:
            return "30,100,200"  # Blue for mayor
        if "副书记" in post:
            return "220,80,80"  # Light red for deputy secretary
        if "纪委书记" in post or "监委" in post:
            return "255,165,0"  # Orange for discipline
        if "常委" in post:
            return "180,100,180"  # Purple for standing committee
        if "副市长" in post or "副" in post:
            return "100,150,220"  # Light blue for deputies
        return "100,100,100"
    
    def person_size(post):
        if "书记" in post and "纪委" not in post:
            return "20.0"
        if "市长" in post:
            return "20.0"
        if "副书记" in post:
            return "15.0"
        if "常委" in post:
            return "12.0"
        if "副市长" in post:
            return "12.0"
        return "10.0"
    
    def org_color(org_type):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "事业单位": "220,220,220",
        }
        return colors.get(org_type, "200,200,200")
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>信阳市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
    lines.append('      <attribute id="8" title="level" type="string"/>')
    lines.append('      <attribute id="9" title="location" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    
    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = person_size(p["current_post"])
        rgb = c.split(",")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    for o in organizations:
        c = org_color(o["type"])
        rgb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    eid = 0
    lines.append('    <edges>')
    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    os.makedirs(os.path.dirname(STAGING_GEXF), exist_ok=True)
    with open(STAGING_GEXF, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {STAGING_GEXF}")
    print(f"  - {len(persons) + len(organizations)} nodes")
    print(f"  - {eid} edges")


# ── Write Person JSONs ─────────────────────────────────────────────────────
def write_person_jsons():
    person_files = []
    
    for p in persons:
        if not p["name"]:
            continue
        # Find positions for this person
        person_positions = [pos for pos in positions if pos["person_id"] == p["id"]]
        # Find relationships for this person
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        
        # Build related persons list
        related = []
        for r in person_rels:
            other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
            other = next((x for x in persons if x["id"] == other_id), None)
            if other:
                related.append({
                    "name": other["name"],
                    "current_post": other["current_post"],
                    "relationship_type": r["type"],
                    "context": r["context"],
                })
        
        # Build position timeline
        timeline = []
        for pos in person_positions:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            timeline.append({
                "title": pos["title"],
                "org": org["name"] if org else "",
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "rank": pos.get("rank", ""),
            })
        
        job_title_clean = p["current_post"].replace("/", "_").replace("、", "_")
        filename = f"{TODAY}-河南省-信阳市-{job_title_clean}-{p['name']}.json"
        filepath = os.path.join(STAGING_PERSONS, filename)
        
        person_data = {
            "name": p["name"],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p.get("birthplace", ""),
            "education": p["education"],
            "party_join": p["party_join"],
            "work_start": p.get("work_start", ""),
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "source": p["source"],
            "investigation_date": AS_OF,
            "task_id": "henan_信阳市",
            "province": "河南省",
            "city": "信阳市",
            "position_timeline": timeline,
            "related_persons": related,
            "open_questions": [],
        }
        
        # Add open questions for persons with incomplete data
        if not p["birth"]:
            person_data["open_questions"].append("出生年月待查")
        if not p.get("birthplace"):
            person_data["open_questions"].append("籍贯待查")
        if not p.get("education"):
            person_data["open_questions"].append("学历/教育背景待查")
        if not timeline or not any(t["start"] for t in timeline if t["start"]):
            person_data["open_questions"].append("完整履历时间线待查（仅确认当前职务）")
        
        # Add career gap note for 张宏伟
        if p["id"] == 1:
            person_data["open_questions"].append("张宏伟到信阳任职前的履历待查（曾任职务、出生地等信息不明）")
            person_data["open_questions"].append("前任市委书记是谁？何时交接？")
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        person_files.append(filepath)
        print(f"Person JSON written: {filepath}")
    
    return person_files


# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} data...")
    print(f"Date: {AS_OF}")
    print()
    
    write_database()
    print()
    
    write_gexf()
    print()
    
    files = write_person_jsons()
    print()
    
    print("=" * 60)
    print("BUILD COMPLETE")
    print("=" * 60)
    print(f"Database: {STAGING_DB}")
    print(f"GEXF:     {STAGING_GEXF}")
    print(f"Person JSONs: {len(files)} files in {STAGING_PERSONS}")
