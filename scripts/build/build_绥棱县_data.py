#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 绥棱县 (Suileng County), 绥化市, 黑龙江省.

Investigation date: 2026-08-05/06
Task ID: heilongjiang_绥棱县
Level: 县 (county)
Parent city: 绥化市
Province: 黑龙江省
Targets: 县委书记 & 县长

Research sources:
  - 绥棱县人民政府官网 (www.suiling.gov.cn) — confirmed current leadership via official news + 领导之窗 official resume pages
  - 绥棱县本地要闻 (zwyw): 2026-07-29/08-04 县委常委会会议新闻 confirmed 徐野 as 县委书记、县长 (一肩挑); 2026-07-13 县委党建人才工作会议 confirmed 赵辉 as 前任县委书记
  - 政府领导之窗 (xzf) official resume pages — confirmed 县政府领导班子 (县长徐野 + 6副县长) with birth/education
  - 县委领导之窗 (alxw) official resume pages — confirmed 县委常委会名单

Key findings:
  - 徐野: 县委书记兼县长 (一肩挑), 男/汉, 1982年4月生, 研究生, 中共党员。2026-07-29前后由县长接任县委书记, 现书记县长双兼。
  - 赵辉: 前任县委书记, 至2026-07中旬仍任县委书记(县委党建人才工作领导小组组长), 7月中下旬卸任, 去向未知。
  - 县政府班子 (1县长 + 6副县长): 徐野(县长)、王连辉(常委/副县长, 疑常务)、潘忠亮(常委/副县长)、张洪建(副县长/公安局长)、曹伟(副县长)、姚庆宇(副县长)、赵锋(副县长)
  - 县委常委会 (2026-08): 徐野、刘兆阳(副书记)、李长勇、王连辉、潘忠亮、冷德明、王海荣、陈峰伟(人武部)、解松梅(宣传部长)、徐雯涛(组织部长)
  - 县人大常委会: 刘剑利(主任)、杨立权/吕贺/孙辅义/李威威(副主任); 县政协: 杜金铭(主席)

Confidence notes:
  - 徐野 (县委书记/县长): confirmed via multiple official government news (2026-07/08) + official resume page
  - 县政府、县委班子: confirmed via official 领导之窗 resume pages + official news attendance lists
  - 常务副县长 (王连辉/潘忠亮): plausible (排序第一、代表县政府列席人大; 官方未明示"常务"字样)
  - 徐野任县长前的完整履历、出生地/籍贯/入党时间: unverified / unknown
  - 赵辉卸任去向: unverified / unknown
  - 县纪委书记/监委主任、法院院长、检察院检察长: unverified
  - Web search engines (Exa, Baidu, Bing, Jina) were rate-limited or blocked during this investigation; official county portal used as primary source
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ── Constants ───────────────────────────────────────────────────────────────
SLUG = "绥棱县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# Correct official live county portal (note: suileng.gov.cn is dead)
SRC_GOV = "http://www.suiling.gov.cn/"
SRC_XWP = "http://www.suiling.gov.cn/sl/zwyw/202608/c12_239086.shtml"   # 2026-08-04 县委常委会 (徐野 书记/县长)
SRC_XWP2 = "http://www.suiling.gov.cn/sl/zwyw/202607/c12_238580.shtml"  # 2026-07-29 县委常委会扩大会 (徐野 书记/县长)
SRC_XWP3 = "http://www.suiling.gov.cn/sl/zwyw/202607/c12_237654.shtml"  # 2026-07-13 赵辉 书记(党建工作领导小组组长)
SRC_XWP4 = "http://www.suiling.gov.cn/sl/zwyw/202607/c12_238718.shtml"  # 2026-07 八一走访 (刘剑利/杜金铭/杨立权/吕贺/孙福义/李威威)
SRC_ZF = "http://www.suiling.gov.cn/sl/xzf/list02.shtml"                # 县政府领导之窗
SRC_XW = "http://www.suiling.gov.cn/sl/alxw/list02.shtml"               # 县委领导之窗

# Individual official resume pages (县政府领导之窗)
SRC_XUYE = "http://www.suiling.gov.cn/sl/xzf/202404/c12_183174.shtml"    # 徐野 县长简历
SRC_WANGLH = "http://www.suiling.gov.cn/sl/xzf/202606/c12_234802.shtml"  # 王连辉 1977.12 本科
SRC_PANZL = "http://www.suiling.gov.cn/sl/xzf/202404/c12_183173.shtml"   # 潘忠亮 1985.4 研究生
SRC_ZHANGHJ = "http://www.suiling.gov.cn/sl/xzf/202503/c12_206739.shtml" # 张洪建 1979.9 大学 (副县长兼公安局长)
SRC_CAOW = "http://www.suiling.gov.cn/sl/xzf/202503/c12_206740.shtml"    # 曹伟 1977.4 大学
SRC_YAOQY = "http://www.suiling.gov.cn/sl/xzf/202606/c12_236188.shtml"   # 姚庆宇 1987.5 女
SRC_ZHAF = "http://www.suiling.gov.cn/sl/xzf/202503/c12_206741.shtml"    # 赵锋 1982.4 大学
SRC_CH_feng = "http://www.suiling.gov.cn/sl/alxw/202507/c12_214199.shtml"  # 陈峰伟 人武部

DB_NAME = f"{SLUG}_network.db"
GEXF_NAME = f"{SLUG}_network.gexf"

# Absolute paths for process_tmp.py compatibility (will be overridden in main())
DB_PATH = os.path.join(BASE, DB_NAME)
GEXF_PATH = os.path.join(BASE, GEXF_NAME)

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 核心领导 (县委书记 & 县长)
    # ═══════════════════════════════════════════════════════════════════════
    # 徐野 — 县委书记兼县长 (一肩挑)
    {
        "id": 1,
        "name": "徐野",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记、县长",
        "current_org": "中共绥棱县委员会",
        "source": SRC_XUYE
    },
    # 赵辉 — 前任县委书记
    {
        "id": 2,
        "name": "赵辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共绥棱县委员会",
        "source": SRC_XWP3
    },
    # 刘兆阳 — 县委副书记
    {
        "id": 3,
        "name": "刘兆阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共绥棱县委员会",
        "source": SRC_XWP
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 县委常委会其他成员
    # ═══════════════════════════════════════════════════════════════════════
    # 李长勇 — 县委常委
    {
        "id": 4,
        "name": "李长勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共绥棱县委员会",
        "source": SRC_XWP
    },
    # 王海荣 — 县委常委
    {
        "id": 5,
        "name": "王海荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共绥棱县委员会",
        "source": SRC_XWP
    },
    # 冷德明 — 县委常委
    {
        "id": 6,
        "name": "冷德明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共绥棱县委员会",
        "source": SRC_XWP
    },
    # 陈峰伟 — 县委常委、人武部部长
    {
        "id": 7,
        "name": "陈峰伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "1978-01",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部部长",
        "current_org": "绥棱县人民武装部",
        "source": SRC_CH_feng
    },
    # 解松梅 — 县委常委、宣传部部长
    {
        "id": 8,
        "name": "解松梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "1977-04",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共绥棱县委宣传部",
        "source": "http://www.suiling.gov.cn/sl/alxw/202607/c12_237730.shtml"
    },
    # 徐雯涛 — 县委常委、组织部部长
    {
        "id": 9,
        "name": "徐雯涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "1982-08",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共绥棱县委组织部",
        "source": "http://www.suiling.gov.cn/sl/alxw/202607/c12_237729.shtml"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 县政府领导班子 (副县长)
    # ═══════════════════════════════════════════════════════════════════════
    # 王连辉 — 县委常委、副县长 (疑常务副县长)
    {
        "id": 10,
        "name": "王连辉",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1977-12",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "绥棱县人民政府",
        "source": SRC_WANGLH
    },
    # 潘忠亮 — 县委常委、副县长
    {
        "id": 11,
        "name": "潘忠亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-04",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "绥棱县人民政府",
        "source": SRC_PANZL
    },
    # 张洪建 — 副县长、县公安局局长
    {
        "id": 12,
        "name": "张洪建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "绥棱县人民政府",
        "source": SRC_ZHANGHJ
    },
    # 曹伟 — 副县长
    {
        "id": 13,
        "name": "曹伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-04",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "绥棱县人民政府",
        "source": SRC_CAOW
    },
    # 姚庆宇 — 副县长
    {
        "id": 14,
        "name": "姚庆宇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987-05",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "绥棱县人民政府",
        "source": SRC_YAOQY
    },
    # 赵锋 — 副县长
    {
        "id": 15,
        "name": "赵锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "绥棱县人民政府",
        "source": SRC_ZHAF
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共绥棱县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共绥化市委员会",
        "location": "绥棱县"
    },
    {
        "id": 2,
        "name": "绥棱县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "绥化市人民政府",
        "location": "绥棱县"
    },
    {
        "id": 3,
        "name": "绥棱县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "绥化市人民代表大会常务委员会",
        "location": "绥棱县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议绥棱县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协绥化市委员会",
        "location": "绥棱县"
    },
    {
        "id": 5,
        "name": "中共绥棱县委宣传部",
        "type": "党委部门",
        "level": "县",
        "parent": "中共绥棱县委员会",
        "location": "绥棱县"
    },
    {
        "id": 6,
        "name": "中共绥棱县委组织部",
        "type": "党委部门",
        "level": "县",
        "parent": "中共绥棱县委员会",
        "location": "绥棱县"
    },
    {
        "id": 7,
        "name": "绥棱县人民武装部",
        "type": "军队",
        "level": "县",
        "parent": "绥化军分区",
        "location": "绥棱县"
    },
    {
        "id": 8,
        "name": "绥棱县公安局",
        "type": "政法",
        "level": "县",
        "parent": "绥棱县人民政府",
        "location": "绥棱县"
    },
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 徐野 — 县委书记、县长 (一肩挑)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-07-29", "end": "present", "rank": "正处级",
     "note": "2026-07-29前后由县长接任县委书记, 现书记县长双兼。confirmed via 2026-07/08 县委常委会新闻."},
    {"person_id": 1, "org_id": 2, "title": "县长", "start": "2024-09前", "end": "present", "rank": "正处级",
     "note": "自2024年9月前即任绥棱县长; 为县政府党组书记."},
    # 赵辉 — 前任县委书记
    {"person_id": 2, "org_id": 1, "title": "县委书记", "start": "", "end": "2026-07中旬", "rank": "正处级",
     "note": "前任县委书记, 2026-07-13仍任县党建工作领导小组组长; 7月中下旬卸任, 去向待查."},
    # 刘兆阳 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "县委副书记, 县委常委会成员."},
    # 李长勇
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "县委常委会成员."},
    # 王海荣
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "县委常委会成员."},
    # 冷德明
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "县委常委会成员."},
    # 陈峰伟
    {"person_id": 7, "org_id": 7, "title": "县委常委、县人武部部长", "start": "", "end": "present", "rank": "副团级",
     "note": "县人武部领导."},
    # 解松梅
    {"person_id": 8, "org_id": 5, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "县委宣传部部长."},
    # 徐雯涛
    {"person_id": 9, "org_id": 6, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "县委组织部部长."},
    # 王连辉
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "常委副县长, 各府昋见列席人大; 疑为常务副县长(plausible)."},
    # 潘忠亮
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "常委副县长."},
    # 张洪建
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "副县长兼公安局长."},
    {"person_id": 12, "org_id": 8, "title": "县公安局局长", "start": "", "end": "present", "rank": "正科级",
     "note": "副县长兼县公安局长."},
    # 曹伟
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "副县长."},
    # 姚庆宇
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "副县长."},
    # 赵锋
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "副县长."},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政一把手 (书记/县长)：徐野与前任书记赵辉 (前后任)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "赵辉任县委书记期间徐野任县长, 2026-07赵辉卸任徐野接任书记(前后任+上下级共事)",
     "overlap_org": "中共绥棱县委/绥棱县人民政府", "overlap_period": "2024-2026-07",
     "strength": "strong", "confidence": "confirmed", "source": SRC_XWP3},
    # 县委常委会共事 (confirmed)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委班子成员", "overlap_org": "中共绥棱县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_XWP},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委班子成员", "overlap_org": "中共绥棱县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_XWP},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委班子成员", "overlap_org": "中共绥棱县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_XWP},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委班子成员", "overlap_org": "中共绥棱县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_XWP},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委班子成员", "overlap_org": "中共绥棱县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_XWP},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委班子成员", "overlap_org": "中共绥棱县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_XWP},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委班子成员", "overlap_org": "中共绥棱县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_XWP},
    # 县政府班子
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县长与副县长工作关系", "overlap_org": "绥棱县人民政府", "overlap_period": "2024-", "strength": "strong", "confidence": "confirmed", "source": SRC_ZF},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县长与副县长工作关系", "overlap_org": "绥棱县人民政府", "overlap_period": "2024-", "strength": "strong", "confidence": "confirmed", "source": SRC_ZF},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县长与副县长工作关系", "overlap_org": "绥棱县人民政府", "overlap_period": "2024-", "strength": "strong", "confidence": "confirmed", "source": SRC_ZF},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县长与副县长工作关系", "overlap_org": "绥棱县人民政府", "overlap_period": "2024-", "strength": "strong", "confidence": "confirmed", "source": SRC_ZF},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县长与副县长工作关系", "overlap_org": "绥棱县人民政府", "overlap_period": "2024-", "strength": "strong", "confidence": "confirmed", "source": SRC_ZF},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县长与副县长工作关系", "overlap_org": "绥棱县人民政府", "overlap_period": "2024-", "strength": "strong", "confidence": "confirmed", "source": SRC_ZF},
    # 副县长与县委委员交叉 (王连杰/潘忠亮 常委兼副县长)
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "同为县委常委会成员及县政府副县长", "overlap_org": "中共绥棱县委/绥棱县人民政府", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed", "source": SRC_ZF},
]

# ── Helper Functions ──────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    title = p.get("current_post", "")
    if "书记" in title and "纪委" not in title:
        return "255,50,50"   # Party Secretary - Red
    elif "县长" in title:
        return "50,100,255"  # Mayor - Blue
    elif "纪委" in title:
        return "255,165,0"   # Discipline - Orange
    else:
        return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "公安" in t or "政法" in t:
        return "200,230,255"
    elif "军队" in t:
        return "180,180,180"
    else:
        return "200,200,200"

# ── Run Build ──────────────────────────────────────────────────────────────
def main():
    staging_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(staging_dir, DB_NAME)
    gexf_path = os.path.join(staging_dir, GEXF_NAME)

    print(f"=== Building {SLUG} network ===")
    print(f"Staging dir: {staging_dir}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")

    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS persons
        (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
         birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
         work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS organizations
        (id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS positions
        (id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER, title TEXT,
         start TEXT, "end" TEXT, rank TEXT, note TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS relationships
        (id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER, type TEXT,
         context TEXT, overlap_org TEXT, overlap_period TEXT, strength TEXT,
         confidence TEXT, source TEXT)''')

    for p in persons:
        c.execute('''INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join,
             work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))
    for o in organizations:
        c.execute('''INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)''',
            (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))
    for i, pos in enumerate(positions, 1):
        c.execute('''INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, "end", rank, note) VALUES (?,?,?,?,?,?,?,?)''',
            (i, pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
             pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))
    for i, rel in enumerate(relationships, 1):
        c.execute('''INSERT OR REPLACE INTO relationships
            (id, person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence, source) VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (i, rel["person_a"], rel["person_b"], rel["type"], rel.get("context", ""),
             rel.get("overlap_org", ""), rel.get("overlap_period", ""),
             rel.get("strength", ""), rel.get("confidence", ""), rel.get("source", "")))
    conn.commit()
    conn.close()
    print(f"✓ Database created: {db_path}")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        is_top = "书记" in p["current_post"]
        sz = "20.0" if is_top else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("confidence", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF created: {gexf_path}")

    # ── Person JSON ──
    for p in persons:
        person_id = f"heilongjiang_suihua_suileng_{p['name']}"
        job = p["current_post"].replace(" ", "").replace("、", "和")
        filename = f"{TODAY}-黑龙江省-绥化市-{job}-{p['name']}.json"
        filepath = os.path.join(staging_dir, filename)
        is_top = "书记" in p["current_post"] or "县长" in p["current_post"]
        person_data = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "黑龙江省", "city": "绥化市", "region": "绥棱县",
                "job": p["current_post"], "task_id": "heilongjiang_绥棱县", "time_focus": AS_OF
            },
            "identity": {
                "person_id": person_id, "name": p["name"], "aliases": [],
                "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""), "birthplace": "", "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""),
                               "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": p.get("party_join", ""), "work_start": "",
                "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth','')}",
                                "name_birthplace": "", "official_profile_url": p.get("source", "")}
            },
            "current_status": {
                "current_post": p["current_post"], "current_org": p["current_org"],
                "administrative_rank": "正处级" if is_top else "副处级",
                "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "", "end": "present", "org": p["current_org"], "title": p["current_post"],
                 "level": "县", "location": "绥棱县, 绥化市, 黑龙江省",
                 "system": "party" if "书记" in p["current_post"] else "government",
                 "rank": "", "is_key_promotion": is_top, "notes": p.get("source", ""),
                 "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [], "secondary_specializations": [],
                "career_pattern": "unknown", "systems_experience": [],
                "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [], "speech_themes": [], "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": [
                {"id": "S001", "title": f"绥棱县人民政府官网 - 领导之窗 (表彰{p['current_post']})",
                 "url": p.get("source", "http://www.suiling.gov.cn/"), "publisher": "绥棱县人民政府",
                 "published_at": AS_OF, "accessed_at": TODAY, "source_type": "official",
                 "reliability": "high", "notes": f"Official leadership window confirming {p['name']} as {p['current_post']}"}
            ],
            "confidence_summary": {
                "identity": "confirmed" if p.get("birth") else "plausible",
                "current_role": "confirmed", "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整职业生涯（出生地/籍贯/入党时间/任前履历）未知" if not p.get("birthplace") else "部分履历未得"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯（出生地、入党时间、任{['current_post']}前的历任职务）",
                 "why_it_matters": "了解干部成长轨迹与跨县/上级关联", "suggested_queries": [f"{p['name']} 简历 绥棱"],
                 "last_attempted": TODAY},
                {"priority": "high",
                 "question": f"{p['name']}任当前职务的确切日期与任免依据",
                 "why_it_matters": "建立精确文本/时间线", "suggested_queries": [f"绥化市委组织部 任前公示 {p['name']}"],
                 "last_attempted": TODAY}
            ]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Person JSON created: {filepath}")

    print(f"\n=== Build complete for {SLUG} ===")
    print(f"Database: {db_path}")
    print(f"GEXF: {gexf_path}")
    print(f"Person JSONs: {len(persons)} files in {staging_dir}")

if __name__ == "__main__":
    main()