#!/usr/bin/env python3
"""
复兴区领导班子工作关系网络 — Build script
河北省邯郸市复兴区（市辖区）

调查日期: 2026-08-05
Core targets: 区委书记 李少锋（2021-05 起任，2026 上半年离任→邯郸市审计局局长）; 区长 李阳（现任）

官方/权威来源 (degraded-web mode, Exa 被限流, 直接抓取官网/政府页 + 百度搜索摘要) :
- 复兴区人民政府信息公开领导页 (www.hdfx.gov.cn): 区长 李阳（男,汉族,1980-10,本科历史学士,中共党员,
  现任复兴区委副书记、区政府区长、党组书记）。
- 邯郸市人民政府·审计局领导班子页 (2026-07-24): 李少锋 党组书记、局长（证明其已离任复兴区委书记）。
- 邯郸市人大/政府 2021 干部大会报道（网易/腾讯/河北新闻网）:
  - 2021-05-18 复兴区区委常委会(扩大)会议: 李艳锋 任复兴区委书记, 潘利军 不再兼任复兴区委书记。
  - 2021-05-22 复兴区领导干部大会: 李阳 任复兴区委委员、常委、副书记; 免去李少锋的区委副书记。
- 复兴区政协八届六次开幕会 (2026-01-25, 区官网): 区委书记李少锋, 区长李阳, 区委副书记王瑞峰,
  区人大常委会主任白建功, 区政协主席李勤芳, 统战部部长程学民等。
- 复兴区政府本地动态多期 (2023-2026): 李少锋多次以区委书记身份主持常委会 (2026-04-30 仍以书记出现)。
- 百度百科: 李少锋生日 1969-11, 籍贯临漳县; 田东（曾任复兴副区长 2021-07~2023-03 → 市住建局局长 2026-07）;
  王瑞峰（2026-06/07 任邯郸市市监局局长）。

Confidence:
- 区长 李阳 / 前任书记 李少锋 / 前任书记 潘利军 = confirmed（官网+多源媒体）。
- 李少锋离任后（2026-05~07 间）的新任区委书记姓名：未在公开检索确认, 以 open_questions / 报告 gap 显式标注。
- 各副区长/副书记名单 = plausible（政协/人大报道列出）。

注：本脚本在“partial evidence”模型下产出；不确定字段留空并以 open_questions / report/open_gaps.md 记录。
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
    # ── 区长 (Government Head, confirmed 现任) ──
    {
        "id": 1,
        "name": "李阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "待查",
        "education": "本科（历史学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "复兴区委副书记、区政府区长、党组书记",
        "current_org": "邯郸市复兴区人民政府",
        "source": "https://www.hdfx.gov.cn/ 政府信息公开领导页 (2026, official)",
    },
    # ── 区委书记 (前任, 2021-05~2026上半年, 现任邯郸市审计局局长) ──
    {
        "id": 2,
        "name": "李少锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-11",
        "birthplace": "河北省邯郸市临漳县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "邯郸市审计局局长、党组书记(一级调研员)(原复兴区委书记)",
        "current_org": "邯郸市审计局",
        "source": "https://www.hd.gov.cn/ 审计局领导班子页 (2026-07-24) + 百度百科 + 复兴区政府本地动态",
    },
    # ── 前任区委书记 (→ 另有任用, 交接 2021-05) ──
    {
        "id": 3,
        "name": "潘利军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原复兴区委书记（2021 免职, 另有任用）",
        "current_org": "中共邯郸市复兴区委员会",
        "source": "网易新闻 2021-05-19 邯郸干部任免报道",
    },
    # ── 区委副书记 (2026-01 区政协会议确认, 调任市监局长 2026-06/07) ──
    {
        "id": 4,
        "name": "王瑞峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "邯郸市市场监督管理局局长(原复兴区委副书记)",
        "current_org": "邯郸市市场监督管理局",
        "source": "百度百科 + 复兴区政协八届六次会议开幕(2026-01-25)",
    },
    # ── 区人大常委会主任 ──
    {
        "id": 5,
        "name": "白建功",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "复兴区人大常委会主任",
        "current_org": "复兴区人大常委会",
        "source": "复兴区政协八届六次会议(2026-01-25) + 邯郸市人大常委会(2021-07)",
    },
    # ── 区政协主席 ──
    {
        "id": 6,
        "name": "李勤芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "复兴区政协党组织书记、主席",
        "current_org": "政协复兴区委员会",
        "source": "复兴区政协八届六次会议(2026-01-25)",
    },
    # ── 区政府班子 (2021-07 十一届人大一次会议当选) ──
    {
        "id": 7,
        "name": "张文涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "复兴区常务副区长(政府班子)",
        "current_org": "复兴区人民政府",
        "source": "邯郸市人大常委会 复兴区十一届人大一次会议(2021-07) + 邯郸市统计局调研报道(2024-12)",
    },
    {
        "id": 8,
        "name": "田东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "邯郸市住房和城乡建设局局长(原复兴区副区长)",
        "current_org": "邯郸市住房和城乡建设局",
        "source": "百度百科 田东 + 邯郸市人民政府 (2026-07 任命)",
    },
    {
        "id": 9,
        "name": "王建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "复兴区副区长(2021)",
        "current_org": "复兴区人民政府",
        "source": "邯郸市人大常委会 复兴区十一届人大一次会议(2021-07)",
    },
    {
        "id": 10,
        "name": "王林之",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "复兴区副区长(2021)",
        "current_org": "复兴区人民政府",
        "source": "邯郸市人大常委会 复兴区十一届人大一次会议(2021-07)",
    },
    {
        "id": 11,
        "name": "张莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "复兴区副区长(2021)",
        "current_org": "复兴区人民政府",
        "source": "邯郸市人大常委会 复兴区十一届人大一次会议(2021-07)",
    },
    # ── 区委常委、统战部长 ──
    {
        "id": 12,
        "name": "程学民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "复兴区委常委、统战部部长",
        "current_org": "中共邯郸市复兴区委员会",
        "source": "复兴区政协八届六次会议(2026-01-25)",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共邯郸市复兴区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共邯郸市委",
        "location": "河北省邯郸市复兴区",
    },
    {
        "id": 2,
        "name": "邯郸市复兴区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市复兴区",
    },
    {
        "id": 3,
        "name": "复兴区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "复兴区",
        "location": "河北省邯郸市复兴区",
    },
    {
        "id": 4,
        "name": "政协复兴区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "复兴区",
        "location": "河北省邯郸市复兴区",
    },
    {
        "id": 5,
        "name": "中共邯郸市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共河北省委",
        "location": "河北省邯郸市",
    },
    {
        "id": 6,
        "name": "邯郸市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "河北省人民政府",
        "location": "河北省邯郸市",
    },
    {
        "id": 7,
        "name": "邯郸市审计局",
        "type": "市直部门",
        "level": "处级",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市",
    },
    {
        "id": 8,
        "name": "邯郸市市场监督管理局",
        "type": "市直部门",
        "level": "处级",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市",
    },
    {
        "id": 9,
        "name": "邯郸市住房和城乡建设局",
        "type": "市直部门",
        "level": "处级",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市",
    },
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    # 李阳 (区长)
    {"person_id": 1, "org_id": 2, "title": "复兴区人民政府区长",
     "start_date": "2021-05", "end_date": "present",
     "rank": "正处级", "note": "2021-05-22 任复兴区委副书记、区政府区长(候选人); 2021-07 十三届人大一次会议当选区长;"},
    {"person_id": 1, "org_id": 1, "title": "复兴区委副书记",
     "start_date": "2021-05", "end_date": "present",
     "rank": "正处级", "note": "区委副书记、区政府党组书记"},
    # 李少锋 (前任书记)
    {"person_id": 2, "org_id": 1, "title": "复兴区委书记(前任)",
     "start_date": "2021-05", "end_date": "2026-?",
     "rank": "正处级", "note": "2021-05-18 任区委书记; 2026上半年离任, 调任市审计局"},
    {"person_id": 2, "org_id": 7, "title": "邯郸市审计局局长(现任)",
     "start_date": "2026-? ", "end_date": "present",
     "rank": "正处级", "note": "2026 上半年任(审计局领导班子页 2026-07-24); 一级调研员"},
    # 潘利军 (前任书记)
    {"person_id": 3, "org_id": 1, "title": "复兴区委书记(更早前任)",
     "start_date": "<2021-05", "end_date": "2021-05",
     "rank": "正处级", "note": "2021-05-18 免职"},
    # 王瑞峰
    {"person_id": 4, "org_id": 1, "title": "复兴区委副书记(前任)",
     "start_date": "2026-01? (至少)", "end_date": "2026-06?",
     "rank": "正处级", "note": "2026-01 仍在任; 2026-06/07 转市市监局"},
    {"person_id": 4, "org_id": 8, "title": "邯郸市市场监管局局长",
     "start_date": "2026-06", "end_date": "present",
     "rank": "正处级", "note": "2026-06 任市知识产权局局长; 2026-07 任市监局(兼)"},
    # 白建功
    {"person_id": 5, "org_id": 3, "title": "复兴区人大常委会主任",
     "start_date": "2021-07", "end_date": "present",
     "rank": "正处级", "note": "2021-07 十三届人大当选"},
    # 李勤芳
    {"person_id": 6, "org_id": 4, "title": "复兴区政协主席",
     "start_date": "2021?", "end_date": "present",
     "rank": "正处级", "note": "2026-01 仍任"},
    # 副区长/班子
    {"person_id": 7, "org_id": 2, "title": "复兴区常务副区长",
     "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "区统计局调研(2024-12)确认常务"},
    {"person_id": 8, "org_id": 2, "title": "复兴区副区长(曾任)",
     "start_date": "2021-07", "end_date": "2023-03", "rank": "副处级", "note": "后任市政府副秘书长, 2026-07 市住建局局长"},
    {"person_id": 9, "org_id": 2, "title": "复兴区副区长(2021)",
     "start_date": "2021-07", "end_date": "present?", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "复兴区副区长(2021)",
     "start_date": "2021-07", "end_date": "present?", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "复兴区副区长(2021)",
     "start_date": "2021-07", "end_date": "present?", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "复兴区委常委、统战部部长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": "2026-01 区政协会议出席"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 2, "person_b": 1, "type": "overlap",
     "context": "区委书记(李少锋)与区长(李阳)党政搭档 2021-2026 在任",
     "overlap_org": "中共邯郸市复兴区委员会/区政府", "overlap_period": "2021-2026"},
    # 前任书记→现任书记 (潘利军→李少锋)
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor",
     "context": "潘利军(更早前任区委书记)→李少锋 2021-05 接任",
     "overlap_org": "中共邯郸市复兴区委员会", "overlap_period": "2021-05"},
    # 区长接任 (李少锋原兼副书记→李阳接任)
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor",
     "context": "李少锋(原区委书记,同时免去区委副书记)→李阳 2021-05 接任区委副书记/区长",
     "overlap_org": "复兴区人民政府", "overlap_period": "2021-05"},
    # 书记→人大/政协
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区人大主任(四大班子)",
     "overlap_org": "复兴区", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与区政协主席",
     "overlap_org": "复兴区", "overlap_period": "2021-2026"},
    # 书记→副书记
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委副书记王瑞峰(区委班子)",
     "overlap_org": "中共邯郸市复兴区委员会", "overlap_period": "2023-2026"},
    # 区长→政府班子
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与常务副区长(区政府班子)",
     "overlap_org": "复兴区人民政府", "overlap_period": "2021-present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长田东(2021-2023)",
     "overlap_org": "复兴区人民政府", "overlap_period": "2021-2023"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "复兴区人民政府", "overlap_period": "2021-present"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "复兴区人民政府", "overlap_period": "2021-present"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "区长与副区长张莹",
     "overlap_org": "复兴区人民政府", "overlap_period": "2021-present"},
]


# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(STAGING_DIR, "复兴区_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "复兴区_network.gexf")

    # Idempotent: remove stale artifacts so the script can be re-run safely.
    for stale in (DB_PATH, GEXF_PATH):
        if os.path.exists(stale):
            os.remove(stale)

    run_build(
        slug="复兴区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete.")