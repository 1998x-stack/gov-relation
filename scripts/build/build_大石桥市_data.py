#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大石桥市 (营口市，辽宁省).

Investigation date: 2026-08-06
Task ID: liaoning_大石桥市
Level: 县级市
Parent city: 营口市
Targets: 市委书记 & 市长

Research status: PRIMARY SOURCE ACCESS (official city portal, partial roster)
  - 大石桥市人民政府门户 (www.dsq.gov.cn): 仅 http 可访问（https 不可达），领导之窗 / 镁都要闻 /
    头条新闻 官方一手报道充分；市政府领导班子简历、市党代会/市委常委会会议报道确认职务。
  - 现任市委书记 徐荣利、市委副书记/市长 衣冠鹏 已通过官方一手信源确认；
    中国共产党大石桥市第八次代表大会（2026-07-22/24 换届）选举八届市委，徐荣利代表七届市委作报告并连任书记。
  - 市政府领导之窗公布市政府领导班子全名单与出生年月/学历/入党情况（衣冠鹏、张雨、金鹏、张滔、李洋、冯君成、林驷源）。
  - Exa / Baidu / Bing / Sogou 检索普遍受限，市委书记徐荣利与多数市委常委的出生/籍贯/学历等履历细节缺失，
    部分常委角色分工（纪委书记/宣传部长/政法委书记/统战部长/组织部长待细分）未完全确认，按证据分级标注。

Confirmed current officeholders (as of 2026-08-06):
   - 市委书记: 徐荣利（多次官方调研/党代会/常委会报道；2026-07-22 代表七届市委作报告、07-24 八代会闭幕、07-29 常委会讲话）
   - 市委副书记、市长: 衣冠鹏（市政府党组书记，主持市政府全面工作；官方简历 1978-09 生、大学学历；2026 年多场市政府会议）
   - 市委常委、常务副市长: 张雨（女，1981-04，在职研究生；市政府党组副书记）
   - 市委常委、副市长(挂职): 金鹏（1985-11，研究生/工程硕士）
   - 市委常委、组织部部长: 柳地润（2026-06-29 两优一先宣读表彰决定）
   - 副市长: 张滔（1976-04，公安局党组书记/局长）、冯君成（1976-09）、李洋（1987-06）、林驷源（1990-05，满族）
   - 市人大常委会党组书记、主任: 代天轶
   - 市政协党组书记、主席: 张燕
   - 营口大石桥经济开发区管委会主任: 李晗（七届市委常委会多次出席）

其他市委常委（角色分工待核）: 李志刚、张龙、孙坤衍、韩娜、蔺智君、王志栋
  （八届党代会各场会议执行主席 / 市领导名单，但具体职务未在可用页面中细分）

Predecessor timeline (piecemeal / unverified):
   - 市委书记: 徐荣利 延续"七届→八届"（八届 2026-07-24 成立），任书记前来自何处及前任书记去向待核
   - 市长: 衣冠鹏 为现任市长（土政），前任市长及任期起始待核

Cross-region / context:
   - 大石桥市 系营口市代管的县级市，别称"中国镁都"，以镁质耐材产业著称
   - 与营口市辖站前、老边、西市、鲅鱼圈等区同属营口市委干部管理体系
   - 营口市委组织部任前公示、市—县(市)干部交流为区域干部流动主要渠道

Confidence policy: 当前角色 confirmed（官方一手），身份(出生/籍贯/学历) 对政府班子为 confirmed（简历公开），
  对市委书记徐荣利、多数常委为 unverified（官方报道确认职务但未给简历）。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (DB I/O is handled by gov_relation.runner via sqlite3)
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "大石桥市"
AS_OF = "2026-08-06"

_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────
# 主要一手来源: 大石桥市政府门户（http://www.dsq.gov.cn/）领导之窗/镁都要闻/头条新闻
persons = [
    # ── 市委（核心） ──
    {"id": 1, "name": "徐荣利", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260723/902177bd-5736-483f-a0a7-9992c77e9c2a.html (2026-07-22 八次党代会作报告)"},
    {"id": 2, "name": "衣冠鹏", "gender": "男", "ethnicity": "汉族", "birth": "1978-09", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "大石桥市人民政府",
     "source": "http://www.dsq.gov.cn/010/011001/011001001/leader.html (大石桥市政府领导之窗/市长简历)"},
    # ── 市委常委 ──
    {"id": 3, "name": "张雨", "gender": "女", "ethnicity": "汉族", "birth": "1981-04", "birthplace": "",
     "education": "在职研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市政府党组副书记、副市长（常务）", "current_org": "大石桥市人民政府",
     "source": "http://www.dsq.gov.cn/010/011003/011003002/leader.html (政府领导·张雨)"},
    {"id": 4, "name": "金鹏", "gender": "男", "ethnicity": "汉族", "birth": "1985-11", "birthplace": "",
     "education": "研究生学历(工程硕士)", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长（挂职）", "current_org": "大石桥市人民政府",
     "source": "http://www.dsq.gov.cn/010/011003/011003004/leader.html (政府领导·金鹏)"},
    {"id": 5, "name": "柳地润", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260630/8edbc985-adc9-4faa-86ee-938196c6a4f0.html (2026-06-29 两优一先宣读表彰决定)"},
    # ── 市委常委（角色分工待核） ──
    {"id": 6, "name": "李志刚", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260727/58b7fa69-637b-4997-9216-9d68ca54d9ee.html (八代会闭幕执行主席)"},
    {"id": 7, "name": "张龙", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260727/58b7fa69-637b-4997-9216-9d68ca54d9ee.html (八代会闭幕执行主席)"},
    {"id": 8, "name": "王志栋", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260723/902177bd-5736-483f-a0a7-9992c77e9c2a.html (八代会开幕执行主席)"},
    {"id": 9, "name": "韩娜", "gender": "女", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260723/902177bd-5736-483f-a0a7-9992c77e9c2a.html (八代会开幕执行主席)"},
    {"id": 10, "name": "蔺智君", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260727/58b7fa69-637b-4997-9216-9d68ca54d9ee.html (八代会闭幕执行主席)"},
    {"id": 11, "name": "孙坤衍", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中国共产党大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260724/c7de6a4b-4cfd-4acc-a118-a02527749607.html (八代会二全体会议执行主席)"},
    # ── 市政府（副市长） ──（公安局局长兼副市长）
    {"id": 12, "name": "张滔", "gender": "男", "ethnicity": "汉族", "birth": "1976-04", "birthplace": "",
     "education": "在职大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长、市公安局党委书记、局长", "current_org": "大石桥市公安局",
     "source": "http://www.dsq.gov.cn/010/011003/011003001/leader.html (政府领导·张滔)"},
    {"id": 13, "name": "冯君成", "gender": "男", "ethnicity": "汉族", "birth": "1976-09", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大石桥市人民政府",
     "source": "http://www.dsq.gov.cn/010/011003/011003003/leader.html (政府领导·冯君成)"},
    {"id": 14, "name": "李洋", "gender": "男", "ethnicity": "汉族", "birth": "1987-06", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大石桥市人民政府",
     "source": "http://www.dsq.gov.cn/010/011003/011003005/leader.html (政府领导·李洋)"},
    {"id": 15, "name": "林驷源", "gender": "男", "ethnicity": "满族", "birth": "1990-05", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "大石桥市人民政府",
     "source": "http://www.dsq.gov.cn/010/011003/011003007/leader.html (政府领导·林驷源)"},
    # ── 四大班子 ──
    {"id": 16, "name": "代天轶", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市人大常委会党组书记、主任", "current_org": "大石桥市人民代表大会常务委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260730/b4d30f2d-0277-433d-b125-fd21802c328e.html (2026-07-29 常委会扩大会议)"},
    {"id": 17, "name": "张燕", "gender": "女", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "", "work_start": "",
     "current_post": "市政协党组书记、主席", "current_org": "中国人民政治协商会议大石桥市委员会",
     "source": "http://www.dsq.gov.cn/003/003001/20260730/b4d30f2d-0277-433d-b125-fd21802c328e.html (2026-07-29 常委会扩大会议)"},
    # ── 开发区 ──
    {"id": 18, "name": "李晗", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "营口大石桥经济开发区管委会主任", "current_org": "营口大石桥经济开发区管委会",
     "source": "http://www.dsq.gov.cn/003/003001/20260629/26632640-9fc8-47ed-b95e-7b4c382e7104.html (2026-06-26 常委会329)"},
]

organizations = [
    {"id": 1, "name": "中国共产党大石桥市委员会", "type": "党委", "level": "县处级(县级市)", "parent": "中共营口市委", "location": "辽宁省营口市大石桥市"},
    {"id": 2, "name": "大石桥市人民政府", "type": "政府", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市大石桥市"},
    {"id": 3, "name": "大石桥市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "大石桥市", "location": "辽宁省营口市大石桥市"},
    {"id": 4, "name": "中国人民政治协商会议大石桥市委员会", "type": "政协", "level": "县处级", "parent": "大石桥市", "location": "辽宁省营口市大石桥市"},
    {"id": 5, "name": "中国共产党大石桥市纪律检查委员会/大石桥市监察委员会", "type": "纪委", "level": "县处级", "parent": "中共营口市纪委", "location": "辽宁省营口市大石桥市"},
    {"id": 6, "name": "大石桥市公安局", "type": "政府", "level": "县处级", "parent": "大石桥市人民政府", "location": "辽宁省营口市大石桥市"},
    {"id": 7, "name": "营口大石桥经济开发区管委会", "type": "开发区", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市大石桥市"},
    {"id": 8, "name": "大石桥市人民法院", "type": "法院", "level": "县处级", "parent": "营口市中级人民法院", "location": "辽宁省营口市大石桥市"},
    {"id": 9, "name": "大石桥市人民检察院", "type": "检察院", "level": "县处级", "parent": "营口市人民检察院", "location": "辽宁省营口市大石桥市"},
    {"id": 10, "name": "中国共产党营口市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委", "location": "辽宁省营口市"},
]

positions = [
    # 徐荣利(1) 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "<=2026", "end_date": "present", "rank": "县处级正职(副厅级常规)",
     "note": "2026-07-22 代表中共大石桥市第七届委员会在八次党代会作工作报告；2026-07-29 八届市委常委会（扩大）会议主持并讲话"},
    {"person_id": 1, "org_id": 1, "title": "市委委员、市委常委", "start_date": "~2021-2026", "end_date": "present", "rank": "县处级",
     "note": "七届市委任期内任书记并过渡至八届（任期可见为独立一任）"},
    # 衣冠鹏(2) 市长
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "unknown", "end_date": "present", "rank": "县处级正职",
     "note": "主持市政府全面工作，负责审计等方面工作，分管市审计局；官网简历（市政府领导·衣冠鹏）"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "市长党内职务，2026-07-22 八次党代会执行主席之一"},
    # 张雨(3) 常务副市长
    {"person_id": 3, "org_id": 2, "title": "市委常委、市政府党组副书记、副市长（常务）", "start_date": "unknown", "end_date": "present", "rank": "县处级副职",
     "note": "2026-07-22 八次党代会第一次全体会议执行主席之一"},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    # 金鹏(4)
    {"person_id": 4, "org_id": 2, "title": "市委常委、副市长（挂职）", "start_date": "unknown", "end_date": "present", "rank": "县处级副职",
     "note": "研究生(工程硕士)；2026-07-23 八代会第二次全体会议执行主席之一；2026-06-03 陪同徐荣利检查高考准备工作"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    # 柳地润(5) 组织部长
    {"person_id": 5, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "2026-06-29 大石桥市两优一先表彰大会宣读《中共大石桥市委关于表彰优秀共产党员、优秀党务工作者、先进基层党组织的决定》"},
    # 常委（角色待核）
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "八次党代会闭幕会议执行主席"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "八次党代会闭幕会议执行主席"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "八次党代会开幕会议执行主席"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "八次党代会开幕会议执行主席"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "八次党代会闭幕会议执行主席"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "八次党代会第二次全体会议执行主席；2026-07-27 八一走访随行"},
    # 政府（副市长）
    {"person_id": 12, "org_id": 6, "title": "市公安局党委书记、局长", "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "大石桥市人民政府党组成员、副市长，公安局党组书记、局长（官网王玉龙简历）"},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "大石桥市政府党组成员、副市长（官网）"},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "大石桥市政府党组成员、副市长（官网）"},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "大石桥市政府党组成员、副市长（官网，满族）"},
    # 四大班子
    {"person_id": 16, "org_id": 3, "title": "市人大常委会党组书记、主任", "start_date": "unknown", "end_date": "present", "rank": "县处级正职",
     "note": "2026-07-29 常委会（扩大）会议出席；2026-07-27 按市委部署活动"},
    {"person_id": 17, "org_id": 4, "title": "市政协党组书记、主席", "start_date": "unknown", "end_date": "present", "rank": "县处级正职",
     "note": "2026-07-29 常委会（扩大）会议出席"},
    # 开发区
    {"person_id": 18, "org_id": 7, "title": "营口大石桥经济开发区管委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "2026-06-26 及多次市委常委会会议出席"},
]

relationships = [
    # 核心党政搭档
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "市委书记（徐荣利）与市长（衣冠鹏，兼市委副书记）——党政一把手搭班",
     "overlap_org": "大石桥市", "overlap_period": "2026-", "confidence": "confirmed"},
    # 四大班子互关
    {"person_a": 1, "person_b": 16, "type": "co_leadership", "context": "市委书记与市人大常委会主任（常委会扩大会议同台）",
     "overlap_org": "大石桥市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 17, "type": "co_leadership", "context": "市委书记与市政协主席（常委会扩大会议同台）",
     "overlap_org": "大石桥市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "co_leadership", "context": "市长与市人大主任（人大/政府分工）", "overlap_org": "大石桥市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "co_leadership", "context": "市长与市政协主席（市政府/政协联动）", "overlap_org": "大石桥市", "overlap_period": "2026-", "confidence": "confirmed"},
    # 市委班子：副书记/组织部/各常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与常务副市长（政府党组副书记，党政班子）", "overlap_org": "大石桥市委", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与组织部部长（党建、选人用人、换届）", "overlap_org": "大石桥市委组织部", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "co_leadership", "context": "书记与挂职副市长（2026-06-03 高考检查同行）", "overlap_org": "大石桥市", "overlap_period": "2026-06", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "co_leadership", "context": "书记与常委（八次党代会执行主席同台）", "overlap_org": "大石桥市委", "overlap_period": "2026-07", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "co_leadership", "context": "书记与常委（八代会执行主席、八一走访同台）", "overlap_org": "大石桥市委", "overlap_period": "2026-07", "confidence": "confirmed"},
    # 政府班子互为同事
    {"person_a": 2, "person_b": 3, "type": "co_leadership", "context": "市长与常务副市长（市政府班子）", "overlap_org": "大石桥市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与公安局局长/副市长（公安、社会稳定）", "overlap_org": "大石桥市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "co_leadership", "context": "常务副市长与挂职常委/副市长（政府班子）", "overlap_org": "大石桥市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 12, "person_b": 13, "type": "co_leadership", "context": "副市长同班子", "overlap_org": "大石桥市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 14, "person_b": 15, "type": "co_leadership", "context": "副市长同班子", "overlap_org": "大石桥市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
]


# ── Person JSONs ────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for the two core leaders (市委书记 & 市长)."""

    xu = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "营口市", "region": "大石桥市",
                                "job": "市委书记", "task_id": "liaoning_大石桥市", "time_focus": "2025-2026"},
        "identity": {
            "person_id": "yingkou_dashiqiao_xurongli",
            "name": "徐荣利",
            "aliases": [],
            "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "徐荣利_unknown", "name_birthplace": "徐荣利_unknown",
                            "official_profile_url": "http://www.dsq.gov.cn/003/003001/20260723/902177bd-5736-483f-a0a7-9992c77e9c2a.html"},
        },
        "current_status": {"current_post": "市委书记", "current_org": "中国共产党大石桥市委员会",
                           "administrative_rank": "县处级正职(副厅级常规)", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002"]},
        "career_timeline": [
            {"start": "~2021-2026", "end": "present", "org": "中共大石桥市委员会", "title": "市委书记（七届→八届）",
             "level": "县处级", "location": "大石桥市", "system": "party", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2026-07-22 代表七届市委作工作报告；2026-07-24 八次党代会选举产生八届市委（连任）；2026-07-29 八届市委常委会（扩大）会议主持并讲话；多场常委会主持",
             "confidence": "confirmed", "source_ids": ["S001", "S002", "S004"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任大石桥市委书记之前的履历（出生、籍贯、学历、入党、参加工作时间、此前职务）公开资料未检索到",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "中国共产党大石桥市委员会", "role": "市委书记"}],
        "relationships": [
            {"person": "衣冠鹏", "person_id": "yingkou_大石桥_yiguanpeng", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：市委书记+市长（兼市委副书记）", "overlap_org": "大石桥市",
             "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
            {"person": "代天轶", "person_id": "yingkou_大石桥_daitianyi", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同届市领导（人大主任）", "overlap_org": "大石桥市", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "张燕", "person_id": "yingkou_大石桥_zhangyan", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同届市领导（市政协主席）", "overlap_org": "大石桥市", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "party_building", "achievement_or_event": "在市第八次党代会作报告，部署未来五年九项重点工作与社会发展目标，推进全面从严治党、抓好县市委书记关键岗位标尺",
             "role_in_event": "市委书记（代表七届委员会）", "measurable_outcome": "", "location": "大石桥市",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "在八届市委常委会（扩大）会议要求稳住经济基本盘、抓项目建设、扩消费稳外贸、优化营商环境、发展新质生产力",
             "role_in_event": "市委书记", "measurable_outcome": "", "location": "大石桥市",
             "confidence": "confirmed", "source_ids": ["S002"]},
            {"period": "2026-07", "domain": "public_security", "achievement_or_event": "带头学习贯彻焦裕禄精神、防汛救灾、安全生产（常委会多次）",
             "role_in_event": "市委书记", "measurable_outcome": "", "location": "大石桥市",
             "confidence": "confirmed", "source_ids": ["S004"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["party"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "市委书记（现职），初始履历未知", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "多次深入基层检查矿山安全、防汛、高考、走访慰问部队、督导镇街工作", "confidence": "plausible", "source_ids": ["S003", "S004"]},
                {"trait": "reform_oriented", "evidence": "强调发展新质生产力、优化营商环境、敢闯敢试", "confidence": "plausible", "source_ids": ["S002"]},
            ],
            "speech_themes": ["经济稳增长", "新质生产力", "政绩观", "安全生产", "全面从严治党", "选人用人"],
            "management_signals": ["强调闭环落实责任制", "建好用好基层治理综治中心"],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06 未发现违纪或负面舆情记录", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "中国共产党大石桥市第八次代表大会隆重召开", "url": "http://www.dsq.gov.cn/003/003001/20260723/902177bd-5736-483f-a0a7-9992c77e9c2a.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "徐荣利代表第七届委员会作工作报告"},
            {"id": "S002", "title": "八届市委常委会（扩大）会议召开", "url": "http://www.dsq.gov.cn/003/003001/20260730/b4d30f2d-0277-433d-b125-fd21802c328e.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "徐荣利以市委书记主持并讲话；衣冠鹏、代天轶、张燕出席"},
            {"id": "S003", "title": "徐荣利检查大石桥市高考准备工作", "url": "http://www.dsq.gov.cn/003/003003/20260605/adc37cf7-3e97-4e0d-bd84-a0fc651f0eb8.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-06-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "徐荣利带队，常委/副市长金鹏随行"},
            {"id": "S004", "title": "中国共产党大石桥市第八次代表大会胜利闭幕", "url": "http://www.dsq.gov.cn/003/003001/20260727/58b7fa69-637b-4997-9216-9d68ca54d9ee.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-07-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "换届选举产生八届市委，徐荣利连任（执行主席）"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "徐荣利出生/籍贯/学历/入党时间/入党时间/任支前履历"},
        "open_questions": [
            {"priority": "critical", "question": "徐荣利出生年月、籍贯、教育背景、入党时间、参加工作时间", "why_it_matters": "基本身份信息缺失",
             "suggested_queries": ["徐荣利 简历 大石桥 营口"], "last_attempted": AS_OF},
            {"priority": "high", "question": "徐荣利何时调任大石桥市委书记、任前职务", "why_it_matters": "判断干部交流源头",
             "suggested_queries": ["徐荣利 任前公示 营口"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任大石桥市委书记是谁、去向如何", "why_it_matters": "班子延续与跨县干部流动",
             "suggested_queries": ["大石桥市 市委 前任 书记"], "last_attempted": AS_OF},
        ],
    }

    yi = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "营口市", "region": "大石桥市",
                                "job": "市长", "task_id": "liaoning_大石桥市", "time_focus": "2025-2026"},
        "identity": {
            "person_id": "yingkou_大石桥_yiguanpeng",
            "name": "衣冠鹏",
            "aliases": [],
            "gender": "男", "ethnicity": "汉族", "birth": "1978-09", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "大学学历(院校待查)", "major": "", "degree": "学士(推断，待查)", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "衣冠鹏_1978-09", "name_birthplace": "衣冠鹏_unknown",
                            "official_profile_url": "http://www.dsq.gov.cn/010/011001/011001001/leader.html"},
        },
        "current_status": {"current_post": "市委副书记、市长", "current_org": "大石桥市人民政府",
                           "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002"]},
        "career_timeline": [
            {"start": "unknown", "end": "present", "org": "大石桥市人民政府", "title": "市政府党组书记、市长",
             "level": "县处级", "location": "大石桥市", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "主持市政府全面工作，负责审计等方面工作，分管市审计局（官网领导之窗）",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "present", "org": "中共大石桥市委员会", "title": "市委副书记",
             "level": "县处级", "location": "大石桥市", "system": "party", "rank": "县处级正职", "is_key_promotion": False,
             "notes": "2026-07-22 八次党代会开幕大会执行主席/主持；常委会会议出席并部署经济工作", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任大石桥市长前的更早履历（此前职务）公开资料未检索到", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "大石桥市人民政府", "role": "市长"}],
        "relationships": [
            {"person": "徐荣利", "person_id": "yingkou_大石桥_xurongli", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：市长（兼市委副书记）与书记", "overlap_org": "大石桥市",
             "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"person": "张雨", "person_id": "yingkou_大石桥_zhangyu", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "市长与常务副市长（市政府班子）", "overlap_org": "大石桥市人民政府",
             "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "2026-04~07", "domain": "economic_development", "achievement_or_event": "在市委常委会（扩大）会议部署二季度经济、指标调度、项目建设、营商环境、工业运行、农业增收、消费外贸、存量盘活等",
             "role_in_event": "市长（兼市委副书记）", "measurable_outcome": "", "location": "大石桥市",
             "confidence": "confirmed", "source_ids": ["S003"]},
            {"period": "2026-07", "domain": "urban_construction", "achievement_or_event": "第八届政府第90次常务会议部署市政重点安排",
             "role_in_event": "市长", "measurable_outcome": "", "location": "大石桥市",
             "confidence": "confirmed", "source_ids": ["S005"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder", "systems_experience": ["party", "government"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "由市委副书记/市长（现职），任前履历未知", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "聚焦经济指标调度、项目建设、营商环境、民生", "confidence": "plausible", "source_ids": ["S003"]}
            ],
            "speech_themes": ["经济稳增长", "项目建设", "营商环境", "民生保障"],
            "management_signals": [], "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06 未发现违纪或负面舆情线索", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "衣冠鹏-大石桥市人民政府(领导之窗)", "url": "http://www.dsq.gov.cn/010/011001/011001001/leader.html",
             "publisher": "大石桥市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "市长简历：男，汉族，1978-09 出生，大学学历，现任大石桥市委副书记，市政府党组书记、市长"},
            {"id": "S002", "title": "八届市委常委会（扩大）会议召开", "url": "http://www.dsq.gov.cn/003/003001/20260730/b4d30f2d-0277-433d-b125-fd21802c328e.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "衣冠鹏以市委副书记、市政府党组书记、市长身份出席并安排部署"},
            {"id": "S003", "title": "七届市委常委会（扩大）会议召开(2026-04)", "url": "http://www.dsq.gov.cn/003/003003/20260427/dd0bc763-663a-44f0-a27f-cc173be239b2.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-04-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "衣冠鹏部署二季度经济工作"},
            {"id": "S004", "title": "中国共产党大石桥市第八次代表大会", "url": "http://www.dsq.gov.cn/003/003001/20260723/902177bd-5736-483f-a0a7-9992c77e9c2a.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "衣冠任执行主席/主持大会"},
            {"id": "S005", "title": "第八届政府第90次常务会议召开", "url": "http://www.dsq.gov.cn/003/003001/20260805/c5ed02ae-d01a-4f80-acd7-9240a5005829.html",
             "publisher": "大石桥市融媒体中心", "published_at": "2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "衣冠鹏主持市政府常务会议"},
        ],
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "衣冠鹏出生4年9月、籍贯、院校、专业、入党时间、此前职务与任期起始"},
        "open_questions": [
            {"priority": "critical", "question": "衣冠鹏具体院校、专业、入党时间、参加工作年份、任前职务与到任大石桥时间", "why_it_matters": "身份与晋升轨迹细节",
             "suggested_queries": ["衣冠鹏 简历 大石桥 市长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任大石桥市长是谁、去向如何", "why_it_matters": "判断班子延续与干部流动",
             "suggested_queries": ["大石桥市 前任市长"], "last_attempted": AS_OF},
        ],
    }

    person_dir = PERSONS_STAGING_DIR
    today = AS_OF.replace("-", "")
    for fname, data in [
        (f"{today}-辽宁省-营口市-市委书记-徐荣利.json", xu),
        (f"{today}-辽宁省-营口市-市长-衣冠鹏.json", yi),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    write_person_jsons()

    print(f"\nDone! Staged output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PERSONS_STAGING_DIR.glob("*.json")):
        if "大石桥" in f.name:
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()