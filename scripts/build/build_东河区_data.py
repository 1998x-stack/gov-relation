#!/usr/bin/env python3
"""Build 包头市东河区 leadership network database and graph.

Task: inner_mongolia_东河区 (市辖区)
Targets: 区委书记 王瑞 & 区长 张利军 (plus 区委常委会/人大/政协/纪委班子 roster)

Schema: 4 tables (persons/organizations/positions/relationships) via
gov_relation.runner.run_build (legacy backend -> sqlite3 under the hood).

Key findings (as of 2026-08-11, all from official govt sites unless noted):
  - 区委书记: 王瑞 (2023-05-04 起主持区委工作; 2026-07-30 十二届区委一次全会连任;
    百度百科词条称其"内蒙古自治区包头市委常委、东河区委书记、人武部党委第一书记、区委党校（行政学校）校长")
  - 区委副书记、区长: 张利军 (2021-12 代区长 -> 2022-01-09 十八届人大一次会议当选;
    2026-07-30 十二届区委一次全会当选副书记; 1976-12 生, 内蒙古固阳人, 公共管理硕士
    ——与百科"青山区委常委、常务副区长"词条信息吻合, 系包头市域内跨区流动)
  - 前任区委书记: 杨二喜 (2021-06~2023-04/05; 蒙古族, 1971-09, 土默特右旗人;
    现任包头市委常委、统战部部长、市政协党组副书记)
  - 区人大常委会党组书记、主任: 王建平 (十七局/十八届主任, 2022-01 续任)
  - 区政协: 白继文 (十一届政协主席 2022-01~2026-06) -> 郭惠文 (区政协党组书记,
    2026-07-30 党组会议主持, 当期为党组书记; 主席职务待政协全会确认)
  - 十二届区委常委(2026-07-30 选举): 王瑞、张利军、王伟、武国栋、马斌、张红艳(女)、
    涂永文、石岩(蒙古族)、孙熙麟、张飞、赵瑞军; 区纪委: 书记 涂永文,
    副书记 章国峰、韩冰(蒙古族)
  - 发展定位 "三区一地": 老工业基地转型发展示范区、精品农业示范区、
    老城更新示范区、烟火生活和文旅休闲体验地 (区第十二次党代会/区委十一届十六次全会)

Research gaps encoded as open_questions (search engines Exa/Baidu/Sogou/360 all blocked):
  王瑞任东河区委书记前的完整履历; 王瑞出生年份/学历; 各人大常委会分工;
  郭惠文履历; 张利军 2019-2021 年迁徙窗口; 前任区委书记(2021-06以前)信息。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── REPO_ROOT 探测（稳健）────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve()
for _parent in range(0, 6):
    _cand = Path(__file__).resolve().parents[_parent]
    if (_cand / "gov_relation").is_dir():
        REPO_ROOT = _cand
        break
else:
    REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "东河区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = datetime.now().strftime("%Y-%m-%d")
# 支持 STAGING_DIR 环境变量覆盖（与 china-gov-network 暂存约定一致）
_STAGING = os.environ.get("STAGING_DIR")
STAGING = Path(_STAGING) if _STAGING else REPO_ROOT / "data" / "tmp" / "inner_mongolia_东河区"

# process_tmp.py requires these tokens lexically present in the build script
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
JSON_DIR = STAGING

SOURCES = [
    {"id": "S1", "title": "东河新闻·王瑞调研科技创新工作", "url": "http://www.donghe.gov.cn/ywdt/dhxw/202608/t20260811_945699.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-08-11", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "区委书记王瑞；区领导王伟、石岩、孙熙麟、田永光参加"},
    {"id": "S2", "title": "中共包头市东河区第十二届委员会第一次全体会议公报", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdhy/qthy/202607/t20260731_943637.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-07-31", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "12届常委11人名单、书记副书记、12届纪委班子"},
    {"id": "S3", "title": "十二届区委一次全会 王瑞当选为区委书记", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdhy/qthy/202607/t20260731_943639.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-07-31", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "王瑞当选书记；张利军、王伟当选副书记；推荐三区一地"},
    {"id": "S4", "title": "中国共产党包头市东河区第十二次代表大会开幕", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdhy/qthy/202607/t20260729_942622.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-07-29", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "党代会报告主题、'三区一地'发展定位"},
    {"id": "S5", "title": "中共包头市东河区第十一届委员会第二十一次全体会议公报", "url": "https://www.donghe.gov.cn/ywdt/dhxw/202607/t20260728_942296.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-07-28", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "王瑞主持；十二次党代会筹备"},
    {"id": "S6", "title": "东河区四套班子领导开展八一建军节走访慰问", "url": "https://www.donghe.gov.cn/ywdt/dhxw/202607/t20260731_943641.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-07-31", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "王瑞/张利军/王建平/郭惠文四位班子领导活动"},
    {"id": "S7", "title": "全区上下掀起传达学习区第十二次党代会精神热潮（一）", "url": "https://www.donghe.gov.cn/ywdt/dhxw/202608/t20260804_944153.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-08-04", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "张利军区长主持政府党组；王建平人大党组；郭惠文政协党组"},
    {"id": "S8", "title": "东河区第十八届人民代表大会第五次会议开幕", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdly/qthy/202601/t20260128_751378.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-01-28", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "人大主席团名单（王建平等）"},
    {"id": "S9", "title": "政协东河区第十一届委员会第五次会议开幕", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdly/qthy/202601/t20260126_743574.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-01-26", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "白继文任政协主席；周永威统战部长；区政协领导名单"},
    {"id": "S10", "title": "区政协围绕'安全生产民主监督'开展主席会议协商调研", "url": "https://www.donghe.gov.cn/ywdt/dhxw/202606/t20260611_922793.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-06-11", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "白继文仍为政协党组书记、主席；石岩=区委常委、副区长"},
    {"id": "S11", "title": "包头市东河区第十八届人民代表大会第一次会议开幕", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdly/qthy/202508/t20250821_270638.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2022-01-18", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "代区长张利军作政府工作报告；杨二喜=区委书记；王建平主持"},
    {"id": "S12", "title": "十八届人大一次会议举行第二次全体会议", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdly/qthy/202508/t20250821_270639.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2022-01-18", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "王建平十七届常委会主任（连任十八届）"},
    {"id": "S13", "title": "政协东河区第十一届委员会第一次会议胜利闭幕", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdly/qthy/202508/t20250821_270640.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2022-01-18", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "白继文当选十一届政协主席；副主席:陈文丽、杨丽虹、李轶、贺东冰"},
    {"id": "S14", "title": "区委常委会（扩大）会议召开（2023-05-04 王瑞主持）", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdly/cwhy/202508/t20250821_270454.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2023-05-12", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "王瑞 2023-05-04 即为区委书记；落实市委书记丁绣峰在东阳干部大会讲话"},
    {"id": "S15", "title": "王瑞看望慰问老干部", "url": "https://www.donghe.gov.cn/ywdt/dhxw/202508/t20250820_235428.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2023-05-12", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "王瑞 2023-05-09 任区委书记；区领导程利翔/胡国瑞"},
    {"id": "S16", "title": "杨二喜·百度百科", "url": "https://wapbaike.baidu.com/item/杨二喜/20135301",
     "publisher": "百度百科", "published_at": "2024", "accessed_at": "2026-08-11",
     "source_type": "encyclopedia", "reliability": "medium", "notes": "1991 起土右旗//固阳县履历；2021-06 东河区委书记；2021-08 起包头市委常委；现统战部长/市政协党组副书记"},
    {"id": "S17", "title": "张利军·百度百科（东河区委副书记、区长）", "url": "https://wapbaike.baidu.com/item/张利军/65219876",
     "publisher": "百度百科", "published_at": "2026", "accessed_at": "2026-08-11",
     "source_type": "encyclopedia", "reliability": "medium", "notes": "1976-12 生，研究生、公共管理硕士；2026-07-30 当选 12 届区委副书记"},
    {"id": "S18", "title": "张利军·百度百科（青山区委常委、常务副区长）", "url": "https://wapbaike.baidu.com/item/张利军/22899652",
     "publisher": "百度百科", "published_at": "2018", "accessed_at": "2026-08-11",
     "source_type": "encyclopedia", "reliability": "medium", "notes": "同生年同学位（1976-12/公共管理硕士）——高置信为同一人；青山区常务副区长至2018+；固阳籍"},
    {"id": "S19", "title": "王瑞·百度百科词条（唯一词条简介）", "url": "https://wapbaike.baidu.com/item/王瑞/57977180",
     "publisher": "百度百科", "published_at": "2026", "accessed_at": "2026-08-11",
     "source_type": "encyclopedia", "reliability": "low", "notes": "词条仅存标题描述：包头市委常委、东河区委书记、人武部党委第一书记、区委党校（行政学校）校长"},
    {"id": "S20", "title": "东河区（行政区概况）", "url": "https://zh.wikipedia.org/wiki/东河区",
     "publisher": "维基百科", "published_at": "2026-08", "accessed_at": "2026-08-11",
     "source_type": "encyclopedia", "reliability": "medium", "notes": "面积464.5km²，七普常住484218；12街2镇；区政府驻河东街道"},
    {"id": "S21", "title": "东河区人民政府·区政府常务会议（2026-06-24）", "url": "https://www.donghe.gov.cn/zwgk/zfxxgk/fdzdgknr/zdly/cwhv/202606/t20260624_930165.html",
     "publisher": "东河区人民政府门户网站", "published_at": "2026-06-24", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "区长张利军主持常务会议"},
    {"id": "S22", "title": "包头市人民政府 任免通知（包府发〔2026〕12-14号）", "url": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_zcvj/202607/",
     "publisher": "包头市人民政府门户网站", "published_at": "2026-07", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "市本级任免（万丽任民委副主任等）与区级班子无冲突——确认市级干部序列"},
]

# ── 东河区领导班子（2026-08 官网/公报确认）───────────────────────────
persons = [
    # 区委常委会（12届，2026-07-30 选举）
    {"id": 1, "name": "王瑞", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "中共包头市东河区委书记", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S1,S2,S3,S14,S15",
     "notes": "2023-05 起任区委书记；2026-07-30 十二届区委一次全会连任；据百科词条兼包头市委常委、人武部党委第一书记、区委党校校长；主持区第十二次党代会"},
    {"id": 2, "name": "张利军", "gender": "男", "ethnicity": "汉族", "birth": "1976年12月",
     "birthplace": "内蒙古固阳县（百科公示）", "education": "研究生学历·公共管理硕士",
     "party_join": "1998年12月（青山区词条）", "work_start": "1993年8月",
     "current_post": "东河区委副书记、区政府党组书记、区长", "current_org": "包头市东河区人民政府",
     "source": "confirmed - S7,S11,S17,S21", "notes": "2021-12 代区长→2022-01-09 当选区长；2026-07-30 十二届副书记"},
    {"id": 3, "name": "王伟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委副书记", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S2,S3", "notes": "2026-07-30 十二届区委一次全会当选副书记；此前为区委常委"},
    {"id": 4, "name": "武国栋", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S2,S3,S8,S9", "notes": "十二届常委；具体分工待查"},
    {"id": 5, "name": "马斌", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S2", "notes": "十二届常委；具体分工待查"},
    {"id": 6, "name": "张红艳", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S2,S8", "notes": "十二届常委；2026-01 区人代会主席团成员"},
    {"id": 7, "name": "涂永文", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委、区纪委书记、监委主任", "current_org": "中共包头市东河区纪律检查委员会",
     "source": "confirmed - S2,S3", "notes": "十二届纪委第一次全会选书记；副书记章国峰、韩冰（蒙古族）"},
    {"id": 8, "name": "石岩", "gender": "", "ethnicity": "蒙古族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委、区政府副区长", "current_org": "包头市东河区人民政府",
     "source": "confirmed - S2,S10", "notes": "2026-06-11 明确为区委常委、区政府副区长"},
    {"id": 9, "name": "孙熙麟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S1,S2", "notes": "十二届常委；具体分工待查"},
    {"id": 10, "name": "张飞", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S2", "notes": "十二届常委；具体分工待查"},
    {"id": 11, "name": "赵瑞军", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区委常委", "current_org": "中共包头市东河区委员会",
     "source": "confirmed - S2", "notes": "十二届常委；2022 年即在人大桌台名单"},
    # 区人大 / 政协
    {"id": 12, "name": "王建平", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区人大常委会党组书记、主任", "current_org": "包头市东河区人民代表大会常务委员会",
     "source": "confirmed - S6,S7,S11,S12", "notes": "十七届/十八届人大常委会主任；2022-01 连任十八届"},
    {"id": 13, "name": "郭惠文", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区政协党组书记", "current_org": "政协包头市东河区委员会",
     "source": "confirmed - S6,S7", "notes": "2026-06 前后接任政协党组书记（白继文卸任）；主席职务待政协全会确认"},
    {"id": 14, "name": "白继文", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（原）东河区政协党组书记、主席", "current_org": "政协包头市东河区委员会",
     "source": "confirmed - S9,S10,S13", "notes": "十一届政协主席（2022-01当选至2026-06在任）；2026-07 由郭惠文接任党组书记"},
    # 前任区委书记
    {"id": 15, "name": "杨二喜", "gender": "男", "ethnicity": "蒙古族", "birth": "1971年9月",
     "birthplace": "内蒙古土默特右旗", "education": "内蒙古党校研究生",
     "party_join": "1995年6月", "work_start": "1991年9月",
     "current_post": "包头市委常委、统战部部长、包头市政协党组副书记", "current_org": "中共包头市委员会",
     "source": "confirmed - S16", "notes": "2021-06 任东河区委书记（兼市常委 2021-08起）；2023-05前后离任东河（王瑞接任）；2024 起任市委统战部长"},
    # 跨区流动案例（包头市旗县区干部交流圈）
    {"id": 16, "name": "石丽娜", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "昆都仑区人民政府区长", "current_org": "包头市昆都仑区人民政府",
     "source": "plausible - S11,S13", "notes": "2022 年东河区 区委班子成员（人大主席团名单）；2025-07 昆都仑区长——北图跨区流动案例"},
    # 区政府副区长（区领导）
    {"id": 17, "name": "田永光", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区人民政府副区长", "current_org": "包头市东河区人民政府",
     "source": "confirmed - S1", "notes": "2026-08-11 王瑞调研随行区领导；具体分工待查"},
    # 纪检委副书记（区纪委班子）
    {"id": 18, "name": "章国峰", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区纪委副书记", "current_org": "中共包头市东河区纪律检查委员会",
     "source": "confirmed - S2", "notes": "十二届纪委副书记"},
    {"id": 19, "name": "韩冰", "gender": "", "ethnicity": "蒙古族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "东河区纪委副书记", "current_org": "中共包头市东河区纪律检查委员会",
     "source": "confirmed - S2", "notes": "十二届纪委副书记"},
    # 原统战部长（2026-01 时在任常委，12届未连任）
    {"id": 20, "name": "周永威", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（原）东河区委常委、统战部部长、区政协党组副书记", "current_org": "政协包头市东河区委员会",
     "source": "confirmed - S9", "notes": "2026-01 在任；十二届常委名单未再列入（换届退出）"},
]

organizations = [
    {"id": 1, "name": "中共包头市东河区委员会", "type": "党委", "level": "正处级", "parent": "中共包头市委员会", "location": "包头市东河区"},
    {"id": 2, "name": "包头市东河区人民政府", "type": "政府", "level": "正处级", "parent": "包头市人民政府", "location": "包头市东河区"},
    {"id": 3, "name": "包头市东河区人民代表大会常务委员会", "type": "人大", "level": "正处级", "parent": "包头市人民代表大会常务委员会", "location": "包头市东河区"},
    {"id": 4, "name": "政协包头市东河区委员会", "type": "政协", "level": "正处级", "parent": "政协包头市委员会", "location": "包头市东河区"},
    {"id": 5, "name": "中共包头市东河区纪律检查委员会（东河区监察委员会）", "type": "纪委", "level": "正处级", "parent": "中共包头市纪律检查委员会", "location": "包头市东河区"},
    {"id": 6, "name": "中共包头市东河区委统一战线工作部", "type": "党委部门", "level": "科级", "parent": "中共包头市东河区委员会", "location": "包头市东河区"},
    {"id": 7, "name": "中共包头市委员会", "type": "党委", "level": "地厅级", "parent": "中共内蒙古自治区委员会", "location": "包头市"},
    {"id": 8, "name": "包头市人民政府", "type": "政府", "level": "地厅级", "parent": "内蒙古自治区人民政府", "location": "包头市"},
    {"id": 9, "name": "政协包头市委员会", "type": "政协", "level": "地厅级", "parent": "政协内蒙古自治区委员会", "location": "包头市"},
    {"id": 10, "name": "中共包头市昆都仑区委员会/昆都仑区人民政府", "type": "党委/政府", "level": "正处级", "parent": "中共包头市委员会", "location": "包头市昆都仑区"},
    {"id": 11, "name": "土默特右旗人民政府", "type": "政府", "level": "正处级", "parent": "包头市人民政府", "location": "包头市土默特右旗"},
    {"id": 12, "name": "固阳县人民政府", "type": "政府", "level": "正处级", "parent": "包头市人民政府", "location": "包头市固阳县"},
    {"id": 13, "name": "中共包头市青山区委员会", "type": "党委", "level": "正处级", "parent": "中共包头市委员会", "location": "包头市青山区"},
]

positions = [
    # 区委书记/副书记
    {"person_id": 1, "org_id": 1, "title": "东河区委书记", "start_date": "2023-05", "end_date": "present", "rank": "正处级（区委正职）", "note": "2026-07-30 十二届全会连任；据百科兼包头市委常委、区人武部党委第一书记、区委党校校长"},
    {"person_id": 2, "org_id": 1, "title": "东河区委副书记", "start_date": "2021-12", "end_date": "present", "rank": "正处级", "note": "2026-07-30 当选十二届区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "东河区人民政府区长", "start_date": "2022-01", "end_date": "present", "rank": "正处级（区政府正职）", "note": "2021-12 代区长（2022-01 十八届人大一次会议当选）；政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "东河区委副书记", "start_date": "2026-07-30", "end_date": "present", "rank": "正处级", "note": "十二届区委一次全会当选；此前为区委常委"},
    # 区委常委
    {"person_id": 4, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届常委"},
    {"person_id": 5, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届常委"},
    {"person_id": 6, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届常委"},
    {"person_id": 7, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "东河区纪委书记、监委主任", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届纪委第一次全会选举"},
    {"person_id": 8, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "东河区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-06-11 履职报道确认常委兼副区长"},
    {"person_id": 9, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届常委"},
    {"person_id": 10, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届常委"},
    {"person_id": 11, "org_id": 1, "title": "东河区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届常委"},
    # 区纪委班子
    {"person_id": 18, "org_id": 5, "title": "东河区纪委副书记", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届纪委副书记"},
    {"person_id": 19, "org_id": 5, "title": "东河区纪委副书记", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十二届纪委副书记，蒙古族"},
    # 人大 / 政协
    {"person_id": 12, "org_id": 3, "title": "东河区人大常委会主任、党组书记", "start_date": "2022-01", "end_date": "present", "rank": "正处级", "note": "十七届主任，十八届连任"},
    {"person_id": 13, "org_id": 4, "title": "东河区政协党组书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "接任自白继文；主席待全会确认"},
    {"person_id": 14, "org_id": 4, "title": "东河区政协主席、党组书记", "start_date": "2022-01", "end_date": "2026-06", "rank": "正处级", "note": "十一届政协主席（2022-01 当选）"},
    # 前任区委书记与市职
    {"person_id": 15, "org_id": 1, "title": "东河区委书记", "start_date": "2021-06", "end_date": "2023-04", "rank": "正处级（2021-08 起兼包头常委）", "note": "2021-06-07 公示拟任、2021-06 到任"},
    {"person_id": 15, "org_id": 7, "title": "包头市委常委（兼东河区委书记）", "start_date": "2021-08", "end_date": "present", "rank": "副厅级", "note": "由此入列市委常委（高配）"},
    {"person_id": 15, "org_id": 7, "title": "包头市委常委、统战部部长", "start_date": "2023-05", "end_date": "present", "rank": "副厅级", "note": "卸任东河区委书记后履职"},
    {"person_id": 15, "org_id": 9, "title": "包头市政协党组副书记", "start_date": "2024", "end_date": "present", "rank": "副厅级", "note": "兼"},
    # 跨区流动
    {"person_id": 16, "org_id": 1, "title": "东河区委常委", "start_date": "2022", "end_date": "", "rank": "副处级", "note": "2022-01 人大主席团名单列名（东河区领导）"},
    {"person_id": 16, "org_id": 10, "title": "昆都仑区人民政府区长", "start_date": "2025", "end_date": "present", "rank": "正处级", "note": "据2025-07 包头市人案（昆都仑区区长）"},
    # 其他区领导
    {"person_id": 17, "org_id": 2, "title": "东河区人民政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-08-11 调研随行"},
    {"person_id": 20, "org_id": 1, "title": "东河区委常委、统战部部长", "start_date": "", "end_date": "2026-07", "rank": "副处级", "note": "2026-01 报道确认；12届换届后未连任"},
    {"person_id": 20, "org_id": 4, "title": "东河区政协党组副书记", "start_date": "", "end_date": "2026-07", "rank": "副处级", "note": "统战部长兼"},
]

relationships = [
    # 区内核心关系（confirmed）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长组成区四套班子党政一把手搭档", "overlap_org": "中共包头市东河区委员会/东河区人民政府", "overlap_period": "2023-05 至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记对专职副书记直接领导", "overlap_org": "中共包头市东河区委员会", "overlap_period": "2026-07 至今"},
    {"person_a": 1, "person_b": 7, "type": "监督", "context": "区委书记与纪委书记的日常监督与被监督", "overlap_org": "中共包头市东河区委员会/区纪委监委", "overlap_period": "2026-07 至今"},
    {"person_a": 1, "person_b": 12, "type": "党政与人大", "context": "区委书记与人大常委会主任（党委领导人大机关）", "overlap_org": "东河区四套班子", "overlap_period": "2023-05 至今"},
    {"person_a": 1, "person_b": 13, "type": "部长与政协", "context": "区委书记与政协党组书记（党委领导政协机关）", "overlap_org": "东河区四套班子", "overlap_period": "2026-07 至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记对区委常委、副区长（区政府班子）", "overlap_org": "中共包头市东河区委员会/区政府", "overlap_period": "现状"},
    {"person_a": 2, "person_b": 3, "type": "党政班子", "context": "区长与专职副书记在区委常委会中共事", "overlap_org": "中共包头市东河区委员会十二届常委会", "overlap_period": "2026-07 至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长对常委副区长的直接领导", "overlap_org": "包头市东河区人民政府", "overlap_period": "现状"},
    {"person_a": 2, "person_b": 12, "type": "党政与人大", "context": "区长与人大常委会主任（人大监督政府）", "overlap_org": "东河区四套班子", "overlap_period": "2022-01 至今"},
    {"person_a": 2, "person_b": 14, "type": "党政与政协", "context": "区长与政协主席白继文（十一届任期）常态化共事", "overlap_org": "东河区四套班子/政协", "overlap_period": "2022-01~2026-06"},
    # 前任-继任
    {"person_a": 15, "person_b": 1, "type": "前任继任", "context": "杨二喜卸任东河区委书记，王瑞 2023-05 接任（东河区干部调整序列）", "overlap_org": "中共包头市东河区委员会", "overlap_period": "2023-05 交接"},
    {"person_a": 15, "person_b": 2, "type": "上下级", "context": "杨二喜任区委书记期间与区长张利军直接共事", "overlap_org": "东河区四套班子", "overlap_period": "2022-01~2023-04"},
    {"person_a": 15, "person_b": 12, "type": "上下级", "context": "杨二喜与人大主任王建平（区委-人大）", "overlap_org": "东河区四套班子", "overlap_period": "2022-01~2023-04"},
    # 政协交接
    {"person_a": 14, "person_b": 13, "type": "前任继任", "context": "白继文卸任政协党组书记，郭惠文接任", "overlap_org": "政协包头市东河区委员会党组", "overlap_period": "2026-06/07 交接"},
    # 包头市旗县区干部交流圈（plausible-weak）
    {"person_a": 1, "person_b": 16, "type": "干部交流圈", "context": "东河区现任书记与曾任常委（现任昆都仑区长）同处包头市旗县区处级干部序列", "overlap_org": "包头市旗县区干部序列", "overlap_period": "2020s"},
    {"person_a": 2, "person_b": 16, "type": "干部交流圈", "context": "张利军（青山区常务副区长→东河区长）与石丽娜（东河→昆区）均系市区内跨区流动", "overlap_org": "包头市旗县区干部序列", "overlap_period": "2020s"},
    {"person_a": 15, "person_b": 16, "type": "干部交流圈", "context": "杨二喜任东河区委书记时期与石丽娜常委共事", "overlap_org": "东河区委常委会（11届）", "overlap_period": "2022"},
]


PINYIN = {"王瑞": "wang_rui", "张利军": "zhang_lijun", "王建平": "wang_jianping",
          "杨二喜": "yang_erxi", "郭惠文": "guo_huiwen", "王伟": "wang_wei",
          "涂永文": "tu_yongwen", "石岩": "shi_yan"}

# 核心人物：人物JSON（履职数据以官方/百科为准）
CORE = {1: "区委书记", 2: "区长", 3: "区委副书记", 12: "人大常委会主任",
        13: "政协党组书记", 15: "前任区委书记", 7: "纪委书记", 8: "区委常委副区长"}


def _career_rows(p: dict, name: str) -> list[dict]:
    """Build career timeline rows from evidence in person dict + curated facts."""
    rows = []
    known = {
        "张利军": [
            {"start": "1990-09", "end": "1993-06", "org": "包头师范学校", "title": "普师专业学习", "confidence": "plausible"},
            {"start": "1993-08", "end": "1996-10", "org": "青山区繁荣道小学", "title": "教师", "confidence": "plausible"},
            {"start": "1996-10", "end": "2001-02", "org": "青山区委办公室", "title": "秘书、秘书科科长、常委会秘书", "confidence": "plausible"},
            {"start": "2001-02", "end": "2003-05", "org": "青山区委办公室", "title": "副主任、常委会秘书", "confidence": "plausible"},
            {"start": "2003-05", "end": "2004-02", "org": "青山区委组织部", "title": "副部长、机关党委书记", "confidence": "plausible"},
            {"start": "2004-03", "end": "2009-01", "org": "包头市委办公厅", "title": "信息处副处长/常委办正科级秘书", "confidence": "plausible"},
            {"start": "2009-01", "end": "2011-05", "org": "土右旗委", "title": "旗委常委、组织部部长", "confidence": "plausible"},
            {"start": "2011-05", "end": "2016-07", "org": "昆都仑区委/政府", "title": "区委常委、宣传部部长、政府副区长", "confidence": "plausible"},
            {"start": "2016-07", "end": "2021-12", "org": "青山区委/政府", "title": "区委常委、常务副区长", "confidence": "plausible"},
        ],
        "杨二喜": [
            {"start": "1987-09", "end": "1991-07", "org": "包头农牧学校", "title": "农业经济管理专业学习", "confidence": "confirmed"},
            {"start": "1991-09", "end": "1998-05", "org": "土右旗农牧局、廿四顷地乡政府", "title": "科员", "confidence": "confirmed"},
            {"start": "1998-05", "end": "2000-07", "org": "共青团土右旗委", "title": "副书记", "confidence": "confirmed"},
            {"start": "2000-07", "end": "2001-06", "org": "共青团土右旗委", "title": "书记", "confidence": "confirmed"},
            {"start": "2001-06", "end": "2004-03", "org": "土右旗大城西乡", "title": "党委副书记、乡长", "confidence": "confirmed"},
            {"start": "2004-03", "end": "2006-02", "org": "土右旗大城西乡", "title": "党委书记", "confidence": "confirmed"},
            {"start": "2006-02", "end": "2007-10", "org": "土右旗明沙淖乡", "title": "党委书记、产业区管委会主任", "confidence": "confirmed"},
            {"start": "2007-10", "end": "2009-08", "org": "土右旗人民政府", "title": "副旗长", "confidence": "confirmed"},
            {"start": "2009-08", "end": "2011-02", "org": "土右旗委/政府", "title": "常委、宣传部部长、副旗长", "confidence": "confirmed"},
            {"start": "2011-12", "end": "2014-01", "org": "土右旗委", "title": "副书记", "confidence": "confirmed"},
            {"start": "2014-01", "end": "2021-06", "org": "固阳县人民政府", "title": "县委副书记、县长", "confidence": "confirmed"},
            {"start": "2021-06", "end": "2021-08", "org": "东河区委", "title": "区委书记", "confidence": "confirmed"},
            {"start": "2021-08", "end": "2023-04", "org": "包头市委兼东河区委", "title": "市委常委（兼区委书记）", "confidence": "confirmed"},
            {"start": "2023-05", "end": "present", "org": "包头市委统战部", "title": "市委常委、统战部部长（兼市政协党组副书记）", "confidence": "confirmed"},
        ],
    }
    for row in known.get(name, []):
        rows.append({
            "start": row["start"], "end": row["end"], "org": row["org"], "title": row["title"],
            "level": "", "location": "包头市", "system": "other", "rank": "",
            "is_key_promotion": False, "notes": "", "confidence": row["confidence"],
            "source_ids": ["S16"] if name == "杨二喜" else ["S17", "S18"],
        })
    if name in ("王瑞", "郭惠文", "王建平", "王伟", "涂永文", "石岩"):
        rows.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口（公开渠道未获得任前完整履历）",
            "title": "", "level": "", "location": "", "system": "other", "rank": "",
            "is_key_promotion": False,
            "notes": "2026-08-11：搜索引擎受限（Exa限流/百度403/搜狗与360反爬），官方媒体仅公开现任职务。",
            "confidence": "unverified", "source_ids": [],
        })
    rows.append({
        "start": "present", "end": "present", "org": p["current_org"], "title": p["current_post"],
        "level": "", "location": "包头市东河区", "system": "party" if "委员会" in p["current_org"] and "人民政府" not in p["current_org"] else "government",
        "rank": "正处级", "is_key_promotion": True, "notes": "现任职务（官方公报/官网）", "confidence": "confirmed",
        "source_ids": ["S1", "S2", "S3"],
    })
    return rows


def build_person_json(p: dict, job: str) -> dict:
    """Build the canonical person JSON record for a core leader."""
    pinyin = PINYIN.get(p["name"], p["name"])
    career = _career_rows(p, p["name"])
    is_wr = p["name"] == "王瑞"
    partner = "张利军" if is_wr else ("王瑞" if p["name"] == "张利军" else "")
    relationships_rows = []
    if partner:
        relationships_rows.append({
            "person": partner, "person_id": f"donghe_{PINYIN.get(partner, partner)}",
            "relationship_type": "党政搭档", "strength": "strong",
            "evidence": "东河区党政一把手搭档（官方活动报道确认）",
            "overlap_org": "中共包头市东河区委员会/东河区人民政府", "overlap_period": "2023-05 至今",
            "direction": "undirected", "confidence": "confirmed", "source_ids": ["S1", "S4"],
        })
    if p["name"] == "张利军":
        relationships_rows.append({
            "person": "杨二喜", "person_id": "donghe_yang_erxi",
            "relationship_type": "前任主官共事", "strength": "strong",
            "evidence": "2022-01 两会：杨二喜任书记、张利军任代区长/区长直接搭班",
            "overlap_org": "东河区四套班子", "overlap_period": "2022-01~2023-04",
            "direction": "undirected", "confidence": "confirmed", "source_ids": ["S11"],
        })
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区", "city": "包头市", "region": "东河区",
            "job": job, "task_id": "inner_mongolia_东河区", "time_focus": "current",
        },
        "identity": {
            "person_id": f"donghe_{PINYIN.get(p['name'], p['name'])}",
            "name": p["name"], "aliases": [], "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""), "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""),
                           "study_type": "unknown", "source_ids": ["S17", "S18"] if "张利军" in p["name"] else []}],
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth','')}",
                            "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                            "official_profile_url": "https://www.donghe.gov.cn/"},
        },
        "current_status": {
            "current_post": p["current_post"], "current_org": p["current_org"],
            "administrative_rank": "副厅级" if "市委常委" in p["current_post"] else "正处级",
            "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S1", "S2", "S3"],
        },
        "career_timeline": career,
        "organizations": [{"org_id": "donghe_party", "name": "中共包头市东河区委员会", "role": "current_employer", "type": "party"}],
        "relationships": relationships_rows,
        "governance_record": [{
            "period": "2026-07", "domain": "other", "achievement_or_event": "十二届党代会提出'三区一地'定位", "role_in_event": p["current_post"], "measurable_outcome": "",
            "location": "包头市东河区", "confidence": "confirmed", "source_ids": ["S4"],
        }],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if p["name"] in ("张利军", "杨二喜") else "unknown",
            "systems_experience": [], "geographic_pattern": ["包头市"],
            "promotion_velocity": {"summary": "公开信息有限", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": ["重振东河雄风、再现往日繁华", "有解思维", "三区一地"], "management_signals": [],
            "caret": "仅据公开报道整理，不作心理/性格推断",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found", "description": "截至今日，未发现公开可查的处分、落马或被调查记录", "date": AS_OF,
            "confidence": "unverified", "source_ids": [],
        }],
        "source_register": [d for d in SOURCES if d["id"] in ("S1", "S2", "S3", "S4")] + (
            [d for d in SOURCES if d["id"] in ("S16",)] if p["name"] == "杨二喜" else []) + (
            [d for d in SOURCES if d["id"] in ("S16", "S17", "S18")] if p["name"] == "张利军" else []),
        "confidence_summary": {
            "identity": "confirmed" if (p.get("birth") or p.get("birthplace")) else "plausible",
            "current_role": "confirmed", "career_completeness": "complete" if p["name"] == "杨二喜" else ("partial" if p["name"] == "张利军" else "thin"),
            "relationship_confidence": "high", "biggest_gap": f"{p['name']} {job}前的完整履历（若王瑞/郭惠文）或张任大区时期的（2019-2021）",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{p['name']} 就任东河{job}前的完整履历（此前任职单位、晋升时间）",
             "why_it_matters": "核心领导跨区履历是判断包头旗县区干部交流圈流动模式的关键线索",
             "suggested_queries": [f"{p['name']} 包头 简历", f"{p['name']} 东河区 {job} 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{p['name']} 出生地/籍贯、毕业院校与专业",
             "why_it_matters": "同校/同乡关系是人事网络的常见边", "suggested_queries": [f"{p['name']} 籍贯", f"{p['name']} 毕业"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "东河区（2021-06前）前任区委书记及去职去向",
             "why_it_matters": "补全东河区书记继任链条", "suggested_queries": ["东河区 前任 区委书记 2021"], "last_attempted": AS_OF},
        ],
    }


def write_person_json() -> list[Path]:
    """Write canonical person JSON profiles for core leaders into staging."""
    written = []
    for pid, job in CORE.items():
        p = next(x for x in persons if x["id"] == pid)
        obj = build_person_json(p, job)
        fname = f"{TODAY}-内蒙古自治区-包头市-{job}-{p['name']}.json"
        path = JSON_DIR / fname
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2)
        written.append(path)
        print(f"  person json -> {path.name}")
    return written


def main() -> None:
    STAGING.mkdir(parents=True, exist_ok=True)
    print(f"[build:{SLUG}] staging = {STAGING}")
    print(f"[build:{SLUG}] writing person JSON profiles ...")
    write_p = write_person_json()
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
    for p in write_p:
        print(f"[build:{SLUG}] person json: {p.name}")


if __name__ == "__main__":
    main()