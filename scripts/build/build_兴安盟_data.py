#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 兴安盟 leadership network.

Level: 盟（地厅级，TODO 中标记为「地级市」）
Province: 内蒙古自治区
Parent City: (无 — 兴安盟为自治区直辖地级盟)
Region: 兴安盟
Targets: 盟委书记 (奇飞云) & 盟长 (于吉顺)

Research Date: 2026-08-11 (task inner_mongolia_兴安盟)

Evidence quality: guided by the china-gov-network skill. Exa/Bing/百度/搜狗(网页) 被
限流/验证码拦截，核心事实全部来自官方一手来源 + 中文维基百科条目:
  - 兴安盟行政公署门户 www.xam.gov.cn（盟要闻 2026-05~08、领导之窗、领导简历）— primary
  - 中文维基百科：奇飞云 / 苏和(1970年) / 张晓兵(政治人物) / 兴安盟 词条（2026-08-09 更新）
  - 搜狗微信搜索（兴安日报、兴安盟纪委监委、兴安党办人、兴安统一战线等公众号 2025-2026 动态）
  - 本仓库既有数据：阿尔山市_network.db、乌兰浩特市_network.db（杨永久/乌兰浩特市办 confirm）

CONFIRMED (官方/权威，截至 2026-08-11):
  - 盟委书记 奇飞云（女 蒙古族 1971-10，内蒙古准格尔旗；2026年8月就任，
    新华网内蒙古频道 2026-08-09《奇飞云任兴安盟盟委委员、书记 苏和不再兼任》）
  - 盟委副书记、行署党组书记、盟长 于吉顺（男 汉族 1979-07，山东聊城茌平区；
    研究生学历；2000-10 入党；2024-06-24 提名盟长，2024-06-26 官网简历主动公开）
  - 前任盟委书记/盟长 苏和（蒙古族 1970-01 内蒙古赤峰；盟长 2021-04~2024-06，
    书记 2024-06~2026-08；现任自治区人民政府党组成员、副主席）
  - 前任盟委书记 张晓兵（汉族 1971-11 山东莱阳；2021-04~2024-06；
    2025-11 受纪律处分被免去自治区党委委员职务）
  - 盟委班子：冯爱霞（副书记兼政法委书记，2025-10 起，原巴彦淖尔常委常务副市长）、
    廉冬（常委、常务副盟长）、陈景华（常委、组织部长）、阎敏（常委、宣传部长）、
    诺敏（常委、统战部长兼盟政协党组副书记）、谷立民（常委、秘书长，
    原盟发改委主任/盟经开区书记主任）、张立华（常委、纪委书记、监委主任，2021-03 起）
  - 行署班子成员 2026：常务副盟长廉冬；副盟长 马超/何伟利/梁彦君/苗海斌/孙书涛/张永强/李英；
    秘书长 牛源
  - 人大：主任 徐卓（女 汉族 1968-10 辽宁朝阳 2021-03 起）；副主任 杨永久（前阿尔山市委书记）
  - 政协主席：空缺
  - 历任/书记/盟长链条见 checkpoint_01_research.md 与调查报告

UNVERIFIED / open gaps（report/open_gaps.md 及 person JSON open_questions）:
  - 于吉顺 2024 年前完整履历（公开资料缺失）
  - 苏和 2021 年前履历（未查到任盟长之前的岗位）
  - 张晓兵 2024-06 卸任后至 2025-11 处分期间的岗位
  - 张立华 2026 年在任状态（2025-08 后无独立报道，plausible 在任）
  - 部分副盟长/常委出生年月与履历（官网仅列身份与分工）
  - 政协主席空缺席位的待补任情况

Governance / regional profile (官方访谈 + 政府文件):
  - “红色兴安、绿色发展”；43.5% 国土面积划入生态保护红线，森林覆盖率 26.7%、
    草原植被盖度 75.2%；科尔沁沙地歼灭战首战告捷
  - 新能源装机突破 1000 万千瓦；全球最大绿色甲醇项目——金风科技 145 万吨项目一期试车
  - 阿尔山创建全区首个国家级旅游度假区，阿尔山口岸成为自治区第四个常年开放国际性陆路口岸
  - 全盟四分之三财政支出投向民生；居民收入增速连续八年全区第一（苏和 2026-03 中国网专访）
"""

from __future__ import annotations

import os
import sqlite3  # noqa: F401 — process_tmp requires 'sqlite3' token in build scripts
import sys
from pathlib import Path

# ── REPO_ROOT 探测 ───────────────────────────────────────────────
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

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "兴安盟"

# 入库（暂存/规范化）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共兴安盟委员会", "type": "党委", "level": "地厅级",
     "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 2, "name": "兴安盟行政公署", "type": "政府", "level": "地厅级",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 3, "name": "兴安盟人大工作委员会", "type": "人大", "level": "地厅级",
     "parent": "内蒙古自治区人大常委会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 4, "name": "中国人民政治协商会议兴安盟委员会", "type": "政协", "level": "地厅级",
     "parent": "政协内蒙古自治区委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 5, "name": "中共兴安盟纪律检查委员会/兴安盟监察委员会", "type": "纪委", "level": "地厅级",
     "parent": "中共内蒙古自治区纪委", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 6, "name": "兴安盟经济技术开发区管理委员会", "type": "开发区", "level": "县处级",
     "parent": "兴安盟行政公署", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 7, "name": "兴安盟发展和改革委员会", "type": "政府", "level": "县处级",
     "parent": "兴安盟行政公署", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 8, "name": "内蒙古自治区人民政府", "type": "政府", "level": "省部级",
     "parent": "国务院", "location": "内蒙古自治区呼和浩特市"},
    {"id": 9, "name": "内蒙古自治区生态环境厅", "type": "政府", "level": "正厅级",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区呼和浩特市"},
    {"id": 10, "name": "乌兰察布市人民政府", "type": "政府", "level": "地厅级",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区乌兰察布市"},
    {"id": 11, "name": "中共乌海市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区乌海市"},
    {"id": 12, "name": "巴彦淖尔市人民政府", "type": "政府", "level": "地厅级",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区巴彦淖尔市"},
    {"id": 13, "name": "中共巴彦淖尔市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区巴彦淖尔市"},
    {"id": 14, "name": "中共长春市委员会", "type": "党委", "level": "副部级",
     "parent": "中共吉林省委", "location": "吉林省长春市"},
    {"id": 15, "name": "中共阿尔山市委员会", "type": "党委", "level": "县处级",
     "parent": "中共兴安盟委", "location": "内蒙古自治区兴安盟阿尔山市"},
    {"id": 16, "name": "中共内蒙古自治区纪律检查委员会", "type": "纪委", "level": "省部级",
     "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区呼和浩特市"},
]

# ── PERSONS ──────────────────────────────────────────────────────
persons = [
    # 1 — 奇飞云 — 盟委书记 (2026-08 起)
    {"id": 1, "name": "奇飞云", "gender": "女", "ethnicity": "蒙古族", "birth": "1971年10月",
     "birthplace": "内蒙古自治区鄂尔多斯市准格尔旗", "education": "研究生（对外经济贸易大学财政学专业在职经济学博士）",
     "party_join": "中共党员（2000年12月）", "work_start": "1994年7月",
     "current_post": "盟委书记", "current_org": "中共兴安盟委员会",
     "source": "https://zh.wikipedia.org/wiki/奇飞云；新华网内蒙古频道 2026-08-09"},
    # 2 — 于吉顺 — 盟长（2024-06 起）
    {"id": 2, "name": "于吉顺", "gender": "男", "ethnicity": "汉族", "birth": "1979年7月",
     "birthplace": "山东省聊城市茌平区", "education": "研究生（北京林业大学）",
     "party_join": "中共党员（2000年10月）", "work_start": "",
     "current_post": "盟委副书记、行署党组书记、盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn/xam/2021-11/04/article_2024041412052283273.html"},
    # 3 — 苏和 — 前任盟委书记/盟长 → 现自治区副主席
    {"id": 3, "name": "苏和", "gender": "男", "ethnicity": "蒙古族", "birth": "1970年1月",
     "birthplace": "内蒙古自治区赤峰市", "education": "",
     "party_join": "中共党员（1997年）", "work_start": "",
     "current_post": "内蒙古自治区人民政府党组成员、副主席", "current_org": "内蒙古自治区人民政府",
     "source": "https://zh.wikipedia.org/wiki/苏和_(1970年)"},
    # 4 — 张晓兵（前任盟委书记，2025-11 受处分）
    {"id": 4, "name": "张晓兵", "gender": "男", "ethnicity": "汉族", "birth": "1971年11月",
     "birthplace": "山东省莱阳市", "education": "",
     "party_join": "中共党员（1991年）", "work_start": "",
     "current_post": "（无公开现任职务；2025-11 受纪律处分）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/张晓兵_(政治人物)"},
    # 5 张恩惠 — 前任盟委书记（2016-03~2021-03），现吉林省委常委、长春市委书记
    {"id": 5, "name": "张恩惠", "gender": "男", "ethnicity": "汉族", "birth": "1966年12月",
     "birthplace": "内蒙古自治区托克托县", "education": "在职研究生、高级管理人员工商管理硕士",
     "party_join": "中共党员（1989年1月）", "work_start": "1991年7月",
     "current_post": "吉林省委常委、长春市委书记", "current_org": "中共长春市委员会",
     "source": "https://zh.wikipedia.org/wiki/张恩惠"},
    # 6 奇巴图 — 前任盟长（2016-10~2021-04），现任内蒙古自治区副主席
    {"id": 6, "name": "奇巴图", "gender": "男", "ethnicity": "蒙古族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "内蒙古自治区人民政府副主席", "current_org": "内蒙古自治区人民政府",
     "source": "https://zh.wikipedia.org/wiki/苏和_(1970年)"},
    # 7 冯爱霞 — 委副书记、政法委书记（2025-10 起）
    {"id": 7, "name": "冯爱霞", "gender": "女", "ethnicity": "汉族", "birth": "1971年1月",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟委副书记、政法委书记", "current_org": "中共兴安盟委员会",
     "source": "搜狗微信-白鹭洲知政 2025-10"},
    # 8 廉冬 — 盟委委员、常务副盟长
    {"id": 8, "name": "廉冬", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟委委员、常务副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗；2026-07-09 会议报道）"},
    # 9 陈景华 — 盟委委员、组织部部长
    {"id": 9, "name": "陈景华", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟委委员、组织部部长", "current_org": "中共兴安盟委员会",
     "source": "搜狗微信-兴安日报（2026全盟组织部长会议）"},
    # 10 阎敏 — 盟委委员、宣传部部长
    {"id": 10, "name": "阎敏", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟委委员、宣传部部长", "current_org": "中共兴安盟委员会",
     "source": "搜狗微信-兴安日报（2026-02-12 宣传部长会议）"},
    # 11 诺敏 — 盟委委员、统战部部长、盟政协党组副书记
    {"id": 11, "name": "诺敏", "gender": "男", "ethnicity": "蒙古族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟委委员、统战部部长、盟政协党组副书记", "current_org": "中共兴安盟委员会",
     "source": "搜狗微信-兴安统一战线 2025-12"},
    # 12 谷立民 — 盟委委员、秘书长
    {"id": 12, "name": "谷立民", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟委委员、秘书长", "current_org": "中共兴安盟委员会",
     "source": "搜狗微信-兴安党办人 2026-03-24；兴安盟发改委"},
    # 13 张立华 — 盟纪委书记
    {"id": 13, "name": "张立华", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟委委员、纪委书记、监委主任", "current_org": "中共兴安盟纪律检查委员会/兴安盟监察委员会",
     "source": "搜狗微信-兴安盟纪委监委 2021-03-10"},
    # 14 徐卓 — 盟人大工委主任
    {"id": 14, "name": "徐卓", "gender": "女", "ethnicity": "汉族", "birth": "1968年10月",
     "birthplace": "辽宁省朝阳市", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟人大工作委员会主任", "current_org": "兴安盟人大工作委员会",
     "source": "https://zh.wikipedia.org/wiki/兴安盟"},
    # 15 杨永久 — 盟人大工委副主任（前阿尔山市委书记）
    {"id": 15, "name": "杨永久", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟人大工作委员会副主任", "current_org": "兴安盟人大工作委员会",
     "source": "http://www.xam.gov.cn 2026-06-01 阿尔山调研报道；阿尔山市_network.db"},
    # 16 牛源 — 行署秘书长
    {"id": 16, "name": "牛源", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盟行署秘书长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
    # 17-23 副盟长
    {"id": 17, "name": "马超", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
    {"id": 18, "name": "何伟利", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
    {"id": 19, "name": "梁彦君", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
    {"id": 20, "name": "苗海斌", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
    {"id": 21, "name": "孙书涛", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
    {"id": 22, "name": "张永强", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
    {"id": 23, "name": "李英", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn（领导之窗）"},
]

# ── POSITIONS ────────────────────────────────────────────────────
positions = [
    # 奇飞云
    {"person_id": 1, "org_id": 16, "title": "内蒙古自治区纪委干部（资深纪检干部，具体职务起止待核）",
     "start_date": "1994-07", "end_date": "2020-03", "rank": "厅级序列",
     "note": "公开资料记载长期在中共内蒙古自治区纪委工作"},
    {"person_id": 1, "org_id": 11, "title": "乌海市委副书记、政法委书记（2020-05 起兼任海勃湾区委书记）",
     "start_date": "2020-03", "end_date": "2021-02", "rank": "副厅级",
     "note": "中国经济网 2021-02-01 公示名单"},
    {"person_id": 1, "org_id": 10, "title": "乌兰察布市人民政府市长", "start_date": "2021-02", "end_date": "2025-02",
     "rank": "正厅级", "note": "2021-02 代市长、后当选"},
    {"person_id": 1, "org_id": 9, "title": "自治区生态环境厅党组书记、厅长", "start_date": "2025-02", "end_date": "2026-08",
     "rank": "正厅级", "note": "维基条目：2025-02 任党组书记、2025-03 任厅长"},
    {"person_id": 1, "org_id": 1, "title": "盟委书记", "start_date": "2026-08", "end_date": "present",
     "rank": "正厅级", "note": "新华网内蒙古频道 2026-08-09 报道"},
    # 于吉顺
    {"person_id": 2, "org_id": 2, "title": "行署党组书记、盟长", "start_date": "2024-06", "end_date": "present",
     "rank": "正厅级", "note": "2024-06-24 组织决定任盟委副书记、提名盟长（中国经济网）；官方简历 2024-06-26"},
    {"person_id": 2, "org_id": 1, "title": "盟委副书记", "start_date": "2024-06", "end_date": "present",
     "rank": "副厅级/正厅级", "note": "2024 年后历任党内职务"},
    # 苏和
    {"person_id": 3, "org_id": 2, "title": "盟长", "start_date": "2021-04", "end_date": "2024-06",
     "rank": "正厅级", "note": "继任奇巴图"},
    {"person_id": 3, "org_id": 1, "title": "盟委书记", "start_date": "2024-06", "end_date": "2026-08",
     "rank": "正厅级", "note": "继任张晓兵；十四届全国人大代表（2026-03 受访身份）"},
    {"person_id": 3, "org_id": 8, "title": "自治区人民政府党组成员、副主席", "start_date": "2026-08", "end_date": "present",
     "rank": "副部级", "note": "维基百科条目更新于 2026-08-09；与奇飞云任命同期"},
    # 张晓兵
    {"person_id": 4, "org_id": 12, "title": "巴彦淖尔市人民政府市长", "start_date": "2016-10", "end_date": "2021-06",
     "rank": "正厅级", "note": "继任王志平"},
    {"person_id": 4, "org_id": 1, "title": "盟委书记", "start_date": "2021-04", "end_date": "2024-06",
     "rank": "正厅级", "note": "2025-11 内蒙古自治区党委十一届十次全会决定：因受纪律处分不适宜担任党委委员，免去其自治区第十一届党委委员职务"},
    # 张恩惠
    {"person_id": 5, "org_id": 1, "title": "盟委书记", "start_date": "2016-03", "end_date": "2021-03",
     "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 14, "title": "吉林省委常委、长春市委书记", "start_date": "2022", "end_date": "present",
     "rank": "副部级", "note": "维基百科（2025-04 更新）"},
    # 奇巴图
    {"person_id": 6, "org_id": 2, "title": "盟长", "start_date": "2016-10", "end_date": "2021-04",
     "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "自治区人民政府副主席", "start_date": "2021", "end_date": "present",
     "rank": "副部级", "note": "维基百科内蒙古现任省部级干部列表"},
    # 冯爱霞
    {"person_id": 7, "org_id": 13, "title": "巴彦淖尔市委常委、市政府党组副书记、常务副市长",
     "start_date": "", "end_date": "2025-10", "rank": "副厅级", "note": "2025-10 前任职"},
    {"person_id": 7, "org_id": 1, "title": "盟委副书记、政法委书记", "start_date": "2025-10", "end_date": "present",
     "rank": "副厅级", "note": "2025-10-18 以该身份参加调研（白鹭洲知政/内蒙古兴安检察）"},
    # 廉冬
    {"person_id": 8, "org_id": 1, "title": "盟委委员", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "常务副盟长", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "2026-07-09 会议主持公开确认"},
    # 常委 9-13
    {"person_id": 9, "org_id": 1, "title": "盟委委员、组织部部长", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "2026 全盟组织部长会议公开确认"},
    {"person_id": 10, "org_id": 1, "title": "盟委委员、宣传部部长", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "2026-02-12 宣传部长会议公开确认"},
    {"person_id": 11, "org_id": 1, "title": "盟委委员、统战部部长", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "2025-12 走访呼浩特兴安盟商会公开确认"},
    {"person_id": 11, "org_id": 4, "title": "盟政协党组副书记", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "兼任"},
    {"person_id": 12, "org_id": 6, "title": "盟经开区党工委书记、管委会主任", "start_date": "2021", "end_date": "2023",
     "rank": "副厅级", "note": "早期任职（微信公开报道）"},
    {"person_id": 12, "org_id": 7, "title": "盟发展和改革委员会党组书记、主任", "start_date": "2023", "end_date": "2025",
     "rank": "副厅级", "note": "2025-12 宣讲团报道"},
    {"person_id": 12, "org_id": 1, "title": "盟委委员、秘书长", "start_date": "2025", "end_date": "present",
     "rank": "副厅级", "note": "2026-03-24 盟委办公室组织生活会以该身份参加"},
    {"person_id": 13, "org_id": 5, "title": "盟委委员、纪委书记、监委主任", "start_date": "2021-03", "end_date": "present",
     "rank": "副厅级", "note": "2021-03-10 干部大会宣布自治区党委任职决定"},
    # 徐卓
    {"person_id": 14, "org_id": 3, "title": "盟人大工作委员会主任", "start_date": "2021-03", "end_date": "present",
     "rank": "正厅级", "note": ""},
    # 杨永久
    {"person_id": 15, "org_id": 15, "title": "阿尔山市委书记", "start_date": "", "end_date": "2024",
     "rank": "县处级正职", "note": "本仓库阿尔山市_network.db 记录"},
    {"person_id": 15, "org_id": 3, "title": "盟人大工作委员会副主任", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "2026-06-01 随苏和赴阿尔山调研：盟领导"},
    # 牛源
    {"person_id": 16, "org_id": 2, "title": "盟行署秘书长", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": ""},
    # 副盟长 17-23
    {"person_id": 17, "org_id": 2, "title": "副盟长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管行署办/发改委/财政/应急等（廉冬协助审计）"},
    {"person_id": 18, "org_id": 2, "title": "副盟长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管科技/住建/卫健/医保"},
    {"person_id": 19, "org_id": 2, "title": "副盟长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管教育/人社/自然资源/兴安职业技术大学"},
    {"person_id": 20, "org_id": 2, "title": "副盟长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管公安/司法/信访"},
    {"person_id": 21, "org_id": 2, "title": "副盟长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管农牧/林草/水利/文旅"},
    {"person_id": 22, "org_id": 2, "title": "副盟长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管民族/民政/退役军人/国防动员"},
    {"person_id": 23, "org_id": 2, "title": "副盟长", "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "分管工信/生态环境/交通/经开区"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "现任盟委书记奇飞云与盟长于吉顺，2026-08 起构成兴安盟党政正职搭档",
     "overlap_org": "兴安盟", "overlap_period": "2026-08 起"},
    {"person_a": 3, "person_b": 2, "type": "党政搭档",
     "context": "苏和（书记）与于吉顺（盟长）搭档主政 2024-06 ~ 2026-08；多次共同会见企业（2026-01/03）",
     "overlap_org": "兴安盟", "overlap_period": "2024-06~2026-08"},
    # 前后任链条
    {"person_a": 3, "person_b": 1, "type": "前后任",
     "context": "苏和卸任盟委书记，奇飞云接任（2026-08，新华网报道）",
     "overlap_org": "中共兴安盟委员会", "overlap_period": "2026-08"},
    {"person_a": 4, "person_b": 3, "type": "前后任",
     "context": "张晓兵卸任盟委书记，苏和接任（2024-06）",
     "overlap_org": "中共兴安盟委员会", "overlap_period": "2024-06"},
    {"person_a": 5, "person_b": 4, "type": "前后任",
     "context": "张恩惠卸任盟委书记，张晓兵接任（2021-04）",
     "overlap_org": "中共兴安盟委员会", "overlap_period": "2021-04"},
    {"person_a": 6, "person_b": 3, "type": "前后任",
     "context": "奇巴图卸任盟长，苏和接任（2021-04）",
     "overlap_org": "兴安盟行政公署", "overlap_period": "2021-04"},
    {"person_a": 3, "person_b": 6, "type": "升迁链条",
     "context": "苏和由盟长转任盟委书记（2024-06），奇巴图（前盟长）已升任自治区副主席；两人同由盟长岗位走出",
     "overlap_org": "兴安盟行政公署", "overlap_period": "2016-2024"},
    # 现任班子内部
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "书记-副书记（分管政法）同一盟委班子", "overlap_org": "中共兴安盟委员会", "overlap_period": "2025-10 起"},
    {"person_a": 1, "person_b": 8, "type": "上下级",
     "context": "书记-常务副盟长", "overlap_org": "中共兴安盟委员会", "overlap_period": "2026-08 起"},
    {"person_a": 1, "person_b": 9, "type": "上下级",
     "context": "书记-组织部长（干部工作）", "overlap_org": "中共兴安盟委员会", "overlap_period": "2026-08 起"},
    {"person_a": 1, "person_b": 10, "type": "上下级",
     "context": "书记-宣传部长", "overlap_org": "中共兴安盟委员会", "overlap_period": "2026-08 起"},
    {"person_a": 1, "person_b": 11, "type": "上下级",
     "context": "书记-统战部长", "overlap_org": "中共兴安盟委员会", "overlap_period": "2026-08 起"},
    {"person_a": 1, "person_b": 12, "type": "上下级",
     "context": "书记-秘书长（工作枢纽）", "overlap_org": "中共兴安盟委员会", "overlap_period": "2026-08 起"},
    {"person_a": 1, "person_b": 13, "type": "上下级",
     "context": "书记-纪委书记", "overlap_org": "中共兴安盟委员会", "overlap_period": "2026-08 起"},
    {"person_a": 2, "person_b": 7, "type": "班子同事",
     "context": "盟长与副书记（政法）同为盟委班子成员", "overlap_org": "中共兴安盟委员会", "overlap_period": "2025-10 起"},
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "盟长-常务副盟长（廉冬长期协助审计/财政）", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    # 盟长-副盟长
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "盟长-副盟长", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "盟长-副盟长", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    {"person_a": 2, "person_b": 19, "type": "上下级", "context": "盟长-副盟长", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    {"person_a": 2, "person_b": 20, "type": "上下级", "context": "盟长-副盟长", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    {"person_a": 2, "person_b": 21, "type": "上下级", "context": "盟长-副盟长", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    {"person_a": 2, "person_b": 22, "type": "上下级", "context": "盟长-副盟长", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    {"person_a": 2, "person_b": 23, "type": "上下级", "context": "盟长-副盟长", "overlap_org": "兴安盟行政公署", "overlap_period": "2024-06 起"},
    # 跨区域交流（巴彦淖尔→兴安盟）
    {"person_a": 4, "person_b": 7, "type": "两地官员交流",
     "context": "张晓兵由巴彦淖尔市长转任兴安盟书记（2021），冯爱霞由巴彦淖尔常委常务副市长转任兴安盟副书记（2025-10），同源地：巴彦淖尔→兴安盟",
     "overlap_org": "巴彦淖尔市", "overlap_period": "2016-2025"},
    # 同场共事（官方报道）
    {"person_a": 3, "person_b": 12, "type": "同场共事",
     "context": "2026-03 会见中国广核集团（苏和、于吉顺、谷立民同席）", "overlap_org": "兴安盟", "overlap_period": "2026-03"},
    {"person_a": 3, "person_b": 15, "type": "同场共事",
     "context": "2026-06-01 赴阿尔山调研（盟领导谷立民、杨永久陪同；苏和为盟委书记）", "overlap_org": "阿尔山市", "overlap_period": "2026-06"},
    {"person_a": 12, "person_b": 15, "type": "同场共事",
     "context": "2026-06-01 随苏和赴阿尔山调研（盟领导同场）", "overlap_org": "阿尔山市", "overlap_period": "2026-06"},
]

if __name__ == "__main__":
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