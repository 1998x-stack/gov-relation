#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 黔江区 (Qianjiang District, Chongqing).

Task: chongqing_黔江区 — 区委书记 & 区长
Province: 重庆市
City: 黔江区 (重庆直辖市下辖区)
Region: 黔江区
Level: 市辖区(直辖市)
Research date: 2026-07-16

Known officeholders (as of most recent available data):
- 区委书记: 罗成 (appointed ~2024-09; previously unknown - 1970.04, 研究生/公共管理硕士)
- 区委副书记、区长: 骆高燕 (confirmed as of 2025-01; 1977.05, 大学/工学学士)
- 区委副书记: 李泽玉 (confirmed from official site; 1970.01, 土家族, 研究生/法学学士)
- 区人大常委会主任: 刘毅 (confirmed from official site; 1970.10, 土家族, 研究生)
- 区政协主席: 姚登惠 (confirmed from official site; 1966.07, 土家族, 研究生/农学硕士)

Confirmed leadership from official qianjiang.gov.cn:
区委领导:
- 罗成 (区委书记)
- 骆高燕 (区委副书记、区长)
- 李泽玉 (区委副书记、区委党校校长)
- 谢承刚 (区委常委、政法委书记)
- 强劲松 (区委常委、纪委书记、监委主任)
- 高苏秦 (区委常委)
- 陈林 (区委常委、宣传部部长)
- 周晓东 (区委常委、统战部部长)
- 张志锋 (区委常委, 2024-09)
- 肖洪林 (区委常委、区人武部政委)
- 王刚 (区委常委、挂职, 2026-07)

区政府领导:
- 骆高燕 (区长)
- 曾祥远 (副区长)
- 滕旭荣 (副区长)
- 张攀 (副区长、区公安局局长)
- 晏伟 (副区长, 无党派, 1980.12)
- 蒋杭航 (副区长)
- 章烈 (副区长)
- 李国政 (挂职)
- 李大东 (挂职)

Previous officeholders:
- 前区委书记: 余常明 (served 2015-2021, moved to 大渡口区)
- 前区委书记 between 余常明 and 罗成: unknown from available sources

Sources:
- www.qianjiang.gov.cn — official government website (primary source for leadership roster)
- qianjiang.gov.cn — 区委领导/区政府领导 pages
- Multiple news reports on qianjiang.gov.cn confirming 罗成 as 区委书记 and 骆高燕 as 区长
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "黔江区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "黔江区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 区委班子 (District Party Committee) ══

    # 区委书记 — 罗成
    ("qj_luo_cheng", "罗成", "男", "汉族", "1970年4月", "待查",
     "研究生、公共管理硕士", "中共党员", "待查",
     "区委书记", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区委副书记、区长 — 骆高燕
    ("qj_luo_gaoyan", "骆高燕", "男", "汉族", "1977年5月", "待查",
     "大学、工学学士", "中共党员", "待查",
     "区委副书记、区长", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 区委副书记（专职）— 李泽玉
    ("qj_li_zeyu", "李泽玉", "女", "土家族", "1970年1月", "待查",
     "研究生、法学学士", "中共党员", "待查",
     "区委副书记、区委党校校长", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区委常委、政法委书记 — 谢承刚
    ("qj_xie_chenggang", "谢承刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区委常委、纪委书记、监委主任 — 强劲松
    ("qj_qiang_jinsong", "强劲松", "男", "汉族", "1973年10月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共重庆市黔江区纪律检查委员会",
     "qianjiang.gov.cn_official"),

    # 区委常委 — 高苏秦
    ("qj_gao_suqin", "高苏秦", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区委常委、宣传部部长 — 陈林
    ("qj_chen_lin", "陈林", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区委常委、统战部部长 — 周晓东
    ("qj_zhou_xiaodong", "周晓东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区委常委 — 张志锋 (from list, detail page returned 404)
    ("qj_zhang_zhifeng", "张志锋", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区委常委、区人武部政治委员 — 肖洪林
    ("qj_xiao_honglin", "肖洪林", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区人武部政治委员", "重庆市黔江区人民武装部",
     "qianjiang.gov.cn_official"),

    # 区委常委（挂职）— 王刚
    ("qj_wang_gang", "王刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委（挂职）", "中共重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # ══ 区政府领导 ══

    # 副区长 — 曾祥远
    ("qj_zeng_xiangyuan", "曾祥远", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 副区长 — 滕旭荣
    ("qj_teng_xurong", "滕旭荣", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 副区长、区公安局局长 — 张攀
    ("qj_zhang_pan", "张攀", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长，区公安局局长", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 副区长 — 晏伟
    ("qj_yan_wei", "晏伟", "男", "汉族", "1980年12月", "待查",
     "大学、工程硕士", "无党派", "待查",
     "区政府副区长", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 副区长 — 蒋杭航
    ("qj_jiang_hanghang", "蒋杭航", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 副区长 — 章烈
    ("qj_zhang_lie", "章烈", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 挂职 — 李国政
    ("qj_li_guozheng", "李国政", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员（挂职）", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # 挂职 — 李大东
    ("qj_li_dadong", "李大东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员（挂职）", "重庆市黔江区人民政府",
     "qianjiang.gov.cn_official"),

    # ══ 人大领导 ══

    # 区人大常委会主任 — 刘毅
    ("qj_liu_yi", "刘毅", "男", "土家族", "1970年10月", "待查",
     "研究生", "中共党员", "待查",
     "区人大常委会党组书记、主任", "重庆市黔江区人民代表大会常务委员会",
     "qianjiang.gov.cn_official"),

    # 区人大常委会副主任 — 张力
    ("qj_zhang_li", "张力", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组副书记、副主任", "重庆市黔江区人民代表大会常务委员会",
     "qianjiang.gov.cn_official"),

    # 区人大常委会副主任 — 任天银
    ("qj_ren_tianyin", "任天银", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组成员、副主任", "重庆市黔江区人民代表大会常务委员会",
     "qianjiang.gov.cn_official"),

    # 区人大常委会副主任 — 陈天沛
    ("qj_chen_tianpei", "陈天沛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组成员、副主任", "重庆市黔江区人民代表大会常务委员会",
     "qianjiang.gov.cn_official"),

    # 区人大常委会副主任 — 张健
    ("qj_zhang_jian", "张健", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任", "重庆市黔江区人民代表大会常务委员会",
     "qianjiang.gov.cn_official"),

    # ══ 政协领导 ══

    # 区政协主席 — 姚登惠
    ("qj_yao_denghui", "姚登惠", "男", "土家族", "1966年7月", "待查",
     "研究生、农学硕士", "中共党员", "待查",
     "区政协党组书记、主席", "中国人民政治协商会议重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区政协副主席 — 刘元寿
    ("qj_liu_yuanshou", "刘元寿", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协党组副书记、副主席", "中国人民政治协商会议重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区政协副主席 — 肖培明
    ("qj_xiao_peiming", "肖培明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协党组成员、副主席", "中国人民政治协商会议重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区政协副主席 — 冉光荣
    ("qj_ran_guangrong", "冉光荣", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协党组成员、副主席", "中国人民政治协商会议重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区政协副主席 — 李世波
    ("qj_li_shibo", "李世波", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "中国人民政治协商会议重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区政协副主席 — 毛立新
    ("qj_mao_lixin", "毛立新", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "中国人民政治协商会议重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # 区政协副主席 — 胡江
    ("qj_hu_jiang", "胡江", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席", "中国人民政治协商会议重庆市黔江区委员会",
     "qianjiang.gov.cn_official"),

    # ══ 前任领导 ══

    # 前区委书记 — 余常明
    ("qj_yu_changming", "余常明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委书记", "中共重庆市黔江区委员会（原）",
     "media_reports;historical_knowledge"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("qj_party_committee", "中共重庆市黔江区委员会", "党委", "地厅级", "中共重庆市委", "重庆市黔江区"),
    ("qj_gov", "重庆市黔江区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市黔江区"),
    ("qj_discipline", "中共重庆市黔江区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市黔江区"),
    ("qj_organization", "中共重庆市黔江区委组织部", "党委部门", "正处级", "黔江区委", "重庆市黔江区"),
    ("qj_propaganda", "中共重庆市黔江区委宣传部", "党委部门", "正处级", "黔江区委", "重庆市黔江区"),
    ("qj_united_front", "中共重庆市黔江区委统战部", "党委部门", "正处级", "黔江区委", "重庆市黔江区"),
    ("qj_political_legal", "中共重庆市黔江区委政法委员会", "党委部门", "正处级", "黔江区委", "重庆市黔江区"),
    ("qj_military_department", "重庆市黔江区人民武装部", "军事", "正师级", "重庆警备区", "重庆市黔江区"),
    ("qj_public_security", "重庆市黔江区公安局", "公安", "正处级", "重庆市公安局", "重庆市黔江区"),
    ("qj_peoples_congress", "重庆市黔江区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市黔江区"),
    ("qj_cppcc", "中国人民政治协商会议重庆市黔江区委员会", "政协", "地厅级", "重庆市政协", "重庆市黔江区"),
    ("qj_party_school", "中共重庆市黔江区委党校", "事业单位", "正处级", "黔江区委", "重庆市黔江区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 罗成 — 区委书记 ═══
    ("qj_luo_cheng", "qj_party_committee", "区委书记", "2024-09", "至今", "正厅级",
     "主持区委全面工作。最早于2024年9月以区委书记身份出现在官方页面。"),

    # ═══ 骆高燕 — 区长 ═══
    ("qj_luo_gaoyan", "qj_gov", "区长", "待查", "至今", "正厅级",
     "主持区政府全面工作。区委副书记、区政府党组书记。"),
    ("qj_luo_gaoyan", "qj_party_committee", "区委副书记", "待查", "至今", "正厅级", "兼任"),

    # ═══ 李泽玉 — 区委副书记 ═══
    ("qj_li_zeyu", "qj_party_committee", "区委副书记、区委党校校长", "待查", "至今", "正厅级",
     "专职副书记。协助区委书记负责区委日常工作和党的建设工作。"),
    ("qj_li_zeyu", "qj_party_school", "区委党校校长", "待查", "至今", "正厅级", "兼任"),

    # ═══ 谢承刚 — 政法委书记 ═══
    ("qj_xie_chenggang", "qj_party_committee", "区委常委", "待查", "至今", "副厅级", ""),
    ("qj_xie_chenggang", "qj_political_legal", "区委政法委书记", "待查", "至今", "副厅级", ""),

    # ═══ 强劲松 — 纪委书记 ═══
    ("qj_qiang_jinsong", "qj_party_committee", "区委常委", "待查", "至今", "副厅级", ""),
    ("qj_qiang_jinsong", "qj_discipline", "区纪委书记、监委主任", "待查", "至今", "副厅级", ""),

    # ═══ 高苏秦 — 区委常委 ═══
    ("qj_gao_suqin", "qj_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 陈林 — 宣传部部长 ═══
    ("qj_chen_lin", "qj_party_committee", "区委常委", "待查", "至今", "副厅级", ""),
    ("qj_chen_lin", "qj_propaganda", "区委宣传部部长", "待查", "至今", "副厅级", ""),

    # ═══ 周晓东 — 统战部部长 ═══
    ("qj_zhou_xiaodong", "qj_party_committee", "区委常委", "2026-02", "至今", "副厅级", ""),
    ("qj_zhou_xiaodong", "qj_united_front", "区委统战部部长", "2026-02", "至今", "副厅级", ""),

    # ═══ 张志锋 — 区委常委 ═══
    ("qj_zhang_zhifeng", "qj_party_committee", "区委常委", "待查", "至今", "副厅级", "官方页面2024年9月更新"),

    # ═══ 肖洪林 — 人武部政委 ═══
    ("qj_xiao_honglin", "qj_party_committee", "区委常委", "待查", "至今", "副厅级", ""),
    ("qj_xiao_honglin", "qj_military_department", "区人武部政治委员", "待查", "至今", "正团级", ""),

    # ═══ 王刚 — 挂职常委 ═══
    ("qj_wang_gang", "qj_party_committee", "区委常委（挂职）", "2026-07", "至今", "副厅级", "2026年7月任挂职区委常委"),

    # ═══ 曾祥远 — 副区长 ═══
    ("qj_zeng_xiangyuan", "qj_gov", "区政府党组成员、副区长", "待查", "至今", "副厅级", ""),

    # ═══ 滕旭荣 — 副区长 ═══
    ("qj_teng_xurong", "qj_gov", "区政府党组成员、副区长", "待查", "至今", "副厅级", ""),

    # ═══ 张攀 — 副区长兼公安局局长 ═══
    ("qj_zhang_pan", "qj_gov", "区政府党组成员、副区长", "待查", "至今", "副厅级", ""),
    ("qj_zhang_pan", "qj_public_security", "区公安局局长", "待查", "至今", "正处级", ""),

    # ═══ 晏伟 — 副区长 ═══
    ("qj_yan_wei", "qj_gov", "区政府副区长", "待查", "至今", "副厅级",
     "无党派人士，1980年12月生。分管规划自然资源、住建、城管等。"),

    # ═══ 蒋杭航 — 副区长 ═══
    ("qj_jiang_hanghang", "qj_gov", "区政府党组成员、副区长", "待查", "至今", "副厅级", ""),

    # ═══ 章烈 — 副区长 ═══
    ("qj_zhang_lie", "qj_gov", "区政府党组成员、副区长", "2026-03", "至今", "副厅级", ""),

    # ═══ 李国政 — 挂职 ═══
    ("qj_li_guozheng", "qj_gov", "区政府党组成员（挂职）", "待查", "至今", "副厅级", "挂职"),

    # ═══ 李大东 — 挂职 ═══
    ("qj_li_dadong", "qj_gov", "区政府党组成员（挂职）", "2025-12", "至今", "副厅级", "挂职"),

    # ═══ 刘毅 — 人大常委会主任 ═══
    ("qj_liu_yi", "qj_peoples_congress", "区人大常委会党组书记、主任", "待查", "至今", "正厅级",
     "主持区人大常委会全面工作。"),

    # ═══ 张力 — 人大常委会副主任 ═══
    ("qj_zhang_li", "qj_peoples_congress", "区人大常委会党组副书记、副主任", "待查", "至今", "副厅级", ""),

    # ═══ 任天银 — 人大常委会副主任 ═══
    ("qj_ren_tianyin", "qj_peoples_congress", "区人大常委会党组成员、副主任", "待查", "至今", "副厅级", ""),

    # ═══ 陈天沛 — 人大常委会副主任 ═══
    ("qj_chen_tianpei", "qj_peoples_congress", "区人大常委会党组成员、副主任", "待查", "至今", "副厅级", ""),

    # ═══ 张健 — 人大常委会副主任 ═══
    ("qj_zhang_jian", "qj_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),

    # ═══ 姚登惠 — 政协主席 ═══
    ("qj_yao_denghui", "qj_cppcc", "区政协党组书记、主席", "待查", "至今", "正厅级",
     "主持区政协全面工作。"),

    # ═══ 刘元寿 — 政协副主席 ═══
    ("qj_liu_yuanshou", "qj_cppcc", "区政协党组副书记、副主席", "待查", "至今", "副厅级", ""),

    # ═══ 肖培明 — 政协副主席 ═══
    ("qj_xiao_peiming", "qj_cppcc", "区政协党组成员、副主席", "待查", "至今", "副厅级", ""),

    # ═══ 冉光荣 — 政协副主席 ═══
    ("qj_ran_guangrong", "qj_cppcc", "区政协党组成员、副主席", "待查", "至今", "副厅级", ""),

    # ═══ 李世波 — 政协副主席 ═══
    ("qj_li_shibo", "qj_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),

    # ═══ 毛立新 — 政协副主席 ═══
    ("qj_mao_lixin", "qj_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),

    # ═══ 胡江 — 政协副主席 ═══
    ("qj_hu_jiang", "qj_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),

    # ═══ 前任领导 ═══
    ("qj_yu_changming", "qj_party_committee", "前任区委书记", "2015-07", "2021-08", "正厅级",
     "2015年7月—2021年8月任黔江区委书记。后调任大渡口区委书记。"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 罗成 ↔ 骆高燕 — 党政正职搭档 ═══
    ("qj_luo_cheng", "qj_luo_gaoyan", "superior_subordinate",
     "区委书记与区长党政正职搭档关系",
     "中共重庆市黔江区委员会;重庆市黔江区人民政府", "2024-09至今"),

    # ═══ 罗成 ↔ 李泽玉 — 书记-副书记 ═══
    ("qj_luo_cheng", "qj_li_zeyu", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市黔江区委员会", "至今"),

    # ═══ 骆高燕 ↔ 李泽玉 — 区长-副书记 ═══
    ("qj_luo_gaoyan", "qj_li_zeyu", "overlap",
     "区长与区委副书记（区委区政府协调）",
     "中共重庆市黔江区委员会", "至今"),

    # ═══ 罗成 ↔ 谢承刚 — 书记-常委(政法委) ═══
    ("qj_luo_cheng", "qj_xie_chenggang", "superior_subordinate",
     "区委书记与政法委书记",
     "中共重庆市黔江区委员会", "至今"),

    # ═══ 罗成 ↔ 强劲松 — 书记-纪委书记 ═══
    ("qj_luo_cheng", "qj_qiang_jinsong", "superior_subordinate",
     "区委书记与纪委书记",
     "中共重庆市黔江区委员会", "至今"),

    # ═══ 罗成 ↔ 陈林 — 书记-宣传部长 ═══
    ("qj_luo_cheng", "qj_chen_lin", "superior_subordinate",
     "区委书记与宣传部部长",
     "中共重庆市黔江区委员会", "至今"),

    # ═══ 罗成 ↔ 周晓东 — 书记-统战部长 ═══
    ("qj_luo_cheng", "qj_zhou_xiaodong", "superior_subordinate",
     "区委书记与统战部部长",
     "中共重庆市黔江区委员会", "2026-02至今"),

    # ═══ 罗成 ↔ 高苏秦 — 书记-常委 ═══
    ("qj_luo_cheng", "qj_gao_suqin", "superior_subordinate",
     "区委书记与区委常委",
     "中共重庆市黔江区委员会", "至今"),

    # ═══ 骆高燕 ↔ 曾祥远 — 区长-副区长 ═══
    ("qj_luo_gaoyan", "qj_zeng_xiangyuan", "superior_subordinate",
     "区长与副区长",
     "重庆市黔江区人民政府", "至今"),

    # ═══ 骆高燕 ↔ 滕旭荣 — 区长-副区长 ═══
    ("qj_luo_gaoyan", "qj_teng_xurong", "superior_subordinate",
     "区长与副区长",
     "重庆市黔江区人民政府", "至今"),

    # ═══ 骆高燕 ↔ 张攀 — 区长-副区长(公安) ═══
    ("qj_luo_gaoyan", "qj_zhang_pan", "superior_subordinate",
     "区长与分管公安工作的副区长",
     "重庆市黔江区人民政府", "至今"),

    # ═══ 骆高燕 ↔ 晏伟 — 区长-副区长 ═══
    ("qj_luo_gaoyan", "qj_yan_wei", "superior_subordinate",
     "区长与副区长",
     "重庆市黔江区人民政府", "至今"),

    # ═══ 骆高燕 ↔ 蒋杭航 — 区长-副区长 ═══
    ("qj_luo_gaoyan", "qj_jiang_hanghang", "superior_subordinate",
     "区长与副区长",
     "重庆市黔江区人民政府", "至今"),

    # ═══ 骆高燕 ↔ 章烈 — 区长-副区长 ═══
    ("qj_luo_gaoyan", "qj_zhang_lie", "superior_subordinate",
     "区长与副区长",
     "重庆市黔江区人民政府", "2026-03至今"),

    # ═══ 罗成 — 前任书记（余常明） ═══
    ("qj_luo_cheng", "qj_yu_changming", "predecessor_successor",
     "罗成接替余常明（经中间一任）任黔江区委书记。余常明2015-2021任职，罗成2024-09到任。",
     "中共重庆市黔江区委员会", "2024-09"),
]


# ════════════════════════════════════════════
# SQLITE SETUP
# ════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
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
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF GENERATION
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def is_top_leader(person_id):
    return person_id in ("qj_luo_cheng", "qj_luo_gaoyan", "qj_yu_changming")


def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id in ("qj_luo_cheng", "qj_yu_changming"):
        return "255,50,50"       # Red — Party Secretary
    elif person_id == "qj_luo_gaoyan":
        return "50,100,255"      # Blue — Government head
    elif person_id == "qj_qiang_jinsong":
        return "255,165,0"       # Orange — Discipline Inspection
    else:
        return "100,100,100"     # Grey — Others


def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "党委部门": "255,220,220",
        "军事": "200,200,200",
        "公安": "200,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return color_map.get(org_type, "200,200,200")


def generate_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Gov Research Agent</creator>')
    lines.append('    <description>重庆市黔江区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── Node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # ── Edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[8]  # current_post
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="person"/>')
        lines.append(f'          <attvalue for="3" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        olevel = o[3]
        c = org_color(oid, otype)
        lines.append(f'      <node id="o{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(olevel)}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at via positions)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        start = pos[3] if pos[3] else ""
        end = pos[4] if pos[4] else ""
        eid += 1
        period = f"{start}-{end}" if start or end else ""
        lines.append(f'      <edge id="e{eid}" source="p{esc(pid)}" target="o{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oid)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        overlap_org = r[4]
        overlap_period = r[5]
        weight = "2.0"  # person-person edges stronger than person-org
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{esc(pa)}" target="p{esc(pb)}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(overlap_org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(overlap_period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF graph created: {GEXF_PATH}")


# ════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════

def print_summary():
    print(f"\n{'='*60}")
    print(f"  重庆市黔江区 领导网络数据")
    print(f"{'='*60}")
    print(f"  人物: {len(PERSONS)}")
    print(f"  机构: {len(ORGANIZATIONS)}")
    print(f"  任职记录: {len(POSITIONS)}")
    print(f"  关系边: {len(RELATIONSHIPS)}")
    print(f"{'='*60}")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"{'='*60}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    generate_gexf()
    print_summary()
