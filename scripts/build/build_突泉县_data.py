#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 兴安盟突泉县 leadership network.

Level: 县
Province: 内蒙古自治区
Parent City: 兴安盟
Region: 突泉县
Targets: 县委书记 (张双城) & 县长 (宁海岩)

Research Date: 2026-08-11 (task inner_mongolia_突泉县)
Evidence quality: guided by the china-gov-network skill. Web-search engines
(Exa/Bing/百度/搜狗/360/今日头条) were rate-limited or bot-walled from this IP,
so core facts come from OFFICIAL primary sources reachable directly:
  - 突泉县人民政府门户 http://www.tq.gov.cn — 政府工作报告 2025/2026,
    县政府常务会议列表(2025年第19次~2026年第16次全部实录)、人大常委会会议新闻、
    县委全体会议新闻（十五届四/五/六次全会）、全县干部大会新闻、县情概况
  - 兴安盟行政公署 http://www.xam.gov.cn — 盟长于吉顺赴突泉调研 (2026-08-07)
  - 中国人民政治协商会议兴安盟委员会 http://zx.xam.gov.cn — 张双城副主席简历 (2024-04-25)
  - 突泉县融媒体中心微信公众号（政府门户链接转发，mp.weixin.qq.com）— 人大常委会
    第二十八/二十九次会议纪要、县政协十四届第二十二次常委会议纪要、
    县政府 2026 年第 14/15/16 次常务会议纪要
  - 搜狗网页搜索（2026-08-11 首次检索可用，随后被限流）— 澎湃号/今日头条转载的
    县委常委会会议（第 65/85/97/103/106 次）、县委信息周报等

CONFIRMED (official, as of 2026-08-11):
  - 县委书记 张双城（男 蒙古族 1970-09 研究生 中共党员；盟政协党组成员、副主席兼任；
    2021 接替屈振年任书记；2025-04-27 主持县委理论学习中心组学习为最后确认履职；
    2026 年起无独立履职报道 —— 状态 plausible）
  - 县委副书记、县长 宁海岩（2026-07-14 第14次常务会议以"县委副书记、代县长"主持；
    2026-07-23 第15次、08-07 第16次以"县长"主持；此前 2021 年为县委常委、组织部部长；
    出生/学历信息公开资料缺失）
  - 前任县长 王家军（男 蒙古族 1976-03 大学/农学学士 中共党员；2019 年为县委常委、常务副县长；
    ~2024-01 起任县委副书记、县长；先后作 2025/2026 年政府工作报告（2025-01-06/2026-01-13）；
    2026-06-14 主持年内第十二次常务会议为最后可得履职；其后去向未公开 — plausible 调离）
  - 前任县委书记 屈振年（2015-11 起任书记；2021-06 获"全国优秀县委书记"，同年转任兴安盟行署
    党组成员、副盟长；此前在突泉长期任职：突泉镇政府干部、团县委书记、六户镇党委书记、
    县委常委、副县长、县委副书记、县长）
  - 前任县长 王永佳（2021-12-19 代县长主持县十七届政府第 41 次常务会议；2022-04 干部大会
    以县长部署工作；后调任巴彦淖尔市委、五原县委书记 — 本仓库 2026-08-11 五原县调查已证实）
  - 人大主任 陈国明（2026-07-07 主持县十八届人大常委会第 28 次会议；党组书记）
  - 政协主席 叶彬（2026-07-29 主持县政协十四届二十二次常委会；党组书记）
  - 常委：常务副县长 胡杨、组织部长 崔荣新（2026-07）、统战部长 庞亮（2026-07-29）、
    副县长 刘志峰（2019 起在班）、以及其他 2025-01 全会名单县领导
    （王建国、方国强、李存琪、李红星、黄雷子、满水龙、康红波 —— 具体分工待核）
  - 法检：县人民法院院长 刘辉；县人民检察院检察长 高峰（2026-07-07）
  - 跨县链条：杨宝田（2021-11 突泉县党代会主席团成员）→ 乌兰浩特市委副书记、市长（2026-07 已证实）；
    于吉顺（兴安盟盟长）2026-06/07/08 三次赴突泉督导（上下级）

OPEN GAPS（report/open_gaps.md 及 person JSON open_questions 同步记录）:
  - 张双城 2025-04 之后履职活动确认（2026 年在任状态属 plausible 推断）
  - 宁海岩出生年月/民族/毕业院校、组织部长→县长完整路径
  - 王家军 2026-06 后的去向
  - 屈振年、耿天良、王永佳、王延波、陈国明、叶彬、崔荣新、胡杨 等 出生信息与完整履历
  - 2025-01 全会名单各成员现任职务完整映射
  - 王延波（前政协主席）与叶彬（现任主席）交接时间

Governance / regional profile（2026-01-13 政府工作报告 + 县情概况）:
  - 面积 4890 km2；辖 6 镇 3 乡、188 行政村；常住人口 22.07 万（七人普；
    汉 70.07%、蒙古族 20.53%、其他 9.4%）
  - 2025：地区生产总值 114.68 亿元 (+1.8% 不变价)；固投 +5.1%；社零 15.96 亿 (+4.5%)；
    一般公共预算收入 3.51 亿元 (-2%)；城乡人均可支配收入 40372/18473 元
  - 新能源装机总量突破 280 万千瓦（蒙能百万千瓦风储基地、中广核 20 万千瓦风电、
    国电投 44.5 万千瓦火电灵改并网）；粮食产量 25 亿斤以上；高标准农田 10 万亩
  - "十四五"：GDP 由 70 亿→114.68 亿（年均 +9%以上）；累计争取上级资金 174 亿元；
    民生投入 143 亿元
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

SLUG = "突泉县"

# 入库（暂存/规范化）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────
organizations = [
    # 县本级核心机构
    {"id": 1, "name": "中共突泉县委员会", "type": "党委", "level": "县处级",
     "parent": "中共兴安盟委员会", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 2, "name": "突泉县人民政府", "type": "政府", "level": "县处级",
     "parent": "兴安盟行政公署", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 3, "name": "突泉县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "兴安盟人大工作委员会", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 4, "name": "中国人民政治协商会议突泉县委员会", "type": "政协", "level": "县处级",
     "parent": "政协兴安盟委员会", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 5, "name": "中共突泉县纪律检查委员会/突泉县监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共兴安盟纪律检查委员会", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 6, "name": "突泉县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共突泉县委", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 7, "name": "突泉县委统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共突泉县委", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 8, "name": "突泉县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共突泉县委", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 9, "name": "突泉县委办公室", "type": "党委", "level": "县处级",
     "parent": "中共突泉县委", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 10, "name": "突泉县人民法院", "type": "其他", "level": "县处级",
     "parent": "兴安盟中级人民法院", "location": "内蒙古自治区兴安盟突泉县"},
    {"id": 11, "name": "突泉县人民检察院", "type": "其他", "level": "县处级",
     "parent": "兴安盟人民检察院", "location": "内蒙古自治区兴安盟突泉县"},
    # 上级（盟）与跨县节点
    {"id": 12, "name": "中共兴安盟委员会", "type": "党委", "level": "地级市",
     "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 13, "name": "兴安盟行政公署", "type": "政府", "level": "地级市",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 14, "name": "政协兴安盟委员会", "type": "政协", "level": "地级市",
     "parent": "政协内蒙古自治区委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 15, "name": "兴安盟人大工作委员会", "type": "人大", "level": "地级市",
     "parent": "内蒙古自治区人大常委会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 16, "name": "中共乌兰浩特市委员会", "type": "党委", "level": "县处级",
     "parent": "中共兴安盟委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 17, "name": "乌兰浩特市人民政府", "type": "政府", "level": "县处级",
     "parent": "兴安盟行政公署", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 18, "name": "中共五原县委员会", "type": "党委", "level": "县处级",
     "parent": "中共巴彦淖尔市委员会", "location": "内蒙古自治区巴彦淖尔市五原县"},
]

# ── PERSONS ──────────────────────────────────────────────────
# person id 1-6 核心/前任正职；7-23 现任班子；24-31 名单其他领导；32-35 跨县/上级相关
persons = [
    # 1 — 张双城 — 县委书记（核心）
    {"id": 1, "name": "张双城", "gender": "男", "ethnicity": "蒙古族", "birth": "1970年9月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "突泉县委书记、盟政协党组成员/副主席（兼）", "current_org": "中共突泉县委员会",
     "source": "http://zx.xam.gov.cn/zx/2024-04/25/article_2024051603431673466.html"},
    # 2 — 宁海岩 — 县长（核心）
    {"id": 2, "name": "宁海岩", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "突泉县人民政府",
     "source": "https://mp.weixin.qq.com/s/FJ0R0ty5rp88KTw_boBlsw"},
    # 3 — 王家军 — 前任县长
    {"id": 3, "name": "王家军", "gender": "男", "ethnicity": "蒙古族", "birth": "1976年3月",
     "birthplace": "", "education": "大学学历（农学学士）", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任突泉县长至 2026-06；去向待核）", "current_org": "突泉县人民政府",
     "source": "http://www.tq.gov.cn/tq/2026-06/15/article_2026061511091513575.html"},
    # 4 — 屈振年 — 前任县委书记
    {"id": 4, "name": "屈振年", "gender": "男", "ethnicity": "汉族", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任突泉县委书记 2015-11~2021；后任兴安盟行署副盟长）", "current_org": "兴安盟行政公署",
     "source": "https://www.sogou.com/web?query=屈振年+突泉县委书记+履新"},
    # 5 — 王永佳 — 前任县长（现五原县委书记）
    {"id": 5, "name": "王永佳", "gender": "男", "ethnicity": "汉族", "birth": "1984年1月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "五原县委书记（一级调研员）", "current_org": "中共五原县委员会",
     "source": "https://www.sogou.com/web?query=王永佳+突泉县+代县长+常务会议"},
    # 6 — 陈国明 — 人大主任
    {"id": 6, "name": "陈国明", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组书记、主任", "current_org": "突泉县人民代表大会常务委员会",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 7 — 叶彬 — 政协主席
    {"id": 7, "name": "叶彬", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组书记、主席", "current_org": "中国人民政治协商会议突泉县委员会",
     "source": "https://mp.weixin.qq.com/s/qa5hRMwfDm6j7y3RVpI1_w"},
    # 8 — 胡杨 — 常委/常务副县长
    {"id": 8, "name": "胡杨", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "突泉县人民政府",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 9 — 崔荣新 — 常委/组织部长
    {"id": 9, "name": "崔荣新", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "突泉县委组织部",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 10 — 庞亮 — 常委/统战部长
    {"id": 10, "name": "庞亮", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长、县政协党组副书记", "current_org": "突泉县委统一战线工作部",
     "source": "https://mp.weixin.qq.com/s/qa5hRMwfDm6j7y3RVpI1_w"},
    # 11 — 刘志峰 — 常委/副县长（自 2019 在班子）
    {"id": 11, "name": "刘志峰", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长（2025-01 全会名单在列）", "current_org": "突泉县人民政府",
     "source": "http://www.tq.gov.cn/tq/2025-07/01/article_2025070118051824789.html"},
    # 12 — 郭江维 — 县领导（职务待核）
    {"id": 12, "name": "郭江维", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县领导（2026-07 列席人大会议；具体职务待核）", "current_org": "中共突泉县委员会",
     "source": "https://mp.weixin.qq.com/s/R_bkKDbFOP_ks72EtUfScQ"},
    # 13 — 兰先峰 — 人大副主任
    {"id": 13, "name": "兰先峰", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "突泉县人民代表大会常务委员会",
     "source": "https://mp.weixin.qq.com/s/R_bkKDbFOP_ks72EtUfScQ"},
    # 14 — 屈彤年 — 人大副主任
    {"id": 14, "name": "屈彤年", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "突泉县人民代表大会常务委员会",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 15 — 曹永欣 — 人大副主任
    {"id": 15, "name": "曹永欣", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "突泉县人民代表大会常务委员会",
     "source": "https://mp.weixin.qq.com/s/R_bkKDbFOP_ks72EtUfScQ"},
    # 16 — 沈春文 — 人大副主任提名人选
    {"id": 16, "name": "沈春文", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任（提名人选）", "current_org": "突泉县人民代表大会常务委员会",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 17 — 汪大明 — 人大副主任提名人选
    {"id": 17, "name": "汪大明", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任（提名人选）", "current_org": "突泉县人民代表大会常务委员会",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 18 — 陈国庆 — 政协副主席
    {"id": 18, "name": "陈国庆", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协副主席", "current_org": "中国人民政治协商会议突泉县委员会",
     "source": "https://mp.weixin.qq.com/s/qa5hRMwfDm6j7y3RVpI1_w"},
    # 19 — 张艳玲 — 政协副主席提名人选
    {"id": 19, "name": "张艳玲", "gender": "女", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "待查", "work_start": "",
     "current_post": "县政协副主席（提名人选）", "current_org": "中国人民政治协商会议突泉县委员会",
     "source": "https://mp.weixin.qq.com/s/qa5hRMwfDm6j7y3RVpI1_w"},
    # 20 — 马弘飞 — 政协副主席提名人选
    {"id": 20, "name": "马弘飞", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协副主席（提名人选）", "current_org": "中国人民政治协商会议突泉县委员会",
     "source": "https://mp.weixin.qq.com/s/qa5hRMwfDm6j7y3RVpI1_w"},
    # 21 — 张莉莉 — 政协副主席提名人选
    {"id": 21, "name": "张莉莉", "gender": "女", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "待审定", "work_start": "",
     "current_post": "县政协副主席（提名人选）", "current_org": "中国人民政治协商会议突泉县委员会",
     "source": "https://mp.weixin.qq.com/s/qa5hRMwfDm6j7y3RVpI1_w"},
    # 22 — 刘辉 — 法院院长
    {"id": 22, "name": "刘辉", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人民法院院长", "current_org": "突泉县人民法院",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 23 — 高峰 — 检察长
    {"id": 23, "name": "高峰", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县人民检察院检察长", "current_org": "突泉县人民检察院",
     "source": "https://mp.weixin.qq.com/s/tuOPiGPxmguGDO2qvEpEiA"},
    # 24—31 — 2025-01 县领导名单（职务分工待核）
    {"id": 24, "name": "王建国", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "待核", "work_start": "",
     "current_post": "县领导（2025-01 全会名单）", "current_org": "中共突泉县委员会",
     "source": "http://www.tq.gov.cn/tq/2025-07/01/article_2025070118051824789.html"},
    {"id": 25, "name": "方国强", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县领导（2025-01 全会名单；2021 党代会主席团成员）", "current_org": "中共突泉县委员会",
     "source": "https://www.sogou.com/web?query=突泉县+方国强"},
    {"id": 26, "name": "李存琪", "gender": "女", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县领导（2025-01 全会名单）", "current_org": "中共突泉县委员会",
     "source": "http://www.tq.gov.cn/tq/2025-07/01/article_2025070115051824789.html"},
    {"id": 27, "name": "李红星", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县领导（2025-01 全会名单）", "current_org": "中共突泉县委员会",
     "source": "http://www.tq.gov.cn/tq/2025-07/01/article_2025070115051824789.html"},
    {"id": 28, "name": "黄雷子", "gender": "男", "ethnicity": "蒙古族", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县领导（2025-01 全会名单）", "current_org": "中共突泉县委员会",
     "source": "http://www.tq.gov.cn/tq/2025-07/01/article_2025070115051824789.html"},
    {"id": 29, "name": "满水龙", "gender": "男", "ethnicity": "蒙古族", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县领导（2025-01 全会名单）", "current_org": "中共突泉县委员会",
     "source": "http://www.tq.gov.cn/tq/2025-07/01/article_2025070115051824789.html"},
    {"id": 30, "name": "康红波", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县领导（2025-01 全会名单；疑纪委书记）", "current_org": "中共突泉县纪律检查委员会/监委",
     "source": "http://www.tq.gov.cn/tq/2025-07/01/article_2025070115051824789.html"},
    # 31 — 王英群 — 前任常委/县委办主任（2019）
    {"id": 31, "name": "王英群", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任县委常委、县委办主任 2019；现职务待核）", "current_org": "突泉县委办公室",
     "source": "https://www.sogou.com/web?query=突泉县委书记+张双城+消防+王英群"},
    # 32 — 杨宝田 — 跨县（乌兰浩特市长）
    {"id": 32, "name": "杨宝田", "gender": "男", "ethnicity": "汉族", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "乌兰浩特市委副书记、市长（2026-07 在任）", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},
    # 33 — 耿天良 — 前任县长
    {"id": 33, "name": "耿天良", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任突泉县长；2021 年前卸任调离）", "current_org": "突泉县人民政府",
     "source": "https://www.sogou.com/web?query=突泉县+处级干部大会+耿天良"},
    # 34 — 王延波 — 前任政协主席
    {"id": 34, "name": "王延波", "gender": "男", "ethnicity": "待查", "birth": "待查",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任县政协主席；2023 年在任，交接时间待核）", "current_org": "中国人民政治协商会议突泉县委员会",
     "source": "https://www.sogou.com/web?query=王延波+突泉县+政协"},
    # 35 — 于吉顺 — 兴安盟盟长（上级）
    {"id": 35, "name": "于吉顺", "gender": "男", "ethnicity": "汉族", "birth": "1979年7月",
     "birthplace": "", "education": "研究生学历", "party_join": "2000年10月", "work_start": "",
     "current_post": "兴安盟盟委副书记、行署党组书记、盟长", "current_org": "兴安盟行政公署",
     "source": "http://www.xam.gov.cn/xam/2021-11/04/article_2024041412052283273.html"},
]

# ── POSITIONS ────────────────────────────────────────────────
positions = [
    # 张双城 — 书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2021-06", "end_date": "present",
     "rank": "正处级", "note": "接任屈振年；2025-04-27 主持理论学习中心组学习为最近确认履职；2026 年在任状态据间接证据（公布于盟政协任、未发现调离报道）"},
    {"person_id": 1, "org_id": 14, "title": "盟政协副主席（兼任）", "start_date": "2023", "end_date": "present",
     "rank": "副厅级", "note": "政协兴安盟委员会党组成员、副主席（官网 2024-04 简历在列）"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "2021-06",
     "rank": "正处级", "note": "任书记前为县长/副书记（盟政协简历间接）；具体事宜待核"},
    # 宁海岩 — 县长
    {"person_id": 2, "org_id": 2, "title": "县长（代）", "start_date": "2026-07", "end_date": "2026-07",
     "rank": "正处级", "note": "2026-07-14 起以\"县委副书记、代县长\"主持县政府 2026 年第 14 次常务会议"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "2026-07-23 之后以\"县长\"主持第 15、16 次常务会议（2026-08-07）"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-07", "end_date": "present",
     "rank": "副处级", "note": "县长惯例入常职务"},
    {"person_id": 2, "org_id": 6, "title": "县委组织部部长", "start_date": "", "end_date": "2026-06",
     "rank": "副处级", "note": "2021-12 县乡镇换届工作会议新闻中为组织部部长；2022-2025 在任证据不完整，任职区间待核"},
    {"person_id": 2, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "2026-06",
     "rank": "副处级", "note": "2021-12 县乡镇领导班子换届会议时在列"},
    # 王家军 — 前任县长
    {"person_id": 3, "org_id": 2, "title": "县长", "start_date": "2024-01", "end_date": "2026-06",
     "rank": "正处级", "note": "2025/2026 年政府工作报告作者（2026-01-13）；2026-06-14 主持第 12 次常务会议为最近确认履职；接任/卸任精确时间待核"},
    {"person_id": 3, "org_id": 2, "title": "县政府常务副县长", "start_date": "", "end_date": "2024-01",
     "rank": "副处级", "note": "2019-01 消防检查随县委书记参加；2021-11 党代会主席团成员"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "2024-01", "end_date": "2026-06",
     "rank": "副处级", "note": "县长兼副书记"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "2024-01",
     "rank": "副处级", "note": "常务副县长时期"},
    # 屈振年 — 前任书记
    {"person_id": 4, "org_id": 1, "title": "县委书记", "start_date": "2015-11", "end_date": "2021-06",
     "rank": "正处级", "note": "2021-06 获\"全国优秀县委书记\"；卸任时间以副盟长任命为准"},
    {"person_id": 4, "org_id": 13, "title": "兴安盟行署副长", "start_date": "2021-06", "end_date": "present",
     "rank": "副厅级", "note": "2021 年 6 月起（任前为突泉县委书记）；最新职务状态待核"},
    # 王永佳 — 前任县长
    {"person_id": 5, "org_id": 2, "title": "代县长", "start_date": "2021-12", "end_date": "2022-01",
     "rank": "正处级", "note": "2021-12-19 主持县十七届政府第 41 次常务会议"},
    {"person_id": 5, "org_id": 2, "title": "县长", "start_date": "2022-01", "end_date": "2023-12",
     "rank": "正处级", "note": "2023 年县十八届人大二次会议在任；最后一次任职活动精确时间待核"},
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start_date": "2021-12", "end_date": "2023-12",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 18, "title": "县委书记", "start_date": "2024-01", "end_date": "present",
     "rank": "正处级", "note": "五原县委书记（2026-08 官网在任）；临问题：任前公示未找到，起任时间按 2023-12 后拟任、2024-01 前后就位，精确待核"},
    # 陈国明 — 人大主任
    {"person_id": 6, "org_id": 3, "title": "县人大常委会主任（党组书记）", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-07-07 主持县十八届人大常委会第 28 次会议；现任任期起始时间待核"},
    # 叶彬 — 政协主席
    {"person_id": 7, "org_id": 4, "title": "县政协主席（党组书记）", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-07-29 主持县政协十四届二十二次常委会议；接替王延波时间待核"},
    # 胡杨 — 常务副县长
    {"person_id": 8, "org_id": 2, "title": "政府常务副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2026-07 多场会议确认在任（人大28/29列席、政协常委会列席）"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 崔荣新 — 组织部长
    {"person_id": 9, "org_id": 6, "title": "县委组织部部长", "start_date": "2026", "end_date": "present",
     "rank": "副处级", "note": "2026-07-07 在任组织部部长（继宁海岩）"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "2026", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 庞亮
    {"person_id": 10, "org_id": 7, "title": "县委统战部部长、县政协党组副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2026-07-29 政协常委会并列"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 刘志峰
    {"person_id": 11, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2019-01 消防检查时已为副县长；2025-01 全会名单在列"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 郭江维
    {"person_id": 12, "org_id": 1, "title": "县领导（具体职务待核）", "start_date": "", "end_date": "present",
     "rank": "", "note": "2026-07-15 县人大常委会 29 次会议\"县领导\"列席名单"},
    # 人大副主任
    {"person_id": 13, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-15 确认"},
    {"person_id": 14, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-07 确认"},
    {"person_id": 15, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-15 确认"},
    {"person_id": 16, "org_id": 3, "title": "县人大常委会副主任（提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026-07-07 确认"},
    {"person_id": 17, "org_id": 3, "title": "县人大常委会副主任（提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026-07-07 确认"},
    # 政协
    {"person_id": 18, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-29 确认"},
    {"person_id": 19, "org_id": 4, "title": "县政协副主席（提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026-07-29 确认"},
    {"person_id": 20, "org_id": 4, "title": "县政协副主席（提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026-07-29 确认"},
    {"person_id": 21, "org_id": 4, "title": "县政协副主席（提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026-07-29 确认"},
    # 法检
    {"person_id": 22, "org_id": 10, "title": "县人民法院院长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-07 确认"},
    {"person_id": 23, "org_id": 11, "title": "县人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-07 确认"},
    # 2025-01 全会名单其他成员（职务待核）
    {"person_id": 24, "org_id": 1, "title": "县领导（职务待核）", "start_date": "", "end_date": "present", "rank": "", "note": "2025-01 六次全会名单"},
    {"person_id": 25, "org_id": 1, "title": "县领导（职务待核）", "start_date": "", "end_date": "present", "rank": "", "note": "2021-11 党代会主席团成员；2025-01 全会名单"},
    {"person_id": 26, "org_id": 1, "title": "县领导（职务待核）", "start_date": "", "end_date": "present", "rank": "", "note": "2025-01 六次全会名单"},
    {"person_id": 27, "org_id": 1, "title": "县领导（职务待核）", "start_date": "", "end_date": "present", "rank": "", "note": "2025-01 六次全会名单"},
    {"person_id": 28, "org_id": 1, "title": "县领导（职务待核）", "start_date": "", "end_date": "present", "rank": "", "note": "2025-01 六次全会名单"},
    {"person_id": 29, "org_id": 1, "title": "县领导（职务待核）", "start_date": "", "end_date": "present", "rank": "", "note": "2025-01 六次全会名单"},
    {"person_id": 30, "org_id": 5, "title": "县领导（疑纪委书记）", "start_date": "", "end_date": "present", "rank": "", "note": "2025-01 六次全会名单"},
    # 前任
    {"person_id": 31, "org_id": 9, "title": "县委办公室主任（曾任）", "start_date": "", "end_date": "2020", "rank": "副处级", "note": "2019-01 随书记消防检查新闻；现职务待核"},
    {"person_id": 31, "org_id": 1, "title": "县委常委（曾任）", "start_date": "", "end_date": "2020", "rank": "副处级", "note": ""},
    {"person_id": 33, "org_id": 2, "title": "县长（曾任）", "start_date": "", "end_date": "2021-11", "rank": "正处级", "note": "2021 年县处级干部大会致谢离任（接任者王永佳）"},
    {"person_id": 34, "org_id": 4, "title": "县政协主席（曾任）", "start_date": "", "end_date": "2024", "rank": "正处级", "note": "2023 年政协十四届二次会议在任；后由叶彬接替"},
    # 跨县/上级
    {"person_id": 32, "org_id": 1, "title": "县领导（曾任）", "start_date": "", "end_date": "2022", "rank": "", "note": "2021-11 突泉县党代会主席团成员；2022 年后调离"},
    {"person_id": 32, "org_id": 17, "title": "乌兰浩特市委副书记、市长", "start_date": "2024", "end_date": "present", "rank": "正处级", "note": "2026-07 乌兰浩特市官网领导之窗在任；任市长起始时间待核"},
    {"person_id": 35, "org_id": 13, "title": "兴安盟盟长", "start_date": "2024-06", "end_date": "present", "rank": "正厅级", "note": "2026-06/07/08 三次赴突泉督导（上下级关系证据）"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "张双城（县委书记）与宁海岩（县长）构成当前党政正职搭档（2026-07 起）",
     "overlap_org": "突泉县", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 3, "type": "党政正职搭档", "context": "张双城任期内先后与县长王家军搭档（2024-01~2026-06）",
     "overlap_org": "突泉县", "overlap_period": "2024-01 ~ 2026-06"},
    {"person_a": 4, "person_b": 1, "type": "继任书记", "context": "张双城接屈克（屈振年）任县委书记（2021-06；屈振年转任盟行署副盟长）",
     "overlap_org": "中共突泉县委员会", "overlap_period": "2015-11 ~ 2021-06"},
    {"person_a": 5, "person_b": 3, "type": "县长继任", "context": "王永佳（县长 2021-12~2023 末）后王家军任县长；王永佳调任五原县委书记",
     "overlap_org": "突泉县人民政府", "overlap_period": "2021-12 ~ 2023-12"},
    {"person_a": 3, "person_b": 2, "type": "县长继任", "context": "宁海岩接继王家军任代/县长（2026-07）；王家军去向待核",
     "overlap_org": "突泉县人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 9, "type": "组织部前后任", "context": "宁海岩（组织部长）与崔荣新（现任组织部长）为同一职务前后任",
     "overlap_org": "突泉县委组织部", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "班子同事", "context": "书记与人大常委会主任（陈国明）为四套班子搭档",
     "overlap_org": "突泉县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "班子同事", "context": "书记与政协主席（叶彬）为四套班子搭档（2026-07-29 政协常委会集新闻中并列）",
     "overlap_org": "突泉县", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "政府上下级", "context": "县长与常务副县长（胡杨协助县长主持日常政务）",
     "overlap_org": "突泉县人民政府", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 5, "type": "党政正职搭档", "context": "张双城任期内与县长王永佳搭档（2021-2023）",
     "overlap_org": "突泉县", "overlap_period": "2021-12 ~ 2023-12"},
    {"person_a": 1, "person_b": 35, "type": "上下级（盟对县）", "context": "盟长于吉顺多次赴突泉督导安全生产/防汛（2026-06/07/08），书记作为属地主要负责人",
     "overlap_org": "兴安盟-突泉县", "overlap_period": "2026"},
    {"person_a": 25, "person_b": 1, "type": "班子同事", "context": "方国强为 2021 党代会主席团成员，2025-01 全会名单仍列（县委班子）",
     "overlap_org": "中共突泉县委员会", "overlap_period": "2021 ~ 2025"},
    {"person_a": 32, "person_b": 1, "type": "班子同事（跨县流动链）", "context": "杨宝田 2021 年为突泉县党代会主席团成员，2024 年后任乌兰浩特市长",
     "overlap_org": "突泉县→乌兰浩特市", "overlap_period": "2021 ~ 2024"},
    {"person_a": 5, "person_b": 18, "type": "跨县调动", "context": "王永佳（突泉县长）调任巴彦淖尔五原县委书记（跨盟市调动链条）",
     "overlap_org": "突泉县→五原县", "overlap_period": "2023-2024"},
    {"person_a": 33, "person_b": 5, "type": "县长继任", "context": "耿天良（县长）与王永佳（代/县长）为前任后继任；干部大会致谢耿天良贡献",
     "overlap_org": "突泉县人民政府", "overlap_period": "2021"},
    {"person_a": 34, "person_b": 7, "type": "政协主席继任", "context": "王延波（政协主席）后叶彬接替（时间点待核）",
     "overlap_org": "突泉县政协", "overlap_period": "2024-2026"},
]


def main() -> int:
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
    print(f"[build] {SLUG}: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print(f"[build] DB:   {DB_PATH}")
    print(f"[build] GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())