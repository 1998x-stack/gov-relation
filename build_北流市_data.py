#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""北流市领导班子工作关系网络 — 数据构建脚本

生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON。

Level: 县级市
Province: 广西壮族自治区
Parent City: 玉林市
Region: 北流市
Targets: 市委书记 & 市长

当前在任 (as of 2026-07-23):
- 市委书记: 周印章 (2026? - )
- 市长: 黄政强 (北流市委副书记、市人民政府党组书记、市长)

数据来源:
  - 北流市人民政府门户网站 http://www.beiliu.gov.cn
  - 市长页面: http://www.beiliu.gov.cn/ldfg/sz/
  - 副市长页面: http://www.beiliu.gov.cn/ldfg/fsz/
  - 政务要闻和市委常委会会议报道 (2026年7月)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "北流市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR
TASK_ID = "guangxi_北流市"
AS_OF = "2026-07-23"
OFFICIAL_SITE = "http://www.beiliu.gov.cn"

# ── 来源登记 ──
source_register = [
    {"id": "S001", "title": "北流市人民政府门户网站 - 市长页面",
     "url": "http://www.beiliu.gov.cn/ldfg/sz/",
     "publisher": "北流市人民政府", "published_at": "2026-07-23",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S002", "title": "北流市人民政府 - 副市长陈法祥页面",
     "url": "http://www.beiliu.gov.cn/ldfg/fsz/t25963648.shtml",
     "publisher": "北流市人民政府", "published_at": "2026-07-21",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S003", "title": "北流市人民政府 - 副市长周慧页面",
     "url": "http://www.beiliu.gov.cn/ldfg/fsz/t27918358.shtml",
     "publisher": "北流市人民政府", "published_at": "2026-07-21",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S004", "title": "北流市人民政府 - 副市长刘松页面",
     "url": "http://www.beiliu.gov.cn/ldfg/fsz/t19667540.shtml",
     "publisher": "北流市人民政府", "published_at": "2026-07-21",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S005", "title": "北流市人民政府 - 副市长陈小军页面",
     "url": "http://www.beiliu.gov.cn/ldfg/fsz/t23364018.shtml",
     "publisher": "北流市人民政府", "published_at": "2026-07-21",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S006", "title": "政务要闻 - 市委常委会召开会议 周印章主持",
     "url": "http://www.beiliu.gov.cn/zfxxgk_1/xxgkml/zwdt/zyhy/swhy/t27904720.shtml",
     "publisher": "北流融媒", "published_at": "2026-07-20",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S007", "title": "政务要闻 - 周印章到北流经济技术开发区调研",
     "url": "http://www.beiliu.gov.cn/zfxxgk_1/xxgkml/zwdt/zwyw/t27904718.shtml",
     "publisher": "北流融媒", "published_at": "2026-07-20",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S008", "title": "政务要闻 - 黄政强督导检查防台防汛及安全生产工作",
     "url": "http://www.beiliu.gov.cn/zfxxgk_1/xxgkml/zwdt/zwyw/t27932143.shtml",
     "publisher": "北流融媒", "published_at": "2026-07-22",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S009", "title": "政务要闻 - 周印章督导生态环保问题整改",
     "url": "http://www.beiliu.gov.cn/zfxxgk_1/xxgkml/zwdt/zwyw/t27863976.shtml",
     "publisher": "北流融媒", "published_at": "2026-07-07",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S010", "title": "政务要闻 - 黄政强调研督导板材家具产业项目",
     "url": "http://www.beiliu.gov.cn/zfxxgk_1/xxgkml/zwdt/zwyw/t27882185.shtml",
     "publisher": "北流融媒", "published_at": "2026-07-13",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S011", "title": "政务要闻 - 周印章走访慰问老干部",
     "url": "http://www.beiliu.gov.cn/zfxxgk_1/xxgkml/zwdt/zwyw/t27859296.shtml",
     "publisher": "北流融媒", "published_at": "2026-07-06",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S012", "title": "市长近期活动 - 市委常委会召开会议 刘启主持",
     "url": "http://www.beiliu.gov.cn/ldfg/sz/ldhd_sz/t27812271.shtml",
     "publisher": "北流市人民政府", "published_at": "2026-06-23",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
]


# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记
    # ════════════════════════════════════════
    {
        "id": "bl_zhou_yinzhang",
        "name": "周印章",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委书记",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月多篇报道确认市委书记身份: 市委常委会会议、经开区调研等",
    },
    # ════════════════════════════════════════
    # 核心领导：市长
    # ════════════════════════════════════════
    {
        "id": "bl_huang_zhengqiang",
        "name": "黄政强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委副书记、市长",
        "current_org": "中共北流市委员会/北流市人民政府",
        "source": "http://www.beiliu.gov.cn/ldfg/sz/",
    },
    # ════════════════════════════════════════
    # 市委常委、副市长
    # ════════════════════════════════════════
    {
        "id": "bl_chen_faxiang",
        "name": "陈法祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委常委、副市长",
        "current_org": "中共北流市委员会/北流市人民政府",
        "source": "http://www.beiliu.gov.cn/ldfg/fsz/t25963648.shtml",
    },
    # ════════════════════════════════════════
    # 副市长
    # ════════════════════════════════════════
    {
        "id": "bl_zhou_hui",
        "name": "周慧",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北流市副市长",
        "current_org": "北流市人民政府",
        "source": "http://www.beiliu.gov.cn/ldfg/fsz/t27918358.shtml",
    },
    {
        "id": "bl_liu_song",
        "name": "刘松",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北流市副市长",
        "current_org": "北流市人民政府",
        "source": "http://www.beiliu.gov.cn/ldfg/fsz/t19667540.shtml",
    },
    {
        "id": "bl_chen_xiaojun",
        "name": "陈小军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市副市长、市公安局局长",
        "current_org": "北流市人民政府/北流市公安局",
        "source": "http://www.beiliu.gov.cn/ldfg/fsz/t23364018.shtml",
    },
    # ════════════════════════════════════════
    # 从市委常委会报道中提取的其他市委常委
    # ════════════════════════════════════════
    {
        "id": "bl_lin_changcong",
        "name": "林长聪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委副书记、办公室主任",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会会议报道(S006)",
    },
    {
        "id": "bl_li_jianfeng",
        "name": "李剑锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委常委",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会会议报道(S006)",
    },
    {
        "id": "bl_wang_hui",
        "name": "王慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委常委",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会会议报道(S006)",
    },
    {
        "id": "bl_lin_yonghong",
        "name": "林咏红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委常委",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会会议报道(S006)",
    },
    {
        "id": "bl_li_hongfei",
        "name": "李红飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委常委",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会会议报道(S006)",
    },
    {
        "id": "bl_zhao_fengzhe",
        "name": "赵逢哲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委常委",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会会议报道(S006)",
    },
    {
        "id": "bl_li_tuanyuan",
        "name": "李团源",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委常委",
        "current_org": "中共北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会会议报道(S006)",
    },
    # ════════════════════════════════════════
    # 列席常委会的其他市领导
    # ════════════════════════════════════════
    {
        "id": "bl_lv_zhineng",
        "name": "吕智能",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北流市领导（人大方向）",
        "current_org": "北流市人民代表大会常务委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会列席报道(S006)",
    },
    {
        "id": "bl_chen_suzhen",
        "name": "陈素贞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北流市领导（政协方向）",
        "current_org": "中国人民政治协商会议北流市委员会",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会列席报道(S006)",
    },
    {
        "id": "bl_zhang_jinqiang",
        "name": "张进强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北流市领导",
        "current_org": "北流市",
        "source": OFFICIAL_SITE + " — 2026年7月市委常委会列席报道(S006)",
    },
    # ════════════════════════════════════════
    # 前任：刘启（前任市委书记）
    # ════════════════════════════════════════
    {
        "id": "bl_liu_qi",
        "name": "刘启",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北流市委原书记（已调离）",
        "current_org": "（调离）",
        "source": OFFICIAL_SITE + " — 2026年6月23日市委常委会由刘启主持(S012)，2026年7月已由周印章接任",
    },
]


# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共北流市委员会", "type": "党委", "level": "县处级",
     "parent": "中共玉林市委员会", "location": "北流市"},
    {"id": 2, "name": "北流市人民政府", "type": "政府", "level": "县处级",
     "parent": "玉林市人民政府", "location": "北流市"},
    {"id": 3, "name": "北流市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "北流市", "location": "北流市"},
    {"id": 4, "name": "中国人民政治协商会议北流市委员会", "type": "政协", "level": "县处级",
     "parent": "北流市", "location": "北流市"},
    {"id": 5, "name": "中共北流市纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共北流市委员会", "location": "北流市"},
    {"id": 6, "name": "北流市公安局", "type": "政府", "level": "县处级",
     "parent": "北流市人民政府", "location": "北流市"},
    {"id": 7, "name": "北流经济技术开发区", "type": "开发区", "level": "县处级",
     "parent": "北流市人民政府", "location": "北流市"},
]


# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 周印章
    {"person_id": "bl_zhou_yinzhang", "org_id": 1, "title": "北流市委书记",
     "start_date": "2026年", "end_date": "present", "rank": "县处级正职",
     "note": "2026年7月多篇报道以市委书记身份出席活动；前任为刘启"},
    # 黄政强
    {"person_id": "bl_huang_zhengqiang", "org_id": 1, "title": "北流市委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "官方简历：北流市委副书记"},
    {"person_id": "bl_huang_zhengqiang", "org_id": 2, "title": "北流市人民政府市长、党组书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "领导市政府全面工作，负责财政、审计工作"},
    # 陈法祥
    {"person_id": "bl_chen_faxiang", "org_id": 1, "title": "北流市委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责经贸科技、市场监管、大数据、招商引资、经开区等工作"},
    {"person_id": "bl_chen_faxiang", "org_id": 2, "title": "北流市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管市经济贸易和科学技术局、市场监督管理局、大数据局等"},
    # 周慧
    {"person_id": "bl_zhou_hui", "org_id": 2, "title": "北流市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管教育、人社、文体广电旅游、卫健、医保、民政、退役军人事务等"},
    # 刘松
    {"person_id": "bl_liu_song", "org_id": 2, "title": "北流市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管农业农村、林业、水利、乡村振兴、交通、征地拆迁等"},
    # 陈小军
    {"person_id": "bl_chen_xiaojun", "org_id": 2, "title": "北流市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管公安、司法、信访、维稳等工作"},
    {"person_id": "bl_chen_xiaojun", "org_id": 6, "title": "北流市公安局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任市公安局党委书记、局长"},
    # 林长聪
    {"person_id": "bl_lin_changcong", "org_id": 1, "title": "北流市委副书记、办公室主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任市委办公室主任"},
    # 其他市委常委
    {"person_id": "bl_li_jianfeng", "org_id": 1, "title": "北流市委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "bl_wang_hui", "org_id": 1, "title": "北流市委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "bl_lin_yonghong", "org_id": 1, "title": "北流市委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "bl_li_hongfei", "org_id": 1, "title": "北流市委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "bl_zhao_fengzhe", "org_id": 1, "title": "北流市委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "bl_li_tuanyuan", "org_id": 1, "title": "北流市委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 人大/政协/列席
    {"person_id": "bl_lv_zhineng", "org_id": 3, "title": "北流市领导（人大方向）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "列席市委常委会"},
    {"person_id": "bl_chen_suzhen", "org_id": 4, "title": "北流市领导（政协方向）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "列席市委常委会"},
    {"person_id": "bl_zhang_jinqiang", "org_id": 2, "title": "北流市领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "列席市委常委会，具体职务待查"},
    # 刘启（前任市委书记）
    {"person_id": "bl_liu_qi", "org_id": 1, "title": "北流市委书记（前任）",
     "start_date": "", "end_date": "2026年", "rank": "县处级正职",
     "note": "2026年6月23日仍以市委书记身份主持常委会，2026年7月由周印章接任"},
]


# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 周印章 <-> 黄政强（党政搭档）
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_huang_zhengqiang",
     "type": "党政搭档",
     "context": "周印章（市委书记）与黄政强（市长）为北流市党政主要领导人",
     "overlap_org": "北流市党政班子", "overlap_period": "2026年"},
    # 周印章 <-> 陈法祥（市委常委班子）
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_chen_faxiang",
     "type": "上下级",
     "context": "周印章（市委书记）与陈法祥（市委常委、副市长）在市委常委会共事",
     "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
    # 黄政强 <-> 陈法祥（市长-副市长）
    {"person_a": "bl_huang_zhengqiang", "person_b": "bl_chen_faxiang",
     "type": "上下级",
     "context": "黄政强（市长）与陈法祥（副市长）在市政府班子中共事",
     "overlap_org": "北流市人民政府", "overlap_period": ""},
    # 周印章 <-> 刘启（前后任）
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_liu_qi",
     "type": "前后任",
     "context": "周印章接替刘启任北流市委书记（2026年）",
     "overlap_org": "中共北流市委员会", "overlap_period": "2026年交接"},
    # 黄政强 <-> 各位副市长（政府班子成员）
    {"person_a": "bl_huang_zhengqiang", "person_b": "bl_zhou_hui",
     "type": "上下级",
     "context": "周慧（副市长）在黄政强（市长）领导下工作",
     "overlap_org": "北流市人民政府", "overlap_period": ""},
    {"person_a": "bl_huang_zhengqiang", "person_b": "bl_liu_song",
     "type": "上下级",
     "context": "刘松（副市长）在黄政强（市长）领导下工作",
     "overlap_org": "北流市人民政府", "overlap_period": ""},
    {"person_a": "bl_huang_zhengqiang", "person_b": "bl_chen_xiaojun",
     "type": "上下级",
     "context": "陈小军（副市长、公安局长）在黄政强（市长）领导下工作",
     "overlap_org": "北流市人民政府", "overlap_period": ""},
    # 市委常委班子成员互相关联
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_lin_changcong",
     "type": "共事", "context": "市委常委会共事", "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_li_jianfeng",
     "type": "共事", "context": "市委常委会共事", "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_wang_hui",
     "type": "共事", "context": "市委常委会共事", "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_lin_yonghong",
     "type": "共事", "context": "市委常委会共事", "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_li_hongfei",
     "type": "共事", "context": "市委常委会共事", "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_zhao_fengzhe",
     "type": "共事", "context": "市委常委会共事", "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
    {"person_a": "bl_zhou_yinzhang", "person_b": "bl_li_tuanyuan",
     "type": "共事", "context": "市委常委会共事", "overlap_org": "中共北流市委员会", "overlap_period": "2026年"},
]


# ═══════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ═══════════════════════════════════════════════
# 构建
# ═══════════════════════════════════════════════

def build():
    os.makedirs(STAGING_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    # Assign auto-increment IDs to persons
    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = p["id"]
        person_map[pid] = idx
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>北流市领导班子关系网络（基于北流市人民政府官网确认数据）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid = person_map[p["id"]]
        post = p.get("current_post", "")
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else "书记" in post and not post.startswith("副")
        is_mayor = "市长" in post and "副" not in post
        is_discipline = "纪委" in post

        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        else:
            color = "100,100,100"

        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        if otype == "党委":
            ocolor = "255,200,200"
        elif otype == "政府":
            ocolor = "200,200,255"
        elif otype == "人大":
            ocolor = "200,255,255"
        elif otype == "政协":
            ocolor = "255,240,200"
        elif otype == "纪委":
            ocolor = "255,200,150"
        elif otype == "开发区":
            ocolor = "200,255,200"
        elif otype == "乡镇/街道":
            ocolor = "255,255,200"
        else:
            ocolor = "200,200,200"

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        oid = pos["org_id"] + 100000 if pos["org_id"] > 0 else 0
        if oid == 0:
            continue
        lines.append(
            f'      <edge id="e{eid}" source="p{person_map[pos["person_id"]]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{person_map[r["person_a"]]}" target="p{person_map[r["person_b"]]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "玉林市",
                "region": "北流市",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"beiliu_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
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
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在北流市人民政府官网公开信息中未发现负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历及出生年月、籍贯、学历等详细信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的出生年月、籍贯、学历、入党时间、参加工作时间",
                 "why_it_matters": "无法建立完整的身份标识",
                 "suggested_queries": [f"{p['name']} 简历 北流"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 北流 任职经历"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 周印章 person JSON ──
    zyz_timeline = []
    zyz_relationships = [
        {"person": "黄政强", "person_id": "beiliu_黄政强", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "周印章（市委书记）与黄政强（市长）为北流市党政主要领导搭档",
         "overlap_org": "北流市党政班子", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006", "S007"]},
        {"person": "陈法祥", "person_id": "beiliu_陈法祥", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "周印章（市委书记）与陈法祥（市委常委、副市长）在市委常委会共事",
         "overlap_org": "中共北流市委员会", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "刘启", "person_id": "beiliu_刘启", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "周印章接替刘启任北流市委书记（2026年）",
         "overlap_org": "中共北流市委员会", "overlap_period": "2026年",
         "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S012"]},
    ]
    zyz_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到周印章任北流市委书记前的履历信息",
        "confidence": "unverified", "source_ids": []})

    zyz_json = make_person_json(persons[0], zyz_timeline, zyz_relationships)
    zyz_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-市委书记-周印章.json")
    with open(zyz_path, "w", encoding="utf-8") as f:
        json.dump(zyz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zyz_path}")

    # ── 黄政强 person JSON ──
    hzq_timeline = []
    hzq_relationships = [
        {"person": "周印章", "person_id": "beiliu_周印章", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄政强（市长）与周印章（市委书记）为北流市党政主要领导搭档",
         "overlap_org": "北流市党政班子", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
        {"person": "陈法祥", "person_id": "beiliu_陈法祥", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄政强（市长）与陈法祥（副市长）在市政府班子共事",
         "overlap_org": "北流市人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "周慧", "person_id": "beiliu_周慧", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄政强（市长）与周慧（副市长）在市政府班子共事",
         "overlap_org": "北流市人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "刘松", "person_id": "beiliu_刘松", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄政强（市长）与刘松（副市长）在市政府班子共事",
         "overlap_org": "北流市人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        {"person": "陈小军", "person_id": "beiliu_陈小军", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄政强（市长）与陈小军（副市长、公安局长）在市政府班子共事",
         "overlap_org": "北流市人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
    ]
    hzq_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到黄政强任北流市长前的完整履历信息",
        "confidence": "unverified", "source_ids": []})

    hzq_json = make_person_json(persons[1], hzq_timeline, hzq_relationships)
    hzq_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-市长-黄政强.json")
    with open(hzq_path, "w", encoding="utf-8") as f:
        json.dump(hzq_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hzq_path}")

    # ── 刘启 person JSON (predecessor) ──
    lq_timeline = []
    lq_relationships = [
        {"person": "周印章", "person_id": "beiliu_周印章", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "刘启任市委书记至2026年中，后由周印章接任",
         "overlap_org": "中共北流市委员会", "overlap_period": "2026年",
         "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S012"]},
        {"person": "黄政强", "person_id": "beiliu_黄政强", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "刘启（原市委书记）与黄政强（市长）曾为党政搭档",
         "overlap_org": "北流市党政班子", "overlap_period": "2026年上半年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    lq_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料仅见2026年6月以市委书记身份主持常委会的报道，完整履历未知",
        "confidence": "unverified", "source_ids": ["S012"]})

    lq_json = make_person_json(persons[-1], lq_timeline, lq_relationships)
    lq_json["identity"]["gender"] = "男"
    lq_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-原市委书记-刘启.json")
    with open(lq_path, "w", encoding="utf-8") as f:
        json.dump(lq_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lq_path}")

    print(f"\nBuild complete. All current roles confirmed from official source {OFFICIAL_SITE}")
    print("Identity info (birth, education, etc.) requires further research.")
    print("周印章、黄政强、刘启的完整履历和详细身份信息仍需补充。")


if __name__ == "__main__":
    build()
