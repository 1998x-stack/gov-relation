#!/usr/bin/env python3
"""
玉门市（酒泉市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yumen City leadership.

Level: 县级市
Province: 甘肃省
Parent City: 酒泉市
Region: 玉门市
Targets: 市委书记 & 市长

Research Sources:
- 玉门市人民政府官网 (www.yumen.gov.cn) — 领导之窗、新闻报道 (2026年7月确认)
- 新闻报道: 玉门市委理论学习中心组会议(2026-07-21)、兰洽会(2026-07-10)等
- build_酒泉市_data.py — 市级已有数据
- build_肃州区_data.py — 何正军曾任玉门市长
- 胡志勇维基百科 — 前任市委书记信息
- 酒泉市人民政府官网 (www.jiuquan.gov.cn)

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── PATHS ──
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_玉门市")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "玉门市_network.db")
GEXF_PATH = os.path.join(STAGING, "玉门市_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# Person IDs use format: ym_{surname}{givenname} (ym = Yumen)
PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, native_place,
    # education, party_join, work_start, current_post, current_org, source

    # ═══════════════════════════
    # 市委领导班子
    # ═══════════════════════════

    # 李应伟 — 市委书记 (as of 2026-07)
    ("ym_li_yingwei", "李应伟", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市委书记",
     "中共玉门市委员会",
     "yumen.gov.cn新闻报道(yumen.gov.cn/yuMen/c103383/)"),

    # ═══════════════════════════
    # 市政府领导班子
    # ═══════════════════════════

    # 王迎军 — 市委副书记、市长
    ("ym_wang_yingjun", "王迎军", "男", "汉族", "1980年11月", "待查", "待查",
     "大学学历/公共管理硕士", "中共党员", "待查",
     "玉门市委副书记、市政府党组书记、市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2026-01-27更新)"),

    # 赵超 — 市委常委、常务副市长
    ("ym_zhao_chao", "赵超", "男", "汉族", "1979年6月", "待查", "待查",
     "省委党校在职研究生(区域经济开发史)", "中共党员", "待查",
     "玉门市委常委、市政府党组副书记、常务副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2026-06-22更新)"),

    # 史先勇 — 市委常委、副市长
    ("ym_shi_xianyong", "史先勇", "男", "汉族", "1983年8月", "待查", "待查",
     "大学本科/管理学学士(信息技术与信息系统)", "中共党员", "待查",
     "玉门市委常委、市政府党组成员、副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2026-01-29更新)"),

    # 王涛 — 市委常委、副市长
    ("ym_wang_tao", "王涛", "男", "汉族", "1983年3月", "待查", "待查",
     "省委党校在职研究生(国民经济学)/工学学士(兰州理工大学环境工程)", "中共党员", "待查",
     "玉门市委常委、市政府党组成员、副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2024-08-07更新)"),

    # 张晓芸 — 市委常委、副市长
    ("ym_zhang_xiaoyun", "张晓芸", "女", "汉族", "1983年3月", "待查", "待查",
     "大学学历/教育学学士", "中共党员", "待查",
     "玉门市委常委、市政府党组成员、副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2026-04-13更新)"),

    # 岳建强 — 副市长、市公安局局长
    ("ym_yue_jianqiang", "岳建强", "男", "汉族", "1983年5月", "待查", "待查",
     "省委党校研究生(学历名称待确认)", "中共党员", "待查",
     "玉门市政府党组成员、副市长、市公安局党委书记/局长/督察长(兼)/三级高级警长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2025-06-05更新)"),

    # 张桐 — 副市长、经开区党工委书记
    ("ym_zhang_tong", "张桐", "男", "汉族", "1984年7月", "待查", "待查",
     "省委党校在职研究生(法学理论)/法学学士(西南石油大学法学)", "中共党员", "待查",
     "玉门市政府党组成员、副市长、经济开发区党工委书记",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2024-08-06更新)"),

    # 马玉军 — 副市长、市农业农村局局长
    ("ym_ma_yujun", "马玉军", "男", "汉族", "1975年1月", "待查", "待查",
     "中央党校在职大学(法律)", "中共党员", "待查",
     "玉门市政府党组成员、副市长、市农业农村局局长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗(2026-06-22更新)"),

    # ═══════════════════════════
    # 其他市委领导(待确认具体职务)
    # ═══════════════════════════

    # 张继 — 市委常委、纪委书记、监委代主任
    ("ym_zhang_ji", "张继", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市委常委、纪委书记、监委代主任",
     "中共玉门市纪律检查委员会",
     "yumen.gov.cn新闻报道(2026-07-09廉洁文化建设调研)"),

    # ═══════════════════════════
    # 人大、政协
    # ═══════════════════════════

    # 李红 — 市人大常委会主任
    ("ym_li_hong", "李红", "待查", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人大常委会主任",
     "玉门市人民代表大会常务委员会",
     "yumen.gov.cn新闻报道(2026-07-21中心组学习会)"),

    # 周勤 — 市政协主席
    ("ym_zhou_qin", "周勤", "待查", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市政协主席",
     "中国人民政治协商会议玉门市委员会",
     "yumen.gov.cn新闻报道(2026-07-21中心组学习会)"),

    # 张存明 — 市政协党组书记
    ("ym_zhang_cunming", "张存明", "待查", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市政协党组书记",
     "中国人民政治协商会议玉门市委员会",
     "yumen.gov.cn新闻报道(2026-07-21中心组学习会)"),

    # ═══════════════════════════
    # 其他市领导(有待确认具体职务)
    # ═══════════════════════════

    # 白雪瑞 — 市领导(疑为市委常委)
    ("ym_bai_xuerui", "白雪瑞", "待查", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导(常委?)",
     "玉门市",
     "yumen.gov.cn新闻报道列席中心组学习会"),

    # 谢祥 — 市领导(疑为市委常委)
    ("ym_xie_xiang", "谢祥", "待查", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导(常委?)",
     "玉门市",
     "yumen.gov.cn新闻报道列席中心组学习会+应急演练"),

    # 范志俊 — 市领导(疑为市委常委)
    ("ym_fan_zhijun", "范志俊", "待查", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导(常委?)",
     "玉门市",
     "yumen.gov.cn新闻报道列席中心组学习会+应急演练"),

    # 王菲 — 市领导(疑为市委常委)
    ("ym_wang_fei", "王菲", "待查", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导(常委?)",
     "玉门市",
     "yumen.gov.cn新闻报道列席中心组学习会+应急演练"),

    # ═══════════════════════════
    # 前任领导
    # ═══════════════════════════

    # 胡志勇 — 前任玉门市委书记(2019.06-2021.10), 现任庆阳市市长
    ("ym_hu_zhiyong", "胡志勇", "男", "汉族", "1974年2月", "甘肃金塔", "甘肃金塔",
     "大专(甘肃政法学院公安学)/在职研究生(兰州大学法律)", "1999年6月", "1995年7月",
     "庆阳市委副书记、市政府党组书记、市长",
     "庆阳市人民政府",
     "维基百科(zh.wikipedia.org/zh-cn/胡志勇)"),

    # 何正军 — 前任玉门市长(后任肃州区委书记), 现任酒泉市人大常委会副主任
    ("ym_he_zhengjun", "何正军", "男", "汉族", "1967年12月", "甘肃金塔", "甘肃金塔",
     "省委党校研究生/文学学士", "中共党员", "1987年7月",
     "酒泉市人大常委会副主任",
     "酒泉市人民代表大会常务委员会",
     "build_肃州区_data.py; thepaper.cn"),

    # 陈炎人 — 更早前任玉门市委书记(维基百科)
    ("ym_chen_yanren", "陈炎人", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "另有任用(原玉门市委书记)",
     "待查",
     "维基百科(玉门市页面)"),

    # 梁秉国 — 前任玉门市人大常委会主任
    ("ym_liang_bingguo", "梁秉国", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "另有任用(原玉门市人大常委会主任)",
     "待查",
     "酒泉市人大网站; yumen.gov.cn旧版新闻报道"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("ym_party_committee", "中共玉门市委员会", "党委", "县级", "中共酒泉市委员会", "酒泉市玉门市"),
    ("ym_gov", "玉门市人民政府", "政府", "县级", "酒泉市人民政府", "酒泉市玉门市"),
    ("ym_discipline", "中共玉门市纪律检查委员会", "纪委", "县级", "中共酒泉市纪律检查委员会", "酒泉市玉门市"),
    ("ym_people_congress", "玉门市人民代表大会常务委员会", "人大", "县级", "酒泉市人大常委会", "酒泉市玉门市"),
    ("ym_cppcc", "中国人民政治协商会议玉门市委员会", "政协", "县级", "酒泉市政协", "酒泉市玉门市"),
    ("ym_public_security", "玉门市公安局", "政府", "正科级", "玉门市人民政府", "酒泉市玉门市"),
    ("ym_economic_dev_zone", "玉门经济开发区", "政府", "待查", "玉门市人民政府", "酒泉市玉门市"),
    ("ym_agriculture_bureau", "玉门市农业农村局", "政府", "正科级", "玉门市人民政府", "酒泉市玉门市"),
    ("ym_party_org", "中共玉门市委组织部", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),
    ("ym_propaganda", "中共玉门市委宣传部", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),
    ("ym_united_front", "中共玉门市委统一战线工作部", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),
    ("ym_political_legal", "中共玉门市委政法委员会", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),

    # 外部组织
    ("ym_jiuquan_party", "中共酒泉市委员会", "党委", "地级", "中共甘肃省委员会", "甘肃省酒泉市"),
    ("ym_jiuquan_gov", "酒泉市人民政府", "政府", "地级", "甘肃省人民政府", "甘肃省酒泉市"),
    ("ym_jiuquan_congress", "酒泉市人民代表大会常务委员会", "人大", "地级", "酒泉市", "甘肃省酒泉市"),
    ("ym_qingyang_gov", "庆阳市人民政府", "政府", "地级", "甘肃省人民政府", "甘肃省庆阳市"),
    ("ym_suzhou_party", "中共肃州区委员会", "党委", "县级", "中共酒泉市委员会", "酒泉市肃州区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 李应伟 — 市委书记 ═══
    ("ym_li_yingwei", "ym_party_committee", "玉门市委书记", "待查", "至今", "正处级", "主持市委全面工作；据新闻报道2026年7月仍在任"),

    # ═══ 王迎军 — 市长 ═══
    ("ym_wang_yingjun", "ym_gov", "玉门市委副书记、市政府党组书记、市长", "~2025末/2026初", "至今", "正处级",
     "主持市政府全面工作。负责审计方面工作。分管审计局。领导之窗最后更新2026-01-27"),
    ("ym_wang_yingjun", "", "肃北县委常委、常务副县长(推测)", "待查", "~2025", "副处级",
     "推测：据肃北县巴成人物档案，王迎军曾任肃北县常务副县长"),

    # ═══ 赵超 — 常务副市长 ═══
    ("ym_zhao_chao", "ym_gov", "玉门市委常委、常务副市长", "~2025", "至今", "副处级",
     "负责市政府常务工作。分管发改、财政、应急、统计等。2025年2月任前公示拟任市委常委"),
    ("ym_zhao_chao", "", "玉门市人民政府副市长(前任)", "待查", "~2025", "副处级", "晋升常务副市长"),

    # ═══ 史先勇 — 副市长 ═══
    ("ym_shi_xianyong", "ym_gov", "玉门市委常委、市政府党组成员、副市长", "", "至今", "副处级",
     "负责第三产业发展。分管人社、住建、商贸物流、招商引资、交通运输等"),

    # ═══ 王涛 — 副市长 ═══
    ("ym_wang_tao", "ym_gov", "玉门市委常委、市政府党组成员、副市长", "", "至今", "副处级",
     "协助市长负责第二产业发展。分管科技、民政、退役军人、生态环境等"),

    # ═══ 张晓芸 — 副市长 ═══
    ("ym_zhang_xiaoyun", "ym_gov", "玉门市委常委、市政府党组成员、副市长", "", "至今", "副处级",
     "负责司法、市场监管、退役军人事务、融媒体等"),

    # ═══ 岳建强 — 副市长、公安局长 ═══
    ("ym_yue_jianqiang", "ym_public_security", "玉门市政府党组成员、副市长、市公安局党委书记/局长/督察长(兼)", "", "至今", "副处级",
     "兼任市公安局局长。负责公安、信访、边防、民族宗教等。三级高级警长"),
    ("ym_yue_jianqiang", "ym_gov", "玉门市政府党组成员、副市长", "", "至今", "副处级", ""),

    # ═══ 张桐 — 副市长、经开区书记 ═══
    ("ym_zhang_tong", "ym_economic_dev_zone", "玉门市政府党组成员、副市长、经济开发区党工委书记", "", "至今", "副处级",
     "负责第二产业发展。负责工业园区(一区三园)、工信、能源、生态环境"),
    ("ym_zhang_tong", "ym_gov", "玉门市政府党组成员、副市长", "", "至今", "副处级", ""),

    # ═══ 马玉军 — 副市长、农业农村局长 ═══
    ("ym_ma_yujun", "ym_agriculture_bureau", "玉门市政府党组成员、副市长、市农业农村局局长", "", "至今", "副处级",
     "负责第一产业发展。负责农业农村、自然资源、水务、乡村振兴"),
    ("ym_ma_yujun", "ym_gov", "玉门市政府党组成员、副市长", "", "至今", "副处级", ""),

    # ═══ 张继 — 纪委书记 ═══
    ("ym_zhang_ji", "ym_discipline", "玉门市委常委、纪委书记、监委代主任", "", "至今", "副处级", ""),

    # ═══ 李红 — 人大主任 ═══
    ("ym_li_hong", "ym_people_congress", "玉门市人大常委会主任", "~2026", "至今", "正处级", "接替梁秉国"),

    # ═══ 周勤 — 政协主席 ═══
    ("ym_zhou_qin", "ym_cppcc", "玉门市政协主席", "", "至今", "正处级", ""),

    # ═══ 张存明 — 政协党组书记 ═══
    ("ym_zhang_cunming", "ym_cppcc", "玉门市政协党组书记", "", "至今", "正处级", ""),

    # ═══ 市领导(待确认) — 相关 ═══
    ("ym_bai_xuerui", "ym_party_committee", "玉门市领导(疑为市委常委)", "", "至今", "副处级", "待确认具体职务"),
    ("ym_xie_xiang", "ym_party_committee", "玉门市领导(疑为市委常委)", "", "至今", "副处级", "待确认具体职务"),
    ("ym_fan_zhijun", "ym_party_committee", "玉门市领导(疑为市委常委)", "", "至今", "副处级", "待确认具体职务"),
    ("ym_wang_fei", "ym_party_committee", "玉门市领导(疑为市委常委)", "", "至今", "副处级", "待确认具体职务"),

    # ═══ 胡志勇 — 前任书记 ═══
    ("ym_hu_zhiyong", "ym_party_committee", "玉门市委书记", "2019-06", "2021-10", "正处级",
     "从酒泉市工信局局长升任"),
    ("ym_hu_zhiyong", "", "酒泉市工业和信息化局局长", "2019-01", "2019-06", "正处级", "前职"),
    ("ym_hu_zhiyong", "ym_qingyang_gov", "庆阳市委副书记、市政府党组书记、市长", "2026-05", "至今", "正厅级",
     "2026年6月正式当选庆阳市市长。此前经历:天水副市长→天水常委/组织部长→庆阳"),

    # ═══ 何正军 — 前任市长 ═══
    ("ym_he_zhengjun", "", "玉门市委副书记、市长", "?", "?", "正处级",
     "前职，具体任期待确认"),
    ("ym_he_zhengjun", "ym_suzhou_party", "肃州区委书记", "~2019", "2024-01", "副厅级", "兼任酒泉市委常委"),
    ("ym_he_zhengjun", "ym_jiuquan_congress", "酒泉市人大常委会副主任", "2025-10", "至今", "副厅级", "现任"),

    # ═══ 陈炎人 — 更早前任书记 ═══
    ("ym_chen_yanren", "ym_party_committee", "玉门市委书记(前任)", "?", "?", "正处级", "维基百科记载;任期及去向待查"),

    # ═══ 梁秉国 — 前任人大主任 ═══
    ("ym_liang_bingguo", "ym_people_congress", "玉门市人大常委会主任(前任)", "", "~2026", "正处级", "由李红接任"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 党政搭档
    ("ym_li_yingwei", "ym_wang_yingjun", "党政搭档",
     "市委书记与市长，共同领导玉门市", "玉门市委/市政府", "至今"),

    # 市长与副市长
    ("ym_wang_yingjun", "ym_zhao_chao", "上下级",
     "市长与常务副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_shi_xianyong", "上下级",
     "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_wang_tao", "上下级",
     "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_zhang_xiaoyun", "上下级",
     "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_yue_jianqiang", "上下级",
     "市长与副市长/公安局长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_zhang_tong", "上下级",
     "市长与副市长/经开区书记", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_ma_yujun", "上下级",
     "市长与副市长/农业农村局长", "玉门市政府", ""),

    # 市委书记与市委常委
    ("ym_li_yingwei", "ym_zhang_ji", "同僚",
     "市委书记与纪委书记", "玉门市委", ""),
    ("ym_li_yingwei", "ym_zhao_chao", "同僚",
     "市委书记与市委常委/常务副市长", "玉门市委", ""),
    ("ym_li_yingwei", "ym_shi_xianyong", "同僚",
     "市委书记与市委常委/副市长", "玉门市委", ""),
    ("ym_li_yingwei", "ym_wang_tao", "同僚",
     "市委书记与市委常委/副市长", "玉门市委", ""),
    ("ym_li_yingwei", "ym_zhang_xiaoyun", "同僚",
     "市委书记与市委常委/副市长", "玉门市委", ""),

    # 人大政协
    ("ym_li_yingwei", "ym_li_hong", "同僚",
     "市委书记与人大主任", "玉门市", ""),
    ("ym_li_yingwei", "ym_zhou_qin", "同僚",
     "市委书记与政协主席", "玉门市", ""),
    ("ym_li_yingwei", "ym_zhang_cunming", "同僚",
     "市委书记与政协党组书记", "玉门市", ""),

    # 继任关系
    ("ym_li_yingwei", "ym_hu_zhiyong", "继任",
     "接替胡志勇任玉门市委书记", "玉门市委", "2021-10后"),
    ("ym_hu_zhiyong", "ym_chen_yanren", "继任",
     "接替陈炎人(?)任玉门市委书记", "玉门市委", "2019-06"),
    ("ym_wang_yingjun", "ym_he_zhengjun", "继任",
     "接替何正军(?确切时间待确认)任玉门市长", "玉门市政府", ""),
    ("ym_li_hong", "ym_liang_bingguo", "继任",
     "接替梁秉国任玉门市人大常委会主任", "玉门市人大", "~2026"),

    # 跨市/跨区调动
    ("ym_hu_zhiyong", "", "跨区调动",
     "玉门市委书记→天水副市长→天水常委/组织部长→庆阳市长", "甘肃省", "2021-2026"),
    ("ym_he_zhengjun", "", "跨区调动",
     "玉门市长→肃州区委书记→酒泉市人大副主任", "酒泉市", ""),
]

# Seed data: predecessor connections to existing 酒泉市 network
# 何正军 also appears in build_肃州区_data.py as 肃州区委书记 predecessor


# ════════════════════════════════════════════
# CREATE DATABASE
# ════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos[0], pos[1] if pos[1] else None, pos[2], pos[3], pos[4], pos[5], pos[6]))

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r[0], r[1] if r[1] else None, r[2], r[3], r[4], r[5]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")

    # Stats
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"   {table}: {count} rows")
    conn.close()


# ════════════════════════════════════════════
# CREATE GEXF GRAPH
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id):
    """Color by role."""
    top_leaders = ["ym_li_yingwei", "ym_hu_zhiyong", "ym_chen_yanren"]
    gov_leaders = ["ym_wang_yingjun", "ym_he_zhengjun"]
    discipline = ["ym_zhang_ji"]

    if person_id in top_leaders:
        return "255,50,50"  # Red - Party Secretary
    elif person_id in gov_leaders:
        return "50,100,255"  # Blue - Government
    elif person_id in discipline:
        return "255,165,0"  # Orange - Discipline
    else:
        return "100,100,100"  # Grey - Others

def is_top_leader(person_id):
    return person_id in ["ym_li_yingwei", "ym_wang_yingjun", "ym_hu_zhiyong", "ym_li_hong", "ym_zhou_qin"]

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "党委部门": "255,200,200",
    }
    return colors.get(org_type, "200,200,200")

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>玉门市（酒泉市）领导班子工作关系网络 — 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Persons as nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[10]  # current_post
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Orgs as nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        if not oid:
            continue
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        if not pb:
            continue
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("玉门市领导班子工作关系网络 — 数据构建")
    print("=" * 50)
    create_database()
    create_gexf()
    print("\n✅ Done. All artifacts generated in staging:")
    print(f"   DB:    {DB_PATH}")
    print(f"   GEXF:  {GEXF_PATH}")
