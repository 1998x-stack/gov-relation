#!/usr/bin/env python3
"""
上蔡县（驻马店市）领导班子工作关系网络 — 构建脚本

等级: 县 | 上级: 河南省驻马店市
调查日期: 2026-08-06
数据来源: 上蔡县人民政府门户 www.shangcai.gov.cn 官方"政府领导"简介与官方时政新闻
说明: 调查期间外部搜索引擎(Exa/Baidu/Bing/Google)全部受限,采用 partial-evidence 模式;
      核心领导身份(县委书记/县长)与县委/县政府班子由官方来源确认,
      传记字段以 open_questions 显式标注。
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
SLUG = "上蔡县"
TODAY = "2026-08-06"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "驻马店市"
REGION = "上蔡县"
TASK_ID = "henan_上蔡县"

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
        "name": "李超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县委书记",
        "current_org": "中共上蔡县委员会",
        "source": "https://www.shangcai.gov.cn/zwyw/zwyw/202608/t20260803_717310.html — 上蔡县政府门户时政新闻《中共上蔡县委常委2026年议军会议召开》(2026-08-03)称「上蔡县委书记、县人武部党委第一书记李超主持会议并讲话」",
        "notes": "2026-08-03官方报道确认为上蔡县委书记兼人武部党委第一书记;出生/籍贯/学历/入党时间/任前职务等公开渠道暂未获取。",
    },
    # ── 现任县长 ──
    {
        "id": 2,
        "name": "李慧阳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-03",
        "birthplace": "",
        "native_place": "",
        "education": "农业推广专业硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县县长",
        "current_org": "上蔡县人民政府",
        "source": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107072.html — 上蔡县政府门户『政府领导』官方简介(2024-08-13发布)",
        "notes": "女，汉族，1983年3月生，农业推广专业硕士，中共党员。现任中共上蔡县委副书记、县政府县长、党组书记；亦有县政府全体会议/巡河报道确认。任县长前完整履历公开渠道暂未获取。",
    },
    # ── 常务副县长 戴沅航 ──
    {
        "id": 3,
        "name": "戴沅航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "",
        "native_place": "",
        "education": "管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县委常委、常务副县长",
        "current_org": "上蔡县人民政府",
        "source": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107073.html — 上蔡县政府『政府简介』戴沅航官方领导简介",
        "notes": "男，汉族，1984年8月生，管理学硕士，中共党员。现任上蔡县委常委，县政府副县长、党组副书记。",
    },
    # ── 班泽宇 (县委宣传部长兼副县长) ──
    {
        "id": 4,
        "name": "班泽宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-01",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县委常委、宣传部部长、副县长",
        "current_org": "中共上蔡县委员会宣传部",
        "source": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107079.html — 上蔡县政府『政府简介』班泽宇官方领导简介",
        "notes": "男，汉族，1978年1月生，大学学历，中共党员。现任上蔡县委常委、宣传部部长，县政府副县长、党组成员。",
    },
    # ── 陈战晓 ──
    {
        "id": 5,
        "name": "陈战晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县人民政府副县长",
        "current_org": "上蔡县人民政府",
        "source": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107075.html — 上蔡县政府『政府简介』陈战晓官方领导简介",
        "notes": "男，汉族，1982年12月生，研究生学历，中共党员。现任上蔡县人民政府副县长、党组成员。",
    },
    # ── 刘军（副县长兼公安局长） ──
    {
        "id": 6,
        "name": "刘军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "",
        "native_place": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县人民政府副县长、县公安局局长",
        "current_org": "上蔡县公安局",
        "source": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107077.html — 上蔡县政府『政府简介』刘军官方领导简介",
        "notes": "男，汉族，1973年12月生，本科学历，中共党员。现任上蔡县人民政府副县长、党组成员，县公安局党委书记、局长。",
    },
    # ── 范少杰 ──
    {
        "id": 7,
        "name": "范少杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-05",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历+工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县人民政府副县长",
        "current_org": "上蔡县人民政府",
        "source": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107078.html — 上蔡县政府『政府简介』范少杰官方领导简介",
        "notes": "男，汉族，1980年5月生，大学学历，工商管理硕士，中共党员。现任上蔡县人民政府副县长、党组成员。",
    },
    # ── 王昊 ──
    {
        "id": 8,
        "name": "王昊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-10",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县人民政府副县长",
        "current_org": "上蔡县人民政府",
        "source": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107081.html — 上蔡县政府『政府简介』王昊官方领导简介",
        "notes": "男，汉族，1986年10月生，研究生学历，中共党员。现任上蔡县人民政府副县长、党组成员。",
    },
    # ── 张海洋（纪委书记、监委代理主任） ──
    {
        "id": 9,
        "name": "张海洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上蔡县委常委、纪委书记、监委代理主任",
        "current_org": "中共上蔡县纪律检查委员会",
        "source": "https://www.shangcai.gov.cn/zwyw/zwyw/202607/t20260715_711959.html — 上蔡县政府门户《上蔡县政府全体会议暨廉政工作会议召开》(2026-07-15)",
        "notes": "2026-07-15政府全会报道称「县委常委、县纪委书记、县监委代理主任张海洋应邀出席会议」;出生/籍贯/学历/正式监委主任转正时间待查。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共上蔡县委员会", "type": "党委", "level": "县处级", "parent": "中共驻马店市委员会", "location": "河南省驻马店市上蔡县"},
    {"id": 2, "name": "上蔡县人民政府", "type": "政府", "level": "县处级", "parent": "驻马店市人民政府", "location": "河南省驻马店市上蔡县"},
    {"id": 3, "name": "中共上蔡县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共上蔡县委员会", "location": "河南省驻马店市上蔡县"},
    {"id": 4, "name": "上蔡县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共上蔡县委员会", "location": "河南省驻马店市上蔡县"},
    {"id": 5, "name": "上蔡县公安局", "type": "政府", "level": "县处级", "parent": "上蔡县人民政府", "location": "河南省驻马店市上蔡县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 李超
    {"person_id": 1, "org_id": 1, "title": "上蔡县委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "2026-08-03官方确认为县委书记；兼任县人武部党委第一书记；任职起始与前任待查"},
    # 李慧阳
    {"person_id": 2, "org_id": 1, "title": "上蔡县委副书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "官方简介与新闻确认兼任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "上蔡县长、党组书记、总河长", "start": "unknown", "end": "present", "rank": "正处级", "note": "2024-08官方领导简介确认；主持县政府全面工作"},
    # 戴沅航
    {"person_id": 3, "org_id": 1, "title": "上蔡县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方简介+政府全会确认（常务副县长分管）"},
    {"person_id": 3, "org_id": 2, "title": "上蔡县委常委、常务副县长、党组副书记", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-07-15政府全会主持"},
    # 班泽宇
    {"person_id": 4, "org_id": 1, "title": "上蔡县委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方简介确认"},
    {"person_id": 4, "org_id": 2, "title": "上蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "兼任宣传部长与副县长"},
    # 陈战晓
    {"person_id": 5, "org_id": 2, "title": "上蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方简介确认"},
    # 刘军
    {"person_id": 6, "org_id": 2, "title": "上蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方简介确认"},
    {"person_id": 6, "org_id": 5, "title": "上蔡县公安局党委书记、局长", "start": "unknown", "end": "present", "rank": "副处级", "note": "兼任县公安局局长"},
    # 范少杰
    {"person_id": 7, "org_id": 2, "title": "上蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方简介确认"},
    # 王昊
    {"person_id": 8, "org_id": 2, "title": "上蔡县人民政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方简介确认；2026-07-30陪同县长巡河"},
    # 张海洋
    {"person_id": 9, "org_id": 1, "title": "上蔡县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-07-15政府全会出席名单"},
    {"person_id": 9, "org_id": 4, "title": "上蔡县纪委书记、县监委代理主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "廉政工作会议应县纪委书记出席"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 李超 ↔ 李慧阳: 县委书记×县长 党政搭档 (confirmed)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "李超任县委书记、李慧阳任县委副书记兼县长，构成党政班子搭档；共同出席议军会议/县委常委会", "overlap_org": "中共上蔡县委员会/上蔡县人民政府", "overlap_period": "2026-至今"},
    # 李慧阳 ↔ 戴沅航: 县长×常务副县长 政府班子 (confirmed, 政府全会戴主持李讲话)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "李慧阳(县长)与戴沅航(常务副县长)在政府全体会议上同台，戴主持会议李讲话", "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今"},
    # 李慧阳 ↔ 县政府副县(班/陈/刘/范/王): 政府班子同僚 (confirmed, 政府全会共同出席)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "政府全体会议共同出席(宣传兼副县)", "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "政府全体会议共同出席", "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "政府全体会议共同出席(公安局长)", "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "政府全体会议共同出席", "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "政府全体会议共同出席，且2026-07-30共同巡河", "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今"},
    # 张海洋(纪委书记) ↔ 李超/李慧阳: 班子成员/廉政会议 (confirmed)
    {"person_a": 9, "person_b": 1, "type": "overlap", "context": "县委常委班子主要成员", "overlap_org": "中共上蔡县委员会", "overlap_period": "2026-至今"},
    {"person_a": 9, "person_b": 2, "type": "overlap", "context": "廉政工作会议上李慧阳作讲话、张海洋出席(主体责任×监督责任)", "overlap_org": "中共上蔡县委员会", "overlap_period": "2026-至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "中共上蔡县委常委2026年议军会议召开(2026-08-03)",
         "url": "https://www.shangcai.gov.cn/zwyw/zwyw/202608/t20260803_717310.html",
         "publisher": "上蔡县人民政府门户网站(来源:上蔡发布)", "published_at": "2026-08-03", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认李超为『上蔡县委书记、县人武部党委第一书记』；列明县委领导名单"},
        {"id": "S002", "title": "李慧阳领导简介（政府简介>政府领导，2024-08-13版）",
         "url": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107072.html",
         "publisher": "上蔡县人民政府门户网站", "published_at": "2024-08-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "官方确认李慧阳：女，汉族，1983-03生，农业推广专业硕士，中共党员，县委副书记、县长、党组书记"},
        {"id": "S003", "title": "戴沅航官方领导简介(2024-08-13)",
         "url": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107073.html",
         "publisher": "上蔡县人民政府门户网站", "published_at": "2024-08-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "戴沅航：男，汉族，1984-08，管理学硕士，中共党员，县委常委、常务副县长、党组副书记"},
        {"id": "S004", "title": "陈战晓/简介(2024-08-13)",
         "url": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107075.html",
         "publisher": "上蔡县人民政府门户网站", "published_at": "2024-08-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "陈战晓：男，汉族，1982-12，研究生，副县长、党组成员"},
        {"id": "S005", "title": "刘军/简介(2024-08-13)",
         "url": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107077.html",
         "publisher": "上蔡县人民政府门户网站", "published_at": "2024-08-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "刘军：男，汉族，1973-12，本科，副县长、党组成员，县公安局党委书记、局长"},
        {"id": "S006", "title": "范少杰/简介(2024-08-13)",
         "url": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107078.html",
         "publisher": "上蔡县人民政府门户网站", "published_at": "2024-08-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "范少杰：男，汉族，1980-05，大学+工商管理硕士，副县长、党组成员"},
        {"id": "S007", "title": "班泽宇/简介(2024-08-13)",
         "url": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107079.html",
         "publisher": "上蔡县人民政府门户网站", "published_at": "2024-08-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "班泽宇：男，汉族，1978-01，大学学历，县委常委、宣传部长兼副县长"},
        {"id": "S008", "title": "王昊/简介(2024-08-13)",
         "url": "https://www.shangcai.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107081.html",
         "publisher": "上蔡县人民政府门户网站", "published_at": "2024-08-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "王昊：男，汉族，1986-10，研究生，副县长、党组成员"},
        {"id": "S009", "title": "上蔡县政府全体会议暨廉政工作会议召开(2026-07-15)",
         "url": "https://www.shangcai.gov.cn/zwyw/zwyw/202607/t20260715_711959.html",
         "publisher": "上蔡县人民政府门户网站(来源:上蔡发布)", "published_at": "2026-07-15", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认县政府班子:李慧阳(县长)、戴沅航(常务)、班泽宇(宣传部副县)、陈战晓/刘军/范少杰/王昊(副县)、张海洋(纪委书记、监委代主任)"},
        {"id": "S010", "title": "李慧阳开展巡河并调研防汛备汛工作(2026-07-30)",
         "url": "https://www.shangcai.gov.cn/zwyw/zwyw/202607/t20260730_716350.html",
         "publisher": "上蔡县人民政府门户网站(来源:上蔡发布)", "published_at": "2026-07-30", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "李慧阳为县委副书记、县长、县总河长；王昊陪同调研"},
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
            "administrative_rank": "正处级" if is_top else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003", "S009", "S010"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"] if person["id"] == 1
            else (["party", "government"] if person["id"] == 2 else ["government", "party"]),
            "geographic_pattern": ["上蔡县(驻马店市)"],
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
            "career_completeness": "thin" if person["id"] in (1, 9) else "partial",
            "relationship_confidence": "high" if is_top else "medium",
            "biggest_gap": "核心领导出生年份/籍贯/学历/入党时间及任现职前完整履历未公开确认",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年月、籍贯、学历/专业、入党与参工时间",
             "why_it_matters": "姓名+出生年是跨区去重与身份校准的关键字段",
             "suggested_queries": [f"{person['name']} 简历 上蔡", f"{person['name']} 百度百科", f"{person['name']} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}任上蔡{job}前的上一职与来源单位",
             "why_it_matters": "还原晋升链条与跨县调动网络",
             "suggested_queries": [f"{person['name']} 驻马店 干部 任前公示", f"{person['name']} 之前 担任"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "上蔡县县委领导班子其他常委分工（组织/政法/统战/人武）名单",
             "why_it_matters": "县委常委会全体名单与分工是细化关系网络的必要输入",
             "suggested_queries": ["上蔡县 领导分工", "上蔡县委班子 名单"],
             "last_attempted": AS_OF},
        ],
    }


# ── 各核心人物 timeline 与 relationships ──

def li_chao_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "present", "org": "履历缺口", "title": "",
         "notes": "李超任上蔡县委书记前的完整履历（出生年度等）公开渠道暂未获取；2026-08-03官方报道确认其任县委书记兼人武部第一书记",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "中共上蔡县委员会", "title": "上蔡县委书记",
         "notes": "2026-08-03议军会议署名「上蔡县委书记、县人武部党委第一书记李超主持会议」确认",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]


def li_huiyang_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "present", "org": "履历缺口", "title": "",
         "notes": "李慧阳任上蔡县长前完整履历未公开（来电单位/任职起始）",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "上蔡县人民政府", "title": "县长、党组书记、总河长",
         "notes": "2024-08-13官方领导简介确认；2026-07主持县政府全体会议并布置工作",
         "confidence": "confirmed", "source_ids": ["S002", "S009", "S010"]},
        {"start": "unknown", "end": "present", "org": "中共上蔡县委员会", "title": "县委副书记",
         "notes": "官方简介与新闻报道均确认兼任县委副书记",
         "confidence": "confirmed", "source_ids": ["S002", "S010"]},
    ]


def build():
    print("=" * 60)
    print("  驻马店市上蔡县领导班子工作关系网络")
    print("  等级: 县 | 调查日期: 2026-08-06")
    print("  信息来源: 上蔡县人民政府门户网站")
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

    # 1. 李超 (县委书记)
    lichao_json = make_person_json(
        persons[0], li_chao_timeline(),
        [
            {"person": "李慧阳", "person_id": "shangcai_李慧阳", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县委书记×县长(县委副书记)党政班子搭档(2026-至今)",
             "overlap_org": "中共上蔡县委员会/上蔡县人民政府", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S009"]},
            {"person": "张海洋", "person_id": "shangcai_张海洋", "relationship_type": "overlap",
             "strength": "medium", "evidence": "同届县委常委会班子成员",
             "overlap_org": "中共上蔡县委员会", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        source_register, "县委书记", "shangcai_李超",
    )
    with open(PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县委书记-李超.json", "w", encoding="utf-8") as f:
        json.dump(lichao_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 李超")

    # 2. 李慧阳 (县长)
    lihuiyang_json = make_person_json(
        persons[1], li_huiyang_timeline(),
        [
            {"person": "李超", "person_id": "shangcai_李超", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县长×县委书记 党政搭档",
             "overlap_org": "上蔡县人民政府/中共上蔡县委员会", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S009"]},
            {"person": "戴沅航", "person_id": "shangcai_戴沅航", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县长×常务副县同台；常务副县主持政府全会",
             "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S009", "S003"]},
            {"person": "王昊", "person_id": "shangcai_王昊", "relationship_type": "overlap",
             "strength": "medium", "evidence": "县政府班子同僚，2026-07-30共同巡河",
             "overlap_org": "上蔡县人民政府", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
        ],
        source_register, "县长", "shangcai_李慧阳",
    )
    lhy_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县长-李慧阳.json"
    with open(lhy_path, "w", encoding="utf-8") as f:
        json.dump(lihuiyang_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 李慧阳")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()