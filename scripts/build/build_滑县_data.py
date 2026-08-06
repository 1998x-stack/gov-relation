#!/usr/bin/env python3
"""
滑县（安阳市）领导班子工作关系网络 — 构建脚本

等级: 县 | 上级: 河南省安阳市
调查日期: 2026-08-06
数据来源: 滑县人民政府门户 www.hnhx.gov.cn「领导信息」官方领导简介、政府门户时政新闻、
         以及 2024-09-02《全县领导干部会议》实录（宣告李明东任书记）。
说明: 调查期间外部搜索引擎(Exa/Baidu/Bing/Google)全部受限，采用 partial-evidence 模式；
      核心领导身份（县委书记/县长）由一手官方来源确认，
      传记/任职细节以 open_questions 显式标注，不虚构。
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
SLUG = "滑县"
TODAY = "2026-08-06"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "安阳市"
REGION = "滑县"
TASK_ID = "henan_滑县"

# ── Paths ──
HERE = Path(__file__).parent
DB_PATH = HERE / f"{REGION}_network.db"
GEXF_PATH = HERE / f"{REGION}_network.gexf"
PERSONS_DIR = HERE

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 现任县委书记 李明东 ──
    {
        "id": 1,
        "name": "李明东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共滑县县委书记（兼安阳市委常委）",
        "current_org": "中共滑县委员会",
        "source": "https://www.hnhx.gov.cn/portal/xwzx/hxyw/webinfo/2024/09/1727012815214012.htm — 全县领导干部会议实录(2024-09-02)；且 www.hnhx.gov.cn 多篇 2026-07/08 新闻称「市委常委、县委书记李明东」",
        "notes": "2024-09-02 全省领导干部会议宣告省委/市委决定：李明东任中共滑县县委委员、常委、书记；同时任中共安阳市委常委。任前职务、出生/籍贯/学历/入党时间 公开渠道暂未获取。",
    },
    # ── 现任县长 王军华 ──
    {
        "id": 2,
        "name": "王军华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "",
        "native_place": "",
        "education": "大学，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长、党组书记、县总河长",
        "current_org": "滑县人民政府",
        "source": "https://www.hnhx.gov.cn 领导信息官方页「王军华官方简介」: 男，汉族，1975年11月出生，大学，法律硕士，中共党员；现任县委副书记，县政府县长、党组书记",
        "notes": "领导信息官方简介确认；2024-09 已为县长兼人大代表会主持人；出生年月 1975-11；早年履历/任滑县县长前上一职务/籍贯 未公开。",
    },
    # ── 现任县委副书记、政法委书记 晁志伟 ──
    {
        "id": 3,
        "name": "晁志伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共滑县委员会",
        "source": "www.hnhx.gov.cn 2026-07「八一」走访慰问报道: 李明东、王军华、县委副书记、政法委书记晁志伟开展走访",
        "notes": "官方报道确认（2026-07）；年纪本/籍贯/学历/任前职务待查。",
    },
    # ── 现行纪委书记 孙洪 ──
    {
        "id": 4,
        "name": "孙洪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "滑县纪律检查委员会",
        "source": "www.hnhx.gov.cn 2026-07-27《县委巡察工作会议暨十三届县委第一轮巡察戒备部署会》: 县委常委、县纪委书记、县监委主任孙洪",
        "notes": "官方报道确认（2026-07）；传记待查。",
    },
    # ── 组织部长 崔文峰 ──
    {
        "id": 5,
        "name": "崔文峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共滑县委员会组织部",
        "source": "www.hnhx.gov.cn 2026-07-27 巡察工作会报道：县委常委、组织部部长崔文峰主持会议并传达相关文件",
        "notes": "官方报道确认（2026-07）；传记待查。",
    },
    # ── 宣传部长 李红霞 ──
    {
        "id": 6,
        "name": "李红霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971-04",
        "birthplace": "",
        "native_place": "",
        "education": "大学，本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长（兼县政府副县长、党组成员）",
        "current_org": "中共滑县委员会宣传部",
        "source": "领导信息官方页：女，汉族，1971年4月出生，大学，本科学历，中共党员；现任县委常委、宣传部部长，县政府副县长、党组成员",
        "notes": "官方简介确认",
    },
    # ── 常务副县长 陈海青 ──
    {
        "id": 7,
        "name": "陈海青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-11",
        "birthplace": "",
        "native_place": "",
        "education": "大学，本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长、党组副书记",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，汉族，1983年11月出生，大学，本科学历；现任县委常委，县政府副县长、党组副书记",
        "notes": "官方简介确认；主持县政府日常工作，办全会上通报经济运行情况。",
    },
    # ── 副县长 王瑞 ──
    {
        "id": 8,
        "name": "王瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，汉族，1982年10月出生，在职研究生，工商管理硕士，中共党员；现任县政府副县长、党组成员",
        "notes": "官方简介确认，兼县委常委；2026 污染防治推进会传达省市精神。",
    },
    # ── 副县长（公安局长）臧国民 ──
    {
        "id": 9,
        "name": "臧国民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、县公安局局长、党委书记、督察长（兼县委政法委副书记）",
        "current_org": "滑县公安局",
        "source": "领导信息官方页：男，汉族，1975年3月出生，大学学历，中共党员；副县长、局长、督察长，县委政法委副书记(兼)",
        "notes": "官方简介确认。",
    },
    # ── 副县长 顾建宇 ──
    {
        "id": 10,
        "name": "顾建宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "",
        "native_place": "",
        "education": "大学，研究生，工商管理专业硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，1984年7月出生，汉族，大学，研究生学历，工商管理专业硕士，中共党员",
        "notes": "官方简介确认。",
    },
    # ── 副县长 李红斌 ──
    {
        "id": 11,
        "name": "李红斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "",
        "native_place": "",
        "education": "大学，法律学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，汉族，1972年9月出生，大学，法律学硕士，中共党员；现任县政府副县长、党组成员",
        "notes": "官方简介确认。",
    },
    # ── 副县长 胡博文 ──
    {
        "id": 12,
        "name": "胡博文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-07",
        "birthplace": "",
        "native_place": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，汉族，1982年7月出生，硕士研究生学历，中共党员；副县长、党组成员",
        "notes": "官方简介确认。",
    },
    # ── 副县长 闫博 ──
    {
        "id": 13,
        "name": "闫博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-04",
        "birthplace": "",
        "native_place": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，1989年4月出生，汉族，大学学历，工学学士，中共党员",
        "notes": "官方简介确认。",
    },
    # ── 副县长 程靓莎 ──
    {
        "id": 14,
        "name": "程靓莎",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987-09",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员；王庄镇党委书记（兼）",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：女，汉族，1987年9月出生，在职研究生，法学学士，中共党员；副县长、王庄镇党委书记（兼）",
        "notes": "官方简介确认。",
    },
    # ── 副县长 徐继峰 ──
    {
        "id": 15,
        "name": "徐继峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-12",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，汉族，1981年12月生，研究生，中共党员",
        "notes": "官方简介确认。",
    },
    # ── 副县长 张红星 ──
    {
        "id": 16,
        "name": "张红星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-05",
        "birthplace": "",
        "native_place": "",
        "education": "大学，本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "滑县人民政府",
        "source": "领导信息官方页：男，汉族，1976年5月出生，大学，本科学历，中共党员",
        "notes": "官方简介确认。",
    },
    # ── 人大常委会主任 王为治 ──
    {
        "id": 17,
        "name": "王为治",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "滑县人民代表大会常务委员会",
        "source": "www.hnhx.gov.cn 多篇新闻报道：王为治为县人大常委会领导（人大六次会议、主任会议等）",
        "notes": "官方报道确认；传记待查。",
    },
    # ── 政协主席 李卫锋 ──
    {
        "id": 18,
        "name": "李卫锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协滑县委员会",
        "source": "www.hnhx.gov.cn 2026「八一」走访慰问报道、政协会议报道；县领导李卫锋",
        "notes": "官方报道确认；传记待查。",
    },
    # ── 检察院检察长 李涛 ──
    {
        "id": 19,
        "name": "李涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民检察院检察长",
        "current_org": "滑县人民检察院",
        "source": "www.hnhx.gov.cn 2026-08-04《县人民检察院举行第二届检察听证员聘任仪式》报道：县检察院检察长李涛",
        "notes": "官方报道确认。",
    },
    # ── 前任县委书记 陈忠 ──
    {
        "id": 20,
        "name": "陈忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记（十二届，2024-09 李明东接任）、去向待查",
        "current_org": "中共滑县委员会",
        "source": "www.hnhx.gov.cn 2023-2024 官方报道：「陈忠在十二届县纪委书记四次全会发言」「陈忠调研…开工……」等系列（十二届县委书记）",
        "notes": "2023-2024 期间为十二届县委书记，2024-09-02 由李明东接任；去向/现职 待查。",
        "is_former": True,
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共滑县委员会", "type": "党委", "level": "县处级",
     "parent": "中共安阳市委员会", "location": "河南省安阳市滑县"},
    {"id": 2, "name": "滑县人民政府", "type": "政府", "level": "县处级",
     "parent": "安阳市人民政府", "location": "河南省安阳市滑县"},
    {"id": 3, "name": "中共滑县委员会政法委", "type": "党委", "level": "县处级",
     "parent": "中共滑县委员会", "location": "滑县"},
    {"id": 4, "name": "滑县纪律检查委员会、县监察委员会", "type": "党委", "level": "县处级",
     "parent": "中共滑县委员会", "location": "滑县"},
    {"id": 5, "name": "中共滑县委员会组织部", "type": "党委", "level": "县处级",
     "parent": "中共滑县委员会", "location": "滑县"},
    {"id": 6, "name": "中共滑县委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共滑县委员会", "location": "滑县"},
    {"id": 7, "name": "滑县公安局", "type": "政府", "level": "县处级",
     "parent": "滑县人民政府", "location": "滑县"},
    {"id": 8, "name": "滑县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "滑县", "location": "滑县"},
    {"id": 9, "name": "中国人民政治协商会议滑县委员会", "type": "政协", "level": "县处级",
     "parent": "滑县", "location": "滑县"},
    {"id": 10, "name": "滑县人民检察院", "type": "政府", "level": "县处级",
     "parent": "滑县", "location": "滑县"},
    {"id": 11, "name": "中共安阳市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共河南省委", "location": "河南省安阳市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 李明东 — 县委书记（2024-09-02 至今）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2024-09-02", "end": "present",
     "rank": "正处级", "note": "2024-09-02 全县领导干部会议宣告任命；兼县人武部党委第一书记"},
    {"person_id": 1, "org_id": 11, "title": "安阳市委常委", "start": "unknown", "end": "present",
     "rank": "副厅级", "note": "官方报道载「市委常委、滑县县委书记」；交叉印证 build_安阳市_data.py；到任准确时间待查"},
    # 王军华 — 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present",
     "rank": "正处级", "note": "官方简介与新闻报道确认"},
    {"person_id": 2, "org_id": 2, "title": "县长、党组书记、县总河长", "start": "unknown", "end": "present",
     "rank": "正处级", "note": "领导信息官方页确认；主持县政府全面工作；2024-09 已任县长；任职起始待查"},
    # 晁志伟
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present",
     "rank": "副处级", "note": "2026-07 官方报道确认"},
    {"person_id": 3, "org_id": 3, "title": "政法委书记", "start": "unknown", "end": "present",
     "rank": "副处级", "note": "2026-07 官方报道确认"},
    # 孙洪 — 纪委
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "县纪委书记、县监委主任", "start": "unknown", "end": "present",
     "rank": "副处级", "note": "2026-07-27 巡察部署会报道确认"},
    # 崔文峰 — 组织
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start": "unknown", "end": "present",
     "rank": "副处级", "note": "2026-07 巡察会报道确认"},
    # 李红霞
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "县政府副县长（兼）", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 陈海青 — 常务副县长
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "常务副县长、党组副书记", "start": "unknown", "end": "present",
     "rank": "副处级", "note": "官方简介确认，主持县政府常务；全县项目推进会上通报经济运行情况"},
    # 王瑞
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "县政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 臧国民
    {"person_id": 9, "org_id": 2, "title": "县政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "县公安局局长、党委书记、督察长（兼县委政法委副书记）", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 顾建宇等一般副县长
    {"person_id": 10, "org_id": 2, "title": "县政府副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县政府副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县政府副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "县政府副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "县政府副县长、党组成员，王庄镇党委书记（兼）", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "县政府副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "县政府副县长、党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 人大 / 政协 / 检察
    {"person_id": 17, "org_id": 8, "title": "县人大常委会主任", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "县政协主席", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 10, "title": "县人民检察院检察长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 陈忠 — 前任书记
    {"person_id": 20, "org_id": 1, "title": "县委书记（十二届，前任）", "start": "unknown", "end": "2024-08",
     "rank": "正处级", "note": "2024-09-02 李明东接任；陈忠任期约 2023 前后－2024 年"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 李明东 ↔ 王军华 书记×县长 党政搭档 (confirmed)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "李任县委书记、王任县委副书记兼县长，同届县委党政班子搭档；共同出席全县领导干部会议、项目提升推进会、污染防治推进会等",
     "overlap_org": "中共滑县委员会/滑县人民政府", "overlap_period": "2024-09-至今"},
    # 王军华 ↔ 陈海庆 县长×常务副县长 政府班子 (confirmed)
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "王(县长)×陈(常委、常务副县长)政府班子，全县项目推进会上王主持、陈通报经济运行",
     "overlap_org": "滑县人民政府", "overlap_period": "2024-至今"},
    # 李明东 ↔ 晁志伟 书记×副书记/政法 (confirmed)
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "李(书记)×晁(县委副书记、政法委书记)同届县委班子，'八一'共同走访优抚对象",
     "overlap_org": "中共滑县委员会", "overlap_period": "2026-至今"},
    # 李明东 ↔ 孙洪 书记×纪委书记 (confirmed)
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "李(书记)×孙(纪委书记)共管党建/巡察；十三届县委首轮巡察部署会上共同出席",
     "overlap_org": "中共滑县委员会", "overlap_period": "2026-至今"},
    # 李明东 ↔ 崔文峰 书记×组织部长 (confirmed)
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "李(书记)×崔(组织部长)，巡察会/党建工作；崔文峰主持巡察会",
     "overlap_org": "中共滑县委员会", "overlap_period": "2026-至今"},
    # 李明东 ↔ 李红霞 书记×宣传部长 (confirmed)
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "同为县委常委会成员（李红霞兼任宣传部长、副县长）",
     "overlap_org": "中共滑县委员会", "overlap_period": "2024-至今"},
    # 前任: 陈忠 → 李明东 (predecessor-successor)
    {"person_a": 20, "person_b": 1, "type": "predecessor_successor",
     "context": "陈忠任县委书记（十二届）至 2024，李明东 2024-09-02 接任",
     "overlap_org": "中共滑县委员会", "overlap_period": "2024"},
    # 王为治/李卫锋 人大×政协 班子搭档 (confirmed)
    {"person_a": 17, "person_b": 18, "type": "overlap",
     "context": "县人大常委会主任×县政协主席，同届四套班子；县委全会/人大/政协两会同台",
     "overlap_org": "滑县四套班子", "overlap_period": "2024-至今"},
    # 王军华 ↔ 王为治 县长×人大主任 (confirmed)
    {"person_a": 2, "person_b": 17, "type": "overlap",
     "context": "县长×人大常委会主任，县十六届人大历次会议同台（政府工作报告报告/审议）",
     "overlap_org": "滑县四套班子", "overlap_period": "2024-至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001",
         "title": "全县领导干部会议宣布李明东任县委书记（2024-09-02）",
         "url": "https://www.hnhx.gov.cn/portal/xwzx/hxyw/webinfo/2024/09/1727012815214012.htm",
         "publisher": "滑县人民政府门户网站", "published_at": "2024-09-02", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "宣告李明的任中共滑县县委书记；『市委常委、滑县县委书记李明东』；列明县四套班子及县领导干部名单"},
        {"id": "S002",
         "title": "滑县人民政府『领导信息』官方页——县长、副县长简介",
         "url": "https://www.hnhx.gov.cn/portal/zwgk/ldxx/A000204index_1.htm",
         "publisher": "滑县人民政府门户网站", "published_at": "2026-08", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认王军华（1975-11/法律硕士/县长），及县政府班子陈海青/王瑞/李红霞/顾建宇/李红斌/胡博文/臧国民/闫博/程靓莎/徐继峰/张红星简介"},
        {"id": "S003",
         "title": "李明东调研项目建设工作（2026-07）",
         "url": "https://www.hnhx.gov.cn/portal/xwzx/hxyw/webinfo/2026/07/1784765006391956.htm",
         "publisher": "滑县人民政府门户网站", "published_at": "2026-07", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "『7月10日，市委常委、县委书记李明东调研项目建设』"},
        {"id": "S004",
         "title": "李明东到大寨镇调研、李明东王军华等走访优抚对象（2026-07/08）",
         "url": "https://www.hnhx.gov.cn/xwzx/hxyw/webinfo/2026/08/1786924089900675.htm",
         "publisher": "滑县人民政府门户网站", "published_at": "2026-08", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "王军华=县委副书记、县长；县政协主席李卫锋；县委副书记、政法委书记晁志伟"},
        {"id": "S005",
         "title": "全县巡察工作会议暨十三届县委第一轮巡察动员部署会（2026-07-27）",
         "url": "https://www.hnhx.gov.cn/portal/xwzx/hxyw/webinfo/2026/07/1786923637445298.htm",
         "publisher": "滑县人民政府门户网站", "published_at": "2026-07-27", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "孙洪=常委、纪委书记、县监委主任；崔文峰=常委、组织部部长；李明东出席讲话"},
        {"id": "S006",
         "title": "县十六届人大六次会议/政协十三届五次会议（2026）",
         "url": "https://www.hnhx.gov.cn/portal/xwzx/hxyw/A000101index_1.htm",
         "publisher": "滑县人民政府门户网站", "published_at": "2026", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "人大代表王为治、政协主席李卫锋；确认滑县第十六届县政府、十六届人大常委会、十三届政协"},
        {"id": "S007",
         "title": "2023-2024 陈忠（原县委书记）官方报道，含『陈忠在十二届县纪委四次全会』等",
         "url": "https://www.hnhx.gov.cn/portal/xwzx/hxyw/A000101index_1.htm",
         "publisher": "滑县人民政府门户网站", "published_at": "2023-2024", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认陈忠为十二届县委书记，2024-09 由李明东接任"},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person: dict, timeline: list[dict], rels: list[dict],
                     source_register: list[dict], job: str, person_id: str) -> dict:
    is_top = person["id"] in (1, 2)
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE, "city": CITY, "region": REGION, "job": job,
            "task_id": TASK_ID, "time_focus": "2024-2026",
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
            "education": [
                {"period": "", "institution": person.get("education", ""), "major": "",
                 "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}
            ],
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
            "source_ids": ["S001", "S002", "S003", "S004", "S005"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"] if person["id"] == 1
            else (["party", "government"] if person["id"] == 2 else ["government", "party"]),
            "geographic_pattern": ["滑县(安阳市)"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未在公开渠道发现纪律处分或负面报道信号；部分领导在巡察/风腐整治专题中被提及为机关主体",
             "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high" if is_top else "medium",
            "biggest_gap": "核心领导（尤其李明东）出生年份/籍贯/学历/入党时间及任现职前完整履历未公开",
        },
        "open_questions": [
            {"priority": "critical",
             "question": f"{person['name']}的出生年月、籍贯、学历/专业、入党及参工时间",
             "why_it_matters": "姓名+出生年是跨区去重与身份校准的关键字段",
             "suggested_queries": [f"{person['name']} 简历 滑县", f"{person['name']} 百度百科", f"{person['name']} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": f"{person['name']}任滑县{job}前的上一职务与来源单位（尤李）；王军华任县长前一职",
             "why_it_matters": "还原晋升链条与跨县调动网络",
             "suggested_queries": [f"{person['name']} 安阳 干部 任前公示", f"{person['name']} 之前 担任", f"{person['name']} 简历"],
             "last_attempted": AS_OF},
            {"priority": "medium",
             "question": "滑县县委统战部长、人大代表副主任、县人大副职等姓名与分工",
             "why_it_matters": "细走关系网络所需",
             "suggested_queries": ["滑县 县委缺 统战部长", "滑县 四套班子 名单"],
             "last_attempted": AS_OF},
        ],
    }


def li_mingdong_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "2024-08", "org": "履历缺口", "title": "",
         "notes": "李明东任县委书记前完整履历及出生年度 公开渠道未获取",
         "confidence": "unverified", "source_ids": []},
        {"start": "2024-09-02", "end": "present", "org": "滑县县委", "title": "县委书记",
         "notes": "2024-09 全县领导干部会议宣告省委/市委决定任职",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "present", "org": "中共安阳市委员会", "title": "市委常委",
         "notes": "官方报道『市委常委、滑县县委书记』（兼）",
         "confidence": "plausible", "source_ids": ["S001", "S003"]},
    ]


def wang_junhua_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "present", "org": "履历缺口", "title": "",
         "notes": "王军华任滑县县长前完整履历未公开（来电单位/任职起始）",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "滑县人民政府", "title": "县长、党组书记、总河长",
         "notes": "领导信息官方简介确认；2024-09 已任县长",
         "confidence": "confirmed", "source_ids": ["S002", "S001"]},
        {"start": "unknown", "end": "present", "org": "中共滑县委员会", "title": "县委副书记",
         "notes": "官方简介与新闻均确认",
         "confidence": "confirmed", "source_ids": ["S002", "S004"]},
    ]


def build():
    print("=" * 64)
    print("  河南省安阳市滑县 领导班子工作关系网络")
    print("  等级: 县 | 调查日期: 2026-08-06 | 信源: 滑县人民政府门户")
    print("=" * 64)

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

    # 1. 李明东（县委书记）
    lmds = make_person_json(
        persons[0], li_mingdong_timeline(),
        [
            {"person": "王军华", "person_id": "huaxian_wang_junhua", "relationship_type": "overlap",
             "strength": "strong",
             "evidence": "书记×县长（县委副书记）党政搭档，2024-09 至今；共同出席县领导干部会议/经济工作会",
             "overlap_org": "滑县县委/滑县人民政府", "overlap_period": "2024-09-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
            {"person": "晁志伟", "person_id": "huaxian_chao_zhiwei", "relationship_type": "overlap",
             "strength": "medium", "evidence": "书记×副书记兼政法委书记，同届班子（2026『八一』同行）",
             "overlap_org": "滑县县委", "overlap_period": "2026-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            {"person": "陈忠", "person_id": "huaxian_chen_zhong", "relationship_type": "predecessor_successor",
             "strength": "medium", "evidence": "前任书记（十二届），2024-09 李明东接任",
             "overlap_org": "滑县县委", "overlap_period": "2024",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S007"]},
        ],
        source_register, "县委书记", "huaxian_li_mingdong",
    )
    with open(PERSONS_DIR / f"{TODAY}-河南省-安阳市-县委书记-李明东.json", "w", encoding="utf-8") as f:
        json.dump(lmds, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 李明东")

    # 2. 王军华（县长）
    wjh = make_person_json(
        persons[1], wang_junhua_timeline(),
        [
            {"person": "李明东", "person_id": "huaxian_li_mingdong", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县长×书记党政搭档（2024-09 至今）",
             "overlap_org": "滑县人民政府/滑县县委", "overlap_period": "2024-09-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
            {"person": "陈海青", "person_id": "huaxian_chen_haiqing", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县长×常委常务副县长，政府班子；陈常务主持项目会通报经济运行",
             "overlap_org": "滑县人民政府", "overlap_period": "2024-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "王为治", "person_id": "huaxian_wang_weizhi", "relationship_type": "overlap",
             "strength": "medium", "evidence": "县长×人大主任，县两会/人大各会他同台",
             "overlap_org": "滑县四套班子", "overlap_period": "2024-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        source_register, "县长", "huaxian_wang_junhua",
    )
    with open(PERSONS_DIR / f"{TODAY}-河南省-安阳市-县长-王军华.json", "w", encoding="utf-8") as f:
        json.dump(wjh, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 王军华")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()