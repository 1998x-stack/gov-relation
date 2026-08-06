"""Build SQLite database and GEXF graph for 富川瑶族自治县 leadership network.

富川瑶族自治县隶属广西壮族自治区贺州市，位于广西东北部、湘桂交界，潇贺古道要冲。
县域面积1572平方公里，辖12个乡镇、137个村委、19个社区，总人口约34.38万，
其中瑶族20.15万人（占58.61%）。产业以富川脐橙、华润循环经济产业示范区为特色。

Current leadership as of 2026-08 (sources: 富川瑶族自治县人民政府门户 www.gxfc.gov.cn 官方新闻、
富政发〔2026〕2号政府领导班子分工通知、贺州市人大常委会任免公告):
- 县委书记: 覃焕发
- 县委副书记、代县长: 钟华斗（接替离任的胡德珺）
- 县人大常委会主任: 余青麒；县政协主席: 唐先秋

鉴于外部搜索引擎（Exa/Baidu/Sogou/Bing）本期受限，关键人物出生/籍贯/学历等身份信息
多数未在公开渠道发布，已在 person JSON 与 report/open_gaps.md 中以 confidence 与
open_questions 显式标注，未作臆造。
"""

import os
import sqlite3
import sys
from pathlib import Path

# Locate repo root regardless of where this script sits (scripts/build/ or data/tmp/<task>/)
def _find_repo_root(start: Path) -> Path:
    for p in [start] + list(start.parents):
        if (p / "gov_relation").is_dir() and (p / "data").is_dir():
            return p
    return start

REPO_ROOT = _find_repo_root(Path(__file__).resolve().parent)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "富川瑶族自治县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "富川瑶族自治县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "富川瑶族自治县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "富川瑶族自治县_network.db"
    GEXF_PATH = GRAPH_DIR / "富川瑶族自治县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共富川瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共贺州市委", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 2, "name": "富川瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 3, "name": "富川瑶族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "贺州市人大常委会", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 4, "name": "中国人民政治协商会议富川瑶族自治县委员会", "type": "政协", "level": "县处级", "parent": "政协贺州市委员会", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 5, "name": "富川瑶族自治县纪委监委", "type": "纪委", "level": "县处级", "parent": "贺州市纪委监委", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 6, "name": "中共贺州市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区贺州市"},
    {"id": 7, "name": "贺州市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区贺州市"},
    {"id": 8, "name": "贺州市人大常委会", "type": "人大", "level": "地厅级", "parent": "广西壮族自治区人大常委会", "location": "广西壮族自治区贺州市"},
    {"id": 9, "name": "富川华润循环经济产业示范区管理委员会", "type": "开发区", "level": "县处级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 10, "name": "富川瑶族自治县发展和改革局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 11, "name": "富川瑶族自治县财政局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 12, "name": "富川瑶族自治县审计局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 13, "name": "富川瑶族自治县委办公室", "type": "党委机关", "level": "乡科级", "parent": "中共富川瑶族自治县委员会", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 14, "name": "富川瑶族自治县水利局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 15, "name": "富川瑶族自治县农业农村局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 16, "name": "富川瑶族自治县卫生健康局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 17, "name": "富川瑶族自治县教育局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 18, "name": "富川瑶族自治县自然资源局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 19, "name": "富川瑶族自治县住房和城乡建设局", "type": "事业单位", "level": "乡科级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 20, "name": "富川瑶族自治县政法委员会", "type": "党委机关", "level": "乡科级", "parent": "中共富川瑶族自治县委员会", "location": "广西壮族自治区贺州市富川瑶族自治县"},
    {"id": 21, "name": "广东省肇庆市（粤桂协作挂职）", "type": "党委", "level": "地厅级", "parent": "中共广东省委", "location": "广东省肇庆市"},
    {"id": 22, "name": "来宾市农业农村局", "type": "政府", "level": "地厅级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市"},
    {"id": 23, "name": "来宾市人民政府办公室", "type": "政府", "level": "地厅级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市"},
    {"id": 24, "name": "中共来宾市兴宾区委员会", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市兴宾区"},
    {"id": 25, "name": "中共贺州市八步区委员会", "type": "党委", "level": "县处级", "parent": "中共贺州市委", "location": "广西壮族自治区贺州市八步区"},
    {"id": 26, "name": "中共昭平县委员会", "type": "党委", "level": "县处级", "parent": "中共贺州市委", "location": "广西壮族自治区贺州市昭平县"},
    {"id": 27, "name": "中共贺州市委员会（组织/党建条线）", "type": "党委机关", "level": "地厅级", "parent": "中共贺州市委", "location": "广西壮族自治区贺州市"},
    {"id": 28, "name": "贺州市住房和城乡建设局", "type": "政府", "level": "地厅级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市"},
    {"id": 29, "name": "富川瑶族自治县机构·县直机关", "type": "政府", "level": "县处级", "parent": "富川瑶族自治县人民政府", "location": "广西壮族自治区贺州市富川瑶族自治县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "覃焕发", "gender": "男", "ethnicity": "壮族",
     "birth": "1976年11月", "birthplace": "广西壮族自治区来宾市兴宾区",
     "education": "在职大学本科", "party_join": "2003年10月", "work_start": "1997年8月",
     "current_post": "中共富川瑶族自治县委书记（兼县人武部党委第一书记）", "current_org": "中共富川瑶族自治县委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27975652.shtml"},
    {"id": 2, "name": "钟华斗", "gender": "男", "ethnicity": "瑶族",
     "birth": "1980年9月", "birthplace": "湖南省永州市",
     "education": "大学本科（广西师范大学汉语言文学）", "party_join": "中共党员", "work_start": "1999年9月",
     "current_post": "县委副书记、副县长、代县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27965232.shtml"},
    {"id": 3, "name": "胡德珺", "gender": "男", "ethnicity": "瑶族",
     "birth": "1975年3月", "birthplace": "广西贺州",
     "education": "在职研究生（广西师范大学）", "party_join": "1996年12月", "work_start": "1994年7月",
     "current_post": "原富川县长（2026-07离任，去向待核）", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zcwj/fzf/t27468383.shtml"},
    {"id": 4, "name": "严自喜", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdwknr/zfwj/fzf/t27468383.shtml"},
    {"id": 5, "name": "韦昌平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、县委办公室主任", "current_org": "中共富川瑶族自治县委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27981274.shtml"},
    {"id": 6, "name": "陈绿冬", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委", "current_org": "中共富川瑶族自治县委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27981274.shtml"},
    {"id": 7, "name": "余青麒", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "富川瑶族自治县人民代表大会常务委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27965232.shtml"},
    {"id": 8, "name": "唐先秋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协主席", "current_org": "中国人民政治协商会议富川瑶族自治县委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27965232.shtml"},
    {"id": 9, "name": "李德奎", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 10, "name": "肖艳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 11, "name": "覃秀娟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 12, "name": "朱启军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长（赴广东戴庆职场挂职）", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 13, "name": "汪克承", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 14, "name": "汪微萍", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 15, "name": "谢绿琪", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 16, "name": "薛文亮", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 17, "name": "周呈军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府处级干部", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 18, "name": "邓寿山", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府处级干部", "current_org": "富川瑶族自治县人民政府",
     "source": "http://www.gxfc.gov.cn/zwgk/zfxxgkzl/fdzdgknr/zfwj/fzf/t27468383.shtml"},
    {"id": 19, "name": "陈开勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县领导（常委）", "current_org": "中共富川瑶族自治县委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27965232.shtml"},
    {"id": 20, "name": "叶振坤", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县领导（常委）", "current_org": "中共富川瑶族自治县委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27965232.shtml"},
    {"id": 21, "name": "杨名军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县领导（常委）", "current_org": "中共富川瑶族自治县委员会",
     "source": "http://www.gxfc.gov.cn/xwzx/zhxw/t27965232.shtml"},
    {"id": 22, "name": "尹哲", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年12月", "birthplace": "广西玉林",
     "education": "大学（北京林业大学）、工程硕士（武汉大学）", "party_join": "2005年11月", "work_start": "2002年8月",
     "current_post": "贺州市委副秘书长（原富川县委书记，拟任副厅级）", "current_org": "中共贺州市委员会",
     "source": "http://www.gxhz.gov.cn/"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 覃焕发 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共富川瑶族自治县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作"},
    # 钟华斗 — 代县长（县委副书记）
    {"person_id": 2, "org_id": 1, "title": "富川县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "富川瑶族自治县人民政府代县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "接替离任县长胡德珺"},
    # 胡德珺 — 原县长
    {"person_id": 3, "org_id": 2, "title": "富川瑶族自治县人民政府县长", "start_date": "", "end_date": "2026", "rank": "正处级", "note": "主持县政府全面工作，主管财政局、审计局"},
    # 严自喜 — 常务副县长（常委）
    {"person_id": 4, "org_id": 1, "title": "富川县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管常务工作"},
    # 韦昌平 — 常委/县委办主任
    {"person_id": 5, "org_id": 1, "title": "富川县委常委、县委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈绿冬 — 常委
    {"person_id": 6, "org_id": 1, "title": "富川县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 余青麒 — 人大主任
    {"person_id": 7, "org_id": 3, "title": "富川瑶族自治县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 唐先秋 — 政协主席
    {"person_id": 8, "org_id": 4, "title": "富川瑶族自治县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 县政府班子
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "民族、自然资源、住建、交通、城管、生态"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "东西部（粤桂）协作、工业协管"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "驻村工作队、市场监督、乡村振兴"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "派驻广东肇庆挂职"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "水利、农业农村、乡村振兴、林业"},
    {"person_id": 13, "org_id": 14, "title": "分管县水利局", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "民政、教育、市场监督、文化、卫生"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "政法、退役军人、信访"},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "人社、央企定点帮扶"},
    # 处级干部
    {"person_id": 17, "org_id": 2, "title": "县政府处级干部", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "县政府处级干部", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 其他县领导（常委）
    {"person_id": 19, "org_id": 1, "title": "县委领导（常委）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 1, "title": "县委领导（常委）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 1, "title": "县委领导（常委）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 覃焕发 — 历史履历（来宾→富川）
    {"person_id": 1, "org_id": 24, "title": "兴宾区寺山乡/良江镇/石牙乡（乡镇基层）", "start_date": "", "end_date": "", "rank": "", "note": "寺山乡、良江镇宣传委员/副镇长、石牙乡乡长"},
    {"person_id": 1, "org_id": 23, "title": "来宾市人民政府副秘书长、办公室副主任", "start_date": "", "end_date": "", "rank": "处级", "note": ""},
    {"person_id": 1, "org_id": 22, "title": "来宾市农业农村局党组书记、局长", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "任富川县委书记前的最后职务（跨市交流）"},
    # 胡德珺 — 历史（八步→昭平→富川）
    {"person_id": 3, "org_id": 25, "title": "八步区委常委、组织部部长", "start_date": "", "end_date": "2018", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 26, "title": "昭平县委副书记（党校校长）", "start_date": "2018-07", "end_date": "2021-06", "rank": "副处级", "note": "二级调研员"},
    {"person_id": 3, "org_id": 2, "title": "富川县委副书记、县政府党组书记、县长", "start_date": "2021-07", "end_date": "2026-07", "rank": "正处级", "note": "2026-07离任，去向待核"},
    # 钟华斗 — 历史（贺州市直→富川代县长）
    {"person_id": 2, "org_id": 25, "title": "八步区仁义镇干部/政府办公文", "start_date": "2007", "end_date": "~2014", "rank": "", "note": "公务员"},
    {"person_id": 2, "org_id": 27, "title": "历任市委党建办主任、市委副秘书长、组织部分管日常工作副部长", "start_date": "", "end_date": "", "rank": "处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、副县长、代县长", "start_date": "2026-07-22", "end_date": "present", "rank": "（代）正处级", "note": "十届人大43次会议决定"},
    # 严自喜 — 历史
    {"person_id": 4, "org_id": 28, "title": "贺州市住房和城乡建设局党组成员、副局长", "start_date": "2022-03", "end_date": "", "rank": "处级", "note": ""},
    # 尹哲 — 前任书记
    {"person_id": 22, "org_id": 1, "title": "富川县委书记（2021.07-2026）", "start_date": "2021-07", "end_date": "2026-06", "rank": "正处级", "note": "华润循环经济产业示范区工委书记兼"},
    {"person_id": 22, "org_id": 6, "title": "贺州市委副秘书长（正处级）", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "拟任设区市副厅级领导职务"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职出口
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与代县长党政正职搭档，共同调研华润园区、文旅项目", "overlap_org": "中共富川瑶族自治县委员会/富川县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "覃焕发任书记期间，胡德珺任县长（党政共治），2026 年胡德珺离任", "overlap_org": "富川瑶族自治县", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "胡德珺辞任县长，由钟华斗接任代县长", "overlap_org": "富川瑶族自治县人民政府", "overlap_period": "2026"},
    # 县委班子
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与常委、常务副县长严自喜共事", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与县委办主任韦昌平", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "代县长与县委办主任", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与县委常委陈绿冬", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "代县长与县委常委陈绿冬", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    # 政府班子
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "代县长与常务副县长严自喜", "overlap_org": "富川瑶族自治县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "原县长与常务副县长严自喜共事", "overlap_org": "富川瑶族自治县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记与副县长汪克承 防汛现场党政联动", "overlap_org": "富川瑶族自治县", "overlap_period": "2026-07"},
    # 人大/政协
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与县人大常委会主任余青麒（四家班子）", "overlap_org": "富川瑶族自治县", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与县政协主席唐先秋", "overlap_org": "富川瑶族自治县", "overlap_period": "current"},
    # 四大班子同场（八一慰问）
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "人大主任与政协主席共同出席八一慰问", "overlap_org": "富川瑶族自治县", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "书记与县领导陈开勇", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "书记与县领导叶振坤", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 21, "type": "overlap", "context": "书记与县领导杨名军", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "current"},
    # 粤桂协作跨省挂职
    {"person_a": 12, "person_b": 21, "type": "overlap", "context": "朱启军副县长赴广东肇庆粤桂协作挂职", "overlap_org": "粤桂协作挂职通道", "overlap_period": "current"},
    # 书记交接（尹哲→覃焕发）
    {"person_a": 22, "person_b": 1, "type": "predecessor_successor", "context": "尹哲2021-2026任富川县委书记，2026年6月由覃焕发接任（跨市交流）", "overlap_org": "中共富川瑶族自治县委员会", "overlap_period": "2026"},
    # 县长交接（胡德珺→钟华斗）
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "胡德珺2021-2026任县长，2026-07-22由钟华斗接任代县长", "overlap_org": "富川瑶族自治县人民政府", "overlap_period": "2026"},
    # 尹哲与胡德珺曾共治（党政搭档）
    {"person_a": 22, "person_b": 3, "type": "overlap", "context": "尹哲任书记、胡德珺任县长，并同任华润循环经济产业示范区工委书记/主任", "overlap_org": "中共富川县委/富川县政府/华润示范区", "overlap_period": "2021-2024"},
    # 覃焕发（书记）与汪克承（副县长）— 防汛现场党政联动
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "覃焕发率队防汛，副县长汪克承陪同", "overlap_org": "富川瑶族自治县", "overlap_period": "2026-07"},
    # 常务副县长与县委办（政班子）条线
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "常务副县长严自喜与县委办主任韦昌平（县委党政办条线）", "overlap_org": "中共富川县委", "overlap_period": "current"},
]

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
    print("Build complete:", DB_PATH)
    print("GEXF:", GEXF_PATH)