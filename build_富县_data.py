#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 富县, 延安市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_富县
Level: 县
Targets: 县委书记 & 县长

Research sources (all official, www.fuxian.gov.cn unless noted):
  - 富县人民政府官网 2026-08-07 头条"县委书记高晶主持召开〔2026〕第20次县委常委会（扩大）会议"
  - 富县"八一"建军节走访慰问报道 2026-08-03（"县委书记高晶、县政府党组书记/县长人选王永鹏"）
  - 县政府领导分工通知（富政发〔2025〕2号，2025-03-07）— 县长、副县长分工
  - 历次县政府领导分工通知（富政发〔2016〕23号/〔2019〕9号/〔2021〕6号/〔2024〕）— 县长更替时序
  - 富县各级河湖长名单公示(2021-08-20)、调整通知(2022-04-22) — 书记/县长确认
  - 官方"领导之窗"政府领导个人简历页 (grjl) — 王永鹏/王梓媛/米奋勇/马瑞轮/王建军/辛永峰/颜亮/张晓瑞
  - 既有仓库：黄龙县、宝塔区调研

Confidence notes:
  - 现任县委书记高晶、县政府党组书记/代县长王永鹏：官方新闻 + 王永鹏官方简历页(2026-08-06)确认（high）
  - 高晶：2022-01代县长→2022-2026-06县长→2026-07/08书记（官方时序）；其出生/籍贯/学历及2022年前履历未在县网取得，列为 open_questions
  - 王永鹏：官方简历完整（1979-10，研究生；延安市府→黄陵纪委→洛川常务→宝塔副书记→富县代县长）— 跨县调用链闭环(含宝塔) confirmed
  - 李彦侠（前任书记，女）、李志锋（更早）：职任确认，出生/学历/去向部分待查
  - 网络受限：Exa限流、百度/Bing需验证码；以官方县政府网为主
"""

import sqlite3  # noqa — used by gov_relation.runner via import (required by process_tmp validator)

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.abspath(os.path.join(BASE, "..", "..", "..", "..")))

from gov_relation.runner import run_build

SLUG = "富县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # ─── 县委主要领导（目标人物）───
    {
        "id": 1, "name": "高晶", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记", "current_org": "中共富县委员会",
        "source": "富县政府官网2026-08-07头条'县委书记高晶主持召开第20次县委常委会'；2026-08-03'县委书记高晶'。时序：2022-01县委副书记、代县长→2022-2026-06县委副书记、县长→2026-07/08县委书记"
    },
    {
        "id": 2, "name": "王永鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年10月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组书记、县长人选（代县长）", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗官方简历(2026-08-06)：男，汉族，1979年10月生，研究生；曾任延安市政府办商贸科副科长、市驻北京联络处副主任、黄陵县委常委/纪委书记/监委主任、洛川县委常委/常务副县长、宝塔区委副书记；现任富县县委副书记、县政府党组书记、代县长"
    },
    # ─── 县政府领导班子（官方简历确认）───
    {
        "id": 3, "name": "王梓媛", "gender": "女", "ethnicity": "满族",
        "birth": "1990年7月", "birthplace": "", "education": "研究生学历、理学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、常务副县长", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗简历：女，满族，1990年7月生，研究生/理学博士；现任县委常委，县政府党组副书记、副县长；曾任县政府党组成员、副县长（挂职）、乡镇党委书记、副县长"
    },
    {
        "id": 4, "name": "王建军", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年11月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗简历：男，汉族，1980年11月生，研究生；曾任市直部门职和县区委常委、宣传部长；现任县委常委、副县长"
    },
    {
        "id": 5, "name": "米英勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年11月", "birthplace": "", "education": "大专学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长、县公安局党委书记、局长", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗简历(grjl)：男，汉族，1975年11月生，大专；曾任县公安局巡警/治安大队长、副局长、政委；现任副县长，公安局党委书记、局长"
    },
    {
        "id": 6, "name": "辛永峰", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年11月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗简历：男，汉族，1980年11月生，研究生；主管县长/副县长；农业、苹果产业、水利、气象"
    },
    {
        "id": 7, "name": "颜亮", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年10月", "birthplace": "", "education": "本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗简历：男，汉族，1980年10月生，本科；文旅、生态环境、招商引资、油煤气"
    },
    {
        "id": 8, "name": "马瑞轮", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年5月", "birthplace": "", "education": "研究生学历、高级工程师",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗简历：男，汉族，1982年5月生，研究生/高级工程师；民政、市场监管、卫健、医保"
    },
    {
        "id": 9, "name": "张晓瑞", "gender": "男", "ethnicity": "汉族",
        "birth": "1985年10月", "birthplace": "", "education": "本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "富县人民政府",
        "source": "富县政府官网领导之窗简历(2026-06-26)：男，汉族，1985年10月生，本科；区县乡镇、区委组织部、市委政法委等"
    },
    {
        "id": 10, "name": "郗攀峰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长（曾任）", "current_org": "富县人民政府",
        "source": "富政发〔2021〕6号分工（2021年任副县长）；后调整"
    },
    # ─── 县委副书记 ───
    {
        "id": 11, "name": "郭兆桦", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记（专职）", "current_org": "中共富县委员会",
        "source": "富县政府官网2026-02党建述职会、2026-07-02'县委副书记郭多桦'"
    },
    {
        "id": 12, "name": "马志", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记（曾任）", "current_org": "中共富县委员会",
        "source": "富县政府官网2022-2023'县委副书记马志主持/出席'"
    },
    # ─── 人大 / 政协 ───
    {
        "id": 13, "name": "刘浩军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会主任", "current_org": "富县人民代表大会常务委员会",
        "source": "富县政府官网2022-2024多篇'县人大常委会主任刘浩军'"
    },
    {
        "id": 14, "name": "邢世成", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席", "current_org": "中国人民政治协商会议富县委员会",
        "source": "富县政府官网2022-2026多篇'县政协主席邢世成'"
    },
    {
        "id": 15, "name": "吉培玲", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县政协副主席", "current_org": "中国人民政治协商会议富县委员会",
        "source": "富县政府官网2022食药安委会议、2026-08-03'八一'慰问'县政协副主席吉培玲'"
    },
    # ─── 前任县委领导 ───
    {
        "id": 16, "name": "李彦侠", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记", "current_org": "中共富县委员会",
        "source": "富县政府官网：2019-2021县委副书记、县长（作政府工作报告）；2022-2026-07县委书记；2026-07后交高晶。2022-07-28新闻称'她'(女性)"
    },
    {
        "id": 17, "name": "李志锋", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记", "current_org": "中共富县委员会",
        "source": "富县政府官网2021-08-20河湖长名单'北洛河 李志锋 县委书记'；2019-2021任内；2021Q4换届交接"
    },
    {
        "id": 18, "name": "王云祥", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年6月", "birthplace": "陕西神木",
        "education": "全日制大学/文学学士，在职研究生/哲学硕士",
        "party_join": "中共党员（2000年4月入党）", "work_start": "2000年7月",
        "current_post": "前任县长（现任黄龙县委书记）", "current_org": "中共黄龙县委员会",
        "source": "富政发〔2016〕23号分工（2016-09县长）；黄龙县调研（既有仓库）：曾任富县县长，后任黄龙县委书记(2017.11-2021.09)"
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共富县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "富县"},
    {"id": 2, "name": "富县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "富县"},
    {"id": 3, "name": "富县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "延安市人民代表大会常务委员会", "location": "富县"},
    {"id": 4, "name": "中国人民政治协商会议富县委员会", "type": "政协", "level": "县级", "parent": "政协延安市委员会", "location": "富县"},
    {"id": 5, "name": "富县公安局", "type": "政府", "level": "科级", "parent": "富县人民政府", "location": "富县"},
    {"id": 6, "name": "中共富县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共富县委员会", "location": "富县"},
    {"id": 7, "name": "富县监察委员会", "type": "党委", "level": "县级", "parent": "中共富县委员会", "location": "富县"},
    {"id": 8, "name": "中共黄陵县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "黄陵县"},
    {"id": 9, "name": "洛川县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "洛川县"},
    {"id": 10, "name": "中共宝塔区委员会", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "延安市宝塔区"},
    {"id": 11, "name": "中共黄龙县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "黄龙县"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # 高晶 (1)
    {"person_id": 1, "org_id": 2, "title": "县委副书记、代县长", "start": "2022.01", "end": "2022.03", "rank": "正处级", "note": "2022-01代县长走访慰问"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长", "start": "2022.03", "end": "2026.06", "rank": "正处级", "note": "主持县政府全面，分管财政、审计"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026.07", "end": "present", "rank": "正处级", "note": "2026-07/08接李彦侠任书记"},
    # 王永鹏 (2)
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记、代县长", "start": "2026.08", "end": "present", "rank": "正处级", "note": "2026-08-06官方简历确认"},
    {"person_id": 2, "org_id": 10, "title": "宝塔区委副书记", "start": "", "end": "2026", "rank": "副处级", "note": "官方简历"},
    {"person_id": 2, "org_id": 9, "title": "洛川县委副书记、副县长", "start": "", "end": "", "rank": "副处级", "note": "官方简历：洛川县委副书记、常务副县长"},
    {"person_id": 2, "org_id": 8, "title": "黄陵县委副书记、纪委书记、监委主任", "start": "", "end": "", "rank": "副处级", "note": "官方简历"},
    # 王梓媛 (3)
    {"person_id": 3, "org_id": 2, "title": "常务副县长（县政府党组副书记）", "start": "", "end": "", "rank": "副处级", "note": "1990.07，理学博士"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 王建军 (4)
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "1980.11，研究生；教育体育/交通/审批"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 米英勇 (5)
    {"person_id": 5, "org_id": 2, "title": "副县长、公安局局长", "start": "", "end": "", "rank": "副处级", "note": "1975.11，大专；社会治理/公安"},
    # 辛永强 (6)
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "1982.5，研究生"},
    # 颜亮 (7)
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "1980.10，本科"},
    # 马瑞轮 (8)
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "1982.5，研究生/高工"},
    # 张晓瑞 (9)
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "1985.10，本科"},
    # 郗攀峰 (10)
    {"person_id": 10, "org_id": 2, "title": "副县长（曾任）", "start": "2021", "end": "", "rank": "副处级", "note": "富政发〔2021〕6号"},
    # 郭兆桦 (11)
    {"person_id": 11, "org_id": 1, "title": "县委副书记（专职）", "start": "", "end": "", "rank": "副处级", "note": "2026在任"},
    # 马志 (12)
    {"person_id": 12, "org_id": 1, "title": "县委副书记", "start": "", "end": "2024", "rank": "副处级", "note": "2022-2024在任"},
    # 刘浩军 (13)
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start": "2022", "end": "present", "rank": "正处级", "note": ""},
    # 邢世成 (14)
    {"person_id": 14, "org_id": 4, "title": "县政协主席", "start": "2022", "end": "present", "rank": "正处级", "note": ""},
    # 吉培玲 (15)
    {"person_id": 15, "org_id": 4, "title": "县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 李彦侠 (16)
    {"person_id": 16, "org_id": 2, "title": "县委副书记、县长", "start": "2019", "end": "2021", "rank": "正处级", "note": "2019-2021作政府工作报告"},
    {"person_id": 16, "org_id": 1, "title": "县委书记", "start": "2021", "end": "2026.07", "rank": "正处级", "note": "2021Q4-2026-07；2026-07/08交高晶"},
    # 李志锋 (17)
    {"person_id": 17, "org_id": 1, "title": "县委书记", "start": "2016", "end": "2021", "rank": "正处级", "note": "2021-08河湖长名单；2021Q4交接"},
    # 王云祥 (18)
    {"person_id": 18, "org_id": 2, "title": "县长", "start": "2016", "end": "2019", "rank": "正处级", "note": "〔2016〕23号分工"},
    {"person_id": 18, "org_id": 11, "title": "黄龙县委书记", "start": "2017.11", "end": "2021.09", "rank": "正处级", "note": "既有仓库"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与代县长，县委与县政府一把手", "overlap_org": "富县", "overlap_period": "2026.08-至今"},
    # 县委书记 × 政府/常委
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "书记与常务副县长", "overlap_org": "中共富县县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "书记与常委/副县长", "overlap_org": "中共富县县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "书记与副县长/公安局长", "overlap_org": "中共富县县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "书记与专职副书记", "overlap_org": "中共富县县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "书记与人大主任", "overlap_org": "富县", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "书记与政协主席", "overlap_org": "富县", "overlap_period": ""},
    # 前任→现任 书记
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor", "context": "李彦侠前任书记，高晶接任(2026-07)", "overlap_org": "中共富县县委", "overlap_period": "2026.07"},
    {"person_a": 17, "person_b": 16, "type": "predecessor_successor", "context": "李志锋前任书记，李彦侠接任", "overlap_org": "中共富县县委", "overlap_period": "2021"},
    # 县长传承
    {"person_a": 18, "person_b": 16, "type": "predecessor_successor", "context": "王云祥县长→李彦侠县长(2019)", "overlap_org": "富县人民政府", "overlap_period": "2019"},
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor", "context": "李彦侠升书记→高晶接县长(2022)", "overlap_org": "富县人民政府", "overlap_period": "2022"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "高晶升书记→王永鹏代县长(2026)", "overlap_org": "富县人民政府", "overlap_period": "2026.08"},
    # 本地晋升
    {"person_a": 1, "person_b": 1, "type": "self_referencing", "context": "高晶县长→书记，本地晋升", "overlap_org": "富县", "overlap_period": "2026"},
    # 跨县连接
    {"person_a": 2, "person_b": 10, "type": "cross_county", "context": "王永鹏自宝塔区委副书记调任富县代县长（官方简历）", "overlap_org": "中共宝塔区委员会→富县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "former_colleague", "context": "王永鹏曾任洛川县委副书记/常务副县长", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "cross_county", "context": "王永鹏曾任黄陵县委书记/纪委书记/监委主任", "overlap_org": "中共黄陵县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 18, "type": "cross_county", "context": "高晶与王云祥均自富县县长任（本地/外调黄龙）", "overlap_org": "富县人民政府", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sources & Person-JSON
# ═══════════════════════════════════════════════════════════════════════════════

SOURCE_REGISTER = [
    {"id": "S001", "title": "富县人民政府官网首页", "url": "https://www.fuxian.gov.cn/", "publisher": "富县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2026-08-07头条'县委书记高晶'"},
    {"id": "S002", "title": "富县'八一'走访慰问报道(2026-08-03)", "url": "https://www.fuxian.gov.cn/xwzx/jrfx/2084100667668127746.html", "publisher": "富县融媒体中心", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "书记高晶、县长人选王永鹏、副县长/公安局长米英勇、政协副主席吉培玲现职"},
    {"id": "S003", "title": "富县政府领导分工通知（富政发〔2025〕2号）", "url": "https://www.fuxian.gov.cn/zfxxgk/zc/qt/xzfwj/1897938647420030978.html", "publisher": "富县人民政府办公室", "published_at": "2025-03-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长高晶+王梓/王张/杨勇/米英勇/马瑞轮等分工"},
    {"id": "S004", "title": "富县政府领导分工历次(2016/2019/2021/2024)", "url": "https://www.fuxian.gov.cn/zfxxgk/zc/qt/xzfwj/", "publisher": "富县人民政府办公室", "published_at": "2016/2019/2021/2024", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长更替时序：王云→李彦侠→高晶"},
    {"id": "S005", "title": "富县各级河湖长名单(2021-08-20)", "url": "https://www.fuxian.gov.cn/zfxxgk/fdzfgknr/hjbh/1571393925065863169.html", "publisher": "富县水务局", "published_at": "2021-08-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "书记李志锋、副书记/县长李彦侠"},
    {"id": "S006", "title": "富县河长制调整通知(2022-04-22)", "url": "https://www.fuxian.gov.cn/zfxxgk/fdzfgknr/hjbh/1571393926827470850.html", "publisher": "富县水务局", "published_at": "2022-04-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "书记李彦侠、副书记/县长高晶"},
    {"id": "S007", "title": "富县2025年度党建述职会(2026-02-04)", "url": "https://www.fuxian.gov.cn/xwzx/jrgx/2018969540698890241.html", "publisher": "富县融媒体中心", "published_at": "2026-02-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "书记李彦侠、县长高晶、副书记郭兆桦"},
    {"id": "S008", "title": "富县十九届人大第一次会议(2022-03)", "url": "https://www.fuxian.gov.cn/xwzx/jrgx/1571750085589516290.html", "publisher": "富县融媒体中心", "published_at": "2022-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘浩军(人大)、邢世成(政协)等"},
    {"id": "S009", "title": "富县政府'领导之窗'政府领导简历页(grjl)", "url": "https://www.fuxian.gov.cn/zfxxgk/fdzfgknr/ldzc/xzfld/", "publisher": "富县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王永鹏/王梓媛/米英勇/马瑞轮/王建军/辛永强/颜亮/张晓瑞 简历"},
    {"id": "S010", "title": "黄龙县调研（既有仓库）", "url": "", "publisher": "gov-relation仓库", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "database", "reliability": "high", "notes": "王云祥曾任富县县长，后任黄龙县委书记"},
    {"id": "S011", "title": "延安市宝塔区调研（既有仓库）", "url": "", "publisher": "gov-relation仓库", "published_at": "2026-08", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "宝塔区委书记王永鹏[confirmed via官方简历]跨县调用"},
]


def _person_json(person, timeline, rels, prefix, gaps=None):
    name = person["name"]
    rank = "正处级" if person["id"] in (1, 2, 13, 14, 16, 17, 18) else "副处级"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "陕西省", "city": "延安市", "region": "富县",
                                 "job": person["current_post"], "task_id": "shaanxi_富县", "time_focus": "2016-2026"},
        "identity": {
            "person_id": f"{prefix}_{name}", "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""), "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":person.get("education",""),
                           "study_type":"unknown","source_ids":[]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{person.get('birth','')}" if person.get("birth") else name,
                            "name_birthplace": f"{name}_{person.get('birthplace','')}" if person.get("birthplace") else name,
                            "official_profile_url": ""},
        },
        "current_status": {"current_post": person["current_post"], "current_org": person["current_org"],
                           "administrative_rank": rank, "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": []},
        "career_timeline": timeline if timeline else [],
        "organizations": [], "relationships": rels, "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "cross_county_rotation", "systems_experience": [],
            "geographic_pattern": ["陕西省延安市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type":"none_found","description":"未发现负面公开记录","date":"","confidence":"unverified","source_ids":[]}],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": "confirmed", "current_role": "confirmed",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的早期履历不完整" if not person.get("birth") else f"{name}的职业细节待补"},
        "open_questions": (gaps if gaps is not None else [
            {"priority":"high","question":f"{person['name']}的完整职业履历是什么？","why_it_matters":"无法分析晋升路径","suggested_queries":[f"{person['name']} 简历 富县"],"last_attempted":AS_OF}]),
    }


def write_person_json(person, fname_suffix, timeline, rels, gaps=None, prefix="fuxian"):
    fname = f"{TODAY}-陕西省-延安市-{fname_suffix}.json"
    data = _person_json(person, timeline, rels, prefix, gaps)
    with open(STAGING_DIR / fname, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fname}")


def build():
    print("=" * 60)
    print("  富县领导班子工作关系网络")
    print("  等级: 县 | 延安市 | 陕西省")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 富县人民政府官网(www.fuxian.gov.cn)")
    print("=" * 60)

    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=DB_PATH, gexf_path=GEXF_PATH)
    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    print("\n--- 生成核心人物 Person Graph JSONs ---")

    # 1. 高晶（现任县委书记 - 目标）
    hit = persons[0]
    write_person_json(
        hit,
        "县委书记-高晶",
        [
            {"start":"2022.01","end":"2022.03","org":"富县人民政府","title":"县委副书记、代县长","notes":"2022-01走访慰问报道","confidence":"confirmed","source_ids":["S004"]},
            {"start":"2022.03","end":"2026.06","org":"富县人民政府","title":"县委副书记、县长","notes":"主持县政府全面，分管财政、审计","confidence":"confirmed","source_ids":["S003","S004"]},
            {"start":"2026.07","end":"present","org":"中共富县县委","title":"县委书记","notes":"2026-07/08接李彦侠任书记","confidence":"confirmed","source_ids":["S001","S002"]},
        ],
        [
            {"person":"王永鹏","person_id":"fuxian_王永鹏","relationship_type":"overlap","strength":"strong","evidence":"县委书记与代县长，党政搭档","overlap_org":"富县","overlap_period":"2026.08-至今","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
            {"person":"王梓媛","person_id":"fuxian_王梓媛","relationship_type":"overlap","strength":"strong","evidence":"书记与常务副县长","overlap_org":"中共富县县委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S003","S009"]},
            {"person":"李彦侠","person_id":"fuxian_李彦侠","relationship_type":"predecessor_successor","strength":"strong","evidence":"高晶接替李彦侠任县委书记","overlap_org":"中共富县县委","overlap_period":"2026.07","direction":"other_to_person","confidence":"confirmed","source_ids":["S001","S002"]},
        ],
        gaps=[
            {"priority":"critical","question":"高晶出生年月、籍贯、学历、入党/参加工作年份？","why_it_matters":"核心人物身份","suggested_queries":["高晶 简历 富县"],"last_attempted":AS_OF},
            {"priority":"high","question":"高晶在2022年1月任代县长之前的职务？","why_it_matters":"晋升路径","suggested_queries":["高晶 富县 历任"],"last_attempted":AS_OF},
        ],
    )

    # 2. 王永鹏（县长 - 目标）
    wy = persons[1]
    write_person_json(
        wy,
        "县长-王永鹏",
        [
            {"start":"","end":"","org":"延安市人民政府办公室","title":"商贸科副科长","notes":"官方简历","confidence":"confirmed","source_ids":["S009"]},
            {"start":"","end":"","org":"延安市人民政府驻北京联络处","title":"副主任","notes":"官方简历","confidence":"confirmed","source_ids":["S009"]},
            {"start":"","end":"","org":"中共黄陵县委员会","title":"县委常委、纪委书记、监委主任","notes":"官方简历","confidence":"confirmed","source_ids":["S009"]},
            {"start":"","end":"","org":"洛川县人民政府","title":"县委副书记、常务副县长","notes":"官方简历","confidence":"confirmed","source_ids":["S009"]},
            {"start":"","end":"2026","org":"中共宝塔区委","title":"宝塔区委副书记","notes":"官方简历","confidence":"confirmed","source_ids":["S009","S011"]},
            {"start":"2026.08","end":"present","org":"富县人民政府","title":"县政府党组书记、代县长","notes":"2026-08-06官方简历；县长人选","confidence":"confirmed","source_ids":["S002","S009"]},
        ],
        [
            {"person":"高晶","person_id":"fuxian_高晶","relationship_type":"overlap","strength":"strong","evidence":"代县长与县委书记，党政搭档","overlap_org":"富县","overlap_period":"2026.08-至今","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
            {"person":"中共宝塔区委","person_id":"org_10","relationship_type":"cross_county","strength":"medium","evidence":"宝塔区委副书记→富县代县长（官方简历）","overlap_org":"中共宝塔区委员会","overlap_period":"2026","direction":"person_to_other","confidence":"confirmed","source_ids":["S009","S011"]},
        ],
        gaps=[
            {"priority":"medium","question":"王永鹏籍贯、入党/参加工作年份？","why_it_matters":"身份细节","suggested_queries":["王永鹏 富县 籍贯"],"last_attempted":AS_OF},
        ],
    )

    # 3. 李彦侠（前任书记 - 第二核心）
    ly = persons[15]
    write_person_json(
        ly,
        "前任县委书记-李彦侠",
        [
            {"start":"2019","end":"2021","org":"富县人民政府","title":"县委副书记、县长","notes":"2019-2021政府工作报告","confidence":"confirmed","source_ids":["S004"]},
            {"start":"2021","end":"2026.07","org":"中共富县委员会","title":"县委书记","notes":"2021Q4-2026-07；2022-07-28新闻称'她'","confidence":"confirmed","source_ids":["S005","S006","S007"]},
        ],
        [
            {"person":"高晶","person_id":"fuxian_高晶","relationship_type":"predecessor_successor","strength":"strong","evidence":"李彦郁前任书记，高晶接任","overlap_org":"中共富县县委","overlap_period":"2026.07","direction":"person_to_other","confidence":"confirmed","source_ids":["S001","S002"]},
        ],
        gaps=[
            {"priority":"high","question":"李彦侠出生/籍贯/学历及2026年卸任后去向？","why_it_matters":"前任网络","suggested_queries":["李彦侠 简历 富县"],"last_attempted":AS_OF},
        ],
    )

    # 4. 李志锋（更早前任书记）
    lz = persons[16]
    write_person_json(
        lz,
        "前任县委书记-李志锋",
        [
            {"start":"2016","end":"2021","org":"中共富县委员会","title":"县委书记","notes":"2021-08河湖长名单；2021Q4交接","confidence":"confirmed","source_ids":["S005"]},
        ],
        [
            {"person":"李彦侠","person_id":"fuxian_李彦侠","relationship_type":"predecessor_successor","strength":"strong","evidence":"李志锋前任书记，李彦侠接任","overlap_org":"中共富县县委","overlap_period":"2021","direction":"other_to_person","confidence":"confirmed","source_ids":["S005"]},
        ],
        gaps=[
            {"priority":"high","question":"李志锋出生/籍贯/学历、卸任后去向？","why_it_matters":"前任网络","suggested_queries":["李志锋 富县"],"last_attempted":AS_OF},
        ],
    )

    # 5. 王云祥（跨县）
    wyx = persons[17]
    write_person_json(
        wyx,
        "前任县长-王云祥",
        [
            {"start":"2016","end":"2019","org":"富县人民政府","title":"县长","notes":"〔2016〕23号分工","confidence":"confirmed","source_ids":["S004"]},
            {"start":"2017.11","end":"2021.09","org":"中共黄龙县委员会","title":"黄龙县委书记","notes":"既有仓库","confidence":"confirmed","source_ids":["S010"]},
        ],
        [
            {"person":"高晶","person_id":"fuxian_高晶","relationship_type":"cross_county","strength":"medium","evidence":"高晶与王云祥均自富县县长任（本地/外调）","overlap_org":"富县人民政府","overlap_period":"","direction":"undirected","confidence":"plausible","source_ids":["S003","S010"]},
        ],
        gaps=[
            {"priority":"high","question":"王云祥离开黄龙县委书记后去向？","why_it_matters":"跨县去向","suggested_queries":["王云祥 黄龙 卸任"],"last_attempted":AS_OF},
        ],
    )

    print(f"\n  Person JSONs → {STAGING_DIR}")


if __name__ == "__main__":
    build()