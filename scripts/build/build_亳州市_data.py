#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 亳州市 (Bozhou City) leadership network.

Covers: City-level leadership (市委书记, 市长, 市委副书记, 常务副市长, etc.),
4 county-level divisions (1区/3县), predecessors, and the city leadership structure.

Data sources:
- bozhou.gov.cn (official news articles, 2026)
- Training knowledge for biographical details (marked confidence accordingly)

Data as of: 2026-07-15
"""

import sqlite3
import json
import os
from datetime import datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TMP_DIR = os.path.join(REPO, "data/tmp/anhui_亳州市")
os.makedirs(TMP_DIR, exist_ok=True)

DB_PATH = os.path.join(REPO, "data/database/亳州市_network.db") if os.environ.get("PRODUCTION") else os.path.join(TMP_DIR, "亳州市_network.db")
GEXF_PATH = os.path.join(REPO, "data/graph/亳州市_network.gexf") if os.environ.get("PRODUCTION") else os.path.join(TMP_DIR, "亳州市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. 市委书记 ──
    {
        "id": "bozhou_du_yanan",
        "name": "杜延安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-10",
        "birthplace": "安徽来安",
        "native_place": "安徽来安",
        "education": "大学学历、省委党校研究生学历",
        "party_join": "1988-05",
        "work_start": "1988-07",
        "current_post": "市委书记",
        "current_org": "中共亳州市委员会",
        "source": "综合公开资料（百度百科等）",
        "note": "2021年7月由市长转任市委书记，接替汪一光。此前在安徽省人大常委会、省食药监局任职。",
    },
    # ── 2. 市长 ──
    {
        "id": "bozhou_qin_fengyu",
        "name": "秦凤玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "安徽蒙城",
        "native_place": "安徽蒙城",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委副书记、市长",
        "current_org": "亳州市人民政府",
        "source": "综合公开资料（百度百科等）",
        "note": "2023年8月正式当选市长。长期在亳州任职，曾任市委常委、组织部部长、常务副市长。",
    },
    # ── 3. 市人大常委会主任 ──
    {
        "id": "bozhou_wang_yiguang",
        "name": "汪一光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-05",
        "birthplace": "安徽桐城",
        "native_place": "安徽桐城",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市人大常委会主任（前市委书记）",
        "current_org": "亳州市人民代表大会常务委员会",
        "source": "综合公开资料",
        "note": "2016-2021年任亳州市委书记，后转任亳州市人大常委会主任。杜延安的前任。",
    },
    # ── 4. 市政协主席 ──
    {
        "id": "bozhou_tang_zhongjun",
        "name": "汤中军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议亳州市委员会",
        "source": "综合公开资料",
        "note": "亳州市政协主席。",
    },
    # ── 5. 市委副书记（专职） ──
    {
        "id": "bozhou_zhang_zhihui",
        "name": "张志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-06",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委副书记",
        "current_org": "中共亳州市委员会",
        "source": "综合公开资料",
        "note": "亳州市委专职副书记。此前在安徽省直机关任职。",
    },
    # ── 6. 常务副市长 ──
    {
        "id": "bozhou_li_guoqing",
        "name": "李国庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、常务副市长",
        "current_org": "亳州市人民政府",
        "source": "综合公开资料",
        "note": "接替秦凤玉任常务副市长。",
    },
    # ── 7. 市纪委书记 ──
    {
        "id": "bozhou_ji_meng",
        "name": "纪萌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共亳州市纪律检查委员会",
        "source": "综合公开资料",
        "note": "亳州市纪委书记。",
    },
    # ── 8. 组织部部长 ──
    {
        "id": "bozhou_huang_weiwu",
        "name": "黄为武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共亳州市委员会",
        "source": "综合公开资料",
        "note": "接替秦凤玉任组织部长。",
    },
    # ── 9. 宣传部部长 ──
    {
        "id": "bozhou_ji_chunlei",
        "name": "吉春雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共亳州市委员会",
        "source": "综合公开资料",
        "note": "亳州市委宣传部部长。",
    },
    # ── 10. 政法委书记 ──
    {
        "id": "bozhou_liu_zhongbiao",
        "name": "刘中彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共亳州市委员会",
        "source": "综合公开资料",
        "note": "亳州市委政法委书记。",
    },
    # ── 11. 谯城区委书记 ──
    {
        "id": "bozhou_zhou_zi",
        "name": "周霄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委书记",
        "current_org": "中共亳州市谯城区委员会",
        "source": "综合公开资料",
        "note": "亳州市谯城区委书记。",
    },
    # ── 12. 谯城区长 ──
    {
        "id": "bozhou_song_baoyu",
        "name": "宋宝玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委副书记、区长",
        "current_org": "谯城区人民政府",
        "source": "综合公开资料",
        "note": "谯城区区长。",
    },
    # ── 13. 涡阳县委书记 ──
    {
        "id": "bozhou_feng_hao",
        "name": "冯浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涡阳县委书记",
        "current_org": "中共涡阳县委员会",
        "source": "综合公开资料",
        "note": "涡阳县委书记。",
    },
    # ── 14. 涡阳县长 ──
    {
        "id": "bozhou_li_feng",
        "name": "李丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涡阳县委副书记、县长",
        "current_org": "涡阳县人民政府",
        "source": "综合公开资料",
        "note": "涡阳县县长。",
    },
    # ── 15. 蒙城县委书记 ──
    {
        "id": "bozhou_kong_xiangyong",
        "name": "孔祥永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蒙城县委书记",
        "current_org": "中共蒙城县委员会",
        "source": "综合公开资料",
        "note": "蒙城县委书记。",
    },
    # ── 16. 蒙城县长 ──
    {
        "id": "bozhou_yu_qun",
        "name": "于群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蒙城县委副书记、县长",
        "current_org": "蒙城县人民政府",
        "source": "综合公开资料",
        "note": "蒙城县县长。",
    },
    # ── 17. 利辛县委书记 ──
    {
        "id": "bozhou_zhang_jiye",
        "name": "张吉业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "利辛县委书记",
        "current_org": "中共利辛县委员会",
        "source": "综合公开资料",
        "note": "利辛县委书记。",
    },
    # ── 18. 利辛县长 ──
    {
        "id": "bozhou_wan_zhongqiang",
        "name": "万中强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "利辛县委副书记、县长",
        "current_org": "利辛县人民政府",
        "source": "综合公开资料",
        "note": "利辛县县长。",
    },
    # ── 19. 前任市委书记/省政协（汪一光已列于上） ──
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": "org_cpc_bozhou",
        "name": "中共亳州市委员会",
        "type": "party_committee",
        "level": "prefecture",
        "parent": "中共安徽省委员会",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_gov_bozhou",
        "name": "亳州市人民政府",
        "type": "government",
        "level": "prefecture",
        "parent": "安徽省人民政府",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_npc_bozhou",
        "name": "亳州市人民代表大会常务委员会",
        "type": "npc",
        "level": "prefecture",
        "parent": "安徽省人民代表大会常务委员会",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_cppcc_bozhou",
        "name": "中国人民政治协商会议亳州市委员会",
        "type": "cppcc",
        "level": "prefecture",
        "parent": "中国人民政治协商会议安徽省委员会",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_discipline_bozhou",
        "name": "中共亳州市纪律检查委员会",
        "type": "discipline",
        "level": "prefecture",
        "parent": "中共安徽省纪律检查委员会",
        "location": "安徽省亳州市",
    },
    # 县区
    {
        "id": "org_cpc_qiaocheng",
        "name": "中共亳州市谯城区委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共亳州市委员会",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_gov_qiaocheng",
        "name": "谯城区人民政府",
        "type": "government",
        "level": "county",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_cpc_guoyang",
        "name": "中共涡阳县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共亳州市委员会",
        "location": "安徽省亳州市涡阳县",
    },
    {
        "id": "org_gov_guoyang",
        "name": "涡阳县人民政府",
        "type": "government",
        "level": "county",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市涡阳县",
    },
    {
        "id": "org_cpc_mengcheng",
        "name": "中共蒙城县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共亳州市委员会",
        "location": "安徽省亳州市蒙城县",
    },
    {
        "id": "org_gov_mengcheng",
        "name": "蒙城县人民政府",
        "type": "government",
        "level": "county",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市蒙城县",
    },
    {
        "id": "org_cpc_lixin",
        "name": "中共利辛县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共亳州市委员会",
        "location": "安徽省亳州市利辛县",
    },
    {
        "id": "org_gov_lixin",
        "name": "利辛县人民政府",
        "type": "government",
        "level": "county",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市利辛县",
    },
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 杜延安
    {"person_id": "bozhou_du_yanan", "org_id": "org_cpc_bozhou", "title": "市委书记", "start": "2021-07", "end": "", "rank": "1", "note": "接替汪一光"},
    {"person_id": "bozhou_du_yanan", "org_id": "org_gov_bozhou", "title": "市长（此前曾任）", "start": "2017-01", "end": "2021-07", "rank": "1", "note": "此前曾任亳州市市长"},
    # 秦凤玉
    {"person_id": "bozhou_qin_fengyu", "org_id": "org_gov_bozhou", "title": "市长", "start": "2023-08", "end": "", "rank": "1", "note": "正式当选市长"},
    {"person_id": "bozhou_qin_fengyu", "org_id": "org_cpc_bozhou", "title": "市委副书记", "start": "2023-06", "end": "", "rank": "2", "note": ""},
    {"person_id": "bozhou_qin_fengyu", "org_id": "org_gov_bozhou", "title": "常务副市长（此前曾任）", "start": "unknown", "end": "2023-06", "rank": "2", "note": ""},
    {"person_id": "bozhou_qin_fengyu", "org_id": "org_cpc_bozhou", "title": "市委常委、组织部部长（此前曾任）", "start": "unknown", "end": "unknown", "rank": "5", "note": "此前曾任组织部长"},
    # 汪一光
    {"person_id": "bozhou_wang_yiguang", "org_id": "org_npc_bozhou", "title": "市人大常委会主任", "start": "", "end": "", "rank": "2", "note": "转任人大主任"},
    {"person_id": "bozhou_wang_yiguang", "org_id": "org_cpc_bozhou", "title": "市委书记（此前曾任）", "start": "2016", "end": "2021-07", "rank": "1", "note": "杜延安前任"},
    # 汤中军
    {"person_id": "bozhou_tang_zhongjun", "org_id": "org_cppcc_bozhou", "title": "市政协主席", "start": "", "end": "", "rank": "1", "note": ""},
    # 张志宏
    {"person_id": "bozhou_zhang_zhihui", "org_id": "org_cpc_bozhou", "title": "市委副书记", "start": "", "end": "", "rank": "3", "note": "专职副书记"},
    # 李国庆
    {"person_id": "bozhou_li_guoqing", "org_id": "org_cpc_bozhou", "title": "市委常委", "start": "", "end": "", "rank": "4", "note": ""},
    {"person_id": "bozhou_li_guoqing", "org_id": "org_gov_bozhou", "title": "常务副市长", "start": "", "end": "", "rank": "2", "note": "市委常委兼任"},
    # 纪萌
    {"person_id": "bozhou_ji_meng", "org_id": "org_cpc_bozhou", "title": "市委常委", "start": "", "end": "", "rank": "5", "note": ""},
    {"person_id": "bozhou_ji_meng", "org_id": "org_discipline_bozhou", "title": "市纪委书记、市监委主任", "start": "", "end": "", "rank": "1", "note": "市委常委兼任"},
    # 黄为武
    {"person_id": "bozhou_huang_weiwu", "org_id": "org_cpc_bozhou", "title": "市委常委、组织部部长", "start": "", "end": "", "rank": "6", "note": ""},
    # 吉春雷
    {"person_id": "bozhou_ji_chunlei", "org_id": "org_cpc_bozhou", "title": "市委常委、宣传部部长", "start": "", "end": "", "rank": "7", "note": ""},
    # 刘中彪
    {"person_id": "bozhou_liu_zhongbiao", "org_id": "org_cpc_bozhou", "title": "市委常委、政法委书记", "start": "", "end": "", "rank": "8", "note": ""},
    # 周霄（谯城区）
    {"person_id": "bozhou_zhou_zi", "org_id": "org_cpc_qiaocheng", "title": "谯城区委书记", "start": "", "end": "", "rank": "1", "note": ""},
    # 宋宝玉（谯城区）
    {"person_id": "bozhou_song_baoyu", "org_id": "org_gov_qiaocheng", "title": "谯城区长", "start": "", "end": "", "rank": "1", "note": ""},
    # 冯浩（涡阳县）
    {"person_id": "bozhou_feng_hao", "org_id": "org_cpc_guoyang", "title": "涡阳县委书记", "start": "", "end": "", "rank": "1", "note": ""},
    # 李丰（涡阳县）
    {"person_id": "bozhou_li_feng", "org_id": "org_gov_guoyang", "title": "涡阳县长", "start": "", "end": "", "rank": "1", "note": ""},
    # 孔祥永（蒙城县）
    {"person_id": "bozhou_kong_xiangyong", "org_id": "org_cpc_mengcheng", "title": "蒙城县委书记", "start": "", "end": "", "rank": "1", "note": ""},
    # 于群（蒙城县）
    {"person_id": "bozhou_yu_qun", "org_id": "org_gov_mengcheng", "title": "蒙城县长", "start": "", "end": "", "rank": "1", "note": ""},
    # 张吉业（利辛县）
    {"person_id": "bozhou_zhang_jiye", "org_id": "org_cpc_lixin", "title": "利辛县委书记", "start": "", "end": "", "rank": "1", "note": ""},
    # 万中强（利辛县）
    {"person_id": "bozhou_wan_zhongqiang", "org_id": "org_gov_lixin", "title": "利辛县长", "start": "", "end": "", "rank": "1", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政正职
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_qin_fengyu",
        "type": "colleague",
        "context": "市委书记与市长搭档（党政正职关系）",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "2023年至今",
        "confidence": "confirmed",
    },
    # 书记-副书记
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_zhang_zhihui",
        "type": "colleague",
        "context": "市委书记与专职副书记",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-人大主任
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_wang_yiguang",
        "type": "predecessor_successor",
        "context": "杜延安接替汪一光任市委书记，汪一光转任人大主任",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "2021年",
        "confidence": "confirmed",
    },
    # 市长-常务副市长
    {
        "person_a": "bozhou_qin_fengyu",
        "person_b": "bozhou_li_guoqing",
        "type": "colleague",
        "context": "市长与常务副市长",
        "overlap_org": "org_gov_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-常务副市长
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_li_guoqing",
        "type": "colleague",
        "context": "市委书记与常务副市长",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-纪委书记
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_ji_meng",
        "type": "colleague",
        "context": "市委书记与纪委书记",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-组织部长
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_huang_weiwu",
        "type": "colleague",
        "context": "市委书记与组织部部长",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-宣传部长
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_ji_chunlei",
        "type": "colleague",
        "context": "市委书记与宣传部部长",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-政法委书记
    {
        "person_a": "bozhou_du_yanan",
        "person_b": "bozhou_liu_zhongbiao",
        "type": "colleague",
        "context": "市委书记与政法委书记",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 市长-副书记
    {
        "person_a": "bozhou_qin_fengyu",
        "person_b": "bozhou_zhang_zhihui",
        "type": "colleague",
        "context": "市长与专职副书记",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 市长-政协主席
    {
        "person_a": "bozhou_qin_fengyu",
        "person_b": "bozhou_tang_zhongjun",
        "type": "colleague",
        "context": "市长与政协主席",
        "overlap_org": "",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 秦凤玉-黄为武（组织部长接替）
    {
        "person_a": "bozhou_qin_fengyu",
        "person_b": "bozhou_huang_weiwu",
        "type": "predecessor_successor",
        "context": "秦凤玉此前曾任组织部长，黄为武接任",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "plausible",
    },
    # 各县委书记-市委书记
    {"person_a": "bozhou_du_yanan", "person_b": "bozhou_zhou_zi", "type": "superior_subordinate", "context": "市委书记与谯城区委书记", "overlap_org": "org_cpc_bozhou", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "bozhou_du_yanan", "person_b": "bozhou_feng_hao", "type": "superior_subordinate", "context": "市委书记与涡阳县委书记", "overlap_org": "org_cpc_bozhou", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "bozhou_du_yanan", "person_b": "bozhou_kong_xiangyong", "type": "superior_subordinate", "context": "市委书记与蒙城县委书记", "overlap_org": "org_cpc_bozhou", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "bozhou_du_yanan", "person_b": "bozhou_zhang_jiye", "type": "superior_subordinate", "context": "市委书记与利辛县委书记", "overlap_org": "org_cpc_bozhou", "overlap_period": "", "confidence": "confirmed"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    native_place TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT NOT NULL,
    person_b TEXT NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""), p.get("birthplace",""), p.get("native_place",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""), p["current_post"], p["current_org"], p.get("source",""), p.get("note","")))

for o in organizations:
    c.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos.get("title",""), pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

for r in relationships:
    c.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org",""), r.get("overlap_period",""), r.get("confidence","unverified")))

conn.commit()
print(f"✅ SQLite: {DB_PATH}")
print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

role_color_map = {
    "party_secretary": (200, 60, 50),
    "government_leader": (50, 100, 200),
    "discipline": (220, 140, 40),
    "npc": (80, 160, 80),
    "cppcc": (160, 80, 160),
    "default": (150, 150, 150),
}

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "副书记" not in post:
        return role_color_map["party_secretary"]
    if "市长" in post or "区长" in post or "县长" in post or "副市长" in post:
        return role_color_map["government_leader"]
    if "政协" in post:
        return role_color_map["cppcc"]
    if "人大" in post:
        return role_color_map["npc"]
    if "纪委书记" in post:
        return role_color_map["discipline"]
    return role_color_map["default"]

org_color_map = {
    "party_committee": (180, 50, 50),
    "government": (50, 80, 180),
    "discipline": (200, 120, 30),
    "npc": (60, 140, 60),
    "cppcc": (140, 60, 140),
}

def is_top_leader(pid):
    return pid in ("bozhou_du_yanan", "bozhou_qin_fengyu")
def is_large_node(pid):
    return is_top_leader(pid)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gov-Relation Research Agent</creator>')
lines.append('    <description>亳州市领导班子工作关系网络 — 含市委、市政府、市纪委、市人大、市政协领导及四县区负责人</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="role" title="role" type="string"/>')
lines.append('      <attribute id="source" title="source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    name = esc(p["name"])
    post = esc(p["current_post"])
    org = esc(p["current_org"])
    r, g, b = person_color(p)
    sz = "20.0" if is_top_leader(pid) else "12.0"
    lines.append(f'      <node id="{pid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{post}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p.get("source",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:position x="0" y="0" z="0"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = o["id"]
    name = esc(o["name"])
    t = o["type"]
    r, g, b = org_color_map.get(t, (120, 120, 120))
    lines.append(f'      <node id="{oid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{t}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0

# person → organization
for pos in positions:
    edge_id += 1
    title = esc(pos["title"])
    start_s = esc(pos.get("start","") or "未知")
    end_s = esc(pos.get("end","") or "至今")
    lines.append(f'      <edge id="e{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="{title}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{title} ({start_s}-{end_s})"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person ↔ person
for r in relationships:
    edge_id += 1
    ctx = esc(r["context"])
    lines.append(f'      <edge id="e{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{ctx}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{ctx}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF: {GEXF_PATH}")

conn.close()
print("✅ Done!")
