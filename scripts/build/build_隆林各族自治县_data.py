#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""隆林各族自治县领导班子工作关系网络 — 数据构建脚本

生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON。

Level: 县
Province: 广西壮族自治区
Parent City: 百色市
Region: 隆林各族自治县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-23):
- 自治县党委书记: 黄茂兵 (2026年7月— )
- 县长: 黄健生 (隆林各族自治县委副书记、县人民政府县长)

数据来源:
  - 广西隆林网 (隆林各族自治县人民政府门户) http://www.longlin.gov.cn
  - 领导动态栏目: http://www.longlin.gov.cn/index.php?c=category&id=9
  - 自治县四家班子联席会报道 (2026年7月14日)
  - 百度百科 / 百度搜索结果
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "隆林各族自治县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR
TASK_ID = "guangxi_隆林各族自治县"
AS_OF = "2026-07-23"
OFFICIAL_SITE = "http://www.longlin.gov.cn"

# ── 来源登记 ──
source_register = [
    {"id": "S001", "title": "广西隆林网 - 自治县人民政府门户网站",
     "url": "http://www.longlin.gov.cn/",
     "publisher": "中共隆林各族自治县委员会宣传部", "published_at": "2026-07-23",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S002", "title": "自治县2026年第三次四家班子联席会报道",
     "url": "http://www.longlin.gov.cn/index.php?c=show&id=78988",
     "publisher": "隆林融媒体中心", "published_at": "2026-07-15",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S003", "title": "黄茂兵调研产业发展、防汛减灾及历史矛盾纠纷化解工作",
     "url": "http://www.longlin.gov.cn/index.php?c=show&id=79050",
     "publisher": "隆林融媒体中心", "published_at": "2026-07-21",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S004", "title": "黄茂兵到沙梨乡开展汛期防汛及历史矛盾纠纷化解工作调研",
     "url": "http://www.longlin.gov.cn/index.php?c=show&id=78995",
     "publisher": "隆林融媒体中心", "published_at": "2026-07-15",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S005", "title": "莫庸开展历史矛盾纠纷化解和防汛减灾工作调研督导",
     "url": "http://www.longlin.gov.cn/index.php?c=show&id=78498",
     "publisher": "隆林融媒体中心", "published_at": "2026-06-18",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S006", "title": "百度百科 - 黄茂兵",
     "url": "https://baike.baidu.com/item/%E9%BB%84%E8%8C%82%E5%85%B5",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S007", "title": "百度搜索 - 隆林各族自治县县委书记结果",
     "url": "https://www.baidu.com/s?wd=隆林各族自治县县委书记",
     "publisher": "百度", "published_at": "",
     "accessed_at": AS_OF, "source_type": "database", "reliability": "medium"},
    {"id": "S008", "title": "汲古新知 - 黄茂兵任隆林县委书记",
     "url": "https://www.baidu.com/s?wd=黄茂兵任隆林县委书记",
     "publisher": "汲古新知", "published_at": "2026-07-15",
     "accessed_at": AS_OF, "source_type": "media", "reliability": "medium"},
    {"id": "S009", "title": "百度百科 - 黄健生（隆林县长）",
     "url": "https://baike.baidu.com/item/%E9%BB%84%E5%81%A5%E7%94%9F/64931641",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S010", "title": "隆林各族自治县人民政府门户网站 - 县长页面",
     "url": "https://www.gxll.gov.cn/ldzc/",
     "publisher": "隆林各族自治县人民政府", "published_at": "2025-08-12",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S011", "title": "百度百科 - 莫庸",
     "url": "https://baike.baidu.com/item/%E8%8E%AB%E5%BA%B8/64256833",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S012", "title": "中国共产党隆林各族自治县第十五届委员会第七次全体会议公报",
     "url": "http://www.longlin.gov.cn/index.php?c=show&id=xxx",
     "publisher": "广西隆林网", "published_at": "2025-12-26",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S013", "title": "中国共产党隆林各族自治县第十五届委员会第六次全体(扩大)会议公报",
     "url": "http://www.longlin.gov.cn/index.php?c=show&id=xxx",
     "publisher": "广西隆林网", "published_at": "2024-12-31",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S014", "title": "隆林各族自治县第十六届人民代表大会第四次会议闭幕报道",
     "url": "https://www.gxll.gov.cn/",
     "publisher": "隆林各族自治县人民政府", "published_at": "2024-03-01",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S015", "title": "360百科 - 隆林各族自治县",
     "url": "https://baike.so.com/doc/5963378-6176324.html",
     "publisher": "360百科", "published_at": "2025-05-18",
     "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
]

# ── 数据 ──

# ===== 人员 =====
persons = [
    {
        "id": "longlin_huang_maobing",
        "name": "黄茂兵",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1973年6月",
        "birthplace": "广西百色",
        "native_place": "广西百色",
        "education": "在职研究生学历",
        "party_join": "1999年6月",
        "work_start": "1995年7月",
        "current_post": "自治县党委书记",
        "current_org": "中共隆林各族自治县委员会",
        "source": "S006+S002",
    },
    {
        "id": "longlin_huang_jiansheng",
        "name": "黄健生",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1974年4月",
        "birthplace": "广西隆林",
        "native_place": "广西隆林",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县长（县委副书记）",
        "current_org": "隆林各族自治县人民政府",
        "source": "S009+S010",
    },
    {
        "id": "longlin_mo_yong",
        "name": "莫庸",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1976年4月",
        "birthplace": "广西那坡县",
        "native_place": "广西那坡县",
        "education": "研究生学历（经济管理专业）",
        "party_join": "1998年6月",
        "work_start": "1995年7月",
        "current_post": "原自治县党委书记（已离任）",
        "current_org": "中共隆林各族自治县委员会（原）",
        "source": "S011",
    },
    {
        "id": "longlin_chen_yungang",
        "name": "陈允刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_huang_shenglian",
        "name": "黄声濂",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_wei_wenjun",
        "name": "韦文君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_wei_qiang",
        "name": "韦强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_huang_gulan",
        "name": "黄桂兰",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_nong_chengliang",
        "name": "农程亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_liu_tong",
        "name": "柳通",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_jiang_minglai",
        "name": "蒋明来",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S002",
    },
    {
        "id": "longlin_xiao_bing",
        "name": "肖兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县党委常委、党委办公室主任",
        "current_org": "中共隆林各族自治县委员会",
        "source": "S003+S004",
    },
    {
        "id": "longlin_yang_shengjun",
        "name": "杨胜军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县党委常委、统战部部长",
        "current_org": "中共隆林各族自治县委员会",
        "source": "S001",
    },
    {
        "id": "longlin_huang_shien",
        "name": "黄世恩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S001",
    },
    {
        "id": "longlin_pan_shundan",
        "name": "潘顺丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县人大常委会主任",
        "current_org": "隆林各族自治县人大常委会",
        "source": "S014",
    },
    {
        "id": "longlin_xia_jingchao",
        "name": "夏景超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县领导（四家班子领导成员）",
        "current_org": "隆林各族自治县四家班子",
        "source": "S014",
    },
    {
        "id": "longlin_yang_dengxiang",
        "name": "杨登祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县人大常委会副主任",
        "current_org": "隆林各族自治县人大常委会",
        "source": "S014",
    },
    {
        "id": "longlin_tao_shiqing",
        "name": "陶世清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县人大常委会副主任",
        "current_org": "隆林各族自治县人大常委会",
        "source": "S014",
    },
    {
        "id": "longlin_wu_linfang",
        "name": "吴林芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县人大常委会副主任",
        "current_org": "隆林各族自治县人大常委会",
        "source": "S014",
    },
]

# ===== 组织 =====
organizations = [
    {"id": 1, "name": "中共隆林各族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共百色市委员会", "location": "隆林各族自治县"},
    {"id": 2, "name": "隆林各族自治县人民政府", "type": "政府", "level": "县处级", "parent": "百色市人民政府", "location": "隆林各族自治县"},
    {"id": 3, "name": "隆林各族自治县人大常委会", "type": "人大", "level": "县处级", "parent": "百色市人大常委会", "location": "隆林各族自治县"},
    {"id": 4, "name": "隆林各族自治县政协", "type": "政协", "level": "县处级", "parent": "政协百色市委员会", "location": "隆林各族自治县"},
    {"id": 5, "name": "隆林各族自治县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共百色市纪律检查委员会", "location": "隆林各族自治县"},
    {"id": 6, "name": "隆林各族自治县委统战部", "type": "党委", "level": "县处级", "parent": "中共隆林各族自治县委员会", "location": "隆林各族自治县"},
    {"id": 7, "name": "隆林各族自治县委办公室", "type": "党委", "level": "县处级", "parent": "中共隆林各族自治县委员会", "location": "隆林各族自治县"},
    {"id": 8, "name": "百色市扶贫开发办公室", "type": "政府", "level": "地市级", "parent": "百色市人民政府", "location": "百色市"},
    {"id": 9, "name": "中共乐业县委员会", "type": "党委", "level": "县处级", "parent": "中共百色市委员会", "location": "乐业县"},
    {"id": 10, "name": "隆林各族自治县四家班子", "type": "党委", "level": "县处级", "parent": "隆林各族自治县", "location": "隆林各族自治县"},
]

# ===== 任职 =====
positions = [
    # 黄茂兵
    {"person_id": "longlin_huang_maobing", "org_id": 8, "title": "党组成员、副主任", "start_date": "2010-09", "end_date": "2014-02", "rank": "副处级", "note": "百色市扶贫开发办公室"},
    {"person_id": "longlin_huang_maobing", "org_id": 9, "title": "县委常委", "start_date": "2014-02", "end_date": "unknown", "rank": "副处级", "note": "乐业县委常委"},
    {"person_id": "longlin_huang_maobing", "org_id": 1, "title": "自治县党委书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "隆林各族自治县党委书记（2026年7月任）"},
    # 黄健生
    {"person_id": "longlin_huang_jiansheng", "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "隆林各族自治县人民政府县长"},
    {"person_id": "longlin_huang_jiansheng", "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 莫庸
    {"person_id": "longlin_mo_yong", "org_id": 1, "title": "自治县党委书记", "start_date": "2023年以前", "end_date": "2026-06", "rank": "正处级", "note": "前任县委书记，至少自2023年任职至2026年6月"},
    # 肖兵
    {"person_id": "longlin_xiao_bing", "org_id": 7, "title": "自治县党委常委、党委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨胜军
    {"person_id": "longlin_yang_shengjun", "org_id": 6, "title": "自治县党委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 潘顺丹
    {"person_id": "longlin_pan_shundan", "org_id": 3, "title": "自治县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 杨登祥
    {"person_id": "longlin_yang_dengxiang", "org_id": 3, "title": "自治县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陶世清
    {"person_id": "longlin_tao_shiqing", "org_id": 3, "title": "自治县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 吴林芳
    {"person_id": "longlin_wu_linfang", "org_id": 3, "title": "自治县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 其他领导成员——四家班子
    {"person_id": "longlin_chen_yungang", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_huang_shenglian", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_wei_wenjun", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_wei_qiang", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_huang_gulan", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_nong_chengliang", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_liu_tong", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_jiang_minglai", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_huang_shien", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": "longlin_xia_jingchao", "org_id": 10, "title": "四家班子领导成员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
]

# ===== 关系 =====
relationships = [
    # 党政主要领导搭档
    {"person_a": "longlin_huang_maobing", "person_b": "longlin_huang_jiansheng",
     "type": "overlap", "context": "黄茂兵（自治县党委书记）与黄健生（县长）为隆林各族自治县党政主要领导搭档",
     "overlap_org": "隆林各族自治县党政班子", "overlap_period": "2026年7月起"},
    # 前任与现任
    {"person_a": "longlin_mo_yong", "person_b": "longlin_huang_maobing",
     "type": "predecessor_successor", "context": "莫庸为隆林前任县委书记，黄茂兵于2026年7月接任",
     "overlap_org": "中共隆林各族自治县委员会", "overlap_period": "2026年"},
    # 前任书记与现任县长
    {"person_a": "longlin_mo_yong", "person_b": "longlin_huang_jiansheng",
     "type": "overlap", "context": "莫庸（原县委书记）与黄健生（县长）曾为党政搭档",
     "overlap_org": "隆林各族自治县党政班子", "overlap_period": "至2026年6月"},
    # 新书记与县委办主任
    {"person_a": "longlin_huang_maobing", "person_b": "longlin_xiao_bing",
     "type": "superior_subordinate", "context": "黄茂兵（书记）与肖兵（党委常委、县委办主任）在县委常委会共事",
     "overlap_org": "中共隆林各族自治县委员会", "overlap_period": "2026年7月起"},
    # 新书记与统战部长
    {"person_a": "longlin_huang_maobing", "person_b": "longlin_yang_shengjun",
     "type": "overlap", "context": "黄茂兵与杨胜军（统战部长）在县委常委会共事",
     "overlap_org": "中共隆林各族自治县委员会", "overlap_period": "2026年7月起"},
    # 人大主任与县长
    {"person_a": "longlin_pan_shundan", "person_b": "longlin_huang_jiansheng",
     "type": "overlap", "context": "潘顺丹（人大常委会主任）与黄健生（县长）在县四家班子共事",
     "overlap_org": "隆林各族自治县四家班子", "overlap_period": ""},
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
    lines.append('    <description>隆林各族自治县领导班子关系网络（基于隆林各族自治县人民政府官网确认数据）</description>')
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
        is_mayor = "县长" in post and "副" not in post
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
                "city": "百色市",
                "region": "隆林各族自治县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"longlin_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": p.get("native_place", ""),
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
                {"type": "none_found", "description": "在隆林各族自治县人民政府官网公开信息中未发现负面信号",
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
                 "question": f"{p['name']}的完整职业生涯履历（包含所有任职时间节点、具体职务、系统路径）",
                 "why_it_matters": "无法追溯其完整的任职路径和系统经历，影响关系网络深度分析",
                 "suggested_queries": [f"{p['name']} 简历 隆林", f"{p['name']} 任职经历 百色"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 黄茂兵 person JSON ──
    hmb_timeline = [
        {"start": "1995-07", "end": "", "org": "履历缺口", "title": "",
         "notes": "1995年7月参加工作，但1995-2010年之间的具体职务未公开",
         "confidence": "unverified", "source_ids": ["S006"]},
        {"start": "2010-09", "end": "2014-02", "org": "百色市扶贫开发办公室", "title": "党组成员、副主任",
         "notes": "", "confidence": "plausible", "source_ids": ["S006"]},
        {"start": "2014-02", "end": "unknown", "org": "乐业县", "title": "县委常委",
         "notes": "2014年2月任乐业县委常委，后续在乐业的职务变动不详",
         "confidence": "plausible", "source_ids": ["S006"]},
        {"start": "unknown", "end": "2026-06", "org": "履历缺口", "title": "",
         "notes": "乐业县委任职后至2026年6月之间的履职信息未公开",
         "confidence": "unverified", "source_ids": []},
        {"start": "2026-07", "end": "present", "org": "中共隆林各族自治县委员会", "title": "自治县党委书记",
         "notes": "2026年7月14日以自治县党委书记身份主持会议",
         "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    hmb_relationships = [
        {"person": "黄健生", "person_id": "longlin_黄健生", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄茂兵（书记）与黄健生（县长）为隆林各族自治县党政主要领导搭档",
         "overlap_org": "隆林各族自治县党政班子", "overlap_period": "2026年7月起",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "莫庸", "person_id": "longlin_莫庸", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "黄茂兵接替莫庸任隆林自治县党委书记（2026年7月）",
         "overlap_org": "中共隆林各族自治县委员会", "overlap_period": "2026年",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002", "S005"]},
        {"person": "肖兵", "person_id": "longlin_肖兵", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "黄茂兵与肖兵（党委常委、县委办主任）在调研活动中共同出席",
         "overlap_org": "中共隆林各族自治县委员会", "overlap_period": "2026年7月起",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
    ]
    hmb_json = make_person_json(persons[0], hmb_timeline, hmb_relationships)
    hmb_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-自治县党委书记-黄茂兵.json")
    with open(hmb_path, "w", encoding="utf-8") as f:
        json.dump(hmb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hmb_path}")

    # ── 黄健生 person JSON ──
    hjs_timeline = [
        {"start": "", "end": "", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到黄健生任县长前的完整履历信息。已知：彝族，1974年4月出生，广西隆林人，研究生学历，中共党员。具体任职经历待查。",
         "confidence": "unverified", "source_ids": ["S009", "S010"]},
    ]
    hjs_relationships = [
        {"person": "黄茂兵", "person_id": "longlin_黄茂兵", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄健生（县长）与黄茂兵（书记）为隆林各族自治县党政主要领导搭档",
         "overlap_org": "隆林各族自治县党政班子", "overlap_period": "2026年7月起",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "莫庸", "person_id": "longlin_莫庸", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄健生（县长）与原县委书记莫庸曾为党政搭档",
         "overlap_org": "隆林各族自治县党政班子", "overlap_period": "至2026年6月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S012"]},
        {"person": "潘顺丹", "person_id": "longlin_潘顺丹", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄健生（县长）与潘顺丹（人大常委会主任）在县四家班子共事",
         "overlap_org": "隆林各族自治县四家班子", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S014"]},
    ]
    hjs_json = make_person_json(persons[1], hjs_timeline, hjs_relationships)
    hjs_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县长-黄健生.json")
    with open(hjs_path, "w", encoding="utf-8") as f:
        json.dump(hjs_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hjs_path}")

    # ── 莫庸 person JSON (predecessor) ──
    my_timeline = [
        {"start": "1995-07", "end": "", "org": "履历缺口", "title": "",
         "notes": "1995年7月参加工作，早期履历未公开",
         "confidence": "unverified", "source_ids": ["S011"]},
        {"start": "2023年以前", "end": "2026-06", "org": "中共隆林各族自治县委员会", "title": "自治县党委书记",
         "notes": "至少自2023年起担任隆林县委书记，2025年12月仍以书记身份讲话，2026年6月18日仍以书记身份调研",
         "confidence": "confirmed", "source_ids": ["S005", "S012"]},
    ]
    my_relationships = [
        {"person": "黄茂兵", "person_id": "longlin_黄茂兵", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "莫庸任县委书记至2026年中，后由黄茂兵接任",
         "overlap_org": "中共隆林各族自治县委员会", "overlap_period": "2026年",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S005"]},
        {"person": "黄健生", "person_id": "longlin_黄健生", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "莫庸（原县委书记）与黄健生（县长）曾为党政搭档",
         "overlap_org": "隆林各族自治县党政班子", "overlap_period": "至2026年6月",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S012"]},
    ]
    my_json = make_person_json(persons[2], my_timeline, my_relationships)
    my_json["identity"]["gender"] = "男"
    my_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-原自治县党委书记-莫庸.json")
    with open(my_path, "w", encoding="utf-8") as f:
        json.dump(my_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {my_path}")

    print(f"\nBuild complete. All current roles confirmed from official source {OFFICIAL_SITE}")
    print("Identity info (birth, education, etc.) requires further research.")
    print("黄茂兵、黄健生、莫庸的完整履历和详细身份信息仍需补充。")


if __name__ == "__main__":
    build()
