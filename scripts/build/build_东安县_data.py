#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东安县 (Dong'an County), 永州市, 湖南省.

Task ID: hunan_东安县
Level: 县
Targets: 县委书记 & 县长
Investigation date: 2026-08-11

Key findings (verified 2026-08-11):
- 现任县委书记: 蒋华 (2026-06-29 由县长升任; 此前 2016-08~2021-07 任常务副县长, 2021-07~2026-06 任县长; 2026-07-29 十四届县委换届连任书记)
- 现任代理县长: 洪海侠 (2026-06-18 任前公示原任株洲高新区党工委委员/株洲市天元区委常委/副区长, 跨地市调入; 2026-06-29 任县委副书记, 2026-07 县人大常委会决定代理县长)
- 前任县委书记: 唐何 (2021-07~2026-06, 另有任用, 去向未公开)
- 书记序列: 谢景林(2011.02-2016.08)→冯德校(2016.08-2021.07)→唐何(2021.07-2026.06)→蒋华(2026.06-)
- 县长序列: 谢景林(2007-2011)→陈宇荣(2011-2015.09)→龙向洋(2016.07-2021.07)→蒋华(2021.07-2026.06)→洪海侠(代理,2026.07-)
- 县域干部上行: 谢景林→永州市副市长(2017)/市政协主席(2022); 冯德校→永州市人大常委会副主任; 龙向洋→永州市人大常委会副主任(2026-07-28)
- 风险信号: 2017-12 新华社报道永州市委组织部通报东安县选拔任用程序问题(两名干部任命被取消), 时任县委书记冯德校被批评教育

Evidence: 东安县人民政府门户网站 (da.gov.cn 政府领导页/东安要闻/党代会新闻), 红网永州站 (任前公示/人事任免), 华声在线(永组在线), 360百科/快懂百科, 新华网, 维基百科东安县条目.
"""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
# Allow the script to also run from a data/tmp/<task> staging copy.
if not (REPO_ROOT / "scripts").exists():
    REPO_ROOT = Path(__file__).resolve().parents[2]

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "东安县"
TODAY = datetime.now().strftime("%Y%m%d")  # 20260811
AS_OF = "2026-08-11"

# ── Output paths (promotion to province dirs is done by scripts/process_tmp.py) ─
STAGING = REPO_ROOT / "data" / "tmp" / "hunan_东安县"
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
JSON_DIR = STAGING

# ══════════════════════════════════════════════════════════════════════════
# SOURCES
# ══════════════════════════════════════════════════════════════════════════
SOURCES = [
    {"id": "S001", "title": "东安县人民政府网: 县政府领导页(领导之窗)", "url": "http://www.da.gov.cn/da/xwld/leaderIndex3.shtml", "publisher": "东安县人民政府", "published_at": "", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "现任县政府班子共9人: 洪海侠(代理县长)、成宇、唐久梅、秦琦、周文、周志成、杨伟燕、宋志勇、周禄雄; 含各单位简历简介"},
    {"id": "S002", "title": "华声在线/永州组在线: 蒋华同志任中共东安县委书记(2026-06-29干部会议)", "url": "https://hunan.voc.com.cn/news/202606/33026245.html", "publisher": "永组在线", "published_at": "2026-06-29", "accessed_at": "2026-08-11", "source_type": "appointment_notice", "reliability": "high", "notes": "宣布蒋华任县委书记; 唐何另有任用; 洪海侠任县委委员、常委、副书记"},
    {"id": "S003", "title": "红网永州: 永州市委管理干部任前公示公告(2026-06-18)", "url": "https://yz.rednet.cn/content/646040/52/16015305.html", "published_at": "2026-06-18", "accessed_at": "2026-08-11", "publisher": "永组在线", "source_type": "appointment_notice", "reliability": "high", "notes": "洪海侠, 1987-04生, 湖南娄底人, 研究生/工学硕士, 现任株洲高新区党工委委员、天元区委常委、副区长, 拟提名为县市区人民政府正职人选"},
    {"id": "S004", "title": "东安县人民政府网: 中国共产党东安县第十四届委员会第一次全体会议(2026-07-29)", "url": "http://da.gov.cn/da/dayw/202607/fc3072e8df9340fcaad3db5427b22f07.shtml", "published_at": "2026-07-29", "accessed_at": "2026-08-11", "publisher": "东安县人民政府", "source_type": "official", "reliability": "high", "notes": "选举第14届县委常委会: 蒋华、洪海侠、李月红、唐亚辉、成宇、秦波、周丽、杨加勉、唐琳玮、周志成、周禄雄; 书记蒋华, 副书记洪海侠、李月红"},
    {"id": "S005", "title": "东安县人民政府网: 东安县第十四届纪律检查委员会全会(2026-07-29)", "url": "http://da.gov.cn/da/dayw/202607/ec155a72e5ff4a029feedcef0fdfd17a.shtml", "published_at": "2026-07-29", "accessed_at": "2026-08-11", "publisher": "东安县人民政府", "source_type": "official", "reliability": "high", "notes": "新一届县纪委全会: 唐琳玮主持并担任县纪委书记"},
    {"id": "S006", "title": "红网: 人事丨唐何同志任中共东安县委书记(2021-07-05)", "url": "https://hn.rednet.cn/content/2021/07/05/9625112.html", "published_at": "2021-07-05", "accessed_at": "2026-08-11", "publisher": "红网(东安发布)", "source_type": "media", "reliability": "high", "notes": "唐何任县委书记; 冯德校卸任另有任用; 龙向洋卸任县长另有任用"},
    {"id": "S007", "title": "红网: 蒋华任中共东安县委副书记、提名为东安县人民政府县长候选人(2021-07-12)", "url": "https://yz.rednet.cn/content/2021/07/12/9653345.html", "published_at": "2021-07-12", "accessed_at": "2026-08-11", "publisher": "红网(东安发布)", "source_type": "media", "reliability": "high", "notes": "蒋华由常务副县长任县委副书记、提名县长候选人"},
    {"id": "S008", "title": "红网专题: 冯德校任东安县委书记 龙向洋提名为县长候选人(2016-08-02)", "url": "http://zt.rednet.cn/c/2016/08/02/4050501.htm", "published_at": "2016-08-02", "accessed_at": "2026-08-11", "publisher": "红网永州", "source_type": "media", "reliability": "high", "notes": "冯德校任县委书记; 龙向洋任副书记、提名县长; 谢景林卸任东安县委书记"},
    {"id": "S009", "title": "360百科: 唐何", "url": "https://baike.so.com/doc/24325504-25130655.html", "publisher": "360百科", "published_at": "", "accessed_at": "2026-08-11", "source_type": "encyclopedia", "reliability": "medium", "notes": "唐何完整履历(1995-2021), 2021年8月当选东安县十三届书记"},
    {"id": "S010", "title": "360百科: 冯德校(现永州市人大常委会副主任)", "url": "https://baike.so.com/doc/3406358-3585382.html", "publisher": "360百科", "published_at": "2017-09-07", "accessed_at": "2026-08-11", "source_type": "encyclopedia", "reliability": "medium", "notes": "冯德校完整履历(1983-2016); 另快懂百科显示其现任永州市人大常委会副主任"},
    {"id": "S011", "title": "快懂百科: 谢景林", "url": "https://www.baike.com/wiki/谢景林", "publisher": "快懂百科", "published_at": "", "accessed_at": "2026-08-11", "source_type": "encyclopedia", "reliability": "medium", "notes": "谢景林完整履历: 江华→冷水滩→东安(2007-2016)→永州市副市长(2017)→市政协主席(2022)"},
    {"id": "S012", "title": "东安县人民政府(门户镜像): 蒋华简历(任常务副县长时期)", "url": "http://qstai.com/html/Item8059.aspx.html", "publisher": "东安县电子政务办镜像", "published_at": "", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "medium", "notes": "蒋华2000-2016完整履历(道县→新田婷→东安)"},
    {"id": "S013", "title": "东安县人民政府网: 张波主持召开县第十八届人大常委会第四十四次会议(2026-07-23)", "url": "http://da.gov.cn/da/dayw/202607/6e6e1312300d4c9e83c58c730faae18d.shtml", "published_at": "2026-07-23", "accessed_at": "2026-08-11", "publisher": "东安县人民政府", "source_type": "official", "reliability": "high", "notes": "人大常委会主任张波主持会议"},
    {"id": "S014", "title": "东安县人民政府网: 蒋华、洪海侠带队走访慰问驻东部队(2026-07-30)", "url": "http://da.gov.cn/da/dayw/202607/0d364d3151d4434bb2f62f5965098a35.shtml", "published_at": "2026-07-30", "accessed_at": "2026-08-11", "publisher": "东安县人民政府/东华发布", "source_type": "official", "reliability": "high", "notes": "蒋华(县委书记)、洪海侠(代理县长)共同活动; 参会县领导李月红、张波、李劲晟、成宇、秦波、杨加勉、周继成"},
    {"id": "S015", "title": "永州政府网: 洪海侠调查东安大市场提质改造(2026-08-04)", "url": "http://www.da.gov.cn/da/dayw/202608/b4667c98f79240ccab421c3f6390c0c5.shtml", "published_at": "2026-08-04", "accessed_at": "2026-08-11", "publisher": "永州市人民政府门户(县区传真)", "source_type": "official", "reliability": "high", "notes": "东安县委副书记、代理县长洪海侠活动记录"},
    {"id": "S016", "title": "新华网: 湖南东安否认'带病提拔'干部经调查复核后被取消任命(2017-12-25)", "url": "https://www.xinhuanet.com/politics/2017-12/25/c_1122165133.htm", "published_at": "2017-12-25", "accessed_at": "2026-08-11", "publisher": "新华社", "source_type": "media", "reliability": "high", "notes": "东安县选拔干部程序问题: 取消周建霞/宋雨薇任命; 县委书记冯德校被批评教育, 组织部长彭俊卿被诫勉"},
    {"id": "S017", "title": "东安县人民政府网: 蒋华主持召开2026年第7次县委常委会(延长会)会议(2026-07-30)", "url": "http://da.gov.cn/da/dayw/202607/cae6364cbff148888727418ab705174c.shtml", "published_at": "2026-07-30", "accessed_at": "2026-08-11", "publisher": "东安县人民政府", "source_type": "official", "reliability": "high", "notes": "蒋华书记: 教育(东安一中/耀祥中学/职业中专), 安全生产, 医疗卫生综合改革, 链式招商等议题"},
    {"id": "S018", "title": "维基百科: 东安县人民政府(含历任县长表)", "url": "https://zh.wikipedia.org/wiki/%E4%B8%9C%E5%AE%89%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C", "publisher": "维基百科", "published_at": "", "accessed_at": "2026-08-11", "source_type": "encyclopedia", "reliability": "medium", "notes": "历任县长: 曾能德2001.10-2006.12, 谢景林2003-2011.02, 陈宇荣2011.02-2015.09, 赵向阳2016.07-2021.07, 蒋华2021.07-"},
    {"id": "S019", "title": "各人物2026-06 唐何主持召开2026年第7次会议/县委常委会记录", "url": "https://yz.rednet.cn/content/646940/61/15081244.html", "publisher": "红网", "published_at": "2026-06-27", "accessed_at": "2026-08-11", "source_type": "media", "reliability": "high", "notes": "唐何(书记)2026-06会议记录及县委领导班子名单(唐何、蒋华、李月红、张波、李劲涛、唐久梅、唐青松、成宇、黄敏、秦波等)"},
    {"id": "S020", "title": "永州市 2026-08人大会议: 龙向洋当选永州市人大常委会副主任", "url": "https://www.yzcity.gov.cn/", "publisher": "永州日报", "published_at": "2026-07-28", "accessed_at": "2026-08-11", "source_type": "media", "reliability": "high", "notes": "2026-07-28会议选举龙向洋(原东安县长)为永州市人大常委会副主任"},
]

# ══════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════
persons = [
    # ── 1. 现任县委书记 ──
    {
        "id": 1, "name": "蒋华", "gender": "男", "ethnicity": "瑶族",
        "birth": "1980-10", "birthplace": "湖南省永州市道县", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "2000-07",
        "current_post": "中共东安县委书记", "current_org": "中共东安县委员会",
        "source": "S001 S002 S007 S012 S014",
        "profile_notes": "1980年10月生, 湖南道县人, 瑶族, 中共党员, 在职研究生学历. 2000年起在道县乡镇/县直机关工作(横岭瑶族乡/梅花镇党委书记, 月岩森林公园管理局党委书记等), 2012年9月任道县人民政府副县长, 2015年4月任新田县委常委、县委办主任(同期挂任东莞市农业农村局副局长), 2016年8月交流至东安县任县委常委、常务副县长, 2021年7月任县委副书记、县长, 2026年6月29日任县委书记(2026-07 十四届县委换届后连任). 履历覆盖: 瑶族乡基层、森林保护管理、县级政府、新田/东安两县. 2026-07-16兼任东安县人武部党委第一书记; 已获县委书记任命的国防责任.",
        "career": [
            {"start": "2000-07", "end": "2004-02", "org": "道县洪塘营瑶族乡人民政府", "title": "洪塘营瑶族乡团乡委书记", "level": "乡科级", "system": "government", "rank": "副科级", "is_key_promotion": False, "notes": "从道县基层起步", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2004-02", "end": "2004-10", "org": "共青团道县委员会", "title": "团县委书记办公室主任", "level": "乡科级", "rank": "股级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2004-10", "end": "2005-11", "org": "道县对外贸易经济合作局", "title": "副局长", "level": "乡科级", "rank": "副科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2005-11", "end": "2006-02", "org": "道县商务局", "title": "党组成员、副局长", "level": "乡科级", "rank": "副科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2006-02", "end": "2010-02", "org": "中共道县横岭瑶族乡党委", "title": "横岭瑶族乡党委书记", "level": "乡科级", "rank": "正科级", "is_key_promotion": True, "notes": "瑶族乡党委书记——少数民族干部基层历练", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2010-02", "end": "2010-09", "org": "中共道县梅花镇党委", "title": "梅花镇党委书记", "level": "乡科级", "rank": "正科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2010-09", "end": "2012-09", "org": "月岩国家森林公园管理局", "title": "管理局党委书记兼月岩林场党委书记、都庞岭国家级自然保护区道县分局局长", "level": "乡科级", "rank": "正科级(待遇副处?)", "is_key_promotion": True, "notes": "生态保护系统管理经验", "confidence": "plausible", "source_ids": ["S012"]},
            {"start": "2012-09", "end": "2015-04", "org": "道县人民政府", "title": "副县长", "level": "县处级", "rank": "副处级", "is_key_promotion": True, "notes": "道县副县长——进入县级班子", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2015-04", "end": "2016-08", "org": "中共新田县委员会", "title": "新田县委常委、县委办公室主任", "level": "县处级", "rank": "副处级", "is_key_promotion": True, "notes": "跨县交流至新田县; 期间2015.03-2016.01挂任广东省东莞市农业农村局副局长——跨省交流", "confidence": "confirmed", "source_ids": ["S012"]},
            {"start": "2016-08", "end": "2021-07", "org": "东安县人民政府", "title": "东安县委常委、常务副县长", "level": "县处级", "rank": "副处级", "is_key_promotion": True, "notes": "调入东安县主持县政府常务, 后转任县长", "confidence": "confirmed", "source_ids": ["S012", "S007"]},
            {"start": "2021-07", "end": "2026-06", "org": "东安县人民政府", "title": "县委副书记、县长", "level": "县处级", "rank": "正处级", "is_key_promotion": True, "notes": "2021-07-12提名县长候选人, 后当选", "confidence": "confirmed", "source_ids": ["S007", "S002"]},
            {"start": "2026-06-29", "end": "present", "org": "中共东安县委员会", "title": "县委书记", "level": "县处级", "rank": "正处级", "is_key_promotion": True, "notes": "2026-06-29干部大会宣布任县委书记; 2026-07-29十四届县委换届后连任书记; 2026-07-16任县人武部党委第一书记", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        ],
        "governance": [
            {"period": "2026-07", "domain": "education", "achievement_or_event": "常委会部署教育优先: 东安一中提质、耀祥中学市县帮扶改革、县职业中专综合试点高中建设、初中教育整体提质", "role_in_event": "主持县委会", "measurable_outcome": "", "location": "东安县", "confidence": "confirmed", "source_ids": ["S017"]},
            {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "提出'三高四新'蓝图下推进链式招商、以商招商、'企业服务年'行动, 扩大'三个园区'建设", "role_in_event": "主持县委常委会", "location": "东安县", "confidence": "confirmed", "source_ids": ["S017"]},
            {"period": "2026-07", "domain": "health", "achievement_or_event": "部署县级一体化医疗卫生服务体系, 卫生健康人才队伍改革", "role_in_event": "主持", "location": "东安县", "confidence": "confirmed", "source_ids": ["S017"]},
        ],
        "work_style": [
            {"trait": "grassroots_oriented", "evidence": "2000-2012年12年基层经历: 乡镇团干/党委书记, 再至县级班子——基层履历完整", "confidence": "confirmed", "source_ids": ["S012"]},
            {"trait": "pragmatic", "evidence": "调度议题集中于教育、安全、产业、医疗等具体民生发展事项", "confidence": "plausible", "source_ids": ["S017"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "local_ladder|cross_county_rotation", "systems": ["government", "party"], "geo": ["道县", "新田", "东安", "东莞(挂职)"]},
    },
    # ── 2. 现任代理县长 ──
    {
        "id": 2, "name": "洪海侠", "gender": "男", "ethnicity": "汉族",
        "birth": "1987-04", "birthplace": "湖南娄底", "education": "研究生(工学硕士)",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县人民政府代理县长", "current_org": "东安县人民政府",
        "source": "S001 S003 S002 S015",
        "profile_notes": "1987年4月生, 湖南娄底人, 中共党员, 研究生学历、工学硕士. 原任株洲高新技术产业开发区党工委委员、株洲市天元区委常委、副区长. 2026-06-18 永州市委组织部任前公示(拟提名为县市区人民政府正职人选), 2026-06-29 任中共东安县委委员、常委、副书记, 2026-07 由县人大常委会决定任代理县长. 跨地市(株洲→永州)调入的年轻县长人选; 其株洲任职前的履历尚未公开(缺口).",
        "career": [
            {"start": "unknown", "end": "2026-06", "org": "株洲高新技术产业开发区", "title": "党工委委员", "level": "县处级", "rank": "", "is_key_promotion": False, "notes": "任前公示显示其原任; 具体任职起始时间待核", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "unknown", "end": "2026-06", "org": "天元区人民政府", "title": "天元区委常委、副区长", "level": "县处级", "rank": "副处级", "is_key_promotion": False, "notes": "株洲市天元区(株洲高新区同城区)职务; 任职时段待核", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "2026-06-29", "end": "2026-07", "org": "中共东安县委员会", "title": "县委副书记", "level": "县处级", "rank": "副处级", "is_key_promotion": True, "notes": "2026-06-29干部会议宣布任县委副书记, 提名为县长候选人", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "2026-07", "end": "present", "org": "东安县人民政府", "title": "县委副书记、代理县长", "level": "县处级", "rank": "正处级", "is_key_promotion": True, "notes": "2026-07 县人大常委会决定代理县长(具体日待核); 主持县政府全面工作(截至2026-08官方领导页)", "confidence": "confirmed", "source_ids": ["S001", "S015"]},
        ],
        "governance": [
            {"period": "2026-08", "domain": "urban_construction", "achievement_or_event": "调研东安大市场提质改造项目(商贸基础设施)", "role_in_event": "代理县长主持", "location": "东安县", "confidence": "confirmed", "source_ids": ["S015"]},
        ],
        "work_style": [
            {"trait": "technocratic", "evidence": "工学硕士、开发区/天元区复合履历——产业发展导向的技术型干部", "confidence": "plausible", "source_ids": ["S003"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "cross_county_rotation|development_zone", "systems": ["government", "development_zone"], "geo": ["娄底", "株洲", "永州"]},
    },
    # ── 3. 前任县委书记 (2021-2026) ──
    {
        "id": 3, "name": "唐何", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-10", "birthplace": "湖南岳阳华容县", "education": "研究生学历(湖南大学在职硕士)",
        "party_join": "1999-06", "work_start": "1999-07",
        "current_post": "前任东安县委书记(另有任用,去向2026-08待核)", "current_org": "中共东安县委员会(前)",
        "source": "S006 S009 S019",
        "profile_notes": "1977年10月生, 湖南华容县人, 1999年7月参加工作, 1999年6月加入中国共产党, 研究生学历. 湖南财政学院会计专业本科, 湖南大学在职硕士. 1999-2016年省直机关系统(省药品监督管理局/食品药品监督管理局人事教育、培训、检验检疫)近17年, 2015年3月挂任衡山县副县长, 2016年8月转地方任宁远县委副书记、县长, 2021年7月任东安县委书记, 2025年晋升二级巡视员. 2026年6月29日卸任县委书记'另有任用'(新去向截至2026-08-11未公开).",
        "career": [
            {"start": "1995-09", "end": "1999-07", "org": "湖南大学(原湖南财经学院)", "title": "财会系会计学专业学生", "level": "", "rank": "", "is_key_promotion": False, "notes": "湖南财经学院财会系会计专业", "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "1999-07", "end": "2000-02", "org": "湖南省三湘客车集团公司", "title": "干部", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "plausible", "source_ids": ["S009"]},
            {"start": "2000-02", "end": "2001-08", "org": "湖南省机关事务管理局", "title": "科员", "level": "厅局级机关", "system": "government", "rank": "科员", "is_key_promotion": False, "notes": "", "confidence": "plausible", "source_ids": ["S009"]},
            {"start": "2001-08", "end": "2003-08", "org": "湖南省食品药品监督管理局", "title": "科员(药品监管)", "level": "厅局级机关", "system": "government", "rank": "科员", "is_key_promotion": False, "notes": "药监系统起步", "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "2003-08", "end": "2013-02", "org": "湖南省食品药品监督管理局", "title": "副主任科员/主任科员/培训中心主任、人事教育处副处长", "level": "厅局级机关", "system": "government", "rank": "副处级(2010)", "is_key_promotion": True, "notes": "2006-08任人事教育处主任科员; 2008-11培训中心主任(副处); 2010-10人事教育处副处长、培训中心主任", "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "2013-02", "end": "2014-12", "org": "湖南省食品药品检验研究院", "title": "党委书记、院长", "level": "处级事业单位", "system": "other", "rank": "正处级", "is_key_promotion": True, "notes": "省食药检院主持", "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "2014-12", "end": "2015-03", "org": "湖南省食品药品监督管理局", "title": "稽查总队稽查专员", "level": "厅局级机关", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "稽查专员——从院领导回机关", "confidence": "plausible", "source_ids": ["S009"]},
            {"start": "2015-03", "end": "2016-08", "org": "衡山县人民政府", "title": "衡山县委常委、副县长(挂职)", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "省直系统下挂衡山(衡阳市)", "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "2016-08", "end": "2016-11", "org": "中共宁远县委员会", "title": "县委副书记、代县长", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2016年8月到任宁远", "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "2016-11", "end": "2021-07", "org": "宁远县人民政府", "title": "县委副书记、县长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2016年11月当选宁远县长", "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "2021-07", "end": "2026-06", "org": "中共东安县委员会", "title": "县委书记", "level": "县处级", "system": "party", "rank": "正处级(2025年二级巡视员)", "is_key_promotion": True, "notes": "2021-07-05任; 2021-08当选东安县十三届县委书记; 2025年5月报道为'县委书记、二级巡视员'", "confidence": "confirmed", "source_ids": ["S006", "S009"]},
            {"start": "2026-06-29", "end": "unknown", "org": "中共东安县委员会", "title": "卸任后'另有任用'(去向待核)", "level": "", "system": "party", "rank": "", "is_key_promotion": False, "notes": "2026-06-29干部大会: 不再担任东安县委书记, 另有任用; 新职务未公开(截至2026-08-11)", "confidence": "confirmed", "source_ids": ["S002", "S019"]},
        ],
        "governance": [
            {"period": "2021-2026", "domain": "economic_development", "achievement_or_event": "任县委书记期间实施'五五一'发展思路,2025年聚焦'拼经济抓改革促发展',推动'三高四新'在县落地", "role_in_event": "县委书记", "location": "东安县", "confidence": "confirmed", "source_ids": ["S019"]},
        ],
        "work_style": [
            {"trait": "low_profile", "evidence": "省直机关出身, 公开讲话以落实中央省委部署为主基调", "confidence": "plausible", "source_ids": ["S019"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "provincial_department|local_ladder", "systems": ["government", "party", "other"], "geo": ["华容", "长沙", "衡山", "宁远", "东安"]},
    },
    # ── 4. 前任县委书记 (2016-2021) ──
    {
        "id": 4, "name": "冯德校", "gender": "男", "ethnicity": "汉族",
        "birth": "1965-03", "birthplace": "湖南永州市冷水滩区", "education": "大学本科(中南林科大经济管理)",
        "party_join": "1985-09", "work_start": "1986-07",
        "current_post": "永州市人大常委会副主任", "current_org": "永州市人大常委会",
        "source": "S008 S010 S016",
        "profile_notes": "1965年3月生, 湖南永州冷水滩区人. 1986年7月参加工作, 大学学历. 从冷水滩起家: 2000-2006冷水滩区委副书记, 2006-2007永州市委政法委副书记, 2007-2010永州市水利局局长, 2010-2014蓝山县委副书记、县长, 2014-2016江永县委书记, 2016-2021东安县委书记. 2021年7月卸任后任永州市人大常委会副主任(第六届). 组织纪律问题前科: 2017年12月新华社报道, 永州市委组织部通报东安县选拔任用干部程序问题(取消两名干部任命), 冯德校被批评教育.",
        "career": [
            {"start": "1983-09", "end": "1986-07", "org": "湖南科技学院", "title": "化学系学生", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "永州市湖南科技学院(原零陵师范专科学校)", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "1986-07", "end": "1992-09", "org": "湖南南岭化工厂", "title": "子弟学校教师/科研所做员、团委副书记、团委书记", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "1986-07任子弟学校教师; 1988-07转科研所处团委", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "1992-09", "end": "1997-11", "org": "永州凤凰园经济开发区", "title": "人才交流中心干部/副主任、经发委主任、招商局局长", "level": "园区", "system": "development_zone", "rank": "正科级(1993)", "is_key_promotion": True, "notes": "开发区系统起步", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "1997-11", "end": "2000-12", "org": "永州凤凰园经济开发区", "title": "管委会党委委员、副主任", "level": "园区", "system": "development_zone", "rank": "副处级", "is_key_promotion": True, "notes": "其间1999.05-2000.01省商务厅挂职副处长", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2000-12", "end": "2006-06", "org": "中共冷水滩区委员会", "title": "区委副书记", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "冷水滩区委副书记", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2006-06", "end": "2007-03", "org": "永州市委政法委", "title": "副书记", "level": "中心级", "system": "public_security", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2007-03", "end": "2010-01", "org": "永州市水利局", "title": "党组副书记、局长", "level": "中心级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2010-02", "end": "2014-05", "org": "蓝山县人民政府", "title": "蓝山县委副书记、县长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2010-01-21任蓝山县代县长", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2014-05", "end": "2016-08", "org": "中共江永县委员会", "title": "县委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2016-08", "end": "2021-07", "org": "中共东安县委员会", "title": "县委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2017年12月因选任程序问题被市委组织部批评教育", "confidence": "confirmed", "source_ids": ["S008", "S016"]},
            {"start": "2021-07", "end": "present", "org": "永州市人大常委会", "title": "永州市人大常委会副主任", "level": "中心级", "system": "other", "rank": "副厅级", "is_key_promotion": True, "notes": "2021-07卸任(另有任用), 后任永州市第六届人大常委会副主任(快解百科/官网确认)", "confidence": "confirmed", "source_ids": ["S010"]},
        ],
        "governance": [],
        "work_style": [
            {"trait": "stability_oriented", "evidence": "历政法委、水利、县党政主官岗位, 干部任免问题曾被追责——注意纪律风险", "confidence": "plausible", "source_ids": ["S016"]},
        ],
        "risk": [
            {"type": "controversy", "description": "2017-12 永州市委组织部通报: 东安县委在两名干部选拔任用中未严格执行程序, 一名干部存在年龄问题, 已取消任命; 东安县委书记冯德校被批评教育", "date": "2017-12", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "extras": {"career_pattern": "local_ladder|cross_county_rotation", "systems": ["development_zone", "public_security", "government", "party"], "geo": ["冷水滩", "永州", "蓝山", "江永", "东安"]},
    },
    # ── 5. 前县长 (2016-2021) ──
    {
        "id": 5, "name": "龙向洋", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "永州市人大常委会副主任", "current_org": "永州市人大常委会",
        "source": "S008 S018 S020",
        "profile_notes": "东安县前县长(约2016.07-2021.07). 2016年8月任东安县委副书记、提名为县长候选人, 2021年7月卸任另有任用. 2026年7月28日当选永州市人大常委会副主任——升任市级. 出生/籍贯/前期履历公开资料不足(缺口).",
        "career": [
            {"start": "2016-08", "end": "2021-07", "org": "东安县人民政府", "title": "县委副书记、县长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2016-08-02提名县长候选人, 同期任县委副书记; 与县委书记冯德校搭班5年", "confidence": "confirmed", "source_ids": ["S008", "S018"]},
            {"start": "2026-07-28", "end": "present", "org": "永州市人大常委会", "title": "副主任", "level": "中心级", "system": "other", "rank": "副厅级", "is_key_promotion": True, "notes": "2021-07卸任后至2026-07期间履历(2022?任职)待核; 2026-07-28永州市级会议选举为人大常委会副主任", "confidence": "confirmed", "source_ids": ["S020"]},
        ],
        "governance": [],
        "work_style": [],
        "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government"], "geo": ["东安", "永州"]},
    },
    # ── 6. 前前任县委书记 (2011-2016), 现市政协主席 ──
    {
        "id": 6, "name": "谢景林", "gender": "男", "ethnicity": "汉族",
        "birth": "1966-04", "birthplace": "湖南永州新田县", "education": "大学文化(中央党校函授大专)",
        "party_join": "1990-03", "work_start": "1987-07",
        "current_post": "永州市政协主席", "current_org": "永州市政协",
        "source": "S008 S011 S020",
        "profile_notes": "1966年4月生, 湖南新田人. 1987年7月起在冷水滩(永州市)基层: 农业系统、街道党委书记、冷水滩副区长兼常委; 2007年3月任东安县委副书记、副县长、代县长、县长; 2012年2月任东安县委书记(2007-2016东安县任职9年); 2016年8月卸任东安县委书记; 2017年1月当选永州市副市长; 2022年1月任永州市政协主席(现任). 典型'本地成长型'干部(新田→冷水滩→东安→永州).",
        "career": [
            {"start": "1987-07", "end": "1991-10", "org": "江华县农业农村委员会", "title": "农委干部", "level": "", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "1991-10", "end": "1995-02", "org": "冷水滩市农业局", "title": "副科级干部", "level": "乡科级", "system": "government", "rank": "副科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "1995-02", "end": "1997-06", "org": "冷水滩区农业综合开发办公室", "title": "副科级干部", "level": "乡科级", "system": "government", "rank": "副科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "1997-06", "end": "1997-12", "org": "冷水滩区菱角山街道办事处", "title": "党工委副书记、主任", "level": "乡科级", "system": "government", "rank": "正科级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "1997-12", "end": "2000-12", "org": "冷水滩区菱角山街道", "title": "党工委书记", "level": "乡科级", "system": "party", "rank": "正科级", "is_key_promotion": True, "notes": "1995.08-1997.12中央党校函授涉外经管大专", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2000-12", "end": "2002-01", "org": "冷水滩区人民政府", "title": "副区长", "level": "县政府", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2002-01", "end": "2007-03", "org": "中共冷水滩区委员会", "title": "区委常委、副区长", "level": "区级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2007-03", "end": "2011-02", "org": "东安县人民政府", "title": "县委副书记、副县长、代县长、县长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2009.03东安县长", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2011-02", "end": "2016-08", "org": "中共东安县委员会", "title": "县委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2016-08-02卸任(因工作需要调往永州市)", "confidence": "confirmed", "source_ids": ["S011", "S008"]},
            {"start": "2017-01", "end": "2021-12", "org": "永州市人民政府", "title": "副市长", "level": "中心级", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "2017-01-09当选永州市副市长", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2022-01", "end": "present", "org": "政协永州市委员会", "title": "市政协主席", "level": "中心级", "system": "other", "rank": "正厅级", "is_key_promotion": True, "notes": "2022-01-01当选市政协六届委员会主席", "confidence": "confirmed", "source_ids": ["S011"]},
        ],
        "governance": [],
        "work_style": [
            {"trait": "local_ladder", "evidence": "冷水26年累计: 冷水滩→东江→永州, 完整本地晋升路径示范", "confidence": "confirmed", "source_ids": ["S011"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "local_ladder|cross_county_rotation", "systems": ["government", "party"], "geo": ["新田", "冷水滩", "东安", "永州"]},
    },
    # ── 7. 现任县委副书记、统战部部长 ──
    {
        "id": 7, "name": "李月红", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "东安县委副书记、统战部部长", "current_org": "中共东安县委员会",
        "source": "S004 S014 S019",
        "profile_notes": "东安县县委副书记、县委统战部部长(2026-01已见报道, 2026-07-28十四届县委换届后连任副书记). 出生、籍贯、教育、之前履历均未查到公开来源(缺口).",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共东安县委员会", "title": "县委副书记、统战部部长", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "2026-01县委常委会报道任用县委副书记、统战部长; 2026-07-29十四届县委副书记连任", "confidence": "confirmed", "source_ids": ["S004", "S019"]},
        ],
        "governance": [],
        "work_style": [],
        "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    # ── 8-15. 县委常委会其余成员 ──
    {
        "id": 8, "name": "唐亚辉", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县委常委", "current_org": "中共东安县委员会",
        "source": "S004",
        "profile_notes": "东安县县委委员、常委(2026-07-29 十四届县委常委会名单); 具体分工(纪检/组织/政法等)未公开查到. 简历待核.",
        "career": [],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 9, "name": "成宇", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-11", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县委常委、县人民政府副县长(常务)", "current_org": "东安县人民政府",
        "source": "S001 S004 S014",
        "profile_notes": "成宇, 男, 汉族, 1983年11月出生, 大学本科, 中共党员. 现任东安县委常委、常务副县长(负责发改、财政、税收、金融、应急等). 此前履历待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民政府", "title": "县委常委、常务副县长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "现任常务副县长; 2026-07-29连任县委常委", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": []},
    },
    {
        "id": 10, "name": "秦波", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县委常委", "current_org": "中共东安县委员会",
        "source": "S004 S014",
        "profile_notes": "东安县委委员、常委(2026-07-29十四届县委常委会); 已于2026-01县委常委会/2026-07走访部队活动中见报道. 具体分工待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共东安县委员会", "title": "县委常委", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 11, "name": "周丽", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县委常委", "current_org": "中共东安县委员会",
        "source": "S004",
        "profile_notes": "东安县委委员、常委(2026-07-29十四届县委常委会名单新进). 女性干部, 具体分工待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共东安县委员会", "title": "县委常委", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "十四届县委常委会新进成员", "confidence": "confirmed", "source_ids": ["S004"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 12, "name": "杨加勉", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县委常委、县人武部部长", "current_org": "东安县人民武装部",
        "source": "S004 S014",
        "profile_notes": "东安县委常委、县人民武装部部长(2026-07-29连任十四届县委常委). 军队系统干部.",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民武装部", "title": "县委常委、县人武部部长", "level": "县处级", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S004", "S014"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 13, "name": "唐琳玮", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县委常委、县纪委书记", "current_org": "中共东安县纪律检查委员会",
        "source": "S004 S005",
        "profile_notes": "东安县委常委、县纪委书记(2026-07-29县纪委十四届一次全会选出新班子, 唐琳玮主持会议; 新一届县纪委书记). 履历待核.",
        "career": [
            {"start": "2026-07-29", "end": "present", "org": "中共东安县纪律检查委员会", "title": "县委常委、县纪委书记", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "县纪委十四届全会选举产生", "confidence": "confirmed", "source_ids": ["S005", "S004"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "discipline_track", "systems": ["party"], "geo": []},
    },
    {
        "id": 14, "name": "周志成", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-01", "birthplace": "湖南永州东安", "education": "本科",
        "party_join": "2003-06", "work_start": "1999-12",
        "current_post": "东安县委常委、副县长", "current_org": "东安县人民政府",
        "source": "S001 S004 S014",
        "profile_notes": "周志成, 男, 1981年1月生, 湖南东安人, 1999年12月参加工作, 2003年6月入党, 本科. 现任东安县委常委、副县长(教育、人社、生态环境、市场监管). 2026-07-29十四届县委常委会连任(新进常委).",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民政府", "title": "副县长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "现任副县长; 2026-07换届后新进县委常委", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government"], "geo": ["东安"]},
    },
    {
        "id": 15, "name": "周禄雄", "gender": "男", "ethnicity": "汉族",
        "birth": "1990-01", "birthplace": "湖南永州新田", "education": "研究生",
        "party_join": "2012-04", "work_start": "2013-09",
        "current_post": "东安县人民政府副县长", "current_org": "东安县人民政府",
        "source": "S001 S004",
        "profile_notes": "周禄雄, 男, 汉族, 1990年1月生, 湖南新田人, 2013年9月参加工作, 2012年4月入党, 研究生. 现任东安县副县长(工业、商务、招商引资等), 2026-07-29新进十四届县委常委. 最年轻的县领导(1990年生).",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民政府", "title": "副县长、县政府副县长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "2026-07-29新进县委常委", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": ["新田"]},
    },
    # ── 16-20. 县政府其他成员 ──
    {
        "id": 16, "name": "唐久梅", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-10", "birthplace": "湖南永州零陵", "education": "大学文化",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县副县长", "current_org": "东安县人民政府",
        "source": "S001",
        "profile_notes": "唐久梅, 男, 汉族, 1972年10月生, 湖南零陵人, 中共党员, 大学. 现任东安县委常委、副县长(自然资源、住房城建、城管). 2026-07-29换届后不再任县委常委(仍副县长).",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民政府", "title": "副县长(自然资源/住建/城管)", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "2026-07-29换届后退出县委常委名单, 留任副县长", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government"], "geo": ["零陵"]},
    },
    {
        "id": 17, "name": "秦琦", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-01", "birthplace": "湖南永州零陵", "education": "大学学历",
        "party_join": "民盟", "work_start": "1996-07",
        "current_post": "东安县人民政府副县长(民盟)", "current_org": "东安县人民政府",
        "source": "S001",
        "profile_notes": "秦琦, 男, 汉族, 湖南零陵人, 1975年1月生, 1996年7月参加工作, 2006年11月加入民盟, 大学学历. 现任副县长(交通、文化、旅游、融媒体等), 民盟永州市委副主任委员(兼).",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民政府", "title": "副县长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "党外干部(民盟)", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": ["零陵"]},
    },
    {
        "id": 18, "name": "周文", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-11", "birthplace": "湖南永州东安", "education": "研究生学历",
        "party_join": "1999-11", "work_start": "2001-09",
        "current_post": "东安县人民政府副县长", "current_org": "东安县人民政府",
        "source": "S001",
        "profile_notes": "周文, 男, 汉族, 湖南东安人, 1978年11月出生, 研究生学历, 2001年9月参加工作, 1999年11月加入中国共产党. 现任副县长(农业农村、水利、林业、乡村振兴等), 本地成长干部.",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民政府", "title": "副县长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "负责农业、水利、乡村振兴等", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government"], "geo": ["东安"]},
    },
    {
        "id": 19, "name": "杨伟燕", "gender": "女", "ethnicity": "汉族",
        "birth": "1985-04", "birthplace": "湖南永州宁远", "education": "硕士研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县人民政府副县长", "current_org": "东安县人民政府",
        "source": "S001",
        "profile_notes": "杨伟燕, 女, 汉族, 1985年4月出生, 湖南宁远人, 中共党员, 硕士研究生学历. 现任东安县政府副县长(民政、卫健、医保、残联等).",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人民政府", "title": "副县长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "负责民政、卫生健康、医保等", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": ["宁远"]},
    },
    {
        "id": 20, "name": "宋志勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-01", "birthplace": "湖南永州", "education": "大学学历",
        "party_join": "1996-07", "work_start": "1999-08",
        "current_post": "东安县人民政府副县长、县公安局局长", "current_org": "东安县公安局",
        "source": "S001",
        "profile_notes": "宋志勇, 男, 汉族, 1976年1月出生, 湖南永州人, 1999年8月参加工作, 1996年7月加入中国共产党, 大学学历. 现任副县长、县公安局局长(公安、司法、信访等), 公安系统交流任职干部.",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县公安局", "title": "副县长、县公安局局长", "level": "县处级", "system": "public_security", "rank": "副处级", "is_key_promotion": False, "notes": "公安系统负责人", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "system_rotation", "systems": ["public_security"], "geo": ["永州"]},
    },
    # ── 21-22. 县人大、政协 ──
    {
        "id": 21, "name": "张波", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县人大常委会主任", "current_org": "东安县人大常委会",
        "source": "S013 S014",
        "profile_notes": "东安县人大常委会主任(2026-07-23主持县十八届人大常委会议). 履历待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "东安县人大常委会", "title": "县人大常委会主任", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promotion": False, "notes": "现任主任", "confidence": "confirmed", "source_ids": ["S013"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 22, "name": "李劲涛", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安县政协主席", "current_org": "政协东安县委员会",
        "source": "S014 S019",
        "profile_notes": "东安县政协主席(2026-01-08/2026-07-30报道). 履历待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "政协东安县委员会", "title": "县政协主席", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S014"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    # ── 23-24. 跨县联动节点 (东安籍/工作关联) ──
    {
        "id": 23, "name": "陈雄", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "湖南永州东安", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "新田县委书记", "current_org": "中共新田县委员会",
        "source": "S018 S020",
        "profile_notes": "陈雄, 湖南东安人, 现任新田县委书记(约2021年起, 具体起始待核). 东安籍干部政新田——'本地干部外县主政'模式之一. 与蒋华构成'蒋华曾任新田(2015-2016)赴东安 (现任), 陈雄赴新田'的接续关系(弱关联).",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共新田县委员会", "title": "县委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": False, "notes": "现任新田县委书记(约2021年起)", "confidence": "confirmed", "source_ids": ["S018"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "cross_county_rotation", "systems": ["party"], "geo": ["东安", "新田"]},
    },
    {
        "id": 24, "name": "蒋崇华", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-03", "birthplace": "湖南永州东安", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "祁阳市委书记", "current_org": "中共祁阳市委员会",
        "source": "S020",
        "profile_notes": "蒋崇华, 1968年3月生, 湖南东安人, 现任永州祁阳市市委书记(截至2026-07-25驻祁阳资料). 东安籍厅处级干部在外县主政: 与东安县本县干部构成'东安籍外县任职'网络. (本库'永州'人物档案20260724期收录: 蒋崇华 祁阳市委书记/1968-03/湖南东安)",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共祁阳市委员会", "title": "市委书记", "level": "县级市", "system": "party", "rank": "正处级", "is_key_promotion": False, "notes": "东安籍, 现任永州祁阳市委书记", "confidence": "confirmed", "source_ids": ["S020"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "cross_county_rotation", "systems": ["party"], "geo": ["东安", "祁阳"]},
    },
]

# ══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共东安县委员会", "type": "党委", "level": "县", "parent": "中共永州市委员会", "location": "湖南省永州市东安县"},
    {"id": 2, "name": "东安县人民政府", "type": "政府", "level": "县", "parent": "永州市人民政府", "location": "湖南省永州市东安县"},
    {"id": 3, "name": "东安县人大常委会", "type": "人大", "level": "县", "parent": "永州市人大常委会", "location": "湖南省永州市东安县"},
    {"id": 4, "name": "政协东安县委员会", "type": "政协", "level": "县", "parent": "政协永州市委员会", "location": "湖南省永州市东安县"},
    {"id": 5, "name": "中共东安县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共永州市纪律检查委员会", "location": "湖南省永州市东安县"},
    {"id": 6, "name": "东安县人民武装部", "type": "军事", "level": "县", "parent": "永州军分区", "location": "湖南省永州市东安县"},
    {"id": 7, "name": "东安县公安局", "type": "政法", "level": "县", "parent": "永州市公安局", "location": "湖南省永州市东安县"},
    {"id": 8, "name": "中共永州市委员会", "type": "党委", "level": "地级市", "parent": "中共湖南省委", "location": "湖南省永州市"},
    {"id": 9, "name": "永州市人民政府", "type": "政府", "level": "地级市", "parent": "湖南省人民政府", "location": "湖南省永州市"},
    {"id": 10, "name": "永州市人大常委会", "type": "人大", "level": "地级市", "parent": "湖南省人大常委会", "location": "湖南省永州市"},
    {"id": 11, "name": "政协永州市委员会", "type": "政协", "level": "地级市", "parent": "政协湖南省委员会", "location": "湖南省永州市"},
    {"id": 12, "name": "中共新田县委员会", "type": "党委", "level": "县", "parent": "中共永州市委", "location": "湖南省永州市新田县"},
    {"id": 13, "name": "宁远县人民政府", "type": "政府", "level": "县", "parent": "永州市人民政府", "location": "湖南省永州市宁远县"},
    {"id": 14, "name": "株洲高新技术产业开发区", "type": "开发区", "level": "地级市园区", "parent": "株洲市人民政府", "location": "湖南省株洲市"},
    {"id": 15, "name": "天元区人民政府(株洲市天元区)", "type": "政府", "level": "区", "parent": "株洲市人民政府", "location": "湖南省株洲市天元区"},
    {"id": 16, "name": "湖南省食品药品监督管理局(历称省药监局/省食药监局)", "type": "政府", "level": "厅级", "parent": "湖南省人民政府", "location": "湖南省长沙市"},
    {"id": 17, "name": "衡山县人民政府", "type": "政府", "level": "县", "parent": "衡阳市人民政府", "location": "湖南省衡阳市衡山县"},
    {"id": 18, "name": "道县人民政府", "type": "政府", "level": "县", "parent": "永州市人民政府", "location": "湖南省永州市道县"},
    {"id": 19, "name": "中共道县横岭瑶族乡等乡镇党委", "type": "乡镇", "level": "乡镇", "parent": "中共道县县委", "location": "湖南省永州市道县"},
    {"id": 20, "name": "中共新田县委员会", "type": "党委", "level": "县", "parent": "中共永州市委", "location": "湖南省永州市新田县", "note": "与中共东安县委平级邻县; 蒋华曾任新田县委常委"},
    {"id": 21, "name": "中共祁阳市委员会", "type": "党委", "level": "县级市", "parent": "中共永州市委", "location": "湖南省永州市祁阳市"},
    {"id": 22, "name": "永州凤凰园经济开发区", "type": "开发区", "level": "市级园区", "parent": "永州市人民政府", "location": "湖南省永州市冷水滩"},
    {"id": 23, "name": "中共冷水滩区委员会", "type": "党委", "level": "区", "parent": "中共永州市委", "location": "湖南省永州市冷水滩区"},
    {"id": 24, "name": "永州市水利局", "type": "政府", "level": "地级市", "parent": "永州市人民政府", "location": "湖南省永州市"},
    {"id": 25, "name": "中共蓝山县委员会", "type": "党委", "level": "县", "parent": "中共永州市委", "location": "湖南省永州市蓝山县"},
    {"id": 26, "name": "中共江永县委员会", "type": "党委", "level": "县", "parent": "中共永州市委", "location": "湖南省永州市江永县"},
]

# ══════════════════════════════════════════════════════════════════════════
# POSITIONS (worked_at edges)
# ══════════════════════════════════════════════════════════════════════════
positions = [
    # 蒋华 (1)
    {"person_id": 1, "org_id": 18, "title": "副县长(副处)", "start_date": "2012-09", "end_date": "2015-04", "rank": "副处级", "note": "道县人民政府副县长"},
    {"person_id": 1, "org_id": 12, "title": "新田县委常委、县委办主任", "start_date": "2015-04", "end_date": "2016-08", "rank": "副处级", "note": "跨县交流; 期间挂东莞市农业农村局副局长"},
    {"person_id": 1, "org_id": 2, "title": "东安县委常委、常务副县长", "start_date": "2016-08", "end_date": "2021-07", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长", "start_date": "2021-07", "end_date": "2026-06", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-06-29", "end_date": "present", "rank": "正处级", "note": "县人武部党委第一书记"},
    # 洪海侠 (2)
    {"person_id": 2, "org_id": 14, "title": "株洲高新区党工委委员", "start_date": "unknown", "end_date": "2026-06", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "天元区委常委、副区长", "start_date": "unknown", "end_date": "2026-06", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-06-29", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "县人大常委会决定(日期待核)"},
    # 唐何 (3)
    {"person_id": 3, "org_id": 16, "title": "省药监/食药监系统历任科员至培训中心主任、人事处副处长", "start_date": "2001-08", "end_date": "2013-02", "rank": "副处级", "note": "2013.02-2014.12省食品药品检验研究院书记/院长"},
    {"person_id": 3, "org_id": 16, "title": "省食药监稽查总队稽查专员", "start_date": "2014-12", "end_date": "2015-03", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 17, "title": "衡山县委常委、副县长(挂职)", "start_date": "2015-03", "end_date": "2016-08", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 13, "title": "宁远县委副书记、县长", "start_date": "2016-08", "end_date": "2021-07", "rank": "正处级", "note": "2016.08-2016.11代县长"},
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2021-07", "end_date": "2026-06", "rank": "正处级", "note": "2025年二级巡视员"},
    # 冯德校 (4)
    {"person_id": 4, "org_id": 22, "title": "凤凰园经开区经委会主任、招商局长等", "start_date": "1992-09", "end_date": "2000-12", "rank": "副处级", "note": "1997-2000管委会党委委员/副主任"},
    {"person_id": 4, "org_id": 23, "title": "冷水滩区委副书记", "start_date": "2000-12", "end_date": "2006-06", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 24, "title": "永州市水利局党组副书记、局长", "start_date": "2007-03", "end_date": "2010-01", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 25, "title": "蓝山县委副书记、县长", "start_date": "2010-02", "end_date": "2014-05", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 26, "title": "县委书记", "start_date": "2014-05", "end_date": "2016-08", "rank": "正处级", "note": "江永县"},
    {"person_id": 4, "org_id": 1, "title": "县委书记", "start_date": "2016-08", "end_date": "2021-07", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 10, "title": "市人大常委会副主任(第六届)", "start_date": "2021-07", "end_date": "present", "rank": "副厅级", "note": ""},
    # 龙向洋 (5)
    {"person_id": 5, "org_id": 2, "title": "县委副书记、县长", "start_date": "2016-08", "end_date": "2021-07", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 10, "title": "永州市人大常委会副主任", "start_date": "2026-07-28", "end_date": "present", "rank": "副厅级", "note": ""},
    # 谢景林 (6)
    {"person_id": 6, "org_id": 22, "title": "冷水滩区菱角山街道党工委书记/街道办主任", "start_date": "1997-06", "end_date": "2000-12", "rank": "正科级", "note": "1997.12起任街道党委书记"},
    {"person_id": 6, "org_id": 2, "title": "县委副书记、副县长、代县长、县长", "start_date": "2007-03", "end_date": "2011-02", "rank": "正处级", "note": "历任, 2009年任县长"},
    {"person_id": 6, "org_id": 1, "title": "县委书记、县委常委、政法委", "start_date": "2011-02", "end_date": "2016-08", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 9, "title": "永州市人民政府副市长", "start_date": "2017-01", "end_date": "2021-12", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 11, "title": "永州市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": ""},
    # 李月红 (7)
    {"person_id": 7, "org_id": 1, "title": "县委副书记、统战部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 9-15 常委/政府 (用县政权组织)
    {"person_id": 9, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "县委常委、县人武部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "县委常委、县纪委书记", "start_date": "2026-07-29", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "教育、人社、环保等; 2026-07-29新进常委"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "工科、商务招商等; 2026-07-29新进常委"},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "自然资源、住建、城管"},
    {"person_id": 17, "org_id": 2, "title": "副县长(民盟)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "民政、卫生、医保"},
    {"person_id": 20, "org_id": 7, "title": "副县长、县公安局局长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "县人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "县政协主席", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    # 跨县联动
    {"person_id": 23, "org_id": 20, "title": "县委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "新田县; 东安县人"},
    {"person_id": 24, "org_id": 21, "title": "市委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "祁阳市; 东安县人"},
]

# ══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════
relationships = [
    # 现任班子
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "蒋华(书记)与洪海侠(代理县长)自2026-06搭班子, 2026-07党代会后连任党政正职", "overlap_org": "东安县党政班子", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 7, "type": "县委领导班子", "context": "蒋华(书记)与李月红(副书记/统战部长)2021-2026年在县委班子共事", "overlap_org": "东安县委", "overlap_period": "2021-2026(换届后连任副书记)"},
    # 前任主官链条
    {"person_a": 1, "person_b": 3, "type": "书记-县长转任", "context": "唐何(书记)+蒋华(县长)搭档执政2021-2026; 2026-06 蒋华接任书记——县长转书记模式", "overlap_org": "东安县党政班子", "overlap_period": "2021-07至2026-06"},
    {"person_a": 4, "person_b": 3, "type": "前后任县委书记交接", "context": "2021-07-05干部大会交接: 冯德校不再担任, 唐何任县委书记", "overlap_org": "东安县委", "overlap_period": "2021-07"},
    {"person_a": 6, "person_b": 4, "type": "前后任县委书记交接", "context": "2016-08-02干部大会: 谢景林不再担任, 冯德校接任县委书记", "overlap_org": "东安县委", "overlap_period": "2016-08"},
    {"person_a": 1, "person_b": 4, "type": "上下级搭档", "context": "冯德校(书记)与蒋华(常务副县长)2016-2021同在东安县委县政府班子", "overlap_org": "东安县", "overlap_period": "2016-08至2021-07"},
    {"person_a": 5, "person_b": 4, "type": "书记-县长搭档", "context": "冯德校(书记)+龙向洋(县长)2016-2021执政搭档", "overlap_org": "东安县", "overlap_period": "2016-08至2021-07"},
    {"person_a": 5, "person_b": 1, "type": "前后任县长", "context": "龙向洋(县长)→蒋华(县长)2021-07干部大会交接", "overlap_org": "东安县政府", "overlap_period": "2021-07"},
    # 县域干部与市级晋升
    {"person_a": 4, "person_b": 5, "type": "市级平台再聚", "context": "冯德校(2021)、龙向洋(2026-07-28)先后从东安调任永州市人大常委会副主任, 在市人大再次共事", "overlap_org": "永州市人大常委会", "overlap_period": "2026-07至今"},
    {"person_a": 5, "person_b": 6, "type": "县级到市级晋升", "context": "龙向洋由东安县县长历任后升永州市人大常委会副主任(2026-07-28), 谢景林由县委书记升永州市政协主席(2022)", "overlap_org": "永州市人大/政协", "overlap_period": "2022/2026"},
    # 跨县交流
    {"person_a": 1, "person_b": 23, "type": "跨县接续任职", "context": "蒋华于2015-2016任新田县委常委(县委办), 陈雄现任新田县委书记(东安籍)——两县干部接续流转的注记", "overlap_org": "新田县", "overlap_period": "2015-2016/2021-"},
    {"person_a": 1, "person_b": 24, "type": "县际干部群体", "context": "蒋华(东安县委书记)与蒋崇华(祁阳市委书记, 东安籍)同为县域正职, 东安县与祁阳系毗邻县市", "overlap_org": "永州市县域主官", "overlap_period": "2026"},
    # 班子共事-现任
    {"person_a": 1, "person_b": 9, "type": "政府班子搭档", "context": "蒋华(县长任期)与成宇(常务副县长)2021-2026年其他同士县政府常务工作", "overlap_org": "东安县政府", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 7, "type": "县委副书记搭档", "context": "洪海侠与李月红2026-07十四届县委第三届副书记当选", "overlap_org": "东安县委", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 9, "type": "政府班子搭档", "context": "洪海侠(代理县长)与成宇(常务副县长)2026搭班", "overlap_org": "东安县政府", "overlap_period": "2026-07至今"},
]

# ══════════════════════════════════════════════════════════════════════════
# DATABASE BUILD
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
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})",
                     [p.get(c, "") for c in cols_p])
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})",
                     [o.get(c, "") for c in cols_o])
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})",
                     [pos.get(c, "") for c in cols_pos])
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})",
                     [r.get(c, "") for c in cols_r])
    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ══════════════════════════════════════════════════════════════════════════
# GEXF
# ══════════════════════════════════════════════════════════════════════════
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(title):
    t = title or ""
    if ("书记" in t and "副" not in t) or "书记" in t:
        return "255,50,50"
    if "县长" in t or "市长" in t:
        return "50,100,255"
    if "纪委" in t:
        return "255,165,0"
    if "主任" in t or "主席" in t:
        return "200,120,40"
    if "常委" in t:
        return "150,120,200"
    return "100,100,100"


def org_color(o):
    return {
        "党委": "255,200,200", "政府": "200,200,255", "纪委": "255,200,150",
        "开发区": "200,255,200", "乡镇": "255,255,200", "事业单位": "220,220,220",
        "人大": "200,255,255", "政协": "255,240,200", "政法": "200,220,255",
        "军事": "230,230,230",
    }.get(o, "200,200,200")


def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>东安县领导班子工作关系网络 — 县委书记/县长双核心, 含前任前后任、县委县政府班子、人大政协、纪检公安与跨县/市级关联节点</description>')
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
    top = {1, 2, 3, 4, 5, 6}
    for p in persons:
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if p["id"] in top else "12.0"
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
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start_date", ""))}—{esc(pos.get("end_date", ""))}"/>')
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
# PERSON JSON (full schema per person_graph_json.md)
# ══════════════════════════════════════════════════════════════════════════
def build_person_json(p: dict) -> dict:
    pid = p["id"]
    career_timeline = []
    # Prefer the curated per-person career list when present.
    for entry in p.get("career", []):
        career_timeline.append({
            "start": entry.get("start") or "unknown", "end": entry.get("end") or "present",
            "org": entry.get("org", ""), "title": entry.get("title", ""),
            "level": entry.get("level", ""), "location": entry.get("location", "湖南省永州市"),
            "system": entry.get("system", "other"), "rank": entry.get("rank", ""),
            "is_key_promotion": entry.get("is_key_promotion", False),
            "notes": entry.get("notes", ""),
            "confidence": entry.get("confidence", "confirmed"),
            "source_ids": entry.get("source_ids", []),
        })
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        # Avoid duplicates for rows also covered by the curated career list.
        dup = any(
            c.get("org", "") == next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
            and c.get("title", "") == pos["title"]
            for c in career_timeline
        )
        if dup:
            continue
        system = "other"
        title = pos["title"]
        if "书记" in title or "委" in title:
            system = "party"
        elif "法院" in title or "公安" in title or "政法" in title:
            system = "public_security"
        elif "纪委" in title or "监委" in title:
            system = "discipline"
        elif "政府" in title or "县长" in title or "市长" in title or "镇" in title or "乡" in title:
            system = "government"
        elif "组织部" in title:
            system = "organization"
        career_timeline.append({
            "start": pos.get("start_date") or "unknown", "end": pos.get("end_date") or "present",
            "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
            "title": title, "level": pos.get("rank", ""), "location": "",
            "system": system, "rank": pos.get("rank", ""),
            "notes": pos.get("note", ""), "confidence": "confirmed",
            "source_ids": [s for s in p.get("source", "").split() if s],
        })
    if not career_timeline:
        career_timeline.append({
            "start": "unknown", "end": "present", "org": p.get("current_org", ""),
            "title": p.get("current_post", ""), "level": "县处级", "location": "湖南省永州市东安县",
            "system": "other", "rank": "", "is_key_promotion": False,
            "notes": "公开资料有限, 任职起始时间待核。", "confidence": "unverified", "source_ids": [],
        })
    rels = []
    for r in relationships:
        if r["person_a"] == pid or r["person_b"] == pid:
            other = r["person_b"] if r["person_a"] == pid else r["person_a"]
            other_name = next((x["name"] for x in persons if x["id"] == other), str(other))
            rels.append({
                "person": other_name, "person_id": f"dongan_{other}",
                "relationship_type": r["type"], "strength": "medium",
                "evidence": r["context"], "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"], "direction": "undirected",
                "confidence": "confirmed", "source_ids": [],
            })
    src_ids = [s for s in p.get("source", "").replace(",", " ").split() if s]
    source_register = [dict(s) for s in SOURCES if s["id"] in src_ids]
    open_qs = []
    if not p.get("birth"):
        open_qs.append({"priority": "high", "question": f"{p['name']}出生年月缺失", "why_it_matters": "识别身份稳定性", "suggested_queries": [], "last_attempted": AS_OF})
    if not p.get("birthplace"):
        open_qs.append({"priority": "medium", "question": f"{p['name']}籍贯缺失", "why_it_matters": "地域网络分析", "suggested_queries": [], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_qs.append({"priority": "medium", "question": f"{p['name']}参加工作年份缺失", "why_it_matters": "履历完整性", "suggested_queries": [], "last_attempted": AS_OF})
    if pid == 3:
        open_qs.append({"priority": "critical", "question": "唐何 2026-06-29 卸任东安县委书记后'另有任用'的具体新职务未公开", "why_it_matters": "前任去向追踪与前向网络", "suggested_queries": ["唐何 新任", "唐何 永州市 局长", "唐何 人大常委会"], "last_attempted": AS_OF})
    if pid == 2:
        open_qs.append({"priority": "high", "question": "洪海侠2026年调任东安前的株洲任职经历(2017?-2026)早期履历未公开", "why_it_matters": "代理县长候选人完整履历", "suggested_queries": ["洪海侠 株洲 天元区 简历", "洪海侠 天元区 副区长 任前公示"], "last_attempted": AS_OF})
    if pid in (2, 7, 8, 10, 11):
        open_qs.append({"priority": "medium", "question": f"{p['name']}党支部内部分工(组织/宣传/政法等)未查证", "why_it_matters": "班子职能结构", "suggested_queries": [f"{p['name']} 东安 分工"], "last_attempted": AS_OF})
    governance = p.get("governance", []) or []
    style = p.get("work_style", []) or []
    risks = p.get("risk", []) or []
    if not risks:
        risks = [{"type": "none_found", "description": f"截至{AS_OF}未检索到{p['name']}本人的纪律处分或负面报道", "date": AS_OF, "confidence": "unverified", "source_ids": []}]
    extras = p.get("extras", {})
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "湖南省", "city": "永州市", "region": "东安县", "job": p.get("current_post", ""), "task_id": "hunan_东安县", "time_focus": "2016-2026"},
        "identity": {"person_id": f"dongan_{p['name']}_{p.get('birth', '')[:4]}", "name": p["name"], "aliases": [], "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""), "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""), "native_place": "", "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}], "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""), "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth', '')}", "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}", "official_profile_url": ""}},
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""), "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": src_ids},
        "career_timeline": career_timeline,
        "organizations": [
            {"org_id": str(pos["org_id"]), "name": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""), "role": pos["title"], "period": f"{pos.get('start_date', '')}-{pos.get('end_date', 'present')}", "source_ids": []}
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
    fname = f"{TODAY}-湖南省-永州市-{job_slug}-{p['name']}.json"
    fpath = Path(JSON_DIR) / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return fname


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
def main() -> None:
    print("=" * 60)
    print("  东安县领导班子工作关系网络 — 数据构建")
    print(f"  调查日期: {AS_OF}  任务: hunan_东安县")
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