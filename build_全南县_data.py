#!/usr/bin/env python3
"""
Build 全南县 (Quannan County) government personnel network database and GEXF graph.

全南县 is a county under 赣州市, 江西省.
Current leadership as of 2026-07-15:
- 张人富: 全南县委书记 (former 县长, promoted ~early July 2026)
- 杨春景: 全南县委副书记、县长候选人 (former 县委常委、副县长, promoted July 2026)
- 边建忠: 前任县委书记、县长 (departed late June/early July 2026, appointed 龙南市委书记)
- 冯健全: 全南县委副书记
Based on official sources from www.quannan.gov.cn news pages, Baidu Baike, and official appointment notices.

"""
import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in BASE:
    REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
else:
    REPO_ROOT = BASE

today = datetime.now().strftime("%Y-%m-%d")

DB_REL = "data/database/全南县_network.db"
GEXF_REL = "data/graph/全南县_network.gexf"

DB_PATH = os.path.join(REPO_ROOT, DB_REL)
GEXF_PATH = os.path.join(REPO_ROOT, GEXF_REL)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ---- Core Leaders ----
    {
        "id": 1,
        "name": "张人富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "江西会昌",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "1997-08",
        "current_post": "全南县委书记",
        "current_org": "中共全南县委员会",
        "source": "全南县人民政府网(www.quannan.gov.cn)—2026年7月3日以县委书记身份主持县委常委会第111次(扩大)会议；7月8日讲授专题党课；百度百科—张人富，1977年11月生，江西会昌人，中央党校大学学历，1997年8月参加工作",
    },
    {
        "id": 2,
        "name": "杨春景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委副书记、县长候选人",
        "current_org": "全南县人民政府",
        "source": "全南县人民政府网—2026年7月3日县委常委会第111次会议首次以县长候选人身份出席；7月8日主持县政府政绩观学习教育整改整治工作推进会",
    },
    {
        "id": 3,
        "name": "边建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委书记、龙南经开区党工委书记",
        "current_org": "中共龙南市委员会",
        "source": "全南县人民政府网—2026年6月29日尚以县委书记身份主持庆祝建党105周年大会；2026年7月初调任龙南市委书记；百度百科—边建忠，1978年7月生，江西峡江人，1997.08工作，2001.04入党，华东政法大学，2026年7月7日任龙南市人武部党委第一书记",
    },
    # ---- Party Standing Committee (县委常委) ----
    {
        "id": 4,
        "name": "冯健全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委副书记",
        "current_org": "中共全南县委员会",
        "source": "全南县人民政府网—2026年6月29日庆祝建党105周年大会宣读表彰决定；7月3日县委常委会第111次会议在座",
    },
    {
        "id": 5,
        "name": "黎庆美",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委常委",
        "current_org": "中共全南县委员会",
        "source": "全南县人民政府网—2026年7月3日县委常委会第111次会议在座常委名单",
    },
    {
        "id": 6,
        "name": "朱新梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委常委、组织部部长",
        "current_org": "中共全南县委组织部",
        "source": "全南县人民政府网—2026年7月8日主持乡镇领导班子成员专题培训班；7月3日县委常委会第111次会议在座",
    },
    {
        "id": 7,
        "name": "彭智军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委常委",
        "current_org": "中共全南县委员会",
        "source": "全南县人民政府网—2026年7月3日县委常委会第111次会议在座常委名单",
    },
    {
        "id": 8,
        "name": "刘宏春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委常委、政法委书记",
        "current_org": "中共全南县委政法委员会",
        "source": "全南县人民政府网—2026年7月3日县委常委会第111次会议在座常委名单",
    },
    {
        "id": 9,
        "name": "朱恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委常委",
        "current_org": "中共全南县委员会",
        "source": "全南县人民政府网—2026年7月3日县委常委会第111次会议在座常委名单；7月13日通报集中整治工作进展情况",
    },
    {
        "id": 10,
        "name": "李宇恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委常委",
        "current_org": "中共全南县委员会",
        "source": "全南县人民政府网—2026年7月3日县委常委会第111次会议在座常委名单",
    },
    {
        "id": 11,
        "name": "姜荣建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县委常委",
        "current_org": "中共全南县委员会",
        "source": "全南县人民政府网—2026年7月3日县委常委会第111次会议在座常委名单",
    },
    # ---- County Government Leaders (县政府领导) ----
    {
        "id": 12,
        "name": "许瑞强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县领导",
        "current_org": "全南县人民政府",
        "source": "全南县人民政府网—2026年7月8日陪同张人富调研物业服务整治；7月8日出席县政府政绩观学习教育整改整治工作推进会",
    },
    {
        "id": 13,
        "name": "肖进林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县领导",
        "current_org": "全南县人民政府",
        "source": "全南县人民政府网—2026年7月8日出席县政府政绩观学习教育整改整治工作推进会",
    },
    {
        "id": 14,
        "name": "舒国飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县领导",
        "current_org": "全南县人民政府",
        "source": "全南县人民政府网—2026年7月8日出席县政府政绩观学习教育整改整治工作推进会",
    },
    # ---- 人大、政协 ----
    {
        "id": 15,
        "name": "马石旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县人大常委会主任",
        "current_org": "全南县人民代表大会常务委员会",
        "source": "全南县人民政府网—2026年6月29日庆祝建党105周年大会在座；7月3日县委常委会第111次会议列席",
    },
    {
        "id": 16,
        "name": "黄健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "全南县政协主席",
        "current_org": "中国人民政治协商会议全南县委员会",
        "source": "全南县人民政府网—2026年6月29日庆祝建党105周年大会在座；7月3日县委常委会第111次会议列席",
    },
    # ---- Predecessors ----
    {
        "id": 17,
        "name": "曾平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原全南县委书记）",
        "current_org": "",
        "source": "旧数据库记录/公开报道—前任全南县委书记（约2019-2025年在任）",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共全南县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共赣州市委员会",
        "location": "江西赣州全南",
    },
    {
        "id": 2,
        "name": "全南县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "赣州市人民政府",
        "location": "江西赣州全南",
    },
    {
        "id": 3,
        "name": "中共全南县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共全南县委员会",
        "location": "江西赣州全南",
    },
    {
        "id": 4,
        "name": "中共全南县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共全南县委员会",
        "location": "江西赣州全南",
    },
    {
        "id": 5,
        "name": "全南县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "赣州市人民代表大会常务委员会",
        "location": "江西赣州全南",
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议全南县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议赣州市委员会",
        "location": "江西赣州全南",
    },
]

positions = [
    # 张人富 — 县委书记（现任）
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "全南县委书记",
        "start": "2026-07",
        "end": "",
        "rank": "县处级正职",
        "note": "2026年7月3日首次以县委书记身份主持县委常委会第111次(扩大)会议。7月8日讲授树立和践行正确政绩观学习教育专题党课。1977-11生，江西会昌人，中央党校大学。1997.08参加工作。此前为全南县委副书记、县长。",
    },
    {
        "id": 2,
        "person_id": 1,
        "org_id": 2,
        "title": "全南县委副书记、县长（前任）",
        "start": "",
        "end": "2026-07",
        "rank": "县处级正职",
        "note": "2026年6月29日庆祝建党105周年大会时仍以县长身份主持。2026年2月28日在县十九届人大六次会议上作政府工作报告。约2026年7月初升任县委书记。1997-08参加工作，此前曾任宁都县委常委、兴国县委副书记、赣州市城管局党组书记等职。",
    },
    # 杨春景 — 县长候选人
    {
        "id": 3,
        "person_id": 2,
        "org_id": 1,
        "title": "全南县委副书记",
        "start": "2026-07",
        "end": "",
        "rank": "县处级副职",
        "note": "2026年7月3日县委常委会第111次会议首次以县委副书记身份出席。",
    },
    {
        "id": 4,
        "person_id": 2,
        "org_id": 2,
        "title": "全南县长候选人",
        "start": "2026-07",
        "end": "",
        "rank": "县处级正职",
        "note": "2026年7月3日以县委副书记、县长候选人身份出席县委常委会。7月8日主持县政府政绩观学习教育整改整治工作推进会。此前为全南县委常委、副县长。",
    },
    {
        "id": 5,
        "person_id": 2,
        "org_id": 2,
        "title": "全南县委常委、副县长（前任）",
        "start": "",
        "end": "2026-07",
        "rank": "县处级副职",
        "note": "此前为全南县委常委、县政府副县长。2026年7月上旬调研重点企业和防汛减灾工作（此时已为县长候选人）。",
    },
    # 边建忠 — 前任县委书记，已调任龙南市委书记
    {
        "id": 6,
        "person_id": 3,
        "org_id": 1,
        "title": "全南县委书记（前任）",
        "start": "2025",
        "end": "2026-07",
        "rank": "县处级正职",
        "note": "约2025年由县长升任县委书记。2026年6月9日主持政绩观学习教育整改整治推进会。6月29日主持庆祝建党105周年大会。2026年7月初调任龙南市委书记、龙南经开区党工委书记。1978-07生，江西峡江人，华东政法大学。1997-08工作，2001-04入党。曾任省委统战部干部、瑞金市副市长、全南组织部长、崇义常务副县长/副书记、全南县长/书记。",
    },
    {
        "id": 7,
        "person_id": 3,
        "org_id": 2,
        "title": "全南县长（前任）",
        "start": "2021",
        "end": "2025",
        "rank": "县处级正职",
        "note": "2021年任全南县长。2023-2025年连续以县长身份在县人代会上作政府工作报告。约2025年升任县委书记。此前曾任崇义县委副书记、崇义常务副县长、全南组织部长、瑞金副市长等职。",
    },
    # 冯健全
    {
        "id": 8,
        "person_id": 4,
        "org_id": 1,
        "title": "全南县委副书记",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年6月29日在庆祝建党105周年大会上宣读表彰决定。2026年7月3日在县委常委会第111次会议在座。",
    },
    # 黎庆美
    {
        "id": 9,
        "person_id": 5,
        "org_id": 1,
        "title": "全南县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年7月3日在县委常委会第111次会议在座。",
    },
    # 朱新梅
    {
        "id": 10,
        "person_id": 6,
        "org_id": 3,
        "title": "全南县委常委、组织部部长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年7月8日主持乡镇领导班子成员专题培训班。",
    },
    # 彭智军
    {
        "id": 11,
        "person_id": 7,
        "org_id": 1,
        "title": "全南县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年7月3日在县委常委会第111次会议在座。",
    },
    # 刘宏春
    {
        "id": 12,
        "person_id": 8,
        "org_id": 4,
        "title": "全南县委常委、政法委书记",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年7月3日在县委常委会第111次会议在座。",
    },
    # 朱恒
    {
        "id": 13,
        "person_id": 9,
        "org_id": 1,
        "title": "全南县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年7月13日通报全县群众身边不正之风和腐败问题集中整治工作进展情况。",
    },
    # 李宇恒
    {
        "id": 14,
        "person_id": 10,
        "org_id": 1,
        "title": "全南县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年7月3日在县委常委会第111次会议在座。",
    },
    # 姜荣建
    {
        "id": 15,
        "person_id": 11,
        "org_id": 1,
        "title": "全南县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任。2026年7月3日在县委常委会第111次会议在座。",
    },
    # 许瑞强
    {
        "id": 16,
        "person_id": 12,
        "org_id": 2,
        "title": "全南县领导",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "2026年7月8日陪同张人富调研物业服务突出问题整治工作。同日出席县政府政绩观学习教育整改整治推进会。具体职务待查。",
    },
    # 肖进林
    {
        "id": 17,
        "person_id": 13,
        "org_id": 2,
        "title": "全南县领导",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "2026年7月8日出席县政府政绩观学习教育整改整治推进会。具体职务待查。",
    },
    # 舒国飞
    {
        "id": 18,
        "person_id": 14,
        "org_id": 2,
        "title": "全南县领导",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "2026年7月8日出席县政府政绩观学习教育整改整治推进会。具体职务待查。",
    },
    # 马石旺
    {
        "id": 19,
        "person_id": 15,
        "org_id": 5,
        "title": "全南县人大常委会主任",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "2026年6月29日在庆祝建党105周年大会在座。7月3日列席县委常委会第111次会议。",
    },
    # 黄健
    {
        "id": 20,
        "person_id": 16,
        "org_id": 6,
        "title": "全南县政协主席",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "2026年6月29日在庆祝建党105周年大会在座。7月3日列席县委常委会第111次会议。",
    },
    # 曾平（前任县委书记）
    {
        "id": 21,
        "person_id": 17,
        "org_id": 1,
        "title": "全南县委书记（前任）",
        "start": "2019",
        "end": "2025",
        "rank": "县处级正职",
        "note": "前任全南县委书记。约2019-2025年在任，接任者边建忠。去向待查。",
    },
]

relationships = [
    # 张人富 ↔ 边建忠（前任接任）
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "前任接任（县委书记）",
        "context": "边建忠为前任全南县委书记，约2026年7月初调离；张人富（原县长）接任县委书记。二人在全南县党政班子共事多年（2021年起边建忠为县长/书记，张人富逐步从县长晋升）。",
        "overlap_org": "全南县党政班子",
        "overlap_period": "2021-2026",
    },
    # 张人富 ↔ 杨春景（正副职搭档）
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政正副职搭档",
        "context": "张人富（县委书记）与杨春景（县委副书记、县长候选人）为新的县委县政府正副职搭档。此前杨春景为县委常委、副县长时即与张人富（县长）共事。",
        "overlap_org": "全南县党政班子",
        "overlap_period": "现任",
    },
    # 张人富 ↔ 冯健全
    {
        "id": 3,
        "person_a_id": 1,
        "person_b_id": 4,
        "type": "党政正副职搭档",
        "context": "张人富（县委书记）与冯健全（县委副书记）为县委正副书记搭档关系。",
        "overlap_org": "中共全南县委员会",
        "overlap_period": "现任",
    },
    # 杨春景 ↔ 冯健全
    {
        "id": 4,
        "person_a_id": 2,
        "person_b_id": 4,
        "type": "党政正副职搭档",
        "context": "杨春景（县委副书记、县长候选人）与冯健全（县委副书记）为县委副书记搭档关系。",
        "overlap_org": "中共全南县委员会",
        "overlap_period": "现任",
    },
    # 张人富 ↔ 朱新梅
    {
        "id": 5,
        "person_a_id": 1,
        "person_b_id": 6,
        "type": "党政搭档",
        "context": "张人富（县委书记）与朱新梅（县委常委、组织部部长）组成县委领导与组织负责人工作关系。朱新梅主持了张人富授课的乡镇领导班子培训班。",
        "overlap_org": "中共全南县委员会",
        "overlap_period": "现任",
    },
    # 张人富 ↔ 刘宏春
    {
        "id": 6,
        "person_a_id": 1,
        "person_b_id": 8,
        "type": "党政搭档",
        "context": "张人富（县委书记）与刘宏春（县委常委、政法委书记）组成县委领导与政法负责人工作关系。",
        "overlap_org": "中共全南县委员会",
        "overlap_period": "现任",
    },
    # 张人富 ↔ 马石旺
    {
        "id": 7,
        "person_a_id": 1,
        "person_b_id": 15,
        "type": "党政人大关系",
        "context": "张人富（县委书记）与马石旺（县人大常委会主任）为县委与人大领导关系。",
        "overlap_org": "全南县",
        "overlap_period": "现任",
    },
    # 张人富 ↔ 黄健
    {
        "id": 8,
        "person_a_id": 1,
        "person_b_id": 16,
        "type": "党政政协关系",
        "context": "张人富（县委书记）与黄健（县政协主席）为县委与政协领导关系。",
        "overlap_org": "全南县",
        "overlap_period": "现任",
    },
    # 边建忠 ↔ 曾平
    {
        "id": 9,
        "person_a_id": 3,
        "person_b_id": 17,
        "type": "前任接任",
        "context": "曾平为前任全南县委书记，边建忠接任县委书记职务。",
        "overlap_org": "中共全南县委员会",
        "overlap_period": "2025前后",
    },
    # 边建忠 ↔ 冯健全
    {
        "id": 10,
        "person_a_id": 3,
        "person_b_id": 4,
        "type": "党政正副职搭档（前任）",
        "context": "边建忠（前任县委书记）与冯健全（县委副书记）为前任县委正副书记搭档关系。",
        "overlap_org": "中共全南县委员会",
        "overlap_period": "至2026-07",
    },
    # 张人富 ↔ 许瑞强
    {
        "id": 11,
        "person_a_id": 1,
        "person_b_id": 12,
        "type": "上下级关系",
        "context": "张人富（县委书记）调研物业整治时，县领导许瑞强陪同参加。",
        "overlap_org": "全南县",
        "overlap_period": "现任",
    },
    # 张人富 ↔ 朱恒
    {
        "id": 12,
        "person_a_id": 1,
        "person_b_id": 9,
        "type": "党政搭档",
        "context": "张人富（县委书记）与朱恒（县委常委）在集中整治工作推进会上分工配合。",
        "overlap_org": "中共全南县委员会",
        "overlap_period": "现任",
    },
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    post = post or ""
    if "书记" in post and ("县委" in post or "党委" in post) and "副" not in post:
        return "230,50,50"
    if "副书记" in post:
        return "200,80,80"
    if "县长" in post or "区长" in post:
        if "副" not in post:
            return "50,100,230"
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    if "人大" in post:
        return "50,180,50"
    if "政协" in post:
        return "180,100,180"
    if "县委常委" in post:
        return "150,100,50"
    return "120,120,120"


def ocolor_viz(otype):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,200",
        "政协": "255,240,200",
    }.get(otype, "200,200,200")


def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
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

    return counts


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus-junior</creator>')
    lines.append(f'    <description>全南县领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c_val = pcolor_viz(p.get("current_post", ""))
        sz = "20.0" if p["id"] in (1, 2) else ("15.0" if p["id"] in (3, 4, 15, 16) else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")), ("2", p.get("birthplace", "")),
                      ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        c_val = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""), ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start", "")), ("2", pos.get("end", "")),
                      ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("全南县 Government Personnel Network Builder")
    print(f"Date: {today}")
    print("=" * 60)

    print(f"\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    print(f"\n▶ Building GEXF graph...")
    tn, te = build_gexf()
    print(f"  ✓ {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    # Verify
    import sys
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"DB file not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF file not created: {GEXF_PATH}")

    if errors:
        print(f"\n✗ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\n✓ BUILD COMPLETE - All artifacts created successfully")
