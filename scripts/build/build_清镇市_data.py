#!/usr/bin/env python3
"""清镇市领导班子关系网络 build script.

任务: guizhou_清镇市 (贵州省贵阳市清镇市, 县级市)
目标: 市委书记 & 市长
数据基准: 截至 2026-08-05
来源: 清镇市人民政府门户网站 www.gzqz.gov.cn 领导之窗（official, 2026-08-05 访问）
      + 清镇市融媒体中心 (www.gzqz.gov.cn/xwdt/xwzx/) 会议/报道（official）
运行: python3 data/tmp/guizhou_清镇市/build_清镇市_data.py
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build

# ── 目录（暂存区）────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "清镇市_network.db"
GEXF_PATH = STAGING / "清镇市_network.gexf"

# ════════════════════════════════════════════════════════════
# 人员 (persons)  — 现任以官方领导之窗为准
# 官方来源：https://www.gzqz.gov.cn/zwgk/ldzc/
# ════════════════════════════════════════════════════════════
persons = [
    # 1 现任市委书记
    {
        "id": 1,
        "name": "马骁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委书记",
        "current_org": "中共清镇市委员会",
        "source": "清镇市人民政府领导之窗-市委领导(2025-03-14 t20250320_87214474)",
    },
    # 2 现任市长（代市长/提名人选）
    {
        "id": 2,
        "name": "刘欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委副书记、市长提名人选（主持市政府工作）",
        "current_org": "清镇市人民政府",
        "source": "清镇市人民政府官网-市委领导(2026-07-03 t20260706_90588524);清镇市融媒体中心(2026-07-10/07-22)",
    },
    # 3 市委副书记
    {
        "id": 3,
        "name": "赵明镜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委副书记",
        "current_org": "中共清镇市委员会",
        "source": "清镇市人民政府官网-市委领导(2025-03 t20250320_87214472)",
    },
    # 4 市纪委书记
    {
        "id": 4,
        "name": "余睿",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1981年8月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、市纪委书记、市监委主任",
        "current_org": "中共清镇市纪律检查委员会",
        "source": "清镇市人民政府官网-市委领导(2025-03 t20250320_87214464)",
    },
    # 5 常务副市长
    {
        "id": 5,
        "name": "柯建峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年1月",
        "birthplace": "待查",
        "education": "管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、常务副市长（分管常务工作）",
        "current_org": "清镇市人民政府",
        "source": "清镇市人民政府官网-市委领导(2025-03 t20250320_87214601)",
    },
    # 6 宣传部部长
    {
        "id": 6,
        "name": "梁俊阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、市委宣传部部长、市委教育工委书记",
        "current_org": "中共清镇市委员会",
        "source": "清镇市人民政府官网-市委领导(2025-03 t20250320_87214643)",
    },
    # 7 统战部部长
    {
        "id": 7,
        "name": "唐庶佳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年7月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、市委统战部部长、市政协党组副书记",
        "current_org": "中共清镇市委员会",
        "source": "清镇市人民政府官网-市委领导(2025-03 t20250320_87214642)",
    },
    # 8 组织部部长
    {
        "id": 8,
        "name": "岳彬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、市委组织部部长",
        "current_org": "中共清镇市委员会",
        "source": "清镇市人民政府官网-市委领导(2025-03 t20250320_87214631)",
    },
    # 9 人武部政委
    {
        "id": 9,
        "name": "王兆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年7月",
        "birthplace": "待查",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、市人武部政委",
        "current_org": "清镇市人民武装部",
        "source": "清镇市人民政府官网-市委领导(2025-04 t20250421_87554833)",
    },
    # 10 政法委书记
    {
        "id": 10,
        "name": "张登军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年2月",
        "birthplace": "待查",
        "education": "大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、市委政法委书记",
        "current_org": "中共清镇市委员会",
        "source": "清镇市人民政府官网-市委领导(2025-09 t20250919_88632996)",
    },
    # 11 市委常委、副市长
    {
        "id": 11,
        "name": "彭松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市委常委、副市长",
        "current_org": "清镇市人民政府",
        "source": "清镇市人民政府官网-市委领导(2026-01 t20260107_89126593)",
    },
    # 12 市人大主任
    {
        "id": 12,
        "name": "廖梓阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年7月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市人大常委会党组书记、主任",
        "current_org": "清镇市人大常委会",
        "source": "清镇市人民政府官网-市人大领导(2025-03 t20250320_87215129)",
    },
    # 13 副市长
    {
        "id": 13,
        "name": "刘杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市人民政府副市长",
        "current_org": "清镇市人民政府",
        "source": "清镇市人民政府官网-市政府领导(2025-05 t20250507_87662208)",
    },
    # 14 副市长
    {
        "id": 14,
        "name": "冉依依",
        "gender": "女",
        "ethnicity": "仡佬族",
        "birth": "1985年",
        "birthplace": "待查",
        "education": "研究生学历，法学博士，民建会员",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "清镇市人民政府副市长",
        "current_org": "清镇市人民政府",
        "source": "清镇市人民政府官网-市政府领导(2025-03 t20250320_87213730)",
    },
    # 15 副市长
    {
        "id": 15,
        "name": "邓延旭",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1979年8月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市人民政府党组成员、副市长",
        "current_org": "清镇市人民政府",
        "source": "清镇市人民政府官网-市政府领导(2025-07 t20250714_88284781)",
    },
    # 16 副市长提名人选（公安局长）
    {
        "id": 16,
        "name": "王成刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清镇市人民政府副市长提名人选、市公安局局长提名人选",
        "current_org": "清镇市公安局",
        "source": "清镇市人民政府官网-市政府领导(2026-07 t20260724_90658493)",
    },
    # 17 市政协主席
    {
        "id": 17,
        "name": "吴筑蓉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年11月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协清镇市委员会主席、党组书记",
        "current_org": "政协清镇市委员会",
        "source": "清镇市人民政府官网-市政协领导(2025-03 t20250320_87213498)",
    },
    # 18 市政协副主席
    {
        "id": 18,
        "name": "王晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协清镇市委员会党组副书记、副主席",
        "current_org": "政协清镇市委员会",
        "source": "清镇市人民政府官网-市政协领导(2025-03 t20250320_87213497)",
    },
    # 19 前任市委书记
    {
        "id": 19,
        "name": "付涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任清镇市委书记（2023年在位，已离任）",
        "current_org": "",
        "source": "清镇市融媒体中心(2023 基层党建述职/巡察工作会议报道)",
    },
    # 20 前任市长
    {
        "id": 20,
        "name": "吴永康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任清镇市委副书记、市长（实则2026-06离任）",
        "current_org": "",
        "source": "清镇市融媒体中心(20260521/20260604 市政府党组会、常务会报道)",
    },
]

# ════════════════════════════════════════════════════════════
# 机构 (organizations)
# ════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1,
        "name": "中共清镇市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共贵阳市委员会",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 2,
        "name": "清镇市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "贵阳市人民政府",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 3,
        "name": "中共清镇市纪律检查委员会、清镇市监察委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共清镇市委员会",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 4,
        "name": "清镇市人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "清镇市",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议清镇市委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "清镇市",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 6,
        "name": "清镇市人民武装部",
        "type": "其它",
        "level": "县处级",
        "parent": "贵阳警备区",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 7,
        "name": "清镇市公安局",
        "type": "政府",
        "level": "县处级",
        "parent": "清镇市人民政府",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 8,
        "name": "贵州清镇经济开发区",
        "type": "开发区",
        "level": "省级",
        "parent": "清镇市",
        "location": "贵州省贵阳市清镇市",
    },
    {
        "id": 9,
        "name": "中共贵阳市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共贵州省委",
        "location": "贵州省贵阳市",
    },
    {
        "id": 10,
        "name": "贵阳市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "贵州省人民政府",
        "location": "贵州省贵阳市",
    },
]

# ════════════════════════════════════════════════════════════
# 任职 (positions)
# ════════════════════════════════════════════════════════════
positions = [
    # 马骁 (1)
    {"person_id": 1, "org_id": 1, "title": "清镇市委书记", "start_date": "2025（约）", "end_date": "present", "rank": "县处级正职", "note": "兼市人武部党委第一书记、贵州清镇经开区党工委书记；2025-03 官方简历在位，一级调研员"},
    {"person_id": 1, "org_id": 8, "title": "贵州清镇经济开发区党工委书记（兼）", "start_date": "2025（约）", "end_date": "present", "rank": "兼", "note": "官方简历标注兼任"},
    {"person_id": 1, "org_id": 6, "title": "清镇市人武部党委第一书记（兼）", "start_date": "2025（约）", "end_date": "present", "rank": "兼", "note": "官方简历标注兼任"},
    # 刘欢 (2)
    {"person_id": 2, "org_id": 2, "title": "清镇市委副书记、清镇市人民政府市长提名人选", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职", "note": "市人民政府党组书记、市长提名人选"},
    {"person_id": 2, "org_id": 8, "title": "贵州清镇经济开发区党工委副书记、管委会主任（兼，提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "兼", "note": "提名人选"},
    # 赵明镜 (3)
    {"person_id": 3, "org_id": 1, "title": "清镇市委副书记", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": ""},
    # 余睿 (4)
    {"person_id": 4, "org_id": 3, "title": "清镇市委常委、市纪委书记、市监委主任", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": "四级高级监察官"},
    # 柯建峰 (5)
    {"person_id": 5, "org_id": 2, "title": "清镇市委常委、常务副市长（市政府党组副书记）", "start_date": "2025", "end_date": "present", "rank": "副处级", "note": "分管常务工作"},
    # 梁俊阳 (6)
    {"person_id": 6, "org_id": 1, "title": "清镇市委常委、市委宣传部长、市委教育工委书记", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": ""},
    # 唐庶佳 (7)
    {"person_id": 7, "org_id": 1, "title": "清镇市委常委、市委统战部长、市政协党组副书记", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": "兼市社会主义学校校长"},
    # 岳彬 (8)
    {"person_id": 8, "org_id": 1, "title": "清镇市委常委、市委组织部长、市委党校校长(兼)", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": ""},
    # 王兆 (9)
    {"person_id": 9, "org_id": 6, "title": "清镇市委常委、市人武部政委", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": ""},
    # 张登军 (10)
    {"person_id": 10, "org_id": 1, "title": "清镇市委常委、市委政法委书记", "start_date": "2025-09", "end_date": "present", "rank": "县处级", "note": "市法学会第一届理事会会长"},
    # 彭松 (11)
    {"person_id": 11, "org_id": 2, "title": "清镇市委常委、副市长", "start_date": "2026-01", "end_date": "present", "rank": "副处级", "note": "三级调研员"},
    # 廖梓阳 (12)
    {"person_id": 12, "org_id": 4, "title": "清镇市人大常委会党组书记、主任", "start_date": "2025", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 刘杰 (13)
    {"person_id": 13, "org_id": 2, "title": "清镇市人民政府副市长", "start_date": "2025-05", "end_date": "present", "rank": "副处级", "note": ""},
    # 冉依依 (14)
    {"person_id": 14, "org_id": 2, "title": "清镇市人民政府副市长", "start_date": "2025-03", "end_date": "present", "rank": "副处级", "note": "民建会员"},
    # 邓延旭 (15)
    {"person_id": 15, "org_id": 2, "title": "清镇市人民政府党组成员、副市长", "start_date": "2025-07", "end_date": "present", "rank": "副处级", "note": ""},
    # 王成刚 (16)
    {"person_id": 16, "org_id": 2, "title": "清镇市人民政府副市长（提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "副市长提名人选"},
    {"person_id": 16, "org_id": 7, "title": "清镇市公安局局长（提名人选）", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "提名人选"},
    # 吴筑蓉 (17)
    {"person_id": 17, "org_id": 5, "title": "政协清镇市委员会主席、党组书记", "start_date": "2025", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 王晓东 (18)
    {"person_id": 18, "org_id": 5, "title": "政协清镇市委员会党组副书记、副主席", "start_date": "2025", "end_date": "present", "rank": "副处级", "note": ""},
    # 付涛 (19) 前任书记
    {"person_id": 19, "org_id": 1, "title": "清镇市委书记（前任）", "start_date": "2023", "end_date": "2024/2025", "rank": "县处级正职", "note": "2023年在位，2024-2025年间离任（去向待查）"},
    # 吴永康 (20) 前任市长
    {"person_id": 20, "org_id": 2, "title": "清镇市委副书记、市长（前任）", "start_date": "2023", "end_date": "2026-06", "rank": "县处级正职", "note": "2026-06 仍在位；2026-07 刘欢接任"},
]

# ════════════════════════════════════════════════════════════
# 关系 (relationships)
# ════════════════════════════════════════════════════════════
relationships = [
    # 党政搭班子（现任核心）
    {"person_a": 1, "person_b": 2, "type": "党政搭班子", "context": "市委书记与市长（提名人选）构成党政一把手班子", "overlap_org": "中共清镇市委、清镇市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记—专职副书记同班", "overlap_org": "中共清镇市委员会", "overlap_period": "2025—present"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "市委书记—人大主任四家班子", "overlap_org": "清镇市四家班子", "overlap_period": "2025—present"},
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "市委书记—政协主席四家班子", "overlap_org": "清镇市四家班子", "overlap_period": "2025—present"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记—市纪委书记同班/一岗双责", "overlap_org": "中共清镇市委员会", "overlap_period": "2025—present"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委书记—组织部长（干部工作）", "overlap_org": "中共清镇市委员会", "overlap_period": "2025—present"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委书记—政法委书记", "overlap_org": "中共清镇市委员会", "overlap_period": "2025—present"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长（代）—常务副市长（市政府党组副书记）同政府班子", "overlap_org": "清镇市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "市长（代）—副市长同政府班子", "overlap_org": "清镇市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "市长（代）—副市长（民建）同政府班子", "overlap_org": "清镇市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "市长（代）—副市长同政府班子", "overlap_org": "清镇市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 5, "person_b": 13, "type": "overlap", "context": "常务副市长—副市长同政府班子", "overlap_org": "清镇市人民政府", "overlap_period": "2026—present"},
    {"person_a": 16, "person_b": 2, "type": "overlap", "context": "公安局长提名人选—市长（代）同政府班子", "overlap_org": "清镇市人民政府", "overlap_period": "2026-07—present"},
    # 前任-继任
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "马骁接替付涛任清镇市委书记（前/继任）", "overlap_org": "中共清镇市委员会", "overlap_period": "2024/2025 交接"},
    {"person_a": 2, "person_b": 20, "type": "predecessor_successor", "context": "刘欢接替吴永康任清镇市长（前/继任）", "overlap_org": "清镇市人民政府", "overlap_period": "2026-06/07 交接"},
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "市委书记—市长吴永康党政搭班子（2025-2026上半年）", "overlap_org": "清镇市四家班子", "overlap_period": "2025—2026-06"},
    {"person_a": 19, "person_b": 20, "type": "overlap", "context": "前任书记付涛—前任市长吴永康党政搭班子", "overlap_org": "清镇市四家班子", "overlap_period": "2023—2024"},
    {"person_a": 3, "person_b": 20, "type": "overlap", "context": "专职副书记赵明镜与前市长吴永康同班", "overlap_org": "中共清镇市委员会", "overlap_period": "2025—2026-06"},
]


def main() -> None:
    run_build(
        slug="清镇市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")
    conn.close()


if __name__ == "__main__":
    main()