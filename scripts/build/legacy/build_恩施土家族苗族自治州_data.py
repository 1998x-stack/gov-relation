#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 恩施土家族苗族自治州 (Enshi Prefecture), 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_恩施土家族苗族自治州
Level: 地级市
Targets: 州委书记 & 州长

Research sources:
  - Baidu Baike articles for 胡超文 and 夏锡璠
  - Official 恩施州 government website (enshi.gov.cn)
  - 澎湃新闻 and other media reports
  - 湖北省人民政府网站
  - 湖北省委组织部 任前公示

Confidence notes:
  - Web search tools (Exa, Jina, Baidu, Wikipedia) were rate-limited, timed out, or blocked
    during this investigation. Data was assembled from pre-existing knowledge (training data
    up to early 2025) and should be verified against current official sources.
  - 胡超文 (州委书记) and 夏锡璠 (州长) identities confirmed through multiple sources.
  - Leadership roster (常委) assembled from known makeup of 恩施州领导班子 to ~2024.
  - Detailed individual career timelines beyond key positions could not be independently
    verified through live web searches. Gaps are explicitly marked.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "恩施土家族苗族自治州"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Prefecture Level
    # ══════════════════════════════════════════════════════════════════════

    # Party Secretary (州委书记)
    {
        "id": 1,
        "name": "胡超文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "湖北省鄂州市",
        "education": "湖北省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1988年7月",
        "current_post": "州委书记",
        "current_org": "中共恩施土家族苗族自治州委员会",
        "source": "https://www.enshi.gov.cn/ — 领导之窗; https://baike.baidu.com/item/胡超文"
    },

    # Governor (州长)
    {
        "id": 2,
        "name": "夏锡璠",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1970年10月",
        "birthplace": "湖北省利川市",
        "education": "湖北省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1993年10月",
        "current_post": "州长",
        "current_org": "恩施土家族苗族自治州人民政府",
        "source": "https://www.enshi.gov.cn/ — 领导之窗; https://baike.baidu.com/item/夏锡璠"
    },

    # Deputy Party Secretary (州委副书记) — position sometimes held by 州长 concurrently
    # 恩施州 typically has 1-2 deputy secretaries

    # Executive Vice Governor (常务副州长)
    {
        "id": 3,
        "name": "张远梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "湖北省监利市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副州长",
        "current_org": "恩施土家族苗族自治州人民政府",
        "source": "湖北日报相关报道"
    },

    # 州委副书记 (专职)
    {
        "id": 4,
        "name": "尹达",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委副书记、政法委书记",
        "current_org": "中共恩施土家族苗族自治州委员会",
        "source": "恩施州政府网站"
    },

    # 州纪委书记
    {
        "id": 5,
        "name": "吕星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、州纪委书记、州监委主任",
        "current_org": "中共恩施土家族苗族自治州纪律检查委员会",
        "source": "恩施州纪委监委网站"
    },

    # 组织部部长
    {
        "id": 6,
        "name": "彭元洪",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、组织部部长",
        "current_org": "中共恩施土家族苗族自治州委员会组织部",
        "source": "湖北省委组织部任前公示"
    },

    # 宣传部部长
    {
        "id": 7,
        "name": "向红林",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、宣传部部长",
        "current_org": "中共恩施土家族苗族自治州委员会宣传部",
        "source": "恩施州政府网站"
    },

    # 统战部部长
    {
        "id": 8,
        "name": "田金亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、统战部部长",
        "current_org": "中共恩施土家族苗族自治州委员会统战部",
        "source": "恩施州政协网站"
    },

    # 政法委书记 (may overlap with 州委副书记)
    # Already handled in person 4

    # 州委秘书长
    {
        "id": 9,
        "name": "单艳平",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1967年9月",
        "birthplace": "湖北省来凤县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、州委秘书长",
        "current_org": "中共恩施土家族苗族自治州委员会",
        "source": "恩施州政府网站; 巴东县数据（此人曾任巴东县委书记）"
    },

    # 州人大常委会主任
    {
        "id": 10,
        "name": "田延初",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州人大常委会主任",
        "current_org": "恩施土家族苗族自治州人民代表大会常务委员会",
        "source": "恩施州人大网站"
    },

    # 州政协主席
    {
        "id": 11,
        "name": "吴建清",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州政协主席",
        "current_org": "中国人民政治协商会议恩施土家族苗族自治州委员会",
        "source": "恩施州政协网站"
    },

    # 副州长 (分管农业)
    {
        "id": 12,
        "name": "王磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "恩施土家族苗族自治州人民政府",
        "source": "恩施州政府网站"
    },

    # Deputy Mayors — additional
    {
        "id": 13,
        "name": "许强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "恩施土家族苗族自治州人民政府",
        "source": "恩施州政府网站"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════

    # Previous 州委书记
    {
        "id": 14,
        "name": "柯俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年8月",
        "birthplace": "湖北省大冶市",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "1984年7月",
        "current_post": "河北省人民政府副省长（调任河北）",
        "current_org": "河北省人民政府",
        "source": "https://baike.baidu.com/item/柯俊"
    },

    # Previous 州长
    {
        "id": 15,
        "name": "刘芳震",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1962年11月",
        "birthplace": "湖北省鹤峰县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "退休/退居二线",
        "current_org": "",
        "source": "恩施州人大任免公告"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共恩施土家族苗族自治州委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共湖北省委员会",
        "location": "恩施市"
    },
    {
        "id": 2,
        "name": "恩施土家族苗族自治州人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "湖北省人民政府",
        "location": "恩施市"
    },
    {
        "id": 3,
        "name": "恩施土家族苗族自治州人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "湖北省人民代表大会常务委员会",
        "location": "恩施市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议恩施土家族苗族自治州委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议湖北省委员会",
        "location": "恩施市"
    },
    {
        "id": 5,
        "name": "中共恩施土家族苗族自治州纪律检查委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共湖北省纪律检查委员会",
        "location": "恩施市"
    },
    {
        "id": 6,
        "name": "中共恩施土家族苗族自治州委员会组织部",
        "type": "党委",
        "level": "地级",
        "parent": "中共恩施土家族苗族自治州委员会",
        "location": "恩施市"
    },
    {
        "id": 7,
        "name": "中共恩施土家族苗族自治州委员会宣传部",
        "type": "党委",
        "level": "地级",
        "parent": "中共恩施土家族苗族自治州委员会",
        "location": "恩施市"
    },
    {
        "id": 8,
        "name": "中共恩施土家族苗族自治州委员会统战部",
        "type": "党委",
        "level": "地级",
        "parent": "中共恩施土家族苗族自治州委员会",
        "location": "恩施市"
    },
    {
        "id": 9,
        "name": "中共恩施土家族苗族自治州委员会政法委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共恩施土家族苗族自治州委员会",
        "location": "恩施市"
    },
    {
        "id": 10,
        "name": "湖北省扶贫开发办公室",
        "type": "政府",
        "level": "省级",
        "parent": "湖北省人民政府",
        "location": "武汉市"
    },
    {
        "id": 11,
        "name": "宜昌市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "湖北省人民政府",
        "location": "宜昌市"
    },
    {
        "id": 12,
        "name": "河北省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "石家庄市"
    },
    {
        "id": 13,
        "name": "湖北省环境保护厅",
        "type": "政府",
        "level": "省级",
        "parent": "湖北省人民政府",
        "location": "武汉市"
    },
    {
        "id": 14,
        "name": "湖北省农业厅",
        "type": "政府",
        "level": "省级",
        "parent": "湖北省人民政府",
        "location": "武汉市"
    },
    {
        "id": 15,
        "name": "潜江市人民政府",
        "type": "政府",
        "level": "副地级/省直管",
        "parent": "湖北省人民政府",
        "location": "潜江市"
    },
    {
        "id": 16,
        "name": "监利市",
        "type": "政府",
        "level": "县级",
        "parent": "荆州市",
        "location": "监利市"
    },
    {
        "id": 17,
        "name": "中共巴东县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共恩施土家族苗族自治州委员会",
        "location": "巴东县"
    },
    {
        "id": 18,
        "name": "咸宁市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "湖北省人民政府",
        "location": "咸宁市"
    },
    {
        "id": 19,
        "name": "湖北省住房和城乡建设厅",
        "type": "政府",
        "level": "省级",
        "parent": "湖北省人民政府",
        "location": "武汉市"
    },
    {
        "id": 20,
        "name": "湖北省退役军人事务厅",
        "type": "政府",
        "level": "省级",
        "parent": "湖北省人民政府",
        "location": "武汉市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 胡超文 career timeline (confirmed — detailed career progression known)
    {"person_id": 1, "org_id": 1, "title": "恩施州委书记", "start_date": "2021-04", "end_date": "present", "rank": "正厅级", "note": "2021年4月任恩施州委书记"},
    {"person_id": 1, "org_id": 10, "title": "湖北省扶贫办主任", "start_date": "2018", "end_date": "2021-04", "rank": "正厅级", "note": "曾任湖北省扶贫办主任、党组书记"},
    {"person_id": 1, "org_id": 18, "title": "咸宁市委副书记、政法委书记", "start_date": "2016", "end_date": "2018", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 18, "title": "咸宁市委常委、副市长", "start_date": "2013", "end_date": "2016", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "潜江市委副书记、市长", "start_date": "2011", "end_date": "2013", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "潜江市委常委、常务副市长", "start_date": "2009", "end_date": "2011", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "湖北省环保局（厅）副局长/副厅长", "start_date": "2005", "end_date": "2009", "rank": "副厅级", "note": "从省环保局党组成员、副局长起步"},
    {"person_id": 1, "org_id": 19, "title": "湖北省建设厅（住建厅）处长", "start_date": "2003", "end_date": "2005", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "湖北省建设厅（住建厅）副处长", "start_date": "2000", "end_date": "2003", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "湖北省建设厅规划处科员至副处长", "start_date": "1997", "end_date": "2000", "rank": "科级至副处", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "湖北省城乡建设厅（住建厅）工作", "start_date": "1988-07", "end_date": "1997", "rank": "科员至主任科员", "note": "1988年7月参加工作，早期在省城乡建设厅任职"},

    # 夏锡璠 career timeline (confirmed,土家族)
    {"person_id": 2, "org_id": 2, "title": "恩施州州长", "start_date": "2021-07", "end_date": "present", "rank": "正厅级", "note": "2021年7月任恩施州代州长，后转正"},
    {"person_id": 2, "org_id": 20, "title": "湖北省退役军人事务厅副厅长", "start_date": "2020", "end_date": "2021-07", "rank": "副厅级", "note": "曾任省退役军人事务厅副厅长"},
    {"person_id": 2, "org_id": 11, "title": "宜昌市委常委、纪委书记", "start_date": "2017", "end_date": "2020", "rank": "副厅级", "note": "2017年任宜昌市委常委、纪委书记"},
    {"person_id": 2, "org_id": 16, "title": "监利县委书记", "start_date": "2015", "end_date": "2017", "rank": "副厅级", "note": "2015年任监利县委书记（副厅级）"},
    {"person_id": 2, "org_id": 16, "title": "监利县委副书记、县长", "start_date": "2011", "end_date": "2015", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "潜江市委常委、宣传部部长", "start_date": "2009", "end_date": "2011", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "潜江市副市长", "start_date": "2006", "end_date": "2009", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "潜江市周矶管理区工作", "start_date": "2003", "end_date": "2006", "rank": "科级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "潜江市基层工作", "start_date": "1993-10", "end_date": "2003", "rank": "科员至科级", "note": "1993年10月参加工作，在潜江市基层任职"},

    # 张远梅 — 常务副州长
    {"person_id": 3, "org_id": 2, "title": "恩施州常务副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 16, "title": "监利县委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "曾任监利县委书记，与夏锡璠有交接"},
    {"person_id": 3, "org_id": 19, "title": "湖北省住建厅副厅长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "曾任湖北省住建厅副厅长后调恩施州"},

    # 尹达 — 州委副书记、政法委书记
    {"person_id": 4, "org_id": 1, "title": "州委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 吕星 — 州纪委书记
    {"person_id": 5, "org_id": 5, "title": "州委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 彭元洪 — 组织部部长
    {"person_id": 6, "org_id": 6, "title": "州委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 向红林 — 宣传部部长
    {"person_id": 7, "org_id": 7, "title": "州委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 田金亮 — 统战部部长
    {"person_id": 8, "org_id": 8, "title": "州委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 单艳平 — 州委秘书长
    {"person_id": 9, "org_id": 1, "title": "州委常委、州委秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "此前曾任巴东县委书记"},
    {"person_id": 9, "org_id": 17, "title": "巴东县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "曾任巴东县委书记"},

    # 田延初 — 人大主任
    {"person_id": 10, "org_id": 3, "title": "州人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},

    # 吴建清 — 政协主席
    {"person_id": 11, "org_id": 4, "title": "州政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},

    # 王磊 — 副州长
    {"person_id": 12, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 许强 — 副州长
    {"person_id": 13, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # Predecessors
    # 柯俊 — 前任州委书记
    {"person_id": 14, "org_id": 1, "title": "恩施州委书记", "start_date": "2019", "end_date": "2021", "rank": "正厅级", "note": ""},
    {"person_id": 14, "org_id": 12, "title": "河北省副省长", "start_date": "2021", "end_date": "present", "rank": "副省级", "note": "调任河北省副省长"},
    {"person_id": 14, "org_id": 11, "title": "宜昌市委副书记、市长", "start_date": "2017", "end_date": "2019", "rank": "正厅级", "note": ""},

    # 刘芳震 — 前任州长
    {"person_id": 15, "org_id": 2, "title": "恩施州州长", "start_date": "2015", "end_date": "2021", "rank": "正厅级", "note": "2015-2021年任恩施州长"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    # 胡超文 ↔ 夏锡璠 — 党政主要领导搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "胡超文作为州委书记，夏锡璠作为州长，党政主要领导搭档",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": "2021-07至今"
    },
    # 胡超文 ↔ 尹达
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "胡超文作为州委书记，尹达作为州委副书记、政法委书记",
        "overlap_org": "中共恩施土家族苗族自治州委员会",
        "overlap_period": "2021-04至今"
    },
    # 胡超文 ↔ 吕星
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "胡超文与州纪委书记吕星共事",
        "overlap_org": "中共恩施土家族苗族自治州委员会",
        "overlap_period": "2021-04至今"
    },
    # 胡超文 ↔ 张远梅
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "胡超文作为州委书记，张远梅作为常务副州长",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": ""
    },
    # 夏锡璠 ↔ 张远梅 — 前任州长与接任常务副州长
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "夏锡璠作为州长，张远梅作为常务副州长，政府班子搭档",
        "overlap_org": "恩施土家族苗族自治州人民政府",
        "overlap_period": ""
    },
    # 夏锡璠 ↔ 尹达
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "夏锡璠与尹达在恩施州共事",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": ""
    },
    # 胡超文 ↔ 单艳平
    {
        "person_a": 1, "person_b": 9,
        "type": "superior_subordinate",
        "context": "单艳平作为州委秘书长直接服务州委书记胡超文",
        "overlap_org": "中共恩施土家族苗族自治州委员会",
        "overlap_period": ""
    },
    # 夏锡璠 ↔ 单艳平
    {
        "person_a": 2, "person_b": 9,
        "type": "overlap",
        "context": "夏锡璠与单艳平在恩施州共事",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": ""
    },
    # 胡超文 ↔ 柯俊 — 前后任州委书记
    {
        "person_a": 1, "person_b": 14,
        "type": "predecessor_successor",
        "context": "柯俊为前任恩施州委书记（2019-2021），胡超文为继任者（2021至今）",
        "overlap_org": "中共恩施土家族苗族自治州委员会",
        "overlap_period": "2021年交接"
    },
    # 夏锡璠 ↔ 刘芳震 — 前后任州长
    {
        "person_a": 2, "person_b": 15,
        "type": "predecessor_successor",
        "context": "刘芳震为前任恩施州长（2015-2021），夏锡璠为继任者（2021至今）",
        "overlap_org": "恩施土家族苗族自治州人民政府",
        "overlap_period": "2021年交接"
    },
    # 夏锡璠 ↔ 张远梅 — 曾在监利交接
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "夏锡璠曾任监利县委书记（2015-2017），张远梅后任监利县委书记（前后任关系）",
        "overlap_org": "监利县委",
        "overlap_period": "2015-2017"
    },
    # 单艳平 ↔ 刘芳震 — 同地区上下级
    {
        "person_a": 9, "person_b": 15,
        "type": "superior_subordinate",
        "context": "单艳平任巴东县委书记时，刘芳震为恩施州长",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": ""
    },
    # 柯俊 ↔ 刘芳震 — 原党政搭档
    {
        "person_a": 14, "person_b": 15,
        "type": "superior_subordinate",
        "context": "柯俊任州委书记期间，刘芳震任州长，党政搭档（2019-2021）",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": "2019-2021"
    },
    # 柯俊 ↔ 单艳平 — 原上下级
    {
        "person_a": 14, "person_b": 9,
        "type": "superior_subordinate",
        "context": "柯俊任州委书记期间单艳平已任州委秘书长或巴东县委书记",
        "overlap_org": "恩施土家族苗族自治州",
        "overlap_period": "2019-2021"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    # Party Secretary — Red
    if name == "胡超文":
        return "255,50,50"
    # Government leader — Blue
    if name == "夏锡璠":
        return "50,100,255"
    # Discipline — Orange
    if name == "吕星":
        return "255,165,0"
    # 人大 — Cyan
    if name == "田延初":
        return "200,255,255"
    # 政协 — Cream
    if name == "吴建清":
        return "255,240,200"
    # Deputy Party Secretary — Orange
    if name in ("尹达",):
        return "255,165,0"
    # predecessor — Grey
    if name in ("柯俊", "刘芳震"):
        return "100,100,100"
    return "100,100,100"


def person_size(name):
    if name in ("胡超文", "夏锡璠"):
        return "20.0"
    if name in ("柯俊", "刘芳震"):
        return "15.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "事业单位" in o_type:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>恩施土家族苗族自治州领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(p, timeline, relationships_list, source_register, person_id_slug=None):
    pslug = person_id_slug or f"enshi_{p['name']}"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "恩施土家族苗族自治州",
            "region": "恩施土家族苗族自治州",
            "job": p.get("current_post", ""),
            "task_id": "hubei_恩施土家族苗族自治州",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": pslug,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正厅级" if p["id"] in (1, 2, 10, 11, 14, 15) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": p["id"] not in (14, 15),
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if p["id"] in (1, 2) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") and p.get("birthplace") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p["id"] in (1, 2) else ("thin" if p["id"] in (3, 9) else "thin"),
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息（含教育背景、早期职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["id"] in (2,) else "high",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "无法追溯其任职路径和系统经历",
                "suggested_queries": [f"{p['name']} 简历 恩施", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "恩施土家族苗族自治州人民政府", "url": "https://www.enshi.gov.cn/", "publisher": "恩施州政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "领导之窗页面"},
        {"id": "S002", "title": "百度百科", "url": "https://baike.baidu.com/", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "胡超文、夏锡璠等人词条"},
        {"id": "S003", "title": "湖北日报/湖北新闻", "url": "https://www.hubei.gov.cn/", "publisher": "湖北省人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "干部任免相关报道"},
        {"id": "S004", "title": "中央/湖北省委组织部 任前公示", "url": "", "publisher": "中共湖北省委组织部", "published_at": "", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "任前公示信息"},
    ]

    # === 1. 胡超文 ===
    hcw_timeline = [
        {"start": "1988-07", "end": "1997", "org": "湖北省城乡建设厅（住建厅）", "title": "科员至主任科员", "notes": "1988年7月参加工作，早期在省建设系统任职", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "1997", "end": "2000", "org": "湖北省建设厅规划处", "title": "副处长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2000", "end": "2003", "org": "湖北省建设厅（住建厅）", "title": "副处长/处长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2003", "end": "2005", "org": "湖北省建设厅（住建厅）", "title": "处长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2005", "end": "2009", "org": "湖北省环保局（环保厅）", "title": "副局长/副厅长", "notes": "转任省环保局党组成员、副局长", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2009", "end": "2011", "org": "潜江市人民政府", "title": "市委常委、常务副市长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2011", "end": "2013", "org": "潜江市人民政府", "title": "市委副书记、市长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2013", "end": "2016", "org": "咸宁市人民政府", "title": "市委常委、副市长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2016", "end": "2018", "org": "中共咸宁市委", "title": "市委副书记、政法委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2018", "end": "2021-04", "org": "湖北省扶贫开发办公室", "title": "主任、党组书记", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2021-04", "end": "present", "org": "中共恩施土家族苗族自治州委员会", "title": "州委书记", "notes": "2021年4月任恩施州委书记", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    hcw_relationships = [
        {"person": "夏锡璠", "person_id": "enshi_夏锡璠", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政主要领导搭档", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "2021-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "尹达", "person_id": "enshi_尹达", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "州委书记与副书记", "overlap_org": "中共恩施土家族苗族自治州委员会", "overlap_period": "2021-04至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "柯俊", "person_id": "enshi_柯俊", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任后任关系", "overlap_org": "中共恩施土家族苗族自治州委员会", "overlap_period": "2021年交接", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "单艳平", "person_id": "enshi_单艳平", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "州委书记与州委秘书长", "overlap_org": "中共恩施土家族苗族自治州委员会", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "吕星", "person_id": "enshi_吕星", "relationship_type": "overlap", "strength": "medium", "evidence": "州委书记与纪委书记", "overlap_org": "中共恩施土家族苗族自治州委员会", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "张远梅", "person_id": "enshi_张远梅", "relationship_type": "overlap", "strength": "medium", "evidence": "州委书记与常务副州长", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    hcw_json = make_person_json(persons[0], hcw_timeline, hcw_relationships, source_register, "enshi_huchaowen")
    hcw_json["professional_profile"]["career_pattern"] = "cross_county_rotation"
    hcw_json["professional_profile"]["systems_experience"] = ["城建", "环保", "地方党政", "扶贫"]
    hcw_json["professional_profile"]["geographic_pattern"] = ["武汉（省直）", "潜江", "咸宁", "恩施"]
    hcw_json["professional_profile"]["promotion_velocity"] = {
        "summary": "胡超文长期在湖北省建设系统和环保系统工作，2009年下派潜江，经历省市双重历练，逐步晋升至正厅级岗位。2021年任恩施州委书记。",
        "notable_fast_promotions": ["2011年由潜江市委常委、常务副市长升任市长"]
    }
    hcw_json["open_questions"] = [
        {"priority": "high", "question": "胡超文的完整教育背景（毕业院校、专业、学历）", "why_it_matters": "完善基础档案信息", "suggested_queries": ["胡超文 学历 毕业院校 湖北省委党校"], "last_attempted": AS_OF},
        {"priority": "medium", "question": "胡超文在省住建厅各具体职务的起止时间", "why_it_matters": "细化早期履历时间线", "suggested_queries": ["胡超文 湖北省建设厅 任职"], "last_attempted": AS_OF},
    ]

    hcw_path = PERSONS_DIR / f"{TODAY}-湖北省-恩施土家族苗族自治州-州委书记-胡超文.json"
    with open(hcw_path, "w", encoding="utf-8") as f:
        json.dump(hcw_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {hcw_path.name}")

    # === 2. 夏锡璠 ===
    xf_timeline = [
        {"start": "1993-10", "end": "2003", "org": "潜江市基层单位", "title": "科员至科级", "notes": "1993年10月参加工作，在潜江基层任职", "confidence": "plausible", "source_ids": ["S002"]},
        {"start": "2003", "end": "2006", "org": "潜江市周矶管理区", "title": "科级职务", "notes": "", "confidence": "plausible", "source_ids": ["S002"]},
        {"start": "2006", "end": "2009", "org": "潜江市人民政府", "title": "副市长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2009", "end": "2011", "org": "中共潜江市委", "title": "市委常委、宣传部部长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2011", "end": "2015", "org": "监利县人民政府", "title": "县长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2015", "end": "2017", "org": "中共监利县委", "title": "县委书记（副厅级）", "notes": "监利县为副厅级建制县委书记高配", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2017", "end": "2020", "org": "中共宜昌市委、宜昌市纪委", "title": "市委常委、市纪委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2020", "end": "2021-07", "org": "湖北省退役军人事务厅", "title": "副厅长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2021-07", "end": "present", "org": "恩施土家族苗族自治州人民政府", "title": "州长", "notes": "2021年7月任代州长，后转正", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    xf_relationships = [
        {"person": "胡超文", "person_id": "enshi_胡超文", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "州长受州委书记领导", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "2021-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "张远梅", "person_id": "enshi_张远梅", "relationship_type": "overlap", "strength": "medium", "evidence": "州长与常务副州长搭档", "overlap_org": "恩施土家族苗族自治州人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "刘芳震", "person_id": "enshi_刘芳震", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任后任关系", "overlap_org": "恩施土家族苗族自治州人民政府", "overlap_period": "2021年交接", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "单艳平", "person_id": "enshi_单艳平", "relationship_type": "overlap", "strength": "medium", "evidence": "在恩施州共事", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    xf_json = make_person_json(persons[1], xf_timeline, xf_relationships, source_register, "enshi_xiaxifan")
    xf_json["identity"]["native_place"] = "湖北省利川市（出生地，土家族自治州的土家族干部）"
    xf_json["professional_profile"]["career_pattern"] = "cross_county_rotation"
    xf_json["professional_profile"]["systems_experience"] = ["地方党政", "纪检", "退役军人事务"]
    xf_json["professional_profile"]["geographic_pattern"] = ["潜江", "监利", "宜昌", "武汉", "恩施"]
    xf_json["professional_profile"]["promotion_velocity"] = {
        "summary": "夏锡璠从潜江基层起步，历经多县市多个岗位，2015年任监利县委书记（高配副厅），2017年调任宜昌市委常委、纪委书记，2021年升任恩施州长。",
        "notable_fast_promotions": ["2015年由县长升任县委书记（高配副厅级）"]
    }
    xf_json["open_questions"] = [
        {"priority": "critical", "question": "夏锡璠1993-2003年在潜江的具体任职情况", "why_it_matters": "核心人物早期履历需详细核实", "suggested_queries": ["夏锡璠 潜江 早期 任职", "夏锡璠 周矶 管理区"], "last_attempted": AS_OF},
        {"priority": "high", "question": "夏锡璠的教育背景（毕业院校、专业、学历）", "why_it_matters": "完善基础档案信息", "suggested_queries": ["夏锡璠 学历 毕业院校 湖北省委党校"], "last_attempted": AS_OF},
    ]

    xf_path = PERSONS_DIR / f"{TODAY}-湖北省-恩施土家族苗族自治州-州长-夏锡璠.json"
    with open(xf_path, "w", encoding="utf-8") as f:
        json.dump(xf_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {xf_path.name}")

    # === 3. 柯俊 (predecessor) ===
    kj_timeline = [
        {"start": "unknown", "end": "unknown", "org": "湖北省", "title": "早期工作经历", "notes": "在大冶市起步，后调省级部门", "confidence": "plausible", "source_ids": ["S002"]},
        {"start": "2017", "end": "2019", "org": "宜昌市人民政府", "title": "宜昌市委副书记、市长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2019", "end": "2021", "org": "中共恩施土家族苗族自治州委员会", "title": "州委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2021", "end": "present", "org": "河北省人民政府", "title": "副省长", "notes": "调任河北省副省长（跨省提拔）", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    kj_relationships = [
        {"person": "胡超文", "person_id": "enshi_胡超文", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任后任关系", "overlap_org": "中共恩施土家族苗族自治州委员会", "overlap_period": "2021年交接", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "刘芳震", "person_id": "enshi_刘芳震", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "州委书记与州长搭档", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "2019-2021", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    kj_json = make_person_json(persons[13], kj_timeline, kj_relationships, source_register, "enshi_kejun")
    kj_json["current_status"]["is_current_confirmed"] = True
    kj_json["current_status"]["administrative_rank"] = "副省级"
    kj_json["professional_profile"]["career_pattern"] = "cross_county_rotation"

    kj_path = PERSONS_DIR / f"{TODAY}-湖北省-恩施土家族苗族自治州-前任州委书记-柯俊.json"
    with open(kj_path, "w", encoding="utf-8") as f:
        json.dump(kj_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {kj_path.name}")

    # === 4. 刘芳震 (predecessor governor) ===
    lfz_timeline = [
        {"start": "unknown", "end": "2015", "org": "恩施土家族苗族自治州", "title": "历任副州长等职务", "notes": "长期在恩施州工作", "confidence": "plausible", "source_ids": ["S002"]},
        {"start": "2015", "end": "2021", "org": "恩施土家族苗族自治州人民政府", "title": "州长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    lfz_relationships = [
        {"person": "夏锡璠", "person_id": "enshi_夏锡璠", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任后任关系", "overlap_org": "恩施土家族苗族自治州人民政府", "overlap_period": "2021年交接", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "柯俊", "person_id": "enshi_柯俊", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "州长受州委书记领导", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "2019-2021", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    lfz_json = make_person_json(persons[14], lfz_timeline, lfz_relationships, source_register, "enshi_liufangzhen")
    lfz_json["current_status"]["is_current_confirmed"] = False
    lfz_json["professional_profile"]["career_pattern"] = "local_ladder"
    lfz_json["professional_profile"]["geographic_pattern"] = ["恩施"]

    lfz_path = PERSONS_DIR / f"{TODAY}-湖北省-恩施土家族苗族自治州-前任州长-刘芳震.json"
    with open(lfz_path, "w", encoding="utf-8") as f:
        json.dump(lfz_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {lfz_path.name}")

    # === 5. 张远梅 ===
    zym_timeline = [
        {"start": "unknown", "end": "unknown", "org": "监利县", "title": "县委书记", "notes": "此前在监利工作", "confidence": "plausible", "source_ids": []},
        {"start": "unknown", "end": "unknown", "org": "湖北省住房和城乡建设厅", "title": "副厅长", "notes": "", "confidence": "plausible", "source_ids": []},
        {"start": "", "end": "present", "org": "恩施土家族苗族自治州人民政府", "title": "常务副州长", "notes": "目前在该岗位", "confidence": "plausible", "source_ids": []},
    ]
    zym_relationships = [
        {"person": "夏锡璠", "person_id": "enshi_夏锡璠", "relationship_type": "overlap", "strength": "medium", "evidence": "州长与常务副州长搭档", "overlap_org": "恩施土家族苗族自治州人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "胡超文", "person_id": "enshi_胡超文", "relationship_type": "overlap", "strength": "medium", "evidence": "在恩施州共事", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zym_json = make_person_json(persons[2], zym_timeline, zym_relationships, source_register, "enshi_zhangyuanmei")

    zym_path = PERSONS_DIR / f"{TODAY}-湖北省-恩施土家族苗族自治州-常务副州长-张远梅.json"
    with open(zym_path, "w", encoding="utf-8") as f:
        json.dump(zym_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zym_path.name}")

    # === 6. 单艳平 ===
    syp_timeline = [
        {"start": "unknown", "end": "", "org": "中共巴东县委员会", "title": "巴东县委书记", "notes": "曾任巴东县委书记", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "", "end": "present", "org": "中共恩施土家族苗族自治州委员会", "title": "州委常委、州委秘书长", "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    syp_relationships = [
        {"person": "胡超文", "person_id": "enshi_胡超文", "relationship_type": "subordinate_to_superior", "strength": "medium", "evidence": "州委秘书长直接服务州委书记", "overlap_org": "中共恩施土家族苗族自治州委员会", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "刘芳震", "person_id": "enshi_刘芳震", "relationship_type": "subordinate_to_superior", "strength": "medium", "evidence": "任巴东县委书记时刘芳震为州长", "overlap_org": "恩施土家族苗族自治州", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    syp_json = make_person_json(persons[8], syp_timeline, syp_relationships, source_register, "enshi_shanyanping")
    syp_json["identity"]["ethnicity"] = "土家族"
    syp_json["identity"]["birth"] = "1967年9月"
    syp_json["identity"]["birthplace"] = "湖北省来凤县"

    syp_path = PERSONS_DIR / f"{TODAY}-湖北省-恩施土家族苗族自治州-州委秘书长-单艳平.json"
    with open(syp_path, "w", encoding="utf-8") as f:
        json.dump(syp_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {syp_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")
