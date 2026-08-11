#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 洮南市 (Taonan), 吉林省.

Investigation date: 2026-08-11
Task ID: jilin_洮南市
Province: 吉林省
Parent city: 白城市
Level: 县级市
Targets: 市委书记 & 市长

Research sources (all accessed via HTTP 2026-08-11):
  - http://www.taonan.gov.cn/   洮南市人民政府门户网站 (primary)
    - /zfjg/szfld/ 市政府领导班子简历页（市长/副市长官方简历）
    - 站内检索 (TRS WAS5, channelid=247054): 市委常委会/人大/政协新闻
  - http://www.jlbc.gov.cn/     白城市人民政府网站（高熙礼任白城副市长官方简历）
  - http://zh.wikipedia.org/wiki/洮南市 (区划背景，无领导名单)

Network constraints this environment: HTTPS blocked; Baidu/Exa/Bing/Google/Jina
unavailable; only official 政府站 HTTP reachable. Hence 高熙礼任书记前完整履历、
2022-2023 洮南市委书记姓名、闫政/闫阔/贺亮 具体常委职务、吴爽/谢复强 2026 去向等
均已写入 open_questions / report gaps（partial-evidence artifact mode）。

Confidence:
  - 徐鹏、赵云、朱晓、肖鑫磊、丁长欣、于凯、张弘、史明玉、吴爱生、张凯函: confirmed
    from 市政府领导简介页（官方简历原文）
  - 刘明伟、董伟、贾作辉、吕宁、马芝源、欧阳传志、刘宇: confirmed 职务 from 官方新闻
  - 薛智金/于洪友/赵文博/韩雷/刘洋: confirmed 职务史实，细节待补
  - 2022-2023 洮南市委书记身份 open (critical)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

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
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401 (kept for reference)

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "洮南市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-11"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_洮南市"
if _CURRENT_DIR.name == "jilin_洮南市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

SRC_GOV = "http://www.taonan.gov.cn/"
SRC_BC = "http://www.jlbc.gov.cn/zfjg_3101/szfld/fsz/lhz_23358/"

# ── Persons ──────────────────────────────────────────────────────────────────
# 1 书记, 2 市长, 3-11 政府班子, 12 人大主任, 13 政协主席,
# 14-21 市委其他常委, 22-28 前任/近期变动
persons = [
    {
        "id": 1, "name": "高熙礼", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年9月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共洮南市委",
        "source": SRC_BC,
        "confidence": "confirmed",
        "notes": "白城官方简历：'高熙礼，男，汉族，1982年9月生，研究生学历，中共党员。现任 白城市副市长、市政府党组成员，洮南市委书记。' 洮南本地时间线（官方新闻/大事记）：2021年 任洮南市委常委、副市长并转常务副市长；2021-11 洮南市十九届人大一次会议当选市长；2023-12 仍以市长身份主持市政府党组会议；2024-02 官方记载为'市委书记、市长'（一肩挑）；2024-10-25 徐鹏全票当选市长后专任书记；2026-07 新闻头衔均为'白城市政府副市长、洮南市委书记'。 2008-2021 年完整履历为 open question。",
    },
    {
        "id": 2, "name": "徐鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年2月", "birthplace": "吉林桦甸",
        "education": "本科（白城师范学院汉语言文学专业）",
        "party_join": "中共党员", "work_start": "2003年8月",
        "current_post": "市委副书记、市长",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/zfjg/szfld/sz/wth/",
        "confidence": "confirmed",
        "notes": "官方简历原文：'徐鹏，汉族，1979年2月出生，吉林桦甸人，2003年8月参加工作， 2005年6月加入中国共产党。白城师范学院汉语言文学专业本科学历。曾任白城市纪委纠风室 副主任科员、主任科员，白城市纪委执法监察室副主任，白城市纪委第五纪检监察室副主任， 白城市纪委第三调查室主任，白城市纪委市监委第九调查室主任，白城市监委委员、市纪委市监委 第九调查室主任，洮南市委常委、纪委书记、监委副主任（代主任），洮南市委常委、纪委书记、 监委主任，白城市审计局局长、党组书记，现任中共洮南市委副书记、洮南市人民政府党组书记、 市长。' 2024-03 曾任洮南市委常委、常务副市长；2024-10-25 洮南市十九届人大四次会议全票 当选市长。主持市政府全面工作，主管市审计局。",
    },
    # ══ 政府班子（现任，官方简历 confirmed）══
    {
        "id": 3, "name": "赵云", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年8月", "birthplace": "黑龙江密山",
        "education": "研究生（吉林省委党校公共经济管理专业）",
        "party_join": "中共党员", "work_start": "2006年7月",
        "current_post": "市委常委、常务副市长",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/zfjg/szfld/fsz/swb_23252/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任共青团大安市委副书记、书记，大安市烧锅镇乡党委副书记、乡长， 洮南市人民政府副市长，现任洮南市委常委、市政府党组副书记、副市长（常务）。协助市长 代管审计局，分管经开区/财政/发改/应急/人社/能源。",
    },
    {
        "id": 4, "name": "朱枫", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年1月", "birthplace": "吉林镇赉",
        "education": "本科（吉林农业大学农业经济管理专业）",
        "party_join": "中共党员", "work_start": "2002年11月",
        "current_post": "市委常委、副市长",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/zfjg/szfld/fsz/swb_23257/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任白城市农村集体资产管理局科员，农村集体资产管理中心副主任， 白城市农业农村局科长、副局长、党组成员；现任洮南市委常委、副市长。",
    },
    {
        "id": 5, "name": "丁长欣", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年9月", "birthplace": "吉林洮南",
        "education": "大专（通榆师范学校汉语言文学专业）",
        "party_join": "中共党员", "work_start": "1996年9月",
        "current_post": "副市长",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/jfjg/szfld/fsz/ljc_31878/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任洮南市劳动和社会保障局副局长，经济开发区招商局局长，市人社局 副局长，劳动就业服务局局长，商贸国有资产运营公司党委书记、总经理，市城管局党委书记、 局长，市住建局党组书记、局长，吉林洮南经济开发区党工委书记、管委会主任；2025-12-26 经人大常委会任命为副市长（分管住建/城管）。",
    },
    {
        "id": 6, "name": "于凯", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年7月", "birthplace": "吉林白城",
        "education": "本科（吉林工学院自动化专业）",
        "party_join": "中国民主建国会", "work_start": "2004年12月",
        "current_post": "副市长",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/jfjg/szfld/fsz/swb_31456/",
        "confidence": "confirmed",
        "notes": "民主党派（民建）副市长。官方简历：曾任白城市震害防御工程研究中心工程师， 白城市地震局执法支队支队长、震害防御科科长、副局长；现任洮南市副市长。",
    },
    {
        "id": 7, "name": "张弘", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年6月", "birthplace": "吉林洮南",
        "education": "本科（吉林农业大学农林经济管理专业）",
        "party_join": "中共党员", "work_start": "2000年7月",
        "current_post": "副市长",
        "current_org": "洮南市人民政府",
        "source": "http://www.tn.gov.cn/zjld/fsz/swb_31451/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任洮南市委组织部干部监督室主任，组织部副部长、非公企业和社会 组织党工委书记，黑水镇党委书记，洮南市委办公室主任；现任洮南市副市长（分管农业农村/ 水利/林草）。组织系统出身（组织→乡镇→市委办→政府）。",
    },
    {
        "id": 8, "name": "史明玉", "gender": "女", "ethnicity": "汉族",
        "birth": "1988年9月", "birthplace": "吉林镇赉",
        "education": "硕士研究生（长春理工大学外国语学院外国语言文学）",
        "party_join": "中共党员", "work_start": "2011年8月",
        "current_post": "副市长",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/jfjg/szfld/fsz/swb_23247/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任镇赉县黑鱼泡镇党委副书记、镇长，镇赉县妇联主席，现任洮南市 副市长（分管教科文卫体旅）。",
    },
    {
        "id": 9, "name": "吴爱生", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年2月", "birthplace": "吉林大安",
        "education": "吉林大学法学院（法律专业）",
        "party_join": "中共党员", "work_start": "2001年4月",
        "current_post": "副市长、市公安局局长",
        "current_org": "洮南市公安局",
        "source": "http://www.taonan.gov.cn/jfjg/szfld/fsz/zdw_30932/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任白城市公安局国保支队副支队长，国内安全保卫机动侦察队队长， 政治安全保卫支队支队长，经济开发区分局局长；现任洮南市人民政府党组成员、副局长、 市公安局党委书记、局长、督察长（2025 年接替韩雷）。",
    },
    {
        "id": 10, "name": "肖鑫磊", "gender": "男", "ethnicity": "汉族",
        "birth": "1987年2月", "birthplace": "黑龙江方正",
        "education": "大学（黑龙江科技学院化学工程与工艺专业）",
        "party_join": "中共党员", "work_start": "2010年7月",
        "current_post": "副市长（挂职）",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/jfjg/szd/fsz/lhc_31588/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任吉林省煤业集团规划发展部业务副主管、非煤事业部业务主管， 长春东煤高技术股份有限公司总经理助理、党群工作部部长、纪委书记；现挂职洮南市副市长 （协助分管能源/热电）。国企系统。",
    },
    {
        "id": 11, "name": "张凯函", "gender": "女", "ethnicity": "回族",
        "birth": "1986年12月", "birthplace": "吉林长春",
        "education": "研究生（吉林大学商学院工商管理）",
        "party_join": "中共党员", "work_start": "2008年7月",
        "current_post": "副市长（挂职）",
        "current_org": "洮南市人民政府",
        "source": "http://www.taonan.gov.cn/jfjg/szt/fsz/ljc_23292/",
        "confidence": "confirmed",
        "notes": "官方简历：曾任吉林省农发集团投融资管理部部长、农业现代产业基金执行董事、 省三侬数字科技执行董事、省农发粮食集团副总经理；现挂职洮南副市长（金融/粮食，协助赵云）。",
    },
    # ═══════════════════ 人大 / 政协 ═══════════════════
    {
        "id": 12, "name": "刘明伟", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "洮南市人民代表大会常务委员会",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2025 起任市人大常委会主任（2025-02 纪委全会及 2025-12 人大常委会均以此职在任）。 此前 2024-02/04 为'市委常委、纪委书记、监委主任'（作纪委全会工作报告）。履历细节 open。",
    },
    {
        "id": 13, "name": "董伟", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协洮南市委员会",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2026-01-07 政协洮南市十六届第五次全会主席台前排（市政协主席）；2026-04-10 主持政协16届21次常委会议。前任石文博。履历细节 open。",
    },
    # ═══════════════════ 市委其他常委（现任） ═══════════════════
    {
        "id": 14, "name": "刘宇", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2026-03 市委编委会议确认其为市委副书记；2026-01 党建扩大会出席。履历细节 open。",
    },
    {
        "id": 15, "name": "贾作辉", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共洮南市纪律检查委员会",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2025-03 十六届市委第五轮巡察动员会：市委常委、市纪委书记、市监委主任、 市委巡察工作领导小组组长（出席并作讲话）；2025-10 第六轮巡察亦以此职出现。前任为刘明伟。",
    },
    {
        "id": 16, "name": "吕宁", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2021-08 换届期间任市委常委、组织部部长；2022-08 兼党校校长；2024-03/04/11、 2025-03 巡察会均为市委常委、组织部长。履历细节 open。",
    },
    {
        "id": 17, "name": "马浩源", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2025-12 宣讲报道：'市委宣讲团成员、市委常委、宣传部长马浩源'；2025-11 中央组 发言、2026-01 党建扩大会出席。履历细节 open。",
    },
    {
        "id": 18, "name": "欧阳传志", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市人武部政委",
        "current_org": "洮南市人民武装部",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2024-11 市委全会出席名单、2025-08-01 八一慰问均以'市委常务、人武部政委欧阳传志' 出现。军队系统。",
    },
    {
        "id": 19, "name": "闫政", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委（具体职务待确认）",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "plausible",
        "notes": "2025-08 双拥会/招商引资培训会（市领导）、2026-01 市委常委会（扩）出席； 2025-08 市委中心组研讨发言（国家安全/保密主题）。具体职务 open。",
    },
    {
        "id": 20, "name": "闫阔", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委（具体职务待确认）",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "plausible",
        "notes": "2025-06 政府党组会列席、2025-08 双拥会、2026-01 党建扩大会均以'市领导'身份 出现。具体职务待确认。",
    },
    {
        "id": 21, "name": "贺亮", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委（具体职务待确认）",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "plausible",
        "notes": "2026-01 党建扩大会出席；2026-06 理论学习中心组发言（正确政绩观）。职务待确认。",
    },
    # ═══════════════════ 前任 / 近期变动 ═══════════════════
    {
        "id": 22, "name": "薛智金", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2021 洮南大事记多次以'白城市委常委、洮南市委书记薛智金'出现；2023-07 洮南新闻 中已以'白城市委常委、宣传部长薛智金'身份出现于白城宣传系统培训班开班式讲话。即约 2022 年 由洮南书记调任白城市委常委、宣传部长。调任精确时间未查实。",
    },
    {
        "id": 23, "name": "于洪友", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市人大常委会主任",
        "current_org": "洮南市人民代表大会常务委员会",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2021 大事记-2024 在位：2021-11 十九届人大一次会（人大常委会主任于洪友主持）， 2024-10-25 人代会与高熙礼分别主持，2024-11 市委全会名单仍为'市人大常委会主任于洪友'； 约 2025 年起由 刘明伟 接任。去向 open question。",
    },
    {
        "id": 24, "name": "石文博", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市政协主席",
        "current_org": "政协洮南市委员会",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2021 曾任市委常委、副市长；2024-12 政协十六届四次全会任主席并作常委会工作报告； 2025-08 政协常委会仍在；2026-01-07 政协十六届五中全会由 董伟 接任主席。去向 open。",
    },
    {
        "id": 25, "name": "吴爽", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委副书记（原宣传部长）",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2023-07 为市委常委、宣传部长（培训班开班仪式讲话）；2024-03 环保会仍为宣传部长； 2024-11 全会名单'市委副书记吴爽'；2024-08-01 至 2025 均为副书记在任；2026 洮南新闻名单中 消失，去向 open。",
    },
    {
        "id": 26, "name": "谢复强", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委常委、政法委书记",
        "current_org": "中共洮南市委",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2024-03/04/11 官方新闻均为'市委常委、政法委书记谢复强'；2025 年后洮南新闻中 未再出现，去向 open question。",
    },
    {
        "id": 27, "name": "韩雷", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任副市长、市公安局局长",
        "current_org": "洮南市公安局",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2023-01（警察节升旗仪式）、2024-07 双拥慰问均以'副市长、公安局长韩雷'出现； 2025 年由吴爱生接任公安局长。去向 open question。",
    },
    {
        "id": 28, "name": "刘洋", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "原副市长（2025-09 免职）",
        "current_org": "洮南市人民政府",
        "source": SRC_GOV,
        "confidence": "confirmed",
        "notes": "2024-03 至 2025-08 为洮南市政府副市长（多次会议出席）；2025-09-03 市人大 第十八次会议免去其副市长职务。免职原因/去向 open（未见违纪通报）。",
    },
]

# ═══════════════════ Organizations ───────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共洮南市委", "type": "党委", "level": "县处级", "parent": "中共白城市委", "location": "洮南市"},
    {"id": 2, "name": "洮南市人民政府", "type": "政府", "level": "县处级", "parent": "白城市人民政府", "location": "洮南市"},
    {"id": 3, "name": "洮南市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "白城市人大常委会", "location": "洮南市"},
    {"id": 4, "name": "政协洮南市委员会", "type": "政协", "level": "县处级", "parent": "政协白城市委员会", "location": "洮南市"},
    {"id": 5, "name": "洮南市公安局", "type": "政府", "level": "正科级", "parent": "洮南市人民政府", "location": "洮南市"},
    {"id": 6, "name": "中共洮南市纪律检查委员会（监委）", "type": "纪委", "level": "县处级", "parent": "中共洮南市委", "location": "洮南市"},
    {"id": 7, "name": "洮南市人民武装部", "type": "军队", "level": "县处级", "parent": "白城军分区", "location": "洮南市"},
    {"id": 8, "name": "吉林洮南经济开发区", "type": "开发区", "level": "县处级", "parent": "洮南市人民政府", "location": "洮南市"},
    {"id": 9, "name": "白城市人民政府", "type": "政府", "level": "地厅级", "parent": "吉林省人民政府", "location": "白城市"},
    {"id": 10, "name": "中共白城市委", "type": "党委", "level": "地厅级", "parent": "中共吉林省委", "location": "白城市"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Positions
# ─────────────────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-01", "end_date": "", "rank": "县处级", "note": "2024-01~10 一肩挑；2024-10 后专任书记"},
    {"person_id": 1, "org_id": 9, "title": "白城市副市长、市政府党组成员", "start_date": "", "end_date": "", "rank": "副厅级", "note": "官方简历确认；到任时间 open"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2021-11", "end_date": "2024-10", "rank": "县处级", "note": "十九届人大一次会议当选"},
    {"person_id": 1, "org_id": 2, "title": "常务副市长", "start_date": "2021", "end_date": "2021-11", "rank": "县处级", "note": "大事记2021"},
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "2024-10", "end_date": "", "rank": "县处级", "note": "2024-10-25 全票当选"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024-08", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "常务副市长", "start_date": "2024-03", "end_date": "2024-10", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "白城市审计局局长、党组书记", "start_date": "", "end_date": "2024", "rank": "正处级", "note": "来洮前职务"},
    {"person_id": 2, "org_id": 6, "title": "市委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "县处级", "note": "历任职务"},
    {"person_id": 3, "org_id": 2, "title": "常务副市长（市政府党组副书记）", "start_date": "2025", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "2025", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "常委副市长"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "2025-12", "end_date": "", "rank": "县处级", "note": "2025-12-26 人大常委会任命"},
    {"person_id": 5, "org_id": 8, "title": "经开区党工委书记、管委会主任", "start_date": "", "end_date": "2025-12", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "民建"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "农业农村/水利"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "教科文卫"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "2025", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "市公安局局长、督察长", "start_date": "2025", "end_date": "", "rank": "县处级", "note": "接韩雷"},
    {"person_id": 10, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "县处级", "note": "省煤业集团系"},
    {"person_id": 11, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "县处级", "note": "省农发集团系"},
    {"person_id": 12, "org_id": 3, "title": "市人大常委会主任", "start_date": "2025", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "市委常委、纪委书记、监委主任", "start_date": "2024", "end_date": "2024-12", "rank": "县处级", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "市政协主席", "start_date": "2026-01", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市委副书记", "start_date": "2025", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "市委常委、纪委书记、监委主任", "start_date": "2025-01", "end_date": "", "rank": "县处级", "note": "接刘明伟"},
    {"person_id": 16, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "2021-08", "end_date": "", "rank": "县处级", "note": "兼党校校长"},
    {"person_id": 17, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "2025", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 18, "org_id": 7, "title": "市委常委、人武部政委", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "市委常委（职务待确认）", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 20, "org_id": 1, "title": "市委常委（职务待确认）", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 21, "org_id": 1, "title": "市委常委（职务待确认）", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 22, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "2022", "rank": "县处级", "note": "2021 兼白城市委常委"},
    {"person_id": 22, "org_id": 10, "title": "白城市委常委、宣传部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "2024", "rank": "县处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "市政协主席", "start_date": "2021", "end_date": "2025", "rank": "县处级", "note": ""},
    {"person_id": 25, "org_id": 1, "title": "市委副书记", "start_date": "2024-11", "end_date": "2025", "rank": "县处级", "note": "此前曾任宣传部长"},
    {"person_id": 26, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "2024", "end_date": "2025", "rank": "县处级", "note": ""},
    {"person_id": 27, "org_id": 5, "title": "副市长、市公安局局长", "start_date": "2023", "end_date": "2025", "rank": "县处级", "note": ""},
    {"person_id": 28, "org_id": 2, "title": "副市长", "start_date": "2024", "end_date": "2025-09", "rank": "县处级", "note": "2025-09-03 免职"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Relationships
# ─────────────────────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长党政搭档；2024-03 同在市府班子", "overlap_org": "中共洮南市委", "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—常务副市长", "overlap_org": "中共洮南市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委副市长", "overlap_org": "中共洮南市委", "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "书记—人大主任", "overlap_org": "洮南市人民代表大会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 13, "type": "共事", "context": "书记—政协主席", "overlap_org": "政协洮南市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 14, "type": "共事", "context": "书记—市委副书记", "overlap_org": "中共洮南市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 15, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共洮南市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 16, "type": "共事", "context": "书记—组织部长（长年搭档）", "overlap_org": "中共洮南市委", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 17, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共洮南市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 18, "type": "共事", "context": "书记—人武部政委（双拥）", "overlap_org": "洮南市人民武装部", "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 25, "type": "共事", "context": "书记—副书记（原宣传部长）", "overlap_org": "中共洮南市委", "overlap_period": "2024-2025"},
    {"person_a": 1, "person_b": 26, "type": "共事", "context": "书记—政法委书记", "overlap_org": "中共洮南市委", "overlap_period": "2024-2025"},
    {"person_a": 1, "person_b": 22, "type": "交接", "context": "前任书记（薛智金）→现任书记（高熙礼）", "overlap_org": "中共洮南市委", "overlap_period": "2021-2024"},
    {"person_a": 1, "person_b": 23, "type": "共事", "context": "书记—人大主任（2024 两会）", "overlap_org": "洮南市人民代表大会", "overlap_period": "2024"},
    {"person_a": 1, "person_b": 24, "type": "共事", "context": "书记—政协主席（两会）", "overlap_org": "政协洮南市委员会", "overlap_period": "2024-2025"},
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "洮南市人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—常委副市长", "overlap_org": "洮南市人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "洮南市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长（民建）", "overlap_org": "洮南市人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "洮南市人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "洮南市人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长、公安局长", "overlap_org": "洮南市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—挂职副市长", "overlap_org": "洮南市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—挂职副市长（金融）", "overlap_org": "洮南市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—人大主任", "overlap_org": "洮南市人民代表大会", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "常务副—副市长（住建/城管）", "overlap_org": "洮南市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 10, "type": "共事", "context": "常务副—挂职副（能源）", "overlap_org": "洮南市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 11, "type": "共事", "context": "常务副—挂职副（金融）", "overlap_org": "洮南市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 12, "person_b": 15, "type": "交接", "context": "纪委书记 刘明伟 → 贾作辉", "overlap_org": "洮南市纪委监委", "overlap_period": "2024-2025"},
    {"person_a": 23, "person_b": 12, "type": "交接", "context": "人大主任 于洪友 → 刘明伟", "overlap_org": "洮南市人民代表大会常务委员会", "overlap_period": "2024-2025"},
    {"person_a": 24, "person_b": 13, "type": "交接", "context": "政协主席 石文博 → 董伟", "overlap_org": "政协洮南市委员会", "overlap_period": "2025-2026"},
    {"person_a": 27, "person_b": 9, "type": "交接", "context": "公安局长 韩雷 → 吴爱生", "overlap_org": "洮南市公安局", "overlap_period": "2025"},
    {"person_a": 16, "person_b": 15, "type": "共事", "context": "组织部长—纪委书记（巡察领导小组）", "overlap_org": "中共洮南市委", "overlap_period": "2025"},
    {"person_a": 2, "person_b": 12, "type": "同系统", "context": "徐鹏（前纪委书记）与刘明伟（后纪委书记）纪委系统前接", "overlap_org": "洮南市纪委监委", "overlap_period": "2023-2024"},
    {"person_a": 28, "person_b": 2, "type": "共事", "context": "原副市长—市长（免职前）", "overlap_org": "洮南市人民政府", "overlap_period": "2024-2025"},
    {"person_a": 28, "person_b": 3, "type": "共事", "context": "原副市长—常务副（同班子）", "overlap_org": "洮南市人民政府", "overlap_period": "2024-2025"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Person JSON generation (person_graph_json.md schema)
# ═════════════════════════════════════════════════════════════════════════════

def _confidence(person: dict) -> str:
    return person.get("confidence", "unverified")


def _open_questions(person: dict):
    qs = []
    if not person.get("birth"):
        qs.append("出生年月未确认")
    if not person.get("birthplace"):
        qs.append("籍贯未确认")
    if not person.get("education"):
        qs.append("学历教育背景未确认")
    if person["id"] == 1:
        qs.append("任洮南市委书记前的完整履历（2008-2021）未确认；任白城副市长确切时间未确认")
    if person["id"] == 22:
        qs.append("卸任洮南书记确切时间未确认；2022-2023 洮南市委书记（过渡期）身份为公开缺口")
    if person["id"] not in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11) and person.get("birth"):
        qs.append("完整任职履历（起止时间）需进一步核实")
    if person["id"] in (19, 20, 21):
        qs.append("市委常委具体分管职务未确认（2026-08 公开资料未见）")
    return qs


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]

    person_positions = [p for p in positions if p["person_id"] == pid]
    career = []
    for pos in sorted(person_positions, key=lambda x: x.get("start_date", "")):
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": _confidence(person),
            "source_ids": ["S1", "S2"],
        })
    if not career or (len(career) <= 1 and not person.get("birth")):
        career.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口",
            "title": "", "level": "", "rank": "",
            "notes": "公开资料不足（官方简历页缺失或已下线，外部百科不可用）。",
            "confidence": "unverified", "source_ids": [],
        })

    rels_out = []
    for r in relationships:
        if pid not in (r["person_a"], r["person_b"]):
            continue
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        rtype = "overlap" if r["type"] == "共事" else (
            "predecessor_successor" if r["type"] == "交接" else "same_system")
        rels_out.append({
            "person": other["name"] if other else f"person_{other_id}",
            "person_id": f"taonan_{other['name'] if other else ''}",
            "relationship_type": rtype,
            "strength": "strong" if r["type"] in ("共事", "交接") else "weak",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": _confidence(person),
            "source_ids": ["S1", "S2"],
        })

    sources = [
        {"id": "S1", "title": "洮南市人民政府门户网站（领导简介/新闻/大事记）",
         "url": person.get("source") or "http://www.taonan.gov.cn/",
         "publisher": "洮南市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "官方领导简历页 + 新闻/大事记交叉确认"},
        {"id": "S2", "title": "白城市人民政府网站（高熙礼官方简历）",
         "url": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fsz/lhz_23358/",
         "publisher": "白城市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "高熙礼兼白城副市长确认"},
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省", "city": "白城市", "region": "洮南市",
            "job": person.get("current_post", ""), "task_id": "jilin_洮南市",
            "time_focus": "2021-2026",
        },
        "identity": {
            "person_id": f"taonan_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [
                {"period": "", "institution": "", "major": "",
                 "degree": person.get("education", ""),
                 "study_type": "unknown", "source_ids": ["S1"]}
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级" if pid != 1 else "县处级（兼白城副市长副厅级）",
            "as_of": AS_OF,
            "is_current_confirmed": _confidence(person) == "confirmed",
            "source_ids": ["S1", "S2"],
        },
        "career_timeline": career,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if person.get("birthplace") else "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现涉及该人物的公开负面信息（站内检索）",
             "date": AS_OF, "confidence": "plausible", "source_ids": ["S1"]}
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": _confidence(person),
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": (_open_questions(person)[0] if _open_questions(person)
                            else "公开履历细节待补充"),
        },
        "open_questions": [
            {"priority": "critical" if pid in (1, 2) else "high",
             "question": q,
             "why_it_matters": "用于去重、跨区域关联与关系网络分析",
             "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
             "last_attempted": AS_OF}
            for q in _open_questions(person)
        ] or [
            {"priority": "low", "question": f"{name} 更多公开履历细节",
             "why_it_matters": "关系网络分析需要更精确时间线",
             "suggested_queries": [f"{name} 百度百科"],
             "last_attempted": AS_OF},
        ],
    }

    fname = f"{TODAY}-吉林省-白城市-{person['current_post']}-{name}.json"
    with open(PJSON_DIR / fname, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fname}")


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs for core figures...")
    core_ids = {1, 2, 3, 4, 9, 12, 13, 15}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    n_p = len(persons)
    n_o = len(organizations)
    n_pos = len(positions)
    n_r = len(relationships)
    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  stats: persons={n_p} organizations={n_o} positions={n_pos} relationships={n_r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())