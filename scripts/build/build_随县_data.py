#!/usr/bin/env python3
"""随县（湖北省随州市）领导班子工作关系网络生成脚本.

任务: hubei_随县 · 目标: 县委书记 & 县长 (level: 县, parent_city: 随州市).

数据锚点 (As-of): 2026-08-11。

确认现任 (随县人民政府门户政府领导页 2026-08-04 更新 / 随县发布 2026-07-11 会议稿):
- 县委书记                   姜辛辛 (1980-11, 研究生; 省检察/纪委/巡视系空降, 2024-12-27 当选县长, 2026-07 任书记)
- 县委副书记、县政府代理县长 曾浩 (1978-09, 大学; 原大洪山风景名胜区党工委书记、随州市科技局党组书记/局长, 2026-07 履新)
- 县委副书记:袁登峰; 县人大主任:庹大鹏; 县政协主席:杨涛; 常务副县长:庞忠斌;
  常委:朱建强(2026-08 新晋)、彭飞(纪委书记/监委代主任)、秦学伟、何仁章(政法委书记, 2026-07 公示拟任正处级)

前任链: 陈良(2021-09~2026-06, 荆州松滋市长交流来) → 陈兴旺(2020-01~2021-09, 现随州市委常委/市委秘书长)
→ 张健(县长2016-2019, 后曾都区长/书记); 县长链: 刘伟(2021-09~2024-12, 百度百科记为随州市人大, plausible) → 姜辛辛 → 曾浩。
历史首任(2009 复县): 周静(女, 现任荆州市人大常委会主任)。

证据标准: 官方门户 = confirmed; 组工公示/媒体转载 = confirmed 或 plausible; 百科 = plausible; 推断缺失留 open_questions。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

for parent in Path(__file__).resolve().parents:
    if (parent / "gov_relation").is_dir():
        sys.path.insert(0, str(parent))
        break

from gov_relation.factory import InsertFactory, PersonJSONFactory
from gov_relation.runner import run_build

TASK_DIR = Path(__file__).resolve().parent
DB_PATH = TASK_DIR / "随县_network.db"
GEXF_PATH = TASK_DIR / "随县_network.gexf"
REPORT_PATH = (
    TASK_DIR / "20260811-湖北省-随州市-随县-领导班子工作关系网络调查报告.md"
)

PERSONS = [
    # ── 现任核心（书记/县长）──
    {
        "canonical_name": "姜辛辛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1980-11",
        "education": "研究生学历",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-jiang-xinxin-1980-11",
    },
    {
        "canonical_name": "曾浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1978-09",
        "education": "大学学历",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-zeng-hao-1978-09",
    },
    # ── 县委副书记 / 人大 / 政协 / 常委 ──
    {
        "canonical_name": "袁登峰",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-yuan-dengfeng",
    },
    {
        "canonical_name": "庹大鹏",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-tuo-dapeng",
    },
    {
        "canonical_name": "杨涛",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-yang-tao",
    },
    {
        "canonical_name": "庞忠斌",
        "gender": "",
        "ethnicity": "",
        "birth_text": "1975-10",
        "education": "大学本科",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-pangzhongbin-1975-10",
    },
    {
        "canonical_name": "彭飞",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-pengfei",
    },
    {
        "canonical_name": "秦学伟",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-qin-xuewei",
    },
    {
        "canonical_name": "朱建强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1977-07",
        "education": "在职大学",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-zhu-jianqiang-1977-07",
    },
    {
        "canonical_name": "何仁章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1972-09",
        "education": "中央党校大学",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-he-renzhang-1972-09",
    },
    {
        "canonical_name": "刘海燕",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-liu-haiyan",
    },
    # ── 县政府班子 ──
    {
        "canonical_name": "李方",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "_source_pk": "suixian-li-fang",
    },
    {
        "canonical_name": "王超",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-wang-chao",
    },
    {
        "canonical_name": "李伟",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "_source_pk": "suixian-li-wei",
    },
    {
        "canonical_name": "刘小波",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "_source_pk": "suixian-liu-xiaobo",
    },
    {
        "canonical_name": "杨海波",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "_source_pk": "suixian-yang-haibo",
    },
    {
        "canonical_name": "申珊珊",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "_source_pk": "suixian-shen-shanshan",
    },
    {
        "canonical_name": "童传新",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "_source_pk": "suixian-tong-chuanxin",
    },
    {
        "canonical_name": "胡超",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "_source_pk": "suixian-hu-chao",
    },
    # ── 前任 / 历史链条 ──
    {
        "canonical_name": "陈良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1981-02",
        "native_place": "山东新泰",
        "education": "在职博士研究生（中国地质大学（武汉）工学博士）",
        "party_join_text": "2006-11",
        "work_start_text": "2003-04",
        "_source_pk": "suixian-chen-liang-1981-02",
    },
    {
        "canonical_name": "刘伟",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-liu-wei-former-mayor",
    },
    {
        "canonical_name": "陈兴旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1971-08",
        "native_place": "湖北广水",
        "education": "省委党校研究生、农学学士",
        "party_join_text": "1993-03",
        "work_start_text": "1993-11",
        "_source_pk": "suixian-chen-xingwang-1971-08",
    },
    {
        "canonical_name": "张健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1967-10",
        "native_place": "湖北广水",
        "education": "省委党校研究生",
        "party_join_text": "1993-04",
        "work_start_text": "1988-08",
        "_source_pk": "suixian-zhang-jian-1967-10",
    },
    {
        "canonical_name": "周静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth_text": "1966-09",
        "native_place": "湖北武汉",
        "education": "在职硕士研究生、公共管理硕士",
        "party_join_text": "1992-06",
        "work_start_text": "1987-06",
        "_source_pk": "suixian-zhou-jing-1966-09",
    },
    {
        "canonical_name": "王成民",
        "gender": "",
        "ethnicity": "",
        "birth_text": "",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-wang-chengmin",
    },
    # ── 跨县交流节点（曾都/广水文）──
    {
        "canonical_name": "邓小菲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth_text": "1981-10",
        "native_place": "湖北随县",
        "education": "硕士",
        "party_join_text": "中共党员",
        "_source_pk": "suixian-deng-xiaofei-1981-10",
    },
    {
        "canonical_name": "杨光胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1977-12",
        "native_place": "湖北随县",
        "education": "法学硕士",
        "party_join_text": "1999-05",
        "work_start_text": "2001-07",
        "_source_pk": "suixian-yang-guangsheng-1977-12",
    },
]

ORGANIZATIONS = [
    {"canonical_name": "中共随县委员会", "organization_type": "party", "location_text": "湖北省随州市随县", "administrative_level": "县"},
    {"canonical_name": "随县人民政府", "organization_type": "government", "location_text": "湖北省随州市随县", "administrative_level": "县"},
    {"canonical_name": "随县人民代表大会常务委员会", "organization_type": "people_congress", "location_text": "湖北省随州市随县", "administrative_level": "县"},
    {"canonical_name": "政协随县委员会", "organization_type": "ppcc", "location_text": "湖北省随州市随县", "administrative_level": "县"},
    {"canonical_name": "随县纪律检查委员会（县监察委员会）", "organization_type": "discipline", "location_text": "湖北省随州市随县", "administrative_level": "县"},
    {"canonical_name": "随县经济开发区管理委员会", "organization_type": "development_zone", "location_text": "湖北省随州市随县经济开发区", "administrative_level": "县"},
    {"canonical_name": "中共随州市委员会", "organization_type": "party", "location_text": "湖北省随州市", "administrative_level": "地级市"},
    {"canonical_name": "随州市人民政府", "organization_type": "government", "location_text": "湖北省随州市", "administrative_level": "地级市"},
    {"canonical_name": "随州市人民代表大会常务委员会", "organization_type": "people_congress", "location_text": "湖北省随州市", "administrative_level": "地级市"},
    {"canonical_name": "随州市科学技术局", "organization_type": "government_department", "location_text": "湖北省随州市", "administrative_level": "地级市"},
    {"canonical_name": "大洪山风景名胜区管理委员会", "organization_type": "scenic_area", "location_text": "湖北省随州市大洪山", "administrative_level": "地级市"},
    {"canonical_name": "中共曾都区委员会", "organization_type": "party", "location_text": "湖北省随州市曾都区", "administrative_level": "区(县)"},
    {"canonical_name": "曾都区人民政府", "organization_type": "government", "location_text": "湖北省随州市曾都区", "administrative_level": "区(县)"},
    {"canonical_name": "中共广水市委员会", "organization_type": "party", "location_text": "湖北省随州市广水市", "administrative_level": "县级市"},
    {"canonical_name": "广水市人民政府", "organization_type": "government", "location_text": "湖北省随州市广水市", "administrative_level": "县级市"},
    {"canonical_name": "湖北省人民检察院", "organization_type": "judicial", "location_text": "武汉市", "administrative_level": "省级"},
    {"canonical_name": "湖北省纪委监委", "organization_type": "discipline", "location_text": "武汉市", "administrative_level": "省级"},
    {"canonical_name": "湖北省纪委监委组织部", "organization_type": "discipline", "location_text": "武汉市", "administrative_level": "省级"},
    {"canonical_name": "中共湖北省委巡视组", "organization_type": "party_agency", "location_text": "武汉市", "administrative_level": "省级"},
    {"canonical_name": "中共松滋市委员会", "organization_type": "party", "location_text": "湖北省荆州市松滋市", "administrative_level": "县级市"},
    {"canonical_name": "松滋市人民政府", "organization_type": "government", "location_text": "湖北省荆州市松滋市", "administrative_level": "县级市"},
    {"canonical_name": "中共石首市委员会", "organization_type": "party", "location_text": "湖北省荆州市石首市", "administrative_level": "县级市"},
    {"canonical_name": "石首市人民政府", "organization_type": "government", "location_text": "湖北省荆州市石首市", "administrative_level": "县级市"},
    {"canonical_name": "中共荆州市荆州区委员会", "organization_type": "party", "location_text": "湖北省荆州市荆州区", "administrative_level": "区(县)"},
    {"canonical_name": "荆州区人民政府", "organization_type": "government", "location_text": "湖北省荆州市荆州区", "administrative_level": "区(县)"},
    {"canonical_name": "荆州经济技术开发区管理委员会", "organization_type": "development_zone", "location_text": "湖北省荆州市", "administrative_level": "地级市"},
    {"canonical_name": "湖北省教育厅", "organization_type": "government_department", "location_text": "武汉市", "administrative_level": "省级"},
    {"canonical_name": "中共恩施州委员会", "organization_type": "party", "location_text": "湖北省恩施州", "administrative_level": "自治州"},
    {"canonical_name": "中共荆州市委员会", "organization_type": "party", "location_text": "湖北省荆州市", "administrative_level": "地级市"},
    {"canonical_name": "荆州市人民代表大会常务委员会", "organization_type": "people_congress", "location_text": "湖北省荆州市", "administrative_level": "地级市"},
    {"canonical_name": "广水市应山街道", "organization_type": "township", "location_text": "湖北省随州市广水市应山街道", "administrative_level": "乡(镇)"},
    {"canonical_name": "随县厉山镇", "organization_type": "township", "location_text": "湖北省随州市随县厉山镇", "administrative_level": "乡(镇)"},
    {"canonical_name": "随县柳林镇", "organization_type": "township", "location_text": "湖北省随州市随县柳林镇", "administrative_level": "乡(镇)"},
    {"canonical_name": "湖北机场集团有限公司", "organization_type": "state_owned_enterprise", "location_text": "武汉市", "administrative_level": "省级"},
]

POSITIONS = [
    # ── 姜辛辛：省检察院-纪委-巡视 → 随县 ──
    {"person_name": "姜辛辛", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委书记", "start_text": "2026-07", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正处级", "confidence": "confirmed", "notes": "2026-06-28 湖北省委组织部公示拟任；2026-07-11 以县委书记身份出席"},
    {"person_name": "姜辛辛", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委副书记、县长（一级调研员）", "start_text": "2024-12-27", "end_text": "2026-06", "sort_order": 10, "rank": "正处级", "confidence": "confirmed", "notes": "2024-12-24 县四届人大第二十次会议任代县长（同日先任命为副县长）；12-27 当选县长"},
    {"person_name": "姜辛辛", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "副县长、代理县长", "start_text": "2024-12-24", "end_text": "2024-12-27", "sort_order": 20, "rank": "正处级", "confidence": "confirmed"},
    {"person_name": "姜辛辛", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委副书记、政法委书记", "start_text": "2023-09前", "end_text": "2024-12", "sort_order": 30, "rank": "副处级", "confidence": "confirmed", "notes": "2023-09 县四大家联席会名单；2024-12-23 报道为县委副书记、县政府党组书记、政法委书记"},
    {"person_name": "姜辛辛", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委常委、副县长", "start_text": "未知", "end_text": "2023", "sort_order": 40, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "姜辛辛", "organization_name": "中共湖北省委巡视组", "organization_text": "中共湖北省委巡视组", "title": "正处级巡视专员", "start_text": "未知", "end_text": "未知", "sort_order": 50, "rank": "正处级", "confidence": "confirmed"},
    {"person_name": "姜辛辛", "organization_name": "湖北省纪委监委组织部", "organization_text": "湖北省纪委监委组织部", "title": "干部处副处长", "start_text": "未知", "end_text": "未知", "sort_order": 60, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "姜辛辛", "organization_name": "湖北省人民检察院", "organization_text": "湖北省人民检察院", "title": "公诉处科员至反贪污贿赂局侦查一处副处长", "start_text": "未知", "end_text": "未知", "sort_order": 70, "rank": "科员至副处级", "confidence": "confirmed", "notes": "历任公诉处科员、刑事审判监督处副主任科员、政治部主任科员、反贪局侦查二处主任科员、反贪局侦查一处副处长"},
    # ── 曾浩 ──
    {"person_name": "曾浩", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委副书记、县政府代理县长、党组书记", "start_text": "2026-07", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正处级", "confidence": "confirmed", "notes": "政府门户页 2026-08-04 更新为代理县长"},
    {"person_name": "曾浩", "organization_name": "随州市科学技术局", "organization_text": "随州市科学技术局", "title": "党组书记、局长", "start_text": "未知", "end_text": "2026-07-31", "sort_order": 10, "rank": "正处级", "confidence": "confirmed", "notes": "2026-07-31 随州市人大常委会免去局长职务"},
    {"person_name": "曾浩", "organization_name": "大洪山风景名胜区管理委员会", "organization_text": "大洪山风景名胜区管理委员会", "title": "党工委书记", "start_text": "未知", "end_text": "未知", "sort_order": 20, "rank": "正处级", "confidence": "confirmed"},
    # ── 袁登峰 ──
    {"person_name": "袁登峰", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委副书记", "start_text": "2023-09", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    # ── 庞忠斌 ──
    {"person_name": "庞忠斌", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委常委", "start_text": "2023", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "庞忠斌", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委常委、常务副县长、县政府党组副书记", "start_text": "2023", "end_text": "至今", "is_current": 1, "sort_order": 10, "rank": "副处级", "confidence": "confirmed", "notes": "官网 2025-11 简介"},
    # ── 彭飞 ──
    {"person_name": "彭飞", "organization_name": "随县纪律检查委员会（县监察委员会）", "organization_text": "随县纪委监委", "title": "县委常委、县纪委书记、县监委代理主任", "start_text": "2025-05", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    # ── 秦学伟 ──
    {"person_name": "秦学伟", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委常委", "start_text": "2025-07", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed", "notes": "分工待核"},
    # ── 朱建强 ──
    {"person_name": "朱建强", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委常委、县政府党组成员", "start_text": "2026-07", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed", "notes": "2026-07-03 随州市委组织部公示拟任副处级（原广水市应山街道党工委书记）"},
    {"person_name": "朱建强", "organization_name": "广水市应山街道", "organization_text": "广水市应山街道", "title": "党工委书记（四级调研员）", "start_text": "未知", "end_text": "2026-07", "sort_order": 10, "rank": "正科级", "confidence": "confirmed"},
    # ── 何仁章 ──
    {"person_name": "何仁章", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委常委、政法委书记（三级调研员）", "start_text": "2025", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed", "notes": "2026-07-03 公示拟任县(市、区)正处级领导职务，去向待核"},
    # ── 庹大鹏 ──
    {"person_name": "庹大鹏", "organization_name": "随县人民代表大会常务委员会", "organization_text": "随县人民代表大会常务委员会", "title": "县人大常委会主任", "start_text": "2026-02", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正处级", "confidence": "confirmed", "notes": "2026-02-27 县委常委会扩大会议以人大主任身份出席"},
    {"person_name": "庹大鹏", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委常委、副县长、政法委书记", "start_text": "2024", "end_text": "2026-02", "sort_order": 10, "rank": "副处级", "confidence": "plausible", "notes": "2025-06 禁毒宣传启动仪式出席"},
    # ── 杨涛 ──
    {"person_name": "杨涛", "organization_name": "政协随县委员会", "organization_text": "政协随县委员会", "title": "县政协主席", "start_text": "2024-07", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正处级", "confidence": "confirmed"},
    # ── 刘海燕 ──
    {"person_name": "刘海燕", "organization_name": "大洪山风景名胜区管理委员会", "organization_text": "大洪山风景名胜区管理委员会", "title": "管委会主任", "start_text": "2026-02", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正处级", "confidence": "confirmed", "notes": "常列席随县四大家会议"},
    # ── 政府班子 ──
    {"person_name": "李方", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "副县长", "start_text": "2026", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "王超", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "副县长、县公安局局长", "start_text": "2024-12", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "李伟", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "副县长、县政府党组成员", "start_text": "2025-11", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "刘小波", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "副县长、县政府党组成员", "start_text": "2025-11", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "杨海波", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "副县长、县政府党组成员", "start_text": "2026-05", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "申珊珊", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "副县长、县政府党组成员", "start_text": "2026-08", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed", "notes": "官网 2026-08-04 更新"},
    {"person_name": "童传新", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县政府党组成员", "start_text": "2025-11", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "胡超", "organization_name": "随县经济开发区管理委员会", "organization_text": "随县经济开发区管理委员会", "title": "党工委书记、管委会主任", "start_text": "2026-02", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副处级", "confidence": "confirmed"},
    # ── 陈良（前任书记，荆州系） ──
    {"person_name": "陈良", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委书记", "start_text": "2021-09", "end_text": "2026-06", "sort_order": 0, "rank": "正处级", "confidence": "confirmed", "notes": "卸任后去向待核"},
    {"person_name": "陈良", "organization_name": "松滋市人民政府", "organization_text": "松滋市人民政府", "title": "市委副书记、市长", "start_text": "2021-01", "end_text": "2021-09", "sort_order": 10, "rank": "正处级", "confidence": "confirmed", "notes": "2021-09-13 松滋市人大接受辞去市长职务"},
    {"person_name": "陈良", "organization_name": "松滋市人民政府", "organization_text": "松滋市人民政府", "title": "市委副书记、副市长、代理市长", "start_text": "2020-10", "end_text": "2021-01", "sort_order": 20, "rank": "正处级", "confidence": "confirmed"},
    {"person_name": "陈良", "organization_name": "中共石首市委员会", "organization_text": "中共石首市委员会", "title": "市委常委、副市长", "start_text": "2016-11", "end_text": "2020-10", "sort_order": 30, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "陈良", "organization_name": "荆州经济技术开发区管理委员会", "organization_text": "荆州经济技术开发区管理委员会", "title": "党工委委员、管委会副主任", "start_text": "2016-03", "end_text": "2016-10", "sort_order": 40, "rank": "副县", "confidence": "confirmed"},
    {"person_name": "陈良", "organization_name": "荆州区人民政府", "organization_text": "荆州区人民政府", "title": "副区长", "start_text": "2014-07", "end_text": "2016-03", "sort_order": 50, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "陈良", "organization_name": "中共松滋市委员会", "organization_text": "中共松滋市委员会", "title": "斯家场镇党委书记、人大主席（历任万家乡、涴市镇、共青团松滋市委）", "start_text": "2008-07", "end_text": "2014-06", "sort_order": 60, "rank": "正科级至副处级", "confidence": "confirmed", "notes": "其间 2012-09~2017-06 中国地质大学（武汉）在职研究生、获工学博士"},
    # ── 刘伟（前任县长） ──
    {"person_name": "刘伟", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委副书记、县长", "start_text": "2021-11", "end_text": "2024-12", "sort_order": 0, "rank": "正处级", "confidence": "confirmed", "notes": "2024-12-24 县四届人大二十次会议接受辞职"},
    {"person_name": "刘伟", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委副书记、副县长、代理县长", "start_text": "2021-09", "end_text": "2021-11", "sort_order": 10, "rank": "正处级", "confidence": "confirmed"},
    {"person_name": "刘伟", "organization_name": "随州市人民代表大会常务委员会", "organization_text": "随州市人民代表大会常务委员会", "title": "党组成员、副主任", "start_text": "2025", "end_text": "至今", "is_current": 1, "sort_order": 20, "rank": "副厅级", "confidence": "plausible", "notes": "百度百科词条现记；任免文书待核"},
    # ── 陈兴旺（前任书记→市委） ──
    {"person_name": "陈兴旺", "organization_name": "中共随州市委员会", "organization_text": "中共随州市委员会", "title": "市委常委、市委秘书长", "start_text": "2021-09", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "副厅级", "confidence": "confirmed", "notes": "长江网/随州新闻网"},
    {"person_name": "陈兴旺", "organization_name": "中共随县委员会", "organization_text": "中共随县委员会", "title": "县委书记", "start_text": "2020-01", "end_text": "2021-09", "sort_order": 10, "rank": "正处级", "confidence": "confirmed", "notes": "2020-01-03 全县干部大会宣布"},
    {"person_name": "陈兴旺", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委副书记、县长", "start_text": "2019", "end_text": "2020-01", "sort_order": 20, "rank": "正处级", "confidence": "confirmed", "notes": "2019-12 省委组织部第207号公示"},
    # ── 张健（县长→曾都） ──
    {"person_name": "张健", "organization_name": "中共曾都区委员会", "organization_text": "中共曾都区委员会", "title": "区委书记", "start_text": "2020-01", "end_text": "未知", "sort_order": 0, "rank": "副厅级", "confidence": "plausible", "notes": "2019-12-24 公示拟任曾都区委书记；后续任免待核"},
    {"person_name": "张健", "organization_name": "随州市人民政府", "organization_text": "随州市人民政府", "title": "市政府秘书长、党组成员、市政府办党组书记", "start_text": "2019", "end_text": "2020-01", "sort_order": 10, "rank": "正处级", "confidence": "confirmed"},
    {"person_name": "张健", "organization_name": "曾都区人民政府", "organization_text": "曾都区人民政府", "title": "区委副书记、区长", "start_text": "2019", "end_text": "2019", "sort_order": 20, "rank": "正处级", "confidence": "plausible", "notes": "时间段按公示履历顺序推断"},
    {"person_name": "张健", "organization_name": "随县人民政府", "organization_text": "随县人民政府", "title": "县委副书记、县长", "start_text": "2016", "end_text": "2019", "sort_order": 30, "rank": "正处级", "confidence": "plausible", "notes": "时间段按公示履历顺序推断"},
    # ── 周静（复县首任书记） ──
    {"person_name": "周静", "organization_name": "荆州市人民代表大会常务委员会", "organization_text": "荆州市人民代表大会常务委员会", "title": "市人大常委会主任", "start_text": "2019-01", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正厅级", "confidence": "confirmed", "notes": "2019-01-24 荆州市五届人大四次会议当选"},
    {"person_name": "周静", "organization_name": "中共荆州市委员会", "organization_text": "中共荆州市委员会", "title": "市委副书记、政法委书记", "start_text": "2017-12", "end_text": "2019-01", "sort_order": 10, "rank": "副厅级", "confidence": "confirmed"},
    {"person_name": "周静", "organization_name": "中共恩施州委员会", "organization_text": "中共恩施州委员会", "title": "州委常委、副州长；州委常委、组织部长、州委党校校长", "start_text": "2011-11", "end_text": "2017-11", "sort_order": 20, "rank": "副厅级", "confidence": "confirmed"},
    {"person_name": "周静", "organization_name": "湖北省教育厅", "organization_text": "湖北省教育厅", "title": "副厅长、党组成员", "start_text": "2011-01", "end_text": "2011-11", "sort_order": 30, "rank": "副厅级", "confidence": "confirmed"},
    {"person_name": "周静", "organization_name": "中共随县委员会", "organization_text": "随县（复县建政）", "title": "随县县委书记、县人大主任（复县首任）", "start_text": "2009-07", "end_text": "2011-01", "sort_order": 40, "rank": "正处级", "confidence": "confirmed", "notes": "2009 年随县恢复建制后首任县委书记"},
    # ── 王成民（前任人大主任） ──
    {"person_name": "王成民", "organization_name": "随县人民代表大会常务委员会", "organization_text": "随县人民代表大会常务委员会", "title": "县人大常委会主任", "start_text": "2021", "end_text": "2025", "sort_order": 0, "rank": "正处级", "confidence": "plausible", "notes": "2023-09 至 2025-07 多次以主任身份出席；卸任时间待核"},
    # ── 跨县节点：邓小菲 / 杨光胜 ──
    {"person_name": "邓小菲", "organization_name": "广水市人民政府", "organization_text": "广水市人民政府", "title": "市委副书记、市政府市长", "start_text": "2026", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正处级", "confidence": "confirmed", "notes": "广水市报告（2026-08-06）"},
    {"person_name": "邓小菲", "organization_name": "中共广水市委员会", "organization_text": "中共广水市委员会", "title": "市委常委、宣传部部长", "start_text": "2021-09", "end_text": "2025-03", "sort_order": 10, "rank": "副处级", "confidence": "confirmed"},
    {"person_name": "邓小菲", "organization_name": "随县厉山镇", "organization_text": "随县厉山镇", "title": "党委书记", "start_text": "未知", "end_text": "2021-09前", "sort_order": 20, "rank": "正科级", "confidence": "confirmed"},
    {"person_name": "邓小菲", "organization_name": "随县柳林镇", "organization_text": "随县柳林镇", "title": "党委书记", "start_text": "未知", "end_text": "未知", "sort_order": 30, "rank": "正科级", "confidence": "confirmed"},
    {"person_name": "杨光胜", "organization_name": "湖北机场集团有限公司", "organization_text": "湖北机场集团有限公司", "title": "纪检条线岗位（具体职务待核）", "start_text": "2025-10", "end_text": "至今", "is_current": 1, "sort_order": 0, "rank": "正处级", "confidence": "plausible", "notes": "2025-10 调任湖北机场集团（广水市报告）"},
    {"person_name": "杨光胜", "organization_name": "中共广水市委员会", "organization_text": "中共广水市委员会", "title": "市委书记", "start_text": "2021-07", "end_text": "2025-10", "sort_order": 10, "rank": "正处级", "confidence": "confirmed"},
]

RELATIONSHIPS = [
    # 1. 现任党政一把手搭档
    {
        "person_from_name": "姜辛辛", "person_to_name": "曾浩",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "2026-07 起姜辛辛任随县县委书记、曾浩任县委副书记、县政府代理县长，构成随县党政一把手组合",
        "overlap_organization_text": "中共随县委员会/随县人民政府", "overlap_period_text": "2026-07至今",
    },
    # 2. 书记交接链
    {
        "person_from_name": "姜辛辛", "person_to_name": "陈良",
        "relationship_type": "predecessor_successor", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "陈良 2021-09 任随县县委书记，姜辛辛 2024-12 任县长并与陈良搭班至 2026-06；2026-07 姜接任",
        "overlap_organization_text": "中共随县委员会", "overlap_period_text": "2021-09至2026-07",
    },
    {
        "person_from_name": "陈良", "person_to_name": "陈兴旺",
        "relationship_type": "predecessor_successor", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "陈兴旺 2020-01 任随县县委书记，2021-09 陈良接任；陈兴旺升任随州市委常委、市委秘书长",
        "overlap_organization_text": "中共随县委员会", "overlap_period_text": "2020-01至2021-09",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "刘伟",
        "relationship_type": "predecessor_successor", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "2024-12-24 随县四届人大第二十次会议接受刘伟辞职，任命姜辛辛为代理县长（12-27 当选）",
        "overlap_organization_text": "随县人民政府", "overlap_period_text": "2024-12",
    },
    # 3. 县委班子共事
    {
        "person_from_name": "姜辛辛", "person_to_name": "袁登峰",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "confirmed",
        "context": "姜辛辛（县长→书记）与袁登峰（县委副书记）在县委常委会长期共事",
        "overlap_organization_text": "中共随县委员会", "overlap_period_text": "2023至今",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "庞忠斌",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "confirmed",
        "context": "县委书记与常务副县长多年同属县委常委会/县政府班子",
        "overlap_organization_text": "中共随县委员会/随县人民政府", "overlap_period_text": "2023至今",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "彭飞",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "confirmed",
        "context": "县委书记与县委常委、纪委书记在县委常委会共事（2025 年起）",
        "overlap_organization_text": "中共随县委员会", "overlap_period_text": "2025至今",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "秦学伟",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "weak", "confidence": "confirmed",
        "context": "同属随县县委常委班子（2025-08 三届十五次全会名单）",
        "overlap_organization_text": "中共随县委员会", "overlap_period_text": "2025至今",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "朱建强",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "weak", "confidence": "confirmed",
        "context": "朱建强 2026-07 由广水调任随县县委常委、县政府党组成员",
        "overlap_organization_text": "中共随县委员会", "overlap_period_text": "2026至今",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "何仁章",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "confirmed",
        "context": "何仁章任随县县委常委、政法委书记期间与县委书记（陈良、后姜辛辛）在县委常委会共事",
        "overlap_organization_text": "中共随县委员会", "overlap_period_text": "2025至今",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "庹大鹏",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "confirmed",
        "context": "庹大鹏由常委、副县长、政法委书记转任县人大常委会主任，与姜辛辛（县长→书记）长期同县班子",
        "overlap_organization_text": "中共随县委员会/随县人民代表大会常务委员会", "overlap_period_text": "2023至今",
    },
    # 4. 政府班子
    {
        "person_from_name": "曾浩", "person_to_name": "庞忠斌",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "代理县长与常务副县长组成县政府核心班子",
        "overlap_organization_text": "随县人民政府", "overlap_period_text": "2026-07至今",
    },
    {
        "person_from_name": "曾浩", "person_to_name": "李方",
        "relationship_type": "overlap", "direction": "undirected", "strength": "weak", "confidence": "confirmed",
        "context": "县政府班子共事", "overlap_organization_text": "随县人民政府", "overlap_period_text": "2026-07至今",
    },
    {
        "person_from_name": "曾浩", "person_to_name": "王超",
        "relationship_type": "overlap", "direction": "undirected", "strength": "weak", "confidence": "confirmed",
        "context": "县政府班子共事（王超兼县公安局局长）", "overlap_organization_text": "随县人民政府", "overlap_period_text": "2026-07至今",
    },
    {
        "person_from_name": "姜辛辛", "person_to_name": "杨涛",
        "relationship_type": "same_system", "direction": "undirected", "strength": "weak", "confidence": "confirmed",
        "context": "县政协主席与县委书记在县四大家框架内共事", "overlap_organization_text": "随县四大家", "overlap_period_text": "2024至今",
    },
    # 5. 大洪山系先后任
    {
        "person_from_name": "曾浩", "person_to_name": "刘海燕",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "plausible",
        "context": "曾浩曾任大洪山风景名胜区党工委书记，刘海燕现任管委会主任，同属大洪山景区管理系统",
        "overlap_organization_text": "大洪山风景名胜区管理委员会", "overlap_period_text": "2026前后",
    },
    # 6. 历史交接
    {
        "person_from_name": "张健", "person_to_name": "陈兴旺",
        "relationship_type": "predecessor_successor", "direction": "undirected",
        "strength": "medium", "confidence": "plausible",
        "context": "张健任随县县长后转曾都区，陈兴旺继任随县县长并升任县委书记（2019-2020 前后交接）",
        "overlap_organization_text": "随县人民政府", "overlap_period_text": "2019",
    },
    # 7. 跨县交流
    {
        "person_from_name": "邓小菲", "person_to_name": "杨光胜",
        "relationship_type": "same_system", "direction": "undirected",
        "strength": "weak", "confidence": "plausible",
        "context": "随县籍干部在广水的先后任职（杨光胜 2021-2025 广水市委书记；邓小菲 2021 起广水市委常委等）",
        "overlap_organization_text": "中共广水市委员会", "overlap_period_text": "2021-2025",
    },
    {
        "person_from_name": "朱建强", "person_to_name": "何仁章",
        "relationship_type": "same_system", "direction": "undirected",
        "strength": "weak", "confidence": "confirmed",
        "context": "2026-07-03 随州市委组织部同批任前公示（何仁章拟任正处级；朱建强拟任副处级）",
        "overlap_organization_text": "中共随州市委员会", "overlap_period_text": "2026-07",
    },
]

SOURCES = [
    {
        "canonical_url": "http://www.zgsuixian.gov.cn/zwgk/xxgkml/xzfld/",
        "title": "随县人民政府门户·政府领导（领导信息）",
        "publisher": "随县人民政府", "published_at": "2026-08-04",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://www.zgsuixian.gov.cn/zwgk/xxgkml/xzfld/zh/",
        "title": "随县政府门户·曾浩（县委副书记、县政府代理县长）领导之窗",
        "publisher": "随县人民政府", "published_at": "2026-08-04",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://www.zgsuixian.gov.cn/zwgk/xxgkml/xzfld/202511/t20251114_1383958.shtml",
        "title": "随县政府门户·庞忠斌（县委常委、常务副县长）简介",
        "publisher": "随县人民政府", "published_at": "2025-11-14",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "https://news.hubeidaily.net/pc/c_3478251.html",
        "title": "随县第四届人大常委会第二十次会议 决定姜辛辛为县人民政府代理县长",
        "publisher": "湖北日报客户端", "published_at": "2024-12-24",
        "accessed_at": "2026-08-11", "source_type": "appointment_notice", "reliability": "high",
    },
    {
        "canonical_url": "https://www.toutiao.com/article/7661542495490245162/",
        "title": "湖北随县县委书记调整（随县发布：姜辛辛任县委书记）",
        "publisher": "今日头条（转随县发布）", "published_at": "2026-07-12",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "https://c.m.163.com/news/a/L1IMVCVI05563DJA.html",
        "title": "姜辛辛任随县县委书记（含简历；曾浩任县委副书记）",
        "publisher": "网易", "published_at": "2026-07-12",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "https://cn.wa01.com/a/jiang-xin-xin-ren-sui-xian-zheng-fu-dang-zu-shu-ji.html",
        "title": "姜辛辛任随县政府党组书记（2024-12-23）",
        "publisher": "天天要闻（转随县发布）", "published_at": "2024-12-23",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "https://www.toutiao.com/article/7658202591281398272/",
        "title": "随州市委组织部干部任前公示（2026-07-03：何仁章、朱建强等11人）",
        "publisher": "今日头条（转随州市委组织部）", "published_at": "2026-07-03",
        "accessed_at": "2026-08-11", "source_type": "appointment_notice", "reliability": "medium",
    },
    {
        "canonical_url": "http://www.suizhou.gov.cn/zwgk/xxgk/rsrm_5792/202001/t20200104_597843.shtml",
        "title": "中共湖北省委组织部干部任前公告公示（2019年第207号：张健、陈兴旺）",
        "publisher": "随州市人民政府门户", "published_at": "2019-12-24",
        "accessed_at": "2026-08-11", "source_type": "appointment_notice", "reliability": "high",
    },
    {
        "canonical_url": "https://baike.baidu.com/item/%E9%99%88%E8%89%AF/20248752",
        "title": "陈良（湖北省随州市随县县委书记）百度百科",
        "publisher": "百度百科", "published_at": "2026-06",
        "accessed_at": "2026-08-11", "source_type": "encyclopedia", "reliability": "medium",
    },
    {
        "canonical_url": "https://baike.baidu.com/item/%E5%88%98%E4%BC%9F/3738066",
        "title": "刘伟（百度百科：曾任随县县长；词条现记为随州市人大常委会党组成员、副主任）",
        "publisher": "百度百科", "published_at": "2026-06",
        "accessed_at": "2026-08-11", "source_type": "encyclopedia", "reliability": "medium",
    },
    {
        "canonical_url": "http://district.ce.cn/newarea/sddy/201901/26/t20190126_31364725.shtml",
        "title": "周静当选荆州市人大常委会主任（图|简历）",
        "publisher": "中国经济网", "published_at": "2019-01-26",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "high",
    },
    {
        "canonical_url": "https://hb.china.com.cn/sz/2023-09/08/content_42509497.html",
        "title": "随县9月份县四大家领导联席会（2023-09 名单）",
        "publisher": "中国网湖北", "published_at": "2023-09-08",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "high",
    },
    {
        "canonical_url": "http://www.zgsuixian.gov.cn/ywdt/sxyw/202502/t20250208_1300676.shtml",
        "title": "县市区委书记访谈｜随县县委书记陈良：五年突破五百亿",
        "publisher": "随县人民政府门户", "published_at": "2025-02-08",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://www.zgsuixian.gov.cn/ywdt/sxyw/202602/t20260228_1409980.shtml",
        "title": "陈良主持召开县委常委会（扩大）会议（2026-02-27）",
        "publisher": "随县人民政府门户", "published_at": "2026-02-28",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://www.zgsuixian.gov.cn/zwgk/xxgkml/qtzdgknr/zfhy/qthy/202508/t20250819_1357592.shtml",
        "title": "中国共产党随县第三届委员会第十五次全体会议（2025-08 常委名单）",
        "publisher": "随县人民政府门户", "published_at": "2025-08-19",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://gaj.suizhou.gov.cn/fbjd_19/zwgk/xxgkml/gzdt/202506/t20250609_1339128.shtml",
        "title": "随县2025年全民禁毒宣传月启动仪式（庞忠斌/王超出席）",
        "publisher": "随州市公安局", "published_at": "2025-06-09",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://www.zgsuixian.gov.cn/ywdt/sxyw/202004/t20200409_780864.shtml",
        "title": "随县召开全县干部大会 陈兴旺担任随县县委书记",
        "publisher": "随县人民政府门户", "published_at": "2020-04-09",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
]


def add_evidence(conn: sqlite3.Connection) -> None:
    inserts = InsertFactory()
    people = dict(conn.execute("SELECT canonical_name, person_id FROM persons"))
    source_ids = dict(conn.execute("SELECT canonical_url, source_id FROM sources"))
    by_person = {
        "姜辛辛": [0, 3, 4, 5, 6],
        "曾浩": [0, 1, 4, 5],
        "陈良": [0, 9, 13, 14],
        "刘伟": [0, 3, 10],
        "陈兴旺": [8, 16],
        "张健": [8],
        "周静": [11],
        "庞忠斌": [0, 2],
        "庹大鹏": [0, 12, 14],
        "袁登峰": [0, 12, 14],
        "杨涛": [0, 14],
        "彭飞": [0, 15],
        "秦学伟": [0, 15],
        "朱建强": [0, 7],
        "何仁章": [0, 7],
        "刘海燕": [0, 14],
        "李方": [0],
        "王超": [0, 16],
        "李伟": [0],
        "刘小波": [0],
        "杨海波": [0],
        "申珊珊": [0],
        "童传新": [0],
        "胡超": [0],
        "王成民": [0, 12],
        "邓小菲": [0],
        "杨光胜": [0],
    }
    for name, indexes in by_person.items():
        person_id = people.get(name)
        if person_id is None:
            print(f"SKIP evidence: person {name} not found")
            continue
        for index in indexes:
            inserts.link_evidence(
                conn, source_ids[SOURCES[index]["canonical_url"]],
                "person", person_id, "identity_and_career",
            )
    for position_id, name in conn.execute(
        "SELECT p.position_id, pe.canonical_name FROM positions p "
        "JOIN persons pe ON pe.person_id = p.person_id"
    ):
        indexes = by_person.get(name)
        if not indexes:
            continue
        inserts.link_evidence(
            conn, source_ids[SOURCES[indexes[0]]["canonical_url"]],
            "position", position_id, "office_and_period",
        )
    for relationship_id, context in conn.execute(
        "SELECT relationship_id, context FROM relationships"
    ):
        if "党政一把手" in context or "代理县长" in context:
            inserts.link_evidence(
                conn, source_ids[SOURCES[3]["canonical_url"]],
                "relationship", relationship_id, "joint_leadership",
            )
            inserts.link_evidence(
                conn, source_ids[SOURCES[4]["canonical_url"]],
                "relationship", relationship_id, "succession",
            )
    conn.commit()


PROFILE_CONFIG = {
    "姜辛辛": {
        "job": "县委书记",
        "questions": [
            "出生地、入党时间、工作起始时间及研究生院校专业缺少官方简历原文",
            "省检察院时期各岗位起止时间待档案核实",
            "2026-07 县委书记到任的正式任免文书日期待核",
        ],
        "career": "partial",
        "specializations": ["纪检监察", "检察公诉", "巡视巡察", "县域治理"],
    },
    "曾浩": {
        "job": "县长",
        "questions": [
            "出生地、入党和参加工作起始时间缺官方简历原文",
            "大洪山风景名胜区党工委书记任期起止时间待核实",
            "随州市科学技术局局长任职起始时间待核实",
            "随县四届人大换届（2026-09 后）正式当选县长结果待观察",
        ],
        "career": "thin",
        "specializations": ["科技管理", "景区开发", "县域治理"],
    },
    "陈良": {
        "job": "前任县委书记",
        "questions": [
            "2026 年中卸任随县县委书记后的去向（未检索到任免公示）",
            "2003-04 参加工作至 2008-07 选调生之间约五年经历待考",
            "松滋市长任上（2021-01~09）与随县任职的正式任命文书核验",
        ],
        "career": "partial",
        "specializations": ["县域经济", "石材/农产品产业链", "纪律教育"],
    },
}


def write_profiles(conn: sqlite3.Connection) -> None:
    factory = PersonJSONFactory()
    for person_id, name in conn.execute(
        "SELECT person_id, canonical_name FROM persons ORDER BY canonical_name"
    ):
        config = PROFILE_CONFIG.get(name)
        if config is None:
            continue
        profile = factory.build(conn, person_id)
        profile["schema_version"] = "1.0"
        profile["investigation_scope"] = {
            "province": "湖北省", "city": "随州市",
            "region": "随县", "job": config["job"],
            "task_id": "hubei_随县", "time_focus": "截至2026-08-11",
        }
        profile["current_status"]["as_of"] = "2026-08-11"
        profile["current_status"]["is_current_confirmed"] = name in {"姜辛辛", "曾浩"}
        profile["professional_profile"] = {
            "primary_specializations": config["specializations"],
            "career_pattern": (
                "cross_county_rotation" if name == "陈良"
                else "discipline_track" if name == "姜辛辛"
                else "provincial_department"
            ),
        }
        profile["confidence_summary"] = {
            "identity": "confirmed" if name in {"姜辛辛", "曾浩"} else "plausible",
            "current_role": "confirmed" if name in {"姜辛辛", "曾浩"} else "plausible",
            "career_completeness": config["career"],
            "relationship_confidence": "high" if name in {"姜辛辛", "曾浩"} else "medium",
            "biggest_gap": config["questions"][0],
        }
        profile["open_questions"] = [
            {
                "priority": "high", "question": question,
                "why_it_matters": "补全身份去重字段、干部流动时间线与后续继任追踪",
                "suggested_queries": [f"{name} 简历", f"{name} 任免公示", f"{name} 随县 组织部"],
                "last_attempted": "2026-08-11",
            }
            for question in config["questions"]
        ]
        filename = f"20260811-湖北省-随州市-{config['job']}-{name}.json"
        (TASK_DIR / filename).write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def write_report() -> None:
    REPORT_PATH.write_text(
        """# 随县领导班子工作关系网络调查报告

> 数据锚点：2026-08-11　·　调查范围：湖北省随州市·随县（县委书记 & 县长）　·　任务：`hubei_随县`
> 现任班子以随县政府门户“政府领导”页（2026-08-04 更新）与随县发布 2026-07 任免报道为准。

## 1. 现任县委书记：姜辛辛

- **身份**：男，汉族，1980年11月生，研究生学历，中共党员。2026-06-28 湖北省委组织部公示拟任县委书记，2026-07 到任（2026-07-11 防汛防台风防溺水督办会以县委书记身份出席）。
- **晋升路径**（省直→县）：湖北省人民检察院（公诉处科员→刑事审判监督处副主任科员→政治部主任科员→反贪局侦查二处主任科员→反贪局侦查一处副处长）→湖北省纪委监委组织部干部处副处长→湖北省委巡视组正处级巡视专员→随县县委常委、副县长→县委副书记、政法委书记→2024-12 代县长/县长→**2026-07 县委书记**（`confirmed`）。
- 施政线索：2025 年抓外贸出口（香菇、跨境电商、海外仓）、主持常务会；2026-07 部署防汛安全工作（`confirmed`）。
- 研判：检察/纪检/巡视出身的一把手，执法监督条线熟悉度高。

## 2. 现任搭档（县长）：曾浩

- **身份**：男，汉族，1978年9月生，大学学历，中共党员（政府门户 2026-08-04）。
- **职务**：**县委副书记、县政府代理县长、党组书记**（2026-07 履行；主持县政府全面工作，负责审计工作）。
- **此前**：大洪山风景名胜区党工委书记→随州市科学技术局党组书记、局长（2026-07-31 免）→随县。
- 研判：市直机关下派；有景区开发背景，与随县文旅/特色农业相关。

## 3. 前任书记 / 前任县长

**陈良（前任书记，荆州系）**：1981年2月，山东新泰人，在职博士（中国地质大学·武汉）。2008-07 省委组织部选调生→松滋市乡镇/团委→荆州区副区长→荆州经开区→石首市委常委、常务副市长→松滋市长→**2021-09~2026-06/07 随县县委书记**（跨地市）。卸任去向未公开（open_gaps ⭐⭐⭐⭐⭐）。

**刘伟（前任县长）**：2021-09~2024-12 随县县委副书记、县长（先代后正式）；2024-12-24 辞职。百度百科现记为随州市人大常委会党组成员、副主任（plausible）。

## 4. 现任“四大家”班子（2026-08）

| 系统 | 姓名 | 职务 | 证据 |
|---|---|---|---|
| 党委 | 姜辛辛 | 县委书记 | 2026-07 公示/报道 |
| 党委 | 曾浩 | 县委副书记、代理县长 | 官网 2026-08-04 |
| 党委 | 袁登峰 | 县委副书记 | 2023-09 起 |
| 党委 | 庞忠斌 | 常委、常务副县长 | 官网 2025-11 |
| 党委 | 彭飞 | 常委、纪委书记、监委代主任 | 2025-05 |
| 党委 | 秦学伟 | 常委 | 2025-07 |
| 党委 | 朱建强 | 常委、县政府党组成员 | 2026-07 公示→web |
| 党委 | 何仁章 | 常委、政法委书记 | 2026-07 公示（拟正处） |
| 人大 | 庹大鹏 | 人大主任 | 2026-02 起 |
| 政协 | 杨涛 | 政协主席 | 2024-07 起 |
| 政府 | 李方、王超、李伟、刘小波、杨海波、申珊珊、童传新 | 副县长/党组成员 | 官网领导之窗 |
| 政府 | 胡超 | 经开区党工委书记、管委会主任 | 2026-02 |
| 市直 | 刘海燕 | 大洪山管委会主任 | 2026-02 起 |

## 5. 近期人事变动时间线

- 2019-12：张健/陈兴旺公示；2020-01-03 陈兴旺任书记。
- 2021-09：陈良接任书记；刘伟任县长。
- 2024-12：刘伟卸任；姜辛辛代县长→县长。
- 2026-02：庹大鹏任人大主任。
- 2026-06-28：省委公示姜辛辛拟任书记。
- 2026-07-03：市委公示何仁章、朱建强等 11 人。
- 2026-07-11：姜辛辛以书记露面；曾浩任副书记。
- 2026-07-31：市人大免曾浩科技局长。
- 2026-08-04：官网更新（代理县长；朱建强、申珊珊入列）。

## 6. 工作关系网络分析

**强（strong）**：姜-曾（书记×代理县长）；姜-陈良（2024-12~2026-06 搭班→2026-07 交接）；姜-刘伟（2024-12 交接）；陈良-陈兴旺（2020-2021 交接）。
**中/弱（medium/weak）**：姜与袁登峰、庞忠斌、彭飞、秦学伟、朱建强、何仁章、庹大鹏（常委会共事）；曾-刘海燕（大洪山先后任）；何-朱（2026-07 同批公示）。

## 7. 周边县区人事交流

- 随县→曾都：张健（县长→曾都区长→市政府秘书长→曾都书记 2019-12 公示）。
- 随县→广水：邓小菲（柳林镇/厉山镇书记→广水市委宣传部长→广水市长）；朱建强（广水应山→随县）回流。
- 县→市：陈兴旺→市委常委、市委秘书长；刘伟（plausible）→市人大。
- 跨地市：陈良（荆州→随州）；崔传金（潜江→广水，旁证）。
- 历史：周静（2009 复县首任书记→省教育厅→恩施→荆州市人大）。

## 8. 关键洞察与突破线索

1. “纪检条线”坐镇农业大县（书记背景）。
2. 县级主官县→市流动顺畅（陈兴旺→市委常委、秘书长）。
3. 曾随一体化干部联动（张健、邓小菲、朱建强等）。
4. 2026-09-21 换届观察窗：曾浩“代理→转正”、何仁章正处级去向。

## 9. 数据文件说明

- `随县_network.db`：v3 SQLite（persons/organizations/positions/relationships/sources/evidence_links 等）。
- `随县_network.gexf`：GEXF 1.3 图文件。
- `20260811-湖北省-随州市-{职务}-{姓名}.json`：核心人物深度档案（姜辛辛/曾浩/陈良）。

## 10. 开放性问题 / 信息来源

见 `checkpoint_01_research.md` 与 `open_gaps.md` 注册表（陈良去向/刘伟现职文书/何仁章去向/张健现状/王成民去向等）；
主要来源：随县人民政府门户领导之窗（zgsuixian.gov.cn）、湖北日报、随县发布、随州市委组织部公示、百度百科、中国经济网（周静简历）等（完整 URL 见脚本 SOURCES 表）。
""",
        encoding="utf-8",
    )


def main() -> None:
    run_build(
        slug="随县", persons=PERSONS, organizations=ORGANIZATIONS,
        positions=POSITIONS, relationships=RELATIONSHIPS, sources=SOURCES,
        claims=[], db_path=DB_PATH, gexf_path=GEXF_PATH,
        backend="v3", overwrite=True,
    )
    conn = sqlite3.connect(DB_PATH)
    try:
        add_evidence(conn)
        write_profiles(conn)
    finally:
        conn.close()
    write_report()
    print("随县 network build complete")
    print("DB:", DB_PATH)
    print("GEXF:", GEXF_PATH)


if __name__ == "__main__":
    main()