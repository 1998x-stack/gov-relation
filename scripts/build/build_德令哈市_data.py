#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 德令哈市 (Delingha City),
海西蒙古族藏族自治州 (Haixi Prefecture), 青海省 (Qinghai Province).

Task ID: qinghai_德令哈市
Level: 县级市 (州府所在地)
Targets: 市委书记 & 市长
Investigation date: 2026-08-07
Confidence basis: 官方一手来源 www.delingha.gov.cn (德令哈市人民政府网站, 直接抓取)
  —— 中国共产党德令哈市第十次代表大会(2026-07-10 开幕) + 第十届市委一次全会(2026-07-11)
  选举产生新一届市委班子; 市第十届人大一次会议(2026-07-21~23)选举市长、人大主任等;
  市"领导之窗/领导介绍"下属 市委领导/市政府领导/市人大领导/市政协领导 四栏官方个人简介
  (含出生年月、学历、职责分工), 均已直接抓取确认。

CURRENT OFFICEHOLDERS (2026-07 换届后, confirmed):
  - 市委书记: 王大磊 (州委常委、德令哈市委书记; 1982-04 生, 汉族, 理学博士; 连任——此前为九届书记)
  - 市长: 赵兴荣 (海西州政府党组成员、副州长 兼 德令哈市委副书记、市长; 1980-10 生, 汉族, 大学;
    2026-07 前为"副州长、市委副书记、市政府党组书记、代市长", 2026-07-23 市十届人大一次会议当选市长)

SUCCESSION:
  - 市委常委会: 王大磊主持, 连任书记 (九届→十届)
  - 市人大常委会: 叶万福 任 党组书记、主任 (十届); 前任 向阳 (九届)
  - 市政府市长: 赵兴荣 接任; 其兼任州政府副州长, 属"州府副职兼市府正职"的特殊安排
  - 市政协: 金泽宇 任 党组书记、主席 (十届)

NOTES:
  - 搜索渠道 (Exa/Baidu/Jina/Bing/360) 均被限或需 JS, 无法获取 王大磊/赵兴荣 的任职前完整履历
    (出生年月、学历层级已由官方简介确认; 但何时到德令哈、之前何职 等简历链待补)。
  - 官方"领导之窗"个人简介页 (info/1013,1423,1424,1425) 提供身分与职责的一手基础信息。
  - 未确认的简历链断口 一律以 confidence=unverified / open_questions 显式标注, 不臆造。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "德令哈市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_德令哈市"
if _CURRENT_DIR.name == "qinghai_德令哈市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────
persons = [
    # ═══ 市委书记 (Party Secretary) & 市长 ═══
    {
        "id": 1,
        "name": "王大磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "研究生学历, 理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海西州委常委、德令哈市委书记",
        "current_org": "中共海西蒙古族藏族自治州委员会/中共德令哈市委员会",
        "source": "德令哈市人民政府网站 领导之窗-市委领导 王大磊同志简介及分工(2025-12-03). www.delingha.gov.cn/info/1013/135818.htm",
    },
    {
        "id": 2,
        "name": "赵兴荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海西州人民政府党组成员、副州长; 德令哈市委副书记、市长",
        "current_org": "海西州人民政府/德令哈市人民政府",
        "source": "德令哈市人民政府网站 领导之窗 赵兴荣简介及分工(2026-07-23). 市十届人大一次会议(2026-07-23)当选市长. delingha.gov.cn/info/1013/143388.htm",
    },
    # ═══ 新一届市委副书记/常委 ═══
    {
        "id": 3,
        "name": "陈政和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委副书记",
        "current_org": "中共德令哈市委员会",
        "source": "领导之窗-市委领导 陈政和简介(2026-06-22). delingha.gov.cn/info/1013/142072.htm",
    },
    {
        "id": 4,
        "name": "韩明雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-12",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委副书记",
        "current_org": "中共德令哈市委员会",
        "source": "领导之窗·市委领导 韩明雄简介(2026-06-22). delingha.gov.cn/info/1013/142073.htm",
    },
    {
        "id": 5,
        "name": "许晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-01",
        "birthplace": "",
        "education": "在职硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委副书记、市政府党组成员、副市长(援青·浙江)",
        "current_org": "中共德令哈市委员会/德令哈市人民政府",
        "source": "领导之窗 许晓简介及分工(2025-08-06). delingha.gov.cn/info/1013/132996.htm",
    },
    {
        "id": 6,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1985-05",
        "birthplace": "",
        "education": "在职博士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委副书记、市政府党组成员、副市长(援青·国铁集团)",
        "current_org": "中共德令哈市委员会/德令哈市人民政府",
        "source": "领导之窗 张斌简介及分工(2025-08-06). delingha.gov.cn/info/1013/132997.htm",
    },
    {
        "id": 7,
        "name": "张庭栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-03",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委常委、纪委书记、四级高级监察官",
        "current_org": "中共德令哈市纪律检查委员会/德令哈市监察委员会",
        "source": "领导之窗 张庭栋简介(2025-05-09)+市第十届纪委一次全会(2026-07-11, 当选书记). delingha.gov.cn/info/1013/129890.htm",
    },
    {
        "id": 8,
        "name": "刚积德",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1980-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委常委、政法委书记",
        "current_org": "中共德令哈市委政法委员会",
        "source": "领导之窗 刚积德简介(2021-06-21). delingha.gov.cn/info/1013/55057.htm",
    },
    {
        "id": 9,
        "name": "满加",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1974-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委常委、统战部部长、市政协党组副书记、市工商联党组书记",
        "current_org": "中共德令哈市委统战部",
        "source": "领导之窗 满加简介(2021-06-21). delingha.gov.cn/info/1013/55614.htm",
    },
    {
        "id": 10,
        "name": "宋子龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市委常委、人民武装部部长",
        "source": "领导之窗 宋子龙简介(2023-03-22). delingha.gov.cn/info/1013/54961.htm",
    },
    {
        "id": 11,
        "name": "马生辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈工业园(省级)党委书记、管委会主任; 市委常委、市政府党组副书记; 市国资委党委书记、市国资监管委主任",
        "current_org": "德令哈工业园/德令哈市人民政府",
        "source": "领导之窗 马生辉简介(2024-10-24). delingha.gov.cn/info/1423/123392.htm",
    },
    # ═══ 市政府副市长 (党组成员) ═══
    {
        "id": 12,
        "name": "王心慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人民政府党组成员、副市长",
        "current_org": "德令哈市人民政府",
        "source": "领导之窗 王心慧简介(2021-06-22). 分管自然资源/林草/水利/交通/供销. delingha.gov.cn/info/1423/54953.htm",
    },
    {
        "id": 13,
        "name": "肖伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人民政府副市长(分管发改/能源/粮食/文体旅游广电)",
        "current_org": "德令哈市人民政府",
        "source": "领导之窗·援青分工交叉引用('协助肖伟同志分管市发改委/市文体旅游广电局'); 市十届政府换届. delingha.gov.cn",
    },
    {
        "id": 14,
        "name": "陈玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人民政府副市长(分管市工信和科技局/市商务局/市招商局/市教育局)",
        "current_org": "德令哈市人民政府",
        "source": "领导之窗·援青分工辅助引用('协助陈玲同志分管市工信和科技局/市教育局'). delingha.gov.cn",
    },
    {
        "id": 15,
        "name": "王占辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人民政府副市长(分管市农牧局/市乡村振兴局)",
        "current_org": "德令哈市人民政府",
        "source": "领导之窗·援疆分工辅助引用('协助王占辉同志分管市农牧局'). delingha.gov.cn",
    },
    {
        "id": 16,
        "name": "丁映中",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人民政府党组成员、副市长",
        "current_org": "德令哈市人民政府",
        "source": "领导之窗·市政府领导列序(接王心慧之后, 疑似注押/未单列简历). delingha.gov.cn/info/1423 列序",
    },
    # ═══ 市人大 (十届) ═══
    {
        "id": 17,
        "name": "叶万福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人大常委会党组书记、主任",
        "current_org": "德令哈市人民代表大会常务委员会",
        "source": "市十届人大一次会议(2026-07) 主席团常务主席、大会执行主席; 人大代表名单. delingha.gov.cn/info/1040/143303.htm",
    },
    {
        "id": 18,
        "name": "白爱芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人大常委会党组成员、副主任; 市总工会主席",
        "current_org": "德令哈市人民代表大会常务委员会",
        "source": "领导之窗 白爱芬简介(2024-08-26). delingha.gov.cn/info/1424/121437.htm",
    },
    {
        "id": 19,
        "name": "沈利军",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1969-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人大常委会副主任",
        "current_org": "德令哈市人民代表大会常务委员会",
        "source": "领导之窗 沈利军简介(2021-06-22). delingha.gov.cn/info/1424/54963.htm",
    },
    {
        "id": 20,
        "name": "高红",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1971-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市人大常委会副主任",
        "current_org": "德令哈市人民代表大会常务委员会",
        "source": "领导之窗 高红简介(2022-11-18). delingha.gov.cn/info/1424/56767.htm",
    },
    {
        "id": 21,
        "name": "向阳",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1973-08",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前德令哈市人大常委会党组书记、主任(九届, 2026换换届卸任)",
        "current_org": "德令哈市人民代表大会常务委员会",
        "source": "领导之窗 向阳简介(2022-11-18). delingha.gov.cn/info/1424/54962.htm",
    },
    # ═══ 市政协 (十届) ═══
    {
        "id": 22,
        "name": "金泽宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-08",
        "birthplace": "",
        "education": "研究生学历, 经济学硕士(简介未注, 学历以官方为准)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市政协党组书记、主席",
        "current_org": "中国人民政治协商会议德令哈市委员会",
        "source": "政协十届一次会议(2026-07) 当选主席; 领导之窗 金泽宇简介(2026-07-31). delingha.gov.cn/info/1425/143603.htm",
    },
    {
        "id": 23,
        "name": "冶尕措",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1977-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "德令哈市政协副主席、市工商联主席",
        "current_org": "德令哈市政协/德令哈市工商业联合会",
        "source": "领导之窗 冶尕措简介(2021-08-03). delingha.gov.cn/info/1425/58526.htm",
    },
    {
        "id": 24,
        "name": "李吉宁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1977-10",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市政协党组成员、副主席; 市农牧局党组书记、局长",
        "current_org": "德令哈市政协委员会/德令哈市农牧局",
        "source": "领导之窗 李吉宁简介(2026-07-31). delingha.gov.cn/info/1425/143604.htm",
    },
    {
        "id": 25,
        "name": "李积询",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德令哈市政协党组成员、副主席",
        "current_org": "德令哈市政协委员会",
        "source": "领导之窗 李积询简介(2022-06-09). delingha.gov.cn/info/1425/63183.htm",
    },
    # ═══ 市委常委会其余成员 (党代会主席团确认, 具体分工待补) ═══
    {
        "id": 26,
        "name": "杨敏",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市委领导(市十届党代会/人大主席团执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会开幕+/市十届人大一次会议执行主席名单. delingha.gov.cn/info/1040/142776.htm",
    },
    {
        "id": 27,
        "name": "王发元",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(党代会执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会开幕词执行主席. delingha.gov.cn",
    },
    {
        "id": 28,
        "name": "张强",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(党代会执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会开幕词执行主席. delingha.gov.cn",
    },
    {
        "id": 29,
        "name": "景凤",
        "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(党代会执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会开幕词执行主席; 党十届人大会议主席团. delingha.gov.cn",
    },
    {
        "id": 30,
        "name": "樊红红",
        "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(党代会闭幕词执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会闭幕式执行主席. delingha.gov.cn/info/1040/142778.htm",
    },
    {
        "id": 31,
        "name": "青格力",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(党代会闭幕式执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会闭幕式执行主席. delingha.gov.cn",
    },
    {
        "id": 32,
        "name": "李金瑛",
        "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(党代会闭幕式执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会闭幕式执行主席. delingha.gov.cn",
    },
    {
        "id": 33,
        "name": "刘四军",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(党代会闭幕式执行主席)",
        "current_org": "中共德令哈市委员会",
        "source": "市第十次党代会闭幕式执行主席. delingha.gov.cn",
    },
    {
        "id": 34,
        "name": "张新华",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "德令哈市领导(市十届人大主席团常务主席)",
        "current_org": "德令哈市人民代表大会常务委员会",
        "source": "市十届人大一次会议主席团常务主席. delingha.gov.cn/info/1040/143175.htm",
    },
    {
        "id": 35,
        "name": "蒋冬梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-12",
        "birthplace": "四川大英",
        "education": "青海民族学院+省委党校研究生",
        "party_join": "中共党员",
        "work_start": "2001",
        "current_post": "前乌兰县委书记(2021.04-2026.07); 此前曾任德令哈市委副书记(~2018-2020)",
        "current_org": "中共乌兰县委员会(已卸任)",
        "source": "跨区干部交流线索: 蒋冬梅任乌兰县委书记前曾任中共德令哈市委副书记(360百科). 详见 build_乌兰县_data.py (qinghai_乌兰县)",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共德令哈市委员会", "type": "党委", "level": "县级",
     "parent": "中共海西蒙古族藏族自治州委员会", "location": "青海省海西州德令哈市"},
    {"id": 2, "name": "德令哈市人民政府", "type": "政府", "level": "县级",
     "parent": "海西蒙古族藏族自治州人民政府", "location": "青海省海西州德令哈市"},
    {"id": 3, "name": "中共海西蒙古族藏族自治州委员会", "type": "党委", "level": "州级",
     "parent": "中共青海省委", "location": "青海省海西州德令哈市"},
    {"id": 4, "name": "海西蒙古族藏族自治州人民政府", "type": "政府", "level": "州级",
     "parent": "青海省人民政府", "location": "青海省海西州德令哈市"},
    {"id": 5, "name": "德令哈市人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "海西蒙古族藏族自治州人大常委会", "location": "青海省海西州德令哈市"},
    {"id": 6, "name": "中国人民政治协商会议德令哈市委员会", "type": "政协", "level": "县级",
     "parent": "中国人民政治协商会议海西蒙古族藏族自治州委员会", "location": "青海省海西州德令哈市"},
    {"id": 7, "name": "中共德令哈市纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共海西蒙古族藏族自治州纪委", "location": "青海省海西州德令哈市"},
    {"id": 8, "name": "德令哈市监察委员会", "type": "政府", "level": "县级", "parent": "",
     "location": "青海省海西州德令哈市"},
    {"id": 9, "name": "中共德令哈市委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共海西州委政法委员会", "location": "青海省海西州德令哈市"},
    {"id": 10, "name": "中共德令哈市委统战部", "type": "党委", "level": "县级",
     "parent": "中共海西州委统战部", "location": "青海省海西州德令哈市"},
    {"id": 11, "name": "德令哈工业园(省级开发区)", "type": "开发区", "level": "省级",
     "parent": "青海省/海西州", "location": "青海省海西州德令哈市"},
    {"id": 12, "name": "中共德令哈市委组织部", "type": "党委", "level": "县级",
     "parent": "中共德令哈市委员会", "location": "青海省海西州德令哈市"},
    {"id": 13, "name": "德令哈市人民武装部", "type": "事业单位", "level": "县级",
     "parent": "海西州军分区", "location": "青海省海西州德令哈市"},
    {"id": 14, "name": "德令哈市农牧局(市乡村振兴局)", "type": "政府", "level": "县级",
     "parent": "德令哈市人民政府", "location": "青海省海西州德令哈市"},
    {"id": 15, "name": "德令哈市交通运输局", "type": "政府", "level": "县级",
     "parent": "德令哈市人民政府", "location": "青海省海西州德令哈市"},
    {"id": 16, "name": "海西蒙古族藏族自治州人大常委会", "type": "人大", "level": "州级",
     "parent": "青海省人大常委会", "location": "青海省海西州德令哈市"},
    {"id": 17, "name": "中国人民政治协商会议海西蒙古族藏族自治州委员会", "type": "政协", "level": "州级",
     "parent": "青海省政协", "location": "青海省海西州德令哈市"},
    {"id": 18, "name": "德令哈市工商业联合会(总商会)", "type": "群团", "level": "县级",
     "parent": "德令哈市委/海西州工商联", "location": "青海省海西州德令哈市"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 书记 & 市长
    {"person_id": 1, "org_id": 1, "title": "海西州委常委、德令哈市委书记", "start_date": "九届(连任)", "end_date": "present", "rank": "副厅级(州委常委)",
     "note": "2026-07 十届市委一次全会 王大磊受主席团委托主持并受选连任; 2026 前为九届州委常委/书记. 主持市委全面工作."},
    {"person_id": 2, "org_id": 2, "title": "德令哈市委副书记、市长", "start_date": "2026-07-23", "end_date": "present", "rank": "正处级(兼州级副职)",
     "note": "2026-07-23 市十届人大一次会议当选市长; 此前为州政府副州长兼德令哈市委副书记、代市长. 主持市政府全面工作, 分管市审计局."},
    # 市委副书记/常委
    {"person_id": 3, "org_id": 1, "title": "德令哈市委副书记", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "十届市委副书记(2026-07 十届一次全会产生)."},
    {"person_id": 4, "org_id": 1, "title": "德令哈市委副书记", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "十届市委副书记(2026-07)."},
    {"person_id": 5, "org_id": 2, "title": "德令哈市委副书记、市政府党组成员、副市长(援青·浙江)", "start_date": "2025", "end_date": "present", "rank": "副处级",
     "note": "浙江援青干部; 负责浙江对口援青、智慧城市."},
    {"person_id": 6, "org_id": 2, "title": "德令哈市委副书记、市政府党组成员、副市长(援青·国铁集团)", "start_date": "2025", "end_date": "present", "rank": "副处级",
     "note": "国铁集团援青干部; 分管火车站街道."},
    {"person_id": 7, "org_id": 7, "title": "德令哈市委常委、纪委书记、四级高级监察官", "start_date": "十届", "end_date": "present", "rank": "副处级",
     "note": "2026-07-11 市第十届纪委一次全会选举; 受十届党代会主席团委托主持全会."},
    {"person_id": 8, "org_id": 9, "title": "德令哈市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "主持市委政法委全面工作."},
    {"person_id": 9, "org_id": 10, "title": "德令哈市委常委、统战部部长/市政协党组副书记/市工商联党组书记", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "主持统战部全面工作."},
    {"person_id": 10, "org_id": 13, "title": "德令哈市委常委、人民武装部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 11, "title": "德令哈工业园党委书记、管委会主任", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "兼 市委常委、市政府党组副书记、市国资委书记."},
    # 市政府副市长
    {"person_id": 12, "org_id": 2, "title": "德令哈市人民政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "分管自然资源/林草/水利/交通运输/供销."},
    {"person_id": 13, "org_id": 2, "title": "德令哈市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "分管发改/科技/文体旅游广电."},
    {"person_id": 14, "org_id": 2, "title": "德令哈市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "分管工信科技/商务/招商/教育."},
    {"person_id": 15, "org_id": 2, "title": "德令哈市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "分管农牧/乡村振兴."},
    {"person_id": 16, "org_id": 2, "title": "德令哈市人民政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 17, "org_id": 5, "title": "德令哈市人大常委会党组书记、主任", "start_date": "2026-07", "end_date": "present", "rank": "正处级",
     "note": "市十届人大一次会议选举; 主席团常务主席/大会执行主席."},
    {"person_id": 18, "org_id": 5, "title": "德令哈市人大常委会党组成员、副主任; 市总工会主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 5, "title": "德令哈市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 5, "title": "德令哈市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 5, "title": "德令哈市人大常委会主任(九届/前任)", "start_date": "2022", "end_date": "2026-07", "rank": "正处级",
     "note": "九届人大常委会党组书记、主任, 2026年换届卸任."},
    # 政协
    {"person_id": 22, "org_id": 6, "title": "德令哈市政协党组书记、主席", "start_date": "2026-07", "end_date": "present", "rank": "正处级",
     "note": "政协十届一次会议(2026-07)当选主席."},
    {"person_id": 23, "org_id": 18, "title": "德令哈市政协副主席、市工商联主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": "非党员(农工/无党派?)待核."},
    {"person_id": 24, "org_id": 6, "title": "德令哈市政协党组成员、副主席; 市农牧局党组书记、局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 6, "title": "德令哈市政协党组成员、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 其余 主席团成员 (分工待补)
    {"person_id": 26, "org_id": 1, "title": "德令哈市领导(党代会/人大主席团执行主席)", "start_date": "", "end_date": "present", "rank": "",
     "note": "具体之职未在简介中确认."},
    {"person_id": 27, "org_id": 1, "title": "德令哈市领导(党代会执行主席)", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    {"person_id": 28, "org_id": 1, "title": "德令哈市领导(党代会执行主席)", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    {"person_id": 29, "org_id": 5, "title": "德令哈市领导(市人大主席团/党代会执行主席)", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    {"person_id": 30, "org_id": 1, "title": "德令哈市领导(党代会闭幕式执行主席)", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    {"person_id": 31, "org_id": 1, "title": "德令哈市领导(党代会闭幕式执行主席)", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    {"person_id": 32, "org_id": 1, "title": "德令哈市领导(党代会闭幕式执行主席)", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    {"person_id": 33, "org_id": 1, "title": "德令哈市领导(党代会闭幕式执行主席)", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    {"person_id": 34, "org_id": 5, "title": "德令哈市人大主席团常务主席", "start_date": "", "end_date": "present", "rank": "", "note": "分工待补."},
    # 跨区干部 (蒋冬梅) —— 与德令哈的关联
    {"person_id": 35, "org_id": 1, "title": "德令哈市委副书记(曾任)", "start_date": "~2018", "end_date": "2020", "rank": "副处级",
     "note": "任乌兰县委书记前的德令哈市委副书记职务(else百科); 跨区(德令哈→乌兰)干部交流."},
    {"person_id": 35, "org_id": 14, "title": "乌兰县委书记(2021.04-2026.07)", "start_date": "2021-04", "end_date": "2026-07", "rank": "正处级",
     "note": "卸任乌兰书记后去向待补."},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 1. 书记×市长 (核心搭班子)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长搭班子; 十届市委全会(王大磊主持) 与 市十届人大(选赵兴荣为市长) 共成新一届班子",
     "overlap_org": "中共德令哈市委员会/德令哈市人民政府", "overlap_period": "2026-07起"},
    # 2. 书记×人大主任
    {"person_a": 1, "person_b": 17, "type": "overlap",
     "context": "书记与人大主任上前排就座,共同主持换届大会(人大=国家权力机关, 书记报/主任主持)",
     "overlap_org": "德令哈市第十届人民代表大会", "overlap_period": "2026-07"},
    # 3. 书记×纪委书记
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "市委书记对全市纪检工作负主体责任; 张庭栋为市委常委、市纪委书记",
     "overlap_org": "中共德令哈市委员会/市纪委", "overlap_period": "2026-07起"},
    # 4. 市长×人大主任
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "市长在人大作政府工作报告并由人大选举产生(对人大负责)",
     "overlap_org": "德令哈市第十届人民代表大会", "overlap_period": "2026-07"},
    # 5. 书记×政协主席
    {"person_a": 1, "person_b": 22, "type": "superior_subordinate",
     "context": "市委领导政协; 金泽宇任市政协党组书记/主席", "overlap_org": "政协德令哈市委员会", "overlap_period": "2026-07"},
    # 6. 市长×政协主席
    {"person_a": 2, "person_b": 22, "type": "overlap",
     "context": "市长与政协主席同参加全市企业家座谈会(2026-07-30)", "overlap_org": "德令哈市人民政府/市政协", "overlap_period": "2026-07"},
    # 7. 书记×常务副市长马斯辉
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "市委书记与市委常委、市政府党组副书记、市主导建设(工业园)负责人", "overlap_org": "中共德令哈市委员会/德令哈市人民政府", "overlap_period": ""},
    # 8. 市长×常务副市长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长与市政府党组副书记(马生辉)在政府班子中行政层", "overlap_org": "德令哈市人民政府/德令哈工业园", "overlap_period": "2026-07起"},
    # 9. 书记×援青副市长 (浙江/国铁)
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委书记与援青市委副书记/副市长(上下级)", "overlap_org": "中共德令哈市委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "市委书记与援青市委副书记/副市长(上下级)", "overlap_org": "中共德令哈市委员会", "overlap_period": "2025-2026"},
    # 10. 市长×援青副市长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长与援青副市长在政府班子", "overlap_org": "德令哈市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与援青副市长在政府班子", "overlap_org": "德令哈市人民政府", "overlap_period": "2025-2026"},
    # 11. 书记×市委副书记(陈/韩)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记(陈政和)", "overlap_org": "中共德令哈市委员会", "overlap_period": "2026-07起"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与市委副书记(韩明雄)", "overlap_org": "中共德令哈市委员会", "overlap_period": "2026-07起"},
    # 12. 市长×市委副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "市委副书记为政府副县长搭档", "overlap_org": "中共德令哈市委员会", "overlap_period": "2026-07起"},
    # 13. 人大主任×政协主席
    {"person_a": 17, "person_b": 22, "type": "overlap", "context": "人大主任与政协主席同为换届会执行主席(两套班子)", "overlap_org": "德令哈市第十届人大/政协", "overlap_period": "2026-07"},
    # 14. 组织部长(统战×) 满加 与 政协
    {"person_a": 9, "person_b": 22, "type": "overlap", "context": "满加任市政协党组副书记(党委统战+市政协)", "overlap_org": "中共德令哈市委统战部/市政协", "overlap_period": ""},
    # 15. 人大副主任×总工会主席 (白爱芬)
    {"person_a": 18, "person_b": 17, "type": "superior_subordinate", "context": "人大副主任为主任的下级", "overlap_org": "德令哈市人大", "overlap_period": ""},
    # 16. 跨区干部: 蒋冬梅 (曾任德令哈市委副书记 → 乌兰县委书记)
    {"person_a": 35, "person_b": 1, "type": "predecessor_successor",
     "context": "蒋冬梅曾任德令哈市委副书记(~2018-2020), 后转任乌兰县委书记(2021.04), 属跨县干部交流; 未与现任王大重型并任同职",
     "overlap_org": "undirected", "overlap_period": ""},
    # 17. 援青干部同搭手
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "两位援青市委副书记/副市长同搭政府班子(浙江 vs 国铁集团)", "overlap_org": "德令哈市人民政府", "overlap_period": "2025-2026"},
]

# ── Person JSON Builders ───────────────────────────────────────────────
def _common_scope(job: str) -> dict:
    return {
        "province": "青海省",
        "city": "海西蒙古族藏族自治州",
        "region": "德令哈市",
        "job": job,
        "task_id": "qinghai_德令哈市",
        "time_focus": "2021-2026",
    }


def _build_wang_dalei_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _common_scope("市委书记"),
        "identity": {
            "person_id": "qinghai_delingha_wangdalei_1982",
            "name": "王大磊",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1982-04",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "理学博士(研究生学历)", "major": "",
                          "degree": "理学博士", "study_type": "full_time", "source_ids": ["S001", "S100"]}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "王大磊_1982", "name_birthplace": "王大磊_", "official_profile_url": "http://www.delingha.gov.cn/info/1013/135818.htm"},
        },
        "current_status": {
            "current_post": "海西州委常委、德令哈市委书记",
            "current_org": "中共海西蒙古族藏族自治州委员会/中共德令哈市委员会",
            "administrative_rank": "副处级(州委常委兼县委书记级)",
            "as_of": "2026-08-07",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S010", "S011"],
        },
        "career_timeline": [
            {"start": "九届（2021前-）", "end": "present", "org": "中共德令哈市委员会", "title": "海西州委常委、德令哈市委书记",
             "level": "副处级", "location": "青海省海西州德令哈市", "system": "party", "rank": "副处级",
             "is_key_promotion": True, "notes": "九届书记连任十届书记; 十届市委一次全会由他受主席团委托主持并作讲话(2026-07-11).",
             "confidence": "confirmed", "source_ids": ["S001", "S010", "S011"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "notes": "王大磊在任德令哈市委书记前的完整履历(何时入州、州委常委晋升轨迹、任何州级职务)公开资料未找到.",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [
            {"org_id": 1, "org_name": "中共德令哈市委员会", "role": "市委书记", "period": "九届-十届(连任)"},
            {"org_id": 3, "org_name": "中共海西蒙古族藏族自治州委员会", "role": "州委常委", "period": "九届-十届"},
        ],
        "relationships": [
            {"person": "赵兴荣", "person_id": "qinghai_delingha_zhao_xingrong_1980", "relationship_type": "superior_subordinate",
             "strength": "strong", "evidence": "市委全会(王大磊主持)统一换届; 市政府换届由市长赵兴荣作报告, 书记与市长搭班子",
             "overlap_org": "中共德令哈市委员会/德令哈市人民政府", "overlap_period": "2026-07起",
             "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S010", "S011"]},
            {"person": "叶万福", "person_id": "qinghai_delingha_ye_wanfu", "relationship_type": "overlap",
             "strength": "medium", "evidence": "书记与人大主任同在上届大会主席团前排就座/执行主席",
             "overlap_org": "德令哈市第十届人民代表大会", "overlap_period": "2026-07",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
        ],
        "governance_record": [
            {"period": "2026-07-10", "domain": "party", "achievement_or_event": "作市第九次党代会报告并主持新一届市委全会, 完成德令哈市第十届市委班子换届",
             "role_in_event": "市委书记(连任)", "measurable_outcome": "当选十届市委书记, 确立'生态立市/产业强市/民生固市/文化润市'与'5+10+5'产业体系路径",
             "location": "德令哈市", "confidence": "confirmed", "source_ids": ["S010", "S011"]},
        ],
        "professional_profile": {
            "primary_specializations": ["理学(博士)", "县域治理", "党建"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["青海省", "海西州", "德令哈"],
            "promotion_velocity": {"summary": "九届→十届 连任市委书记", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "grassroots_oriented", "evidence": "党代会报告强调生态/民生/正确政绩观, 多次下基层调研并开企业家座谈会", "confidence": "plausible", "source_ids": ["S002", "S010"]}],
            "speech_themes": ["生态立市", "产业强市", "民生固市", "文化润市", "零碳城市", "正确政绩观"],
            "management_signals": [],
            "caveat": "Work style inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "当前公开检索(官方报道为基础)未发现王大磊负面/纪律信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "王大磊同志简介及分工(市委领导)", "url": "http://www.delingha.gov.cn/info/1013/135818.htm",
             "publisher": "德令哈市人民政府", "published_at": "2025-12-03", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "海西州委常委、德令哈市委书记; 主持市委全面工作"},
            {"id": "S010", "title": "中国共产党德令哈市第十次代表大会隆重开幕", "url": "http://www.delingha.gov.cn/info/1040/142776.htm",
             "publisher": "德令哈市融媒体", "published_at": "2026-07-11", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "王大磊代表人九届市委作报告"},
            {"id": "S011", "title": "中国共产党德令哈市第十届委员会第一次全体会议召开", "url": "http://www.delingha.gov.cn/info/1040/142766.htm",
             "publisher": "德令哈市融媒体", "published_at": "2026-07-12", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "王大磊受主席团委托主持全会, 受选并代表新班子讲话"},
            {"id": "S012", "title": "德令哈市第十届人民代表大会第一次会议胜利闭幕", "url": "http://www.delingha.gov.cn/info/1040/143303.htm",
             "publisher": "德令哈市融媒体", "published_at": "2026-07-24", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "主席团常务主席·大会执行主席王大磊等前排就座"},
        ],
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "王大磊担任德令哈市委书记前的完整履历(出生/籍贯/教育具体院校/何时到德令哈)"},
        "open_questions": [
            {"priority": "critical", "question": "王大磊出生年月(已知1982-04)仅为何开始; 籍贯、教育具体院校(理学博士何校)?", "why_it_matters": "个人画像与去重", "suggested_queries": ["王大磊 海西州委常委 简历", "王大磊 德令哈 理学博士"], "last_attempted": AS_OF},
            {"priority": "high", "question": "王大磊在成为德令哈市委书记前任过哪些州内职务(何时晋升州委常委)?", "why_it_matters": "职业轨迹判断", "suggested_queries": ["王大磊 德令哈 任命 州委常委"], "last_attempted": AS_OF},
        ],
    }


def _build_zhao_xingrong_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _common_scope("市长"),
        "identity": {
            "person_id": "qinghai_delingha_zhao_xingrong_1980",
            "name": "赵兴荣",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1980-10",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "大学(学历)", "major": "",
                          "degree": "", "study_type": "unknown", "source_ids": ["S002", "S101"]}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "赵兴荣_1980", "name_birthplace": "赵兴荣_", "official_profile_url": "http://www.delingha.gov.cn/info/1013/143388.htm"},
        },
        "current_status": {
            "current_post": "海西州人民政府党组成员、副州长; 德令哈市委副书记、市长",
            "current_org": "海西州人民政府/德令哈市人民政府",
            "administrative_rank": "正处级(兼州级副职)",
            "as_of": "2026-08-07",
            "is_current_confirmed": True,
            "source_ids": ["S002", "S020", "S021"],
        },
        "career_timeline": [
            {"start": "2026-07-23", "end": "present", "org": "德令哈市人民政府", "title": "德令哈市委副书记、市长",
             "level": "正处级", "location": "青海省海西州德令哈市", "system": "government", "rank": "正处级",
             "is_key_promotion": True, "notes": "市十届人大一次会议(2026-07-23)当选市长; 主持市政府全面工作, 分管市审计局.",
             "confidence": "confirmed", "source_ids": ["S002", "S021"]},
            {"start": "2026 前", "end": "2026-07-23", "org": "中共德令哈市委员会/德令哈市人民政府", "title": "海西州政府党组成员、副州长 兼 德令哈市委副书记、市政府代市长",
             "level": "正处级", "location": "青海省海西州", "system": "government", "rank": "副州长/代市长",
             "is_key_promotion": True, "notes": "换届前为州政府副州长(简称副州长)兼市委副书记、市政府代市长; 于7月以代市长身份作政府工作报告.",
             "confidence": "confirmed", "source_ids": ["S021", "S022", "S023"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "notes": "赵兴荣任州政府副州长前的完整履历(大学学历院校、入州任职、何职得以任副州长) 公开资料未找到.",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [
            {"org_id": 2, "org_name": "德令哈市人民政府", "role": "市长", "period": "2026-07-23至"},
            {"org_id": 4, "org_name": "海西蒙古族藏族自治州人民政府", "role": "州政府党组成员、副州长", "period": "兼"},
            {"org_id": 1, "org_name": "中共德令哈市委员会", "role": "市委副书记", "period": "2026 至"},
        ],
        "relationships": [
            {"person": "王大磊", "person_id": "qinghai_delingha_wang_dalei_1982", "relationship_type": "superior_subordinate",
             "strength": "strong", "evidence": "市长在市委副书记/书记领导下, 与书记共搭换届班子",
             "overlap_org": "中共德令哈市委员会/德令哈市人民政府", "overlap_period": "2026-07起",
             "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S021", "S022"]},
            {"person": "叶万福", "person_id": "qinghai_delingha_ye_wanfu", "relationship_type": "overlap",
             "strength": "medium", "evidence": "市长在人代会作工作报告并获选举, 人大主席主持", "overlap_org": "德令哈市第十届人民代表大会", "overlap_period": "2026-07",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "governance_record": [
            {"period": "2026-07-21", "domain": "economic_development", "achievement_or_event": "代市长阶段向市十届人大一次会议作政府工作报告(五年度成效+未来五年部署)",
             "role_in_event": "代市长", "measurable_outcome": "全市GDP从2020年86.4亿增至2025年117.8亿, 确立'5+10+5'产业体系、零碳城市",
             "location": "德令哈市", "confidence": "confirmed", "source_ids": ["S022"]},
        ],
        "professional_profile": {
            "primary_specializations": ["政府经济治理", "工业经济", "生态民生"],
            "secondary_specializations": [],
            "career_pattern": "provincial_department / cross_level",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["青海省", "海西州", "德令哈"],
            "promotion_velocity": {"summary": "州政府副州长 →(兼)德令哈代市长 → 当选市长", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "pragmatic", "evidence": "政府工作报告强调产业招商、防汛攻坚、民生七有、项目投资", "confidence": "plausible", "source_ids": ["S022", "S023"]}],
            "speech_themes": ["生态立市", "产业强市", "零碳城市", "招商促投资", "安全发展"],
            "management_signals": [],
            "caveat": "Work style inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "当前公开检索未发现赵兴荣负面/纪律信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S002", "title": "赵兴荣同志简介及分工(市委领导/市政府领导)", "url": "http://www.delingha.gov.cn/info/1013/143388.htm",
             "publisher": "德令哈市人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "海西州政府党组成员、副州长, 德令哈市委副书记、市长; 主持市政府全面工作"},
            {"id": "S021", "title": "德令哈市第十届人民代表大会第一次会议胜利闭幕", "url": "http://www.delingha.gov.cn/info/1040/143303.htm",
             "publisher": "德令哈市融媒体", "published_at": "2026-07-24", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "选举市十届人大常委会主任、市政府市长; 王大磊、叶万福等为执行主席"},
            {"id": "S022", "title": "德令哈市第十届人民代表大会第一次会议隆重开幕", "url": "http://www.delingha.gov.cn/info/1040/143175.htm",
             "publisher": "德令哈市融媒体", "published_at": "2026-07-21", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "州政府副长、市委副书记、市政府副市长代市长赵兴荣作政府工作报告"},
            {"id": "S023", "title": "市政府召开党组(扩大)会议", "url": "http://www.delingha.gov.cn/info/1040/142768.htm",
             "publisher": "德令哈市融媒体", "published_at": "2026-07-13", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "州政府副长、市委副书记、市政府党组书记赵兴荣主持"},
        ],
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "赵兴荣任海州副州长前的完整履历(院校、何时任副州长、何职晋升)"},
        "open_questions": [
            {"priority": "critical", "question": "赵兴荣大学学历就读院校/专业?", "why_it_matters": "教育画像与同学网", "suggested_queries": ["赵兴荣 简历 海西州", "赵兴荣 副州长 大学"], "last_attempted": AS_OF},
            {"priority": "high", "question": "赵兴荣何时/何以被任命为海州政府副州长、何职晋升?", "why_it_matters": "职业轨迹与前职交集", "suggested_queries": ["赵兴荣 海西州 副州长 任命"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "赵兴荣接替的前任德令哈市长是谁、去向? (primary: 九届市长)", "why_it_matters": "前任对接与交接", "suggested_queries": ["德令哈 市长 赵兴荣 前任"], "last_attempted": AS_OF},
        ],
    }


def _build_ye_wanfu_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _common_scope("市人大常委会主任"),
        "identity": {
            "person_id": "qinghai_delingha_ye_wanfu",
            "name": "叶万福",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "叶万福_", "name_birthplace": "叶万福_", "official_profile_url": "http://www.delingha.gov.cn"},
        },
        "current_status": {
            "current_post": "德令哈市人大常委会党组书记、主任",
            "current_org": "德令哈市人民代表大会常务委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-08-07",
            "is_current_confirmed": True,
            "source_ids": ["S012", "S030"],
        },
        "career_timeline": [
            {"start": "2026-07", "end": "present", "title": "德令哈市人大常委会党组书记、主任",
             "level": "正处级", "location": "青海省海西州德令哈市", "system": "other", "rank": "正处级",
             "is_key_promotion": True, "notes": "十届人大一次会议选举; 十届人大主席团常务主席、大会执行主席, 主持大会.",
             "confidence": "confirmed", "source_ids": ["S012", "S030"]},
            {"start": "unknown", "end": "unknown", "title": "履历缺口", "notes": "叶万福任余人大主任前的履历(出生、教育、曾任职务)未找到.",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"org_id": 5, "role": "人大常委会党组书记、主任", "period": "2026-07至"}],
        "relationships": [
            {"person": "王大磊", "person_id": "qinghai_delingha_wang_dalei_1982", "relationship_type": "overlap", "strength": "medium",
             "evidence": "两人同在十届人大大会主席团/执行主席前排就座", "overlap_org": "德令哈市第十届人民代表大会", "overlap_period": "2026-07",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
        ],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown",
                                  "systems_experience": ["other"], "geographic_pattern": ["海西州"],
                                  "promotion_velocity": {"summary": "接替向阳任人大主任", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
                                        "caveat": "Work style inferred from public records."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未见明显负面", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S030", "title": "德令哈市第十届人民代表大会第一次会议胜利闭幕", "url": "http://www.delingha.gov.cn/info/1040/143303.htm",
             "publisher": "德令哈市融媒体", "published_at": "2026-07-24", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "主席团常务主席、执行主席 叶万福"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "low", "biggest_gap": "叶万福出生年月与任人大主任之前的完整履历"},
        "open_questions": [
            {"priority": "high", "question": "叶万福出生年月/教育/曾任职务(其顺位为何任人大主任)", "why_it_matters": "班子结构与交接", "suggested_queries": ["叶万福 德令哈 人大 简历"], "last_attempted": AS_OF},
        ],
    }


_json_configs = [
    ("市委书记", "王大磊", _build_wang_dalei_json),
    ("市长", "赵兴荣", _build_zhao_xingrong_json),
    ("市人大常委会主任", "叶万福", _build_ye_wanfu_json),
]


def _write_person_jsons_main() -> None:
    for job, name, builder in _json_configs:
        data = builder()
        filename = f"{TODAY}-青海省-海西蒙古族藏族自治州-{job}-{name}.json"
        filepath = PJSON_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")


# ── Main ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    _write_person_jsons_main()