#!/usr/bin/env python3
"""
Build 赣县区 (Ganxian District, 赣州市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

赣县区 is a district of 赣州市, Jiangxi Province. It was historically 赣县
(county) and was converted to 赣县区 (Ganxian District) in 2016.
Current as of: 2026-07-15

Targets: 区委书记 & 区长
Core figures: 廖永平 (区委书记), 刘文彦 (区委副书记、区长)

Notes:
- Data sourced primarily from ganzhou.gov.cn public reports and
  build_ganzhou_remaining_data.py (last updated ca. 2025-2026).
- Detailed career timelines and deputy rosters are incomplete pending
  direct access to www.ganxian.gov.cn (site behind WAF).
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "赣县区_network.db")
GEXF_PATH = os.path.join(BASE, "赣县区_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "廖永平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-07",
        "birthplace": "江西宁都",
        "education": "大学学历/MPA",
        "party_join": "1993-12",
        "work_start": "1992-08",
        "current_post": "赣县区委书记",
        "current_org": "中共赣县区委员会",
        "source": "build_ganzhou_remaining_data.py (compiled from ganzhou.gov.cn); https://www.ganxian.gov.cn (WAF-blocked)",
    },
    {
        "id": 2,
        "name": "刘文彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "江西宁都",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委副书记、区长",
        "current_org": "赣县区人民政府",
        "source": "build_ganzhou_remaining_data.py (compiled from ganzhou.gov.cn)",
    },
    # ── Predecessors ────────────────────────────────────────────────────
    # Predecessor 区委书记: 胡晓平 was 赣县区委书记 before 廖永平
    # Predecessor 区长: 张景霖 was 赣县区长 before 刘文彦
    {
        "id": 3,
        "name": "胡晓平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-12",
        "birthplace": "江西信丰",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣州市人大常委会副主任（原赣县区委书记）",
        "current_org": "赣州市人大常委会",
        "source": "公开报道; 胡晓平于2016-2020任赣县区委书记（撤县设区后首任书记）",
    },
    {
        "id": 4,
        "name": "张景霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-09",
        "birthplace": "江西崇义",
        "education": "中央党校大学学历",
        "party_join": "1992-03",
        "work_start": "1988-08",
        "current_post": "赣州市政协副主席（原赣县区长/赣县县长）",
        "current_org": "赣州市政协",
        "source": "公开报道; 张景霖2011-2021任赣县县长/赣县区长",
    },
    # ── Key deputies: 区委常委、副区长 ─────────────────────────────────
    # Note: The following deputies' data is partially inferred from
    # public news reports mentioning their participation in 赣县区 events.
    # Data quality: plausible (from media reports) — not verified from
    # the official leadership page (www.ganxian.gov.cn blocked).
    {
        "id": 5,
        "name": "赖卫国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委副书记",
        "current_org": "中共赣县区委员会",
        "source": "赣县区新闻报道; ganzhou.gov.cn",
    },
    {
        "id": 6,
        "name": "罗理强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委常委、常务副区长",
        "current_org": "赣县区人民政府",
        "source": "赣县区新闻报道",
    },
    {
        "id": 7,
        "name": "刘桂健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委常委、纪委书记、监委主任",
        "current_org": "中共赣县区纪律检查委员会",
        "source": "赣县区新闻报道",
    },
    {
        "id": 8,
        "name": "黄桂昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委常委、组织部长",
        "current_org": "中共赣县区委组织部",
        "source": "赣县区新闻报道",
    },
    {
        "id": 9,
        "name": "邓永明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委常委、宣传部部长",
        "current_org": "中共赣县区委宣传部",
        "source": "赣县区新闻报道",
    },
    {
        "id": 10,
        "name": "陈铁军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委常委、政法委书记",
        "current_org": "中共赣县区委政法委员会",
        "source": "赣县区新闻报道",
    },
    {
        "id": 11,
        "name": "肖桂香",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区委常委（人武部）",
        "current_org": "赣县区人武部",
        "source": "赣县区新闻报道",
    },
    # ── 副区长 ──────────────────────────────────────────────────────────
    {
        "id": 12,
        "name": "肖云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区副区长",
        "current_org": "赣县区人民政府",
        "source": "赣县区新闻报道",
    },
    {
        "id": 13,
        "name": "刘震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区副区长、市公安局赣县分局局长",
        "current_org": "赣县区人民政府/市公安局赣县分局",
        "source": "赣县区新闻报道",
    },
    {
        "id": 14,
        "name": "左旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区副区长",
        "current_org": "赣县区人民政府",
        "source": "赣县区新闻报道",
    },
    # ── 其他区领导 ──────────────────────────────────────────────────────
    {
        "id": 15,
        "name": "潘清生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区人大常委会主任",
        "current_org": "赣县区人大常委会",
        "source": "赣县区新闻报道",
    },
    {
        "id": 16,
        "name": "孔祥鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赣县区政协主席",
        "current_org": "赣县区政协",
        "source": "赣县区新闻报道",
    },
    # ── 相关人物（跨县关联）────────────────────────────────────────────
    # 李赣兴 — 南康区长, 赣县出生
    {
        "id": 17,
        "name": "李赣兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "江西赣县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南康区委副书记、区长",
        "current_org": "南康区人民政府",
        "source": "build_南康区_data.py; 南康区政府官网 https://www.nkjx.gov.cn",
    },
]

organizations = [
    {"id": 1, "name": "中共赣县区委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州赣县"},
    {"id": 2, "name": "赣县区人民政府", "type": "政府", "level": "县处级",
     "parent": "赣州市人民政府", "location": "江西赣州赣县"},
    {"id": 3, "name": "中共赣县区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市纪律检查委员会", "location": "江西赣州赣县"},
    {"id": 4, "name": "赣县区人大常委会", "type": "人大", "level": "县处级",
     "parent": "赣州市人大常委会", "location": "江西赣州赣县"},
    {"id": 5, "name": "赣县区政协", "type": "政协", "level": "县处级",
     "parent": "赣州市政协", "location": "江西赣州赣县"},
    {"id": 6, "name": "赣县区委组织部", "type": "党委", "level": "副处级",
     "parent": "中共赣县区委员会", "location": "江西赣州赣县"},
    {"id": 7, "name": "赣县区委宣传部", "type": "党委", "level": "副处级",
     "parent": "中共赣县区委员会", "location": "江西赣州赣县"},
    {"id": 8, "name": "赣县区委政法委员会", "type": "党委", "level": "副处级",
     "parent": "中共赣县区委员会", "location": "江西赣州赣县"},
    {"id": 9, "name": "赣县区人武部", "type": "政府", "level": "县处级",
     "parent": "赣州军分区", "location": "江西赣州赣县"},
    {"id": 10, "name": "市公安局赣县分局", "type": "政府", "level": "副处级",
     "parent": "赣州市公安局", "location": "江西赣州赣县"},
    {"id": 11, "name": "赣州市人大常委会", "type": "人大", "level": "地厅级",
     "parent": "江西省人大常委会", "location": "江西赣州"},
    {"id": 12, "name": "赣州市政协", "type": "政协", "level": "地厅级",
     "parent": "江西省政协", "location": "江西赣州"},
    {"id": 13, "name": "南康区人民政府", "type": "政府", "level": "县处级",
     "parent": "赣州市人民政府", "location": "江西赣州南康"},
]

positions = [
    # 廖永平 — 区委书记
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "赣县区委书记", "start": "2020", "end": "",
     "rank": "县处级正职", "note": "现任（2020年起任赣县区委书记）"},
    # 刘文彦 — 区长
    {"id": 2, "person_id": 2, "org_id": 1,
     "title": "赣县区委副书记", "start": "2021", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2,
     "title": "赣县区委副书记、区长", "start": "2021", "end": "",
     "rank": "县处级正职", "note": "现任"},
    # 胡晓平 — 前任区委书记
    {"id": 4, "person_id": 3, "org_id": 1,
     "title": "赣县区委书记", "start": "2016", "end": "2020",
     "rank": "县处级正职", "note": "前任区委书记，赣县撤县设区后首任书记"},
    {"id": 5, "person_id": 3, "org_id": 11,
     "title": "赣州市人大常委会副主任", "start": "2020", "end": "",
     "rank": "副厅级", "note": "现任（2020年晋升）"},
    # 张景霖 — 前任区长
    {"id": 6, "person_id": 4, "org_id": 2,
     "title": "赣县县长/赣县区长", "start": "2011", "end": "2021",
     "rank": "县处级正职", "note": "前任政府主官（从赣县到赣县区）"},
    {"id": 7, "person_id": 4, "org_id": 12,
     "title": "赣州市政协副主席", "start": "2021", "end": "",
     "rank": "副厅级", "note": "现任（2021年晋升）"},
    # 赖卫国 — 副书记
    {"id": 8, "person_id": 5, "org_id": 1,
     "title": "赣县区委副书记", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任"},
    # 罗理强 — 常务副区长
    {"id": 9, "person_id": 6, "org_id": 1,
     "title": "赣县区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 10, "person_id": 6, "org_id": 2,
     "title": "赣县区常务副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 刘桂健 — 纪委书记
    {"id": 11, "person_id": 7, "org_id": 1,
     "title": "赣县区委常委、纪委书记", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 12, "person_id": 7, "org_id": 3,
     "title": "赣县区监委主任", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 黄桂昌 — 组织部长
    {"id": 13, "person_id": 8, "org_id": 6,
     "title": "赣县区委常委、组织部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 邓永明 — 宣传部长
    {"id": 14, "person_id": 9, "org_id": 7,
     "title": "赣县区委常委、宣传部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 陈铁军 — 政法委书记
    {"id": 15, "person_id": 10, "org_id": 8,
     "title": "赣县区委常委、政法委书记", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 肖桂香 — 人武部
    {"id": 16, "person_id": 11, "org_id": 9,
     "title": "赣县区委常委（人武部部长/政委）", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 肖云 — 副区长
    {"id": 17, "person_id": 12, "org_id": 2,
     "title": "赣县区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 刘震 — 副区长、公安局长
    {"id": 18, "person_id": 13, "org_id": 2,
     "title": "赣县区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 19, "person_id": 13, "org_id": 10,
     "title": "市公安局赣县分局局长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 左旭 — 副区长
    {"id": 20, "person_id": 14, "org_id": 2,
     "title": "赣县区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 潘清生 — 人大主任
    {"id": 21, "person_id": 15, "org_id": 4,
     "title": "赣县区人大常委会主任", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任"},
    # 孔祥鑫 — 政协主席
    {"id": 22, "person_id": 16, "org_id": 5,
     "title": "赣县区政协主席", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任"},
    # 李赣兴 — 南康区长（赣县出生关联）
    {"id": 23, "person_id": 17, "org_id": 13,
     "title": "南康区委副书记、区长", "start": "2021", "end": "",
     "rank": "县处级正职", "note": "现任; 江西赣县（今赣县区）出生"},
]

relationships = [
    # 党政搭档：廖永平 × 刘文彦
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "廖永平（区委书记）与刘文彦（区委副书记、区长）为赣县区党政正职搭档",
     "overlap_org": "赣县区", "overlap_period": "2021至今"},
    # 前后任：胡晓平 → 廖永平
    {"id": 2, "person_a_id": 3, "person_b_id": 1,
     "type": "前后任",
     "context": "胡晓平（前任区委书记）→ 廖永平（现任区委书记），胡晓平升任赣州市人大常委会副主任",
     "overlap_org": "中共赣县区委员会", "overlap_period": "2020交接"},
    # 前后任：张景霖 → 刘文彦
    {"id": 3, "person_a_id": 4, "person_b_id": 2,
     "type": "前后任",
     "context": "张景霖（前任区长）→ 刘文彦（现任区长），张景霖升任赣州市政协副主席",
     "overlap_org": "赣县区人民政府", "overlap_period": "2021交接"},
    # 廖永平与各常委/副区长的上下级关系
    {"id": 4, "person_a_id": 1, "person_b_id": 5,
     "type": "上下级",
     "context": "廖永平（区委书记）与赖卫国（区委副书记）",
     "overlap_org": "中共赣县区委员会", "overlap_period": "至今"},
    {"id": 5, "person_a_id": 1, "person_b_id": 6,
     "type": "上下级",
     "context": "廖永平（区委书记）与罗理强（常委、常务副区长）",
     "overlap_org": "赣县区", "overlap_period": "至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 7,
     "type": "上下级",
     "context": "廖永平（区委书记）与刘桂健（纪委书记）",
     "overlap_org": "中共赣县区委员会", "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 8,
     "type": "上下级",
     "context": "廖永平（区委书记）与黄桂昌（组织部长）",
     "overlap_org": "中共赣县区委员会", "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 9,
     "type": "上下级",
     "context": "廖永平（区委书记）与邓永明（宣传部长）",
     "overlap_org": "中共赣县区委员会", "overlap_period": "至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 10,
     "type": "上下级",
     "context": "廖永平（区委书记）与陈铁军（政法委书记）",
     "overlap_org": "中共赣县区委员会", "overlap_period": "至今"},
    {"id": 10, "person_a_id": 1, "person_b_id": 11,
     "type": "上下级",
     "context": "廖永平（区委书记）与肖桂香（人武部）",
     "overlap_org": "赣县区", "overlap_period": "至今"},
    {"id": 11, "person_a_id": 1, "person_b_id": 15,
     "type": "上下级",
     "context": "廖永平（区委书记）与潘清生（人大主任）",
     "overlap_org": "赣县区", "overlap_period": "至今"},
    {"id": 12, "person_a_id": 1, "person_b_id": 16,
     "type": "上下级",
     "context": "廖永平（区委书记）与孔祥鑫（政协主席）",
     "overlap_org": "赣县区", "overlap_period": "至今"},
    # 刘文彦与各副区长的工作关系
    {"id": 13, "person_a_id": 2, "person_b_id": 6,
     "type": "上下级",
     "context": "刘文彦（区长）与罗理强（常务副区长）",
     "overlap_org": "赣县区人民政府", "overlap_period": "至今"},
    {"id": 14, "person_a_id": 2, "person_b_id": 12,
     "type": "上下级",
     "context": "刘文彦（区长）与肖云（副区长）",
     "overlap_org": "赣县区人民政府", "overlap_period": "至今"},
    {"id": 15, "person_a_id": 2, "person_b_id": 13,
     "type": "上下级",
     "context": "刘文彦（区长）与刘震（副区长、公安局长）",
     "overlap_org": "赣县区人民政府", "overlap_period": "至今"},
    {"id": 16, "person_a_id": 2, "person_b_id": 14,
     "type": "上下级",
     "context": "刘文彦（区长）与左旭（副区长）",
     "overlap_org": "赣县区人民政府", "overlap_period": "至今"},
    # 前后任书记与前任书记的原班子成员
    {"id": 17, "person_a_id": 3, "person_b_id": 4,
     "type": "同僚",
     "context": "胡晓平（前任书记）与张景霖（前任区长）在赣县区/赣县长期搭班子",
     "overlap_org": "赣县区", "overlap_period": "2016-2020"},
    # 跨县关联：李赣兴（赣县出生，现南康区长）
    {"id": 18, "person_a_id": 1, "person_b_id": 17,
     "type": "跨县关联",
     "context": "李赣兴出生于原赣县（今赣县区），现任南康区长，与廖永平有赣县本地渊源",
     "overlap_org": "赣县区/南康区", "overlap_period": ""},
    {"id": 19, "person_a_id": 2, "person_b_id": 17,
     "type": "跨县关联",
     "context": "刘文彦（赣县区长）与李赣兴（南康区长、赣县出生）——同地域人脉纽带",
     "overlap_org": "赣州市", "overlap_period": ""},
    # 同乡关联：廖永平与刘文彦均为宁都人
    {"id": 20, "person_a_id": 1, "person_b_id": 2,
     "type": "同乡",
     "context": "廖永平（宁都人）与刘文彦（宁都人）均为宁都籍，有同乡关系",
     "overlap_org": "赣县区", "overlap_period": "至今"},
]


# ── BUILD SQLite ─────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER NOT NULL,
            person_b_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    print(f"✓ SQLite DB created: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")
    return counts


# ── BUILD GEXF ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role:
        return "255,50,50"  # Red for party secretary
    if "区长" in role or "市长" in role or "县长" in role:
        return "50,100,255"  # Blue for government head
    if "纪委书记" in role or "纪检" in role:
        return "255,165,0"  # Orange for discipline
    return "100,100,100"  # Grey


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    return p["id"] <= 2


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>赣县区领导班子工作关系网络 - 区委书记廖永平 &amp; 区长刘文彦</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "role"), ("2", "birth"), ("3", "birthplace"), ("4", "education")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "context"), ("2", "start"), ("3", "end")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("education", ""))}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Worked-at edges (person -> organization)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person <-> person)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph created: {GEXF_PATH}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {len(positions) + len(relationships)}")


# ── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"赣县区 (Ganxian District) 领导班子工作关系网络")
    print(f"Date: {today}")
    print(f"{'─' * 50}")
    build_db()
    build_gexf()
    print(f"{'─' * 50}")
    print(f"Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
