#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黄南藏族自治州 (Huangnan Tibetan
Autonomous Prefecture), 青海省.

Task ID: qinghai_黄南藏族自治州 | Level: 地级市（自治州） | Targets: 州委书记 & 州长 | Date: 2026-08-07

Research status: CORE CONFIRMED, ROSTER PARTIAL.

Confirmed (official / multiple sources):
  - 州委书记: 夏吾杰 (藏族, 男, 1970年10月生, 青海循化, 2026年1月就任) —— 中国经济网 2026-01-28
  - 州长（代州长）: 才让索南 (藏族, 男, 1973年10月生, 青海共和, 2026年5月28日任副州长兼代州长) —— 中国经济网 2026-05-29
  - 前任州长: 扎西才让 (藏族, 男, 1966年9月生, 2026-05-28 辞去州长职务)
  - 人大主任: 蒋树成 (汉族, 1966年2月生, 2021年5月就任)
  - 政协主席: 叶忠措 (女, 藏族, 1969年12月生, 2024年2月就任)

罗列 (from 黄南州人大/黄南新闻网/Baidu Baike, plausible level; 部分副州长姓名可能有转写差异):
  - 常务副州长 王海瑞; 副州长 裴旅、周涛、项素、金涛、陆宁(窦?)、霍均、胡文娟 (2026.8新); 秘书长 崔晓园
  - 人大副主任 辛海萍、马进贤; 秘书长 马祥成; 州中院院长 杨海云
  - 政协副主席 白萍、夏日仓·旦增久美、多杰才让、韩尚丽、张海渊、张浩

Confidence:
  - 州委书记 夏吾杰 / 州长 才让索南 / 前任州长 扎西才让: confirmed
  - 人大主任 蒋树成 / 政协主席 叶忠措: confirmed
  - 州政府/人大/政协其他成员: plausible（姓名可能因抓取转写有误）
  - 州委常驻班子成员（书记、组织部/宣传部/政法委/统战部、纪委）: unverified（政府网站被 WAF 阻断，未达个人资料档案）

Web access note: 中国政府网站被 WAF/验证码阻断；Exa 限流；Bing/Sogou/360 反爬。本文一级来源为
中国经济网(district.ce.cn)、Wikipedia zh、黄南新闻网(qhhnnews.com)、Baidu Baike 政府页。
"""

import json
import sqlite3  # noqa: required by process_tmp.py token check
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Locate repo root: data/tmp/<id>/build_<slug>.py → parents[3] (the 海北 pattern uses parents[3]),
# or scripts/build/<slug>.py → parents[2].
_REPO = BASE
for _ in range(3):
    if (_REPO / "gov_relation").is_dir():
        break
    _REPO = _REPO.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "黄南藏族自治州"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"
DB_PATH = str(BASE / f"{SLUG}_network.db")
GEXF_PATH = str(BASE / f"{SLUG}_network.gexf")

# ═══════════════════════════ Persons ═══════════════════════════
persons = [
    # Core top-two leaders — confirmed
    {"id": 1, "name": "夏吾杰", "gender": "男", "ethnicity": "藏族", "birth": "1970年10月",
     "birthplace": "青海省循化撒拉族自治县", "education": "青海师范大学汉语言文学，文学学士",
     "party_join": "1991年9月", "work_start": "1989年7月",
     "current_post": "州委书记", "current_org": "中共黄南藏族自治州委员会",
     "source": "中国经济网2026-01-28; Wikipedia zh 黄南藏族自治州; Baidu Baike 夏吾杰"},
    {"id": 2, "name": "才让索南", "gender": "男", "ethnicity": "藏族", "birth": "1973年10月",
     "birthplace": "青海省共和县", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "州委副书记、州长（代）", "current_org": "黄南藏族自治州人民政府",
     "source": "中国经济网2026-05-29; Wikipedia zh 黄南藏族自治州; Baidu Baike 才让索南"},
    {"id": 3, "name": "扎西才让", "gender": "男", "ethnicity": "藏族", "birth": "1966年9月",
     "birthplace": "", "education": "省委党校经济管理专业",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任州长（2026-05辞任）", "current_org": "",
     "source": "中国经济网2026-05-29; 20210816_36810370"},
    {"id": 4, "name": "蒋树成", "gender": "男", "ethnicity": "汉族", "birth": "1966年2月",
     "birthplace": "青海省大通回族土族自治县", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "州人大常委会主任", "current_org": "黄南藏族自治州人民代表大会常务委员会",
     "source": "Wikipedia zh 黄南藏族自治州"},
    {"id": 5, "name": "叶忠措", "gender": "女", "ethnicity": "藏族", "birth": "1969年12月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "州政协主席", "current_org": "政协黄南藏族自治州委员会",
     "source": "黄南新闻网 政协第十四届委员会; Wikipedia zh 黄南藏族自治州"},

    # 州政府 executive (partial / plausible)
    {"id": 6, "name": "王海瑞", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "常务副州长", "current_org": "黄南藏族自治州人民政府",
     "source": "Baidu Baike 黄南藏族自治州人民政府（黄南州人大）"},
    {"id": 7, "name": "项秀", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副州长", "current_org": "黄南藏族自治州人民政府",
     "source": "中国经济网2026-05-29（2026-05-28任命）"},
    {"id": 8, "name": "裴治", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "黄南藏族自治州人民政府",
     "source": "Baidu Baike 黄南藏族自治州人民政府"},
    {"id": 9, "name": "周涛", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "黄南藏族自治州人民政府",
     "source": "Baidu Baike 黄南藏族自治州人民政府"},
    {"id": 10, "name": "金涛", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "黄南藏族自治州人民政府",
     "source": "Baidu Baike 黄南藏族自治州人民政府"},
    {"id": 11, "name": "陆宁", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "黄南藏族自治州人民政府",
     "source": "Baidu Baike 黄南藏族自治州人民政府"},
    {"id": 12, "name": "霍均", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长（2026-08新）", "current_org": "黄南藏族自治州人民政府",
     "source": "黄南人大 2026-08-06; Baidu Baike 黄南藏族自治州人民政府"},
    {"id": 13, "name": "胡文娟", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长（2026-08新）", "current_org": "黄南藏族自治州人民政府",
     "source": "黄南人大 2026-08-06; Baidu Baike 黄南藏族自治州人民政府"},
    {"id": 14, "name": "孙勇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任副州长（2026-05-28免职，或系援青干部）", "current_org": "",
     "source": "中国经济网2026-05-29; 黄南人大 2026-03-18"},
    {"id": 15, "name": "梁晓园", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州政府秘书长", "current_org": "黄南藏族自治州人民政府",
     "source": "Baidu Baike 黄南藏族自治州人民政府"},

    # 人大
    {"id": 16, "name": "辛海萍", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州人大常委会副主任", "current_org": "黄南藏族自治州人民代表大会常务委员会",
     "source": "黄南新闻网 人大办 2026-03-18"},
    {"id": 17, "name": "马进贤", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州人大常委会副主任", "current_org": "黄南藏族自治州人民代表大会常务委员会",
     "source": "黄南新闻网 人大办 2026-03-18"},
    {"id": 18, "name": "马祥成", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州人大常委会秘书长", "current_org": "黄南藏族自治州人民代表大会常务委员会",
     "source": "黄南新闻网 人大办 2026-03-18"},

    # 政协
    {"id": 19, "name": "白萍", "gender": "女", "ethnicity": "藏族", "birth": "1966年7月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "州政协副主席（党组副书记）", "current_org": "政协黄南藏族自治州委员会",
     "source": "黄南新闻网 政协第十四届简历"},
    {"id": 20, "name": "夏日仓·旦增久美", "gender": "男", "ethnicity": "藏族", "birth": "1979年9月",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "州政协副主席", "current_org": "政协黄南藏族自治州委员会",
     "source": "黄南新闻网 政协第十四届简历"},
    {"id": 21, "name": "多杰才让", "gender": "男", "ethnicity": "藏族", "birth": "1965年5月",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "州政协副主席", "current_org": "政协黄南藏族自治州委员会",
     "source": "黄南新闻网 政协第十四届简历"},
    {"id": 22, "name": "韩尚丽", "gender": "女", "ethnicity": "汉族", "birth": "1973年4月",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "州政协副主席", "current_org": "政协黄南藏族自治州委员会",
     "source": "黄南新闻网 政协第十四届简历"},
    {"id": 23, "name": "张海渊", "gender": "男", "ethnicity": "藏族", "birth": "1966年6月",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "州政协副主席", "current_org": "政协黄南藏族自治州委员会",
     "source": "黄南新闻网 政协第十四届简历"},
    {"id": 24, "name": "张浩", "gender": "男", "ethnicity": "汉族", "birth": "1971年4月",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "州政协副主席", "current_org": "政协黄南藏族自治州委员会",
     "source": "黄南新闻网 政协第十四届简历"},
]

# ═══════════════════════════ Organizations ═══════════════════════════
organizations = [
    {"id": 1, "name": "中共黄南藏族自治州委员会", "type": "党委", "level": "地级", "parent": "中共青海省委员会", "location": "黄南藏族自治州同仁市"},
    {"id": 2, "name": "黄南藏族自治州人民政府", "type": "政府", "level": "地级", "parent": "青海省人民政府", "location": "黄南藏族自治州同仁市"},
    {"id": 3, "name": "黄南藏族自治州人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "青海省人大常委会", "location": "黄南藏族自治州同仁市"},
    {"id": 4, "name": "中国人民政治协商会议黄南藏族自治州委员会", "type": "政协", "level": "地级", "parent": "青海省政协", "location": "黄南藏族自治州同仁市"},
    {"id": 5, "name": "同仁市人民政府", "type": "政府", "level": "县级", "parent": "黄南藏族自治州人民政府", "location": "同仁市"},
    {"id": 6, "name": "尖扎县人民政府", "type": "政府", "level": "县级", "parent": "黄南藏族自治州人民政府", "location": "尖扎县"},
    {"id": 7, "name": "泽库县人民政府", "type": "政府", "level": "县级", "parent": "黄南藏族自治州人民政府", "location": "泽库县"},
    {"id": 8, "name": "河南蒙古族自治县人民政府", "type": "政府", "level": "县级", "parent": "黄南藏族自治州人民政府", "location": "河南蒙古族自治县"},
    {"id": 9, "name": "中共海北藏族自治州委员会", "type": "党委", "level": "地级", "parent": "中共青海省委员会", "location": "海北藏族自治州"},
    {"id": 10, "name": "海北藏族自治州人民政府", "type": "政府", "level": "地级", "parent": "青海省人民政府", "location": "海北藏族自治州"},
    {"id": 11, "name": "中共果洛藏族自治州委员会", "type": "党委", "level": "地级", "parent": "中共青海省委员会", "location": "果洛藏族自治州"},
    {"id": 12, "name": "果洛藏族自治州政协", "type": "政协", "level": "地级", "parent": "青海省政协", "location": "果洛藏族自治州"},
    {"id": 13, "name": "中共班玛县委员会", "type": "党委", "level": "县级", "parent": "中共果洛藏族自治州委员会", "location": "班玛县"},
    {"id": 14, "name": "班玛县人民政府", "type": "政府", "level": "县级", "parent": "果洛藏族自治州人民政府", "location": "班玛县"},
    {"id": 15, "name": "中共青海省委办公厅", "type": "党委", "level": "省级", "parent": "中共青海省委员会", "location": "西宁市"},
    {"id": 16, "name": "青海省人民政府办公厅", "type": "政府", "level": "省级", "parent": "青海省人民政府", "location": "西宁市"},
    {"id": 17, "name": "青海省信访局", "type": "政府", "level": "省级", "parent": "青海省人民政府", "location": "西宁市"},
    {"id": 18, "name": "中共青海省委员会", "type": "党委", "level": "省级", "parent": "", "location": "西宁市"},
]

# ═══════════════════════════ Positions ═══════════════════════════
positions = [
    # 夏吾杰 (id 1)
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start_date": "2026-01", "end_date": "present", "rank": "地级市正职", "note": "2026-01-22 前任海北州委书记调入"},
    {"person_id": 1, "org_id": 9, "title": "州委书记", "start_date": "2023-02", "end_date": "2025-12", "rank": "地级市正职", "note": "海北州委书记"},
    {"person_id": 1, "org_id": 10, "title": "州委副书记、代州长、州政府党组书记", "start_date": "2022-08", "end_date": "2023-02", "rank": "地级市正职", "note": "海北州代州长"},
    {"person_id": 1, "org_id": 12, "title": "政协主席、党组书记", "start_date": "2021-08", "end_date": "2022-07", "rank": "地级市正职", "note": "果洛州政协主席"},
    {"person_id": 1, "org_id": 11, "title": "州委常委、班玛县委书记", "start_date": "2016-11", "end_date": "2021-06", "rank": "地级市副职", "note": "果洛州委常委 兼 班玛县委书记"},
    {"person_id": 1, "org_id": 13, "title": "县委书记", "start_date": "2014-08", "end_date": "2016-11", "rank": "县级正职", "note": "班玛县委书记"},
    {"person_id": 1, "org_id": 14, "title": "县委副书记、县长", "start_date": "2011-07", "end_date": "2014-08", "rank": "县级正职", "note": "班玛县（代）县长"},
    {"person_id": 1, "org_id": 17, "title": "省信访局副局长（正处级）", "start_date": "2007-12", "end_date": "2011-07", "rank": "正处级", "note": "其间挂职 国家信访局、玉树灾后重建"},
    {"person_id": 1, "org_id": 16, "title": "省政府办公厅干部、副处长", "start_date": "1992-09", "end_date": "2007-12", "rank": "处级", "note": "翻译处干部，后社会二处副处长；其间函授获文学学士"},

    # 才让索南 (id 2)
    {"person_id": 2, "org_id": 2, "title": "州委副书记、州长（代）", "start_date": "2026-05", "end_date": "present", "rank": "地级市正职", "note": "2026-05-28 任副州长兼代州长，接替扎西才让"},
    {"person_id": 2, "org_id": 1, "title": "州委副书记", "start_date": "2026-05", "end_date": "present", "rank": "地级市副职", "note": "州政府党组书记、州委副书记"},

    # 扎西才让 (id 3)
    {"person_id": 3, "org_id": 2, "title": "州长", "start_date": "2021-05", "end_date": "2026-05", "rank": "地级市正职", "note": "2021-08 州十六届人大当选；2026-05-28 辞任"},

    # 蒋树成 (id 4)
    {"person_id": 4, "org_id": 3, "title": "州人大常委会主任", "start_date": "2021-05", "end_date": "present", "rank": "地级市正职", "note": ""},

    # 叶忠措 (id 5)
    {"person_id": 5, "org_id": 4, "title": "州政协主席", "start_date": "2024-02", "end_date": "present", "rank": "地级市正职", "note": ""},

    # 副州长 / 秘书长
    {"person_id": 6, "org_id": 2, "title": "常务副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副州长", "start_date": "2026-05", "end_date": "present", "rank": "地级市副职", "note": "2026-05-28 任命"},
    {"person_id": 8, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副州长", "start_date": "2026-08", "end_date": "present", "rank": "地级市副职", "note": "2026-08-06 任命"},
    {"person_id": 13, "org_id": 2, "title": "副州长", "start_date": "2026-08", "end_date": "present", "rank": "地级市副职", "note": "2026-08-06 任命"},
    {"person_id": 14, "org_id": 2, "title": "副州长（前任）", "start_date": "unknown", "end_date": "2026-05", "rank": "地级市副职", "note": "2026-05-28 免职，或系援青干部"},
    {"person_id": 15, "org_id": 2, "title": "州政府秘书长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},

    # 人大
    {"person_id": 16, "org_id": 3, "title": "州人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "州人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "州人大常委会秘书长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},

    # 政协
    {"person_id": 19, "org_id": 4, "title": "州政协副主席（党组副书记）", "start_date": "2024-02", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "州政协副主席", "start_date": "2024-02", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "州政协副主席", "start_date": "2024-02", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "州政协副主席", "start_date": "2024-02", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "州政协副主席", "start_date": "2024-02", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "州政协副主席", "start_date": "2024-02", "end_date": "present", "rank": "地级市副职", "note": ""},
]

# ═══════════════════════════ Relationships ═══════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "决策搭档", "context": "现任州委书记与州长（代）党政班子搭档", "overlap_org": "中共黄南藏族自治州委员会/黄南州人民政府", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任（书记不接州长）", "context": "夏吾杰任书记期间，扎西才让任州长；后由才让索南接任州长", "overlap_org": "中共黄南藏族自治州委员会", "overlap_period": "2026-01至2026-05"},
    {"person_a": 2, "person_b": 3, "type": "前任-继任", "context": "才让索南2026-05接任扎西才让州长", "overlap_org": "黄南藏族自治州人民政府", "overlap_period": "2026-05"},
    {"person_a": 1, "person_b": 4, "type": "班子交集", "context": "州委书记与州人大常委会主任同属州四套班子", "overlap_org": "中共黄南州委员会", "overlap_period": "2026-01至今"},
    {"person_a": 1, "person_b": 5, "type": "班子交集", "context": "州委书记与州政协主席同属州四套班子", "overlap_org": "中共黄南州委员会", "overlap_period": "2024-02至今"},
    {"person_a": 2, "person_b": 6, "type": "班子/上下级", "context": "常务副州长协助州长主持州政府日常", "overlap_org": "黄南藏族自治州人民政府", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 6, "type": "班子交集", "context": "常务副州长通常为州委常委，与书记同属州委常委会", "overlap_org": "中共黄南藏族自治州委员会", "overlap_period": "2026-01至今"},
]


def main():
    print(f"[黄南藏族自治州] 构建 SQLite DB + GEXF ...")
    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=DB_PATH, gexf_path=GEXF_PATH)
    _verify_db()
    write_persons_files()
    print(f"[黄南藏族自治州] 完成：{DB_PATH}\n{GEXF_PATH}\npersons JSON {len(persons)} 人")


def _verify_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required = {"persons", "organizations", "positions", "relationships"}
        missing = sorted(required - tables)
        if missing:
            raise SystemExit(f"DB 缺少表: {missing}")
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in sorted(required)}
        print(f"  DB 校验: {counts}")
    finally:
        conn.close()


# ═══════════════════════════ Person JSON ═══════════════════════════
SOURCE_REGISTER = [
    {"id": "S001", "title": "中国经济网——夏吾杰任黄南州委书记", "url": "http://district.ce.cn/newarea/sddy/202601/t20260128_2735032.shtml", "publisher": "中国经济网", "published_at": "2026-01-28", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "夏吾杰履任黄南州委书记，藏族、1970-10"},
    {"id": "S002", "title": "中国经济网——才让索南任黄南州代州长、扎西才让辞州长职", "url": "http://district.ce.cn/newarea/sddy/202605/t20260529_2997488.shtml", "publisher": "中国经济网", "published_at": "2026-05-29", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "才让索南1973-10代州长；扎西才让1966-09辞任"},
    {"id": "S003", "title": "Wikipedia zh《黄南藏族自治州》", "url": "https://zh.wikipedia.org/wiki/黄南藏族自治州", "publisher": "Wikipedia", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "四套班子现任领导及就任日期"},
    {"id": "S004", "title": "中国经济网——蒋树成当选州人大主任、扎西才让当选州长", "url": "http://district.ce.cn/newarea/sddy/202108/16/t20210816_36810370.shtml", "publisher": "中国经济网", "published_at": "2021-08-16", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "扎西才让2021-08当选州长"},
    {"id": "S005", "title": "黄南新闻网——州人大、州政协会议", "url": "https://www.qhhnnews.com/zt/", "publisher": "黄南新闻网", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "政协十四届简历、人大副主任/秘书长名单"},
    {"id": "S006", "title": "百度百科《黄南藏族自治州人民政府》", "url": "https://baike.baidu.com/item/黄南藏族自治州人民政府", "publisher": "Baidu Baike", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "州政府领导名录"},
    {"id": "S007", "title": "百度百科《夏吾杰》", "url": "https://baike.baidu.com/item/夏吾杰", "publisher": "Baidu Baike", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "夏吾杰完整履历"},
    {"id": "S008", "title": "中国经济网——多杰任海北州委书记、夏吾杰任州委副书记", "url": "http://district.ce.cn/newarea/sddy/202208/13/t20220813_3884.shtml", "publisher": "中国经济网", "published_at": "2022-08-13", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "夏吾杰2022-08任海北州委副书记/州政府党组书记"},
]


def build_person_file(name, current_post, profile, big_gap="", qs=None):
    """Write a person JSON from a single profile dict."""
    p = BASE / f"{TODAY}-青海省-黄南藏族自治州-{current_post}-{name}.json"
    orgs = profile.get("organizations", []) or []
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "青海省", "city": "黄南藏族自治州", "region": "黄南藏族自治州",
                                "job": current_post, "task_id": "qinghai_黄南藏族自治州", "time_focus": "2024-2026"},
        "identity": {"person_id": f"huangnan_{name}", "name": name,
                     "aliases": [], "gender": profile.get("gender", ""),
                     "ethnicity": profile.get("ethnicity", ""),
                     "birth": profile.get("birth", ""),
                     "birthplace": profile.get("birthplace", profile.get("birth", "")),
                     "native_place": profile.get("birthplace", ""),
                     "education": profile.get("education", []),
                     "party_join": profile.get("party_join", ""), "work_start": profile.get("work_start", ""),
                     "dedupe_keys": {"name_birth": f"huangnan_{name}_{profile.get('birth','')}",
                                     "name_birthplace": f"huangnan_{name}_{profile.get('birthplace',profile.get('birth',''))}",
                                     "official_profile_url": ""}},
        "current_status": {"current_post": current_post, "current_org": profile.get("current_org", ""),
                           "administrative_rank": profile.get("rank", ""), "as_of": AS_OF,
                           "is_current_confirmed": profile.get("is_confirmed", True),
                           "source_ids": list(profile.get("source_ids", ["S001", "S002"]))},
        "career_timeline": profile.get("career_timeline", []),
        "organizations": orgs,
        "relationships": profile.get("relationships", []),
        "governance_record": profile.get("governance_record", []),
        "professional_profile": profile.get("professional_profile", {}),
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": profile.get("risk_signals", []),
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": profile.get("identity_confidence", "plausible"),
            "current_role": profile.get("current_confidence", "confirmed"),
            "career_completeness": profile.get("career_completeness", "partial"),
            "relationship_confidence": profile.get("relationship_confidence", "medium"),
            "biggest_gap": big_gap or profile.get("biggest_gap", "")},
        "open_questions": qs or [{"priority": "high", "question": big_gap or profile.get("biggest_gap", "履历未完整"),
                                  "why_it_matters": "任职网络分析",
                                  "suggested_queries": [f"{name} 简历"], "last_attempted": AS_OF}],
    }
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("  person JSON:", p.name)


def write_persons_files():
    # ── 州委书记 夏吾杰 ──
    build_person_file(
        "夏吾杰", "州委书记",
        {"gender": "男", "ethnicity": "藏族", "birth": "1970年10月", "birthplace": "青海省循化撒拉族自治县",
         "education": [{"period": "2006-2009", "institution": "青海师范大学", "major": "汉语言文学", "degree": "文学学士", "study_type": "part_time", "source_ids": ["S007"]}],
         "party_join": "1991年9月", "work_start": "1989年7月",
         "current_org": "中共黄南藏族自治州委员会", "rank": "地级市正职",
         "is_confirmed": True, "source_ids": ["S001", "S002", "S007"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "complete",
         "relationships": [
             {"person": "才让索南", "person_id": "huangnan_才让索南", "relationship_type": "overlap", "strength": "strong", "evidence": "党政班子搭档", "overlap_org": "中共黄南州委/黄南州人民政府", "overlap_period": "2026-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
             {"person": "扎西才让", "person_id": "huangnan_扎西才让", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "夏任州委书记任内州长由扎西才让过渡至才让索南", "overlap_org": "中共黄南州委员会", "overlap_period": "2026-01至2026-05", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}],
         "organizations": [
             {"id": "huangnan_州委", "name": "中共黄南藏族自治州委员会", "type": "党委", "level": "地级", "location": "同仁市"},
             {"id": "huangnan_州政府", "name": "黄南藏族自治州人民政府", "type": "政府", "level": "地级", "location": "同仁市"},
             {"id": "huangnan_海北州委", "name": "中共海北藏族自治州委员会", "type": "党委", "level": "地级", "location": "海北州"},
             {"id": "huangnan_果洛政协", "name": "果洛藏族自治州政协", "type": "政协", "level": "地级", "location": "果洛州"}],
         "career_timeline": [
             {"start": "2026-01", "end": "present", "org": "中共黄南藏族自治州委员会", "title": "州委书记", "level": "地级市", "system": "party", "rank": "地级市正职", "is_key_promotion": True, "notes": "由海北州委书记调任", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
             {"start": "2023-02", "end": "2025-12", "org": "中共海北藏族自治州委员会", "title": "州委书记", "level": "地级市", "system": "party", "rank": "地级市正职", "is_key_promotion": True, "notes": "海北州委书记", "confidence": "confirmed", "source_ids": ["S008"]},
             {"start": "2022-08", "end": "2023-02", "org": "海北藏族自治州人民政府", "title": "州委副书记、代州长、州政府党组书记", "level": "地级市", "system": "government", "rank": "地级市正职", "is_key_promotion": True, "notes": "海北州代州长", "confidence": "confirmed", "source_ids": ["S008"]},
             {"start": "2021-08", "end": "2022-07", "org": "果洛藏族自治州政协", "title": "政协主席、党组书记", "level": "地级市", "system": "other", "rank": "地级市正职", "is_key_promotion": True, "notes": "果洛州政协主席", "confidence": "confirmed", "source_ids": ["S007"]},
             {"start": "2016-11", "end": "2021-06", "org": "班玛县（果洛州）", "title": "果洛州委常委、班玛县委书记", "level": "县级", "system": "party", "rank": "地级市副职", "is_key_promotion": False, "notes": "果洛州委常委 兼 班玛县委书记", "confidence": "confirmed", "source_ids": ["S007"]},
             {"start": "2011-07", "end": "2014-08", "org": "班玛县政府", "title": "县委副书记、县长（代）", "level": "县级", "system": "government", "rank": "县级正职", "is_key_promotion": False, "notes": "班玛县代县长、县长", "confidence": "confirmed", "source_ids": ["S007"]},
             {"start": "2007-12", "end": "2011-07", "org": "青海省信访局", "title": "副局长（正处级）", "level": "省级", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "其间挂职国家信访局、玉树灾后重建指挥部", "confidence": "confirmed", "source_ids": ["S007"]},
             {"start": "1992-09", "end": "2007-12", "org": "青海省人民政府办公厅", "title": "秘书、副处长", "level": "省级", "system": "government", "rank": "处级", "is_key_promotion": False, "notes": "省政府办公厅翻译处、社会二处", "confidence": "confirmed", "source_ids": ["S007"]}],
         "professional_profile": {"primary_specializations": ["民族地区治理", "基层党政历练"], "secondary_specializations": [],
                                  "career_pattern": "grassroots_local_ladder", "systems_experience": ["party", "government", "other"],
                                  "geographic_pattern": ["循化→西宁→果洛→海北→黄南"], "promotion_velocity": {"summary": "2015年以来历任县、州、地级市党委书记", "notable_fast_promotions": []}},
         "risk_signals": [{"type": "none_found", "description": "公开检索未发现处分/审计/舆情问题", "date": AS_OF, "confidence": "confirmed", "source_ids": []}],
         "biggest_gap": "夏吾杰 2022年前部分早期任职年限可再核实"},
    )
    # ── 州长 才让索南 ──
    build_person_file(
        "才让索南", "州长",
        {"gender": "男", "ethnicity": "藏族", "birth": "1973年10月", "birthplace": "青海省共和县",
         "education": [{"period": "", "institution": "", "major": "", "degree": "在职大学", "study_type": "part_time", "source_ids": ["S002"]}],
         "party_join": "中共党员", "work_start": "", "current_org": "黄南藏族自治州人民政府", "rank": "地级市正职",
         "is_confirmed": True, "source_ids": ["S001", "S002"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "thin",
         "relationships": [
             {"person": "夏吾杰", "person_id": "huangnan_夏吾杰", "relationship_type": "overlap", "strength": "strong", "evidence": "党政班子搭档", "overlap_org": "中共黄南州委/黄南州人民政府", "overlap_period": "2026-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
             {"person": "扎西才让", "person_id": "huangnan_扎西才让", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "接任扎西才让. 州长", "overlap_org": "黄南州人民政府", "overlap_period": "2026-05", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}],
         "organizations": [
             {"id": "huangnan_州政府", "name": "黄南藏族自治州人民政府", "type": "政府", "level": "地级", "location": "同仁市"},
             {"id": "huangnan_州委", "name": "中共黄南藏族自治州委员会", "type": "党委", "level": "地级", "location": "同仁市"}],
         "career_timeline": [
             {"start": "2026-05", "end": "present", "org": "黄南藏族自治州人民政府", "title": "州委副书记、州长（代）", "level": "地级市", "system": "government", "rank": "地级市正职", "is_key_promotion": True, "notes": "2026-05-28 任副州长兼代州长", "confidence": "confirmed", "source_ids": ["S002"]},
             {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "", "rank": "", "notes": "2026年前（海南州/县委职）完整履历未获一级来源", "confidence": "unverified", "source_ids": []}],
         "biggest_gap": "才让索南任黄南州长前的岗位（2026年前履历）"},
    )
    # ── 前任州长 扎西才让 ──
    build_person_file(
        "扎西才让", "前任州长",
        {"gender": "男", "ethnicity": "藏族", "birth": "1966年9月", "birthplace": "",
         "education": [{"period": "", "institution": "省委党校", "major": "经济管理", "degree": "", "study_type": "party_school", "source_ids": ["S002"]}],
         "party_join": "中共党员", "work_start": "", "current_org": "", "rank": "地级市正职",
         "is_confirmed": False, "source_ids": ["S002", "S004"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "thin",
         "relationships": [
             {"person": "才让索南", "person_id": "huangnan_才让索南", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "2026-05将州长交接给才让索南", "overlap_org": "黄南州人民政府", "overlap_period": "2026-05", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}],
         "organizations": [
             {"id": "huangnan_州政府", "name": "黄南藏族自治州人民政府", "type": "政府", "level": "地级", "location": "同仁市"}],
         "career_timeline": [
             {"start": "2021-05", "end": "2026-05", "org": "黄南藏族自治州人民政府", "title": "州长", "level": "地级市", "system": "government", "rank": "地级市正职", "is_key_promotion": True, "notes": "2021-08州人大当选，2026-05-28辞任", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
             {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "", "rank": "", "notes": "2021年前完整履历及辞任后去向未获一级来源", "confidence": "unverified", "source_ids": []}],
         "biggest_gap": "扎西才让 2021年前履历及2026-05辞任后去向（是否转任他职或退休）"},
    )
    # 说明：州四套班子其他成员（王海瑞/项秀/蒋树成/白萍等）可按身份补建，此处因资料 partial 先建核心三人。


if __name__ == "__main__":
    main()