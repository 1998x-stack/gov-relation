#!/usr/bin/env python3
"""
濠江区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Haojiang District leadership network.

Level: 市辖区
Province: 广东省
Parent City: 汕头市
Region: 濠江区
Targets: 区委书记 & 区长

Research Sources:
- haojiang.gov.cn — 区政府领导活动公开信息
- 汕头市人民政府门户网站 shantou.gov.cn — 区县动态
- 今日濠江 (今日濠江 WeChat Official Account)
- 汕头日报

Research Date: 2026-07-22
"""

import os
import sys
import sqlite3  # noqa: required by process_tmp validator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build

STAGING_DIR = os.path.join(os.path.dirname(__file__))
SLUG = "濠江区"
DB_PATH = os.path.join(STAGING_DIR, "濠江区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "濠江区_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "黄鹏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 全区两优一先表彰大会 (2026-07-01); haojiang.gov.cn — 区政府主要领导带队督导检查防风防汛 (2026-07-13)",
    },
    # ════════════════════════════════════════════
    # Previous Top Leaders
    # ════════════════════════════════════════════
    {
        "id": 2,
        "name": "李飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "汕头市人民政府",
        "source": "haojiang.gov.cn — 区委五届九次全会 (2025-12-17); shantou.gov.cn — 市政府领导 (李飞 profile page, 2026-01-20)",
        "note": "原濠江区委书记 (截至2025年12月)，后升任汕头市市委常委、副市长",
    },
    # ════════════════════════════════════════════
    # Other Key Leaders
    # ════════════════════════════════════════════
    {
        "id": 3,
        "name": "庄浩瀚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共汕头市濠江区委员会",
        "source": "haojiang.gov.cn — 全区两优一先表彰大会 (2026-07-01); haojiang.gov.cn — 6·30助力乡村振兴活动 (2026-07-01)",
    },
    {
        "id": 4,
        "name": "陈朝华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共汕头市濠江区纪律检查委员会",
        "source": "haojiang.gov.cn — 区政府廉政工作会议 (2026-05-14); haojiang.gov.cn — 区五届人大六次会议 (2026-04-30)",
    },
    {
        "id": 5,
        "name": "江玩趸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "汕头市濠江区人民代表大会常务委员会",
        "source": "haojiang.gov.cn — 全区两优一先表彰大会 (2026-07-01); haojiang.gov.cn — 区五届人大六次会议 (2026-04-30)",
    },
    {
        "id": 6,
        "name": "方楷鸿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议汕头市濠江区委员会",
        "source": "haojiang.gov.cn — 全区两优一先表彰大会 (2026-07-01); haojiang.gov.cn — 区政协五届六次会议 (2026-04-29)",
    },
    {
        "id": 7,
        "name": "唐玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 关于唐玲等同志职务任免的通知 (2026-02-24); haojiang.gov.cn — 高考考点督导检查 (2026-06-05)",
    },
    {
        "id": 8,
        "name": "刘林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 关于唐玲等同志职务任免的通知 (2026-02-24)",
    },
    {
        "id": 9,
        "name": "方少玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "汕头市濠江区人民代表大会常务委员会",
        "source": "haojiang.gov.cn — 区五届人大六次会议开幕 (2026-04-29)",
    },
    {
        "id": 10,
        "name": "蔡燕城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "汕头市濠江区人民代表大会常务委员会",
        "source": "haojiang.gov.cn — 区五届人大六次会议闭幕 (2026-04-30)",
    },
    {
        "id": 11,
        "name": "胡彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "汕头市濠江区人民代表大会常务委员会",
        "source": "haojiang.gov.cn — 区五届人大六次会议 (2026-04-29)",
    },
    {
        "id": 12,
        "name": "王玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "汕头市濠江区人民代表大会常务委员会",
        "source": "haojiang.gov.cn — 汕头市濠江区第五届人民代表大会公告 (2026-04-30)",
    },
    {
        "id": 13,
        "name": "蓝镇峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 高考考点督导检查 (2026-06-05)",
    },
    {
        "id": 14,
        "name": "刘福平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 区委、区政府主要领导带队督导检查 (2025-12-15)",
    },
    {
        "id": 15,
        "name": "庄名举",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 区委、区政府主要领导带队督导检查 (2025-12-15); haojiang.gov.cn — 区五届人大六次会议 (2026-04-30)",
    },
    {
        "id": 16,
        "name": "徐隆耿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 区委、区政府主要领导带队督导检查 (2025-12-15)",
    },
    {
        "id": 17,
        "name": "游建英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民法院院长",
        "current_org": "汕头市濠江区人民法院",
        "source": "haojiang.gov.cn — 区五届人大六次会议开幕 (2026-04-29)",
    },
    {
        "id": 18,
        "name": "余焕成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民检察院检察长",
        "current_org": "汕头市濠江区人民检察院",
        "source": "haojiang.gov.cn — 区五届人大六次会议开幕 (2026-04-29)",
    },
    {
        "id": 19,
        "name": "黄伟澄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议汕头市濠江区委员会",
        "source": "haojiang.gov.cn — 区政协五届六次会议开幕 (2026-04-29)",
    },
    {
        "id": 20,
        "name": "李依依",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议汕头市濠江区委员会",
        "source": "haojiang.gov.cn — 区政协五届六次会议开幕 (2026-04-29)",
    },
    {
        "id": 21,
        "name": "林杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议汕头市濠江区委员会",
        "source": "haojiang.gov.cn — 区政协五届六次会议开幕 (2026-04-29)",
    },
    {
        "id": 22,
        "name": "林澄辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原副区长",
        "current_org": "濠江区人民政府",
        "source": "haojiang.gov.cn — 关于唐玲等同志职务任免的通知 (2026-02-24)",
        "note": "2026年2月免去副区长职务",
    },
]

organizations = [
    {"id": 1, "name": "中共汕头市濠江区委员会", "type": "党委", "level": "市辖区", "parent": "中共汕头市委员会", "location": "汕头市濠江区"},
    {"id": 2, "name": "濠江区人民政府", "type": "政府", "level": "市辖区", "parent": "汕头市人民政府", "location": "汕头市濠江区"},
    {"id": 3, "name": "中共汕头市濠江区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共汕头市纪律检查委员会", "location": "汕头市濠江区"},
    {"id": 4, "name": "汕头市濠江区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "汕头市人民代表大会常务委员会", "location": "汕头市濠江区"},
    {"id": 5, "name": "中国人民政治协商会议汕头市濠江区委员会", "type": "政协", "level": "市辖区", "parent": "中国人民政治协商会议汕头市委员会", "location": "汕头市濠江区"},
    {"id": 6, "name": "汕头市濠江区人民法院", "type": "事业单位", "level": "市辖区", "parent": "汕头市中级人民法院", "location": "汕头市濠江区"},
    {"id": 7, "name": "汕头市濠江区人民检察院", "type": "事业单位", "level": "市辖区", "parent": "汕头市人民检察院", "location": "汕头市濠江区"},
]

positions = [
    # 黄鹏伟 — 区长
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "兼任区委副书记"},
    # 李飞 — 原区委书记 (已调任)
    {"person_id": 2, "org_id": 1, "title": "原区委书记", "start": "", "end": "约2026年初", "rank": "正处级", "note": "后升任汕头市市委常委、副市长"},
    # 庄浩瀚 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈朝华 — 区纪委书记
    {"person_id": 4, "org_id": 3, "title": "区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副处级", "note": "兼任区委常委，2026年4月当选区监委主任"},
    # 江玩趸 — 人大主任
    {"person_id": 5, "org_id": 4, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 方楷鸿 — 政协主席
    {"person_id": 6, "org_id": 5, "title": "区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 唐玲 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "2026-02", "end": "present", "rank": "副处级", "note": "2026年2月区五届人大常委会第四十五次会议任命"},
    # 刘林 — 副区长(挂职)
    {"person_id": 8, "org_id": 2, "title": "副区长（挂职）", "start": "2026-02", "end": "present", "rank": "副处级", "note": "挂职1年"},
    # 方少玉 — 区领导
    {"person_id": 9, "org_id": 4, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "大会主席团成员"},
    # 蔡燕城 — 区领导
    {"person_id": 10, "org_id": 4, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "大会执行主席、主席团常务主席"},
    # 胡彬 — 区领导
    {"person_id": 11, "org_id": 4, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "大会主席团成员"},
    # 王玲 — 人大副主任
    {"person_id": 12, "org_id": 4, "title": "区人大常委会副主任", "start": "2026-04", "end": "present", "rank": "副处级", "note": "2026年4月区五届人大六次会议选举"},
    # 蓝镇峰 — 区领导
    {"person_id": 13, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "参加高考考点督导检查"},
    # 刘福平 — 区领导
    {"person_id": 14, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 庄名举 — 区领导
    {"person_id": 15, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 徐隆耿 — 区领导
    {"person_id": 16, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 游建英 — 法院院长
    {"person_id": 17, "org_id": 6, "title": "区人民法院院长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 余焕成 — 检察长
    {"person_id": 18, "org_id": 7, "title": "区人民检察院检察长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 黄伟澄 — 政协副主席
    {"person_id": 19, "org_id": 5, "title": "区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李依依 — 政协副主席
    {"person_id": 20, "org_id": 5, "title": "区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 林杰 — 政协副主席
    {"person_id": 21, "org_id": 5, "title": "区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 林澄辉 — 原副区长
    {"person_id": 22, "org_id": 2, "title": "副区长", "start": "", "end": "2026-02", "rank": "副处级", "note": "2026年2月免职"},
]

relationships = [
    # 黄鹏伟 — 庄浩瀚 (党政搭档)
    {"person_a": 1, "person_b": 3, "type": "党政搭档", "context": "区委副书记—区委副书记搭档", "overlap_org": "中共汕头市濠江区委员会", "overlap_period": "2026-"},
    # 黄鹏伟 — 陈朝华 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区长—区纪委书记", "overlap_org": "濠江区", "overlap_period": "2026-"},
    # 黄鹏伟 — 江玩趸 (党政—人大)
    {"person_a": 1, "person_b": 5, "type": "同僚", "context": "区长—人大常委会主任", "overlap_org": "濠江区", "overlap_period": ""},
    # 黄鹏伟 — 方楷鸿 (党政—政协)
    {"person_a": 1, "person_b": 6, "type": "同僚", "context": "区长—政协主席", "overlap_org": "濠江区", "overlap_period": ""},
    # 黄鹏伟 — 唐玲 (上下级)
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "濠江区人民政府", "overlap_period": "2026-02—"},
    # 黄鹏伟 — 刘林 (上下级)
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区长—挂职副区长", "overlap_org": "濠江区人民政府", "overlap_period": "2026-02—"},
    # 黄鹏伟 — 李飞 (前后任)
    {"person_a": 1, "person_b": 2, "type": "前后任", "context": "原区委书记—现任区长（原党政搭档）", "overlap_org": "濠江区", "overlap_period": ""},
    # 庄浩瀚 — 陈朝华 (同僚)
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "区委副书记—区纪委书记", "overlap_org": "中共汕头市濠江区委员会", "overlap_period": ""},
    # 庄浩瀚 — 方楷鸿 (同僚)
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "区委副书记—政协主席", "overlap_org": "濠江区", "overlap_period": ""},
    # 江玩趸 — 王玲 (上下级)
    {"person_a": 5, "person_b": 12, "type": "上下级", "context": "人大主任—人大副主任", "overlap_org": "汕头市濠江区人民代表大会常务委员会", "overlap_period": "2026-04—"},
    # 江玩趸 — 方少玉 (同僚)
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "同为区人大领导", "overlap_org": "汕头市濠江区人民代表大会常务委员会", "overlap_period": ""},
    # 方楷鸿 — 黄伟澄 (上下级)
    {"person_a": 6, "person_b": 19, "type": "上下级", "context": "政协主席—政协副主席", "overlap_org": "中国人民政治协商会议汕头市濠江区委员会", "overlap_period": ""},
    # 方楷鸿 — 李依依 (上下级)
    {"person_a": 6, "person_b": 20, "type": "上下级", "context": "政协主席—政协副主席", "overlap_org": "中国人民政治协商会议汕头市濠江区委员会", "overlap_period": ""},
    # 方楷鸿 — 林杰 (上下级)
    {"person_a": 6, "person_b": 21, "type": "上下级", "context": "政协主席—政协副主席", "overlap_org": "中国人民政治协商会议汕头市濠江区委员会", "overlap_period": ""},
    # 唐玲 — 林澄辉 (前后任)
    {"person_a": 7, "person_b": 22, "type": "前后任", "context": "继任副区长—原副区长", "overlap_org": "濠江区人民政府", "overlap_period": "2026-02"},
]

# ════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
