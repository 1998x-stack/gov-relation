#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 娄星区 (Louxing District), 娄底市, 湖南省.

Task ID: hunan_娄星区
Level: 市辖区 (娄底市中心城区)
Targets: 区委书记 & 区长
Investigation date: 2026-08-11

Key findings (verified 2026-08-11 via official + media sources):
- 现任区委书记: 刘迟辉 (2026-05-22 全区领导干部会议宣布任区委委员/常委/书记; 2026-06-11 兼任区人武部党委第一书记; 2026-07-30 娄星区第十次党代会十届一次全会当选书记)
- 现任代理区长: 赖毅 (2026-05-29 任区委委员、常委、副书记; 2026-06-01 区十一届人大常委会第四十次会议决定副区长并代理区长; 1982-05 生, 法学学士)
- 前任区委书记: 李彦文 (2018-10 至 2026-05-22, '另有任用' 去向未公开; 1971-03 生, 湖南涟源人)
- 前任区长: 刘志刚 (2021-10 至 2026-06-01, '因工作调动辞去区长', 去向未公开; 1979-10 生, 湖南新化人)
- 第十届区委常委会 (2026-07-30): 刘迟辉、赖毅、向波、高英、彭连赐、李立德、张迪凯、胡红辉、吴彪雄、龙江波、阮丽萍
- 风险信号: 2026-06-02 湖南省纪委监委通报 娄底市委常委、常务副市长谢学龙接受纪律审查和监察调查
- 区人大: 主任 陈晓林(1966-02生, 二级巡视员); 区政协: 主席 徐迪仁; 前任政协主席 邓伟(约2025年卸任)

来源: 娄星区政府门户(louxing.gov.cn 领导之窗30份简历页 + 娄星动态新闻列表), 华声在线(刘迟辉任命/娄底市委组织部任前公示/谢学龙被查), 娄底市政府网(人事任免公文), 娄星在线(hnldlx.cn 公示公告栏目), 维基百科(身份信息).
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
SLUG = "娄星区"
TODAY = datetime.now().strftime("%Y%m%d")  # 20260811
AS_OF = "2026-08-11"

# ── Output paths (promotion to province dirs is done by scripts/process_tmp.py) ─
STAGING = REPO_ROOT / "data" / "tmp" / "hunan_娄星区"
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
JSON_DIR = STAGING

# ══════════════════════════════════════════════════════════════════════════
# SOURCES
# ══════════════════════════════════════════════════════════════════════════
SOURCES = [
    {"id": "S001", "title": "娄星区政府网: 领导之窗·区委 刘迟辉简历页", "url": "https://www.louxing.gov.cn/louxing/xxgk/ldzc/quw/202605/e568960f172d44ef05bf0b238f42640.shtml", "publisher": "娄星区人民政府", "published_at": "", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "刘迟辉, 男, 汉族, 1976年10月生, 研究生学历, 中共党员, 现任中共娄底市娄星区委书记, 主持区委全面工作"},
    {"id": "S002", "title": "娄星区政府网: 领导之窗·区政府 赖毅简历页", "url": "https://www.louxing.gov.cn/louxing/xxgk/ldzc/qzf/202107/31a0a03addb8432d9ebc41f63b0b265b.shtml", "publisher": "娄星区人民政府", "published_at": "", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "赖毅, 男, 汉族, 1982年5月生, 大学学历, 法学学士, 中共党员, 现任区委副书记、区人民政府党组书记、副区长、代理区长, 主持区政府全面工作"},
    {"id": "S003", "title": "华声在线: 刘迟辉任娄底市娄星区委书记 (2026-05-22 全区领导干部会议)", "url": "https://hunan.voc.com.cn/news/202605/32722215.html", "publisher": "华声在线", "published_at": "2026-05-22", "accessed_at": "2026-08-11", "source_type": "appointment_notice", "reliability": "high", "notes": "宣布省委、市委有关人事安排决定; 市委常委、市委组织部部长章清宣布: 刘迟辉任区委委员、常委、书记; 李彦文不再担任区委书记、常委、委员职务, 另有任用"},
    {"id": "S004", "title": "娄星区政府网: 娄星区召开领导干部会议 (2026-05-22 省委、市委人事安排)", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/202605/597335cfe4764cc188012c7bb2f4437f.shtml", "publisher": "娄星区人民政府", "published_at": "2026-05-22", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "刘迟辉任区委委员、常委、书记; 李彦文不再担任、另有任用"},
    {"id": "S005", "title": "娄星区政府网: 娄星区召开领导干部会议 (2026-05-29 市委人事安排)", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/202605/9b8019bbf4804bd691e190de882572c5.shtml", "publisher": "娄星区人民政府", "published_at": "2026-05-29", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "市委组织部分管日常工作的副部长周向红宣布: 赖毅任中共娄底市娄星区委委员、常委、副书记"},
    {"id": "S006", "title": "娄星区政府网: 区十一届人大常委会第四十次会议 赖毅任代理区长 (2026-06-01)", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/202606/0e218f333bbf4e44bd9c1074bd18eeac.shtml", "publisher": "娄星区人民政府", "published_at": "2026-06-01", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "接受刘志刚因工作调动辞去区长职务; 任命赖毅任副区长并代理区长; 区人大常委会党组书记陈颂飞列席; 区委常委、组织部部长肖亮到会说明人事"},
    {"id": "S007", "title": "娄星区政府网: 宣布区人武部党委第一书记任职大会 (2026-06-11)", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/202606/f73ba2cfb05745698ea0db5623f6861b.shtml", "publisher": "娄星区人民政府", "published_at": "2026-06-11", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "娄底市委常委、娄底军分区政委许连颁发任职证书并讲话; 区委书记、区人武部党委第一书记刘迟辉作任职表态发言; 李立德、张迪凯、刘智勇等参加"},
    {"id": "S008", "title": "娄星区政府网: 中共娄底市娄星区第十届委员会第一次全体会议 刘迟辉当选书记 (2026-07-30)", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/202607/920e2375470943039d9cd4848f5819b2.shtml", "publisher": "娄星区人民政府", "published_at": "2026-07-30", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "十届区委全会公报式新闻: 刘迟辉当选区委书记; 赖毅、向波当选区委副书记"},
    {"id": "S009", "title": "娄星区政府网: 中国共产党娄底市娄星区第十次代表大会开幕 (2026-07-29 刘迟辉作报告)", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/202607/90cc74d160ce4352b82f4927798ef5f6.shtml", "publisher": "娄星区人民政府", "published_at": "2026-07-29", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "报告提出'六区'建设('中部地区材料谷核心区等)与'1122'现代产业体系; 书面审议第九届区纪委工作报告"},
    {"id": "S010", "title": "娄星区政府网: 区十一届人大常委会第四十二次会议 任命肖佺为副区长 (2026-07-10)", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/202607/a5c97b97a41c43e6bc15a514432c8a70.shtml", "publisher": "娄星区人民政府", "published_at": "2026-07-10", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "会议决定任命肖佺为区人民政府副区长; 区人大常委会党组书记陈颂飞列席; 区委常委、组织部部长肖亮到会说明人事; 区法院院长罗立静、区检察院检察长汤亮列席"},
    {"id": "S011", "title": "华声在线: 娄底市委管理干部任前公示公告·(2026-06-08)", "url": "https://hunan.voc.com.cn/news/202606/32857420.html", "publisher": "华声在线", "published_at": "2026-06-08", "accessed_at": "2026-08-11", "source_type": "appointment_notice", "reliability": "high", "notes": "邓函提(1983-07, 现任娄星区副区长)拟进一步使用; 肖佺(1989-07, 新化县圳上镇党委书记)拟提名为县市区政府副职人选; 周璐(1989-11, 娄星区乐坪街道党工委书记)拟提名为县市区政府副职人选"},
    {"id": "S012", "title": "华声在线: 湖南省娄底市委常委、常务副市长谢学龙被查 (2026-06-02)", "url": "https://hunan.voc.com.cn/news/202606/32806600.html", "publisher": "华声在线(三湘风纪)", "published_at": "2026-06-02", "accessed_at": "2026-08-11", "source_type": "media", "reliability": "high", "notes": "谢学龙, 娄底市委常委、市人民政府常务副市长, 接受纪律审查和监察调查"},
    {"id": "S013", "title": "维基百科: 娄星区", "url": "https://zh.wikipedia.org/wiki/%E5%A8%84%E6%98%9F%E5%8C%BA", "publisher": "维基百科", "published_at": "", "accessed_at": "2026-08-11", "source_type": "encyclopedia", "reliability": "medium", "notes": "身份信息: 李彦文 1971-03/湖南涟源; 刘志刚 1979-10/湖南新化; 陈晓林 新化; 邓伟 1972-04/湖南宁乡; 就任日期: 书记2018-10, 区长/人大/政协 2021-10"},
    {"id": "S014", "title": "娄星在线(hnldlx.com): 公示公告 — 区领导公开接访公告 (2026-08)", "url": "https://www.hnldlx.cn/content/646042/91/16159484.html", "publisher": "娄星在线(红网)", "published_at": "2026-08", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "肖佺(万宝镇)、李立德/聂永红(涟滨街道)、阮丽萍(双江乡)公开接访公告——确认其现任区级领导身份与活动"},
    {"id": "S015", "title": "娄底市政府网: 政务公开·人事信息栏目", "url": "https://www.hnloudi.gov.cn/loudi/xxgk/xxgk.shtml", "publisher": "娄底市人民政府", "published_at": "2026-07-08", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "娄底市人民政府任免工作人员(2026-05-09/05-26/07-08) — 局委办负责人调整, 未涉及县区党政正职"},
    {"id": "S016", "title": "娄星区政府网: 领导之窗(区委/区人大/区政府/区政协 名侧栏)", "url": "https://www.louxing.gov.cn/louxing/index.shtml", "publisher": "娄星区人民政府", "published_at": "", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "现行四大班子 30 份简历页侧栏名单: 区委11人; 区人大6人; 区政府11人; 区政协6人"},
    {"id": "S017", "title": "娄星区政府网(娄星动态·2026-01..05): 李彦文/刘志刚活动记录", "url": "https://www.louxing.gov.cn/louxing/zwdt/lxdt/list.shtml", "publisher": "娄星区人民政府", "published_at": "", "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high", "notes": "2026-01..05李彦文以书记身份主持区委常委会/防汛/信访/支部组织生活会; 刘志刚以区长身份主持区政府常务会/督查 — 佐证任职至卸任前"},
    {"id": "S018", "title": "华声在线: 冷水江市召开领导干部会议 宣布娄底市委有关人事安排决定 (2026-06)", "url": "https://hunan.voc.com.cn/news/202606/33026645.html", "publisher": "华声在线", "published_at": "2026-06", "accessed_at": "2026-08-11", "source_type": "media", "reliability": "high", "notes": "娄底市县市区干部调整联动背景: 冷水江市(唐正任市委书记)等县市区同步换届调整"},
]
# ══════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════
persons = [
    # ── 1. 现任区委书记 ──
    {
        "id": 1, "name": "刘迟辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-10", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委书记", "current_org": "中共娄底市娄星区委员会",
        "source": "S001 S003 S004 S007 S008",
        "profile_notes": "1976年10月生, 男, 汉族, 研究生学历, 中共党员. 2026-05-22 全区领导干部会议宣布任区委委员、常委、书记(省委、市委决定, 市委常委、市委组织部部长章清宣布); 2026-06-11 兼任区人武部党委第一书记; 2026-07-29 主持区第十次党代会作工作报告, 2026-07-30 十届一次全会当选区委书记. 履任前的职务与履历公开资料未检索到(缺口). 党代会报告提出推进'六区'建设与'1122'现代产业体系.",
        "career": [
            {"start": "unknown", "end": "2026-05-22", "org": "（履任前单位待核）", "title": "履历缺口——公开资料未检索到履任区委书记前的职务", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "娄底市/县域党政系统干部; 具体前职待核", "confidence": "unverified", "source_ids": []},
            {"start": "2026-05-22", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2026-05-22宣任; 2026-06-11任区人武部党委第一书记; 2026-07-30区第十届一次全会当选区委书记", "confidence": "confirmed", "source_ids": ["S003", "S004", "S007", "S008"]},
        ],
        "governance": [
            {"period": "2026-07-29", "domain": "economic_development", "achievement_or_event": "区第十次党代会报告: 推进'六区'建设高质量发展(中部地区'材料谷'建设核心区、粤港澳大湾区产业协同先行区、长株潭都市圈融合发展先导区、城乡融合高质量发展示范区、现代服务业转型升级样板区、文明幸福首善区); 构建'1122'现代化产业体系", "role_in_event": "区委书记作报告", "measurable_outcome": "", "location": "娄底市娄星区", "confidence": "confirmed", "source_ids": ["S009"]},
            {"period": "2026-06", "domain": "economic_development", "achievement_or_event": "率队赴广东开展招商考察; 到涟钢(华菱涟钢)对接座谈; 调研娄星产业园重点企业", "role_in_event": "区委书记带队", "location": "娄星区", "confidence": "confirmed", "source_ids": ["S017"]},
            {"period": "2026-05-2026-08", "domain": "public_security", "achievement_or_event": "主持区委平安建设/安全生产/信访/群众身边不正之风和腐败问题集中整治专题调度会多项", "role_in_event": "主持", "location": "娄星区", "confidence": "confirmed", "source_ids": ["S017"]},
        ],
        "work_style": [
            {"trait": "grassroots_oriented", "evidence": "2026-06..08多轮'四不两直'暗访检查(消防/防汛/安全生产)与信访接待", "confidence": "confirmed", "source_ids": ["S017"]},
            {"trait": "pragmatic", "evidence": "招商考察(长三角/广东)、'三电一钛'产业专班推进——产业导向", "confidence": "plausible", "source_ids": ["S017"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "cross_county_rotation", "systems": ["party"], "geo": []},
    },
    # ── 2. 现任代理区长 ──
    {
        "id": 2, "name": "赖毅", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-05", "birthplace": "", "education": "大学学历, 法学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记、代理区长", "current_org": "娄星区人民政府",
        "source": "S002 S005 S006 S013",
        "profile_notes": "1982年5月生, 男, 汉族, 大学学历, 法学学士, 中共党员. 现任中共娄底市娄星区委副书记、区人民政府党组书记、副区长、代理区长, 主持区政府全面工作. 2026-05-29 市委任命区委委员、常委、副书记(市委组织部副部长周向红宣布); 2026-06-01 区十一届人大常委会第十次会议决定副区长并代理区长(刘志刚因工作调动辞职). 2026-07-30 第十届区委一次全会当选区委副书记. 履任待核: 2021-07领导之窗已有其区委班子成员简历页, 此前任职履历未公开.",
        "career": [
            {"start": "unknown", "end": "2026-05-29", "org": "娄星区(区委任一职务待核)", "title": "履历缺口", "level": "县处级", "system": "party", "rank": "", "is_key_promotion": False, "notes": "2021-07起已有区委领导之窗简历页, 具体职务待核", "confidence": "unverified", "source_ids": ["S002"]},
            {"start": "2026-05-29", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委副书记", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "2026-05-29市委任命; 2026-07-30十届一次全会继续当选副书记", "confidence": "confirmed", "source_ids": ["S005", "S008"]},
            {"start": "2026-06-01", "end": "present", "org": "娄星区人民政府", "title": "区人民政府党组书记、代理区长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "区十一届人大常委会第四十次会议: 任命副区长并代理区长; 主持区政府全面工作", "confidence": "confirmed", "source_ids": ["S006", "S002"]},
        ],
        "governance": [
            {"period": "2026-06-07", "domain": "other", "achievement_or_event": "主持召开全区群众身边不正之风和腐败问题集中整治专项工作调度会、区应安委全会等", "role_in_event": "代理区长主持", "location": "娄星区", "confidence": "confirmed", "source_ids": ["S017"]},
            {"period": "2026-06", "domain": "economic_development", "achievement_or_event": "与区委书记赴涟钢对接、调研娄星产业园重点企业; 检查高考准备工作", "role_in_event": "代理区长", "location": "娄星区", "confidence": "confirmed", "source_ids": ["S017"]},
        ],
        "work_style": [
            {"trait": "technocratic", "evidence": "法学学士背景; 人事安排表态'讲政治拎得清、抓发展干得了、守底线靠得住'", "confidence": "plausible", "source_ids": ["S006"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["party", "government", "legal"], "geo": []},
    },
    # ── 3. 前任区委书记 (2018.10-2026.05) ──
    {
        "id": 3, "name": "李彦文", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-03", "birthplace": "湖南省涟源市", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任娄星区委书记(另有任用,去向2026-08待核)", "current_org": "(候任)",
        "source": "S003 S013 S017",
        "profile_notes": "1971年3月生, 男, 汉族, 湖南涟源人, 中共党员. 2018年10月起任中共娄底市娄星区委书记(维基百科确认就任日期2018-10), 2021-07 娄星区第九次党代会后连任区委书记. 履职期间主持区委全面工作, 2026-01..05 多次主持区委常委会/防汛/信访等. 2026-05-22 全区领导干部会议宣布不再担任区委书记、常委、委员职务, 另有任用; 新职务截至2026-08-11未公开(关键待核项). 此前期履历(涟源当地成长?)未检索到完整公开来源.",
        "career": [
            {"start": "unknown", "end": "2018-10", "org": "涟源市/娄底市直(待核)", "title": "履历缺口", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "湖南涟源人; 1980年代参加工作, 具体履历待核", "confidence": "unverified", "source_ids": []},
            {"start": "2018-10", "end": "2021-07", "org": "中共娄底市娄星区委员会", "title": "区委书记", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2018-10就任(维基); 第九次党代会(2021-07)前连任", "confidence": "confirmed", "source_ids": ["S013"]},
            {"start": "2021-07", "end": "2026-05-22", "org": "中共娄底市娄星区委员会", "title": "区委书记(第九届连任)", "level": "县处级", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2026-01..05主持区委常委会/四套班子活动记录", "confidence": "confirmed", "source_ids": ["S013", "S017"]},
            {"start": "2026-05-22", "end": "unknown", "org": "(另行任用)", "title": "去向待核", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "另有任用; 新职务2026-08-11前未公开", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        ],
        "governance": [
            {"period": "2026-01-05", "domain": "economic_development", "achievement_or_event": "区委经济工作会议; '全力以赴抓产业、抓项目、抓招商'; 部署烟花爆竹管控/防汛/反诈", "role_in_event": "区委书记主持", "location": "娄星区", "confidence": "confirmed", "source_ids": ["S017"]},
        ],
        "work_style": [
            {"trait": "grassroots_oriented", "evidence": "2026-04 信访坐班接访推行'三有推定'工作法; 多次乡镇/一线调研", "confidence": "plausible", "source_ids": ["S017"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["party"], "geo": ["涟源", "娄星"]},
    },
    # ── 4. 前任区长 (2021.10-2026.06) ──
    {
        "id": 4, "name": "刘志刚", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-10", "birthplace": "湖南省新化县", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任娄星区区长(因工作调动,去向2026-08待核)", "current_org": "(待核)",
        "source": "S006 S013 S017",
        "profile_notes": "1979年10月生, 男, 汉族, 湖南新化人, 中共党员. 2021年10月当选娄星区人民政府区长(第九届/第十届人大安排); 履职期间主持区政府全面工作(区政府常务会/安全生产/防汛/禁毒/地质灾害). 2026-06-01 区十一届人大常委会第四十次会议接受其因工作调动的辞职请求; 调动去向截至2026-08-11未公开. 此前履历未检索到公开来源(缺口).",
        "career": [
            {"start": "unknown", "end": "2021-10", "org": "娄底市县区(待核)", "title": "履历缺口", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "2021年调任娄星区长前职待核", "confidence": "unverified", "source_ids": []},
            {"start": "2021-10", "end": "2026-06-01", "org": "娄星区人民政府", "title": "区长", "level": "县处级", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2026-01..05 主持区政府常务会/应安委全会/防汛工作", "confidence": "confirmed", "source_ids": ["S013", "S017"]},
            {"start": "2026-06-01", "end": "unknown", "org": "(工作调动)", "title": "去向待核", "level": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "因工作调动辞去区长; 新职务未公开", "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        "governance": [
            {"period": "2026-01-05", "domain": "public_security", "achievement_or_event": "新一轮娄星禁毒人民战争部署大会(2026-05)出席并讲话; 主持应安委全会、安全生产与防汛部署会", "role_in_event": "区长", "location": "娄星区", "confidence": "confirmed", "source_ids": ["S017"]},
        ],
        "work_style": [
            {"trait": "grassroots_oriented", "evidence": "2026-05 多次带队巡河、督查危房整治、暗访安全生产——一线督查型", "confidence": "plausible", "source_ids": ["S017"]},
        ],
        "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government"], "geo": ["新化", "娄星"]},
    },
    # ── 5. 新任区委副书记 (2026-07-30 十届一次全会) ──
    {
        "id": 5, "name": "向波", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记", "current_org": "中共娄底市娄星区委员会",
        "source": "S008",
        "profile_notes": "2026-07-30 娄星区第十届委员会第一次全体会议当选区委副书记(与书记刘迟辉、第二副书记赖毅并列). 出生/籍贯/前职未公开检索到(缺口).",
        "career": [
            {"start": "2026-07-30", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委副书记", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "十届一次全会当选; 前职未公开", "confidence": "confirmed", "source_ids": ["S008"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    # ── 6-13. 现任区委常委 (十届, 2026-07-30 起) ──
    {
        "id": 6, "name": "高英", "gender": "女", "ethnicity": "汉族",
        "birth": "1980-12", "birthplace": "", "education": "研究生学历, 学士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、统战部部长, 区政协党组副书记(兼)", "current_org": "中共娄底市娄星区委员会",
        "source": "S008 S016",
        "profile_notes": "高英, 女, 汉族, 1980年12月生, 研究生学历, 学士学位, 中共党员. 现任区委常委、统战部部长、区政协党组副书记(兼), 主管统一战线、民族宗教、侨务等. 2026-07-30 十届区委一次全会连任常委(为九届继任成员).",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委常委、统战部部长", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "2026-07-30十届常委会连任", "confidence": "confirmed", "source_ids": ["S008", "S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 7, "name": "彭连赐", "gender": "男", "ethnicity": "汉族",
        "birth": "1984-10", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区纪委书记, 区监委代理主任", "current_org": "中共娄底市娄星区纪律检查委员会",
        "source": "S016",
        "profile_notes": "彭连赐, 男, 汉族, 1984年10月生, 研究生学历, 中共党员. 现任区委常委、区纪委书记、区监委代理主任, 主管纪检监察和党风廉政建设、巡察、作风建设. 2026-07-30 连任十届区委常委; 2026-07/08 区纪委十届一次全会主持/纪委班子换届. 年轻纪委干部(1984年生).",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共娄底市娄星区纪律检查委员会", "title": "区委常委、区纪委书记、区监委代理主任", "level": "县处级", "system": "discipline", "rank": "副处级", "is_key_promotion": False, "notes": "纪委系统干部; 区监委代理主任待区人代会选举", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "discipline_track", "systems": ["discipline"], "geo": []},
    },
    {
        "id": 8, "name": "李立德", "gender": "男", "ethnicity": "汉族",
        "birth": "1984-03", "birthplace": "", "education": "大学学历, 学士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区委办公室主任", "current_org": "中共娄底市娄星区委员会",
        "source": "S007 S014 S016",
        "profile_notes": "李立德, 男, 汉族, 1984年3月生, 大学学历, 学士学位, 中共党员. 现任区委常委、区委办公室主任, 主持区委机关日常工作. 2026-07-30 连任十届区委常委; 2026-08公开接访公告(涟滨街道)确认其在区级领导岗位.",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委常委、区委办公室主任", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016", "S014"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 9, "name": "张迪凯", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-08", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区人武部部长", "current_org": "娄星区人民武装部",
        "source": "S007 S008 S016",
        "profile_notes": "张迪凯, 男, 汉族, 1976年8月生, 大学学历, 中共党员. 现任区委常委、区人民武装部部长(军分区系统交流任职). 2026-07-30 连任十届区委常委.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民武装部", "title": "区委常委、区人武部部长", "level": "县处级", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 10, "name": "胡红辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-11", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委(2026-07起)、区人民政府副区长", "current_org": "娄星区人民政府",
        "source": "S008 S016",
        "profile_notes": "胡红辉, 男, 汉族, 1977年11月生, 大学学历, 中共党员. 副区长(分管科技、工信、交通、公路、企业改革、中小企业、石油邮政通信、信访、金融证券保险、民间融资风险处置等). 2026-07-30 新进十届区委常委会——由区政府副区长升任常委.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府", "title": "副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "2026-07-30新进区委常委", "confidence": "confirmed", "source_ids": ["S016", "S008"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government"], "geo": []},
    },
    {
        "id": 11, "name": "吴彪雄", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委(新进)", "current_org": "中共娄底市娄星区委员会",
        "source": "S008",
        "profile_notes": "2026-07-30 十届一次全会新当选区委常委. 出生/籍贯/前职/分工均未公开检索到(缺口).",
        "career": [
            {"start": "2026-07-30", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委常委", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "新进十届常委会; 前职待核", "confidence": "confirmed", "source_ids": ["S008"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 12, "name": "龙江波", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委(新进)", "current_org": "中共娄底市娄星区委员会",
        "source": "S008",
        "profile_notes": "2026-07-30 十届一次全会新当选区委常委。出生/籍贯/前职/分工未公开检索到(缺口).",
        "career": [
            {"start": "2026-07-30", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委常委", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "新进十届常委会; 前职待核", "confidence": "confirmed", "source_ids": ["S008"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 13, "name": "阮丽萍", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委(新进)", "current_org": "中共娄底市娄星区委员会",
        "source": "S008 S014",
        "profile_notes": "2026-07-30 十届一次全会新当选区委常委; 2026-08 公开接访公告安排其到双江乡公开接访(区级领导当班). 出生/籍贯/前职/分工未公开(缺口).",
        "career": [
            {"start": "2026-07-30", "end": "present", "org": "中共娄底市娄星区委员会", "title": "区委常委", "level": "县处级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "新进十届常委会", "confidence": "confirmed", "source_ids": ["S008", "S014"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    # ── 14-18. 九届常委/换届后调整 ──
    {
        "id": 14, "name": "周庶舟", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-04", "birthplace": "", "education": "大学学历, 硕士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民政府党组副书记、常务副区长", "current_org": "娄星区人民政府",
        "source": "S016",
        "profile_notes": "周庶舟, 男, 汉族, 1980年4月生, 大学学历, 硕士学位, 中共党员. 现任区委常委(至2026-07第九届)、区人民政府党组副书记、常务副区长. 2026-07-30 十届区委换届后未再进入常委会(仍任常务副区长; 2026-07-10人大会议仍以区委常委、常务副区长身份列席). 协助区长负责政府常务工作(发改/财政/税务/统计/应急/营商等).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府", "title": "区委常委(至2026-07)、常务副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "2026-07-10 区人大第42次会议仍以区委常委、常务副区长列席; 十届换届后退出常委会", "confidence": "confirmed", "source_ids": ["S016", "S010"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["government"], "geo": []},
    },
    {
        "id": 15, "name": "王谦", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-06", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委(至2026-07)、区人民政府副区长", "current_org": "娄星区人民政府",
        "source": "S016",
        "profile_notes": "王谦, 男, 汉族, 1973年6月生, 研究生学历, 中共党员. 现任区委常委(至2026-07九届)、区人民政府副区长(分管民政/水利/农业农村/乡村振兴/退役军人等). 2026-07-30 换届后未再进入十届常委会(仍任副区长).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府", "title": "区委常委(至2026-07)、副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "换届后退出常委会, 留任副区长", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": []},
    },
    {
        "id": 16, "name": "肖亮", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-01", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "原区委常委、组织部部长(2026-07换届后去向待核)", "current_org": "中共娄底市娄星区委员会(前)",
        "source": "S006 S010 S016",
        "profile_notes": "肖亮, 男, 汉族, 1979年1月生, 研究生学历, 中共党员. 原任区委常委、组织部部长(2026-05/06/07 多次以该身份到区人大常委会说明人事安排). 2026-07-30 十届区委换届后不再担任区委常委; 新去向未公开(缺口).",
        "career": [
            {"start": "unknown", "end": "2026-07", "org": "中共娄底市娄星区委员会", "title": "区委常委、组织部部长", "level": "县处级", "system": "organization", "rank": "副处级", "is_key_promotion": False, "notes": "换届后去向待核", "confidence": "confirmed", "source_ids": ["S006", "S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "organization_track", "systems": ["organization"], "geo": []},
    },
    {
        "id": 17, "name": "曾海军", "gender": "女", "ethnicity": "汉族",
        "birth": "1970-11", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "原区委常委、宣传部部长(2026-07换届后去向)", "current_org": "中共娄底市娄星区委员会(前)",
        "source": "S016",
        "profile_notes": "曾海军, 女, 汉族, 1970年11月生, 大学学历, 中共党员, 三级调研员. 原任区委常委、宣传部部长(宣传思想/意识形态/文明建设等). 2026-07-30 换届后未进入十届常委会; 新去向待核.",
        "career": [
            {"start": "unknown", "end": "2026-07", "org": "中共娄底市娄星区委员会", "title": "区委常委、宣传部部长", "level": "县处级", "system": "propaganda", "rank": "副处级", "is_key_promotion": False, "notes": "换届后去向待核", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["propaganda"], "geo": []},
    },
    {
        "id": 18, "name": "吕许灵", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-01", "birthplace": "", "education": "大学学历, 硕士学位, 公职律师",
        "party_join": "中共党员", "work_start": "",
        "current_post": "原区委副书记、政法委书记(2026-07换届后去向)", "current_org": "中共娄底市娄星区委员会(前)",
        "source": "S016",
        "profile_notes": "吕许灵, 男, 汉族, 1979年1月生, 大学学历, 硕士学位, 公职律师, 中共党员. 原任区委副书记、政法委书记(协助书记抓党建/政法/信访/平安建设/农业农村/教育). 2026-07-30 十届区委一次全会未再当选副书记; 新去向待核.",
        "career": [
            {"start": "unknown", "end": "2026-07", "org": "中共娄底市娄星区委员会", "title": "区委副书记、政法委书记", "level": "县处级", "system": "public_security", "rank": "副处级", "is_key_promotion": False, "notes": "换届后去向待核", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["party", "public_security", "legal"], "geo": []},
    },
    # ── 19-25. 区政府其他领导 ──
    {
        "id": 19, "name": "唐爱华", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-01", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民政府副区长", "current_org": "娄星区人民政府",
        "source": "S016",
        "profile_notes": "唐爱华, 男, 汉族, 1970年1月生, 大学学历, 中共党员. 现任娄星区人民政府党组成员、副区长(负责娄星产业开发区、城乡投、招商引资、投融资、涟钢周边环境综合治理、煤矿棚户区改造等; 协管财税, 对接涟钢领导小组办公室).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府", "title": "副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "产业园区与招商条线", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government", "development_zone"], "geo": []},
    },
    {
        "id": 20, "name": "周俊华", "gender": "男", "ethnicity": "汉族",
        "birth": "1969-11", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民政府副区长", "current_org": "娄星区人民政府",
        "source": "S016",
        "profile_notes": "周俊华, 男, 汉族, 1969年11月生, 大学学历, 中共党员. 现任区人民政府党组成员、副区长(自然资源、生态环境、住建、人防、林业、城管、征地拆迁、控违拆违等).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府", "title": "副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "城建条线", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": []},
    },
    {
        "id": 21, "name": "肖民海", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-04", "birthplace": "", "education": "大学学历",
        "party_join": "非党", "work_start": "",
        "current_post": "区人民政府副区长(无党派)", "current_org": "娄星区人民政府",
        "source": "S016",
        "profile_notes": "肖民海, 男, 汉族, 1979年4月生, 大学学历, 非党. 现任区人民政府副区长(内外贸易、外向型经济、市场监督管理、知识产权等), 党外干部.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府", "title": "副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "党外干部(非党)", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": []},
    },
    {
        "id": 22, "name": "谢劭", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-11", "birthplace": "", "education": "大学学历, 学士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民政府副区长、娄底市公安局娄星分局局长", "current_org": "娄底市公安局娄星分局",
        "source": "S016",
        "profile_notes": "谢劭, 男, 汉族, 1977年11月生, 大学学历, 学士学位, 中共党员, 二级高级警长. 娄星区人民政府党组成员、副区长、娄底市公安局娄星分局党委书记、局长(政法委系统交流任职; 负责公安、司法、维稳、禁毒等).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄底市公安局娄星分局", "title": "副区长、公安分局局长", "level": "县处级", "system": "public_security", "rank": "副处级", "is_key_promotion": False, "notes": "公安系统交流任职", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "system_rotation", "systems": ["public_security"], "geo": []},
    },
    {
        "id": 23, "name": "肖佺", "gender": "男", "ethnicity": "汉族",
        "birth": "1989-07", "birthplace": "湖南省新化县", "education": "大学学历, 文学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民政府副区长", "current_org": "娄星区人民政府",
        "source": "S011 S010 S014",
        "profile_notes": "肖佺, 男, 汉族, 1989年7月生, 大学学历, 文学学士, 中共党员. 原任新化县圳上镇党委书记、一级主任科员; 2026-06-08 娄底市委组织部任前公示拟提名为县市区政府副职人选; 2026-07-10 区十一届人大常委会第四十二次会议决定任命为区人民政府副区长; 2026-08 公开接访公告确认其在万宝镇公开接访. 九十年代出生年轻干部跨县赴区任职.",
        "career": [
            {"start": "unknown", "end": "2026-07-10", "org": "中共新化县圳上镇委员会", "title": "新化县圳上镇党委书记、一级主任科员", "level": "乡科级", "system": "party", "rank": "正科级", "is_key_promotion": False, "notes": "乡镇党委书记起步", "confidence": "confirmed", "source_ids": ["S011"]},
            {"start": "2026-07-10", "end": "present", "org": "娄星区人民政府", "title": "副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "跨县(新化→娄星)任职; 2026-08 万宝镇接访当班", "confidence": "confirmed", "source_ids": ["S010", "S014"]},
        ],
        "governance": [], "work_style": [],
        "risk": [],
        "extras": {"career_pattern": "cross_county_rotation", "systems": ["government", "party"], "geo": ["新化", "娄星"]},
    },
    {
        "id": 24, "name": "姚满文", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-06", "birthplace": "", "education": "大专学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民政府党组成员、区政府办公室主任", "current_org": "娄星区人民政府",
        "source": "S016",
        "profile_notes": "姚满文, 男, 汉族, 1975年6月生, 大专学历, 中共党员. 现任区人民政府党组成员、区政府办公室党组书记、主任, 负责处理区政府日常工作.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府办公室", "title": "区政府党组成员、办公室主任", "level": "县处级", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": []},
    },
    {
        "id": 25, "name": "邓函提", "gender": "女", "ethnicity": "汉族",
        "birth": "1983-07", "birthplace": "", "education": "大学学历, 文学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民政府副区长(2026-06公示拟进一步使用)", "current_org": "娄星区人民政府",
        "source": "S011 S016",
        "profile_notes": "邓函提, 女, 汉族, 1983年7月生, 大学学历, 文学学士, 中共党员. 现任娄星区人民政府副区长. 2026-06-08 娄底市委管理干部任前公示公告: 邓函提拟进一步使用(2026-07-30十届换届后未进入区委常委会, 具体新职/去向待核).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人民政府", "title": "副区长", "level": "县处级", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "2026-06 '拟进一步使用'; 新职待核", "confidence": "confirmed", "source_ids": ["S011"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": []},
    },
    {
        "id": 26, "name": "周璐", "gender": "女", "ethnicity": "汉族",
        "birth": "1989-11", "birthplace": "", "education": "大学学历, 管理学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乐坪街道党工委书记(2026-06公示拟任县市区政府副职)", "current_org": "娄星区乐坪街道",
        "source": "S011",
        "profile_notes": "周璐, 女, 汉族, 1989年11月生, 大学学历, 管理学学士, 中共党员. 现任娄星区乐坪街道党工委书记、一级主任科员. 2026-06-08 公示拟提名为县市区政府副职人选(是否留任娄星区副区长或他县区任职, 截至2026-08-11未确认).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区乐坪街道", "title": "党工委书记、一级主任科员", "level": "乡科级", "system": "party", "rank": "正科级", "is_key_promotion": False, "notes": "2026-06公示拟任县市区政府副职; 去向待核", "confidence": "confirmed", "source_ids": ["S011"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    # ── 27-33. 区人大常委会 ──
    {
        "id": 27, "name": "陈晓林", "gender": "男", "ethnicity": "汉族",
        "birth": "1966-02", "birthplace": "湖南省新化县", "education": "大学学历, 学士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组书记、主任", "current_org": "娄星区人大常委会",
        "source": "S006 S013 S016",
        "profile_notes": "陈晓林, 男, 汉族, 1966年2月生, 大学学历, 学士学位, 中共党员, 二级巡视员(维基; 娄底新化人). 现任娄星区人大常委会党组书记、主任, 主持区人大常委会党组和常委会全面工作. 2021年10月就任区人大常委会主任; 2026-06/07多次主持区人大常委会会议(其中40次会议 赖毅任代理区长, 第42次会议 肖佺任副区长).",
        "career": [
            {"start": "2021-10", "end": "present", "org": "娄星区人大常委会", "title": "党组书记、主任", "level": "县处级", "system": "other", "rank": "正处级", "is_key_promotion": True, "notes": "2021-10就任(维基); 二级巡视员", "confidence": "confirmed", "source_ids": ["S013", "S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": ["新化", "娄星"]},
    },
    {
        "id": 28, "name": "陈颂飞", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组书记(候任主任候选人待核)", "current_org": "娄星区人大常委会",
        "source": "S006 S010",
        "profile_notes": "2026-06/07 区人大常委会第四十、四十二次会议均以'区人大常委会党组书记'身份列席(主任陈晓林主持会议)——显示区人大领导班子正处交接期(党组书记已换, 主任待区人代会换届). 出生/籍贯/履历任前职务未公开检索到(缺口).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人大常委会", "title": "党组书记(陈晓林仍任主任)", "level": "县", "system": "other", "rank": "", "is_key_promotion": False, "notes": "候任主任候选人; 换届人代会待 2026-10 前召开", "confidence": "confirmed", "source_ids": ["S006", "S010"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 29, "name": "李煌", "gender": "男", "ethnicity": "汉族",
        "birth": "1969-09", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组副书记、副主任", "current_org": "娄星区人大常委会",
        "source": "S010 S016",
        "profile_notes": "李煌, 男, 汉族, 1969年9月生, 大学学历, 中共党员. 现任区人大常委会党组副书记、副主任(分管常委会办公室、财经委等), 2026-07-10主持区人大第42次会议.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人大常委会", "title": "党组副书记、副主任", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016", "S010"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 30, "name": "聂永红", "gender": "女", "ethnicity": "汉族",
        "birth": "1968-09", "birthplace": "", "education": "研究生学历",
        "party_join": "无党派", "work_start": "",
        "current_post": "区人大常委会副主任、区工商联主席", "current_org": "娄星区人大常委会",
        "source": "S014 S016",
        "profile_notes": "聂永红, 女, 汉族, 1968年9月生, 研究生学历, 无党派人士. 现任区人大常委会副主任、区工商联主席(无党派干部). 2026-08 公开接访公告: 聂永红与李立德到涟滨街道公开接访.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人大常委会", "title": "副主任、区工商联主席", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "无党派人士", "confidence": "confirmed", "source_ids": ["S016", "S014"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 31, "name": "周红", "gender": "女", "ethnicity": "汉族",
        "birth": "1972-10", "birthplace": "", "education": "大学学历, 学士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会副主任", "current_org": "娄星区人大常委会",
        "source": "S016",
        "profile_notes": "周红, 女, 汉族, 1972年10月生, 大学学历, 学士学位, 中共党员. 现任区人大常委会副主任(联系教育科学文化卫生委员会等).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人大常委会", "title": "副主任", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 32, "name": "彭海燕", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-10", "birthplace": "", "education": "大学学历, 学士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会副主任", "current_org": "娄星区人大常委会",
        "source": "S016",
        "profile_notes": "彭海燕, 男, 汉族, 1975年10月生, 大学学历, 学士学位, 中共党员. 现任区人大常委会党组成员、副主任(联系农业与农村、环资委).",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人大常委会", "title": "副主任", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 33, "name": "王迎灿", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-01", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会副主任、区总工会主席", "current_org": "娄星区人大常委会",
        "source": "S016",
        "profile_notes": "王迎灿, 男, 汉族, 1973年1月生, 大学学历, 中共党员. 现任区人大常委会党组成员、副主任, 区总工会主席.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄星区人大常委会", "title": "副主任、区总工会主席", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    # ── 34-40. 区政协 + 前任政协主席 ──
    {
        "id": 34, "name": "徐迪仁", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-02", "birthplace": "", "education": "大学学历, 学士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协党组书记、主席", "current_org": "政协娄底市娄星区委员会",
        "source": "S016",
        "profile_notes": "徐迪仁, 男, 汉族, 1968年2月生, 大学学历, 学士学位, 中共党员. 现任娄星区政协党组书记、主席, 主持区政协全面工作(负责市城发集团、创发集团、万宝投等项目建设协调). 领导之窗侧栏自2018-10即有简历页(政协副主席), 后于前任主席邓伟卸任后接任主席(具体时间待核, 约2024-2025).",
        "career": [
            {"start": "unknown", "end": "2024-12", "org": "政协娄底市娄星区委员会", "title": "区政协副主席", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "2018-10 起有领导之窗简历页(原为副主席)", "confidence": "plausible", "source_ids": ["S016"]},
            {"start": "2025-01", "end": "present", "org": "政协娄底市娄星区委员会", "title": "党组书记、主席", "level": "县", "system": "other", "rank": "正处级", "is_key_promotion": True, "notes": "接前任邓伟任主席(确切就任日期待核)", "confidence": "plausible", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "local_ladder", "systems": ["other"], "geo": []},
    },
    {
        "id": 35, "name": "童松闾", "gender": "男", "ethnicity": "汉族",
        "birth": "1967-02", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协党组副书记、副主席", "current_org": "政协娄底市娄星区委员会",
        "source": "S016",
        "profile_notes": "童松闾, 男, 汉族, 1967年2月生, 大学学历, 中共党员. 现任区政协党组副书记、副主席, 协助主席主持区政协日常工作.",
        "career": [
            {"start": "unknown", "end": "present", "org": "政协娄底市娄星区委员会", "title": "党组副书记、副主席", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 36, "name": "肖建军", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-12", "birthplace": "", "education": "大专学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协党组成员、副主席", "current_org": "政协娄底市娄星区委员会",
        "source": "S016",
        "profile_notes": "肖建军, 男, 汉族, 1970年12月生, 大专学历, 中共党员. 现任区政协党组成员、副主席.",
        "career": [
            {"start": "unknown", "end": "present", "org": "政协娄底市娄星区委员会", "title": "副主席", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 37, "name": "王文成", "gender": "女", "ethnicity": "汉族",
        "birth": "1969-02", "birthplace": "", "education": "大学学历",
        "party_join": "民盟", "work_start": "",
        "current_post": "区政协副主席(兼), 民盟娄星区委主委", "current_org": "政协娄底市娄星区委员会",
        "source": "S016",
        "profile_notes": "王文成, 女, 汉族, 1969年2月生, 大学学历, 民盟成员. 现任区政协副主席、民盟娄星区委主委(兼)、市政协提案委员会副主任(兼).",
        "career": [
            {"start": "unknown", "end": "present", "org": "政协娄底市娄星区委员会", "title": "副主席(兼)", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "民主党派干部", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 38, "name": "王剑红", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-10", "birthplace": "", "education": "大学学历",
        "party_join": "九三学社", "work_start": "",
        "current_post": "区政协副主席(兼), 九三学社娄星区委主委", "current_org": "政协娄底市娄星区委员会",
        "source": "S016",
        "profile_notes": "王剑红, 男, 汉族, 1968年10月生, 大学学历, 九三学社成员. 现任区政协副主席(兼)、九三学社娄星区委主委、区计划生育协会会长(兼).",
        "career": [
            {"start": "unknown", "end": "present", "org": "政协娄底市娄星区委员会", "title": "副主席(兼)", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "民主党派干部", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": []},
    },
    {
        "id": 39, "name": "颜炜", "gender": "女", "ethnicity": "汉族",
        "birth": "1970-12", "birthplace": "", "education": "大学学历",
        "party_join": "无党派", "work_start": "",
        "current_post": "区政协副主席(兼), 区人民检察院四级高级检察官", "current_org": "政协娄底市娄星区委员会",
        "source": "S016",
        "profile_notes": "颜炜, 女, 汉族, 1970年12月生, 大学学历, 无党派人士. 现任区政协副主席(兼)、区人民检察院四级高级检察官.",
        "career": [
            {"start": "unknown", "end": "present", "org": "政协娄底市娄星区委员会", "title": "副主席(兼)", "level": "县", "system": "other", "rank": "副处级", "is_key_promotion": False, "notes": "法检系统兼政协", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other", "legal"], "geo": []},
    },
    {
        "id": 40, "name": "邓伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-04", "birthplace": "湖南省宁乡市", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任区政协主席(2026-01前已卸任, 去向待核)", "current_org": "政协娄底市娄星区委员会(前)",
        "source": "S013 S016",
        "profile_notes": "邓伟, 男, 汉族, 1972年4月生, 湖南宁乡人(维基), 中共党员. 2021年10月起任娄星区政协主席(十届). 2026-01 起的政协活动报道已由徐迪仁以主席身份出现, 显示邓伟约在2024-2025年间卸任(具体时间与去向未公开, 重点待核).",
        "career": [
            {"start": "2021-10", "end": "2025-12", "org": "政协娄底市娄星区委员会", "title": "主席", "level": "县", "system": "other", "rank": "正处级", "is_key_promotion": True, "notes": "2021-10就任(维基); 卸任时间约2024-2025待核", "confidence": "plausible", "source_ids": ["S013"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["other"], "geo": ["宁乡", "娄星"]},
    },
    # ── 41-45. 法检 + 市级关联节点 ──
    {
        "id": 41, "name": "罗立晖", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民法院院长", "current_org": "娄底市娄星区人民法院",
        "source": "S006 S010",
        "profile_notes": "娄星区人民法院院长(2026-06/07 区人大常委会会议列席人员名单). 履历待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄底市娄星区人民法院", "title": "院长", "level": "县", "system": "legal", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "geo": []},
    },
    {
        "id": 42, "name": "汤亮", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人民检察院检察长", "current_org": "娄底市娄星区人民检察院",
        "source": "S006 S010",
        "profile_notes": "娄星区人民检察院检察长(2026年区人大常委会会议列席名单). 履历待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "娄底市娄星区人民检察院", "title": "检察长", "level": "县", "system": "legal", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "geo": []},
    },
    {
        "id": 43, "name": "谢学龙", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "原娄底市委常委、常务副市长(2026-06-02 接受审查调查)", "current_org": "中共娄底市委员会",
        "source": "S012",
        "profile_notes": "娄底市委常委、市人民政府常务副市长(2026-06-02 湖南省纪委监委/三湘风纪通报接受纪律审查和监察调查). 官方通报未载明性别/出生信息, 本档案仅记录公开职务信息与案发时间. 娄底市级层面的重大风险信号——娄星区作为市委市政府驻地的中心城区, 市常务副市长被查对该区财政/项目条线的传导影响需关注.",
        "career": [
            {"start": "unknown", "end": "2026-06-02", "org": "娄底市人民政府", "title": "市委常委、常务副市长", "level": "地级市", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "2026-06-02 被查", "confidence": "confirmed", "source_ids": ["S012"]},
        ],
        "governance": [],
        "work_style": [],
        "risk": [
            {"type": "disciplinary_action", "description": "2026-06-02 湖南省纪委监委通报: 娄底市委常委、市人民政府常务副市长谢学龙接受纪律审查和监察调查", "date": "2026-06-02", "confidence": "confirmed", "source_ids": ["S012"]},
        ],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": ["娄底"]},
    },
    {
        "id": 44, "name": "章清", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "娄底市委常委、市委组织部部长", "current_org": "中共娄底市委员会",
        "source": "S003",
        "profile_notes": "娄底市委常委、市委组织部部长(2026-05-22 出席娄星区领导干部会议并宣布省委、市委决定——刘迟辉任区委书记). 组织人事条线市级主管. 履历待核.",
        "career": [
            {"start": "unknown", "end": "present", "org": "中共娄底市委员会", "title": "市委常委、组织部部长", "level": "地级市", "rank": "副厅级", "is_key_promotion": False, "notes": "2026-05-22 宣布娄星区人事安排", "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "organization_track", "systems": ["organization"], "geo": []},
    },
    {
        "id": 45, "name": "曾超群", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "娄底市委书记(2025.04-)", "current_org": "中共娄底市委",
        "source": "S016",
        "profile_notes": "娄底市委书记(2025-04 起, 与娄底市网络库一致)。娄星作为娄底中心城区, 区委书记向市委负责。来源: 娄底市政府/红网新闻调度记录.",
        "career": [
            {"start": "2025-04", "end": "present", "org": "中共娄底市委员会", "title": "市委书记", "level": "地级市", "rank": "正厅级", "is_key_promotion": False, "notes": "娄底市网络库收录", "confidence": "confirmed", "source_ids": ["S013"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["party"], "geo": []},
    },
    {
        "id": 46, "name": "何朝晖", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "娄底市人民政府市长(2025.11-)", "current_org": "娄底市人民政府",
        "source": "S016",
        "profile_notes": "娄底市人民政府市长(2025.11 起, 与娄底市网络库一致; 2026 多次到娄星区调研督导). 娄星区代理区长为市长的下级条线.",
        "career": [
            {"start": "2025-11", "end": "present", "org": "娄底市人民政府", "title": "市长", "level": "地级市", "rank": "正厅级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S016"]},
        ],
        "governance": [], "work_style": [], "risk": [],
        "extras": {"career_pattern": "unknown", "systems": ["government"], "geo": []},
    },
]

# ══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共娄底市娄星区委员会", "type": "党委", "level": "区", "parent": "中共娄底市委", "location": "湖南省娄底市娄星区"},
    {"id": 2, "name": "娄星区人民政府", "type": "政府", "level": "区", "parent": "娄底市人民政府", "location": "湖南省娄底市娄星区"},
    {"id": 3, "name": "娄底市娄星区人大常委会", "type": "人大", "level": "区", "parent": "娄底市人大常委会", "location": "湖南省娄底市娄星区"},
    {"id": 4, "name": "政协娄底市娄星区委员会", "type": "政协", "level": "区", "parent": "政协娄底市委员会", "location": "湖南省娄底市娄星区"},
    {"id": 5, "name": "中共娄底市娄星区纪律检查委员会(区监委)", "type": "纪委", "level": "区", "parent": "中共娄底市纪委", "location": "湖南省娄底市娄星区"},
    {"id": 6, "name": "娄底市公安局娄星分局", "type": "政法", "level": "区", "parent": "娄底市公安局", "location": "湖南省娄底市娄星区"},
    {"id": 7, "name": "娄底市娄星区人民武装部", "type": "军事", "level": "区", "parent": "娄底军分区", "location": "湖南省娄底市娄星区"},
    {"id": 8, "name": "娄底市娄星区人民法院", "type": "政法", "level": "区", "parent": "娄底市中级人民法院", "location": "湖南省娄底市娄星区"},
    {"id": 9, "name": "娄底市娄星区人民检察院", "type": "政法", "level": "区", "parent": "娄底市人民检察院", "location": "湖南省娄底市娄星区"},
    {"id": 10, "name": "娄星产业开发区", "type": "开发区", "level": "区级园区", "parent": "娄星区人民政府", "location": "湖南省娄底市娄星区"},
    {"id": 11, "name": "中共娄底市委员会", "type": "党委", "level": "地级市", "parent": "中共湖南省委", "location": "湖南省娄底市"},
    {"id": 12, "name": "娄底市人民政府", "type": "政府", "level": "地级市", "parent": "湖南省人民政府", "location": "湖南省娄底市"},
    {"id": 13, "name": "中共湖南省委", "type": "党委", "level": "省", "parent": "中共中央", "location": "湖南省长沙市"},
    {"id": 14, "name": "湖南省人民政府", "type": "政府", "level": "省", "parent": "国务院", "location": "湖南省长沙市"},
    {"id": 15, "name": "中共新化县圳上镇委员会", "type": "乡镇", "level": "乡镇", "parent": "中共新化县委", "location": "湖南省娄底市新化县"},
    {"id": 16, "name": "娄星区乐坪街道党工委", "type": "乡镇", "level": "街道", "parent": "中共娄底市娄星区委员会", "location": "湖南省娄底市娄星区"},
]

# ══════════════════════════════════════════════════════════════════════════
# POSITIONS (worked_at edges)
# ══════════════════════════════════════════════════════════════════════════
positions = [
    # 刘迟辉 (1)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-05-22", "end_date": "present", "rank": "正处级", "note": "2026-06-11 兼任区人武部党委第一书记; 2026-07-30 十届一次全会当选"},
    # 赖毅 (2)
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026-05-29", "end_date": "present", "rank": "副处级", "note": "2026-07-30 十届一次全会连任副书记"},
    {"person_id": 2, "org_id": 2, "title": "区人民政府党组书记、代理区长", "start_date": "2026-06-01", "end_date": "present", "rank": "正处级", "note": "区十一届人大常委会第四十次会议决定"},
    # 李彦文 (3)
    {"person_id": 3, "org_id": 1, "title": "区委书记", "start_date": "2018-10", "end_date": "2026-05-22", "rank": "正处级", "note": "2021-07 九届党代会连任"},
    # 刘志刚 (4)
    {"person_id": 4, "org_id": 2, "title": "区长", "start_date": "2021-10", "end_date": "2026-06-01", "rank": "正处级", "note": "因工作调动辞职"},
    # 向波 (5)
    {"person_id": 5, "org_id": 1, "title": "区委副书记", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "十届一次全会当选"},
    # 高英 (6)
    {"person_id": 6, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "兼区政协党组副书记"},
    # 彭连赐 (7)
    {"person_id": 7, "org_id": 5, "title": "区委常委、区纪委书记、区监委代理主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 李立德 (8)
    {"person_id": 8, "org_id": 1, "title": "区委常委、区委办公室主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 张迪凯 (9)
    {"person_id": 9, "org_id": 7, "title": "区委常委、区人武部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 胡红辉 (10)
    {"person_id": 10, "org_id": 2, "title": "副区长(2026-07起区委常委)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "工信/交通/金融信访条线"},
    # 吴彪雄 (11) 龙江波 (12) 阮丽萍 (13)
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "新进"},
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "新进"},
    {"person_id": 13, "org_id": 1, "title": "区委常委", "start_date": "2026-07-30", "end_date": "present", "rank": "副处级", "note": "新进"},
    # 周庶舟 (14)
    {"person_id": 14, "org_id": 2, "title": "常务副区长(九届区委常委至2026-07)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "发改/财政/税务/统计/应急"},
    # 王谦 (15)
    {"person_id": 15, "org_id": 2, "title": "副区长(九届区委常委至2026-07)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "民政/水利/农业农村/乡村振兴"},
    # 肖亮 (16)
    {"person_id": 16, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "unknown", "end_date": "2026-07", "rank": "副处级", "note": "换届后去向待核"},
    # 曾海军 (17)
    {"person_id": 17, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "unknown", "end_date": "2026-07", "rank": "副处级", "note": "换届后去向待核"},
    # 吕许灵 (18)
    {"person_id": 18, "org_id": 1, "title": "区委副书记、政法委书记", "start_date": "unknown", "end_date": "2026-07", "rank": "副处级", "note": "换届后去向待核"},
    # 唐爱华 (19) 周俊华 (20) 肖民海 (21)
    {"person_id": 19, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "娄星产业开发区、招商、涟钢周边"},
    {"person_id": 20, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "自然资源、住建、城管"},
    {"person_id": 21, "org_id": 2, "title": "副区长(非党)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "商务、市场监管"},
    # 谢劭 (22)
    {"person_id": 22, "org_id": 6, "title": "副区长兼娄星公安分局局长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "二级高级警长"},
    # 肖佺 (23)
    {"person_id": 23, "org_id": 15, "title": "新化县圳上镇党委书记", "start_date": "unknown", "end_date": "2026-07-09", "rank": "正科级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "副区长", "start_date": "2026-07-10", "end_date": "present", "rank": "副处级", "note": "跨县任职"},
    # 姚满文 (24)
    {"person_id": 24, "org_id": 2, "title": "区政府党组成员、办公室主任", "start_date": "unknown", "end_date": "present", "rank": "", "note": ""},
    # 邓函提 (25)
    {"person_id": 25, "org_id": 2, "title": "副区长(2026-06公示拟进一步使用)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "新职待核"},
    # 周璐 (26)
    {"person_id": 26, "org_id": 16, "title": "乐坪街道党工委书记", "start_date": "unknown", "end_date": "present", "rank": "正科级", "note": "2026-06公示拟任县市区政府副职"},
    # 区人大 (27-33)
    {"person_id": 27, "org_id": 3, "title": "人大常委会党组书记、主任", "start_date": "2021-10", "end_date": "present", "rank": "正处级", "note": "二级巡视员"},
    {"person_id": 28, "org_id": 3, "title": "人大常委会党组书记(候任主任)", "start_date": "unknown", "end_date": "present", "rank": "", "note": "陈晓林仍任主任"},
    {"person_id": 29, "org_id": 3, "title": "人大常委会党组副书记、副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 30, "org_id": 3, "title": "人大常委会副主任、区工商联主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "无党派"},
    {"person_id": 31, "org_id": 3, "title": "人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 32, "org_id": 3, "title": "人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 33, "org_id": 3, "title": "人大常委会副主任、区总工会主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 区政协 (34-40)
    {"person_id": 34, "org_id": 4, "title": "政协党组书记、主席", "start_date": "2025-01", "end_date": "present", "rank": "正处级", "note": "确任日期待核(约2024-2025)"},
    {"person_id": 35, "org_id": 4, "title": "政协党组副书记、副主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 36, "org_id": 4, "title": "政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 37, "org_id": 4, "title": "政协副主席(民盟)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 38, "org_id": 4, "title": "政协副主席(九三学社)", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 39, "org_id": 4, "title": "政协副主席(兼)、区检察院四级高级检察官", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 40, "org_id": 4, "title": "政协主席", "start_date": "2021-10", "end_date": "2025-12", "rank": "正处级", "note": "卸任时间待核"},
    # 法检 (41-42)
    {"person_id": 41, "org_id": 8, "title": "区人民法院院长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 42, "org_id": 9, "title": "区人民检察院检察长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 市级节点 (43-46)
    {"person_id": 43, "org_id": 12, "title": "娄底市委常委、常务副市长", "start_date": "unknown", "end_date": "2026-06-02", "rank": "副厅级", "note": "2026-06-02 被查"},
    {"person_id": 44, "org_id": 11, "title": "娄底市委常委、市委组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "2026-05-22 宣布娄星区人事"},
    {"person_id": 45, "org_id": 11, "title": "市委书记", "start_date": "2025-04", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 46, "org_id": 12, "title": "市长", "start_date": "2025-11", "end_date": "present", "rank": "正厅级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════
relationships = [
    # 现任党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "刘迟辉(书记)与赖毅(代理区长)自2026-05/06起搭班; 2026-07-30 十届党代会后双双连任(书记/副书记)", "overlap_org": "娄星区党政班子", "overlap_period": "2026-05/06至今"},
    # 前任主官链条
    {"person_a": 3, "person_b": 1, "type": "前后任书记交接", "context": "2026-05-22 全区领导干部会议: 李彦文不再担任区委书记(另有任用), 刘迟辉接任——省委、市委决定的书记更替", "overlap_org": "中共娄底区委", "overlap_period": "2026-05-22"},
    {"person_a": 4, "person_b": 2, "type": "前后任区长交接", "context": "2026-06-01 区人大第四十次会议: 刘志刚因工作调动辞去区长, 赖毅任命副区长并代理区长", "overlap_org": "娄星区人民政府", "overlap_period": "2026-06-01"},
    {"person_a": 3, "person_b": 4, "type": "党政正职搭档", "context": "李彦文(书记)与刘志刚(区长)2021.10-2026.05 搭班执政近五年", "overlap_org": "娄星区党政班子", "overlap_period": "2021-10至2026-05"},
    # 新班子内部分工
    {"person_a": 1, "person_b": 5, "type": "书记-副书记", "context": "2026-07-30 十届一次全会: 刘迟辉任书记、向波任副书记", "overlap_org": "中共娄底区委", "overlap_period": "2026-07-30至今"},
    {"person_a": 2, "person_b": 5, "type": "副书记并立", "context": "2026-07-30 赖毅与向波同时当选区委副书记(赖毅兼任政府)", "overlap_org": "中共娄底区委", "overlap_period": "2026-07-30至今"},
    {"person_a": 1, "person_b": 7, "type": "区委班子共事", "context": "刘迟辉与纪委彭连赐等十届常委会成员共事", "overlap_org": "中共娄底区委", "overlap_period": "2026-07-30至今"},
    {"person_a": 1, "person_b": 8, "type": "区委班子共事", "context": "刘迟辉与区委办主任李立德日常政务配合(2026-06/08信访、八一等活动同列)", "overlap_org": "中共娄底区委", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 9, "type": "党管武装上下级", "context": "刘迟辉任人武部党委第一书记(2026-06-11), 张迪凯(人武部部长、常委)", "overlap_org": "娄星区人民武装部", "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 14, "type": "政府常务搭档", "context": "代理区长赖毅与常务副区长周庶舟政府班子常务运作", "overlap_org": "娄星区人民政府", "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 10, "type": "政府班子搭档", "context": "赖毅(代区长)与胡红辉(副区长, 2026-07 升区委常委)", "overlap_org": "娄星区人民政府", "overlap_period": "2026-06至今"},
    {"person_a": 10, "person_b": 19, "type": "政府条线搭档", "context": "胡红辉与唐爱华同任副区长(工信/金融 vs 园区/招商)对接产业条线", "overlap_org": "娄星区人民政府", "overlap_period": "2026"},
    {"person_a": 22, "person_b": 2, "type": "政府班子搭档", "context": "谢劭(副区长、公安局长)在区政府班子内", "overlap_org": "娄星区人民政府", "overlap_period": "2026"},
    {"person_a": 23, "person_b": 2, "type": "政府班子搭档", "context": "肖佺(2026-07-10任副区长)入席区政府班子运作", "overlap_org": "娄星区人民政府", "overlap_period": "2026-07至今"},
    # 区四大班子
    {"person_a": 27, "person_b": 3, "type": "四大班子共事", "context": "人大常委会主任陈晓林(2021-10起)与前任书记李彦文、前任区长刘志刚同届搭班", "overlap_org": "娄星区四套班子", "overlap_period": "2021-10至2026-05"},
    {"person_a": 27, "person_b": 28, "type": "人大领导交接", "context": "陈晓林仍任主任, 陈颂飞已任人大常委会党组书记——人大换届交接期(新一届人代会待开)", "overlap_org": "娄星区人大常委会", "overlap_period": "2026-06至今"},
    {"person_a": 34, "person_b": 40, "type": "前后任政协主席", "context": "徐迪仁接替邓伟任区政协主席(接任约2024-2025, 具体时间待核)", "overlap_org": "政协娄底市娄星区委员会", "overlap_period": "2025"},
    {"person_a": 34, "person_b": 30, "type": "政协-工商联联动", "context": "徐迪仁(主席)与聂永红(副主席兼工商联)在区政协十届(2026 两会等)活动共事", "overlap_org": "娄星区政协/工商联", "overlap_period": "2026"},
    # 人事任命链
    {"person_a": 44, "person_b": 1, "type": "组织任命链", "context": "2026-05-22 市委常委、组织部部长章清出席娄星区领导干部会议宣布刘迟辉任区委书记——市委组织部主推的区县正职任命", "overlap_org": "娄底市委组织部", "overlap_period": "2026-05-22"},
    {"person_a": 44, "person_b": 2, "type": "组织任命链", "context": "2026-05-29 市委组织部副部长周向红宣布赖毅任区委副书记——市委组织部推进的政府正职接班人", "overlap_org": "娄底市委组织部", "overlap_period": "2026-05-29"},
    {"person_a": 45, "person_b": 1, "type": "市-区上下级", "context": "娄底市委书记曾超群与娄星区委书记刘迟辉的市-区上下级领导关系", "overlap_org": "娄底市/娄星区", "overlap_period": "2026"},
    {"person_a": 46, "person_b": 2, "type": "市-区上下级", "context": "娄底市长何朝晖与娄星区代理区长赖毅的上下级关系(2026 起多至娄星区调研督导)", "overlap_org": "娄底市政府/娄星区政府", "overlap_period": "2026"},
    # 风险传导
    {"person_a": 43, "person_b": 45, "type": "市级班子风险传导", "context": "常务副市长谢学龙 2026-06-02 被查——娄底市委班子重大风险事件, 波及中心城区娄星(财政/项目条线)", "overlap_org": "娄底市", "overlap_period": "2026-06"},
    # 换届重组
    {"person_a": 16, "person_b": 5, "type": "换届交接", "context": "肖亮(原组织部长)退出十届常委会, 向波(新副书记)等进入", "overlap_org": "中共娄底区委", "overlap_period": "2026-07-30"},
    {"person_a": 18, "person_b": 5, "type": "换届交接", "context": "原副书记吕许灵换届后退出(未再当选), 向波接任副书记", "overlap_org": "中共娄底区委", "overlap_period": "2026-07-30"},
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
    for person in persons:
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})",
                     [person.get(c, "") for c in cols_p])
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for org in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})",
                     [org.get(c, "") for c in cols_o])
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})",
                     [pos.get(c, "") for c in cols_pos])
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for rel in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})",
                     [rel.get(c, "") for c in cols_r])
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
    if ("书记" in t and "副" not in t) and "纪委" not in t:
        return "221,74,56"      # 红色: 党委书记/区委书记
    if "区长" in t or "市长" in t or "代理区长" in t:
        return "68,114,196"     # 蓝色: 政府正职
    if "纪委" in t or "监委" in t:
        return "249,140,42"     # 橙色: 纪检
    if "主任" in t or "主席" in t:
        return "194,134,56"     # 金棕: 人大/政协
    if "常委" in t:
        return "155,120,200"    # 紫: 区委常委
    if "部长" in t:
        return "155,120,200"
    if "局长" in t or "公安" in t or "法院" in t or "检察" in t:
        return "120,160,200"    # 法政
    return "130,130,130"


def org_color(otype):
    return {
        "党委": "255,200,200", "政府": "200,200,255", "纪委": "255,200,150",
        "开发区": "200,255,200", "乡镇": "255,255,200", "事业单位": "220,220,220",
        "人大": "200,255,255", "政协": "255,240,200", "政法": "200,220,255",
        "军事": "230,230,230",
    }.get(otype, "200,200,200")


def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>娄星区领导班子工作关系网络 — 区委书记/区长双核心, 含前任主官、第十届区委常委会、区政府/人大/政协班子、法检与市级关联节点</description>')
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
    top = {1, 2, 3, 4, 5, 43, 44, 45, 46}
    for person in persons:
        c = person_color(person.get("current_post", ""))
        sz = "20.0" if person["id"] in top else ("12.0" if person["id"] <= 42 else "10.0")
        lines.append(f'      <node id="p{person["id"]}" label="{esc(person["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(person.get("current_post", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        cr, cg, cb = c.split(",")
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for org in organizations:
        c = org_color(org["type"])
        cr, cg, cb = c.split(",")
        lines.append(f'      <node id="o{org["id"]}" label="{esc(org["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(org["type"])}"/>')
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
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(rel["overlap_period"])}"/>')
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
    for entry in p.get("career", []):
        career_timeline.append({
            "start": entry.get("start") or "unknown", "end": entry.get("end") or "present",
            "org": entry.get("org", ""), "title": entry.get("title", ""),
            "level": entry.get("level", ""), "location": "湖南省娄底市",
            "system": entry.get("system", "other"), "rank": entry.get("rank", ""),
            "is_key_promotion": entry.get("is_key_promotion", False),
            "notes": entry.get("notes", ""),
            "confidence": entry.get("confidence", "confirmed"),
            "source_ids": entry.get("source_ids", []),
        })
    for pos in positions:
        if pos["person_id"] != pid:
            continue
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
        elif "公安" in title or "政法" in title or "维稳" in title:
            system = "public_security"
        elif "纪委" in title or "监委" in title:
            system = "discipline"
        elif "政府" in title or "区长" in title or "市长" in title or "镇" in title or "街道" in title:
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
            "title": p.get("current_post", ""), "level": "县处级", "location": "湖南省娄底市娄星区",
            "system": "other", "rank": "", "is_key_promotion": False,
            "notes": "公开资料有限, 任职起始时间待核。", "confidence": "unverified", "source_ids": [],
        })
    rels = []
    for rel in relationships:
        if rel["person_a"] == pid or rel["person_b"] == pid:
            other = rel["person_b"] if rel["person_a"] == pid else rel["person_a"]
            other_name = next((x["name"] for x in persons if x["id"] == other), str(other))
            rels.append({
                "person": other_name, "person_id": f"louxing_{other}",
                "relationship_type": rel["type"], "strength": "medium",
                "evidence": rel["context"], "overlap_org": rel["overlap_org"],
                "overlap_period": rel["overlap_period"], "direction": "undirected",
                "confidence": "confirmed", "source_ids": [],
            })
    src_ids = [s for s in p.get("source", "").replace(",", " ").split() if s]
    source_register = [dict(s) for s in SOURCES if s["id"] in src_ids]
    open_qs = []
    if not p.get("birth"):
        open_qs.append({"priority": "high", "question": f"{p['name']}出生年月缺失", "why_it_matters": "识别身份稳定性", "suggested_queries": [f"{p['name']} 简历"], "last_attempted": AS_OF})
    if not p.get("birthplace"):
        open_qs.append({"priority": "medium", "question": f"{p['name']}籍贯缺失", "why_it_matters": "地域网络分析", "suggested_queries": [f"{p['name']} 籍贯"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_qs.append({"priority": "medium", "question": f"{p['name']}参加工作年份缺失", "why_it_matters": "履历完整性", "suggested_queries": [f"{p['name']} 任前公示"], "last_attempted": AS_OF})
    if pid in (1, 2):
        open_qs.append({"priority": "critical", "question": f"{p['name']} 2026年履任{('区委书记' if pid==1 else '代理区长')}前的前职与完整履历未公开", "why_it_matters": "核心正职衔接网络", "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 娄底 任前公示"], "last_attempted": AS_OF})
    if pid == 3:
        open_qs.append({"priority": "critical", "question": "李彦文 2026-05-22 卸任娄星区委书记后'另有任用'的新职务未公开", "why_it_matters": "前任去向追踪与前向网络", "suggested_queries": ["李彦文 新任职", "李彦文 娄底 2026"], "last_attempted": AS_OF})
    if pid == 4:
        open_qs.append({"priority": "critical", "question": "刘志刚 2026-06-01 因工作调动辞去娄星区区长后去向未公开", "why_it_matters": "前任去向追踪", "suggested_queries": ["刘志刚 娄底 新职 2026"], "last_attempted": AS_OF})
    if pid in (5, 11, 12, 13):
        open_qs.append({"priority": "high", "question": f"{p['name']} 2026-07 新进(任)区委常委会前的职务与分工未公开", "why_it_matters": "新班子网络", "suggested_queries": [f"{p['name']} 娄星 简历"], "last_attempted": AS_OF})
    if pid == 40:
        open_qs.append({"priority": "high", "question": "邓伟卸任娄星区政协主席的具体时间与去向未公开", "why_it_matters": "政协序列前向网络", "suggested_queries": ["邓伟 娄星 卸任"], "last_attempted": AS_OF})
    if pid == 28:
        open_qs.append({"priority": "high", "question": "陈颂飞任区人大常委会党组书记前的职务与履历未公开", "why_it_matters": "人大换届人事安排", "suggested_queries": ["陈颂飞 娄底 简历"], "last_attempted": AS_OF})
    if pid == 25:
        open_qs.append({"priority": "medium", "question": "邓函提'拟进一步使用'(2026-06公示)的新职务去向", "why_it_matters": "区政府班子变动", "suggested_queries": ["邓函提 2026 任命"], "last_attempted": AS_OF})
    governance = p.get("governance", []) or []
    style = p.get("work_style", []) or []
    risks = p.get("risk", []) or []
    if not risks:
        risks = [{"type": "none_found", "description": f"截至{AS_OF}未检索到{p['name']}本人的纪律处分或负面报道", "date": AS_OF, "confidence": "unverified", "source_ids": []}]
    extras = p.get("extras", {})
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "湖南省", "city": "娄底市", "region": "娄星区", "job": p.get("current_post", ""), "task_id": "hunan_娄星区", "time_focus": "2018-2026"},
        "identity": {"person_id": f"louxing_{p['name']}_{p.get('birth', '')[:4]}", "name": p["name"], "aliases": [], "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""), "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""), "native_place": "", "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}], "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""), "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth', '')}", "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}", "official_profile_url": ""}},
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
    fname = f"{TODAY}-湖南省-娄底市-{job_slug}-{p['name']}.json"
    fpath = Path(JSON_DIR) / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return fname


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
def main() -> None:
    print("=" * 60)
    print("  娄星区领导班子工作关系网络 — 数据构建")
    print(f"  调查日期: {AS_OF}  任务: hunan_娄星区")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Person JSONs:")
    for person in persons:
        fname = write_person_json(person)
        print(f"  {fname}")
    print("\nDone.")
    print(f"DB:    {DB_PATH}")
    print(f"GEXF:  {GEXF_PATH}")


if __name__ == "__main__":
    main()
