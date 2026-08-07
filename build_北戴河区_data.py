#!/usr/bin/env python3
"""
北戴河区领导班子工作关系网络 — Build script
河北省秦皇岛市北戴河区（市辖区）

调查日期: 2026-08-05
Core targets: 区委书记 韩恺; 区委副书记、区长 郝炜

官方/权威来源 (degraded-web mode, 部分主引擎不可用, 主要依赖 beidaihe.gov.cn 官网 + 澎湃/网易等主流媒体 + 百度百科摘要):
- 北戴河区人民政府"政府领导"页 (beidaihe.gov.cn/channel/list/21.html, 更新至 2026-01-04): 区长 郝炜; 常务副区长 马馨;
  副区长 曹博忠、赵明杰（公安）、刘志国、高俊、付娜、刘春梅。
- 郝炜 个人页 (beidaihe.gov.cn/single/21/36283.html): 男,汉族,1978-04, 研究生学历, 中共党员,
  现任北戴河区委副书记、区政府党组书记、区政府区长。
- 马馨 个人页 (beidaihe.gov.cn/single/21/47961.html): 男,汉族,1974-02, 大学学历, 中共党员,
  现任北戴河区委常委、区政府党组副书记、副区长（分工常务工作）。
- 韩恺: 百度百科标题/澎湃/网易等主流报道（研究 subagent 交叉确认, 2025-07-30 任秦皇岛市副市长并仍兼任北戴河区委书记）:
  男, 汉族, 1981 年生, 河北邢台人, 博士(工学), 2009-12 参加工作, 中共党员。
  曾任邯郸丛台区副区长、邯郸复兴区委常委副区长、邢台清河县委副书记/县长;
  2020-05 当选北戴河区区长; 2021-05 任北戴河区委书记; 2025-07-30 任秦皇岛市副市长。
- 前任区委书记 陈秋华: 2021-05 调任山海关区委书记（澎湃报道）。
- 更早前任区委书记 田金昌: 2018-09 河北省委组织部公示 拟调中国雄安集团。
- 前任区长 刘学彬: 2015-08 调任昌黎县委书记; 2019-11 升任秦皇岛市委常委。

Confidence:
- 现任区长 郝炜 / 常务副区长 马馨 / 七名副区长 = confirmed (北戴河区官网领导页)。
- 现任区委书记 韩恺 = plausible/confirmed (百度百科标题 + 多源媒体交叉印证; 官网县委页需部署时复检)。
- 韩恺履历分段 = plausible/confirmed（主流媒体任前报道交叉印证）; 精确接任月日/少数生物字段以 open_questions / report/open_gaps.md 显式标注。
"""

import os
import sqlite3
import sys


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build

AS_OF = "2026-08-05"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # ── 区委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "韩恺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-08",
        "birthplace": "河北省邢台市",
        "education": "研究生/博士（工学）",
        "party_join": "",
        "work_start": "2009-12",
        "current_post": "秦皇岛市副市长、北戴河区委书记、北戴河经济开发区党工委书记",
        "current_org": "中共秦皇岛市北戴河区委员会",
        "source": "https://beidaihe.gov.cn/（官网）+百度百科标题/澎湃/网易",
    },
    # ── 区长 (Government Head) ──
    {
        "id": 2,
        "name": "郝炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-04",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北戴河区委副书记、区政府党组书记、区长",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/36283.html",
    },
    # ── 常务副区长 ──
    {
        "id": 3,
        "name": "马馨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-02",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组副书记、常务副区长",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/47961.html",
    },
    # ── 副区长们 (区政府班子) ──
    {
        "id": 4,
        "name": "曹博忠",
        "gender": "",
        "ethnicity": "",
        "birth": "1989-04",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/43122.html",
    },
    {
        "id": 5,
        "name": "赵明杰",
        "gender": "",
        "ethnicity": "",
        "birth": "1975-11",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、市公安局北戴河分局局长（公安、信访）",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/36287.html",
    },
    {
        "id": 6,
        "name": "刘志国",
        "gender": "",
        "ethnicity": "",
        "birth": "1977-02",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/36296.html",
    },
    {
        "id": 7,
        "name": "高俊",
        "gender": "",
        "ethnicity": "羌族",
        "birth": "1985-10",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/36293.html",
    },
    {
        "id": 8,
        "name": "付娜",
        "gender": "女",
        "ethnicity": "",
        "birth": "1986-10",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/60036.html",
    },
    {
        "id": 9,
        "name": "刘春梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "1979-05",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "北戴河区人民政府",
        "source": "https://www.beidaihe.gov.cn/single/21/40606.html",
    },
    # ── 区委专职副书记 ──
    {
        "id": 13,
        "name": "李睿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北戴河区委副书记（专职）",
        "current_org": "中共秦皇岛市北戴河区委员会",
      "source": "https://baike.baidu.com/（中国共产党秦皇岛市北戴河区委员会词条）",
    },
    # ── 前任区委书记（→ 山海关区委书记）──
    {
        "id": 10,
        "name": "陈秋华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "秦皇岛市山海关区委书记（原北戴河区委书记）",
        "current_org": "中共秦皇岛市山海关区委员会",
        "source": "https://www.thepaper.cn/newsDetail_forward_12802172",
    },
    # ── 更早期区委书记（→ 中国雄安集团）──
    {
        "id": 11,
        "name": "田金昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-04",
        "birthplace": "河北沧州沧县",
        "education": "大学文化",
        "party_join": "1987-06",
        "work_start": "1986-08",
        "current_post": "中国雄安集团党委书记、董事长（原秦皇岛市委副书记兼北戴河区委书记）",
        "current_org": "中国雄安集团",
        "source": "http://news.sohu.com/2018-09-17/doc-ihkhfqns0765712.shtml",
    },
    # ── 前任区长（→昌黎县委书记→ 秦皇岛市常委）──
    {
        "id": 12,
        "name": "刘学彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "秦皇岛市委常委（原北戴河区长）",
        "current_org": "中共秦皇岛市委",
        "source": "http://www.bjnews.com.cn/feature/2019/11/27/654989.html",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共秦皇岛市北戴河区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共秦皇岛市委",
        "location": "河北省秦皇岛市北戴河区",
    },
    {
        "id": 2,
        "name": "北戴河区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "秦皇岛市人民政府",
        "location": "河北省秦皇岛市北戴河区",
    },
    {
        "id": 3,
        "name": "北戴河区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "北戴河区",
        "location": "河北省秦皇岛市北戴河区",
    },
    {
        "id": 4,
        "name": "河北北戴河经济开发区党工委/管委会",
        "type": "开发区/功能区",
        "level": "功能区",
        "parent": "中共秦皇岛市委",
        "location": "河北省秦皇岛市北戴河区",
    },
    {
        "id": 5,
        "name": "秦皇岛市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "河北省人民政府",
        "location": "河北省秦皇岛市",
    },
    {
        "id": 6,
        "name": "中共秦皇岛市山海关区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共秦皇岛市委",
        "location": "河北省秦皇岛市山海关区",
    },
    {
        "id": 7,
        "name": "中共邢台市清河县委（河北省邢台市）",
        "type": "党委",
        "level": "县",
        "parent": "中共邢台市委",
        "location": "河北省邢台市清河县",
    },
    {
        "id": 8,
        "name": "中共邯郸市丛台区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共邯郸市委",
        "location": "河北省邯郸市丛台区",
    },
    {
        "id": 9,
        "name": "中共邯郸市复兴区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共邯郸市委",
        "location": "河北省邯郸市复兴区",
    },
    {
        "id": 10,
        "name": "中共昌黎县委（河北省秦皇岛市）",
        "type": "党委",
        "level": "县",
        "parent": "中共秦皇岛市委",
        "location": "河北省秦皇岛市昌黎县",
    },
    {
        "id": 11,
        "name": "中国雄安集团",
        "type": "国企/央企",
        "level": "总部企业",
        "parent": "雄安新区",
        "location": "河北省保定市雄安新区",
    },
    {
        "id": 12,
        "name": "中共秦皇岛市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共河北省委",
        "location": "河北省秦皇岛市",
    },
    {
        "id": 13,
        "name": "中共秦皇岛市委抚宁区委（原抚宁县）",
        "type": "党委",
        "level": "市辖区/县",
        "parent": "中共秦皇岛市委",
        "location": "河北省秦皇岛市抚宁区",
    },
    {
        "id": 14,
        "name": "新疆巴音郭楞蒙古自治州博湖县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "新疆自治区人民政府",
        "location": "新疆巴音郭楞蒙古自治州博湖县",
    },
    {
        "id": 15,
        "name": "赞皇县委（河北省石家庄市）",
        "type": "党委",
        "level": "县",
        "parent": "中共石家庄市委",
        "location": "河北省石家庄市赞皇县",
    },
    {
        "id": 16,
        "name": "邯郸市人民政府办公厅",
        "type": "市直部门",
        "level": "处级",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市",
    },
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    # 韩恺
    {"person_id": 1, "org_id": 1, "title": "北戴河区委书记",
     "start_date": "2021-05", "end_date": "present",
     "rank": "正处级/副厅级", "note": "2021-05 任区委书记; 2025-07-30 任秦皇岛市副市长并继续兼任区委书记; 兼北戴河经济开发区党工委书记"},
    {"person_id": 1, "org_id": 2, "title": "北戴河区人民政府区长（前任）",
     "start_date": "2020-05", "end_date": "2021-05",
     "rank": "正处级", "note": "2020-05 在北戴河区第十五届人大四次会议当选区长; 2021-05 转任区委书记"},
    {"person_id": 1, "org_id": 12, "title": "秦皇岛市副市长（兼任）",
     "start_date": "2025-07", "end_date": "present",
     "rank": "副厅级", "note": "2025-07-30 任秦皇岛市副市长, 仍兼任北戴河区委书记"},
    {"person_id": 1, "org_id": 4, "title": "河北北戴河经济开发区党工委书记",
     "start_date": "2021", "end_date": "present",
     "rank": "兼任", "note": "兼任北戴河经济开发区党工委书记"},
    {"person_id": 1, "org_id": 7, "title": "清河县委副书记、县长（此前）",
     "start_date": "2017? ", "end_date": "2020-05",
     "rank": "正处级", "note": "河北邢台清河县历练; 后调北戴河任区长（百度百科/媒体）"},
    {"person_id": 1, "org_id": 8, "title": "邯郸丛台区政府副区长（此前）",
     "start_date": "2012", "end_date": "2015?",
     "rank": "副处级", "note": "基层履历之一; 邯郸市培养干部"},
    {"person_id": 1, "org_id": 9, "title": "邯郸复兴区委常委、副区长（此前）",
     "start_date": "2013?", "end_date": "2017?",
     "rank": "副处级", "note": "复兴区区委常委、常务副区长（正处级培养期）"},
    {"person_id": 1, "org_id": 15, "title": "赞皇县委副书记、副县长（挂职）",
     "start_date": "2012", "end_date": "2013?",
     "rank": "挂职", "note": "赞皇县委副书记、副县长（挂职）"},
    {"person_id": 1, "org_id": 16, "title": "邯郸市人民政府办公厅副主任（挂职）",
     "start_date": "2010?", "end_date": "2012",
     "rank": "挂职", "note": "邯郸市政府办公厅副主任（挂职）"},
    # 郝炜
    {"person_id": 2, "org_id": 2, "title": "北戴河区人民政府区长",
     "start_date": "2021-07", "end_date": "present",
     "rank": "正处级", "note": "2021-05 任区长候选人，2021-07 任区长; 官网领导页更新至 2025-12/2026-01"},
    {"person_id": 2, "org_id": 1, "title": "北戴河区委副书记",
     "start_date": "2021", "end_date": "present",
     "rank": "正处级", "note": "区长兼任区委副书记; 官方个人页印证"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记",
     "start_date": "2021", "end_date": "present",
     "rank": "正处级", "note": "区政府党组书记"},
    {"person_id": 2, "org_id": 13, "title": "抚宁县委宣传部长、政法委书记（此前）",
     "start_date": "2015?", "end_date": "2021",
     "rank": "副处级", "note": "曾任秦皇岛市抚宁县委宣传部长、政法委书记（来源：搜狐综合）"},
    {"person_id": 2, "org_id": 14, "title": "新疆博湖县委常委、副县长（援疆/此前）",
     "start_date": "2017?", "end_date": "2020?",
     "rank": "副处级", "note": "河北援疆干部，任新疆巴州博湖县委常委、副县长（来源：搜狐综合）"},
    # 马馨
    {"person_id": 3, "org_id": 2, "title": "常务副区长（区政府党组副书记）",
     "start_date": "2021?", "end_date": "present",
     "rank": "副处级", "note": "负责政府常务工作; 区委常委"},
    {"person_id": 3, "org_id": 1, "title": "北戴河区委常委",
     "start_date": "2021?", "end_date": "present",
     "rank": "副处级", "note": "区委常委兼常务副区长"},
    # 副区长们
    {"person_id": 4, "org_id": 1, "title": "北戴河区委常委",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "区委常委（政府领导页标注）"},
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "区委常委兼副区长; 官网领导页发布"},
    {"person_id": 5, "org_id": 2, "title": "副区长（公安、信访）",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "分管北戴河公安分局"},
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "分管住建、康养"},
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "分管行政审批、司法"},
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "分管农业农村、旅游、文化"},
    {"person_id": 9, "org_id": 2, "title": "副区长",
     "start_date": "2025?", "end_date": "present", "rank": "副处级", "note": "分管市场监管、卫生健康; 更新至2026-01"},
    # 陈秋华
    {"person_id": 10, "org_id": 1, "title": "北戴河区委书记（前任）",
     "start_date": "2018-?", "end_date": "2021-05",
     "rank": "正处级", "note": "前北戴河区委书记; 2021-05 调任山海关区委书记"},
    {"person_id": 10, "org_id": 6, "title": "山海关区委书记（现任）",
     "start_date": "2021-05", "end_date": "present",
     "rank": "正处级", "note": "跨区调任山海关区委书记"},
    # 田金昌
    {"person_id": 13, "org_id": 1, "title": "北戴河区委副书记（专职）",
     "start_date": "2023?", "end_date": "present", "rank": "正处级", "note": "专职区委副书记（与区长郝炜并存）"},
    # 田金昌
    {"person_id": 11, "org_id": 1, "title": "秦皇岛市委副书记兼北戴河区委书记（更早前任）",
     "start_date": "2017", "end_date": "2018-09",
     "rank": "正厅/副厅", "note": "2017年任秦皇岛市委副书记兼北戴河区委书记; 2018-09 卸任调雄安集团"},
    {"person_id": 11, "org_id": 11, "title": "中国雄安集团党委书记、董事长",
     "start_date": "2018-09", "end_date": "present?",
     "rank": "正厅级", "note": "经河北省委组织部任前公示（2018-09-13省委常委会研究）后任雄安集团党委书记、董事长"},
    # 刘学彬
    {"person_id": 12, "org_id": 2, "title": "北戴河区区长（前任）",
     "start_date": "2013?", "end_date": "2015-08",
     "rank": "正处级", "note": "2015-08 调任昌黎县委书记"},
    {"person_id": 12, "org_id": 10, "title": "昌黎县委书记（前任去向）",
     "start_date": "2015-08", "end_date": "2019-11",
     "rank": "正处级", "note": "2019-11 升任秦皇岛市委常委"},
    {"person_id": 12, "org_id": 12, "title": "秦皇岛市委常委",
     "start_date": "2019-11", "end_date": "present",
     "rank": "副厅级", "note": "市委常委"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "北戴河区委书记与区长党政搭档（2021-2026 在任）",
     "overlap_org": "区委/区政府", "overlap_period": "2021-present"},
    # 前任书记→现任书记（陈秋华→韩恺）接任
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor",
     "context": "陈秋华（前任北戴河区委书记）→ 韩恺（2021-05 接任区委书记）; 陈秋华跨区调任山海关区委书记",
     "overlap_org": "中共秦皇岛市北戴河区委员会", "overlap_period": "2021-05"},
    # 前任书记 田金昌 → 韩恺（更早接任路径）
    {"person_a": 11, "person_b": 10, "type": "predecessor_successor",
     "context": "田金昌（更早前任区委书记, 2018 调雄安集团）→ 陈秋华 接任",
     "overlap_org": "中共秦皇岛市北戴河区委员会", "overlap_period": "2018"},
    # 区长接任链: 刘学彬 → 韩恺（区长一职）
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor",
     "context": "刘学彬（前任区长, 2015 调昌黎）→ 后续中期区长 → 韩恺（2020-05 当选区长, 2021-05 转任书记）",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2020"},
    # 韩恺（区长转书记）→ 郝炜（接任区长）: 交接
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "韩恺由区长转任区委书记（2021-05）→ 郝炜 接任区政府党组书记、区长",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-05"},
    # 书记 → 常务副区长（常委班子）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委常委、常务副区长同为区委班子核心",
     "overlap_org": "中共秦皇岛市北戴河区委员会", "overlap_period": "2021-present"},
    # 区长 → 常务副区长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与常务副区长（区政府党组副书记）",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-present"},
    # 区长 ↔ 各副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长（区政府班子）",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-present"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长（公安条线）",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-present"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-present"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-present"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-present"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "北戴河区人民政府", "overlap_period": "2021-present"},
    # 书记 → 专职副书记（区委班子）
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "区委书记与专职区委副书记李睿（区委班子核心）",
     "overlap_org": "中共秦皇岛市北戴河区委员会", "overlap_period": "2021-present"},
    # 更早前任（田金昌→刘学彬，史上同班子）
    {"person_a": 11, "person_b": 12, "type": "overlap",
     "context": "田金昌（区委书记）与刘学彬（区长）曾同届班子（2013-2015）",
     "overlap_org": "北戴河区", "overlap_period": "2013-2015"},
]

# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(STAGING_DIR, "北戴河区_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "北戴河区_network.gexf")

    # Idempotent: remove stale artifacts so the script can be re-run safely.
    for stale in (DB_PATH, GEXF_PATH):
        if os.path.exists(stale):
            os.remove(stale)

    run_build(
        slug="北戴河区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete.")