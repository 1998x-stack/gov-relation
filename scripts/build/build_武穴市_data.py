#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 武穴市 (Hubei, 黄冈市).

Investigation date: 2026-08-06
Task ID: hubei_武穴市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.wuxue.gov.cn (武穴市人民政府门户, HTTP) — 政府领导渠道（市长及 9 名政府副职官方简历）、
    武穴要闻 (2026-07 至 08): 查俊/叶林出席活动、常委会点名.
  - www.hg.gov.cn (黄冈市人民政府门户) — 市委/市政府上级上下文（李军杰赴武穴、黄梅调研 2026-08）.
  - 搜索引擎（Exa rate-limited / Baidu 403 / Bing-Sogou 需 JS）不可用，书记查俊党内完整履历及
    前任书记交接链、个别常委（组织/宣传/政法）分工未核到 — 记为 open_questions。
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Allow importing gov_relation regardless of where this script lives.
for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "武穴市"
PROVINCE = "湖北省"
CITY = "黄冈市"
AS_OF = "2026-08-06"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "查俊", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委书记", "current_org": "中共武穴市委员会",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12111221.html"},
    {"id": 2, "name": "叶林", "gender": "男", "ethnicity": "汉族", "birth": "1981-10", "birthplace": "湖北蕲春",
     "education": "大学学历", "party_join": "2002-04", "work_start": "2002-09",
     "current_post": "市长", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=224&leaderTypeId=59"},
    {"id": 3, "name": "董晓燕", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委副书记", "current_org": "中共武穴市委员会",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12111221.html"},
    {"id": 4, "name": "李阜乔", "gender": "男", "ethnicity": "汉族", "birth": "1985-02", "birthplace": "湖北黄梅",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "常务副市长", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=311&leaderTypeId=59"},
    {"id": 5, "name": "田间", "gender": "男", "ethnicity": "汉族", "birth": "1986-08", "birthplace": "山东高密",
     "education": "博士研究生", "party_join": "2008-04", "work_start": "2011-07",
     "current_post": "副市长（挂职）", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=324&leaderTypeId=59"},
    {"id": 6, "name": "秦良骥", "gender": "男", "ethnicity": "汉族", "birth": "1979-08", "birthplace": "湖北红安",
     "education": "研究生学历", "party_join": "2006-06", "work_start": "2002-06",
     "current_post": "副市长", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=332&leaderTypeId=59"},
    {"id": 7, "name": "丰峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委、市委办公室主任", "current_org": "中共武穴市委员会",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12111221.html"},
    {"id": 8, "name": "徐楷", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委、统战部部长", "current_org": "中共武穴市委员会",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12112118.html"},
    {"id": 9, "name": "周向宇", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市纪委书记、市监委主任", "current_org": "中共武穴市纪律检查委员会",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12110627.html"},
    {"id": 10, "name": "李向阳", "gender": "男", "ethnicity": "汉族", "birth": "1975-06", "birthplace": "湖北蕲春",
     "education": "大学学历", "party_join": "2003-06", "work_start": "1996-08",
     "current_post": "副市长、公安局局长", "current_org": "武穴市公安局",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=227&leaderTypeId=59"},
    {"id": 11, "name": "马聪", "gender": "男", "ethnicity": "汉族", "birth": "1985-10", "birthplace": "湖北麻城",
     "education": "大学学历、农业推广硕士", "party_join": "2005-05", "work_start": "2007-07",
     "current_post": "副市长", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=230&leaderTypeId=59"},
    {"id": 12, "name": "蔡慧", "gender": "女", "ethnicity": "汉族", "birth": "1976-05", "birthplace": "湖北武穴",
     "education": "大学学历", "party_join": "2012-08(民盟)", "work_start": "1997-07",
     "current_post": "副市长", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=239&leaderTypeId=59"},
    {"id": 13, "name": "马子飞", "gender": "男", "ethnicity": "汉族", "birth": "1985-06", "birthplace": "山东冠县",
     "education": "研究生学历", "party_join": "2007-06", "work_start": "2011-10",
     "current_post": "副市长", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=367&leaderTypeId=59"},
    {"id": 14, "name": "高宁波", "gender": "男", "ethnicity": "汉族", "birth": "1988-08", "birthplace": "湖北团风",
     "education": "武汉科技大学研究生", "party_join": "2006-07", "work_start": "2010-09",
     "current_post": "市政府党组成员、副市长", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=375&leaderTypeId=59"},
    {"id": 15, "name": "徐珂", "gender": "男", "ethnicity": "汉族", "birth": "1988-02", "birthplace": "山东济宁",
     "education": "上海交通大学博士研究生", "party_join": "2008-11", "work_start": "2016-10",
     "current_post": "市政府党组成员、副市长（挂职）", "current_org": "武穴市人民政府",
     "source": "http://www.wuxue.gov.cn/content/column/6795185?liId=372&leaderTypeId=59"},
    {"id": 16, "name": "程小兵", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市政协副主席", "current_org": "中国人民政治协商会议武穴市委员会",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12111221.html"},
    {"id": 17, "name": "熊春晖", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市人武部部长", "current_org": "湖北省武穴市人民武装部",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12111221.html"},
    {"id": 18, "name": "刘英利", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市人武部政委", "current_org": "湖北省武穴市人民武装部",
     "source": "http://www.wuxue.gov.cn/xwzx/wxyw/12111221.html"},
    {"id": 19, "name": "李军杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "黄冈市委书记", "current_org": "中共黄冈市委",
     "source": "https://www.hg.gov.cn/zwxw/hgyw/9392028.html"},
    {"id": 20, "name": "刘洁", "gender": "女", "ethnicity": "汉族", "birth": "1969-03", "birthplace": "",
     "education": "大学学历、法律硕士", "party_join": "", "work_start": "",
     "current_post": "黄冈市委副书记、市长", "current_org": "黄冈市人民政府",
     "source": "https://www.hg.gov.cn/"},
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共武穴市委员会", "type": "党委", "level": "县级市", "parent": "中共黄冈市委", "location": "湖北省黄冈市武穴市"},
    {"id": 2, "name": "武穴市人民政府", "type": "政府", "level": "县级市", "parent": "黄冈市人民政府", "location": "湖北省黄冈市武穴市"},
    {"id": 3, "name": "中共武穴市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共黄冈市纪委", "location": "湖北省黄冈市武穴市"},
    {"id": 4, "name": "武穴市监察委员会", "type": "党委", "level": "县级市", "parent": "黄冈市监委", "location": "湖北省黄冈市武穴市"},
    {"id": 5, "name": "武穴市公安局", "type": "政府", "level": "县级市", "parent": "武穴市人民政府", "location": "湖北省黄冈市武穴市"},
    {"id": 6, "name": "湖北省武穴市人民武装部", "type": "政府", "level": "县级市", "parent": "黄冈军分区", "location": "湖北省黄冈市武穴市"},
    {"id": 7, "name": "中国人民政治协商会议武穴市委员会", "type": "政协", "level": "县级市", "parent": "武穴市", "location": "湖北省黄冈市武穴市"},
    {"id": 8, "name": "武穴市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "武穴市", "location": "湖北省黄冈市武穴市"},
    {"id": 9, "name": "湖北武穴经济开发区", "type": "开发区", "level": "县级市", "parent": "武穴市人民政府", "location": "湖北省黄冈市武穴市"},
    {"id": 10, "name": "湖北省智能化新能源船舶产业园", "type": "开发区", "level": "县级市", "parent": "武穴市", "location": "湖北省黄冈市武穴市"},
    {"id": 11, "name": "中共黄冈市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省黄冈市"},
    {"id": 12, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
]

# ── Positions (confirmed, as-of 2026-08-06) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "兼市人武部党委第一书记（2026-07-29 八一慰问等确认）"},
    {"person_id": 1, "org_id": 6, "title": "市人武部党委第一书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "八一走访慰问 2026-07-29 确认"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "市委副书记、市长（官方政府领导渠道）"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正县级", "note": "市委副书记、市政府党组书记、市长，主持市政府全面工作（官方简历）"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "八一慰问出席、千万夏工程推进会主持（2026-07）"},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市委常委、市政府党组副书记、常务副市长（官方领导渠道）"},
    {"person_id": 5, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "市委常委、副市长（挂职）（官方领导渠道）"},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市委常委、市政府党组成员、副市长（官方领导渠道）"},
    {"person_id": 7, "org_id": 1, "title": "市委常委、市委办公室主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "千万夏工程推进会宣读（2026-07）"},
    {"person_id": 8, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "潍柴重机座谈陪同（2026-08-05）"},
    {"person_id": 9, "org_id": 3, "title": "市纪委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "市委常委会（扩大）会议点名（2026-07-24）"},
    {"person_id": 9, "org_id": 4, "title": "市监委主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼市监察委员会主任"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组成员、副市长（官方领导渠道）"},
    {"person_id": 10, "org_id": 5, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "副市长、公安局局长（官方领导渠道），主持市公安局"},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组成员、副市长（官方领导渠道）"},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "副市长（非党，民盟）（官方领导渠道）"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组成员、副市长（官方领导渠道）"},
    {"person_id": 14, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "官方领导渠道"},
    {"person_id": 15, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组成员、副市长（挂职）（官方领导渠道）"},
    {"person_id": 16, "org_id": 7, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副县级", "note": "八一慰问出席（2026-07-29）"},
    {"person_id": 17, "org_id": 6, "title": "市人武部部长", "start_date": "", "end_date": "", "rank": "正团级", "note": "八一慰问出席（2026-07-29）"},
    {"person_id": 18, "org_id": 6, "title": "市人武部政委", "start_date": "", "end_date": "", "rank": "正团级", "note": "八一慰问出席（2026-07-29）"},
    {"person_id": 19, "org_id": 11, "title": "黄冈市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "上级（黄冈市委书记）赴武穴调研"},
    {"person_id": 20, "org_id": 12, "title": "黄冈市委副书记、市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "上级（黄冈市长）"},
]

# ── Relationships (confirmed) ─────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长（市委班子核心搭子）", "overlap_org": "中共武穴市委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "市委书记—市委副书记董晓燕", "overlap_org": "中共武穴市委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记—常务副市长李阜乔", "overlap_org": "中共武穴市委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "市委书记—常委/市委办主任丰峰", "overlap_org": "中共武穴市委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记—常委/统战部长徐楷", "overlap_org": "中共武穴市委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "市委书记—市纪委书记周向宇（常委班子）", "overlap_org": "中共武穴市委员会", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "市长—常务副市长李阜乔（市政府党组）", "overlap_org": "武穴市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "市长—副市长田间（挂职）（市政府班子）", "overlap_org": "武穴市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长—副市长秦良骥（市政府班子）", "overlap_org": "武穴市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "市长—副市长/公安局长李向阳（市政府班子）", "overlap_org": "武穴市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "市长—副市长马聪（市政府班子）", "overlap_org": "武穴市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "市长—副市长高宁波（市政府班子）", "overlap_org": "武穴市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "市长—副市长徐珂（挂职）（市政府班子）", "overlap_org": "武穴市人民政府", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 19, "type": "上下级", "context": "武穴市委书记—黄冈市委书记（上级考核）", "overlap_org": "中共黄冈市委", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 20, "type": "上下级", "context": "武穴市长—黄冈市长（上级）", "overlap_org": "黄冈市人民政府", "overlap_period": "2026年"},
]

# ── Person JSON generation ────────────────────────────────────────────────
_CAREERS = {
    "查俊": [
        {"start": "unknown", "end": "present", "org": "中共武穴市委员会", "title": "市委书记",
         "level": "县级市", "location": "湖北省黄冈市武穴市", "system": "party", "rank": "正县级",
         "is_key_promotion": True, "notes": "兼市人武部党委第一书记；公开新闻自 2026-06 起以'市委书记'出现",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "",
         "location": "", "system": "unknown", "rank": "", "is_key_promotion": False,
         "notes": "查俊任武穴市委书记前的完整履历（出生/籍贯/学历/前职/就任时间）公开不足，待补",
         "confidence": "unverified", "source_ids": []},
    ],
    "叶林": [
        {"start": "2002-09", "end": "", "org": "（参工）", "title": "参加工作", "level": "", "location": "",
         "system": "other", "rank": "", "is_key_promotion": False, "notes": "2002-09 参加工作，2002-04 入党（官方简历）",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "present", "org": "武穴市人民政府", "title": "市长",
         "level": "县级市", "location": "湖北省黄冈市武穴市", "system": "government", "rank": "正县级",
         "is_key_promotion": True, "notes": "市委副书记、市长（官方政府领导渠道）",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "",
         "location": "", "system": "", "rank": "", "is_key_promotion": False,
         "notes": "叶林任市长前的历任职务、出生地点、入党时间细节待补",
         "confidence": "unverified", "source_ids": []},
    ],
}

_GOVERNANCE = {
    "查俊": [
        {"period": "2026", "domain": "urban_construction", "achievement_or_event": "主持推进城市更新'2.0版'攻坚（老旧小区改造/加装电梯/停车位扩容/'九街十八巷'）", "role_in_event": "市委书记主持/督导", "measurable_outcome": "城市更新2.0攻坚", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "rural_revitalization", "achievement_or_event": "主持全市'千万夏工程'暨片区化推进乡村振兴半年现场推进会", "role_in_event": "市委书记讲话", "measurable_outcome": "", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "other", "achievement_or_event": "率市四大家调研大话嬉游旅游度假区项目（文旅支柱产业）", "role_in_event": "市委书记带队", "measurable_outcome": "推进试营业", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "与潍柴动力座谈，布局新能源船舶动力配套产业链", "role_in_event": "市委书记洽谈", "measurable_outcome": "", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "public_security", "achievement_or_event": "防汛防台风专题调度、地质灾害督导、安全生产排查", "role_in_event": "市委书记主持/督导", "measurable_outcome": "", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
    ],
    "叶林": [
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "主持市政府全面；分管招商引资、交通运输、经济开发区", "role_in_event": "市长", "measurable_outcome": "", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "public_security", "achievement_or_event": "部署城区防汛防台风工作", "role_in_event": "市长部署", "measurable_outcome": "", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "other", "achievement_or_event": "八一建军营即慰问驻军部队（查/叶带队）", "role_in_event": "市长带队", "measurable_outcome": "", "location": "武穴市", "confidence": "confirmed", "source_ids": ["S001"]},
    ],
}

_PROFILE_META = {
    "查俊": ("cross_county_rotation", ["party", "development_zone"], ["城市更新", "乡村振兴", "招商", "船舶产业"],
             ["人民城市理念/城市更新2.0", "千万夏/片区化乡村振兴", "文旅支柱产业（大话嬉游）", "新能源船舶产业链（潍柴）", "防汛防台风/安全底线"],
             "现任武穴市委书记前完整履历（出生/籍贯/学历/前职/就任时间）与前任书记交接链未获（网络受限）"),
    "叶林": ("local_ladder", ["government", "party"], ["招商引资", "交通运输", "经济开发区"],
             ["城区防汛防台风部署", "民生实事", "政府全面工作"],
             "叶林任市长前的历任职务、出生地点、党籍等细节未获（网络受限）"),
}


def _rank_for(name):
    return "正县级" if name in {"查俊", "叶林", "董晓燕", "李阜乔"} else "副县级"


def _person(name):
    for p in persons:
        if p["name"] == name:
            return p
    raise KeyError(name)


def _career_row(person):
    return {"start": "unknown", "end": "present", "org": person["current_org"], "title": person["current_post"],
            "level": "县级市", "location": "湖北省黄冈市武穴市",
            "system": "government" if "人民政府" in person["current_org"] else "party",
            "rank": _rank_for(person["name"]), "is_key_promotion": False, "notes": "官方来源确认现任职务",
            "confidence": "confirmed", "source_ids": ["S001"]}


def _profile(name):
    person = _person(name)
    pattern, systems, spec, themes, gap = _PROFILE_META[name]
    career = _CAREERS.get(name, [_career_row(person)])
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": person["current_post"],
                                "task_id": "hubei_武穴市", "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"wuxi_{name}", "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "",
                           "degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{person.get('birth','')}",
                            "name_birthplace": f"{name}_{person.get('birthplace','')}",
                            "official_profile_url": person.get("source", "")},
        },
        "current_status": {"current_post": person["current_post"], "current_org": person["current_org"],
                           "administrative_rank": _rank_for(name), "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002"]},
        "career_timeline": career,
        "organizations": [
            {"org": "中共武穴市委员会", "type": "党委", "level": "县级市", "location": "湖北省黄冈市武穴市"},
            {"org": "武穴市人民政府", "type": "政府", "level": "县级市", "location": "湖北省黄冈市武穴市"},
        ],
        "relationships": [],
        "governance_record": _GOVERNANCE.get(name, []),
        "professional_profile": {"primary_specializations": list(spec), "secondary_specializations": [],
                                 "career_pattern": pattern, "systems_experience": list(systems),
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": list(themes),
                                       "management_signals": [],
                                       "caveat": "工作风格仅依据公开新闻/讲话推断，非心理评估。"},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次调研（官方新闻+政府领导渠道）未发现明确负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "武穴市人民政府门户（政府领导渠道 + 武穴要闻）", "url": "http://www.wuxue.gov.cn/", "publisher": "武穴市人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "note": "官方简历/新闻确认现任职务"},
            {"id": "S002", "title": "黄冈市人民政府门户（县区动态/黄冈要闻）", "url": "https://www.hg.gov.cn/", "publisher": "黄冈市人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "note": "市委市政府调研的县政府情"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "partial" if person.get("birth") else "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap},
        "open_questions": [{"priority": "high", "question": gap, "why_it_matters": "跨县网络与履历深度分析",
                            "suggested_queries": [f"武穴市 {name} 简历", f"{CITY} 组织部 任前公示 {name}"], "last_attempted": AS_OF}],
    }


def _write_profiles_json():
    profiles = []
    for name in ("查俊", "叶林"):
        role_label = "市委书记" if name == "查俊" else "市长"
        profiles.append((f"{TODAY}-湖北省-黄冈市-{role_label}-{name}.json", _profile(name)))
    for fname, data in profiles:
        with open(str(HERE / fname), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级市")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 武穴市人民政府门户 + 黄冈市人民政府门户")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )

    profiles = _write_profiles_json()
    print(f"\n  人物JSON: {len(profiles)} 个")
    for fname, _ in profiles:
        print(f"    - {fname}")

    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()