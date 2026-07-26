#!/usr/bin/env python3
"""
阳曲县领导班子工作关系网络 — 数据构建脚本
调查日期: 2026-07-26
信息来源: 公开新闻报道、百度百科、阳曲县人民政府门户网站 (www.yangqu.gov.cn)
"""

import sqlite3
import os
from datetime import datetime

SLUG = "阳曲县"
TODAY = "2026-07-26"
AS_OF = "2026-07-26"
PROVINCE = "山西省"
CITY = "太原市"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR.endswith("scripts/build"):
    REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
elif "data/tmp" in BASE_DIR:
    # Running from staging dir - repo root is grandparent of data/tmp
    parts = BASE_DIR.split(os.sep)
    # Find where 'data/tmp' is
    try:
        tmp_idx = parts.index("tmp")
        REPO_ROOT = os.sep.join(parts[:tmp_idx - 1])
    except ValueError:
        REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
else:
    REPO_ROOT = BASE_DIR
DB_PATH = os.path.join(REPO_ROOT, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", f"{SLUG}_network.gexf")

# =========================================================================
# Research Data
# =========================================================================

persons = [
    # ── Current Core Leaders ──
    {
        "id": 1,
        "name": "姬发军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "山西娄烦",
        "education": "中央党校大学、工学硕士",
        "party_join": "2000年8月",
        "work_start": "1996年8月",
        "current_post": "县委书记、县长",
        "current_org": "中共阳曲县委、阳曲县人民政府",
        "source": "山西商人网(阳曲政府网消息) (https://www.shanxishangren.com/b2b/news/show.php?itemid=170127); 网易新闻 (https://c.m.163.com/news/a/JS51I18U0535B1FH.html)",
        "notes": "兼任阳曲现代农业产业示范区党工委书记、管委会主任。2025年4月由县长升任县委书记，党政一肩挑。一级调研员"
    },
    # ── Deputy Party Secretaries (县委副书记) ──
    {
        "id": 2,
        "name": "吴英志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、统战部部长",
        "current_org": "中共阳曲县委",
        "source": "中新网 (https://www.sx.chinanews.com.cn/news/2024/0807/234163.html); 山西大学新闻 (https://gnhzc.sxu.edu.cn/hzxx/xdhz/cb91b0baf43548848f12df8f40eebfb6.htm)",
        "notes": "曾任阳曲县委常委、组织部部长，后任县委副书记、统战部部长"
    },
    # ── Standing Committee Members (县委常委) ──
    {
        "id": 3,
        "name": "孙慧生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650); 中新网 (https://www.sx.chinanews.com.cn/news/2024/1216/237539.html)",
        "notes": "常务副县长，负责县政府日常工作"
    },
    {
        "id": 4,
        "name": "王庆丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共阳曲县委宣传部、阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650)",
        "notes": "分管农业农村、水务、林业、乡村振兴、信访、融媒体等工作"
    },
    {
        "id": 5,
        "name": "郭志红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650)",
        "notes": "分管科技、审计、市场监管、供销社等工作"
    },
    {
        "id": 6,
        "name": "阴笑弘",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650); (https://www.shanxishangren.com/b2b/news/show.php?itemid=160912)",
        "notes": "分管招商引资、金融、投资促进等工作"
    },
    {
        "id": 7,
        "name": "武晓俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共阳曲县委政法委",
        "source": "粉丝服务网 (https://www.fensifuwu.com/emotion/me/1976445.html)",
        "notes": ""
    },
    {
        "id": 8,
        "name": "范旭宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部政委",
        "current_org": "阳曲县人民武装部",
        "source": "中新网 (https://www.sx.chinanews.com.cn/news/2024/0807/234163.html)",
        "notes": ""
    },
    # ── Other Deputy County Mayors (副县长) ──
    {
        "id": 9,
        "name": "马有利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650)",
        "notes": "分管自然资源、住建、交通、环卫、城建等工作"
    },
    {
        "id": 10,
        "name": "申彩萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长(已卸任)",
        "current_org": "阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650); 网易新闻 (https://www.163.com/dy/article/KU37ISV705149E7M.html)",
        "notes": "分管人社、民政、退役军人事务等。2026年5月已卸任"
    },
    {
        "id": 11,
        "name": "张建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650); 粉丝服务网 (https://www.fensifuwu.com/emotion/me/0c7bdb12babcae9c4232fbae41af993f.html)",
        "notes": "分管教育、文旅、审批等工作"
    },
    {
        "id": 12,
        "name": "游胜文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阳曲县人民政府",
        "source": "山西商人网 (https://www.shanxishangren.com/b2b/news/show.php?itemid=149650)",
        "notes": "分管工信、商务、统计、园区建设等工作"
    },
    {
        "id": 13,
        "name": "刘波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长(已卸任)",
        "current_org": "阳曲县公安局",
        "source": "网易新闻 (https://www.163.com/dy/article/KU37ISV705149E7M.html)",
        "notes": "主管公安、司法等工作。2026年5月已卸任"
    },
    {
        "id": 14,
        "name": "李峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "阳曲县公安局",
        "source": "网易新闻 (https://www.163.com/dy/article/KU37ISV705149E7M.html)",
        "notes": "2026年5月新任副县长兼公安局长"
    },
    {
        "id": 15,
        "name": "乔馨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阳曲县人民政府",
        "source": "网易新闻 (https://www.163.com/dy/article/KU37ISV705149E7M.html)",
        "notes": "2026年5月新任副县长"
    },
    # ── County People's Congress (县人大) ──
    {
        "id": 16,
        "name": "王志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "阳曲县人大常委会",
        "source": "中新网 (https://www.sx.chinanews.com/news/2025/1212/245742.html); 360百科 (https://baike.so.com/doc/5392226-24986080.html)",
        "notes": "曾任阳曲县委常委"
    },
    # ── County CPPCC (县政协) ──
    {
        "id": 17,
        "name": "于文成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "山西阳曲",
        "education": "中央党校大学",
        "party_join": "1996年11月",
        "work_start": "1991年7月",
        "current_post": "县政协党组书记、主席",
        "current_org": "阳曲县政协",
        "source": "中文百科全书 (https://www.newton.com.tw/wiki/%E6%96%BC%E6%96%87%E6%88%90/58597057)",
        "notes": "历任泥屯镇、大盂镇、侯村乡、西凌井乡等乡镇职务，曾任副县长、县委常委"
    },
    # ── Predecessors (前任) ──
    {
        "id": 18,
        "name": "李京京",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "山东沂水",
        "education": "研究生、工程硕士",
        "party_join": "1996年10月",
        "work_start": "1997年7月",
        "current_post": "前任县委书记",
        "current_org": "中共阳曲县委(已离任)",
        "source": "百度百科 (https://baike.baidu.com/item/%E6%9D%8E%E4%BA%AC%E4%BA%AC/19926837); 网易新闻 (https://c.m.163.com/news/a/JRLKGJ600535B1FH.html)",
        "notes": "2019年1月任阳曲代县长，2019年2月任县长，2022年3月任县委书记。2025年3月调任清徐县委书记"
    },
    {
        "id": 19,
        "name": "裴耀军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年7月",
        "birthplace": "山西榆社",
        "education": "大学(兰州大学历史系)",
        "party_join": "1996年6月",
        "work_start": "1991年6月",
        "current_post": "前任县委书记",
        "current_org": "中共阳曲县委(已离任)",
        "source": "百度百科 (https://baike.baidu.com/item/%E8%A3%B4%E8%80%80%E5%86%9B/7381004); 澎湃新闻 (https://m.thepaper.cn/newsDetail_forward_2786529)",
        "notes": "2016年8月任阳曲县长，2019年1月任县委书记。2022年2月升任太原市人大常委会副主任，后任太原市委常委、秘书长、常务副市长。2026年任山西省工商联党组书记"
    },
    {
        "id": 20,
        "name": "刘晋萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1965年1月",
        "birthplace": "山西五台",
        "education": "中央党校研究生",
        "party_join": "1985年12月",
        "work_start": "1987年7月",
        "current_post": "前任县委书记",
        "current_org": "中共阳曲县委(已离任)",
        "source": "人民网 (http://renshi.people.com.cn/n1/2016/0105/c139617-28015162.html); 澎湃新闻 (https://www.thepaper.cn/newsDetail_forward_1417799)",
        "notes": "曾任太原市团委副书记、晋源区委宣传部部长、太原市贸促会会长。2013年4月任阳曲县长，2015年12月任县委书记。后调任吕梁市副市长"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共阳曲县委",
        "type": "党委",
        "level": "县",
        "parent": "中共太原市委",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 2,
        "name": "阳曲县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "太原市人民政府",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 3,
        "name": "中共阳曲县委统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共阳曲县委",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 4,
        "name": "中共阳曲县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共阳曲县委",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 5,
        "name": "中共阳曲县委政法委",
        "type": "党委",
        "level": "县",
        "parent": "中共阳曲县委",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 6,
        "name": "阳曲县人民武装部",
        "type": "党委",
        "level": "县",
        "parent": "太原警备区",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 7,
        "name": "阳曲县公安局",
        "type": "政府",
        "level": "县",
        "parent": "阳曲县人民政府",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 8,
        "name": "阳曲县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "太原市人大常委会",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 9,
        "name": "阳曲县政协",
        "type": "政协",
        "level": "县",
        "parent": "太原市政协",
        "location": "山西省太原市阳曲县"
    },
    {
        "id": 10,
        "name": "阳曲现代农业产业示范区",
        "type": "政府",
        "level": "县",
        "parent": "阳曲县人民政府",
        "location": "山西省太原市阳曲县"
    },
]

positions = [
    # 姬发军
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "2025-04", "end": "present", "rank": "正处级(一级调研员)", "note": "2025年4月任县委书记"},
    {"person_id": "p1", "org_id": 2, "title": "县长", "start": "2022-04", "end": "present", "rank": "正处级", "note": "2022年4月任代县长，2022年5月任县长"},
    {"person_id": "p1", "org_id": 10, "title": "党工委书记、管委会主任", "start": "2025-04", "end": "present", "rank": "", "note": "兼任"},
    # 姬发军早期履历
    {"person_id": "p1", "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "", "note": "曾任阳曲县副县长"},
    {"person_id": "p1", "org_id": 0, "title": "太原广播电视台党委副书记、副台长、总编辑", "start": "", "end": "2022-04", "rank": "", "note": "调任阳曲前任职太原广播电视台"},
    # 吴英志
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 3, "title": "统战部部长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 1, "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "", "note": "曾任职务"},
    # 孙慧生
    {"person_id": "p3", "org_id": 2, "title": "县委常委、副县长(常务)", "start": "", "end": "present", "rank": "", "note": "负责县政府日常工作"},
    # 王庆丰
    {"person_id": "p4", "org_id": 4, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": "p4", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "", "note": "分管农业农村等工作"},
    # 郭志红
    {"person_id": "p5", "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "", "note": "分管科技、审计、市场监管"},
    # 阴笑弘
    {"person_id": "p6", "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "", "note": "分管招商引资、金融"},
    # 武晓俊
    {"person_id": "p7", "org_id": 5, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 范旭宇
    {"person_id": "p8", "org_id": 6, "title": "县委常委、人武部政委", "start": "", "end": "present", "rank": "", "note": ""},
    # 马有利
    {"person_id": "p9", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "", "note": "分管自然资源、住建、交通"},
    # 申彩萍
    {"person_id": "p10", "org_id": 2, "title": "副县长", "start": "", "end": "2026-05", "rank": "", "note": "已卸任"},
    # 张建
    {"person_id": "p11", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "", "note": "分管教育、文旅、审批"},
    # 游胜文
    {"person_id": "p12", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "", "note": "分管工信、商务、统计"},
    # 刘波
    {"person_id": "p13", "org_id": 7, "title": "副县长、县公安局局长", "start": "", "end": "2026-05", "rank": "", "note": "已卸任"},
    # 李峰
    {"person_id": "p14", "org_id": 7, "title": "副县长、县公安局局长", "start": "2026-05", "end": "present", "rank": "", "note": "新任"},
    # 乔馨
    {"person_id": "p15", "org_id": 2, "title": "副县长", "start": "2026-05", "end": "present", "rank": "", "note": "新任"},
    # 王志勇
    {"person_id": "p16", "org_id": 8, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 于文成
    {"person_id": "p17", "org_id": 9, "title": "县政协主席", "start": "2021-04", "end": "present", "rank": "", "note": "2021年4月当选"},
    # 李京京
    {"person_id": "p18", "org_id": 1, "title": "县委书记", "start": "2022-03", "end": "2025-03", "rank": "正处级", "note": "调任清徐县委书记"},
    {"person_id": "p18", "org_id": 2, "title": "县长", "start": "2019-01", "end": "2022-03", "rank": "正处级", "note": "2019年1月任代县长，2019年2月任县长"},
    # 裴耀军
    {"person_id": "p19", "org_id": 1, "title": "县委书记", "start": "2019-01", "end": "2022-02", "rank": "正处级", "note": "2022年2月升任太原市人大常委会副主任"},
    {"person_id": "p19", "org_id": 2, "title": "县长", "start": "2016-08", "end": "2019-01", "rank": "正处级", "note": ""},
    # 刘晋萍
    {"person_id": "p20", "org_id": 1, "title": "县委书记", "start": "2015-12", "end": "2018-12", "rank": "正处级", "note": "后任吕梁市副市长"},
    {"person_id": "p20", "org_id": 2, "title": "县长", "start": "2012-07", "end": "2015-12", "rank": "正处级", "note": "2012年7月任代县长，2013年4月任县长"},
]

relationships = [
    # 姬发军 — 李京京 (predecessor-successor 县委书记)
    {"person_a": "p1", "person_b": "p18", "type": "predecessor_successor", "context": "李京京调任清徐县委书记后，姬发军由县长升任县委书记", "overlap_org": "阳曲县", "overlap_period": "2022-2025", "confidence": "confirmed"},
    # 姬发军 — 李京京 (predecessor-successor 县长)
    {"person_a": "p1", "person_b": "p18", "type": "predecessor_successor", "context": "姬发军接替李京京任县长", "overlap_org": "阳曲县人民政府", "overlap_period": "2022", "confidence": "confirmed"},
    # 李京京 — 裴耀军 (predecessor-successor 县委书记)
    {"person_a": "p18", "person_b": "p19", "type": "predecessor_successor", "context": "裴耀军升任太原市人大常委会副主任后，李京京由县长升任县委书记", "overlap_org": "阳曲县", "overlap_period": "2019-2022", "confidence": "confirmed"},
    # 裴耀军 — 刘晋萍 (predecessor-successor 县委书记)
    {"person_a": "p19", "person_b": "p20", "type": "predecessor_successor", "context": "刘晋萍调任后裴耀军接任县委书记", "overlap_org": "中共阳曲县委", "overlap_period": "2016-2019", "confidence": "confirmed"},
    # 姬发军 — 孙慧生 (colleague, 县长与常务副县长)
    {"person_a": "p1", "person_b": "p3", "type": "overlap", "context": "党政主要领导与常务副县长搭档", "overlap_org": "阳曲县人民政府", "overlap_period": "2022至今", "confidence": "confirmed"},
    # 姬发军 — 吴英志 (colleague, 县长与副书记)
    {"person_a": "p1", "person_b": "p2", "type": "overlap", "context": "党政正副职搭档", "overlap_org": "中共阳曲县委", "overlap_period": "至今", "confidence": "confirmed"},
    # 姬发军 — 阴笑弘 (colleague)
    {"person_a": "p1", "person_b": "p6", "type": "overlap", "context": "正副县长工作关系", "overlap_org": "阳曲县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 姬发军 — 郭志红 (colleague)
    {"person_a": "p1", "person_b": "p5", "type": "overlap", "context": "正副县长工作关系", "overlap_org": "阳曲县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 姬发军 — 王庆丰 (colleague)
    {"person_a": "p1", "person_b": "p4", "type": "overlap", "context": "正副县长工作关系", "overlap_org": "阳曲县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 姬发军 — 马有利 (colleague)
    {"person_a": "p1", "person_b": "p9", "type": "overlap", "context": "正副县长工作关系", "overlap_org": "阳曲县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 姬发军 — 张建 (colleague)
    {"person_a": "p1", "person_b": "p11", "type": "overlap", "context": "正副县长工作关系", "overlap_org": "阳曲县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 姬发军 — 游胜文 (colleague)
    {"person_a": "p1", "person_b": "p12", "type": "overlap", "context": "正副县长工作关系", "overlap_org": "阳曲县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 吴英志 — 王庆丰 (colleague in 县委班子)
    {"person_a": "p2", "person_b": "p4", "type": "overlap", "context": "县委领导班子成员", "overlap_org": "中共阳曲县委", "overlap_period": "至今", "confidence": "confirmed"},
    # 于文成曾任副县长、县委常委 — 姬发军 (overlap)
    {"person_a": "p17", "person_b": "p1", "type": "overlap", "context": "于文成曾任副县长、县委常委，与姬发军有工作交集", "overlap_org": "阳曲县人民政府/中共阳曲县委", "overlap_period": "", "confidence": "plausible"},
]


# =========================================================================
# Database Build
# =========================================================================

def build():
    """Run database + GEXF build."""
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
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
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
        if "县委书记" in post and "副" not in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "纪委" in post:
            return ("255,165,0", 12.0)
        elif "常委" in post and "副" in post:
            return ("100,150,255", 12.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and "县长" in post and "卸任" not in post:
            return ("100,100,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        elif "前任" in post or "卸任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>阳曲县领导班子工作关系网络 - {AS_OF}</description>')
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
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
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
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
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

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"阳曲县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
