#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东风区 (Dongfeng District), 佳木斯市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_东风区
Level: 市辖区
Targets: 区委书记 & 区长

Data sources:
  - 佳木斯市东风区人民政府官方网站 领导之窗 https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml
    — complete leadership roster with names and roles (confirmed current as of page access date)
  - Wikipedia (zh.wikipedia.org/wiki/东风区) — district overview, 区委书记 recorded as 周政治 (outdated; 张义利 now current)
  - 佳木斯市人民政府官网 leadership listing

Confidence notes:
  - Leadership roster: confirmed via official 东风区 government website
  - 张义利 (区委书记) and 钟华 (区长): confirmed with portrait and listing on official site
  - Full party committee standing committee and government deputy head list: confirmed from official site
  - Detailed biographies, career timelines, birth years, education: UNVERIFIED — official site provides names/roles only
  - Predecessor information: Wikipedia shows 周政治 as predecessor party secretary; no predecessor info for 钟华
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(STAGING, "..", ".."))
SLUG = "东风区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

# ── Helpers ────────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(role):
    if role is None:
        role = ""
    if "书记" in role and "纪委" not in role and "副书记" not in role:
        return "220,30,30"
    if "区长" in role and "副" not in role:
        return "40,100,220"
    if "副区长" in role:
        return "40,140,220"
    if "纪委书记" in role:
        return "180,130,50"
    if "人大" in role:
        return "220,160,40"
    if "政协" in role:
        return "200,150,40"
    if "副书记" in role:
        return "180,60,180"
    if "部长" in role or "政法委" in role:
        return "120,120,120"
    return "160,160,160"

def person_size(role):
    if role is None:
        role = ""
    if "区委书记" in role:
        return "20.0"
    if "区长" in role and "副" not in role:
        return "18.0"
    if "副书记" in role:
        return "16.0"
    if "人大" in role or "政协" in role:
        return "14.0"
    if "常委" in role:
        return "14.0"
    return "12.0"

def org_color(org_type):
    if org_type is None:
        org_type = ""
    if "党委" in org_type:
        return "200,60,60"
    if "政府" in org_type or "公安" in org_type:
        return "60,100,200"
    if "人大" in org_type:
        return "200,150,40"
    if "政协" in org_type:
        return "180,130,40"
    if "纪委" in org_type:
        return "160,120,40"
    if "党委部门" in org_type:
        return "200,80,80"
    return "120,120,120"


# =========================================================================
# DATA
# =========================================================================

# ── PERSONS ──
# [id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start,
#  current_post, current_org, source]

PERSONS = [
    # ═══════════════════════════════════════════════════════════════════
    # TOP LEADERS
    # ═══════════════════════════════════════════════════════════════════

    # 张义利 — 东风区委书记
    # Confirmed via official 东风区 government website leadership page (portrait + title)
    ["jiamusi_dongfeng_zhang_yili", "张义利", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "东风区委书记",
     "中共佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委书记 via official leadership page)"],

    # 钟华 — 东风区委副书记、区长
    # Confirmed via official website — listed as both 区委副书记 and 区长
    ["jiamusi_dongfeng_zhong_hua", "钟华", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "东风区委副书记、区长",
     "佳木斯市东风区人民政府",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区长 via official leadership page)"],

    # 孙照丰 — 东风区委副书记（专职）
    ["jiamusi_dongfeng_sun_zhaofeng", "孙照丰", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "东风区委副书记（专职）",
     "中共佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委副书记 via official leadership page)"],

    # ═══════════════════════════════════════════════════════════════════
    # 区委常委
    # ═══════════════════════════════════════════════════════════════════

    # 徐鹤钧 — 区委常委 (likely 纪委书记 or 组织部长 or similar)
    ["jiamusi_dongfeng_xu_hejun", "徐鹤钧", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区委常委",
     "中共佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委常委)"],

    # 杨德松 — 区委常委、副区长
    ["jiamusi_dongfeng_yang_desong", "杨德松", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区委常委、副区长",
     "佳木斯市东风区人民政府",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委常委、副区长)"],

    # 吕钢 — 区委常委
    ["jiamusi_dongfeng_lv_gang", "吕钢", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区委常委",
     "中共佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委常委)"],

    # 李晨 — 区委常委
    ["jiamusi_dongfeng_li_chen", "李晨", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区委常委",
     "中共佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委常委)"],

    # 王学礼 — 区委常委、副区长
    ["jiamusi_dongfeng_wang_xueli", "王学礼", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区委常委、副区长",
     "佳木斯市东风区人民政府",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委常委、副区长)"],

    # 杨悦 — 区委常委
    ["jiamusi_dongfeng_yang_yue", "杨悦", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区委常委",
     "中共佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区委常委)"],

    # ═══════════════════════════════════════════════════════════════════
    # 副区长（非常委）
    # ═══════════════════════════════════════════════════════════════════

    # 周建军 — 副区长
    ["jiamusi_dongfeng_zhou_jianjun", "周建军", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区副区长",
     "佳木斯市东风区人民政府",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 副区长)"],

    # 马智博 — 副区长
    ["jiamusi_dongfeng_ma_zhibo", "马智博", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区副区长",
     "佳木斯市东风区人民政府",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 副区长)"],

    # 张爱军 — 副区长
    ["jiamusi_dongfeng_zhang_aijun", "张爱军", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区副区长",
     "佳木斯市东风区人民政府",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 副区长)"],

    # 史皓同 — 副区长
    ["jiamusi_dongfeng_shi_haotong", "史皓同", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区副区长",
     "佳木斯市东风区人民政府",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 副区长)"],

    # ═══════════════════════════════════════════════════════════════════
    # 人大
    # ═══════════════════════════════════════════════════════════════════

    # 关雨龙 — 区人大常委会主任
    ["jiamusi_dongfeng_guan_yulong", "关雨龙", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区人大常委会主任",
     "佳木斯市东风区人民代表大会常务委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区人大常委会主任)"],

    # 刘三威 — 区人大常委会副主任
    ["jiamusi_dongfeng_liu_sanwei", "刘三威", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区人大常委会副主任",
     "佳木斯市东风区人民代表大会常务委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区人大常委会副主任)"],

    # 魏玉玺 — 区人大常委会副主任
    ["jiamusi_dongfeng_wei_yuxi", "魏玉玺", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区人大常委会副主任",
     "佳木斯市东风区人民代表大会常务委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区人大常委会副主任)"],

    # 吴佳飞 — 区人大常委会副主任
    ["jiamusi_dongfeng_wu_jiafei", "吴佳飞", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区人大常委会副主任",
     "佳木斯市东风区人民代表大会常务委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区人大常委会副主任)"],

    # 王志勇 — 区人大常委会副主任
    ["jiamusi_dongfeng_wang_zhiyong", "王志勇", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区人大常委会副主任",
     "佳木斯市东风区人民代表大会常务委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区人大常委会副主任)"],

    # ═══════════════════════════════════════════════════════════════════
    # 政协
    # ═══════════════════════════════════════════════════════════════════

    # 杨金才 — 区政协主席
    ["jiamusi_dongfeng_yang_jincai", "杨金才", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区政协主席",
     "中国人民政治协商会议佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区政协主席)"],

    # 李宏博 — 区政协副主席
    ["jiamusi_dongfeng_li_hongbo", "李宏博", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "东风区政协副主席",
     "中国人民政治协商会议佳木斯市东风区委员会",
     "https://www.jmsdf.gov.cn/dfq/c100119/ldzc.shtml (confirmed as 区政协副主席)"],

    # ═══════════════════════════════════════════════════════════════════
    # 前任
    # ═══════════════════════════════════════════════════════════════════

    # 周政治 — 前任东风区委书记（Wikipedia记载，更新至2023年11月）
    ["jiamusi_dongfeng_zhou_zhengzhi", "周政治", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原东风区委书记，张义利前任）",
     "中共佳木斯市东风区委员会（原）",
     "https://zh.wikipedia.org/wiki/东风区 (confirmed by Wikipedia infobox, revision 2023-11-20)"],
]

# ── ORGANIZATIONS ──
# [id, name, type, level, parent, location]

ORGANIZATIONS = [
    ["jiamusi_dongfeng_party_committee", "中共佳木斯市东风区委员会", "党委", "县处级",
     "中共佳木斯市委", "黑龙江省佳木斯市东风区"],
    ["jiamusi_dongfeng_gov", "佳木斯市东风区人民政府", "政府", "县处级",
     "佳木斯市人民政府", "黑龙江省佳木斯市东风区"],
    ["jiamusi_dongfeng_people_congress", "佳木斯市东风区人民代表大会常务委员会", "人大", "县处级",
     "佳木斯市人民代表大会常务委员会", "黑龙江省佳木斯市东风区"],
    ["jiamusi_dongfeng_cppcc", "中国人民政治协商会议佳木斯市东风区委员会", "政协", "县处级",
     "中国人民政治协商会议佳木斯市委员会", "黑龙江省佳木斯市东风区"],
    ["jiamusi_dongfeng_discipline", "中共佳木斯市东风区纪律检查委员会", "纪委", "县处级",
     "中共佳木斯市纪委", "黑龙江省佳木斯市东风区"],
    ["jiamusi_dongfeng_org_dept", "中共佳木斯市东风区委组织部", "党委部门", "正科级",
     "中共佳木斯市东风区委员会", "黑龙江省佳木斯市东风区"],
    ["jiamusi_dongfeng_propaganda_dept", "中共佳木斯市东风区委宣传部", "党委部门", "正科级",
     "中共佳木斯市东风区委员会", "黑龙江省佳木斯市东风区"],
    ["jiamusi_dongfeng_politics_law_committee", "中共佳木斯市东风区委政法委员会", "党委部门", "正科级",
     "中共佳木斯市东风区委员会", "黑龙江省佳木斯市东风区"],
    # 上级组织
    ["jiamusi_city_party_committee", "中共佳木斯市委员会", "党委", "地厅级",
     "中共黑龙江省委", "黑龙江省佳木斯市"],
    ["jiamusi_city_gov", "佳木斯市人民政府", "政府", "地厅级",
     "黑龙江省人民政府", "黑龙江省佳木斯市"],
]

# ── POSITIONS ──
# [person_id, org_id, title, start, end, rank, note]

POSITIONS = [
    # 张义利 — 区委书记
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_party_committee",
     "东风区委书记", "待查", "present", "县处级",
     "confirmed via official 东风区 leadership page; successor to 周政治"],

    # 钟华 — 区长、区委副书记
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_gov",
     "东风区区长", "待查", "present", "县处级",
     "confirmed via official 东风区 leadership page"],
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_party_committee",
     "东风区委副书记", "待查", "present", "县处级", ""],

    # 孙照丰 — 专职副书记
    ["jiamusi_dongfeng_sun_zhaofeng", "jiamusi_dongfeng_party_committee",
     "东风区委副书记（专职）", "待查", "present", "县处级",
     "confirmed via official 东风区 leadership page"],

    # 徐鹤钧 — 区委常委
    ["jiamusi_dongfeng_xu_hejun", "jiamusi_dongfeng_party_committee",
     "东风区委常委", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page; specific portfolio unknown"],

    # 杨德松 — 区委常委、副区长
    ["jiamusi_dongfeng_yang_desong", "jiamusi_dongfeng_party_committee",
     "东风区委常委", "待查", "present", "副县处级", ""],
    ["jiamusi_dongfeng_yang_desong", "jiamusi_dongfeng_gov",
     "东风区副区长", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 吕钢 — 区委常委
    ["jiamusi_dongfeng_lv_gang", "jiamusi_dongfeng_party_committee",
     "东风区委常委", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 李晨 — 区委常委
    ["jiamusi_dongfeng_li_chen", "jiamusi_dongfeng_party_committee",
     "东风区委常委", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 王学礼 — 区委常委、副区长
    ["jiamusi_dongfeng_wang_xueli", "jiamusi_dongfeng_party_committee",
     "东风区委常委", "待查", "present", "副县处级", ""],
    ["jiamusi_dongfeng_wang_xueli", "jiamusi_dongfeng_gov",
     "东风区副区长", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 杨悦 — 区委常委
    ["jiamusi_dongfeng_yang_yue", "jiamusi_dongfeng_party_committee",
     "东风区委常委", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 副区长（非常委）
    ["jiamusi_dongfeng_zhou_jianjun", "jiamusi_dongfeng_gov",
     "东风区副区长", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_ma_zhibo", "jiamusi_dongfeng_gov",
     "东风区副区长", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_zhang_aijun", "jiamusi_dongfeng_gov",
     "东风区副区长", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_shi_haotong", "jiamusi_dongfeng_gov",
     "东风区副区长", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 人大
    ["jiamusi_dongfeng_guan_yulong", "jiamusi_dongfeng_people_congress",
     "东风区人大常委会主任", "待查", "present", "县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_liu_sanwei", "jiamusi_dongfeng_people_congress",
     "东风区人大常委会副主任", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_wei_yuxi", "jiamusi_dongfeng_people_congress",
     "东风区人大常委会副主任", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_wu_jiafei", "jiamusi_dongfeng_people_congress",
     "东风区人大常委会副主任", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_wang_zhiyong", "jiamusi_dongfeng_people_congress",
     "东风区人大常委会副主任", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 政协
    ["jiamusi_dongfeng_yang_jincai", "jiamusi_dongfeng_cppcc",
     "东风区政协主席", "待查", "present", "县处级",
     "confirmed via official 东风区 leadership page"],

    ["jiamusi_dongfeng_li_hongbo", "jiamusi_dongfeng_cppcc",
     "东风区政协副主席", "待查", "present", "副县处级",
     "confirmed via official 东风区 leadership page"],

    # 前任
    ["jiamusi_dongfeng_zhou_zhengzhi", "jiamusi_dongfeng_party_committee",
     "东风区委书记（原）", "待查", "待查", "县处级",
     "Wikipedia shows 周政治 as 区委书记 (revision 2023-11-20); succeeded by 张义利"],
]

# ── RELATIONSHIPS ──
# [person_a, person_b, type, context, overlap_org, overlap_period]

RELATIONSHIPS = [
    # 核心工作关系：书记-区长
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_zhong_hua",
     "superior_subordinate",
     "区委书记与区长搭档",
     "中共佳木斯市东风区委员会 / 佳木斯市东风区人民政府",
     "待查—present"],

    # 书记-专职副书记
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_sun_zhaofeng",
     "superior_subordinate",
     "区委书记与专职副书记",
     "中共佳木斯市东风区委员会",
     "待查—present"],

    # 区长-专职副书记
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_sun_zhaofeng",
     "overlap",
     "区长与专职副书记同属区委领导班子",
     "中共佳木斯市东风区委员会",
     "待查—present"],

    # 书记-常委会成员
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_xu_hejun",
     "overlap",
     "区委书记与区委常委在区委常委会共事",
     "中共佳木斯市东风区委员会",
     "待查—present"],
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_yang_desong",
     "overlap",
     "区委书记与区委常委在区委常委会共事",
     "中共佳木斯市东风区委员会",
     "待查—present"],
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_lv_gang",
     "overlap",
     "区委书记与区委常委在区委常委会共事",
     "中共佳木斯市东风区委员会",
     "待查—present"],
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_li_chen",
     "overlap",
     "区委书记与区委常委在区委常委会共事",
     "中共佳木斯市东风区委员会",
     "待查—present"],
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_wang_xueli",
     "overlap",
     "区委书记与区委常委在区委常委会共事",
     "中共佳木斯市东风区委员会",
     "待查—present"],
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_yang_yue",
     "overlap",
     "区委书记与区委常委在区委常委会共事",
     "中共佳木斯市东风区委员会",
     "待查—present"],

    # 区长-副区长
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_yang_desong",
     "superior_subordinate",
     "区长与副区长在区政府班子共事",
     "佳木斯市东风区人民政府",
     "待查—present"],
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_wang_xueli",
     "superior_subordinate",
     "区长与副区长在区政府班子共事",
     "佳木斯市东风区人民政府",
     "待查—present"],
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_zhou_jianjun",
     "superior_subordinate",
     "区长与副区长在区政府班子共事",
     "佳木斯市东风区人民政府",
     "待查—present"],
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_ma_zhibo",
     "superior_subordinate",
     "区长与副区长在区政府班子共事",
     "佳木斯市东风区人民政府",
     "待查—present"],
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_zhang_aijun",
     "superior_subordinate",
     "区长与副区长在区政府班子共事",
     "佳木斯市东风区人民政府",
     "待查—present"],
    ["jiamusi_dongfeng_zhong_hua", "jiamusi_dongfeng_shi_haotong",
     "superior_subordinate",
     "区长与副区长在区政府班子共事",
     "佳木斯市东风区人民政府",
     "待查—present"],

    # 书记-人大主任
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_guan_yulong",
     "overlap",
     "区委书记和人大常委会主任在区四套班子中协作",
     "中共佳木斯市东风区委员会 / 佳木斯市东风区人民代表大会常务委员会",
     "待查—present"],

    # 书记-政协主席
    ["jiamusi_dongfeng_zhang_yili", "jiamusi_dongfeng_yang_jincai",
     "overlap",
     "区委书记和政协主席在区四套班子中协作",
     "中共佳木斯市东风区委员会 / 中国人民政治协商会议佳木斯市东风区委员会",
     "待查—present"],

    # 前任-现任书记
    ["jiamusi_dongfeng_zhou_zhengzhi", "jiamusi_dongfeng_zhang_yili",
     "predecessor_successor",
     "周政治为张义利前任区委书记",
     "中共佳木斯市东风区委员会",
     "任职时间前后承接"],
]


# =========================================================================
# FUNCTIONS
# =========================================================================

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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


def build_slug(name):
    return name.lower().replace(" ", "_")


# =========================================================================
# MAIN
# =========================================================================

def main():
    # Build ordinal ID maps
    person_map = {}
    for i, p in enumerate(PERSONS):
        person_map[p[0]] = i + 1

    org_map = {}
    for i, o in enumerate(ORGANIZATIONS):
        org_map[o[0]] = i + 1

    # ── 1. SQLite ──────────────────────────────────────────────────────
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    for pid_str, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source in PERSONS:
        conn.execute(
            "INSERT INTO persons (name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        )

    # Insert organizations
    for oid_str, name, org_type, level, parent, location in ORGANIZATIONS:
        conn.execute(
            "INSERT INTO organizations (name, type, level, parent, location) VALUES (?,?,?,?,?)",
            (name, org_type, level, parent, location)
        )

    # Insert positions
    for pid_str, oid_str, title, start, end_date, rank, note in POSITIONS:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (person_map[pid_str], org_map[oid_str], title, start, end_date, rank, note)
        )

    # Insert relationships
    for a_str, b_str, rel_type, context, overlap_org, overlap_period in RELATIONSHIPS:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (person_map[a_str], person_map[b_str], rel_type, context, overlap_org, overlap_period)
        )

    conn.commit()
    conn.close()
    print(f"✅ SQLite database created: {DB_PATH}")
    print(f"   Persons: {len(PERSONS)}, Organizations: {len(ORGANIZATIONS)}, Positions: {len(POSITIONS)}, Relationships: {len(RELATIONSHIPS)}")

    # ── 2. GEXF ────────────────────────────────────────────────────────
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Opencode Research Agent</creator>')
    lines.append(f'    <description>东风区（佳木斯市）领导班子工作关系网络 — {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for i, (pid_str, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) in enumerate(PERSONS):
        uid = i + 1
        c = person_color(current_post)
        sz = person_size(current_post)
        lines.append(f'      <node id="p{uid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(current_post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(current_org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(source[:100])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for i, (oid_str, name, org_type, level, parent, location) in enumerate(ORGANIZATIONS):
        uid = len(PERSONS) + i + 1
        c = org_color(org_type)
        lines.append(f'      <node id="o{uid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(org_type)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(level)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pid_str, oid_str, title, start, end_date, rank, note in POSITIONS:
        eid += 1
        person_num = person_map[pid_str]
        org_num = len(PERSONS) + org_map[oid_str]
        lines.append(f'      <edge id="e{eid}" source="p{person_num}" target="o{org_num}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note[:100])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship)
    for a_str, b_str, rel_type, context, overlap_org, overlap_period in RELATIONSHIPS:
        eid += 1
        person_a_num = person_map[a_str]
        person_b_num = person_map[b_str]
        lines.append(f'      <edge id="e{eid}" source="p{person_a_num}" target="p{person_b_num}" label="{esc(context)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel_type)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(overlap_org)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")

    print(f"\n✅ Build complete for {SLUG}")


if __name__ == "__main__":
    import sqlite3
    main()
