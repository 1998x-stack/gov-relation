#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
河北省沧州市南皮县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 沧州市
Region: 南皮县
Targets: 县委书记 & 县长

Research Sources（政府官网 + 地方媒体，多通道交叉核实）：
- 南皮县人民政府官网（www.nanpi.gov.cn）「政府常务会」：
    - 2024-05-15 / 2025-06-06 / 2026-05-15 县政府常务会议均由「县委副书记、县长罗遥」主持（2026-05 仍任县长）。
    - 2026-02-10《"两会"进行时|县十八届人大六次会议闭幕》：主席团执行主席 毕汝卫、罗遥、肖江普、
      孙国臣、张林国、吕学周；肖江普主持；毕汝卫作总结讲话（县委书记身份）。
- 南皮县人民政府官网「机构设置>领导介绍」：温纯玉，女，1981年3月生，满族，研究生，现任南皮县委常委、副县长，
  负责残联工作；协助吴建业同志分管乡村振兴工作。
- 百度百科「中国共产党南皮县委员会」：现任县委书记为毕汝卫。
- 百度百科「毕汝卫」：男，河北沧县人，1977年7月生，1997年参加工作，2004年入党，中国农业大学；
  沧州市新华区国债服务部职员→南大街办事处→区政府办公室科员、副主任→2017 新华区委常委、办公室主任→
  2019 沧州市委副秘书长→2021 沧州市体育局长→2021 黄骅市委副书记、市长→2022-06-11 南皮县委书记。
- 百度百科/望海司「罗遥」：男，1987年12月生，博士研究生（清华大学），中共党员，河北省2015年定向招录选调生；
  石家庄桥西区彭后街道历练→2017-01 石家庄栾城区栾城镇党委副书记、镇长→涞水县委常委、副县长→
  2024-01-18 南皮县委副书记、代县长→2024-01-24 十八届人大四次会议补选为县长。
- 本地库交叉编码：data/persons/20260805-河北省-唐山市-区委书记-董继华.json 确认 南皮前任县委书记 董继华
  （2021-05 至 2021-07，事后赴省工业和信息化厅副厅长，现任唐山市委常委、曹妃甸区委书记）。
- 澎湃新闻《南皮县十八届人大常委会召开第五次会议》（2022-01-18）：时任县政府副县长岳建玲、监委主任李志歧、
  县人民法院院长庞爱民、县人民检察院检察长孙维东。
- 网易「沧州一地县长有变」（2024-01）：前任县长（胡学锋）南皮县长任期约 2021-05 至 2024-01，罗遥接任。
- 沧州市人民政府网（cangzhou.gov.cn）南皮频道：县委书记毕汝卫主持召开十二届县委第113次常委会（2024-11-19）等。
- 360百科「南皮县」（2024-06 快照）：县委书记 毕汝卫(2022.06)；县长 胡学锋（后更早信息，县长已更替为罗遥）。

Confidence 说明：
  毕汝卫 任县委书记 — confirmed（沧州晚报/河北日报 2022-06-11 任前公示；2024-11 县委常委会报道；2026-02 人代会
    亲政讲话）。截至本次调研（2026-08-05），有媒体（网易，约 2026-07 底）指称毕汝卫已履新沧州市海洋和港航管理局
    党组书记（原南皮县委书记），其继任者身份暂未查得，见 person JSON open_questions。
  罗遥 任县长 — confirmed（2024-01-18 人大常委会决定其为代县长；2024-01-24 人大五次会议补选县长；
    2026-05-15 县长罗遥主持县政府常务会）。
  董继华（前任书记）/ 胡学锋（前任县长）— confirmed（本地库 曹妃甸区 person JSON + 澎湃新闻）。
  温纯玉（县委常委、副县长）：confirmed（官网领导介绍）。
  肖江普（县人大常委会主任）/ 邢毅（县政协主席）— plausible-confirmed（2025/2026 人代会主席台 + 处级领导名单）。
  其余领导班子 成员出生信息/精确分工 — 多为 待查，见 person JSON open_questions。

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

SLUG = "南皮县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

persons = [
    # ═══════════ 现任核心领导 ═══════════
    {
        "id": 1,
        "name": "毕汝卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年7月",
        "birthplace": "河北省沧县",
        "native_place": "河北省沧县",
        "education": "大学（中国农业大学）",
        "party_join": "中共党员（2004年加入）",
        "work_start": "1997年",
        "current_post": "县委书记（2022-06起；2026年中曾报道转任沧州市海洋和港航管理局党组书记）",
        "current_org": "中共南皮县委员会",
        "source": "百度百科「毕汝卫」/「中国共产党南皮县委员会」：男，河北沧县人，1977-07生，中国农大毕业，1997参工/2004入党；沧州市新华区国债服务部→南大街办事处→新华区政府办科员、副主任→2017 新华区委常委、办公室主任→2019 沧州市委副秘书长→2021 沧州市体育局长→2021 黄骅市委副书记、市长→2022-06-11 南皮县委书记。沧州晚报/河北日报任前公示；2024-11 主持十二届县委113次常委；2026-02 人代会讲话；2026-07 公开报道指‘原南皮县委书记毕汝卫’履新沧州海洋和港航管理局党组书记。"
    },
    {
        "id": 2,
        "name": "罗遥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "博士研究生（清华大学）",
        "party_join": "中共党员",
        "work_start": "2015年",
        "current_post": "县委副书记、县长",
        "current_org": "南皮县人民政府",
        "source": "南皮县政府官网领导介绍（2023-08-04）：罗遥，男，汉族，1987-12生，博士研究生，中共党员，现任南皮县委副书记、县长；望海司2024-01「罗遥，清华大学博士，河北省2015年定向招录选调生，初在石家庄桥西区彭后街锻炼，2017-01到石家庄栾城区栾城镇任党委副书记、镇长，后任涞水县委常委、副县长」；2024-01-18 人大常委会任命副县长/代县长；2024-01-24 十八届人大五次会议补选县长；2024/2025/2026 多次主持县政府常务会议。"
    },
    # ═══════════ 四套班子负责人 ═══════════
    {
        "id": 3,
        "name": "肖江普",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县人大常委会主任",
        "current_org": "南皮县人民代表大会（常务委员会）",
        "source": "南皮县政府《2026-02-16 县十八届人大六次会议闭幕》：大会主席团常务主席、执行主席 肖江普 主持大会；2025-01 十八届人大五次会议县处级领导名单将 肖江普列为人大主任。"
    },
    {
        "id": 4,
        "name": "邢毅",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议南皮县委员会",
        "source": "南皮县十八届人大五次会议（2025-2026）县处级领导名单：邢毅（县政协主席）；政协南皮县十届六次全会（2026-02-07，南皮发布）。"
    },
    # ═══════════ 换届前专职副书记/常务副县长等 ═══════════
    {
        "id": 5,
        "name": "吴建业",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委/县政府领导（分管乡村振兴统筹，温纯玉协助)",
        "current_org": "中共南皮县委员会／南皮县人民pie政府",
        "source": "南皮县政府官网领导介绍：温纯玉“协助 吴建业同志分管乡村振兴工作”；吴建业职务为县委/县政府分管领导，精确职务待核。"
    },
    {
        "id": 6,
        "name": "温纯玉",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1981年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "南皮县人民政府 / 中共南皮县委员会",
        "source": "南皮县政府官网领导介绍（发布日期2023-11-10）：温纯玉，女，1981年3月生，满族，研究生，现任南皮县委常委、副县长；负责残联工作，协助吴建业同志分管乡村振兴工作；分管残疾人联合会。2025-01 十八届人大五次会议县处级领导名单亦含温纯玉。"
    },
    # ═══════════ 前任领导 ═══════════
    {
        "id": 7,
        "name": "董继华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "唐山市委常委、曹妃甸区委书记（前任南皮县委书记）",
        "current_org": "中共唐山市曹妃甸区委员会",
        "source": "本地库 data/persons/20260805-河北省-唐山市-区委书记-董继华.json：2021-05 任南皮县委书记（一级调研员），2021-07 离任后赴河北省工业和信息化厅副厅长，现任唐山市委常委、曹妃甸区委书记。"
    },
    {
        "id": 8,
        "name": "胡学锋",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任南皮县长（约2021-05 至 2024-01）",
        "current_org": "南皮县人民政府",
        "source": "澎湃/望海司 2024-01《沧州一地县长有变》：前任南皮县长任期约 2021-05 至 2024-01，罗遥接任。360百科南皮县（2024-06快照）记县长 胡学锋。"
    },
    # ═══════════ 县委领导班子成员（处级，2025-2026 人大名单） ═══════════
    {
        "id": 9,
        "name": "李军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县处级领导（县委班子成员）",
        "current_org": "中共南皮县委员会",
        "source": "2025-06/ 南皮县十八届人大五次会议县处级领导名单。具体职务待查。"
    },
    {
        "id": 10,
        "name": "刘席纲",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县处级领导（县委班子成员）",
        "current_org": "中共南皮县委员会",
        "source": "2025-06 十八届人大五次会议县处级名单。具体职务待查。"
    },
    {
        "id": 11,
        "name": "蔡宏浩",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县处级领导（县委班子成员）",
        "current_org": "中共南皮县委员会",
        "source": "2026-02 人代会主席台就座名单 + 2025-06 县处级名单。具体职务待查。"
    },
    {
        "id": 12,
        "name": "王庆君",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县处级领导（县政府班子成员）",
        "current_org": "南皮县人民政府",
        "source": "2026-02 人代会主席台名单 + 2025 县处级名单。具体职务待查。"
    },
    {
        "id": 13,
        "name": "郑勇",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县处级领导（县政府班子成员）",
        "current_org": "南皮县人民政府",
        "source": "2026-02 人代会主席台名单 + 2025 县处级名单。具体职务待查。"
    },
]

organizations = [
    {"id": 1, "name": "中共南皮县委员会", "type": "党委", "level": "县级", "location": "沧州市南皮县", "parent": "中共沧州市委"},
    {"id": 2, "name": "南皮县人民政府", "type": "政府", "level": "县级", "location": "沧州市南皮县", "parent": "沧州市人民政府"},
    {"id": 3, "name": "南皮县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "沧州市南皮县", "parent": "沧州市人大常委会"},
    {"id": 4, "name": "中国人民政治协商会议南皮县委员会", "type": "政协", "level": "县级", "location": "沧州市南皮县", "parent": "沧州市政协"},
    {"id": 5, "name": "沧州市发展和改革委员会", "type": "政府_市直", "level": "地厅级", "location": "沧州市", "parent": "沧州市人民政府"},
    {"id": 6, "name": "河北省工业和信息化厅", "type": "政府_省直", "level": "厅级", "location": "石家庄市", "parent": "河北省人民政府"},
    {"id": 7, "name": "中共唐山市曹妃甸区委员会", "type": "党委", "level": "地厅级", "location": "唐山市曹妃甸区", "parent": "中共唐山市委"},
    {"id": 8, "name": "中共黄骅市委员会/黄骅市人民政府", "type": "党委/政府", "level": "县级市", "location": "沧州市黄骅市", "parent": "中共沧州市委/沧州市人民政府"},
    {"id": 9, "name": "沧州市海洋和港航管理局", "type": "政府_市直", "level": "地厅级", "location": "沧州市", "parent": "沧州市人民政府"},
    {"id": 10, "name": "中共沧州市委员会", "type": "党委", "level": "地厅级", "location": "沧州市", "parent": "中共河北省委"},
    {"id": 11, "name": "石家庄市栾城区栾城镇", "type": "乡镇", "level": "科级", "location": "石家庄市栾城区", "parent": "石家庄市"},
    {"id": 12, "name": "中共涞水县委员会/涞水县人民政府", "type": "党委/政府", "level": "县级", "location": "保定市涞水县", "parent": "中共保定市委"},
]

_pos = [
    # (person_id, org_id, title, start_date, end_date, rank, note)
    (1, 1, "县委书记", "2022-06", "present", "正处级", "2022-06-11 南皮领导干部大会任命；2026-07 有报道指其转任沧州海洋和港航管理局党组书记（原南皮县委书记）"),
    (1, 8, "市委副书记、市长", "2021", "2022-06", "正处级", "黄骅市委副书记、市长"),
    (1, 10, "市委副秘书长", "2019", "2021", "副处级", "沧州市委副秘书长"),
    (1, 10, "市体育局党组书记/局长", "2021", "2021", "正处级", "沧州市体育局长"),
    (2, 2, "县长", "2024-01-24", "present", "正处级", "2024-01-18 代县长 → 2024-01-24 当选县长"),
    (2, 1, "县委副书记", "2024-01", "present", "正处级", "县委副书记、县长"),
    (2, 12, "县委副书记、县长" if False else "县委常委、副县长", "待查", "2024-01", "副处级", "涞水县委常委、副县长"),
    (3, 3, "县人大常委会主任", "约2021", "present", "正处级", "2026-02 人代会执行主席/主持大会"),
    (4, 4, "县政协主席", "约2021", "present", "正处级", "2026-02 政协十届六次全会"),
    (5, 1, "县委分管领导（常务副县长）", "待查", "present", "待查", "主管乡村振兴，温纯玉协助"),
    (6, 2, "副县长", "约2021", "present", "副处级", "官网领导介绍2023-11"),
    (6, 1, "县委常委", "待查", "present", "正处级", "南皮县委常委"),
    (7, 1, "县委书记", "2021-05", "2021-07", "正处级", "南皮县委书记（一级调研员）"),
    (7, 5, "市发改委主任", "2020-02", "2021-07", "正处级", "沧州市发展改革委主任"),
    (7, 6, "省工信厅副厅长", "2021-07", "2025", "副厅级", "河北省工业信息化厅副厅长、党组成员"),
    (7, 7, "市委常委、曹妃甸区委书记", "2025", "present", "副厅级", "现任唐山曹妃甸区委书记"),
    (8, 2, "县长", "2021-05", "2024-01", "正处级", "前任县长胡学锋，罗遥接任"),
    (9, 1, "县委班子成员", "待查", "present", "正处级", "2025 县处级名单"),
    (10, 1, "县处级领导（县委）", "待查", "present", "正处级", "2025 县处级名单"),
    (11, 1, "县处级领导（县委）", "待查", "present", "正处级", "2026-02 主席台名单"),
    (12, 2, "县处级领导（县政府）", "待查", "present", "副处级", "2026-02 主席台名单"),
    (13, 2, "县处级领导（县政府）", "待查", "present", "副处级", "2026-02 主席台名单"),
]
positions = [
    {"person_id": p, "org_id": o, "title": t, "start_date": s, "end_date": e, "rank": r, "note": n}
    for (p, o, t, s, e, r, n) in _pos
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记毕汝卫与县委副书记、县长罗遥为南皮党政搭档", "overlap_org": "中共南皮县委/南皮县政府", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 7, "type": "predecessor_successor", "context": "董继华（前任书记，2021-05至2021-07）→ 毕汝卫接任南皮县委书记（2022-06）", "overlap_org": "中共南皮县委员会", "overlap_period": "2022前后交接"},
    {"person_a": 2, "person_b": 8, "type": "predecessor_successor", "context": "胡学锋（前任县长）→ 罗遥（代县长2024-01-18，县长2024-01-24）", "overlap_org": "南皮县人民政府", "overlap_period": "2024-01"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记领导县人大常委会主任", "overlap_org": "南皮县四套班子", "overlap_period": "2021-"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记领导县政协主席", "overlap_org": "南皮县四套班子", "overlap_period": "2021-"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与人大主任共参加人大全会", "overlap_org": "南皮县四套班子", "overlap_period": "2024-"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长温纯玉（分管残联）；温纯玉协助吴建业分管乡村振兴", "overlap_org": "南皮县人民政府", "overlap_period": "2024-"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "温纯玉协助吴建业分管乡村振兴（并列分工）", "overlap_org": "南皮县人民政府", "overlap_period": "2023-"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记领导呼应组（县委专责领导）", "overlap_org": "中共南皮县委", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委领导班子共事", "overlap_org": "中共南皮县委", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委领导班子共事", "overlap_org": "中共南皮县委", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委领导班子共事", "overlap_org": "中共南皮县委", "overlap_period": "2022-"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县政府班子共事", "overlap_org": "南皮县人民政府", "overlap_period": "2024-"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县政府班子共事", "overlap_org": "南皮县人民政府", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "基层县委书记接受中共沧州市委领导", "overlap_org": "中共沧州市委/中共南皮县委", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 9, "type": "career_transfer", "context": "毕汝卫（原南皮书记）2026-07 报道转任沧州市海洋和港航管理局党组书记", "overlap_org": "南皮县委→沧州海航局", "overlap_period": "2026-07"},
    {"person_a": 7, "person_b": 9, "type": "cross_county_cross_layer", "context": "毕汝卫从沧县/黄骅/南皮县域基层升至市委机关（沧州政经圈层）", "overlap_org": "沧州市政经体系", "overlap_period": "2021-2026"},
    {"person_a": 7, "person_b": 10, "type": "superior_subordinate", "context": "前南皮请与沧州市委领导体系交集", "overlap_org": "沧州市", "overlap_period": "2021-2026"},
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

print("\n=== 南皮县 network build complete ===")
print(f"persons: {len(persons)}  orgs: {len(organizations)}  positions: {len(positions)}  relationships: {len(relationships)}")
print(f"DB:   {DB_PATH}")
print(f"GEXF: {GEXF_PATH}")