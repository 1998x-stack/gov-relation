#!/usr/bin/env python3
"""Build 广南县 (Guangnan County) 领导班子工作关系网络.

云南省文山壮族苗族自治州下辖县.
调查日期: 2026-08-03.

数据来源:
  - 广南县人民政府官网 https://www.yngn.gov.cn — 领导之窗栏目
    (县委领导: /gnxrmzf/xwld/pc/list.html, 政府领导: /gnxrmzf/zfld/pc/list.html,
     人大: /gnxrmzf/rdcwh/pc/list.html, 政协: /gnxrmzf/zxld/pc/list.html)
  - 2026-05-27 广南县领导干部会议宣布主要领导调整 (视听广南GNTV)
  - 2026-06-19 广南县第十八届人大常委会干部任免职名单
"""

import sqlite3
from pathlib import Path

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "广南县"
TODAY = "2026-08-03"
PROVINCE = "云南省"
CITY = "文山壮族苗族自治州"

# ── Paths ────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
DB_PATH = BASE / f"{SLUG}_network.db"
GEXF_PATH = BASE / f"{SLUG}_network.gexf"

# ── Data: Persons ────────────────────────────────────────────────────────
persons = [
    # ===== 县委领导 (Party Committee Leadership) =====
    {
        "id": 1,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1982年12月",
        "birthplace": "云南马关",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "2001年10月",
        "current_post": "县委书记",
        "current_org": "中共广南县委",
        "source": "广南县人民政府官网/领导之窗/县委领导; Baidu Baike摘要",
    },
    {
        "id": 2,
        "name": "卢建国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1999年10月",
        "current_post": "县委副书记、县人民政府党组书记、副县长、代理县长",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    {
        "id": 3,
        "name": "周靖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1999年08月",
        "current_post": "县委副书记",
        "current_org": "中共广南县委",
        "source": "广南县人民政府官网/领导之窗/县委领导",
    },
    {
        "id": 4,
        "name": "田永灿",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1981年01月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共广南县纪委",
        "source": "广南县人民政府官网/领导之窗/县委领导",
    },
    {
        "id": 5,
        "name": "农嵋麟",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "2005年09月",
        "current_post": "县委常委、县政府党组副书记、常务副县长",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/县委领导",
    },
    {
        "id": 6,
        "name": "王兆光",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1999年09月",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共广南县委",
        "source": "广南县人民政府官网/领导之窗/县委领导",
    },
    {
        "id": 7,
        "name": "矣焱阳",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2006年12月",
        "current_post": "县委常委、县委统战部部长",
        "current_org": "中共广南县委",
        "source": "广南县人民政府官网/领导之窗/县委领导",
    },
    {
        "id": 8,
        "name": "彭光文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2001年09月",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共广南县委",
        "source": "广南县人民政府官网/领导之窗/县委领导",
    },
    {
        "id": 9,
        "name": "唐雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2009年11月",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共广南县委",
        "source": "广南县人民政府官网/领导之窗/县委领导",
    },
    # ===== 政府领导 =====
    {
        "id": 10,
        "name": "余涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2009年07月",
        "current_post": "副县长（挂职）",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    {
        "id": 11,
        "name": "陈刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2008年07月",
        "current_post": "副县长（挂职）",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    {
        "id": 12,
        "name": "谢帮林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2002年11月",
        "current_post": "副县长、县公安局局长",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    {
        "id": 13,
        "name": "沈斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1999年08月",
        "current_post": "副县长",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    {
        "id": 14,
        "name": "丁视启",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2000年08月",
        "current_post": "副县长",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    {
        "id": 15,
        "name": "秦凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2008年12月",
        "current_post": "副县长",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    {
        "id": 16,
        "name": "邵南银",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2003年07月",
        "current_post": "副县长（挂职）",
        "current_org": "广南县人民政府",
        "source": "广南县人民政府官网/领导之窗/政府领导",
    },
    # ===== 人大常委会领导 =====
    {
        "id": 17,
        "name": "刘选良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2000年08月",
        "current_post": "县人大常委会党组书记",
        "current_org": "广南县人大常委会",
        "source": "广南县人民政府官网/领导之窗/人大常委会领导",
    },
    {
        "id": 18,
        "name": "钱虎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1991年03月",
        "current_post": "县人大常委会主任",
        "current_org": "广南县人大常委会",
        "source": "广南县人民政府官网/领导之窗/人大常委会领导",
    },
    {
        "id": 19,
        "name": "梁忠",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2000年07月",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "广南县人大常委会",
        "source": "广南县人民政府官网/领导之窗/人大常委会领导",
    },
    {
        "id": 20,
        "name": "余邦发",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1992年07月",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "广南县人大常委会",
        "source": "广南县人民政府官网/领导之窗/人大常委会领导",
    },
    {
        "id": 21,
        "name": "杨有龙",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2002年10月",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "广南县人大常委会",
        "source": "广南县人民政府官网/领导之窗/人大常委会领导",
    },
    {
        "id": 22,
        "name": "刘巍巍",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "无党派",
        "work_start": "2005年11月",
        "current_post": "县人大常委会副主任",
        "current_org": "广南县人大常委会",
        "source": "广南县人民政府官网/领导之窗/人大常委会领导",
    },
    # ===== 政协领导 =====
    {
        "id": 23,
        "name": "李贵洪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1994年07月",
        "current_post": "县政协党组书记、主席",
        "current_org": "广南县政协",
        "source": "广南县人民政府官网/领导之窗/政协领导",
    },
    {
        "id": 24,
        "name": "陶飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1997年09月",
        "current_post": "县政协党组副书记、副主席",
        "current_org": "广南县政协",
        "source": "广南县人民政府官网/领导之窗/政协领导",
    },
    {
        "id": 25,
        "name": "陆俊江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "1999年07月",
        "current_post": "县政协副主席",
        "current_org": "广南县政协",
        "source": "广南县人民政府官网/领导之窗/政协领导",
    },
    {
        "id": 26,
        "name": "陆令兮",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "1996年07月",
        "current_post": "县政协副主席",
        "current_org": "广南县政协",
        "source": "广南县人民政府官网/领导之窗/政协领导",
    },
    {
        "id": 27,
        "name": "李晓蕊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "无党派",
        "work_start": "1998年12月",
        "current_post": "县政协副主席",
        "current_org": "广南县政协",
        "source": "广南县人民政府官网/领导之窗/政协领导",
    },
]

# ── Data: Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共广南县委", "type": "党委", "level": "县级",
     "parent": "中共文山州委", "location": "广南县"},
    {"id": 2, "name": "广南县人民政府", "type": "政府", "level": "县级",
     "parent": "文山州人民政府", "location": "广南县"},
    {"id": 3, "name": "广南县人大常委会", "type": "人大", "level": "县级",
     "parent": "文山州人大常委会", "location": "广南县"},
    {"id": 4, "name": "广南县政协", "type": "政协", "level": "县级",
     "parent": "文山州政协", "location": "广南县"},
    {"id": 5, "name": "中共广南县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共文山州纪委", "location": "广南县"},
    {"id": 6, "name": "广南县公安局", "type": "政府", "level": "县级",
     "parent": "广南县人民政府", "location": "广南县"},
]

# ── Data: Positions ─────────────────────────────────────────────────────
positions = [
    # 陈伟 - 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "县委书记",
     "start_date": "2026-05", "end_date": "至今", "rank": "正处级",
     "note": "2026年5月全县领导干部会议宣布任职; 此前任广南县长"},
    # 陈伟 曾任广南县长
    {"id": 101, "person_id": 1, "org_id": 2, "title": "县长",
     "start_date": "2021-06", "end_date": "2026-05", "rank": "正处级",
     "note": "2021年5月任代县长, 6月任县长; 2026年6月辞去县长职务"},
    # 陈伟 曾任麻栗坡县委副书记
    {"id": 102, "person_id": 1, "org_id": 1, "title": "县委副书记",
     "start_date": "2020-07", "end_date": "2021-05", "rank": "副处级",
     "note": "麻栗坡县委副书记"},
    # 卢建国 - 代理县长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "副县长、代理县长",
     "start_date": "2026-06", "end_date": "至今", "rank": "正处级",
     "note": "2026年6月县人大常委会任命为副县长、代理县长"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "县委副书记",
     "start_date": "2026-06", "end_date": "至今", "rank": "副处级", "note": ""},
    # 周靖 - 专职副书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "专职副书记"},
    # 田永灿 - 县纪委书记
    {"id": 5, "person_id": 4, "org_id": 5, "title": "县纪委书记、监主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 农嵋麟 - 常务副县长
    {"id": 6, "person_id": 5, "org_id": 2, "title": "县委常委、常务副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "县政府党组副书记"},
    {"id": 7, "person_id": 5, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 王兆光 - 县委办主任
    {"id": 8, "person_id": 6, "org_id": 1, "title": "县委常委、县委办公室主任",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "兼县委国安办主任、县直机关工委书记"},
    # 矣焱阳 - 统战部长
    {"id": 9, "person_id": 7, "org_id": 1, "title": "县委常委、统战部部长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "女"},
    # 彭光文 - 宣传部长
    {"id": 10, "person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 唐雷 - 政法委书记
    {"id": 11, "person_id": 9, "org_id": 1, "title": "县委常委、政法委书记",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 副县长
    {"id": 12, "person_id": 10, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 13, "person_id": 11, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 14, "person_id": 12, "org_id": 6, "title": "副县长、县公安局局长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 15, "person_id": 13, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 16, "person_id": 14, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 17, "person_id": 15, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 18, "person_id": 16, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 人大常委会
    {"id": 19, "person_id": 17, "org_id": 3, "title": "党组书记",
     "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"id": 20, "person_id": 18, "org_id": 3, "title": "主任",
     "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"id": 21, "person_id": 19, "org_id": 3, "title": "副主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党组成员"},
    {"id": 22, "person_id": 20, "org_id": 3, "title": "副主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党组成员"},
    {"id": 23, "person_id": 21, "org_id": 3, "title": "副主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党组成员"},
    {"id": 24, "person_id": 22, "org_id": 3, "title": "副主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "无党派"},
    # 政协
    {"id": 25, "person_id": 23, "org_id": 4, "title": "主席",
     "start_date": "", "end_date": "至今", "rank": "正处级", "note": "党组书记"},
    {"id": 26, "person_id": 24, "org_id": 4, "title": "副主席",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党组副书记"},
    {"id": 27, "person_id": 25, "org_id": 4, "title": "副主席",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 28, "person_id": 26, "org_id": 4, "title": "副主席",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"id": 29, "person_id": 27, "org_id": 4, "title": "副主席",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "无党派"},
]

# ── Data: Relationships ─────────────────────────────────────────────────
relationships = [
    # 陈伟 ↔ 卢建国 (书记和代县长)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "陈伟任县委书记, 卢建国任代理县长",
     "overlap_org": "广南党政领导班子",
     "overlap_period": "2026-至今"},
    # 陈伟 ↔ 周靖 (书记和副书记)
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "陈伟与周靖在县委班子中共事",
     "overlap_org": "中共广南县委",
     "overlap_period": "2026-至今"},
    # 陈伟 ↔ 农嵋麟 (书记和常务副)
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "陈伟曾与农嵋麟在党政班子中共事",
     "overlap_org": "广南县委县政府",
     "overlap_period": "2021/2026-至今"},
    # 卢建国 ↔ 农嵋麟 (代县长和常务副)
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "卢建国与农嵋麟在县政府班子中共事",
     "overlap_org": "广南县人民政府",
     "overlap_period": "2026-至今"},
    # 周靖 ↔ 田永灿 (县委班子)
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共广南县委",
     "overlap_period": "至今"},
    # 王兆光 ↔ 矣焱阳 (县委班子)
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共广南县委",
     "overlap_period": "至今"},
    # 彭光文 ↔ 唐雷 (县委班子)
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共广南县委",
     "overlap_period": "至今"},
    # 谢帮林 ↔ 沈斌 (副县长班子)
    {"person_a": 12, "person_b": 13, "type": "overlap",
     "context": "同为县政府副县长",
     "overlap_org": "广南县人民政府",
     "overlap_period": "至今"},
    # 丁视启 ↔ 秦凯 (副县长班子)
    {"person_a": 14, "person_b": 15, "type": "overlap",
     "context": "同为县政府副县长",
     "overlap_org": "广南县人民政府",
     "overlap_period": "至今"},
    # 钱虎 ↔ 李贵洪 (人大+政协正职)
    {"person_a": 18, "person_b": 23, "type": "overlap",
     "context": "县人大常委会主任与县政协主席",
     "overlap_org": "广南县",
     "overlap_period": "至今"},
    # 刘选良 ↔ 钱虎 (人大班子)
    {"person_a": 17, "person_b": 18, "type": "overlap",
     "context": "刘选良（党组书记）与钱虎（主任）在人常委会共事",
     "overlap_org": "广南县人大常委会",
     "overlap_period": "至今"},
    # 陶飞 ↔ 李晓蕊 (政协班子)
    {"person_a": 24, "person_b": 27, "type": "overlap",
     "context": "政协副主席同僚",
     "overlap_org": "广南县政协",
     "overlap_period": "至今"},
    # 余涛 ↔ 陈刚 (挂职副县长)
    {"person_a": 10, "person_b": 11, "type": "overlap",
     "context": "同为挂职副县长",
     "overlap_org": "广南县人民政府",
     "overlap_period": "至今"},
]

# ── SQL Schema ──────────────────────────────────────────────────────────
def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start_date TEXT, end_date TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)


# ── Run Build ───────────────────────────────────────────────────────────
def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print("=" * 60)

    conn = sqlite3.connect(str(DB_PATH))
    create_tables(conn)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute("INSERT INTO persons (" + ",".join(cols_p) + ") VALUES (" + ",".join(["?"]*len(cols_p)) + ")", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute("INSERT INTO organizations (" + ",".join(cols_o) + ") VALUES (" + ",".join(["?"]*len(cols_o)) + ")", vals)

    cols_pos = ["id","person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute("INSERT INTO positions (" + ",".join(cols_pos) + ") VALUES (" + ",".join(["?"]*len(cols_pos)) + ")", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (" + ",".join(["?"]*len(cols_r)) + ")", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post or "书记" in post:
            return ("255,50,50", 20.0)
        elif "代理县长" in post:
            return ("50,100,255", 18.0)
        elif "县长" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "纪委" in post or "监委" in post:
            return ("255,165,0", 12.0)
        elif "副县长" in post or "党组成员" in post:
            return ("100,100,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        elif "挂职" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }.get(typ, "200,200,200")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c_val, sz_val = person_color(p["current_post"])
        parts = c_val.split(",")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="{sz_val}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"]).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'        <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(str(GEXF_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()