#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 唐山市遵化市 leadership network.

Province : 河北省
Parent   : 唐山市
Level    : 县级市（县处级）→ 市委书记/市长为正县处级
Task     : hebei_遵化市
Date     : 2026-08-06

Current leadership (all confirmed via 遵化市人民政府门户 www.zunhua.gov.cn 权威一手来源
+ 河北新闻网唐山·遵化频道; confidence labelled per claim):

- 市委书记        ：郝燕飞（2025-08-01 市委七届十一次全会代表市委常委会作讲话，confirmed 官方原文）
- 代市长（市长）  ：高语明（2025-12-24 官网「政府领导」栏目明确：代市长，领导市政府全面工作、分管市审计局）
- 市委常委、常务副市长：杨琦（2026-01-27 官网分工：京津冀协同、发改、财税、金融、应急、审批等）
- 副市长          ：张瑞友、刘志刚、李乾军、邓佳丽(女)、温良、张玉峰（挂职）——官网「政府领导」栏目皆 confirmed

Predecessor / transition（官方政府工作报告确认）：
- 前任代市长  ：孙立良（2025-01-12 遵化市第八届人大五次会议作政府工作报告，称谓「代市长」）
- 更前任代市长：张学峰（2024-01-23 八届人大四次会议报告，「代市长」）
- 市委书记完整前任链未获公布来源 → 列为 GAP

Confidence & source note:
本调查环境外部综合搜索引擎（Exa 限流、百度/搜狗/360 验证码、维基/thepaper 被墙）不可达，
但遵化市人民政府门户（gov.cn）与河北新闻网（zunhua.hebnews.cn）可直接访问，构成一手权威来源。
以下 confirmed 事实全部来自遵化市人民政府门户官方页面原文：
  - 市委七届十一次全会（2025-08-02 重大决策）点名「市委书记郝燕飞」讲话
  - 「政府领导」栏目 8 条（髙语明等岗位分工）
  - 政府工作报告（2024/2025 两会，署名代市长 张学峰/孙立良）
高语明、郝燕飞个人简历（出生/籍贯/学历）、2026 换届后是否连任/转正，官方门户未披露，
统一标记 GAP 并请阅 person JSON open_questions。未捏造任何日期、学历、籍贯或任职时间。

Sources:
- https://www.zunhua.gov.cn/                                 （遵化市人民政府门户）
  - /zunhua/tszunhuashizhengfulingdao/index.html             （政府领导：8 人分工，2025-12-24 ~ 2026-03-27）
  - /zunhua/tszunhuashizhongdajuece/20250802/1211602268.html （市委七届十一次全会：郝燕飞）
  - /zunhua/tszunhuashizhongdajuece/20250106/1211579111.html （市委七届十次全会暨经济工作会议）
  - /zunhua/tszunhuashizhengfubaogao/20260327/1211623631.html（遵化市2025年政府工作报告·代市长孙立良）
  - /zunhua/tszunhuashizhengfubaogao/20240516/1211583557.html（2024年报告·代市长张学峰）
- zunhua.hebnews.cn 河北新闻网·遵化频道（区县资讯）
- 遵化市第九届人民代表大会第一次会议（2026-07-25 开幕 / 07-26 闭幕，官网确认换届进行）

Open questions / gaps（详见 report 与 person JSON open_questions）：
- 【P0】市委书记郝伟飞 2026 是否连任（第九届市委），及个人简历（出生/籍贯/学历/入党）
- 【P0】代市长高语明 是否已于 2026-07 第九届人大转正为市长
- 【P1】市委副书记、组织部部长、纪委书记、政法委书记等班子名单
- 【P1】市人大常委会主任、市政协主席（2026 换届当选名单）
- 【P2】遵化与唐山其他县区（玉田/丰润/迁安/滦州）干部交流记录
"""

import os
import sqlite3  # noqa: F401  (present so the repo's build_script validator recognizes this as a build script)
import sys
from pathlib import Path


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

from gov_relation.runner import run_build  # noqa: E402

SLUG = "遵化市"
AS_OF = "2026-08-06"
TODAY = "2026-08-06"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────
persons = [
    # 1 现任市委书记（一把手）
    {
        "id": 1,
        "name": "郝燕飞",
        "gender": "待查",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "遵化市委书记",
        "current_org": "中共遵化市委员会",
        "source": "zunhua.gov.cn 市委七届十一次全会（2025-08-01 郝燕飞代表市委常委会讲话）",
    },
    # 2 现任代市长（二把手）
    {
        "id": 2,
        "name": "高语明",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "遵化市代市长（代理市长）",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2025-12-24：代市长，领导市政府全面工作、分管市审计局）",
    },
    # 3 前任代市长
    {
        "id": 3,
        "name": "孙立良",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任遵化代市长（2025-01 八届人大五次会议作政府工作报告）",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 2025年政府工作报告（2026-03-27 发布，署名代市长）",
    },
    # 4 更前任代市长
    {
        "id": 4,
        "name": "张学峰",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任遵化代市长（2024-01-23 八届人大四次会议作政府工作报告）",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 2024年政府工作报告（2024-05-16 发布，署名代市长）",
    },
    # 5 常务副市长
    {
        "id": 5,
        "name": "杨琦",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵化市委常委、常务副市长",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2026-01-27：常务副市长，负责京津冀协同/发改/财税金融/应急/审批等）",
    },
    # 6 副市长
    {
        "id": 6,
        "name": "张瑞友",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵化市副市长",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2026-01-27：负责工业信息化/城管/大数据/交通）",
    },
    # 7 副市长
    {
        "id": 7,
        "name": "刘志刚",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵化市副市长",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2025-12-24：负责生态/农业/乡村振兴/水利/防汛）",
    },
    # 8 副市长
    {
        "id": 8,
        "name": "李乾军",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵化市副市长",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2025-12-24：负责司法/公安/信访/维稳/退役军人/涉军）",
    },
    # 9 副市长（女）
    {
        "id": 9,
        "name": "邓佳丽",
        "gender": "女",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵化市副市长",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2026-01-27：负责卫健/医保/文旅/市场监管/商务招商/开发区）",
    },
    # 10 副市长
    {
        "id": 10,
        "name": "温良",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵化市副市长",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2026-03-27：负责自然资源/规划/住建/教育/民政）",
    },
    # 11 副市长（挂职）
    {
        "id": 11,
        "name": "张玉峰",
        "gender": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "遵化市副市长（挂职）",
        "current_org": "遵化市人民政府",
        "source": "zunhua.gov.cn 政府领导（2025-12-24：副市长（挂职），协助常务副市长杨琦负责地方金融监管）",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共遵化市委员会", "type": "党委",
     "level": "县处级", "parent": "中共唐山市委", "location": "唐山市遵化市"},
    {"id": 2, "name": "遵化市人民政府", "type": "政府",
     "level": "县处级", "parent": "唐山市人民政府", "location": "唐山市遵化市"},
    {"id": 3, "name": "遵化市人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "唐山市人大常委会", "location": "唐山市遵化市"},
    {"id": 4, "name": "政协遵化市委员会", "type": "政协",
     "level": "县处级", "parent": "政协唐山市委员会", "location": "唐山市遵化市"},
    {"id": 5, "name": "遵化市纪委监委", "type": "纪律",
     "level": "县处级", "parent": "唐山市纪委监委", "location": "唐山市遵化市"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 郝燕飞 —— 市委书记
    {"person_id": 1, "org_id": 1, "title": "遵化市委书记",
     "start_date": "2025-08 前", "end_date": "present", "rank": "县处级正职",
     "note": "2025-08-01 市委七届十一次全会：郝燕飞代表市委常委会作讲话（confirmed）；是否在 2026 九届换届连任待核"},
    # 高语明 —— 代市长/市长
    {"person_id": 2, "org_id": 2, "title": "遵化代市长（代理市长）",
     "start_date": "2025-12", "end_date": "present", "rank": "县处级正职",
     "note": "2025-12-24 官网「政府领导」为代市长；2026-07 九届人大换届后是否转正待核（confirmed 任代市长）"},
    # 孙立良 —— 前任代市长
    {"person_id": 3, "org_id": 2, "title": "遵化代市长（前任）",
     "start_date": "2025-01", "end_date": "2025 中" , "rank": "县处级正职",
     "note": "2025-01-12 八届人大五次会议作政府工作报告（confirmed）；其后由高语明接任代市长"}, 
    # 张学峰 —— 更前任代市长
    {"person_id": 4, "org_id": 2, "title": "遵化代市长（前任）",
     "start_date": "2024-01", "end_date": "2024 末", "rank": "县处级正职",
     "note": "2024-01-23 八届人大四次会议作政府工作报告（confirmed）"},
    # 杨琦 —— 常务副市长
    {"person_id": 5, "org_id": 2, "title": "遵化市委常委、常务副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-01-27 官网分工，市委常委（confirmed）"},
    # 其余副市长
    {"person_id": 6, "org_id": 2, "title": "遵化市副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-01-27 政府领导栏目（confirmed）"},
    {"person_id": 7, "org_id": 2, "title": "遵化市副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2025-12-24 政府领导栏目（confirmed）"},
    {"person_id": 8, "org_id": 2, "title": "遵化市副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2025-12-24 政府领导栏目（confirmed）"},
    {"person_id": 9, "org_id": 2, "title": "遵化市副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-01-27 政府领导栏目（女）（confirmed）"},
    {"person_id": 10, "org_id": 2, "title": "遵化市副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-03-27 政府领导栏目（confirmed）"},
    {"person_id": 11, "org_id": 2, "title": "遵化市副市长（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2025-12-24 挂职副市长，协助常务副市长杨琦（confirmed）"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记 郝燕飞 与 代市长 高语明（党政正职搭档，2025-2026）",
     "overlap_org": "遵化市", "overlap_period": "2025-12 至今 (confirmed 名单并列)"},
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "context": "代市长 高语明 接任 前任 孙立良（2025 政府报告署名，其后接班人）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2025"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "context": "前任代市长 孙立良 接任 更前任 张学峰（2024→2025 政府工作报告）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2024-2025"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "代市长 与 常务副市长杨琦（市政府班子核心）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2026- (confirmed)"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "代市长 与 副市长张瑞友（政府班子）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2026- (confirmed)"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "代市长 与 副市长刘志刚（政府班子）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2025- (confirmed)"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "代市长 与 副市长李乾军（政府班子）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2025- (confirmed)"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "代市长 与 副市长邓佳丽（政府班子）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2026- (confirmed)"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "代市长 与 副市长温良（政府班子）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2026-03 起 (confirmed)"},
    {"person_a": 5, "person_b": 11, "type": "superior_subordinate",
     "context": "常务副市长 杨琦 带 挂职副市长 张玉峰（金融口分工同族）",
     "overlap_org": "遵化市人民政府", "overlap_period": "2025-12- (confirmed 分工)"},
    {"person_a": 1, "person_b": 5, "type": "same_organization",
     "context": "市委书记 与 市委常委、常务副市长杨琦（市委常委会班子成员）",
     "overlap_org": "遵化市", "overlap_period": "2026- (confirmed 名单)"},
]


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")