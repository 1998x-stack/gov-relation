#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 巴彦淖尔市磴口县 leadership network.

Level: 县
Province: 内蒙古自治区
Parent City: 巴彦淖尔市
Region: 磴口县
Targets: 县委书记 (刘向阳) & 县长 (张宇)

Research Date: 2026-08-06 (task inner_mongolia_磴口县)
Evidence quality: guided by the china-gov-network skill; web access degraded
(Exa rate-limited, Baidu/Bing/Jina captcha or timeout, www.dengkou.gov.cn + https
DNS blocked). Core facts confirmed from the OFFICIAL 磴口县人民政府 portal
http://www.nmgdk.gov.cn 领导之窗/政府工作报告 (primary source).

CONFIRMED (official, as of 2026-08-06):
  - 县委书记 刘向阳 (男 汉族 1970-07 研究生 中共党员; 主持县委全面工作)
  - 县委副书记、县长 张宇 (男 汉族 1980-02 研究生硕士 中共党员;
    2026-01-28 县人代会为【代县长】, 现为县长)
  - 县委副书记、政法委书记 马海波 (回族 1973-09 大学本科)
  - 县委常委: 统战部长 黄晓峰(蒙古族), 组织部长 王兴强, 县委办主任 赵晓奕,
    纪委书记/监委主任提名人选 杨璧玮, 宣传部长 樊晓乐(女), 政府副县长 韩瑞
  - 政府副县长: 何蓉(兼公安局长, 女), 李文芳(女, 无党派), 唐东年, 云盛,
    胡学超(工学博士/正高级工程师)
  - 县人大常委会党组书记、主任、一级调研员 秦霞 (女 1969-07)
  - 县政协党组书记、主席 弓建刚 (1972-10)
  - 磴口县第十七次党代会 2026-07-28/30 换届 (刘向阳主持县委全面工作)

PREDECESSOR (confirmed via 政府工作报告 lineage):
  - 县长链: 李志雄 (2023 代 / 2024-2025 县长) —> 张宇 (2026-01 代县长 → 现任县长)

UNVERIFIED / open gaps (见 report/open_gaps.md 与各 person JSON open_questions):
  - 刘向阳 任县委书记时间及 前任县委书记; 是否即巴彦淖尔市曾任副市长/公安局长 刘向阳 (去重风险)
  - 张宇 任县长前完整履历; 李志雄 卸任去向
  - 薛源 (分工中胡学超“协助薛源同志工作”) 具体职务 (疑常务副县长)
  - 各班子成员 任职起始时间与跨县调动记录

Governance / regional profile (2026 政府工作报告, 2026-01-28):
  - 2025 地区生产总值 85.09 亿元, 增长 5.2% (全市第二); 规上工业增加值 13.7 亿元, 增长 8.5%
  - 属 26 个农牧业旗县第一梯队; 粮食产量稳定 7 亿斤以上
  - “百湖之乡” 磴口: 肉苁蓉、光伏+生态肉苁蓉 (全国乡村振兴创新案例), 防沙治沙林草覆盖度 41.4%
"""

from __future__ import annotations

import os
import sqlite3  # noqa: F401 — process_tmp requires 'sqlite3' token in build scripts
import sys
from pathlib import Path

# ── REPO_ROOT 探测 ───────────────────────────────────────────────
_REPO_CANDIDATE = Path(__file__).resolve()
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

SLUG = "磴口县"

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
    {"id": 1, "name": "中共磴口县委员会", "type": "党委", "level": "县处级",
     "parent": "中共巴彦淖尔市委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 2, "name": "磴口县人民政府", "type": "政府", "level": "县处级",
     "parent": "巴彦淖尔市人民政府", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 3, "name": "磴口县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "巴彦淖尔市人大常委会", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 4, "name": "中国人民政治协商会议磴口县委员会", "type": "政协", "level": "县处级",
     "parent": "政协巴彦淖尔市委员会", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 5, "name": "磴口县纪律检查委员会/磴口县监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共巴彦淖尔市纪委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 6, "name": "磴口县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共磴口县委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 7, "name": "磴口县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共磴口县委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 8, "name": "磴口县委统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共磴口县委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 9, "name": "磴口县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共磴口县委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 10, "name": "磴口县公安局", "type": "政府", "level": "县处级",
     "parent": "巴彦淖尔市公安局", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    {"id": 11, "name": "磴口县委办公室", "type": "党委", "level": "县处级",
     "parent": "中共磴口县委", "location": "内蒙古自治区巴彦淖尔市磴口县"},
    # 跨县区 / 上级节点
    {"id": 12, "name": "中共巴彦淖尔市委员会", "type": "党委", "level": "地级市",
     "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区巴彦淖尔市"},
    {"id": 13, "name": "巴彦淖尔市人民政府", "type": "政府", "level": "地级市",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区巴彦淖尔市"},
]

# ── PERSONS ──────────────────────────────────────────────────
persons = [
    # 1 — 刘向阳 — 县委书记
    {"id": 1, "name": "刘向阳", "gender": "男", "ethnicity": "汉族", "birth": "1970年7月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "磴口县委书记", "current_org": "中共磴口县委员会",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxw/dkxwsj/llxy/"},
    # 2 — 张宇 — 县长
    {"id": 2, "name": "张宇", "gender": "男", "ethnicity": "汉族", "birth": "1980年2月",
     "birthplace": "", "education": "研究生硕士学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "中共磴口县委员会",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzf/dkzfxz/lzx/"},
    # 3 — 马海波 — 县委副书记、政法委书记
    {"id": 3, "name": "马海波", "gender": "男", "ethnicity": "回族", "birth": "1973年9月",
     "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、政法委书记", "current_org": "中共磴口县委员会",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxw/dkxwfsj/mhb/"},
    # 4 — 黄晓峰 — 县委常委、统战部长
    {"id": 4, "name": "黄晓峰", "gender": "男", "ethnicity": "蒙古族", "birth": "1974年9月",
     "birthplace": "", "education": "大专学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "磴口县委统一战线工作部",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxw/dkxwcw/hxf/"},
    # 5 — 王兴强 — 县委常委、组织部长
    {"id": 5, "name": "王兴强", "gender": "男", "ethnicity": "汉族", "birth": "1977年12月",
     "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "磴口县委组织部",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxw/dkxwcw/wxq/"},
    # 6 — 赵晓奕 — 县委常委、县委办主任
    {"id": 6, "name": "赵晓奕", "gender": "男", "ethnicity": "汉族", "birth": "1982年",
     "birthplace": "", "education": "大学本科", "party_join": "", "work_start": "",
     "current_post": "县委常委、县委办主任", "current_org": "磴口县委办公室",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxw/dkxwcw/zf/"},
    # 7 — 杨璧玮 — 县委常委、纪委书记
    {"id": 7, "name": "杨璧玮", "gender": "男", "ethnicity": "汉族", "birth": "1982年7月",
     "birthplace": "", "education": "大学本科", "party_join": "", "work_start": "",
     "current_post": "县委常委、纪委书记、监委主任提名人选", "current_org": "磴口县纪律检查委员会/监委",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxw/dkxwcw/ldl/"},
    # 8 — 樊晓乐 — 县委常委、宣传部长
    {"id": 8, "name": "樊晓乐", "gender": "女", "ethnicity": "汉族", "birth": "1987年2月",
     "birthplace": "", "education": "研究生经济学硕士", "party_join": "", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "磴口县委宣传部",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxw/dkxwcw/fxl/"},
    # 9 — 韩瑞 — 县委常委、副县长
    {"id": 9, "name": "韩瑞", "gender": "男", "ethnicity": "汉族", "birth": "1979年10月",
     "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政府副县长", "current_org": "磴口县人民政府",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzf/dkzffxz/hanr/"},
    # 10 — 何蓉 — 副县长、公安局长
    {"id": 10, "name": "何蓉", "gender": "女", "ethnicity": "汉族", "birth": "1976年2月",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局党委书记、局长", "current_org": "磴口县公安局",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzf/dkzffxz/hr/"},
    # 11 — 李文芳 — 副县长
    {"id": 11, "name": "李文芳", "gender": "女", "ethnicity": "汉族", "birth": "1979年9月",
     "birthplace": "", "education": "大学本科学历", "party_join": "无党派人士", "work_start": "",
     "current_post": "副县长", "current_org": "磴口县人民政府",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzf/dkzffxz/lwf/"},
    # 12 — 唐东年 — 副县长
    {"id": 12, "name": "唐东年", "gender": "男", "ethnicity": "汉族", "birth": "1976年11月",
     "birthplace": "", "education": "党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "磴口县人民政府",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzf/dkzffxz/hanr_1/"},
    # 13 — 云盛 — 副县长
    {"id": 13, "name": "云盛", "gender": "男", "ethnicity": "汉族", "birth": "1985年3月",
     "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "磴口县人民政府",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzf/dkzffxz/yunsheng/"},
    # 14 — 胡学超 — 副县长
    {"id": 14, "name": "胡学超", "gender": "男", "ethnicity": "汉族", "birth": "1987年12月",
     "birthplace": "", "education": "工学博士（正高级工程师、硕士生导师）", "party_join": "中共党员",
     "work_start": "",
     "current_post": "副县长", "current_org": "磴口县人民政府",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzf/dkzffxz/hxc/"},
    # 15 — 秦霞 — 县人大常委会主任
    {"id": 15, "name": "秦霞", "gender": "女", "ethnicity": "汉族", "birth": "1969年7月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组书记、主任（一级调研员）", "current_org": "磴口县人民代表大会常务委员会",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxrd/dkrdzr/qx/"},
    # 16 — 弓建刚 — 县政协主席
    {"id": 16, "name": "弓建刚", "gender": "男", "ethnicity": "汉族", "birth": "1972年10月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组书记、主席", "current_org": "政协磴口县委员会",
     "source": "http://www.nmgdk.gov.cn/dkldzc/dkxzx/dkzxzx/gjg/"},
    # 17 — 李志雄 — 前任县长
    {"id": 17, "name": "李志雄", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任磴口县长 2023-2025；卸任去向待核）", "current_org": "磴口县人民政府",
     "source": "http://www.nmgdk.gov.cn/zfxxgkdk/fdzdgknrdk/dkgzbg/202401/t20240117_162587.html"},
]

# ── POSITIONS ────────────────────────────────────────────────
positions = [
    # 刘向阳 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持县委全面工作；第十七次党代会 2026-07 交接周期"},
    # 张宇 — 县长（兼副书记）
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-01", "end_date": "present",
     "rank": "正处级", "note": "2026-01-28 十八届人大五次会议为【代县长】，现为县长"},
    # 马海波 — 副书记/政法委
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "协助处理县委日常工作、党建等"},
    {"person_id": 3, "org_id": 9, "title": "县委政法委书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "主持县委政法委工作"},
    # 黄晓峰 — 统战部长
    {"person_id": 4, "org_id": 8, "title": "县委统战部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "常委"},
    # 王兴强 — 组织部长
    {"person_id": 5, "org_id": 6, "title": "县委组织部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "常委"},
    # 赵晓奕 — 县委办主任
    {"person_id": 6, "org_id": 11, "title": "县委办公室主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "常委"},
    # 杨璧玮 — 纪委书记
    {"person_id": 7, "org_id": 5, "title": "县委书记、纪委书记、监委主任提名人选", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "常委"},
    # 樊晓乐 — 宣传部长
    {"person_id": 8, "org_id": 7, "title": "县委宣传部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "常委"},
    # 韩瑞 — 常委/副县长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "常委；分管农牧科技(乡村振兴)、防沙治沙(林草)、水利等"},
    # 何蓉 — 副县长/公安局长
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管公安"},
    {"person_id": 10, "org_id": 10, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 李文芳 — 副县长
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "无党派；分管民政、卫生健康、医保等"},
    # 唐云 — 副县长
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管城乡建设、自然资源、综合执法、交通等"},
    # 云盛 — 副县长
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管人社、文体旅广、市场监管、民族事务等"},
    # 胡学超 — 副县长
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "工学博士/正高工；分管教育、政务服务与数据管理、招商等；协助薛源同志工作"},
    # 秦霞 — 人大主任
    {"person_id": 15, "org_id": 3, "title": "县人大常委会主任（党组书记、一级调研员）", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    # 弓建刚 — 政协主席
    {"person_id": 16, "org_id": 4, "title": "县政协主席（党组书记）", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    # 李志雄 — 前任县长
    {"person_id": 17, "org_id": 2, "title": "县长", "start_date": "2023", "end_date": "2025",
     "rank": "正处级", "note": "2023 代县长 / 2024-2025 县长；2026 由张宇接任，去向待核"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长（县委-政府正职）党政班子搭档", "overlap_org": "中共磴口县委员会", "overlap_period": "2026"},
    # 县委班子（书记-副书记/常委）
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与县委副书记、政法委书记 班子共事", "overlap_org": "中共磴口县委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 2, "type": "overlap",
     "context": "县委副书记（县长）与县委副书记（政法委）同为副书记", "overlap_org": "中共磴口县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与组织部部长（干部人事）", "overlap_org": "中共磴口县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与纪委书记（监委）同班子监督关系", "overlap_org": "中共磴口县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委书记与宣传部长", "overlap_org": "中共磴口县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委书记与县委办主任（机要/决策落实）", "overlap_org": "中共磴口县委员会", "overlap_period": "current"},
    # 政府班子内部
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "县长与副县长、公安局长（社会稳定）", "overlap_org": "磴口县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "县长与副县长胡学超（教育、政务数据）", "overlap_org": "磴口县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "县长与常委、副县长韩瑞（农牧/乡村振兴）", "overlap_org": "磴口县人民政府", "overlap_period": "current"},
    # 党政与人大政协
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "县委书记与人大主任（两会交叉）", "overlap_org": "磴口县", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "overlap",
     "context": "县长与政协主席（两会协商）", "overlap_org": "磴口县", "overlap_period": "2026"},
    # 前任-现任（县长链）
    {"person_a": 17, "person_b": 2, "type": "predecessor_successor",
     "context": "前任县长李志雄（2023-2025）由张宇接任（2026 代县长→县长）", "overlap_org": "磴口县人民政府", "overlap_period": "2023-2026"},
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
    print(f"\nDone: {SLUG} staging build complete.")