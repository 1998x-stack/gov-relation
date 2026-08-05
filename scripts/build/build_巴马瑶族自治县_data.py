#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 巴马瑶族自治县 leadership network.

巴马瑶族自治县隶属广西壮族自治区河池市，位于广西西北部，是全国著名的"世界长寿之乡"、
"中国长寿之乡"，右江革命根据地中心腹地之一。2026年为自治县成立70周年。全县总面积约1976
平方公里，常住人口约23.6万，辖1个镇10个乡。经济以长寿康养、包装水、香猪、油茶等产业为主，
为国家乡村振兴重点帮扶县。

Current leadership as of 2026-08 (sources: 广西县域经济网、人民网广西频道、百度百科、巴马县政府网站、广西纪检监察网):
- 县委书记: 韦涛（2023.11起，跨市调任）
- 县委副书记、县长: 余浩学（2023初起）

县委书记更替：覃荣武 → 奉海峰(2013.06-2016) → 王军(2016.06-2021.02) → 黄炳峰(2021-2023.11) → 韦涛(2023.11-)

Biographical data sourced from official government pages, appointment notices (任前公示),
and mainstream media. Confidence marked per person (见 report 与 open_gaps.md)。
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

SLUG = "巴马瑶族自治县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "巴马瑶族自治县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "巴马瑶族自治县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "巴马瑶族自治县_network.db"
    GEXF_PATH = GRAPH_DIR / "巴马瑶族自治县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共巴马瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 2, "name": "巴马瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 3, "name": "巴马瑶族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "河池市人大常委会", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 4, "name": "中国人民政治协商会议巴马瑶族自治县委员会", "type": "政协", "level": "县处级", "parent": "政协河池市委员会", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 5, "name": "中共巴马瑶族自治县纪律检查委员会/巴马瑶族自治县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共河池市纪委", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 6, "name": "巴马瑶族自治县人民武装部", "type": "军队", "level": "县处级", "parent": "河池军分区", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 7, "name": "中共来宾市象州县委员会", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市象州县"},
    {"id": 8, "name": "象州县人民政府", "type": "政府", "level": "县处级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市象州县"},
    {"id": 9, "name": "广西建工集团有限责任公司", "type": "国企", "level": "省属企业", "parent": "广西壮族自治区国资委", "location": "广西壮族自治区南宁市"},
    {"id": 10, "name": "中共来宾市兴宾区委员会", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市兴宾区"},
    {"id": 11, "name": "兴宾区人民政府", "type": "政府", "level": "县处级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市兴宾区"},
    {"id": 12, "name": "来宾市人力资源和社会保障局", "type": "政府", "level": "地厅级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市"},
    {"id": 13, "name": "中共合山市委员会", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市合山市"},
    {"id": 14, "name": "合山市人民政府", "type": "政府", "level": "县处级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市合山市"},
    {"id": 15, "name": "中共大化瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市大化瑶族自治县"},
    {"id": 16, "name": "大化瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市大化瑶族自治县"},
    {"id": 17, "name": "大化瑶族自治县雅龙乡人民政府", "type": "乡镇", "level": "乡科级", "parent": "大化瑶族自治县人民政府", "location": "广西壮族自治区河池市大化瑶族自治县"},
    {"id": 18, "name": "河池市发展和改革委员会", "type": "政府", "level": "地厅级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市"},
    {"id": 19, "name": "河池市扶贫开发办公室", "type": "政府", "level": "地厅级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市"},
    {"id": 20, "name": "中共河池市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区河池市"},
    {"id": 21, "name": "河池市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区河池市"},
    {"id": 22, "name": "中共环江毛南族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市环江毛南族自治县"},
    {"id": 23, "name": "环江毛南族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市环江毛南族自治县"},
    {"id": 24, "name": "中共都安瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市都安瑶族自治县"},
    {"id": 25, "name": "都安瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市都安瑶族自治县"},
    {"id": 26, "name": "中共天峨县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委", "location": "广西壮族自治区河池市天峨县"},
    {"id": 27, "name": "天峨县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市天峨县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 韦涛 — 县委书记（现任）
    {"id": 1, "name": "韦涛", "gender": "男", "ethnicity": "壮族",
     "birth": "1976年2月", "birthplace": "广西壮族自治区来宾市",
     "education": "在职大学学历（武汉冶金科技大学劳动人事管理专业、中南财经政法大学法学专业函授），在职研究生学历",
     "party_join": "2002年6月加入中国共产党", "work_start": "1997年8月参加工作",
     "current_post": "中共巴马瑶族自治县委书记、县人武部党委第一书记", "current_org": "中共巴马瑶族自治县委员会",
     "source": "http://m.gxcounty.com/show-30-180701-0.html"},
    # 2 — 余浩学 — 县长（现任）
    {"id": 2, "name": "余浩学", "gender": "男", "ethnicity": "瑶族",
     "birth": "1983年1月", "birthplace": "广西壮族自治区河池市",
     "education": "中南民族大学计算机科学学院数学与应用数学专业毕业，大学本科",
     "party_join": "2007年加入中国共产党", "work_start": "2006年参加工作",
     "current_post": "巴马瑶族自治县委副书记、县人民政府县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "https://www.newton.com.tw/wiki/%E4%BD%99%E6%B5%A9%E5%AD%B8/58995393"},
    # 3 — 黄永红 — 县人大常委会主任（现任）
    {"id": 3, "name": "黄永红", "gender": "男", "ethnicity": "瑶族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人大常委会主任", "current_org": "巴马瑶族自治县人民代表大会常务委员会",
     "source": "https://www.gxnews.com.cn/staticpages/20240126/newgx65b3342c-21417057.shtml"},
    # 4 — 罗彩梅 — 县政协主席（现任）
    {"id": 4, "name": "罗彩梅", "gender": "女", "ethnicity": "瑶族",
     "birth": "1970年", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县政协主席", "current_org": "中国人民政治协商会议巴马瑶族自治县委员会",
     "source": "http://www.zhongguolaoqu.com/index.php?a=show&c=index&catid=31&id=76488&m=content"},
    # 5 — 黄炳峰 — 前任县委书记（2021-2023.11）
    {"id": 5, "name": "黄炳峰", "gender": "男", "ethnicity": "毛南族",
     "birth": "", "birthplace": "广西壮族自治区环江毛南族自治县",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县原县委书记（2023.11卸任）", "current_org": "中共巴马瑶族自治县委员会",
     "source": "http://gx.people.com.cn/n2/2022/0117/c179464-35098807.html"},
    # 6 — 王军 — 前任县委书记、现任河池市市长
    {"id": 6, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "河池市委副书记、市人民政府市长", "current_org": "河池市人民政府",
     "source": "https://www.thepaper.cn/newsDetail_forward_11407035"},
    # 7 — 奉海峰 — 前任县委书记（2013-2016）
    {"id": 7, "name": "奉海峰", "gender": "男", "ethnicity": "瑶族",
     "birth": "1963年5月", "birthplace": "广西壮族自治区桂林市全州县",
     "education": "广西区党校研究生学历", "party_join": "1988年3月加入中国共产党", "work_start": "1981年9月参加工作",
     "current_post": "原巴马县委书记、河池市委常委（2013-2016）", "current_org": "中共巴马瑶族自治县委员会",
     "source": "http://district.ce.cn/newarea/sddy/201306/05/t20130605_24452501.shtml"},
    # 8 — 蓝海洲 — 前任县长（约2016-2022）
    {"id": 8, "name": "蓝海洲", "gender": "男", "ethnicity": "瑶族",
     "birth": "1968年3月", "birthplace": "广西壮族自治区大化瑶族自治县",
     "education": "大学学历", "party_join": "1993年2月加入中国共产党", "work_start": "",
     "current_post": "巴马瑶族自治县原县长（约2016-2022）", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://gxcounty.com/zhengwu/rsrm/20160503/124948.html"},
    # 9 — 蓝淞耀 — 县委常委、政法委书记
    {"id": 9, "name": "蓝淞耀", "gender": "男", "ethnicity": "瑶族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县委常委、政法委书记", "current_org": "中共巴马瑶族自治县委员会",
     "source": "https://c.m.163.com/news/a/L1HK1C8N05568W0A.html"},
    # 10 — 张高峰 — 县委常委、人武部政委
    {"id": 10, "name": "张高峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年8月", "birthplace": "",
     "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县委常委、县人民武装部政委", "current_org": "巴马瑶族自治县人民武装部",
     "source": "https://www.newton.com.tw/wiki/%E4%B8%AD%E5%9C%8B%E5%85%B1%E7%94%A2%E9%BB%A8%E5%B7%B4%E9%A6%AC%E7%91%A4"},
    # 11 — 梁光华 — 县委常委、统战部长
    {"id": 11, "name": "梁光华", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县委常委、统战部部长", "current_org": "中共巴马瑶族自治县委员会",
     "source": "https://znhd.guangxi.chinatax.gov.cn/hechi/gzdt_15548/xjgzdt_15550/202304/t20230419_386506.html"},
    # 12 — 吴昌勋 — 县委常委、县委办主任
    {"id": 12, "name": "吴昌勋", "gender": "男", "ethnicity": "瑶族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县委常委、县委办公室主任", "current_org": "中共巴马瑶族自治县委员会",
     "source": "https://www.zhongguolaoqu.com/index.php?a=show&c=index&catid=31&id=85063&m=content"},
    # 13 — 呼其日和 — 县委常委、副县长
    {"id": 13, "name": "呼其日和", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县委常委、副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://www.zhongguolaoqu.com/index.php?a=show&c=index&catid=31&id=76488&m=content"},
    # 14 — 韦健 — 县纪委书记/监委主任（2021年任上）
    {"id": 14, "name": "韦健", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县委常委、纪委书记、监委主任（2021年）", "current_org": "中共巴马瑶族自治县纪律检查委员会",
     "source": "https://www.gxjjw.gov.cn/staticpages/20210910/gxjjw613b3628-161934.shtml"},
    # 15 — 黄瑞吉 — 前巴马常委/宣传部长/副县长（现都安县长，落马）
    {"id": 15, "name": "黄瑞吉", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "都安瑶族自治县委副书记、县长（2025.09落马）", "current_org": "都安瑶族自治县人民政府",
     "source": "https://news.qq.com/rain/a/20250924A08DLU00"},
    # 16 — 王炳卜 — 前巴马副县长（现天峨县长）
    {"id": 16, "name": "王炳卜", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年12月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "2011年7月参加工作",
     "current_post": "天峨县委副书记、县长", "current_org": "天峨县人民政府",
     "source": "https://baike.baidu.com/item/%E7%8E%8B%E7%82%B3%E5%8D%9C/19131370"},
    # 17 — 蓝海洲前任县长（重复）— 已并入 #8；此处为副县长代表：林健
    {"id": 17, "name": "林健", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人民政府副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://www.zgcounty.com/news/40028.html"},
    # 18 — 陈彬 — 副县长
    {"id": 18, "name": "陈彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人民政府副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "https://c.m.163.com/news/a/L1HK1C8N05568W0A.html"},
    # 19 — 贝联准 — 副县长
    {"id": 19, "name": "韦联准", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人民政府副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://www.zgcounty.com/news/40028.html"},
    # 20 — 常珊 — 副县长
    {"id": 20, "name": "常珊", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人民政府副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://www.zgcounty.com/news/40028.html"},
    {"id": 21, "name": "隆甫", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人民政府副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://www.zgcounty.com/news/40028.html"},
    {"id": 22, "name": "罗明志", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人民政府副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://www.zgcounty.com/news/40028.html"},
    {"id": 23, "name": "苏玲", "gender": "女", "ethnicity": "壮族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巴马瑶族自治县人民政府副县长", "current_org": "巴马瑶族自治县人民政府",
     "source": "http://www.zgcounty.com/news/40028.html"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 韦涛
    {"person_id": 1, "org_id": 1, "title": "中共巴马瑶族自治县委书记", "start": "2023-11", "end": "present", "rank": "正处级", "note": "跨市调任，2024.01兼任县人武部党委第一书记"},
    {"person_id": 1, "org_id": 8, "title": "象州县委副书记、县长、县政府党组书记", "start": "2020-01", "end": "2023-11", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "兴宾区委常委、常务副区长", "start": "2019-02", "end": "2020-01", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "合山市委常委、常务副市长", "start": "2017-04", "end": "2019-02", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "来宾市人社局副局长、党组成员", "start": "2016-05", "end": "2017-04", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "兴宾区人民政府副区长", "start": "2009-08", "end": "2016-05", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "广西建工集团劳动人事部干部/教育培训中心副主任", "start": "1997-08", "end": "2009-08", "rank": "", "note": "建工集团内部任职"},
    # 余浩学
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "2023-01", "end": "present", "rank": "正处级", "note": "2022.12任前公示拟作为县长人选"},
    {"person_id": 2, "org_id": 15, "title": "大化县委常委、副县长（常务）", "start": "2021-07", "end": "2022-12", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 19, "title": "河池市扶贫开发办公室副主任", "start": "2018-07", "end": "2021-07", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 18, "title": "河池市发展改革委科长", "start": "2012-11", "end": "2018-06", "rank": "", "note": "投资科/综合规划科"},
    {"person_id": 2, "org_id": 17, "title": "大化县雅龙乡党政办秘书/组织委员/副乡长", "start": "2006-07", "end": "2012-11", "rank": "", "note": ""},
    # 黄永红
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start": "2023", "end": "present", "rank": "正处级", "note": ""},
    # 罗彩梅
    {"person_id": 4, "org_id": 4, "title": "县政协主席", "start": "2023", "end": "present", "rank": "正处级", "note": ""},
    # 黄炳峰（前任书记）
    {"person_id": 5, "org_id": 1, "title": "县委书记", "start": "2021", "end": "2023-11", "rank": "正处级", "note": "韦涛直接前任"},
    {"person_id": 5, "org_id": 23, "title": "环江毛南族自治县县长", "start": "", "end": "2021", "rank": "正处级", "note": "2021年河组示〔2021〕3号拟进一步使用为县党委书记"},
    # 王军
    {"person_id": 6, "org_id": 21, "title": "河池市委副书记、市长", "start": "2021-03", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "巴马县委书记", "start": "2016-06", "end": "2021-02", "rank": "正处级", "note": "2020.12-2021.04兼任河池市委常委"},
    # 奉海峰
    {"person_id": 7, "org_id": 1, "title": "巴马县委书记、河池市委常委", "start": "2013-06", "end": "2016-06", "rank": "正处级/副厅", "note": ""},
    # 蓝海洲（前任县长）
    {"person_id": 8, "org_id": 2, "title": "巴马县委副书记、县长", "start": "2016-06", "end": "2022-12", "rank": "正处级", "note": ""},
    # 蓝淞耀
    {"person_id": 9, "org_id": 1, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张高峰
    {"person_id": 10, "org_id": 6, "title": "县委常委、人武部政委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 梁光华
    {"person_id": 11, "org_id": 1, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "2023.04任上"},
    # 吴昌勋
    {"person_id": 12, "org_id": 1, "title": "县委常委、县委办主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 呼其日和
    {"person_id": 13, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "2025外出考察"},
    # 韦健
    {"person_id": 14, "org_id": 5, "title": "纪委书记、监委主任（常委）", "start": "", "end": "2021", "rank": "副处级", "note": "2021年任上，现任待核"},
    # 黄瑞吉
    {"person_id": 15, "org_id": 25, "title": "都安县委副书记、县长", "start": "2019", "end": "2025-09", "rank": "正处级", "note": "2025.09涉嫌违纪违法被查"},
    {"person_id": 15, "org_id": 1, "title": "巴马县委常委、宣传部部长、副县长", "start": "", "end": "2018", "rank": "副处级", "note": ""},
    # 王炳卜
    {"person_id": 16, "org_id": 27, "title": "天峨县委副书记、县长", "start": "2023", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "巴马瑶族自治县副县长", "start": "", "end": "2020", "rank": "副处级", "note": ""},
    # 副县长
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "韦涛（县委书记）与余浩学（县长）为巴马县党政主要一把手，同一班子共事", "overlap_org": "巴马县", "overlap_period": "2023至今"},
    {"person_a": 5, "person_b": 2, "type": "党政搭档", "context": "黄炳峰（书记）与 余浩学（县长）曾共事（2023年初起），余浩学在黄炳峰任内任县长", "overlap_org": "巴马县", "overlap_period": "2023"},
    {"person_a": 5, "person_b": 1, "type": "predecessor_successor", "context": "黄炳峰为韦涛的直接前任巴马县委书记", "overlap_org": "巴马县", "overlap_period": "2023"},
    {"person_a": 6, "person_b": 5, "type": "predecessor_successor", "context": "王军（2016-2021书记）卸任后由黄炳峰接任", "overlap_org": "巴马县", "overlap_period": "2021"},
    {"person_a": 6, "person_b": 1, "type": "inferred", "context": "王军曾任巴马县委书记，现为河池市长，韦涛任巴马书记属河池市委领导下工作", "overlap_org": "河池市", "overlap_period": "2023至今"},
    {"person_a": 2, "person_b": 15, "type": "same_system", "context": "余浩学任巴马县长，黄瑞吉曾在巴马任子宣传部长/副县长，后在都安任县长被查", "overlap_org": "巴马县", "overlap_period": "不确定"},
    {"person_a": 8, "person_b": 2, "type": "predecessor_successor", "context": "蓝海洲（前任县长）卸任后由余浩学接任", "overlap_org": "巴马县", "overlap_period": "2022-2023"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "吴昌勋（县委办主任）在韦涛（书记）领导下工作", "overlap_org": "巴马县", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "韦涛书记与分管政法的常委蓝淞耀共事", "overlap_org": "巴马县", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "韦涛书记与常委副县长呼其日和共事", "overlap_org": "巴马县", "overlap_period": "2023至今"},
    {"person_a": 2, "person_b": 16, "type": "cross_county_exchange", "context": "余浩学（县长）与王炳阗（天峨县长）均被列为河池县级领导，王炳阗曾任巴马副县长", "overlap_org": "河池市", "overlap_period": ""},
    {"person_a": 1, "person_b": 16, "type": "cross_county_exchange", "context": "韦涛（巴马书记）、王炳卜（曾巴马副县长，现天峨县长）跨县调任网络", "overlap_org": "河池市", "overlap_period": ""},
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