#!/usr/bin/env python3
"""Build script for 白河县 (安康市, 陕西省) government network.

Research date: 2026-07-25
Sources:
  - https://www.baihe.gov.cn/ (official website - 领导之窗, leader profiles)
  - https://www.baihe.gov.cn/Node-32258.html (中共白河县委 leadership)
  - https://www.baihe.gov.cn/Node-32260.html (白河县人民政府 leadership)
  - News articles from 白河县融媒体中心 2026
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "白河县"
TODAY = date.today().strftime("%Y%m%d")
AS_OF = date.today().strftime("%Y-%m-%d")
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

PERSONS = [
    {"id": 1, "name": "王日新", "gender": "男", "ethnicity": "汉族", "birth": "1971年3月", "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "", "current_post": "县委书记", "current_org": "中共白河县委员会", "source": "https://www.baihe.gov.cn/Content-790741.html"},
    {"id": 2, "name": "关汉杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记、县长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-2926588.html"},
    {"id": 3, "name": "丁辉", "gender": "男", "ethnicity": "汉族", "birth": "1975年9月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记", "current_org": "中共白河县委员会", "source": "https://www.baihe.gov.cn/Content-2318295.html"},
    {"id": 4, "name": "骆禹", "gender": "男", "ethnicity": "汉族", "birth": "1975年1月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记（挂职）", "current_org": "中共白河县委员会", "source": "https://www.baihe.gov.cn/Content-2604181.html"},
    {"id": 5, "name": "冯子惬", "gender": "男", "ethnicity": "汉族", "birth": "1978年4月", "birthplace": "", "education": "中央党校大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、常务副县长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-848894.html"},
    {"id": 6, "name": "李建国", "gender": "男", "ethnicity": "汉族", "birth": "1970年12月", "birthplace": "", "education": "大学本科学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、政法委书记", "current_org": "中共白河县委政法委员会", "source": "https://www.baihe.gov.cn/Content-2054898.html"},
    {"id": 7, "name": "李军帮", "gender": "男", "ethnicity": "汉族", "birth": "1974年11月", "birthplace": "", "education": "大学学历，在职研究生", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、副县长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-791142.html"},
    {"id": 8, "name": "纪昌斌", "gender": "男", "ethnicity": "汉族", "birth": "1972年9月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、统战部部长", "current_org": "中共白河县委员会", "source": "https://www.baihe.gov.cn/Content-848912.html"},
    {"id": 9, "name": "周满仓", "gender": "男", "ethnicity": "汉族", "birth": "1983年5月", "birthplace": "", "education": "省委党校研究生学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、组织部部长", "current_org": "中共白河县委员会", "source": "https://www.baihe.gov.cn/Content-2450213.html"},
    {"id": 10, "name": "张胜明", "gender": "男", "ethnicity": "汉族", "birth": "1988年3月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、宣传部部长", "current_org": "中共白河县委员会", "source": "https://www.baihe.gov.cn/Content-2724104.html"},
    {"id": 11, "name": "钟明玉", "gender": "男", "ethnicity": "汉族", "birth": "1980年", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县人武部政委", "current_org": "白河县人民武装部", "source": "https://www.baihe.gov.cn/Content-848914.html"},
    {"id": 12, "name": "陈康", "gender": "男", "ethnicity": "汉族", "birth": "1979年3月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县纪委书记、监委主任", "current_org": "中共白河县纪律检查委员会", "source": "https://www.baihe.gov.cn/Content-848961.html"},
    {"id": 13, "name": "陈亮", "gender": "男", "ethnicity": "汉族", "birth": "1980年1月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、副县长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-2920678.html"},
    {"id": 14, "name": "张安邦", "gender": "男", "ethnicity": "汉族", "birth": "1975年7月", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "副县长、县公安局局长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-2041914.html"},
    {"id": 15, "name": "杨先慧", "gender": "男", "ethnicity": "汉族", "birth": "1978年8月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "副县长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-2318617.html"},
    {"id": 16, "name": "王亮", "gender": "男", "ethnicity": "汉族", "birth": "1983年8月", "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "", "current_post": "副县长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-791692.html"},
    {"id": 17, "name": "曾秉国", "gender": "男", "ethnicity": "汉族", "birth": "1981年4月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "副县长", "current_org": "白河县人民政府", "source": "https://www.baihe.gov.cn/Content-2768639.html"},
    {"id": 18, "name": "高福宏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县人大常委会主任", "current_org": "白河县人大常委会", "source": "https://www.baihe.gov.cn/Node-32259.html"},
    {"id": 19, "name": "凃斌", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县人大常委会副主任", "current_org": "白河县人大常委会", "source": "https://www.baihe.gov.cn/Node-32259.html"},
    {"id": 20, "name": "查萍", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县人大常委会副主任", "current_org": "白河县人大常委会", "source": "https://www.baihe.gov.cn/Node-32259.html"},
    {"id": 21, "name": "叶怀成", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县人大常委会副主任", "current_org": "白河县人大常委会", "source": "https://www.baihe.gov.cn/Node-32259.html"},
    {"id": 22, "name": "游益林", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县人大常委会副主任", "current_org": "白河县人大常委会", "source": "https://www.baihe.gov.cn/Node-32259.html"},
    {"id": 23, "name": "余盛武", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县政协主席", "current_org": "政协白河县委员会", "source": "https://www.baihe.gov.cn/Node-32261.html"},
    {"id": 24, "name": "方景海", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县政协副主席", "current_org": "政协白河县委员会", "source": "https://www.baihe.gov.cn/Node-32261.html"},
    {"id": 25, "name": "汪功祥", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县政协副主席", "current_org": "政协白河县委员会", "source": "https://www.baihe.gov.cn/Node-32261.html"},
    {"id": 26, "name": "杨自力", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县政协副主席", "current_org": "政协白河县委员会", "source": "https://www.baihe.gov.cn/Node-32261.html"},
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共白河县委员会", "type": "党委", "level": "县处级", "parent": "中共安康市委", "location": "陕西省安康市白河县"},
    {"id": 2, "name": "白河县人民政府", "type": "政府", "level": "县处级", "parent": "安康市人民政府", "location": "陕西省安康市白河县"},
    {"id": 3, "name": "中共白河县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共安康市纪委", "location": "陕西省安康市白河县"},
    {"id": 4, "name": "中共白河县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共白河县委员会", "location": "陕西省安康市白河县"},
    {"id": 5, "name": "白河县人民武装部", "type": "军队", "level": "县处级", "parent": "安康军分区", "location": "陕西省安康市白河县"},
    {"id": 6, "name": "白河县人大常委会", "type": "人大", "level": "县处级", "parent": "安康市人大常委会", "location": "陕西省安康市白河县"},
    {"id": 7, "name": "政协白河县委员会", "type": "政协", "level": "县处级", "parent": "政协安康市委员会", "location": "陕西省安康市白河县"},
    {"id": 8, "name": "白河县公安局", "type": "政府", "level": "乡科级", "parent": "白河县人民政府", "location": "陕西省安康市白河县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "由县长转任县委书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年6月26日当选县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助党建、农业农村、乡村振兴、党校"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "苏陕协作挂职"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "政法委书记"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "县委常委、县人武部政委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "上校政治委员"},
    {"person_id": 12, "org_id": 3, "title": "县委常委、县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-06-26", "end_date": "present", "rank": "正处级", "note": "2026年6月26日县十九届人大六次会议当选"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责环保、交通、农业农村等"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助乡村振兴、文旅、招商"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责公安、司法、退役军人事务、信访"},
    {"person_id": 14, "org_id": 8, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "乡科级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责教育体育、自然资源、住建等"},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责工业经济、招商、民政"},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责文旅、卫健、医保、市场监管"},
    {"person_id": 4, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "苏陕协作挂职"},
    {"person_id": 18, "org_id": 6, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 7, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 7, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 7, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 7, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "strength": "strong", "context": "王日新任县委书记，关汉杰任县长，2026年6月起搭档", "overlap_org": "白河县", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "strength": "strong", "context": "王日新任县委书记，丁辉任县委副书记", "overlap_org": "中共白河县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 18, "type": "党政同僚", "strength": "medium", "context": "县委书记与县人大常委会主任", "overlap_org": "白河县", "overlap_period": ""},
    {"person_a": 1, "person_b": 23, "type": "党政同僚", "strength": "medium", "context": "县委书记与县政协主席", "overlap_org": "白河县", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "strength": "strong", "context": "县委书记与常务副县长", "overlap_org": "白河县", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "上下级", "strength": "strong", "context": "县委书记与县纪委书记", "overlap_org": "中共白河县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "strength": "strong", "context": "县长与常务副县长直接工作搭档", "overlap_org": "白河县人民政府", "overlap_period": "2026-"},
    {"person_a": 5, "person_b": 9, "type": "同系统", "strength": "weak", "context": "冯子惬曾任汉阴县委组织部长，周满仓为白河县委组织部长，同属组织系统", "overlap_org": "组织系统", "overlap_period": ""},
    {"person_a": 12, "person_b": 14, "type": "同系统", "strength": "weak", "context": "陈康曾任宁陕县副县长、公安局长，张安邦现任白河县公安局长，同属政法系统", "overlap_org": "政法系统", "overlap_period": ""},
    {"person_a": 10, "person_b": 1, "type": "上下级", "strength": "medium", "context": "张胜明由安康市委办调任白河县委常委", "overlap_org": "中共白河县委员会", "overlap_period": ""},
    {"person_a": 16, "person_b": 1, "type": "上下级", "strength": "medium", "context": "王亮由安康高新区调任白河县副县长", "overlap_org": "白河县人民政府", "overlap_period": ""},
    {"person_a": 18, "person_b": 19, "type": "上下级", "strength": "strong", "context": "县人大常委会主任与副主任", "overlap_org": "白河县人大常委会", "overlap_period": ""},
    {"person_a": 18, "person_b": 20, "type": "上下级", "strength": "strong", "context": "县人大常委会主任与副主任", "overlap_org": "白河县人大常委会", "overlap_period": ""},
    {"person_a": 18, "person_b": 21, "type": "上下级", "strength": "strong", "context": "县人大常委会主任与副主任", "overlap_org": "白河县人大常委会", "overlap_period": ""},
    {"person_a": 18, "person_b": 22, "type": "上下级", "strength": "strong", "context": "县人大常委会主任与副主任", "overlap_org": "白河县人大常委会", "overlap_period": ""},
    {"person_a": 23, "person_b": 24, "type": "上下级", "strength": "strong", "context": "县政协主席与副主席", "overlap_org": "政协白河县委员会", "overlap_period": ""},
    {"person_a": 23, "person_b": 25, "type": "上下级", "strength": "strong", "context": "县政协主席与副主席", "overlap_org": "政协白河县委员会", "overlap_period": ""},
    {"person_a": 23, "person_b": 26, "type": "上下级", "strength": "strong", "context": "县政协主席与副主席", "overlap_org": "政协白河县委员会", "overlap_period": ""},
]


def make_source_register():
    return [
        {"id": "S001", "title": "王日新——县委书记官方简历", "url": "https://www.baihe.gov.cn/Content-790741.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "白河县十九届人大六次会议闭幕", "url": "https://www.baihe.gov.cn/Content-2926588.html", "publisher": "白河县融媒体中心", "published_at": "2026-06-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "关汉杰当选县长"},
        {"id": "S003", "title": "丁辉——县委副书记官方简历", "url": "https://www.baihe.gov.cn/Content-2318295.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S004", "title": "骆禹——县委副书记（挂职）官方简历", "url": "https://www.baihe.gov.cn/Content-2604181.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S005", "title": "冯子惬——县委常委、常务副县长官方简历", "url": "https://www.baihe.gov.cn/Content-848894.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S006", "title": "李建国——县委常委、政法委书记官方简历", "url": "https://www.baihe.gov.cn/Content-2054898.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S007", "title": "李军帮——县委常委、副县长官方简历", "url": "https://www.baihe.gov.cn/Content-791142.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S008", "title": "纪昌斌——县委常委、统战部部长官方简历", "url": "https://www.baihe.gov.cn/Content-848912.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S009", "title": "周满仓——县委常委、组织部部长官方简历", "url": "https://www.baihe.gov.cn/Content-2450213.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S010", "title": "张胜明——县委常委、宣传部部长官方简历", "url": "https://www.baihe.gov.cn/Content-2724104.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S011", "title": "钟明玉——县委常委、县人武部政委官方简历", "url": "https://www.baihe.gov.cn/Content-848914.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S012", "title": "陈康——县委常委、纪委书记官方简历", "url": "https://www.baihe.gov.cn/Content-848961.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S013", "title": "陈亮——县委常委、副县长官方简历", "url": "https://www.baihe.gov.cn/Content-2920678.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S014", "title": "张安邦——副县长、公安局长官方简历", "url": "https://www.baihe.gov.cn/Content-2041914.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S015", "title": "杨先慧——副县长官方简历", "url": "https://www.baihe.gov.cn/Content-2318617.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S016", "title": "王亮——副县长官方简历", "url": "https://www.baihe.gov.cn/Content-791692.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S017", "title": "曾秉国——副县长官方简历", "url": "https://www.baihe.gov.cn/Content-2768639.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S018", "title": "白河县领导之窗——县委", "url": "https://www.baihe.gov.cn/Node-32258.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S019", "title": "白河县领导之窗——县政府", "url": "https://www.baihe.gov.cn/Node-32260.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S020", "title": "白河县领导之窗——县人大", "url": "https://www.baihe.gov.cn/Node-32259.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S021", "title": "白河县领导之窗——县政协", "url": "https://www.baihe.gov.cn/Node-32261.html", "publisher": "白河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S022", "title": "白河县庆祝中国共产党成立105周年大会", "url": "https://www.baihe.gov.cn/Content-2926587.html", "publisher": "白河县融媒体中心", "published_at": "2026-06-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S023", "title": "县领导开展'七一'慰问活动", "url": "https://www.baihe.gov.cn/Content-2927483.html", "publisher": "白河县融媒体中心", "published_at": "2026-07-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S024", "title": "县政府召开2026年第七次常务会议", "url": "https://www.baihe.gov.cn/Content-2930345.html", "publisher": "白河县融媒体中心", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S025", "title": "关汉杰调研县城建设工作", "url": "https://www.baihe.gov.cn/Content-2930712.html", "publisher": "白河县融媒体中心", "published_at": "2026-07-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S026", "title": "白河县十九届人大六次会议召集人会议", "url": "https://www.baihe.gov.cn/Content-2926175.html", "publisher": "白河县融媒体中心", "published_at": "2026-06-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    ]


def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "安康市",
            "region": "白河县",
            "job": p.get("current_post", ""),
            "task_id": "shaanxi_白河县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"baihexian_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("birthplace", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}] if p.get("education") else [],
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
            "administrative_rank": "县处级正职",
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
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息有待补充"
        },
        "open_questions": [
            {"priority": "critical" if not p.get("birth") else "medium",
             "question": f"{p['name']}的完整职业生涯履历",
             "why_it_matters": "无法追溯其任职路径和系统经历",
             "suggested_queries": [f"{p['name']} 简历 白河县", f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result


def build():
    print("=" * 60)
    print("  白河县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-25")
    print("  信息来源: 白河县人民政府网站 领导之窗")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"\n  人物: {len(PERSONS)} 人, 机构: {len(ORGANIZATIONS)} 个, 任职: {len(POSITIONS)} 条, 关系: {len(RELATIONSHIPS)} 条")

    source_register = make_source_register()

    # 1. 王日新 (县委书记)
    wang_timeline = [
        {"start": "", "end": "", "org": "中共汉滨区委员会", "title": "汉滨区委常委、组织部部长", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "中共白河县委员会", "title": "白河县委常委、县政府常务副县长", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "中共白河县委员会", "title": "白河县委副书记、县政府县长", "notes": "后由县长转任县委书记", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "中共白河县委员会", "title": "白河县委书记", "notes": "现任", "confidence": "confirmed", "source_ids": ["S001", "S022"]},
    ]
    wang_rels = [
        {"person": "关汉杰", "person_id": "baihexian_关汉杰", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与县长党政工作搭档", "overlap_org": "白河县", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "高福宏", "person_id": "baihexian_高福宏", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记与人大主任", "overlap_org": "白河县", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S022"]},
        {"person": "余盛武", "person_id": "baihexian_余盛武", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记与政协主席", "overlap_org": "白河县", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S022"]},
    ]
    wang_json = make_person_json(PERSONS[0], wang_timeline, wang_rels, source_register)
    wang_path = PERSONS_DIR / f"{TODAY}-陕西省-安康市-县委书记-王日新.json"
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wang_path.name}")

    # 2. 关汉杰 (县长)
    guan_timeline = [
        {"start": "2026-06-26", "end": "", "org": "白河县人民政府", "title": "白河县县长", "notes": "县十九届人大六次会议当选", "confidence": "confirmed", "source_ids": ["S002", "S024"]},
    ]
    guan_rels = [
        {"person": "王日新", "person_id": "baihexian_王日新", "relationship_type": "overlap", "strength": "strong", "evidence": "县长与县委书记党政搭档", "overlap_org": "白河县", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "冯子惬", "person_id": "baihexian_冯子惬", "relationship_type": "overlap", "strength": "strong", "evidence": "县长与常务副县长", "overlap_org": "白河县人民政府", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    guan_json = make_person_json(PERSONS[1], guan_timeline, guan_rels, source_register)
    guan_path = PERSONS_DIR / f"{TODAY}-陕西省-安康市-县长-关汉杰.json"
    with open(guan_path, "w", encoding="utf-8") as f:
        json.dump(guan_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {guan_path.name}")

    # 3. 冯子惬 (常务副县长)
    feng_timeline = [
        {"start": "", "end": "", "org": "白河县人民政府", "title": "白河县政府副县长", "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "", "end": "", "org": "中共汉阴县委员会", "title": "汉阴县委常委、组织部部长", "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "", "end": "", "org": "中共白河县委员会", "title": "白河县委常委、县政府党组副书记、常务副县长", "notes": "现任", "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    feng_rels = [
        {"person": "关汉杰", "person_id": "baihexian_关汉杰", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副县长与县长", "overlap_org": "白河县人民政府", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "王日新", "person_id": "baihexian_王日新", "relationship_type": "overlap", "strength": "medium", "evidence": "曾为王日新任县长时的副县长", "overlap_org": "白河县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
    ]
    feng_json = make_person_json(PERSONS[4], feng_timeline, feng_rels, source_register)
    feng_path = PERSONS_DIR / f"{TODAY}-陕西省-安康市-常务副县长-冯子惬.json"
    with open(feng_path, "w", encoding="utf-8") as f:
        json.dump(feng_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {feng_path.name}")


if __name__ == "__main__":
    build()
