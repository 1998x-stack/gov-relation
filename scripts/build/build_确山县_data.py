#!/usr/bin/env python3
"""
确山县（驻马店市·河南省）领导班子工作关系网络 — 构建脚本

等级: 县 | 上级: 河南省驻马店市
调查日期: 2026-08-06
数据来源: 确山县人民政府门户 (www.queshan.gov.cn) 官方"领导信息"栏目政府领导简介
         与官方时政新闻《红色确山》多篇权威稿 (2025-07~2026-07)
说明: 调查期间外部搜索引擎 (Exa/Baidu/Bing/Google) 全部受限,采用 partial-evidence 模式;
      书记/县长身份、县委与县政府班子名单、前任书记及党政搭档关系均由官方来源确认,
      人物传记字段（出生/籍贯/学历/入党时间）以 open_questions 显式标注。
"""

import json
import sqlite3  # noqa — used by gov_relation.runner
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent
while not (_REPO_ROOT / "gov_relation").exists() and _REPO_ROOT != _REPO_ROOT.parent:
    _REPO_ROOT = _REPO_ROOT.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ──
SLUG = "确山县"
TODAY = "2026-08-06"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "驻马店市"
REGION = "确山县"

# ── Paths ──
HERE = Path(__file__).parent
DB_PATH = HERE / f"{REGION}_network.db"
GEXF_PATH = HERE / f"{REGION}_network.gexf"
PERSONS_DIR = HERE

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

XWS = "中共确山县委员会"
XZF = "确山县人民政府"

persons = [
    # ── 现任县委书记 (一把手) ──
    {
        "id": 1, "name": "蒋贵印", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县委书记", "current_org": XWS,
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202606/t20260623_706918.html — 确山县第十四次党代会预备会(2026-06-22)官方报道; 2026-05-12《县委书记蒋贵印到县委办公室调研》",
        "notes": "确山县委书记。原任确山县委副书记、县长(2025-07~2026-03官方稿称'县长蒋贵印');2026-05《县委书记蒋贵印到县委办公室调研》称'县委书记、县长蒋贵印'(党政一肩挑过渡);2026-06-22第十四次党代会确认为县委书记。出生/籍贯/学历/入党时间等公开渠道未获取。",
    },
    # ── 现任县长 (二把手) ──
    {
        "id": 2, "name": "王东亮", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县人民政府县长、党组书记", "current_org": XZF,
        "source": "https://www.queshan.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/t20241022_319927.html — 政府'领导信息'领导简介; 2026-06-22党代会; 2026-07-21《确山: 县长调研重点项目建设》",
        "notes": "男, 汉族, 中共党员。确山县委副书记, 县人民政府县长、党组书记, 主持县政府全面工作。任职起始约2026-06(接任蒋贵印转书记后的县长空缺)。任现职前履历公开渠道未详。",
    },
    # ── 前任县委书记 ──
    {
        "id": 3, "name": "路耕", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "（前任）确山县委书记", "current_org": XWS,
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202604/t20260410_696410.html — 2026-04-08《确山: 县委书记走访调研》; 2025-07~2025-12多篇官稿",
        "notes": "确山县委书记(前任)。2026-04-08官稿仍称'县委书记路耕',2026-03-18人大主席团常务主席仍列路耕居首;约2026-05由蒋贵印继任。卸任去向未公开。兼确山县人武部党委第一书记。",
    },
    # ── 县委副书记 ──
    {
        "id": 4, "name": "吴玉冰", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县委副书记", "current_org": XWS,
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202608/t20260805_717783.html — 2026-07-31县委中心组学习官稿; 2026-06-22党代会名单",
        "notes": "县委副书记。2026-06-22第十四次党代会列县委班子;2026-07-31中心组学习由其在书记主持后领学。",
    },
    # ── 县委常委/常务副县长 ──
    {
        "id": 5, "name": "杨坡", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县委常委、县人民政府常务副县长、党组副书记", "current_org": XZF,
        "source": "https://www.queshan.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/t20241022_319928.html — 政府领导简介; 2026-07-27书记县长调研官稿",
        "notes": "县委常委、常务副县长、党组副书记, 政府二号位。",
    },
    # ── 县委常委/宣传部部长 ──
    {
        "id": 6, "name": "王巧雨", "gender": "女", "ethnicity": "汉族", "birth": "1984-10",
        "birthplace": "", "native_place": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县委常委、县委宣传部部长, 政府副县长、党组成员", "current_org": "中共确山县委员会宣传部",
        "source": "https://www.queshan.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/t20241022_319929.html — 政府领导简介",
        "notes": "女, 汉族, 1984.10生, 在职研究生学历, 中共党员。县委常委、宣传部长兼县政府副县长。",
    },
    # ── 县委常委/纪委书记 ──
    {
        "id": 7, "name": "晏国兵", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县委常委、县纪委书记、县监委主任", "current_org": "中共确山县纪律检查委员会",
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202607/t20260709_710761.html — 2026-07-08县委中心组官稿; 2026-06-03人大会议",
        "notes": "县委常委、纪委书记、监委主任(监督条线)。",
    },
    # ── 县委常委/组织部部长 ──
    {
        "id": 8, "name": "戚斌", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县委常委、县委组织部部长", "current_org": "中共确山县委员会组织部",
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202607/t20260709_710761.html — 2026-07-08县委中心组官稿; 2026-03-18人大主席团名单",
        "notes": "县委常委、组织部长(干部人事条线)。",
    },
    # ── 县委常委/县委办公室主任 ──
    {
        "id": 9, "name": "张高峰", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县委常委、县委办公室主任", "current_org": "中共确山县委员会办公室",
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202608/t20260805_717783.html — 2026-07-31县委中心组官稿; 2026-06-04《十六届人大三十次会议》",
        "notes": "2025-12-10任'县委常委、宣传部部长、副县长张高峰';2026-06-03人大免除其副县长职务, 2026-07-31已任县委常委、县委办公室主任。",
    },
    # ── 副县长兼公安局长 ──
    {
        "id": 10, "name": "陈卫华", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县人民政府副县长、党组成员，县公安局局长", "current_org": "确山县公安局",
        "source": "https://www.queshan.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/t20241022_319930.html — 政府领导简介",
        "notes": "副县长兼公安局长(政法条线)。",
    },
    # ── 副县长 ──
    {
        "id": 11, "name": "刘冬梅", "gender": "女", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县人民政府副县长、党组成员", "current_org": XZF,
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202508/t20250820_647377.html — 2025-08县长调研官稿; 2026-06-04人大会议列席",
        "notes": "副县长, 陪同县长调研农业农村/乡村振兴工作。",
    },
    {
        "id": 12, "name": "杨东荣", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县人民政府副县长、党组成员", "current_org": XZF,
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202607/t20260723_713803.html — 2026-07-21县长调研官稿",
        "notes": "副县长。",
    },
    {
        "id": 13, "name": "王俊奇", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县人民政府副县长、党组成员", "current_org": XZF,
        "source": "https://www.queshan.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/t20251027_662524.html — 政府领导简介(2025-10)",
        "notes": "副县长(2025-10新增入政府班子)。",
    },
    {
        "id": 14, "name": "吕国凯", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县人民政府副县长、党组成员", "current_org": XZF,
        "source": "https://www.queshan.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/t20241022_319932.html — 政府领导简介",
        "notes": "副县长。",
    },
    # ── 县开发区管委会主任 ──
    {
        "id": 15, "name": "张杰", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "确山县开发区管委会主任", "current_org": "确山经济技术开发区管理委员会",
        "source": "https://www.queshan.gov.cn/zwyw/ttxw/202607/t20260723_713803.html — 2026-07-21县长调研官稿",
        "notes": "县开发区管委会主任(产业园区条线)。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共确山县委员会", "type": "党委", "level": "县处级", "parent": "中共驻马店市委员会", "location": "河南省驻马店市确山县"},
    {"id": 2, "name": "确山县人民政府", "type": "政府", "level": "县处级", "parent": "驻马店市人民政府", "location": "河南省驻马店市确山县"},
    {"id": 3, "name": "中共确山县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共确山县委员会", "location": "河南省驻马店市确山县"},
    {"id": 4, "name": "中共确山县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共确山县委员会", "location": "河南省驻马店市确山县"},
    {"id": 5, "name": "中共确山县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共确山县委员会", "location": "河南省驻马店市确山县"},
    {"id": 6, "name": "中共确山县委员会办公室", "type": "党委", "level": "县处级", "parent": "中共确山县委员会", "location": "河南省驻马店市确山县"},
    {"id": 7, "name": "确山县公安局", "type": "政府", "level": "县处级", "parent": "确山县人民政府", "location": "河南省驻马店市确山县"},
    {"id": 8, "name": "确山县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "驻马店市人大常委会", "location": "河南省驻马店市确山县"},
    {"id": 9, "name": "中国人民政治协商会议确山县委员会", "type": "政协", "level": "县处级", "parent": "政协驻马店市委员会", "location": "河南省驻马店市确山县"},
    {"id": 10, "name": "确山经济技术开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "确山县人民政府", "location": "河南省驻马店市确山县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 蒋贵印 (1)
    {"person_id": 1, "org_id": 1, "title": "确山县委书记", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026-05《县委书记蒋贵印到县委办公室调研》转任书记; 2026-06-22第十四次党代会确认"},
    {"person_id": 1, "org_id": 2, "title": "确山县人民政府县长(兼任过渡)", "start": "2026-05", "end": "2026-06", "rank": "正处级", "note": "'县委书记、县长蒋贵印'过渡期, 约2026-06交棒王东亮"},
    {"person_id": 1, "org_id": 2, "title": "确山县委副书记、县长", "start": "2025-07", "end": "2026-05", "rank": "正处级", "note": "2025-07/08/10官稿'县长蒋贵印'; 2026-03县政府全体会议县长讲话"},
    # 王东亮 (2)
    {"person_id": 2, "org_id": 1, "title": "确山县委副书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026-06-22第十四次党代会称'县委副书记、县长王东亮'"},
    {"person_id": 2, "org_id": 2, "title": "确山县人民政府县长、党组书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "政府领导之窗确认主持县政府全面工作; 2026-07多次调研"},
    # 路耕 (3) — 前任书记
    {"person_id": 3, "org_id": 1, "title": "确山县委书记(前任)", "start": "2025-07", "end": "2026-05", "rank": "正处级", "note": "2026-04-08官稿仍为书记; 约2026-05卸任交蒋贵印. 去向未公开"},
    # 吴玉冰 (4)
    {"person_id": 4, "org_id": 1, "title": "确山县委副书记", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026-06-22党代会; 2026-07-31县委中心组学习"},
    # 杨坡 (5)
    {"person_id": 5, "org_id": 1, "title": "确山县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": "县委班子"},
    {"person_id": 5, "org_id": 2, "title": "确山县常务副县长、党组副书记", "start": "unknown", "end": "present", "rank": "副处级", "note": "政府常务位"},
    # 王巧雨 (6)
    {"person_id": 6, "org_id": 1, "title": "确山县委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "宣传部部长"},
    {"person_id": 6, "org_id": 2, "title": "确山县副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": "政府领导简介"},
    # 晏国兵 (7)
    {"person_id": 7, "org_id": 1, "title": "确山县委常委、县纪委书记、县监委主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-07县委中心组领学"},
    # 戚斌 (8)
    {"person_id": 8, "org_id": 1, "title": "确山县委常委、县委组织部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-07县委中心组领学"},
    # 张高峰 (9)
    {"person_id": 9, "org_id": 1, "title": "确山县委常委、县委办公室主任", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026-07-31县委中心组领学; 2026-06-03免副县长后转办公室主任"},
    {"person_id": 9, "org_id": 2, "title": "确山县副县长(2025,免)", "start": "2025-12", "end": "2026-06", "rank": "副处级", "note": "2025-12-10'县委常委、宣传部部长、副县长'; 2026-06-03人大免除副县长"},
    {"person_id": 9, "org_id": 5, "title": "确山县委宣传部部长(已转)", "start": "2025-12", "end": "2026-06", "rank": "副处级", "note": ""},
    # 陈卫华 (10)
    {"person_id": 10, "org_id": 2, "title": "确山县副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "确山县公安局局长(兼)", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 刘冬梅 (11)
    {"person_id": 11, "org_id": 2, "title": "确山县副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管农工/乡村振兴"},
    # 杨东荣 (12)
    {"person_id": 12, "org_id": 2, "title": "确山县副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 王俊奇 (13)
    {"person_id": 13, "org_id": 2, "title": "确山县副县长、党组成员", "start": "2025-10", "end": "present", "rank": "副处级", "note": "2025-10-27领导简介"},
    # 吕国凯 (14)
    {"person_id": 14, "org_id": 2, "title": "确山县副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 张杰 (15)
    {"person_id": 15, "org_id": 2, "title": "确山县开发区管委会主任", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 10, "title": "确山经济技术开发区管委会主任", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 蒋贵印 ↔ 王东亮: 书记×县长 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记蒋贵印×县长(县委副书记)王东亮构成党政搭档, 2026年任内(2026-07-27'书记县长调研重点项目')", "overlap_org": "中共确山县委员会/确山县人民政府", "overlap_period": "2026-06至今"},
    # 蒋贵印 ↔ 路耕: 继任关系
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "蒋贵印继任路耕任确山县委书记(2026-05)", "overlap_org": "中共确山县委员会", "overlap_period": "2025-07~2026-06"},
    # 蒋贵印(县长时) ↔ 路耕(书记) 党政搭档
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "蒋贵印任县长期间与路耕(书记)搭班子", "overlap_org": "确山县", "overlap_period": "2025-07~2026-05"},
    # 王东亮 ↔ 杨坡: 县长×常务副县长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与常务副县长县政府班子搭档", "overlap_org": "确山县人民政府", "overlap_period": "2026-06至今"},
    # 蒋贵印 ↔ 吴玉冰: 县委班子
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "书记×副书记县委班子", "overlap_org": "中共确山县委员会", "overlap_period": "2026-06至今"},
    # 县委班子: 晏国兵、戚斌 × 蒋贵印
    {"person_a": 7, "person_b": 1, "type": "overlap", "context": "纪委书记为县委常委, 同届班子并参加县委中心组学习", "overlap_org": "中共确山县委员会", "overlap_period": "2026-至今"},
    {"person_a": 8, "person_b": 1, "type": "overlap", "context": "组织部长为县委常委, 同届班子", "overlap_org": "中共确山县委员会", "overlap_period": "2026-至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "确山县第十四次党代会举行预备会议(2026-06-22)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202606/t20260623_706918.html", "publisher": "确山县人民政府门户-红色确山", "published_at": "2026-06-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认蒋贵印为县委书记, 王东亮为县委副书记/县长, 吴玉冰为副书记"},
        {"id": "S002", "title": "确山: 县委书记蒋贵印到县委办公室调研(2026-05-12)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202605/t20260512_700419.html", "publisher": "确山县人民政府官网-红色确山", "published_at": "2026-05-12", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "称'县委书记、县长蒋贵印'确认蒋由县长转任书记"},
        {"id": "S003", "title": "确山: 县委书记到普会寺调研(2026-04-08)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202604/t20260410_696410.html", "publisher": "确山县人民政府官网", "published_at": "2026-04-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "前任县委书记路耕 2026-04 仍在任"},
        {"id": "S004", "title": "确山: 县委理论学习中心组学习会议召开(2026-07-09)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202607/t20260709_710761.html", "publisher": "确山县人民政府官网-红色确山", "published_at": "2026-07-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "书记蒋贵印主持; 晏国兵(纪委)、戚斌(组织部)领学"},
        {"id": "S005", "title": "王东亮 领导简介(政府·领导信息)", "url": "https://www.queshan.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/t20241022_319927.html", "publisher": "确山县人民政府门户", "published_at": None, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王东亮: 男, 汉族, 中共党员, 县委副书记, 县长、党组书记, 主持县政府全面工作; 杨坡/王巧雨/陈卫华等见 szfld 页"},
        {"id": "S006", "title": "确山: 县长调研重点项目建设(2026-07-22)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202607/t20260723_713803.html", "publisher": "确山县人民政府官网-红色确山", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长王东亮率队调研; 副县长杨东荣等陪同"},
        {"id": "S007", "title": "确山: 书记县长调研重点项目(2026-07-28)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202607/t20260730_716385.html", "publisher": "确山县人民政府官网-红色确山", "published_at": "2026-07-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委书记蒋贵印、县长王东亮带队调研县开发区并部署"},
        {"id": "S008", "title": "确山县十六届人大常委会第三十次会议(2026-06-04)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202606/t20260604_704393.html", "publisher": "确山县人民政府官网-红色确山", "published_at": "2026-06-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "免除张高峰副县长职务; 人大主任王月红"},
        {"id": "S009", "title": "确山县第十六届人民代表大会第六次会议闭幕(2026-03-19)", "url": "https://www.queshan.gov.cn/zwyw/ttxw/202603/t20260319_693375.html", "publisher": "确山县人民政府官网-红色确山", "published_at": "2026-03-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "主席团: 路耕、蒋贵印、吴玉冰等; 县政府列席名单"},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person, person_relationships, source_register, job) -> dict:
    timeline = timeline_for(person["id"])
    is_core = person["id"] in (1, 2, 3)
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE, "city": CITY, "region": REGION, "job": job,
            "task_id": "henan_确山县", "time_focus": "2026",
        },
        "identity": {
            "person_id": f"queshan_{person['name']}",
            "name": person["name"], "aliases": [], "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""), "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""), "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""), "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if person["id"] in (1, 2, 3) else "副处级",
            "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002", "S005"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder" if person["id"] in (1, 2) else "unknown",
            "systems_experience": ["party"] if person["id"] in (1, 3) else (["party", "government"] if person["id"] == 2 else ["government"]),
            "geographic_pattern": ["确山县(驻马店市)"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public reports, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在公开渠道发现纪律处分或负面报道信号",
                                         "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible" if person["id"] in (1, 3) else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin" if person["id"] in (1, 2, 3) else "partial",
            "relationship_confidence": "medium" if person["id"] in (1, 2, 3) else "low",
            "biggest_gap": "核心领导出生年份/籍贯/学历/入党时间及任现职前完整履历未公开确认",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年份/籍贯/学历/入党时间, 以及任现职前的完整任职履历",
             "why_it_matters": "姓名+出生年份是跨区去重与身份校准的关键",
             "suggested_queries": [f"{person['name']} 简历 确山", f"{person['name']} 任前公示 驻马店"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}任确山相关职务前的上一任职与来源单位",
             "why_it_matters": "还原晋升链条与跨区调动网络",
             "suggested_queries": [f"{person['name']} 驻马店 干部公示", f"{person['name']} 之前 担任"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "确山县委全体常委名单与分工(含王霞、杨彦博、黄新猛的职务)",
             "why_it_matters": "细化县委常委会关系网络",
             "suggested_queries": ["确山县 新一届县委班子 名单", "确山 常委 分工"],
             "last_attempted": AS_OF},
        ],
    }


def timeline_for(pid: int) -> list[dict]:
    if pid == 1:
        return [
            {"start": "unknown", "end": "2025-07", "org": "履历缺口", "title": "",
             "notes": "蒋贵印任确山县县长前的履历(上一站/出生年度)公开渠道未获取", "confidence": "unverified", "source_ids": []},
            {"start": "2025-07", "end": "2026-05", "org": "确山县人民政府", "title": "县委副书记、县长",
             "notes": "2025-07/08/10官稿'县长蒋贵印'调研; 2026-03县政府全体会议县长讲话", "confidence": "confirmed", "source_ids": ["S006", "S009"]},
            {"start": "2026-05", "end": "2026-06", "org": "确山县", "title": "县委书记、县长(党政一肩挑过渡)",
             "notes": "2026-05-12官稿'县委书记、县长蒋贵印'", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2026-05", "end": "present", "org": "中共确山县委员会", "title": "确山县委书记",
             "notes": "2026-07-09中心组主持; 2026-07-28书记县长调研部署", "confidence": "confirmed", "source_ids": ["S004", "S007"]},
        ]
    if pid == 2:
        return [
            {"start": "unknown", "end": "2026-06", "org": "履历缺口", "title": "",
             "notes": "王东亮任确山县县长前的履历公开渠道未获取", "confidence": "unverified", "source_ids": []},
            {"start": "2026-06", "end": "present", "org": "确山县人民政府", "title": "县长、党组书记",
             "notes": "政府'领导信息'之窗确认为县长, 主持县政府全面工作", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2026-06", "end": "present", "org": "中共确山县委员会", "title": "县委副书记",
             "notes": "2026-06-22党代会'县委副书记、县长王东亮'", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    # pid 3 路耕
    return [
        {"start": "unknown", "end": "2025-07", "org": "履历缺口", "title": "",
         "notes": "路耕任确山县委书记前的背景(出生/籍贯/学历)公开渠道未获取", "confidence": "unverified", "source_ids": []},
        {"start": "2025-07", "end": "2026-05", "org": "中共确山县委员会", "title": "确山县委书记、县人武部党委第一书记",
         "notes": "2026-04-08官稿仍为书记; 2026-03-18人大主席团居首", "confidence": "confirmed", "source_ids": ["S003", "S009"]},
        {"start": "2026-05", "end": "unknown", "org": "去向未明", "title": "卸任(去向未公开)",
         "notes": "约2026-05卸任交蒋贵印", "confidence": "unverified", "source_ids": []},
    ]


def build():
    print("=" * 60)
    print("确山县领导班子工作关系网络")
    print("等级: 县 | 上级: 驻马店市(河南省) | 调查: 2026-08-06")
    print("来源: 确山县人民政府门户官方新闻/领导简介")
    print("=" * 60)

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

    print(f"\n✅ DB/GEXF 构建完成。")
    print(f"  人物: {len(persons)} | 机构: {len(organizations)} | 任职: {len(positions)} | 关系: {len(relationships)}")

    source_register = make_source_register()

    # 1. 蒋贵印 (县委书记)
    jiang_json = make_person_json(persons[0], [
        {"person": "王东亮", "person_id": "queshan_王东亮", "relationship_type": "overlap", "strength": "strong",
         "evidence": "书记×副书记/县长党政搭档(2026-迄今)", "overlap_org": "确山县", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S007"]},
        {"person": "路耕", "person_id": "queshan_路耕", "relationship_type": "predecessor_successor", "strength": "strong",
         "evidence": "接任路耕任新书记", "overlap_org": "中共确山县委员会", "overlap_period": "2026-05",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "吴玉冰", "person_id": "queshan_吴玉冰", "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委班子成员", "overlap_org": "中共确山县委员会", "overlap_period": "2026-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ], source_register, "县委书记")
    jiang_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县委书记-蒋贵印.json"
    with open(jiang_path, "w", encoding="utf-8") as f:
        json.dump(jiang_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 蒋贵印")

    # 2. 王东亮 (县长)
    wang_json = make_person_json(persons[1], [
        {"person": "蒋贵印", "person_id": "queshan_蒋贵印", "relationship_type": "overlap", "strength": "strong",
         "evidence": "县长×书记 党政搭档(2026起)", "overlap_org": "确山县", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S005", "S007"]},
        {"person": "杨坡", "person_id": "queshan_杨坡", "relationship_type": "overlap", "strength": "medium",
         "evidence": "县长×常务副县长 政府班子搭档", "overlap_org": "确山县人民政府", "overlap_period": "2026-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
    ], source_register, "县长")
    wang_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县长-王东亮.json"
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 王东亮")

    # 3. 路耕 (前任县委书记)
    lu_json = make_person_json(persons[2], [
        {"person": "蒋贵印", "person_id": "queshan_蒋贵印", "relationship_type": "predecessor_successor", "strength": "medium",
         "evidence": "蒋贵印继任其书记职务", "overlap_org": "中共确山县委员会", "overlap_period": "2026-05",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ], source_register, "前任县委书记")
    lu_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-前任县委书记-路耕.json"
    with open(lu_path, "w", encoding="utf-8") as f:
        json.dump(lu_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 路耕")

    print(f"\nPerson Graph JSONs 生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()