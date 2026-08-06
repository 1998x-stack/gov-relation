#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乌兰察布市集宁区 leadership network.

集宁区是内蒙古自治区乌兰察布市的中心城区（市辖区），为乌兰察布市委、市政府驻地，
经济上以大数据/云计算、装备制造、文旅及商贸物流为主导产业，是乌兰察布市的政治、
经济、文化中心，也是全市唯一市辖区。

Current leadership (confirmed 2026-08-06 from official 集宁区人民政府 领导之窗
https://www.jnq.gov.cn/ldzc/ 及 乌兰察布市人民政府 领导之窗):
- 区委书记: 冀宏 (乌兰察布市委常委兼任集宁区委书记; 2026-07-30 集宁区第十五次党代会
  当选新一届区委书记, 连选连任)
- 区委副书记、区政府党组书记、代区长: 郝晓亭 (此前任乌兰察布市政府秘书长, 由市政府
  秘书长调任集宁区代区长)

换届/调动背景：
- 中国共产党乌兰察布市集宁区第十五次代表大会 2026-07-30 闭幕, 选出新一届区委委员41名、
  候补委员9名、纪委委员21名。大会执行主席/新一届班子: 冀宏、郝晓亭、田海军、沈冬梅、
  张新、庞文辉。┃
- 前任区长: 康海瑞 — 2026-01-28 在集宁区第十六届人大第五次会议上作《2026年政府工作
  报告》(当时任区长), 后由郝晓亭接任(代区长), 属市级机关→区级任职的向下交流。

参考构建:
- scripts/build/build_和林格尔县_data.py  (内蒙古县域网络模板)
- scripts/build/build_乌兰察布市_data.py  data/tmp/inner_mongolia_乌兰察布市 (上一任务,
  已建地级市班子, 含 冀宏/郝晓亭 的市委/市政府岗位)
"""

import sys
import os
import sqlite3  # noqa: F401  (used via gov_relation.runner.run_build)

from pathlib import Path

_REPO = Path(__file__).resolve().parent
while not (_REPO / "gov_relation").is_dir():
    if _REPO == _REPO.parent:
        break
    _REPO = _REPO.parent
sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "集宁区"
DB_PATH = DATABASE_DIR / "集宁区_network.db"
GEXF_PATH = GRAPH_DIR / "集宁区_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共乌兰察布市集宁区委员会", "type": "党委", "level": "市辖区",
     "parent": "中共乌兰察布市委", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 2, "name": "集宁区人民政府", "type": "政府", "level": "市辖区",
     "parent": "乌兰察布市人民政府", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 3, "name": "集宁区人大常委会", "type": "人大", "level": "市辖区",
     "parent": "乌兰察布市人大常委会", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 4, "name": "集宁区政协", "type": "政协", "level": "市辖区",
     "parent": "乌兰察布市政协", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 5, "name": "集宁区纪律检查委员会（监委）", "type": "纪委", "level": "市辖区",
     "parent": "中共集宁区委", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 6, "name": "中共集宁区委政法委员会", "type": "党委", "level": "市辖区",
     "parent": "中共集宁区委", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 7, "name": "中共集宁区委组织部", "type": "党委", "level": "市辖区",
     "parent": "中共集宁区委", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 8, "name": "中共集宁区委宣传部", "type": "党委", "level": "市辖区",
     "parent": "中共集宁区委", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 9, "name": "中共集宁区委统战部", "type": "党委", "level": "市辖区",
     "parent": "中共集宁区委", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 10, "name": "中共集宁区委办公室", "type": "党委", "level": "市辖区",
     "parent": "中共集宁区委", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 11, "name": "乌兰察布市公安局集宁区分局", "type": "政府", "level": "市辖区",
     "parent": "乌兰察布市公安局", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 12, "name": "集宁区人民法院", "type": "事业单位", "level": "市辖区",
     "parent": "集宁区人大常委会", "location": "内蒙古自治区乌兰察布市集宁区"},
    {"id": 13, "name": "集宁区人民检察院", "type": "事业单位", "level": "市辖区",
     "parent": "乌兰察布市人民检察院", "location": "内蒙古自治区乌兰察布市集宁区"},
    # 上级/相关组织（用于跨区域关系）
    {"id": 14, "name": "中共乌兰察布市委员会", "type": "党委", "level": "地级市",
     "parent": "中共内蒙古自治区委", "location": "内蒙古自治区乌兰察布市"},
    {"id": 15, "name": "乌兰察布市人民政府", "type": "政府", "level": "地级市",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区乌兰察布市"},
]

# ═══════════════════════════════════════════════════════════════════════════
# PERSONS
# ═══════════════════════════════════════════════════════════════════════════
persons = [
    # ═══ 区委领导 ═══
    # 1 — 冀宏 — 区委书记（兼市委常委，高配）
    {"id": 1, "name": "冀宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年3月", "birthplace": "待查",
     "education": "中央党校研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "乌兰察布市委常委、集宁区委书记",
     "current_org": "中共乌兰察布市集宁区委员会",
     "source": "https://www.jnq.gov.cn/ldzc/ 领导之窗(swld)；wulanchabu.gov.cn/swld/1691461.html"},
    # 2 — 郝晓亭 — 区委副书记、区政府代区长
    {"id": 2, "name": "郝晓亭", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年5月", "birthplace": "待查",
     "education": "大学学历，经济学硕士学位", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委副书记、政府党组书记、代区长",
     "current_org": "集宁区人民政府",
     "source": "https://www.jnq.gov.cn/ldzc/；此前任乌兰察布市政府秘书长(wulanchabu.gov.cn/zfld/65620.html)"},
    # 3 — 孔发鹏 — 区委副书记、政法委书记
    {"id": 3, "name": "孔发鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年11月", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委副书记、政法委书记",
     "current_org": "中共集宁区委政法委员会",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 4 — 田海军 — 区委常委、办公室主任
    {"id": 4, "name": "田海军", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年10月", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委常委、办公室主任",
     "current_org": "中共集宁区委办公室",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 5 — 沈冬梅 — 区委常委、宣传部部长
    {"id": 5, "name": "沈冬梅", "gender": "女", "ethnicity": "汉族",
     "birth": "1980年10月", "birthplace": "待查",
     "education": "大学学历，管理学学士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委常委、宣传部部长",
     "current_org": "中共集宁区委宣传部",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 6 — 张新 — 区委常委、组织部部长
    {"id": 6, "name": "张新", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年3月", "birthplace": "待查",
     "education": "大学学历，军事学学士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委常委、组织部部长",
     "current_org": "中共集宁区委组织部",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 7 — 庞文辉 — 区委常委、纪委书记、监委代主任
    {"id": 7, "name": "庞文辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年12月", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委常委、纪委书记、监委代主任",
     "current_org": "集宁区纪律检查委员会（监委）",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 8 — 王志威 — 区委常委、常务副区长
    {"id": 8, "name": "王志威", "gender": "男", "ethnicity": "汉族",
     "birth": "1987年2月", "birthplace": "待查",
     "education": "研究生学历，公共管理硕士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委常委、政府党组副书记、常务副区长",
     "current_org": "集宁区人民政府",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 9 — 丰雪 — 区委常委、副区长
    {"id": 9, "name": "丰雪", "gender": "女", "ethnicity": "汉族",
     "birth": "1984年10月", "birthplace": "待查",
     "education": "大学学历，文学学士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委常委、副区长",
     "current_org": "集宁区人民政府",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 10 — 郭辉 — 区委常委、统战部部长、政协党组副书记
    {"id": 10, "name": "郭辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年11月", "birthplace": "待查",
     "education": "大专学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区委常委、统战部部长、政协党组副书记",
     "current_org": "中共集宁区委统战部",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # ═══ 政府领导（非常委）═══
    # 11 — 王立新 — 副区长、公安分局长
    {"id": 11, "name": "王立新", "gender": "男", "ethnicity": "汉族",
     "birth": "1967年8月", "birthplace": "待查",
     "education": "大学学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "市公安局党委委员、集宁区政府副区长、公安分局长、党委书记",
     "current_org": "乌兰察布市公安局集宁区分局",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 12 — 李琨 — 副区长（无党派）
    {"id": 12, "name": "李琨", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年1月", "birthplace": "待查",
     "education": "大学学历", "party_join": "无党派", "work_start": "待查",
     "current_post": "集宁区人民政府副区长",
     "current_org": "集宁区人民政府",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 13 — 张鑫 — 副区长（蒙古族）
    {"id": 13, "name": "张鑫", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1987年4月", "birthplace": "待查",
     "education": "内蒙古党校研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区政府党组成员、副区长",
     "current_org": "集宁区人民政府",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # 14 — 杨志清 — 副区长
    {"id": 14, "name": "杨志清", "gender": "女", "ethnicity": "汉族",
     "birth": "1982年4月", "birthplace": "待查",
     "education": "内蒙古党校研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区政府党组成员、副区长",
     "current_org": "集宁区人民政府",
     "source": "https://www.jnq.gov.cn/ldzc/"},
    # ═══ 人大 / 政协 ═══
    # 15 — 王俊 — 人大常委会党组书记、主任候选人
    {"id": 15, "name": "王俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年8月", "birthplace": "待查",
     "education": "内蒙古党校研究生学历", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区人大常委会党组书记、主任候选人",
     "current_org": "集宁区人大常委会",
     "source": "https://www.jnq.gov.cn/rdld/ 领导之窗"},
    # 16 — 陈伟 — 人大常委会主任
    {"id": 16, "name": "陈伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年10月", "birthplace": "内蒙古乌兰察布市兴和县",
     "education": "全日制大专(内蒙古大学电子学与信息系统)；在职本科(中央党校函授经济管理)",
     "party_join": "中共党员", "work_start": "1993年8月",
     "current_post": "集宁区人大常委会主任",
     "current_org": "集宁区人大常委会",
     "source": "https://www.jnq.gov.cn/rdld/ 领导之窗"},
    # 17 — 刘琦 — 政协主席
    {"id": 17, "name": "刘琦", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年10月", "birthplace": "待查",
     "education": "大学学历，农学学士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "集宁区政协党组书记、主席",
     "current_org": "集宁区政协",
     "source": "https://www.jnq.gov.cn/zxld/ 领导之窗"},
    # ═══ 前任领导 ═══
    # 18 — 康海瑞 — 前任区长
    {"id": 18, "name": "康海瑞", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "（前任）集宁区人民政府区长",  # 已调离
     "current_org": "集宁区人民政府",
     "source": "2026-01-28 集宁区十六届人大五次会议《2026年政府工作报告》",
     "confidence": "confirmed", "is_former": True},
]

# ═══════════════════════════════════════════════════════════════════════════
# POSITIONS
# ═══════════════════════════════════════════════════════════════════════════
positions = [
    # 冀宏
    {"person_id": 1, "org_id": 14, "title": "乌兰察布市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "兼任集宁区委书记（高配）"},
    {"person_id": 1, "org_id": 1, "title": "集宁区委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026-07 连任（十五次党代会当选）"},
    # 郝晓亭
    {"person_id": 2, "org_id": 15, "title": "乌兰察布市政府秘书长", "start": "", "end": "2026", "rank": "正处级", "note": "市政府副秘书长/秘书长任上，后调任集宁区"},
    {"person_id": 2, "org_id": 1, "title": "集宁区委副书记", "start": "2026", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "集宁区政府党组书记、代区长", "start": "2026", "end": "present", "rank": "正处级", "note": "现任代区长，主持区政府全面工作"},
    # 孔发鹏
    {"person_id": 3, "org_id": 1, "title": "集宁区委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "政法委书记", "start": "", "end": "present", "rank": "副县级", "note": "负责政法、信访、维稳、乡村振兴、群团等"},
    # 田海军
    {"person_id": 4, "org_id": 10, "title": "区委常委、办公室主任", "start": "", "end": "present", "rank": "副县级", "note": "兼任区委深改办主任"},
    # 沈冬梅
    {"person_id": 5, "org_id": 8, "title": "区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "负责宣传思想文化、意识形态"},
    # 张新
    {"person_id": 6, "org_id": 7, "title": "区委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": "负责组织、干部、编制、人才"},
    # 庞文辉
    {"person_id": 7, "org_id": 5, "title": "区委常委、纪委书记、监委代主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 王志威
    {"person_id": 8, "org_id": 1, "title": "集宁区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "常务副区长、政府党组副书记", "start": "", "end": "present", "rank": "副县级", "note": "兼察哈尔高新技术开发区党工委委员"},
    # 丰雪
    {"person_id": 9, "org_id": 1, "title": "集宁区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长、政府党组成员", "start": "", "end": "present", "rank": "副县级", "note": "文化教育卫生商贸物流大数据等"},
    # 郭辉
    {"person_id": 10, "org_id": 9, "title": "区委常委、统战部部长", "start": "", "end": "present", "rank": "副县级", "note": "政协党组副书记"},
    # 王立新
    {"person_id": 11, "org_id": 11, "title": "公安分局局长、党委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "集宁区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李琨
    {"person_id": 12, "org_id": 2, "title": "集宁区副区长", "start": "", "end": "present", "rank": "副县级", "note": "无党派，城市建设管理"},
    # 张鑫
    {"person_id": 13, "org_id": 2, "title": "集宁区副区长", "start": "", "end": "present", "rank": "副县级", "note": "蒙古族，城建、自然、生态、交通"},
    # 杨志清
    {"person_id": 14, "org_id": 2, "title": "集宁区副区长", "start": "", "end": "present", "rank": "副县级", "note": "女性，工业和信息化"},
    # 王俊
    {"person_id": 15, "org_id": 3, "title": "区人大常委会党组书记、主任候选人", "start": "", "end": "present", "rank": "正处级", "note": "换届过渡/主任候选人"},
    # 陈伟
    {"person_id": 16, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "2026 换届后任主任候选人浮现（王俊）"},
    # 刘琦
    {"person_id": 17, "org_id": 4, "title": "区政协党组书记、主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 康海瑞（前任区长）
    {"person_id": 18, "org_id": 2, "title": "集宁区人民政府区长", "start": "", "end": "2026", "rank": "正处级", "note": "前任区长，2026 年后由郝晓亭代任"},
]

# ═══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════════════
relationships = [
    # 党政一把手搭档：书记 ↔ 区长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "集宁区党政一把手搭档：区委书记与区政府代区长",
     "overlap_org": "中共集宁区委/集宁区人民政府", "overlap_period": "2026-"},
    # 书记 ↔ 各副书记/常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记、政法委书记", "overlap_org": "中共集宁区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委办主任", "overlap_org": "中共集宁区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与宣传部长", "overlap_org": "中共集宁区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与组织部长（干部任免条线密切）", "overlap_org": "中共集宁区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与纪委书记（党风廉政）", "overlap_org": "中共集宁区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区委书记与常务副区长", "overlap_org": "中共集宁区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区委书记与副区长", "overlap_org": "中共集宁区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "区委书记与统战部长", "overlap_org": "中共集宁区委", "overlap_period": ""},
    # 区长 ↔ 副区长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "代区长与常务副区长", "overlap_org": "集宁区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "代区长与副区长", "overlap_org": "集宁区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "代区长与副区长（公安系统）", "overlap_org": "集宁区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "代区长与副区长", "overlap_org": "集宁区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "代区长与副区长", "overlap_org": "集宁区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "代区长与副区长", "overlap_org": "集宁区人民政府", "overlap_period": "2026-"},
    # 前任区长 ↔ 现任代区长 (predecessor/successor)
    {"person_a": 18, "person_b": 2, "type": "predecessor_successor",
     "context": "集宁区老领导（前区长）与现任代区长的职务更替", "overlap_org": "集宁区人民政府",
     "overlap_period": "2026 换届"},
    # 郝晓亭 — 市委/市政府出身 (跨区域条线)
    {"person_a": 2, "person_b": 1, "type": "same_system",
     "context": "郝晓亭曾任乌兰察布市政府秘书长、冀宏为乌兰察布市委常委（市域任职背景）",
     "overlap_org": "乌兰察布市/集宁区", "overlap_period": "2023-2026"},
    # 王俊（人大主任候选人）— 换届衔接
    {"person_a": 15, "person_b": 16, "type": "predecessor_successor",
     "context": "人大常委会主任候选人王俊（书记）与新主任人选、原主任陈伟的换届衔接",
     "overlap_org": "集宁区人大常委会", "overlap_period": "2026"},
]

# ═══════════════════════════════════════════════════════════════════════════
# PERSON JSON FILES
# ═══════════════════════════════════════════════════════════════════════════
TODAY = "20260806"
PJSON_DIR = DATABASE_DIR.parent / "persons"

def write_person_json(person: dict) -> None:
    """Write a deep per-person graph JSON profile to data/persons/."""
    from gov_relation.paths import REPO_ROOT
    # Note: this runs inside a staging script; still target data/persons via canonical path.
    name = person["name"]
    job_map = {"冀宏": "区委书记", "郝晓亭": "区长"}
    job = job_map.get(name, person["current_post"].split("、")[0].replace("，", "_").replace(" ", "_"))
    province = "内蒙古自治区"
    city = "乌兰察布市"
    fname = f"{TODAY}-{province}-{city}-{job}-{name}.json"
    fpath = PJSON_DIR / fname
    import json
    data = {
        "schema_version": "1.0",
        "generated_at": "2026-08-06",
        "investigation_scope": {
            "province": province, "city": city, "region": "集宁区",
            "job": person["current_post"], "task_id": "inner_mongolia_集宁区",
            "time_focus": "现任班子（截止2026-08-06）",
        },
        "identity": {
            "person_id": f"jining_{name}",
            "name": name,
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "education": person.get("education", ""),
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {},
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "as_of": "2026-08-06",
            "is_current_confirmed": not person.get("current_former", False),
            "source": person.get("source", ""),
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "source_register": [],
        "confidence_summary": {
            "identity": "confirmed" if person.get("source") else "plausible",
            "current_role": "confirmed" if person.get("source") else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "早年履历及跨区域调动明细待补",
        },
        "open_questions": [
            {"priority": "high", "question": "早年 (2000-2020) 详细任职履历",
             "why_it_matters": "识别来自何单位、何系统以推断跨区域网络",
             "suggested_queries": [f"{name} 简历 任职 乌兰察布"],
             "last_attempted": "2026-08-06"},
            {"priority": "medium", "question": "调动来源与前任/后任",
             "why_it_matters": "评估干部交流网络",
             "suggested_queries": [f"{name} 任前公示 调任 集宁"],
             "last_attempted": "2026-08-06"},
        ],
        "source_register": [{"id": "S01", "url": "https://www.jnq.gov.cn/ldzc/",
                             "source_type": "official", "reliability": "high",
                             "note": "集宁区领导之窗（现任班子）"}],
    }
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    written = []
    for p in persons:
        if p["name"] in ("冀宏", "郝晓亭"):
            written.append(write_person_json(p))
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSON: {written}")
    print("BUILD OK")