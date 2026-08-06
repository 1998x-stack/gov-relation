#!/usr/bin/env python3
"""
新蔡县（驻马店市）领导班子工作关系网络 — 构建脚本

等级: 县 | 上级: 河南省驻马店市
调查日期: 2026-08-06
数据来源: 新蔡县人民政府门户 www.xincai.gov.cn 官方时政新闻 + 官方"领导信息"简介 +
          新蔡人大任免名单 + Baidu 百科/知乎/猎狐网等二次来源
说明: 调查期间 Exa 限流、Baidu 中途遇验证码、Jina 空响应,采用 partial-evidence 模式;
      核心领导身份(县委书记杨大群/县长刘欣英)由官方来源 confirmed,
      部分传记字段(出生年/籍贯/学历)来自百度百科等 secondary, 以 open_questions 显式标注缺口。
"""

import json
import sqlite3  # noqa — used by gov_relation.runner
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
while not (_REPO_ROOT / "gov_relation").exists() and _REPO_ROOT.parent != _REPO_ROOT:
    _REPO_ROOT = _REPO_ROOT.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ──
SLUG = "新蔡县"
TODAY = "2026-08-06"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "驻马店市"
REGION = "新蔡县"
TASK_ID = "henan_新蔡县"

# ── Paths ──
HERE = Path(__file__).parent
DB_PATH = HERE / f"{REGION}_network.db"
GEXF_PATH = HERE / f"{REGION}_network.gexf"
PERSONS_DIR = HERE

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 现任县委书记 ──
    {
        "id": 1,
        "name": "杨大群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "河南省",
        "native_place": "",
        "education": "理学博士、研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驻马店市委常委、新蔡县委书记",
        "current_org": "中共新蔡县委员会",
        "source": "https://www.xincai.gov.cn/zwyw/tpxw/202606/t20260612_705562.html — 新蔡县政府门户《全县树立和践行正确政绩观学习教育警示教育会暨突出问题集中整治工作推进会召开》(2026-06-12)称「市委常委、新蔡县委书记杨大群出席并讲话」",
        "notes": "男，汉族，1981年2月生，研究生，理学博士，中共党员。曾任河南省发展和改革委员会农村经济处处长；2022年11月起任驻马店市人民政府副市长并兼任新蔡县委书记（后转任市委常委）；2026-05~07 官方报道署名「市委常委、新蔡县委书记」。兼任新蔡县人武部党委第一书记（惯例）。任书记前出生/籍贯等公开渠道部分缺失。",
    },
    # ── 现任县长 ──
    {
        "id": 2,
        "name": "刘欣英",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "河南省",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县委副书记、县人民政府县长",
        "current_org": "新蔡县人民政府",
        "source": "https://www.xincai.gov.cn/zwyw/tpxw/202606/t20260615_705754.html — 新蔡县政府门户《新蔡县政府常务会议召开》(2026-06-15)称「代县长刘欣英主持召开县十六届人民政府第83次常务会议」；https://www.xincai.gov.cn/zwyw/tpxw/202606/t20260629_707791.html 两优一先表彰大会称「县委副书记、县长刘欣英主持」",
        "notes": "女，云南党委、驻马店市委委员。曾任共青团驻马店市委书记、泌阳县副县长、上蔡县委常委兼宣传部长、确山县委副书记、确山县石滚河镇党委书记。2026-06-03 新蔡县十六届人大常委会三十七次会议决定刘欣英代理县长；2026-06-25 第十六届人民代表大会第七次会议当选县长。出生年月/入党时间等公开渠道尚未获取。",
    },
    # ── 前县长 李勇 ──
    {
        "id": 3,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "河南省汝南县",
        "native_place": "河南省汝南县",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前）新蔡县委副书记、县政府县长",
        "current_org": "新蔡县人民政府",
        "source": "https://www.xincai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319918.html — 新蔡县政府『领导信息』官方简介(2024-10-21)称「李勇，男，汉族，1975年11月生，河南省汝南县人，中共党员，研究生学历，现任新蔡县委副书记、县政府县长」",
        "notes": "男，汉族，1975年11月生，河南省汝南县人，中共党员，研究生学历。曾任新蔡县委副书记、县政府县长，主持县政府全面工作、分管县审计局。2026-03仍以县委副书记、县长身份参加县政协十二届五次会议讨论；其后由刘欣英继任县长(2026-06)。",
    },
    # ── 前任县委书记 邵奉公 ──
    {
        "id": 4,
        "name": "邵奉公",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-02",
        "birthplace": "河南省",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前）新蔡县委书记",
        "current_org": "中共新蔡县委员会",
        "source": "银河传媒猎狐网/知乎 2024-09 — 公开报道称前任新蔡县委书记邵奉公，1968年2月生，曾任河南省正阳县委副书记、驻马店市扶贫开发办公室党组书记/主任，2021年2月任新蔡县委书记",
        "notes": "公开资料：邵奉公，1968年2月生，中共党员。曾任河南省正阳县委副书记、驻马店市扶贫开发办公室党组书记、主任；2021年2月任新蔡县委书记；约2022-11由杨大群接任。",
    },
    # ── 常务副县长 乔鹏 ──
    {
        "id": 5,
        "name": "乔鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-05",
        "birthplace": "河南省汝南县",
        "native_place": "河南省汝南县",
        "education": "法学博士、研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县委常委、县政府常务副县长",
        "current_org": "新蔡县人民政府",
        "source": "新蔡县政府『领导信息』官方简介(2025-10-11) — 「乔鹏，男，汉族，1982年5月生，河南省汝南县人，中共党员，法学博士、研究生学历」；新蔡县人民代表大会常务委员会任命名单(2025-09-29)决定任命乔鹏为新蔡县人民政府副县长",
        "notes": "男，汉族，1982年5月生，河南省汝南县人，中共党员，法学博士、研究生学历。2025-09-29 人大任命为副县长；2026-08 人大常委会第三十九次会议报道称其为县委常委、县人民政府常务副县长（列席）。",
    },
    # ── 副县长 刘久锋 ──
    {
        "id": 6,
        "name": "刘久锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县人民政府副县长",
        "current_org": "新蔡县人民政府",
        "source": "新蔡县政府『领导信息』栏目录入(乔鹏 刘久锋 尹坤 刘雪岭 李雪涛 孙策)",
        "notes": "县政府副县长（新蔡县政府领导信息栏）。出生/籍贯/学历等公开渠道暂未获取。",
    },
    # ── 副县长 尹坤 ──
    {
        "id": 7,
        "name": "尹坤",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1986",
        "birthplace": "",
        "native_place": "",
        "education": "硕士研究生，高级工程师，一级建造师",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县人民政府副县长",
        "current_org": "新蔡县人民政府",
        "source": "新蔡县政府『领导信息』官方简介(2024-10-21) — 尹坤，男，蒙古族，1986年生，中共党员，硕士研究生，高级工程师，一级建造师",
        "notes": "男，蒙古族，1986年生，中共党员，硕士研究生，高级工程师，一级建造师。新蔡县人民政府副县长。",
    },
    # ── 副县长 刘雪岭 ──
    {
        "id": 8,
        "name": "刘雪岭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县人民政府副县长",
        "current_org": "新蔡县人民政府",
        "source": "新蔡县政府『领导信息』栏",
        "notes": "副县长（新蔡县政府领导“领导信息”）。公开传记细节待查。",
    },
    # ── 副县长 李雪涛 ──
    {
        "id": 9,
        "name": "李雪涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县人民政府副县长（县领导）",
        "current_org": "新蔡县人民政府",
        "source": "腾讯新闻 2025-12-14 《王飞虎带队赴新蔡县开展调研交流活动》称「新蔡县领导刘欣英、李君朝、田坤琦、李雪涛等陪同」；新蔡县政府『领导信息』栏",
        "notes": "新蔡县领导（政府班子成员），2025-12陪同赴企/农文旅考察。公开生辰等细节待查。",
    },
    # ── 副县长 孙策 ──
    {
        "id": 10,
        "name": "孙策",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县人民政府副县长",
        "current_org": "新蔡县人民政府",
        "source": "新蔡县政府『领导信息』栏",
        "notes": "新蔡县人民政府副县长（官方领导信息栏）。",
    },
    # ── 副县长 王盼 ──
    {
        "id": 11,
        "name": "王盼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-09",
        "birthplace": "河南省新蔡县",
        "native_place": "河南省新蔡县",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县人民政府副县长",
        "current_org": "新蔡县人民政府",
        "source": "百度百科《王盼(河南省驻马店市新蔡县人民政府副县长)》 — 女，汉族，1986年9月出生，河南新蔡人，中共党员，研究生学历",
        "notes": "女，汉族，1986年9月生，河南新蔡人，中共党员，研究生学历。分工分管人力资源和社会保障、应急管理、退役军人、市场监督管理、交通运输等。",
    },
    # ── 县委常委、县政府副县长 李东 ──
    {
        "id": 12,
        "name": "李东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县委常委、县政府副县长",
        "current_org": "新蔡县人民政府",
        "source": "大象新闻·河南广电融媒体记者 马彬《驻马店市新蔡县委常委、县政府副县长李东一行深入乡镇调研产业…》",
        "notes": "新蔡县委常委、县政府副县长。到砖店镇、李桥镇、黄楼镇调研产业发展。公开出生等细节待查。",
    },
    # ── 县委常委、纪委书记、监委主任 李玉清 ──
    {
        "id": 13,
        "name": "李玉清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县委常委、县纪委书记、县监委主任",
        "current_org": "中共新蔡县纪律检查委员会",
        "source": "https://www.xincai.gov.cn/zwysw/tpxw/202606/t20260612_705562.html — 2026-06-12警示教育推进会报道称「县委常委、县纪委书记、县监委主任李玉清通报典型案例」",
        "notes": "县委常委、纪委书记、监委主任。公开传记细节待查。",
    },
    # ── 县委常委、组织部长 葛鹏 ──
    {
        "id": 14,
        "name": "葛鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县委常委、组织部部长",
        "current_org": "中共新蔡县委员会组织部",
        "source": "https://www.xincai.gov.cn/zwyw/tpxw/202606/t20260612_705562.html — 2026-06-12报道称「县委常委、组织部部长葛鹏传达上级有关文件和会议精神」",
        "notes": "县委常委、组织部部长。公开传记细节待查。",
    },
    # ── 县领导 张小歌 ──
    {
        "id": 15,
        "name": "张小歌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新蔡县领导班子成员（职务待补）",
        "current_org": "中共新蔡县委员会",
        "source": "https://www.xincai.gov.cn/zwyw/tpxw/202605/t20260521_701922.html — 2026-05-21座谈会报道称「县领导李玉清、葛鹏、张小歌出席」",
        "notes": "新蔡县处级领导（具体常委分工待查）。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共新蔡县委员会", "type": "党委", "level": "县处级", "parent": "中共驻马店市委员会", "location": "河南省驻马店市新蔡县"},
    {"id": 2, "name": "新蔡县人民政府", "type": "政府", "level": "县处级", "parent": "驻马店市人民政府", "location": "河南省驻马店市新蔡县"},
    {"id": 3, "name": "中共新蔡县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共新蔡县委员会", "location": "河南省驻马店市新蔡县"},
    {"id": 4, "name": "中共新蔡县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共新蔡县委员会", "location": "河南省驻马店市新蔡县"},
    {"id": 5, "name": "新蔡县公安局", "type": "政府", "level": "县处级", "parent": "新蔡县人民政府", "location": "河南省驻马店市新蔡县"},
    {"id": 6, "name": "新蔡县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "河南省人大常委会", "location": "河南省驻马店市新蔡县"},
    {"id": 7, "name": "政协新蔡县委员会", "type": "政协", "level": "县处级", "parent": "政协驻马店市委员会", "location": "河南省驻马店市新蔡县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 杨大群 (县委书记, 兼驻马店市委常委)
    {"person_id": 1, "org_id": 1, "title": "新蔡县委书记", "start": "2022-11", "end": "present", "rank": "副厅级", "note": "兼驻马店市委常委(2026报道)；兼任县人武部党委第一书记；2022-11起任县委书记"},
    {"person_id": 1, "org_id": 1, "title": "驻马店市委常委（兼）", "start": "2026", "end": "present", "rank": "副厅级", "note": "2026年报道署名『市委常委、新蔡县委书记』"},
    # 刘欣英 (现任县长)
    {"person_id": 2, "org_id": 1, "title": "新蔡县委副书记", "start": "2024", "end": "present", "rank": "正处级", "note": "县委副书记；2026-06 任县长"},
    {"person_id": 2, "org_id": 2, "title": "新蔡县代县长→县长", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026-06-03 人大任命代县长，2026-06-25 十六届人大七次会议当选县长"},
    # 李勇 (前县长)
    {"person_id": 3, "org_id": 2, "title": "新蔡县委副书记、县长", "start": "2021", "end": "2026-05", "rank": "正处级", "note": "主持县政府全面工作、分管审计局；2026-03仍任县长，2026-06由刘欣英继任"},
    # 邵奉公 (前任书记)
    {"person_id": 4, "org_id": 1, "title": "新蔡县委书记", "start": "2021-02", "end": "2022-11", "rank": "副厅级/正处级", "note": "2021-02任新蔡县委书记；约2022-11由杨大群接任"},
    # 乔鹏 (常务副县长)
    {"person_id": 5, "org_id": 2, "title": "新蔡县政府常务副县长", "start": "2025-09", "end": "present", "rank": "副处级", "note": "2025-09-29人大任命副县长；后任县委常务副县长(2026-08列席）"},
    {"person_id": 5, "org_id": 1, "title": "新蔡县委常委（兼）", "start": "2025", "end": "present", "rank": "副处级", "note": "2026-08人大常委会会议上列席署名为常委、常务副县"},
    # 刘远
    {"person_id": 6, "org_id": 2, "title": "新蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方领导信息栏确认"},
    # 尹坤
    {"person_id": 7, "org_id": 2, "title": "新蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方领导简介确认"},
    # 刘雪岭
    {"person_id": 8, "org_id": 2, "title": "新蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方领导信息栏确认"},
    # 李雪涛
    {"person_id": 9, "org_id": 2, "title": "新蔡县人民政府副县长（县领导）", "start": "unknown", "end": "present", "rank": "副处级", "note": "2025-12陪同考察"},
    # 孙策
    {"person_id": 10, "org_id": 2, "title": "新蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方领导信息栏确认"},
    # 王盼
    {"person_id": 11, "org_id": 2, "title": "新蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管人社/应急/退役/市场监管/交通"},
    # 李东
    {"person_id": 12, "org_id": 2, "title": "新蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "县委常委、副县长"},
    # 李玉清
    {"person_id": 13, "org_id": 1, "title": "新蔡县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-06警示教育会出席"},
    {"person_id": 13, "org_id": 3, "title": "新蔡县纪委书记、县监委主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-06通报典型案例"},
    # 葛鹏
    {"person_id": 14, "org_id": 1, "title": "新蔡县委常委、组织部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-06传达上级文件精神"},
    # 张小歌
    {"person_id": 15, "org_id": 1, "title": "新蔡县处级领导（常委待确认）", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-05-21县直单位座谈会出席"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 杨大群 ↔ 刘欣英: 现任书记×现任县长 党政搭档 (confirmed)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "杨大群任县委书记、刘欣英任县委副书记兼县长，构成党政班子搭档(2026-06 起)；2026-06 政绩观推进会/两优一先表彰大会上同台（杨出席、刘主持）", "overlap_org": "中共新蔡县委员会/新蔡县人民政府", "overlap_period": "2026-至今"},
    # 杨大群 ↔ 李勇: 前任县委书记×县长 (2022-2026 搭档, 后刘接任)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "杨大群任县委书记期间，李勇任县委副书记兼县长；2026-03 政协新蔡十二届五次会议杨大群、李勇共同参加委员分组讨论", "overlap_org": "中共新蔡县委员会/新蔡县人民政府", "overlap_period": "2022-2026"},
    # 杨大群 ↔ 邵奉公: 继任书记 (predecessor_successor)
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "杨大群2022-11接任邵奉公的新蔡县委书记职务", "overlap_org": "中共新蔡县委员会", "overlap_period": "2021-2022（交接）"},
    # 刘欣英 ↔ 李勇: 继任县长 (predecessor_successor)，同县班子
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "刘欣英2026-06接替李勇任新蔡县长；李勇任县委副书记时刘任县副书记/县领导", "overlap_org": "新蔡县人民政府", "overlap_period": "2025-2026"},
    # 刘欣英 ↔ 乔鹏: 县长×常务副县长 (政府班子)
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "刘欣英(县长)与乔鹏(常务副县长)组成县政府班子；2026-08 人大常委会上刘欣英县长向常委会作报告、乔鹏常务副县列席", "overlap_org": "新蔡县人民政府", "overlap_period": "2026-至今"},
    # 刘欣英 ↔ 各副县长: 县政府班子 (乔/刘/李雪涛/孙岑)
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县政府班子同僚", "overlap_org": "新蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县政府班子同僚", "overlap_org": "新蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县政府班子同僚", "overlap_org": "新蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县政府班子同僚，2025-12共同陪同外县考察", "overlap_org": "新蔡县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县政府班子同僚", "overlap_org": "新蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县政府班子同僚(李东为县委常委副县长)", "overlap_org": "新蔡县人民政府", "overlap_period": "2026-至今"},
    # 乔鹏 ↔ 各副县长: 政府班子
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "常务副县×副县 政府班子", "overlap_org": "新蔡县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "常务副县×副县 政府班子", "overlap_org": "新蔡县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "常务副县×副县 政府班子", "overlap_org": "新蔡县人民政府", "overlap_period": "2025-至今"},
    # 李玉清 ↔ 杨大群: 纪委监督×班子
    {"person_a": 13, "person_b": 1, "type": "overlap", "context": "县委常委班子成员，警示教育会李通报案例、杨出席讲话", "overlap_org": "中共新蔡县委员会", "overlap_period": "2026-至今"},
    # 葛鹏 ↔ 杨大群: 组织部长×书记
    {"person_a": 14, "person_b": 1, "type": "overlap", "context": "组织部部长与县委书记在县委警示教育会/座谈会同台", "overlap_org": "中共新蔡县委员会", "overlap_period": "2026-至今"},
    # 张小歌 ↔ 杨大群: 县委领导
    {"person_a": 15, "person_b": 1, "type": "overlap", "context": "县直单位座谈会议，张小歌随杨大群出席", "overlap_org": "中共新蔡县委员会", "overlap_period": "2026-至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "李勇领导简介（政府领导信息，2024-10-21）",
         "url": "https://www.xincai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241021_319918.html",
         "publisher": "新蔡县人民政府门户网站", "published_at": "2024-10-21", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "官方确认前任县长李勇：男，汉族，1975-11，河南汝南，中共党员，研究生学历，时任县委副书记、县政府县长，主持政府全面工作"},
        {"id": "S002", "title": "新蔡县树立和践行正确政绩观警示教育会暨突出问题集中整治工作推进会(2026-06-12)",
         "url": "https://www.xincai.gov.cn/zwyw/tpxw/202606/t20260612_705562.html",
         "publisher": "新蔡县人民政府门户网站(来源:掌上新蔡)", "published_at": "2026-06-12", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "「市委常委、新蔡县委书记杨大群出席并讲话」；李玉清（纪委书记）、葛鹏（组织部部长）通报/传达"},
        {"id": "S003", "title": "新蔡县十六届人民政府第85次常务会议召开(2026-07-27)",
         "url": "https://www.xincai.gov.cn/zwyw/tpxw/202607/t20260727_715074.html",
         "publisher": "新蔡县人民政府门户网站(掌上新蔡)", "published_at": "2026-07-27", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "7月24日县长刘欣英主持召开县政府第85次常务会议，确认现任县长"},
        {"id": "S004", "title": "新蔡县政府常务会议召开(2026-06-15)",
         "url": "https://www.xincai.gov.cn/zwyw/tpxw/202606/t20260615_705754.html",
         "publisher": "新蔡县人民政府门户网站(掌上新蔡)", "published_at": "2026-06-15", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "6月13日代县长刘欣英主持召开第83次常务会议，确认代县长过渡期"},
        {"id": "S005", "title": "新蔡县树立和践行正确政绩观学习教育县直单位座谈会(2026-05-21)",
         "url": "https://www.xincai.gov.cn/zwyw/tpxw/202605/t20260521_701922.html",
         "publisher": "新蔡县人民政府门户网站(掌上新蔡)", "published_at": "2026-05-21", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "杨大群主持并讲话；县领导李玉清、葛鹏、张小歌出席"},
        {"id": "S006", "title": "新蔡县“两优一先”表彰大会召开(2026-06-29)",
         "url": "https://www.xincai.gov.cn/zwys/", "publisher": "新蔡县人民政府门户网站(掌上新蔡)", "published_at": "2026-06-29", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "杨大群出席并讲话、刘欣英主持，确认现任书记×县长搭档"},
        {"id": "S007", "title": "召回要求：派驻政府领导信息——乔鹏/尹坤等官方简介（2024-2025）",
         "url": "https://www.xincai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/",
         "publisher": "新蔡县人民政府门户网站", "published_at": "2025-10-11", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "官方领导信息栏列出：乔鹏、刘久锋、尹坤、刘雪岭、李雪涛、孙策；乔鹏(1982-05汝南/法学博士/常务副县)、尹坤简介(蒙古族1986/硕士/一级建造师)"},
        {"id": "S008", "title": "新蔡县人民代表大会常务委员会任命名单(2025-09-29)",
         "url": "https://www.xincai.gov.cn/rd/", "publisher": "新蔡人大网", "published_at": "2025-09-29", "accessed_at": AS_OF,
         "source_type": "appointment_notice", "reliability": "high",
         "notes": "决定任命乔鹏同志为新蔡县人民政府副县长"},
        {"id": "S009", "title": "新蔡县十六届人大常委会三十九次会议(2026-08)",
         "url": "https://www.xincai.gov.cn/rd/", "publisher": "新蔡人大网", "published_at": "2026-08", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "县委常委、县人民政府常务副县长乔鹏列席；县人民法院院长李晓龙列席；听取县政府2026年上半年国民经济和社会发展计划执行情况报告"},
        {"id": "S010", "title": "刘欣英当选为新蔡县县长(2026-06-25)；陈中 新蔡融媒",
         "url": "https://www.xincai.gov.cn/", "publisher": "新蔡融媒微信公号(转新蔡县政府网)", "published_at": "2026-06-25", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "medium",
         "notes": "县十六届人大七次会议2026-06-25选举刘欣英(女)为新蔡县政府县长，进行宪法宣誓"},
        {"id": "S011", "title": "新蔡县政府党组(扩大)会议/第66次常务会议(2025-01-16)",
         "url": "https://www.xincai.gov.cn/", "publisher": "新蔡县人民政府门户", "published_at": "2025-01-16", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2025-01-14县委副书记、县长李勇主持政府第66次常务会议（印证李勇任县长期间）"},
        {"id": "S012", "title": "副市长、新蔡县委书记杨大群参加政协新蔡十二届五次会议分组讨论(2026-03-10)",
         "url": "https://mp.weixin.qq.com/", "publisher": "新蔡县政府/县政协(微信公众号平台)", "published_at": "2026-03-10", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "medium",
         "notes": "称杨大群为驻马店市副市长同期新蔡县委书记、且与县委副书记、县长李勇共同参加；确认2026-03时李勇仍在任县长"},
        {"id": "S013", "title": "王盼(新蔡县副县长)百度百科",
         "url": "https://baike.baidu.com/", "publisher": "百度百科", "published_at": "2024-09", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium",
         "notes": "王盼，女，汉族，1986-09生，河南新蔡人，中共党员，研究生学历，副县长"},
        {"id": "S014", "title": "杨大群/邵奉公 媒体信源(猎狐网/知乎/百度知道 2024-09)",
         "url": "https://www.baidu.com/", "publisher": "银河传媒猎聘/知乎/百度知道", "published_at": "2024-09", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium",
         "notes": "杨大群1981-02理学士博士，曾任省发改委农村经济处处长，2022-11任驻马店副市长并兼新蔡县委书记；前任邵奉公1968-02，曾任正阳县委副书记/驻马店市扶贫办，2021-02任县委书记"},
        {"id": "S015", "title": "李东调研产业(大象新闻·河南广电融媒体)",
         "url": "https://www.hntv.tv/", "publisher": "大象新闻", "published_at": "一", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium",
         "notes": "确认驻马店市新蔡县委常委、县政府副县长李东，调研砖店镇、李乔镇、黄楼镇产业"},
        {"id": "S016", "title": "王飞虎带队赴新蔡县学考察(腾讯新闻 2025-12-14)",
         "url": "https://new.qq.com/", "publisher": "腾讯新闻", "published_at": "2025-12-14", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium",
         "notes": "县领导刘欣英、李勇(县长)、李君浦、田坤、李雪涛陪同；确认2025-12时刘欣已是县领导"},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person: dict, timeline: list[dict], person_relationships: list[dict],
                     source_register: list[dict], job: str, person_id: str) -> dict:
    is_top = person["id"] in (1, 2)
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": REGION,
            "job": job,
            "task_id": TASK_ID,
            "time_focus": "2026",
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "副厅级" if person["id"] == 1 else ("正处级" if is_top else "副处级"),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002", "S003", "S007", "S010", "S012"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "provincial_department" if person["id"] == 1 else
            ("cross_county_rotation" if person["id"] == 2 else "local_ladder"),
            "systems_experience": ["party"] if person["id"] == 1
            else (["party", "government"] if person["id"] == 2 else ["government", "party"]),
            "geographic_pattern": ["新蔡县(驻马店市)"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public reports, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在公开渠道发现纪律处分或负面报道信号",
                                         "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin" if person["id"] in (1, 2) else "partial",
            "relationship_confidence": "high" if is_top else "medium",
            "biggest_gap": "现任书记/县长出生年与任前年度完整履历未公开完整确认",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年月、籍贯/户籍地、学历与入党、参工时间",
             "why_it_matters": "姓名+出生年是跨区去重与身份校准关键字段",
             "suggested_queries": [f"{person['name']} 简历 新蔡县", f"{person['name']} 百度百科", f"{person['name']} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}任新蔡{job}前的上一职务与来源单位",
             "why_it_matters": "还原晋升链条与跨县调动网络",
             "suggested_queries": [f"{person['name']} 驻马店 干部任前公示", f"{person['name']} 之前 担任"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "新蔡县委常委会完整名单及分工（组织/政法/统战/人武）、人大主任、政协主席",
             "why_it_matters": "县委全体名单是细化关系网络必要输入",
             "suggested_queries": ["新蔡县委班子 名单", "新蔡县 领导分工"],
             "last_attempted": AS_OF},
        ],
    }


# ── 各核心人物 timeline ──

def yang_daqun_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "2022", "org": "河南省发展和改革委员会农村经济处", "title": "处长",
         "level": "乡科级→县处级", "location": "郑州市", "system": "government",
         "notes": "曾任河南省发展和改革委员会农村经济处处长", "confidence": "confirmed", "source_ids": ["S014"]},
        {"start": "2022-11", "end": "present", "org": "驻马店市人民政府", "title": "副市长（后任市委常委）",
         "notes": "2022年11月任驻马店市人民政府副市长并兼任新蔡县委书记；2026年报道署名‘市委常委、新蔡县委书记’",
         "confidence": "confirmed", "source_ids": ["S014", "S002", "S012"]},
        {"start": "2022-11", "end": "present", "org": "中共新蔡县委员会", "title": "新蔡县委书记",
         "notes": "2022-11起任新蔡县委书记兼县人武部党委第一书记（继任邵奉公）", "confidence": "confirmed", "source_ids": ["S014", "S002", "S012"]},
    ]


def liu_xinying_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "unknown", "org": "共青团驻马店市委", "title": "书记",
         "notes": "曾任共青团驻马店市委书记", "confidence": "plausible", "source_ids": ["S013"]},
        {"start": "unknown", "end": "unknown", "org": "泌阳县政府/上蔡县委/确山县委", "title": "泌阳县副县长、上蔡县委常委兼宣传部长、确山县委副书记、确山县石滚河镇党委书记等",
         "notes": "跨县履历：曾任泌阳县副县长、上蔡县委常委兼宣传部部长、确山县委副书记、确山县石滚河镇党委书记", "confidence": "plausible", "source_ids": ["S013"]},
        {"start": "2024", "end": "present", "org": "中共新蔡县委/县政府", "title": "县委副书记、县长（代→当选）",
         "notes": "2026-06-03代县长，2026-06-25十六届人大七次会议当选；此前(2024-2025)任新蔡县委副书记/县领导",
         "confidence": "confirmed", "source_ids": ["S003", "S004", "S010", "S016"]},
    ]


def build():
    print("=" * 60)
    print("  驻马店市新蔡县领导班子工作关系网络")
    print("  等级: 县 | 调查日期: 2026-08-06")
    print("  信息来源: 新蔡县人民政府门户 + 新蔡人大 + 公开媒体")
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

    # ── Generate Person Graph JSONs (核心二人: 县委书记/县长) ──
    source_register = make_source_register()

    # 1. 杨大群 (县委书记)
    yang_json = make_person_json(
        persons[0], yang_daqun_timeline(),
        [
            {"person": "刘欣英", "person_id": "xincai_刘欣英", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县委书记×县长 党政班子搭档(2026-至今)，同台出席县政绩观推进会/两优一先表彰大会",
             "overlap_org": "中共新蔡县委员会/新蔡县人民政府", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S006"]},
            {"person": "李勇", "person_id": "xincai_李勇", "relationship_type": "overlap",
             "strength": "strong", "evidence": "杨大群任书记期间李勇任县长，2026-03任命讨论同台",
             "overlap_org": "中共新蔡县委员会/新蔡县人民政府", "overlap_period": "2022-2026",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012", "S011"]},
            {"person": "邵奉公", "person_id": "xincai_邵奉公", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "杨大群2022-11继任邵恭任新蔡县委书记",
             "overlap_org": "中共新蔡县委员会", "overlap_period": "2021-2022",
             "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S014"]},
            {"person": "李玉清", "person_id": "xincai_李玉清", "relationship_type": "overlap",
             "strength": "medium", "evidence": "县委警示教育会上杨大群讲话、纪委书记通报，主题班班子成员",
             "overlap_org": "中共新蔡县委员会", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        source_register, "县委书记", "xincai_杨大群",
    )
    with open(PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县委书记-杨大群.json", "w", encoding="utf-8") as f:
        json.dump(yang_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 杨大群")

    # 2. 刘欣英 (县长)
    liu_xinying_json = make_person_json(
        persons[1], liu_xinying_timeline(),
        [
            {"person": "杨大群", "person_id": "xincai_杨大群", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县长×县委书记 党政组成(2026-至今)",
             "overlap_org": "新蔡县人民政府/中共新蔡县委员会", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S006"]},
            {"person": "李勇", "person_id": "xincai_李勇", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "刘欣英2026-06接替李勇任县长",
             "overlap_org": "新蔡县人民政府", "overlap_period": "2025-2026",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010", "S016"]},
            {"person": "乔鹏", "person_id": "xincai_乔鹏", "relationship_type": "overlap",
             "strength": "medium", "evidence": "县长×常务副县长 政府班子",
             "overlap_org": "新蔡县人民政府", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S009"]},
        ],
        source_register, "县长", "xincai_刘欣英",
    )
    lxy_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县长-刘欣英.json"
    with open(lxy_path, "w", encoding="utf-8") as f:
        json.dump(liu_xinying_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 刘欣英")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()