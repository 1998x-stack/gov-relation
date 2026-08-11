#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 沅江市 (Yuanjiang City), 益阳市, 湖南省.

Task ID: hunan_沅江市
Level: 县级市
Targets: 市委书记 & 市长
Investigation date: 2026-08-11

Key findings (verified 2026-08-11):
- 现任市委书记: 罗必胜 (2025-12-22 由市长升任, 2026-07 十四届市委换届连任)
- 现任市长: 廖江华 (代理市长, 2026-02-05 市人大常委会第三十次会议任命; 兼任市委副书记)
- 前任市委书记: 杨智勇 (2021-07-03 至 2025-11 调离沅江)
- 前任市长链条: 周振宇→邓宗祥→肖胜利(落马)→谢君毅→杨智勇→罗必胜→廖江华(代理)
- 前任人大常委会主任 孟智勇 2025-06-18 被纪律审查和监察调查; 高应良当选新任主任
- 省委第十五巡视组 2025-03 进驻沅江, 2025-06-20 反馈

Evidence: 沅江市人民政府门户网站 (yuanjiang.gov.cn 市委领导/市政府/人大/政协页), 红网 (yiyang.rednet.cn), 维基百科沅江市条目 (2025-12-30 修订), 百度百科/360百科, 湖南日报/新湖南, 益阳市委组织部任前公示.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "沅江市"
TODAY = datetime.now().strftime("%Y%m%d")  # 20260811
AS_OF = "2026-08-11"

# ── Staging paths (province-aware promotion is done by scripts/process_tmp.py) ─
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_沅江市"
if _CURRENT_DIR.name == "hunan_沅江市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
JSON_DIR = STAGING

# ══════════════════════════════════════════════════════════════════════════
# SOURCES
# ══════════════════════════════════════════════════════════════════════════
SOURCES = [
    {"id": "S001", "title": "红网益阳站: 罗必胜同志任中共沅江市委书记 (2025-12-22)", "url": "https://yiyang.rednet.cn/content/646956/66/15560393.html", "publisher": "红网(益阳市委组织部、沅江发布)", "published_at": "2025-12-22", "source_type": "media", "reliability": "high"},
    {"id": "S002", "title": "沅江市人民政府门户网站: 市委领导页", "url": "http://www.yuanjiang.gov.cn/21203/21211/index.htm", "publisher": "沅江市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S003", "title": "沅江市人民政府门户网站: 罗必胜个人简历", "url": "http://www.yuanjiang.gov.cn/21203/21211/content_847810.html", "publisher": "沅江市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S004", "title": "维基百科: 沅江市 (含现任Yes领导表, 2025-12-30修订)", "url": "https://zh.wikipedia.org/wiki/沅江市", "publisher": "维基百科", "published_at": "2025-12-30", "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S005", "title": "维基百科: 杨智勇", "url": "https://zh.wikipedia.org/wiki/%E6%9D%A8%E6%99%BA%E5%8B%87", "publisher": "维基百科", "published_at": "2022-11-01", "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S006", "title": "百度百科: 杨智勇(沅江市委原书记)", "url": "https://baike.baidu.com/item/%E6%9D%A8%E6%99%BA%E5%8B%87/13015164", "publisher": "百度百科", "published_at": "", "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S007", "title": "百度百科: 罗必胜(沅江市委书记)", "url": "https://baike.baidu.com/item/%E7%BD%97%E5%BF%85%E8%83%9C", "publisher": "百度百科", "published_at": "", "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S008", "title": "沅江市政府: 2025-11-05市人大常委会主任候选人提名人选履新见面会(高应良)", "url": "http://www.yuanjiang.gov.cn/20809/content_2108088.html", "publisher": "沅江市人民政府", "published_at": "2025-11-05", "source_type": "official", "reliability": "high"},
    {"id": "S009", "title": "沅江市人民政府门户网站: 市人大常委会领导·高应良简历", "url": "http://www.yuanjiang.gov.cn/21203/21212/content_2138048.html", "publisher": "沅江市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S010", "title": "新湖南: 高应良当选沅江市十八届人大常委会主任", "url": "https://m-xhncloud.voc.com.cn/portal/news/show?id=15373435", "publisher": "新湖南(湖南日报社)", "published_at": "2026-02", "source_type": "media", "reliability": "high"},
    {"id": "S011", "title": "360百科: 高应良", "url": "https://baike.so.com/doc/24158131-24743653.html", "publisher": "360百科", "published_at": "", "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S012", "title": "沅江市人民政府: 市政府领导·廖江华简历", "url": "http://www.yuanjiang.gov.cn/21203/21211/content_2148763.html", "publisher": "沅江市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S013", "title": "桃源新闻网/红网: 廖江华任沅江市委副书记(2026)", "url": "https://yiyang.rednet.cn/", "publisher": "红网益阳", "published_at": "2026-01-23", "source_type": "media", "reliability": "high"},
    {"id": "S014", "title": "省委第十五巡视组巡视沅江市工作动员会召开 (2025-03-04)", "url": "http://www.yuanjiang.gov.cn/21138/21227/content_2043728.html", "publisher": "沅江市人民政府", "published_at": "2025-03-04", "source_type": "official", "reliability": "high"},
    {"id": "S015", "title": "省委第十五巡视组向沅江市委反馈巡视情况 (2025-06-20)", "url": "http://www.yuanjiang.gov.cn/21138/21227/content_2079422.html", "publisher": "沅江市人民政府", "published_at": "2025-06-20", "source_type": "official", "reliability": "high"},
    {"id": "S016", "title": "三湘风纪/湖南日报: 益阳市沅江市人大常委会原主任孟智勇接受审查调查 (2025-06-18)", "url": "http://www.sxfj.gov.cn/", "publisher": "湖南省纪委监委", "published_at": "2025-06-18", "source_type": "official", "reliability": "high"},
    {"id": "S017", "title": "红网: 肖胜利被查 (2015-08-05)", "url": "http://hn.rednet.cn/c/2015/08/05/3758359.htm", "publisher": "红网", "published_at": "2015-08-05", "source_type": "media", "reliability": "high"},
    {"id": "S018", "title": "澎湃新闻: 沅江原市长肖胜利一审获刑5年 (2017-12)", "url": "https://www.thepaper.cn/newsDetail_forward_1926250", "publisher": "澎湃新闻", "published_at": "2017-12-28", "source_type": "media", "reliability": "high"},
    {"id": "S019", "title": "红网: 邓宗祥被查/双开 (2018-08/11)", "url": "http://www.hncdc.gov.cn/", "publisher": "红网/湖南省纪委监委", "published_at": "2018-11", "source_type": "media", "reliability": "high"},
    {"id": "S020", "title": "红网新湖南: 黄育文任沅江市委书记 (2019-04)", "url": "https://m.voc.com.cn/xhn/news/201904/16930514.html", "publisher": "新湖南", "published_at": "2019-04", "source_type": "media", "reliability": "high"},
    {"id": "S021", "title": "益阳人大: 高应良履新见面会 / 2025-12-17 黄育文辞去益阳市人大常委会副主任 (人大代表网)", "url": "http://www.yyrd.gov.cn/", "publisher": "益阳市人大常委会", "published_at": "2025-12-17", "source_type": "official", "reliability": "high"},
    {"id": "S022", "title": "新浪新闻: 周振宇任常德代市长 (2021-11-19)", "url": "https://finance.sina.com.cn/jjxw/2021-11-19/doc-iktzscyy6477923.shtml", "publisher": "新浪新闻/红网", "published_at": "2021-11-19", "source_type": "media", "reliability": "high"},
    {"id": "S023", "title": "维基百科: 周振宇", "url": "https://zh.wikipedia.org/wiki/周振宇", "publisher": "维基百科", "published_at": "", "source_type": "encyclopedia", "reliability": "medium"},
    {"id": "S024", "title": "湖南日报: 湖南省委组织部干部任前公示(谢君毅拟任省直单位正厅级) (2025-12-13)", "url": "https://epaper.hnrb.hnrbnews.com/", "publisher": "湖南日报", "published_at": "2025-12-13", "source_type": "appointment_notice", "reliability": "high"},
    {"id": "S025", "title": "澎湃新闻: 娄底市(谢君毅任市委秘书长后转任市州领导公示)", "url": "https://www.thepaper.cn/", "publisher": "澎湃新闻", "published_at": "2025-12-12", "source_type": "media", "reliability": "high"},
    {"id": "S026", "title": "沅江市政府网站: 市政府领导分工页(张心镜/宋铁成/郭强等名单)", "url": "http://www.yuanjiang.gov.cn/21203/21214/index.htm", "publisher": "沅江市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S027", "title": "沅江市政府网站: 市政协领导页(刘武/徐鄂春等)", "url": "http://www.yuanjiang.gov.cn/21203/21213/index.htm", "publisher": "沅江市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S028", "title": "沅江市政府网站: 市人大领导页", "url": "http://www.yuanjiang.gov.cn/21203/21212/index.htm", "publisher": "沅江市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S029", "title": "红网: 谢君毅任娄底市副市长 (2020-09)", "url": "https://hunan.voc.com.cn/", "publisher": "红网", "published_at": "2020-09", "source_type": "media", "reliability": "high"},
    {"id": "S030", "title": "益阳人大网: 陶德保任免消息 (2019-2021)", "url": "http://www.yyrd.gov.cn/", "publisher": "益阳市人大常委会", "published_at": "2021-06-29", "source_type": "official", "reliability": "high"},
]

# ══════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════
persons = [
    # ── 1. 现任市委书记 ──
    {
        "id": 1, "name": "罗必胜", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-04", "birthplace": "湖南省益阳市安化县",
        "education": "大学本科", "party_join": "1995-04", "work_start": "1991-08",
        "current_post": "中共沅江市委书记", "current_org": "中共沅江市委员会",
        "source": "S003 S001 S007",
        "profile_notes": "1991年起在安化县基层工作，历任安化县政府副县长、县委常委/政法委书记；2016年8月交流至沅江市任市委常委、常务副市长，2020年4月任市委副书记，2021年10月当选市长，2025年12月升任市委书记，2026年7月中共沅江市第十四次代表大会后连任。2021年4月荣获'湖南省脱贫攻坚先进个人'。",
        "governance": [
            {"period": "2016-2020", "domain": "urban_construction", "achievement_or_event": "任沅江市委常委、常务副市长，分管经济与城市建设", "role_in_event": "常务副市长", "measurable_outcome": "", "location": "沅江市", "confidence": "plausible", "source_ids": ["S007"]},
            {"period": "2021-2025", "domain": "poverty_alleviation", "achievement_or_event": "任沅江市市长，2021年4月30日获湖南省委授予'湖南省脱贫攻坚先进个人'", "role_in_event": "市长", "measurable_outcome": "脱贫先进个人称号", "location": "沅江市", "confidence": "confirmed", "source_ids": ["S007"]},
        ],
        "work_style": [
            {"trait": "grassroots_oriented", "evidence": "1991年至2016年在安化县乡镇、县直系统工作25年，基层履历完整", "confidence": "confirmed", "source_ids": ["S007"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "local_ladder|cross_county_rotation", "systems": ["government", "party", "legal"], "geo": ["湖南省", "益阳市", "安化县", "沅江市"]},
    },
    # ── 2. 现任市长 (代理) ──
    {
        "id": 2, "name": "廖江华", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-01", "birthplace": "",
        "education": "硕士研究生(法律/法学)", "party_join": "中共党员", "work_start": "",
        "current_post": "沅江市人民政府市长(代理)", "current_org": "沅江市人民政府",
        "source": "S012, S013",
        "profile_notes": "1983年生，硕士研究生，早期在邵阳市中级人民法院工作，后调入省人大(法制委/环资委/办公厅)，2022年10月任常德市石门县委常委、常务副县长，2024年8月任石门县委副书记、统战部长，2026年1月交流任沅江市委副书记(提名为市长候选人)，2026年2月5日市人大常委会决定其为副市长、代理市长。跨市交流(常德→益阳)干部。",
        "career": [
            {"start": "unknown", "end": "unknown", "org": "邵阳市中级人民法院", "title": "早期工作", "level": "乡科级", "system": "other", "rank": "", "is_key_promotion": False, "notes": "早年曾在邵阳市中级人民法院工作", "confidence": "plausible", "source_ids": ["S013"]},
            {"start": "unknown", "end": "2022-10", "org": "湖南省人大常委会机关", "title": "省人大部门工作(法制委/环资委/办公厅)", "level": "厅局级", "system": "other", "rank": "正处级?", "is_key_promotion": False, "notes": "曾在湖南省人大有关专门委员会和办公厅工作", "confidence": "plausible", "source_ids": ["S013"]},
            {"start": "2022-10", "end": "2024-08", "org": "中共石门县委员会", "title": "县委常委、常务副县长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "常德市石门县委常委、常务副县长", "confidence": "confirmed", "source_ids": ["S013", "S012"]},
            {"start": "2024-08", "end": "2026-01", "org": "中共石门县委员会", "title": "县委副书记、统战部部长", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "石门县委副书记、统战部部长", "confidence": "confirmed", "source_ids": ["S013"]},
            {"start": "2026-01-23", "end": "2026-02", "org": "中共沅江市委员会", "title": "市委副书记", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "2026年1月23日任沅江市委副书记，提名为市长候选人", "confidence": "confirmed", "source_ids": ["S013"]},
            {"start": "2026-02-05", "end": "", "org": "沅江市人民政府", "title": "市长(代理)", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2026年2月5日沅江市第十八届人大常委会第三十次会议决定罗必胜辞去市长职务，任命廖江华为副市长、代理市长；现为代理市长", "confidence": "confirmed", "source_ids": ["S012"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "cross_county_rotation|civil_service_directorate", "systems": ["other", "party", "government"], "geo": ["邵阳", "常德", "石门", "益阳", "沅江"]},
    },
    # ── 3. 前任市委书记 ──
    {
        "id": 3, "name": "杨智勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-11", "birthplace": "湖南省宁乡市",
        "education": "历史学博士(湖南师范大学)", "party_join": "1995-12", "work_start": "1997-07",
        "current_post": "前沅江市委书记(已调任)", "current_org": "中共沅江市委员会(前)",
        "source": "S005, S006",
        "profile_notes": "1997年湖南师范大学历史系毕业后留校工作近20年(历史学硕士、博士)，2016年8月转入地方：资阳区委副书记→2017年5月沅江市委副书记→2017年8月代理市长→2017年12月市长→2021年7月升任市委书记。2025年受省委巡视组巡视(2025年3月进驻、6月反馈)，2025年11月调离沅江市(调离本行政区域)，新去向尚未公开。历任市长任内2018年沅江涉黑涉恶案件(何建国等)于其市长任内获查办。",
        "career": [
            {"start": "1993-09", "end": "1997-07", "org": "湖南师范大学", "title": "历史系学习", "level": "", "system": "other", "rank": "", "is_key_promote": False, "note": "湖南师范大学历史系本科", "confidence": "confirmed", "source_ids": ["S006"]},
            {"start": "1997-07", "end": "2016-08", "org": "湖南师范大学", "title": "留校工作(历任学院党委副书记等)", "level": "乡科级", "system": "education", "rank": "", "is_key_promote": False, "note": "1997年留校，获历史学硕士、博士学位，2012年4月起任历史文化学院党委书记等职", "confidence": "confirmed", "source_ids": ["S006"]},
            {"start": "2016-08", "end": "2017-05", "org": "中共益阳市资阳区委员会", "title": "区委副书记", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promote": True, "note": "2016年8月由湖南师大转入地方，任益阳市资阳区委副书记", "confidence": "confirmed", "source_ids": ["S006"]},
            {"start": "2017-05", "end": "2017-08", "org": "中共沅江市委员会", "title": "市委副书记", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promote": True, "note": "", "confidence": "confirmed", "source_ids": ["S006"]},
            {"start": "2017-08", "end": "2017-12", "org": "沅江市人民政府", "title": "代理市长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promote": True, "note": "", "confidence": "confirmed", "source_ids": ["S006"]},
            {"start": "2017-12", "end": "2021-07", "org": "沅江市人民政府", "title": "市长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promote": True, "note": "2017年12月市第十七届人大会议当选沅江市市长；2020年获评'湖南省脱贫攻坚先进个人'", "confidence": "confirmed", "source_ids": ["S006"]},
            {"start": "2021-07-03", "end": "2025-11", "org": "中共沅江市委员会", "title": "市委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promote": True, "note": "2021年7月3日沅江市召开领导干部大会宣布杨智勇任市委书记；2025年3-6月省委第十五巡视组巡视沅江；2025年11月调离本行政区域", "confidence": "confirmed", "source_ids": ["S001", "S014", "S015"]},
            {"start": "2025-11", "end": "", "org": "（调离后任所待核实）", "title": "新职务(公开未披露)", "level": "", "system": "other", "rank": "", "is_key_promote": False, "note": "2025年11月调离沅江市行政区域，具体新职务尚未见公开报道", "confidence": "unverified", "source_ids": []},
        ],
        "governance": [
            {"period": "2018", "domain": "public_security", "achievement_or_event": "任市长期间配合查处以何金勇为首的涉黑涉恶组织(沅江'7·12'案件), 该案入选全国扫黑除恶十大典型案例", "role_in_event": "市长", "measurable_outcome": "案件全国通报", "location": "沅江市", "confidence": "plausible", "source_ids": []},
        ],
        "workflow": [
            {"trait": "technocratic", "evidence": "湖南师大历史学博士，高校工作近20年后转入地方", "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        "risk": [
            {"type": "inspection_feedback", "description": "省委第十五巡视组2025年3月4日进驻沅江巡视，6月20日反馈问题，杨智勇主持反馈会议并作表态发言；2025年11月调离", "date": "2025-03~11", "confidence": "confirmed", "source_ids": ["S014", "S015"]},
        ],
        "extras": {"career_pattern": "academic_to_official", "systems": ["education", "party", "government"], "geo": ["宁乡", "长沙", "益阳", "资阳区", "沅江"]},
    },
    # ── 4. 市委副书记、统战部长 ──
    {
        "id": 4, "name": "张心镜", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-06", "birthplace": "",
        "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "中共沅江市委副书记、统战部部长", "current_org": "中共沅江市委员会",
        "source": "S002, S004",
        "profile_notes": "1979年生，大学。历任至2024年前为南县有关职务(2024年9月13日南县第十八届人大常委会二十一次会议免去其南县副县长职务)，后交流至沅江市任职副书记、统战部部长，兼市教工委书记、市委党校校长。任现职至2026年。",
        "career": [
            {"start": "unknown", "end": "2024-09", "org": "南县人民政府", "title": "副县长(等)", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promote": False, "note": "2024年9月13日前担任南县副县长，此后调离南县", "confidence": "confirmed", "source_ids": ["S004", "S026"]},
            {"start": "2024", "end": "", "org": "中共沅江市委员会", "title": "市委副书记、统战部部长兼教工委书记、党校校长", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promote": True, "note": "现任", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "cross_county_rotation", "systems": ["party", "government"], "geo": ["南县", "沅江"]},
    },
    # ── 5. 纪委书记 ──
    {
        "id": 5, "name": "刘慧峰", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-02", "birthplace": "",
        "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "中共沅江市委常委、市纪委书记、市监委主任", "current_org": "中共沅江市纪律检查委员会",
        "source": "S002",
        "profile_notes": "1976年生，本科。2021年7月中共沅江市第十三次代表大会选为新一届市纪委委员、常委、书记，2021年10月当选市监委主任；2026年7月新一届市委(十四届)继续留任纪检书记。",
        "career": [
            {"start": "2021-07-31", "end": "", "org": "中共沅江市纪律检查委员会", "title": "市委常委、市纪委书记，市监委主任", "level": "县处级", "system": "discipline", "rank": "副处级", "is_key_promote": True, "note": "2021年7月31日沅江市纪委十三届一次全会当选书记，10月28日市十八届人大一次会议当选市监委主任；2026年7月留任", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "discipline_track", "systems": ["discipline"], "geo": ["沅江"]},
    },
    # ── 6. 组织部长 ──
    {
        "id": 6, "name": "谌思羽", "gender": "女", "ethnicity": "汉族",
        "birth": "1987-08", "birthplace": "",
        "education": "研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "沅江市委常委、组织部部长", "current_org": "中共沅江市委员会",
        "source": "S002",
        "profile_notes": "1987年生，女，研究生。2021年任沅江市委常委、组织部部长，2025年2月按组织安排兼任市直机关工委书记。2026年7月留任。",
        "career": [
            {"start": "2021", "end": "", "org": "中共沅江市委员会", "title": "市委常委、组织部部长", "level": "县处级", "system": "organization", "rank": "副处级", "is_key_promote": True, "note": "现任；2025年主持高应良任人大常委会主任候选人见面会等事宜", "confidence": "confirmed", "source_ids": ["S002", "S008"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "organization_track", "systems": ["organization"], "geo": ["沅江"]},
    },
    # ── 7. 常务副市长 ──
    {
        "id": 7, "name": "夏鑫", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-08", "birthplace": "",
        "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "沅江市委常委、市人民政府常务副市长", "current_org": "沅江市人民政府",
        "source": "S026, S002",
        "profile_notes": "1981年生，硕士。2021年任沅江市委常委、常务副市长，分管发改、财政、园区、衡管理等工作；2026年任新一届市委常委。",
        "career": [
            {"start": "2021", "end": "", "org": "沅江市人民政府", "title": "市委常委、常务副市长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promote": True, "note": "现任", "confidence": "confirmed", "source_ids": ["S026"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": ["沅江"]},
    },
    # ── 8. 副市长(常委) ──
    {
        "id": 8, "name": "吴限忠", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-09", "birthplace": "",
        "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "沅江市委常委、市公安局党委书记、局长", "current_org": "沅江市公安局",
        "source": "S026",
        "profile_notes": "1971年生，公安局党委书记、局长。",
        "career": [
            {"start": "unknown", "end": "", "org": "沅江市公安局", "title": "市委常委、市公安局党委书记、局长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promote": False, "note": "", "confidence": "plausible", "source_ids": ["S026"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "public_security_track", "systems": ["public_security"], "geo": ["沅江"]},
    },
    # ── 9. 市人大主任(前任) ──
    {
        "id": 9, "name": "孟智勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1969-07", "birthplace": "湖南省南县",
        "education": "大学文化(中央电大法学本科)", "party_join": "1995-11", "work_start": "1987-07",
        "current_post": "前沅江市人大常委会主任(被查)", "current_org": "沅江市人大常委会(前)",
        "source": "S016, S004",
        "profile_notes": "南县华阁镇人，1987年参加工作，历任南县华阁镇联校教师、乡镇长助理/镇长/党委书记，2012年11月任南县人民政府副县长，2020年任南县人大常委会党组副书记、副主任？(注：2025年前为南县人大主任)【更正】2021年10月起任沅江市人大常委会主任；2025年6月18日被湖南省纪委监委纪律审查和监察调查(涉嫌严重违纪违法)，2025年10月30日沅江市十八届人大常委会决定终止代表资格、主任职务资格终止。",
        "career": [
            {"start": "1987-07", "end": "1998", "org": "南县华阁镇", "title": "教师/乡镇干部(历任副镇长、镇长、镇长]", "level": "乡科级", "system": "government", "rank": "", "is_key_promote": False, "note": "华阁镇联校教师、镇副镇长、党委副书记、镇长、党委书记等", "confidence": "confirmed", "source_ids": ["S016"]},
            {"start": "2000", "end": "2012-11", "org": "南县", "title": "历任镇党委书记、副县长等县委常委", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promote": True, "note": "2012年11月任南县委常委", "confidence": "confirmed", "source_ids": ["S016"]},
            {"start": "2012-11", "end": "2020", "org": "中共南县委员会", "title": "县委常委(宣传部长/政法委书记等)", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promote": False, "note": "", "confidence": "plausible", "source_ids": ["S016"]},
            {"start": "2020", "end": "2021-10", "org": "南县人大常委会", "title": "南县人大常委会主任", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promote": False, "note": "", "confidence": "plausible", "source_ids": ["S016"]},
            {"start": "2021-10-28", "end": "2025-10", "org": "沅江市人大常委会", "title": "沅江市人大常委会主任", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promote": True, "note": "2021年10月28日沅江市十八届人大一次会议当选主任；2025年6月18日被查，2025年10月30日代表资格终止", "confidence": "confirmed", "source_ids": ["S016", "S004"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [
            {"type": "disciplinary_action", "description": "2025年6月18日 湖南省纪委监委：孟智勇涉嫌严重违纪违法接受纪律审查和监察调查；2025年10月人大代表资格被终止", "date": "2025-06-18", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "extras": {"career_pattern": "local_ladder", "systems": ["government", "party", "other"], "geo": ["南县", "沅江"]},
    },
    # ── 10. 现任人大主任 ──
    {
        "id": 10, "name": "高应良", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-06", "birthplace": "湖南省益阳市资阳区",
        "education": "大学本科", "party_join": "1996-04", "work_start": "1993-07",
        "current_post": "沅江市人大常委会主任(党组书记)", "current_org": "沅江市人大常委会",
        "source": "S008, S009, S010, S011",
        "profile_notes": "1971年出生(市政府网站页写1971-08，360百科写1971-06，以人大官网1971-06待核/采用1971-06)，湖南资阳人。1993年参加工作起在沅江当地政法、组织部、党办、乡镇、经济部门成长：赤山监狱司法警察→沅江市法院书记员→镇政府司法员→大同乡党政办→市委政研室文字秘书→市委办经研室→市政府办→市经发局长→共华镇党委书记→瓯湖街道工委书记→2016年9月任沅江市副市长。2025年11月5日本市召开人大常委会主任候选人提名人选履新见面会；2026年2月沅江市十八届人大五次会议当选人大常委会主任(接任被查的孟氏)。",
        "career": [
            {"start": "1993-07", "end": "1995-04", "org": "湖南省赤山监狱", "title": "司法警察", "level": "乡科级", "system": "other", "rank": "", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "1995-04", "end": "1997-12", "org": "沅江市人民法院", "title": "赤山法庭书记员、助理审判员", "level": "乡科级", "system": "other", "rank": "", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "1997-12", "end": "2000-07", "org": "沅江市原阳罗镇", "title": "司法员、组织干事、团委书记", "level": "乡镇级", "system": "government", "rank": "", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2000-07", "end": "2003-07", "org": "沅江市原大同乡", "title": "党政办公室主任", "level": "乡镇级", "system": "government", "rank": "", "is_key_promote": False, "note": "其间在湖南省委党校法律专业学习(2001.03-2003.09)", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2003-07", "end": "2005-08", "org": "沅江市委政研室", "title": "文字秘书", "level": "乡科级", "system": "party", "rank": "", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2005-08", "end": "2008-05", "org": "沅江市委办公室", "title": "副主任科员、经研室组长", "level": "乡科级", "system": "party", "rank": "副科级", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2008-05", "end": "2009-06", "org": "沅江市人民政府办公室", "title": "党组成员、工会主席", "level": "乡科级", "system": "government", "rank": "", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2009-06", "end": "2009-09", "org": "沅江市人民政府办公室", "title": "副主任、党组成员", "level": "乡科级", "system": "government", "rank": "副科级", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2009-09", "end": "2011-02", "org": "沅江市经济发展局", "title": "局长、工委书记", "level": "乡科级", "system": "government", "rank": "正科级", "is_key_promote": True, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2011-02", "end": "2013-01", "org": "沅江市共华镇", "title": "党委书记、人大主席", "level": "乡镇级", "system": "party", "rank": "正科级", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2013-01", "end": "2016-08", "org": "沅江市瓯湖街道", "title": "工委书记、人大联組长", "level": "乡镇级", "system": "party", "rank": "正科级", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2016-09", "end": "2025-10", "org": "沅江市人民政府", "title": "副市长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promote": True, "note": "2016年12月1日沅江市第十七届人大一次会议当选副市长；负责农业农村或建设等工作分工", "confidence": "confirmed", "source_ids": ["S011", "S009"]},
            {"start": "2025-11", "end": "2026-02", "org": "沅江市人大常委会", "title": "市(候)人大常委会主任候选人", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promote": True, "note": "2025年11月5日履新见面会任党组/候选人", "confidence": "confirmed", "source_ids": ["S008"]},
            {"start": "2026-02", "end": "", "org": "沅江市人大常委会", "title": "主任(党组书记)", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promote": True, "note": "2026年2月沅江市第十八届人民代表大会第五次会议当选主任", "confidence": "confirmed", "source_ids": ["S010"]},
        ],
        "governance": [],
        "workflow": [
            {"trait": "grassroots_oriented", "evidence": "1993年起30余年步走沅江本地基层，历经司法、法院、乡镇、党办、经委、城建各系统", "confidence": "confirmed", "source_ids": ["S011"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["other", "government", "party"], "geo": ["资阳", "沅江"]},
    },
    # ── 11. 市政协主席 ──
    {
        "id": 11, "name": "刘武", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-11", "birthplace": "湖南省沅江市",
        "education": "大学文化(湖南省司法学校)", "party_join": "中共党员", "work_start": "1989-09",
        "current_post": "政协沅江市委员会主席(党组书记)", "current_org": "政协沅江市委员会",
        "source": "S027, S004",
        "profile_notes": "1968年生，湖南沅江人，早年湖南省司法学校毕业，长期在政法系统：原南大乡司法员→原北大乡公安特派员、民政所长→1998年11月起历任。2021年10月27日市政协十届一次会议当选主席。",
        "career": [
            {"start": "1989-09", "end": "1991-09", "org": "湖南省司法学校", "title": "学习法律专业", "level": "", "system": "other", "rank": "", "is_key_promote": False, "note": "司法学校法律专业学习", "confidence": "confirmed", "source_ids": ["S027"]},
            {"start": "1991-09", "end": "1993-03", "org": "沅江市原南大乡", "title": "司法员", "level": "乡镇级", "system": "government", "rank": "", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S027"]},
            {"start": "1993-03", "end": "1998-11", "org": "沅江市原北大乡", "title": "公安特派员、民政所长", "level": "乡镇级", "system": "government", "rank": "", "is_key_promote": False, "note": "期间1995.09-1997.12湖南省委党校业余大专班经济管理专业学习", "confidence": "confirmed", "source_ids": ["S027"]},
            {"start": "1998-11", "end": "2016", "org": "沅江市乡镇/市直", "title": "乡镇和市直部门历任领导职务", "level": "乡科级", "system": "government", "rank": "", "is_key_promote": False, "note": "1998年11月起在沅江乡镇及市直单位任职，具体职务待查", "confidence": "unverified", "source_ids": ["S027"]},
            {"start": "2021-10-27", "end": "", "org": "政协沅江市委员会", "title": "市政协主席、党组书记", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promote": True, "note": "2021年10月27日市政协十一届一次会议当选；现任，2026年7月继续任", "confidence": "confirmed", "source_ids": ["S027", "S004"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government", "other"], "geo": ["沅江"]},
    },
    # ── 12. 前任市长(周振宇→常德市长) ──
    {
        "id": 12, "name": "周振宇", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-01", "birthplace": "湖南省邵阳县",
        "education": "大学(中南工业大学/中南大学机电专业)", "party_join": "中共党员", "work_start": "1991",
        "current_post": "常德市人民政府市长", "current_org": "常德市人民政府",
        "source": "S022, S023",
        "profile_notes": "1970年1月生，湖南邵阳邵阳县人，1991年和中南工业大学（现中南大学）机电系毕业。原任沅江市市长(2007-2008)，历任益阳市资阳区常务副区长、区委书记，2011年12月任益阳市副市长，2021年11月任常德市委副书记、代市长、市长。与沅江渊源：2006年11月挂职沅江市委副书记、2007年任代市长/市长(其间2007年11月省委组织部安排其主持市委常委班子)。",
        "career": [
            {"start": "1991", "end": "1994-10", "org": "中南工业大学", "title": "毕业生(机电系)", "confidence": "confirmed", "is_key_promote": False, "note": ""},
            {"start": "1994-10", "end": "2006", "org": "湖南省纪委", "title": "省纪委机关干部", "rank": "正处级", "is_key_promote": False, "note": "至2006年任省纪委办公厅主任等", "confidence": "confirmed"},
            {"start": "2006-11", "end": "2007-11", "org": "沅江市人民政府", "title": "代理市长→市长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promote": True, "note": "2006年11月任沅江市委副书记、代市长；2007年1月当选市长", "confidence": "confirmed"},
            {"start": "2007-11", "end": "2011-12", "org": "中共益阳市资阳区委员会", "title": "区委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promote": True, "note": "", "confidence": "confirmed"},
            {"start": "2011-12", "end": "2021-04", "org": "益阳市人民政府", "title": "副市长、市委常委", "level": "地市级", "system": "government", "rank": "副厅级", "is_key_promote": True, "note": "2011年12月任益阳市副市长，后任市委常委、市委秘书长等", "confidence": "confirmed"},
            {"start": "2021-04", "end": "2021-11", "org": "中共怀化市委", "title": "市委副书记", "level": "地市级", "system": "party", "rank": "副厅级", "is_key_promote": True, "note": "", "confidence": "confirmed"},
            {"start": "2021-11", "end": "", "org": "常德市人民政府", "title": "市委副书记、市长", "level": "地市级", "system": "government", "rank": "正厅级", "is_key_promote": True, "note": "2021年11月19日任常德市委副书记、代市长；2022年1月当选市长，现任", "confidence": "confirmed", "source_ids": ["S022", "S023"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "cross_county_rotation", "systems": ["party", "government"], "geo": ["邵阳", "长沙", "沅江", "资阳", "益阳", "怀化", "常德"]},
    },
    # ── 13. 前任市长肖胜利(落马) ──
    {
        "id": 13, "name": "肖胜利", "gender": "男", "ethnicity": "汉族",
        "birth": "1965", "birthplace": "湖南省",
        "education": "大学", "party_join": "中共党员", "work_start": "",
        "current_post": "前沅江市市长(已判刑入狱)", "current_org": "沅江市人民政府(前)",
        "source": "S017, S018",
        "profile_notes": "2011年12月任沅江市市长。2015年8月5日被湖南省纪委立案调查；2016年6月被开出党籍、公职(双开)，2017年12月28日长沙市中级人民法院一审以受贿罪判处有期徒刑5年。",
        "career": [
            {"start": "2011-12", "end": "2015-08", "org": "沅江市人民政府", "title": "市长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promote": True, "note": "被查时任市长", "confidence": "confirmed", "source_ids": ["S017"]},
            {"start": "2015-08", "end": "2017", "org": "被调查", "title": "接受纪律审查和监察调查(2015.08.05双开)", "level": "", "system": "discipline", "rank": "", "is_key_promote": False, "note": "2015年8月5日被查，双开，2017年12月28日一审获刑5年", "confidence": "confirmed", "source_ids": ["S017", "S018"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [{"type": "disciplinary_action", "description": "2015.08.05被纪律审查，2016年双开，2017.12.28一审以受贿罪判处5年有期徒刑", "date": "2015-08-05", "confidence": "confirmed", "source_ids": ["S017", "S018"]}],
        "extras": {"career_pattern": "discipline_fall", "systems": ["government"], "geo": ["沅江"]},
    },
    # ── 14. 前任市长谢君毅 ──
    {
        "id": 14, "name": "谢君毅", "gender": "男", "ethnicity": "土家族",
        "birth": "1980-10", "birthplace": "湖南省湘乡",
        "education": "大学(湘潭大学毕业)", "party_join": "中共党员", "work_start": "2002-08",
        "current_post": "中共娄底市委常委、市委秘书长(拟任省直正厅级)", "current_org": "中共娄底市委",
        "source": "S024, S029",
        "profile_notes": "1980年生，湖南湘乡人，土家族，湘潭大学文学学士，中央党校研究生。2002年8月起在益阳市委办公室工作，2009年10月任沅江市副市长，2011年任共青团益阳市委书记，2013年任安化县委副书记(正处级)，2015年12月任沅江市委副书记、市长(至2017年6月)，2017年7月任共青团湖南省委副书记，2020年9月任娄底市副市长，2025年任娄底市委常委、市委秘书长；2025年12月湖南省委组织部公示拟任省直单位正厅级领导职务。",
        "career": [
            {"start": "2002-08", "end": "2009-10", "org": "中共益阳市委办公室", "title": "经研究/秘书岗位", "level": "地市级", "system": "party", "rank": "", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S029"]},
            {"start": "2009-10", "end": "2011-01", "org": "沅江市人民政府", "title": "副市长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promote": False, "note": "", "confidence": "confirmed", "source_ids": ["S029"]},
            {"start": "2011-01", "end": "2012-04", "org": "共青团益阳市委员会", "title": "书记", "level": "乡科级", "system": "other", "rank": "正科级", "is_key_promote": True, "note": "", "confidence": "confirmed", "source_ids": ["S029"]},
            {"start": "2012-04", "end": "2015-12", "org": "中共安化县委员会", "title": "县委副书记(正处级)", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promote": True, "note": "", "confidence": "confirmed", "source_ids": ["S029"]},
            {"start": "2015-12", "end": "2017-06", "org": "沅江市人民政府", "title": "市长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promote": True, "note": "2015年12月至2017年6月任沅江市市长", "confidence": "confirmed", "source_ids": ["S029"]},
            {"start": "2017-07", "end": "2020-09", "org": "共青团湖南省委", "title": "副书记→书记", "level": "厅局级", "system": "other", "rank": "副厅级", "is_key_promote": True, "note": "2017年7月任团省委副书记，后任书记", "confidence": "confirmed", "source_ids": ["S029"]},
            {"start": "2020-09", "end": "2025", "org": "娄底市人民政府", "title": "副市长", "level": "地市级", "system": "government", "rank": "副厅级", "is_key_promote": True, "note": "2020年9月补选为娄底市副市长", "confidence": "confirmed", "source_ids": ["S029"]},
            {"start": "2025", "end": "", "org": "中共娄底市委", "title": "市委常委、市委秘书长", "level": "地市级", "system": "party", "rank": "副厅级", "is_key_promote": True, "note": "2025年12月13日湖南省委组织部公示：拟任省直单位正厅级领导职务", "confidence": "confirmed", "source_ids": ["S024"]},
        ],
        "governance": [],
        "workflow": [],
        "risk": [],
        "extras": {"career_pattern": "cross_county_rotation|provincial_department", "systems": ["party", "government", "other"], "geo": ["益阳", "沅江", "安化", "湖南省", "娄底"]},
    },
]

# ══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共沅江市委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市沅江市"},
    {"id": 2, "name": "沅江市人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市沅江市"},
    {"id": 3, "name": "沅江市人大常委会", "type": "人大", "level": "县处级", "parent": "益阳市人大常委会", "location": "湖南省益阳市沅江市"},
    {"id": 4, "name": "政协沅江市委员会", "type": "政协", "level": "县处级", "parent": "政协益阳市委员会", "location": "湖南省益阳市沅江市"},
    {"id": 5, "name": "中共沅江市纪律检查委员会/市监委", "type": "纪委", "level": "县处级", "parent": "中共沅江市委", "location": "湖南省益阳市沅江市"},
    {"id": 6, "name": "沅江市公安局", "type": "政府", "level": "乡科级", "parent": "沅江市人民政府", "location": "湖南省益阳市沅江市"},
    {"id": 7, "name": "中共益阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省益阳市"},
    {"id": 8, "name": "益阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省益阳市"},
    {"id": 9, "name": "中共湖南省委巡视组(十五组)", "type": "党委", "level": "省部级", "parent": "中共湖南省委", "location": "湖南省长沙市"},
    {"id": 10, "name": "湖南师范大学", "type": "事业单位", "level": "厅局级", "parent": "湖南省教育厅", "location": "湖南省长沙市"},
    {"id": 11, "name": "中共益阳市资阳区委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市资阳区"},
    {"id": 12, "name": "常德市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省常德市"},
    {"id": 13, "name": "中共石门县委员会", "type": "党委", "level": "县处级", "parent": "中共常德市委", "location": "湖南省常德市石门县"},
    {"id": 14, "name": "石门县人民政府", "type": "政府", "level": "县处级", "parent": "常德市人民政府", "location": "湖南省常德市石门县"},
    {"id": 15, "name": "邵阳市中级人民法院", "type": "政法", "level": "地市级", "parent": "湖南省高级人民法院", "location": "湖南省邵阳市"},
    {"id": 16, "name": "中共南县委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市南县"},
    {"id": 17, "name": "南县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市南县"},
    {"id": 18, "name": "南县人大常委会", "type": "人大", "level": "县处级", "parent": "益阳市人大常委会", "location": "湖南省益阳市南县"},
    {"id": 19, "name": "安化县(各乡镇/县直)", "type": "乡镇", "level": "乡科级", "parent": "安化县人民政府", "location": "湖南省益阳市安化县"},
    {"id": 20, "name": "安化县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市安化县"},
    {"id": 21, "name": "共青团湖南省委", "type": "群团", "level": "厅局级", "parent": "共青团中央/中共湖南省委", "location": "湖南省长沙市"},
    {"id": 22, "name": "中共娄底市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省娄底市"},
    {"id": 23, "name": "娄底市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省娄底市"},
    {"id": 24, "name": "中共怀化市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省怀化市"},
    {"id": 25, "name": "湖南省纪委", "type": "纪委", "level": "省部级", "parent": "中共湖南省委", "location": "湖南省长沙市"},
]

# ══════════════════════════════════════════════════════════════════════════
# POSITIONS (flattened from persons data + dedicated rows)
# ══════════════════════════════════════════════════════════════════════════
_position_orgmap = {}
positions = []


def _add_pos(person_id, org_id, title, start, end="", rank="", note="", source_ids=("",)):
    positions.append({
        "person_id": person_id, "org_id": org_id, "title": title,
        "start": start, "end": end, "rank": rank, "note": note,
        "source": ",".join(source_ids),
    })


def _seed_positions():
    # 罗必胜 (1) - key positions
    _add_pos(1, 7, "中共益阳市委(交流干部岗位)", "", "", "", "早年安化县基层(1991-2007)；2007.11壹宁县副政府副县长、2011.06县委常委、政法委书记", "S007")
    _add_pos(1, 20, "安化县人民政府副县长/县委常委、政法委书记", "2007-11", "2016-08", "副处级", "安化县副县长(2007.11-2011.06)；安化县委常委、政法委书记(2011.06-2016.08)", "S007")
    _add_pos(1, 2, "沅江市委常委、常务副市长", "2016-08", "2020-04", "副处级", "2016年8月交流到沅江市", "S007")
    _add_pos(1, 1, "沅江市委副书记", "2020-04", "2021-10", "副处级", "S007")
    _add_pos(1, 2, "沅江市人民政府市长", "2021-10", "2025-12", "正处级", "2021年7月任市长候选人，10月当选", "S007")
    _add_pos(1, 1, "中共沅江市委书记", "2025-12-22", "", "正处级", "现任", "S001")
    # 廖江华
    _add_pos(2, 15, "早期工作(邵阳市中级人民法院)", "", "", "", "早期", "S013")
    _add_pos(2, 13, "石门县委常委、常务副县长", "2022-10", "2024-08", "副处级", "", "S012")
    _add_pos(2, 13, "石门县委副书记、统战部部长(兼)", "2024-08", "2026-01", "副处级", "S012")
    _add_pos(2, 1, "沅江市委副书记", "2026-01-23", "", "副处级", "", "S013")
    _add_pos(2, 2, "沅江市人民政府代理市长", "2026-02-05", "", "正处级", "现任(代理)", "S012")
    # 杨智勇
    _add_pos(3, 10, "湖南师范大学(学习+工作)", "1993-09", "2016-08", "", "历史学本科至博士、留校工作", "S006")
    _add_pos(3, 11, "益阳市资阳区委副书记", "2016-08", "2017-05", "副处级", "S006")
    _add_pos(3, 1, "沅江市委副书记→代市长", "2017-05", "2017-12", "副处级", "S006")
    _add_pos(3, 2, "沅江市人民政府市长", "2017-12", "2021-07", "正处级", "2017.12-2021.07", "S006")
    _add_pos(3, 1, "中共沅江市委书记", "2021-07-03", "2025-11", "正处级", "2025年11月调离", "S001")
    # 张心镜
    _add_pos(4, 17, "南县副县长(等)", "", "2024-09", "副处级", "2024-09-13 南县人大常委会免去", "S026")
    _add_pos(4, 1, "沅江市委副书记、统战部部长", "2024", "", "副处级", "现任", "S002")
    # 刘慧峰
    _add_pos(5, 5, "市委常委、市纪委书记、市监委主任", "2021-07-31", "", "副处级", "现任", "S002")
    # 谌思羽
    _add_pos(6, 1, "市委常委、组织部部长", "2021", "", "副处级", "现任", "S002")
    # 夏鑫
    _add_pos(7, 2, "市委常委、常务副市长", "2021", "", "副处级", "现任", "S026")
    # 吴限忠
    _add_pos(8, 6, "市委常委、市公安局党委书记、局长", "", "", "副处级", "S026")
    # 孟智勇
    _add_pos(9, 19, "南县华阁镇(教师/乡镇领导)", "1987-07", "2000", "乡科级", "S016")
    _add_pos(9, 16, "南县委常委、(先后任县委办主任/宣传部长等)", "2000", "2021-10", "副处级", "S016")
    _add_pos(9, 3, "沅江市人大常委会主任", "2021-10-28", "2025-10", "正处级", "2025年6月18日被查；2025年10月代表资格终止", "S016")
    # 高应良
    _add_pos(10, 2, "沅江市人民政府副市长(历任多岗)", "2016-09", "2025-10", "副处级", "1993年起在沅江政法/乡镇/办公室系统历任，2009年任经发局长、2011年瓯湖街道书记；2009-2016先后于各乡镇、市直单位任职", "S011")
    _add_pos(10, 3, "沅江市人大常委会主任、党组书记", "2026-02", "", "正处级", "现任；2025-11履新见面会候选人", "S010")
    # 刘武
    _add_pos(11, 4, "政协沅江市委员会主席、党组书记", "2021-10-27", "", "正处级", "现任", "S027")
    # 周振宇
    _add_pos(12, 8, "益阳市人民政府副市长/市委常等", "2011-12", "2021-04", "副厅级", "之前任沅江市长、资阳区委书记", "S023")
    _add_pos(12, 24, "怀化市委副书记", "2021-04", "2021-11", "副厅级", "S023")
    _add_pos(12, 12, "常德市委副书记、市长", "2021-11", "", "正厅级", "现任", "S022")
    # 肖胜利
    _add_pos(13, 2, "沅江市人民政府市长", "2011-12", "2015-08", "正处级", "被查", "S017")
    # 谢君毅
    _add_pos(14, 21, "共青团湖南省委副书记→书记", "2017-07", "2020-09", "副厅级", "S029")
    _add_pos(14, 23, "娄底市人民政府副市长", "2020-09", "2025", "副厅级", "S029")
    _add_pos(14, 22, "娄底市委常委、市委秘书长", "2025", "", "副厅级", "拟任省直单位正厅级", "S024")


_seed_positions()

# ══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════
relationships = [
    {"person_a": 1, "person_b": 3, "type": "前任/继任", "context": "杨2021-2025任市委书记，2025年11月调离后罗必胜(原市长)升任市委书记", "overlap_org": "中共沅江市委员会", "overlap_period": "2021-2025"},
    {"person_a": 1, "person_b": 2, "type": "前后任市长/搭档", "context": "罗必胜2021-2025年任市长，2026年2月辞去市长后，廖江华任代理市长；同时罗必胜(书记)与廖江华(市委副书记、代理市长)为现任党政正职搭档", "overlap_org": "沅江市人民政府", "overlap_period": "2026-至今"},
    {"person_a": 3, "person_b": 12, "type": "前后任市长", "context": "周振宇2007-2008年任沅江市长；杨智勇2017-2021年任市长", "overlap_org": "沅江市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "前后任市长", "context": "谢君毅2015-2017年任沅江市长，罗必胜2021年接任市长", "overlap_org": "沅江市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 14, "type": "前后任市长", "context": "谢君毅2015-2017年任市长，杨智勇2017-12年接任", "overlap_org": "沅江市人民政府", "overlap_period": "2015-2017"},
    {"person_a": 13, "person_b": 14, "type": "前后任市长", "context": "肖胜利2011-2015任市长(落马)，谢君毅2015年12月接任市长", "overlap_org": "沅江市人民政府", "overlap_period": "2015"},
    {"person_a": 9, "person_b": 10, "type": "前任/继任", "context": "孟智勇2021-2025任沅江市人大常委会主任(2025年6月被查)，高应良2026年2月当选接任", "overlap_org": "沅江市人大常委会", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 9, "type": "上下级", "context": "杨智勇(市委书记)、孟智勇(人大常委会主任)2021-2025年在沅江市委/人大班子共事", "overlap_org": "沅江市", "overlap_period": "2021-2025"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "罗必胜(市长/书记)与孟智勇(人大主任)2021-2025年在沅江市政府/人大常委会班子共事", "overlap_org": "沅江市", "overlap_period": "2021-2025"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "罗必胜(市长/书记)与高应良(副市长→人大主任)在沅江市政府班子共事至2025年，后高2026年任人大主任", "overlap_org": "沅江市人民政府", "overlap_period": "2016-2026"},
    {"person_a": 2, "person_b": 13, "type": "跨市交流参考", "context": "廖江华从常德市石门县委副书记调任沅江市委副书记、代理市长，属跨市交流", "overlap_org": "常德/益阳", "overlap_period": "2026"},
    {"person_a": 12, "person_b": 8, "type": "前后任/共事", "context": "周振宇2012年任益阳市副市长，晚于沅江市长任内；对沅江市较熟悉", "overlap_org": "益阳市", "overlap_period": "2006-2012"},
    {"person_a": 3, "person_b": 5, "type": "上下级", "context": "杨智勇为市委书记期间，刘慧峰任纪委书记(纪委监委)", "overlap_org": "中共沅江市委员会", "overlap_period": "2021-2025"},
    {"person_a": 3, "person_b": 11, "type": "班委搭档", "context": "杨智勇(书记)与刘武(政协主席)2021-2025年间在沅江市四套班子共事", "overlap_org": "沅江市", "overlap_period": "2021-2025"},
    {"person_a": 1, "person_b": 11, "type": "现任班委搭档", "context": "罗必胜(书记)与刘武(政协主席)现任沅江市班子主要成员", "overlap_org": "沅江市", "overlap_period": "2025-至今"},
]

# Notes: relationships reference persons by id matched to list — ids must exist in `persons`.

# ══════════════════════════════════════════════════════════════════════════
# DATABASE BUILD (legacy schema, mirroring scripts/build/build_桃江县_data.py)
# ══════════════════════════════════════════════════════════════════════════
def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    for t in ["relationships", "positions", "organizations", "persons"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '',
        start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id))""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id))""")
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})",
                     [p.get(c, "") for c in cols_p])
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})",
                     [o.get(c, "") for c in cols_o])
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})",
                     [pos.get(c, "") for c in cols_pos])
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})",
                     [r.get(c, "") for c in cols_r])
    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ══════════════════════════════════════════════════════════════════════════
# GEXF (string formatting per gexf_pattern.md)
# ══════════════════════════════════════════════════════════════════════════
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(title):
    t = title or ""
    if "书记" in t and "副" not in t:
        return "255,50,50"
    if "市长" in t and "副" not in t and "代理" not in t:
        return "50,100,255"
    if "纪委" in t:
        return "255,165,0"
    if "主任" in t or "主席" in t:
        return "200,120,40"
    if "副" in t or "代理" in t:
        return "100,150,220"
    return "100,100,100"


def org_color(o):
    return {
        "党委": "255,200,200", "政府": "200,200,255", "纪委": "255,200,150",
        "开发区": "200,255,200", "乡镇": "255,255,200", "事业单位": "220,220,220",
        "群团": "255,220,255", "人大": "200,255,255", "政协": "255,240,200",
        "政法": "200,220,255",
    }.get(o, "200,200,200")


def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>沅江市领导班子工作关系网络 — 含党政正职、人大政协、前任后任、纪检组织部门及关联组织</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if p["id"] in (1, 2, 3) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        cr, cg, cb = c.split(",")
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"])
        cr, cg, cb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    added = set()
    for pos in positions:
        pid, oid = pos["person_id"], pos["org_id"]
        if oid not in {o["id"] for o in organizations}:
            continue
        key = f"p{pid}-o{oid}-{pos['title']}"
        if key in added:
            continue
        added.add(key)
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════
# PERSON JSON (full schema per person_graph_json.md — required by process_tmp)
# ══════════════════════════════════════════════════════════════════════════
def build_person_json(p: dict) -> dict:
    pid = p["id"]
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        system = "other"
        title = pos["title"]
        if "委" in title or "书记" in title:
            system = "party"
        elif "法院" in title or "公安" in title or "政法" in title:
            system = "public_security"
        elif "纪委" in title or "监委" in title:
            system = "discipline"
        elif "政府" in title or "市长" in title or "镇长" in title or "乡" in title:
            system = "government"
        elif "组织部" in title:
            system = "organization"
        career_timeline.append({
            "start": pos["start"] or "unknown", "end": pos["end"] or "present",
            "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
            "title": title, "level": pos.get("rank", ""), "location": "",
            "system": system, "rank": pos.get("rank", ""),
            "notes": pos.get("note", ""), "confidence": "confirmed",
            "source_ids": [s for s in pos.get("source", "").split(",") if s],
        })
    if not career_timeline:
        if pid not in (3, 4, 9, 10, 12, 13, 14):
            career_timeline.append({
                "start": "unknown", "end": "present", "org": p.get("current_org", ""),
                "title": p.get("current_post", ""), "level": "县处级", "location": "湖南省益阳市沅江市",
                "system": "other", "rank": "", "is_key_promotion": False,
                "notes": "公开资料有限，任职起始时间待核。", "confidence": "unverified", "source_ids": [],
            })
    rels = []
    for r in relationships:
        if r["person_a"] == pid or r["person_b"] == pid:
            other = r["person_b"] if r["person_a"] == pid else r["person_a"]
            other_name = next((x["name"] for x in persons if x["id"] == other), str(other))
            rels.append({
                "person": other_name, "person_id": f"yuanjiang_{other}",
                "relationship_type": r["type"], "strength": "medium",
                "evidence": r["context"], "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"], "direction": "undirected",
                "confidence": "confirmed", "source_ids": [],
            })
    src_ids = [s for s in p.get("source", "").split(",") if s]
    source_register = [dict(s) for s in SOURCES if s["id"] in src_ids]
    open_qs = []
    if not p.get("birth"):
        open_qs.append({"priority": "high", "question": f"{p['name']}出生年月缺失", "why_it_matters": "身份信息完整性", "suggested_queries": [], "last_attempted": AS_OF})
    if not p.get("birthplace"):
        open_qs.append({"priority": "medium", "question": f"{p['name']}籍贯缺失", "why_it_matters": "地域网络分析", "suggested_queries": [], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_qs.append({"priority": "medium", "question": f"{p['name']}参加工作年份缺失", "why_it_matters": "履历完整性", "suggested_queries": [], "last_attempted": AS_OF})
    if "unverified" in p.get("profile_notes", "") or pid == 3:
        open_qs.append({"priority": "high", "question": f"{p['name']}离开沅江后的新职务未公开", "why_it_matters": "前任去向网络追踪", "suggested_queries": [], "last_attempted": AS_OF})
    # governance / style / risk from P
    governance = p.get("governance", []) or []
    style = p.get("work_style", p.get("workflow", [])) or []
    risks = p.get("risk", []) or []
    if not risks:
        risks = [{"type": "none_found", "description": f"截至{AS_OF}未检索到{p['name']}的纪律处分或负面报道(当事人简历薄的情况除外)", "date": AS_OF, "confidence": "unverified", "source_ids": []}]
    extras = p.get("extras", {})
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "湖南省", "city": "益阳市", "region": "沅江市", "job": p.get("current_post", ""), "task_id": "hunan_沅江市", "time_focus": "2016-2026"},
        "identity": {"person_id": f"yuanjiang_{p['name']}_{p.get('birth', '')[:4]}", "name": p["name"], "aliases": [], "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""), "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""), "native_place": "", "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}], "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""), "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth', '')}", "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}", "official_profile_url": ""}},
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""), "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": "conf" in p.get("profile_notes", "") or pid in (1, 2), "source_ids": src_ids},
        "career_timeline": career_timeline,
        "organizations": [
            {"org_id": str(pos["org_id"]), "name": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""), "role": pos["title"], "period": f"{pos.get('start', '')}-{pos.get('end', 'present')}", "source_ids": []}
            for pos in positions if pos["person_id"] == pid
        ],
        "relationships": rels,
        "governance_record": governance,
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": extras.get("career_pattern", "local_ladder"), "systems_experience": extras.get("systems", []), "geographic_pattern": extras.get("geo", []), "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": style, "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": risks,
        "source_register": source_register,
        "confidence_summary": {"identity": "confirmed" if p.get("birth") else "plausible", "current_role": "confirmed", "career_completeness": "partial" if len(career_timeline) >= 3 else "thin", "relationship_confidence": "medium", "biggest_gap": open_qs[0]["question"] if open_qs else ""},
        "open_questions": open_qs,
    }


def write_person_json(p: dict) -> str:
    obj = build_person_json(p)
    job_slug = p["current_post"].replace(" ", "_").replace("(", "").replace(")", "")
    fname = f"{TODAY}-湖南省-益阳市-{job_slug}-{p['name']}.json"
    fpath = Path(JSON_DIR) / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return fname


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
def main() -> None:
    print("=" * 60)
    print("  沅江市领导班子工作关系网络 — 数据构建")
    print(f"  调查日期: {AS_OF}")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Person JSONs:")
    for p in persons:
        fname = write_person_json(p)
        print(f"  {fname}")
    print("\nDone.")
    print(f"DB:    {DB_PATH}")
    print(f"GEXF:  {GEXF_PATH}")


if __name__ == "__main__":
    main()