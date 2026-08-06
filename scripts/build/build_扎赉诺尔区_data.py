#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 呼伦贝尔市扎赉诺尔区 leadership network.

扎赉诺尔区（市辖区）隶属内蒙古自治区呼伦贝尔市，位于中俄蒙边境、呼伦湖畔，是
"满扎一体化"与向北开放的重要枢纽。区经济以煤炭（扎赉诺尔煤业/扎煤公司）、
新能源、文旅（"呼伦湖·猛犸故乡"、"国际研学小城"）为支柱。

数据时间锚点：2026-08-06。核心任职信息以扎赉诺尔区人民政府官网「领导之窗」、
第三届区委三届一次全会公报（2026-07-31）、2026年政府工作报告、以及呼伦贝尔市委
组织部任前公示为 confirmed 依据；个人履历细节以官网/主流媒体为确认，无法确认者标注
unverified 并列入 open_gaps。

核心人员（现任，2026-08）：
- 区委书记：布尔金（蒙古族，1976-11，博士研究生）
- 区委副书记、区长：万宏宇（女，汉族，1987-06，文学学士，区长候选人/区政府党组书记）
前任（2026-06-31 第三届区委换届）：
- 前任区委书记：齐善剑（→ 鄂伦春旗委书记）
- 前任区长：张兴旺（→ 呼伦贝尔市住建局局长）
关键人事流动带：满洲里市委（布尔金、齐善剑同为满洲里市委常委）；鄂温克旗
（布尔金、万宏宇、金文成均曾任职鄂温克旗）。

来源：
- 扎赉诺尔区政府网站 领导之窗 /Leader/ 及成员页，2026-08 访问
- 三届一次全会：/News/show/1446756.html（2026-08-03）
- 2026 政府工作报告（代区长布尔金） /OpennessContent/show/556418.html
- 呼伦贝尔市委组织部任前公示（布尔金 2023-05/2025-03；原文经主流媒体转载）
- 百度百科词条（布尔金/万宏宇/金文成等），2026-08 访问
"""

import sys
import sqlite3  # noqa: F401 (used via gov_relation.runner.run_build)
from pathlib import Path

# Robustly add repo root to path (works from staging dir, scripts/build/, or repo root)
_REPO = Path(__file__).resolve().parent
while not (_REPO / "gov_relation").is_dir():
    if _REPO == _REPO.parent:
        break
    _REPO = _REPO.parent
sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "扎赉诺尔区"
DB_PATH = DATABASE_DIR / "扎赉诺尔区_network.db"
GEXF_PATH = GRAPH_DIR / "扎赉诺尔区_network.gexf"

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共扎赉诺尔区委员会", "type": "党委", "level": "县处级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 2, "name": "扎赉诺尔区人民政府", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 3, "name": "扎赉诺尔区人大常委会", "type": "人大", "level": "县处级", "parent": "呼伦贝尔市人大常委会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 4, "name": "扎赉诺尔区政协", "type": "政协", "level": "县处级", "parent": "呼伦贝尔市政协", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 5, "name": "扎赉诺尔区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "呼伦贝尔市纪委", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 6, "name": "扎赉诺尔区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共扎赉诺尔区委员会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 7, "name": "扎赉诺尔区委组织部", "type": "党委", "level": "县处级", "parent": "中共扎赉诺尔区委员会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 8, "name": "扎赉诺尔区委宣传部", "type": "党委", "level": "县处级", "parent": "中共扎赉诺尔区委员会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 9, "name": "扎赉诺尔区委统战部", "type": "党委", "level": "县处级", "parent": "中共扎赉诺尔区委员会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 10, "name": "扎赉诺尔区委办公室", "type": "党委", "level": "县处级", "parent": "中共扎赉诺尔区委员会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 11, "name": "扎赉诺尔区人民武装部", "type": "事业单位", "level": "县处级", "parent": "呼伦贝尔军分区", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 12, "name": "呼伦贝尔市公安局扎赉诺尔分局", "type": "政府", "level": "县处级", "parent": "扎赉诺尔区人民政府", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    {"id": 13, "name": "扎赉诺尔区监察委员会", "type": "纪委", "level": "县处级", "parent": "扎赉诺尔区纪律检查委员会", "location": "内蒙古自治区呼伦贝尔市扎赉诺尔区"},
    # 外部关联组织（人事流动/前任去向）
    {"id": 14, "name": "鄂温克族自治旗人民政府", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市鄂温克族自治旗"},
    {"id": 15, "name": "满洲里市人民政府", "type": "政府", "level": "正处级/计划单列市", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 16, "name": "中共满洲里市委员会", "type": "党委", "level": "地厅级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市满洲里市"},
    {"id": 17, "name": "额尔古纳市人民政府", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市额尔古纳市"},
    {"id": 18, "name": "中共鄂伦春自治旗委员会", "type": "党委", "level": "县处级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市鄂伦春自治旗"},
    {"id": 19, "name": "鄂伦春自治旗人民政府", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市鄂伦春自治旗"},
    {"id": 20, "name": "呼伦贝尔市住房和城乡建设局", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市海拉尔区"},
    {"id": 21, "name": "鄂温克族自治旗委员会", "type": "党委", "level": "县处级", "parent": "中共呼伦贝尔市委", "location": "内蒙古自治区呼伦贝尔市鄂温克族自治旗"},
    {"id": 22, "name": "海拉尔区人民政府", "type": "政府", "level": "县处级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古自治区呼伦贝尔市海拉尔区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ 现任区委班子 ═══
    # 1 — 布尔金 — 区委书记
    {"id": 1, "name": "布尔金", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1976年11月", "birthplace": "待查",
     "education": "博士研究生（高校学习视域未注明专业，属在职/全日制待查）",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "呼伦贝尔市扎赉诺尔区区委书记", "current_org": "中共扎赉诺尔区委员会",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/828.html；三届一次全会 /News/show/1446756.html"},
    # 2 — 万宏宇 — 区委副书记、区长
    {"id": 2, "name": "万宏宇", "gender": "女", "ethnicity": "汉族",
     "birth": "1987年6月", "birthplace": "河北省保定市新城县（待核实）",
     "education": "大学、文学学士（天津外国语学院）",
     "party_join": "2008年12月", "work_start": "待查",
     "current_post": "扎赉诺尔区委副书记、区人民政府党组书记、区长候选人", "current_org": "扎赉诺尔区人民政府",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/1084.html；呼伦贝尔市委组织部任前公示（媒体转载）"},
    # 3 — 林干 — 区委副书记、政法委书记
    {"id": 3, "name": "林干", "gender": "男", "ethnicity": "汉族",
     "birth": "1985年8月", "birthplace": "待查",
     "education": "研究生", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委副书记、区委政法委书记", "current_org": "扎赉诺尔区委员会",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/988.html"},
    # 4 — 佟拉嘎 — 纪委书记
    {"id": 4, "name": "佟拉嘎", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1981年1月", "birthplace": "待查",
     "education": "大学本科", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委常委、区纪委书记、监委主任", "current_org": "扎赉诺尔区纪律检查委员会",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/946.html；三届纪委一次全会 /News/show/1446563.html"},
    # 5 — 徐国彬 — 宣传部长
    {"id": 5, "name": "徐国彬", "gender": "男", "ethnicity": "满族",
     "birth": "1983年12月", "birthplace": "待查",
     "education": "大学", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委常委、宣传部部长", "current_org": "扎赉诺尔区委宣传部",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/813.html"},
    # 6 — 王静 — 统战部长
    {"id": 6, "name": "王静", "gender": "女", "ethnicity": "汉族",
     "birth": "1981年7月", "birthplace": "待查",
     "education": "大学", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委常委、统战部部长", "current_org": "扎赉诺尔区委统战部",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/1083.html"},
    # 7 — 金文成 — 常务副区长
    {"id": 7, "name": "金文成", "gender": "男", "ethnicity": "鄂温克族",
     "birth": "1974年6月", "birthplace": "待查",
     "education": "大学", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委常委、区政府党组副书记、常务副区长", "current_org": "扎赉诺尔区人民政府",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/1048.html；百度百科"},
    # 8 — 高旭斌 — 副区长
    {"id": 8, "name": "高旭斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年6月", "birthplace": "待查",
     "education": "大学本科", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区副区长（区委常委、政府党组成员）", "current_org": "扎赉诺尔区人民政府",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/830.html"},
    # 9 — 井树冬 — 区委办主任
    {"id": 9, "name": "井树冬", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年9月", "birthplace": "待查",
     "education": "大学", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委常委、办公室主任", "current_org": "扎赉诺尔区委办公室",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/1086.html"},
    # 10 — 冯暴 — 组织部长
    {"id": 10, "name": "冯暴", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年12月", "birthplace": "待查",
     "education": "吉林省委党校研究生、法学硕士", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委常委、组织部部长", "current_org": "扎赉诺尔区委组织部",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/1085.html"},
    # 11 — 胡毅 — 人武部政委
    {"id": 11, "name": "胡毅", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年8月", "birthplace": "待查",
     "education": "大学本科（军事院校待查）", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区委常委、区人民武装部上校政治委员", "current_org": "扎赉诺尔区人民武装部",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/256/1081.html"},
    # 12 — 杨波 — 副区长兼公安局长
    {"id": 12, "name": "杨波", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1970年10月", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区副区长、市公安局扎赉诺尔分局党委书记、局长", "current_org": "呼伦贝尔市公安局扎赉诺尔分局",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/258/831.html"},
    # 13 — 白琰 — 副区长
    {"id": 13, "name": "白琰", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1984年6月", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区副区长（政府党组成员）", "current_org": "扎赉诺尔区人民政府",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/258/827.html"},
    # 14 — 王胜利 — 人大主任
    {"id": 14, "name": "王胜利", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年4月", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "扎赉诺尔区人大常委会主任", "current_org": "扎赉诺尔区人大常委会",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/257/824.html"},
    # 15 — 高胜 — 政协主席
    {"id": 15, "name": "高胜", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1967年4月", "birthplace": "内蒙古乌兰察布",
     "education": "待查", "party_join": "中共党员", "work_start": "1990年7月",
     "current_post": "扎赉诺尔区政协主席", "current_org": "扎赉诺尔区政协",
     "source": "扎赉诺尔区政府 领导之窗 /Leader/show/259/832.html"},
    # ═══ 前任（换届更替 / 人事去向）═══
    # 16 — 齐善剑 — 前任区委书记
    {"id": 16, "name": "齐善剑", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年10月", "birthplace": "内蒙古新巴尔虎右旗",
     "education": "在职研究生", "party_join": "1999年6月", "work_start": "1992年8月",
     "current_post": "鄂伦春自治旗旗委书记（2026-06 起）", "current_org": "中共鄂伦春自治旗委员会",
     "source": "鄂伦春旗政府 领导之窗；汲古新知 2026-06-17 报道；呼伦贝尔市委组织部任前公示"},
    # 17 — 张兴旺 — 前任区长
    {"id": 17, "name": "张兴旺", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年4月", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "呼伦贝尔市住房和城乡建设局局长（调任后）", "current_org": "呼伦贝尔市住房和城乡建设局",
     "source": "内蒙古人大/呼伦贝尔市住建局；媒体 2024-2025 报道"},
    # 18 — 吴振丽 — 前任区委宣传部部长
    {"id": 18, "name": "吴振丽", "gender": "女", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "（原扎赉诺尔区委宣传部部长，2026-04 报道仍以该身份出现，换届后由徐国彬接任；去向待查）", "current_org": "扎赉诺尔区委宣传部",
     "source": "呼伦贝尔市/扎达区政府网站 2026-04-22 相关报道"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 布尔金（现任区委书记）
    {"person_id": 1, "org_id": 14, "title": "鄂温克族自治旗副旗长", "start_date": "待查", "end_date": "待查", "rank": "副处级", "note": "早期履历公开信息不全"},
    {"person_id": 1, "org_id": 17, "title": "额尔古纳市委副书记、政法委书记", "start_date": "待查", "end_date": "2023-05", "rank": "副处级", "note": "呼伦贝尔市委组织部 2023-05 任前公示确认此前任此职"},
    {"person_id": 1, "org_id": 15, "title": "满洲里市委常委、副市长", "start_date": "2023-06", "end_date": "2025-03", "rank": "副地级", "note": "2023-06 任满洲里市委常委、副市长"},
    {"person_id": 1, "org_id": 2, "title": "扎赉诺尔区委副书记、代区长", "start_date": "2025-04", "end_date": "2026-02", "rank": "正处级", "note": "2025-03 呼伦贝尔公示拟提名旗市区政府正职"},
    {"person_id": 1, "org_id": 2, "title": "扎赉诺尔区区长", "start_date": "2026-02", "end_date": "2026-06", "rank": "正处级", "note": "2026-02-04 区二届人大五次会议作政府工作报告"},
    {"person_id": 1, "org_id": 1, "title": "扎赉诺尔区委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026-07-31 三届一次全会选举为第三届区委书记"},
    # 万宏宇（现任区长候选人）
    {"person_id": 2, "org_id": 22, "title": "海拉尔区信访局副科级信访专员", "start_date": "待查", "end_date": "待查", "rank": "副科级", "note": "早期履历"},
    {"person_id": 2, "org_id": 22, "title": "共青团海拉尔区委副书记、书记", "start_date": "待查", "end_date": "待查", "rank": "副科-正科级", "note": "共青团海拉尔区委"},
    {"person_id": 2, "org_id": 22, "title": "海拉尔区哈克镇党委副书记、镇长", "start_date": "待查", "end_date": "约2021-07", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "鄂温克族自治旗副旗长", "start_date": "2021-07", "end_date": "2025", "rank": "副处级", "note": "2021-07 任鄂温克旗副旗长"},
    {"person_id": 2, "org_id": 21, "title": "鄂温克族自治旗委常委、副旗长", "start_date": "2025", "end_date": "2026", "rank": "副处级", "note": "晋升旗委常委"},
    {"person_id": 2, "org_id": 2, "title": "扎赉诺尔区委副书记、区政府党组书记、区长候选人", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "待区人大依法任命为正式区长"},
    # 林干（区委副书记/政法委书记）
    {"person_id": 3, "org_id": 1, "title": "扎赉诺尔区委副书记", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "三届一次全会选举副书记"},
    {"person_id": 3, "org_id": 6, "title": "扎赉诺尔区委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 佟拉嘎（纪委书记）
    {"person_id": 4, "org_id": 5, "title": "扎赉诺尔区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "三届纪委一次全会当选书记，连任"},
    {"person_id": 4, "org_id": 13, "title": "扎赉诺尔区监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐国彬（宣传部长）
    {"person_id": 5, "org_id": 8, "title": "扎赉诺尔区委常委、宣传部部长", "start_date": "2026-06", "end_date": "present", "rank": "副处级", "note": "接任吴振丽（前任部长）"},
    # 王静（统战部长）
    {"person_id": 6, "org_id": 9, "title": "扎赉诺尔区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 金布成（常务副区长）
    {"person_id": 7, "org_id": 2, "title": "扎赉诺尔区委常委、区政府党组副书记、常务副区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "分管发改/能源/城建/交通/应急/统计/招商/政务"},
    # 高旭斌（副区长）
    {"person_id": 8, "org_id": 2, "title": "扎赉诺尔区委常委、区政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管财税/国资/城管/农牧水利/卫健/生态"},
    # 井树冬（区委办主任）
    {"person_id": 9, "org_id": 10, "title": "扎赉诺尔区委常委、办公室办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "保密/机要/改革/政策研究/档案"},
    # 冯爆（组织部长）
    {"person_id": 10, "org_id": 7, "title": "扎赉诺尔区委常委、组织部部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "组织/编办/老干/公务员/人才"},
# 胡毅（人武部政委）
    {"person_id": 11, "org_id": 11, "title": "扎赉诺尔区人民武装部上校政治委员", "start_date": "", "end_date": "present", "rank": "", "note": "国防动员/边防/军事"},
    {"person_id": 11, "org_id": 1, "title": "扎赉诺尔区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨波（副区长/公安局长）
    {"person_id": 12, "org_id": 2, "title": "扎赉诺尔区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "社会稳定/依法治区/信访"},
    {"person_id": 12, "org_id": 12, "title": "呼伦贝尔市公安局扎赉诺尔分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科/副处级", "note": "公安/司法/信访"},
    # 白琰（副区长）
    {"person_id": 13, "org_id": 2, "title": "扎赉诺尔区副区长（政府党组成员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "工信/科技/商贸/教育/民政/文旅/园区"},
    # 王胜利（人大主任）
    {"person_id": 14, "org_id": 3, "title": "扎赉诺尔区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 高胜（政协主席）
    {"person_id": 15, "org_id": 4, "title": "扎赉诺尔区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 齐善剑（前任区委书记）
    {"person_id": 16, "org_id": 1, "title": "扎赆诺尔区委书记（前任）", "start_date": "2022-03", "end_date": "2026-06", "rank": "正处级", "note": "2022-03 任满洲里市委常委兼扎赉诺尔区委书记"},
    {"person_id": 16, "org_id": 16, "title": "满洲里市委常委、政法委书记", "start_date": "", "end_date": "2022-03", "rank": "副地级", "note": ""},
    {"person_id": 16, "org_id": 18, "title": "中共鄂伦春自治旗委书记（现任）", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026-06 调任鄂伦春旗"},
    # 张乔（前任区长）
    {"person_id": 17, "org_id": 2, "title": "扎赉诺尔区区长（前任）", "start_date": "2022", "end_date": "2024-2025", "rank": "正处级", "note": "任内与齐善剑搭班子"},
    {"person_id": 17, "org_id": 20, "title": "呼伦贝尔市住房和城乡建设局局长", "start_date": "约2025", "end_date": "present", "rank": "正处级", "note": "卸任区长后调任"},
    # 吴振丽（前任宣传部长）
    {"person_id": 18, "org_id": 8, "title": "扎赉诺尔区委宣传部部长（前任）", "start_date": "2025及以前", "end_date": "2026-06", "rank": "副处级", "note": "2026-04 报道仍在任，换届后由徐国彬接任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS (person <-> person)
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政核心搭档：布尔金 — 万宏宇
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "布尔金任区委书记、万宏宇任区长候选人/区政府党组书记，构成区委—政府核心搭档", "overlap_org": "扎赉诺尔区委员会/政府", "overlap_period": "2026-06—present"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与专职副书记、政法委书记共同属区委班子", "overlap_org": "扎赉诺尔区委员会", "overlap_period": "2026-06—present"},
    {"person_a": 2, "person_b": 3, "type": "同事", "context": "区长候选人（区委副书记）与专职副书记同属区委班子", "overlap_org": "扎赉诺尔区委员会", "overlap_period": "2026-06—present"},
    # 布尔金 — 前任区委书记 齐善剑（前任后任）
    {"person_a": 1, "person_b": 16, "type": "前任后任", "context": "齐善剑 2022-03-2026-06 任扎赉诺尔区委书记，2026-06 由布尔金接任；此前两人同为满洲里市委常委（布尔 2023-06 起）", "overlap_org": "中共扎赉诺尔区委员会/中共满洲里市委员会", "overlap_period": "2026-06（同为满洲里市委常委 2023-06）"},
    # 布尔金 — 前任区长 张兴旺（前任后任）
    {"person_a": 1, "person_b": 17, "type": "前任后任", "context": "张兴旺 2022-2024 任扎赉区长，布尔金 2025-04 接任", "overlap_org": "扎达区政府/扎赉诺尔区人民政府", "overlap_period": "2025"},
    # 布尔金 — 万宏宇（鄂温克旗人事流动共同背景）
    {"person_a": 1, "person_b": 7, "type": "同事", "context": "布尔金曾为鄂温克旗副旗长，金文成来自鄂温克旗（2021-06起副旗长提名人选），同鄂温克系干部", "overlap_org": "鄂温克族自治旗政府", "overlap_period": "2020s"},
    {"person_a": 2, "person_b": 7, "type": "同事", "context": "万宏宇曾任鄂温克旗副旗长（2021-07），金文成来自鄂温克旗，鄂温克—扎赉干部交流带", "overlap_org": "鄂温克族自治旗政府", "overlap_period": "2021—2025"},
    # 书记—各常务（委班子）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与纪委书记佟拉嘎（常委会）", "overlap_org": "中共扎赉诺尔区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委与宣传部部长徐国彬（常委会）", "overlap_org": "中共扎赉诺尔区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委与组织部部长冯暴（常委会）", "overlap_org": "中共扎赉诺尔区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委与办公室主任井树冬（常委会）", "overlap_org": "中共扎赉诺尔区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "区委与人武部政委胡毅（常委会）", "overlap_org": "中共扎赉诺尔区委员会/人武部", "overlap_period": "present"},
    # 布尔金—各副区长
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "区长与副区长兼公安局长杨波（区政府党组）", "overlap_org": "扎赉诺尔区人民政府", "overlap_period": "present"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "区长与副区长白琰（政府党组）", "overlap_org": "扎赉诺尔区人民政府", "overlap_period": "present"},
    # 前任—人大/政协
    {"person_a": 16, "person_b": 14, "type": "同事", "context": "齐善剑任区委书记期间（2022-2026）、王胜利任人大主任，党政人大班子联动", "overlap_org": "扎赉诺尔区", "overlap_period": "2022-2026"},
    {"person_a": 16, "person_b": 15, "type": "同事", "context": "齐善剑任书记期间、高胜任政协主席", "overlap_org": "扎赉诺尔区", "overlap_period": "2022-2026"},
    # 前任区长与前任书记
    {"person_a": 16, "person_b": 17, "type": "同事", "context": "齐善剑（书记）与张兴旺（区长）2022-2024 搭班子", "overlap_org": "扎赉诺尔区委员会/政府", "overlap_period": "2022—2024"},
    # 宣传部部长更替
    {"person_a": 5, "person_b": 18, "type": "前任后任", "context": "徐国彬接任吴振丽任宣传部部长", "overlap_org": "扎赉诺尔区委宣传部", "overlap_period": "2026"},
]

# ══════════════════════════════════════════════════════════════════════════════

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
    print("Build complete for 扎赉诺尔区.")