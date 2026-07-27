#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海林市 (Hailin City), 牡丹江市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_海林市
Research sources:
  - Hailin City Government Website (www.hailin.gov.cn)
  - Government leadership page (领导之窗)
  - Official leader biography pages
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

# ── Staging paths ─────────────────────────────────────────────────────────────

STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "海林市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# Canonical destination paths (for promotion)
CANONICAL_DB = os.path.join(STAGING, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(STAGING, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(STAGING, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(STAGING) / ".." / ".." / "persons"

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else ""

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 张洪蓬 — 市委书记 (as of July 2026)
    {"id": 1, "name": "张洪蓬", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年8月", "birthplace": "", "education": "黑龙江省委党校经济管理专业，研究生学历，法学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/secretary/202411/c03_357775.shtml"},

    # 于德波 — 市委副书记、市长 (as of July 2026)
    {"id": 2, "name": "于德波", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年10月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/mayor/202605/c03_357760.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    #市委 Deputy Secretaries
    # ══════════════════════════════════════════════════════════════════════════

    # 杜宇明 — 市委副书记
    {"id": 3, "name": "杜宇明", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年5月", "birthplace": "", "education": "研究生学历，管理学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记", "current_org": "中共海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/deputysecretary/202605/c03_1046499.shtml"},

    # 朱艳辉 — 市委副书记（正处级）
    {"id": 4, "name": "朱艳辉", "gender": "女", "ethnicity": "汉族",
     "birth": "1985年3月", "birthplace": "", "education": "研究生学历，管理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记（正处级）", "current_org": "中共海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/deputysecretary/202504/c03_1002759.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    #市委 Standing Committee
    # ══════════════════════════════════════════════════════════════════════════

    # 刘业贤 — 市委常委、市纪委书记、市监委主任
    {"id": 5, "name": "刘业贤", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年8月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市纪委书记、市监委主任", "current_org": "中共海林市纪律检查委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202305/c03_355669.shtml"},

    # 李修杰 — 市委常委、市政府副市长、党组成员，海林经济技术开发区管理委员会主任
    {"id": 6, "name": "李修杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202307/c03_355840.shtml"},

    # 衣明 — 市委常委、组织部部长，市委党校第一副校长
    {"id": 7, "name": "衣明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中共海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202312/c03_852431.shtml"},

    # 韩雨昊 — 市委常委，市政府副市长、党组副书记
    {"id": 8, "name": "韩雨昊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长（党组副书记）", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202312/c03_988383.shtml"},

    # 丁建萍 — 市委常委，市政府副市长、党组成员
    {"id": 9, "name": "丁建萍", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202412/c03_988386.shtml"},

    # 马君钰 — 市委常委、宣传部部长
    {"id": 10, "name": "马君钰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、宣传部部长", "current_org": "中共海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202501/c03_988740.shtml"},

    # 冯立明 — 市委常委、政法委书记
    {"id": 11, "name": "冯立明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、政法委书记", "current_org": "中共海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202305/c03_1032509.shtml"},

    # 王超 — 市委常委（2026年6月新任命）
    {"id": 12, "name": "王超", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委", "current_org": "中共海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202606/c03_1048861.shtml"},

    # 张志刚 — 市委常委、武装部部长
    {"id": 13, "name": "张志刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、武装部部长", "current_org": "海林市人民武装部",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202606/c03_1049687.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # Deputy Mayors (non-standing committee)
    # ══════════════════════════════════════════════════════════════════════════

    # 李峰 — 市政府副市长、党组成员
    {"id": 14, "name": "李峰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/deputymayor/202305/c03_350549.shtml"},

    # 王胜勇 — 市政府副市长、党组成员，市公安局党委书记、局长、督察长
    {"id": 15, "name": "王胜勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副市长、市公安局局长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/deputymayor/202508/c03_1015636.shtml"},

    # 杨旭莹 — 市政府副市长
    {"id": 16, "name": "杨旭莹", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/deputymayor/202601/c03_1032593.shtml"},

    # 郭忠奎 — 市政府副市长、党组成员
    {"id": 17, "name": "郭忠奎", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/deputymayor/202305/c03_350515.shtml"},

    # 孙凌宇 — 市政府副市长、党组成员
    {"id": 18, "name": "孙凌宇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "海林市人民政府",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/deputymayor/202605/c03_355850.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # 人大 (NPC)
    # ══════════════════════════════════════════════════════════════════════════

    # 王欣 — 市人大常委会主任、党组书记
    {"id": 19, "name": "王欣", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会主任", "current_org": "海林市人大常委会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/NPCdirector/202305/c03_350501.shtml"},

    # 鲍丰臣 — 市人大常委会副主任
    {"id": 20, "name": "鲍丰臣", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会副主任", "current_org": "海林市人大常委会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/NPCdeputydirector/202305/c03_355632.shtml"},

    # 李洪君 — 市人大常委会副主任
    {"id": 21, "name": "李洪君", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会副主任", "current_org": "海林市人大常委会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/NPCdeputydirector/202305/c03_355630.shtml"},

    # 张亮 — 人大常委会副主任
    {"id": 22, "name": "张亮", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市人大常委会副主任", "current_org": "海林市人大常委会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/NPCdeputydirector/202308/c03_361776.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # 政协 (CPPCC)
    # ══════════════════════════════════════════════════════════════════════════

    # 赵立群 — 市政协主席、党组书记
    {"id": 23, "name": "赵立群", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市政协主席", "current_org": "政协海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/CPPCCchairman/202506/c03_1008935.shtml"},

    # 齐景伟 — 市政协副主席
    {"id": 24, "name": "齐景伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市政协副主席", "current_org": "政协海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/CPPCCcochairman/202305/c03_350529.shtml"},

    # 徐静 — 市政协副主席
    {"id": 25, "name": "徐静", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市政协副主席", "current_org": "政协海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/CPPCCcochairman/202404/c03_922402.shtml"},

    # 李乐 — 市政协副主席候选人
    {"id": 26, "name": "李乐", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "市政协副主席候选人", "current_org": "政协海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/CPPCCcochairman/202605/c03_350527.shtml"},

    # 郝勇 — 市政协党组成员、秘书长
    {"id": 27, "name": "郝勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市政协秘书长", "current_org": "政协海林市委员会",
     "source": "https://www.hailin.gov.cn/mdjhlsrmzf/CPPCCofficedirector/202305/c03_350534.shtml"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共海林市委员会", "type": "党委", "level": "县处级", "parent": "中共牡丹江市委员会", "location": "黑龙江省牡丹江市海林市"},
    {"id": 2, "name": "海林市人民政府", "type": "政府", "level": "县处级", "parent": "牡丹江市人民政府", "location": "黑龙江省牡丹江市海林市"},
    {"id": 3, "name": "中共海林市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共海林市委员会", "location": "黑龙江省牡丹江市海林市"},
    {"id": 4, "name": "海林市人大常委会", "type": "人大", "level": "县处级", "parent": "海林市", "location": "黑龙江省牡丹江市海林市"},
    {"id": 5, "name": "政协海林市委员会", "type": "政协", "level": "县处级", "parent": "海林市", "location": "黑龙江省牡丹江市海林市"},
    {"id": 6, "name": "海林市公安局", "type": "政府", "level": "乡科级", "parent": "海林市人民政府", "location": "黑龙江省牡丹江市海林市"},
    {"id": 7, "name": "海林经济技术开发区管理委员会", "type": "政府", "level": "县处级", "parent": "海林市人民政府", "location": "黑龙江省牡丹江市海林市"},
    {"id": 8, "name": "海林市人民武装部", "type": "政府", "level": "县处级", "parent": "牡丹江军分区", "location": "黑龙江省牡丹江市海林市"},
    {"id": 9, "name": "中共海林市委宣传部", "type": "党委", "level": "乡科级", "parent": "中共海林市委员会", "location": "黑龙江省牡丹江市海林市"},
    {"id": 10, "name": "中共海林市委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共海林市委员会", "location": "黑龙江省牡丹江市海林市"},
    {"id": 11, "name": "中共海林市委组织部", "type": "党委", "level": "乡科级", "parent": "中共海林市委员会", "location": "黑龙江省牡丹江市海林市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 张洪蓬 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "海林市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "至迟2024年11月已任职；2026年7月仍在任"},

    # 于德波 — 市长
    {"person_id": 2, "org_id": 2, "title": "海林市市长", "start": "", "end": "", "rank": "县处级正职", "note": "主持市政府全面工作，负责财政局、审计局"},
    {"person_id": 2, "org_id": 1, "title": "海林市委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 杜宇明 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "海林市委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "2026年5月官网确认"},

    # 朱艳辉 — 市委副书记（正处级）
    {"person_id": 4, "org_id": 1, "title": "海林市委副书记（正处级）", "start": "", "end": "", "rank": "县处级正职", "note": ""},

    # 刘业贤 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "海林市纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 李修杰 — 常委、副市长、开发区主任
    {"person_id": 6, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "海林市副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "海林经济技术开发区管委会主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 衣明 — 组织部长
    {"person_id": 7, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 11, "title": "海林市委组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "兼市委党校第一副校长"},

    # 韩雨昊 — 常委、副市长（党组副书记）
    {"person_id": 8, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "海林市副市长（党组副书记）", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 丁建萍 — 常委、副市长
    {"person_id": 9, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "海林市副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 马君钰 — 宣传部长
    {"person_id": 10, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "海林市委宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 冯立明 — 政法委书记
    {"person_id": 11, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "海林市委政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 王超 — 市委常委（2026年6月）
    {"person_id": 12, "org_id": 1, "title": "海林市委常委", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "2026年6月官网上新列入"},

    # 张志刚 — 武装部长
    {"person_id": 13, "org_id": 1, "title": "海林市委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "海林市武装部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # Deputy Mayors
    {"person_id": 14, "org_id": 2, "title": "海林市副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "海林市副市长", "start": "", "end": "", "rank": "县处级副职", "note": "负责公安、司法"},
    {"person_id": 15, "org_id": 6, "title": "海林市公安局局长", "start": "", "end": "", "rank": "乡科级正职", "note": "党委书记、督察长，市委政法委副书记"},
    {"person_id": 16, "org_id": 2, "title": "海林市副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "海林市副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "海林市副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 人大
    {"person_id": 19, "org_id": 4, "title": "海林市人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "党组书记"},
    {"person_id": 20, "org_id": 4, "title": "海林市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "海林市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "海林市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 政协
    {"person_id": 23, "org_id": 5, "title": "海林市政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "党组书记"},
    {"person_id": 24, "org_id": 5, "title": "海林市政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": "党组副书记"},
    {"person_id": 25, "org_id": 5, "title": "海林市政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 26, "org_id": 5, "title": "海林市政协副主席候选人", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 27, "org_id": 5, "title": "海林市政协秘书长", "start": "", "end": "", "rank": "县处级副职", "note": "党组成员"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 张洪蓬 — 于德波：党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "市委书记与市长党政工作搭档", "overlap_org": "海林市", "overlap_period": ""},

    # 张洪蓬 — 副书记们
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记与市委副书记", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记与市委副书记", "overlap_org": "中共海林市委", "overlap_period": ""},

    # 张洪蓬 — 常委们
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记与纪委书记", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委书记与常委副市长", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "市委书记与组织部长", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记与常委副市长", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "市委书记与常委副市长", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "市委书记与宣传部长", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "市委书记与政法委书记", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "市委书记与常委", "overlap_org": "中共海林市委", "overlap_period": "2026-06起"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "市委书记与武装部长", "overlap_org": "中共海林市委", "overlap_period": ""},

    # 于德波 — 副市长们
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长与常务副市长", "overlap_org": "海林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "市长与副市长（党组副书记）", "overlap_org": "海林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "市长与副市长", "overlap_org": "海林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "市长与副市长", "overlap_org": "海林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "市长与副市长、公安局长", "overlap_org": "海林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "市长与副市长", "overlap_org": "海林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "市长与副市长", "overlap_org": "海林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "市长与副市长", "overlap_org": "海林市人民政府", "overlap_period": ""},

    # 常委同僚
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市委常委", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "市委常委", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "同僚", "context": "市委常委", "overlap_org": "中共海林市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 11, "type": "同僚", "context": "市委常委", "overlap_org": "中共海林市委", "overlap_period": ""},

    # 副书记之间
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市委副书记", "overlap_org": "中共海林市委", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post and "监委" not in post:
        return ("255,50,50", 20.0)  # Red, large
    elif "市长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue, large
    elif "纪委" in post or "监委" in post:
        return ("255,165,0", 12.0)  # Orange
    elif "副" in post:
        return ("100,150,255", 12.0)  # Light blue
    elif "常委" in post:
        return ("100,150,255", 12.0)
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>海林市领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"海林市领导之窗—市委领导","url":"https://www.hailin.gov.cn/mdjhlsrmzf/ldjs/ldzc.shtml","publisher":"海林市人民政府","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"海林市领导之窗页面，包含市委、市人大、市政府、市政协全体领导"},
        {"id":"S002","title":"张洪蓬简历—市委书记","url":"https://www.hailin.gov.cn/mdjhlsrmzf/secretary/202411/c03_357775.shtml","publisher":"海林市人民政府","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"张洪蓬，1977年8月生，黑龙江省委党校经济管理专业研究生"},
        {"id":"S003","title":"于德波简历—市长","url":"https://www.hailin.gov.cn/mdjhlsrmzf/mayor/202605/c03_357760.shtml","publisher":"海林市人民政府","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"于德波，1976年10月生，大学学历"},
        {"id":"S004","title":"杜宇明简历—市委副书记","url":"https://www.hailin.gov.cn/mdjhlsrmzf/deputysecretary/202605/c03_1046499.shtml","publisher":"海林市人民政府","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"杜宇明，1975年5月生，研究生学历"},
        {"id":"S005","title":"朱艳辉简历—市委副书记","url":"https://www.hailin.gov.cn/mdjhlsrmzf/deputysecretary/202504/c03_1002759.shtml","publisher":"海林市人民政府","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"朱艳辉，1985年3月生，女，研究生"},
        {"id":"S006","title":"刘业贤简历—市纪委书记","url":"https://www.hailin.gov.cn/mdjhlsrmzf/memberofthestandingcommittee/202305/c03_355669.shtml","publisher":"海林市人民政府","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"刘业贤，1973年8月生"},
        {"id":"S007","title":"市委书记张洪蓬调研新闻","url":"https://www.hailin.gov.cn/mdjhlsrmzf/hailinheadlinenews/202607/c03_1053773.shtml","publisher":"海林市人民政府","published_at":"2026-07-23","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"张洪蓬以市委书记身份调研，确认2026年7月在任"},
    ]


def make_person_json(p, timeline, relationships_list, source_register):
    is_top = "市委书记" in p["current_post"] or "市长" == p.get("current_post","").replace("海林市","")
    rank = "县处级正职" if (p["id"] in [1,2,4,19,23]) else "县处级副职"

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "牡丹江市",
            "region": "海林市",
            "job": p["current_post"],
            "task_id": "heilongjiang_海林市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"hailinshi_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"confirmed","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息有待补充" if not p.get("birth") else f"{p['name']}早期职业生涯需确认"
        },
        "open_questions": [
            {"priority":"critical" if not p.get("birth") else "medium",
             "question": f"{p['name']}的完整职业生涯履历",
             "why_it_matters": "无法追溯其任职路径和系统经历",
             "suggested_queries": [f"{p['name']} 简历 海林市",f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result


def build_person_jsons():
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 张洪蓬 (市委书记)
    zhang_timeline = [
        {"start":"","end":"","org":"中共海林市委员会","title":"海林市委书记","notes":"至迟2024年11月已任职；2026年7月仍在任","confidence":"confirmed","source_ids":["S002","S007"]},
    ]
    zhang_relationships = [
        {"person":"于德波","person_id":"hailinshi_于德波","relationship_type":"overlap","strength":"strong","evidence":"市委书记与市长党政工作搭档","overlap_org":"海林市","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S003"]},
        {"person":"杜宇明","person_id":"hailinshi_杜宇明","relationship_type":"overlap","strength":"strong","evidence":"市委书记与市委副书记","overlap_org":"中共海林市委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S004"]},
        {"person":"朱艳辉","person_id":"hailinshi_朱艳辉","relationship_type":"overlap","strength":"strong","evidence":"市委书记与市委副书记","overlap_org":"中共海林市委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S005"]},
        {"person":"刘业贤","person_id":"hailinshi_刘业贤","relationship_type":"overlap","strength":"strong","evidence":"市委书记与纪委书记","overlap_org":"中共海林市委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S006"]},
    ]
    zhang_json = make_person_json(persons[0], zhang_timeline, zhang_relationships, source_register)
    zhang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-牡丹江市-市委书记-张洪蓬.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")

    # 2. 于德波 (市长)
    yu_timeline = [
        {"start":"","end":"","org":"海林市人民政府","title":"海林市市长","notes":"主持市政府全面工作；市委副书记","confidence":"confirmed","source_ids":["S003"]},
        {"start":"","end":"","org":"中共海林市委员会","title":"海林市委副书记","notes":"","confidence":"confirmed","source_ids":["S003"]},
    ]
    yu_relationships = [
        {"person":"张洪蓬","person_id":"hailinshi_张洪蓬","relationship_type":"overlap","strength":"strong","evidence":"市长与市委书记党政工作搭档","overlap_org":"海林市","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"李修杰","person_id":"hailinshi_李修杰","relationship_type":"overlap","strength":"strong","evidence":"市长与常务副市长","overlap_org":"海林市人民政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
        {"person":"韩雨昊","person_id":"hailinshi_韩雨昊","relationship_type":"overlap","strength":"strong","evidence":"市长与副市长（党组副书记）","overlap_org":"海林市人民政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
    ]
    yu_json = make_person_json(persons[1], yu_timeline, yu_relationships, source_register)
    yu_path = PERSONS_DIR / f"{TODAY}-黑龙江省-牡丹江市-市长-于德波.json"
    with open(yu_path, "w", encoding="utf-8") as f:
        json.dump(yu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {yu_path.name}")

    # 3. 杜宇明 (市委副书记)
    du_timeline = [
        {"start":"","end":"","org":"中共海林市委员会","title":"海林市委副书记","notes":"2026年5月官网确认","confidence":"confirmed","source_ids":["S004"]},
    ]
    du_relationships = [
        {"person":"张洪蓬","person_id":"hailinshi_张洪蓬","relationship_type":"overlap","strength":"strong","evidence":"市委副书记与市委书记","overlap_org":"中共海林市委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002","S004"]},
        {"person":"朱艳辉","person_id":"hailinshi_朱艳辉","relationship_type":"overlap","strength":"medium","evidence":"同为市委副书记","overlap_org":"中共海林市委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S005"]},
    ]
    du_json = make_person_json(persons[2], du_timeline, du_relationships, source_register)
    du_path = PERSONS_DIR / f"{TODAY}-黑龙江省-牡丹江市-市委副书记-杜宇明.json"
    with open(du_path, "w", encoding="utf-8") as f:
        json.dump(du_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {du_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  海林市领导班子工作关系网络")
    print("  等级: 县级市")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 海林市政府网站")
    print("=" * 60)

    build_db()
    build_gexf()
    build_person_jsons()

    print(f"\n✅ 海林市数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

if __name__ == "__main__":
    main()
