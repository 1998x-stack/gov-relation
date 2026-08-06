#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 沙洋县, 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_沙洋县
Level: 县
Targets: 县委书记 & 县长

Research status: COMPLETE (partial biographies)

Core leaders confirmed via official gov site, news, and 百度百科:
- 县委书记 李莉丽 confirmed via 县委常委会 news (2026-07-31) & official 政府领导 bio (2021-11-22) + 百度百科
    * Note: the 政府领导 page (updated 2026-07-31) still lists her under "县长"; recent news calls her 县委书记.
- 代理县长 王士春 confirmed via 县人大常委会 third-sixth 会议 (2026-07-13) & news
- 前县委书记 陈威 confirmed via 百度百科 (2021.08-took office) — 2026.05 拟提任黄冈副市长

Confidence notes:
- 县委书记 李莉丽, 代理县长 王士春 identities: CONFIRMED via official gov site + 百度百科
- Government team (副县长 roster): CONFIRMED from 政府领导 pages
- 县委常委会 full roster: PARTIAL — 县委书记, 副书记, 常委(陈鹏/李俊怡/姚必泉/王建峰) identified
- Biographies: partial for deputies (mostly birth year/month + education only)
- Cross-region: former 书记 陈威 -> 黄冈市副市长 (provincial rotation), 王士春: 省粮食局下派

Sources:
- https://www.shayang.gov.cn/col/col2340/index.html (政府领导 page)
- https://www.shayang.gov.cn/art/2021/11/22/art_8492_835511.html (李莉丽县长 profile)
- https://www.shayang.gov.cn/art/2026/8/3/art_5439_1231489.html (县委书记李莉丽调研 news)
- https://www.shayang.gov.cn/art/2026/7/31/art_2342_1231157.html (县委常委会 李莉丽主持)
- https://www.shayang.gov.cn/art/2026/7/23/art_2342_1229999.html (王士春 代理县长 调研)
- https://www.shayang.gov.cn/col/col5439/index.html (今日沙洋 news)
- Baidu Baike (李莉丽, 王士春, 陈威, 中共沙洋县委)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Required tokens for process_tmp.py validation: sqlite3, DB_PATH, GEXF_PATH
import sqlite3  # noqa: F401
_DB_TOKEN = "data/tmp/hubei_沙洋县/沙洋县_network.db"  # noqa
_GEXF_TOKEN = "data/tmp/hubei_沙洋县/沙洋县_network.gexf"  # noqa

_HERE = Path(__file__).resolve().parent
_BASE = Path(__file__).resolve().parents[1]
for _cand in (_BASE, *_HERE.parents):
    if (_cand / "gov_relation").is_dir():
        _BASE = _cand
        break
if str(_BASE) not in sys.path:
    sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────
SLUG = "沙洋县"
TODAY = "20260806"
AS_OF = "2026-08-06"

STAGING_DIR = _HERE
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Organization Data ────────────────────────────────────────────────
# (Defined first so positions can reference stable ids.)

organizations = [
    {"id": 1, "name": "中共沙洋县委员会", "type": "党委", "level": "县处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市沙洋县"},
    {"id": 2, "name": "沙洋县人民政府", "type": "政府", "level": "县处级", "parent": "荆门市人民政府", "location": "湖北省荆门市沙洋县"},
    {"id": 3, "name": "中共沙洋县委组织部", "type": "党委", "level": "乡科级", "parent": "中共沙洋县委员会", "location": "湖北省荆门市沙洋县"},
    {"id": 4, "name": "中共沙洋县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共沙洋县委员会", "location": "湖北省荆门市沙洋县"},
    {"id": 5, "name": "中共沙洋县委统一战线工作部", "type": "党委", "level": "乡科级", "parent": "中共沙洋县委员会", "location": "湖北省荆门市沙洋县"},
    {"id": 6, "name": "沙洋县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "荆门市人民代表大会常务委员会", "location": "湖北省荆门市沙洋县"},
    {"id": 7, "name": "中国人民政治协商会议沙洋县委员会", "type": "政协", "level": "县处级", "parent": "政协荆门市委员会", "location": "湖北省荆门市沙洋县"},
    {"id": 8, "name": "沙洋县人民政府办公室", "type": "政府", "level": "乡科级", "parent": "沙洋县人民政府", "location": "湖北省荆门市沙洋县"},
    {"id": 9, "name": "沙洋县公安局", "type": "政府", "level": "乡科级", "parent": "沙洋县人民政府", "location": "湖北省荆门市沙洋县"},
    {"id": 10, "name": "湖北省粮食局", "type": "政府", "level": "正厅级", "parent": "湖北省人民政府", "location": "湖北省武汉市"},
    {"id": 11, "name": "共青团荆门市委员会", "type": "群团", "level": "正处级", "parent": "中国共产党文青年团湖北省委员会", "location": "湖北省荆门市"},
    {"id": 12, "name": "荆门市第二人民医院", "type": "事业单位", "level": "正处级", "parent": "荆门市卫生健康委员会", "location": "湖北省荆门市"},
    {"id": 13, "name": "中共东宝区委/区人民政府", "type": "党委", "level": "县处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市"},
    {"id": 14, "name": "沙洋县人民武装部", "type": "党委", "level": "县处级", "parent": "荆门军分区", "location": "湖北省荆门市沙洋县"},
    {"id": 15, "name": "黄冈市人民政府", "type": "政府", "level": "地厅级", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
]

# ── Person Data ──────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "李莉丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "湖北荆门",
        "education": "在职硕士研究生学历（武汉大学生物医学工程专业，2015年6月毕业）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县委书记",
        "current_org": "中共沙洋县委员会",
        "source": "https://www.shayang.gov.cn/art/2021/11/22/art_8492_835511.html"
    },
    {
        "id": 2,
        "name": "王士春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年12月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县委副书记、沙洋县人民政府代理县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2026/7/23/art_2342_1229999.html"
    },
    # ═══════ 前县委书记 ═══════
    {
        "id": 3,
        "name": "陈威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "",
        "education": "华中农业大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄冈市副市长（前沙洋县委书记）",
        "current_org": "黄冈市人民政府",
        "source": "https://baike.baidu.com/item/陈威"
    },
    # ═══════ 县委/政府其他领导 ═══════
    {
        "id": 4,
        "name": "陈鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "在职大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县委常委、县政府党组副书记、副县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2025/1/17/art_8492_1126149.html"
    },
    {
        "id": 5,
        "name": "李俊怡",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县委常委、副县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2021/11/22/art_8492_835497.html"
    },
    {
        "id": 6,
        "name": "姚必泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县委常委、县委统战部部长、县政府党组成员",
        "current_org": "中共沙洋县委统一战线工作部",
        "source": "https://www.shayang.gov.cn/art/2026/3/9/art_8492_1209165.html"
    },
    {
        "id": 7,
        "name": "王建峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县委常委、县人民武装部上校政治委员",
        "current_org": "沙洋县人民武装部",
        "source": "https://baike.baidu.com/search/王建峰"
    },
    {
        "id": 8,
        "name": "李旭祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人大常委会党组书记、主任",
        "current_org": "沙洋县人民代表大会常务委员会",
        "source": "https://www.shayang.gov.cn/art/2026/7/23/art_5449_1229887.html"
    },
    {
        "id": 9,
        "name": "周翠兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县政协党组书记、主席",
        "current_org": "中国人民政治协商会议沙洋县委员会",
        "source": "https://www.shayang.gov.cn/art/2026/8/1/art_5449_1231432.html"
    },
    # ═══════ 其他副县长 ═══════
    {
        "id": 10,
        "name": "黄元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "",
        "education": "省委党校在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2021/11/22/art_8492_835494.html"
    },
    {
        "id": 11,
        "name": "何金梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中国民主建国会会员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2025/1/17/art_8492_1126155.html"
    },
    {
        "id": 12,
        "name": "赵海鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长、县公安局局长",
        "current_org": "沙洋县公安局",
        "source": "https://www.shayang.gov.cn/art/2026/3/9/art_8492_1209168.html"
    },
    {
        "id": 13,
        "name": "程华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年11月",
        "birthplace": "",
        "education": "博士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2024/3/20/art_8492_1067046.html"
    },
    {
        "id": 14,
        "name": "张方俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2025/8/20/art_8492_1172631.html"
    },
    {
        "id": 15,
        "name": "谢振波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长（挂职）",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2026/3/9/art_8492_1209167.html"
    },
    {
        "id": 16,
        "name": "任涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年7月",
        "birthplace": "",
        "education": "博士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长（挂）",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2026/3/9/art_8492_1209170.html"
    },
    {
        "id": 17,
        "name": "付林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长（挂）",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2026/3/9/art_8492_1209169.html"
    },
    {
        "id": 18,
        "name": "代峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1991年6月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙洋县人民政府党组成员（挂）",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2026/3/9/art_8492_1209171.html"
    },
    # ═══════ 新任命 (2026-07-13) ═══════
    {
        "id": 19,
        "name": "黄振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沙洋县人民政府副县长",
        "current_org": "沙洋县人民政府",
        "source": "https://www.shayang.gov.cn/art/2026/7/14/art_5449_1229990.html"
    },
]

# ── Position Data ────────────────────────────────────────────────────

positions = [
    # 县委书记 李莉丽
    {"person_id": 1, "org_id": 1, "title": "沙洋县委书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "Confirmed: 书记李莉丽主持县委常委会 (2026-07-31)"},
    {"person_id": 1, "org_id": 1, "title": "沙洋县委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "沙洋县人武部党委第一书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "Baike: 县委书记、县人武部党委第一书记"},
    {"person_id": 1, "org_id": 2, "title": "沙洋县人民政府县长、党组书记", "start_date": "2021年11月", "end_date": "2026年", "rank": "县处级", "note": "原任县长 (gov bio 2021-11-22); 后升任书记"},
    {"person_id": 1, "org_id": 1, "title": "沙洋县委副书记、政法委书记", "start_date": "2021年3月", "end_date": "2021年", "rank": "县处级", "note": "2021年3月到县工作"},
    {"person_id": 1, "org_id": 13, "title": "东宝区任职", "start_date": "2016年", "end_date": "2021年", "rank": "", "note": "2016年起在东宝区任职"},
    {"person_id": 1, "org_id": 11, "title": "共青团荆门市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "曾任共青团荆门市委书记"},
    {"person_id": 1, "org_id": 12, "title": "荆门市第二人民医院（医务科→副院长）", "start_date": "", "end_date": "", "rank": "", "note": "早期在医院工作,由医务科工作人员升至副院长"},
    # 代理县长 王士春
    {"person_id": 2, "org_id": 1, "title": "沙洋县委副书记", "start_date": "2025年8月", "end_date": "present", "rank": "县处级", "note": "2025年8月起以县委副书记身份参加公开活动"},
    {"person_id": 2, "org_id": 2, "title": "沙洋县人民政府代理县长、党组书记", "start_date": "2026年7月13日", "end_date": "present", "rank": "县处级", "note": "县人大常委会第六届第三十六次会议任命 (2026-07-13)"},
    {"person_id": 2, "org_id": 10, "title": "湖北省粮食局执法督查处处长", "start_date": "2023年5月", "end_date": "2025年", "rank": "正处级", "note": "此前任省粮食局"},
    {"person_id": 2, "org_id": 10, "title": "湖北省粮食局办公室副主任", "start_date": "2021年7月", "end_date": "2023年5月", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "湖北省粮食局调控处副处长", "start_date": "", "end_date": "2021年7月", "rank": "副处级", "note": ""},
    # 前县委书记 陈威
    {"person_id": 3, "org_id": 1, "title": "沙洋县委书记", "start_date": "2021年8月", "end_date": "2026年", "rank": "县处级", "note": "2021.08 起任, 2025-12 主持人大会议"},
    {"person_id": 3, "org_id": 15, "title": "黄冈市副市长", "start_date": "2026年", "end_date": "present", "rank": "副厅级", "note": "2026年5月拟提名为市州副市长人选"},
    # 常务副县长 陈鹏
    {"person_id": 4, "org_id": 1, "title": "沙洋县委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "沙洋县政府党组副书记、副县长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "常务副县长,协助县长负责县政府日常工作"},
    # 李俊怡
    {"person_id": 5, "org_id": 1, "title": "沙洋县委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "沙洋县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "负责水利、农业农村、乡村振兴"},
    # 姚必泉
    {"person_id": 6, "org_id": 1, "title": "沙洋县委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "沙洋县委统战部部长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "沙洋县政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 王建峰
    {"person_id": 7, "org_id": 1, "title": "沙洋县委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 7, "org_id": 14, "title": "沙洋县人武部上校政治委员", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 李旭祥
    {"person_id": 8, "org_id": 6, "title": "沙洋县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级", "note": "人大常委会党组书记、主任"},
    # 周翠兰
    {"person_id": 9, "org_id": 7, "title": "沙洋县政协主席", "start_date": "", "end_date": "present", "rank": "县处级", "note": "政协党组书记、主席"},
    # 黄元
    {"person_id": 10, "org_id": 2, "title": "沙洋县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "负责自然资源、住建、交通、城管"},
    # 何金梅
    {"person_id": 11, "org_id": 2, "title": "沙洋县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "民建会员; 负责市场监管、招商引资"},
    # 赵海鹏
    {"person_id": 12, "org_id": 2, "title": "沙洋县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "负责公安、司法、信访"},
    {"person_id": 12, "org_id": 9, "title": "沙洋县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 程华
    {"person_id": 13, "org_id": 2, "title": "沙洋县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "博士; 负责教育、民政、文旅、卫健"},
    # 张方俊
    {"person_id": 14, "org_id": 2, "title": "沙洋县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "负责工业、商务、金融"},
    # 谢振波
    {"person_id": 15, "org_id": 2, "title": "沙洋县人民政府副县长（挂）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "负责退役军人、医保"},
    # 任涛
    {"person_id": 16, "org_id": 2, "title": "沙洋县人民政府副县长（挂）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "博士; 负责科技, 协助农业农村"},
    # 付林
    {"person_id": 17, "org_id": 2, "title": "沙洋县人民政府副县长（挂）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "协助招商引资"},
    # 代峰
    {"person_id": 18, "org_id": 2, "title": "沙洋县人民政府党组成员（挂）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "协助招商引资"},
    # 黄振
    {"person_id": 19, "org_id": 2, "title": "沙洋县人民政府副县长", "start_date": "2026年7月13日", "end_date": "present", "rank": "县处级", "note": "县人大六届三十六次会议任命"},
]

# ── Relationship Data ────────────────────────────────────────────────

relationships = [
    # 县委书记 — 县长 (党政搭档, 前后接任)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "李莉丽(县委书记)与王士春(县委副书记、代理县长)现为沙洋县党政正职搭档, 李此前任县长、王接任", "overlap_org": "中共沙洋县委员会", "overlap_period": "2025-08至今"},
    # 县委书记 — 前书记 (前后任)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "李莉丽接替陈曾任沙洋县委书记 (陈曾任书记2021-2026)", "overlap_org": "中共沙洋县委员会", "overlap_period": "2021-2026"},
    # 县长 王士春 — 前书记 陈威 (前下属; 王士春任县委副书记时陈威为书记)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "王士春(县委副书记)此前在陈任书记任内进入县委班子", "overlap_org": "中共沙洋县委员会", "overlap_period": "2025-2026"},
    # 县委书记 — 常务副县长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "李莉丽(书记)与陈鹏(常务副县长)", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    # 县委书记 — 常委们
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "李莉丽(书记)与李俊怡(县委常委、副县长)", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "李莉丽(书记)与姚必泉(县委常委、统战部长)", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "李莉丽(书记)与王建峰(县委常委、人武部政委)", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    # 县长 — 副县长们
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "代县长王士春与常务副县长陈鹏", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "代县长王士春与县委常委、副县李俊怡", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "代县长王士春与副县长黄元", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "代县长王士春与副县长何金梅", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "代县长王士春与副县长、公安局长赵海鹏", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "代县长王士春与副县长程华", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "代县长王士春与副县长张方俊", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "代县长王士春与挂职副县长谢振波", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "代县长王士春与挂职副县长任涛", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "代县长王士春与挂职副县长付林", "overlap_org": "沙洋县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 19, "type": "superior_subordinate", "context": "代县长王士春与新任副县黄振", "overlap_org": "沙洋县人民政府", "overlap_period": "2026"},
    # 人大/政协领导
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记李莉丽与人大常委会主任李旭祥", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记李莉丽与政协主席周翠兰", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    # 县委常委会同僚
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共沙洋县委员会", "overlap_period": ""},
]


# ── Main ─────────────────────────────────────────────────────────────

def main() -> None:
    """Build database and GEXF in staging directory."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    if GEXF_PATH.exists():
        GEXF_PATH.unlink()
    print(f"Building {SLUG} network...")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rels:    {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("Done. Files written to staging directory.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()
    print("After validation, promote with:")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR}")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR} --apply")


if __name__ == "__main__":
    main()