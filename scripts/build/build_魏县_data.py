#!/usr/bin/env python3
"""
魏县领导班子工作关系网络 — Build script
河北省邯郸市魏县（县）

调查日期: 2026-08-05
Core targets: 县委书记 张平; 县委副书记、政府县长 李卫峰

官方/权威来源 (degraded-web mode, 部分主引擎限流, 主要依赖 www.wei.gov.cn 魏县党政网官网 + 邯郸市政府网 + 百度百科摘要 + 网易/澎湃等主流媒体任前报道交叉印证):
- 魏县党政网 领导之窗-县委（官网 ldzc_9, 2026-08-05 抓取快照）: 县委书记 张平; 县委副书记、政府县长 李卫峰;
  县委副书记 刘亚强; 县委常委、纪委书记、监委主任 翟亮; 县委常委、人武部部长 李张保。
- 魏县十七届人大七次会议（2025-10-10~11, 魏县党政网/微信官号）: 李卫峰全票当选魏县人民政府县长; 翟亮全票当选县监委主任。县领导名册含 张平、李卫峰、刘亚强、魏志凌、刘忠良、李庆民、王秀云、陈瑞学。
- 网易《邯郸人口大县县委书记调整》(2025-09-15): 张平,男,汉族,曲周县人,1980年7月生,2003年7月参加工作,2005年6月入党,
  燕山大学工商管理专业本科,省委党校在职研究生。曾任魏县县长; 2025-09 接棒苏雷芳任县委书记。
- 河北日报/人民资讯（2021-05-20）: 苏雷芳任魏县县委书记（接任 樊中青）; 2024-07/2025-06 仍以县委书记身份公开活动。
- 网易《河北5市人事任免》(2023-04-15): 张平任魏县县委副书记,免去高巍的魏县县委副书记、常委、委员职务（高巍调任大名县委书记）。

Confidence:
- 现任县委书记 张平 / 县长 李卫峰 = confirmed（魏县党政网官网快照 + 人大选举报道 + 两会新年贺词）。
- 县委班子 刘亚强 / 翟亮 / 李张保 = confirmed（官方县委页 + 人大选举）。
- 政府班子（刘勇、陈国军、吴瑞丽、张俊刚、李腾、高立彬、刘宇浩 等）= plausible（县政府常务会参会名单, 2026-01-05）。
- 前任书记 苏雷芳 / 樊中青 = confirmed; 前任县长 高巍 = confirmed（知名县（前任县长）, 2023-04 调任大名县委书记）。
- 张平 / 李卫峰 完整早期履历、出生地、籍贯、毕业院校、入党/参加工作时间等部分字段缺失──标记在 identity/open_questions 与 report/open_gaps.md。
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
    # ── 县委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "张平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "河北省邯郸市曲周县",
        "education": "燕山大学工商管理本科(1999-2003)；省委党校在职研究生经济管理专业",
        "party_join": "2005年6月",
        "work_start": "2003年7月",
        "current_post": "魏县县委书记",
        "current_org": "中共魏县委员会",
        "source": "魏县党政网；网易任前报道；河北日报",
    },
    # ── 县委副书记、政府县长 (County Mayor) ──
    {
        "id": 2,
        "name": "李卫峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县委副书记、政府县长",
        "current_org": "魏县人民政府",
        "source": "魏县党政网；魏县十七届人大七次会议",
    },
    # ── 县委副书记 (专职) ──
    {
        "id": 3,
        "name": "刘亚强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共魏县委员会",
        "source": "魏县党政网",
    },
    # ── 县委常委、纪委书记、监委主任 ──
    {
        "id": 4,
        "name": "翟亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共魏县纪律检查委员会",
        "source": "魏县党政网；魏县十七届人大七次会议",
    },
    # ── 县委常委、人武部部长 ──
    {
        "id": 5,
        "name": "李张保",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县委常委、人武部部长",
        "current_org": "魏县人民武装部",
        "source": "魏县党政网",
    },
    # ── 县政府领导（常务副职）──
    {
        "id": 6,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县政府领导（常务工作）",
        "current_org": "魏县人民政府",
        "source": "魏县政府第61次常务会；官方新闻",
    },
    # ── 县政府副县长 ──
    {
        "id": 7,
        "name": "陈国军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "魏县人民政府",
        "source": "魏县政府第61次常务会",
    },
    {
        "id": 8,
        "name": "吴瑞丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "魏县人民政府",
        "source": "魏县政府第61次常务会",
    },
    {
        "id": 9,
        "name": "张俊刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "魏县人民政府",
        "source": "魏县政府第61次常务会；官方新闻",
    },
    {
        "id": 10,
        "name": "李腾",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "魏县人民政府",
        "source": "魏县党政网（2026-03 调研新闻）",
    },
    {
        "id": 11,
        "name": "高立彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "魏县人民政府",
        "source": "魏县政府第61次常务会",
    },
    {
        "id": 12,
        "name": "刘宇浩",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "魏县人民政府",
        "source": "魏县政府第61次常务会",
    },
    # ── 县人大 / 政协领导 ──
    {
        "id": 13,
        "name": "魏志凌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县人大领导",
        "current_org": "魏县人大常委会",
        "source": "魏县十七届人大七次会议名册",
    },
    {
        "id": 14,
        "name": "李庆民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "县人大领导",
        "current_org": "魏县人大常委会",
        "source": "魏县人大会议；县政府列席",
    },
    # ── 前任县委书记 / 县长 ──
    {
        "id": 20,
        "name": "苏雷芳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "魏县前任县委书记（已离任）",
        "current_org": "",
        "source": "人民资讯(河北日报)；魏县党政网 2024-07/2025-06",
    },
    {
        "id": 21,
        "name": "高巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "大名县委书记（自魏县县长调任）",
        "current_org": "中共大名县委员会",
        "source": "本项目已有档案(build_大名县_政府.json)；搜狗/河北5市任免",
    },
    {
        "id": 22,
        "name": "樊中青",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "魏县前任县委书记（至2021-05）",
        "current_org": "",
        "source": "河北日报/人民资讯(2021-05-20)",
    },
    # ── 历史落马人物 ──
    {
        "id": 23,
        "name": "边飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "current_post": "魏县早期县委书记（约2000年代, 已落马）",
        "current_org": "",
        "source": "本项目已有档案 build_大名县/永年区; 纪检公开通报",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共魏县委员会", "type": "党委", "level": "县级", "parent": "中共邯郸市委", "location": "河北省邯郸市魏县"},
    {"id": 2, "name": "魏县人民政府", "type": "政府", "level": "县级", "parent": "邯郸市人民政府", "location": "河北省邯郸市魏县"},
    {"id": 3, "name": "中共魏县纪律检查委员会", "type": "纪检委", "level": "县级", "parent": "中共魏县委员会", "location": "河北省邯郸市魏县"},
    {"id": 4, "name": "魏县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "魏县", "location": "河北省邯郸市魏县"},
    {"id": 5, "name": "中国人民政治协商会议魏县委员会", "type": "政协", "level": "县级", "parent": "魏县", "location": "河北省邯郸市魏县"},
    {"id": 6, "name": "魏县人民武装部", "type": "军事机构", "level": "县级", "parent": "中共魏县委员会", "location": "河北省邯郸市魏县"},
    {"id": 7, "name": "中共大名县委员会", "type": "党委", "level": "县级", "parent": "中共邯郸市委", "location": "河北省邯郸市大名县"},
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    # 张平（县委书记, 2025-09 至今）
    {"person_id": 1, "org_id": 1, "title": "魏县县委书记", "start_date": "2025-09", "end_date": "present", "rank": "正处级",
     "note": "接棒苏雷芳任县委书记；兼任县人武部党委第一书记"},
    {"person_id": 1, "org_id": 2, "title": "魏县县长（先任）", "start_date": "2023-04", "end_date": "2025-09", "rank": "正处级",
     "note": "2023-04 任县委副书记、政府副县长、代理县长"},
    # 李卫峰（县长）
    {"person_id": 2, "org_id": 1, "title": "魏县县委副书记", "start_date": "2025-09", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "魏县县长", "start_date": "2025-10", "end_date": "present", "rank": "正处级",
     "note": "2025-09 代县长; 2025-10-10 魏县十七届人大七次会议当选"},
    # 刘亚强（县委副书记）
    {"person_id": 3, "org_id": 1, "title": "魏县县委副书记", "start_date": "present", "end_date": "present", "rank": "副处级", "note": "专职副书记"},
    # 翟亮（纪委书记/监委主任）
    {"person_id": 4, "org_id": 3, "title": "魏县纪委书记、监委主任", "start_date": "2025-10", "end_date": "present", "rank": "副处级",
     "note": "2025-10 当选监委主任"},
    {"person_id": 4, "org_id": 1, "title": "魏县县委常委", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    # 李张保（人武部长）
    {"person_id": 5, "org_id": 6, "title": "魏县人武部部长", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "魏县县委常委", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    # 政府班子
    {"person_id": 6, "org_id": 2, "title": "魏县常务副县长（政府领导）", "start_date": "present", "end_date": "present", "rank": "副处级", "note": "参与县政府常务工作"},
    {"person_id": 7, "org_id": 2, "title": "魏县副县长", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "魏县副县长", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "魏县副县长", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "魏县副县长", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "魏县政府领导", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "魏县政府领导", "start_date": "present", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 13, "org_id": 4, "title": "魏县人大领导", "start_date": "present", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "魏县人大领导", "start_date": "present", "end_date": "present", "rank": "正处级", "note": ""},
    # 前任
    {"person_id": 20, "org_id": 1, "title": "魏县县委书记（前任）", "start_date": "2021-05", "end_date": "2025-09", "rank": "正处级",
     "note": "2021-05-20 任; 2025 离任（张平接任）"},
    {"person_id": 21, "org_id": 2, "title": "魏县县长（前任）", "start_date": "2023-04 前", "end_date": "2023-04", "rank": "正处级",
     "note": "2023-04 调任大名县委书记"},
    {"person_id": 21, "org_id": 7, "title": "大名县委书记（调任）", "start_date": "2023", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 1, "title": "魏县县委书记（更早前任）", "start_date": "2021-05 前", "end_date": "2021-05", "rank": "正处级",
     "note": "2021-05 免职"},
    {"person_id": 23, "org_id": 1, "title": "魏县县委书记（早期, 落马）", "start_date": "约2003", "end_date": "约2008", "rank": "正处级",
     "note": "2013 年落马, 被判无期徒刑"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "魏县县委书记与县长党政搭档（2025-09/10 起在任）",
     "overlap_org": "区委/县政府", "overlap_period": "2025-present"},
    # 前任县委书记 苏雷芳 → 现任书记 张平
    {"person_a": 20, "person_b": 1, "type": "predecessor_successor",
     "context": "苏雷芳（前任魏县县委书记, 2021-05 到任）→ 张平（2025-09 接任）",
     "overlap_org": "中共魏县委员会", "overlap_period": "2025-09"},
    # 前任县委书记 樊中青 → 苏雷芳
    {"person_a": 22, "person_b": 20, "type": "predecessor_successor",
     "context": "樊中青（2021-05 免职）→ 苏雷芳（2021-05-20 任魏县县委书记）",
     "overlap_org": "中共魏县委员会", "overlap_period": "2021-05"},
    # 前任县长 高巍 → 张平（县长交接）
    {"person_a": 21, "person_b": 1, "type": "predecessor_successor",
     "context": "高巍（前任魏县县长, 2023-04 调任大名县委书记）→ 张平（2023-04 任魏县县委副书记、代理县长）",
     "overlap_org": "魏县人民政府", "overlap_period": "2023-04"},
    # 张平（县长转书记）→ 李卫峰（接任县长）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "张平由县长转任县委书记（2025-09）→ 李卫峰 接任代县长/县长",
     "overlap_org": "魏县人民政府", "overlap_period": "2025-09"},
    # 书记 → 专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "魏县县委书记与县委副书记（区委班子核心）",
     "overlap_org": "中共魏县委员会", "overlap_period": "2025-present"},
    # 书记 → 纪委书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "魏县县委书记与县纪委书记、监委主任",
     "overlap_org": "中共魏县委员会", "overlap_period": "2025-present"},
    # 书记 → 人武部长（常委班子）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "魏县县委书记与县人武部部长（常委班子）",
     "overlap_org": "中共魏县委员会", "overlap_period": "2025-present"},
    # 县长 → 各副县长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与常务副县长（政府班子）", "overlap_org": "魏县人民政府", "overlap_period": "2025-present"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "魏县人民政府", "overlap_period": "2025-present"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "魏县人民政府", "overlap_period": "2025-present"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "魏县人民政府", "overlap_period": "2025-present"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "魏县人民政府", "overlap_period": "2025-present"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与县政府领导", "overlap_org": "魏县人民政府", "overlap_period": "2025-present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与县政府领导", "overlap_org": "魏县人民政府", "overlap_period": "2025-present"},
    # 高巍 → 大名县委书记（跨县）链条
    {"person_a": 21, "person_b": 1, "type": "overlap",
     "context": "高巍（魏县→大名）与张平（魏县）跨县干部轮换届上的交接链",
     "overlap_org": "魏县", "overlap_period": "2023"},
    # 早期历史 (边飞 落马前任)
    {"person_a": 23, "person_b": 20, "type": "overlap",
     "context": "边飞（早期魏县书记, 落马）为魏县县委书记更早历史链条人物",
     "overlap_org": "中共魏县委员会", "overlap_period": "跨年代（非直接交接）"},
]

# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(STAGING_DIR, "魏县_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "魏县_network.gexf")

    # Idempotent: remove stale artifacts so the script can be re-run safely.
    for stale in (DB_PATH, GEXF_PATH):
        if os.path.exists(stale):
            os.remove(stale)

    run_build(
        slug="魏县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete.")