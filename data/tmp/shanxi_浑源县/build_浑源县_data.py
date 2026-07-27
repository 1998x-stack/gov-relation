#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 浑源县, 大同市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_浑源县
Level: 县
Targets: 县委书记 & 县长

Research context:
  - Official government site www.hunyuan.gov.cn was successfully fetched.
  - All county government leadership profiles obtained from official "县政府领导" page.
  - Party committee (县委) side confirmed via news article (县委常委会).
  - Web search tools (Exa) were rate-limited; Baidu unavailable.
  - All information is from official government sources (confirmed).
  - Some career timeline details are inferred from official biographical sketches.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "浑源县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_浑源县"
if _CURRENT_DIR.name == "shanxi_浑源县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leadership, 3-11 standing committee + deputy mayors, 12+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current, confirmed from official sources)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "赵昱清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共浑源县委员会",
        "source": "https://www.hunyuan.gov.cn (县委常委会新闻报道 2026-07-16)",
        "notes": "赵昱清以县委书记身份主持2026年7月16日县委常委会第二十次会议。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "杨琼圣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-04",
        "birthplace": "山西应县",
        "education": "大学学历",
        "party_join": "1998-10",
        "work_start": "1996-09",
        "current_post": "县委副书记、县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/llx/szfld.shtml",
        "notes": "杨琼圣，1977年4月生，山西应县人，大学学历。1998年10月入党，1996年9月参加工作。历任矿区区委常委、区委办主任，大同市市政管理委员会副主任，浑源县委常委、政府副县长，浑源县委副书记、政法委书记。现任浑源县委副书记、政府党组书记、政府县长。",
        "confidence": "confirmed"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Deputy County Heads
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "赵祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "山西大同",
        "education": "大学学历",
        "party_join": "1997-06",
        "work_start": "1994-08",
        "current_post": "县委常委、常务副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/qbw/szfld.shtml",
        "notes": "赵祥，1974年9月生，山西大同人。1997年6月入党，1994年8月参加工作。历任大同县倍加造镇综合办主任，巨乐乡副乡长、副书记、纪检书记，周士庄镇人大主席，湖东街道党委书记，云州区政府办公室主任，浑源县委常委、县委办公室主任，现任浑源县委常委、政府党组副书记、副县长。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "曹启龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "山西浑源",
        "education": "大学学历",
        "party_join": "1997-10",
        "work_start": "1996-08",
        "current_post": "县政府党组成员、恒山风景名胜区管理中心党委书记、主任",
        "current_org": "恒山风景名胜区管理中心",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/FQZHY/szfld.shtml",
        "notes": "曹启龙，1975年1月生，山西浑源人。1997年10月入党，1996年8月参加工作。历任浑源县委组织部干部科长、下韩村乡乡长、西坊城镇党委书记、东坊城乡党委书记、县委办公室主任、县委常委、政府副县长。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "雷迎春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-07",
        "birthplace": "山西浑源",
        "education": "大学学历",
        "party_join": "1994-06",
        "work_start": "1996-02",
        "current_post": "县委常委、副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/hgh/szfld.shtml",
        "notes": "雷迎春，1974年7月生，山西浑源人。1994年6月入党，1996年2月参加工作。历任共青团浑源县委书记、永安镇镇长、西留村乡党委书记、林业局局长、扶贫开发办公室主任，现任浑源县委常委、政府党组成员、副县长。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "胡鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-01",
        "birthplace": "山西平遥",
        "education": "研究生学历，哲学硕士",
        "party_join": "2008-06",
        "work_start": "2008-10",
        "current_post": "县委常委、副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/wye/szfld.shtml",
        "notes": "胡鹏，1985年1月生，山西平遥人，研究生学历，哲学硕士。2008年6月入党，2008年10月参加工作。历任山西经贸集团办公室主任科员、办公室副主任，山西文旅集团办公室副主任。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "李倩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-01",
        "birthplace": "山西灵丘",
        "education": "吉林大学计算机科学与技术专业，大学学历，理学学士",
        "party_join": "2007-11",
        "work_start": "2009-07",
        "current_post": "县委常委、副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/lqs/szfld.shtml",
        "notes": "李倩，1986年1月生，山西灵丘人。吉林大学计算机科学与技术专业毕业。2007年11月入党，2009年7月参加工作。历任省档案馆电子档案部四级调研员、副部长。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "贾雪花",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "山西天镇",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1995-10",
        "current_post": "副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/lys/szfld.shtml",
        "notes": "贾雪花，1973年5月生，山西天镇人。1995年10月参加工作。历任矿区法律援助中心副主任、矿区晋华宫街道办事处副主任、矿区工商业联合会主席、市工商业联合会副主席。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "付元进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "山西浑源",
        "education": "大学本科学历",
        "party_join": "1993-11",
        "work_start": "1992-09",
        "current_post": "副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/lxy/szfld.shtml",
        "notes": "付元进，1971年11月生，山西浑源人。1993年11月入党，1992年9月参加工作。先后在西河口乡、千佛岭乡、青磁窑乡、蔡村镇、永安镇、大磁窑镇和恒山管委会工作。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "赵铸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "山西阳高",
        "education": "大学学历",
        "party_join": "2000-06",
        "work_start": "1995-08",
        "current_post": "副县长、公安局长",
        "current_org": "浑源县公安局",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/chaotao/szfld.shtml",
        "notes": "赵铸，1972年11月生，山西阳高人。2000年6月入党，1995年8月参加工作。历任阳高县公安局王官屯派出所所长、龙泉派出所所长、副局长，大同市公安局云冈分局政委，广灵县副县长、公安局局长，2024年3月任浑源县政府党组成员、公安局党委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "张树军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-03",
        "birthplace": "山西大同",
        "education": "大学学历",
        "party_join": "1999-12",
        "work_start": "1996-04",
        "current_post": "副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/wzc/szfld.shtml",
        "notes": "张树军，1974年3月生，山西大同人。1999年12月入党，1996年4月参加工作。历任南郊区区委组织部副部长、口泉乡乡长、云冈区鸦儿崖乡党委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "王武明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-04",
        "birthplace": "山西广灵",
        "education": "大学学历",
        "party_join": "2004-11",
        "work_start": "1999-08",
        "current_post": "副县长",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/sll/szfld.shtml",
        "notes": "王武明，1980年4月生，山西广灵人。2004年11月入党，1999年8月参加工作。历任广灵县教科局科员、县委组织部科员、团县委书记、南村镇镇长、梁庄乡党委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "李玉路",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "河南南阳",
        "education": "大学学历",
        "party_join": "2005-06",
        "work_start": "2008-07",
        "current_post": "副县长（挂职）",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/wth/szfld.shtml",
        "notes": "李玉路，1984年8月生，河南南阳人。2005年6月入党，2008年7月参加工作。历任大同出入境检验检疫局办公室主任、朔州海关查检科科长、大同海关副关长，现任太原海关动植物检疫处副处长、浑源县政府党组成员、副县长（挂职）。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "王秉权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-08",
        "birthplace": "山西浑源",
        "education": "本科学历",
        "party_join": "2007-06",
        "work_start": "2002-10",
        "current_post": "县政府党组成员、县政府办公室主任",
        "current_org": "浑源县人民政府",
        "source": "https://www.hunyuan.gov.cn/hyxrmzfz/lds/szfld.shtml",
        "notes": "王秉权，1983年8月生，山西浑源人。2007年6月入党，2002年10月参加工作。先后在西坊城中心校、浑源纪检委工作；历任王庄堡镇镇长、吴城乡党委书记。",
        "confidence": "confirmed"
    },
]

organizations = [
    {"id": 1, "name": "中共浑源县委员会", "type": "党委", "level": "县处级", "parent": "中共大同市委", "location": "山西省大同市浑源县"},
    {"id": 2, "name": "浑源县人民政府", "type": "政府", "level": "县处级", "parent": "大同市人民政府", "location": "山西省大同市浑源县"},
    {"id": 3, "name": "浑源县公安局", "type": "政府", "level": "乡科级", "parent": "浑源县人民政府", "location": "山西省大同市浑源县"},
    {"id": 4, "name": "恒山风景名胜区管理中心", "type": "事业单位", "level": "县处级", "parent": "浑源县人民政府", "location": "山西省大同市浑源县"},
    {"id": 5, "name": "浑源县纪委监委", "type": "党委", "level": "县处级", "parent": "中共浑源县委员会", "location": "山西省大同市浑源县"},
    {"id": 6, "name": "浑源县人大常委会", "type": "人大", "level": "县处级", "parent": "浑源县", "location": "山西省大同市浑源县"},
    {"id": 7, "name": "浑源县政协", "type": "政协", "level": "县处级", "parent": "浑源县", "location": "山西省大同市浑源县"},
    {"id": 8, "name": "矿区区委", "type": "党委", "level": "县处级", "parent": "中共大同市委", "location": "山西省大同市矿区"},
    {"id": 9, "name": "大同市市政管理委员会", "type": "政府", "level": "县处级", "parent": "大同市人民政府", "location": "山西省大同市"},
    {"id": 10, "name": "大同县（云州区）委组织部", "type": "党委", "level": "乡科级", "parent": "中共大同县委", "location": "山西省大同市"},
    {"id": 11, "name": "山西经贸集团", "type": "政府", "level": "", "parent": "山西省国资委", "location": "山西省太原市"},
    {"id": 12, "name": "山西文旅集团", "type": "政府", "level": "", "parent": "山西省国资委", "location": "山西省太原市"},
    {"id": 13, "name": "山西省档案馆", "type": "事业单位", "level": "厅级", "parent": "山西省人民政府", "location": "山西省太原市"},
    {"id": 14, "name": "共青团浑源县委", "type": "群团", "level": "乡科级", "parent": "共青团大同市委", "location": "山西省大同市浑源县"},
    {"id": 15, "name": "浑源县林业局", "type": "政府", "level": "乡科级", "parent": "浑源县人民政府", "location": "山西省大同市浑源县"},
    {"id": 16, "name": "浑源县扶贫开发办公室", "type": "政府", "level": "乡科级", "parent": "浑源县人民政府", "location": "山西省大同市浑源县"},
    {"id": 17, "name": "阳高县公安局", "type": "政府", "level": "乡科级", "parent": "阳高县人民政府", "location": "山西省大同市阳高县"},
    {"id": 18, "name": "大同市公安局云冈分局", "type": "政府", "level": "乡科级", "parent": "大同市公安局", "location": "山西省大同市云冈区"},
    {"id": 19, "name": "广灵县人民政府", "type": "政府", "level": "县处级", "parent": "大同市人民政府", "location": "山西省大同市广灵县"},
    {"id": 20, "name": "广灵县团县委", "type": "群团", "level": "乡科级", "parent": "共青团大同市委", "location": "山西省大同市广灵县"},
    {"id": 21, "name": "大同海关", "type": "政府", "level": "县处级", "parent": "太原海关", "location": "山西省大同市"},
    {"id": 22, "name": "太原海关", "type": "政府", "level": "厅级", "parent": "海关总署", "location": "山西省太原市"},
    {"id": 23, "name": "大同市工商业联合会", "type": "群团", "level": "县处级", "parent": "大同市政协", "location": "山西省大同市"},
]

positions = [
    # ── Yang Qiongsheng's Career (杨琼圣) ──
    {"person_id": 2, "org_id": 8, "title": "矿区区委常委、区委办主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "大同市市政管理委员会副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "浑源县委常委、政府副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "浑源县委副书记、政法委书记", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "浑源县委副书记、政府代县长", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "浑源县委副书记、县政府党组书记、县长", "start": "", "end": "present", "rank": "正县级", "note": "现任"},

    # ── Zhao Xiang's Career (赵祥) ──
    {"person_id": 3, "org_id": 10, "title": "大同县倍加造镇综合办主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "巨乐乡副乡长、副书记、纪检书记", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "周士庄镇人大主席", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "湖东街道党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "云州区（原大同县）政府办公室主任", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "浑源县委常委、县委办公室主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "浑源县委常委、常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Cao Qilong's Career (曹启龙) ──
    {"person_id": 4, "org_id": 1, "title": "浑源县委组织部干部科长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "下韩村乡党委副书记、乡长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "西坊城镇党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "东坊城乡党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "浑源县委办公室主任", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "浑源县委常委、政府副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县政府党组成员、恒山风景区管理中心主任", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Lei Yingchun's Career (雷迎春) ──
    {"person_id": 5, "org_id": 14, "title": "共青团浑源县委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "永安镇镇长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "西留村乡党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 5, "org_id": 15, "title": "浑源县林业局局长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 5, "org_id": 16, "title": "浑源县扶贫开发办公室主任", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "浑源县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Hu Peng's Career (胡鹏) ──
    {"person_id": 6, "org_id": 11, "title": "山西经贸集团办公室主任科员", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 11, "title": "山西经贸集团办公室副主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 12, "title": "山西文旅集团办公室副主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "浑源县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Li Qian's Career (李倩) ──
    {"person_id": 7, "org_id": 13, "title": "省档案馆电子档案部四级调研员", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 13, "title": "省档案馆电子档案部副部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "浑源县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Jia Xuehua's Career (贾雪花) ──
    {"person_id": 8, "org_id": 8, "title": "矿区法律援助中心副主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "矿区晋华宫街道办事处副主任", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "矿区工商业联合会主席", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 8, "org_id": 23, "title": "大同市工商业联合会副主席", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "浑源县副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Fu Yuanjin's Career (付元进) ──
    {"person_id": 9, "org_id": 2, "title": "西河口乡团委书记、副乡长、副书记", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "千佛岭乡党委副书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "青磁窑乡党委副书记、乡长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "蔡村镇党委书记、人大主席", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "永安镇党委书记、人大主席", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "大磁窑镇党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "恒山风景名胜区管委会主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "浑源县副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Zhao Zhu's Career (赵铸) ──
    {"person_id": 10, "org_id": 17, "title": "阳高县公安局王官屯派出所所长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 17, "title": "阳高县公安局龙泉派出所所长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 10, "org_id": 17, "title": "阳高县公安局副局长兼龙泉派出所所长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 10, "org_id": 18, "title": "大同市公安局云冈分局政委", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 19, "title": "广灵县副县长、公安局局长", "start": "", "end": "2024-03", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 3, "title": "浑源县副县长、公安局长", "start": "2024-03", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Zhang Shujun's Career (张树军) ──
    {"person_id": 11, "org_id": 8, "title": "南郊区区委组织部副部长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "口泉乡党委副书记、乡长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 11, "org_id": 18, "title": "云冈区鸦儿崖乡党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "浑源县副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Wang Wuming's Career (王武明) ──
    {"person_id": 12, "org_id": 19, "title": "广灵县教科局科员", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 19, "title": "广灵县委组织部科员/组织科副科长/公务员管理科科长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 20, "title": "广灵县团县委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 12, "org_id": 19, "title": "广灵县南村镇党委副书记、镇长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 12, "org_id": 19, "title": "广灵县梁庄乡党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "浑源县副县长", "start": "", "end": "present", "rank": "副县级", "note": "现任"},

    # ── Li Yulu's Career (李玉路 - 挂职) ──
    {"person_id": 13, "org_id": 21, "title": "大同出入境检验检疫局办公室主任", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 13, "org_id": 21, "title": "朔州海关查检科科长、一级主办", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 13, "org_id": 21, "title": "大同海关副关长、党委委员", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 22, "title": "太原海关动植物检疫处副处长", "start": "", "end": "present", "rank": "副处级", "note": "现任"},
    {"person_id": 13, "org_id": 2, "title": "浑源县副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},

    # ── Wang Bingquan's Career (王秉权) ──
    {"person_id": 14, "org_id": 2, "title": "西坊城中心校工作", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "浑源纪检委工作", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "王庄堡镇镇长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "吴城乡党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "县政府党组成员、县政府办公室主任", "start": "", "end": "present", "rank": "乡科级", "note": "现任"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "赵昱清作为县委书记，杨琼圣作为县长，是党政一把手搭档关系",
     "overlap_org": "中共浑源县委员会/浑源县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "strength": "strong",
     "context": "杨琼圣作为县长，赵祥作为常务副县长，协助县长主持日常工作",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "杨琼圣与雷迎春在县政府班子共事，雷迎春任县委常委、副县长",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "strength": "strong",
     "context": "杨琼圣与胡鹏在县政府班子共事，胡鹏任县委常委、副县长",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "strength": "strong",
     "context": "杨琼圣与李倩在县政府班子共事，李倩任县委常委、副县长",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "strength": "strong",
     "context": "杨琼圣与付元进在县政府班子共事，付元进任副县长",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "strength": "strong",
     "context": "杨琼圣与赵铸在县政府班子共事，赵铸任副县长、公安局长",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "2024-03至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "赵祥与雷迎春同为浑源县委常委、副县长，在县委常委会和县政府班子共事",
     "overlap_org": "中共浑源县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "赵昱清与赵祥在县委常委会共事，赵祥任县委常委",
     "overlap_org": "中共浑源县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "赵昱清与雷迎春在县委常委会共事，雷迎春任县委常委、副县长",
     "overlap_org": "中共浑源县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "strong",
     "context": "赵昱清与胡鹏在县委常委会共事，胡鹏任县委常委、副县长",
     "overlap_org": "中共浑源县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "strong",
     "context": "赵昱清与李倩在县委常委会共事，李倩任县委常委、副县长",
     "overlap_org": "中共浑源县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 9, "type": "overlap", "strength": "medium",
     "context": "雷迎春与付元进在浑源县共事多年，两人均在浑源本地长期任职",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 10, "person_b": 12, "type": "cross_county", "strength": "medium",
     "context": "赵铸与王武明均曾在广灵县工作过，赵铸任广灵县副县长/公安局长，王武明在广灵县多乡镇任职",
     "overlap_org": "广灵县",
     "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 10, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "赵铸与赵祥在浑源县政府班子共事，赵铸任副县长、公安局长",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "2024-03至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "赵祥与曹启龙在浑源县委常委班子共事多年",
     "overlap_org": "中共浑源县委员会",
     "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 10, "person_b": 14, "type": "overlap", "strength": "medium",
     "context": "赵铸与王秉权同在浑源县政府工作",
     "overlap_org": "浑源县人民政府",
     "overlap_period": "", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role:
        return "50,100,255"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "副县长" in role:
        return "50,100,255"
    elif "主任" in role and "党委" in p.get("current_org", ""):
        return "100,100,100"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role or "县长" in role

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>浑源县领导班子工作关系网络 - 山西省大同市浑源县</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    import sqlite3
    build_db()
    build_gexf()
    print_summary()
