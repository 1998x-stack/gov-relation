#!/usr/bin/env python3
"""
郴州市领导班子工作关系网络 — 数据构建脚本
province: 湖南省
level: 地级市
targets: 市委书记 & 市长
as_of: 2026-07-24
"""
import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-24"
SLUG = "郴州市"
PROVINCE = "湖南省"

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ══════════════════════════════════════════════════════════════════════════
# Data
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ── 郴州市本级 ──
    {
        "id": "p1",
        "name": "阚保勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "山东省成武县",
        "education": "大学（院校待查）",
        "party_join": "1993年12月",
        "work_start": "1996年8月",
        "current_post": "中共郴州市委书记",
        "current_org": "中共郴州市委员会",
        "source": "https://zh.wikipedia.org/wiki/阚保勇",
        "notes": "1996年毕业于（院校待查）。由市长升任书记。"
    },
    {
        "id": "p2",
        "name": "白云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "天津市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "郴州市人民政府市长",
        "current_org": "郴州市人民政府",
        "source": "https://zh.wikipedia.org/wiki/白云峰_(1981年9月)",
        "notes": "80后地级市市长，2026年6月由郴州市人大常委会任命。此前曾在湖南省某市任职，完整履历待查。"
    },
    {
        "id": "p3",
        "name": "江波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年11月",
        "birthplace": "湖南省醴陵市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "郴州市人大常委会主任",
        "current_org": "郴州市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/郴州市",
        "notes": ""
    },
    {
        "id": "p4",
        "name": "陈跃文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年7月",
        "birthplace": "湖南省益阳市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "郴州市政协主席",
        "current_org": "中国人民政治协商会议郴州市委员会",
        "source": "https://zh.wikipedia.org/wiki/郴州市",
        "notes": ""
    },
    # ── 前任 ──
    {
        "id": "p5",
        "name": "吴巨培",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "湖南省涟源市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（待公布）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/吴巨培",
        "notes": "2022.03-2026.05任郴州市委书记。2026年5月卸任，'另有任用'。曾任湖南省公安厅副厅长、株洲市纪委书记、援藏总领队等。"
    },
    {
        "id": "p6",
        "name": "刘志仁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年9月",
        "birthplace": "湖南省新邵县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/刘志仁_(1964年)",
        "notes": "2021.03-2022.03任郴州市委书记。调任湘潭市委书记(2022.03-2024.08)。2024年12月28日被查，2025年被开除党籍。"
    },
    # ── 桂阳县 ──
    {
        "id": "p7",
        "name": "巫初华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "江西省宜丰县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂阳县委书记",
        "current_org": "中共桂阳县委员会",
        "source": "https://zh.wikipedia.org/wiki/桂阳县",
        "notes": "2021年7月起任桂阳县委书记。此前为桂阳县委副书记、县长。"
    },
    {
        "id": "p8",
        "name": "李志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "湖南省武冈市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂阳县县长",
        "current_org": "桂阳县人民政府",
        "source": "https://zh.wikipedia.org/wiki/桂阳县",
        "notes": "2021年4月起任桂阳县县长。80后县长。"
    },
    {
        "id": "p9",
        "name": "刘久正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年4月",
        "birthplace": "湖南省蓝山县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂阳县人大常委会主任",
        "current_org": "桂阳县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/桂阳县",
        "notes": "2021年7月起任职。"
    },
    {
        "id": "p10",
        "name": "肖晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年7月",
        "birthplace": "湖南省桂阳县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂阳县政协主席",
        "current_org": "中国人民政治协商会议桂阳县委员会",
        "source": "https://zh.wikipedia.org/wiki/桂阳县",
        "notes": "2016年12月起任职。"
    },
    # ── 资兴市 ──
    {
        "id": "p11",
        "name": "杨理诚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年",
        "birthplace": "湖南省湘阴县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "资兴市委书记",
        "current_org": "中共资兴市委员会",
        "source": "https://zh.wikipedia.org/wiki/资兴市",
        "notes": "2021年7月起任资兴市委书记。"
    },
    {
        "id": "p12",
        "name": "陈占华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年2月",
        "birthplace": "湖南省永兴县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "资兴市市长",
        "current_org": "资兴市人民政府",
        "source": "https://zh.wikipedia.org/wiki/资兴市",
        "notes": "2021年7月起任资兴市市长。"
    },
    {
        "id": "p13",
        "name": "王仁庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "湖南省安仁县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "资兴市人大常委会主任",
        "current_org": "资兴市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/资兴市",
        "notes": "2021年7月起任职。"
    },
    {
        "id": "p14",
        "name": "陈一之",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "资兴市政协主席",
        "current_org": "中国人民政治协商会议资兴市委员会",
        "source": "https://zh.wikipedia.org/wiki/资兴市",
        "notes": "2021年7月起任职。"
    },
    # ── 宜章县 ──
    {
        "id": "p15",
        "name": "张润槐",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1976年3月",
        "birthplace": "湖南省新晃侗族自治县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜章县委书记",
        "current_org": "中共宜章县委员会",
        "source": "https://zh.wikipedia.org/wiki/宜章县",
        "notes": "2021年5月起任宜章县委书记。"
    },
    {
        "id": "p16",
        "name": "邓生华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "湖南省桂阳县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜章县县长",
        "current_org": "宜章县人民政府",
        "source": "https://zh.wikipedia.org/wiki/宜章县",
        "notes": "2021年7月起任宜章县县长。80后县长。"
    },
    {
        "id": "p17",
        "name": "李秀芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年5月",
        "birthplace": "湖南省宜章县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜章县人大常委会主任",
        "current_org": "宜章县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/宜章县",
        "notes": "2021年7月起任职。"
    },
    {
        "id": "p18",
        "name": "周小文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜章县政协主席",
        "current_org": "中国人民政治协商会议宜章县委员会",
        "source": "https://zh.wikipedia.org/wiki/宜章县",
        "notes": "2021年7月起任职。"
    },
    # ── 永兴县 ──
    {
        "id": "p19",
        "name": "刘朝晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "湖南省攸县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永兴县委书记",
        "current_org": "中共永兴县委员会",
        "source": "https://zh.wikipedia.org/wiki/永兴县",
        "notes": "2021年5月起任永兴县委书记。"
    },
    {
        "id": "p20",
        "name": "宾心华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "湖南省衡山县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永兴县县长",
        "current_org": "永兴县人民政府",
        "source": "https://zh.wikipedia.org/wiki/永兴县",
        "notes": "2021年6月起任永兴县县长。80后县长。"
    },
    {
        "id": "p21",
        "name": "王梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "安徽省凤台县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永兴县人大常委会主任",
        "current_org": "永兴县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/永兴县",
        "notes": "2021年7月起任职。"
    },
    {
        "id": "p22",
        "name": "李玲华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年8月",
        "birthplace": "湖南省耒阳市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永兴县政协主席",
        "current_org": "中国人民政治协商会议永兴县委员会",
        "source": "https://zh.wikipedia.org/wiki/永兴县",
        "notes": "2021年7月起任职。"
    },
]

organizations = [
    {"id": 1, "name": "中共郴州市委员会", "type": "党委", "level": "地级市", "parent": "中共湖南省委员会", "location": "郴州市"},
    {"id": 2, "name": "郴州市人民政府", "type": "政府", "level": "地级市", "parent": "湖南省人民政府", "location": "郴州市"},
    {"id": 3, "name": "郴州市人大常委会", "type": "人大", "level": "地级市", "parent": "湖南省人大常委会", "location": "郴州市"},
    {"id": 4, "name": "中国人民政治协商会议郴州市委员会", "type": "政协", "level": "地级市", "parent": "湖南省政协", "location": "郴州市"},
    {"id": 5, "name": "中共桂阳县委员会", "type": "党委", "level": "县级", "parent": "中共郴州市委员会", "location": "桂阳县"},
    {"id": 6, "name": "桂阳县人民政府", "type": "政府", "level": "县级", "parent": "郴州市人民政府", "location": "桂阳县"},
    {"id": 7, "name": "桂阳县人大常委会", "type": "人大", "level": "县级", "parent": "郴州市人大常委会", "location": "桂阳县"},
    {"id": 8, "name": "中国人民政治协商会议桂阳县委员会", "type": "政协", "level": "县级", "parent": "郴州市政协", "location": "桂阳县"},
    {"id": 9, "name": "中共资兴市委员会", "type": "党委", "level": "县级", "parent": "中共郴州市委员会", "location": "资兴市"},
    {"id": 10, "name": "资兴市人民政府", "type": "政府", "level": "县级", "parent": "郴州市人民政府", "location": "资兴市"},
    {"id": 11, "name": "资兴市人大常委会", "type": "人大", "level": "县级", "parent": "郴州市人大常委会", "location": "资兴市"},
    {"id": 12, "name": "中国人民政治协商会议资兴市委员会", "type": "政协", "level": "县级", "parent": "郴州市政协", "location": "资兴市"},
    {"id": 13, "name": "中共宜章县委员会", "type": "党委", "level": "县级", "parent": "中共郴州市委员会", "location": "宜章县"},
    {"id": 14, "name": "宜章县人民政府", "type": "政府", "level": "县级", "parent": "郴州市人民政府", "location": "宜章县"},
    {"id": 15, "name": "宜章县人大常委会", "type": "人大", "level": "县级", "parent": "郴州市人大常委会", "location": "宜章县"},
    {"id": 16, "name": "中国人民政治协商会议宜章县委员会", "type": "政协", "level": "县级", "parent": "郴州市政协", "location": "宜章县"},
    {"id": 17, "name": "中共永兴县委员会", "type": "党委", "level": "县级", "parent": "中共郴州市委员会", "location": "永兴县"},
    {"id": 18, "name": "永兴县人民政府", "type": "政府", "level": "县级", "parent": "郴州市人民政府", "location": "永兴县"},
    {"id": 19, "name": "永兴县人大常委会", "type": "人大", "level": "县级", "parent": "郴州市人大常委会", "location": "永兴县"},
    {"id": 20, "name": "中国人民政治协商会议永兴县委员会", "type": "政协", "level": "县级", "parent": "郴州市政协", "location": "永兴县"},
    {"id": 21, "name": "中共湖南省委", "type": "党委", "level": "省级", "parent": "", "location": "长沙市"},
    {"id": 22, "name": "湖南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长沙市"},
    {"id": 23, "name": "湖南省公安厅", "type": "政府", "level": "省级", "parent": "湖南省人民政府", "location": "长沙市"},
    {"id": 24, "name": "中国有色金属工业总公司", "type": "事业单位", "level": "中央", "parent": "", "location": "北京市"},
    {"id": 25, "name": "中国铜铅锌集团公司", "type": "事业单位", "level": "中央", "parent": "", "location": "北京市"},
    {"id": 26, "name": "中央企业工委组织部", "type": "党委", "level": "中央", "parent": "", "location": "北京市"},
    {"id": 27, "name": "国务院国资委", "type": "政府", "level": "中央", "parent": "", "location": "北京市"},
    {"id": 28, "name": "中国铝业公司", "type": "事业单位", "level": "中央", "parent": "", "location": "北京市"},
    {"id": 29, "name": "长沙有色冶金研究设计院", "type": "事业单位", "level": "省级", "parent": "", "location": "长沙市"},
    {"id": 30, "name": "中共长沙市委", "type": "党委", "level": "地级市", "parent": "中共湖南省委", "location": "长沙市"},
    {"id": 31, "name": "中共株洲市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共湖南省纪委", "location": "株洲市"},
    {"id": 32, "name": "中共湘潭市委", "type": "党委", "level": "地级市", "parent": "中共湖南省委", "location": "湘潭市"},
]

positions = [
    # 阚保勇
    {"person_id": "p1", "org_id": 24, "title": "中国有色金属工业总公司 工作", "start": "1996.08", "end": "1998.04", "rank": "", "note": "早期职业生涯"},  # Fixed: org_id changed from 0 to 24
    {"person_id": "p1", "org_id": 25, "title": "中国铜铅锌集团公司 工作", "start": "1998.04", "end": "2000.12", "rank": "", "note": ""},
    {"person_id": "p1", "org_id": 26, "title": "中央企业工委组织部 工作", "start": "2000.12", "end": "2003.06", "rank": "", "note": ""},
    {"person_id": "p1", "org_id": 27, "title": "国务院国资委企业领导人员管理二局", "start": "2003.06", "end": "2004.03", "rank": "", "note": ""},
    {"person_id": "p1", "org_id": 28, "title": "中国铝业公司人事部干部处副处长、处长", "start": "2004.03", "end": "2011.03", "rank": "处级", "note": ""},
    {"person_id": "p1", "org_id": 29, "title": "长沙有色冶金研究设计院党委副书记、纪委书记", "start": "2011.03", "end": "2013.03", "rank": "副厅级", "note": ""},
    {"person_id": "p1", "org_id": 29, "title": "长沙有色冶金研究设计院党委书记", "start": "2013.03", "end": "2015.12", "rank": "副厅级", "note": ""},
    {"person_id": "p1", "org_id": 28, "title": "中国铝业公司人力资源部主任", "start": "2015.12", "end": "2020.10", "rank": "副厅级", "note": ""},
    {"person_id": "p1", "org_id": 1, "title": "郴州市委副书记、党校校长、政法委书记", "start": "2020.10", "end": "2021.05", "rank": "副厅级", "note": "空降郴州"},
    {"person_id": "p1", "org_id": 30, "title": "长沙市委副书记、政法委书记", "start": "2021.05", "end": "2022.03", "rank": "副厅级", "note": ""},
    {"person_id": "p1", "org_id": 2, "title": "郴州市委副书记、代市长/市长", "start": "2022.03", "end": "2026.05", "rank": "正厅级", "note": "升任正厅"},
    {"person_id": "p1", "org_id": 1, "title": "中共郴州市委书记", "start": "2026.05", "end": "present", "rank": "正厅级", "note": "由市长升任"},
    # 白云峰
    {"person_id": "p2", "org_id": 2, "title": "郴州市人民政府市长", "start": "2026.06", "end": "present", "rank": "正厅级", "note": "80后市长，此前曾在湖南省某市任职（待查）"},
    # 江波
    {"person_id": "p3", "org_id": 3, "title": "郴州市人大常委会主任", "start": "2022.01", "end": "present", "rank": "正厅级", "note": ""},
    # 陈跃文
    {"person_id": "p4", "org_id": 4, "title": "郴州市政协主席", "start": "2022.01", "end": "present", "rank": "正厅级", "note": ""},
    # 吴巨培
    {"person_id": "p5", "org_id": 31, "title": "株洲市纪委书记", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": "p5", "org_id": 23, "title": "湖南省公安厅副厅长", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": "p5", "org_id": 2, "title": "郴州市人民政府市长", "start": "2021.05", "end": "2022.03", "rank": "正厅级", "note": ""},
    {"person_id": "p5", "org_id": 1, "title": "中共郴州市委书记", "start": "2022.03", "end": "2026.05", "rank": "正厅级", "note": ""},
    # 刘志仁
    {"person_id": "p6", "org_id": 1, "title": "中共郴州市委书记", "start": "2021.03", "end": "2022.03", "rank": "正厅级", "note": ""},
    {"person_id": "p6", "org_id": 32, "title": "中共湘潭市委书记", "start": "2022.03", "end": "2024.08", "rank": "正厅级", "note": ""},
    # 桂阳县
    {"person_id": "p7", "org_id": 5, "title": "桂阳县委书记", "start": "2021.07", "end": "present", "rank": "正处级", "note": "此前为桂阳县县长"},
    {"person_id": "p8", "org_id": 6, "title": "桂阳县县长", "start": "2021.04", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p9", "org_id": 7, "title": "桂阳县人大常委会主任", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p10", "org_id": 8, "title": "桂阳县政协主席", "start": "2016.12", "end": "present", "rank": "正处级", "note": ""},
    # 资兴市
    {"person_id": "p11", "org_id": 9, "title": "资兴市委书记", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p12", "org_id": 10, "title": "资兴市市长", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p13", "org_id": 11, "title": "资兴市人大常委会主任", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p14", "org_id": 12, "title": "资兴市政协主席", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    # 宜章县
    {"person_id": "p15", "org_id": 13, "title": "宜章县委书记", "start": "2021.05", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p16", "org_id": 14, "title": "宜章县县长", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p17", "org_id": 15, "title": "宜章县人大常委会主任", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p18", "org_id": 16, "title": "宜章县政协主席", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    # 永兴县
    {"person_id": "p19", "org_id": 17, "title": "永兴县委书记", "start": "2021.05", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p20", "org_id": 18, "title": "永兴县县长", "start": "2021.06", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p21", "org_id": 19, "title": "永兴县人大常委会主任", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p22", "org_id": 20, "title": "永兴县政协主席", "start": "2021.07", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    # 阚保勇 ← 白云峰 (市长接替)
    {"person_a": "p2", "person_b": "p1", "type": "predecessor_successor", "context": "白云峰接替阚保勇任市长", "overlap_org": "郴州市人民政府", "overlap_period": "2026.06", "confidence": "confirmed"},
    # 阚保勇 — 吴巨培 (书记接替)
    {"person_a": "p5", "person_b": "p1", "type": "predecessor_successor", "context": "吴巨培因'另有任用'卸任，阚保勇由市长升任书记", "overlap_org": "中共郴州市委员会", "overlap_period": "2026.05", "confidence": "confirmed"},
    # 吴巨培 — 阚保勇 (市长交接)
    {"person_a": "p5", "person_b": "p1", "type": "predecessor_successor", "context": "吴巨培由市长升任书记后，阚保勇接任市长", "overlap_org": "郴州市人民政府", "overlap_period": "2022.03", "confidence": "confirmed"},
    # 刘志仁 — 吴巨培 (书记接替)
    {"person_a": "p6", "person_b": "p5", "type": "predecessor_successor", "context": "刘志仁调任湘潭后，吴巨培由市长升任书记", "overlap_org": "中共郴州市委员会", "overlap_period": "2022.03", "confidence": "confirmed"},
    # 刘志仁 — 吴巨培 (市长交接)
    {"person_a": "p6", "person_b": "p5", "type": "predecessor_successor", "context": "刘志仁任书记期间，吴巨培任市长", "overlap_org": "郴州市", "overlap_period": "2021.05-2022.03", "confidence": "confirmed"},
    # 阚保勇 — 吴巨培 (市长+书记共事)
    {"person_a": "p1", "person_b": "p5", "type": "overlap", "context": "阚保勇任市长期间，吴巨培任书记（搭档共事约4年）", "overlap_org": "郴州市", "overlap_period": "2022.03-2026.05", "confidence": "confirmed"},
]

# ══════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════

def build():
    """Run database + GEXF build."""

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "市委书记" in post or "县委书记" in post:
            if "副" not in post and "纪委" not in post:
                return ("255,50,50", 20.0)
        if "市长" in post or "县长" in post:
            if "副" not in post:
                return ("50,100,255", 20.0)
        if "副书记" in post:
            return ("50,100,255", 15.0)
        if "常委" in post and ("副" in post or "组织" in post or "政法" in post or "宣传" in post or "统战" in post):
            return ("100,150,255", 12.0)
        if "副" in post and ("市长" in post or "县长" in post or "书记" in post):
            return ("100,150,255", 12.0)
        if "人大" in post or "政协" in post:
            return ("200,255,255", 12.0)
        return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
        "事业单位": ("220,220,220", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG}领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{pid(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid_val = pid(pos["person_id"])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        a = pid(r["person_a"])
        b = pid(r["person_b"])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ──
    print(f"\n{'='*60}")
    print(f"{SLUG} Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
