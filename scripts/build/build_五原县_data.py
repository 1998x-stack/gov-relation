#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 巴彦淖尔市五原县 leadership network.

Level: 县
Province: 内蒙古自治区
Parent City: 巴彦淖尔市
Region: 五原县
Targets: 县委书记 (王永佳) & 县长/代县长 (刘岳明)

Research Date: 2026-08-11 (task inner_mongolia_五原县)
Evidence quality: guided by the china-gov-network skill; public search engines
(Exa/Bing/百度/搜狗/360) rate-limited or captcha-blocked from this IP, so all core
facts come from OFFICIAL primary sources:
  - 五原县人民政府门户 http://www.wuyuan.gov.cn (领导之窗-县委/人大/政府/政协,
    政府工作报告 2023-2026, 人事信息/人大常委会任免) — primary source
  - 巴彦淖尔党建网 www.bynrdj.gov.cn 干部任前公示公告 2023-2026 — appointment notices
  - 磴口县调查报告 (20260806, 本仓库) — 张宇(原五原县委副书记→磴口县长) cross-county chain

CONFIRMED (official, as of 2026-08-11):
  - 县委书记 王永佳 (男 汉族 1984-01 研究生 中共党员 一级调研员; 主持县委全面工作)
  - 县委副书记、政府党组书记、代县长 刘岳明 (男 汉族 1988-02 大学 农学学士 中共党员;
    2026-04-21 县人大常委会决定代理县长; 2026-03-24 市委组织部公示拟提旗县区政府正职候选人)
  - 县委副书记、政法委书记 李东 (1979-03, 2025-07 公示自常委、副县长转任)
  - 县委常委: 常务副县长 孟克朝鲁(蒙古族 1982-12), 副县长 宋剑宫(满族 1980-12),
    统战部长 李震(1979-06), 组织部长 戴飞龙(1982-05, 2026-02 补选县代表),
    纪委书记/监委主任 田海芳(女 1986-10, 2026-02 接刘鸿昊), 县委办主任 张翼飞(1977-11),
    人武部上校部长 任彦农(1978-04)
  - 政府副县长: 郭连月(1976-07, 发改/工业/招商), 孙美英(女 1981-01 无党派, 卫建/医卫),
    王智功(1982-08, 2026-01-14 任命, 农牧/乡村振兴), 吴斌(1978-06, 副县长兼公安局长,
    2024-08 公示自市公安局警务保障支队下派), 姜伟(1977-12, 财政局局长, 2026-06 公示拟任副县长)
  - 人大: 主任 詹美(女 1970-12), 副主任 查干朝鲁(蒙古族 1970-02)/刘建斌(1970-08)
  - 政协: 主席 邵永斌(1972-05, 2026-01 公示由副县长转任; 2026-04 辞副县长),
    副主席 王丽培/吕忠平/付志强(原农牧和科技局局长)/侯龙胜(原信访局局长)
  - 前任: 县长 王勇 (2022-06-27 当选; 2025-01-22 十八届人大五次会议作报告;
    2026 年后不在县政府班子, 卸任时间与去向未公开)
  - 前任县委副书记、政法委书记 张宇 (1980-02; 2025-07-17 市委组织部公示拟提旗县区政府正职;
    后调磴口县任县委副书记、县长, 2026-01-28 磴口县两会为代县长 —— 五原→磴州跨县链)
  - 前任监委主任 刘鸿昊 (2026-02-05 县人大代表资格终止/辞监委主任, 调离)
  - 前任宣传部长 郝季芬 (女 1979-09; 2026-05-14 公示拟任旗县区委副书记, 本县宣传部长空缺待公示)

UNVERIFIED / open gaps (report/open_gaps.md 及各 person JSON open_questions):
  - 王永佳 任五原县委书记起始时间、前任书记、任前公示; 任前履历(检索提示与兴安盟关联, 未证实)
  - 刘岳明 2024 年"拟任市直群团正职"后的具体岗位与 2025 年转任五原 任职时间
  - 王勇 卸任时间与去向
  - 县常委/副县 出生信息与履历不完整 (官网仅列基本身份)
  - 现任宣传部长未公开(郝显芬调出后席位待补)

Governance / regional profile (2026-02-07 政府工作报告等官方报告):
  - 2024 地区生产总值 143.41 亿元 (2023 预计 130.4 亿元, +6.5%)
  - "十四五"末: 经济总量累计增长 43.5%, 人均 GDP 4.6 万→7 万元, 固投年均+4.6%,
    财政预算收入年均+4.6%, 市场主体 1.8 万→2.5 万户, 全社会用电 5.1 亿→8.7 亿度
  - 粮食产量稳定 8 亿斤以上; 高标准农田 67.6 万亩; 盐碱地改良 12.7 万亩
    (国家盐碱地综合利用试点县)
  - 自主研发食葵品种国内市占率 40%、南瓜籽 16%; 国家农业现代化示范区;
    全国农业绿色发展先行区创建单位; 工业园区产值突破 130 亿 (2025)
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

SLUG = "五原县"

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
    {"id": 1, "name": "中共五原县委员会", "type": "党委", "level": "县处级",
     "parent": "中共巴彦淖尔市委", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 2, "name": "五原县人民政府", "type": "政府", "level": "县处级",
     "parent": "巴彦淖尔市人民政府", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 3, "name": "五原县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "巴彦淖尔市人大常委会", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 4, "name": "中国人民政治协商会议五原县委员会", "type": "政协", "level": "县处级",
     "parent": "政协巴彦淖尔市委员会", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 5, "name": "中共五原县纪律检查委员会/五原县监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共巴彦淖尔市纪委", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 6, "name": "五原县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共五原县委", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 7, "name": "五原县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共五原县委", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 8, "name": "五原县委统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共五原县委", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 9, "name": "五原县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共五原县委", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 10, "name": "五原县委办公室", "type": "党委", "level": "县处级",
     "parent": "中共五原县委", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 11, "name": "五原县公安局", "type": "政府", "level": "县处级",
     "parent": "五原县人民政府", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 12, "name": "五原县财政局", "type": "政府", "level": "县处级",
     "parent": "五原县人民政府", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 13, "name": "五原县农牧和科技局（乡村振兴局）", "type": "政府", "level": "县处级",
     "parent": "五原县人民政府", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 14, "name": "五原县信访局", "type": "政府", "level": "县处级",
     "parent": "五原县人民政府", "location": "内蒙古自治区巴彦淖尔市五原县"},
    {"id": 15, "name": "五原县人民武装部", "type": "其他", "level": "县处级",
     "parent": "巴彦淖尔军分区", "location": "内蒙古自治区巴彦淖尔市五原县"},
    # 跨县区 / 上级节点
    {"id": 16, "name": "中共巴彦淖尔市委员会", "type": "党委", "level": "地级市",
     "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区巴彦淖尔市"},
    {"id": 17, "name": "巴彦淖尔市人民政府", "type": "政府", "level": "地级市",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区巴彦淖尔市"},
    {"id": 18, "name": "巴彦淖尔市公安局", "type": "政府", "level": "地级市",
     "parent": "巴彦淖尔市人民政府", "location": "内蒙古自治区巴彦淖尔市"},
    {"id": 19, "name": "中共乌拉特前旗委员会", "type": "党委", "level": "县处级",
     "parent": "中共巴彦淖尔市委", "location": "内蒙古自治区巴彦淖尔市乌拉特前旗"},
    {"id": 20, "name": "磴口县人民政府", "type": "政府", "level": "县处级",
     "parent": "巴彦淖尔市人民政府", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 21, "name": "中共磴口县委员会", "type": "党委", "level": "县处级",
     "parent": "中共巴彦淖尔市委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
]

# ── PERSONS ──────────────────────────────────────────────────
persons = [
    # 1 — 王永佳 — 县委书记
    {"id": 1, "name": "王永佳", "gender": "男", "ethnicity": "汉族", "birth": "1984年1月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "五原县委书记（一级调研员）", "current_org": "中共五原县委员会",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 2 — 刘岳明 — 代县长
    {"id": 2, "name": "刘岳明", "gender": "男", "ethnicity": "汉族", "birth": "1988年2月",
     "birthplace": "", "education": "大学本科（农学学士）", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、政府代县长", "current_org": "五原县人民政府",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 3 — 李东 — 县委副书记
    {"id": 3, "name": "李东", "gender": "男", "ethnicity": "汉族", "birth": "1979年3月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、政法委书记", "current_org": "中共五原县委员会",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 4 — 孟克朝鲁 — 常务副县长
    {"id": 4, "name": "孟克朝鲁", "gender": "男", "ethnicity": "蒙古族", "birth": "1982年12月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政府副县长", "current_org": "五原县人民政府",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 5 — 宋剑公 — 常委/副县长
    {"id": 5, "name": "宋剑宫", "gender": "男", "ethnicity": "满族", "birth": "1980年12月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政府副县长", "current_org": "五原县人民政府",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 6 — 李震 — 统战部长
    {"id": 6, "name": "李震", "gender": "男", "ethnicity": "汉族", "birth": "1979年6月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "五原县委统一战线工作部",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 7 — 戴飞龙 — 组织部长
    {"id": 7, "name": "戴飞龙", "gender": "男", "ethnicity": "汉族", "birth": "1982年5月",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "五原县委组织部",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 8 — 田海芳 — 纪委书记
    {"id": 8, "name": "田海芳", "gender": "女", "ethnicity": "汉族", "birth": "1986年10月",
     "birthplace": "", "education": "大学（理学学士、教育学学士）", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共五原县纪律检查委员会/监委",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 9 — 张翼飞 — 县委办主任
    {"id": 9, "name": "张翼飞", "gender": "男", "ethnicity": "汉族", "birth": "1977年11月",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县委办公室主任", "current_org": "五原县委办公室",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 10 — 任彦农 — 人武部
    {"id": 10, "name": "任彦农", "gender": "男", "ethnicity": "汉族", "birth": "1978年4月",
     "birthplace": "", "education": "本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、五原县人民武装部上校部长", "current_org": "五原县人民武装部",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 11 — 郭连月 — 副县长
    {"id": 11, "name": "郭连月", "gender": "男", "ethnicity": "汉族", "birth": "1976年7月",
     "birthplace": "", "education": "本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "政府副县长", "current_org": "五原县人民政府",
     "source": "http://www.wuyuan.gov.cn/zfld/"},
    # 12 — 孙美英 — 副县长
    {"id": 12, "name": "孙美英", "gender": "女", "ethnicity": "汉族", "birth": "1981年1月",
     "birthplace": "", "education": "本科学历", "party_join": "无党派人士", "work_start": "",
     "current_post": "政府副县长", "current_org": "五原县人民政府",
     "source": "http://www.wuyuan.gov.cn/zfld/"},
    # 13 — 王智功 — 副县长
    {"id": 13, "name": "王智功", "gender": "男", "ethnicity": "汉族", "birth": "1982年8月",
     "birthplace": "", "education": "硕士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "政府副县长", "current_org": "五原县人民政府",
     "source": "http://www.wuyuan.gov.cn/zfld/"},
    # 14 — 吴斌 — 副县长、公安局长
    {"id": 14, "name": "吴斌", "gender": "男", "ethnicity": "汉族", "birth": "1978年6月",
     "birthplace": "", "education": "在职研究生（教育学学士）", "party_join": "中共党员", "work_start": "",
     "current_post": "政府副县长、县公安局局长", "current_org": "五原县公安局",
     "source": "http://www.wuyuan.gov.cn/zfld/"},
    # 15 — 姜伟 — 副县长（新）
    {"id": 15, "name": "姜伟", "gender": "男", "ethnicity": "汉族", "birth": "1977年12月",
     "birthplace": "", "education": "大学学历（党校大学）", "party_join": "中共党员", "work_start": "",
     "current_post": "政府副县长、县财政局局长", "current_org": "五原县财政局",
     "source": "http://www.wuyuan.gov.cn/zfld/"},
    # 16 — 詹美 — 人大主任
    {"id": 16, "name": "詹美", "gender": "女", "ethnicity": "汉族", "birth": "1970年12月",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组书记、主任（一级调研员）", "current_org": "五原县人民代表大会常务委员会",
     "source": "http://www.wuyuan.gov.cn/rdld/"},
    # 17 — 查干朝鲁 — 人大副主任
    {"id": 17, "name": "查干朝鲁", "gender": "男", "ethnicity": "蒙古族", "birth": "1970年2月",
     "birthplace": "", "education": "大专学历", "party_join": "无党派人士", "work_start": "",
     "current_post": "县人大常委会副主任（三级调研员）", "current_org": "五原县人民代表大会常务委员会",
     "source": "http://www.wuyuan.gov.cn/rdld/"},
    # 18 — 刘建斌 — 人大副主任
    {"id": 18, "name": "刘建斌", "gender": "男", "ethnicity": "汉族", "birth": "1970年8月",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组副书记、副主任", "current_org": "五原县人民代表大会常务委员会",
     "source": "http://www.wuyuan.gov.cn/rdld/"},
    # 19 — 邵永斌 — 政协主席
    {"id": 19, "name": "邵永斌", "gender": "男", "ethnicity": "汉族", "birth": "1972年5月",
     "birthplace": "", "education": "研究生学历（党校研究生）", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组书记、主席", "current_org": "政协五原县委员会",
     "source": "http://www.wuyuan.gov.cn/zxld/"},
    # 20 — 王丽培 — 政协副主席
    {"id": 20, "name": "王丽霞", "gender": "女", "ethnicity": "汉族", "birth": "1972年9月",
     "birthplace": "", "education": "大学学历", "party_join": "无党派人士", "work_start": "",
     "current_post": "县政协副主席", "current_org": "政协五原县委员会",
     "source": "http://www.wuyuan.gov.cn/zxld/"},
    # 21 — 吕忠平 — 政协副主席
    {"id": 21, "name": "吕忠平", "gender": "男", "ethnicity": "汉族", "birth": "1970年5月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组副书记、副主席", "current_org": "政协五原县委员会",
     "source": "http://www.wuyuan.gov.cn/zxld/"},
    # 22 — 付志强 — 政协副主席
    {"id": 22, "name": "付志强", "gender": "男", "ethnicity": "汉族", "birth": "1970年8月",
     "birthplace": "", "education": "研究生学历（党校研究生）", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组成员、副主席（四级调研员）", "current_org": "政协五原县委员会",
     "source": "http://www.wuyuan.gov.cn/zxld/"},
    # 23 — 侯龙胜 — 政协副主席
    {"id": 23, "name": "侯龙胜", "gender": "男", "ethnicity": "汉族", "birth": "1976年3月",
     "birthplace": "", "education": "大专学历", "party_join": "无党派人士", "work_start": "",
     "current_post": "县政协副主席", "current_org": "政协五原县委员会",
     "source": "http://www.wuyuan.gov.cn/zxld/"},
    # 24 — 王勇 — 前任县长
    {"id": 24, "name": "王勇", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任五原县长 2022-2025；卸任去向待核）", "current_org": "五原县人民政府",
     "source": "http://www.wuyuan.gov.cn/zfgzbg/52854.html"},
    # 25 — 吕华东 — 前任副书记
    {"id": 25, "name": "吕华东", "gender": "男", "ethnicity": "汉族", "birth": "1977年12月",
     "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任五原县委副书记、政法委书记；2023-12 公示调任市委部门）", "current_org": "中共五原县委员会",
     "source": "http://www.wuyuan.gov.cn/xwld/"},
    # 26 — 张宇 — 前任副书记/现磴口县长
    {"id": 26, "name": "张宇", "gender": "男", "ethnicity": "汉族", "birth": "1980年2月",
     "birthplace": "", "education": "在职大学（公共管理硕士）", "party_join": "中共党员", "work_start": "",
     "current_post": "（原五原县委副书记、政法委书记；现磴口县委副书记、县长）", "current_org": "磴口县人民政府",
     "source": "https://www.bynrdj.gov.cn/cms/info/preview.jsp?SiteID=djw&ColumnID=25&KeyID=20250718085645999809252"},
    # 27 — 刘鸿昊 — 前任监委主任
    {"id": 27, "name": "刘鸿昊", "gender": "男", "ethnicity": "汉族", "birth": "1985年11月",
     "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任五原县监察委员会主任；2026-02 调离）", "current_org": "中共五原县纪律检查委员会/监委",
     "source": "http://www.wuyuan.gov.cn/rsxx/52557.html"},
    # 28 — 郝耀芬 — 前任宣传部长
    {"id": 28, "name": "郝耀芬", "gender": "女", "ethnicity": "汉族", "birth": "1979年9月",
     "birthplace": "", "education": "大学（农学学士）", "party_join": "中共党员", "work_start": "",
     "current_post": "（原五原县委常委、宣传部部长；2026-05 公示拟任旗县区委副书记）", "current_org": "五原县委宣传部",
     "source": "https://www.bynrdj.gov.cn/cms/info/preview.jsp?SiteID=djw&ColumnID=25&KeyID=20260515090015845180883"},
]

# ── POSITIONS ────────────────────────────────────────────────
positions = [
    # 王永佳 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记（一级调研员）", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持县委全面工作；2026-08 官网领导之窗在任"},
    # 刘岳明 — 代县长
    {"person_id": 2, "org_id": 2, "title": "县长（代理）", "start_date": "2026-04", "end_date": "present",
     "rank": "正处级", "note": "2026-04-21 县十八届人大常委会 31 次会议决定代理县长"},
    {"person_id": 2, "org_id": 2, "title": "政府党组成员、副县长", "start_date": "", "end_date": "2026-04",
     "rank": "副处级", "note": "2026-02-07 县十八届人大七次会议作 《2026 政府工作报告》时任常委、副县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "官领导之窗现任县委副书记"},
    {"person_id": 2, "org_id": 19, "title": "旗委常委、旗委办公室主任", "start_date": "", "end_date": "2024",
     "rank": "副处级", "note": "2023-12-21 任前公示（拟任市直群团部门正职）；2024 年调市直群团部门（具体岗位待核）"},
    # 李东 — 副书记/政法委
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "2025-08", "end_date": "present",
     "rank": "副处级", "note": "2025-07-17 任前公示拟任旗县区党委副书记"},
    {"person_id": 3, "org_id": 9, "title": "县委政法委书记", "start_date": "2025-08", "end_date": "present",
     "rank": "副处级", "note": "接张宇岗位；负责维稳综治、信访"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、政府副县长", "start_date": "", "end_date": "2025-08",
     "rank": "副处级", "note": "2023-06 曾公示“拟进一步使用”"},
    {"person_id": 3, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "2023",
     "rank": "副处级", "note": ""},
    # 孟克朝鲁 — 常务副县长
    {"person_id": 4, "org_id": 2, "title": "县委常委、政府副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "承担县政府日常事务工作；分管财政/应急/城建/审计"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 宋剑宫
    {"person_id": 5, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管人社、民政、文体旅广、民委"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 李震
    {"person_id": 6, "org_id": 8, "title": "县委统战部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管工商联、宗教"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 戴飞龙
    {"person_id": 7, "org_id": 6, "title": "县委组织部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2026-02 补选为县人大代表（新任干部）"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 田海芳
    {"person_id": 8, "org_id": 5, "title": "县纪委书记、监委主任", "start_date": "2026-02", "end_date": "present",
     "rank": "副处级", "note": "2016-01 任前公示（市纪委监委派驻纪检组组长）；2026-02-06 刘鸿昊辞监委主任同批",
},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "2026-02", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 张翼飞
    {"person_id": 9, "org_id": 10, "title": "县委办公室主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "常委"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 任彦农
    {"person_id": 10, "org_id": 15, "title": "县人民武装部上校部长", "start_date": "", "end_date": "present",
     "rank": "正团级", "note": "常委"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副团级", "note": "任彦农为军事系统派驻"},
    # 郭连月
    {"person_id": 11, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管发改/工业/园区/自然资源/招商引资"},
    # 孙美英
    {"person_id": 12, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管卫健、医保、市场监管；无党派"},
    # 王智功
    {"person_id": 13, "org_id": 2, "title": "政府副县长", "start_date": "2026-01", "end_date": "present",
     "rank": "副处级", "note": "2026-01-14 县人大常委会第 28 次会议任命；分管农牧科技、乡村振兴"},
    # 吴斌
    {"person_id": 14, "org_id": 11, "title": "县公安局局长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2024 年起（2024-08-23 任前公示自市公安局警务保障支队）"},
    {"person_id": 14, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管公安、司法、信访"},
    {"person_id": 14, "org_id": 18, "title": "市公安局警务保障支队支队长", "start_date": "", "end_date": "2024",
     "rank": "副处级", "note": "2024-08-23 公示：现任市公安局警务保障支队支队长、四级高级警长，拟提名任旗县区政府副职"},
    # 姜伟
    {"person_id": 15, "org_id": 12, "title": "县财政局局长、国资委主任", "start_date": "", "end_date": "2026-07",
     "rank": "正科级", "note": "2026-06-22 公示：现任财政局长拟提名任旗县区政府副职"},
    {"person_id": 15, "org_id": 2, "title": "政府副县长", "start_date": "2026-07", "end_date": "present",
     "rank": "副处级", "note": "分管交通、教育（职级保留四级调研员）"},
    # 詹美
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任（党组书记）", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "一级调研员"},
    # 查干朝鲁
    {"person_id": 17, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "无党派；三级调研员"},
    # 刘建斌
    {"person_id": 18, "org_id": 3, "title": "县人大常委会党组副书记、副主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 邵永斌
    {"person_id": 19, "org_id": 4, "title": "县政协主席（党组书记）", "start_date": "2026-01", "end_date": "present",
     "rank": "正处级", "note": "2026-01-16 公示拟旗县区政协主席候选人"},
    {"person_id": 19, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "2026-04",
     "rank": "副处级", "note": "2026-04-21 接受辞去副县长职务"},
    # 王丽霞
    {"person_id": 20, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "无党派"},
    # 吕忠平
    {"person_id": 21, "org_id": 4, "title": "县政协党组副书记、副主席", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 付志强
    {"person_id": 22, "org_id": 4, "title": "县政协党组成员、副主席", "start_date": "2026-01", "end_date": "present",
     "rank": "副处级", "note": "2026-01-16 公示；四级调研员"},
    {"person_id": 22, "org_id": 13, "title": "五原县农牧和科技局党组书记、局长（乡村振兴局局长）", "start_date": "", "end_date": "2026-01",
     "rank": "正科级", "note": ""},
    # 侯龙胜
    {"person_id": 23, "org_id": 4, "title": "县政协副主席", "start_date": "2026-01", "end_date": "present",
     "rank": "副处级", "note": "2026-01-16 公示；无党派人士"},
    {"person_id": 23, "org_id": 14, "title": "县信访局局长", "start_date": "", "end_date": "2026-01",
     "rank": "正科级", "note": "2026-01-16 公示时职务"},
    # 王勇 — 前任县长
    {"person_id": 24, "org_id": 2, "title": "县长", "start_date": "2022-06", "end_date": "2025",
     "rank": "正处级", "note": "2022-06-27 当选；2024-01-13/2025-01-22 两会在任并作报告；2025 下半年起卸任去向待核"},
    # 吕华东 — 前任副书记
    {"person_id": 25, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "2023-12",
     "rank": "副处级", "note": "2023-12-21 公示拟任市委工作部门常务副职"},
    {"person_id": 25, "org_id": 9, "title": "县委政法委书记", "start_date": "", "end_date": "2023-12",
     "rank": "副处级", "note": "三级调研员"},
    # 张宇 — 前任副书记 → 磴口县长
    {"person_id": 26, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "2025-09",
     "rank": "副处级", "note": "一级调研员；2025-07-17 公示拟提旗县区政府正职候选人"},
    {"person_id": 26, "org_id": 9, "title": "县委政法委书记", "start_date": "", "end_date": "2025-09",
     "rank": "副处级", "note": "2023 年起任；五原→磴口跨县交流链"},
    {"person_id": 26, "org_id": 21, "title": "磴口县委副书记", "start_date": "2025-10", "end_date": "present",
     "rank": "副处级", "note": "2026-01-28 磴口县两会为代县"},
    {"person_id": 26, "org_id": 20, "title": "磴口县县长（代理）", "start_date": "2026-01", "end_date": "present",
     "rank": "正处级", "note": "磴口县人民政府工作报告 (2026-01-28)"},
    # 刘鸿昊 — 前任监委主任
    {"person_id": 27, "org_id": 5, "title": "县监察委员会主任", "start_date": "2024", "end_date": "2026-02",
     "rank": "副处级", "note": "2023-12-21 公示拟任旗县区党委副职；2026-02-05 辞去监委会主任，代表资格终止"},
    # 郝耀芬 — 前任宣传部长
    {"person_id": 28, "org_id": 7, "title": "县委宣传部部长", "start_date": "", "end_date": "2026-05",
     "rank": "副处级", "note": "三级调研员；2026-05-14 公示拟任旗县区党委副书记"},
    {"person_id": 28, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "2026-05",
     "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ────────────────────────────────────────────
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与代县长（县委-政府正职）党政班子搭档", "overlap_org": "中共五原县委员会", "overlap_period": "2026"},
    # 县委班子（书记-副书记/常委）
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与县委副书记、政法委书记 班子共事", "overlap_org": "中共五原县委员会", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 2, "type": "overlap",
     "context": "县委副书记（县长）与县委副书记（政法委）同为副书记", "overlap_org": "中共五原县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与组织部部长（干部人事）", "overlap_org": "中共五原县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委书记与纪委书记（监委）同班子监督关系", "overlap_org": "中共五原县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委书记与县委办主任（机要/决策落实）", "overlap_org": "中共五原县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委书记与统战部长", "overlap_org": "中共五原县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 28, "type": "overlap",
     "context": "县委书记与宣传部长共事（郝耀芬 2026-05 调离）", "overlap_org": "中共五原县委员会", "overlap_period": "2025-2026"},
    # 政府班子
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "代县长与常务副县长（县政府日常事务）", "overlap_org": "五原县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "代县长与常委副县长 宋剑宫", "overlap_org": "五原县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "代县长与副县长、公安局长（社会稳定）", "overlap_org": "五原县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "代县长与副县长姜伟（财政/交通/教育）", "overlap_org": "五原县人民政府", "overlap_period": "2026-07"},
    {"person_a": 14, "person_b": 2, "type": "overlap",
     "context": "公安局长与县长（公安工作分管关系）", "overlap_org": "五原县人民政府", "overlap_period": "2025-2026"},
    # 党政与人大政协
    {"person_a": 1, "person_b": 16, "type": "overlap",
     "context": "县委书记与人大常委会主任（两会交叉）", "overlap_org": "五原县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "context": "县委书记与政协主席（两会协商）", "overlap_org": "五原县", "overlap_period": "2026"},
    {"person_a": 19, "person_b": 22, "type": "overlap",
     "context": "政协主席与政协副主席（原农牧局长）", "overlap_org": "政协五原县委员会", "overlap_period": "2026"},
    # 前任-接任链
    {"person_a": 24, "person_b": 2, "type": "predecessor_successor",
     "context": "前任县长王勇（2022-2025）由刘岳明代理接任（2026-04）", "overlap_org": "五原县人民政府", "overlap_period": "2022-2026"},
    {"person_a": 24, "person_b": 1, "type": "overlap",
     "context": "县长与县委书记（王永佳任书记 2023-2025 期间党政搭档；王永佳任书记起始时间待核）", "overlap_org": "五原县", "overlap_period": "2022-2025"},
    {"person_a": 3, "person_b": 26, "type": "predecessor_successor",
     "context": "政法委书记岗位继任：张宇（至 2025-09）→ 李东（2025-08 起）", "overlap_org": "五原县委政法委员会", "overlap_period": "2025"},
    {"person_a": 8, "person_b": 27, "type": "predecessor_successor",
     "context": "监委主任岗位继任：刘鸿昊（至 2026-02）→ 田海芳（2026-02 起）", "overlap_org": "五原县监察委员会", "overlap_period": "2026-02"},
    # 跨县流动
    {"person_a": 26, "person_b": 24, "type": "promotion_chain",
     "context": "张宇由五原县委副书记调磴口县任副书记、代县长/县长（2025-2026），形成五原→磴口县长链", "overlap_org": "巴彦淖尔市", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 26, "type": "other",
     "context": "刘岳明（前任旗）（2026-04 升任五原代县长）与张宇（2026-01 磴口代县长）同期县域交流（不同县）", "overlap_org": "巴彦淖尔市", "overlap_period": "2026"},
    {"person_a": 14, "person_b": 25, "type": "other",
     "context": "吴斌（2024 市公安局警务保障支队下派任副县长/公安局长）属市→县下派", "overlap_org": "巴彦淖尔市公安局", "overlap_period": "2024"},
    # 政协内部流动（来源），付志强/侯龙胜 由局长转任副主席
    {"person_a": 22, "person_b": 2, "type": "other",
     "context": "付志强 2026 年由农牧和科技局长转县政协副主席（副处）", "overlap_org": "五原县", "overlap_period": "2026"},
    {"person_a": 23, "person_b": 2, "type": "other",
     "context": "侯龙胜 2026 年由信访局长转县政协副主席（无党派干部使用）", "overlap_org": "五原县", "overlap_period": "2026"},
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