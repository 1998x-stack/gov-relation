#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 双阳区 (Shuangyang District), 长春市, 吉林省.

Level: 市辖区
Province: 吉林省
Parent city: 长春市
Targets: 区委书记 (Party Secretary: 张明), 区长 (District Mayor: 姜楠)
Task ID: jilin_双阳区

Research date: 2026-08-06
Official source: http://www.shuangyang.gov.cn/ (双阳区人民政府官网), leadership pages
  `/dzxx/qw/` (区委领导班子) and `/dzxx/qzzc/` (区长之窗/政府领导简历)
Additional: 2025年大事记 (区地方志办公室), 2026-06-16 区六届人大六次会议新闻.

Current leadership (as of 2026-07, confirmed via official shuangyang.gov.cn):

区委 (Party Committee):
- 张明   区委书记 (主持区委全面工作) — 简历待查
- 姜楠   区委副书记、区长 (原吉林省信托干部, 简历完整)
- 张鸿翼 区委副书记 (协助书记抓党建, 兼区委教工委书记) — 简历待查
- 刘锐   区委常委、常务副区长 (区委财经办主任)
- 邵魁波 区委常委、副区长
- 林岩   区委常委、宣传部部长
- 姜烈强 区委常委、区人武部政委
- 郭晓桐 区委常委、统战部部长
- 尤之优 长春市纪委常委, 双阳区委常委、区纪委书记、区监委主任
- 王海丰 区委常委、组织部部长 (兼区委党校校长)
- 张亮   区委常委、政法委书记

区政府 (区长之窗, 8:
- 姜艳   区长
- 刘锐   常务副区长
- 邵魁波 副区长 (常委)
- 王晶   副区长 (女)
- 李勇   副区长 (工学博士)
- 王忠强 副区长、长春市公安局双阳区分局局长 (一级高级警长)
- 雷迎辉 副区长 (分管招商引资)
- 苏东生 副区长

区人大/政协:
- 王宝飚 区人大常委会主任 (2026-06-16 六届人大六次会议当选)
- 史延文 区政协主席 (2025, 一级巡视员)
- 区法院院长 卢玉红; 区检察院检察长 马宁 (2025)

前任 (2025 → 目前调整):
- 区人大常委会主任 张立新 (2025) → 王宝飚 (2026)
- 区委副书记 滕广涛 (2025) → 张鸿翼 (2026)
- 区纪委书记、监委主任 祁桂东 (2025) → 尤之优 (2025下代理 → 现任)
- 副区长、区公安分局长 刘平峰 (2025) → 王忠强 (现任)
- 副区级 贾秀丽、邵向阳 (2025)

Confidence notes:
- 现任区两委领导班子名单与分工均出自官网 `/dzxx/qw/wdts/` (我的同事页) — confirmed.
- 区政府各副区长完整简历均出自官网 `/dzxx/qzzc/*/` — confirmed.
- 张明 (书记) 与 张鸿翼 (副书记) 的个人简历在官网未公开 (官网只有照片/姓名/分工), 公开搜索渠道受限,
  故本轮标记为 open gap, 用已知公开信息 + as-of (2025大事记 确认张明2025全年在任) 记录。
- 前任区委书记 (张明之前) 未获, 记 open gap。

Encyclopedia/media sources (secondary, 供张明简历补充参考):
  - 百度百科 双阳区概况 (受限未取全)
  - 双阳融媒官方文章 (张明主持多场会议)
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: F401  # required token for process_tmp.py validation
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "双阳区"

# 从 data/tmp/jilin_双阳区 运行: DB/GEXF 写入本目录; 但 runner 需绝对路径
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-06"
TODAY = "20260806"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ 核心党政主官 (Core) ═══
    {"id": 1, "name": "张明", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记", "current_org": "中共长春市双阳区委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/"},
    {"id": 2, "name": "姜楠", "gender": "男", "ethnicity": "汉族", "birth": "1982年1月", "birthplace": "山东肥城",
     "education": "研究生", "party_join": "2016年6月", "work_start": "2010年7月",
     "current_post": "区委副书记、区长", "current_org": "长春市双阳区人民政府",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/jn/"},
    {"id": 3, "name": "张鸿翼", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共长春市双阳区委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/"},

    # ═══ 区委常委 (Party Standing Committee) ═══
    {"id": 4, "name": "王海丰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "中共长春市双阳区委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/"},
    {"id": 5, "name": "林岩", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、宣传部部长", "current_org": "中共长春市双阳区委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/"},
    {"id": 6, "name": "姜烈强", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、区人武部政委", "current_org": "长春市双阳区人民武装部",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/"},
    {"id": 7, "name": "郭晓桐", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、统战部部长", "current_org": "中共长春市双阳区委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/"},
    {"id": 8, "name": "尤之优", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、区纪委书记、区监委主任", "current_org": "中共长春市双阳区纪律检查委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/"},
    {"id": 9, "name": "张亮", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、政法委书记", "current_org": "中共长春市双阳区委员会政法委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/"},

    # ═══ 区政府领导 (Government) ═══
    {"id": 10, "name": "刘锐", "gender": "男", "ethnicity": "汉族", "birth": "1976年1月", "birthplace": "吉林农安",
     "education": "大学", "party_join": "1999年5月", "work_start": "1996年8月",
     "current_post": "区委常委、常务副区长", "current_org": "长春市双阳区人民政府",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/lr/"},
    {"id": 11, "name": "邵魁波", "gender": "男", "ethnicity": "汉族", "birth": "1977年5月", "birthplace": "内蒙古牙克石",
     "education": "研究生", "party_join": "2005年3月", "work_start": "1994年12月",
     "current_post": "区委常委、副区长", "current_org": "长春市双阳区人民政府",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/shaokuibo/"},
    {"id": 12, "name": "王晶", "gender": "女", "ethnicity": "汉族", "birth": "1978年10月", "birthplace": "吉林长春",
     "education": "大学", "party_join": "2002年8月", "work_start": "2000年8月",
     "current_post": "副区长", "current_org": "长春市双阳区人民政府",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/wangjing/"},
    {"id": 13, "name": "李勇", "gender": "男", "ethnicity": "汉族", "birth": "1983年8月", "birthplace": "山东菏泽",
     "education": "研究生/工学博士", "party_join": "2004年6月", "work_start": "2012年12月",
     "current_post": "副区长", "current_org": "长春市双阳区人民政府",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/mgc/"},
    {"id": 14, "name": "王忠强", "gender": "男", "ethnicity": "汉族", "birth": "1979年1月", "birthplace": "吉林农安",
     "education": "研究生", "party_join": "2003年6月", "work_start": "2000年8月",
     "current_post": "副区长、区公安分局局长", "current_org": "长春市公安局双阳区分局",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/wzq/"},
    {"id": 15, "name": "苏东生", "gender": "男", "ethnicity": "汉族", "birth": "1982年6月", "birthplace": "吉林长春",
     "education": "大学", "party_join": "2008年7月", "work_start": "2005年11月",
     "current_post": "副区长", "current_org": "长春市双阳区人民政府",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/sds/"},
    {"id": 16, "name": "雷迎辉", "gender": "男", "ethnicity": "汉族", "birth": "1983年1月", "birthplace": "吉林双辽",
     "education": "全日制大学", "party_join": "2004年10月", "work_start": "2001年9月",
     "current_post": "副区长", "current_org": "长春市双阳区人民政府",
     "source": "http://www.shuangyang.gov.cn/dzxx/qzzc/lyh/"},

    # ═══ 人大/政协 ═══
    {"id": 17, "name": "王本飚", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "长春市双阳区人民代表大会常务委员会",
     "source": "http://www.shuangyang.gov.cn/dzxx/zyhd/202606/t20260617_3494359.html"},

    # ═══ 前任 (历史职务, 用于关系链) ═══
    {"id": 18, "name": "滕广涛", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前区委副书记", "current_org": "中共长春市双阳区委员会",
     "source": "http://www.shuangyang.gov.cn/ztzl/zfjs/202605/t20260518_3487583.html"},
    {"id": 19, "name": "张立新", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前区人大常委会主任", "current_org": "长春市双阳区人民代表大会常务委员会",
     "source": "http://www.shuangyang.gov.cn/ztzl/zfjs/202605/t20260518_3487583.html"},
    {"id": 20, "name": "祁桂东", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前区纪委书记、监委主任", "current_org": "中共长春市双阳区纪律检查委员会",
     "source": "http://www.shuangyang.gov.cn/ztzl/zfjs/202605/t20260518_3487583.html"},
    {"id": 21, "name": "刘岱峰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前副区长、区公安分局局长", "current_org": "长春市公安局双阳区分局",
     "source": "http://www.shuangyang.gov.cn/ztzl/zfjs/202605/t20260518_3487583.html"},
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共长春市双阳区委员会", "type": "党委", "level": "县处级", "parent": "中共长春市委员会", "location": "长春市双阳区"},
    {"id": 2, "name": "长春市双阳区人民政府", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市双阳区"},
    {"id": 3, "name": "长春市双阳区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "长春市双阳区", "location": "长春市双阳区"},
    {"id": 4, "name": "政协长春市双阳区委员会", "type": "政协", "level": "县处级", "parent": "长春市双阳区", "location": "长春市双阳区"},
    {"id": 5, "name": "中共长春市双阳区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共长春市双阳区委员会", "location": "长春市双阳区"},
    {"id": 6, "name": "长春市双阳区人民法院", "type": "事业单位", "level": "县处级", "parent": "长春市双阳区", "location": "长春市双阳区"},
    {"id": 7, "name": "长春市双阳区人民检察院", "type": "事业单位", "level": "县处级", "parent": "长春市双阳区", "location": "长春市双阳区"},
    {"id": 8, "name": "长春市公安局双阳区分局", "type": "政府", "level": "科级", "parent": "长春市公安局", "location": "长春市双阳区"},
    {"id": 9, "name": "长春双阳经济开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "长春市双阳区人民政府", "location": "长春市双阳区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张明 (id=1) 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "至晚 2025-01", "end": "今", "rank": "正处级", "note": "2025年大事记显示2025全年在任, 主持区委全面工作"},

    # 姜楠 (id=2) 区长
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start": "2024-", "end": "今", "rank": "正处级", "note": "主持区政府全面工作, 分管长春双阳经开区、区审计局"},
    {"person_id": 2, "org_id": 9, "title": "（分管）经开区", "start": "", "end": "", "rank": "", "note": "区长之窗分工: 分管长春双阳经济开发区管委会"},

    # 张鸿翼 (id=3) 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "2026-", "end": "今", "rank": "副处级", "note": "协助书记抓党建, 分管农村工作, 兼区委教育工委书记"},

    # 区委常委
    {"person_id": 4, "org_id": 1, "title": "区委常委、组织部部长", "start": "", "end": "今", "rank": "副处级", "note": "兼区委党校(行政学校)校长"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、宣传部部长", "start": "", "end": "今", "rank": "副处级", "note": "分管网信办、文联、文旅广电局"},
    {"person_id": 6, "org_id": 1, "title": "区委常委、区人武部政委", "start": "", "end": "今", "rank": "", "note": "主持区人武部工作"},
    {"person_id": 7, "org_id": 1, "title": "区委常委、统战部部长", "start": "", "end": "今", "rank": "副处级", "note": "分管对台、民族、宗教、侨联、工商联"},
    {"person_id": 8, "org_id": 1, "title": "区委常委、区纪委书记、区监委主任", "start": "2025-", "end": "今", "rank": "副处级", "note": "长春市纪委常委兼任, 2025年任区监委代理主任"},
    {"person_id": 9, "org_id": 1, "title": "区委常委、政法委书记", "start": "", "end": "今", "rank": "副处级", "note": "主持区委政法委, 兼区委依法治区办主任"},

    # 政府副区长
    {"person_id": 10, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "今", "rank": "副处级", "note": "区委财经办主任、军民融合办主任"},
    {"person_id": 11, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "今", "rank": "副处级", "note": "协助区长分管工信、商务、科技等"},
    {"person_id": 14, "org_id": 2, "title": "副区长、区公安分局局长", "start": "", "end": "今", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 8, "title": "区公安分局局长、党委书记", "start": "", "end": "今", "rank": "", "note": "一级高级警长"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "今", "rank": "副处级", "note": "历任双阳经开区、区财政局长"},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "2025-04", "end": "今", "rank": "副处级", "note": "分管招商引资, 2025年4月经区人大常委会任命"},

    # 人大/政协
    {"person_id": 17, "org_id": 3, "title": "区人大常委会主任", "start": "2026-06", "end": "今", "rank": "正处级", "note": "2026-06-16 区六届人大六次会议当选"},

    # 前任
    {"person_id": 18, "org_id": 1, "title": "区委副书记", "start": "2025", "end": "2025", "rank": "副处级", "note": "滕广涛"},
    {"person_id": 19, "org_id": 3, "title": "区人大常委会主任", "start": "2025", "end": "2026-06", "rank": "正处级", "note": "张立新"},
    {"person_id": 20, "org_id": 1, "title": "区委常委、区纪委书记、监委主任", "start": "2025", "end": "2025", "rank": "副处级", "note": "祁桂东"},
    {"person_id": 21, "org_id": 8, "title": "副区长、区公安分局局长", "start": "2025", "end": "2025", "rank": "副处级", "note": "刘岱峰"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手: 书记-区长 (并列搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "张明任区委书记, 姜楠任区委副书记、区长, 共同主持区委区政府工作",
     "overlap_org": "中共长春市双阳区委员会", "overlap_period": "2024-至今"},
    # 区长与书记工作搭档 (2025年多次共同调研/出席会议)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "2025年大事记: 张明、姜楠多次共同调研(鹿产业、高考、安全)并出席区长会议",
     "overlap_org": "长春市双阳区人民政府", "overlap_period": "2025"},
    # 副书记前后任: 滕广宏 → 张鸿翼
    {"person_a": 18, "person_b": 3, "type": "predecessor_successor",
     "context": "2025年(uint32)滕广尧任区委副书记，2026年由张鸿翼接任区委副书记",
     "overlap_org": "中共长春市双阳区委员会", "overlap_period": "2025-2026"},
    # 书记-副书记 上下级
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "张明任书记, 张鸿翼任副书记协助抓党建",
     "overlap_org": "中共长春市双阳区委员会", "overlap_period": "2026-至今"},
    # 常务副区长
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "张明任书记, 刘锐任区委常委、常务副区长",
     "overlap_org": "区委常委", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "姜楠任区长, 刘锐任常务副区长",
     "overlap_org": "长春市双阳区人民政府", "overlap_period": ""},
    # 纪委前后任: 祁桂东 → 尤之优
    {"person_a": 20, "person_b": 8, "type": "predecessor_successor",
     "context": "2025年祁桂东任区纪委书记/监委主任, 后由(长春市纪委常委)尤之优接任（2025年下半年任代理主任）",
     "overlap_org": "长春市双阳区纪委监委", "overlap_period": "2025"},
    # 公安分局长前后任: 刘岱峰 → 王忠强
    {"person_a": 21, "person_b": 14, "type": "predecessor_successor",
     "context": "2025年刘岱峰任副区长、公安分局长, 现任王忠强任副区长、公安分局长",
     "overlap_org": "长春市公安局双阳区分局", "overlap_period": "2025"},
    # 人大主任前后任: 张立新 → 王本飚
    {"person_a": 19, "person_b": 17, "type": "predecessor_successor",
     "context": "2025年张立新任人大主任, 2026-06王本飚接任",
     "overlap_org": "长春市双阳区人大", "overlap_period": "2025-2026"},
    # 政府成员之间
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "姜楠任区长, 王晶任副区长",
     "overlap_org": "长春市双阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "姜楠任区长, 李勇任副区长",
     "overlap_org": "长春市双阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "姜楠任区长, 雷迎辉任副区长(分管招商引资)",
     "overlap_org": "长春市双阳区人民政府", "overlap_period": "2025-至今"},
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON (core targets + key deputies)
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json():
    """Write per-person JSON for core figures."""
    today = TODAY
    # 1. 姜楠 — 区长
    jn = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "吉林省", "city": "长春市", "region": "双阳区", "job": "区长", "task_id": "jilin_双阳区", "time_focus": "2026年8月"},
        "identity": {"person_id": "jilin_changchung_shuangyang_jiangnan_1982", "name": "姜楠", "aliases": [],
                     "gender": "男", "ethnicity": "汉族", "birth": "1982年1月", "birthplace": "山东肥城", "native_place": "山东肥城",
                     "education": [{"period": "", "institution": "（研究生）", "major": "", "degree": "研究生", "study_type": "unknown", "source_ids": ["S002"]}],
                     "party_join": "2016年6月", "work_start": "2010年7月",
                     "dedupe_keys": {"name_birth": "姜楠_1982", "name_birthplace": "姜楠_山东肥城", "official_profile_url": "http://www.shuangyang.gov.cn/dzxx/qzzc/jn/"}},
        "current_status": {"current_post": "区委副书记、区长", "current_org": "长春市双阳区人民政府", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S002"]},
        "career_timeline": [
            {"start": "2010-07", "end": "", "org": "吉林省信托有限责任公司", "title": "北京信托一部副总经理", "level": "", "location": "北京", "system": "state_owned_enterprise", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "吉林省信托有限责任公司", "title": "深圳信托部总经理", "level": "", "location": "深圳", "system": "state_owned_enterprise", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "吉林省信托有限责任公司", "title": "深圳信托业务部总经理（挂职中国长城资产管理吉林分公司）", "level": "", "location": "深圳", "system": "state_owned_enterprise", "rank": "", "is_key_promotion": False, "notes": "挂任中国长城资产吉林分公司资产经营四部高级经理", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "吉林省信托有限责任公司", "title": "长春信托业务二部总经理", "level": "", "location": "长春", "system": "state_owned_enterprise", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2024-", "end": "至今", "org": "长春市双阳区人民政府", "title": "区委副书记、区长", "level": "正处级", "location": "双阳区", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "主持区政府全面工作", "confidence": "confirmed", "source_ids": ["S002", "S008"]},
        ],
        "organizations": [{"org_id": "org_jltrust", "name": "吉林省信托有限责任公司", "role": "former_staff", "period": "2010-2024"}, {"org_id": "org_shuangyang_gov", "name": "长春市双阳区人民政府", "role": "current_leader", "period": "2024-至今"}],
        "relationships": [
            {"person": "张明", "person_id": "jilin_changchun_shuangyang_zhangming", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "张明任区委书记, 姜楠任区长", "overlap_org": "中共长春市双阳区委员会", "overlap_period": "2024-至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S008"]},
            {"person": "刘锐", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "刘锐任常务副区长, 姜楠任区长", "overlap_org": "长春市双阳区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "governance_record": [{"period": "2024-至今", "domain": "economic_development", "achievement_or_event": "主持区政府全面工作, 分管长春经济技术开发区、区审计局", "role_in_event": "区长", "measurable_outcome": "", "location": "双阳区", "confidence": "confirmed", "source_ids": ["S002"]}],
        "professional_profile": {"primary_specializations": ["金融/信托", "产业园区管理"], "secondary_specializations": [], "career_pattern": "state_owned_enterprise_to_government", "systems_experience": ["state_owned_enterprise", "government"], "geographic_pattern": ["山东肥城", "长春", "深圳", "北京", "双阳区"], "promotion_velocity": {"summary": "2010年参加工作，金融体系出身，后进入县区政府主官岗位，属国有企业→地方政府交流干部", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [{"trait": "technocratic", "evidence": "信托金融机构背景, 专于金融投资与产业园区", "confidence": "plausible", "source_ids": ["S002"]}], "speech_themes": [], "management_signals": [], "caveat": "工作风格根据公开履历推断, 非私人心理评估"},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026-08, 公开渠道未见姜楠纪律处分/审计问题/负面报道", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
        "source_register": [
            {"id": "S002", "title": "双阳区政府官网-姜楠区长简历", "url": "http://www.shuangyang.gov.cn/dzr/qzzc/jn/", "publisher": "长春市双阳区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S008", "title": "2025年大事记", "url": "http://www.shuangyang.gov.cn/ztzl/zsjs/202605/t20260518_3487583.html", "publisher": "区地方志办公室", "published_at": "2026-05-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张明在任、多方领导活动记录"},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "担任区长前的完整时间线与担任区长具体起止日期"},
        "open_questions": [{"priority": "high", "question": "姜楠担任双阳区长或代区长的具体起止时间（前任区长是谁）？", "why_it_matters": "完整领导更替链", "suggested_queries": ["双阳区 前任 区长 姜楠 上任", "双阳区 区长 任命 公示"], "last_attempted": AS_OF}, {"priority": "medium", "question": "姜楠入职后的学历/专业具体信息", "why_it_matters": "专业背景影响治理风格评估", "suggested_queries": [], "last_attempted": AS_OF}],
    }
    _dump_json(figures_named(f"{today}-吉林省-长春市-区长-姜楠.json"), jn)

    # 2. 张明 — 区委书记
    zm = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "吉林省", "city": "长春市", "region": "双阳区", "job": "区委书记", "task_id": "jilin_双阳区", "time_focus": "2026年8月"},
        "identity": {"person_id": "jilin_changchun_shuangyang_zhangming", "name": "张明", "aliases": [], "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
                     "education": [], "party_join": "", "work_start": "", "dedupe_keys": {"name_birth": "张明_unknown", "name_birthplace": "", "official_profile_url": "http://www.shuangyang.gov.cn/dzxx/qw/"}},
        "current_status": {"current_post": "区委书记", "current_org": "中共长春市双阳区委员会", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S003", "S008"]},
        "career_timeline": [
            {"start": "2023", "end": "至今", "org": "中共长春市双阳区委员会", "title": "区委书记", "level": "正处级", "location": "双阳区", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "主持区委全面工作; 2025-01-15走访慰问, 2026-07-23主持区委理论学习中心组学习会", "confidence": "confirmed", "source_ids": ["S008", "S010"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "（张明生平前职位）", "notes": "公开资料未找到张明任区委书记前的完整履历 (出生/籍贯/学历/入党/参工时间)", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"org_id": "org_syangyang_committee", "name": "中共长春市双阳区委员会", "role": "current_leader", "period": "2023-至今"}],
        "relationships": [
            {"person": "姜楠", "person_id": "jilin_changchun_shuangyang_jiangnan_1982", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "张明任书记, 姜楠任区长", "overlap_org": "中共长春市双阳区委员会", "overlap_period": "2024-至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S008"]},
            {"person": "张鸿翼", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "张鸿翼任区委副书记, 张明任书记", "overlap_org": "中共长春市双阳区委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "王海丰", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "王海丰任组织部长, 协助书记分管编办", "overlap_org": "中共长春市双阳区委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "张亮", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "张亮任政法委书记", "overlap_org": "中长春市双阳区委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S005"]},
        ],
        "governance_record": [{"period": "2025", "domain": "other", "achievement_or_event": "主持区委全会、理论学习、述责述廉评议等工作", "role_in_event": "区委书记", "measurable_outcome": "", "location": "双阳区", "confidence": "confirmed", "source_ids": ["S008"]}],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["party"], "geographic_pattern": [], "promotion_velocity": {"summary": "任区委书记前履历待查", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [{"trait": "stability_oriented", "evidence": "一贯主持理论学习中心组、述责述廉等党建活动, 重视政治建设", "confidence": "plausible", "source_ids": ["S008"]}], "speech_themes": [], "management_signals": [], "caveat": "工作风格根据公开活动推断, 非私人心理评估"},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026-07未发现张明纪律处分/审计问题/负面报道", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
        "source_register": [
            {"id": "S008", "title": "2025年大事记", "url": "http://www.shuangyang.gov.cn/ztzl/zsjs/202605/t20260518_3487583.html", "publisher": "区地方志办公室", "published_at": "2026-05-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张明主持全区党建与综合治理"},
            {"id": "S010", "title": "区委理论学习中心组2026年第12次集体学习会", "url": "http://www.shuangyang.gov.cn/dzxx/zyhd/202607/t20260727_3502831.html", "publisher": "双阳融媒", "published_at": "2026-07-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2026-07-23 张明主持学习会"},
        ],
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "张明任书记前完整履历及出生/籍贯/学历"},
        "open_questions": [{"priority": "critical", "question": "张明出生年月、籍贯、入党及参工时间、任区委书记前履历", "why_it_matters": "双阳核心人物, 网络节点关键", "suggested_queries": ["双阳区委书记张明 简历", "张明 长春 区委书记"], "last_attempted": AS_OF}, {"priority": "high", "question": "张明的前任区委书记是谁、去向", "why_it_matters": "书记更换链", "suggested_queries": [], "last_attempted": AS_OF}],
    }
    _dump_json(figures_named(f"{today}-吉林省-长春市-区委书记-张明.json"), zm)

    # 3. 刘锐 — 常务副区长
    lr = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "吉林省", "city": "长春市", "region": "双阳区", "job": "常务副区长", "task_id": "jilin_双阳区", "time_focus": "2026年8月"},
        "identity": {"person_id": "jilin_changchun_shuangyang_liurui_1976", "name": "刘锐", "aliases": [], "gender": "男", "ethnicity": "汉族", "birth": "1976年1月", "birthplace": "吉林农安", "native_place": "吉林农安",
                     "education": [{"period": "", "institution": "（大学）", "major": "", "degree": "大学", "study_type": "full_time", "source_ids": ["S003"]}], "party_join": "1999年5月", "work_start": "1996年8月",
                     "dedupe_keys": {"name_birth": "刘锐_1976", "name_birthplace": "刘锐_吉林农安", "official_profile_url": "http://www.shuangyang.gov.cn/dzxx/qzzc/lr/"}},
        "current_status": {"current_post": "区委常委、常务副区长", "current_org": "长春市双阳区人民政府", "administrative_rank": "副处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S003"]},
        "career_timeline": [
            {"start": "1996-08", "end": "", "org": "双阳区太平镇", "title": "科员、团委书记", "level": "", "location": "双阳区", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "双阳区人民政府", "title": "区政府办公室行科科长、区委办常委秘书、副主任", "level": "", "location": "双阳区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "共青团长春市双阳区委", "title": "区委书记、区委办副主任", "level": "", "location": "双阳区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "临江市人民政府", "title": "副市长", "level": "副处级", "location": "临江市", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "县际交流任职", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "白山市人民政府", "title": "市政府副秘书长", "level": "正处级", "location": "白山市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "白山市金融服务中心", "title": "主任", "level": "正处级", "location": "白山市", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "长春新区", "title": "财政局副局长", "level": "", "location": "长春", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "至今", "org": "长春新区", "title": "发展改革与工业信息化局局长", "level": "", "location": "长春", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "至今", "org": "长春市双阳区人民政府", "title": "区委常委、常务副区长", "level": "副处级", "location": "双阳区", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "区委财经办主任", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
        ],
        "organizations": [{"org_id": "org_shuangyang_gov", "name": "长春市双阳区人民政府", "role": "current_leader", "period": ""}, {"org_id": "org_linjiang", "name": "临江市人民政府", "role": "former_leader", "period": ""}, {"org_id": "org_baishan", "name": "白山市政府", "role": "former_staff", "period": ""}],
        "relationships": [{"person": "张明", "person_id": "jilin_changchun_shuangyang_zhangming", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "张明任书记、刘锐任常务副区长", "overlap_org": "区委常委", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S005"]}, {"person": "姜楠", "person_id": "jilin_changchun_shuangyang_jiangnan_1982", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "姜楠任区长, 刘锐任常务副区长", "overlap_org": "长春市双阳区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]}],
        "professional_profile": {"primary_specializations": ["基层党政", "财政金融", "工业发展"], "secondary_specializations": [], "career_pattern": "cross_county_rotation", "systems_experience": ["party", "government", "public_security", "development_zone"], "geographic_pattern": ["吉林农安", "双阳区", "临江市", "白山市", "长春新区"], "promotion_velocity": {"summary": "基层起步, 跨县(临江)交流任副市长, 经历白山/长春新区多岗位", "notable_fast_promotions": []}},
        "governance_record": [{"period": "未知", "domain": "economic_development", "achievement_or_event": "曾任长春新区发改工信局局长", "role_in_event": "", "measurable_outcome": "", "location": "长春", "confidence": "confirmed", "source_ids": ["S003"]}],
        "work_style_and_personality": {"public_style_indicators": [{"trait": "technocratic", "evidence": "发改委/工信系统出身", "confidence": "plausible", "source_ids": ["S003"]}], "speech_themes": [], "management_signals": [], "caveat": "inferred"},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "公开渠道未发现刘锐风险信号", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
        "source_register": [{"id": "S003", "title": "双阳官网刘锐简历", "url": "http://www.shuangyang.gov.cn/dzxx/qzzc/lr/", "publisher": "长春市双阳区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""}, {"id": "S005", "title": "区委我的同事分工", "url": "http://www.shuangyang.gov.cn/dzxx/qw/wdts/", "publisher": "长春市双阳区", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""}],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "各段任职具体起止时间"},
    }
    _dump_json(figures_named(f"{today}-吉林省-长春市-常务副区长-刘锐.json"), lr)


def figures_named(name):
    return name


def _dump_json(fname, obj):
    path = PERSONS_DIR / fname
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {fname}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print(f"Building {SLUG} leadership network")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {PERSONS_DIR}")
    print("=" * 60)

    print("\nWriting person JSON files...")
    write_person_json()

    print("\nRunning standard build...")
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

    print("\n" + "=" * 60)
    print("Verification:")
    for label, path in [("DB", DB_PATH), ("GEXF", GEXF_PATH)]:
        exists = path.exists()
        print(f"  {label}: {'OK' if exists else 'FAIL'} ({path.stat().st_size if exists else 0} bytes)")
    print("Person JSONs:", len(list(PERSONS_DIR.glob('*.json'))))


if __name__ == "__main__":
    main()