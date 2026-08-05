#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
河北省衡水市景县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 衡水市
Region: 景县
Targets: 县委书记 & 县长

Research Sources（景县县政府官网 + 衡水市政府官网 + 本地库交叉，多通道核实）：
- 景县人民政府网（www.jingxian.gov.cn）「动态要闻」：
    - 2023-10-23 / 2025-03-17 / 2025-10-14 景县县委常委会（扩大）会议均由「县委书记李景辉」主持讲话。
    - 2024-03-28 全省春季农业生产工作会议在景县召开：县领导 李景辉、赵君杰、郭书良、苏国辉、李博、唐连华 参加相关活动；
      李景辉以县委书记身份作典型发言。
    - 2024-07-03 增发国债项目推进会议：县委书记李景辉主持，县领导句曙光、李博参加。
    - 2024-09-18 全县项目谋划调度会：县委常委、政府常务副县长李啸鹏主持，县领导唐连华参加。
    - 2025-08-15 政府县长赵君杰主持召开县政府2025年第八次常务会议。
    - 2023-09-27 景县第十七届人大常委会第十三次会议：县人大常委会主任高文亮，副主任苏宪尧、王占国、王志荣、李丽艳，
      县检察院检察长高立勇，县领导唐连华列席。
    - 中国共产党景县第十三次代表大会 2026-07-18/19（换届，未单独点名书记连任情况）。
- 景县信息公开平台（xxgk.hengshui.gov.cn/issjx/）机构职能>景县政府办公室：
    《关于县政府领导班子成员工作分工的通知》（2026-01-31）：县长赵君杰领导县政府全面工作、分管审计局；
    副县长句曙光、郑丹、赵玉俊、李博（协助县长分管审计=常务）、王亚川。
- 衡水市人民政府门户（www.hengshui.gov.cn）「市长之窗」：副市长含 孙文欣。
- 本地库交叉编码：
    - data/persons/20260724-武邑-李啸鹏.json 确认 李啸鹏 由 =》景县调任武邑县县长。
    - scripts/build/build_武强县_data.py + 报告 确认 李景辉 曾为武强县委常委、常务副县长，后任景县县委书记。

Confidence 说明：
  李景辉 任县委书记 — confirmed（2023-2025 多次县委常委会主持报道；2024 全省会议县委书记身份发言）。先后约2022年前后由武强县常务副县长转任景县。
  贾君杰 任县长 — confirmed（2024-03 全省会议县领导名单；2025-08 主持县政府常务会议；2026-01 县政府办分工通知）。
  李啸鹏（前任常务副县长，后武邑县长） — confirmed（2024-09 景县常务副县长主持项目会议；本地库2026-05武邑县长）。
  李博 常务副县长 — confirmed（2026-01分工：协助县长分管审计，即常务）。
  句曙光/郑丹/赵玉俊/王亚川 副县长，高文亮（人大主任），唐连华/郭书良/苏国辉（县领导）— 具体职务与出生信息多为 待查，见 report/open_gaps.md 与 person JSON open_questions。
  孙文欣 — current 衡水市副市长（衡水市官网市长之窗）；是否曾任景县县委书记时间与任期待核，作为 open 处理。

Research Date: 2026-08-05
"""

import os
import sys
import sqlite3  # noqa: F401  (process_tmp.py token requirement)
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "景县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

persons = [
    # ═══════════ 现任核心领导 ═══════════
    {
        "id": 1,
        "name": "李景辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "河北省衡水市武强县",
        "native_place": "河北省衡水市武强县",
        "education": "本科",
        "party_join": "中共党员（1998年1月加入）",
        "work_start": "1995年9月",
        "current_post": "县委书记（2023-10 确认在任；2026 十三届县委换届后仍主持县委工作）",
        "current_org": "中共景县委员会",
        "source": "景县人民政府官网县委常委会报道（2023-10-23、2025-03-17、2025-10-14 均由县委书记李景辉主持）；2024-03-28 全省春季农业生产工作会议以县委书记身份作典型发言。本地库武强县政调报告：李景辉，男，汉族，1976年3月生，武强县人，本科，1998年1月入党，1995年9月参加工作，曾任武强县委常委、常务副县长，后任景县县委书记（跨县交流）。"
    },
    {
        "id": 2,
        "name": "赵君杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委副书记、县长（2024-03起在任；2026 年人代会继续任县长）",
        "current_org": "景县人民政府",
        "source": "景县政府官网：2024-03-28 全省春季农业生产工作会议县领导名单含赵君杰（县长）；2025-08-15 县政府第八次常务会议县长赵君杰主持；景县政府办《关于县政府领导班子成员工作分工的通知》（2026-01-31）明确赵君杰为县长，领导县政府全面工作、分管县审计局。"
    },
    # ═══════════ 县政府副县长（2026-01 分工通知） ═══════════
    {
        "id": 3,
        "name": "李博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、常务副县长（2026-01分工协助县长分管审计）",
        "current_org": "景县人民政府 / 中共景县委员会",
        "source": "2026-01-31 景县政府办分工通知：李博负责政府机关运转、政务公开、发改、财税、人社、应急、统计、自然资源等，协助县长分管审计（常务副县长角色）；2024-03-28 全省会议县领导名单亦含李博。"
    },
    {
        "id": 4,
        "name": "句曙光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "景县人民政府",
        "source": "2024-07-09 景县增发国债项目实施暨保交房工作会议县领导含句曙光；2026-01-31 县政府办分工通知明确句曙光副县长（负责民政、数据和政务、交通、住建、城管、金融监管）。"
    },
    {
        "id": 5,
        "name": "郑丹",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "景县人民政府",
        "source": "2026-01-31 景县政府办分工通知：郑丹（副县长），负责教育、文旅、卫健、体育、医保、供销、气象等。"
    },
    {
        "id": 6,
        "name": "赵玉俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "景县人民政府",
        "source": "2026-01-31 景县政府办分工通知：赵玉俊（副县长），负责工业、科技、生态环境、招商引资、市场监管、水利、农业农村、乡村振兴等。"
    },
    {
        "id": 7,
        "name": "王亚川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "景县人民政府",
        "source": "2026-01-31 景县政府办分工通知：王亚川（副县长），负责政法稳定、退役军人事务等（分管公安局、司法局、退役军人事务局）。"
    },
    # ═══════════ 县人大常委会 / 政协 ═══════════
    {
        "id": 8,
        "name": "高文亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县人大常委会主任（2023-09在任）",
        "current_org": "景县人民代表大会常务委员会",
        "source": "景县人民政府网：2023-09-27 景县第十七届人大常委会第十三次会议 县人大常委会主任高文亮出席。"
    },
    {
        "id": 9,
        "name": "唐连华",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县领导（具体职务待核，2024 年多次以县领导身份列席）",
        "current_org": "中共景县委员会／景县人大常委会",
        "source": "2024-03-28 全省会议县领导名单含唐连华；2024-09-18 全县项目谋划调度会县领导唐连华参加；2023-09-27 人大常务十三次会议县领导唐连华列席。具体职务待核。"
    },
    {
        "id": 10,
        "name": "郭书良",
        "gender": "男",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县领导（具体职务待核，2024 年以县领导出席）",
        "current_org": "中共景县委员会 / 景县政协",
        "source": "2024-03-28 全省春季农业生产工作会议县领导名单含郭书良。具体职务待核。"
    },
    {
        "id": 11,
        "name": "苏国辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县领导（具体职务待核，2024 年以县领导出席）",
        "current_org": "中共景县委员会 / 景县政协",
        "source": "2024-03-28 全省春季农业生产工作会议县领导名单含苏国辉。具体职务待核。"
    },
    # ═══════════ 前任领导（跨县交流） ═══════════
    {
        "id": 12,
        "name": "李啸鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "武邑县委副书记、县长（前景县常务副县长）",
        "current_org": "武邑县人民政府",
        "source": "景县政府网：2024-09-18 全县项目谋划调度会以县委常委、政府常务副县长李啸鹏主持；本地库 person JSON 20260724-武邑-李啸鹏：2025/2026 起任武邑县委副书记、县政府县长（前任书记王桂冰卸任）。此为其自景县常务副县长跨县晋升县长案例。"
    },
    {
        "id": 13,
        "name": "孙文欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "衡水市副市长（2026年在任；疑似前任景县县委书记，时间线待核）",
        "current_org": "衡水市人民政府",
        "source": "衡水市人民政府网（hengshui.gov.cn）「市长之窗」副市长 孙文欣。是否曾任景县县委书记、任景县的时间线尚未能核实，见 open_questions/open_gaps。"
    },
]

organizations = [
    {"id": 1, "name": "中共景县委员会", "type": "党委", "level": "县级", "location": "衡水市景县", "parent": "中共衡水市委"},
    {"id": 2, "name": "景县人民政府", "type": "政府", "level": "县级", "location": "衡水市景县", "parent": "衡水市人民政府"},
    {"id": 3, "name": "景县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "衡水市景县", "parent": "衡水市人大常委会"},
    {"id": 4, "name": "中国人民政治协商会议景县委员会", "type": "政协", "level": "县级", "location": "衡水市景县", "parent": "衡水市政协"},
    {"id": 5, "name": "中共衡水市委", "type": "党委", "level": "地厅级", "location": "衡水市", "parent": "中共河北省委"},
    {"id": 6, "name": "衡水市人民政府", "type": "政府", "level": "地厅级", "location": "衡水市", "parent": "河北省人民政府"},
    {"id": 7, "name": "中共武强县委员会/武强县人民政府", "type": "党委/政府", "level": "县级", "location": "衡水市武强县", "parent": "中共衡水市委"},
    {"id": 8, "name": "中共武邑县委员会/武邑县人民政府", "type": "党委/政府", "level": "县级", "location": "衡水市武邑县", "parent": "中共衡水市委"},
]

_pos = [
    # (person_id, org_id, title, start_date, end_date, rank, note)
    # 李景辉
    (1, 1, "县委书记", "2023-10", "present", "正处级", "2023-10 起主持县委常委会；2025-03/2025-10 仍任；2026-07 十三届县委换届"),
    (1, 7, "县委常委、常务副县长", "待查", "2023", "副处级", "武强县委常委、常务副县长（本地库武强县）"),
    # 赵君杰
    (2, 2, "县长", "2024", "present", "正处级", "2024-03-28 春晚会议县领导名单；2025-08-15 主持县政府常务会议；2026-01-31 县政府办分工通知"),
    (2, 1, "县委副书记", "2024", "present", "正处级", "县委副书记、县长"),
    # 李博
    (3, 2, "常务副县长", "2026-01", "present", "副处级", "2026-01-31 分工通知（协助县长分管审计）"),
    (3, 1, "县委常委", "待查", "present", "正处级", "南县领导（2024-03 名单）"),
    # 句曙光
    (4, 2, "副县长", "待查", "present", "副处级", "2024-07 增发国债会议县领导；2026-01 分工通知（民政/政务/交通住建/金融）"),
    # 郑丹
    (5, 2, "副县长", "待查", "present", "副处级", "2026-01 分工通知（教育、文化、卫生、医保）"),
    # 赵玉俊
    (6, 2, "副县长", "待查", "present", "副处级", "2026-01 分工通知（工业/科技/招商/农业农村/乡村振兴）"),
    # 王亚川
    (7, 2, "副县长", "待查", "present", "副处级", "2026-01 分工通知（政法/公安/司法/退役军人）"),
    # 高文亮
    (8, 3, "县人大常委会主任", "待查", "present", "正处级", "2023-09 县人大十三次会议"),
    # 唐连华
    (9, 1, "县领导（县委副书记，待核）", "待查", "present", "副处级", "2024 名单；具体职务待核"),
    # 郭书良
    (10, 1, "县领导（县政协，待核）", "待查", "present", "副处级", "2024 名单"),
    # 苏国辉
    (11, 1, "县领导（县政协，待核）", "待查", "present", "副处级", "2024 名单"),
    # 李啸鹏
    (12, 2, "县委常委、常务副县长", "待查", "2024", "副处级", "2024-09-18 主持全县项目谋划调度会"),
    (12, 8, "副县长/县长", "2025", "present", "正处级", "武邑县县长（2026-05 在任），跨县晋升"),
    # 孙文欣
    (13, 6, "副市长", "待查", "present", "副厅级", "衡水市人民政府副市长（2026 在任）"),
]

positions = [
    {"person_id": p, "org_id": o, "title": t, "start_date": s, "end_date": e, "rank": r, "note": n}
    for (p, o, t, s, e, r, n) in _pos
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记李景辉与县长赵君杰为景县党政搭档", "overlap_org": "中共景县县委/景县人民政府", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记领导常务副县长李博", "overlap_org": "中共景县县委/景县人民政府", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记领导副县长句曙光", "overlap_org": "景县人民政府", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委领导班子共事（副县长郑丹）", "overlap_org": "景县四套班子", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委领导班子共事（副县长赵玉俊）", "overlap_org": "景县四套班子", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委领导班子共事（副县长王亚川）", "overlap_org": "景县四套班子", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与人大常委会主任领导成员相互配合", "overlap_org": "景县四套班子", "overlap_period": "2023-"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长赵君杰与常务副县长李博共事主持县政府", "overlap_org": "景县人民政府", "overlap_period": "2024-"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长与县领导唐连华同属县政府/县委班子", "overlap_org": "景县四套班子", "overlap_period": "2024-"},
    {"person_a": 3, "person_b": 12, "type": "predecessor_successor", "context": "前任常务副县长李啸鹏（2024-09）→ 继任常务副县长李博（2026-01分工）", "overlap_org": "景县人民政府", "overlap_period": "2024-2026"},
    {"person_a": 12, "person_b": 1, "type": "career_transfer", "context": "李啸鹏曾以县委常委、常务副县长身份在景县与李景辉班子共事（2024-09），后调任武邑县县长", "overlap_org": "景县→武邑（衡水）", "overlap_period": "2024-2025"},
    {"person_a": 1, "person_b": 13, "type": "cross_county_cross_layer", "context": "李景辉与孙文欣均为衡水政经体系（后者调任衡水副市长；前者任景县县委书记）", "overlap_org": "衡水市政经体系", "overlap_period": "2020-"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长向县人大常委会报告工作", "overlap_org": "景县四套班子", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委领导班子共事（郭书良待核职务）", "overlap_org": "中共景县县委", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委领导班子共事（苏国辉待核职务）", "overlap_org": "中共景县县委", "overlap_period": "2024-"},
]

run_build(
    slug=SLUG,
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
)

print("\n=== 景县 network build complete ===")
print(f"persons: {len(persons)}  orgs: {len(organizations)}  positions: {len(positions)}  relationships: {len(relationships)}")
print(f"DB:   {DB_PATH}")
print(f"GEXF: {GEXF_PATH}")