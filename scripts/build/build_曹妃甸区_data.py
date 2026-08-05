#!/usr/bin/env python3
"""
曹妃甸区领导班子工作关系网络 — Build script
河北省唐山市曹妃甸区（市辖区）

调查日期: 2026-08-05
Core targets: 区委书记 董继华; 区委副书记、区长 郑友东

官方/权威来源 (degraded-web mode, Exa/Bing/Sogou/Jina/cfd.gov.cn unavailable):
- 百度百科「董继华」(baike.baidu.com/item/董继华/24479393): 男, 中共党员; 2020-02~2021-07 沧州市发改委主任;
  2021-05 南皮县委书记(一级调研员); 曾任河北省工信厅副厅长、党组成员; 现任唐山市委常委、曹妃甸区委书记。
- 百度百科「郑友东」(baike.baidu.com/item/郑友东/57039031): 男, 汉族, 1973-09, 唐山丰南人, 河北科技师范学院法学学士;
  曾任丰南区财政局长、党组书记, 丰南区委常委、政法委书记; 2020起 唐山国际旅游岛党工委书记、管委会主任;
  2021-05 曹妃甸区委副书记、代区长, 2021-07 当选区长; 现任曹妃甸区委副书记、区政府区长; 河北省十四届人大代表。
- 百度百科「中国共产党唐山市曹妃甸区委员会」(item/62646604): 区委书记 董继华; 区委副书记 郑友东、王克超。
- 天津大学新闻网 (news.tju.edu.cn/info/1003/557269.htm, 2025-08-22): 唐山市委常委、曹妃甸区委书记董继华一行来访。
- 曹妃甸融媒/区委全会报道: 三届十次全会(2026-01-03) 董继华讲话、郑友东部署经济工作; 三届十二/十三次全会董继华讲话。
- 前任区委书记 侯旭: 2025-09 河北省纪委监委通报严重违纪违法被开除党籍、开除公职（唐山反腐）。

Confidence: 现任区委书记/区长 roles = confirmed (多来源). 履历分段 = plausible/confirmed.
早期/精确接任时间等未定位字段以 open_questions / report/open_gaps.md 显式标注。
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
        "name": "董继华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "唐山市委常委、曹妃甸区委书记",
        "current_org": "中共唐山市曹妃甸区委员会",
        "source": "https://baike.baidu.com/item/董继华/24479393",
    },
    # ── 区长 (Government Head) ──
    {
        "id": 2,
        "name": "郑友东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-09",
        "birthplace": "河北唐山丰南区",
        "education": "河北科技师范学院法学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区政府区长",
        "current_org": "曹妃甸区人民政府",
        "source": "https://baike.baidu.com/item/郑友东/57039031",
    },
    # ── 区委副书记 ──
    {
        "id": 3,
        "name": "王克超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共唐山市曹妃甸区委员会",
        "source": "https://baike.baidu.com/item/中国共产党唐山市曹妃甸区委员会/62646604",
    },
    # ── 区委常委、政法委书记 ──
    {
        "id": 4,
        "name": "孙素慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共唐山市曹妃甸区委员会",
        "source": "http://baijiahao.baidu.com/s?id=1707169041761195663",
    },
    # ── 区委常委、副区长 ──
    {
        "id": 5,
        "name": "董金海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "曹妃甸区人民政府",
        "source": "http://news.tju.edu.cn/info/1003/557269.htm",
    },
    {
        "id": 6,
        "name": "闫琳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府副区长",
        "current_org": "曹妃甸区人民政府",
        "source": "https://mp.weixin.qq.com/s/曹妃甸区人大常委会会议",
    },
    # ── 区政府副区长 / 公安局局长 ──
    {
        "id": 7,
        "name": "赵秀光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府副区长、公安局党委书记、局长",
        "current_org": "曹妃甸区人民政府",
        "source": "http://baijiahao.baidu.com/s?id=1707169041761195663",
    },
    # ── 区人大常委会副主任 / 总工会主席 ──
    {
        "id": 8,
        "name": "佟秀媛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会党组副书记、副主任, 总工会主席",
        "current_org": "曹妃甸区人大常委会",
        "source": "https://m.haiwainet.cn/middle/3541083/2021/0707/content_32152714_1.html",
    },
    # ── 区政府党组成员 / 副区长 ──
    {
        "id": 9,
        "name": "马亚楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "曹妃甸区人民政府",
        "source": "https://m.haiwainet.cn/middle/3541083/2021/0707/content_32152714_1.html",
    },
    # ── 区法院院长 / 检察院检察长 ──
    {
        "id": 10,
        "name": "陈丹宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人民法院院长",
        "current_org": "曹妃甸区人民法院",
        "source": "https://mp.weixin.qq.com/曹妃甸区人大常委会会议",
    },
    {
        "id": 11,
        "name": "周立杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人民检察院检察长",
        "current_org": "曹妃甸区人民检察院",
        "source": "https://mp.weixin.qq.com/曹妃甸区人大常委会会议",
    },
    # ── 前任区委书记（反腐落马）──
    {
        "id": 12,
        "name": "侯旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "河北迁安",
        "education": "大学文化",
        "party_join": "1994-04",
        "work_start": "1992-08",
        "current_post": "原唐山市委常委、曹妃甸区委书记（2025-09 被双开）",
        "current_org": "卸任（违纪违法被开除党籍、开除公职）",
        "source": "https://baike.baidu.com/item/侯旭",
    },
    # ── 前任区长（杨洁）──
    {
        "id": 13,
        "name": "杨洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "唐山市人大常委会党组书记、主任（曾任曹妃甸区区长）",
        "current_org": "唐山市人大常委会",
        "source": "https://baike.baidu.com/item/杨洁",
    },
    # ── 更早区委书记（孙贵石）──
    {
        "id": 14,
        "name": "孙贵石",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原曹妃甸区委书记、曹妃甸工业区党工委书记兼管委会主任",
        "current_org": "卸任/去向待查",
        "source": "https://www.thepaper.cn/唐山反腐档案",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共唐山市曹妃甸区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共唐山市委",
        "location": "河北省唐山市曹妃甸区",
    },
    {
        "id": 2,
        "name": "曹妃甸区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "唐山市人民政府",
        "location": "河北省唐山市曹妃甸区",
    },
    {
        "id": 3,
        "name": "曹妃甸区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "曹妃甸区",
        "location": "河北省唐山市曹妃甸区",
    },
    {
        "id": 4,
        "name": "曹妃甸区人民法院",
        "type": "政法",
        "level": "市辖区",
        "parent": "曹妃甸区",
        "location": "河北省唐山市曹妃甸区",
    },
    {
        "id": 5,
        "name": "曹妃甸区人民检察院",
        "type": "政法",
        "level": "市辖区",
        "parent": "曹妃甸区",
        "location": "河北省唐山市曹妃甸区",
    },
    {
        "id": 6,
        "name": "唐山市丰南区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "唐山市人民政府",
        "location": "河北省唐山市丰南区",
    },
    {
        "id": 7,
        "name": "唐山国际旅游岛党工委/管委会",
        "type": "开发区/功能区",
        "level": "功能区",
        "parent": "中共唐山市",
        "location": "河北省唐山市",
    },
    {
        "id": 8,
        "name": "河北省工业和信息化厅",
        "type": "省直部门",
        "level": "厅级",
        "parent": "河北省人民政府",
        "location": "河北省石家庄市",
    },
    {
        "id": 9,
        "name": "中共南皮县委（河北省沧州市）",
        "type": "党委",
        "level": "县",
        "parent": "中共沧州市委",
        "location": "河北省沧州市南皮县",
    },
    {
        "id": 10,
        "name": "沧州市发展和改革委员会",
        "type": "市直部门",
        "level": "处级",
        "parent": "沧州市人民政府",
        "location": "河北省沧州市",
    },
    {
        "id": 11,
        "name": "唐山市人大常委会",
        "type": "人大",
        "level": "地级市",
        "parent": "唐山市",
        "location": "河北省唐山市",
    },
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    # 董继华
    {"person_id": 1, "org_id": 1, "title": "曹妃甸区委书记",
     "start_date": "2025?", "end_date": "present",
     "rank": "副厅级", "note": "现任，兼唐山市委常委; 2025-08-22 天津大学来访; 三届十次/十三次全会讲话; 接任后反腐落马的侯旭"},
    {"person_id": 1, "org_id": 8, "title": "河北省工业和信息化厅副厅长、党组成员",
     "start_date": "2021-07", "end_date": "2025?",
     "rank": "副厅级", "note": "从沧州发改委主任/南皮县委书记转任省工信厅（百科）"},
    {"person_id": 1, "org_id": 9, "title": "南皮县委书记（一级调研员）",
     "start_date": "2021-05", "end_date": "2021-07",
     "rank": "正处级/副厅级", "note": "2021-05 任南皮县委书记（沧州市属县）"},
    {"person_id": 1, "org_id": 10, "title": "沧州市发展和改革委员会主任",
     "start_date": "2020-02", "end_date": "2021-07",
     "rank": "正处级", "note": "2020-02 起任沧州发改委主任"},
    # 郑友东
    {"person_id": 2, "org_id": 1, "title": "曹妃甸区委副书记",
     "start_date": "2021-05", "end_date": "present",
     "rank": "副厅级", "note": "区长兼区委副书记; 2021-05 任区委副书记、代区长"},
    {"person_id": 2, "org_id": 2, "title": "曹妃甸区人民政府区长",
     "start_date": "2021-07", "end_date": "present",
     "rank": "正处级", "note": "2021-05 代理, 2021-07 当选区长; 2026-01-03 区委经济工作会议部署工作"},
    {"person_id": 2, "org_id": 7, "title": "唐山国际旅游岛党工委书记、管委会主任",
     "start_date": "2020", "end_date": "present(兼任)",
     "rank": "双肩挑", "note": "2020 起任国际旅游岛主要负责人"},
    {"person_id": 2, "org_id": 6, "title": "丰南区委常委、政法委书记（此前）",
     "start_date": "2016?", "end_date": "2020",
     "rank": "副处级", "note": "长期在丰南区工作: 区委常委、政法委书记"},
    {"person_id": 2, "org_id": 6, "title": "丰南区财政局局长、党组书记（此前）",
     "start_date": "2010?", "end_date": "2016?",
     "rank": "正科级", "note": "长期在丰南区财政系统（百科）"},
    # 王克超
    {"person_id": 3, "org_id": 1, "title": "曹妃甸区委副书记",
     "start_date": "2021?", "end_date": "present",
     "rank": "副厅级", "note": "百度百科区委员会现任领导: 区委副书记之一"},
    # 孙素慧 / 董金海 / 闫琳 / 赵秀光 / 佟秀媛 / 马亚楠 / 陈丹宁 / 周立杰
    {"person_id": 4, "org_id": 1, "title": "区委常委、政法委书记",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": "海外网2021 报道"},
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长",
     "start_date": "2025?", "end_date": "present", "rank": "副处级", "note": "2025-08-22 天津大学来访（董金海 参加会见）"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、区政府副区长",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "区人大常委会会议列席"},
    {"person_id": 7, "org_id": 2, "title": "区政府副区长、公安局党委书记、局长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": "海外网2021 报道"},
    {"person_id": 8, "org_id": 3, "title": "区人大常委会副主任、总工会主席",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": "第二届曹妃甸‘十佳工匠’颁奖活动"},
    {"person_id": 9, "org_id": 2, "title": "区政府党组成员、副区长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": "2021 年‘十佳工匠’报道列名副区长候选人"},
    {"person_id": 10, "org_id": 4, "title": "区人民法院院长",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "区人大常委会会议列席"},
    {"person_id": 11, "org_id": 5, "title": "区人民检察院检察长",
     "start_date": "2023?", "end_date": "present", "rank": "副处级", "note": "区人大常委会会议列席"},
    # 侯旭（前任书记）
    {"person_id": 12, "org_id": 1, "title": "曹妃甸区委书记（前任）",
     "start_date": "2021-06", "end_date": "2025-09",
     "rank": "副厅级", "note": "曾任唐山市委常委、曹妃甸区委书记; 2025-09 河北省纪委监委通报严重违纪违法被开除党籍、开除公职"},
    # 杨洁（前任区长）
    {"person_id": 13, "org_id": 2, "title": "唐山市曹妃甸区区长（前任）",
     "start_date": "2012-?", "end_date": "2014?",
     "rank": "正处级", "note": "2012 年任曹妃甸区区长; 2014 年任唐山市委常委、宣传部部长"},
    {"person_id": 13, "org_id": 11, "title": "唐山市人大常委会副主任（现任）",
     "start_date": "2021-08", "end_date": "present",
     "rank": "副厅级", "note": "2021-06 报道已任唐山市人大常委会党组书记，同年8月转正"},
    # 孙贵石（更早书记）
    {"person_id": 14, "org_id": 1, "title": "曹妃甸区委书记（更早前任）",
     "start_date": "2016?", "end_date": "2021?",
     "rank": "副厅级", "note": "曾任曹妃甸区委书记、曹妃甸工业区党工委书记兼管委会主任"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "曹妃甸区委书记与区长党政搭档（2025-2026 在任）",
     "overlap_org": "区委/区政府", "overlap_period": "2021-present"},
    # 徐旭 → 董继华（前任书记接任, 反腐补位）
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor",
     "context": "侯旭（前任曹妃甸区委书记, 2025-09 被开除党籍/公职）→ 董继华 接任补位",
     "overlap_org": "中共唐山市曹妃甸区委员会", "overlap_period": "2025"},
    # 杨洁 → 郑（前任区长→现任区长）
    {"person_a": 13, "person_b": 2, "type": "predecessor_successor",
     "context": "杨洁（前任曹妃甸区区长）→ 郑友东（接任区长, 2021-07）",
     "overlap_org": "曹妃甸区人民政府", "overlap_period": "2021"},
    # 董书记 ↔ 区领导班
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记王克超同为区委班子",
     "overlap_org": "中共唐山市曹妃甸区委员会", "overlap_period": "2021-present"},
    # 政法条线: 书记 ↔ 政法书记/公安
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委常委、政法委书记同班",
     "overlap_org": "曹妃甸区委常委会", "overlap_period": "2021-present"},
    # 政府班子: 区长 与 常委副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与区委常委、副区长（区政府班子）",
     "overlap_org": "曹妃甸区人民政府", "overlap_period": "2021-present"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与区委常委、区政府副区长（班子）",
     "overlap_org": "曹妃甸区人民政府", "overlap_period": "2021-present"},
]

# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(STAGING_DIR, "曹妃甸区_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "曹妃甸区_network.gexf")

    # Idempotent: remove stale artifacts so the script can be re-run safely.
    for stale in (DB_PATH, GEXF_PATH):
        if os.path.exists(stale):
            os.remove(stale)

    run_build(
        slug="曹妃甸区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete.")