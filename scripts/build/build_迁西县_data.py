#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 迁西县, 唐山市, 河北省."""

import sys
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(BASE, "scripts"))
sys.path.insert(0, BASE)

TMP = os.path.join(BASE, "data/tmp/hebei_迁西县")
DB_PATH = os.path.join(TMP, "迁西县_network.db")
GEXF_PATH = os.path.join(TMP, "迁西县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "都建华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县委书记、县人武部党委第一书记", "current_org": "中共迁西县委员会",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20240906/1211564794.html"},
    {"id": 2, "name": "薛波", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-09", "birthplace": "安徽省明光市", "education": "研究生学历",
     "party_join": "2009-06", "work_start": "2000-06",
     "current_post": "迁西县委副书记、县长", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianzhengfulingdao/20251013/1469353.html"},

    # ── Previous Leaders ──
    {"id": 3, "name": "田文学", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县长（已辞职）", "current_org": "",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20260629/1211631329.html"},
    {"id": 4, "name": "石井满", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县长（2021年当选）", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384612.html"},

    # ── Government Leadership Team ──
    {"id": 5, "name": "王云祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县委常委、常务副县长", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20230526/1529049.html"},
    {"id": 6, "name": "曹宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-01", "birthplace": "河北省固安县", "education": "大学学历",
     "party_join": "2006-04", "work_start": "2006-07",
     "current_post": "迁西县委常委、副县长", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianzhengfulingdao/20250721/869004.html"},
    {"id": 7, "name": "宋晓华", "gender": "女", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "河北迁西县", "education": "大学学历",
     "party_join": "2004-06", "work_start": "2000-05",
     "current_post": "迁西县人民政府副县长", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianzhengfulingdao/20250721/1495145.html"},
    {"id": 8, "name": "冯磊", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-01", "birthplace": "河北唐山", "education": "本科学历",
     "party_join": "2007-12", "work_start": "2008-08",
     "current_post": "迁西县人民政府副县长", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianzhengfulingdao/20250721/1211575387.html"},
    {"id": 9, "name": "孙广领", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "河北省邢台市", "education": "大学学历",
     "party_join": "1997-12", "work_start": "1994-08",
     "current_post": "迁西县人民政府副县长、县公安局局长", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianzhengfulingdao/20251201/1131581103.html"},
    {"id": 10, "name": "薛志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-04", "birthplace": "河北迁西县", "education": "研究生学历",
     "party_join": "1999-09", "work_start": "1996-08",
     "current_post": "迁西县人民政府副县长", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianzhengfulingdao/20251201/1211613479.html"},
    {"id": 11, "name": "杨帆（挂职）", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-01", "birthplace": "河北省石家庄", "education": "研究生学历",
     "party_join": "2005-06", "work_start": "2007-09",
     "current_post": "迁西县人民政府副县长（挂职）", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianzhengfulingdao/20251201/1211613467.html"},

    # ── County Leaders & Deputies ──
    {"id": 12, "name": "田会生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县副县长（2021年当选，后离任）", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384612.html"},
    {"id": 13, "name": "关佳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县副县长（2023年5月免职）", "current_org": "",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20230526/1529049.html"},
    {"id": 14, "name": "赵秋生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县副县长（2025年6月免职）", "current_org": "",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20250624/1211598153.html"},
    {"id": 15, "name": "王洪桥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县副县长（2022年11月免职）", "current_org": "",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20221201/1482767.html"},
    {"id": 16, "name": "陈朝阳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县副县长（2021年当选）", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384612.html"},
    {"id": 17, "name": "唐海生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县副县长（2021年当选）", "current_org": "迁西县人民政府",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384612.html"},
    {"id": 18, "name": "关立董", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县副县长（2022年11月任命，后续离任）", "current_org": "",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20221201/1482767.html"},

    # ── Other Key Posts ──
    {"id": 19, "name": "郑宏锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县纪委书记、监委主任", "current_org": "迁西县监察委员会",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixionrenshirenmian/20211206/1384612.html"},
    {"id": 20, "name": "薛向刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县人大常委会主任", "current_org": "迁西县人民代表大会常务委员会",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384612.html"},
    {"id": 21, "name": "刘永宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县政协主席", "current_org": "中国人民政治协商会议迁西县委员会",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384608.html"},
    {"id": 22, "name": "秦连国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县人民法院院长", "current_org": "迁西县人民法院",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384612.html"},
    {"id": 23, "name": "狄泽军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县人民检察院检察长", "current_org": "迁西县人民检察院",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20211206/1384612.html"},
    {"id": 24, "name": "袁久野", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县委常委、人武部部长", "current_org": "迁西县人民武装部",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20240906/1211564794.html"},
    {"id": 25, "name": "高海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原迁西县监察委员会副主任（2025年6月免职）", "current_org": "迁西县监察委员会",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20250624/1211598153.html"},
    {"id": 26, "name": "王海欣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迁西县监察委员会副主任", "current_org": "迁西县监察委员会",
     "source": "https://www.qianxi.gov.cn/qianxi/tsqianxixianrenshirenmian/20250624/1211598153.html"},
]

organizations = [
    {"id": 1, "name": "中共迁西县委员会", "type": "党委", "level": "县处级", "parent": "中共唐山市委",
     "location": "河北省唐山市迁西县"},
    {"id": 2, "name": "迁西县人民政府", "type": "政府", "level": "县处级", "parent": "唐山市人民政府",
     "location": "河北省唐山市迁西县"},
    {"id": 3, "name": "迁西县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "唐山市人大常委会", "location": "河北省唐山市迁西县"},
    {"id": 4, "name": "中国人民政治协商会议迁西县委员会", "type": "政协", "level": "县处级",
     "parent": "唐山市政协", "location": "河北省唐山市迁西县"},
    {"id": 5, "name": "迁西县监察委员会", "type": "党委", "level": "县处级",
     "parent": "迁西县人民政府", "location": "河北省唐山市迁西县"},
    {"id": 6, "name": "迁西县人民法院", "type": "政府", "level": "县处级",
     "parent": "唐山市中级人民法院", "location": "河北省唐山市迁西县"},
    {"id": 7, "name": "迁西县人民检察院", "type": "政府", "level": "县处级",
     "parent": "唐山市人民检察院", "location": "河北省唐山市迁西县"},
    {"id": 8, "name": "迁西县人民武装部", "type": "政府", "level": "县处级",
     "parent": "唐山市军分区", "location": "河北省唐山市迁西县"},
    {"id": 9, "name": "迁西县公安局", "type": "政府", "level": "乡科级",
     "parent": "迁西县人民政府", "location": "河北省唐山市迁西县"},
]

positions = [
    # ── Du Jianhua (都建华) ──
    {"person_id": 1, "org_id": 1, "title": "迁西县委书记、县人武部党委第一书记",
     "start": "2024-09", "end": "present", "rank": "副厅级",
     "note": "2024年9月5日就任迁西县人武部党委第一书记；此前已任迁西县委书记", "source_type": "official"},

    # ── Xue Bo (薛波) ──
    {"person_id": 2, "org_id": 1, "title": "迁西县委副书记",
     "start": "2025-09", "end": "present", "rank": "正县级",
     "note": "2025年9月11日任代理县长，后正式当选", "source_type": "official"},
    {"person_id": 2, "org_id": 2, "title": "迁西县代县长→县长",
     "start": "2025-09", "end": "present", "rank": "正县级",
     "note": "2025年9月11日任代县长；2026年1月28日在县第十七届人大八次会议上作政府工作报告", "source_type": "official"},

    # ── Tian Wenxue (田文学) ──
    {"person_id": 3, "org_id": 2, "title": "迁西县委副书记、县长",
     "start": "c.2023", "end": "2025-09", "rank": "正县级",
     "note": "2025年9月11日因工作需要辞去县长职务", "source_type": "official"},

    # ── Shi Jingman (石井满) ──
    {"person_id": 4, "org_id": 2, "title": "迁西县县长",
     "start": "2021-07", "end": "c.2023", "rank": "正县级",
     "note": "2021年7月26日当选迁西县第十七届人民政府县长", "source_type": "official"},

    # ── Wang Yunxiang (王云祥) ──
    {"person_id": 5, "org_id": 1, "title": "迁西县委常委",
     "start": "2023-05", "end": "present", "rank": "副县级",
     "note": "", "source_type": "official"},
    {"person_id": 5, "org_id": 2, "title": "迁西县常务副县长",
     "start": "2023-05", "end": "present", "rank": "副县级",
     "note": "2023年5月25日被任命为副县长", "source_type": "official"},

    # ── Cao Hong (曹宏) ──
    {"person_id": 6, "org_id": 1, "title": "迁西县委常委、副县长",
     "start": "2021-07", "end": "present", "rank": "副县级",
     "note": "2021年7月26日当选副县长；留任至今", "source_type": "official"},
    {"person_id": 6, "org_id": 2, "title": "迁西县副县长",
     "start": "2021-07", "end": "present", "rank": "副县级",
     "note": "分管工业、信息化、住建、城管、审批、电力", "source_type": "official"},

    # ── Song Xiaohua (宋晓华) ──
    {"person_id": 7, "org_id": 2, "title": "迁西县副县长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "分管农业、乡村振兴、水利、林业、供销、移民、气象", "source_type": "official"},

    # ── Feng Lei (冯磊) ──
    {"person_id": 8, "org_id": 2, "title": "迁西县副县长",
     "start": "2024-11", "end": "present", "rank": "副县级",
     "note": "2024年11月27日任命；分管文旅、市场监管、商务招商", "source_type": "official"},

    # ── Sun Guangling (孙广领) ──
    {"person_id": 9, "org_id": 2, "title": "迁西县副县长、县公安局局长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "分管公安、信访、退役军人、司法", "source_type": "official"},
    {"person_id": 9, "org_id": 9, "title": "县公安局局长",
     "start": "", "end": "present", "rank": "乡科级",
     "note": "兼任", "source_type": "official"},

    # ── Xue Zhigang (薛志刚) ──
    {"person_id": 10, "org_id": 2, "title": "迁西县副县长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "分管自然资源、教育、卫健、医保、民政", "source_type": "official"},

    # ── Yang Fan (杨帆/挂职) ──
    {"person_id": 11, "org_id": 2, "title": "迁西县副县长（挂职）",
     "start": "", "end": "present", "rank": "副县级",
     "note": "协助常务副县长王云祥分管金融保险", "source_type": "official"},

    # ── Tian Huisheng (田会生) ──
    {"person_id": 12, "org_id": 2, "title": "迁西县副县长",
     "start": "2021-07", "end": "c.2023", "rank": "副县级",
     "note": "2021年7月26日当选副县长", "source_type": "official"},

    # ── Guan Jia (关佳) ──
    {"person_id": 13, "org_id": 2, "title": "迁西县副县长",
     "start": "2021-07", "end": "2023-05", "rank": "副县级",
     "note": "2021年7月26日当选；2023年5月25日免职", "source_type": "official"},

    # ── Zhao Qiusheng (赵秋生) ──
    {"person_id": 14, "org_id": 2, "title": "迁西县副县长",
     "start": "2022-11", "end": "2025-06", "rank": "副县级",
     "note": "2022年11月30日任命；2025年6月16日免职", "source_type": "official"},

    # ── Wang Hongqiao (王洪桥) ──
    {"person_id": 15, "org_id": 2, "title": "迁西县副县长",
     "start": "2021-07", "end": "2022-11", "rank": "副县级",
     "note": "2021年7月26日当选；2022年11月30日免职", "source_type": "official"},

    # ── Chen Zhaoyang (陈朝阳) ──
    {"person_id": 16, "org_id": 2, "title": "迁西县副县长",
     "start": "2021-07", "end": "", "rank": "副县级",
     "note": "2021年7月26日当选", "source_type": "official"},

    # ── Tang Haisheng (唐海生) ──
    {"person_id": 17, "org_id": 2, "title": "迁西县副县长",
     "start": "2021-07", "end": "", "rank": "副县级",
     "note": "2021年7月26日当选", "source_type": "official"},

    # ── Guan Lidong (关立董) ──
    {"person_id": 18, "org_id": 2, "title": "迁西县副县长",
     "start": "2022-11", "end": "", "rank": "副县级",
     "note": "2022年11月30日任命", "source_type": "official"},

    # ── Zheng Hongfeng (郑宏锋) ──
    {"person_id": 19, "org_id": 1, "title": "迁西县委常委、纪委书记",
     "start": "2021-07", "end": "present", "rank": "副县级",
     "note": "2021年7月26日当选县监察委员会主任", "source_type": "official"},
    {"person_id": 19, "org_id": 5, "title": "迁西县监委主任",
     "start": "2021-07", "end": "present", "rank": "副县级",
     "note": "2021年7月26日当选", "source_type": "official"},

    # ── Xue Xianggang (薛向刚) ──
    {"person_id": 20, "org_id": 3, "title": "迁西县人大常委会主任",
     "start": "2021-07", "end": "present", "rank": "正县级",
     "note": "2021年7月26日当选", "source_type": "official"},

    # ── Liu Yonghong (刘永宏) ──
    {"person_id": 21, "org_id": 4, "title": "迁西县政协主席",
     "start": "2021-07", "end": "present", "rank": "正县级",
     "note": "2021年7月26日当选", "source_type": "official"},

    # ── Qin Lianguo (秦连国) ──
    {"person_id": 22, "org_id": 6, "title": "迁西县法院院长",
     "start": "2021-07", "end": "present", "rank": "副县级",
     "note": "2021年7月26日当选", "source_type": "official"},

    # ── Di Zejun (狄泽军) ──
    {"person_id": 23, "org_id": 7, "title": "迁西县检察院检察长",
     "start": "2021-07", "end": "present", "rank": "副县级",
     "note": "2021年7月26日当选", "source_type": "official"},

    # ── Yuan Jiuye (袁久野) ──
    {"person_id": 24, "org_id": 1, "title": "迁西县委常委、县人武部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "", "source_type": "official"},
    {"person_id": 24, "org_id": 8, "title": "迁西县人武部部长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "", "source_type": "official"},

    # ── Gao Haifeng (高海峰) ──
    {"person_id": 25, "org_id": 5, "title": "迁西县监委副主任",
     "start": "", "end": "2025-06", "rank": "副县级",
     "note": "2025年6月16日免职", "source_type": "official"},

    # ── Wang Haixin (王海欣) ──
    {"person_id": 26, "org_id": 5, "title": "迁西县监委副主任",
     "start": "2025-06", "end": "present", "rank": "副县级",
     "note": "2025年6月16日任命", "source_type": "official"},
]

relationships = [
    # ── Party Secretary & County Magistrate ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "strength": "strong",
     "context": "都建华(县委书记)与薛波(县长)为迁西县党政一把手搭档关系",
     "overlap_org": "中共迁西县委员会/迁西县人民政府",
     "overlap_period": "2025-09至今",
     "confidence": "confirmed"},

    # ── Magicipal Succession ──
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "strength": "strong",
     "context": "薛波接替田文学任迁西县长",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2025-09",
     "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "strength": "strong",
     "context": "田文学接替石井满任迁西县长",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "c.2023",
     "confidence": "plausible"},

    # ── Standing Committee Overlaps ──
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "strength": "strong",
     "context": "都建华与王云祥同为迁西县委常委",
     "overlap_org": "中共迁西县委员会",
     "overlap_period": "2024-09至今",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "strength": "strong",
     "context": "都建华与曹宏同为迁西县委常委",
     "overlap_org": "中共迁西县委员会",
     "overlap_period": "2024-09至今",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "strength": "strong",
     "context": "都建华与郑宏锋同在迁西县委常委会",
     "overlap_org": "中共迁西县委员会",
     "overlap_period": "2024-09至今",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 24, "type": "overlap",
     "strength": "strong",
     "context": "2024年9月都建华任人武部党委第一书记，袁久野任人武部部长",
     "overlap_org": "中共迁西县委员会/迁西县人武部",
     "overlap_period": "2024-09至今",
     "confidence": "confirmed"},

    # ── Government Team Overlaps ──
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "strength": "strong",
     "context": "薛波与王云祥在迁西县政府任正副职",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2025-09至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "strength": "strong",
     "context": "薛波与曹宏在迁西县政府共事",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2025-09至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "strength": "strong",
     "context": "薛波与宋晓华同在迁西县政府",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2025-09至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "strength": "strong",
     "context": "薛波与冯磊同在迁西县政府",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2025-09至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "strength": "strong",
     "context": "薛波与孙广领同在迁西县政府",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2025-09至今",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "strength": "strong",
     "context": "薛波与薛志刚同在迁西县政府",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2025-09至今",
     "confidence": "confirmed"},

    # ── Previous Team Overlaps ──
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "strength": "strong",
     "context": "田文学与王云祥在迁西县政府共事",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2023-05至2025-09",
     "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "strength": "strong",
     "context": "田文学与曹宏在迁西县政府共事",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "c.2023至2025-09",
     "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "strength": "strong",
     "context": "石井满与曹宏在迁西县政府共事（2021年同批当选）",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2021-07至c.2023",
     "confidence": "confirmed"},
    {"person_a": 4, "person_b": 12, "type": "overlap",
     "strength": "strong",
     "context": "石井满与田会生当年同为政府班子成员",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2021-07至c.2023",
     "confidence": "confirmed"},
    {"person_a": 4, "person_b": 13, "type": "overlap",
     "strength": "strong",
     "context": "石井满与关佳在政府班子成员期期",
     "overlap_org": "迁西县人民政府",
     "overlap_period": "2021-07至2023-05",
     "confidence": "confirmed"},
]

# ── BUILD ─────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(title):
    """Return 'r,g,b' color string for a person based on their role."""
    t = (title or "").lower()
    if "县委书记" in t or "书记" in t:
        return "255,50,50"
    if "县长" in t or "县长" in t or "副县长" in t or "代县长" in t:
        return "50,100,255"
    if "纪委" in t or "监委" in t:
        return "255,165,0"
    return "100,100,100"

def is_top_leader(p):
    t = (p.get("current_post") or "").lower()
    return "县委书记" in t or "副书记" in t or "县长" in t

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,200",
        "法院": "200,200,255",
        "检察院": "200,200,255",
    }
    return colors.get(org_type, "200,200,200")

# Build SQLite
import sqlite3
db_path = DB_PATH
os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(db_path)
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
    source TEXT
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
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    strongth TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""
        INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p.get("birthplace",""), p.get("education",""),
          p.get("party_join",""), p.get("work_start",""), p.get("current_post",""), p.get("current_org",""), p.get("source","")))

for o in organizations:
    cur.execute("""
        INSERT INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o.get("level",""), o.get("parent",""), o.get("location","")))

for pos in positions:
    cur.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos.get("title",""), pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

for r in relationships:
    cur.execute("""
        INSERT INTO relationships (person_a, person_b, type, strongth, context, overlap_org, overlap_period, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r.get("type",""), r.get("strength",""), r.get("context",""), r.get("overlap_org",""), r.get("overlap_period",""), r.get("confidence","")))

conn.commit()
conn.close()
print(f"SQLite DB created: {db_path}")
print(f"  - {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# Build GEXF
gexf_path = GEXF_PATH
os.makedirs(os.path.dirname(gexf_path), exist_ok=True)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>迁西县领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    pid = f"p{p['id']}"
    c = person_color(p.get("current_post",""))
    sz = person_size(p)
    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append('        </attvalues>')
    parts = c.split(",")
    lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    oid = f"o{o['id']}"
    oc = org_color(o["type"])
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value=""/>')
    lines.append('        </attvalues>')
    op = oc.split(",")
    lines.append(f'        <viz:color r="{op[0]}" g="{op[1]}" b="{op[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
eid_counter = 0
lines.append('    <edges>')
for pos in positions:
    eid_counter += 1
    pid = f"p{pos['person_id']}"
    oid = f"o{pos['org_id']}"
    lines.append(f'      <edge id="e{eid_counter}" source="{pid}" target="{oid}" label="{esc(pos.get("title",""))}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    eid_counter += 1
    lines.append(f'      <edge id="e{eid_counter}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type",""))}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r.get("type",""))}"/>')
    lines.append(f'          <attvalue for="0" value="{esc(r.get("context",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(gexf_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF created: {gexf_path}")

print("\nDone.")