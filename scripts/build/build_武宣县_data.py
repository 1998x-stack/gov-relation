#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 武宣县 leadership network.

武宣县隶属广西壮族自治区来宾市，位于广西中部，北回归线上，别称"仙城"，系太平天国西王萧朝贵故乡、
桂中最早建立农村党组织的革命老区。辖 9 镇 1 乡，总人口约 45.28 万人，是国家糖料蔗基地县、
中国长寿之乡、广西高质量发展进步县，当前锚定"滨湖新城·大美武宣"，建设"三城三区"、打造出海
"双通道"重要节点城市。

现任班子（as of 2026-08，来源：武宣县人民政府门户 www.wuxuan.gov.cn 领导车站/武宣要闻/政务任免）：
- 县委书记: 谭小春（2026-04-30 自治区党委批准任命；2026-07-30 十四届县委一次全会再度当选）
- 县委副书记、县长: 钟宏珊（2024-09-14 当选）
- 县委副书记: 张波（2026-07-30 十四届一次全会当选）
- 县人大常委会主任: 莫红兵
- 县政协主席: 吴海音
下辖副县长7人（官网"副县长"栏目）；部分常委会成员职务信息尚待官方细分页补全（已标注为 open gaps）。

书记更迭：雷应天（前任，于2026-04-30 前调离）→ 谭小春（2026-04-30—今）。
身份/履历细节对部分成员未知，按 open gaps 编码，不以编造填充。
"""

import os
import sqlite3  # noqa: F401  (referenced by process_tmp.py build-script validation)
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

SLUG = "武宣县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "武宣县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "武宣县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "武宣县_network.db"
    GEXF_PATH = GRAPH_DIR / "武宣县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共武宣县委员会", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 2, "name": "武宣县人民政府", "type": "政府", "level": "县处级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 3, "name": "武宣县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "来宾市人大常委会", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 4, "name": "中国人民政治协商会议武宣县委员会", "type": "政协", "level": "县处级", "parent": "政协来宾市委员会", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 5, "name": "中共武宣县纪律检查委员会/武宣县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共来宾市纪委", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 6, "name": "中共武宣县委组织部", "type": "党委部门", "level": "县处级", "parent": "中共武宣县委", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 7, "name": "武宣县人民武装部", "type": "党委部门", "level": "县处级", "parent": "中共武宣县委/来宾军分区", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 8, "name": "武宣县公安局", "type": "政府机构", "level": "县处级", "parent": "武宣县人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 9, "name": "武宣县人民政府办公室", "type": "政府机构", "level": "县处级", "parent": "武宣县人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 10, "name": "武宣县财政局", "type": "政府机构", "level": "县处级", "parent": "武宣县人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 11, "name": "武宣县审计局", "type": "政府机构", "level": "县处级", "parent": "武宣县人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 12, "name": "武宣县三江口新区（武宣片区）开发建设", "type": "开发区", "level": "县处级", "parent": "武宣县人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 13, "name": "广西仙城投资发展集团有限公司", "type": "国有企业", "level": "县处级", "parent": "武宣县人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 14, "name": "武宣县大藤峡水利枢纽工程移民安置(水库和扶贫易地安置中心)", "type": "政府机构", "level": "县处级", "parent": "武宣县人民政府", "location": "广西壮族自治区来宾市武宣县"},
    {"id": 15, "name": "中共来宾市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区来宾市"},
    {"id": 16, "name": "中共来宾市委组织部", "type": "党委部门", "level": "地厅级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市"},
    {"id": 17, "name": "合山市人民政府", "type": "政府", "level": "县处级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市合山市"},
    {"id": 18, "name": "中共柳州市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区柳州市"},
    {"id": 19, "name": "柳州市城中区（区政府）", "type": "政府", "level": "地厅级", "parent": "柳州市人民政府", "location": "广西壮族自治区柳州市城中区"},
    {"id": 20, "name": "鹿寨县人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府", "location": "广西壮族自治区柳州市鹿寨县"},
    {"id": 21, "name": "柳州市行政审批局", "type": "政府机构", "level": "地厅级", "parent": "柳州市人民政府", "location": "广西壮族自治区柳州市"},
    {"id": 22, "name": "中共广西壮族自治区委员会", "type": "党委", "level": "省部级", "parent": "中国共产党中央委员会", "location": "广西壮族自治区南宁市"},
    {"id": 23, "name": "广西壮族自治区人民政府", "type": "政府", "level": "省部级", "parent": "国务院", "location": "广西壮族自治区南宁市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 谭小春 — 县委书记（现任）
    {"id": 1, "name": "谭小春", "gender": "男", "ethnicity": "瑶族",
     "birth": "", "birthplace": "",
     "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共武宣县委书记", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27536747.shtml"},
    # 2 — 钟宏珊 — 县长（现任）
    {"id": 2, "name": "钟宏珊", "gender": "女", "ethnicity": "汉族",
     "birth": "1983年6月", "birthplace": "广西柳州",
     "education": "研究生（管理学硕士）",
     "party_join": "2004年4月", "work_start": "2007年7月",
     "current_post": "武宣县委副书记、县长", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/xz/"},
    # 3 — 张波 — 县委副书记（现任）
    {"id": 3, "name": "张波", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县委副书记", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27971050.shtml"},
    # 4 — 雷应天 — 前任县委书记
    {"id": 4, "name": "雷应天", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县原县委书记（2026-04离任）", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/"},
    # 5 — 拉邦余 — 县委常委、常务副县长
    {"id": 5, "name": "覃邦余", "gender": "男", "ethnicity": "壮族",
     "birth": "1983年8月", "birthplace": "", "education": "博士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县委常委、常务副县长", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/fxz/t19274444.shtml"},
    # 6 — 邱海天 — 县委常委、副县长
    {"id": 6, "name": "邱海天", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年9月", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县委常委、副县长/广西驻村工作队武宣县工作队队长", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/fxz/t22512178.shtml"},
    # 7 — 甘昕熠 — 副县长、公安局局长
    {"id": 7, "name": "甘昕熠", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年10月", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县人民政府副县长、公安局局长", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/fxz/t18055319.shtml"},
    # 8 — 梁济谞 — 副县长
    {"id": 8, "name": "梁济谞", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年12月", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县人民政府副县长", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/fxz/t27957593.shtml"},
    # 9 — 余佩兰 — 副县长
    {"id": 9, "name": "余佩兰", "gender": "女", "ethnicity": "汉族",
     "birth": "1978年12月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县人民政府副县长", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/fxz/t8064094.shtml"},
    # 10 — 曹智媛 — 副县长
    {"id": 10, "name": "曹智媛", "gender": "女", "ethnicity": "汉族",
     "birth": "1980年1月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县人民政府副县长", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/fxz/t10380396.shtml"},
    # 11 — 欧阳铁铸 — 县政府党组成员
    {"id": 11, "name": "欧阳铁铸", "gender": "男", "ethnicity": "汉族",
     "birth": "1990年4月", "birthplace": "", "education": "研究生（农业推广硕士）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县人民政府党组成员", "current_org": "武宣县人民政府",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/fxz/t9578777.shtml"},
    # 12 — 覃华东 — 县政府办公室主任
    {"id": 12, "name": "覃华东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县人民政府办公室主任", "current_org": "武宣县人民政府办公室",
     "source": "http://www.wuxuan.gov.cn/xxgk/ldjj/bgszr/"},
    # 13 — 莫红兵 — 县人大常委会主任
    {"id": 13, "name": "莫红兵", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县人大常委会主任", "current_org": "武宣县人民代表大会常务委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27536747.shtml"},
    # 14 — 吴海音 — 县政协主席
    {"id": 14, "name": "吴海音", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县政协主席", "current_org": "中国人民政治协商会议武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27536747.shtml"},
    # 15 — 甘永辉 — 来宾市委常委、组织部部长（宣布任命）
    {"id": 15, "name": "甘永辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "来宾市委常委、组织部部长", "current_org": "中共来宾市委组织部",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27536747.shtml"},
    # 16 — 蒙家贺 — 县四家班子领导（十四届县委常委会成员）
    {"id": 16, "name": "蒙家贺", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县四家班子领导（县委常委会成员）", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27971050.shtml"},
    # 17 — 林子 — 县四家班子领导（县委常委会成员）
    {"id": 17, "name": "林子", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县四家班子领导（县委常委会成员）", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27971050.shtml"},
    # 18 — 陈周全 — 县四家班子领导（县委常委会成员）
    {"id": 18, "name": "陈周全", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县四家班子领导（县委常委会成员）", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27971050.shtml"},
    # 19 — 覃冬莲 — 县四家班子领导（县委常委会成员）
    {"id": 19, "name": "覃冬莲", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县四家班子领导（县委常委会成员）", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27971050.shtml"},
    # 20 — 李红恩 — 县四家班子领导（县委常委会成员）
    {"id": 20, "name": "李红恩", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县四家班子领导（县委常委会成员）", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27971050.shtml"},
    # 21 — 廖海山 — 县四家班子领导（县委常委会成员）
    {"id": 21, "name": "廖海山", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宣县四家班子领导（县委常委会成员）", "current_org": "中共武宣县委员会",
     "source": "http://www.wuxuan.gov.cn/xwzx/wxyw/t27971050.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 谭小春（县委书记）
    {"person_id": 1, "org_id": 1, "title": "武宣县委书记", "start": "2026-04-30", "end": "present", "rank": "正处级", "note": "2026-04-30 干部大会宣布，自治区党委批准；2026-07-30十四届县委一次全会当选"},
    {"person_id": 1, "org_id": 17, "title": "合山市人民政府市长", "start": "2021-08", "end": "约2026-04", "rank": "正处级", "note": "2021-08 合山市十届人大一次会议当选；跨县域交流：合山→武宣"},
    {"person_id": 1, "org_id": 7, "title": "武宣县人武部党委第一书记", "start": "2026-05-22", "end": "present", "rank": "", "note": "来宾军分区政委莫凌波于2026-05-22宣读"},
    # 钟宏珊(县长)
    {"person_id": 2, "org_id": 2, "title": "武宣县人民政府县长", "start": "2024-09-14", "end": "present", "rank": "正处级", "note": "2024-09-14 当选"},
    {"person_id": 2, "org_id": 1, "title": "武宣县委副书记", "start": "2024-07", "end": "present", "rank": "副处级", "note": "2024-07 任县委副书记、代理县长；2026-07-30 十四届一次全会当选县委副书记"},
    {"person_id": 2, "org_id": 21, "title": "柳州市行政审批局局长", "start": "2023-08", "end": "2024-08", "rank": "正处级", "note": "跨县域培养"},
    {"person_id": 2, "org_id": 20, "title": "鹿寨县委常委、组织部部长、副县长", "start": "约2018", "end": "2023-08", "rank": "副处级", "note": "柳州→鹿寨"},
    {"person_id": 2, "org_id": 19, "title": "柳州市城中区（含街道/区政府）", "start": "2007-07", "end": "约2018", "rank": "", "note": "起步于柳州城中区"},
    # 张波(县委副书记)
    {"person_id": 3, "org_id": 1, "title": "武宣县委副书记", "start": "2026-07-30", "end": "present", "rank": "副处级", "note": "十四届县委一次全会当选"},
    # 雷应天(前任县委书记)
    {"person_id": 4, "org_id": 1, "title": "武宣县委书记（前任）", "start": "约2021", "end": "2026-04-30", "rank": "正处级", "note": "谭小春2026-04-30接任"},
    # 覃邦余(常务副县长)
    {"person_id": 5, "org_id": 2, "title": "武宣县委常委、常务副县长", "start": "", "end": "present", "rank": "副县处级", "note": "负责政府常务、发改、财政（协助）、应急、统计、重大项目、三江口新区(武宣片区)开发"},
    # 邱海天(常委、副县长)
    {"person_id": 6, "org_id": 2, "title": "武宣县委常委、副县长", "start": "", "end": "present", "rank": "副县处级", "note": "广西驻村工作队武宣县工作队队长；水利/卫健/医保"},
    # 甘昕熠(副县长、公安局长)
    {"person_id": 7, "org_id": 2, "title": "武宣县人民政府副县长", "start": "", "end": "present", "rank": "副县处级", "note": "负责政法/法制/国安"},
    {"person_id": 7, "org_id": 8, "title": "武宣县公安局党委书记、局长", "start": "", "end": "present", "rank": "", "note": "主持公安全面工作"},
    # 梁济谞(副县长)
    {"person_id": 8, "org_id": 2, "title": "武宣县人民政府副县长", "start": "", "end": "present", "rank": "副县处级", "note": "市场监管/交通/林业"},
    # 余佩兰(副县长)
    {"person_id": 9, "org_id": 2, "title": "武宣县人民政府副县长", "start": "", "end": "present", "rank": "副县处级", "note": "乡村振兴/教育/文旅/农业农村"},
    # 曹智媛(副县长)
    {"person_id": 10, "org_id": 2, "title": "武宣县人民政府副县长", "start": "", "end": "present", "rank": "副县处级", "note": "工信/商务/科技/招商/人社/生态"},
    # 欧阳铁铸(县政府党组成员)
    {"person_id": 11, "org_id": 2, "title": "武宣县人民政府党组成员", "start": "", "end": "present", "rank": "副县处级", "note": "自然资源/住建/民政/退役"},
    # 覃华东(县政府办主任)
    {"person_id": 12, "org_id": 9, "title": "武宣县人民政府办公室主任", "start": "", "end": "present", "rank": "科处级", "note": ""},
    # 莫红兵(人大主任)
    {"person_id": 13, "org_id": 3, "title": "武宣县人大常委会主任", "start": "", "end": "present", "rank": "正县处级", "note": "2026-04-30 在县干部大会主席台"},
    # 吴海音(政协主席)
    {"person_id": 14, "org_id": 4, "title": "武宣县政协主席", "start": "", "end": "present", "rank": "正县处级", "note": "2026-04-30 在县干部大会主席台"},
    # 甘永辉(来宾组织部部长，宣布任命)
    {"person_id": 15, "org_id": 16, "title": "来宾市委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": "2026-04-30 宣读谭小春任命"},
    # 蒙家贺/林子/陈周全/覃冬莲/李红恩/廖海山(领导班子成员)
    {"person_id": 16, "org_id": 1, "title": "武宣县班子领导（县委常委会成员）", "start": "2026-07-30", "end": "present", "rank": "县处级", "note": "十四大前排就座"},
    {"person_id": 17, "org_id": 1, "title": "武宣县班子领导（县委常委会成员）", "start": "2026-07-30", "end": "present", "rank": "县处级", "note": "十四大前排就座"},
    {"person_id": 18, "org_id": 1, "title": "武宣县班子领导（县委常委会成员）", "start": "2026-07-30", "end": "present", "rank": "县处级", "note": "十四大前排就座"},
    {"person_id": 19, "org_id": 1, "title": "武宣县班子领导（县委常委会成员）", "start": "2026-07-30", "end": "present", "rank": "县处级", "note": "十四大前排就座"},
    {"person_id": 20, "org_id": 1, "title": "武宣县班子领导（县委常委会成员）", "start": "2026-07-30", "end": "present", "rank": "县处级", "note": "十四大前排就座"},
    {"person_id": 21, "org_id": 1, "title": "武宣县班子领导（县委常委会成员）", "start": "2026-07-30", "end": "present", "rank": "县处级", "note": "十四大前排就座"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "谭小春（县委书记）与钟宏珊（县长）为武宣县现任党政一把手，同一班子共事", "overlap_org": "武宣县", "overlap_period": "2026-04至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "谭小春任书记与县委副书记张波共事（县委常委会）", "overlap_org": "武宣县", "overlap_period": "2026-07至今"},
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "雷应天为谭小春的直接前任武宣县委书记，2026-04-30 干部大会宣布由谭小春接任", "overlap_org": "武宣县", "overlap_period": "2026-04-30"},
    {"person_a": 1, "person_b": 13, "type": "同班子", "context": "谭小春任书记与县人大主任莫红兵共事（县四家班子）", "overlap_org": "武宣县", "overlap_period": "2026-04至今"},
    {"person_a": 1, "person_b": 14, "type": "同班子", "context": "谭小春任书记与县政协主席吴海音共事（县四家班子）", "overlap_org": "武宣县", "overlap_period": "2026-04至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "钟宏珊县长与常务副县长覃邦余共事（县政府班子）", "overlap_org": "武宣县", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "钟宏珊县长与副县长邱海天共事（县政府班子）", "overlap_org": "武宣县", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "钟宏珊县长与副县长/公安局长甘昕华共事（县政府班子）", "overlap_org": "武宣县", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 15, "type": "组织任命", "context": "来宾市委组织部部长甘永辉2026-04-30宣布谭小春任武宣县委书记决定", "overlap_org": "中共来宾市委组织部/武宣县", "overlap_period": "2026-04-30"},
    {"person_a": 1, "person_b": 16, "type": "同班子", "context": "谭小春与县委常委会成员蒙家郢共事", "overlap_org": "武宣县", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 21, "type": "同机构任职", "context": "钟宏珊曾任柳州市行政审批局局长，属柳州市（跨市厘升）", "overlap_org": "柳州市行政审批局", "overlap_period": "2023-08~2024-08"},
    {"person_a": 2, "person_b": 20, "type": "同机构任职", "context": "钟宏珊曾任鹿寨县委常委、组织部部长、副县长", "overlap_org": "鹿寨县人民政府", "overlap_period": "约2018~2023-08"},
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