#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 凤山县 leadership network.

凤山县隶属广西壮族自治区河池市，位于广西西北部，是"世界地质公园"乐业—凤山世界地质公园所在县。
经济以桑蚕、八角、油茶、林下经济等特色农林产业为主，为国家乡村振兴重点帮扶县。

Current leadership as of 2026-08 (sources: 自治区党委组织部任前公示、广西县域经济网、河池市任前公示系列):
- 县委书记: 班华任（2026年起，接杨胜涛任凤山县县长后升任书记）
- 县委副书记、县长: 苏镭（2026-06公示拟提名为县长候选人）

县委书记更替：黄德意 → 廖锦成(2012.11-2020.07, 落马) → 薛海源(2020.08-2023.08) → 杨胜涛(2023.10-2026) → 班华任(2026-)

Biographical data sourced from official appointment notices (任前公示) and mainstream media.
Confidence marked per person (见 report 与 open_gaps.md)。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "凤山县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "凤山县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "凤山县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "凤山县_network.db"
    GEXF_PATH = GRAPH_DIR / "凤山县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共凤山县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市凤山县"},
    {"id": 2, "name": "凤山县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市凤山县"},
    {"id": 3, "name": "凤山县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "河池市人大常委会", "location": "广西壮族自治区河池市凤山县"},
    {"id": 4, "name": "中国人民政治协商会议凤山县委员会", "type": "政协", "level": "县处级", "parent": "政协河池市委员会", "location": "广西壮族自治区河池市凤山县"},
    {"id": 5, "name": "中共凤山县纪律检查委员会/凤山县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共河池市纪委", "location": "广西壮族自治区河池市凤山县"},
    {"id": 6, "name": "中共河池市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区河池市"},
    {"id": 7, "name": "河池市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区河池市"},
    {"id": 8, "name": "河池市水产技术推广站", "type": "事业单位", "level": "", "parent": "河池市农业农村局", "location": "广西壮族自治区河池市"},
    {"id": 9, "name": "中共河池市委办公室", "type": "党委", "level": "地厅级", "parent": "中共河池市委", "location": "广西壮族自治区河池市"},
    {"id": 10, "name": "河池市人民政府办公室", "type": "政府", "level": "地厅级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市"},
    {"id": 11, "name": "中共宜州市委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市宜州市"},
    {"id": 12, "name": "宜州市人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市宜州市"},
    {"id": 13, "name": "中共宜州区委/宜州区委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市宜州区"},
    {"id": 14, "name": "河池市教育局", "type": "政府", "level": "地厅级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市"},
    {"id": 15, "name": "中共大化瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市大化瑶族自治县"},
    {"id": 16, "name": "大化瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市大化瑶族自治县"},
    {"id": 17, "name": "中共天峨县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市天峨县"},
    {"id": 18, "name": "天峨县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市天峨县"},
    {"id": 19, "name": "中共宜州市委组织部", "type": "党委部门", "level": "县处级", "parent": "中共宜州市委", "location": "广西壮族自治区河池市宜州市"},
    {"id": 20, "name": "中共广西壮族自治区委员会组织部", "type": "党委部门", "level": "省部级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区南宁市"},
    # 21 — 中国乐业—凤山世界地质公园管理委员会
    {"id": 21, "name": "中国乐业—凤山世界地质公园管理委员会", "type": "事业单位", "level": "正处级", "parent": "凤山县人民政府", "location": "广西壮族自治区河池市凤山县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 班华任 — 县委书记（现任）
    {"id": 1, "name": "班华任", "gender": "男", "ethnicity": "壮族",
     "birth": "1975年4月", "birthplace": "广西壮族自治区河池市东兰县",
     "education": "广西大学淡水渔业专业农学学士，广西区委党校在职研究生公共管理专业",
     "party_join": "1997年6月加入中国共产党", "work_start": "1997年7月参加工作",
     "current_post": "中共凤山县委书记", "current_org": "中共凤山县委员会",
     "source": "http://www.gxcounty.com/zhengwu/rsrm/180318.html"},
    # 2 — 苏镭 — 县长（现任）
    {"id": 2, "name": "苏镭", "gender": "男", "ethnicity": "瑶族",
     "birth": "1984年1月", "birthplace": "广西壮族自治区河池市大化瑶族自治县",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县委副书记、县人民政府县长", "current_org": "凤山县人民政府",
     "source": "http://gx.news.cn/20260618/0a84d36cc0dc439b9f49f5513303506f/c.html"},
    # 3 — 廖锦成 — 前任县委书记（2012.11-2020.07，落马）
    {"id": 3, "name": "廖锦成", "gender": "男", "ethnicity": "壮族",
     "birth": "1965年8月", "birthplace": "广西壮族自治区河池市罗城仫佬族自治县",
     "education": "",
     "party_join": "1992年6月加入中国共产党", "work_start": "",
     "current_post": "凤山县原县委书记（2020年落马被开除党籍）", "current_org": "中共凤山县委员会",
     "source": "https://www.gxjjw.gov.cn/"},
    # 4 — 薛海源 — 前任县委书记（2020.08-2023.08）
    {"id": 4, "name": "薛海源", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "河池市宜州区委书记", "current_org": "中共宜州区委",
     "source": "http://gx.news.cn/"},
    # 5 — 杨胜涛 — 前任县委书记（2023.06-2026）
    {"id": 5, "name": "杨胜涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年4月", "birthplace": "广西壮族自治区河池市天峨县",
     "education": "在职研究生学历，管理学学士",
     "party_join": "1997年6月加入中国共产党", "work_start": "",
     "current_post": "凤山县原县委书记（2026年调离）", "current_org": "中共凤山县委员会",
     "source": "http://www.gxcounty.com/zhengwu/zjyl/180319.html"},
    # 6 — 黄德意 — 更前任县委书记
    {"id": 6, "name": "黄德意", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县原县委书记（更早前任）", "current_org": "中共凤山县委员会",
     "source": "http://gx.news.cn/"},
    # 7 — 黄玉广 — 县委常委、纪委书记、监委主任
    {"id": 7, "name": "黄玉广", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县委常委、纪委书记、监委主任", "current_org": "中共凤山县纪律检查委员会",
     "source": "http://gx.news.cn/"},
    # 8 — 黄德先 — 县委常委、办公室主任
    {"id": 8, "name": "黄德先", "gender": "男", "ethnicity": "壮族",
     "birth": "1974年12月", "birthplace": "广西壮族自治区凤山县",
     "education": "在职大学",
     "party_join": "2001年5月加入中国共产党", "work_start": "",
     "current_post": "凤山县委常委、县委办公室主任", "current_org": "中共凤山县委员会",
     "source": "http://gx.news.cn/"},
    # 9 — 韦永健 — 凤山县委常委、统战部部长、副县长（部分来源亦写作"韦湘湘"）
    {"id": 9, "name": "韦永健", "gender": "女", "ethnicity": "毛南族",
     "birth": "1980年2月", "birthplace": "广西壮族自治区河池市东兰县",
     "education": "在职研究生",
     "party_join": "2001年10月加入中国共产党", "work_start": "1999年10月参加工作",
     "current_post": "凤山县委常委、统战部部长、副县长", "current_org": "凤山县人民政府",
     "source": "http://gx.news.cn/"},
    # 10 — 覃欢 — 凤山县委常委、政法委书记
    {"id": 10, "name": "覃欢", "gender": "男", "ethnicity": "壮族",
     "birth": "1977年10月", "birthplace": "广西壮族自治区河池市大化县",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县委常委、政法委书记", "current_org": "中共凤山县委员会",
     "source": "http://gx.news.cn/"},
    # 11 — 罗帆 — 凤山县委常委、宣传部部长
    {"id": 11, "name": "罗帆", "gender": "男", "ethnicity": "壮族",
     "birth": "1977年12月", "birthplace": "广西壮族自治区凤山",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "1997年12月出生（原文如此）",
     "current_post": "凤山县委常委、宣传部部长", "current_org": "中共凤山县委员会",
     "source": "http://gx.news.cn/"},
    # 12 — 罗国照 — 凤山县人大常委会主任
    {"id": 12, "name": "罗国照", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县人大常委会主任", "current_org": "凤山县人民代表大会常务委员会",
     "source": "http://gx.news.cn/"},
    # 13 — 韦海涛 — 凤山县政协主席
    {"id": 13, "name": "韦海涛", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县政协主席", "current_org": "中国人民政治协商会议凤山县委员会",
     "source": "http://gx.news.cn/"},
    # 14 — 潘玉香 — 中国乐业—凤山世界地质公园管理委员会主任, 原凤山县常委、副县长
    {"id": 14, "name": "潘玉香", "gender": "女", "ethnicity": "瑶族",
     "birth": "1979年11月", "birthplace": "广西壮族自治区河池市大化县",
     "education": "大学农学学士",
     "party_join": "2001年10月加入中国共产党", "work_start": "",
     "current_post": "中国乐业—凤山世界地质公园管理委员会主任（原凤山县常委、副县长）", "current_org": "中国乐业—凤山世界地质公园管理委员会",
     "source": "http://gx.news.cn/"},
    # 15 — 周尚启 — 常委（2023-11会议名单中）
    {"id": 15, "name": "周尚启", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县委常委（2023-11会议名单中）", "current_org": "中共凤山县委员会",
     "source": "http://gx.news.cn/"},
    # 16 — 黄黎婉 — 常委（2023-11会议名单中）
    {"id": 16, "name": "黄黎婉", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县委常委（2023-11会议名单中）", "current_org": "中共凤山县委员会",
     "source": "http://gx.news.cn/"},
    # 17 — 万选理 — 常委（2023-11会议名单中）
    {"id": 17, "name": "万选理", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤山县委常委（2023-11会议名单中）", "current_org": "中共凤山县委员会",
     "source": "http://gx.news.cn/"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 班华任
    {"person_id": 1, "org_id": 1, "title": "凤山县委书记", "start": "2026", "end": "present", "rank": "正处级", "note": "2026-06-17任前公示拟任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "凤山县委副书记、县长", "start": "2023-10", "end": "2026", "rank": "正处级", "note": "接杨胜涛任凤山县县长"},
    {"person_id": 1, "org_id": 14, "title": "河池市教育局局长", "start": "2021-07", "end": "2023-10", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "宜州区委副书记", "start": "2017-11", "end": "2021-07", "rank": "副处级", "note": "2017县级改为宜州区"},
    {"person_id": 1, "org_id": 12, "title": "宜州市委常委、常务副市长", "start": "2015", "end": "2017-11", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "宜州市委常委、组织部部长", "start": "2011", "end": "2015", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "河池市人民政府办公室/督查室干部", "start": "2009-01", "end": "2011", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "河池市委办公室干部", "start": "2003-08", "end": "2009-01", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "河池市水产技术推广站干部", "start": "1997", "end": "2003-08", "rank": "", "note": "1997年7月参加工作起步"},
    # 苏镭
    {"person_id": 2, "org_id": 2, "title": "凤山县委副书记、县长", "start": "2026", "end": "present", "rank": "正处级", "note": "2026-06-17任前公示拟提名为县长候选人"},
    {"person_id": 2, "org_id": 2, "title": "凤山县常委、副县长（常务）", "start": "", "end": "2026", "rank": "副处级", "note": "常务副县长"},
    {"person_id": 2, "org_id": 16, "title": "大化县基层（乡镇）干部", "start": "", "end": "", "rank": "", "note": "大化县基层乡镇起步"},
    # 廖锦成
    {"person_id": 3, "org_id": 1, "title": "凤山县委书记", "start": "2012-11", "end": "2020-07", "rank": "正处级", "note": "2020年落马被开除党籍"},
    # 薛海源
    {"person_id": 4, "org_id": 1, "title": "凤山县委书记", "start": "2020-08", "end": "2023-08", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 13, "title": "河池宜州区委书记", "start": "2023-08", "end": "present", "rank": "正处级", "note": "调任"},
    # 杨胜涛
    {"person_id": 5, "org_id": 1, "title": "凤山县委书记", "start": "2023-10", "end": "2026", "rank": "正处级", "note": "2026年调离"},
    # 黄德意
    {"person_id": 6, "org_id": 1, "title": "凤山县委书记", "start": "", "end": "", "rank": "正处级", "note": "更早前任，履历待查"},
    # 黄玉广
    {"person_id": 7, "org_id": 5, "title": "凤山县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 黄德先
    {"person_id": 8, "org_id": 1, "title": "凤山县委常委、办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 韦永健/韦湘湘
    {"person_id": 9, "org_id": 1, "title": "凤山县委常委、统战部部长", "start": "2024-12", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "凤山县政府副县长（兼）", "start": "2024-12", "end": "present", "rank": "副处级", "note": ""},
    # 覃欢
    {"person_id": 10, "org_id": 1, "title": "凤山县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 罗帆
    {"person_id": 11, "org_id": 1, "title": "凤山县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 罗国照
    {"person_id": 12, "org_id": 3, "title": "凤山县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 韦海涛
    {"person_id": 13, "org_id": 4, "title": "凤山县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 潘玉香
    {"person_id": 14, "org_id": 1, "title": "凤山县委常委、副县长（原常委）", "start": "", "end": "", "rank": "副处级", "note": "原任"},
    {"person_id": 14, "org_id": 21, "title": "中国乐业—凤山世界地质公园管理委员会主任", "start": "", "end": "present", "rank": "正处级", "note": "管委会主任"},
    # 周尚启
    {"person_id": 15, "org_id": 1, "title": "凤山县委常委", "start": "2023-11", "end": "present", "rank": "副处级", "note": "2023-11会议名单中"},
    # 黄黎婉
    {"person_id": 16, "org_id": 1, "title": "凤山县委常委", "start": "2023-11", "end": "present", "rank": "副处级", "note": "2023-11会议名单中"},
    # 万选理
    {"person_id": 17, "org_id": 1, "title": "凤山县委常委", "start": "2023-11", "end": "present", "rank": "副处级", "note": "2023-11会议名单中"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "班华任（县委书记）与苏镭（县长）为凤山县现任党政主要一把手，同一班子共事", "overlap_org": "凤山县", "overlap_period": "2026至今"},
    {"person_a": 5, "person_b": 1, "type": "predecessor_successor", "context": "杨胜涛为班华任的直接前任凤山县委书记", "overlap_org": "凤山县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "班华任于2023年接杨胜涛任凤山县县长，两人曾共事", "overlap_org": "凤山县", "overlap_period": "2023-2026"},
    {"person_a": 4, "person_b": 5, "type": "predecessor_successor", "context": "薛海源卸任凤山县委书记由杨胜涛接任", "overlap_org": "凤山县", "overlap_period": "2023"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "廖锦成卸任风山县委书记由薛海源接任", "overlap_org": "凤山县", "overlap_period": "2020"},
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "苏镭任凤山县常务副县长时期，班华任任凤山县长（上下级）", "overlap_org": "凤山县", "overlap_period": "2023-2026"},
    {"person_a": 5, "person_b": 2, "type": "上下级", "context": "杨胜涛书记任内苏镭任凤山县常委/副县长", "overlap_org": "凤山县", "overlap_period": "2023-2026"},
    {"person_a": 4, "person_b": 14, "type": "上下级", "context": "薛海源书记任内潘玉香任凤山县常委副县长", "overlap_org": "凤山县", "overlap_period": "2020-2023"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "班华任现任书记与县委班子共事（统战部长等常委）", "overlap_org": "凤山县", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "班华任任书记与县纪委书记黄玉广共事", "overlap_org": "凤山县", "overlap_period": "2026至今"},
    {"person_a": 5, "person_b": 12, "type": "上下级", "context": "杨胜涛任书记时罗国照任凤山县人大主任", "overlap_org": "凤山县", "overlap_period": "2023-2026"},
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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")