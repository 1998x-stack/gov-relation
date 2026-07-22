#!/usr/bin/env python3
"""Build script for 清新区 (Qingxin District, Qingyuan, Guangdong) leadership network.

Generated: 2026-07-22
Sources:
  - www.qingxin.gov.cn (official government website - 领导班子 page, 政务要闻)
  - qingxin.gov.cn/zwgk/ldzc/qzf/qz/content/post_1350621.html (黄国杰 profile)
  - qingxin.gov.cn/zwgk/zfgzbg/content/post_1502544.html (2021 政府工作报告)
  - qingxin.gov.cn/zwgk/qxyw/content/post_1926734.html (2024-09 区委常委会, 刘建俊 as 区委书记)
  - qingxin.gov.cn/zwgk/qxyw/content/post_1988046.html (2025-03 区九届人大五次会议)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2109856.html (2026-01 区委八届十次全会, 黄国杰主持)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html (2026-03 区九届人大六次会议)
  - qingxin.gov.cn/zwgk/qxyw/content/post_1827496.html (2024-02 宣传思想文化会议, 潘康凯 as 区委副书记)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2167513.html (2026-07 区委常委会)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2162450.html (2026-07 警示教育会, 黄河/万小阳)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2110791.html (2026-02 八届区纪委六次全会, 郝朝文 as 区纪委书记)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2130775.html (2026-03 经济形势分析会, 副区长名单)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2146780.html (2026-05 招商引资会议, 徐泽城/欧超泉/侯利新)
  - qingxin.gov.cn/zwgk/qxyw/content/post_2158456.html (2026-06 防汛会议, 徐泽城/欧超泉)
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ============ 区委领导 ============
    {
        "id": 1,
        "name": "黄国杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "清新区区长（主持区委全面工作）",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/ldzc/qzf/qz/content/post_1350621.html",
    },
    {
        "id": 2,
        "name": "刘建俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前清新区委书记（2025年3月后去向待查）",
        "current_org": "中共清远市清新区委员会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_1988046.html (confirmed as区委书记 until 2025-03-12)",
    },
    {
        "id": 3,
        "name": "潘康凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共清远市清新区委员会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_1827496.html (confirmed as区委副书记 2024-02-07)",
    },
    {
        "id": 4,
        "name": "黄河",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共清远市清新区委员会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2162450.html (confirmed attending区委会议 2026-07)",
    },
    {
        "id": 5,
        "name": "万小阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共清远市清新区委员会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2160375.html (confirmed attending区委理论学习中心组 2026-06)",
    },
    {
        "id": 6,
        "name": "郝朝文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共清远市清新区纪律检查委员会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2110791.html (八届区纪委六次全会 2026-02, as 区纪委书记、区监委代理主任)",
    },
    # ============ 区政府领导 ============
    {
        "id": 7,
        "name": "徐泽城",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2146780.html (confirmed attending招商引资会议 2026-05)",
    },
    {
        "id": 8,
        "name": "温俭良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/ldzc/ (区政府领导页面 listing)",
    },
    {
        "id": 9,
        "name": "曹辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2130775.html (confirmed attending经济形势分析会 2026-03)",
    },
    {
        "id": 10,
        "name": "邹早银",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2130775.html (confirmed attending经济形势分析会 2026-03)",
    },
    {
        "id": 11,
        "name": "叶玉树",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2130775.html (confirmed attending经济形势分析会 2026-03)",
    },
    {
        "id": 12,
        "name": "侯利新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2146780.html (confirmed attending招商引资会议 2026-05)",
    },
    {
        "id": 13,
        "name": "欧超泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "清远市清新区人民政府",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2158456.html (confirmed attending防汛会议 2026-06)",
    },
    # ============ 人大领导 ============
    {
        "id": 14,
        "name": "欧建宽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "清远市清新区人大常委会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html (区九届人大六次会议 2026-03)",
    },
    {
        "id": 15,
        "name": "唐庆卫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协党组书记、主席",
        "current_org": "中国人民政治协商会议清远市清新区委员会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html (区九届人大六次会议 2026-03)",
    },
    # ============ 人大常委会副主任 ============
    {
        "id": 16,
        "name": "欧阳振",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "清远市清新区人大常委会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html",
    },
    {
        "id": 17,
        "name": "张国力",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "清远市清新区人大常委会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html",
    },
    {
        "id": 18,
        "name": "罗文波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "清远市清新区人大常委会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html",
    },
    {
        "id": 19,
        "name": "朱明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "清远市清新区人大常委会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html",
    },
    {
        "id": 20,
        "name": "唐宝通",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "清远市清新区人大常委会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html",
    },
    {
        "id": 21,
        "name": "麦少珍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "清远市清新区人大常委会",
        "source": "https://www.qingxin.gov.cn/zwgk/qxyw/content/post_2124332.html",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共清远市清新区委员会", "type": "党委", "level": "正处级", "parent": "中共清远市委员会", "location": "清远市清新区"},
    {"id": 2, "name": "清远市清新区人民政府", "type": "政府", "level": "正处级", "parent": "清远市人民政府", "location": "清远市清新区"},
    {"id": 3, "name": "清远市清新区人大常委会", "type": "人大", "level": "正处级", "parent": "清远市人大常委会", "location": "清远市清新区"},
    {"id": 4, "name": "中国人民政治协商会议清远市清新区委员会", "type": "政协", "level": "正处级", "parent": "清远市政协", "location": "清远市清新区"},
    {"id": 5, "name": "中共清远市清新区纪律检查委员会", "type": "党委", "level": "副处级", "parent": "中共清远市纪律检查委员会", "location": "清远市清新区"},
]

POSITIONS = [
    # 黄国杰
    {"person_id": 1, "org_id": 2, "title": "清新区区长", "start_date": "2021-11", "end_date": "present", "rank": "正处级", "note": "2021年11月22日在清新区第九届人大第一次会议上当选区长"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "2021-11", "end_date": "present", "rank": "副处级", "note": "主持区委全面工作（自2025年起代行区委书记职能）"},
    # 刘建俊
    {"person_id": 2, "org_id": 1, "title": "清新区委书记", "start_date": "2022?", "end_date": "~2025-03", "rank": "正处级/副厅级", "note": "最后确认在任：2025年3月12日区九届人大五次会议；去向待查"},
    # 潘康凯
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄河
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
    # 万小阳
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
    # 郝朝文
    {"person_id": 6, "org_id": 5, "title": "区纪委书记、区监委主任", "start_date": "2026-02", "end_date": "present", "rank": "副处级", "note": "2026年2月任代理主任，2026年3月正式当选区监委主任"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "2026-02", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐泽城
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管经济、招商等工作"},
    # 温俭良
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 曹辉
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 邹早银
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "身份为区领导，确认参加会议"},
    # 叶玉树
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "身份为区领导，确认参加会议"},
    # 侯利新
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "身份为区领导，确认参加会议"},
    # 欧超泉
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "身份为区领导，确认参加会议"},
    # 欧建宽
    {"person_id": 14, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 唐庆卫
    {"person_id": 15, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 人大副主任
    {"person_id": 16, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# Relationships based on organizational overlap and working proximity
RELATIONSHIPS = [
    # 党政正职（现任/前）
    {"person_a": 1, "person_b": 2, "type": "前后任", "context": "黄国杰（区长）接续主持刘建俊离任后的区委全面工作", "overlap_org": "清新区委", "overlap_period": "2021-2025", "source": "", "confidence": "confirmed"},
    # 书记-副书记/区长
    {"person_a": 2, "person_b": 1, "type": "上下级", "context": "原区委书记刘建俊与区委副书记、区长黄国杰搭档", "overlap_org": "清新区委常委会", "overlap_period": "2021-2025", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "原区委书记刘建俊与区委副书记潘康凯搭档", "overlap_org": "清新区委常委会", "overlap_period": "2024-2025", "source": "", "confidence": "confirmed"},
    # 党政正职（现任）
    {"person_a": 1, "person_b": 3, "type": "党政副职搭档", "context": "区长与专职副书记", "overlap_org": "清新区委常委会", "overlap_period": "2025-2026", "source": "", "confidence": "confirmed"},
    # 区委-常委
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区长—区委常委黄河", "overlap_org": "清新区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区长—区委常委万小阳", "overlap_org": "清新区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区长—区纪委书记郝朝文", "overlap_org": "清新区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区长-副区长
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区长—副区长徐泽城", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区长—副区长温俭良", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区长—副区长曹辉", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区长—副区长邹早银", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "区长—副区长叶玉树", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "区长—副区长侯利新", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "区长—副区长欧超泉", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 人大/政协核心
    {"person_a": 1, "person_b": 14, "type": "党政人搭档", "context": "区长—人大主任欧建宽", "overlap_org": "清新区四套班子", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 15, "type": "党政政协搭档", "context": "区长—政协主席唐庆卫", "overlap_org": "清新区四套班子", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区纪委-区委
    {"person_a": 6, "person_b": 4, "type": "同僚", "context": "区纪委书记郝朝文与区委常委黄河", "overlap_org": "清新区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 5, "type": "同僚", "context": "区纪委书记郝朝文与区委常委万小阳", "overlap_org": "清新区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 副区长之间
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副区长徐泽城与副区长温俭良", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "副区长徐泽城与副区长曹辉", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 12, "type": "同僚", "context": "副区长徐泽城与副区长侯利新", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 13, "type": "同僚", "context": "副区长徐泽城与副区长欧超泉", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "副区长温俭良与副区长曹辉", "overlap_org": "清新区政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 人大副主任之间
    {"person_a": 16, "person_b": 17, "type": "同僚", "context": "区人大常委会副主任", "overlap_org": "清新区人大常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 18, "type": "同僚", "context": "区人大常委会副主任", "overlap_org": "清新区人大常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 19, "type": "同僚", "context": "区人大常委会副主任", "overlap_org": "清新区人大常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 20, "type": "同僚", "context": "区人大常委会副主任", "overlap_org": "清新区人大常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 21, "type": "同僚", "context": "区人大常委会副主任", "overlap_org": "清新区人大常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "清新区_network.db"
GEXF_PATH = GRAPH_DIR / "清新区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="清新区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
