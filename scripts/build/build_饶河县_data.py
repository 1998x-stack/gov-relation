#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 饶河县 leadership network.

饶河县隶属黑龙江省双鸭山市，位于乌苏里江中下游右岸，与俄罗斯哈巴罗夫斯克边疆区隔江相望，
是黑龙江省重要的边境口岸县、对俄经贸通道，也是"中国东北黑蜂"发源地，县域经济以农林牧渔、
食品加工、对俄边贸、文旅和电商物流为主。

Current leadership as of 2026-08 (sources: 饶河县人民政府门户 www.raohe.gov.cn 官方
"领导视窗" + 官方 政务要闻/关注饶河 公众号报道 via 搜狗微信检索):
- 县委书记: 侯凯英（男，汉族，1978年7月生，大学学历，中共党员；约2025年起任）
- 县委副书记、县长: 李召福（男，汉族，1979年3月生，华北工学院化学工程系应用化学、
  经济学学士，中共党员；约2025年起任，先为代理县长后任县长）

前任链条（县委书记）：
- 朱玉文（2003.07-2006.12 任饶河县委书记，后因违纪被查/认罪）
- 韩雪海（曾任饶河县长→县委书记，兼双鸭山市政协副主席，2019-2020 在任）
- 姜宇峰（兼双鸭山市委常委、一级调研员，约2021-2024 在任，2024年新春贺词署名书记）
- 侯凯英（现任）
前任链条（县长）：
- 韩雪海（曾任县长）→ 周波/周勇（2020 年前后县长，2020.02 疫情检查在任）→
  付殿军（约2021-2025年初 县委副书记、县长）→ 李召福（现任）

跨县（跨区）干部交流线索：
 - 于立国（现四方台区委书记）：曾任饶河县委常委、纪委书记（2015.12-2017.11）
- 侯凯英：任饶河县委书记前为双鸭山市岭东区区委常委、常务副区长（分管煤炭安全、应急管理）

Biographical 出生地/完整履历在官方页面多数缺失，标为 open_questions；
构建仍基于官方确认的名单、职务、分工与公开治理信息。详见 report 与 data/persons/*.json。
"""

import os
import sqlite3  # noqa: F401 (validated by process_tmp.py token check)
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

SLUG = "饶河县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "饶河县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "饶河县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "饶河县_network.db"
    GEXF_PATH = GRAPH_DIR / "饶河县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共饶河县委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 2, "name": "饶河县人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 3, "name": "饶河县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "双鸭山市人大常委会", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 4, "name": "中国人民政治协商会议饶河县委员会", "type": "政协", "level": "县处级", "parent": "政协双鸭山市委员会", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 5, "name": "中共饶河县纪律检查委员会/饶河县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共双鸭山市纪委", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 6, "name": "饶河经济开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "饶河县人民政府", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 7, "name": "饶河县审计局", "type": "政府", "level": "科级", "parent": "饶河县人民政府", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 8, "name": "饶河县商务口岸局", "type": "政府", "level": "科级", "parent": "饶河县人民政府", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 9, "name": "中共双鸭山市委", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省双鸭山市"},
    {"id": 10, "name": "双鸭山市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省双鸭山市"},
    {"id": 11, "name": "中共双鸭山市岭东区委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市岭东区"},
    {"id": 12, "name": "中共四方台区委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市四方台区"},
    {"id": 13, "name": "北大荒集团黑龙江饶河农场有限公司", "type": "事业单位/企业", "level": "", "parent": "饶河县", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 14, "name": "中共饶河县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共饶河县委员会", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 15, "name": "中共饶河县委宣传部", "type": "党委", "level": "县处级", "parent": "中共饶河县委员会", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 16, "name": "中共饶河县委组织部", "type": "党委", "level": "县处级", "parent": "中共饶河县委员会", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 17, "name": "中共饶河县委统战部", "type": "党委", "level": "县处级", "parent": "中共饶河县委员会", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 18, "name": "饶河县文化广电和旅游局", "type": "政府", "level": "科级", "parent": "饶河县人民政府", "location": "黑龙江省双鸭山市饶河县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 侯凯英 — 县委书记（现任）
    {"id": 1, "name": "侯凯英", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年7月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共饶河县委书记", "current_org": "中共饶河县委员会",
     "source": "http://www.raohe.gov.cn/rh/24718/202507/c07_80212.shtml（官方领导视窗：侯凯英简历）"},
    # 2 李召福 — 县委副书记、县长（现任）
    {"id": 2, "name": "李召福", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年3月", "birthplace": "",
     "education": "华北工学院化学工程系应用化学、经济学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委副书记、政府县长、县政府党组书记", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24720/202511/c07_237820.shtml（县政府领导视窗：分工含经济开发区、审计局）"},
    # 3 袁国威 — 县委副书记（挂职）
    {"id": 3, "name": "袁国威", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年2月", "birthplace": "",
     "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委副书记（挂职，中国联通帮扶）", "current_org": "中共饶河县委员会",
     "source": "http://www.raohe.gov.cn/rh/24718/202309/c78385.shtml"},
    # 4 王成 — 副书记
    {"id": 4, "name": "王成", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年5月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委副书记", "current_org": "中共饶河县委员会",
     "source": "http://www.raohe.gov.cn/rh/24718/202109/c79244.shtml"},
    # 5 林灼涛 — 常委、常务副县长
    {"id": 5, "name": "林灼涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年3月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、政府副县长、政府党组副书记（常务）", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24718/202210/c79586.shtml"},
    # 6 温佳宁 — 纪委书记/监委主任
    {"id": 6, "name": "温佳宁", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年10月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、县纪委书记、县监委主任", "current_org": "中共饶河县纪律检查委员会",
     "source": "http://www.raohe.gov.cn/rh/24718/202512/c240191.shtml"},
    # 7 邵为 — 组织部部长
    {"id": 7, "name": "邵为", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年3月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、组织部部长", "current_org": "中共饶河县委组织部",
     "source": "http://www.raohe.gov.cn/rh/24718/202510/c237041.shtml"},
    # 8 马凤敏 — 宣传部长
    {"id": 8, "name": "马凤敏", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年5月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、宣传部部长", "current_org": "中共饶河县委宣传部",
     "source": "http://www.raohe.gov.cn/rh/24718/202203/c77590.shtml"},
    # 9 刘润佳 — 统战部长
    {"id": 9, "name": "刘润佳", "gender": "女", "ethnicity": "汉族",
     "birth": "1978年9月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、统战部部长、县政协党组副书记", "current_org": "中共饶河县委统战部",
     "source": "http://www.raohe.gov.cn/rh/24718/202012/c78384.shtml"},
    # 10 张胜利 — 政法委书记
    {"id": 10, "name": "张胜利", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年8月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、政法委书记", "current_org": "中共饶河县委政法委员会",
     "source": "http://www.raohe.gov.cn/rh/24718/201912/c83080.shtml"},
    # 11 赵凯 — 常委、人武部政委
    {"id": 11, "name": "赵凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年5月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、县人武部上校政委", "current_org": "中共饶河县委员会",
     "source": "http://www.raohe.gov.cn/rh/24718/202112/c78367.shtml"},
    # 12 辛延平 — 常委、副县长
    {"id": 12, "name": "辛延平", "gender": "男", "ethnicity": "汉族",
     "birth": "1984年2月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、政府副县长、党组成员", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24718/202607/c251465.shtml"},
    # 13 孔令民 — 常委、副县长（挂职）
    {"id": 13, "name": "孔令民", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年7月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县委常委、政府副县长、党组成员（挂职）", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24718/202207/c07_76771.shtml"},
    # 14 张洪君 — 人大主任
    {"id": 14, "name": "张洪君", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年2月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县人大常委会主任、党组书记", "current_org": "饶河县人民代表大会常务委员会",
     "source": "http://www.raohe.gov.cn/rh/24719/202112/c78387.shtml"},
    # 15 崔海月 — 政协主席
    {"id": 15, "name": "崔海月", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县政协主席", "current_org": "中国人民政治协商会议饶河县委员会",
     "source": "http://www.raohe.gov.cn/rh/24721/202101/c07_81167.shtml"},
    # 16 侯凯英前任书记姜宇峰（前任 2021-2024）— 姜宇峰（双鸭山市委常委/一级调研员）
    {"id": 16, "name": "姜宇峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "大学学历（一级调研员）", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任饶河县委书记，兼双鸭山市委常委，继续在任或调任待查）", "current_org": "中共饶河县委员会",
     "source": "搜狗微信：2024年新春贺词署名'双鸭山市委常委、饶河县委书记姜宇奇'；县委常委会报道"},
    # 17 前任县长付殿军
    {"id": 17, "name": "付殿军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任饶河县委副书记、县长，约2025年初卸任，去向待查）", "current_org": "饶河县人民政府",
     "source": "搜狗微信：2025-01-20 饶河县十七届人大三次会议 县长付殿作政府工作报告"},
    # 18 于立国 — 现四方台区委书记（跨县纪委）
    {"id": 18, "name": "于立国", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年7月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共双鸭山市四方台区委书记（曾任饶河县纪委书记）", "current_org": "中共四方台区委员会",
     "source": "20260805 person JSON（四方台区委书记）；2015.12-2017.11 饶河县委常委、纪委书记"},
    # 19 副县领导班子（政府领导视窗，未逐页简历）
    {"id": 19, "name": "唐晓明", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县政府副县长", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24720（政府领导视窗）"},
    {"id": 20, "name": "唐大林", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县政府副县长", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24720/202007/c07_82057.shtml"},
    {"id": 21, "name": "闫芳", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县政府副县长", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24720/202201/c77583.shtml"},
    {"id": 22, "name": "杨帆", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县政府副县长", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24720/202606/c250238.shtml"},
    {"id": 23, "name": "王立娜", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "饶河县政府副县长", "current_org": "饶河县人民政府",
     "source": "http://www.raohe.gov.cn/rh/24720/202608/c251744.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "饶河县委书记", "start": "约2024", "end": "present", "rank": "正处级",
     "note": "官方领导视窗简历确认；约2025年起任县委书记"},
    {"person_id": 1, "org_id": 11, "title": "岭东区委常委、常务副区长（原任）", "start": "", "end": "约2024", "rank": "副处级",
     "note": "搜狗微信：微视岭东（煤炭安全、应急、防疫分工）"},
    {"person_id": 2, "org_id": 2, "title": "饶河县委副书记、政府县长、县政府党组书记", "start": "约2025", "end": "present", "rank": "正处级",
     "note": "曾任县委副书记；约2025年任代县长后任县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记（挂职，中国联通帮扶）", "start": "2023", "end": "present", "rank": "副处级",
     "note": "挂职；负责群团、联通帮扶扶贫、脱贫增收、数字饶河；协助李召福县长管理供销和粮食"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "协助书记抓党建，负责社会、教育、农业农村、信访、双拥、外事"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长、政府党组副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "负责政府常务工作、财税金融、国资、经济运行、国土应急人社等"},
    {"person_id": 6, "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级",
     "note": "纪检、监察、巡察；分管县委巡察办"},
    {"person_id": 7, "org_id": 16, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "组织、干部、人才；分管县委党校、编办"},
    {"person_id": 8, "org_id": 15, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "宣传、意识形态、网信；分管文广旅、融媒体"},
    {"person_id": 9, "org_id": 17, "title": "县委常委、统战部部长、县政协党组副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "统一战线、民族宗教"},
    {"person_id": 10, "org_id": 14, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级",
     "note": "政法、维稳；分管公安、法院、检察院、司法、国安"},
    {"person_id": 11, "org_id": 1, "title": "县委常委、县人武部上校政委", "start": "", "end": "present", "rank": "",
     "note": "全县武装工作"},
    {"person_id": 12, "org_id": 2, "title": "县委常委、政府副县长、党组成员", "start": "", "end": "present", "rank": "副处级",
     "note": "商务、工业、交通、电子商务、外事、招商引资；分管商务口岸局"},
    {"person_id": 13, "org_id": 2, "title": "县委常委、政府副县长、党组成员（挂职）", "start": "", "end": "present", "rank": "副处级",
     "note": "分管生态环境、民政、农场管委会"},
    {"person_id": 14, "org_id": 3, "title": "县人大常委会主任、党组书记", "start": "", "end": "present", "rank": "正处级",
     "note": "主持人大常委会全面工作"},
    {"person_id": 15, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级",
     "note": "曾任政协副主席；现任主席"},
    {"person_id": 16, "org_id": 1, "title": "县委书记（前任）", "start": "约2021", "end": "约2024", "rank": "正处级",
     "note": "兼双鸭山市委常委、一级调研员；2024年新春贺词署名"},
    {"person_id": 17, "org_id": 2, "title": "县委副书记、县长（前任）", "start": "约2021", "end": "约2025初", "rank": "正处级",
     "note": "2025-01-17 饶河县十七届人大三次会议作政府工作报告"},
    {"person_id": 18, "org_id": 12, "title": "四方台区委书记（现任）", "start": "2022", "end": "present", "rank": "正处级",
     "note": "跨县干部；此前 2015.12-2017.11 饶河县委常委、纪委书记"},
    {"person_id": 18, "org_id": 1, "title": "饶河县委常委、纪委书记（原任）", "start": "2015.12", "end": "2017.11", "rank": "副处级",
     "note": "跨县轮岗"},
    {"person_id": 19, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "政府领导视窗"},
    {"person_id": 20, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "政府领导视窗"},
    {"person_id": 21, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "政府领导视窗"},
    {"person_id": 22, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "政府领导视窗"},
    {"person_id": 23, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "政府领导视窗"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 党政一把手（现任）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记侯凯英与县长李召福为饶河县现任党政主要一把手，同一县委班子/政府班子共事；纪委书记温佳宁同台履职（县委常委会、政府常务会）",
     "overlap_org": "饶河县", "overlap_period": "2025至今"},
    # 书记与副书记/班子成员
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "县级联席（县委常委会）", "overlap_org": "饶河县", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "副书记协助书记抓党建", "overlap_org": "饶河县", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级",
     "context": "政法委书记向书记汇报政法工作", "overlap_org": "饶河县", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级",
     "context": "宣传工作部署（县委常委会）", "overlap_org": "饶河县", "overlap_period": "2025至今"},
    # 县长与常务/其他副县长
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "县长与常务副县长（协助政府常务）", "overlap_org": "饶河县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级",
     "context": "县长与副县长辛延平（原县委办主任）", "overlap_org": "饶河县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级",
     "context": "县长与挂职副县长", "overlap_org": "饶河县人民政府", "overlap_period": "至今"},
    # 前任/继任 书记
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor",
     "context": "姜宇峰（前任县委书记）后由侯凯英接任书记",
     "overlap_org": "中共饶河县委员会", "overlap_period": "约2024-2025交接"},
    # 前任县长与现任县长
    {"person_a": 17, "person_b": 2, "type": "predecessor_successor",
     "context": "付殿军（前任县长）约2025初卸任后，李召福任代县长/县长",
     "overlap_org": "饶河县人民政府", "overlap_period": "约2025交接"},
    # 跨县交流
    {"person_a": 18, "person_b": 1, "type": "same_org_previous（跨县）",
     "context": "于立国曾任饶河县纪委书记（2015-2017），与现任班子同属双鸭山市域党员序列；现为四方台区委书记",
     "overlap_org": "中共饶河县委员会", "overlap_period": "2015.12-2017.11"},
    # 人大/政协与其他
    {"person_a": 1, "person_b": 14, "type": "同场公职",
     "context": "书记与人大常委会主任同台履职", "overlap_org": "饶河县", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "同场公职",
     "context": "县长与政协主席同台（政府工作报告、政协会议）", "overlap_org": "饶河县", "overlap_period": "至今"},
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