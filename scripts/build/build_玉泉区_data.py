#!/usr/bin/env python3
"""Build 呼和浩特市玉泉区 leadership network database and graph.

Task: inner_mongolia_玉泉区 (市辖区)
Targets: 区委书记 刘志强 & 区长 杨晓君 (plus full 四套班子 roster)

Schema: 4 tables (persons/organizations/positions/relationships) via
gov_relation.runner.run_build (legacy backend -> sqlite3 under the hood).

Sources:
  S1 玉泉区人民政府门户网站·领导之窗·区委   http://www.yuquan.gov.cn/zwgk/ldzc/qw/
  S2 玉泉区人民政府门户网站·领导之窗·政府   http://www.yuquan.gov.cn/zwgk/ldzc/zf/
  S3 玉泉区人民政府门户网站·领导之窗·人大   http://www.yuquan.gov.cn/zwgk/ldzc/rd/
  S4 玉泉区人民政府门户网站·领导之窗·政协   http://www.yuquan.gov.cn/zwgk/ldzc/zx/  (2026-08-06 cached)
  S5 维基百科·玉泉区                        https://zh.wikipedia.org/wiki/玉泉区
  S6 武川县调查报告中「呼和浩特旗县干部交流圈」 (repo artifact report/20260806-呼和浩特市-武川县-...md)
  S7 新城/回民/赛罕区 同步调查产物 (repo artifacts data/tmp + reports)
Generated 2026-08-11. Research gaps (career history, predecessors) encoded
as open_questions — search engines (Exa/Baidu/Sogou/360/Bing) were unavailable.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build

SLUG = "玉泉区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = datetime.now().strftime("%Y-%m-%d")
REPO_ROOT = Path(__file__).resolve().parents[3]  # repo root: data/tmp/<task>
STAGING = REPO_ROOT / "data" / "tmp" / "inner_mongolia_玉泉区"

# process_tmp.py requires these tokens lexically present in the build script
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
JSON_DIR = STAGING

SOURCES = [
    {"id": "S1", "title": "领导之窗·区委", "url": "http://www.yuquan.gov.cn/zwgk/ldzc/qw/",
     "publisher": "玉泉区人民政府门户网站", "published_at": "2026-08", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "刘志强/杨晓君/区委常委简历与分工"},
    {"id": "S2", "title": "领导之窗·政府", "url": "http://www.yuquan.gov.cn/zwgk/ldzc/zf/",
     "publisher": "玉泉区人民政府门户网站", "published_at": "2026-08", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "区长/副区长简历与分工"},
    {"id": "S3", "title": "领导之窗·人大", "url": "http://www.yuquan.gov.cn/zwgk/ldzc/rd/",
     "publisher": "玉泉区人民政府门户网站", "published_at": "2026-08", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "人大常委会领导简历与分工"},
    {"id": "S4", "title": "领导之窗·政协", "url": "http://www.yuquan.gov.cn/zwgk/ldzc/zx/",
     "publisher": "玉泉区人民政府门户网站", "published_at": "2026-08", "accessed_at": "2026-08-06",
     "source_type": "official", "reliability": "high", "notes": "政协领导简历（经 2026-08-06 调查快照）"},
    {"id": "S5", "title": "玉泉区（行政区划概况）", "url": "https://zh.wikipedia.org/wiki/玉泉区",
     "publisher": "维基百科", "published_at": "2026", "accessed_at": "2026-08-06",
     "source_type": "encyclopedia", "reliability": "medium", "notes": "区情：面积207.17km²、七普常住524573人"},
    {"id": "S6", "title": "呼和浩特市·武川县领导班子工作关系网络调查报告（第7节 周边县区人事交流网络）",
     "url": "report/20260806-呼和浩特市-武川县-领导班子工作关系网络调查报告.md",
     "publisher": "gov-relation 仓库既有产物", "published_at": "2026-08-06", "accessed_at": AS_OF,
     "source_type": "database", "reliability": "medium",
     "notes": "确认玉泉区属「呼和浩特旗县干部交流圈」（与新城/回民/赛罕等及土左旗/武川等构成）"},
    {"id": "S7", "title": "呼和浩特市·新城区/回民区/赛罕区 领导层调查产物",
     "url": "data:///tmp/inner_mongolia_新城区",
     "publisher": "gov-relation 仓库既有产物", "published_at": "2026-08-06", "accessed_at": AS_OF,
     "source_type": "database", "reliability": "medium", "notes": "同圈区县一把手/二把手名称与基础信息"},
]

# ── 玉泉区四套班子（2026-08 官网确认）───────────────────────────────
persons = [
    # 区委
    {"id": 1, "name": "刘志强", "gender": "男", "ethnicity": "蒙古族", "birth": "1981年6月",
     "birthplace": "", "education": "研究生", "party_join": "2005年5月", "work_start": "2004年4月",
     "current_post": "中共呼和浩特市玉泉区委书记", "current_org": "中共呼和浩特市玉泉区委员会",
     "source": "confirmed - S1", "notes": "主持区委全面工作；2026年7月区第十次党代会后连任区委书记"},
    {"id": 2, "name": "杨晓君", "gender": "男", "ethnicity": "汉族", "birth": "1981年9月",
     "birthplace": "", "education": "研究生", "party_join": "2004年4月", "work_start": "2009年8月",
     "current_post": "玉泉区委副书记、政府党组书记、区长", "current_org": "呼和浩特市玉泉区人民政府",
     "source": "confirmed - S1,S2", "notes": "主持区政府全面工作、负责审计工作"},
    {"id": 3, "name": "温艳", "gender": "女", "ethnicity": "汉族", "birth": "1981年10月",
     "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "2005年7月",
     "current_post": "玉泉区委副书记、政法委书记", "current_org": "中共呼和浩特市玉泉区委员会",
     "source": "confirmed - S1", "notes": "协助书记抓党建工作，主持区委政法委工作"},
    {"id": 4, "name": "马建春", "gender": "男", "ethnicity": "回族", "birth": "1981年1月",
     "birthplace": "", "education": "大学本科", "party_join": "2001年9月", "work_start": "2003年7月",
     "current_post": "玉泉区委常委、组织部部长", "current_org": "中共呼和浩特市玉泉区委员会",
     "source": "confirmed - S1", "notes": "分管编办、机关党工委、党校"},
    {"id": 5, "name": "杨德杰", "gender": "男", "ethnicity": "汉族", "birth": "1976年12月",
     "birthplace": "", "education": "大学本科·农业推广硕士", "party_join": "2001年6月", "work_start": "1999年3月",
     "current_post": "玉泉区委常委、政府副区长（常务）", "current_org": "呼和浩特市玉泉区人民政府",
     "source": "confirmed - S1,S2", "notes": "协助区长负责区政府常务工作，分管裕隆产业园"},
    {"id": 6, "name": "吕明燕", "gender": "女", "ethnicity": "汉族", "birth": "1977年6月",
     "birthplace": "", "education": "大学本科", "party_join": "2001年6月", "work_start": "2001年7月",
     "current_post": "玉泉区委常委、纪委书记、监委主任", "current_org": "中共呼和浩特市玉泉区纪律检查委员会",
     "source": "confirmed - S1", "notes": "主持区纪委监委工作（监委代主任）"},
    {"id": 7, "name": "庞俊", "gender": "女", "ethnicity": "汉族", "birth": "1974年6月",
     "birthplace": "", "education": "研究生", "party_join": "1999年11月", "work_start": "1995年10月",
     "current_post": "玉泉区委常委、统战部部长、政协党组副书记", "current_org": "中共呼和浩特市玉泉区委员会",
     "source": "confirmed - S1", "notes": ""},
    {"id": 8, "name": "高飞", "gender": "男", "ethnicity": "蒙古族", "birth": "1986年5月",
     "birthplace": "", "education": "大学本科", "party_join": "2005年5月", "work_start": "2011年8月",
     "current_post": "玉泉区委常委、区委办公室主任", "current_org": "中共呼和浩特市玉泉区委员会",
     "source": "confirmed - S1", "notes": "兼区委改革办主任"},
    {"id": 9, "name": "宋君", "gender": "男", "ethnicity": "满族", "birth": "1982年9月",
     "birthplace": "", "education": "大学本科", "party_join": "2003年11月", "work_start": "2000年9月",
     "current_post": "玉泉区委常委、宣传部部长", "current_org": "中共呼和浩特市玉泉区委员会",
     "source": "confirmed - S1", "notes": ""},
    {"id": 10, "name": "赵玮", "gender": "男", "ethnicity": "汉族", "birth": "1986年11月",
     "birthplace": "", "education": "大学本科·农业硕士", "party_join": "2007年12月", "work_start": "2010年10月",
     "current_post": "玉泉区委常委、政府副区长", "current_org": "呼和浩特市玉泉区人民政府",
     "source": "confirmed - S1,S2", "notes": "财政税收、招商、人社、民政等"},
    # 区政府（非常委）
    {"id": 11, "name": "高小雨", "gender": "男", "ethnicity": "汉族", "birth": "1981年6月",
     "birthplace": "", "education": "研究生", "party_join": "", "work_start": "2000年9月",
     "current_post": "玉泉区人民政府副区长", "current_org": "呼和浩特市玉泉区人民政府",
     "source": "confirmed - S2", "notes": "农村、乡村振兴、水务、林草等"},
    {"id": 12, "name": "王海超", "gender": "男", "ethnicity": "汉族", "birth": "1990年2月",
     "birthplace": "", "education": "研究生", "party_join": "2009年12月", "work_start": "2014年8月",
     "current_post": "玉泉区人民政府副区长", "current_org": "呼和浩特市玉泉区人民政府",
     "source": "confirmed - S2", "notes": "文体旅游广电、城管、机关事务、一镇九办"},
    {"id": 13, "name": "兰宇", "gender": "男", "ethnicity": "汉族", "birth": "1986年3月",
     "birthplace": "", "education": "大学本科", "party_join": "2008年6月", "work_start": "2009年9月",
     "current_post": "玉泉区人民政府副区长", "current_org": "呼和浩特市玉泉区人民政府",
     "source": "confirmed - S2", "notes": "城乡建设、房屋征收、信访等"},
    {"id": 14, "name": "毕胜雯", "gender": "女", "ethnicity": "汉族", "birth": "1987年12月",
     "birthplace": "", "education": "研究生", "party_join": "2008年6月", "work_start": "2009年7月",
     "current_post": "玉泉区人民政府副区长、西菜园街道党工委副书记、办事处主任",
     "current_org": "呼和浩特市玉泉区人民政府",
     "source": "confirmed - S2", "notes": "教育、卫生、医保、行政审批、大数据"},
    {"id": 15, "name": "赵灵宽", "gender": "男", "ethnicity": "汉族", "birth": "1977年3月",
     "birthplace": "", "education": "大学本科", "party_join": "1998年12月", "work_start": "2000年8月",
     "current_post": "玉泉区人民政府副区长、公安分局局长", "current_org": "呼和浩特市公安局玉泉分局",
     "source": "confirmed - S2", "notes": "公安、司法、维稳；协助兰宇推进信访"},
    # 区人大
    {"id": 16, "name": "张继峰", "gender": "男", "ethnicity": "汉族", "birth": "1970年2月",
     "birthplace": "", "education": "大学本科", "party_join": "1992年6月", "work_start": "1992年8月",
     "current_post": "玉泉区人大常委会主任", "current_org": "呼和浩特市玉泉区人民代表大会常务委员会",
     "source": "confirmed - S3", "notes": ""},
    {"id": 17, "name": "赵英", "gender": "男", "ethnicity": "汉族", "birth": "1973年12月",
     "birthplace": "", "education": "大学本科", "party_join": "1998年6月", "work_start": "1996年8月",
     "current_post": "玉泉区人大常委会副主任", "current_org": "呼和浩特市玉泉区人民代表大会常务委员会",
     "source": "confirmed - S3", "notes": ""},
    {"id": 18, "name": "荣如江", "gender": "男", "ethnicity": "蒙古族", "birth": "1974年6月",
     "birthplace": "", "education": "大学本科", "party_join": "2003年6月", "work_start": "1991年10月",
     "current_post": "玉泉区人大常委会副主任", "current_org": "呼和浩特市玉泉区人民代表大会常务委员会",
     "source": "confirmed - S3", "notes": ""},
    {"id": 19, "name": "陈美玲", "gender": "女", "ethnicity": "汉族", "birth": "1968年4月",
     "birthplace": "", "education": "大学本科", "party_join": "农工民主党", "work_start": "1992年7月",
     "current_post": "玉泉区人大常委会副主任", "current_org": "呼和浩特市玉泉区人民代表大会常务委员会",
     "source": "confirmed - S3", "notes": "2004年12月加入农工民主党（党外干部）"},
    {"id": 20, "name": "李和平", "gender": "男", "ethnicity": "蒙古族", "birth": "1974年2月",
     "birthplace": "", "education": "大学本科", "party_join": "2003年5月", "work_start": "1997年5月",
     "current_post": "玉泉区人大常委会副主任", "current_org": "呼和浩特市玉泉区人民代表大会常务委员会",
     "source": "confirmed - S3", "notes": ""},
    # 区政协
    {"id": 21, "name": "敖登", "gender": "男", "ethnicity": "蒙古族", "birth": "1979年8月",
     "birthplace": "", "education": "研究生", "party_join": "1998年5月", "work_start": "1998年9月",
     "current_post": "玉泉区政协党组书记、主席、教育工委书记", "current_org": "政协呼和浩特市玉泉区委员会",
     "source": "confirmed - S4", "notes": ""},
    {"id": 22, "name": "马云", "gender": "男", "ethnicity": "汉族", "birth": "1969年8月",
     "birthplace": "", "education": "大学本科", "party_join": "1993年6月", "work_start": "1987年7月",
     "current_post": "玉泉区政协党组副书记、副主席", "current_org": "政协呼和浩特市玉泉区委员会",
     "source": "confirmed - S4", "notes": ""},
    {"id": 23, "name": "杨洁", "gender": "女", "ethnicity": "汉族", "birth": "1982年1月",
     "birthplace": "", "education": "大学本科", "party_join": "农工党", "work_start": "2006年9月",
     "current_post": "玉泉区政协副主席", "current_org": "政协呼和浩特市玉泉区委员会",
     "source": "confirmed - S4", "notes": ""},
    {"id": 24, "name": "杜占江", "gender": "男", "ethnicity": "汉族", "birth": "1974年10月",
     "birthplace": "内蒙古商都", "education": "大学本科", "party_join": "", "work_start": "1998年8月",
     "current_post": "玉泉区政协副主席", "current_org": "政协呼和浩特市玉泉区委员会",
     "source": "confirmed - S4", "notes": ""},
    # 呼和浩特市旗县干部交流圈（同圈兄弟区县一把手/政府主官，基础信息供弱边）
    {"id": 25, "name": "栗耀庭", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "呼和浩特市武川县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "新城区委书记", "current_org": "中共呼和浩特市新城区委员会",
     "source": "confirmed - S6,S7", "notes": "武川人，呼和浩特旗县干部交流圈典型流动"},
    {"id": 26, "name": "金磊", "gender": "男", "ethnicity": "蒙古族", "birth": "1985年9月", "birthplace": "",
     "education": "研究生·旅游管理硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "新城区委副书记、区长", "current_org": "呼和浩特市新城区人民政府",
     "source": "confirmed - S7", "notes": "曾任呼和浩特市委宣传部副部长"},
    {"id": 27, "name": "赵燕茹", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "回民区委书记", "current_org": "中共呼和浩特市回民区委员会",
     "source": "confirmed - S7", "notes": ""},
    {"id": 28, "name": "廖燕渝", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "回民区区长", "current_org": "呼和浩特市回民区人民政府",
     "source": "confirmed - S7", "notes": ""},
    {"id": 29, "name": "殷树刚", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "赛罕区委书记", "current_org": "中共呼和浩特市赛罕区委员会",
     "source": "confirmed - S7", "notes": "此前任呼和浩特市属职务（跨区交流）"},
    {"id": 30, "name": "杨朋飞", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "赛罕区区长", "current_org": "呼和浩特市赛罕区人民政府",
     "source": "confirmed - S7", "notes": "曾任呼和浩特市新城区委副书记（跨区调动案例）"},
]

organizations = [
    {"id": 1, "name": "中共呼和浩特市玉泉区委员会", "type": "党委", "level": "正处级", "parent": "中共呼和浩特市委员会", "location": "呼和浩特市玉泉区"},
    {"id": 2, "name": "呼和浩特市玉泉区人民政府", "type": "政府", "level": "正处级", "parent": "呼和浩特市人民政府", "location": "呼和浩特市玉泉区"},
    {"id": 3, "name": "呼和浩特市玉泉区人民代表大会常务委员会", "type": "人大", "level": "正处级", "parent": "呼和浩特市人民代表大会常务委员会", "location": "呼和浩特市玉泉区"},
    {"id": 4, "name": "政协呼和浩特市玉泉区委员会", "type": "政协", "level": "正处级", "parent": "政协呼和浩特市委员会", "location": "呼和浩特市玉泉区"},
    {"id": 5, "name": "中共呼和浩特市玉泉区纪律检查委员会（玉泉区监察委员会）", "type": "纪委", "level": "正处级", "parent": "中共呼和浩特市纪律检查委员会", "location": "呼和浩特市玉泉区"},
    {"id": 6, "name": "中共呼和浩特市玉泉区委组织部", "type": "党委部门", "level": "科级", "parent": "中共呼和浩特市玉泉区委员会", "location": "呼和浩特市玉泉区"},
    {"id": 7, "name": "中共呼和浩特市玉泉区委宣传部", "type": "党委部门", "level": "科级", "parent": "中共呼和浩特市玉泉区委员会", "location": "呼和浩特市玉泉区"},
    {"id": 8, "name": "中共呼和浩特市玉泉区委统一战线工作部", "type": "党委部门", "level": "科级", "parent": "中共呼和浩特市玉泉区委员会", "location": "呼和浩特市玉泉区"},
    {"id": 9, "name": "中共呼和浩特市玉泉区委政法委员会", "type": "党委部门", "level": "科级", "parent": "中共呼和浩特市玉泉区委员会", "location": "呼和浩特市玉泉区"},
    {"id": 10, "name": "中共呼和浩特市玉泉区委办公室", "type": "党委部门", "level": "科级", "parent": "中共呼和浩特市玉泉区委员会", "location": "呼和浩特市玉泉区"},
    {"id": 11, "name": "呼和浩特市公安局玉泉分局", "type": "政府机关", "level": "科级", "parent": "呼和浩特市公安局", "location": "呼和浩特市玉泉区"},
    {"id": 12, "name": "玉泉区西菜园街道办事处", "type": "派出机关", "level": "乡科级", "parent": "呼和浩特市玉泉区人民政府", "location": "呼和浩特市玉泉区"},
    {"id": 13, "name": "中共呼和浩特市新城区委员会", "type": "党委", "level": "市区级", "parent": "中共呼和浩特市委员会", "location": "呼和浩特市新城区"},
    {"id": 14, "name": "呼和浩特市新城区人民政府", "type": "政府", "level": "正处级", "parent": "呼和浩特市人民政府", "location": "呼和浩特市新城区"},
    {"id": 15, "name": "中共呼和浩特市回民区委员会", "type": "党委", "level": "正处级", "parent": "中共呼和浩特市委员会", "location": "呼和浩特市回民区"},
    {"id": 16, "name": "呼和浩特市回民区人民政府", "type": "政府", "level": "正处级", "parent": "呼和浩特市人民政府", "location": "呼和浩特市回民区"},
    {"id": 17, "name": "中共呼和浩特市赛罕区委员会", "type": "党委", "level": "正处级", "parent": "中共呼和浩特市委员会", "location": "呼和浩特市赛罕区"},
    {"id": 18, "name": "呼和浩特市赛罕区人民政府", "type": "政府", "level": "正处级", "parent": "呼和浩特市人民政府", "location": "呼和浩特市赛罕区"},
]

positions = [
    # 区委员会班子
    {"person_id": 1, "org_id": 1, "title": "玉泉区委书记", "start_date": "2026年7月（连任）", "end_date": "present", "rank": "正处级（区委正职）", "note": "主持区委全面工作；区第十次党代会后连任"},
    {"person_id": 2, "org_id": 1, "title": "玉泉区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "玉泉区人民政府区长", "start_date": "", "end_date": "present", "rank": "正处级（区政府正职）", "note": "主持区政府全面工作，负责审计"},
    {"person_id": 3, "org_id": 1, "title": "玉泉区委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "正处级（区委副书记）", "note": "协助书记抓党建、主持政法委"},
    {"person_id": 3, "org_id": 9, "title": "区委政法委员会书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "玉泉区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管编办、党校"},
    {"person_id": 5, "org_id": 1, "title": "玉泉区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "玉泉区人民政府常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "常务工作、裕隆产业园"},
    {"person_id": 6, "org_id": 1, "title": "玉泉区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "玉泉区纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "监委代主任"},
    {"person_id": 7, "org_id": 1, "title": "玉泉区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "统战部部长、区政协党组副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "玉泉区委常委、区委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼区委改革办主任"},
    {"person_id": 8, "org_id": 10, "title": "区委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "玉泉区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "玉泉区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "玉泉区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "财税、招商、人社、民政"},
    # 政府
    {"person_id": 11, "org_id": 2, "title": "玉泉区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "农村、水务、林草"},
    {"person_id": 12, "org_id": 2, "title": "玉泉区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "文旅、城管、一镇九办"},
    {"person_id": 13, "org_id": 2, "title": "玉泉区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "城建、征收、信访"},
    {"person_id": 14, "org_id": 2, "title": "玉泉区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "教育、卫健、医保、大数据"},
    {"person_id": 14, "org_id": 12, "title": "西菜园街道党工委副书记、办事处主任", "start_date": "", "end_date": "present", "rank": "乡科级", "note": "兼任街道职"},
    {"person_id": 15, "org_id": 2, "title": "玉泉区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "公安、司法"},
    {"person_id": 15, "org_id": 11, "title": "公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 16, "org_id": 3, "title": "玉泉区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "玉泉区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "玉泉区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "玉泉区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "玉泉区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 21, "org_id": 4, "title": "玉泉区政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼区委教育工委书记"},
    {"person_id": 22, "org_id": 4, "title": "玉泉区政协党组副书记、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "玉泉区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "玉泉区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 交流圈（兄弟区县）
    {"person_id": 25, "org_id": 13, "title": "新城区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 26, "org_id": 14, "title": "新城区人民政府区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 27, "org_id": 15, "title": "回民区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 28, "org_id": 16, "title": "回民区人民政府区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 29, "org_id": 17, "title": "赛罕区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 30, "org_id": 18, "title": "赛罕区人民政府区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

relationships = [
    # 区内核验关系（confirmed）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长组成区四套班子党政一把手搭档", "overlap_org": "中共呼和浩特市玉泉区委员会/玉泉区人民政府", "overlap_period": "现状"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记对副书记（政法委书记）直接领导", "overlap_org": "中共呼和浩特市玉泉区委员会", "overlap_period": "现状"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记对组织部长（管干部/编制/党校）", "overlap_org": "中共呼和浩特市玉泉区委员会", "overlap_period": "现状"},
    {"person_a": 1, "person_b": 6, "type": "监督", "context": "区委书记与纪委书记的日常监督与被监督关系", "overlap_org": "中共呼和浩特市玉泉区委员会/区纪委监委", "overlap_period": "现状"},
    {"person_a": 1, "person_b": 16, "type": "党政与人大", "context": "区委书记与人大常委会主任（党委领导人大机关）", "overlap_org": "玉泉区四套班子", "overlap_period": "现状"},
    {"person_a": 1, "person_b": 21, "type": "部长与政协", "context": "区政协主席同时兼区委教育工委书记，与区委书记为班子内领导", "overlap_org": "玉泉区四套班子", "overlap_period": "现状"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记对常务副区长（区政府二号人物）", "overlap_org": "中共呼和浩特市玉泉区委员会/区政府", "overlap_period": "现状"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长对常务副区长的直接领导", "overlap_org": "呼和浩特市玉泉区人民政府", "overlap_period": "现状"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与区委常委副区长（分管财政、审计协助）", "overlap_org": "呼和浩特市玉泉区人民政府", "overlap_period": "现状"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与90后副区长王海超（一镇九办、文旅）", "overlap_org": "呼和浩特市玉泉区人民政府", "overlap_period": "现状"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "区长与公安局长（维稳、司法）", "overlap_org": "玉泉区人民政府/公安分局", "overlap_period": "现状"},
    {"person_a": 7, "person_b": 21, "type": "同级党组", "context": "统战部长兼区政协党组副书记，与政协主席同党组共事", "overlap_org": "政协呼和浩特市玉泉区委员会党组", "overlap_period": "现状"},
    # --- 呼和浩特旗县干部交流圈（plausible，依据 S6 武川县报告第7节）
    {"person_a": 1, "person_b": 25, "type": "干部交流圈", "context": "同属呼和浩特旗县干部交流圈（玉泉↔新城），区县一把手平行交流序列", "overlap_org": "呼和浩特市旗县区县处级干部序列", "overlap_period": "2020s", "overlap_org_note": "S6"},
    {"person_a": 1, "person_b": 27, "type": "干部交流圈", "context": "同属呼和浩特旗县干部交流圈（玉泉↔回民）", "overlap_org": "呼和浩特市旗县区县处级干部序列", "overlap_period": "2020s"},
    {"person_a": 1, "person_b": 29, "type": "干部交流圈", "context": "同属呼和浩特旗县干部交流圈（玉泉↔赛罕）", "overlap_org": "呼和浩特市旗县区县处级干部序列", "overlap_period": "2020s"},
    {"person_a": 2, "person_b": 26, "type": "干部交流圈", "context": "玉泉区长与新城区长同处市辖区区县干部交流圈", "overlap_org": "呼和浩特市旗县区县处级干部序列", "overlap_period": "2020s"},
    {"person_a": 2, "person_b": 28, "type": "干部交流圈", "context": "玉泉区长与回民区长同处干部交流圈", "overlap_org": "呼和浩特市旗县区县处级干部序列", "overlap_period": "2020s"},
    {"person_a": 2, "person_b": 30, "type": "干部交流圈", "context": "玉泉区长与赛罕区长同处干部交流圈（杨朋飞曾任新城区副书记，交流圈典型流动）", "overlap_org": "呼和浩特市旗县区县处级干部序列", "overlap_period": "2020s"},
]


PINYIN = {"刘志强": "liu_zhiqiang", "杨晓君": "yang_xiaojun", "温艳": "wen_yan",
          "杨德杰": "yang_dejie", "吕明燕": "lv_mingyan", "张继峰": "zhang_jifeng",
          "敖登": "aodeng"}


def build_person_json(p: dict, job: str) -> dict:
    """Build the canonical person JSON record for a core leader."""
    career = [
        {
            "start": "unknown", "end": "unknown", "org": "履历缺口（公开渠道未获得任前履历）",
            "title": "", "level": "", "location": "", "system": "other", "rank": "",
            "is_key_promotion": False,
            "notes": "2026-08-11：外网搜索引擎不可用（Exa 限流/百度/搜狗/360 验证码），官方领导之窗仅公开现任职务；"
                     f"此前任各级职务待查。现任：{p['current_post']}（来源 S1-S4）。",
            "confidence": "unverified", "source_ids": [],
        }
    ]
    current = {
        "start": "present", "end": "present", "org": p["current_org"], "title": p["current_post"],
        "level": "", "location": "呼和浩特市玉泉区", "system": "government" if "人民政府" in p["current_org"] else "party",
        "rank": "正处级" if "书记" in p["current_post"] and "副" not in p["current_post"] else "副处级",
        "is_key_promotion": True, "notes": "现任职务（官方领导之窗）", "confidence": "confirmed",
        "source_ids": ["S1", "S2"] if "区长" in p["current_post"] else ["S1"],
    }
    career.append(current)
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区", "city": "呼和浩特市", "region": "玉泉区",
            "job": job, "task_id": "inner_mongolia_玉泉区", "time_focus": "current",
        },
        "identity": {
            "person_id": f"yuquan_{PINYIN.get(p['name'], p['name'])}",
            "name": p["name"], "aliases": [], "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""), "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""),
                           "study_type": "unknown", "source_ids": ["S1", "S2"]}],
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth','')}",
                            "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                            "official_profile_url": "http://www.yuquan.gov.cn/zwgk/ldzc/qw/"},
        },
        "current_status": {
            "current_post": p["current_post"], "current_org": p["current_org"],
            "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True,
            "source_ids": ["S1", "S2"],
        },
        "career_timeline": career,
        "organizations": [{"org_id": "yuquan_party", "name": "中共呼和浩特市玉泉区委员会", "role": "current_employer", "type": "party"}],
        "relationships": [
            {"person": "杨晓君", "person_id": "yuquan_yang_xiaojun", "relationship_type": "党政搭档",
             "strength": "strong", "evidence": "区四套班子中区委书记与区长组成核心搭档", "overlap_org": "玉泉区委/区政府",
             "overlap_period": "现状", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S1", "S2"]}
        ] if p["name"] == "刘志强" else [
            {"person": "刘志强", "person_id": "yuquan_liu_zhiqiang", "relationship_type": "党政搭档",
             "strength": "strong", "evidence": "区委书记与区长组成核心搭档", "overlap_org": "玉泉区委/区政府",
             "overlap_period": "现状", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S1", "S2"]}
        ],
        "governance_record": [{
            "period": "2026-08", "domain": "other", "achievement_or_event": "现任职务分工（依官方领导之窗）",
            "role_in_event": p["current_post"], "measurable_outcome": "", "location": "呼和浩特市玉泉区",
            "confidence": "confirmed", "source_ids": ["S1", "S2"],
        }],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": [],
            "geographic_pattern": ["呼和浩特市"], "promotion_velocity": {"summary": "公开信息有限，无法评估提速情况", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [], "management_signals": [],
            "caret": "无公开资料；待补充",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found", "description": "截至今日，未发现公开可查的处分、落马或被调查记录", "date": AS_OF,
            "confidence": "unverified", "source_ids": [],
        }],
        "source_register": [
            {"id": "S1", "title": "领导之窗·区委", "url": "http://www.yuquan.gov.cn/zwgk/ldzc/qw/",
             "publisher": "玉泉区人民政府门户网站", "published_at": "2026-08", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S2", "title": "领导之窗·政府", "url": "http://www.yuquan.gov.cn/zwgk/ldzc/zf/",
             "publisher": "玉泉区人民政府门户网站", "published_at": "2026-08", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "confirmed", "current_role": "confirmed",
            "career_completeness": "thin", "relationship_confidence": "high",
            "biggest_gap": f"{p['name']} 就任{job}前的完整履历（此前担任的职务/来源）",
        },
        "open_questions": [
            {"priority": "critical",
             "question": f"{p['name']} 就任玉泉区{job}前的完整履历（此前任职单位、晋升时间）",
             "why_it_matters": "核心领导跨区履历是判断呼和浩特旗县干部交流圈流动模式与圈子纽带的关键线索",
             "suggested_queries": [f"{p['name']} 呼和浩特 简历", f"{p['name']} 玉泉 {job} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": f"{p['name']} 出生地/籍贯、毕业院校与专业",
             "why_it_matters": "同校/同乡关系是人事网络的重要边",
             "suggested_queries": [f"{p['name']} 籍贯", f"{p['name']} 毕业"], "last_attempted": AS_OF},
            {"priority": "medium",
             "question": f"玉泉区前任{job}的继任链（前任是谁、去职去向）",
             "why_it_matters": "前任去向可揭示区县晋升梯",
             "suggested_queries": [f"玉泉区 前任 {job}", "玉泉区 区委书记 上任"], "last_attempted": AS_OF},
        ],
    }


JOBS = {1: "区委书记", 2: "区长", 3: "区委副书记", 5: "常务副区长",
        6: "纪委书记", 16: "人大常委会主任", 21: "政协主席"}


def write_person_json(p: dict) -> Path | None:
    """Write one canonical person JSON into the staging dir."""
    job = JOBS.get(p["id"])
    if job is None:
        return None
    obj = build_person_json(p, job)
    fname = f"{TODAY}-内蒙古自治区-呼和浩特市-{job}-{p['name']}.json"
    path = JSON_DIR / fname
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
    print(f"  person json -> {path.name}")
    return path


def main() -> None:
    STAGING.mkdir(parents=True, exist_ok=True)
    print(f"[build:{SLUG}] staging = {STAGING}")
    print(f"[build:{SLUG}] writing person JSON profiles ...")
    for person in persons:
        write_person_json(person)
    print(f"[build:{SLUG}] run_build backend=legacy (sqlite3 + gexf)")
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
    print(f"[build:{SLUG}] done. DB = {DB_PATH}")
    print(f"[build:{SLUG}] done. GEXF = {GEXF_PATH}")


if __name__ == "__main__":
    main()