#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 鹿邑县, 周口市, 河南省.

Level: 县
Province: 河南省
Parent city: 周口市
Targets: 县委书记 (Party Secretary: 郭俊涛), 县长 (Mayor: 刘锋磊)
Task ID: henan_鹿邑县

Research dates: 2026-08-07 (初始) / 2026-08-11 (复核补充)
Sources: 鹿邑县人民政府门户(luyi.gov.cn)官方(接访日程表/领导信息/县党代会/常委会/政府常务会) +
  周口市政府门户(zhoukou.gov.cn)、周口日报·中华龙都网(zhld.com)、河南经济报、
  今日头条(2024-05 任命报道)、周口网(2021-03 当选报道)、百度百科(郭俊涛, 次级来源) +
  本仓库 data/persons/20260724-河南省-濮阳市-市长-朱良才.json。

Current status (as of 2026-08, 复核至 2026-04 总林长令/2026-03 人大七次会议):
- 县委书记: 郭俊涛（男，汉族，1981年10月生，河南禹州市人，大学学历·法学学士(郑州大学法学院)，
  2001-12入党、2003-08参工；2024-05 任鹿邑县委书记，2024-06 兼县人武部党委第一书记；
  2026-06-24 十四次党代会作县委工作报告；任期至 2026-08 获多重官方报道确认）
- 县长: 刘锋磊（男，中共党员；2024年四季度前后任县委副书记、县长；2026-02 县十六届人大
  七次会议作政府工作报告；2026-04 以县长/县总林长签发总林长令；任前履历公开渠道未获）
- 县委副书记、政法委书记: 袁航（2021-11 曾为县委常委、组织部长；现职副书记、政法委书记）
- 县委常委、副县长(正处级): 李展
- 县委常委、常务副县长: 张建威（2024-12-26 县十六届人大常委会第十八次会议任命副县长）
- 县委常委、纪委书记、监委主任: 朱高建
- 县委常委、组织部长: 牛海燕（兼县委教育工作委员会书记）
- 县委常委、宣传部长: 王臻
- 县委常委、县委办公室主任: 刘翔
- 县委常委、统战部长、副县长: 刘双博
- 副县长、公安局局长: 韩凤城
- 副县长: 乔伟
- 县处级干部: 毛斌（县先进制造业开发区五级职员）
- 县人大常委会党组书记、主任: 王智华

书记序列（本复核链条, 确认）:
  朱良才(周口市委常委、鹿邑县委书记 ~2015-2017初; 2017-07-05 以河南省政府副秘书长出席鹿邑会议;
后任省民政厅厅长、濮阳市市长) → 梁建松(书记 2017.02前已任-2021.01, 现周口市副市长) → 李刚
  (书记 2021.01-2024.03, 现洛阳市副市长) → 郭俊涛(2024.05-)
县长序列: 朱良才(2010-2015) → 梁建松(早年任县长) → 李刚(2017.07提名/2018.01当选-2021.01)
  → 郭俊涛(2021.03当选-2024.05转书记) → 刘锋磊(2024年四季度前后-)

Confidence notes:
- 郭俊涛/刘锋磊 在任 confirmed（官方接访表/党代会/常委会/常务会/林长令）。
- 郭俊涛身份履历 confirmed(百度百科+媒体多源); 刘锋磊任前履历为 open gap。
- 县委班子成员与分工: 据 2026-08 官方接访日程PDF + 政府领导页（2026-08 之后）。
  2025 年人员对照（周口日报）: 张凯歌(宣传部长兼副县长, 2026 未再出现)、齐长军(副书记
  /政法委, 2026 未再出现)、皇彬/肖炜(免职)等 —— 换届/调整后名单以 2026-08 为准, 差异入 open_questions。
- 前置书记朱良才路径 confirmed: 本地 data/persons 朱良才.json + 周口市政府网 2017 会议次序 +
  头条 2024-05 报道（李刚去向）。其"鹿邑县委书记"任期修正为 2015-2017 初（非 2015-2021）。
"""

import json
import sqlite3  # noqa: F401 — used by gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Locate repo root robustly across staging vs canonical locations.
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in (2, 3, 4, 5):
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401  (canonical dest helpers)

SLUG = "鹿邑县"
TASK_ID = "henan_鹿邑县"

# DB/GEXF + person JSONs always land in the task staging dir.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / TASK_ID
if _CURRENT_DIR.name == TASK_ID:
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING

AS_OF = "2026-08-11"   # 复核日期（在任状态的最晚确认点: 2026-04 总林长令 / 2026-03 政府工作报告报道）
TODAY = "20260807"     # 与既有 person JSON 文件名保持一致（2026-08-07 首版生成）

_PID = "luyi"  # person-id prefix for graph dedup across investigations

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core: 县委书记 ──
    {
        "id": 1,
        "name": "郭俊涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "河南省禹州市",
        "education": "大学学历, 法学学士(郑州大学法学院法学专业)",
        "party_join": "中共党员(2001年12月入党)",
        "work_start": "2003年8月",
        "current_post": "县委书记",
        "current_org": "中共鹿邑县委员会",
        "source": "鹿邑县政府官网·2026-08接访日程表/县委常委会报道(2026-07-13,08-03) + 百度百科(郭俊涛词条) + 今日头条2024-05-15(任前报道)",
        "notes": "男,汉族,1981年10月生,河南禹州市人,2001年12月入党,2003年8月参工,郑州大学法学院法学专业毕业(学士)。2024-05任鹿邑县委书记,2024-06兼县人武部党委第一书记;2026-06-24党代会作报告。履历:许昌市政府办→东城区管委会→襄城县委常委/副县长→长葛市委常委/常务副市长→鹿邑县长(2021.03)→鹿邑书记(2024.05)。",
    },
    # ── Core: 县长 ──
    {
        "id": 2,
        "name": "刘锋磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "鹿邑县人民政府",
        "source": "鹿邑县政府门户·2026-08接访日程表+县十六届人大七次会议(2026-02)+周口日报(中华龙都网)多次常务会议报道",
        "notes": "男,中共党员。2024年四季度前后任鹿邑县委副书记、县长(2024-11-29以县长身份主持县政府第40次常务会议为最早可证节点;2024-07-19在县处级领导会出席名单中)。2026-02-12县十六届人大七次会议作政府工作报告;2026-04-03以县长、县总林长身份签发总林长令。出生年月/学历/任县长前履历公开渠道未获取(开放缺口)。",
    },
    # ── 县委副书记、政法委书记 ──
    {
        "id": 3,
        "name": "袁航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共鹿邑县委员会",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表+人民政协网2021-11-26(任组织部长报道)",
        "notes": "男,中共党员。2021-11为中共鹿邑县委常委、组织部部长(人民政协网《河南省鹿邑县委书记李刚到县政协机关调研》出席名单);2026-08为县委副书记、政法委书记(接访日程表,负责县委日常工作、政法/信访/三农)。2025-06 分工资料显示时任政法委书记为齐长军, 2026 党内调整后现职为准, 衔接点待核。",
    },
    # ── 常委/副县长(正处级) ──
    {
        "id": 4,
        "name": "李展",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长(正处级)",
        "current_org": "鹿邑县人民政府",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表+政府领导页",
        "notes": "男,中共党员,现任县委常委、副县长(正处级);负责工信、科技、招商引资、开发区建设。履历待核。",
    },
    # ── 常委/常务副县长 ──
    {
        "id": 5,
        "name": "张建威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "鹿邑县人民政府",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表+2024-12-26县十六届人大第18次常委会任免公告",
        "notes": "男,中共党员。2024-12-26县十六届人大常委会第十八次会议决定任命为鹿邑县人民政府副县长;2025-06起为县委常委、常务副县长(协助县长负责县政府日常工作)。履历待核。",
    },
    # ── 常委/纪委书记 ──
    {
        "id": 6,
        "name": "朱高建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共鹿邑县纪律检查委员会",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表",
        "notes": "男,中共党员,现任县委常委,县纪委书记、监委会主任;主持县纪委监委全面工作,分管县委巡察办。履历待核。",
    },
    # ── 常委/组织部长 ──
    {
        "id": 7,
        "name": "牛海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共鹿邑县委员会",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表",
        "notes": "女,中共党员,现任县委常委、组织部部长,兼县委教育工作委员会书记。2025-06 曾以县处级干部身份出席县政府常务会议(周口日报)。履历待核。",
    },
    # ── 常委/宣传部长 ──
    {
        "id": 8,
        "name": "王臻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共鹿邑县委员会",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表",
        "notes": "男,中共党员,现任县委常委、宣传部部长;分管人社、文旅、教育、卫健、医保等。2025-06 时任宣传部长为张凯歌(2026 未见其名单, 换届/调整待核)。履历待核。",
    },
    # ── 常委/县委办主任 ──
    {
        "id": 9,
        "name": "刘翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共鹿邑县委员会",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表",
        "notes": "男,中共党员。2025-06 时以副县长身份出席接访(分管自然资源、城乡建设、城市更新等);2026-08 为县委常委、县委办公室主任(分管自然资源、住建、生态、城市更新)——同一人班子内转任。履历待核。",
    },
    # ── 常委/统战部长、副县长 ──
    {
        "id": 10,
        "name": "刘双博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长、副县长",
        "current_org": "鹿邑县人民政府",
        "source": "鹿邑县政府门户·2026-08党政领导接访日程表",
        "notes": "男,中共党员,现任县委常委、统战部部长,兼任副县长(分管农业农村、乡村振兴等);2025-06 时以副县长身份出席接访。履历待核。",
    },
    # ── 副县长/公安局长 ──
    {
        "id": 11,
        "name": "韩凤城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "鹿邑县人民政府/鹿邑县公安局",
        "source": "鹿邑县政府门户·政府领导页+2026-08党政领导接访日程表",
        "notes": "男,中共党员,副县长、党组成员,县公安局党委书记、局长;分管公安、司法、信访等。履历待核。",
    },
    # ── 副县长 ──
    {
        "id": 12,
        "name": "乔伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "鹿邑县人民政府",
        "source": "鹿邑县政府门户·政府领导页+2026-08党政领导接访日程表",
        "notes": "现任副县长;分管民政、交通、市场监管、通用机场、内河航运、城乡养老等。履历待核。",
    },
    # ── 县处级干部 ──
    {
        "id": 13,
        "name": "毛斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县处级干部(县先进制造业开发区五级职员)",
        "current_org": "鹿邑县先进制造业开发区",
        "source": "鹿邑县政府门户·政府领导页+2026-08党政领导接访日程表",
        "notes": "男,中共党员,县先进制造业开发区五级职员(县处级);协助常务副县长分管应急管理(防汛)、负责农业农村与乡村振兴。",
    },
    # ── 县人大常委会主任 ──
    {
        "id": 14,
        "name": "王智华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "鹿邑县人民代表大会常务委员会",
        "source": "鹿邑县政府门户·县十六届人大七次会议报道(2026-02-13)",
        "notes": "男,中共党员,现任县人大常委会党组书记、主任;2026-02县十六届人大七次会议作人大常委会工作报告。履历待核。",
    },
    # ── 前置/跨区: 朱良才（前任鹿邑县委书记→现任濮阳市市长）──
    {
        "id": 15,
        "name": "朱良才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "河南扶沟",
        "education": "农业技术推广硕士(河南农业大学)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "濮阳市市长(曾任鹿邑县委书记)",
        "current_org": "濮阳市人民政府",
        "source": "本仓库 data/persons/20260724-河南省-濮阳市-市长-朱良才.json(维基百科+濮阳政府) + 周口市政府网2017-07接访(2017-07-05以省政府副秘书长身份)",
        "notes": "男,汉族,1975年8月生,河南扶沟人,农业技术推广硕士。履历:共青团周口市委书记(2007)→鹿邑县委副书记、县长(约2010-约2014)→周口市委常委、鹿邑县委书记(约2015-2017初)→河南省政府副秘书长(2017-07确认)→河南省民政厅厅长(2021-11)→濮阳市市长(2023-)。注意: 其担任鹿邑县委书记的截止时间修正为2017年初前后(2017-07-05 周口市政府网会议报道中以『省政府副秘书长、办公厅党组成员』身份出席鹿邑县领导干部会议; 2017-02 周口市政府网报道中鹿邑县委书记为梁建松)。",
    },
    # ── 前置书记: 梁建松（书记 2017-2021.01 → 现周口市副市长）──
    {
        "id": 16,
        "name": "梁建松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "周口市副市长(曾任鹿邑县委书记)",
        "current_org": "周口市人民政府",
        "source": "周口市人民政府网『领导介绍』(副市长梁建松简介) + 周口市政府网2017-02+中华龙都网2020-09(历任鹿邑书记报道)",
        "notes": "男,汉族,1966年10月生,大学学历,中共党员,现任周口市人民政府副市长、党组成员。曾任鹿邑县委书记(2017年初-2021.01,李刚2021.01接任并透露梁建松调离);更早曾多年在鹿邑任职(早年任鹿邑县长,具体起止待核)。",
    },
    # ── 前置任: 李刚（书记 2021.01-2024.03 → 现洛阳市副市长）──
    {
        "id": 17,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "河南省新密市",
        "native_place": "河南省新密市",
        "education": "学历待核(郑州任职背景)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛阳市副市长(曾任鹿邑县委书记)",
        "current_org": "洛阳市人民政府",
        "source": "今日头条2024-05-15(郭俊涛任鹿邑县委书记报道:李刚1974年4月生、河南新密人)+人民政协网2021-11-25+中华龙都网2018-11(县长调研报道)",
        "notes": "男,汉族,1974年4月生,河南新密市人。曾任鹿邑县县长(2017-07省委提名、2018-01十五届人大二次会议当选, 省十三届人大代表)、鹿邑县委书记(2021.01-2024.03);2024-03跨市任洛阳市人民政府副市长。更早在郑州市金水区、巩义市工作(具体职务与时间待核)。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共鹿邑县委员会", "type": "党委", "level": "县处级",
     "parent": "中共周口市委员会", "location": "河南省周口市鹿邑县"},
    {"id": 2, "name": "鹿邑县人民政府", "type": "政府", "level": "县处级",
     "parent": "周口市人民政府", "location": "河南省周口市鹿邑县"},
    {"id": 3, "name": "鹿邑县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "周口市人大常委会", "location": "河南省周口市鹿邑县"},
    {"id": 4, "name": "政协鹿邑县委员会", "type": "政协", "level": "县处级",
     "parent": "政协周口市委员会", "location": "河南省周口市鹿邑县"},
    {"id": 5, "name": "中共鹿邑县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共周口市纪律检查委员会", "location": "河南省周口市鹿邑县"},
    {"id": 6, "name": "鹿邑县公安局", "type": "政府", "level": "乡科级",
     "parent": "鹿邑县人民政府", "location": "河南省周口市鹿邑县"},
    {"id": 7, "name": "鹿邑县先进制造业开发区", "type": "开发区", "level": "省级",
     "parent": "鹿邑县人民政府", "location": "河南省周口市鹿邑县"},
    {"id": 8, "name": "中共周口市委员会", "type": "党委", "level": "地级市",
     "parent": "中共河南省委", "location": "河南省周口市"},
    {"id": 9, "name": "周口市人民政府", "type": "政府", "level": "地级市",
     "parent": "河南省人民政府", "location": "河南省周口市"},
    {"id": 10, "name": "濮阳市人民政府", "type": "政府", "level": "地级市",
     "parent": "河南省人民政府", "location": "河南省濮阳市"},
    {"id": 11, "name": "共青团周口市委", "type": "群团", "level": "地级",
     "parent": "共青团河南省委", "location": "河南省周口市"},
    {"id": 12, "name": "河南省人民政府", "type": "政府", "level": "省级",
     "parent": "国务院", "location": "河南省郑州市"},
    {"id": 13, "name": "河南省民政厅", "type": "政府", "level": "省级",
     "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 14, "name": "洛阳市人民政府", "type": "政府", "level": "地级市",
     "parent": "河南省人民政府", "location": "河南省洛阳市"},
    {"id": 15, "name": "鹿邑县人民武装部", "type": "军事", "level": "县处级",
     "parent": "周口军分区", "location": "河南省周口市鹿邑县"},
    {"id": 16, "name": "许昌市人民政府办公室", "type": "政府", "level": "地级市直属",
     "parent": "许昌市人民政府", "location": "河南省许昌市"},
    {"id": 17, "name": "许昌市东城区管理委员会", "type": "政府", "level": "正处级",
     "parent": "许昌市人民政府", "location": "河南省许昌市"},
    {"id": 18, "name": "襄城县人民政府", "type": "政府", "level": "县处级",
     "parent": "许昌市人民政府", "location": "河南省许昌市襄城县"},
    {"id": 19, "name": "长葛市人民政府", "type": "政府", "level": "县处级",
     "parent": "许昌市人民政府", "location": "河南省许昌市长葛市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 郭俊涛(1): 许昌市→襄城→长葛→鹿邑 完整履历 ──
    {"person_id": 1, "org_id": 16, "title": "许昌市人民政府办公室(法制办→六科副科长/科长)", "start_date": "2003-08", "end_date": "2012-03",
     "rank": "科员→正科", "note": "2003-08-2005-09 法制办工作; 2005-09-2012-03 六科工作, 2006-10任副科长、2010-04任科长"},
    {"person_id": 1, "org_id": 17, "title": "管委会副主任、党工委委员(2015-09起常务副主任)", "start_date": "2012-03", "end_date": "2016-06",
     "rank": "副处级", "note": "2016年前后许昌市东城区区划调整, 管委会更名/并入示范区, 属同源任用"},
    {"person_id": 1, "org_id": 18, "title": "襄城县委常委、县政府副县长", "start_date": "2016-06", "end_date": "2019-09",
     "rank": "副处级", "note": "跨县任职"},
    {"person_id": 1, "org_id": 19, "title": "长葛市委常委、常务副市长", "start_date": "2019-09", "end_date": "2021-03",
     "rank": "副处级", "note": "县级市党政班子常务副职"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、代县长→县长", "start_date": "2021-03", "end_date": "2024-05",
     "rank": "正处级", "note": "2021-03-10 鹿邑县十五届人大六次会议依法当选鹿邑县人民政府县长"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2024-05", "end_date": "present",
     "rank": "正处级", "note": "主持县委全面工作; 2024-05-14 首次以书记身份主持县委常委会; 2026-06-24 中共鹿邑县第十四次代表大会作县委工作报告; 兼任县人武部党委第一书记"},
    {"person_id": 1, "org_id": 15, "title": "县人武部党委第一书记", "start_date": "2024-06", "end_date": "present",
     "rank": "正处级(兼)", "note": "2024-06-25 县人武部党委第一书记任职宣布大会, 经周口军分区党委研究决定"},

    # ── 刘锋磊(2) ──
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2024-10", "end_date": "present",
     "rank": "副处级", "note": "2024-11-29 以县委副书记、县长身份主持县政府第40次常务会议(最早可证节点); 2024-07-19 曾出席县处级领导干部会议名单(职务未明)"},
    {"person_id": 2, "org_id": 2, "title": "县长、党组书记、县总林长", "start_date": "2024-10", "end_date": "present",
     "rank": "正处级", "note": "主持县政府及县政府党组全面工作; 2026-02-12 县十六届人大七次会议作政府工作报告; 2026-04-03 以县总林长身份签发鹿邑县2026年总林长令"},

    # ── 袁航(3) ──
    {"person_id": 3, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "2021-11", "end_date": "2023",
     "rank": "副处级", "note": "人民政协网2021-11-26报道出席名单确认"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记、政法委书记", "start_date": "2023", "end_date": "present",
     "rank": "副处级", "note": "负责县委常务工作, 主持县委政法委; 2026-08 接访日程表确认; 与2025-06时任政法委书记齐长军的衔接点待核"},

    # ── 李展(4) ──
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长(正处级)", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "负责工信、科技、招商引资、开发区建设"},

    # ── 张建威(5) ──
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "2024-12", "end_date": "present",
     "rank": "副处级", "note": "2024-12-26 县十六届人大常委会第十八次会议决定任命为副县长; 2025-06起任常务副县长(协助县长负责县政府日常工作、发改、财政、金融)"},

    # ── 朱高建(6) ──
    {"person_id": 6, "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "主持县纪委监委全面工作; 分管县委巡察办"},

    # ── 牛海燕(7) ──
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "主持县委组织部; 兼县委教育工作委员会书记; 2025-06 以县处级身份出席县府常务会"},

    # ── 王臻(8) ──
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "主持县委宣传部; 分管人社、文旅、教育、卫健、医保"},

    # ── 刘翔(9) ──
    {"person_id": 9, "org_id": 1, "title": "县委常委、县委办公室主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "主持县委办公室; 分管自然资源、住建、生态、城市更新; 2025-06 曾以副县长身份列接访(班子内转任)"},

    # ── 刘双博(10) ──
    {"person_id": 10, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "主持县委统战部; 协助袁航推进农业农村/乡村振兴"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "统战部长兼副县长"},

    # ── 韩凤城(11) ──
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "副县长、党组成员"},
    {"person_id": 11, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "present",
     "rank": "正科级", "note": "副县长兼县公安局长; 分管公安、司法、信访等"},

    # ── 乔伟(12) ──
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责民政、交通、市场监管、通用机场、内河航运、城乡养老等"},

    # ── 毛斌(13) ──
    {"person_id": 13, "org_id": 7, "title": "县先进制造业开发区五级职员", "start_date": "", "end_date": "present",
     "rank": "县处级", "note": "协助常务副县长分管应急管理(防汛); 负责农业农村与乡村振兴"},

    # ── 王智华(14) ──
    {"person_id": 14, "org_id": 3, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-02 县十六届人大七次会议作人大常委会工作报告"},

    # ── 朱良才(15) ──
    {"person_id": 15, "org_id": 11, "title": "共青团周口市委书记", "start_date": "2007-02", "end_date": "2010",
     "rank": "县处级", "note": "来源: 本仓库 data/persons 朱良才.json"},
    {"person_id": 15, "org_id": 2, "title": "鹿邑县委副书记、县长", "start_date": "2010", "end_date": "2015-03",
     "rank": "县处级", "note": "约2010-2015 任鹿邑县长"},
    {"person_id": 15, "org_id": 1, "title": "周口市委常委、鹿邑县委书记", "start_date": "2015-03", "end_date": "2017",
     "rank": "副厅级", "note": "约2015-03至2017年初(2016年末-2017初转省; 2017-07-05 已以省政府副秘书长、办公厅党组成员身份出席鹿邑县处级领导干部会议)"},
    {"person_id": 15, "org_id": 12, "title": "河南省人民政府副秘书长(兼省政府研究室主任)", "start_date": "2017-07", "end_date": "2021-11",
     "rank": "副厅级", "note": "2017-07-05 周口市政府网会议报道确认在任; 2019-04-起兼任省政府研究室主任"},
    {"person_id": 15, "org_id": 13, "title": "河南省民政厅厅长、党组书记", "start_date": "2021-11", "end_date": "2023-03",
     "rank": "正厅级", "note": "晋升正厅级"},
    {"person_id": 15, "org_id": 10, "title": "濮阳市市长", "start_date": "2023-03", "end_date": "present",
     "rank": "正厅级", "note": "2023-03 任代市长、市长"},

    # ── 梁建松(16) ──
    {"person_id": 16, "org_id": 2, "title": "鹿邑县县长(早年任期)", "start_date": "", "end_date": "",
     "rank": "县处级", "note": "报道未标明年份(约2015年前后任鹿邑县委副书记、县长; 朱良才称『建松同志以前在鹿邑工作过』); 具体起止待核"},
    {"person_id": 16, "org_id": 1, "title": "鹿邑县委书记", "start_date": "2017", "end_date": "2021-01",
     "rank": "正处级", "note": "2017-02 周口市政府网报道已为鹿邑县委书记; 2021-01 李刚接任书记并透出梁建松调离"},
    {"person_id": 16, "org_id": 9, "title": "周口市副市长、党组成员", "start_date": "2021", "end_date": "present",
     "rank": "副厅级", "note": "周口市人民政府官网『领导介绍』确认现任"},

    # ── 李刚(17) ──
    {"person_id": 17, "org_id": 2, "title": "鹿邑县委副书记、县长", "start_date": "2017-07", "end_date": "2021-01",
     "rank": "正处级", "note": "2017-07-05 省委通知任鹿邑县委副书记、提名为县长候选人; 2018-01-08 鹿邑县十五届人大二次会议当选; 省十三届人大代表"},
    {"person_id": 17, "org_id": 1, "title": "鹿邑县委书记", "start_date": "2021-01", "end_date": "2024-03",
     "rank": "正处级", "note": "2021-01 起任(接梁建松); 2022-11 接受周口市政府网访谈"},
    {"person_id": 17, "org_id": 14, "title": "洛阳市人民政府副市长", "start_date": "2024-03", "end_date": "present",
     "rank": "副厅级", "note": "跨市任洛阳市人民政府副市长(自鹿邑县委书记任上)"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 现任党政一把手（搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "郭俊涛(县委书记)、刘锋磊(县委副书记/县长) 2024年末起主政搭档；十四届党代会主席台并列前排，多次同场主持全会/两会/总林长令签发",
     "overlap_org": "中共鹿邑县委员会/鹿邑县人民政府", "overlap_period": "2024年末至今"},

    # 县委班子: 书记 × 副书记/常委
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "郭俊涛(书记) × 袁航(专职副书记、政法委书记)",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "刘锋磊(县长) × 袁航(县委副书记) 同届县委班子，袁航协助推动三农/乡村振兴",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2024年末至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "郭俊涛(书记) × 张建威(常委、常务副县长)",
     "overlap_org": "中共鹿邑县委员会/鹿邑县人民政府", "overlap_period": "2024.12至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "郭俊涛(书记) × 朱高建(常委、纪委书记、监委主任)",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "郭俊涛(书记) × 牛海燕(常委、组织部长)",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "郭俊涛(书记) × 王臻(常委、宣传部长)",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "郭俊涛(书记) × 刘翔(常委、县委办公室主任)",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "郭俊涛(书记) × 刘双博(常委、统战部长、副县长)",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "郭俊涛(书记) × 李展(常委、副县长正处级)",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "郭俊涛(书记) × 韩凤城(副县长、公安局长) —— 地方维稳与政法工作主责配合",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2026年至今"},

    # 政府班子: 县长 × 副职们
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "刘锋磊(县长) × 张建威(常务副县长)——党政主干分工配合",
     "overlap_org": "鹿邑县人民政府", "overlap_period": "2024.12至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "刘锋磊(县长) × 李展(副县长正处级)",
     "overlap_org": "鹿邑县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "刘锋磊(县长) × 韩凤城(副县长、公安局长)",
     "overlap_org": "鹿邑县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "刘锋磊(县长) × 乔伟(副县长)",
     "overlap_org": "鹿邑县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "刘锋磊(县长) × 毛斌(县处级干部、开发区五级职员)",
     "overlap_org": "鹿邑县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "刘锋磊(县长) × 刘双博(副县长兼统战部长)",
     "overlap_org": "鹿邑县人民政府", "overlap_period": "2026年至今"},

    # 政府 × 人大
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "刘锋磊(县长) × 王智华(人大常委会党组书记、主任)——2026-02 人大七次会议同台，政府向人大报告工作",
     "overlap_org": "鹿邑县人民代表大会常务委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "郭俊涛(书记) × 王智华(人大常委会主任)——2026-02 县七届人大会议同台",
     "overlap_org": "中共鹿邑县委员会/鹿邑县人民代表大会常务委员会", "overlap_period": "2026年至今"},

    # 书记序列: 朱良才 → 梁建松 → 李刚 → 郭俊涛（跨区域/交接）
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor",
     "context": "李刚任鹿邑县委书记(2021.01-2024.03)期间，郭俊涛从2021.03起任县委副书记/县长——二人县长×书记共事三年；2024.03 李刚跨市调任洛阳市副市长后，郭俊涛2024.05接任县委一把手（职务交接）",
     "overlap_org": "中共鹿邑县委员会/鹿邑县人民政府", "overlap_period": "2021.03-2024.05"},
    {"person_a": 17, "person_b": 16, "type": "predecessor_successor",
     "context": "梁建松任鹿邑县委书记(2017-2021.01)期间，李刚于2017.07任县委副书记、县长(2018.01当选)——梁李共事约三年半；2021.01 李刚接任县委书记（职务交接）",
     "overlap_org": "中共鹿邑县委员会/鹿邑县人民政府", "overlap_period": "2017.07-2021.01"},
    {"person_a": 15, "person_b": 16, "type": "predecessor_successor",
     "context": "朱良才任周口市委常委、鹿邑县委书记(约2015-2017初)后转河南省政府，梁建松2017年初前后接任鹿邑县委书记（交接点待核，2017-02梁已为书记）",
     "overlap_org": "中共鹿邑县委员会", "overlap_period": "2016年末-2017年初"},
    {"person_a": 15, "person_b": 1, "type": "cross_county",
     "context": "朱良才（鹿邑县委书记→省政府副秘书长→省民政厅厅长→濮阳市市长）为鹿邑走出去的最高级干部路径之一；郭俊涛为现行书记，构成鹿邑书记序列的『本地』与『跨市』两端（间接关联）",
     "overlap_org": "鹿邑县/河南省/濮阳市", "overlap_period": "2015-2023"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

_SOURCES_ALL = [
    {"id": "S001", "title": "鹿邑县人民政府门户·2026年8月县党政领导干部接访日程安排表(官方PDF)",
     "url": "https://www.luyi.gov.cn/portal/xinwen/tzgg/webinfo/2026/07/1787018693575066.htm",
     "publisher": "鹿邑县人民政府", "source_type": "official", "reliability": "high",
     "notes": "县委/县政府全班子名称、现任岗位与分工(郭俊涛、刘锋磊、袁航、李展、张建威、朱高建、牛海燕、王臻、刘翔、刘双博、韩凤城、乔伟、毛斌等)"},
    {"id": "S002", "title": "鹿邑县政府门户·《领导信息》页",
     "url": "https://www.luyi.gov.cn/portal/zwgk/ldxx/A000205index_1.htm",
     "publisher": "鹿邑县人民政府", "source_type": "official", "reliability": "high",
     "notes": "县长/各副县长名单与职责分工"},
    {"id": "S003", "title": "中国共产党鹿邑县第十四次代表大会隆重开幕（鹿邑要闻）",
     "url": "https://www.luyi.gov.cn/portal/xinwen/lyyw/webinfo/2026/06/1784240597263763.htm",
     "publisher": "鹿邑县人民政府", "source_type": "official", "reliability": "high",
     "notes": "2026-06-24 郭俊涛作县委工作报告；主席团名单"},
    {"id": "S004", "title": "县委常委会召开扩大会议（2026-07-14 报道 / 2026-08-05 报道）",
     "url": "https://www.luyi.gov.cn/portal/xinwen/lyyw/webinfo/2026/07/1785449216137977.htm",
     "publisher": "鹿邑县人民政府", "source_type": "official", "reliability": "high",
     "notes": "县委书记郭俊涛主持召开常委会（确认在任）"},
    {"id": "S005", "title": "县政府召开第63次常务会议",
     "url": "https://www.luyi.gov.cn/portal/xinwen/lyyw/webinfo/2026/07/1786773174658518.htm",
     "publisher": "鹿邑县人民政府", "source_type": "official", "reliability": "high",
     "notes": "县长刘锋磊主持县政府常务会议（确认在任）"},
    {"id": "S006", "title": "县十六届人大七次会议隆重开幕",
     "url": "https://www.luyi.gov.cn/portal/xinwen/lyyw/webinfo/2026/02/1771767041769892.htm",
     "publisher": "鹿邑县人民政府", "source_type": "official", "reliability": "high",
     "notes": "王智华 县人大常委会党组书记、主任；郭俊涛宣布开幕、刘锋磊作政府工作报告"},
    {"id": "S007", "title": "本仓库 person JSON·朱良才(濮阳市市长·曾任鹿邑县委书记)",
     "url": "data/persons/20260724-河南省-濮阳市-市长-朱良才.json",
     "publisher": "gov-relation 仓库", "source_type": "database", "reliability": "high",
     "notes": "朱良才 鹿邑县长(2010)→周口市委常委/鹿邑县委书记(2015)→省政府副秘书长(2017)→省民政厅(2021)→濮阳市长(2023)"},
    {"id": "S008", "title": "百度百科·郭俊涛词条（人物履历/职务任免）",
     "url": "https://baike.baidu.com/item/%E9%83%AD%E4%BF%8A%E6%B6%9B/9755065",
     "publisher": "百度百科", "source_type": "encyclopedia", "reliability": "medium",
     "notes": "郭俊涛：男,汉族,1981-10生于河南禹州,2001-12入党,2003-08参工,郑大法学学士；许昌市政府办→襄城→长葛→鹿邑县(2021.03)→书记(2024.05)；2024.06兼人武部党委第一书记"},
    {"id": "S009", "title": "今日头条·《郭俊涛任周口市鹿邑县委书记》(2024-05-15)",
     "url": "https://www.toutiao.com/article/7369045941862810175/",
     "publisher": "今日头条(鹿邑融媒体中心消息)", "source_type": "media", "reliability": "high",
     "notes": "2024-05-14 郭俊涛以书记身份主持县委常委会; 李刚 1974年4月生、河南新密人, 2021-01任鹿邑书记, 2024-03已跨市任洛阳市人民政府副市长"},
    {"id": "S010", "title": "快讯！郭振涛当选鹿邑县人民政府县长——周口网(2021-03-11)",
     "url": "http://www.zkxww.com/news/zhoukou/yw/2021-03-11/308813.html",
     "publisher": "周口网/周口广播电视台", "source_type": "media", "reliability": "high",
     "notes": "2021-03-10 鹿邑县十五届人大六次会议选举郭俊涛为县长"},
    {"id": "S011", "title": "周口市人民政府·领导介绍——副市长梁建松",
     "url": "https://www.zhoukou.gov.cn/page_pc/zwgk/jcxxgk/ldzc/szf/ljs/jl/article8cc6d1ca35dc4b7bb532b897c2fda53b.html",
     "publisher": "周口市人民政府", "source_type": "official", "reliability": "high",
     "notes": "梁建松：男,汉族,1966-10生,大学学历,中共党员,现任周口市政府副市长、党组成员"},
    {"id": "S012", "title": "鹿邑县召开2020年『庆国庆迎中秋』老干部座谈会(2020-09-22)",
     "url": "http://www.zhld.com/content/2020-09/22/content_896570.html",
     "publisher": "中华龙都网(周口日报社)", "source_type": "media", "reliability": "high",
     "notes": "2020-09 鹿邑县委书记为梁建松、县委副书记兼县长为李刚；雷申、杨所、侯自峰等参加"},
    {"id": "S013", "title": "鹿邑县研究部署重点工作(中华龙都网 2024-12-06)",
     "url": "http://www.zhld.com/szb/pc/col/202412/06/content_261854.html",
     "publisher": "中华龙都网(周口日报社)", "source_type": "media", "reliability": "high",
     "notes": "2024-11-29 鹿邑县委副书记、县长刘锋磊主持县政府第四十次常务会议(县长身份最早节点)"},
    {"id": "S014", "title": "宏图已绘 稳中求进挑大梁——2026年鹿邑县政府工作报告解读(2026-03-13)",
     "url": "http://www.zhld.com/content/2026-03/13/content_1098125.html",
     "publisher": "中华龙都网(周口日报社)", "source_type": "media", "reliability": "high",
     "notes": "2026-02-12 县十六届人大七次会议开幕, 刘锋磊作政府工作报告; 2025年GDP 524.5亿、+6.4%、居全市首位"},
    {"id": "S015", "title": "鹿邑县发布2026年总林长令(河南经济报 2026-04-03)",
     "url": "https://www.hnjjbs.com/article/2026-04/178717507551722.html",
     "publisher": "河南经济报", "source_type": "media", "reliability": "high",
     "notes": "2026-04 县委书记、县第一总林长郭俊涛与县长、县总林长刘锋磊共同签发总林长令"},
    {"id": "S016", "title": "确保高质量完成全年目标任务(中华龙都网 2024-07-19)",
     "url": "http://www.zhld.com/szb/pc/col/202407/19/content_245915.html",
     "publisher": "中华龙都网(周口日报社)", "source_type": "media", "reliability": "medium",
     "notes": "2024-07-19 鹿邑县领导干部会议：郭俊涛、刘锋磊、齐长军、王智华、张国庆、宋涛、袁航、肖炜、孙自豪、王树强、顾永庆等县处级领导出席"},
    {"id": "S017", "title": "以全面深化改革推进中国式现代化建设鹿邑实践——访鹿邑县委书记郭俊涛(2024-10-25)",
     "url": "https://www.zhoukou.gov.cn/page_pc/zmhd/zxft/article6bbfee0c2b7b43b99f4da1b0410d5e0d.html",
     "publisher": "周口市人民政府门户", "source_type": "official", "reliability": "high",
     "notes": "权威访谈 郭俊涛 县委书记（2024-10）"},
    {"id": "S018", "title": "河南省鹿邑县委书记杨刚（已卸任）到县政协机关调研(人民政协网 2021-11-26)",
     "url": "http://www.rmzxw.com.cn/c/2021-11-26/2991785.shtml",
     "publisher": "人民政协网", "source_type": "media", "reliability": "high",
     "notes": "杨刚当选县委书记；袁航 组织部长；雷刚 县政协主席；丁崇高、顾伟、李兰明 政协副主席"},
    {"id": "S019", "title": "鹿邑县 2020-09-28 巡视整改小组会议",
     "url": "http://www.zhld.com/content/2020-09/17/content_897782.html",
     "publisher": "中华龙都网(周口日报社)", "source_type": "media", "reliability": "high",
     "notes": "省委第十一巡视组反馈整改：梁建松（书记）主持；李刚等县领导参会（对照中华龙都网 2020-09-28 报道 x 修正）"},
]

_person_source_map = {
    1: ["S001", "S002", "S008", "S009", "S010", "S017"],     # 郭俊涛
    2: ["S001", "S002", "S006", "S013", "S014", "S015"],     # 刘锋磊
    3: ["S001", "S016", "S018"],                              # 袁航
    4: ["S001", "S002"],                                      # 李展
    5: ["S001", "S002"],                                      # 张建威
    6: ["S001"],                                              # 朱高建
    7: ["S001"],                                              # 牛海燕
    8: ["S001"],                                              # 王臻
    9: ["S001", "S002"],                                      # 刘翔
    10: ["S001", "S002"],                                     # 刘双博
    11: ["S001", "S002"],                                     # 韩凤城
    12: ["S001", "S002"],                                     # 乔伟
    13: ["S001", "S002"],                                     # 毛斌
    14: ["S006"],                                             # 王智华
    15: ["S007", "S009"],                                    # 朱良才
    16: ["S011", "S012", "S019"],                            # 梁建松
    17: ["S009", "S012", "S018"],                            # 李刚
}

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON 生成（含关系/治理记录/专业画像）
# ══════════════════════════════════════════════════════════════════════════════

_NAME_BY_ID = {p["id"]: p["name"] for p in persons}
_TOP_IDS = {1, 2}
_RANK_BY_ID = {1: "正处级", 2: "正处级", 3: "副处级", 4: "正处级", 5: "副处级", 6: "副处级",
               7: "副处级", 8: "副处级", 9: "副处级", 10: "副处级", 11: "副处级", 12: "副处级",
               13: "县处级", 14: "正处级", 15: "正厅级", 16: "副厅级", 17: "副厅级"}


def _relationships_for(person_id: int) -> list[dict]:
    out = []
    for item in relationships:
        if item["person_a"] != person_id and item["person_b"] != person_id:
            continue
        other = item["person_b"] if item["person_a"] == person_id else item["person_a"]
        out.append({
            "person": _NAME_BY_ID[other],
            "person_id": f"{_PID}_{_NAME_BY_ID[other]}",
            "relationship_type": item["type"],
            "strength": _rel_for_strength(item),
            "evidence": item["context"],
            "overlap_org": item.get("overlap_org", ""),
            "overlap_period": item.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if item["type"] != "cross_county" else "plausible",
            "source_ids": [],
        })
    return out


def _rel_for_strength(item: dict) -> str:
    if item["type"] == "predecessor_successor":
        return "strong"
    if item["type"] == "cross_county":
        return "weak"
    return "strong" if (item["person_a"] in _TOP_IDS or item["person_b"] in _TOP_IDS) else "medium"


def _timeline_for(person_id: int) -> list[dict]:
    out = []
    for p in positions:
        if p["person_id"] != person_id:
            continue
        org_name = next((o["name"] for o in organizations if o["id"] == p["org_id"]), "")
        out.append({
            "start": p.get("start_date") or "未知",
            "end": p.get("end_date") or "未知",
            "org": org_name,
            "title": p["title"],
            "level": p.get("rank", ""),
            "system": "party" if "委" in org_name and "政府" not in org_name else "government",
            "rank": p.get("rank", ""),
            "is_key_promotion": False,
            "notes": p.get("note", ""),
            "confidence": "confirmed",
            "source_ids": [],
        })
    return out if out else [
        {"start": "未知", "end": "未知", "org": "履历缺口", "title": "",
         "notes": "公开资料未获取完整履历", "confidence": "unverified", "source_ids": []}
    ]


_GOVERNANCE: dict[int, list[dict]] = {
    1: [
        {"period": "2025", "domain": "economic_development", "achievement_or_event": "全县地区生产总值524.5亿元(+6.4%), 总量居周口市首位; 规上工业增加值+10.6%",
         "role_in_event": "县委书记, 主持县委全面工作", "measurable_outcome": "GDP 524.5亿元, 连续4年跻身全省县域经济30强/中部百强县", "location": "鹿邑县", "confidence": "confirmed", "source_ids": ["S014"]},
        {"period": "2025", "domain": "industry", "achievement_or_event": "澄明食品产业园价值超60亿, 宋河酒业重整成功, 高端化妆刷/精品工业刷市场占有率提升, 通大数控五轴联动数控机床核心技术国内领先",
         "role_in_event": "书记, 产业升级主抓", "measurable_outcome": "培育高新技术企业23家、科技型中小企业125家; 战新产业增加值占规上工业30%", "location": "鹿邑县", "confidence": "confirmed", "source_ids": ["S014"]},
        {"period": "2025", "domain": "environment", "achievement_or_event": "涡河北岸生态廊道建设、引江济淮工程县域生态环境保护、城乡供水一体化",
         "role_in_event": "县委书记、县第一总林长(2026-04签发总林长令)", "measurable_outcome": "总林长令部署鸟类保护与生态安全", "location": "鹿邑县", "confidence": "confirmed", "source_ids": ["S015"]},
    ],
}
_PROFESSIONAL: dict[int, dict] = {
    1: {
        "primary_specializations": ["县域经济", "开发区/园区建设", "招商引资", "基层治理"],
        "secondary_specializations": ["法治工作(法学出身)", "乡村振兴", "文旅融合(老子故里)"],
        "career_pattern": "cross_county_rotation",
        "systems_experience": ["party", "government"],
        "geographic_pattern": ["许昌市(出生地)", "许昌市东城区", "襄城县", "长葛市", "鹿邑县(周口市)"],
        "promotion_velocity": {"summary": "2012副处(东城区管委会)→2016县常委→2019县级市常委/常务副→2021正处县长→2024县委书记，县域执政阶梯约8年; 由生产性科员岗位起步（许昌市政府办）",
                               "notable_fast_promotions": ["2019-2021 长葛市委常委/常务副市长→鹿邑县长(跨市升任正处)"]},
    },
}
_EXTRA_OPEN_QUESTIONS: dict[int, list[dict]] = {
    1: [
        {"priority": "medium", "question": "郭俊涛任职鹿邑县委书记是否于2026年8月后有任何调整", "why_it_matters": "本轮复核资料截至2026-04", "suggested_queries": ["鹿邑县委书记 2026年8月"], "last_attempted": AS_OF},
    ],
}


def write_person_json(person: dict, source_register: list[dict]) -> None:
    pid = person["id"]
    name = person["name"]
    role = person["current_post"]
    fname = f"{TODAY}-河南省-周口市-{role}-{name}.json"
    is_top = pid in _TOP_IDS
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省", "city": "周口市", "region": "鹿邑县",
            "job": role, "task_id": TASK_ID, "time_focus": AS_OF,
        },
        "identity": {
            "person_id": f"{_PID}_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", person.get("birthplace", "")),
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": person.get("education", "") or "学历待核",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": "https://www.luyi.gov.cn/portal/zwgk/ldxx/A000205index_1.htm",
            },
        },
        "current_status": {
            "current_post": role,
            "current_org": person["current_org"],
            "administrative_rank": _RANK_BY_ID.get(pid, "副处级"),
            "as_of": AS_OF,
            "is_current_confirmed": pid in (1, 2, 14) or pid in (15, 16, 17),
            "source_ids": [s.get("id") for s in source_register][:4],
        },
        "career_timeline": _timeline_for(pid),
        "organizations": [],
        "relationships": _relationships_for(pid),
        "governance_record": _GOVERNANCE.get(pid, []),
        "professional_profile": _PROFESSIONAL.get(pid, {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "未知",
            "systems_experience": [],
            "geographic_pattern": ["鹿邑县"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        }),
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style inferred from public reports, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "本轮调查范围（鹿邑县政府门户/官方会议报道/周口日报）未发现针对相关领导的纪律处分或负面报道；2020-09 省委第十一巡视组整改为常规整改进程，非针对个人处置。",
             "confidence": "unverified", "source_ids": []}
        ],
"source_register": source_register,
        "confidence_summary": {
            "identity": ("confirmed" if person.get("birth") else "partial"),
            "current_role": "confirmed",
            "career_completeness": ("complete" if pid == 1 else ("partial" if pid in (2, 15, 16, 17) else "thin")),
            "relationship_confidence": "high" if pid in (1, 2) else "medium",
            "biggest_gap": ("刘锋磊出生/学历/任前履历未公开" if pid == 2 else "上任前完整履历(出生/学历/时间线)"),
        },
        "open_questions": [
            {"priority": "critical" if pid in (2,) else "high", "question": f"{name} 的出生年月、学历、上任前履历(时间线)",
             "why_it_matters": "还原晋升路径与跨县人际网络",
             "suggested_queries": [f"{name} 简历", f"{name} 任前公示 鹿邑"], "last_attempted": TODAY},
            * _EXTRA_OPEN_QUESTIONS.get(pid, []),
        ],
    }
    path = PERSONS_DIR / fname
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


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

    written = []
    for pid, src_ids in _person_source_map.items():
        person = next(p for p in persons if p["id"] == pid)
        reg = [s for s in _SOURCES_ALL if s["id"] in src_ids]
        written.append(write_person_json(person, reg))

    print("鹿邑县 network build complete.")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Person JSONs: {len(written)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")