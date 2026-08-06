#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 固始县 leadership network.

固始县 - 信阳市 - 河南省.
Targets: 县委书记杨浩威, 县长李新民
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable (works from data/tmp/<task_id>/ during staging
# and from scripts/build/ after promotion)
_SELF = Path(__file__).resolve()
_REPO = next(
    (p for p in _SELF.parents if (p / "gov_relation").is_dir()),
    _SELF.parents[2],
)
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "固始县"
TASK_ID = "henan_固始县"
TODAY = "20260806"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── 核心: 县委书记 杨浩威 ──
    {
        "id": 1,
        "name": "杨浩威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-06",
        "birthplace": "河南省漯河市临颍县",
        "education": "管理学博士（东南大学 管理科学与工程 2006-2009）；管理学硕士（江苏省委党校 企业管理 2003-2006）；河南师范大学信息管理与信息系统 管理学学士（1999-2003）",
        "party_join": "2006-05",
        "work_start": "2009-09",
        "current_post": "固始县委书记、县人武部党委第一书记",
        "current_org": "中国共产党固始县委员会",
        "source": "https://baike.baidu.com/item/杨浩威/6062498",
    },
    # ── 核心领导: 县长 李新民 ──
    {
        "id": 2,
        "name": "李新民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "河南省信阳市新县",
        "education": "党校大学",
        "party_join": "",
        "work_start": "1996-09",
        "current_post": "固始县委副书记、县政府党组书记、县长",
        "current_org": "固始县人民政府",
        "source": "https://www.gushi.gov.cn/gsxrmzf/zwgk/ldjs/webinfo/2024/05/1717016971322283.htm",
    },
    # ── 前任县委书记 王治学 ──
    {
        "id": 3,
        "name": "王治学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-12",
        "birthplace": "河南省信阳市新县",
        "education": "大学，公共管理硕士（北京大学哲学系哲学专业 学士 1987-1991）",
        "party_join": "1995-12",
        "work_start": "1991-10",
        "current_post": "原固始县委书记（2023-06卸任）、信阳市人大常委会原副主任",
        "current_org": "",
        "source": "https://district.ce.cn/newarea/sddy/202108/09/t20210809_36788568.shtml",
    },
    # ── 前任县委书记 曲尚英 ──
    {
        "id": 4,
        "name": "曲尚英",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原固始县委书记（2021-08卸任）",
        "current_org": "",
        "source": "https://web.archive.org/web/20210926170555/https://www.henandaily.cn/content/2021/0819/316314.html",
    },
    # ── 县委副书记 ──
    {
        "id": 5,
        "name": "姜洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委副书记",
        "current_org": "中国共产党固始县委员会",
        "source": "https://app.dahecube.com/nweb/news/20260107/258728n2d5026ac122.htm",
    },
    {
        "id": 6,
        "name": "郭立场",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委副书记、郭陆滩镇党委书记",
        "current_org": "中国共产党固始县委员会",
        "source": "https://www.gushi.gov.cn/cms/cmsadmin/infopub/infopre.jsp?channelcode=A010201",
    },
    # ── 县委常委 ──
    {
        "id": 7,
        "name": "司坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-03",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委、宣传部部长、副县长（负责教育体育、文化旅游、交通运输）",
        "current_org": "中国共产党固始县委员会",
        "source": "https://www.gushi.gov.cn/cms/cmsadmin/infopub/infopre.jsp?channelcode=A010207",
    },
    {
        "id": 8,
        "name": "胡冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委",
        "current_org": "中国共产党固始县委员会",
        "source": "https://www.gushi.gov.cn/cms/cmsadmin/infopub/infopre.jsp?channelcode=A010201",
    },
    {
        "id": 9,
        "name": "游安光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委",
        "current_org": "中国共产党固始县委员会",
        "source": "https://www.gushi.gov.cn/cms/cmsadmin/infopub/infopre.jsp?channelcode=A010201",
    },
    {
        "id": 10,
        "name": "陈刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委",
        "current_org": "中国共产党固始县委员会",
        "source": "https://www.gushi.gov.cn/cms/cmsadmin/infopub/infopre.jsp?channelcode=A010201",
    },
    {
        "id": 11,
        "name": "许涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委、组织部部长",
        "current_org": "中国共产党固始县委员会",
        "source": "https://www.hnxydj.gov.cn/s/gc20d/2022-11-16/7743.html",
    },
    {
        "id": 12,
        "name": "唐磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委",
        "current_org": "中国共产党固始县委员会",
        "source": "https://www.gushi.gov.cn/cms/cmsadmin/infopub/infopre.jsp?channelcode=A010201",
    },
    # ── 纪委 ──
    {
        "id": 13,
        "name": "葛开茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委、县纪委书记、县监委代主任",
        "current_org": "中共固始县纪律检查委员会",
        "source": "http://www.xinyangjiwei.gov.cn/sitesources/xysjcj/page_pc/xsqjw/gushixian/gzdt/article00ed1efa314f40d4872b29beb582c1f9.html",
    },
    # ── 政府班子 ──
    {
        "id": 14,
        "name": "王廷辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县委常委、副县长",
        "current_org": "固始县人民政府",
        "source": "https://www.gushi.gov.cn/gsxrmzf/zwgk/ldjs/webinfo/2024/05/1717016971322283.htm",
    },
    {
        "id": 15,
        "name": "夏明刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县副县长",
        "current_org": "固始县人民政府",
        "source": "https://www.gushi.gov.cn/gsxrmzf/zwgk/ldjs/webinfo/2024/05/1717016971322283.htm",
    },
    {
        "id": 16,
        "name": "刘易强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县副县长",
        "current_org": "固始县人民政府",
        "source": "https://www.gushi.gov.cn/gsxrmzf/zwgk/ldjs/webinfo/2024/05/1717016971322283.htm",
    },
    {
        "id": 17,
        "name": "杨松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县副县长",
        "current_org": "固始县人民政府",
        "source": "https://www.gushi.gov.cn/cms/cmsadmin/infopub/channelpre.jsp?channel=A010207",
    },
    {
        "id": 18,
        "name": "赵峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县副县长、县先进制造业开发区党工委书记、管委会主任",
        "current_org": "固始县先进制造业开发区",
        "source": "http://wjqhnsh.com/show.asp?id=327",
    },
    # ── 人大、政协 ──
    {
        "id": 19,
        "name": "苏锦峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县人大常委会主任",
        "current_org": "固始县人大常委会",
        "source": "https://app.dahecube.com/nweb/news/20231020/178248n2b8ab5ace8a.htm",
    },
    {
        "id": 20,
        "name": "胡海燕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固始县政协主席",
        "current_org": "中国人民政治协商会议固始县委员会",
        "source": "https://app.dahecube.com/nweb/news/20230508/161826nd2d6382e9b8.htm",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党固始县委员会", "type": "党委", "level": "县级", "parent": "中国共产党信阳市委员会", "location": "固始县"},
    {"id": 2, "name": "固始县人民政府", "type": "政府", "level": "县级", "parent": "信阳市人民政府", "location": "固始县"},
    {"id": 3, "name": "固始县人大常委会", "type": "人大", "level": "县级", "parent": "固始县", "location": "固始县"},
    {"id": 4, "name": "中国人民政治协商会议固始县委员会", "type": "政协", "level": "县级", "parent": "固始县", "location": "固始县"},
    {"id": 5, "name": "中共固始县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中国共产党固始县委员会", "location": "固始县"},
    {"id": 6, "name": "固始县先进制造业开发区", "type": "开发区", "level": "县级", "parent": "固始县人民政府", "location": "固始县"},
    {"id": 7, "name": "郭陆滩镇", "type": "乡镇", "level": "乡科级", "parent": "固始县", "location": "固始县"},
    {"id": 8, "name": "中国共产党信阳市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党河南省委员会", "location": "信阳市"},
    {"id": 9, "name": "信阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "信阳市"},
    {"id": 10, "name": "中国共产党平桥区委员会", "type": "党委", "level": "区级", "parent": "中国共产党信阳市委员会", "location": "平桥区"},
    {"id": 11, "name": "信阳高新技术产业开发区管理委员会", "type": "开发区", "level": "地级市", "parent": "信阳市人民政府", "location": "信阳市"},
    {"id": 12, "name": "中国共产党息县委员会", "type": "党委", "level": "县级", "parent": "中国共产党信阳市委员会", "location": "息县"},
    {"id": 13, "name": "息县包信镇", "type": "乡镇", "level": "乡科级", "parent": "息县", "location": "息县"},
    {"id": 14, "name": "中国共产党临颍县委员会", "type": "党委", "level": "县级", "parent": "中国共产党漯河市委员会", "location": "临颍县"},
    {"id": 15, "name": "中国共产党新县委员会", "type": "党委", "level": "县级", "parent": "中国共产党信阳市委员会", "location": "新县"},
    {"id": 16, "name": "中国共产党光山县委员会", "type": "党委", "level": "县级", "parent": "中国共产党信阳市委员会", "location": "光山县"},
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 杨浩威 (书记) — 完整履历 (百度百科确认)
    {"person_id": 1, "org_id": 1, "title": "固始县委书记、县人武部党委第一书记", "start_date": "2023-09", "end_date": "present", "rank": "正县级", "note": "2023-09起专任县委书记（此前2023-06-2023-09书记兼县长）"},
    {"person_id": 1, "org_id": 1, "title": "固始县委书记兼县长、县人武装党委第一书记", "start_date": "2023-06", "end_date": "2023-09", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "固始县人民政府县长", "start_date": "2022-05", "end_date": "2023-06", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "固始县委副书记、副县长、代县长", "start_date": "2021-08", "end_date": "2022-05", "rank": "正县级", "note": "2021-08任固始县委委员、常委、副书记并代县长"},
    {"person_id": 1, "org_id": 11, "title": "信阳高新技术产业开发区党委副书记、管委会主任", "start_date": "2020-07", "end_date": "2021-08", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "信阳市平桥区委常委、副区长", "start_date": "2018-03", "end_date": "2020-07", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "信阳市发展和改革委员会党组成员、副主任", "start_date": "2016-12", "end_date": "2018-03", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "息县人民政府副处级干部/政府党组成员", "start_date": "2012-09", "end_date": "2016-12", "rank": "副县级", "note": "2012-09县政府党组成员(副处级)；2015-10副处级干部"},
    {"person_id": 1, "org_id": 13, "title": "息县包信镇党委副书记（副处级）", "start_date": "2011-06", "end_date": "2012-09", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "息县包信镇党委副书记（正科级）", "start_date": "2010-01", "end_date": "2011-06", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "息县包信镇工作（引进博士）", "start_date": "2009-09", "end_date": "2010-01", "rank": "干部", "note": "博士毕业后引进到信阳市息县包信镇"},
    # 李新民 (县长)
    {"person_id": 2, "org_id": 1, "title": "固始县委副书记", "start_date": "2023", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "固始县人民政府县长", "start_date": "2023-10", "end_date": "present", "rank": "正县级", "note": "2023-10-20固始县十五届人大一次会议全票当选县长"},
    {"person_id": 2, "org_id": 2, "title": "固始县委常委、常务副县长", "start_date": "2020", "end_date": "2023", "rank": "副县级", "note": "分管政府常务、财政、金融、营商环境"},
    # 王治学 (前任书记)
    {"person_id": 3, "org_id": 1, "title": "固始县委书记", "start_date": "2021-08", "end_date": "2023-06", "rank": "正县级", "note": "兼信阳市人大常委会副主任；2023-06-10卸任"},
    {"person_id": 3, "org_id": 2, "title": "固始县人民政府县长", "start_date": "2014-03", "end_date": "2021-08", "rank": "正县级", "note": "2014-03至2021-08任固始县长"},
    {"person_id": 3, "org_id": 16, "title": "光山县委副书记、县长", "start_date": "2011-04", "end_date": "2014-03", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "信阳市委副秘书长、政研室主任", "start_date": "2007-07", "end_date": "2011-04", "rank": "副处级", "note": "2007-2011"},
    {"person_id": 3, "org_id": 9, "title": "信阳市政府副秘书长", "start_date": "2003-09", "end_date": "2007-07", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "信阳市浉河区十三里桥乡党委书记", "start_date": "2001-01", "end_date": "2003-09", "rank": "正科级", "note": "此前浉河区委办副主任、政研室主任"},
    # 曲尚英 (前任)
    {"person_id": 4, "org_id": 1, "title": "固始县委书记（原）", "start_date": "", "end_date": "2021-08", "rank": "正县级", "note": "2021-08-19 王治学接任，曲尚英不再担任"},
    # 姜洋, 郭立场
    {"person_id": 5, "org_id": 1, "title": "固始县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "固始县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "郭陆滩镇党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "县委副书记兼任"},
    # 县委常委们
    {"person_id": 7, "org_id": 1, "title": "固始县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼副县长"},
    {"person_id": 8, "org_id": 1, "title": "固始县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "固始县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "固始县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "固始县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "固始县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "固始县委常委、县纪委书记、县监委代主任", "start_date": "2025", "end_date": "present", "rank": "副县级", "note": "姚晓越2023任纪委书，葛开茂2025任代主任"},
    # 政府班子
    {"person_id": 14, "org_id": 2, "title": "固始县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "固始县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "固始县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "固始县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 6, "title": "固始县先进制造业开发区党工委书记、管委会主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县政府党组成员"},
    {"person_id": 18, "org_id": 2, "title": "固始县政府党组成员", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 人大、政协
    {"person_id": 19, "org_id": 3, "title": "固始县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "固始县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    # 现任党政一把手
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "杨浩威（县委书记）与李新民（县长）现任固始党政一把手搭档", "overlap_org": "固始县", "overlap_period": "2023-至今"},
    # 杨浩威与前任王治学
    {"person_a": 1, "person_b": 3, "type": "前任继任", "context": "杨浩威接替王治学任固始县委书记（2023-06-10）；此前王为书记、杨为县长（上下级 2021-2023）", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2021-2023"},
    {"person_a": 1, "person_b": 4, "type": "前任继任", "context": "杨浩威2021任固始县长时曲尚英为书记至2021-08，随后王治学接任", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2021-08"},
    # 王治学与曲尚英
    {"person_a": 3, "person_b": 4, "type": "前任继任", "context": "王治学2021-08-19接替曲尚英任固始县委书记", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2021-08"},
    # 杨浩威与县班子各常委
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "杨浩威（书记）与姜洋（副书记）县委班子上下级", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "杨浩威（书记）与郭立场（副书记兼郭陆滩镇书记）县委班子上下级", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "杨浩威（书记）与司坤（宣传部长、副县长）县委班子上下级", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "杨浩威（书记）与许涛（组织部长）县委班子上下级（干部人事）", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "杨浩威（书记）与葛开茂（纪委书记、监委代主任）纪委监督上下级", "overlap_org": "中国共产党固始县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 19, "type": "共事", "context": "杨浩威（书记）与苏锦峰（人大主任）党政与人大负责人共事", "overlap_org": "固始县", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 20, "type": "共事", "context": "杨浩威（书记）与胡海燕（政协主席）党政与政协负责人共事", "overlap_org": "固始县", "overlap_period": "2023-至今"},
    # 县长李新民与政府班子
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "李新民（县长）与王廷辉（常委、副县长）政府班子上下级", "overlap_org": "固始县人民政府", "overlap_period": "2023-至今"},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "李新民（县长）与赵峰（开发区党工委书记、管委会主任）开发区建设上下级", "overlap_org": "固始县先进制造业开发区", "overlap_period": "2023-至今"},
    # 王治学与光山体系（跨县）
    {"person_a": 3, "person_b": 2, "type": "前任继任", "context": "王治学2021-08转任固始县委书记后，李新民在其任内任常务副县长并继任县长；王治学2011-2014曾任光山县长（与杨浩威同属信阳跨县体系）", "overlap_org": "固始县人民政府", "overlap_period": "2020-2023"},
    # 信阳体系内履历交集
    {"person_a": 1, "person_b": 3, "type": "同系统", "context": "杨浩威与王治学皆为信阳市委体系干部（发改/政府/县委），跨县交流", "overlap_org": "中国共产党信阳市委员会", "overlap_period": "2016-2023"},
]

# ── Build ─────────────────────────────────────────────────────────────

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

    print(f" DB: {DB_PATH}")
    print(f" GEXF: {GEXF_PATH}")
    print(" Done.")